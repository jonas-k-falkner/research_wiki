"""DuckDB-backed corpus index: chunking, embedding, FTS + vector build/update/status."""

from __future__ import annotations

import hashlib
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import duckdb as duckdb_type

logger = logging.getLogger(__name__)

# ── constants ─────────────────────────────────────────────────────────────────

_CHUNK_WINDOW = 800
_CHUNK_OVERLAP = 100
_EMBED_DIM = 384


# ── data types ────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Chunk:
    """One indexable unit of text.

    Attributes:
        source_path: Relative path string (from kb_root) identifying the origin file.
        citekey: Zotero citekey for literature chunks; ``None`` for wiki pages.
        section: Section title (wiki) or approximate page label (PDF).
        text: Raw text content of this chunk.
    """

    source_path: str
    citekey: str | None
    section: str
    text: str


# ── chunking ─────────────────────────────────────────────────────────────────


def _heading_split(text: str) -> list[tuple[str, str]]:
    """Split a markdown body on H2/H3 headings.

    Args:
        text: Full markdown text including frontmatter (stripped before parsing).

    Returns:
        List of ``(section_title, body_text)`` pairs.  The preamble before the first
        heading is emitted under the title ``"intro"`` when non-empty.
    """
    # Strip YAML frontmatter
    stripped = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    parts: list[tuple[str, str]] = []
    current_title = "intro"
    current_lines: list[str] = []
    for line in stripped.splitlines():
        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if m:
            body = "\n".join(current_lines).strip()
            if body or current_title != "intro":
                parts.append((current_title, body))
            current_title = m.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)
    body = "\n".join(current_lines).strip()
    if body or current_title != "intro":
        parts.append((current_title, body))
    return parts


def chunk_wiki_page(page_path: Path, kb_root: Path) -> list[Chunk]:
    """Chunk a wiki markdown page by H2/H3 headings.

    Args:
        page_path: Absolute path to the wiki page.
        kb_root: Knowledge-base root (for computing relative source path).

    Returns:
        List of ``Chunk`` objects, one per heading section (or the whole page if no
        headings are present).
    """
    try:
        text = page_path.read_text(encoding="utf-8")
    except OSError:
        logger.warning("chunk_wiki_page: cannot read %s", page_path)
        return []

    rel = page_path.relative_to(kb_root).as_posix()
    sections = _heading_split(text)
    if not sections:
        return [Chunk(source_path=rel, citekey=None, section="body", text=text.strip())]
    chunks: list[Chunk] = []
    for title, body in sections:
        if body:
            chunks.append(Chunk(source_path=rel, citekey=None, section=title, text=body))
    return chunks


def chunk_txt(txt_path: Path, citekey: str, kb_root: Path) -> list[Chunk]:
    """Chunk a plain-text/markdown file with a sliding window.

    Args:
        txt_path: Absolute path to the extracted ``.txt`` file.
        citekey: Zotero citekey of the parent item.
        kb_root: Knowledge-base root (for computing relative source path).

    Returns:
        List of ``Chunk`` objects produced by sliding-window splitting.
    """
    try:
        text = txt_path.read_text(encoding="utf-8")
    except OSError:
        logger.warning("chunk_txt: cannot read %s", txt_path)
        return []

    rel = txt_path.relative_to(kb_root).as_posix()
    chunks: list[Chunk] = []
    start = 0
    total = len(text)
    idx = 0
    while start < total:
        end = min(start + _CHUNK_WINDOW, total)
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(Chunk(source_path=rel, citekey=citekey, section=f"chunk-{idx}", text=chunk_text))
        idx += 1
        if end >= total:
            break
        start = end - _CHUNK_OVERLAP
    return chunks


# ── embedder interface ────────────────────────────────────────────────────────


class Embedder(ABC):
    """Abstract base for embedding providers."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts.

        Args:
            texts: Non-empty list of text strings to embed.

        Returns:
            List of float vectors, same length as ``texts``.  Each vector has exactly
            ``_EMBED_DIM`` dimensions.
        """


class LocalEmbedder(Embedder):
    """Local ONNX embedder via fastembed (``[semantic]`` extra).

    Args:
        model: Model identifier; defaults to ``BAAI/bge-small-en-v1.5``.
    """

    def __init__(self, model: str = "BAAI/bge-small-en-v1.5") -> None:
        """Initialise and load the embedding model.

        Args:
            model: fastembed model identifier.

        Raises:
            MissingExtraError: If ``fastembed`` is not installed.
        """
        from wikitools.commands.extract import MissingExtraError

        try:
            from fastembed import TextEmbedding
        except ImportError as exc:
            raise MissingExtraError("LocalEmbedder requires the [semantic] extra. Install with: uv sync --extra semantic") from exc
        self._model = TextEmbedding(model_name=model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts using the loaded fastembed model.

        Args:
            texts: List of strings to embed.

        Returns:
            List of 384-dimensional float vectors.
        """
        return [v.tolist() for v in self._model.embed(texts)]


class OpenAIEmbedder(Embedder):
    """OpenAI embeddings via the ``[api]`` extra.

    Args:
        model: OpenAI embedding model identifier.
    """

    def __init__(self, model: str = "text-embedding-3-small") -> None:
        """Initialise the OpenAI client.

        Args:
            model: OpenAI embedding model identifier.

        Raises:
            MissingExtraError: If ``openai`` is not installed.
        """
        from wikitools.commands.extract import MissingExtraError

        try:
            import openai
        except ImportError as exc:
            raise MissingExtraError("OpenAIEmbedder requires the [api] extra. Install with: uv sync --extra api") from exc
        self._client = openai.OpenAI()
        self._model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed texts using the OpenAI API.

        Args:
            texts: List of strings to embed.

        Returns:
            List of float vectors.
        """
        resp = self._client.embeddings.create(input=texts, model=self._model)
        return [item.embedding for item in resp.data]


# ── DB helpers ────────────────────────────────────────────────────────────────


def _db_path(kb_root: Path) -> Path:
    """Return the DuckDB corpus path for the given kb_root.

    Args:
        kb_root: Knowledge-base root directory.

    Returns:
        Path to ``corpus.duckdb`` inside ``.wiki/``.
    """
    return kb_root / ".wiki" / "corpus.duckdb"


def _open_db(kb_root: Path) -> duckdb_type.DuckDBPyConnection:
    """Open (or create) the DuckDB corpus at the canonical path.

    Args:
        kb_root: Knowledge-base root directory.

    Returns:
        Open DuckDB connection.
    """
    import duckdb

    db_file = _db_path(kb_root)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_file))
    return con


def _ensure_schema(con: duckdb_type.DuckDBPyConnection) -> None:
    """Create tables and FTS index if they do not exist.

    Args:
        con: Open DuckDB connection.
    """
    con.execute("INSTALL fts")
    con.execute("LOAD fts")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id          INTEGER PRIMARY KEY,
            source_path VARCHAR NOT NULL,
            citekey     VARCHAR,
            section     VARCHAR NOT NULL,
            text        VARCHAR NOT NULL,
            embedding   FLOAT[384]
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key   VARCHAR PRIMARY KEY,
            value VARCHAR NOT NULL
        )
        """
    )


def _rebuild_fts(con: duckdb_type.DuckDBPyConnection) -> None:
    """Drop and rebuild the FTS index on ``chunks.text``.

    Args:
        con: Open DuckDB connection.
    """
    import contextlib

    with contextlib.suppress(Exception):
        con.execute("DROP FTS INDEX IF EXISTS chunks_fts")
    con.execute("PRAGMA create_fts_index('chunks', 'id', 'text', overwrite=1)")


def _file_hash(path: Path) -> str:
    """Return SHA-256 hex of file bytes.

    Args:
        path: File to hash.

    Returns:
        64-char hex string.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ── build / update ────────────────────────────────────────────────────────────


def _collect_wiki_chunks(kb_root: Path) -> list[Chunk]:
    """Collect all chunks from wiki markdown pages.

    Args:
        kb_root: Knowledge-base root directory.

    Returns:
        All chunks from wiki pages.
    """
    wiki_dir = kb_root / "wiki"
    if not wiki_dir.is_dir():
        return []
    chunks: list[Chunk] = []
    for md in sorted(wiki_dir.rglob("*.md")):
        chunks.extend(chunk_wiki_page(md, kb_root))
    return chunks


def _collect_txt_chunks(kb_root: Path) -> list[Chunk]:
    """Collect all chunks from extracted PDF text files.

    Args:
        kb_root: Knowledge-base root directory.

    Returns:
        All chunks from literature txt files.
    """
    txt_dir = kb_root / "raw" / "literature" / "txt"
    if not txt_dir.is_dir():
        return []
    chunks: list[Chunk] = []
    for txt in sorted(txt_dir.glob("*.txt")):
        stem = txt.stem
        # citekey: strip -suppl suffix for supplement files
        citekey = stem[: -len("-suppl")] if stem.endswith("-suppl") else stem
        chunks.extend(chunk_txt(txt, citekey, kb_root))
    return chunks


def build_index(
    kb_root: Path,
    embedder: Embedder | None = None,
    embed_dim: int = _EMBED_DIM,
    batch_size: int = 256,
) -> None:
    """Full corpus rebuild: chunk, embed, and FTS-index all wiki pages and txt files.

    Args:
        kb_root: Knowledge-base root directory.
        embedder: Embedding provider.  When ``None``, embeddings are stored as ``NULL``.
        embed_dim: Dimensionality of embedding vectors (must match schema).
        batch_size: Number of chunks per embedding batch.  Larger batches are faster
            but use more memory.  Progress is logged after each batch.
    """
    con = _open_db(kb_root)
    _ensure_schema(con)

    # Drop existing content for full rebuild
    con.execute("DELETE FROM chunks")
    con.execute("DELETE FROM meta")

    wiki_chunks = _collect_wiki_chunks(kb_root)
    txt_chunks = _collect_txt_chunks(kb_root)
    all_chunks = wiki_chunks + txt_chunks

    logger.info("build_index: %d wiki chunks, %d txt chunks", len(wiki_chunks), len(txt_chunks))

    _insert_chunks(con, all_chunks, embedder, batch_size=batch_size)
    _rebuild_fts(con)

    ts = str(int(time.time()))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('last_build', ?)", [ts])
    model_name = type(embedder).__name__ if embedder else "none"
    con.execute("INSERT OR REPLACE INTO meta VALUES ('embed_model', ?)", [model_name])
    con.execute("INSERT OR REPLACE INTO meta VALUES ('embed_dim', ?)", [str(embed_dim)])
    con.close()

    logger.info("build_index: done (%d total chunks)", len(all_chunks))


def _insert_chunks(
    con: duckdb_type.DuckDBPyConnection,
    chunks: list[Chunk],
    embedder: Embedder | None,
    batch_size: int = 256,
) -> None:
    """Insert chunks, computing embeddings in batches when an embedder is provided.

    Args:
        con: Open DuckDB connection.
        chunks: Chunks to insert.
        embedder: Optional embedder; when ``None`` embeddings are stored as ``NULL``.
        batch_size: Chunks per embedding call.  Progress logged after each batch.
    """
    if not chunks:
        return

    row = con.execute("SELECT COALESCE(MAX(id), 0) FROM chunks").fetchone()
    next_id = (row[0] if row else 0) + 1

    embeddings: list[list[float] | None]
    if embedder is not None:
        texts = [c.text for c in chunks]
        embeddings = []
        total_batches = (len(texts) + batch_size - 1) // batch_size
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min(start + batch_size, len(texts))
            batch_vecs = embedder.embed(texts[start:end])
            embeddings.extend(batch_vecs)
            logger.info("build_index: embedded batch %d/%d (%d/%d chunks)", batch_idx + 1, total_batches, end, len(texts))
    else:
        embeddings = [None] * len(chunks)

    rows = [(next_id + i, c.source_path, c.citekey, c.section, c.text, embeddings[i]) for i, c in enumerate(chunks)]
    con.executemany(
        "INSERT INTO chunks (id, source_path, citekey, section, text, embedding) VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )


def update_index(kb_root: Path, embedder: Embedder | None = None) -> int:
    """Incremental update: reprocess only changed pages/txt files.

    Compares the SHA-256 hash of each source file against a stored ``file_hashes``
    meta-table.  Replaces all chunks for changed files; does not touch unchanged ones.

    Args:
        kb_root: Knowledge-base root directory.
        embedder: Embedding provider.

    Returns:
        Number of source files reprocessed.
    """
    con = _open_db(kb_root)
    _ensure_schema(con)

    # Ensure file_hashes table
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS file_hashes (
            source_path VARCHAR PRIMARY KEY,
            hash        VARCHAR NOT NULL
        )
        """
    )

    # Collect current hashes from DB
    stored: dict[str, str] = {row[0]: row[1] for row in con.execute("SELECT source_path, hash FROM file_hashes").fetchall()}

    wiki_dir = kb_root / "wiki"
    txt_dir = kb_root / "raw" / "literature" / "txt"

    candidates: list[Path] = []
    if wiki_dir.is_dir():
        candidates.extend(sorted(wiki_dir.rglob("*.md")))
    if txt_dir.is_dir():
        candidates.extend(sorted(txt_dir.glob("*.txt")))

    reprocessed = 0
    for path in candidates:
        rel = path.relative_to(kb_root).as_posix()
        current_hash = _file_hash(path)
        if stored.get(rel) == current_hash:
            continue

        # Remove existing chunks for this file
        con.execute("DELETE FROM chunks WHERE source_path = ?", [rel])

        # Rechunk
        if path.suffix == ".md":
            chunks = chunk_wiki_page(path, kb_root)
        else:
            stem = path.stem
            citekey = stem[: -len("-suppl")] if stem.endswith("-suppl") else stem
            chunks = chunk_txt(path, citekey, kb_root)

        _insert_chunks(con, chunks, embedder)
        con.execute("INSERT OR REPLACE INTO file_hashes VALUES (?, ?)", [rel, current_hash])
        reprocessed += 1

    if reprocessed:
        _rebuild_fts(con)
        ts = str(int(time.time()))
        con.execute("INSERT OR REPLACE INTO meta VALUES ('last_build', ?)", [ts])

    con.close()
    logger.info("update_index: %d files reprocessed", reprocessed)
    return reprocessed


def index_status(kb_root: Path) -> dict[str, object]:
    """Return counts and metadata about the current corpus index.

    Args:
        kb_root: Knowledge-base root directory.

    Returns:
        Dict with keys: ``db_path``, ``exists``, ``chunk_count``, ``wiki_chunk_count``,
        ``txt_chunk_count``, ``embed_model``, ``embed_dim``, ``last_build``.
    """
    db_file = _db_path(kb_root)
    if not db_file.exists():
        return {
            "db_path": str(db_file),
            "exists": False,
            "chunk_count": 0,
            "wiki_chunk_count": 0,
            "txt_chunk_count": 0,
            "embed_model": None,
            "embed_dim": None,
            "last_build": None,
        }

    import duckdb

    con = duckdb.connect(str(db_file), read_only=True)
    total = con.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]  # type: ignore[index]
    wiki = con.execute("SELECT COUNT(*) FROM chunks WHERE citekey IS NULL").fetchone()[0]  # type: ignore[index]
    txt = con.execute("SELECT COUNT(*) FROM chunks WHERE citekey IS NOT NULL").fetchone()[0]  # type: ignore[index]

    meta_rows = con.execute("SELECT key, value FROM meta").fetchall()
    meta = {r[0]: r[1] for r in meta_rows}
    con.close()

    return {
        "db_path": str(db_file),
        "exists": True,
        "chunk_count": total,
        "wiki_chunk_count": wiki,
        "txt_chunk_count": txt,
        "embed_model": meta.get("embed_model"),
        "embed_dim": meta.get("embed_dim"),
        "last_build": meta.get("last_build"),
    }
