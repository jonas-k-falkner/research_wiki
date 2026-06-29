"""PDF text extraction: reconciliation, extraction pipeline, and sidecar tracking."""

from __future__ import annotations

import hashlib
import json as json_mod
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from docling.document_converter import DocumentConverter

from wikitools.wikilib import load_library

logger = logging.getLogger(__name__)


def _file_hash(path: Path) -> str:
    """Return SHA-256 hex digest of raw file bytes.

    Args:
        path: File to hash.

    Returns:
        Lowercase 64-character hex string.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _get_engine_version(engine: str) -> str:
    """Return a human-readable version string for the given engine.

    Args:
        engine: Engine name — ``fast``, ``docling``, or ``marker``.

    Returns:
        Version string; falls back to a safe placeholder on failure.
    """
    if engine == "fast":
        try:
            result = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
            line = (result.stderr or result.stdout).strip().split("\n")[0]
            return line if line else "pdftotext (version unknown)"
        except FileNotFoundError:
            return "pdftotext (not found)"
    elif engine == "docling":
        try:
            import docling

            return f"docling {getattr(docling, '__version__', 'version unknown')}"
        except ImportError:
            return "docling (not installed)"
    elif engine == "marker":
        try:
            import marker

            return f"marker {getattr(marker, '__version__', 'version unknown')}"
        except ImportError:
            return "marker (not installed)"
    return engine


def _resolve_engine(engine: str | None) -> tuple[str, bool]:
    """Resolve the engine to use, with automatic fallback.

    When no engine is requested, prefer ``docling`` (math-aware) if the [ocr]
    extra is installed; otherwise fall back to ``fast`` (pdftotext).

    Args:
        engine: Explicit engine name, or ``None`` to auto-resolve.

    Returns:
        Tuple of (engine_name, is_degraded_fallback).  ``is_degraded_fallback``
        is True only when the caller requested auto-resolution and docling was
        unavailable, signalling that math in equations will be degraded.
    """
    if engine is not None:
        return engine, False
    try:
        import docling  # noqa: F401

        return "docling", False
    except ImportError:
        return "fast", True


class MissingExtraError(RuntimeError):
    """Raised when an optional engine is requested without its extra installed."""


@dataclass(frozen=True, order=True)
class ReconciliationIssue:
    """A single reconciliation diagnostic between pdf/, library.json, and txt/."""

    kind: str
    path: str
    message: str


def run_reconciliation(kb_root: Path) -> list[ReconciliationIssue]:
    """Check consistency between raw/literature/pdf/, library.json, and txt/.

    Checks:
    - Every pdf/<citekey>.pdf basename maps to a citekey in library.json.
    - Every pdf/ file has a corresponding extracted txt/ file.

    Library-only items without a PDF are intentionally metadata-only and are not flagged.

    Args:
        kb_root: Path to kb root (will be resolved).

    Returns:
        Sorted list of ReconciliationIssue objects; empty list if all is consistent.
    """
    kb_root = kb_root.resolve()
    lit_root = kb_root / "raw" / "literature"
    pdf_dir = lit_root / "pdf"
    txt_dir = lit_root / "txt"
    library = load_library(lit_root / "library.json")

    issues: list[ReconciliationIssue] = []

    if not pdf_dir.exists():
        return issues

    for pdf_file in sorted(pdf_dir.iterdir()):
        if pdf_file.suffix != ".pdf":
            continue
        citekey = pdf_file.stem.removesuffix("-suppl")
        ref = f"raw/literature/pdf/{pdf_file.name}"

        if library and citekey not in library:
            issues.append(
                ReconciliationIssue(
                    kind="pdf-missing-from-library",
                    path=ref,
                    message=f"PDF {pdf_file.name!r} has no entry in library.json (expected citekey: {citekey!r})",
                )
            )

        txt_file = txt_dir / f"{pdf_file.stem}.txt"
        if not txt_file.exists():
            issues.append(
                ReconciliationIssue(
                    kind="txt-missing",
                    path=ref,
                    message=f"No extracted txt for {pdf_file.name!r}",
                )
            )

    return sorted(issues)


def extract_pdf(
    pdf_path: Path,
    txt_path: Path,
    extractor: str = "fast",
    _converter: DocumentConverter | None = None,
) -> None:
    """Extract text from a single PDF to a txt file.

    Args:
        pdf_path: Source PDF file.
        txt_path: Destination txt file (parent created if absent).
        extractor: Extraction engine — ``fast`` (pdftotext, default),
            ``docling`` (math-aware Markdown output), or ``marker``.
        _converter: Pre-initialised ``DocumentConverter`` instance; when provided,
            avoids reloading model weights on every call.

    Raises:
        MissingExtraError: If ``docling`` or ``marker`` are requested but the
            [ocr] extra is not installed.
        RuntimeError: If pdftotext exits non-zero.
        ValueError: If extractor is unknown.
    """
    if extractor == "fast":
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["pdftotext", str(pdf_path), str(txt_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"pdftotext failed for {pdf_path.name!r}: {result.stderr.strip()}")

    elif extractor == "docling":
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:
            raise MissingExtraError("Engine 'docling' requires the [ocr] extra. Install with: uv sync --extra ocr") from exc
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        converter = _converter if _converter is not None else DocumentConverter()
        result_doc = converter.convert(str(pdf_path))
        txt_path.write_text(result_doc.document.export_to_markdown(), encoding="utf-8")

    elif extractor == "marker":
        try:
            import marker  # noqa: F401
        except ImportError as exc:
            raise MissingExtraError("Engine 'marker' requires the [ocr] extra. Install with: uv sync --extra ocr") from exc
        raise NotImplementedError("'marker' engine integration not yet implemented")

    else:
        raise ValueError(f"Unknown extractor: {extractor!r}")


def run_extract(
    kb_root: Path,
    engine: str | None = None,
    force: bool = False,
    citekey: str | None = None,
    formula_enrichment: bool = True,
) -> tuple[int, int, list[ReconciliationIssue]]:
    """Extract text from PDFs in raw/literature/pdf/ with idempotency and reconciliation.

    Engine resolution: when ``engine`` is ``None``, uses ``docling`` if the [ocr]
    extra is installed; otherwise falls back to ``fast`` (pdftotext) and logs a
    degradation warning.

    Runs reconciliation first (reports issues, does not abort). Then iterates PDFs,
    skipping files whose sidecar hash matches the current PDF content unless ``force``.
    Writes ``txt/<stem>.txt`` and sidecar ``txt/<stem>.extract.json`` per extracted file.
    Failed extractions are logged and skipped (non-fatal).

    Args:
        kb_root: Path to kb root (will be resolved).
        engine: Extraction engine (``fast``, ``docling``, ``marker``), or ``None``
            to auto-resolve.
        force: If True, re-extract even when the source hash matches.
        citekey: If set, process only PDFs whose citekey equals this value.
        formula_enrichment: When True and engine is ``docling``, enables the
            formula VLM (CodeFormulaV2) to emit proper LaTeX fences instead of
            raw glyph text.  Slower but required for math-bearing papers.

    Returns:
        Tuple of (extracted_count, skipped_count, reconciliation_issues).
    """
    kb_root = kb_root.resolve()
    lit_root = kb_root / "raw" / "literature"
    pdf_dir = lit_root / "pdf"
    txt_dir = lit_root / "txt"

    actual_engine, degraded = _resolve_engine(engine)
    if degraded:
        logger.warning("docling not installed; using fast path — math in equations will be degraded. Install the [ocr] extra: uv sync --extra ocr")

    issues = run_reconciliation(kb_root)
    for issue in issues:
        logger.warning("reconciliation [%s] %s: %s", issue.kind, issue.path, issue.message)

    if not pdf_dir.exists():
        logger.info("No pdf/ directory at %s — nothing to extract", pdf_dir)
        return 0, 0, issues

    txt_dir.mkdir(parents=True, exist_ok=True)

    extracted = 0
    skipped = 0
    engine_version = _get_engine_version(actual_engine)

    converter: DocumentConverter | None = None
    if actual_engine == "docling":
        try:
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import PdfPipelineOptions
            from docling.document_converter import DocumentConverter, PdfFormatOption

            pipeline_opts = PdfPipelineOptions(
                do_formula_enrichment=formula_enrichment,
                generate_page_images=formula_enrichment,
            )
            converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_opts)})
            if formula_enrichment:
                logger.info("Docling converter initialised with formula enrichment (CodeFormulaV2)")
            else:
                logger.info("Docling converter initialised without formula enrichment")
        except ImportError as exc:
            raise MissingExtraError("Engine 'docling' requires the [ocr] extra. Install with: uv sync --extra ocr") from exc

    for pdf_file in sorted(pdf_dir.iterdir()):
        if pdf_file.suffix != ".pdf":
            continue
        stem = pdf_file.stem
        this_citekey = stem.removesuffix("-suppl")
        if citekey is not None and this_citekey != citekey:
            continue

        txt_file = txt_dir / f"{stem}.txt"
        sidecar = txt_dir / f"{stem}.extract.json"
        current_hash = _file_hash(pdf_file)

        if not force and sidecar.exists() and txt_file.exists():
            try:
                stored = json_mod.loads(sidecar.read_text(encoding="utf-8"))
                if stored.get("source_hash") == current_hash:
                    logger.debug("Skipping %s (hash unchanged)", pdf_file.name)
                    skipped += 1
                    continue
            except (json_mod.JSONDecodeError, KeyError):
                pass

        try:
            extract_pdf(pdf_file, txt_file, extractor=actual_engine, _converter=converter)
            sidecar.write_text(
                json_mod.dumps(
                    {
                        "extractor": actual_engine,
                        "engine_version": engine_version,
                        "source_hash": current_hash,
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            logger.info("Extracted: %s", pdf_file.name)
            extracted += 1
        except Exception as exc:
            logger.warning("Extraction failed for %s: %s", pdf_file.name, exc)

    return extracted, skipped, issues
