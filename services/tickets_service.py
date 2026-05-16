import httpx
from config import API_TOKEN


def search_tickets(search_data):
    origin = search_data["origin"]
    destination = search_data["destination"]
    departure_at = search_data["departure_at"]
    direct = search_data["direct"]
    currency = search_data["currency"]
    limit = search_data["limit"]
    one_way = search_data["one_way"]
    budget = search_data["budget"]
    url = f"https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&departure_at={departure_at}&direct={direct.lower()}&currency={currency}&limit={limit}&page=1&one_way={one_way}&token={API_TOKEN}"
    filtered_tickets = []
    response = httpx.get(url)
    data = response.json()
    tickets = data["data"]
    if tickets is None:
        return []
    for ticket in tickets:
        if budget is None or ticket["price"] <= budget:
            filtered_tickets.append(ticket)
    return filtered_tickets

def get_cheapest_ticket(tickets):
    if not tickets:
        return None

    cheapest_ticket = min(tickets, key=lambda ticket: ticket["price"])
    return cheapest_ticket

search_data = {
    "origin": "VOG",
    "destination": "IST",
    "departure_at": "2026-05",
    "direct": False,
    "currency": "rub",
    "limit": 5, 
    "one_way": False
    }
