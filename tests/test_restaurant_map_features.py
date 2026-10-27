"""Tests for restaurant mapping, paging and filtering."""
import pytest
import requests
from models.restaurant import Restaurant
from services.restaurant_api import search_nearby_restaurants
from services.restaurant_service import filter_restaurants


def test_page_and_coordinates_are_forwarded(monkeypatch):
    captured = {}
    class Response:
        def raise_for_status(self):
            pass
        def json(self):
            return {"documents": [{"place_name": "식당", "distance": "123", "x": "127.5", "y": "34.9"}]}
    def fake_get(url, **kwargs):
        captured.update(kwargs)
        return Response()
    monkeypatch.setattr(requests, "get", fake_get)
    result = search_nearby_restaurants(34.9, 127.5, 1000, "test-key", page=2)
    assert captured["params"]["page"] == 2
    assert result[0]["latitude"] == 34.9
    assert result[0]["longitude"] == 127.5


@pytest.mark.parametrize("page", [0, 46, 1.5, "2", True])
def test_invalid_page_is_rejected(page):
    with pytest.raises(ValueError, match="페이지"):
        search_nearby_restaurants(34.9, 127.5, 1000, "test-key", page=page)


def test_restaurant_category_and_distance_filter():
    places = [
        Restaurant("한식집", "음식점 > 한식", "", 300, "", "", 34.9, 127.5),
        Restaurant("카페", "음식점 > 카페", "", 900, "", "", 34.91, 127.51),
    ]
    assert [r.name for r in filter_restaurants(places, "음식점 > 한식", 500)] == ["한식집"]
    assert len(filter_restaurants(places)) == 2
