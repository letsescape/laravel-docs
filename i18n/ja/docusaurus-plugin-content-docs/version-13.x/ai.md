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
Laravel は、AI 支援およびエージェント開発に最適なフレームワークとして独自の立場にあります。 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)、[OpenCode](https://opencode.ai)、[Cursor](https://cursor.com)、[GitHub Copilot](https://github.com/features/copilot) などの AI コーディング エージェントの台頭により、開発者のコ​​ードの書き方は変わりました。これらのツールは、前例のない速度で機能全体を生成し、複雑な問題をデバッグし、コードをリファクタリングできます。しかし、その有効性は、コードベースをどの程度理解しているかに大きく依存します。

<a name="why-laravel-for-ai-development"></a>
<!-- ### Why Laravel for AI Development? -->
### Why Laravel for AI Development?

<!-- Laravel's opinionated conventions and well-defined structure make it an ideal framework for AI assisted development. When you ask an AI agent to add a controller, it knows exactly where to place it. When you need a new migration, the naming conventions and file locations are predictable. This consistency eliminates the guesswork that often trips up AI tools in more flexible frameworks. -->
Laravel の独自の規約と明確に定義された構造により、Laravel は AI 支援開発にとって理想的なフレームワークとなっています。 AI エージェントにコントローラの追加を依頼すると、AI エージェントはコントローラを配置する場所を正確に認識します。新しい移行が必要な場合、命名規則とファイルの場所は予測可能です。この一貫性により、より柔軟なフレームワークで AI ツールをつまずかせる推測作業が排除されます。

<!-- Beyond file organization, Laravel's expressive syntax and comprehensive documentation give AI agents the context they need to generate accurate, idiomatic code. Features like Eloquent relationships, form requests, and middleware follow patterns that agents can reliably understand and replicate. The result is AI-generated code that looks like it was written by a seasoned Laravel developer, not stitched together from generic PHP snippets. -->
ファイル構成を超えて、Laravel の表現力豊かな構文と包括的なドキュメントは、AI エージェントに正確で慣用的なコードを生成するために必要なコンテキストを提供します。 Eloquent リレーションシップ、フォーム リクエスト、ミドルウェアなどの機能は、エージェントが確実に理解して複製できるパターンに従います。その結果、AI によって生成されたコードは、一般的な PHP スニペットをつなぎ合わせたものではなく、熟練した Laravel 開発者によって書かれたように見えます。

<a name="laravel-boost"></a>
<!-- ## Laravel Boost -->
## Laravel Boost

<!-- [Laravel Boost](https://github.com/laravel/boost) bridges the gap between AI coding agents and your Laravel application. Boost is an MCP (Model Context Protocol) server equipped with over 15 specialized tools that provide AI agents with deep insight into your application's structure, database, routes, and more. When you install Boost, your AI agent transforms from a general-purpose code assistant into a Laravel expert that understands your specific application. -->
[Laravel Boost](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを橋渡しします。 Boost は、アプリケーションの構造、データベース、ルートなどについての深い洞察を AI エージェントに提供する 15 を超える特殊なツールを備えた MCP (Model Context Protocol) サーバーです。 Boost をインストールすると、AI エージェントは汎用コード アシスタントから、特定のアプリケーションを理解する Laravel エキスパートに変わります。

<!-- Boost provides three major capabilities: a suite of MCP tools for inspecting and interacting with your application, composable AI guidelines crafted specifically for the Laravel ecosystem, and a powerful documentation API containing over 17,000 pieces of Laravel-specific knowledge. -->
Boost は 3 つの主要な機能を提供します。アプリケーションを検査して操作するための一連の MCP ツール、Laravel エコシステム向けに特別に作成された構成可能な AI ガイドライン、および 17,000 を超える Laravel 固有の知識を含む強力なドキュメント API です。

<a name="installation"></a>
<!-- ### Installation -->
### Installation

<!-- Boost can be installed in Laravel 10, 11, 12, and 13 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency: -->
Boost は、PHP 8.1 以降を実行している Laravel 10、11、12、13 アプリケーションにインストールできます。まず、Boost を開発依存関係としてインストールします。

```shell
composer require laravel/boost --dev
```

<!-- Once installed, run the interactive installer: -->
インストールしたら、対話型インストーラーを実行します。

```shell
php artisan boost:install
```

<!-- The installer will auto-detect your IDE and AI agents, allowing you to select the integrations that make sense for your project. Boost will generate the necessary configuration files, such as `.mcp.json` for MCP-compatible editors and guideline files for AI context. -->
インストーラーは IDE と AI エージェントを自動検出し、プロジェクトに適した統合を選択できるようにします。 Boost は、MCP 互換エディター用の `.mcp.json` や AI コンテキスト用のガイドライン ファイルなど、必要な構成ファイルを生成します。

> [!NOTE]
> 各開発者が独自の環境を構成したい場合は、`.mcp.json`、`CLAUDE.md`、`boost.json` などの生成された構成ファイルを `.gitignore` に安全に追加できます。

<a name="available-tools"></a>
<!-- ### Available Tools -->
### Available Tools

<!-- Boost exposes a comprehensive set of tools to AI agents via the Model Context Protocol. These tools allow agents to deeply understand and interact with your Laravel application: -->
Boost は、モデル コンテキスト プロトコルを介して包括的なツール セットを AI エージェントに公開します。これらのツールを使用すると、エージェントは Laravel アプリケーションを深く理解し、操作できるようになります。

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
- **アプリケーションのイントロスペクション** - PHP および Laravel のバージョンをクエリし、インストールされているパッケージを一覧表示し、アプリケーションの構成変数と環境変数を検査します。
- **データベース ツール** - 会話を離れることなく、データベース スキーマを検査し、読み取り専用クエリを実行し、データ構造を理解します。
- **ルート検査** - 登録されているすべてのルートとそのミドルウェア、コントローラ、パラメーターを一覧表示します。
- **Artisan コマンド** - 利用可能なArtisan コマンドとその引数を検出し、エージェントがタスクに適切なコマンドを提案して実行できるようにします。
- **ログ分析** - アプリケーションのログ ファイルを読んで分析し、問題のデバッグに役立てます。
- **ブラウザ ログ** - Laravel のフロントエンド ツールを使用して開発する場合、ブラウザ コンソールのログとエラーにアクセスします。
- **Tinker の統合** - Laravel Tinker を介してアプリケーションのコンテキストで PHP コードを実行し、エージェントが仮説をテストして動作を検証できるようにします。
- **ドキュメント検索** - インストールされているパッケージのバージョンに合わせた結果で、Laravel エコシステムのドキュメントを検索します。

<!-- </div> -->
</div>

<a name="ai-guidelines"></a>
<!-- ### AI Guidelines -->
### AI Guidelines

<!-- Boost includes a comprehensive set of AI guidelines specifically crafted for the Laravel ecosystem. These guidelines teach AI agents how to write idiomatic Laravel code, follow framework conventions, and avoid common pitfalls. Guidelines are composable and version-aware, meaning agents receive instructions appropriate for your exact package versions. -->
Boost には、Laravel エコシステム向けに特別に作成された包括的な AI ガイドラインのセットが含まれています。これらのガイドラインは、慣用的な Laravel コードを記述し、フレームワークの規則に従い、よくある落とし穴を回避する方法を AI エージェントに教えます。ガイドラインは構成可能でバージョンを認識します。つまり、エージェントは正確なパッケージ バージョンに適した指示を受け取ります。

<!-- Guidelines are available for Laravel itself and over 16 packages in the Laravel ecosystem, including: -->
ガイドラインは、Laravel 自体と、次のような Laravel エコシステム内の 16 以上のパッケージで利用できます。

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
- Livewire (2.x、3.x、および 4.x)
- Inertia.js (React、Svelte、および Vue のバリアント)
- Tailwind CSS (3.x および 4.x)
- Filament (3.x および 4.x)
- PHPUnit
- Pest PHP
- Laravel Pint
- 他にもたくさん

<!-- </div> -->
</div>

<!-- When you run `boost:install`, Boost automatically detects which packages your application uses and assembles the relevant guidelines into your project's AI context files. -->
`boost:install` を実行すると、Boost はアプリケーションが使用するパッケージを自動的に検出し、関連するガイドラインをプロジェクトの AI コンテキスト ファイルにアセンブルします。

<a name="agent-skills"></a>
<!-- ### Agent Skills -->
### Agent Skills

<!-- [Agent Skills](https://agentskills.io/home) are lightweight, targeted knowledge modules that agents can activate on-demand when working on specific domains. Unlike guidelines, which are loaded upfront, skills allow detailed patterns and best practices to be loaded only when relevant, reducing context bloat and improving the relevance of AI-generated code. -->
[Agent Skills](https://agentskills.io/home) は、エージェントが特定のドメインで作業するときにオンデマンドでアクティブ化できる軽量の対象を絞ったナレッジ モジュールです。事前に読み込まれるガイドラインとは異なり、スキルを使用すると、関連する場合にのみ詳細なパターンとベスト プラクティスを読み込むことができるため、コンテキストの肥大化が軽減され、AI によって生成されたコードの関連性が向上します。

<!-- Skills are available for popular Laravel packages like Livewire, Inertia, Tailwind CSS, Pest, and more. When you run `boost:install` and select skills as a feature, skills are automatically installed based on the packages detected in your `composer.json`. -->
スキルは、Livewire、Inertia、Tailwind CSS、Pest などの人気のある Laravel パッケージで利用できます。 `boost:install` を実行し、機能としてスキルを選択すると、`composer.json` で検出されたパッケージに基づいてスキルが自動的にインストールされます。

<a name="documentation-search"></a>
<!-- ### Documentation Search -->
### Documentation Search

<!-- Boost includes a powerful documentation API that gives AI agents access to over 17,000 pieces of Laravel ecosystem documentation. Unlike generic web searches, this documentation is indexed, vectorized, and filtered to match your exact package versions. -->
Boost には、AI エージェントが 17,000 を超える Laravel エコシステム ドキュメントにアクセスできる強力なドキュメント API が含まれています。一般的な Web 検索とは異なり、このドキュメントは、正確なパッケージ バージョンに一致するようにインデックス付けされ、ベクトル化され、フィルター処理されます。

<!-- When an agent needs to understand how a feature works, it can search Boost's documentation API and receive accurate, version-specific information. This eliminates the common problem of AI agents suggesting deprecated methods or syntax from older framework versions. -->
エージェントが機能の仕組みを理解する必要がある場合、Boost のドキュメント API を検索して、正確なバージョン固有の情報を受け取ることができます。これにより、AI エージェントが古いフレームワーク バージョンの非推奨のメソッドや構文を提案するという一般的な問題が解消されます。

<a name="agents-integration"></a>
<!-- ### Agents Integration -->
### Agents Integration

<!-- Boost integrates with popular IDEs and AI tools that support the Model Context Protocol. For detailed setup instructions for Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, and Junie, see the [Set Up Your Agents](/docs/13.x/boost#set-up-your-agents) section of the Boost documentation. -->
Boost は、モデル コンテキスト プロトコルをサポートする一般的な IDE および AI ツールと統合します。 Cursor、Claude Code、Codex、Gemini CLI、GitHub Copilot、および Junie の詳細なセットアップ手順については、Boost ドキュメントの [Set Up Your Agents](/docs/13.x/boost#set-up-your-agents) セクションを参照してください。

