---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-zanotti-retraining-frequency
tags:
- timeseries-forecasting
- global-models
- retraining
zotero: zanottiRetrainingFrequencyGlobal2025
source_hash: 89c3e5ad92975d6301cb10ac39c7b832c657cb90da5d76afb85dd9e4c22eed3f
---

# Retraining Frequency of Global Models

**Zanotti et al. (2025)**

## Summary

Studies retraining frequency for global forecasting models on two real retail datasets: **M5** (30,490 Walmart SKU×Store daily series, 2011–2016, with prices/promotions/events) and **VN1** (15,053 weekly e-vendor SKUs, 2020–2024). Tests 10 global models: five ML (Linear Regression, Random Forest, XGBoost, LGBM, CatBoost) and five DL (MLP, RNN/LSTM, TCN, **N-BEATS**, **N-HiTS**).

Main finding: retraining frequency has little impact on accuracy — periodic retraining every 3–4 weeks matches continuous retraining on M5, and can even improve accuracy on VN1. ML models (especially LGBM) are marginally more cost-efficient at lower retraining frequencies.

## Key claims

- **N-BEATS and N-HiTS are the deep learning state-of-the-art models applied to M5 and VN1 real retail benchmarks in this 2025 study.** iTransformer, TimeMixer, and TimeKAN are not included — their SOTA claims come from academic LTSF benchmarks (ETT, Weather, Electricity), not real competition datasets. [Evidence: Section 3.2.2]
- **LGBM is among the top solutions across all major demand forecasting competitions** (M5, Favorita, Rossmann, VN1) with careful feature engineering (lags, rolling averages, calendar, promotions). [Evidence: Section 3.2.1]
- **Less frequent retraining does not degrade point forecast accuracy** of global models on real retail data; retraining every 3–4 weeks is optimal for M5. [Evidence: Figure 1, Figure 2 Friedman-Nemenyi test]
- Global DL models plateau at ~50% compute saving from reduced retraining (vs ~90% for ML models), due to DL training overhead that dominates even with rare updates. [Evidence: Figure 5]

## Applicability to P1

**Indirect relevance** (revised 2026-06-30 — P1 domain shifted to price/commodity forecasting). This study focuses on **retail demand forecasting** (M5, VN1), which is no longer P1's primary domain. Key takeaways that remain relevant:

- **N-BEATS and N-HiTS as DL SOTA on real retail benchmarks**: confirms these are the appropriate DL baselines for demand-type data; useful as methodological comparisons.
- **Retraining cadence finding**: global cluster-pretrained models do not need continuous retraining — weekly/monthly retraining sufficient. Directly applicable to P1's production deployment cadence regardless of domain.
- **LGBM competition dominance on demand data**: the competitive bar for demand forecasting is LGBM; for price/EPF forecasting the bar is different (GARCH/ARIMAX and ML baselines specific to price data).

For P1's price/EPF domain, NBEATSx and TimeXer (validated on EPF) are more directly relevant than this paper.

## Related

- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS architecture
- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS architecture
- [comparisons/tsf-backbone-comparison](../comparisons/tsf-backbone-comparison.md)
