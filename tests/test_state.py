"""Tests for session initialization, reset and favorite selection."""
import pytest
from config import DEFAULT_FILTERS
from state import init_filter_state, reset_filters, toggle_favorite, select_tour


def test_init_state_populates_independent_defaults(fresh_session):
    init_filter_state(['순천시'], ['자연 관광'], ['자연생태'])
    assert all(k in fresh_session for k in DEFAULT_FILTERS)
    assert fresh_session['favorites'] == []
    assert fresh_session['selected_tour'] == ''
    assert fresh_session['show_n'] == 9


def test_init_state_preserves_valid_and_drops_stale_choices(fresh_session):
    fresh_session['regions'] = ['순천시', '삭제된 지역']
    fresh_session['categories'] = ['자연 관광', '잘못된 값']
    fresh_session['subcategories'] = ['자연생태', '기타']
    fresh_session['keyword'] = '순천만'
    init_filter_state(['순천시'], ['자연 관광'], ['자연생태'])
    assert fresh_session['regions'] == ['순천시']
    assert fresh_session['categories'] == ['자연 관광']
    assert fresh_session['subcategories'] == ['자연생태']
    assert fresh_session['keyword'] == '순천만'


def test_reset_resets_filters_but_preserves_favorites(fresh_session):
    init_filter_state(['순천시'], ['자연 관광'], ['자연생태'])
    fresh_session['regions'] = ['순천시']
    fresh_session['keyword'] = '죽녹원'
    fresh_session['favorites_only'] = True
    fresh_session['favorites'] = ['a']
    fresh_session['selected_tour'] = 'a'
    reset_filters()
    for key, default in DEFAULT_FILTERS.items():
        assert fresh_session[key] == default
    assert fresh_session['favorites'] == ['a']
    assert fresh_session['selected_tour'] == 'a'


def test_favorite_add_and_remove(fresh_session):
    init_filter_state([], [], [])
    toggle_favorite('a')
    toggle_favorite('b')
    assert fresh_session['favorites'] == ['a','b']
    toggle_favorite('a')
    assert fresh_session['favorites'] == ['b']


def test_select_tour(fresh_session):
    init_filter_state([], [], [])
    select_tour('c')
    assert fresh_session['selected_tour'] == 'c'


def test_reset_defaults_do_not_mutate_config(fresh_session):
    init_filter_state(['순천시'],[],[])
    fresh_session['regions'].append('순천시')
    assert DEFAULT_FILTERS['regions'] == []
    reset_filters()
    fresh_session['regions'].append('순천시')
    assert DEFAULT_FILTERS['regions'] == []
