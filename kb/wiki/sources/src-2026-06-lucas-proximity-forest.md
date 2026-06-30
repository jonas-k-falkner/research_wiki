---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-29
sources:
- src-2026-06-lucas-proximity-forest
tags:
- classification
- proximity-forest
- ensemble
- timeseries
zotero: lucasProximityForestEffective2019
source_hash: 941e4828130da6190ab7010e503a681b41eb3ef4e3048c3be6409aab8ba0b3a2
---

# Source: Proximity Forest: An Effective and Scalable Distance-Based Classifier for Time Series (2019)

## Metadata

- **Citekey:** `lucasProximityForestEffective2019`
- **Authors:** Benjamin Lucas, Ahmed Shifaz, Charlotte Pelletier, Lachlan O'Neill, Nayyar Zaidi, Bart Goethals, François Petitjean, Geoffrey I. Webb
- **Venue:** Data Mining and Knowledge Discovery, 2019
- **Relevant projects:** P1

## One-line takeaway

Proximity Forest — a random forest of elastic distance classifiers — achieves SOTA TS classification accuracy via an ensemble of diverse distance measures while scaling to large datasets.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| An ensemble of diverse distance measures (DTW, ERP, LCSS, TWE, MSM, etc.) significantly outperforms any single distance measure for TS classification | Empirical results on UCR archive; Proximity Forest outperforms COTE on many datasets | Suggests P1 routing should consider combining multiple distance signals | medium |
| Random selection of distance measure + hyperparameter at each split enables scalability while maintaining diversity | Core design; scales to large datasets unlike exact TS methods | Ensemble distance routing could work for P1 if computational budget allows | low |
| Scalable to millions of instances through random selection; avoids O(n²) distance matrix computation | Architecture design | Relevant for P1's millions-of-SKUs scale | medium |

## Limitations & caveats

- Classification (labelled data) context; routing in P1 is unlabelled clustering.
- Ensemble adds complexity; for P1 production routing, a single fast distance (Euclidean + FAISS) is likely preferred.

## Decision impact for P1

- Low direct impact. Confirms ensemble distances outperform single distance for routing accuracy. For P1, this could inform offline cluster validation: compare cluster stability across multiple distance measures.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
