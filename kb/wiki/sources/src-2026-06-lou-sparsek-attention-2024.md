---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-lou-sparsek-attention-2024
tags:
- source
- sparse-attention
- linear-attention
- llm
citekey: louSparserFasterLess2024
source_hash: 4e0132efade352c9db34f30f678294e25fb1751cf92d9954d7313eb19dbcc8d6
author: Lou, Ziteng; Shi, Hanlin; Huang, Difan; Pan, Jingyang; Zhao, Kun; Lin, Jian
year: 2024
title: 'Sparser, Faster, Less Is More: Efficient Sparse Attention with SPARSEK'
venue: arXiv 2024
zotero: louSparserFasterLess2024
---

# Lou et al. (2024) — SPARSEK Attention

## Summary

Introduces SPARSEK Attention, a linear-time sparse attention mechanism for LLMs. Uses a scoring network that evaluates key-value importance independently of queries, enabling differentiable top-k masking without quadratic cost. Designed for long-context language modeling where full attention is computationally infeasible. The scoring network produces sparse selection of which KV pairs to attend to before computing queries, making it memory-efficient.

## Key claims

1. SPARSEK uses a query-independent scoring network to evaluate KV importance, enabling linear-time sparse attention for LLMs while maintaining differentiability through a soft top-k masking mechanism.
2. Decoupling KV scoring from query computation allows precomputing which positions to attend to, reducing memory usage for long-sequence models — the scoring overhead is amortized across all queries.
3. SPARSEK is designed for LLM long-range sequence modeling, not covariate selection; it sparsifies token positions within a sequence rather than selecting among heterogeneous input feature types.

## Relevance to P1

Tangentially relevant: SPARSEK demonstrates that differentiable sparse top-k selection at scale is feasible in 2024 Transformer practice, which is background support for the entmax approach in P1. The query-independent scoring idea has a conceptual parallel to cluster-level routing (cluster routing is also independent of within-cluster attention). However, SPARSEK is not directly applicable to covariate selection in forecasting.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
