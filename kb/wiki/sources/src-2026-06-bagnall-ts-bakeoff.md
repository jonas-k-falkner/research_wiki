---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-bagnall-ts-bakeoff
tags:
- classification
- benchmark
- timeseries
- survey
zotero: bagnallGreatTimeSeries2017
source_hash: d7630b9a131c3037e4ccc5f5c7d01902da28aae7a3c4cdafb79c92bbb14905ba
---

# Source: The Great Time Series Classification Bake Off (2017)

## Metadata

- **Citekey:** `bagnallGreatTimeSeries2017`
- **Authors:** Anthony Bagnall, Jason Lines, Aaron Bostrom, James Large, Eamonn Keogh
- **Venue:** Data Mining and Knowledge Discovery, 2017
- **Relevant projects:** P1

## One-line takeaway

Comprehensive benchmark of 18 TS classifiers on 85 UCR datasets; ensemble methods (COTE) dominate, and 1-NN-DTW remains a strong baseline — simple distance-based methods often outperform complex models on short series.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Ensemble approaches (COTE) significantly outperform individual classifiers, including 1-NN-DTW, on the majority of UCR datasets | Large-scale empirical study; statistical significance tested | Classification benchmarks only; not directly applicable to clustering for P1 | medium |
| 1-NN-DTW is the most robust single-algorithm baseline for TS classification | Comparison across 85 datasets; DTW with learned warping window is competitive across diverse domains | Sets a lower bound for routing quality comparison | medium |
| No single algorithm dominates across all dataset types; the best method depends on data characteristics | Empirical finding across 85 datasets | P1 should evaluate multiple clustering criteria on its own demand data rather than assuming DTW is optimal | medium |

## Limitations & caveats

- The bake-off focuses on classification (labelled data), not clustering or forecasting — results don't directly transfer to P1.
- UCR datasets are short, clean, and labelled; retail demand data is longer, noisier, and unlabelled.
- The paper predates deep learning classifiers (InceptionTime, ResNet) which have since surpassed COTE on many datasets.

## Decision impact for P1

- Sets baseline expectations for routing accuracy: if P1's routing (cluster assignment) is treated as classification, it should at minimum match 1-NN-DTW performance.
- The ensemble finding suggests P1 might benefit from combining multiple clustering signals (shape + regime + frequency) rather than relying on a single distance metric.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
