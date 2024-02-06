import argparse
import pathlib
from os import path

project_root = path.normpath(path.join(path.dirname(__file__), '..'))


def help(help: str):
    return f"{help} (%(default)s)"


def common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("--ifname", '-i', help=help('Network interface for bootserver to listen on'))
    parser.add_argument("--address", '-a', help=help('Address for bootserver to listen on'))
    parser.add_argument("--http-port", help=help('Port for HTTP server to listen on'), default=8080)
    parser.add_argument('--static', '-s', help=help("Path to static files served by bootserver"),
                        default=(pathlib.Path(project_root) / 'static'))
    parser.add_argument("--verbose", '-v', help=help('Verbose output'), action='store_true')


def add_prepare_command(subparsers):
    parser = subparsers.add_parser('prepare', description="Clone, configure, and build iPXE with chainloader")
    parser.add_argument('--ipxe', help=help("Path to iPXE git working directory"),
                        default=path.join(project_root, 'ipxe'))
    parser.add_argument('--ipxe-git', help=help("URL from which to clone iPXE"),
                        default='https://github.com/ipxe/ipxe')
    parser.add_argument('--ipxe-clean', help=help("Clean output before building"), action='store_true')
    parser.add_argument("--overwrite-ipxe", action='store_true',
                        help=help('Ignore existing git working directory for iPXE'))
    parser.add_argument("--chainload", '-c', help=help('Path to template for iPXE chainload script'),
                        default=path.join(project_root, 'chainload.ipxe'))
    parser.add_argument("--config-create-or-join",
                        help=help('Path to template file for config-create.yaml/config-join.yaml'),
                        default=path.join(project_root, 'config-create-or-join.yaml'))
    parser.add_argument("--chainload-output", help=help('Path to save rendered iPXE chainload script'),
                        default=path.join(project_root, 'chainload.ipxe.rendered'))
    common_arguments(parser)
    return parser


def add_run_command(subparsers):
    parser = subparsers.add_parser('run', description="Serves iPXE over TFTP")
    common_arguments(parser)


def add_inventory_command(subparsers):
    subparsers.add_parser('inventory', description="Lists inventory")
    common_arguments(parser)


parser = argparse.ArgumentParser(prog="bootserver",
                                 description="Bootstraps a bare metal server with an operating system")
subparsers = parser.add_subparsers(title="subcommands", dest='command', required=True)
add_prepare_command(subparsers)
add_run_command(subparsers)
add_inventory_command(subparsers)
options = parser.parse_args()
