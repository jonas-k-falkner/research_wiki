"""Wiki health-check linter: all checks, --fix, and output formatters."""

from __future__ import annotations

import json as json_mod
import logging
import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import yaml

from wikitools.wikilib import (
    FM_KEY_ORDER,
    FULL_LINK_RE,
    RAW_PATH_RE,
    REQUIRED_FM_KEYS,
    VALID_CONFIDENCES,
    VALID_DOMAINS,
    VALID_PROJECTS,
    VALID_STAGES,
    VALID_STATUSES,
    VALID_TYPES,
    VERIFY_RE,
    Item,
    Page,
    inbound_links,
    iter_links,
    iter_pages,
    load_library,
)

logger = logging.getLogger(__name__)

# ── Finding ───────────────────────────────────────────────────────────────────

_NAV_ROOT_NAMES: frozenset[str] = frozenset({"index.md", "log.md", "overview.md"})
_THIN_BODY_CHARS = 150
_BOILERPLATE_RE = re.compile(r"\b(placeholder|todo:?\s|tbd\b|fill\s+in\s+later)", re.IGNORECASE)
_DUP_TITLE_THRESHOLD = 0.70
_CLAIM_TYPES: frozenset[str] = frozenset({"project", "domain", "concept", "comparison", "decision", "experiment", "entity"})


@dataclass(frozen=True, order=True)
class Finding:
    """A single lint diagnostic."""

    severity: str
    check: str
    path: str
    message: str


# ── Check helpers ─────────────────────────────────────────────────────────────


def _rel(path: Path, kb_root: Path) -> str:
    """Return path relative to kb_root as a POSIX string."""
    return path.relative_to(kb_root).as_posix()


def _is_nav_root(page: Page) -> bool:
    return page.path.name in _NAV_ROOT_NAMES


# ── Individual checks ─────────────────────────────────────────────────────────


def _check_broken_links(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Detect broken portable Markdown links; severity=error."""
    out: list[Finding] = []
    for page in pages:
        for link in iter_links(page):
            if not link.resolved.exists():
                out.append(Finding("error", "broken-links", _rel(page.path, kb_root), f"Broken link: ]({link.target_raw})"))
    return sorted(out)


def _check_frontmatter_schema(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Validate YAML frontmatter: required keys, enum values, and date format; severity=error."""
    out: list[Finding] = []
    for page in pages:
        p = _rel(page.path, kb_root)
        if page.fm_parse_error:
            out.append(Finding("error", "frontmatter-schema", p, f"YAML parse error: {page.fm_parse_error}"))
            continue
        fm = page.raw_fm
        for key in sorted(REQUIRED_FM_KEYS - fm.keys()):
            out.append(Finding("error", "frontmatter-schema", p, f"Missing required key: {key}"))
        for field_name, valid_set in (
            ("type", VALID_TYPES),
            ("domain", VALID_DOMAINS),
            ("project", VALID_PROJECTS),
            ("status", VALID_STATUSES),
            ("stage", VALID_STAGES),
            ("confidence", VALID_CONFIDENCES),
        ):
            val = fm.get(field_name)
            if val is not None and str(val) not in valid_set:
                out.append(Finding("error", "frontmatter-schema", p, f"Invalid {field_name}: {val!r}"))
        # updated must be a date
        if "updated" in fm and page.updated is None:
            out.append(Finding("error", "frontmatter-schema", p, f"Invalid updated date: {fm['updated']!r}"))
        # sources must be a list
        sources_val = fm.get("sources")
        if sources_val is not None and not isinstance(sources_val, list):
            out.append(Finding("error", "frontmatter-schema", p, f"sources must be a list, got {type(sources_val).__name__}"))
    return sorted(out)


def _check_dangling_sources(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Detect source IDs in sources[] that have no matching sources/ page; severity=error."""
    sources_dir = kb_root / "wiki" / "sources"
    out: list[Finding] = []
    for page in pages:
        p = _rel(page.path, kb_root)
        for src_id in page.sources:
            if not (sources_dir / f"{src_id}.md").exists():
                out.append(Finding("error", "dangling-sources", p, f"No source page for: {src_id}"))
    return sorted(out)


def _check_verify_on_researched(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Detect [verify] markers on pages with stage:researched; severity=error."""
    out: list[Finding] = []
    for page in pages:
        if page.stage == "researched" and VERIFY_RE.search(page.body):
            out.append(Finding("error", "verify-on-researched", _rel(page.path, kb_root), "stage:researched page contains [verify] markers"))
    return sorted(out)


def _check_orphans(pages: list[Page], inbound: dict[Path, set[Path]], kb_root: Path) -> list[Finding]:
    """Detect pages with no inbound links, excluding nav roots; severity=warn."""
    out: list[Finding] = []
    for page in pages:
        if _is_nav_root(page):
            continue
        if not inbound.get(page.path):
            out.append(Finding("warn", "orphans", _rel(page.path, kb_root), "Page has no inbound links"))
    return sorted(out)


def _check_stage_confidence_sanity(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Warn on stage:seed + confidence:high combinations; severity=warn."""
    out: list[Finding] = []
    for page in pages:
        if page.stage == "seed" and page.confidence == "high":
            out.append(Finding("warn", "stage-confidence-sanity", _rel(page.path, kb_root), "stage:seed with confidence:high — review required"))
    return sorted(out)


def _check_provenance(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Warn on claim-bearing pages without sources and source pages without a raw path; severity=warn."""
    out: list[Finding] = []
    for page in pages:
        if _is_nav_root(page):
            continue
        p = _rel(page.path, kb_root)
        if page.type == "source":
            has_zotero = "zotero" in page.raw_fm
            raw_refs = RAW_PATH_RE.findall(page.body)
            has_raw_path = any((kb_root / ref).exists() for ref in raw_refs)
            if not has_zotero and not has_raw_path:
                out.append(Finding("warn", "provenance", p, "Source page has no zotero key and no resolvable raw path reference"))
        elif page.type in _CLAIM_TYPES and not page.sources:
            out.append(Finding("warn", "provenance", p, "Claim-bearing page has no sources[]"))
    return sorted(out)


def _check_thin_pages(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Warn on pages with very short bodies or boilerplate patterns; severity=warn."""
    out: list[Finding] = []
    for page in pages:
        if _is_nav_root(page):
            continue
        body = page.body.strip()
        if len(body) < _THIN_BODY_CHARS:
            out.append(Finding("warn", "thin-page", _rel(page.path, kb_root), f"Body too short ({len(body)} chars)"))
        elif _BOILERPLATE_RE.search(body):
            out.append(Finding("warn", "thin-page", _rel(page.path, kb_root), "Body matches boilerplate pattern"))
    return sorted(out)


def _check_citekey_integrity(pages: list[Page], library: dict[str, Item], kb_root: Path) -> list[Finding]:
    """Warn on mismatched zotero keys and PDF/txt inconsistencies; severity=warn."""
    out: list[Finding] = []
    # Only check zotero keys if library exists
    if library:
        for page in pages:
            if page.type == "source" and "zotero" in page.raw_fm:
                citekey = str(page.raw_fm["zotero"])
                if citekey not in library:
                    out.append(Finding("warn", "citekey-integrity", _rel(page.path, kb_root), f"zotero key {citekey!r} not found in library.json"))
    # Check PDFs have library entries and extracted text
    pdf_dir = kb_root / "raw" / "literature" / "pdf"
    if pdf_dir.exists():
        for pdf_file in sorted(pdf_dir.iterdir()):
            if pdf_file.suffix != ".pdf":
                continue
            citekey = pdf_file.stem.removesuffix("-suppl")
            ref = f"raw/literature/pdf/{pdf_file.name}"
            if library and citekey not in library:
                out.append(Finding("warn", "citekey-integrity", ref, f"PDF {pdf_file.name!r} has no entry in library.json"))
            txt_file = kb_root / "raw" / "literature" / "txt" / f"{pdf_file.stem}.txt"
            if not txt_file.exists():
                out.append(Finding("warn", "citekey-integrity", ref, f"No extracted txt for {pdf_file.name!r}"))
    return sorted(out)


def _check_reachability(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Warn on pages not reachable from index.md via link traversal; severity=warn."""
    index = kb_root / "wiki" / "index.md"
    if not index.exists():
        return []
    page_map: dict[Path, Page] = {p.path: p for p in pages}
    reachable: set[Path] = set()
    queue: deque[Path] = deque([index])
    while queue:
        cur = queue.popleft()
        if cur in reachable:
            continue
        reachable.add(cur)
        if cur in page_map:
            for link in iter_links(page_map[cur]):
                if link.resolved.exists() and link.resolved not in reachable:
                    queue.append(link.resolved)
    out: list[Finding] = []
    for page in pages:
        if _is_nav_root(page) or page.path in reachable:
            continue
        out.append(Finding("warn", "reachability", _rel(page.path, kb_root), "Page not reachable from index.md"))
    return sorted(out)


def _token_set(text: str) -> set[str]:
    return {w.lower() for w in re.split(r"\W+", text) if len(w) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    """Compute Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def _check_near_duplicate_titles(pages: list[Page], kb_root: Path) -> list[Finding]:
    """Warn on page pairs with near-identical titles by Jaccard similarity; severity=warn."""
    page_tokens = [(p, _token_set(p.title)) for p in pages]
    out: list[Finding] = []
    seen: set[tuple[Path, Path]] = set()
    for i, (page_a, tokens_a) in enumerate(page_tokens):
        for page_b, tokens_b in page_tokens[i + 1 :]:
            sim = _jaccard(tokens_a, tokens_b)
            if sim < _DUP_TITLE_THRESHOLD:
                continue
            key = (page_a.path, page_b.path)
            if key in seen:
                continue
            seen.add(key)
            rel_b = _rel(page_b.path, kb_root)
            out.append(Finding("warn", "near-duplicate-titles", _rel(page_a.path, kb_root), f"Near-duplicate title with {rel_b} (Jaccard={sim:.2f})"))
    return sorted(out)


# ── Auto-fix ──────────────────────────────────────────────────────────────────


def _strip_dead_links(text: str, page_path: Path) -> str:
    """Replace broken [text](dead.md) links with plain text."""

    def _replace(m: re.Match[str]) -> str:
        link_text = m.group(1)
        raw = m.group(2).split("#")[0]
        resolved = (page_path.parent / raw).resolve()
        return link_text if not resolved.exists() else m.group(0)

    return FULL_LINK_RE.sub(_replace, text)


def _normalize_fm_order(text: str) -> str:
    """Rewrite frontmatter with canonical key order, preserving values."""
    if not text.startswith("---"):
        return text
    close = text.find("\n---", 3)
    if close == -1:
        return text
    fm_str = text[3:close].strip()
    body_tail = text[close + 4 :]
    try:
        fm: dict[str, object] = yaml.safe_load(fm_str) or {}
    except yaml.YAMLError:
        return text
    if not isinstance(fm, dict):
        return text
    ordered: dict[str, object] = {}
    for key in FM_KEY_ORDER:
        if key in fm:
            ordered[key] = fm[key]
    for key, val in fm.items():
        if key not in ordered:
            ordered[key] = val
    new_fm = yaml.dump(ordered, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return f"---\n{new_fm}---{body_tail}"


def _apply_fixes(pages: list[Page]) -> None:
    """Apply safe auto-fixes to all pages in place."""
    for page in pages:
        original = page.path.read_text(encoding="utf-8")
        fixed = _strip_dead_links(original, page.path)
        fixed = _normalize_fm_order(fixed)
        if fixed != original:
            page.path.write_text(fixed, encoding="utf-8")
            logger.info("Fixed: %s", page.path)


# ── Main entry point ──────────────────────────────────────────────────────────


def run_lint(kb_root: Path, *, fix: bool = False, severity_filter: str = "warn") -> list[Finding]:
    """Run all wiki lint checks and return sorted findings.

    Args:
        kb_root: Path to the kb root directory.
        fix: If True, apply safe auto-fixes before reporting.
        severity_filter: "warn" reports everything; "error" reports errors only.

    Returns:
        Sorted list of Finding objects.

    Raises:
        ValueError: If kb_root/wiki/ does not exist.
    """
    kb_root = kb_root.resolve()
    wiki_root = kb_root / "wiki"
    if not wiki_root.exists():
        raise ValueError(f"No wiki/ directory under {kb_root}")

    pages = list(iter_pages(kb_root))

    if fix:
        _apply_fixes(pages)
        pages = list(iter_pages(kb_root))

    library = load_library(kb_root / "raw" / "literature" / "library.json")
    inbound = inbound_links(pages)

    all_findings: list[Finding] = []
    all_findings.extend(_check_broken_links(pages, kb_root))
    all_findings.extend(_check_frontmatter_schema(pages, kb_root))
    all_findings.extend(_check_dangling_sources(pages, kb_root))
    all_findings.extend(_check_verify_on_researched(pages, kb_root))
    all_findings.extend(_check_orphans(pages, inbound, kb_root))
    all_findings.extend(_check_stage_confidence_sanity(pages, kb_root))
    all_findings.extend(_check_provenance(pages, kb_root))
    all_findings.extend(_check_thin_pages(pages, kb_root))
    all_findings.extend(_check_citekey_integrity(pages, library, kb_root))
    all_findings.extend(_check_reachability(pages, kb_root))
    all_findings.extend(_check_near_duplicate_titles(pages, kb_root))

    if severity_filter == "error":
        all_findings = [f for f in all_findings if f.severity == "error"]

    return sorted(all_findings)


# ── Output formatters ─────────────────────────────────────────────────────────


def format_human(findings: list[Finding]) -> str:
    """Format findings as a human-readable report string."""
    if not findings:
        return "wiki lint: OK"
    lines: list[str] = []
    for f in findings:
        prefix = "ERROR" if f.severity == "error" else "WARN "
        lines.append(f"{prefix}  [{f.check}]  {f.path}: {f.message}")
    errors = sum(1 for f in findings if f.severity == "error")
    warns = sum(1 for f in findings if f.severity == "warn")
    lines.append(f"\n{errors} error(s), {warns} warning(s)")
    return "\n".join(lines)


def format_json(findings: list[Finding], kb_root: Path) -> str:
    """Format findings as a stable JSON string.

    Args:
        findings: Sorted list of findings.
        kb_root: Used for metadata only (not in output structure).

    Returns:
        Pretty-printed JSON string with findings and summary.
    """
    errors = sum(1 for f in findings if f.severity == "error")
    warns = sum(1 for f in findings if f.severity == "warn")
    payload = {
        "findings": [{"severity": f.severity, "check": f.check, "path": f.path, "message": f.message} for f in findings],
        "summary": {"errors": errors, "warns": warns},
    }
    return json_mod.dumps(payload, indent=2, ensure_ascii=False)
