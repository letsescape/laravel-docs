# Translation Sync 리팩토링 검증 프롬프트

작성: 2026-07-26 KST
대상 스냅샷: `refactor/sync-docs` 브랜치의 `645a2d4` (`refact: temp`)
선행 문서: `docs/review/translation-sync-refactor-review-2026-07-15.md` (이하 **선행 보고서**)

이 문서 전체를 검증 담당자(사람 또는 에이전트)에게 그대로 프롬프트로 전달한다. 절과 순서를 임의로 건너뛰지 않는다.

---

## 0. 임무와 기본 규칙

### 0.1 임무

`645a2d4`가 **그대로 merge 가능한 상태인지** 판정한다. 판정은 다음 네 가지를 모두 만족해야 통과다.

1. 결정적(provider-free) gate가 **커밋된 스냅샷에서** 재현된다.
2. 선행 보고서가 "해결"로 표시한 항목이 **실제로 코드와 테스트로 고정**되어 있다.
3. 선행 보고서가 깊이 감사하지 않은 대규모 신규 코드에 **새로운 P0/P1 결함이 없다**.
4. 실제 운영 설정으로 `gpt-5.4-mini`와 `gpt-5.6-luna`가 각각 동일한 문서 표본을 3회 연속 독립 실행해, 매번 동기화·KO/JA 번역·검증에 성공한다.

### 0.2 기본 규칙

- **코드를 수정하지 않는다.** 결함은 재현 근거와 함께 보고만 한다. 수정은 사용자 승인 후 별도 작업이다.
- 모든 파일 읽기·쓰기·임시 작업은 현재 프로젝트 루트 내부로 제한한다. 프로젝트의 상위 디렉터리, 형제 디렉터리, 사용자 홈 또는 시스템 임시 디렉터리를 탐색하거나 작업 경로로 사용하지 않는다.
- 루트의 `dot_env`는 사용자가 이번 검증을 위해 제공한 실제 운영 credential 파일이다. 에이전트가 값을 화면이나 로그로 읽어 출력해서는 안 되며, §1.4와 부록 A의 strict loader가 시작하는 제한된 하위 프로세스만 이 파일을 환경 변수로 받을 수 있다.
- live provider 호출은 결정적 gate가 모두 통과한 뒤 모델별 `provider-check` 1회와 문서 1건 × 3회 독립 실행만 허용한다. 총 범위는 2개 모델 × 3회이며, 추가 표본·전체 동기화·반복 품질 실험은 별도 승인 없이 실행하지 않는다.
- 원격에 영향을 주는 행위(push, PR 생성, workflow 실행)를 하지 않는다.
- 어떤 저장소나 임시 clone에서도 `git commit`, `git merge`, `git rebase`, tag 생성 또는 push를 실행하지 않는다. `act`로 commit/push/deploy step이 포함된 원본 workflow를 실실행하지 않는다.
- `dot_env`를 stage, commit, 임시 checkout, Docker build context 또는 테스트 산출물에 복사하지 않는다.
- `set -x`, `printenv`, `env`, process environment dump, HTTP debug logging처럼 secret 값을 노출할 수 있는 진단을 사용하지 않는다.
- `act`와 Docker가 설치되어 있으면 우선 활용하되, `act`는 원본 workflow의 dry-run/구조 확인에만 사용하고 실제 번역은 commit step이 없는 Docker 명령으로 실행한다.
- 사소한 말투·문체 차이는 결함으로 취급하지 않는다. 의미 누락·추가, 기술적으로 잘못된 번역, 영어 본문 잔존, Markdown/링크/앵커/코드 손상과 동기화 실패를 우선 판정한다.
- 선행 보고서를 **정답지가 아니라 검증 대상 주장(claim)으로** 취급한다. 보고서와 코드를 쓴 주체가 같으므로, 보고서가 놓친 것은 보고서를 읽어서는 찾을 수 없다.
- 확신이 없으면 "확인 불가"로 명시한다. 실행하지 않은 검증을 통과로 적지 않는다.

### 0.3 심각도 (선행 보고서와 동일 척도)

- **P0 / release blocker**: 커밋 또는 운영 반영을 막아야 한다.
- **P1 / high**: 자동 커밋에 잘못된 문서가 들어가거나 정상 upstream 변경이 막힐 수 있다.
- **P2 / medium**: 오류 진단, 재현성, provider 일관성, 유지보수성을 유의미하게 낮춘다.
- **P3 / low**: 현재 운영 경로는 통과하지만 계약·개발 환경을 더 정확히 만들 필요가 있다.

---

## 1. 대상 스냅샷과 검증 환경

### 1.1 스냅샷 사실관계 (먼저 직접 확인할 것)

| 항목 | 값 |
|---|---|
| 브랜치 | `refactor/sync-docs` |
| 검증 대상 커밋 | `645a2d4` (`refact: temp`) |
| `main..HEAD` | 이 커밋 **1개** |
| 변경 규모 | 74 files, +13,232 / −1,288 |
| 활성 작업 트리 | `dot_env`, `prompt.md`가 미추적 상태일 수 있음. 둘 다 사용자 소유 파일로 취급 |

```
git log --oneline main..HEAD
git status --porcelain
git show --stat 645a2d4
```

### 1.2 스냅샷 경계가 바뀌었다 — 가장 중요한 전제

선행 보고서의 모든 수치(Python 419 tests, 679개 문서 identity replay, KO/JA fragment target 46,626, Node 26 build)는 **워킹 트리** 기준이었고, 그 보고서의 유일한 P0인 **F-01은 "staged index가 커밋 가능한 상태가 아니다"** 였다.

지금은 당시 intended code/doc 변경이 `645a2d4`에 들어갔다. 활성 워킹 트리에는 검증 프롬프트와 운영 credential이 미추적 파일로 존재하지만, 이들은 검증 대상 커밋에 포함되지 않는다. 즉 **선행 보고서의 최종 판정(merge 불가)은 현재 검증 대상에 그대로 적용되지 않으며, 동시에 그 통과 수치들도 현재 커밋 스냅샷에서 재확인된 적이 없다.**

따라서 §2를 다른 어떤 작업보다 먼저 수행한다.

### 1.3 실행 환경 계약

- Python: `uv run --frozen --python 3.14` (Makefile 정의를 그대로 사용, 임의로 다른 인터프리터를 쓰지 않는다)
- Node: 26 계열 (`.nvmrc` 값과 실제 실행 버전이 일치하는지 함께 확인)
- 로컬 검증 경로는 `<project-root>/.review/translation-sync-validation/` 아래로 고정한다. `mktemp`, `/tmp`, 프로젝트 상위 경로 또는 홈 디렉터리를 사용하지 않는다.
- `TMPDIR`, `UV_CACHE_DIR`, npm cache와 검증용 `HOME`도 모두 위 `.review` 아래로 지정한다.
- `replay.py`는 내부적으로 disposable sandbox commit을 생성하므로 이번 "commit 절대 금지" 실행에서는 `make translation-replay`와 이를 포함하는 `make translation-check`를 직접 실행하지 않는다. replay 동작은 코드·단위 테스트로 검토하고, 실제 end-to-end는 commit 없는 Docker 실행으로 대체한다.
- live 검증은 `dot_env`를 깨끗한 checkout 밖에 둔 채 strict loader가 만든 하위 프로세스의 environment로만 주입한다.
- 현재 확인된 도구는 `act 0.2.89`, Docker `29.1.3`, Docker Compose `v5.0.1`이다. 실행 시 실제 버전을 다시 기록한다.
- 각 gate의 정확한 명령은 부록 B에 정리되어 있다.

### 1.4 실제 운영 credential 안전 계약

현재 `dot_env`는 다음 변수 이름 4개를 포함한다. 값은 출력하거나 보고서에 기록하지 않는다.

```text
TRANSLATION_PROVIDER
TRANSLATION_MODEL
TRANSLATION_REASONING_EFFORT
OPENAI_API_KEY
```

사전 확인에서 assignment 4개, invalid line 0개, bash 문법 유효로 확인됐다. 실행 담당자는 값이 아니라 다음 조건만 다시 검사한다.

1. 일반 파일이며 symlink가 아니다.
2. 소유자가 현재 사용자다.
3. 빈 값이 없고 중복 key가 없다.
4. assignment/comment/blank line 외의 shell 문법이 없다.
5. 파일 권한이 `0600`이다.

사전 점검에서 `0644`였던 권한은 실제 키 보호를 위해 `0600`으로 축소했다. 실행 시작 시 다시 확인하고, `0600`이 아니면 live 호출 전에 `chmod 600 dot_env`를 적용한다. 권한 변경 외에는 파일을 수정하지 않는다.

`.gitignore`와 `.dockerignore`의 `.env` 규칙은 `dot_env`를 보호하지 않는다. 따라서:

- 활성 저장소에서 `git add -A`, `git add .`, commit을 실행하지 않는다.
- `dot_env`가 있는 활성 저장소를 Docker build context로 사용하지 않는다.
- live 실행용 임시 clone에 `dot_env`를 복사하지 않는다.
- credential 경로는 clone 외부의 절대 경로로 유지한다.
- live 명령은 부록 A의 strict loader로만 실행해, dotenv 값을 shell code로 평가하지 않고 종료 후 credential 환경이 상위 셸에 남지 않게 한다.

위 조건 중 하나라도 충족하지 않으면 결정적 검증은 계속하되 live 단계만 중단하고 이유를 보고한다.

---

## 2. Section 1 — 깨끗한 checkout에서 gate 수치 재확립

`645a2d4`를 프로젝트 내부 `.review/translation-sync-validation/base/`에 새로 clone해서(현재 워크트리를 재사용하지 말 것) 아래를 실행하고, 선행 보고서의 수치와 비교한다. 준비 명령은 부록 A.1을 따른다.

| # | gate | 명령 | 선행 보고서 기준값 | 이번 결과 | 판정 |
|---|---|---|---|---|---|
| 2.1 | Python 단위 테스트 | `make translation-test` | 419 passed | | |
| 2.2 | replay 계약 | replay 관련 단위 테스트 + `replay.py` 코드 검토 | 실제 replay 679 docs, 2회차 no-op | | |
| 2.3 | workflow 구조 | `act --dryrun` + workflow 정독 | 해당 없음 | | |
| 2.4 | 산출 경로 검사기 smoke | `make translation-artifact-check` | pass | | |
| 2.5 | Markdown 링크 유틸 | `make site-test` | pass | | |
| 2.6 | typecheck + build + anchor | `make site-check` | fragment target 46,626 / 46,626 | | |
| 2.7 | 공백/충돌 마커 | `git diff --check HEAD^...HEAD` | pass | | |

> **주의**: `make translation-replay`와 `make translation-check`는 `replay.py`의 내부 임시 commit을 동반하므로 이번 실행에서는 금지한다. 실행하지 않은 replay를 통과로 적지 않는다. 대신 419개 단위 테스트의 replay fixture, 코드 검토, 모델별 3회의 commit 없는 Docker end-to-end 결과를 각각 독립 증거로 기록한다.

> `make translation-artifact-check`(`validate_generated_changes.py`)는 `git ls-files --others --exclude-standard`로 **untracked 파일까지** 검사 대상에 넣는다. 따라서 활성 워크트리에 남아 있는 `prompt.md`, `dot_env`, `.review`에서 실행하면 실패한다. 2.4는 깨끗한 base clone에서 실행하고, 실제 의미 있는 산출 경로 판정은 각 live run checkout에서 §2.10으로 수행한다.

기록 규칙:

- 통과/실패뿐 아니라 **실제 숫자**(테스트 수, 문서 수, target 수)를 적는다. 숫자가 선행 보고서와 다르면 그 차이 자체가 finding 후보다. 특히 테스트 수가 419보다 **적으면** 커밋 과정에서 테스트가 누락됐을 가능성을 의심한다.
- 실패 시 재현 명령과 출력 앞뒤 20줄을 그대로 인용한다.
- `make site-check`와 Docker 실행은 오래 걸릴 수 있지만, 사용자 완료 조건인 모델별 3회 실행을 시간 부족으로 축소하지 않는다. 끝내지 못하면 검증은 미완료다.

### 2.8 실제 운영 provider 계약 gate

§2.1~2.7과 §1.4가 모두 통과한 뒤 부록 A.4의 strict runner로 각 모델에 대해 다음을 한 번씩 실행한다.

```text
gpt-5.4-mini  → provider_check.py
gpt-5.6-luna  → provider_check.py
```

기본 실행이 KO/JA를 모두 검사하는지 확인한다. provider, model, reasoning effort, locale, prompt SHA-256은 기록할 수 있지만 secret, request header, credential 경로는 기록하지 않는다.

판정 기준:

- KO와 JA가 모두 fresh response contract와 최종 verifier를 통과한다.
- wrapper/설명/외곽 code fence/영어 echo/구조 손상이 없다.
- 실제로 선택된 provider와 model이 프로젝트 운영 의도와 일치한다.
- 실패 시 API 응답 본문 전체나 환경 변수를 덤프하지 않고, 프로젝트가 정제한 오류만 기록한다.

### 2.9 두 모델 × 3회의 실제 문서 end-to-end 번역

provider fixture만으로는 원문 동기화부터 파일 기록까지의 live 경로를 증명할 수 없다. 부록 A.5에 따라 프로젝트 내부에 6개의 독립 checkout을 만들고, 각 checkout에서 `version-13.x/ai-sdk.md` 한 건만 과거 기준본으로 되돌린 뒤 실제 번역한다.

| 모델 | Run 1 | Run 2 | Run 3 | 완료 조건 |
|---|---|---|---|---|
| `gpt-5.4-mini` | | | | 3/3 성공 |
| `gpt-5.6-luna` | | | | 3/3 성공 |

각 run은 이전 run의 결과를 재사용하지 않는다. 동일한 HEAD와 동일한 부모 기준본에서 시작해야 하며, 로그에 실제 `translating: ko`, `translating: ja`, `translated 1 doc(s) into ko, ja`가 있어야 한다. `no source changes to translate`는 번역 성공 1회로 세지 않는다.

이 단계는 다음을 동시에 검증해야 한다.

- 공식 upstream 원문 동기화와 run별 manifest 생성
- 변경 감지와 PatchPlan
- KO/JA provider 호출
- response contract
- 후처리와 최종 verifier
- 허용 경로에만 기록
- 두 번째 실행 no-op

`ai-sdk.md`를 사용할 수 없으면 이번 커밋에서 영어 캐시와 KO/JA가 함께 변경된 문서 하나를 선택하고 이유를 기록한다. 6회 모두 같은 문서와 같은 기준 상태를 사용한다. 전체 버전이나 여러 문서를 실행하지 않는다.

### 2.10 live 산출물 후 gate

2.9의 6개 checkout 각각에서 실행한다.

```text
make translation-artifact-check
make site-check
git diff --check
```

다음을 확인한다.

- 변경 경로가 영어 캐시, 해당 KO/JA 문서와 필요한 sidebar 산출물로 제한된다.
- `dot_env`, `prompt.md`, 코드, workflow가 산출물에 포함되지 않는다.
- KO/JA diff를 사람이 읽어 누락, 영어 본문 잔존, 중대한 오역과 구조 문제를 확인한다. 사소한 말투·문체 차이는 실패 사유가 아니다.
- 각 run에서 같은 manifest로 명령을 한 번 더 실행했을 때 `no source changes to translate`로 끝나고 추가 diff가 생기지 않는다. 이 no-op 재실행은 3회 성공 횟수에 포함하지 않는다.

### 2.11 F-01(P0)의 실제 종료 여부 — 저비용·고판별 확인

선행 보고서 F-01의 근거 두 가지가 커밋에서 닫혔는지 직접 확인한다.

1. **import seam 검증** — 단순 import 성공 여부가 아니라 **그것을 성립시키는 구조**를 본다.
   `provider_check.py:11`은 `from sync import config, prompt, response_contract, translate, verify`인 반면, 실제 파일은 `sync/verification/response_contract.py`에 있다. 이 import는 `sync/__init__.py`가 하위 모듈을 재export하고 `sys.modules`에 평탄화된 alias를 등록하기 때문에만 성립한다(이번 커밋에서 변경된 부분이다). 따라서 확인할 것은:
   - `sync/__init__.py`의 `_ALIASES` 재export와 `sys.modules` 등록이 **의도된 설계**인가, 모듈 트리 재배치의 부산물인가. 의도라면 어디에 문서화되어 있는가.
   - `sidebar`만 `sys.modules` 등록에서 제외된 이유가 무엇이며, 그 비대칭이 의도적인가.
   - 이 평탄화가 순환 import나 모듈 중복 로드(같은 모듈이 두 경로로 각각 초기화되는 상태)를 만들지 않는가.
   - `make translation-test`가 import 단계에서 실패하지 않는가 (선행 보고서의 index 스냅샷은 `Ran 153 tests, errors=1`이었다). 테스트가 통과한다면 import 자체는 이미 해소된 것이므로, 판정은 위 세 항목의 설계 타당성으로 내린다.
2. **문서 번호 정리**
   - `translation-sync/docs/07-error-cases.md`가 **남아 있지 않은지** (커밋에서 삭제되고 `07-local-replay.md` + `08-error-cases.md`로 재편된 것이 의도대로인지)
   - `00-workflow-summary.md`가 현재 번호 체계(00~08)를 정확히 참조하는지
   - 문서 간 상호 참조에 stale 링크가 없는지

이 두 항목이 모두 성립하면 F-01은 닫힌다. 하나라도 어긋나면 **F-01은 여전히 P0**이며 그 사실을 최상단에 보고한다.

---

## 3. Track A — "해결" 클레임의 적대적 재검증

선행 보고서 §4에서 **해결**로 표시된 항목이 대상이다. 각 항목에 대해 다음 세 질문에 답한다.

- **A-1. 어디에 고정되어 있나**: 그 주장을 강제하는 구체적 코드 지점(`파일:줄`)과 테스트(테스트 함수명)를 지목한다.
- **A-2. 되돌리면 깨지나**: 그 수정을 되돌렸다고 가정할 때 지목한 테스트가 **실제로 실패하는가**. 논리적으로 판단하되, 판단이 애매하면 격리 사본에서 국소 revert 후 해당 테스트만 돌려 확인한다(원본 트리는 수정 금지).
- **A-3. 우회 가능한가**: 그 테스트가 통과하면서도 결함이 재발할 수 있는 입력이 존재하는가. 존재한다면 그 입력을 구체적으로 제시한다.

A-2가 "실패하지 않는다"거나 A-3에 해당 입력이 있으면, 해당 항목은 **해결이 아니라 미완결**로 재분류한다.

| 항목 | 선행 보고서 주장 | 확인 지점 |
|---|---|---|
| F-02 (P1) | strict response contract + negative corpus 도입 | `sync/verification/response_contract.py`, `tests/test_verify.py`. 본문 누락 / 영어 echo / 중복 occurrence 누락 / 추가 prose / 미지원 구조 5종 거부가 각각 **독립된** negative 테스트로 존재하는가 |
| F-03 (P1) | provider check가 production verifier와 동일 contract 공유 | `provider_check.py`가 `verify`/`response_contract`를 실제로 같은 경로로 호출하는가, 아니면 완화된 별도 경로가 남아 있는가 |
| F-04 (P1) | link version identity 보존 + wrong-version negative test | `verify.py`의 정규화 로직. 표현만 정규화하고 버전 식별자는 보존하는지, 잘못된 버전 링크를 거부하는 테스트가 있는지 |
| F-05 (P2) | named-section reorder / separator 보존 구현 | `sync/translation/patch.py` + `tests/test_patch.py`. 유효 이동은 통과, 모호한 ownership은 거부되는지 |
| F-06 (P2) | 숫자형 option 조기 검증, `ConfigError` → exit 2 | `sync/runtime/config.py`, `main.py`. endpoint URL 형식, API version 형식, 모델명 등 **어디까지** 검증하는지 경계를 명시 |
| F-07 (P2) | CLI env allowlist, 임시 cwd, 사용자 hook 차단 | `sync/translation/translate.py`의 Codex CLI adapter. allowlist 누락 시 환경 변수가 새는 경로가 없는지 |
| F-08 (P2) | prompt 규칙 충돌 제거 | `prompt.md`, `prompt_jp.md`. 생략 허용/금지 충돌이 실제로 사라졌는지, 두 언어 프롬프트가 서로 다른 규칙을 갖고 있지 않은지 |
| F-10 (P3) | Node 26 build 통과 | §2.6 결과로 대체 확인 |
| F-13 (P1) | 정규화기의 Markdown context 손상 수정 | `sync/common/markdown.py`(+606), `preprocess.py`, `postprocess.py`. `> **Note:**` parser, heading ID, sentinel, style/list 경계 각각에 회귀 테스트가 있는지 |
| F-16 (P2) | sidebar version filename을 `versions.json`에서 동적 파생 | `sync/sidebar/generator.py`. 하드코딩된 `8.x`~`13.x` 목록이 **완전히** 사라졌는지 (다른 파일에도 남아 있지 않은지 grep) |

Track A의 출력은 항목별 한 줄 판정(**확인됨 / 부분적 / 미확인 / 반증됨**)과 근거다.

---

## 4. Track B — 신규·대폭 변경 코드의 정면 리뷰

선행 보고서가 깊이 감사하지 않은 영역이다. **여기가 이번 검증의 실질적 가치**이며, 새 finding은 대부분 여기서 나와야 한다.

리뷰 대상 규모:

| 파일 | 현재 줄수 | 이번 커밋 변화 |
|---|---:|---:|
| `sync/translation/patch.py` | 3,045 | +2,440 |
| `sync/verification/response_contract.py` | 1,317 | 신규 |
| `sync/common/markdown.py` | 711 | +606 |
| `main.py` | 764 | +381 |
| `sync/translation/translate.py` | 515 | +350 |
| `sync/verification/verify.py` | 480 | +213 |
| `replay.py` | 414 | 신규 |
| `sync/source/upstream.py` | 181 | +115 |
| `provider_check.py` | 179 | 신규 |
| `validate_generated_changes.py` | 86 | 신규 |

### 4.1 `patch.py` — patch engine (최우선)

- **fail-closed 원칙이 실제로 지켜지는가.** 모호한 patch를 조용히 적용하는 경로(예외를 삼키는 `try/except`, 최선 추정 fallback, 부분 일치 허용)가 있는지 찾는다. 발견 시 그 입력을 제시한다.
- **경계 조건**: 문서 맨 앞/맨 뒤 삽입, 인접 hunk 병합, 코드 펜스 내부와 경계가 겹치는 hunk, 표 행 패치, admonition 블록, 중복 occurrence(동일 문자열이 여러 번 등장)에서의 대상 선택.
- **후보 선택 로직**: `main.py`가 여러 후보 중 issue 수가 최소인 것을 고르는 구조라면, 동점 처리와 "issue는 적지만 내용이 더 손상된" 후보가 선택될 가능성을 평가한다.
- 3,045줄 전체를 정독할 필요는 없다. **공개 진입점부터 시작해 fail-closed 경계와 분기 조건에 집중**한다.

### 4.2 `response_contract.py` — provider 응답 계약

- contract가 거부해야 할 5종(본문 누락 / 긴 영어 echo / 중복 occurrence 누락 / 추가 prose / 미지원 구조)에 대해, **거부 조건이 휴리스틱인지 구조적 판정인지** 구분한다. 휴리스틱이면 임계값과 오탐/미탐 방향을 명시한다.
- 정상 번역이 거부되는 경우(false positive)가 파이프라인 전체를 막는지, 아니면 재시도로 흡수되는지 확인한다. 전자라면 정상 upstream 변경을 막는 P1 후보다.
- `verify.py`와의 책임 분리가 명확한지, 같은 검사를 서로 다른 기준으로 중복 수행하지 않는지 본다.

### 4.3 `markdown.py` — 공통 파서

- pre/postprocess/verify/contract가 모두 이 파서에 의존한다면, **한 곳의 파싱 오차가 전 단계에 전파**된다. 파서가 CommonMark/GFM의 어느 범위를 지원한다고 가정하는지, 그 가정이 문서화되어 있는지 확인한다.
- 선행 보고서가 F-15에 남긴 미해결 문법(여러 줄 code span, multi-backtick span, inline code 내부 `<img>`, 1~3칸 들여쓴 blockquote)이 **이 커밋에서 상태가 바뀌었는지**만 확인한다(§6 취급 규칙).

### 4.4 `translate.py` / `provider_check.py` — provider 경계

- API adapter와 Codex CLI adapter가 **동일한 contract 검사를 통과해야만** 결과를 반환하는지.
- 재시도 정책: 무엇을 재시도하고(429/5xx/timeout), 무엇을 재시도하지 않는지(contract 위반). contract 위반을 재시도로 덮으면 잘못된 결과가 우연히 통과할 수 있다.
- 실패 시 종료 코드와 로그가 원인을 구분 가능한 형태인지.

### 4.5 `replay.py` — 격리 통합 검증

- 활성 워크트리 밖에서 실행되는 것이 **코드로 보장**되는지, 관례에 불과한지.
- identity replay가 실제로 무엇을 증명하는지 정확히 진술한다(구조·멱등성이며 번역 의미가 아니다).
- 2회차 no-op 판정 기준이 무엇인지(파일 해시 비교인지, diff 없음인지).

### 4.6 테스트 품질 — 계약을 고정하는가, 구현을 반사하는가

테스트 증가분이 매우 크다: `test_verify.py` +1,655, `test_patch.py` +1,405, `test_main.py` +728, `test_translate.py` +653, `test_replay.py` 347(신규), `test_upstream.py` +165, `test_provider_check.py` 147(신규).

각 주요 테스트 파일에서 표본을 뽑아 다음을 판정한다.

- **기대값이 구현 출력을 그대로 복사한 것인가**(구현을 바꾸면 테스트도 같이 바꿔야 하는 형태), 아니면 **독립적으로 서술된 계약인가**.
- negative 테스트가 "거부됐다"만 확인하는가, **거부 사유까지** 확인하는가. 사유를 확인하지 않으면 엉뚱한 이유로 거부돼도 통과한다.
- 대량의 fixture가 실제로 서로 다른 경로를 커버하는가, 같은 경로를 반복하는가.
- 위 §3 A-2 판정(revert하면 깨지는가)의 근거로 사용한다.

---

## 5. 생성 산출물과 CI/배포 경로

### 5.1 커밋에 섞여 있는 생성 산출물

이 커밋은 파이프라인 리팩토링과 **번역 산출물 변경을 함께 담고 있다**.

- `i18n/ja/.../version-{8.x,9.x,10.x,12.x,13.x,master}/*.md` (controllers, helpers, http-tests, notifications, ai, ai-sdk, boost)
- `versioned_docs/version-{12.x,13.x,master}/{ai-sdk,boost}.md`

확인할 것:

1. 이 변경들이 **리팩토링된 파이프라인이 재생성하는 결과와 일치**하는가. 즉 현재 코드로 다시 돌렸을 때 no-op인가, 아니면 또 다른 diff가 나오는가.
2. 각 diff가 의도된 개선(용어 정정, 정규화)인지, 파이프라인 변경의 **부작용**인지 내용으로 판단한다. 특히 `ai-sdk.md`(각 9줄)와 `boost.md`(각 6줄)처럼 여러 버전에 동일 패턴으로 적용된 변경은 한 곳만 보지 말고 일관성을 확인한다.
3. `validate_generated_changes.py`의 `_ALLOWED_PATHS`가 **정확히 이 경로들만** 허용하는지, 그리고 파이프라인이 건드리면 안 되는 경로(코드, 워크플로, 프롬프트)를 확실히 차단하는지. 정규식이 과대 허용(`[^/]+\.md`의 범위)인지 검토한다.

### 5.2 Python gate가 닿지 않는 배포 경로

`.github/workflows/sync-translation.yml`(+110)은 이 커밋에서 **가장 큰 비-Python 동작 변경**이며 `make translation-check`가 전혀 커버하지 않는다. 별도로 정독한다.

확인할 것:

- **credential 경계**: `persist-credentials: false`로 checkout하고 push 단계에서만 `gh auth setup-git`을 호출하는 구조가 실제로 의도대로 동작하는가. 그 사이 단계(`npm ci`, preflight, provider check, build)에서 write credential이 없어 실패하는 경로가 없는가.
- **branch ref 검증**: `github.ref_type != 'branch'`에서 실패시키는 가드가 schedule/dispatch 양쪽에서 올바르게 동작하는가.
- **manifest 계약**: preflight 단계가 `MANIFEST` 파일을 만들지 못하면 실패시키는 로직과, `status`를 보존해 마지막에 `exit "$status"`하는 흐름이 오류를 삼키지 않는지.
- **단계 순서**: preflight → provider check → 실제 sync → site-check → artifact-check → commit → push → deploy. 검증이 커밋 **전**에 오는지, 실패 시 부분 산출물이 남는지(F-09 transaction 경계와 연결).
- **deploy 트리거**: `github.ref_name == 'main'` 조건이 이전 로직과 동등한지.
- `.github/workflows/deploy.yml`(+10), `.nvmrc`, `Dockerfile`, `docker-compose.yml`, `package.json`, `Makefile`(+60)의 변경이 서로 모순되지 않는지(특히 Node 버전이 `.nvmrc` / workflow / Dockerfile / `docker-compose.yml`에서 일치하는지).

### 5.3 문서-구현 정합

`translation-sync/docs/00~08`과 `prompt.md` / `prompt_jp.md`가 현재 구현을 정확히 기술하는지 표본 확인한다. 특히 §2.11에서 확인한 번호 재편, 그리고 새로 추가된 `07-local-replay.md`(replay 실제 동작과 일치하는지), `08-error-cases.md`(기술된 실패 사례가 현재 코드에서 재발 불가인지)를 본다.

---

## 6. 이미 알려진 미해결 항목 — 현재 증거로 재판정

다음은 선행 보고서에 **미해결 또는 사용자 결정 필요**로 기록되어 있다. 같은 설명을 새 ID로 중복 제출하지는 않지만, 현재 코드와 실제 실행 증거로 상태를 재판정해야 한다.

| 항목 | 성격 | 이번 검증의 필수 증거 |
|---|---|---|
| F-09 (P3) | 실행 전체가 하나의 transaction이 아님 | 임시 clone에서 후반 target 실패 시 앞선 파일이 남는지, workflow가 이를 commit하지 않는지 |
| F-14 (P1) | legacy note canonicalization이 provider 뒤에 있어 번역된 marker를 놓침 | localized legacy marker 최소 fixture로 현재 생성 경로를 재현 |
| F-15 (P1) | 파서/site gate의 Markdown 문법 지원 범위가 CommonMark/GFM보다 좁음 | multi-backtick/multiline code span과 link title 최소 fixture의 실제 판정 |
| F-18 (P2) | `versions.json` latest-stable 순서·중복 자동 검증 부재 | 임시 repo에서 순서 오류와 중복을 loader가 거부하는지 |
| F-11 (P2) | Azure API version / adapter 전략 | 현재 `dot_env`에는 Azure 설정이 없으므로 OpenAI 검증과 구분해 미검증으로 유지 |
| F-12 (P3) | deploy workflow action의 SHA 고정 여부 | sync/deploy workflow의 pinning 정책 차이 확인 |
| F-17 (P3) | cron 정각·direct push의 GitHub 운영 조건 의존 | 저장소 내부에서 증명 가능한 부분과 GitHub ruleset 외부 조건 분리 |

각 항목을 **해결 / 부분 해결 / 그대로 / 악화 / 외부 결정 필요 / 검증 불가** 중 하나로 판정하고 근거를 남긴다. F-14와 F-15가 그대로 P1이면 merge 가능 여부와 무인 운영 가능 여부에서 각각 어떤 blocker인지 명시한다.

---

## 7. 산출물 형식

`docs/review/` 아래에 **새 리뷰 문서**를 한국어로 작성한다. 파일명은 `translation-sync-refactor-verification-<검증일>.md`(예: `translation-sync-refactor-verification-2026-07-26.md`)로 한다.

- 선행 보고서(`translation-sync-refactor-review-2026-07-15.md`)는 **수정하지 않는다.** 그 문서는 당시 워킹 트리에 대한 기록이며, 이번 문서는 `645a2d4` 커밋 스냅샷에 대한 독립된 판정이다.
- 선행 보고서의 finding을 인용할 때는 ID(F-01 등)로 참조만 하고 내용을 복제하지 않는다.
- 아래 순서와 항목을 그대로 따르며, 선행 보고서와 나란히 비교할 수 있어야 한다.

1. **결론** — 판정 한 문장(`merge 가능` / `조건부 가능` / `merge 불가`)과 그 근거 3줄 이내. 조건부·불가면 blocker를 번호로 나열.
2. **검증 스냅샷** — 커밋 SHA, 실행 환경(Python/Node 실제 버전), 실행한 deterministic/live gate와 실행하지 못한 gate.
3. **gate 결과표** — §2의 표를 실제 수치로 채운 것.
4. **Track A 결과** — 항목별 확인됨/부분적/미확인/반증됨 + 근거.
5. **신규 Finding 요약표** — ID(`N-01` 형식), 심각도, 한 줄 요약, 상태.
6. **상세 Finding** — 아래 템플릿.
7. **알려진 미해결 항목의 상태 변화** — §6의 7개 항목 한 줄씩.
8. **live 표본 결과** — provider/model/prompt hash, KO/JA 계약, 선택 문서, 변경 경로, 사람 검토 결과. secret은 기록하지 않는다.
9. **검증 한계** — 실행하지 못한 것과 그 이유(§9).
10. **최종 판정과 다음 작업**.

### Finding 템플릿

```
### N-01. <한 문장 결함 진술> — P1

#### 근거
<파일:줄, 코드 인용, 재현 명령과 실제 출력>

#### 재현 조건
<구체적 입력 → 잘못된 출력/실패. "가능성이 있다"가 아니라 실제 입력으로 서술>

#### 영향
<어떤 문서가 어떻게 잘못되거나, 어떤 정상 변경이 막히는가>

#### 권고
<최소 범위의 수정 방향. 코드는 작성하지 않는다>

#### 완료 조건
<이 결함이 닫혔다고 판정할 수 있는 검증 가능한 기준(회귀 테스트 포함)>
```

재현 조건을 채울 수 없는 finding은 **제출하지 않는다.** "~일 수 있다" 수준의 추측은 별도 절에 "추가 조사 필요"로 모아 한 줄씩만 적는다.

---

## 8. 우선순위

시간이 제한되면 이 순서로 수행하고, 도달하지 못한 지점을 보고서에 명시한다.

1. §2.1~2.4 + §2.11 (F-01 종료 여부 — P0 판정에 직결)
2. §4.1 `patch.py` fail-closed, §4.2 response contract
3. §5.1 생성 산출물 재현성 + `validate_generated_changes.py` 허용 범위
4. §5.2 `sync-translation.yml`
5. §3 Track A 적대적 재검증
6. §2.5~2.7 site gate
7. §2.8~2.10 실제 운영 provider와 문서 1건의 live 경로
8. §4.6 테스트 품질, §5.3 문서 정합

---

## 9. 이 검증의 구조적 한계 (보고서에 그대로 명시할 것)

- **identity replay의 의미**: patch/구조/멱등성 검증이며 번역 품질 검증이 아니다.
- **live 검증의 범위**: 두 모델의 provider fixture와 동일한 실제 문서 1건을 모델별 3회 검사한다. 전체 Laravel 문서군의 의미 정확성이나 장기간 provider 안정성을 보장하지 않는다.
- **secret 비열람**: `dot_env`의 key 이름과 구조만 확인하고 값은 사람이 읽지 않는다. 실제 유효성은 하위 프로세스 호출 성공으로만 간접 확인한다.
- **현재 provider만 검증**: `dot_env`가 실제 선택한 provider 경로만 검증한다. Azure 필수 key가 없으므로 Azure deployment/API version 경로는 판정하지 않는다.
- **비용·성능 표본 한계**: 모델별 3회의 한 문서 실행에서 얻은 latency/retry는 운영 전체 비용이나 tail latency를 대표하지 않는다.
- 위 항목은 결함이 아니라 **검증 범위의 한계**다. 범위 밖 항목을 "통과"로 적지 않는다.

---

## 부록 A. 프로젝트 내부의 실제 운영 검증 절차

### A.1 프로젝트 내부 workspace 준비

프로젝트 루트에서 시작한다. 모든 cache, clone, log, manifest와 임시 HOME은 프로젝트 내부에 둔다.

```bash
project_root="$(git rev-parse --show-toplevel)"
test "$PWD" = "$project_root"
umask 077

review_root="$project_root/.review/translation-sync-validation-$(date +%Y%m%d-%H%M%S)"
base_checkout="$review_root/base"
credential_file="$project_root/dot_env"

mkdir -p \
  "$review_root/home" \
  "$review_root/tmp" \
  "$review_root/uv-cache" \
  "$review_root/npm-cache" \
  "$review_root/logs" \
  "$review_root/runs"

export HOME="$review_root/home"
export TMPDIR="$review_root/tmp"
export UV_CACHE_DIR="$review_root/uv-cache"
export npm_config_cache="$review_root/npm-cache"

git clone --no-hardlinks "$project_root" "$base_checkout"
git -C "$base_checkout" checkout --detach 645a2d4
test -z "$(git -C "$base_checkout" status --porcelain)"
```

금지 사항:

- `cd ..`, `find ..`, `ls ..`, `~`, `/tmp`, 시스템 임시 경로 사용
- 프로젝트 상위·형제 디렉터리 또는 사용자 홈 탐색
- 어떤 checkout에서도 `git commit`, merge, rebase, tag, push
- 검증 경로를 프로젝트 밖으로 mount

### A.2 credential 보호와 무출력 검증

아래 검사는 성공 시 secret 값을 출력하지 않는다.

```bash
test -f "$credential_file"
test ! -L "$credential_file"
test -O "$credential_file"
chmod 600 "$credential_file"
test "$(stat -f '%OLp' "$credential_file")" = "600"

LC_ALL=C awk '
  /^[[:space:]]*($|#)/ { next }
  /^[A-Za-z_][A-Za-z0-9_]*=.+$/ {
    key=$0
    sub(/=.*/, "", key)
    if (seen[key]++) exit 1
    present[key]=1
    next
  }
  { exit 1 }
  END {
    required[1]="TRANSLATION_PROVIDER"
    required[2]="TRANSLATION_MODEL"
    required[3]="TRANSLATION_REASONING_EFFORT"
    required[4]="OPENAI_API_KEY"
    for (index=1; index<=4; index++) {
      if (!present[required[index]]) exit 1
    }
  }
' "$credential_file"
```

실패하면 값을 조사하지 말고 live 단계를 중단한다.

다음은 항상 금지한다.

- `cat dot_env`, `source dot_env`, `. dot_env`
- `env`, `printenv`, `set`, `export -p`
- `set -x`, `curl -v`, SDK HTTP debug
- secret을 command argument, report, log file명 또는 tool output에 포함
- `dot_env`를 clone, image, volume 또는 Docker build context에 복사

### A.3 모델 override를 지원하는 strict runner

`.review` 아래에 검증 전용 `credential_runner.py`를 `apply_patch`로 만든다. 이 파일에는 secret이 들어가지 않으며 commit하지 않는다.

```python
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

credential_path = Path(sys.argv[1])
working_directory = Path(sys.argv[2])
model = sys.argv[3]
command = sys.argv[4:]

allowed_models = {"gpt-5.4-mini", "gpt-5.6-luna"}
allowed_keys = {
    "TRANSLATION_PROVIDER",
    "TRANSLATION_MODEL",
    "TRANSLATION_REASONING_EFFORT",
    "OPENAI_API_KEY",
}
passthrough_keys = {
    "PATH",
    "HOME",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "DOCKER_HOST",
    "DOCKER_CONTEXT",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
}
key_pattern = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

if model not in allowed_models:
    raise SystemExit("unsupported model override")
if not command or command[0] not in {"docker", "make"}:
    raise SystemExit("unsupported validation command")

values = {}
for line_number, raw_line in enumerate(
    credential_path.read_text(encoding="utf-8").splitlines(), start=1
):
    line = raw_line.strip()
    if not line or line.startswith("#"):
        continue
    key, separator, raw_value = line.partition("=")
    if not separator or not key_pattern.fullmatch(key) or key not in allowed_keys:
        raise SystemExit(f"invalid credential assignment at line {line_number}")
    if key in values:
        raise SystemExit(f"duplicate credential key at line {line_number}")
    raw_value = raw_value.strip()
    if not raw_value:
        raise SystemExit(f"empty credential value at line {line_number}")
    if raw_value[0] in {"'", '"'}:
        try:
            value = ast.literal_eval(raw_value)
        except (SyntaxError, ValueError):
            raise SystemExit(f"invalid quoted value at line {line_number}")
        if not isinstance(value, str) or not value:
            raise SystemExit(f"invalid credential value at line {line_number}")
    else:
        if any(character.isspace() for character in raw_value):
            raise SystemExit(f"unquoted whitespace at line {line_number}")
        value = raw_value
    values[key] = value

missing = sorted(allowed_keys - values.keys())
if missing:
    raise SystemExit("missing required credential keys: " + ", ".join(missing))

environment = {
    key: value
    for key, value in os.environ.items()
    if key in passthrough_keys or key.startswith("LC_")
}
environment.update(values)
environment["TRANSLATION_MODEL"] = model

raise SystemExit(
    subprocess.run(
        command,
        cwd=working_directory,
        env=environment,
        check=False,
    ).returncode
)
```

저장 경로는 다음으로 고정한다.

```bash
credential_runner="$review_root/credential_runner.py"
chmod 700 "$credential_runner"
python3 -m py_compile "$credential_runner"
```

### A.4 `act` dry-run과 Docker image/provider gate

원본 workflow에는 commit/push/deploy step이 있으므로 `act`는 dry-run으로만 사용한다.

```bash
(
  cd "$base_checkout"
  act workflow_dispatch \
    --dryrun \
    -W .github/workflows/sync-translation.yml \
    --input version=13.x \
    --input doc=ai-sdk.md
)
```

`act` 실실행, `gh workflow run`, commit/push step 실행은 금지한다. `dot_env`를 `--secret-file`, `--env-file` 또는 다른 방식으로 `act`에 전달하지 않는다.

`dot_env`가 없는 깨끗한 base clone만 Docker build context로 사용한다.

```bash
translation_image="laravel-docs-translation-validation:645a2d4"
site_image="laravel-docs-site-validation:645a2d4"

docker build \
  -f "$base_checkout/Dockerfile.translate" \
  -t "$translation_image" \
  "$base_checkout"

docker build \
  -f "$base_checkout/Dockerfile" \
  -t "$site_image" \
  "$base_checkout"
```

이미지 빌드 후 결정적 gate를 실행한다. 사이트 이미지에는 `Makefile`이 없으므로 `make site-check`가 정의한 네 단계를 직접 실행한다.

```bash
docker run --rm "$translation_image" \
  env PYTHONPATH=. uv run --frozen --python 3.14 \
    python -m unittest discover -s tests

(
  cd "$base_checkout"
  UV_CACHE_DIR="$review_root/uv-cache" make translation-artifact-check
  git diff --check HEAD^...HEAD
)

docker run --rm "$site_image" sh -lc '
  npm run test:markdown-links &&
  npm run typecheck -- --pretty false &&
  npm run build &&
  npm run validate-anchors
'
```

두 모델의 provider contract를 각각 한 번 실행한다. `-e KEY`에는 값이 아니라 key 이름만 전달하며, Docker CLI가 strict runner의 environment에서 값을 전달한다.

```bash
provider_status=0
for model in gpt-5.4-mini gpt-5.6-luna; do
  if ! python3 "$credential_runner" \
      "$credential_file" \
      "$base_checkout" \
      "$model" \
      docker run --rm \
        -e TRANSLATION_PROVIDER \
        -e TRANSLATION_MODEL \
        -e TRANSLATION_REASONING_EFFORT \
        -e OPENAI_API_KEY \
        "$translation_image" \
        uv run --frozen --python 3.14 python provider_check.py \
        >"$review_root/logs/provider-${model}.log" 2>&1; then
    provider_status=1
  fi
done
test "$provider_status" -eq 0
```

각 log는 KO와 JA 모두 성공했는지만 확인한다. API key나 전체 environment를 출력하지 않는다.

### A.5 모델별 3회 독립 end-to-end 실행

총 6개의 독립 checkout을 사용한다. 각 run은 같은 HEAD와 같은 부모 기준본에서 시작한다.

```bash
translation_status=0
for model in gpt-5.4-mini gpt-5.6-luna; do
  for run_number in 1 2 3; do
    run_checkout="$review_root/runs/${model}/run-${run_number}"
    run_log="$review_root/logs/${model}-run-${run_number}.log"

    mkdir -p "$(dirname "$run_checkout")"
    git clone --no-hardlinks "$project_root" "$run_checkout"
    git -C "$run_checkout" checkout --detach 645a2d4

    git -C "$run_checkout" restore --source=HEAD^ -- \
      i18n/en/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md \
      versioned_docs/version-13.x/ai-sdk.md \
      i18n/ja/docusaurus-plugin-content-docs/version-13.x/ai-sdk.md

    if ! python3 "$credential_runner" \
        "$credential_file" \
        "$run_checkout" \
        "$model" \
        docker run --rm \
          -e TRANSLATION_PROVIDER \
          -e TRANSLATION_MODEL \
          -e TRANSLATION_REASONING_EFFORT \
          -e OPENAI_API_KEY \
          -e TRANSLATION_UPSTREAM_MANIFEST=/app/.git/translation-upstream-refs.json \
          -v "$run_checkout/.git:/app/.git" \
          -v "$run_checkout/i18n:/app/i18n" \
          -v "$run_checkout/versioned_docs:/app/versioned_docs" \
          -v "$run_checkout/versioned_sidebars:/app/versioned_sidebars" \
          "$translation_image" \
          uv run --frozen --python 3.14 \
            python main.py --fail-fast --version 13.x --doc ai-sdk.md \
          >"$run_log" 2>&1; then
      translation_status=1
    fi

    if ! rg -q '^translating: ko ' "$run_log" ||
       ! rg -q '^translating: ja ' "$run_log" ||
       ! rg -q '^translated 1 doc\(s\) into ko, ja$' "$run_log"; then
      translation_status=1
    fi
  done
done
test "$translation_status" -eq 0
```

각 run은 다음 조건을 모두 만족해야 성공이다.

1. 종료 코드 `0`
2. KO와 JA가 모두 실제 번역됨
3. `translated 1 doc(s) into ko, ja` 출력
4. `make translation-artifact-check` 통과
5. `git diff --check` 통과
6. Docker 이미지에서 `make site-check`와 동등한 네 개의 npm 단계 통과
7. KO/JA diff에 누락, 영어 본문 잔존, 중대한 오역, 링크·앵커·코드·Markdown 손상 없음

각 checkout에서 다음 후속 gate를 실행한다.

```bash
gate_status=0
for model in gpt-5.4-mini gpt-5.6-luna; do
  for run_number in 1 2 3; do
    run_checkout="$review_root/runs/${model}/run-${run_number}"

    if ! docker run --rm \
        -v "$run_checkout/i18n:/app/i18n" \
        -v "$run_checkout/versioned_docs:/app/versioned_docs" \
        -v "$run_checkout/versioned_sidebars:/app/versioned_sidebars" \
        "$site_image" \
        sh -lc '
          npm run test:markdown-links &&
          npm run typecheck -- --pretty false &&
          npm run build &&
          npm run validate-anchors
        '; then
      gate_status=1
    fi

    if ! (
      cd "$run_checkout"
      UV_CACHE_DIR="$review_root/uv-cache" make translation-artifact-check
      git diff --check
    ); then
      gate_status=1
    fi
  done
done
test "$gate_status" -eq 0
```

### A.6 run별 no-op 재실행

각 성공 checkout에서 같은 model과 동일 manifest로 main 명령을 한 번 더 실행한다. 두 번째 실행은 성공 횟수에 포함하지 않는다.

```bash
noop_status=0
for model in gpt-5.4-mini gpt-5.6-luna; do
  for run_number in 1 2 3; do
    run_checkout="$review_root/runs/${model}/run-${run_number}"
    noop_log="$review_root/logs/${model}-run-${run_number}-noop.log"
    before_hash="$(
      git -C "$run_checkout" diff --binary | shasum -a 256 | awk '{print $1}'
    )"

    if ! python3 "$credential_runner" \
        "$credential_file" \
        "$run_checkout" \
        "$model" \
        docker run --rm \
          -e TRANSLATION_PROVIDER \
          -e TRANSLATION_MODEL \
          -e TRANSLATION_REASONING_EFFORT \
          -e OPENAI_API_KEY \
          -e TRANSLATION_UPSTREAM_MANIFEST=/app/.git/translation-upstream-refs.json \
          -v "$run_checkout/.git:/app/.git" \
          -v "$run_checkout/i18n:/app/i18n" \
          -v "$run_checkout/versioned_docs:/app/versioned_docs" \
          -v "$run_checkout/versioned_sidebars:/app/versioned_sidebars" \
          "$translation_image" \
          uv run --frozen --python 3.14 \
            python main.py --fail-fast --version 13.x --doc ai-sdk.md \
          >"$noop_log" 2>&1; then
      noop_status=1
    fi

    after_hash="$(
      git -C "$run_checkout" diff --binary | shasum -a 256 | awk '{print $1}'
    )"
    if [ "$before_hash" != "$after_hash" ]; then
      noop_status=1
    fi
    if ! rg -q 'no source changes to translate' "$noop_log"; then
      noop_status=1
    fi
    if rg -q '^translating:' "$noop_log"; then
      noop_status=1
    fi
  done
done
test "$noop_status" -eq 0
```

완료 조건:

- `no source changes to translate`
- provider 재호출 없음
- 첫 실행 후 diff hash와 재실행 후 diff hash가 동일
- 새로운 변경 경로 없음

추가 diff 또는 provider 재호출이 발생하면 해당 run은 실패다.

### A.7 최종 완료 판정

다음이 모두 충족돼야 검증 완료다.

- `gpt-5.4-mini`: 3/3 성공
- `gpt-5.6-luna`: 3/3 성공
- 총 6개 run의 artifact/site/diff gate 통과
- 총 6개 run의 no-op 재실행 통과
- 활성 브랜치에 commit 0건, push 0건
- 변경은 프로젝트 내부 `.review`와 검증 보고서에만 존재

한 번이라도 실패하면 원인을 기록하고 **검증 미완료**로 판정한다. 성공할 때까지 임의로 재시도해 실패 표본을 지우지 않는다. 사소한 말투·문체 차이는 실패가 아니지만, 누락·중대한 오역·영어 잔존·구조 손상은 실패다.

---

## 부록 B. 명령 요약

| 목적 | 명령 |
|---|---|
| Python 단위 테스트 | `make translation-test` |
| replay 검증 | 관련 단위 테스트와 `replay.py` 코드 검토 (`git commit` 금지로 실제 replay 미실행) |
| workflow 구조 검증 | `act workflow_dispatch --dryrun` |
| 산출 경로 범위 검사 | `make translation-artifact-check` |
| Markdown 링크 유틸 테스트 | `make site-test` |
| typecheck + build + anchor 검증 | `make site-check` |
| Docker image 검증 | 부록 A.4 |
| 두 모델 provider 응답 계약 | 부록 A.4 strict runner |
| 두 모델 × 3회 실제 문서 번역 | 부록 A.5~A.7 |

고정 표본: `VERSION=13.x`, `DOC=ai-sdk.md`. 모델: `gpt-5.4-mini`, `gpt-5.6-luna`.

---

## 부록 C. 참고 — 커밋 분할

`645a2d4`는 `refact: temp`라는 임시 커밋으로, 파이프라인 코드·문서·번역 산출물·CI 설정이 한 덩어리에 들어 있다. 검증 결과 보고 시 **분할 가능한 경계**(예: 파이프라인 코드 / 기획 문서 / 번역 산출물 / CI 설정)를 한 줄로 제안한다. 다만 커밋 분할 자체는 이 검증의 목표가 아니므로 이를 근거로 finding을 만들지 않는다.
