# Market VaR / ES — Backtesting + Stress Testing (Python)

一个**小而完整**的量化风险项目：算 VaR/ES，然后用**回测**和**压力测试**回答两个现实问题：
- VaR 预测有没有“经常被打穿”？（exceptions + Kupiec test）
- 在不利情景下尾部风险会变多大？（shock + vol multiplier）

> 结果总览请直接看：**`docs/report.md`**

## Quick start
```bash
pip install -r requirements.txt
python main.py
```

输出在 `docs/`：
- `report.md`（一页总结：point estimates / backtest / stress）
- `point_estimates.csv`
- `backtest_summary.csv`
- `stress_summary.csv`
- `loss_hist.png`
- `backtest_*.png`（图里会标出 exceptions）

## 换成你的真实数据
准备一个 CSV（两列即可）：
- `date`（YYYY-MM-DD）
- `close`（价格）

然后：
```bash
python main.py --data data/your_prices.csv
```

## 口径说明（够用且易解释）
- VaR/ES 输出为**正数**，代表损失阈值（loss = -return）
- 模型（都很常见、易解释）：
  - historical simulation
  - normal parametric
  - EWMA conditional normal（RiskMetrics 风格）

## 局限（建议你在 SOP 里也这么写）
- 正态模型对厚尾市场会低估尾部；
- EWMA 很实用但对结构性断点不敏感；
- 这里是单资产 demo；组合扩展没有写入，为了保持干净可审阅。

## 简历一句话（可直接用）
**Market Risk VaR/ES (Python)** — Implemented historical/parametric/EWMA VaR-ES, ran rolling backtests (exceptions + Kupiec test), and stress-tested tail losses under simple shock scenarios. (Link)
