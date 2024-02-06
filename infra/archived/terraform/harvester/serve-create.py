import os
import shlex
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from string import Template

port = 8000
dirname = os.path.dirname(__file__)
config_create_path = os.path.join(dirname, 'config-create.yaml')
opts = {
    "cluster_vip": "192.168.1.32",
    "token": "",
    "hostname": "tiny2",
    "ssh_authorized_key": "github:johntron",
    "dns_nameserver": "192.168.1.254",
    "shell_password": "",
    "target_drive": "/dev/nvme0n1",
    "iso_url": "https://releases.rancher.com/harvester/v1.1.2/harvester-v1.1.2-amd64.iso",
}


def config_create():
    with open(config_create_path, 'r') as f:
        template = f.read()
    config_create = Template(template)
    config_create = config_create.substitute(**opts)
    # print(config_create)
    return config_create


class ConfigCreateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytearray(config_create(), 'utf-8'))

    def do_DELETE(self):
        print("Shutting down")
        self.send_response(200)
        self.end_headers()
        sys.exit()


def run(server_class=HTTPServer, handler_class=ConfigCreateHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Listening on http://{httpd.server_name}:{httpd.server_port} {httpd.server_address}')
    httpd.serve_forever()


def daemonize():
    print("Starting server daemon")
    process = subprocess.Popen(
        shlex.split(f"{sys.executable} {__file__}"),
        # start_new_session=True,
        close_fds=True
    )
    print(f"Started pid {process.pid}")


if __name__ == '__main__':
    if 'daemon' in sys.argv:
        daemonize()
    else:
        run()

[addr.address for addr in psutil.net_if_addrs()["wlo1"] if addr.family == socket.AF_INET]