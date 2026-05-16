from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


search_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔍 Найти билеты",
                callback_data="search_help"
            )
        ]
    ]
)


after_search_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏙 О городе",
                callback_data="city_info"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Новый поиск",
                callback_data="search_help"
            )
        ]
    ]
)