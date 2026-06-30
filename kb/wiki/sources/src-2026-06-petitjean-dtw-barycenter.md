---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-petitjean-dtw-barycenter
tags:
- clustering
- dtw
- averaging
- timeseries
zotero: petitjeanGlobalAveragingMethod2011
source_hash: e244a2a90543f371937a2e50d38e915c1773f78c7472d2463b4f382b4827c5af
---

# Source: A Global Averaging Method for Dynamic Time Warping, with Applications to Clustering (2011)

## Metadata

- **Citekey:** `petitjeanGlobalAveragingMethod2011`
- **Authors:** François Petitjean, Alain Ketterlin, Pierre Ganc̨arski
- **Venue:** Pattern Recognition 44(3), 2011 (University of Strasbourg / CNES)
- **Relevant projects:** P1

## One-line takeaway

DTW Barycenter Averaging (DBA) enables principled global averaging of time series under DTW distance, producing cluster prototypes that outperform pairwise averaging methods and improve k-means clustering quality for TS data.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| DBA (DTW Barycenter Averaging) produces better cluster prototypes than pairwise averaging methods (NLAAF, PSA) by averaging all sequences globally and iteratively | Empirical comparison on UCR datasets; WGSS decreases with DBA vs pairwise methods | When using k-means with DTW distance for TS clustering | high |
| Standard Euclidean averaging of warped time series produces prototypes that do not resemble the original data (spurious peaks/troughs) | Figure 1 in petitjeanFasterMoreAccurate2016 (the companion paper) demonstrates this clearly | Euclidean centroid is inappropriate for k-means with TS when series have temporal shifts | high |
| DBA converges iteratively (analogous to k-means EM steps) and minimises WGSS under DTW | Theoretical analysis Section 4.1; convergence not guaranteed in general but observed empirically | Practical tool for computing cluster prototypes in DTW-based TS clustering | medium |

## Limitations & caveats

- DBA is an O(n × T²) operation per iteration (n series of length T), making it expensive at scale; not suitable for millions of SKUs without approximation.
- Convergence to a global optimum is not guaranteed; result depends on initial average sequence.
- Focused on univariate time series; extension to multivariate TS is non-trivial.

## Decision impact for P1

- If P1 uses DTW-based clustering for offline cluster formation, DBA is the appropriate method for computing cluster prototypes.
- For large-scale P1 (millions of SKUs), DBA is too expensive; use k-medoids or approximate averaging with Euclidean centroid (acceptable for routing if clusters are stable).
- The Euclidean centroid failure mode (spurious peaks) is relevant if P1 visualizes cluster prototypes for analyst review — use DBA or medoid for interpretable prototypes.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
