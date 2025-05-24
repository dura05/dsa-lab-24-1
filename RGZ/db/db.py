import asyncpg
from config import DB_CONFIG

async def get_pool():
    return await asyncpg.create_pool(**DB_CONFIG)
