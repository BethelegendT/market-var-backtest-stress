from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class Scenario:
    name: str
    shock_return: float
    vol_mult: float

def apply_scenario(returns: pd.Series, sc: Scenario) -> pd.Series:
    r = returns.dropna().astype(float)
    mu = r.mean()
    centered = r - mu
    return mu + sc.vol_mult*centered + sc.shock_return

def worst_window_sum(returns: pd.Series, window: int = 20):
    r = returns.dropna().astype(float)
    s = r.rolling(window).sum()
    t = s.idxmin()
    return t, float(s.loc[t])
