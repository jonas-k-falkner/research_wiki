"""Tests for wiki extract command."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from wikitools.commands.extract import (
    MissingExtraError,
    _get_engine_version,
    _resolve_engine,
    extract_pdf,
    run_extract,
    run_reconciliation,
)

FIXTURES = Path(__file__).parent.parent / "fixtures" / "kb_extract"


# ── helpers ───────────────────────────────────────────────────────────────────


def _make_kb(tmp_path: Path) -> Path:
    """Copy fixture kb to a writable tmp location."""
    kb = tmp_path / "kb"
    shutil.copytree(FIXTURES, kb)
    return kb


def _fake_pdftotext(pdf_path: Path, txt_path: Path, extractor: str = "fast") -> None:
    """Stand-in for extract_pdf that writes deterministic text without shelling out."""
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    txt_path.write_text(f"Extracted text from {pdf_path.name}\n", encoding="utf-8")


# ── run_reconciliation ────────────────────────────────────────────────────────


def test_reconciliation_detects_txt_missing(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    issues = run_reconciliation(kb)
    kinds = {i.kind for i in issues}
    assert "txt-missing" in kinds


def test_reconciliation_no_issues_when_all_present(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    txt_dir = kb / "raw" / "literature" / "txt"
    txt_dir.mkdir(parents=True, exist_ok=True)
    # Write stubs for both PDFs
    for stem in ("smithExamplePaper2024", "jonesSupplement2023-suppl"):
        (txt_dir / f"{stem}.txt").write_text("text", encoding="utf-8")
    issues = run_reconciliation(kb)
    txt_issues = [i for i in issues if i.kind == "txt-missing"]
    assert txt_issues == []


def test_reconciliation_flags_pdf_not_in_library(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # Add a PDF whose citekey is not in library.json
    rogue = kb / "raw" / "literature" / "pdf" / "unknownPaper9999.pdf"
    rogue.write_bytes(b"%PDF-1.4 fake")
    issues = run_reconciliation(kb)
    kinds = {i.kind for i in issues}
    assert "pdf-missing-from-library" in kinds


def test_reconciliation_metadata_only_not_flagged(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    # brownMetadataOnly2022 has no PDF — this is intentional; should not be flagged
    issues = run_reconciliation(kb)
    paths = {i.path for i in issues}
    assert not any("brownMetadataOnly" in p for p in paths)


def test_reconciliation_empty_pdf_dir(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    shutil.rmtree(kb / "raw" / "literature" / "pdf")
    issues = run_reconciliation(kb)
    assert issues == []


def test_reconciliation_returns_sorted(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    issues = run_reconciliation(kb)
    assert issues == sorted(issues)


# ── extract_pdf ───────────────────────────────────────────────────────────────


def test_extract_pdf_fast_calls_subprocess(tmp_path: Path) -> None:
    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    txt = tmp_path / "test.txt"

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        extract_pdf(pdf, txt, extractor="fast")

    mock_run.assert_called_once()
    call_args = mock_run.call_args[0][0]
    assert call_args[0] == "pdftotext"
    assert str(pdf) in call_args
    assert str(txt) in call_args


def test_extract_pdf_fast_creates_parent(tmp_path: Path) -> None:
    pdf = tmp_path / "src.pdf"
    pdf.write_bytes(b"%PDF-1.4")
    txt = tmp_path / "subdir" / "out.txt"

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        extract_pdf(pdf, txt, extractor="fast")

    assert txt.parent.exists()


def test_extract_pdf_fast_raises_on_nonzero_exit(tmp_path: Path) -> None:
    pdf = tmp_path / "bad.pdf"
    pdf.write_bytes(b"not a pdf")
    txt = tmp_path / "out.txt"

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stderr="Syntax Error")
        with pytest.raises(RuntimeError, match="pdftotext failed"):
            extract_pdf(pdf, txt, extractor="fast")


def test_extract_pdf_unknown_engine_raises(tmp_path: Path) -> None:
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF")
    with pytest.raises(ValueError, match="Unknown extractor"):
        extract_pdf(pdf, tmp_path / "x.txt", extractor="unknown")


def test_extract_pdf_ocr_engine_raises_missing_extra(tmp_path: Path) -> None:
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF")

    with patch.dict("sys.modules", {"docling": None, "marker": None}), pytest.raises(MissingExtraError):
        extract_pdf(pdf, tmp_path / "x.txt", extractor="docling")


# ── run_extract ───────────────────────────────────────────────────────────────


def test_run_extract_writes_txt_and_sidecar(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        extracted, _skipped, _issues = run_extract(kb)

    assert extracted == 2
    txt_dir = kb / "raw" / "literature" / "txt"
    assert (txt_dir / "smithExamplePaper2024.txt").exists()
    assert (txt_dir / "smithExamplePaper2024.extract.json").exists()


def test_run_extract_sidecar_contains_extractor_and_hash(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        run_extract(kb)

    sidecar = kb / "raw" / "literature" / "txt" / "smithExamplePaper2024.extract.json"
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    assert data["extractor"] == "fast"
    assert "source_hash" in data
    assert len(data["source_hash"]) == 64  # SHA-256 hex
    assert "engine_version" in data


def test_run_extract_idempotent_skips_on_second_run(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        extracted1, _sk1, _ = run_extract(kb)
        extracted2, skipped2, _ = run_extract(kb)

    assert extracted1 == 2
    assert extracted2 == 0
    assert skipped2 == 2


def test_run_extract_force_reextracts(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        run_extract(kb)
        extracted, _sk, _ = run_extract(kb, force=True)

    assert extracted == 2


def test_run_extract_citekey_filter(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        extracted, _sk, _ = run_extract(kb, citekey="smithExamplePaper2024")

    assert extracted == 1
    txt_dir = kb / "raw" / "literature" / "txt"
    assert (txt_dir / "smithExamplePaper2024.txt").exists()
    # suppl belongs to jonesSupplement2023 — different citekey, should not be extracted
    assert not (txt_dir / "jonesSupplement2023-suppl.txt").exists()


def test_run_extract_failed_pdf_is_non_fatal(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)

    call_count = 0

    def flaky_extract(pdf_path: Path, txt_path: Path, extractor: str = "pdftotext") -> None:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("simulated failure")
        _fake_pdftotext(pdf_path, txt_path, extractor)

    with patch("wikitools.commands.extract.extract_pdf", side_effect=flaky_extract):
        extracted, _sk, _ = run_extract(kb)

    # One succeeded despite one failing
    assert extracted == 1


def test_run_extract_no_pdf_dir(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    shutil.rmtree(kb / "raw" / "literature" / "pdf")

    with patch("wikitools.commands.extract.extract_pdf") as mock_ext:
        extracted, _sk, _ = run_extract(kb)

    mock_ext.assert_not_called()
    assert extracted == 0


def test_run_extract_returns_reconciliation_issues(tmp_path: Path) -> None:
    kb = _make_kb(tmp_path)
    rogue = kb / "raw" / "literature" / "pdf" / "noSuchCitekey9999.pdf"
    rogue.write_bytes(b"%PDF-1.4 fake")

    with patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext):
        _, _, issues = run_extract(kb)

    kinds = {i.kind for i in issues}
    assert "pdf-missing-from-library" in kinds


# ── CLI integration ───────────────────────────────────────────────────────────


def test_extract_cli_exits_zero(tmp_path: Path) -> None:
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with upatch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext), upatch("sys.argv", ["wiki", "--kb", str(kb), "extract"]):
        try:
            main()
        except SystemExit as exc:
            assert exc.code in (None, 0)


def test_extract_cli_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    import contextlib

    with (
        upatch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext),
        upatch("sys.argv", ["wiki", "--kb", str(kb), "extract", "--json"]),
        contextlib.suppress(SystemExit),
    ):
        main()

    out = capsys.readouterr().out
    data = json.loads(out)
    assert "extracted" in data
    assert "skipped" in data
    assert "reconciliation_issues" in data


# ── engine resolution ────────────────────────────────────────────────────────


def test_resolve_engine_explicit_fast() -> None:
    engine, degraded = _resolve_engine("fast")
    assert engine == "fast"
    assert degraded is False


def test_resolve_engine_explicit_docling_not_installed() -> None:
    with patch.dict("sys.modules", {"docling": None}):
        engine, degraded = _resolve_engine("docling")
    # Explicit request: no degraded flag (caller asked for docling explicitly)
    assert engine == "docling"
    assert degraded is False


def test_resolve_engine_auto_falls_back_to_fast_when_docling_absent() -> None:
    with patch.dict("sys.modules", {"docling": None}):
        engine, degraded = _resolve_engine(None)
    assert engine == "fast"
    assert degraded is True


def test_resolve_engine_auto_returns_docling_when_available() -> None:
    import types

    fake_docling = types.ModuleType("docling")
    fake_docling.__version__ = "2.0.0"  # type: ignore[attr-defined]
    with patch.dict("sys.modules", {"docling": fake_docling}):
        engine, degraded = _resolve_engine(None)
    assert engine == "docling"
    assert degraded is False


def test_get_engine_version_fast_returns_string() -> None:
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stderr="pdftotext version 24.02.0\n", stdout="")
        version = _get_engine_version("fast")
    assert "pdftotext" in version


def test_get_engine_version_unknown_engine() -> None:
    version = _get_engine_version("unknown-engine")
    assert version == "unknown-engine"


# ── docling engine path ───────────────────────────────────────────────────────


def test_extract_pdf_docling_raises_missing_extra(tmp_path: Path) -> None:
    pdf = tmp_path / "x.pdf"
    pdf.write_bytes(b"%PDF")

    with patch.dict("sys.modules", {"docling": None, "docling.document_converter": None}), pytest.raises(MissingExtraError):
        extract_pdf(pdf, tmp_path / "x.txt", extractor="docling")


def test_extract_pdf_docling_writes_markdown(tmp_path: Path) -> None:
    pdf = tmp_path / "math.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake")
    txt = tmp_path / "math.txt"

    fake_doc = MagicMock()
    fake_doc.document.export_to_markdown.return_value = "# Title\n\n$$E = mc^2$$\n"
    fake_converter_cls = MagicMock(return_value=MagicMock(**{"convert.return_value": fake_doc}))

    import types

    fake_docling_mod = types.ModuleType("docling")
    fake_dc_mod = types.ModuleType("docling.document_converter")
    fake_dc_mod.DocumentConverter = fake_converter_cls  # type: ignore[attr-defined]

    with patch.dict("sys.modules", {"docling": fake_docling_mod, "docling.document_converter": fake_dc_mod}):
        extract_pdf(pdf, txt, extractor="docling")

    assert txt.exists()
    content = txt.read_text(encoding="utf-8")
    assert "$$E = mc^2$$" in content


def test_run_extract_degradation_warning_logged(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    import logging as _logging

    kb = _make_kb(tmp_path)

    with (
        patch.dict("sys.modules", {"docling": None}),
        patch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext),
        caplog.at_level(_logging.WARNING),
    ):
        run_extract(kb, engine=None)

    assert any("degraded" in r.message.lower() for r in caplog.records)


def test_extract_cli_warns_on_degraded_engine(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    import contextlib
    from unittest.mock import patch as upatch

    from wikitools.cli import main

    kb = _make_kb(tmp_path)

    with (
        patch.dict("sys.modules", {"docling": None}),
        upatch("wikitools.commands.extract.extract_pdf", side_effect=_fake_pdftotext),
        upatch("sys.argv", ["wiki", "--kb", str(kb), "extract"]),
        contextlib.suppress(SystemExit),
    ):
        main()

    err = capsys.readouterr().err
    assert "degraded" in err.lower()


@pytest.mark.integration
def test_extract_real_kb_pdftotext() -> None:
    """Extract first PDF from real kb and verify idempotency."""
    import subprocess

    result = subprocess.run(
        ["uv", "run", "wiki", "extract", "--citekey", "aghabozorgiTimeseriesClusteringDecade2015"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    # Rerun: should report 0 extracted
    result2 = subprocess.run(
        ["uv", "run", "wiki", "extract", "--citekey", "aghabozorgiTimeseriesClusteringDecade2015"],
        capture_output=True,
        text=True,
    )
    assert result2.returncode == 0
    assert "0 extracted" in result2.stdout
