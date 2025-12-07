#!/usr/bin/env python3
"""Remote CLI Runner (rcr): run commands on a remote host via SSH."""

from __future__ import annotations

import configparser
import socket
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Default config path: ~/.remote-cli-runner.ini
CONFIG_PATH = Path.home() / ".remote-cli-runner.ini"


@dataclass
class RemoteConfig:
    """Configuration for connecting to the remote host."""

    host: str
    user: str
    key: str
    port: int = 22


def load_config() -> RemoteConfig:
    """Load remote configuration from CONFIG_PATH."""
    if not CONFIG_PATH.exists():
        print(f"Config file not found: {CONFIG_PATH}", file=sys.stderr)
        print(
            "Create it with a [remote] section (host, user, key, port).",

            file=sys.stderr,
        )
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    if "remote" not in config:
        print(f"[remote] section missing in {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)

    remote = config["remote"]
    host = remote.get("host")
    user = remote.get("user")
    key = remote.get("key")
    port_str = remote.get("port", "22")

    missing = [
        name for name, value in [
            ("host", host),
            ("user", user),
            ("key", key),
        ] if not value
    ]
    if missing:
        print(
            f"Missing values in [remote] section: {', '.join(missing)}",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        port = int(port_str)
    except ValueError:
        print(f"Invalid port in config: {port_str}", file=sys.stderr)
        sys.exit(1)

    return RemoteConfig(host=host, user=user, key=key, port=port)


def resolve_ip(host: str) -> str:
    """Resolve the IP address of the given hostname."""
    try:
        return socket.gethostbyname(host)
    except (socket.gaierror, OSError):
        return "unknown"


def build_ssh_command(cfg: RemoteConfig, remote_cmd: List[str]) -> List[str]:
    """Build the SSH command list for subprocess.run."""
    return [
        "ssh",
        "-i", cfg.key,
        "-p", str(cfg.port),
        f"{cfg.user}@{cfg.host}",
        *remote_cmd,
    ]


def run_remote_command(
    remote_cmd: List[str],
    cmd_label: Optional[str] = None,
    show_banner: bool = True,
) -> int:
    """Execute a remote command via SSH using the default config."""
    cfg = load_config()
    resolved_ip = resolve_ip(cfg.host)

    if show_banner:
        label = cmd_label or (remote_cmd[0] if remote_cmd else "command")
        print(f"Running {label} on host {cfg.host} with IP {resolved_ip}")

    ssh_cmd = build_ssh_command(cfg, remote_cmd)

    try:
        result = subprocess.run(ssh_cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print(
            "Error: ssh client not found. Install OpenSSH client and ensure "
            "'ssh' is in PATH.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        return 130


def print_usage() -> None:
    """Print usage information for the rcr CLI."""
    usage = (
        "Usage:\n"
        "  rcr ping <ping-arguments...>\n"
        "  rcr nslookup <nslookup-arguments...>\n"
        "  rcr <command> [args...]\n\n"
        "Examples:\n"
        "  rcr ping 8.8.8.8 -c 4\n"
        "  rcr nslookup example.com\n"
        "  rcr uname -a\n"
        "  rcr systemctl status ssh\n"
    )
    print(usage, file=sys.stderr)


def main() -> None:
    """Entry point for the rcr CLI."""
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print_usage()
        sys.exit(0 if len(sys.argv) > 1 else 1)

    command = sys.argv[1]

    if command == "ping":
        if len(sys.argv) < 3:
            print("rcr ping requires ping arguments.", file=sys.stderr)
            print("Example: rcr ping 8.8.8.8 -c 4", file=sys.stderr)
            sys.exit(1)
        remote_cmd = ["ping", *sys.argv[2:]]
        code = run_remote_command(remote_cmd, cmd_label="ping")
        sys.exit(code)

    if command == "nslookup":
        if len(sys.argv) < 3:
            print("rcr nslookup requires a hostname.", file=sys.stderr)
            print("Example: rcr nslookup example.com", file=sys.stderr)
            sys.exit(1)
        remote_cmd = ["nslookup", *sys.argv[2:]]
        code = run_remote_command(remote_cmd, cmd_label="nslookup")
        sys.exit(code)

    remote_cmd = sys.argv[1:]
    code = run_remote_command(remote_cmd, cmd_label=command)
    sys.exit(code)


if __name__ == "__main__":
    main()
