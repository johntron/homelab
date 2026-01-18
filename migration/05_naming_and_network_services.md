# 05_naming_and_network_services.md

## goal
Stop hunting DHCP leases. Make every Tier 1 service reachable via stable names.

## decision status
DNS approach is **tabled** for now. This doc tracks options and the minimum requirements regardless of choice.

## minimum requirements (must have)
- DHCP reservations for:
  - routers/switches/APs
  - cameras
  - servers (TMM PCs, mini-ITX)
  - Pis that host services
- Stable names for Tier 1:
  - home assistant
  - frigate
  - nas/backups
- A single place to look up “what is where” (this doc)

## domain preference
- Public domain: johntron.com
- Internal usage: desired, but exact naming scheme TBD

## options (choose later)

### option A: subdomain for internal services
- Example: ha.home.johntron.com
- Pros: contained, easy wildcard certs, clearer split-horizon
- Cons: longer names

### option B: direct hostnames under root
- Example: ha.johntron.com
- Pros: short names
- Cons: requires careful local overrides / split-horizon to avoid surprises

### option C: separate internal-only domain
- Example: home.arpa
- Pros: avoids conflicts entirely
- Cons: doesn’t use johntron.com

## local DNS implementation candidates (later)
- MikroTik DNS + static records (simple but manual)
- Pi-hole / AdGuard Home (nice UX; also ads/malware blocking)
- Dedicated DNS (Unbound/BIND) if needed (probably overkill)

## reserved names (draft)
- ha.<TBD> → (Home Assistant on Pi 4 PoE)
- frigate.<TBD> → (Frigate IP)
- nas.<TBD> → (NAS IP)
- zwave.<TBD> → (Z-Wave JS / zwavejs2mqtt, if kept separate from HA)
- kuma.<TBD> → (Uptime Kuma IP)
- proxy.<TBD> → (reverse proxy IP)

## TLS plan (draft, independent of naming)
- Prefer reverse proxy for Tier 1 with HTTPS for browser-facing services
- Cert strategy:
  - Use Let’s Encrypt DNS-01 with Cloudflare API (works without public exposure)
  - Scope of wildcard depends on naming decision (A/B)

## open items to fill later
- LAN subnet(s)
- DHCP reservation table
- Final naming scheme choice
