# Translation Sync 수정본 검증 보고서

검증 실행: 2026-07-26 KST
검증 대상: `refactor/sync-docs`의 **`645a2d4` + 로컬 미커밋 수정 38개 파일** (+1,907 / −215)
검증 지시서: 프로젝트 루트 `prompt.md`
workspace: `.review/verify-fixes-20260726-104813/`

---

## 0. 이 문서의 위치와 ID 조정

`645a2d4`에 대해 **세 개의 독립 리뷰**가 이미 존재하고, 그 지적사항을 반영한 **로컬 수정**이 들어왔다. 이 문서는 **그 수정이 실제로 결함을 닫았는지**를 검증한다.

| 문서 | 범위 | finding 접두사 |
|---|---|---|
| `translation-sync-refactor-review-2026-07-15.md` | 선행 보고서 (워킹 트리 기준) | `F-xx` |
| `translation-sync-refactor-verification-2026-07-26.md` | `645a2d4` 검증 (주 보고서) | `N-01`~`N-19` |
| `translation-sync-refactor-verification-2026-07-26-supplement.md` | `645a2d4` 검증 (보완) | `S-01`~`S-14` |
| `translation-sync-refactor-verification-2026-07-26-independent.md` | `645a2d4` 검증 (독립) | `N-01`~`N-06` ← **주 보고서와 충돌** |
| **이 문서** | **수정본 검증** | 새 결함은 `V-xx` |

**주의: 주 보고서와 independent 문서가 같은 `N-01`~`N-06` 표기를 서로 다른 결함에 쓴다.** 아래 모든 표에서 출처 문서를 반드시 병기한다.

이 문서는 기존 세 문서를 수정하지 않는다.

---

## 1. 결론

**판정: 큰 폭의 개선. 다만 merge 전 P1 회귀 1건을 닫아야 하고, A.7 완료 조건은 여전히 미충족이다.**

- 세 리뷰가 공통으로 지목한 **headline blocker가 닫혔다.** `partial patch failed: missing existing translation block for: > [!NOTE]`는 이전 라운드에서 두 모델 6/6이 결정론적으로 막혔고 fixture 아티팩트 가설까지 기각됐던 항목인데, 수정본에서는 실제 문서가 KO·JA 모두 번역돼 통과한다.
- finding 26건 중 **16건 closed / 8건 partial / 5건 not_fixed**(중복 집계 포함).
- 그러나 수정이 **새 회귀 7건**을 만들었고, 그중 확실한 P1은 **V-06**(신규 `inline code mismatch` 계약 검사가 repair가 치유하던 것을 앞질러 차단하며 고유 검출력은 0)이다. V-01b(locale pairing이 파이프라인 산출물을 거부)도 P1 후보지만 재현 1건에 근거하며 직접 확인하지 못했다. V-02는 **현재 워크트리에서 이미 해소**됐다.
- live A.7은 **3/6**(mini 2/3, luna 1/3)이다. 실패 성격이 이전 라운드와 근본적으로 다르다 — 결정론적 차단이 아니라 **간헐적 거부**다. 판별 결과 **luna 2회는 provider의 실제 계약 위반**(과잉거부 아님)이고, **mini 1회는 V-06 회귀**다.
- 과잉거부율은 6.80% → 0.72%로 내려갔으나, **개선분은 사실상 전부 S-02(quote) 몫**이고 S-04가 겨냥한 paragraph 슬라이스는 6건 해소·6건 신규로 **순변화 0**이다.

---

## 2. 검증 스냅샷

| 항목 | 값 |
|---|---|
| 기준 커밋 | `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a` |
| 검증 대상 | 위 커밋 + **로컬 미커밋 수정 38 files** (+1,907 / −215) |
| 수정 범위 | 코드 13, 테스트 11, JA 문서 9, `.gitignore`·`.dockerignore`·workflow 2·README |
| Docker / Compose | 29.1.3 / v5.0.1 |
| Node / npm | v26.5.0 / 11.17.0 |
| Python / uv | 3.14.6 / 0.11.31 |
| upstream | `laravel/docs` 13.x `b0b1c3e17c715880e0c380cd30061da6ca952c9d` |
| provider | `openai`, reasoning `medium` |
| 활성 브랜치 commit·push | **0건** |

### 2.1 수정본을 검증 대상에 싣는 방법 (중요)

`prompt.md`의 절차는 모든 checkout을 `git clone` + `checkout --detach 645a2d4`로 만든다. **clone은 커밋된 객체만 옮기므로, 미커밋 수정 38개 파일은 checkout에 실리지 않는다.** 이 상태로 파이프라인을 돌리면 수정 이전 코드를 검증하고 "여전히 실패"라는 잘못된 결론에 이른다.

§0.2가 어떤 저장소에서도 commit을 금지하므로, 임시 커밋 대신 **patch 전송**을 썼다.

```
git diff 645a2d4 -- translation-sync/ i18n/ .github/ .gitignore .dockerignore README.md > local-fixes.patch
# 각 checkout: git apply local-fixes.patch
```

그리고 **모든 run checkout에서 `patch.py`의 SHA-256을 워크트리와 대조**해 수정본이 실제로 실렸음을 증명했다.

| 대상 | `patch.py` SHA-256(앞 16자) |
|---|---|
| `645a2d4` | `ff889b98a8bd4f6a` |
| patch 적용 후 checkout | `d5dc13c38cb029a5` |
| 워크트리 | `d5dc13c38cb029a5` |

### 2.2 검증 대상이 움직였다 (중요)

검증 중에도 워크트리 수정이 계속 추가됐다. 이 보고서의 범위는 **patch를 추출한 10:48 시점의 38개 파일**이며, 그 스냅샷이 곧 Docker 이미지 `laravel-docs-translation-fixes:local`(md5 일치 확인)이고 live 6회를 돌린 코드다.

patch 추출 이후 들어온 변경(이 검증에 **포함되지 않음**):

| 시각 | 파일 | 내용 |
|---|---|---|
| 11:44 | `response_contract.py`, `verify.py` | `strip_inline_code`, `_protected_ascii_letter_allowance`, `_markdown_link_signatures`(link target/label/pair/title 4종 신규 거부), `_html_img_sources`, 미종료 fence 처리, `_source_comments_are_preserved` ownership 추가 패스 |
| 11:48 | `test_verify.py` | 위 변경에 대응 |
| (이후) | `Makefile` | `uv run --frozen` → `--locked` |

11:44 변경은 아래 §5의 일부 항목에 영향을 준다. 해당 항목마다 명시했다.

**현재 워크트리에 대해 추가로 확인한 것** (전체 검증은 아니고 두 가지만):

| 검사 | 결과 |
|---|---|
| 단위 테스트 | **Ran 550 tests, 실패 1건** (10:48본 464에서 +86). 유일한 실패는 `test_missing_manifest_preserves_nonzero_preflight_status`가 `/app/.github/workflows/sync-translation.yml`을 읽으려다 나는 `FileNotFoundError`로, **Dockerfile.translate가 `.github/`를 COPY하지 않는 환경 제약**이다. 코드 결함이 아니다 |
| link title 파싱 | **V-02가 해소됐다**(아래) |

#### patch 전송의 두 번째 함정 — untracked 신규 파일

`git diff`는 **추적 파일의 변경만** 담는다. 현재 워크트리에는 새 모듈 `translation-sync/sync/common/versions.py`가 **untracked로** 추가돼 있어 patch에 실리지 않았고, 그 결과 옮긴 checkout에서 다음이 났다.

```
ModuleNotFoundError: No module named 'sync.common.versions'
→ Ran 33 tests, errors=15   (대부분의 테스트 모듈이 import 단계에서 실패)
```

**워크트리 자체는 정상이다**(호스트에서 `from sync import verify` 성공). untracked 파일을 함께 복사한 뒤 550 tests가 정상 수집됐다. §2.1의 clone 함정과 같은 계열이므로, 이 절차를 재현하는 사람은 **`git diff` + untracked 파일 복사**를 함께 해야 한다.

---

## 3. Gate 결과표

| # | gate | 645a2d4 결과 | 수정본 결과 | 판정 |
|---|---|---|---|---|
| 2.1 | Python 단위 테스트 | 419 passed | **464 passed, OK** (+45) | PASS |
| 2.2 | replay 계약 | 미실행(commit 금지) | 미실행(동일 사유) | 미실행 |
| 2.4 | 산출 경로 검사기 | exit 0 (smoke) | **하네스 제약으로 직접 판정 불가** (아래) | 대체 검사 통과 |
| 2.5 | Markdown 링크 유틸 | fail 0 | fail 0 | PASS |
| 2.6 | typecheck + build + anchor | 46,626 / 46,626 | 6개 run 전부 exit 0 | PASS |
| 2.7 | 공백/충돌 마커 | 무출력 | 6개 run 전부 무출력 | PASS |
| 2.8 | provider contract | 두 모델 PASS | (이번 라운드 미재실행) | — |
| 2.9 | 실제 문서 end-to-end | **0/3, 0/3** | **2/3, 1/3** | 미충족 |
| A.6 | no-op 재실행 | 0/6 | 조건 미충족 — 단 원인은 절차(§8) | 미충족 |

### A.7 최종 완료 판정 — **검증 미완료**

| 조건 | 결과 |
|---|---|
| `gpt-5.4-mini` 3/3 | **미충족 (2/3)** |
| `gpt-5.6-luna` 3/3 | **미충족 (1/3)** |
| 6 run artifact/site/diff gate | site·diff 6/6 통과. artifact는 하네스 제약으로 직접 판정 불가, 대체 검사 통과 |
| 6 run no-op 재실행 | **미충족** — 다만 원인은 지시서 절차의 구조적 한계(§8) |
| 활성 브랜치 commit·push 0건 | **충족** |
| 변경이 `.review`와 보고서에만 존재 | **충족** |

실패 표본을 지우거나 성공할 때까지 재시도하지 않았다.

### 2.4가 "직접 판정 불가"인 이유

`validate_generated_changes.py`는 `git ls-files --others` + `git diff`로 워크트리 변경을 검사한다. 이 검증은 수정본을 **patch로 주입**했으므로, 주입된 38개 파일이 전부 `unexpected translation sync changes`로 잡힌다. 이는 파이프라인 결함이 아니라 검증 방식의 산물이다.

대신 **번역이 실제로 만든 변경만** 추려 확인했다(주입 파일 제외).

```
i18n/en/.../version-13.x/ai-sdk.md      (원문 캐시)
i18n/ja/.../version-13.x/ai-sdk.md      (JA)
versioned_docs/version-13.x/ai-sdk.md   (KO)
```

허용 경로이며 KO/JA가 쌍으로 대칭이다. **산출 경로 규율 자체는 정상이다.**

다만 이 과정에서 별개의 사실이 드러났다 — 강화된 validator가 `unpaired translation document` 10건을 보고했고, 그 대상이 이번 수정이 **의도적으로 JA에만 추가한 alias 문서 9개**였다. 이것이 V-01이다.

---

## 4. finding별 수정 상태

출처 문서를 병기한다. 근거는 모두 실측이다.

### 4.1 Closed (16건)

| 출처 · ID | 내용 | 닫힌 근거 |
|---|---|---|
| 주 N-05 / 보완 A.5 | `missing existing translation block for: > [!NOTE]` | 원인이 특정됨 — 새 admonition **삽입**이 아니라 **marker kind flip**(`[!NOTE]`→`[!WARNING]`)이었다. 코퍼스 측정: 13.x 103문서의 note_flip 78건이 645a2d4에서 **전부 실패** → 수정본에서 **76건 성공**(잔여 2건은 수정 전에도 실패하던 기존 미동기 문서). `is_admonition_marker_change`를 `return False`로 되돌리면 신규 테스트 3건이 실패 |
| 주 N-01 | TARGET 판정이 빈 신규 본문·삭제 orphan을 성공 처리 | 두 갈래 모두 fail-closed. `annotated block is missing its translated body` / `deleted source translation remains outside its annotated block`. 코퍼스 500건에서 과잉발동 0건 |
| 주 N-03 | 중복 named anchor가 count만 맞으면 위치 drift 허용 | 삭제·삽입 두 방향 모두 거부. `_anchor_occurrence_at_context` 무력화 시 테스트 2건 실패 |
| 주 N-04 | upstream version token 미검증으로 EN_ROOT 밖 쓰기 | 쓰기 전 거부 확인 |
| 주 N-08 | clone 실패 traceback 탈출 / 없는 branch skip 후 exit 0 | 두 경로 모두 정제된 non-zero |
| 주 N-09 | config 검증이 upstream 뒤 | `main.py:695`(config) < `:701`(upstream). 실제로 EN 캐시가 clean하게 남음 |
| 주 N-13 | replay interrupt 시 불완전 sandbox 잔존 | 닫힘 |
| 주 N-14 / 보완 S-01 (P1) | `validate-anchors.mjs`가 JA 절대 링크를 KO 빌드로 검증 | `anchor-routes.mjs`가 localePrefix를 절대 경로에도 적용. 2로케일 풀 빌드 2회 + 4셀 매트릭스로 확인 |
| 주 N-15 / 보완 S-05 | JA에 alias 앵커 9개 누락 | 9개 문서에 `data-translation-alias` 추가됨 |
| 보완 S-07 / 주 N-18 | TOC 접두부 문서에서 reorder 미발동 | 코퍼스 측정: **645a2d4 41/99 → 수정본 99/99 발동**. 무관한 접두부 변경은 여전히 거부 |
| 보완 S-08 | `_code_plan_state` fail-open 비대칭 | `plan_state`와 동형이 됨. 로컬 drift 코드가 조용히 소실되던 것이 이제 거부됨. docstring도 갱신 |
| 보완 S-12 | `sync.sidebar` 속성 shadowing | `from . import sidebar` + `sidebar/__init__.py` re-export. `sidebar.sync_versions` 정상, `import sync.sidebar.generator`도 이제 동작. **회귀 없음** |
| independent N-01 | 중복 annotation 뒤 EOF 구조 삽입 위치 오류 | occurrence-aware `_context_anchor_block`로 해소 |
| independent N-02 | 후행 admonition/table 뒤 fenced code 삽입 순서 | 닫힘 |
| F-18 | `versions.json` 순서·중복 자동 검증 | `generator.py` +23이 닫음 |
| — | **`apply_plan` 앵커 시퀀스 동일성 불변식 유지** | 새 table_row 경로가 이 전역 불변식을 우회하지 않음을 확인 |

### 4.2 Partial (8건)

| 출처 · ID | 남은 부분 |
|---|---|
| 주 N-02 / 보완 S-06 | 결함 자체는 fail-closed로 닫혔으나, 실제로 막는 것은 `TableRowChange.row_count` 구조 검사이지 새 helper `_table_row_matches_context`가 아니다. 구조 참조를 못 쓰는 fallback 경로(13.x 단일행 변경 101건 중 **6건**)에서 helper만 되돌리면 sibling 행을 여전히 덮어쓴다. 즉 helper는 테스트로 고정되지 않았다 |
| 주 N-17 / 보완 S-11 | 표 경로 테스트 0건은 해소(6건 추가). 그러나 `test_candidates_exclude_rows_inside_code_fences`가 **이름과 달리** fence 제외를 고정하지 않는다 — fence 제외를 삭제해도 106건 전부 통과한다. 게다가 이 fence 제외가 V-04 회귀의 원인이다 |
| 주 N-07 | validator가 version membership·삭제 규모를 보게 됐으나 과대·과소가 함께 남음(V-01 참조) |
| 보완 S-04 / 주 N-06 | 문서화된 재현 입력(`**Supported providers:** Anthropic, Gemini`)은 통과하게 됐다. 그러나 **정상 번역이 한국어를 전혀 포함하지 않는 문단은 구조적으로 도달 불가**다 — `_has_target_language`가 `response_contract.py:1143`의 `target_count < required`에서 먼저 탈락해 완화된 ascii 백스톱(`:1160`)이 실행되지 않는다. 실측: `**whereDate / whereMonth / whereDay / whereYear / whereTime**`는 수정 전후 모두 거부되며 이 형태가 `13.x/queries.md`에 **10건 실재**한다. 11:44 워크트리의 `_protected_ascii_letter_allowance`도 동일하게 실패한다 |
| 보완 S-02 / 주 N-16 | quote 주석 요구는 **완화 방향으로 닫혔다**(출하 코퍼스·프롬프트·최종 verifier에 맞춤). 다만 10:48 스냅샷에는 부작용이 있었다 — `response_contract.py:1195`의 `if _quote_depth(...) > 0: continue`가 quote 안 주석의 ownership 검사를 **완전히 면제**해, 인용 안에 원문과 무관한 날조 주석을 넣어도 `[]`가 나왔다. **11:44 워크트리에서는 이 구멍이 닫혔다**(다시 2건 거부). 다만 그 수정을 고정하는 테스트가 있는지는 미확인 |
| 주 N-10 | 영구 usage/model 오류 차단은 닫혔으나 완료 조건 절반 미충족 + V-03 회귀 발생 |
| F-14 | localized legacy marker가 `참고`·`注意` **두 리터럴만** 닫힘 |
| F-15(a) | multi-backtick code span의 내용 변경은 닫혔으나 **delimiter 폭 변경은 그대로** |
| F-15(c) | link title은 target 파싱만 닫힘. **title 값 보존은 그대로**이며 V-02 회귀의 원인 |
| 보완 S-10 | exact-list 단언 승격이 일부만 이뤄짐 |

### 4.2.1 과잉거부율 재측정

보완 보고서가 S-04 근거로 제시한 측정을 같은 방법(13.x + master, block signature 1:1 정렬 문서)으로 pre/post 양쪽에 적용했다.

| 빌드 | 전체 | paragraph 슬라이스 | quote 슬라이스 |
|---|---|---|---|
| 645a2d4 | **454 / 6,678 (6.80%)** | 47 / 6,271 (0.75%) | 407 / 407 |
| 수정본 (10:48) | **48 / 6,678 (0.72%)** | **47 / 6,271 (0.75%)** | 1 / 407 |
| 11:44 워크트리 | 50 / 6,678 (0.75%) | 49 / 6,271 | 1 / 407 |

key 집합 delta: **412 해소 / 42 유지 / 6 신규**.

- 해소 412건 중 **406건이 quote**다. 즉 6.80% → 0.72%의 개선은 사실상 전부 **S-02(quote 주석 요구 완화)의 몫**이다.
- 해소된 paragraph는 정확히 **6건**이고 모두 S-04 형태다(`13.x/mail.md:87`, `13.x/sail.md:40`, `master/mail.md:55`, `master/sail.md:40`, `master/search.md:290`, `master/search.md:302`).
- 신규 6건은 전부 V-06(`provider inline code mismatch`)이다.

**→ S-04가 겨냥한 paragraph 과잉거부는 6건 해소 / 6건 신규로 정확히 상쇄돼 순변화 0이다(0.75% → 0.75%).**

보완 보고서의 분모 `31,934`는 보관된 스크립트로 재현되지 않았다(같은 조건에서 prose 블록 6,678). paragraph 슬라이스 0.75%가 원 보고 0.96%와 같은 자릿수이므로 비교 가능한 슬라이스는 paragraph 쪽이다.

### 4.3 Not fixed (5건)

| 출처 · ID | 상태 |
|---|---|
| F-15(d) | 1~3칸 들여쓴 legacy quote marker — 미해결 |
| 보완 S-15 | echo 검사의 부분문자열 우회 — **그대로**. `response_contract.py:1343-1347`의 `source_body in translated_body`는 유지됐고, 추가된 것은 `and not _is_protected_source_phrase(...)`로 검사를 **더 좁히는** 방향이다. 한 글자만 바꾼 echo는 여전히 통과한다 |
| independent N-05 (P2) | multiline HTML comment 안 heading literal 변조 — 미수정 |
| 보완 S-09 계열 | `TRANSLATION_CLI_COMMAND` 형식 오류가 config 경계가 아니라 번역 단계에서 exit 1로 오분류 — 그대로 |
| independent N-06 (P3) | manifest 없을 때 workflow가 replay exit 2/3을 exit 1로 덮음 — 그대로 |
| — | `test_replay.py`에서 기존 단언이 **약화**됨: `assertEqual(list(sandboxes.iterdir()), [])` → `assertFalse(sandboxes.exists())` |

---

## 5. 신규 회귀 (V-xx)

| ID | 심각도 | 요약 | 현재 워크트리 상태 |
|---|---|---|---|
| V-06 | **P1** | 신규 `provider inline code mismatch` 계약 검사가 `repair`가 스스로 치유하던 드리프트를 앞질러 hard-fail시킨다. 고유 검출력은 0에 수렴한다 | **잔존** |
| V-01b | **P1** (재현 1건, 미확인) | locale pairing 강제가 파이프라인 산출물 자체를 거부한다 | 미확인 |
| V-01a | P2 (직접 관측) | locale pairing 강제가 수동 단일 로케일 편집을 차단한다 | 잔존 |
| V-03 | P2 | `_is_retryable` 정규식 교체로 실제 transient CLI 실패(5xx·timeout·rate limit)가 재시도 없이 1회 만에 실패한다 | 미확인 |
| V-04 | P2 | 코드 펜스 **안에 실재하는** 표 행을 upstream이 수정하면, 수정 전에는 정상 적용되던 패치가 이제 `missing existing translation block`으로 무조건 실패한다 | 미확인 |
| V-07 | P2 | 계약 실패 시 provider 응답이 기록되지 않아 이 실패 유형을 진단할 수 없다 | 잔존 |
| V-02 | P2 | `markdown._link_destination`이 link title 앞 공백을 잘라 `repair`가 `[x](t "T")`를 `[x](t"T")`로 망가뜨린다 | **해소됨** |
| V-05 | P3 | link title 위조와 인용부호 종류 변경이 수정 전에는 우연히 검출됐으나 이제 무검출로 통과한다 | 미확인 |

아래 상세는 발견 순이다(심각도 순은 위 표를 따를 것).

### V-01. 산출물 validator의 locale pairing 강제 — 두 갈래로 나눠 판정

강화된 `validate_generated_changes.py`가 KO/JA locale pairing을 요구한다. A.7 gate에서 `unpaired translation document` 10건이 나왔으나, **증거의 강도가 서로 다른 두 갈래**이므로 분리한다.

#### V-01a. 수동 단일 로케일 편집을 차단한다 — P2 (직접 관측)

내가 gate에서 실제로 본 10건의 내역은 다음과 같다.

- **9건** = 이번 수정이 **의도적으로 JA에만 추가한 alias 앵커 문서**(내가 patch로 주입한 것)
- **1건** = `version-13.x/ai-sdk.md`, mini run-1에서 **KO는 기록되고 JA가 실패한** 반쪽 적용 상태

**후자는 validator가 반쪽 적용을 정확히 잡아낸 것으로 오히려 올바른 동작이다.** 전자는 "파이프라인 산출물"이 아니라 사람이 한 보정이다. 따라서 직접 관측된 범위에서 이것은 **수동 단일 로케일 편집이 gate에서 막힌다**는 P2이지, 파이프라인 산출이 막힌다는 P1이 아니다.

다만 실무 영향은 남는다 — alias 보정처럼 한쪽 로케일만 손대는 정당한 작업이 gate를 통과하지 못하므로, 그 상태로 커밋하면 이후 모든 sync 실행이 artifact-check에서 멈춘다.

#### V-01b. 파이프라인 산출물 자체를 거부한다 — P1 (재현 1건, 미확인)

별도 검증에서 "번역 결과가 바이트 동일한 정상 sync(공백만 바뀐 upstream EN 편집)"가 같은 사유로 거부됨이 보고됐다. 이것이 사실이라면 workflow가 `make translation-artifact-check` 실패 시 커밋하지 않으므로 **정상 실행이 커밋 단계에서 차단**되는 P1이다.

**단, 이 재현은 내가 직접 확인하지 않았다.** 내 6개 run에서는 번역 성공 시 KO/JA가 항상 쌍으로 바뀌어(§3 대체 검사) 이 경로에 닿지 않았다. **P1 판정 전에 이 재현을 독립 확인해야 한다.**

**권고.** pairing을 하드 실패가 아니라 경고로 낮추거나, "번역 산출로 생긴 비대칭"과 "수동 보정으로 생긴 비대칭"을 구분한다. 최소한 이번 수정이 만든 JA-only alias 추가가 통과해야 한다.

**완료 조건.** JA에만 alias를 추가한 워크트리에서 `make translation-artifact-check`가 exit 0이고, 진짜 orphan(한쪽에만 있는 신규 문서)과 반쪽 적용은 여전히 거부되는 테스트가 존재한다.

### V-07. provider 응답이 실패 시 기록되지 않아 이 실패 유형을 진단할 수 없다 — P2

**근거.** live 실패 로그(`logs/*-run-*.log`)에는 실패 요약만 남는다. §6의 luna 실패를 판별할 때 **어느 문단이 `provider untranslated source text`를 유발했는지 끝내 복원할 수 없었다** — 계약 판정은 raw provider 응답에 대해 이뤄지는데 그 응답이 어디에도 저장되지 않는다.

**영향.** 지금 A.7을 막고 있는 것이 바로 이 실패 유형이다. CI에서 `provider untranslated source text`를 본 운영자는 **근본 원인에 도달할 경로가 없다** — 어떤 블록이, 어떤 응답으로 걸렸는지 알 수 없고 재현도 불가능하다(provider 응답은 비결정적).

**권고.** 계약 실패 시 해당 블록의 원문과 응답을 **secret이 아닌 범위에서** 진단 로그로 남긴다. 최소한 블록 인덱스와 위반한 판정의 입력 근거(예: 겹친 부분문자열 길이, target/ascii 카운트)를 출력한다.

**완료 조건.** 계약 실패 로그만 보고 어느 소스 블록이 원인인지 특정할 수 있다.

### V-02. link title 앞 공백 손실 — P2 · **현재 워크트리에서 해소됨**

**근거.** `markdown._link_destination`이 title 앞 구분 공백을 잘라내 `repair`가 `[x](t "T")`를 `[x](t"T")`로 재조립했다.

세 버전을 같은 입력으로 직접 대조했다.

| 버전 | `markdown_links('[x](t "T")')` |
|---|---|
| `645a2d4` | `target='t'`, `title=' "T"'` (공백 유지) |
| **10:48 수정본** | `target='t'`, **`title='"T"'`** ← 회귀 발생 |
| **현재 워크트리(11:44)** | `target='t'`, `title=' "T"'` ← **해소** |

**상태**: 이 회귀는 이 보고서가 검증한 10:48 스냅샷에서만 존재하며 **현재 워크트리에서는 이미 고쳐졌다.** 별도 조치가 필요 없다. 다만 이 항목을 고정하는 회귀 테스트가 있는지는 확인하지 않았다.

### V-03. retry 정규식 교체로 실제 transient 오류가 재시도되지 않는다 — P2

**근거.** N-10 수정이 substring 목록을 정규식으로 대체하면서, 키워드가 없는 5xx 응답과 `timeout` 표기의 실제 일시 오류가 재시도 대상에서 빠졌다. 영구 오류(usage/model)를 즉시 중단시키려던 의도는 달성했으나 반대 방향으로 과교정됐다.

**권고.** 영구 오류를 **거부 목록**으로 명시하고 나머지는 재시도하는 방향으로 뒤집는다.

### V-06. 신규 `provider inline code mismatch` 검사가 순손실이다 — P1

**근거.** `response_contract.py:1285-1291`의 이 검사는 `645a2d4`에 없던 신규 항목이다. 계약은 **raw provider 응답**에 대해 실행되며, `_repair_segment_translation`(`main.py:262` → `repair.repair_preserved_markup`)보다 **먼저** 돈다.

inline code 드리프트 3형태를 실측한 결과:

| 드리프트 | 신규 계약 | repair 결과 | 최종 `verify.verify` |
|---|---|---|---|
| 스팬 **내용**이 번역됨 (`` `prompt` `` → `` `プロンプト` ``) | **거부** | `` `prompt` `` 복원 | `[]` |
| 스팬 **백틱이 벗겨짐** (`` `summarize` `` → `summarize`) | **거부** | `` `summarize` `` 복원 | `[]` |
| 스팬이 **추가**됨 (`Gemini` → `` `Gemini` ``) | **거부** | RepairError | `['inline code mismatch']` |

**3형태 중 2형태는 파이프라인이 스스로 치유하던 것**이다. 게다가 `main.py:50`의 `SEGMENT_RETRYABLE_VERIFICATION_ISSUES`에 이미 `"inline code mismatch"`가 재시도 대상으로 등재돼 있어, 설계 의도 자체가 "치유·재시도 가능"이다. 그러나 **계약 단계의 이슈는 이 집합을 타지 못하고** 2회 시도 후 `IncompleteTranslation`으로 run 전체가 중단된다.

**고유 검출력이 0에 수렴한다는 근거 세 가지:**

1. 이 검사를 끄는 mutation은 `test_rejects_changed_inline_code_only_identifier_list` 1건만 실패시키는데, 그 입력은 검사를 꺼도 여전히 `provider protected term mismatch`로 거부된다. 실패 사유는 exact-list 단언이라 리스트 내용이 달라졌기 때문일 뿐이다.
2. 13.x+master 출하 코퍼스에서 이 검사만으로 새로 거부된 6건(`container.md:712/721`, `master/container.md:708/717`, `master/mail.md:343/440`)은 **전부 최종 `verify.verify`도 잡는다.** 6건 중 repair로 치유되는 것은 1건뿐이라 실제 문서 손상은 이미 최종 게이트가 막고 있었다.
3. §6의 mini run-1 실패(`provider inline code mismatch` 단독)가 이 검사의 실제 비용이다. 구조·markup·주석이 전부 일치하는 ja 응답이 inline code 멀티셋만으로 차단됐다.

**영향.** 순수 손실이다 — 새로 잡는 것은 없고, 치유 가능한 응답을 차단하며, live 실패를 만든다. **11:44 워크트리에도 그대로 남아 있어 다음 실행에서 재발한다.**

**권고.** 이 검사를 제거하거나, 계약이 아니라 **repair 이후** 단계로 옮긴다.

**완료 조건.** 위 3형태 중 repair가 치유하는 2형태가 계약을 통과하고, 치유 불가능한 형태만 거부되며, 그 구분을 고정하는 테스트가 존재한다.

### V-04. 코드 펜스 안 실재 표 행 수정이 무조건 실패한다 — P2

**근거.** N-17 수정이 `_table_regions`에서 fence 내부를 제외했다. 그 결과 upstream이 **펜스 안에 실제로 존재하는 표 행**을 수정하면 대상 후보가 0이 되어 `missing existing translation block`으로 실패한다. 수정 전에는 정상 적용되던 경로다.

**권고.** 펜스 내부를 후보에서 제외하는 대신, 펜스 내부/외부를 구분해 **원문에서의 위치와 같은 쪽**을 고르도록 한다.

---

## 6. live 결과 (§2.9)

고정 표본 `VERSION=13.x`, `DOC=ai-sdk.md`. fixture는 **production-representative**(로케일 파일을 `645a2d4` 상태로 두고 delta를 upstream만으로 공급)를 썼다. 이는 이전 라운드에서 A.5-literal fixture의 KO/JA rollback이 `> [!NOTE]` 정규화를 되돌린다는 사실을 확인한 뒤 채택한 것이다.

| 모델 | run 1 | run 2 | run 3 | 결과 |
|---|---|---|---|---|
| `gpt-5.4-mini` | FAIL | PASS | PASS | **2/3** |
| `gpt-5.6-luna` | FAIL | PASS | FAIL | **1/3** |

실패 사유:

| run | 실패 locale | contract issue |
|---|---|---|
| mini run-1 | ja | `provider inline code mismatch` |
| luna run-1 | ko | `provider untranslated source text`, `provider target language mismatch` |
| luna run-3 | ko | `provider untranslated source text`, `provider target language mismatch` |

**이전 라운드와의 결정적 차이**: 645a2d4에서는 6/6이 **문자 단위로 동일한 오류**로 막혀 어떤 재시도로도 통과할 수 없었다. 수정본에서는 **같은 코드·같은 입력으로 성공과 실패가 갈린다**(mini run-1 실패 → run-2·3 성공). 즉 결정론적 차단이 간헐적 거부로 바뀌었다.

### 실패 3건의 판별 결과

**luna ko × 2회 → (b) provider의 실제 계약 위반.** 과잉거부가 아니다. 판별 근거:

1. provider에게 실제로 간 블록을 재현했다 — `diff.hunks_between` → 11 hunks → `build_plan` → 13 changes, provider 호출 대상 **10 블록**.
2. 그 10블록의 모든 text 서브블록이 영어 10~53단어의 **진짜 산문**이며 `_is_protected_source_phrase`·`_is_bare_protected_term_list` 모두 False다. **"원문 그대로가 정답"인 블록은 하나도 없다.** 순수 식별자 블록과 TOC 목록은 identity 입력에도 계약이 `[]`를 반환하므로 원인이 아니다.
3. **결정적 교차검증**: 성공한 run-2의 ko·ja 산출물을 새 EN과 블록 정렬해 계약을 돌린 결과 **변경 대상 30개 prose 블록이 ko·ja 양쪽 모두 0건 거부**였다. 거부된 3건은 변경 집합 밖의 레거시 `> **Warning:**` 형식(기존 문서 드리프트).
4. `provider untranslated source text`는 정규화된 원문 문단 **전체가 번역문에 통째로 부분문자열로 존재**해야 발동하고, `target language mismatch`가 동반된 것은 같은 문단에 한국어가 없었다는 뜻이다. 27~53단어 산문에서 정상 번역이 이를 만족할 방법은 없다.

provider 응답이 로그에 남지 않아 특정 문단은 복원 불가다. 판정은 **블록 단위로 (b)**다.

**mini ja × 1회 → 이번 수정이 도입한 회귀(V-06).** 상세는 §5 참조. 같은 run이 ko는 성공적으로 기록한 뒤 ja에서만, 그것도 `provider inline code mismatch` **단독**으로 실패했다 — 구조·markup·주석은 전부 일치했다는 뜻이다.

---

## 7. 알려진 미해결 항목의 상태 변화

| 항목 | 645a2d4 | 수정본 |
|---|---|---|
| F-14 | 그대로 | **부분 해결** (`참고`·`注意` 두 리터럴만) |
| F-15 | 그대로 | **부분 해결** — (b) multiline span·inline `<img>` 닫힘, (a) delimiter 폭·(c) title 값·(d) 들여쓴 marker는 그대로 |
| F-18 | 그대로 | **해결** (`generator.py`) |
| F-09 | 그대로 | **부분 해결** — config 검증이 upstream 앞으로 이동(주 N-09)해 설정 오류 시 EN 캐시 오염이 사라졌다. 전체 transaction 경계는 여전히 없음 |
| F-07 | 확인됨 | **유지** — CLI env allowlist·hook 차단에 약화 없음 |
| F-11 | 검증 불가 | 검증 불가 (Azure key 없음) |
| F-12 | 그대로 | 그대로 |
| F-17 | 그대로 | 그대로 |

---

## 8. no-op 재실행 (A.6)

### 1차 시도는 무효

파이프라인의 no-op 6회가 전부 `exit=2`로 실패했으나, 로그를 보면 사유가 다음이었다.

```
can't open file '.../credential_runner.py': [Errno 2] No such file or directory
```

병행하던 검증 에이전트들이 같은 `.review` 디렉터리에서 실험하며 이 파일을 일시적으로 제거한 것이 원인이다. **파이프라인과 무관한 하네스 사고이므로 이 결과는 무효**이며, 성공한 3개 checkout에 대해 재실행했다.

### 재실행 결과 — A.6 조건 미충족, 다만 원인은 절차에 있다

| checkout | exit | `no source changes` | 재번역 | diff 해시 |
|---|---|---|---|---|
| mini run-2 | 1 | 아니오 | 시도 중 contract 실패 | 동일 |
| mini run-3 | 0 | 아니오 | **`translated 1 doc(s) into ko, ja`** | 동일 |
| luna run-2 | 0 | 아니오 | **`translated 1 doc(s) into ko, ja`** | 동일 |

A.6이 요구하는 두 조건(`no source changes to translate` 출력, provider 재호출 없음)은 **셋 다 미충족**이다.

**그러나 이는 파이프라인 결함이 아니라 지시서 절차의 구조적 한계다.** `diff.changed_sources()`는 `git status --porcelain -- i18n/en`으로 변경을 감지한다. §0.2가 어떤 저장소에서도 commit을 금지하므로 첫 실행이 만든 EN 캐시 갱신이 커밋되지 않고 워크트리에 남는다. 따라서 두 번째 실행도 **같은 delta를 그대로 다시 본다**. 실제 운영에서는 workflow가 첫 실행 결과를 커밋하므로 다음 실행에서는 이 delta가 사라진다.

의미 있는 것은 **결과의 동일성**이다. 재번역했음에도 세 checkout 모두 diff 해시가 변하지 않았다 — 같은 입력에 대해 **구조적 멱등성은 성립**한다. mini run-2의 exit 1은 §6에서 관측한 간헐적 contract 거부가 재실행에서도 나타난 사례다.

**권고**: 지시서 A.6은 "commit 금지"와 "`no source changes` 도달"을 동시에 요구하므로 원리적으로 충족 불가능하다. 재실행 조건을 "결과 diff가 변하지 않는다"로 바꾸거나, sandbox clone 안에서만 commit을 허용해야 한다.

---

## 9. 검증 한계

- **patch 전송 방식의 부작용**: 수정본을 미커밋 상태로 검증하기 위해 patch로 주입했으므로 `make translation-artifact-check`를 직접 판정할 수 없다. 대체 검사(번역 산출 경로만 추출)로 확인했다. 이 수정을 **커밋한 뒤 gate를 다시 돌리는 것**이 최종 확인으로 필요하다.
- **live 표본 한계**: 문서 1건 × 모델별 3회. 간헐적 실패의 **빈도**를 이 표본으로 추정할 수 없다. 3/6이라는 수치는 "간헐성이 존재한다"는 사실만 뒷받침한다.
- **replay 미실행**: 지시서의 commit 금지 규정에 따라 이번에도 실행하지 않았다. 선행 보고서의 679문서 identity replay는 세 라운드 연속 재확립되지 않았다.
- **provider contract gate 미재실행**: 이번 라운드에서 §2.8을 다시 돌리지 않았다. 이전 라운드에서 두 실행의 결과가 갈린 바 있어(한쪽은 두 모델 통과, 다른 쪽은 luna JA 실패) 이 gate의 재현성 자체가 의심스럽다.
- **검증 대상이 이동 중**: `Makefile`의 `--frozen` → `--locked` 변경 등 patch 추출 이후의 수정은 포함되지 않았다.
- **Azure 경로 미검증**, **secret 비열람**.
- 활성 브랜치에 commit·push **0건**.

---

## 10. 최종 판정과 다음 작업

**수정은 실질적인 개선이다.** 세 리뷰가 지목한 blocker 중 가장 무거운 것(admonition marker flip으로 인한 결정론적 sync 차단)이 코퍼스 규모로 확인 가능하게 닫혔고, 그 밖에도 15건이 실측으로 닫혔다. `apply_plan`의 전역 앵커 불변식도 유지된다.

**그러나 지금 상태로 무인 운영을 켜면 안 된다.**

권장 처리 순서:

1. **V-06 (P1)** — `provider inline code mismatch` 검사를 제거하거나 repair 이후로 옮긴다. 순수 손실이며 live 실패를 직접 만든다. **가장 저렴하고 효과가 확실한 조치**다.
2. **V-01b 재현 확인 → 필요 시 P1 처리** — "바이트 동일한 정상 sync가 거부된다"는 재현을 독립 확인한다. 사실이면 최우선이 된다. 확인 전까지는 V-01a(P2)로 다룬다.
3. **V-04** — 표 fence 제외 과교정. "수정 전에는 되던 것이 안 되는" 회귀다.
4. **V-03** — retry 분류를 거부 목록 방식으로 뒤집기.
5. **V-07 (P2)** — 계약 실패 시 진단 정보 기록. 지금 A.7을 막는 실패 유형이 진단 불가 상태다.
5. **S-04 잔여** — `_has_target_language`의 `target_count < required` 게이트가 완화된 ascii 백스톱보다 앞서 탈락시키는 구조를 고친다. `13.x/queries.md`에만 10건이 실재하므로 실제 sync를 막는다.
6. **테스트 판별력 보강** — `_table_row_matches_context`(주 N-02), `_table_regions` fence 제외(주 N-17), V-06 검사는 현재 어떤 테스트도 실질적으로 고정하지 않는다. `test_replay.py`의 약화된 단언(`assertEqual(list(sandboxes.iterdir()), [])` → `assertFalse(sandboxes.exists())`)도 복원할 것.
7. **11:44 이후 변경 재검증** — 이 보고서 범위 밖의 `response_contract.py`/`verify.py` 수정(link 4종 신규 거부 포함)은 검증되지 않았다. 신규 거부 항목은 V-06과 같은 유형의 과교정 위험이 있으므로 같은 방법으로 확인해야 한다.
8. 나머지 partial·not_fixed 항목.

**luna의 간헐 실패는 코드 결함이 아니다.** 판별 결과 provider가 실제로 계약을 위반한 것이므로, 완화가 아니라 **프롬프트 개선 또는 재시도 정책**으로 다뤄야 한다. 현재 `MAX_SEGMENT_VERIFICATION_ATTEMPTS = 2`와 `--fail-fast` 조합에서는 한 블록의 실패가 run 전체를 중단시킨다.

**커밋 분할 제안**: 이번 로컬 수정도 파이프라인 코드 / 테스트 / JA 산출물 / 인프라 설정(`.gitignore`·`.dockerignore`·workflow)의 네 경계로 나눌 수 있다.
