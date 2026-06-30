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

## Sources & related

- [sources/src-2026-06-p2-causal-embedding-model](../../sources/src-2026-06-p2-causal-embedding-model.md), [sources/src-2026-06-p1-cluster-pretrained-deep-models](../../sources/src-2026-06-p1-cluster-pretrained-deep-models.md)
- [sources/src-2026-06-cheng-timemae](../../sources/src-2026-06-cheng-timemae.md), [sources/src-2026-06-yue-ts2vec](../../sources/src-2026-06-yue-ts2vec.md), [sources/src-2026-06-li-ti-mae](../../sources/src-2026-06-li-ti-mae.md), [sources/src-2026-06-eldele-ts-tcc](../../sources/src-2026-06-eldele-ts-tcc.md)
- [sources/src-2026-06-fraikin-trep](../../sources/src-2026-06-fraikin-trep.md), [sources/src-2026-06-foumani-series2vec](../../sources/src-2026-06-foumani-series2vec.md), [sources/src-2026-06-talukder-totem](../../sources/src-2026-06-talukder-totem.md), [sources/src-2026-06-eldele-ca-tcc](../../sources/src-2026-06-eldele-ca-tcc.md)
- Project: [projects/p2-causal-embedding-v2](../../projects/p2-causal-embedding-v2.md)
