# 테스트·운영·보안 리뷰 (2026-07-30)

대상 커밋: `d0a29b7` (`refactor/sync-docs`)

## 1. 테스트

### 1.1 테스트 구성

| 계층 | 위치 | 규모 | 실행 주체 |
|---|---|---|---|
| Python 단위 | `translation-sync/tests/test_*.py` | 16개 파일 / **실측 771 tests** | `make translation-test` ← `make check`(pre-commit), `make translation-check`(sync workflow) |
| Node 단위 | `translation-sync/scripts/markdown-link-utils.test.mjs` | 1개 파일 / 1 test | `npm run test:markdown-links` ← `make site-test` ← `make site-check` |
| 브라우저 E2E | `e2e/*.spec.ts` | 7개 파일 / `test(` 정의 85개 / **실행 시 98 tests**(반응형 루프로 확장) | **수동만** (`npm run test:e2e`) |
| 통합 게이트 | `replay.py`, `provider_check.py`, `validate_generated_changes.py` | - | Makefile / sync workflow |
| corpus 자기검사 | `main.py --check-annotations` | - | **연결된 실행 주체 없음** |

### 1.2 핵심 기능의 테스트 여부

테스트가 실제로 방어하는 위험(확인됨):

- **파일 손상·경로 이탈**: `test_annotate.py`(심링크 locale root/버전 root/문서, 경로 이탈), `test_upstream.py`(`os.replace` 실패 시 캐시 보존, 임시 파일 잔재 없음), `test_files.py`(fsync 순서 file→directory, 하드링크 다른 이름 불변)
- **커밋 범위**: `test_generated_changes.py`(산출 경로 allowlist, malformed git name-status 거부, 심링크 leaf/ancestor 거부)
- **provider 계약**: `test_translate.py`(429/5xx/네트워크만 재시도, model·auth 오류 즉시 중단, 잘린 OpenAI/Azure 응답 거부, sleep 주입으로 결정적)
- **격리 replay**: `test_replay.py`(외부 manifest 스테이징, 인터럽트 시 미생성, cleanup 실패 시 export 차단, active worktree fingerprint)
- **크로스 스택 버전**: `test_files.py:55-67`(`package.json`의 Playwright 핀 ↔ `Dockerfile.playwright` ARG)
- **렌더링 계약(E2E)**: `docs-rendering.spec.ts`(앵커 매핑, `{{version}}` 잔존, admonition 변환, 사이드바 영문 label, JA 배너 부재, `/en` 404, 버전별 렌더)

이 구성은 "테스트 수"가 아니라 **파괴적 실패**를 겨냥한다. 이 프로젝트 목적 기준으로 올바른 설계다.

### 1.3 누락된 주요 시나리오

| 누락 | 근거 | 영향 |
|---|---|---|
| annotation corpus 회귀 게이트 | `--check-annotations`가 Makefile·workflow 미연결 | 실제로 master 11건 / 13.x 12건 실패 중인데 아무도 감지하지 않는다 |
| `src/remark/*` 7개 변환 플러그인 단위 테스트 | 테스트 파일 없음 | 빌드 성공만으로 통과하고, 변환 회귀는 E2E에만 의존(그 E2E는 CI 미연결) |
| `validate-anchors.mjs` 자체 테스트 | 없음 | 사이트 게이트의 최종 방어선인데 자기 검증이 없다 |
| `sync-versioned-links.mjs`, `create-latest-doc-redirects.mjs` | 없음 | prebuild/postbuild에서 산출물·tracked 파일을 변경하는데 무테스트 |
| JA 로케일 E2E | `docs-rendering.spec.ts` 2건뿐, 나머지 spec은 모두 KO(`/`) 기준 | 발행 중인 JA 홈·네비·푸터 회귀가 무방비 |
| 비앵커 깨진 링크 | `validate-anchors.mjs`가 `#` 없는 링크를 skip, `onBrokenLinks: 'warn'` | 문서 사이트의 1차 실패 모드에 게이트가 없다 |
| 콘솔 에러·JS 예외·접근성 | E2E 전수에 단언 없음 | 런타임 오류가 조용히 배포된다 |

### 1.4 테스트 실행 가능 여부

재현 가능하다(확인됨). `uv sync --locked`, `npm ci`, Playwright 정확 버전 핀으로 환경이 고정된다. 이번 리뷰에서 모든 테스트를 실제로 실행했다(§4 참조).

단 결함이 하나 있다. `test_files.py:56-67`이 저장소 루트의 `package.json`과 `Dockerfile.playwright`를 읽는데, `Dockerfile.translate:20-26`은 두 파일을 복사하지 않는다. 따라서 **번역 Docker 이미지 안에서는 전체 스위트가 통과할 수 없다**(확실성: 확인됨 — 코드 기반. 컨테이너 실제 실행은 미수행).

### 1.5 테스트 신뢰성

- 강점: 재시도 테스트가 `sleep`을 주입해 실제 대기가 없다. 대소문자 비구분 파일시스템은 명시적 `skipTest`로 분기한다.
- 약점: `e2e/docs-rendering.spec.ts:124`의 `page.waitForTimeout(3500)` 고정 대기는 시간 기반 flake 소스다. CI `retries: 2`가 이를 은폐할 수 있다(다만 CI에서 E2E가 실행되지 않으므로 현재는 무관).
- 약점: `e2e/build.spec.ts`는 브라우저를 쓰지 않고 `build/` 존재만 확인한다. `playwright.config.ts:30`의 webServer가 `npm run build`를 선행하므로 사실상 동어반복이다.
- 약점: `test_replay.py:33-43`이 workflow YAML을 문자열 들여쓰기로 파싱해 형식 변경에 취약하다. 또한 검증 대상은 preflight 스텝 하나뿐이다.

### 1.6 테스트와 실제 요구사항의 일치 여부

**평가: 대체로 적절** — 단위 테스트는 요구사항(구조 보존, 경로 안전, provider 계약)과 정확히 정렬된다.

그러나 문서화된 테스트 목록은 코드와 불일치한다. `e2e/TEST_LIST_HOMEPAGE.md`는 78개를 주장하나 정의는 20개이며, 문서가 "검증한다"고 적은 UI를 코드는 "없어야 한다"고 단언한다(상세는 02 문서 참조).

## 2. 운영

### 2.1 환경별 설정

| 항목 | 로컬 호스트 | 로컬 Docker | CI |
|---|---|---|---|
| 번역 실행 | `make translation-run` | `make translate` | `sync-translation.yml` |
| 비밀 공급 | process env (`config.py`는 `os.environ`만) | `translation-sync/.env`(compose `env_file`) | GitHub Secrets → step env |
| upstream SHA 고정 | `MANIFEST` 수동 지정 | **불가** (전달 경로 없음 → 항상 브랜치 HEAD) | preflight가 생성 후 live run이 재사용 |
| 통과 게이트 | 사용자가 선택 | **없음** | preflight → provider-check → run → site-check → artifact-check |

같은 이름의 기능이 세 경로에서 결정성과 안전망이 다르다. `make translate`는 게이트 없이 bind mount된 `versioned_docs`/`i18n`에 직접 결과를 쓴다(확인됨).

### 2.2 빌드와 배포

- 게이트 순서(확인됨): preflight → live provider 계약 → 번역 → `site-check` → 산출 경로 → commit → push → (main만) deploy dispatch. **순서 자체는 목적에 정확히 부합한다.**
- 재현성: 모든 GitHub Action이 커밋 SHA로 핀되어 있다. `uv sync --locked`, `npm ci`로 잠금 설치.
- 결함: `deploy.yml:53`의 `make site-check`에는 `NODE_OPTIONS` heap 확장이 없다. `sync-translation.yml:113`과 `Dockerfile`에는 있다. **동일 게이트가 배포 경로에서만 다른 조건으로 돈다.**
- 결함: 4개 workflow 전부 `timeout-minutes`가 없다(grep 0건). provider 지연 시 GitHub 기본 6시간까지 점유될 수 있고, `concurrency: cancel-in-progress: false`와 결합하면 다음 스케줄이 대기한다.

### 2.3 데이터베이스 마이그레이션

해당 없음(확인됨). DB·캐시·오브젝트 스토리지·백엔드 런타임이 존재하지 않는다. 영속 상태는 (a) git 저장소 콘텐츠, (b) 실행 중 `runner.temp`의 upstream manifest JSON, (c) 로컬 Playwright docker volume뿐이다.

따라서 "데이터 손실" 위험은 **잘못된 커밋/배포**로 환원되며, 방어가 커밋 전 게이트에 집중된 설계는 타당하다.

### 2.4 로그와 모니터링

**평가: 부분적으로 부적절**

- 애플리케이션 로그는 전부 `print`(stdout/stderr)다. 재시도 횟수·지연·토큰·latency 기록이 없다.
- workflow에 `if: failure()` 알림 step이 없다. 로그·manifest artifact 업로드도 없다. manifest는 job 로그에 `cat`으로만 남는다.
- 실패 탐지가 사람의 수동 관찰에 의존한다. 격일 스케줄이므로 실패를 며칠 뒤 발견할 수 있다.

### 2.5 장애 대응 가능성

- fail-fast는 명시적 정책이다(`Makefile`의 `--fail-fast`, `translation-sync/docs/00` A군 표). 실패 시 커밋을 생략해 잘못된 산출물이 원격에 반영되지 않는다. 안전 우선으로 타당하다.
- 그러나 run 단위 트랜잭션이 없다. 로컬 직접 실행은 실패 전 기록된 파일이 worktree에 남는다(문서가 인지·명시).
- 삭제(`D`) 처리가 루프 초반에 즉시 `unlink`된다(`main.py:901-909`). 이후 다른 문서가 실패해도 로컬 삭제는 남는다.

### 2.6 외부 서비스 장애 처리

| 상황 | 처리 | 평가 |
|---|---|---|
| 네트워크/429/5xx | 최대 3회, 300초 고정 간격 | 대체로 적절 (백오프·jitter 없음) |
| API 부분 응답 | `status != completed` / `finish_reason != stop` → 저장 없이 실패 | 적절 |
| CLI 비일시 오류 | 즉시 실패 + stderr 진단 | 설계는 적절, 단 분류가 문서 본문에 오염될 수 있음(03 문서 참조) |
| SDK 자체 재시도 | `max_retries=0`으로 비활성화, 재시도 소유권을 앱이 가짐 | 적절 |
| upstream clone 실패 | 3회 재시도, 300초 timeout | 적절 |

### 2.7 롤백과 복구 가능성

**평가: 부분적으로 부적절**

- 롤백 workflow가 없고 문서에도 절차가 없다(전수 확인). 복구 수단은 revert 커밋 + `deploy.yml` 수동 dispatch뿐이다.
- `deploy.yml`의 `cancel-in-progress: true`는 연속 push나 sync의 deploy dispatch와 겹칠 때 진행 중 배포를 취소한다. Pages 배포는 원자적이라 사이트 파손보다 **배포 누락**으로 나타나며 자동 재시도가 없다.
- 권장: `workflow_dispatch(ref)`로 임의 커밋을 재배포하는 rollback workflow 추가, 배포 job은 `cancel-in-progress: false`.

## 3. 보안

### 3.1 인증과 인가

**평가: 적절**

- `checkout`이 write credential을 남기지 않는다(`persist-credentials: false`). 의존성 설치·번역·검증·훅 단계에 push 자격증명이 없고, **push step에서만** `gh auth setup-git`을 호출한다.
- provider 비밀은 `translation-provider-check`와 `translation-run` **두 step에만** 주입된다. preflight·site-check·artifact-check·commit/push에는 주입되지 않는다.
- `deploy.yml`은 `contents: read` + `pages: write` + `id-token: write`로 최소 권한이며 `main` 브랜치 가드가 있다.

결함: `sync-translation.yml`의 sync job에는 `environment:`가 없다. `workflow_dispatch`는 임의 브랜치에서 그 브랜치의 workflow 정의로 실행되며 `contents: write` + 전체 provider 비밀을 사용한다(High).

### 3.2 입력값 검증

**평가: 적절**

- upstream URL은 코드 상수다(사용자 입력 아님).
- `version`은 `versions.json` 목록과 대조되고 정규식(`^(?:master|(?:0|[1-9]\d*)\.x)$`)으로 제한된다.
- `doc`은 `Path(doc).name == doc`과 `.md` 확장자로 제한된다.
- 목적지 경로는 symlink 성분과 저장소 이탈을 거부한다(`_version_destination`, `_document_destination`, `main.py:_validated_output_path`).
- manifest는 저장소 일치와 40자 hex commit 정규식으로 검증된다.
- workflow input은 env 경유로 인용되어(`"$VERSION"`) 셸 주입 표면이 좁다.

### 3.3 비밀 정보 관리

- `.gitignore`가 `.env`·키·인증서 경로를 광범위하게 무시하고, `.dockerignore`가 이미지에서 `.env`류를 제외한다.
- `translate.py:84-95`의 `_SENSITIVE_ENVIRONMENT_KEYS` + `_provider_error_message()`가 예외 메시지의 실제 비밀 값을 `[REDACTED:KEY]`로 치환한다.
- `provider_check.py`는 provider·model·reasoning·prompt SHA-256만 출력하고 비밀은 출력하지 않는다.

**[High] 다만 저장소 작업 디렉터리에 실제 형태의 API 키가 평문 파일로 존재한다**(`.env`와 동일 내용의 `dot_env`). git 추적·커밋 이력은 없음이 확인됐다(`.gitignore` 적용). 값은 이 문서에 포함하지 않는다. 권장: 키 로테이션과 저장 위치(비밀 관리자 또는 OS keychain) 재검토, `dot_env` 사본 제거.

### 3.4 민감 정보 로깅

- 예외 메시지는 마스킹된다.
- 비밀이 아닌 설정값(`TRANSLATION_PROVIDER`, `TRANSLATION_MODEL`, `TRANSLATION_REASONING_EFFORT`)이 Secrets로 주입되어 로그에서 마스킹된다. 실행 조건 추적이 어려워지므로 `vars.*`로 옮기는 것이 낫다(Medium).

### 3.5 외부 요청 및 파일 처리

- Codex CLI는 저장소 밖 임시 디렉터리에서 `--ignore-user-config --ignore-rules --ephemeral --strict-config --sandbox read-only`로 실행되며 browser·shell·plugin·web search 등 19종이 비활성화된다. child에는 allowlist env만 전달하고 모델의 subprocess 환경 상속은 `none`이다.
- `serve-build.mjs`는 decode → normalize → 상위 경로 제거 후 root prefix를 검사하고 GET/HEAD만 허용한다.

### 3.6 데이터 접근 제어

산출 경로 allowlist(`validate_generated_changes.py:17-31`)가 커밋 직전에 fail-closed로 동작한다. 허용 경로는 `i18n/en`, `i18n/ja`, `versioned_docs`, `versioned_sidebars`, locale sidebar JSON뿐이다. untracked 파일까지 검사 대상에 포함한다.

### 3.7 위험한 기본 설정

### [High] 에이전트 런타임 권한이 사실상 무제한이다

- 관련 경로: `.claude/settings.json`(`"defaultMode": "bypassPermissions"`, `"skipDangerousModePermissionPrompt": true`), `.codex/config.toml`(`approval_policy = "never"`, `web_search = "live"`)
- 확인 내용: 유일한 방어선인 `.hooks/*.sh`는 정규화된 명령 문자열 grep 휴리스틱이다. `pre_tool_use_common.sh:3`의 `HOOK_COMMAND_BOUNDARY='(^|[;&|][[:space:]]*)'` 경계는 `bash -lc "git push"` 같은 래핑을 포착하지 못할 수 있다.
- 영향: 이 저장소에서 가장 넓은 권한 표면이다. 에이전트가 잘못 동작하면 저장소·로컬 환경 변경을 막을 실질 게이트가 없다.
- 권장: 명령 파싱 기반 훅 또는 승인 모드 복원.
- 확실성: 확인됨(설정). 훅 우회 가능성은 [INFERENCE] — 실제 우회를 시도하지 않았다.

### 3.8 기타 보안 항목

- **[Medium] 보안 스캔 자동화 없음**: CodeQL·gitleaks·trivy·semgrep·`npm audit`·osv 설정이 전무하다.
- **[Medium] Dependabot 커버리지 공백**: `github-actions`와 `npm`만 등록. `uv.lock`(openai 등)과 Docker 베이스 이미지는 수동 관리 대상이다.
- **[Medium] 컨테이너 digest 미고정**: `node:26-alpine`, `python:3.14-slim`, `node:26-bookworm`이 태그 핀만 사용한다. `Dockerfile.playwright`는 빌드 시 네트워크 설치를 수행한다.
- **[High] `make claude`의 원격 지시문 주입**: 서드파티 저장소 `main` 브랜치의 파일을 `curl`로 받아 체크섬 검증 없이 tracked `AGENTS.md`에 append하며, `make dev`에 포함된다. `AGENTS.md`는 에이전트 시스템 지시문이므로 상류 변경이 곧 지시문 변경이다. 권장: 커밋 SHA 고정 + 체크섬 검증 또는 벤더링.
- **[Low] CODEOWNERS 부재**: 리뷰 소유권이 코드로 표현되지 않는다.

## 4. 실행 검증 결과

이번 리뷰에서 직접 실행한 결과다.

| 검증 항목 | 실행 명령 | 결과 | 주요 내용 | 비고 |
|---|---|---|---|---|
| 의존성 확인 (Python) | `uv sync --locked --python 3.14` | 성공 | 16 packages | lockfile 일치 |
| 의존성 확인 (Node) | `npm ci` | 성공 | 1282 packages | install script 미승인 경고 3건 |
| 린트 (Python, 참고) | `uvx ruff check .` | **실패 (exit 1)** | 159 errors 보고 (81건 자동 수정 가능). 그중 `patch.py`의 `DiffLine` 미import(F821)는 룰셋과 무관한 실제 타입 결함 | **프로젝트가 채택한 게이트가 아니다.** ruff 설정 파일이 없고 Makefile·workflow에 Python lint 참조 0건. 따라서 159건을 "코드 결함 수"로 취급하지 않고, 유효한 발견은 게이트 부재 자체로 기록한다 (03 문서 §10) |
| 린트 (Node/TS) | — | 해당 없음 | ESLint 설정 없음 | 저장소에 lint 도구 부재 |
| 타입 검사 | `npm run typecheck -- --pretty false` | **성공** | 오류 0 | `strict` 미설정 |
| 단위 테스트 (Python) | `PYTHONPATH=. python -m unittest discover -s tests` | **성공** | **Ran 771 tests — OK** | 21.2초 |
| 단위 테스트 (Node) | `npm run test:markdown-links` | **성공** | 1 pass / 0 fail | |
| 통합 검증 | `make translation-check` | **성공** | 771 tests + identity replay 수렴 | 외부 API 미사용 |
| 빌드 | `npm run build` | **성공** | KO/JA 빌드 + redirect 101개 | 615초. 최초 1회는 `npm ci`와 동시 실행으로 모듈 교체 경쟁이 발생해 실패 → 설치 완료 후 재실행하여 성공 (환경 문제) |
| 앵커 검증 | `npm run validate-anchors` | **실패** | 46,626개 중 **JA 15개 `id not found`** | 성공한 빌드 산출물 기준으로 재실행한 결과. 예: `#actions-handled-by-resource-controller`(실제 id는 복수형) |
| 브라우저 E2E | `PLAYWRIGHT_REUSE_SERVER=1 npm run test:e2e` | **성공** | **98 passed** (정의 85개 + 반응형 루프 확장) | 성공한 빌드 산출물 서버에서 실행 |
| 산출 경로 검사 | `make translation-artifact-check` | 실패 | untracked 3건(`.docs/review/*` 2건, `translation-sync/.coverage`) | **코드 결함 아님.** `.gitignore` 미등록 항목 때문. 이번 리뷰 산출물(`docs/review/*`)도 allowlist 밖이라 동일하게 실패한다 |
| corpus 자기검사 (master) | `main.py --check-annotations --version master` | **실패** | 11건 (`legacy note marker`, `source comment mismatch`, `missing original comment`, `untranslated source text`) | 어떤 게이트에도 미연결 |
| corpus 자기검사 (13.x) | `main.py --check-annotations --version 13.x` | **실패** | 12건 (동일 계열) | 동일 |
| 문서 빌드 | — | 해당 없음 | 별도 문서 빌드 파이프라인 없음 | 문서는 Markdown 원본으로 관리 |
| live provider 계약 | `make translation-provider-check` | **미실행** | — | 외부 유료 API 호출을 피하기 위해 이번 회차에서는 실행하지 않음 |
| live 번역 실행 | `make translation-run` | **미실행** | — | 저장소 문서를 실제로 수정하므로 금지 대상 |
| E2E 컨테이너 | `npm run test:e2e:docker` | **미실행** | — | 컨테이너 빌드 비용. 호스트 E2E로 대체 |

### 4.1 실패 원인 판단 (환경 문제 vs 코드/데이터 문제)

| 실패 | 판단 |
|---|---|
| `validate-anchors` JA 15건 | **데이터 문제** — JA 문서에 KO에는 있는 alias anchor가 없다. validator 자체는 정상 동작 |
| `--check-annotations` 23건 | **데이터 문제** — 강화된 verifier 기준에 맞춰 corpus migration이 완료되지 않았다 |
| `translation-artifact-check` | **환경 문제** — 로컬 untracked 파일. CI는 새 checkout이므로 영향 없음. 단 `.gitignore` 보강이 필요한 로컬 게이트 견고성 문제 |
| 최초 `npm run build` 실패 | **환경 문제** — `npm ci`와 동시 실행으로 `markdown-extensions` 모듈이 교체되는 중이었다. 설치 완료 후 재실행하여 성공 |
| 최초 `npm run test:e2e` 실패 | **환경 문제** — 위 빌드 실패의 파생(webServer가 `npm run build`를 선행). 성공한 빌드에서 재실행하여 98 passed |

## 5. 종합 평가

| 영역 | 평가 | 근거 |
|---|---|---|
| 테스트 설계·위험 정렬 | 적절 | 파일 손상·경로 이탈·provider 계약을 정면으로 방어. 771 tests 실측 통과 |
| 테스트 게이트 배치 | **부적절** | PR에서 실행되는 테스트가 0건. E2E 98개가 CI 미연결. `--check-annotations`는 실행 주체 없음 |
| 정적 분석 | 부분적으로 부적절 | Python lint·type 게이트 부재, TS `strict` 미설정 |
| 환경 구분·재현성 | 대체로 적절 | 버전 핀 일관. 단 번역 실행 3경로의 계약이 다르고 `deploy.yml`만 `NODE_OPTIONS` 누락 |
| 관측성 | 부분적으로 부적절 | print 기반, 실패 알림·artifact 업로드 없음 |
| 롤백·복구 | 부분적으로 부적절 | 롤백 workflow·절차 없음, 배포 취소 위험 |
| 인증·인가·비밀 관리 | 적절 | 최소 주입, credential 분리, redaction, 경로 allowlist |
| 입력 검증 | 적절 | 상수 URL, 화이트리스트, symlink 거부, 인용된 셸 변수 |
| 에이전트 런타임 보안 | **부적절** | 승인 게이트 해제 + 휴리스틱 훅 |
| 공급망 보안 | 부분적으로 부적절 | Action SHA 핀은 우수. 스캔 자동화 부재, Dependabot·digest 공백 |
