# 06_observability.md

## goal
Know when Tier 1 is down without guessing. Alerts go to phone.

## Tier 1 alert targets
- Home Assistant reachable and healthy
- Frigate reachable and recording/detection functioning
- NAS reachable + backups not stale + storage not full

## minimum viable stack (recommended)
- Uptime Kuma for:
  - HTTP/TCP/ping checks
  - simple dashboards
  - notifications to phone (Pushover recommended; alternatives: HA mobile push / Telegram)
- Optional later:
  - metrics (Prometheus + Grafana)
  - centralized logs (Loki / ELK), only if needed

## checks (initial)
### service uptime checks
- Home Assistant: HTTPS/HTTP check
- Frigate: HTTPS/HTTP check
- NAS:
  - ping
  - TCP port check (SMB 445 or NFS 2049 or SSH 22)
  - “disk usage high” alert (from NAS or via exporter/script)

### backup freshness (“heartbeat”)
- Each backup job should emit a success signal:
  - hit a Kuma “push” endpoint, OR
  - write a timestamp file checked by a script, OR
  - update a Home Assistant sensor
- Alert if no success signal within threshold (e.g., 24h)

### infrastructure checks (Tier 1 dependencies)
- WAN reachability (simple external ping)
- Router/switch/AP reachability
- DNS resolver reachability (once DNS choice is made)

## notification policy (phone)
- Severity:
  - P0: HA/Frigate/NAS down → immediate
  - P1: backups stale / disk usage high → same-day
  - P2: lab nodes down → optional/noisy; default off
- Quiet hours: TBD

## “power outage recovery” test
- Quarterly: simulate power loss
- Pass criteria:
  - Tier 1 returns without manual intervention
  - Alerts fire correctly
  - No corrupt storage / degraded pools
