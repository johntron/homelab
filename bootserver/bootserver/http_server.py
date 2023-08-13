import asyncio
from http.server import BaseHTTPRequestHandler

from bootserver.options import options


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello, world!")


class SimpleHTTPProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.headers = {}
        self.response = ''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        request = data.decode()
        self.handle_request(request)

    def handle_request(self, request):
        self.set_header('Content-Type', 'text/plain')
        self.response = 'Hello, world!'
        self.end(200, 'OK')

    def set_header(self, key, value):
        self.headers[key] = value

    def end(self, code, status):
        self.set_header('Content-Length', len(self.response))

        response = f'HTTP/1.1 {code} {status}\r\n'
        for key, value in self.headers.items():
            response += f'{key}: {value}\r\n'
        response += '\r\n'
        response += self.response
        self.transport.write(response.encode())
        self.transport.close()
        self.response = ''


# Create and run the server
async def serve():
    server = await asyncio.get_event_loop().create_server(
        lambda: SimpleHTTPProtocol(),
        options.address, options.http_port
    )
    print(f'HTTP listening on {options.address}:{options.http_port}')
    return server
