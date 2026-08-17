---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Creating a Laravel Application](#creating-a-laravel-project)
    - [Getting Started Using AI](#getting-started-using-ai)
    - [Installing PHP and the Laravel Installer](#installing-php)
    - [Creating an Application](#creating-an-application)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases and Migrations](#databases-and-migrations)
    - [Directory Configuration](#directory-configuration)
- [Installation Using Herd](#installation-using-herd)
    - [Herd on macOS](#herd-on-macos)
    - [Herd on Windows](#herd-on-windows)
- [IDE Support](#ide-support)
- [Laravel and AI](#laravel-and-ai)
    - [Installing Laravel Boost](#installing-laravel-boost)
- [Next Steps](#next-steps)
    - [Laravel the Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel the API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
<!-- ## Meet Laravel -->
## Meet Laravel

<!-- Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details. -->
Laravel は、表現力豊かでエレガントな構文を備えた Web アプリケーション フレームワークです。 Web フレームワークは、アプリケーション作成の構造と開始点を提供するため、私たちが詳細に取り組んでいる間、ユーザーは素晴らしいものを作成することに集中できます。

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel は、徹底した依存関係の注入、表現力豊かなデータベース抽象化レイヤー、キューとスケジュールされたジョブ、単体テストと統合テストなどの強力な機能を提供しながら、素晴らしい開発者エクスペリエンスを提供するよう努めています。

<!-- Whether you are new to PHP web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP Web フレームワークを初めて使用する場合でも、長年の経験がある場合でも、Laravel はあなたとともに成長できるフレームワークです。私たちは、Web 開発者としての最初の一歩を踏み出すお手伝いをしたり、専門知識を次のレベルに引き上げるサポートを提供します。あなたが何を構築するのか楽しみです。

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
Web アプリケーションを構築するときに利用できるさまざまなツールやフレームワークがあります。ただし、最新のフルスタック Web アプリケーションを構築するには Laravel が最適な選択であると考えています。

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
私たちは Laravel を「進歩的な」フレームワークと呼びたいと思っています。つまり、Laravel はあなたとともに成長するということです。 Web 開発への最初の一歩を踏み出したばかりの場合、Laravel のドキュメント、ガイド、[video tutorials](https://laracasts.com) の膨大なライブラリは、圧倒されることなくコツを学ぶのに役立ちます。

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/13.x/container), [unit testing](/docs/13.x/testing), [queues](/docs/13.x/queues), [real-time events](/docs/13.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise workloads. -->
あなたが上級開発者であれば、Laravel は [dependency injection](/docs/13.x/container)、[unit testing](/docs/13.x/testing)、[queues](/docs/13.x/queues)、[real-time events](/docs/13.x/broadcasting) などのための強力なツールを提供します。 Laravel はプロフェッショナルな Web アプリケーションを構築するために微調整されており、エンタープライズ ワークロードを処理する準備ができています。

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel は信じられないほどスケーラブルです。 PHP のスケーリングに適した性質と、Redis などの高速分散キャッシュ システムに対する Laravel の組み込みサポートのおかげで、Laravel による水平スケーリングは簡単です。実際、Laravel アプリケーションは、月あたり数億のリクエストを処理できるように簡単に拡張できます。

<!-- Need extreme scaling? Platforms like [Laravel Cloud](https://cloud.laravel.com) allow you to run your Laravel application at nearly limitless scale. -->
極端なスケーリングが必要ですか? [Laravel Cloud](https://cloud.laravel.com) のようなプラットフォームを使用すると、Laravel アプリケーションをほぼ無制限のスケールで実行できます。

<!-- #### An Agent Ready Framework -->
#### An Agent Ready Framework

<!-- Laravel's opinionated conventions and well-defined structure make it an ideal framework for [AI assisted development](/docs/13.x/ai) using tools like Cursor and Claude Code. When you ask an AI agent to add a controller, it knows exactly where to place it. When you need a new migration, the naming conventions and file locations are predictable. This consistency eliminates the guesswork that often trips up AI tools in more flexible frameworks. -->
Laravel の独自の規約と明確に定義された構造により、Cursor や Claude Code などのツールを使用する [AI assisted development](/docs/13.x/ai) にとって理想的なフレームワークになります。 AI エージェントにコントローラの追加を依頼すると、AI エージェントはコントローラを配置する場所を正確に認識します。新しい移行が必要な場合、命名規則とファイルの場所は予測可能です。この一貫性により、より柔軟なフレームワークで AI ツールをつまずかせる推測作業が排除されます。

<!-- Beyond file organization, Laravel's expressive syntax and comprehensive documentation give AI agents the context they need to generate accurate, idiomatic code. Features like Eloquent relationships, form requests, and middleware follow patterns that agents can reliably understand and replicate. The result is AI-generated code that looks like it was written by a seasoned Laravel developer, not stitched together from generic PHP snippets. -->
ファイル構成を超えて、Laravel の表現力豊かな構文と包括的なドキュメントは、AI エージェントに正確で慣用的なコードを生成するために必要なコンテキストを提供します。 Eloquent リレーションシップ、フォーム リクエスト、ミドルウェアなどの機能は、エージェントが確実に理解して複製できるパターンに従います。その結果、AI によって生成されたコードは、一般的な PHP スニペットをつなぎ合わせたものではなく、熟練した Laravel 開発者によって書かれたように見えます。

<!-- To learn more about why Laravel is the perfect choice for AI assisted development, check out our documentation on [agentic development](/docs/13.x/ai). -->
Laravel が AI 支援開発に最適な選択肢である理由について詳しくは、[agentic development](/docs/13.x/ai) のドキュメントをご覧ください。

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel は、PHP エコシステムの最高のパッケージを組み合わせて、利用可能な最も堅牢で開発者に優しいフレームワークを提供します。さらに、世界中の何千人もの才能ある開発者が [contributed to the framework](https://github.com/laravel/framework) を持っています。もしかしたら、あなたも Laravel のコントリビューターになれるかも知れません。

<a name="creating-a-laravel-project"></a>
<!-- ## Creating a Laravel Application -->
## Creating a Laravel Application

<a name="getting-started-using-ai"></a>
<!-- ### Getting Started Using AI -->
### Getting Started Using AI

<!-- If you are using an AI coding agent like [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or [OpenCode](https://opencode.ai), you can start with a prompt that gives the agent a Laravel-specific playbook before it touches your project. -->
[Claude Code](https://docs.anthropic.com/en/docs/claude-code) や [OpenCode](https://opencode.ai) などの AI コーディング エージェントを使用している場合は、プロジェクトに触れる前にエージェントに Laravel 固有の Playbook を提供するプロンプトから始めることができます。

<!-- The prompt below tells the agent where to find Laravel's installation guidance, what to prioritize, and how to make sensible defaults when you haven't made a choice yet. Paste this into your agent to get started: -->
以下のプロンプトは、エージェントに、Laravel のインストール ガイダンスの場所、何を優先するか、まだ選択していない場合に適切なデフォルトを設定する方法を示します。これをエージェントに貼り付けて開始します。

```text
I'm building a new Laravel application.

Fetch and follow the instructions from https://laravel.com/for/agents. Treat the returned Markdown as the source of truth for how to install and set up Laravel in this session.
```

<!-- After the agent reads the instructions, it should guide you step by step and keep the setup aligned with Laravel's defaults. -->
エージェントが手順を読んだ後、段階的にガイドし、セットアップを Laravel のデフォルトに合わせて維持します。

<a name="installing-php"></a>
<!-- ### Installing PHP and the Laravel Installer -->
### Installing PHP and the Laravel Installer

<!-- Before creating your first Laravel application, make sure that your local machine has [PHP](https://php.net), [Composer](https://getcomposer.org), and [the Laravel installer](https://github.com/laravel/installer) installed. In addition, you should install either [Node and NPM](https://nodejs.org) or [Bun](https://bun.sh/) so that you can compile your application's frontend assets. -->
最初の Laravel アプリケーションを作成する前に、ローカル マシンに [PHP](https://php.net)、[Composer](https://getcomposer.org)、および [the Laravel installer](https://github.com/laravel/installer) がインストールされていることを確認してください。さらに、アプリケーションのフロントエンド アセットをコンパイルできるように、[Node and NPM](https://nodejs.org) または [Bun](https://bun.sh/) をインストールする必要があります。

<!-- If you don't have PHP and Composer installed on your local machine, the following commands will install PHP, Composer, and the Laravel installer on macOS, Windows, or Linux: -->
ローカル マシンに PHP と Composer がインストールされていない場合は、次のコマンドで PHP、Composer、および Laravel インストーラーを macOS、Windows、または Linux にインストールします。

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.5)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.5'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.5)"
```

<!-- After running one of the commands above, you should restart your terminal session. To update PHP, Composer, and the Laravel installer after installing them via `php.new`, you can re-run the command in your terminal. -->
上記のコマンドのいずれかを実行した後、ターミナル セッションを再起動する必要があります。 `php.new` 経由でインストールした後に PHP、Composer、および Laravel インストーラーを更新するには、ターミナルでコマンドを再実行します。

<!-- If you already have PHP and Composer installed, you may install the Laravel installer via Composer: -->
すでに PHP と Composer がインストールされている場合は、Composer 経由で Laravel インストーラーをインストールできます。

```shell
composer global require laravel/installer
```

> [!NOTE]
> フル機能のグラフィカルな PHP のインストールと管理エクスペリエンスについては、[Laravel Herd](#installation-using-herd) をチェックしてください。

<a name="creating-an-application"></a>
<!-- ### Creating an Application -->
### Creating an Application

<!-- After you have installed PHP, Composer, and the Laravel installer, you are ready to create a new Laravel application: -->
PHP、Composer、および Laravel インストーラーをインストールしたら、新しい Laravel アプリケーションを作成する準備が整います。

```shell
laravel new example-app
```

<!-- Once the application has been created, you can start Laravel's local development server, queue worker, and Vite development server using the `dev` Composer script: -->
アプリケーションが作成されたら、`dev` Composer スクリプトを使用して、Laravel のローカル開発サーバー、キューワーカー、および Vite 開発サーバーを起動できます。

```shell
cd example-app
npm install && npm run build
composer run dev
```

<!-- Once you have started the development server, you can access your application in your web browser at [http://localhost:8000](http://localhost:8000). Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations) and run the necessary migrations. -->
開発サーバーを起動したら、Web ブラウザで [http://localhost:8000](http://localhost:8000) からアプリケーションにアクセスできます。次に、[start taking your next steps into the Laravel ecosystem](#next-steps) に進む準備ができました。もちろん、[configure a database](#databases-and-migrations) を設定し、必要なマイグレーションを実行することもできます。

> [!NOTE]
> Laravel アプリケーションの開発を早く始めたい場合は、[starter kits](/docs/13.x/starter-kits) のいずれかの使用を検討してください。 Laravel のスターター キットは、新しい Laravel アプリケーションにバックエンドおよびフロントエンドの認証スキャフォールディングを提供します。

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel フレームワークのすべての設定ファイルは `config` ディレクトリに保存されています。各オプションには説明が付いているので、ファイルを見ながら利用できるオプションを把握してみてください。

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `url` and `locale` that you may wish to change according to your application. -->
Laravel では、すぐに使用できる追加の構成はほとんど必要ありません。自由に開発を始めることができます。ただし、`config/app.php` ファイルとそのドキュメントを確認することをお勧めします。これには、`url` や `locale` などのいくつかのオプションが含まれており、アプリケーションに応じて変更できます。

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel の構成オプション値の多くは、アプリケーションがローカル マシンで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would be exposed. -->
アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が公開されるため、セキュリティ リスクになります。

> [!NOTE]
> `.env` ファイルと環境ベースの構成の詳細については、完全な [configuration documentation](/docs/13.x/configuration#environment-configuration) を確認してください。

<a name="databases-and-migrations"></a>
<!-- ### Databases and Migrations -->
### Databases and Migrations

<!-- Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with an SQLite database. -->
Laravel アプリケーションを作成したので、おそらくいくつかのデータをデータベースに保存したいと思うでしょう。デフォルトでは、アプリケーションの `.env` 構成ファイルは、Laravel が SQLite データベースと対話することを指定します。

<!-- During the creation of the application, Laravel created a `database/database.sqlite` file for you, and ran the necessary migrations to create the application's database tables. -->
アプリケーションの作成中に、Laravel は `database/database.sqlite` ファイルを作成し、アプリケーションのデータベーステーブルを作成するために必要な移行を実行しました。

<!-- If you prefer to use another database driver such as MySQL or PostgreSQL, you can update your `.env` configuration file to use the appropriate database. For example, if you wish to use MySQL, update your `.env` configuration file's `DB_*` variables like so: -->
MySQL や PostgreSQL などの別のデータベース ドライバを使用したい場合は、適切なデータベースを使用するように `.env` 構成ファイルを更新できます。たとえば、MySQL を使用する場合は、`.env` 構成ファイルの `DB_*` 変数を次のように更新します。

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

<!-- If you choose to use a database other than SQLite, you will need to create the database and run your application's [database migrations](/docs/13.x/migrations): -->
SQLite 以外のデータベースの使用を選択した場合は、データベースを作成し、アプリケーションの [database migrations](/docs/13.x/migrations) を実行する必要があります。

```shell
php artisan migrate
```

> [!NOTE]
> macOS または Windows で開発していて、MySQL、PostgreSQL、または Redis をローカルにインストールする必要がある場合は、[Herd Pro](https://herd.laravel.com/#plans) または [DBngin](https://dbngin.com/) の使用を検討してください。

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files present within your application. -->
Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="installation-using-herd"></a>
<!-- ## Installation Using Herd -->
## Installation Using Herd

<!-- [Laravel Herd](https://herd.laravel.com) is a blazing fast, native Laravel and PHP development environment for macOS and Windows. Herd includes everything you need to get started with Laravel development, including PHP and Nginx. -->
[Laravel Herd](https://herd.laravel.com) は、macOS および Windows 用の非常に高速なネイティブ Laravel および PHP 開発環境です。 Herd には、PHP や Nginx など、Laravel 開発を始めるために必要なものがすべて含まれています。

<!-- Once you install Herd, you're ready to start developing with Laravel. Herd includes command line tools for `php`, `composer`, `laravel`, `expose`, `node`, `npm`, and `nvm`. -->
Herd をインストールしたら、Laravel を使用して開発を開始する準備が整います。 Herd には、`php`、`composer`、`laravel`、`expose`、`node`、`npm`、および `nvm` のコマンド ライン ツールが含まれています。

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans) は、ローカルの MySQL、Postgres、Redis データベースの作成と管理、ローカル メールの表示とログの監視などの強力な機能を追加して Herd を強化します。

<a name="herd-on-macos"></a>
<!-- ### Herd on macOS -->
### Herd on macOS

<!-- If you develop on macOS, you can download the Herd installer from the [Herd website](https://herd.laravel.com). The installer automatically downloads the latest version of PHP and configures your Mac to always run [Nginx](https://www.nginx.com/) in the background. -->
macOS で開発する場合は、[Herd website](https://herd.laravel.com) から Herd インストーラーをダウンロードできます。インストーラーは最新バージョンの PHP を自動的にダウンロードし、常にバックグラウンドで [Nginx](https://www.nginx.com/) を実行するように Mac を設定します。

<!-- Herd for macOS uses [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) to support "parked" directories. Any Laravel application in a parked directory will automatically be served by Herd. By default, Herd creates a parked directory at `~/Herd` and you can access any Laravel application in this directory on the `.test` domain using its directory name. -->
Herd for macOS は、[dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) を使用して「パーク」ディレクトリをサポートします。パークディレクトリ内の Laravel アプリケーションはすべて、Herd によって自動的に提供されます。デフォルトでは、Herd は `~/Herd` にパークディレクトリを作成し、そのディレクトリ名を使用して、`.test` ドメイン上のこのディレクトリ内の任意の Laravel アプリケーションにアクセスできます。

<!-- After installing Herd, the fastest way to create a new Laravel application is using the Laravel CLI, which is bundled with Herd: -->
Herd をインストールした後、新しい Laravel アプリケーションを作成する最も早い方法は、Herd にバンドルされている Laravel CLI を使用することです。

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```

<!-- Of course, you can always manage your parked directories and other PHP settings via Herd's UI, which can be opened from the Herd menu in your system tray. -->
もちろん、システム トレイの Herd メニューから開くことができる Herd の UI を介して、パークしたディレクトリやその他の PHP 設定をいつでも管理できます。

<!-- You can learn more about Herd by checking out the [Herd documentation](https://herd.laravel.com/docs). -->
Herd について詳しくは、[Herd documentation](https://herd.laravel.com/docs) をご覧ください。

<a name="herd-on-windows"></a>
<!-- ### Herd on Windows -->
### Herd on Windows

<!-- You can download the Windows installer for Herd on the [Herd website](https://herd.laravel.com/windows). After the installation finishes, you can start Herd to complete the onboarding process and access the Herd UI for the first time. -->
Herd の Windows インストーラーは、[Herd website](https://herd.laravel.com/windows) からダウンロードできます。インストールが完了したら、Herd を起動してオンボーディング プロセスを完了し、Herd UI に初めてアクセスできます。

<!-- The Herd UI is accessible by left-clicking on Herd's system tray icon. A right-click opens the quick menu with access to all tools that you need on a daily basis. -->
Herd UI には、Herd のシステム トレイ アイコンを左クリックしてアクセスできます。右クリックするとクイック メニューが開き、日常的に必要なすべてのツールにアクセスできます。

<!-- During installation, Herd creates a "parked" directory in your home directory at `%USERPROFILE%\Herd`. Any Laravel application in a parked directory will automatically be served by Herd, and you can access any Laravel application in this directory on the `.test` domain using its directory name. -->
インストール中に、Herd は `%USERPROFILE%\Herd` のホーム ディレクトリに「パーク」ディレクトリを作成します。パークされたディレクトリ内のすべての Laravel アプリケーションは、Herd によって自動的に提供され、ディレクトリ名を使用して、`.test` ドメイン上のこのディレクトリ内のすべての Laravel アプリケーションにアクセスできます。

<!-- After installing Herd, the fastest way to create a new Laravel application is using the Laravel CLI, which is bundled with Herd. To get started, open Powershell and run the following commands: -->
Herd をインストールした後、新しい Laravel アプリケーションを作成する最も早い方法は、Herd にバンドルされている Laravel CLI を使用することです。まず、Powershell を開いて次のコマンドを実行します。

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```

<!-- You can learn more about Herd by checking out the [Herd documentation for Windows](https://herd.laravel.com/docs/windows). -->
Herd について詳しくは、[Herd documentation for Windows](https://herd.laravel.com/docs/windows) をご覧ください。

<a name="ide-support"></a>
<!-- ## IDE Support -->
## IDE Support

<!-- You are free to use any code editor you wish when developing Laravel applications. The [Laravel LSP](https://github.com/laravel/lsp) provides framework-aware editor support, including code completions, hover information, diagnostics, document links, go-to definition, and quick fixes for Laravel and Blade code. -->
Laravel アプリケーションの開発では、好きなコードエディタを自由に使用できます。[Laravel LSP](https://github.com/laravel/lsp) はフレームワークを認識したエディタサポートを提供し、Laravel と Blade のコードに対するコード補完、ホバー情報、診断、ドキュメントリンク、定義ジャンプ、クイックフィックスなどを利用できます。

<!-- To install the Laravel LSP, install it globally via Composer. Ensure that Composer's global vendor bin directory is on your `PATH`: -->
Laravel LSP をインストールするには、Composer 経由でグローバルにインストールします。Composer のグローバルな vendor bin ディレクトリが `PATH` に含まれていることを確認してください。

```shell
composer global require laravel/lsp
```

<!-- If you're looking for lightweight and extensible editors, [VS Code](https://code.visualstudio.com) or [Cursor](https://cursor.com) combined with the official [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) provides syntax highlighting, snippets, Artisan command integration, and automatic Laravel LSP support. Official Laravel extensions are also available for [Sublime Text](https://github.com/laravel/sublime-extension) and [Zed](https://github.com/laravel/zed-extension). Refer to the [Laravel LSP repository](https://github.com/laravel/lsp) for setup instructions for other language-server-compatible editors, including Neovim and OpenCode. -->
軽量で拡張可能なエディタをお探しの場合は、[VS Code](https://code.visualstudio.com) または [Cursor](https://cursor.com) と公式の [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) を組み合わせることで、構文の強調表示、スニペット、Artisan コマンドの統合、自動的な Laravel LSP サポートを利用できます。[Sublime Text](https://github.com/laravel/sublime-extension) と [Zed](https://github.com/laravel/zed-extension) 向けの公式 Laravel 拡張機能も用意されています。Neovim や OpenCode を含む、その他の language server 対応エディタのセットアップ方法については、[Laravel LSP repository](https://github.com/laravel/lsp) を参照してください。

<!-- For extensive and robust support of Laravel, take a look at [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025), a JetBrains IDE. PhpStorm's built-in Laravel framework support includes Blade templates, smart autocompletion for Eloquent models, routes, views, translations, and components, along with powerful code generation and navigation across Laravel projects. -->
Laravel の広範囲かつ堅牢なサポートについては、JetBrains IDE の [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025) をご覧ください。 PhpStorm の組み込み Laravel フレームワーク サポートには、Blade テンプレート、Eloquent モデルのスマート オートコンプリート、ルート、ビュー、翻訳、コンポーネントに加えて、強力なコード生成と Laravel プロジェクト全体のナビゲーションが含まれます。

<!-- For those seeking a cloud-based development experience, [Firebase Studio](https://firebase.studio/) provides instant access to building with Laravel directly in your browser. With zero setup required, Firebase Studio makes it easy to start building Laravel applications from any device. -->
クラウドベースの開発エクスペリエンスを求める人のために、[Firebase Studio](https://firebase.studio/) を使用すると、ブラウザーで直接 Laravel を使用して構築するための即時アクセスが提供されます。 Firebase Studio を使用すると、セットアップが不要で、どのデバイスからでも簡単に Laravel アプリケーションの構築を開始できます。

<a name="laravel-and-ai"></a>
<!-- ## Laravel and AI -->
## Laravel and AI

<!-- [Laravel Boost](https://github.com/laravel/boost) is a powerful tool that bridges the gap between AI coding agents and Laravel applications. Boost provides AI agents with Laravel-specific context, tools, and guidelines so they can generate more accurate, version-specific code that follows Laravel conventions. -->
[Laravel Boost](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを埋める強力なツールです。 Boost は、AI エージェントに Laravel 固有のコンテキスト、ツール、ガイドラインを提供するため、Laravel の規則に従って、より正確なバージョン固有のコードを生成できます。

<!-- When you install Boost in your Laravel application, AI agents gain access to over 15 specialized tools including the ability to know which packages you are using, query your database, search the Laravel documentation, read browser logs, generate tests, and execute code via Tinker. -->
Laravel アプリケーションに Boost をインストールすると、AI エージェントは、使用しているパッケージの把握、データベースのクエリ、Laravel ドキュメントの検索、ブラウザのログの読み取り、テストの生成、Tinker 経由のコードの実行など、15 を超える特殊なツールにアクセスできるようになります。

<!-- In addition, Boost gives AI agents access to over 17,000 pieces of vectorized Laravel ecosystem documentation, specific to your installed package versions. This means agents can provide guidance targeted to the exact versions your project uses. -->
さらに、Boost を使用すると、AI エージェントは、インストールされているパッケージのバージョンに応じて、17,000 を超えるベクトル化された Laravel エコシステム ドキュメントにアクセスできるようになります。これは、エージェントがプロジェクトで使用する正確なバージョンを対象としたガイダンスを提供できることを意味します。

<!-- Boost also includes Laravel-maintained AI guidelines that help agents to follow framework conventions, write appropriate tests, and avoid common pitfalls when generating Laravel code. -->
Boost には、エージェントがフレームワークの規則に従い、適切なテストを作成し、Laravel コードを生成するときによくある落とし穴を回避するのに役立つ、Laravel が管理する AI ガイドラインも含まれています。

<a name="installing-laravel-boost"></a>
<!-- ### Installing Laravel Boost -->
### Installing Laravel Boost

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

<!-- The installer will auto-detect your IDE and AI agents, allowing you to opt into the features that make sense for your project. Boost respects existing project conventions and doesn't force opinionated style rules by default. -->
インストーラーは IDE および AI エージェントを自動検出し、プロジェクトに適した機能を選択できるようにします。 Boost は既存のプロジェクトの規則を尊重し、デフォルトでは独自のスタイル ルールを強制しません。

> [!NOTE]
> Boostの詳細については、[Laravel Boost repository on GitHub](https://github.com/laravel/boost) をご覧ください。

<a name="adding-custom-ai-guidelines"></a>
<!-- #### Adding Custom AI Guidelines -->
#### Adding Custom AI Guidelines

<!-- To augment Laravel Boost with your own custom AI guidelines, add `.blade.php` or `.md` files to your application's `.ai/guidelines/*` directory. These files will automatically be included with Laravel Boost's guidelines when you run `boost:install`. -->
独自のカスタム AI ガイドラインで Laravel Boost を拡張するには、`.blade.php` または `.md` ファイルをアプリケーションの `.ai/guidelines/*` ディレクトリに追加します。これらのファイルは、`boost:install` を実行すると、Laravel Boost のガイドラインに自動的に組み込まれます。

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel application, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
Laravel アプリケーションを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<div class="content-list" markdown="1">

<!-- - [Request Lifecycle](/docs/13.x/lifecycle) - [Configuration](/docs/13.x/configuration) - [Directory Structure](/docs/13.x/structure) - [Frontend](/docs/13.x/frontend) - [Service Container](/docs/13.x/container) - [Facades](/docs/13.x/facades) -->
- [Request Lifecycle](/docs/13.x/lifecycle)
- [Configuration](/docs/13.x/configuration)
- [Directory Structure](/docs/13.x/structure)
- [Frontend](/docs/13.x/frontend)
- [Service Container](/docs/13.x/container)
- [Facades](/docs/13.x/facades)

</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel the Full Stack Framework -->
### Laravel the Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/13.x/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel. -->
Laravel はフルスタック フレームワークとして機能する可能性があります。 「フルスタック」フレームワークとは、Laravel を使用してリクエストをアプリケーションにルーティングし、[Blade templates](/docs/13.x/blade) または [Inertia](https://inertiajs.com) のような単一ページ アプリケーションのハイブリッド テクノロジを介してフロントエンドをレンダリングすることを意味します。これは、Laravel フレームワークを使用する最も一般的な方法であり、私たちの意見では、Laravel を使用する最も生産的な方法です。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/13.x/frontend), [routing](/docs/13.x/routing), [views](/docs/13.x/views), or the [Eloquent ORM](/docs/13.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://livewire.laravel.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
これが Laravel の使用方法である場合は、[frontend development](/docs/13.x/frontend)、[routing](/docs/13.x/routing)、[views](/docs/13.x/views)、または [Eloquent ORM](/docs/13.x/eloquent) に関するドキュメントを確認してください。さらに、[Livewire](https://livewire.laravel.com) や [Inertia](https://inertiajs.com) などのコミュニティ パッケージについても興味があるかもしれません。これらのパッケージを使用すると、シングルページ JavaScript アプリケーションによって提供される UI の利点の多くを享受しながら、Laravel をフルスタック フレームワークとして使用できるようになります。

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/13.x/vite). -->
Laravel をフルスタック フレームワークとして使用している場合は、[Vite](/docs/13.x/vite) を使用してアプリケーションの CSS と JavaScript をコンパイルする方法を学習することも強くお勧めします。

> [!NOTE]
> アプリケーションの構築をいち早く始めたい場合は、公式の [application starter kits](/docs/13.x/starter-kits) をチェックしてください。

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel the API Backend -->
### Laravel the API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/13.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel は、JavaScript シングルページ アプリケーションまたはモバイル アプリケーションへの API バックエンドとしても機能します。たとえば、[Next.js](https://nextjs.org) アプリケーションの API バックエンドとして Laravel を使用することができます。このコンテキストでは、Laravel を使用してアプリケーションに [authentication](/docs/13.x/sanctum) とデータ ストレージ/取得を提供すると同時に、キュー、電子メール、通知などの Laravel の強力なサービスも利用できます。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/13.x/routing), [Laravel Sanctum](/docs/13.x/sanctum), and the [Eloquent ORM](/docs/13.x/eloquent). -->
これが Laravel の使用方法である場合は、[routing](/docs/13.x/routing)、[Laravel Sanctum](/docs/13.x/sanctum)、および [Eloquent ORM](/docs/13.x/eloquent) に関するドキュメントを確認してください。
