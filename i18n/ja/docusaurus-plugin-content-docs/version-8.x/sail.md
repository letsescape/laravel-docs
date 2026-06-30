<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation & Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Configuring A Bash Alias](#configuring-a-bash-alias)
- [Starting & Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [MeiliSearch](#meilisearch)
- [File Storage](#file-storage)
- [Running Tests](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
- [Node Versions](#sail-node-versions)
- [Sharing Your Site](#sharing-your-site)
- [Debugging With Xdebug](#debugging-with-xdebug)
  - [Xdebug CLI Usage](#xdebug-cli-usage)
  - [Xdebug Browser Usage](#xdebug-browser-usage)
- [Customization](#sail-customization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Sail](https://github.com/laravel/sail) is a light-weight command-line interface for interacting with Laravel's default Docker development environment. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
[Laravel Sail](https://github.com/laravel/sail) は、Laravel のデフォルトの Docker 開発環境と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

<!-- At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file. -->
Sail の中心となるのは、プロジェクトのルートに保存されている `docker-compose.yml` ファイルと `sail` スクリプトです。 `sail` スクリプトは、`docker-compose.yml` ファイルで定義された Docker コンテナーと対話するための便利なメソッドを備えた CLI を提供します。

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail は、macOS、Linux、Windows ([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 経由) でサポートされています。

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<!-- Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/8.x/installation) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with. -->
Laravel Sail はすべての新しい Laravel アプリケーションとともに自動的にインストールされるため、すぐに使用を開始できます。新しい Laravel アプリケーションの作成方法については、お使いのオペレーティング システム用の Laravel の [installation documentation](/docs/8.x/installation) を参照してください。インストール中に、アプリケーションが対話する Sail 対応サービスを選択するよう求められます。

<a name="installing-sail-into-existing-applications"></a>
<!-- ### Installing Sail Into Existing Applications -->
### Installing Sail Into Existing Applications

<!-- If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies: -->
既存の Laravel アプリケーションで Sail を使用することに興味がある場合は、Composer パッケージ マネージャーを使用して Sail をインストールするだけです。もちろん、これらの手順は、既存のローカル開発環境で Composer の依存関係をインストールできることを前提としています。

```
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application: -->
Sail がインストールされたら、`sail:install` Artisan コマンドを実行できます。このコマンドは、Sail の `docker-compose.yml` ファイルをアプリケーションのルートに公開します。

```
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
最後に、Sail を開始できます。 Sail の使用方法を学習し続けるには、このドキュメントの残りの部分を読み続けてください。

<!--     ./vendor/bin/sail up -->
    ./vendor/bin/sail up

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 内で開発したい場合は、`sail:install` コマンドに `--devcontainer` オプションを指定できます。 `--devcontainer` オプションは、デフォルトの `.devcontainer/devcontainer.json ` ファイルをアプリケーションのルートに公開するように `sail:install` コマンドに指示します。

```
php artisan sail:install --devcontainer
```

<a name="configuring-a-bash-alias"></a>
<!-- ### Configuring A Bash Alias -->
### Configuring A Bash Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
デフォルトでは、Sail コマンドは、すべての新しい Laravel アプリケーションに含まれる `vendor/bin/sail` スクリプトを使用して呼び出されます。

```bash
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a Bash alias that allows you to execute Sail's commands more easily: -->
ただし、`vendor/bin/sail` を繰り返し入力して Sail コマンドを実行する代わりに、Sail のコマンドをより簡単に実行できる Bash エイリアスを構成することもできます。

```bash
alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'
```

<!-- Once the Bash alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
Bash エイリアスが設定されたら、「`sail`」と入力するだけで Sail コマンドを実行できます。このドキュメントの残りの例では、このエイリアスが設定されていることを前提としています。

```bash
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting & Stopping Sail -->
## Starting & Stopping Sail

<!-- Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail の `docker-compose.yml` ファイルは、Laravel アプリケーションの構築を支援するために連携して動作するさまざまな Docker コンテナを定義します。これらの各コンテナーは、`docker-compose.yml` ファイルの `services` 構成内のエントリです。 `laravel.test` コンテナーは、アプリケーションを提供するプライマリ アプリケーション コンテナーです。

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command: -->
Sail を開始する前に、ローカル コンピューター上で他の Web サーバーやデータベースが実行されていないことを確認する必要があります。アプリケーションの `docker-compose.yml` ファイルで定義されているすべての Docker コンテナを起動するには、`up` コマンドを実行する必要があります。

```bash
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
すべての Docker コンテナをバックグラウンドで起動するには、Sail を「デタッチ」モードで起動します。

```bash
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
アプリケーションのコンテナが開始されたら、Web ブラウザで http://localhost. にあるプロジェクトにアクセスできます。

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
すべてのコンテナを停止するには、Ctrl + C を押してコンテナの実行を停止します。または、コンテナーがバックグラウンドで実行されている場合は、`stop` コマンドを使用できます。

```bash
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail を使用する場合、アプリケーションは Docker コンテナ内で実行され、ローカル コンピューターから分離されます。ただし、Sail は、任意の PHP コマンド、Artisan コマンド、Composer コマンド、Node / NPM コマンドなど、アプリケーションに対してさまざまなコマンドを実行する便利な方法を提供します。

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel ドキュメントを読むと、Sail を参照していない Composer、Artisan、および Node / NPM コマンドへの参照が頻繁に表示されます。** これらの例では、これらのツールがローカル コンピューターにインストールされていることを前提としています。ローカルの Laravel 開発環境に Sail を使用している場合は、Sail を使用してこれらのコマンドを実行する必要があります。

```bash
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
<!-- ### Executing PHP Commands -->
### Executing PHP Commands

<!-- PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions): -->
PHP コマンドは、`php` コマンドを使用して実行できます。もちろん、これらのコマンドは、アプリケーション用に構成された PHP バージョンを使用して実行されます。 Laravel Sail で利用可能な PHP バージョンの詳細については、[PHP version documentation](#sail-php-versions) を参照してください。

```bash
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer 2.x installation: -->
Composer コマンドは、`composer` コマンドを使用して実行できます。 Laravel Sail のアプリケーションコンテナには Composer 2.x インストールが含まれています。

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
<!-- #### Installing Composer Dependencies For Existing Applications -->
#### Installing Composer Dependencies For Existing Applications

<!-- If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer. -->
チームでアプリケーションを開発している場合、最初に Laravel アプリケーションを作成するのは自分ではない可能性があります。したがって、アプリケーションのリポジトリをローカル コンピュータに複製した後は、Sail を含むアプリケーションの Composer 依存関係はインストールされません。

<!-- You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies: -->
アプリケーションのディレクトリに移動し、次のコマンドを実行することで、アプリケーションの依存関係をインストールできます。このコマンドは、PHP と Composer を含む小さな Docker コンテナを使用して、アプリケーションの依存関係をインストールします。

```nothing
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v $(pwd):/var/www/html \
    -w /var/www/html \
    laravelsail/php81-composer:latest \
    composer install --ignore-platform-reqs
```

<!-- When using the `laravelsail/phpXX-composer` image, you should use the same version of PHP that you plan to use for your application (`74`, `80`, or `81`). -->
`laravelsail/phpXX-composer` イメージを使用する場合は、アプリケーションに使用する予定と同じバージョンの PHP を使用する必要があります (`74`、`80`、または `81`)。

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel Artisan コマンドは、`artisan` コマンドを使用して実行できます。

```bash
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
ノード コマンドは `node` コマンドを使用して実行でき、NPM コマンドは `npm` コマンドを使用して実行できます。

```nothing
sail node --version

sail npm run prod
```

<!-- If you wish, you may use Yarn instead of NPM: -->
必要に応じて、NPM の代わりに Yarn を使用することもできます。

```nothing
sail yarn
```

<a name="interacting-with-sail-databases"></a>
<!-- ## Interacting With Databases -->
## Interacting With Databases

<a name="mysql"></a>
<!-- ### MySQL -->
### MySQL

<!-- As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. In addition, when the MySQL container is starting, it will ensure a database exists whose name matches the value of your `DB_DATABASE` environment variable. -->
お気づきかもしれませんが、アプリケーションの `docker-compose.yml` ファイルには、MySQL コンテナのエントリが含まれています。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、データベースに保存されているデータは保持されます。さらに、MySQL コンテナの起動時に、`DB_DATABASE` 環境変数の値と名前が一致するデータベースが存在することが確認されます。

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
コンテナーを起動したら、アプリケーションの `.env` ファイル内の `DB_HOST` 環境変数を `mysql` に設定することで、アプリケーション内の MySQL インスタンスに接続できます。

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306. -->
ローカル マシンからアプリケーションの MySQL データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、MySQL データベースは `localhost` ポート 3306 でアクセスできます。

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
アプリケーションの `docker-compose.yml` ファイルには、[Redis](https://redis.io) コンテナーのエントリも含まれています。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、Redis データに保存されたデータは保持されます。コンテナーを起動したら、アプリケーションの `.env` ファイル内の `REDIS_HOST` 環境変数を `redis` に設定することで、アプリケーション内の Redis インスタンスに接続できます。

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
ローカル マシンからアプリケーションの Redis データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、Redis データベースは `localhost` ポート 6379 でアクセスできます。

<a name="meilisearch"></a>
<!-- ### MeiliSearch -->
### MeiliSearch

<!-- If you chose to install the [MeiliSearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search-engine that is [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) with [Laravel Scout](/docs/8.x/scout). Once you have started your containers, you may connect to the MeiliSearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail のインストール時に [MeiliSearch](https://www.meilisearch.com) サービスのインストールを選択した場合、アプリケーションの `docker-compose.yml` ファイルには、この強力な検索エンジンのエントリ ([compatible](https://github.com/meilisearch/meilisearch-laravel-scout) と [Laravel Scout](/docs/8.x/scout)) が含まれます。コンテナーを起動したら、`MEILISEARCH_HOST` 環境変数を `http://meilisearch:7700` に設定することで、アプリケーション内の Meil​​iSearch インスタンスに接続できます。

<!-- From your local machine, you may access MeiliSearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
ローカル マシンから、Web ブラウザで `http://localhost:7700` に移動して、MeiliSearch の Web ベースの管理パネルにアクセスできます。

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file. -->
本番環境でアプリケーションを実行しているときに Amazon S3 を使用してファイルを保存する予定がある場合は、Sail のインストール時に [MinIO](https://min.io) サービスをインストールすることをお勧めします。 MinIO は、運用 S3 環境で「テスト」ストレージ バケットを作成せずに、Laravel の `s3` ファイルストレージ ドライバを使用してローカルで開発するために使用できる S3 互換 API を提供します。 Sail のインストール中に MinIO のインストールを選択した場合、MinIO 構成セクションがアプリケーションの `docker-compose.yml` ファイルに追加されます。

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows: -->
デフォルトでは、アプリケーションの `filesystems` 構成ファイルには、`s3` ディスクのディスク構成がすでに含まれています。このディスクを使用して Amazon S3 と対話するだけでなく、構成を制御する関連する環境変数を変更するだけで、MinIO などの S3 互換ファイルストレージ サービスと対話するためにディスクを使用することもできます。たとえば、MinIO を使用する場合、ファイルシステムの環境変数構成を次のように定義する必要があります。

```ini
FILESYSTEM_DRIVER=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/8.x/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command: -->
Laravel はすぐに使える素晴らしいテストサポートを提供しており、Sail の `test` コマンドを使用してアプリケーション [feature and unit tests](/docs/8.x/testing) を実行できます。 PHPUnit によって受け入れられる CLI オプションはすべて、`test` コマンドに渡すこともできます。

<!--     sail test -->
    sail test

<!--     sail test --group orders -->
    sail test --group orders

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail `test` コマンドは、`test` Artisan コマンドの実行と同等です。

<!--     sail artisan test -->
    sail artisan test

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/8.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file: -->
[Laravel Dusk](/docs/8.x/dusk) は、表現力豊かで使いやすいブラウザ自動化およびテスト API を提供します。 Sail のおかげで、Selenium やその他のツールをローカル コンピューターにインストールしなくても、これらのテストを実行できます。まず、アプリケーションの `docker-compose.yml` ファイル内の Selenium サービスのコメントを解除します。

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<!-- Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`: -->
次に、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービスに、`selenium` の `depends_on` エントリがあることを確認します。

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
最後に、Sail を起動して `dusk` コマンドを実行することで、Dusk テスト スイートを実行できます。

<!--     sail dusk -->
    sail dusk

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium On Apple Silicon -->
#### Selenium On Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `seleniarm/standalone-chromium` image: -->
ローカル マシンに Apple Silicon チップが含まれている場合、`selenium` サービスは `seleniarm/standalone-chromium` イメージを使用する必要があります。

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `docker-compose.yml` file contains a service entry for [MailHog](https://github.com/mailhog/MailHog). MailHog intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, MailHog's default host is `mailhog` and is available via port 1025: -->
Laravel Sail のデフォルトの `docker-compose.yml` ファイルには、[MailHog](https://github.com/mailhog/MailHog) のサービスエントリが含まれています。 MailHog は、ローカル開発中にアプリケーションによって送信された電子メールをインターセプトし、ブラウザで電子メール メッセージをプレビューできる便利な Web インターフェイスを提供します。 Sail を使用する場合、MailHog のデフォルトのホストは `mailhog` で、ポート 1025 経由で利用できます。

```bash
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the MailHog web interface at: http://localhost:8025 -->
Sail の実行中は、http://localhost:8025 で MailHog Web インターフェイスにアクセスできます。

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well execute arbitrary shell commands within the container: -->
場合によっては、アプリケーションのコンテナ内で Bash セッションを開始したい場合があります。 `shell` コマンドを使用してアプリケーションのコンテナに接続すると、そのファイルやインストールされているサービスを検査したり、コンテナ内で任意のシェル コマンドを実行したりできます。

```nothing
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
新しい [Laravel Tinker](https://github.com/laravel/tinker) セッションを開始するには、`tinker` コマンドを実行します。

```bash
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.1, PHP 8.0, or PHP 7.4. The default PHP version used by Sail is currently PHP 8.1. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file: -->
Sail は現在、PHP 8.1、PHP 8.0、または PHP 7.4 を介したアプリケーションの提供をサポートしています。 Sail で使用されるデフォルトの PHP バージョンは現在 PHP 8.1 です。アプリケーションの提供に使用される PHP バージョンを変更するには、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` コンテナの `build` 定義を更新する必要があります。

```yaml
# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file: -->
さらに、アプリケーションで使用されている PHP のバージョンを反映するように、`image` 名を更新することもできます。このオプションは、アプリケーションの `docker-compose.yml` ファイルでも定義されます。

```yaml
image: sail-8.1/app
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
アプリケーションの `docker-compose.yml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

<!--     sail build --no-cache -->
    sail build --no-cache

<!--     sail up -->
    sail up

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 16 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file: -->
Sail はデフォルトで Node 16 をインストールします。イメージのビルド時にインストールされるノードのバージョンを変更するには、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービスの `build.args` 定義を更新します。

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
アプリケーションの `docker-compose.yml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

<!--     sail build --no-cache -->
    sail build --no-cache

<!--     sail up -->
    sail up

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
場合によっては、同僚にサイトをプレビューしたり、アプリケーションとの Webhook 統合をテストしたりするために、サイトをパブリックに共有する必要がある場合があります。サイトを共有するには、`share` コマンドを使用できます。このコマンドを実行すると、アプリケーションへのアクセスに使用できるランダムな `laravel-sail.site` URL が発行されます。

<!--     sail share -->
    sail share

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies within the `TrustProxies` middleware. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` コマンドを使用してサイトを共有する場合は、`TrustProxies` ミドルウェア内でアプリケーションの信頼できるプロキシを構成する必要があります。そうしないと、`url` や `route` などの URL生成ヘルパは、URL生成中に使用する必要がある正しい HTTP ホストを決定できなくなります。

```
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
共有サイトのサブドメインを選択したい場合は、`share` コマンドを実行するときに `subdomain` オプションを指定できます。

<!--     sail share --subdomain=my-sail-site -->
    sail share --subdomain=my-sail-site

> [!TIP]
> `share` コマンドは、[Expose](https://github.com/beyondcode/expose)（[BeyondCode](https://beyondco.de) によるオープンソース トンネリング サービス）を利用しています。

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. In order to enable Xdebug, you will need to add a few variables to your application's `.env` file to [configure Xdebug](https://xdebug.org/docs/step_debug#mode). To enable Xdebug you must set the appropriate mode(s) before starting Sail: -->
Laravel Sail の Docker 構成には、PHP 用の人気のある強力なデバッガーである [Xdebug](https://xdebug.org/) のサポートが含まれています。 Xdebug を有効にするには、アプリケーションの `.env` ファイルから [configure Xdebug](https://xdebug.org/docs/step_debug#mode) にいくつかの変数を追加する必要があります。 Xdebug を有効にするには、Sail を開始する前に適切なモードを設定する必要があります。

```ini
SAIL_XDEBUG_MODE=develop,debug
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux, you will need to manually define this environment variable. -->
内部的には、`XDEBUG_CONFIG` 環境変数は `client_host=host.docker.internal` として定義されているため、Xdebug は Mac および Windows (WSL2) に対して適切に構成されます。ローカル マシンが Linux を実行している場合は、この環境変数を手動で定義する必要があります。

<!-- First, you should determine the correct host IP address to add to the environment variable by running the following command. Typically, the `<container-name>` should be the name of the container that serves your application and often ends with `_laravel.test_1`: -->
まず、次のコマンドを実行して、環境変数に追加する正しいホスト IP アドレスを決定する必要があります。通常、`<container-name>` はアプリケーションを提供するコンテナーの名前である必要があり、多くの場合 `_laravel.test_1` で終わります。

```bash
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

<!-- Once you have obtained the correct host IP address, you should define the `SAIL_XDEBUG_CONFIG` variable within your application's `.env` file: -->
正しいホスト IP アドレスを取得したら、アプリケーションの `.env` ファイル内で `SAIL_XDEBUG_CONFIG` 変数を定義する必要があります。

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
Artisan コマンドの実行時に、`sail debug` コマンドを使用してデバッグ セッションを開始できます。

```bash
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
<!-- ### Xdebug Browser Usage -->
### Xdebug Browser Usage

<!-- To debug your application while interacting with the application via a web browser, follow the [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) for initiating an Xdebug session from the web browser. -->
Web ブラウザ経由でアプリケーションと対話しながらアプリケーションをデバッグするには、[instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) に従って Web ブラウザから Xdebug セッションを開始します。

<!-- If you're using PhpStorm, please review JetBrain's documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm を使用している場合は、[zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) に関する JetBrain のドキュメントを確認してください。

> [!NOTE]
> Laravel Sail は、アプリケーションを提供するために `artisan serve` に依存しています。 Laravel バージョン 8.53.0 では、`artisan serve` コマンドは `XDEBUG_CONFIG` 変数と `XDEBUG_MODE` 変数のみを受け入れます。 Laravel の古いバージョン (8.52.0 以下) はこれらの変数をサポートしておらず、デバッグ接続を受け入れません。

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail は単なる Docker であるため、Sail に関するほぼすべてを自由にカスタマイズできます。 Sail 独自の Dockerfile を公開するには、`sail:publish` コマンドを実行します。

```bash
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
このコマンドを実行すると、Laravel Sail で使用される Dockerfile およびその他の構成ファイルが、アプリケーションのルート ディレクトリの `docker` ディレクトリ内に配置されます。 Sail インストールをカスタマイズした後、アプリケーションの `docker-compose.yml` ファイル内のアプリケーション コンテナーのイメージ名を変更することができます。その後、`build` コマンドを使用してアプリケーションのコンテナを再構築します。 Sail を使用して単一マシン上で複数の Laravel アプリケーションを開発している場合、アプリケーション イメージに一意の名前を割り当てることが特に重要です。

```bash
sail build --no-cache
```

