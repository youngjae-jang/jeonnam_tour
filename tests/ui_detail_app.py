"""Small AppTest target for the selected-tour detail component."""
import pandas as pd
import streamlit as st

from components.tour_card import render_detail


tour = pd.DataFrame([{
    'record_id': 'ui-tour', 'title': '화면 테스트 관광지', 'addr1': '전라남도 순천시 테스트길',
    'region': '순천시', 'category': '자연 관광', 'subcategory': '자연생태',
    'contentid': 'ui-tour', 'firstimage': '', 'description': '',
    'latitude': 34.9, 'longitude': 127.5,
}])

render_detail(tour)
