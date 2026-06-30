---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-keogh-parameter-free-ts
tags:
- clustering
- parameter-free
- timeseries
- data-mining
zotero: keoghParameterfreeDataMining2004
source_hash: a00ce1b38962ffdf4a0719c6c253ccab432a723c9ed735a3c4b2fefe41a53bbb
---

# Source: Towards Parameter-Free Data Mining (KDD 2004)

## Metadata

- **Citekey:** `keoghParameterfreeDataMining2004`
- **Authors:** Eamonn Keogh, Stefano Lonardi, Chotirat Ratanamahatana
- **Venue:** KDD 2004 (UC Riverside)
- **Relevant projects:** P1

## One-line takeaway

Compression-based dissimilarity measure (CDM) enables parameter-free TS clustering using Kolmogorov complexity — avoids the need to tune distance measure parameters at the cost of some accuracy.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| CDM (Compression-based Dissimilarity Measure) provides a parameter-free distance measure for TS clustering by approximating Kolmogorov complexity via compression | Empirical demonstration on clustering and classification tasks | Useful when domain-specific distance tuning is infeasible; P1 likely has enough data to tune DTW | low |
| Parameter-free clustering avoids selecting DTW warping window size — a key hyperparameter that significantly affects DTW quality | Motivation; tuning warping window is non-trivial on new datasets | Relevant for P1 cold-start on new product categories with no historical data | medium |
| CDM clustering accuracy is below DTW on some datasets but requires zero tuning | Comparison in paper | For P1 production clustering, parameterized DTW with cross-validation is preferred when data is available | medium |

## Limitations & caveats

- CDM is slower than DTW in practice; the "parameter-free" benefit comes at computational cost.
- Accuracy below tuned DTW; not recommended for production if data volume allows parameter tuning.

## Decision impact for P1

- Low direct impact. Consider CDM only for P1 cold-start scenarios where no historical data is available to tune DTW window size.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
