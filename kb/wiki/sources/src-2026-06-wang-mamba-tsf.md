---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-wang-mamba-tsf
tags:
- ssm
- timeseries-forecasting
- background
zotero: wangMambaEffectiveTime2024
source_hash: 11f25c26b33a50455c835cd4062d9314b417716c8a6d35356249efa56d230751
---

# Source: Is Mamba Effective for Time Series Forecasting? (2024)

## Metadata
- **Citekey:** `wangMambaEffectiveTime2024`
- **Authors:** Wang, Kong, Feng, Wang, Yang, Zhao, Wang, Zhang
- **Venue:** arXiv / Northeastern University 2024
- **Relevant projects:** P1 (background)

## One-line takeaway

S-Mamba, a bidirectional Mamba model for inter-variate correlation encoding, achieves competitive TSF performance on high-variate periodic datasets but shows suboptimal results on low-variate aperiodic datasets (ETT, Exchange) where DLinear is competitive or better.

## Key claims (background only)

- S-Mamba uses a bidirectional Mamba block for inter-variate correlation (VC) encoding and a Feed-Forward Network for temporal dependency (TD) encoding, evaluated on 13 datasets including ETT, Weather, Traffic, and Electricity.
- On aperiodic low-variate datasets (ETTh1, ETTh2, ETTm1, ETTm2, Exchange), S-Mamba "does not demonstrate a pronounced superiority in performance; indeed, it exhibits a suboptimal outcome" — DLinear is competitive in these regimes.
- On high-variate periodic datasets (Traffic, Electricity, PEMS, Solar-Energy), S-Mamba achieves leading MSE, but the advantage is attributed to the bidirectional Mamba VC encoding rather than to SSM temporal modeling per se.

## Relevance to P1

Background: the most relevant SSM TSF evaluation paper; shows Mamba-based models offer no clear advantage over DLinear on the ETT/Exchange benchmarks most analogous to retail SKU forecasting (low-variate, aperiodic). P1 uses a compact MLP/linear backbone rather than SSMs given this evidence and the additional interpretability constraint on hidden states.
