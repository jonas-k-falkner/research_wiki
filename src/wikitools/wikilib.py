"""Shared primitives for wiki page enumeration, linking, and library loading."""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import re
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

# ── Frontmatter constants ─────────────────────────────────────────────────────

REQUIRED_FM_KEYS: frozenset[str] = frozenset({"type", "status", "stage", "confidence", "updated", "sources"})

VALID_TYPES: frozenset[str] = frozenset(
    {
        "project",
        "domain",
        "source",
        "concept",
        "comparison",
        "decision",
        "experiment",
        "shared",
        "query",
        "entity",
    }
)
VALID_DOMAINS: frozenset[str] = frozenset(
    {
        "timeseries-forecasting",
        "embedding-models",
        "scenario-engine",
        "nowcasting-graph",
        "shared",
    }
)
VALID_PROJECTS: frozenset[str] = frozenset({"P1", "P2", "P3", "P4", "shared"})
VALID_STATUSES: frozenset[str] = frozenset({"draft", "active", "needs-review", "superseded", "archived"})
VALID_STAGES: frozenset[str] = frozenset({"seed", "researched", "validated"})
VALID_CONFIDENCES: frozenset[str] = frozenset({"low", "medium", "high"})

FM_KEY_ORDER: list[str] = ["type", "domain", "project", "status", "stage", "confidence", "updated", "sources", "tags"]

# Portable Markdown link regex — matches ](path.md) and ](path.md#anchor)
LINK_RE: re.Pattern[str] = re.compile(r"\]\(([^)\n]+?\.md(?:#[^)\n]*)?)\)")
# Full link including text: [text](path.md)
FULL_LINK_RE: re.Pattern[str] = re.compile(r"\[([^\]\n]*)\]\(([^)\n]+?\.md(?:#[^)\n]*)?)\)")
# [verify] marker
VERIFY_RE: re.Pattern[str] = re.compile(r"\[verify\]", re.IGNORECASE)
# Raw path backtick references in body: `raw/...`
RAW_PATH_RE: re.Pattern[str] = re.compile(r"`(raw/[^`]+)`")


# ── Data models ───────────────────────────────────────────────────────────────


@dataclass
class Page:
    """A parsed wiki markdown page with frontmatter and body."""

    path: Path
    type: str
    domain: str
    project: str
    status: str
    stage: str
    confidence: str
    updated: date | None
    sources: list[str]
    tags: list[str]
    title: str
    body: str
    raw_fm: dict[str, object]
    fm_parse_error: str | None = None


@dataclass
class Link:
    """A portable Markdown link extracted from a page body."""

    source_page: Path
    target_raw: str
    anchor: str | None
    resolved: Path


@dataclass
class Item:
    """A literature item from a Better CSL JSON library export."""

    id: str
    title: str
    doi: str | None
    authors: list[str]
    year: int | None
    abstract: str | None


# ── Internal helpers ──────────────────────────────────────────────────────────


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str, str | None]:
    """Split YAML frontmatter from body and return (fm, body, error).

    Args:
        text: Full file text starting from the first character.

    Returns:
        Tuple of (frontmatter_dict, body_text, parse_error_or_None).
    """
    if not text.startswith("---"):
        return {}, text, None
    close = text.find("\n---", 3)
    if close == -1:
        return {}, text, "No closing --- delimiter found"
    fm_str = text[3:close].strip()
    body = text[close + 4 :].lstrip("\n")
    try:
        fm = yaml.safe_load(fm_str)
    except yaml.YAMLError as exc:
        return {}, body, str(exc)
    if not isinstance(fm, dict):
        return {}, body, f"Frontmatter is not a YAML mapping (got {type(fm).__name__})"
    result: dict[str, object] = fm
    return result, body, None


def _parse_date(val: object) -> date | None:
    """Parse a date value from frontmatter, returning None on failure."""
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val)
        except ValueError:
            return None
    return None


def _to_str_list(val: object) -> list[str]:
    """Coerce a frontmatter value to a flat list of strings."""
    if val is None:
        return []
    if isinstance(val, list):
        return [str(v) for v in val]
    if isinstance(val, str):
        return [val]
    return []


def _first_h1(body: str, fallback: str) -> str:
    """Extract the first H1 heading from body text, falling back to a default."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


# ── Public API ────────────────────────────────────────────────────────────────


def iter_pages(root: Path) -> Iterator[Page]:
    """Enumerate all wiki pages under root/wiki/ in deterministic order.

    Args:
        root: Path to the kb root directory (must contain a wiki/ subdirectory).

    Yields:
        Page objects parsed from YAML frontmatter and body.
    """
    wiki_root = root.resolve() / "wiki"
    for path in sorted(wiki_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm, body, err = _parse_frontmatter(text)
        yield Page(
            path=path,
            type=str(fm.get("type", "")),
            domain=str(fm.get("domain", "")),
            project=str(fm.get("project", "")),
            status=str(fm.get("status", "")),
            stage=str(fm.get("stage", "")),
            confidence=str(fm.get("confidence", "")),
            updated=_parse_date(fm.get("updated")),
            sources=_to_str_list(fm.get("sources")),
            tags=_to_str_list(fm.get("tags")),
            title=_first_h1(body, path.stem),
            body=body,
            raw_fm=fm,
            fm_parse_error=err,
        )


def iter_links(page: Page) -> Iterator[Link]:
    """Yield all portable Markdown links to .md files found in a page body.

    Args:
        page: The wiki page to scan.

    Yields:
        Link objects with resolved absolute paths (resolved path may not exist).
    """
    for match in LINK_RE.finditer(page.body):
        raw = match.group(1)
        anchor: str | None
        if "#" in raw:
            target, anchor = raw.split("#", 1)
        else:
            target, anchor = raw, None
        resolved = (page.path.parent / target).resolve()
        yield Link(source_page=page.path, target_raw=raw, anchor=anchor, resolved=resolved)


def load_library(library_path: Path) -> dict[str, Item]:
    """Load all items from a Better CSL JSON library export.

    Args:
        library_path: Path to library.json. Returns empty dict if file is absent.

    Returns:
        Dict mapping citekey → Item.
    """
    if not library_path.exists():
        return {}
    with library_path.open(encoding="utf-8") as fh:
        raw: list[dict[str, object]] = json.load(fh)
    result: dict[str, Item] = {}
    for entry in raw:
        citekey = str(entry.get("id", ""))
        if not citekey:
            continue
        authors: list[str] = []
        raw_authors = entry.get("author") or []
        for author in raw_authors if isinstance(raw_authors, list) else []:
            if isinstance(author, dict):
                parts = [str(author.get("family", "")), str(author.get("given", ""))]
                authors.append(" ".join(p for p in parts if p))
        year: int | None = None
        issued = entry.get("issued", {})
        if isinstance(issued, dict):
            dp = issued.get("date-parts", [[]])
            if isinstance(dp, list) and dp and isinstance(dp[0], list) and dp[0]:
                with contextlib.suppress(ValueError, TypeError):
                    year = int(dp[0][0])
        result[citekey] = Item(
            id=citekey,
            title=str(entry.get("title", "")),
            doi=str(entry["DOI"]) if "DOI" in entry else None,
            authors=authors,
            year=year,
            abstract=str(entry["abstract"]) if "abstract" in entry else None,
        )
    return result


def pdf_path(kb_root: Path, citekey: str) -> Path | None:
    """Return the PDF path for a citekey if it exists, else None.

    Args:
        kb_root: Path to the kb root.
        citekey: The citekey string (basename without extension).

    Returns:
        Absolute path to the PDF, or None if absent.
    """
    p = kb_root / "raw" / "literature" / "pdf" / f"{citekey}.pdf"
    return p if p.exists() else None


def txt_path(kb_root: Path, citekey: str) -> Path | None:
    """Return the extracted text path for a citekey if it exists, else None.

    Args:
        kb_root: Path to the kb root.
        citekey: The citekey string (basename without extension).

    Returns:
        Absolute path to the .txt file, or None if absent.
    """
    p = kb_root / "raw" / "literature" / "txt" / f"{citekey}.txt"
    return p if p.exists() else None


def content_hash(path: Path) -> str:
    """Return a stable SHA-256 hex digest of the normalized file content.

    Args:
        path: Path to the file.

    Returns:
        Lowercase hex SHA-256 string.
    """
    text = path.read_text(encoding="utf-8")
    normalized = "\n".join(line.rstrip() for line in text.splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def inbound_links(pages: list[Page]) -> dict[Path, set[Path]]:
    """Build a map from page path to the set of pages that link to it.

    Args:
        pages: All wiki pages.

    Returns:
        Dict mapping each page path to the set of source paths that link to it.
    """
    result: dict[Path, set[Path]] = {p.path: set() for p in pages}
    for page in pages:
        for link in iter_links(page):
            if link.resolved in result:
                result[link.resolved].add(page.path)
    return result
