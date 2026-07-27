# 로컬 Translation Replay

`translation-check`는 GitHub Actions가 live provider 호출 전에 실행하는 API 키 없는 번역 preflight다. Python 단위 테스트와 `translation-replay`를 순서대로 실행하며 Action과 같이 `uv run --locked`로 lockfile freshness를 확인하고 Python 3.14를 사용한다.

```bash
make translation-check
```

`translation-replay`는 그중 실제 upstream 동기화와 `main.py`의 plan, apply, KO/JA 전체 검증을 격리 환경에서 실행하는 통합 점검 하위 명령이다.

```bash
make translation-replay
```

특정 문서만 확인할 수 있다.

```bash
make translation-replay VERSION=13.x DOC=collections.md
```

`VERSION`과 `DOC`은 서로 독립적인 optional selector다. `VERSION`만 주면 해당 버전의 모든 문서, `DOC`만 주면 모든 지원 버전의 같은 basename, 둘 다 주면 그 한 쌍을 대상으로 한다. `DOC`는 upstream 존재 assertion이 아니다. upstream에 없는 파일은 기존 cache에 있으면 삭제 변경으로 처리되고 cache에도 없으면 sidebar sync 뒤 no-op으로 끝날 수 있다. 필터 실행은 로그와 실제 변경 목록을 확인해야 한다. 문서 필터와 sidebar 범위도 같지 않다. sidebar sync 대상으로 정해진 버전은 cached `documentation.md` 전체로 sidebar를 재생성하고 locale sidebar override를 제거한다.

실행기는 현재 tracked 변경과 Git이 무시하지 않는 untracked 파일을 운영체제의 임시 디렉터리에 만든 독립 clone으로 복사하고 baseline commit을 만든다. 임시 디렉터리(`TMPDIR` 포함)나 명시적 sandbox parent가 active repository 안이면 clone 전에 종료 코드 2로 거부한다. 외부 경로를 따라 쓰지 않도록 untracked symlink와 변경된 tracked symlink는 거부한다. 변경되지 않은 tracked symlink는 저장소 내부를 가리킬 때만 허용하고, 저장소 밖을 가리키면 거부한다. replay용 Git 명령은 system/global config를 읽지 않으며 prompt도 비활성화한다. 그 clone에서 `TRANSLATION_PROVIDER=identity`로 실제 `translation-sync/main.py`를 실행하고 결과를 commit한 뒤 새 프로세스로 한 번 더 실행한다. 두 번째 실행은 같은 PatchPlan을 다시 적용하는 단위 멱등성 검사가 아니라, 같은 pinned source에서 새 diff가 없어 전체 process가 no-op으로 수렴하는지 확인한다. `--fail-fast`를 사용하지 않아 감지된 변경을 한국어와 일본어 모두 검증한다.

명시한 upstream manifest 경로는 child process에 직접 전달하지 않는다. `MANIFEST`에는 절대 경로를 사용해야 한다. 기존 regular file이면 setup 단계에서 final symlink를 따르지 않는 단일 file descriptor로 열고 `fstat`한 snapshot을 sandbox의 `.git` 아래에 읽기 전용 입력으로 복사한다. 없는 경로이면 child가 sandbox 내부 manifest를 생성하고 replay와 active-worktree 시작·종료 상태 비교 및 sandbox 삭제가 모두 성공한 뒤에만 외부 경로에 export한다. 외부 parent는 고정한 directory descriptor를 기준으로 active repository와 inode identity를 다시 검사한다. 완성한 임시 regular file을 `fsync`한 뒤 no-replace link로 최종 이름에 원자적으로 공개하므로 기존 destination은 덮어쓰지 않으며 publication 순간 같은 경로가 존재하면 실패한다. 실행 도중 생겼다가 publication 전에 사라진 destination 이력은 추적하지 않는다.

active repository 내부 경로는 대소문자나 filesystem alias가 달라도 거부한다. 기존 final symlink와 non-regular target은 clone 전에 거부하며, setup 뒤 새로 생기거나 바뀐 ancestor가 active repository를 가리키는 경우도 publication 전에 거부한다. 이미 존재하면서 active repository 밖을 가리키는 ancestor symlink는 canonical 외부 경로로 고정해 허용한다.

이 clone은 active worktree 오염을 막는 실행 격리 장치이지 OS 권한이나 filesystem을 제한하는 보안 sandbox가 아니다. 현재 사용자 권한으로 worktree의 Python 코드를 실행한다. upstream Git clone은 각 시도에 300초 timeout을 두고 최대 3회 시도한다. 그 밖의 replay 하위 명령에는 공통 subprocess timeout이 없으므로 해당 명령이 멈추면 CI job timeout까지 지속될 수 있다.

identity provider는 번역할 영어 source를 그대로 반환한다. 따라서 이 명령은 번역문의 언어 품질이 아니라 번역 소유 단위 선택, patch 적용 위치, 보존 markup, 최종 문서 검증과 sidebar 동기화를 확인한다.

실제 API/CLI 응답의 wrapper, 목표 언어 문자와 구조 계약은 별도 live 게이트인 `make translation-provider-check`가 확인한다. 동기화 workflow는 replay 뒤, 본 번역 전에 이 검사를 KO/JA 모두 실행한다.

GitHub Actions도 live provider를 호출하기 전에 같은 `replay.py`를 실행한다. workflow는 preflight가 기록한 upstream commit manifest 경로를 live 실행에 다시 전달하므로 두 단계가 같은 Laravel 원문 commit을 사용한다. 일반 로컬 `make translation-replay`와 별도의 `make translation-run` 사이에는 manifest가 자동 공유되지 않으며, 같은 SHA가 필요하면 두 명령에 동일한 `MANIFEST` 경로를 명시해야 한다. `identity` provider는 replay runner가 격리 process에 설정하며, 일반 실행에서는 `TRANSLATION_REPLAY=1`이 없으면 설정 검증에서 거부된다. 이는 실수 방지 장치이며 보안 경계는 아니다.

특정 upstream manifest를 재현할 때는 경로를 함께 지정한다.

```bash
make translation-replay VERSION=13.x DOC=collections.md MANIFEST=/path/to/translation-upstream-refs.json
```

지정한 manifest가 이미 존재하면 setup 때 얻은 snapshot의 읽기 전용 사본에서 기록된 SHA를 사용한다. setup 이후 외부 파일이 교체되어도 실행 중 입력은 바뀌지 않는다. 파일이 없으면 현재 upstream 브랜치 SHA를 sandbox 내부에 기록해 첫 실행과 두 번째 실행에 함께 사용하고, 전체 replay 성공과 sandbox 삭제 뒤 지정 경로에 새 파일로 export한다. sandbox 삭제가 실패하거나 중단되면 외부 manifest를 만들지 않는다. sandbox는 active repository를 `git clone --local`로 복제하므로 복제 중 원본 저장소가 동시에 바뀌지 않는다는 로컬 실행 전제가 있다.

API 키가 없어도 이 구조 검증은 실행할 수 있다. OpenAI/Azure 모델의 실제 번역 품질과 응답 안정성은 검증 범위에 포함되지 않는다.

배포 workflow의 사이트 검증까지 로컬에서 함께 실행하려면 `make preflight`를 사용한다. 이 명령은 `translation-check` 뒤에 링크 유틸리티 테스트, 타입 검사, Docusaurus 빌드와 KO/JA inline Markdown fragment target 검증을 실행한다.

성공하면 임시 clone을 삭제한다. 실행 또는 검증이 sandbox 삭제 전에 실패하면 출력된 경로에 clone을 보존한다. clone 준비 자체가 완료되기 전 실패하면 불완전한 임시 디렉터리를 정리한다. active repository fingerprint는 시작과 종료에 비교하므로 그 사이 변경되었다가 정확히 원복된 이력은 감지하지 않는다. 외부 manifest publication은 sandbox를 성공적으로 삭제한 뒤 수행하므로, publication 경쟁이나 filesystem 오류로 종료 코드 2가 되면 clone은 이미 제거된 상태다.

| 종료 코드 | 의미 |
|---|---|
| `0` | KO/JA replay, 최종 검증, pinned source 두 번째 새 프로세스 수렴 확인 성공 |
| `1` | sandbox의 translation sync 실패 |
| `2` | replay 준비, 실행 또는 임시 clone 정리 실패 |
| `3` | 실행 중 active HEAD/tree, tracked 및 Git이 무시하지 않는 untracked worktree 내용 또는 staging 상태가 바뀌었거나, 종료 후 active 상태 조회 명령이 실패함 |
