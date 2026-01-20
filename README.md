# Homelab rebuild (Ansible)

This repo documents and automates a low-power, reliable, remotely manageable homelab using a simple two-tier model.
For the full planning notes, see `docs/architecture.md`.

## Intent
Rebuild the homelab to be low power, reliable, and remotely manageable (attic), using:
- Tier 1 (boring/stable): household-critical services
- Tier 2 (experimental): everything else

## Priorities
1. Simplicity
2. Usability
3. Reliability (including clean recovery after power loss)
4. Low power
5. High availability
6. Experimentation capability
7. Security (nice-to-have)

## Non-negotiables
- Stable reachability: no hunting DHCP leases (reservations + names)
- Observability + phone alerts for Tier 1
- Backups that actually restore (automated + periodic restore test)
- Tier 1 recovery runbook

## Current stance (resolved decisions)
- VLAN scope: start with 2 VLANs
- Tier 1 platform:
  - TrueNAS on ProDesk (bare metal)
  - Home Assistant on Pi 4 w/ PoE (migrated; running)
  - Core services on the same ProDesk via docker-compose
  - Frigate on Jetson Nano 4GB with Pi PoE hat
- Storage: TrueNAS dataset/share for Frigate recordings
- Remote access: Cloudflare (for now)
- Tier 2 direction: leaning k3s, not committed

## Tier 1 services (must-work)
- Home Assistant
  - Runs on: Pi 4 (PoE) + Aeotec Z-Wave USB
  - Role: home automation control plane
  - Dependencies: LAN, Z-Wave radio, DNS/reservations
- TrueNAS
  - Runs on: ProDesk (bare metal)
  - Role: NAS + backups + authoritative persistent data (ZFS)
  - Key datasets: `frigate-recordings` (high churn), `backups` (critical)
- Frigate
  - Runs on: Jetson Nano 4GB with Pi PoE hat
  - Role: NVR + object detection
  - Storage: local config, recordings on TrueNAS dataset/share
  - Dependencies: camera reachability, share permissions, optional hardware accel
- Core services box (docker-compose on ProDesk)
  - Uptime Kuma (recommended)
  - Reverse proxy (only if needed)
  - Cloudflare connector/tunnel component (if needed)
  - Glue services that do not belong on TrueNAS or HA

## Tier 2 (experimental)
- Compute: mini-ITX + ProDesk #2 + spare Pis (Pi 4 SDR, Pi 5 gear)
- Platform: TBD (leaning k3s)
- Rule: Tier 2 failures must not affect Tier 1

## Network and naming
- Two VLANs to start:
  - VLAN A: Core / Tier 1
  - VLAN B: IoT / cameras / misc
- Stable names and reservations are first-class.
- Naming options under consideration:
  - `*.home.johntron.com`
  - `*.johntron.com`
  - `home.arpa`

## Observability (Tier 1)
- Use Uptime Kuma for HTTP/TCP/ping checks and phone alerts (Pushover recommended).
- Minimum checks: HA, Frigate, NAS (ping + SMB/NFS/SSH), and backup freshness.

## Operations
- Tier 1 recovery runbook: `docs/runbooks/tier1_recovery.md`
- ADRs: `docs/decisions/`

## How to run (Ansible)

From the repo root:

```shell
make lint
make inventory
make check
make apply
make bootstrap
```

Use the example Tier 1 inventory:

```shell
make check INVENTORY=inventories/tier1/hosts.yml
```

Local test recipe:

```shell
# Lint
make lint

# Inventory sanity check (dry-run)
make inventory

# Check mode with diffs
make check

# Targeted tags (example)
make check TAGS=baseline
```

Secrets:
- Do not commit secrets.
- Use ansible-vault with an untracked `ansible/group_vars/all/vault.yml`.
- Provide the vault password via `ANSIBLE_VAULT_PASSWORD_FILE` or `--vault-id`.
