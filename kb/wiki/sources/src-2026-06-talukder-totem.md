---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-talukder-totem
tags:
- ssl
- tokenizer
- vqvae
- cross-domain
- generalist
- time-series
zotero: talukderTOTEMTOkenizedTime2024
source_hash: 0ea0ac4aba897492b3911417502e14d995cdc190754ef8012633be20c36fe7ee
---

# TOTEM: TOkenized Time Series EMbeddings for General Time Series Analysis

**Talukder, Yue & Gkioxari (2024) — Caltech / ICML 2024**

## Summary

TOTEM uses a VQVAE (Vector Quantised Variational Autoencoder) to learn a discrete codebook representation of time series, enabling cross-domain generalist training. Unlike contrastive and MAE methods, TOTEM's pretext task is reconstruction (L_rec + commitment loss L_cmt). The tokenizer operates on univariate series (multivariate flattened per sensor), creating non-overlapping discrete tokens along the time dimension. Evaluated on 17 datasets across 3 tasks (imputation, anomaly detection, forecasting); achieves highest AvgWins in both specialist and generalist settings. Zero-shot testing on 5 unseen domains: TOTEM 80% AvgWins vs GPT2 20%.

## Key results

- Specialist imputation: TOTEM 52.1% AvgWins vs GPT2 35.4%
- Generalist in-domain imputation: TOTEM 58.3% vs GPT2 43.8%
- Zero-shot imputation: TOTEM 80.0% vs GPT2 20.0%
- Specialist anomaly detection: TOTEM 33.3% AvgWins (5-way tie second place)
- Forecasting: competitive with specialist baselines in in-domain testing
- No data engineering: operates directly on raw timesteps without auxiliary features or frequency transforms

## Architecture details

- VQVAE encoder E: strided 1D conv (cumulative stride F) maps univariate x ∈ ℝ^T → z ∈ ℝ^{T/F × D}
- Codebook C = {c_i}^K_i=1, K learned codewords of dimension D
- Quantizer: replaces z with ẑ by nearest-neighbour lookup in codebook
- Decoder D: strided transpose 1D conv (inverse of encoder) reconstructs x̂ from ẑ
- Objective: L = L_rec + α × L_cmt (reconstruction + commitment loss — no contrastive objective)
- Forecasting extension: frozen codebook → transformer encoder (attention over time tokens) → linear projection → prediction
- Sensor-agnostic: multivariate flattened to per-sensor univariate → enables generalist training across different sensor counts

## Claims

**Claim:** VQVAE-based tokenization enables zero-shot generalization across time series domains, with TOTEM achieving 80% AvgWins vs GPT2 20% on 5 unseen zero-shot imputation datasets.
**Evidence:** Talukder et al. 2024, Table 2B (zero-shot imputation). All 5 zero-shot datasets: TOTEM wins by large margin vs GPT2.
**Applicability:** Cross-domain pretraining scenarios where test domains differ from training. P2 may benefit from this for commodity series onboarding — a single pretrained tokenizer could serve multiple commodity types.
**Limitations:** Reconstruction pretext does not produce discriminative embeddings as well as contrastive methods for classification. Discrete codebook may lose fine-grained continuous structure important for forecasting. Sensor-agnostic treatment (per-sensor univariate) ignores cross-sensor dependencies.
**Contradictions:** TimeMAE produces stronger classification embeddings; TS2Vec produces stronger forecasting embeddings in direct comparisons. TOTEM's strength is generalist / zero-shot, not specialist peak performance.
**Decision impact:** TOTEM's VQVAE tokenizer is a candidate for P2's pretraining stage if cross-commodity generalization is a priority. The discrete codebook could serve as the common vocabulary for P1's multi-cluster routing. Not the right architecture for P2's directed objective (VQVAE is symmetric reconstruction), but the generalist cross-domain training strategy is valuable.
**Confidence:** high

## Applicability to P2

Medium. TOTEM's VQVAE tokenizer is not a directed/asymmetric method, but its cross-domain generalist pretraining is relevant to P2's onboarding requirement (new commodity series should embed quickly without per-series training). The discrete codebook representation could be used as the shared vocabulary before P2's asymmetric fine-tuning head.

## Related

- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — timestep-level SSL alternative
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — MAE-based encoder alternative
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
