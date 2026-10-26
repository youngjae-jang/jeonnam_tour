from services.restaurant_search import restaurant_search_query, restaurant_search_urls


def test_query_uses_full_address_for_nearby_search():
    tour = {"title": "순천만습지", "region": "순천시", "addr1": "전라남도 순천시 순천만길 513"}
    assert restaurant_search_query(tour) == "전라남도 순천시 순천만길 513 주변 맛집"


def test_query_falls_back_to_region_then_default():
    assert restaurant_search_query({"region": "여수시"}) == "여수시 주변 맛집"
    assert restaurant_search_query({}) == "전남 맛집"


def test_map_urls_encode_korean_query():
    urls = restaurant_search_urls({"addr1": "전라남도 목포시 해안로"})
    assert urls["네이버 지도"].startswith("https://map.naver.com/p/search/")
    assert urls["카카오맵"].startswith("https://map.kakao.com/link/search/")
    assert "%EC%A3%BC%EB%B3%80%20%EB%A7%9B%EC%A7%91" in urls["네이버 지도"]
    assert "주변 맛집" not in urls["카카오맵"]
