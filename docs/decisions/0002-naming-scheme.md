# ADR 0002: Host Naming Scheme

## Status
Proposed

## Context
Stable naming is required for Tier 1 reliability and recovery. Names should encode role and tier without exposing implementation detail.

## Decision
Use short, role-based hostnames with a Tier 1 prefix and a documented inventory mapping.
Example: `core-services`, `nas-truenas`, `frigate`, `homeassistant`.

## Consequences
- Easier recovery and troubleshooting.
- Less churn when hardware changes.
- Inventory remains the source of truth for IP mappings.
