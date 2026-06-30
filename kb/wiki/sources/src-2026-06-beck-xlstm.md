---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-beck-xlstm
tags:
- ssm
- timeseries-forecasting
- background
zotero: beckXLSTMExtendedLong2024
source_hash: 8cfe1b57d0ab668a7ea82d05e1ce0d962cbf19cf9f05f3b440510555dc3370e6
---

# Source: xLSTM: Extended Long Short-Term Memory (2024)

## Metadata
- **Citekey:** `beckXLSTMExtendedLong2024`
- **Authors:** Beck, Pöppel, Spanring, Auer, Prudnikova, Kopp, Klambauer, Brandstetter, Hochreiter
- **Venue:** NeurIPS 2024 (ELLIS Unit / JKU Linz)
- **Relevant projects:** P1 (background)

## One-line takeaway

xLSTM extends LSTMs with exponential gating (sLSTM) and a parallelizable matrix memory cell (mLSTM), scaling to billions of parameters and achieving performance competitive with Transformers and SSMs on language modeling benchmarks.

## Key claims (background only)

- xLSTM introduces two new memory cells: sLSTM with exponential gates and new memory mixing, and mLSTM with a matrix memory and covariance update rule that is fully parallelizable — addressing the three core LSTM limitations (inability to revise decisions, limited storage capacity, non-parallelizability).
- xLSTM performs "favorably when compared to state-of-the-art Transformers and State Space Models, both in performance and scaling" on language modeling up to billions of parameters.
- No TSF evaluation reported; benchmarks focus on language modeling (Wikitext-103, synthetic nearest-neighbor search, rare token prediction).

## Relevance to P1

Background: establishes xLSTM as a modernized LSTM alternative to Transformers and SSMs for language modeling. P1 uses a compact MLP/linear backbone rather than xLSTM due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
