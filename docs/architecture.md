# Architecture

## System diagram

```
React -- SSE/REST -- FastAPI
                |
    Security Layer (validation, rate limiting, injection guard)
                |
            LangGraph
                |
             Planner
                |
   Router (validates the proposed tool against an allowlist)
   +-----------+-----------+
   |           |           |
   v           v           v
Retriever   GitHub      Web Research
   |        Tool        Tool (optional)
   v          |             |
Qdrant    +-----+-----+
                |
                v
   Policy Engine (permission check, destructive-op confirmation)
                |
                v
           Synthesizer
                |
                v
Output Validator (schema + citation + grounding check)
                |
                v
           Final Answer
```

## Nodes

- **Planner** — decides the next step given the conversation and prior tool results. (Built in Phase 5.)
- **Router** — validates the planner's proposed tool call against a fixed allowlist before anything executes; picks knowledge search, GitHub, web, or a direct answer. (Phase 5, allowlist from Phase 4.)
- **Retriever** — queries Qdrant for relevant chunks of `knowledge/`. (Phase 2.)
- **Tools** (GitHub, Work Items, Web) — typed, explicitly registered functions; no arbitrary execution. (Phase 3.)
- **Policy Engine** — checks the proposed tool's permission level (READ/WRITE/DESTRUCTIVE) and requires user confirmation for DESTRUCTIVE ops. (Phase 4.)
- **Synthesizer** — turns tool/retrieval results into a draft answer with citations. (Phase 5.)
- **Output Validator** — schema-, citation-, and groundedness-checks the draft before it ships. (Phase 5.)

## Why the LLM never executes a tool directly

The LLM only ever *proposes* a tool call (name + arguments) as structured output. The
application — never the model — looks that proposal up in a fixed tool registry,
checks it against the permission policy, and only then executes it. This means a
successful prompt injection can, at worst, get the model to *propose* an unauthorized
or malformed call; it can never make the app execute something outside the registry,
skip a permission check, or run arbitrary code. This boundary is what Phase 4's
security layer enforces and Phase 4's security tests verify.

## Current status

Phase 1 (Foundation) complete: FastAPI app, settings, structured logging, typed
errors, `/health`, Docker, CI. No RAG, tools, agent, or frontend yet — those arrive in
Phases 2–6.
