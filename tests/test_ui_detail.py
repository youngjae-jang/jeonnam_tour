from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_FILE = Path(__file__).with_name('ui_detail_app.py')


def test_detail_component_shows_selected_tour():
    app = AppTest.from_file(str(APP_FILE))
    app.session_state['selected_tour'] = 'ui-tour'
    app.run()
    assert any('화면 테스트 관광지' in item.value for item in app.subheader)


def test_detail_component_clears_selection_when_filter_hides_tour():
    app = AppTest.from_file(str(APP_FILE))
    app.session_state['selected_tour'] = 'missing-tour'
    app.run()
    assert app.session_state['selected_tour'] == ''
