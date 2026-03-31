# E2E 테스트 리스트 — 네비게이션 (Navbar)

원본 Laravel.com (v13.x, 2026-03-25 기준) 메인 페이지 네비게이션을 Playwright로 검증한 테스트 리스트입니다.

**뷰포트 브레이크포인트:**

- 데스크톱: 1280px
- 태블릿: 768px
- 모바일: 430px

---

## `navbar.spec.ts` — Navbar

### 데스크톱 (1280px)

| #    | 테스트명                     | 검증 내용                                                                                                                                  |
| ---- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| N-1  | 네비바 표시                  | `navigation "Main"`이 페이지 상단에 보이는지                                                                                               |
| N-2  | 로고 표시 및 링크            | Laravel 로고 이미지가 보이고 `/`로 링크되는지                                                                                              |
| N-3  | Framework 드롭다운 열기      | "Framework" 버튼 클릭 시 메가 메뉴가 펼쳐지는지                                                                                            |
| N-3a | Framework > Explore Laravel  | "Explore Laravel" 헤딩 아래 Overview(`/`), Changelog(`/docs/changelog`), Laravel Learn(`/learn`) 3개 항목 + 설명 텍스트                    |
| N-3b | Framework > Latest packages  | "Latest packages" 헤딩 아래 AI SDK(`/ai`), Boost(`/ai/boost`), Wayfinder(`github.com/laravel/wayfinder`) 3개 항목 + 설명 텍스트            |
| N-3c | Framework > Documentation    | "Documentation" 헤딩 아래 Installation, Agent Setup, Eloquent ORM, Artisan Console, Routing 5개 항목 + "View all"(`/docs`)                 |
| N-3d | Framework > Starter kits     | "Starter kits"(`/starter-kits`) 링크 + 코드 미리보기(users.svelte, users.tsx, users.vue, users.blade.php)                                  |
| N-4  | Products 드롭다운 열기       | "Products" 버튼 클릭 시 메가 메뉴가 펼쳐지는지                                                                                             |
| N-4a | Products > Cloud             | Cloud(`cloud.laravel.com`) — "The fastest way to deploy and scale Laravel applications", "Deploy now"                                      |
| N-4b | Products > Forge             | Forge(`forge.laravel.com`) — "Next-level server management with unparalleled control", "Manage your servers"                               |
| N-4c | Products > Nightwatch        | Nightwatch(`nightwatch.laravel.com`) — "Full observability and monitoring for Laravel apps", "Free plans available"                        |
| N-5  | Resources 드롭다운 열기      | "Resources" 버튼 클릭 시 메가 메뉴가 펼쳐지는지                                                                                            |
| N-5a | Resources > Company          | "Company" 헤딩 아래 Blog(`/blog`), Careers(`/careers`), Trust(`trust.laravel.com`), Legal(`/legal`), Status(`status.laravel.com`) 5개 항목 |
| N-5b | Resources > Social 링크      | GitHub, YouTube, X, LinkedIn, Discord 5개 소셜 링크                                                                                        |
| N-5c | Resources > Partners         | "Partners" 헤딩 아래 CACI Limited, Kirschbaum, Curotec, 64 Robots, Steadfast Collective, byte5 6개 항목 + "View all"(`/partners`)          |
| N-5d | Resources > Featured article | "Featured article" 헤딩 아래 블로그 글(제목, 날짜, 발췌문, "Read more" 링크)                                                               |
| N-6  | Events 드롭다운 열기         | "Events" 버튼 클릭 시 메가 메뉴가 펼쳐지는지                                                                                               |
| N-6a | Events > Upcoming events     | "Upcoming events" 헤딩 아래 5개 밋업 항목(날짜, 이름, 장소) + "View all"(`/community`)                                                     |
| N-6b | Events > Featured events     | Laravel Live Japan, Laravel Live UK, Laracon US 등 컨퍼런스 카드(이미지, 이름, 날짜, 도시, 국가)                                           |
| N-7  | Docs 링크                    | "Docs" 링크가 보이고 `/docs`로 연결되는지                                                                                                  |
| N-10 | 검색 버튼                    | "Search docs" 버튼이 보이고 `⌘K` 단축키 표시가 있는지                                                                                      |
| N-11 | 검색 키보드 단축키           | `Ctrl+K` 입력 시 검색 모달이 열리는지                                                                                                      |
| N-12 | 네비바 상단 고정             | 스크롤 시에도 네비바가 상단에 고정(`sticky`)되는지                                                                                         |
| N-13 | 네비바 전체 요소 확인        | 로고, 드롭다운 5개, Search docs(⌘K) **모두 표시**                                                                                          |

### 태블릿 (768px)

| #    | 테스트명              | 검증 내용                                                                |
| ---- | --------------------- | ------------------------------------------------------------------------ |
| N-14 | 네비바 좌측           | 로고 + Framework/Products/Resources/Events 드롭다운 + Docs 링크 **표시** |
| N-15 | 네비바 우측 요소 숨김  | Search docs가 **숨겨지는지**                                             |
| N-16 | 햄버거 메뉴 없음      | "Open navigation menu" 버튼이 **존재하지 않는지**                        |

### 모바일 (430px)

| #    | 테스트명                    | 검증 내용                                                                                               |
| ---- | --------------------------- | ------------------------------------------------------------------------------------------------------- |
| N-17 | 햄버거 메뉴 표시            | 로고 + "Open navigation menu" 버튼만 표시되고, 드롭다운/Search 모두 **숨겨지는지**                      |
| N-18 | 햄버거 메뉴 열기/닫기       | 햄버거 클릭 시 드로어 펼쳐지고, 닫기 버튼으로 닫히는지                                                  |
| N-19 | 드로어 > Framework 아코디언 | Overview, Starter Kits, Release Notes, Documentation, Laravel Learn — 단순 리스트 5개                   |
| N-20 | 드로어 > Products 아코디언  | Laravel Cloud, Forge, Nightwatch, Nova — **4개** (데스크톱은 3개)                                       |
| N-21 | 드로어 > Resources 아코디언 | Blog, Partners, Careers, Trust, Legal, Status — 단순 리스트 6개                                         |
| N-22 | 드로어 > Events 직접 링크   | Events가 `/community`로의 직접 링크 (드롭다운 아님)                                                     |
| N-23 | 드로어 > Docs 직접 링크     | Docs(`/docs`) 링크 존재                                                                                 |

---

## 요약

| 뷰포트   | 테스트 수 |
| -------- | --------- |
| 데스크톱 | 23개      |
| 태블릿   | 3개       |
| 모바일   | 7개       |
| **합계** | **33개**  |
