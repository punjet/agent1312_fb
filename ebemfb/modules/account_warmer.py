from playwright.async_api import async_playwright
from modules.config_loader import settings
from modules.logger import logger
import asyncio

async def warm_account(acc: dict):
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    context = await browser.new_context(storage_state=acc.get('session'))
    page = await context.new_page()
    try:
        await page.goto('https://facebook.com')
        # эмулируем лайки и прочие действия
        await asyncio.sleep(2)
        await page.goto(settings.ads_manager)
        await asyncio.sleep(2)
        acc['session'] = await context.storage_state()
        logger.info("Account warmed", login=acc['login'])
    finally:
        await browser.close()
        await pw.stop()
    return acc

async def warm_batch(accounts):
    return [await warm_account(acc) for acc in accounts]