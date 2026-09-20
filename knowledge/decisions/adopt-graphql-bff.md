# Decision: Adopt GraphQL at the BFF Layer

## Context

Frontend teams were over-fetching from REST endpoints designed around backend
resource boundaries rather than screen requirements, causing unnecessary payload
size and a proliferation of one-off endpoints for slightly different field
combinations.

## Decision

Introduce a GraphQL layer at the BFF, aggregating REST/gRPC calls to backend
services behind a single schema shaped around frontend needs. REST endpoints
remain for service-to-service calls; GraphQL is client-facing only.

## Consequence

Frontend teams get field-level control over what they fetch, reducing
over-fetching. The cost is an added translation layer to maintain and the usual
GraphQL operational concerns (query complexity limits, N+1 resolution) which the
BFF's resolvers need to guard against explicitly.
