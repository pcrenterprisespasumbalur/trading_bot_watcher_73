import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

def find_support_resistance(df, window=20):
    """Detects support and resistance levels from market data."""
    if df is None or df.empty or len(df) <= window:
        return [], []

    df["min"] = np.nan
    df["max"] = np.nan
    df.loc[df.index[argrelextrema(df["low"].values, np.less_equal, order=window)], "min"] = df["low"]
    df.loc[df.index[argrelextrema(df["high"].values, np.greater_equal, order=window)], "max"] = df["high"]

    return df["min"].dropna().tolist(), df["max"].dropna().tolist()

def apply_strategy(df):
    """Applies strategy to determine buy/sell signals."""
    support_levels, resistance_levels = find_support_resistance(df)
    latest_close = df["close"].iloc[-1]

    for support in support_levels:
        if latest_close <= support * 1.02:
            return "buy", support

    for resistance in resistance_levels:
        if latest_close >= resistance * 0.98:
            return "sell", resistance

    return "hold", None
