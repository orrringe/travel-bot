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

"""response = httpx.get("https://api.github.com")

print(response.status_code)

data = response.json()

print(data["current_user_url"])
print(data["emojis_url"])
print(data["repository_url"])"""


"""response = httpx.get(url)
data = response.json()
tickets = data["data"]
ct = 0
for ticket in tickets:
    if ticket["transfers"] == 0:
        ct+=1
        print(ct, ".", ticket["origin"], "→", ticket["destination"], " - ",  ticket["price"], "₽,", "Пересадок:", ticket["transfers"])
if ct == 0:
    print("Прямых рейсов не найдено")"""
        
    
        





"""if len(tickets) == 0:
    print("К сожалению, подходящих билетов нет")
else:
    ct = 0
    for ticket in tickets:
        ct+=1
        print(ct, ".", ticket["city"], "-", ticket["price"], "₽")"""



"""print("Ищу билеты", search_data["origin"], "→", search_data["destination"], "на", search_data["date"])
if search_data["budget"] != None:
    print("Бюджет до", search_data["budget"])"""

"""cheap_ticket = tickets[0]
for ticket in tickets:
    if ticket["price"] < cheap_ticket["price"]:
        cheap_ticket = ticket


print(cheap_ticket["city"], '-', cheap_ticket["price"])"""



"""for ticket in tickets:
    if ticket["price"] < 20000 and ticket["transfers"] == 0:
        print(ticket["city"], '-', ticket["price"])"""