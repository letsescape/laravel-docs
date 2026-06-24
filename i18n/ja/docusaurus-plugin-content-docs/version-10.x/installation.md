---
slug: /
---

<!-- # Installation -->
# Installation

- [Meet Laravel](#meet-laravel)
    - [Why Laravel?](#why-laravel)
- [Creating a Laravel Project](#creating-a-laravel-project)
- [Initial Configuration](#initial-configuration)
    - [Environment Based Configuration](#environment-based-configuration)
    - [Databases and Migrations](#databases-and-migrations)
    - [Directory Configuration](#directory-configuration)
- [Docker Installation Using Sail](#docker-installation-using-sail)
    - [Sail on macOS](#sail-on-macos)
    - [Sail on Windows](#sail-on-windows)
    - [Sail on Linux](#sail-on-linux)
    - [Choosing Your Sail Services](#choosing-your-sail-services)
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

> [!NOTE]
> Laravel は初めてですか?最初の Laravel アプリケーションを構築する手順を説明しながら、フレームワークの実践的なツアーについては、[Laravel Bootcamp](https://bootcamp.laravel.com) をご覧ください。

<a name="why-laravel"></a>
<!-- ### Why Laravel? -->
### Why Laravel?

<!-- There are a variety of tools and frameworks available to you when building a web application. However, we believe Laravel is the best choice for building modern, full-stack web applications. -->
Web アプリケーションを構築するときに利用できるさまざまなツールやフレームワークがあります。ただし、最新のフルスタック Web アプリケーションを構築するには Laravel が最適な選択であると考えています。

<!-- #### A Progressive Framework -->
#### A Progressive Framework

<!-- We like to call Laravel a "progressive" framework. By that, we mean that Laravel grows with you. If you're just taking your first steps into web development, Laravel's vast library of documentation, guides, and [video tutorials](https://laracasts.com) will help you learn the ropes without becoming overwhelmed. -->
私たちは Laravel を「進歩的な」フレームワークと呼びたいと思っています。つまり、Laravel はあなたとともに成長するということです。 Web 開発への最初の一歩を踏み出したばかりの場合、Laravel のドキュメント、ガイド、[video tutorials](https://laracasts.com) の膨大なライブラリは、圧倒されることなくコツを学ぶのに役立ちます。

<!-- If you're a senior developer, Laravel gives you robust tools for [dependency injection](/docs/10.x/container), [unit testing](/docs/10.x/testing), [queues](/docs/10.x/queues), [real-time events](/docs/10.x/broadcasting), and more. Laravel is fine-tuned for building professional web applications and ready to handle enterprise work loads. -->
あなたが上級開発者であれば、Laravel は [dependency injection](/docs/10.x/container)、[unit testing](/docs/10.x/testing)、[queues](/docs/10.x/queues)、[real-time events](/docs/10.x/broadcasting) などのための強力なツールを提供します。 Laravel は、プロフェッショナルな Web アプリケーションを構築するために微調整されており、エンタープライズのワークロードを処理する準備ができています。

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

<a name="creating-a-laravel-project"></a>
<!-- ## Creating a Laravel Project -->
## Creating a Laravel Project

<!-- Before creating your first Laravel project, make sure that your local machine has PHP and [Composer](https://getcomposer.org) installed. If you are developing on macOS, PHP and Composer can be installed in minutes via [Laravel Herd](https://herd.laravel.com). In addition, we recommend [installing Node and NPM](https://nodejs.org). -->
最初の Laravel プロジェクトを作成する前に、ローカル マシンに PHP と [Composer](https://getcomposer.org) がインストールされていることを確認してください。 macOS で開発している場合は、[Laravel Herd](https://herd.laravel.com) を介して PHP と Composer を数分でインストールできます。また、[installing Node and NPM](https://nodejs.org) を推奨します。

<!-- After you have installed PHP and Composer, you may create a new Laravel project via Composer's `create-project` command: -->
PHP と Composer をインストールした後、Composer の `create-project` コマンドを使用して新しい Laravel プロジェクトを作成できます。

```nothing
composer create-project "laravel/laravel:^10.0" example-app
```

<!-- Or, you may create new Laravel projects by globally installing [the Laravel installer](https://github.com/laravel/installer) via Composer: -->
または、Composer 経由で [the Laravel installer](https://github.com/laravel/installer) をグローバルにインストールすることで、新しい Laravel プロジェクトを作成することもできます。

```nothing
composer global require laravel/installer

laravel new example-app
```

<!-- Once the project has been created, start Laravel's local development server using Laravel Artisan's `serve` command: -->
プロジェクトが作成されたら、Laravel Artisan の `serve` コマンドを使用して、Laravel のローカル開発サーバーを起動します。

```nothing
cd example-app

php artisan serve
```

<!-- Once you have started the Artisan development server, your application will be accessible in your web browser at [http://localhost:8000](http://localhost:8000). Next, you're ready to [start taking your next steps into the Laravel ecosystem](#next-steps). Of course, you may also want to [configure a database](#databases-and-migrations). -->
Artisan 開発サーバーを起動すると、Web ブラウザ ([http://localhost:8000](http://localhost:8000)) でアプリケーションにアクセスできるようになります。次に、[start taking your next steps into the Laravel ecosystem](#next-steps) の準備が整いました。もちろん、[configure a database](#databases-and-migrations) することもできます。

> [!NOTE]
> Laravel アプリケーションの開発を早く始めたい場合は、[starter kits](/docs/10.x/starter-kits) のいずれかの使用を検討してください。 Laravel のスターター キットは、新しい Laravel アプリケーションにバックエンドおよびフロントエンドの認証スキャフォールディングを提供します。

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

<!-- Since many of Laravel's configuration option values may vary depending on whether your application is running on your local machine or on a production web server, many important configuration values are defined using the `.env` file that exists at the root of your application. -->
Laravel の構成オプション値の多くは、アプリケーションがローカル マシンで実行されているか実稼働 Web サーバーで実行されているかによって異なる場合があるため、多くの重要な構成値は、アプリケーションのルートに存在する `.env` ファイルを使用して定義されます。

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

> [!NOTE]
> `.env` ファイルと環境ベースの構成の詳細については、完全な [configuration documentation](/docs/10.x/configuration#environment-configuration) を確認してください。

<a name="databases-and-migrations"></a>
<!-- ### Databases and Migrations -->
### Databases and Migrations

<!-- Now that you have created your Laravel application, you probably want to store some data in a database. By default, your application's `.env` configuration file specifies that Laravel will be interacting with a MySQL database and will access the database at `127.0.0.1`. -->
Laravel アプリケーションを作成したので、おそらくいくつかのデータをデータベースに保存したいと思うでしょう。デフォルトでは、アプリケーションの `.env` 構成ファイルは、Laravel が MySQL データベースと対話し、`127.0.0.1` でデータベースにアクセスすることを指定します。

> [!NOTE]
> macOS で開発していて、MySQL、Postgres、または Redis をローカルにインストールする必要がある場合は、[DBngin](https://dbngin.com/) の使用を検討してください。

<!-- If you do not want to install MySQL or Postgres on your local machine, you can always use a [SQLite](https://www.sqlite.org/index.html) database. SQLite is a small, fast, self-contained database engine. To get started, update your `.env` configuration file to use Laravel's `sqlite` database driver. You may remove the other database configuration options: -->
MySQL または Postgres をローカル マシンにインストールしたくない場合は、いつでも [SQLite](https://www.sqlite.org/index.html) データベースを使用できます。 SQLite は、小型、高速、自己完結型のデータベース エンジンです。まず、Laravel の `sqlite` データベースドライバを使用するように `.env` 構成ファイルを更新します。他のデータベース構成オプションは削除できます。

```ini
DB_CONNECTION=sqlite # [tl! add]
DB_CONNECTION=mysql # [tl! remove]
DB_HOST=127.0.0.1 # [tl! remove]
DB_PORT=3306 # [tl! remove]
DB_DATABASE=laravel # [tl! remove]
DB_USERNAME=root # [tl! remove]
DB_PASSWORD= # [tl! remove]
```

<!-- Once you have configured your SQLite database, you may run your application's [database migrations](/docs/10.x/migrations), which will create your application's database tables: -->
SQLite データベースを構成したら、アプリケーションの [database migrations](/docs/10.x/migrations) を実行すると、アプリケーションのデータベース テーブルが作成されます。

```shell
php artisan migrate
```

<!-- If an SQLite database does not exist for your application, Laravel will ask you if you would like the database to be created. Typically, the SQLite database file will be created at `database/database.sqlite`. -->
アプリケーションに SQLite データベースが存在しない場合、Laravel はデータベースを作成するかどうかを尋ねます。通常、SQLite データベース ファイルは `database/database.sqlite` に作成されます。

<a name="directory-configuration"></a>
<!-- ### Directory Configuration -->
### Directory Configuration

<!-- Laravel should always be served out of the root of the "web directory" configured for your web server. You should not attempt to serve a Laravel application out of a subdirectory of the "web directory". Attempting to do so could expose sensitive files present within your application. -->
Laravel は常に、Web サーバーに設定された「Web ディレクトリ」のルートから提供される必要があります。 「Web ディレクトリ」のサブディレクトリから Laravel アプリケーションを提供しようとしないでください。これを試みると、アプリケーション内に存在する機密ファイルが公開される可能性があります。

<a name="docker-installation-using-sail"></a>
<!-- ## Docker Installation Using Sail -->
## Docker Installation Using Sail

<!-- We want it to be as easy as possible to get started with Laravel regardless of your preferred operating system. So, there are a variety of options for developing and running a Laravel project on your local machine. While you may wish to explore these options at a later time, Laravel provides [Sail](/docs/10.x/sail), a built-in solution for running your Laravel project using [Docker](https://www.docker.com). -->
私たちは、好みのオペレーティング システムに関係なく、できるだけ簡単に Laravel を始められるようにしたいと考えています。したがって、ローカルマシン上で Laravel プロジェクトを開発および実行するには、さまざまなオプションがあります。これらのオプションを後で検討することもできますが、Laravel では、[Sail](/docs/10.x/sail) を使用して Laravel プロジェクトを実行するための組み込みソリューションである [Docker](https://www.docker.com) が提供されています。

<!-- Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local machine's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your local machine. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop). -->
Docker は、ローカル マシンにインストールされているソフトウェアや構成に干渉しない、小型軽量の「コンテナ」でアプリケーションやサービスを実行するためのツールです。これは、ローカル マシン上で Web サーバーやデータベースなどの複雑な開発ツールの構成やセットアップについて心配する必要がないことを意味します。開始するには、[Docker Desktop](https://www.docker.com/products/docker-desktop) をインストールするだけです。

<!-- Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
Laravel Sail は、Laravel のデフォルトの Docker 構成と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

> [!NOTE]
> すでに Docker の専門家ですか?心配しないで！ Sail に関するすべては、Laravel に含まれる `docker-compose.yml` ファイルを使用してカスタマイズできます。

<a name="sail-on-macos"></a>
<!-- ### Sail on macOS -->
### Sail on macOS

<!-- If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
Mac で開発していて、[Docker Desktop](https://www.docker.com/products/docker-desktop) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s "https://laravel.build/example-app" | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]
> Laravel Sail についてさらに学習するには、[complete documentation](/docs/10.x/sail) を参照してください。

<a name="sail-on-windows"></a>
<!-- ### Sail on Windows -->
### Sail on Windows

<!-- Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
Windows マシンに新しい Laravel アプリケーションを作成する前に、必ず [Docker Desktop](https://www.docker.com/products/docker-desktop) をインストールしてください。次に、Windows Subsystem for Linux 2 (WSL2) がインストールされ、有効になっていることを確認する必要があります。 WSL を使用すると、Linux バイナリ実行可能ファイルを Windows 10 上でネイティブに実行できます。WSL2 をインストールして有効にする方法に関する情報は、Microsoft の [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10) にあります。

> [!NOTE]
> WSL2 をインストールして有効にした後、Docker Desktop が [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/) であることを確認する必要があります。

<!-- Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
次に、最初の Laravel プロジェクトを作成する準備が整いました。 [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) を起動し、WSL2 Linux オペレーティング システムの新しいターミナル セッションを開始します。次に、単純なターミナル コマンドを使用して、新しい Laravel プロジェクトを作成できます。たとえば、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]
> Laravel Sail についてさらに学習するには、[complete documentation](/docs/10.x/sail) を参照してください。

<!-- #### Developing Within WSL2 -->
#### Developing Within WSL2

<!-- Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack). -->
もちろん、WSL2 インストール内で作成された Laravel アプリケーション ファイルを変更できる必要があります。これを実現するには、Microsoft の [Visual Studio Code](https://code.visualstudio.com) エディターと、同社の [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) 用のファーストパーティ拡張機能を使用することをお勧めします。

<!-- Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal. -->
これらのツールをインストールしたら、Windows ターミナルを使用してアプリケーションのルート ディレクトリから `code .` コマンドを実行して、Laravel プロジェクトを開くことができます。

<a name="sail-on-linux"></a>
<!-- ### Sail on Linux -->
### Sail on Linux

<!-- If you're developing on Linux and [Docker Compose](https://docs.docker.com/compose/install/) is already installed, you can use a simple terminal command to create a new Laravel project. -->
Linux で開発していて、[Docker Compose](https://docs.docker.com/compose/install/) がすでにインストールされている場合は、単純なターミナル コマンドを使用して新しい Laravel プロジェクトを作成できます。

<!-- First, if you are using Docker Desktop for Linux, you should execute the following command. If you are not using Docker Desktop for Linux, you may skip this step: -->
まず、Docker Desktop for Linux を使用している場合は、次のコマンドを実行する必要があります。 Linux 用 Docker Desktop を使用していない場合は、この手順をスキップできます。

```shell
docker context use default
```

<!-- Then, to create a new Laravel application in a directory named "example-app", you may run the following command in your terminal: -->
次に、「example-app」という名前のディレクトリに新しい Laravel アプリケーションを作成するには、ターミナルで次のコマンドを実行します。

```shell
curl -s https://laravel.build/example-app | bash
```

<!-- Of course, you can change "example-app" in this URL to anything you like - just make sure the application name only contains alpha-numeric characters, dashes, and underscores. The Laravel application's directory will be created within the directory you execute the command from. -->
もちろん、この URL の「example-app」を好きなものに変更できます。ただし、アプリケーション名には英数字、ダッシュ、アンダースコアのみが含まれていることを確認してください。 Laravelアプリケーションのディレクトリは、コマンドを実行したディレクトリ内に作成されます。

<!-- Sail installation may take several minutes while Sail's application containers are built on your local machine. -->
Sail のアプリケーション コンテナーがローカル マシン上に構築されるまで、Sail のインストールには数分かかる場合があります。

<!-- After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration: -->
プロジェクトが作成されたら、アプリケーション ディレクトリに移動して Laravel Sail を開始できます。 Laravel Sail は、Laravel のデフォルトの Docker 設定と対話するためのシンプルなコマンドライン インターフェイスを提供します。

```shell
cd example-app

./vendor/bin/sail up
```

<!-- Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. -->
アプリケーションの Docker コンテナが開始されると、Web ブラウザで http://localhost. からアプリケーションにアクセスできます。

> [!NOTE]
> Laravel Sail についてさらに学習するには、[complete documentation](/docs/10.x/sail) を参照してください。

<a name="choosing-your-sail-services"></a>
<!-- ### Choosing Your Sail Services -->
### Choosing Your Sail Services

<!-- When creating a new Laravel application via Sail, you may use the `with` query string variable to choose which services should be configured in your new application's `docker-compose.yml` file. Available services include `mysql`, `pgsql`, `mariadb`, `redis`, `memcached`, `meilisearch`, `typesense`, `minio`, `selenium`, and `mailpit`: -->
Sail 経由で新しい Laravel アプリケーションを作成する場合、`with` クエリ文字列変数を使用して、新しいアプリケーションの `docker-compose.yml` ファイルでどのサービスを構成するかを選択できます。利用可能なサービスには、`mysql`、`pgsql`、`mariadb`、`redis`、`memcached`、`meilisearch`、`typesense`、`minio`、`selenium`、および `mailpit` が含まれます。

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis" | bash
```

<!-- If you do not specify which services you would like configured, a default stack of `mysql`, `redis`, `meilisearch`, `mailpit`, and `selenium` will be configured. -->
設定するサービスを指定しない場合は、`mysql`、`redis`、`meilisearch`、`mailpit`、および `selenium` のデフォルト スタックが設定されます。

<!-- You may instruct Sail to install a default [Devcontainer](/docs/10.x/sail#using-devcontainers) by adding the `devcontainer` parameter to the URL: -->
URL に `devcontainer` パラメータを追加することで、デフォルトの [Devcontainer](/docs/10.x/sail#using-devcontainers) をインストールするように Sail に指示できます。

```shell
curl -s "https://laravel.build/example-app?with=mysql,redis&devcontainer" | bash
```

<a name="ide-support"></a>
<!-- ## IDE Support -->
## IDE Support

<!-- You are free to use any code editor you wish when developing Laravel applications; however, [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/) offers extensive support for Laravel and its ecosystem, including [Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html). -->
Laravel アプリケーションを開発する際には、任意のコード エディタを自由に使用できます。ただし、[PhpStorm](https://www.jetbrains.com/phpstorm/laravel/) は、[Laravel Pint](https://www.jetbrains.com/help/phpstorm/using-laravel-pint.html) を含む、Laravel とそのエコシステムに対する広範なサポートを提供します。

<!-- In addition, the community maintained [Laravel Idea](https://laravel-idea.com/) PhpStorm plugin offers a variety of helpful IDE augmentations, including code generation, Eloquent syntax completion, validation rule completion, and more. -->
さらに、コミュニティが管理する [Laravel Idea](https://laravel-idea.com/) PhpStorm プラグインは、コード生成、Eloquent 構文補完、検証ルール補完など、さまざまな便利な IDE 拡張機能を提供します。

<a name="laravel-and-ai"></a>
<!-- ## Laravel and AI -->
## Laravel and AI

<!-- [Laravel Boost](https://github.com/laravel/boost) is a powerful tool that bridges the gap between AI coding agents and Laravel applications. Boost provides AI agents with Laravel-specific context, tools, and guidelines so they can generate more accurate, version-specific code that follows Laravel conventions. -->
[Laravel Boost](https://github.com/laravel/boost) は、AI コーディング エージェントと Laravel アプリケーションの間のギャップを埋める強力なツールです。 Boost は、AI エージェントに Laravel 固有のコンテキスト、ツール、ガイドラインを提供するため、Laravel の規則に従って、より正確なバージョン固有のコードを生成できます。

<!-- When you install Boost in your Laravel application, AI agents gain access to over 15 specialized tools including the ability to know which packages you are using, query your database, search the Laravel documentation, read browser logs, generate tests, and execute code via Tinker. -->
Laravel アプリケーションに Boost をインストールすると、AI エージェントは、使用しているパッケージの把握、データベースのクエリ、Laravel ドキュメントの検索、ブラウザのログの読み取り、テストの生成、Tinker 経由のコードの実行など、15 を超える特殊なツールにアクセスできるようになります。

<!-- In addition, Boost gives AI agents access to over 17,000 pieces of vectorized Laravel ecosystem documentation, specific to your installed package versions. This means agents can provide guidance targeted to the exact versions your project uses. -->
さらに、Boost を使用すると、AI エージェントは、インストールされているパッケージのバージョンに応じて、17,000 を超えるベクトル化された Laravel エコシステム ドキュメントにアクセスできるようになります。これは、エージェントがプロジェクトで使用する正確なバージョンを対象としたガイダンスを提供できることを意味します。

<!-- Boost also includes Laravel-maintained AI guidelines that nudge agents to follow framework conventions, write appropriate tests, and avoid common pitfalls when generating Laravel code. -->
Boost には、エージェントがフレームワークの規則に従い、適切なテストを作成し、Laravel コード生成時によくある落とし穴を回避するように促す、Laravel が管理する AI ガイドラインも含まれています。

<a name="installing-laravel-boost"></a>
<!-- ### Installing Laravel Boost -->
### Installing Laravel Boost

<!-- Boost can be installed in Laravel 10, 11, and 12 applications running PHP 8.1 or higher. To get started, install Boost as a development dependency: -->
Boost は、PHP 8.1 以降を実行している Laravel 10、11、12 アプリケーションにインストールできます。まず、Boost を開発依存関係としてインストールします。

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

<a name="next-steps"></a>
<!-- ## Next Steps -->
## Next Steps

<!-- Now that you have created your Laravel project, you may be wondering what to learn next. First, we strongly recommend becoming familiar with how Laravel works by reading the following documentation: -->
Laravel プロジェクトを作成したので、次に何を学べばよいのか疑問に思っているかもしれません。まず、次のドキュメントを読んで、Laravel がどのように動作するかを理解することを強くお勧めします。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Request Lifecycle](/docs/10.x/lifecycle)
- [Configuration](/docs/10.x/configuration)
- [Directory Structure](/docs/10.x/structure)
- [Frontend](/docs/10.x/frontend)
- [Service Container](/docs/10.x/container)
- [Facades](/docs/10.x/facades)
-->
- [Request Lifecycle](/docs/10.x/lifecycle)
- [Configuration](/docs/10.x/configuration)
- [Directory Structure](/docs/10.x/structure)
- [Frontend](/docs/10.x/frontend)
- [Service Container](/docs/10.x/container)
- [Facades](/docs/10.x/facades)

<!-- </div> -->
</div>

<!-- How you want to use Laravel will also dictate the next steps on your journey. There are a variety of ways to use Laravel, and we'll explore two primary use cases for the framework below. -->
Laravel をどのように使用したいかによって、旅の次のステップも決まります。 Laravel を使用するにはさまざまな方法がありますが、以下ではフレームワークの 2 つの主な使用例を検討します。

> [!NOTE]
> Laravel は初めてですか?最初の Laravel アプリケーションを構築する手順を説明しながら、フレームワークの実践的なツアーについては、[Laravel Bootcamp](https://bootcamp.laravel.com) をご覧ください。

<a name="laravel-the-fullstack-framework"></a>
<!-- ### Laravel the Full Stack Framework -->
### Laravel the Full Stack Framework

<!-- Laravel may serve as a full stack framework. By "full stack" framework we mean that you are going to use Laravel to route requests to your application and render your frontend via [Blade templates](/docs/10.x/blade) or a single-page application hybrid technology like [Inertia](https://inertiajs.com). This is the most common way to use the Laravel framework, and, in our opinion, the most productive way to use Laravel. -->
Laravel はフルスタック フレームワークとして機能する可能性があります。 「フルスタック」フレームワークとは、Laravel を使用してリクエストをアプリケーションにルーティングし、[Blade templates](/docs/10.x/blade) または [Inertia](https://inertiajs.com) のような単一ページ アプリケーションのハイブリッド テクノロジを介してフロントエンドをレンダリングすることを意味します。これは、Laravel フレームワークを使用する最も一般的な方法であり、私たちの意見では、Laravel を使用する最も生産的な方法です。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [frontend development](/docs/10.x/frontend), [routing](/docs/10.x/routing), [views](/docs/10.x/views), or the [Eloquent ORM](/docs/10.x/eloquent). In addition, you might be interested in learning about community packages like [Livewire](https://livewire.laravel.com) and [Inertia](https://inertiajs.com). These packages allow you to use Laravel as a full-stack framework while enjoying many of the UI benefits provided by single-page JavaScript applications. -->
これが Laravel の使用方法である場合は、[frontend development](/docs/10.x/frontend)、[routing](/docs/10.x/routing)、[views](/docs/10.x/views)、または [Eloquent ORM](/docs/10.x/eloquent) に関するドキュメントを確認してください。さらに、[Livewire](https://livewire.laravel.com) や [Inertia](https://inertiajs.com) などのコミュニティ パッケージについても興味があるかもしれません。これらのパッケージを使用すると、シングルページ JavaScript アプリケーションによって提供される UI の利点の多くを享受しながら、Laravel をフルスタック フレームワークとして使用できるようになります。

<!-- If you are using Laravel as a full stack framework, we also strongly encourage you to learn how to compile your application's CSS and JavaScript using [Vite](/docs/10.x/vite). -->
Laravel をフルスタック フレームワークとして使用している場合は、[Vite](/docs/10.x/vite) を使用してアプリケーションの CSS と JavaScript をコンパイルする方法を学習することも強くお勧めします。

> [!NOTE]
> アプリケーションの構築をいち早く始めたい場合は、公式の [application starter kits](/docs/10.x/starter-kits) をチェックしてください。

<a name="laravel-the-api-backend"></a>
<!-- ### Laravel the API Backend -->
### Laravel the API Backend

<!-- Laravel may also serve as an API backend to a JavaScript single-page application or mobile application. For example, you might use Laravel as an API backend for your [Next.js](https://nextjs.org) application. In this context, you may use Laravel to provide [authentication](/docs/10.x/sanctum) and data storage / retrieval for your application, while also taking advantage of Laravel's powerful services such as queues, emails, notifications, and more. -->
Laravel は、JavaScript シングルページ アプリケーションまたはモバイル アプリケーションへの API バックエンドとしても機能します。たとえば、[Next.js](https://nextjs.org) アプリケーションの API バックエンドとして Laravel を使用することができます。このコンテキストでは、Laravel を使用してアプリケーションに [authentication](/docs/10.x/sanctum) とデータ ストレージ/取得を提供すると同時に、キュー、電子メール、通知などの Laravel の強力なサービスも利用できます。

<!-- If this is how you plan to use Laravel, you may want to check out our documentation on [routing](/docs/10.x/routing), [Laravel Sanctum](/docs/10.x/sanctum), and the [Eloquent ORM](/docs/10.x/eloquent). -->
これが Laravel の使用方法である場合は、[routing](/docs/10.x/routing)、[Laravel Sanctum](/docs/10.x/sanctum)、および [Eloquent ORM](/docs/10.x/eloquent) に関するドキュメントを確認してください。

> [!NOTE]
> Laravel バックエンドと Next.js フロントエンドのスキャフォールディングをいち早く始める必要がありますか? Laravel Breeze は [API stack](/docs/10.x/starter-kits#breeze-and-next) だけでなく [Next.js frontend implementation](https://github.com/laravel/breeze-next) も提供しているので、数分で開始できます。

