import os
import subprocess
import sys
from http.server import HTTPServer
import shlex
from socketserver import BaseRequestHandler

port = 8000
dirname = os.path.dirname(__file__)


class SingleFileHandler(BaseRequestHandler):
    pass


def run(ip=None, server_class=HTTPServer, handler_class=SingleFileHandler):
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print(f'Listening on http://{ip or httpd.server_name}:{httpd.server_port} {httpd.server_address}')
    httpd.serve_forever()


def daemonize():
    print("Starting server daemon")
    process = subprocess.Popen(
        shlex.split(f"{sys.executable} {__file__}"),
        start_new_session=True,
        close_fds=True
    )
    print(f"Started pid {process.pid}")


if 'daemon' in sys.argv:
    daemonize()
else:
    run()
