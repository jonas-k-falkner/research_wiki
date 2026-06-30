---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-peters-sparse-seq2seq-2019
tags:
- source
- sparse-attention
- entmax
- seq2seq
citekey: petersSparseSequencetoSequenceModels2019
source_hash: f2a6214933e8150ad1d85134460ecb1675c36f9ce00f6bb6570022e5c98814ca
author: Peters, Ben; Niculae, Vlad; Martins, André F. T.
year: 2019
title: Sparse Sequence-to-Sequence Models
venue: ACL 2019
zotero: petersSparseSequencetoSequenceModels2019
---

# Peters et al. (2019) — Sparse Sequence-to-Sequence Models

## Summary

Introduces the α-entmax transformation family as a drop-in replacement for softmax in seq2seq attention and output layers. α-entmax interpolates between softmax (α=1), 1.5-entmax, and sparsemax (α=2); values α>1 produce exactly-zero weights for low-scoring elements. The paper provides an exact O(d log d) algorithm for 1.5-entmax and demonstrates near-softmax GPU speed. Evaluated on CoNLL-SIGMORPHON 2018 morphological inflection and three MT language pairs (six directions).

## Key claims

1. 1.5-entmax is the empirical sweet spot in the α-entmax family: it outperforms softmax (BLEU 26.17 vs 25.70 on DE→EN) and sparsemax (24.69) on neural machine translation, consistently across language pairs.
2. Sparse attention via 1.5-entmax dramatically reduces average non-zero attention weights per step: softmax 24.25 vs 1.5-entmax 5.55 vs sparsemax 3.75 — enabling interpretable, focused attention patterns.
3. Sparse output distributions concentrate all probability mass on a single output sequence in 81% of high-resource morphological inflection cases, confirming that sparse output and sparse attention can be combined end-to-end.

## Relevance to P1

Direct algorithmic foundation for hierarchical entmax covariate selection. Establishes that 1.5-entmax is the recommended α value for training stability + sparsity, provides the exact O(d log d) algorithm, and shows interpretable sparse attention patterns are achievable in practice. Confirms the entmax mechanism is not just theoretical — it achieves better task performance than softmax in the settings tested.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/attention-faithfulness](../concepts/attention-faithfulness.md)
