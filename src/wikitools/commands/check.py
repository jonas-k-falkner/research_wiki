"""Idempotent ingest check and claim deduplication (`wiki check source / claim`)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

logger = logging.getLogger(__name__)

# Similarity thresholds for claim classification
_DUPLICATE_THRESHOLD = 0.85
_SUPPORT_THRESHOLD = 0.50


# ── enums / data types ────────────────────────────────────────────────────────


class SourceState(StrEnum):
    """Result of comparing an ingest source against an existing wiki source page.

    Attributes:
        NEW: No wiki source page found for this citekey.
        UNCHANGED: Page exists and its recorded source_hash matches the raw file.
        CHANGED: Page exists but the source_hash differs (file was updated).
    """

    NEW = "new"
    UNCHANGED = "unchanged"
    CHANGED = "changed"


@dataclass(frozen=True)
class SourceStatus:
    """Full result of `check_source`.

    Attributes:
        state: Whether the source is new, unchanged, or changed.
        page_path: Path to the existing wiki source page, or ``None`` when state is ``NEW``.
        recorded_hash: The ``source_hash:`` stored in the page frontmatter, or ``None``.
        current_hash: SHA-256 of the raw file at query time, or ``None`` if no file exists.
    """

    state: SourceState
    page_path: Path | None
    recorded_hash: str | None
    current_hash: str | None


class ClaimClassification(StrEnum):
    """How a claim hit relates to the candidate claim.

    Attributes:
        DUPLICATE: Same source already records this claim.
        ADDITIONAL_SUPPORT: Different source, high similarity — provides extra evidence.
        NEW: Low similarity — this claim is likely not already recorded.
    """

    DUPLICATE = "duplicate"
    ADDITIONAL_SUPPORT = "additional-support"
    NEW = "new"


@dataclass(frozen=True)
class ClaimHit:
    """One result from `check_claim`.

    Attributes:
        source_path: Relative path (from kb_root) of the page containing the hit.
        section: Section heading within the page.
        snippet: Short text excerpt.
        score: Similarity score (higher = more similar).
        cites_queried_source: True when the hit page cites the queried citekey.
        classification: Duplicate, additional-support, or new.
    """

    source_path: str
    section: str
    snippet: str
    score: float
    cites_queried_source: bool
    classification: ClaimClassification


# ── source check ──────────────────────────────────────────────────────────────


def _find_source_page(citekey: str, kb_root: Path) -> tuple[Path | None, str | None]:
    """Scan wiki/sources/ for a page whose frontmatter has ``zotero: <citekey>``.

    Args:
        citekey: Zotero citekey to look for.
        kb_root: Knowledge-base root directory.

    Returns:
        Tuple of ``(page_path, recorded_source_hash)``.  Both are ``None`` if no page found.
    """
    import yaml

    sources_dir = kb_root / "wiki" / "sources"
    if not sources_dir.is_dir():
        return None, None

    for md in sources_dir.glob("*.md"):
        text = md.read_text(encoding="utf-8")
        # Fast pre-filter before full YAML parse
        if citekey not in text:
            continue
        try:
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        if str(fm.get("zotero", "")).strip() == citekey:
            return md, str(fm.get("source_hash", "")).strip() or None

    return None, None


def check_source(citekey: str, kb_root: Path) -> SourceStatus:
    """Determine whether a literature source has already been ingested.

    Looks for a wiki source page with ``zotero: <citekey>`` in its frontmatter.
    Computes the current SHA-256 of the raw file (PDF preferred, then .txt) and
    compares it against the ``source_hash:`` stored in the existing page.

    Args:
        citekey: Zotero citekey of the source to check.
        kb_root: Knowledge-base root directory.

    Returns:
        A ``SourceStatus`` indicating new/unchanged/changed, the page path, and hashes.
    """
    from wikitools.commands.extract import _file_hash as _binary_hash
    from wikitools.wikilib import content_hash, pdf_path, txt_path

    page_path, recorded_hash = _find_source_page(citekey, kb_root)

    # PDF → binary SHA-256 (text decode fails on binary); .txt → normalized text SHA-256
    pdf = pdf_path(kb_root, citekey)
    txt = txt_path(kb_root, citekey)
    raw: Path | None = pdf or txt
    current_hash: str | None = None
    if raw is not None:
        try:
            current_hash = _binary_hash(raw) if raw.suffix == ".pdf" else content_hash(raw)
        except OSError:
            logger.warning("check_source: cannot hash %s", raw)

    if page_path is None:
        return SourceStatus(state=SourceState.NEW, page_path=None, recorded_hash=None, current_hash=current_hash)

    if recorded_hash and current_hash and recorded_hash == current_hash:
        return SourceStatus(state=SourceState.UNCHANGED, page_path=page_path, recorded_hash=recorded_hash, current_hash=current_hash)

    return SourceStatus(state=SourceState.CHANGED, page_path=page_path, recorded_hash=recorded_hash, current_hash=current_hash)


# ── claim check ───────────────────────────────────────────────────────────────


def _load_page_citekeys(source_path: str, kb_root: Path) -> set[str]:
    """Extract all ``zotero:`` frontmatter values from a wiki page.

    Also returns any citekeys found in ``sources[]`` entries that look like a
    citekey (no whitespace, alphanumeric-dash).

    Args:
        source_path: Relative path string (from kb_root) to the page.
        zotero: Zotero citekey for checking whether the hit page cites a queried source.
        kb_root: Knowledge-base root directory.

    Returns:
        Set of citekey strings referenced in the page.
    """
    import re

    import yaml

    full_path = kb_root / source_path
    if not full_path.exists() or full_path.suffix != ".md":
        return set()
    try:
        text = full_path.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) < 3:
            return set()
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return set()

    keys: set[str] = set()
    z = str(fm.get("zotero", "")).strip()
    if z:
        keys.add(z)
    for src in fm.get("sources", []) or []:
        s = str(src).strip()
        if re.match(r"^[A-Za-z0-9_-]+$", s):
            keys.add(s)
    return keys


def _classify(score: float, cites_queried: bool) -> ClaimClassification:
    """Classify a claim hit.

    Args:
        score: Similarity score.
        cites_queried: Whether the hit page already cites the queried source.

    Returns:
        Classification: duplicate, additional-support, or new.
    """
    if score >= _DUPLICATE_THRESHOLD:
        return ClaimClassification.DUPLICATE
    if score >= _SUPPORT_THRESHOLD:
        return ClaimClassification.ADDITIONAL_SUPPORT
    return ClaimClassification.NEW


def check_claim(
    claim_text: str,
    kb_root: Path,
    *,
    citekey: str | None = None,
    page: str | None = None,
    k: int = 10,
    mode: str = "hybrid",
) -> list[ClaimHit]:
    """Search the corpus for existing claims similar to `claim_text`.

    Uses the T004 search index (lexical FTS primary; cosine secondary when
    ``[semantic]`` extra is installed).  Classifies each hit as duplicate,
    additional-support, or new relative to the provided source.

    Args:
        claim_text: The candidate claim to check.
        kb_root: Knowledge-base root directory.
        citekey: Optional citekey of the source being ingested; used to mark hits
                 that already cite this source.
        page: Optional relative path to the page being edited; excluded from results
              so a page does not flag its own content as a duplicate.
        k: Maximum number of hits to return.
        mode: Search mode — ``"lexical"``, ``"semantic"``, or ``"hybrid"`` (default).

    Returns:
        List of ``ClaimHit`` objects, sorted by descending score, filtered to
        non-NEW classifications.  Empty list when no similar claims are found.

    Raises:
        FileNotFoundError: If the search index does not exist.
    """
    from wikitools.commands.search import search

    try:
        hits = search(claim_text, kb_root, k=k, mode=mode, scope="wiki")
    except FileNotFoundError:
        raise
    except Exception as exc:
        logger.warning("check_claim: search failed (%s)", exc)
        return []

    results: list[ClaimHit] = []
    for h in hits:
        if page and h.source_path == page:
            continue
        cites_queried = False
        if citekey:
            page_citekeys = _load_page_citekeys(h.source_path, kb_root)
            cites_queried = citekey in page_citekeys

        classification = _classify(h.score, cites_queried)
        if classification == ClaimClassification.NEW:
            continue

        results.append(
            ClaimHit(
                source_path=h.source_path,
                section=h.section,
                snippet=h.snippet,
                score=h.score,
                cites_queried_source=cites_queried,
                classification=classification,
            )
        )

    return results
