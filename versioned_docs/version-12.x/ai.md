# AI 지원 개발 (AI Assisted Development)

- [소개](#introduction)
    - [AI 개발에 Laravel이 적합한 이유](#why-laravel-for-ai-development)
- [Laravel Boost](#laravel-boost)
    - [설치](#installation)
    - [사용 가능한 도구](#available-tools)
    - [AI 가이드라인](#ai-guidelines)
    - [에이전트 스킬](#agent-skills)
    - [문서 검색](#documentation-search)
    - [에이전트 통합](#agents-integration)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 및 에이전트 기반 개발에 가장 적합한 프레임워크라는 점에서 독보적인 위치를 차지하고 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장으로 개발자가 코드를 작성하는 방식이 크게 변화했습니다. 이러한 도구들은 전체 기능 생성, 복잡한 문제 디버깅, 빠른 코드 리팩토링까지 이전과는 비교할 수 없는 속도로 작업할 수 있도록 도와주지만, 그 효과는 여러분의 코드베이스를 얼마나 잘 이해하느냐에 크게 달려 있습니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 Laravel이 적합한 이유

Laravel이 제공하는 명확한 규칙(convention)과 체계적인 구조는 AI 지원 개발에 매우 이상적입니다. 예를 들어, AI 에이전트에게 컨트롤러를 추가하라고 하면, 어디에 파일을 두어야 할지 정확히 알고 작업합니다. 새로운 마이그레이션이 필요할 때도, 파일명이나 위치가 예측 가능하여 혼란이 없습니다. 이러한 일관성 덕분에, 다른 유연한 프레임워크에서는 자주 문제가 되는 ‘추측’이 완전히 사라집니다.

디렉토리 구조 외에도, Laravel의 직관적인 문법과 방대한 공식 문서는 AI 에이전트가 정확하고 Laravel다운 코드를 생성하는 데 중요한 맥락 정보를 제공합니다. Eloquent 연관관계, Form Request, 미들웨어(Middleware) 등 많은 기능들이 패턴화되어 있어 AI가 쉽게 이해하고 재현할 수 있습니다. 그 결과, AI가 생성한 코드는 마치 숙련된 Laravel 개발자가 작성한 것처럼 자연스러우며, 단순한 PHP 코드 조각을 이어붙인 수준이 아닙니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 여러분의 Laravel 애플리케이션 사이를 연결해주는 도구입니다. Boost는 MCP(Model Context Protocol) 서버로, AI 에이전트가 애플리케이션의 구조, 데이터베이스, 라우트 등 깊은 정보를 파악할 수 있게 돕는 15개 이상의 특화 도구를 제공합니다. Boost를 설치하면, AI 에이전트는 범용 코드 도우미에서 여러분의 애플리케이션을 이해하는 ‘Laravel 전문가’로 변신합니다.

Boost가 제공하는 세 가지 주요 기능은 다음과 같습니다: 애플리케이션 점검 및 상호작용을 위한 MCP 도구 모음, Laravel에 특화된 조합형 AI 가이드라인, 17,000개 이상의 Laravel 관련 지식을 담고 있는 강력한 문서화 API입니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상이 동작하는 Laravel 10, 11, 12 애플리케이션에서 설치할 수 있습니다. 다음과 같이 개발 의존성으로 Boost를 설치하세요:

```shell
composer require laravel/boost --dev
```

설치 후에는 인터랙티브 설치 프로그램을 실행합니다:

```shell
php artisan boost:install
```

설치 프로그램은 사용 중인 IDE와 AI 에이전트를 자동으로 감지하여, 프로젝트에 필요한 통합 기능을 직접 선택할 수 있도록 도와줍니다. 설치가 완료되면, `.mcp.json`과 같은 MCP 호환 에디터용 설정 파일과 AI 맥락용 가이드라인 파일이 자동으로 생성됩니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json`와 같이 생성된 설정 파일들은 개발자마다 각자 환경을 구성하도록 `.gitignore`에 추가해도 무방합니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에게 다양한 도구를 제공합니다. 이 도구들은 에이전트가 여러분의 Laravel 애플리케이션을 심층적으로 이해하고 상호작용할 수 있게 해줍니다.

<div class="content-list" markdown="1">

- **애플리케이션 점검** – PHP/Laravel 버전 조회, 설치된 패키지 목록 확인, 애플리케이션 환경 변수와 설정 정보 점검 등
- **데이터베이스 도구** – 데이터베이스 스키마 점검, 읽기 전용 쿼리 실행, 데이터 구조 이해 등
- **라우트 점검** – 등록된 모든 라우트 리스트, 미들웨어, 컨트롤러, 파라미터 확인
- **Artisan 명령어** – 사용 가능한 Artisan 명령어 및 인수 탐색, 적합한 명령 추천 및 실행 지원
- **로그 분석** – 애플리케이션 로그 파일을 읽고 분석하여 문제 해결 지원
- **브라우저 로그** – 프론트엔드 개발 중 브라우저 콘솔 로그 및 오류 접근
- **Tinker 통합** – Laravel Tinker를 통해 애플리케이션 맥락에서 PHP 코드 실행, 동작 검증 및 가설 테스트
- **문서 검색** – 설치된 패키지 버전에 최적화된 Laravel 에코시스템 문서를 검색

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost는 Laravel 에코시스템에 최적화된 방대한 AI 가이드라인을 기본 제공합니다. 이 가이드라인은 AI 에이전트에게 Laravel다운 코드 작성법, 프레임워크 규칙 준수, 자주 발생하는 실수 방지법 등을 안내합니다. 또한 조합형(composable), 버전 인식(version-aware) 방식으로, 사용 중인 패키지 버전에 맞춘 지침이 제공됩니다.

가이드라인은 Laravel 자체뿐 아니라, 다음을 포함한 16개 이상의 라이브러리와 패키지에 대해 준비되어 있습니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Svelte, Vue용 변형 포함)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 기타 다수

</div>

`boost:install` 명령 실행 시, Boost가 여러분의 애플리케이션에서 사용하는 패키지를 자동으로 탐지해, 관련 가이드라인을 AI 맥락 파일에 조합하여 포함시킵니다.

<a name="agent-skills"></a>
### 에이전트 스킬

[에이전트 스킬](https://agentskills.io/home)은 에이전트가 특정 도메인 작업 시 필요한 지식만을 선택적으로 불러올 수 있게 해주는 경량 지식 모듈입니다. 가이드라인이 미리 전체 맥락에 로드되는 데 반해, 스킬은 실제로 필요할 때만 세부 패턴과 모범 사례를 불러오므로 컨텍스트가 불필요하게 커지는 것을 막고, AI가 더 관련성 높은 코드를 작성하도록 돕습니다.

스킬은 Livewire, Inertia, Tailwind CSS, Pest 등 인기 Laravel 패키지에 대해 제공됩니다. `boost:install`에서 스킬 기능을 선택하면, 여러분의 `composer.json`에서 감지한 패키지 정보를 바탕으로 관련 스킬이 자동 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색

Boost는 AI 에이전트에게 17,000개 이상의 Laravel 에코시스템 문서에 접근할 수 있는 강력한 문서 API를 제공합니다. 일반적인 웹 검색과 달리, 이 문서는 색인화 및 벡터화되어 설치된 패키지 버전에 최적화된 결과만 제공합니다.

에이전트가 어떤 기능의 동작 방식을 알아야 할 때, Boost의 문서 API를 검색해 정확하고 버전 일치하는 정보를 받을 수 있습니다. 이를 통해 AI가 구버전 문서의 폐기된 메서드나 잘못된 문법을 추천하는 문제를 효과적으로 방지할 수 있습니다.

<a name="agent-integration"></a>
### 에이전트 통합

Boost는 Model Context Protocol을 지원하는 주요 IDE와 AI 도구와 통합할 수 있습니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie 등과의 상세한 연동 방법은 Boost 문서의 [에이전트 설정](/docs/12.x/boost#set-up-your-agents) 섹션을 참고하세요.