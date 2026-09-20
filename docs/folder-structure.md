# Folder Structure

```
task-and-knowledge-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (health, chat, etc.)
│   │   ├── agent/        # LangGraph graph, state, planner, router, retriever, synthesizer (Phase 5)
│   │   ├── security/     # injection guard, policies, SSRF, redaction, execution limits (Phase 4)
│   │   ├── tools/        # tool registry + typed tool implementations (Phase 3)
│   │   ├── rag/          # ingestion, chunking, embeddings, Qdrant client (Phase 2)
│   │   ├── models/       # shared Pydantic models
│   │   ├── services/     # cross-cutting application services
│   │   ├── core/         # settings, logging, error types (Phase 1)
│   │   └── main.py       # FastAPI app entrypoint
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── security/     # populated from Phase 4 onward
├── frontend/
│   └── src/               # React app (Phase 6)
├── knowledge/              # markdown notes the agent retrieves from (RAG corpus, Phase 2+)
├── evals/                  # agent_cases.json, security_cases.json (Phase 7)
├── docs/                   # documentation for humans — never ingested by the agent
│   └── decisions/          # one ADR per non-obvious choice
├── docker/                 # Dockerfiles
├── docker-compose.yml
├── .github/workflows/      # CI
├── README.md
└── Makefile
```

`knowledge/` is the agent's RAG corpus; `docs/` is documentation about the project
itself for a human reader. Keeping them separate avoids the agent retrieving its own
README as if it were engineering knowledge.
