"""Business logic for nearby restaurant results; no Streamlit dependency."""
from models.restaurant import Restaurant
from services.restaurant_api import search_nearby_restaurants


def find_restaurants(latitude, longitude, radius_m, api_key) -> list[Restaurant]:
    """Fetch and convert API results into predictable domain objects."""
    return [
        Restaurant.from_api(item)
        for item in search_nearby_restaurants(latitude, longitude, radius_m, api_key)
    ]
