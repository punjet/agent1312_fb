import aiohttp
from modules.circuit_breaker import circuit
from modules.logger import logger

PROXY_API = "https://proxyprovider.example.com"

@circuit()
async def health_check(proxy_url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://facebook.com/ping", proxy=proxy_url, timeout=5) as r:
                return r.status == 200
    except Exception as e:
        logger.warn("Proxy health check failed", proxy=proxy_url, error=str(e))
        return False

@circuit()
async def assign_proxy(accounts):
    # accounts: list of dicts
    from modules.proxy_api_client import fetch_proxy
    results = []
    for acc in accounts:
        proxy = await fetch_proxy()
        ok = await health_check(proxy)
        if ok:
            acc['proxy'] = proxy
            results.append(acc)
    return results