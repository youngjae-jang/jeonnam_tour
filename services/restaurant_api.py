"""Kakao Local API client for nearby restaurant results."""
import math

import requests

API_URL = "https://dapi.kakao.com/v2/local/search/category.json"


class RestaurantSearchError(RuntimeError):
    """A safe, user-facing restaurant search failure."""


def _coordinate(value, lower, upper):
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValueError("유효한 관광지 좌표가 필요합니다.") from exc
    if not math.isfinite(number) or not lower <= number <= upper:
        raise ValueError("유효한 관광지 좌표가 필요합니다.")
    return number


def _radius(value):
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("검색 반경은 0~20,000m 범위여야 합니다.") from exc
    if not math.isfinite(number) or not number.is_integer() or not 0 <= number <= 20000:
        raise ValueError("검색 반경은 0~20,000m 범위여야 합니다.")
    return int(number)


def search_nearby_restaurants(latitude, longitude, radius_m, api_key, page=1):
    """Fetch one Kakao page (up to 15 restaurants), sorted by distance."""
    if not api_key:
        raise RestaurantSearchError("카카오 REST API 키를 설정해야 음식점을 검색할 수 있습니다.")
    latitude = _coordinate(latitude, -90, 90)
    longitude = _coordinate(longitude, -180, 180)
    radius_m = _radius(radius_m)
    if isinstance(page, bool) or not isinstance(page, int) or not 1 <= page <= 45:
        raise ValueError("페이지 번호는 1~45 사이의 정수여야 합니다.")

    try:
        response = requests.get(
            API_URL,
            headers={"Authorization": f"KakaoAK {api_key}"},
            params={
                "category_group_code": "FD6", "x": longitude, "y": latitude,
                "radius": radius_m, "sort": "distance", "size": 15, "page": page,
            },
            timeout=8,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "알 수 없음"
        raise RestaurantSearchError(f"카카오 음식점 검색 요청이 거부됐습니다 (HTTP {status}). API 키와 사용 설정을 확인해 주세요.") from exc
    except (requests.RequestException, ValueError) as exc:
        raise RestaurantSearchError("카카오 음식점 검색에 실패했습니다. 잠시 후 다시 시도해 주세요.") from exc

    def optional_coordinate(value, lower, upper):
        try:
            return _coordinate(value, lower, upper)
        except ValueError:
            return None

    return [
        {
            "name": place.get("place_name", "이름 미상"),
            "category": place.get("category_name", ""),
            "address": place.get("road_address_name") or place.get("address_name", ""),
            "distance_m": int(place["distance"]) if str(place.get("distance", "")).isdigit() else None,
            "phone": place.get("phone", ""),
            "url": place.get("place_url", ""),
            "latitude": optional_coordinate(place.get("y"), -90, 90),
            "longitude": optional_coordinate(place.get("x"), -180, 180),
        }
        for place in payload.get("documents", [])
    ]
