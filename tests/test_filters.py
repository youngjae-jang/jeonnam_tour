from config import DATA_FILE
from data_service import load_data,apply_filters,valid_map_points,region_counts

def source():return load_data(str(DATA_FILE),DATA_FILE.stat().st_mtime_ns)
def test_load_and_schema():
    df=source()
    assert len(df)>500
    assert {'region','category','subcategory','latitude','longitude','record_id'}.issubset(df.columns)
def test_region_filter():
    df=source()
    region=df.region.iloc[0]
    assert set(apply_filters(df,regions=[region]).region)=={region}
def test_search_address():
    df=source()
    address=df.addr1.iloc[0]
    result=apply_filters(df,keyword=address)
    assert len(result)>=1
def test_sorting_and_favorite():
    df=source()
    out=apply_filters(df,sort_option='관광지명 오름차순')
    assert out.title.tolist()==sorted(out.title.tolist())
    key=df.record_id.iloc[0]
    assert set(apply_filters(df,favorite_ids=[key],favorites_only=True).record_id)=={key}
def test_valid_coordinates():
    df=source()
    m=valid_map_points(df)
    assert len(m)<=len(df)
    assert m.latitude.between(33,36).all()
    assert m.longitude.between(125,128.2).all()
def test_counts():
    df=source()
    assert region_counts(df)['count'].sum()==len(df)
