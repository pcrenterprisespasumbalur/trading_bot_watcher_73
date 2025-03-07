import schedule
import time
from config.config import COIN_NAME, TIMEFRAME, LIMIT, TRADE_AMOUNT
from core.binance_api import fetch_market_data
from core.strategy import apply_strategy
from core.trade_manager import load_trade_state, place_order
import json

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

schedule.every(5).minutes.do(run_bot)

while True:
    print(f"🔄 Running Trading Bot at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    schedule.run_pending()
    time.sleep(60)