# research-wiki

LLM-maintained research wiki for AI projects P1–P4. Markdown-in-git architecture with a retrieval and maintenance layer.

## Layout

```
src/wikitools/   # wiki CLI package
tests/           # unit + integration tests
.agent/          # governance docs and specs
kb/              # knowledge base (content — never linted as code)
  raw/           #   immutable sources (PDFs, seed notes, library.json)
  wiki/          #   LLM-maintained markdown pages
  templates/
  .wiki/         #   rebuildable DuckDB index (gitignored)
```

## CLI

```
wiki lint       # health checks (broken links, frontmatter, orphans, …)
wiki toc        # generate root + per-domain index pages
wiki extract    # extract text from literature PDFs
wiki index      # build / update hybrid search index
wiki search     # hybrid lexical + semantic search
wiki check      # source idempotency and claim deduplication
```

Global flag: `--kb PATH` (or `WIKI_KB` env var) overrides the kb root.

## QA loop

```bash
uv run ruff format .
uv run ruff check . --fix
uv run mypy src
uv run pytest tests/unit
```

Targets `src/` and `tests/` only — never `kb/`.
