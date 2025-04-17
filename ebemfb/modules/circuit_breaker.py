import functools
import asyncio
from aiobreaker import CircuitBreaker

# общий CircuitBreaker для внешних вызовов
breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

def circuit():
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapped(*args, **kwargs):
            return await breaker.call(fn, *args, **kwargs)
        return wrapped
    return decorator