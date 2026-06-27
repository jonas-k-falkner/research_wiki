---
type: shared
domain: shared
project: shared
status: active
confidence: high
stage: seed
updated: 2026-06-25
sources:
  - src-2026-06-px-cross-project-strategy
  - src-2026-06-p1-cluster-pretrained-deep-models
  - src-2026-06-p4-availability-nowcasting
tags:
  - log
---

# Log

## 2026-06-22

- Ingested `raw/seed/sybilion_ai_projects_review.pptx` as P1–P3 strategic project source.
- Ingested `raw/seed/p1_cluster-pretrained_deep-models.md` as P1/P2 sparse covariate-selection design note.
- Ingested `raw/seed/p4_availability_nowcasting.md` as P4 nowcasting/evidence-ledger graph source.
- Created four project pages: P1, P2, P3, P4.
- Created four domain thesis pages.
- Created shared project map, evaluation strategy, risks/caveats, and open questions.
- Created ADR-0001 for project sequencing.
- Created initial experiment pages for P1–P4.
- Updated `CLAUDE.md` to reflect the four-project wiki structure.

### Needs review

- Confirm whether P4 should be a first-class project track or a research-adjacent domain.
- Confirm whether P3 Bayesian uncertainty is v1 or v2.
- Assign owners for P1 cluster-quality gate and P2 causal embedding research.

## 2026-06-22 (lint + seed-hardening pass)

Ran the `CLAUDE.md` lint workflow against the initial ingest and fixed structural/depth issues, keeping everything explicitly at **seed** stage (scaffold for later literature research, not final scope).

### Lint findings

- Concept pages carried identical boilerplate ("Current view" / "Decision impact") — violated the no-generic-summaries rule.
- Experiment pages were stubs ("Protocol: TBD", identical failure modes); the P1 gate protocol present in the source deck (Slide 3) was under-extracted.
- Source pages were dead-ends (0 inbound links) — provenance trail unwalkable.
- One concept page (`cluster-pretrained-deep-models`) was a true orphan, not linked from its own project.
- Contradiction/superseded machinery unused despite the schema; the P3 Bayesian v1/v2 source-internal inconsistency was silently smoothed.
- Missing structures the schema declares: no comparison page (despite the deck's six-dimension matrix), no entities, no research backlog.
- Corpus gap: production-repo context not ingested, so architecture claims (Model ABC, determinism) can't be checked.
- `confidence` near-uniform `medium` and decorative; B2B source page missing `Date`.

### Fixes applied

- Added a **maturity model** (`seed`/`researched`/`validated`) and a `stage:` frontmatter field on every page; all pages marked `stage: seed`.
- Rewrote all **8 concept pages**: real definitions, "Open research questions", "Literature to integrate" (candidate methods marked `[verify]`), cross-project relevance, inline source links.
- Rewrote all **4 experiment pages**: extracted real protocols (P1 gate now carries the full Slide-3 protocol + low/high-variance decision rule), project-specific failure modes, metrics, `[seed gaps]` to specify, research hooks.
- Fixed provenance: project/domain pages now link their **source pages inline** (sources went from 0 inbound to 11/7/5).
- Recorded contradictions: P3 Bayesian v1/v2 (source-internal); P1 determinism-vs-MC-dropout (cross-layer, pending repo ingest).
- Created `comparisons/portfolio-evaluation.md` (deck matrix + derived P4 row), `entities/p4-public-data-sources.md`, and `shared/research-backlog.md` (planned literature + internal sources + known tensions + contradiction status).
- Added numbering crosswalk to `overview.md`; seed banners on `index.md`/`overview.md`; added `Date` to the B2B source page.
- Verified: **0 broken wikilinks**; only `index.md`/`log.md` remain without inbound links (correct — they are nav roots).

### Still open (for the research pass, tracked in [shared/research-backlog](shared/research-backlog.md))

- Attach real citations to every `[verify]` item; promote pages `seed → researched`.
- Ingest `forecast_pipeline` / `embedding_model` / deployment / product context to ground architecture claims and resolve the determinism carve-out.
- Set numeric thresholds for the P1 gate; assign experiment owners.

## 2026-06-25 (finalize — source layer + ref sync)

Finalized the seed KB as a clean starting point for the research pass.

### Structure & sources
- Reconciled `wiki/sources/` with the five-note `raw/seed/` corpus. Source pages now: P1, P2,
  P3, P4, PX — one per seed note. Created P2, P3, PX; rewrote P1 (now consolidates the cluster
  models + the gaze covariate-selection content); renamed P4.
- The May-2026 deck is retained as the **upstream origin** (`src-2026-05-...`), consolidated
  into the five notes and no longer cited directly by content pages.
- Fixed the malformed `src-2026-06-p4.md` source ID (dropped the `.md`).

### Reference remap (deterministic, by project)
- `gaze` → P1 source (content folded into the P1 note).
- deck → per-project source (P1/P2/P3) or PX (shared); `src-2026-06-p4(.md)` → P4 source.
- Applied to frontmatter `sources:` and inline links; deduped sources lists.

### Verification
- 0 broken Markdown links; 0 orphan pages (only `index.md`/`log.md` nav roots lack inbound).
- Source IDs consistent across all pages; `updated` bumped to 2026-06-25.
- Added `raw/seed/README.md`; updated `CLAUDE.md` corpus + structure; updated `index.md`
  source summaries.

### Still seed-stage (for the research pass)
- All pages remain `stage: seed`; `[verify]` literature unattached; production-repo context
  (`forecast_pipeline`, `embedding_model`) not yet ingested — tracked in
  [shared/research-backlog](shared/research-backlog.md).

## 2026-06-27 (ingest — TSF literature review, deep-research synthesis)

Ingested a deep-research synthesis of 2024–2026 time-series forecasting literature, read against P1.

### Provenance call (important)
- Classified as a **secondary synthesis, `[verify]`-tier**: it names real primaries (TimeXer, Channel Clustering, DUET, ChronosX, UniCA, ApolloPFN, CATS-ATS, CauAir, …) but **carries no resolvable citations**. Ingest did **not** promote any page `seed → researched`. Pages remain `seed`; all added claims are attributed to the synthesis and marked `[verify]` against the named primaries.

### Added
- `raw/research/deep-forecaster-tsf-review-2026.md` (new `raw/research/` bucket).
- Source page `sources/src-2026-06-tsf-literature-review.md` with explicit evidence-tier framing.

### Distilled into
- `concepts/cluster-pretrained-deep-models` — Channel Clustering → DUET as best-supported lineage; "simple backbone, spend budget on selector"; no residual bypass.
- `concepts/hierarchical-entmax-covariate-selection` — calibration: entmax support in TSF is **adjacent, not direct** (seed note overstated it); cluster-level attribution is an open opportunity.
- `concepts/causal-covariate-embeddings` — TimeXer validates asymmetric target/covariate modeling; shared-encoder-for-target-conditioned-routing is unmatched (novelty point).
- `domains/timeseries-forecasting/thesis` — two-stream framing; TSFMs are background, not center. (Also fixed a duplicated source link.)
- `projects/p1-cluster-pretrained-deep-models` — external-literature positioning; **moat tension updated with first non-self-assessed support** (no 2024–2026 paper solves P1's exact combination), caveated as sympathetic secondary synthesis. (Also fixed a duplicated source link.)
- `comparisons/portfolio-evaluation` — partial answer to the P1/P2 moat question.
- `shared/research-backlog` — P1/P2 literature rows upgraded from vague areas to **named, venue-tagged primaries**; logged as a completed deep-research step.

### Next (tracked in research-backlog)
- Export the named primaries from Zotero into `raw/literature/`, then verify each claim against the primary source before any `seed → researched` promotion.
