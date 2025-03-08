from core.binance_api import binance
import ccxt
from config.config import API_KEY, API_SECRET
 
try:
client = Client(API_KEY, API_SECRET, tld="us")

balance = client.get_asset_balance(asset="USDT")
print(f"💰 USDT Balance: {balance['free']}")
except ccxt.NetworkError as e:
        print(f"⚠️ Network error: {e}")
except ccxt.ExchangeError as e:
        print(f"⚠️ Binance API error: {e}")
except Exception as e:
    print("❌ Binance API Error:", e)
