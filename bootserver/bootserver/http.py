import asyncio
from http.server import SimpleHTTPRequestHandler


class HTTPProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.handler = SimpleHTTPRequestHandler()

    def data_received(self, data):
        self.handler.rfile.feed_data(data)
        self.handler.rfile.feed_eof()
        self.handler.wfile = self.transport

        self.handler.handle_request()

    def connection_lost(self, exc):
        print("HTTP connection lost")
