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


def _cmd_extract(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki extract command."""
    from wikitools.commands.extract import MissingExtraError, _resolve_engine, run_extract

    _, degraded = _resolve_engine(args.engine)
    if degraded:
        print(
            "wiki extract: [warn] docling not installed; using fast path — math in equations will be degraded. Install the [ocr] extra: uv sync --extra ocr",
            file=sys.stderr,
        )

    try:
        extracted, skipped, issues = run_extract(
            kb_root,
            engine=args.engine,
            force=args.force,
            citekey=args.citekey or None,
        )
    except MissingExtraError as exc:
        print(f"wiki extract: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"wiki extract: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json

        payload = {
            "extracted": extracted,
            "skipped": skipped,
            "reconciliation_issues": [{"kind": i.kind, "path": i.path, "message": i.message} for i in issues],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for issue in issues:
            print(f"RECONCILE  [{issue.kind}]  {issue.path}: {issue.message}")
        print(f"wiki extract: {extracted} extracted, {skipped} skipped")


def _cmd_toc_build(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki toc build subcommand."""
    from wikitools.commands.toc import build_toc

    try:
        changed = build_toc(kb_root, check=args.check)
    except ValueError as exc:
        print(f"wiki toc build: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        if changed:
            print("wiki toc build: index(es) are stale — run `wiki toc build` to update", file=sys.stderr)
            sys.exit(1)
        else:
            print("wiki toc build: up-to-date")
    else:
        if changed:
            print("wiki toc build: indexes updated")
        else:
            print("wiki toc build: already up-to-date")


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

    toc_p = subparsers.add_parser("toc", help="Generate root and per-domain index pages.")
    toc_sub = toc_p.add_subparsers(dest="toc_subcommand", metavar="SUBCOMMAND")
    toc_sub.required = True
    toc_build_p = toc_sub.add_parser("build", help="Write root and domain index pages.")
    toc_build_p.add_argument("--check", action="store_true", help="Exit non-zero if indexes are stale; do not write.")

    extract_p = subparsers.add_parser("extract", help="Extract text from literature PDFs.")
    extract_p.add_argument("--engine", choices=["fast", "docling", "marker"], default=None, help="Extraction engine (default: docling if [ocr] extra installed, else fast).")
    extract_p.add_argument("--force", action="store_true", help="Re-extract even when source hash is unchanged.")
    extract_p.add_argument("--citekey", metavar="KEY", default=None, help="Process only PDFs with this citekey.")
    extract_p.add_argument("--json", action="store_true", help="Emit structured JSON output.")
    subparsers.add_parser("index", help="Build or update the search index.")
    subparsers.add_parser("search", help="Search the wiki and literature corpus.")
    subparsers.add_parser("check", help="Check source idempotency and claim deduplication.")

    args = parser.parse_args()
    kb_root = resolve_kb_root(args.kb)

    if args.command == "lint":
        _cmd_lint(args, kb_root)
    elif args.command == "extract":
        _cmd_extract(args, kb_root)
    elif args.command == "toc":
        if args.toc_subcommand == "build":
            _cmd_toc_build(args, kb_root)
    else:
        print(f"wiki {args.command}: not implemented", file=sys.stderr)
        sys.exit(1)
