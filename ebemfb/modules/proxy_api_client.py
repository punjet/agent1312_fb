import aiohttp
from modules.config_loader import settings
from modules.circuit_breaker import circuit

@circuit()
async def fetch_proxy(api_key: str = None) -> str:
    key = api_key or settings.oxylabs_api_key
    url = f"https://api.oxylabs.io/proxy?api_key={key}&limit=1&country=UA"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data['proxy']  # например 'http://user:pass@host:port'