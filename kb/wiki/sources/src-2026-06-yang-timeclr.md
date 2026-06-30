---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-yang-timeclr
tags:
- ssl
- self-supervised
- contrastive
- dtw
- augmentation
- time-series
zotero: yangTimeCLRSelfsupervisedContrastive2022
source_hash: 6d03594d2a17d192061bad66ff5bd23679d3c0497d9246f9992faf73ac598d9d
---

# TimeCLR: A Self-Supervised Contrastive Learning Framework for Univariate Time Series Representation

**Yang, Zhang & Cui (2022) — Knowledge-Based Systems**

## Summary

Extends SimCLR to univariate TS. Two key innovations: (1) **DTW data augmentation** — a specially trained autoencoder that maps TS to a Euclidean latent space and generates phase shifts and amplitude changes (the phenomena DTW captures), without disrupting temporal structure; (2) an InceptionTime-based feature extractor. The augmentation is motivated by the DTW-based 1NN classifier's success: phase shifts and amplitude changes exist within the same class, so augmenting to produce them is semantically valid. Achieves comparable performance to supervised InceptionTime; generalises across domains.

## Key results

- Comparable performance to supervised InceptionTime on UCR classification datasets
- Better than supervised learning in insufficient-labels scenarios
- DTW augmentation outperforms jitter/permutation for contrastive learning on 8 UCR test sets
- Zero-shot transfer works across domains (feature extractor generalises)

## Architecture details

- DTW augmentation: siamese autoencoder (shared weights) trains to predict pairwise DTW distances in latent space; movement in latent space → phase shift + amplitude change in reconstructed TS
- Feature extractor: InceptionTime (multi-scale CNN, inception modules)
- Contrastive framework: SimCLR (two augmented views per sample; NT-Xent loss; large batch)
- Representation: pool InceptionTime output to single vector per series

## Claims

**Claim:** DTW-aware augmentation (via a pre-trained autoencoder generating phase shifts and amplitude changes in latent space) preserves TS temporal structure better than jitter/permutation for SimCLR contrastive learning.
**Evidence:** Yang et al. 2022, ablation in Section 5. DTW augmentation vs. standard augmentations on UCR; 1NN-DTW evaluation confirms structural preservation.
**Applicability:** Univariate TS contrastive learning. Phase shift / amplitude change phenomena are common in commodity prices — augmentation by analogy could be useful.
**Limitations:** Augmentation requires training a separate autoencoder first (extra step). Limited to univariate; SimCLR instance-level (not timestep-level) — not suitable for forecasting.
**Contradictions:** TS2Vec and TimeMAE outperform instance-level contrastive methods on most tasks; timestep-level representations are now preferred.
**Decision impact:** TimeCLR establishes that domain-aware augmentation (phase shift / amplitude change) is semantically valid for TS. For P2, this supports the idea that commodity price TS have natural symmetry-breaking phenomena (trend reversals, volatility shifts) that augmentation can exploit. Still symmetric.
**Confidence:** high

## Applicability to P2

Low. Symmetric SimCLR variant; instance-level representation; univariate only. Reference for DTW-aware augmentation design, but outperformed by more recent methods.

## Related

- [src-2026-06-foumani-series2vec](src-2026-06-foumani-series2vec.md) — also uses DTW-based similarity; more principled
- [src-2026-06-eldele-ts-tcc](src-2026-06-eldele-ts-tcc.md) — comparison contrastive method
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
