---
type: domain
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-p2-causal-embedding-model
- src-2026-06-p1-cluster-pretrained-deep-models
- src-2026-06-eldele-ts-tcc
- src-2026-06-yue-ts2vec
- src-2026-06-li-ti-mae
- src-2026-06-cheng-timemae
- src-2026-06-foumani-series2vec
- src-2026-06-choi-multitask-ssl
- src-2026-06-eldele-ca-tcc
- src-2026-06-eldele-label-efficient-review
- src-2026-06-jawed-ssl-semisupervised
- src-2026-06-yang-timeclr
- src-2026-06-fraikin-trep
- src-2026-06-talukder-totem
- src-2026-06-he-moco
- src-2026-06-kazemi-time2vec
- src-2026-06-musgrave-metric-learning-reality
- src-2026-06-liu-ssl-comparison
- src-2026-06-beck-xlstm
- src-2026-06-embedding-model-v1
tags:
- thesis
- embeddings
- ssl
---

# Domain thesis: Embedding models

## Current thesis

The strategic embedding opportunity is to move from symmetric shape similarity toward directed, query-dependent covariate influence. P2 aims to make causal covariate discovery approximately retrievable rather than explicitly quadratic.

## Main research question

Can an asymmetric embedding objective distilled from Transfer Entropy or Granger-style labels recover useful directed covariates at scale, and does this improve downstream forecasting or scenario quality?

## Evaluation hierarchy

1. Directional retrieval metrics against held-out TE/Granger-style labels.
2. Robustness across regimes and horizons.
3. Downstream forecast lift in P1-like cluster models.
4. Explanation usefulness in P3/P4-style decision surfaces.

## Caveat

P2 should be treated as causal-candidate retrieval, not proof of causal effect. Claims need validation through forecasting lift, robustness checks, and where possible intervention-like tests.

## SSL landscape (confirmed 2026-06-30)

Primary literature pass on 4 SSL TS papers confirms the thesis gap: no published method implements an asymmetric/directed objective. The SOTA symmetric encoders are:
- **TimeMAE** (Cheng et al. 2023, TKDE) — decoupled MAE with window slicing; 91.31% linear eval on HAR; strongest classification encoder
- **TS2Vec** (Yue et al. 2022, AAAI) — hierarchical contrastive; SOTA across 8 tasks including forecasting; most universal baseline
- **Ti-MAE** (Li et al. 2023) — masked autoencoder; best SSL forecasting 2023; alleviates distribution shift
- **TS-TCC** (Eldele et al. 2021) — temporal + contextual contrasting; semi-supervised efficiency (10% labels ≈ 100% supervised)

All four are symmetric. P2's asymmetric objective is a confirmed research gap as of 2024.

## SSL landscape — MEDIUM papers (I-P2-A ingest, 2026-06-30)

8 additional SSL papers surveyed; all symmetric. Notable additions:
- **T-Rep** (Fraikin et al. 2024, ICLR): first SSL TS method with learned time-embeddings in pretext tasks; replaces binary contrastive signal with continuous JSD divergence target; outperforms TS2Vec; robust to missing data.
- **Series2Vec** (Foumani et al. 2024): similarity-preserving pretext (Soft-DTW) avoids augmentation corruption; outperforms prior SSL methods on UCR/UEA.
- **CA-TCC** (Eldele et al. 2023, TPAMI): semi-supervised 4-phase pipeline; 1% labels ≈ fully supervised on HAR.
- **TOTEM** (Talukder et al. 2024, ICML): VQVAE tokenizer; zero-shot 80% AvgWins across 5 unseen domains.
- Survey (Eldele 2024): P2's training scenario sits in in-domain semi-supervised quadrant — not cross-domain transfer.

All 12 SSL papers reviewed confirm: no asymmetric/directed TS SSL objective exists in published literature.

## Architecture & training inputs (ingest 2026-06-30)

Four additional high-priority papers close key design questions:
- **MoCo** ([src-2026-06-he-moco](../../sources/src-2026-06-he-moco.md), He et al. 2020): momentum encoder (EMA) + 65k-entry queue is the standard training mechanism for all TS contrastive methods. P2 adopts: EMA encoder for source branch, gradient-updated for target; queue-based negatives for sparse positive regime.
- **Time2Vec** ([src-2026-06-kazemi-time2vec](../../sources/src-2026-06-kazemi-time2vec.md), Kazemi et al. 2019): learnable sinusoidal time embeddings foundational to T-Rep. P2 should condition directed pretext on t2v(timestamp) for regime-aware label quality.
- **Liu SSL comparison** ([src-2026-06-liu-ssl-comparison](../../sources/src-2026-06-liu-ssl-comparison.md), 2024): MAE backbone preferred over SimCLR at sparse label ratio (< 0.1) — matches P2's TE/Granger annotation budget.
- **Musgrave** ([src-2026-06-musgrave-metric-learning-reality](../../sources/src-2026-06-musgrave-metric-learning-reality.md), 2020): fair evaluation protocol — equal architecture/dimensions/augmentations + Bayesian cross-val hyperparameter tuning required; MAP@R as primary metric.
- **xLSTM mLSTM** ([src-2026-06-beck-xlstm](../../sources/src-2026-06-beck-xlstm.md), 2024): matrix memory C ∈ ℝ^{d×d} proves asymmetric key–value geometries converge end-to-end — validates P2's feasibility premise.

## V1 production baseline (I-P2-v1, 2026-06-30)

The production v1 model is the concrete starting point for P2 research. See [sources/src-2026-06-embedding-model-v1](../../sources/src-2026-06-embedding-model-v1.md) for full details.

**Architecture summary:**
- `SSLModel` (`src/core_model/model.py`): encoder + decoder + 3 SSL heads
- `ConvAttnEncoder`: TCN → multi-head attention → meanmax pooling → 128-dim `z` (retrieval) + `z_seq` (sequential)
- `RNNAttnDecoder`: sLSTM + cross-attention; only active during training (GL head)
- INPUT_DIM=1, HIDDEN_DIM=128, EMB_DIM=128, MAX_SEQ_LEN=180

**Default training regime:** SL (Soft-DTW, weight 0.7) + GL (masked MSE, weight 0.3); CL off.

**Production KPIs:** MAP@50 > 0.95, combined_rank_score > 0.925, reconstruction_error < 0.31.

**P2 implication:** V1's SL head (Soft-DTW) is symmetric by construction. P2's research question is whether replacing this head's distance function with TE/Granger-derived asymmetric targets produces a stable directed geometry while keeping the backbone and KPIs intact.

## Sources & related

- [sources/src-2026-06-p2-causal-embedding-model](../../sources/src-2026-06-p2-causal-embedding-model.md), [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md)
- [sources/src-2026-06-cheng-timemae](../../sources/src-2026-06-cheng-timemae.md), [sources/src-2026-06-yue-ts2vec](../../sources/src-2026-06-yue-ts2vec.md), [sources/src-2026-06-li-ti-mae](../../sources/src-2026-06-li-ti-mae.md), [sources/src-2026-06-eldele-ts-tcc](../../sources/src-2026-06-eldele-ts-tcc.md)
- [sources/src-2026-06-fraikin-trep](../../sources/src-2026-06-fraikin-trep.md), [sources/src-2026-06-foumani-series2vec](../../sources/src-2026-06-foumani-series2vec.md), [sources/src-2026-06-talukder-totem](../../sources/src-2026-06-talukder-totem.md), [sources/src-2026-06-eldele-ca-tcc](../../sources/src-2026-06-eldele-ca-tcc.md)
- [sources/src-2026-06-he-moco](../../sources/src-2026-06-he-moco.md), [sources/src-2026-06-kazemi-time2vec](../../sources/src-2026-06-kazemi-time2vec.md), [sources/src-2026-06-musgrave-metric-learning-reality](../../sources/src-2026-06-musgrave-metric-learning-reality.md), [sources/src-2026-06-liu-ssl-comparison](../../sources/src-2026-06-liu-ssl-comparison.md), [sources/src-2026-06-beck-xlstm](../../sources/src-2026-06-beck-xlstm.md)
- [sources/src-2026-06-embedding-model-v1](../../sources/src-2026-06-embedding-model-v1.md) — v1 production baseline; ConvAttnEncoder + SSL heads + KPIs
- Project: [projects/p2-causal-embedding-v2](../../projects/p2-causal-embedding-v2.md)
