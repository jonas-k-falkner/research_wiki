---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-zeng-dlinear
tags:
- timeseries-forecasting
- backbone
- linear-models
zotero: zengAreTransformersEffective2022
source_hash: 796f69fd9be69b38e68be57eedce5cd94ceaacd4f188ca1ee155e830eedf8fa8
---

# Are Transformers Effective for Time Series Forecasting? (DLinear)

**Zeng et al. (AAAI 2023)**

## Summary

Challenges the dominant position of Transformer-based models for long-term time series forecasting (LTSF). Introduces LTSF-Linear, a set of one-layer linear models (Vanilla Linear, DLinear, NLinear) as baselines, and shows they outperform all tested Transformer-based LTSF models on nine standard benchmarks.

The core argument: self-attention is permutation-invariant, which causes temporal information loss when applied to ordered continuous time series data. Linear models avoid this problem entirely.

## Architecture

- **DLinear**: decomposition (moving average) into trend + remainder, then two independent linear layers summed for the final forecast.
- **NLinear**: subtracts last value before a linear layer, adds it back — simple normalization for distribution shift.
- Both share weights across variates (no inter-variate modeling).

## Key results

- DLinear outperforms FEDformer (then-SOTA Transformer) on 9 benchmarks by **20–50% in MSE** for multivariate long-term forecasting (horizons 96–720).
- Transformers fail to exploit longer look-back windows; their accuracy is flat or degrades as look-back increases beyond 96. LTSF-Linear accuracy improves monotonically with longer look-back.
- Ablation: gradually simplifying Informer toward a linear layer consistently improves performance, confirming the self-attention scheme is not necessary for LTSF.
- Exchange-Rate: even a naive repeat baseline outperforms Transformers (~45%), suggesting Transformers overfit to trend noise.

## Claims

- **Simple one-layer linear models outperform all tested Transformer-based LTSF models** on nine public benchmarks, by 20–50% MSE in multivariate settings. [Evidence: Table 2, AAAI 2023]
- **Transformer self-attention is permutation-invariant and loses temporal ordering information**, a fundamental mismatch with the ordered nature of time series. [Evidence: Section 3 argument + ablation]
- **Transformers fail to scale with longer look-back windows**, plateauing or degrading beyond 96 steps, while LTSF-Linear improves monotonically. [Evidence: Figure 4]
- LTSF-Linear results do not model inter-variate correlations; this is a deliberate simplification that still wins, implying standard benchmark datasets have weak inter-variate signal.

## Caveats

- Scope limited to LTSF benchmarks with strong trend and/or periodicity (ETT, Electricity, Traffic, Weather, ILI, Exchange-Rate). Not a claim about all time series scenarios.
- Does not address short-term forecasting, probabilistic forecasting, or settings with strong exogenous covariates.
- Later work (e.g., iTransformer, PatchTST) partially addresses the permutation-invariance critique by using patch-level or variate-level tokenization.
- The "no inter-variate modeling" assumption may not hold for demand data with strong cross-SKU effects.

## Applicability to P1

Very high. DLinear is the compact backbone baseline for P1. The result confirms that a simple linear backbone — potentially enhanced with covariate injection — can be a strong and computationally cheap starting point before considering heavier architectures. The scalability with look-back window size is directly useful for cluster-pretrained models that benefit from longer context.

## Related

- [src-2026-06-oreshkin-nbeats](src-2026-06-oreshkin-nbeats.md) — N-BEATS: another strong non-Transformer backbone
- [src-2026-06-challu-nhits](src-2026-06-challu-nhits.md) — N-HiTS: MLP + hierarchical interpolation alternative
- [src-2026-06-chen-closer-look-transformers](src-2026-06-chen-closer-look-transformers.md) — follow-up analysis explaining why simple Transformers win
