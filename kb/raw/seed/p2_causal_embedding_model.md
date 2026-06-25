# Causal Embedding Model v2 — Directed Covariate Retrieval

*Seed source note for P2. Consolidates the project deck (Slide 4) with grounding in the
`embedding_model` repo. Sections marked "Design considerations", "Things to try", and "Open
questions" are reasoning/options, not decided facts — treat as candidates to validate.*

---

## Problem Setup

- Feature selection today runs **Granger / Transfer Entropy selectors explicitly** — O(n²) in
  the number of series.
- With ~200M available series, exhaustive TE/Granger computation is intractable.
- In production, covariate discovery is currently handled by explicit selection plus the
  driver-search path (RecommenderClient → AnglerClient); analysts otherwise select covariates
  manually or from a small pre-filtered set, leaving signal on the table.
- Goal: replace expensive explicit pairwise causal scoring with **fast vector retrieval** of
  high-impact covariates, target/query-dependent, at inference time.

---

## Starting Point — the Current Embedding Model

The `embedding_model` repo today produces 128-dim embeddings via a `ConvAttnEncoder`
(TCN → multi-head attention → meanmax pooling). Its similarity-learning (SL) objective aligns
**Soft-DTW distances in series-space** with **L2 distances in embedding-space** — i.e. the
space encodes **shape similarity** and is **symmetric** (d(A,B) = d(B,A)). Retrieval KPIs are
ranking/retrieval metrics (MAP@50, combined rank score).

P2 changes the objective, not the encoder backbone: keep the encoder, **swap the symmetric
shape objective for a directed, asymmetric one** so proximity ≈ causal influence.

---

## Core Idea (from deck)

Retrain the embedding model with a **directed, asymmetric objective (Transfer Entropy /
Granger distillation)** so the 128-dim space encodes causal influence rather than shape
similarity. Use the target series as a **query vector** to retrieve high-impact covariates
from the 200M-series space via fast vector search, replacing O(n²) explicit Granger/TE.

How it works:

1. Precompute pairwise TE/Granger scores on a **subset** of series (distillation — tractable
   on a small team).
2. Use those scores as **soft labels** to train a **directed** embedding space where proximity
   approximates causal influence.
3. At inference: embed target TS → vector search over the embedding space → retrieve top-k
   candidate causal drivers in milliseconds.
4. The space is **asymmetric**: A→B ≠ B→A (no symmetric DTW).

---

## Why It Matters (from deck)

- **100–1000× faster** covariate discovery vs. explicit Granger/TE selection.
- No published equivalent — claimed novel contribution / defensible moat.
- Data flywheel: more usage → richer causal graph across the series space.
- **Feeds P1 directly**: causal covariate embeddings (`z_cov`) replace shape-similarity
  embeddings in P1's covariate-attention layer, making the cluster models materially stronger.

---

## Design Considerations — Encoding Asymmetry

The hard part is representing a directed relation in a vector space. Candidate mechanisms
(to evaluate, not yet chosen):

- **Source/target projection heads**: one encoder, two learned projections; score
  influence(A→B) = f(src(A), tgt(B)) with an asymmetric (e.g. bilinear) scorer.
- **Order / asymmetric embeddings** (order-embedding, hyperbolic/entailment-cone families):
  geometry that natively encodes a directed partial order.
- **Asymmetric distance head** over the existing 128-dim z, trained on TE soft labels.

All must be checked for the deck's stated key risk: **asymmetric geometry convergence** — does
training converge to a stable directed space, or collapse back toward symmetric similarity?

---

## Validation & Importance

- **Directional retrieval accuracy** vs. held-out TE/Granger: does top-k retrieval recover the
  true high-TE drivers, and respect direction (A→B vs B→A)?
- **Geometry-health check**: explicit test that the space has not collapsed to symmetric.
- **Downstream forecast lift** (cleanest signal, requires P1): does retrieved-covariate
  substitution improve P1 cluster-model accuracy on held-out series, beyond ranking metrics?
- Extend the repo's existing retrieval KPIs (MAP@50, rank score) with directional variants.

---

## Challenges

1. **Asymmetric geometry convergence** (deck key risk) — stability of the directed objective.
2. **Distilled-label noise / coverage** — TE/Granger soft labels are themselves
   estimator-and-lag dependent and computed on a subset; the embedding inherits their bias.
3. **Correlation ≠ causation** — retrieved series are *candidate* drivers; "causal" framing is
   unjustified until downstream lift is shown. Prefer "candidate causal driver retrieval".
4. **Regime dependence** — relationships estimated in one regime may not transfer.

---

## Things to Try

- Reuse the existing `SimMemoryBuffer` (same-length negative sampling) adapted for directed
  pairs / hard negatives.
- Use `forecast_pipeline`'s `GrangerSelector` / `TransferEntropySelector` as the **teacher**
  that produces the distillation labels — keeps the label pipeline in the existing stack.
- Condition retrieval on target metadata (cluster ID, horizon) for better generalization when
  the available covariate set varies across targets.
- Decorrelation/diversity on retrieved sets so top-k spans multiple macro factors rather than
  one redundant cluster.

---

## Coupling

- **P2 → P1**: `z_cov` causal embeddings feed P1's covariate-attention layer (replacing
  shape-similarity embeddings). P2 ships as a research thread first; P1's full build starts once
  P2's covariate retrieval is validated.
- **P1 → P2**: P1's cluster forecasting task is P2's downstream evaluation beyond ranking.

---

## Deck Metadata

- Horizon: 6–9 months. Team cost: medium (research track). Primary value: speed + moat.
- Key risk: asymmetric geometry convergence.
