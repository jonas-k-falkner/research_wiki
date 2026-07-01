from __future__ import annotations

from pathlib import Path

from wikitools.wikilib import (
    content_hash,
    inbound_links,
    iter_links,
    iter_pages,
    load_library,
    load_library_raw,
    pdf_path,
    txt_path,
    write_library,
)

FIXTURE_KB = Path(__file__).parent.parent / "fixtures" / "kb"


# ── iter_pages ────────────────────────────────────────────────────────────────


def test_iter_pages_finds_all_md(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "a.md").write_text("---\ntype: shared\n---\n# A\n")
    (tmp_path / "wiki" / "b.md").write_text("---\ntype: shared\n---\n# B\n")
    paths = [p.path for p in iter_pages(tmp_path)]
    assert len(paths) == 2


def test_iter_pages_parses_frontmatter():
    pages = list(iter_pages(FIXTURE_KB))
    src = next(p for p in pages if p.path.name == "src-test-source.md")
    assert src.type == "source"
    assert src.stage == "seed"
    assert src.confidence == "medium"
    assert "src-test-source" in src.sources


def test_iter_pages_deterministic_order():
    pages_a = [p.path for p in iter_pages(FIXTURE_KB)]
    pages_b = [p.path for p in iter_pages(FIXTURE_KB)]
    assert pages_a == pages_b


def test_iter_pages_missing_frontmatter(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "no-fm.md").write_text("# Just a heading\n\nNo frontmatter here.\n")
    pages = list(iter_pages(tmp_path))
    assert len(pages) == 1
    assert pages[0].fm_parse_error is None
    assert pages[0].type == ""


def test_iter_pages_malformed_frontmatter(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "bad.md").write_text("---\ntype: [unclosed\n---\n# body\n")
    pages = list(iter_pages(tmp_path))
    assert pages[0].fm_parse_error is not None


def test_iter_pages_title_from_h1(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "t.md").write_text("---\ntype: shared\n---\n# My Title\n\nBody.\n")
    pages = list(iter_pages(tmp_path))
    assert pages[0].title == "My Title"


def test_iter_pages_title_falls_back_to_stem(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "my-page.md").write_text("---\ntype: shared\n---\nNo heading here.\n")
    pages = list(iter_pages(tmp_path))
    assert pages[0].title == "my-page"


# ── iter_links ────────────────────────────────────────────────────────────────


def test_iter_links_extracts_relative_links():
    pages = list(iter_pages(FIXTURE_KB))
    index = next(p for p in pages if p.path.name == "index.md")
    links = list(iter_links(index))
    targets = [lk.resolved.name for lk in links]
    assert "src-test-source.md" in targets
    assert "concept-foo.md" in targets


def test_iter_links_resolves_anchor():
    pages = list(iter_pages(FIXTURE_KB))
    concept = next(p for p in pages if p.path.name == "concept-foo.md")
    links = list(iter_links(concept))
    assert any(lk.resolved.name == "src-test-source.md" for lk in links)


def test_iter_links_skips_non_md(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "p.md").write_text("---\ntype: shared\n---\n[img](img.png) [link](foo.md)\n")
    pages = list(iter_pages(tmp_path))
    links = list(iter_links(pages[0]))
    assert len(links) == 1
    assert links[0].target_raw == "foo.md"


def test_iter_links_no_links(tmp_path):
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "p.md").write_text("---\ntype: shared\n---\nNo links here.\n")
    pages = list(iter_pages(tmp_path))
    assert list(iter_links(pages[0])) == []


# ── inbound_links ─────────────────────────────────────────────────────────────


def test_inbound_links_detects_links_to_source():
    pages = list(iter_pages(FIXTURE_KB))
    inbound = inbound_links(pages)
    src = next(p for p in pages if p.path.name == "src-test-source.md")
    referrers = {p.name for p in inbound[src.path]}
    assert "index.md" in referrers


def test_inbound_links_index_has_no_inbound():
    pages = list(iter_pages(FIXTURE_KB))
    inbound = inbound_links(pages)
    index = next(p for p in pages if p.path.name == "index.md")
    assert len(inbound[index.path]) == 0


# ── content_hash ──────────────────────────────────────────────────────────────


def test_content_hash_deterministic(tmp_path):
    f = tmp_path / "f.md"
    f.write_text("hello\nworld\n")
    assert content_hash(f) == content_hash(f)


def test_content_hash_normalizes_trailing_whitespace(tmp_path):
    f1 = tmp_path / "f1.md"
    f2 = tmp_path / "f2.md"
    f1.write_text("hello   \nworld\n")
    f2.write_text("hello\nworld\n")
    assert content_hash(f1) == content_hash(f2)


def test_content_hash_differs_on_different_content(tmp_path):
    f1 = tmp_path / "f1.md"
    f2 = tmp_path / "f2.md"
    f1.write_text("hello\n")
    f2.write_text("world\n")
    assert content_hash(f1) != content_hash(f2)


# ── load_library ──────────────────────────────────────────────────────────────


def test_load_library_missing_returns_empty(tmp_path):
    result = load_library(tmp_path / "nonexistent.json")
    assert result == {}


def test_load_library_parses_items(tmp_path):
    library = tmp_path / "library.json"
    library.write_text('[{"id": "smith2024", "title": "A Paper", "author": [{"family": "Smith", "given": "J"}],"issued": {"date-parts": [[2024]]}, "DOI": "10.1234/x"}]')
    items = load_library(library)
    assert "smith2024" in items
    item = items["smith2024"]
    assert item.title == "A Paper"
    assert item.year == 2024
    assert item.doi == "10.1234/x"


def test_load_library_skips_entries_without_id(tmp_path):
    library = tmp_path / "library.json"
    library.write_text('[{"title": "No ID here"}]')
    assert load_library(library) == {}


# ── load_library_raw / write_library ──────────────────────────────────────────


def test_load_library_raw_missing_returns_empty(tmp_path):
    assert load_library_raw(tmp_path / "nonexistent.json") == {}


def test_load_library_raw_preserves_all_fields(tmp_path):
    library = tmp_path / "library.json"
    library.write_text('[{"id": "smith2024", "title": "A Paper", "custom-field": "kept", "container-title": "Journal"}]')
    entries = load_library_raw(library)
    assert entries["smith2024"]["custom-field"] == "kept"
    assert entries["smith2024"]["container-title"] == "Journal"


def test_load_library_raw_skips_entries_without_id(tmp_path):
    library = tmp_path / "library.json"
    library.write_text('[{"title": "No ID here"}]')
    assert load_library_raw(library) == {}


def test_write_library_sorts_by_citekey(tmp_path):
    library = tmp_path / "library.json"
    write_library(library, {"zebra2024": {"id": "zebra2024"}, "apple2023": {"id": "apple2023"}})
    text = library.read_text(encoding="utf-8")
    assert text.index("apple2023") < text.index("zebra2024")


def test_write_library_matches_existing_on_disk_shape(tmp_path):
    library = tmp_path / "library.json"
    write_library(library, {"smith2024": {"id": "smith2024", "title": "A Paper"}})
    assert library.read_text(encoding="utf-8") == '[\n  {"id":"smith2024","title":"A Paper"}\n]\n'


def test_write_library_empty_entries(tmp_path):
    library = tmp_path / "library.json"
    write_library(library, {})
    assert library.read_text(encoding="utf-8") == "[]\n"


def test_write_library_round_trips_through_load_library_raw(tmp_path):
    library = tmp_path / "library.json"
    entries = {"a2024": {"id": "a2024", "abstract": "x"}, "b2023": {"id": "b2023"}}
    write_library(library, entries)
    assert load_library_raw(library) == entries


def test_write_library_deterministic_regardless_of_dict_order(tmp_path):
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    write_library(a, {"b2023": {"id": "b2023"}, "a2024": {"id": "a2024"}})
    write_library(b, {"a2024": {"id": "a2024"}, "b2023": {"id": "b2023"}})
    assert a.read_text(encoding="utf-8") == b.read_text(encoding="utf-8")


# ── pdf_path / txt_path ───────────────────────────────────────────────────────


def test_pdf_path_absent(tmp_path):
    assert pdf_path(tmp_path, "smith2024") is None


def test_pdf_path_present(tmp_path):
    pdf_dir = tmp_path / "raw" / "literature" / "pdf"
    pdf_dir.mkdir(parents=True)
    (pdf_dir / "smith2024.pdf").write_bytes(b"%PDF")
    result = pdf_path(tmp_path, "smith2024")
    assert result is not None
    assert result.name == "smith2024.pdf"


def test_txt_path_absent(tmp_path):
    assert txt_path(tmp_path, "smith2024") is None


def test_txt_path_present(tmp_path):
    txt_dir = tmp_path / "raw" / "literature" / "txt"
    txt_dir.mkdir(parents=True)
    (txt_dir / "smith2024.txt").write_text("extracted text")
    result = txt_path(tmp_path, "smith2024")
    assert result is not None
    assert result.name == "smith2024.txt"
