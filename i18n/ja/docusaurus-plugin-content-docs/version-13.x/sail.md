<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
    - [Rebuilding Sail Images](#rebuilding-sail-images)
    - [Configuring A Shell Alias](#configuring-a-shell-alias)
- [Starting and Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [File Storage](#file-storage)
- [Running Tests](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
    - [Additional PHP Extensions](#sail-php-extensions)
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

<!-- At its heart, Sail is the `compose.yaml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `compose.yaml` file. -->
Sail の中心となるのは、プロジェクトのルートに保存されている `compose.yaml` ファイルと `sail` スクリプトです。 `sail` スクリプトは、`compose.yaml` ファイルで定義された Docker コンテナーと対話するための便利なメソッドを備えた CLI を提供します。

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail は、macOS、Linux、Windows ([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 経由) でサポートされています。

<a name="installation"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<!-- You may install Sail using the Composer package manager: -->
Composer パッケージ マネージャーを使用して Sail をインストールできます。

```shell
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `compose.yaml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services: -->
Sail がインストールされたら、`sail:install` Artisan コマンドを実行できます。このコマンドは、Sail の `compose.yaml` ファイルをアプリケーションのルートに公開し、Docker サービスに接続するために必要な環境変数を使用して `.env` ファイルを変更します。

```shell
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
最後に、Sail を開始できます。 Sail の使用方法を学習し続けるには、このドキュメントの残りの部分を読み続けてください。

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux 用の Docker デスクトップを使用している場合は、コマンド `docker context use default` を実行して、`default` Docker コンテキストを使用する必要があります。さらに、コンテナ内でファイル権限エラーが発生した場合は、`SUPERVISOR_PHP_USER` 環境変数を `root` に設定する必要がある場合があります。

<a name="adding-additional-services"></a>
<!-- #### Adding Additional Services -->
#### Adding Additional Services

<!-- If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command: -->
既存の Sail インストールに追加サービスを追加したい場合は、`sail:add` Artisan コマンドを実行できます。

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 内で開発したい場合は、`sail:install` コマンドに `--devcontainer` オプションを指定できます。 `--devcontainer` オプションは、デフォルトの `.devcontainer/devcontainer.json ` ファイルをアプリケーションのルートに公開するように `sail:install` コマンドに指示します。

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
<!-- ### Rebuilding Sail Images -->
### Rebuilding Sail Images

<!-- Sometimes you may want to completely rebuild your Sail images to ensure all of the image's packages and software are up to date. You may accomplish this using the `build` command: -->
場合によっては、Sail イメージを完全に再構築して、イメージのすべてのパッケージとソフトウェアを最新の状態にしたい場合があります。これは、`build` コマンドを使用して実行できます。

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
<!-- ### Configuring A Shell Alias -->
### Configuring A Shell Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
デフォルトでは、Sail コマンドは、すべての新しい Laravel アプリケーションに含まれる `vendor/bin/sail` スクリプトを使用して呼び出されます。

```shell
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily: -->
ただし、`vendor/bin/sail` を繰り返し入力して Sail コマンドを実行する代わりに、Sail のコマンドをより簡単に実行できるシェル エイリアスを構成することもできます。

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

<!-- To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell. -->
これを常に利用できるようにするには、これをホーム ディレクトリのシェル構成ファイル (`~/.zshrc` や `~/.bashrc` など) に追加し、シェルを再起動します。

<!-- Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
シェル エイリアスが設定されたら、「`sail`」と入力するだけで Sail コマンドを実行できます。このドキュメントの残りの例では、このエイリアスが設定されていることを前提としています。

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting and Stopping Sail -->
## Starting and Stopping Sail

<!-- Laravel Sail's `compose.yaml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `compose.yaml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail の `compose.yaml` ファイルは、Laravel アプリケーションの構築を支援するために連携して動作するさまざまな Docker コンテナを定義します。これらの各コンテナーは、`compose.yaml` ファイルの `services` 構成内のエントリです。 `laravel.test` コンテナーは、アプリケーションを提供するプライマリ アプリケーション コンテナーです。

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `compose.yaml` file, you should execute the `up` command: -->
Sail を開始する前に、ローカル コンピューター上で他の Web サーバーやデータベースが実行されていないことを確認する必要があります。アプリケーションの `compose.yaml` ファイルで定義されているすべての Docker コンテナを起動するには、`up` コマンドを実行する必要があります。

```shell
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
すべての Docker コンテナをバックグラウンドで起動するには、Sail を「デタッチ」モードで起動します。

```shell
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
アプリケーションのコンテナが開始されたら、Web ブラウザで http://localhost. にあるプロジェクトにアクセスできます。

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
すべてのコンテナを停止するには、Ctrl + C を押してコンテナの実行を停止します。または、コンテナーがバックグラウンドで実行されている場合は、`stop` コマンドを使用できます。

```shell
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail を使用する場合、アプリケーションは Docker コンテナ内で実行され、ローカル コンピューターから分離されます。ただし、Sail は、任意の PHP コマンド、Artisan コマンド、Composer コマンド、Node / NPM コマンドなど、アプリケーションに対してさまざまなコマンドを実行する便利な方法を提供します。

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel ドキュメントを読むと、Sail を参照していない Composer、Artisan、および Node / NPM コマンドへの参照が頻繁に表示されます。** これらの例では、これらのツールがローカル コンピューターにインストールされていることを前提としています。ローカルの Laravel 開発環境に Sail を使用している場合は、Sail を使用してこれらのコマンドを実行する必要があります。

```shell
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

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer installation: -->
Composer コマンドは、`composer` コマンドを使用して実行できます。 Laravel Sail のアプリケーションコンテナには Composer インストールが含まれています。

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel Artisan コマンドは、`artisan` コマンドを使用して実行できます。

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
ノード コマンドは `node` コマンドを使用して実行でき、NPM コマンドは `npm` コマンドを使用して実行できます。

```shell
sail node --version

sail npm run dev
```

<!-- If you wish, you may use Yarn instead of NPM: -->
必要に応じて、NPM の代わりに Yarn を使用することもできます。

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
<!-- ## Interacting With Databases -->
## Interacting With Databases

<a name="mysql"></a>
<!-- ### MySQL -->
### MySQL

<!-- As you may have noticed, your application's `compose.yaml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
お気づきかもしれませんが、アプリケーションの `compose.yaml` ファイルには、MySQL コンテナのエントリが含まれています。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、データベースに保存されているデータは保持されます。

<!-- In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data. -->
さらに、MySQL コンテナを初めて起動すると、2 つのデータベースが作成されます。最初のデータベースは、`DB_DATABASE` 環境変数の値を使用して名前が付けられ、ローカル開発用です。 2 つ目は、`testing` という名前の専用のテスト データベースで、テストが開発データに干渉しないことを保証します。

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
コンテナーを起動したら、アプリケーションの `.env` ファイル内の `DB_HOST` 環境変数を `mysql` に設定することで、アプリケーション内の MySQL インスタンスに接続できます。

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password. -->
ローカル マシンからアプリケーションの MySQL データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、MySQL データベースは `localhost` ポート 3306 でアクセスでき、アクセス資格情報は `DB_USERNAME` および `DB_PASSWORD` 環境変数の値に対応します。または、`root` ユーザーとして接続することもできます。この場合も、`DB_PASSWORD` 環境変数の値がパスワードとして使用されます。

<a name="mongodb"></a>
<!-- ### MongoDB -->
### MongoDB

<!-- If you chose to install the [MongoDB](https://www.mongodb.com/) service when installing Sail, your application's `compose.yaml` file contains an entry for a [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) container which provides the MongoDB document database with Atlas features like [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
Sail のインストール時に [MongoDB](https://www.mongodb.com/) サービスのインストールを選択した場合、アプリケーションの `compose.yaml` ファイルには、[MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) コンテナのエントリが含まれています。このコンテナは、[Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) などの Atlas 機能を備えた MongoDB ドキュメント データベースを提供します。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、データベースに保存されているデータは保持されます。

<!-- Once you have started your containers, you may connect to the MongoDB instance within your application by setting your `MONGODB_URI` environment variable within your application's `.env` file to `mongodb://mongodb:27017`. Authentication is disabled by default, but you can set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables to enable authentication before starting the `mongodb` container. Then, add the credentials to the connection string: -->
コンテナーを起動したら、アプリケーションの `.env` ファイル内の `MONGODB_URI` 環境変数を `mongodb://mongodb:27017` に設定することで、アプリケーション内の MongoDB インスタンスに接続できます。認証はデフォルトでは無効になっていますが、`mongodb` コンテナーを開始する前に、`MONGODB_USERNAME` および `MONGODB_PASSWORD` 環境変数を設定して認証を有効にすることができます。次に、資格情報を接続文字列に追加します。

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

<!-- For seamless integration of MongoDB with your application, you can install the [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/). -->
MongoDB をアプリケーションとシームレスに統合するには、[official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) をインストールします。

<!-- To connect to your application's MongoDB database from your local machine, you may use a graphical interface such as [Compass](https://www.mongodb.com/products/tools/compass). By default, the MongoDB database is accessible at `localhost` port `27017`. -->
ローカル マシンからアプリケーションの MongoDB データベースに接続するには、[Compass](https://www.mongodb.com/products/tools/compass) などのグラフィカル インターフェイスを使用できます。デフォルトでは、MongoDB データベースは `localhost` ポート `27017` でアクセスできます。

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `compose.yaml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis instance is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
アプリケーションの `compose.yaml` ファイルには、[Redis](https://redis.io) コンテナーのエントリも含まれています。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、Redis インスタンスに保存されたデータは保持されます。コンテナーを起動したら、アプリケーションの `.env` ファイル内の `REDIS_HOST` 環境変数を `redis` に設定することで、アプリケーション内の Redis インスタンスに接続できます。

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
ローカル マシンからアプリケーションの Redis データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、Redis データベースは `localhost` ポート 6379 でアクセスできます。

<a name="valkey"></a>
<!-- ### Valkey -->
### Valkey

<!-- If you choose to install Valkey service when installing Sail, your application's `compose.yaml` file will contain an entry for [Valkey](https://valkey.io/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Valkey instance is persisted even when stopping and restarting your containers. You can connect to this container in your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `valkey`. -->
Sail のインストール時に Valkey サービスのインストールを選択した場合、アプリケーションの `compose.yaml` ファイルには、[Valkey](https://valkey.io/) のエントリが含まれます。このコンテナーは [Docker volume](https://docs.docker.com/storage/volumes/) を使用するため、Valkey インスタンスに保存されているデータは、コンテナーを停止および再起動しても保持されます。アプリケーションの `.env` ファイル内の `REDIS_HOST` 環境変数を `valkey` に設定することで、アプリケーションでこのコンテナに接続できます。

<!-- To connect to your application's Valkey database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Valkey database is accessible at `localhost` port 6379. -->
ローカル マシンからアプリケーションの Valkey データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、Valkey データベースは `localhost` ポート 6379 でアクセスできます。

<a name="meilisearch"></a>
<!-- ### Meilisearch -->
### Meilisearch

<!-- If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `compose.yaml` file will contain an entry for this powerful search engine that is integrated with [Laravel Scout](/docs/13.x/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail のインストール時に [Meilisearch](https://www.meilisearch.com) サービスのインストールを選択した場合、アプリケーションの `compose.yaml` ファイルには、[Laravel Scout](/docs/13.x/scout) と統合されたこの強力な検索エンジンのエントリが含まれます。コンテナーを起動したら、`MEILISEARCH_HOST` 環境変数を `http://meilisearch:7700` に設定することで、アプリケーション内の Meil​​isearch インスタンスに接続できます。

<!-- From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
ローカル マシンから、Web ブラウザで `http://localhost:7700` に移動して、Meilisearch の Web ベースの管理パネルにアクセスできます。

<a name="typesense"></a>
<!-- ### Typesense -->
### Typesense

<!-- If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `compose.yaml` file will contain an entry for this lightning fast, open-source search engine that is natively integrated with [Laravel Scout](/docs/13.x/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables: -->
Sail のインストール時に [Typesense](https://typesense.org) サービスのインストールを選択した場合、アプリケーションの `compose.yaml` ファイルには、[Laravel Scout](/docs/13.x/scout#typesense) とネイティブに統合されたこの超高速のオープンソース検索エンジンのエントリが含まれます。コンテナーを起動したら、次の環境変数を設定して、アプリケーション内の Typesense インスタンスに接続できます。

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

<!-- From your local machine, you may access Typesense's API via `http://localhost:8108`. -->
ローカル マシンから、`http://localhost:8108` 経由で Typesense の API にアクセスできます。

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [RustFS](https://rustfs.com) service when installing Sail. RustFS provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install RustFS while installing Sail, a RustFS configuration section will be added to your application's `compose.yaml` file. -->
本番環境でアプリケーションを実行しているときに Amazon S3 を使用してファイルを保存する予定がある場合は、Sail のインストール時に [RustFS](https://rustfs.com) サービスをインストールすることをお勧めします。 RustFS は、運用 S3 環境で「テスト」ストレージ バケットを作成せずに、Laravel の `s3` ファイルストレージ ドライバを使用してローカルで開発するために使用できる S3 互換 API を提供します。 Sail のインストール中に RustFS のインストールを選択した場合、RustFS 構成セクションがアプリケーションの `compose.yaml` ファイルに追加されます。

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as RustFS by simply modifying the associated environment variables that control its configuration. For example, when using RustFS, your filesystem environment variable configuration should be defined as follows: -->
デフォルトでは、アプリケーションの `filesystems` 構成ファイルには、`s3` ディスクのディスク構成がすでに含まれています。このディスクを使用して Amazon S3 と対話するだけでなく、構成を制御する関連する環境変数を変更するだけで、RustFS などの S3 互換ファイルストレージ サービスと対話するために使用することもできます。たとえば、RustFS を使用する場合、ファイルシステムの環境変数設定を次のように定義する必要があります。

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/13.x/testing). Any CLI options that are accepted by Pest / PHPUnit may also be passed to the `test` command: -->
Laravel はすぐに使える素晴らしいテストサポートを提供しており、Sail の `test` コマンドを使用してアプリケーション [feature and unit tests](/docs/13.x/testing) を実行できます。 Pest / PHPUnit によって受け入れられる CLI オプションはすべて、`test` コマンドに渡すこともできます。

```shell
sail test

sail test --group orders
```

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail `test` コマンドは、`test` Artisan コマンドの実行と同等です。

```shell
sail artisan test
```

<!-- By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests: -->
デフォルトでは、Sail は専用の `testing` データベースを作成し、テストがデータベースの現在の状態に干渉しないようにします。デフォルトの Laravel インストールでは、Sail はテストの実行時にこのデータベースを使用するように `phpunit.xml` ファイルも設定します。

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/13.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `compose.yaml` file: -->
[Laravel Dusk](/docs/13.x/dusk) は、表現力豊かで使いやすいブラウザ自動化およびテスト API を提供します。 Sail のおかげで、Selenium やその他のツールをローカル コンピューターにインストールしなくても、これらのテストを実行できます。まず、アプリケーションの `compose.yaml` ファイル内の Selenium サービスのコメントを解除します。

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<!-- Next, ensure that the `laravel.test` service in your application's `compose.yaml` file has a `depends_on` entry for `selenium`: -->
次に、アプリケーションの `compose.yaml` ファイル内の `laravel.test` サービスに、`selenium` の `depends_on` エントリがあることを確認します。

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
最後に、Sail を起動して `dusk` コマンドを実行することで、Dusk テスト スイートを実行できます。

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium on Apple Silicon -->
#### Selenium on Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `selenium/standalone-chromium` image: -->
ローカル マシンに Apple Silicon チップが含まれている場合、`selenium` サービスは `selenium/standalone-chromium` イメージを使用する必要があります。

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `compose.yaml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025: -->
Laravel Sail のデフォルトの `compose.yaml` ファイルには、[Mailpit](https://github.com/axllent/mailpit) のサービスエントリが含まれています。 Mailpit は、ローカル開発中にアプリケーションによって送信された電子メールをインターセプトし、ブラウザで電子メール メッセージをプレビューできる便利な Web インターフェイスを提供します。 Sail を使用する場合、Mailpit のデフォルトのホストは `mailpit` で、ポート 1025 経由で利用できます。

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the Mailpit web interface at: http://localhost:8025 -->
Sail の実行中は、http://localhost:8025 で Mailpit Web インターフェイスにアクセスできます。

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well as execute arbitrary shell commands within the container: -->
場合によっては、アプリケーションのコンテナ内で Bash セッションを開始したい場合があります。 `shell` コマンドを使用してアプリケーションのコンテナに接続すると、そのファイルやインストールされたサービスを検査したり、コンテナ内で任意のシェル コマンドを実行したりできます。

```shell
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
新しい [Laravel Tinker](https://github.com/laravel/tinker) セッションを開始するには、`tinker` コマンドを実行します。

```shell
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.5, 8.4, 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.5. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `compose.yaml` file: -->
Sail は現在、PHP 8.5、8.4、8.3、8.2、8.1、または PHP 8.0 を介したアプリケーションの提供をサポートしています。 Sail で使用されるデフォルトの PHP バージョンは現在 PHP 8.5 です。アプリケーションの提供に使用される PHP バージョンを変更するには、アプリケーションの `compose.yaml` ファイル内の `laravel.test` コンテナの `build` 定義を更新する必要があります。

```yaml
# PHP 8.5
context: ./vendor/laravel/sail/runtimes/8.5

# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `compose.yaml` file: -->
さらに、アプリケーションで使用されている PHP のバージョンを反映するように、`image` 名を更新することもできます。このオプションは、アプリケーションの `compose.yaml` ファイルでも定義されます。

```yaml
image: sail-8.2/app
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images: -->
アプリケーションの `compose.yaml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

```shell
sail build --no-cache

sail up
```

<a name="sail-php-extensions"></a>
<!-- ### Additional PHP Extensions -->
### Additional PHP Extensions

<!-- Sail's runtime images include a common set of PHP extensions. If your application requires additional extensions, you may install them when building the image by adding a space-separated `PHP_EXTENSIONS` build argument to the `laravel.test` service in your application's `compose.yaml` file: -->
Sail のランタイムイメージには、一般的な PHP 拡張機能のセットが含まれています。アプリケーションで追加の拡張機能が必要な場合は、アプリケーションの `compose.yaml` ファイルの `laravel.test` サービスにスペース区切りの `PHP_EXTENSIONS` ビルド引数を追加することで、イメージのビルド時にインストールできます。

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        PHP_EXTENSIONS: 'gmp imagick'
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images. -->
アプリケーションの `compose.yaml` ファイルを更新した後、コンテナイメージを再構築する必要があります。

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 24 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `compose.yaml` file: -->
Sail はデフォルトで Node 24 をインストールします。イメージのビルド時にインストールされるノードのバージョンを変更するには、アプリケーションの `compose.yaml` ファイル内の `laravel.test` サービスの `build.args` 定義を更新します。

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images: -->
アプリケーションの `compose.yaml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
場合によっては、同僚にサイトをプレビューしたり、アプリケーションとの Webhook 統合をテストしたりするために、サイトをパブリックに共有する必要がある場合があります。サイトを共有するには、`share` コマンドを使用できます。このコマンドを実行すると、アプリケーションへのアクセスに使用できるランダムな `laravel-sail.site` URL が発行されます。

```shell
sail share
```

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies using the `trustProxies` middleware method in your application's `bootstrap/app.php` file. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` コマンドを介してサイトを共有する場合、アプリケーションの `bootstrap/app.php` ファイルで `trustProxies` ミドルウェア メソッドを使用して、アプリケーションの信頼できるプロキシを構成する必要があります。そうしないと、`url` や `route` などの URL生成ヘルパは、URL生成中に使用する必要がある正しい HTTP ホストを決定できなくなります。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
共有サイトのサブドメインを選択したい場合は、`share` コマンドを実行するときに `subdomain` オプションを指定できます。

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` コマンドは、[Expose](https://github.com/beyondcode/expose) によるオープン ソース トンネリング サービスである [BeyondCode](https://beyondco.de) を利用しています。

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. To enable Xdebug, ensure you have [published your Sail configuration](#sail-customization). Then, add the following variables to your application's `.env` file to configure Xdebug: -->
Laravel Sail の Docker 構成には、PHP 用の人気のある強力なデバッガーである [Xdebug](https://xdebug.org/) のサポートが含まれています。 Xdebug を有効にするには、[published your Sail configuration](#sail-customization) があることを確認してください。次に、次の変数をアプリケーションの `.env` ファイルに追加して、Xdebug を構成します。

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

<!-- Next, ensure that your published `php.ini` file includes the following configuration so that Xdebug is activated in the specified modes: -->
次に、指定されたモードで Xdebug がアクティブ化されるように、公開された `php.ini` ファイルに次の構成が含まれていることを確認します。

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

<!-- After modifying the `php.ini` file, remember to rebuild your Docker images so that your changes to the `php.ini` file take effect: -->
`php.ini` ファイルを変更した後は、`php.ini` ファイルへの変更を有効にするために、忘れずに Docker イメージを再構築してください。

```shell
sail build --no-cache
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux and you're using Docker 20.10+, `host.docker.internal` is available, and no manual configuration is required. -->
内部的には、`XDEBUG_CONFIG` 環境変数は `client_host=host.docker.internal` として定義されているため、Xdebug は Mac および Windows (WSL2) に対して適切に構成されます。ローカル マシンで Linux が実行されており、Docker 20.10 以降を使用している場合は、`host.docker.internal` が利用可能であり、手動構成は必要ありません。

<!-- For Docker versions older than 20.10, `host.docker.internal` is not supported on Linux, and you will need to manually define the host IP. To do this, configure a static IP for your container by defining a custom network in your `compose.yaml` file: -->
20.10 より古い Docker バージョンの場合、`host.docker.internal` は Linux でサポートされていないため、ホスト IP を手動で定義する必要があります。これを行うには、`compose.yaml` ファイルでカスタム ネットワークを定義して、コンテナーの静的 IP を構成します。

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

<!-- Once you have set the static IP, define the SAIL_XDEBUG_CONFIG variable within your application's .env file: -->
静的 IP を設定したら、アプリケーションの .env ファイル内で SAIL_XDEBUG_CONFIG 変数を定義します。

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
Artisan コマンドの実行時に、`sail debug` コマンドを使用してデバッグ セッションを開始できます。

```shell
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

<!-- If you're using PhpStorm, please review JetBrains' documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm を使用している場合は、[zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) に関する JetBrains のドキュメントを確認してください。

> [!WARNING]
> Laravel Sail は、アプリケーションを提供するために `artisan serve` に依存しています。 Laravel バージョン 8.53.0 では、`artisan serve` コマンドは `XDEBUG_CONFIG` 変数と `XDEBUG_MODE` 変数のみを受け入れます。 Laravel の古いバージョン (8.52.0 以下) はこれらの変数をサポートしておらず、デバッグ接続を受け入れません。

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail は単なる Docker であるため、Sail に関するほぼすべてを自由にカスタマイズできます。 Sail 独自の Dockerfile を公開するには、`sail:publish` コマンドを実行します。

```shell
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `compose.yaml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
このコマンドを実行すると、Laravel Sail で使用される Dockerfile およびその他の構成ファイルが、アプリケーションのルート ディレクトリの `docker` ディレクトリ内に配置されます。 Sail インストールをカスタマイズした後、アプリケーションの `compose.yaml` ファイル内のアプリケーション コンテナーのイメージ名を変更することができます。その後、`build` コマンドを使用してアプリケーションのコンテナを再構築します。 Sail を使用して単一マシン上で複数の Laravel アプリケーションを開発している場合、アプリケーション イメージに一意の名前を割り当てることが特に重要です。

```shell
sail build --no-cache
```

