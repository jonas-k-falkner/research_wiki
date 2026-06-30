---
type: source
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-06-25
sources:
- src-2026-06-p2-causal-embedding-model
tags:
- embedding
- causal
- transfer-entropy
- retrieval
---

# Source: P2 — Causal embedding model v2

## Metadata

- Source ID: `src-2026-06-p2-causal-embedding-model`
- Raw path: `raw/seed/p2_causal_embedding_model.md`
- Source type: seed design note (grounded in the `embedding_model` repo)
- Date: June 2026
- Upstream origin: [src-2026-05-sybilion-ai-projects-review](src-2026-05-sybilion-ai-projects-review.md) (deck Slide 4)
- Relevant projects: P2 (feeds P1)

## One-line takeaway

Retrain the existing 128-dim encoder with a directed, asymmetric objective (Transfer Entropy / Granger distillation) so vector proximity approximates causal influence, enabling millisecond top-k covariate retrieval over the series space in place of O(n²) explicit Granger/TE search.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Explicit Granger/TE covariate search does not scale. | O(n²) over ~200M series is intractable; analysts fall back to manual/pre-filtered sets. | Motivates retrieval-based discovery. | medium |
| A directed objective can encode causal influence as proximity. | Distil pairwise TE/Granger on a subset into an asymmetric space (A→B ≠ B→A). | P2 changes the objective, not the ConvAttn backbone; replaces today's symmetric Soft-DTW similarity. | medium |
| Retrieval is 100–1000× faster than explicit selection. | Vector search vs pairwise computation. | Speed is the headline value (deck claim — unvalidated). | low |
| Retrieved series are candidate, not confirmed, causal drivers. | Correlation ≠ causation; distilled labels are estimator/lag/regime dependent. | Use "candidate causal retrieval"; validate via downstream forecast lift. | medium |

## Risks

- Asymmetric geometry convergence (deck key risk) — may collapse to symmetric similarity.
- Distilled-label noise and coverage; regime dependence.

## Product implications

- `z_cov` causal embeddings feed P1's covariate-attention layer (replacing shape-similarity embeddings).
- P1's cluster forecasting task is P2's downstream validation beyond ranking metrics.
- Reuse `GrangerSelector` / `TransferEntropySelector` as the distillation teacher; reuse `SimMemoryBuffer` for negative sampling.

## Open questions

- Which asymmetric geometry (source/target heads, order/hyperbolic, asymmetric distance head)?
- Pairwise-label sampling strategy on the distillation subset.

## See also

- [sources/src-2026-06-embedding-model-v1](src-2026-06-embedding-model-v1.md) — v1 production architecture context (ConvAttnEncoder, SSL heads, SimMemoryBuffer, KPIs); the concrete symmetric baseline this source's asymmetric proposal builds on.

## Updated pages

- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
- [experiments/exp-p2-causal-retrieval-validation](../experiments/exp-p2-causal-retrieval-validation.md)
