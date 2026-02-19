# Market VaR / ES — Backtesting + Stress Testing (Python)

A compact, review-friendly **market risk** project that computes **VaR/ES** and demonstrates two core risk workflows:

1) **Backtesting** — do VaR exceptions occur as often as expected? (exceptions + **Kupiec** unconditional coverage test)  
2) **Stress testing** — how does tail risk expand under adverse, explainable shocks?

**One-page output:** `reports/example_run/report.md`  
**Runs offline:** ships with a small synthetic daily price series (`data/sample_prices.csv`).

---

## What’s inside

### Risk models (loss-based, positive numbers)
- **Historical simulation**
- **Parametric (Normal)**
- **EWMA conditional normal** (RiskMetrics-style volatility)

### Validation & reporting
- Rolling 1-day VaR forecasts
- Exceptions + exception rate
- **Kupiec LR test + p-value** (unconditional coverage)
- Stress scenarios (return shock + volatility multiplier)
- Plots: loss histogram & backtest charts with exceptions marked

---

## Quick start (reproducible)

```bash
pip install -r requirements.txt
python -m src.market_risk.cli --data data/sample_prices.csv --out reports/example_run --alpha 0.99 --window 500
