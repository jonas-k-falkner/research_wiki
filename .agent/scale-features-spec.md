# Wiki Scale Features — Build Spec

Scope for four capabilities that keep the file-based research wiki viable from ~3 to
several hundred sources. Written to be handed to a Claude Code agent one feature at a
time. Each feature is a self-contained PR with its own acceptance tests, in the build
order given below.

The guiding principle from the design discussion: **the markdown-in-git architecture does
not change — we add a retrieval/maintenance layer over the same files.** Nothing here
introduces a server, a GUI, or an online dependency. Every artifact produced is local and
rebuildable from the wiki + `raw/`.

---

## 0. Shared foundation & conventions (build first)

Before the four features, build the small shared library they all depend on. Do not
duplicate frontmatter parsing or page enumeration across features.

### `wikilib` — internal support library

A typed Python module providing the primitives every feature reuses:

- `iter_pages(root) -> Iterator[Page]` — enumerate all `wiki/**/*.md`, parse YAML
  frontmatter + body, expose `path`, `type`, `domain`, `project`, `status`, `stage`,
  `confidence`, `updated`, `sources: list[str]`, `tags`, `title`, `body`.
- `iter_links(page) -> Iterator[Link]` — extract **portable Markdown links** (`](target.md)`
  / `](target.md#anchor)`), resolve each to a path or `None`. (The wiki uses Markdown links,
  not Obsidian wikilinks — see `kb/CLAUDE.md`.)
- `load_library(raw/literature/library.json) -> dict[citekey, Item]` — parse the
  Better CSL JSON export; expose `id` (citekey), DOI, title, authors, year, abstract.
- `pdf_path(citekey) -> Path | None` and `txt_path(citekey) -> Path | None` — resolve
  `raw/literature/pdf/<citekey>.pdf` / `txt/<citekey>.txt` by basename (also `-suppl`
  variants); return `None` when absent (metadata-only items are normal).
- `content_hash(path) -> str` — stable SHA-256 of normalized content (for idempotency).
- `inbound_links(pages) -> dict[path, set[path]]` — the link graph (used by lint, toc,
  retrieval graph-expansion).

### House style (match the existing Python repos)

- Python 3.12+, `uv` + `pyproject.toml`, fully typed (`mypy`), linted/formatted (`ruff`).
- Deterministic by default: identical inputs → identical outputs; any randomness explicitly
  seeded; stable sort orders in all output.
- No hidden global state; file I/O confined to clearly-named functions.
- `pytest` with unit + a small integration test per feature; cover empty/missing/malformed
  inputs and determinism.
- QA loop before every commit: `uv run ruff format . && uv run ruff check . --fix &&
  uv run mypy src && uv run pytest tests/unit` (targets `src/` and `tests/` only — never `kb/`).

### One CLI, several subcommands

Expose everything through a single entry point `wiki` (the `src/wikitools/` package, a
uv console script). Subcommands introduced by the features below:
`wiki lint`, `wiki toc`, `wiki extract`, `wiki index`, `wiki search`, `wiki check`.

Every subcommand supports `--json` for agent consumption and prints human-readable output
by default. Exit non-zero only where specified (lint errors, check failures).

### Where artifacts live

- Code: `src/wikitools/` (repo-root `pyproject.toml`, uv-managed).
- Rebuildable caches/DBs: `kb/.wiki/` (gitignored) — never committed, always regenerable.
- Extracted PDF text: committed under `raw/literature/txt/<citekey>.txt` (derived-but-stable,
  useful in diffs and grep; same basename as the PDF, `-suppl` variants included).

### Build order

1. `wikilib` foundation (this section)
2. **Feature 3 — Lint** (cheapest, validates the corpus, no extraction needed)
3. **Feature 4 — Split index generator** (shares frontmatter reading with lint)
4. **Feature 1 — Retrieval layer** (the actual scale unlock; biggest)
5. **Feature 2 — Idempotent / claim-check ingest** (leans on Feature 1's search)

Each is one reviewable commit. Each must update `CLAUDE.md` to document its tool so the
agent knows the capability exists, and (Features 1–2) update the research-pass prompt.

---

## Feature 1 — Retrieval layer

### Goal

Replace "agent reads `index.md` to know where everything is" with a search tool over both
the wiki pages and the full text of the literature PDFs. This is the single capability
that the ~100-source navigation ceiling demands.

### Scope

Two parts:

**1a. PDF text extraction (ingest-time, cached, idempotent).**
For each PDF in `raw/literature/pdf/` (`<citekey>.pdf` and any `<citekey>-suppl.pdf`),
extract to `raw/literature/txt/<basename>.txt`. Default extractor: `pdftotext` (poppler-utils)
— fast, deterministic, sufficient for text-based papers. Provide `--engine docling|marker`
as an opt-in fallback for scanned/figure-heavy PDFs (heavier deps, off by default). Skip
re-extraction when a stored source hash matches (idempotent). Record extractor + hash in a
sidecar `txt/<basename>.extract.json`.

Layout rules the extractor must respect:
- Resolve papers by **basename = citekey**, never by parsing attachment paths from `library.json`.
- Supplements share the citekey with a `-suppl` suffix (`<citekey>-suppl.pdf` → `-suppl.txt`).
- **Metadata-only items** (in `library.json` with no PDF — e.g. web pages not printed to PDF)
  are normal: skip them, do not error.

**Reconciliation check (run first, surfaces rename/sync mistakes).** Before extracting, verify:
every `pdf/` basename maps to a citekey present in `library.json`; every `library.json` item
either has a `pdf/<citekey>.pdf` or is intentionally metadata-only; every `pdf/` has a current
`txt/`. Emit a clean error list (`--json`) rather than failing silently — this turns a
mis-renamed PDF into a reported gap. (Lint also runs this; see Feature 3.)

**1b. Search index + query (hybrid lexical + semantic).**
Chunk and index: wiki pages by heading section; extracted PDF text by ~800-token windows
with ~100-token overlap. Each chunk stores `(source_path, citekey|None, page|section, text,
embedding)`. Two ranking signals, fused:

- **Lexical** — DuckDB FTS (BM25). Anchors on exact technical terms and citekeys.
- **Semantic** — an `embedding FLOAT[N]` column in the *same* DuckDB file, populated at
  index-build time by a local embedding model, queried with the built-in
  `array_cosine_similarity` function (brute-force scan — no extension, no HNSW). At this
  corpus size (~hundreds of papers → low-tens-of-thousands of chunks) brute-force cosine is
  sub-second; HNSW/`vss` is unnecessary and its persistence is still experimental.

`wiki search` runs both and fuses with **reciprocal-rank fusion (RRF)**. Rationale: claim
text is often paraphrase ("preserves directional influence" ↔ a paper saying "asymmetric
causal relation"), which semantic catches; lexical anchors exact terms. Fused beats either
alone for "find the N papers bearing on this claim."

**Embedding model.** Default to a **local** model (`fastembed` ONNX, or
`sentence-transformers` e.g. `bge-small-en`, 384-dim) — free, offline, keeps papers on the
machine, deterministic given fixed weights (preserves the house determinism rule). The
chosen dimension fixes the `FLOAT[N]` column width. An API model (OpenAI
`text-embedding-3-small`, Voyage) is a documented opt-in for higher quality at the cost of an
external dependency and weaker reproducibility; not the default.

### Non-goals

No server, no web UI, no online API, no separate vector database (OpenSearch et al. are
overkill at this scale — one DuckDB file holds both lexical and vector). Not a replacement
for `library.json` (that remains the canonical item catalog). DuckDB does not generate
embeddings — the local model does; DuckDB stores and searches them.

### Upgrade path (do NOT build now)

Add the `vss` HNSW index only if the corpus grows past ~100k chunks and brute-force cosine
becomes a measurable bottleneck. Do not enable `hnsw_enable_experimental_persistence` before
then — it has no incremental updates and re-serializes the whole index per checkpoint. Until
that threshold, brute-force is the correct, deterministic choice.

### CLI contract

```
wiki extract [--engine pdftotext|docling|marker] [--force] [--citekey X]
    # populate/refresh raw/literature/txt/<basename>.txt; idempotent by hash; runs reconciliation first

wiki index build [--embedder local|openai] [--model NAME]
    # full (re)build of .wiki/corpus.duckdb: chunk, FTS, AND embed every chunk
wiki index update           # incremental: only changed pages/PDFs (by mtime+hash), re-embed those
wiki index status           # counts: pages, chunks, PDFs indexed, embed model/dim, last build

wiki search "QUERY" [--scope wiki|lit|all] [--k 10] [--project P1] \
    [--type concept|source|...] [--mode hybrid|lexical|semantic] [--json]
    # hybrid (default) = RRF fusion of BM25 + cosine; returns ranked hits:
    #   path, citekey, section/page, score, snippet
    # --json emits a stable list the agent consumes instead of reading index.md
```

### Implementation notes

- Chunking and tokenization deterministic; char-based windows acceptable if a tokenizer adds
  an unwanted dependency.
- Lexical: DuckDB `fts` extension, BM25; stable tie-break by `(path, chunk_index)`.
- Semantic: store `embedding FLOAT[N]`; query via `array_cosine_similarity(embedding, $q)`
  `ORDER BY ... LIMIT k` — no `vss` extension, no HNSW. Embedding done once at index time,
  cached in the DB; re-embed only changed chunks on `update`.
- Fusion: reciprocal-rank fusion of the two ranked lists (single documented function,
  configurable k constant). Optional source-overlap/Markdown-link graph bonus on top — borrow
  nashsu's source-overlap signal — kept in the same scoring function.
- Keep the embedder behind a small interface (`embed(texts) -> vectors`) so local/API/model
  swaps don't touch the index code.

### Outputs & locations

- `raw/literature/txt/<basename>.txt` + `txt/<basename>.extract.json` (committed)
- `.wiki/corpus.duckdb` (gitignored, rebuildable — holds chunks, FTS, embeddings)

### Dependencies

`poppler-utils` (system, `pdftotext`), `duckdb` (python), `fastembed` *or*
`sentence-transformers` for local embeddings. docling/marker and API embedders optional.

### Acceptance criteria

- `wiki extract` produces a `.txt` per text PDF; rerun with no changes makes zero writes;
  `--force` re-extracts.
- `wiki index build` chunks, FTS-indexes, and embeds; `wiki index status` reports model + dim.
- `wiki search "entmax" --json` (hybrid) returns the entmax concept page and matching paper
  chunks, ranked, with resolvable paths; `--mode semantic` finds a paraphrased claim that has
  no exact term overlap (semantic-recall test); `--mode lexical` finds an exact citekey.
- `wiki index update` after touching one page reprocesses and re-embeds only that page.
- Identical DB + query → byte-identical `--json` (determinism test; local embedder fixed).
- A PDF that fails extraction is logged, skipped, non-fatal.

### Effort

Medium-large. The biggest of the four; split 1a and 1b into two commits if helpful.

---

## Feature 2 — Idempotent / claim-check ingest

### Goal

Prevent the semantic-duplication failure mode at scale (two passes writing the same fact
in different words, both merging cleanly in git) and make re-ingesting a source converge
instead of accreting. Keyed on the stable citekey identity.

### Scope

**2a. Idempotent source ingest.**
Each source maps to exactly one `wiki/sources/src-*.md` page carrying `zotero: <citekey>`
and `source_hash: <hash>` in frontmatter. Ingesting a citekey that already has a page is an
**update in place**, never a second page. If `source_hash` matches the current source, the
ingest is a no-op (zero diff). Re-ingesting the whole corpus in any order converges to the
same state.

**2b. Claim-check (advisory dedup).**
Before the agent writes a claim onto a concept/project page, it can ask whether the corpus
already states it. Returns existing similar claims with locations and similarity, keyed on
`(citekey, claim)`. Same fact from the **same** source already present → update, don't
duplicate. Same fact from a **different** source → legitimate additional support: merge into
one claim with multiple `sources[]`, don't create a parallel claim. The tool advises; the
agent decides per `CLAUDE.md` confidence tiers (it does not auto-merge).

### Non-goals

No automatic claim merging or rewriting (human/agent judgment, per schema). No NLP claim
extraction — operates on claim text the agent supplies.

### CLI contract

```
wiki check source --citekey X [--json]
    # → existing src page path + whether source_hash matches (no-op vs update) vs new

wiki check claim "CLAIM TEXT" [--citekey X] [--page concepts/foo.md] [--json]
    # → ranked existing claims that may duplicate it: location, snippet, similarity,
    #   and whether they already cite citekey X
```

### Implementation notes

- Similarity: lexical first (FTS query against Feature 1's index, or trigram/token overlap)
  — deterministic and cheap. If the optional semantic index exists, offer `--semantic`.
- `wiki check source` computes `content_hash` of the raw source and compares to the page's
  `source_hash`; emits one of `{new, unchanged, changed}` so the ingest harness can branch.
- Provide a thin ingest wrapper (or document the sequence in the research-pass prompt) that:
  resolve src page → if `unchanged` stop → else update + rewrite `source_hash` → append a
  parseable `log.md` entry keyed by citekey so re-runs are detectable.

### Dependencies

Reuses Feature 1 search; otherwise `ripgrep` + stdlib.

### Acceptance criteria

- Re-running ingest on an unchanged source yields zero git diff (true idempotency test).
- Two source pages can never share a citekey (collision → in-place update).
- `wiki check claim` surfaces a known duplicated claim's existing location; a genuinely new
  claim returns no high-similarity hits.
- A claim supported by a second source is reported as "extend `sources[]`," not "new claim."

### Effort

Small-medium (leans on Feature 1).

---

## Feature 3 — Scripted lint

### Goal

Turn the manual health checks (the ones run by hand during the seed-hardening pass) into an
automated lint that scales past eyeballing, runnable in pre-commit and CI.

### Scope — checks (severity: error blocks commit, warn reports)

- **Broken links** — every portable Markdown link `](target.md)` resolves to a file. *(error)*
- **Frontmatter schema** — required keys present (`type, status, stage, confidence, updated,
  sources`); valid enum values; valid YAML; `updated` is a date. *(error)*
- **Dangling `sources[]`** — every frontmatter source id has a matching `src-*` page. *(error)*
- **`[verify]` on researched pages** — a page marked `stage: researched` must have no
  remaining `[verify]` markers. *(error)*
- **Orphans** — pages with 0 inbound links, excluding nav roots (`index.md`, `log.md`,
  domain indexes). *(warn)*
- **Stage/confidence sanity** — `stage: seed` + `confidence: high` flagged for review. *(warn)*
- **Provenance** — claim-bearing pages have ≥1 `sources[]` and link their source page inline;
  source pages have a resolvable raw path + `zotero` key. *(warn)*
- **Thin / boilerplate pages** — body below a length threshold or matching known boilerplate
  phrases (catches filler regressions). *(warn)*
- **Citekey integrity / literature reconciliation** — `zotero:` keys in source pages exist in
  `library.json`; every `pdf/<citekey>.pdf` basename is a citekey in `library.json`; every
  PDF has a current `txt/`; `library.json` items are either backed by a PDF or intentionally
  metadata-only. *(warn)*
- **Reachability** — every page reachable from `index.md` or a domain index. *(warn)*
- **Near-duplicate titles/pages** — scale safety net for dedup. *(warn)*

### CLI contract

```
wiki lint [--json] [--fix] [--severity error|warn]
    # human report by default; --json structured; non-zero exit if any error
    # --fix applies only SAFE auto-fixes (strip dead Markdown links, normalize frontmatter
    #   key order) — gated, never edits prose or claims
```

### Integration

- `.pre-commit-config.yaml` hook running `wiki lint` (errors block the commit).
- Optional GitHub Actions workflow running the same on push.
- This is the "Lint" operation referenced in `CLAUDE.md`; cross-reference it there.

### Dependencies

`pyyaml`; no heavy deps.

### Acceptance criteria

- Run on the current repo: reports zero errors (the seed-hardening pass already fixed them)
  and the expected warns; matches the findings documented in `log.md`.
- Inject a broken Markdown link → caught, non-zero exit.
- Inject a `seed`+`high` page → warned.
- `--json` schema is stable and documented.
- `--fix` strips a dead wikilink and leaves all prose untouched (diff test).

### Effort

Small-medium.

---

## Feature 4 — Split index (generated, multi-level)

### Goal

Replace the single flat `index.md` (unscannable and rot-prone at hundreds of pages) with a
generated root index linking per-domain catalog pages, so navigation stays cheap and the
agent's entry read stays small.

### Scope

- **Root `wiki/index.md`** — links domain indexes + `shared/`, `comparisons/`, `entities/`,
  `research-backlog`, with per-section page counts and stage/status rollups.
- **`wiki/domains/<domain>/index.md`** — catalog of every page with that `domain:` across all
  types (project, concepts, experiments, sources), each with title, type, stage, status.
- **Generated, not hand-maintained.** A generator reads frontmatter and rewrites only the
  region between `<!-- AUTO:start -->` / `<!-- AUTO:end -->` fences; human prose outside the
  fences is preserved. Idempotent.

### CLI contract

```
wiki toc build [--check]
    # regenerate root + domain index AUTO regions from frontmatter
    # --check exits non-zero if regeneration would change anything (CI guard against
    #   stale indexes) — pairs well with the lint reachability check
```

### Implementation notes

- Domain set derives from `domain:` frontmatter values (currently the four project domains
  plus `shared`); new domains appear automatically.
- Stable ordering: by type, then title. Counts and rollups deterministic.
- Update `CLAUDE.md` to describe the multi-level index and that index files are generated
  (humans edit only outside the AUTO fences).

### Dependencies

`pyyaml`; shares `wikilib` frontmatter reading with Feature 3.

### Acceptance criteria

- Generates root + the four domain indexes from the current corpus; rerun is a no-op
  (idempotency test).
- Add a page with a new `domain:` → `wiki toc build` creates/extends the right domain index.
- Prose written outside the AUTO fences survives regeneration.
- `wiki toc build --check` exits non-zero when an index is stale.

### Effort

Small.

---

## Feature 5 — Bulk literature import

### Goal

Replace the manual "hand-copy PDFs and merge library.json" process with a single
deterministic command that takes a folder containing a **new Zotero export** (one CSL-JSON
library file + `<citekey>.pdf` / `<citekey>-suppl.pdf` attachments, same naming convention as
`raw/literature/`) and merges it into the canonical `raw/literature/` tree, then runs
extraction + index update for whatever changed.

### Scope

- `wikilib.load_library_raw(path) -> dict[citekey, dict]` — full CSL entries (every field),
  not the reduced `Item`. `wikilib.write_library(path, entries)` — deterministic write:
  stable sort by `id`, Zotero's on-disk shape (`[\n`, one compact `  {...}` line per entry,
  `\n]\n`).
- `wikitools.commands.bulk_import` — `run_import(kb_root, source_dir, force=False,
  do_extract=True, do_index=True, ...) -> ImportReport`.
- Merge semantics, keyed by citekey:
  - new citekey → **add** entry to canonical `library.json`, copy PDF(s) into
    `raw/literature/pdf/`.
  - existing citekey, `force=False` (default) → **skip**; canonical entry + PDF untouched.
  - existing citekey, `force=True` → **replace**; overwrite canonical entry + PDF(s).
- After merging, run extraction (existing `run_extract`) and incremental index update
  (existing `update_index`) scoped to the added/replaced citekeys only.
- `--dry-run` reports added/skipped/replaced without writing.

### Non-goals

- Does not create or edit `wiki/sources/*.md` pages or any wiki content — page authoring
  stays the editorial research-pass job; `wiki check source` already flags `new` citekeys
  for the agent to write up.
- Does not touch `raw/seed/`.
- No bibliographic validation of incoming CSL entries.

### CLI contract

```
wiki import <source-dir>
    --force         # replace existing entries/PDFs on citekey collision (default: skip)
    --dry-run       # report planned changes, write nothing
    --no-extract    # merge only, skip extraction
    --no-index      # merge (+ extract) only, skip index update
    --engine ...    # forwarded to extract (fast|docling|marker)
    --json          # structured output: added / skipped / replaced citekeys, extracted/indexed counts
```

### Implementation notes

- `source_dir` is read-only input — never modified or deleted. The only mutated tree is
  `raw/literature/` inside the kb (the controlled exception to "raw/ is immutable": this
  command *populates* raw/, it does not let other tools edit it afterward).
- Locate the library file by globbing `*.json` directly in `source_dir`; error (not guess) if
  zero or more than one match unless `--library <path>` disambiguates.
- Citekey from PDF filename = stem with `-suppl` suffix stripped (matches `extract.py`).
- Skip rewriting a PDF when `--force` and the incoming bytes are identical (hash check) — keeps
  git diffs clean; not required for correctness.
- Extend `run_extract` to accept an optional `citekeys: list[str]` (in addition to the existing
  single `citekey: str`) so import can scope extraction to exactly what changed instead of a
  full-corpus pass.

### Dependencies

None new — `shutil` + `json` stdlib; reuses `extract.run_extract` and `index.update_index`.

### Acceptance criteria

- Folder with 3 new citekeys, no collisions → all 3 added + copied + extracted + indexed;
  re-running the identical import is a no-op (idempotency test: second run reports
  `added=0, skipped=3`).
- Folder with 1 colliding citekey, default mode → canonical entry and PDF byte-identical to
  before; reported `skipped`; no re-extraction triggered.
- Same, with `--force` → entry + PDF replaced, re-extraction triggered (hash changed), index
  updated.
- `--dry-run` → correct counts reported; `git status` shows zero changes under `kb/`.
- 0 or >1 `*.json` files in `source_dir` → clear `ValueError`, no partial writes.
- Determinism test: importing two folders in either order produces byte-identical
  `library.json`.
- `kb/CLAUDE.md` Ingest workflow documents `wiki import` as the entry point for new Zotero
  exports, ahead of the existing per-source steps.

### Effort

Medium.

---

## Cross-cutting: prompt & schema updates

When Features 1 and 2 land, update the research-pass prompt so step (b) reads:
*"call `wiki search` (and `wiki check claim`) before writing — do not read `index.md` to
navigate; consult the local Zotero `library.json` and extracted text first; only web-search
for genuine gaps."* When Feature 4 lands, point the prompt's "read index" step at the root +
relevant domain index rather than a flat file.

Keep each feature's `CLAUDE.md` documentation block short and factual so the agent reliably
discovers and uses the tool. The whole point of the layer is that the agent reaches for
`wiki search` / `wiki lint` / `wiki toc` by default, the way it currently reaches for `git`.
