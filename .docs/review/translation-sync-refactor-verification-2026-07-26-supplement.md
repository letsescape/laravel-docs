# Translation Sync 리팩토링 검증 — 보완 보고서 (645a2d4)

검증 실행: 2026-07-26 KST
대상 스냅샷: `refactor/sync-docs`의 `645a2d4a374c5d7eb8a1a1d4d8678e7effce4b0a` (`refact: temp`)
검증 지시서: 프로젝트 루트 `prompt.md`
workspace: `.review/translation-sync-validation-20260726-010825/`

## 이 문서의 위치

같은 커밋에 대해 **두 개의 독립 검증이 병행**됐다.

| | 주 보고서 | 이 보완 보고서 |
|---|---|---|
| 파일 | `translation-sync-refactor-verification-2026-07-26.md` | 이 문서 |
| workspace | `.review/translation-sync-validation-20260726-010820/` | `...-010825/` |
| 강점 | live 경로 실증 | **live 독립 재현 + 정적 정면 리뷰 깊이**(mutation 기반 적대적 재검증, 코퍼스 전수 실측) |
| finding ID | `N-xx` | `S-xx` (충돌 방지) |

주 보고서는 수정하지 않았다. 이 문서는 주 보고서를 대체하지 않으며, **주 보고서에 없는 결함**과 **판정이 갈리는 항목**을 담고, A.7 완료 판정을 독립적으로 내린다. 두 문서에서 같은 결론에 도달한 항목은 §4에 대조표로만 정리한다.

live 단계(A.4~A.7)는 **이 실행에서도 전 구간을 직접 수행했다**. 결과는 §1-A에 있으며, 주 보고서의 live 판정을 다른 workspace·다른 미러·다른 checkout에서 독립 재현한다. 다만 §2.8 provider contract만은 두 실행의 결과가 갈렸다(§1-A 참조).

---

## 1. 이 실행이 재확립한 gate

| # | gate | 결과 | 실행 경로 |
|---|---|---|---|
| 2.1 | Python 단위 테스트 | **Ran 419 tests, OK** (1.573s) | Docker `laravel-docs-translation-validation:645a2d4` |
| 2.4 | 산출 경로 검사기 | `output paths verified: 0 file(s)`, exit 0 (**smoke only**) | base checkout + `python3` 직접 실행 |
| 2.5 | Markdown 링크 유틸 | `fail 0` | 호스트 Node v26.5.0 |
| 2.6 | typecheck + build + anchor | typecheck 무오류, KO/JA build `Compiled successfully`, **46,626 / 46,626 OK, id not found 0** | 호스트 Node v26.5.0 |
| 2.7 | 공백/충돌 마커 | 출력 없음 | `git diff --check HEAD^...HEAD` |
| 2.8 | provider contract (2모델) | **두 모델 모두 PASS** — `gpt-5.4-mini`·`gpt-5.6-luna` 각각 exit 0, KO/JA 모두 검사 | strict runner + Docker |
| 2.9 | 실제 문서 end-to-end | **0/3, 0/3 — 6회 전부 동일 실패** | 아래 §1-A |
| 2.10 | live 후속 gate | artifact=0 / diff-check=0 / site=0 (6/6) — **단, 번역 미적용 상태의 통과** | 아래 §1-A |
| A.6 | no-op 재실행 | **0/6** — 수렴 마커에 도달하지 못하고 같은 오류 반복 | 아래 §1-A |
| 2.11 | F-01 종료 여부 | **닫힘** | import seam 실증 + 문서 번호 감사 |

환경 편차(주 보고서와 별개로 이 실행에서 발생한 것):

- 로컬 `make translation-test`는 uv 패키지 다운로드가 네트워크 타임아웃으로 실패해, 부록 A.4가 규정한 Docker 이미지 실행으로 수행했다.
- `make translation-artifact-check`는 `uv run`을 거치지만 `validate_generated_changes.py`가 표준 라이브러리만 import하므로 base checkout에서 `python3` 직접 실행으로 동등 수행했다.
- site Docker 이미지는 `npm ci`가 `ECONNRESET`으로 두 번 실패했다. 동일 `package-lock.json`(SHA-256 일치 확인)의 기존 `node_modules`를 사용해 호스트 Node로 4단계를 수행했다.
- 부록 A.2의 awk 스크립트는 변수명 `index`가 awk 내장 함수와 충돌해 그대로 실행되지 않는다. 변수명만 `i`로 바꾼 동등 검사로 통과시켰다.

**2.6의 통과가 곧 S-01의 근거다.** 아래를 보라.

### §1-A. live 단계 독립 재현 (A.4 ~ A.7)

이 실행은 처음에 live 범위가 병행 실행에서 소진됐다고 보고 생략했으나, **A.7 완료 판정까지 직접 수행하라는 지시에 따라 전 구간을 독립 실행했다.** 결과는 주 보고서의 live 판정을 독립적으로 확인한다.

#### A.4 provider contract — 두 모델 모두 통과

| 모델 | locale | 결과 |
|---|---|---|
| `gpt-5.4-mini` | ko / ja | exit 0, 구조·주석·코드 블록 정상 |
| `gpt-5.6-luna` | ko / ja | exit 0, 구조·주석·코드 블록 정상 |

provider `openai`, reasoning `medium`. prompt SHA-256은 KO `8bf437f9ff84…`, JA `104d626b647a…`로 두 모델이 동일한 프롬프트를 받았다. wrapper·설명·외곽 code fence·영어 echo·구조 손상은 없었다.

**이 결과는 주 보고서 §3의 "2.8 … luna KO 통과·JA 실패, 판정 실패"와 어긋난다.** 이 실행에서는 `gpt-5.6-luna`의 JA도 정상 출력(`[atomic locks](#atomic-locks) APIを`Cache::lock`で使用します。`)으로 통과했다.

**판별 검사**: 이 실행의 prompt SHA-256은 KO `8bf437f9ff84…`, JA `104d626b647a…`이고 두 모델이 같은 값을 받았다. 주 보고서 실행이 기록한 해시와 비교하면 원인이 갈린다 — 해시가 같으면 **provider 응답 변동**(같은 입력에 다른 출력)이고, 다르면 **runner/프롬프트 구성 차이**다. 후자라면 두 실행 중 하나의 환경이 운영과 다르므로 그쪽을 먼저 맞춰야 한다. 이 비교 없이는 "재현성 없는 gate"로 단정할 수 없으며, 어느 쪽이든 **이 gate 단독 결과를 무인 운영 판단 근거로 쓰면 안 된다**는 결론은 같다.

#### A.5 실제 문서 end-to-end — 0/3, 0/3

고정 표본 `VERSION=13.x`, `DOC=ai-sdk.md`. 6개 독립 checkout 모두 `645a2d4` detached에서 시작해 동일 기준 상태를 만들었다(KO/JA는 `HEAD^`, EN 캐시는 `f89a4c2^`). 공식 upstream은 `laravel/docs` 13.x `b0b1c3e17c715880e0c380cd30061da6ca952c9d` — 주 보고서가 기록한 SHA와 동일하다.

```
translating: ko i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md
verify failed: ko …/version-13.x/ai-sdk.md:
  ['partial patch failed: missing existing translation block for: > [!NOTE]']
stopping after first verification failure
```

| 모델 | run 1 | run 2 | run 3 |
|---|---|---|---|
| `gpt-5.4-mini` | FAIL | FAIL | FAIL |
| `gpt-5.6-luna` | FAIL | FAIL | FAIL |

**6회 전부 문자 단위로 동일한 오류**다. 모델·회차와 무관하므로 provider 품질 문제가 아니라 patch 엔진의 admonition 블록 처리 결함이다. `translating: ko`는 출력되므로 provider 호출까지는 도달하고, patch 적용 단계에서 막혀 JA에는 도달조차 못 한다.

이는 주 보고서 N-05를 **다른 workspace·다른 미러·다른 checkout에서 독립 재현**한 것이다.

##### fixture 아티팩트 가설 검증 — 기각됨 (중요)

부록 A.5는 KO/JA를 `HEAD^`로 되돌리게 한다. 그런데 `645a2d4`가 이 두 파일에 가한 변경은 **정확히 `> **참고:**` / `> **注意:**` → `> [!NOTE]` 정규화**다(KO 3건, JA 3건). 따라서 "A.5의 rollback이 정규화 이전 상태를 만들어 실패를 인위적으로 유발했고, 실제 운영 상태에서는 발생하지 않는다"는 가설이 성립할 수 있었다. 그렇다면 두 보고서의 headline blocker가 fixture 아티팩트가 된다.

이를 확인하려고 **production-representative fixture로 1회 추가 실행**했다. KO/JA를 `645a2d4` 그대로 두고(정규화 완료 상태, `[!NOTE]` 각 6건) EN만 upstream이 갱신하도록 한 조건이다.

```
결과: exit 1
verify failed: ko …/version-13.x/ai-sdk.md:
  ['partial patch failed: missing existing translation block for: > [!NOTE]']
```

**동일하게 실패했다. 가설은 기각된다.** 실패는 rollback이 만든 상태 때문이 아니라 실재하는 결함이다.

> 이 1회는 §0.2의 "2모델 × 3회" 범위를 넘는 추가 표본이다. 판정의 정확성이 여기에 달려 있어(headline blocker가 실재하는지 fixture 산물인지) 실행했고, 사실대로 기록한다. 모델은 `gpt-5.4-mini` 1회만 사용했다.

##### 실패의 정확한 성격

| 대상 | `> [!NOTE]` 개수 |
|---|---|
| upstream 최신 EN (13.x `b0b1c3e17`) | 4 |
| KO (`645a2d4`) | 6 |
| EN diff에서 upstream이 **새로 추가**한 것 | 1 (`+> [!NOTE]`) |

즉 이번 upstream 변경은 **새 admonition 블록을 추가**하는 것이었고, patch 엔진은 이를 삽입 대상으로 처리하지 못하고 "기존 번역 블록 찾기" 경로로 빠져 실패한다. 오류 문구(`missing existing translation block for`)가 그 경로를 그대로 드러낸다.

이것이 이 커밋의 **실질적 무인 운영 blocker**다. Laravel 문서에서 `> [!NOTE]` 추가는 흔한 변경이며, `--fail-fast` 때문에 그 문서 하나가 run 전체를 중단시킨다.

#### A.5 후속 gate — 6/6 통과, 다만 의미에 주의

| 검사 | 결과 |
|---|---|
| `validate_generated_changes.py` | 6/6 exit 0 |
| `git diff --check` | 6/6 무출력 |
| site 4단계(markdown-links · typecheck · build · validate-anchors) | 6/6 exit 0 |

**이 통과는 파이프라인이 정상 동작했다는 근거가 아니다.** 번역이 적용되지 않아 KO/JA 산출물이 원본 그대로이고, 변경된 것은 `i18n/en/.../ai-sdk.md` 하나인데 그 경로가 `_ALLOWED_PATHS`에 속하기 때문이다. 즉 **완전히 실패한 실행이 모든 후속 gate를 통과한다.**

#### A.6 no-op 재실행 — 0/6

| 조건 | 결과 |
|---|---|
| 종료 코드 0 | **미충족** (6/6 exit 1) |
| `no source changes to translate` | **미충족** (도달하지 못함) |
| provider 재호출 없음 | **미충족** (같은 patch 오류를 반복) |
| diff 해시 동일 | 충족 (6/6 `hash_same=yes`) |

첫 실행이 번역을 적용하지 못했으므로 재실행이 같은 지점에서 다시 막힌다. 파일이 변하지 않는다는 점만 유지된다.

#### F-09 transaction 부재의 실측 근거

실패한 6개 checkout 모두에 `i18n/en/.../version-13.x/ai-sdk.md`가 **변경된 채 남았다**. `upstream.main()`이 영어 캐시를 갱신한 뒤 번역이 실패했는데 롤백 경계가 없기 때문이다. workflow는 실패 시 commit하지 않아 원격 브랜치는 보호되지만, 로컬 워크트리에는 부분 산출물이 남는다. 이는 §7의 F-09 "그대로" 판정을 합성이 아닌 실제 실행으로 뒷받침한다.

#### A.7 최종 완료 판정 — **검증 미완료**

- `gpt-5.4-mini` 3/3 성공: **미충족** (0/3)
- `gpt-5.6-luna` 3/3 성공: **미충족** (0/3)
- 6개 run의 artifact/site/diff gate 통과: 충족(단 위 단서)
- 6개 run의 no-op 재실행 통과: **미충족** (0/6)
- 활성 브랜치 commit 0건 / push 0건: **충족**
- 변경이 `.review`와 검증 보고서에만 존재: **충족**

실패 표본을 지우거나 성공할 때까지 재시도하지 않았다.

#### 절차상 편차 기록

- 컨테이너의 `git clone https://github.com/laravel/docs.git`이 이 호스트에서 반복 실패했다(`curl 92 HTTP/2 stream … CANCEL`, `early EOF`) — 컨테이너 2회, 호스트 미러 3회. `http.version=HTTP/1.1`로 강제하자 첫 시도에 성공했다. 12회 반복 clone의 네트워크 불안정을 제거하려고 공식 저장소를 그대로 clone한 프로젝트 내부 read-only 미러를 만들고, 컨테이너에는 git `insteadOf`만 주입했다. **파이프라인 코드는 수정하지 않았고**, 미러 13.x SHA가 공식 값과 일치함을 확인했다.
- 부록 A.5는 세 파일을 모두 `HEAD^`로 되돌리게 하지만 `645a2d4`는 `i18n/en`을 전혀 변경하지 않아 EN에 대한 restore가 no-op이었다. 이를 보고 EN 캐시를 `f89a4c2^`로 추가로 되돌렸는데, **이 조치는 불필요했다**. `upstream.main()`이 `diff.changed_sources()`보다 먼저 실행되어 EN을 최신으로 덮어쓰므로 rollback은 관측되기 전에 지워진다. 실제 delta(+378/−3)는 upstream이 캐시된 EN보다 앞서 있었기 때문에 생긴 것이다. 무해했지만 무의미했으므로, 재현하는 사람이 같은 단계를 반복하지 않도록 기록해 둔다. (production-representative 검증에 쓴 probe도 같은 이유로 EN rollback 여부가 결과에 영향을 주지 않았다.)
- 부록 A.5의 KO/JA rollback은 이 커밋의 성격상 `> [!NOTE]` 정규화를 되돌리는 효과가 있다. 위 "fixture 아티팩트 가설 검증"에서 이것이 실패 원인이 아님을 확인했지만, **A.5 절차 자체는 이 커밋에 대해 production 상태를 대표하지 않는다.** 지시서를 다시 쓴다면 로케일 파일은 대상 커밋 상태로 두고 delta를 upstream만으로 공급하는 편이 정확하다.
- 검증용 `credential_runner`가 `dot_env` 3번째 줄의 inline comment를 "unquoted whitespace"로 거부했다. 그 줄(`TRANSLATION_REASONING_EFFORT`)에 한해 ` #` 이후를 주석으로 떼도록 보완했고, `OPENAI_API_KEY`에는 공백 금지를 그대로 유지했다. 값은 열람하지 않았다.
- site gate는 site Docker 이미지의 `npm ci`가 `ECONNRESET`으로 두 번 실패해, 동일 `package-lock.json`의 기존 `node_modules`를 링크해 호스트 Node v26.5.0으로 수행했다.

---

## 2. 주 보고서에 없는 신규 Finding

| ID | 심각도 | 요약 |
|---|---|---|
| S-01 | P1 | `validate-anchors.mjs`가 JA 문서의 절대 경로 링크를 KO 빌드에 대해 검증해, JA 앵커 깨짐을 구조적으로 볼 수 없다 |
| S-02 | P1 | response contract가 인용(admonition) 본문에 원문 주석을 요구하나 프롬프트·출하 코퍼스·최종 verifier 모두 요구하지 않는다 |
| S-03 | P1 | 전소문자 식별자만으로 된 inline-code 목록이 보호되지 않아 "원문 그대로"라는 유일한 정답이 항상 거부된다 |
| S-04 | P1 | ASCII 비율 임계값이 제품명·식별자가 많은 정상 번역을 거부한다(코퍼스 블록 실측 0.96%) |
| S-05 | P2 | JA에 문서 간 alias 앵커 9개가 누락돼 JA 사이트에 죽은 앵커가 배포 중이다 |
| S-06 | P2 | 표 행 후보 스캔이 코드 펜스 내부까지 훑어 펜스 안 코드를 로케일 텍스트로 덮어쓴다 |
| S-07 | P2 | named-section reorder가 TOC 접두부를 가진 실제 문서(99/100)에서 발동하지 않는다 |
| S-08 | P2 | `_code_plan_state`는 fail-open, 형제 `plan_state`는 fail-closed이며 docstring이 제공하지 않는 보존을 약속한다 |
| S-09 | P2 | 구조 거부 3종이 한 라벨로 수렴하고 `elif` short-circuit으로 `_signature` 상세가 독립 고정되지 않는다 |
| S-10 | P2 | negative 테스트 95건이 전부 `assertIn`이고 exact-list 단언이 0건이라 과잉거부가 검출되지 않는다 |
| S-11 | P2 | 표 패치 경로 약 110줄에 테스트가 0건이다 |
| S-12 | P3 | `sync/__init__.py`의 facade가 `sync.sidebar` 패키지 속성을 shadow해 `import sync.sidebar.generator`가 깨진다 |
| S-13 | P3 | `verify.py`가 사용하지 않는 `structural_html_tags`를 import한다 |
| S-14 | P3 | README dotenv 블록의 들여쓰기 손실로 README 후반 15줄이 코드 블록에 삼켜진다 |

---

### S-01. `validate-anchors.mjs`가 JA 문서의 절대 경로 링크를 KO 빌드에 대해 검증한다 — P1

#### 근거
이번 커밋이 `validate-anchors.mjs`의 `DOCS_ROOTS`에 JA 루트(`i18n/ja/docusaurus-plugin-content-docs`, `localePrefix: '/ja'`)를 새로 추가했다. 이전 버전(`645a2d4^`)은 `versioned_docs`(KO)만 순회했다. 그런데 신규 파일 `translation-sync/scripts/anchor-routes.mjs:17-22`의 `relativeTargetPath()`가

```js
if (path.startsWith('/')) return path;
```

로 **절대 경로에 로케일 접두사를 붙이지 않고 즉시 반환**한다. `validate-anchors.mjs:130` → `:138` `htmlPathFor()`가 `build/docs/...`(KO)를 읽는다. `sourceUrl()`은 JA에 `/ja`를 정상 부착하므로 same-page(`#x`)·상대 경로는 맞게 해석되고, 절대 `/docs/<v>/...#anchor`만 KO로 샌다. 이 코퍼스의 문서 간 링크는 전부 절대 경로 형식이다.

#### 재현 조건
이 실행의 §2.6 빌드 산출물에서:

```
grep -o 'href="[^"]*errors#logging[^"]*"' build/ja/docs/10.x/helpers/index.html  → /ja/docs/10.x/errors/#logging
grep -c 'id="logging"' build/ja/docs/10.x/errors/index.html                     → 0
grep -c 'id="logging"' build/docs/10.x/errors/index.html                        → 1
npm run validate-anchors                                                        → id not found: 0  (통과)
```

빌드 산출물 기준으로 로케일별 문서 간 앵커를 재검사하면 **KO 1,482개 중 broken 0, JA 1,482개 중 broken 9**다.

#### 영향
`make site-check`는 sync workflow와 deploy workflow **양쪽의 유일한 사이트 게이트**다. JA 문서 간 앵커는 이 게이트를 전혀 통과 검사받지 않으며, 현재 이미 9개가 죽은 채 배포된다. JA 커버리지를 추가한 이번 변경이 실질적으로 same-page 링크에만 작동한다. 이 실행의 §2.6이 `46,626 / 46,626 OK`로 통과한 것 자체가 증거다 — 그 수치는 "KO 기준 전부 정상"이라는 뜻이지 JA 커버리지를 보장하지 않는다.

#### 권고
`relativeTargetPath()`의 절대 경로 early-return을 제거하고 `srcUrl`에서 얻은 `localePrefix`를 절대 경로에도 적용한다(`/docs/...` → `${localePrefix}/docs/...`). 외부 절대 URL은 상위에서 `http(s)://`로 이미 걸러진다.

#### 완료 조건
수정 후 `npm run validate-anchors`가 현재 트리에서 JA 대상 `id not found`를 최소 9건 보고하고, S-05를 해소한 뒤 0건이 된다. `markdown-link-utils.test.mjs`에 "JA 소스의 `/docs/x` 절대 링크 → `/ja/docs/x`" 케이스를 추가한다.

---

### S-02. response contract가 인용 본문에 원문 주석을 요구해 정상 upstream 변경이 run 전체를 중단시킨다 — P1

#### 근거
`sync/verification/response_contract.py:263-275` — `_required_comments`가 `>` 라인의 인용 부호를 벗겨 `quote:{depth}` paragraph로 누적하므로 인용 본문에도 주석을 요구한다.

```python
if stripped.startswith(">"):
    ...
    append_paragraph(f"quote:{depth}", quote)
```

반면 최종 verifier `verify.py:358-360`은 `is_non_annotatable_line`(=`>`로 시작하면 True)로 인용을 건너뛴다. 프롬프트도 요구하지 않는다 — `translate.py:159-161`은 "For each translated **heading and paragraph**"라고만 한다. `docs/02-translation.md`·`docs/04-verification.md` 어디에도 인용 본문 주석 필수 규정이 없다.

#### 재현 조건
저장소 자체 fixture(`tests/test_patch.py:1851`)의 hunk로 plan을 만들어 provider에 전달되는 segment를 확인:

```
segment: '> Vector search requires the AI SDK and PostgreSQL or MongoDB.\n'
contract required comments: ['Vector search requires the AI SDK and PostgreSQL or MongoDB.']
final verifier required comments: set()
  A) 미주석 인용 본문(출하 코퍼스 형식) → ['provider original comment mismatch', 'provider annotation ownership mismatch']
  C) 인용 안 주석 `> <!-- EN -->`      → []
```

통과하는 형식은 (C) 하나뿐인데 **출하 코퍼스는 (A)**다 — ko 3,383건 중 주석 보유 49건, ja 3,380건 중 7건으로 **98.5%가 미주석**. 모델에 함께 전달되는 `Existing Translation Context`도 (A)이고, 재시도 피드백(`main.py:143-150`)은 "Include the English source comments required by the existing annotated format"이라 하여 **잘못된 방향으로 유도**한다.

#### 영향
`MAX_SEGMENT_VERIFICATION_ATTEMPTS = 2`이므로 2회 모두 거부 → `IncompleteTranslation` → `Makefile:37-43`이 항상 붙이는 `--fail-fast`로 **run 전체 중단**. 그 run의 커밋은 0건이 되어 성공한 다른 문서까지 반영되지 않는다. `> [!NOTE]` 본문 수정은 Laravel 문서에서 흔하다.

주 보고서 N-05(실제 `ai-sdk.md` sync가 `missing existing translation block for: > [!NOTE]`로 3/3 실패)와 **같은 문법 영역**을 다른 층에서 관측한 것이다. 주 보고서는 patch lookup 층에서, 이 항목은 response contract 층에서 인용 블록 처리가 어긋나 있음을 보인다. 두 층 모두 확인해야 한다.

#### 권고
둘 중 하나로 정렬한다. (a) `_required_comments`에서 인용 본문을 `verify.py`와 동일하게 주석 비요구로 두거나, (b) 요구를 유지한다면 `_ANNOTATION_FORMAT`에 인용 규칙과 `> <!-- EN -->` 예시를 명시하고 기존 코퍼스 3,383건을 마이그레이션하며 `docs/02`·`04`에 기록한다.

#### 완료 조건
출하 코퍼스 형식(A) 응답이 contract를 통과하거나(a), 프롬프트·문서·코퍼스가 (C)로 일치하고(b), 각 경우를 고정하는 positive/negative 테스트가 추가된다.

---

### S-03. 전소문자 식별자 목록이 보호되지 않아 유일한 정답이 항상 거부된다 — P1

#### 근거
`response_contract.py:876-884`

```python
def _term_like(token: str) -> bool:
    lowered = token.lower()
    return bool(
        lowered in _LOWERCASE_TECH_TERMS   # {"npm","php","macos"} 3개뿐
        or token.isupper() or token[:1].isupper()
        or any(char.isdigit() for char in token)
        or any(char.isupper() for char in token[1:])
    )
```

`_term_like("data")` → `False`. `_is_bare_protected_term_list`가 False가 되어 목록이 일반 prose로 언어·echo 검사를 받는데, `_language_sample`(908-915)이 인라인 코드를 제거하므로 sample에는 공백만 남는다.

#### 재현 조건
```python
src = "- `data`\n- `render`\n- `resolve`\n- `shouldRender`\n"   # blade.md 컴포넌트 메서드 목록
tr  = "<!-- - `data` - `render` - `resolve` - `shouldRender` -->\n" + src   # 유일한 정답
response_contract.verify(tr, src, locale="ko")
# -> ['provider untranslated source text', 'provider target language mismatch']
```

첫 글자만 대문자로 바꾸면 통과한다(`- \`Data\`` → `[]`). `- \`Laravel\Cashier\Events\WebhookReceived\`` 목록도 동일하게 거부되며, 이는 `billing.md`·`cashier-paddle.md`·`blade.md`의 실재 블록이다. `patch.py:104-113`의 `provider_free` 우회는 fenced code·named anchor·`^\[..\]\(#..\)$`만 대상이므로 이 블록은 반드시 contract를 거친다.

#### 영향
정답이 "원문 그대로" 하나뿐인 블록을 contract가 거부한다. 재시도로 흡수 불가 → run 중단. 해당 문서들은 upstream에서 메서드가 추가될 때마다 바뀌는 목록이다.

주 보고서 N-06(제품명 `Laravel Vapor` 오탐)과 **원인 메커니즘이 다르다**. N-06은 echo 규칙(`source_body in translated_body`)이 원인이고, 이 항목은 `_term_like`의 대소문자 가정이 원인이다. 한쪽만 고쳐도 다른 쪽은 남는다.

#### 권고
`_is_bare_protected_term_list`가 **항목 전체가 인라인 코드 span인 경우** 대소문자와 무관하게 보호하도록 확장하거나, `_language_sample` 결과가 비면(번역 가능한 자연어 없음) 언어·echo 검사를 면제한다.

#### 완료 조건
위 `src`/`tr` 쌍이 `[]`를 반환하고 이를 고정하는 accept 테스트가 추가되며, 되돌리면 그 테스트가 실패한다.

---

### S-04. ASCII 비율 임계값이 제품명·식별자가 많은 정상 번역을 거부한다 — P1

#### 근거
`response_contract.py:1123-1124`

```python
ascii_letters = len(re.findall(r"[A-Za-z]", sample))
return ascii_letters <= target_count * 2 + 2
```

`source_word_count`는 코드 제거 **전** 본문에서 세는데 `target_count`/`ascii_letters`는 코드·링크 제거 **후** sample에서 센다 — 기준이 다르다.

#### 재현 조건
실제 출하 문서 `13.x/ai-sdk.md`의 문단:

```python
src = "**Supported providers:** Anthropic, Gemini\n"
tr  = "<!-- **Supported providers:** Anthropic, Gemini -->\n**지원 제공자:** Anthropic, Gemini\n"
response_contract.verify(tr, src, locale="ko")   # -> ['provider target language mismatch']
# target=5(지원제공자), ascii=15(Anthropic+Gemini) → 15 > 5*2+2=12
```

코퍼스 실측(13.x + master, block signature가 1:1로 정렬된 문서만): **정렬된 prose 블록 31,934건 중 306건(0.96%) 거부**. 표본에 `ai-sdk.md`의 provider 목록, `ai.md`의 지원 스택, `contributions.md`의 저장소 링크 목록 등 명백한 정상 번역이 포함된다.

#### 영향
결정론적 판정이므로 재시도 2회로 흡수되지 않는다. 해당 블록이 바뀌는 순간 run이 중단된다. Laravel 문서는 제품명·클래스명이 많아 이 형태가 흔하다. 이 항목은 주 보고서 N-06과 **동일한 `_has_target_language`/echo 계열이지만 다른 판정식**(비율 백스톱)이며, 코퍼스 규모 실측이 이 문서에만 있다.

#### 권고
비율 백스톱을 절대 문자 수가 아니라 **원문 대비 상대 비율**로 바꾸거나(번역문 ascii ≤ 원문 ascii), 제품명·식별자 토큰을 sample에서 제외한 뒤 계산한다. 3개짜리 `_LOWERCASE_TECH_TERMS`에 의존하는 현재 구조를 대체해야 한다.

#### 완료 조건
위 두 입력이 `[]`를 반환하고, 코퍼스 실측 거부율이 유의미하게 내려가며, 두 shape를 고정하는 accept 테스트가 추가된다.

---

### P2·P3 상세 (축약)

#### S-05. JA에 문서 간 alias 앵커 9개가 누락돼 있다 — P2
KO(`versioned_docs`)와 JA(`i18n/ja`)의 `data-translation-alias` 앵커를 전량 대조한 결과 JA에만 없는 alias가 9개다 — `errors.md#logging`(8.x/9.x/10.x), `migrations.md#writing-migrations`(8.x/9.x/10.x), `database-testing.md#writing-factories`(8.x), `helpers.md#fluent-strings`(10.x), `eloquent-mutators.md#date-casting`(8.x). 빌드 스캔의 JA broken 9건 분포와 정확히 일치한다. 이번 커밋이 JA에 **추가한** alias 5개는 모두 **동일 문서 내부** `#x` 링크 대상으로 링크 클래스가 다르다. **권고**: KO의 alias 집합을 JA에 대칭 반영하고, alias 생성이 same-page 링크만 스캔한다면 문서 간 절대 링크도 대상에 넣는다.

#### S-06. 표 행 후보 스캔이 코드 펜스 내부까지 훑는다 — P2
`patch.py:2674-2681`의 후보 스캔 루프에 코드 펜스 제외가 없다. 같은 파일에 `_code_fence_regions`(2049)가 있으나 호출되지 않는다. 매칭 기준이 **영문** 후행 셀이므로 번역된 로케일 표 행은 탈락하고, 펜스 안에 영문으로 남아 있는 예시 행만 후보가 된다. 실측: `_table_row_index -> 8`(펜스 영역 `[(7,9)]` 내부) → 진짜 표 행은 미갱신인 채 펜스 안이 한국어로 오염, `verify: ['inline code mismatch', 'code block mismatch']`. 실제 코퍼스에 이 형태가 있다(`version-12.x/notifications.md:968-971`, `mail.md:862-865`). 최종 verifier가 커밋을 막으므로 문서 손상은 아니지만, 정당한 표 행 갱신이 영구 적용 불가가 되고 오류 메시지가 원인과 무관한 곳을 가리킨다. 주 보고서 N-02와 **같은 함수의 다른 결함**이다(N-02는 단일 후보 시 context 미확인, 이 항목은 후보 집합 자체가 오염). **권고**: 후보 스캔에서 `_code_fence_regions`를 제외한다. 같은 파일의 `_searchable_raw_indexes`(2603)가 이미 동등한 제외를 한다.

#### S-07. named-section reorder가 실제 문서 형태에서 발동하지 않는다 — P2 (F-05 판정 상충)
`patch.py:2941`의 `if old_prefix != new_prefix or len(old_sections) < 2: return None`. `old_prefix`는 첫 `<a name>` 이전 전체 텍스트인데, Laravel 문서는 여기에 앵커 TOC를 두므로 section 이동 시 TOC도 함께 움직여 접두부가 달라진다. 실측: TOC 2줄 + 두 section을 함께 swap한 입력 → `named_section_reorder: None` → 일반 diff 경로 → `PatchError: missing existing translation block for: <a name="beta"></a> ## Beta`. 번역 2건을 실제 공급해도 동일. **`version-13.x`의 앵커 보유 100개 문서 중 99개**가 TOC 접두부를 갖는다. 기존 F-05 fixture는 파이프라인 레벨 테스트를 포함해 전부 접두부가 없거나 동일한 합성 형태다. **권고**: 접두부 변경이 "이동한 section에 대응하는 TOC 항목 재정렬"만으로 설명될 때는 reorder로 인정하고 그 외는 fail-closed 유지.

#### S-08. `_code_plan_state`는 fail-open, 형제 `plan_state`는 fail-closed — P2
`patch.py:748-759`가 로케일 코드 블록이 old/new 어느 쪽과도 불일치할 때 `return PlanState.UNGUARDED`로 진행한다. 20줄 위 `plan_state`(724)는 같은 조건에서 `raise PatchError`한다. `CodeChange` docstring(152-155)은 "a diverged document is left untouched rather than corrupted"라고 약속하지만, 실측에서 로컬 추가 줄 `$local = 'custom';`이 **조용히 삭제**되고 문서 단위 `verify`는 `[]`였다. 로케일 코드는 영문과 바이트 동일해야 하므로 최종 상태로는 옳다. 실질 손해는 자매 함수 간 정책 반전과 docstring 불일치다. **권고**: docstring을 실제 동작에 맞게 정정하거나 `_code_plan_state`를 명시적 예외로 바꾼다(둘 중 하나).

#### S-09. 구조 거부 3종이 한 라벨로 수렴한다 — P2
`response_contract.py:1216-1227`의 4단계가 모두 `provider block structure mismatch`를 쓰고 `elif`로 연결돼 뒤 단계가 가려진다. mutation 실측: `_signature`를 `(block.kind,)`로 축약해도 **실패 테스트 0건**(런타임은 fall-through가 대신 수행), 4단계 전부 제거하면 15건 실패. 즉 합집합만 고정되고 개별 방어는 고정되지 않았다. **권고**: 4단계에 각각 다른 라벨을 부여하고 `elif`를 독립 `if`로 분리한다.

#### S-10. negative 테스트에 exact-list 단언이 0건 — P2
`test_verify.py` 137건 중 `assertIn` 95 / `assertNotIn` 24 / `assertEqual` 37이고, `assertEqual`의 거의 전부가 `== []`(accept)다. **비어 있지 않은 정확한 issue 목록을 단언하는 negative 테스트가 0건**이다. 균형 잡힌 반대 증거도 있다 — `_has_target_language`를 항상 False로 만들면 24개 accept 테스트가 실패하므로 **전면적** 과잉거부는 막힌다. 막지 못하는 것이 S-02·S-03·S-04의 **특정 shape**다. 추가로 `test_rejects_comment_without_owned_body`(542)는 이름과 달리 ownership을 고정하지 않는다(mutation 시 실패하지 않으며, 단언하는 라벨은 block 수 비교에서 나온다). **권고**: 5종 거부의 대표 테스트를 `assertEqual(issues, ["<label>"])`로 승격한다.

#### S-11. 표 패치 경로 약 110줄에 테스트가 0건 — P2
`patch.py:2637-2717`의 6개 함수에 대해 `tests/test_patch.py` 81개 중 표를 다루는 테스트가 0건이다. 구조적 이유가 있다 — 표 행은 `is_non_annotatable_line`(markdown.py:453)에 의해 `_source_blocks`에서 제외되므로 `plan_state` 판정도, `apply_plan`(670-672)의 앵커 시퀀스 동일성 검사도 표 변경에 제약을 걸지 않는다. 유일한 방어는 후행 셀 일치와 컨텍스트 좁히기이며, 그 방어가 뚫리는 사례가 S-06과 주 보고서 N-02다. **가장 방어가 얇은 경로가 가장 검증이 안 된 경로와 일치한다.** **권고**: 정상 교체 / 중복 시 컨텍스트 좁히기 / 펜스 내부 배제 / 로케일 셀 번역 시 fail-closed 4개 테스트 추가.

#### S-12. facade가 `sync.sidebar` 패키지 속성을 shadow한다 — P3
`sync/__init__.py`의 `from .sidebar import generator as sidebar`가 패키지 속성을 덮어 `from sync.sidebar import generator`는 되지만 `import sync.sidebar.generator`는 `ImportError`가 된다. 저장소 내 사용처는 0건이라 실무 영향은 없다. `sidebar`만 `_ALIASES`의 `sys.modules` 등록에서 제외한 것 자체는 **올바른 회피**다(패키지를 덮으면 하위 모듈 import가 깨진다). 이 평탄화 설계는 `translation-sync/docs/` 어디에도 문서화되어 있지 않다. **권고**: facade 규칙을 docstring이나 문서에 명시한다.

#### S-13. `verify.py`가 사용하지 않는 심볼을 import한다 — P3
`verify.py:31`의 `structural_html_tags`가 파일 내에서 참조되지 않는다. 프로젝트에 lint 설정이 없어 CI가 잡지 못한다. **권고**: import 제거.

#### S-14. README 코드 블록이 깨진다 — P3
645a2d4 diff에서 `AZURE_OPENAI_API_VERSION=` 줄만 3칸 들여쓰기를 잃어, 닫는 펜스가 여는 펜스로 재해석되고 README 후반 15줄(621 bytes)이 언어 없는 코드 블록에 삼켜진다. mdast 파싱으로 확인했다(`root>code lang=null`, line 76-90). 런타임 영향은 없고 저장소 첫 화면 렌더만 깨진다. **권고**: 해당 줄 들여쓰기 복원.

---

## 3. 주 보고서와 판정이 갈리는 항목

| 항목 | 주 보고서 | 이 문서 | 근거 |
|---|---|---|---|
| **F-05** named-section reorder | **확인됨** | **부분적 (미완결)** | A-1/A-2는 양쪽 모두 통과. 이 문서는 여기에 A-3(우회 입력)을 추가로 물었고, `patch.py:2941`의 접두부 바이트 동일성 요구 때문에 **TOC를 가진 실제 문서 99/100**에서 경로가 꺼짐을 실측했다(S-07). 합성 fixture에서만 성립하는 "해결"이다 |
| **F-08** prompt 규칙 충돌 제거 | **부분적** | **미확인** | 두 문서 모두 KO에 대응 hard rule이 없음을 지적한다. 이 문서는 추가로 **되돌림 테스트**를 실행했다 — `prompt.md`/`prompt_jp.md`를 이전 내용으로 되돌려도 419개 중 **실패 0건**이다(어떤 테스트도 두 파일을 읽지 않는다). `prompt.py`는 파일을 읽어 `.strip()`할 뿐이고 `test_prompt.py` 2건은 로딩만 검증한다. 강제 지점이 0이므로 "부분적"이 아니라 "미확인"이다 |
| **F-13** 정규화기 손상 수정 | **부분적** | **확인됨** | 이 문서는 5개 항목 각각에 대해 **해당 fix hunk만 `3aab108` 상태로 되돌린 하이브리드**(구 구현 + 신 테스트)를 컨테이너에서 실행해 전부 테스트 실패를 확인했다. 단서 하나: `test_does_not_treat_stylesheet_as_style`은 단일 hunk 되돌리기로는 실패하지 않고 두 hunk 동시 되돌림에서만 실패한다(방어 중복) |
| **F-03** provider check contract 공유 | **부분적** | **확인됨(테스트 공백은 별도)** | `provider_check.py:123-124`가 production과 동일한 `response_contract.verify` + `verify.verify`를 호출하며, 갈라지는 지점은 전부 provider_check가 **더 엄격**한 방향이다. 다만 `main()` 자체에 테스트가 0건이라 "KO/JA 모두 검사"가 고정돼 있지 않다 — `_locales`를 `return (value,)`로 바꿔도 348개 테스트가 전부 통과한다 |
| **F-15** Markdown 문법 범위 | (개별 판정 없음) | **그대로, 단 현재 corpus에서 휴면** | 5개 항목 전부 fixture로 무변화 실측. 여러 줄 code span은 pre-fix와 **바이트 동일** 출력, multi-backtick span은 `markdown.py`에 code-span helper 자체가 부재, link title은 double-quoted만 지원(이번 커밋 이전에도 동일). **다만 `i18n/en` 678개 문서 전수 census에서 이 5개 문법의 실제 사례가 0건**이므로 활성 위험은 provider 응답 쪽뿐이다. 이번 커밋의 실제 parser 이득은 balanced-paren link destination 지원이다 |

---

## 4. 두 문서가 같은 결론에 도달한 항목

| 주제 | 주 보고서 | 이 문서 | 공통 결론 |
|---|---|---|---|
| 표 행 패치 결함 | N-02 (단일 후보 시 raw context 미확인) | S-06 (후보 스캔이 펜스 내부 포함) | `_table_row_index`가 **두 가지 독립된 이유로** 잘못된 행을 고른다. 함께 고쳐야 한다 |
| response contract 과잉거부 | N-06 (echo 규칙, 제품명) | S-03(`_term_like` 대소문자), S-04(ASCII 비율) | 세 개의 **서로 다른 판정식**이 각각 정상 번역을 거부한다. 하나만 고치면 나머지가 남는다 |
| config 검증 순서 | N-09 | (본문 §7 F-09 항목) | `config.load_config()`가 `upstream.main()` 뒤라 설정 오류 실행도 EN 캐시를 갈아엎는다. 선행 보고서 자신의 F-06 권고와 어긋난다 |
| 산출물 validator | N-07 | (동일 결론) | `versions.json` membership 미검증, 임의 basename 허용, 삭제 규모 미확인. 다만 코드·workflow·프롬프트로의 **우회 경로는 없다** |
| upstream 실패 정규화 | N-08 | **실제 네트워크 실패로 독립 재현** | 이 실행의 probe에서 `laravel/docs` clone이 실 네트워크 오류(`RPC failed; curl 92 ... early EOF`)로 끊겼다. 결과는 정제된 `upstream sync failed`가 아니라 **`CalledProcessError`의 raw traceback이 그대로 탈출**했다(`upstream.py:145` → `:33`). N-08이 지적한 "초기 clone이 try 밖"이 합성 fixture가 아니라 실제 장애에서 그대로 발현함을 확인한다 |
| F-01 종료 | 종료 | 닫힘 | import seam 성립(모듈 중복 로드 0), 문서 00~08 정확, stale 링크 없음 |
| F-09 transaction | 그대로 | 그대로 | 롤백·staging 경계 없음. workflow는 실패 시 commit하지 않아 원격 branch는 보호됨 |
| F-16 / F-10 | 확인됨 | 확인됨 | 하드코딩 제거 완료, Node 26 7개 표면 일관 |
| 테스트 삭제·약화 | (언급 없음) | **없음** | 파일별 `git show 645a2d4 -- <file> \| grep '^-'` 전수 확인. 제거된 줄은 사라진 helper 잔재이거나 rename이며 일부는 오히려 강화됐다 |

---

## 5. 이 실행의 한계

- **live 실행 범위**: provider contract 2회(모델별 1회)와 실제 문서 1건에 대한 모델별 3회, 그리고 no-op 재실행 6회를 수행했다(§1-A). 전체 Laravel 문서군의 의미 정확성이나 장기 provider 안정성은 이 표본으로 판정할 수 없다. 특히 **A.5가 KO 단계에서 막혀 JA 번역 경로는 실행되지 못했으므로, JA end-to-end는 이번에도 미검증이다.**
- **provider contract의 재현성 한계**: 같은 커밋·같은 fixture에 대해 이 실행은 두 모델 모두 통과, 병행 실행은 `gpt-5.6-luna` JA 실패로 결과가 갈렸다. 이 gate 단독 결과를 무인 운영 판단 근거로 쓸 수 없다.
- **replay 미실행**: `make translation-replay` / `make translation-check`는 지시서의 commit 금지 규정에 따라 실행하지 않았다. 선행 보고서의 "679개 문서 identity replay"는 **이번에도 재확립되지 않았다**.
- **replay가 증명하는 것과 아닌 것**(코드 검토 기준): 판정 기준은 파일 해시가 아니라 `_worktree_fingerprint`(HEAD sha + tree sha + `status --porcelain -z -uall` + `diff --binary` + untracked 바이트의 SHA-256)다. 증명하지 않는 것은 번역 의미, **`response_contract.verify` 표면 전체**(identity 경로는 이를 우회), patch 재적용 멱등성(1회차 결과가 sandbox에 commit되므로 2회차는 조기 종료해 파이프라인에 재진입하지 않는다), added-document 경로다.
- **Azure 미검증**: `dot_env`에 Azure key가 없다.
- **secret 비열람**: key 이름과 구조만 확인했고 값은 읽지 않았다.
- **`_ALLOWED_PATHS` 판정 근거**: clean checkout gate 통과가 아니라 정규식 프로브 결과다.
- 활성 브랜치에 commit·push·merge·rebase·tag **0건**. 변경은 `.review/`와 이 보고서에만 존재한다.

---

## 6. 종합

**A.7 판정: 검증 미완료. merge 불가.** 주 보고서와 같은 결론이며, 이 문서는 그 결론을 독립 실행으로 확인하고 blocker 목록을 넓힌다.

A.7 항목별 결과는 §1-A에 있다. 요약하면 두 모델 모두 **0/3**, no-op **0/6**이고, 활성 브랜치 commit·push는 **0건**이다.

이번 live 실행에서 가장 중요한 관측은 **완전히 실패한 실행이 후속 gate를 6/6 통과했다**는 점이다. 번역이 하나도 적용되지 않아 산출물이 원본과 같고, 변경된 `i18n/en/...`이 허용 경로에 속하기 때문이다. 즉 `artifact-check` + `site-check` + `git diff --check` 조합은 "파이프라인이 제 일을 했는가"를 판정하지 못한다. 이 gate들을 통과 신호로 삼는 workflow 설계는 재검토가 필요하다.

live 실패(`missing existing translation block for: > [!NOTE]`)와 이 문서의 S-02(response contract가 인용 본문에 주석을 요구하나 출하 코퍼스 98.5%는 미주석)는 **같은 문법 영역을 서로 다른 층에서 관측한 것**이다. 인용/admonition 블록 처리가 patch lookup 층과 contract 층 양쪽에서 어긋나 있으므로, 한 층만 고치면 다른 층에서 다시 막힐 가능성이 높다. 수정 시 두 층을 함께 봐야 한다.

권장 처리 순서:

1. **인용/admonition 블록 경로** — 주 N-05(patch lookup) + S-02(contract 주석 요구). 실제 sync를 막고 있는 최우선 blocker다.
2. **response contract 과잉거부 3종** — 주 N-06 + S-03 + S-04. 서로 다른 판정식이므로 개별로 닫고, S-10(exact-list 단언)을 함께 도입해 향후 과잉거부가 테스트에 드러나게 한다.
3. **표 행 패치** — 주 N-02 + S-06 + S-11(테스트 공백). 한 함수의 두 결함과 그 경로의 테스트 부재를 함께 처리한다.
4. **S-01 + S-05** — JA 앵커 게이트 맹점과 실제 죽은 앵커 9개. 게이트를 먼저 고치면 S-05가 자동으로 드러난다.
5. 주 N-01/N-03/N-04(TARGET 판정, 중복 anchor 위치, upstream version token 경로 탈출)와 나머지 P2·P3.
