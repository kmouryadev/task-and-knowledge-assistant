import uuid

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.rag.chunking import Chunk


class SearchResult(BaseModel):
    content: str
    section: str | None
    project: str
    type: str
    source: str
    score: float


class KnowledgeStore:
    def __init__(self, client: QdrantClient, collection_name: str, embedding_dimension: int):
        self._client = client
        self._collection_name = collection_name
        self._embedding_dimension = embedding_dimension

    def ensure_collection(self) -> None:
        if self._client.collection_exists(self._collection_name):
            return
        self._client.create_collection(
            collection_name=self._collection_name,
            vectors_config=VectorParams(size=self._embedding_dimension, distance=Distance.COSINE),
        )

    def upsert_chunks(
        self, chunks: list[Chunk], vectors: list[list[float]], metadata: dict
    ) -> None:
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "content": chunk.content,
                    "section": chunk.section,
                    "chunk_index": chunk.chunk_index,
                    **metadata,
                },
            )
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]
        self._client.upsert(collection_name=self._collection_name, points=points)

    def search(self, query_vector: list[float], limit: int = 5) -> list[SearchResult]:
        hits = self._client.query_points(
            collection_name=self._collection_name, query=query_vector, limit=limit
        ).points
        return [
            SearchResult(
                content=hit.payload["content"],
                section=hit.payload.get("section"),
                project=hit.payload["project"],
                type=hit.payload["type"],
                source=hit.payload["source"],
                score=hit.score,
            )
            for hit in hits
        ]
