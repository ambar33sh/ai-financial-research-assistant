from uuid import uuid5, NAMESPACE_URL

from qdrant_client import QdrantClient, models

from app.config import get_settings
from app.schemas import DocumentChunk, SearchResult
from app.services.embeddings import EmbeddingService


class VectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        self.collection = settings.qdrant_collection
        self.embeddings = EmbeddingService()

    def ensure_collection(self) -> None:
        if self.client.collection_exists(self.collection):
            return
        size = len(self.embeddings.encode_query("financial report"))
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE),
        )

    def upsert(self, chunks: list[DocumentChunk]) -> int:
        if not chunks:
            return 0
        self.ensure_collection()
        vectors = self.embeddings.encode([chunk.text for chunk in chunks])
        points = []
        for chunk, vector in zip(chunks, vectors):
            point_id = str(uuid5(NAMESPACE_URL, f"{chunk.source_name}:{chunk.chunk_index}:{chunk.page}"))
            points.append(models.PointStruct(
                id=point_id,
                vector=vector,
                payload=chunk.model_dump(),
            ))
        self.client.upsert(collection_name=self.collection, points=points, wait=True)
        return len(points)

    def search(self, query: str, top_k: int = 5, company: str | None = None, fiscal_year: int | None = None) -> list[SearchResult]:
        self.ensure_collection()
        query_vector = self.embeddings.encode_query(query)
        conditions = []
        if company:
            conditions.append(models.FieldCondition(key="company", match=models.MatchValue(value=company)))
        if fiscal_year:
            conditions.append(models.FieldCondition(key="fiscal_year", match=models.MatchValue(value=fiscal_year)))
        query_filter = models.Filter(must=conditions) if conditions else None
        response = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )
        return [SearchResult(
            text=hit.payload["text"],
            score=float(hit.score),
            page=int(hit.payload["page"]),
            source_name=hit.payload["source_name"],
            company=hit.payload["company"],
            fiscal_year=hit.payload.get("fiscal_year"),
            section=hit.payload.get("section"),
        ) for hit in response.points]
