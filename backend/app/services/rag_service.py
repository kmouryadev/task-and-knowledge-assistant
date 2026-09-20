from functools import lru_cache

from qdrant_client import QdrantClient

from app.core.settings import get_settings
from app.rag.embeddings import EmbeddingClient
from app.rag.qdrant import KnowledgeStore


@lru_cache
def get_embedding_client() -> EmbeddingClient:
    settings = get_settings()
    return EmbeddingClient(api_key=settings.gemini_api_key)


@lru_cache
def get_knowledge_store() -> KnowledgeStore:
    settings = get_settings()
    client = QdrantClient(url=settings.qdrant_url)
    return KnowledgeStore(
        client=client,
        collection_name=settings.qdrant_collection,
        embedding_dimension=settings.embedding_dimension,
    )
