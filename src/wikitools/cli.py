"""CLI dispatcher for the wiki tooling package."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


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


def _cmd_lint(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki lint command."""
    from wikitools.commands.lint import format_human, format_json, run_lint

    try:
        findings = run_lint(kb_root, fix=args.fix, severity_filter=args.severity)
    except ValueError as exc:
        print(f"wiki lint: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(format_json(findings, kb_root))
    else:
        print(format_human(findings))

    if any(f.severity == "error" for f in findings):
        sys.exit(1)


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

    lint_p = subparsers.add_parser("lint", help="Run health checks over wiki pages.")
    lint_p.add_argument("--json", action="store_true", help="Emit structured JSON output.")
    lint_p.add_argument("--fix", action="store_true", help="Apply safe auto-fixes (strip dead links, normalize frontmatter order).")
    lint_p.add_argument("--severity", choices=["error", "warn"], default="warn", help="Minimum severity to report (default: warn).")

    subparsers.add_parser("toc", help="Generate root and per-domain index pages.")
    subparsers.add_parser("extract", help="Extract text from literature PDFs.")
    subparsers.add_parser("index", help="Build or update the search index.")
    subparsers.add_parser("search", help="Search the wiki and literature corpus.")
    subparsers.add_parser("check", help="Check source idempotency and claim deduplication.")

    args = parser.parse_args()
    kb_root = resolve_kb_root(args.kb)

    if args.command == "lint":
        _cmd_lint(args, kb_root)
    else:
        print(f"wiki {args.command}: not implemented", file=sys.stderr)
        sys.exit(1)
