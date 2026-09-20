# 0006: Defer the GitHub tool

**Context:** The build plan's toolset includes a read-only GitHub tool
(search_issues, get_issue, search_repository, get_recent_commits) alongside
Work Items and Web Research, capped at ~4 tools total (including Knowledge
Search from Phase 2). Building all three non-RAG tools in one phase was the
original plan, but Work Items and Web Research alone are enough to prove the
tool pattern (typed functions, permission-level tagging, independent tests)
that Phase 4's registry and Phase 5's Router will consume.

**Decision:** Build Work Items and Web Research in Phase 3; defer the GitHub
tool. It is not dropped — it still fits under the 4-tool cap (Knowledge
Search, Work Items, Web Research, GitHub) — just deferred to whenever it's
next useful, without blocking Phase 4 (security layer) or Phase 5 (agent).

**Consequence:** Phase 5's agent will launch with 3 tools instead of 4. Adding
the GitHub tool later is additive: a new `backend/app/tools/github.py`
following the same pattern as `work_items.py`/`web.py`, plus its own permission
tagging and tests — it doesn't require changes to Phase 3's, Phase 4's, or
Phase 5's other work.
