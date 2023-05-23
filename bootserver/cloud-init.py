import os
import shlex
import subprocess
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from bootserver.prompt import choose_address
from bootserver.netboot import prepare

port = 8000
dirname = os.path.dirname(__file__)
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


class ConfigCreateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.end_headers()
        self.wfile.write(bytearray(config_create(), 'utf-8'))

    def do_DELETE(self):
        print("Shutting down")
        self.send_response(200)
        self.end_headers()
        sys.exit()


class SingleFileHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        with open('static/undionly.kpxe', 'rb') as f:
            self.undionly = f.read()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Disposition", 'attachment; filename="undionly.kpxe"')
        self.end_headers()
        self.wfile.write(self.undionly)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, directory="bootserver")


def run(ip=None, server_class=HTTPServer, handler_class=SingleFileHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print(f'Listening on http://{ip or httpd.server_name}:{httpd.server_port} {httpd.server_address}')
    httpd.serve_forever()


def daemonize():
    print("Starting server daemon")
    process = subprocess.Popen(
        shlex.split(f"{sys.executable} {__file__}"),
        # start_new_session=True,
        close_fds=True
    )
    print(f"Started pid {process.pid}")


choose_address()
prepare()
# run(ip)
# if 'daemon' in sys.argv:
#     daemonize()
# else:
#     run()
