---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-gu-mamba
tags:
- ssm
- timeseries-forecasting
- background
zotero: guMambaLinearTimeSequence2024
source_hash: adf70ed1803c85b1899dec3e21f3af0b124411439e8654b840ea65f7b9f52b2e
---

# Source: Mamba: Linear-Time Sequence Modeling with Selective State Spaces (2024)

## Metadata
- **Citekey:** `guMambaLinearTimeSequence2024`
- **Authors:** Gu, Dao
- **Venue:** arXiv 2024 (also NeurIPS 2024)
- **Relevant projects:** P1 (background)

## One-line takeaway

Mamba introduces a selective state space model (SSM) with input-dependent parameters and a hardware-aware parallel scan, achieving Transformer-quality language modeling at linear sequence length complexity.

## Key claims (background only)

- Selective SSMs address the key weakness of prior LTI SSMs — inability to perform content-based reasoning — by making parameters input-dependent, enabling selective propagation or forgetting of information.
- Mamba achieves 5x higher throughput than Transformers of the same size and matches or exceeds Transformer performance on language, audio, and genomics at scales up to 3B parameters.
- No TSF evaluation reported; benchmarks focus on language modeling, audio waveform generation, and DNA sequence modeling.

## Relevance to P1

Background: establishes that Mamba exists as a subquadratic alternative sequence model primarily designed for language modeling. P1 uses a compact MLP/linear backbone rather than SSMs due to interpretability constraints (SSM hidden states are opaque to the AttGrad attribution protocol) and absence of compelling TSF gains over linear baselines.
