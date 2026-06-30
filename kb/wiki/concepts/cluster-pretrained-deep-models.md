---
type: concept
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-tsf-literature-review
- src-2026-06-chen-channel-clustering
- src-2026-06-qiu-duet-clustering
- src-2026-06-aghabozorgi-ts-clustering-survey
- src-2026-06-petitjean-dtw-barycenter
- src-2026-06-petitjean-faster-dtw
- src-2026-06-bagnall-ts-bakeoff
- src-2026-06-sen-global-local-forecasting
- src-2026-06-ruta-sax-navigator
- src-2026-06-keogh-parameter-free-ts
- src-2026-06-lucas-proximity-forest
- src-2026-06-wang-ts-classification-cnn
- src-2026-06-ismail-benchmarking-dl-ts
tags:
- concept
---

# Cluster-pretrained deep models

## Definition

A forecasting family where similar time series are grouped into clusters, each cluster has a lightweight deep model trained on its members, and a new series is embedded and routed (FAISS) to the matching cluster model for zero-shot or minimal-fold-in forecasting. See [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md).

## Why it matters

It reframes SKU onboarding from per-series analyst tuning into a routing problem, which is the P1 scalability thesis. The load-bearing assumption is that a single shared model can serve a cluster without underfitting mixed regimes — now partially validated by primary literature (see below).

## Primary literature findings

### 1. Does channel clustering improve forecasting accuracy? (Research question 1)

**Yes — directly confirmed by two NeurIPS/KDD 2024–2025 primary experiments.**

[Chen et al. (NeurIPS 2024)](../sources/src-2026-06-chen-channel-clustering.md) — CCM (Channel Clustering Module) — shows a +2.4% average MSE improvement on long-term and +7.2% on short-term forecasting across 9 multivariate benchmark datasets versus base models (TSMixer, DLinear, PatchTST, TimesNet). The module improves performance in 90.3% of test configurations.

[Qiu et al. (KDD 2025)](../sources/src-2026-06-qiu-duet-clustering.md) — DUET — extends this to 25 datasets across 10 domains and achieves 7.1% MSE reduction over the prior state-of-the-art. Both TCM (temporal clustering) and CCM (channel clustering) components contribute independently (ablation Table 2).

**Clustering criterion used (Research question 1 continued):** Both papers use learned similarity, not regime labels:
- CCM (Chen et al.) uses a radial basis function (RBF) kernel on standardized time series values — shape/correlation-based. The ClusterLoss maximises intra-cluster similarity and minimises inter-cluster overlap.
- DUET (Qiu et al.) uses a learnable Mahalanobis distance in frequency (FFT amplitude) space — spectral correlation-based. Neither paper clusters by regime label, seasonality type, or stationarity directly.

**Caveat:** All experiments use standard academic benchmarks (ETT, Weather, Traffic, Electricity, M4). No retail demand or e-commerce SKU datasets are included. The magnitude of gain on P1's data is unknown.

### 2. What does DUET add over CCM? (Research question 2)

| Feature | CCM (Chen 2024) | DUET (Qiu 2025) |
|---|---|---|
| Channel clustering | Hard soft-assignment (Bernoulli via Gumbel-softmax) | Soft mask matrix via learnable Mahalanobis distance in freq domain |
| Temporal clustering | None | TCM: MoE-style router over M linear pattern extractors per distribution |
| Routing mechanism | Cluster-aware Feed Forward (cluster identity replaces channel identity) | Fusion Module: masked cross-channel attention using channel mask M |
| Zero-shot capability | Yes: prototype embeddings enable routing of unseen channels | No: no prototype mechanism; cold-start channels not handled |
| Cluster-level attribution | Partial: ClusterLoss is auxiliary; cluster visualization via t-SNE | Channel mask M is interpretable; Fig 7 shows per-channel soft groupings |

**Key design difference:** DUET separates clustering from routing explicitly. The CCM outputs a mask matrix M that is used in a subsequent masked attention module — the clustering informs attention but the model backbone still runs over all channels. CCM (Chen) assigns cluster-aware weights directly to the feed-forward layer, replacing channel identity with cluster identity.

DUET does NOT provide zero-shot routing to unseen series — this is a gap relative to CCM and relative to P1's requirements.

### 3. Shape similarity vs. regime consistency (Research question 3)

The literature does not directly answer whether shape clusters reliably capture stationary/seasonal regimes. What can be said from primary sources:

- [Aghabozorgi et al. (2015)](../sources/src-2026-06-aghabozorgi-ts-clustering-survey.md) distinguishes three similarity types: **similarity in time** (correlation/Euclidean), **similarity in shape** (DTW, LCSS), and **structural similarity** (ARMA, HMM — captures regime). Shape-based and structural similarity are distinct objectives; shape clusters do not guarantee regime consistency.
- DUET's TCM clusters by temporal distribution (latent normal distribution parameters), not by shape — this is closer to regime clustering than CCM's shape-based approach. The ablation shows TCM provides larger gains on ETTh2 (high distribution shift) than on Traffic (lower distribution shift), consistent with regime-change sensitivity.
- Neither CCM nor DUET validates whether shape clusters are regime-consistent. P1's exp-p1-cluster-quality-gate experiment should measure this directly on its own data.

**Interim assessment:** Shape clusters likely capture correlation structure and dominant periodicity but may split or merge differently from regime-consistent clusters. Regime sub-clustering is the P1 experiment that remains open.

### 4. Cluster quality metrics for time series (Research question 4)

[Aghabozorgi et al. (2015)](../sources/src-2026-06-aghabozorgi-ts-clustering-survey.md) provides the authoritative review:

- **Internal metrics** (no ground truth needed): Sum of Squared Error (SSE / within-cluster variance), Silhouette index, Davies-Bouldin index, Calinski-Harabasz index, Dunn index.
- **External metrics** (ground truth required): Rand Index, Adjusted Rand Index, F-measure, NMI, Purity.
- For P1: SSE and Silhouette are the canonical internal metrics. Silhouette is preferred for comparing across different K values. Neither is DTW-aware in standard implementations — compute with the same distance used for clustering.
- No DTW-specific cluster quality metric is recommended in the literature as a standard; DTW silhouette is computationally expensive but feasible at P1's cluster-count scale.

[Petitjean et al. (2011)](../sources/src-2026-06-petitjean-dtw-barycenter.md) uses WGSS (Within Group Sum of Squares = SSE under DTW) as the primary cluster quality measure during DBA optimization — this is the DTW-native analog of SSE.

### 5. Global model over clustered series vs. per-series models (Research question 5)

[Sen et al. (NeurIPS 2019)](../sources/src-2026-06-sen-global-local-forecasting.md) — DeepGLO — directly and conclusively answers this for a 115K-series dataset (Wikipedia traffic):

**Hybrid global + local model wins over both extremes.** Global-only (matrix factorization + TCN) beats per-series local models at scale; but adding a per-series local TCN that takes global predictions as covariates improves further. The global model captures shared temporal patterns (basis series); the local model captures per-series idiosyncrasies.

The key insight for P1: the cluster model is the global component; any series-specific fold-in (few-shot fine-tuning) is the local component. The literature supports not using pure per-series models at P1's SKU scale.

**Caveat:** DeepGLO uses matrix factorization (all series contribute linearly to all basis series), not hard cluster assignment — its global model is equivalent to continuous clustering. Hard cluster assignment may be a constrained version that loses some global generalization.

## Open research questions

- Is shape-based clustering (CCM-style) sufficient for P1's demand data, or is regime sub-clustering (TCM-style) also required? → [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
- What backbone — D-Linear vs MLP vs small foundation-model-style architecture — and does the choice interact with cluster granularity?
- Does CCM's zero-shot prototype routing meet P1's new-SKU onboarding latency requirements?
- What is the right cluster count K for P1's demand data? (CCM ablation suggests K = 0.2–0.6 × channel count; DeepGLO's rank k suggests k is the intrinsic dimensionality of the demand matrix.)
- How do clusters degrade over time as demand patterns shift seasonally or due to external events?

## Literature findings summary

| Paper | Venue | Key finding for P1 |
|---|---|---|
| Chen et al. (CCM) | NeurIPS 2024 | Shape-based channel clustering +2.4–7.2% accuracy; prototype-based zero-shot routing | high confidence |
| Qiu et al. (DUET) | KDD 2025 | Dual clustering (temporal + channel) +7.1% over SOTA; soft channel mask; no zero-shot | high confidence |
| Aghabozorgi et al. | Inf. Systems 2015 | SSE and Silhouette are canonical internal metrics; DTW most accurate shape distance | high confidence |
| Sen et al. (DeepGLO) | NeurIPS 2019 | Global+local hybrid > global-only or per-series models on 115K series | high confidence |
| Petitjean et al. (DBA) | Pattern Recog. 2011 | DBA is the correct DTW-consistent averaging method for cluster prototypes | high confidence |
| Petitjean et al. (NCC-DTW) | IEEE TKDE 2016 | DBA centroids achieve NN-DTW accuracy at 100x speedup for routing | high confidence |
| Bagnall et al. (Bake-off) | DAMI 2017 | Ensemble distances > single distance for TS classification/routing | medium confidence |

## Cross-project relevance

- Consumes covariate selection from [concepts/hierarchical-entmax-covariate-selection](hierarchical-entmax-covariate-selection.md) and, later, embeddings from [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md).

## Related pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md)
