from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

from src.config import RunConfig
from src.data import load_prices, returns_from_close
from src.var_models import historical_var_es, parametric_var_es, ewma_var_es, rolling_var
from src.backtest import backtest_var
from src.stress import Scenario, apply_scenario, worst_window_sum
from src.plotting import loss_hist, loss_vs_var

def _pct(x: float) -> str:
    return f"{100.0*x:.2f}%"

def _write_report(
    out_dir: Path,
    alpha: float,
    point_df: pd.DataFrame,
    backtest_df: pd.DataFrame,
    stress_df: pd.DataFrame,
    worst_window_line: str,
) -> None:
    lines: list[str] = []
    lines.append("# Market VaR/ES — Backtest + Stress (Report)")
    lines.append("")
    lines.append(f"- VaR/ES confidence level: **alpha = {alpha:.2f}**")
    lines.append("")
    lines.append("## Point estimates (full sample)")
    lines.append(point_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Backtest summary (rolling 1-day VaR forecasts)")
    lines.append(backtest_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Stress summary (simple, explainable shocks)")
    lines.append(stress_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Worst historical window (20 trading days)")
    lines.append(worst_window_line.strip())
    lines.append("")
    lines.append("## Plots")
    lines.append("- Loss histogram: `loss_hist.png`")
    lines.append("- Backtest plots: `backtest_*.png` (exceptions are marked)")
    lines.append("")
    (out_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def run(data_path: Path, out_dir: Path, cfg: RunConfig) -> None:
    cfg.validate()
    out_dir.mkdir(parents=True, exist_ok=True)

    df = load_prices(data_path)
    r = returns_from_close(df["close"])
    r.index = df["date"]
    r = r.dropna()

    # Point estimates (full sample)
    hv = historical_var_es(r, cfg.alpha)
    pv = parametric_var_es(r, cfg.alpha)
    ev = ewma_var_es(r, cfg.alpha)

    point_df = pd.DataFrame([
        {"model": "historical", "VaR": _pct(hv.var), "ES": _pct(hv.es)},
        {"model": "parametric_normal", "VaR": _pct(pv.var), "ES": _pct(pv.es)},
        {"model": "ewma_conditional_normal", "VaR": _pct(ev.var), "ES": _pct(ev.es)},
    ])
    point_df.to_csv(out_dir / "point_estimates.csv", index=False)

    # Rolling backtests
    bt_rows = []
    for m in ["historical", "parametric", "ewma"]:
        var_fc = rolling_var(r, model=m, window=cfg.window, alpha=cfg.alpha)
        bt = backtest_var(r, var_fc, cfg.alpha)
        bt_rows.append({
            "model": m,
            "n": bt.n,
            "exceptions": bt.exceptions,
            "exception_rate": f"{100.0*bt.exception_rate:.2f}%",
            "kupiec_LR": round(bt.kupiec_LR, 3),
            "kupiec_p_value": round(bt.kupiec_p_value, 3),
        })
        loss_vs_var(r, var_fc, str(out_dir / f"backtest_{m}.png"), alpha=cfg.alpha)

    backtest_df = pd.DataFrame(bt_rows).sort_values("model")
    backtest_df.to_csv(out_dir / "backtest_summary.csv", index=False)

    # Stress tests (simple, explainable)
    scenarios = [
        Scenario("Base", 0.0, 1.0),
        Scenario("Mild", -0.01, 1.3),
        Scenario("Severe", -0.03, 2.0),
    ]
    st_rows = []
    for sc in scenarios:
        rs = apply_scenario(r, sc)
        st_rows.append({
            "scenario": sc.name,
            "hist_VaR": _pct(historical_var_es(rs, cfg.alpha).var),
            "hist_ES": _pct(historical_var_es(rs, cfg.alpha).es),
            "param_VaR": _pct(parametric_var_es(rs, cfg.alpha).var),
            "param_ES": _pct(parametric_var_es(rs, cfg.alpha).es),
            "ewma_VaR": _pct(ewma_var_es(rs, cfg.alpha).var),
            "ewma_ES": _pct(ewma_var_es(rs, cfg.alpha).es),
        })
    stress_df = pd.DataFrame(st_rows)
    stress_df.to_csv(out_dir / "stress_summary.csv", index=False)

    t, w = worst_window_sum(r, window=20)
    worst_line = f"Ends at **{t.date()}**, cumulative return (simple sum) ≈ **{w:.4f}**"
    (out_dir / "worst_window.txt").write_text(worst_line + "\n", encoding="utf-8")

    # plots
    loss_hist(r, str(out_dir / "loss_hist.png"))

    # human-readable summary
    (out_dir / "run_summary.txt").write_text(
        "\n".join([
            "Point estimates (full sample)",
            f"alpha={cfg.alpha}",
            f"historical: VaR={_pct(hv.var)}, ES={_pct(hv.es)}",
            f"parametric: VaR={_pct(pv.var)}, ES={_pct(pv.es)}",
            f"ewma: VaR={_pct(ev.var)}, ES={_pct(ev.es)}",
            "",
            "Tables:",
            "- point_estimates.csv",
            "- backtest_summary.csv",
            "- stress_summary.csv",
            "",
            "See report.md for a single-page GitHub-friendly summary.",
        ]) + "\n",
        encoding="utf-8"
    )

    _write_report(out_dir, cfg.alpha, point_df, backtest_df, stress_df, worst_line)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, default="data/sample_prices.csv")
    ap.add_argument("--out", type=str, default="docs")
    ap.add_argument("--alpha", type=float, default=0.99)
    ap.add_argument("--window", type=int, default=500)
    args = ap.parse_args()

    cfg = RunConfig(alpha=args.alpha, window=args.window)
    run(Path(args.data), Path(args.out), cfg)

if __name__ == "__main__":
    main()
