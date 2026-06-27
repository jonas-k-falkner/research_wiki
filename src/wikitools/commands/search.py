"""Hybrid search over the DuckDB corpus index: lexical (FTS/BM25), semantic, or RRF-fused."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import duckdb as duckdb_type

logger = logging.getLogger(__name__)

_RRF_K = 60
_DEFAULT_K = 10


@dataclass(frozen=True)
class Hit:
    """One search result.

    Attributes:
        source_path: Relative path from kb_root to the originating file.
        citekey: Zotero citekey for literature hits; ``None`` for wiki pages.
        section: Section or chunk label within the file.
        score: Final relevance score (higher = more relevant).
        snippet: Short text excerpt from the chunk.
    """

    source_path: str
    citekey: str | None
    section: str
    score: float
    snippet: str


def _snippet(text: str, max_len: int = 200) -> str:
    """Return a short excerpt of the text, trimmed at a word boundary.

    Args:
        text: Full chunk text.
        max_len: Maximum snippet length in characters.

    Returns:
        Excerpt ending with ``"…"`` when truncated.
    """
    t = text.strip().replace("\n", " ")
    if len(t) <= max_len:
        return t
    cut = t[:max_len].rsplit(" ", 1)[0]
    return f"{cut}…"


def _rrf_fuse(lexical_rows: list[tuple], semantic_rows: list[tuple], k_rrf: int = _RRF_K) -> list[tuple[str, str | None, str, float, str]]:
    """Fuse two ranked lists using Reciprocal Rank Fusion.

    Both row lists share schema ``(source_path, citekey, section, text)``.
    Tie-break is by ``(source_path, section)`` for determinism.

    Args:
        lexical_rows: Rows from the lexical (BM25) query, in rank order.
        semantic_rows: Rows from the semantic (cosine) query, in rank order.
        k_rrf: RRF constant (default 60).

    Returns:
        List of ``(source_path, citekey, section, score, text)`` sorted by descending RRF score.
    """
    scores: dict[tuple[str, str], float] = {}
    texts: dict[tuple[str, str], tuple[str, str | None, str]] = {}

    for rank, row in enumerate(lexical_rows, start=1):
        key = (row[0], row[2])  # (source_path, section)
        scores[key] = scores.get(key, 0.0) + 1.0 / (k_rrf + rank)
        texts[key] = (row[0], row[1], row[3])  # (source_path, citekey, text)

    for rank, row in enumerate(semantic_rows, start=1):
        key = (row[0], row[2])
        scores[key] = scores.get(key, 0.0) + 1.0 / (k_rrf + rank)
        texts[key] = (row[0], row[1], row[3])

    fused = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    result: list[tuple[str, str | None, str, float, str]] = []
    for (sp, section), score in fused:
        sp_, citekey, text = texts[(sp, section)]
        result.append((sp_, citekey, section, score, text))
    return result


def search(
    query: str,
    kb_root: Path,
    *,
    k: int = _DEFAULT_K,
    mode: str = "hybrid",
    scope: str | None = None,
    project: str | None = None,
    type_: str | None = None,
) -> list[Hit]:
    """Search the corpus index.

    Args:
        query: Free-text query string.
        kb_root: Knowledge-base root directory.
        k: Maximum number of results to return.
        mode: One of ``"lexical"``, ``"semantic"``, or ``"hybrid"``.
        scope: Optional filter: ``"wiki"`` (no citekey), ``"literature"`` (has citekey),
               or ``None`` (all).
        project: Unused filter placeholder; reserved for future frontmatter filtering.
        type_: Unused filter placeholder; reserved for future frontmatter filtering.

    Returns:
        Up to ``k`` ``Hit`` objects sorted by descending relevance.

    Raises:
        FileNotFoundError: If the corpus DuckDB does not exist.
        ValueError: If ``mode`` is not one of the accepted values.
    """
    from wikitools.commands.index import _EMBED_DIM, _db_path

    if mode not in ("lexical", "semantic", "hybrid"):
        raise ValueError(f"Unknown search mode: {mode!r}. Choose lexical, semantic, or hybrid.")

    db_file = _db_path(kb_root)
    if not db_file.exists():
        raise FileNotFoundError(f"Corpus index not found at {db_file}. Run `wiki index build` first.")

    import duckdb

    con = duckdb.connect(str(db_file), read_only=True)
    con.execute("LOAD fts")

    scope_clause = ""
    if scope == "wiki":
        scope_clause = " AND citekey IS NULL"
    elif scope == "literature":
        scope_clause = " AND citekey IS NOT NULL"

    over_k = k * 4  # fetch more for RRF fusion, then trim to k

    lexical_rows: list[tuple] = []
    semantic_rows: list[tuple] = []

    if mode in ("lexical", "hybrid"):
        lexical_rows = _run_lexical(con, query, over_k, scope_clause)

    if mode in ("semantic", "hybrid"):
        semantic_rows = _run_semantic(con, query, over_k, scope_clause, _EMBED_DIM)

    con.close()

    if mode == "lexical":
        hits = [Hit(source_path=r[0], citekey=r[1], section=r[2], score=r[4], snippet=_snippet(r[3])) for r in lexical_rows[:k]]
    elif mode == "semantic":
        hits = [Hit(source_path=r[0], citekey=r[1], section=r[2], score=r[4], snippet=_snippet(r[3])) for r in semantic_rows[:k]]
    else:
        fused = _rrf_fuse(lexical_rows, semantic_rows)
        hits = [Hit(source_path=sp, citekey=ck, section=sec, score=score, snippet=_snippet(text)) for sp, ck, sec, score, text in fused[:k]]

    return hits


def _run_lexical(con: duckdb_type.DuckDBPyConnection, query: str, k: int, scope_clause: str) -> list[tuple]:
    """Run a BM25 FTS query.

    Args:
        con: Open DuckDB connection with FTS loaded.
        query: Free-text query string.
        k: Maximum rows to return.
        scope_clause: Extra SQL WHERE fragment (starts with ``" AND "`` or is empty).

    Returns:
        List of ``(source_path, citekey, section, text, score)`` tuples.
    """
    try:
        sql = f"""
            SELECT source_path, citekey, section, text, score
            FROM (
                SELECT c.source_path, c.citekey, c.section, c.text,
                       fts_main_chunks.match_bm25(c.id, ?) AS score
                FROM chunks c
            ) sub
            WHERE score IS NOT NULL{scope_clause}
            ORDER BY score DESC
            LIMIT {k}
        """
        rows = con.execute(sql, [query]).fetchall()
        return list(rows)
    except Exception as exc:
        logger.warning("lexical search failed: %s", exc)
        return []


def _run_semantic(
    con: duckdb_type.DuckDBPyConnection,
    query: str,
    k: int,
    scope_clause: str,
    embed_dim: int,
) -> list[tuple]:
    """Run a cosine-similarity semantic search.

    Requires chunks to have non-NULL embeddings.  Falls back to empty list if
    ``[semantic]`` extra is not installed or if no embeddings are stored.

    Args:
        con: Open DuckDB connection.
        query: Free-text query string.
        k: Maximum rows to return.
        scope_clause: Extra SQL WHERE fragment.
        embed_dim: Fixed embedding dimensionality matching the column type.

    Returns:
        List of ``(source_path, citekey, section, text, score)`` tuples.
    """
    try:
        from wikitools.commands.index import LocalEmbedder

        embedder = LocalEmbedder()
        q_vec = embedder.embed([query])[0]
    except Exception as exc:
        logger.warning("semantic search: embedder unavailable (%s)", exc)
        return []

    q_param = q_vec  # list[float]
    try:
        sql = f"""
            SELECT source_path, citekey, section, text,
                   array_cosine_similarity(embedding, $q::FLOAT[{embed_dim}]) AS score
            FROM chunks
            WHERE embedding IS NOT NULL{scope_clause}
            ORDER BY score DESC
            LIMIT {k}
        """
        rows = con.execute(sql, {"q": q_param}).fetchall()
        return list(rows)
    except Exception as exc:
        logger.warning("semantic search failed: %s", exc)
        return []
