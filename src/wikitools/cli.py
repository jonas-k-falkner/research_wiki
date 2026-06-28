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


def _cmd_index(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki index subcommand (build / update / status)."""
    from wikitools.commands.extract import MissingExtraError
    from wikitools.commands.index import LocalEmbedder, build_index, index_status, update_index

    sub = args.index_subcommand

    if sub == "status":
        import json

        status = index_status(kb_root)
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    embedder = None
    if not getattr(args, "no_embed", False):
        try:
            embedder = LocalEmbedder()
        except MissingExtraError:
            print(
                "wiki index: [warn] fastembed not installed; building lexical-only index. Install the [semantic] extra: uv sync --extra semantic",
                file=sys.stderr,
            )

    if sub == "build":
        build_index(kb_root, embedder=embedder)
        status = index_status(kb_root)
        print(f"wiki index build: {status['chunk_count']} chunks indexed")
    elif sub == "update":
        n = update_index(kb_root, embedder=embedder)
        print(f"wiki index update: {n} files reprocessed")


def _cmd_search(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki search command."""
    from wikitools.commands.search import search

    try:
        hits = search(
            args.query,
            kb_root,
            k=args.k,
            mode=args.mode,
            scope=args.scope,
        )
    except FileNotFoundError as exc:
        print(f"wiki search: {exc}", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print(f"wiki search: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json

        payload = [
            {
                "source_path": h.source_path,
                "citekey": h.citekey,
                "section": h.section,
                "score": h.score,
                "snippet": h.snippet,
            }
            for h in hits
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for i, h in enumerate(hits, start=1):
            citekey_str = f" [{h.citekey}]" if h.citekey else ""
            print(f"{i}. {h.source_path}{citekey_str} § {h.section}  (score={h.score:.4f})")
            print(f"   {h.snippet}")
            print()


def _cmd_check(args: argparse.Namespace, kb_root: Path) -> None:
    """Run the wiki check subcommand (source / claim)."""
    import json as json_mod

    from wikitools.commands.check import check_claim, check_source

    sub = args.check_subcommand

    if sub == "source":
        status = check_source(args.citekey, kb_root)
        if args.json:
            payload = {
                "citekey": args.citekey,
                "state": status.state.value,
                "page_path": str(status.page_path) if status.page_path else None,
                "recorded_hash": status.recorded_hash,
                "current_hash": status.current_hash,
            }
            print(json_mod.dumps(payload, indent=2, ensure_ascii=False))
        else:
            page_str = str(status.page_path) if status.page_path else "—"
            print(f"wiki check source: {args.citekey} → {status.state.value}  (page: {page_str})")
            if status.state.value == "changed":
                print(f"  recorded hash: {status.recorded_hash}")
                print(f"  current hash:  {status.current_hash}")

    elif sub == "claim":
        try:
            hits = check_claim(
                args.text,
                kb_root,
                citekey=args.citekey or None,
                page=args.page or None,
                k=args.k,
                mode=args.mode,
            )
        except FileNotFoundError as exc:
            print(f"wiki check claim: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.json:
            claim_payload = [
                {
                    "source_path": h.source_path,
                    "section": h.section,
                    "snippet": h.snippet,
                    "score": h.score,
                    "cites_queried_source": h.cites_queried_source,
                    "classification": h.classification.value,
                }
                for h in hits
            ]
            print(json_mod.dumps(claim_payload, indent=2, ensure_ascii=False))
        else:
            if not hits:
                print("wiki check claim: no similar claims found — likely new")
            else:
                for h in hits:
                    cites = " [cites-source]" if h.cites_queried_source else ""
                    print(f"[{h.classification.value}]{cites}  {h.source_path} § {h.section}  (score={h.score:.4f})")
                    print(f"   {h.snippet}")
                    print()


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
    index_p = subparsers.add_parser("index", help="Build or update the search index.")
    index_sub = index_p.add_subparsers(dest="index_subcommand", metavar="SUBCOMMAND")
    index_sub.required = True
    index_build_p = index_sub.add_parser("build", help="Full corpus rebuild: chunk, embed, and FTS-index.")
    index_build_p.add_argument("--no-embed", action="store_true", help="Skip embedding (lexical-only index).")
    index_update_p = index_sub.add_parser("update", help="Incremental update: reprocess only changed files.")
    index_update_p.add_argument("--no-embed", action="store_true", help="Skip embedding for changed files.")
    index_sub.add_parser("status", help="Report index counts and metadata.")

    search_p = subparsers.add_parser("search", help="Search the wiki and literature corpus.")
    search_p.add_argument("query", help="Free-text query string.")
    search_p.add_argument("--mode", choices=["lexical", "semantic", "hybrid"], default="hybrid", help="Search mode (default: hybrid).")
    search_p.add_argument("-k", type=int, default=10, help="Number of results (default: 10).")
    search_p.add_argument("--scope", choices=["wiki", "literature"], default=None, help="Restrict to wiki pages or literature chunks.")
    search_p.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    check_p = subparsers.add_parser("check", help="Check source idempotency and claim deduplication.")
    check_sub = check_p.add_subparsers(dest="check_subcommand", metavar="SUBCOMMAND")
    check_sub.required = True
    check_source_p = check_sub.add_parser("source", help="Check whether a citekey has already been ingested.")
    check_source_p.add_argument("--citekey", required=True, metavar="KEY", help="Zotero citekey to check.")
    check_source_p.add_argument("--json", action="store_true", help="Emit structured JSON output.")
    check_claim_p = check_sub.add_parser("claim", help="Search for existing claims similar to the given text.")
    check_claim_p.add_argument("text", help="Candidate claim text to check.")
    check_claim_p.add_argument("--citekey", metavar="KEY", default=None, help="Citekey of the source being ingested (marks whether hits already cite it).")
    check_claim_p.add_argument("--page", metavar="PATH", default=None, help="Relative path of the page being edited (excluded from results).")
    check_claim_p.add_argument("--mode", choices=["lexical", "semantic", "hybrid"], default="hybrid", help="Search mode (default: hybrid).")
    check_claim_p.add_argument("-k", type=int, default=10, help="Maximum results (default: 10).")
    check_claim_p.add_argument("--json", action="store_true", help="Emit structured JSON output.")

    args = parser.parse_args()
    kb_root = resolve_kb_root(args.kb)

    if args.command == "lint":
        _cmd_lint(args, kb_root)
    elif args.command == "extract":
        _cmd_extract(args, kb_root)
    elif args.command == "toc":
        if args.toc_subcommand == "build":
            _cmd_toc_build(args, kb_root)
    elif args.command == "index":
        _cmd_index(args, kb_root)
    elif args.command == "search":
        _cmd_search(args, kb_root)
    elif args.command == "check":
        _cmd_check(args, kb_root)
    else:
        print(f"wiki {args.command}: not implemented", file=sys.stderr)
        sys.exit(1)
