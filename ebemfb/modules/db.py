import asyncpg
from modules.config_loader import settings

async def get_pool():
    pool = await asyncpg.create_pool(dsn=settings.db_dsn)
    return pool