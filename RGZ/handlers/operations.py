from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.queries import get_user_operations, is_registered
import aiohttp

router = Router()

class Operations(StatesGroup):
    currency = State()

@router.message(F.text == "/operations")
async def show_operations(message: Message, state: FSMContext):
    pool = message.bot.session_pool
    if not await is_registered(pool, message.chat.id):
        await message.answer("Сначала зарегистрируйтесь.")
        return

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="RUB"), KeyboardButton(text="USD"), KeyboardButton(text="EUR")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Выберите валюту:", reply_markup=kb)
    await state.set_state(Operations.currency)

@router.message(Operations.currency)
async def process_currency(message: Message, state: FSMContext):
    currency = message.text.upper()
    if currency not in ["RUB", "USD", "EUR"]:
        await message.answer("Некорректная валюта. Выберите из предложенных.")
        await state.clear()
        return

    pool = message.bot.session_pool
    operations = await get_user_operations(pool, message.chat.id)

    rate = 1.0
    if currency != "RUB":
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://localhost:5000/rate?currency={currency}') as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        rate = data['rate']
                    else:
                        await message.answer("Ошибка получения курса.")
                        return
        except Exception as e:
            await message.answer("Сервис недоступен.")
            return

    response = []
    for op in operations:
        converted_sum = float(op['sum']) / rate
        response.append(
            f"ID: {op['id']}\n"
            f"Дата: {op['date']}\n"
            f"Сумма: {converted_sum:.2f} {currency}\n"
            f"Тип: {op['type_operation']}\n"
        )

    await message.answer("\n\n".join(response) if response else "Операций нет.")
    await state.clear()
