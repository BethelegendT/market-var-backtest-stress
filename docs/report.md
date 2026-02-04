# Market VaR/ES — Backtest + Stress (Report)

- VaR/ES confidence level: **alpha = 0.99**

## Point estimates (full sample)
| model                   | VaR   | ES    |
|:------------------------|:------|:------|
| historical              | 1.77% | 3.18% |
| parametric_normal       | 1.74% | 1.99% |
| ewma_conditional_normal | 1.39% | 1.59% |

## Backtest summary (rolling 1-day VaR forecasts)
| model      |    n |   exceptions | exception_rate   |   kupiec_LR |   kupiec_p_value |
|:-----------|-----:|-------------:|:-----------------|------------:|-----------------:|
| ewma       | 2108 |           23 | 1.09%            |       0.172 |            0.679 |
| historical | 2108 |           21 | 1.00%            |       0     |            0.986 |
| parametric | 2108 |           26 | 1.23%            |       1.08  |            0.299 |

## Stress summary (simple, explainable shocks)
| scenario   | hist_VaR   | hist_ES   | param_VaR   | param_ES   | ewma_VaR   | ewma_ES   |
|:-----------|:-----------|:----------|:------------|:-----------|:-----------|:----------|
| Base       | 1.77%      | 3.18%     | 1.74%       | 1.99%      | 1.39%      | 1.59%     |
| Mild       | 3.30%      | 5.13%     | 3.26%       | 3.59%      | 2.71%      | 3.11%     |
| Severe     | 6.54%      | 9.36%     | 6.47%       | 6.98%      | 7.10%      | 8.13%     |

## Worst historical window (20 trading days)
Ends at **2020-03-04**, cumulative return (simple sum) ≈ **-0.5131**

## Plots
- Loss histogram: `loss_hist.png`
- Backtest plots: `backtest_*.png` (exceptions are marked)

