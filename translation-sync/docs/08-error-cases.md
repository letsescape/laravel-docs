# 오류 처리 설계

## 요약

원문 동기화와 번역 단계는 실패를 숨기지 않고 즉시 종료한다. provider transport와 응답 보정만 정해진 범위에서 재시도한다. 배포 관련 오류는 이 워크플로우에 존재하지 않고, Git 반영 실패는 issue code 없이 잡 실패로만 나타난다.

## 1. 공통 원칙

1. 설정과 선택자 오류는 upstream 조회 전에 실패한다.
2. 원문 동기화 실패 시 번역을 시작하지 않는다.
3. provider 응답이 계약을 통과하지 못하면 제한된 feedback 재요청 뒤 실패한다.
4. 후처리 또는 구조 검증에 실패한 문서는 기록하지 않는다.
5. 한 대상이 실패하면 이후 대상을 처리하지 않는다.
6. 구조화된 실패 이벤트와 선택적 JSON 보고서에서는 인증 정보와 절대 경로를 제거한다. 예상하지 못한 오류의 CLI 진단에는 내부 상세를 출력하지 않는다.
7. 액션의 커밋 단계는 앞 단계가 모두 성공했을 때만 실행된다. 이 단계의 push 실패는 §7의 계약 밖 실패다. 배포를 호출하는 경로는 어디에도 없다.

## 2. 오류 분류

| 코드 | 분류 | 의미 |
|---|---|---|
| `C` | configuration | provider, 인증, 모델, 예산 또는 런타임 설정 오류 |
| `I` | input | 선택자, 원문 상태, diff, manifest 또는 전처리 입력 오류 |
| `P` | plan | 번역 소유 블록과 변경 계획 생성 오류 |
| `T` | translation | provider 요청, 응답 또는 번역 제한 시간 오류 |
| `R` | postprocessing | placeholder·markup 복원과 후처리 오류 |
| `V` | verification | Markdown 구조와 annotation 검증 오류 |
| `S` | sidebar | sidebar 입력·경로·내용 검증 오류 |
| `A` | output | 허용되지 않은 출력 경로 오류 |
| `X` | infrastructure | 실행 환경, 보고서 기록 또는 분류되지 않은 내부 오류 |

## 3. Stable issue code

### 3.1 설정 (`C`)

`PROVIDER_SELECTION_INVALID`, `PROVIDER_CREDENTIAL_MISSING`, `REQUIRED_CONFIG_MISSING`, `STALE_LINK_REGISTRY_INVALID`, `TOKENIZER_METADATA_UNAVAILABLE`, `INVALID_REQUEST_BUDGET`, `INVALID_RUNTIME_OPTION`

### 3.2 입력 (`I`)

`FILE_STATE_CONFLICT`, `RAW_DIFF_MISSING`, `PREPROCESS_PLACEHOLDER_INVALID`, `PREPROCESS_BOUNDARY_AMBIGUOUS`, `INVALID_SELECTOR`, `INVALID_MANIFEST`, `MANIFEST_COMMIT_UNRESOLVED`, `MANIFEST_DIGEST_MISMATCH`, `MANIFEST_EXPORT_CONFLICT`, `STALE_LINK_REGISTRY_CHANGED`

### 3.3 변경 계획 (`P`)

`BLOCK_BOUNDARY_AMBIGUOUS`, `PATCH_LOCATION_AMBIGUOUS`, `ANNOTATION_STATE_INVALID`, `PATCH_RESULT_CARDINALITY_INVALID`, `UNSUPPORTED_OVERSIZE_BLOCK`, `UNSUPPORTED_CHANGE_UNIT`

### 3.4 번역 (`T`)

`PROVIDER_TRANSIENT_EXHAUSTED`, `PROVIDER_REQUEST_REJECTED`, `CLI_PROVIDER_FAILED`, `PROVIDER_PARTIAL_RESPONSE`, `RESPONSE_CONTRACT_FAILED`, `RUN_DEADLINE_EXCEEDED`

운영 Actions는 OpenAI API만 사용한다. `CLI_PROVIDER_FAILED`는 호스트 로컬 실행에서 OpenAI CLI를 선택했을 때의 오류 코드이며 운영 액션이 CLI를 설치하거나 호출한다는 의미가 아니다. 호스트 로컬 실행은 환경 변수로 OpenAI API도 선택할 수 있다.

### 3.5 후처리 (`R`)

`RESTORE_MAP_INVALID`, `MARKUP_RESTORE_AMBIGUOUS`, `POSTPROCESS_RESIDUE`, `VERIFICATION_BASIS_GENERATION_FAILED`, `NO_WRITE_MUTATION`

### 3.6 검증 (`V`)

`RESIDUAL_PATTERN`, `SOURCE_STRUCTURE_MISMATCH`, `LIST_TABLE_STRUCTURE_MISMATCH`, `PIPELINE_ANNOTATION_MISMATCH`, `SOURCE_COMMENT_MISMATCH`, `FRONT_MATTER_MISMATCH`, `VERIFICATION_INPUT_CHANGED`

### 3.7 사이드바 (`S`)

`SIDEBAR_INPUT_INVALID`, `SIDEBAR_DANGLING_DOC`, `SIDEBAR_PATH_INVALID`, `SIDEBAR_CONTENT_MISMATCH`, `SIDEBAR_OVERRIDE_REMAINS`, `SIDEBAR_INPUT_CHANGED`

### 3.8 출력 (`A`)

`OUTPUT_PATH_FORBIDDEN`

### 3.9 인프라 (`X`)

`RUNNER_OPERATION_FAILED`, `REPORT_WRITE_FAILED`, `UNCLASSIFIED_INTERNAL`

## 4. Provider 재시도

- 연결·rate limit·일시적 server 오류만 transport 재시도 대상이다.
- 유효하지만 response contract를 통과하지 못한 응답은 검증 feedback을 포함해 제한 횟수만 재요청한다.
- 인증, 잘못된 요청, 입력 구조와 예산 오류는 재시도하지 않는다.
- 재시도 예산 소진 시 해당 문서를 기록하지 않고 실패한다.

## 5. 실패 보고서

`TRANSLATION_RUN_ID`와 `TRANSLATION_FAILURE_REPORT`가 모두 설정된 경우 `main.py`는 redacted JSON 보고서를 지정 경로에 기록한다. 보고서는 실행 오류를 보조할 뿐 필수 workflow artifact가 아니다.

보고서는 **동기화 실행의 구조화된 실패 경로에만** 적용한다. 알 수 없는 인수, `--doc`을 `--version` 없이 지정한 경우처럼 선택자 파싱 단계에서 끝나는 실패는 구조화된 실패 이벤트를 만들기 전에 진단 메시지와 함께 `1`을 반환하므로 보고서를 남기지 않는다.

주요 필드는 `schema_version`, `run_id`, `stage`, `classification`, `code`, `exit_code`, 문서 문맥, provider 시도 횟수와 정렬된 `issues`다. 원격 commit, 배포 상태 또는 임시 candidate 경로 필드는 사용하지 않는다.

## 6. 복구

- 설정·입력 오류: 값을 수정한 뒤 처음부터 다시 실행한다.
- provider 일시 오류: 내장 재시도 소진 후 새 실행으로 재시도한다.
- 구조 오류: 원문 변경 유형 또는 처리 규칙을 수정하고 테스트한 뒤 다시 실행한다.
- 이미 기록된 앞선 문서: `git diff`로 확인해 유지하거나 호출자가 명시적으로 되돌린다.

번역 코드가 자동으로 Git 변경을 제거하거나 저장하지 않는다.

## 7. 진입점 종료 코드 계약

| 종료 코드 | 의미 |
|---|---|
| `0` | 성공 또는 번역할 유효 변화 없음 |
| `1` | 설정·입력·계획·번역·후처리·검증·사이드바·출력의 통제된 실패 |
| `2` | 실행 환경 또는 예기치 않은 내부 실패 |

Actions, 호스트의 `make translation-run`과 Docker의 `make translate`는 모두 `main.py`의 성공·실패를 전달한다. Make target은 별도 종료 의미를 만들지 않으며, 정확한 `0`·`1`·`2` 구분은 `main.py` 직접 실행의 계약이다.

액션 커밋 단계의 실패는 이 계약 밖이다. 원격이 앞서 있어 갱신이 거부되는 경우처럼 커밋 단계에서 발생한 실패는 issue code 없이 잡 실패로만 나타난다. 이때 로컬 커밋은 이미 만들어진 상태이고 원격 branch에만 반영되지 않으며, 그 커밋은 runner와 함께 폐기된다. 같은 결과를 얻으려면 실행을 다시 수행한다.

## 8. 수용 기준

- 모든 issue code가 정확히 하나의 분류와 종료 의미를 가진다.
- 번역 또는 검증에 실패한 현재 문서는 기록되지 않는다.
- 구조화된 실패 이벤트와 JSON 보고서에서 인증 정보와 절대 경로가 제거된다.
- 오류 처리 코드에 Git 원격 갱신, publication 또는 배포 상태가 없다.
- 운영 진입점이 `0`, `1`, `2`의 의미를 동일하게 사용한다.
