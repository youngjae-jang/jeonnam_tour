# 전남 관광 대시보드 V2 — 자동 테스트 설명서

## 1. 목적
코드가 바뀌어도 기존 필터, 검색, CSV 전처리, 지도 좌표 검사, 통계, 세션 관리가 예상대로 동작하는지 검사합니다.

## 2. 실행
프로젝트 최상위 폴더에서 다음 명령을 실행합니다.

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pytest -v
python -m pytest --cov=data_service --cov=state --cov=services --cov-report=term-missing
```

## 3. 테스트 구성
| 파일 | 내용 |
| --- | --- |
| `tests/conftest.py` | 재사용 가능한 `sample_tours` 데이터와 격리된 `fresh_session` fixture. Streamlit 미설치 환경에서만 최소 대역 사용 |
| `tests/test_filters.py` | 기존 실제 CSV 기반 회귀 테스트 6개 |
| `tests/test_validation.py` | 기존 검증 테스트 2개 |
| `tests/test_filters_extended.py` | 지역/유형/세부분류, 조합 필터, 검색, 즐겨찾기, 정렬, 집계 테스트 |
| `tests/test_state.py` | 상태 초기화·기존 값 보존·필터 리셋·즐겨찾기 토글·선택 관광지 테스트 |
| `tests/test_validation_extended.py` | 필수 컬럼별 예외, 좌표 경계/NaN/0, 품질 요약 및 빈 데이터 테스트 |
| `tests/test_data_loading.py` | CSV 파일 생성·로딩·전처리·누락 컬럼·잘못된 좌표·사진 URL·인코딩 대체 처리 테스트 |

## 4. 테스트 원리
`test_`로 시작하는 함수는 pytest가 자동 수집합니다. 각 테스트는 대상 함수를 호출한 다음 `assert`로 예상 결과를 검증합니다. `@pytest.mark.parametrize`는 하나의 테스트 함수에 여러 입력을 자동 대입하므로 테스트 개수가 증가합니다. `tmp_path`는 임시 CSV 파일을 만들고 자동 정리합니다. `monkeypatch`로 세션을 격리해 테스트끼리 간섭하지 않도록 합니다.

## 5. 기준 결과
- 전체 53개 통과 (2026-10-24, 실행 환경 Python 3.13)
- `data_service.py`, `state.py`, `services/`의 **측정된 문장 커버리지 100%**
- 해당 수치는 지정한 순수 로직 모듈만 포함하며 Streamlit 화면, 지도 UI, 실제 브라우저 클릭 및 네트워크를 테스트하지 않습니다.
- 기존 프로젝트 구현 로직은 변경하지 않았습니다.

## 6. 새로운 기능 추가 시
1. 기대하는 입출력과 경계 사례를 결정합니다.
2. 관련 `tests/test_*.py`에 fixture와 test 함수를 추가합니다.
3. `python -m pytest -q`로 전체 회귀 테스트를 실행합니다.
4. 실패 원인이 기대값 오류인지 실제 코드 문제인지 구분합니다.
5. Streamlit 웹 화면에서 버튼/지도/이미지까지 수동으로 확인합니다.

## 7. 향후 추가 테스트
Streamlit `AppTest`를 활용한 렌더링·위젯 상태 테스트, Folium 지도 팝업의 통합 테스트, GitHub Actions CI를 추가할 수 있습니다. 현재 번들은 화면 테스트가 없는 단위/데이터 회귀 테스트입니다.
