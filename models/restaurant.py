"""Immutable restaurant result model independent of Streamlit."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Restaurant:
    name: str
    category: str
    address: str
    distance_m: int | None
    phone: str
    url: str
    latitude: float | None = None
    longitude: float | None = None

    @classmethod
    def from_api(cls, place: dict) -> "Restaurant":
        return cls(
            name=place.get("name", "이름 미상"),
            category=place.get("category", ""),
            address=place.get("address", ""),
            distance_m=place.get("distance_m"),
            phone=place.get("phone", ""),
            url=place.get("url", ""),
            latitude=place.get("latitude"),
            longitude=place.get("longitude"),
        )
