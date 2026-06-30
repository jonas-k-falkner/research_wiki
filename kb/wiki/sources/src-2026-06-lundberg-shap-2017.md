---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-lundberg-shap-2017
tags:
- source
- shap
- attribution
- interpretability
citekey: lundbergUnifiedApproachInterpreting2017
source_hash: ee58029f0ffac4ef8f962e7ce75cbf025de41ecab4de0207b192242441b3edae
author: Lundberg, Scott M.; Lee, Su-In
year: 2017
title: A Unified Approach to Interpreting Model Predictions
venue: NeurIPS 2017
zotero: lundbergUnifiedApproachInterpreting2017
---

# Lundberg & Lee (2017) — SHAP

## Summary

Introduces SHAP (SHapley Additive exPlanations), a unified framework for model attribution based on cooperative game theory Shapley values. Shapley values uniquely satisfy local accuracy, missingness, and consistency axioms. Kernel SHAP provides a model-agnostic approximation using weighted linear regression without requiring gradient access. Deep SHAP uses backpropagation for neural networks. Exact computation is exponential O(2^M) in number of features; Kernel SHAP approximates via sampling.

## Key claims

1. Kernel SHAP is model-agnostic and does not require gradient access — it approximates Shapley values via weighted linear regression, making it applicable to any black-box model including attention-based forecasters.
2. Shapley values satisfy local accuracy (attributions sum to the prediction difference from a baseline), missingness (absent features get zero attribution), and consistency (higher-contribution features always receive equal or higher attribution) — uniquely among additive feature attribution methods.
3. SHAP does not model temporal ordering of features: it treats each feature independently, making it less suited to time-series covariate selection where temporal structure and lagged dependencies are essential.

## Relevance to P1

SHAP provides the post-hoc attribution alternative to attention-based explanation. Kernel SHAP's gradient-free property is attractive for inference-time explanation but the independence assumption and lack of temporal structure modeling are limitations for macro-covariate time series. Can serve as an external validation baseline for entmax selection — if SHAP and entmax weights agree, the entmax explanation gains credibility.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
