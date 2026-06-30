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

## Zotero export

For the Zotero export, export Better CSL JSON and export files (set naming convention to the citekey). Run this inside the parent directory that contains the Zotero single-file subdirectories (moves all PDFs from subfolders into the current directory and does not overwrite files with the same name because of -n):
```bash
find . -mindepth 2 -type f -iname '*.pdf' -exec mv -n -t . {} +
```
Then remove the now-empty directories:
```bash
find . -mindepth 1 -type d -empty -delete
```
Finally copy/append json to existing library.json and move pdf files into `kb/raw/literature/pdf`.
