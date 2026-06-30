---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-wang-timemixer
tags:
- timeseries-forecasting
- backbone
- mlp-mixer
- multi-scale
zotero: wangTimeMixerGeneralTime2024
source_hash: 6cc61e02bc357a1cff160d783156c0f5dcfce761ce08b4d39b0ce87621d9da41
---

# TimeMixer++: A General Time Series Pattern Machine for Universal Predictive Analysis

**Wang et al. (2024)**

## Summary

TimeMixer++ is a general-purpose time series pattern machine (TSPM) that processes multi-scale time series through multi-resolution time imaging (MRTI), time image decomposition (TID), multi-scale mixing (MCM), and multi-resolution mixing (MRM). By representing time series at multiple scales and in both time and frequency domains, it achieves state-of-the-art across 8 time series tasks (forecasting, classification, anomaly detection, imputation).

## Architecture

- **Multi-scale input**: progressive downsampling (stride-2 convolution) to produce M scales x_0, ..., x_M.
- **Channel mixing at coarsest scale**: variate-wise self-attention at coarsest scale x_M for cross-variable interaction.
- **MixerBlock**: (1) MRTI converts each scale to 2D time image; (2) TID applies dual-axis attention (temporal + frequency) to disentangle seasonal and trend; (3) MCM hierarchically aggregates patterns across scales; (4) MRM adaptively integrates across frequency resolutions.
- **Output**: multiple scale-specific prediction heads, ensembled.

## Key results

- Achieves SOTA across 8 time series analysis tasks; outperforms both general-purpose and task-specific models.
- No exogenous variable support in the base configuration.

## Claims

- **Multi-scale, multi-resolution processing via MixerBlocks outperforms single-scale approaches** across diverse time series tasks. [Evidence: Figure 1, benchmarks]
- **Disentangling seasonal and trend in frequency/time image space** is more flexible than applying fixed moving-average decomposition. [Evidence: Section 3.1]

## Caveats / Applicability to P1

Medium. TimeMixer++ represents a stronger multi-task backbone option, but adds complexity over DLinear/N-HiTS without clear exogenous covariate support. Useful as a backbone candidate if P1 needs to support classification/anomaly detection tasks beyond forecasting.
