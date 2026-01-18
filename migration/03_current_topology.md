# 03_current_topology.md

## current topology summary
- Internet → AT&T fiber ONT → AT&T router
- AT&T router:
  - Performs NAT to LAN
  - Defines the LAN network (single flat LAN)
- MikroTik hEX PoE:
  - Acts as DHCP server for the network defined on AT&T router
  - All traffic goes through the hEX PoE
  - Powers Wi-Fi APs (cAP ac)
- MikroTik RB5009:
  - Currently used as an additional switch/router in the LAN (exact role TBD)
  - Home Assistant Pi 4 (PoE) is currently connected here
- Wi-Fi:
  - 3x MikroTik cAP ac, managed by CAPsMAN (RouterOS)
- No VLANs currently, but would like 2
- Remote access:
  - Cloudflare used to expose Home Assistant and Frigate with SSO

## devices/services placement (current)
- ProDesk (docker-compose) hosts:
  - Frigate
  - Core services (TBD)
- mini-ITX hosts TrueNAS and is connected to UPS via USB
- Pi 4 (PoE + Z-Wave USB) hosts: Home Assistant
- Z-Wave JS / zwavejs2mqtt: TBD (either as an HA add-on on the Pi, or as a separate service)
- Pi (RTL-SDR) hosts: SDR services
- Cameras: Amcrest PoE via passive PoE switch

## current pain points (topology-related)
- Single flat LAN (no isolation)
- IP discovery via DHCP lease checking
- No observability/alerting

## desired (not decided yet)
- Potential segmentation (VLANs) for IoT/cameras/guests
- Stable naming (DNS) + DHCP reservations
- Tiered “core vs lab” network boundaries
- Better storage + backups + restore test
