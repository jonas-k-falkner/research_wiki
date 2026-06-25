---
type: concept
domain: embedding-models
project: P2
status: active
confidence: medium
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-p2-causal-embedding-model
  - src-2026-06-p1-cluster-pretrained-deep-models
tags:
  - concept
---

# Causal covariate embeddings

## Definition

Directed/asymmetric time-series embeddings where vector proximity is trained to approximate causal/directed influence (covariate → target), not symmetric shape similarity, so that top-k covariate retrieval via vector search substitutes for explicit O(n²) Granger/Transfer-Entropy search. See [sources/src-2026-06-p2-causal-embedding-model](../sources/src-2026-06-p2-causal-embedding-model.md).

## Why it matters

Explicit TE/Granger over a ~200M-series universe is intractable (the deck's stated bottleneck), and retrieval-speed covariate discovery is the proposed P2 moat. The hard, unvalidated part is whether an asymmetric geometry converges and whether retrieved drivers are causal rather than merely correlated.

## Open research questions

- Can a vector space represent asymmetric relations (A→B ≠ B→A) stably without collapsing to symmetric similarity?
- Are distilled TE/Granger soft labels reliable enough to train on, and do they transfer across regimes/horizons?
- Retrieved covariates are *candidate* causal drivers — what validation (downstream forecast lift, intervention-style tests) is needed before any causal language is used externally?

## Literature to integrate `[verify]`

- Asymmetric / order embeddings: order-embeddings (Vendrov et al.), entailment cones, hyperbolic/Poincaré embeddings (Nickel & Kiela) as candidate geometries `[verify]`
- Transfer Entropy (Schreiber) and Granger causality estimation at scale; conditional/multivariate TE `[verify]`
- Knowledge distillation from expensive pairwise scores into a learned retrieval space `[verify]`
- Causal discovery caveats: correlation-vs-causation failure modes in observational time series

## Cross-project relevance

- Feeds [concepts/hierarchical-entmax-covariate-selection](hierarchical-entmax-covariate-selection.md) and the P1 attention layer ([projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)).
- Could supply candidate relation retrieval for P4, but P4 must keep provenance ([concepts/explicit-evidence-graph](explicit-evidence-graph.md)).

## Related pages

- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
