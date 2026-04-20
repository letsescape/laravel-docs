# E2E 테스트 리스트 — 메인 페이지 콘텐츠

원본 Laravel.com (v13.x, 2026-03-25 기준) 메인 페이지 콘텐츠를 Playwright로 검증한 테스트 리스트입니다.

**뷰포트 브레이크포인트:**
- 데스크톱: 1280px
- 태블릿: 768px
- 모바일: 430px

---

## `homepage.spec.ts` — 메인 페이지 콘텐츠

### 히어로 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| H-1 | 메인 헤드라인 | h1 "The clean stack for Artisans and agents." |
| H-2 | 서브 텍스트 | "Laravel is batteries-included so everyone can build and ship web apps at ridiculous speed." |
| H-3 | View framework docs 버튼 | "View framework docs" → `/docs` |
| H-4 | 히어로 일러스트레이션 SVG 표시 | 우측에 메인 일러스트레이션 SVG(`absolute right-0 bottom-0`)가 표시되고 너비 > 0인지 |
| H-5 | 일러스트레이션 940px 미만 숨김 | 메인 일러스트레이션 SVG에 `max-[940px]:hidden` 클래스가 적용되어 있는지 |
| H-6 | SVG 내 도메인 텍스트 (v13) | 일러스트레이션 SVG 내 `<text>` 요소에 "v13.laravel.cloud" 텍스트가 존재하는지 |
| H-7 | SVG 내 도메인 텍스트 (skills) | 일러스트레이션 SVG 내 `<text>` 요소에 "skills.laravel.cloud" 텍스트가 존재하는지 |
| H-8 | SVG 내 내장 이미지 | 일러스트레이션 SVG 내 `<image>` 요소가 `/images/home/taylor-otwell.avif`를 참조하는지 |
| H-9 | 플로팅 아이콘 SVG | 히어로 오버레이 영역에 플로팅 아이콘 SVG가 19개 존재하는지 |

### AI Framework 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| AF-1 | 섹션 헤딩 | h2 "Ship web apps with the AI-enabled framework" |
| AF-2 | Toggle AI 버튼 | "Toggle AI" 버튼이 존재하고 `pressed` 상태인지 |
| AF-3 | 서브 텍스트 | "We're ready when you're ready" |

### 프레임워크 상세 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| FD-1 | 섹션 헤딩 | h3 "A framework for developers and agents" |
| FD-2 | 설명 텍스트 | "Laravel has opinions on everything..." |
| FD-3 | 기능 목록 4개 | Starter kits, AI SDK, Database ORM, Open source ecosystem |
| FD-4 | Explore 링크 | "Explore the framework" → `laravel.com/docs/` |
| FD-5 | 코드 카테고리 탭 8개 | Auth, AI SDK, ORM, Migrations, Validation, Storage, Queues, Testing |
| FD-6 | 기본 활성 카테고리 | "Auth" 탭이 `pressed` 상태 |
| FD-7 | 코드 파일 탭 | "web.php"(`selected`), "UserController.php" 2개 |
| FD-8 | 코드 내용 | web.php에 `Route::get('/dashboard'...` 코드 표시 |
| FD-9 | 카테고리 탭 전환 | 다른 카테고리 클릭 시 코드 내용 변경 |
| FD-10 | 파일 탭 전환 | "UserController.php" 클릭 시 코드 내용 변경 |

### Laravel Cloud 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| CL-1 | 섹션 헤딩 | h3 "Laravel Cloud takes you from local to live in seconds" |
| CL-2 | 설명 텍스트 | "No more guessing how many servers you need..." |
| CL-3 | 기능 목록 2개 | Full control via dashboard or CLI, Instantly add databases... |
| CL-4 | CTA 링크 | "Explore Laravel Cloud" → `cloud.laravel.com` |
| CL-5 | 오토스케일 일러스트레이션 컨테이너 | 일러스트레이션 영역(`overflow-hidden`, `aria-hidden="true"`)이 표시되는지 |
| CL-6 | 오토스케일 SVG | 메인 SVG(viewBox `0 0 748 274`)가 렌더링되는지 |
| CL-7 | 상태 배지 텍스트 | "Idling", "Scaling up", "Scaling down" 3개 배지가 존재하는지 |
| CL-8 | 활성 배지 1개 표시 | 상태 배지 중 `opacity: 1`인 배지가 정확히 1개인지 |

### Preview Environments 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| PE-1 | 섹션 헤딩 | h3 "Check pull requests from your team (or agents) in preview environments" |
| PE-2 | 설명 텍스트 | "Review every change in Cloud's zero-risk..." |
| PE-3 | 기능 목록 2개 | Integrates seamlessly with GitHub Actions, Test migrations... |
| PE-4 | CTA 링크 | "Explore Preview Environments" → `cloud.laravel.com/docs/preview-environments` |
| PE-5 | 파이프라인 일러스트레이션 SVG | 일러스트레이션 SVG(viewBox `0 0 524 398`)가 렌더링되는지 |
| PE-6 | SVG 내 도메인 텍스트 | 일러스트레이션 SVG 내 `<text>` 요소에 "laravel-ai.laravel.cloud", "skills.laravel.cloud" 텍스트가 존재하는지 |

### Nightwatch 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| NW-1 | 섹션 헤딩 | h3 "Monitor and fix issues with Nightwatch" |
| NW-2 | 설명 텍스트 | "Laravel Nightwatch gives full observability..." |
| NW-3 | 기능 목록 3개 | Fix errors..., Trace requests..., Let agents fix... |
| NW-4 | CTA 링크 | "Explore Nightwatch" → `nightwatch.laravel.com` |
| NW-5 | 대시보드 이미지 | "Nightwatch dashboard screenshot" alt 이미지 표시 |

### Frontend 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| FE-1 | 섹션 헤딩 | h3 "The best partner to any front-end" |
| FE-2 | 설명 텍스트 | "Easily craft frontend experiences with React, Vue, or Svelte..." |
| FE-3 | CTA 링크 | "Explore front-ends" → `laravel.com/docs/frontend` |
| FE-4 | 코드 탭 | users.svelte, users.tsx, users.vue, users.blade.php 4개 |

### CTA 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| CT-1 | 섹션 헤딩 | h2 "Create without limits. What will you ship?" |
| CT-2 | Deploy on Cloud 버튼 | → `cloud.laravel.com` |
| CT-3 | View framework docs 버튼 | → `/docs` |

### Events 섹션 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| E-1 | 섹션 라벨 | "[Events]" 라벨 텍스트 |
| E-2 | 섹션 헤딩 | h2 "We'll see you in {도시명}" (로테이션) |
| E-3 | 설명 텍스트 | "Laravel is best known for its amazing community..." |
| E-4 | Find nearby meetups 링크 | → `/events` |
| E-5 | 이벤트 카드 4개 | Laravel Live Japan, Laravel Live UK, Laracon US, Laravel Live Denmark (이름, 날짜, 도시, 국가코드) |
| E-6 | Claim your ticket 링크 | 각 카드의 URL 검증 (`laravellive.jp/en`, `laravellive.uk`, `laracon.us`, `laravellive.dk`) |
| E-7 | 이벤트 네비게이션 | "Previous event", "Next event" 버튼 |

### 푸터 (데스크톱)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| FT-1 | 푸터 표시 | 푸터 영역이 보이는지 |
| FT-2 | 로고 및 태그라인 | Laravel 로고 + "Laravel is the most productive way to build, deploy, and monitor software." |
| FT-3 | 소셜 링크 4개 | GitHub, X, YouTube, Discord |
| FT-4 | 저작권 및 하단 링크 | "© 2026 Laravel", Legal(`/legal`), Status(`status.laravel.com`) |
| FT-5 | Products 컬럼 | Cloud, Forge, Nightwatch, Vapor, Nova (5개) |
| FT-6 | Packages 컬럼 | Cashier, Dusk, Horizon, Octane, Scout, Pennant, Pint, Sail, Sanctum, Socialite, Telescope, Pulse, Reverb, Echo (14개) |
| FT-7 | Resources 컬럼 | Documentation, Starter Kits, Release Notes, Blog, News, Community, Larabelles, Learn, Jobs, Careers, Trust (11개) |
| FT-8 | Partners 컬럼 | Bacancy, CACI Limited, byte5, Jump24, Swoo, Tighten, 64 Robots, Threadable, UCodeSoft, Kirschbaum (10개) + "See All" |
| FT-9 | 하단 Laravel 워드마크 | 푸터 하단에 대형 Laravel SVG 로고(viewBox `0 0 1280 308`, `text-laravel-red`)가 표시되는지 |

### 반응형 — 태블릿 (768px)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| HR-1 | 가로 스크롤 없음 | `scrollWidth`가 뷰포트 너비를 초과하지 않는지 |
| HR-2 | 푸터 세로 스택 | 4개 컬럼이 세로로 스택되는지 |
| HR-3 | 히어로 일러스트레이션 숨김 | 데스크톱의 우측 일러스트레이션 SVG(`max-[940px]:hidden`)가 768px에서 표시되지 않는지 |
| HR-4 | 가로 스크롤 없음(하단) | 페이지 하단까지 스크롤 후 `scrollWidth`가 뷰포트 너비를 초과하지 않는지 |

### 반응형 — 모바일 (430px)

| # | 테스트명 | 검증 내용 |
|---|---------|----------|
| HR-5 | 히어로 텍스트 오버플로우 없음 | h1 텍스트가 가로 오버플로우 없이 보이는지 |
| HR-6 | CTA 버튼 표시 | "View framework docs" 버튼 표시 |
| HR-7 | 코드 카테고리 탭 | 8개 카테고리 탭이 가로 스크롤 가능한 형태로 표시되는지 |
| HR-8 | 이벤트 카드 + 네비게이션 | 이벤트 카드 표시 + Previous/Next 버튼으로 탐색 가능 |
| HR-9 | 푸터 세로 스택 | 4개 컬럼이 세로로 스택되는지 |
| HR-10 | 가로 스크롤 없음 | `scrollWidth`가 뷰포트 너비를 초과하지 않는지 |

---

## 요약

| 뷰포트 | 테스트 수 |
|---------|----------|
| 데스크톱 | 64개 |
| 태블릿 | 4개 |
| 모바일 | 10개 |
| **합계** | **78개** |
