---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-30
sources:
- src-2026-06-tan-ts-indexing
tags:
- indexing
- scalability
- classification
- dtw
zotero: tanIndexingClassifyingGigabytes2017
source_hash: cadce636a794ab41d2a2d7568d71544b5380e9987b79feea7bd85c6eed547127
---

# Source: Indexing and Classifying Gigabytes of Time Series under Time Warping (2017)

## Metadata
- **Citekey:** `tanIndexingClassifyingGigabytes2017`
- **Authors:** Tan, Webb, Petitjean (Monash University)
- **Venue:** SDM 2017
- **Relevant projects:** P1 (cluster routing at scale), P2 (embedding index)

## One-line takeaway

TSI (Time Series Indexing) combines hierarchical K-means clustering with DTW lower-bounding to classify 100M+ time series orders-of-magnitude faster than NN-DTW, enabling contract-time classification on satellite-scale datasets.

## Key claims

- **Motivation:** NN-DTW is the SOTA accuracy method for TS classification, but has O(N·L) complexity per query. At N = 1M training examples and a 100M test set (Sentinel-2 satellite), NN-DTW would take ~30,000 years.
- **TSI algorithm:** builds a hierarchical K-means tree over the training set; at query time, traverses the tree using DTW lower-bounds (LB_Keogh) to prune branches before full DTW computation; returns the nearest neighbor in contracted time.
- **Results:** TSI achieves NN-DTW-comparable accuracy while being orders of magnitude faster. On satellite datasets (100M+ series), TSI is the only feasible approach.
- DTW is not a metric (no triangle inequality), making standard metric-index structures (k-d tree, ball tree) inapplicable. TSI's K-means + LB_Keogh combination is specifically designed for the DTW space.

## Relevance to P1

At P1 scale (millions of commodity price series routed to clusters), the cluster routing step needs a scalable nearest-neighbor or centroid-assignment algorithm in DTW space. TSI's hierarchical K-means tree is directly applicable: build the tree on cluster centroid representatives, then route each new series by tree traversal + LB_Keogh pruning rather than scanning all centroids. This cuts routing latency from O(K·L²) to O(log(K)·L) in practice.

## Relevance to P2

P2 targets a 200M embedding index. TSI confirms the scalability challenge is real: brute-force NN search at 200M scale is infeasible without indexing. P2 should use FAISS (approximate NN) for the learned embedding index (not DTW-based), but TSI validates that hierarchical tree structures over temporal data are tractable and accurate for billion-scale retrieval.
