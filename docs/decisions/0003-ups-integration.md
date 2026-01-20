# ADR 0003: UPS Integration

## Status
Proposed

## Context
Attic deployment needs safe shutdown and alerting during power events. Tier 1 must remain stable and recoverable.

## Decision
Integrate UPS monitoring and safe-shutdown automation for Tier 1 hosts.
Select the implementation (NUT or vendor tools) after confirming hardware compatibility.

## Consequences
- Tier 1 shutdown order is deterministic.
- Alerts on power events and battery health are required.
- Adds a dependency to maintain and test periodically.
