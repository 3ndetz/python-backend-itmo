from typing import Any, Awaitable, Callable
from hw.asgi.responses import send_err, send_result, get_body


def fibonacci(n: int) -> list:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    elif n == 2:
        return 1
    else:
        fib1 = fib2 = 1
        n = int(n) - 2
        while n > 0:
            fib1, fib2 = fib2, fib1 + fib2
            n -= 1
    return fib2


def factorial(n: int) -> int:
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def mean(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)


async def validate_int(send, inp: str) -> int | None:
    try:
        number = int(inp)
        if number is None:
            raise ValueError
        return number
    except (TypeError, ValueError):
        await send_err(send, 422, "invalid input")
        return None


async def validate_int_param(send, query: dict, param_name) -> int | None:
    got_n = query.get(param_name, [None])
    if got_n is not None and len(got_n) > 0:
        return await validate_int(send, got_n[0])
    else:
        await send_err(send, 422, "invalid input")
        return None


async def validate_int_path(send, path: list, level: int = 2) -> int | None:
    if len(path) > level:
        got_n = path[level]
        if got_n is not None and len(got_n) > 0:
            return await validate_int(send, got_n)
        else:
            await send_err(send, 422, "invalid input")
            return None
    else:
        await send_err(send, 422, "invalid path (too much levels)")


async def validate_float_list(send, query: dict) -> list[float] | None:
    try:
        if not isinstance(query, list):
            await send_err(send, 422, 'invalid json type (only list supported)')
            return None
        if len(query) == 0:
            await send_err(send, 400, 'empty list')
            return None
        query = map(float, query)
        query = list(query)
        
        return query
    except (ValueError, TypeError):
        await send_err(send, 422, 'Invalid json input')
        return None


async def factorial_command(_, send: Callable[[dict[str, Any]], Awaitable[None]],
                            query: dict, ___):
    n = await validate_int_param(send, query, 'n')
    if n is not None:
        if n < 0:
            await send_err(send, 400, "n is lower than 0")
        else:
            await send_result(send, factorial(n))


async def fibonacci_command(_, send: Callable[[dict[str, Any]], Awaitable[None]],
                        ____, url: list):
    n = await validate_int_path(send, url, 2)
    if n is not None:
        if n < 0:
            await send_err(send, 400, "n is lower than 0")
        else:
            await send_result(send, fibonacci(n))


async def mean_command(recieve: Callable[[], Awaitable[dict[str, Any]]],
                        send: Callable[[dict[str, Any]], Awaitable[None]],
                            query: dict, ___):
    full_body = await get_body(send, recieve)
    if full_body is not None:
        floats = await validate_float_list(send, full_body)
        if floats is not None:
            await send_result(send, mean(floats))

'''
(recieve, send, query, url)

command_handle(recieve: Callable[[], Awaitable[dict[str, Any]]],
                         send: Callable[[dict[str, Any]], Awaitable[None]],
                         query: dict, url: list) -> None

'''
str2cmd = {
    "factorial": factorial_command,
    "fibonacci": fibonacci_command,
    "mean": mean_command
}
