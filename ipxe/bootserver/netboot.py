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
        print(f"Overwriting existing iPXE at {options.ipxe_repo_path}")
        shutil.rmtree(options.ipxe_repo_path, ignore_errors=True)

    if os.path.exists(options.ipxe_repo_path):
        print(f"iPXE exists at {options.ipxe_repo_path}")
        return

    print(f"Cloning iPXE from {options.ipxe_git_url} to {options.ipxe_repo_path}")
    Repo.clone_from(options.ipxe_git_url, options.ipxe_repo_path, progress=CloneProgress())


def render_chainloader():
    pass


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
