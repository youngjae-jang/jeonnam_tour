# 보안 및 이메일 개인정보 보호

## 키 저장

실제 API 키는 GitHub 소스에 넣지 않습니다. 현재 앱은 프로세스 환경변수 또는 Streamlit Secrets의 `KAKAO_REST_API_KEY`를 읽습니다.

- 로컬: `.streamlit/secrets.toml.example`을 `.streamlit/secrets.toml`로 복사한 뒤 값을 입력합니다.
- Streamlit Cloud: 해당 앱의 Secrets에서 값을 설정합니다.
- `.env.example`은 설정 이름을 안내하는 빈 예제입니다. 앱은 `.env`를 자동 로드하지 않습니다.
- `.gitignore`는 로컬 비밀파일·개인키·캐시·테스트 산출물을 제외합니다. 이미 추적 중인 파일에는 무시 규칙만 추가해도 적용되지 않으므로 저장 전에 `git status`를 확인합니다.

## 앞으로의 커밋 이메일

GitHub 웹 설정의 **Emails**에서 다음을 활성화합니다.

1. **Keep my email addresses private**
2. **Block command line pushes that expose my email**

VS Code 터미널에서 이 프로젝트 폴더를 연 뒤 다음을 실행합니다. 이 명령은 현재 저장소의 로컬 설정만 바꿉니다.

```powershell
git config --local user.email "67226437+youngjae-jang@users.noreply.github.com"
git config --local --get user.email
```

GitHub 계정의 이메일 설정은 로컬 Git 설정을 자동 변경하지 않습니다. 새 PC나 다른 저장소에서는 작성자 설정을 다시 확인합니다. 과거 커밋의 이메일도 자동 제거되지 않습니다. 과거 이력 재작성은 별도 검토·승인 후 진행합니다.

CI의 `Commit email privacy`는 PR·main push에 새로 포함된 커밋의 작성자 주소가 GitHub noreply인지 검사하며 실제 주소를 로그에 출력하지 않습니다. 이미 공개 브랜치에 push한 이메일 노출을 되돌리지는 못하므로 위 GitHub 설정과 로컬 설정을 함께 사용합니다.

## 자동 검사와 main 보호

`Security checks`는 다음 검사를 수행합니다.

- `Repository hygiene`: 비밀파일·자동 생성 파일이 Git에 추적되는 것을 차단합니다. 파일 내용은 출력하지 않습니다.
- `Commit email privacy`: 새 커밋의 작성자 주소를 확인합니다. 과거 공개 이력은 변경하지 않습니다.
- `Secret scan`: SHA256으로 검증한 고정 버전 Gitleaks의 기본 규칙과 카카오 REST API 키 규칙을 사용합니다. 전체 가져온 Git 이력을 검사하고 검출값은 모두 가립니다. 실제 키 없이 합성 입력으로 검출·마스킹 기능도 검증합니다.

GitHub의 **Advanced Security**에서 Secret scanning과 Push protection 상태를 확인합니다. 이 저장소의 관리자가 활성화 상태를 확인해야 하며, 워크플로 파일을 추가하는 것만으로 GitHub 설정이 바뀌지는 않습니다.

`main`에는 PR을 통한 변경과 아래 검사 통과를 필수로 설정합니다. 보호 설정은 **Settings → Branches** 또는 **Rules → Rulesets**에서 별도로 적용합니다.

- `pytest (Python 3.11)`
- `pytest (Python 3.12)`
- `Repository hygiene`
- `Commit email privacy`
- `Secret scan`

강제 push와 브랜치 삭제를 허용하지 않습니다. 저장소 소유자 혼자 운영하는 경우 다른 사람의 승인을 필수로 요구하지 않아도 PR과 자동 검사는 필수로 유지할 수 있습니다.

## 키가 실제로 노출된 경우

1. 서비스 제공처에서 노출된 키를 먼저 폐기·재발급합니다.
2. 새 키는 실행 환경의 비밀값으로만 저장합니다.
3. 소스·로그·첨부파일·Git 이력의 영향 범위를 확인합니다.
4. 필요한 과거 이력 정리는 별도 승인 후 수행합니다. 최신 파일만 지워도 이전 커밋에 값이 남을 수 있습니다.

보안 문제를 공개 이슈나 PR에 알릴 때 실제 키, 개인 이메일, 전화번호를 붙여 넣지 않습니다. 파일 경로와 값이 가려진 설명만 사용합니다.
