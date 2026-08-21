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

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 문서 갱신

문서 갱신 진입점은 `translation-sync/main.py`입니다. upstream에서 원본 문서를 동기화한 뒤 변경된 문서를 Python과 OpenAI API로 번역하고 검증된 문서·사이드바를 작업 트리에 기록합니다.

`main.py`는 Git을 조작하지 않습니다. 운영 Actions는 마지막 단계에서 갱신된 문서를 실행 branch에 커밋·push합니다. 번역 워크플로우는 Node 설치, 사이트 빌드, 배포를 수행하지 않으며, 사이트 배포는 이 워크플로우의 완료 이벤트를 구독하는 별도 워크플로우가 담당합니다.

GitHub Actions에서는 GitHub Variables를 사용하지 않고 OpenAI 실행에 필요한 Secret만 전달

- provider/model은 코드 기본값 `openai`/`gpt-5.6-luna` 사용
- Secret: `OPENAI_API_KEY`
- reasoning effort는 코드 기본값 `medium` 사용
- 승인된 OpenAI 모델의 context/output 예산·request timeout·tokenizer는 코드의 모델 profile 기본값 사용

provider run timeout 기본값은 코드에서 `21600`초로 관리
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
