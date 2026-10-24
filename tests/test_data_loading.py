"""Input CSV loading and normalization tests using temporary files."""
import pandas as pd
import pytest
from data_service import load_data


def make_csv(tmp_path, rows, encoding='utf-8-sig'):
    path = tmp_path/'tour.csv'
    pd.DataFrame(rows).to_csv(path,index=False,encoding=encoding)
    return path


def test_load_normalizes_and_adds_optional_fields(tmp_path):
    path=make_csv(tmp_path,[dict(title='  순천만  ',addr1='전라남도 순천시 어딘가',cat1='A01',cat2='A0102',mapx='127.5',mapy='34.9')])
    df=load_data(str(path),path.stat().st_mtime_ns)
    row=df.iloc[0]
    assert row.title=='순천만'
    assert row.region=='순천시'
    assert row.category=='자연 관광'
    assert row.subcategory=='자연생태'
    assert row.latitude==34.9 and row.longitude==127.5
    assert row.firstimage==''
    assert row.record_id=='row-0'


def test_load_keeps_invalid_coordinates_but_converts_to_nan(tmp_path):
    path=make_csv(tmp_path,[dict(title='A',addr1='주소 알수없음',cat1='???',mapx='invalid',mapy='invalid',firstimage='javascript:alert(1)')])
    df=load_data(str(path),path.stat().st_mtime_ns)
    row=df.iloc[0]
    assert row.region=='지역 미상'
    assert row.category=='기타'
    assert pd.isna(row.latitude) and pd.isna(row.longitude)
    assert row.firstimage==''


def test_load_accepts_http_https_only(tmp_path):
    rows = [dict(title='A',addr1='전남 여수시 길',cat1='A01',mapx=127,mapy=34,firstimage=x) for x in ('https://photo.test/1.jpg','http://photo.test/2.jpg','ftp://photo.test/3.jpg')]
    path=make_csv(tmp_path,rows)
    df=load_data(str(path),path.stat().st_mtime_ns)
    assert df.firstimage.tolist()==['https://photo.test/1.jpg','http://photo.test/2.jpg','']


def test_load_rejects_missing_required_columns(tmp_path):
    path=make_csv(tmp_path,[dict(title='A')])
    with pytest.raises(ValueError, match='필수 컬럼'):
        load_data(str(path),path.stat().st_mtime_ns)


def test_load_fails_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(str(tmp_path/'missing.csv'),0)


def test_load_falls_back_to_cp949(tmp_path):
    path=make_csv(tmp_path,[dict(title='한글 관광지',addr1='전라남도 목포시',cat1='A02',mapx=126.4,mapy=34.8)],encoding='cp949')
    df=load_data(str(path),path.stat().st_mtime_ns)
    assert df.iloc[0].title=='한글 관광지'
    assert df.iloc[0].region=='목포시'
