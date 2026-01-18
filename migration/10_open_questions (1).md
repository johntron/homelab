# 10_open_questions.md

A running checklist of open decisions (and what’s already decided *for now*).

## Open decisions
- [ ] DNS approach for internal names
- [ ] Internal naming scheme (ha.johntron.com vs ha.home.johntron.com vs home.arpa)
- [ ] UPS integration (ride-through only vs graceful shutdown via NUT/apcupsd) — setup still pending on mini‑ITX + ProDesks
- [ ] Rack thermal strategy (passive vs active cooling)
- [ ] Alert thresholds (how many minutes before paging phone)
- [ ] Backup/restore test cadence and procedure
- [ ] Tier 2 platform choice (none vs k3s vs VMs/containers) — leaning k3s

## Resolved decisions (current stance)
- [x] VLAN scope — start with 2 VLANs
- [x] Tier 1 platform — TrueNAS on mini‑ITX; Home Assistant on Pi 4 (PoE); core-services + Frigate on a ProDesk via docker-compose
- [x] Home Assistant migration — moved off Harvester to the Pi 4 (PoE) and is currently on the RB5009 (LAN)
- [x] Storage design for NAS + Frigate recordings — TrueNAS, with a dedicated share/dataset for Frigate recordings
- [x] Remote access posture — Cloudflare for now
