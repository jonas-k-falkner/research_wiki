---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-peng-eagle-finch
tags:
- ssm
- timeseries-forecasting
- background
zotero: pengEagleFinchRWKV2024
source_hash: a3dfadd8619d698b065fefccc8e13e09e92002649977f6cd0c0b70cdfd4ca177
---

# Source: Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence (2024)

## Metadata
- **Citekey:** `pengEagleFinchRWKV2024`
- **Authors:** Peng, Goldstein, Anthony, et al. (EleutherAI / RWKV Project)
- **Venue:** arXiv 2024
- **Relevant projects:** P1 (background)

## One-line takeaway

Eagle (RWKV-5) and Finch (RWKV-6) improve on RWKV-4 by introducing multi-headed matrix-valued recurrent states and a dynamic recurrence mechanism, achieving competitive performance across multilingual NLP benchmarks at 0.46–7.5B parameters.

## Key claims (background only)

- Eagle (RWKV-5) and Finch (RWKV-6) extend RWKV-4 with multi-headed matrix-valued states (expanding recurrent state expressivity) and dynamic recurrence via token shift, improving performance while retaining RNN constant-memory inference efficiency.
- Models trained on a new 1.12 trillion token multilingual corpus achieve competitive performance versus similarly-sized Transformers on LM Evaluation Harness, associative recall, and long-context benchmarks.
- No TSF evaluation reported; all benchmarks are language modeling and NLP tasks.

## Relevance to P1

Background: establishes Eagle/Finch as the next-generation RWKV architecture. P1 uses a compact MLP/linear backbone rather than RWKV variants due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
