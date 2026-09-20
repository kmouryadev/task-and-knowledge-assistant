# 0004: Cap the toolset at 4 tools

**Context:** Every additional tool the agent can call is both a new capability and a
new attack surface — a new thing that needs a permission level, injection-safe
argument handling, and dedicated security tests.

**Decision:** Cap the toolset at four: Knowledge Search (Qdrant), GitHub (read-only:
search_issues, get_issue, search_repository, get_recent_commits), Work Items (SQLite
CRUD), and an optional Web Research tool (DuckDuckGo, SSRF-protected).

**Consequence:** The project stays demoable and securable end-to-end within the
Oct–Dec timeline. Breadth (more tools) is explicitly traded for depth (more rigorous
guardrails and evals on fewer tools) — matching the plan's stated 70% engineering/
security depth target.
