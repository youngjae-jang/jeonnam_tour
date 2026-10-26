from config import category_label, subcategory_label
from services.tour_data import apply_filters, load_tours


def test_unknown_category_codes_remain_identifiable():
    assert category_label('A99') == '미분류 (A99)'
    assert subcategory_label('A9901') == '미분류 (A9901)'
    assert category_label(None) == '미분류'


def test_filter_service_does_not_require_streamlit(sample_tours):
    result = apply_filters(sample_tours, regions=['순천시'])
    assert result.record_id.tolist() == ['a', 'c']


def test_loader_normalizes_unknown_codes(tmp_path):
    import pandas as pd

    path = tmp_path / 'unknown.csv'
    pd.DataFrame([{
        'title': '새 관광 유형', 'addr1': '전라남도 순천시', 'cat1': 'A99', 'cat2': 'A9901',
        'mapx': '127.5', 'mapy': '34.9',
    }]).to_csv(path, index=False, encoding='utf-8-sig')
    row = load_tours(path).iloc[0]
    assert row.category == '미분류 (A99)'
    assert row.subcategory == '미분류 (A9901)'
