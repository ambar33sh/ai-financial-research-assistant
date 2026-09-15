from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import get_settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(get_settings().embedding_model)


class EmbeddingService:
    def encode(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = get_embedding_model().encode(texts, normalize_embeddings=True)
        return vectors.tolist()

    def encode_query(self, query: str) -> list[float]:
        return self.encode([query])[0]
