from data.cities import cities
from data.months import months
from datetime import datetime

# Проверяет дату, которую пользователь вводит в FSM
def validate_departure_date(text):
    if not (
        len(text) == 7
        and text[4] == "-"
        and text[0:4].isdigit()
        and text[5:7].isdigit()
    ):
        return (
            "✈️ Напиши месяц в формате ГГГГ-ММ\n"
            "Например: 2026-06"
        )

    year = int(text[0:4])
    month_number = text[5:7]
    month = int(month_number)

    if not (0 < month < 13):
        return (
            f"В моей вселенной нет месяца {month} 🥲\n"
            "Введи дату еще раз."
        )

    name_month = months[month_number]

    if year < datetime.now().year:
        return (
            "Давай жить настоящим 😅\n"
            "Введи актуальный год поездки."
        )

    if (
        year == datetime.now().year
        and month < datetime.now().month
    ):
        return (
            f"{name_month.title()} уже прошёл 🥲\n"
            "Введи будущий месяц поездки."
        )

    return None

# Разбирает команду /search
def parse_search_command(text):
    parts = text.split()

    if len(parts) < 3:
        return None, "Напиши так: /search волгоград стамбул"

    origin_city = parts[1].lower()
    destination_city = parts[2].lower()

    if len(parts) == 4:
        if parts[3].isdigit():
            budget = int(parts[3])
        else:
            return None, "Введи бюджет числом"
    else:
        budget = None

    return {
        "origin_city": origin_city,
        "destination_city": destination_city,
        "budget": budget
    }, None

# Проверяет город, которую пользователь вводит в FSM
def validate_city(text):
    if text not in cities:
        return (
            f"Похоже, самолёты туда пока не летают... по крайней мере в моей базе ✈️🥲 \n " 
            f"Проверь написание или загляни в /cities"
        )
    return None

def validate_same_city(origin, destination):
    if origin == destination:
        return (
            "Кажется, мы пытаемся улететь "
            "из города в него же 😅\n"
            "Введи другой город назначения."
        )

    return None