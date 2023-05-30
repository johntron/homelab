import asyncio

from bootserver.http import HTTPProtocol
from bootserver.options import options
from bootserver.tftp import TFTPProtocol


async def run_servers():
    loop = asyncio.get_running_loop()

    udp_transport, udp_protocol = await loop.create_datagram_endpoint(
        lambda: TFTPProtocol(options.address, loop, {}), local_addr=(options.address, 69)
    )

    http_server = await loop.create_server(lambda: HTTPProtocol(), options.address, 8080)

    try:
        await asyncio.Future()
    finally:
        udp_transport.close()
        http_server.close()
        udp_transport.close()
        http_server.close()


def serve():
    # Run the UDP and HTTP servers
    try:
        print("Starting TFTP and HTTP servers")
        asyncio.run(run_servers())
    except KeyboardInterrupt:
        print("Exiting")
