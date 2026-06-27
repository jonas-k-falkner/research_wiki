---
type: concept
domain: timeseries-forecasting
project: P1
status: active
confidence: medium
stage: seed
updated: 2026-06-27
sources:
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-tsf-literature-review
tags:
  - concept
---

# Hierarchical entmax covariate selection

## Definition

A two-stage, target-query-dependent sparse selector: first select covariate *clusters* via α-entmax over cluster prototypes, then select features *within* chosen clusters via α-entmax; final weight is the product of cluster and within-cluster weights. Importance is reported via weight × gradient sensitivity and cluster mass, not raw attention weights. See [sources/src-2026-06-p1-cluster-pretrained-deep-models](../sources/src-2026-06-p1-cluster-pretrained-deep-models.md).

## Why it matters

Macro covariates are highly correlated, which makes flat top-k selection unstable and makes single-feature importance arbitrary. Hierarchy + cluster-level mass is the proposed robustness fix, and the explicit separation of *routing* from *explanation* is what keeps the interpretability claim defensible.

## Open research questions

- α-entmax vs hard L0 / hard-concrete gates: the note prefers entmax for training stability, but hard gates give stronger interpretability — which wins on our correlated-macro data?
- How is the cluster structure obtained (precomputed embedding clusters vs learned), and how sensitive is selection to it?
- Does "no residual path bypassing selection" cost accuracy, and is that an acceptable price for interpretability?

## Literature to integrate `[verify]`

- sparsemax / α-entmax (Martins & Astudillo; Peters, Niculae & Martins) `[verify]`
- Temporal Fusion Transformer variable selection networks (Lim et al.) as a comparison mechanism `[verify]`
- L0 regularization / hard-concrete gates (Louizos, Welling, Kingma) `[verify]`
- Faithfulness of attention as explanation (Jain & Wallace; Wiegreffe & Pinter) `[verify]`
- Diversity/decorrelation regularizers for redundant feature sets

## What the external review says `[verify]`

A deep-research synthesis ([sources/src-2026-06-tsf-literature-review](../sources/src-2026-06-tsf-literature-review.md)) adds two calibrations:

- **α-entmax / hard-concrete support in TSF is adjacent, not direct.** The strong 2024–2026 covariate and clustering papers use attention, soft clustering, or adapters — not entmax/hard-concrete gates. Choosing entmax imports a sensible sparse-selection tool into a gap area; it is *not* following a dominant TSF tradition. The seed note slightly overstated entmax as literature-backed.
- **Cluster-level attribution is a genuine open opportunity.** Channel Clustering reports interpretability gains but no faithful attribution mechanism; DUET clusters/sparsifies but does not do cluster importance in the explanation sense. Reporting cluster mass + cluster sensitivity + within-cluster representatives is more methodologically mature than current forecasting papers, and the attention-faithfulness debate ("Attention is not Explanation" / "…not not Explanation") supports treating routing weights as proxies paired with weight×gradient and stability diagnostics.

All `[verify]` against named primaries; page stays `seed`.

## Cross-project relevance

- Primary selection mechanism for [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md); consumes [concepts/causal-covariate-embeddings](causal-covariate-embeddings.md) when P2 matures.

## Related pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [projects/p2-causal-embedding-v2](../projects/p2-causal-embedding-v2.md)
