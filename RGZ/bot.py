import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import BOT_TOKEN
from db.db import get_pool
from aiogram.client.default import DefaultBotProperties

from handlers.register import router as reg_router
from handlers.add_operation import router as add_op_router
from handlers.operations import router as operations_router
from handlers.update_operation import router as upd_router
from handlers.start import router as start_router

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    pool = await get_pool()
    bot.session_pool = pool
    dp = Dispatcher(storage=MemoryStorage())
    

    await bot.set_my_commands([
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/reg", description="Регистрация"),
        BotCommand(command="/add_operation", description="Добавить операцию"),
        BotCommand(command="/operations", description="Показать операции"),
        BotCommand(command="/update_operation", description="Изменить операцию")
    ])
    dp.include_router(start_router)
    dp.include_router(reg_router)
    dp.include_router(add_op_router)
    dp.include_router(operations_router)
    dp.include_router(upd_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
