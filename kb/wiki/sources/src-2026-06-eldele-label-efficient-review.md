---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-eldele-label-efficient-review
tags:
- ssl
- self-supervised
- semi-supervised
- survey
- time-series
zotero: eldeleLabelefficientTimeSeries2024
source_hash: 561915c05becfb6adf9bc01e147f1e77268e566ecb9add9aed2e96d97fe16ce9
---

# Label-efficient Time Series Representation Learning: A Review

**Eldele et al. (2024) — IEEE Transactions on Neural Networks and Learning Systems (survey)**

## Summary

Comprehensive survey of label-efficient deep learning for time series. Introduces a novel taxonomy based on whether methods rely on external data sources: **in-domain** (data augmentation, SSL, semi-supervised learning — no external sources) vs. **cross-domain** (transfer learning, domain adaptation — uses external labeled source domain). Reviews three data scenarios: limited labels, fully unlabeled, and mixed labeled+unlabeled. Covers 100+ methods across all categories. This is a survey paper — no new experimental results.

## Taxonomy

**In-domain strategies:**
- Data augmentation (when only few labeled samples exist): jitter, scaling, TimeWarp, window slicing, GAN-based synthesis
- Self-supervised learning (fully unlabeled): contrastive (TS-TCC, TS2Vec, Series2Vec), masked autoencoder (Ti-MAE, TimeMAE, TST), generative
- Semi-supervised learning (mixed labeled + unlabeled): FixMatch-style, self-training with pseudo-labels, CA-TCC

**Cross-domain strategies:**
- Transfer learning: fine-tune pretrained encoder from source domain to target
- Domain adaptation: align source and target distributions without labeled target data

## Claims

**Claim:** The fundamental challenge of label-efficient TS learning splits cleanly into in-domain (no external data) and cross-domain (leverages labeled source domain) strategies, with each suited to different data availability scenarios.
**Evidence:** Eldele et al. 2024 taxonomy overview (IEEE TNNLS survey).
**Applicability:** Meta-level guidance for P2 training design. P2 operates in-domain (abundant unlabeled TS, few TE/Granger labels) — in-domain semi-supervised SSL is the right category.
**Limitations:** Survey paper — no new performance numbers. Coverage is as of early 2024; does not include 2024-2025 advances (TimeKAN, TOTEM, etc.).
**Contradictions:** None (survey).
**Decision impact:** Confirms P2's correct quadrant: in-domain semi-supervised SSL using a phased pretrain-then-refine approach (CA-TCC is the reference). Cross-domain transfer is not the right paradigm for P2 because commodity/price TS domains are too distinct from standard HAR/ECG benchmarks.
**Confidence:** medium

## Applicability to P2

Medium. Useful as a structured literature map. The in-domain / cross-domain taxonomy clarifies that P2 should stay in-domain (pretrain on unlabeled commodity TS, not transfer from ECG/HAR). No new technical content beyond the other four HIGH-priority papers.

## Related

- [src-2026-06-eldele-ca-tcc](src-2026-06-eldele-ca-tcc.md) — CA-TCC, the semi-supervised method from the same team
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md), [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — SSL methods covered in survey
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
