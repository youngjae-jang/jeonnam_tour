"""사이드바 UI. 위젯 값은 session_state의 key가 관리한다."""
import streamlit as st
from config import SORT_OPTIONS
from state import reset_filters

def render_sidebar(regions,categories,subcategories):
    with st.sidebar:
        st.title('🔎 관광지 검색')
        st.multiselect('지역 선택',regions,key='regions',placeholder='전체 지역')
        st.multiselect('관광 대분류',categories,key='categories',placeholder='전체 유형')
        st.multiselect('관광 세부분류',subcategories,key='subcategories',placeholder='전체 유형')
        st.text_input('관광지명·지역·주소 통합 검색',key='keyword',placeholder='예: 순천만')
        st.selectbox('정렬 기준',SORT_OPTIONS,key='sort_option')
        st.slider('카드 표시 수',3,24,step=3,key='show_n')
        st.checkbox('즐겨찾기만 보기',key='favorites_only')
        st.button('🔄 필터 초기화',on_click=reset_filters,use_container_width=True)
        st.caption('즐겨찾기는 현재 브라우저 세션에 저장됩니다.')
