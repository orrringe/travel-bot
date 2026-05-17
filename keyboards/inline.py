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

def get_months_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                text="Май 2026",
                callback_data="month:2026-05"
            ),
            InlineKeyboardButton(
                text="Май 2026",
                callback_data="month:2026-05"
            ),
            InlineKeyboardButton(
                text="Май 2026",
                callback_data="month:2026-05"
            )
        ],
        [
            InlineKeyboardButton(
                text="Июнь 2026",
                callback_data="month:2026-06"
            ),
            InlineKeyboardButton(
                text="Июнь 2026",
                callback_data="month:2026-06"
            ),
            InlineKeyboardButton(
                text="Июнь 2026",
                callback_data="month:2026-06"
            )
        ],
        [
            InlineKeyboardButton(
                text="Июль 2026",
                callback_data="month:2026-07"
            ),
            InlineKeyboardButton(
                text="Июль 2026",
                callback_data="month:2026-07"
            ),
            InlineKeyboardButton(
                text="Июль 2026",
                callback_data="month:2026-07"
            )
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )