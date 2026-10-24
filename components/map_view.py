"""상호작용 지도: 팝업에 관광지명, 지역, 주소 출력."""
import folium
import streamlit as st
from streamlit_folium import st_folium
from data_service import valid_map_points

def render_map(df):
    points = valid_map_points(df)
    if points.empty:
        st.info('표시할 수 있는 지도 좌표가 없습니다.')
        return
    center = [float(points.latitude.median()), float(points.longitude.median())]
    fmap = folium.Map(location=center,zoom_start=8,tiles='OpenStreetMap',control_scale=True)
    colors = {'자연 관광':'green','인문·문화 관광':'blue'}
    # 다수 마커는 클러스터로 렌더링 부담을 줄임.
    from folium.plugins import MarkerCluster
    cluster = MarkerCluster().add_to(fmap)
    import html
    for r in points.itertuples():
        popup = '<b>' + html.escape(str(r.title)) + '</b><br>' + html.escape(str(r.region)) + '<br>' + html.escape(str(r.addr1))
        folium.Marker([r.latitude,r.longitude],popup=folium.Popup(popup,max_width=260),tooltip=str(r.title),icon=folium.Icon(color=colors.get(r.category,'gray'),icon='info-sign')).add_to(cluster)
    st_folium(fmap,height=430,use_container_width=True,returned_objects=[])
    excluded = len(df)-len(points)
    if excluded: st.caption(f'좌표 유효성 검사로 지도에서 제외된 관광지: {excluded}개')
