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

**status:** pending

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

**Changes (1a — extraction):**
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

**Changes (1b — index + search):**
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

**status:** pending

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

**status:** pending
