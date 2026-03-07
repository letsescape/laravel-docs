<div align="center">

# 라라벨 한국어 문서

[![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?logo=laravel&logoColor=white)](http://laravel.com)
[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/letsescape/laravel-docs-web/main?label=Last%20Updated)](https://github.com/letsescape/laravel-docs-web/commits/main)
[![License](https://img.shields.io/github/license/letsescape/laravel-docs-web)](https://github.com/letsescape/laravel-docs-web/blob/main/LICENSE)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 한국어 문서를 [Docusaurus](https://docusaurus.io) & [GitHub Pages](https://pages.github.com)를 사용하여 배포합니다.

- 지원 버전 : `master`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 업데이트 주기 : 매일 04시 (KST) [#](.github/workflows/update-docs.yml#L5)

## 실행

> Node.js 24 이상이 필요합니다. (`.nvmrc` 참고)

```bash
npm install
npm start
```

사이드바 생성 및 타입 검사:

```bash
npm run generate-sidebars
npm run typecheck
```

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 번역 실행

1. `source/.env.example` 파일을 복사하여 `source/.env` 파일을 만들고 번역 제공자를 설정합니다.

   ```dotenv
   # OpenAI
   TRANSLATION_PROVIDER=openai
   TRANSLATION_MODEL=gpt-4.1

   OPENAI_API_KEY=your_openai_api_key
   ```

   ```dotenv
   # Azure OpenAI
   TRANSLATION_PROVIDER=azure
   TRANSLATION_MODEL=gpt-4.1

   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_API_VERSION=2025-05-01-preview
   AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   ```

2. 의존성 설치 및 번역 실행

   ```bash
   cd source
   uv sync         # 의존성 설치
   uv run main.py  # 번역 실행
   ```

### Docker로 번역 실행

1. `source/.env.example` 파일을 복사하여 `source/.env` 파일을 만들고 번역 제공자를 설정합니다.

2. Docker로 번역 실행

   ```bash
   docker compose run --rm translate
   ```

## 라이선스

- 문서 웹사이트 코드 : MIT License
- 라라벨 문서 : MIT License `(Copyright (c) Taylor Otwell)`
