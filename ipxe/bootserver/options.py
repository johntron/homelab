import argparse
from os import path

project_root = path.normpath(path.join(path.dirname(__file__), '..'))
parser = argparse.ArgumentParser(prog="bootserver",
                                 description="Bootstraps a bare metal server with an operating system")
parser.add_argument('--static-path', default=path.join(project_root, 'static'))
parser.add_argument('--ipxe-repo-path', default=path.join(project_root, 'ipxe'))
parser.add_argument('--ipxe-git-url', default='https://github.com/ipxe/ipxe')
parser.add_argument("--overwrite-ipxe", action='store_true', help="Ignore existing git working directory for iPXE")

options = parser.parse_args()
print(options)
