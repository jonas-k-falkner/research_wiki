---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-eldele-ts-tcc
tags:
- ssl
- contrastive-learning
- time-series-representation
- self-supervised
zotero: eldeleTimeSeriesRepresentationLearning2021
source_hash: 13a4a7c988c986b4b6c002489145a5124cc75c08f25cdfc5090437500210cebd
---

# TS-TCC: Time-Series Representation Learning via Temporal and Contextual Contrasting

**Eldele et al. (2021) — IJCAI 2021**

## Summary

TS-TCC is a two-module contrastive framework for unsupervised TS representation learning. It generates two views with weak (jitter+scale) and strong (permutation+jitter) augmentations, then applies (1) Temporal Contrasting: a cross-view autoregressive prediction task where the strong-augmentation context predicts future timesteps of the weak view and vice versa, and (2) Contextual Contrasting: SimCLR-style instance-level similarity maximization over the resulting context vectors. Encoder is a 3-block CNN; autoregressive model is a Transformer.

## Key results

- Linear evaluation matches supervised accuracy: HAR 90.37% vs supervised 90.14%; Epilepsy 97.23% vs 96.66%
- Semi-supervised: TS-TCC fine-tuned with 10% labeled data achieves comparable performance to 100%-supervised baseline across all 3 datasets
- Transfer learning: +4% average accuracy over supervised pretraining on cross-domain Fault Diagnosis (12 conditions)
- Beats SimCLR, CPC, and SSL-ECG across HAR, Sleep-EDF, Epilepsy benchmarks

## Architecture details

- Weak aug: jitter (random noise) + scale (magnitude scaling)
- Strong aug: permutation (shuffle random segments up to M) + jitter
- Temporal Contrasting: cross-view prediction — $c_t^s$ predicts $z_{t+k}^w$ and $c_t^w$ predicts $z_{t+k}^s$; K=40% of feature length is optimal
- Contextual Contrasting: standard SimCLR NT-Xent loss with temperature τ=0.2 over transformer context token
- Combined loss: $\mathcal{L} = \lambda_1(\mathcal{L}_{TC}^s + \mathcal{L}_{TC}^w) + \lambda_2 \mathcal{L}_{CC}$, best with $\lambda_1=1$, $\lambda_2=0.7$

## Claims

**Claim:** TS-TCC cross-view temporal contrasting (predicting one view's future from the other view's context) learns representations robust to temporal perturbations, matching or exceeding supervised baselines in linear evaluation.
**Evidence:** Table 2: HAR 90.37%±0.34 vs Supervised 90.14%±2.49; Epilepsy 97.23%±0.10 vs 96.66%±0.24.
**Applicability:** Classification and transfer learning tasks on short-to-medium length multivariate TS (HAR 128 steps, Epilepsy 178 steps).
**Limitations:** Evaluated on sensor/biomedical signals — no forecasting benchmark; short series only; no asymmetric or directed objective.
**Contradictions:** TimeMAE later reports better performance on same HAR benchmark (91.31% linear eval vs 77.63% for TS-TCC in that setup).
**Decision impact:** TS-TCC is a solid SSL baseline for P2 ablation; demonstrates contrastive objectives work for TS classification, but symmetric design rules it out as a direct P2 encoder.
**Confidence:** high

**Claim:** Using two distinct augmentation types (weak and strong) rather than two instances of the same augmentation substantially improves representation quality.
**Evidence:** Table 4 ablation: TS-TCC with both aug types achieves HAR 90.37% vs 76.55% (weak-only) and 60.23% (strong-only).
**Applicability:** Time series where class-discriminative patterns span temporal scale (HAR, Sleep-EDF).
**Limitations:** Epilepsy dataset can achieve comparable performance with single augmentation — dataset-dependent.
**Contradictions:** None.
**Decision impact:** Dual-augmentation strategy is worth applying if P2 moves to contrastive pretraining; augmentation design matters more than architecture choice for TS.
**Confidence:** high

## Applicability to P2

Low-medium. TS-TCC produces **symmetric** representations — no directed/asymmetric objective. The temporal contrasting idea (cross-view future prediction) is relevant as inspiration but the contrastive framework does not support the target→covariate directional retrieval P2 requires. TS-TCC's transfer efficiency (10% labels match 100% supervised) is relevant for P2's large-scale training strategy.

## Related

- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — TS2Vec: improved hierarchical contrastive, symmetric
- [src-2026-06-li-ti-mae](src-2026-06-li-ti-mae.md) — Ti-MAE: masked autoencoder, symmetric
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — TimeMAE: decoupled MAE, symmetric, better classification results
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
