---
type: source
domain: timeseries-forecasting
project: P1
status: active
stage: researched
confidence: medium
updated: 2026-06-30
sources:
- src-2026-06-tsitsulin-embedding-quality
tags:
- embedding-evaluation
- clustering
- faiss
- unsupervised-metrics
zotero: tsitsulinUnsupervisedEmbeddingQuality2023
source_hash: d2176efa1f47bd95c0ebb60a2a8dc4f10449af58005d39c5ab9b601f0b25f775
---

# Unsupervised Embedding Quality Evaluation

**Tsitsulin et al. (2023)**

## Summary

Proposes and evaluates metrics for assessing the quality of embeddings **without access to downstream labels** — the unsupervised embedding quality evaluation problem. Surveys existing metrics (NESum, dimensional collapse measures, alignment/uniformity) and introduces four novel metrics based on different geometric perspectives:

1. **Coherence / Incoherence** (µ₀): measures how easily a linear probe can separate the data from the representations alone; higher incoherence = more linearly separable.
2. **Stable rank**: effective intrinsic dimensionality of the representation matrix; avoids dimensional collapse.
3. **SelfCluster**: pairwise dot-product norm normalized by random expectation — measures how strongly the embeddings cluster relative to isotropic random vectors.
4. A fourth metric based on covariance structure (related to barlow twins analysis).

Experiments: supervised representation learning (deep DNNs) and shallow graph embeddings.

## Claims

- **No universally dominant metric** for unsupervised embedding quality — different metrics are optimal for different architectures and tasks; a suite of metrics is recommended. [Evidence: Section 4, experimental results]
- **Coherence and stable rank correlate best with downstream task performance** and are more computationally stable than state-of-the-art metrics, especially for shallow embedding models. [Evidence: Section 4]
- **SelfCluster measures geometric clustering tendency** of embeddings relative to random distribution; useful for detecting whether embeddings are meaningfully clustered. [Evidence: Section 3.4]
- **Standard metrics fail for shallow models** (e.g., graph embeddings) — the proposed metrics handle both deep DNN representations and shallow single-layer embeddings. [Evidence: Section 4.2]

## Caveats

- No direct evaluation on time-series embeddings — tested on image classification (supervised) and graph node embeddings (unsupervised).
- Metrics assume L₂-normalized embeddings; behavior on unnormalized TSF embeddings needs validation.
- The paper does not address dynamic embeddings (embeddings that change over time as price regimes shift) — static evaluation framework.
- "No free lunch" finding means P1 will need to use multiple metrics, not a single score.

## Applicability to P1

**High and direct for the P1 cluster quality gate.**

P1's cluster routing quality gate requires evaluating whether FAISS clusters of time-series embeddings are "good" — i.e., whether series in the same cluster share meaningful dynamical properties (volatility regime, seasonality structure) that justify a shared model. This is exactly the unsupervised embedding quality evaluation problem.

Specific metrics from this paper applicable to P1's cluster QA:
- **Coherence/Incoherence**: do cluster-member embeddings support good linear separation between cluster types?
- **Stable rank**: are the embeddings informationally dense, or have they collapsed to a low-dimensional manifold?
- **SelfCluster**: do the embeddings naturally cluster with high geometric compactness, or are they diffuse?

These metrics can be computed without any labels and before running any forecasting experiments — making them practical as a pre-training quality gate.

The "no free lunch" finding implies P1 should report multiple metrics in the cluster quality gate experiment rather than a single number. See [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md).

## Related

- [experiments/exp-p1-cluster-quality-gate](../experiments/exp-p1-cluster-quality-gate.md) — P1 cluster quality gate experiment
- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md) — Cluster quality success criterion
