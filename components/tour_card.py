"""개별 관광지 카드 및 선택 상세정보."""
import streamlit as st
from state import toggle_favorite, select_tour

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

def render_detail(df):
    chosen = str(st.session_state.get('selected_tour',''))
    if not chosen:return
    match=df[df['record_id'].eq(chosen)]
    if match.empty:
        st.info('선택한 관광지가 현재 데이터에 없습니다.')
        return
    r=match.iloc[0]
    with st.expander('📌 선택한 관광지 상세정보',expanded=True):
        st.subheader(str(r['title']))
        st.write('**주소:**',r['addr1'])
        st.write('**지역 / 유형:**',r['region'],'/',r['category'],'/',r['subcategory'])
        st.write('**관광지 ID:**',r['contentid'])
        if r['firstimage']: st.image(r['firstimage'],width=480)
        if str(r.get('description','')).strip(): st.write(r['description'])
        else: st.caption('원본 데이터에 상세 소개가 없어 기본 정보만 표시합니다.')
