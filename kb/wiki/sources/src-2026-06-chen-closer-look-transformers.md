---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-chen-closer-look-transformers
tags:
- timeseries-forecasting
- backbone
- transformer
- analysis
zotero: chenCloserLookTransformers
source_hash: a23145d5d1cef5d3c89f8b6d752d5f02e21dda06dff152096121e7134f7b5ad2
---

# A Closer Look at Transformers for Time Series Forecasting: Understanding Why They Work and Where They Struggle

**Chen et al. (Imperial College London, ICML 2025)**

## Summary

Analytical study explaining why simple Transformers (iTransformer, PatchTST) outperform complex ones on standard benchmarks. Key finding: intra-variate dependencies dominate performance on standard benchmarks because these datasets are largely self-dependent and stationary. Z-score normalization and skip connections are the actual drivers of success, not complex attention mechanisms.

## Key findings

1. **Point-wise Transformers are less effective** because point tokens cannot capture temporal intra-variate patterns through self-attention.
2. **Intra-variate vs. inter-variate**: inter-variate attention contributes minimally on standard benchmarks because variates are largely self-dependent. PatchTST (intra-variate only) and iTransformer (inter-variate only) perform similarly.
3. **Z-score normalization + skip connections are the critical architectural elements** driving success of simpler models. Without Z-norm, performance degrades on stationary datasets.
4. **Benchmark artifact**: standard benchmarks (ETT, Electricity, Weather) are stationary and self-dependent, biasing results toward models that don't need inter-variate information.
5. On non-standard (healthcare) data: inter-variate dependencies matter more — simpler models may underperform.

## Claims

- **Z-score normalization and skip connections — not complex attention mechanisms — explain the success of iTransformer and PatchTST** on standard benchmarks. [Evidence: Section 4, ablations]
- **Standard TSF benchmarks are self-dependent and stationary**, making them poor proxies for real-world settings with genuine inter-variate correlations. [Evidence: Section 5]
- **Intra-variate attention (patch-wise) is sufficient for standard benchmark performance**; inter-variate attention adds marginal benefit in self-dependent data. [Evidence: Mutual information experiments]

## Caveats / Applicability to P1

High and direct. This paper explains why DLinear wins on benchmarks (intra-variate self-dependence + stationary) and why those wins may not generalize to P1's retail demand data, which has genuine exogenous covariate drivers (promotions, prices). The findings suggest that P1 must go beyond standard benchmark evaluation and explicitly test on data with real exogenous effects to validate the backbone choice.
