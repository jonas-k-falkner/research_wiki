# Execution Tasks — Research Wiki Tooling

Source of truth for execution progress (G1). Work tasks in order; one task = one reviewable
commit (C build order). Mark complete only after the execution loop is green (G2, G8).

Cross-reference legend (G8.2): `G*` → guidelines.md · `S*` → scale-features-spec.md ·
`C*` → wiki-context.md · `kb/CLAUDE.md` → wiki content schema.

---

### Task T001 — Repo migration & scaffold

**Goal:** Establish the repository layout so feature work has a stable home, with the existing
knowledge base relocated **unchanged** under `kb/`. No wiki content is edited in this task.

**Progress (2026-06-27):** Config + content + governance half is DONE; the Python package half
is NOT. Remaining work is content-free.

- DONE — `pyproject.toml` (wiki-tools, `src/wikitools` package, core deps duckdb/pyyaml/pypdf,
  extras semantic/api/ocr, `wiki = wikitools.cli:main` script, `[tool.wikitools]`, pytest
  markers + `norecursedirs … kb`, `ruff extend-exclude = ["kb"]`, google pydocstyle).
- DONE — `.gitignore` (ignores `kb/.wiki/`, `*.duckdb`, fastembed cache, `.idea/`; does NOT
  ignore kb content); `uv.lock` committed; git history present.
- DONE — `.agent/guidelines.md`, `.agent/scale-features-spec.md`, `.agent/wiki-context.md`.
- DONE — `kb/` relocated (CLAUDE.md, raw/{seed,research}, wiki/, templates/); verified
  37 pages, 0 broken links, 7 source pages — byte-identical to the finalized+ingested state.
- TODO — `src/wikitools/__init__.py` + `cli.py` stub dispatcher (the console script target
  does not exist yet, so `uv run wiki --help` currently fails on import).
- TODO — `tests/unit/__init__.py` + a trivial CLI test.
- TODO — `README.md`.
- TODO — `.pre-commit-config.yaml` (minimal: ruff format + ruff check; the `wiki lint` hook is
  added in T002).
- TODO — place this `.agent/tasks.md` into `.agent/`.

**Scope (remaining):**
- src/wikitools/__init__.py
- src/wikitools/cli.py
- tests/unit/__init__.py
- tests/unit/test_cli.py
- README.md
- .pre-commit-config.yaml
- .agent/tasks.md

**Root cause:** The kb shipped as a standalone tree; the spec and config assume the full repo
layout (G0). Building features against paths that are about to move is the one sequencing
mistake to avoid (C build order).

**Changes (remaining):**
- Implement `src/wikitools/cli.py` as an **empty subcommand dispatcher** registering the
  `wiki` console script with stub subcommands `lint|toc|extract|index|search|check`, each
  printing "not implemented" and exiting non-zero. No feature logic yet.
- Add `src/wikitools/__init__.py` (package marker; may expose `__version__`).
- Resolve `[tool.wikitools].kb_root` (default `kb`) via config, overridable by `--kb` /
  `WIKI_KB` (G0); do not hardcode `kb/` paths.
- Add `tests/unit/test_cli.py` asserting `wiki --help` lists the six subcommands and that an
  unknown subcommand exits non-zero.
- Add a short `README.md` (what the repo is, layout, QA loop) and a minimal
  `.pre-commit-config.yaml` (ruff format + ruff check only).
- Place this `tasks.md` under `.agent/`.
- `uv sync`. Confirm `kb/` is excluded from ruff (`extend-exclude`) and pytest
  (`norecursedirs`) so the QA loop never touches content (G0, G2). (Both already configured —
  verify, don't re-add.)

**Cross-references:**
- G0
- G2
- G3
- C  (Hard constraints; Build order)
- kb/CLAUDE.md  (Repository structure)

**DoD:**
- `src/wikitools/` exists; `uv run wiki --help` lists the six subcommands and exits cleanly;
  an unknown subcommand exits non-zero.
- `README.md`, `.pre-commit-config.yaml`, and `.agent/tasks.md` present.
- `kb/` content remains byte-identical (no diffs under `kb/wiki/` or `kb/raw/`).
- `uv sync` succeeds; `uv.lock` committed (G3).
- Execution loop green: `uv run ruff format . && uv run ruff check . --fix && uv run mypy src
  && uv run pytest tests/unit` (G2).
- ruff/mypy/pytest demonstrably do **not** traverse `kb/`.
- One commit completing the scaffold.

**Notes / minor deviations to decide (non-blocking):**
- Optional extras are specified as ranges (`fastembed>=0.3`, …); G3 says extras MUST be pinned
  to specific versions. `uv.lock` pins them in practice — tighten the `pyproject` constraints
  if strict G3 compliance is wanted.

**status:** done

---

### Task T002 — `wikilib` foundation + `wiki lint`

**Goal:** Implement the shared `wikilib` primitives and the `wiki lint` command (S Feature 3),
giving a working, deterministic health check over the real `kb/` with no PDFs or embeddings
required.

**Scope:**
- src/wikitools/wikilib.py        (or a `wikilib/` subpackage)
- src/wikitools/commands/lint.py
- src/wikitools/cli.py             (wire the `lint` subcommand)
- .pre-commit-config.yaml          (add the lint hook)
- tests/unit/test_wikilib.py
- tests/unit/test_lint.py
- tests/fixtures/                  (small synthetic kb fixtures — never the real kb/)
- kb/CLAUDE.md                     (document `wiki lint` under the Lint workflow)

**Root cause:** Lint and the foundation need zero PDFs and validate the kb already finalized,
so they are the cheapest first build and exercise `wikilib` before heavier features (C build
order; S §0 Build order).

**Changes:**
- Implement `wikilib` per S §0:
  `iter_pages`, `iter_links` (portable Markdown links, **not** wikilinks), `load_library`,
  `pdf_path`/`txt_path` (basename = citekey, `-suppl` variants, `None` when absent),
  `content_hash`, `inbound_links`. Typed; Google-style docstrings (G7); f-strings only (G7.2).
- Implement the lint checks in S Feature 3 with the stated severities (errors block, warns
  report): broken Markdown links, frontmatter schema, dangling `sources[]`, `[verify]` on
  `researched` pages, orphans, stage/confidence sanity, provenance, thin/boilerplate,
  citekey-integrity / literature reconciliation, reachability, near-duplicate titles.
- CLI contract per S Feature 3: `wiki lint [--json] [--fix] [--severity error|warn]`; non-zero
  exit on any error; `--json` stable schema; `--fix` does only SAFE fixes (strip dead Markdown
  links, normalize frontmatter key order) and NEVER edits prose/claims.
- Resolve `kb_root` from config/flag/env (G0); fail fast with a clear message if missing (G5).
- Add the pre-commit hook running `wiki lint` (errors block commit) (S Feature 3 Integration).
- Document `wiki lint` in `kb/CLAUDE.md` Lint workflow (C: every feature updates CLAUDE.md).
- Determinism: stable sort orders; identical kb → byte-identical `--json` (C; G4).

**Cross-references:**
- S §0  (`wikilib` foundation; Build order)
- S Feature 3  (Scripted lint — checks, CLI, acceptance)
- G2
- G4
- G5
- G7
- C  (determinism; one feature = one commit)

**DoD:**
- `uv run wiki lint` on the real `kb/` reports **0 errors** and the expected warns, consistent
  with `kb/wiki/log.md` (S Feature 3 acceptance).
- Injected broken Markdown link in a fixture → caught, non-zero exit.
- Injected `stage: seed` + `confidence: high` fixture page → warned.
- `--json` schema documented and stable across runs on identical input (determinism test).
- `--fix` strips a dead Markdown link in a fixture and leaves all prose untouched (diff test).
- Unit + edge-case tests (empty/missing/malformed frontmatter) pass; real-kb test marked
  `@pytest.mark.integration` (G4).
- `kb/CLAUDE.md` Lint workflow updated; pre-commit hook present.
- Execution loop green (G2). One commit.

**status:** done

---

### Task T003 — `wiki toc`: generated multi-level index

**Goal:** Replace the manually maintained flat `wiki/index.md` with a generated root index
plus per-domain catalog pages, keeping navigation cheap and the agent's entry read small at
hundreds of pages. Human prose outside `<!-- AUTO:start -->` / `<!-- AUTO:end -->` fences is
preserved across regenerations.

**Scope:**
- `src/wikitools/commands/toc.py`
- `src/wikitools/cli.py`              (restructure `toc` to dispatch `toc build`)
- `tests/unit/test_toc.py`
- `tests/fixtures/`                   (extend with multi-domain kb fixture)
- `kb/CLAUDE.md`                      (document `wiki toc` under a new TOC workflow section)
- `kb/wiki/index.md`                  (one-time: insert AUTO fences around generated region)
- `kb/wiki/domains/*/index.md`        (generated on first run; committed)

**Root cause:** Flat `index.md` becomes unreadable past ~100 pages and drifts as the corpus
grows. Generated indexes derived from frontmatter are always current and verifiable in CI
(S Feature 4; C: navigation stays cheap).

**Changes:**
- Implement `toc.py`:
  - `generate_root(pages, kb_root) -> str` — rewrites the AUTO region of `wiki/index.md`
    with a section per domain (counts, stage/status rollups) and links to each domain index.
    Rows ordered by domain, then type, then title — deterministic.
  - `generate_domain_index(pages, domain, kb_root) -> str` — rewrites the AUTO region of
    `wiki/domains/<domain>/index.md` with a catalog table of all pages whose `domain:`
    matches, columns: title, type, stage, status.
  - `_rewrite_auto_region(existing_text, new_content) -> str` — replaces text between
    `<!-- AUTO:start -->` and `<!-- AUTO:end -->` fences; inserts fences + content at end if
    absent (first-run bootstrap).
  - `build_toc(kb_root, check=False) -> bool` — orchestrates root + all domain indexes;
    returns True if any file was (or would be) changed; idempotent by string equality.
- Wire `wiki toc build [--check]` in `cli.py`: restructure the `toc` subparser to dispatch
  sub-subcommands; `--check` exits non-zero if any file would change (CI staleness guard),
  without writing.
- Resolve `kb_root` from config/flag/env (G0).
- Domain set is derived dynamically from `domain:` values seen in pages — new domains appear
  without code changes.
- Update `kb/CLAUDE.md`: add a short TOC workflow section explaining that `wiki/index.md`
  and `wiki/domains/*/index.md` are generated, that humans edit only outside the AUTO fences,
  and that `wiki toc build --check` is the CI guard (C: every feature updates CLAUDE.md).
- Update `kb/wiki/index.md` to insert AUTO fences around the generated catalog region, keeping
  all existing human prose (intro, project-track table, etc.) outside the fences.

**Cross-references:**
- S Feature 4
- G0
- G2
- G4
- G7
- C  (determinism; one feature = one commit; CLAUDE.md updated)

**DoD:**
- `wiki toc build` on the real `kb/` generates root + four domain indexes; rerun is a no-op.
- Add a fixture page with a new `domain:` → `wiki toc build` creates/extends the right domain
  index without any code change.
- Prose outside the AUTO fences in both the root and a domain index survives regeneration
  (diff test: before and after have identical non-AUTO lines).
- `wiki toc build --check` exits non-zero when an index is stale; exits 0 when up-to-date.
- `--json` output (if any) is stable across identical runs (determinism).
- Unit + idempotency tests pass; real-kb test marked `@pytest.mark.integration`.
- `kb/CLAUDE.md` TOC workflow section present; AUTO fences in `wiki/index.md`.
- Execution loop green (G2). One commit.

**status:** done

---

### Task T004 — Retrieval layer: PDF extraction + hybrid search index

**Goal:** Replace "read `index.md` to navigate" with `wiki search` over wiki pages and
full-text literature PDFs. Hybrid lexical (BM25) + semantic (local embedding cosine) search
fused with RRF, stored in a single DuckDB file. This is the primary scale unlock.

**Prerequisite:** Zotero PDF export present in `kb/raw/literature/` (`library.json` + `pdf/`).
The task can be started on the code before PDFs arrive, but acceptance tests require real PDFs
to run at integration level. Unit tests use fixtures only (G4).

**Scope (two commits — 1a then 1b):**

*Commit 1a — extraction:*
- `src/wikitools/commands/extract.py`
- `src/wikitools/cli.py`             (wire `extract` subcommand)
- `tests/unit/test_extract.py`

*Commit 1b — index + search:*
- `src/wikitools/commands/index.py`  (`build`, `update`, `status`)
- `src/wikitools/commands/search.py`
- `src/wikitools/cli.py`             (restructure `index` to dispatch sub-subcommands; wire `search`)
- `tests/unit/test_index.py`
- `tests/unit/test_search.py`
- `kb/CLAUDE.md`                     (document `wiki extract`, `wiki index`, `wiki search`)

**Root cause:** Single flat `index.md` breaks at ~100 sources; agents must search, not
browse. Hybrid search (lexical anchors exact terms; semantic finds paraphrases) over both
wiki pages and extracted PDF text is the single capability that makes the corpus scalable
(C; S Feature 1).

#### 1a extraction:
- Implement `extract.py`:
  - `run_reconciliation(kb_root) -> list[ReconciliationIssue]` — before any extraction:
    every `pdf/<citekey>` basename must be in `library.json`; every `library.json` item
    either has a PDF or is metadata-only; every PDF has a current `txt/`. Emits issues,
    does not fail silently.
  - `extract_pdf(pdf_path, txt_path, extractor="pdftotext") -> None` — shells out to
    `pdftotext` (default), `docling`, or `marker`. Logs and skips on failure (non-fatal).
  - `run_extract(kb_root, engine, force, citekey) -> None` — runs reconciliation first, then
    iterates `pdf/` files, skips if `txt/<basename>.extract.json` hash matches current PDF
    (idempotent), writes `txt/<basename>.txt` + sidecar `extract.json` (extractor name +
    source hash).
  - `docling` and `marker` engines are behind the `[ocr]` optional extra; raise
    `MissingExtraError` if invoked without that extra installed (G3, G5).
- Wire `wiki extract [--engine pdftotext|docling|marker] [--force] [--citekey X]`.

#### 1a.2 Math-aware PDF extraction

**Goal:** Extract literature PDFs to text that **preserves math as LaTeX** instead of
mangling it, by defaulting to a structure-aware engine (Docling → Markdown + `$$…$$`),
while keeping the dependency-free fast path working and the PDF as the math authority.

**Scope:**
- src/wikitools/commands/extract.py
- src/wikitools/wikilib.py            (engine dispatch helpers only)
- pyproject.toml                      ([ocr] extra; verify, don't loosen)
- tests/unit/test_extract.py
- tests/fixtures/                     (one tiny math-bearing PDF or a stubbed engine)
- kb/CLAUDE.md                        (document `wiki extract` engines)

**Root cause:** `pdftotext`/`pypdf` read glyphs in layout order and drop sub/superscript and
math-font semantics, so equations become unsearchable, unreadable garbage. Academic PDFs are
the dominant corpus, so math-aware extraction is the right default for literature, not a rare
fallback.

**Changes:**
- `wiki extract [--engine docling|marker|fast] [--kb …]`. Engine resolution for literature:
  default to **docling** when the `[ocr]` extra is installed; if absent, fall back to **fast**
  (pypdf/pdftotext) and print a one-line stderr warning that math will be degraded. Core
  behavior must work with **no** extras installed (G3).
- `--engine docling|marker` without its extra → fail fast with an actionable install message
  (G3, G5). `--engine fast` never requires an extra.
- Read `kb/raw/literature/pdf/<basename>.pdf` (incl. `<citekey>-suppl.pdf`); write
  `kb/raw/literature/txt/<basename>.txt` (content = Markdown with LaTeX math fences). Resolve
  by basename = citekey; skip metadata-only items (no PDF) without error.
- Idempotent by source hash: skip re-extraction when the stored hash matches. Record
  `engine + engine_version + source_sha256` in sidecar `txt/<basename>.extract.json`.
- Never silently drop a math region — emit it as a LaTeX fence so the agent can recognize it
  and re-read the PDF (the authority) when a claim depends on exact notation.
- Do NOT mutate `kb/raw/**` originals; the `.txt`/sidecar are the only writes (G10).

**Determinism note (do not reject the ML engine over this):** extracted `.txt` is **committed**
and extraction is **hash-skipped** (run once, never regenerated per machine). Extraction is a
one-time upstream step whose output is frozen in git and reviewed by diff; the determinism
constraint (C) binds the search/index/lint layer that *reads* the committed text, not the ML
extraction that produced it. The sidecar (engine+version+hash) makes the step auditable. No
determinism test is required on extraction output; determinism tests belong to T00x (search).

**Cross-references:**
- S Feature 1   (1a — extraction; idempotent-by-hash; sidecar)
- G3            (optional extras: pinned, error if missing, no effect on core when absent)
- G5            (fail fast, actionable errors)
- G2 / G4 / G10
- C             (determinism reconciliation above; raw/ immutable)
- kb/CLAUDE.md  (Literature layout conventions)

**DoD:**
- On a real math-bearing literature PDF, `wiki extract --engine docling` produces output whose
  equations appear as LaTeX fences (`$…$` / `$$…$$`), not reordered glyphs — assert on a known
  equation in a fixture.
- With `[ocr]` absent: `wiki extract` runs the fast path + emits the degradation warning;
  `--engine docling` errors with an install hint. Core lexical path unaffected (G3).
- Re-run with unchanged source hash is a no-op; sidecar records engine+version+source hash.
- `txt/` basenames mirror `pdf/` (incl. `-suppl`); metadata-only items skipped, not errored.
- `kb/raw/**` byte-unchanged after a run.
- `kb/CLAUDE.md` documents the engines and the "PDF is authority for exact math" rule.
- Execution loop green (G2). One commit.



#### 1b index + search:
- Implement chunking:
  - Wiki pages: split body by H2/H3 headings into sections; each chunk = `(path, None,
    section_title, text)`. Char-based, deterministic.
  - PDF text: sliding window ~800 chars, ~100-char overlap; each chunk = `(path, citekey,
    page_approx, text)`. Deterministic given fixed text.
- Implement `index.py`:
  - Schema: DuckDB table `chunks(id, source_path, citekey, section, text, embedding FLOAT[384])`.
  - `build_index(kb_root, embedder, model) -> None` — full rebuild; FTS index via DuckDB
    `fts` extension; embeddings via `embed(texts) -> list[list[float]]` interface; stores
    result. One DuckDB file at `kb/.wiki/corpus.duckdb`.
  - `update_index(kb_root) -> None` — reprocesses only changed pages/PDFs (mtime + hash);
    re-embeds only those chunks. Appends/replaces rows; never full rebuild.
  - `index_status(kb_root) -> dict` — counts pages, chunks, PDFs, embed model, dim, last-build
    timestamp.
  - Embedder interface: `class Embedder` with `embed(texts) -> list[list[float]]`; two
    implementations: `LocalEmbedder` (fastembed, default) and `OpenAIEmbedder` (opt-in, `[api]`
    extra). `LocalEmbedder` raises `MissingExtraError` if `fastembed` not installed (G3, G5).
  - Brute-force cosine via `array_cosine_similarity`; no `vss`/HNSW (S Feature 1 non-goals;
    C: determinism, no experimental persistence).
- Implement `search.py`:
  - `search(query, kb_root, scope, k, project, type_, mode) -> list[Hit]` — lexical (BM25
    FTS), semantic (cosine), or hybrid (RRF fusion). `Hit` carries path, citekey, section,
    score, snippet.
  - RRF: `score = Σ 1/(k_rrf + rank_i)` over the two lists; configurable `k_rrf=60`; stable
    tie-break by `(source_path, chunk_index)`.
  - Optional source-overlap graph bonus: if a hit's page links to the query page (or vice
    versa), add a small score bonus. Keep it in the same scoring function.
  - `--json` output deterministic: same DB + query → byte-identical results.
- Wire `wiki index build|update|status` and `wiki search "QUERY" [opts]` in `cli.py`:
  restructure `index` subparser to dispatch sub-subcommands `build`, `update`, `status`.
- Pin `fastembed` to exact version in `pyproject.toml` `[semantic]` extra (G3). Run
  `uv sync` after pinning.
- Update `kb/CLAUDE.md` with short factual blocks for `wiki extract`, `wiki index`, and
  `wiki search`; update the Query workflow to call `wiki search` instead of reading
  `index.md`; update research-pass prompt (C: every feature updates CLAUDE.md).

**Cross-references:**
- S Feature 1  (full spec including 1a and 1b)
- S §0         (wikilib; `pdf_path`, `txt_path`, `load_library`)
- G0
- G2
- G3           (fastembed pinning; MissingExtraError)
- G4
- G5
- G6           (brute-force cosine, no HNSW)
- G7
- C            (determinism; CLAUDE.md updated; build order; no vss/HNSW)

**DoD:**
- `wiki extract` with real PDFs: one `.txt` per text PDF; rerun zero writes; `--force`
  re-extracts; failed PDF logged and skipped.
- `wiki index build` chunks, FTS-indexes, and embeds all content; `wiki index status` reports
  model, dim, counts.
- `wiki search "entmax" --json --mode hybrid` returns the entmax concept page and matching
  paper chunks with resolvable paths.
- `wiki search --mode semantic` finds a paraphrased claim with no exact term overlap (semantic
  recall test against the real kb).
- `wiki search "CITEKEY" --mode lexical` returns the exact source page (lexical recall test).
- `wiki index update` after touching one page reprocesses only that page.
- Identical DB + query → byte-identical `--json` (determinism test).
- Unit tests use fixture PDFs/pages; real-kb tests marked `@pytest.mark.integration`.
- `kb/CLAUDE.md` updated; Query workflow uses `wiki search`.
- Execution loop green (G2). Two commits (1a then 1b).

**status:** done

---

### Task T005 — Idempotent ingest + claim-check (`wiki check`)

**Goal:** Prevent semantic duplication at scale: re-ingesting a source converges to the same
state (no duplicate source pages), and the agent can ask before writing a claim whether the
corpus already states it.

**Prerequisite:** T004 complete (claim-check uses the search index for similarity; `wiki check
source` uses `content_hash` from `wikilib`).

**Scope:**
- `src/wikitools/commands/check.py`
- `src/wikitools/cli.py`   (restructure `check` to dispatch `check source` / `check claim`)
- `tests/unit/test_check.py`
- `kb/CLAUDE.md`           (document `wiki check`; update Ingest workflow and research-pass prompt)

**Root cause:** Without a convergence guarantee, repeated ingest passes accrete duplicate
source pages and semantically identical claims in different words (C; S Feature 2).

**Changes:**
- Implement `check.py`:
  - `check_source(citekey, kb_root) -> SourceStatus` — scan `wiki/sources/` for a page with
    `zotero: <citekey>` in frontmatter; compute `content_hash` of the matching raw source
    (`pdf_path` or `txt_path`); compare to `source_hash:` in that page's frontmatter. Returns
    one of `{new, unchanged, changed}` plus the existing page path (if any).
  - `check_claim(claim_text, kb_root, citekey, page) -> list[ClaimHit]` — search the corpus
    for existing claims similar to `claim_text`. Primary: lexical FTS (BM25) against the index
    from T004; secondary: if `[semantic]` extra installed, also cosine similarity. Each
    `ClaimHit` carries: location (path + line-range), snippet, similarity score, and whether
    the hit already cites `citekey`.
  - Classify each `ClaimHit` as `duplicate` (same source), `additional-support` (different
    source, high similarity), or `new` (low similarity). Advises only; never auto-merges.
  - `MissingExtraError` raised if semantic mode requested but `[semantic]` not installed (G3, G5).
- Wire `wiki check source --citekey X [--json]` and `wiki check claim "TEXT" [--citekey X]
  [--page PATH] [--json]` in `cli.py`: restructure `check` subparser with sub-subcommands
  `source` and `claim`.
- Ingest wrapper (documented in `kb/CLAUDE.md`, not a separate command):
  resolve src page → if `unchanged` stop → else update `source_hash:` in frontmatter +
  append a parseable `log.md` entry keyed by citekey (re-runs are detectable via `git log`).
- Update `kb/CLAUDE.md`: add `wiki check` to the Ingest workflow; update research-pass prompt
  to call `wiki check claim` before writing new claims; document `source_hash:` and `zotero:`
  as required frontmatter for literature source pages (C: every feature updates CLAUDE.md).

**Cross-references:**
- S Feature 2
- S Feature 1  (search index reused for claim similarity)
- S §0         (`content_hash`, `load_library`)
- G0
- G2
- G3           (MissingExtraError for semantic mode)
- G4
- G5
- G7
- C            (determinism; CLAUDE.md updated; one feature = one commit)

**DoD:**
- Re-ingesting an unchanged source (`wiki check source --citekey X`) returns `unchanged`
  and zero git diff (true idempotency test).
- Two source pages cannot share a citekey: ingesting the same citekey twice → second run
  returns `unchanged` or `changed` (in-place update path), never creates a second page.
- `wiki check claim "CLAIM"` surfaces a known near-duplicate claim's location; a genuinely
  new claim returns no high-similarity hits.
- A claim supported by a second source is classified `additional-support`, not `duplicate`.
- `--json` output stable across identical runs (determinism).
- Unit tests cover all status codes and classification cases; real-kb test marked
  `@pytest.mark.integration`.
- `kb/CLAUDE.md` Ingest workflow updated; research-pass prompt updated.
- Execution loop green (G2). One commit.

**status:** done

---

### Task T006 — Semantic search integration: fastembed pin + integration tests + rebuild UX

**Goal:** Make the semantic search path production-ready: pin `fastembed` to the installed
exact version, exercise real embeddings end-to-end on the real kb, verify RRF hybrid recall,
and surface two UX gaps (rebuild time + `update_index` with embeddings).

**Prerequisite:** T004-1b done (`wiki index build` + `wiki search` wired). fastembed 0.8.0
installed via `uv sync --extra semantic`.

**Root cause (3 distinct gaps found during install+test):**
1. **G3 pin gap:** `pyproject.toml` has `fastembed>=0.3` (range), not a pinned exact version.
   `uv.lock` pins in practice, but the declared constraint should match G3.
2. **Rebuild time:** Embedding 11k chunks takes several minutes. There is no progress
   reporting, no batch-size knob, and the rebuild cadence is undocumented. Agent needs to know
   not to rebuild on every query.
3. **`update_index` semantic gap:** `update_index` reprocesses only changed files, but the
   embedder path is untested end-to-end (unit tests used `embedder=None`). Need an integration
   test with real fastembed to catch silent failures (e.g. wrong vector dimensionality stored).

**Scope:**
- `pyproject.toml`                  — tighten `semantic` extra to `==0.8.0`
- `src/wikitools/commands/index.py` — add `batch_size` param to `_insert_chunks` + `build_index`;
                                      emit `logger.info` progress every N batches
- `tests/unit/test_index.py`        — add test: `build_index` with real embedder mock that returns
                                      384-dim vectors; verify embedding column is non-NULL
- `tests/integration/test_semantic.py` — real-kb integration tests (marked `@pytest.mark.integration`):
  - `test_build_index_with_fastembed` — builds real index, checks `embed_model != "none"`,
    chunk count > 0, at least one chunk has a non-NULL embedding
  - `test_search_semantic_recall` — `wiki search "sparse probability mapping" --mode semantic`
    returns the entmax concept page in top-5 (paraphrase recall, no exact term overlap)
  - `test_search_hybrid_beats_lexical_on_paraphrase` — a paraphrased query hits the right page
    in hybrid but not in lexical top-5 (validates RRF semantic contribution)
  - `test_update_index_with_embedder` — edit one wiki page, run `update_index` with real
    embedder, confirm only 1 file reprocessed and the updated chunk has a non-NULL embedding
- `kb/CLAUDE.md`                    — add note to Index workflow: rebuild time (~N min on full
                                      corpus); run `wiki index build` once per machine after
                                      `uv sync --extra semantic`; `wiki index update` for
                                      incremental updates after adding pages

**Changes:**
- Pin `pyproject.toml` `semantic` extra: `fastembed==0.8.0`.
- Add `batch_size: int = 256` to `build_index` and `_insert_chunks`; emit a `logger.info`
  progress line every batch (e.g. `"build_index: embedded batch %d/%d"`) so long runs are
  visible in verbose mode.
- Add `tests/integration/` directory with `__init__.py` and `conftest.py` (skip all unless
  `[semantic]` extra detected; no fixtures — uses real `kb/`).
- Write the 4 integration tests above. Each must pass without network access after the
  fastembed model is cached (model cache is populated on first `uv run wiki index build`).
- Add one new unit test in `test_index.py`: embedder mock that returns 384-dim vectors →
  confirm the stored embedding is non-NULL and has correct length.
- Document rebuild cadence in `kb/CLAUDE.md` Index workflow.

**Cross-references:**
- G3            (fastembed pinning)
- G4            (integration tests marked; no fixtures = real kb)
- S Feature 1   (semantic recall validation)
- C             (determinism; CLAUDE.md updated)

**DoD:**
- `pyproject.toml` `semantic` extra is `fastembed==0.8.0`; `uv sync` succeeds; `uv.lock` committed.
- `wiki index build` with `[semantic]` installed: progress lines visible at `--log-level INFO`;
  `wiki index status` shows `embed_model != "none"`.
- `test_build_index_with_fastembed` passes with real fastembed.
- `test_search_semantic_recall` returns the entmax concept page in top-5 for a paraphrase query.
- `test_update_index_with_embedder` confirms incremental embed on single changed file.
- All 3 hybrid/semantic integration tests pass on real kb.
- New unit test for 384-dim mock embedding passes in execution loop (G2).
- `kb/CLAUDE.md` documents rebuild cadence.
- Execution loop green (G2). One commit.

**status:** done

---

### Task T007 — Bulk literature import: `wiki import` for new Zotero export folders

**Goal:** Replace the manual "hand-copy PDFs + merge library.json" process with one
deterministic command that ingests a folder of a new Zotero export (CSL-JSON library file +
`<citekey>.pdf`/`<citekey>-suppl.pdf` attachments) into `raw/literature/`, then extracts and
indexes whatever changed. Default on citekey collision: skip existing entries; `--force`
replaces them.

**Root cause:** The original four features (T001–T006) assumed `raw/literature/` is already
populated. There is no tooling for *getting new sources in* at scale — today that's manual
file copying + hand-editing `library.json`, which doesn't survive past a handful of exports
and has no collision/replace semantics.

**Scope:**
- `src/wikitools/wikilib.py` — add `load_library_raw(path) -> dict[citekey, dict]` (full CSL
  entries) and `write_library(path, entries: dict[citekey, dict])` (deterministic: sort by
  `id`, Zotero on-disk shape — see S Feature 5 Implementation notes).
- `src/wikitools/commands/bulk_import.py` (new) — `run_import(...)` + `ImportReport`
  dataclass.
- `src/wikitools/commands/extract.py` — extend `run_extract` to accept `citekeys:
  list[str] | None` alongside the existing single `citekey` param, so import can scope
  extraction to exactly what changed.
- `src/wikitools/cli.py` — new `wiki import <source-dir>` subcommand (`--force`, `--dry-run`,
  `--no-extract`, `--no-index`, `--engine`, `--json`).
- `tests/unit/test_bulk_import.py` — fixtures only, never the real `kb/`.
- `tests/integration/test_bulk_import.py` — one real-kb test marked `@pytest.mark.integration`.
- `kb/CLAUDE.md` — new step in Ingest workflow pointing at `wiki import` as the entry point
  for new Zotero exports.

**Changes:**
- `load_library_raw`/`write_library`: round-trip every CSL field losslessly (do not go
  through the reduced `Item` dataclass — that drops fields the canonical catalog must keep).
- `run_import`: glob `*.json` in `source_dir` (error if 0 or >1, unless `--library <path>`
  given); citekey from PDF stem with `-suppl` stripped (matches `extract.py` convention).
  For each citekey in the new library: not in canonical → add (merge entry, copy PDF(s));
  in canonical + `force=False` → skip untouched; in canonical + `force=True` → replace entry
  + PDF(s). Write canonical `library.json` only if changed. `source_dir` is read-only input —
  never modified or deleted.
- Optional optimization: skip rewriting a PDF on `--force` when incoming bytes hash-match the
  existing file (keeps git diffs clean).
- Wire `--no-extract`/`--no-index` to call the existing `run_extract`/`update_index` scoped to
  added+replaced citekeys; `--dry-run` writes nothing, reports counts only.
- `ImportReport`: `added`, `skipped`, `replaced` (citekey lists) + `extracted`, `indexed_files`
  counts; `--json` emits it.

**Cross-references:**
- G2  (execution loop: format/lint/mypy/pytest before done)
- G3  (no new deps — stdlib `shutil`/`json` only)
- G4  (unit tests with fixtures; integration test marked, real kb)
- G10 (`kb/raw/` immutability — this command is the controlled exception that *populates*
  raw/; it must not let other tools mutate it afterward, and the source export folder itself
  is never written to)
- S Feature 5  (full contract — added in this task, see `.agent/scale-features-spec.md`)
- C  (determinism: stable sort, byte-identical merged `library.json` regardless of import
  order; architecture unchanged — no server/DB beyond the existing DuckDB index)

**DoD:**
- 3 new citekeys, no collisions → added + copied + extracted + indexed; re-import is a no-op
  (`added=0, skipped=3`).
- 1 colliding citekey, default mode → entry + PDF untouched, reported `skipped`, no
  re-extraction.
- Same with `--force` → entry + PDF replaced, re-extraction triggered, index updated.
- `--dry-run` → correct reported counts, zero `git status` changes under `kb/`.
- 0 or >1 `*.json` in source folder → `ValueError`, no partial writes.
- Determinism test: two import orders → byte-identical `library.json`.
- `kb/CLAUDE.md` Ingest workflow documents `wiki import`.
- Execution loop green (G2). One commit.

**Incidental fixes (pre-existing, discovered while building T007, not part of the feature):**
- `wikitools.wikilib.write_library` itself had a bug at first draft (missing `,` between
  array entries — multi-entry round-trip test caught it before this was marked done).
- `tests/unit/test_extract.py`: `docling` is now actually installed in this environment
  (it wasn't when T004's tests were written), so `_resolve_engine(None)` auto-resolves to
  `"docling"` instead of `"fast"`. This broke 3 pre-existing tests whose `_fake_pdftotext`/
  `flaky_extract` mocks didn't accept the `_converter` kwarg the real `extract_pdf` always
  receives, plus one assertion that hard-coded `extractor == "fast"`. Fixed by widening the
  mock signatures and pinning `engine="fast"` where the test's intent is the fast/pdftotext
  path, not engine auto-resolution.
- `src/wikitools/cli.py`: the `wiki extract --engine` flag's argparse `default` was the
  literal string `"docling"`, not `None`. This silently defeated `_resolve_engine`'s
  documented fallback (`wiki extract` with no flags hard-failed if the `[ocr]` extra was
  absent, instead of falling back to `fast`). Changed `default="docling"` to `default=None`
  so the auto-resolve path the help text already describes actually runs. One test
  (`test_extract_cli_warns_on_degraded_engine`) now passes as a result.
- One further pre-existing failure remains, NOT fixed here (out of scope, env-dependent,
  unrelated to bulk import): `test_extract_pdf_ocr_engine_raises_missing_extra` is flaky
  when run after other tests warm the real `docling.document_converter` import cache in the
  same pytest session — its `sys.modules` absence-sentinel stops working once that submodule
  is already cached. Passes in isolation; worth a follow-up task if it bites again.

**status:** done
