---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-wang-ts-classification-cnn
tags:
- classification
- cnn
- deep-learning
- timeseries
zotero: wangTimeSeriesClassification2017
source_hash: 1ca6cedaad6f7ebef3db9ba67963ddab2c1148c30c456925f31e5b24f74f50f1
---

# Source: Time Series Classification from Scratch with Deep Neural Networks: A Strong Baseline (2017)

## Metadata

- **Citekey:** `wangTimeSeriesClassification2017`
- **Authors:** Zhiguang Wang, Weizhong Yan, Tim Oates
- **Venue:** IJCNN 2017
- **Relevant projects:** P1

## One-line takeaway

FCN and ResNet achieve competitive TS classification accuracy with minimal feature engineering by applying deep CNNs directly to raw TS data, establishing deep learning baselines that rival traditional distance-based methods.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| FCN (Fully Convolutional Network) and ResNet achieve accuracy competitive with COTE ensemble on UCR benchmarks | Empirical results; FCN wins on ~60% of datasets vs DTW-1NN | Demonstrates deep learning viability for TS classification/routing | medium |
| Raw TS input with global average pooling avoids the need for feature engineering or representation selection | Architecture design | Applicable to P1 routing: no manual feature extraction needed for cluster routing | medium |
| ResNet with skip connections is more robust to vanishing gradients on longer TS | Architecture comparison | For P1 series longer than ~200 time points, ResNet preferred over FCN | low |

## Limitations & caveats

- Classification benchmark context; clustering/routing performance not directly assessed.
- UCR datasets are short and clean; retail demand is noisier and more intermittent.

## Decision impact for P1

- Low direct impact. Establishes that a simple CNN backbone is competitive for TS routing. P1 could use a pretrained FCN/ResNet as the series encoder for FAISS routing.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
