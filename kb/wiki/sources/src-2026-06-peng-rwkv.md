---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-peng-rwkv
tags:
- ssm
- timeseries-forecasting
- background
zotero: pengRWKVReinventingRNNs2023
source_hash: 57d18c40bdbb4bc1ab69c078a304f97e31657b4f543c408d8a5520e672a3fab0
---

# Source: RWKV: Reinventing RNNs for the Transformer Era (2023)

## Metadata
- **Citekey:** `pengRWKVReinventingRNNs2023`
- **Authors:** Peng, Alcaide, Anthony, et al. (EleutherAI)
- **Venue:** EMNLP 2023
- **Relevant projects:** P1 (background)

## One-line takeaway

RWKV combines RNN inference efficiency (linear complexity, constant memory) with Transformer-style parallelizable training via a linear attention mechanism, scaling to 14B parameters and matching similarly sized Transformers on NLP benchmarks.

## Key claims (background only)

- RWKV replaces dot-product token interaction with channel-directed linear attention (WKV mechanism), enabling the model to be formulated as either a Transformer for parallel training or an RNN for constant-time-per-step autoregressive inference.
- RWKV scales to 14B parameters (the largest dense RNN trained at publication) and matches similarly sized Transformers on twelve NLP tasks while requiring O(Td) time and O(d) memory versus O(T²d) and O(T²+Td) for standard Transformers.
- No TSF evaluation reported; all benchmarks are NLP tasks evaluated via language modeling harness.

## Relevance to P1

Background: establishes RWKV as a linear-complexity recurrent model for language modeling. P1 uses a compact MLP/linear backbone rather than RWKV due to interpretability constraints and absence of compelling TSF gains over linear baselines.
