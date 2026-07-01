"""Tests for wiki import (bulk literature import from a Zotero export folder)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from wikitools.commands.bulk_import import run_import
from wikitools.wikilib import load_library_raw

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_extract"


# ── helpers ───────────────────────────────────────────────────────────────────


def _make_kb(tmp_path: Path) -> Path:
    """Copy fixture kb to a writable tmp location."""
    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    return kb


def _make_source(
    tmp_path: Path,
    entries: list[dict[str, object]],
    pdfs: dict[str, bytes],
    *,
    name: str = "zotero_export",
    json_name: str = "library.json",
) -> Path:
    """Build a synthetic Zotero export folder: one CSL JSON file + PDFs."""
    source = tmp_path / name
    source.mkdir()
    (source / json_name).write_text(json.dumps(entries), encoding="utf-8")
    for name, content in pdfs.items():
        (source / name).write_bytes(content)
    return source


def _fake_pdftotext(pdf_path: Path, txt_path: Path, extractor: str = "fast", _converter: object | None = None) -> None:
    """Stand-in for extract_pdf that writes deterministic text without shelling out."""
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path.write_text(f"Extracted text from {pdf_path.name}\n", encoding="utf-8")


# ── add (new citekeys) ────────────────────────────────────────────────────────


def test_run_import_adds_new_citekey(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New Paper"}], {"newPaperBar2026.pdf": b"%PDF-1.4 new"})

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, do_index=False, engine="fast")

    assert report.added == ["newPaperBar2026"]
    assert report.skipped == []
    assert report.replaced == []
    assert report.extracted == 1

    canonical = load_library_raw(kb / "raw" / "literature" / "library.json")
    assert canonical["newPaperBar2026"]["title"] == "New Paper"
    assert (kb / "raw" / "literature" / "pdf" / "newPaperBar2026.pdf").read_bytes() == b"%PDF-1.4 new"
    assert (kb / "raw" / "literature" / "txt" / "newPaperBar2026.txt").exists()


def test_run_import_metadata_only_new_citekey_no_pdf(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "metaOnly2026", "title": "No PDF"}], {})

    report = run_import(kb, source, do_extract=False, do_index=False)

    assert report.added == ["metaOnly2026"]
    canonical = load_library_raw(kb / "raw" / "literature" / "library.json")
    assert "metaOnly2026" in canonical
    assert not (kb / "raw" / "literature" / "pdf" / "metaOnly2026.pdf").exists()


def test_run_import_idempotent_second_run_skips(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    entries = [{"id": f"paper{i}New2026", "title": f"Paper {i}"} for i in range(3)]
    pdfs = {f"paper{i}New2026.pdf": f"%PDF {i}".encode() for i in range(3)}
    source = _make_source(tmp_path, entries, pdfs)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        first = run_import(kb, source, do_index=False, engine="fast")
        second = run_import(kb, source, do_index=False, engine="fast")

    assert len(first.added) == 3
    assert second.added == []
    assert sorted(second.skipped) == sorted(e["id"] for e in entries)
    assert second.extracted == 0


# ── default skip on collision ─────────────────────────────────────────────────


def test_run_import_default_skips_existing_collision(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    original_pdf_bytes = (kb / "raw" / "literature" / "pdf" / "smithExamplePaper2024.pdf").read_bytes()
    original_entry = load_library_raw(kb / "raw" / "literature" / "library.json")["smithExamplePaper2024"]

    source = _make_source(
        tmp_path,
        [{"id": "smithExamplePaper2024", "title": "Replaced Title"}],
        {"smithExamplePaper2024.pdf": b"%PDF-1.4 replaced bytes"},
    )

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, do_index=False, engine="fast")

    assert report.added == []
    assert report.skipped == ["smithExamplePaper2024"]
    assert report.replaced == []
    assert report.extracted == 0

    canonical = load_library_raw(kb / "raw" / "literature" / "library.json")
    assert canonical["smithExamplePaper2024"] == original_entry
    assert (kb / "raw" / "literature" / "pdf" / "smithExamplePaper2024.pdf").read_bytes() == original_pdf_bytes


def test_run_import_orphan_pdf_logged_and_not_copied(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    import logging

    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"orphanPaper9999.pdf": b"%PDF orphan"})

    with caplog.at_level(logging.WARNING), patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, do_index=False, engine="fast")

    assert report.added == ["newPaperBar2026"]
    assert not (kb / "raw" / "literature" / "pdf" / "orphanPaper9999.pdf").exists()
    assert any("orphanPaper9999" in r.message for r in caplog.records)


# ── --force replace ───────────────────────────────────────────────────────────


def test_run_import_force_replaces_existing_collision(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(
        tmp_path,
        [{"id": "smithExamplePaper2024", "title": "Replaced Title"}],
        {"smithExamplePaper2024.pdf": b"%PDF-1.4 replaced bytes"},
    )

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, force=True, do_index=False, engine="fast")

    assert report.added == []
    assert report.replaced == ["smithExamplePaper2024"]
    assert report.skipped == []
    assert report.extracted == 1

    canonical = load_library_raw(kb / "raw" / "literature" / "library.json")
    assert canonical["smithExamplePaper2024"]["title"] == "Replaced Title"
    assert (kb / "raw" / "literature" / "pdf" / "smithExamplePaper2024.pdf").read_bytes() == b"%PDF-1.4 replaced bytes"


def test_run_import_force_identical_bytes_skips_reextraction(tmp_path: Path) -> None:
    from wikitools.commands.extract import run_extract

    kb = _make_kb(tmp_path)
    original_pdf_bytes = (kb / "raw" / "literature" / "pdf" / "smithExamplePaper2024.pdf").read_bytes()

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        run_extract(kb, citekey="smithExamplePaper2024", engine="fast")  # pre-populate sidecar/hash

    source = _make_source(
        tmp_path,
        [{"id": "smithExamplePaper2024", "title": "Same Bytes, New Metadata"}],
        {"smithExamplePaper2024.pdf": original_pdf_bytes},
    )

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext) as mock_extract:
        report = run_import(kb, source, force=True, do_index=False, engine="fast")

    assert report.replaced == ["smithExamplePaper2024"]
    assert report.extracted == 0
    mock_extract.assert_not_called()
    canonical = load_library_raw(kb / "raw" / "literature" / "library.json")
    assert canonical["smithExamplePaper2024"]["title"] == "Same Bytes, New Metadata"


# ── dry-run ────────────────────────────────────────────────────────────────────


def test_run_import_dry_run_writes_nothing(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    library_path = kb / "raw" / "literature" / "library.json"
    original_text = library_path.read_text(encoding="utf-8")
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with patch("wikitools.commands.extract.extract_pdf") as mock_extract:
        report = run_import(kb, source, dry_run=True)

    mock_extract.assert_not_called()
    assert report.added == ["newPaperBar2026"]
    assert report.extracted == 0
    assert report.indexed_files == 0
    assert library_path.read_text(encoding="utf-8") == original_text
    assert not (kb / "raw" / "literature" / "pdf" / "newPaperBar2026.pdf").exists()


# ── index wiring ───────────────────────────────────────────────────────────────


def test_run_import_updates_index_when_changed(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, do_index=True, embedder=None, engine="fast")

    assert report.indexed_files > 0
    assert (kb / ".wiki" / "corpus.duckdb").exists()


def test_run_import_no_index_skips_db(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        report = run_import(kb, source, do_index=False, engine="fast")

    assert report.indexed_files == 0
    assert not (kb / ".wiki" / "corpus.duckdb").exists()


def test_run_import_no_extract_skips_extraction(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with patch("wikitools.commands.extract.extract_pdf") as mock_extract:
        report = run_import(kb, source, do_extract=False, do_index=False)

    mock_extract.assert_not_called()
    assert report.extracted == 0
    assert (kb / "raw" / "literature" / "pdf" / "newPaperBar2026.pdf").exists()
    assert not (kb / "raw" / "literature" / "txt" / "newPaperBar2026.txt").exists()


# ── library file detection ────────────────────────────────────────────────────


def test_run_import_no_json_file_raises(tmp_path: Path) -> None:
    source = tmp_path / "zotero_export"
    source.mkdir()
    (source / "paper.pdf").write_bytes(b"%PDF")
    kb = _make_kb(tmp_path)
    with pytest.raises(ValueError, match="Expected exactly one"):
        run_import(kb, source, do_extract=False, do_index=False)


def test_run_import_multiple_json_files_raises(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026"}], {})
    (source / "extra.json").write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="Expected exactly one"):
        run_import(kb, source, do_extract=False, do_index=False)


def test_run_import_explicit_library_disambiguates(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026"}], {})
    (source / "extra.json").write_text("[]", encoding="utf-8")

    report = run_import(kb, source, library=source / "library.json", do_extract=False, do_index=False)

    assert report.added == ["newPaperBar2026"]


# ── determinism ────────────────────────────────────────────────────────────────


def test_run_import_order_independent_merge(tmp_path: Path) -> None:
    base_a = tmp_path / "scenario_a"
    base_b = tmp_path / "scenario_b"
    base_a.mkdir()
    base_b.mkdir()
    kb_a = _make_kb(base_a)
    kb_b = _make_kb(base_b)

    source1 = _make_source(tmp_path, [{"id": "firstNew2026", "title": "First"}], {"firstNew2026.pdf": b"%PDF 1"}, name="source1")
    source2 = _make_source(tmp_path, [{"id": "secondNew2026", "title": "Second"}], {"secondNew2026.pdf": b"%PDF 2"}, name="source2")

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        run_import(kb_a, source1, do_extract=False, do_index=False)
        run_import(kb_a, source2, do_extract=False, do_index=False)
        run_import(kb_b, source2, do_extract=False, do_index=False)
        run_import(kb_b, source1, do_extract=False, do_index=False)

    text_a = (kb_a / "raw" / "literature" / "library.json").read_text(encoding="utf-8")
    text_b = (kb_b / "raw" / "literature" / "library.json").read_text(encoding="utf-8")
    assert text_a == text_b


# ── CLI integration ───────────────────────────────────────────────────────────


def test_import_cli_dry_run_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib

    from wikitools.cli import main

    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with patch("sys.argv", ["wiki", "--kb", str(kb), "import", str(source), "--dry-run", "--json"]), contextlib.suppress(SystemExit):
        main()

    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["added"] == ["newPaperBar2026"]
    assert data["dry_run"] is True
    assert not (kb / "raw" / "literature" / "pdf" / "newPaperBar2026.pdf").exists()


def test_import_cli_missing_json_exits_nonzero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from wikitools.cli import main

    kb = _make_kb(tmp_path)
    source = tmp_path / "empty_export"
    source.mkdir()

    with patch("sys.argv", ["wiki", "--kb", str(kb), "import", str(source)]), pytest.raises(SystemExit) as exc:
        main()

    assert exc.value.code != 0
    assert "Expected exactly one" in capsys.readouterr().err


def test_import_cli_force_and_extract(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib

    from wikitools.cli import main

    kb = _make_kb(tmp_path)
    source = _make_source(tmp_path, [{"id": "newPaperBar2026", "title": "New"}], {"newPaperBar2026.pdf": b"%PDF new"})

    with (
        patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext),
        patch("sys.argv", ["wiki", "--kb", str(kb), "import", str(source), "--no-index", "--engine", "fast"]),
        contextlib.suppress(SystemExit),
    ):
        main()

    out = capsys.readouterr().out
    assert "added 1" in out
    assert (kb / "raw" / "literature" / "txt" / "newPaperBar2026.txt").exists()
