---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-han-unica
tags:
- timeseries-forecasting
- tsfm
- exogenous
- adapter
- multimodal
zotero: hanUNICAUNIFIEDCOVARIATE2026
source_hash: 2aed00685519d7104a29341938dbbef880aac925aa4bb65c8a4b7365e264ff7e
---

# UNICA: Unified Covariate Adaptation for Time Series Foundation Models

**Han et al. (Nanjing University + Ant Group, 2026)**

## Summary

UNICA is a plug-in adaptation framework that enables TSFMs (Chronos, Moirai, TimesFM, Time-MoE) to handle both homogeneous (real-valued) and heterogeneous (categorical, image, text) covariates without changing the pretrained model's parameters. The framework has two components: (1) covariate homogenization that converts all covariates to dense temporal representations, and (2) a dual attention-based fusion mechanism with pre-fusion (past covariates before the TSFM encoder) and post-fusion (future covariates after the encoder).

## Covariate gap identification

"Most state-of-the-art TSFMs (Ansari et al., 2024; Das et al., 2024; Goswami et al., 2024) are fundamentally designed for univariate forecasting, processing each time series in isolation... None of the existing methods can handle both homogeneous and heterogeneous, especially multi-modal covariates."

Explicitly lists Chronos, TimesFM, MOMENT as ignoring covariates; Moirai as partially supporting homogeneous covariates only.

## Architecture

**Covariate Homogenization**: categorical covariates → embedding layer; multimodal (images/text) → domain encoder (CNN/pretrained transformer) → linear projector → temporal representation C_(het). All covariates concatenated into unified C_{1:T+H}.

**TSFM decomposition**: Tokenizer T → Temporal Encoder E → Predictor P.

**Pre-Fusion (past covariates)**: Conditional Attention Pooling (CAP) on past covariates + static features → gated fusion with tokenized target representations → fed to TSFM encoder.

**Post-Fusion (future covariates)**: CAP on future covariates → self-attention combining past-encoded representations with future covariate tokens → predictor.

Pre-trained TSFM weights are frozen; only adaptation modules are trained.

## Key results

- Outperforms ChronosX and task-specific baselines on 12 unimodal and 2 multimodal (MMSP satellite imagery, Time-MMD) covariate datasets.
- Works across all major TSFM families (token-based Chronos, patch-based TimesFM/Moirai, MLP-based TTM, MoE Time-MoE).

## Claims

- **TSFMs cannot handle heterogeneous covariates (categorical, image, text) natively**; UNICA is the first framework to unify heterogeneous covariate adaptation across TSFM families. [Evidence: Section 1, Table 1]
- **Covariate homogenization — converting all covariate types to dense temporal series representations — enables a single unified attention-based fusion mechanism** to work across modalities. [Evidence: Section 4.1]
- **Pre-fusion (past) + post-fusion (future) decomposition preserves TSFM generalization ability** while effectively injecting covariate information. [Evidence: Section 4.2, experiments]
- UNICA outperforms ChronosX (which is limited to point-wise TSFMs) on all benchmark types. [Evidence: Figure 3]

## Caveats

- The homogenization step introduces domain-specific encoders for image/text; these add complexity and require domain-specific pre-training.
- Pre-fusion uses CAP inspired by TFT's variable selection — interpretability of which covariates matter is partial but present.
- 2026 preprint; not yet peer-reviewed at time of ingest.

## Applicability to P1

Adjacent. UNICA's modular fusion design is instructive for P1's covariate architecture, particularly: (1) the homogenization step that makes heterogeneous covariates tractable, (2) the pre/post fusion decomposition separating past and future covariates, (3) the compatibility across TSFM families. For P1 specifically, the homogenization concept could handle categorical SKU attributes and promotional flags alongside continuous price/quantity covariates.

## Related

- [src-2026-06-arango-chronosx](src-2026-06-arango-chronosx.md) — ChronosX: simpler adapter, comparable goal
- [src-2026-06-potapczinski-apollopfn](src-2026-06-potapczinski-apollopfn.md) — ApolloPFN: zero-shot native covariate handling
- [src-2026-06-wang-timexer](src-2026-06-wang-timexer.md) — TimeXer: supervised endo/exo split model
