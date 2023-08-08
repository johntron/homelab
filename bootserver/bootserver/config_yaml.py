import string

from bootserver.console import console
from bootserver.options import options


def configs():
    base_config = {
        "cluster_vip": "192.168.1.32",
        "token": "",
        "ssh_authorized_key": "github:johntron",
        "shell_password": "",
        "target_drive": "/dev/nvme0n1",
        "iso_url": f"http://{options.address}/os.iso",
    }

    return {
        "tiny1": {
            **base_config,
            "mode": "create",
            "hostname": "tiny2",
        },
        "tiny2": {
            **base_config,
            "mode": "join",
            "hostname": "tiny1",
        },
        "itx1": {
            **base_config,
            "mode": "join",
            "hostname": "itx1",
        }
    }


def write_configs():
    console.print("Writing cloud configs")
    template: str | string.Template
    with open(options.config_create_or_join, "r") as f:
        template = f.read()
    template = string.Template(template)
    for name, config in configs().items():
        with open(f"{options.static}/config-{name}.yaml", "w") as f:
            compiled = template.substitute(config)
            f.write(compiled)
