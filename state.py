"""모든 위젯 렌더링 전에 세션을 초기화한다."""
import streamlit as st
from config import DEFAULT_FILTERS

def init_filter_state(regions, categories, subcategories):
    for key, default in DEFAULT_FILTERS.items():
        if key not in st.session_state:
            st.session_state[key] = default.copy() if isinstance(default,list) else default
    for key, choices in [('regions',regions),('categories',categories),('subcategories',subcategories)]:
        st.session_state[key] = [v for v in st.session_state[key] if v in choices]
    if 'favorites' not in st.session_state: st.session_state.favorites = []
    if 'selected_tour' not in st.session_state: st.session_state.selected_tour = ''

def reset_filters():
    for key, default in DEFAULT_FILTERS.items():
        st.session_state[key] = default.copy() if isinstance(default,list) else default

def toggle_favorite(record_id):
    ids = st.session_state.favorites
    if record_id in ids: ids.remove(record_id)
    else: ids.append(record_id)

def select_tour(record_id):
    st.session_state.selected_tour = record_id
