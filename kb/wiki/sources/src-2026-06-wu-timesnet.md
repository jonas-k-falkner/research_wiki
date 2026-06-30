---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-wu-timesnet
tags:
- timeseries-forecasting
- backbone
zotero: wuTimesNetTemporal2DVariation2023
source_hash: a45cb3d35c7b4db7091439ee714fd43dd6cd9e8f2fb1867f5463ae0433aebbd1
---

# TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis

**Wu et al. (Tsinghua, ICLR 2023)**

## Summary (3 bullets)

- TimesNet transforms 1D time series into 2D tensors based on discovered periods, enabling 2D convolution (Inception blocks) to capture both intraperiod and interperiod variations simultaneously.
- Achieves SOTA across 5 tasks (short/long-term forecasting, imputation, classification, anomaly detection) as a general backbone.
- No exogenous covariate support; later outperformed on pure forecasting tasks by DLinear and iTransformer/PatchTST. **Applicability to P1**: background only.
