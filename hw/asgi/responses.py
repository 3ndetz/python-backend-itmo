from typing import Any, Awaitable, Callable
import json


status2str = {
    400: "Bad request",
    404: "Not found",
    422: "Unprocessable entity",

}

ResponseStart = {
        'type': 'http.response.start',
        'headers': [(b'content-type', b'application/json')]
    }
ResponseBody = {
        'type': 'http.response.body',
    }


async def get_body(send: Callable[[dict[str, Any]], Awaitable[None]],
                    recieve: Callable[[], Awaitable[dict[str, Any]]],) -> dict | list | None:
    body = await get_raw_body(recieve)
    try:
        body = json.loads(body.decode())
        return body
    except (ValueError, TypeError, json.JSONDecodeError):
        await send_err(send, 422, 'invalid json input')
        return None


async def get_raw_body(recieve: Callable[[], Awaitable[dict[str, Any]]]) -> bytes:
    body = b''
    more_body = True
    while more_body:
        message = await recieve()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)
    return body   # .decode()


async def send_response(send: Callable[[dict[str, Any]], Awaitable[None]],
                        code: int, body: dict) -> None:
    start = dict(ResponseStart)
    start["status"] = code
    send_body = dict(ResponseBody)
    #if code//100 == 2:
    send_body['body'] = json.dumps(body).encode()
    await send(start)
    await send(send_body)


async def send_err(send: Callable[[dict[str, Any]], Awaitable[None]],
                   code: int, description: str) -> None:
    await send_response(send, code,
                        {'detail': status2str[code] + ": " + description})


async def send_result(send, output: float | int) -> None:
    await send_response(send, 200, {'result': output})
    #print(output)
