from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db.queries import is_registered, operation_exists, update_operation

router = Router()

class UpdateOp(StatesGroup):
    id = State()
    new_sum = State()

@router.message(F.text == "/update_operation")
async def upd_start(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    if not await is_registered(pool, message.chat.id):
        await message.answer("Сначала зарегистрируйтесь.")
        return
    await message.answer("Введите ID операции:")
    await state.set_state(UpdateOp.id)

@router.message(UpdateOp.id)
async def upd_id(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    try:
        op_id = int(message.text)
        if not await operation_exists(pool, message.chat.id, op_id):
            raise ValueError
    except:
        await message.answer("Ошибка: операция не найдена или неверный ID.")
        await state.clear()
        return

    await state.update_data(id=op_id)
    await message.answer("Введите новую сумму:")
    await state.set_state(UpdateOp.new_sum)

@router.message(UpdateOp.new_sum)
async def upd_sum(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    data = await state.get_data()
    try:
        new_sum = float(message.text.replace(",", "."))
        if new_sum <= 0:
            raise ValueError
    except:
        await message.answer("Некорректная сумма. Введите положительное число.")
        await state.clear()
        return

    await update_operation(pool, message.chat.id, data['id'], new_sum)
    await message.answer("Операция обновлена.")
    await state.clear()
