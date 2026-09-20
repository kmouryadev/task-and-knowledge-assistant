from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.rag.ingestion import IngestionReport
from app.rag.qdrant import SearchResult
from app.services.rag_service import get_embedding_client, get_knowledge_store


def test_ingest_endpoint_returns_report(monkeypatch):
    fake_store = MagicMock()
    fake_embedder = MagicMock()

    app.dependency_overrides[get_knowledge_store] = lambda: fake_store
    app.dependency_overrides[get_embedding_client] = lambda: fake_embedder

    monkeypatch.setattr(
        "app.api.knowledge.ingest_knowledge_base",
        lambda knowledge_dir, store, embedder: IngestionReport(files_processed=4, chunks_indexed=9),
    )

    client = TestClient(app)
    response = client.post("/ingest")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"files_processed": 4, "chunks_indexed": 9}


def test_search_endpoint_returns_cited_results():
    fake_store = MagicMock()
    fake_store.search.return_value = [
        SearchResult(
            content="Checkout API latency incident",
            section="Summary",
            project="checkout-api-latency",
            type="incidents",
            source="incidents/checkout-api-latency.md",
            score=0.87,
        )
    ]
    fake_embedder = MagicMock()
    fake_embedder.embed_query.return_value = [0.1, 0.2, 0.3]

    app.dependency_overrides[get_knowledge_store] = lambda: fake_store
    app.dependency_overrides[get_embedding_client] = lambda: fake_embedder

    client = TestClient(app)
    response = client.get("/search", params={"q": "why was checkout slow", "limit": 5})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "why was checkout slow"
    assert body["results"][0]["source"] == "incidents/checkout-api-latency.md"
    assert body["results"][0]["score"] == 0.87


def test_search_endpoint_requires_query_param():
    client = TestClient(app)
    response = client.get("/search")
    assert response.status_code == 422
