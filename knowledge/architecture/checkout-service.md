# Checkout Service Architecture

## Overview

The checkout service is a FastAPI application sitting behind the BFF layer. It
owns cart finalization, payment intent creation, and order confirmation. It talks
to the payments provider over REST and publishes an `order.created` event to
Kafka on success.

## Data flow

A checkout request arrives at the BFF, which forwards it to the checkout service
with a validated cart snapshot. The service creates a payment intent, waits for
a synchronous authorization response (typically 200-400ms), and on success writes
the order row and publishes the event. Downstream consumers (inventory, email,
analytics) react to `order.created` asynchronously.

## Known constraints

The synchronous payment authorization call is the dominant source of checkout
latency. It cannot be made asynchronous because the user needs an immediate
success/failure result. Caching is not applicable since every authorization is
a distinct financial transaction.
