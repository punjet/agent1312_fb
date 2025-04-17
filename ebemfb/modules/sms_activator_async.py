import aiohttp
import asyncio
from modules.config_loader import settings
from modules.circuit_breaker import circuit

class SMSAsync:
    def __init__(self, api_key: str = None):
        self.key = api_key or settings.helper_sms_key
        self.base = "https://api.helper20sms.ru"

    @circuit()
    async def get_number(self) -> str:
        async with aiohttp.ClientSession() as session:
            payload = {'api_key': self.key, 'service': 'fb'}
            async with session.post(f"{self.base}/getNumber", data=payload) as r:
                data = await r.json()
                return data['number']

    @circuit()
    async def wait_code(self, number: str, timeout: int = 180) -> str:
        import time
        start = time.time()
        async with aiohttp.ClientSession() as session:
            while time.time() - start < timeout:
                async with session.get(f"{self.base}/getMessages", params={'api_key': self.key, 'number': number}) as r:
                    msgs = await r.json()
                    if msgs:
                        return msgs[0]['code']
                await asyncio.sleep(5)
        raise TimeoutError("No SMS code")