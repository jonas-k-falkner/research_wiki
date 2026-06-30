---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-tay-sparse-sinkhorn-attention-2020
tags:
- source
- sparse-attention
- sinkhorn
- sequence-modeling
citekey: taySparseSinkhornAttention2020
source_hash: bc28fffdb31dd25a940a071a13422aa08c7f6fe0295cee7b60870ccfee56733f
author: Tay, Yi; Bahri, Dara; Yang, Liu; Metzler, Donald; Juan, Da-Cheng
year: 2020
title: Sparse Sinkhorn Attention
venue: ICML 2020
zotero: taySparseSinkhornAttention2020
---

# Tay et al. (2020) — Sparse Sinkhorn Attention

## Summary

Proposes Sparse Sinkhorn Attention for efficient sequence modeling. Uses differentiable sorting via Sinkhorn operators to produce block-wise sparse attention patterns. The standard variant has O(B² + N²B) memory complexity (B = block size, N = sequence length); the SORTCUT variant achieves O(l·Nk) linear complexity. Evaluated on language modeling, sorting, and summarization tasks.

## Key claims

1. Sinkhorn-based differentiable sorting enables end-to-end trainable sparse attention without discrete top-k operations, maintaining gradient flow through the sparsification step.
2. The SORTCUT variant achieves linear O(l·Nk) memory complexity versus O(l²) for full attention, enabling longer sequences — but block-level granularity means individual position selection is not as fine-grained as token-level entmax.
3. Sparse Sinkhorn Attention targets sequence position sparsification (which blocks of tokens to attend), not feature/covariate selection; the mechanism is structural rather than semantic.

## Relevance to P1

Background reference for differentiable sparse selection mechanisms. The Sinkhorn approach shows that block-sparse selection can be learned end-to-end, providing methodological context for the entmax approach in P1. However, Sinkhorn's block granularity and sequence-position focus make it less applicable than α-entmax for covariate selection, where we want to select among semantically distinct feature variables rather than contiguous token blocks.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
