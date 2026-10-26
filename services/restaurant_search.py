"""Build map search links for restaurants near a selected attraction."""
from urllib.parse import quote


def restaurant_search_query(tour: dict) -> str:
    """Return a useful local restaurant query using the attraction's location."""
    address = str(tour.get("addr1", "") or "").strip()
    region = str(tour.get("region", "") or "").strip()
    title = str(tour.get("title", "") or "").strip()

    location = address or region or title
    if not location:
        return "전남 맛집"
    return f"{location} 주변 맛집"


def restaurant_search_urls(tour: dict) -> dict[str, str]:
    """Return Naver Map and Kakao Map search URLs for the attraction area."""
    query = quote(restaurant_search_query(tour), safe="")
    return {
        "네이버 지도": f"https://map.naver.com/p/search/{query}",
        "카카오맵": f"https://map.kakao.com/link/search/{query}",
    }
