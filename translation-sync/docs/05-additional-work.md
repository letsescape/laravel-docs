# 전체 운영 및 산출 검증 설계

## 요약

완성된 candidate snapshot에서 사이트 빌드와 허용 경로·상태 정합성을 검증하고 tree 식별자를 봉인한다. publication commit은 이 verified tree를 정확히 참조해야 하며, `main` 실행 결과만 별도 배포 단계로 전달한다.

## 흐름도

```mermaid
flowchart TD
    A([Candidate 산출 검증 시작]) --> B[링크 유틸리티 테스트]
    B --> C[타입 검사]
    C --> D[Docusaurus 빌드]
    D --> E[Fragment link 검증]
    E --> F[허용 경로 및 상태 정합성 검증]
    F --> G{모든 검증을 통과했는가?}
    G -- 아니요 --> X[Candidate 폐기 및 publication 금지]
    G -- 예 --> H[Candidate tree 식별자 봉인]
    H --> I{변경분이 있는가?}
    I -- 예 --> J[HEAD 재확인 및 verified tree commit]
    I -- 아니요 --> K[HEAD·원격 ref 재확인 후 빈 커밋 생략]
    J --> L{Commit tree가 verified tree와 같은가?}
    L -- 아니요 --> X
    L -- 예 --> M[Push credential 설정 및 원격 ref CAS]
    M --> N{Main 실행인가?}
    K --> N
    N -- 예 --> O[배포 워크플로우 트리거 및 재검증 대기]
    N -- 아니요 --> P([완료])
    O --> Q{배포 검증이 통과했는가?}
    Q -- 예 --> P
    Q -- 아니요 --> R[Published commit 유지 및 산출 실패 보고]
```

## 1. 목적

번역 동기화의 사이트 빌드 검증, 산출 경로 검증, git 반영 규칙을 규범적으로 정의한다.

## 2. 범위

이 문서는 다음만 소유한다.

- 사이트 빌드 검증 기준
- 산출 경로 허용 범위 검증 기준
- git 반영 세부 규칙
- `main` publication 뒤 배포 trigger·재검증 결과 처리

이 문서의 원격 publication 규칙은 live 실행에 적용한다. Replay는 [07-local-replay.md](07-local-replay.md)에 따라 verified tree를 sandbox 내부 commit으로만 연결하고 push와 배포를 금지한다.

단계별 전처리·번역·후처리·문서 검증·사이드바 설계는 각 단계 문서가 소유한다.

| 단계 | 기준 문서 |
|------|----------|
| 전처리 | [01-preprocessing.md](01-preprocessing.md) |
| 번역 | [02-translation.md](02-translation.md) |
| 후처리 | [03-postprocessing.md](03-postprocessing.md) |
| 문서 검증 | [04-verification.md](04-verification.md) |
| 사이드바 갱신·검증 | [06-sidebar-sync.md](06-sidebar-sync.md) |
| 전체 순서·회귀 | [00-workflow-summary.md](00-workflow-summary.md) |
| 로컬 replay | [07-local-replay.md](07-local-replay.md) |
| 오류 분류·복구 | [08-error-cases.md](08-error-cases.md) |

## 3. 입력

| 항목 | 설명 |
|------|------|
| candidate snapshot | 문서 검증을 통과한 locale artifact와 검증된 sidebar candidate가 적재된 격리 파일 집합 |
| candidate 사이트 소스 | 승인 기준본의 Docusaurus 프로젝트 전체에 candidate 변경을 적용한 소스 |
| 승인 기준본 식별자 | 실행 시작 시 고정한 base `HEAD`, tree, clean checkout fingerprint와 원격 branch ref |
| 전체 workflow deadline | entrypoint 시작 시 확정한 단조 시계 deadline |

## 4. 출력

| 항목 | 설명 |
|------|------|
| 사이트 검증 통과 여부 | 빌드·링크·타입·fragment 검증 결과 |
| 산출 경로 검증 통과 여부 | 허용 범위 안의 변경만 존재하는지 여부 |
| verified tree 식별자 | 모든 검증이 끝난 candidate tree의 불변 식별자 |
| 실행 브랜치 커밋 | 변경분과 모든 사전 publication 검증이 있을 때만 생성되는 커밋. no-change 성공이면 없음 |
| 배포 결과 | `main`이면 trigger와 배포 측 재검증의 최종 성공·실패, 그 외 branch면 적용 불가 |

## 5. 불변 조건

1. 사이트 검증과 산출 경로 검증을 모두 통과하지 않으면 커밋해서는 안 된다.
2. 번역 동기화 범위 밖 파일을 변경해서는 안 된다.
3. 문서 변경이 있으면 영어 원문 캐시 변경이 반드시 함께 있어야 한다.
4. locale sidebar override JSON은 삭제 상태만 허용해야 한다. 생성이나 수정을 허용해서는 안 된다.
5. 사이트 UI 번역 파일(`code.json`)은 이 검증의 삭제·수정 대상이 아니다.
6. 사이트·산출 경로 검증 중 active worktree, index와 실행 브랜치 `HEAD`를 변경해서는 안 된다.
7. publication commit tree는 verified tree 식별자와 정확히 일치해야 한다.
8. 테스트·빌드의 cache와 생성 산출물은 candidate source tree 밖에 기록하거나 tree 봉인 전에 폐기해야 한다. 검증 명령이 tracked candidate source를 변경하면 실패해야 한다.
9. 각 검증 subprocess와 배포 결과 대기는 남은 전체 workflow deadline을 넘겨서는 안 된다.

## 6. 사이트 빌드 검증

사이트 검증은 active worktree가 아닌 candidate snapshot의 격리 checkout에서 다음 항목을 순서대로 확인해야 한다.

1. Markdown 링크 유틸리티 단위 테스트를 통과해야 한다.
2. 타입 검사를 통과해야 한다.
3. Docusaurus 빌드를 통과해야 한다.
4. 한국어·일본어 문서의 inline Markdown fragment link가 가리키는 빌드 산출물 HTML과 `id`가 존재해야 한다.
5. 검증 전후 candidate source fingerprint가 같아야 한다. 빌드 도구가 source를 변경한 경우 검증 실패로 처리해야 한다.

fragment 없는 route, reference-style link, 일반 HTML `href`는 이 자동 검사 범위에 포함하지 않는다.

## 7. 산출 경로 검증

승인 기준본과 candidate snapshot의 diff를 비교하여 동기화 실행이 변경할 수 있는 경로를 다음으로 제한해야 한다.

### 7.1 허용 경로

| 경로 분류 | 허용 상태 |
|-----------|-----------|
| 영어 원문 캐시 | 추가·수정·삭제 |
| 한국어 문서 | 추가·수정·삭제 |
| 일본어 문서 | 추가·수정·삭제 |
| 공통 versioned sidebar JSON | 추가·수정 |
| locale sidebar override JSON | 삭제만 |

### 7.2 상태 정합성 규칙

- 추가(`A`) 또는 삭제(`D`)는 영어·한국어·일본어 세 파일이 모두 동일한 단일 상태여야 한다.
- rename은 삭제 경로의 세 파일 `D`와 추가 경로의 세 파일 `A`로 검증해야 한다.
- 수정(`M`)은 변경 목록에 나타난 locale 파일의 상태가 모두 `M`이어야 한다.
- 수정 시 byte 변경이 없어 목록에서 빠진 locale 파일은, 변경된 영어 원문 기준으로 검증하여 issue가 없음을 증명해야 한다. 증명되지 않은 영어 단독 수정은 거부해야 한다.

### 7.3 금지 사항

- 허용 경로 이외의 파일을 변경해서는 안 된다.
- locale sidebar override JSON을 생성하거나 수정해서는 안 된다.
- 문서 변경 없이 영어 원문만 변경되어서는 안 된다(증명 없는 경우).

## 8. git 반영 세부 규칙

1. 사이트 검증과 산출 경로 검증을 candidate snapshot에서 실행한 뒤 candidate tree 식별자를 봉인해야 한다.
2. publication 직전에 checkout `HEAD`·index·소유 경로 fingerprint가 승인 기준본과 같은지 확인해야 한다.
3. verified tree를 정확히 참조하고 승인 기준본 `HEAD`를 parent로 사용하는, 아직 branch에 연결되지 않은 commit을 구성해야 한다.
4. 생성된 commit의 tree 식별자를 verified tree와 다시 비교해야 한다. 다르면 원격 branch ref를 갱신하거나 push해서는 안 된다.
5. tree 동일성 확인 후 검증된 commit 식별자를 원격 실행 branch로 직접 push하되, 원격 ref가 승인 기준본 값일 때만 compare-and-swap으로 갱신해야 한다.
6. 검증이 실패하거나 publication 전제 조건이 달라지면 원격 실행 branch를 갱신해서는 안 된다.
7. 반영할 변경분이 없으면 빈 커밋을 만들어서는 안 된다.
8. 실행 브랜치에 직접 push해야 한다. Pull Request를 자동 생성해서는 안 된다.
9. checkout은 write credential을 저장해서는 안 된다. 의존성 설치·번역·검증·commit 구성에는 push credential을 노출해서는 안 된다.
10. mutation 가능한 commit hook은 verified tree 봉인 뒤 실행해서는 안 된다. 필요한 hook 검사는 봉인 전에 candidate에서 실행해야 한다.
11. push credential은 commit tree 동일성 확인이 끝난 별도 push 단계에서만 설정해야 한다.
12. push는 원격 branch가 예상한 승인 기준본에서 전진하지 않았을 때만 허용하며, non-fast-forward 또는 lease 실패는 publication 실패로 처리해야 한다. 로컬 active branch ref를 갱신할 필요는 없다.
13. `main` 브랜치 실행일 때만 배포를 트리거해야 한다. commit/push와 배포 트리거는 분리해야 한다.
14. `main`에서는 변경이 없는 재실행도 실행·원격 branch가 승인 기준본과 같음을 확인한 뒤 배포를 트리거하여, push 후 배포 트리거만 실패한 실행을 복구할 수 있어야 한다.
15. 배포 워크플로우도 사이트 검증을 다시 실행해야 한다.
16. branch가 아닌 ref(tag 등)에서의 실행은 초기에 거부해야 한다.
17. `main` 실행은 배포 workflow의 재검증 결과까지 성공해야 전체 성공이다. trigger·재검증 실패 또는 deadline 초과 시 published commit을 되돌리지 않고 산출 실패로 보고해야 한다.

## 9. 실패 정책

- 사이트 또는 산출 경로 검증 실패 시: candidate를 publication하지 않고 워크플로우를 실패로 종료해야 한다.
- 승인 기준본의 checkout 상태나 원격 ref가 달라진 경우: candidate를 덮어쓰지 않고 publication 경쟁 실패로 종료해야 한다.
- commit tree와 verified tree가 다른 경우: push를 금지하고 publication 실패로 종료해야 한다.
- 배포 trigger 또는 배포 측 재검증 실패 시: 이미 공개된 commit은 유지하고 실패 보고서를 남긴다. 해당 commit을 새 승인 기준본으로 사용하는 no-change 실행으로 배포만 다시 시도할 수 있다.
- 사전 publication에 실패한 candidate는 디버깅 목적으로 격리 상태로 보존할 수 있지만 active worktree와 실행 브랜치에는 반영해서는 안 된다.

### 9.1 Publication 이후 콘텐츠 결함 복구

[문서 검증](04-verification.md)의 자동 판정 범위 밖인 번역 의미 오류·용어 오류·누락 등이 published tree에서 뒤늦게 확인되면 배포 실패와 구분되는 콘텐츠 사고로 처리한다.

1. 결함을 처음 도입한 publication commit과 영향받은 version·locale·문서 경로를 확정한다.
2. 원격 branch를 reset하거나 force-push하지 않는다. 현재 원격 branch `HEAD`를 parent로 하여 결함 publication 전체를 되돌리는 revert candidate를 만든다.
3. 후속 publication과 충돌하여 전체 revert를 기계적으로 적용할 수 없으면 자동으로 일부만 되돌리지 않는다. 현재 tree에서 해당 publication의 변경을 완전히 제거하면서 7.2의 상태 정합성 규칙을 만족하는 복구 candidate를 별도 repository review 대상으로 작성한다.
4. 복구 candidate도 일반 candidate와 동일하게 문서·sidebar·사이트·산출 경로 검증을 모두 통과하고 verified tree 식별자를 봉인해야 한다.
5. 8절의 commit tree 동일성 확인과 원격 ref compare-and-swap을 거쳐 복구 commit을 publication한다. `main`이면 복구 commit의 배포 재검증까지 완료해야 한다.
6. 즉시 복구가 끝난 뒤 원인을 수정하고, 복구 commit을 새 승인 기준본으로 하여 전체 동기화를 새로 실행한다. 실패한 과거 candidate나 provider 응답을 재사용해서는 안 된다.

No-change 배포 재시도는 published tree의 내용이 여전히 승인 가능하고 trigger·배포 측 실행만 실패한 경우에만 허용한다. 콘텐츠 결함이 확인된 commit을 같은 내용으로 다시 배포하는 데 사용해서는 안 된다. 성공했던 과거 실행의 종료 코드와 실패 보고서를 소급 변경하지 않으며, 콘텐츠 사고와 복구 commit 식별자는 별도 운영 기록으로 남긴다.

## 10. 수용 기준

- 사이트 빌드·타입 검사·링크 유틸리티·fragment 검증이 모두 통과해야 한다.
- 산출 경로가 허용 범위 안에 있고, 상태 정합성 규칙을 만족해야 한다.
- verified tree 식별자와 publication commit tree 식별자가 같아야 한다.
- publication 직전 checkout과 원격 실행 branch가 승인 기준본에서 변경되지 않았음을 확인할 수 있어야 한다.
- push credential이 검증 및 커밋 단계에 노출되지 않았음을 확인할 수 있어야 한다.
- `main` 실행은 배포 trigger와 배포 측 재검증의 최종 결과까지 확인할 수 있어야 한다.
- 사이트 검증·publication·배포 결과 대기가 같은 전체 workflow deadline 안에서 수행되어야 한다.
- publication 후 콘텐츠 결함은 같은 commit의 배포 재시도와 구분되고, 검증된 revert 또는 복구 commit을 통해서만 되돌릴 수 있어야 한다.
