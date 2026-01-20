#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class HostSummary:
    name: str
    reachable: bool
    os: Optional[str]
    uptime_seconds: Optional[int]
    mounts: Optional[str]
    disk_usage: Optional[str]
    systemd_running: Optional[str]
    docker_ps: Optional[str]
    ip_addr: Optional[str]
    ip_route: Optional[str]
    red_flags: List[str] = field(default_factory=list)

    def to_json(self) -> Dict[str, Any]:
        return {
            "host": self.name,
            "reachable": self.reachable,
            "os": self.os,
            "uptime_seconds": self.uptime_seconds,
            "mounts": self.mounts,
            "disk_usage": self.disk_usage,
            "services": {
                "systemd": self.systemd_running is not None,
                "docker": self.docker_ps is not None,
            },
            "network": {
                "ip_addr": self.ip_addr,
                "ip_route": self.ip_route,
            },
            "red_flags": self.red_flags,
        }


def _read_text(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}") from exc


def _format_os(facts: Dict[str, Any]) -> Optional[str]:
    distro = facts.get("ansible_distribution")
    version = facts.get("ansible_distribution_version")
    system = facts.get("ansible_system")
    parts = [part for part in [distro, version] if part]
    if parts:
        return " ".join(parts)
    if system:
        return str(system)
    return None


def _discover_hosts(artifacts_dir: Path) -> Dict[str, Dict[str, Path]]:
    hosts: Dict[str, Dict[str, Path]] = {}
    facts_dir = artifacts_dir / "facts"
    probes_dir = artifacts_dir / "probes"

    if facts_dir.exists():
        for fact_path in facts_dir.glob("*.json"):
            hosts.setdefault(fact_path.stem, {})["facts"] = fact_path

    if probes_dir.exists():
        for host_dir in probes_dir.iterdir():
            if not host_dir.is_dir():
                continue
            host_entry = hosts.setdefault(host_dir.name, {})
            host_entry["mounts"] = host_dir / "mounts.txt"
            host_entry["disk"] = host_dir / "df.txt"
            host_entry["systemctl"] = host_dir / "systemctl_running.txt"
            host_entry["docker"] = host_dir / "docker_ps.txt"
            host_entry["ip_addr"] = host_dir / "ip_addr.txt"
            host_entry["ip_route"] = host_dir / "ip_route.txt"

    return hosts


def _build_summary(host: str, paths: Dict[str, Path]) -> HostSummary:
    facts: Dict[str, Any] = {}
    if "facts" in paths and paths["facts"].exists():
        facts = _read_json(paths["facts"])

    mounts = _read_text(paths["mounts"]) if "mounts" in paths else None
    disk_usage = _read_text(paths["disk"]) if "disk" in paths else None
    systemd_running = _read_text(paths["systemctl"]) if "systemctl" in paths else None
    docker_ps = _read_text(paths["docker"]) if "docker" in paths else None
    ip_addr = _read_text(paths["ip_addr"]) if "ip_addr" in paths else None
    ip_route = _read_text(paths["ip_route"]) if "ip_route" in paths else None

    reachable = bool(facts) or any(
        value for value in [mounts, disk_usage, systemd_running, docker_ps, ip_addr, ip_route]
    )

    red_flags: List[str] = []
    if host.lower() == "frigate":
        if not mounts or "recordings" not in mounts.lower():
            red_flags.append("recordings mount not detected")

    return HostSummary(
        name=host,
        reachable=reachable,
        os=_format_os(facts) if facts else None,
        uptime_seconds=facts.get("ansible_uptime_seconds") if facts else None,
        mounts=mounts,
        disk_usage=disk_usage,
        systemd_running=systemd_running,
        docker_ps=docker_ps,
        ip_addr=ip_addr,
        ip_route=ip_route,
        red_flags=red_flags,
    )


def _render_markdown(summaries: List[HostSummary], generated_at: str) -> str:
    lines = ["# Homelab Discovery Summary", "", f"Generated: {generated_at}", ""]
    lines.append("## Host Reachability")
    for summary in summaries:
        status = "reachable" if summary.reachable else "unreachable"
        lines.append(f"- {summary.name}: {status}")

    lines.append("")
    lines.append("## Host Details")
    for summary in summaries:
        lines.append(f"### {summary.name}")
        lines.append(f"- Reachable: {'yes' if summary.reachable else 'no'}")
        lines.append(f"- OS: {summary.os or 'unknown'}")
        if summary.uptime_seconds is not None:
            lines.append(f"- Uptime (seconds): {summary.uptime_seconds}")
        else:
            lines.append("- Uptime (seconds): unknown")
        lines.append(
            "- Key services: systemd={systemd}, docker={docker}".format(
                systemd="yes" if summary.systemd_running is not None else "no",
                docker="yes" if summary.docker_ps is not None else "no",
            )
        )

        lines.append("- Mounts:")
        lines.append("```")
        lines.append(summary.mounts or "(no data)")
        lines.append("```")

        lines.append("- Disk usage:")
        lines.append("```")
        lines.append(summary.disk_usage or "(no data)")
        lines.append("```")

        lines.append("- Network interfaces:")
        lines.append("```")
        lines.append(summary.ip_addr or "(no data)")
        lines.append("```")

        lines.append("- Routes:")
        lines.append("```")
        lines.append(summary.ip_route or "(no data)")
        lines.append("```")

        if summary.red_flags:
            lines.append(f"- Red flags: {', '.join(summary.red_flags)}")
        else:
            lines.append("- Red flags: none")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    default_artifacts = repo_root / "ansible" / "artifacts"
    artifacts_dir = Path(os.environ.get("ARTIFACTS_DIR", default_artifacts))

    if not artifacts_dir.exists():
        raise SystemExit(f"Artifacts directory not found: {artifacts_dir}")

    hosts = _discover_hosts(artifacts_dir)
    if not hosts:
        raise SystemExit(f"No discovery artifacts found in {artifacts_dir}")

    summaries = [_build_summary(host, paths) for host, paths in sorted(hosts.items())]
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    status_dir = artifacts_dir / "status"
    status_dir.mkdir(parents=True, exist_ok=True)

    summary_json = {
        "generated_at": generated_at,
        "hosts": [summary.to_json() for summary in summaries],
    }

    (status_dir / "summary.json").write_text(
        json.dumps(summary_json, indent=2) + "\n", encoding="utf-8"
    )
    (status_dir / "summary.md").write_text(
        _render_markdown(summaries, generated_at), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
