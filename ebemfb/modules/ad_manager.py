from modules.logger import logger
import asyncio

class TestAdVerifier:
    def __init__(self, acc: dict):
        self.acc = acc

    async def verify(self) -> dict:
        # эмулируем ожидание модерации
        await asyncio.sleep(10)
        success = True  # логика проверки
        logger.info("Test ad verified", login=self.acc['login'], success=success)
        return { 'test_success': success, 'firstbill_amount': 0.5, 'session': self.acc.get('session') }

class MainCampaignAgent:
    def __init__(self, acc: dict):
        self.acc = acc

    async def confirm(self) -> dict:
        # эмулируем подтверждение основной кампании
        await asyncio.sleep(10)
        campaign_id = 'cmp_' + self.acc['login'][:6]
        logger.info("Main campaign launched", login=self.acc['login'], campaign_id=campaign_id)
        return { 'campaign_id': campaign_id }