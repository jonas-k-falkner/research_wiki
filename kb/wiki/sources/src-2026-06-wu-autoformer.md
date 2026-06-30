---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-wu-autoformer
tags:
- timeseries-forecasting
- backbone
- transformer
- decomposition
zotero: wuAutoformerDecompositionTransformers2021
source_hash: 95fef4aaf57c1cf9d397adcb3051ab6c656cdd2d017aa1fb61a88b8f893b5415
---

# Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting

**Wu et al. (Tsinghua, NeurIPS 2021)**

## Summary

Autoformer replaces vanilla self-attention with an Auto-Correlation mechanism based on series periodicity, operating at sub-series level rather than point-wise. Also introduces progressive series decomposition (moving average) as an inner block rather than pre-processing. Achieves 38% relative improvement over prior methods on 6 long-term forecasting benchmarks.

## Key points

- **Auto-Correlation**: exploits periodicity to discover sub-series similarity; O(L log L) complexity; avoids point-wise permutation-invariance problem.
- **Progressive decomposition**: moving average inside each encoder/decoder layer, not just pre-processing.
- No exogenous covariate support.
- Later shown by Zeng et al. (DLinear) to be outperformed by a simple linear model.

## Claims

- **Progressive series decomposition as an inner block** enables Autoformer to extract trend and seasonal components throughout the forecasting process. [Evidence: Section 3.1]
- **Auto-Correlation (sub-series attention) outperforms point-wise self-attention** for long-term forecasting in both accuracy and efficiency. [Evidence: Section 3.2]

## Caveats / Applicability to P1

Background only. Autoformer was the SOTA Transformer baseline that DLinear subsequently outperformed. Provides context for the DLinear result and the broader evaluation of Transformer-based models. Not recommended as a P1 backbone given the evidence from DLinear.
