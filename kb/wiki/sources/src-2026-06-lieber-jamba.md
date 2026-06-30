---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-lieber-jamba
tags:
- ssm
- timeseries-forecasting
- background
zotero: lieberJambaHybridTransformerMamba2024
source_hash: 517673951e0ff6dbd27701e52f4ab5d3ccf3f40d3eddae3d4e27dcf90f38d665
---

# Source: Jamba: A Hybrid Transformer-Mamba Language Model (2024)

## Metadata
- **Citekey:** `lieberJambaHybridTransformerMamba2024`
- **Authors:** Lieber, Lenz, Bata, Cohen, Osin, Dalmedigos, et al. (AI21 Labs)
- **Venue:** arXiv 2024
- **Relevant projects:** P1 (background)

## One-line takeaway

Jamba interleaves Transformer attention layers with Mamba SSM layers and MoE modules into a production-scale hybrid architecture that fits a 52B-parameter model (12B active) in a single 80GB GPU while achieving 3x throughput over Mixtral-8x7B on long contexts.

## Key claims (background only)

- Jamba combines Transformer and Mamba layers at a configurable ratio (e.g., 1:7 attention-to-Mamba), reducing the KV cache to 8x smaller than a vanilla Transformer while maintaining comparable language modeling performance to Mixtral-8x7B and Llama-2-70B on standard benchmarks.
- The hybrid architecture trades off memory usage, training efficiency, and long-context quality, supporting up to 256K context tokens with state-of-the-art throughput; MoE increases total parameters without proportional compute increase.
- No TSF evaluation reported; benchmarks are standard language modeling, long-context understanding, and inference efficiency on text.

## Relevance to P1

Background: establishes Jamba as the first production-scale hybrid Transformer-Mamba model. P1 uses a compact MLP/linear backbone rather than hybrid SSM architectures due to deployment complexity, interpretability constraints, and absence of demonstrated TSF gains over linear baselines.
