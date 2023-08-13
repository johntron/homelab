import dataclasses
import string

from bootserver import inventory
from bootserver.console import console
from bootserver.options import options


def write_configs():
    console.print("Writing cloud configs")
    template: str | string.Template
    with open(options.config_create_or_join, "r") as f:
        template = f.read()
    template = string.Template(template)
    cluster = inventory.cluster()
    for node in inventory.all_nodes():
        out = f"{options.static}/config-{node.hostname}.yaml"
        with open(out, "w") as f:
            mappings = {
                **dataclasses.asdict(cluster),
                **dataclasses.asdict(node)
            }
            compiled = template.substitute(mappings)
            f.write(compiled)
            console.print(f"Wrote config for {node.hostname} to {out}")
