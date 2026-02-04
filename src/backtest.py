from __future__ import annotations
import math
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .norm import norm_cdf

@dataclass
class BacktestResult:
    alpha: float
    n: int
    exceptions: int
    exception_rate: float
    kupiec_LR: float
    kupiec_p_value: float

def kupiec(exceptions: int, n: int, alpha: float) -> tuple[float, float]:
    """Kupiec unconditional coverage test (1 df)."""
    if n <= 0:
        raise ValueError("n must be positive")

    p = 1 - alpha
    x = max(0, min(int(exceptions), int(n)))

    # Avoid log(0)
    if x == 0:
        phat = 1e-7
    elif x == n:
        phat = 1 - 1e-7
    else:
        phat = x / n

    ll0 = (n-x)*math.log(1-p) + x*math.log(p)
    ll1 = (n-x)*math.log(1-phat) + x*math.log(phat)
    lr = -2*(ll0 - ll1)

    # Chi-square(1) survival without SciPy
    pv = 2.0 * (1.0 - norm_cdf(math.sqrt(max(lr, 0.0))))
    pv = max(min(pv, 1.0), 0.0)
    return float(lr), float(pv)

def backtest_var(returns: pd.Series, var_fc: pd.Series, alpha: float) -> BacktestResult:
    r = returns.loc[var_fc.index].dropna()
    v = var_fc.loc[r.index].astype(float)
    exc = int(np.sum((-r.values) > v.values))
    n = int(len(r))
    lr, pv = kupiec(exc, n, alpha)
    return BacktestResult(alpha, n, exc, exc/n if n else float("nan"), lr, pv)
