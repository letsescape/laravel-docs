# Laravel Boost (Laravel Boost)

- [소개](#introduction)
- [설치](#installation)
    - [에이전트 설정](#set-up-your-agents)
    - [Boost 리소스를 최신 상태로 유지하기](#keeping-boost-resources-updated)
- [MCP 서버](#mcp-server)
    - [사용 가능한 MCP 도구](#available-mcp-tools)
    - [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 지침](#ai-guidelines)
    - [사용 가능한 AI 지침](#available-ai-guidelines)
    - [커스텀 AI 지침 추가](#adding-custom-ai-guidelines)
    - [Boost AI 지침 재정의](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 지침](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [커스텀 스킬](#custom-skills)
    - [스킬 재정의](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [지침과 스킬](#guidelines-vs-skills)
- [문서 API](#documentation-api)
- [Boost 확장](#extending-boost)
    - [다른 IDE / AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Boost는 AI 에이전트가 Laravel 모범 사례를 따르는 고품질 Laravel 애플리케이션을 작성하도록 돕는 핵심 지침과 에이전트 스킬을 제공하여 AI 지원 개발 속도를 높입니다.

또한 Boost는 내장 MCP 도구와 17,000개가 넘는 Laravel 전용 정보가 담긴 방대한 지식 베이스를 결합한 강력한 Laravel 생태계 문서 API를 제공합니다. 이 지식 베이스는 임베딩을 사용하는 의미 기반 검색 기능으로 강화되어, 정확하고 문맥을 고려한 결과를 제공합니다. Boost는 Claude Code와 Cursor 같은 AI 에이전트가 이 API를 사용하여 최신 Laravel 기능과 모범 사례를 학습하도록 안내합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Boost는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/boost --dev
```

그다음 MCP 서버와 코딩 지침을 설치합니다.

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 에이전트 지침 파일과 스킬 파일을 생성합니다.

Laravel Boost가 설치되면 Cursor, Claude Code 또는 원하는 AI 에이전트로 코딩을 시작할 준비가 됩니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 지침 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), `boost.json` 설정 파일은 애플리케이션의 `.gitignore`에 추가해도 됩니다. 이러한 파일은 `boost:install`과 `boost:update`를 실행할 때 자동으로 다시 생성되기 때문입니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정

```text tab=Cursor
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "/open MCP Settings"
3. Turn the toggle on for `laravel-boost`
```

```text tab=Claude Code
Claude Code support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

```text tab=Codex
Codex support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

```text tab=Gemini CLI
Gemini CLI support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

```text tab=GitHub Copilot (VS Code)
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "MCP: List Servers"
3. Arrow to `laravel-boost` and press `enter`
4. Choose "Start server"
```

```text tab=Junie
1. Press `shift` twice to open the command palette
2. Search "MCP Settings" and press `enter`
3. Check the box next to `laravel-boost`
4. Click "Apply" at the bottom right
```

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스를 최신 상태로 유지하기

설치된 Laravel 생태계 패키지의 최신 버전을 반영하도록 로컬 Boost 리소스(AI 지침과 스킬)를 주기적으로 업데이트하고 싶을 수 있습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

Composer의 "post-update-cmd" 스크립트에 추가하여 이 과정을 자동화할 수도 있습니다.

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```

기본적으로 `boost:update` 명령어는 애플리케이션 안에 이미 게시된 기존 Boost 리소스만 업데이트합니다. Boost가 애플리케이션에서 새로 설치된 패키지를 검색하고, 해당 패키지의 지침과 스킬 게시를 제안하도록 하려면 `--discover` 옵션을 사용할 수 있습니다.

```shell
php artisan boost:update --discover
```

<a name="mcp-server"></a>
## MCP 서버 (MCP Server)

Laravel Boost는 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있는 도구를 노출하는 MCP(Model Context Protocol) 서버를 제공합니다. 이 도구를 통해 에이전트는 애플리케이션 구조를 검사하고, 데이터베이스를 조회하고, 코드를 실행하는 등 여러 작업을 수행할 수 있습니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                 | 참고                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Application Info     | PHP 및 Laravel 버전, 데이터베이스 엔진, 버전이 포함된 생태계 패키지 목록, Eloquent 모델을 읽습니다 |
| Browser Logs         | 브라우저의 로그와 오류를 읽습니다                                                                       |
| Database Connections | 기본 연결을 포함하여 사용 가능한 데이터베이스 연결을 검사합니다                                    |
| Database Query       | 데이터베이스에 대해 쿼리를 실행합니다                                                                        |
| Database Schema      | 데이터베이스 스키마를 읽습니다                                                                                    |
| Get Absolute URL     | 에이전트가 유효한 URL을 생성하도록 상대 경로 URI를 절대 경로로 변환합니다                                        |
| Last Error           | 애플리케이션 로그 파일에서 마지막 오류를 읽습니다                                                        |
| Read Log Entries     | 마지막 N개의 로그 항목을 읽습니다                                                                                 |
| Search Docs          | 설치된 패키지를 기준으로 문서를 가져오기 위해 Laravel 호스팅 문서 API 서비스를 조회합니다    |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

때로는 원하는 에디터에 Laravel Boost MCP 서버를 수동으로 등록해야 할 수 있습니다. 다음 세부 정보를 사용하여 MCP 서버를 등록해야 합니다.

<table>
<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>
<tr><td><strong>인수</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

JSON 예시:

```json
{
    "mcpServers": {
        "laravel-boost": {
            "command": "php",
            "args": ["artisan", "boost:mcp"]
        }
    }
}
```

<a name="ai-guidelines"></a>
## AI 지침 (AI Guidelines)

AI 지침은 AI 에이전트에 Laravel 생태계 패키지에 대한 핵심 문맥을 미리 제공하기 위해 로드되는 조합 가능한 지시 파일입니다. 이 지침에는 에이전트가 일관되고 고품질의 코드를 생성하는 데 도움이 되는 핵심 규칙, 모범 사례, 프레임워크별 패턴이 포함되어 있습니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 지침

Laravel Boost에는 다음 패키지와 프레임워크를 위한 AI 지침이 포함되어 있습니다. `core` 지침은 해당 패키지의 모든 버전에 적용할 수 있는 일반적이고 범용적인 조언을 AI에 제공합니다.

| 패키지           | 지원 버전     |
| ----------------- | ---------------------- |
| Core & Boost      | core                   |
| Laravel Framework | core, 10.x, 11.x, 12.x, 13.x |
| Livewire          | core, 2.x, 3.x, 4.x    |
| Flux UI           | core, free, pro        |
| Folio             | core                   |
| Herd              | core                   |
| Inertia Laravel   | core, 1.x, 2.x, 3.x    |
| Inertia React     | core, 1.x, 2.x, 3.x    |
| Inertia Vue       | core, 1.x, 2.x, 3.x    |
| Inertia Svelte    | core, 1.x, 2.x, 3.x    |
| MCP               | core                   |
| Pennant           | core                   |
| Pest              | core, 3.x, 4.x         |
| PHPUnit           | core                   |
| Pint              | core                   |
| Sail              | core                   |
| Tailwind CSS      | core, 3.x, 4.x         |
| Livewire Volt     | core                   |
| Wayfinder         | core                   |
| Enforce Tests     | conditional            |

> **참고:** AI 지침을 최신 상태로 유지하려면 [Boost 리소스를 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 커스텀 AI 지침 추가

Laravel Boost에 직접 만든 커스텀 AI 지침을 추가하려면 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가합니다. 이 파일들은 `boost:install`을 실행할 때 Laravel Boost의 지침에 자동으로 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 지침 재정의

일치하는 파일 경로를 가진 커스텀 지침을 만들어 Boost의 내장 AI 지침을 재정의할 수 있습니다. 기존 Boost 지침 경로와 일치하는 커스텀 지침을 만들면 Boost는 내장 지침 대신 커스텀 버전을 사용합니다.

예를 들어 Boost의 "Inertia React v2 Form Guidance" 지침을 재정의하려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 만듭니다. `boost:install`을 실행하면 Boost는 기본 지침 대신 커스텀 지침을 포함합니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 지침

서드파티 패키지를 관리하고 있고 Boost가 해당 패키지의 AI 지침을 포함하도록 하고 싶다면, 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 지침을 자동으로 로드합니다.

AI 지침에는 패키지가 무엇을 하는지에 대한 짧은 개요, 필요한 파일 구조나 규칙, 주요 기능을 만들거나 사용하는 방법(예시 명령어 또는 코드 조각 포함)을 담아야 합니다. AI가 사용자에게 올바른 코드를 생성할 수 있도록 간결하고 실행 가능하며 모범 사례에 집중해서 작성하세요. 예시는 다음과 같습니다.

```php
## Package Name

This package provides [brief description of functionality].

### Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```

<a name="agent-skills"></a>
## 에이전트 스킬 (Agent Skills)

[Agent Skills](https://agentskills.io/home)는 에이전트가 특정 도메인 작업을 할 때 필요에 따라 활성화할 수 있는 가볍고 목적이 분명한 지식 모듈입니다. 미리 로드되는 지침과 달리, 스킬은 관련성이 있을 때만 상세한 패턴과 모범 사례를 로드할 수 있게 해 줍니다. 이를 통해 문맥이 불필요하게 커지는 것을 줄이고 AI가 생성하는 코드의 관련성을 높입니다.

`boost:install`을 실행하고 스킬을 기능으로 선택하면, `composer.json`에서 감지된 패키지를 기준으로 스킬이 자동 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 포함되어 있다면 `livewire-development` 스킬이 자동으로 설치됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬

| 스킬                      | 패키지        |
| -------------------------- | -------------- |
| fluxui-development         | Flux UI        |
| folio-routing              | Folio          |
| inertia-react-development  | Inertia React  |
| inertia-svelte-development | Inertia Svelte |
| inertia-vue-development    | Inertia Vue    |
| livewire-development       | Livewire       |
| mcp-development            | MCP            |
| pennant-development        | Pennant        |
| pest-testing               | Pest           |
| tailwindcss-development    | Tailwind CSS   |
| volt-development           | Volt           |
| wayfinder-development      | Wayfinder      |

> **참고:** 스킬을 최신 상태로 유지하려면 [Boost 리소스를 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="custom-skills"></a>
### 커스텀 스킬

직접 커스텀 스킬을 만들려면 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가합니다. `boost:update`를 실행하면 커스텀 스킬이 Boost의 내장 스킬과 함께 설치됩니다.

예를 들어 애플리케이션의 도메인 로직을 위한 커스텀 스킬을 만들려면 다음 파일을 생성합니다.

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 재정의

일치하는 이름을 가진 커스텀 스킬을 만들어 Boost의 내장 스킬을 재정의할 수 있습니다. 기존 Boost 스킬 이름과 일치하는 커스텀 스킬을 만들면 Boost는 내장 스킬 대신 커스텀 버전을 사용합니다.

예를 들어 Boost의 `livewire-development` 스킬을 재정의하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 만듭니다. `boost:update`를 실행하면 Boost는 기본 스킬 대신 커스텀 스킬을 포함합니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

서드파티 패키지를 관리하고 있고 Boost가 해당 패키지의 스킬을 포함하도록 하고 싶다면, 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 사용자 선택에 따라 스킬을 자동으로 설치합니다.

Boost 스킬은 [Agent Skills 형식](https://agentskills.io/what-are-skills)을 지원하며, YAML frontmatter와 Markdown 지침이 포함된 `SKILL.md` 파일을 담은 폴더 구조여야 합니다. `SKILL.md` 파일에는 필수 frontmatter(`name`과 `description`)가 포함되어야 하며, 선택적으로 스크립트, 템플릿, 참고 자료를 포함할 수 있습니다.

스킬에는 필요한 파일 구조나 규칙을 설명하고, 주요 기능을 만들거나 사용하는 방법(예시 명령어 또는 코드 조각 포함)을 담아야 합니다. AI가 사용자에게 올바른 코드를 생성할 수 있도록 간결하고 실행 가능하며 모범 사례에 집중해서 작성하세요.

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## When to use this skill
Use this skill when working with PackageName features...

## Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

$result = PackageName::featureTwo($param1, $param2);
```

<a name="guidelines-vs-skills"></a>
## 지침과 스킬 (Guidelines vs. Skills)

Laravel Boost는 AI 에이전트에 애플리케이션에 대한 문맥을 제공하는 두 가지 서로 다른 방법인 **지침**과 **스킬**을 제공합니다.

**지침**은 AI 에이전트가 시작될 때 미리 로드되어, 코드베이스 전반에 넓게 적용되는 Laravel 규칙과 모범 사례에 대한 핵심 문맥을 제공합니다.

**스킬**은 특정 작업을 수행할 때 필요에 따라 활성화되며, Livewire 컴포넌트나 Pest 테스트 같은 특정 도메인에 대한 상세한 패턴을 포함합니다. 관련성이 있을 때만 스킬을 로드하면 문맥이 불필요하게 커지는 것을 줄이고 코드 품질을 높일 수 있습니다.

| 측면      | 지침                        | 스킬                           |
| ----------- | --------------------------------- | -------------------------------- |
| **로드 방식**  | 미리 로드되며 항상 존재합니다           | 필요할 때 관련성이 있으면 로드됩니다         |
| **범위**   | 넓고 기초적입니다               | 집중되어 있으며 작업별로 특화되어 있습니다           |
| **목적** | 핵심 규칙과 모범 사례 | 상세한 구현 패턴 |

<a name="documentation-api"></a>
## 문서 API (Documentation API)

Laravel Boost에는 AI 에이전트가 17,000개가 넘는 Laravel 전용 정보가 담긴 방대한 지식 베이스에 접근할 수 있게 해 주는 Documentation API가 포함되어 있습니다. 이 API는 임베딩을 사용한 의미 기반 검색으로 정확하고 문맥을 고려한 결과를 제공합니다.

`Search Docs` MCP 도구를 사용하면 에이전트가 설치된 패키지를 기준으로 문서를 가져오기 위해 Laravel 호스팅 문서 API 서비스를 조회할 수 있습니다. Boost의 AI 지침과 스킬은 코딩 에이전트가 이 API를 사용하도록 자동으로 안내합니다.

| 패키지           | 지원 버전 |
| ----------------- | ------------------ |
| Laravel Framework | 10.x, 11.x, 12.x, 13.x |
| Filament          | 2.x, 3.x, 4.x, 5.x |
| Flux UI           | 2.x Free, 2.x Pro  |
| Inertia           | 1.x, 2.x           |
| Livewire          | 1.x, 2.x, 3.x, 4.x |
| Nova              | 4.x, 5.x           |
| Pest              | 3.x, 4.x           |
| Tailwind CSS      | 3.x, 4.x           |

<a name="extending-boost"></a>
## Boost 확장 (Extending Boost)

Boost는 여러 인기 IDE와 AI 에이전트를 기본적으로 지원합니다. 아직 사용하는 코딩 도구가 지원되지 않는다면, 직접 에이전트를 만들고 Boost와 통합할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE / AI 에이전트 지원 추가

새 IDE나 AI 에이전트 지원을 추가하려면 `Laravel\Boost\Install\Agents\Agent`를 확장하는 클래스를 만들고, 필요한 기능에 따라 다음 계약 중 하나 이상을 구현합니다.

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 지침 지원을 추가합니다.
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원을 추가합니다.
- `Laravel\Boost\Contracts\SupportsSkills` - Agent Skills 지원을 추가합니다.

<a name="writing-the-agent"></a>
#### 에이전트 작성

```php
<?php

declare(strict_types=1);

namespace App;

use Laravel\Boost\Contracts\SupportsGuidelines;
use Laravel\Boost\Contracts\SupportsMcp;
use Laravel\Boost\Contracts\SupportsSkills;
use Laravel\Boost\Install\Agents\Agent;

class CustomAgent extends Agent implements SupportsGuidelines, SupportsMcp, SupportsSkills
{
    // Your implementation...
}
```

구현 예시는 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)를 참고하세요.

<a name="registering-the-agent"></a>
#### 에이전트 등록

애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 에이전트를 등록합니다.

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면 `php artisan boost:install`을 실행할 때 해당 에이전트를 선택할 수 있습니다.
