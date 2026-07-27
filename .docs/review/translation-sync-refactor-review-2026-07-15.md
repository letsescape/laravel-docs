# Translation Sync 리팩토링 검증 보고서

최초 작성: 2026-07-15 01:03 KST

최종 재검증: 2026-07-18 KST

## 1. 결론

7월 15일에 확인한 기존 P1 오류는 현재 워킹 트리에서 회귀 테스트와 함께 해결됐다. 이번 00~08 문서 전수 검토에서는 F-13의 구체적인 정규화 오류와 F-16의 sidebar version 파생 오류를 추가로 재현해 수정했으며, 새 provider 응답은 문서에 쓰기 전에 본문 누락, 긴 영어 echo, 중복 occurrence 누락, 추가 prose, 지원되는 Markdown 구조와 잘못된 Laravel version 링크를 거부한다.

현재 전체 워킹 트리는 다음 gate를 통과했다.

- Python **419 tests passed**
- 실제 upstream **679개 문서** identity replay 통과
- 현재 delta **12개 문서 × KO/JA** 적용 후 두 번째 새 프로세스 no-op
- 기존 KO/JA 산출물 전체 annotation check 통과
- Node `v26.4.0`의 Markdown-link test, typecheck, KO/JA build 통과
- KO/JA inline Markdown fragment target **46,626 / 46,626 OK**
- `git diff --check` 통과
- 현재 index만 내보낸 임시 저장소는 Python test import 단계에서 **실패**(`Ran 153 tests`, `errors=1`)

따라서 전체 워킹 트리의 결정적 gate는 통과하지만, **현재 index는 커밋 가능한 상태가 아니다(F-01, P0)**. staged `provider_check.py`가 index에 없는 `sync.response_contract`를 import하며, 문서 index도 두 개의 `07-*` 파일을 만들고 최신 `08-error-cases.md`와 갱신된 00 문서를 누락한다. 현재 수정안을 merge하려면 마지막 항목이 필수이고, 자동 운영 전에는 앞의 네 항목도 해당 범위에 맞게 완료해야 한다.

1. provider 호출 전에 영어 legacy note marker를 canonical GitHub Markdown alert로 바꾸는 F-14의 처리 시점 문제를 해결하거나, 자동 운영의 명시적 제한으로 수용한다.
2. F-15의 multiline code span 손상을 막고 inline-code delimiter와 유효 link title 보존 검사를 공통 parser로 보강한다.
3. 실제 credential 환경에서 `gpt-5.6-luna`의 KO/JA provider check와 대표 문서 품질 표본을 확인한다.
4. Azure를 운영 provider로 쓴다면 legacy 날짜형 API를 계속 쓸지 Microsoft가 권장하는 v1 API로 옮길지 결정하고, 해당 deployment에서 실제 호출을 검증한다.
5. 이번 merge 범위의 변경을 모두 끝낸 뒤 최종 intended diff를 stage하고, 그 index snapshot에서 Python test, replay, site/artifact gate를 다시 실행한다.

현재 판정은 **워킹 트리 gate 통과, 현재 index merge 불가, 자동 운영 조건부**다. F-09의 실행 전체 transaction, provider telemetry와 prompt 축소는 후속 개선이지만, F-14의 처리 시점과 F-15의 문법 범위는 새 자동 번역 입력을 받을 때 고려해야 하는 정확성 경계다.

## 2. 검토 기준과 스냅샷

### 2.1 범위

다음을 함께 검토했다.

- staged, unstaged, untracked를 포함한 현재 로컬 초안 전체
- `translation-sync/docs`의 00~08 문서 전부
- translation sync의 upstream 동기화, diff, preprocess, patch, provider, postprocess, verify, sidebar, replay
- GitHub Actions의 sync/deploy 흐름과 Make target
- 한국어·일본어 운영 프롬프트
- OpenAI Responses API, Azure Chat Completions, Codex CLI adapter의 역할과 차이
- Python 테스트, 실제 upstream identity replay, Docusaurus build/anchor 검증

`translation-sync/docs/CLAUDE.md`도 확인했다. 이 파일은 내용이 비어 있는 43-byte `<claude-mem-context>` stub으로 프로젝트 사양이나 검토 finding은 포함하지 않는다.

후속 재검증에서는 구현과 맞지 않던 문서 표현, cron 주석, CLI 호환 버전과 Azure API version 예시를 최소 범위로 바로잡았다. 별도 커밋이나 staging 변경은 만들지 않았다.

### 2.2 관찰한 상태

| 항목 | 값 |
|---|---|
| HEAD | `3aab108cf588b2cefb1248a79a9e7b173f25c568` |
| staged | 신규 파일 11개 |
| unstaged | 66개 경로(`AM`/`AD` 포함) |
| untracked | `translation-sync/docs/08-error-cases.md` 1개 |
| `main.py` | `ea086e913962` |
| `provider_check.py` | `3ecc2a332ae5` |
| `patch.py` | `ff889b98a8bd` |
| `verify.py` | `3d3a33861113` |
| `response_contract.py` | `52a094fead69` |
| `translate.py` | `ba8114719bb6` |
| `common/markdown.py` | `93652bcbf079` |
| `preprocess.py` | `b17954d31dff` |
| `postprocess.py` | `596cfa5460db` |
| `sidebar/generator.py` | `961922e28e7b` |
| KO prompt | `9aef3d92ea65` |
| JA prompt | `dd737ab65608` |

이 보고서의 현재 판정은 위 전체 워킹 트리 기준이다. 현재 index snapshot은 전체 intended diff를 포함하지 않을 뿐 아니라 import 단계에서 실패하므로 최종 커밋 후보로 사용할 수 없다.

### 2.3 심각도

- **P0 / release blocker**: 현재 커밋 또는 운영 반영을 막아야 한다.
- **P1 / high**: 자동 커밋에 잘못된 문서가 들어가거나 정상 upstream 변경이 막힐 가능성이 있다.
- **P2 / medium**: 오류 진단, 재현성, provider 일관성, 유지보수성을 유의미하게 낮춘다.
- **P3 / low**: 현재 운영 경로는 통과하지만 계약·개발 환경을 더 정확하게 만들 필요가 있다.

### 2.4 문서별 완료 감사

누락 여부를 파일 단위로 확인한 결과는 다음과 같다.

| 파일 | 대조한 핵심 계약 | 결과 |
|---|---|---|
| `00-workflow-summary.md` | 단계 순서, 00~08 교차 링크, retry 횟수, replay/site/git gate | 최초 포함 요청 횟수와 site 검사 범위를 수정 |
| `01-preprocessing.md` | raw source 보존, base64/style/title/list 전처리, config fail-fast | heading ID·sentinel·style/list 경계를 F-13에서 수정하고 예약 sentinel·unclosed style·code-span 한계를 명시 |
| `02-translation.md` | literal diff/PatchPlan, provider-free 변경, API/CLI adapter, retry/response contract | retry, 독립 fenced-code-only 범위와 inline-link parser subset을 실제 구현에 맞춤 |
| `03-postprocessing.md` | image, alert, version, title class, HTML comment, whitespace | alert 지원 type, heading ID와 inline-code 한계를 명시; fence/note/JSX img 구현을 F-13에서 수정 |
| `04-verification.md` | response contract와 final verifier 책임, link/code/anchor/HTML 범위 | stale img/heading regex를 실제 scanner로 수정하고 link/code parser 범위를 명시 |
| `05-additional-work.md` | source cache, KO/JA 산출, sidebar, site/artifact, branch 반영 | site gate, live fail-fast와 `versions.json` ordering contract를 실제 범위로 수정 |
| `06-sidebar-sync.md` | documentation parser, version/file naming, duplicate occurrence, locale override | future version 파생과 silent omission을 수정; latest-stable 순서 전제를 명시 |
| `07-local-replay.md` | tracked/nonignored-untracked snapshot, symlink, manifest, 두 process 수렴, exit code | fingerprint 범위 표현 수정; replay와 symlink 회귀 테스트 대조 |
| `08-error-cases.md` | 2026-06-23~07-03 실패 8건, 역사/현재 상태 분리, P/T/R/V/S/A 분류 | P/V 공동 최다, retry·owner·occurrence·multiset 및 F-14/F-15/F-18 현재 상태 수정 |
| `CLAUDE.md` | agent-memory 내용 유무 | 43-byte 빈 context stub이며 프로젝트 계약 없음 |

이 보고서의 실제 Markdown hyperlink 고유 URL 23개와 00~08 문서의 외부 URL 1개, 총 24개는 최종 감사에서 redirect를 따라 모두 HTTP 200을 반환했다. 내용 근거가 필요한 현재성 주장은 3.4·3.5와 F-11~F-18의 OpenAI, Microsoft, GitHub, Docusaurus, CommonMark 공식 자료를 직접 대조했다.

## 3. 확인된 강점

### 3.1 현재 워킹 트리의 테스트와 replay

- `UV_CACHE_DIR=/private/tmp/laravel-docs-uv-cache make translation-check`
  - **419 tests passed**
  - master, 13.x, 12.x, 11.x, 10.x, 9.x, 8.x의 upstream 문서 **679개** 동기화
  - 실제 현재 delta 12개 문서를 KO/JA에 적용
  - 두 번째 새 프로세스는 `no source changes to translate`로 종료
- 현재 index를 임시 저장소로 export한 뒤 Python test 실행
  - **153 tests 실행 중 import error 1건으로 실패**
  - staged `provider_check.py`가 index에 없는 `sync.response_contract`를 import
- `uv run --frozen --python 3.14 python main.py --check-annotations`
  - 최초 감사에서 영어 legacy marker 2건을 검출해 실패
  - 지역화되어 verifier가 놓치던 marker 28건과 함께 canonical alert로 정리하고 미번역 영어 본문 1건을 번역한 뒤 **pass**

이 결과는 현재 실제 upstream delta에 대해 patch engine이 동작하고, active worktree를 건드리지 않는 replay 격리가 작동한다는 강한 긍정 증거다.

### 3.2 workflow 안전장치

다음 설계는 유지할 가치가 있다.

- replay가 만든 upstream manifest를 live run이 재사용해 두 단계 사이의 upstream drift를 막는다.
- source/target/partial 상태를 구분하고, 모호한 patch는 추정 적용하지 않고 실패한다.
- 삭제, 순수한 독립 fenced-code-only 변경, bare internal-link list를 provider 없이 결정적으로 처리한다.
- provider 결과를 block 기준으로 먼저 검증하고 적용 후 전체 최신 source로 다시 검증한다.
- translation, site build, KO/JA inline Markdown fragment target, generated path scope가 모두 통과해야만 커밋한다.
- `main`이 아닌 수동 실행 branch에는 배포를 트리거하지 않는다.
- CLI command를 `shell=True` 없이 `shlex.split` 결과로 실행하고 임시 디렉터리와 `--output-last-message`를 사용한다.

### 3.3 사이트 검증

Node `v26.4.0`, npm `11.17.0`에서 다음을 확인했다.

- Markdown link utility test 성공
- TypeScript typecheck 성공
- Docusaurus KO/JA 전체 build 성공
- KO/JA inline Markdown fragment target 검증: **46,626 / 46,626 OK**
- missing HTML: 0
- missing id: 0

Docusaurus의 공식 최소 요구사항은 Node 20 이상이므로 Node 26은 버전 범위 안에 있다. 다만 Node 26은 2026년 10월 전까지 Current release이며 아직 LTS가 아니다. 이는 사용자가 선택한 런타임 정책으로 보고 되돌리지 않았다.

### 3.4 모델과 API 선택

`gpt-5.6-luna`는 공식적으로 존재하며 Responses와 Chat Completions를 지원하는 reasoning model이다. OpenAI 공식 문서는 Luna를 비용 민감·대량 workload용으로 설명하고, `medium`을 균형 잡힌 reasoning 시작점으로 제시한다.

- [GPT-5.6 Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [GPT-5.6 model/reasoning guidance](https://developers.openai.com/api/docs/guides/latest-model#update-api-and-model-parameters)

따라서 모델 ID, OpenAI Responses API, `reasoning.effort=medium`, `store=false` 선택 자체는 타당하다. `codex exec`의 prompt-plus-stdin 사용도 공식 non-interactive 문서 및 설치된 `codex-cli 0.144.5`의 실제 옵션 파싱과 일치한다.

다만 “지원되는 모델”과 “이 문서군에 충분한 품질의 모델”은 같은 결론이 아니다. Luna는 비용 민감·대량 처리에 최적화된 tier이므로, table/MDX/admonition/긴 API reference가 섞인 representative fixture에서 completeness·contract success·자연스러움·비용을 표본 평가해야 한다. 현재 검증만으로는 실제 KO/JA 번역 품질을 판정할 수 없다.

### 3.5 외부 공식 자료 대조

- OpenAI: [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [GPT-5.6 모델 지침](https://developers.openai.com/api/docs/guides/latest-model), [Responses API 전환](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- Codex: [non-interactive prompt-plus-stdin](https://learn.chatgpt.com/docs/non-interactive-mode#advanced-stdin-piping)
- Microsoft: [Azure OpenAI API lifecycle](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle), [Azure reasoning model 지원표](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning)
- GitHub: [`GITHUB_TOKEN` workflow trigger 규칙](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow), [workflow dispatch REST API](https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event), [action SHA 고정 보안 지침](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)
- Docusaurus: [Node.js 20 이상 요구사항](https://docusaurus.io/docs/installation#requirements)
- Node.js: [Node 26 release 상태](https://nodejs.org/en/about/previous-releases)
- uv: [`--frozen`과 Python 선택 동작](https://docs.astral.sh/uv/reference/cli/), [Python 3.14 Tier 1 지원](https://docs.astral.sh/uv/reference/policies/python/)

## 4. Finding 요약

| ID | 최초 심각도 | 후속 상태 | 현재 판정 |
|---|---:|---|---|
| F-01 | P0 | 현재 index export가 153 tests 중 import error로 실패하고 문서 번호·내용도 stale | merge blocker |
| F-02 | P1 | 새 live 응답 앞에 strict response contract를 적용하고 negative corpus 추가 | 해결 |
| F-03 | P1 | provider check가 공통 response contract와 final verifier를 함께 사용 | 해결 |
| F-04 | P1 | current version identity를 보존하고 wrong-version negative test 추가 | 해결 |
| F-05 | P2 | named-section reorder와 separator 보존 구현·회귀 테스트 추가 | 해결 |
| F-06 | P2 | 숫자형 option 조기 검증, `ConfigError` 포착과 종료 코드 2 적용 | 핵심 해결, model별 capability는 provider 확인 |
| F-07 | P2 | CLI env allowlist, 임시 cwd, 사용자 설정·도구·hook 차단, prompt-plus-stdin 적용 | 보안 경계 해결, usage 계측은 개선 항목 |
| F-08 | P2 | 생략 허용 충돌 제거, 문장 결합 범위를 같은 Markdown paragraph로 제한 | 충돌 해결, prompt 축소·live eval은 개선 항목 |
| F-09 | P3 | workflow branch는 보호되지만 로컬 실행의 partial write 가능성 유지 | 후속 개선 |
| F-10 | P3 | Node 26 전체 build와 KO/JA inline fragment target 46,626건 통과 | 해결 |
| F-11 | P2 | Azure 예시의 `2025-05-01-preview`는 현행 Azure OpenAI 공식 버전으로 확인되지 않음 | 예시는 placeholder로 수정, API 전략 사용자 결정 필요 |
| F-12 | P3 | deploy workflow의 GitHub action 5개가 이동 가능한 major tag 사용 | 기능 오류 아님, 공급망 정책 사용자 결정 필요 |
| F-13 | P1 | pre/postprocessor의 Markdown context·placeholder·HTML/JSX 경계에서 결정적 손상 재현 | 구체적 무음 손상을 회귀 테스트와 함께 해결 |
| F-14 | P1 | legacy note 정규화가 provider 뒤에 있어 번역된 marker를 놓침 | 현재 산출물 30건은 정리, 생성 시점 문제는 미해결 |
| F-15 | P1 | preprocess/verifier/response contract/site/sidebar가 지원하는 Markdown 문법이 전체 CommonMark/GFM보다 좁음 | 무음 sidebar 삭제는 차단, 나머지 미해결 |
| F-16 | P2 | sidebar filename이 `versions.json`과 별도로 8.x~13.x에 하드코딩됨 | 동적 파생으로 해결 |
| F-17 | P3 | 정각 cron과 direct push가 GitHub 지연·ruleset 외부 조건에 의존 | 운영 결정 필요 |
| F-18 | P2 | 여러 consumer가 `versions.json`의 첫 non-master를 latest stable로 쓰지만 순서·중복을 검증하지 않음 | ordering contract 문서화, 자동 검증 미해결 |

> 아래 상세 Finding은 최초 재현 근거를 보존한다. 각 항목의 현재 상태는 위 표와 항목 첫머리의 "후속 재검증"을 우선한다.

## 5. 상세 Finding

### F-01. staged snapshot이 현재 커밋 가능한 상태가 아니다 — P0

> **후속 재검증:** 현재 index export는 `Ran 153 tests` 뒤 import error 1건으로 실패한다. staged `provider_check.py`가 `sync.response_contract`를 import하지만 이를 export하는 `sync/__init__.py` 변경은 unstaged다. index에는 오래된 `07-error-cases.md`와 `07-local-replay.md`가 함께 들어가고, 최신 `08-error-cases.md`와 갱신된 00 문서는 빠져 있다. 따라서 지금 커밋하면 검증한 워킹 트리와 다른 코드·문서가 만들어진다.

#### 최초 근거 (2026-07-15)

최초 스냅샷의 워킹 트리에서는 260개 테스트가 통과했지만, 당시 `git checkout-index`로 **index만** 임시 저장소에 내보내 실행한 결과는 다음과 같았다.

```text
Ran 241 tests
FAILED (failures=2)

test_translate_one_inserts_structural_section_before_raw_anchor
test_translate_one_repairs_segment_anchors_and_comments

partial patch failed: patched block order does not match the target source
```

또한 당시 다음 파일은 untracked였다.

```text
translation-sync/provider_check.py
translation-sync/tests/test_generated_changes.py
translation-sync/tests/test_provider_check.py
translation-sync/validate_generated_changes.py
```

`MM` 상태인 핵심 파일도 많았다. 즉 워킹 트리에서 검증한 fix와 테스트가 당시 index에는 전부 들어 있지 않았다.

#### 영향

- 지금 `git commit`을 하면 import가 깨진 코드와 중복된 07번 문서가 커밋되고, 최신 08번 역사 문서와 올바른 symlink 설명은 누락된다.
- 일반 `git commit -a`도 untracked 파일을 포함하지 않는다.
- local test success를 commit success로 오인할 수 있다.

#### 권고

1. intended diff를 한 번 정리해 staged/unstaged/untracked 경계를 제거한다.
2. index를 별도 임시 저장소로 export한다.
3. 그 임시 저장소에서 `translation-test`, `translation-replay`, 선택한 Node 버전의 `site-check`를 실행한다.
4. 그 결과만 merge 후보로 본다.

#### 완료 조건

- intended 범위에 unstaged 또는 untracked 변경이 없다.
- staged snapshot에서 최종 워킹 트리와 같은 전체 테스트가 모두 통과한다.
- staged snapshot의 전체 identity replay가 두 번째 pass no-op으로 끝난다.
- untracked provider/artifact checker와 해당 테스트가 최종 commit에 포함된다.

### F-02. verifier가 번역 본문 cardinality와 ownership을 검증하지 않는다 — P1

> **후속 재검증:** 운영 live 응답 경로는 해결됐다. `response_contract.py`가 provider 결과를 적용하기 전에 순서·occurrence·owned body·영어 echo·extra prose·목표 언어·Markdown 구조를 검사하고, main/provider check가 이를 공유한다. 기존 locale와 identity replay에 쓰는 final verifier는 호환성을 위해 더 관대하지만, 새 provider 응답이 이 strict 경계를 우회하지 않는다.

#### 최초 근거 (2026-07-15)

`sync/verification/verify.py`의 `_required_comments`와 `_translated_comments`는 모두 `set[str]`를 사용한다. 이 때문에 동일한 원문 문단이 두 번 나타나도 occurrence가 하나로 축약된다. `verify()`는 필요한 주석이 집합에 존재하는지만 보고, 각 주석 뒤에 실제 번역 본문이 하나씩 있는지 또는 주석 밖의 prose가 어디서 왔는지 확인하지 않는다.

현재 코드에서 다음 입력은 모두 성공을 의미하는 `[]`를 반환했다.

| 반례 | 실제 문제 | `verify()` |
|---|---|---:|
| 영어 주석만 있고 본문 없음 | 번역 누락 | `[]` |
| 영어 주석 뒤에 원문 영어를 그대로 출력 | 번역 미수행 | `[]` |
| 동일 source 문단 2개, output occurrence 1개 | 중복 문단 누락 | `[]` |
| 정상 block 뒤에 원문에 없는 한국어 문장 추가 | provider hallucination/wrapper | `[]` |

`translation-sync/docs/04-verification.md`도 이 한계를 일부 명시한다. 문제는 workflow가 사람 검토 없이 결과를 branch에 직접 커밋하므로, 알려진 한계가 운영상 P1 gate 공백이 된다는 점이다.

#### 영향

- 구조·링크·코드가 멀쩡하면 내용이 비어 있거나 영어여도 자동 커밋될 수 있다.
- duplicate source가 많은 API reference에서 한 occurrence가 사라져도 검출하지 못한다.
- provider의 사과문, 요약, 추가 설명이 구조를 건드리지 않으면 남을 수 있다.
- replay는 identity provider이므로 이 문제의 실제 번역 품질을 증명하지 않는다.

#### 권고

별도의 **response contract parser**를 만들고 final verifier도 같은 모델을 사용한다.

1. source를 순서가 있는 annotatable block 목록으로 만든다.
2. 각 block에 normalized source와 occurrence index를 부여한다.
3. output을 `source comment -> 정확히 하나의 owned body` 단위로 파싱한다.
4. source와 output의 block 수·순서·occurrence가 정확히 같은지 비교한다.
5. anchor, code, table, bare link list처럼 번역 소유가 아닌 구조 block만 명시적으로 예외 처리한다.
6. 파싱된 block 밖의 비공백 prose는 거부한다.
7. body가 비어 있거나 normalized source와 동일한 영어 echo면 거부한다.

의미 품질 전체를 정규식으로 판정하려 하면 오탐이 커진다. 우선 deterministic하게 확인 가능한 **본문 존재, exact English echo, block cardinality, extra prose ownership**을 강제하고, 자연스러움과 의미 정확성은 별도의 live eval/human sample로 다루는 편이 안전하다.

#### 필수 회귀 테스트

- missing body
- exact English echo
- duplicate source의 첫 번째/두 번째 occurrence 각각 누락
- prefix/suffix/middle extra prose
- 정상적인 다문장 번역 body
- table, admonition, list, blockquote, raw HTML, code 사이의 ownership
- KO/JA 모두에서 영어 기술 용어가 많은 정상 번역

### F-03. live-provider gate가 실제 계약 위반을 정상 처리한다 — P1

> **후속 재검증:** 해결됐다. provider check는 공통 response contract와 final verifier를 모두 호출하며 KO/JA의 missing body, English echo, 목표 문자 부족, duplicate omission, prefix/middle/suffix extra prose와 주요 Markdown 구조 negative fixture를 거부한다.

#### 최초 근거 (2026-07-15)

현재 `provider_check.py`는 fixture의 anchor, heading comment, heading, paragraph comment, code block, 응답 끝을 확인하도록 보강되어 있다. suffix wrapper는 이제 정상적으로 거부한다.

그러나 paragraph body는 한 줄 이상이라는 것만 확인하고, 응답 전체에서 locale 문자 한 글자만 찾는다. 다음 결과를 재현했다.

| fixture output | `evaluate_output("ko", ...)` |
|---|---:|
| 정상 KO output | `[]` |
| 원문에 없는 한국어 설명 한 줄 추가 | `[]` |
| 본문은 원문 영어 그대로이고 끝에 `한` 한 글자만 추가 | `[]` |
| 정상 output 뒤 `Translation complete.` 추가 | `unexpected provider response shape` |

즉 wrapper 끝 검사는 개선되었지만, gate가 가장 중요한 “실제로 번역했는가”를 보장하지 못한다.

#### 영향

- live provider의 prompt adherence가 깨져도 workflow가 번역 본 단계로 진행한다.
- 고정 fixture 한 건의 통과를 전체 문서·모든 block 종류의 계약 보장으로 오인할 수 있다.
- F-02의 약한 verifier를 다시 호출하므로 두 gate가 같은 blind spot을 공유한다.

#### 권고

- F-02의 response contract parser를 `provider_check`와 production verifier가 공유한다.
- provider check만의 ad-hoc shape parser를 장기적으로 제거한다.
- positive fixture 1개가 아니라 작은 contract corpus를 둔다.

최소 corpus는 다음을 포함해야 한다.

- 단일 prose
- duplicate prose
- heading + named anchor
- list와 nested list
- table
- admonition/blockquote
- fenced code와 inline code
- internal/absolute/versioned link
- raw HTML/MDX
- wrapper, English echo, missing body, extra prose의 negative fixture

실제 provider gate에서는 각 locale별 corpus 성공률, retry, latency, input/cached/output token을 기록해야 한다. 매 실행 전체 corpus가 비싸다면 짧은 deterministic fixture는 매번 실행하고, 확대 corpus는 prompt/model 변경 때 필수로 실행할 수 있다.

### F-04. link version 정규화가 의미 오류를 숨긴다 — P1

> **후속 재검증:** 해결됐다. current document version을 정규화에 전달하고, 표현만 다른 같은-version 링크는 허용하되 13.x → 12.x와 master ↔ version 변경은 거부하는 테스트를 추가했다.

#### 최초 근거 (2026-07-15)

`verify.py`의 `_normalize_link_target`은 `/docs/<version>/`와 `https://laravel.com/docs/<version>/` prefix를 제거한다. 표현 방식이 다른 동일 문서 링크를 비교하기 위한 의도는 타당하지만, version까지 버린다.

다음 변경은 현재 `verify()`에서 `[]`다.

```text
source:     /docs/13.x/guide
translated: /docs/12.x/guide
```

absolute Laravel URL의 13.x → 12.x 변경도 같은 이유로 통과한다.

#### 영향

- 13.x 문서가 오래된 12.x 설명으로 연결되어도 자동 검증이 성공한다.
- 12.x target 문서가 실제 존재하면 site build와 rendered-link 검증도 성공할 수 있다.
- 구조 검증과 사이트 검증을 모두 통과한 의미 오류가 된다.

#### 권고

link canonicalization에 source document context와 expected version을 전달한다.

- 같은 문서 문맥에서 `guide`, `./guide`, `/docs/13.x/guide`, Laravel 13.x absolute URL은 동등하게 볼 수 있다.
- `/docs/12.x/guide`는 13.x와 동등하게 보지 않는다.
- `master`도 별도 version identity로 유지한다.
- stale-link alias와 excluded-link 목록은 각각 왜 필요한지 fixture와 만료 조건을 둔다.

#### 완료 조건

- representation만 다른 같은-version 링크는 통과한다.
- 13.x ↔ 12.x, version ↔ master 변경은 실패한다.
- fragment-only, relative, absolute, external scheme, image link가 모두 context-aware test를 가진다.

### F-05. patch engine의 유효 transition coverage가 아직 불완전하다 — P2

> **후속 재검증:** 재현했던 두 사례는 해결됐다. 유일한 named section 재정렬을 명시적으로 처리하고 moved source comment ownership과 source separator를 보존하는 회귀 테스트를 추가했다. 교차된 annotation ownership처럼 모호한 이동은 계속 fail-closed한다.

#### 사례 A: named-anchor section 이동

다음처럼 두 section의 순서만 바꾸는 정상 source 변경을 재현했다.

```text
old: alpha section -> beta section
new: beta section -> alpha section
```

결과:

```text
PatchError: patched block order does not match the target source
```

문서를 잘못 쓰지 않고 실패하는 점은 안전하다. 그러나 `translation-sync/docs/02-translation.md`가 변경 유형으로 “이동”을 분류하고 있고, 실제 Laravel 문서에서 section 재배치는 가능한 변경이므로 자동 sync 가용성 공백이다.

#### 사례 B: 문서 맨 앞 prose 삽입과 raw anchor 사이 공백

source:

```markdown
Paragraph 99.

<a name="section-1"></a>
## Section 1
```

identity patch 결과:

```markdown
<!-- Paragraph 99. -->
Paragraph 99.
<a name="section-1"></a>
<!-- ## Section 1 -->
## Section 1
```

source의 빈 줄 하나가 사라졌지만 `verify()`는 `[]`였다. 현재 Docusaurus가 이 fixture를 렌더할 가능성은 높지만, prompt가 요구하는 blank-line/Markdown 구조 보존과는 다르고 parser가 달라지면 AST가 달라질 수 있다.

#### 권고

- section move를 명시적 operation으로 구현하거나, 해당 operation만 isolated full-document regeneration fallback으로 보낸다.
- fallback도 같은 strict contract와 full-document verification을 통과해야 하며 기존 checkout에 직접 쓰지 않는다.
- `strip_annotations(identity_result)`와 normalized latest source가 정확히 같아야 하는 differential property를 추가한다.
- whitespace 차이를 무조건 무시하지 말고 fenced code 밖의 block separator는 source와 동일하게 검증한다.
- 실제 Laravel upstream의 과거 commit에서 paragraph split/merge, duplicate, section move, anchor rename, table/admonition/code 이동 fixture corpus를 만든다.

`patch.py`를 한 번에 다시 쓰는 것은 권하지 않는다. 2026-07-15 최초 검토 당시 2,480줄의 patch logic과 1,550줄의 test 자산을 유지하면서 operation별 pure seam과 differential test를 추가하는 편이 위험이 낮다고 판단했다.

### F-06. config boundary가 형식 오류를 막지 않는다 — P2

> **후속 재검증:** 핵심 오류는 해결됐다. retry delay는 0 이상 정수, CLI timeout은 양의 정수로 config 단계에서 검사하고, `main()`은 `ConfigError`를 짧은 메시지와 종료 코드 2로 처리한다. deployment/model/API version의 실제 지원 여부는 외부 provider에 종속되므로 adapter/live check 경계에 남긴다.

#### 최초 근거 (2026-07-15)

`load_config()`의 docstring과 `ConfigError`는 누락·형식·provider 조합 오류를 config 단계에서 처리한다고 설명한다. 실제로는 optional 값을 trim한 문자열로만 저장한다.

```text
TRANSLATION_RETRY_DELAY=not-an-integer
```

위 설정은 `load_config()`를 통과하고 첫 provider 호출 직전 `_with_retries()`의 `int(...)`에서 다음 raw error를 낸다.

```text
ValueError: invalid literal for int() with base 10: 'not-an-integer'
```

`TRANSLATION_CLI_TIMEOUT`도 같은 늦은 conversion 구조다. 또한 `main.py`의 일반 실행은 `config.load_config()`를 catch하지 않아 잘못된 provider 설정이 concise diagnostic이 아니라 traceback으로 끝날 수 있다. 이 시점에는 upstream sync가 이미 수행된 뒤다.

#### 권고

- `load_config()`에서 `TRANSLATION_RETRY_DELAY`를 0 이상 정수로 검증한다.
- `TRANSLATION_CLI_TIMEOUT`은 양의 정수로 검증한다.
- reasoning effort는 선택한 provider/model이 지원하는 값으로 검증한다. GPT-5.6 기준 공식 값은 `none`, `low`, `medium`, `high`, `xhigh`, `max`다.
- endpoint/API version/model capability처럼 provider별 제약은 adapter boundary에 명시한다.
- `main()`은 `ConfigError`를 catch해 비밀값 없이 한 줄 diagnostic과 고정 exit code를 반환한다.
- config 검증은 upstream write보다 먼저 할 수 있는 부분을 먼저 수행한다.

### F-07. API와 Codex CLI adapter는 동등한 번역 surface가 아니다 — P2

> **후속 재검증:** 보안·입력 경계는 해결됐다. CLI는 locale instruction을 prompt argument로, structured request를 stdin `<stdin>` context로 전달한다. 전용 임시 cwd, env allowlist, 빈 subprocess env 상속, 사용자 config/rules/AGENTS 제외와 불필요한 feature·hook·web 차단을 적용했다. 이 prompt-plus-stdin 형태와 모든 현재 플래그는 공식 문서와 `codex-cli 0.144.5`의 실제 옵션 파싱으로 확인했다. API/CLI usage telemetry와 실제 품질 비교만 개선 항목으로 남는다.

#### 최초 확인된 차이 (2026-07-15)

| 항목 | OpenAI API | Azure adapter | Codex CLI |
|---|---|---|---|
| 호출 | Responses API | Chat Completions | `codex exec` agent |
| 운영 prompt 역할 | `instructions` system-level | `system` message | 당시 stdin 전체가 초기 Codex prompt |
| source 역할 | `input` | `user` message | 당시 locale prompt와 source가 같은 payload |
| 도구 | 코드가 tools를 전달하지 않음 | 없음 | Codex agent tool surface 존재 |
| sandbox | 해당 없음 | 해당 없음 | model-generated command가 read-only |
| 세션 | 요청 1회 | 요청 1회 | block마다 새 `--ephemeral` process |
| 결과 | `output_text` | first choice content | `--output-last-message` file |
| usage 계측 | 응답 usage 사용 가능 | 응답 usage 사용 가능 | 현재 final message만 읽어 미수집 |

OpenAI 공식 문서는 Responses의 `instructions`를 system-level guidance로 설명한다. 반면 Codex 공식 non-interactive 문서는 `codex exec -`에서 stdin이 전체 prompt가 된다고 설명한다. `read-only`는 model-generated command의 쓰기를 제한하지만 tool 호출 자체를 제거하는 옵션이 아니다.

- [Responses API roles and benefits](https://developers.openai.com/api/docs/guides/migrate-to-responses#responses-benefits)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)

따라서 당시 CLI 경로를 API와 동일한 prompt role 또는 동일 token behavior로 간주하면 안 됐다. 현재 구현은 prompt argument와 stdin context를 분리했지만 API와 CLI의 전체 system context·token behavior까지 같아지는 것은 아니다.

#### 최초 환경 상속 (2026-07-15)

당시 CLI의 `subprocess.run(...)`에는 `env`가 없어서 자식 Codex process가 parent의 전체 환경을 상속했다. 빈 임시 디렉터리, user config/rules 무시, `project_doc_max_bytes=0`, read-only만으로는 다음을 막지 못했다.

- 자식 process가 불필요한 환경 변수 이름/값을 보는 것
- read-only tool로 host의 읽기 가능한 파일을 조사하는 것
- 외부 source text가 agent instruction처럼 해석되는 것
- 기본 제공 cached web search 같은 불필요한 agent capability 사용

운영 workflow는 현재 API/Azure를 전제로 보이므로 직접 위험은 주로 local CLI adapter에 있다. 그래도 adapter contract에는 최소 환경을 명시해야 한다.

#### token behavior

현재 구현으로는 API와 CLI의 token 비용을 확실히 비교할 수 없다.

- KO prompt: 13,899 bytes / 219 lines
- JA prompt: 28,205 bytes / 388 lines
- 각 changed block 또는 added-document chunk마다 locale prompt를 다시 보낸다.
- API는 prompt caching 효과가 있을 수 있지만 현재 usage를 기록하지 않는다.
- CLI에는 Codex의 system/developer context와 tool schema overhead가 추가되지만 현재 `--json` usage event를 수집하지 않는다.

Luna의 max input은 충분히 크므로 현재 prompt 크기는 capacity 문제가 아니다. 문제는 반복 비용, latency, instruction 집중도이며 이는 실측해야 한다.

#### 권고

1. **운영 기준은 direct API adapter로 둔다.** CLI는 local parity/eval adapter로 정의한다.
2. CLI를 유지하면 locale instruction을 prompt argument로, source를 stdin context로 넘기는 공식 prompt-plus-stdin 형태를 유지한다. 당시처럼 모든 내용을 `-`의 한 prompt로 합치는 것보다 instruction/data 경계가 분명하다.
3. pure translation에 필요 없는 web search/tool capability를 명시적으로 끈다.
4. CLI child env를 allowlist로 만든다. 예: 실행에 필요한 `PATH`, locale/temp, 명시한 Codex auth home만 전달하고 임의 application secret은 전달하지 않는다.
5. API `response.usage`와 별도 CLI eval의 `--json` `turn.completed.usage`를 수집해 input, cached input, output, reasoning, latency, retry를 비교한다.
6. API/CLI는 exact wording이 아니라 F-02의 동일 structural/content contract와 human-reviewed quality rubric으로 비교한다.

#### 최초 live 실행 제한 (2026-07-15)

설치된 `codex-cli 0.144.4`는 현재 사용한 flags를 지원했다. 실제 `gpt-5.6-luna` provider check도 시도했지만 이 리뷰 세션 안의 nested Codex 실행이 다음 환경 오류로 model 응답 전에 종료됐다.

```text
failed to initialize in-process app-server client: Operation not permitted
```

API key는 환경에 없었고 금지된 `.env`는 읽지 않았다. 따라서 이 결과는 prompt/model 결함 증거가 아니라 리뷰 환경 제한이다. **실제 Luna KO/JA 출력 품질은 아직 검증되지 않았다.**

### F-08. prompt 규칙을 더 짧고 모순 없이 만들어야 한다 — P2

> **후속 재검증:** 확인된 규칙 충돌은 해결됐다. 일본어 prompt의 `As you can see` 생략 허용을 제거하고, 문장 분할·결합은 같은 Markdown paragraph 안에서만 허용하며 누락·추가 금지를 우선한다. prompt 크기 축소는 공식 GPT-5.6 지침상 평가 가치가 있지만, 결과를 바꿀 수 있으므로 live corpus 없이 기계적으로 줄이지 않았다.

#### 최초 확인된 충돌 (2026-07-15)

일본어 prompt는 앞부분에서 다음을 강제한다.

- 임의 생략·요약·재배치·앞뒤 문구 추가 금지
- 원문의 줄바꿈·빈 줄 유지
- 영어 주석을 제외한 Markdown AST 동일

그러나 뒷부분에서는 다음을 허용한다.

- `As you can see,`를 생략할 수 있음
- 문장을 적극적으로 분할·결합할 수 있음
- Laravel의 가벼운 표현을 문맥상 불필요하면 약하게 처리할 수 있음

자연스러운 일본어 문장 안에서 문장부호를 나누는 것과 Markdown paragraph/block을 나누는 것은 다른데 현재 문구는 이를 구분하지 않는다. “AST 동일”도 text node 내용은 번역으로 달라지므로 정확한 표현이 아니다.

한국어 prompt는 더 짧고 규칙 우선순위가 명시되어 있지만, 일본어 prompt는 약 두 배 크고 glossary/style 예시가 hard contract와 한 파일에 섞여 있다.

#### 영향

- provider가 생략을 스타일 개선으로 정당화할 수 있다.
- API/CLI 또는 prompt 위치에 따라 서로 다른 규칙을 우선할 수 있다.
- 큰 공통 prefix를 block마다 반복해 비용과 latency를 늘린다.
- verifier가 의미 누락을 못 잡는 F-02와 결합하면 prompt 모순이 그대로 문서에 들어갈 수 있다.

#### 권고 prompt 구조

다음 세 층으로 단순화한다.

1. **공통 hard contract**
   - source 범위만 출력
   - 누락·추가·요약 금지
   - block 순서와 Markdown 구조 보존
   - link label/target, heading, anchor, code, inline code 보존
   - required English comments와 output-only 규칙
2. **locale style**
   - KO/JA 자연스러운 문체
   - sentence split/merge는 같은 Markdown paragraph 안에서만 허용
   - 담화 표현도 의미를 삭제하지 않고 자연스럽게 번역
3. **locale glossary**
   - 실제로 반복되는 용어만 유지
   - hard contract와 충돌할 수 없음

“Markdown AST 동일” 대신 verifier가 실제 비교하는 structural signature를 정확히 열거하는 편이 낫다. prompt 맨 앞과 마지막에 서로 다른 규칙을 반복하기보다, 한 번의 우선순위와 짧은 final checklist를 둔다.

#### prompt 완료 조건

- KO/JA hard contract의 의미가 동일하다.
- “생략 금지”와 충돌하는 예시가 없다.
- sentence-level 자연스러움과 Markdown block preservation이 구분된다.
- prompt/model 변경 때 실제 historical fixture corpus를 KO/JA/API/CLI로 실행한다.
- human reviewer가 completeness, terminology, naturalness, structure를 표본 평가한다.
- prompt hash뿐 아니라 eval corpus version과 결과도 남긴다.

### F-09. 전체 실행이 하나의 transaction이 아니다 — P3

> **후속 재검증:** 남아 있는 후속 개선이다. workflow는 어떤 gate라도 실패하면 commit하지 않아 원격 branch는 보호하지만, 로컬 직접 실행은 앞서 성공한 문서가 남을 수 있다. 현재 테스트에서 잘못된 commit은 재현되지 않았으므로 release blocker가 아니라 운영 복구성 문제로 분류한다.

#### 현재 근거

`main.py`는 각 locale/document가 검증되면 destination에 즉시 `write_text`한다. 이후 다른 locale, 다른 문서, sidebar, site build가 실패할 수 있다.

workflow runner에서는 실패 결과를 커밋하지 않으므로 branch는 보호된다. 그러나 로컬 실행에는 앞에서 성공한 파일만 남고, process crash 시 한 파일 write도 원자적이라고 보장되지 않는다.

#### 권고

replay가 이미 가진 격리 worktree 패턴을 live run의 transaction boundary로 승격하는 방안을 권한다.

```text
pinned source
  -> pure PatchPlan
  -> provider output
  -> strict response parsing
  -> isolated candidate worktree
  -> full verify + sidebar + site + artifact scope
  -> 성공 시에만 promotion/commit
```

한 번에 큰 rewrite를 할 필요는 없다. 먼저 document 단위 temp file + atomic replace를 적용하고, 다음 단계에서 workflow 전체를 isolated candidate로 만들 수 있다.

### F-10. Node 지원 범위가 실제 build 결과보다 넓다 — P3

#### 최초 근거 (2026-07-15)

- `.nvmrc`: Node 24
- GitHub Actions: Node 24
- `package.json`: `node >=24`
- README: Node 24 이상

로컬 Node `v26.4.0`에서 `make site-check`를 실행하면 Markdown-link test와 typecheck는 통과하지만 Docusaurus build가 KO 13.x의 6개 route output을 찾지 못해 실패했다. 같은 checkout을 Node `v24.18.0`으로 실행하면 KO/JA build와 23,313개 anchor 검증이 모두 통과했다.

실패 route:

- notifications
- octane
- packages
- pagination
- passport
- passwords

#### 최초 권고

Node 26을 실제 지원할 때까지 `24.x` 또는 `>=24 <25`로 계약을 좁힌다. 또는 Node 26 build 실패의 Docusaurus 원인을 별도 조사하고 지원 matrix test를 추가한다. workflow는 이미 Node 24로 고정되어 있으므로 운영 blocker는 아니다.

#### 후속 대응 — 해결

사용자 결정에 따라 런타임 기준을 Node 26으로 통일했다. `.nvmrc`, `package.json`/`package-lock.json` 엔진, Dockerfile, Make 초기화 이미지, deploy/sync workflow와 README를 모두 Node 26으로 맞췄다. Docusaurus 3.10.1은 공식 요구사항과 package engine이 모두 Node 20 이상이므로 별도 의존성 업그레이드는 적용하지 않았다.

현재 checkout에서 Node `v26.4.0`으로 KO 단일 build, KO/JA 전체 build, `docusaurus clear` 이후 clean KO/JA build를 각각 실행했으며 모두 통과했다. 잠금 파일 기반 `npm ci` 후 `make site-check`도 통과했고 KO/JA inline Markdown fragment target은 **46,626 / 46,626 OK**였다. Docker `node:26-alpine` 태그는 Node `v26.5.0`으로 실행됨을 확인했다. 따라서 초기 리뷰에서 관찰한 6개 route 누락은 현재 상태에서 재현되지 않으며 F-10은 해결된 것으로 갱신한다.

### F-11. Azure API version과 adapter 전략을 deployment 기준으로 확정해야 한다 — P2

#### 근거

README와 workflow 요약은 Azure 예시를 `AZURE_OPENAI_API_VERSION=2025-05-01-preview`로 고정하고 있었다. 그러나 Microsoft의 현행 Azure OpenAI inference 문서는 legacy 날짜형 data-plane API의 마지막 preview를 `2025-04-01-preview`로 설명하고, 2025년 8월 이후에는 월별 `api-version` 교체가 필요 없는 v1 API 사용을 권장한다. `2025-05-01-preview`는 다른 Azure AI 서비스에는 존재하지만, 현재 Azure OpenAI inference 공식 버전으로 확인되지 않았다.

한편 현재 adapter는 `AzureOpenAI(..., api_version=..., azure_endpoint=...)`와 deployment 이름을 사용하는 legacy 형태다. Azure 공식 지원표상 `gpt-5.6-luna`의 Chat Completions와 `reasoning_effort` 자체는 지원되지만, 실제 deployment·region·endpoint가 어떤 API surface를 허용하는지는 credential이 있는 환경에서만 확인할 수 있다.

- [Azure OpenAI API version lifecycle](https://learn.microsoft.com/en-us/azure/foundry/openai/api-version-lifecycle)
- [Azure OpenAI reasoning model support](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning)

#### 적용한 수정

잘못된 특정 버전을 권장하지 않도록 README와 workflow 요약의 값을 `your_deployment_api_version` placeholder로 바꿨다. 코드의 호출 surface는 운영 deployment 정보 없이 임의로 바꾸지 않았다.

#### 사용자 결정이 필요한 선택지

1. OpenAI Responses adapter만 운영하고 Azure를 비활성 경로로 둘 수 있다.
2. Azure legacy adapter를 유지한다면 실제 deployment가 지원하는 날짜형 API version을 secret에 넣고 KO/JA provider check를 실행한다.
3. 장기 운영에서 Azure를 주 provider로 쓴다면 v1 API와 Responses adapter로 통합하는 별도 migration을 설계하고, 현재 Chat Completions 결과와 회귀 비교한다.

완료 기준은 선택한 Azure 경로에서 KO/JA provider check, 대표 문서 1건, retry/error 분류와 `finish_reason`/response contract가 모두 통과하는 것이다.

### F-12. deploy workflow action도 full commit SHA로 고정할지 결정해야 한다 — P3

translation sync workflow의 `checkout`, `setup-uv`, `setup-node`는 full commit SHA로 고정되어 있다. 반면 deploy workflow는 `actions/checkout@v7`, `actions/setup-node@v6`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`처럼 이동 가능한 major tag를 사용한다.

현재 기능 실패나 악성 변경을 관찰한 것은 아니다. 다만 GitHub 공식 보안 지침은 full commit SHA만 immutable release라고 설명하며, repository 정책으로 GitHub 공식 action까지 SHA 고정을 강제할 수 있다. Pages deploy job은 `pages: write`와 `id-token: write` 권한이 있으므로 sync workflow와 같은 공급망 기준을 적용할 이유가 있다.

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)

이는 자동으로 최신 patch를 받는 major tag의 편의성과 검토한 코드만 실행하는 immutable pin 사이의 정책 선택이다. SHA 고정을 선택한다면 각 tag가 가리키는 공식 repository commit을 확인해 주석으로 release tag를 남기고, Dependabot으로 갱신하는 방식을 권장한다.

### F-13. 정규화기가 Markdown context와 literal을 손상시키는 결정적 오류가 있었다 — P1

> **후속 재검증:** 아래 재현은 모두 최소 수정과 회귀 테스트로 해결했다. 지원 문법 전체를 새 parser로 교체하지 않고, 손상시키던 구체적 경계만 보수적으로 고쳤다.

#### 재현된 오류

| 입력 | 이전 결과 | 위험 |
|---|---|---|
| outer fenced code 안의 literal `> [!NOTE]` | closing fence와 뒤 빈 줄에 `>`를 추가 | 문서 예제 손상, source 기준본도 같은 방식으로 손상되어 final verifier 통과 가능 |
| outer fence 안의 같은 길이 ```` ```php ```` | info suffix가 있는 opening을 closing으로 오인 | 뒤 alert·image·prose까지 일반 본문으로 변조하고 verifier도 통과 |
| `> **Note:** body` | `note:`로 파싱해 변환하지 않고 verifier도 놓침 | legacy marker 무음 잔존 |
| `<img alt="1 > 0">` | 따옴표 안의 첫 `>`를 tag 끝으로 오인 | malformed HTML 생성, verifier도 self-closing tag를 오탐 |
| `<img hidden={count > 0} />` | JSX expression 안의 `>`에서 tag를 잘라 `<img hidden={count/> 0} />` 생성 | 이미 유효한 image를 손상하고 verifier도 통과 |
| `# Stable {#stable-anchor}` | `{#stable-anchor}` 삭제 | Docusaurus의 명시적 stable heading ID 손실 |
| ``Use ``<style>`` literally`` / `<stylesheet>` | inline literal 삭제 / 문서 절단 | 정상 prose 손상 |
| 닫히지 않은 top-level `<style>` | 해당 지점부터 EOF까지 삭제 | 후속 본문 전체 무음 손실 |
| 일반 list item의 4-space continuation | top-level fenced code로 변환 | 목록 구조 손상 |
| 원문 literal `__BASE64_IMAGE_001__`와 첫 이미지 | literal까지 data URI로 전역 복원 | 정상 prose 변조, expected source도 같이 변조되어 검출 불가 |

Docusaurus는 `{#id}`를 stable explicit heading ID로 지원하며, GitHub의 해당 blockquote 문법 공식 명칭은 Markdown alert다.

- [Docusaurus explicit heading IDs](https://docusaurus.io/docs/markdown-features/toc)
- [GitHub Markdown alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts)

#### 적용한 수정

- 일반 fence 상태를 추적하고 closing fence 뒤에는 공백만 허용해 outer fence 안의 alert와 info-string fence 예제를 byte-equivalent하게 보존한다.
- bold 내부 colon, quoted HTML attribute와 balanced JSX expression의 `>`, legacy marker 검사를 같은 canonicalization 의미로 맞춘다.
- 제목 attribute list에서 class만 제거하고 explicit ID는 보존한다.
- 실제 standalone `<style>` tag boundary만 제거 대상으로 보고 inline/multi-backtick 예제와 `<stylesheet>`는 보존하며, 종료 tag가 없으면 remainder 전체를 유지한다.
- list parent 아래의 code-looking continuation은 애매한 구조로 보고 변환하지 않는다.
- 원문에 이미 존재하는 base64 sentinel 번호는 건너뛰어 잘못 복원하지 않는다. literal sentinel namespace 자체는 예약어로 명시 실패한다.
- NOTE/TIP/WARNING/CAUTION/IMPORTANT outer-fence fixture, closing suffix, HTML/JSX 경계, heading ID, unclosed style, list와 placeholder collision 회귀 테스트를 추가했다.

여러 줄 code span, inline code 안의 `<img>`, HTML comment/raw `<code>` 안의 `<style>`, 1~3칸 들여쓴 legacy blockquote와 완전한 CommonMark list container 판정은 이 국소 수정의 해결 범위가 아니며 F-15에 남긴다.

### F-14. legacy note canonicalization이 provider 뒤에 있어 번역된 marker를 놓친다 — P1

현재 영어 legacy marker 표준화는 provider 응답을 받은 뒤 `postprocess.py`에서 실행한다. provider가 marker 자체를 번역해 `> **참고:**`, `> **注:**`, `> **注意:**`로 반환하면 영어 `_NOTE_TYPES`와 final verifier의 영어 legacy pattern은 이를 인식하지 못한다.

완료 감사의 전체 `--check-annotations`는 KO 12.x·13.x `ai-sdk.md`의 영어 legacy marker 2건을 실제 실패로 검출했다. 동시에 같은 문서군에는 verifier가 놓치는 지역화 marker 28건이 있었다. 13.x 한 건은 marker뿐 아니라 note 본문 전체가 영어로 남아 있었다.

현재 산출물의 30건은 모두 canonical `[!NOTE]`로 정리했고 영어 본문 1건을 한국어로 번역했다. 이후 전체 annotation check는 통과하며 legacy bold marker scan 결과도 0건이다. 그러나 이는 현재 산출물 migration일 뿐 새 provider 응답에서 같은 형식이 다시 생기는 원인을 막지는 않는다.

이는 F-13의 `> **Note:**` parser fix와 다른 처리 시점 문제다. 영어 source의 legacy marker를 provider 호출 **전에** canonical GitHub Markdown alert로 바꾸고, provider에는 marker를 번역 불가 구조로 전달해야 한다. postprocess의 영어 fallback은 과거 입력 호환을 위해 유지할 수 있다.

자동 커밋에서 비표준 note 형식을 허용하지 않는 것이 목표라면 이 항목은 운영 투입 전 닫아야 한다. 반대로 과거 localized blockquote를 호환 형식으로 허용한다면 03·04 문서와 verifier 계약을 그에 맞게 명시적으로 완화해야 한다.

### F-15. Markdown parser와 site gate가 지원하는 문법 범위가 제한적이다 — P1

여러 경계가 전체 CommonMark/GFM이 아니라 구현된 subset만 검사한다. 특히 첫 번째 항목은 유효한 원문을 무음 손상시키므로 P1이다.

1. preprocess의 standalone `<style>` 경계 보강은 같은 줄의 inline/multi-backtick 예제를 보존하지만 CommonMark의 **여러 줄 code span** 상태는 추적하지 않는다. `Use ``\n<style>...`처럼 backtick run 사이의 다음 줄이 `<style>`로 시작하면 style block과 내용이 삭제되고, expected source에도 같은 손상이 적용돼 final verifier가 놓친다. HTML comment나 raw `<code>` 안의 standalone `<style>`도 같은 문맥 한계가 있다.
2. `verify.py`와 `response_contract.py`의 inline-code 정규식은 single-line content만 모델링하고 delimiter run을 보존하지 않는다. 예를 들어 source의 ```` ``foo`` ````를 output의 `` `foo` ``로 바꿔도 두 검사가 모두 `[]`를 반환한다. inline span 안의 `<img>`도 후처리 대상이 될 수 있다. CommonMark code span delimiter는 하나 이상의 같은 backtick run이며 line ending도 허용한다.
3. 공통 inline-link parser는 balanced target과 double-quoted title만 지원한다. 유효한 `[x](foo 'title')`와 `[x](foo (title))`의 target을 `bar`로 바꾼 응답도 `response_contract.verify()`와 final `verify()`가 모두 `[]`를 반환한다.
4. legacy alert parser와 verifier는 column 0의 영어 type만 대상으로 하므로 CommonMark가 허용하는 1~3칸 들여쓴 `> **Note:**`와 지역화 marker를 놓친다. 지역화 marker의 근본 생성 문제는 F-14와 연결된다.
5. `validate-anchors.mjs`는 KO/JA의 inline Markdown link 중 fragment가 있는 target만 검사한다. fragment 없는 route, reference-style link, HTML `href`는 제외되며, multi-backtick code span을 완전히 mask하지 못해 그 안의 가짜 link를 검사 대상으로 오인할 수 있다. Docusaurus 설정도 broken link를 `warn`, broken anchor를 `ignore`로 둔다. 05 문서의 표현은 실제 범위로 좁혀 수정했다.
6. sidebar 정규식은 optional title과 target 내부 중첩 괄호가 있는 유효한 link를 파싱하지 못한다. 이번 수정으로 이런 `- [` 줄을 조용히 누락·삭제하지 않고 fail-closed issue로 바꿨지만, 유효 문법 자체는 아직 지원하지 않는다.
7. list parent 탐색은 손상을 피하도록 보수적으로 유지했지만 전체 CommonMark container/marker-width 문법을 판정하지 않는다. 애매한 입력을 보존한다는 안전 계약은 지키지만 모든 indented code를 자동 변환한다고 볼 수 없다.

- [CommonMark code spans](https://spec.commonmark.org/0.31.2/#code-spans)
- [CommonMark links](https://spec.commonmark.org/0.31.2/#links)

권고는 각 정규식을 독립적으로 늘리는 것이 아니라 이미 공통화된 Markdown scanner에 delimiter run과 span, link destination/title을 추가하고 preprocess·response contract·final verifier·sidebar가 같은 parser를 재사용하는 것이다. site gate는 검사 범위를 현재처럼 명시적으로 제한하거나, reference/HTML link까지 포함하는 renderer 기반 graph 검사로 확장해야 한다.

### F-16. sidebar version filename이 `versions.json`과 별도로 하드코딩돼 있었다 — P2

`06-sidebar-sync.md`는 `version-<version>` 패턴과 `versions.json`을 단일 version 기준으로 설명하지만, generator는 `master`, 8.x~13.x filename을 세 곳에서 열거했다. `versions.json`에 `14.x`를 추가한 fixture는 `unsupported sidebar version: 14.x`로 실패했다.

검증된 `VERSION_RE` token에서 source/locale filename을 직접 파생하고 `_write_sidebar()`도 같은 helper를 사용하도록 수정했다. `14.x` future-version 회귀 테스트가 실제 sidebar 파일 생성을 확인한다. Docusaurus도 version 이름에서 `version-[versionName]-sidebars.json`을 파생한다.

- [Docusaurus versioning file structure](https://docusaurus.io/docs/versioning)

이 항목은 해결됐다.

### F-17. schedule과 direct push는 저장소 밖 GitHub 운영 조건에 의존한다 — P3

sync cron은 `0 13 */2 * *`로 정각에 실행된다. GitHub는 정각처럼 부하가 높은 시각의 scheduled run이 지연되거나 일부 유실될 수 있다고 명시한다. 또한 workflow의 실행 branch 직접 반영은 repository ruleset이 GitHub Actions bot의 push를 허용하거나 적절한 bypass를 제공한다는 전제가 필요하지만, 이 운영 전제가 문서에 없다.

- [GitHub Actions schedule 주의사항](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [GitHub repository ruleset과 bypass 설정](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)

권고는 minute `17`처럼 비정각으로 옮기고, schedule이 SLA가 아님을 운영 문서에 명시하며, 누락 시 manual dispatch 절차와 main/develop ruleset의 bot bypass 전제를 기록하는 것이다. 실제 ruleset과 선호 시각은 저장소 밖 정보이므로 이번 검토에서 workflow를 임의 변경하지 않았다.

### F-18. `versions.json`의 latest-stable 순서 계약을 자동 검증하지 않는다 — P2

Python sidebar generator, `docusaurus.config.ts`, docs utility와 redirect/link script는 모두 `versions.json`에서 첫 번째 non-`master` 항목을 최신 안정 버전으로 사용한다. 현재 파일은 `master`, 13.x, 12.x ... 순으로 올바르지만, 새 `14.x`를 배열 끝에 append하면 version filename 생성은 F-16 수정으로 성공하면서 API link와 latest route는 계속 13.x를 가리킨다. 순서·중복을 공통으로 검증하는 loader도 없다.

05·06 문서에는 `master`, 최신 안정, 나머지 내림차순이라는 현재 ordering contract를 명시했다. 다음 version 추가 전에는 한 곳의 validator가 이 순서와 중복을 검사하도록 만들고 Python/TypeScript/JavaScript consumer가 같은 결과를 사용하게 하는 편이 안전하다. 또는 consumer가 semantic version을 직접 정렬한다면 `versions.json`의 표시 순서 의미와 분리해야 한다.

## 6. 권장 구조와 개선 순서

### 6.1 유지할 중심 설계

다음 원칙은 그대로 유지한다.

- pinned upstream source가 유일한 기준
- diff는 변경 범위를 찾고, 최신 full source는 최종 truth로 사용
- 모호한 patch는 fail-closed
- provider-free operation은 결정적으로 처리
- locale 결과는 최신 full source와 검증
- replay는 active worktree 밖에서 실행하고 idempotency 확인

### 6.2 현재 seam 상태

- **ResponseContract**: 구현 완료. source block sequence와 provider output ownership을 적용 전에 검사하고 production/provider check가 공유한다.
- **Version-aware link verification**: 구현 완료. representation은 정규화하되 version identity는 보존한다.
- **PatchOperation coverage**: insert/delete/replace/split/merge/named-section move/code/table/admonition과 모호성 회귀 fixture를 보강했다.
- **CandidateWorkspace**: replay에는 구현되어 있으나 live run 전체 promotion boundary에는 아직 적용하지 않았다.
- **ProviderTelemetry**: prompt hash는 출력하지만 token/latency/retry의 구조화 기록은 아직 없다.

핵심 경계는 유지하되 F-14의 canonicalization 시점, F-15의 알려진 Markdown grammar 공백과 F-18의 version ordering 검증은 보강해야 한다. CandidateWorkspace와 ProviderTelemetry는 실제 운영 복구성이나 비용 계측이 필요할 때 독립적으로 추가할 수 있다.

### 6.3 실행 순서

1. **legacy alert 경계 확정**
   - F-14의 provider 전 canonicalization을 구현하고 기존 localized marker 정리 범위를 결정
2. **Markdown grammar 범위 확정**
   - F-15의 multi-backtick span과 link/site 지원 범위를 구현하거나 명시적 제한으로 고정
3. **version ordering gate 추가**
   - F-18의 `versions.json` 순서·중복을 공통으로 검증
4. **실제 Luna 검증**
   - KO/JA provider check와 대표 문서 human review
5. **Azure 운영 경로 결정**
   - 사용한다면 legacy version 고정 또는 v1 migration 중 하나를 선택해 live 검증
6. **최종 staging과 index gate**
   - 이번 merge 범위의 변경을 모두 끝낸 뒤 intended files를 stage하고 index snapshot에서 translation-check, replay, site/artifact gate 재실행
7. **후속 개선**
   - 필요 시 CandidateWorkspace promotion, provider telemetry, eval 기반 prompt 축소

## 7. merge 전 필수 검증표

| 검증 | 이번 결과 | 반영 기준 |
|---|---:|---:|
| 현재 worktree Python tests | 419 passed | pass |
| 현재 index snapshot Python tests | 153 tests 중 import error | **fail, merge blocker** |
| full identity replay | 679 docs, second process no-op | pass |
| actual current upstream delta | 12 docs × KO/JA pass | pass |
| 기존 KO/JA 전체 annotation check | 최초 2 fail + 미검출 localized 28건 정리 후 pass | pass |
| response-contract negative corpus | missing/echo/duplicate/extra/structure reject | pass |
| wrong-version link | reject | pass |
| named-section reorder | valid move pass, ambiguous ownership reject | pass |
| config/CLI hardening tests | pass | pass |
| Codex 0.144.5 option parsing | pass, unauthenticated 401에서 종료 | pass |
| Node 26 site build | pass | pass |
| KO/JA inline Markdown fragment targets | 46,626 / 46,626 | pass |
| `git diff --check` | pass | pass |
| live Luna KO/JA fixture | credential 부재로 미실행 | 운영 전 pass 필요 |
| live Luna 실제 문서 표본 | 미실행 | 운영 전 human-reviewed pass 필요 |
| Azure adapter | deployment 정보 부재로 미실행 | Azure 사용 시 pass 필요 |

## 8. 실제 Luna 검증 권장 절차

API key 또는 Codex 인증을 사용할 수 있는 일반 terminal/CI secret 환경에서 다음 순서로 검증한다.

1. staged snapshot으로 새 임시 checkout을 만든다.
2. `make translation-check`를 실행하고 manifest를 보존한다.
3. `make translation-provider-check`를 KO/JA 모두 실행한다.
4. contract corpus를 같은 model/reasoning으로 실행한다.
5. `VERSION=13.x DOC=collections.md`처럼 한 문서를 isolated candidate에 실제 번역한다.
6. strict verifier, site-check, artifact-check를 실행한다.
7. 기존 locale 문맥과 비교해 사람이 completeness, 용어, 자연스러움을 검토한다.
8. API와 CLI 각각 token/latency/retry를 기록하되 exact wording 일치는 요구하지 않는다.
9. 같은 input을 재실행해 구조적 idempotency와 불필요한 drift가 없는지 확인한다.

실제 번역 표본 없이 identity replay와 고정 fixture만으로 “다양한 Laravel 문서에서 번역 품질이 확실하다”고 결론 내릴 수는 없다.

## 9. 검증 한계

- OpenAI/Azure credential이 제공되지 않아 실제 번역 API 호출은 하지 못했다.
- 빈 `CODEX_HOME`에서 `codex-cli 0.144.5`의 전체 옵션과 prompt-plus-stdin 파싱은 확인했으며, 예상대로 인증 401에서 model 출력 전에 종료했다.
- `.env`와 credential 파일은 읽지 않았다.
- identity replay는 patch/structure/idempotency 검증이며 번역 의미·문체 검증이 아니다.
- Node 26은 현재 build를 통과하지만 2026년 10월 전까지 Node.js Current release이고 LTS가 아니다.
- Azure deployment·region·지원 API surface는 외부 계정 정보가 없어 판정하지 않았다.
- 현재 index test는 import 단계에서 실패하며 전체 intended worktree도 포함하지 않는다.

## 10. 최종 판정

현재 워킹 트리는 최초 리뷰의 P1 오류, F-13의 구체적인 정규화 오류, F-16의 sidebar version 파생 오류와 현재 산출물의 legacy marker 30건을 정리했고, Python 419개 테스트, 전체 annotation check, 최신 upstream identity replay, Node 26 사이트와 inline fragment target gate를 통과했다. 그러나 현재 index는 import error와 문서 번호 불일치가 있으므로 **merge 불가**다.

남은 일에는 staging 정리뿐 아니라 저장소 안에서 확인된 설계 경계도 포함된다.

1. F-14의 provider 전 legacy marker canonicalization을 구현하거나 자동 운영 제한으로 명시한다.
2. F-15의 multiline code span 손상과 code/link delimiter 검증 공백을 보강한다.
3. 다음 version 추가 전에 F-18의 `versions.json` 순서·중복 gate를 추가한다.
4. 실제 `gpt-5.6-luna` KO/JA fixture와 대표 문서를 검토한다.
5. Azure를 쓴다면 deployment-compatible legacy API 또는 v1 migration 중 하나를 확정하고 live 검증한다.
6. 이번 merge 범위의 변경을 모두 끝낸 뒤 사용자가 최종 intended diff를 stage하고 그 index로 gate를 재실행한다.

F-09 transaction, provider telemetry, prompt 축소와 F-17 운영 hardening은 가치 있는 후속 개선이다. 현재 수정안의 merge blocker는 마지막 staging/index gate인 F-01이며, 자동 번역 운영 전에는 F-14·F-15와 live provider 조건까지 함께 닫아야 한다. F-18은 현재 파일 순서에서는 잠재 경계지만 다음 version 추가 전에 닫아야 한다. F-14~F-18 중 이번 merge 범위에 포함하는 변경이 있다면 그 구현과 검증을 먼저 끝내고 마지막에 index gate를 실행해야 한다.
