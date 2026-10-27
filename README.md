# 전남 관광 대시보드 V2

실제 관광 데이터 CSV를 기반으로 만든 Streamlit 관광 분석 웹앱입니다.

## 구조

- `app.py` — 진입점: 로딩 → 세션 → 필터 → 화면 실행
- `config.py` — 경로 / 관광분류 / 기본 필터 / CSS / 맛집 검색 설정
- `data_service.py` — Streamlit 캐시 어댑터
- `services/tour_data.py` — UI와 분리된 CSV 정규화·검색·정렬·필터
- `services/restaurant_api.py` — 카카오 로컬 음식점 반경 검색
- `services/restaurant_search.py` — 네이버·카카오 지도 검색 링크 생성
- `state.py` — 세션 초기화, 전체 필터 초기화, 즐겨찾기와 관광지 선택
- `filters.py` — 사이드바 위젯
- `views.py` — 지표·차트·품질 점검·다운로드
- `services/validation.py` — 필수 컬럼, 좌표 및 품질 점검
- `services/statistics.py` — 집계
- `components/map_view.py` — Folium 마커클러스터·팝업 지도
- `components/tour_card.py` — 관광지 카드·즐겨찾기·상세보기
- `tests/test_ui_detail.py` — Streamlit AppTest 상세보기 렌더링 검사
- `tests/` — 자동 테스트
- `data/jeonnam.csv` — 원본 데이터 (수정하지 않음)

## 실행 (VS Code 터미널)

```powershell
pip install -r requirements.txt
streamlit run app.py
```

실시간 주변 음식점 검색에는 카카오 REST API 키가 필요합니다. `KAKAO_REST_API_KEY` 환경 변수 또는 Streamlit Secrets에 설정하면 상세 보기에서 반경을 지정해 음식점을 거리순으로 볼 수 있습니다. 키가 없으면 네이버 지도·카카오맵 검색 링크를 계속 사용할 수 있습니다.

## 테스트

```powershell
pip install -r requirements-dev.txt
python -m pytest -q
```

## 기능

1. 필수 컬럼·사진·지역·좌표·중복 등 품질 점검
2. 관광지 클릭 상세보기 (원본 소개글이 없는 경우 기본 정보만 표기)
3. 관광지명/지역/주소 통합 검색
4. 지도 마커 클러스터, 장소명 툴팁 및 주소 팝업
5. `cat2` 세부분류
6. 이름 오름/내림차순, 지역명, 등록일 정렬
7. `st.session_state` 즐겨찾기·관광지 선택 상태 (브라우저 연결 종료 후 영구 유지하지 않음)
8. CSV mtime 기반 캐시 무효화 (`@st.cache_data`)
9. 카드와 테마 CSS, 2열 차트·지도 배치
10. pytest 데이터·필터·지도좌표 테스트
11. 선택 관광지 좌표 기준 음식점 반경 검색 (카카오 로컬 API 키 필요)
12. 새로운 관광 분류 코드도 코드와 함께 화면에 표시

## 주의사항

- 지도좌표 검증은 넓은 경위도 영역 검사입니다. **정확한 행정경계 검증은 아닙니다.**
- 즐겨찾기는 데이터베이스에 저장하지 않으며 브라우저 세션 동안만 유지됩니다.
- 원본 데이터에 관광지 상세 본문이 없을 수 있어 별도의 설명을 지어내지 않습니다.
- 이미지 URL이 없는 장소는 안내 문구로 대체됩니다.
- 사진 외부 호스팅이 차단되면 이미지가 표시되지 않을 수 있습니다.

## GitHub / Streamlit Cloud

전체 폴더를 GitHub 저장소 루트에 커밋하고 Streamlit Community Cloud에서 `app.py`를 메인 파일로 선택합니다.
민감한 API 키 등은 GitHub에 올리지 말고 앱의 Secrets에 저장하세요.

## 확장 자동 테스트 (V2 테스트 보강)
- 자세한 내용: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- 설치: `python -m pip install -r requirements-dev.txt`
- 실행: `python -m pytest -q`
- 커버리지: `python -m pytest --cov=data_service --cov=state --cov=services --cov-report=term-missing`
- 커버리지 측정은 명령에 지정된 모듈만 포함합니다. AppTest 상세보기 테스트는 별도로 실행됩니다.

## 보안 및 이메일 개인정보 보호

API 키 저장 방법, 로컬 Git 작성자 이메일 설정과 자동 보안 검사는 [SECURITY.md](SECURITY.md)를 참고하세요. 실제 비밀값은 소스에 넣지 않습니다.
