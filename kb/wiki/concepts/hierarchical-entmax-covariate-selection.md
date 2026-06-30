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
- src-2026-06-peters-sparse-seq2seq-2019
- src-2026-06-jain-attention-not-explanation-2019
- src-2026-06-wiegreffe-attention-not-not-2019
- src-2026-06-lim-tft-2021
- src-2026-06-lundberg-shap-2017
- src-2026-06-sundararajan-integrated-gradients-2017
- src-2026-06-liu-rethinking-attention-explainability-2022
- src-2026-06-bastings-elephant-interpretability-2020
- src-2026-06-bibal-attention-explanation-survey-2022
- src-2026-06-rojat-xai-timeseries-2021
- src-2026-06-yasuda-sequential-attention-2023
- src-2026-06-tezekbayev-alpha-relu-2022
- src-2026-06-zhao-sparse-transformer-2019
- src-2026-06-lou-sparsek-attention-2024
- src-2026-06-tay-sparse-sinkhorn-attention-2020
- src-2026-06-sokar-wast-feature-selection-2022
- src-2026-06-embedding-model-v1
tags:
- concept
---

# Hierarchical entmax covariate selection

## Definition

A two-stage, target-query-dependent sparse selector: first select covariate *clusters* via α-entmax over cluster prototypes, then select features *within* chosen clusters via α-entmax; final weight is the product of cluster and within-cluster weights. Importance is reported via weight × gradient (AttGrad) sensitivity and cluster mass, not raw attention weights alone. See [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md).

**Query and key representations (2026-06-30 update):** In P1's two-stream architecture, the query and key vectors for the selection layer come from **pre-computed v1 embeddings** ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)), not from the backbone or a separately trained encoder. This gives the selection layer rich structural representations (shape similarity, DTW-invariant patterns) before any gradient flows through it. An optional learned projection (128 → d_sel) adapts the 128-dim v1 embeddings to the selection layer's internal dimension.

## Why it matters

Macro covariates are highly correlated, which makes flat top-k selection unstable and makes single-feature importance arbitrary. Hierarchy + cluster-level mass is the proposed robustness fix, and the explicit separation of *routing* from *explanation* (via AttGrad, not raw attention) is what keeps the interpretability claim defensible against the Jain/Wiegreffe faithfulness debate.

## α-entmax mechanism

The α-entmax transformation family interpolates between softmax (α=1), 1.5-entmax, and sparsemax (α=2); values α>1 produce exactly-zero weights for low-scoring elements. Peters et al. (2019) establish that **1.5-entmax is the empirical sweet spot**: it outperforms softmax (BLEU 26.17 vs 25.70 on DE→EN) and sparsemax (24.69) on NMT across six language pair directions, and reduces average non-zero attention positions from 24.25 (softmax) to 5.55 (vs 3.75 for sparsemax). An exact O(d log d) bisection algorithm exists for 1.5-entmax, and GPU speed is near-softmax. See [sources/src-2026-06-peters-sparse-seq2seq-2019](../sources/src-2026-06-peters-sparse-seq2seq-2019.md).

## TFT comparison baseline

The Temporal Fusion Transformer (Lim et al. 2021) is the primary comparison mechanism. TFT's variable selection network uses a GRN followed by **standard Softmax** (not sparsemax or entmax) to produce variable importance weights v_χt. This gives non-sparse weights where all variables receive some positive mass, preventing hard feature zeroing. Ablation shows removing variable selection networks increases P90 quantile loss by **4.1% on average** — establishing a benchmark for how much covariate selection contributes to accuracy. P1 aims to replace TFT's Softmax with α-entmax to gain hard sparsity and explicit cluster routing. See [sources/src-2026-06-lim-tft-2021](../sources/src-2026-06-lim-tft-2021.md).

## Faithfulness: what the debate resolved

The attention-faithfulness literature (2019–2022) converges on a practical consensus relevant to P1:

1. **Raw attention weights are insufficient as explanation** (Jain & Wallace 2019): attention weights in BiLSTMs correlate only weakly with gradient/LOO feature importance (Kendall τ ~0.3–0.5). Adversarial attention distributions exist — alternative weights with JSD ~0.69 from learned weights that produce identical predictions. See [sources/src-2026-06-jain-attention-not-explanation-2019](../sources/src-2026-06-jain-attention-not-explanation-2019.md).

2. **Attention can be faithful but requires validation** (Wiegreffe & Pinter 2019): trained attention outperforms adversarial alternatives on diagnostic tests; faithfulness is task- and dataset-dependent. Attention is not categorically unusable — but cannot be assumed. See [sources/src-2026-06-wiegreffe-attention-not-not-2019](../sources/src-2026-06-wiegreffe-attention-not-not-2019.md).

3. **AttGrad is the recommended explanation measure** (Liu et al. 2022): raw attention has polarity-consistency violation ratios of ~0.31–0.40; Attention ⊗ Gradient reduces this to ~0.02–0.06. Deeper architectures → more violations. Use AttGrad (α ⊗ ∇α) not raw α. See [sources/src-2026-06-liu-rethinking-attention-explainability-2022](../sources/src-2026-06-liu-rethinking-attention-explainability-2022.md).

4. **Saliency over attention** (Bastings & Filippova 2020): attention operates on contextual representations, not original inputs; gradient saliency requires only one backward pass and is systematically preferable for input-level attribution. See [sources/src-2026-06-bastings-elephant-interpretability-2020](../sources/src-2026-06-bastings-elephant-interpretability-2020.md).

**Implication for P1**: the P1 explanation protocol must report AttGrad (entmax weight × gradient of forecast loss w.r.t. that weight), not raw entmax weights. Cluster-level mass is a routing signal, not a direct faithfulness claim. Faithfulness must be validated empirically per dataset using the polarity consistency test (Liu et al. 2022). This is a faithfulness claim (mechanistic accuracy), not merely a plausibility claim (human-aligned appearance). See [concepts/attention-faithfulness](attention-faithfulness.md).

## Post-hoc attribution alternatives

- **SHAP / Kernel SHAP** (Lundberg & Lee 2017): model-agnostic, no gradients needed, but treats features independently and does not model temporal ordering — limiting applicability to time-series covariate explanation. Can serve as external validation baseline. See [sources/src-2026-06-lundberg-shap-2017](../sources/src-2026-06-lundberg-shap-2017.md).
- **Integrated Gradients** (Sundararajan et al. 2017): gold-standard gradient-based attribution, satisfies Completeness axiom. Requires 20–300 gradient evaluations per attribution — infeasible at inference time but valuable for offline validation. See [sources/src-2026-06-sundararajan-integrated-gradients-2017](../sources/src-2026-06-sundararajan-integrated-gradients-2017.md).
- **XAI for time series** (Rojat et al. 2021): temporal ordering and stability of explanations are underexplored criteria; post-hoc methods introduce a gap between explanation and model computation. Intrinsic (built-in) selection as in P1 closes this gap. See [sources/src-2026-06-rojat-xai-timeseries-2021](../sources/src-2026-06-rojat-xai-timeseries-2021.md).

## Feature selection alternatives

- **Sequential Attention** (Yasuda et al. 2023): greedy marginal selection captures residual feature value, avoiding redundant-feature selection that flat entmax may suffer from. Equivalent to OMP for linear regression. Consider as ablation or post-hoc refinement step in P1. See [sources/src-2026-06-yasuda-sequential-attention-2023](../sources/src-2026-06-yasuda-sequential-attention-2023.md).
- **α-ReLU** (Tezekbayev et al. 2022): faster alternative to α-entmax with same sparsity properties, matching softmax training speed. Useful if entmax bisection becomes a bottleneck; note that unnormalized outputs complicate cluster-mass attribution interpretation. See [sources/src-2026-06-tezekbayev-alpha-relu-2022](../sources/src-2026-06-tezekbayev-alpha-relu-2022.md).

## V1-embedding-based selection mechanism (2026-06-30)

Using v1 pre-computed embeddings ([src-2026-06-embedding-model-v1](../sources/src-2026-06-embedding-model-v1.md)) as query/key vectors substantially de-risks the selection layer:

**Selection scores (Phase 0):**
```
query_k  = W_q · z_target     # optionally just z_target directly (unit-norm)
key_k    = W_k · z_cov_k      # optionally just z_cov_k directly
score_k  = dot(query_k, key_k)
weights  = α-entmax(scores)   # exact-zero weights = hard covariate gate
```

**Why v1 embeddings are a good prior for selection:**
- v1 SL head (Soft-DTW, weight 0.7) is directly trained to map structurally similar series to nearby vectors — this is exactly the structural relevance prior a covariate selector needs
- v1 has L2 norm regularization pushing embeddings toward unit-norm, so dot-product ≈ cosine similarity without any projection
- Embeddings are offline-computable, stable, and interpretable (similar z → similar shape/dynamics)

**What the selection layer still needs to learn:**
- The projection W_q, W_k (optional but recommended): adapts the symmetric shape-similarity space to forecasting-task-specific relevance
- The α-entmax temperature / threshold: controls sparsity given the forecast loss

**Phase 0 → Phase 1:** When P2 is ready, replace `z_cov_k` with P2's directed embeddings at the key input. The learned projection and entmax operation are unchanged — the directional information enters through the keys alone.

## Open research questions

- **α-entmax vs hard L0 / hard-concrete gates**: entmax preferred for training stability and interpretable cluster mass; hard gates give stronger sparsity guarantees. The correlated-macro-data setting may favor entmax's continuous relaxation for convergence. Requires empirical comparison on P1 datasets.
- **Redundancy under correlation**: flat entmax may assign high mass to multiple correlated covariates simultaneously. Sequential Attention's greedy marginal approach (Yasuda et al.) could address this; alternatively, a decorrelation regularizer on cluster weights.
- **Cluster structure sensitivity**: now anchored to v1 embedding space (stable pretraining, not fold-sensitive). Risk reduced vs learned-from-scratch prototypes. Main residual risk: does v1's shape-similarity space separate P1's commodity regimes well enough for routing?
- **Projection necessity**: v1 embeddings are near-unit-norm; cosine similarity may be sufficient without W_q/W_k. Empirical ablation needed.
- **AttGrad validation on forecasting**: Liu et al.'s polarity consistency test was developed on NLP classification tasks. Its translation to quantile forecasting targets (P10/P50/P90) requires adaptation — the "polarity" direction is less obvious for multi-horizon loss minimization.
- **No-residual-path cost**: does enforcing no residual path bypassing the entmax selection gate cost forecast accuracy, and is that an acceptable price for interpretability?

## Cross-project relevance

- Primary selection mechanism for [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md); consumes [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md) when P2 matures.

## Related pages

- [concepts/attention-faithfulness](attention-faithfulness.md)
- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
