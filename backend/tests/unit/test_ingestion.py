from unittest.mock import MagicMock

from app.rag.ingestion import ingest_knowledge_base


def test_ingest_knowledge_base_processes_all_markdown_files(tmp_path):
    arch_dir = tmp_path / "architecture"
    arch_dir.mkdir()
    (arch_dir / "checkout-service.md").write_text(
        "# Checkout Service\n\n## Overview\n\nSome architecture content here."
    )

    incidents_dir = tmp_path / "incidents"
    incidents_dir.mkdir()
    (incidents_dir / "latency.md").write_text("# Latency Incident\n\n## Summary\n\nWhat happened.")

    embedder = MagicMock()
    embedder.embed_texts.return_value = [[0.1, 0.2, 0.3]]

    store = MagicMock()

    report = ingest_knowledge_base(tmp_path, store=store, embedder=embedder)

    assert report.files_processed == 2
    assert report.chunks_indexed >= 2
    store.ensure_collection.assert_called_once()
    assert store.upsert_chunks.call_count == 2

    call_metadatas = [call.args[2] for call in store.upsert_chunks.call_args_list]
    types = {m["type"] for m in call_metadatas}
    assert types == {"architecture", "incidents"}


def test_ingest_knowledge_base_skips_non_markdown_files(tmp_path):
    arch_dir = tmp_path / "architecture"
    arch_dir.mkdir()
    (arch_dir / "notes.txt").write_text("not markdown")
    (arch_dir / ".gitkeep").write_text("")

    embedder = MagicMock()
    store = MagicMock()

    report = ingest_knowledge_base(tmp_path, store=store, embedder=embedder)

    assert report.files_processed == 0
    assert report.chunks_indexed == 0
    store.upsert_chunks.assert_not_called()
