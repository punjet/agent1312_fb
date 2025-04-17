import asyncio
from modules.logger import logger

async def handle_pipeline_error(context):
    err = context.error
    msg = str(err)
    if '429' in msg:
        wait = 10
        logger.warning("Rate limit, backing off", wait=wait)
        await asyncio.sleep(wait)
        context.retry()
    elif 'captcha' in msg.lower():
        logger.warning("Captcha detected, retrying")
        context.retry()
    else:
        logger.error("Unrecoverable error, skipping account", error=msg)
        context.skip()