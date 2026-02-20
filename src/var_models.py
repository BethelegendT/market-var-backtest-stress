from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .norm import norm_ppf


@dataclass
class VarResult:
    alpha: float
    var: float  # positive loss threshold
    es: float  # positive tail mean loss


def _clean(r: pd.Series) -> pd.Series:
    r = r.dropna().astype(float)
    if r.empty:
        raise ValueError("empty returns after dropping NA")
    return r


def historical_var_es(returns: pd.Series, alpha: float = 0.99) -> VarResult:
    r = _clean(returns)
    losses = (-r).values
    q = float(np.quantile(losses, alpha))
    tail = losses[losses >= q]
    es = float(tail.mean()) if len(tail) else q
    return VarResult(alpha, q, es)


def parametric_var_es(returns: pd.Series, alpha: float = 0.99) -> VarResult:
    r = _clean(returns)
    mu = float(r.mean())
    sigma = float(r.std(ddof=1))
    z = norm_ppf(alpha)

    # Loss L = -R; VaR_alpha = -(mu - z*sigma)
    var = -(mu - z * sigma)

    phi = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z * z)
    es = -(mu - sigma * (phi / (1 - alpha)))
    return VarResult(alpha, float(var), float(es))


def ewma_sigma(returns: pd.Series, lam: float = 0.94) -> pd.Series:
    r = _clean(returns)
    x = r.values
    s2 = np.zeros_like(x)

    s2[0] = np.var(x[:30]) if len(x) >= 30 else np.var(x)
    for t in range(1, len(x)):
        s2[t] = lam * s2[t - 1] + (1 - lam) * (x[t - 1] ** 2)

    return pd.Series(np.sqrt(s2), index=r.index)


def ewma_var_es(returns: pd.Series, alpha: float = 0.99, lam: float = 0.94) -> VarResult:
    r = _clean(returns)
    sigma = float(ewma_sigma(r, lam=lam).iloc[-1])
    z = norm_ppf(alpha)

    var = z * sigma

    phi = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z * z)
    es = sigma * (phi / (1 - alpha))
    return VarResult(alpha, float(var), float(es))


def rolling_var(
    returns: pd.Series, model: str, window: int = 500, alpha: float = 0.99
) -> pd.Series:
    r = _clean(returns)

    vals: list[float] = []
    idx: list = []

    for i in range(window, len(r)):
        hist = r.iloc[i - window : i]

        if model == "historical":
            vals.append(historical_var_es(hist, alpha).var)
        elif model == "parametric":
            vals.append(parametric_var_es(hist, alpha).var)
        elif model == "ewma":
            vals.append(ewma_var_es(hist, alpha).var)
        else:
            raise ValueError(f"unknown model: {model}")

        idx.append(r.index[i])

    return pd.Series(vals, index=idx, name=f"VaR_{model}")

