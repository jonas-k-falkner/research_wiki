---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-liu-longhorn
tags:
- ssm
- timeseries-forecasting
- background
zotero: liuLonghornStateSpace2024
source_hash: 6ee83bc94692787369fa0e7856ff5380bca8ea7bcb5857fbd48e35d5103554fd
---

# Source: Longhorn: State Space Models Are Amortized Online Learners (2024)

## Metadata
- **Citekey:** `liuLonghornStateSpace2024`
- **Authors:** Liu, Wang, Wu, Feng, Stone, Liu
- **Venue:** arXiv 2024 (UT Austin)
- **Relevant projects:** P1 (background)

## One-line takeaway

Longhorn reframes SSM design as solving online learning objectives, deriving its state update rule as the closed-form solution to an online associative recall problem, achieving 1.8x better sample efficiency than Mamba at 1.3B parameters without a separately parameterized forget gate.

## Key claims (background only)

- Longhorn derives its recurrent update rule from the implicit closed-form solution to an online associative recall objective, providing a principled design principle for SSMs rather than ad-hoc gating mechanisms — and naturally balancing forgetting and learning without a separate forget gate parameter.
- Longhorn outperforms Mamba on standard sequence modeling benchmarks, language modeling, and vision tasks at 1.3B parameters (100B tokens, SlimPajama), and can extrapolate to 16x longer contexts at inference than its training length.
- No TSF evaluation reported; benchmarks are language modeling and synthetic associative recall tasks.

## Relevance to P1

Background: establishes Longhorn as an SSM designed via online learning principles. P1 uses a compact MLP/linear backbone rather than SSMs due to interpretability constraints and absence of demonstrated TSF gains over linear baselines.
