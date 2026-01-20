# Tier 1 Recovery Runbook

This runbook targets Tier 1 services (HA, TrueNAS, Frigate, core services host).
Keep steps boring, reversible, and documented.

## Power-loss recovery
1. Verify UPS status and restore power to network core (switch/router).
2. Bring up TrueNAS first; confirm pools are healthy.
3. Bring up core services host; verify docker-compose stack health.
4. Bring up Home Assistant and Frigate; verify integrations and storage mounts.
5. Confirm monitoring/alerts are green (phone alerts working).

## Degraded storage (TrueNAS or dataset issues)
1. Put Tier 1 into read-only mode where possible.
2. Confirm pool status and recent scrub results on TrueNAS.
3. Detach non-critical workloads from Tier 1 storage.
4. Restore from known-good backups if integrity is compromised.
5. Document incident and update recovery notes.

## Lost DNS / name resolution
1. Confirm DHCP reservations or static mappings still exist.
2. Fall back to known IPs for Tier 1 hosts (use inventory file).
3. Restore local DNS service or router-based DNS.
4. Validate that stable names resolve (Tier 1 first, then Tier 2).

## Frigate cannot write recordings
1. Confirm TrueNAS dataset/share is mounted and reachable.
2. Verify permissions/ownership for the Frigate recording path.
3. Check remaining disk space and dataset quotas.
4. Restart Frigate only after storage is verified.
5. If storage is degraded, redirect recordings to temporary local storage and document.
