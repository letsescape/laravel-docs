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
    - [사용자 정의 AI 가이드라인 추가](#adding-custom-ai-guidelines)
    - [Boost AI 가이드라인 오버라이드](#overriding-boost-ai-guidelines)
    - [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- [에이전트 스킬](#agent-skills)
    - [사용 가능한 스킬](#available-skills)
    - [사용자 정의 스킬](#custom-skills)
    - [스킬 오버라이드](#overriding-skills)
    - [서드파티 패키지 스킬](#third-party-package-skills)
- [가이드라인 vs. 스킬](#guidelines-vs-skills)
- [문서화 API](#documentation-api)
- [Boost 확장](#extending-boost)
    - [기타 IDE/AI 에이전트 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개

Laravel Boost는 AI 에이전트가 Laravel 베스트 프랙티스에 따라 고품질의 Laravel 애플리케이션을 작성할 수 있도록 필수 가이드라인과 에이전트 스킬을 제공하여 AI 기반 개발을 가속화합니다.

Boost는 또한 내장된 MCP 도구와 17,000개 이상의 Laravel 관련 정보가 포함된 방대한 지식 베이스가 결합된 강력한 Laravel 에코시스템 문서화 API를 제공합니다. 이 API는 임베딩 기반의 시맨틱 검색 기능을 활용하여 정밀하고 상황에 맞는 결과를 제공합니다. Boost는 Claude Code 및 Cursor와 같은 AI 에이전트가 최신 Laravel 기능과 베스트 프랙티스를 학습할 수 있도록 이 API 활용을 안내합니다.

<a name="installation"></a>
## 설치

Laravel Boost는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/boost --dev
```

그다음 MCP 서버와 코딩 가이드라인을 설치하세요.

```shell
php artisan boost:install
```

`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트용으로 적절한 에이전트 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost 설치가 완료되면, Cursor, Claude Code, 또는 원하는 AI 에이전트와 함께 코딩을 바로 시작할 수 있습니다.

> [!NOTE]
> 생성된 MCP 구성 파일(`.mcp.json`), 가이드라인 파일들(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), 그리고 `boost.json` 구성 파일은 `.gitignore`에 자유롭게 추가하셔도 됩니다. 이러한 파일들은 `boost:install` 및 `boost:update` 실행 시 자동으로 다시 생성됩니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정

```text tab=Cursor
1. 커맨드 팔레트(`Cmd+Shift+P` 또는 `Ctrl+Shift+P`)를 엽니다.
2. "/open MCP Settings"를 입력 후 엔터를 누릅니다.
3. `laravel-boost` 토글을 켭니다.
```

```text tab=Claude Code
Claude Code 지원은 대개 자동으로 활성화됩니다. 만약 자동 지원이 되지 않는 경우, 프로젝트 디렉터리에서 셸을 열고 아래 명령어를 실행하세요.

claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

```text tab=Codex
Codex 지원은 대개 자동으로 활성화됩니다. 만약 자동 지원이 되지 않는 경우, 프로젝트 디렉터리에서 셸을 열고 아래 명령어를 실행하세요.

codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

```text tab=Gemini CLI
Gemini CLI 지원은 대개 자동으로 활성화됩니다. 만약 자동 지원이 되지 않는 경우, 프로젝트 디렉터리에서 셸을 열고 아래 명령어를 실행하세요.

gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

```text tab=GitHub Copilot (VS Code)
1. 커맨드 팔레트(`Cmd+Shift+P`)를 엽니다.
2. "MCP: List Servers"를 입력 후 엔터를 누릅니다.
3. `laravel-boost`로 이동하여 엔터를 누릅니다.
4. "Start server"를 선택합니다.
```

```text tab=Junie
1. Shift 키를 두 번 눌러 커맨드 팔레트를 엽니다.
2. "MCP Settings"를 검색 후 엔터를 누릅니다.
3. `laravel-boost` 옆 체크박스를 선택합니다.
4. 우측 하단의 "Apply"를 클릭합니다.
```

<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 최신 상태 유지

설치된 Laravel 에코시스템 패키지의 최신 버전을 반영하기 위해, 로컬 Boost 리소스(AI 가이드라인 및 스킬)를 주기적으로 업데이트하는 것이 좋습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

이 과정을 자동화하고 싶다면 Composer의 "post-update-cmd" 스크립트에 아래와 같이 추가할 수 있습니다.

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
## MCP 서버

Laravel Boost는 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있도록 지원하는 MCP(Model Context Protocol) 서버를 제공합니다. 이 서버는 에이전트가 애플리케이션 구조를 탐색하고, 데이터베이스를 쿼리하며, 코드를 실행하는 등 다양한 기능을 제공합니다.

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

| 이름                        | 설명                                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------- |
| Application Info            | PHP & Laravel 버전, 데이터베이스 엔진, 에코시스템 패키지 목록(버전 포함), Eloquent 모델 정보 조회        |
| Browser Logs                | 브라우저로부터 로그 및 에러 읽기                                                                       |
| Database Connections        | 사용 가능한 데이터베이스 연결(기본 연결 포함) 탐색                                                     |
| Database Query              | 데이터베이스에 쿼리 실행                                                                               |
| Database Schema             | 데이터베이스 스키마 읽기                                                                               |
| Get Absolute URL            | 상대 URI 경로를 절대 경로로 변환하여 유효한 URL 생성                                                   |
| Get Config                  | "dot" 표기법으로 구성 파일 내 특정 값 조회                                                             |
| Last Error                  | 애플리케이션 로그 파일에서 최근 에러 읽기                                                              |
| List Artisan Commands       | 사용 가능한 Artisan 명령어 목록 조회                                                                   |
| List Available Config Keys  | 사용 가능한 구성 키 조회                                                                                |
| List Available Env Vars     | 사용 가능한 환경 변수 키 조회                                                                           |
| List Routes                 | 애플리케이션 라우트 정보 확인                                                                          |
| Read Log Entries            | 최근 N개의 로그 항목 읽기                                                                              |
| Search Docs                 | 설치된 패키지에 따른 문서를 Laravel 호스팅 문서 API 서비스에서 검색                                    |
| Tinker                      | 애플리케이션 컨텍스트 내 임의의 코드 실행                                                             |

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

에디터에서 Laravel Boost MCP 서버를 수동으로 등록해야 하는 경우, 다음 정보를 참고하여 등록하시기 바랍니다.

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
## AI 가이드라인

AI 가이드라인은 AI 에이전트가 Laravel 에코시스템 패키지에 대한 중대한 컨텍스트를 사전에 제공받을 수 있게 만들어진 조합 가능한 지침 파일입니다. 이 가이드라인들은 핵심 규칙, 베스트 프랙티스, 프레임워크별 패턴이 포함되어 있어 일관되고 품질 높은 코드를 생성할 수 있도록 도와줍니다.

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 가이드라인

Laravel Boost에는 아래 패키지 및 프레임워크용 AI 가이드라인이 포함되어 있습니다. `core` 가이드라인은 AI에게 패키지별 일반적이고 범용적인 권고 사항을 제공합니다.

| 패키지             | 지원 버전                  |
| ------------------- | ------------------------- |
| Core & Boost        | core                      |
| Laravel Framework   | core, 10.x, 11.x, 12.x    |
| Livewire            | core, 2.x, 3.x, 4.x       |
| Flux UI             | core, free, pro           |
| Folio               | core                      |
| Herd                | core                      |
| Inertia Laravel     | core, 1.x, 2.x            |
| Inertia React       | core, 1.x, 2.x            |
| Inertia Vue         | core, 1.x, 2.x            |
| Inertia Svelte      | core, 1.x, 2.x            |
| MCP                 | core                      |
| Pennant             | core                      |
| Pest                | core, 3.x, 4.x            |
| PHPUnit             | core                      |
| Pint                | core                      |
| Sail                | core                      |
| Tailwind CSS        | core, 3.x, 4.x            |
| Livewire Volt       | core                      |
| Wayfinder           | core                      |
| Enforce Tests       | conditional               |

> **참고:** AI 가이드라인을 최신 상태로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 절을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
### 사용자 정의 AI 가이드라인 추가

맞춤형 AI 가이드라인을 Boost에 추가하려면, `.ai/guidelines/*` 디렉터리에 `.blade.php` 혹은 `.md` 파일을 추가하세요. 이 파일들은 `boost:install` 실행 시 Boost의 기본 가이드라인과 함께 자동으로 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI 가이드라인 오버라이드

Boost 기본 가이드라인과 동일한 경로로 사용자 정의 가이드라인 파일을 생성하면 Boost의 내장 가이드라인을 오버라이드할 수 있습니다. 경로가 일치하는 커스텀 가이드라인이 있으면 Boost는 기본 대신 여러분의 버전을 사용합니다.

예를 들어, Boost의 “Inertia React v2 Form Guidance” 가이드라인을 오버라이드하려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 경로에 파일을 만들어두세요. `boost:install` 수행 시, Boost는 기본이 아닌 여러분의 가이드라인을 포함하게 됩니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 가이드라인

여러분이 서드파티 패키지의 유지자라면, Boost에서 해당 패키지용 AI 가이드라인을 포함하려면 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하세요. 여러분의 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 자동으로 이 가이드라인을 로드합니다.

AI 가이드라인에는 패키지의 기능을 간략하게 설명하고, 필요한 파일구조/규칙, 주요 기능의 생성 및 사용 방법(예시 코드/명령어 포함)을 안내하세요. 간결하고 실용적이어야 하며, 베스트 프랙티스에 초점을 맞추어 AI가 사용자를 위해 올바른 코드를 생성할 수 있게 해야 합니다. 아래는 예시입니다.

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
## 에이전트 스킬

[에이전트 스킬](https://agentskills.io/home)은 특정 도메인 작업에 특화된 경량 지식 모듈로, 필요할 때마다 AI 에이전트가 활성화합니다. 가이드라인이 기본적으로 모두 로드되는 것과 달리, 스킬은 관련 작업이 발생할 때만 상세 패턴과 베스트 프랙티스를 로드하여 컨텍스트 오염을 줄이고, AI가 더 관련성 높은 코드를 생성할 수 있도록 돕습니다.

`boost:install` 명령 및 스킬 기능 선택 시, `composer.json`에서 감지된 패키지 기반으로 자동으로 스킬이 설치됩니다. 예를 들어, 프로젝트에 `livewire/livewire`가 있다면 `livewire-development` 스킬이 함께 설치됩니다.

<a name="available-skills"></a>
### 사용 가능한 스킬

| 스킬                     | 패키지         |
| ------------------------ | -------------- |
| fluxui-development       | Flux UI        |
| folio-routing            | Folio          |
| inertia-react-development | Inertia React  |
| inertia-svelte-development| Inertia Svelte |
| inertia-vue-development  | Inertia Vue    |
| livewire-development     | Livewire       |
| mcp-development          | MCP            |
| pennant-development      | Pennant        |
| pest-testing             | Pest           |
| tailwindcss-development  | Tailwind CSS   |
| volt-development         | Volt           |
| wayfinder-development    | Wayfinder      |

> **참고:** 스킬을 최신으로 유지하려면 [Boost 리소스 최신 상태 유지](#keeping-boost-resources-updated) 절을 참조하세요.

<a name="custom-skills"></a>
### 사용자 정의 스킬

사용자 정의 스킬을 만들려면, `.ai/skills/{skill-name}/` 디렉터리 내에 `SKILL.md` 파일을 추가하세요. `boost:update` 실행 시, Boost 내장 스킬과 함께 여러분의 커스텀 스킬도 설치됩니다.

예를 들어, 도메인 로직용 스킬을 만들고 싶다면 다음과 같은 경로로 파일을 생성합니다.

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### 스킬 오버라이드

Boost 기본 스킬과 이름이 동일한 사용자 정의 스킬을 생성하면, 내장 스킬 대신 여러분의 커스텀 스킬이 사용됩니다.

예를 들어 Boost의 `livewire-development` 스킬을 오버라이드하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 만들면 됩니다. `boost:update` 실행 시, 커스텀 스킬이 우선적으로 반영됩니다.

<a name="third-party-package-skills"></a>
### 서드파티 패키지 스킬

여러분이 서드파티 패키지의 유지자라면, Boost에 해당 패키지용 스킬을 포함하려면 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하세요. 패키지 사용자가 `php artisan boost:install`을 실행할 때, 사용자 선택에 따라 여러분의 스킬이 자동 설치됩니다.

Boost 스킬은 [Agent Skills 포맷](https://agentskills.io/what-are-skills)을 지원하며, 폴더 내에 YAML 프론트매터 및 Markdown 설명이 포함된 `SKILL.md` 파일로 구성해야 합니다. 이 파일은 반드시 `name`과 `description` 프론트매터가 포함되어야 하며, 스크립트·템플릿·참고자료 등을 추가할 수 있습니다.

스킬에는 필요한 파일 구조나 규칙, 주요 기능의 생성 및 사용법(예제 코드, 명령어 등)을 안내하세요. 간결하고 실용적이어야 하며, 베스트 프랙티스 중심으로 AI가 사용자를 위한 올바른 코드를 생성할 수 있도록 해야 합니다.

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
## 가이드라인 vs. 스킬

Laravel Boost는 애플리케이션에 대한 AI 에이전트의 컨텍스트 부여를 위해 **가이드라인**과 **스킬**이라는 두 가지 방식을 제공합니다.

**가이드라인**은 AI 에이전트 시작 시 사전에 로드되어, Laravel 규약 및 베스트 프랙티스 등 넓은 범위에서 반드시 필요한 컨텍스트를 제공합니다.

**스킬**은 Livewire 컴포넌트 작성이나 Pest 테스트처럼 특정 작업을 수행할 때 온디맨드 방식으로 활성화되며, 해당 도메인에 대한 상세한 구현 패턴을 담고 있습니다. 스킬을 필요할 때만 로드함으로써, 컨텍스트 오버로드를 줄이고 코드 품질을 높일 수 있습니다.

| 구분        | 가이드라인                        | 스킬                               |
| ----------- | --------------------------------- | ----------------------------------- |
| **적용 시점** | 사전 전체 로드                     | 필요 시 개별 온디맨드 로드           |
| **범위**    | 광범위, 기초적                     | 집중적, 태스크 특화                  |
| **목적**    | 핵심 규약 및 베스트 프랙티스        | 상세 구현 패턴 및 실무 사례           |

<a name="documentation-api"></a>
## 문서화 API

Laravel Boost에는 17,000건 이상의 Laravel 관련 정보를 담은 방대한 지식 베이스에 접근할 수 있는 문서화 API가 포함되어 있습니다. 이 API는 임베딩(embeddings) 기반의 시맨틱 검색을 통해 정밀하고 상황에 맞는 결과를 제공합니다.

`Search Docs` MCP 도구를 활용하면, 에이전트가 설치된 패키지에 맞는 문서를 Laravel 호스팅 문서 API 서비스에서 실시간으로 검색할 수 있습니다. Boost의 AI 가이드라인과 스킬은 코딩 에이전트가 이 API를 활용하도록 자동 안내합니다.

| 패키지             | 지원 버전              |
| ------------------- | --------------------- |
| Laravel Framework   | 10.x, 11.x, 12.x      |
| Filament            | 2.x, 3.x, 4.x, 5.x    |
| Flux UI             | 2.x Free, 2.x Pro     |
| Inertia             | 1.x, 2.x              |
| Livewire            | 1.x, 2.x, 3.x, 4.x    |
| Nova                | 4.x, 5.x              |
| Pest                | 3.x, 4.x              |
| Tailwind CSS        | 3.x, 4.x              |

<a name="extending-boost"></a>
## Boost 확장

Boost는 주요 IDE와 AI 에이전트에서 바로 사용할 수 있도록 지원합니다. 만약 아직 지원되지 않는 코딩 도구를 사용한다면, 새로운 에이전트를 직접 구현하여 Boost와 연동할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
### 기타 IDE/AI 에이전트 지원 추가

새로운 IDE 또는 AI 에이전트를 지원하려면, `Laravel\Boost\Install\Agents\Agent`를 상속하는 클래스를 만들고, 필요한 경우 아래의 컨트랙트 중 하나 이상을 구현하세요.

- `Laravel\Boost\Contracts\SupportsGuidelines` — AI 가이드라인 지원 추가
- `Laravel\Boost\Contracts\SupportsMcp` — MCP 지원 추가
- `Laravel\Boost\Contracts\SupportsSkills` — 에이전트 스킬 지원 추가

<a name="writing-the-agent"></a>
#### 에이전트 작성 예시

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

여러분의 커스텀 에이전트를 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록하세요.

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

등록이 완료되면, `php artisan boost:install` 명령 실행 시 해당 에이전트를 선택할 수 있습니다.
