# Request Flow

This is a live document — update it whenever the actual flow changes, rather
than letting it drift from the code.

## Current flow (Phase 2: RAG only)

Example: "Why was checkout slow?"

1. Client calls `GET /search?q=why+was+checkout+slow&limit=5`.
2. `app/api/knowledge.py::search` gets an `EmbeddingClient` and `KnowledgeStore`
   via `app/services/rag_service.py`'s factory functions.
3. `EmbeddingClient.embed_query` calls Gemini's `gemini-embedding-001` with
   `task_type="retrieval_query"` and `output_dimensionality=768`, returning a
   768-dim vector.
4. `KnowledgeStore.search` queries Qdrant's `engineering_knowledge` collection
   for the nearest chunks by cosine similarity.
5. Each result carries its `content`, `section`, `project`, `type`, `source`,
   and similarity `score` — the citation is the `source` field, e.g.
   `incidents/checkout-api-latency.md`.
6. The API returns `{"query": ..., "results": [...]}` directly — there is no
   LLM synthesis step yet. Phase 5 adds the Planner/Router/Synthesizer that
   turns these raw results into a narrative answer with inline citations.

Verified end-to-end against the sample corpus: querying "why was checkout
slow" returns `incidents/checkout-api-latency.md` as the top result (score
~0.76), followed by related `architecture/checkout-service.md` sections.

## What's not here yet

No planning, no tool calls, no permission checks, no answer synthesis, no
groundedness validation — this phase proves retrieval works end-to-end.
Phases 3–5 add the rest of the pipeline shown in `architecture.md`'s system
diagram.
