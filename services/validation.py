"""데이터 품질 검사. 잘못된 좌표도 관광지 목록에서는 유지한다."""
import pandas as pd
REQUIRED = ('title','addr1','cat1','mapx','mapy')

def validate_schema(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError('CSV 필수 컬럼 누락: ' + ', '.join(missing))

def map_valid_mask(df):
    # 전남 일대의 완화된 경계 박스. 행정구역 포함 여부의 정밀 판정은 아님.
    return df['latitude'].between(33.0,36.0) & df['longitude'].between(125.0,128.2)

def quality_summary(df):
    ids = df.get('contentid',pd.Series(dtype='object'))
    return {'전체 건수':len(df), '관광지명 누락':int(df['title'].fillna('').astype(str).str.strip().eq('').sum()),
            '주소 누락':int(df['addr1'].fillna('').astype(str).str.strip().eq('').sum()),
            '지역 판독 불가':int(df['region'].eq('지역 미상').sum()),
            '지도 좌표 확인 필요':int((~map_valid_mask(df)).sum()),
            '사진 URL 누락':int(df['firstimage'].eq('').sum()),
            '식별자 중복':int(ids.duplicated().sum()) if len(ids) else 0}
