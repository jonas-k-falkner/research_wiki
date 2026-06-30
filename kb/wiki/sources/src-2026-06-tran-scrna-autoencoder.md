---
type: source
domain: embedding-models
project: P2
status: active
stage: researched
confidence: low
updated: 2026-06-30
sources:
- src-2026-06-tran-scrna-autoencoder
tags:
- autoencoder
- hierarchical
- background
zotero: tranFastPreciseSinglecell2021
source_hash: 187d13728a347eee3428183ced2efd43c8eb5d9d4885e8f385094b3c440fa43e
---

# Source: Fast and Precise Single-cell Data Analysis Using a Hierarchical Autoencoder (2021)

## Metadata
- **Citekey:** `tranFastPreciseSinglecell2021`
- **Authors:** Tran, Ang (scRNA-seq / genomics domain)
- **Venue:** Nature Communications 2021
- **Relevant projects:** background only (hierarchical autoencoder architecture)

## One-line takeaway

scHPF (single-cell Hierarchical Probabilistic Framework): hierarchical autoencoder for scRNA-seq data that decomposes cells into interpretable latent factors — the hierarchical structure is the only architecturally relevant concept for Sybilion projects.

## Key claims

- Hierarchical autoencoder decomposes single-cell gene expression into cell-level and gene-level latent factors simultaneously.
- Fast and scalable: processes millions of cells via stochastic variational inference.
- Main innovation is in the scRNA-seq domain (sparse count data, dropout noise, zero-inflation) — not directly applicable to financial TS.

## Relevance to P1/P2/P4

Low. The hierarchical decomposition principle (global + local factors) is abstractly relevant to P1's regime sub-clustering (cluster-level factors + series-level factors) and P2's embedding hierarchy (domain-level vs series-level representations), but there are no concrete transferable mechanisms. Background reading only.
