import json
import threading
import os
from config.config import COIN_NAME, TRADE_AMOUNT
from core.binance_api import binance

TRADE_FILE = "data/current_trade.json"
trade_lock = threading.Lock()  # Prevents race conditions when updating JSON

# Ensure the data directory exists
os.makedirs(os.path.dirname(TRADE_FILE), exist_ok=True)

def save_trade_state(trade_data):
    """Save trade state to JSON file."""
    try:
        with open(TRADE_FILE, "w") as f:
            json.dump(trade_data, f, indent=4)
        print("✅ Trade state saved successfully!")
    except Exception as e:
        print(f"❌ Error saving trade state: {e}")

def load_trade_state():
    """Load trade state from JSON file."""
    if os.path.exists(TRADE_FILE):  # Check if file exists
        try:
            with open(TRADE_FILE, "r") as f:
                trade_data = json.load(f)
            return trade_data if trade_data else None  # Return None if file is empty
        except json.JSONDecodeError:
            print(f"⚠️ Error: Corrupted JSON in {TRADE_FILE}. Resetting...")
            save_trade_state({})
        except Exception as e:
            print(f"⚠️ Error loading trade state: {e}")
    return None

def place_order(symbol, order_type, amount):
    """Simulate placing an order and updating JSON trade state."""
    global trade_lock
    try:
        if order_type == "buy":
            order = binance.create_market_buy_order(symbol, amount)
            buy_price = order.get("price") or binance.fetch_ticker(symbol)["last"]
            stop_loss_price = buy_price * 0.98
            take_profit_price = buy_price * 1.05

            trade_data = {
                "buy_price": buy_price,
                "stop_loss": stop_loss_price,
                "take_profit": take_profit_price,
                "status": "open",
                "symbol": symbol,
                "amount": amount
            }

            with trade_lock:
                save_trade_state(trade_data)

            print(f"✅ BUY Order at {buy_price}, SL: {stop_loss_price}, TP: {take_profit_price}")
            return buy_price, stop_loss_price, take_profit_price

        elif order_type == "sell":
            trade_data = load_trade_state() or {}

            if trade_data and trade_data != {} and trade_data.get("status") == "open":  # Ensure trade is active
                sell_price = binance.fetch_ticker(symbol)["last"]  # Get current price
                trade_data["status"] = "close"
                save_trade_state(trade_data)  # Save updated trade data                    

                print(f"✅ SELL Order at {sell_price}. Trade status updated to 'close'.")
                return sell_price

            else:
                print(f"⚠️ No active trade found to close.")

    except Exception as e:
        print(f"⚠️ Order Failed: {str(e)}")
        return None, None, None
