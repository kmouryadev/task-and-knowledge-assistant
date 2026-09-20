from pathlib import Path

from fastapi import APIRouter, Depends

from app.core.settings import get_settings
from app.rag.embeddings import EmbeddingClient
from app.rag.ingestion import IngestionReport, ingest_knowledge_base
from app.rag.qdrant import KnowledgeStore
from app.services.rag_service import get_embedding_client, get_knowledge_store

router = APIRouter()

_DEFAULT_KNOWLEDGE_DIR = Path(__file__).resolve().parents[3] / "knowledge"


def _resolve_knowledge_dir() -> Path:
    configured = get_settings().knowledge_dir
    return Path(configured) if configured else _DEFAULT_KNOWLEDGE_DIR


@router.post("/ingest", response_model=IngestionReport)
def ingest(
    store: KnowledgeStore = Depends(get_knowledge_store),
    embedder: EmbeddingClient = Depends(get_embedding_client),
) -> IngestionReport:
    return ingest_knowledge_base(_resolve_knowledge_dir(), store=store, embedder=embedder)


@router.get("/search")
def search(
    q: str,
    limit: int = 5,
    store: KnowledgeStore = Depends(get_knowledge_store),
    embedder: EmbeddingClient = Depends(get_embedding_client),
) -> dict:
    query_vector = embedder.embed_query(q)
    results = store.search(query_vector=query_vector, limit=limit)
    return {"query": q, "results": [r.model_dump() for r in results]}
