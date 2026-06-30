---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-qin-hgrn2
tags:
- ssm
- timeseries-forecasting
- background
zotero: qinHGRN2GatedLinear2024
source_hash: 82ac48e18d24d639444eb981a64981aaf5aa84339c15717b9f5b48095f08660c
---

# Source: HGRN2: Gated Linear RNNs with State Expansion (2024)

## Metadata
- **Citekey:** `qinHGRN2GatedLinear2024`
- **Authors:** Qin, Yang, Sun, Shen, Li, Sun, Zhong
- **Venue:** arXiv 2024 (MIT CSAIL / OpenNLPLab)
- **Relevant projects:** P1 (background)

## One-line takeaway

HGRN2 expands HGRN's recurrent state via a non-parametric outer-product mechanism, significantly increasing memory capacity without extra parameters and enabling hardware-efficient training via linear attention chunkwise form.

## Key claims (background only)

- HGRN2 introduces an outer-product state expansion that enlarges the recurrent state from size d to d×d without additional parameters, providing a linear attention interpretation that enables hardware-efficient chunkwise training.
- HGRN2 consistently outperforms HGRN1 and is "highly competitive compared to other subquadratic efficient models" including Mamba and GLA on language modeling benchmarks.
- No TSF evaluation reported; all benchmarks are language modeling (Wikitext-103, large-scale SlimPajama experiments).

## Relevance to P1

Background: establishes HGRN2 as an improved gated linear RNN with expanded state capacity. P1 uses a compact MLP/linear backbone rather than HGRN2 due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
