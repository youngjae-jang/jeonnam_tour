"""Streamlit cache adapter for the framework-independent tour data service."""
import streamlit as st

from services.tour_data import apply_filters, load_tours, region_counts, valid_map_points


@st.cache_data(show_spinner="관광 데이터를 읽는 중입니다…", max_entries=4)
def load_data(filepath, modified_ns):
    # 파일 수정 시각을 캐시 키로 사용해 CSV 변경을 반영한다.
    return load_tours(filepath)
