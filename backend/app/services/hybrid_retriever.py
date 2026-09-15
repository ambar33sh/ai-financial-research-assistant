import re
from functools import lru_cache

from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from app.config import get_settings
from app.schemas import SearchResult
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


@lru_cache
def get_reranker() -> CrossEncoder:
    return CrossEncoder(get_settings().reranker_model)


class HybridRetriever:
    """Retrieve with vector similarity, candidate-set BM25, then cross-encoder reranking."""

    def __init__(self) -> None:
        self.store = VectorStore()
        self.embeddings = EmbeddingService()

    def retrieve(self, query: str, top_k: int = 5, company: str | None = None, fiscal_year: int | None = None) -> list[SearchResult]:
        candidates = self.store.search(query, max(top_k * 4, 10), company, fiscal_year)
        if not candidates:
            return []

        corpus = [tokenize(item.text) for item in candidates]
        bm25 = BM25Okapi(corpus)
        raw_scores = bm25.get_scores(tokenize(query))
        minimum = float(min(raw_scores))
        maximum = float(max(raw_scores))
        if maximum > minimum:
            lexical_scores = [(float(score) - minimum) / (maximum - minimum) for score in raw_scores]
        else:
            lexical_scores = [0.0] * len(raw_scores)

        for item, lexical in zip(candidates, lexical_scores):
            item.score = 0.7 * float(item.score) + 0.3 * lexical

        candidates.sort(key=lambda item: item.score, reverse=True)
        shortlist = candidates[: max(top_k * 2, 8)]
        try:
            rerank_scores = get_reranker().predict([(query, item.text) for item in shortlist])
            ranked = sorted(zip(shortlist, rerank_scores), key=lambda pair: float(pair[1]), reverse=True)
            return [item for item, _ in ranked[:top_k]]
        except Exception:
            return shortlist[:top_k]
