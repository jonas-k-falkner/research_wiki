"""Wiki TOC generator: root index and per-domain catalog pages."""

from __future__ import annotations

import logging
from pathlib import Path

from wikitools.wikilib import Page, iter_pages

logger = logging.getLogger(__name__)

_AUTO_START = "<!-- AUTO:start -->"
_AUTO_END = "<!-- AUTO:end -->"

_DOMAIN_DISPLAY: dict[str, str] = {
    "timeseries-forecasting": "Time-series forecasting",
    "embedding-models": "Embedding models",
    "scenario-engine": "Scenario engine",
    "nowcasting-graph": "Nowcasting graph",
    "shared": "Shared",
}

_TYPE_ORDER: dict[str, int] = {
    "project": 0,
    "domain": 1,
    "concept": 2,
    "entity": 3,
    "comparison": 4,
    "decision": 5,
    "experiment": 6,
    "query": 7,
    "source": 8,
    "shared": 9,
}


def _rewrite_auto_region(existing: str, new_content: str) -> str:
    """Replace content between AUTO fences; append fences at end if absent.

    Args:
        existing: Full text of the file to rewrite.
        new_content: Replacement content to place between the fences.

    Returns:
        Updated file text with the AUTO region replaced or appended.
    """
    start_idx = existing.find(_AUTO_START)
    end_idx = existing.find(_AUTO_END)

    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
        before = existing[:start_idx]
        after = existing[end_idx + len(_AUTO_END) :]
        return f"{before}{_AUTO_START}\n{new_content}\n{_AUTO_END}{after}"

    # No fences — append at end, ensuring single trailing newline before
    tail = existing.rstrip("\n")
    return f"{tail}\n\n{_AUTO_START}\n{new_content}\n{_AUTO_END}\n"


def _page_sort_key(page: Page) -> tuple[int, str]:
    """Return sort key (type_order, title) for deterministic catalog ordering.

    Args:
        page: Wiki page.

    Returns:
        Tuple of (type_order_int, lowercase_title).
    """
    return (_TYPE_ORDER.get(page.type, 99), page.title.lower())


def _relative_link(from_dir: Path, target: Path) -> str:
    """Compute a relative Markdown link path from from_dir to target.

    Args:
        from_dir: Directory containing the page with the link.
        target: Absolute path to the target page.

    Returns:
        Relative POSIX path string suitable for a Markdown link.
    """
    return target.relative_to(from_dir, walk_up=True).as_posix()


def generate_domain_index(pages: list[Page], domain: str, kb_root: Path) -> str:
    """Generate the AUTO region content for a domain catalog page.

    Args:
        pages: All wiki pages.
        domain: Domain slug (e.g. ``timeseries-forecasting``).
        kb_root: Resolved path to kb root.

    Returns:
        String to place inside the AUTO fences of the domain index.
    """
    domain_pages = [p for p in pages if p.domain == domain and p.path.name != "index.md"]
    domain_pages.sort(key=_page_sort_key)

    domain_index_dir = kb_root / "wiki" / "domains" / domain

    rows: list[str] = []
    for p in domain_pages:
        rel = _relative_link(domain_index_dir, p.path)
        rows.append(f"| [{p.title}]({rel}) | {p.type} | {p.stage} | {p.status} |")

    table_header = "| Title | Type | Stage | Status |\n|---|---|---|---|"
    table_body = "\n".join(rows) if rows else "_No pages yet._"

    display = _DOMAIN_DISPLAY.get(domain, domain)
    stage_counts: dict[str, int] = {}
    for p in domain_pages:
        stage_counts[p.stage] = stage_counts.get(p.stage, 0) + 1
    rollup_parts = [f"{v} {k}" for k, v in sorted(stage_counts.items())]
    rollup = ", ".join(rollup_parts) if rollup_parts else "0 pages"

    return f"## {display} — page catalog\n\n{table_header}\n{table_body}\n\n_{len(domain_pages)} page(s): {rollup}._"


def _new_domain_index(domain: str, kb_root: Path, auto_content: str) -> str:
    """Build a complete new domain index file from scratch.

    Args:
        domain: Domain slug.
        kb_root: Resolved path to kb root.
        auto_content: Content to place inside the AUTO fences.

    Returns:
        Full file text for the new domain index.
    """
    display = _DOMAIN_DISPLAY.get(domain, domain)
    rel_to_wiki = "../../index.md"
    frontmatter = f"""---
type: shared
domain: {domain}
project: shared
status: active
stage: seed
confidence: low
updated: {_today()}
sources: []
tags:
  - index
---"""
    return f"""{frontmatter}

# Domain index: {display}

_Generated catalog. Edit prose outside the AUTO fences; run `wiki toc build` to refresh._

[← Wiki index]({rel_to_wiki})

{_AUTO_START}
{auto_content}
{_AUTO_END}
"""


def _today() -> str:
    """Return today's date as YYYY-MM-DD.

    Returns:
        ISO date string.
    """
    from datetime import date

    return date.today().isoformat()


def generate_root(pages: list[Page], kb_root: Path) -> str:
    """Generate the AUTO region content for the root index page.

    Args:
        pages: All wiki pages.
        kb_root: Resolved path to kb root.

    Returns:
        String to place inside the AUTO fences of wiki/index.md.
    """
    wiki_root = kb_root / "wiki"
    index_dir = wiki_root

    domains = sorted({p.domain for p in pages if p.domain and p.domain != "shared"})

    lines: list[str] = []
    lines.append("## Domain indexes\n")
    lines.append("| Domain | Pages | Stages |")
    lines.append("|---|---|---|")

    for domain in domains:
        domain_pages = [p for p in pages if p.domain == domain and p.path.name != "index.md"]
        count = len(domain_pages)
        stage_counts: dict[str, int] = {}
        for p in domain_pages:
            stage_counts[p.stage] = stage_counts.get(p.stage, 0) + 1
        rollup_parts = [f"{v} {k}" for k, v in sorted(stage_counts.items())]
        rollup = ", ".join(rollup_parts) if rollup_parts else "—"
        display = _DOMAIN_DISPLAY.get(domain, domain)
        domain_index = wiki_root / "domains" / domain / "index.md"
        rel = _relative_link(index_dir, domain_index)
        lines.append(f"| [{display}]({rel}) | {count} | {rollup} |")

    # Shared pages summary
    shared_pages = [p for p in pages if p.domain == "shared" and p.path.name not in {"index.md", "log.md", "overview.md"}]
    shared_pages.sort(key=_page_sort_key)
    lines.append("")
    lines.append("## Shared pages\n")
    for p in shared_pages:
        rel = _relative_link(index_dir, p.path)
        lines.append(f"- [{p.title}]({rel})")

    total = sum(1 for p in pages if p.path.name not in {"index.md", "log.md", "overview.md"})
    lines.append("")
    lines.append(f"_{total} total pages across {len(domains)} domain(s) + shared._")

    return "\n".join(lines)


def build_toc(kb_root: Path, *, check: bool = False) -> bool:
    """Build or check root index and all domain catalog pages.

    Reads all wiki pages, generates each domain index and the root AUTO region,
    and writes any changed files unless ``check`` is True.

    Args:
        kb_root: Resolved path to kb root.
        check: If True, detect changes but do not write.

    Returns:
        True if any file was (or would be) changed; False if already up-to-date.

    Raises:
        ValueError: If ``kb_root/wiki/`` does not exist.
    """
    kb_root = kb_root.resolve()
    wiki_root = kb_root / "wiki"
    if not wiki_root.exists():
        raise ValueError(f"No wiki/ directory under {kb_root}")

    pages = list(iter_pages(kb_root))
    changed = False

    # Determine all non-shared domains from page metadata
    domains = sorted({p.domain for p in pages if p.domain and p.domain != "shared"})

    for domain in domains:
        domain_dir = wiki_root / "domains" / domain
        index_path = domain_dir / "index.md"
        auto_content = generate_domain_index(pages, domain, kb_root)

        if index_path.exists():
            existing = index_path.read_text(encoding="utf-8")
            new_text = _rewrite_auto_region(existing, auto_content)
        else:
            new_text = _new_domain_index(domain, kb_root, auto_content)

        existing_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
        if new_text != existing_text:
            changed = True
            if not check:
                domain_dir.mkdir(parents=True, exist_ok=True)
                index_path.write_text(new_text, encoding="utf-8")
                logger.info("Updated domain index: %s", index_path)

    # Root index AUTO region
    root_index = wiki_root / "index.md"
    if root_index.exists():
        root_existing = root_index.read_text(encoding="utf-8")
        root_auto = generate_root(pages, kb_root)
        root_new = _rewrite_auto_region(root_existing, root_auto)
        if root_new != root_existing:
            changed = True
            if not check:
                root_index.write_text(root_new, encoding="utf-8")
                logger.info("Updated root index: %s", root_index)

    return changed
