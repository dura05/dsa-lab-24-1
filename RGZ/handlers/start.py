from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
<b>💰 Финансовый менеджер</b>

📌 Доступные команды:
/reg — регистрация
/add_operation — добавить операцию
/operations — просмотреть операции
/update_operation — обновить операцию


    """
    await message.answer(welcome_text)