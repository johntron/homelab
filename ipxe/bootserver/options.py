import argparse
from os import path

def help(help: str):
    return f"{help} (%(default)s)"

project_root = path.normpath(path.join(path.dirname(__file__), '..'))
parser = argparse.ArgumentParser(prog="bootserver",
                                 description="Bootstraps a bare metal server with an operating system")
parser.add_argument('--static', '-s', help=help("Path to static files served by bootserver"),
                    default=path.join(project_root, 'static'))
parser.add_argument('--ipxe', help=help("Path to iPXE git working directory"),
                    default=path.join(project_root, 'ipxe'))
parser.add_argument('--ipxe-git', help=help("URL from which to clone iPXE"), default='https://github.com/ipxe/ipxe')
parser.add_argument("--overwrite-ipxe", action='store_true', help=help('Ignore existing git working directory for iPXE'))
parser.add_argument("--bootserver", '-b', help=help('IP address for bootserver to listen on'))
parser.add_argument("--chainload", '-c', help=help('Path to template for iPXE chainload script'), default=path.join(project_root, 'chainload.ipxe'))
parser.add_argument("--chainload-output", help=help('Path to save rendered iPXE chainload script'), default=path.join(project_root, 'chainload.ipxe.rendered'))

options = parser.parse_args()
