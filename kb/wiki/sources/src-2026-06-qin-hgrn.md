---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-qin-hgrn
tags:
- ssm
- timeseries-forecasting
- background
zotero: qinHierarchicallyGatedRecurrent2023
source_hash: f293b5dca72cd9be969058308ac2b96b9c2f37bd887c45668c0b802a5d56d655
---

# Source: Hierarchically Gated Recurrent Neural Network for Sequence Modeling (2023)

## Metadata
- **Citekey:** `qinHierarchicallyGatedRecurrent2023`
- **Authors:** Qin, Yang, Zhong
- **Venue:** NeurIPS 2023
- **Relevant projects:** P1 (background)

## One-line takeaway

HGRN introduces hierarchical forget gates with monotonically increasing lower bounds across layers, enabling lower layers to model short-term dependencies and upper layers to model long-term dependencies while retaining efficient linear recurrence.

## Key claims (background only)

- HGRN uses element-wise linear recurrence with data-dependent forget gates bounded below by a per-layer learnable value that increases monotonically toward the top layer, addressing the tension between forgetting short-term noise and retaining long-term context.
- Competitive with Transformers on language modeling, image classification, and Long Range Arena benchmarks, with linear training complexity via parallel scan.
- No TSF evaluation reported; benchmarks are language modeling, image classification (ViT-style), and Long Range Arena.

## Relevance to P1

Background: establishes HGRN as a gated linear RNN with hierarchical inductive bias for sequence modeling. P1 uses a compact MLP/linear backbone rather than HGRN due to interpretability constraints and absence of compelling TSF gains over linear baselines.
