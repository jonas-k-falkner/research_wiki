---
type: source
domain: timeseries-forecasting
project: P1
status: active
confidence: medium
stage: seed
updated: 2026-06-27
sources:
  - src-2026-06-tsf-literature-review
tags:
  - literature-review
  - deep-research
  - forecasting
  - covariate-selection
---

# Source: TSF literature review (deep-research synthesis, Jan 2024–mid 2026)

## Metadata

- Source ID: `src-2026-06-tsf-literature-review`
- Raw path: `raw/research/deep-forecaster-tsf-review-2026.md`
- Source type: **deep-research synthesis** (secondary) — reviews TSF literature against the P1 design
- Date: June 2026
- Relevant projects: P1 (covariate layer relevant to P2)

## Provenance & evidence tier (read first)

This is a **secondary synthesis**, not primary literature. It names real, checkable papers but
**carries no resolvable citations** — its `citeturn…` markers are the research tool's internal
handles, not links/DOIs. Therefore its paper-level claims are **`[verify]` against the named
primaries**: ingesting it does **not** promote any page to `stage: researched`. It is a
high-quality *map of what to verify*. The named primaries are pending export into
`raw/literature/` (from Zotero) and primary-source confirmation. The report itself flags
uncertainty (approximate citation counts; ApolloPFN not archival; several 2026 works too new).

It is also written *for* the P1 architecture, so it reads the field sympathetically toward P1 —
weigh its novelty/moat conclusion accordingly.

## Key claims (all `[verify]` against named primaries)

| Claim | Named evidence | Decision impact | Confidence |
|---|---|---|---|
| Asymmetric target/covariate modeling is a validated, successful pattern. | TimeXer (NeurIPS 2024) — endogenous/exogenous split + bridge token. | Supports P1 covariate layer and P2 asymmetric objective. | medium |
| Cluster-first handling of correlated channels is the best-supported piece of the P1 design. | Channel Clustering / "From Similarity to Superiority" (NeurIPS 2024); DUET (KDD 2025, dual clustering + soft-cluster + sparsification). | Supports cluster-then-feature routing over flat feature routing. | medium |
| TS foundation models are background, not the center for covariate selection. | ChronosX, UniCA, ApolloPFN all exist *because* leading TSFMs ignore/adapt poorly to covariates. | TSFMs are baselines/backbones to adapt, not blueprints. | medium |
| Keep the backbone simple; spend the modeling budget on the covariate selector. | "A Closer Look at Transformers for TSF" (ICML 2025); linear-baseline wave. | De-risks P1 — no exotic backbone needed. | medium |
| Routing weights are not faithful importance. | "Attention is not Explanation" / "…not not Explanation" debate. | Confirms weight×gradient + cluster aggregation + stability over raw attention. | medium |
| Avoid a residual bypass around the selector. | Design inference from the "A Closer Look" skip-connection finding (report's own inference, not a direct recommendation). | Supports P1's no-residual-bypass choice. | low |

## The gap it confirms (decision-relevant)

No 2024–2026 top-venue paper combines query-dependent sparse exogenous selection + hierarchical
cluster→feature gating + α-entmax/hard-concrete covariate gating + cluster-level attribution +
diversity regularization + MC-dropout selection stability. So P1's *combination* is a
still-distinct direction, not a crowded incremental niche. This is the **first non-self-assessed
support** for the deck's "very high moat" rating — but it is a sympathetic secondary synthesis,
not a systematic survey, so treat as medium confidence.

## Calibrations / tensions vs. seed notes

- α-entmax / hard-concrete support in TSF is **adjacent, not direct** — the strong covariate/
  clustering papers use attention, soft clustering, or adapters, not entmax gates. The seed note
  slightly overstated entmax as literature-backed.
- The "shared encoder for both targets and covariates, trained independently of the head, then
  used for target-conditioned sparse routing" is **not matched by any flagship paper** — a real
  novelty point.

## Named primaries to export & verify

TimeXer · Channel Clustering ("From Similarity to Superiority") · DUET · ChronosX · UniCA ·
ApolloPFN · CATS-ATS · CauAir · (context/baselines: iTransformer, TimeMixer, Chronos, Moirai,
TimesFM, Time-MoE, Sundial, Timer; "A Closer Look at Transformers for TSF"; the attention-
faithfulness pair). Pending Zotero export into `raw/literature/`.

## Updated pages

- [projects/p1-cluster-pretrained-deep-models](../projects/p1-cluster-pretrained-deep-models.md)
- [concepts/cluster-pretrained-deep-models](../concepts/cluster-pretrained-deep-models.md)
- [concepts/hierarchical-entmax-covariate-selection](../concepts/hierarchical-entmax-covariate-selection.md)
- [concepts/causal-covariate-embeddings](../concepts/causal-covariate-embeddings.md)
- [domains/timeseries-forecasting/thesis](../domains/timeseries-forecasting/thesis.md)
- [comparisons/portfolio-evaluation](../comparisons/portfolio-evaluation.md)
- [shared/research-backlog](../shared/research-backlog.md)
