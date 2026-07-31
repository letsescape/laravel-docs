# 사이드바 갱신 및 검증 설계

## 목적

영어 원문 `documentation.md`를 단일 기준으로 Docusaurus 사이드바 산출물을 결정적으로 생성하고, locale별 sidebar override JSON을 제거하여 모든 locale이 동일한 영어 label 기반 사이드바를 사용하게 한다.

## 범위

- `documentation.md` 파싱에서 `versioned_sidebars/*.json` 갱신까지의 생성 흐름을 소유한다.
- locale별 sidebar JSON(`i18n/{ko,ja}/…/version-*.json`) 제거를 소유한다.
- 문서 본문 번역, heading, anchor, 문서 title은 이 단계의 관리 대상이 아니다.

## 입력

| 항목 | 설명 |
|---|---|
| 영어 원문 `documentation.md` | 각 버전의 사이드바 구조를 선언하는 단일 기준 문서 |
| 기존 `versioned_sidebars/*.json` | category collapsed 상태 등 표시 속성 보존 목적으로만 참조 |
| `versions.json` | 대상 버전 목록. `master` + 내림차순 안정 버전 배열 |

## 출력

| 항목 | 설명 |
|---|---|
| `versioned_sidebars/version-<version>-sidebars.json` | 영어 `documentation.md` 기준으로 재생성된 사이드바 |
| locale sidebar JSON 삭제 | `i18n/{ko,ja}/…/version-<version>.json` 존재 시 삭제 |

## 불변조건

1. **단일 기준**: sidebar 구조와 label의 유일한 기준은 영어 원문 `documentation.md`이다. locale 번역본은 읽지 않는다.
2. **Label 비번역**: category, doc, link label은 번역하지 않고 영어 값을 그대로 사용한다.
3. **저장소 오염 방지**: 출력 경로가 저장소 밖을 가리키면 거부한다. symlink를 따라 외부에 쓰지 않는다. 기존 sidebar JSON이 symlink이면 읽거나 덮어쓰지 않는다.
4. **Fail-closed**: 파싱 issue 발생 시 해당 버전의 sidebar 쓰기와 locale JSON 삭제를 모두 차단한다.
5. **원자적 공개**: sidebar JSON은 독자가 부분 기록 상태를 관측할 수 없는 단일 교체 단위로 공개해야 한다.
6. **Override 제거**: locale별 sidebar JSON은 stale override가 되므로 존재 시 삭제한다.

## 처리 순서

```text
1. versions.json 스키마 검증 (배열 형식, master 위치, 정렬, 중복)
2. 대상 버전 결정
3. 각 버전에 대해:
   a. 영어 documentation.md 파싱 → category / doc / link 항목 추출
   b. 파싱 issue 확인 (지원하지 않는 문법, 중복 key 등)
   c. issue 있으면 해당 버전 건너뜀
   d. 기존 sidebar JSON에서 category collapsed 상태 읽기
   e. sidebar JSON 생성·기록
   f. locale sidebar JSON 존재 시 삭제
   g. 산출물 재읽기·정합성 검증
```

## 파싱 규칙

| 소스 패턴 | 산출 유형 |
|---|---|
| `- ## Label` | category (items를 하위에 수집) |
| 들여쓴 `- [Label](/docs/<version>/<id>)` | doc item (id는 path 마지막 segment) |
| `- [Label](외부 또는 deep URL)` | link item |

- `- [`로 시작하지만 지원 문법과 일치하지 않는 줄은 조용히 생략하지 않고 issue로 기록한다.
- 동일 category label 반복은 translation key 충돌이므로 issue로 기록한다.
- 동일 doc id가 여러 category에 등장하는 것은 허용하되, 두 번째부터 고유 key를 부여한다.
- `master` sidebar의 루트 API Documentation link URL은 `versions.json` 최신 안정 버전으로 정규화한다.

## 실패 정책

| 상태 | 처리 |
|---|---|
| `versions.json` 스키마 위반 | 전체 sidebar 갱신 중단 |
| `documentation.md` 파싱 issue | 해당 버전의 쓰기·삭제 차단, 다른 버전은 계속 |
| 출력 경로가 저장소 밖 또는 symlink | 해당 경로 거부 |
| 기존 sidebar JSON 스키마 위반 | 해당 버전의 쓰기·삭제 건너뜀 |
| doc id에 대응하는 영어 원문 파일 부재 | 해당 버전 실패 |

## 수용 기준

사이드바 갱신 후 다음을 모두 만족해야 한다.

1. `documentation.md`에서 지원 문법을 만족하는 모든 doc link가 sidebar JSON에 같은 순서로 존재한다.
2. sidebar JSON에만 있고 `documentation.md`에 없는 doc item이 없다.
3. sidebar doc label과 category label이 `documentation.md`의 값과 일치한다.
4. locale별 sidebar JSON(`i18n/{ko,ja}/…/version-*.json`)이 남아 있지 않는다.
5. `master`의 루트 API Documentation link가 최신 안정 버전 URL이다.
6. doc id에 대응하는 영어 원문 파일이 존재한다.
7. category와 link의 translation key가 중복되지 않는다.
8. 지원하지 않는 문법이 조용히 생략되지 않았다.

## 종료 상태 의미

sidebar 검증 실패는 번역 품질 문제가 아니라 sidebar sync 단계 자체의 실패로 분류한다. provider 재시도 없이 sidebar sync를 재실행해야 한다.

전체 동기화 진입점에서 sidebar 실패는 종료 코드 `1`(대상 실패)로 반영된다.
