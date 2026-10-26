import pytest
import requests

from services.restaurant_api import RestaurantSearchError, search_nearby_restaurants


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {'documents': [{
            'place_name': '순천 식당', 'category_name': '음식점 > 한식',
            'road_address_name': '순천시 길 1', 'distance': '250',
            'phone': '061-000-0000', 'place_url': 'https://place.test/1',
        }]}


def test_search_uses_food_category_and_location(monkeypatch):
    captured = {}

    def fake_get(url, **kwargs):
        captured.update(url=url, **kwargs)
        return FakeResponse()

    monkeypatch.setattr(requests, 'get', fake_get)
    places = search_nearby_restaurants(34.95, 127.49, 1000, 'test-key')
    assert captured['params']['category_group_code'] == 'FD6'
    assert captured['params']['x'] == 127.49
    assert captured['params']['y'] == 34.95
    assert captured['params']['sort'] == 'distance'
    assert places[0]['name'] == '순천 식당'
    assert places[0]['distance_m'] == 250


@pytest.mark.parametrize('radius', [-1, 20001])
def test_search_rejects_out_of_range_radius(radius):
    with pytest.raises(ValueError, match='반경'):
        search_nearby_restaurants(34.9, 127.5, radius, 'test-key')


def test_search_reports_http_failures_without_leaking_key(monkeypatch):
    response = requests.Response()
    response.status_code = 401
    error = requests.HTTPError(response=response)

    class FailedResponse:
        def raise_for_status(self):
            raise error

    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: FailedResponse())
    with pytest.raises(RestaurantSearchError, match='HTTP 401') as caught:
        search_nearby_restaurants(34.9, 127.5, 1000, 'secret-key')
    assert 'secret-key' not in str(caught.value)
