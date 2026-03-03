<div align="center">

# 라라벨 한국어 문서

[![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?logo=laravel&logoColor=white)](http://laravel.com)
[![Laravel Version](https://img.shields.io/packagist/v/laravel/framework)](https://packagist.org/packages/laravel/framework)
[![Last Updated](https://img.shields.io/github/last-commit/letsescape/laravel-docs-web/main?label=Last%20Updated)](https://github.com/letsescape/laravel-docs-web/commits/main)
[![License](https://img.shields.io/github/license/letsescape/laravel-docs-web)](https://github.com/letsescape/laravel-docs-web/blob/main/LICENSE)
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/letsescape/laravel-docs-web?utm_source=oss&utm_medium=github&utm_campaign=letsescape%2Flaravel-docs-web&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)

[라라벨 공식 문서](https://laravel.com) | [라라벨 한국어 문서](https://laravel.chanhyung.kim)

</div>

## 소개

라라벨 한국어 문서를 [Docusaurus](https://docusaurus.io) & [GitHub Pages](https://pages.github.com)를 사용하여 배포합니다.

- 지원 버전 : `master`, `12.x`, `11.x`, `10.x`, `9.x`, `8.x`
- 업데이트 주기 : 매일 04시 (KST) [#](.github/workflows/update-docs.yml#L4)

### 문서 필터링

번역 시, 다음과 같은 필터링을 적용합니다.

- 코드 블록 변환 : 들여쓰기 코드 블록을 펜스(백틱) 코드 블록으로 변환합니다.
- 스타일 태그 제거 : `<style>` 태그와 그 내용을 제거합니다.
- 이미지 태그 수정 : 이미지 태그(`<img>`)를 닫는 태그(`<img />`)로 변환합니다.
- 제목 중괄호 제거 : 제목 옆에 있는 클래스 옵션을 제거합니다 (`### 'after()' {.collection-method}` -> `### 'after()'`).
- 툴팁 형식 표준화 : 다양한 형태의 툴팁/노트(`> {note}`, `> **Note**`)를 `> [!NOTE]\n> message` 형식으로 통일합니다.
- 버전 플레이스홀더 치환 : 문서 내 `{{version}}` 플레이스홀더를 해당 버전 문자열(`master`, `12.x` 등)로 치환합니다.

## 실행

```bash
npm install
docusaurus start
```

문서의 목차(사이드바)를 자동으로 생성하려면 다음 명령을 실행합니다.  
이 스크립트는 `versioned_docs/version-{버전}/origin/documentation.md` 파일을 분석하여 각 버전에 대한 사이드바 구조를 생성합니다.

```bash
npm run generate-sidebars
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

## 라이선스

- 번역 코드 : MIT License
- 라라벨 문서 : MIT License `(Copyright (c) Taylor Otwell)`
