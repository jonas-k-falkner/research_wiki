# Agent Guidelines — Research Wiki Tooling

This document defines **mandatory rules** for all Agent actions in this repository.
These rules override any default behavior or assumptions.
This file is the authoritative governance document for the Agent's **code** work.
The Agent MUST treat this file as binding regardless of other documentation.


## Caveman Policy (MANDATORY)
Respond like a caveman. No articles, no filler words, no pleasantries. Short. Direct. Code speaks for itself.

### Details
Give the answer first.
Prefer direct solutions over explanations.
If explanation is needed, limit to one sentence.

Use minimal tokens while preserving correctness.

Assume an expert user; do not explain basics.

For coding tasks:
- Output code first, then a brief note if needed.
- Do not describe obvious code behavior.
- Prefer minimal diffs over full rewrites when possible.
- Preserve existing style unless told otherwise.

For problem solving:
- State assumptions briefly if required.
- Do not speculate; ask if missing critical info.
- Prefer deterministic answers over hedging.

Formatting:
- Avoid unnecessary lists.
- Use bullets only if they improve clarity.
- No markdown headers unless requested.

Do not:
- Apologize
- Add motivational or conversational text
- Restate the question

---

## 0. Repository Layout & the Code/Content Boundary (MANDATORY)

```
src/wikitools/   # the tooling package + `wiki` CLI  — CODE
tests/           # unit + integration tests          — CODE
.agent/          # governance + specs                — GOVERNANCE
kb/              # the knowledge base                 — CONTENT (the deliverable)
  CLAUDE.md      #   schema for wiki CONTENT (authoritative for content/structure)
  raw/           #   IMMUTABLE sources (PDFs, seed notes, library.json) — never edit
  wiki/          #   LLM-maintained markdown pages
  templates/
  .wiki/         #   rebuildable DuckDB index (gitignored)
```

**Two governance docs, two scopes:**
- `guidelines.md` (this file) governs the **tooling code** under `src/` and `tests/`.
- `kb/CLAUDE.md` governs **wiki content** — page types, claim format, ingest/query/lint
  rules. It binds only when a task edits `kb/wiki/` content, not when building tools.

**Hard boundary:**
- The QA loop (format/lint/typecheck/test) targets `src/` and `tests/` ONLY. NEVER run it
  on `kb/`. `kb/` is excluded in `pyproject.toml` (`ruff extend-exclude`, pytest
  `norecursedirs`).
- Tools OPERATE ON `kb/` (read pages, index PDFs) but MUST NOT treat it as code to
  lint/format, and MUST NOT mutate `kb/raw/` under any circumstance.
- KB path is configured (`[tool.wikitools].kb_root`, default `kb`), overridable by `--kb`
  flag and `WIKI_KB` env var. Never hardcode `kb/` paths in the package.

---

## 1. Sources of Truth

- Execution progress MUST be tracked in:
  - `.agent/tasks.md`

The Agent MUST NOT invent new requirements or APIs.
If something is unclear or missing, the Agent must pause and propose a change to `.agent/tasks.md`.

Reference documents (read before implementing — see §8.2):
- `.agent/scale-features-spec.md` — what to build (features, contracts, acceptance).
- `.agent/wiki-context.md` — what it is for, scope, hard constraints.

---

## 2. Execution Loop (MANDATORY)

For every coding task, the Agent MUST complete the following loop before finishing:

1. Implement only the explicitly requested scope.
2. Run formatting:
   - `uv run ruff format .`
3. Run linting:
   - `uv run ruff check . --fix`
4. Run type checking:
   - `uv run mypy src`
5. Run unit tests:
   - `uv run pytest tests/unit`
6. If any step fails:
   - Fix the issue.
   - Re-run the full loop from step 2.
7. If a step cannot be run:
   - Explain why.
   - Stop without marking the task complete.

The loop never touches `kb/` (see §0).

---

## 3. Dependency Policy

- Do NOT add new runtime or dev dependencies without explicit approval.
- Use only dependencies declared in `pyproject.toml`.
- Prefer standard library functionality when possible.
- Core runtime deps are: `duckdb`, `pyyaml`, `pypdf`. Prefer stdlib over a new core dep.
- After any dependency change, run `uv sync`.
- Never use `pip install`.
- Use `uv run` instead of `python -m` for running scripts.
- `uv.lock` IS committed.

Optional extra dependencies (sanctioned groups: `semantic`, `api`, `ocr`):
- MUST be pinned to specific versions (`uv add --optional <group> <pkg>`).
- MUST raise a clear error if missing at runtime.
- MUST NOT affect core behavior when not installed.
- Example: semantic search requires `[semantic]` (fastembed); without it, `wiki index build`
  must fail with an actionable message, and lexical-only search must still work.

---

## 4. Testing Requirements

Every new module MUST include tests.

Minimum expectations:
- Unit tests for core logic
- Edge-case tests (empty payloads, missing fields, invalid configs, malformed frontmatter)
- Determinism tests where applicable (identical inputs → byte-identical output)
- Contract tests for ingestion / search / lint / index boundaries

Tests live under `tests/` and must import only the public API where possible.
- Unit tests use small fixtures under `tests/` — never the real `kb/`.
- Tests that exercise the real `kb/` MUST be marked `@pytest.mark.integration`.

---

## 5. Error Handling & Validation

- Fail fast on invalid inputs.
- Raise clear, user-facing exceptions for:
  - Invalid CLI args / missing kb_root
  - Malformed frontmatter / unresolvable wikilinks (in lint context)
  - Missing optional extra when its feature is invoked
- Avoid silent coercion or implicit fixes.

Error messages should help users correct their data.

---

## 6. Performance & Memory

- Avoid unnecessary copies of large arrays/dataframes.
- Prefer vectorized / set-based (SQL) operations over Python loops.
- Brute-force cosine is correct at this corpus scale; do NOT add HNSW/`vss` (see spec).
- Document any operation with non-obvious complexity.

Do NOT micro-optimize unless requested.

---

## 7. Documentation Expectations

- All public classes/functions MUST have docstrings explaining:
  - Purpose
  - Parameters (especially time-related ones)
  - Return values

### 7.1 Docstring Style (MANDATORY)

All public-facing classes, functions, and methods MUST use **Google-style docstrings**.

Rules:
- Use Google format: short summary line, followed by sections like `Args`, `Returns`, `Raises`.
- Keep the summary line **one sentence, ≤ 80 characters**, describing *what*, not *how*.
- Do NOT include type information in docstrings if it is already present in type hints.
- Avoid verbosity: prefer concise, precise phrasing.
- Do NOT use NumPy-style or reStructuredText-style docstrings.
- Private helpers may omit docstrings unless non-trivial.
- If a docstring exceeds ~10 lines for a function or ~15 lines for a class,
the Agent must shorten it unless explicitly requested to be verbose.

Example (canonical):
```python
def search(
    query: str,
    mode: str = "hybrid",
    k: int = 10,
) -> list[Hit]:
    """Search the wiki + literature corpus and return ranked hits.

    Args:
        query: Free-text query.
        mode: One of "hybrid", "lexical", "semantic".
        k: Maximum number of hits to return.

    Returns:
        Hits ordered by descending fused score.

    Raises:
        MissingExtraError: If mode requires `[semantic]` and it is not installed.
    """
```

### 7.2 String Formatting (MANDATORY)

All string formatting MUST use **f-strings**.

Rules:
- Never use `%`-formatting or `str.format()`.
- Use f-strings for all interpolation, including log messages and exception text.
- For multiline strings, f-strings are still preferred over `.format()`.

---

## 8. Task Discipline

- Work only on tasks explicitly listed in `.agent/tasks.md`.
- Mark tasks complete only after:
  - Code is written
  - Tests pass
  - Execution loop is complete
- If scope grows:
  - Add new tasks instead of improvising.


### 8.1 Task format

```markdown
### Task TXXX — Short action-oriented title

**Goal:** Desired outcome.

**Scope:**
- allowed/file.py
- tests/unit/test_x.py

**Root cause:** Optional technical explanation.

**Changes:**
- Required implementation step
- Required implementation step

**Cross-references:**
- G*
- S*
- C*


**DoD:**
- Observable result
- Required tests pass
- Execution loop green

**status:** pending
```

### 8.2 Reference Resolution Rules

Task cross-references MUST resolve as follows:

- `G*` → `guidelines.md` (this file)
- `S*` → `.agent/scale-features-spec.md`
- `C*` → `.agent/wiki-context.md`
- `kb/CLAUDE.md` → wiki content schema (consult when a task edits `kb/wiki/`)

Examples:
- `G3` refers to section 3 in `guidelines.md`
- `S Feature 1` refers to the Retrieval layer in the spec

Tasks without valid cross-references are invalid.
Cross-references are authoritative and MUST be consulted before implementation.


---

## 9. Review Mindset

The Agent is an implementer, not an architect.

When uncertain:
- Pause
- Ask
- Propose changes
- Do NOT guess

Correctness, reproducibility, and determinism are more important than speed.


---

## 10. Special Files (MANDATORY)

### .ignore
All files in `.ignore` MUST be excluded from any actions or operations.
The Agent MUST NOT read or write any of these files.

### implementation_refs
All files in `implementation_refs` MUST NOT be read, with the only exception of being EXPLICITLY requested.

### kb/raw/
Immutable source material. The Agent MUST NOT create, edit, or delete anything under
`kb/raw/`. Tools may read it and write derived artifacts (extracted `.txt`) beside sources,
but the original source bytes are never modified.
