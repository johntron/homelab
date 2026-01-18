# 00_requirements.md

## intent
Rebuild the homelab to be low power, reliable, and remotely manageable (attic), with:
- **Tier 1 (boring/stable):** services used by the whole family
- **Tier 2 (experimental):** everything else

## goals
- Low power (minimize idle draw and heat in attic)
- Resilience / fast recovery for Tier 1
- Self-hosting for core services
- Reliable operations (predictable upgrades, recoverable failures)
- Security (lowest priority): improve isolation and transport security (VLANs/TLS) without turning this into a second job

## constraints
- Limited maintenance time
- Remotely managed in attic (physical access is expensive)
- UPS available
- Must recover cleanly after power events (no “kick the cluster” rituals)

## risk tolerance
- Tier 1 must be stable and self-healing after outages
- Tier 2 can break; failures must not affect Tier 1

## priorities (ranked)
1. Simplicity
2. Usability
3. Reliability (including clean recovery after power loss)
4. Low power
5. HA
6. Experimentation capability
7. Security

## non-negotiable operational requirements
- Stable reachability: stop hunting DHCP leases (names/reservations)
- Observability + phone alerts for Tier 1: know when something is down
- Backup + restore is real: backups + periodic restore test
- Documented “how to recover” runbook for Tier 1

## tier 1
Architecture:
- mini-ITX TrueNAS
- Pi4 Home Assistant
- ProDesk docker-compose for core services and Frigate

 Services (must alert to phone)
- Home Assistant
- Frigate
- NAS / backups

## known pain points to eliminate
- k8s nodes needing manual intervention after power loss
- needing to check DHCP leases to find IPs
- no observability/alerts; discovering outages late
- weak NAS setup
- no VLAN isolation and little/no internal TLS
- Kubernetes didn't distribute load across nodes

## open decisions (tracked)
- DNS approach for internal names (table for now; decide later)
- VLAN scope (2 VLAN vs 4 VLAN start)
- Tier 1 platform choice (k8s vs “boring VMs/containers”)
- Storage design for NAS + Frigate recordings
- Remote access posture (Cloudflare Access vs VPN-only vs hybrid)

## acceptance criteria (done means…)
- After pulling power (simulated outage), Tier 1 returns to healthy without manual intervention
- Phone gets alerted within X minutes if HA/Frigate/NAS are down
- All Tier 1 services reachable via stable names (no IP scavenger hunt)
- Backups run automatically; restore test succeeds on a schedule
