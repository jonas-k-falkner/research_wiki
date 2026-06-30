---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-zhao-sparse-transformer-2019
tags:
- source
- sparse-attention
- transformer
- topk
citekey: zhaoetal.SparseTransformerConcentrated2019
source_hash: 7c30496286a4d573fa0ac8b54c7f45888744d2d8221f91ca78f82930bf04bc37
author: Zhao, Guangxiang; Sun, Xu; Xu, Jingjing; Zhang, Zhiyuan; Luo, Liangchen
year: 2019
title: 'SPARSE TRANSFORMER: Concentrated Attention Through Explicit Selection'
venue: arXiv 2019
zotero: zhaoetal.SparseTransformerConcentrated2019
---

# Zhao et al. (2019) — Sparse Transformer: Concentrated Attention Through Explicit Selection

## Summary

Proposes a Sparse Transformer that applies explicit top-k selection to concentrate attention on the k most relevant positions, rather than distributing attention across all sequence positions. Implemented by masking out all but the top-k attention scores before applying softmax. Evaluated on NMT (IWSLT EN-VI, DE-EN) and image captioning and language modeling. Achieves state-of-the-art on IWSLT 2015 EN-VI and 2014 DE-EN translation benchmarks.

## Key claims

1. Explicit top-k selection before softmax forces concentrated attention on the k most relevant positions, reducing distraction from irrelevant context and improving alignment quality compared to vanilla Transformer attention.
2. Sparse Transformer achieves state-of-the-art performance on IWSLT 2015 EN-VI and IWSLT 2014 DE-EN translation, demonstrating that concentrated sparse attention improves task performance not just efficiency.
3. Top-k masking at the top Transformer layers is especially beneficial: vanilla Transformer's upper layers concentrate on end-of-sequence positions (a failure mode), while Sparse Transformer exhibits more informative attention patterns at those layers.

## Relevance to P1

Provides a hard top-k baseline alternative to entmax's continuous sparse selection. The key distinction: top-k mask + softmax produces a non-differentiable boundary (the k-th score cutoff is discontinuous), whereas α-entmax produces a differentiable sparse selection. For P1 training, entmax is preferable; Zhao et al.'s results confirm that sparse concentrated attention improves NLP task performance, supporting the general principle behind P1's design.

## Related pages

- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
