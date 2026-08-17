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

번역 동기화 단위 테스트와 격리 replay는 운영 publication과 분리된 진단 명령으로 실행

```bash
make translation-diagnostic          # Python 단위 테스트 + identity replay
make translation-provider-diagnostic # live provider fixture만 검사
make translation-path-diagnostic     # 현재 checkout의 산출 경로만 검사
make site-check                       # 링크 유틸리티 + 타입 + 빌드 + 앵커 검사
make preflight                        # live provider·publication 제외 진단
npm run test:e2e:docker               # Playwright E2E
```

### Docker 실행

```bash
docker build -t laravel-docs .
docker run -p 3000:3000 laravel-docs
```

### 문서 갱신

문서 갱신의 유일한 운영 진입점은 `translation-sync/workflow.py`의 `prepare`, `publish`, `deploy` 세 단계로 구성
`prepare`에서 승인 기준본·단위 테스트·identity replay·live fixture·격리 candidate·사이트 및 경로 검증·publication commit 준비를 하나의 제한 시간 안에 수행
`publish`에서 봉인된 tree를 다시 검증한 뒤 원격 branch를 compare-and-swap 방식으로 갱신
`main`의 `deploy`에서 정확한 published commit으로 배포를 요청하고 결과까지 대기

GitHub Actions에서는 GitHub Variables를 사용하지 않고 OpenAI 실행에 필요한 Secret만 전달

- provider/model은 코드 기본값 `openai`/`gpt-5.6-luna` 사용
- Secret: `OPENAI_API_KEY`
- reasoning effort는 코드 기본값 `medium` 사용
- 승인된 OpenAI 모델의 context/output 예산·request timeout·tokenizer는 코드의 모델 profile 기본값 사용

provider run/workflow timeout 기본값은 코드에서 `21600`초로 관리하며, 전체 workflow timeout은 버전 관리되는 `translation-sync/workflow.json`에서 `21600`초로 관리
request timeout ≤ run timeout ≤ workflow timeout 관계와 reserved output token < context window 관계가 필수
값이 없거나 관계가 맞지 않으면 provider 호출 전에 실패

로컬 운영 실행은 저장소 밖의 새 artifact 디렉터리와 명시적인 push endpoint를 사용
`prepare`에서 endpoint의 `owner/name`과 `REPOSITORY`의 정확한 일치 여부를 확인하고 배포 대상을 phase state에 봉인
이후 `deploy`에는 저장소 인자를 다시 전달하지 않음
HTTPS publication과 `main` 배포에는 `GH_TOKEN` 필요
`translation-prepare`는 Makefile에서 push 자격 증명을 제거한 환경으로 실행

```bash
artifact_root="$(mktemp -d)"

make translation-run \
  ARTIFACT_ROOT="$artifact_root" \
  PUSH_ENDPOINT="https://github.com/OWNER/REPOSITORY.git" \
  BRANCH="$(git branch --show-current)" \
  REPOSITORY="OWNER/REPOSITORY"
```

`VERSION=13.x DOC=collections.md`와 같은 selector 추가 가능
자격 증명을 단계별 shell에 따로 주입하려면 같은 `ARTIFACT_ROOT`로 `make translation-prepare`, `make translation-publish`, `make translation-deploy`를 순서대로 실행
`main` 이외의 branch에서는 deploy 단계 생략

Docker에서도 동일한 운영 CLI만 사용
저장소는 read-only로 mount되고 candidate와 phase state는 별도 named volume의 `/artifacts` 아래에 기록
매 실행마다 새로운 경로 선택 필요

```bash
make translate \
  DOCKER_ARTIFACT_ROOT="/artifacts/manual-001" \
  PUSH_ENDPOINT="https://github.com/OWNER/REPOSITORY.git" \
  BRANCH="main" \
  REPOSITORY="OWNER/REPOSITORY"
```

GitHub Actions도 동일하게 외부 artifact root에서 `prepare` → `publish` → `main`의 `deploy`만 호출
OpenAI provider 설정·인증은 prepare step에만, `GH_TOKEN`은 publish/deploy step에만 주입
실패 보고서·manifest·검증된 fixture 메타데이터·publication 및 deploy 결과만 Actions artifact로 보존
preparation key, provider 응답 본문과 candidate는 업로드하지 않음
Pull Request 자동 생성 없음

개별 진단 명령은 publication evidence를 만들지 않으며 운영 동기화 대신 사용할 수 없음
전체 계약은 [번역 동기화 작업 흐름](translation-sync/docs/00-workflow-summary.md), [전체 운영 및 산출 검증](translation-sync/docs/05-additional-work.md), [로컬 Translation Replay](translation-sync/docs/07-local-replay.md) 참고

## 라이선스

- 문서 웹사이트 코드: MIT License
- 라라벨 문서: MIT License `(Copyright (c) Taylor Otwell)`
