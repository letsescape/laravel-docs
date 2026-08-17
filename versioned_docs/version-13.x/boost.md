<!-- # Laravel Boost -->
# Laravel Boost

- [Introduction](#introduction)
- [Installation](#installation)
    - [Set Up Your Agents](#set-up-your-agents)
    - [Keeping Boost Resources Updated](#keeping-boost-resources-updated)
- [MCP Server](#mcp-server)
    - [Available MCP Tools](#available-mcp-tools)
    - [Manually Registering the MCP Server](#manually-registering-the-mcp-server)
- [AI Guidelines](#ai-guidelines)
    - [Available AI Guidelines](#available-ai-guidelines)
    - [Adding Custom AI Guidelines](#adding-custom-ai-guidelines)
    - [Overriding Boost AI Guidelines](#overriding-boost-ai-guidelines)
    - [Third-Party Package AI Guidelines](#third-party-package-ai-guidelines)
- [Agent Skills](#agent-skills)
    - [Available Skills](#available-skills)
    - [Custom Skills](#custom-skills)
    - [Overriding Skills](#overriding-skills)
    - [Third-Party Package Skills](#third-party-package-skills)
- [Guidelines vs. Skills](#guidelines-vs-skills)
- [Project Rules](#project-rules)
    - [Recording Rules](#recording-rules)
    - [Inferring Your Application's Conventions](#inferring-your-applications-conventions)
    - [Disabling Project Rules](#disabling-project-rules)
- [Documentation API](#documentation-api)
- [Extending Boost](#extending-boost)
    - [Adding Support for Other IDEs / AI Agents](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel Boost accelerates AI-assisted development by providing the essential guidelines and agent skills that help AI agents write high-quality Laravel applications that adhere to Laravel best practices. -->
Laravel Boost는 AI 에이전트가 Laravel 모범 사례를 따르는 고품질 Laravel 애플리케이션을 작성하도록 돕는 핵심 지침과 에이전트 스킬을 제공하여 AI 지원 개발 속도를 높입니다.

<!-- Boost also provides a powerful Laravel ecosystem documentation API that combines a built-in MCP tool with an extensive knowledge base containing over 17,000 pieces of Laravel-specific information, all enhanced by semantic search capabilities using embeddings for precise, context-aware results. Boost instructs AI agents like Claude Code and Cursor to use this API to learn about the latest Laravel features and best practices. -->
또한 Boost는 내장 MCP 도구와 17,000개가 넘는 Laravel 전용 정보가 담긴 방대한 지식 베이스를 결합한 강력한 Laravel 생태계 문서 API를 제공합니다. 이 지식 베이스는 임베딩을 사용하는 의미 기반 검색 기능으로 강화되어, 정확하고 문맥을 고려한 결과를 제공합니다. Boost는 Claude Code와 Cursor 같은 AI 에이전트가 이 API를 사용하여 최신 Laravel 기능과 모범 사례를 학습하도록 안내합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Laravel Boost can be installed via Composer: -->
Laravel Boost는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/boost --dev
```

<!-- Next, install the MCP server and coding guidelines: -->
그다음 MCP 서버와 코딩 지침을 설치합니다.

```shell
php artisan boost:install
```

<!-- The `boost:install` command will generate the relevant agent guideline and skill files for the coding agents you selected during the installation process. -->
`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트에 맞는 에이전트 지침 파일과 스킬 파일을 생성합니다.

<!-- Once Laravel Boost has been installed, you're ready to start coding with Cursor, Claude Code, or your AI agent of choice. -->
Laravel Boost가 설치되면 Cursor, Claude Code 또는 원하는 AI 에이전트로 코딩을 시작할 준비가 됩니다.

> [!NOTE]
> 생성된 MCP 설정 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), `boost.json` 설정 파일은 애플리케이션의 `.gitignore`에 자유롭게 추가해도 됩니다. 이러한 파일은 `boost:install` 및 `boost:update`를 실행할 때 자동으로 다시 생성됩니다.

<a name="set-up-your-agents"></a>
<!-- ### Set Up Your Agents -->
### Set Up Your Agents

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
<!-- ### Keeping Boost Resources Updated -->
### Keeping Boost Resources Updated

<!-- You may want to periodically update your local Boost resources (AI guidelines and skills) to ensure they reflect the latest versions of the Laravel ecosystem packages you have installed. To do so, you can use the `boost:update` Artisan command. -->
설치된 Laravel 생태계 패키지의 최신 버전을 반영하도록 로컬 Boost 리소스(AI 지침과 스킬)를 주기적으로 업데이트하고 싶을 수 있습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```

<!-- You may also automate this process by adding it to your Composer "post-update-cmd" scripts: -->
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

<!-- By default, the `boost:update` command will only update the existing Boost resources already published within your application. If you would like Boost to scan your application for any newly installed packages and offer to publish their corresponding guidelines and skills, you may use the `--discover` option: -->
기본적으로 `boost:update` 명령어는 애플리케이션 안에 이미 게시된 기존 Boost 리소스만 업데이트합니다. Boost가 애플리케이션에서 새로 설치된 패키지를 검색하고, 해당 패키지의 지침과 스킬 게시를 제안하도록 하려면 `--discover` 옵션을 사용할 수 있습니다.

```shell
php artisan boost:update --discover
```

<a name="mcp-server"></a>
<!-- ## MCP Server -->
## MCP Server

<!-- Laravel Boost provides an MCP (Model Context Protocol) server that exposes tools for AI agents to interact with your Laravel application. These tools give agents the ability to inspect your application's structure, query the database, execute code, and more. -->
Laravel Boost는 AI 에이전트가 Laravel 애플리케이션과 상호작용할 수 있는 도구를 노출하는 MCP(Model Context Protocol) 서버를 제공합니다. 이 도구를 통해 에이전트는 애플리케이션 구조를 검사하고, 데이터베이스를 조회하고, 코드를 실행하는 등 여러 작업을 수행할 수 있습니다.

<a name="available-mcp-tools"></a>
<!-- ### Available MCP Tools -->
### Available MCP Tools

<div class="overflow-auto">

<!-- | Name | Notes | | -------------------- | ----------------------------------------------------------------------------------------------------------- | | Application Info | Read PHP & Laravel versions, database engine, list of ecosystem packages with versions, and Eloquent models | | Browser Logs | Read logs and errors from the browser | | Database Connections | Inspect available database connections, including the default connection | | Database Query | Execute a query against the database | | Database Schema | Read the database schema | | Get Absolute URL | Convert relative path URIs to absolute so agents generate valid URLs | | Last Error | Read the last error from the application's log files | | Read Log Entries | Read the last N log entries | | Record Rule | Record a durable [project rule](#project-rules) into `.ai/rules` so future agents inherit it | | Search Docs | Query the Laravel hosted documentation API service to retrieve documentation based on installed packages | -->
| 이름                 | 설명                                                                                                       |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| 애플리케이션 정보     | PHP 및 Laravel 버전, 데이터베이스 엔진, 버전이 포함된 생태계 패키지 목록, Eloquent 모델을 읽습니다 |
| 브라우저 로그         | 브라우저의 로그와 오류를 읽습니다                                                                       |
| 데이터베이스 연결     | 기본 연결을 포함해 사용 가능한 데이터베이스 연결을 검사합니다                                    |
| 데이터베이스 쿼리     | 데이터베이스에 대해 쿼리를 실행합니다                                                                        |
| 데이터베이스 스키마   | 데이터베이스 스키마를 읽습니다                                                                                    |
| 절대 URL 가져오기     | 에이전트가 유효한 URL을 생성할 수 있도록 상대 경로 URI를 절대 URI로 변환합니다                                        |
| 마지막 오류           | 애플리케이션 로그 파일에서 마지막 오류를 읽습니다                                                        |
| 로그 항목 읽기        | 마지막 N개의 로그 항목을 읽습니다                                                                                 |
| 규칙 기록             | 지속적으로 적용되는 [project rule](#project-rules)을 `.ai/rules`에 기록해 이후 에이전트가 이를 상속하도록 합니다                |
| 문서 검색             | 설치된 패키지를 기반으로 문서를 검색하기 위해 Laravel 호스팅 문서 API 서비스를 조회합니다    |

</div>

<a name="manually-registering-the-mcp-server"></a>
<!-- ### Manually Registering the MCP Server -->
### Manually Registering the MCP Server

<!-- Sometimes you may need to manually register the Laravel Boost MCP server with your editor of choice. You should register the MCP server using the following details: -->
때로는 원하는 에디터에 Laravel Boost MCP 서버를 수동으로 등록해야 할 수 있습니다. 다음 세부 정보를 사용하여 MCP 서버를 등록해야 합니다.

<table>
<!-- <tr><td><strong>Command</strong></td><td><code>php</code></td></tr> <tr><td><strong>Args</strong></td><td><code>artisan boost:mcp</code></td></tr> -->
<tr><td><strong>명령어</strong></td><td><code>php</code></td></tr>
<tr><td><strong>인수</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

<!-- JSON example: -->
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
<!-- ## AI Guidelines -->
## AI Guidelines

<!-- AI guidelines are composable instruction files that are loaded upfront to provide AI agents with essential context about Laravel ecosystem packages. These guidelines contain core conventions, best practices, and framework-specific patterns that help agents generate consistent, high-quality code. -->
AI 지침은 AI 에이전트에 Laravel 생태계 패키지에 대한 핵심 문맥을 미리 제공하기 위해 로드되는 조합 가능한 지시 파일입니다. 이 지침에는 에이전트가 일관되고 고품질의 코드를 생성하는 데 도움이 되는 핵심 규칙, 모범 사례, 프레임워크별 패턴이 포함되어 있습니다.

<a name="available-ai-guidelines"></a>
<!-- ### Available AI Guidelines -->
### Available AI Guidelines

<!-- Laravel Boost includes AI guidelines for the following packages and frameworks. The `core` guidelines provide generic, generalized advice to the AI for the given package that is applicable across all versions. -->
Laravel Boost에는 다음 패키지와 프레임워크를 위한 AI 지침이 포함되어 있습니다. `core` 지침은 해당 패키지의 모든 버전에 적용할 수 있는 일반적이고 범용적인 조언을 AI에 제공합니다.

<div class="overflow-auto">

<!-- | Package | Versions Supported | | ----------------- | ---------------------- | | Core & Boost | core | | Laravel Framework | core, 10.x, 11.x, 12.x, 13.x | | Livewire | core, 2.x, 3.x, 4.x | | Flux UI | core, free, pro | | Folio | core | | Herd | core | | Inertia Laravel | core, 1.x, 2.x, 3.x | | Inertia React | core, 1.x, 2.x, 3.x | | Inertia Vue | core, 1.x, 2.x, 3.x | | Inertia Svelte | core, 1.x, 2.x, 3.x | | MCP | core | | Pennant | core | | Pest | core, 3.x, 4.x | | PHPUnit | core | | Pint | core | | Sail | core | | Tailwind CSS | core, 3.x, 4.x | | Livewire Volt | core | | Wayfinder | core | | Enforce Tests | conditional | -->
| 패키지            | 지원 버전                  |
| ----------------- | -------------------------- |
| Core & Boost      | core                     |
| Laravel Framework | core, 10.x, 11.x, 12.x, 13.x |
| Livewire          | core, 2.x, 3.x, 4.x      |
| Flux UI           | core, free, pro          |
| Folio             | core                     |
| Herd              | core                     |
| Inertia Laravel   | core, 1.x, 2.x, 3.x      |
| Inertia React     | core, 1.x, 2.x, 3.x      |
| Inertia Vue       | core, 1.x, 2.x, 3.x      |
| Inertia Svelte    | core, 1.x, 2.x, 3.x      |
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

</div>

> [!NOTE]
> AI 가이드라인을 최신 상태로 유지하려면 [Keeping Boost Resources Updated](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="adding-custom-ai-guidelines"></a>
<!-- ### Adding Custom AI Guidelines -->
### Adding Custom AI Guidelines

<!-- To augment Laravel Boost with your own custom AI guidelines, add `.blade.php` or `.md` files to your application's `.ai/guidelines/*` directory. These files will automatically be included with Laravel Boost's guidelines when you run `boost:install`. -->
Laravel Boost에 직접 만든 커스텀 AI 지침을 추가하려면 애플리케이션의 `.ai/guidelines/*` 디렉터리에 `.blade.php` 또는 `.md` 파일을 추가합니다. 이 파일들은 `boost:install`을 실행할 때 Laravel Boost의 지침에 자동으로 포함됩니다.

<a name="overriding-boost-ai-guidelines"></a>
<!-- ### Overriding Boost AI Guidelines -->
### Overriding Boost AI Guidelines

<!-- You can override Boost's built-in AI guidelines by creating your own custom guidelines with matching file paths. When you create a custom guideline that matches an existing Boost guideline path, Boost will use your custom version instead of the built-in one. -->
일치하는 파일 경로를 가진 커스텀 지침을 만들어 Boost의 내장 AI 지침을 재정의할 수 있습니다. 기존 Boost 지침 경로와 일치하는 커스텀 지침을 만들면 Boost는 내장 지침 대신 커스텀 버전을 사용합니다.

<!-- For example, to override Boost's "Inertia React v2 Form Guidance" guidelines, create a file at `.ai/guidelines/inertia-react/2/forms.blade.php`. When you run `boost:install`, Boost will include your custom guideline instead of the default one. -->
예를 들어 Boost의 "Inertia React v2 Form Guidance" 지침을 재정의하려면 `.ai/guidelines/inertia-react/2/forms.blade.php` 파일을 만듭니다. `boost:install`을 실행하면 Boost는 기본 지침 대신 커스텀 지침을 포함합니다.

<a name="third-party-package-ai-guidelines"></a>
<!-- ### Third-Party Package AI Guidelines -->
### Third-Party Package AI Guidelines

<!-- If you maintain a third-party package and would like Boost to include AI guidelines for it, you can do so by adding a `resources/boost/guidelines/core.blade.php` file to your package. When users of your package run `php artisan boost:install`, Boost will automatically load your guidelines. -->
서드파티 패키지를 관리하고 있고 Boost가 해당 패키지의 AI 지침을 포함하도록 하고 싶다면, 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 지침을 자동으로 로드합니다.

<!-- AI guidelines should provide a short overview of what your package does, outline any required file structure or conventions, and explain how to create or use its main features (with example commands or code snippets). Keep them concise, actionable, and focused on best practices so AI can generate correct code for your users. Here is an example: -->
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
<!-- ## Agent Skills -->
## Agent Skills

<!-- [Agent Skills](https://agentskills.io/home) are lightweight, targeted knowledge modules that agents can activate on-demand when working on specific domains. Unlike guidelines, which are loaded upfront, skills allow detailed patterns and best practices to be loaded only when relevant, reducing context bloat and improving the relevance of AI-generated code. -->
[Agent Skills](https://agentskills.io/home)는 에이전트가 특정 도메인 작업을 할 때 필요에 따라 활성화할 수 있는 가볍고 목적이 분명한 지식 모듈입니다. 미리 로드되는 지침과 달리, 스킬은 관련성이 있을 때만 상세한 패턴과 모범 사례를 로드할 수 있게 해 줍니다. 이를 통해 문맥이 불필요하게 커지는 것을 줄이고 AI가 생성하는 코드의 관련성을 높입니다.

<!-- When you run `boost:install` and select skills as a feature, skills are automatically installed based on the packages detected in your `composer.json`. For example, if your project includes `livewire/livewire`, the `livewire-development` skill will be installed automatically. Skills included with Boost, such as `infer-conventions`, are installed regardless of which packages you have. -->
`boost:install`을 실행하고 기능으로 skills를 선택하면 `composer.json`에서 감지된 패키지를 기준으로 skills가 자동으로 설치됩니다. 예를 들어 프로젝트에 `livewire/livewire`가 포함되어 있으면 `livewire-development` skill이 자동으로 설치됩니다. `infer-conventions`처럼 Boost에 포함된 skills는 어떤 패키지를 사용하든 설치됩니다.

<a name="available-skills"></a>
<!-- ### Available Skills -->
### Available Skills

<div class="overflow-auto">

<!-- | Skill | Package | | -------------------------- | -------------- | | fluxui-development | Flux UI | | folio-routing | Folio | | infer-conventions | Boost | | inertia-react-development | Inertia React | | inertia-svelte-development | Inertia Svelte | | inertia-vue-development | Inertia Vue | | livewire-development | Livewire | | mcp-development | MCP | | pennant-development | Pennant | | pest-testing | Pest | | tailwindcss-development | Tailwind CSS | | volt-development | Volt | | wayfinder-development | Wayfinder | -->
| 기술 | 패키지 |
| -------------------------- | -------------- |
| fluxui-development         | Flux UI        |
| folio-routing              | Folio          |
| infer-conventions          | Boost          |
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

</div>

> [!NOTE]
> 기술 역량을 최신 상태로 유지하려면 [Keeping Boost Resources Updated](#keeping-boost-resources-updated) 섹션을 참고하세요.

<a name="custom-skills"></a>
<!-- ### Custom Skills -->
### Custom Skills

<!-- To create your own custom skills, add a `SKILL.md` file to your application's `.ai/skills/{skill-name}/` directory. When you run `boost:update`, your custom skills will be installed alongside Boost's built-in skills. -->
직접 커스텀 스킬을 만들려면 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가합니다. `boost:update`를 실행하면 커스텀 스킬이 Boost의 내장 스킬과 함께 설치됩니다.

<!-- For example, to create a custom skill for your application's domain logic: -->
예를 들어 애플리케이션의 도메인 로직을 위한 커스텀 스킬을 만들려면 다음 파일을 생성합니다.

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
<!-- ### Overriding Skills -->
### Overriding Skills

<!-- You can override Boost's built-in skills by creating your own custom skills with matching names. When you create a custom skill that matches an existing Boost skill name, Boost will use your custom version instead of the built-in one. -->
일치하는 이름을 가진 커스텀 스킬을 만들어 Boost의 내장 스킬을 재정의할 수 있습니다. 기존 Boost 스킬 이름과 일치하는 커스텀 스킬을 만들면 Boost는 내장 스킬 대신 커스텀 버전을 사용합니다.

<!-- For example, to override Boost's `livewire-development` skill, create a file at `.ai/skills/livewire-development/SKILL.md`. When you run `boost:update`, Boost will include your custom skill instead of the default one. -->
예를 들어 Boost의 `livewire-development` 스킬을 재정의하려면 `.ai/skills/livewire-development/SKILL.md` 파일을 만듭니다. `boost:update`를 실행하면 Boost는 기본 스킬 대신 커스텀 스킬을 포함합니다.

<a name="third-party-package-skills"></a>
<!-- ### Third-Party Package Skills -->
### Third-Party Package Skills

<!-- If you maintain a third-party package and would like Boost to include skills for it, you can do so by adding a `resources/boost/skills/{skill-name}/SKILL.md` file to your package. When users of your package run `php artisan boost:install`, Boost will automatically install your skills based on user preference. -->
서드파티 패키지를 관리하고 있고 Boost가 해당 패키지의 스킬을 포함하도록 하고 싶다면, 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지 사용자가 `php artisan boost:install`을 실행하면 Boost가 사용자 선택에 따라 스킬을 자동으로 설치합니다.

<!-- Boost Skills support the [Agent Skills format](https://agentskills.io/what-are-skills) and should be structured as a folder containing a `SKILL.md` file with YAML frontmatter and Markdown instructions. The `SKILL.md` file must include required frontmatter (`name` and `description`) and can optionally include scripts, templates, and reference materials. -->
Boost 스킬은 [Agent Skills format](https://agentskills.io/what-are-skills)을 지원하며, YAML frontmatter와 Markdown 지침이 포함된 `SKILL.md` 파일을 담은 폴더 구조여야 합니다. `SKILL.md` 파일에는 필수 frontmatter(`name`과 `description`)가 포함되어야 하며, 선택적으로 스크립트, 템플릿, 참고 자료를 포함할 수 있습니다.

<!-- Skills should outline any required file structure or conventions, and explain how to create or use its main features (with example commands or code snippets). Keep them concise, actionable, and focused on best practices so AI can generate correct code for your users: -->
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
<!-- ## Guidelines vs. Skills -->
## Guidelines vs. Skills

<!-- Laravel Boost provides two distinct ways to give AI agents context about your application: **guidelines** and **skills**. -->
Laravel Boost는 AI 에이전트에 애플리케이션에 대한 문맥을 제공하는 두 가지 서로 다른 방법인 **지침**과 **스킬**을 제공합니다.

<!-- **Guidelines** are loaded upfront when the AI agent starts, providing essential context about Laravel conventions and best practices that apply broadly across your codebase. -->
**지침**은 AI 에이전트가 시작될 때 미리 로드되어, 코드베이스 전반에 넓게 적용되는 Laravel 규칙과 모범 사례에 대한 핵심 문맥을 제공합니다.

<!-- **Skills** are activated on-demand when working on specific tasks, containing detailed patterns for particular domains (like Livewire components or Pest tests). Loading skills only when relevant reduces context bloat and improves code quality. -->
**스킬**은 특정 작업을 수행할 때 필요에 따라 활성화되며, Livewire 컴포넌트나 Pest 테스트 같은 특정 도메인에 대한 상세한 패턴을 포함합니다. 관련성이 있을 때만 스킬을 로드하면 문맥이 불필요하게 커지는 것을 줄이고 코드 품질을 높일 수 있습니다.

<div class="overflow-auto">

<!-- | Aspect | Guidelines | Skills | | ----------- | --------------------------------- | -------------------------------- | | **Loaded** | Upfront, always present | On-demand, when relevant | | **Scope** | Broad, foundational | Focused, task-specific | | **Purpose** | Core conventions & best practices | Detailed implementation patterns | -->
| 측면      | 가이드라인                        | 스킬                           |
| ----------- | --------------------------------- | -------------------------------- |
| **로드됨**  | 처음부터 항상 제공됨           | 관련 있을 때 온디맨드로 제공됨         |
| **범위**   | 광범위하고 기반이 됨               | 집중적이고 작업별로 구분됨           |
| **목적** | 핵심 규칙 및 모범 사례 | 구체적인 구현 패턴 |

</div>

<!-- Both guidelines and skills describe the Laravel ecosystem. To capture the conventions of your own application, you should use [project rules](#project-rules). -->
지침과 스킬은 모두 Laravel 생태계를 설명합니다. 애플리케이션의 고유한 규칙을 반영하려면 [project rules](#project-rules)를 사용해야 합니다.

<a name="project-rules"></a>
<!-- ## Project Rules -->
## Project Rules

<!-- While guidelines and skills teach agents how to write Laravel, project rules teach them how to write your application. A rule is anything you would otherwise need to explain again in every new session: -->
가이드라인과 스킬은 에이전트에게 Laravel을 작성하는 방법을 가르치지만, 프로젝트 규칙은 에이전트에게 애플리케이션을 작성하는 방법을 가르칩니다. 규칙이란 새로운 세션을 시작할 때마다 다시 설명해야 하는 모든 것을 의미합니다:

<div class="content-list" markdown="1">

<!-- - Decisions made along the way by you, your agents, or your teammates. - Style guidelines and preferences that are difficult to get an agent to follow. - Traps and constraints that can't be inferred from the surrounding code. -->
- 사용자, 에이전트 또는 팀원이 진행 중에 내린 결정
- 에이전트가 따르도록 하기가 어려운 스타일 가이드와 선호 사항
- 주변 코드만으로는 추론할 수 없는 함정과 제약 조건

</div>

<!-- Rules are stored as Markdown files within your application's `.ai/rules` directory and should be committed to source control. Unlike an agent's own memory, which is personal and session-scoped, your rules are shared with your team and with every agent that works on your application. -->
규칙은 애플리케이션의 `.ai/rules` 디렉터리에 Markdown 파일로 저장하며, 소스 제어에 커밋해야 합니다. 에이전트의 자체 메모리는 개인적이고 세션 범위로 제한되지만, 규칙은 팀과 애플리케이션에서 작업하는 모든 에이전트가 공유합니다.

<!-- Each rule file declares the file globs it applies to within its frontmatter: -->
각 규칙 파일은 프런트 matter에서 적용할 파일 glob을 선언합니다:

```markdown
---
paths:
  - app/Http/Controllers/**
---

# Http Controllers

## Extend BaseController for tenant scoping

All controllers must extend `App\Http\Controllers\BaseController`, which applies the
current tenant's query scope. Extending Laravel's base controller directly will leak
data across tenants.
```

<!-- In addition, Boost maintains an `.ai/rules/index.md` file which maps globs to their rule files. Agents are instructed to consult this index before planning or editing any file, so a rule is only loaded when it is relevant: -->
또한 Boost는 glob 패턴을 규칙 파일에 매핑하는 `.ai/rules/index.md` 파일을 관리합니다. 에이전트는 파일에 대한 계획을 세우거나 파일을 편집하기 전에 이 인덱스를 참조하도록 지시받으므로, 규칙은 관련이 있을 때만 로드됩니다:

```markdown
# Project Rules Index

Before planning or editing, find the row whose globs match the file's path and read that rule file.

| Applies to | Rule file |
| --- | --- |
| app/Http/Controllers/** | .ai/rules/controllers.md |
| app/Models/** | .ai/rules/models.md |
```

> [!NOTE]
> `.mcp.json` 및 생성된 가이드라인 파일과 달리, `.ai/rules` 디렉터리는 팀과 규칙을 공유할 수 있도록 소스 관리에 커밋해야 합니다.

<a name="recording-rules"></a>
<!-- ### Recording Rules -->
### Recording Rules

<!-- To record a rule, you may simply ask your agent to remember it: -->
규칙을 기록하려면 에이전트에게 해당 규칙을 기억해 달라고 요청하기만 하면 됩니다.

```text
Remember that all money values are stored as integer cents, never as floats.
```

<!-- The agent will invoke Boost's `record-rule` MCP tool with a `glob`, a short `title`, and a `note`. Boost will then file the rule under the matching area, creating the rule file if needed, and update the index. -->
에이전트는 `glob`, 짧은 `title`, `note`와 함께 Boost의 `record-rule` MCP 툴을 호출합니다. 그러면 Boost는 일치하는 영역에 규칙을 저장하고, 필요한 경우 규칙 파일을 생성한 다음 인덱스를 업데이트합니다.

<!-- You should always record rules using the `record-rule` tool rather than creating rule files by hand. Boost regenerates `.ai/rules/index.md` as part of recording a rule, and agents rely on that index to discover which rules apply to the file they are working on. A rule file that is added manually will not be discovered until the index is next regenerated. -->
항상 직접 규칙 파일을 만드는 대신 `record-rule` 도구를 사용해 규칙을 기록해야 합니다. Boost는 규칙을 기록하는 과정에서 `.ai/rules/index.md`를 다시 생성하며, 에이전트는 이 인덱스를 사용해 작업 중인 파일에 적용되는 규칙을 확인합니다. 수동으로 추가한 규칙 파일은 인덱스가 다음에 다시 생성될 때까지 검색되지 않습니다.

<a name="inferring-your-applications-conventions"></a>
<!-- ### Inferring Your Application's Conventions -->
### Inferring Your Application's Conventions

<!-- Recording rules one at a time works well going forward; however, an existing application already contains years of conventions. The `infer-conventions` skill will bootstrap your rules from the code you have already written. To get started, ask your agent to use the skill: -->
앞으로는 한 번에 하나씩 기록 규칙을 작성하는 방식이 잘 작동합니다. 하지만 기존 애플리케이션에는 이미 수년간 쌓인 규칙이 있습니다. `infer-conventions` 스킬은 이미 작성한 코드에서 규칙을 추출해 초기 규칙을 설정합니다. 시작하려면 에이전트에게 이 스킬을 사용하도록 요청하세요:

```text
Use the infer-conventions skill
```

<!-- The skill will sweep your application across a checklist of Laravel convention dimensions, including validation, controllers, authorization, models, architecture, testing, frontend, database, and console, followed by an open-ended pass for patterns such as base classes, shared traits, and module layouts. -->
이 스킬은 유효성 검증, 컨트롤러, 인가, 모델, 아키텍처, 테스트, 프론트엔드, 데이터베이스, 콘솔을 비롯한 Laravel 규칙 영역의 체크리스트를 기준으로 애플리케이션을 점검한 다음, 기본 클래스, 공유 트레이트, 모듈 구성과 같은 패턴을 폭넓게 검토합니다.

<!-- The skill documents what your code actually does rather than what it should do. It records only well-supported, non-default conventions, skips framework defaults and anything Pint or Rector already enforces, and reports genuinely mixed patterns instead of recording them. Before writing any rules, the skill will present each convention it discovered, along with its supporting evidence, for your approval. If you would like the skill to record all discovered conventions without confirmation, you may tell it to "yolo". -->
이 스킬은 코드가 어떻게 동작해야 하는지가 아니라 실제로 어떻게 동작하는지를 문서화합니다. 충분한 근거가 있는 비기본 규칙만 기록하고, 프레임워크 기본값과 Pint 또는 Rector가 이미 적용하는 규칙은 건너뛰며, 실제로 패턴이 혼재하는 경우에는 이를 기록하지 않고 보고합니다. 규칙을 작성하기 전에 스킬은 발견한 각 규칙과 이를 뒷받침하는 근거를 제시하고 승인을 요청합니다. 확인 없이 발견한 모든 규칙을 기록하게 하려면 "yolo"라고 입력하면 됩니다.

<a name="disabling-project-rules"></a>
<!-- ### Disabling Project Rules -->
### Disabling Project Rules

<!-- Project rules are enabled by default. To disable them entirely, define the following environment variable. This removes the `record-rule` MCP tool and stops Boost from managing the `.ai/rules` directory: -->
프로젝트 규칙은 기본적으로 활성화되어 있습니다. 프로젝트 규칙을 완전히 비활성화하려면 다음 환경 변수를 정의하세요. 그러면 `record-rule` MCP 도구가 제거되고 Boost가 `.ai/rules` 디렉터리를 관리하지 않게 됩니다:

```ini
BOOST_RULES_ENABLED=false
```

<a name="documentation-api"></a>
<!-- ## Documentation API -->
## Documentation API

<!-- Laravel Boost includes a Documentation API that provides AI agents with access to an extensive knowledge base containing over 17,000 pieces of Laravel-specific information. The API uses semantic search with embeddings to deliver precise, context-aware results. -->
Laravel Boost에는 AI 에이전트가 17,000개가 넘는 Laravel 전용 정보가 담긴 방대한 지식 베이스에 접근할 수 있게 해 주는 Documentation API가 포함되어 있습니다. 이 API는 임베딩을 사용한 의미 기반 검색으로 정확하고 문맥을 고려한 결과를 제공합니다.

<!-- The `Search Docs` MCP tool allows agents to query the Laravel hosted documentation API service to retrieve documentation based on your installed packages. Boost's AI guidelines and skills will automatically instruct your coding agent to use this API. -->
`Search Docs` MCP 도구를 사용하면 에이전트가 설치된 패키지를 기준으로 문서를 가져오기 위해 Laravel 호스팅 문서 API 서비스를 조회할 수 있습니다. Boost의 AI 지침과 스킬은 코딩 에이전트가 이 API를 사용하도록 자동으로 안내합니다.

<div class="overflow-auto">

<!-- | Package | Versions Supported | | ----------------- | ------------------ | | Laravel Framework | 10.x, 11.x, 12.x, 13.x | | Filament | 2.x, 3.x, 4.x, 5.x | | Flux UI | 2.x Free, 2.x Pro | | Inertia | 1.x, 2.x | | Livewire | 1.x, 2.x, 3.x, 4.x | | Nova | 4.x, 5.x | | Pest | 3.x, 4.x | | Tailwind CSS | 3.x, 4.x | -->
| 패키지           | 지원 버전         |
| ---------------- | ------------------ |
| Laravel Framework | 10.x, 11.x, 12.x, 13.x |
| Filament          | 2.x, 3.x, 4.x, 5.x |
| Flux UI           | 2.x Free, 2.x Pro  |
| Inertia           | 1.x, 2.x           |
| Livewire          | 1.x, 2.x, 3.x, 4.x |
| Nova              | 4.x, 5.x           |
| Pest              | 3.x, 4.x           |
| Tailwind CSS      | 3.x, 4.x           |

</div>

<a name="extending-boost"></a>
<!-- ## Extending Boost -->
## Extending Boost

<!-- Boost works with many popular IDEs and AI agents out of the box. If your coding tool isn't supported yet, you can create your own agent and integrate it with Boost. -->
Boost는 여러 인기 IDE와 AI 에이전트를 기본적으로 지원합니다. 아직 사용하는 코딩 도구가 지원되지 않는다면, 직접 에이전트를 만들고 Boost와 통합할 수 있습니다.

<a name="adding-support-for-other-ides-ai-agents"></a>
<!-- ### Adding Support for Other IDEs / AI Agents -->
### Adding Support for Other IDEs / AI Agents

<!-- To add support for a new IDE or AI agent, create a class that extends `Laravel\Boost\Install\Agents\Agent` and implement one or more of the following contracts depending on what you need: -->
새 IDE나 AI 에이전트 지원을 추가하려면 `Laravel\Boost\Install\Agents\Agent`를 확장하는 클래스를 만들고, 필요한 기능에 따라 다음 계약 중 하나 이상을 구현합니다.

<!-- - `Laravel\Boost\Contracts\SupportsGuidelines` - Adds support for AI guidelines. - `Laravel\Boost\Contracts\SupportsMcp` - Adds support for MCP. - `Laravel\Boost\Contracts\SupportsSkills` - Adds support for Agent Skills. -->
- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 가이드라인 지원을 추가합니다.
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원을 추가합니다.
- `Laravel\Boost\Contracts\SupportsSkills` - Agent Skills 지원을 추가합니다.

<a name="writing-the-agent"></a>
<!-- #### Writing the Agent -->
#### Writing the Agent

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

<!-- For an example implementation, see [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php). -->
구현 예시는 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)를 참고하세요.

<a name="registering-the-agent"></a>
<!-- #### Registering the Agent -->
#### Registering the Agent

<!-- Register your custom agent in the `boot` method of your application's `App\Providers\AppServiceProvider`: -->
애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 커스텀 에이전트를 등록합니다.

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

<!-- Once registered, your agent will be available for selection when running `php artisan boost:install`. -->
등록이 완료되면 `php artisan boost:install`을 실행할 때 해당 에이전트를 선택할 수 있습니다.
