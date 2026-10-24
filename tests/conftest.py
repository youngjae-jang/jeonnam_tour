"""Offline-friendly unit tests: stub Streamlit only when it is not installed."""
import sys
import types
from pathlib import Path
import pytest
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    import streamlit
except ImportError:
    st = types.ModuleType('streamlit')
    st.cache_data = lambda *args, **kwargs: (lambda fn: fn)
    st.session_state = {}
    sys.modules['streamlit'] = st


@pytest.fixture
def sample_tours():
    return pd.DataFrame([
        dict(record_id='a', title='순천만습지', addr1='전라남도 순천시 해룡면', region='순천시', category='자연 관광', subcategory='자연생태', createdtime='20240101', latitude=34.9, longitude=127.5, firstimage='https://example.com/a.jpg', contentid='a'),
        dict(record_id='b', title='죽녹원', addr1='전라남도 담양군 담양읍', region='담양군', category='자연 관광', subcategory='자연경관', createdtime='20240501', latitude=35.3, longitude=126.98, firstimage='', contentid='b'),
        dict(record_id='c', title='순천 드라마촬영장', addr1='전라남도 순천시 비례골길', region='순천시', category='인문·문화 관광', subcategory='체험관광', createdtime='20240601', latitude=34.9, longitude=127.55, firstimage='', contentid='c'),
        dict(record_id='d', title='해변', addr1='전라남도 여수시', region='여수시', category='자연 관광', subcategory='자연경관', createdtime='20230101', latitude=0.0, longitude=0.0, firstimage='', contentid='d'),
    ])


@pytest.fixture
def fresh_session(monkeypatch):
    """Lightweight dict session supports both st.session_state.key and ['key']."""
    class Session(dict):
        def __getattr__(self, key):
            try: return self[key]
            except KeyError: raise AttributeError(key) from None
        def __setattr__(self, key, value): self[key] = value
    import state
    session = Session()
    monkeypatch.setattr(state.st, 'session_state', session)
    return session
