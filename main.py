import schedule
import time
from config.config import COIN_NAME, TIMEFRAME, LIMIT, TRADE_AMOUNT
from core.binance_api import fetch_market_data
from core.strategy import apply_strategy
from core.trade_manager import load_trade_state, place_order
import json
import os
from core.binance_api import binance

TRADE_FILE = "data/current_trade.json"

# Ensure data directory exists
os.makedirs(os.path.dirname(TRADE_FILE), exist_ok=True)

def run_bot():
    """Main function to run the trading bot."""
    
    df = fetch_market_data(COIN_NAME, TIMEFRAME, LIMIT)
    if df is None:
        print("⚠️ No market data, skipping cycle.")
        return

    signal, level = apply_strategy(df)
    latest_price = df["close"].iloc[-1]
    print(f"📈 Signal: {signal}, Level: {level}, Current Price: {latest_price}")

    current_trade = load_trade_state()

    if signal == "buy" and (not current_trade or current_trade == {} or current_trade.get("status") != "open"):
        print("✅ BUY Signal! Placing order.")
        place_order(COIN_NAME, "buy", TRADE_AMOUNT)

    elif signal == "sell" and current_trade:
        print("❌ SELL Signal! Closing trade.")
        place_order(COIN_NAME, "sell", TRADE_AMOUNT)
        
def load_trade_state_w():
    """Load the current trade state from JSON."""
    if os.path.exists(TRADE_FILE):
        try:
            with open(TRADE_FILE, "r") as f:
                trade_data = json.load(f)
                return trade_data if trade_data else None  # Handle empty file
        except json.JSONDecodeError:
            print(f"⚠️ Error: Corrupted JSON in {TRADE_FILE}. Resetting...")
            save_trade_state({})  # Reset file
        except Exception as e:
            print(f"⚠️ Error loading trade state: {e}")
    return None

def save_trade_state(trade_data):
    """Save the trade state to JSON."""
    try:
        with open(TRADE_FILE, "w") as f:
            json.dump(trade_data, f, indent=4)
    except Exception as e:
        print(f"❌ Error saving trade state: {e}")
 
def close_trade(symbol):
    """Close trade by placing a market sell order for the open order amount."""
    try:
        balance = binance.fetch_balance()
        coin_symbol = symbol.split("/")[0]        
        order_amount = balance['total'].get(coin_symbol, 0)
        
        if order_amount <= 0:
            print(f"⚠️ No remaining amount to sell for {symbol}.")
            return

        # ✅ Place a market sell order for the exact remaining amount
        order = binance.create_market_sell_order(symbol, order_amount)
        print(f"✅ SELL Order Executed: Sold {order_amount} of {symbol}. Trade Closed.")

        # ✅ Reset trade file after selling
        save_trade_state({})  

    except Exception as e:
        print(f"⚠️ Failed to close trade for {symbol}: {str(e)}")

def monitor_trade():
    """Check trade status and close if SL or TP is hit."""
    print("🔄 Checking trade status...")
    trade_data = load_trade_state_w()    
    
    if trade_data and trade_data.get("status") == "open":
        required_keys = {"symbol", "stop_loss", "take_profit", "amount"}
        if not required_keys.issubset(trade_data.keys()):
            print(f"⚠️ Incomplete trade data! Missing keys: {required_keys - trade_data.keys()}")
            return

        symbol = trade_data["symbol"]
        stop_loss = trade_data["stop_loss"]
        take_profit = trade_data["take_profit"]
        amount = trade_data["amount"]

        try:
            market_data = binance.fetch_ticker(symbol)
            if not market_data or "last" not in market_data:
                print(f"⚠️ Error fetching market price for {symbol}.")
                return

            market_price = market_data["last"]
            print(f"📊 {symbol} - Price: {market_price} | SL: {stop_loss} | TP: {take_profit} | Amount: {amount}")

            if market_price <= stop_loss or market_price >= take_profit:
                print(f"⚠️ Price hit SL or TP for {symbol}! Closing trade...")
                close_trade(symbol)

        except Exception as e:
            print(f"❌ Error fetching market price: {str(e)}")
            
    elif trade_data and trade_data.get("status") == "close":
        try:
            symbol = trade_data["symbol"]
            print(f"⚠️ Price hit sell for {symbol}! Closing trade...")
            close_trade(symbol)
        except Exception as e:
            print(f"❌ Error closing trade: {str(e)}")

# Schedule the function to run every 10 seconds
schedule.every(3).seconds.do(monitor_trade) 
schedule.every(5).minutes.do(run_bot)

while True:
    print(f"🔄 Running Trading Bot at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    schedule.run_pending()
    time.sleep(60)
