---
type: concept
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-06-30
sources:
  - src-2026-06-p2-causal-embedding-model
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-tsf-literature-review
  - src-2026-06-wang-timexer
  - src-2026-06-arango-chronosx
  - src-2026-06-han-unica
  - src-2026-06-potapczinski-apollopfn
  - src-2026-06-lu-cats-ats
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
- concept
- ssl
- self-supervised
---

# Causal covariate embeddings

## Definition

Directed/asymmetric time-series embeddings where vector proximity is trained to approximate causal/directed influence (covariate → target), not symmetric shape similarity, so that top-k covariate retrieval via vector search substitutes for explicit O(n²) Granger/Transfer-Entropy search. See [sources/src-2026-06-p2-causal-embedding-model](../sources/src-2026-06-p2-causal-embedding-model.md).

## Why it matters

Explicit TE/Granger over a ~200M-series universe is intractable (the deck's stated bottleneck), and retrieval-speed covariate discovery is the proposed P2 moat. The hard, unvalidated part is whether an asymmetric geometry converges and whether retrieved drivers are causal rather than merely correlated.

## Open research questions

- Can a vector space represent asymmetric relations (A→B ≠ B→A) stably without collapsing to symmetric similarity?
- Are distilled TE/Granger soft labels reliable enough to train on, and do they transfer across regimes/horizons?
- Retrieved covariates are *candidate* causal drivers — what validation (downstream forecast lift, intervention-style tests) is needed before any causal language is used externally?

## SSL landscape — P2 gap confirmed (I-P2-A ingest, 2026-06-30)

Primary literature pass on 4 HIGH-priority SSL/contrastive TS papers establishes the following:

**All major SSL TS encoders are symmetric.** None of TS-TCC, TS2Vec, Ti-MAE, or TimeMAE implement a directional/asymmetric objective:
- **TS-TCC** ([src-2026-06-eldele-ts-tcc](../sources/src-2026-06-eldele-ts-tcc.md), IJCAI 2021): temporal contrasting with cross-view prediction + SimCLR contextual loss; symmetric. Linear eval matches supervised on HAR (90.37%) and Epilepsy (97.23%); 10% labeled data matches 100% supervised fine-tuning.
- **TS2Vec** ([src-2026-06-yue-ts2vec](../sources/src-2026-06-yue-ts2vec.md), AAAI 2022): hierarchical contrastive with contextual consistency positive pairs; symmetric; SOTA on 125 UCR datasets (+2.4%) and −32.6% forecasting MSE vs supervised. Best general-purpose symmetric TS encoder prior to 2023.
- **Ti-MAE** ([src-2026-06-li-ti-mae](../sources/src-2026-06-li-ti-mae.md), ICLR 2023 workshop): masked autoencoder, 75% masking ratio, symmetric encoder-decoder. Best SSL method for long-term TS forecasting as of 2023; alleviates distribution shift.
- **TimeMAE** ([src-2026-06-cheng-timemae](../sources/src-2026-06-cheng-timemae.md), TKDE 2023): decoupled masked autoencoder with window slicing + 60% masking; symmetric. Current SOTA for TS classification (91.31% linear eval on HAR vs TS-TCC 77.63%, TS2Vec 78.16%).

**The P2 gap is real:** No existing SSL TS paper implements or evaluates an asymmetric/directed objective where A→B ≠ B→A. This gap validates P2's novelty claim. The closest related work is in asymmetric embedding literature (order embeddings, Poincaré spaces) — not yet validated for TS.

**Design implications:**
- TS2Vec (dilated CNN + contextual consistency) and TimeMAE (decoupled MAE + window slicing) are the strongest symmetric encoder baselines for P2 ablation.
- TimeMAE's window slicing and decoupled architecture are the most relevant design patterns to adopt for P2's pretraining stage.
- P2's directed objective needs to be layered on top of (or replace) the symmetric pretraining objective.

## SSL landscape — MEDIUM papers (I-P2-A ingest, 2026-06-30)

Eight additional SSL TS papers (MEDIUM priority) extend the baseline established above. Key findings:

**Symmetric methods confirmed again:**
- **Series2Vec** ([src-2026-06-foumani-series2vec](../sources/src-2026-06-foumani-series2vec.md), DMKD 2024): replaces augmentation with Soft-DTW similarity as pretext target; outperforms TS-TCC/TS2Vec/Ti-MAE/TimeMAE on UCR; still symmetric.
- **TimeCLR** ([src-2026-06-yang-timeclr](../sources/src-2026-06-yang-timeclr.md), KBS 2022): SimCLR + DTW-aware augmentation (autoencoder generates phase shifts); InceptionTime backbone; symmetric.
- **Multi-task SSL** ([src-2026-06-choi-multitask-ssl](../sources/src-2026-06-choi-multitask-ssl.md), ICLR 2023 ws): combines contextual+temporal+transformation consistency in single framework; symmetric.
- **CA-TCC** ([src-2026-06-eldele-ca-tcc](../sources/src-2026-06-eldele-ca-tcc.md), TPAMI 2023): journal extension of TS-TCC; adds semi-supervised variant (pseudo-labels → class-aware contrastive); symmetric.
- **Jawed 2020** ([src-2026-06-jawed-ssl-semisupervised](../sources/src-2026-06-jawed-ssl-semisupervised.md), ECML 2020): earliest SSL TS paper; forecasting-as-auxiliary-task; superseded by 2021-2023 methods.
- **TOTEM** ([src-2026-06-talukder-totem](../sources/src-2026-06-talukder-totem.md), ICML 2024): VQVAE tokenizer for cross-domain generalist training; zero-shot 80% AvgWins; symmetric reconstruction.

**Key novel finding — T-Rep:**
- **T-Rep** ([src-2026-06-fraikin-trep](../sources/src-2026-06-fraikin-trep.md), ICLR 2024): first SSL TS method to incorporate **learned time-embeddings** (from timestep indices) in pretext tasks. Two novel tasks: (1) Divergence prediction — predict JSD between time-embeddings given representation difference (continuous temporal distance, replaces binary contrastive); (2) Time-embedding-conditioned forecasting. Built on TS2Vec encoder. Outperforms TS2Vec on all tasks + stronger robustness to missing data. Still symmetric.

**P2 design implications from MEDIUM papers:**
- T-Rep's time-embedding approach could inform P2's directed pretext: a regime-aware time-embedding conditioned on market state could sharpen TE/Granger label quality for P2's asymmetric objective.
- Series2Vec confirms that similarity-preserving pretext (using TS-specific distance as target) outperforms augmentation-based contrastive — same principle applies to P2's TE/Granger targets.
- CA-TCC's 4-phase semi-supervised pattern (pretrain on unlabeled → sparse labels → pseudo-labels → class-aware contrastive) is the reference architecture for P2's training with expensive TE/Granger labels.
- TOTEM's VQVAE tokenizer is a candidate cross-domain pretraining stage for P2 if commodity series onboarding is a priority.
- Survey paper (Eldele 2024): P2 is firmly in the **in-domain semi-supervised** quadrant — do not use cross-domain transfer from HAR/ECG benchmarks.

**SSL symmetry gap: confirmed again.** All 12 papers reviewed in I-P2-A (8 HIGH + 8 MEDIUM) are symmetric.

## Literature still to integrate `[verify]`

- Asymmetric / order embeddings: order-embeddings (Vendrov et al.), entailment cones, hyperbolic/Poincaré embeddings (Nickel & Kiela) as candidate asymmetric geometries `[verify]`
- Transfer Entropy (Schreiber) and Granger causality estimation at scale; conditional/multivariate TE `[verify]`
- Knowledge distillation from expensive pairwise scores into a learned retrieval space `[verify]`
- Causal discovery caveats: correlation-vs-causation failure modes in observational time series

## What the primary literature confirms (P1 scope, partial)

From the I-P1-C primary literature pass (2026-06-29):

- **TimeXer** ([src-2026-06-wang-timexer](../sources/src-2026-06-wang-timexer.md), NeurIPS 2024): confirmed primary. Uses cross-attention with a patch-based endogenous encoder and a variate-level exogenous token ("bridge token"); shows statistically significant MSE reduction versus iTransformer, PatchTST, and Chronos on 8 benchmarks. Validates the endo/exo split architecture. Does NOT use retrieval or sparse selection — it attends over all exogenous covariates simultaneously.
- **ChronosX, UNICA, ApolloPFN, CATS-ATS** ([src-2026-06-arango-chronosx](../sources/src-2026-06-arango-chronosx.md), [src-2026-06-han-unica](../sources/src-2026-06-han-unica.md), [src-2026-06-potapczinski-apollopfn](../sources/src-2026-06-potapczinski-apollopfn.md), [src-2026-06-lu-cats-ats](../sources/src-2026-06-lu-cats-ats.md)): all four 2025–2026 papers independently confirm that leading TSFMs (Chronos, TimesFM, MOMENT) do not support exogenous covariates. Covariate adapters are an active and open area.

**What remains unmatched by primaries:** a shared encoder trained independently of the forecasting head, then used for *target-conditioned sparse retrieval* over hundreds of covariates. TimeXer and adapters use dense attention over all covariates; none implement sparse top-k covariate retrieval. This gap is real and represents the P2 novelty claim.

The P2-specific claims (asymmetric geometry, TE/Granger distillation) remain `[verify]` — they are not covered by P1 primary literature.

## Cross-project relevance

- Feeds [concepts/hierarchical-entmax-covariate-selection](hierarchical-entmax-covariate-selection.md) and the P1 attention layer ([projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)).
- Could supply candidate relation retrieval for P4, but P4 must keep provenance ([concepts/explicit-evidence-graph](explicit-evidence-graph.md)).

## Related pages

- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
