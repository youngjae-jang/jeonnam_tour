"""Streamlit restaurant UI and caching; detail/card components stay presentation-only."""
import pandas as pd
import streamlit as st

from config import RESTAURANT_RADIUS_DEFAULT, RESTAURANT_RADIUS_MAX
from services.restaurant_api import RestaurantSearchError
from services.restaurant_search import restaurant_search_urls
from services.restaurant_service import find_restaurants


@st.cache_data(ttl=600, show_spinner=False, max_entries=128)
def _cached_restaurant_search(latitude, longitude, radius_m, api_key):
    """Preserve the existing 10-minute cache and key isolation."""
    return find_restaurants(latitude, longitude, radius_m, api_key)


def render_restaurants(tour, api_key=""):
    """Draw map links and optional live results for one selected attraction."""
    st.markdown("**주변 맛집 찾기**")
    st.caption("카카오 로컬 API로 반경 내 음식점을 거리순으로 검색합니다.")
    for label, url in restaurant_search_urls(tour.to_dict()).items():
        st.link_button(f"{label}에서 주변 맛집 검색", url, use_container_width=True)
    if not api_key:
        st.caption("실시간 검색을 쓰려면 KAKAO_REST_API_KEY를 앱 비밀키 또는 환경 변수에 설정하세요.")
    elif pd.isna(tour["latitude"]) or pd.isna(tour["longitude"]):
        st.caption("관광지 좌표가 없어 실시간 주변 맛집 검색을 할 수 없습니다.")
    else:
        _render_restaurant_results(tour, api_key)


def _render_restaurant_results(tour, api_key):
    """Keep the previous widget keys and session result behavior."""
    record_id = str(tour["record_id"])
    radius = st.slider(
        "맛집 검색 반경 (m)",
        min_value=500,
        max_value=RESTAURANT_RADIUS_MAX,
        value=RESTAURANT_RADIUS_DEFAULT,
        step=500,
        key=f"restaurant_radius_{record_id}",
    )
    result_key = f"restaurant_results_{record_id}_{radius}"
    error_key = f"restaurant_error_{record_id}_{radius}"
    if st.button("주변 음식점 검색", key=f"restaurant_search_{record_id}_{radius}"):
        try:
            st.session_state[result_key] = _cached_restaurant_search(
                float(tour["latitude"]), float(tour["longitude"]), radius, api_key
            )
            st.session_state.pop(error_key, None)
        except (RestaurantSearchError, ValueError) as exc:
            st.session_state[error_key] = str(exc)

    if st.session_state.get(error_key):
        st.warning(st.session_state[error_key])
    results = st.session_state.get(result_key)
    if results is None:
        return
    if not results:
        st.info("검색 반경 안에 음식점이 없습니다.")
        return

    st.caption(f"{len(results)}곳을 가까운 순서로 찾았습니다.")
    for index, place in enumerate(results):
        distance = f" · {place.distance_m}m" if place.distance_m is not None else ""
        st.markdown(f"**{place.name}**{distance}")
        st.caption(" · ".join(value for value in (place.category, place.address, place.phone) if value))
        if place.url:
            st.link_button(
                "카카오맵에서 보기", place.url,
                key=f"restaurant_place_{record_id}_{radius}_{index}",
            )
