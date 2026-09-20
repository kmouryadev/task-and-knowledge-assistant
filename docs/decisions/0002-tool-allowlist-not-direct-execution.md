# 0002: Tool allowlist + validation, never direct LLM execution

**Context:** Agentic systems that let a model directly execute whatever it outputs are
a well-known security liability — a prompt injection (direct or indirect, e.g. via a
retrieved note or a GitHub issue body) can otherwise translate straight into an
action.

**Decision:** The LLM only ever proposes a tool call (name + typed arguments) as
structured output. The application looks that proposal up in a fixed tool registry,
checks it against a permission policy (READ/WRITE/DESTRUCTIVE, with DESTRUCTIVE
requiring explicit user confirmation), and only then executes it. No shell, subprocess,
arbitrary Python, or arbitrary SQL tools exist in the registry at all.

**Consequence:** A successful injection can at worst get the model to propose an
unauthorized or malformed call — it can never cause the app to run something outside
the registry or skip a permission check. This is the security differentiator the whole
project is designed around, and it's enforced in `backend/app/security/` (Phase 4) and
covered by `backend/tests/security/` before the agent is ever wired up.
