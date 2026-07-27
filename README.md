<div align="center">

# 라라벨 한국어 문서

[![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?logo=laravel&logoColor=white)](http://laravel.com)
[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/letsescape/laravel-docs/main?label=Last%20Updated)](https://github.com/letsescape/laravel-docs/commits/main)
[![License](https://img.shields.io/github/license/letsescape/laravel-docs)](https://github.com/letsescape/laravel-docs/blob/main/LICENSE)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 한국어 문서를 [Docusaurus](https://docusaurus.io) & [GitHub Pages](https://pages.github.com)를 사용하여 배포합니다.

- 지원 버전 : `master`, `13.x`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 문서 갱신 : GitHub Actions `Sync Documentation Translation` 워크플로우 정기 또는 수동 실행 [#](.github/workflows/sync-translation.yml)

## 실행

> Node.js 26.x가 필요합니다. (`.nvmrc` 참고)

```bash
npm install
npm start
```

타입 검사:

```bash
npm run typecheck
```

번역 동기화와 배포 검증을 로컬에서 같은 진입점으로 실행할 수 있습니다.

```bash
make translation-check  # Python 단위 테스트 + API 키 없는 격리 replay
make translation-provider-check  # 설정된 live provider의 고정 fixture 응답 검사
make site-check         # 링크 유틸리티 + 타입 검사 + 빌드 + 앵커 검증
make preflight          # translation-check + site-check (live provider 호출 제외)
npm run test:e2e:docker # Node 26 + 고정 Playwright Chromium 컨테이너 E2E
```

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 문서 갱신

문서 갱신은 GitHub Actions 또는 로컬의 공통 Make target으로 실행합니다. 실제 provider를 호출하지 않는 구조 검증은 `make translation-check`로 먼저 실행합니다.

1. GitHub 저장소 Secrets에 번역 제공자와 API 키를 설정합니다.

   ```dotenv
   # OpenAI
   TRANSLATION_PROVIDER=openai
   TRANSLATION_MODEL=gpt-5.6-luna
   TRANSLATION_REASONING_EFFORT=medium

   OPENAI_API_KEY=your_openai_api_key
   ```

   ```dotenv
   # Azure OpenAI
   TRANSLATION_PROVIDER=azure
   TRANSLATION_MODEL=your_azure_deployment_name
   TRANSLATION_REASONING_EFFORT=medium

   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_API_VERSION=your_deployment_api_version
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   ```

2. GitHub Actions의 `Sync Documentation Translation` 워크플로우를 수동 실행합니다.

워크플로우는 `uv sync --locked` 후 `make translation-check`, live KO/JA fixture 검사, `make translation-run`을 순서대로 실행합니다. 생성 결과에 대해 `make site-check`와 허용 산출 경로 검사를 통과한 경우에만 workflow를 실행한 브랜치에 커밋하고 push합니다. checkout write credential은 저장하지 않고 최종 push step에서만 설정합니다. `main` 실행은 commit/push와 분리된 배포 workflow를 트리거하며 Pull Request는 자동 생성하지 않습니다.

로컬에서 번역 스크립트를 점검할 때는 API 키 대신 CLI 제공자를 사용할 수 있습니다.

```dotenv
TRANSLATION_PROVIDER=cli
TRANSLATION_CLI_COMMAND="codex exec"
TRANSLATION_MODEL=gpt-5.6-luna
TRANSLATION_REASONING_EFFORT=medium
TRANSLATION_CLI_TIMEOUT=1800
```

CLI adapter는 임시 디렉터리에서 Codex를 `--ephemeral`, read-only, 사용자 설정·execpolicy rules·`AGENTS.md` 제외 모드로 실행하고 `--output-last-message` 파일의 최종 Markdown만 읽습니다. browser, computer, image generation, plugin, app, shell, subagent와 web search 기능을 끄며, child process에는 인증·런타임·proxy/CA에 필요한 allowlist 환경 변수만 전달합니다. 모델이 실행하는 subprocess에는 환경 변수를 상속하지 않습니다. `TRANSLATION_CLI_COMMAND`에는 옵션 없이 Codex 실행 진입점만 지정합니다. 현재 플래그 호환 기준은 `codex-cli 0.145.0`이며 CLI를 바꾸면 단위 테스트와 live provider 검사를 다시 통과해야 합니다. OpenAI adapter는 완료된 Responses API의 `output_text`를 사용하고, Azure adapter는 `finish_reason=stop`인 Chat Completions 응답만 사용합니다.

실제 provider가 wrapper 문구 없이 구조가 보존된 KO/JA Markdown을 반환하는지 먼저 확인할 수 있습니다. 이 명령은 문서 파일을 수정하지 않으며 provider, model, reasoning, locale과 런타임 출력 규칙까지 포함한 effective prompt SHA-256을 출력합니다.

```bash
make translation-provider-check
make translation-provider-check LOCALE=ko
```

```bash
make translation-run VERSION=13.x DOC=collections.md
```

전체 단계와 replay의 범위는 [번역 동기화 작업 흐름](translation-sync/docs/00-workflow-summary.md)과 [로컬 Translation Replay](translation-sync/docs/07-local-replay.md)를 참고합니다.

## 라이선스

- 문서 웹사이트 코드 : MIT License
- 라라벨 문서 : MIT License `(Copyright (c) Taylor Otwell)`
