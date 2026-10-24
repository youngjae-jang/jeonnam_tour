import pandas as pd
import pytest
from services.validation import validate_schema,quality_summary
from data_service import load_data
from config import DATA_FILE

def test_missing_column():
    with pytest.raises(ValueError,match='필수 컬럼'):
        validate_schema(pd.DataFrame({'title':['A']}))
def test_quality_counts():
    df=load_data(str(DATA_FILE),DATA_FILE.stat().st_mtime_ns)
    result=quality_summary(df)
    assert result['전체 건수']==len(df)
    assert all(isinstance(v,int) for v in result.values())
