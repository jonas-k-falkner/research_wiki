---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: low
updated: 2026-06-29
sources:
- src-2026-06-patro-simba
tags:
- ssm
- timeseries-forecasting
- background
zotero: patroSiMBASimplifiedMambaBased2024
source_hash: ff87c5fe3c2623cdcd063f777a183b66cb47be077e31e5b7efffbfbcaac87410
---

# Source: SiMBA: Simplified Mamba-Based Architecture for Vision and Multivariate Time Series (2024)

## Metadata
- **Citekey:** `patroSiMBASimplifiedMambaBased2024`
- **Authors:** Patro, Agneeswaran
- **Venue:** arXiv / Microsoft 2024
- **Relevant projects:** P1 (background)

## One-line takeaway

SiMBA addresses Mamba's training instability at scale by combining Mamba for sequence mixing with Einstein FFT (EinFFT) for channel mixing, reporting state-of-the-art SSM results on ImageNet and seven TSF benchmark datasets.

## Key claims (background only)

- SiMBA introduces EinFFT (Einstein FFT) as a stable channel modeling technique that keeps eigenvalues of the state matrix as negative real numbers, fixing Mamba's vanishing/exploding gradient issue when scaled to large vision networks.
- SiMBA is the first SSM to close the performance gap with state-of-the-art attention-based Transformers on ImageNet, and claims competitive TSF performance on seven standard time series datasets.
- Comparison to Transformers on TSF is mixed — SiMBA bridges the gap but does not consistently outperform strong Transformer baselines, and no comparison against DLinear is highlighted.

## Relevance to P1

Background: establishes SiMBA as a stable Mamba variant with EinFFT channel mixing. P1 uses a compact MLP/linear backbone rather than SSMs due to the added complexity of spectral channel mixing and absence of demonstrated TSF accuracy gains over linear baselines in the retail forecasting regime.
