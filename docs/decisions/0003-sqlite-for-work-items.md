# 0003: SQLite for work items

**Context:** The Work Items tool needs CRUD storage (create/read/update/delete
tasks) that supports READ/WRITE/DESTRUCTIVE permission levels. This is a
single-user portfolio demo, not a multi-tenant production service.

**Decision:** Use SQLite as the work-items store — a single file, zero infrastructure,
zero billing risk, trivially resettable between demo runs.

**Consequence:** No connection pooling, migrations tooling, or hosted database is
needed. The trade-off (no concurrent-writer safety, no horizontal scaling) is
irrelevant at this scope and explicitly out of scope: Kubernetes, a Redis cluster,
Kafka, or a microservices split would be infra overkill for a single-user portfolio
demo.
