import os
import shlex
import shutil
import subprocess

from git import Repo, RemoteProgress
from rich.progress import Progress, BarColumn, TextColumn
from rich import print
from rich.console import Console

from .options import options


class RichProgress(RemoteProgress):
    def __init__(self, progress: Progress):
        self.progress = progress
        self.title = 'Cloning'
        self.task = progress.add_task(self.title)
        super().__init__()

    def update(self, op_code, cur_count, max_count=None, message=''):
        operation = op_code & RemoteProgress.OP_MASK
        stage = op_code & RemoteProgress.STAGE_MASK
        self.progress.update(self.task, total=max_count, completed=cur_count, description=message or self.title)


def clone():
    if options.overwrite_ipxe:
        print(f"Overwriting existing iPXE at {options.ipxe}")
        shutil.rmtree(options.ipxe, ignore_errors=True)

    if os.path.exists(options.ipxe):
        print(f"iPXE exists at {options.ipxe}")
        return

    print(f"Cloning iPXE {options.ipxe_git} ➡ {options.ipxe}")
    with Progress(BarColumn(), TextColumn(' {task.description}'), transient=True) as p:
        Repo.clone_from(options.ipxe_git, options.ipxe, progress=RichProgress(p))


def render_chainloader():
    print(f"Using {options.address} in chainloader")
    with open(options.chainload, 'r') as f:
        template = f.read()
    rendered = template.format(bootserver=options.address)
    with open(options.chainload_output, 'w') as f:
        f.write(rendered)
    print(f"Rendered chainloader script to {options.chainload_output}")


def build():
    command = shlex.split(
        f"make -j24 "
        f"{'clean ' if options.ipxe_clean else ''} "
        f"bin-x86_64-efi/ipxe.efi "
        f"EMBED={os.path.abspath(options.chainload_output)}"  # not an environment variable
    )
    with Progress(BarColumn(), TextColumn(' {task.description}'), transient=True) as p:
        p.add_task('Building', start=False)
        result = subprocess.run(
            command,
            cwd=f"{options.ipxe}/src",
            text=True,
            capture_output=not options.verbose
        )
    try:
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        print(result.stdout)
        console = Console()
        console.print(result.stderr, style="bold red")
        console.print(f"Failed to compile iPXE using: {' '.join(command)}")


def install():
    print(f'Installing ipxe.efi to {options.static}')
    shutil.copy(f'{options.ipxe}/src/bin-x86_64-efi/ipxe.efi', options.static)


def prepare():
    print("Preparing iPXE for netboot")
    clone()
    render_chainloader()
    build()
    install()
    print("Done 🎉")
