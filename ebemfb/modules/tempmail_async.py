import aiohttp
import asyncio
import uuid
from modules.circuit_breaker import circuit

@circuit()
async def get_domains():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.temp-mail.org/request/domains/") as r:
            return await r.json()

@circuit()
async def create_email() -> str:
    domains = await get_domains()
    local = uuid.uuid4().hex[:8]
    return f"{local}@{domains[0]}"

@circuit()
async def wait_for_code(email: str, timeout: int = 120) -> str:
    import time
    start = time.time()
    async with aiohttp.ClientSession() as session:
        while time.time() - start < timeout:
            async with session.get(f"https://api.temp-mail.org/request/mail/id/{email}/") as r:
                msgs = await r.json()
                for m in msgs:
                    if 'код' in m.get('subject', ''):
                        # простая регексп-выборка
                        import re
                        m_body = m.get('body', '')
                        match = re.search(r"(\d{4,6})", m_body)
                        if match:
                            return match.group(1)
            await asyncio.sleep(5)
    raise TimeoutError("No email code received")