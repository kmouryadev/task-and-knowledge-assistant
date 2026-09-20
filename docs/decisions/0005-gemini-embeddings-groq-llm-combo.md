# 0005: Gemini for embeddings, Groq for LLM generation

**Context:** The build plan names both Groq and Gemini as acceptable free-tier LLM
providers but doesn't specify an embedding provider. Groq doesn't offer an
embeddings endpoint; a local model (e.g. sentence-transformers) would avoid an
API dependency entirely but adds a ~90MB model download and CPU-bound indexing
cost to every environment that runs ingestion.

**Decision:** Use Gemini's free-tier embeddings endpoint for indexing and
querying `knowledge/`, and reserve Groq for the LLM reasoning calls (Planner,
Synthesizer) added in Phase 5. Both are free-tier APIs with no card on file, so
this keeps a single "zero billing risk" posture across the whole stack while
splitting responsibilities: Gemini for embeddings, Groq for generation.

The model is `models/gemini-embedding-001` (the `text-embedding-004` model
originally planned has since been retired from the API), called with
`output_dimensionality=768` to keep vectors at a fixed size regardless of which
embedding model is used later.

**Consequence:** Phase 2 takes a dependency on a Gemini API key (`GEMINI_API_KEY`
in `.env`, never committed) in addition to Qdrant. The trade-off versus a local
embedding model is an external API call per ingested chunk and per query,
subject to Gemini's free-tier rate limits — acceptable at this corpus size
(a handful of markdown files, re-ingested rarely). If free-tier limits become a
problem during demoing, the embedding provider is isolated behind
`EmbeddingClient` (`backend/app/rag/embeddings.py`) and can be swapped without
touching chunking, storage, or the API layer.
