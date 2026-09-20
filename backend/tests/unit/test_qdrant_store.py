from qdrant_client import QdrantClient

from app.rag.chunking import Chunk
from app.rag.qdrant import KnowledgeStore


def make_store() -> KnowledgeStore:
    client = QdrantClient(":memory:")
    store = KnowledgeStore(client=client, collection_name="test_collection", embedding_dimension=3)
    store.ensure_collection()
    return store


def test_ensure_collection_is_idempotent():
    store = make_store()
    store.ensure_collection()


def test_upsert_and_search_returns_matching_chunk():
    store = make_store()
    chunks = [
        Chunk(content="Checkout API latency incident", section="Summary", chunk_index=0),
        Chunk(content="Unrelated onboarding notes", section="Summary", chunk_index=0),
    ]
    vectors = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

    store.upsert_chunks(
        chunks[:1],
        vectors[:1],
        {"project": "checkout", "type": "incidents", "source": "incidents/checkout.md"},
    )
    store.upsert_chunks(
        chunks[1:],
        vectors[1:],
        {"project": "onboarding", "type": "projects", "source": "projects/onboarding.md"},
    )

    results = store.search(query_vector=[1.0, 0.0, 0.0], limit=1)

    assert len(results) == 1
    assert results[0].content == "Checkout API latency incident"
    assert results[0].project == "checkout"
    assert results[0].source == "incidents/checkout.md"
    assert results[0].score > 0
