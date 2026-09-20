# Overview

## What this is

A production-style agentic RAG system: an assistant that reasons over private
engineering notes (RAG via Qdrant), calls typed external tools (GitHub, work items,
optional web research) under an explicit authorization policy, and defends against
prompt injection and tool abuse.

## What it demonstrates

| Resume claim | What gets built |
|---|---|
| Autonomously plans & executes multi-step tasks | Planner → Router → tool/retrieval execution loop, capped by execution limits |
| LangGraph reasoning workflow, context-aware decisions | Router picks knowledge search / GitHub / web / direct-answer per step |
| RAG: chunking, embeddings, vector search | Markdown notes chunked, embedded, indexed in local Qdrant with metadata |
| Dynamic tool-calling based on user intent | Knowledge Search, GitHub, Work Items, optional Web Research |
| Structured outputs, validation, fallback guardrails | Pydantic-validated planner/tool/answer schemas, citation checks |
| Full-stack: FastAPI + React | FastAPI over SSE; React split-pane chat + execution trace |
| Security-conscious engineering practice | Tool allowlist, injection defenses, SSRF protection, secret redaction, execution limits, rate limiting, kill switch |

## Running locally

Set `GEMINI_API_KEY` in a local `.env` file at the repo root first (get a free
key from Google AI Studio — never commit this file).

```bash
docker compose up --build
curl -X POST http://localhost:8000/ingest
curl "http://localhost:8000/search?q=why+was+checkout+slow"
```

Backend dev loop without Docker:

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

Tests:

```bash
cd backend
pytest tests -v
```

This section grows as later phases add tools, the agent, and the frontend.
