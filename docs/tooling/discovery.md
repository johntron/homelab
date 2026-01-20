# Discovery Toolkit

## What gets collected
- Ansible facts per host in `ansible/artifacts/facts/<host>.json`.
- Read-only probes per host in `ansible/artifacts/probes/<host>/`:
  - `mounts.txt` from `mount`
  - `df.txt` from `df -h`
  - `systemctl_running.txt` from `systemctl --no-pager --type=service --state=running`
  - `docker_ps.txt` from `docker ps` (only if docker is installed)
  - `ip_addr.txt` from `ip -br a`
  - `ip_route.txt` from `ip r`
- Summaries written to `ansible/artifacts/status/summary.md` and `ansible/artifacts/status/summary.json`.

## How to run
```bash
make discover
make summarize
```

To scope discovery, set `LIMIT` (and any inventory overrides as needed):
```bash
make discover LIMIT=ha
```

## How to extend probes safely
- Keep probes read-only and avoid pipelines.
- Guard each probe with `command -v <cmd>` and set `changed_when: false` and `failed_when: false` on the guard.
- Use `ansible.builtin.command` for the probe itself with `changed_when: false`.
- Write outputs with `delegate_to: localhost` into `ansible/artifacts/probes/<host>/`.
