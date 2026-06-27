# CLAUDE.md — Sybilion AI Research Wiki Maintainer

You maintain a Git-backed markdown research wiki for Sybilion's research-heavy AI product features.

The wiki has four project tracks:

1. **P1 — Cluster-pretrained deep models**: scalable SKU forecasting through cluster-routed lightweight deep models.
2. **P2 — Causal embedding model v2**: directed/asymmetric embeddings for fast causal covariate retrieval.
3. **P3 — Scenario engine**: interpretable CPCV-validated scenario queries for procurement and cost forecasting.
4. **P4 — Availability nowcasting graph**: public-first B2B supply-availability nowcast with evidence ledger and explicit provenance graph.

The purpose is to maintain a durable, skeptical, cross-linked research memory that helps the team make product, architecture, model, evaluation, and sequencing decisions.

## Maturity model (IMPORTANT — read first)

This wiki is in an early stage. The current `raw/` corpus is a small set of **starting sources**: five consolidated seed notes (P1–P4 plus a cross-project strategy note), derived from an internal strategy deck and two technical notes. It is **not** the full scope, and it does not yet contain external academic/industrial literature or the production-repo context. The intended workflow is:

1. **seed** — page is built only from the current starting sources. Claims are provisional. This is where almost everything is today.
2. **researched** — external literature and/or additional internal sources have been pulled in, candidate methods have been checked against published work, and citations are attached.
3. **validated** — a Sybilion experiment has produced evidence that moves the claim.

Every content page carries a `stage:` frontmatter field reflecting where it sits. Do not present a `seed` page as if it were `researched` or `validated`. When a page makes a methodological claim that rests on a named external method, treat that method as a **candidate to verify in the literature pass**, not as established fact — record it under "Literature to integrate" rather than asserting it.

Two recurring section types make the scaffold honest and ready for the research pass:

- **Open research questions** — what this page cannot yet answer from current sources.
- **Literature to integrate** — named candidate methods/areas to find, verify, and cite later. Mark each as `[verify]` until a real citation is attached in a `researched`-stage update.

Single-source concept/entity pages are intentionally retained at seed stage as **landing pages** for the literature that will be attached to them later. They are not orphans-by-accident; keep them linked from their project pages and give them research hooks rather than boilerplate.

## Core rules

- `raw/` contains immutable source material. Do not modify raw sources.
- `wiki/` contains the compiled research memory. You may create and update wiki pages.
- The wiki is not a place for polished generic summaries. It is a decision-support system.
- Every important claim should connect to source evidence, applicability, caveats, and decision impact.
- Do not erase superseded claims. Mark them as superseded and link to the newer view.
- Use Git diffs as the human review mechanism.

## Current source corpus

Five seed notes (the sources content pages cite), plus the deck as their upstream origin:

- `raw/seed/p1_cluster-pretrained_deep-models.md` — cluster-pretrained deep models + query-dependent sparse covariate selection. → `src-2026-06-p1-cluster-pretrained-deep-models`
- `raw/seed/p2_causal_embedding_model.md` — causal/asymmetric embeddings for retrieval-speed covariate discovery. → `src-2026-06-p2-causal-embedding-model`
- `raw/seed/p3_forecast_scenario_engine.md` — interpretable CPCV-validated "if-then" scenario forecasting. → `src-2026-06-p3-scenario-engine`
- `raw/seed/p4_availability_nowcasting.md` — hybrid B2B supply-availability nowcast + evidence ledger. → `src-2026-06-p4-availability-nowcasting`
- `raw/seed/px_cross-project_strategy.md` — cross-project comparison, sequencing, decision. → `src-2026-06-px-cross-project-strategy`
- `raw/seed/sybilion_ai_projects_review.pptx` — May-2026 deck; upstream origin of P1/P2/P3/PX. Consolidated into the notes above; not cited directly by content pages. → `src-2026-05-sybilion-ai-projects-review`

## Repository structure
```text
repo-root/
  pyproject.toml          # uv, ruff, mypy, pytest config
  README.md
  .gitignore              # .wiki/ cache, __pycache__, etc.
  .pre-commit-config.yaml
  .agent/
    wiki-context.md
    scale-features-spec.md
    tasks.md              # optional
  src/
    wikitools/            # the package: wikilib + the `wiki` CLI
  tests/
  kb/                     # the knowledge base (was the wiki root)
    CLAUDE.md
    raw/
    templates/
    wiki/                 # stays as-is — index.md, log.md, pages
    .wiki/                  # gitignored DuckDB cache (under kb/)
```

## Wiki dir structure

```text
.../kb/
    raw/
      seed/                              # originating internal source material — not literature
        sybilion_ai_projects_review.pptx   # May-2026 deck (upstream origin of P1/P2/P3/PX)
        p1_cluster-pretrained_deep-models.md
        p2_causal_embedding_model.md
        p3_forecast_scenario_engine.md
        p4_availability_nowcasting.md
        px_cross-project_strategy.md
        README.md                        # what these are, and the note→deck provenance
      literature/                        # Zotero export + PDFs (keyed by citekey)
        library.json                     # Better CSL JSON export — canonical catalog of ALL items
        pdf/
          <citekey>.pdf                  # primary PDF per item
          <citekey>-suppl.pdf            # optional supplementary material
        txt/
          <citekey>.txt                  # extracted text (derived from pdf/, same basename)
          <citekey>-suppl.txt
    
    wiki/
      index.md
      overview.md
      log.md
      projects/
      domains/
        timeseries-forecasting/
        embedding-models/
        scenario-engine/
        nowcasting-graph/
      shared/
      entities/
      concepts/
      sources/
      comparisons/
      decisions/
      experiments/
      queries/
     
    templates/
```

## Literature layout conventions

`raw/literature/` is keyed by **citekey** (from the Better CSL JSON export), flat by type — not by topic. Topic/project association lives in source-page frontmatter, never in paths.

- `library.json` — Better CSL JSON export; the canonical catalog of **all** items. An item's `id` is its citekey.
- `pdf/<citekey>.pdf` — the primary PDF for an item. Supplementary material is `pdf/<citekey>-suppl.pdf`.
- `txt/<citekey>.txt` — extracted text, derived from the matching PDF, sharing the same basename (`<citekey>-suppl.txt` for supplements). Committed (grep/diff-friendly); regenerable by the extractor.
- **Non-PDF items** (web pages, blog posts) are either captured as an HTML→PDF print under the same `<citekey>.pdf` name, or left **metadata-only** — present in `library.json` with no file. An item without a PDF is normal, not an error.
- A citekey is unique within the library and is the join key across `library.json`, `pdf/`, `txt/`, and the `zotero:`/source-page reference. Tools resolve a paper by basename, never by parsing attachment paths.

Use lowercase kebab-case filenames.

Examples:

```text
wiki/projects/p1-cluster-pretrained-deep-models.md
wiki/projects/p2-causal-embedding-v2.md
wiki/concepts/evidence-ledger.md
wiki/decisions/adr-0001-project-sequencing.md
```

Use stable source IDs:

```text
src-YYYY-MM-DD-short-slug
```


## Linking convention

Use portable Markdown links by default.

Good:

- [P1 — Cluster-pretrained deep models](projects/p1-cluster-pretrained-deep-models.md)
- [Temporal generalization](concepts/temporal-generalization.md)
- [ADR-0001](decisions/adr-0001-project-sequencing.md)

Do not use Obsidian-only wikilinks unless explicitly requested:

- [[projects/p1-cluster-pretrained-deep-models]]
- [[Temporal generalization]]

The wiki may be opened in Obsidian, but Git-compatible Markdown is the source format.


## Frontmatter

Every wiki page should begin with YAML frontmatter:

```yaml
---
type: project | domain | source | concept | comparison | decision | experiment | shared | query | entity
domain: timeseries-forecasting | embedding-models | scenario-engine | nowcasting-graph | shared
project: P1 | P2 | P3 | P4 | shared
status: draft | active | needs-review | superseded | archived
stage: seed | researched | validated
confidence: low | medium | high
updated: YYYY-MM-DD
sources:
  - src-YYYY-MM-DD-short-slug
tags: []
---
```

`stage` reflects research maturity (see Maturity model). `confidence` reflects how strongly the page's core thesis is supported *given its stage* — at `seed` stage, `high` confidence should be rare and reserved for claims with direct, unambiguous source support (e.g., customer-interview counts quoted verbatim from the deck).

## Claim format

When recording a claim, distinguish:

- **Claim**: what is being asserted.
- **Evidence**: source or experiment that supports it.
- **Applicability**: when it applies to Sybilion's product/data.
- **Limitations**: when it may fail.
- **Contradictions**: sources or experiments that disagree.
- **Decision impact**: architecture, eval, cost, UX, risk, commercial sequencing.
- **Confidence**: low, medium, high.

## Project-specific guidance

### P1 — Cluster-pretrained deep models

Track:

- cluster routing quality
- shape versus regime mismatch
- regime sub-clustering
- D-Linear versus MLP backbone
- PyTorch integration into forecast pipeline
- serialization and determinism constraints
- FAISS routing index
- zero-shot or minimal fold-in onboarding
- analyst-time elimination as a primary metric
- M5 and VN2 validation
- dependency on P2 causal covariate embeddings

### P2 — Causal embedding model v2

Track:

- directed/asymmetric embedding objectives
- Transfer Entropy and Granger distillation
- pairwise-label sampling strategy
- asymmetric geometry convergence
- top-k causal covariate retrieval
- retrieval latency at 200M-series scale
- ranking metrics and downstream forecasting validation
- data flywheel and defensibility
- interaction with P1 covariate attention

### P3 — Scenario engine

Track:

- CPCV validation
- Granger/TE causal feature selection
- interpretable linear models
- scenario re-run API
- confidence intervals
- optional Bayesian / variational posterior layer
- customer pain and commercial urgency
- Cost Model Forecast PRD and Buy Window visualization
- linear-model ceiling on nonlinear dynamics

### P4 — Availability nowcasting graph

Track:

- public-first source ingestion
- entity normalization
- taxonomy alignment
- event and relation extraction
- evidence ledger
- explicit provenance graph
- mixed-frequency signal fusion
- category × region availability
- supplier × category availability
- score calibration and alert explanations
- why full graph reconstruction is deferred
- expansion path via customs, AIS, and distributor APIs

## Ingest workflow

When asked to ingest a source:

1. Identify source metadata and assign a source ID.
2. Create a page under `wiki/sources/`.
3. Extract important claims and caveats.
4. Update the relevant project page.
5. Update the relevant domain thesis page.
6. Create or update concept pages only for concepts likely to be reused.
7. Update decisions and experiments if the source changes what should be done next.
8. Update `wiki/index.md`.
9. Append a concise entry to `wiki/log.md`.

Do not over-create pages. Prefer a small number of high-signal pages over many thin pages.

## Query workflow

When answering a research question:

1. Read `wiki/index.md`.
2. Read the relevant project, domain, concept, decision, and experiment pages.
3. Answer from the wiki first.
4. State if the wiki is insufficient.
5. File durable synthesis under `wiki/queries/` when useful.
6. Update relevant pages when the answer changes the research memory.

## Extract workflow

`wiki extract` populates `raw/literature/txt/` with one `.txt` per PDF in `raw/literature/pdf/`. It is idempotent: rerunning skips files whose source hash is unchanged. A sidecar `<stem>.extract.json` records the extractor name, version, and the hash of the source PDF.

**Engines:**

| Engine | Requires | Output | When to use |
|---|---|---|---|
| `docling` | `[ocr]` extra | Markdown + `$$…$$` LaTeX fences | **Default** when [ocr] installed; preserves math |
| `fast` | `pdftotext` (system) | Plain text | Fast; math becomes unreadable glyph sequences |
| `marker` | `[ocr]` extra | Markdown | Not yet implemented |

**Engine resolution:** When `--engine` is not specified, `wiki extract` uses `docling` if the `[ocr]` extra is installed; otherwise falls back to `fast` with a stderr warning that math will be degraded.

**PDF is the authority for exact math.** The `.txt` file captures math as a LaTeX fence (`$…$` / `$$…$$`) when extracted with docling — treat these as pointers back to the PDF, not authoritative source. For any claim that depends on exact notation, re-read the original PDF.

**Commands:**

```
wiki extract                             # extract all PDFs (docling if available, else fast)
wiki extract --engine fast               # force plain-text extraction
wiki extract --engine docling            # force docling (requires [ocr] extra)
wiki extract --force                     # re-extract even when hash is unchanged
wiki extract --citekey smithExact2024    # extract only PDFs for this citekey
wiki extract --json                      # emit structured JSON output
```

Reconciliation runs first on every invocation and reports:
- `pdf-missing-from-library` — a PDF in `raw/literature/pdf/` has no entry in `library.json`
- `txt-missing` — a PDF has no extracted `.txt` (cleared once you run `wiki extract`)

Reconciliation issues are reported but do not abort extraction. Library-only items (no PDF) are intentionally metadata-only and are not flagged.

After running `wiki extract`, commit the `raw/literature/txt/` files (both `.txt` and `.extract.json` sidecars). They are derived-but-stable, useful in diffs and grep, and both are tracked by git.

## TOC workflow

`wiki/index.md` and `wiki/domains/*/index.md` contain **generated regions** fenced by:

```
<!-- AUTO:start -->
...generated content...
<!-- AUTO:end -->
```

**Rules:**
- Human prose lives **outside** the AUTO fences. Edits inside the fences are overwritten on the next `wiki toc build` run.
- `wiki/index.md` keeps the project-tracks table and any human intro above the AUTO region; the AUTO region contains the domain summary table, shared pages list, and total count.
- Domain index files (`wiki/domains/<domain>/index.md`) are created on first run if absent. The AUTO region contains the full page catalog table for that domain.

**Commands:**

```
wiki toc build             # regenerate; idempotent (no-op if up-to-date)
wiki toc build --check     # exit non-zero if stale (CI staleness guard)
```

`wiki toc build --check` is the CI guard: run it in CI after any page addition or frontmatter change to verify that committed indexes are current.

After ingesting a new source or adding pages, run `wiki toc build` and commit the updated index files alongside the content changes. Domain set is derived dynamically from `domain:` values in frontmatter — new domains appear in the indexes without any code change.

## Lint workflow

Run automated lint via the `wiki` CLI before committing or when asked to lint:

```
wiki lint [--json] [--fix] [--severity error|warn]
```

- Non-zero exit if any **error** is found (blocks commit via pre-commit hook).
- `--json` emits a stable, machine-readable report.
- `--fix` applies safe auto-fixes only: strips broken Markdown links and normalises
  frontmatter key order. Never rewrites prose or claims.
- `--severity error` suppresses warnings and shows errors only.

**Errors** (block commit):
- Broken Markdown links (`](target.md)` does not resolve to a file).
- Frontmatter schema violations: missing required keys, invalid enum values, bad date.
- Dangling `sources[]` entries with no matching `wiki/sources/<id>.md` page.
- `[verify]` markers remaining on a `stage: researched` page.

**Warnings** (reported, do not block):
- Orphan pages (0 inbound links, excluding nav roots).
- `stage: seed` + `confidence: high` combination.
- Provenance gaps: claim-bearing pages with no `sources[]`, or source pages with no
  resolvable raw path or `zotero:` key.
- Thin or boilerplate page bodies.
- Citekey integrity: mismatched `zotero:` keys vs `library.json`; PDFs missing `.txt`.
- Pages unreachable from `index.md` via link traversal.
- Near-duplicate titles (Jaccard ≥ 0.70).

When asked to lint manually:

1. Run `wiki lint` and review the report.
2. Run `wiki lint --fix` to apply safe fixes.
3. Address errors before committing; flag warns for human review.
4. Update `wiki/index.md` and `wiki/log.md` if the fixes change structure.

## Style

Be precise, skeptical, and concise.

Prefer tables for tradeoffs, project comparisons, assumptions, and risks.

Prefer explicit uncertainty over false confidence.

Keep the wiki oriented around decisions, experiments, assumptions, and reusable synthesis.
