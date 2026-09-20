# 0007: Web tool is search-only — no arbitrary URL fetching

**Context:** The guardrails section calls for "SSRF protection (for the web
tool)": validate protocol, resolve DNS, block private/internal IP ranges,
validate redirects, cap timeout and response size. Those protections matter
when a tool accepts an LLM-supplied URL and fetches it — the classic SSRF
vector, where a prompt injection could aim the tool at an internal service
(e.g. a cloud metadata endpoint).

**Decision:** The Phase 3 web tool is `search_web(query: str)` only. It always
calls one fixed, hardcoded host (`api.duckduckgo.com`) with the query as a
parameter — the LLM never supplies a URL for the tool to fetch. There is
therefore no SSRF surface in this tool: the destination host is never
attacker-influenced, regardless of what the query string contains.

**Consequence:** Phase 4's SSRF module (`backend/app/security/ssrf.py`) is
built as reusable infrastructure per the original plan, but this tool doesn't
strictly require it to be safe. If a future `fetch_url(url)` capability is
added (fetching full page content by URL, which a search-snippet-only tool
can't provide), that capability is exactly when Phase 4's SSRF protections
become load-bearing rather than precautionary — it should be gated behind
them, not added ad hoc.

## Known limitation (found during Phase 3 verification)

DuckDuckGo's Instant Answer API — the free, no-key endpoint this tool calls —
is built for named-entity lookups (e.g. "FastAPI", "Python"), not general
web search. Live verification showed it returns empty results for
research-style queries like "checkout latency" or "python asyncio", while
well-known-entity queries return useful abstracts and related topics. This
was a known trade-off accepted to stay on a free, no-key API matching the
build plan's "DuckDuckGo, no key" requirement — a key-based alternative
(e.g. Tavily, Brave Search) would return better results for general research
questions but is a new dependency not in the original plan, so it wasn't
added without asking first. If the agent's Phase 5 usage shows this
limitation matters in practice, revisit then.
