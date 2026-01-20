#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bw_ssh_agent.sh load --item <name-or-id> [--attachment <filename>] [--ttl 1h] [--confirm] [--ephemeral-ttl <seconds>]
  bw_ssh_agent.sh create --name <item-name> [--comment <ssh-comment>] [--ephemeral-ttl <seconds>]

Notes:
  - Requires Bitwarden CLI ("bw") and an unlocked session (BW_SESSION).
  - For macOS sandboxed environments, you may need:
      export BITWARDENCLI_APPDATA_DIR="$HOME/.bw-cli"
  - Use --ephemeral-ttl to store Bitwarden CLI data in a temp dir that
    auto-deletes after the specified number of seconds.

Quick start (bash/zsh):
  export BITWARDENCLI_APPDATA_DIR="$(mktemp -d "/tmp/bwcli.XXXXXX")"
  bw login
  export BW_SESSION="$(bw unlock --raw)"
  eval "$(ssh-agent -s)"
  bw_ssh_agent.sh create --name "SSH Key - Network Appliances - readonly"
  bw_ssh_agent.sh load --item "SSH Key - Network Appliances - readonly" --attachment id_ed25519 --ttl 1h --confirm

Quick start (fish):
  set -x BITWARDENCLI_APPDATA_DIR (mktemp -d "/tmp/bwcli.XXXXXX")
  bw login
  set -x BW_SESSION (bw unlock --raw)
  eval (ssh-agent -c)
  bw_ssh_agent.sh create --name "SSH Key - Network Appliances - readonly"
  bw_ssh_agent.sh load --item "SSH Key - Network Appliances - readonly" --attachment id_ed25519 --ttl 1h --confirm
USAGE
}

err() {
  echo "error: $*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || err "missing dependency: $1"
}

require_session() {
  if [[ -z "${BW_SESSION:-}" ]]; then
    err "BW_SESSION not set. Run: bw login && export BW_SESSION=\$(bw unlock --raw) (fish: set -x BW_SESSION (bw unlock --raw))"
  fi
}

resolve_item_id() {
  local ident="$1"
  local items_json
  items_json="$(bw --session "$BW_SESSION" list items --search "$ident")"
  python3 - <<'PY' "$ident" "$items_json"
import json, sys
ident = sys.argv[1]
try:
    items = json.loads(sys.argv[2])
except json.JSONDecodeError:
    sys.stderr.write("error: Bitwarden CLI returned non-JSON output; ensure you are logged in and online.\n")
    sys.stderr.write("hint: run 'bw login' then 'bw unlock --raw' in the same shell.\n")
    sys.stderr.write(sys.argv[2] + "\n")
    sys.exit(2)
exact = [i for i in items if i.get("name") == ident or i.get("id") == ident]
if len(exact) == 1:
    print(exact[0]["id"])
    sys.exit(0)
if len(exact) > 1:
    sys.stderr.write("error: multiple items match; use an item id:\n")
    for i in exact:
        sys.stderr.write(f'  {i.get("name")} ({i.get("id")})\n')
    sys.exit(2)
sys.stderr.write("error: no matching item found\n")
sys.exit(3)
PY
}

select_attachment_id() {
  local item_id="$1"
  local filename="${2:-}"
  local item_json
  item_json="$(bw --session "$BW_SESSION" get item "$item_id")"
  python3 - <<'PY' "$item_json" "$filename"
import json, sys
try:
    item = json.loads(sys.argv[1])
except json.JSONDecodeError:
    sys.stderr.write("error: Bitwarden CLI returned non-JSON output; ensure you are logged in and online.\n")
    sys.stderr.write("hint: run 'bw login' then 'bw unlock --raw' in the same shell.\n")
    sys.stderr.write(sys.argv[1] + "\n")
    sys.exit(2)
filename = sys.argv[2] if len(sys.argv) > 2 else ""
atts = item.get("attachments") or []
if not atts:
    sys.stderr.write("error: item has no attachments\n")
    sys.exit(2)
if filename:
    for a in atts:
        if a.get("fileName") == filename:
            print(a["id"])
            sys.exit(0)
    sys.stderr.write("error: attachment not found; available:\n")
    for a in atts:
        sys.stderr.write(f'  {a.get("fileName")} ({a.get("id")})\n')
    sys.exit(3)
if len(atts) == 1:
    print(atts[0]["id"])
    sys.exit(0)
sys.stderr.write("error: multiple attachments; specify --attachment <filename>\n")
for a in atts:
    sys.stderr.write(f'  {a.get("fileName")} ({a.get("id")})\n')
sys.exit(4)
PY
}

ensure_agent() {
  if [[ -z "${SSH_AUTH_SOCK:-}" ]]; then
    err "SSH_AUTH_SOCK not set. Start an agent: eval \"\$(ssh-agent -s)\" (fish: eval (ssh-agent -c))"
  fi
}

ensure_bw_unlocked() {
  local status_json
  status_json="$(bw --session "$BW_SESSION" status --raw 2>/dev/null || true)"
  python3 - <<'PY' "$status_json"
import json, sys
raw = sys.argv[1]
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    sys.stderr.write("error: unable to read Bitwarden status; ensure you are logged in and online.\n")
    sys.stderr.write("hint: run 'bw login' then 'bw unlock --raw' in the same shell.\n")
    sys.stderr.write(raw + "\n")
    sys.exit(2)
status = data.get("status")
if status != "unlocked":
    sys.stderr.write(f"error: Bitwarden status is '{status}'. Run: bw login && bw unlock\n")
    sys.stderr.write("fish: set -x BW_SESSION (bw unlock --raw)\n")
    sys.exit(2)
PY
}

setup_ephemeral_appdata() {
  local ttl="$1"
  [[ -n "$ttl" ]] || return 0
  if ! [[ "$ttl" =~ ^[0-9]+$ ]]; then
    err "--ephemeral-ttl must be a number of seconds"
  fi

  if [[ -n "${BITWARDENCLI_APPDATA_DIR:-}" ]]; then
    local base_tmp="${TMPDIR:-/tmp}"
    if [[ "$BITWARDENCLI_APPDATA_DIR" == "$base_tmp"* || "$BITWARDENCLI_APPDATA_DIR" == "/var/folders/"* || "$BITWARDENCLI_APPDATA_DIR" == "/tmp/"* ]]; then
      (sleep "$ttl"; rm -rf "$BITWARDENCLI_APPDATA_DIR") >/dev/null 2>&1 &
    else
      echo "warning: BITWARDENCLI_APPDATA_DIR is not in a temp path; skipping auto-delete" >&2
    fi
    return 0
  fi

  umask 077
  local tmpdir
  tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/bwcli.XXXXXX")"
  chmod 700 "$tmpdir"
  export BITWARDENCLI_APPDATA_DIR="$tmpdir"
  (sleep "$ttl"; rm -rf "$tmpdir") >/dev/null 2>&1 &
}

cmd="${1:-}"
shift || true

case "$cmd" in
  load)
    need_cmd bw
    need_cmd ssh-add
    need_cmd python3
    require_session
    ensure_agent
    ensure_bw_unlocked

    item=""
    attachment=""
    ttl=""
    confirm="false"
    ephemeral_ttl=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --item) item="$2"; shift 2 ;;
        --attachment) attachment="$2"; shift 2 ;;
        --ttl) ttl="$2"; shift 2 ;;
        --confirm) confirm="true"; shift ;;
        --ephemeral-ttl) ephemeral_ttl="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) err "unknown argument: $1" ;;
      esac
    done
    [[ -n "$item" ]] || err "--item is required"
    setup_ephemeral_appdata "$ephemeral_ttl"

    item_id="$(resolve_item_id "$item")"
    attachment_id="$(select_attachment_id "$item_id" "$attachment")"

    umask 077
    tmpdir="${TMPDIR:-/tmp}"
    tmpfile="$(mktemp "$tmpdir/bwkey.XXXXXX")"
    trap 'rm -f "$tmpfile"' EXIT

    bw --session "$BW_SESSION" get attachment "$attachment_id" --itemid "$item_id" --output "$tmpfile" >/dev/null

    ssh_args=()
    [[ -n "$ttl" ]] && ssh_args+=("-t" "$ttl")
    [[ "$confirm" == "true" ]] && ssh_args+=("-c")
    ssh-add "${ssh_args[@]}" "$tmpfile" >/dev/null
    ;;

  create)
    need_cmd bw
    need_cmd ssh-keygen
    need_cmd python3
    require_session
    ensure_bw_unlocked

    name=""
    comment="codex-readonly"
    ephemeral_ttl=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --name) name="$2"; shift 2 ;;
        --comment) comment="$2"; shift 2 ;;
        --ephemeral-ttl) ephemeral_ttl="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) err "unknown argument: $1" ;;
      esac
    done
    [[ -n "$name" ]] || err "--name is required"
    setup_ephemeral_appdata "$ephemeral_ttl"

    umask 077
    tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/bwkeydir.XXXXXX")"
    trap 'rm -rf "$tmpdir"' EXIT

    keyfile="$tmpdir/id_ed25519"
    ssh-keygen -t ed25519 -a 100 -N "" -C "$comment" -f "$keyfile" >/dev/null

    encoded="$(
      cat <<JSON | bw --session "$BW_SESSION" encode
{"type":2,"name":"$name","notes":"Generated by bw_ssh_agent.sh"}
JSON
    )"

    item_id="$(
      bw --session "$BW_SESSION" create item "$encoded" | python3 - <<'PY'
import json, sys
try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.stderr.write("error: Bitwarden CLI returned non-JSON output; ensure you are logged in and online.\n")
    sys.stderr.write("hint: run 'bw login' then 'bw unlock --raw' in the same shell.\n")
    sys.exit(2)
print(data["id"])
PY
    )"

    bw --session "$BW_SESSION" create attachment --itemid "$item_id" --file "$keyfile" >/dev/null
    bw --session "$BW_SESSION" create attachment --itemid "$item_id" --file "$keyfile.pub" >/dev/null

    echo "Created Bitwarden item: $name ($item_id)"
    echo "Public key:"
    cat "$keyfile.pub"
    ;;

  -h|--help|"")
    usage
    ;;
  *)
    err "unknown command: $cmd"
    ;;
esac
