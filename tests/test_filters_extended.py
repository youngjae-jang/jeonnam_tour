"""Generated regression tests for all filter branches using fixed records."""
import pytest
from data_service import apply_filters, region_counts
from services.statistics import counts


def test_no_filters_returns_all_without_mutating_source(sample_tours):
    original = sample_tours.copy(deep=True)
    result = apply_filters(sample_tours)
    assert result.record_id.tolist() == ['a', 'b', 'c', 'd']
    assert sample_tours.equals(original)

@pytest.mark.parametrize('field,value,expected', [
    ('regions', ['순천시'], ['a', 'c']),
    ('categories', ['자연 관광'], ['a', 'b', 'd']),
    ('subcategories', ['자연경관'], ['b', 'd']),
    ('regions', ['없는 지역'], []),
])
def test_individual_multiselect_filters(sample_tours, field, value, expected):
    assert apply_filters(sample_tours, **{field:value}).record_id.tolist() == expected


def test_combined_filters_are_intersection(sample_tours):
    found = apply_filters(sample_tours, regions=['순천시'], categories=['자연 관광'], subcategories=['자연생태'])
    assert found.record_id.tolist() == ['a']

@pytest.mark.parametrize('term,expected', [
    ('순천만', ['a']),
    ('비례골길', ['c']),
    ('담양군', ['b']),
    ('순천시', ['a','c']),
    (' 순천만 ', ['a']),
    ('드라마촬영장', ['c']),
    ('not-found', []),
    ('.*', []),
])
def test_keyword_matches_name_address_region_literally(sample_tours, term, expected):
    assert apply_filters(sample_tours, keyword=term).record_id.tolist() == expected


def test_case_insensitive_search(sample_tours):
    sample_tours.loc[0,'title'] = 'Suncheon Bay'
    assert apply_filters(sample_tours, keyword='suncheon').record_id.tolist() == ['a']


def test_favorites_only_and_missing_ids(sample_tours):
    assert apply_filters(sample_tours, favorites_only=True, favorite_ids=['c']).record_id.tolist() == ['c']
    assert apply_filters(sample_tours, favorites_only=True, favorite_ids=[]).empty
    assert apply_filters(sample_tours, favorites_only=False, favorite_ids=['c']).shape[0] == 4

@pytest.mark.parametrize('option,expected', [
    ('관광지명 오름차순', ['c','a','b','d']),
    ('관광지명 내림차순', ['d','b','a','c']),
    ('등록일 최신순', ['c','b','a','d']),
    ('지역명순', ['b','a','c','d']),
    ('유효하지 않은 정렬', ['a','b','c','d']),
])
def test_sort_options(sample_tours, option, expected):
    assert apply_filters(sample_tours, sort_option=option).record_id.tolist() == expected


def test_empty_dataframe_returns_empty(sample_tours):
    assert apply_filters(sample_tours.iloc[:0], keyword='찾기').empty


def test_grouped_counts_consistent(sample_tours):
    grouped = region_counts(sample_tours)
    assert grouped['count'].sum() == len(sample_tours)
    assert dict(zip(grouped.region,grouped['count'])) == {'순천시':2,'담양군':1,'여수시':1}
    other = counts(sample_tours,'category')
    assert dict(zip(other.category,other['count'])) == {'자연 관광':3,'인문·문화 관광':1}
