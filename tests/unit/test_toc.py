"""Tests for wiki toc command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from wikitools.commands.toc import (
    _AUTO_END,
    _AUTO_START,
    _rewrite_auto_region,
    build_toc,
    generate_domain_index,
    generate_root,
)
from wikitools.wikilib import iter_pages

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_toc"


# ── _rewrite_auto_region ──────────────────────────────────────────────────────


def test_rewrite_replaces_existing_region() -> None:
    existing = f"Before\n{_AUTO_START}\nold content\n{_AUTO_END}\nAfter\n"
    result = _rewrite_auto_region(existing, "new content")
    assert "new content" in result
    assert "old content" not in result
    assert result.startswith("Before\n")
    assert "After\n" in result


def test_rewrite_appends_when_no_fences() -> None:
    existing = "# Title\n\nSome prose.\n"
    result = _rewrite_auto_region(existing, "generated")
    assert _AUTO_START in result
    assert _AUTO_END in result
    assert "generated" in result
    assert "Some prose." in result


def test_rewrite_preserves_prose_outside_fences() -> None:
    existing = f"# Intro\n\nHuman.\n\n{_AUTO_START}\nold\n{_AUTO_END}\n\nFooter.\n"
    result = _rewrite_auto_region(existing, "fresh")
    assert "Human." in result
    assert "Footer." in result
    assert "old" not in result
    assert "fresh" in result


def test_rewrite_idempotent() -> None:
    existing = f"Prose.\n{_AUTO_START}\ncontent\n{_AUTO_END}\n"
    first = _rewrite_auto_region(existing, "content")
    second = _rewrite_auto_region(first, "content")
    assert first == second


# ── generate_domain_index ─────────────────────────────────────────────────────


def test_generate_domain_index_ts_domain() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_domain_index(pages, "timeseries-forecasting", FIXTURES)
    assert "timeseries-forecasting" in result.lower() or "Time-series" in result
    # Both ts pages appear
    assert "P1 — Deep models" in result or "p1-deep-models" in result
    assert "TS Concept" in result or "tsconcept" in result


def test_generate_domain_index_excludes_other_domains() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_domain_index(pages, "timeseries-forecasting", FIXTURES)
    assert "Embedding Concept" not in result


def test_generate_domain_index_contains_table_header() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_domain_index(pages, "embedding-models", FIXTURES)
    assert "| Title |" in result
    assert "| Type |" in result
    assert "| Stage |" in result


def test_generate_domain_index_rollup_line() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_domain_index(pages, "timeseries-forecasting", FIXTURES)
    assert "page(s)" in result


# ── generate_root ─────────────────────────────────────────────────────────────


def test_generate_root_contains_all_domains() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_root(pages, FIXTURES)
    assert "timeseries-forecasting" in result or "Time-series" in result
    assert "embedding-models" in result or "Embedding" in result


def test_generate_root_links_to_domain_indexes() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_root(pages, FIXTURES)
    assert "domains/timeseries-forecasting/index.md" in result
    assert "domains/embedding-models/index.md" in result


def test_generate_root_includes_shared_pages() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_root(pages, FIXTURES)
    assert "Strategy" in result or "strategy" in result


def test_generate_root_total_line() -> None:
    pages = list(iter_pages(FIXTURES))
    result = generate_root(pages, FIXTURES)
    assert "total pages" in result


# ── build_toc ─────────────────────────────────────────────────────────────────


def test_build_toc_creates_domain_indexes(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    changed = build_toc(kb)
    assert changed is True

    ts_index = kb / "wiki" / "domains" / "timeseries-forecasting" / "index.md"
    emb_index = kb / "wiki" / "domains" / "embedding-models" / "index.md"
    assert ts_index.exists()
    assert emb_index.exists()


def test_build_toc_idempotent(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    build_toc(kb)
    changed_second = build_toc(kb)
    assert changed_second is False


def test_build_toc_updates_root_index(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    build_toc(kb)

    root_text = (kb / "wiki" / "index.md").read_text(encoding="utf-8")
    assert _AUTO_START in root_text
    assert _AUTO_END in root_text
    assert "Human prose that must survive regeneration." in root_text


def test_build_toc_preserves_prose_outside_fences(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    build_toc(kb)
    root_text = (kb / "wiki" / "index.md").read_text(encoding="utf-8")
    assert "Human prose that must survive regeneration." in root_text
    assert "Manual section outside fences." in root_text


def test_build_toc_check_mode_detects_stale(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    # First check: stale (domain indexes don't exist yet)
    changed = build_toc(kb, check=True)
    assert changed is True
    # Files not written in check mode
    ts_index = kb / "wiki" / "domains" / "timeseries-forecasting" / "index.md"
    assert not ts_index.exists()


def test_build_toc_check_mode_exits_zero_when_fresh(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    build_toc(kb)
    changed = build_toc(kb, check=True)
    assert changed is False


def test_build_toc_new_domain_no_code_change(tmp_path: Path) -> None:
    import shutil

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    build_toc(kb)

    # Add page with new domain
    new_page = kb / "wiki" / "concepts" / "new-domain-concept.md"
    new_page.write_text(
        "---\n"
        "type: concept\n"
        "domain: scenario-engine\n"
        "project: P3\n"
        "status: draft\n"
        "stage: seed\n"
        "confidence: low\n"
        "updated: 2026-06-27\n"
        "sources: []\n"
        "tags: []\n"
        "---\n\n# Scenario Concept\n\nNew domain page.\n",
        encoding="utf-8",
    )

    changed = build_toc(kb)
    assert changed is True
    scenario_index = kb / "wiki" / "domains" / "scenario-engine" / "index.md"
    assert scenario_index.exists()
    assert "Scenario Concept" in scenario_index.read_text(encoding="utf-8")


def test_build_toc_raises_on_missing_wiki(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No wiki/"):
        build_toc(tmp_path / "nonexistent")


# ── CLI integration ───────────────────────────────────────────────────────────


def test_toc_build_cli_exits_zero(tmp_path: Path) -> None:
    import shutil

    from wikitools.cli import main

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    with patch("sys.argv", ["wiki", "--kb", str(kb), "toc", "build"]):
        try:
            main()
        except SystemExit as exc:
            assert exc.code in (None, 0)


def test_toc_build_check_nonzero_when_stale(tmp_path: Path) -> None:
    import shutil

    from wikitools.cli import main

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    with patch("sys.argv", ["wiki", "--kb", str(kb), "toc", "build", "--check"]), pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_toc_build_check_zero_when_fresh(tmp_path: Path) -> None:
    import shutil

    from wikitools.cli import main

    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)

    build_toc(kb)

    with patch("sys.argv", ["wiki", "--kb", str(kb), "toc", "build", "--check"]):
        try:
            main()
        except SystemExit as exc:
            assert exc.code in (None, 0)


@pytest.mark.integration
def test_toc_build_real_kb_no_errors() -> None:
    """Build TOC on the real kb and verify idempotency."""
    import subprocess

    result = subprocess.run(
        ["uv", "run", "wiki", "toc", "build", "--check"],
        capture_output=True,
        text=True,
    )
    # Should exit 0 if indexes are up-to-date (run `wiki toc build` first)
    assert result.returncode == 0, result.stderr
