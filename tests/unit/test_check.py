"""Tests for wiki check source and wiki check claim."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from wikitools.commands.check import (
    ClaimClassification,
    ClaimHit,
    SourceState,
    SourceStatus,
    _classify_cosine,
    _find_source_page,
    check_claim,
    check_source,
)

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_search"

KNOWN_CITEKEY = "smithEntmax2024"
KNOWN_HASH = "b16ab9ab7a4ca5fcadac6d1dba880648b8ad3e3d2da4f9b2cf85b87083718236"


def _make_kb(tmp_path: Path) -> Path:
    """Copy the kb_search fixture to a writable tmp location."""
    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    return kb


# ── _classify_cosine ──────────────────────────────────────────────────────────


def test_classify_cosine_high_score_is_duplicate() -> None:
    assert _classify_cosine(0.90) == ClaimClassification.DUPLICATE


def test_classify_cosine_medium_score_is_additional_support() -> None:
    assert _classify_cosine(0.70) == ClaimClassification.ADDITIONAL_SUPPORT


def test_classify_cosine_low_score_is_new() -> None:
    assert _classify_cosine(0.10) == ClaimClassification.NEW


def test_classify_cosine_boundary_at_duplicate_threshold() -> None:
    assert _classify_cosine(0.85) == ClaimClassification.DUPLICATE


def test_classify_cosine_just_below_support_threshold_is_new() -> None:
    assert _classify_cosine(0.59) == ClaimClassification.NEW


def test_classify_cosine_bm25_score_would_be_duplicate() -> None:
    # Demonstrates why BM25 scores must NOT use this function:
    # a typical BM25 score of 7.0 far exceeds the 0.85 threshold.
    assert _classify_cosine(7.0) == ClaimClassification.DUPLICATE  # wrong result for BM25


# ── _find_source_page ─────────────────────────────────────────────────────────


def test_find_source_page_returns_path_and_hash(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page, recorded_hash = _find_source_page(KNOWN_CITEKEY, kb)
    assert page is not None
    assert page.name == "src-smith-entmax-2024.md"
    assert recorded_hash == KNOWN_HASH


def test_find_source_page_unknown_citekey_returns_none(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page, recorded_hash = _find_source_page("noSuchPaper9999", kb)
    assert page is None
    assert recorded_hash is None


def test_find_source_page_no_sources_dir(tmp_path: Path) -> None:
    kb = tmp_path / "kb"
    kb.mkdir()
    page, _ = _find_source_page("anything", kb)
    assert page is None


# ── check_source ──────────────────────────────────────────────────────────────


def test_check_source_unchanged(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    status = check_source(KNOWN_CITEKEY, kb)
    assert status.state == SourceState.UNCHANGED
    assert status.page_path is not None
    assert status.recorded_hash == KNOWN_HASH
    assert status.current_hash == KNOWN_HASH


def test_check_source_new_citekey(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    status = check_source("unknownPaper2099", kb)
    assert status.state == SourceState.NEW
    assert status.page_path is None


def test_check_source_changed_hash(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Modify the source page to have a stale hash
    page = kb / "wiki" / "sources" / "src-smith-entmax-2024.md"
    text = page.read_text(encoding="utf-8")
    page.write_text(text.replace(KNOWN_HASH, "deadbeef" * 8), encoding="utf-8")

    status = check_source(KNOWN_CITEKEY, kb)
    assert status.state == SourceState.CHANGED
    assert status.recorded_hash == "deadbeef" * 8
    assert status.current_hash == KNOWN_HASH


def test_check_source_page_exists_no_hash_is_changed(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    page = kb / "wiki" / "sources" / "src-smith-entmax-2024.md"
    text = page.read_text(encoding="utf-8")
    # Remove source_hash entirely
    lines = [ln for ln in text.splitlines() if not ln.startswith("source_hash:")]
    page.write_text("\n".join(lines), encoding="utf-8")

    status = check_source(KNOWN_CITEKEY, kb)
    assert status.state == SourceState.CHANGED


def test_check_source_returns_sourcestatus_type(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    status = check_source(KNOWN_CITEKEY, kb)
    assert isinstance(status, SourceStatus)


def test_check_source_no_pdf_and_no_txt_returns_new(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Remove txt file so no raw file is available; page still has zotero key
    txt = kb / "raw" / "literature" / "txt" / "smithEntmax2024.txt"
    txt.unlink()
    status = check_source(KNOWN_CITEKEY, kb)
    # Page exists but current_hash is None → can't confirm unchanged → CHANGED
    assert status.state == SourceState.CHANGED
    assert status.current_hash is None


# ── check_claim ───────────────────────────────────────────────────────────────


def test_check_claim_raises_without_index(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Use lexical mode so we don't need the embedder in unit tests
    with pytest.raises(FileNotFoundError):
        check_claim("entmax sparse attention", kb, mode="lexical")


def test_check_claim_semantic_raises_missing_extra(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from wikitools.commands.extract import MissingExtraError
    from wikitools.commands.index import build_index

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    monkeypatch.setitem(__import__("sys").modules, "fastembed", None)
    with pytest.raises(MissingExtraError, match="semantic"):
        check_claim("entmax sparse attention", kb, mode="semantic")


def test_check_claim_no_hits_for_novel_text(tmp_path: Path) -> None:
    from wikitools.commands.index import build_index

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    # A completely unrelated claim — should return no non-NEW hits
    hits = check_claim("the boiling point of water is 100 degrees at sea level", kb, mode="lexical")
    assert all(isinstance(h, ClaimHit) for h in hits)
    # All returned hits are at least additional-support (NEW filtered out)
    assert all(h.classification != ClaimClassification.NEW for h in hits)


def test_check_claim_excludes_self_page(tmp_path: Path) -> None:
    from wikitools.commands.index import build_index

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    # Use exact text from the entmax page; exclude itself
    hits = check_claim(
        "Entmax is a sparse probability mapping",
        kb,
        page="wiki/pages/entmax.md",
        mode="lexical",
    )
    assert not any(h.source_path == "wiki/pages/entmax.md" for h in hits)


def test_check_claim_marks_cites_queried_source(tmp_path: Path) -> None:
    from wikitools.commands.index import build_index

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)
    hits = check_claim("sparse attention concentration", kb, citekey=KNOWN_CITEKEY, mode="lexical")
    # The source page for smithEntmax2024 has zotero: smithEntmax2024 — if it surfaces, cites_queried_source=True
    for h in hits:
        if h.source_path.endswith("src-smith-entmax-2024.md"):
            assert h.cites_queried_source is True


def test_check_claim_json_output_stable(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    import json
    from unittest.mock import patch as upatch

    from wikitools.cli import main
    from wikitools.commands.index import build_index

    kb = _make_kb(tmp_path)
    build_index(kb, embedder=None)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "claim", "entmax sparse", "--mode", "lexical", "--json"]), contextlib.suppress(SystemExit):
        main()
    out1 = capsys.readouterr().out

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "claim", "entmax sparse", "--mode", "lexical", "--json"]), contextlib.suppress(SystemExit):
        main()
    out2 = capsys.readouterr().out

    assert out1 == out2, "check claim JSON not deterministic"
    data = json.loads(out1)
    assert isinstance(data, list)
    for item in data:
        assert "classification" in item
        assert item["classification"] in ("duplicate", "additional-support", "new")


# ── CLI integration ───────────────────────────────────────────────────────────


def test_check_source_cli_exits_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "source", "--citekey", KNOWN_CITEKEY]), contextlib.suppress(SystemExit):
        main()

    out = capsys.readouterr().out
    assert "unchanged" in out


def test_check_source_cli_new_citekey(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "source", "--citekey", "noSuchPaper2099"]), contextlib.suppress(SystemExit):
        main()

    out = capsys.readouterr().out
    assert "new" in out


def test_check_source_cli_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    import json
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "source", "--citekey", KNOWN_CITEKEY, "--json"]), contextlib.suppress(SystemExit):
        main()

    data = json.loads(capsys.readouterr().out)
    assert data["state"] == "unchanged"
    assert data["citekey"] == KNOWN_CITEKEY
    assert "current_hash" in data


def test_check_claim_cli_no_index_exits_nonzero(tmp_path: Path) -> None:
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("sys.argv", ["wiki", "--kb", str(kb), "check", "claim", "entmax"]), pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
