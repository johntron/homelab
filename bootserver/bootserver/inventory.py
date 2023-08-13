import dataclasses
import ipaddress
import pathlib
import typing

from bootserver.options import options


@dataclasses.dataclass
class Cluster:
    cluster_vip: ipaddress.IPv4Address
    ssh_authorized_key: str
    token: str


@dataclasses.dataclass
class Node:
    hostname: str
    mode: typing.Literal["create"] | typing.Literal["join"]
    target_drive: pathlib.Path
    shell_password: str
    iso_url: str


def cluster():
    return Cluster(
        cluster_vip=ipaddress.IPv4Address("192.168.1.32"),
        token="",
        ssh_authorized_key="github:johntron",
    )


def all_nodes():
    return [
        Node(
            hostname="tiny1",
            mode="create",
            target_drive=pathlib.Path("/dev/nvme0n1"),
            iso_url=f"http://{options.address}:{options.http_port}/os.iso",
            shell_password=""
        ),
        Node(
            hostname="tiny2",
            mode="join",
            target_drive=pathlib.Path("/dev/nvme0n1"),
            iso_url=f"http://{options.address}:{options.http_port}/os.iso",
            shell_password=""
        ),
        Node(
            hostname="itx1",
            mode="join",
            target_drive=pathlib.Path("/dev/nvme0n1"),
            iso_url=f"http://{options.address}:{options.http_port}/os.iso",
            shell_password=""
        )
    ]
