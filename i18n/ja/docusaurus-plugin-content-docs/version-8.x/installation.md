---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Your First Laravel Project](#your-first-laravel-project)
    - [Getting Started On macOS](#getting-started-on-macos)
    - [Getting Started On Windows](#getting-started-on-windows)
    - [Getting Started On Linux](#getting-started-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
    - [Installation Via Composer](#installation-via-composer)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Directory Configuration](#directory-configuration)
- [Next Steps](#next-steps)
    - [Laravel The Full Stack Framework](#laravel-the-fullstack-framework)
    - [Laravel The API Backend](#laravel-the-api-backend)

<a name="meet-laravel"></a>
<!-- ## Meet Laravel -->
## Meet Laravel

<!-- Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details. -->
Laravel は、表現力豊かでエレガントな構文を備えた Web アプリケーション フレームワークです。 Web フレームワークは、アプリケーション作成の構造と開始点を提供するため、私たちが詳細に取り組んでいる間、ユーザーは素晴らしいものを作成することに集中できます。

<!-- Laravel strives to provide an amazing developer experience while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more. -->
Laravel は、徹底した依存関係の注入、表現力豊かなデータベース抽象化レイヤー、キューとスケジュールされたジョブ、単体テストと統合テストなどの強力な機能を提供しながら、素晴らしい開発者エクスペリエンスを提供するよう努めています。

<!-- Whether you are new to PHP or web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build. -->
PHP や Web フレームワークを初めて使用する場合でも、長年の経験がある場合でも、Laravel はあなたとともに成長できるフレームワークです。私たちは、Web 開発者としての最初の一歩を踏み出すお手伝いをしたり、専門知識を次のレベルに引き上げるサポートを提供します。あなたが何を構築するのか楽しみです。

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
Web アプリケーションを構築するときに利用できるさまざまなツールやフレームワークがあります。ただし、最新のフルスタック Web アプリケーションを構築するには Laravel が最適な選択であると考えています。

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
私たちは Laravel を「進歩的な」フレームワークと呼びたいと思っています。つまり、Laravel はあなたとともに成長するということです。 Web 開発への最初の一歩を踏み出したばかりの場合、Laravel のドキュメント、ガイド、[video tutorials](https://laracasts.com) の膨大なライブラリは、圧倒されることなくコツを学ぶのに役立ちます。

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/8.x/container), [unit testing](/docs/8.x/testing), [queues](/docs/8.x/queues), [real-time events](/docs/8.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads. -->
あなたが上級開発者であれば、Laravel は [dependency injection](/docs/8.x/container)、[unit testing](/docs/8.x/testing)、[queues](/docs/8.x/queues)、[real-time events](/docs/8.x/broadcasting) などのための強力なツールを提供します。 Laravel は、プロフェッショナルな Web アプリケーションを構築するために微調整されており、エンタープライズのワークロードを処理する準備ができています。

<!-- #### A Scalable Framework -->
#### A Scalable Framework

<!-- Laravel is incredibly scalable. Thanks to the scaling-friendly nature of PHP and Laravel's built-in support for fast, distributed cache systems like Redis, horizontal scaling with Laravel is a breeze. In fact, Laravel applications have been easily scaled to handle hundreds of millions of requests per month. -->
Laravel は信じられないほどスケーラブルです。 PHP のスケーリングに適した性質と、Redis などの高速分散キャッシュ システムに対する Laravel の組み込みサポートのおかげで、Laravel による水平スケーリングは簡単です。実際、Laravel アプリケーションは、月あたり数億のリクエストを処理できるように簡単に拡張できます。

<!-- Need extreme scaling? Platforms like [Laravel Vapor](https://vapor.laravel.com) allow you to run your Laravel application at nearly limitless scale on AWS's latest serverless technology. -->
極端なスケーリングが必要ですか? [Laravel Vapor](https://vapor.laravel.com) のようなプラットフォームを使用すると、AWS の最新のサーバーレステクノロジー上でほぼ無制限のスケールで Laravel アプリケーションを実行できます。

<!-- #### A Community Framework -->
#### A Community Framework

<!-- Laravel combines the best packages in the PHP ecosystem to offer the most robust and developer friendly framework available. In addition, thousands of talented developers from around the world have [contributed to the framework](https://github.com/laravel/framework). Who knows, maybe you'll even become a Laravel contributor. -->
Laravel は、PHP エコシステムの最高のパッケージを組み合わせて、利用可能な最も堅牢で開発者に優しいフレームワークを提供します。さらに、世界中の何千人もの才能ある開発者が [contributed to the framework](https://github.com/laravel/framework) を持っています。もしかしたら、あなたも Laravel のコントリビューターになれるかも知れません。

<a name="your-first-laravel-project"></a>
<!-- ## Your First Laravel Project -->
## Your First Laravel Project

<!-- We want it to be as easy as possible to get started with Laravel. There are a variety of options for developing and running a Laravel project on your own computer. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/8.x/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com). -->
私たちは、Laravel をできるだけ簡単に始められるようにしたいと考えています。自分のコンピュータで Laravel プロジェクトを開発および実行するには、さまざまなオプションがあります。これらのオプションを後で検討することもできますが、Laravel では、[Sail](/docs/8.x/sail) を使用して Laravel プロジェクトを実行するための組み込みソリューションである [Docker](https://www.docker.com) が提供されています。

<!-- Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local computer's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your personal computer. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). -->
Docker は、ローカル コンピューターにインストールされているソフトウェアや構成に干渉しない、小型軽量の「コンテナー」でアプリケーションやサービスを実行するためのツールです。これは、Web サーバーやデータベースなどの複雑な開発ツールをパーソナル コンピューター上で構成したりセットアップしたりすることを心配する必要がないことを意味します。開始するには、[Docker Desktop](https://www.docker.com/products/docker-desktop) をインストールするだけです。

<!-- Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
Laravel Sail は、Laravel のデフォルトの Docker 構成と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

> [!TIP]
> すでに Docker のエキスパートですか?心配しないで！ Sail に関するすべては、Laravel に含まれる `docker-compose.yml` ファイルを使用してカスタマイズできます。

<a name="getting-started-on-macos"></a>
<!-- ### Getting Started On macOS -->
### Getting Started On macOS

<!-- If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Mac で開発していて、[Docker Desktop](https://www.docker.com/products/docker-desktop) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s "https://laravel.build/example-app" | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!TIP]
> Laravel Sail についてさらに詳しく知りたい場合は、[complete documentation](/docs/8.x/sail) を確認してください。

<a name="getting-started-on-windows"></a>
<!-- ### Getting Started On Windows -->
### Getting Started On Windows

<!-- Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
Windows マシンに新しい Laravel アプリケーションを作成する前に、必ず [Docker Desktop](https://www.docker.com/products/docker-desktop) をインストールしてください。次に、Windows Subsystem for Linux 2 (WSL2) がインストールされ、有効になっていることを確認する必要があります。 WSL を使用すると、Linux バイナリ実行可能ファイルを Windows 10 上でネイティブに実行できます。WSL2 をインストールして有効にする方法に関する情報は、Microsoft の [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10) にあります。

> [!TIP]
> WSL2 をインストールして有効にした後、Docker デスクトップが [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/) であることを確認する必要があります。

<!-- Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
次に、最初の Laravel プロジェクトを作成する準備が整いました。 [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) を起動し、WSL2 Linux オペレーティング システムの新しいターミナル セッションを開始します。次に、単純なターミナル コマンドを使用して、新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!TIP]
> Laravel Sail についてさらに詳しく知りたい場合は、[complete documentation](/docs/8.x/sail) を確認してください。

<!-- #### Developing Within WSL2 -->
#### Developing Within WSL2

<!-- Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack). -->
もちろん、WSL2 インストール内で作成された Laravel アプリケーション ファイルを変更できる必要があります。これを実現するには、Microsoft の [Visual Studio Code](https://code.visualstudio.com) エディターと、同社の [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 用のファーストパーティ拡張機能を使用することをお勧めします。

<!-- Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal. -->
これらのツールをインストールしたら、Windows ターミナルを使用してアプリケーションのルート ディレクトリから `code .` コマンドを実行して、Laravel プロジェクトを開くことができます。

<a name="getting-started-on-linux"></a>
<!-- ### Getting Started On Linux -->
### Getting Started On Linux

<!-- If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Linux で開発していて、[Docker Compose](https://docs.docker.com/compose/install/) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```nothing
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」はお好みのものに変更できます。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```nothing
cd example-app

./vendor/bin/sail up
```

<!-- The first time you run the Sail `up` command, Sail's application containers will be built on your machine. This could take several minutes. **Don't worry, subsequent attempts to start Sail will be much faster.** -->
初めて Sail `up` コマンドを実行すると、Sail のアプリケーション コンテナーがマシン上に構築されます。これには数分かかる場合があります。 **心配しないでください。その後の Sail の開始試行ははるかに速くなります。**

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!TIP]
> Laravel Sail についてさらに詳しく知りたい場合は、[complete documentation](/docs/8.x/sail) を確認してください。

<a name="choosing-your-sail-services"></a>
<!-- ### Choosing Your Sail Services -->
### Choosing Your Sail Services

<!-- When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `minio`, `selenium`, and `mailhog`: -->
Sail 経由で新しい Laravel アプリケーションを作成する場合、`with` クエリ文字列変数を使用して、新しいアプリケーションの `docker-compose.yml` ファイルでどのサービスを構成するかを選択できます。利用可能なサービスには、`mysql`、`pgsql`、`mariadb`、`redis`、`memcached`、`meilisearch`、`minio`、`selenium`、および `mailhog` が含まれます。

```nothing
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

<!-- If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailhog`, and `selenium` will be configured. -->
設定するサービスを指定しない場合は、`mysql`、`redis`、`meilisearch`、`mailhog`、および `selenium` のデフォルト スタックが設定されます。

<a name="installation-via-composer"></a>
<!-- ### Installation Via Composer -->
### Installation Via Composer

<!-- If your computer already has PHP and Composer installed, you may create a new Laravel project by using Composer directly. After the application has been created, you may start Laravel's local development server using the Artisan CLI's `serve` command: -->
コンピューターにすでに PHP と Composer がインストールされている場合は、Composer を直接使用して新しい Laravel プロジェクトを作成できます。アプリケーションの作成後、Artisan CLI の `serve` コマンドを使用して、Laravel のローカル開発サーバーを起動できます。

```
composer create-project laravel/laravel:^8.0 example-app

cd example-app

php artisan serve
```

<a name="the-laravel-installer"></a>
<!-- #### The Laravel Installer -->
#### The Laravel Installer

<!-- Or, you may install the Laravel Installer as a global Composer dependency: -->
または、Laravel インストーラーをグローバル Composer 依存関係としてインストールすることもできます。

```nothing
composer global require laravel/installer

laravel new example-app

cd example-app

php artisan serve
```

<!-- Make sure to place Composer's system-wide vendor bin directory in your `$PATH` so the `laravel` executable can be located by your system. This directory exists in different locations based on your operating system; however, some common locations include: -->
`laravel` 実行可能ファイルがシステムで見つけられるように、Composer のシステム全体のベンダー bin ディレクトリを `$PATH` に配置してください。このディレクトリは、オペレーティング システムに応じて異なる場所に存在します。ただし、一般的な場所には次のようなものがあります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux Distributions: `$HOME/.config/composer/vendor/bin` or `$HOME/.composer/vendor/bin`
-->
- macOS: `$HOME/.composer/vendor/bin`
- Windows: `%USERPROFILE%\AppData\Roaming\Composer\vendor\bin`
- GNU / Linux ディストリビューション: `$HOME/.config/composer/vendor/bin` または `$HOME/.composer/vendor/bin`

<!-- </div> -->
</div>

<!-- For convenience, the Laravel installer can also create a Git repository for your new project. To indicate that you want a Git repository to be created, pass the `--git` flag when creating a new project: -->
便宜上、Laravel インストーラーは新しいプロジェクト用の Git リポジトリを作成することもできます。 Git リポジトリを作成することを示すには、新しいプロジェクトの作成時に `--git` フラグを渡します。

```bash
laravel new example-app --git
```

<!-- This command will initialize a new Git repository for your project and automatically commit the base Laravel skeleton. The `git` flag assumes you have properly installed and configured Git. You can also use the `--branch` flag to set the initial branch name: -->
このコマンドは、プロジェクトの新しい Git リポジトリを初期化し、基本 Laravel スケルトンを自動的にコミットします。 `git` フラグは、Git が適切にインストールおよび構成されていることを前提としています。 `--branch` フラグを使用して初期ブランチ名を設定することもできます。

```bash
laravel new example-app --git --branch="main"
```

<!-- Instead of using the `--git` flag, you may also use the `--github` flag to create a Git repository and also create a corresponding private repository on GitHub: -->
`--git` フラグを使用する代わりに、`--github` フラグを使用して Git リポジトリを作成し、GitHub 上に対応するプライベート リポジトリを作成することもできます。

```bash
laravel new example-app --github
```

<!-- The created repository will then be available at `https://github.com/<your-account>/example-app`. The `github` flag assumes you have properly installed the [GitHub CLI](https://cli.github.com) and are authenticated with GitHub. Additionally, you should have `git` installed and properly configured. If needed, you can pass additional flags that are supported by the GitHub CLI: -->
作成されたリポジトリは、`https://github.com/<your-account>/example-app` で利用できるようになります。 `github` フラグは、[GitHub CLI](https://cli.github.com) が適切にインストールされており、GitHub で認証されていることを前提としています。さらに、`git` がインストールされ、適切に構成されている必要があります。必要に応じて、GitHub CLI でサポートされている追加のフラグを渡すことができます。

```bash
laravel new example-app --github="--public"
```

<!-- You may use the `--organization` flag to create the repository under a specific GitHub organization: -->
`--organization` フラグを使用して、特定の GitHub 組織の下にリポジトリを作成できます。

```bash
laravel new example-app --github="--public" --organization="laravel"
```

<a name="initial-configuration"></a>
<!-- ## Initial Configuration -->
## Initial Configuration

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

<!-- Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application. -->
Laravel では、すぐに使用できる追加の構成はほとんど必要ありません。自由に開発を始めることができます。ただし、`config/app.php` ファイルとそのドキュメントを確認することをお勧めします。これには、`timezone` や `locale` などのいくつかのオプションが含まれており、アプリケーションに応じて変更できます。

<a name="environment-based-configuration"></a>
<!-- ### Environment Based Configuration -->
### Environment Based Configuration

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local computer or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel の構成オプション値の多くは、アプリケーションがローカル コンピューターで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

> [!TIP]
> `.env` ファイルと環境ベースの構成の詳細については、完全な [configuration documentation](/docs/8.x/configuration#environment-configuration) を確認してください。

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files that exist within your application. -->
Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
Laravel プロジェクトを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/8.x/lifecycle)
- [Configuration](/docs/8.x/configuration)
- [Directory Structure](/docs/8.x/structure)
- [Service Container](/docs/8.x/container)
- [Facades](/docs/8.x/facades)
-->
- [Request Lifecycle](/docs/8.x/lifecycle)
- [Configuration](/docs/8.x/configuration)
- [Directory Structure](/docs/8.x/structure)
- [Service Container](/docs/8.x/container)
- [Facades](/docs/8.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel The Full Stack Framework -->
### Laravel The Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/8.x/blade) or using a single-page application hybrid technology like [Inertia.js](https://inertiajs.com). This is the most common way to use the Laravel framework. -->
Laravel はフルスタック フレームワークとして機能する可能性があります。 「フルスタック」フレームワークとは、Laravel を使用してリクエストをアプリケーションにルーティングし、[Blade templates](/docs/8.x/blade) 経由で、または [Inertia.js](https://inertiajs.com) のような単一ページ アプリケーションのハイブリッド テクノロジを使用してフロントエンドをレンダリングすることを意味します。これは、Laravel フレームワークを使用する最も一般的な方法です。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/8.x/routing), [views](/docs/8.x/views), or the [Eloquent ORM](/docs/8.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://laravel-livewire.com) and [Inertia.js](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
これが Laravel の使用方法である場合は、[routing](/docs/8.x/routing)、[views](/docs/8.x/views)、または [Eloquent ORM](/docs/8.x/eloquent) に関するドキュメントを確認してください。さらに、[Livewire](https://laravel-livewire.com) や [Inertia.js](https://inertiajs.com) などのコミュニティ パッケージについても興味があるかもしれません。これらのパッケージを使用すると、シングルページ JavaScript アプリケーションによって提供される UI の利点の多くを享受しながら、Laravel をフルスタック フレームワークとして使用できるようになります。

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Laravel Mix](/docs/8.x/mix). -->
Laravel をフルスタック フレームワークとして使用している場合は、[Laravel Mix](/docs/8.x/mix) を使用してアプリケーションの CSS と JavaScript をコンパイルする方法を学習することも強くお勧めします。

> [!TIP]
> アプリケーションの構築をいち早く始めたい場合は、公式 [application starter kits](/docs/8.x/starter-kits) をチェックしてください。

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel The API Backend -->
### Laravel The API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/8.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel は、JavaScript シングルページ アプリケーションまたはモバイル アプリケーションへの API バックエンドとしても機能します。たとえば、[Next.js](https://nextjs.org) アプリケーションの API バックエンドとして Laravel を使用することができます。このコンテキストでは、Laravel を使用してアプリケーションに [authentication](/docs/8.x/sanctum) とデータ ストレージ/取得を提供すると同時に、キュー、電子メール、通知などの Laravel の強力なサービスも利用できます。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/8.x/routing), [Laravel Sanctum](/docs/8.x/sanctum), and the [Eloquent ORM](/docs/8.x/eloquent). -->
これが Laravel の使用方法である場合は、[routing](/docs/8.x/routing)、[Laravel Sanctum](/docs/8.x/sanctum)、および [Eloquent ORM](/docs/8.x/eloquent) に関するドキュメントを確認してください。

> [!TIP]
> Laravel バックエンドと Next.js フロントエンドのスキャフォールディングを早めに始める必要がありますか? Laravel Breeze は [API stack](/docs/8.x/starter-kits#breeze-and-next) だけでなく [Next.js frontend implementation](https://github.com/laravel/breeze-next) も提供しているので、数分で開始できます。


