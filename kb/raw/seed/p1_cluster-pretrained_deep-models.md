# P1 — Cluster-Pretrained Deep Models

*Seed source note for P1. Consolidates the project deck (Slides 2–3, cluster models, routing,
integration risks, gate experiment) with the query-dependent covariate-selection design note
("gaze"). The system context and risks/gate are deck-sourced; the Covariate Selection Layer
section is the original design note. "Things to try" / "challenges" are reasoning, not decided
facts.*

---

## The Problem It Solves

- Analysts currently hand-tune transforms and hyperparameters **per product**.
- At 10–20 SKUs per client this is manageable; at 500–1000 SKUs it breaks — headcount scales
  linearly with SKU count, which is unsustainable.
- Cluster-pretrained models give every new series a **pre-fitted inductive bias matching its
  type**, eliminating per-product analyst tuning at scale.

Idea: train a lightweight deep model (MLP / D-Linear + covariate attention) **per cluster of
similar series**. When a new SKU arrives: embed → route to its cluster model → forecast
zero-shot or with minimal fold-in.

---

## System Architecture

```
~200M series
   → embedding model (shared SSL encoder)
   → k clusters via FAISS                     (shape clusters)
   → optional sub-clustering by regime         (stationarity / seasonality within a shape cluster)
   → D-Linear / MLP backbone trained on all series in the cluster
   → covariate attention over z_cov embeddings (from P2 — no redundant covariate-rep learning)
   → forecast head
```

- **Routing**: a new series is embedded and routed (FAISS nearest cluster) to its cluster
  model. The cluster routing index is part of model state.
- **Hybrid representation**: embeddings for selection/routing; raw time series retained for
  temporal detail when needed.
- **Covariate layer**: attention consumes `z_cov` embeddings supplied by P2 (causal embedding
  v2), so the cluster model does not relearn covariate representations. The internals of that
  selection layer are the subject of the next section.

---

## Covariate Selection Layer (query-dependent, sparse)

This is the design for the covariate-attention layer referenced above: how, for a given target
query, the model selects and weights a sparse subset of the 50–1000 candidate covariates, and
how it reports interpretable importance. The remainder of this section is the original
covariate-selection design note.

### Problem Setup (covariate selection)

- Global forecasting model trained per target cluster (4–8 clusters).
- Targets and covariates are encoded with a **shared self-supervised encoder**.
- Number of exogenous covariates varies per target (≈50–1000).
- Covariates are independent macroeconomic time series (not fixed sensors).
- Selection must be **target/query-dependent**.
- Goal:
  - propagate only useful covariates,
  - obtain approximate feature importance,
  - maintain stable training and robustness to correlated features.

---

## Selection Mechanisms Considered

- Top-k attention
- α-entmax
- Differentiable ranking / sorting
- Soft k-means clustering
- Hard gates (L0 / hard-concrete)

---

## Attention Weights ≠ Feature Importance

Research suggests:

- Attention weights are not guaranteed to be faithful explanations.
- Different attention distributions may produce nearly identical predictions.
- Attention is better viewed as a routing mechanism than causal attribution.
- Weights alone should be interpreted only as proxies.

---

## Hard Gates vs α-entmax

### Hard Gates (L0 / hard-concrete)

#### Pros

- Stronger interpretability.
- Information flow truly controlled by gates.
- Near binary selection possible.

#### Cons

- More difficult optimization.
- Requires temperature scheduling.
- Risk of collapse (all-on or all-off).
- More hyperparameter tuning.

---

### α-entmax

#### Pros

- Fully differentiable.
- Stable optimization.
- Naturally sparse.
- Adaptive number of active features.

#### Cons

- Weights are not strict importance measures.
- Correlated features may split or concentrate attention arbitrarily.

#### Overall

α-entmax preferred for stable training.

---

## Shared Encoder Setup

- Same encoder for targets and covariates.
- Trained independently with self-supervised similarity objective.
- Covariate clusters can be precomputed in embedding space.
- Embedding-space clusters can act as latent macro factors.

---

## Feature Importance

Avoid using raw attention weights only.

### Per-feature importance

Given entmax weights:

\[
a_i = \text{entmax}(s_i)
\]

Use:

#### Weight × sensitivity

\[
Imp_i = a_i \cdot \left|\frac{\partial \mathcal L}{\partial a_i}\right|
\]

or

\[
Imp_i = a_i \cdot \left\|\frac{\partial \hat y}{\partial a_i}\right\|
\]

Advantages:

- One forward + backward pass.
- Much cheaper than ablation.
- More faithful than attention weights alone.

---

## Handling Correlated Features

Correlated macro variables create unstable top-k selections.

Rather than identifying individual series, identify latent factors.

### Cluster-level importance

Given clusters \(C_j\):

Cluster mass:

\[
A_j = \sum_{i\in C_j} a_i
\]

Cluster importance:

\[
ImpCluster_j
=
A_j
\cdot
\left|
\frac{\partial \mathcal L}{\partial A_j}
\right|
\]

Advantages:

- Robust to collinearity.
- Stable across runs.
- Captures macro themes rather than arbitrary representatives.

---

## Hierarchical Selection (Recommended)

### Stage 1: Cluster selection

Compute cluster embeddings/prototypes.

Score clusters:

\[
u_j = g(q,p_j)
\]

Apply α-entmax:

\[
\beta = entmax(u)
\]

---

### Stage 2: Within-cluster selection

For cluster \(j\):

\[
\gamma^{(j)}
=
entmax(s_i)
\]

Final feature weight:

\[
a_i
=
\beta_{c(i)}
\cdot
\gamma^{(c(i))}_i
\]

Benefits:

- Better robustness to correlated features.
- Natural factor-level interpretability.
- Lower computation for large N.

---

## Diversity Regularization

Prevent selecting many nearly identical series.

Possible penalty:

\[
\sum_{i\neq j}
a_i a_j
\cos(e_i,e_j)
\]

Effects:

- Encourages coverage of multiple macro factors.
- Produces more meaningful top features.

---

## Fast Alternatives to Ablation

Full ablations are expensive.

Avoid:

- KernelSHAP (too expensive).
- Large-scale leave-one-out.

Prefer:

#### Weight × gradient

\[
a_i
\cdot
\left|
\frac{\partial \mathcal L}{\partial a_i}
\right|
\]

#### Cluster importance

\[
A_j
\cdot
\left|
\frac{\partial \mathcal L}{\partial A_j}
\right|
\]

#### MC dropout stability

Run multiple stochastic forward passes:

Measure:

- cluster activation frequency,
- variance of cluster importance.

Provides confidence estimates cheaply.

---

## Recommended Architecture

Shared encoder
↓
Target query embedding q
↓
Covariate embeddings e_i
↓
Hierarchical selector

Cluster entmax
↓
Within-cluster entmax
↓
Sparse weighted covariate aggregation
↓
Forecast head

No residual path bypassing selection.

---

## Importance Reporting

### Forecast-level

Top macro clusters:

- cluster mass
- cluster sensitivity

Within each cluster:

- highest-weight covariates
- highest sensitivity covariates
- representative covariates closest to cluster centroid

---

### Dataset-level

Aggregate:

- cluster importance by target cluster,
- horizon-specific cluster importance,
- stability across MC-dropout samples.

---

## Main Recommendation

Prefer:

- Shared encoder
- Precomputed embedding clusters
- Hierarchical cluster→feature α-entmax
- No residual bypass before selection
- Feature importance via:

\[
a_i
\cdot
\left|
\frac{\partial \mathcal L}{\partial a_i}
\right|
\]

and

\[
A_j
\cdot
\left|
\frac{\partial \mathcal L}{\partial A_j}
\right|
\]

This provides:

- stable training,
- adaptive sparsity,
- robustness to correlated macro variables,
- scalable handling of 50–1000 covariates,
- interpretable cluster-level explanations without expensive ablation.




## Thoughts:

### things to try:
- look into variable selection method used in TFT
- use cluster assignments from clustering (for grouped/diversity data)

- treat data similar to target (from vector search) as another cluster
- do hierarchical gating/attribution to prevent over influence of a single cluster with highly correlated features
  - first selecting a subset of clusters via per cluster embedding (e.g. mean-max of their member embeddings)
  - select a subset of members from each cluster
- this allows for "per cluster importance" and refined "per-feature importance"
- add additional decorrelation regularizer 
  - Encourage using multiple clusters
  - Within top clusters, discourage selecting many highly similar members


---
Because we have a cluster per target and covariate clusters, a nice synergy is - condition the selector on:
- target embedding
- target cluster ID embedding
- horizon embedding

This improves generalization when the available covariates change a lot across targets.


### challenges:
1. stop high variance in feature selection because of high correlation/information redundancy of covariates
2. get useful importance scores for clusters and covariates which are not heavily affected by 1.)
   - e.g. via dropout masks: run 10 stochastic forward passes (MC dropout) and compute:
     - how often each cluster gets non-zero mass
     - variance of cluster mass
    - This is often more actionable than single-pass weights and far cheaper than ablations.
---

## Risks & Mitigations (deck Slide 3)

**1. Cluster quality — shape ≠ regime.**
DTW/shape embeddings cluster by shape similarity, but two shape-similar series may sit in
different stationarity regimes requiring different transforms; a single cluster model could
underfit mixed-regime members.
*Mitigation:* sub-cluster by regime within each shape cluster using existing detector flags
(`NonstationarityDetector`, `SeasonalityDetector`, `HeteroscedasticityDetector`); each
sub-cluster gets its own model trained on regime-consistent series.

**2. PyTorch integration into the library.**
`forecast_pipeline` uses strict layering (LGBM, linear, statsforecast). A PyTorch deep model
must extend the `Model` ABC and the serialization layer without violating determinism or
layering invariants.
*Mitigation:* implement `ClusterDeepModel` as a first-class `Model` ABC subclass; persist the
FAISS cluster routing index via `save_state_dict`; keep the deep model an **optional
dependency** so the library stays lightweight for non-deep use cases. (Note the determinism
carve-out this implies for any MC-dropout importance estimation in the selection layer.)

**3. No proven accuracy gain over tuned LGBM yet.**
Deep models don't always beat well-tuned gradient boosting on tabular/TS data.
*Mitigation:* frame success as **analyst-time elimination, not raw accuracy**. Validate on M5
and VN2 (200M series are the training data). If cluster models *match* tuned LGBM accuracy,
zero-shot onboarding is already a net win.

---

## Gate Experiment (2–3 weeks, run immediately)

Validates cluster quality before committing engineering bandwidth:

1. Embed **150 benchmark series**.
2. Cluster the embeddings.
3. Run the detector suite per cluster.
4. Measure **within-cluster variance** of stationarity, seasonality, and heteroscedasticity
   flags.

**Decision rule:** low within-cluster variance → proceed directly to per-cluster models; high
variance → implement shape + regime sub-clustering, then proceed. *(Threshold vs. a
random-clustering baseline must be pre-registered — not specified in the deck.)*

---

## Expected Impact (deck Slide 2)

- Near-zero marginal cost per new SKU onboarded.
- Enables 1000-SKU enterprise clients without an analyst bottleneck.
- Public-benchmark validation: M5 and VN2 Inventory Planning; 200M series are the training
  pool, so there is no benchmark dependency for training.

---

## Coupling

- **P2 → P1**: causal covariate embeddings (`z_cov`) replace shape-similarity embeddings in the
  attention layer, making P1 materially stronger. P1's full build starts once P2's covariate
  retrieval is validated.
- **P3 → P1**: P3 proves value at 10–20 SKUs; as clients scale to 100–1000 SKUs the analyst
  bottleneck becomes the hard constraint — P3 creates the commercial pressure that justifies
  P1.
- **P1 → P2**: P1's cluster forecasting task is P2's downstream validation beyond ranking
  metrics.

---

## Deck Metadata

- Horizon: 6–10 months. Team cost: high (1 FTE lead). Primary value: scalability (core unlock).
- Gate: 2–3 week cluster QA first.
- Open architecture question (deck Slide 8): D-Linear vs MLP backbone — prototype both on one
  cluster, or commit upfront?
