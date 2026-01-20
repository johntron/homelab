# ADR 0001: DNS Approach

## Status
Proposed

## Context
Tier 1 requires stable names and reservations. DNS must work during outages and not depend on Tier 2 experiments.

## Decision
Adopt a simple, locally managed DNS strategy with static reservations for Tier 1.
Document the chosen implementation once selected (router DNS, dedicated resolver, or TrueNAS-hosted DNS).

## Consequences
- Tier 1 hostnames are stable and documented.
- Tier 2 can evolve without impacting Tier 1 name resolution.
- Requires a clear recovery path when DNS fails.
