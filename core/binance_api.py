import ccxt
import pandas as pd
from config.config import API_KEY, API_SECRET

binance = ccxt.binance({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "options": {"adjustForTimeDifference": True},
})
binanceus = ccxt.binanceus({
    "apiKey": API_KEY,
    "secret": API_SECRET,
    "timeout": 30000,  # Increase timeout to 30 seconds
    "options": {"adjustForTimeDifference": True},
})

def fetch_market_data(symbol="BTC/USDT", timeframe="5m", limit=100):
    try:
        bars = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not bars:
            print("❌ No data received from Binance!")
            return None

        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        print(f"❌ Error Fetching Data: {str(e)}")
        return None
