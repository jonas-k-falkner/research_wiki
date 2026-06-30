---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-liang-itfkan
tags:
- timeseries-forecasting
- interpretability
- kan
- symbolic-ai
zotero: liangITFKANInterpretableTime2025
source_hash: 401774ad8a3edcd920795fe580d38177d18ec5606c99f9653f67d2476032ce29
---

# iTFKAN: Interpretable Time Series Forecasting with Kolmogorov-Arnold Network

**Liang et al. (2025)**

## Summary

iTFKAN is an interpretable forecasting model built on KAN (Kolmogorov-Arnold Network) with three components: (1) **Trend-Seasonal Decomposition** — split input into trend and seasonal; (2) **Prior-Guided TaylorKAN** — inject prior knowledge (polynomial for trend, Fourier series for seasonality) into KAN activation functions; (3) **Time-Frequency Synergy Learning** — process seasonal component from both time and frequency (FFT) perspectives using patch-based KAN. Claims both competitive forecast accuracy and interpretability via model symbolization.

Evaluated on **academic LTSF benchmarks only** (implied by related work comparisons to DLinear, TimeMixer, PatchTST).

## Architecture

- **TrendKAN**: polynomial-injected TaylorKAN; models monotonicity of trend via degree-p polynomial prior.
- **SeasonalKAN**: Fourier-series-injected KAN; models periodicity; top-K frequency components.
- **TFKAN (Time-Frequency)**: patch-based KAN applied separately in time domain and frequency domain (FFT); concatenated.
- **Interpretability**: KAN's learnable spline activations on edges can be inspected as symbolic formulas — what function each node computes is directly readable. Prior injection at the first layer guides structure toward interpretable forms.
- Output: linear projector over concatenated representations.

## Claims

- **iTFKAN achieves competitive forecasting accuracy** while providing high interpretability through model symbolization — forecasting performance is not sacrificed for interpretability. [Evidence: experimental results section]
- **Prior knowledge injection into KAN activation functions** (polynomial for trend, Fourier for seasonality) guides model structure learning and reduces overfitting to spurious patterns. [Evidence: Section 4.3, ablation]
- **Time-frequency synergy** (processing seasonal component from both domains) improves over single-domain processing — complementary perspectives. [Evidence: Section 4.4]
- **KAN's activation function symbolization** enables extraction of interpretable mathematical formulas from the learned model — qualitatively different from attention weight visualization. [Evidence: Section 3, KAN background]

## Caveats

- Academic LTSF benchmarks only — no EPF, commodity price, or M4/M5 evaluation.
- KAN-based models remain computationally heavier than DLinear/GLinear; TaylorKAN uses polynomial expansion to reduce vs spline-KAN, but still more complex.
- **AttGrad incompatibility risk**: P1's attribution method (weight × gradient) assumes smooth, differentiable activations. KAN's piecewise spline activations create complex gradient paths — the same concern as TimeKAN ([src-2026-06-huang-timekan](src-2026-06-huang-timekan.md)).
- Interpretability is of the *backbone temporal dynamics*, not of *covariate attribution* — iTFKAN does not have exogenous variable support.
- Prior injection requires domain knowledge about trend/seasonality structure; commodity prices may not conform to polynomial+Fourier priors (regime shifts, spikes).

## Applicability to P1

**Low — interesting for interpretability research context, not a primary backbone candidate.**

iTFKAN's interpretability via KAN symbolization is conceptually appealing for P1's attribution goal — but the attribution P1 needs is **covariate attribution** (which exogenous input drove the price move), not temporal pattern interpretation (what mathematical function describes the trend). These are different problems.

The backbone complexity concerns apply: KAN complicates AttGrad, and there is no exogenous variable support. Academic LTSF benchmarks only with no EPF or commodity price evaluation.

**Most useful for**: understanding the KAN interpretability design space; comparing against the case for AttGrad-over-MLP as a simpler, equally interpretable alternative.

## Related

- [src-2026-06-huang-timekan](src-2026-06-huang-timekan.md) — TimeKAN: different KAN-based TSF model; similar caveats
- [src-2026-06-rizvi-glinear](src-2026-06-rizvi-glinear.md) — GLinear: simpler linear model that also achieves competitive accuracy without KAN complexity
- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md) — P1 attribution design (AttGrad)
