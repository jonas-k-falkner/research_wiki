---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-yang-gla
tags:
- ssm
- timeseries-forecasting
- background
zotero: yangGatedLinearAttention2024
source_hash: 9965bc4f590fb2ba35c2146f660e145fd730c7d9f8c6e7be10ba9a11518383d6
---

# Source: Gated Linear Attention Transformers with Hardware-Efficient Training (2024)

## Metadata
- **Citekey:** `yangGatedLinearAttention2024`
- **Authors:** Yang, Wang, Shen, Panda, Kim
- **Venue:** ICML 2024 (MIT / MIT-IBM Watson)
- **Relevant projects:** P1 (background)

## One-line takeaway

GLA Transformer adds data-dependent gating to linear attention with a hardware-efficient chunkwise training algorithm (FLASHLINEARATTENTION), achieving competitive language modeling performance versus Mamba and LLaMA-architecture Transformers while being faster to train.

## Key claims (background only)

- GLA introduces input-dependent gating to the linear attention recurrence update, bridging the gap between static-decay methods (RetNet) and softmax attention; the FLASHLINEARATTENTION implementation is faster than FlashAttention-2 even on 1K sequences.
- GLA Transformer trained at 340M/1.3B parameters on 15B/100B tokens performs "competitively against the LLaMA-architecture Transformer" and outperforms RetNet and Mamba on length generalization (2K → 20K+).
- No TSF evaluation reported; all benchmarks are language modeling and NLP recall-intensive tasks.

## Relevance to P1

Background: establishes GLA as a hardware-efficient gated linear attention model. P1 uses a compact MLP/linear backbone rather than GLA due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
