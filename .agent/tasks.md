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

**status:** in-progress

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

**status:** pending

---

## Backlog (not yet scoped into tasks)

Per C build order, after T002: T003 `wiki toc` (S Feature 4) → T004 retrieval (S Feature 1;
requires the Zotero PDF export into `kb/raw/literature/`) → T005 idempotent/claim-check ingest
(S Feature 2). Scope each as its own task when reached (G8 — add tasks, don't improvise).
