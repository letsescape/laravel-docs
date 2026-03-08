# Laravel Boost (Laravel Boost)

- [소개](#introduction)
- [설치](#installation)
    - [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated)
    - [에이전트 설정](#set-up-your-agents)
- [MCP 서버](#mcp-server)
    - [사용 가능한 MCP 도구](#available-mcp-tools)
    - [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 가이드라인](#ai-guidelines)
    - [사용 가능한 AI 가이드라인](#available-ai-guidelines)
    - [커스텀 AI 가이드라인 추가](#adding-custom-ai-guidelines)
    - [Boost AI 가이드라인 덮어쓰기](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [커스텀 스킬](#custom-skills)
    - [스킬 덮어쓰기](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인과 스킬의 차이](#guidelines-vs-skills)
- [문서화 API](#documentation-api)
- [Boost 확장](#extending-boost)
    - [다른 IDE / AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel Boost는 AI 에이전트가 Laravel 베스트 프랙티스를 준수하면서 고품질의 Laravel 애플리케이션을 작성할 수 있도록 핵심 가이드라인과 에이전트 스킬을 제공하여 AI 지원 개발을 가속화합니다.

Boost는 또한 내장된 MCP 도구와 함께 17,000개 이상의 Laravel 특화 정보가 담긴 방대한 지식 베이스를 결합한 강력한 Laravel 생태계 문서화 API를 제공합니다. 이 API는 임베딩(embeddings)을 이용한 시맨틱 검색 기능을 갖추고 있어, 정밀하고 상황에 맞는 검색 결과를 제공합니다. Boost는 Claude Code 및 Cursor 같은 AI 에이전트에게 이 API를 사용해 최신 Laravel 기능과 베스트 프랙티스에 대해 학습하도록 지시합니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel Boost는 Composer를 통해 설치할 수 있습니다:

```shell
composer require laravel/boost --dev
```

다음으로 MCP 서버와 코딩 가이드라인을 설치합니다:

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 에이전트 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost 설치가 완료되면, Cursor, Claude Code 또는 원하는 AI 에이전트로 코딩을 시작할 준비가 완료된 것입니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 설정 파일은 `.gitignore`에 추가해도 무방합니다. 이 파일들은 `boost:install` 및 `boost:update` 실행 시 자동으로 재생성되기 때문입니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정 (Set Up Your Agents)

```text tab=Cursor
1. 명령 팔레트(`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)를 엽니다
2. "/open MCP Settings"에서 `enter`를 누릅니다
3. `laravel-boost` 토글을 켭니다
```

```text tab=Claude Code
Claude Code 지원은 일반적으로 자동으로 활성화됩니다. 만약 활성화되어 있지 않다면, 프로젝트 디렉터리에서 쉘을 열고 다음 명령을 실행하세요:

claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

```text tab=Codex
Codex 지원도 자동으로 활성화됩니다. 만약 활성화되어 있지 않다면, 프로젝트 디렉터리에서 쉘을 열고 다음 명령을 실행하세요:

codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

```text tab=Gemini CLI
Gemini CLI 지원은 기본적으로 자동 활성화됩니다. 활성화되어 있지 않다면 프로젝트 디렉터리에서 쉘을 열고 다음 명령을 실행하세요:

gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

```text tab=GitHub Copilot (VS Code)
1. 명령 팔레트(`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)를 엽니다
2. "MCP: List Servers"에서 `enter`를 누릅니다
3. `laravel-boost`를 화살표 키로 선택 후 `enter`
4. "Start server"를 선택합니다
```

```text tab=Junie
1. Shift 키를 두 번 눌러 명령 팔레트를 엽니다
2. "MCP Settings"를 검색하고 `enter`
3. `laravel-boost` 옆의 체크박스를 활성화
4. 오른쪽 아래 "Apply" 클릭
```

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 최신 상태 유지 (Keeping Boost Resources Updated)

설치된 Laravel 생태계 패키지들의 최신 버전을 반영하기 위해, Boost의 로컬 리소스(AI 가이드라인 및 스킬)를 주기적으로 업데이트하는 것이 좋습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

이 작업을 자동화하려면 Composer의 "post-update-cmd" 스크립트에 다음을 추가할 수 있습니다:

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

Laravel Boost는 MCP(Model Context Protocol) 서버를 제공하여, AI 에이전트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있게 합니다. 이 도구들을 통해 에이전트는 애플리케이션 구조를 조회하고, 데이터베이스를 쿼리하며, 임의의 코드를 실행하는 등 다양한 작업이 가능합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구 (Available MCP Tools)

| 이름                        | 비고                                                                                                |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| Application Info           | PHP & Laravel 버전, 데이터베이스 엔진, 생태계 패키지 목록(버전 포함), Eloquent 모델 목록 조회        |
| Browser Logs               | 브라우저 로그 및 에러 읽기                                                                         |
| Database Connections       | 사용 가능한 데이터베이스 커넥션(기본 커넥션 포함) 조회                                             |
| Database Query             | 데이터베이스 쿼리 실행                                                                             |
| Database Schema            | 데이터베이스 스키마 읽기                                                                            |
| Get Absolute URL           | 상대 경로 URI를 절대 경로로 변환하여 에이전트가 올바른 URL 생성하도록 지원                          |
| Get Config                 | "도트(dotted)" 표기법을 사용해 설정 파일 값 가져오기                                                |
| Last Error                 | 애플리케이션 로그 파일에서 마지막 에러 읽기                                                         |
| List Artisan Commands      | 사용 가능한 Artisan 명령어 조회                                                                     |
| List Available Config Keys | 사용 가능한 설정 키 조회                                                                             |
| List Available Env Vars    | 사용 가능한 환경 변수 키 조회                                                                        |
| List Routes                | 애플리케이션 라우트 목록 조회                                                                        |
| Read Log Entries           | 마지막 N개 로그 항목 읽기                                                                           |
| Search Docs                | 설치된 패키지에 따라 Laravel 호스트 문서 API 서비스에 쿼리하여 문서 검색                            |
| Tinker                     | 애플리케이션 문맥 내에서 임의의 코드 실행                                                           |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록 (Manually Registering the MCP Server)

가끔은 원하는 에디터에 Laravel Boost MCP 서버를 직접 등록해야 할 수도 있습니다. 이 경우 다음과 같은 정보를 사용해 MCP 서버를 등록하세요:

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr>
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

AI 가이드라인은 Laravel 생태계 패키지에 대한 필수 컨텍스트를 제공하는 조합 가능한(in composable) 지침 파일입니다. 이러한 가이드라인은 핵심 관례, 베스트 프랙티스, 프레임워크별 패턴을 담고 있어, AI 에이전트가 일관되고 고품질의 코드를 생성하는 데 도움을 줍니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인 (Available AI Guidelines)

Laravel Boost는 다음과 같은 패키지 및 프레임워크에 대한 AI 가이드라인을 포함합니다. `core` 가이드라인은 해당 패키지에 적용 가능한 일반화된 조언을 제공합니다.

| 패키지             | 지원 버전                 |
| ----------------- | ------------------------ |
| Core & Boost      | core                     |
| Laravel Framework | core, 10.x, 11.x, 12.x   |
| Livewire          | core, 2.x, 3.x, 4.x      |
| Flux UI           | core, free, pro          |
| Folio             | core                     |
| Herd              | core                     |
| Inertia Laravel   | core, 1.x, 2.x           |
| Inertia React     | core, 1.x, 2.x           |
| Inertia Vue       | core, 1.x, 2.x           |
| Inertia Svelte    | core, 1.x, 2.x           |
| MCP               | core                     |
| Pennant           | core                     |
| Pest              | core, 3.x, 4.x           |
| PHPUnit           | core                     |
| Pint              | core                     |
| Sail              | core                     |
| Tailwind CSS      | core, 3.x, 4.x           |
| Livewire Volt     | core                     |
| Wayfinder         | core                     |
| Enforce Tests     | conditional              |

> **참고:** AI 가이드라인을 항상 최신 상태로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 항목을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 커스텀 AI 가이드라인 추가 (Adding Custom AI Guidelines)

직접 만든 AI 가이드라인을 Laravel Boost에 추가하려면, `.blade.php` 또는 `.md` 파일을 애플리케이션의 `.ai/guidelines/*` 디렉터리에 넣으세요. 이 파일들은 `boost:install` 실행 시 Boost의 가이드라인과 함께 자동으로 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 덮어쓰기 (Overriding Boost AI Guidelines)

Boost에서 제공하는 기본 AI 가이드라인을 덮어쓰려면, 동일한 파일 경로에 커스텀 가이드라인을 생성하세요. 기존 Boost 가이드라인 경로와 일치하는 커스텀 파일이 있으면, Boost는 기본 가이드라인 대신 해당 파일을 사용합니다.

예를 들어, Boost의 "Inertia React v2 Form Guidance" 가이드라인을 덮어쓰려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 생성하세요. `boost:install` 실행 시 커스텀 가이드라인이 기본 가이드라인 대신 사용됩니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 가이드라인 (Third-Party Package AI Guidelines)

여러분이 직접 개발한 서드파티 패키지에 대해 Boost가 AI 가이드라인을 포함하도록 하려면, 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하세요. 해당 패키지 사용자들이 `php artisan boost:install`을 실행하면 Boost에서 가이드라인을 자동으로 로드합니다.

AI 가이드라인에는 패키지의 간단한 사용 개요, 필요한 파일 구조나 관례, 주요 기능 사용법(예시 명령어나 코드 스니펫 등)을 포함해야 합니다. 간결하고 실용적이며, 베스트 프랙티스에 집중해 AI가 정확한 코드를 생성할 수 있게 작성하세요. 아래는 예시입니다:

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

[에이전트 스킬](https://agentskills.io/home)은 AI 에이전트가 특정 도메인 작업을 할 때 필요에 따라 활성화할 수 있는 가볍고 표적화된 지식 모듈입니다. 가이드라인과 달리 스킬은 필요할 때마다 로드하므로, 불필요한 정보를 줄이고 AI가 더 관련성 높은 코드를 생성할 수 있습니다.

`boost:install` 명령 실행 시, 프로젝트의 `composer.json`에 포함된 패키지에 따라 스킬이 자동으로 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 있다면 `livewire-development` 스킬이 자동 추가됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬 (Available Skills)

| 스킬                       | 패키지            |
| -------------------------- | ----------------- |
| fluxui-development         | Flux UI           |
| folio-routing              | Folio             |
| inertia-react-development  | Inertia React     |
| inertia-svelte-development | Inertia Svelte    |
| inertia-vue-development    | Inertia Vue       |
| livewire-development       | Livewire          |
| mcp-development            | MCP               |
| pennant-development        | Pennant           |
| pest-testing               | Pest              |
| tailwindcss-development    | Tailwind CSS      |
| volt-development           | Volt              |
| wayfinder-development      | Wayfinder         |

> **참고:** 스킬을 최신 상태로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 항목을 참고하세요.

<a name="custom-skills"></a>
### 커스텀 스킬 (Custom Skills)

커스텀 스킬을 만들려면, `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가하세요. `boost:update` 실행 시, 커스텀 스킬도 Boost의 기본 스킬과 함께 설치됩니다.

예를 들어, 애플리케이션의 도메인 로직에 대한 커스텀 스킬을 만들려면:

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 덮어쓰기 (Overriding Skills)

Boost 기본 스킬을 덮어쓰려면, 같은 이름의 커스텀 스킬을 생성하면 됩니다. 기존 Boost 스킬과 이름이 같으면, 커스텀 스킬이 기본 스킬을 대신하게 됩니다.

예를 들어 `livewire-development` 스킬을 덮어쓰려면, `.ai/skills/livewire-development/SKILL.md` 파일을 만들어주세요. `boost:update` 실행 시 해당 커스텀 스킬이 적용됩니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬 (Third-Party Package Skills)

서드파티 패키지의 스킬도 쉽게 추가할 수 있습니다. 패키지 내에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 포함시키세요. 패키지 사용자가 `php artisan boost:install`을 실행하면 사용자가 선택한 옵션에 따라 해당 스킬이 자동 설치됩니다.

Boost 스킬은 [Agent Skills 포맷](https://agentskills.io/what-are-skills)을 지원하며, 폴더 안에 YAML frontmatter와 Markdown 지침이 들어있는 `SKILL.md` 파일이 필요합니다. `name`과 `description` frontmatter는 필수이며, 스크립트, 템플릿, 참고 자료 등도 추가 가능합니다.

스킬에는 필요 파일 구조, 관례, 주요 기능 사용법(명령어나 코드 예시 등)을 간결하고 실행 가능한 방식으로 기술해, AI가 사용자에게 올바른 코드를 생성할 수 있게 해야 합니다. 아래는 예시입니다:

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
## 가이드라인과 스킬의 차이 (Guidelines vs. Skills)

Laravel Boost는 AI 에이전트에게 컨텍스트를 제공하는 두 가지 방식을 지원합니다: **가이드라인(guidelines)**과 **스킬(skills)**입니다.

**가이드라인**은 AI 에이전트가 시작될 때 미리 로드되어, 전체 코드베이스에 폭넓게 적용되는 Laravel 관례 및 베스트 프랙티스의 핵심 컨텍스트를 제공합니다.

**스킬**은 특정 작업이나 도메인 작업을 할 때 필요에 따라 활성화하며, 해당 영역(예: Livewire 컴포넌트, Pest 테스트 등)에 맞는 상세 패턴을 포함합니다. 필요한 시점에만 로드하므로 정보 과다(컨텍스트 블로트)를 줄이고 코드 품질을 높일 수 있습니다.

| 항목        | 가이드라인                          | 스킬                               |
| ----------- | --------------------------------- | ---------------------------------- |
| **로드 시점**   | 시작 시, 항상 불러옴                  | 필요할 때, 관련 작업 시만 불러옴         |
| **적용 범위**   | 폭넓고 기초적인 영역                  | 특정 작업이나 도메인에 집중            |
| **목적**       | 핵심 관례와 베스트 프랙티스            | 상세한 구현 패턴                     |

<a name="documentation-api"></a>
## 문서화 API (Documentation API)

Laravel Boost에는 17,000개 이상의 Laravel 특화 정보를 담은 방대한 지식 베이스에 AI 에이전트가 접근할 수 있는 문서화 API가 포함되어 있습니다. 이 API는 임베딩을 활용한 시맨틱 검색을 사용해, 정밀하고 상황 맞춤형 결과를 제공합니다.

`Search Docs` MCP 도구를 통해, 설치된 패키지 목록을 기반으로 Laravel 호스팅 문서 API 서비스로 쿼리하여 관련 문서를 검색할 수 있습니다. Boost의 AI 가이드라인과 스킬은 코딩 에이전트가 이 API를 자동으로 사용하도록 안내합니다.

| 패키지             | 지원 버전              |
| ----------------- | -------------------- |
| Laravel Framework | 10.x, 11.x, 12.x     |
| Filament          | 2.x, 3.x, 4.x, 5.x   |
| Flux UI           | 2.x Free, 2.x Pro    |
| Inertia           | 1.x, 2.x             |
| Livewire          | 1.x, 2.x, 3.x, 4.x   |
| Nova              | 4.x, 5.x             |
| Pest              | 3.x, 4.x             |
| Tailwind CSS      | 3.x, 4.x             |

<a name="extending-boost"></a>
## Boost 확장 (Extending Boost)

Boost는 여러 인기 IDE와 AI 에이전트에서 즉시 사용할 수 있습니다. 만약 사용하는 코딩 도구가 아직 지원되지 않는 경우, 직접 에이전트를 생성하여 Boost와 연동할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE / AI 에이전트 지원 추가 (Adding Support for Other IDEs / AI Agents)

새로운 IDE나 AI 에이전트를 지원하려면, `Laravel\Boost\Install\Agents\Agent`를 상속하는 클래스를 만들고, 필요에 따라 다음 컨트랙트 중 하나 이상을 구현하세요:

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 가이드라인 지원 추가
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원 추가
- `Laravel\Boost\Contracts\SupportsSkills` - 에이전트 스킬 지원 추가

<a name="writing-the-agent"></a>
#### 에이전트 작성 (Writing the Agent)

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

구현 예시는 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)에서 확인할 수 있습니다.

<a name="registering-the-agent"></a>
#### 에이전트 등록 (Registering the Agent)

애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 에이전트를 등록하세요:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면, `php artisan boost:install` 명령 실행 시 해당 에이전트를 선택할 수 있게 됩니다.
