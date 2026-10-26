"""개별 관광지 카드 및 선택 상세정보."""
import streamlit as st
import pandas as pd
from config import RESTAURANT_RADIUS_DEFAULT, RESTAURANT_RADIUS_MAX
from state import toggle_favorite, select_tour
from services.restaurant_api import RestaurantSearchError, search_nearby_restaurants
from services.restaurant_search import restaurant_search_urls


@st.cache_data(ttl=600, show_spinner=False, max_entries=128)
def _cached_restaurant_search(latitude, longitude, radius_m, api_key):
    # 같은 좌표와 반경 요청은 10분 동안 재사용한다.
    return search_nearby_restaurants(latitude, longitude, radius_m, api_key)

def render_cards(df, show_n):
    st.subheader('🏝️ 관광지 둘러보기')
    rows = df.head(show_n)
    if rows.empty: st.info('조건에 맞는 관광지가 없습니다.');return
    for start in range(0,len(rows),3):
        cols = st.columns(3,gap='medium')
        for col,(_,r) in zip(cols,rows.iloc[start:start+3].iterrows()):
            with col:
                with st.container(border=True):
                    if r['firstimage']:
                        st.image(r['firstimage'],use_container_width=True)
                    else:
                        st.info('🖼️ 등록된 사진이 없습니다.')
                    st.markdown('**'+str(r['title'])+'**')
                    st.caption(f"📍 {r['region']} · {r['category']} · {r['subcategory']}")
                    a,b=st.columns(2)
                    id_ = str(r['record_id'])
                    a.button('★ 즐겨찾기 해제' if id_ in st.session_state.favorites else '☆ 즐겨찾기',key=f'fav_{start}_{id_}',on_click=toggle_favorite,args=(id_,),use_container_width=True)
                    b.button('상세보기',key=f'detail_{start}_{id_}',on_click=select_tour,args=(id_,),use_container_width=True)

def render_detail(df, restaurant_api_key=''):
    chosen = str(st.session_state.get('selected_tour',''))
    if not chosen:return
    match=df[df['record_id'].eq(chosen)]
    if match.empty:
        # 검색 결과에서 제외된 관광지는 선택 상태를 해제해 오래된 상세 정보가 남지 않게 한다.
        st.session_state.selected_tour = ''
        return
    r=match.iloc[0]
    with st.expander('📌 선택한 관광지 상세정보',expanded=True):
        st.subheader(str(r['title']))
        st.write('**주소:**',r['addr1'])
        st.write('**지역 / 유형:**',r['region'],'/',r['category'],'/',r['subcategory'])
        st.write('**관광지 ID:**',r['contentid'])
        st.markdown('**주변 맛집 찾기**')
        st.caption('카카오 로컬 API로 반경 내 음식점을 거리순으로 검색합니다.')
        for label, url in restaurant_search_urls(r.to_dict()).items():
            st.link_button(f'{label}에서 주변 맛집 검색', url, use_container_width=True)
        if restaurant_api_key and pd.notna(r['latitude']) and pd.notna(r['longitude']):
            _render_restaurant_results(r, restaurant_api_key)
        elif not restaurant_api_key:
            st.caption('실시간 검색을 쓰려면 KAKAO_REST_API_KEY를 앱 비밀키 또는 환경 변수에 설정하세요.')
        else:
            st.caption('관광지 좌표가 없어 실시간 주변 맛집 검색을 할 수 없습니다.')
        if r['firstimage']: st.image(r['firstimage'],width=480)
        if str(r.get('description','')).strip(): st.write(r['description'])
        else: st.caption('원본 데이터에 상세 소개가 없어 기본 정보만 표시합니다.')


def _render_restaurant_results(tour, api_key):
    """Offer an explicit radius search and retain results across Streamlit reruns."""
    record_id = str(tour['record_id'])
    radius = st.slider(
        '맛집 검색 반경 (m)',
        min_value=500,
        max_value=RESTAURANT_RADIUS_MAX,
        value=RESTAURANT_RADIUS_DEFAULT,
        step=500,
        key=f'restaurant_radius_{record_id}',
    )
    result_key = f'restaurant_results_{record_id}_{radius}'
    error_key = f'restaurant_error_{record_id}_{radius}'
    if st.button('주변 음식점 검색', key=f'restaurant_search_{record_id}_{radius}'):
        try:
            st.session_state[result_key] = _cached_restaurant_search(
                float(tour['latitude']), float(tour['longitude']), radius, api_key
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
        st.info('검색 반경 안에 음식점이 없습니다.')
        return
    st.caption(f'{len(results)}곳을 가까운 순서로 찾았습니다.')
    for index, place in enumerate(results):
        distance = f" · {place['distance_m']}m" if place['distance_m'] is not None else ''
        st.markdown(f"**{place['name']}**{distance}")
        st.caption(' · '.join(value for value in (place['category'], place['address'], place['phone']) if value))
        if place['url']:
            st.link_button('카카오맵에서 보기', place['url'], key=f"restaurant_place_{record_id}_{radius}_{index}")
