"""Regression tests for the independent restaurant domain/service layers."""
from models.restaurant import Restaurant
from services import restaurant_service


def test_restaurant_model_maps_fields_and_defaults():
    item = Restaurant.from_api({"name": "순천 식당", "distance_m": 250, "url": "https://example.test"})
    assert item.name == "순천 식당"
    assert item.distance_m == 250
    assert item.category == ""
    assert item.address == ""
    assert item.phone == ""
    assert item.url == "https://example.test"


def test_restaurant_model_is_immutable():
    from dataclasses import FrozenInstanceError
    import pytest

    item = Restaurant.from_api({"name": "A"})
    with pytest.raises(FrozenInstanceError):
        item.name = "B"


def test_restaurant_service_delegates_and_normalizes(monkeypatch):
    calls = []

    def fake_api(latitude, longitude, radius_m, api_key):
        calls.append((latitude, longitude, radius_m, api_key))
        return [{"name": "가까운 식당", "distance_m": 123, "address": "순천시"}]

    monkeypatch.setattr(restaurant_service, "search_nearby_restaurants", fake_api)
    result = restaurant_service.find_restaurants(34.9, 127.5, 1000, "key")
    assert calls == [(34.9, 127.5, 1000, "key")]
    assert result == [Restaurant("가까운 식당", "", "순천시", 123, "", "")]


def test_restaurant_service_empty_results(monkeypatch):
    monkeypatch.setattr(restaurant_service, "search_nearby_restaurants", lambda *args: [])
    assert restaurant_service.find_restaurants(34.9, 127.5, 1000, "key") == []
