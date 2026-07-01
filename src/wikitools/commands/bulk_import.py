"""Bulk literature import: merge a new Zotero export folder into raw/literature/."""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from wikitools.wikilib import load_library_raw, write_library

if TYPE_CHECKING:
    from wikitools.commands.index import Embedder

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ImportReport:
    """Result of a `wiki import` run.

    Attributes:
        added: Citekeys newly added to the canonical library.
        skipped: Citekeys that already existed and were left untouched.
        replaced: Citekeys that already existed and were overwritten (``--force``).
        extracted: Number of PDFs extracted (0 if extraction was skipped or nothing changed).
        indexed_files: Number of source files reprocessed by the index (0 if the index
            update was skipped or nothing changed).
    """

    added: list[str]
    skipped: list[str]
    replaced: list[str]
    extracted: int
    indexed_files: int


def _find_library_file(source_dir: Path, library: Path | None) -> Path:
    """Locate the single CSL JSON library file in a Zotero export folder.

    Args:
        source_dir: Folder containing the new Zotero export.
        library: Explicit override path; bypasses auto-detection when given.

    Returns:
        Path to the library JSON file.

    Raises:
        ValueError: If ``library`` is unset and ``source_dir`` contains zero or more
            than one top-level ``*.json`` file.
    """
    if library is not None:
        return library
    candidates = sorted(source_dir.glob("*.json"))
    if len(candidates) != 1:
        names = [c.name for c in candidates]
        raise ValueError(f"Expected exactly one *.json file in {source_dir}, found {len(candidates)}: {names}. Use --library to disambiguate.")
    return candidates[0]


def _citekey_for_pdf(pdf_path: Path) -> str:
    """Return the citekey for a PDF path, stripping the ``-suppl`` suffix."""
    return pdf_path.stem.removesuffix("-suppl")


def _copy_if_changed(src: Path, dest: Path) -> None:
    """Copy ``src`` to ``dest``, skipping the write if content is already identical."""
    from wikitools.commands.extract import _file_hash

    if dest.exists() and _file_hash(dest) == _file_hash(src):
        return
    shutil.copy2(src, dest)


def run_import(
    kb_root: Path,
    source_dir: Path,
    *,
    library: Path | None = None,
    force: bool = False,
    do_extract: bool = True,
    do_index: bool = True,
    dry_run: bool = False,
    engine: str | None = None,
    embedder: Embedder | None = None,
) -> ImportReport:
    """Merge a new Zotero export folder into raw/literature/, then extract + index.

    For each citekey in the incoming library file: a citekey absent from the
    canonical library is **added** (entry + PDF(s) copied in); a citekey already
    present is **skipped** unless ``force=True``, in which case it is **replaced**
    (entry + PDF(s) overwritten). ``source_dir`` is read-only input — never modified
    or deleted.

    Args:
        kb_root: Knowledge-base root directory.
        source_dir: Folder containing the new Zotero export (one CSL JSON file plus
            ``<citekey>.pdf`` / ``<citekey>-suppl.pdf`` attachments).
        library: Explicit path to the CSL JSON file, overriding auto-detection.
        force: If True, overwrite existing entries/PDFs on citekey collision.
        do_extract: If True, run text extraction for added/replaced citekeys.
        do_index: If True, run an incremental index update after extraction.
        dry_run: If True, compute the report without writing anything.
        engine: Extraction engine forwarded to ``run_extract`` (``None`` auto-resolves).
        embedder: Embedding provider forwarded to ``update_index``; ``None`` stores
            embeddings as ``NULL`` (lexical-only).

    Returns:
        An ``ImportReport`` describing what changed, or what would change if ``dry_run``.

    Raises:
        ValueError: If the library file cannot be unambiguously located.
    """
    kb_root = kb_root.resolve()
    source_dir = source_dir.resolve()
    lit_root = kb_root / "raw" / "literature"
    canonical_path = lit_root / "library.json"
    pdf_dir = lit_root / "pdf"

    library_file = _find_library_file(source_dir, library)
    incoming = load_library_raw(library_file)
    canonical = load_library_raw(canonical_path)

    incoming_pdfs: dict[str, list[Path]] = {}
    for pdf in sorted(source_dir.glob("*.pdf")):
        incoming_pdfs.setdefault(_citekey_for_pdf(pdf), []).append(pdf)
    for orphan in sorted(set(incoming_pdfs) - set(incoming)):
        logger.warning("wiki import: PDF citekey %r in %s has no entry in the incoming library file", orphan, source_dir)

    added: list[str] = []
    skipped: list[str] = []
    replaced: list[str] = []
    for citekey in sorted(incoming):
        if citekey not in canonical:
            added.append(citekey)
        elif force:
            replaced.append(citekey)
        else:
            skipped.append(citekey)

    if dry_run:
        return ImportReport(added=added, skipped=skipped, replaced=replaced, extracted=0, indexed_files=0)

    changed_keys = added + replaced
    if changed_keys:
        pdf_dir.mkdir(parents=True, exist_ok=True)
        for citekey in changed_keys:
            canonical[citekey] = incoming[citekey]
            for pdf in incoming_pdfs.get(citekey, []):
                _copy_if_changed(pdf, pdf_dir / pdf.name)
        write_library(canonical_path, canonical)
        logger.info("wiki import: %d added, %d replaced, %d skipped", len(added), len(replaced), len(skipped))
    else:
        logger.info("wiki import: nothing to add or replace (%d skipped)", len(skipped))

    extracted = 0
    if do_extract and changed_keys:
        from wikitools.commands.extract import run_extract

        extracted, _skipped, _issues = run_extract(kb_root, engine=engine, citekeys=changed_keys)

    indexed_files = 0
    if do_index and changed_keys:
        from wikitools.commands.index import update_index

        indexed_files = update_index(kb_root, embedder=embedder)

    return ImportReport(added=added, skipped=skipped, replaced=replaced, extracted=extracted, indexed_files=indexed_files)
