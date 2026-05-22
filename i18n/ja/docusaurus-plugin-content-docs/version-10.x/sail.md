# Laravel Sail (Laravel Sail)

- [Introduction](#introduction)
- [インストールとセットアップ](#installation)
    - [既存のアプリケーションへの Sail のインストール](#installing-sail-into-existing-applications)
    - [シェルエイリアスの構成](#configuring-a-shell-alias)
- [帆の開始と停止](#starting-and-stopping-sail)
- [コマンドの実行](#executing-sail-commands)
    - [PHPコマンドの実行](#executing-php-commands)
    - [Composer コマンドの実行](#executing-composer-commands)
    - [Artisan コマンドの実行](#executing-artisan-commands)
    - [ノード/NPMコマンドの実行](#executing-node-npm-commands)
- [データベースとの対話](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [ファイルストレージ](#file-storage)
- [テストの実行](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [メールのプレビュー](#previewing-emails)
- [コンテナCLI](#sail-container-cli)
- [PHPのバージョン](#sail-php-versions)
- [ノードのバージョン](#sail-node-versions)
- [サイトを共有する](#sharing-your-site)
- [Xdebug を使用したデバッグ](#debugging-with-xdebug)
  - [Xdebug CLI の使用法](#xdebug-cli-usage)
  - [Xdebug ブラウザの使用法](#xdebug-browser-usage)
- [Customization](#sail-customization)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Sail](https://github.com/laravel/sail) は、Laravel のデフォルトの Docker 開発環境と対話するための軽量のコマンドライン インターフェイスです。 Sail は、事前の Docker 経験を必要とせずに、PHP、MySQL、および Redis を使用して Laravel アプリケーションを構築するための優れた出発点を提供します。

Sail の中心となるのは、プロジェクトのルートに保存されている `docker-compose.yml` ファイルと `sail` スクリプトです。 `sail` スクリプトは、`docker-compose.yml` ファイルで定義された Docker コンテナーと対話するための便利なメソッドを備えた CLI を提供します。

Laravel Sail は、macOS、Linux、Windows ([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 経由) でサポートされています。

<a name="installation"></a>
## インストールとセットアップ (Installation and Setup)

Laravel Sail はすべての新しい Laravel アプリケーションとともに自動的にインストールされるため、すぐに使用を開始できます。新しい Laravel アプリケーションの作成方法については、お使いのオペレーティング システム用の Laravel の [インストールドキュメント](/docs/{{version}}/installation#docker-installation-using-sail) を参照してください。インストール中に、アプリケーションが対話する Sail 対応サービスを選択するよう求められます。

<a name="installing-sail-into-existing-applications"></a>
### 既存のアプリケーションへの Sail のインストール

既存の Laravel アプリケーションで Sail を使用することに興味がある場合は、Composer パッケージ マネージャーを使用して Sail をインストールするだけです。もちろん、これらの手順は、既存のローカル開発環境で Composer の依存関係をインストールできることを前提としています。

```shell
composer require laravel/sail --dev
```

Sail がインストールされたら、`sail:install` Artisan コマンドを実行できます。このコマンドは、Sail の `docker-compose.yml` ファイルをアプリケーションのルートに公開し、Docker サービスに接続するために必要な環境変数を使用して `.env` ファイルを変更します。

```shell
php artisan sail:install
```

最後に、Sail を開始できます。 Sail の使用方法を学習し続けるには、このドキュメントの残りの部分を読み続けてください。

```shell
./vendor/bin/sail up
```

> [!WARNING]  
> Linux 用の Docker デスクトップを使用している場合は、コマンド `docker context use default` を実行して、`default` Docker コンテキストを使用する必要があります。

<a name="adding-additional-services"></a>
#### 追加サービスの追加

既存の Sail インストールに追加サービスを追加したい場合は、`sail:add` Artisan コマンドを実行できます。

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer の使用

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 内で開発したい場合は、`sail:install` コマンドに `--devcontainer` オプションを指定できます。 `--devcontainer` オプションは、デフォルトの `.devcontainer/devcontainer.json ` ファイルをアプリケーションのルートに公開するように `sail:install` コマンドに指示します。

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
### シェルエイリアスの構成

デフォルトでは、Sail コマンドは、すべての新しい Laravel アプリケーションに含まれる `vendor/bin/sail` スクリプトを使用して呼び出されます。

```shell
./vendor/bin/sail up
```

ただし、`vendor/bin/sail` を繰り返し入力して Sail コマンドを実行する代わりに、Sail のコマンドをより簡単に実行できるシェル エイリアスを構成することもできます。

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

これを常に利用できるようにするには、これをホーム ディレクトリのシェル構成ファイル (`~/.zshrc` や `~/.bashrc` など) に追加し、シェルを再起動します。

シェル エイリアスが設定されたら、「`sail`」と入力するだけで Sail コマンドを実行できます。このドキュメントの残りの例では、このエイリアスが設定されていることを前提としています。

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## 帆の開始と停止 (Starting and Stopping Sail)

Laravel Sail の `docker-compose.yml` ファイルは、Laravel アプリケーションの構築を支援するために連携して動作するさまざまな Docker コンテナを定義します。これらの各コンテナーは、`docker-compose.yml` ファイルの `services` 構成内のエントリです。 `laravel.test` コンテナーは、アプリケーションを提供するプライマリ アプリケーション コンテナーです。

Sail を開始する前に、ローカル コンピューター上で他の Web サーバーやデータベースが実行されていないことを確認する必要があります。アプリケーションの `docker-compose.yml` ファイルで定義されているすべての Docker コンテナを起動するには、`up` コマンドを実行する必要があります。

```shell
sail up
```

すべての Docker コンテナをバックグラウンドで起動するには、Sail を「デタッチ」モードで起動します。

```shell
sail up -d
```

アプリケーションのコンテナが開始されたら、Web ブラウザで http://localhost. にあるプロジェクトにアクセスできます。

すべてのコンテナを停止するには、Ctrl + C を押してコンテナの実行を停止します。または、コンテナーがバックグラウンドで実行されている場合は、`stop` コマンドを使用できます。

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## コマンドの実行 (Executing Commands)

Laravel Sail を使用する場合、アプリケーションは Docker コンテナ内で実行され、ローカル コンピューターから分離されます。ただし、Sail は、任意の PHP コマンド、Artisan コマンド、Composer コマンド、Node / NPM コマンドなど、アプリケーションに対してさまざまなコマンドを実行する便利な方法を提供します。

**Laravel ドキュメントを読むと、Sail を参照していない Composer、Artisan、および Node / NPM コマンドへの参照が頻繁に表示されます。** これらの例では、これらのツールがローカル コンピューターにインストールされていることを前提としています。ローカルの Laravel 開発環境に Sail を使用している場合は、Sail を使用してこれらのコマンドを実行する必要があります。

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHPコマンドの実行

PHP コマンドは、`php` コマンドを使用して実行できます。もちろん、これらのコマンドは、アプリケーション用に構成された PHP バージョンを使用して実行されます。 Laravel Sail で利用可能な PHP バージョンの詳細については、[PHPバージョンのドキュメント](#sail-php-versions) を参照してください。

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer コマンドの実行

Composer コマンドは、`composer` コマンドを使用して実行できます。 Laravel Sail のアプリケーションコンテナには Composer 2.x インストールが含まれています。

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
#### 既存のアプリケーションの Composer 依存関係のインストール

チームでアプリケーションを開発している場合、最初に Laravel アプリケーションを作成するのは自分ではない可能性があります。したがって、アプリケーションのリポジトリをローカル コンピュータに複製した後は、Sail を含むアプリケーションの Composer 依存関係はインストールされません。

アプリケーションのディレクトリに移動し、次のコマンドを実行することで、アプリケーションの依存関係をインストールできます。このコマンドは、PHP と Composer を含む小さな Docker コンテナを使用して、アプリケーションの依存関係をインストールします。

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

`laravelsail/phpXX-composer` イメージを使用する場合は、アプリケーションに使用する予定と同じバージョンの PHP を使用する必要があります (`80`、`81`、`82`、または `83`)。

<a name="executing-artisan-commands"></a>
### Artisan コマンドの実行

Laravel Artisan コマンドは、`artisan` コマンドを使用して実行できます。

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### ノード/NPMコマンドの実行

ノード コマンドは `node` コマンドを使用して実行でき、NPM コマンドは `npm` コマンドを使用して実行できます。

```shell
sail node --version

sail npm run dev
```

必要に応じて、NPM の代わりに Yarn を使用することもできます。

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## データベースとの対話 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

お気づきかもしれませんが、アプリケーションの `docker-compose.yml` ファイルには、MySQL コンテナのエントリが含まれています。このコンテナーは [Docker ボリューム](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、データベースに保存されているデータは保持されます。

さらに、MySQL コンテナを初めて起動すると、2 つのデータベースが作成されます。最初のデータベースは、`DB_DATABASE` 環境変数の値を使用して名前が付けられ、ローカル開発用です。 2 つ目は、`testing` という名前の専用のテスト データベースで、テストが開発データに干渉しないことを保証します。

コンテナーを起動したら、アプリケーションの `.env` ファイル内の `DB_HOST` 環境変数を `mysql` に設定することで、アプリケーション内の MySQL インスタンスに接続できます。

ローカル マシンからアプリケーションの MySQL データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、MySQL データベースは `localhost` ポート 3306 でアクセスでき、アクセス資格情報は `DB_USERNAME` および `DB_PASSWORD` 環境変数の値に対応します。または、`root` ユーザーとして接続することもできます。この場合も、`DB_PASSWORD` 環境変数の値がパスワードとして使用されます。

<a name="redis"></a>
### レディス

アプリケーションの `docker-compose.yml` ファイルには、[Redis](https://redis.io) コンテナーのエントリも含まれています。このコンテナーは [Docker ボリューム](https://docs.docker.com/storage/volumes/) を使用するため、コンテナーを停止および再起動しても、Redis データに保存されたデータは保持されます。コンテナーを起動したら、アプリケーションの `.env` ファイル内の `REDIS_HOST` 環境変数を `redis` に設定することで、アプリケーション内の Redis インスタンスに接続できます。

ローカル マシンからアプリケーションの Redis データベースに接続するには、[TablePlus](https://tableplus.com) などのグラフィカル データベース管理アプリケーションを使用できます。デフォルトでは、Redis データベースは `localhost` ポート 6379 でアクセスできます。

<a name="meilisearch"></a>
### メイリサーチ

Sail のインストール時に [Meilisearch](https://www.meilisearch.com) サービスのインストールを選択した場合、アプリケーションの `docker-compose.yml` ファイルには、この強力な検索エンジンのエントリ ([compatible](https://github.com/meilisearch/meilisearch-laravel-scout) と [Laravel Scout](/docs/{{version}}/scout)) が含まれます。コンテナーを起動したら、`MEILISEARCH_HOST` 環境変数を `http://meilisearch:7700` に設定することで、アプリケーション内の Meil​​isearch インスタンスに接続できます。

ローカル マシンから、Web ブラウザで `http://localhost:7700` に移動して、Meilisearch の Web ベースの管理パネルにアクセスできます。

<a name="typesense"></a>
### Typesense

Sail のインストール時に [Typesense](https://typesense.org) サービスのインストールを選択した場合、アプリケーションの `docker-compose.yml` ファイルには、[Laravel Scout](/docs/{{version}}/scout#typesense) とネイティブに統合されたこの超高速のオープンソース検索エンジンのエントリが含まれます。コンテナーを起動したら、次の環境変数を設定して、アプリケーション内の Typesense インスタンスに接続できます。

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

ローカル マシンから、`http://localhost:8108` 経由で Typesense の API にアクセスできます。

<a name="file-storage"></a>
## ファイルストレージ (File Storage)

本番環境でアプリケーションを実行しているときに Amazon S3 を使用してファイルを保存する予定がある場合は、Sail のインストール時に [MinIO](https://min.io) サービスをインストールすることをお勧めします。 MinIO は、運用 S3 環境で「テスト」ストレージ バケットを作成せずに、Laravel の `s3` ファイルストレージ ドライバを使用してローカルで開発するために使用できる S3 互換 API を提供します。 Sail のインストール中に MinIO のインストールを選択した場合、MinIO 構成セクションがアプリケーションの `docker-compose.yml` ファイルに追加されます。

デフォルトでは、アプリケーションの `filesystems` 構成ファイルには、`s3` ディスクのディスク構成がすでに含まれています。このディスクを使用して Amazon S3 と対話するだけでなく、構成を制御する関連する環境変数を変更するだけで、MinIO などの S3 互換ファイルストレージ サービスと対話するためにディスクを使用することもできます。たとえば、MinIO を使用する場合、ファイルシステムの環境変数構成を次のように定義する必要があります。

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

MinIO の使用時に Laravel の Flysystem 統合で適切な URL を生成するには、アプリケーションのローカル URL と一致し、URL パスにバケット名が含まれるように `AWS_URL` 環境変数を定義する必要があります。

```ini
AWS_URL=http://localhost:9000/local
```

バケットは、`http://localhost:8900` で利用できる MinIO コンソール経由で作成できます。 MinIO コンソールのデフォルトのユーザー名は `sail` で、デフォルトのパスワードは `password` です。

> [!WARNING]  
> MinIO を使用する場合、`temporaryUrl` メソッドによる一時ストレージ URL の生成はサポートされません。

<a name="running-tests"></a>
## テストの実行 (Running Tests)

Laravel はすぐに使える素晴らしいテストサポートを提供しており、Sail の `test` コマンドを使用してアプリケーション [機能テストと単体テスト](/docs/{{version}}/testing) を実行できます。 PHPUnit によって受け入れられる CLI オプションはすべて、`test` コマンドに渡すこともできます。

```shell
sail test

sail test --group orders
```

Sail `test` コマンドは、`test` Artisan コマンドの実行と同等です。

```shell
sail artisan test
```

デフォルトでは、Sail は専用の `testing` データベースを作成し、テストがデータベースの現在の状態に干渉しないようにします。デフォルトの Laravel インストールでは、Sail はテストの実行時にこのデータベースを使用するように `phpunit.xml` ファイルも設定します。

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/{{version}}/dusk) は、表現力豊かで使いやすいブラウザ自動化およびテスト API を提供します。 Sail のおかげで、Selenium やその他のツールをローカル コンピューターにインストールしなくても、これらのテストを実行できます。まず、アプリケーションの `docker-compose.yml` ファイル内の Selenium サービスのコメントを解除します。

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

次に、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービスに、`selenium` の `depends_on` エントリがあることを確認します。

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

最後に、Sail を起動して `dusk` コマンドを実行することで、Dusk テスト スイートを実行できます。

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Appleシリコン上のセレン

ローカル マシンに Apple Silicon チップが含まれている場合、`selenium` サービスは `seleniarm/standalone-chromium` イメージを使用する必要があります。

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## メールのプレビュー (Previewing Emails)

Laravel Sail のデフォルトの `docker-compose.yml` ファイルには、[Mailpit](https://github.com/axllent/mailpit) のサービスエントリが含まれています。 Mailpit は、ローカル開発中にアプリケーションによって送信された電子メールをインターセプトし、ブラウザで電子メール メッセージをプレビューできる便利な Web インターフェイスを提供します。 Sail を使用する場合、Mailpit のデフォルトのホストは `mailpit` で、ポート 1025 経由で利用できます。

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail の実行中は、http://localhost:8025 で Mailpit Web インターフェイスにアクセスできます。

<a name="sail-container-cli"></a>
## コンテナCLI (Container CLI)

場合によっては、アプリケーションのコンテナ内で Bash セッションを開始したい場合があります。 `shell` コマンドを使用してアプリケーションのコンテナに接続すると、そのファイルやインストールされているサービスを検査したり、コンテナ内で任意のシェル コマンドを実行したりできます。

```shell
sail shell

sail root-shell
```

新しい [Laravel Tinker](https://github.com/laravel/tinker) セッションを開始するには、`tinker` コマンドを実行します。

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHPのバージョン (PHP Versions)

Sail は現在、PHP 8.3、8.2、8.1、または PHP 8.0 を介したアプリケーションの提供をサポートしています。 Sail で使用されるデフォルトの PHP バージョンは現在 PHP 8.3 です。アプリケーションの提供に使用される PHP バージョンを変更するには、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` コンテナの `build` 定義を更新する必要があります。

```yaml
# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

さらに、アプリケーションで使用されている PHP のバージョンを反映するように、`image` 名を更新することもできます。このオプションは、アプリケーションの `docker-compose.yml` ファイルでも定義されます。

```yaml
image: sail-8.1/app
```

アプリケーションの `docker-compose.yml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## ノードのバージョン (Node Versions)

Sail はデフォルトで Node 20 をインストールします。イメージのビルド時にインストールされるノードのバージョンを変更するには、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービスの `build.args` 定義を更新します。

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

アプリケーションの `docker-compose.yml` ファイルを更新した後、コンテナー イメージを再構築する必要があります。

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## サイトを共有する (Sharing Your Site)

場合によっては、同僚にサイトをプレビューしたり、アプリケーションとの Webhook 統合をテストしたりするために、サイトをパブリックに共有する必要がある場合があります。サイトを共有するには、`share` コマンドを使用できます。このコマンドを実行すると、アプリケーションへのアクセスに使用できるランダムな `laravel-sail.site` URL が発行されます。

```shell
sail share
```

`share` コマンドを使用してサイトを共有する場合は、`TrustProxies` ミドルウェア内でアプリケーションの信頼できるプロキシを構成する必要があります。そうしないと、`url` や `route` などの URL生成ヘルパは、URL生成中に使用する必要がある正しい HTTP ホストを決定できなくなります。

    /**
     * The trusted proxies for this application.
     *
     * @var array|string|null
     */
    protected $proxies = '*';

共有サイトのサブドメインを選択したい場合は、`share` コマンドを実行するときに `subdomain` オプションを指定できます。

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]  
> `share` コマンドは、[BeyondCode](https://github.com/beyondcode/expose) によるオープン ソース トンネリング サービスである [Expose](https://beyondco.de) を利用しています。

<a name="debugging-with-xdebug"></a>
## Xdebug を使用したデバッグ (Debugging With Xdebug)

Laravel Sail の Docker 構成には、PHP 用の人気のある強力なデバッガーである [Xdebug](https://xdebug.org/) のサポートが含まれています。 Xdebug を有効にするには、アプリケーションの `.env` ファイルから [Xdebug を設定する](https://xdebug.org/docs/step_debug#mode) にいくつかの変数を追加する必要があります。 Xdebug を有効にするには、Sail を開始する前に適切なモードを設定する必要があります。

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

#### Linux ホスト IP 構成

内部的には、`XDEBUG_CONFIG` 環境変数は `client_host=host.docker.internal` として定義されているため、Xdebug は Mac および Windows (WSL2) に対して適切に構成されます。ローカル マシンで Linux を実行している場合は、Docker Engine 17.06.0 以降および Compose 1.16.0 以降を実行していることを確認する必要があります。それ以外の場合は、以下に示すようにこの環境変数を手動で定義する必要があります。

まず、次のコマンドを実行して、環境変数に追加する正しいホスト IP アドレスを決定する必要があります。通常、`<container-name>` はアプリケーションを提供するコンテナーの名前である必要があり、多くの場合 `_laravel.test_1` で終わります。

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

正しいホスト IP アドレスを取得したら、アプリケーションの `.env` ファイル内で `SAIL_XDEBUG_CONFIG` 変数を定義する必要があります。

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI の使用法

Artisan コマンドの実行時に、`sail debug` コマンドを使用してデバッグ セッションを開始できます。

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug ブラウザの使用法

Web ブラウザ経由でアプリケーションと対話しながらアプリケーションをデバッグするには、[Xdebug によって提供される手順](https://xdebug.org/docs/step_debug#web-application) に従って Web ブラウザから Xdebug セッションを開始します。

PhpStorm を使用している場合は、[ゼロ構成デバッグ](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) に関する JetBrain のドキュメントを確認してください。

> [!WARNING]  
> Laravel Sail は、アプリケーションを提供するために `artisan serve` に依存しています。 Laravel バージョン 8.53.0 では、`artisan serve` コマンドは `XDEBUG_CONFIG` 変数と `XDEBUG_MODE` 変数のみを受け入れます。 Laravel の古いバージョン (8.52.0 以下) はこれらの変数をサポートしておらず、デバッグ接続を受け入れません。

<a name="sail-customization"></a>
## カスタマイズ (Customization)

Sail は単なる Docker であるため、Sail に関するほぼすべてを自由にカスタマイズできます。 Sail 独自の Dockerfile を公開するには、`sail:publish` コマンドを実行します。

```shell
sail artisan sail:publish
```

このコマンドを実行すると、Laravel Sail で使用される Dockerfile およびその他の構成ファイルが、アプリケーションのルート ディレクトリの `docker` ディレクトリ内に配置されます。 Sail インストールをカスタマイズした後、アプリケーションの `docker-compose.yml` ファイル内のアプリケーション コンテナーのイメージ名を変更することができます。その後、`build` コマンドを使用してアプリケーションのコンテナを再構築します。 Sail を使用して単一マシン上で複数の Laravel アプリケーションを開発している場合、アプリケーション イメージに一意の名前を割り当てることが特に重要です。

```shell
sail build --no-cache
```

