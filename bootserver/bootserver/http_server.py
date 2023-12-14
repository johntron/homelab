import asyncio
import pathlib

from aiohttp import web

from bootserver.options import options, project_root


# async def handle(request):
#     path = request.path[1:]
#
#     try:
#         with open(pathlib.Path(project_root, "static", path), "rb") as f:
#             mime_type, _ = mimetypes.guess_type(path)
#
#             if mime_type is None:
#                 mime_type = "application/octet-stream"
#
#             return web.Response(body=f.read(), content_type=mime_type)
#     except FileNotFoundError:
#         return web.Response(status=404)


async def serve(loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()):
    app = web.Application()
    static_path = pathlib.Path(project_root, "static")
    app.add_routes([web.static('/', static_path)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, options.address, options.http_port)
    await site.start()
    print(f'HTTP listening on {options.address}:{options.http_port}')
    return site
