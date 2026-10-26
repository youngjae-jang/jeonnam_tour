from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'jeonnam.csv'
DEFAULT_FILTERS = {'regions': [], 'categories': [], 'subcategories': [], 'keyword': '', 'sort_option': '기본순', 'show_n': 9, 'favorites_only': False}
CATEGORY_NAMES = {'A01': '자연 관광', 'A02': '인문·문화 관광'}
SUBCATEGORY_NAMES = {'A0101':'자연경관', 'A0102':'자연생태', 'A0201':'역사관광', 'A0202':'휴양관광', 'A0203':'체험관광', 'A0204':'산업관광', 'A0205':'건축·조형', 'A0206':'문화시설', 'A0207':'축제·공연', 'A0208':'레포츠'}
SORT_OPTIONS = ['기본순', '관광지명 오름차순', '관광지명 내림차순', '지역명순', '등록일 최신순']
RESTAURANT_RADIUS_DEFAULT = 1000
RESTAURANT_RADIUS_MAX = 20000

def get_restaurant_api_key(secrets=None):
    """Read the optional Kakao key from Streamlit secrets or the process environment."""
    try:
        secret_key = secrets.get('KAKAO_REST_API_KEY', '') if secrets is not None else ''
    except Exception:
        secret_key = ''
    return secret_key or os.getenv('KAKAO_REST_API_KEY', '')

def category_label(code):
    """Keep newly encountered category codes visible instead of hiding them as generic data."""
    value = '' if code is None or str(code).lower() in {'nan', '<na>', 'none'} else str(code).strip()
    return CATEGORY_NAMES.get(value, f'미분류 ({value})' if value else '미분류')

def subcategory_label(code):
    """Show unknown subcategory codes so new source categories remain identifiable."""
    value = '' if code is None or str(code).lower() in {'nan', '<na>', 'none'} else str(code).strip()
    return SUBCATEGORY_NAMES.get(value, f'미분류 ({value})' if value else '분류 미상')

STYLE = '''<style>.stApp{background:#f2f8fb}.block-container{padding-top:1.8rem;max-width:1420px}h1,h2,h3{color:#075174}[data-testid="stMetric"]{background:#fff;border:1px solid #d4e5ef;border-radius:14px;padding:16px}[data-testid="stSidebar"]{background:#e9f3f9}</style>'''
