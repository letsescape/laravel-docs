# 로컬 Replay 격리 검증 설계

## 목적

identity provider를 사용하여 격리된 환경에서 번역 동기화 전체 process를 실행하고, pinned source 기준 2회 수렴을 확인함으로써 plan 선택·적용·검증·sidebar 동기화의 결정론적 정합성을 보증한다.

## 범위

- identity 기반 격리 replay의 sandbox 생성·실행·정리를 소유한다.
- upstream manifest lifecycle(생성·snapshot·공유·export)을 소유한다.
- 2회 수렴 검증(두 번째 실행이 변경 없음으로 종료)을 소유한다.
- 번역 의미·문체 품질은 이 단계의 검증 범위가 아니다.
- live provider 응답 계약 검증은 별도 provider 검사 단계가 소유한다.

## 입력

| 항목 | 설명 |
|---|---|
| active repository worktree | tracked 변경 및 untracked 파일 포함 |
| upstream manifest (선택) | pinned upstream commit SHA를 기록한 파일. 존재하면 재사용, 부재하면 생성 |
| VERSION / DOC selector (선택) | 대상 버전·문서 필터 |

## 출력

| 항목 | 설명 |
|---|---|
| 종료 코드 | 수렴 성공(0), sync 실패(1), 인프라 오류(2), worktree 오염(3) |
| upstream manifest (조건부) | 지정 경로에 파일이 없었고 전체 replay 성공 시 export |

## 불변조건

1. **Active worktree 오염 방지**: replay 전체 과정에서 active repository의 HEAD, tracked 내용, staging 상태, Git이 무시하지 않는 untracked 내용이 변경되지 않아야 한다. 시작·종료 fingerprint를 비교하여 위반 시 종료 코드 3을 반환한다.
2. **격리 실행**: sandbox는 OS 임시 디렉터리에 생성한 독립 clone이며, active repository 안에 생성할 수 없다. 실행은 system/global Git config를 읽지 않고 prompt를 비활성화한다.
3. **Identity provider 제한**: `TRANSLATION_PROVIDER=identity`는 replay runner가 격리 process에만 설정한다. 일반 실행에서 `TRANSLATION_REPLAY=1` 없이 identity를 사용하면 설정 검증에서 거부된다.
4. **Symlink 안전성**: untracked symlink와 변경된 tracked symlink는 거부한다. 변경되지 않은 tracked symlink는 저장소 내부를 가리킬 때만 허용한다.
5. **Manifest 무결성**: 기존 manifest는 setup 시점에 단일 file descriptor로 snapshot하며, 이후 외부 파일이 변경되어도 실행 중 입력에 영향을 주지 않는다. 새 manifest export는 replay 성공 및 sandbox 삭제 완료 후에만 수행한다.
6. **2회 수렴 계약**: 두 번째 실행은 같은 plan 재적용이 아니라 같은 pinned source에서 새 process가 변경 없음(no-op)으로 수렴하는지 확인한다.

## 처리 순서

```text
1. Active worktree fingerprint 기록 (HEAD, tree hash, staging, untracked)
2. Sandbox 경로 안전성 검증 (active repo 밖, symlink 제한)
3. Active repository를 임시 디렉터리에 독립 clone
4. Tracked 변경 및 untracked 파일을 clone에 복사, baseline commit 생성
5. Upstream manifest 처리:
   a. 기존 파일이면 → snapshot을 sandbox .git 아래에 읽기 전용 복사
   b. 부재하면 → 첫 실행에서 sandbox 내부에 생성
6. 첫 번째 실행: identity provider로 번역 동기화 진입점 실행 → 결과 snapshot 확정
7. 두 번째 실행: 새 process에서 동일 진입점 재실행 → 변경 없음 확인
8. Active worktree fingerprint 재비교 (불일치 시 종료 코드 3)
9. Sandbox 삭제
10. Manifest export (조건부: 지정 경로에 파일이 없었고 전체 성공 시)
```

## 실패 정책

| 상태 | 종료 코드 | 처리 |
|---|---|---|
| KO/JA replay + 두 번째 수렴 성공 | 0 | sandbox 삭제, 조건부 manifest export |
| sandbox 내 translation sync 실패 | 1 | sandbox 보존 (경로 출력) |
| sandbox 준비·실행·정리 오류 | 2 | 불완전 sandbox 정리 또는 보존 |
| active worktree fingerprint 불일치 | 3 | sandbox 보존 (경로 출력) |
| 두 번째 실행에서 변경 발생 | 1 | 수렴 실패로 분류, sandbox 보존 |
| sandbox 경로가 active repo 안 | 2 | clone 전 즉시 거부 |
| manifest 대상이 active repo 안 | 거부 | publication 전 거부 |
| manifest 대상에 이미 파일 존재 | 실패 | no-replace 원칙으로 덮어쓰기 방지 |

## Manifest Lifecycle

```text
┌─ 기존 manifest 있음 ─┐        ┌─ 기존 manifest 없음 ─┐
│ setup에서 FD snapshot │        │ 첫 실행에서 sandbox   │
│ → sandbox .git에 복사 │        │ 내부에 생성           │
│ → 두 실행 모두 사용   │        │ → 두 실행 모두 사용   │
└───────────────────────┘        │ → 전체 성공 + sandbox │
                                 │   삭제 후 외부 export │
                                 └───────────────────────┘
```

Export 조건:
- replay 전체 성공 (종료 코드 0)
- sandbox 삭제 성공
- 외부 경로에 동명 파일 부재 (no-replace)
- 외부 경로가 active repository 밖

## 수용 기준

1. 첫 번째 실행이 identity provider로 plan 선택·적용·검증·sidebar 동기화를 KO/JA 모두 성공적으로 완료한다.
2. 두 번째 실행이 같은 pinned source에서 새 process를 실행했을 때 변경 없음(no-op)으로 수렴한다.
3. 실행 전후 active worktree fingerprint가 동일하다.
4. sandbox가 성공 시 삭제되고, 실패 시 보존되어 디버깅에 사용 가능하다.
5. manifest가 조건을 충족할 때만 export되며, 기존 파일을 덮어쓰지 않는다.

## 종료 상태 의미

| 종료 코드 | 의미 |
|---|---|
| 0 | KO/JA replay, 최종 검증, pinned source 2회 수렴 성공 |
| 1 | sandbox의 translation sync 실패 또는 두 번째 실행에서 변경 발생 |
| 2 | replay 준비·실행·sandbox 정리 오류 |
| 3 | active worktree fingerprint 변경 감지 |

## 부록: Identity Provider의 역할

identity provider는 번역할 영어 source를 그대로 반환한다. 이를 통해 검증하는 것:
- 번역 소유 단위(chunk) 선택의 정확성
- patch 적용 위치의 정확성
- 보존 markup(코드, 링크, 앵커, annotation)의 무결성
- 최종 문서 검증 통과 여부
- sidebar 동기화의 정합성

검증하지 않는 것:
- 번역 의미·문체 품질
- live provider 응답의 wrapper 부재·목표 언어 문자 존재
- 실제 API/CLI 연결성
