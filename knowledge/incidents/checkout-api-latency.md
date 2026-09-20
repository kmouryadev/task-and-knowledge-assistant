# Incident: Checkout API Latency Spike

## Summary

Checkout API p95 latency rose from ~350ms to over 2s for roughly 40 minutes.
Root cause was a connection pool exhaustion against the payments provider after
a deploy reduced the pool size default.

## Timeline

Alert fired when p95 crossed 1.5s. On-call confirmed elevated latency was
isolated to the checkout service's outbound calls to the payments provider, not
the payments provider itself (their status page showed no incident). Rolling
back the most recent checkout-service deploy restored the previous pool size and
latency returned to baseline within two minutes of rollback completing.

## Follow-ups

Pool size is now set explicitly in config rather than relying on the client
library's default, and a dashboard alert was added for outbound connection pool
utilization specifically, not just latency.
