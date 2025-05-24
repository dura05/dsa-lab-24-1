from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db.queries import insert_operation, is_registered

router = Router()

class AddOp(StatesGroup):
    type = State()
    sum = State()
    date = State()

@router.message(F.text == "/add_operation")
async def add_op_cmd(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    if not await is_registered(pool, message.chat.id):
        await message.answer("Вы не зарегистрированы.")
        return

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="РАСХОД"), KeyboardButton(text="ДОХОД")]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer("Выберите тип операции:", reply_markup=kb)
    await state.set_state(AddOp.type)

@router.message(AddOp.type)
async def add_op_type(message: Message, state: FSMContext):
    if message.text not in ["РАСХОД", "ДОХОД"]:
        await message.answer("Выберите тип из кнопок ниже.")
        return

    await state.update_data(type_op=message.text)
    await message.answer("Введите сумму:")
    await state.set_state(AddOp.sum)

@router.message(AddOp.sum)
async def add_op_sum(message: Message, state: FSMContext):
    try:
        sum_ = float(message.text.replace(",", "."))
        if sum_ <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Некорректная сумма. Введите число больше нуля.")
        await state.clear()
        return

    await state.update_data(sum=sum_)
    await message.answer("Введите дату в формате ГГГГ-ММ-ДД:")
    await state.set_state(AddOp.date)

@router.message(AddOp.date)
async def add_op_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
        await state.clear()
        return

    pool = message.bot.session_pool
    data = await state.get_data()
    await insert_operation(pool, message.chat.id, data['sum'], date, data['type_op'])
    await message.answer("Операция добавлена.")
    await state.clear()
