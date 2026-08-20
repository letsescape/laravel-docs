# 로컬 번역 실행

## 요약

로컬 실행도 운영 액션과 같은 `translation-sync/main.py`를 사용한다. 별도 replay·candidate·publication 단계는 없다.

## 1. 준비

- Python 3.14
- uv
- macOS 또는 Linux 등 POSIX process group을 지원하는 환경
- upstream 조회를 위한 Git과 네트워크
- 선택한 OpenAI provider의 인증 값
- 기록 대상 경로에 커밋되지 않은 변경이 없는 작업 트리

Node와 npm은 번역 실행에 필요하지 않다.

운영 Actions는 OpenAI API를 사용한다. 호스트 로컬 실행은 `TRANSLATION_PROVIDER` 환경 변수로 OpenAI API(`openai`) 또는 OpenAI CLI(`cli`)를 선택한다. API 실행에는 `OPENAI_API_KEY`가 필요하고, CLI 실행에는 [OpenAI CLI adapter 보안 경계](02-translation.md#83-openai-cli-adapter-보안-경계)에 정의된 명령·모델·인증 환경 변수가 필요하다.

### 작업 트리 전제

번역 실행은 영어 원문 캐시, KO·JA 문서, 사이드바를 작업 트리에 직접 덮어쓰고 삭제한다. 기록 직전에 대상 파일의 현재 byte를 다시 확인하지 않으므로, 같은 경로에 커밋되지 않은 편집이 있으면 예고 없이 사라진다.

- 실행 전에 `git status --short -- i18n versioned_docs versioned_sidebars`로 대상 경로가 깨끗한지 확인한다.
- 같은 작업 트리에서 두 실행을 동시에 수행하지 않는다.
- 실행이 중간에 실패하면 앞선 문서와 삭제 결과가 남는다. 같은 명령을 그대로 재실행하기 전에 `git status`로 남은 상태를 확인한다. 삭제까지 진행된 뒤 실패한 경우 재실행에서 `FILE_STATE_CONFLICT`가 발생할 수 있으므로, 그때는 대상 경로를 `git checkout`으로 되돌린 뒤 다시 실행한다.

Actions는 매 실행이 새 checkout이므로 이 전제가 자동으로 성립한다. 로컬과 Docker 실행에서는 호출자가 보장해야 한다.

## 2. 테스트

```bash
make translation-test
```

또는 다음 명령을 직접 실행한다.

```bash
uv run --directory translation-sync --locked --python 3.14 \
  python -m unittest discover -s tests
```

## 3. 로컬 실행

Makefile은 같은 Python 진입점을 실행하는 단순 래퍼다. 저장소 루트의 `.env`가 있으면 Makefile이 그 값을 환경 변수로 넣는다. 이미 설정된 변수는 덮지 않으므로 명령줄에서 준 값이 우선한다. 전체 버전의 변경 문서를 OpenAI API로 처리하는 예시는 다음과 같다.

```bash
TRANSLATION_PROVIDER=openai OPENAI_API_KEY=... make translation-run
```

특정 버전 또는 문서만 처리할 수 있다.

```bash
TRANSLATION_PROVIDER=openai OPENAI_API_KEY=... make translation-run VERSION=13.x
TRANSLATION_PROVIDER=openai OPENAI_API_KEY=... make translation-run VERSION=13.x DOC=collections.md
```

OpenAI CLI를 사용할 때는 `TRANSLATION_PROVIDER=cli`와 CLI adapter에 필요한 환경 변수를 설정한 뒤 같은 `make translation-run`을 실행한다. provider 선택 외에 실행 순서나 결과 기록 방식은 달라지지 않는다.

Docker는 번역 스크립트 전체를 재현 가능한 Python 환경에서 시험하기 위한 로컬 실행 방법이다. `make translate`는 컨테이너 안에서 같은 `main.py`를 호출하며, 원문 동기화·변경 감지·번역·검증·작업 트리 기록을 그대로 수행한다. Docker 전용 동기화 로직은 없다. Docker 테스트는 OpenAI API를 사용한다.

```bash
OPENAI_API_KEY=... make translate VERSION=13.x DOC=collections.md
```

## 4. 결과 확인

실행 뒤 `git status --short`와 `git diff`로 영어 원문, KO·JA 문서와 사이드바 변경을 확인한다. 로컬 실행은 변경을 커밋하거나 원격에 전송하지 않는다. 커밋은 운영 액션에서만 일어난다.

## 5. 종료 코드

종료 코드 의미는 [08-error-cases.md](08-error-cases.md#7-진입점-종료-코드-계약)를 따른다. 실패 시 작업 트리에 이미 기록된 앞선 문서가 있을 수 있으므로 결과를 사용하기 전에 종료 코드와 diff를 함께 확인한다.

## 6. 수용 기준

- 호스트 로컬 실행, Docker 테스트와 Actions가 같은 Python 진입점을 사용한다.
- 호스트 로컬 실행은 환경 변수로 OpenAI API 또는 OpenAI CLI를 선택하고, Docker 테스트는 OpenAI API를 사용한다.
- Makefile은 Python 또는 Docker 명령과 선택자 전달만 감싸며 별도 동기화 단계를 추가하지 않는다.
- 로컬 실행에 artifact root, branch, repository 또는 push endpoint 입력이 필요하지 않다.
- 실행 과정에서 현재 저장소의 `HEAD`·branch를 checkout하거나 변경하지 않으며, 임시 commit, push 또는 배포 호출도 발생하지 않는다.
- 성공 시 변경된 문서와 사이드바만 작업 트리에 남는다.
