from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db.queries import is_registered, register_user

router = Router()

class RegState(StatesGroup):
    waiting_for_name = State()

@router.message(F.text == "/reg")
async def reg_cmd(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    if await is_registered(pool, message.chat.id):
        await message.answer("Вы уже зарегистрированы.")
    else:
        await message.answer("Введите ваше имя:")
        await state.set_state(RegState.waiting_for_name)

@router.message(RegState.waiting_for_name)
async def reg_name(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    await register_user(pool, message.chat.id, message.text)
    await message.answer("Регистрация завершена.")
    await state.clear()
