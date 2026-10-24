"""Schema, coordinate boundaries and data quality edge cases."""
import pandas as pd
import pytest
from services.validation import validate_schema, map_valid_mask, quality_summary
from data_service import valid_map_points


def test_complete_minimal_schema_is_valid():
    validate_schema(pd.DataFrame(columns=['title','addr1','cat1','mapx','mapy']))

@pytest.mark.parametrize('missing', ['title','addr1','cat1','mapx','mapy'])
def test_missing_each_required_column(missing):
    keys = [x for x in ['title','addr1','cat1','mapx','mapy'] if x != missing]
    with pytest.raises(ValueError, match=missing):
        validate_schema(pd.DataFrame(columns=keys))


def test_valid_map_coordinates_at_boundaries(sample_tours):
    df = sample_tours.iloc[:4].copy()
    df['latitude'] = [33.0,36.0,32.999,36.001]
    df['longitude'] = [125.0,128.2,126.0,126.0]
    assert map_valid_mask(df).tolist() == [True,True,False,False]


def test_map_excludes_nan_and_zero(sample_tours):
    df = sample_tours.copy()
    df.loc[1,'latitude'] = float('nan')
    assert valid_map_points(df).record_id.tolist() == ['a','c']


def test_quality_summary_detects_missing_and_duplicates(sample_tours):
    df=sample_tours.copy()
    df.loc[1,'title']='  '
    df.loc[1,'addr1']=''
    df.loc[1,'region']='지역 미상'
    df.loc[1,'contentid']='a'
    result=quality_summary(df)
    assert result['전체 건수']==4
    assert result['관광지명 누락']==1
    assert result['주소 누락']==1
    assert result['지역 판독 불가']==1
    assert result['지도 좌표 확인 필요']==1
    assert result['사진 URL 누락']==3
    assert result['식별자 중복']==1


def test_empty_quality_summary(sample_tours):
    q=quality_summary(sample_tours.iloc[:0])
    assert all(v==0 for v in q.values())
