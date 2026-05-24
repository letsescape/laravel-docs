# Laravelブースト (Laravel Boost)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Boost リソースを常に最新の状態に保つ](#keeping-boost-resources-updated)
    - [エージェントをセットアップする](#set-up-your-agents)
- [MCPサーバー](#mcp-server)
    - [利用可能な MCP ツール](#available-mcp-tools)
    - [MCP サーバーの手動登録](#manually-registering-the-mcp-server)
- [AI ガイドライン](#ai-guidelines)
    - [利用可能な AI ガイドライン](#available-ai-guidelines)
    - [カスタム AI ガイドラインの追加](#adding-custom-ai-guidelines)
    - [Boost AI ガイドラインの上書き](#overriding-boost-ai-guidelines)
    - [サードパーティパッケージ AI ガイドライン](#third-party-package-ai-guidelines)
- [エージェントのスキル](#agent-skills)
    - [利用可能なスキル](#available-skills)
    - [カスタムスキル](#custom-skills)
    - [オーバーライドスキル](#overriding-skills)
    - [サードパーティパッケージのスキル](#third-party-package-skills)
- [ガイドラインとスキル](#guidelines-vs-skills)
- [ドキュメントAPI](#documentation-api)
- [ブーストの延長](#extending-boost)
    - [他の IDE / AI エージェントのサポートの追加](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel Boost は、AI エージェントが Laravel のベストプラクティスに準拠した高品質の Laravel アプリケーションを作成するのに役立つ重要なガイドラインとエージェント スキルを提供することで、AI 支援開発を加速します。

Boost は、組み込みの MCP ツールと、17,000 を超える Laravel 固有の情報を含む広範なナレッジ ベースを組み合わせた強力な Laravel エコシステム ドキュメント API も提供します。これらはすべて、正確でコンテキストを認識した結果を得るために埋め込みを使用したセマンティック検索機能によって強化されています。 Boost は、Claude Code や Cursor などの AI エージェントに、この API を使用して最新の Laravel 機能とベストプラクティスについて学習するように指示します。

<a name="installation"></a>
## インストール (Installation)

Laravel Boost は Composer 経由でインストールできます。

```shell
composer require laravel/boost --dev
```

次に、MCP サーバーとコーディング ガイドラインをインストールします。

```shell
php artisan boost:install
```

`boost:install` コマンドは、インストール プロセス中に選択したコーディング エージェントに関連するエージェント ガイドラインとスキル ファイルを生成します。

Laravel Boost がインストールされたら、Cursor、Claude Code、または選択した AI エージェントを使用してコーディングを開始する準備が整います。

> [!NOTE]
> 生成された MCP 構成ファイル (`.mcp.json`)、ガイドライン ファイル (`CLAUDE.md`、`AGENTS.md`、`junie/` など)、および `boost.json` 構成ファイルをアプリケーションの `.gitignore` に自由に追加してください。これらのファイルは、`boost:install` の実行時に自動的に再生成され、 `boost:update`。

<a name="set-up-your-agents"></a>
### エージェントをセットアップする

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
### Boost リソースを常に最新の状態に保つ

ローカルの Boost リソース (AI ガイドラインとスキル) を定期的に更新して、インストールした Laravel エコシステム パッケージの最新バージョンが確実に反映されるようにすることをお勧めします。これを行うには、`boost:update` Artisan コマンドを使用します。

```shell
php artisan boost:update
```

Composer の「post-update-cmd」スクリプトにこのプロセスを追加することで、このプロセスを自動化することもできます。

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
## MCPサーバー (MCP Server)

Laravel Boost は、AI エージェントが Laravel アプリケーションと対話するためのツールを公開する MCP (Model Context Protocol) サーバーを提供します。これらのツールを使用すると、エージェントはアプリケーションの構造の検査、データベースのクエリ、コードの実行などを行うことができます。

<a name="available-mcp-tools"></a>
### 利用可能な MCP ツール

| 名前                       | 注意事項                                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 申請情報           | PHP と Laravel のバージョン、データベース エンジン、エコシステム パッケージのバージョンと Eloquent モデルのリストを読む |
| ブラウザログ               | ブラウザからログとエラーを読み取る                                                                       |
| データベース接続       | デフォルト接続を含む、利用可能なデータベース接続を検査する                                    |
| データベースクエリ             | データベースに対してクエリを実行する                                                                        |
| データベーススキーマ            | データベーススキーマを読み取る                                                                                    |
| 絶対URLの取得           | エージェントが有効な URL を生成できるように、相対パス URI を絶対パスに変換します                                        |
| 構成の取得                 | 「ドット」表記を使用して構成ファイルから値を取得します                                               |
| 最後のエラー                 | アプリケーションのログ ファイルから最後のエラーを読み取ります                                                        |
| Artisan コマンドのリスト      | 使用可能なArtisan コマンドを確認する                                                                      |
| 使用可能な構成キーのリスト | 利用可能な構成キーを検査する                                                                    |
| 利用可能な環境変数をリストする    | 使用可能な環境変数キーを検査する                                                             |
| ルートのリスト                | アプリケーションのルートを検査する                                                                            |
| ログエントリの読み取り           | 最新の N 個のログ エントリを読み取る                                                                                 |
| ドキュメントの検索                | Laravel でホストされているドキュメント API サービスにクエリを実行して、インストールされているパッケージに基づいてドキュメントを取得します    |
| Tinker                     | アプリケーションのコンテキスト内で任意のコードを実行する                                                |

<a name="manually-registering-the-mcp-server"></a>
### MCP サーバーの手動登録

場合によっては、選択したエディターに Laravel Boost MCP サーバーを手動で登録する必要がある場合があります。次の詳細を使用して MCP サーバーを登録する必要があります。

<table>
<tr><td><strong>コマンド</strong></td><td><code>php</code></td></tr>
<tr><td><strong>引数</strong></td><td><code>artisan boost:mcp</code></td></tr>
</table>

JSON の例:

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
## AI ガイドライン (AI Guidelines)

AI ガイドラインは、AI エージェントに Laravel エコシステム パッケージに関する重要なコンテキストを提供するために、事前にロードされる構成可能な命令ファイルです。これらのガイドラインには、エージェントが一貫した高品質のコードを生成するのに役立つ、中心的な規則、ベスト プラクティス、およびフレームワーク固有のパターンが含まれています。

<a name="available-ai-guidelines"></a>
### 利用可能な AI ガイドライン

Laravel Boost には、次のパッケージとフレームワークの AI ガイドラインが含まれています。 `core` ガイドラインは、すべてのバージョンに適用できる、特定のパッケージに対する AI への一般的なアドバイスを提供します。

| パッケージ           | サポートされているバージョン     |
| ----------------- | ---------------------- |
| コア＆ブースト      | コア                   |
| Laravelフレームワーク | コア、10.x、11.x、12.x |
| Livewire          | コア、2.x、3.x、4.x    |
| フラックスUI           | コア、無料、プロ        |
| Folio             | コア                   |
| Herd              | コア                   |
| InertiaLaravel   | コア、1.x、2.x         |
| Inertia反応     | コア、1.x、2.x         |
| イナーシャビュー       | コア、1.x、2.x         |
| イナーシャ・スヴェルト    | コア、1.x、2.x         |
| MCP               | コア                   |
| Pennant           | コア                   |
| 害虫              | コア、3.x、4.x         |
| PHPUユニット           | コア                   |
| Pint              | コア                   |
| 帆              | コア                   |
| Tailwind CSS      | コア、3.x、4.x         |
| Livewire Volt     | コア                   |
| ウェイファインダー         | コア                   |
| テストを強制する     | 条件付き            |

> **注:** AI ガイドラインを最新の状態に保つには、[Boost リソースを常に最新の状態に保つ](#keeping-boost-resources-updated) セクションを参照してください。

<a name="adding-custom-ai-guidelines"></a>
### カスタム AI ガイドラインの追加

独自のカスタム AI ガイドラインで Laravel Boost を拡張するには、`.blade.php` または `.md` ファイルをアプリケーションの `.ai/guidelines/*` ディレクトリに追加します。これらのファイルは、`boost:install` を実行すると、Laravel Boost のガイドラインに自動的に組み込まれます。

<a name="overriding-boost-ai-guidelines"></a>
### Boost AI ガイドラインの上書き

一致するファイル パスを使用して独自のカスタム ガイドラインを作成することで、Boost の組み込み AI ガイドラインをオーバーライドできます。既存の Boost ガイドライン パスに一致するカスタム ガイドラインを作成すると、Boost は組み込みバージョンの代わりにカスタム バージョンを使用します。

たとえば、Boost の「Inertia React v2 Form Guide」ガイドラインをオーバーライドするには、`.ai/guidelines/inertia-react/2/forms.blade.php` にファイルを作成します。 `boost:install` を実行すると、Boost にはデフォルトのガイドラインの代わりにカスタム ガイドラインが含まれます。

<a name="third-party-package-ai-guidelines"></a>
### サードパーティパッケージ AI ガイドライン

サードパーティのパッケージを管理しており、Boost にそのパッケージの AI ガイドラインを含めたい場合は、`resources/boost/guidelines/core.blade.php` ファイルをパッケージに追加することで実現できます。パッケージのユーザーが `php artisan boost:install` を実行すると、Boost は自動的にガイドラインをロードします。

AI ガイドラインでは、パッケージが何を行うのかについての簡単な概要を提供し、必要なファイル構造や規則の概要を示し、その主な機能の作成方法や使用方法を (コマンド例やコード スニペットを使用して) 説明する必要があります。 AI がユーザー向けに正しいコードを生成できるように、簡潔で実用的でベスト プラクティスに焦点を当てたものにしてください。以下に例を示します。

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
## エージェントのスキル (Agent Skills)

[エージェントのスキル](https://agentskills.io/home) は、エージェントが特定のドメインで作業するときにオンデマンドでアクティブ化できる軽量の対象を絞ったナレッジ モジュールです。事前に読み込まれるガイドラインとは異なり、スキルを使用すると、関連する場合にのみ詳細なパターンとベスト プラクティスを読み込むことができるため、コンテキストの肥大化が軽減され、AI によって生成されたコードの関連性が向上します。

`boost:install` を実行し、機能としてスキルを選択すると、`composer.json` で検出されたパッケージに基づいてスキルが自動的にインストールされます。たとえば、プロジェクトに `livewire/livewire` が含まれている場合、`livewire-development` スキルが自動的にインストールされます。

<a name="available-skills"></a>
### 利用可能なスキル

| スキル                      | パッケージ        |
| -------------------------- | -------------- |
| フラクスイ開発         | フラックスUI        |
| Folio ルーティング              | Folio          |
| Inertia反応開発  | Inertia反応  |
| 惰性的な開発 | イナーシャ・スヴェルト |
| Inertiaビュー開発    | イナーシャビュー    |
| Livewire開発       | Livewire       |
| mcp開発            | MCP            |
| Pennant 開発        | Pennant        |
| 害虫検査               | 害虫           |
| tailwindcss 開発    | Tailwind CSS   |
| Volt 開発           | Volt           |
| ウェイファインダー開発      | ウェイファインダー      |

> **注:** スキルを最新の状態に保つには、[Boost リソースを常に最新の状態に保つ](#keeping-boost-resources-updated) セクションを参照してください。

<a name="custom-skills"></a>
### カスタムスキル

独自のカスタム スキルを作成するには、`SKILL.md` ファイルをアプリケーションの `.ai/skills/{skill-name}/` ディレクトリに追加します。 `boost:update` を実行すると、カスタム スキルが Boost の組み込みスキルと一緒にインストールされます。

たとえば、アプリケーションのドメイン ロジックのカスタム スキルを作成するには、次のようにします。

```
.ai/skills/creating-invoices/SKILL.md
```

<a name="overriding-skills"></a>
### オーバーライドスキル

一致する名前を持つ独自のカスタム スキルを作成することで、Boost の組み込みスキルをオーバーライドできます。既存の Boost スキル名と一致するカスタム スキルを作成すると、Boost は組み込みバージョンの代わりにカスタム バージョンを使用します。

たとえば、Boost の `livewire-development` スキルをオーバーライドするには、`.ai/skills/livewire-development/SKILL.md` にファイルを作成します。 `boost:update` を実行すると、Boost にはデフォルトのスキルの代わりにカスタム スキルが含まれます。

<a name="third-party-package-skills"></a>
### サードパーティパッケージのスキル

サードパーティのパッケージを管理しており、Boost にそのパッケージのスキルを含めたい場合は、`resources/boost/skills/{skill-name}/SKILL.md` ファイルをパッケージに追加することで実現できます。パッケージのユーザーが `php artisan boost:install` を実行すると、Boost はユーザーの設定に基づいてスキルを自動的にインストールします。

Boost Skills は [エージェントスキル形式](https://agentskills.io/what-are-skills) をサポートしており、YAML フロントマッターと Markdown 命令を含む `SKILL.md` ファイルを含むフォルダーとして構造化する必要があります。 `SKILL.md` ファイルには、必要なフロントマター (`name` および `description`) が含まれている必要があり、オプションでスクリプト、テンプレート、および参考資料を含めることができます。

スキルは、必要なファイル構造または規則の概要を説明し、その主な機能の作成方法または使用方法を (コマンド例またはコード スニペットを使用して) 説明する必要があります。 AI がユーザー向けに正しいコードを生成できるように、簡潔で実用的でベスト プラクティスに焦点を当てたものにしてください。

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
## ガイドラインとスキル (Guidelines vs. Skills)

Laravel Boost は、AI エージェントにアプリケーションに関するコンテキストを提供する 2 つの異なる方法、**ガイドライン** と **スキル**を提供します。

**ガイドライン**は、AI エージェントの起動時に事前に読み込まれ、コードベース全体に広く適用される Laravel の規則とベスト プラクティスに関する重要なコンテキストを提供します。

**スキル**は、特定のドメイン (Livewire コンポーネントやペスト テストなど) の詳細なパターンを含む特定のタスクに取り組むときにオンデマンドでアクティブ化されます。関連する場合にのみスキルを読み込むことで、コンテキストの肥大化が軽減され、コードの品質が向上します。

| 側面      | ガイドライン                        | スキル                           |
| ----------- | --------------------------------- | -------------------------------- |
| **ロード済み**  | 率直に、常に存在する           | 必要に応じてオンデマンドで         |
| **範囲**   | 幅広く、基礎的な               | 焦点を絞った、特定のタスクに特化した           |
| **目的** | 中心となる規約とベストプラクティス | 詳細な実装パターン |

<a name="documentation-api"></a>
## ドキュメントAPI (Documentation API)

Laravel Boost には、17,000 を超える Laravel 固有の情報を含む広範なナレッジ ベースへのアクセスを AI エージェントに提供するドキュメント API が含まれています。 API は、埋め込みを使用したセマンティック検索を使用して、正確でコンテキストを認識した結果を提供します。

`Search Docs` MCP ツールを使用すると、エージェントは Laravel でホストされているドキュメント API サービスにクエリを実行し、インストールされているパッケージに基づいてドキュメントを取得できます。 Boost の AI ガイドラインとスキルは、コーディング エージェントにこの API を使用するように自動的に指示します。

| パッケージ           | サポートされているバージョン |
| ----------------- | ------------------ |
| Laravelフレームワーク | 10.x、11.x、12.x   |
| フィラメント          | 2.x、3.x、4.x、5.x |
| フラックスUI           | 2.x 無料、2.x プロ  |
| Inertia           | 1.x、2.x           |
| Livewire          | 1.x、2.x、3.x、4.x |
| ノヴァ              | 4.x、5.x           |
| 害虫              | 3.x、4.x           |
| Tailwind CSS      | 3.x、4.x           |

<a name="extending-boost"></a>
## ブーストの延長 (Extending Boost)

Boost は、多くの人気のある IDE および AI エージェントでそのまま動作します。コーディング ツールがまだサポートされていない場合は、独自のエージェントを作成して Boost と統合できます。

<a name="adding-support-for-other-ides-ai-agents"></a>
### 他の IDE / AI エージェントのサポートの追加

新しい IDE または AI エージェントのサポートを追加するには、`Laravel\Boost\Install\Agents\Agent` を拡張するクラスを作成し、必要に応じて次の 1 つ以上のコントラクトを実装します。

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI ガイドラインのサポートを追加します。
- `Laravel\Boost\Contracts\SupportsMcp` - MCP のサポートを追加します。
- `Laravel\Boost\Contracts\SupportsSkills` - エージェント スキルのサポートを追加します。

<a name="writing-the-agent"></a>
#### エージェントの作成

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

実装例については、[ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php) を参照してください。

<a name="registering-the-agent"></a>
#### エージェントの登録

アプリケーションの `App\Providers\AppServiceProvider` の `boot` メソッドにカスタム エージェントを登録します。

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

登録すると、`php artisan boost:install` を実行するときにエージェントを選択できるようになります。

