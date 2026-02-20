from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def loss_hist(returns: pd.Series, out_path: str) -> None:
    losses = (-returns.dropna()).values
    plt.figure(figsize=(6, 4))
    plt.hist(losses, bins=60)
    plt.title("Loss distribution (daily, -return)")
    plt.xlabel("loss")
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def loss_vs_var(returns: pd.Series, var_fc: pd.Series, out_path: str, alpha: float) -> None:
    r = returns.loc[var_fc.index]
    losses = -r
    exc = losses.values > var_fc.values

    plt.figure(figsize=(10, 4))
    plt.plot(losses.index, losses.values, label="Realized loss (-return)")
    plt.plot(var_fc.index, var_fc.values, label=f"Forecast VaR (alpha={alpha:.2f})")

    if exc.any():
        plt.scatter(losses.index[exc], losses.values[exc], s=10, label="Exceptions", zorder=3)

    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
