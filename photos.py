import httpx
from config import API_TOKEN_PHOTO

def get_city_photo(name):
    url = f"https://api.pexels.com/v1/search?query={name}&per_page=1"
    headers = {
    "Authorization": API_TOKEN_PHOTO
    }
    response = httpx.get(url, headers=headers)
    data = response.json()
    photo = data["photos"][0]["src"]["large"]
    return photo