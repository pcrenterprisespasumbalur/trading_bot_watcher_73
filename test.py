from core.binance_api import binance
import ccxt
 
try:
    market_data = binance.fetch_ticker("BTC/USDT")
    print("✅ Market Data:", market_data)
except ccxt.NetworkError as e:
        print(f"⚠️ Network error: {e}")
except ccxt.ExchangeError as e:
        print(f"⚠️ Binance API error: {e}")
except Exception as e:
    print("❌ Binance API Error:", e)
