import argparse
from os import path


def help(help: str):
    return f"{help} (%(default)s)"


def common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("--address", '-a', help=help('Address for bootserver to listen on'))
    parser.add_argument('--static', '-s', help=help("Path to static files served by bootserver"),
                        default=path.join(project_root, 'static'))
    parser.add_argument("--verbose", '-v', help=help('Verbose output'), action='store_true')


project_root = path.normpath(path.join(path.dirname(__file__), '..'))
parser = argparse.ArgumentParser(prog="bootserver",
                                 description="Bootstraps a bare metal server with an operating system")
subparsers = parser.add_subparsers(title="subcommands", dest='command', required=True)

prepare_parser = subparsers.add_parser('prepare', description="Clone, configure, and build iPXE with chainloader")
prepare_parser.add_argument('--ipxe', help=help("Path to iPXE git working directory"),
                            default=path.join(project_root, 'ipxe'))
prepare_parser.add_argument('--ipxe-git', help=help("URL from which to clone iPXE"),
                            default='https://github.com/ipxe/ipxe')
prepare_parser.add_argument('--ipxe-clean', help=help("Clean output before building"), action='store_true')
prepare_parser.add_argument("--overwrite-ipxe", action='store_true',
                            help=help('Ignore existing git working directory for iPXE'))
prepare_parser.add_argument("--chainload", '-c', help=help('Path to template for iPXE chainload script'),
                            default=path.join(project_root, 'chainload.ipxe'))
prepare_parser.add_argument("--chainload-output", help=help('Path to save rendered iPXE chainload script'),
                            default=path.join(project_root, 'chainload.ipxe.rendered'))

run_parser = subparsers.add_parser('run', description="Serves iPXE over TFTP")

common_arguments(prepare_parser)
common_arguments(run_parser)

options = parser.parse_args()
