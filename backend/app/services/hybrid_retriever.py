from functools import lru_cache

from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

from app.config import get_settings
from app.schemas import DocumentChunk, SearchResult
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


@lru_cache
def get_reranker() -> CrossEncoder:
    return CrossEncoder(get_settings().reranker_model)


class HybridRetriever:
    """Combine vector candidates with lexical matching and a cross-encoder reranker.

    Qdrant remains the primary candidate source. The lexical stage operates on the
    retrieved candidate set so the service remains simple and scalable for the
    internship-sized corpus.
    """

    def __init__(self) -> None:
        self.store = VectorStore()
        self.embeddings = EmbeddingService()

    def retrieve(self, query: str, top_k: int = 5, company: str | None = None, fiscal_year: int | None = None) -> list[SearchResult]:
        candidates = self.store.search(query, max(top_k * 4, 10), company, fiscal_year)
        if not candidates:
            return []

        query_terms = set(query.lower().split())
        lexical_scores = []
        for item in candidates:
            terms = item.text.lower().split()
            overlap = len(query_terms.intersection(terms)) / max(len(query_terms), 1)
            lexical_scores.append(overlap)

        for item, lexical in zip(candidates, lexical_scores):
            item.score = 0.7 * item.score + 0.3 * lexical

        candidates.sort(key=lambda x: x.score, reverse=True)
        shortlist = candidates[: max(top_k * 2, 8)]
        try:
            rerank_scores = get_reranker().predict([(query, item.text) for item in shortlist])
            ranked = sorted(zip(shortlist, rerank_scores), key=lambda pair: float(pair[1]), reverse=True)
            return [item for item, _ in ranked[:top_k]]
        except Exception:
            return shortlist[:top_k]
