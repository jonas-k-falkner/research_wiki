---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-aghabozorgi-ts-clustering-survey
tags:
- clustering
- timeseries-clustering
- survey
- distance-measures
- cluster-evaluation
zotero: aghabozorgiTimeseriesClusteringDecade2015
source_hash: 06d218648da255764fffea03e08554dc32dc8e4f7e7ac187ad42efbf0e0bd1ea
---

# Source: Time-Series Clustering — A Decade Review (2015)

## Metadata

- **Citekey:** `aghabozorgiTimeseriesClusteringDecade2015`
- **Authors:** Saeed Aghabozorgi, Ali Seyed Shirkhorshidi, Teh Ying Wah
- **Venue:** Information Systems, Elsevier, 2015 (University of Malaya)
- **Relevant projects:** P1

## One-line takeaway

Comprehensive taxonomy of TS clustering covering representation methods, distance measures, prototype definitions, and cluster evaluation metrics; the main finding is that DTW and Euclidean distance are the most practical similarity measures, silhouette/SSE are the standard internal quality metrics, and no single approach dominates across all settings.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Three types of TS similarity exist and require different distance measures: similarity in time (Euclidean, correlation), similarity in shape (DTW, LCSS), and structural similarity / regime (ARMA, HMM) | Taxonomy in Section 3.1–3.3 | P1 must decide which axis to cluster on — shape vs. regime vs. correlation | high |
| DTW is the most accurate shape-based distance measure in most applications, but computationally expensive (O(n²)) | Literature review Section 3.4; multiple comparative studies cited | DTW appropriate for P1 offline clustering; too slow for real-time routing | high |
| Euclidean distance is competitive for classification accuracy (Keogh & Kasetty 2003) and is far faster | Section 3.4 citing [145]; "Euclidean distance is surprisingly competitive" | Use Euclidean for routing/serving; use DTW for offline cluster formation | medium |
| Standard internal cluster quality metrics for TS: SSE (within-cluster sum of squares), Silhouette index, Davies-Bouldin, Calinski-Harabasz, and Dunn index | Section 6.2 | For P1's cluster quality gate experiment, SSE and silhouette are the canonical internal metrics | high |
| Shape-level similarity (DTW, Euclidean) is appropriate for short to medium length time series; structural/regime similarity (ARMA/HMM-based) is appropriate for long series | Section 3.2 vs 3.3; distinction between shape-level and structure-level | P1's SKU demand windows (~1–4 weeks) are short: shape-based clustering is appropriate | medium |
| Cluster prototype quality significantly affects clustering convergence and accuracy; local search prototype > averaging > medoid in quality | Section 4.4 citing Hautamaki et al. | For P1's cluster prototypes (used for FAISS routing), accuracy of prototype matters — medoid is fastest but lowest quality | medium |
| Subsequence clustering (clustering windows of a single series) is deemed "meaningless" by Keogh & Lin | Section 1.3 citing [242] | P1 should cluster whole series (one series = one SKU), not subsequences | high |

## Limitations & caveats

- Survey covers pre-2015 literature; does not cover deep learning clustering, learned embeddings, or neural TS clustering (CCM, DUET, etc.).
- Evaluation recommendations are based on datasets with ground truth labels; many real P1 SKU datasets lack ground truth cluster assignments.
- No coverage of high-dimensional multivariate settings or channel clustering (the survey focuses on whole time-series clustering).
- Model-based (ARMA, HMM) clustering has scalability problems noted in the survey; not practical for millions of SKUs.

## Decision impact for P1

- Confirms that SSE and silhouette are the right internal metrics for P1's cluster quality gate experiment.
- Establishes that shape-based clustering (Euclidean/DTW) is appropriate for P1's short-window SKU demand data.
- Warns against subsequence clustering — P1 should cluster whole series per SKU, not sliding windows.
- Medoid is the fastest prototype; local search gives better prototype quality but at higher cost. P1 should test both.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
