# 01_inventory.md

## compute
- 2x HP ProDesk 600 G6 Mini PCs
  - each: 2x NVMe drives
- 1x mini-ITX PC
  - 2x NVMe drives
- Raspberry Pi 4 + PoE + Aeotec Z-Wave USB controller (Home Assistant)
- Raspberry Pi 4 + RTL-SDR dongle + antenna
- Raspberry Pi 5 PoE (unused)
- Raspberry Pi 5 + NVMe shield
- 2x unused PoE shields (for Pi)
- PiKVM with 4-port KVM

## network
- MikroTik hEX PoE (currently core router/DHCP; powers APs)
- 3x MikroTik cAP ac (CAPsMAN-managed)
- MikroTik RB5009UPr-IN-S PoE switch/router (in use; Home Assistant Pi is currently connected here)
- AT&T router
- AT&T fiber ONT
- 8-port gigabit unmanaged switch
- 4-port passive PoE switch (cameras)

## cameras / IoT / misc
- 2x Amcrest PoE cameras
- Hue bridge + Hue lights
- Various Z-Wave devices (switches, roller shades, etc.)
- 3D printer + wireless camera
- Various laptops
- 3–4 smartphones / tablets

## power / physical
- UPS: APC Back-UPS 600 BE600M1
- Mini rack: present
  - 3D-printed mounts in progress
- Attic environment: TBD (conditioned vs typical hot attic)

## assigned roles
- mini-ITX → TrueNAS
- Pi4 + PoE + Aeotec Z-Wave → Home Assistant (migrated; running)
- ProDesk #1 → docker-compose host (core-services + Frigate)
- ProDesk #2 → spare / Tier 2
- Pi5 gear → unused/spare

## notes
- Key constraint: physical access is hard → prioritize out-of-band access, labeling, and simple recovery
