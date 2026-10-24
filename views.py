"""대시보드 출력 구성. 데이터 로직은 서비스에, 지도와 카드는 컴포넌트에 위임."""
import streamlit as st
import plotly.express as px
from config import STYLE
from services.statistics import counts
from services.validation import quality_summary
from components.map_view import render_map
from components.tour_card import render_cards,render_detail

def render_header():
    st.markdown(STYLE,unsafe_allow_html=True)
    st.title('🌊 전남 관광 한눈에 보기')
    st.caption('지역과 관광유형을 선택해 전남의 아름다운 여행지를 찾아보세요.')

def render_metrics(df):
    a,b,c,d=st.columns(4)
    a.metric('📍 관광지 수',f'{len(df):,}개')
    b.metric('🗺️ 지역 수',f"{df['region'].nunique()}개")
    c.metric('🏷️ 관광 유형 수',f"{df['category'].nunique()}개")
    d.metric('⭐ 내 즐겨찾기',f"{len(st.session_state.favorites)}개")

def render_charts_map(df):
    left,right=st.columns([1,1],gap='large')
    with left:
        st.subheader('📊 지역별 관광지 수')
        fig=px.bar(counts(df,'region'),x='region',y='count',text='count',color='count',color_continuous_scale='Teal')
        fig.update_layout(height=430,showlegend=False,coloraxis_showscale=False,margin=dict(l=5,r=5,t=10,b=5))
        st.plotly_chart(fig,use_container_width=True)
    with right:
        st.subheader('🗺️ 관광지 상세 지도')
        render_map(df)
    sub=counts(df,'subcategory')
    with st.expander('관광 세부분류 통계'):
        fig2=px.bar(sub,x='subcategory',y='count',text='count')
        st.plotly_chart(fig2,use_container_width=True)

def render_table(df):
    with st.expander('📋 관광지 데이터 및 다운로드'):
        cols=['title','region','category','subcategory','addr1','latitude','longitude']
        st.dataframe(df[cols],hide_index=True,use_container_width=True)
        st.download_button('필터 결과 CSV 저장',df.to_csv(index=False).encode('utf-8-sig'),file_name='jeonnam_filtered.csv',mime='text/csv')

def render_quality(df):
    with st.expander('🧪 데이터 품질 점검'):
        q=quality_summary(df)
        st.dataframe([{'점검 항목':k,'건수':v} for k,v in q.items()],hide_index=True,use_container_width=True)
        st.caption('지도 검증은 경위도 범위 검사이며 전라남도 행정 경계 내 위치를 완벽하게 보장하지 않습니다.')
