import json
import os
import sys
from pathlib import Path
from typing import Any

import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "starter"))
from baseline import TfidfIndex

CHUNKS_PATH = ROOT / "starter" / "data" / "converted" / "chunks.json"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STRATEGY = "B"
FILTER_COLUMNS = {"platform", "section"}


def to_pgvector(vector: list[float]) -> str:
    return "[" + ",".join(str(float(x)) for x in vector) + "]"


def load_chunks() -> list[dict[str, Any]]:
    return json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))


def check_filters(filters: dict[str, Any] | None) -> dict[str, Any]:
    filters = filters or {}
    for column in filters:
        if column not in FILTER_COLUMNS:
            raise ValueError(f"cannot filter on {column!r}; allowed: {sorted(FILTER_COLUMNS)}")
    return filters


class DenseRetriever:
    name = "dense"

    def __init__(self, database_url: str | None = None):
        load_dotenv(ROOT / ".env")
        self.url = database_url or os.getenv("DATABASE_URL")
        if not self.url:
            raise SystemExit("Thiếu DATABASE_URL trong .env")
        self.embedder = SentenceTransformer(MODEL_NAME)

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        filters = check_filters(filters)
        qv = to_pgvector(self.embedder.encode(query, normalize_embeddings=True).tolist())
        where, params = ["strategy = %s"], [STRATEGY]
        for column, value in filters.items():
            where.append(f"{column} = %s")
            params.append(value)
        sql = f"""
            SELECT chunk_id, document_id, source, page, section, platform, text,
                   1 - (embedding <=> %s::vector) AS score
            FROM chunks
            WHERE {" AND ".join(where)}
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        with psycopg.connect(self.url) as conn:
            rows = conn.execute(sql, [qv, *params, qv, top_k]).fetchall()
        return [{"id": cid, "source_id": doc, "source": src, "page": page, "text": text,
                 "metadata": {"section": sec, "platform": plat}, "score": float(score), "strategy": self.name}
                for cid, doc, src, page, sec, plat, text, score in rows]


class LexicalRetriever:
    name = "tfidf"

    def __init__(self, chunks: list[dict[str, Any]] | None = None):
        self.chunks = chunks or load_chunks()
        self.index = TfidfIndex(self.chunks)

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        filters = check_filters(filters)
        ranked = self.index.search(query, top_k=len(self.chunks))
        kept = [c for c in ranked if all(c["metadata"].get(k) == v for k, v in filters.items())]
        return [{**c, "strategy": self.name} for c in kept[:top_k]]


class HybridRetriever:
    name = "hybrid"

    def __init__(self, dense: DenseRetriever, lexical: LexicalRetriever, *, candidates: int = 20, k: int = 60):
        self.dense, self.lexical, self.candidates, self.k = dense, lexical, candidates, k

    def search(self, query: str, *, filters: dict[str, Any] | None, top_k: int) -> list[dict[str, Any]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        n = max(self.candidates, top_k)
        scores: dict[str, float] = {}
        chunk_by_id: dict[str, dict[str, Any]] = {}
        for ranking in (self.dense.search(query, filters=filters, top_k=n),
                        self.lexical.search(query, filters=filters, top_k=n)):
            for rank, c in enumerate(ranking, start=1):
                scores[c["id"]] = scores.get(c["id"], 0.0) + 1 / (self.k + rank)
                chunk_by_id.setdefault(c["id"], c)
        best = sorted(scores, key=lambda cid: (-scores[cid], cid))[:top_k]
        return [{**chunk_by_id[cid], "score": scores[cid], "strategy": self.name} for cid in best]


def build(method: str):
    if method == "dense":
        return DenseRetriever()
    if method == "tfidf":
        return LexicalRetriever()
    if method == "hybrid":
        return HybridRetriever(DenseRetriever(), LexicalRetriever())
    raise ValueError(f"unknown method {method!r}")


if __name__ == "__main__":
    for m in ("dense", "tfidf", "hybrid"):
        top = build(m).search("How do I change page margins in Word?", filters={"platform": "microsoft_word"}, top_k=3)
        print(m, [(c["id"], round(c["score"], 3)) for c in top])
