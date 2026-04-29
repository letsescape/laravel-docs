# AI 지원 개발 (AI Assisted Development)

 - [소개](#introduction)
     - [AI 개발에 Laravel이 적합한 이유는 무엇인가요?](#why-laravel-for-ai-development)
 - [Laravel Boost](#laravel-boost)
     - [설치](#installation)
     - [사용 가능한 도구](#available-tools)
     - [AI 가이드라인](#ai-guidelines)
     - [Agent Skills](#agent-skills)
     - [문서 검색](#documentation-search)
     - [에이전트 통합](#agent-integration)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 AI 지원 개발과 에이전트 기반 개발에 가장 적합한 프레임워크가 될 수 있는 독보적인 위치에 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com), [GitHub Copilot](https://github.com/features/copilot) 같은 AI 코딩 에이전트의 등장은 개발자가 코드를 작성하는 방식을 바꾸어 놓았습니다. 이러한 도구는 전체 기능을 생성하고, 복잡한 문제를 디버깅하며, 전례 없는 속도로 코드를 리팩터링할 수 있습니다. 하지만 그 효과는 도구가 코드베이스를 얼마나 잘 이해하는지에 크게 좌우됩니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 Laravel이 적합한 이유는 무엇인가요?

Laravel의 명확한 관례와 잘 정의된 구조는 AI 지원 개발에 이상적인 프레임워크가 되게 합니다. AI 에이전트에게 컨트롤러를 추가해 달라고 요청하면, 에이전트는 그것을 어디에 배치해야 하는지 정확히 알고 있습니다. 새로운 마이그레이션이 필요할 때도 이름 지정 규칙과 파일 위치를 예측할 수 있습니다. 이러한 일관성은 더 유연한 프레임워크에서 AI 도구가 자주 겪는 추측 과정을 줄여 줍니다.

파일 구성뿐만 아니라, Laravel의 표현력 있는 문법과 포괄적인 문서는 AI 에이전트가 정확하고 Laravel다운 코드를 생성하는 데 필요한 컨텍스트를 제공합니다. Eloquent 연관관계, form requests, middleware 같은 기능은 에이전트가 안정적으로 이해하고 재현할 수 있는 패턴을 따릅니다. 그 결과 AI가 생성한 코드는 일반적인 PHP 코드 조각을 이어 붙인 것처럼 보이지 않고, 숙련된 Laravel 개발자가 작성한 코드처럼 보입니다.

<a name="laravel-boost"></a>
## Laravel Boost (Laravel Boost)

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 사이의 간극을 메워 줍니다. Boost는 애플리케이션의 구조, 데이터베이스, 라우트 등에 대한 깊은 통찰을 AI 에이전트에 제공하는 15개 이상의 전문 도구를 갖춘 MCP(Model Context Protocol) 서버입니다. Boost를 설치하면 AI 에이전트는 범용 코드 도우미에서, 사용자의 특정 애플리케이션을 이해하는 Laravel 전문가로 바뀝니다.

Boost는 세 가지 주요 기능을 제공합니다. 애플리케이션을 검사하고 상호작용하기 위한 MCP 도구 모음, Laravel 생태계에 맞게 특별히 작성된 조합 가능한 AI 가이드라인, 그리고 Laravel 관련 지식 17,000개 이상을 담은 강력한 문서 API입니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상에서 실행되는 Laravel 10, 11, 12, 13 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치합니다.

```shell
composer require laravel/boost --dev
```

설치가 완료되면 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install
```

설치 프로그램은 IDE와 AI 에이전트를 자동으로 감지하며, 프로젝트에 적합한 통합을 선택할 수 있게 해 줍니다. Boost는 MCP 호환 에디터를 위한 `.mcp.json`, AI 컨텍스트를 위한 가이드라인 파일 등 필요한 설정 파일을 생성합니다.

> [!NOTE]
> 각 개발자가 자신의 환경을 직접 설정하도록 하고 싶다면 `.mcp.json`, `CLAUDE.md`, `boost.json` 같은 생성된 설정 파일을 `.gitignore`에 안전하게 추가할 수 있습니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에 포괄적인 도구 모음을 제공합니다. 이러한 도구를 통해 에이전트는 Laravel 애플리케이션을 깊이 이해하고 상호작용할 수 있습니다.

<div class="content-list" markdown="1">

- **애플리케이션 내부 검사** - PHP와 Laravel 버전을 조회하고, 설치된 패키지를 나열하며, 애플리케이션의 설정과 환경 변수를 검사합니다.
- **데이터베이스 도구** - 대화에서 벗어나지 않고 데이터베이스 스키마를 검사하고, 읽기 전용 쿼리를 실행하며, 데이터 구조를 이해합니다.
- **라우트 검사** - 등록된 모든 라우트를 middleware, 컨트롤러, 파라미터와 함께 나열합니다.
- **Artisan 명령어** - 사용 가능한 Artisan 명령어와 해당 인수를 확인하여, 에이전트가 작업에 맞는 명령어를 제안하고 실행할 수 있게 합니다.
- **로그 분석** - 문제 디버깅을 돕기 위해 애플리케이션의 로그 파일을 읽고 분석합니다.
- **브라우저 로그** - Laravel의 프론트엔드 도구로 개발할 때 브라우저 콘솔 로그와 오류에 접근합니다.
- **Tinker 통합** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드를 실행하여, 에이전트가 가설을 테스트하고 동작을 검증할 수 있게 합니다.
- **문서 검색** - 설치된 패키지 버전에 맞춘 결과로 Laravel 생태계 문서를 검색합니다.

</div>

<a name="ai-guidelines"></a>
### AI 가이드라인

Boost에는 Laravel 생태계를 위해 특별히 작성된 포괄적인 AI 가이드라인이 포함되어 있습니다. 이 가이드라인은 AI 에이전트가 Laravel다운 코드를 작성하고, 프레임워크 관례를 따르며, 흔한 실수를 피하는 방법을 알려 줍니다. 가이드라인은 조합 가능하고 버전을 인식하므로, 에이전트는 사용자의 정확한 패키지 버전에 맞는 지침을 받습니다.

가이드라인은 Laravel 자체와 Laravel 생태계의 16개 이상의 패키지에 대해 제공되며, 여기에는 다음이 포함됩니다.

<div class="content-list" markdown="1">

- Livewire (2.x, 3.x, 4.x)
- Inertia.js (React, Svelte, Vue 변형)
- Tailwind CSS (3.x, 4.x)
- Filament (3.x, 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 그 외 다수

</div>

`boost:install`을 실행하면 Boost는 애플리케이션이 사용하는 패키지를 자동으로 감지하고, 관련 가이드라인을 프로젝트의 AI 컨텍스트 파일에 구성합니다.

<a name="agent-skills"></a>
### Agent Skills

[Agent Skills](https://agentskills.io/home)는 에이전트가 특정 도메인에서 작업할 때 필요에 따라 활성화할 수 있는 가볍고 목적이 뚜렷한 지식 모듈입니다. 처음부터 로드되는 가이드라인과 달리, skills는 관련이 있을 때만 자세한 패턴과 모범 사례를 로드할 수 있게 하여 컨텍스트가 불필요하게 커지는 것을 줄이고 AI 생성 코드의 관련성을 높입니다.

Skills는 Livewire, Inertia, Tailwind CSS, Pest 등 인기 있는 Laravel 패키지에 대해 제공됩니다. `boost:install`을 실행하고 기능으로 skills를 선택하면, `composer.json`에서 감지된 패키지를 기반으로 skills가 자동 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색

Boost에는 AI 에이전트가 Laravel 생태계 문서 17,000개 이상에 접근할 수 있게 해 주는 강력한 문서 API가 포함되어 있습니다. 일반적인 웹 검색과 달리, 이 문서는 사용자의 정확한 패키지 버전에 맞게 색인화되고, 벡터화되며, 필터링됩니다.

에이전트가 어떤 기능이 어떻게 동작하는지 이해해야 할 때 Boost의 문서 API를 검색하여 정확하고 버전에 맞는 정보를 받을 수 있습니다. 이를 통해 AI 에이전트가 오래된 프레임워크 버전의 더 이상 권장되지 않는 메서드나 문법을 제안하는 흔한 문제를 없앨 수 있습니다.

<a name="agent-integration"></a>
### 에이전트 통합

Boost는 Model Context Protocol을 지원하는 인기 IDE 및 AI 도구와 통합됩니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, Junie에 대한 자세한 설정 지침은 Boost 문서의 [에이전트 설정](/docs/13.x/boost#set-up-your-agents) 섹션을 참고하세요.
