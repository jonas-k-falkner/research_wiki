from __future__ import annotations

import json
from pathlib import Path

import pytest

from wikitools.commands.lint import format_json, run_lint

FIXTURE_KB = Path(__file__).parent.parent / "fixtures" / "kb"

# ── Minimal valid frontmatter helpers ────────────────────────────────────────


def _valid_fm(**overrides: object) -> str:
    fm = {
        "type": "concept",
        "domain": "shared",
        "project": "shared",
        "status": "active",
        "stage": "seed",
        "confidence": "medium",
        "updated": "2026-01-01",
        "sources": ["src-test-source"],
        "tags": [],
    }
    fm.update(overrides)
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _long_body() -> str:
    return "# Title\n\n" + "This is a sufficiently long body with enough content. " * 5


# ── Fixture kb: zero errors ───────────────────────────────────────────────────


def test_fixture_kb_zero_errors():
    findings = run_lint(FIXTURE_KB)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], f"Unexpected errors: {errors}"


# ── Broken links (error) ──────────────────────────────────────────────────────


def test_broken_link_detected(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "bad-link.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm() + _long_body() + "\n[Dead](../nonexistent.md)\n")
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "broken-links"]
    assert len(errors) >= 1
    assert errors[0].severity == "error"
    assert "nonexistent.md" in errors[0].message


def test_valid_link_no_error(tmp_path):
    _make_kb(tmp_path)
    findings = run_lint(tmp_path)
    assert not any(f.check == "broken-links" for f in findings)


# ── Fix: strip dead links ─────────────────────────────────────────────────────


def test_fix_strips_dead_link(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "fixable.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm() + _long_body() + "\n[DeadText](../gone.md) stays.\n")
    # One error before fix
    assert any(f.check == "broken-links" for f in run_lint(tmp_path))
    run_lint(tmp_path, fix=True)
    after = page.read_text()
    assert "[DeadText](../gone.md)" not in after
    assert "DeadText" in after  # text preserved
    # No errors after fix
    assert not any(f.check == "broken-links" for f in run_lint(tmp_path) if "fixable" in f.path)


def test_fix_leaves_prose_unchanged(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "prose.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    prose = "Some important claim about the research area.\n"
    page.write_text(_valid_fm() + "# Title\n\n" + prose * 5)
    run_lint(tmp_path, fix=True)
    after = page.read_text()
    assert prose in after


# ── Frontmatter schema (error) ────────────────────────────────────────────────


def test_missing_required_key(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "missing.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    # FM without 'stage'
    page.write_text("---\ntype: concept\nstatus: active\nconfidence: medium\nupdated: 2026-01-01\nsources:\n  - src-test-source\ntags: []\n---\n# T\n\n" + "body " * 40)
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "frontmatter-schema" and "stage" in f.message]
    assert len(errors) >= 1


def test_invalid_enum_value(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "badenum.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(stage="unknown-stage") + _long_body())
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "frontmatter-schema" and "stage" in f.message]
    assert len(errors) >= 1


def test_invalid_updated_date(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "baddate.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(updated="not-a-date") + _long_body())
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "frontmatter-schema" and "updated" in f.message]
    assert len(errors) >= 1


def test_malformed_yaml_frontmatter(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "badfm.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("---\ntype: [unclosed\n---\n# Title\n\nbody body body body body body body\n")
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "frontmatter-schema"]
    assert len(errors) >= 1


# ── Dangling sources (error) ──────────────────────────────────────────────────


def test_dangling_source_detected(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "dangling.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(sources=["src-does-not-exist"]) + _long_body())
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "dangling-sources"]
    assert len(errors) >= 1
    assert "src-does-not-exist" in errors[0].message


# ── [verify] on researched pages (error) ─────────────────────────────────────


def test_verify_on_researched_is_error(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "researched.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(stage="researched") + "# T\n\nSome claim [verify] needs citation.\n" + "body " * 20)
    findings = run_lint(tmp_path)
    errors = [f for f in findings if f.check == "verify-on-researched"]
    assert len(errors) == 1
    assert errors[0].severity == "error"


def test_verify_on_seed_not_error(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "seedverify.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(stage="seed") + _long_body() + "\n[verify] this claim\n")
    findings = run_lint(tmp_path)
    assert not any(f.check == "verify-on-researched" for f in findings)


# ── Stage/confidence sanity (warn) ────────────────────────────────────────────


def test_seed_high_confidence_is_warn(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "seedhigh.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(stage="seed", confidence="high") + _long_body())
    findings = run_lint(tmp_path)
    warns = [f for f in findings if f.check == "stage-confidence-sanity"]
    assert len(warns) >= 1
    assert warns[0].severity == "warn"


# ── Orphans (warn) ────────────────────────────────────────────────────────────


def test_orphan_page_is_warn(tmp_path):
    _make_kb(tmp_path)
    # Add a page not linked from anywhere
    orphan = tmp_path / "wiki" / "concepts" / "lost.md"
    orphan.parent.mkdir(parents=True, exist_ok=True)
    orphan.write_text(_valid_fm() + _long_body())
    findings = run_lint(tmp_path)
    warns = [f for f in findings if f.check == "orphans" and "lost.md" in f.path]
    assert len(warns) == 1
    assert warns[0].severity == "warn"


def test_nav_roots_not_orphaned(tmp_path):
    _make_kb(tmp_path)
    findings = run_lint(tmp_path)
    orphan_paths = {f.path for f in findings if f.check == "orphans"}
    assert not any("index.md" in p or "log.md" in p for p in orphan_paths)


# ── Severity filter ───────────────────────────────────────────────────────────


def test_severity_error_filters_warns(tmp_path):
    _make_kb(tmp_path)
    page = tmp_path / "wiki" / "concepts" / "seedhigh.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(_valid_fm(stage="seed", confidence="high") + _long_body())
    all_findings = run_lint(tmp_path, severity_filter="warn")
    error_only = run_lint(tmp_path, severity_filter="error")
    assert len(error_only) <= len(all_findings)
    assert all(f.severity == "error" for f in error_only)


# ── JSON output stability ─────────────────────────────────────────────────────


def test_json_output_stable():
    findings_a = run_lint(FIXTURE_KB)
    findings_b = run_lint(FIXTURE_KB)
    out_a = format_json(findings_a, FIXTURE_KB)
    out_b = format_json(findings_b, FIXTURE_KB)
    assert out_a == out_b


def test_json_schema_valid():
    findings = run_lint(FIXTURE_KB)
    payload = json.loads(format_json(findings, FIXTURE_KB))
    assert "findings" in payload
    assert "summary" in payload
    assert "errors" in payload["summary"]
    assert "warns" in payload["summary"]
    for f in payload["findings"]:
        assert "severity" in f
        assert "check" in f
        assert "path" in f
        assert "message" in f


# ── Integration test ──────────────────────────────────────────────────────────


@pytest.mark.integration
def test_real_kb_has_zero_errors():
    real_kb = Path(__file__).parent.parent.parent / "kb"
    findings = run_lint(real_kb)
    errors = [f for f in findings if f.severity == "error"]
    assert errors == [], "Real kb has errors:\n" + "\n".join(f"{f.path}: {f.message}" for f in errors)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_kb(root: Path) -> None:
    """Scaffold a minimal valid kb under root."""
    (root / "wiki" / "sources").mkdir(parents=True, exist_ok=True)
    (root / "wiki" / "concepts").mkdir(parents=True, exist_ok=True)
    (root / "raw" / "seed").mkdir(parents=True, exist_ok=True)
    (root / "raw" / "seed" / "test-source.md").write_text("# Raw\n")

    (root / "wiki" / "index.md").write_text(
        "---\ntype: shared\ndomain: shared\nproject: shared\nstatus: active\n"
        "stage: seed\nconfidence: medium\nupdated: 2026-01-01\nsources:\n  - src-test-source\ntags: []\n---\n"
        "# Index\n\n[Source](sources/src-test-source.md)\n"
    )
    (root / "wiki" / "log.md").write_text(
        "---\ntype: shared\ndomain: shared\nproject: shared\nstatus: active\n"
        "stage: seed\nconfidence: medium\nupdated: 2026-01-01\nsources:\n  - src-test-source\ntags: []\n---\n"
        "# Log\n\n- Entry.\n"
    )
    (root / "wiki" / "sources" / "src-test-source.md").write_text(
        "---\ntype: source\ndomain: shared\nproject: shared\nstatus: active\n"
        "stage: seed\nconfidence: medium\nupdated: 2026-01-01\nsources:\n  - src-test-source\ntags: []\n---\n"
        "# Source\n\n- Raw path: `raw/seed/test-source.md`\n\n" + "Body content. " * 15
    )
