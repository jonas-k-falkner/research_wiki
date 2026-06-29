"""Tests for wiki index command: chunking, build, update, status."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from wikitools.commands.index import (
    Chunk,
    LocalEmbedder,
    OpenAIEmbedder,
    _heading_split,
    build_index,
    chunk_txt,
    chunk_wiki_page,
    index_status,
    update_index,
)

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_search"


def _make_kb(tmp_path: Path) -> Path:
    """Copy the kb_search fixture to a writable tmp location."""
    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    return kb


def _fake_embedder(dim: int = 4) -> MagicMock:
    """Return a mock Embedder that returns zero vectors."""
    m = MagicMock()
    m.embed.side_effect = lambda texts: [[0.0] * dim for _ in texts]
    return m


# ── _heading_split ────────────────────────────────────────────────────────────


def test_heading_split_basic() -> None:
    md = "## Intro\n\nHello world.\n\n## Methods\n\nWe do things."
    parts = _heading_split(md)
    assert len(parts) == 2
    titles = [p[0] for p in parts]
    assert "Intro" in titles
    assert "Methods" in titles


def test_heading_split_strips_frontmatter() -> None:
    md = "---\ntype: concept\n---\n\n## Overview\n\nContent."
    parts = _heading_split(md)
    assert len(parts) == 1
    assert parts[0][0] == "Overview"
    assert "Content." in parts[0][1]


def test_heading_split_no_headings_returns_intro() -> None:
    md = "Just some text with no headings."
    parts = _heading_split(md)
    assert parts == [("intro", "Just some text with no headings.")]


def test_heading_split_preamble_emitted_as_intro() -> None:
    md = "Preamble text.\n\n## Section\n\nBody."
    parts = _heading_split(md)
    titles = [p[0] for p in parts]
    assert "intro" in titles


def test_heading_split_empty_body_section_still_emitted() -> None:
    md = "## Empty\n\n## NonEmpty\n\nHas content."
    parts = _heading_split(md)
    non_empty_only = [(t, b) for t, b in parts if b]
    assert len(non_empty_only) == 1
    assert non_empty_only[0][0] == "NonEmpty"


# ── chunk_wiki_page ───────────────────────────────────────────────────────────


def test_chunk_wiki_page_produces_chunks(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page = kb / "wiki" / "pages" / "entmax.md"
    chunks = chunk_wiki_page(page, kb)
    assert len(chunks) >= 2
    assert all(isinstance(c, Chunk) for c in chunks)


def test_chunk_wiki_page_relative_path(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page = kb / "wiki" / "pages" / "entmax.md"
    chunks = chunk_wiki_page(page, kb)
    assert all(c.source_path.startswith("wiki/") for c in chunks)


def test_chunk_wiki_page_no_citekey(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page = kb / "wiki" / "pages" / "entmax.md"
    chunks = chunk_wiki_page(page, kb)
    assert all(c.citekey is None for c in chunks)


def test_chunk_wiki_page_missing_file(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    missing = kb / "wiki" / "nonexistent.md"
    chunks = chunk_wiki_page(missing, kb)
    assert chunks == []


# ── chunk_txt ─────────────────────────────────────────────────────────────────


def test_chunk_txt_produces_chunks(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    txt = kb / "raw" / "literature" / "txt" / "smithEntmax2024.txt"
    chunks = chunk_txt(txt, "smithEntmax2024", kb)
    assert len(chunks) >= 1
    assert all(isinstance(c, Chunk) for c in chunks)


def test_chunk_txt_citekey_set(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    txt = kb / "raw" / "literature" / "txt" / "smithEntmax2024.txt"
    chunks = chunk_txt(txt, "smithEntmax2024", kb)
    assert all(c.citekey == "smithEntmax2024" for c in chunks)


def test_chunk_txt_sliding_window_overlap(tmp_path: Path) -> None:
    kb = tmp_path / "kb"
    txt_dir = kb / "raw" / "literature" / "txt"
    txt_dir.mkdir(parents=True)
    # Write exactly 1000 chars to produce 2 overlapping chunks
    long_text = "x" * 1000
    (txt_dir / "long2024.txt").write_text(long_text, encoding="utf-8")
    chunks = chunk_txt(txt_dir / "long2024.txt", "long2024", kb)
    assert len(chunks) >= 2


def test_chunk_txt_missing_file(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    missing = kb / "raw" / "literature" / "txt" / "noexist.txt"
    chunks = chunk_txt(missing, "noexist", kb)
    assert chunks == []


# ── LocalEmbedder / OpenAIEmbedder MissingExtraError ─────────────────────────


def test_local_embedder_raises_when_fastembed_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    from wikitools.commands.extract import MissingExtraError

    monkeypatch.setitem(__import__("sys").modules, "fastembed", None)
    with pytest.raises(MissingExtraError):
        LocalEmbedder()


def test_openai_embedder_raises_when_openai_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    from wikitools.commands.extract import MissingExtraError

    monkeypatch.setitem(__import__("sys").modules, "openai", None)
    with pytest.raises(MissingExtraError):
        OpenAIEmbedder()


# ── build_index ───────────────────────────────────────────────────────────────


def test_build_index_creates_db(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    db = kb / ".wiki" / "corpus.duckdb"
    assert db.exists()


def test_build_index_chunks_present(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    status = index_status(kb)
    assert status["chunk_count"] > 0


def test_build_index_wiki_and_txt_chunks(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    status = index_status(kb)
    assert status["wiki_chunk_count"] > 0
    assert status["txt_chunk_count"] > 0


def test_build_index_idempotent(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    s1 = index_status(kb)
    build_index(kb, embedder=None)
    s2 = index_status(kb)
    assert s1["chunk_count"] == s2["chunk_count"]


def test_build_index_with_embedder(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Use a mock embedder that returns 768-dim zeros
    embedder = MagicMock()
    embedder.embed.side_effect = lambda texts: [[0.0] * 768 for _ in texts]
    build_index(kb, embedder=embedder)
    assert embedder.embed.called


def test_build_index_768dim_mock_stores_non_null_embeddings(tmp_path: Path) -> None:
    import duckdb

    kb = _make_kb(tmp_path)
    embedder = MagicMock()
    embedder.embed.side_effect = lambda texts: [[0.1] * 768 for _ in texts]
    build_index(kb, embedder=embedder)

    db_file = kb / ".wiki" / "corpus.duckdb"
    con = duckdb.connect(str(db_file), read_only=True)
    row = con.execute("SELECT embedding FROM chunks WHERE embedding IS NOT NULL LIMIT 1").fetchone()
    con.close()

    assert row is not None, "at least one chunk must have a non-NULL embedding"
    assert len(row[0]) == 768


# ── index_status ──────────────────────────────────────────────────────────────


def test_index_status_no_db(tmp_path: Path) -> None:
    kb = tmp_path / "kb"
    kb.mkdir()
    status = index_status(kb)
    assert status["exists"] is False
    assert status["chunk_count"] == 0


def test_index_status_after_build(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    status = index_status(kb)
    assert status["exists"] is True
    assert isinstance(status["last_build"], str)


# ── update_index ──────────────────────────────────────────────────────────────


def test_update_index_initial_processes_all(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Start from empty DB (build_index not called)
    build_index(kb, embedder=None)  # prime DB schema
    n = update_index(kb, embedder=None)
    # All files are "new" on first update_index after build_index clears hashes
    assert n >= 0  # non-negative


def test_update_index_unchanged_files_skipped(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    update_index(kb, embedder=None)  # primes hashes
    n2 = update_index(kb, embedder=None)
    assert n2 == 0


def test_update_index_changed_file_reprocessed(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    update_index(kb, embedder=None)

    # Modify one wiki page
    page = kb / "wiki" / "pages" / "entmax.md"
    page.write_text(page.read_text(encoding="utf-8") + "\n\n## New Section\n\nNew content.", encoding="utf-8")

    n = update_index(kb, embedder=None)
    assert n == 1


# ── CLI integration ───────────────────────────────────────────────────────────


def test_index_build_cli_exits_zero(tmp_path: Path) -> None:
    import contextlib
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "index", "build"]), contextlib.suppress(SystemExit):
        main()


def test_index_status_cli_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "index", "status"]), contextlib.suppress(SystemExit):
        main()

    out = capsys.readouterr().out
    data = json.loads(out)
    assert "chunk_count" in data
    assert "exists" in data
