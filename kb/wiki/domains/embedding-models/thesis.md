---
type: domain
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
  - thesis
  - embeddings
---

# Domain thesis: Embedding models

## Current thesis

The strategic embedding opportunity is to move from symmetric shape similarity toward directed, query-dependent covariate influence. P2 aims to make causal covariate discovery approximately retrievable rather than explicitly quadratic.

## Main research question

Can an asymmetric embedding objective distilled from Transfer Entropy or Granger-style labels recover useful directed covariates at scale, and does this improve downstream forecasting or scenario quality?

## Evaluation hierarchy

1. Directional retrieval metrics against held-out TE/Granger-style labels.
2. Robustness across regimes and horizons.
3. Downstream forecast lift in P1-like cluster models.
4. Explanation usefulness in P3/P4-style decision surfaces.

## Caveat

P2 should be treated as causal-candidate retrieval, not proof of causal effect. Claims need validation through forecasting lift, robustness checks, and where possible intervention-like tests.

## Sources & related

- [sources/src-2026-06-p2-causal-embedding-model](../../sources/src-2026-06-p2-causal-embedding-model.md), [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md)
- Project: [projects/p2-causal-embedding-v2](../../projects/p2-causal-embedding-v2.md)
