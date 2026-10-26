"""전남 관광 대시보드 실행 진입점. 함수 호출 순서만 관리."""
import streamlit as st
from config import DATA_FILE
from data_service import load_data,apply_filters
from state import init_filter_state
from filters import render_sidebar
from views import render_header,render_metrics,render_charts_map,render_table,render_quality
from components.tour_card import render_cards,render_detail

def main():
    st.set_page_config(page_title='전남 관광 대시보드',page_icon='🌊',layout='wide')

    render_header()

    if not DATA_FILE.exists():
        st.error(f'CSV 파일을 찾지 못했습니다: {DATA_FILE}')
        st.stop()
    try:
        df=load_data(str(DATA_FILE),DATA_FILE.stat().st_mtime_ns)
    except (ValueError,UnicodeError,OSError) as exc:
        st.error(f'데이터를 불러오지 못했습니다: {exc}')
        st.stop()

    regions=sorted(df.region.dropna().unique().tolist())
    categories=sorted(df.category.dropna().unique().tolist())
    subcategories=sorted(df.subcategory.dropna().unique().tolist())

    init_filter_state(regions,categories,subcategories)

    render_sidebar(regions,categories,subcategories)

    filtered=apply_filters(df,regions=st.session_state.regions,categories=st.session_state.categories,subcategories=st.session_state.subcategories,keyword=st.session_state.keyword,favorite_ids=st.session_state.favorites,favorites_only=st.session_state.favorites_only,sort_option=st.session_state.sort_option)
    render_metrics(filtered)
    render_quality(df)

    if filtered.empty:
        st.info('선택 조건에 맞는 관광지가 없습니다. 필터를 초기화해 보세요.')
    else:
        render_charts_map(filtered)
        render_cards(filtered,st.session_state.show_n)
        render_table(filtered)
        
    render_detail(df)

if __name__=='__main__':
    main()
