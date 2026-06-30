---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-arango-chronosx
tags:
- timeseries-forecasting
- tsfm
- exogenous
- adapter
zotero: arangoChronosXAdaptingPretrained2025
source_hash: cf934ba841056d2119d61ced731a0ac5966f584ec36146ce46d8ad9b97f69855
---

# ChronosX: Adapting Pretrained Time Series Models with Exogenous Variables

**Arango et al. (Amazon AWS, AISTATS 2025)**

## Summary

ChronosX is a modular adapter method to inject covariate information into the pretrained univariate Chronos model (and by extension TimesFM and MOMENT) without modifying the pretrained weights. Two lightweight FFN modules are attached: an Input Injection Block (IIB) for past covariates that updates token embeddings, and an Output Injection Block (OIB) for future covariates that adjusts output logits. Training only the adapter modules is fast even with a frozen pretrained backbone.

## Covariate gap identification

The paper explicitly states: "The majority of pretrained time series models do not support covariate data (Dooley et al., 2023; Goswami et al., 2024; Das et al., 2024; Ansari et al., 2024)." — Chronos, TimesFM, MOMENT, LagLlama are listed as not supporting covariates. Moirai is noted as the only exception (via "any-variate attention"), but even Moirai only handles homogeneous covariates.

## Architecture

- **IIB (past covariates)**: f_IIB(z_{t-1}, x_{t-1}) = h_emb(z_{t-1}) + FFN(ReLU(h_emb(z_{t-1})·W_emb ⊕ x_{t-1}·W_cov))
- **OIB (future covariates)**: adjusts output logits: f_OIB = h_out·W_out + FFN(ReLU(h_out·W_out ⊕ x_t·W_cov))
- Modular: can use IIB only (past covariates), OIB only (future known), or both.
- Extended to TimesFM and MOMENT via patched input variant.

## Key results

- ChronosX outperforms zero-shot Chronos by 22% in both WQL and MASE on 32 synthetic covariate datasets.
- ChronosX outperforms NHiTS, NBEATSx, TFT, DeepAR on complex synthetic datasets; NHiTS and NBEATSx competitive on simple ones.
- Demonstrated on 18 real-world datasets with covariates.
- Full fine-tuning (ChronosX-FF) generally improves over adapter-only, but adapter alone is significantly faster.

## Claims

- **Chronos, TimesFM, and MOMENT do not natively support exogenous covariates**; Moirai is the only TSFM with native covariate handling (but limited to homogeneous). [Evidence: Section 1-2, explicit citations]
- **Lightweight adapter modules (IIB + OIB) can effectively inject past and future covariate information into frozen pretrained TSFMs**, with 22% improvement over zero-shot Chronos. [Evidence: Figure 4, Section 6.1]
- The adapter approach allows much faster task-specific fine-tuning than full model retraining. [Evidence: Section 3 design rationale]

## Caveats

- Evaluated primarily on synthetic benchmarks designed by the paper's authors; real-world covariate datasets are limited.
- Adapter approach freezes the pretrained model: the backbone cannot adapt its temporal representations to covariate-rich domains.
- ChronosX is built on Chronos which is univariate — multivariate target settings require running it per-series.

## Applicability to P1

Adjacent. ChronosX demonstrates the feasibility of the adapter pattern for adding covariate support to frozen pretrained models, which is directly relevant to P1's architecture if Chronos or a similar TSFM is used as the backbone. However, P1 aims to pretrain cluster-specific models from scratch, so the adapter pattern is more relevant as an architectural template than a direct component.

## Related

- [src-2026-06-han-unica](src-2026-06-han-unica.md) — UNICA: broader adaptation framework including heterogeneous covariates
- [src-2026-06-potapczinski-apollopfn](src-2026-06-potapczinski-apollopfn.md) — ApolloPFN: zero-shot approach natively incorporating covariates
- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: supervised model with endo/exo split
