"""Integration tests for semantic search (require [semantic] extra).

Uses the small kb_search fixture (~3 wiki pages + 1 txt file, ~15 chunks total)
so embedding takes a few seconds.  The production kb/.wiki/corpus.duckdb is never
touched — all builds go to session-scoped tmp dirs.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

# Module-level skip so pytest never tries to run the session fixture when
# fastembed is absent (session fixtures evaluate before function-scoped autouse).
pytest.importorskip("fastembed", reason="[semantic] extra not installed — run: uv sync --extra semantic")

from wikitools.commands.index import LocalEmbedder, build_index, index_status, update_index
from wikitools.commands.search import search

_FIXTURE_KB = Path(__file__).parent.parent / "fixtures" / "kb_search"


@pytest.fixture(scope="session")
def indexed_kb(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Copy fixture kb to tmp and build a semantic index once per test session."""
    kb = tmp_path_factory.mktemp("semantic_kb") / "kb"
    shutil.copytree(_FIXTURE_KB, kb)
    build_index(kb, embedder=LocalEmbedder())
    return kb


@pytest.mark.integration
def test_build_index_with_fastembed(indexed_kb: Path) -> None:
    """Index built with fastembed has a named embed_model and at least one non-NULL embedding."""
    import duckdb

    status = index_status(indexed_kb)
    assert status["exists"] is True
    assert status["chunk_count"] > 0
    assert status["embed_model"] not in (None, "none")

    db_file = indexed_kb / ".wiki" / "corpus.duckdb"
    con = duckdb.connect(str(db_file), read_only=True)
    row = con.execute("SELECT COUNT(*) FROM chunks WHERE embedding IS NOT NULL").fetchone()
    con.close()
    assert row is not None and row[0] > 0


@pytest.mark.integration
def test_search_semantic_recall(indexed_kb: Path) -> None:
    """Semantic search returns the entmax page for a paraphrase query with no shared exact terms."""
    # Query describes the concept without using "sparse", "probability", or "entmax".
    hits = search(
        "neural mechanism that assigns zero weight to non-salient inputs",
        indexed_kb,
        k=5,
        mode="semantic",
        scope="wiki",
    )
    paths = [h.source_path for h in hits]
    assert any("entmax" in p for p in paths), f"entmax page not in semantic top-5: {paths}"


@pytest.mark.integration
def test_search_hybrid_beats_lexical_on_paraphrase(indexed_kb: Path) -> None:
    """A zero-overlap paraphrase surfaces in hybrid (RRF) but not in lexical BM25 top-5."""
    # "predictor", "outcome", "metric space" have no overlap with causal-embeddings.md terms.
    query = "flow of dependency from predictor to outcome captured in metric space"

    lexical_hits = search(query, indexed_kb, k=5, mode="lexical", scope="wiki")
    hybrid_hits = search(query, indexed_kb, k=5, mode="hybrid", scope="wiki")

    lexical_paths = {h.source_path for h in lexical_hits}
    hybrid_paths = {h.source_path for h in hybrid_hits}

    target = "causal-embeddings"
    assert not any(target in p for p in lexical_paths), f"lexical should miss the target for a zero-overlap query, got: {lexical_paths}"
    assert any(target in p for p in hybrid_paths), f"hybrid should surface the target via semantic component, got: {hybrid_paths}"


@pytest.mark.integration
def test_update_index_with_embedder(tmp_path: Path) -> None:
    """update_index with a real embedder reprocesses exactly the changed file with embeddings."""
    import duckdb

    kb = tmp_path / "kb"
    shutil.copytree(_FIXTURE_KB, kb)
    embedder = LocalEmbedder()

    build_index(kb, embedder=embedder)
    update_index(kb, embedder=embedder)  # prime file_hashes table

    # Modify exactly one wiki page
    page = kb / "wiki" / "pages" / "entmax.md"
    original = page.read_text(encoding="utf-8")
    page.write_text(original + "\n\n## Additional notes\n\nAdded in integration test.", encoding="utf-8")

    n = update_index(kb, embedder=embedder)
    assert n == 1, f"expected exactly 1 file reprocessed, got {n}"

    db_file = kb / ".wiki" / "corpus.duckdb"
    con = duckdb.connect(str(db_file), read_only=True)
    row = con.execute("SELECT COUNT(*) FROM chunks WHERE source_path LIKE '%entmax%' AND embedding IS NOT NULL").fetchone()
    con.close()
    assert row is not None and row[0] > 0, "updated chunks must have non-NULL embeddings"
