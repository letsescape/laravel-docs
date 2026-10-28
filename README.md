<div align="center">

# 라라벨 한국어 문서

[![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?logo=laravel&logoColor=white)](http://laravel.com)
[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/letsescape/laravel-docs/main?label=Last%20Updated)](https://github.com/letsescape/laravel-docs/commits/main)
[![License](https://img.shields.io/github/license/letsescape/laravel-docs)](https://github.com/letsescape/laravel-docs/blob/main/LICENSE)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 한국어 문서를 [Docusaurus](https://docusaurus.io)와 [GitHub Pages](https://pages.github.com)를 사용해 배포

- 지원 버전: `master`, `13.x`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 문서 갱신: GitHub Actions `Sync Documentation Translation` 워크플로우 정기 또는 수동 실행 [#](.github/workflows/sync-translation.yml)

## 실행

> Node.js 24 이상 필요 (`.nvmrc` 참고)

```bash
npm install
npm start
```

타입 검사:

```bash
npm run typecheck
```

번역 동기화 Python 단위 테스트와 사이트 검증은 각각 실행

```bash
make translation-test # 번역 동기화 Python 단위 테스트
make site-check       # 링크 유틸리티 + 타입 + 빌드 + 앵커 검사
make preflight        # 위 두 검사 실행
npm run test:e2e:docker
```

### 문서 채팅

SDK URL과 API URL을 설정하면 문서 페이지 우측 하단에 채팅 버튼을 표시합니다. 설정하지 않으면 SDK를 로드하지 않습니다. 문서 이동 시 같은 위젯의 페이지 정보를 갱신하고, 문서 밖에서는 위젯을 숨깁니다.

로컬에서는 먼저 `../laravel-chat/demo/README.md`에 따라 API와 문서 데모 서버를 실행합니다. 기본 주소는 각각 `127.0.0.1:8010`, `127.0.0.1:8011`입니다. 이후 이 저장소에서 실행합니다.

```bash
npm run start:chat
```

문서 사이트는 `http://127.0.0.1:3000/docs/13.x/container/`에서 확인합니다. 개발 서버의 `/__chat/` 프록시가 기존 데모의 SDK와 `/v1/chat`에 연결합니다. 이 프록시는 `npm start` 개발 서버에만 적용됩니다. 데모 주소를 직접 지정하려면 다음과 같이 실행합니다.

```bash
LARAVEL_CHAT_LOCAL_DEMO=http://127.0.0.1:8011 npm start -- --host 127.0.0.1 --no-open
```

호스팅 후에는 두 URL을 설정하고 사이트를 다시 빌드합니다. 아래 주소는 예시입니다. 연결 컴포넌트는 수정할 필요가 없습니다.

```bash
LARAVEL_CHAT_SDK_URL=https://sdk.example.com/index.js \
LARAVEL_CHAT_API_URL=https://api.example.com/v1/chat \
LARAVEL_CHAT_BROWSER_MANIFEST_URL=https://static.example.com/browser/manifest.json \
npm run build
```

SDK 호스트는 `sdk/dist/` 전체의 상대 경로를 유지해야 합니다. 외부 호스트를 쓰면 SDK와 API에서 문서 사이트 origin의 요청을 허용해야 합니다. SDK를 사이트에 함께 배포한다면 SDK URL에 `/chat-sdk/index.js` 같은 경로를 사용할 수 있습니다.

GitHub Actions 배포에서는 저장소 변수 `LARAVEL_CHAT_SDK_URL`·`LARAVEL_CHAT_API_URL`을 설정합니다. 브라우저 로컬 실행을 제공하면 `LARAVEL_CHAT_BROWSER_MANIFEST_URL`도 설정합니다. API와 SDK 연결 검증이 끝난 뒤 `LARAVEL_CHAT_ENABLED`를 `true`로 지정해야 배포 빌드에 URL을 전달합니다. 이 값이 없거나 `true`가 아니면 위젯을 비활성화한 사이트를 빌드합니다. 위의 직접 빌드 명령에는 이 활성화 변수가 필요하지 않습니다.

`LARAVEL_CHAT_BROWSER_MANIFEST_URL`을 명시하면 로컬 모델 선택을 연결합니다. 생략하면 기본 서버 채팅만 사용합니다. 개발 프록시를 쓸 때는 같은 문서 release의 색인을 제공하는 `/__chat/__browser/manifest.json`을 지정할 수 있습니다. 브라우저 색인 호스트도 문서 사이트 origin의 요청을 허용해야 합니다. 피드백 수집은 연결하지 않습니다.

위젯은 게시 revision을 전달하지 않습니다. 기본 API는 질문과 이전 대화에 버전이 없으면 기본 안정 버전을 사용합니다. 특정 버전이 필요하면 질문에 명시합니다. 로컬 검색은 현재 페이지의 버전과 언어를 사용합니다.

```bash
npm run test:chat
```

### 문서 채팅 색인 준비

이 저장소의 명시적 명령으로 게시 정보와 채팅 색인을 준비합니다. 생성기는 형제 `../laravel-chat` 저장소의 공통 도구를 사용합니다. 다른 위치라면 각 명령에 `--chat-dir <경로>`를 지정합니다. 일반 `npm run build`는 게시 정보 생성이나 AI 색인을 실행하지 않습니다.

이 명령에는 Node.js 26, uv와 `laravel-chat`의 Python·SDK·데모 의존성이 필요합니다. 일반 문서 사이트의 Node.js 24 이상 조건과 구분합니다. 먼저 `../laravel-chat`에서 `make install-demo`를 실행합니다.

1. 커밋한 문서 원문으로 새 게시 빌드를 만듭니다. 아래 출력 경로는 아직 없어야 합니다.

   ```bash
   npm run chat:build -- --output tmp/chat-publication
   ```

   명령은 시작 시 문서 Git HEAD를 고정합니다. 문서 원문이 해당 커밋과 다르면 실패합니다. UI의 미커밋 변경은 사용할 수 있으며, 실제 HTML 해시는 게시 정보에 기록합니다. 한국어·일본어 페이지마다 원문 해시·HTML 해시·canonical URL·앵커를 기록합니다. 기존 `build/`는 수정하지 않습니다.

2. 게시 빌드와 같은 revision의 SQLite release를 만듭니다.

   ```bash
   npm run chat:index -- sqlite \
     --published-dir tmp/chat-publication \
     --output tmp/chat-releases
   ```

   기본 API도 사용할 경우 같은 revision을 검토한 의도 근거 JSON을 `--curation <파일>`로 추가합니다. 이전 revision의 검토 자료를 그대로 재사용하지 않습니다. 이 단계는 공개 GitHub 커밋을 확인하지만 AI 공급자를 호출하지 않습니다. 색인은 한국어·영어·일본어 원문을 모두 포함합니다. 실제 게시 정보는 한국어·일본어만 포함하며, 영어 출처는 고정 GitHub 원문 URL을 사용합니다.

3. 로컬 모델용 브라우저 색인을 명시적으로 생성합니다. `<release>`는 앞 단계가 출력한 디렉터리로 바꿉니다.

   ```bash
   npm run chat:index -- browser \
     --manifest tmp/chat-releases/<release>/manifest.json \
     --output tmp/chat-browser
   ```

   이 단계는 모델을 다운로드하고 모든 청크의 임베딩을 계산합니다. 원문 JSONL은 `tmp/chat-browser.jsonl`, 정적 색인은 `tmp/chat-browser/`에 남습니다. 실패한 중간 자료를 자동 삭제하지 않습니다. 완성된 `manifest.json`의 URL을 위젯의 `LARAVEL_CHAT_BROWSER_MANIFEST_URL`에 지정합니다.

   기본 계산 장치는 CPU입니다. WebGPU를 지원하는 환경에서는 위 명령에 `--device webgpu`를 추가해 GPU로 계산할 수 있습니다. CPU를 명시하려면 `--device cpu`를 사용합니다.

4. 기본 API를 사용할 때만 OpenAI 색인을 업로드합니다. `OPENAI_API_KEY`를 실행 환경에 설정해야 합니다. 이 명령은 실제 API를 호출하며 요금이 발생합니다.

   ```bash
   npm run chat:index -- openai \
     --manifest tmp/chat-releases/<release>/manifest.json \
     --output tmp/chat-openai
   ```

   중단한 같은 release의 업로드는 동일한 인자에 `--resume`을 추가합니다. 임시 자료의 만료 기간은 `--expires-days 7`처럼 지정할 수 있습니다. API는 같은 release의 `INDEX_MANIFEST`와 `OPENAI_RETRIEVAL_MANIFEST`를 사용해야 합니다.

문서가 갱신되면 새 게시 빌드부터 다시 준비합니다. 이 명령은 수동 준비 절차이며 배포나 자동 갱신 워크플로우를 실행하지 않습니다. 생성한 게시 빌드와 SQLite·OpenAI·브라우저 색인은 같은 문서 revision을 기준으로 함께 사용합니다.

```bash
npm run test:chat-index
```

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 문서 갱신

문서 갱신 진입점은 `translation-sync/main.py`입니다. upstream에서 원본 문서를 동기화한 뒤 변경된 문서를 Python과 선택한 OpenAI provider(API 또는 CLI)로 번역하고 검증된 문서·사이드바를 작업 트리에 기록합니다.

`main.py`는 Git을 조작하지 않습니다. 운영 Actions는 마지막 단계에서 갱신된 문서를 실행 branch에 커밋·push합니다. 번역 워크플로우는 Node 설치, 사이트 빌드, 배포를 수행하지 않으며, 사이트 배포는 이 워크플로우의 완료 이벤트를 구독하는 별도 워크플로우가 담당합니다.

GitHub Actions에서는 GitHub Variables를 사용하지 않고 OpenAI 실행에 필요한 Secret만 전달

- provider/model은 코드 기본값 `openai`/`gpt-6-luna` 사용
- Secret: `OPENAI_API_KEY`
- reasoning effort는 코드 기본값 `medium` 사용
- 승인된 OpenAI 모델의 context/output 예산·request timeout·tokenizer는 코드의 모델 profile 기본값 사용

provider run timeout 기본값은 코드에서 `21000`초로 관리
request timeout ≤ run timeout 관계와 reserved output token < context window 관계가 필수
기본값 적용 후에도 필수 값을 확정할 수 없거나 관계가 맞지 않으면 provider 호출 전에 실패

로컬 실행은 `TRANSLATION_PROVIDER`로 OpenAI API(`openai`) 또는 OpenAI CLI(`cli`)를 선택합니다. 저장소 루트의 `.env`가 있으면 Makefile이 값을 읽어 넣고, 명시적으로 준 환경 변수가 우선합니다.

```bash
TRANSLATION_PROVIDER=openai OPENAI_API_KEY=... make translation-run
```

`VERSION=13.x DOC=collections.md`와 같은 selector 추가 가능

Docker도 Python 전용 이미지에서 같은 `main.py`를 호출하고 현재 작업 트리에 결과를 기록합니다. 이미지에 CLI를 설치하지 않으므로 Docker 테스트는 OpenAI API를 사용합니다.

```bash
OPENAI_API_KEY=... make translate VERSION=13.x DOC=collections.md
```

전체 계약은 [번역 동기화 작업 흐름](translation-sync/docs/00-workflow-summary.md), [번역 실행 경계](translation-sync/docs/05-additional-work.md), [로컬 번역 실행](translation-sync/docs/07-local-replay.md) 참고

## 라이선스

- 문서 웹사이트 코드: MIT License
- 라라벨 문서: MIT License `(Copyright (c) Taylor Otwell)`
