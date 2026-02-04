from __future__ import annotations
import pathlib
import pandas as pd

def load_prices(path: str | pathlib.Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns or "close" not in df.columns:
        raise ValueError("CSV must contain columns: date, close")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def returns_from_close(close: pd.Series) -> pd.Series:
    return close.pct_change()
