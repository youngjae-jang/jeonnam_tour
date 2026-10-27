"""Business logic for nearby restaurant results; no Streamlit dependency."""
from models.restaurant import Restaurant
from services.restaurant_api import search_nearby_restaurants


def find_restaurants(latitude, longitude, radius_m, api_key, page=1) -> list[Restaurant]:
    """Fetch one Kakao result page and convert to domain objects."""
    # Preserve the four-argument API call used by existing regression tests.
    if page == 1:
        raw = search_nearby_restaurants(latitude, longitude, radius_m, api_key)
    else:
        raw = search_nearby_restaurants(latitude, longitude, radius_m, api_key, page=page)
    return [Restaurant.from_api(item) for item in raw]


def filter_restaurants(restaurants, category="전체", max_distance_m=None):
    """Filter loaded results without any additional API requests."""
    return [
        place for place in restaurants
        if (category == "전체" or place.category == category)
        and (max_distance_m is None or
             (place.distance_m is not None and place.distance_m <= max_distance_m))
    ]
