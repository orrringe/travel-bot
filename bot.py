from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import asyncio

from config import TELEGRAM_TOKEN
from services.tickets_service import (
    search_tickets,
    get_cheapest_ticket
)
from data.cities import cities
from data.months import months
from data.city_info import city_info
from photos import get_city_photo

from utils.formatters import (
    format_tickets_message,
    format_search_title,
    format_city_info
)
from utils.validators import (
    validate_departure_date,
    parse_search_command,
    validate_city,
    validate_same_city
)
from keyboards.inline import (
    search_keyboard,
    after_search_keyboard
)


# --- Инициализация бота ---

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# --- Глобальные переменные ---

# Храним последний город назначения пользователя,
# чтобы потом показать информацию о городе по кнопке "О городе"
last_destination_city = {}


# --- FSM состояния для пошагового поиска ---

class SearchStates(StatesGroup):
    origin = State()
    destination = State()
    departure_date = State()

# --- Вспомогательные функции ---

# Собирает параметры поиска для TravelPayouts API
def build_search_data(origin_city, destination_city, departure_date="2026-05", budget=None):
    if origin_city not in cities or destination_city not in cities:
        return None, (
            "Не знаю такой город 😢\n"
            "Доступные города можешь посмотреть по команде /cities"
        )

    origin = cities[origin_city]
    destination = cities[destination_city]

    search_data = {
        "origin": origin,
        "destination": destination,
        "origin_name": origin_city,
        "destination_name": destination_city,
        "departure_at": departure_date,
        "direct": str(False),
        "currency": "rub",
        "limit": 5,
        "budget": budget,
        "one_way": True,
    }

    return search_data, None

# Подготавливает search_data для поиска через команду /search или /cheap
def prepare_search_data(text):
    data, error = parse_search_command(text)

    if error:
        return None, error

    origin_city = data["origin_city"]
    destination_city = data["destination_city"]
    budget = data["budget"]

    # Пока для команд дата остаётся дефолтной
    departure_date = "2026-05"

    return build_search_data(origin_city, destination_city, departure_date, budget)

# --- Команда /start ---
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! Я travel bot ✈️\n\n"
        "Нажми кнопку ниже или напиши /help.\n"
        "Доступные города можно посмотреть по команде /cities",
        reply_markup=search_keyboard
    )


# --- Запуск поиска через кнопку ---

@dp.callback_query(F.data == "search_help")
async def search_help(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✈️ Откуда летим?")
    await state.set_state(SearchStates.origin)
    await callback.answer()


# --- FSM поиск через диалог ---

# Первый шаг FSM: получаем город отправления
@dp.message(SearchStates.origin)
async def process_origin(message: Message, state: FSMContext):
    origin = message.text.lower()

    error = validate_city(origin)

    if error:
        await message.answer(error)
        return

    await state.update_data(origin=origin)
    await message.answer("✈️ Куда летим?")
    await state.set_state(SearchStates.destination)


# Второй шаг FSM: получаем город назначения
@dp.message(SearchStates.destination)
async def process_destination(message: Message, state: FSMContext):
    destination = message.text.lower()
    data = await state.get_data()

    error = validate_city(destination)

    if error:
        await message.answer(error)
        return

    error = validate_same_city(
        data["origin"],
        destination
    )

    if error:
        await message.answer(error)
        return

    await state.update_data(destination=destination)

    await message.answer(
        "✈️ Напиши месяц в формате ГГГГ-ММ\n"
        "Например: 2026-06"
    )

    await state.set_state(SearchStates.departure_date)
    
# Третий шаг FSM: получаем дату и запускаем поиск
@dp.message(SearchStates.departure_date)
async def process_departure_date(message: Message, state: FSMContext):
    departure_date = message.text.lower()

    error = validate_departure_date(departure_date)

    if error:
        await message.answer(error)
        return

    await state.update_data(departure_date=departure_date)

    data = await state.get_data()

    search_data, error = build_search_data(
        data["origin"],
        data["destination"],
        data["departure_date"]
    )

    if error:
        await message.answer(error)
        await state.clear()
        return

    last_destination_city[message.from_user.id] = search_data["destination_name"]

    result = search_tickets(search_data)

    if len(result) == 0:
        await message.answer("Подходящих билетов нет :(")
        await state.clear()
        return

    await message.answer(format_search_title(search_data))

    text = format_tickets_message(result)

    await message.answer(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=after_search_keyboard
    )

    await state.clear()


# --- Команды ---

# Команда поиска билетов
@dp.message(Command("search"))
async def search(message: Message):
    search_data, error = prepare_search_data(message.text)

    if error:
        await message.answer(error)
        return

    last_destination_city[message.from_user.id] = search_data["destination_name"]

    result = search_tickets(search_data)

    if len(result) == 0:
        await message.answer("Билеты не найдены")
        return

    await message.answer(format_search_title(search_data))

    text = format_tickets_message(result)

    await message.answer(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=after_search_keyboard
    )


# Команда поиска самого дешёвого билета
@dp.message(Command("cheap"))
async def cheap(message: Message):
    search_data, error = prepare_search_data(message.text)

    if error:
        await message.answer(error)
        return

    result = search_tickets(search_data)

    if len(result) == 0:
        await message.answer("Билеты не найдены")
        return

    cheapest_ticket = get_cheapest_ticket(result)

    text = format_tickets_message([cheapest_ticket])

    await message.answer(
        text,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


# Команда помощи
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "✈️ Я ищу дешёвые билеты.\n\n"
        "Как пользоваться:\n"
        "/search город_откуда город_куда\n"
        "/search город_откуда город_куда бюджет\n\n"
        "Примеры:\n"
        "/search волгоград стамбул\n"
        "/search волгоград стамбул 15000\n\n"
        "Доступные города можно посмотреть по команде /cities"
    )


# Команда списка доступных городов
@dp.message(Command("cities"))
async def cities_command(message: Message):
    text = "🌍 Пока доступны города:\n\n"

    for city in cities:
        text += f"- {city.title()}\n"

    await message.answer(text)


# --- Callback-кнопки после поиска ---

# Показывает информацию о последнем найденном городе назначения
@dp.callback_query(F.data == "city_info")
async def show_city_info(callback: CallbackQuery):
    user_id = callback.from_user.id

    city_name = last_destination_city.get(user_id)

    if not city_name:
        await callback.message.answer(
            "Не получилось определить город 😢 Попробуй выполнить поиск заново."
        )
        await callback.answer()
        return
    
    city = city_info.get(city_name.lower())

    if not city:
        url_photo = get_city_photo(city_name)
        await callback.message.answer_photo(url_photo)
        await callback.message.answer("Пока у меня нет описания этого города 😢 Но есть фото :)")
        await callback.answer()
        return

    city_name = city["title"]
    url_photo = get_city_photo(city_name)

    await callback.message.answer_photo(url_photo)

    await callback.message.answer(
        format_city_info(city),
        parse_mode="HTML"
    )

    await callback.answer()


# --- Логирование всех остальных сообщений ---

@dp.message()
async def all_messages(message: Message):
    print(
        message.from_user.username,
        ":",
        message.text
    )


# --- Запуск бота ---

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())