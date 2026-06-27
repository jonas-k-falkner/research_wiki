"""CLI dispatcher for the wiki tooling package."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_SUBCOMMANDS = ("lint", "toc", "extract", "index", "search", "check")


def _load_wikitools_config() -> dict[str, object]:
    """Load [tool.wikitools] from pyproject.toml relative to cwd."""
    import tomllib  # stdlib in Python 3.11+

    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        return {}
    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)
    result: dict[str, object] = data.get("tool", {}).get("wikitools", {})
    return result


def resolve_kb_root(kb_flag: str | None) -> Path:
    """Resolve the knowledge-base root from CLI flag, env var, or pyproject config.

    Args:
        kb_flag: Value passed via ``--kb``; ``None`` when omitted.

    Returns:
        Resolved path to the kb root directory.
    """
    if kb_flag:
        return Path(kb_flag)
    env = os.environ.get("WIKI_KB")
    if env:
        return Path(env)
    cfg = _load_wikitools_config()
    return Path(str(cfg.get("kb_root", "kb")))


def main() -> None:
    """Entry point for the ``wiki`` CLI dispatcher."""
    parser = argparse.ArgumentParser(
        prog="wiki",
        description="Research wiki tooling: lint, toc, extract, index, search, check.",
    )
    parser.add_argument(
        "--kb",
        metavar="PATH",
        default=None,
        help="Knowledge-base root path (overrides WIKI_KB env var and pyproject config).",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    subparsers.add_parser("lint", help="Run health checks over wiki pages.")
    subparsers.add_parser("toc", help="Generate root and per-domain index pages.")
    subparsers.add_parser("extract", help="Extract text from literature PDFs.")
    subparsers.add_parser("index", help="Build or update the search index.")
    subparsers.add_parser("search", help="Search the wiki and literature corpus.")
    subparsers.add_parser("check", help="Check source idempotency and claim deduplication.")

    args = parser.parse_args()

    print(f"wiki {args.command}: not implemented", file=sys.stderr)
    sys.exit(1)
