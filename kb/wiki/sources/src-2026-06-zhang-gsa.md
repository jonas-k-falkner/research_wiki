---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-zhang-gsa
tags:
- ssm
- timeseries-forecasting
- background
zotero: zhangGatedSlotAttention2024
source_hash: 8517e5a607c38ec84bf667d5cefc7f3a6f4cd7afa1291b8be7fd4d353d725492
---

# Source: Gated Slot Attention for Efficient Linear-Time Sequence Modeling (2024)

## Metadata
- **Citekey:** `zhangGatedSlotAttention2024`
- **Authors:** Zhang, Yang, Zhu, Zhang, Cui, Wang, Wang, Shi, Wang, Bi, Zhou, Fu
- **Venue:** NeurIPS 2024 (Soochow / MIT / Tencent)
- **Relevant projects:** P1 (background)

## One-line takeaway

Gated Slot Attention (GSA) enhances linear attention by combining softmax-based bounded-memory control (ABC) with GLA-style gating, enabling efficient in-context recall and effective finetuning of pretrained Transformers to linear RNNs without full retraining.

## Key claims (background only)

- GSA reformulates ABC as two-pass linear attention linked via softmax, incorporating GLA-style data-dependent gating to improve adaptive forgetting while retaining the softmax operation that reduces discrepancy when finetuning pretrained Transformer models to RNNs.
- GSA significantly outperforms other linear models on in-context recall-intensive tasks without requiring large state sizes, and surpasses RWKV6-7B and Mamba-7B when finetuning Mistral-7B to the GSA architecture.
- No TSF evaluation reported; benchmarks are language modeling, in-context recall, and Transformer-to-RNN finetuning evaluations.

## Relevance to P1

Background: establishes GSA as a linear attention model optimized for in-context recall and pretrained model conversion. P1 uses a compact MLP/linear backbone rather than linear attention variants due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
