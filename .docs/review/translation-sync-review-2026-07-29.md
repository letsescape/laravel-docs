# Translation Sync 미완료·개선 사항 리뷰 (d0a29b7)

검증 실행: 2026-07-29 KST
대상: `refactor/sync-docs`의 `d0a29b70d7d8421511ab64081ec43ed2daeb1077` ("refact")
범위: `main..HEAD` 단일 커밋, 77 files, +33,100 / −2,919
워킹 트리: 깨끗함 (로컬 변경 0, stash 0, 추가 worktree 0)

선행 문서: 같은 디렉터리의 리뷰 6개(`F-`/`N-`/`S-`/`V-` 계열). 이 문서의 신규 항목은 `R-`을 쓴다.

---

## 1. 최종 판정

**merge 불가 — 필수 게이트 2개가 현재 실패하고, 그중 하나는 배포와 번역 sync를 동시에 차단한다.**

단위 테스트 771개, 격리 replay, live provider contract, live end-to-end는 모두 통과한다. 이전 라운드의 headline blocker(admonition marker flip patch 실패)도 닫혔다. 그러나 CI가 실제로 실행하는 게이트 두 개가 red이고, 정확성 누출 3건이 남아 있다.

| ID | 심각도 | 요약 |
|---|---|---|
| R-01 | **P0** | JA alias 앵커 15개 누락 → `make site-check` exit 2 → **배포·sync 동시 차단** |
| R-02 | **P1** | `--check-annotations` 93건 실패 (27문서, 전 버전) |
| R-03 | **P1** | `repair`가 인라인 코드를 **위치 기준으로 강제 정렬**해 문장 의미를 역전시키고, `verify`는 Counter 비교라 구조적으로 탐지 불가 |
| R-04 | **P1** | 문장 단위 **부분 echo**가 계약·최종 verifier를 모두 통과해 미번역 영어가 출하된다 (S-15 재판정) |
| R-05 | **P1** | `verified_unchanged_locales`가 **raw EN**을 verify 기준으로 써서 비대칭 sync 구제 분기가 무력 (V-01b 재판정) |
| R-06 | **P1** | `data-translation-alias` 생성 코드가 파이프라인에 **없다** — KO 15개는 수작업, JA/EN 0개 |
| R-07 | **P1** | `--check-annotations` / `--annotate-existing`이 어떤 make target·CI에도 **연결되지 않았다** |

발견 총량: 60건 (P0 1 / P1 7 / P2 27 / P3 25). P0·P1은 전부 독립 반증 검증을 거쳤다(CONFIRMED 9, PLAUSIBLE 1, REFUTED 2 — 아래 §6).

---

## 2. 게이트 실측 결과

`d0a29b7` 그대로, 워킹 트리 수정 없이 실행했다.

| 게이트 | 명령 | 결과 |
|---|---|---|
| 정적 검사 | `git diff --check` + conflict marker 스캔 | 통과 |
| lockfile | `uv lock --check` | 통과 (18 packages, drift 0) |
| Python 단위 테스트 | `make translation-test` | **771 tests, OK** |
| 격리 replay | `make translation-check` | **exit 0** (sandbox 정상 제거) |
| 사이트 검증 | `make site-check` | **exit 2 실패** — R-01 |
| annotation corpus | `main.py --check-annotations` | **exit 1 실패 (93건)** — R-02 |
| live provider contract | `make translation-provider-check` | **exit 0** (KO/JA) |
| live end-to-end | 격리 clone, `--version 13.x --doc ai-sdk.md` | **exit 0** (KO/JA 번역 성공) |
| 산출 경로 (격리 상태) | `validate_generated_changes.py` | **exit 0** — `3 file(s) verified` |
| 재실행 수렴 | 동일 manifest 2회차 | diff 해시 **동일** (단서 아래) |

live 검증은 `dot_env`를 하위 프로세스 environment로만 주입해 운영과 동일한 설정(`openai`, reasoning `medium`)으로 수행했다. 값은 argv·로그·이 문서 어디에도 남기지 않았다. prompt SHA-256만 기록한다 — KO `92cc1c6e2ea2…`, JA `e2d5aea0b504…`.

**재실행 수렴 단서**: 2회차가 `no source changes to translate`에 도달하지 않고 다시 번역했으나 **결과 diff 해시는 바이트 동일**이다. 파이프라인이 `git status` 기반으로 변경을 감지하는데 1회차를 커밋하지 않아 2회차도 같은 delta를 보기 때문이며, 운영에서는 workflow가 1회차를 커밋하므로 발생하지 않는다. 구조적 멱등성은 성립한다.

**격리 artifact-check 통과의 의미**: 순수 생성 산출물만 있는 상태에서 `3 file(s) verified`로 통과했다. 정상 번역 경로에서 locale pairing이 오작동하지 않음을 확인한다(단, R-05의 별개 경로는 남아 있다).

---

## 3. P0 — R-01: JA alias 앵커 15개 누락

### 근거

```
Total anchor links:  46626
  OK (id in HTML):   46611
  id not found:      15
```

15건 **전부 JA**, KO 0건. `validate-anchors.mjs:82`가 `process.exit(2)`를 내므로 `make site-check`가 실패한다.

| 대상 | `data-translation-alias` 수 |
|---|---|
| KO (`versioned_docs/`) | **15** |
| JA (`i18n/ja/`) | **0** |

깨진 앵커 15건이 KO에만 있는 alias 15개와 정확히 대응한다.

### 회귀 경로

`645a2d4`는 현재 히스토리의 조상이 **아니다**(버려진 커밋). `d0a29b7`은 `3aab108` 위에 새로 작성됐고 `i18n/ja`를 전혀 건드리지 않았다.

| 커밋 | JA alias | KO alias |
|---|---|---|
| `3aab108` (main) | 0 | 15 |
| `645a2d4` (버려짐) | **6** | 15 |
| `d0a29b7` (현재) | **0** | 15 |

15건 중 **6건은 회귀**(유실), **9건은 원래부터 누락**(cross-document alias)이다.

유실된 6건:

```
version-10.x/controllers.md:203   #actions-handled-by-resource-controller
version-10.x/helpers.md:1088      #method-array-sort-recursive-desc
version-12.x/ai.md:156            #agents-integration
version-8.x/http-tests.md:735     #assert-similar-json
version-9.x/notifications.md:1401 #formatting-shortcode-notifications
version-master/ai.md:156          #agents-integration
```

원래 누락된 9건: `{8,9,10}.x` 계열의 `errors#logging`, `migrations#writing-migrations`, `10.x/helpers#fluent-strings`, `8.x/database-testing#writing-factories`, `8.x/eloquent-mutators##date-casting`(이중 해시 — 원문 오타 보정).

### 왜 지금 드러났는가

이전 라운드에서 `anchor-routes.mjs`가 JA 절대 경로를 KO 빌드로 검증하던 결함이 수정됐다. **수정이 제대로 작동해서 숨어 있던 JA 깨짐이 노출된 것**이다. 검증기는 정상이고 데이터가 미비하다.

### 영향

`make site-check`는 두 workflow의 유일한 사이트 게이트다.

- `deploy.yml:53` → **배포 차단**
- `sync-translation.yml:114` → 이후 단계인 commit/push에 도달 불가 → **자동 번역 sync 차단**

### 권고

KO의 alias 15개를 JA에 대칭 반영한다. 6건은 `645a2d4`에서 이식 가능하고, 9건은 KO 배치 위치를 따라 신규 추가한다. 근본 해결은 R-06(생성 코드 부재)이다.

### 완료 조건

`make site-check` exit 0, `id not found: 0`, KO/JA alias 차집합 0.

---

## 4. P1 상세

### R-02. annotation corpus 93건 실패

`main.py --check-annotations` → exit 1, **93건 / 27개 문서**.

| 실패 유형 | 건수 |
|---|---:|
| `source comment mismatch` | 38 |
| `missing original comment` | 30 |
| `legacy note marker` | 12 |
| `inline code mismatch` | 4 |
| `untranslated source text` | 3 |
| `sentence cardinality mismatch` | 2 |
| `link pair mismatch` / `link label mismatch` | 2 / 2 |

로케일 ko 49 / ja 44, 버전 8.x~master 전역(10.x 22, 8.x 19, 9.x 13, 13.x 12, master 11, 12.x 11, 11.x 5).

**원인 분류**: 93건 중 **71건이 후처리 미재적용 drift**(산출물이 현재 postprocess 결과와 다름)이고, 나머지 22건이 별개 원인 4종이다. 그중 16건은 `vite.md`의 **목록 항목 다중 행 블록 주석**을 verify가 인식하지 못하는 것(4개 버전 × ko/ja)이고, 일부는 한국어 괄호 병기(용어 원어 표기)를 `untranslated source text`로 오탐하는 것이다.

§11.3이 명시하듯 이 실패를 locale 주석 삭제로 숨기면 안 된다. 71건은 재생성으로, 22건은 verify 계약 수정으로 접근해야 한다.

### R-03. repair가 인라인 코드를 위치 기준으로 강제 정렬한다 (신규, CONFIRMED)

`repair`가 번역문의 인라인 코드 스팬을 **원문 순서에 맞춰 위치 기준으로 재배치**한다. 한국어·일본어는 어순이 영어와 다르므로, 정당하게 순서가 바뀐 번역에서 **스팬 내용이 서로 뒤바뀌어 문장 의미가 역전**된다.

`verify`의 인라인 코드 검사는 `Counter` 기반 multiset 비교이므로 **순서 변화를 구조적으로 탐지할 수 없다.** 즉 이 손상은 어떤 게이트도 잡지 못하고 그대로 출하된다.

같은 문제가 링크에도 있다 — `repair`가 링크 label/target을 위치 기준으로 재배치해, 계약이 정당한 어순 변경까지 과잉거부하도록 강제한다(P2).

**권고**: 위치 기준 정렬을 내용 기준 매칭으로 바꾸거나, 순서가 바뀐 경우 fail-closed로 거부한다. `verify`에 순서 민감 검사를 추가한다.

### R-04. 문장 단위 부분 echo가 전 게이트를 통과한다 (S-15 재판정, CONFIRMED)

`response_contract.py:1683-1703`의 `contains_untranslated_source_phrase`는 소스 블록 **전체**의 word sequence가 번역문에 연속으로 나타날 때만 True다. 따라서 **두 문장짜리 문단에서 첫 문장만 verbatim으로 남기면 발동하지 않는다.**

실측: 첫 문장을 영어 그대로 두고 나머지를 한국어로 번역한 입력에 대해 `response_contract.verify(...) == []`, `verify.verify(...) == []`.

이전 라운드가 인용한 `source_body in translated_body`는 HEAD에 더 이상 없다. 구두점·대소문자 우회는 word-sequence 방식으로 닫혔으나 **부분 echo는 열려 있다.** 게이트 불편이 아니라 **정확성 누출**이다.

**권고**: echo 검사를 문장 단위(또는 n-gram 창)로 내린다. 최소한 문장이 2개 이상인 블록은 각 문장을 개별 키로 검사한다.

### R-05. `verified_unchanged_locales`가 raw EN을 기준으로 쓴다 (V-01b 재판정, CONFIRMED)

`validate_generated_changes.py:152-160`이 `source.read_text()`(raw EN 캐시)를 그대로 `verify.verify(...)`에 넘긴다. 파이프라인의 올바른 기준은 `main.py:535-539`의 `_expected_source()`(preprocess → postprocess)이며 `main.py:548`의 annotation check는 이 기준을 쓴다.

실측 (13.x 103문서): raw EN 기준 clean **ko 7 / ja 7**, `_expected_source` 기준 clean **ko 99 / ja 100**. 그 결과 구제 분기가 반환한 항목은 206개 중 **14개뿐**이다.

**영향**: `validate_generated_changes.py:113-118`의 `unverified unchanged translation` 구제 분기가 96/103 문서에서 발동하지 못한다. `sync-translation.yml:117`의 artifact-check가 `:120` commit보다 앞서므로 EN만 바뀌고 로케일이 바이트 동일한 sync가 커밋되지 않는다.

**권고**: 두 곳이 같은 헬퍼(`_expected_source`)를 공유하게 만든다.

### R-06. alias 생성 코드가 파이프라인에 없다

`data-translation-alias` 앵커를 생성하는 코드가 **어디에도 없다**. KO 15개는 수작업으로 넣은 것이고 JA·EN은 0개다. R-01이 반복되는 구조적 원인이다.

**권고**: alias 생성을 파이프라인 단계로 편입하거나, 최소한 KO/JA 대칭성을 강제하는 검사를 추가한다.

### R-07. 코퍼스 유지보수 명령이 CI에 연결되지 않았다

`--check-annotations`와 `--annotate-existing`이 **어떤 make target에도, 어떤 workflow에도 없다.** §11.3이 필수 게이트로 지정했지만 자동 실행 경로가 없어 93건이 누적될 때까지 아무도 몰랐다.

**권고**: `make translation-annotations` 같은 target을 만들고 `translation-check`에 편입하거나 CI에 단계로 추가한다.

---

## 5. 이전 리뷰 항목 재판정

### 해결된 것

| 항목 | 근거 |
|---|---|
| V-02 (link title 앞 공백) | 파서가 구분 공백 유지 |
| V-05 (title 위조 무검출) | 검출됨 |
| F-15(c) (title 값 보존) | repair가 3형태 모두 복원 |
| S-04 재현 입력 | `13.x/queries.md` 11건은 `_is_protected_source_phrase`가 True를 반환해 계약 통과 |
| F-18 (versions.json 순서·중복) | `versions.py:17-42`가 master 선두·중복·내림차순 전부 검증 |
| F-12 (action SHA pin) | workflow action 8개 전부 full SHA |
| F-11 (Azure API version) | 하드코드 없음 |
| independent N-05 (multiline comment) | 위조 검출됨 |
| independent N-06 (manifest exit code) | `sync-translation.yml:73-84`가 status 보존 |
| `test_replay` 약화 단언 | `assertEqual(iterdir,[])`가 성공 경로에 유지되고 `assertFalse(exists())`는 조기거부 경로라 오히려 더 강함 |
| admonition marker flip patch 실패 | live end-to-end에서 KO·JA 모두 정상 번역 |

### 그대로 또는 부분

V-01a(P2, EN 미변경 단일 로케일 수정 거부), V-03(P2, transient 실패 표본 절반이 재시도 없이 1회 실패), V-07(P2, 계약 실패 시 provider 응답·블록 인덱스 미기록), F-09(P2, run 전체 transaction 경계 없음 — ko 기록 후 ja 실패 시 반쪽 상태 잔존), F-14(P2, 리터럴 3개만 처리하고 전부 NOTE로 매핑), F-15(a)(P2, multi-backtick delimiter 폭 변경 무음 통과), F-15(d)(P3, 들여쓴 legacy quote marker 미처리), S-09(P3, `TRANSLATION_CLI_COMMAND` 형식 오류 오분류), F-17(P3, cron·direct push 외부 조건 의존).

### 판정이 뒤집힌 것 — V-06

이전 라운드는 `provider inline code mismatch`를 "순손실, 고유 검출력 0"으로 판정했다. **이번 반증 검증에서 REFUTED됐고 심각도가 P3으로 내려갔다.**

이유: 이 검사는 **R-03(repair의 위치 기반 재배치)이 스팬 순서를 바꾼 응답을 조용히 오염시키는 것을 막는 유일한 가드**다. `verify`가 Counter 비교라 순서를 못 보므로, 계약 단계의 이 검사를 제거하면 R-03의 손상이 무검출로 출하된다.

따라서 **V-06을 제거하라는 이전 권고는 철회한다.** 올바른 순서는 R-03을 먼저 고치고(위치 기반 정렬 제거), 그 다음에 이 검사의 필요성을 재평가하는 것이다.

`V-04`(fence 내부 표 행)도 증상은 재현되나 원인 귀속이 정정됐다 — `_table_regions`의 fence 제외가 아니라 `patch.py:2620-2640`의 `_has_structural_lines`가 fence 내부 여부와 무관하게 `|`·`>`·TOC·anchor 라인을 structural로 판정하는 것이 원인이다. 심각도는 P2로 조정됐다(코퍼스 실재 8문서).

---

## 6. 반증 검증 결과

P0/P1 후보 12건을 독립 에이전트가 **반증을 목표로** 재검증했다.

| 판정 | 건수 |
|---|---|
| CONFIRMED | 9 |
| PLAUSIBLE | 1 |
| REFUTED | 2 |

REFUTED 2건은 V-06(위 §5)과 "거부 테스트 94%가 사유를 고정하지 않는다"(→ P3으로 하향)이다. 심각도가 조정된 것: V-04 P1→P2, PR CI 부재 P1→P2, issue 게이트 미검출 P1→P2, `.dockerignore` P1→P2.

---

## 7. P2 / P3 요약

### 인프라·CI (P2 중심)

- **PR CI workflow 부재** — 771개 테스트와 site-check가 PR에서 한 번도 돌지 않는다
- **`.dockerignore`가 중첩 `.env` 미제외** — `translation-sync/.env`가 Docker 이미지 레이어에 복사된다
- `deploy.yml` checkout이 write credential을 남긴다(저장소 자체 문서화된 정책 위반)
- e2e(Playwright)가 어떤 workflow에서도 실행되지 않는다
- 프로덕션 배포 빌드만 `NODE_OPTIONS` heap 확장 없이 실행(OOM 이력이 문서에 있음)
- `make translate`(Docker 경로)가 manifest pinning과 모든 gate를 우회
- dependabot이 npm·github-actions만 커버(Python·Docker base image 제외)
- README의 Docker 실행 명령이 동작하지 않음(CMD가 서버가 아니라 빌드)
- job에 `timeout-minutes` 없음 — live provider 호출이 걸리면 최대 6시간 소모
- `.review/`가 여전히 `.git/info/exclude`에만 있고 `.gitignore`에 없음(머신 로컬 제외)

### 코드 품질 (P2/P3)

- `restore_list_markers`가 소프트랩 문단을 불릿 3개로 바꾸고 그것을 잡을 유일한 verify 신호를 스스로 지운다
- `verify.py`만 CommonMark 토크나이저로 옮기고 `repair.py`는 순진한 백틱 regex에 남아 두 모듈이 구조적으로 발산
- repair의 주석/펜스 상태머신이 단락평가 탓에, 코드펜스 안 미종료 HTML 주석이 닫는 펜스와 문서 나머지를 삼킨다
- `verify.py`와 `response_contract.py`가 같은 이름의 파서 헬퍼 8쌍을 서로 다른 본문으로 중복 구현, `verify`가 상대 모듈 private 심볼 13개를 직접 import
- 경로 보안 `_has_symlink_component` 2중 복제, `_split_line_ending` 3중 복제
- 정적 타입 체커 부재 — `patch.py`의 `DiffLine` 미정의 참조 7곳이 통과
- 검증 게이트 9곳의 `zip(..., strict=False)`가 블록 수 불일치 시 꼬리를 조용히 제외
- 데드코드 5건

### 테스트 판별력 (P1/P2)

- `verify()`/`response_contract.verify()`의 **issue 게이트 8개가 어떤 테스트로도 검출되지 않는다**
- **표 행 fallback 경로**(`_table_row_matches_context`, narrowed 모호성 가드)가 프로덕션에서 도달 가능한데 **테스트 0건** — 직전 라운드 지적 미수정
- `replay.py`의 저장소 이탈 가드·manifest 부모 TOCTOU 가드에 사유 단언 테스트 없음
- 호출되지만 테스트가 도달하지 않는 함수 5개
- sidebar 공개 API `resolve_versions`/`sync_versions`가 한 번도 실행되지 않고, 유일한 프로덕션 호출부는 항상 mock
- bool 판정 함수 224개 강제 뮤턴트 중 **36개 생존**
- issue 게이트 69개 중 29개가 단일 테스트에만 의존

### locale·사이트 (P2/P3)

- verify의 untranslated-source-text 검사가 한국어 괄호 병기를 오탐
- annotation check와 anchor check가 서로 다른 파일 집합을 잡음 — 어느 한쪽만으로는 코퍼스를 게이트할 수 없다
- `eloquent-mutators.md`의 `id="#date-casting"` alias는 원문 오타를 잘못된 방식으로 덮은 것
- `relativeTargetPath`가 `/docs/`로 시작하지 않는 절대 경로에 locale prefix를 붙이지 않음(잠재)
- `validate-anchors`의 `walkMd`가 빌드 exclude 목록과 어긋남

---

## 8. 권장 처리 순서

1. **R-01** — JA alias 15개 반영. 배포·sync를 막고 있으므로 최우선이다.
2. **R-03** — repair의 위치 기반 인라인 코드 정렬. 무검출 의미 손상이며 V-06 판단의 전제다.
3. **R-04** — 문장 단위 echo 검사. 미번역 영어 출하를 막는다.
4. **R-02** — annotation 93건. 71건(후처리 재적용)과 22건(verify 계약)을 분리해 접근한다.
5. **R-05** — `verified_unchanged_locales` 기준을 `_expected_source`로 통일.
6. **R-06 · R-07** — alias 생성 파이프라인 편입, 코퍼스 게이트 CI 연결. 재발 방지 조치다.
7. **PR CI workflow 추가**와 **`.dockerignore` 중첩 `.env`** — 인프라 P2 중 영향이 크다.
8. 테스트 판별력 보강 — issue 게이트 8개, 표 행 fallback, 뮤턴트 생존 36건.

R-03을 고치기 전에는 V-06(`provider inline code mismatch`)을 제거하지 말 것.

---

## 9. 로컬 상태 처분 내역

`.docs/system-prompt.md` §1.3에 따라 재고했다.

| 항목 | 상태 | 처분 |
|---|---|---|
| unstaged / staged 변경 | 없음 | 해당 없음 |
| stash | 없음 (이전 세션의 `!!GitHub_Desktop` stash가 정리됨) | 해당 없음 |
| 추가 worktree | 없음 (메인 1개) | 해당 없음 |
| ignored 산출물 | `.env`, `dot_env`, `node_modules/`, `.venv/`, `.review/`, `.remember/`, `.idea/`, `.husky/_/`, `.serena/`, `.github/workflows/CLAUDE.md` | **보류** — 정상 로컬 산출물·도구 설정. 이번 작업 산출물은 `.review/session-20260729/`에 격리 |
| `.docs/review/*.md` | 기존 6개 | **보존** — §1.3 제거 예외. 이 문서를 7번째로 추가 |

활성 저장소에 commit·staging·push·PR·worktree·stash 생성은 **0건**이다. 검증 산출물은 전부 ignored인 `.review/session-20260729/` 아래에 있다.

---

## 10. 검증 한계

- **93건 annotation 실패의 개별 문서별 수정 방향은 확정하지 않았다.** 유형·분포·영향 문서(27개)와 71/22 원인 분리까지 확정했다.
- **live 표본은 문서 1건**(`13.x/ai-sdk.md`) 1회다. 간헐적 contract 거부의 빈도는 이 표본으로 추정할 수 없다.
- **문서↔구현 정합 감사(00~08)는 미완료다.** 담당 조사 에이전트가 stall로 실패했다. 다른 5개 영역은 완료됐다.
- **Azure adapter 경로 미검증** — `dot_env`에 Azure 키가 없다.
- **E2E 미실행**.
- **no-op 마커 미도달**은 커밋 금지 제약에서 비롯된 절차적 한계이며 결함으로 판정하지 않았다(결과 diff 해시 동일로 멱등성 확인).
- P2·P3 항목은 반증 검증을 거치지 않았다. P0·P1만 독립 재검증했다.
