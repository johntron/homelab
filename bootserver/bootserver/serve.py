import asyncio

from bootserver import tftp


async def run_servers():
    loop = asyncio.get_running_loop()

    udp_transport, _ = await tftp.serve()
    http_server = await http.serve()

    try:
        await asyncio.Future()
    finally:
        udp_transport.close()
        udp_transport.close()
        http_server.close()


def serve():
    # Run the UDP and HTTP servers
    try:
        print("Starting TFTP and HTTP servers")
        asyncio.run(run_servers())
    except KeyboardInterrupt:
        print("Exiting")
