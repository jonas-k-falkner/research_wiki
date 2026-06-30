---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: high
updated: 2026-06-29
sources:
- src-2026-06-sen-global-local-forecasting
tags:
- global-forecasting
- local-forecasting
- matrix-factorization
- temporal-convolution
- timeseries-forecasting
zotero: senThinkGloballyAct2019
source_hash: 257bffdc84a828a1369e998b92ec669ef741d7cccda8dbfb74f7b8da19a6909a
---

# Source: Think Globally, Act Locally: A Deep Neural Network Approach to High-Dimensional Time Series Forecasting (NeurIPS 2019)

## Metadata

- **Citekey:** `senThinkGloballyAct2019`
- **Authors:** Rajat Sen, Hsiang-Fu Yu, Inderjit Dhillon
- **Venue:** NeurIPS 2019 (Amazon / UT Austin)
- **Relevant projects:** P1

## One-line takeaway

DeepGLO — a hybrid global (matrix factorization regularized by TCN) + local (per-series TCN) model — outperforms purely global or purely local models by >25% WAPE on Wikipedia traffic data with 115K series, directly demonstrating the value of global pattern capture combined with local calibration.

## Key claims

| Claim | Evidence / rationale | Applicability | Confidence |
|---|---|---|---|
| Hybrid global+local model (DeepGLO) outperforms both global-only (TRMF, SVD+TCN) and local-only (LSTM, DeepAR, TCN) models on large-scale multi-series forecasting | Table 2: DeepGLO in top-2 on electricity (370 series), traffic (963 series), and wiki (115K series) datasets | Most relevant for P1's regime: many correlated series, shared global patterns | high |
| The global component (matrix factorization + TCN) extracts k basis time series from n total, where k << n, capturing shared temporal patterns across all series | Method Section 5.1; basis series are visualized in Fig 2a; low-rank factorization assumption | The basis series are the "global model" analog — effectively cluster-level patterns | high |
| Combining global predictions as covariates for a local TCN captures per-series idiosyncrasies without sacrificing global pattern knowledge | Method Section 5.2 (DeepGLO architecture); both local and global components trained jointly | This is the "global model + local residual" design pattern that P1's cluster-then-forecast mirrors | high |
| LeveledInit (initializing TCN weights so initial prediction = window mean) enables training on unnormalized data with wide scale variation | Section 4; enables training without per-series normalization | Directly relevant for P1's SKU data which has wide demand scale variation across SKUs | medium |
| Per-series local models (LSTM, DeepAR, TCN without global features) underperform on unnormalized/diverse datasets — normalization is critical if using pure local models | Table 2: LSTM/DeepAR WAPE degrades substantially without normalization | Supports P1's design choice: use a global cluster model rather than per-series models | high |

## Limitations & caveats

- DeepGLO is NOT a cluster-based model — it uses matrix factorization (all series contribute linearly to all basis series). This is different from hard cluster assignment.
- The global component is trained jointly with the local component — the basis series are learned, not pre-defined clusters.
- Wiki dataset is web traffic (page views), not retail demand; demand patterns may differ.
- The paper predates the CCM/DUET generation of channel clustering methods; it does not address inter-channel relationships within a single multivariate series.

## Decision impact for P1

- **Directly addresses the "global model over clustered series vs. per-series models" debate**: DeepGLO shows global+local hybrid beats both extremes on high-dimensional (115K series) data.
- The key insight is that a global model capturing shared patterns + local calibration per series is the dominant design — P1's cluster model is the global component, with a cluster-level backbone + any per-series fold-in being the local component.
- Scale variation across SKUs (e.g., 1 unit/week vs 10K units/week) is a known problem; LeveledInit or instance normalization (RevIN) are the standard remedies.
- The matrix factorization approach provides a direct interpretation: k clusters correspond to k basis series. P1's cluster count is thus bounded by the intrinsic rank of the demand matrix.

## Updated pages

- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
