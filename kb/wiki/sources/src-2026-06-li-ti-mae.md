---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-li-ti-mae
tags:
- ssl
- masked-autoencoder
- time-series-representation
- self-supervised
- forecasting
zotero: liTiMAESelfSupervisedMasked2023
source_hash: dc10e30498ab560ef25f6773148067dd935f4cbdc68d262cef760b702fa8bf64
---

# Ti-MAE: Self-Supervised Masked Time Series Autoencoders

**Li et al. (2023) — ICLR 2023 Workshop (Self-Supervised Learning for Time Series)**

## Summary

Ti-MAE adapts the MAE paradigm (He et al. 2022) to time series. Random masking at 75% is applied to time steps; a standard Transformer encoder encodes only visible (unmasked) patches; a lightweight decoder reconstructs the masked values. Key finding: 75% masking is optimal for TS (much higher than NLP's 15% or images' 50–75%), because TS exhibit strong temporal autocorrelation making easy reconstruction uninformative at low masking rates. Ti-MAE alleviates distribution shift between TS patches by treating each masked position independently during reconstruction.

## Key results

- Outperforms TS-TCC, TS2Vec, and SimMTM on long-term forecasting benchmarks (ETT, Weather, Exchange-Rate, ILI)
- Best masking ratio: 75% random (point-level masking over raw time steps)
- Pretraining on target domain, then fine-tuning forecasting head
- Classification results are competitive but Ti-MAE's primary strength is forecasting (unlike TS-TCC/TS2Vec which target classification)

## Architecture details

- Input: raw time series, tokenized into patches (patch size tuned per dataset)
- Masking: random 75% of patches dropped; only visible patches fed to encoder
- Encoder: standard Transformer (shared with MAE-style)
- Decoder: lightweight Transformer operating over encoder output + masked position tokens
- Loss: MSE reconstruction over masked positions only
- **Symmetric**: encoder produces a global representation; no directed/asymmetric objective

## Claims

**Claim:** Masked autoencoder pretraining with 75% masking ratio on time series produces representations that outperform contrastive learning methods on long-term forecasting, because higher masking forces the encoder to learn global temporal context rather than local autocorrelation.
**Evidence:** Ablation in Ti-MAE paper: forecasting MSE decreases monotonically as masking ratio increases from 15% to 75%, peaks at 75%, then degrades at 90%+. Outperforms TS2Vec and TS-TCC on ETT{h1,h2,m1,m2}, Weather, and ILI benchmarks.
**Applicability:** Long-term forecasting tasks with sufficient pretraining data on the target domain.
**Limitations:** Evaluated at ICLR workshop level — not peer-reviewed main track. Point-level masking (not sub-series patches) means less semantic density per masked unit than TimeMAE; worse on classification benchmarks.
**Contradictions:** TimeMAE uses 60% masking ratio with sub-series patches and outperforms on classification; Ti-MAE claims 75% optimal for point-level masking — different granularity makes direct comparison invalid.
**Decision impact:** MAE-style pretraining is preferable over contrastive learning for forecasting applications, which is P1's primary task. However, Ti-MAE's symmetric design means it cannot directly serve P2's asymmetric retrieval objective.
**Confidence:** high

**Claim:** Ti-MAE alleviates TS distribution shift (train-test covariate shift common in financial/commodity TS) as a byproduct of masked reconstruction pretraining on the target distribution.
**Evidence:** Ti-MAE paper, motivation section and ablation on distribution shift datasets.
**Applicability:** Domains with non-stationary dynamics (energy prices, commodity prices) where distribution shift between pretraining and test periods is common.
**Limitations:** The claim is made in the workshop paper; not independently replicated.
**Contradictions:** None.
**Decision impact:** Relevant for P1 price/commodity forecasting, where distribution shift is a known failure mode.
**Confidence:** medium

## Applicability to P2

Low. Ti-MAE is **symmetric** — standard encoder-decoder with no directional objective. Its masked reconstruction pretraining is relevant as an SSL paradigm study for the broader P2 design space, and its distribution-shift mitigation property is relevant for P1. Not applicable as a P2 encoder directly.

## Related

- [src-2026-06-eldele-ts-tcc](src-2026-06-eldele-ts-tcc.md) — TS-TCC: contrastive, symmetric
- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — TS2Vec: contrastive, symmetric
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — TimeMAE: decoupled MAE, better design for classification
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
