# AI支援開発 (AI Assisted Development)

 - [Introduction](#introduction)
     - [Why Laravel for AI Development?](#why-laravel-for-ai-development)
 - [Laravelブースト](#laravel-boost)
     - [Installation](#installation)
     - [Available Tools](#available-tools)
     - [AI Guidelines](#ai-guidelines)
     - [Agent Skills](#agent-skills)
     - [Documentation Search](#documentation-search)
     - [Agents Integration](#agent-integration)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、AI 支援およびエージェント開発に最適なフレームワークとして独自の立場にあります。 [クロード・コード](https://docs.anthropic.com/en/docs/claude-code)、[OpenCode](https://opencode.ai)、[Cursor](https://cursor.com)、[GitHub コパイロット](https://github.com/features/copilot) などの AI コーディング エージェントの台頭により、開発者のコ​​ードの書き方は変わりました。これらのツールは、前例のない速度で機能全体を生成し、複雑な問題をデバッグし、コードをリファクタリングできます。しかし、その有効性は、コードベースをどの程度理解しているかに大きく依存します。

<a name="why-laravel-for-ai-development"></a>
### AI 開発に Laravel を選ぶ理由

Laravel の独自の規約と明確に定義された構造により、Laravel は AI 支援開発にとって理想的なフレームワークとなっています。 AI エージェントにコントローラの追加を依頼すると、AI エージェントはコントローラを配置する場所を正確に認識します。新しい移行が必要な場合、命名規則とファイルの場所は予測可能です。この一貫性により、より柔軟なフレームワークで AI ツールをつまずかせる推測作業が排除されます。

ファイル構成を超えて、Laravel の表現力豊かな構文と包括的なドキュメントは、AI エージェントに正確で慣用的なコードを生成するために必要なコンテキストを提供します。 Eloquent リレーションシップ、フォーム リクエスト、ミドルウェアなどの機能は、エージェントが確実に理解して複製できるパターンに従います。その結果、AI によって生成されたコードは、一般的な PHP スニペットをつなぎ合わせたものではなく、熟練した Laravel 開発者によって書かれたように見えます。

<a name="laravel-boost"></a>
## Laravelブースト (Laravel Boost)

[Laravelブースト](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを橋渡しします。 Boost は、アプリケーションの構造、データベース、ルートなどについての深い洞察を AI エージェントに提供する 15 を超える特殊なツールを備えた MCP (Model Context Protocol) サーバーです。 Boost をインストールすると、AI エージェントは汎用コード アシスタントから、特定のアプリケーションを理解する Laravel エキスパートに変わります。

Boost は 3 つの主要な機能を提供します。アプリケーションを検査して操作するための一連の MCP ツール、Laravel エコシステム向けに特別に作成された構成可能な AI ガイドライン、および 17,000 を超える Laravel 固有の知識を含む強力なドキュメント API です。

<a name="installation"></a>
### インストール

Boost は、PHP 8.1 以降を実行している Laravel 10、11、12、13 アプリケーションにインストールできます。まず、Boost を開発依存関係としてインストールします。

```shell
composer require laravel/boost --dev
```

インストールしたら、対話型インストーラーを実行します。

```shell
php artisan boost:install
```

インストーラーは IDE エージェントと AI エージェントを自動検出し、プロジェクトに適した統合を選択できるようにします。 Boost は、MCP 互換エディター用の `.mcp.json` や AI コンテキスト用のガイドライン ファイルなど、必要な構成ファイルを生成します。

> [!NOTE]
> 各開発者が独自の環境を構成したい場合は、`.mcp.json`、`CLAUDE.md`、`boost.json` などの生成された構成ファイルを `.gitignore` に安全に追加できます。

<a name="available-tools"></a>
### 利用可能なツール

Boost は、モデル コンテキスト プロトコルを介して包括的なツール セットを AI エージェントに公開します。これらのツールを使用すると、エージェントは Laravel アプリケーションを深く理解し、操作できるようになります。

<div class="content-list" markdown="1">

- **アプリケーションのイントロスペクション** - PHP および Laravel のバージョンをクエリし、インストールされているパッケージを一覧表示し、アプリケーションの構成変数と環境変数を検査します。
- **データベース ツール** - 会話を離れることなく、データベース スキーマを検査し、読み取り専用クエリを実行し、データ構造を理解します。
- **ルート検査** - 登録されているすべてのルートとそのミドルウェア、コントローラ、パラメーターを一覧表示します。
- **Artisan コマンド** - 利用可能なArtisan コマンドとその引数を検出し、エージェントがタスクに適切なコマンドを提案して実行できるようにします。
- **ログ分析** - アプリケーションのログ ファイルを読んで分析し、問題のデバッグに役立てます。
- **ブラウザ ログ** - Laravel のフロントエンド ツールを使用して開発する場合、ブラウザ コンソールのログとエラーにアクセスします。
- **Tinker の統合** - Laravel Tinker を介してアプリケーションのコンテキストで PHP コードを実行し、エージェントが仮説をテストして動作を検証できるようにします。
- **ドキュメント検索** - インストールされているパッケージのバージョンに合わせた結果で、Laravel エコシステムのドキュメントを検索します。

</div>

<a name="ai-guidelines"></a>
### AI ガイドライン

Boost には、Laravel エコシステム向けに特別に作成された包括的な AI ガイドラインのセットが含まれています。これらのガイドラインは、慣用的な Laravel コードを記述し、フレームワークの規則に従い、よくある落とし穴を回避する方法を AI エージェントに教えます。ガイドラインは構成可能でバージョンを認識します。つまり、エージェントは正確なパッケージ バージョンに適した指示を受け取ります。

ガイドラインは、Laravel 自体と、次のような Laravel エコシステム内の 16 以上のパッケージで利用できます。

<div class="content-list" markdown="1">

- Livewire (2.x、3.x、および 4.x)
- Inertia.js (React、Svelte、および Vue のバリアント)
- Tailwind CSS (3.x および 4.x)
- フィラメント (3.x および 4.x)
- PHPUユニット
- 害虫PHP
- LaravelPint
- 他にもたくさん

</div>

`boost:install` を実行すると、Boost はアプリケーションが使用するパッケージを自動的に検出し、関連するガイドラインをプロジェクトの AI コンテキスト ファイルにアセンブルします。

<a name="agent-skills"></a>
### エージェントのスキル

[エージェントのスキル](https://agentskills.io/home) は、エージェントが特定のドメインで作業するときにオンデマンドでアクティブ化できる軽量の対象を絞ったナレッジ モジュールです。事前に読み込まれるガイドラインとは異なり、スキルを使用すると、関連する場合にのみ詳細なパターンとベスト プラクティスを読み込むことができるため、コンテキストの肥大化が軽減され、AI によって生成されたコードの関連性が向上します。

スキルは、Livewire、Inertia、Tailwind CSS、Pest などの人気のある Laravel パッケージで利用できます。 `boost:install` を実行し、機能としてスキルを選択すると、`composer.json` で検出されたパッケージに基づいてスキルが自動的にインストールされます。

<a name="documentation-search"></a>
### ドキュメントの検索

Boost には、AI エージェントが 17,000 を超える Laravel エコシステム ドキュメントにアクセスできる強力なドキュメント API が含まれています。一般的な Web 検索とは異なり、このドキュメントは、正確なパッケージ バージョンに一致するようにインデックス付けされ、ベクトル化され、フィルター処理されます。

エージェントが機能の仕組みを理解する必要がある場合、Boost のドキュメント API を検索して、正確なバージョン固有の情報を受け取ることができます。これにより、AI エージェントが古いフレームワーク バージョンの非推奨のメソッドや構文を提案するという一般的な問題が解消されます。

<a name="agent-integration"></a>
### エージェントの統合

Boost は、モデル コンテキスト プロトコルをサポートする一般的な IDE および AI ツールと統合します。 Cursor、Claude Code、Codex、Gemini CLI、GitHub Copilot、および Junie の詳細なセットアップ手順については、Boost ドキュメントの [エージェントをセットアップする](/docs/{{version}}/boost#set-up-your-agents) セクションを参照してください。

