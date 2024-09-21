from typing import Any, Awaitable, Callable
from urllib.parse import parse_qs
from hw.asgi.commands import str2cmd
from hw.asgi.responses import send_err


async def command_handle(recieve: Callable[[], Awaitable[dict[str, Any]]],
                         send: Callable[[dict[str, Any]], Awaitable[None]],
                         command: str, query: dict[str, Any], url: list) -> None:
    await str2cmd[command](recieve, send, query, url)


async def app(
    scope: dict[str, Any],
    recieve: Callable[[], Awaitable[dict[str, Any]]],
    send: Callable[[dict[str, Any]], Awaitable[None]],
) -> None:
    assert scope['type'] == 'http'
    url = scope["path"].split('/')
    if len(url) > 1:
        command = url[1]
        if command in str2cmd.keys():
            meth = scope["method"]
            if meth == 'GET':
                #try:
                    query = parse_qs(scope['query_string'].decode())
                    await command_handle(recieve, send, command, query, url)
                #except (TypeError, ValueError,):
                #    await send_err(send, 422, "invalid json input")
            else:
                await send_err(send, 404, "unknown method (supported only GET)")
        else:
            await send_err(send, 404, "command not found")
    else:
        await send_err(send, 404, "no path found")
