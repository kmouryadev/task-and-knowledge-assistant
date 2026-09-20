# 0001: Local Qdrant over hosted Qdrant Cloud

**Context:** Vector search needs somewhere to store and query embeddings. Qdrant
offers a hosted free tier, but hosted free tiers introduce an external dependency
(account setup, potential cold starts/stalling, quota resets) that isn't needed for a
single-user portfolio demo, and a prior attempt at using the hosted tier for a
different project stalled.

**Decision:** Run Qdrant locally via Docker (`qdrant/qdrant` image), with its own
volume for persistence in local dev. For the deployed demo, re-run ingestion on
container start if the hosting platform's disk isn't persistent, rather than depending
on hosted infrastructure.

**Consequence:** Zero billing risk and no external account dependency. The trade-off
is the deployed demo must either use a host with a persistent volume or re-ingest a
small, fast-to-rebuild corpus on boot — both zero-cost options, handled in the
Deployment phase. Local dev also gets a tangible artifact to demo: the Qdrant
dashboard at `localhost:6333/dashboard`.
