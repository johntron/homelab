import asyncio
import os
import sys

from rich import padding, syntax

from bootserver import http_server
from bootserver import tftp_server
from bootserver.console import console


async def run_servers():
    loop = asyncio.get_running_loop()

    udp_transport, _ = await tftp_server.serve()
    server = await http_server.serve()

    try:
        await asyncio.Future()
    finally:
        udp_transport.close()
        udp_transport.close()
        server.close()


def serve():
    # Run the UDP and HTTP servers
    try:
        print("Starting TFTP and HTTP servers")
        asyncio.run(run_servers())
    except KeyboardInterrupt:
        print("Exiting")
    except PermissionError:
        python_path = os.path.realpath(sys.executable)
        console.print("[red]Could not listen on privileged port. Run the following command to enable:")
        console.print(
            padding.Padding(syntax.Syntax(f"sudo setcap 'cap_net_bind_service=+ep' {python_path}", "shell"),
                            (1, 1, 1, 1)))
