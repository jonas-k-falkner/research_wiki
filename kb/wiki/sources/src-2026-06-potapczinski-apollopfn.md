---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-potapczinski-apollopfn
tags:
- timeseries-forecasting
- tsfm
- exogenous
- prior-fitted-networks
- zero-shot
zotero: potapczynskiTimeAwarePriorFitted2026
source_hash: 1a639cd03f66a7002be150749efb7ebe73111d4d5ca847497cfec3641180a32e
---

# ApolloPFN: Time-Aware Prior Fitted Networks for Zero-Shot Forecasting with Exogenous Variables

**Potapczynski et al. (Amazon + NYU, 2026)**

## Summary

ApolloPFN is a prior-data fitted network (PFN) that is both time-aware (unlike tabular PFNs like TabPFN-TS) and natively incorporates exogenous covariates (unlike most TSFMs). It addresses the failure modes of TabPFN-TS — lack of temporal ordering, weak trend extrapolation, no recency bias — through a novel synthetic data generation procedure (SRNGN graph algorithm with temporally-correlated root nodes) and time-aware architectural modifications (RoPE positional encodings, full attention across time steps).

## Covariate gap identification

"Most current time series foundation models (e.g., Chronos, Sundial, TimesFM, TimeMoE, TimeLLM, and LagLlama) ignore exogenous covariates and make forecasts solely from the numerical time series history." The paper explicitly lists these six models as not handling exogenous inputs.

## Architecture

- Based on TabPFN transformer with sample-feature separable attention (AttnFeat × AttnSamp).
- **Modifications for time series**: (1) Single Root Node Random Growing Network (SRNGN) for synthetic training data with temporal dependencies; (2) RoPE positional encodings for relative temporal ordering; (3) absolute positional encodings; (4) full attention (test points attend to each other, unlike i.i.d. TabPFN).
- Exogenous variables are natural features in the tabular framework — the model jointly attends over (y_t, x_t) tuples.
- Zero-shot inference: no fine-tuning needed; model generalizes to new datasets via in-context learning.

## Key results

- Achieves state-of-the-art on M5 (contains exogenous price/promotional covariates) and electricity price forecasting (EPF) benchmarks.
- On EPF (sCRPS): ApolloPFN (0x) matches or beats TabPFN-TS (0x) on most datasets; substantially better than Moirai-Large and Chronos-Large.
- On M5 (weekly, with promotions): ignoring price information causes ~catastrophic errors; ApolloPFN with exogenous covariates tracks price dynamics correctly.

## Claims

- **Chronos, Sundial, TimesFM, TimeMoE, TimeLLM, LagLlama all ignore exogenous covariates**, limiting their applicability to real-world forecasting where covariates drive spikes and discontinuities. [Evidence: Section 1]
- **TabPFN-TS fails as a time series FM** due to order-invariance, weak trend extrapolation, no recency bias, and poorly calibrated confidence intervals — all attributable to i.i.d. training assumption. [Evidence: Section 3, Figure 2]
- **Time-aware inductive biases (temporal root excitation + RoPE encodings) are necessary** for a PFN to achieve reliable zero-shot time series forecasting. [Evidence: Section 4, ablations Section 5.4]
- **ApolloPFN natively handles exogenous covariates in a zero-shot setting** without task-specific fine-tuning. [Evidence: Table 1, Section 5]

## Caveats

- Preprint (2026); full peer review pending.
- Performance comparison to ChronosX/UNICA is not head-to-head as these are fine-tuned approaches.
- Synthetic training data generation is complex; the SRNGN procedure may not cover all real-world covariate interaction patterns.
- Zero-shot capability means no cluster-specific adaptation — may underperform cluster-pretrained specialist models on seen-domain data.

## Applicability to P1

Adjacent. ApolloPFN demonstrates that zero-shot TSFM with native covariate handling is achievable, validating the covariate adapter design direction for P1. The M5 benchmark results are directly relevant to P1's retail demand use case. However, ApolloPFN's zero-shot approach differs from P1's cluster-pretrained approach; P1 should outperform zero-shot baselines on its trained clusters.

## Related

- [src-2026-06-arango-chronosx](src-2026-06-arango-chronosx.md) — ChronosX: adapter-based alternative
- [src-2026-06-han-unica](src-2026-06-han-unica.md) — UNICA: heterogeneous covariate adaptation
- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: supervised endo/exo split
