import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Включаем логирование
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Хранилище курсов валют
currency_data = {}

# Состояния
class CurrencyState(StatesGroup):
    waiting_for_currency_name = State()
    waiting_for_currency_rate = State()

class ConvertState(StatesGroup):
    waiting_for_convert_currency = State()
    waiting_for_amount = State()
    
    
    
    
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()  # сбрасываем текущее состояние
    await message.answer(
        "Привет! Я бот лабораторной работы 4.\n\n"
        "Вот что я умею:\n"
        "/save_currency — сохранить курс валюты\n"
        "/convert — конвертировать валюту в рубли\n"
        "/restart — сбросить текущий процесс"
    )    

# Команда /save_currency
@dp.message(Command("save_currency"))
async def cmd_save_currency(message: Message, state: FSMContext):
    await message.answer("Введите название валюты (например, USD, EUR):")
    await state.set_state(CurrencyState.waiting_for_currency_name)
    logger.debug("Ожидаем ввод названия валюты")

@dp.message(CurrencyState.waiting_for_currency_name)
async def process_currency_name(message: Message, state: FSMContext):
    await state.update_data(currency_name=message.text.upper())
    await message.answer(f"Теперь введите курс {message.text.upper()} к рублю:")
    await state.set_state(CurrencyState.waiting_for_currency_rate)

@dp.message(CurrencyState.waiting_for_currency_rate)
async def process_currency_rate(message: Message, state: FSMContext):
    user_data = await state.get_data()
    currency_name = user_data.get("currency_name")

    try:
        rate = float(message.text.replace(",", "."))
        currency_data[currency_name] = rate
        await message.answer(f"Курс {currency_name} к рублю сохранен: {rate}")
        await message.answer("Теперь вы можете использовать команду /convert для конвертации.")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число для курса.")

# Команда /convert
@dp.message(Command("convert"))
async def cmd_convert(message: Message, state: FSMContext):
    await message.answer("Введите название валюты, которую хотите конвертировать:")
    await state.set_state(ConvertState.waiting_for_convert_currency)

@dp.message(ConvertState.waiting_for_convert_currency)
async def process_convert_currency(message: Message, state: FSMContext):
    currency = message.text.upper()
    if currency not in currency_data:
        await message.answer("Такой валюты нет в базе. Сначала сохраните её через /save_currency.")
        await state.clear()
        return
    await state.update_data(currency=currency)
    await message.answer(f"Введите сумму в валюте {currency}:")
    await state.set_state(ConvertState.waiting_for_amount)

@dp.message(ConvertState.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    user_data = await state.get_data()
    currency = user_data.get("currency")
    try:
        amount = float(message.text.replace(",", "."))
        rate = currency_data[currency]
        rubles = amount * rate
        await message.answer(f"{amount} {currency} = {rubles:.2f} RUB")
        await state.clear()
    except ValueError:
        await message.answer("Введите корректное число.")

# Команда /restart — ручной сброс FSM
@dp.message(Command("restart"))
async def cmd_restart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Состояние сброшено. Можете начать с /save_currency или /convert.")
    logger.debug("FSM сброшено вручную")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
