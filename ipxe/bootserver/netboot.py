import os
import shutil

from git import Repo
from git import RemoteProgress
from tqdm import tqdm

from .options import options


class CloneProgress(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.pbar = tqdm(colour="blue")

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


def clone():
    if options.overwrite_ipxe:
        print(f"Overwriting existing iPXE at {options.ipxe}")
        shutil.rmtree(options.ipxe, ignore_errors=True)

    if os.path.exists(options.ipxe):
        print(f"iPXE exists at {options.ipxe}")
        return

    print(f"Cloning iPXE from {options.ipxe_git} to {options.ipxe}")
    Repo.clone_from(options.ipxe_git, options.ipxe, progress=CloneProgress())


def render_chainloader():
    print(f"Using {options.bootserver} in chainloader")
    with open(options.chainload, 'r') as f:
        template = f.read()
    rendered = template.format(bootserver=options.bootserver)
    with open(options.chainload_output, 'w') as f:
        f.write(rendered)
    print(f"Rendered chainloader script to {options.chainload_output}")


def build():
    pass


def move():
    pass


def prepare():
    print("Preparing iPXE for netboot")
    clone()
    render_chainloader()
    build()
    move()
