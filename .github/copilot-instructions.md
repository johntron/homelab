# Copilot/Codex Instructions - Homelab Rebuild

## Project goals
- Prioritize Tier 1 stability and recoverability over cleverness.
- Keep Tier 1 and Tier 2 strictly isolated (failure in Tier 2 must not impact Tier 1).
- Prefer low power, remotely manageable, attic-safe operations.
- Make stable names + reservations first-class (no hunting DHCP leases).

## Definition of done (Tier 1 work)
- Service is idempotently managed by Ansible and supports `--check --diff`.
- Monitoring/alerting exists and is documented (phone alerts for Tier 1).
- Backup and restore are documented and testable.
- A recovery runbook step exists for power-loss and degraded dependencies.
- Rollback note is included in the change description.

## Safety rails
- Never break existing working services; prefer additive changes.
- Avoid destructive changes by default; require explicit break-glass markers for risky ops.
- Break-glass marker: include `# BREAK_GLASS:` in playbooks/tasks and document the operator confirmation steps.
- If unsure, add an ADR and choose the simplest reversible option.

## Ansible operational rules
- Idempotent changes only; every task should support `--check`.
- Use handlers; avoid `shell` or `command` unless required and document why.
- Keep inventory clean; use `inventories/`, `group_vars/`, `host_vars/`, and roles per service.
- Every change must have a rollback note ("re-run playbook" is acceptable if true).

## Secrets policy
- Do NOT commit secrets.
- Source of truth is Bitwarden; assume the operator provides tokens via env vars or local untracked files.
- Default method: untracked `group_vars/all/vault.yml` encrypted with `ansible-vault`.
  - Document required keys in `group_vars/all/vault.yml.example`.
  - Operators supply the vault password via `ANSIBLE_VAULT_PASSWORD_FILE` or `--vault-id`.

## Documentation policy
- Update `README.md` with how-to-run commands and architecture summary.
- Maintain `docs/runbooks/tier1_recovery.md` with key recovery scenarios.
- Maintain ADRs in `docs/decisions/` for key choices (DNS, naming, UPS).

## Testing policy
- CI must run `ansible-lint` (and `yamllint` if available) on PRs.
- Provide a local test recipe: lint, check mode, targeted tags, and an inventory sanity check.
