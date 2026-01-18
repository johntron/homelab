# Services

This document is the canonical inventory of “what runs where” in the homelab, split by tiers.

## Current decisions (summary)

- **Tier 1 platform**
  - **TrueNAS** on the **mini-ITX**
  - **Home Assistant** on a **Pi 4 w/ PoE** (migrated; running)
  - **Core services + Frigate** on a **ProDesk** using **docker-compose**
- **Storage**
  - Frigate recordings live on a dedicated **TrueNAS dataset/share**
- **Remote access**
  - **Cloudflare** (for now)
- **Network**
  - Start simple with **2 VLANs** (details in topology doc)
- **Tier 2**
  - Undecided; leaning toward a lightweight k8s distro (**k3s**)

---

## Tier 1 services (must-work)

### TrueNAS
- **Purpose:** NAS, backups target, shared storage for Tier 1 services
- **Runs on:** mini-ITX (bare metal)
- **Storage:** ZFS pools/datasets (authoritative source of persistent data)
- **Interfaces:**
  - SMB/NFS shares (as needed)
  - TrueNAS UI
- **Notes:**
  - Create a dedicated dataset/share for Frigate recordings (and any other high-churn data).
  - UPS integration for TrueNAS is pending.

### Home Assistant (HA)
- **Purpose:** home automation control plane
- **Runs on:** Pi 4 w/ PoE (bare metal install / HAOS-style)
- **Status:** **migrated; running**
- **Interfaces:**
  - Web UI
  - Mobile app
- **Dependencies:**
  - Z-Wave (via attached dongle/controller as applicable)
  - Network + DNS (names TBD)
- **Remote access:**
  - Cloudflare (for now) — exact method documented under “remote access” below

### Frigate
- **Purpose:** NVR + object detection (Tier 1 because it’s a core household service)
- **Runs on:** ProDesk (docker-compose)
- **Storage:**
  - Config: local bind mount on ProDesk
  - Recordings: **TrueNAS dataset/share** mounted to ProDesk
- **Dependencies:**
  - Cameras network reachability
  - Hardware accel (iGPU / Coral / etc.) as configured
  - Reliable mount permissions to the TrueNAS share

### Core services host (docker-compose on ProDesk)
This is the “Tier 1 app box” for anything that should be simple and restartable.

**Planned / expected residents (some may be Tier 1 or Tier 1.5):**
- Reverse proxy (if needed)
- Cloudflare connector/tunnel component (if needed)
- Uptime Kuma
- Any lightweight glue services that don’t belong on TrueNAS or HA

---

## Tier 1 supporting capabilities (not exactly “apps,” but required)

### Remote access (Cloudflare)
- **Decision:** use Cloudflare for now (posture may evolve later)
- **Goals:**
  - Remote access without opening inbound ports broadly
  - Phone-friendly access to Tier 1 UIs
- **Open items:**
  - Final posture: Access vs Tunnel vs hybrid with VPN (captured in open questions)

### UPS integration
- **Decision:** UPS setup is required, but approach is still open
- **Pending work:**
  - Configure UPS connectivity for **mini-ITX TrueNAS** and **ProDesks**
  - Decide: “ride-through only” vs “graceful shutdown” (NUT/apcupsd)

---

## Tier 2 services (nice-to-have / experiments)

### Tier 2 platform
- **Leaning:** k3s (lightweight Kubernetes)
- **Status:** undecided / not started
- **Expected use:**
  - Non-critical apps, experiments, internal tools, long-tail services
  - Anything that benefits from k8s patterns without risking Tier 1 stability

---

## Naming, DNS, and networking (high-level)

- **2 VLANs** to start (exact VLAN definitions and boundaries tracked in topology/network docs).
- Internal DNS and naming scheme are still open decisions:
  - `ha.johntron.com` vs `ha.home.johntron.com` vs `home.arpa` etc.
- For now, services should be reachable via stable IPs / reservations and later mapped to canonical names.

---

## Service checklist (implementation tracking)

Tier 1:
- [ ] TrueNAS installed/configured on mini-ITX
- [ ] TrueNAS datasets/shares created (incl. Frigate recordings)
- [x] HA provisioned on Pi 4 w/ PoE (migrated; running)
- [ ] ProDesk docker host provisioned (OS, updates, restore-on-power)
- [ ] docker-compose stack for core services + Frigate deployed
- [ ] Cloudflare remote access configured for Tier 1 endpoints
- [ ] UPS configured for TrueNAS + ProDesks

Tier 2:
- [ ] Decide Tier 2 platform (k3s vs other)
- [ ] Provision Tier 2 cluster (if chosen)
