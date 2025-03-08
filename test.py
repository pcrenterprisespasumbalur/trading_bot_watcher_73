from core.binance_api import binance
 
try:
    market_data = binance.fetch_ticker("BTC/USDT")
    print("✅ Market Data:", market_data)
except Exception as e:
    print("❌ Binance API Error:", e)
