---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-choi-multitask-ssl
tags:
- ssl
- self-supervised
- multi-task
- contrastive
- time-series
zotero: choiMultiTaskSelfSupervisedTimeSeries2023
source_hash: f5061136eb8ee1901af579c678ccf7da02ae4cc0440fce6d8d2e3fbd836ada6f
---

# Multi-Task Self-Supervised Time-Series Representation Learning

**Choi & Kang (2023) — ICLR 2023 (workshop or poster)**

## Summary

Proposes combining three existing SSL consistency types — contextual (TS2Vec), temporal (TNC), and transformation (TS-TCC) — in a single multi-task framework. A shared TS2Vec dilated-CNN encoder is optimized jointly with all three contrastive losses. Uncertainty weighting (Kendall et al.) automatically balances loss magnitudes without manual weight tuning. Evaluated on time series classification, forecasting, and anomaly detection. Outperforms each single-consistency baseline and shows strong cross-domain transfer.

## Key results

- Multi-task combination outperforms single-consistency baselines on all three downstream tasks (classification, forecasting, anomaly detection)
- Uncertainty weighting outperforms fixed-weight multi-task combination
- Strong cross-domain transfer: representations generalize to unseen domains better than single-task SSL
- Architecture reuses TS2Vec dilated CNN encoder with shared weights across all tasks

## Architecture details

- Shared encoder: TS2Vec dilated CNN (10 residual blocks, dilated 1D conv)
- Contextual consistency (TS2Vec): hierarchical timestamp-wise + instance-wise contrastive on overlapping subseries
- Temporal consistency (TNC): neighborhood vs. non-neighborhood discriminator; Augmented Dickey-Fuller test for stationarity boundary
- Transformation consistency (TS-TCC): weak/strong augmented views as positive pairs; SimCLR instance-wise loss
- Multi-task loss: uncertainty-weighted sum L_total = Σ (1/α_i²) × L_i + log(α_i)
- Inputs: overlapping cropped subseries (shared across all three tasks)

## Claims

**Claim:** Combining contextual, temporal, and transformation consistencies in a single multi-task framework with uncertainty weighting outperforms any single-consistency SSL method on TS classification, forecasting, and anomaly detection.
**Evidence:** Choi & Kang 2023, experimental tables. Multi-task model beats TS2Vec, TS-TCC, and TNC individually; uncertainty weighting beats fixed weights.
**Applicability:** Any TS domain where multiple types of temporal structure coexist. More relevant for general-purpose encoders than for P2's directed objective.
**Limitations:** Still symmetric — all three combined consistencies treat both series in a pair identically. More complex to tune than single-method SSL.
**Contradictions:** TimeMAE (2023) achieves stronger HAR classification than multi-task contrastive combinations — masking-based methods now dominate classification.
**Decision impact:** Confirms that combining complementary SSL signals improves generalization. P2 could consider combining a symmetric backbone with a directed asymmetric loss head (multi-task setup where the directed TE-distillation head is one task).
**Confidence:** high

## Applicability to P2

Low-medium. Method is symmetric. However, the multi-task training pattern (shared encoder, multiple specialized loss heads) is directly applicable to P2's design: a symmetric backbone trained with contextual/temporal consistency as auxiliary tasks, plus a directed TE-distillation head as the primary asymmetric objective.

## Related

- [src-2026-06-eldele-ts-tcc](src-2026-06-eldele-ts-tcc.md) — transformation consistency component
- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — contextual consistency component
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
