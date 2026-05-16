from data.months import months

# Формирует текст с информацией о городе
def format_city_info(city):
    places_text = "\n".join([f"• {place}" for place in city["places"]])

    return (
        f"<b>🏙 {city['title']}</b>\n\n"
        f"{city['text']}\n\n"
        f"<b>📍 Что посмотреть:</b>\n"
        f"{places_text}\n\n"
        f"<b>🗓 На сколько ехать:</b> {city['days']}\n\n"
        f"<b>✨ Чем хорош:</b>\n"
        f"{city['feature']}"
    )

# Формирует красивый текст со списком билетов
def format_tickets_message(result):
    text = ""
    ct = 0

    for ticket in result:
        full_link = "https://www.aviasales.ru" + ticket["link"]
        ct += 1

        text += (
            f"{ct}. ✈️ {ticket['departure_at'][:10]}\n"
            f"{ticket['origin']} → {ticket['destination']}\n"
            f"💰 {ticket['price']} ₽\n"
            f"🔁 Пересадок: {ticket['transfers']}\n"
            f'<a href="{full_link}">🔗 Купить билет</a>\n\n'
        )

    return text

# Формирует красивый заголовок поиска: "Сочи → Москва на июнь 2026"
def format_search_title(search_data):
    origin = search_data["origin_name"].title()
    destination = search_data["destination_name"].title()
    departure_date = search_data["departure_at"]

    month_number = departure_date[5:7]
    month = months[month_number]
    year = departure_date[0:4]

    return f"✈️ Найдены билеты {origin} → {destination} на {month} {year}:"
