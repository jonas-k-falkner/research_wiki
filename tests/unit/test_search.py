"""Tests for wiki search command: Hit, _rrf_fuse, search modes."""

from __future__ import annotations

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from wikitools.commands.index import build_index
from wikitools.commands.search import Hit, _rrf_fuse, _snippet, search

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_search"


def _make_kb(tmp_path: Path) -> Path:
    """Copy the kb_search fixture to a writable tmp location."""
    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    return kb


# ── _snippet ──────────────────────────────────────────────────────────────────


def test_snippet_short_text_unchanged() -> None:
    text = "Hello world."
    assert _snippet(text, max_len=200) == "Hello world."


def test_snippet_long_text_truncated() -> None:
    text = "word " * 100
    result = _snippet(text, max_len=50)
    assert len(result) <= 55  # a bit of slack for the ellipsis
    assert result.endswith("…")


def test_snippet_strips_newlines() -> None:
    text = "line one\nline two\nline three"
    result = _snippet(text, max_len=200)
    assert "\n" not in result


# ── _rrf_fuse ─────────────────────────────────────────────────────────────────


def _row(sp: str, ck: str | None, sec: str, text: str = "text") -> tuple:
    return (sp, ck, sec, text)


def test_rrf_fuse_both_empty() -> None:
    result = _rrf_fuse([], [])
    assert result == []


def test_rrf_fuse_lexical_only() -> None:
    lex = [_row("a.md", None, "s1"), _row("b.md", None, "s2")]
    result = _rrf_fuse(lex, [])
    assert len(result) == 2
    sps = [r[0] for r in result]
    assert "a.md" in sps


def test_rrf_fuse_semantic_only() -> None:
    sem = [_row("x.md", "ck1", "s1"), _row("y.md", "ck2", "s2")]
    result = _rrf_fuse([], sem)
    assert len(result) == 2


def test_rrf_fuse_overlap_boosts_score() -> None:
    shared = _row("shared.md", None, "intro")
    unique_lex = _row("only_lex.md", None, "s1")
    unique_sem = _row("only_sem.md", None, "s1")
    lex = [shared, unique_lex]
    sem = [shared, unique_sem]
    result = _rrf_fuse(lex, sem)
    # The shared item should have the highest score (appears in both lists at rank 1)
    assert result[0][0] == "shared.md"


def test_rrf_fuse_score_strictly_higher_for_overlap() -> None:
    shared = _row("shared.md", None, "intro")
    only_lex = _row("only_lex.md", None, "s1")
    result = _rrf_fuse([shared, only_lex], [shared])
    shared_score = next(r[3] for r in result if r[0] == "shared.md")
    only_score = next(r[3] for r in result if r[0] == "only_lex.md")
    assert shared_score > only_score


def test_rrf_fuse_deterministic_tiebreak() -> None:
    a = _row("a.md", None, "s1")
    b = _row("b.md", None, "s1")
    r1 = _rrf_fuse([a, b], [b, a])
    r2 = _rrf_fuse([a, b], [b, a])
    assert [x[0] for x in r1] == [x[0] for x in r2]


def test_rrf_fuse_key_is_source_and_section() -> None:
    # Same source_path but different sections → separate entries
    a1 = _row("a.md", None, "sec1")
    a2 = _row("a.md", None, "sec2")
    result = _rrf_fuse([a1], [a2])
    assert len(result) == 2


# ── search ────────────────────────────────────────────────────────────────────


def test_search_raises_without_index(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    with pytest.raises(FileNotFoundError, match="wiki index build"):
        search("entmax", kb)


def test_search_invalid_mode_raises(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    with pytest.raises(ValueError, match="Unknown search mode"):
        search("entmax", kb, mode="magic")


def test_search_lexical_returns_hits(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = search("entmax", kb, mode="lexical")
    assert isinstance(hits, list)
    assert len(hits) > 0
    assert all(isinstance(h, Hit) for h in hits)


def test_search_lexical_hit_fields(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = search("entmax", kb, mode="lexical")
    for h in hits:
        assert h.source_path
        assert h.section
        assert h.snippet
        assert isinstance(h.score, float)


def test_search_lexical_scope_wiki_excludes_literature(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = search("entmax", kb, mode="lexical", scope="wiki")
    assert all(h.citekey is None for h in hits)


def test_search_lexical_scope_literature_excludes_wiki(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = search("sparse attention", kb, mode="lexical", scope="literature")
    assert all(h.citekey is not None for h in hits)


def test_search_lexical_k_limits_results(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = search("entmax", kb, mode="lexical", k=1)
    assert len(hits) <= 1


def test_search_hybrid_falls_back_without_embedder(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    # Hybrid mode with no embeddings stored → lexical-only RRF (semantic returns [])
    hits = search("entmax", kb, mode="hybrid")
    assert isinstance(hits, list)


def test_search_semantic_without_embedder_returns_empty(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    # No embeddings stored, LocalEmbedder not installed → should return empty list gracefully
    with patch("wikitools.commands.index.LocalEmbedder", side_effect=Exception("not installed")):
        hits = search("entmax", kb, mode="semantic")
    assert hits == []


def test_search_json_output_stable(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    import json
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "search", "entmax", "--mode", "lexical", "--json"]), contextlib.suppress(SystemExit):
        main()

    out1 = capsys.readouterr().out
    with upatch("sys.argv", ["wiki", "--kb", str(kb), "search", "entmax", "--mode", "lexical", "--json"]), contextlib.suppress(SystemExit):
        main()

    out2 = capsys.readouterr().out
    assert out1 == out2, "JSON output not deterministic"

    data = json.loads(out1)
    assert isinstance(data, list)
    if data:
        assert "source_path" in data[0]
        assert "snippet" in data[0]
        assert "score" in data[0]


def test_search_cli_no_index_exits_nonzero(tmp_path: Path) -> None:
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "search", "entmax"]), pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
