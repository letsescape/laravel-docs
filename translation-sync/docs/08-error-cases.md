# 번역 동기화 오류 케이스 정리 (리팩터링 전 기록)

> [!IMPORTANT]
> 이 문서는 2026-07-15 리팩터링 전에 수집한 실패 사례와 당시 구현 상태를 보존한 역사 기록이다. 아래 상세 표의 코드 줄 번호와 "당시 동작"은 현재 사양이 아니다. 현재 운영 계약은 00~07 문서와 `docs/review/translation-sync-refactor-review-2026-07-15.md`의 후속 재검증 결과를 따른다.

이 문서는 기존 문서 갱신(부분 동기화) 경로에서 실행을 실패시키거나 산출물을 왜곡했던 케이스를 단계별로 정리한다. 각 케이스에 ID를 부여해 리팩터링 시 케이스별 명시 처리의 기준으로 사용했다.

케이스 수집 근거:

- GitHub Actions 실행 이력 (2026-06-23 ~ 2026-07-03, 실패 8건)
- 코드 전수 조사 (`sync/` 패키지의 모든 오류 발생 지점)
- 기획서(00~06) 대비 구현 격차 분석

---

## 현재 상태 (2026-07-26)

| 부류 | 후속 상태 |
|---|---|
| C군 | C1/C2와 숫자형 runtime option은 설정 단계에서 `ConfigError`로 정리하고 `main.py`가 짧은 메시지와 종료 코드 2로 처리한다. endpoint, deployment, API version의 provider별 유효성은 실제 provider 경계에서 확인한다. |
| I군 | 입력 전제가 모호하면 쓰지 않고 실패하는 fail-closed 동작을 유지한다. |
| P군 | 소유 단위 `PatchPlan`, named-section 재정렬, separator 보존과 관련 회귀 테스트를 추가했다. P8의 코드 블록 발산은 최종 검증에서 잡히지만 최초 실패 지점의 진단 개선 여지는 남아 있다. |
| T군 | 재시도 가능 오류와 비재시도 오류를 모두 `IncompleteTranslation`으로 정규화한다. 새 provider 응답은 적용 전에 공통 response contract를 통과하며, 최초 완료 응답을 포함해 블록당 최대 2개의 완료 응답을 평가한다(verification feedback 재요청 1회). 각 평가의 transport는 timeout·네트워크·429·5xx에 초기 호출 포함 최대 3회 시도하므로 물리 provider 호출 상한은 블록당 6회다. |
| R군 | 영어와 지원 locale의 legacy marker를 fenced code 밖에서 canonical `[!NOTE]` 계열로 변환하고, fenced code 밖 `{{version}}`만 치환해 R2/R3 및 review F-14의 직접 재현을 해결했다. marker 변환은 본문을 번역하지 않는다. 완료 감사에서 현재 산출물의 legacy marker 30개(지역화 28개, 영어 2개)를 정리하고 미번역 영어 본문 1개를 번역해 전체 annotation check를 통과시켰다. |
| V군 | 새 provider 응답의 누락·echo·추가 prose와 표·인용·HTML/JSX·front matter 구조는 response contract가 검사한다. final verifier는 적용 결과의 지원되는 링크와 single/double/괄호형 title, 가변 길이·여러 줄 inline code, fenced code, heading, 명시적 anchor, HTML image `src`와 동적 표시 expression, admonition 유형, 원문 주석을 검사한다. fence suffix, JSX image expression, inline code의 literal comment delimiter, 닫히지 않은 fence와 review F-15의 직접 무음 손상은 회귀 테스트로 고정했다. |
| S군 | sidebar generator가 label·순서·중복 category/link key와 doc id occurrence·source 존재·locale override 제거를 검증한다. master의 root API 문서 링크만 최신 안정 버전으로 바꾸는 동작은 현재의 의도된 계약이다. 지원하지 않거나 잘못된 sidebar 문법은 조용히 누락하지 않고 실패한다. `versions.json`도 `master` 선두, 내림차순, 중복과 JSON shape를 엄격히 검사해 review F-18을 닫았다. |
| A군 | live workflow의 fail-fast와 전체 커밋 생략은 안전 우선 정책으로 남아 있다. 단계 회귀는 자동 루프가 아니라 원인 수정 후 재실행하는 운영 절차다. 파일별 즉시 기록 때문에 로컬 실패 시 부분 결과가 남을 수 있는 transaction 한계도 남아 있다. |

---

## 0. 요약

| 단계 | 케이스 | 실패 단위 | CI 실제 발생 |
|------|--------|----------|:---:|
| 설정 | C1~C3 | 실행 전체 중단 | 2건 |
| 입력 전제 | I1~I3 | 문서 단위 / 전체 중단 | - |
| 세그먼트 분할·매칭 | P1~P8 | 문서 단위 (`partial patch failed`) | 3건 |
| 번역 provider | T1~T3 | 문서 단위 / 전체 중단 | - |
| 후처리·보정 | R1~R3 | 폴백 (일부 무음) | - |
| 검증 | V1~V18 | 문서 단위 (`verify failed`) | 3건 |
| 사이드바 | S1~S2 | 실행 전체 실패 | - |
| 구조적 증폭 요인 | A1~A4 | - | - |

실제 CI 건수는 **세그먼트 매칭 실패(P군)** 과 **검증 실패(V군)** 이 각 3건으로 공동 최다다. P군은 upstream 편집이 새로운 형태로 블록 경계를 가로지를 때마다 재발해 왔다.

---

## 1. 설정 단계 (C군) — 실행 전체 중단

| ID | 케이스 | 발생 지점 | 당시 동작 | 사례 |
|----|--------|-----------|-----------|------|
| C1 | `TRANSLATION_PROVIDER` 미설정 또는 허용값(`azure`/`cli`/`openai`) 외 | `runtime/config.py:46` | `ConfigError` — main.py가 잡지 않아 traceback으로 중단 | run 28049304728 (6/23), 28121537621 (6/24) — 시크릿 미설정, 이후 해결 |
| C2 | provider별 필수 env 누락 (예: `openai`인데 `OPENAI_API_KEY` 없음) | `runtime/config.py:60` | 동일 | - |
| C3 | env 값 형식 오류 미검증 — endpoint URL, API version, 모델명이 형식상 잘못돼도 통과 | `runtime/config.py` (검증 부재) | 번역 단계에서 provider 예외로 지연 표면화 | 기획서 01 §10 대비 격차 |

---

## 2. 입력 전제 (I군)

| ID | 케이스 | 발생 지점 | 당시 동작 |
|----|--------|-----------|-----------|
| I1 | 원문은 수정(M)인데 기존 ko/ja 번역 파일이 없음 | `main.py` (`missing existing translation for partial sync`) | 문서 단위 실패 |
| I2 | 변경 감지는 됐는데 diff hunks가 비어 있음 | `main.py` (`missing diff hunks for partial sync`) | 문서 단위 실패 |
| I3 | 프롬프트 파일(`prompt.md`/`prompt_jp.md`) 없음 | `translation/prompt.py:19` | `PromptError` — 실행 전체 중단 |

---

## 3. 세그먼트 분할·매칭 (P군) — `partial patch failed`

부분 동기화의 핵심 경로. diff hunk를 세그먼트로 나누고, 삭제 라인을 join한 문자열로 기존 번역의 HTML 주석 앵커를 찾아 교체/삽입/삭제한다. **매칭은 텍스트 휴리스틱이라 upstream 편집 형태에 따라 실패가 재발해 온 부류다** (patch.py: 2026-06-25 생성 후 fix 커밋 7건).

| ID | 케이스 | 트리거 | 발생 지점 | 상태 |
|----|--------|--------|-----------|------|
| P1 | **혼합 세그먼트**: 삭제 라인이 코드 블록 꼬리(`});`, ` ``` `)와 뒤따르는 산문 문단에 걸침 — 사이에 빈 컨텍스트 줄이 없으면 한 세그먼트로 묶여, join한 키가 어떤 주석 앵커와도 불일치 | upstream이 코드 블록 끝과 인접 문단을 함께 수정/삭제 | `patch.py _find_block` | run 28664138975 (7/3, billing.md 13.x). **e21f6a1로 해소** — 단 before/after 컨텍스트가 모두 존재하고 기존 문서에서 찾을 수 있을 때만 |
| P2 | **코드 라인이 앵커 키로 사용됨**: 코드 영역 감지(`_code_region_index`)를 통과하지 못한 코드 라인(예: `use Exception;`)이 old_lines가 되어 주석 앵커로 검색됨 | 코드 블록 내부 변경이 구조적 라인과 섞이거나 영역 판정 실패 | `patch.py _code_region_index`, `_find_block` | run 28184487386 (6/25, http-client.md). 당시 fix로 해소, 유사 변형 재발 가능 |
| P3 | **주석 불일치 문단**: 여러 문장·볼드 포함 문단이 기존 번역에서 여러 주석으로 쪼개져 있거나, 주석이 이전 원문 그대로라 최신 diff의 삭제 라인과 불일치 | upstream이 문단을 통째로 재작성 | `patch.py _find_block` | run 28183516363 (6/25, errors.md) |
| P4 | **부분 일치 모호**: 정확 일치 없고 부분 일치 후보가 2개 이상이면 매칭 포기 | 같은 문구가 문서에 반복 | `patch.py _matching_blocks` | 잠재 — 실패로 이어지면 P1~P3과 같은 메시지 |
| P5 | **삽입 컨텍스트 부재**: 추가 세그먼트의 before/after 컨텍스트를 블록·raw 라인 어느 쪽에서도 못 찾음 | 컨텍스트 자체가 이번 diff에서 함께 변경된 경우 등 | `patch.py:411` (`missing insertion context`) | 잠재 |
| P6 | **주석 앵커 손상**: 기존 번역의 HTML 주석이 잘못됐거나 닫히지 않음 | 과거 산출물 오염 | `patch.py:324, 338` | 잠재 |
| P7 | **번역 블록 수 불일치**: needs_translation 세그먼트 수와 번역 결과 수가 어긋남 (내부 불변식 위반) | 코드 결함 시나리오 | `patch.py:231, 237` | 잠재 |
| P8 | **코드 블록 발산 무음 스킵**: 코드 블록 교체 시 block_index가 범위 밖이거나 anchor 라인이 소실되면 **조용히 원본 유지** → 이후 검증에서 `code block mismatch`로 지연 표면화되어 원인 추적이 어려움 | 기존 번역의 코드 블록 수/내용이 원문과 발산 | `patch.py _apply_code_block` (침묵 `return text` 2곳) | 잠재 — 무음이라 미관측일 수 있음 |

---

## 4. 번역 provider (T군)

| ID | 케이스 | 당시 동작 | 비고 |
|----|--------|-----------|------|
| T1 | timeout / 네트워크 오류 / CLI 비정상 종료가 초기 요청 포함 총 3회 시도를 초과(시도 사이 최대 두 차례 5분 대기) | `IncompleteTranslation` → 문서 단위 실패 (`partial translation failed`) | 기획서 02 §9 부합 |
| T2 | 비재시도 예외 (인증 실패, 4xx 등) | main.py가 잡지 않아 **traceback으로 실행 전체 중단** | C군과 달리 분류·메시지 없음 |
| T3 | 응답은 정상 수신했으나 내용 불량 (사과문, 요약문, 코드펜스로 감싼 출력 등) | 이 단계에서 미검출 — 검증 단계에서 V군의 다른 이름으로 표면화 | 기획서 04 §17 "미완료 번역/provider 실패 게이트"가 verify.py에 없음 (격차) |

---

## 5. 후처리·보정 (R군) — 폴백 또는 무음

| ID | 케이스 | 당시 동작 | 비고 |
|----|--------|-----------|------|
| R1 | `RepairError` — 번역본 링크/heading 수가 원문 초과, 앵커 불일치 등 | 보정 포기, 원본 후보로 폴백 후 verify 이슈 최소 후보 선택 | 치명 아님. 남은 이슈는 V군으로 표면화 |
| R2 | `> **Note:** ...`(콜론이 볼드 내부) admonition 미변환 | 변환 실패하고 verify 정규식도 못 잡아 **무음 통과** | `postprocess.py _parse_note_line` 버그. 기획서 03 §6.4 예시가 그대로 실패 |
| R3 | `{{version}}`이 코드 블록 내부까지 무조건 치환 | 원문·번역 모두 동일 처리라 verify 통과 — **무음 왜곡** | 기획서 03 §7.5 예외 미구현 |

---

## 6. 검증 (V군) — `verify failed`, 문서 단위 실패

`verify.verify()`는 아래 중 하나라도 걸리면 issue를 반환한다 (빈 목록 = success). 코드 블록 내부는 잔존 패턴 검사에서 제외.

### 6.1 잔존 패턴 (source 없이 항상 검사)

| ID | issue 라벨 | 조건 | CI 사례 |
|----|-----------|------|---------|
| V1 | `unreplaced {{version}}` | `{{version}}` 잔존 | - |
| V2 | `unrestored base64 placeholder` | `__BASE64_IMAGE_n__` 잔존 | - |
| V3 | `legacy note marker` | 지원 type의 `> {note}` / `> **Note**` / `> **Note:**` / `> Note:` 잔존(영문 marker 기준) | - |
| V4 | `unclosed img tag` | self-closing 아닌 `<img>` | - |
| V5 | `title style class` | 제목 줄 `{.class}` 잔존 | - |
| V6 | `admonition body outside blockquote` | `> [!NOTE]` 다음 본문이 `>` 없이 시작 | run 28206132419 (6/25, search.md ja) |
| V7 | `duplicate admonition marker` | 마커 연속 중복 | - |

### 6.2 원문 대조 (엄격 — 완전 일치 요구)

| ID | issue 라벨 | 조건 | 엄격도 |
|----|-----------|------|--------|
| V8 | `link target mismatch` | 링크 target multiset 불일치 | 높음 |
| V9 | `link label mismatch` | 링크 label 순서 포함 불일치 | **매우 높음** |
| V10 | `link pair mismatch` | (label, target) 쌍 불일치 | 높음 |
| V11 | `inline code mismatch` | 인라인 코드 multiset 완전 일치 요구 | **매우 높음** |
| V12 | `anchor mismatch` | `<a name>` 앵커 multiset(발생 횟수 포함) 불일치 | 중간 |
| V13 | `code block mismatch` | 코드 블록 내용 완전 일치 요구 | **매우 높음** — P8 무음 스킵의 지연 표면화 지점 |
| V14 | `heading mismatch` | heading 레벨 시퀀스 불일치 | 중간 |
| V15 | `heading text mismatch` | heading 텍스트가 영어 원문과 완전 일치해야 함 | **매우 높음** |
| V16 | `list marker mismatch` | 번역본 목록 마커 수 < 원문 | 중간 |
| V17 | `front matter title mismatch` | front matter `title` 불일치 | 낮음 |
| V18 | `missing original comment` | 원문 모든 문단이 번역본 HTML 주석으로 존재해야 함 | **매우 높음** — run 28189054745, 28191751344 (6/25, mongodb.md) |
| V19 | `sentence cardinality mismatch` | 단순 source 문장의 소유 번역 줄에 원문 절 구조로 설명되지 않는 추가 문장이 붙음 | 높음 |
| V20 | `html display expression mismatch` | `alt` 등 표시 속성의 동적 expression에서 identifier·operator 구조가 바뀜 | 높음 |
| V21 | `source comment mismatch` | 구조 주석이 같은 모양의 다른 quote/table occurrence를 소유하거나 source 주석 뒤 본문이 비어 있음 | 높음 |

번역 산출물이 인라인 코드·코드 블록·heading·링크 label을 한 글자라도 바꾸거나 원문 주석을 하나라도 누락하면 즉시 실패한다. 품질 게이트로는 타당하나, A1(전량 커밋 스킵)과 결합해 실패 빈도를 증폭시킨다.

### 6.3 기획서 04 대비 당시 미구현 검증

- 미완료 번역 / provider 실패 텍스트 게이트 (§17) → T3 참고
- 표 구조, 인용문 연쇄, 열린 HTML 태그, 순서 목록 번호 (§10 일부)
- HTML `<img src>` 경로 보존 검사 (§8.1)
- 사이드바 정합성은 verify.py가 아닌 sidebar generator가 별도 수행

---

## 7. 사이드바 (S군)

| ID | 케이스 | 발생 지점 | 당시 동작 |
|----|--------|-----------|-----------|
| S1 | unknown/unsupported/invalid version, 저장소 밖 경로 | `sidebar/generator.py` (ValueError 다수) | 실행 전체 실패 |
| S2 | `missing source doc for sidebar item` — documentation.md가 존재하지 않는 문서를 참조 | `sidebar/generator.py` | sidebar sync failure로 실행 실패 |

참고: API 문서 링크 정규화가 master 버전에만 적용된다 (기획서 06 §3.3 문언과 상이 — 의도 확인 필요).

---

## 8. 구조적 증폭 요인 (A군)

개별 오류가 아니라, 오류의 빈도와 파급을 키우는 운영 구조.

| ID | 요인 | 내용 |
|----|------|------|
| A1 | **fail-fast + 전량 커밋 스킵** | 문서 1건의 세그먼트 1개 실패 → exit 1 → 커밋 단계 미실행 → 성공한 번역도 폐기. 다음 실행에서 미반영 diff가 누적돼 실패 확률이 더 올라갈 수 있다. workflow는 매월 홀수일 22:17 KST에 실행되므로 월 경계에서는 실행 간격이 정확히 2일이 아닐 수 있다. |
| A2 | **회귀 루프 미구현** | 기획서 00 §1.1은 검증 실패 시 원인 단계로 회귀해 재처리한다고 명시하나, 구현은 즉시 종료. `_repair_segment_translation`의 후보 선택이 제한적 대체물 |
| A3 | **무음 스킵의 지연 표면화** | P8, R2, R3처럼 실패 지점에서 조용히 넘어간 문제가 뒤 단계에서 다른 이름으로 나타나거나 산출물에 남음 — 진단 비용 증가 |
| A4 | **오류 메시지에 진단 컨텍스트 부재** | `PatchError`가 검색 키만 담고 케이스 분류·hunk 위치·세그먼트 종류를 담지 않아, 실패마다 수동 재현이 필요 |

---

## 9. 당시 리팩토링 방향 — 케이스별 명시 처리

현재 patch 경로는 "시도 → 실패 → 폴백" 연쇄(try/except 체인)라서, 어떤 세그먼트가 어떤 경로로 처리됐는지 불투명하고 새 형태마다 폴백을 추가해 왔다. 목표는 **분류를 먼저 하고, 분류된 케이스만 단일 경로로 처리하며, 미분류는 명시적으로 실패**시키는 구조다.

1. **세그먼트 분류기 도입**: 세그먼트 생성 시점에 kind를 확정한다 — `prose-block`(주석 앵커 교체) / `code-interior`(코드 블록 통째 교체) / `code-boundary-mixed`(P1: 코드 경계+산문 분리 처리) / `heading` / `anchor-section` / `deletion` / `insertion`. kind별 핸들러 1개, 폴백 체인 제거. 분류 불가 세그먼트는 "unclassified segment" 오류로 즉시 실패시켜 새 케이스를 조기에 드러낸다.
2. **실패 격리(문서 단위)**: 한 문서의 실패가 나머지 문서의 번역·커밋을 막지 않게 한다. 실패 문서는 목록으로 보고하고 성공분만 커밋 (fail-fast는 개발/디버그 옵션으로 유지).
3. **최후 폴백 재검토**: 매칭 불가 문서는 전체 재번역(status A 경로)으로 처리하는 옵션을 재도입한다. 788c39f에서 제거된 사유(비용·기존 번역 덮어쓰기)를 재평가해, "부분 패치 실패 시에만"으로 조건을 좁히면 결정적으로 성공하는 안전망이 된다.
4. **무음 스킵 금지**: P8의 침묵 `return text`를 명시적 오류 또는 최소한 stderr 로그로 바꾼다. R2/R3 버그 수정.
5. **오류에 진단 컨텍스트 포함**: PatchError에 케이스 ID, hunk 위치(old/new lineno), 세그먼트 kind, 검색 키를 담아 CI 로그만으로 분류·재현이 가능하게 한다.
6. **검증 게이트 보강**: T3(미완료 번역/사과문 잔존) 게이트를 verify.py에 추가해 기획서 04 §17과 위치를 맞춘다.
