# Translation Sync 리팩토링 독립 검증 보고서

검증일: 2026-07-26 KST  
대상: `refactor/sync-docs`의 `645a2d4` (`refact: temp`)  
기준: `main`의 `3aab108`

## 1. 결론

**merge 불가.** 신규 P1인 N-01·N-02가 실제 입력에서 잘못된 블록 순서를 만들고도 최종 verifier를 통과했다. 기존 P1 F-14·F-15도 재현됐다. 또한 strict credential runner가 제공된 `dot_env`를 거부해 두 모델의 live 3회 검증을 시작하지 못했으므로 부록 A.7 완료 조건을 충족하지 못했다.

Blocker:

1. N-01: 중복 annotation 뒤 구조 블록 삽입 위치 오류
2. N-02: fenced code 삽입과 후행 admonition/table 순서 오류
3. F-14: localized legacy admonition marker 우회
4. F-15: multi-backtick/multiline code span과 link title 보존 우회
5. A.7 미완료: `gpt-5.4-mini` 0/3, `gpt-5.6-luna` 0/3

## 2. 검증 스냅샷

- 대상 SHA: `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a`
- `main..HEAD`: 1 commit
- 변경 규모: 74 files, +13,232 / -1,288
- 검증 checkout: 프로젝트 내부 `.review/translation-sync-validation-20260726-031218/base`
- Python: 3.14.6
- uv: 0.11.31
- Node: 26.5.0 (`.nvmrc`와 일치)
- npm: 11.17.0
- act: 0.2.89
- Docker: 29.1.3
- Docker Compose: v5.0.1
- credential: 일반 파일, 현재 사용자 소유, symlink 아님, mode `0600`; 값은 읽거나 기록하지 않았다.

실행하지 않은 gate:

- `make translation-replay` / `make translation-check`: 내부 commit 금지 규칙에 따라 미실행
- live provider/document gate: strict runner가 `unquoted whitespace at line 3`으로 credential 입력을 거부해 중단
- 원격 write, commit, merge, rebase, tag, push, workflow 실실행: 0회

## 3. Gate 결과표

| # | Gate | 실제 결과 | 판정 |
|---|---|---|---|
| 2.1 | `make translation-test` | 419 tests, OK, 5.779s | 통과 |
| 2.2 | replay 계약 | replay 단위 테스트 포함 419 tests 통과; `replay.py` 격리·active fingerprint·2-process no-op 코드 검토 완료; 실제 replay 미실행 | 제한적 확인 |
| 2.3 | `act --dryrun` | workflow job/step 해석을 시작했으나 `setup-uv` action clone에서 HTTP/2 `stream error: CANCEL`로 종료 | 미확인 |
| 2.4 | `make translation-artifact-check` | `translation sync output paths verified: 0 file(s)` | 통과 |
| 2.5 | `make site-test` | Node test 1/1 통과 | 통과 |
| 2.6 | `make site-check` | typecheck/build 통과; anchor 46,626/46,626, missing 0 | 통과 |
| 2.7 | `git diff --check HEAD^...HEAD` | 출력 없음, exit 0 | 통과 |
| A.4 | translation Docker unit gate | 419 tests, OK, 1.601s | 통과 |
| A.4 | site Docker gate | test/typecheck/build/anchor 통과; 46,626/46,626 | 통과 |
| 2.8 | `gpt-5.4-mini` provider check | strict runner가 credential 형식을 거부, provider 미호출 | 미실행 |
| 2.8 | `gpt-5.6-luna` provider check | 같은 선행 blocker로 provider 미호출 | 미실행 |
| 2.9 | `gpt-5.4-mini` live 문서 | 0/3 | 실패/미완료 |
| 2.9 | `gpt-5.6-luna` live 문서 | 0/3 | 실패/미완료 |
| 2.10 | 6개 live checkout artifact/site/diff/no-op | live checkout 미생성 | 미실행 |
| 2.11 | F-01 import seam/docs 번호 | import object 단일성 확인, 419 tests collection 성공, docs 00~08 정리 확인 | 종료 확인 |

`act`의 첫 실행은 기본 이미지 선택 대화에서 EOF로 끝났다. Medium 이미지를 명시한 재실행은 workflow 구조를 전개했지만 외부 action clone 실패로 전체 dry-run을 완료하지 못했다. 실행하지 않은 workflow를 통과로 기록하지 않는다.

## 4. Track A 결과

| 항목 | 판정 | 근거 |
|---|---|---|
| F-01 | 확인됨 | `sync/__init__.py:16-30`이 `response_contract`를 재export하고 flat/nested import가 같은 module object임을 확인했다. `provider_check.py` collection을 포함한 419 tests가 통과했다. docs는 `00`~`08`이고 `07-error-cases.md`는 없다. |
| F-02 | 확인됨(지원 구조 범위) | `main.py:154-210,217-265`의 pre-write response contract와 `response_contract.py:1195-1312`. missing body, exact/near English echo, duplicate occurrence omission, extra prose, changed structure negative test가 독립적으로 존재한다. |
| F-03 | 부분적 | `provider_check.py:115-125`가 response/final verifier를 모두 호출한다. 다만 final verifier 호출만 독립적으로 깨뜨리는 회귀 테스트는 없다. |
| F-04 | 부분적 | wrong-version inline link tests는 존재한다. 그러나 reference-style definition의 13.x→12.x drift가 annotation을 갖춘 출력에서 `verify(...) == []`로 재현됐다. |
| F-05 | 확인됨 | named-section permutation은 source/target state와 signature로 보호되며 ambiguity는 전용 reorder 경로에 들어가지 않는다. 관련 `test_patch.py:845-983` 존재. |
| F-06 | 부분적 | 숫자 옵션 검증과 `ConfigError`→exit 2가 구현됐다. source change가 없으면 config load 전에 0으로 반환하는 경계가 남지만 provider는 호출되지 않는다. |
| F-07 | 부분적 | CLI cwd/env/flags/`.env` 차단은 테스트된다. `TRANSLATION_CLI_COMMAND`와 `PATH`는 trusted deployment input이라는 전제가 명시적으로 강제되지 않는다. |
| F-08 | 부분적 | prompt 충돌은 정리됐고 구조 누락은 강하게 검사한다. 의미 단위 누락은 자동 검출 범위 밖이다. 실제로 `Install the package, then run the migration.`에서 migration 절을 제거해도 response/final verifier가 모두 `[]`였다. |
| F-10 | 확인됨 | Node 26 host·Docker build와 anchor 46,626/46,626을 현재 SHA에서 재확립했다. |
| F-13 | 부분적 | 기존 경계 회귀 테스트는 존재한다. 그러나 multiline HTML comment 안 heading attribute가 `# Literal {.page-title #literal}`→`# Literal {#literal}`로 바뀌는 입력을 재현했다. |
| F-16 | 확인됨 | sidebar filename/version은 `versions.json`에서 파생되고 future 14.x test가 존재한다. 순서·중복 문제는 별도 F-18로 남는다. |

## 5. 신규 Finding 요약

| ID | 심각도 | 요약 | 상태 |
|---|---:|---|---|
| N-01 | P1 | 중복 annotation 뒤 EOF 구조 삽입이 첫 occurrence 뒤에 잘못 배치되고 verifier를 통과 | 재현됨 |
| N-02 | P1 | 후행 admonition/table 뒤 fenced code 삽입이 구조 블록 앞으로 이동하고 verifier를 통과 | 재현됨 |
| N-03 | P2 | 번역된 두 table 중 첫 행 변경이 provider 전에 `PatchError`로 차단 | 재현됨 |
| N-04 | P2 | reference-style link definition의 version drift가 final verifier를 우회 | 재현됨 |
| N-05 | P2 | multiline HTML comment 안 heading literal을 preprocessing이 변경 | 재현됨 |
| N-06 | P3 | manifest가 없을 때 workflow가 replay exit 2/3을 exit 1로 덮음 | 코드 경로 확인 |

## 6. 상세 Finding

### N-01. 중복 annotation 뒤 구조 블록 삽입이 잘못된 occurrence를 선택한다 — P1

#### 근거

`sync/translation/patch.py:1658-1667`의 structural path는 일반 source block 위치 정보를 만들지 않는다. `:1466-1470`은 anchor 없는 non-code insert를 거부한 뒤, `:1362-1369`에서 occurrence 없이 `_find_block`을 호출한다. `_find_block`은 `:987-1001`에서 첫 exact match를 선택한다.

실제 재현 결과:

```markdown
<!-- Repeat. -->
첫 번째 반복입니다.

> [!NOTE]
> 새 경고입니다.

<!-- Repeat. -->
두 번째 반복입니다.
```

source의 새 admonition은 두 번째 `Repeat.` 뒤 EOF에 있어야 하지만 첫 occurrence 뒤에 들어갔다. `verify.verify(result, source=new)`는 `[]`였다.

#### 재현 조건

```python
old = "Repeat.\n\nRepeat.\n"
new = old + "\n> [!NOTE]\n> New warning.\n"
existing = (
    "<!-- Repeat. -->\n첫 번째 반복입니다.\n\n"
    "<!-- Repeat. -->\n두 번째 반복입니다.\n"
)
plan = patch.build_plan(hunks_between(old, new), new)
result = patch.apply_plan(existing, plan, ["> [!NOTE]\n> 새 경고입니다.\n"])
assert verify.verify(result, source=new) == []
```

#### 영향

경고, table, navigation fragment가 다른 문단/section에 들어가도 자동 commit gate를 통과할 수 있다.

#### 권고

structural insertion에도 source predecessor/successor occurrence를 보존한다. occurrence가 유일하지 않으면 첫 match를 선택하지 말고 `PatchError`로 fail-closed한다.

#### 완료 조건

두 개의 동일 `Repeat.` 뒤 EOF admonition/table 삽입이 두 번째 occurrence 뒤에 배치되는 회귀 테스트와, ambiguity에서 실패하는 negative test가 통과한다.

### N-02. fenced code 삽입이 후행 구조 블록과의 상대 순서를 잃는다 — P1

#### 근거

`patch.py:1228-1250`의 `_insert_fenced_code_block`은 전체 문서 경계가 아니라 fenced block ordinal만 사용한다. code와 non-annotatable structural line은 source block discovery에서 제외된다(`:2982-3041`). Final verifier는 code block 순서와 admonition 형식은 비교하지만 두 종류 사이 상대 순서를 비교하지 않는다.

실제 결과는 source의 `old code → warning → inserted code`가 `old code → inserted code → warning`으로 바뀌었고 `verify.verify(result, source=new) == []`였다.

#### 재현 조건

```python
old = "```php\nold();\n```\n\n> [!NOTE]\n> Keep this warning.\n"
new = old + "\n```php\ninserted();\n```\n"
existing = "```php\nold();\n```\n\n> [!NOTE]\n> 이 경고를 유지합니다.\n"
plan = patch.build_plan(hunks_between(old, new), new)
result = patch.apply_plan(existing, plan, ["```php\ninserted();\n```\n"])
assert verify.verify(result, source=new) == []
```

#### 영향

경고나 table이 설명하는 코드 예제의 위치가 바뀌어 의미 관계가 손상되지만 파일 기록과 자동 commit이 가능하다.

#### 권고

code insertion을 전체 source-relative boundary에 결합한다. boundary가 없거나 모호하면 ordinal fallback 대신 실패한다.

#### 완료 조건

admonition/table 앞뒤 code prepend/append 회귀 테스트가 source-relative 순서를 검증하고, 모호한 경계는 기록 전에 실패한다.

### N-03. 번역된 table 행 변경이 다음 table 때문에 차단된다 — P2

#### 근거

`patch.py:2656-2681`은 locale row의 첫 cell 이후가 old English cell과 같아야 한다. 번역된 설명은 일치하지 않는다. 두 번째 narrowing도 raw English context를 검색한다(`:2686-2702`).

#### 재현 조건

두 개의 table을 둔 source에서 첫 table의 `Old explanation`만 `New explanation`으로 바꾸고, locale에는 `이전 설명`과 `기존 설명`을 둔다. `patch.existing_context(...)`가 실제로 다음으로 실패했다.

```text
PatchError missing existing translation block for: | `foo` | Old explanation |
```

#### 영향

정상적인 번역 table cell 업데이트가 provider 호출 전 중단된다. 잘못된 write는 없지만 정상 upstream 변경을 막는다.

#### 권고

번역값 equality 대신 source table ordinal·row key·structural boundary로 locale row를 찾고 ambiguity에서만 실패한다.

#### 완료 조건

두 translated table fixture에서 첫 locale row만 교체되고, duplicate ambiguous table fixture는 fail-closed한다.

### N-04. reference-style link version drift가 검증되지 않는다 — P2

#### 근거

`verify.py:156-212`의 version-aware normalization은 inline link에 적용되지만 shared `markdown_links()`는 reference definition을 읽지 않는다. 다음 출력은 definition을 13.x에서 12.x로 변경했지만 `verify(...) == []`였다.

#### 재현 조건

```markdown
<!-- See [Cache][cache-doc]. -->
See [Cache][cache-doc].

<!-- [cache-doc]: /docs/13.x/cache -->
[cache-doc]: /docs/12.x/cache
```

#### 영향

reference-style link를 사용하는 문서에서 과거/미래 버전으로 잘못 연결될 수 있다.

#### 권고

reference definition을 parse해 version-sensitive target 비교에 포함하거나 지원하지 않는 syntax를 명시적으로 거부한다.

#### 완료 조건

13.x→12.x definition 변경이 `link target mismatch`로 실패한다.

### N-05. multiline HTML comment 안 heading literal이 변경된다 — P2

#### 근거

`preprocess.py:281-315`에서 heading attribute 정규화가 HTML comment context를 알지 못한다. 실제 입력:

```markdown
<!--
# Literal {.page-title #literal}
-->
```

출력:

```markdown
<!--
# Literal {#literal}
-->
```

#### 영향

source-authored multiline comment payload가 provider 호출 전에 바뀌며, 이후 verifier도 변경된 expected source를 기준으로 삼아 손상을 놓칠 수 있다.

#### 권고

heading attribute 정규화 전에 HTML comment span을 mask하거나 comment-aware line mapper를 공유한다.

#### 완료 조건

multiline comment 내부 heading literal은 byte-identical하고 visible heading의 기존 정규화 테스트는 유지된다.

### N-06. workflow가 replay의 구체적 exit code를 잃는다 — P3

#### 근거

`.github/workflows/sync-translation.yml:71-80`은 `make translation-check` status를 저장하지만 manifest가 없으면 무조건 `exit 1`한다. `replay.py`가 정의한 setup/replay error 2와 active-worktree mutation 3이 manifest 생성 전 실패에서 1로 바뀐다.

#### 재현 조건

sandbox clone 실패처럼 manifest 생성 전 `run_replay()`가 2를 반환하게 한다. workflow shell은 missing-manifest branch에서 1을 반환한다.

#### 영향

commit은 안전하게 차단되지만 CI 진단 분류가 손실된다.

#### 권고

manifest가 없고 `status != 0`이면 원래 status를 반환하고, `status == 0`인데 manifest만 없을 때 1을 반환한다.

#### 완료 조건

status 2/3 보존과 status 0 + missing manifest→1을 검증하는 shell regression이 존재한다.

## 7. 알려진 미해결 항목의 상태 변화

| 항목 | 판정 | 근거 |
|---|---|---|
| F-09 | 그대로 | target별 즉시 write/delete 후 batch rollback이 없다. workflow는 실패 시 commit하지 않지만 local partial output은 남는다. |
| F-14 | 그대로(P1) | `> **참고:**`, `> **注:**`가 postprocess에서 유지되고 `verify()`가 `[]`를 반환하는 것을 재현했다. |
| F-15 | 그대로(P1) | multi-backtick 내용 변경, multiline span 변경, link title 삭제/변경이 verifier를 우회했다. |
| F-18 | 그대로(P2) | misordered/duplicate `versions.json`을 `load_versions`가 수용하는 것을 재현했다. |
| F-11 | 검증 불가 | 현재 credential은 OpenAI 변수만 제공하며 Azure deployment/API version 실환경은 검증하지 않았다. |
| F-12 | 부분 해결(P3) | sync workflow는 full SHA pin이지만 deploy workflow는 mutable major tag다. |
| F-17 | 외부 결정 필요 | schedule/direct push는 코드에서 확인했으나 ruleset bypass와 schedule 지연은 저장소 밖 조건이다. |

F-14와 F-15는 무인 운영 merge blocker다. 둘 다 provider 결과나 source 구조 손상을 자동 commit 전에 놓칠 수 있다.

## 8. Live 표본 결과

| 모델 | Provider contract | Run 1 | Run 2 | Run 3 | no-op | 판정 |
|---|---|---|---|---|---|---|
| `gpt-5.4-mini` | 미실행 | - | - | - | - | 0/3 |
| `gpt-5.6-luna` | 미실행 | - | - | - | - | 0/3 |

- 고정 표본 예정: `version-13.x/ai-sdk.md`
- prompt hash: live runner가 시작되지 않아 기록하지 않음
- 변경 경로/KO·JA 사람 검토: live output 없음
- secret은 출력·기록하지 않았다.
- Strict runner 실패: `unquoted whitespace at line 3`. 값은 조사하지 않았다.

## 9. 검증 한계

- identity replay는 patch/구조/멱등성 검증이며 번역 의미 정확성 검증이 아니다.
- 두 모델 live 검증은 credential runner 선행 실패로 수행하지 못했다. 전체 문서군이나 장기간 provider 안정성을 판정하지 않는다.
- `dot_env`의 값은 읽지 않았고, 실제 provider 유효성도 확인하지 못했다.
- Azure deployment/API version 경로는 현재 credential 범위 밖이다.
- `act --dryrun`은 외부 action clone 오류로 끝까지 완료하지 못했다.
- 자동 verifier는 번역 의미 동등성을 증명하지 않는다. 별도 사람 검토가 필요하다.

## 10. 최종 판정과 다음 작업

**최종 판정: merge 불가, 검증 미완료.**

최소 수정 순서:

1. N-01·N-02의 source-relative insertion boundary를 fail-closed하게 수정하고 회귀 테스트 추가
2. F-14를 provider 이전 canonicalization과 source-derived admonition contract로 차단
3. F-15를 shared delimiter-aware code-span/link parser로 수정
4. N-03·N-04·N-05·F-18 회귀 테스트와 최소 구현 수정
5. N-06의 workflow status 보존 수정
6. Strict runner와 제공된 dotenv 형식 계약을 secret 비노출 상태로 일치시킨 뒤 두 모델 provider check와 모델별 3회 live run 재수행
7. 6개 run 모두 artifact/site/diff/no-op를 통과한 뒤에만 merge 가능 재판정

커밋 분할 제안: 파이프라인 코드·테스트 / 운영 문서·prompt / 생성 번역 산출물 / CI·Docker 설정을 분리할 수 있다. 분할 자체는 finding이 아니다.
