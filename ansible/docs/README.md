# Homelab Ansible

Minimum viable automation for a homelab. Start with inspection, then baseline, then host-specific roles.

## Prereqs

- Install Ansible locally.
- (Optional) Install collections: `ansible-galaxy collection install -r requirements.yml`.
- Configure SSH access for your hosts.

## Inventory

Edit `inventory/hosts.yml` and set `ansible_user` and host IPs. This repo assumes IPs (no DNS yet).

## Vault (example)

Create an encrypted vars file when you need secrets:

```
ansible-vault create group_vars/all/vault.yml
```

Then reference vars from your playbooks/roles. Keep secrets out of the repo.
Your SSH private key should not live in the repo; use your local SSH agent or
an untracked `group_vars/all/vault.yml` or `host_vars/*/vault.yml` if needed.

## How to run

- Inspect hosts (safe, read-only):
  - `make inspect`
- Baseline in check mode:
  - `make check`
- Apply baseline:
  - `ansible-playbook -i inventory/hosts.yml playbooks/site.yml`

## Safety notes

- Use `--check --diff` for preview runs.
- SSH hardening defaults keep password auth enabled unless you set `baseline_ssh_password_auth: "no"` and provide SSH keys.
- Running baseline requires `become`.
- When enabling Docker, add users to `docker_users` and re-login.
