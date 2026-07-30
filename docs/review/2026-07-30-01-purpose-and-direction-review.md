# 목적과 방향 리뷰 (2026-07-30)

대상 커밋: `d0a29b7` (`refactor/sync-docs`)

## 1. 문서에서 확인되는 공식 목적

| 문서 | 진술 |
|---|---|
| `README.md` §소개 | "라라벨 한국어 문서를 Docusaurus & GitHub Pages를 사용하여 배포합니다." 지원 버전 `master`, `13.x`~`8.x` 명시. |
| `README.md` §문서 갱신 | 문서 갱신은 GitHub Actions `Sync Documentation Translation` 또는 로컬 Make target으로 실행. |
| `package.json` | `description: "The Laravel Korean documentation."` |
| `translation-sync/pyproject.toml` | `description = "Laravel 문서 자동 번역 동기화 구현체"` |
| `translation-sync/docs/00-workflow-summary.md` | 원문 동기화 → 변경 계획 → 번역 → 검증 → 사이드바 → 사이트 검증 → 실행 브랜치 반영의 고정 순서. |
| `translation-sync/docs/05-additional-work.md` §3 | 번역 대상은 본문, 비번역 대상은 제목·heading·링크 label·사이드바 label·앵커·코드·기술 용어. |

즉 문서상 공식 목적은 **"Laravel 한국어 문서 사이트 + 그 자동 갱신"** 이다.

## 2. 코드에서 추론되는 실제 목적

확인된 사실:

- 발행 로케일은 **한국어와 일본어 2개**다. `docusaurus.config.ts`의 `LOCALES = ['ko','ja']`, `DEFAULT_LOCALE = 'ko'`.
- 일본어는 부가 기능이 아니라 일급 대상이다.
  - 전용 프롬프트: `translation-sync/prompt_jp.md` (391행)
  - 출력 경로: `main.py`의 `_ja_output()` → `i18n/ja/docusaurus-plugin-content-docs/version-*`
  - 번역 루프가 KO/JA를 항상 함께 처리: `main.py:911-914`
  - CI가 KO/JA fixture를 모두 게이트: `provider_check.py`, `sync-translation.yml:87-95`
- `i18n/en`은 발행되지 않는 **입력 캐시**다. `localeConfigs.en`은 존재하지만 `LOCALES`에 없다.
- 홈페이지는 문서 사이트 기본 홈이 아니라 laravel.com 마케팅 페이지 구조의 현지화 복제다. `src/pages/index.tsx`가 Hero / AIFramework / Framework / Cloud / Nightwatch / Frontend / CTA / Events 섹션을 조립한다. 이벤트 데이터는 `EventsSection.tsx`에 하드코딩되어 있다.

따라서 코드가 실제로 제공하는 것은 **"KO+JA 2개 로케일 Laravel 문서 포털(문서 + 마케팅 홈) + 자동 번역 운영 도구"** 이다.

## 3. 가능한 해석 비교

프로젝트 목적이 문서에 완전히 정의되어 있지 않으므로 하나로 확정하지 않고 근거별로 비교한다.

| 해석 | 지지 근거 | 반증 근거 | 판정 |
|---|---|---|---|
| A. Laravel 공식 문서 미러 | `i18n/en`에 원문을 byte 단위로 캐시, 홈페이지가 laravel.com 구조를 모사 | EN은 발행되지 않음(`LOCALES` 미포함), 미러가 최종 산출물이 아님 | 부분적으로만 성립 |
| B. KO/JA 현지화 문서 사이트 | 실제 서빙 산출물이 KO/JA, 버전 7개, 검색·locale 드롭다운·SEO 구성 | README/package.json이 KO만 언급 | **가장 강하게 성립** |
| C. 자동 번역 운영 도구 | `translation-sync`가 저장소 규모의 절반 이상, 문서 9종이 이 도구만 다룸 | 사이트 경로에 강결합(`REPO_ROOT` 상대, 고정 `i18n`/`versioned_docs` 레이아웃) — 독립 제품이 아님 | 목적이 아니라 수단 |

**결론:** 실제 목적은 B이고 C는 B를 유지하기 위한 수단이다. 문서는 B를 "한국어"로만 좁혀 서술해 JA를 누락한다.

## 4. 주요 사용자와 사용 시나리오

| 사용자 | 시나리오 | 확실성 |
|---|---|---|
| 한/일 Laravel 개발자 | 검색 또는 직접 URL로 특정 버전 문서를 읽는다. 버전·언어 드롭다운으로 이동한다. | 추론 (계측·검색·드롭다운 구성으로 뒷받침) |
| 저장소 운영자 | 격일 스케줄 결과를 확인하고 실패 시 원인을 수정해 재실행한다. | 확인됨 (`sync-translation.yml`, `translation-sync/docs/00` §1.1) |
| 자동화 에이전트 | `.docs/system-prompt.md` 계약에 따라 리뷰·수정을 수행한다. | 확인됨 |

**핵심 사용 시나리오(확인됨):** upstream 문서가 변경되면 자동으로 해당 블록만 번역되어 KO/JA 문서에 반영되고, 모든 게이트를 통과할 때만 커밋되며, `main`이면 배포된다.

## 5. 핵심 가치

1. **증분성** — 전체 재번역이 아니라 diff 기반 블록 단위 번역(`patch.py`). 비용과 회귀 범위를 줄인다.
2. **구조 보존** — 링크·앵커·코드·heading을 원문 기준으로 유지하고 자동 검증한다(`verify.py`, `response_contract.py`). 번역이 문서 navigation을 깨뜨리지 않게 한다.
3. **원문 추적성** — 각 번역 블록에 영어 원문을 HTML 주석으로 병기해 이후 diff와 검증의 기준으로 쓴다(`annotate.py`).
4. **fail-closed 운영** — 검증 실패 시 기록·커밋하지 않는다(`main.py:920-936`, `validate_generated_changes.py`).

## 6. 현재 범위와 제외 범위

현재 범위(확인됨):
- KO/JA 문서 7개 버전, 마케팅 홈페이지, 검색, 버전/언어 전환, GitHub Pages 배포
- upstream 동기화·번역·검증·사이드바 재생성·산출 경로 검사

의도적 제외(확인됨):
- EN 로케일 발행 (`LOCALES` 미포함, `e2e/docs-rendering.spec.ts`가 `/en` 404를 단언)
- 블로그 (`presets.classic.blog: false`)
- `origin/**`, `readme.md`, `documentation.md` 렌더링 (`docusaurus.config.ts` exclude)
- PR 자동 생성 (`README.md`: "Pull Request는 자동 생성하지 않습니다")
- `main` 이외 브랜치의 배포 (`deploy.yml` 브랜치 가드)
- heading·label·앵커 번역 (`05-additional-work.md` §3)

## 7. 현재 구현이 향하는 방향

- **단기(확인됨):** 번역 파이프라인의 정확성 강화. `patch.py`·`response_contract.py`가 계속 커지고 있고(4,059행 / 2,427행), 신규 upstream 편집 형태별 헬퍼가 추가되는 형태다. `translation-sync/docs/08-error-cases.md`가 과거 실패 사례를 ID로 보존하는 것도 같은 방향이다.
- **장기(추론):** 로케일 확장 여지는 코드에 존재하나(프롬프트 분리, `SIDEBAR_LOCALES`) 확장은 자동화되어 있지 않다. 새 로케일은 최소 `main.py`, `validate_generated_changes.py`, `provider_check.py`, `docusaurus.config.ts`, `create-latest-doc-redirects.mjs`, `validate-anchors.mjs`를 동시에 수정해야 한다. 로드맵 문서는 없다.
- **성공 기준(확인됨: 문서에 없음):** `ROADMAP.md`, `CONTRIBUTING.md`, `CHANGELOG.md`가 모두 없다. 사실상의 성공 기준은 `make preflight`·`make site-check`·`translation-provider-check` 게이트 통과다.

## 8. 문서와 코드의 방향 일치 여부

| 항목 | 문서상 정의 | 코드상 확인 결과 | 일치 여부 | 평가 |
|---|---|---|---|---|
| 해결하려는 문제 | "라라벨 한국어 문서"를 Docusaurus로 배포하고 Actions로 갱신 (`README.md` §소개, §문서 갱신) | diff 기반 증분 번역(`sync/source/diff.py`, `sync/translation/patch.py`), upstream SHA 고정(`upstream.py`), EN 캐시 | 대체로 일치 (JA 누락) | 대체로 적절 |
| 주요 사용자 | 명시 없음 | 공개 독자 전제 구성(Algolia `contextualSearch`, gtag, GTM, locale 드롭다운) | 판단 불가 | 판단 보류 |
| 핵심 기능 | 지원 버전 7개, 번역 갱신 워크플로, 번역 규칙(`prompt.md`) | 7버전 × 2로케일 발행, 이중언어 주석 형식, 사이드바 재생성, 마케팅 홈페이지 | 부분 일치 (홈페이지 미기재) | 부분적으로 부적절 |
| 운영 방식 | `README.md` §문서 갱신의 workflow 순서, Make target 5개 | `sync-translation.yml` step 순서와 일치, `deploy.yml` 브랜치 가드 | 일치 | 적절 |
| 확장 방향 | 문서 없음 | 로케일 추가가 6개 파일 이상에 하드코딩 분산 | 판단 불가 | 판단 보류 |

## 9. 불명확하거나 충돌하는 방향

### [High] 일본어가 문서상 존재하지 않는다
- 관련 문서: `README.md`(전체), `package.json` `description`
- 관련 코드: `docusaurus.config.ts:20`, `main.py` `_ja_output`, `prompt_jp.md`, `provider_check.py`
- 확인 내용: 저장소는 JA를 KO와 동등하게 번역·검증·발행하지만 공식 문서 어디에도 JA가 언급되지 않는다.
- 영향: 신규 기여자가 JA 산출물을 부수적인 것으로 오해한다. JA 전용 결함(예: 이번 리뷰에서 확인한 JA 앵커 15건)이 "부가 기능 문제"로 과소평가된다.
- 권장 조치: `README.md` §소개와 `package.json` description에 JA 로케일을 명시한다.
- 확실성: 확인됨

### [Medium] 마케팅 홈페이지의 위치가 정의되지 않았다
- 관련 문서: 없음
- 관련 코드: `src/pages/index.tsx`, `src/components/Homepage/*`(`EventsSection.tsx`에 2026 이벤트 하드코딩)
- 확인 내용: 홈페이지는 laravel.com 마케팅 구조를 복제하지만 동기화 메커니즘도 갱신 정책도 문서화되어 있지 않다.
- 영향: laravel.com이 바뀌면 홈페이지가 조용히 낡는다. 문서 사이트인지 포털인지 범위가 모호해 유지보수 판단 기준이 없다.
- 권장 조치: `README.md`에 홈페이지가 수동 관리 대상이며 upstream과 자동 동기화되지 않는다는 한 줄을 추가한다.
- 확실성: 확인됨 (의도는 추론)

### [Medium] 성공 기준과 완료 정의가 문서에 없다
- 관련 문서: `ROADMAP.md`/`CONTRIBUTING.md` 부재
- 관련 코드: `Makefile`의 `preflight`, `site-check`
- 확인 내용: "무엇이 통과해야 정상인가"가 Makefile target으로만 존재한다. 그런데 이번 리뷰에서 `make site-check`(JA 앵커 15건)와 `--check-annotations`(master 11건, 13.x 12건)가 실패 상태임을 확인했다. 즉 사실상의 성공 기준이 현재 저장소 자체에서 충족되지 않는다.
- 영향: 게이트 실패가 "정상 상태"로 굳어지면 게이트의 판별력이 사라진다.
- 권장 조치: `README.md`에 "정상 상태 = preflight + site-check 통과"를 명시하고, 현재 알려진 실패 항목을 별도로 추적한다.
- 확실성: 확인됨

## 10. 프로젝트가 집중해야 할 핵심 영역

목적(B: KO/JA 문서 포털) 기준으로 우선순위를 매기면 다음 순서다.

1. **문서 산출물의 정확성** — 링크·앵커가 깨지면 문서 사이트의 1차 가치가 훼손된다. 현재 JA 앵커 15건이 실패 중이며 비앵커 링크에는 게이트가 없다(`docusaurus.config.ts`의 `onBrokenLinks: 'warn'`).
2. **번역 파이프라인의 데이터 무결성** — 잘못된 번역 반영은 문서를 조용히 손상시킨다. 이번 세션에서 `normalize_stale_link_targets`의 label 손상을 직접 재현했다(03 문서 참조).
3. **게이트 배치** — PR 단계 검증이 없어 회귀가 배포 시점에 드러난다.
4. **문서 신뢰성** — README·E2E 목록이 구현과 충돌한다.

반대로 지금 우선순위가 아닌 것: 마케팅 홈페이지 기능 확장, 신규 로케일 추가, 대규모 아키텍처 재설계.

## 11. 프로젝트 목적 관점의 종합 평가

**평가: 대체로 적절**

근거:

- 코드가 실제로 목적(KO/JA 문서 최신 유지)을 직접 지원한다. 파이프라인 단계가 문서 단계와 1:1로 대응하고, 검증이 "번역 품질"이 아니라 "구조 보존"이라는 자동 판정 가능한 목표에 정확히 맞춰져 있다. 이는 LLM 번역 시스템에서 올바른 범위 설정이다.
- 목적과 무관한 코드가 과도하게 포함되어 있지는 않다. 다만 죽은 스캐폴딩(`sidebars.ts`, `docs/index.md`, `src/components/{Hero,CodeExamples,Features}`)과 기능 플래그로 도달 불가한 자산(`SHOW_CAROUSEL=false`, `SHOW_DISABLED_NAV=false`)이 남아 있다.
- 감점 요인은 목적 자체가 아니라 **목적의 서술 범위**(JA·홈페이지 누락)와 **목적 달성을 보증하는 게이트의 현재 실패 상태**다.
