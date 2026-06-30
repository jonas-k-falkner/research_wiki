---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-sun-ttt
tags:
- ssm
- timeseries-forecasting
- background
zotero: sunLearningLearnTest2024
source_hash: 4a4917910c9605c463188c8760ef53013642b6cc8a12056a118571987a93b28f
---

# Source: Learning to (Learn at Test Time): RNNs with Expressive Hidden States (2024)

## Metadata
- **Citekey:** `sunLearningLearnTest2024`
- **Authors:** Sun, Li, Dalal, Xu, Vikram, Zhang, Dubois, Chen, Wang, Koyejo, Hashimoto, Guestrin
- **Venue:** arXiv 2024 (Stanford / UC San Diego / UC Berkeley)
- **Relevant projects:** P1 (background)

## One-line takeaway

TTT layers replace the fixed-size RNN hidden state with a small machine learning model (linear or MLP) updated by self-supervised learning on each input, enabling expressive long-context modeling at linear complexity that keeps improving beyond 16K tokens unlike Mamba.

## Key claims (background only)

- TTT (Test-Time Training) layers make the hidden state itself a model whose weights are updated by gradient steps on a self-supervised loss at inference time, allowing context compression to improve adaptively rather than being bounded by a fixed recurrence formula.
- TTT-Linear and TTT-MLP match or exceed both a strong Transformer and Mamba at 125M–1.3B parameters; unlike Mamba, TTT-Linear continues reducing perplexity beyond 16K tokens; TTT-Linear is faster than Transformer at 8K context and matches Mamba in wall-clock time.
- No TSF evaluation reported; all benchmarks are language modeling with varying context lengths.

## Relevance to P1

Background: establishes TTT layers as an expressive alternative hidden state for linear-complexity sequence models. P1 uses a compact MLP/linear backbone rather than TTT layers due to training complexity and absence of demonstrated TSF gains over linear baselines.
