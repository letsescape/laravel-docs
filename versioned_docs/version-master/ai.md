# AI 지원 개발 (AI Assisted Development)

 - [소개](#introduction)
     - [AI 개발에 Laravel을 사용하는 이유](#why-laravel-for-ai-development)
 - [Laravel Boost](#laravel-boost)
     - [설치](#installation)
     - [사용 가능한 도구](#available-tools)
     - [AI 가이드라인](#ai-guidelines)
     - [Agent Skills](#agent-skills)
     - [문서 검색](#documentation-search)
     - [에이전트 통합](#agents-integration)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 개발(AI assisted development)과 에이전트 기반 개발(agentic development)에 매우 적합한 프레임워크입니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장으로 개발자가 코드를 작성하는 방식이 크게 변화했습니다. 이러한 도구는 전체 기능을 생성하고, 복잡한 문제를 디버깅하며, 코드를 매우 빠른 속도로 리팩터링할 수 있습니다. 하지만 이러한 도구의 효과는 AI가 여러분의 코드베이스를 얼마나 잘 이해하느냐에 크게 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 Laravel을 사용하는 이유

Laravel은 명확한 규약(opinionated conventions)과 잘 정의된 구조를 갖추고 있어 AI 지원 개발에 매우 이상적인 프레임워크입니다. 예를 들어 AI 에이전트에게 컨트롤러를 추가해 달라고 요청하면, 해당 파일을 정확히 어디에 배치해야 하는지 알고 있습니다. 새로운 마이그레이션이 필요할 때도 파일 이름 규칙과 위치가 예측 가능하게 정해져 있습니다. 이러한 일관성 덕분에 보다 유연한 프레임워크에서 AI 도구가 흔히 겪는 추측이나 혼란을 크게 줄일 수 있습니다.

파일 구조뿐만 아니라, Laravel의 표현력이 풍부한 문법과 포괄적인 문서는 AI 에이전트가 정확하고 관용적인(프레임워크 스타일에 맞는) 코드를 생성하는 데 필요한 충분한 맥락을 제공합니다. Eloquent 연관관계(relationships), Form Request, Middleware 같은 기능들은 일정한 패턴을 따르기 때문에 AI 에이전트가 이를 안정적으로 이해하고 재현할 수 있습니다. 그 결과 AI가 생성한 코드는 일반적인 PHP 코드 조각을 이어 붙인 형태가 아니라, 숙련된 Laravel 개발자가 작성한 것처럼 자연스럽게 보입니다.

<a name="laravel-boost"></a>
## Laravel Boost

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 연결해 주는 도구입니다. Boost는 MCP(Model Context Protocol) 서버로, 15개 이상의 전문 도구를 제공하여 AI 에이전트가 애플리케이션의 구조, 데이터베이스, 라우트 등을 깊이 이해할 수 있도록 합니다. Boost를 설치하면 일반적인 코드 보조 도구였던 AI 에이전트가 여러분의 특정 Laravel 애플리케이션을 이해하는 Laravel 전문가로 변하게 됩니다.

Boost는 세 가지 주요 기능을 제공합니다. 애플리케이션을 검사하고 상호작용하기 위한 MCP 도구 모음, Laravel 생태계에 맞게 설계된 조합형 AI 가이드라인, 그리고 17,000개 이상의 Laravel 관련 지식을 포함한 강력한 문서 API입니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상을 사용하는 Laravel 10, 11, 12 애플리케이션에서 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치합니다.

```shell
composer require laravel/boost --dev
```

설치가 완료되면 다음과 같이 인터랙티브 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

설치 프로그램은 여러분의 IDE와 AI 에이전트를 자동으로 감지하고, 프로젝트에 맞는 통합 옵션을 선택할 수 있도록 안내합니다. 이후 Boost는 MCP 호환 에디터를 위한 `.mcp.json` 파일이나 AI 컨텍스트를 위한 가이드라인 파일 등 필요한 설정 파일을 생성합니다.

> [!NOTE]
> `.mcp.json`, `CLAUDE.md`, `boost.json`과 같은 생성된 설정 파일은 각 개발자가 자신의 환경을 개별적으로 구성하도록 하고 싶다면 `.gitignore`에 안전하게 추가할 수 있습니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에 다양한 도구를 제공합니다. 이러한 도구를 사용하면 에이전트가 Laravel 애플리케이션을 깊이 이해하고 상호작용할 수 있습니다.

<div class="content-list" markdown="1">

- **애플리케이션 인트로스펙션(Application Introspection)** - PHP 및 Laravel 버전을 조회하고, 설치된 패키지를 확인하며, 애플리케이션 설정과 환경 변수를 검사합니다.
- **데이터베이스 도구(Database Tools)** - 데이터베이스 스키마를 확인하고 읽기 전용 쿼리를 실행하며, 대화에서 벗어나지 않고도 데이터 구조를 이해할 수 있습니다.
- **라우트 검사(Route Inspection)** - 등록된 모든 라우트를 Middleware, 컨트롤러, 파라미터 정보와 함께 확인할 수 있습니다.
- **Artisan 명령어(Artisan Commands)** - 사용 가능한 Artisan 명령어와 인수를 확인하여 작업에 적절한 명령어를 제안하고 실행할 수 있습니다.
- **로그 분석(Log Analysis)** - 애플리케이션 로그 파일을 읽고 분석하여 문제 디버깅을 지원합니다.
- **브라우저 로그(Browser Logs)** - Laravel 프런트엔드 도구로 개발할 때 브라우저 콘솔 로그와 오류를 확인할 수 있습니다.
- **Tinker 통합(Tinker Integration)** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드를 실행하여 가설을 테스트하고 동작을 검증할 수 있습니다.
- **문서 검색(Documentation Search)** - 설치된 패키지 버전에 맞춘 Laravel 생태계 문서를 검색할 수 있습니다.

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost에는 Laravel 생태계를 위해 특별히 설계된 종합적인 AI 가이드라인이 포함되어 있습니다. 이러한 가이드라인은 AI 에이전트가 Laravel 스타일에 맞는 코드를 작성하고, 프레임워크 규칙을 따르며, 흔히 발생하는 문제를 피하도록 안내합니다. 가이드라인은 조합형(composable)이며 버전 인식(version-aware)을 지원하므로, 에이전트는 여러분이 사용하는 정확한 패키지 버전에 맞는 지침을 받게 됩니다.

가이드라인은 Laravel 자체뿐 아니라 Laravel 생태계의 16개 이상의 패키지를 지원하며, 예를 들면 다음과 같습니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Svelte, Vue 변형)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 그 외 다양한 패키지

</div>

`boost:install`을 실행하면 Boost는 애플리케이션에서 사용하는 패키지를 자동으로 감지하고, 해당 가이드라인을 프로젝트의 AI 컨텍스트 파일에 자동으로 구성합니다.

<a name="agent-skills"></a>
### Agent Skills

[Agent Skills](https://agentskills.io/home)는 특정 도메인 작업을 수행할 때 에이전트가 필요에 따라 활성화할 수 있는 가볍고 집중된 지식 모듈입니다. 가이드라인이 처음부터 로드되는 것과 달리, Skills는 필요한 상황에서만 상세한 패턴과 모범 사례(best practices)를 불러옵니다. 이를 통해 컨텍스트 크기를 줄이고 AI가 생성하는 코드의 관련성과 정확성을 높일 수 있습니다.

Skills는 Livewire, Inertia, Tailwind CSS, Pest 등 인기 있는 Laravel 패키지를 지원합니다. `boost:install` 실행 시 Skills 기능을 선택하면 `composer.json`에 감지된 패키지를 기반으로 필요한 Skills가 자동으로 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색

Boost에는 AI 에이전트가 Laravel 생태계 문서 17,000개 이상에 접근할 수 있도록 하는 강력한 문서 API가 포함되어 있습니다. 일반적인 웹 검색과 달리, 이 문서는 인덱싱되고 벡터화되어 있으며 여러분이 사용하는 정확한 패키지 버전에 맞게 필터링됩니다.

에이전트가 특정 기능의 동작 방식을 이해해야 할 때 Boost의 문서 API를 검색하면, 정확하고 버전별로 맞는 정보를 얻을 수 있습니다. 이를 통해 AI 에이전트가 오래된 프레임워크 버전의 폐기된(deprecated) 메서드나 문법을 제안하는 문제를 방지할 수 있습니다.

<a name="agent-integration"></a>
### 에이전트 통합

Boost는 Model Context Protocol을 지원하는 다양한 IDE 및 AI 도구와 통합됩니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie 설정 방법에 대한 자세한 내용은 Boost 문서의 [Set Up Your Agents](/docs/master/boost#set-up-your-agents) 섹션을 참고하시기 바랍니다.