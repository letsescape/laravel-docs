# 번역 동기화 워크플로우 총괄 설계

## 요약

실행 시작 시 승인 기준본을 고정하고, 동일한 upstream manifest로 replay와 live provider 계약을 확인한다. 이후 모든 산출물을 격리된 candidate snapshot에서 생성·검증하며, 검증된 candidate tree와 정확히 같은 tree만 실행 브랜치에 반영한다.

## 흐름도

```mermaid
flowchart TD
    A([동기화 시작]) --> B[승인 기준본 및 단위 테스트 확정]
    B --> C[Identity replay 및 manifest 확정]
    C --> D{동일 SHA 2차 replay가 no-op인가?}
    D -- 아니요 --> X[Candidate 폐기 및 실행 실패]
    D -- 예 --> E[Live provider fixture 계약 검사]
    E --> F[동일 manifest로 candidate 원문 동기화]
    F --> G[파일 상태 분류 및 전처리]
    G --> H[Effective delta 및 PatchPlan 생성]
    H --> I[번역 및 후처리]
    I --> J[문서 검증 및 candidate 적재]
    J --> K[Candidate sidebar 생성 및 검증]
    K --> L[Candidate 사이트·경로 검증 및 tree 봉인]
    L --> M[검증된 tree를 실행 브랜치에 반영]
    M --> O{Main 실행인가?}
    O -- 아니요 --> N([동기화 완료])
    O -- 예 --> P[배포 trigger 및 재검증 대기]
    P --> Q{성공했는가?}
    Q -- 예 --> N
    Q -- 아니요 --> Y[Published commit 유지 및 실행 실패]
```

그림에서 생략한 모든 단계의 실패 경로는 candidate 폐기와 실행 실패로 수렴하며, 후속 단계로 진행하지 않는다.

## 1. 목적

번역 동기화 워크플로우의 전체 단계 순서, 실패 시 회귀 경로, git 반영 조건을 규범적으로 정의한다.

## 2. 범위

이 문서는 다음만 소유한다.

- 동기화 단계의 실행 순서와 의존 관계
- 실패 시 회귀 단계의 결정 규칙
- 산출물의 git 반영 조건

단계별 세부 설계는 각 단계 문서가 소유한다.

| 순서 | 단계 | 기준 문서 |
|---:|------|----------|
| 0 | 승인 기준본 고정·원문 동기화·파일 상태 분류 | 이 문서의 실행 상태 모델 |
| 1 | 전처리 | [01-preprocessing.md](01-preprocessing.md) |
| 2 | effective delta·변경 계획·번역 | [02-translation.md](02-translation.md) |
| 3 | 후처리 | [03-postprocessing.md](03-postprocessing.md) |
| 4 | 문서 검증 | [04-verification.md](04-verification.md) |
| 5 | 사이드바 갱신·검증 | [06-sidebar-sync.md](06-sidebar-sync.md) |
| 6 | 사이트·산출 경로 검증 | [05-additional-work.md](05-additional-work.md) |
| 7 | git 반영 | [05-additional-work.md](05-additional-work.md) |

오류 분류와 복구 정책은 [08-error-cases.md](08-error-cases.md)가 소유한다.

## 3. 입력

| 항목 | 설명 |
|------|------|
| upstream 원문 저장소 | 버전별 영어 Markdown 원문 |
| upstream manifest | 버전별 commit SHA를 기록한 JSON |
| 기존 locale 문서 | 한국어·일본어 번역 문서 |
| 승인 기준본 | clean publication checkout의 실행 시작 `HEAD` tree와 원격 branch ref |
| `versions.json` | 처리 대상 버전 목록 |
| `documentation.md` | 버전별 사이드바 기준 원문 |
| 번역 프롬프트 | locale별 번역 지침 |
| workflow 설정 | shell 문자열이 아닌 `unit_test_command` argv 배열, provider request budget과 양의 정수 `workflow_timeout_seconds` |
| stale-link registry | version-controlled `translation-sync/stale-links.json` |
| VERSION / DOC selector | 선택적 처리 범위를 canonical 상대 경로와 version 값으로 정규화한 selector |

## 4. 출력

| 항목 | 설명 |
|------|------|
| 갱신된 영어 원문 캐시 | manifest SHA 기준으로 동기화된 원문 |
| 갱신된 locale 문서 | 변경 diff가 반영된 한국어·일본어 문서 |
| 갱신된 사이드바 JSON | `documentation.md` 기준으로 재생성된 sidebar |
| 검증된 candidate tree | 모든 검증을 통과한 파일 집합과 tree 식별자 |
| 실행 브랜치 커밋 | 모든 검증을 통과한 변경분 |
| 배포 결과 | `main` 실행의 trigger와 배포 측 재검증 결과 |

## 5. 불변 조건

1. 단계는 정해진 순서대로 실행해야 한다. 순서를 건너뛰거나 역행해서는 안 된다.
2. 한 target의 실패는 현재 단계를 실패시키며, 실패한 단계의 후속 단계는 실행해서는 안 된다.
3. candidate snapshot은 active worktree와 분리해야 하며, 최종 publication 전에는 실행 브랜치의 파일·index·HEAD를 변경해서는 안 된다.
4. 이전 영어 원문은 승인 기준본에서만 읽고, 현재 raw 영어 원문은 manifest SHA로 동기화한 candidate에서만 읽어야 한다.
5. 같은 워크플로우 실행에서 replay와 live 실행은 동일한 upstream manifest SHA와 정규화된 VERSION / DOC selector를 사용해야 한다.
6. 검증된 candidate tree와 다른 tree를 커밋하거나 push해서는 안 된다.
7. 실패한 candidate는 publication하지 않는다. 원인 수정 후에는 새 승인 기준본을 고정하여 전체 워크플로우를 다시 실행해야 한다.
8. publication 가능한 live 실행은 시작 시 tracked worktree와 index가 `HEAD`와 같고 동기화 소유 경로에 non-ignored untracked 파일이 없어야 한다. dirty worktree 검증은 격리 replay만 허용한다.
9. entrypoint 시작부터 배포 trigger 결과까지의 wall-clock은 `workflow_timeout_seconds`를 넘겨서는 안 된다. 각 subprocess는 남은 전체 예산보다 긴 timeout으로 시작해서는 안 된다.

## 6. 단계 순서

```text
승인 기준본·단위 테스트 확정 → identity replay·upstream SHA manifest 확정 → 같은 SHA 2차 replay(새 프로세스 수렴 확인) → live provider fixture 계약 검사 → 동일 manifest로 candidate 원문 동기화 → 파일 상태 분류 → 이전·현재 원문 전처리 → effective delta·변경 계획 생성 → 소유 단위 번역·후처리 → locale 문서 검증 및 candidate 적재 → candidate sidebar 생성·검증 → candidate 사이트·산출 경로 검증 → candidate tree 봉인 → 실행 브랜치 반영 → main이면 배포 trigger·재검증 결과 대기
```

`단위 테스트 확정`은 workflow 설정의 `unit_test_command` argv를 shell interpolation 없이 승인 기준본에서 분기한 격리 checkout의 저장소 root에서 실행하여 종료 코드 `0`을 확인하고, 실행 전후 tracked source fingerprint가 같음을 확인하는 것을 뜻한다. 명령이 없거나 빈 argv이거나 source를 변경하면 설정 오류로, 명령이 비정상 종료하면 검증 오류로 실패한다.

`candidate sync core`는 고정 manifest 원문 동기화부터 파일 상태 분류, 전처리, 계획·번역·후처리, 문서·sidebar·사이트·산출 경로 검증과 tree 봉인까지의 공통 내부 실행이다. 외부 orchestration의 승인 기준본·단위 테스트 확정, identity replay 호출, live fixture, 원격 publication과 배포 trigger는 포함하지 않는다. Replay와 live는 provider profile만 달리하여 같은 core를 호출해야 한다.

전체 workflow deadline은 entrypoint 진입 시 단조 시계로 계산한다. deadline이 지나면 새 단계·provider 호출·publication을 시작하지 않으며, 실행 중 subprocess에는 남은 시간으로 강제 timeout을 설정한다. publication 뒤 deadline 초과는 이미 공개된 commit을 되돌리지 않고 실패 보고서만 남긴다.

### 6.1 실행 상태 모델

| 상태 | 의미 |
|------|------|
| 승인 기준본 | candidate sync core의 clean 시작 `HEAD`와 tree. Live는 원격 실행 branch ref도 포함하고 replay는 원격 ref를 적용하지 않음 |
| 이전 영어 원문 | 승인 기준본의 영어 원문 캐시 byte. delta의 old side |
| 현재 raw 영어 원문 | manifest commit에서 읽어 candidate에 저장할 upstream byte. delta의 new side이자 publication 대상 |
| 정규화된 영어 작업 사본 | 이전·현재 raw 원문에 전처리를 적용한 임시 비교 입력. publication 대상이 아님 |
| 영어 verification view | 현재 raw 원문에 결정적 source-side 후처리를 적용한 최종 구조 검증 기준. pipeline annotation과 locale 번역문은 포함하지 않음 |
| expected annotation map | 현재 정규화 영어 작업 사본에서 구조 주소별 canonical pipeline annotation을 파생한 검증 기준 |
| candidate snapshot | 승인 기준본에서 분기하여 원문·locale·sidebar 변경을 누적하는 격리 snapshot |
| verified tree | 문서·sidebar·사이트·산출 경로 검증을 모두 통과하여 식별자가 봉인된 candidate tree |
| published tree | verified tree와 동일함이 확인된 실행 브랜치 commit tree |

`기록` 또는 `적재`는 candidate snapshot 갱신을 뜻한다. `publication` 또는 `반영`만 실행 브랜치와 원격 저장소를 변경한다.

### 6.2 원문 동기화와 파일 상태

manifest 기준 현재 원문과 승인 기준본의 영어 원문 캐시를 경로별로 비교하여 다음과 같이 처리한다.

| 상태 | 처리 |
|------|------|
| 추가 (`A`) | 이전 원문과 locale 파일이 없는 상태를 요구한다. 현재 원문 전체를 create 계획으로 번역해 KO·JA 문서를 생성한다. |
| 수정 (`M`) | 승인 기준본의 이전 원문과 기존 KO·JA 문서가 모두 존재해야 한다. 이전·현재 원문으로 effective delta를 계산한다. |
| 삭제 (`D`) | 승인 기준본의 영어·KO·JA 파일이 모두 존재해야 한다. provider 호출 없이 candidate에서 세 파일을 삭제한다. |
| rename | 삭제와 추가의 조합으로 처리한다. 추가 경로는 전체 문서 번역을 수행하며 기존 locale 번역을 추정 재사용하지 않는다. |

원문 정규화 결과 effective delta가 비어 있어도 현재 raw 영어 원문 갱신은 candidate에 유지한다. 이 경우 locale byte가 변경되지 않더라도 영어 verification view와 expected annotation map 기준의 전체 문서 검증을 통과해야 한다.

### 6.3 Candidate publication

1. 각 locale 문서는 문서 검증을 통과한 뒤에만 candidate snapshot에 적재한다.
2. sidebar는 모든 대상 버전의 candidate 산출 검증이 끝난 뒤 candidate snapshot에 한 번에 적재한다.
3. 완성된 candidate snapshot을 [전체 운영 및 산출 검증 단계](05-additional-work.md)에 전달한다.
4. 해당 단계가 verified tree 식별자와 publication 성공을 함께 반환한 경우에만 원격 반영이 완료된 것으로 판정한다.
5. 검증 또는 publication 실패 결과를 받은 candidate는 원격 branch에 반영하지 않는다.

## 7. 회귀 규칙

실패 시 자동 회귀 루프를 수행하지 않는다. 아래 표는 원인을 수정하고 재검증해야 할 소유 단계를 나타낸다. candidate는 publication하지 않으며, 수정 후 새 실행은 승인 기준본 고정 단계부터 다시 시작한다.

| 실패 발생 단계 | 실패 원인 | 수정·재검증 소유 단계 |
|---------------|-----------|----------------------|
| 검증 | 전처리 누락 | 전처리 |
| 검증 | 구조 손상 응답·번역 누락 | 번역 |
| 검증 | 후처리 형식 오류 | 후처리 |
| 검증 | 사이드바 항목 누락·라벨 불일치·locale sidebar JSON 잔존 | 사이드바 갱신 |
| 최종 산출 | 산출 기준 미달 | 검증 |
| 배포 | trigger 또는 배포 측 재검증 실패 | 전체 운영 및 산출 검증 |
| publication 후 운영 검토 | published 문서의 의미 오류·누락 등 콘텐츠 결함 | 전체 운영 및 산출 검증의 publication 후 콘텐츠 복구 |

회귀 원칙:

- provider transport와 response feedback 재시도만 동일 실행 안에서 허용한다.
- 그 밖의 사전 publication 실패는 candidate를 반영하지 않고 실행을 종료한다.
- 배포 단계 실패는 published commit을 유지하고, 해당 commit을 새 승인 기준본으로 하는 no-change 전체 실행에서 배포 경로를 다시 수행한다.
- published tree 자체에 콘텐츠 결함이 있으면 같은 commit의 배포 재시도를 사용하지 않는다. [05-additional-work.md](05-additional-work.md)의 publication 후 콘텐츠 복구 절차로 검증된 revert commit을 먼저 publication한다.
- 원인 수정 후에는 전체 워크플로우를 새로 실행하며, 고정된 입력이 다른 실행의 중간 산출물과 섞이지 않게 한다.

### 7.1 provider 재시도 경계

동일 블록의 provider 응답 평가는 최초 요청을 포함하여 최대 2회까지 수행할 수 있다. 각 평가의 transport 호출은 일시 오류에 한해 최대 3회 시도할 수 있다. 따라서 블록당 물리 provider 호출 상한은 6회다.

## 8. git 반영 조건

git publication 규칙의 유일한 소유자는 [05-additional-work.md](05-additional-work.md)의 `git 반영 세부 규칙`이다. 총괄 단계는 해당 문서가 반환한 verified tree 식별자와 publication 결과만 소비하며 별도의 반영 규칙을 정의하지 않는다.

## 9. 수용 기준

- 모든 단계가 정의된 순서대로 실행되고 있음을 확인할 수 있어야 한다.
- 실패 시 정확한 회귀 대상 단계를 식별할 수 있어야 한다.
- [05-additional-work.md](05-additional-work.md)의 publication 수용 기준을 만족하지 않는 원격 branch 갱신이 존재해서는 안 된다.
- replay 결과의 manifest digest·정규화 selector가 후속 live core 입력과 같아야 한다.
- 추가·수정·삭제·rename의 입력 전제와 candidate 산출 상태를 경로별로 판정할 수 있어야 한다.
- 승인 기준본, verified candidate tree, publication commit tree의 식별자를 대조할 수 있어야 한다.
- 모든 단계와 배포 결과가 하나의 `workflow_timeout_seconds` deadline을 공유해야 한다.
- `main` 실행은 배포 trigger와 배포 측 재검증 결과가 성공해야 완료로 판정되어야 한다.
