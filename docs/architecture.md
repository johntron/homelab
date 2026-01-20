# Homelab Architecture

_Last updated: 2026-01-05 (America/Chicago)_

## Intent
Rebuild the homelab to be low power, reliable, and remotely manageable (attic), using a simple two-tier model:
- Tier 1 (boring/stable): household-critical services
- Tier 2 (experimental): everything else

## Priorities (ranked)
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
- Tier 1 runbook: documented recovery steps

## Current stance (resolved decisions)
- VLAN scope: start with 2 VLANs
- Tier 1 platform:
  - TrueNAS on ProDesk (bare metal)
  - Home Assistant on Pi 4 w/ PoE (migrated; running)
  - Core services on the same ProDesk via docker-compose
  - Frigate on Jetson Nano 4GB with Pi PoE hat
- Storage design: TrueNAS dataset/share for Frigate recordings
- Remote access: Cloudflare (for now)
- Tier 2 direction: leaning k3s, not committed

## Tier 1 services (must-work)

### Home Assistant (HA)
- Runs on: Pi 4 (PoE) + Aeotec Z-Wave USB
- Role: home automation control plane
- Interfaces: web UI + mobile app
- Hard dependencies: LAN, Z-Wave radio, DNS/reservations

### TrueNAS
- Runs on: ProDesk (bare metal)
- Role: NAS + backups target + authoritative persistent data (ZFS)
- Interfaces: TrueNAS UI, SMB/NFS/SSH as needed
- Important datasets/shares:
  - `frigate-recordings` (high churn)
  - `backups` (critical; low churn)

### Frigate
- Runs on: Jetson Nano 4GB with Pi PoE hat
- Role: NVR + object detection
- Storage:
  - Config: local bind mount on ProDesk
  - Recordings: mounted TrueNAS dataset/share
- Hard dependencies: camera network reachability, mounted share reliability/permissions, optional hardware accel

### Tier 1 core services (docker-compose on ProDesk)
Keep this boring and restartable.
- Uptime Kuma (recommended)
- Reverse proxy (only if needed)
- Cloudflare connector/tunnel component (if needed)
- Glue services that do not belong on TrueNAS or HA

## Tier 2 (experimental)
- Compute: mini-ITX + ProDesk #2 + spare Pis (Pi 4 SDR, Pi 5 gear)
- Platform: TBD (leaning k3s)
- Rule: Tier 2 failures must not affect Tier 1

## Hardware inventory (condensed)

### Compute
- 2x HP ProDesk 600 G6 Mini (each has 2x NVMe)
- 1x mini-ITX PC (1x NVMe, 1x empty PCIe slot)
- Raspberry Pi 4 + PoE + Aeotec Z-Wave USB - HA role
- Raspberry Pi 4 + RTL-SDR + antenna - SDR role
- Raspberry Pi 5 PoE (unused)
- Raspberry Pi 5 + NVMe shield (unused)
- PiKVM + 4-port KVM (out-of-band access)

### Network
- AT&T fiber ONT + AT&T router (defines upstream WAN/LAN)
- MikroTik hEX PoE (current core router/DHCP; powers APs)
- MikroTik RB5009UPr-IN-S (in LAN; switching and/or future core)
- 3x MikroTik cAP ac (CAPsMAN-managed)
- 8-port gigabit unmanaged switch
- 4-port passive PoE switch (cameras)

### Cameras / IoT
- 2x Amcrest PoE cameras
- Hue bridge + Hue lights
- Z-Wave devices (switches, shades, etc.)

### Power / physical
- UPS: APC Back-UPS 600 (BE600M1)
- Mini rack + 3D-printed mounts (in progress)
- Attic environment (cooling/conditioning): TBD

## Network topology (now -> next)

### Current (as-is)
- Internet -> ONT -> AT&T router (NAT)
- MikroTik hEX PoE provides DHCP for the LAN and powers APs
- RB5009 acts as an additional switch/router in the LAN (core role evolving)
- Wi-Fi: cAP ac via CAPsMAN
- Cameras on passive PoE switch

### Next (near-term goals)
- Keep it simple: 2 VLANs to start
  - VLAN A: Core / Tier 1
  - VLAN B: IoT / cameras / misc
- Make names/reservations the default way humans reach services

## Naming and network services (minimums)

### Minimum requirements
- DHCP reservations for: routers/switches/APs, cameras, servers, service-hosting Pis
- Stable names for Tier 1:
  - `ha.<tbd>`
  - `frigate.<tbd>`
  - `nas.<tbd>`
  - Optional: `kuma.<tbd>`, `zwave.<tbd>`, `proxy.<tbd>`

### Naming scheme options (choose later)
- A. `*.home.johntron.com` (clean split-horizon + wildcard certs)
- B. `*.johntron.com` (short, but demands careful split-horizon)
- C. `home.arpa` (internal-only, zero conflicts)

### TLS strategy (independent of naming)
- Prefer HTTPS for browser-facing Tier 1 services (usually via reverse proxy)
- Use Let's Encrypt DNS-01 with Cloudflare API (works without exposing ports)
- Wildcard scope depends on naming option (A/B)

## Observability (Tier 1)

### Goals
- Know when Tier 1 is down without guessing
- Alerts go to phone

### Minimum viable stack
- Uptime Kuma
  - HTTP/TCP/ping checks
  - simple dashboard
  - phone notifications (Pushover recommended; alternatives: HA mobile push / Telegram)

### Initial checks
- HA: HTTP(S) check
- Frigate: HTTP(S) check
- NAS:
  - ping
  - TCP check (SMB 445 / NFS 2049 / SSH 22)
  - storage usage high alert (from NAS or via a script/exporter)
- Backup freshness heartbeat:
  - backup job hits a Kuma push endpoint (preferred), or writes a timestamp checked by script

### Notification policy
- P0: HA/Frigate/NAS down -> immediate
- P1: backups stale / disk usage high -> same day
- P2: Tier 2 nodes down -> off by default

### Power outage recovery test
- Quarterly: simulate outage (pull power)
- Pass criteria:
  - Tier 1 returns healthy without manual intervention
  - alerts fire correctly
  - no storage corruption / degraded pools

## Rack layout and operations (attic)

### Principles
- Keep Tier 1 dependencies physically together and boring
- Keep Tier 2 physically and logically separated where possible
- Label both ends of every cable: `device:port -> switch:port`
- Ensure PiKVM remains reachable when everything else is sad

### Rack facts (to fill)
- Rack size/depth/access: TBD
- Environment/cooling strategy: TBD (and monitor temperature)

### Power + UPS
- Decide what rides on UPS at minimum:
  - router/switch/AP
  - Tier 1 compute (Pi + ProDesk #1)
  - TrueNAS
- Decide shutdown posture
