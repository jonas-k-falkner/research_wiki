---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-yang-gated-delta
tags:
- ssm
- timeseries-forecasting
- background
zotero: yangGatedDeltaNetworks2025
source_hash: 55f84f2ae9c4e52ff494bfa699499867f5e9e17514994ac71de43888363a5fb9
---

# Source: Gated Delta Networks: Improving Mamba2 with Delta Rule (2025)

## Metadata
- **Citekey:** `yangGatedDeltaNetworks2025`
- **Authors:** Yang, Kautz, Hatamizadeh
- **Venue:** ICLR 2025 (NVIDIA)
- **Relevant projects:** P1 (background)

## One-line takeaway

Gated DeltaNet combines gating (rapid memory erasure) with the delta update rule (targeted key-value modification) into a unified linear recurrence that consistently outperforms Mamba2 and DeltaNet on language modeling and in-context retrieval benchmarks.

## Key claims (background only)

- The gated delta rule unifies two complementary memory management strategies: gating (uniform rapid erasure via α_t → 0) and the delta rule (targeted single key-value update), implemented with a hardware-efficient chunkwise parallel training algorithm extending the WY representation.
- Gated DeltaNet surpasses Mamba2 and DeltaNet on language modeling, commonsense reasoning, in-context retrieval, length extrapolation, and long-context understanding; hybrid variants combining Gated DeltaNet with sliding window attention further improve performance.
- No TSF evaluation reported; all benchmarks are language modeling and NLP tasks.

## Relevance to P1

Background: establishes Gated DeltaNet as a next-generation linear recurrent model improving on Mamba2. P1 uses a compact MLP/linear backbone rather than SSMs due to interpretability constraints and absence of compelling TSF gains over linear baselines.
