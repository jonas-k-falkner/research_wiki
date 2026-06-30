---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-huang-timekan
tags:
- timeseries-forecasting
- backbone
- kan
- frequency-decomposition
zotero: huangTimeKANKANbasedFrequency2025
source_hash: 6e313d463f481cc0aa0141a9fcc3a196f3b6a21ea42fecb7197d095e0e34f550
---

# TimeKAN: KAN-based Frequency Decomposition Learning Architecture for Long-term Time Series Forecasting

**Huang et al. (2025)**

## Summary

TimeKAN replaces MLP blocks with Kolmogorov-Arnold Networks (KAN) inside a Decomposition-Learning-Mixing (DLM) architecture. Cascaded Frequency Decomposition (CFD) progressively removes high-frequency components; Multi-order KAN Representation Learning (M-KAN) models each frequency band with KANs of increasing polynomial order; Frequency Mixing recombines the bands.

## Key result

SOTA on most long-term forecasting benchmarks (ETT, Weather, Traffic, Solar, Exchange-Rate, ILI). Outperforms TimeMixer on all reported datasets. iTransformer achieves best result on Electricity (high-dimensional, strong inter-variate signal); TimeKAN is second.

Explicitly: **"DLinear already shows a significant gap when compared to state-of-the-art methods."** [Table 6, efficiency comparison section]

## Architecture

- Progressive high-frequency removal via moving average (like DLinear's decomposition, but iterative).
- CFD → M-KAN blocks (polynomial KANs, order 1 at coarsest to order 5 at finest frequency band).
- Depthwise convolution for efficiency; parameter count is 2–20× smaller than PatchTST/TimeMixer for comparable or better accuracy.
- Channel-independent (no inter-variate modeling by default).

## Efficiency vs accuracy

On Weather dataset: TimeKAN uses 20.05% of TimeMixer's parameters and 36.14% of its MACs while achieving lower MSE. On Electricity: iTransformer is best (high-variate dataset benefits from channel-wise attention); TimeKAN is competitive.

## Claims

- **KAN with multi-order polynomial basis outperforms MLP in frequency-band representation** when orders are matched to frequency band complexity. [Evidence: Table 3 ablation]
- **DLinear is no longer competitive with 2024–2025 SOTA on standard benchmarks**; the gap is described as "significant." [Evidence: Table 6, Section IV-B]
- **iTransformer's channel-wise attention is specifically advantageous on high-dimensional datasets** (Electricity); on lower-dimensional or aperiodic datasets, TimeKAN or TimeMixer are superior.

## Caveats / Applicability to P1

Medium. TimeKAN is the 2025 SOTA for compact long-term forecasting. For P1's cluster-pretrained backbone:
- Relevant as the upper-bound benchmark to compare against.
- Channel-independent design matches P1's cluster-level training (each cluster is treated independently).
- No exogenous covariate support — same limitation as DLinear and N-BEATS.
- Depthwise-conv + KAN may complicate AttGrad covariate attribution relative to linear/MLP architectures.

## Related

- [src-2026-06-zeng-dlinear](src-2026-06-zeng-dlinear.md) — DLinear: simpler but outperformed by TimeKAN
- [src-2026-06-wang-timemixer](src-2026-06-wang-timemixer.md) — TimeMixer++: strong multi-task competitor
- [comparisons/tsf-backbone-comparison](../comparisons/tsf-backbone-comparison.md)
