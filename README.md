<div align="center">

# 라라벨 한국어 문서

[![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?logo=laravel&logoColor=white)](http://laravel.com)
[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/letsescape/laravel-docs/develop?label=Last%20Updated)](https://github.com/letsescape/laravel-docs/commits/develop)
[![License](https://img.shields.io/github/license/letsescape/laravel-docs)](https://github.com/letsescape/laravel-docs/blob/develop/LICENSE)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 한국어 문서를 [Docusaurus](https://docusaurus.io) & [GitHub Pages](https://pages.github.com)를 사용하여 배포합니다.

- 지원 버전 : `master`, `13.x`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 문서 갱신 : GitHub Actions `update-docs` 워크플로우 수동 실행 [#](.github/workflows/update-docs.yml)

## 실행

> Node.js 24 이상이 필요합니다. (`.nvmrc` 참고)

```bash
npm install
npm start
```

타입 검사:

```bash
npm run typecheck
```

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 문서 갱신

문서 갱신은 GitHub Actions에서만 실행합니다.

1. GitHub 저장소 Secrets에 번역 제공자와 API 키를 설정합니다.

   ```dotenv
   # OpenAI
   TRANSLATION_PROVIDER=openai
   TRANSLATION_MODEL=gpt-5

   OPENAI_API_KEY=your_openai_api_key
   ```

   ```dotenv
   # Azure OpenAI
   TRANSLATION_PROVIDER=azure
   TRANSLATION_MODEL=gpt-5

   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_API_VERSION=2025-05-01-preview
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   ```

2. GitHub Actions의 `update-docs` 워크플로우를 수동 실행합니다.

워크플로우는 `.github/docs-updater`에서 `uv sync --frozen` 후 테스트와 `uv run python main.py`를 실행합니다. 이후 번역 구조, 타입, 빌드, 앵커 검증을 통과한 원문 캐시와 변경된 `versioned_docs/`, `versioned_sidebars/`를 `develop`에 커밋합니다.

로컬에서 번역 스크립트를 점검할 때는 API 키 대신 CLI 제공자를 사용할 수 있습니다.

```dotenv
TRANSLATION_PROVIDER=cli
TRANSLATION_CLI_COMMAND="codex exec --sandbox read-only --skip-git-repo-check -"
TRANSLATION_CLI_TIMEOUT=1800
```

CLI 명령은 표준 입력으로 번역 지침과 원문 Markdown을 받고, 표준 출력으로 번역된 Markdown만 반환해야 합니다. 사용하는 로컬 CLI에 맞게 `TRANSLATION_CLI_COMMAND` 값을 바꾸면 됩니다. 운영 워크플로우에서는 `openai` 또는 `azure` 제공자를 사용합니다.

## 라이선스

- 문서 웹사이트 코드 : MIT License
- 라라벨 문서 : MIT License `(Copyright (c) Taylor Otwell)`
