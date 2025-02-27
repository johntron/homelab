import asyncio
import os
import pathlib
from urllib import parse, request

import aiohttp
import github
import rich
from rich import print, progress
from yaml import load, Loader

from bootserver import options
from bootserver.console import console


class Release:
    yaml: str

    def __init__(self, url):
        data = request.urlopen(url).read().decode("utf-8")
        self.yaml = load(data, Loader)

    @property
    def url(self):
        return self.yaml["spec"]["isoURL"].strip()

    @property
    def checksum(self):
        return self.yaml["spec"]["isoChecksum"].strip()


def get_tag():
    g = github.Github()
    r = g.get_repo('harvester/harvester')
    return r.get_latest_release().tag_name


class Downloader:
    def __init__(self, session, progress: rich.progress.Progress):
        self.session = session
        self.progress = progress

    async def download_if_missing(self, url: str, filename: str = None):
        parsed = parse.urlparse(url)
        filename = filename or os.path.basename(parsed.path)
        dest_path = (pathlib.Path(options.project_root) / "static" / filename)
        if os.path.exists(dest_path):
            print(f"Already downloaded {dest_path}")
            return

        chunk_size = 32 * 1024
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Unexpected response {response.status} downloading {url}")
            size = int(response.headers["Content-Length"])
            task = self.progress.add_task(f"Downloading {filename}", total=size)
            with open(dest_path, "wb") as dest:
                async for chunk in response.content.iter_chunked(chunk_size):
                    dest.write(chunk)
                    self.progress.update(task, advance=chunk_size)


async def main():
    console.print("Downloading boot files")
    tag = get_tag()
    console.print(f"Latest version is {tag}")
    async with aiohttp.ClientSession() as session:
        with rich.progress.Progress() as progress:
            dl = Downloader(session, progress)
            tasks = []
            base_url = f"https://releases.rancher.com/harvester"
            tasks.append(dl.download_if_missing(f"{base_url}/{tag}/harvester-{tag}-amd64.iso", "os.iso"))
            tasks.append(
                dl.download_if_missing(f"{base_url}/{tag}/harvester-{tag}-rootfs-amd64.squashfs", "fs.squashfs"))
            base_url = f"https://github.com/harvester/harvester/releases/download"
            tasks.append(dl.download_if_missing(f"{base_url}/{tag}/harvester-{tag}-initrd-amd64", "initrd"))
            tasks.append(dl.download_if_missing(f"{base_url}/{tag}/harvester-{tag}-vmlinuz-amd64", "vmlinuz"))
            await asyncio.gather(*tasks)


def netboot_files():
    asyncio.get_event_loop().run_until_complete(main())
