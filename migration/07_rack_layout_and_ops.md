# 07_rack_layout_and_ops.md

## goal
Make the attic rack serviceable: predictable cabling, labeling, power, cooling, and remote access.

## rack facts (fill in)
- Rack size (U): TBD
- Rack depth: TBD
- Front/back access: TBD
- Environment: conditioned attic? TBD
- Cooling: passive/active? TBD

## rack layout principles
- Put “Tier 1 dependencies” physically together and simple:
  - ONT / AT&T router / MikroTik core / switch
- Keep Tier 2 physically and logically separate when possible
- Favor short, labeled patch cables
- Make PiKVM reachable even when everything else is sad

## suggested physical grouping (conceptual)
- **Network row**
  - ONT, AT&T router, MikroTik core routing/switching, uplinks to APs, camera PoE
  - Include RB5009 here if it remains part of the “always-on” Tier 1 network path
- **Core compute/storage row**
  - Tier 1 compute host(s), NAS, reverse proxy/monitoring
- **Lab row**
  - k8s/harvester experiments, SDR, spare Pis

## power + UPS
- UPS present: include model, VA/W rating, runtime target
- Decide what is on UPS:
  - minimum: router/switch/AP + Tier 1 compute + NAS
- Decide if graceful shutdown is needed:
  - UPS USB/network integration (NUT/apcupsd) vs ride-through only

## cabling + labeling
- Label both ends:
  - “device-port → switch-port”
- Maintain a simple port map in this doc

## out-of-band management
- PiKVM:
  - what it can reach (which hosts)
  - how it is powered and networked
- Goal: be able to reach a console even if primary services are down

## thermal monitoring
- Add at least one temperature sensor in rack/attic
- Alert on temperature threshold (ties into observability)

## 3D-printed mounts
- Track which devices are mounted and how
- Note any failure modes (heat warp, strain relief, cable retention)

## open items
- Final U-by-U map
- Switch port map
- UPS load plan
