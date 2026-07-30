# Translation Sync 현재 HEAD 준비도 리뷰

- 검토일: 2026-07-29 KST
- 검토 대상: `d0a29b70d7d8421511ab64081ec43ed2daeb1077`
- 브랜치: `refactor/sync-docs`
- 판정 계약: `.docs/system-prompt.md`
- 참고 계약: `.docs/prompt.md`, `translation-sync/docs/00-workflow-summary.md` ~ `08-error-cases.md`

## 1. 최종 판정

**검증 미완료, 현재 체크아웃 상태로는 배포 불가다.**

Python 단위 테스트 771개와 격리 replay를 포함한 `make translation-check`는 통과했다. 그러나 현재 HEAD에 커밋된 KO/JA 문서 자체는 전체 annotation 검사에서 93건 실패하고, `make site-check`는 일본어 문서의 누락 fragment 15건으로 실패한다. 구현의 강화된 계약과 함께 필요한 번역 산출물 마이그레이션이 현재 HEAD에 포함되지 않은 상태다.

이번 요청은 코드 변경을 금지하고 리뷰 문서 추가만 요구했으므로 구현·번역 문서는 수정하지 않았다. 이 문서만 새 Git 비무시 변경으로 남긴다.

## 2. 시작 상태와 검토 범위

| 항목 | 확인 결과 | 판정 |
|---|---|---|
| HEAD / 원격 추적 ref | 로컬 HEAD와 `origin/refactor/sync-docs`가 모두 `d0a29b7` | 현재 HEAD를 기준으로 검토 |
| tracked worktree / index | 시작 시 clean, staged 변경 0 | 보존 |
| worktree | 활성 worktree 1개 | 새 worktree 생성 0 |
| stash | 0개 | 새 stash 생성 0 |
| `.docs/*.md`, 기존 `.docs/review/*.md` | 현재 HEAD와 대조해 읽기 전용 재고 | 수정·삭제하지 않음 |
| `.review/session-20260729` | 63 MB, 현재 HEAD의 mutation/reproduction 증거 146개 파일 | 근거 부족 삭제를 피하고 보류 |
| `.env` | 정책상 열람 불가 | 접근·열람 0 |
| `dot_env` | mode `0600`; 허용 key 이름 4개만 확인 | 값·header 출력 없이 strict loader 입력으로만 사용, 보존 |
| `node_modules`, `translation-sync/.venv` | 로컬 재현 의존성 캐시 | 보존 |
| IDE/도구 설정과 ignored `CLAUDE.md` | 사용자·도구 로컬 상태 | 보존 |
| `.docusaurus`, `build`, `__pycache__` | 이번 검증에서 재생성 가능한 산출물 | 검증 후 정확한 경로만 제거 |

`dot_env`에서 사용한 allowlist는 `OPENAI_API_KEY`, `TRANSLATION_MODEL`, `TRANSLATION_PROVIDER`, `TRANSLATION_REASONING_EFFORT`뿐이다. 값은 상위 shell에 export하거나 로그에 출력하지 않았다. 모델만 각 검증 자식 프로세스에서 명시적으로 덮어썼다.

## 3. 실행 결과

### 3.1 결정적 게이트

| 명령 | 결과 |
|---|---|
| `git diff --check` 및 conflict marker 검사 | 통과 |
| `cd translation-sync && uv lock --check` | 통과, 18 packages resolved |
| Python 3.14 compileall | 통과 |
| `make translation-test` | 통과, **771 tests**, failure 0, error 0 |
| `make translation-check` | 통과, 771 tests + 679 source replay; 31개 변경 문서를 identity KO/JA로 처리하고 두 번째 새 process가 `no source changes to translate`로 수렴 |
| `cd translation-sync && uv run --locked --python 3.14 python main.py --check-annotations` | **실패**, **93 annotation checks** |
| `NODE_OPTIONS=--max-old-space-size=4096 make site-check` | Markdown utility/typecheck/KO·JA production build 통과 후 anchor 검사 **46,611 / 46,626**, fragment 누락 15건으로 실패 |
| `npm audit --audit-level=low` | 알려진 취약점 0 |
| `cd translation-sync && uv audit` | 17 packages, 알려진 취약점·adverse status 0 |

실행 환경은 Python 3.14.6, Node 26.5.0, npm 11.17.0, uv 0.11.31이었다. lock 계약에서 지정한 uv setup 버전은 workflow의 0.11.32이며, 실제 `uv lock --check`와 모든 Python gate는 현 로컬 0.11.31에서 수행했다.

### 3.2 운영 provider fixture

프로젝트의 production OpenAI adapter, 현재 prompt, response contract와 final verifier를 그대로 사용했다. sandbox가 project virtualenv의 CA bundle을 읽지 못해 TLS 검증은 운영체제 기본 trust store로 연결했으며, 요청 payload·provider 구현·prompt·검증기는 변경하지 않았다.

| 모델 | reasoning | KO | JA | 반복 결과 |
|---|---|---|---|---|
| `gpt-5.4-mini` | `medium` | 통과 | 통과 | **3 / 3** |
| `gpt-5.6-luna` | `medium` | 통과 | 통과 | **3 / 3** |

- KO effective prompt SHA-256: `92cc1c6e2ea222a00374b668d00aaa355dddc5de48135ff0d066fbca106dbe39`
- JA effective prompt SHA-256: `e2d5aea0b504032ef289a70d0e5cae5c619f373b6a884313290b435b53e3732e`
- 총 6회 모델 실행, 12 locale fixture가 모두 성공했다.
- 이는 live API와 고정 fixture 계약의 성공 증거다. 원문 동기화부터 파일 기록까지 수행하는 실제 문서 E2E 6회를 대신하지 않는다.

`.docs/prompt.md`는 실제 문서 live 실행을 모든 결정적 gate 통과 뒤에만 허용한다. annotation과 site gate가 먼저 실패했으므로 `version-13.x/ai-sdk.md`의 두 모델 × 3회 유료 E2E는 실행하지 않았다. 실패한 선행 조건을 무시하고 이를 완료로 판정하지 않는다.

### 3.3 Docker와 `act`

- Docker client 29.1.3은 있으나 daemon socket이 없어 server에 연결할 수 없었다.
- `act 0.2.89 workflow_dispatch --dryrun -W .github/workflows/sync-translation.yml`은 job/image 선택까지 진행한 뒤 같은 daemon 부재로 종료 코드 1이었다.
- 따라서 Docker image, Docker E2E, `act` 전체 dry-run은 **conditional 미검증**이며 통과로 기록하지 않는다.

## 4. 확인된 미완료와 개선 사항

### R-01 — P1: 커밋된 locale corpus가 현재 annotation 계약을 충족하지 않는다

`python main.py --check-annotations`가 8.x부터 13.x와 master의 KO/JA 문서에서 93건 실패했다. 실패 유형에는 source comment 불일치·누락, legacy note marker, link label/pair, inline code, sentence cardinality, source text 잔존이 포함됐다.

대표 영향 파일은 다음과 같다.

- `version-10.x/controllers.md`, `eloquent.md`, `helpers.md`, `requests.md`
- `version-11.x/upgrade.md`, `vite.md`
- `version-12.x/ai-sdk.md`, `boost.md`, `search.md`, `vite.md`
- `version-13.x/ai-sdk.md`, `boost.md`, `search.md`, `vite.md`
- 같은 계열의 8.x, 9.x, master 문서

영향은 명확하다. 현재 HEAD의 코드와 현재 HEAD의 생성 산출물이 서로 다른 계약 세대에 있다. 구현만 병합하고 locale migration을 제외하면 `.docs/system-prompt.md` §11.3과 §13을 만족할 수 없다.

완료 조건은 깨끗한 checkout에서 생성한 KO/JA migration을 함께 검토하고, 전체 annotation corpus가 issue 0으로 끝나는 것이다. 단순히 검사를 완화하거나 annotation을 삭제해 숨기면 안 된다.

### R-02 — P1: 현재 HEAD의 production site gate에 일본어 broken fragment 15건이 있다

KO/JA Docusaurus build는 성공했지만 anchor validator가 46,626건 중 15건을 거부했다. 모두 target HTML route는 존재하고 fragment ID만 없다.

| JA 문서 | 누락 fragment target |
|---|---|
| `version-10.x/controllers.md` | `controllers/#actions-handled-by-resource-controller` |
| `version-10.x/eloquent.md` | `migrations/#writing-migrations` |
| `version-10.x/helpers.md` | `helpers/#method-array-sort-recursive-desc` |
| `version-10.x/helpers.md` | `errors/#logging` |
| `version-10.x/requests.md` | `helpers/#fluent-strings` |
| `version-12.x/ai.md` | `ai/#agents-integration` |
| `version-8.x/billing.md` | `eloquent-mutators/##date-casting` |
| `version-8.x/eloquent.md` | `migrations/#writing-migrations` |
| `version-8.x/helpers.md` | `errors/#logging` |
| `version-8.x/http-tests.md` | `database-testing/#writing-factories` |
| `version-8.x/http-tests.md` | `http-tests/#assert-similar-json` |
| `version-9.x/eloquent.md` | `migrations/#writing-migrations` |
| `version-9.x/helpers.md` | `errors/#logging` |
| `version-9.x/notifications.md` | `notifications/#formatting-shortcode-notifications` |
| `version-master/ai.md` | `ai/#agents-integration` |

예를 들어 KO `version-10.x/controllers.md`에는 구 fragment를 위한 `data-translation-alias`가 있지만 대응 JA 문서에는 없다. 이 상태에서 `deploy.yml`이 실행하는 `make site-check`는 실패하므로 현재 HEAD는 그대로 배포할 수 없다.

완료 조건은 누락 alias/target을 원문과 locale별로 정합하게 생성하고, 깨끗한 checkout에서 anchor 결과가 **46,626 / 46,626** 이상 동일 corpus 전건 성공하는 것이다. `##date-casting`처럼 원래 link 자체가 잘못된 항목은 alias를 추가하기보다 target을 바로잡아야 한다.

### R-03 — P2: `translation-check` 성공이 체크인된 배포 corpus의 준비도를 증명하지 않는다

같은 HEAD에서 다음 두 사실이 동시에 성립했다.

1. `make translation-check`는 격리 clone에서 identity sync로 31개 문서를 생성·수렴시켜 통과했다.
2. 활성 checkout의 annotation과 site gate는 각각 93건, 15건 실패했다.

replay는 generator가 미래 상태를 만들 수 있고 두 번째 실행이 수렴하는지를 잘 검증한다. 반면 현재 커밋이 이미 그 미래 상태를 포함하는지는 검증하지 않는다. sync workflow는 live sync 뒤 site gate를 실행하지만, 일반 PR/merge나 `main` push의 deploy workflow는 현재 checkout에서 곧바로 site gate를 실행한다.

개선안은 둘 중 하나다.

- implementation 변경과 그 implementation이 만든 locale migration을 같은 delivery 단위에 포함한다.
- PR/merge gate에 깨끗한 checkout의 `--check-annotations`와 `site-check`를 추가해 생성 산출물 누락을 merge 전에 차단한다.

`translation-check`의 의미를 바꾸지 않고 별도 “committed corpus readiness” gate를 두는 편이 replay의 격리·수렴 책임을 흐리지 않는다.

### R-04 — P3: 전체 run transaction/rollback은 아직 구현되지 않았다

`main.py`는 개별 파일에 `atomic_write_text`를 사용하지만 target 전체를 staging한 뒤 일괄 publish하지 않는다. 뒤 locale 또는 sidebar가 실패하면 앞서 기록한 EN cache/locale 파일이 로컬 worktree에 남는다. workflow는 실패 시 commit/push를 생략해 원격은 보호하지만, 로컬 수동 실행의 부분 상태는 자동 복구하지 않는다.

이는 `00-workflow-summary.md:78-80`, `05-additional-work.md:46,68`, `06-sidebar-sync.md:239`, `08-error-cases.md:27`에 정확히 문서화돼 있어 문서·코드 불일치는 아니다. 이전 F-09의 알려진 미구현 개선 항목이다.

개선 시에는 run manifest에 포함된 EN/KO/JA/sidebar를 저장소 밖 또는 같은 filesystem의 staging 경계에서 모두 검증한 뒤 publish하거나, 정확한 affected-file snapshot과 rollback failure injection을 구현해야 한다. 현재의 per-file `fsync`/atomic replace 보장은 유지해야 한다.

### R-05 — P3: replay와 workflow에 명시적 전체 제한 시간이 없다

upstream clone은 300초 timeout과 최대 3회 retry가 있지만, `replay.py:628-638`의 첫 번째·두 번째 `main.py` 자식 process에는 `timeout`이 없다. sync workflow job에도 `timeout-minutes`가 없다. 따라서 자식이 멈추면 로컬 실행은 무기한, Actions는 기본 job 한도까지 점유할 수 있다. 이 한계는 `07-local-replay.md:29`에 이미 문서화돼 있다.

개선 시 문서 크기와 provider-free replay의 관측 시간을 기준으로 자식 process timeout과 job-level `timeout-minutes`를 함께 두고, timeout을 replay 종료 코드 계약에 맞게 정규화해야 한다.

### R-06 — P2: production live sync의 provider contract 실패 진단 정보가 부족하다

`main.py:283-287`, `358-361`은 최종 contract issue label만 반환한다. 실패한 block/document의 안정적인 식별자, attempt, 응답 hash, 크기·문자/구조 metric은 남기지 않는다. 고정 fixture용 `provider_check.py`는 fixture 응답을 출력하지만 실제 다중 문서 sync의 해당 경로를 보완하지 않는다.

이전 V-07과 `08-error-cases.md`의 P8 진단 개선 여지가 남아 있다. 원문·응답 전체를 무조건 CI log에 노출하는 대신 version/doc/locale/block ordinal, prompt hash, response SHA-256, response length, contract issue별 판정 metric을 구조화해 남기는 것이 적절하다.

## 5. 기존 리뷰 finding 재판정

| 기존 항목 | 현재 판정 |
|---|---|
| F-01 import/export P0 | **Closed** — 전체 test discovery가 771개를 정상 실행했다. |
| F-02~F-08, F-13~F-16, F-18 및 대응 N/S 회귀 | 현재 구현과 회귀 test는 HEAD에 포함됐고 전체 test가 통과했다. 이번 검토에서 동일 코드 결함을 재개방할 직접 반례는 확인하지 않았다. 다만 R-01/R-02 때문에 그 계약을 따르는 배포 산출물은 아직 미완료다. |
| F-09 run transaction | **Open improvement** — R-04. 문서와 구현은 일치하지만 rollback 미구현이다. |
| F-10 site/anchor | **Reopened at artifact level** — validator/build 구현이 아니라 현재 JA corpus의 15개 누락 target 때문에 R-02로 실패한다. |
| F-11 Azure live path | **Conditional** — `dot_env`에는 OpenAI 운영 경로만 있어 Azure deployment/API version은 live 검증하지 못했다. |
| F-12 action SHA pin | **Closed** — sync/deploy workflow의 외부 action이 full-length SHA로 고정돼 있다. |
| F-17 schedule/ruleset | **External conditional** — schedule 지연과 branch protection/ruleset은 저장소 밖 운영 조건이다. |
| N-11 deploy ref guard | **Closed** — deploy workflow가 `main` branch ref를 검증한다. |
| V-03 transient retry | **Closed** — timeout/network/429/5xx 분류와 관련 test가 현재 구현에 있다. |
| V-06 inline-code contract | **Closed in implementation** — repair/retry 경로와 회귀 test가 통합돼 있다. |
| V-07 / P8 diagnostics | **Open improvement** — R-06. |

## 6. 공식 1차 자료 대조

- OpenAI [GPT-5.4 mini model](https://developers.openai.com/api/docs/models/gpt-5.4-mini): `gpt-5.4-mini`는 Responses API와 `reasoning.effort=medium`을 지원한다.
- OpenAI [GPT-5.6 Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna): `gpt-5.6-luna`는 비용 민감·대량 workload용 공식 model ID이며 Responses API와 reasoning token을 지원한다.
- OpenAI [Model guidance](https://developers.openai.com/api/docs/guides/latest-model): GPT-5.6 Luna는 efficient high-volume 선택지이고 `medium`은 균형 잡힌 시작점이다. 현재 provider/model/effort 조합은 공식 지원 범위다.
- GitHub [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): job과 step에 `timeout-minutes`를 지정할 수 있고 job 기본값은 360분이다. R-05의 명시적 제한 시간 권고 근거다.
- GitHub [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): 외부 action을 full-length commit SHA로 pin하는 것이 immutable release를 사용하는 방법이다. 현재 workflow는 이 권고를 충족한다.

## 7. 변경 파일과 로컬 상태 처분

새로 추가한 파일은 이 문서 하나다.

- `.docs/review/translation-sync-current-head-readiness-review-2026-07-29.md`

코드, 번역 corpus, workflow, lockfile은 수정하지 않았다. 활성 저장소에서 commit, staging, push, PR, 새 worktree, 새 stash를 만들지 않았다.

검증이 만든 `.docusaurus`, `build`, Python `__pycache__`는 재생성 가능한 ignored 산출물이므로 정확한 경로만 제거했다. `.review/session-20260729`은 현재 검토의 mutation/reproduction 증거이고 의미 상실 근거가 부족해 보류했다. `node_modules`, `.venv`, 사용자 도구 설정, `dot_env`도 보존했다. 되돌릴 수 없는 material 삭제는 수행하지 않았다.

## 8. 완료 조건과 conditional gate

완료 판정 전에 최소한 다음이 모두 필요하다.

1. 현재 구현으로 생성한 locale migration을 delivery에 포함한다.
2. 깨끗한 checkout의 전체 annotation corpus를 0건으로 만든다.
3. 깨끗한 checkout의 `make site-check`를 fragment 누락 0건으로 만든다.
4. 같은 최종 상태에서 771개 이상 전체 unit test와 `make translation-check`를 다시 통과시킨다.
5. 결정적 gate 통과 뒤 `.docs/prompt.md` A.5~A.7의 `ai-sdk.md` 실제 E2E를 두 모델 각각 독립 3/3 및 각 run no-op으로 검증한다.
6. Docker daemon이 있는 환경에서 image/E2E와 `act` workflow dry-run을 실행한다.

현재 실행하지 못한 conditional gate는 Azure live adapter, Docker image/E2E, 완전한 `act` dry-run이다. 실제 문서 6회 OpenAI E2E는 credential 부재가 아니라 선행 결정적 gate 실패 때문에 계약에 따라 실행하지 않았다.
