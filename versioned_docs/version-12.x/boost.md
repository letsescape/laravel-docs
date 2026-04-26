# Laravel Boost (Laravel Boost)

- [소개](#introduction)
- [설치](#installation)
    - [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated)
    - [에이전트 설정](#set-up-your-agents)
- [MCP 서버](#mcp-server)
    - [사용 가능한 MCP 도구](#available-mcp-tools)
    - [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 가이드라인](#ai-guidelines)
    - [사용 가능한 AI 가이드라인](#available-ai-guidelines)
    - [사용자 정의 AI 가이드라인 추가](#adding-custom-ai-guidelines)
    - [Boost AI 가이드라인 재정의](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [사용자 정의 스킬](#custom-skills)
    - [스킬 재정의](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인과 스킬 비교](#guidelines-vs-skills)
- [문서 API](#documentation-api)
- [Boost 확장](#extending-boost)
    - [다른 IDE / AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Boost는 AI 에이전트가 Laravel 모범 사례를 따르는 고품질 Laravel 애플리케이션을 작성할 수 있도록 필수 가이드라인과 에이전트 스킬을 제공하여 AI 지원 개발 속도를 높여줍니다.

Boost는 강력한 Laravel 생태계 문서 API도 제공합니다. 이 API는 내장 MCP 도구와 17,000개가 넘는 Laravel 전용 정보를 담은 방대한 지식 베이스를 결합하며, 임베딩을 활용한 시맨틱 검색 기능으로 정확하고 문맥을 고려한 결과를 제공합니다. Boost는 Claude Code와 Cursor 같은 AI 에이전트가 이 API를 사용하여 최신 Laravel 기능과 모범 사례를 학습하도록 안내합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Boost는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/boost --dev
```

다음으로 MCP 서버와 코딩 가이드라인을 설치합니다.

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 에이전트 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost 설치가 완료되면 Cursor, Claude Code 또는 원하는 AI 에이전트로 코딩을 시작할 준비가 된 것입니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 설정 파일은 애플리케이션의 `.gitignore`에 자유롭게 추가해도 됩니다. 이 파일들은 `boost:install`과 `boost:update`를 실행할 때 자동으로 다시 생성됩니다.

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
### Boost 리소스 최신 상태로 유지하기

설치한 Laravel 생태계 패키지의 최신 버전을 반영하도록 로컬 Boost 리소스(AI 가이드라인 및 스킬)를 주기적으로 업데이트하고 싶을 수 있습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

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

<a name="mcp-server"></a>
## MCP 서버 (MCP Server)

Laravel Boost는 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있는 도구를 노출하는 MCP(Model Context Protocol) 서버를 제공합니다. 이 도구들은 에이전트가 애플리케이션 구조를 검사하고, 데이터베이스에 질의하고, 코드를 실행하는 등 다양한 작업을 수행할 수 있게 합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                 | 참고                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| 애플리케이션 정보     | PHP 및 Laravel 버전, 데이터베이스 엔진, 생태계 패키지와 버전 목록, Eloquent 모델을 읽습니다 |
| 브라우저 로그         | 브라우저의 로그와 오류를 읽습니다                                                                       |
| 데이터베이스 연결 | 기본 연결을 포함하여 사용 가능한 데이터베이스 연결을 검사합니다                                    |
| 데이터베이스 쿼리       | 데이터베이스에 대해 쿼리를 실행합니다                                                                        |
| 데이터베이스 스키마      | 데이터베이스 스키마를 읽습니다                                                                                    |
| 절대 URL 가져오기     | 에이전트가 유효한 URL을 생성할 수 있도록 상대 경로 URI를 절대 경로로 변환합니다                                        |
| 마지막 오류           | 애플리케이션 로그 파일에서 마지막 오류를 읽습니다                                                        |
| 로그 항목 읽기     | 마지막 N개의 로그 항목을 읽습니다                                                                                 |
| 문서 검색          | 설치된 패키지를 기준으로 문서를 가져오기 위해 Laravel 호스팅 문서 API 서비스에 질의합니다    |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

때로는 선택한 에디터에 Laravel Boost MCP 서버를 수동으로 등록해야 할 수 있습니다. 다음 세부 정보를 사용하여 MCP 서버를 등록해야 합니다.

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
## AI 가이드라인 (AI Guidelines)

AI 가이드라인은 AI 에이전트에게 Laravel 생태계 패키지에 대한 필수 문맥을 제공하기 위해 처음부터 로드되는 조합 가능한 지침 파일입니다. 이 가이드라인에는 에이전트가 일관성 있고 고품질인 코드를 생성하도록 돕는 핵심 규칙, 모범 사례, 프레임워크별 패턴이 포함되어 있습니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인

Laravel Boost는 다음 패키지와 프레임워크를 위한 AI 가이드라인을 포함합니다. `core` 가이드라인은 모든 버전에 적용할 수 있는 해당 패키지에 대한 일반적이고 범용적인 조언을 AI에 제공합니다.

| 패키지           | 지원 버전     |
| ----------------- | ---------------------- |
| Core & Boost      | core                   |
| Laravel Framework | core, 10.x, 11.x, 12.x |
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

> **참고:** AI 가이드라인을 최신 상태로 유지하려면 [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 사용자 정의 AI 가이드라인 추가

Laravel Boost에 직접 만든 사용자 정의 AI 가이드라인을 추가하려면 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가하세요. 이 파일들은 `boost:install`을 실행할 때 Laravel Boost의 가이드라인에 자동으로 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 재정의

파일 경로가 일치하는 사용자 정의 가이드라인을 만들어 Boost의 내장 AI 가이드라인을 재정의할 수 있습니다. 기존 Boost 가이드라인 경로와 일치하는 사용자 정의 가이드라인을 만들면, Boost는 내장 버전 대신 사용자 정의 버전을 사용합니다.

예를 들어 Boost의 "Inertia React v2 Form Guidance" 가이드라인을 재정의하려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 만드세요. `boost:install`을 실행하면 Boost는 기본 가이드라인 대신 사용자 정의 가이드라인을 포함합니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 가이드라인

서드파티 패키지를 관리하고 있으며 Boost가 해당 패키지의 AI 가이드라인을 포함하도록 하고 싶다면, 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 자동으로 가이드라인을 로드합니다.

AI 가이드라인은 패키지가 하는 일을 짧게 설명하고, 필요한 파일 구조나 규칙을 정리하며, 주요 기능을 만들거나 사용하는 방법을 설명해야 합니다(예시 명령어나 코드 조각 포함). AI가 사용자를 위해 올바른 코드를 생성할 수 있도록 간결하고 실행 가능하며 모범 사례에 집중하세요. 예시는 다음과 같습니다.

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

[에이전트 스킬](https://agentskills.io/home)은 에이전트가 특정 도메인에서 작업할 때 필요에 따라 활성화할 수 있는 가볍고 목적이 분명한 지식 모듈입니다. 처음부터 로드되는 가이드라인과 달리, 스킬은 관련이 있을 때만 자세한 패턴과 모범 사례를 로드할 수 있어 문맥 비대화를 줄이고 AI가 생성하는 코드의 관련성을 높입니다.

`boost:install`을 실행하고 기능으로 스킬을 선택하면, `composer.json`에서 감지된 패키지를 기준으로 스킬이 자동 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 포함되어 있다면 `livewire-development` 스킬이 자동으로 설치됩니다.

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

> **참고:** 스킬을 최신 상태로 유지하려면 [Boost 리소스 최신 상태로 유지하기](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="custom-skills"></a>
### 사용자 정의 스킬

직접 만든 사용자 정의 스킬을 생성하려면 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가하세요. `boost:update`를 실행하면 사용자 정의 스킬이 Boost의 내장 스킬과 함께 설치됩니다.

예를 들어 애플리케이션의 도메인 로직을 위한 사용자 정의 스킬을 만들려면 다음과 같이 작성합니다.

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 재정의

이름이 일치하는 사용자 정의 스킬을 만들어 Boost의 내장 스킬을 재정의할 수 있습니다. 기존 Boost 스킬 이름과 일치하는 사용자 정의 스킬을 만들면, Boost는 내장 버전 대신 사용자 정의 버전을 사용합니다.

예를 들어 Boost의 `livewire-development` 스킬을 재정의하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 만드세요. `boost:update`를 실행하면 Boost는 기본 스킬 대신 사용자 정의 스킬을 포함합니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

서드파티 패키지를 관리하고 있으며 Boost가 해당 패키지의 스킬을 포함하도록 하고 싶다면, 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 사용자 선호에 따라 스킬을 자동으로 설치합니다.

Boost 스킬은 [Agent Skills 형식](https://agentskills.io/what-are-skills)을 지원하며, YAML frontmatter와 Markdown 지침이 포함된 `SKILL.md` 파일을 담은 폴더 구조로 작성해야 합니다. `SKILL.md` 파일에는 필수 frontmatter(`name`과 `description`)가 포함되어야 하며, 선택적으로 스크립트, 템플릿, 참고 자료를 포함할 수 있습니다.

스킬은 필요한 파일 구조나 규칙을 정리하고, 주요 기능을 만들거나 사용하는 방법을 설명해야 합니다(예시 명령어나 코드 조각 포함). AI가 사용자를 위해 올바른 코드를 생성할 수 있도록 간결하고 실행 가능하며 모범 사례에 집중하세요.

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
## 가이드라인과 스킬 비교 (Guidelines vs. Skills)

Laravel Boost는 AI 에이전트에 애플리케이션에 대한 문맥을 제공하는 두 가지 구분된 방법인 **가이드라인**과 **스킬**을 제공합니다.

**가이드라인**은 AI 에이전트가 시작될 때 처음부터 로드되며, 코드베이스 전반에 폭넓게 적용되는 Laravel 규칙과 모범 사례에 대한 필수 문맥을 제공합니다.

**스킬**은 특정 작업을 수행할 때 필요에 따라 활성화되며, 특정 도메인(예: Livewire 컴포넌트 또는 Pest 테스트)에 대한 자세한 패턴을 포함합니다. 관련이 있을 때만 스킬을 로드하면 문맥 비대화를 줄이고 코드 품질을 높일 수 있습니다.

| 항목      | 가이드라인                        | 스킬                           |
| ----------- | --------------------------------- | -------------------------------- |
| **로드 방식**  | 처음부터 로드되며 항상 존재           | 필요할 때, 관련이 있을 때 로드         |
| **범위**   | 넓고 기초적               | 집중되어 있으며 작업별로 특화           |
| **목적** | 핵심 규칙 및 모범 사례 | 자세한 구현 패턴 |

<a name="documentation-api"></a>
## 문서 API (Documentation API)

Laravel Boost에는 17,000개가 넘는 Laravel 전용 정보를 담은 방대한 지식 베이스에 AI 에이전트가 접근할 수 있게 해주는 문서 API가 포함되어 있습니다. 이 API는 임베딩 기반 시맨틱 검색을 사용하여 정확하고 문맥을 고려한 결과를 제공합니다.

`Search Docs` MCP 도구를 사용하면 에이전트가 설치된 패키지를 기준으로 문서를 가져오기 위해 Laravel 호스팅 문서 API 서비스에 질의할 수 있습니다. Boost의 AI 가이드라인과 스킬은 코딩 에이전트가 이 API를 사용하도록 자동으로 안내합니다.

| 패키지           | 지원 버전 |
| ----------------- | ------------------ |
| Laravel Framework | 10.x, 11.x, 12.x   |
| Filament          | 2.x, 3.x, 4.x, 5.x |
| Flux UI           | 2.x Free, 2.x Pro  |
| Inertia           | 1.x, 2.x           |
| Livewire          | 1.x, 2.x, 3.x, 4.x |
| Nova              | 4.x, 5.x           |
| Pest              | 3.x, 4.x           |
| Tailwind CSS      | 3.x, 4.x           |

<a name="extending-boost"></a>
## Boost 확장 (Extending Boost)

Boost는 여러 인기 IDE와 AI 에이전트에서 기본적으로 작동합니다. 사용하는 코딩 도구가 아직 지원되지 않는다면 직접 에이전트를 만들고 Boost와 통합할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE / AI 에이전트 지원 추가

새 IDE 또는 AI 에이전트 지원을 추가하려면 `Laravel\Boost\Install\Agents\Agent`를 확장하는 클래스를 만들고, 필요한 기능에 따라 다음 계약 중 하나 이상을 구현하세요.

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 가이드라인 지원을 추가합니다.
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

애플리케이션의 `App\Providers\AppServiceProvider`에 있는 `boot` 메서드에서 사용자 정의 에이전트를 등록하세요.

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면 `php artisan boost:install`을 실행할 때 에이전트를 선택할 수 있습니다.
