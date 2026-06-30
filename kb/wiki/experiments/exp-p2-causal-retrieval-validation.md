---
type: experiment
domain: embedding-models
project: P2
status: draft
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p2-causal-embedding-model
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-embedding-model-v1
tags:
- experiment
---

# Experiment: P2 causal retrieval validation

## Status

Designed-from-source, not yet run. Research-track; owner unassigned. Should run in parallel to P3 without blocking it (ADR-0001).

## Hypothesis

An asymmetric embedding trained from distilled Transfer-Entropy/Granger soft labels retrieves directionally-correct, high-impact covariates (A→B ≠ B→A) better than symmetric shape/DTW similarity, and these covariates improve downstream P1 forecast accuracy.

## V1 symmetric baseline

The concrete symmetric baseline to beat is the production v1 model ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)):

- **Encoder:** `ConvAttnEncoder` (TCN → MHA → meanmax pooling → 128-dim `z`)
- **Similarity objective:** SL head — Soft-DTW in x-space, L2 in z-space (weight 0.7)
- **Negative sampling:** `SimMemoryBuffer` (length-binned)
- **Production KPIs:** MAP@50 > 0.95, combined_rank_score > 0.925

P2 v2 replaces the SL head only. All other components (encoder, GL head, SimMemoryBuffer) are reused.

## Protocol (seed — from deck Slide 4 + gaze note)

1. Compute pairwise TE/Granger scores on a tractable subset of series using `GrangerSelector` / `TransferEntropySelector` as the distillation teacher.
2. Train a directed/asymmetric SL head on the `ConvAttnEncoder` backbone, supervised by the soft labels from step 1. Use `SimMemoryBuffer` for directed negative sampling.
3. Build a vector index over embeddings; query with target series → retrieve top-k candidate drivers.
4. Evaluate on (a) held-out directional retrieval vs held-out TE/Granger and (b) downstream forecast lift inside a P1-style cluster model.

## Metrics

- **Retrieval (primary):** MAP@50 vs v1 symmetric baseline; A→B vs B→A consistency (directional ranking gap).
- **Geometry health:** does training converge to a stable asymmetric space, or collapse to symmetric?
- **Downstream:** forecast lift over v1 shape/DTW covariates on held-out series.
- **Retrieval latency:** at target 200M-series scale (FAISS index).

## To specify before running

- TE/Granger estimator + lag selection on the distillation subset.
- Pairwise-label sampling strategy (open question in [shared/open-questions](../shared/open-questions.md)).
- Which P1 task is the first downstream validation target.
- Pretraining stage: MAE backbone preferred at sparse label ratio (< 0.1) — see [src-2026-06-liu-ssl-comparison](../sources/src-2026-06-liu-ssl-comparison.md).

## Literature to integrate `[verify]`

- Asymmetric/order embeddings; hyperbolic embeddings (Nickel & Kiela) `[verify]`
- Transfer Entropy estimation, conditional TE `[verify]`
- Distillation of expensive pairwise relations into retrieval spaces `[verify]`

## Expected failure modes (project-specific)

- Distilled labels are noisy/regime-bound → embedding learns the noise, retrieval fails out-of-regime.
- Geometry collapses to symmetric → no directional signal.
- Retrieval returns correlated-but-non-causal series that add no forecast lift → "causal" framing unjustified; downgrade to "candidate driver retrieval".

## Decision impact

Go / modify / defer on whether P2 graduates from research thread to P1 covariate-layer dependency.

## Related pages

- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [sources/src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md) — v1 production baseline architecture
