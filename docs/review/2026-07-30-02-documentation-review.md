# 문서 리뷰 (2026-07-30)

대상 커밋: `d0a29b7` (`refactor/sync-docs`)
대상: 사람이 작성한 문서 전량. 자동 생성 산출물(`versioned_docs`, `i18n/**` 번역 본문, `.docusaurus`)은 제외.

## 1. 문서 목록과 문서별 역할

| 문서 | 역할 | 독자 | 상태 |
|---|---|---|---|
| `README.md` | 저장소 진입점: 소개, 실행, 문서 갱신, 라이선스 | 사용자·기여자 | 운영 중 (오류 포함) |
| `translation-sync/docs/00-workflow-summary.md` | 파이프라인 사양 허브 (단계 순서, 기술 기준, 재시도, git 반영) | 운영자·에이전트 | 운영 중 |
| `translation-sync/docs/01-preprocessing.md` | 전처리 계약 | 개발자 | 운영 중 |
| `translation-sync/docs/02-translation.md` | 번역 소유 단위·청크·provider 계약 | 개발자 | 운영 중 |
| `translation-sync/docs/03-postprocessing.md` | 후처리 계약 | 개발자 | 운영 중 |
| `translation-sync/docs/04-verification.md` | 검증 계약 (`response_contract` vs `verify` 역할 분리) | 개발자 | 운영 중 |
| `translation-sync/docs/05-additional-work.md` | 전체 운영 기준 (데이터 경로, 사이드바 정책, 검증·산출·git 기준) | 운영자 | 운영 중 |
| `translation-sync/docs/06-sidebar-sync.md` | 사이드바 재생성 계약 | 개발자 | 운영 중 |
| `translation-sync/docs/07-local-replay.md` | 격리 replay 계약, 종료 코드 | 개발자 | 운영 중 |
| `translation-sync/docs/08-error-cases.md` | 리팩터링 이전 실패 사례 이력 | 개발자 | **이력** (문서 스스로 명시) |
| `translation-sync/prompt.md`, `prompt_jp.md` | 운영 프롬프트 (데이터) | LLM | 운영 중 |
| `.github/docs/branch-name-guide.md` | 브랜치 규칙 | 기여자 | 운영 중 (orphan) |
| `.github/docs/pull-request-guide.md` | PR 규칙 | 기여자 | 운영 중 (orphan) |
| `.github/docs/repository-copilot-guide.md` | Copilot MCP 설정 | 기여자 | 참고 (orphan) |
| `.husky/docs/commit-message-guide.md` | 커밋 메시지 규칙 | 기여자 | 운영 중 (orphan) |
| `e2e/TEST_LIST_HOMEPAGE.md`, `TEST_LIST_NAV.md` | E2E 테스트 목록 | 개발자 | **구현과 충돌** |
| `SECURITY.md` | 취약점 보고 정책 | 외부 보고자 | **템플릿 미완성** |
| `CODE_OF_CONDUCT.md` | 행동 규약 | 기여자 | 완성 (orphan) |
| `AGENTS.md` | 에이전트 지침 | 에이전트 | 외부 생성물 |
| `.docs/system-prompt.md`, `user-prompt.md`, `prompt.md` | 일회성 세션 계약 | 에이전트 | 일회성 |
| `.docs/review/*.md` (8건) | 리뷰 원장 | 운영자 | 이력 누적 |
| `docs/index.md` | 내용이 문자열 `index.md`인 스캐폴딩 | - | **죽은 파일** |

## 2. 문서 구조 평가

**평가: 부분적으로 부적절**

강점(확인됨):
- `translation-sync/docs`는 단계별로 분리되어 있고 **코드가 문서를 역참조**한다. `main.py:4`→00, `sync/verification/verify.py:1`→04, `sync/sidebar/generator.py:3`→06, `sync/preprocessing/preprocess.py:1`→01. 문서가 장식이 아니라 사양으로 기능한다.
- `08-error-cases.md`는 상단에서 "현재 사양이 아님"을 선언해 이력과 운영 문서를 구분한다. 이는 대부분의 프로젝트가 하지 않는 좋은 관행이다.

약점(확인됨):
- `README.md`가 진입점 역할을 못 한다. `.github/docs`, `.husky/docs`, `SECURITY.md`, `CODE_OF_CONDUCT.md`로의 링크가 0건이다. 훅 실패 메시지도 가이드 경로를 알려주지 않는다.
- 문서가 4개 위치(`translation-sync/docs`, `.github/docs`, `.husky/docs`, `.docs`)에 분산되어 있고 상호 링크가 없다.
- 일회성 세션 문서(`.docs/*`)와 상시 사양이 같은 계층에서 구분 표기 없이 공존한다.

## 3. 정확성 평가

**평가: 부분적으로 부적절** — `translation-sync/docs`는 정확하고, 사이트·기여자 문서 계층은 부정확하다.

일치가 확인된 항목:
- `README.md`가 나열한 Make target 5개(`translation-check`, `translation-provider-check`, `site-check`, `preflight`, `test:e2e:docker`)가 모두 실재하고 구성도 일치한다.
- `README.md` §문서 갱신의 workflow 순서 = `sync-translation.yml` 실제 step 순서(확인됨).
- 런타임 버전: `.nvmrc`=26, `engines >=26 <27`, workflow node 26, `Dockerfile` node:26-alpine, `pyproject` `>=3.14`, `Makefile --python 3.14`, `Dockerfile.translate` python:3.14-slim, uv 0.11.32 — 모두 일치.
- `versions.json` = README "지원 버전" 목록 — 일치.
- `07-local-replay.md`가 "공통 subprocess timeout 없음"을 명시한 것은 코드와 일치한다(정직한 한계 서술).

## 4. 완전성 평가

**평가: 부분적으로 부적절**

포함된 것: 파이프라인 사양, 실행 명령 일부, 브랜치·커밋·PR 규칙, 행동 규약, 데이터 경로 계약, 사이드바 정책, 재시도 정책.

누락된 것(확인됨):
- 일본어 로케일의 존재 자체 (`README.md`, `package.json`)
- 유지보수 CLI 3종: `--check-annotations`, `--fix-preserved-markup`, `annotate_cli.py`. `translation-sync/docs`·`README.md`·`Makefile`·workflow 전체 grep 결과 **0건**.
- E2E가 CI에서 실행되지 않는다는 사실
- `make translate`(Docker 경로)가 `translation-sync/.env`를 읽는다는 사실
- 마케팅 홈페이지의 관리 정책
- 성공 기준 / 로드맵 / 릴리스 개념

## 5. 발견 사항

### [Critical] E2E 테스트 목록 문서가 구현과 정면 충돌한다

- 관련 문서: `e2e/TEST_LIST_HOMEPAGE.md`, `e2e/TEST_LIST_NAV.md`
- 관련 코드: `e2e/homepage.spec.ts`, `e2e/navbar.spec.ts`
- 확인 내용:
  - `TEST_LIST_HOMEPAGE.md`는 78개(64/4/10)를 주장하지만 `homepage.spec.ts`의 `test(` 정의는 20개다.
  - `TEST_LIST_NAV.md`는 33개(23/3/7)를 주장하지만 `navbar.spec.ts`의 정의는 30개다.
  - 문서는 영어 원문 문구(`"The clean stack for Artisans and agents."`)를 검증한다고 적었으나 코드는 한국어 문자열을 단언한다.
  - 문서는 Resources·Events 드롭다운과 Search `⌘K`를 "검증한다"고 적었으나 코드는 그 요소들이 **존재하지 않아야 한다**고 단언한다(`SHOW_DISABLED_NAV = false`와 정합).
  - ID 의미가 상충한다. 문서 `N-12`=네비바 좌측, 코드 `N-12`=상단 고정. 문서 `HR-3`=태블릿 일러스트 숨김, 코드 `HR-3`=모바일 h1 오버플로.
  - `footer.spec.ts`(10개 정의)에 대응하는 목록 문서가 아예 없다.
- 프로젝트에 미치는 영향: 기여자가 문서를 신뢰하면 **의도적으로 비활성화한 메뉴를 되살리는 방향**으로 작업한다. 문서를 회귀 판단 기준으로 쓸 수 없다.
- 권장 조치: 두 파일을 삭제한다(spec 내 ID 주석이 이미 같은 역할을 한다). 유지하려면 spec에서 재생성하고 ID를 1:1로 고정한다.
- 확실성: 확인됨

### [Critical] README의 Docker 실행 안내가 동작하지 않는다

- 관련 문서: `README.md` §Docker 실행 — `docker run -p 3000:3000 laravel-docs`
- 관련 코드: `Dockerfile` 최종행 `CMD ["npm", "run", "build"]`, `EXPOSE` 없음, 서버 프로세스 없음. `docker-compose.yml`의 `build` 서비스도 포트 매핑이 없다.
- 확인 내용: 루트 이미지는 빌드 전용이다. 안내대로 실행하면 빌드 후 컨테이너가 종료되고 3000 포트에서 아무것도 서비스되지 않는다.
- 프로젝트에 미치는 영향: README의 두 실행 경로 중 하나가 확정적으로 실패한다. 최초 신뢰를 깨는 오류다.
- 권장 조치: 제목을 "Docker 빌드"로 바꾸고 `docker compose run --rm build`를 안내하거나, 로컬 서버는 `npm start` / `npm run build && npm run serve`를 안내한다.
- 확실성: 확인됨

### [High] 세 문서가 존재하지 않는 `docs/review/` 경로를 가리킨다

- 관련 문서: `translation-sync/docs/08-error-cases.md:4`, `.docs/system-prompt.md:62,114,119,694,712,733`, `.docs/user-prompt.md:2`, `.docs/prompt.md:5,360`
- 관련 경로: 실제 리뷰는 `.docs/review/`(8건)에 있고, 리뷰 전 `docs/`에는 `index.md` 하나뿐이었다.
- 확인 내용: `08-error-cases.md`는 현행 운영 계약의 근거로 `docs/review/translation-sync-refactor-review-2026-07-15.md`를 지목하는데 그 경로에 파일이 없다. `.docs/user-prompt.md:2`는 에이전트에게 `docs/review/*.md`를 모두 읽으라고 지시한다.
- 프로젝트에 미치는 영향: 사람·에이전트가 계약 입력을 찾지 못하거나 "리뷰 없음"으로 오판한다. 자동화 에이전트가 이 지시를 따르는 저장소이므로 실질 운영 위험이다.
- 참고: 이번 리뷰 산출물이 `docs/review/`에 생성되면서 경로 자체는 존재하게 되었지만, 세 문서가 참조하는 **파일**은 여전히 `.docs/review/`에 있다. 경로 수정이 필요하다.
- 권장 조치: 세 문서의 경로를 `.docs/review/`로 정정한다.
- 확실성: 확인됨

### [High] 유지보수 CLI 3종이 문서에도, 게이트에도 없다

- 관련 문서: `translation-sync/docs/05-additional-work.md` §5 (`--annotate-existing --apply`만 기재)
- 관련 코드: `main.py:736-748`의 `_FLAG_OPTIONS`/`_MAINTENANCE_OPTIONS`(`--check-annotations`, `--fix-preserved-markup` 포함), `annotate_cli.py`
- 확인 내용: `translation-sync/docs` + `README.md` + `Makefile` + `.github/workflows` 전체 grep 결과 `check-annotations`·`fix-preserved-markup`·`annotate_cli` **0건**. 그런데 이번 리뷰에서 `--check-annotations`를 실행한 결과 master 11건, 13.x 12건이 실패했다.
- 프로젝트에 미치는 영향: 실패 중인 corpus 자기검사가 문서에도 없고 자동 실행도 되지 않아, 실행 주체와 시점이 정의되지 않는다. 결과적으로 이 검사는 사실상 방치된다.
- 권장 조치: `05-additional-work.md` §5에 유지보수 CLI 표(명령 / 목적 / 기록 조건 / 실행 시점)를 추가한다. 새 문서 신설은 불필요하다.
- 확실성: 확인됨

### [High] SECURITY.md가 채워지지 않은 템플릿이다

- 관련 문서: `SECURITY.md`
- 관련 코드: `sync-translation.yml`의 provider secrets, `translate.py:84-95`의 비밀 마스킹
- 확인 내용: "프로젝트의 어떤 버전이 ... 알려주세요", "취약점을 보고하는 방법을 안내해주세요" 같은 **템플릿 지시문이 본문에 남아 있고**, Direct Email 항목에 실제 주소가 없다(`CODE_OF_CONDUCT.md`에는 존재). 지원 버전 표(`latest` / `< 1.0`)는 문서 사이트에 의미가 없다.
- 프로젝트에 미치는 영향: 실질적인 취약점 보고 채널이 없다. 이 저장소는 LLM provider API 키와 `contents: write` 토큰을 다루므로 공백의 비용이 크다.
- 권장 조치: 템플릿 지시문을 제거하고 실제 연락 채널과 지원 범위(배포 중인 사이트 / `main`)를 명시한다.
- 확실성: 확인됨

### [Medium] 코드 주석이 참조하는 문서 절 번호가 존재하지 않는다

- 관련 문서: `translation-sync/docs/05-additional-work.md` (§1~§8 구조, T 번호 체계 없음)
- 관련 코드: `.github/workflows/sync-translation.yml:3`("docs/05(T4) 트리거"), `annotate_cli.py:1`("docs/05 T2"), `sync/source/upstream.py:8`("docs/05(T1)")
- 확인 내용: 05 문서에 T1/T2/T4가 없다. 리팩터링으로 문서 구조가 바뀌고 주석만 남았다.
- 영향: 주석에서 사양으로 이동하는 경로가 끊긴다.
- 권장 조치: 주석을 현행 절 번호로 교체한다.
- 확실성: 확인됨

### [Medium] `.env` 로딩 서술이 Docker 경로와 어긋난다

- 관련 문서: `translation-sync/docs/00-workflow-summary.md:123` — "동기화 명령이 저장소의 `.env`를 자동으로 읽지는 않는다"
- 관련 코드: `docker-compose.yml:15-17` `env_file: translation-sync/.env`, `Makefile`의 `translate` target
- 확인 내용: 호스트 경로(`sync/runtime/config.py`는 `os.environ`만 읽음)에서는 문서가 맞다. 그러나 `make translate`는 compose `env_file`을 통해 `translation-sync/.env`를 읽는다.
- 영향: 로컬에서 `make translate`가 왜 동작/미동작하는지 문서로 설명되지 않는다.
- 권장 조치: 00 §2.2에 경로별 로딩 차이 한 행을 추가한다.
- 확실성: 확인됨

### [Medium] README가 Makefile 표면의 일부만 노출한다

- 관련 문서: `README.md` §실행
- 관련 코드: `Makefile`의 target 17개
- 확인 내용: README는 5개만 노출한다. pre-commit이 실제 실행하는 `make check`, workflow가 실행하는 `make translation-artifact-check`, Docker 경로 `make translate`가 빠져 있다.
- 영향: 커밋이 왜 느린지, 무엇이 검사되는지 기여자가 알 수 없다.
- 권장 조치: README에 명령 표 하나로 통합한다.
- 확실성: 확인됨

### [Medium] 강제 규칙과 권장 관례가 구분되지 않는다

- 관련 문서: `.husky/docs/commit-message-guide.md`, `.github/docs/pull-request-guide.md`
- 관련 코드: `.husky/validate-commit.cjs`
- 확인 내용: 문서는 "첫 글자 소문자 / 마침표 금지 / 50자 이내"를 규칙으로 적었으나 정규식은 `type(scope):` 형식만 검사한다. 문서의 예외 목록도 `Initial commit`과 Revert 따옴표 조건을 누락했다.
- 영향: 훅 통과를 규칙 준수로 오해하거나, 반대로 불필요하게 `--no-verify`를 쓴다.
- 권장 조치: 각 항목에 (자동 검사) / (관례)를 표기하고 예외 목록을 정정한다.
- 확실성: 확인됨

### [Medium] 기여자 문서가 어디에서도 링크되지 않는다 (orphan)

- 관련 문서: `.github/docs/*`(3건), `.husky/docs/commit-message-guide.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`
- 확인 내용: `README.md`·PR 템플릿·훅 스크립트에서 이들에 대한 참조가 0건이다.
- 영향: 규칙 위반 시 근거 문서로 도달할 수 없다.
- 권장 조치: README 하단에 "기여" 섹션 5줄(브랜치/커밋/PR/보안/CoC 링크)을 추가한다. `CONTRIBUTING.md` 신설은 중복 원천이 되므로 권장하지 않는다.
- 확실성: 확인됨

### [Medium] PR 템플릿이 렌더링되지 않는다

- 관련 문서: `.github/pull_request_template.md`
- 확인 내용: 전체가 HTML 주석이라 PR 본문에 보이는 텍스트가 0이다. 허용 type 목록이 이 주석에만 존재하고 `pull-request-guide.md`에는 없다.
- 영향: 템플릿이 실질 기능을 하지 않고, type 목록의 단일 출처가 숨겨져 있다.
- 권장 조치: 최소 체크리스트를 가시 텍스트로 두고, type 목록은 `pull-request-guide.md`로 옮긴다.
- 확실성: 확인됨

### [Low] 저장소 내 기준 테스트 수가 서로 모순된다

- 관련 문서: `.docs/prompt.md:122,136`이 "419 passed"를 기준으로 고정
- 확인 내용: 이번 리뷰의 실측은 **771 tests**다. `.docs/prompt.md`는 특정 스냅샷(`645a2d4`) 전용 문서인데 유효기간 표기가 없다.
- 영향: 이 문서를 따르는 에이전트가 정상 상태를 오판한다.
- 권장 조치: `.docs/prompt.md` 상단에 대상 커밋 전용·만료됨을 명시한다.
- 확실성: 확인됨

### [Low] 기타

- `AGENTS.md`는 `make claude`가 외부 저장소에서 받아 append하는 범용 문서인데 출처 표기가 없고, `.docs/user-prompt.md`는 이를 선행 계약으로 지시한다. → 상단에 출처와 성격을 2줄 명시.
- `.github/agents/*.agent.md` 3종이 PHPDoc·N+1·SQL Injection 등 이 저장소에 없는 대상을 전제한다. → 저장소화 또는 제거.
- `.claude/hookify.sync-docs.local.md`가 존재하지 않는 `app/Domains/{domain}/docs/`를 요구한다(`enabled: false`). → 제거 또는 교체.
- `.github/workflows/CLAUDE.md`가 빈 도구 아티팩트다. → 삭제.
- `docs/index.md`는 내용이 문자열 `index.md`인 죽은 파일인데 `Dockerfile`이 여전히 `COPY docs ./docs`로 복사해 "사용 중"처럼 보인다.

## 6. 중복되거나 충돌하는 문서

| 항목 | 중복/충돌 위치 | 판단 |
|---|---|---|
| CLI 비활성 기능 목록 | `README.md`, `00-workflow-summary.md:143`, `02-translation.md:383`(`hook` 추가) | 02가 최신. README는 요약임을 명시하면 충돌 아님 |
| 커밋/PR 규칙 | `.husky/docs/commit-message-guide.md`, `.github/docs/pull-request-guide.md`, PR 템플릿 주석 | type 목록의 단일 출처를 `pull-request-guide.md`로 통합 필요 |
| 사이드바 단일 기준 | `06-sidebar-sync.md`(=`documentation.md`) vs 루트 `sidebars.ts` 잔존 | `sidebars.ts`가 죽은 파일이므로 제거가 정답 |
| 리뷰 원장 | `.docs/review/*.md` 8건 | 현행/폐기 표기와 인덱스 없음 |

## 7. 오래되었을 가능성이 있는 문서

- `.docs/prompt.md` — 대상 스냅샷 `645a2d4`, 현재 HEAD `d0a29b7`. 기준 테스트 수도 실측과 다르다.
- `.docs/review/*.md` 8건 — 시간순 누적일 뿐 어느 판정이 유효한지 표기가 없다.
- `translation-sync/docs/08-error-cases.md` — 스스로 이력임을 선언했으므로 문제는 아니나, 인용한 코드 좌표(`runtime/config.py:46`)는 현재와 다르다.
- `i18n/{ko,ja}/docusaurus-theme-classic/footer.json` — `/docs/12.x` 기준(현재 최신 13.x)이고 커스텀 Footer가 소비하지 않는다.

## 8. 부족한 문서 (실제 운영에 필요한 것만)

1. **유지보수 CLI 표** — `05-additional-work.md` §5에 1개 표 추가.
2. **README의 명령·기여·JA·홈페이지 4개 항목 보강** — 새 파일 없이 README 수정으로 해결.
3. **현재 알려진 게이트 실패 항목의 추적 위치** — `.docs/review` 최신 문서 상단 3줄로 대체 가능.

새로 만들 필요가 **없는** 문서: `CONTRIBUTING.md`(README 섹션으로 충분), `CHANGELOG.md`(릴리스 개념 없음), 별도 ADR·아키텍처 문서(`translation-sync/docs`가 담당), `.docs/review/INDEX.md`(유지비가 이득을 초과).

## 9. 삭제 또는 보관을 검토할 문서

| 대상 | 이유 |
|---|---|
| `e2e/TEST_LIST_HOMEPAGE.md`, `e2e/TEST_LIST_NAV.md` | 구현과 정면 충돌, spec 주석이 같은 역할 수행 |
| `docs/index.md`, `sidebars.ts` | 사이트 구성에서 사용되지 않는 죽은 스캐폴딩 |
| `.github/workflows/CLAUDE.md` | 빈 도구 아티팩트 |
| `.claude/hookify.sync-docs.local.md` | 존재하지 않는 경로 전제, 비활성 |
| `.github/agents/*.agent.md` | 타 프로젝트 boilerplate |

## 10. 권장 문서 구조

```text
README.md                          ← 단일 진입점 (소개/실행/명령표/문서 갱신/기여 링크/라이선스)
├── translation-sync/docs/00~07    ← 파이프라인 운영 사양 (현행 유지)
├── translation-sync/docs/08       ← 이력 (현행 표기 유지)
├── .github/docs/                  ← 브랜치·PR 규칙 (README에서 링크)
├── .husky/docs/                   ← 커밋 규칙 (README에서 링크)
├── SECURITY.md, CODE_OF_CONDUCT.md ← 거버넌스 (README에서 링크)
├── docs/review/                   ← 리뷰 산출물
└── .docs/                         ← 일회성 세션 계약 (상단에 만료 표기)
```

## 11. 문서 개선 우선순위

| 순서 | 항목 | 조치 규모 |
|---|---|---|
| 1 | `e2e/TEST_LIST_*.md` 삭제 또는 재생성 | 파일 2개 |
| 2 | README Docker 절 정정 | 5행 |
| 3 | `docs/review/` → `.docs/review/` 경로 정정 | 문서 3개 |
| 4 | SECURITY.md 실제 내용 작성 | 파일 1개 |
| 5 | `05-additional-work.md`에 유지보수 CLI 표 추가 | 표 1개 |
| 6 | README에 JA·명령표·기여 링크·`translation-sync/.env` 보강 | 20행 내 |
| 7 | 코드 주석의 T1/T2/T4 참조 정정 | 3개 파일 |
| 8 | 커밋/PR 문서의 강제·관례 구분 | 문서 2개 |
| 9 | 죽은 스캐폴딩·아티팩트 제거 | 파일 5개 + Dockerfile 2행 |
