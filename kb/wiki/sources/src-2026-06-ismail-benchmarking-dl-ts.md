---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-ismail-benchmarking-dl-ts
tags:
- classification
- benchmark
- deep-learning
- timeseries
zotero: ismailBenchmarkingDeepLearning
source_hash: 606889442710cce9ef0590819ba36c15448e8555b54202b4f00fe4367bbc6b95
---

# Source: Benchmarking Deep Learning Interpretability in Time Series Predictions (Ismail Fawaz et al.)

## Metadata

- **Citekey:** `ismailBenchmarkingDeepLearning`
- **Authors:** Hassan Ismail Fawaz et al.
- **Venue:** NeurIPS (date from citekey context)
- **Relevant projects:** P1

## One-line takeaway

Systematic benchmark of deep learning methods for TS classification finds InceptionTime is the most accurate overall deep architecture, while interpretability (CAM-based attribution) can identify which time-steps drive predictions.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| InceptionTime (inception-style multi-scale CNN) achieves the best overall deep learning accuracy on UCR TS classification benchmarks | Large-scale empirical comparison; statistically significant | Useful for P1: if deep routing is used, InceptionTime is the recommended architecture | medium |
| Class Activation Maps (CAM) provide time-step attribution for CNN TS classifiers, enabling interpretability | Demonstration on multiple datasets | P1 could use CAM to explain which time-steps determined cluster routing for an SKU | low |
| Deep learning for TS classification has converged: ensemble of deep networks (similar to HIVE-COTE) needed for marginal gains over strong individual models | Meta-finding | P1 should not over-invest in architecture search; use InceptionTime/ResNet as baseline | medium |

## Limitations & caveats

- Classification (labelled) benchmark; not directly applicable to P1's unlabelled clustering.
- Interpretability results are on short UCR series; applicability to long, intermittent retail demand is uncertain.

## Decision impact for P1

- Low direct impact. If P1 uses deep learning routing, InceptionTime is the recommended encoder architecture. CAM-based attribution could be used to explain cluster routing decisions to analysts.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
