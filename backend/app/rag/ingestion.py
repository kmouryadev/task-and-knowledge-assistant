from pathlib import Path

from pydantic import BaseModel

from app.rag.chunking import chunk_markdown
from app.rag.embeddings import EmbeddingClient
from app.rag.qdrant import KnowledgeStore


class IngestionReport(BaseModel):
    files_processed: int
    chunks_indexed: int


def ingest_knowledge_base(
    knowledge_dir: Path, store: KnowledgeStore, embedder: EmbeddingClient
) -> IngestionReport:
    store.ensure_collection()

    files_processed = 0
    chunks_indexed = 0

    for type_dir in sorted(p for p in knowledge_dir.iterdir() if p.is_dir()):
        doc_type = type_dir.name
        for md_file in sorted(type_dir.glob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            source = str(md_file.relative_to(knowledge_dir)).replace("\\", "/")
            chunks = chunk_markdown(text, source=source)
            if not chunks:
                continue

            vectors = embedder.embed_texts([chunk.content for chunk in chunks])
            metadata = {"project": md_file.stem, "type": doc_type, "source": source}
            store.upsert_chunks(chunks, vectors, metadata)

            files_processed += 1
            chunks_indexed += len(chunks)

    return IngestionReport(files_processed=files_processed, chunks_indexed=chunks_indexed)
