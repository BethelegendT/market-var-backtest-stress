# Market VaR / ES — Backtesting + Stress Testing (Python)

A small, review-friendly market risk project: compute **VaR/ES** and demonstrate two core risk workflows:
- **Backtesting**: does VaR break as often as expected? (exceptions + **Kupiec** test)
- **Stress testing**: how much does tail risk expand under adverse shocks?

**One-page results:** [`docs/report.md`](docs/report.md)  
**Data:** this repo ships with a **synthetic** daily price series (`data/sample_prices.csv`) so it runs offline and is reproducible.

---

## What’s included
**Models (loss-based, positive numbers):**
- Historical simulation
- Parametric (Normal)
- EWMA conditional normal (RiskMetrics-style)

**Auto-generated outputs (in `docs/`):**
- [`report.md`](docs/report.md) — one-page summary (tables)
- `point_estimates.csv`
- `backtest_summary.csv`
- `stress_summary.csv`
- `loss_hist.png`
- `backtest_*.png` — exceptions are marked

---

## Quick start
```bash
pip install -r requirements.txt
python main.py
