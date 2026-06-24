<!-- # AI Assisted Development -->
# AI Assisted Development

 - [Introduction](#introduction)
     - [Why Laravel for AI Development?](#why-laravel-for-ai-development)
 - [Laravel Boost](#laravel-boost)
     - [Installation](#installation)
     - [Available Tools](#available-tools)
     - [AI Guidelines](#ai-guidelines)
     - [Agent Skills](#agent-skills)
     - [Documentation Search](#documentation-search)
     - [Agents Integration](#agents-integration)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel is uniquely positioned to be the best framework for AI assisted and agentic development. The rise of AI coding agents like [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), and [GitHub Copilot](https://github.com/features/copilot) has transformed how developers write code. These tools can generate entire features, debug complex issues, and refactor code at unprecedented speed - but their effectiveness depends heavily on how well they understand your codebase. -->
Laravel은 AI 지원 개발과 에이전트 기반 개발에 가장 적합한 프레임워크가 될 수 있는 독보적인 위치에 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot) 같은 AI 코딩 에이전트의 등장은 개발자가 코드를 작성하는 방식을 바꾸어 놓았습니다. 이러한 도구는 전체 기능을 생성하고, 복잡한 문제를 디버깅하며, 전례 없는 속도로 코드를 리팩터링할 수 있습니다. 하지만 그 효과는 도구가 코드베이스를 얼마나 잘 이해하는지에 크게 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
<!-- ### Why Laravel for AI Development? -->
### Why Laravel for AI Development?

<!-- Laravel's opinionated conventions and well-defined structure make it an ideal framework for AI assisted development. When you ask an AI agent to add a controller, it knows exactly where to place it. When you need a new migration, the naming conventions and file locations are predictable. This consistency eliminates the guesswork that often trips up AI tools in more flexible frameworks. -->
Laravel의 명확한 관례와 잘 정의된 구조는 AI 지원 개발에 이상적인 프레임워크가 되게 합니다. AI 에이전트에게 컨트롤러를 추가해 달라고 요청하면, 에이전트는 그것을 어디에 배치해야 하는지 정확히 알고 있습니다. 새로운 마이그레이션이 필요할 때도 이름 지정 규칙과 파일 위치를 예측할 수 있습니다. 이러한 일관성은 더 유연한 프레임워크에서 AI 도구가 자주 겪는 추측 과정을 줄여 줍니다.

<!-- Beyond file organization, Laravel's expressive syntax and comprehensive documentation give AI agents the context they need to generate accurate, idiomatic code. Features like Eloquent relationships, form requests, and middleware follow patterns that agents can reliably understand and replicate. The result is AI-generated code that looks like it was written by a seasoned Laravel developer, not stitched together from generic PHP snippets. -->
파일 구성뿐만 아니라, Laravel의 표현력 있는 문법과 포괄적인 문서는 AI 에이전트가 정확하고 Laravel다운 코드를 생성하는 데 필요한 컨텍스트를 제공합니다. Eloquent 연관관계, form requests, middleware 같은 기능은 에이전트가 안정적으로 이해하고 재현할 수 있는 패턴을 따릅니다. 그 결과 AI가 생성한 코드는 일반적인 PHP 코드 조각을 이어 붙인 것처럼 보이지 않고, 숙련된 Laravel 개발자가 작성한 코드처럼 보입니다.

<a name="laravel-boost"></a>
<!-- ## Laravel Boost -->
## Laravel Boost

<!-- [Laravel Boost](https://github.com/laravel/boost) bridges the gap between AI coding agents and your Laravel application. Boost is an MCP (Model Context Protocol) server equipped with over 15 specialized tools that provide AI agents with deep insight into your application's structure, database, routes, and more. When you install Boost, your AI agent transforms from a general-purpose code assistant into a Laravel expert that understands your specific application. -->
[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 메워 줍니다. Boost는 애플리케이션의 구조, 데이터베이스, 라우트 등에 대한 깊은 통찰을 AI 에이전트에 제공하는 15개 이상의 전문 도구를 갖춘 MCP(Model Context Protocol) 서버입니다. Boost를 설치하면 AI 에이전트는 범용 코드 도우미에서, 사용자의 특정 애플리케이션을 이해하는 Laravel 전문가로 바뀝니다.

<!-- Boost provides three major capabilities: a suite of MCP tools for inspecting and interacting with your application, composable AI guidelines crafted specifically for the Laravel ecosystem, and a powerful documentation API containing over 17,000 pieces of Laravel-specific knowledge. -->
Boost는 세 가지 주요 기능을 제공합니다. 애플리케이션을 검사하고 상호작용하기 위한 MCP 도구 모음, Laravel 생태계에 맞게 특별히 작성된 조합 가능한 AI 가이드라인, 그리고 Laravel 관련 지식 17,000개 이상을 담은 강력한 문서 API입니다.

<a name="installation"></a>
<!-- ### Installation -->
### Installation

<!-- Boost can be installed in Laravel 10, 11, 12, and 13 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency: -->
Boost는 PHP 8.1 이상에서 실행되는 Laravel 10, 11, 12, 13 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치합니다.

```shell
composer require laravel/boost --dev
```

<!-- Once installed, run the interactive installer: -->
설치가 완료되면 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

<!-- The installer will auto-detect your IDE and AI agents, allowing you to select the integrations that make sense for your project. Boost will generate the necessary configuration files, such as `.mcp.json` for MCP-compatible editors and guideline files for AI context. -->
설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하며, 프로젝트에 적합한 통합을 선택할 수 있게 해 줍니다. Boost는 MCP 호환 에디터를 위한 `.mcp.json`, AI 컨텍스트를 위한 가이드라인 파일 등 필요한 설정 파일을 생성합니다.

> [!NOTE]
> 각 개발자가 자신의 환경을 직접 설정하도록 하고 싶다면 `.mcp.json`, `CLAUDE.md`, `boost.json` 같은 생성된 설정 파일을 `.gitignore`에 안전하게 추가할 수 있습니다.

<a name="available-tools"></a>
<!-- ### Available Tools -->
### Available Tools

<!-- Boost exposes a comprehensive set of tools to AI agents via the Model Context Protocol. These tools allow agents to deeply understand and interact with your Laravel application: -->
Boost는 Model Context Protocol을 통해 AI 에이전트에 포괄적인 도구 모음을 제공합니다. 이러한 도구를 통해 에이전트는 Laravel 애플리케이션을 깊이 이해하고 상호작용할 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **Application Introspection** - Query your PHP and Laravel versions, list installed packages, and inspect your application's configuration and environment variables.
- **Database Tools** - Inspect your database schema, execute read-only queries, and understand your data structure without leaving the conversation.
- **Route Inspection** - List all registered routes with their middleware, controllers, and parameters.
- **Artisan Commands** - Discover available Artisan commands and their arguments, enabling agents to suggest and execute the right commands for your task.
- **Log Analysis** - Read and analyze your application's log files to help debug issues.
- **Browser Logs** - Access browser console logs and errors when developing with Laravel's frontend tools.
- **Tinker Integration** - Execute PHP code in the context of your application via Laravel Tinker, allowing agents to test hypotheses and verify behavior.
- **Documentation Search** - Search Laravel ecosystem documentation with results tailored to your installed package versions.
-->
- **애플리케이션 내부 검사** - PHP와 Laravel 버전을 조회하고, 설치된 패키지를 나열하며, 애플리케이션의 설정과 환경 변수를 검사합니다.
- **데이터베이스 도구** - 대화에서 벗어나지 않고 데이터베이스 스키마를 검사하고, 읽기 전용 쿼리를 실행하며, 데이터 구조를 이해합니다.
- **라우트 검사** - 등록된 모든 라우트를 middleware, 컨트롤러, 파라미터와 함께 나열합니다.
- **Artisan 명령어** - 사용 가능한 Artisan 명령어와 해당 인수를 확인하여, 에이전트가 작업에 맞는 명령어를 제안하고 실행할 수 있게 합니다.
- **로그 분석** - 문제 디버깅을 돕기 위해 애플리케이션의 로그 파일을 읽고 분석합니다.
- **브라우저 로그** - Laravel의 프론트엔드 도구로 개발할 때 브라우저 콘솔 로그와 오류에 접근합니다.
- **Tinker 통합** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드를 실행하여, 에이전트가 가설을 테스트하고 동작을 검증할 수 있게 합니다.
- **문서 검색** - 설치된 패키지 버전에 맞춘 결과로 Laravel 생태계 문서를 검색합니다.

<!-- </div> -->
</div>

<a name="ai-guidelines"></a>
<!-- ### AI Guidelines -->
### AI Guidelines

<!-- Boost includes a comprehensive set of AI guidelines specifically crafted for the Laravel ecosystem. These guidelines teach AI agents how to write idiomatic Laravel code, follow framework conventions, and avoid common pitfalls. Guidelines are composable and version-aware, meaning agents receive instructions appropriate for your exact package versions. -->
Boost에는 Laravel 생태계를 위해 특별히 작성된 포괄적인 AI 가이드라인이 포함되어 있습니다. 이 가이드라인은 AI 에이전트가 Laravel다운 코드를 작성하고, 프레임워크 관례를 따르며, 흔한 실수를 피하는 방법을 알려 줍니다. 가이드라인은 조합 가능하고 버전을 인식하므로, 에이전트는 사용자의 정확한 패키지 버전에 맞는 지침을 받습니다.

<!-- Guidelines are available for Laravel itself and over 16 packages in the Laravel ecosystem, including: -->
가이드라인은 Laravel 자체와 Laravel 생태계의 16개 이상의 패키지에 대해 제공되며, 여기에는 다음이 포함됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Livewire (2.x, 3.x, and 4.x)
- Inertia.js (React, Svelte, and Vue variants)
- Tailwind CSS (3.x and 4.x)
- Filament (3.x and 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- And many more
-->
- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Svelte, Vue 변형)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 그 외 다수

<!-- </div> -->
</div>

<!-- When you run `boost:install`, Boost automatically detects which packages your application uses and assembles the relevant guidelines into your project's AI context files. -->
`boost:install`을 실행하면 Boost는 애플리케이션이 사용하는 패키지를 자동으로 감지하고, 관련 가이드라인을 프로젝트의 AI 컨텍스트 파일에 구성합니다.

<a name="agent-skills"></a>
<!-- ### Agent Skills -->
### Agent Skills

<!-- [Agent Skills](https://agentskills.io/home) are lightweight, targeted knowledge modules that agents can activate on-demand when working on specific domains. Unlike guidelines, which are loaded upfront, skills allow detailed patterns and best practices to be loaded only when relevant, reducing context bloat and improving the relevance of AI-generated code. -->
[Agent Skills](https://agentskills.io/home)는 에이전트가 특정 도메인에서 작업할 때 필요에 따라 활성화할 수 있는 가볍고 목적이 뚜렷한 지식 모듈입니다. 처음부터 로드되는 가이드라인과 달리, skills는 관련이 있을 때만 자세한 패턴과 모범 사례를 로드할 수 있게 하여 컨텍스트가 불필요하게 커지는 것을 줄이고 AI 생성 코드의 관련성을 높입니다.

<!-- Skills are available for popular Laravel packages like Livewire, Inertia, Tailwind CSS, Pest, and more. When you run `boost:install` and select skills as a feature, skills are automatically installed based on the packages detected in your `composer.json`. -->
Skills는 Livewire, Inertia, Tailwind CSS, Pest 등 인기 있는 Laravel 패키지에 대해 제공됩니다. `boost:install`을 실행하고 기능으로 skills를 선택하면, `composer.json`에서 감지된 패키지를 기반으로 skills가 자동 설치됩니다.

<a name="documentation-search"></a>
<!-- ### Documentation Search -->
### Documentation Search

<!-- Boost includes a powerful documentation API that gives AI agents access to over 17,000 pieces of Laravel ecosystem documentation. Unlike generic web searches, this documentation is indexed, vectorized, and filtered to match your exact package versions. -->
Boost에는 AI 에이전트가 Laravel 생태계 문서 17,000개 이상에 접근할 수 있게 해 주는 강력한 문서 API가 포함되어 있습니다. 일반적인 웹 검색과 달리, 이 문서는 사용자의 정확한 패키지 버전에 맞게 색인화되고, 벡터화되며, 필터링됩니다.

<!-- When an agent needs to understand how a feature works, it can search Boost's documentation API and receive accurate, version-specific information. This eliminates the common problem of AI agents suggesting deprecated methods or syntax from older framework versions. -->
에이전트가 어떤 기능이 어떻게 동작하는지 이해해야 할 때 Boost의 문서 API를 검색하여 정확하고 버전에 맞는 정보를 받을 수 있습니다. 이를 통해 AI 에이전트가 오래된 프레임워크 버전의 더 이상 권장되지 않는 메서드나 문법을 제안하는 흔한 문제를 없앨 수 있습니다.

<a name="agents-integration"></a>
<!-- ### Agents Integration -->
### Agents Integration

<!-- Boost integrates with popular IDEs and AI tools that support the Model Context Protocol. For detailed setup instructions for Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, and Junie, see the [Set Up Your Agents](/docs/13.x/boost#set-up-your-agents) section of the Boost documentation. -->
Boost는 Model Context Protocol을 지원하는 인기 IDE 및 AI 도구와 통합됩니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie에 대한 자세한 설정 지침은 Boost 문서의 [Set Up Your Agents](/docs/13.x/boost#set-up-your-agents) 섹션을 참고하세요.
