---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-dao-mamba2
tags:
- ssm
- timeseries-forecasting
- background
zotero: daoTransformersAreSSMs2024
source_hash: 6fe16414fa471a5ab150cddcba5840d3a94e347e96992c50c12c1fb8b919479f
---

# Source: Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality (2024)

## Metadata
- **Citekey:** `daoTransformersAreSSMs2024`
- **Authors:** Dao, Gu
- **Venue:** ICML 2024
- **Relevant projects:** P1 (background)

## One-line takeaway

Mamba-2 unifies SSMs and attention through a structured state space duality (SSD) framework, yielding a 2–8x faster SSM layer with larger recurrent states while matching or exceeding Mamba and Transformer++ on language modeling benchmarks.

## Key claims (background only)

- The SSD framework shows that SSMs and variants of linear attention are mathematically dual through structured semiseparable matrices, enabling transfer of Transformer hardware optimizations (tensor parallelism, sequence parallelism) to SSMs.
- Mamba-2's SSD layer is 2–8x faster than Mamba's selective scan and supports state sizes 8x larger, crossing over with FlashAttention-2 speed at sequence length 2K and running 6x faster at 16K.
- No TSF evaluation reported; all benchmarks are language modeling (Pile, standard downstream NLP evaluations).

## Relevance to P1

Background: establishes Mamba-2 as the refined successor to Mamba with theoretical connections to linear attention. P1 uses a compact MLP/linear backbone rather than SSMs due to interpretability constraints and absence of compelling TSF gains over linear baselines.
