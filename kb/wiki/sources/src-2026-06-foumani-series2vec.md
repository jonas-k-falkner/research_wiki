---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-foumani-series2vec
tags:
- ssl
- self-supervised
- contrastive
- similarity
- time-series
zotero: foumaniSeries2vecSimilaritybasedSelfsupervised2024
source_hash: 099af51812b31bd7085e084567ebfd9e2d85942ca62ccf5048b06682de317fb8
---

# Series2Vec: Similarity-based Self-Supervised Representation Learning for Time Series Classification

**Foumani et al. (2024) — Data Mining and Knowledge Discovery (DMKD) / Springer**

## Summary

Proposes Series2Vec, an SSL method that replaces hand-crafted data augmentation with a similarity-prediction pretext task. The encoder is trained to preserve pairwise Soft-DTW distances in the time domain and Euclidean distances in the frequency domain — both computed on the original unaugmented series. Order-invariant self-attention across the batch reinforces that similar series get similar representations. No augmentation is used during pretraining. Evaluated on UCR/UEA archive plus 9 large real-world datasets; outperforms existing SSL methods. Can be fused with other SSL methods for further gains.

## Key results

- Outperforms TS-TCC, TS2Vec, Ti-MAE, and TimeMAE on UCR/UEA classification under linear evaluation
- Fusion with other SSL representations yields further improvement
- No augmentation needed — avoids the semantic corruption risk documented for jitter/permutation on irregular TS
- Code and models open-sourced

## Architecture details

- Time encoder (disjoint CNN) + frequency encoder (disjoint CNN, applied to Fourier spectrum)
- Similarity function: Soft-DTW for time domain (differentiable, GPU-optimised); Euclidean for frequency domain
- Loss: similarity-preserving MSE between encoder-space distances and Soft-DTW/Euclidean distances
- Order-invariant self-attention applied across the batch to enforce global similarity consistency
- Final representation: concatenation of time and frequency encoder outputs

## Claims

**Claim:** Series2Vec avoids augmentation-based semantic corruption by using Soft-DTW pairwise similarity as the SSL pretext target; this produces higher-quality representations than jitter/permutation-based contrastive methods on UCR/UEA classification.
**Evidence:** Foumani et al. 2024, Table 3/4; outperforms TS-TCC, TS2Vec, Ti-MAE, TimeMAE on UCR/UEA under linear eval. Also shows 1NN-DTW accuracy drops from 0.89 to 0.77 when using TS-TCC augmented data, motivating the approach.
**Applicability:** TS classification and any downstream task where augmentation semantics are unclear. Less directly relevant to P2's directed/asymmetric objective, but the similarity-preservation approach is a useful design pattern.
**Limitations:** Soft-DTW is O(L²) — expensive for long series. Frequency encoder adds compute. Still symmetric.
**Contradictions:** TimeMAE (Cheng et al. 2023) achieves higher linear eval accuracy on HAR; comparison depends on dataset.
**Decision impact:** Series2Vec confirms that similarity-preserving pretext tasks outperform augmentation-based ones for irregular TS. P2 could consider using directional similarity measures (TE/Granger) as the pretext target — same conceptual approach but with asymmetric targets.
**Confidence:** high

**Claim:** All published SSL TS representation methods (TS-TCC, TS2Vec, Ti-MAE, TimeMAE, Series2Vec) are symmetric — none implement a directed/asymmetric pretext objective where A→B ≠ B→A.
**Evidence:** Architectural review of Series2Vec + prior literature confirms symmetric Soft-DTW/Euclidean targets.
**Applicability:** Directly confirms the P2 research gap.
**Limitations:** Survey as of 2024.
**Contradictions:** None found.
**Decision impact:** Additional support for P2 novelty claim established in I-P2-A (see [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md)).
**Confidence:** high

## Applicability to P2

Medium. Series2Vec is still a symmetric method, but its core design principle — use a meaningful TS-specific similarity measure as the pretext target — is directly applicable to P2. P2's directed pretext could adopt the same framework but replace Soft-DTW with Transfer Entropy as the directed similarity target.

## Related

- [src-2026-06-yue-ts2vec](src-2026-06-yue-ts2vec.md) — comparison baseline
- [src-2026-06-cheng-timemae](src-2026-06-cheng-timemae.md) — SSL symmetry gap synthesis
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
