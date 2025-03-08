from core.binance_api import binance

# Change the API endpoint (if required)
binance.urls["api"] = "https://api.binance.us"  # For Binance.US users

try:
    market_data = binance.fetch_ticker("BTC/USDT")
    print("✅ Market Data:", market_data)
except Exception as e:
    print("❌ Binance API Error:", e)
