---
type: concept
domain: embedding-models
project: P2
status: active
stage: seed
confidence: medium
updated: 2026-07-01
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
  - src-2026-06-he-moco
  - src-2026-06-kazemi-time2vec
  - src-2026-06-musgrave-metric-learning-reality
  - src-2026-06-liu-ssl-comparison
  - src-2026-06-beck-xlstm
  - src-2026-06-embedding-model-v1
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

## Chosen design approach: Series2Vec-style similarity learning with asymmetric target (decided 2026-07-01)

P2's directed objective is a **direct extension of v1's SL head**, using the same Series2Vec learning paradigm with a different similarity function:

| | V1 SL head | P2 SL head |
|---|---|---|
| Similarity function | Soft-DTW(x_A, x_B) — symmetric | TE(x_A → x_B) / Granger(A→B) — asymmetric |
| Pairwise matrix M_ij | Soft-DTW(x_i, x_j) = M_ji | TE(x_i → x_j) ≠ TE(x_j → x_i) |
| z-space distance | L2 (symmetric) | Directed: sim(z_A_src, z_B_tgt) ≠ sim(z_B_src, z_A_tgt) |
| Loss structure | SmoothL1(Soft-DTW_x, L2_z) | directed_loss(TE_{ij}, directed_dist(z_i, z_j)) |

**Why not knowledge distillation:** TE/Granger scores are used as direct pairwise similarity labels in the loss — no teacher model, no two-stage training. The mechanism is Eq. 3 of Series2Vec with the similarity function swapped. `GrangerSelector` / `TransferEntropySelector` in v1 are label generators for the asymmetric similarity matrix, not distillation teachers.

**Key implementation question:** Whether TE/Granger can be computed at batch-training granularity (pairs computed on-the-fly) or requires a precomputed lookup table. The `SimMemoryBuffer` provides the length-binned pairs; the open question is label freshness and computational cost per batch.

## Open research questions

- Do `W_src` and `W_tgt` dual projections produce a stable asymmetric geometry, or does training collapse to `W_src ≈ W_tgt` (symmetric degenerate solution)? A convergence monitor tracking `||W_src − W_tgt||_F` during training is needed.
- Can TE/Granger scores be computed efficiently enough per batch, or does a precomputed lookup table cover sufficient pair coverage? The `SimMemoryBuffer` re-samples the candidate pool each epoch; on-the-fly TE per batch may be too slow.
- Are TE/Granger scores reliable as training labels across regimes and horizons, or do they generalize poorly outside the sampled window?
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

## Architecture inputs (ingest 2026-06-30)

**Associative memory as directed embedding analogy:**
- **xLSTM mLSTM** ([src-2026-06-beck-xlstm](../sources/src-2026-06-beck-xlstm.md), NeurIPS 2024): matrix memory C_t = f_t·C_{t-1} + i_t·v_t·k_t^T is a parallelizable key–value associative memory trained end-to-end. This validates that asymmetric (k, v, q) geometries converge under gradient descent, directly addressing the first open research question above. The mLSTM is not P2's architecture, but proves the core feasibility premise.

**Time-embedding for directed pretext:**
- **Time2Vec** ([src-2026-06-kazemi-time2vec](../sources/src-2026-06-kazemi-time2vec.md), 2019): t2v(τ)[i] = sin(ωᵢτ + φᵢ) with learned frequencies/phase-shifts. Extending T-Rep's temporal conditioning, P2 should concatenate t2v(timestamp) with each series embedding as an auxiliary signal — this makes TE/Granger label distillation regime-aware (commodity supercycles, harvest seasons, monetary policy phases). Foundational reference for T-Rep ([src-2026-06-fraikin-trep](../sources/src-2026-06-fraikin-trep.md)).

**Training design:**
- **MoCo** ([src-2026-06-he-moco](../sources/src-2026-06-he-moco.md), CVPR 2020): momentum encoder (EMA m=0.999) + FIFO queue (65,536 negatives) enables large consistent dictionaries at 8-GPU scale. P2 should use a momentum encoder for the source/cause branch and a gradient-updated encoder for the target/effect branch; queue-based negatives solve the sparse positive problem (TE/Granger positive pairs are rare at 200M scale).

**Pretraining stage decision:**
- **Liu SSL comparison** ([src-2026-06-liu-ssl-comparison](../sources/src-2026-06-liu-ssl-comparison.md), 2024): at sparse label regime (< 0.1 label ratio) — which matches P2's TE/Granger annotation budget — MAE pretraining outperforms SimCLR. P2 decision: **use MAE backbone for pretraining**, then fine-tune the directed asymmetric head.

**Evaluation protocol:**
- **Musgrave** ([src-2026-06-musgrave-metric-learning-reality](../sources/src-2026-06-musgrave-metric-learning-reality.md), ECCV 2020): most claimed metric learning improvements vanish under fair evaluation (equal architecture, dimensions, augmentations, Bayesian hyperparameter search). P2 evaluation must fix these variables across all symmetric baselines; use MAP@R or directional precision metrics, not Recall@K alone.

## V1 symmetric baseline (production, 2026-06-30)

The production v1 model ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)) is the concrete symmetric baseline P2 must beat. Its learning paradigm is built on two conceptual sources:

- **SL head (weight 0.7) ← Series2Vec** ([src-2026-06-foumani-series2vec](../sources/src-2026-06-foumani-series2vec.md)): similarity-preserving pretext with Soft-DTW pairwise targets. Replaces augmentation-based contrastive learning. V1's loss `SmoothL1(Soft-DTW_x, L2_z)` is the direct implementation of Series2Vec's Eq. 3.
- **GL head (weight 0.3) ← Ti-MAE** ([src-2026-06-li-ti-mae](../sources/src-2026-06-li-ti-mae.md)): masked autoencoder paradigm (30% masking → reconstruction forces encoder to handle missing values and learn global context). Ti-MAE validated this paradigm for time-series SSL.

V1 components:
- **Encoder:** `ConvAttnEncoder` — TCN → multi-head attention → meanmax pooling → 128-dim `z`
- **SL head:** Soft-DTW in x-space + L2 in z-space — **symmetric** by construction (DTW(A,B) = DTW(B,A)) — P2 replaces this
- **GL head:** MSE on 30% masked tokens; sLSTM decoder — P2 reuses unchanged
- **Negative sampling:** `SimMemoryBuffer` — length-binned `(x, z)` pairs across batches — P2 reuses

| | V1 (symmetric) | P2 v2 (directed) |
|---|---|---|
| x-space similarity | Soft-DTW(A,B) = Soft-DTW(B,A) | TE(A→B) ≠ TE(B→A) |
| z-space target | L2 (symmetric) | asymmetric directed distance |
| Label source | Unsupervised (shape geometry) | TE/Granger computed on batch pairs |
| A→B ≠ B→A? | No | Yes — this is the P2 claim |
| Paradigm | Series2Vec Eq. 3 with Soft-DTW | Series2Vec Eq. 3 with TE/Granger |

**Why this matters for the concept:** P2's change is minimal — three specific lines changed in the loss pipeline plus two linear projection heads added to the model. V1 proves the encoder, data pipeline, and `SimMemoryBuffer` work at production scale. P2's research bet is whether replacing the similarity function and inducing role-differentiated projections (`W_src`, `W_tgt`) produces a stable asymmetric geometry rather than collapsing to `W_src ≈ W_tgt`. See [sources/src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md) → "Relevance to P2" for the full code-level delta.

## Literature still to integrate `[verify]`

- Transfer Entropy (Schreiber) and Granger causality estimation at scale; conditional/multivariate TE; estimator bias and sample-size requirements (Runge 2018) `[verify]`
- Granger/TE equivalence under Gaussianity (Barnett 2009) — determines which estimator to use for commodity series `[verify]`
- Asymmetric / order embeddings: order-embeddings (Vendrov et al.), hyperbolic/Poincaré embeddings (Nickel & Kiela) — candidate z-space geometries for the directed distance function `[verify]` (note: chosen paradigm is Series2Vec-style similarity learning; the asymmetric geometry is a z-space design choice within that, not an alternative approach)
- Causal discovery caveats: correlation-vs-causation failure modes in observational time series

**Removed from verify list:** knowledge distillation (Hinton 2015, Park 2019 relational KD) — not the chosen mechanism. P2 uses direct pairwise similarity labels, not a teacher-student training process.

## What the primary literature confirms (P1 scope, partial)

From the I-P1-C primary literature pass (2026-06-29):

- **TimeXer** ([src-2026-06-wang-timexer](../sources/src-2026-06-wang-timexer.md), NeurIPS 2024): confirmed primary. Uses cross-attention with a patch-based endogenous encoder and a variate-level exogenous token ("bridge token"); shows statistically significant MSE reduction versus iTransformer, PatchTST, and Chronos on 8 benchmarks. Validates the endo/exo split architecture. Does NOT use retrieval or sparse selection — it attends over all exogenous covariates simultaneously.
- **ChronosX, UNICA, ApolloPFN, CATS-ATS** ([src-2026-06-arango-chronosx](../sources/src-2026-06-arango-chronosx.md), [src-2026-06-han-unica](../sources/src-2026-06-han-unica.md), [src-2026-06-potapczinski-apollopfn](../sources/src-2026-06-potapczinski-apollopfn.md), [src-2026-06-lu-cats-ats](../sources/src-2026-06-lu-cats-ats.md)): all four 2025–2026 papers independently confirm that leading TSFMs (Chronos, TimesFM, MOMENT) do not support exogenous covariates. Covariate adapters are an active and open area.

**What remains unmatched by primaries:** a shared encoder trained independently of the forecasting head, then used for *target-conditioned sparse retrieval* over hundreds of covariates. TimeXer and adapters use dense attention over all covariates; none implement sparse top-k covariate retrieval. This gap is real and represents the P2 novelty claim.

The P2-specific claims (asymmetric geometry, TE/Granger distillation) remain `[verify]` — they are not covered by P1 primary literature.

## Cross-project relevance

**P1 (active, v1 phase):** P1 already uses v1 pre-computed embeddings as the key/query vectors in its covariate selection layer ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)). V1's symmetric SL head (Soft-DTW) gives shape-similarity covariate selection for free. This is Phase 0 of the P1/P2 integration. Phase 1 is a surgical interface swap: replace `z_cov_k` from v1 with `z_cov_k` from P2's directed model — no other P1 changes required. See [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md).

**P4:** Could supply candidate relation retrieval, but P4 must keep provenance ([concepts/explicit-evidence-graph](explicit-evidence-graph.md)).

## Related pages

- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
- [domains/embedding-models/thesis](../domains/embedding-models/thesis.md)
