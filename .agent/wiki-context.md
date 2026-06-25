# Wiki Tooling — Project Context

Read this before implementing anything in `scale-features-spec.md`. It explains *what the
wiki is, why it exists, and the constraints you must respect*. The spec says what to build;
this says what you're building it for.

---

## What this repository is

A **research wiki**: an LLM-maintained, durable, cross-linked knowledge base about a set of
AI research projects (P1–P4, see below). It follows the Karpathy "LLM wiki" pattern — the
LLM incrementally builds and maintains a persistent wiki from sources, instead of retrieving
raw chunks from scratch on every question. Knowledge is *compiled once and kept current*.

Three layers:
- `raw/` — **immutable** source material. Never edited by the wiki. Two buckets:
  `raw/seed/` (originating internal notes/deck) and `raw/literature/<citekey>/` (papers from
  Zotero, keyed by Better BibTeX citekey, with `library.json` as the canonical item catalog).
- `wiki/` — LLM-generated markdown pages (projects, concepts, experiments, sources, domains,
  comparisons, entities, shared). Cross-linked with `[[wikilinks]]`, YAML frontmatter on every
  page, Obsidian-compatible.
- `CLAUDE.md` — the schema: structure rules, page types, claim format, maturity model,
  ingest/query/lint workflows. **Authoritative — read it first.**

## Why it exists (the goal)

To support decisions on a real AI product roadmap by turning scattered sources + external
literature into auditable, skeptical, reusable knowledge. The wiki is decision-support, not a
summary dump: every page carries claims with evidence, limitations, contradictions, and a
confidence/stage marker. Quality bar: **faithful to sources, skeptical, no filler.**

## Maturity stage (important)

The wiki is at **`seed`** stage — built from a few starting sources, awaiting a literature
research pass. Pages carry `stage: seed|researched|validated`. Candidate methods are marked
`[verify]` until a real citation is attached. You are not doing the research pass; you are
building the **tooling that makes it viable at scale** (hundreds of sources).

---

## The projects the wiki covers (just enough to recognize terms)

| ID | Domain | One line |
|----|--------|----------|
| P1 | timeseries-forecasting | Cluster-pretrained deep forecasting models + query-dependent sparse covariate selection (hierarchical α-entmax). |
| P2 | embedding-models | Causal/asymmetric time-series embeddings for retrieval-speed covariate discovery (replacing O(n²) Granger/TE). |
| P3 | scenario-engine | Deterministic, interpretable "if-then" scenario forecasting with confidence bounds. |
| P4 | nowcasting-graph | Public-first supply-availability nowcast + provenance-backed evidence ledger + lightweight evidence graph. |

You don't need to understand the science — but the tooling reads `domain:`/`project:`
frontmatter and these are the values it will see.

---

## Why this work now (the problem being solved)

The wiki will grow to **several hundred PDF sources**. The original pattern assumes the agent
reads `index.md` to navigate — that breaks past ~100 sources. The architecture (markdown +
git) stays; we add a **retrieval + maintenance layer** over the same files. Four features
(full detail in `scale-features-spec.md`):

1. **Retrieval** — PDF→text extraction + hybrid lexical (BM25) + semantic (local-embedding
   cosine) search in one DuckDB file. The scale unlock; the agent searches instead of reading
   the index.
2. **Idempotent / claim-check ingest** — re-ingest converges (no duplicate pages); advisory
   dedup keyed on citekey kills semantic-duplicate claims.
3. **Scripted lint** — automated health checks (broken links, orphans, frontmatter, thin
   pages, provenance, stage sanity) for pre-commit/CI.
4. **Split index** — generated multi-level index (root + per-domain) so navigation stays
   cheap.

---

## Hard constraints (non-negotiable)

- **The architecture does not change.** No server, no GUI, no online service, no external
  vector DB. Everything is local files + one rebuildable DuckDB. `raw/` stays immutable.
- **Deterministic by default.** Identical inputs → identical outputs. Stable sort orders.
  Local embedding model with fixed weights (not an API whose results drift). Seed any
  randomness. Determinism is a tested property, not an aspiration.
- **House style:** Python 3.12+, `uv` + `pyproject.toml`, fully typed (`mypy`), `ruff`
  format+check, `pytest`. QA loop before every commit:
  `uv run ruff format . && uv run ruff check . --fix && uv run mypy . && uv run pytest`.
- **One CLI, subcommands** (`wiki lint|toc|extract|index|search|check`), all with `--json` for
  agent use. Shared logic lives in `wikilib` — do not duplicate frontmatter parsing.
- **Build artifacts placement:** code in `tools/`; rebuildable caches in `.wiki/`
  (gitignored); extracted PDF text committed beside its PDF in `raw/literature/<citekey>/`.
- **Every feature updates `CLAUDE.md`** to document its tool so the agent discovers and uses
  it by default — and Features 1–2 update the research-pass prompt to call `wiki search` /
  `wiki check` instead of reading the index.
- **One feature = one reviewable commit.** Build order: `wikilib` → lint → toc → retrieval →
  ingest-check. Cheap-and-validating first; the dependency reason is in the spec.

## Definition of done (per feature)

Acceptance criteria in the spec pass; QA loop clean; `CLAUDE.md` updated; runs correctly
against the actual wiki in this repo (not a toy fixture); determinism test included.

## When in doubt

Prefer fewer high-signal pages and simpler tools over cleverness. If a choice trades away
determinism, auditability, or the immutability of `raw/`, it's the wrong choice — stop and
flag it rather than proceeding.
