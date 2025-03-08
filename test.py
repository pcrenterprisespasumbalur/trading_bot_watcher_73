from core.binance_api import binance,binanceus
import ccxt
# Increase request timeout
binance.timeout = 60000  # 60 seconds timeout



try:
    market_data = binanceus.fetch_ticker("BTC/USDT")
    print("✅ Market Data:", market_data)
except ccxt.NetworkError as e:
    print(f"⚠️ Network error: {e}")
except ccxt.ExchangeError as e:
    print(f"⚠️ Binance API error: {e}")
except Exception as e:
    print("❌ Binance API Error:", e)
