# Translation Sync 리팩토링 검증

검증일: 2026-07-26 KST

대상: `refactor/sync-docs`의 `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a`

## 1. 결론

**merge 불가.** Blocker는 F-01~F-04, F-13~F-15, N-01~N-06, N-14, N-16이다. 공식 13.x `ai-sdk.md` 동기화가 두 모델 모두 3회 전부 같은 patch 오류로 실패했고, luna JA provider fixture와 JA anchor gate도 유효한 계약 증거를 만들지 못했다.

## 2. 검증 스냅샷

| 항목 | 값 |
|---|---|
| 대상 커밋 | `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a` (`refact: temp`) |
| `main..HEAD` | 1 commit |
| 커밋 규모 | 74 files, +13,232 / -1,288 |
| Python | CPython 3.14.6, uv 0.11.31 |
| Node / npm | Node 26.5.0 / npm 11.17.0 (`.nvmrc` 26과 일치) |
| act | 0.2.89 |
| Docker | Engine 29.1.3, Compose standalone 5.0.1 |
| 검증 workspace | 프로젝트 내부 `.review/translation-sync-validation-20260726-010820/` |
| 공식 upstream | `laravel/docs` 13.x `b0b1c3e17c715880e0c380cd30061da6ca952c9d` |
| 운영 provider | `openai`, reasoning `medium` |

실행한 gate:

- Docker Python unit suite 419개
- `act workflow_dispatch --dryrun`
- 산출 경로 smoke, Markdown 링크 유틸, typecheck, KO/JA site build, anchor validator, `git diff --check`
- 두 모델의 live provider contract 각 1회
- 두 모델 × 3개의 독립 checkout에서 실제 upstream sync
- 6개 checkout의 artifact/site/diff 및 실패 상태 진단 재실행
- F-01 종료 여부, Track A, Track B, 생성 산출물, workflow, 문서 정합 감사

실행하지 않은 gate:

- 실제 `make translation-replay`: 내부적으로 disposable commit을 만들기 때문에 이번 `git commit` 절대 금지 조건에 따라 실행하지 않았다. replay unit test와 코드 경로만 검증했다.
- Azure adapter live path: 제공된 credential에는 Azure 필수 설정이 없다.

절차상 환경 편차:

- 부록 A.2의 BSD `awk`는 loop 변수명 `index`가 내장 함수와 충돌했다. 값 비열람 검사는 동일 로직에서 변수명만 `i`로 바꿔 통과했다.
- 부록 A.3의 strict credential runner 원문은 비민감 설정 줄의 inline comment를 거부해 API 호출 전에 종료됐다. 이 prescribed runner 결과 자체는 실패로 보존했다. 실제 provider 증거는 검증 전용 사본에서 비밀값이 아닌 줄에만 dotenv의 `공백 + # 주석` 규칙을 적용한 호환 runner로 얻었고, API key에는 원래 공백 금지를 유지했다. 따라서 §2.8은 이 절차 편차와 luna JA 계약 실패를 함께 반영해 실패로 판정한다.
- 호스트 unit suite는 관리형 sandbox가 synthetic `.env` fixture 삭제를 차단해 cleanup 오류 1건이 났다. 동일 commit과 Python의 Docker suite 419개가 통과했으므로 Docker 결과를 판정 근거로 사용했다.
- Docker build의 외부 package fetch가 느려 project-local cache와 공식 upstream read-only mirror를 사용했다. 번역 이미지의 `main.py`, `provider_check.py`, `uv.lock`, `patch.py` SHA-256은 clean checkout과 일치했다.
- 기준 site Docker의 최초 실행은 네 site container가 겹친 상태에서 JA compile 중 exit 137이었다. `site-validation.log`와 exit를 보존하고 `NODE_OPTIONS=--max-old-space-size=3072` 단독 재실행해 link test 1/1, typecheck, KO/JA build, 현 validator 46,626/46,626을 exit 0으로 확인했다. site image 자체는 정상 build/tag됐지만 최초 wrapper는 zsh read-only 변수명 `status` 때문에 image build 뒤 exit 1을 냈으므로 image 존재와 clean build 로그를 별도로 확인했다.
- 검증 도중 별도 병행 작업의 `.review/translation-sync-validation-20260726-010825/`와 `translation-sync-refactor-verification-2026-07-26-supplement.md`가 작업 트리에 나타났다. 이 실행에서는 해당 파일을 수정·삭제하지 않았고, 그 주장도 그대로 수용하지 않았다. 주 보고서에 추가한 내용은 `645a2d4` clean checkout에서 독립 재현한 항목뿐이다.

## 3. gate 결과표

| # | gate | 선행 기준값 | 이번 결과 | 판정 |
|---|---|---|---|---|
| 2.1 | Python 단위 테스트 | 419 passed | Docker `Ran 419 tests`, `OK` | 통과 |
| 2.2 | replay 계약 | 실제 replay 679 docs, 2회차 no-op | replay unit 13개 통과와 process fingerprint 코드 경로 확인. 실제 replay는 commit 금지로 미실행 | 미실행 |
| 2.3 | workflow 구조 | 해당 없음 | `act workflow_dispatch --dryrun`이 workflow graph와 전체 step을 해석함. 실제 step은 실행하지 않음 | 통과 |
| 2.4 | 산출 경로 smoke | pass | `translation sync output paths verified: 0 file(s)` | 통과 |
| 2.5 | Markdown 링크 유틸 | pass | Node test 1개 통과 | 통과 |
| 2.6 | typecheck + build + anchor | 46,626 / 46,626 | host와 단독 Docker retry에서 typecheck·KO/JA build 성공, 현 validator 46,626 / 46,626. locale-correct 대조에서 JA 9건 누락(N-14/N-15) | 부분적 |
| 2.7 | 공백/충돌 마커 | pass | `git diff --check HEAD^...HEAD` 출력 없음 | 통과 |
| 2.8 | provider contract | 해당 없음 | prescribed runner는 API 전 거부. 호환 runner에서 mini KO/JA 통과, luna KO 통과·JA 실패 | 실패 |
| 2.9 | 실제 문서 번역 | 해당 없음 | mini 0/3, luna 0/3 | 실패 |
| 2.10 | live 후속 gate | 해당 없음 | artifact/site/diff 6/6 통과, 성공 checkout이 없어 정식 no-op 적용 불가 | 실패 |
| 2.11 | F-01 종료 | 선행 P0 | flat import는 동작하지만 facade가 `sync.sidebar` package를 shadow하고 설계 문서가 없음. docs 00~08은 정상 | 미종료(P0) |

F-01의 import 확인은 단순 import 성공에 그치지 않았다. `translation-sync/sync/__init__.py:9-36`의 12개 flat alias와 canonical module은 같은 객체였고, 같은 origin의 중복 module object와 순환 import는 0개였다. 그러나 `sidebar` generator를 `sync.sidebar` 속성으로 노출하면서 package를 shadow한다. `python -m sync.sidebar --help`는 exit 0이지만 `import sync.sidebar.generator` 뒤 통상적인 `sync.sidebar.generator` 접근은 `AttributeError`이며, 이 비대칭과 flat alias 설계는 `translation-sync/docs/`에 문서화되어 있지 않다. 문서 번호 체계는 00~08 정확히 9개이고 구 `07-error-cases.md`와 stale link가 없지만, prompt §2.11의 두 종료 조건 중 import seam이 미완결이므로 F-01은 P0으로 남는다.

이하 `main.py`, `provider_check.py`, `replay.py`, `validate_generated_changes.py`, `docs/...`, `scripts/...`, `tests/...`는 프로젝트 루트의 `translation-sync/` 아래이며 bare `test_*.py`도 `translation-sync/tests/`에 있다. bare module명은 `response_contract.py`·`verify.py` → `translation-sync/sync/verification/`, `patch.py`·`translate.py` → `translation-sync/sync/translation/`, `config.py` → `translation-sync/sync/runtime/`, `upstream.py` → `translation-sync/sync/source/`, `sidebar/generator.py` → `translation-sync/sync/sidebar/`를 뜻한다. `annotation/...`과 `common/...`은 각각 `translation-sync/sync/annotation/...`, `translation-sync/sync/common/...`이고, workflow는 `.github/workflows/`를 명시한다. Python inline 재현의 공통 실행 명령은 프로젝트 루트에서 `PYTHONPATH=.review/translation-sync-validation-20260726-010820/build-base/translation-sync python3 -`였고, Node inline 재현은 `(cd .review/translation-sync-validation-20260726-010820/build-base && node --input-type=module -)`로 실행했다. 각 finding의 재현 조건 블록은 표준 입력과 실제 출력을 기록하며, live 명령 원문은 `.review/translation-sync-validation-20260726-010820/logs/`에 보존했다.

## 4. Track A 결과

| 항목 | 판정 | A-1 / A-2 / A-3 근거 |
|---|---|---|
| F-02 | 부분적 | `response_contract.py:220-304,1127-1315`가 ordered occurrence와 ownership을 강제한다. contract 제거 시 `test_rejects_comment_without_owned_body`, `test_rejects_missing_duplicate_source_occurrence`, `test_rejects_unowned_extra_prose` 등 5종 negative test가 7건 실패했다. 그러나 같은 owned body에 추가한 환각 prose가 통과했으므로 A-3 규칙상 미완결이다. |
| F-03 | 부분적 | `provider_check.py:115-125`가 production contract와 final verifier를 함께 호출하고, 제거 시 `test_rejects_paragraph_indented_as_a_code_block`와 `test_rejects_modified_fenced_code`가 실패했다. live fixture는 heading/prose/code 각 1개뿐이며 의미가 잘못된 문장은 형식만 맞으면 통과했다. |
| F-04 | 부분적 | inline link의 13.x→12.x drift는 `verify.py:192-212,446-451`과 `test_detects_internal_doc_link_version_drift`로 막히며 정규화를 되돌리면 drift tests가 실패했다. 그러나 reference-style definition의 13.x→12.x 변경은 contract와 final verifier 모두 `[]`였다. |
| F-05 | 부분적 | `patch.py:245-273,688-745,2869-2979`와 `test_moves_named_anchor_sections_without_retranslation`, `test_unique_named_section_reorder_rejects_crossed_annotation_ownership` 등 9개 test가 단순 reorder와 separator를 고정한다. 그러나 TOC prefix까지 함께 바뀌면 special path가 발동하지 않고 실제 13.x의 reorder 가능 문서 99개 모두 이 shape이므로 A-3에서 반례가 재현됐다(N-18). |
| F-06 | 부분적 | numeric option과 exit 2는 `config.py:46-53,80-87`, `main.py:709-714`, `test_config_rejects_invalid_numeric_runtime_options`, `test_main_reports_invalid_provider_configuration_without_traceback`로 고정된다. 검증기를 제거하면 네 숫자 subtest가 실패하지만 임의 reasoning 값은 허용되고 config 검증은 upstream 뒤다. |
| F-07 | 부분적 | `translate.py:45-81,393-466`의 env allowlist, 임시 cwd, read-only sandbox, user hook 차단은 `test_cli_request_returns_only_the_last_agent_message`가 고정하며 전체 parent env를 되돌리면 실패했다. 공격 문자열은 stdin에만 남았지만 실제 Codex CLI 품질 parity와 prompt-injection 저항성은 미검증이다. |
| F-08 | 부분적 | JP prompt의 특정 생략/재배치 충돌은 정리됐지만 `tests/test_prompt.py`는 실제 규칙 문구를 고정하지 않는다. 규칙을 되돌려도 tests가 통과했고, request-ID 보존 의미를 누락한 KO/JA 최소 입력도 contract를 통과했다. |
| F-10 | 확인됨 | Node 26.5.0에서 typecheck와 KO/JA full build가 통과해 Node 26 호환 주장은 확인됐다. 현 anchor 명령도 46,626 / 46,626이지만 JA 절대 링크 coverage는 N-14로 반증됐다. |
| F-13 | 부분적 | note/heading/style/list 관련 구현과 회귀 tests를 확인했다. 관련 helper mutation은 tests를 깨뜨렸지만 sentinel round-trip test가 production 양단을 함께 호출하고 final sentinel 거부 사유 독립 test가 없어 A-3 방어가 약하다. |
| F-16 | 확인됨 | `sidebar/generator.py:29-47,104-124,323-331`이 `versions.json`에서 동적 파생한다. production `sync/sidebar`, `sidebar`, `main.py` 전체 grep에서 8.x~13.x 하드코딩은 0건이고 `test_supports_future_version_listed_in_versions_json`도 통과했다. |

### 생성 산출물·workflow 교차 확인

기존 `ai-sdk` 3개 version × KO/JA 2개 locale = 6건과 `boost`의 같은 6건, 합계 12개 문서는 annotation 검사에서 모두 `CLEAN`이었다. 생성 diff는 legacy marker 30건을 0건으로 정리했고 flat alias 대상 6개 파일은 alias 추가와 EOF 공백 외 변화가 없었으며 `git diff --check`도 통과했다. 반면 localized legacy marker는 실제 쓰기 경로에서 남는 F-14, 산출물 validator의 허용 범위는 N-07로 계속 열린다. workflow 정독에서는 sync action의 SHA pin과 단계 순서를 확인했지만 deploy mutable tag(F-12), 수동 non-main 배포(N-11), credential 파일의 build-context 노출(N-12), 외부 ruleset 의존(F-17)을 닫지 못했다.

## 5. 신규 Finding 요약표

| ID | 심각도 | 요약 | 상태 |
|---|---|---|---|
| N-01 | P1 | TARGET 판정이 주석 sequence만 확인해 빈 신규 본문과 삭제 orphan을 성공 처리 | Open |
| N-02 | P1 | table row 단일 후보가 raw context를 확인하지 않고 sibling 행을 덮어씀 | Open |
| N-03 | P1 | 중복 named anchor는 count만 맞으면 잘못된 section 위치를 허용 | Open |
| N-04 | P1 | upstream version token 미검증으로 EN root 밖 쓰기 가능 | Open |
| N-05 | P1 | 현재 공식 `ai-sdk.md` sync가 두 모델 모두 3/3 patch 단계에서 실패 | Open |
| N-06 | P1 | response contract가 보존형·제품명 중심 정상 번역을 세 휴리스틱으로 오탐 | Open |
| N-07 | P2 | 산출물 validator가 미지원 version·단독 locale·삭제를 허용 | Open |
| N-08 | P2 | upstream clone/branch 실패가 일관된 non-zero 결과로 정규화되지 않음 | Open |
| N-09 | P2 | provider config 오류를 upstream 네트워크·쓰기 뒤에 검사 | Open |
| N-10 | P2 | CLI retry가 substring으로 영구 usage/model 오류도 재시도 | Open |
| N-11 | P2 | deploy 수동 실행이 main ref를 강제하지 않음 | Open |
| N-12 | P2 | 운영 credential 파일 `dot_env`가 Git/Docker context에서 제외되지 않음 | Open |
| N-13 | P3 | replay 준비 중 interrupt가 불완전 sandbox를 남겨 문서 계약과 불일치 | Open |
| N-14 | P1 | JA 절대 문서 링크 anchor를 KO HTML에서 검사해 회귀를 숨김 | Open |
| N-15 | P2 | JA 8.x~10.x 문서에 KO가 가진 alias anchor 9개가 누락 | Open |
| N-16 | P1 | quote/admonition 주석 정책이 prompt·annotation·final verifier와 불일치 | Open |
| N-17 | P2 | table 후보 스캔이 code fence 안의 예시 행을 선택해 정상 sync를 차단 | Open |
| N-18 | P2 | 실제 TOC prefix 변경을 동반한 named-section reorder가 전용 경로를 타지 못함 | Open |
| N-19 | P3 | README dotenv 예시의 fence가 깨져 후반 15 source line이 코드로 렌더됨 | Open |

## 6. 상세 Finding

### N-01. TARGET 판정이 번역 본문 완전성을 확인하지 않는다 — P1

#### 근거

`patch.py:688-723`은 annotation signature만으로 TARGET을 판정하고, `patch.py:562-565`는 TARGET anchored change를 건너뛴다. `AnnotatedBlock`은 본문 0줄도 허용한다(`patch.py:930-943`). Production 경로도 TARGET이면 provider/response contract 없이 `existing_context`를 재사용한다(`main.py:391-396`).

#### 재현 조건

신규 문단:

```text
old: Before. / After.
new: Before. / Inserted meaning. / After.
existing: <!-- Inserted meaning. --> 주석만 있고 번역 body 없음
```

실제 출력:

```text
state=target
existing_context='<!-- Inserted meaning. -->'
unchanged=True
inserted_body_absent=True
verify=[]
```

삭제 문단에서도 주석이 사라지고 `삭제되어야 할 번역.` body만 남은 입력이 `unchanged=True`, `verify=[]`였다. `patch.py:1299-1302`가 code-like raw evidence가 없으면 자연어 residue 검사를 즉시 끝내기 때문이다.

#### 영향

새 의미가 화면에서 사라지거나 삭제된 의미가 번역 문서에 남아도 자동 workflow가 성공할 수 있다.

#### 권고

TARGET 판정에 annotation별 owned body 존재·cardinality를 포함하고, deletion은 old source의 locale body ownership을 기준으로 orphan을 검출한다.

#### 완료 조건

comment-only insertion과 natural-language deletion orphan fixture가 모두 fail-closed하고 해당 regression tests가 없으면 실패해야 한다.

### N-02. table row 단일 후보가 raw context 없이 sibling 행을 덮어쓴다 — P1

#### 근거

`patch.py:2673-2684`는 stable tail-cell 후보가 전역 1개면 즉시 반환한다. before/after context narrowing은 후보가 2개 이상일 때만 실행된다(`patch.py:2686-2702`).

#### 재현 조건

원문 표의 `First | same`을 `Changed | same`으로 바꾸되 locale 표에는 `Second | same` 행만 남긴다. 새 번역 행 `변경됨 | same`을 적용하면 유일한 둘째 행이 덮어써지고 결과 data row는 1개가 된다.

실제 결과:

```text
result='| 변경됨 | same |'
verify(existing, source=old)=[]
verify(result, source=new)=[]
```

#### 영향

부분 drift가 있는 표에서 변경 대상이 아닌 행을 잃거나 잘못 번역하면서 verifier까지 통과한다. 반대로 두 후보가 모두 있는 정상 표는 `missing existing translation block`으로 막혀 가용성도 낮춘다.

#### 권고

후보 수와 무관하게 raw before/after context와 source ordinal을 확인하고, context가 맞지 않으면 쓰기 전에 거부한다.

#### 완료 조건

위 sibling-only fixture는 거부되고 완전한 duplicate-tail 표는 정확한 첫 행만 변경하는 regression test가 통과해야 한다.

### N-03. named anchor의 count만 확인해 위치 drift를 허용한다 — P1

#### 근거

`patch.py:1393-1404`는 target anchor count가 맞으면 insertion/rename/deletion을 no-op 처리한다. final verifier도 anchor를 `Counter`로만 비교한다(`verify.py:454-455`).

#### 재현 조건

동일한 `<a name="dup"></a>` 두 개 중 첫 anchor를 삭제하는 source 변경에서, locale에는 anchor 하나가 여전히 첫 section 앞에 남고 target은 둘째 section 앞을 요구하도록 구성했다.

```text
apply_plan unchanged
anchor_before_first=True
anchor_before_second=False
verify=[]
```

#### 영향

fragment link가 잘못된 section으로 이동해도 자동 sync와 final verifier가 성공한다.

#### 권고

anchor occurrence별 인접 annotation/source block identity를 비교해 위치까지 TARGET state에 포함한다.

#### 완료 조건

중복 anchor count는 같지만 위치가 다른 fixture를 거부하고 올바른 occurrence 이동을 검증하는 test가 필요하다.

### N-04. upstream version token으로 destination 경계를 벗어날 수 있다 — P1

#### 근거

`upstream.py:27-29`는 `versions.json` 값을 그대로 반환하고 `upstream.py:95-116`은 `EN_ROOT / f"version-{version}"`을 생성·삭제·기록한다. `sidebar/generator.py:34-37`에 있는 token regex guard가 upstream에는 없다.

#### 재현 조건

`version='x/../../escaped'`와 단일 Markdown source fixture를 `sync_version`에 전달했다.

```text
count=1
EN_ROOT 밖 escaped/example.md 생성=True
```

#### 영향

잘못된 tracked version 값이 번역 cache 밖 경로를 삭제하거나 덮어쓸 수 있다.

#### 권고

공유 version validator를 upstream 진입점에서 먼저 호출하고 resolved destination이 `EN_ROOT` 하위인지 검사한다.

#### 완료 조건

slash, `..`, absolute path가 포함된 version을 쓰기 전에 거부하고 destination escape 파일이 생기지 않는 regression test가 필요하다.

### N-05. 현재 공식 `ai-sdk.md` 변경을 partial patch가 처리하지 못한다 — P1

#### 근거

공식 `laravel/docs` 13.x `b0b1c3e17c715880e0c380cd30061da6ca952c9d`의 `ai-sdk.md`는 대상 cache와 +378/-3 차이가 난다. 동일 official ref와 동일 HEAD baseline의 6개 독립 checkout에서 모두 다음으로 종료됐다.

```text
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
verify failed: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md:
  ['partial patch failed: missing existing translation block for: > [!NOTE]']
stopping after first verification failure
```

오류는 `patch.py:1004` 또는 `patch.py:1065`의 existing-block lookup에서 발생한다.

#### 재현 조건

`645a2d4` checkout에서 부록 A.5대로 KO/JA를 `HEAD^` 기준으로 복원하고 공식 13.x HEAD를 sync한 뒤 `main.py --fail-fast --version 13.x --doc ai-sdk.md`를 실행한다.

#### 영향

두 모델 모두 0/3이며 JA와 실제 provider 번역 단계에 도달하지 못한다. A.7 완료 조건과 무인 동기화 가용성을 직접 위반한다.

#### 권고

legacy note와 GFM note가 기존/target state에서 같은 structural block으로 정규화되도록 patch plan의 lookup 기준을 통일한다.

#### 완료 조건

동일 official SHA와 `HEAD^` baseline의 KO/JA가 모델별 3회 모두 번역·검증·site gate에 성공하고 두 번째 실행이 수렴해야 한다.

### N-06. 보존형·제품명 중심 정상 번역을 세 휴리스틱으로 거부한다 — P1

#### 근거

`response_contract.py:38,876-915,1104-1124,1285-1312`에는 서로 독립적인 세 false-positive 경로가 있다. source substring echo, lowercase inline-code 보호 목록 분류 실패, `ascii_letters <= target_count * 2 + 2` 목표 언어 비율이다.

#### 재현 조건

```text
source='Laravel Vapor'
translated='<!-- Laravel Vapor -->\nLaravel Vapor를 사용합니다.'
```

구조, annotation, locale 문자 조건을 만족하지만 결과는 `['provider untranslated source text']`였다. 같은 owned line 끝에 원문에 없는 한국어 문장을 붙인 반대 fixture는 `[]`였다.

두 번째 fixture는 실제 Blade 식별자 목록 shape다.

```text
source:
- `data`
- `render`

output:
<!-- - `data` - `render` -->
- `data`
- `render`

contract=['provider untranslated source text',
          'provider target language mismatch']
final=[]
```

목록 전체가 inline-code와 구두점뿐인 정확한 보존 결과를 거부하지만 각 항목에 임의 한국어 설명을 붙이면 두 verifier가 모두 통과했다.

세 번째 fixture는 실제 `ai-sdk.md` 블록이다.

```text
source='**Supported providers:** Anthropic, Gemini'
output='<!-- **Supported providers:** Anthropic, Gemini -->\n**지원 제공자:** Anthropic, Gemini'
contract=['provider target language mismatch']
final=[]
target_chars=5 ascii_letters=15 allowed_ascii=12
```

세 fixture 모두 production `_translate_block_change`에서 같은 정상 응답을 두 번 반환하면 provider 2회 뒤 `IncompleteTranslation`이었다. `test_verify.py` 137개는 모두 통과해 이 positive 경계를 고정하지 않는다.

#### 영향

제품명·API 이름을 유지해야 하는 짧은 정상 문단, 식별자만으로 구성된 목록, 제품명 비중이 높은 간결한 번역이 pipeline 전체를 막는다. 같은 line이나 목록 항목에 붙인 불필요한 의미 추가는 오히려 통과할 수 있다.

#### 권고

inline-code-only 목록은 대소문자와 무관하게 source와 정확히 같은 보호 목록만 허용한다. prose에서는 보존 대상 제품명·식별자를 자연어 echo 및 ASCII 비율 계산에서 분리하고, source/body block의 의미 없는 추가를 검출할 구조적 기준을 둔다.

#### 완료 조건

세 positive fixture와 실제 Blade 8개 식별자 목록이 첫 provider 응답으로 통과해야 한다. 식별자 변경·누락·설명 추가, 기존 near-English echo, same-line extra prose는 각각 의도한 사유로 실패해야 하며 KO/JA 제품명 경계 tests를 추가해야 한다.

### N-07. 산출물 validator가 허용 version과 변경 상태를 검증하지 않는다 — P2

#### 근거

`validate_generated_changes.py:12-24`의 version regex는 `versions.json` membership을 확인하지 않는다. `:29-56`은 path만 보고 Git status, 파일 유형, locale pairing을 보지 않는다.

#### 재현 조건

격리 fixture에서 아래 변경을 만들었다.

```text
versioned_docs/version-999.x/arbitrary.md
versioned_sidebars/version-999.x-sidebars.json
```

결과는 `unexpected=[]`, main-equivalent exit 0이었다. 단독 KO 파일, 임의 문서명과 허용 Markdown 삭제도 통과했다.

#### 영향

미지원 version이나 orphan locale 산출물이 workflow의 후속 `git add -A`에 포함될 수 있다.

#### 권고

`versions.json` membership, status별 허용, source/KO/JA pairing, 삭제 정책을 검사한다.

#### 완료 조건

999.x, 단독 locale, 임의 filename, 예상 밖 삭제가 각각 독립 negative test로 거부돼야 한다.

### N-08. upstream 실패가 일관된 non-zero 결과로 닫히지 않는다 — P2

#### 근거

초기 clone은 `upstream.py:143-145`의 try 밖이라 `CalledProcessError`가 traceback으로 탈출한다. 반면 unpinned branch checkout 실패는 `upstream.py:153-161`에서 skip한 뒤 성공한다.

#### 재현 조건

```text
초기 clone 실패 -> CalledProcessError(128) escape
version-ghost branch 없음 -> "branch not found, skipped", total: 0 files, exit=0
```

#### 영향

호출자는 정제된 `upstream sync failed` 계약을 받지 못하거나 stale cache를 정상 동기화로 오인한다.

#### 권고

clone과 checkout 오류를 모두 잡고 요청된 version/doc을 가져오지 못하면 non-zero로 종료한다.

#### 완료 조건

초기 clone 실패와 필터 대상 branch 부재가 traceback 없이 서로 구분 가능한 메시지와 non-zero exit를 내야 한다.

### N-09. 잘못된 provider 설정도 upstream을 먼저 변경한다 — P2

#### 근거

`main.py:692-715`의 순서는 `upstream.main` → `_select_changes` → `config.load_config`다.

#### 재현 조건

invalid timeout config와 mock upstream을 사용한 호출 순서는 다음이었다.

```text
events=['upstream', 'config']
exit=2
stderr='configuration failed: TRANSLATION_CLI_TIMEOUT must be an integer > 0'
```

#### 영향

잘못된 model/key/runtime config가 확실한 실행도 네트워크와 영어 cache 쓰기를 먼저 수행해 실패 원자성과 진단성을 낮춘다.

#### 권고

provider-independent maintenance mode가 아닌 translation sync에서는 config를 upstream보다 먼저 검증한다.

#### 완료 조건

invalid config fixture에서 upstream mock이 호출되지 않는 regression test가 통과해야 한다.

### N-10. CLI retry 분류가 영구 오류도 재시도한다 — P2

#### 근거

`translate.py:300-340`은 오류 문자열의 `500`, `connection` substring을 transient marker로 취급한다.

#### 재현 조건

```text
invalid model: gpt-500                  -> calls=3, sleeps=2
unexpected argument '--connection-mode' -> calls=3, sleeps=2
```

#### 영향

고칠 수 없는 model/usage 오류가 기본 설정에서 장시간 지연되고 실제 transient 실패와 구분되지 않는다.

#### 권고

HTTP status object와 제한된 transport exception type을 사용하고 CLI text는 anchored 진단만 재시도한다.

#### 완료 조건

위 두 영구 오류는 1회, 429/5xx/timeout fixture는 정책 횟수만큼 호출되는 tests가 필요하다.

### N-11. deploy 수동 실행이 main ref를 강제하지 않는다 — P2

#### 근거

`.github/workflows/deploy.yml:15`는 unrestricted `workflow_dispatch`다. checkout(`:32-33`)과 deploy job(`:50-60`)에도 main guard가 없다. sync workflow의 호출만 `--ref main`으로 제한된다(`.github/workflows/sync-translation.yml:150`).

#### 재현 조건

GitHub UI/API에서 deploy workflow를 feature branch 또는 tag ref로 dispatch하면 해당 ref checkout이 production `github-pages` environment deploy job으로 이어지는 workflow graph다.

#### 영향

실수로 비-main 문서를 production Pages에 배포할 수 있다. 외부 environment rule이 차단하는지는 저장소에서 확인할 수 없다.

#### 권고

workflow 첫 step 또는 두 job 모두에서 branch ref가 main인지 강제한다.

#### 완료 조건

feature/tag dispatch가 build 전에 실패하고 main dispatch만 deploy job에 도달하는 workflow test 또는 `act` fixture가 필요하다.

### N-12. 운영 credential 파일이 ignore/context 경계에 없다 — P2

#### 근거

`.dockerignore:15-16`과 `.gitignore`는 `.env` 계열만 제외하며 `dot_env`는 제외하지 않는다. Compose는 root `.`을 build context로 사용한다(`docker-compose.yml:5,13`). `Makefile:106`도 저장소 전체를 container에 mount한다.

#### 재현 조건

현재 활성 root에서 `git check-ignore dot_env`와 `.dockerignore` 검사를 수행했으며 둘 다 제외되지 않았다. 실제 키 때문에 이번 검증은 clean clone만 Docker context로 사용했다.

#### 영향

일반적인 root Docker build/init 또는 실수한 `git add -A`가 운영 credential을 context/index에 포함할 수 있다.

#### 권고

실제 운영 파일명을 Git/Docker ignore에 추가하거나 표준 ignored `.env` 경로로 옮긴다.

#### 완료 조건

`git check-ignore dot_env`가 성공하고 Docker build context 검사에서 파일이 제외되며 secret scanning test가 이를 고정해야 한다.

### N-13. replay 준비 interrupt가 불완전 sandbox를 남긴다 — P3

#### 근거

`replay.py:183-208`의 준비 cleanup은 `OSError`, `ReplayError`만 처리한다. `07-local-replay.md:41,47`은 준비 실패 시 불완전 directory 정리를 보장한다고 기술한다.

#### 재현 조건

clone helper에서 `KeyboardInterrupt`를 발생시켰다.

```text
keyboard_interrupt_propagated=True
remaining_sandboxes=1
```

#### 영향

사용자 interrupt 뒤 불완전 sandbox가 남고 문서화된 exit/cleanup 계약과 달라진다.

#### 권고

interrupt cleanup과 exit code를 구현하거나 문서에서 명시적으로 예외로 둔다.

#### 완료 조건

준비 단계 interrupt 후 sandbox count 0과 정해진 exit code를 확인하는 test가 필요하다.

### N-14. JA 절대 문서 링크 anchor를 KO HTML에서 검사한다 — P1

#### 근거

`scripts/validate-anchors.mjs:42-53,130,138`은 KO와 JA 문서를 모두 순회하지만 `scripts/anchor-routes.mjs:17-21`은 `/docs/...` 절대 경로를 locale prefix 없이 반환한다. JA source URL에서도 대상이 `build/ja/docs/...`가 아니라 `build/docs/...`로 해석된다. `scripts/markdown-link-utils.test.mjs:43-44`도 이 잘못된 기대값을 고정한다.

#### 재현 조건

기존 build에서 `npm run validate-anchors`와 동일 router를 locale-aware하게 대조하는 project-local Node harness를 실행했다.

```text
current validator:
Total anchor links: 46626
OK: 46626
id not found: 0

locale-correct unique (source file, href):
KO: 1482 / 1482, missing-id=0
JA: 1473 / 1482, missing-id=9

sourceUrl=/ja/docs/10.x/helpers/
absolute=/docs/10.x/errors
relative=/ja/docs/10.x/errors
```

실제 JA HTML에는 `/ja/docs/10.x/errors/#logging` 링크가 있지만 JA target ID는 0개이고, KO target ID는 1개였다.

#### 영향

`Makefile:58-61`, `.github/workflows/sync-translation.yml:107-108`, `.github/workflows/deploy.yml:43-44`의 유일한 anchor gate가 모든 JA 절대 문서 링크 회귀를 KO HTML로 대체 검증한다. 잘못된 JA 문서가 gate를 통과해 자동 commit·배포될 수 있다.

#### 권고

JA source에서 `/docs/...`를 해석할 때 `/ja/docs/...`를 만들고, 이미 locale이 붙은 경로와 사이트 외 절대 경로는 중복 prefix 없이 보존한다. 현재 잘못된 단위 test 기대값도 함께 고친다.

#### 완료 조건

N-15 수정 전에는 validator가 JA 누락 9건을 검출하고, 수정 후 KO·JA가 각각 1,482/1,482를 통과해야 한다. JA·KO 절대 경로와 이미 localized된 경로의 unit tests 및 전체 `make site-check`가 통과해야 한다.

### N-15. JA 문서에 alias anchor 9개가 누락되어 있다 — P2

#### 근거

현재 KO에는 `data-translation-alias` 15개, JA에는 6개만 있다. 집합 차이 9개가 N-14의 locale-correct scan에서 발견된 실제 broken anchor 9개와 정확히 일치했다.

#### 재현 조건

기존 build와 source를 함께 센 결과다.

```text
KO alias instances=15
JA alias instances=6
JA missing=9
rendered localized href=9
matching JA target id=0
```

누락 대상은 8.x~10.x `logging` 3건, 8.x~10.x `writing-migrations` 3건, 8.x `writing-factories`, 10.x `fluent-strings`, 8.x `##date-casting`이다. 각 source link는 실제 JA HTML에 렌더되지만 대응 target ID가 없다.

#### 영향

9개 링크는 페이지를 열지만 의도한 fragment로 이동하지 않는다. N-14 때문에 이 정적 콘텐츠 불일치가 배포 gate에서도 보이지 않는다.

#### 권고

KO alias를 JA의 대응 canonical section에 대칭 반영한다. `##date-casting`은 양 locale 링크와 alias를 정상적인 단일 `#date-casting`으로 정리할지 함께 검토한다.

#### 완료 조건

KO/JA alias가 각각 15개로 같고 locale-correct scan이 양쪽 모두 1,482/1,482, missing 0이어야 한다. N-14를 고친 정식 anchor validator도 통과해야 한다.

### N-16. quote/admonition의 원문 주석 정책이 검증 계층마다 다르다 — P1

#### 근거

`response_contract.py:220-282,1127-1192`는 quote 본문에 같은 quote depth의 원문 주석을 요구한다. 반면 `verify.py:322-364`, `common/markdown.py:445-454`, `annotation/annotate.py:202-207`은 quote line을 주석 대상에서 제외하고, `translate.py:159-168`의 prompt도 quoted comment 형식을 설명하지 않는다.

#### 재현 조건

production contract, final verifier와 `_translate_block_change`를 같은 최소 입력으로 호출했다.

```text
source:
> Vector search requires the AI SDK and PostgreSQL or MongoDB.

output:
> 벡터 검색에는 AI SDK와 PostgreSQL 또는 MongoDB가 필요합니다.

contract=[
  'provider original comment mismatch',
  'provider annotation ownership mismatch'
]
final=[]
provider_calls=2
result=IncompleteTranslation
```

일반 주석도 ownership mismatch이며 `> <!-- source -->` 형식만 통과한다. 현재 KO admonition 3,383개 중 바로 뒤 quoted comment가 있는 것은 49개, JA 3,380개 중 7개뿐이다.

#### 영향

현재 corpus와 prompt에 맞는 정상 changed-admonition 응답이 두 번 거부되고 fail-fast run 전체가 종료된다. 모델이 문서화되지 않은 quoted comment 형태를 우연히 생성해야만 통과할 수 있다.

#### 권고

기존 corpus와 final verifier에 맞춰 quote 본문을 필수 주석 대상에서 제외하되 quote depth와 admonition type 보존은 유지한다. 주석 의무화를 선택한다면 prompt, annotation 생성기, 문서와 전체 corpus를 함께 이관해야 한다.

#### 완료 조건

미주석 quote positive가 첫 provider 응답으로 통과하고 quote depth/type 변경은 계속 실패해야 한다. prompt, annotation 생성기, response contract, final verifier의 정책을 같은 tests로 고정해야 한다.

### N-17. table 후보 스캔이 code fence 안의 예시 행을 선택한다 — P2

#### 근거

`patch.py:2673-2681`은 table-like line 전체를 후보로 훑으면서 fence 범위를 제외하지 않고, `:2711-2717`은 선택된 행을 교체한다. 같은 파일 `:2603-2634`에는 fence 제외 scanner가 있지만 table 경로는 사용하지 않는다.

#### 재현 조건

실제 locale 표 `| 이전 | 사용 가능 |` 뒤 code fence에 `| Old | Available |` 예시를 두고 source table의 `Old`를 `New`로 변경했다. production diff→plan→apply→verify harness를 3회 실행했다.

```text
reproduced=3/3
selected_row=11
fence_ranges=[(10, 12)]
real_table_unchanged=True
code_example_replaced='| 새 값 | 사용 가능 |'
final=['code block mismatch']
```

#### 영향

최종 verifier가 쓰기를 막으므로 silent corruption은 아니지만, 유효한 table 변경이 code mismatch로 실패해 동기화 run을 중단한다. 영어 corpus에는 fence 안 table-like line을 가진 문서가 12개 있어 latent 입력이 존재한다.

#### 권고

table 후보 domain에서 fenced/indented code 범위를 제외하고, N-02의 raw context 검증도 모든 후보 수에서 동일하게 적용한다.

#### 완료 조건

외부 실제 표와 fence 내부 예시가 함께 있을 때 외부 행만 바뀌고 code bytes는 보존되어야 한다. 중복 후보, fence-only 후보, N-02 sibling 행 fixture를 독립 tests로 고정해야 한다.

### N-18. 실제 TOC prefix 변경을 동반한 named-section reorder가 실패한다 — P2

#### 근거

`patch.py:2869-2908`은 첫 named anchor 전부를 prefix로 잡고 `:2941`에서 old/new prefix byte equality를 요구한다. section 순서와 함께 TOC link 순서가 정상적으로 바뀌면 `_named_section_reorder`가 `None`이 되어 전용 경로를 타지 못한다.

#### 재현 조건

section만 swap한 control과 TOC 두 줄까지 같은 순서로 swap한 실제 shape를 production plan에 3회 넣었다.

```text
section-only named_plan=True
section+TOC named_plan=None
general_plan changes=3 translations=2
apply='existing block order matches neither source nor target plan state'
reproduced=3/3
```

13.x named-anchor 문서 100개 모두 nonempty TOC prefix를 가지며 그중 99개가 2개 이상 section을 가져 reorder 가능하다.

#### 영향

F-05의 전용 reorder 구현이 실제 Laravel 문서 shape 대부분에서 발동하지 않아 정상 section 이동이 provider translation 또는 patch failure로 퇴행한다.

#### 권고

TOC를 opaque prefix가 아니라 section anchor 순서에 종속된 구조로 함께 reorder하거나, TOC의 link permutation을 별도 검증한 뒤 허용한다.

#### 완료 조건

section과 TOC가 함께 같은 permutation으로 이동하는 실제 13.x fixture가 provider-free로 성공하고 두 번째 적용이 no-op이어야 한다. TOC target 변경이나 crossed ownership은 계속 fail-closed여야 한다.

### N-19. README dotenv 예시의 Markdown fence가 깨져 있다 — P3

#### 근거

`HEAD^...HEAD`에서 `README.md:74`의 세 칸 들여쓰기만 사라졌다. 그 결과 `README.md:76`의 원래 closing fence가 새 무언어 fence opener로 해석된다.

#### 재현 조건

현재 README와 부모 버전을 같은 remark parser로 읽어 AST source span을 비교했다.

```text
unexpected code node source span=76-90
captured source lines=15
node content lines=13
node characters=621
node UTF-8 bytes=913
```

#### 영향

README 후반 15개 source line이 일반 설명이 아니라 하나의 code block으로 렌더되어 로컬 설정 지침의 구조와 가독성이 깨진다. 번역 runtime에는 영향이 없다.

#### 권고

dotenv 예시의 opener/closer indentation과 fence 짝을 복구한다.

#### 완료 조건

remark AST에서 해당 예시만 code node이고 76~90행이 정상 paragraph/list 구조로 돌아와야 한다. Markdown fence 검사를 문서 또는 site test에 추가한다.

## 7. 알려진 미해결 항목의 상태 변화

| 항목 | 판정 | 현재 증거 |
|---|---|---|
| F-09 (P3) | 그대로 | KO 성공 뒤 JA 실패 fixture에서 KO 파일이 남았다. workflow는 live 실패 시 commit step에 도달하지 않아 branch는 보호된다. |
| F-14 (P1) | 그대로, merge·무인 운영 blocker | localized `> **참고:**` provider output이 `_translate_added_document`에서 contract/final issue 없이 실제 파일에 기록됐다. merge 시 legacy marker가 검증을 통과해 자동 배포될 수 있어 무인 운영도 불가하다. |
| F-15 (P1) | 그대로, merge·무인 운영 blocker | multi-backtick, multiline code span, inline-code `<img>`, single/parenthesized link title과 title 값 변경, 1~3칸 들여쓴 quote 문제를 모두 재현했다. silent markup mutation을 gate가 감지하지 못해 무인 운영도 불가하다. |
| F-18 (P2) | 그대로 | 잘못된 순서와 duplicate `versions.json`을 loader가 거부하지 않았다. 실제 현재 파일 순서는 정상이다. |
| F-11 (P2) | 검증 불가 | 현재 credential은 OpenAI 경로만 제공한다. Azure API version/deployment 전략은 범위 밖이다. |
| F-12 (P3) | 그대로 | sync action은 SHA pin, deploy action 5개는 mutable major tag다. |
| F-17 (P3) | 외부 결정 필요 | cron 정각과 direct push는 GitHub schedule 전달 및 branch ruleset/bypass에 의존한다. |

F-14 재현의 실제 생성 결과:

```text
TRANSLATE_ISSUES=[]
DEST_EXISTS=True
CONTRACT_ISSUES=[]
FINAL_ISSUES=[]
CANONICAL_MARKER=False
LOCALIZED_LEGACY_REMAINS=True
```

F-15의 대표 silent mutation:

- 원문 `Use ``foo`` now.`에서 닫는 double-backtick delimiter를 단일 backtick으로 바꿔도 두 verifier 통과
- multiline code span 내부 `<style>`이 preprocess에서 삭제된 뒤 변형된 기준본과 output이 함께 검증돼 통과
- inline-code 내부 `<img>`가 `<img .../>`로 바뀌어도 통과
- `[x](foo 'title')`, `[x](foo (title))` target 변경과 double-quoted title 값 변경 통과

## 8. live 표본 결과

### Provider fixture

| Model | Provider | KO prompt SHA-256 | JA prompt SHA-256 | KO | JA |
|---|---|---|---|---|---|
| `gpt-5.4-mini` | openai | `8bf437f9ff848cebcf3c0420818d00fdf57bef56512659a643e922de010e59f7` | `104d626b647a0c33b60e34b96c72a01f64149538c738fd39d68a8764da5a3782` | 통과 | 통과 |
| `gpt-5.6-luna` | openai | 동일 | 동일 | 통과 | 실패: response shape 및 link target/label/pair mismatch |

### 실제 문서

- 선택 문서: `version-13.x/ai-sdk.md`
- 공식 upstream: `b0b1c3e17c715880e0c380cd30061da6ca952c9d`
- 영어 source delta: +378 / -3

| Model | Run | Sync | KO/JA | Site | Artifact/diff | No-op |
|---|---:|---|---|---|---|---|
| `gpt-5.4-mini` | 1 | 실패 | KO patch 실패, JA 미실행 | 명령 통과* | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |
| `gpt-5.4-mini` | 2 | 실패 | KO patch 실패, JA 미실행 | 명령 통과 | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |
| `gpt-5.4-mini` | 3 | 실패 | KO patch 실패, JA 미실행 | 명령 통과 | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |
| `gpt-5.6-luna` | 1 | 실패 | KO patch 실패, JA 미실행 | 명령 통과* | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |
| `gpt-5.6-luna` | 2 | 실패 | KO patch 실패, JA 미실행 | 명령 통과* | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |
| `gpt-5.6-luna` | 3 | 실패 | KO patch 실패, JA 미실행 | 명령 통과* | 통과, 3 paths | 진단 재실행 exit 1, diff hash 동일 |

6개 모두 official source sync와 manifest 생성까지 성공했으나 `translated 1 doc(s) into ko, ja`에 도달하지 못했다. 새 KO/JA provider 산출물이 없어 사람 번역 품질 검토 대상도 생성되지 않았다. 변경 경로는 영어 cache와 부록이 복원한 기존 KO/JA `ai-sdk.md` 세 경로로 제한됐다.

`*` 최초 병렬 site 시도에서는 mini run 1과 luna run 1이 `Killed`로 끝났고 luna run 2/3은 빌드 도중 중단했다. mini와 겹친 luna run 1의 첫 retry도 의도적으로 중단했다. 모든 로그를 보존하고 다른 container를 종료한 뒤 `NODE_OPTIONS=--max-old-space-size=3072` 단독 순차 재실행에서 6개 모두 KO/JA build와 현 validator 46,626/46,626이 통과했다. 이는 제품 결함으로 세지 않았지만 실패·중단 표본을 삭제하지 않았다. “명령 통과”는 현 validator의 exit 0을 뜻하며, JA absolute-link coverage 자체는 N-14 때문에 유효하지 않다.

첫 실행에 성공한 checkout이 0개이므로 부록 A.6의 정식 no-op 검사를 적용할 대상도 0개였다. 별도 진단 재실행에서는 6개 모두 같은 source diff를 다시 감지해 `translating: ko` 뒤 exit 1이었다. 첫 실패 뒤 diff hash는 변하지 않았지만 `no source changes to translate`와 provider 무호출 성공 조건은 만족하지 못했다.

## 9. 검증 한계

- **identity replay의 의미**: patch/구조/멱등성 검증이며 번역 품질 검증이 아니다.
- **live 검증의 범위**: 두 모델의 provider fixture와 동일한 실제 문서 1건을 모델별 3회 검사한다. 전체 Laravel 문서군의 의미 정확성이나 장기간 provider 안정성을 보장하지 않는다.
- **secret 비열람**: `dot_env`의 key 이름과 구조만 확인하고 값은 사람이 읽지 않았다. 실제 유효성은 하위 프로세스 호출 성공으로만 간접 확인했다.
- **현재 provider만 검증**: `dot_env`가 실제 선택한 provider 경로만 검증했다. Azure 필수 key가 없으므로 Azure deployment/API version 경로는 판정하지 않았다.
- **비용·성능 표본 한계**: 모델별 3회의 한 문서 실행에서 얻은 latency/retry는 운영 전체 비용이나 tail latency를 대표하지 않는다.
- 위 항목은 결함이 아니라 검증 범위의 한계다. 범위 밖 항목을 통과로 적지 않았다.
- 실제 문서 6회는 patch 단계에서 KO provider 호출 전에 실패했다. 따라서 모델별 실제 문서 번역 품질 비교는 불가능했고 provider fixture만 모델 응답 증거로 남았다.
- `act --dryrun`은 workflow graph와 step 구조를 해석했으며 어떤 실제 step도 실행하지 않았다.
- response contract tests의 issue 검증은 `assertIn` 중심이고 non-empty exact issue-list 단언이 없어 독립 방어력 평가는 제한적이다. table fallback의 successful match/replace와 fence 배제도 기존 test coverage가 없었다. 이는 N-06/N-17의 재현 근거로 사용했지만 별도 운영 결함으로 중복 집계하지 않았다.

## 10. 최종 판정과 다음 작업

최종 판정은 **merge 불가**, 부록 A.7은 **검증 미완료**다.

- `gpt-5.4-mini`: 0/3
- `gpt-5.6-luna`: 0/3
- provider fixture: mini 통과, luna JA 실패
- artifact/site/diff 명령: 6/6 통과(현 anchor validator의 JA coverage 결함은 N-14)
- 정식 no-op: 적용 가능 checkout 0개(선행 성공 0개)
- 실패 상태 진단 재실행: 0/6 성공
- 검증 중 생성 commit: 0건. 활성 HEAD와 6개 run HEAD 모두 `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a`로 불변
- push: 0건
- 이 실행이 만든 경로: `.review/translation-sync-validation-20260726-010820/`와 이 주 보고서. `dot_env`·`prompt.md`는 선행 사용자 파일이고, 별도 `.review/translation-sync-validation-20260726-010825/`와 supplement는 병행 산출물로서 수정하지 않음

다음 작업 우선순위:

1. F-01의 flat facade/package shadow를 제거하거나 명시적 호환 API로 문서화하고 import seam tests를 추가
2. N-05의 GFM/legacy note partial patch를 고친 뒤 같은 official upstream SHA로 두 모델 3회씩 재검증
3. N-14를 먼저 고쳐 JA 누락을 gate에 드러내고 N-15 alias 9건을 복구
4. N-06/N-16과 F-02/F-03/F-13/F-14/F-15의 contract·normalizer 불일치를 공통 parser 계층에서 수정
5. N-01~N-04, F-04, N-17/N-18의 silent mutation·candidate selection 회귀 tests 추가
6. N-07~N-13의 fail-closed·workflow·credential 경계와 N-19 README fence를 보강

커밋 분할을 한다면 파이프라인 코드 / 기획·운영 문서 / 생성 번역 산출물 / CI·배포 설정 경계가 가장 작고 검토 가능한 단위다. 이번 검증에서는 commit이나 분할 작업을 수행하지 않았다.
