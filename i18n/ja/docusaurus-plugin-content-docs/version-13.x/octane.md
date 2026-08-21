<!-- # Laravel Octane -->
# Laravel Octane

- [Introduction](#introduction)
- [Installation](#installation)
- [Server Prerequisites](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Serving Your Application](#serving-your-application)
    - [Serving Your Application via HTTPS](#serving-your-application-via-https)
    - [Serving Your Application via Nginx](#serving-your-application-via-nginx)
    - [Watching for File Changes](#watching-for-file-changes)
    - [Specifying the Worker Count](#specifying-the-worker-count)
    - [Specifying the Max Request Count](#specifying-the-max-request-count)
    - [Specifying the Max Execution Time](#specifying-the-max-execution-time)
    - [Reloading the Workers](#reloading-the-workers)
    - [Stopping the Server](#stopping-the-server)
- [Dependency Injection and Octane](#dependency-injection-and-octane)
    - [Container Injection](#container-injection)
    - [Request Injection](#request-injection)
    - [Configuration Repository Injection](#configuration-repository-injection)
- [Managing Memory Leaks](#managing-memory-leaks)
- [Concurrent Tasks](#concurrent-tasks)
- [Ticks and Intervals](#ticks-and-intervals)
- [The Octane Cache](#the-octane-cache)
    - [Cache Intervals](#cache-intervals)
- [Tables](#tables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Octane](https://github.com/laravel/octane) supercharges your application's performance by serving your application using high-powered application servers, including [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), and [RoadRunner](https://roadrunner.dev). Octane boots your application once, keeps it in memory, and then feeds it requests at supersonic speeds. -->
[Laravel Octane](https://github.com/laravel/octane) は、[FrankenPHP](https://frankenphp.dev/)、[Open Swoole](https://openswoole.com/)、[Swoole](https://github.com/swoole/swoole-src)、[RoadRunner](https://roadrunner.dev) などの高性能アプリケーション サーバーを使用してアプリケーションを提供することにより、アプリケーションのパフォーマンスを大幅に向上させます。 Octane はアプリケーションを一度起動してメモリに保持し、超音速でリクエストを送ります。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Octane may be installed via the Composer package manager: -->
Octane は Composer パッケージ マネージャー経由でインストールできます。

```shell
composer require laravel/octane
```

<!-- After installing Octane, you may execute the `octane:install` Artisan command, which will install Octane's configuration file into your application: -->
Octane をインストールした後、`octane:install` Artisan コマンドを実行すると、Octane の構成ファイルがアプリケーションにインストールされます。

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
<!-- ## Server Prerequisites -->
## Server Prerequisites

<a name="frankenphp"></a>
<!-- ### FrankenPHP -->
### FrankenPHP

<!-- [FrankenPHP](https://frankenphp.dev) is a PHP application server, written in Go, that supports modern web features like early hints, Brotli, and Zstandard compression. When you install Octane and choose FrankenPHP as your server, Octane will automatically download and install the FrankenPHP binary for you. -->
[FrankenPHP](https://frankenphp.dev) は Go で書かれた PHP アプリケーション サーバーで、初期ヒント、Brotli、Zstandard 圧縮などの最新の Web 機能をサポートします。 Octane をインストールし、サーバーとして FrankenPHP を選択すると、Octane は自動的に FrankenPHP バイナリをダウンロードしてインストールします。

<a name="frankenphp-via-laravel-sail"></a>
<!-- #### FrankenPHP via Laravel Sail -->
#### FrankenPHP via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/13.x/sail), you should run the following commands to install Octane and FrankenPHP: -->
[Laravel Sail](/docs/13.x/sail) を使用してアプリケーションを開発する場合は、次のコマンドを実行して Octane と FrankenPHP をインストールする必要があります。

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

<!-- Next, you should use the `octane:install` Artisan command to install the FrankenPHP binary: -->
次に、`octane:install` Artisan コマンドを使用して、FrankenPHP バイナリをインストールする必要があります。

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

<!-- Finally, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
最後に、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービス定義に `SUPERVISOR_PHP_COMMAND` 環境変数を追加します。この環境変数には、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供するために使用するコマンドが含まれます。

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

<!-- To enable HTTPS, HTTP/2, and HTTP/3, apply these modifications instead: -->
HTTPS、HTTP/2、および HTTP/3 を有効にするには、代わりに次の変更を適用します。

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

<!-- Typically, you should access your FrankenPHP Sail application via `https://localhost`, as using `https://127.0.0.1` requires additional configuration and is [discouraged](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker). -->
通常、`https://localhost` を使用して FrankenPHP Sail アプリケーションにアクセスする必要があります。`https://127.0.0.1` を使用するには追加の構成が必要であり、[discouraged](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker) であるためです。

<a name="frankenphp-via-docker"></a>
<!-- #### FrankenPHP via Docker -->
#### FrankenPHP via Docker

<!-- Using FrankenPHP's official Docker images can offer improved performance and the use of additional extensions not included with static installations of FrankenPHP. In addition, the official Docker images provide support for running FrankenPHP on platforms it doesn't natively support, such as Windows. FrankenPHP's official Docker images are suitable for both local development and production usage. -->
FrankenPHP の公式 Docker イメージを使用すると、パフォーマンスが向上し、FrankenPHP の静的インストールには含まれていない追加の拡張機能を使用できます。さらに、公式の Docker イメージは、Windows など、ネイティブにサポートされていないプラットフォームでの FrankenPHP の実行のサポートを提供します。 FrankenPHP の公式 Docker イメージは、ローカル開発と運用環境の両方に適しています。

<!-- You may use the following Dockerfile as a starting point for containerizing your FrankenPHP powered Laravel application: -->
FrankenPHP を利用した Laravel アプリケーションをコンテナ化するための開始点として、次の Dockerfile を使用できます。

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

<!-- Then, during development, you may utilize the following Docker Compose file to run your application: -->
その後、開発中に次の Docker Compose ファイルを利用してアプリケーションを実行できます。

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

<!-- If the `--log-level` option is explicitly passed to the `php artisan octane:start` command, Octane will use FrankenPHP's native logger and, unless configured differently, will produce structured JSON logs. -->
`--log-level` オプションが `php artisan octane:start` コマンドに明示的に渡された場合、Octane は FrankenPHP のネイティブ ロガーを使用し、別の設定がされていない限り、構造化された JSON ログを生成します。

<!-- You may consult [the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/) for more information on running FrankenPHP with Docker. -->
Docker での FrankenPHP の実行の詳細については、[the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/) を参照してください。

<a name="frankenphp-caddyfile"></a>
<!-- #### Custom Caddyfile Configuration -->
#### Custom Caddyfile Configuration

<!-- When using FrankenPHP, you may specify a custom Caddyfile using the `--caddyfile` option when starting Octane: -->
FrankenPHP を使用する場合、Octane の起動時に `--caddyfile` オプションを使用してカスタム Caddyfile を指定できます。

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

<!-- This allows you to customize FrankenPHP's configuration beyond the default settings, such as adding custom middleware, configuring advanced routing, or setting up custom directives. You may consult the [official Caddy documentation](https://caddyserver.com/docs/caddyfile) for more information on Caddyfile syntax and configuration options. -->
これにより、カスタム ミドルウェアの追加、高度なルーティングの構成、カスタム ディレクティブの設定など、デフォルト設定を超えて FrankenPHP の構成をカスタマイズできます。 Caddyfile の構文と構成オプションの詳細については、[official Caddy documentation](https://caddyserver.com/docs/caddyfile) を参照してください。

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev) は、Go を使用して構築された RoadRunner バイナリを利用しています。 RoadRunner ベースの Octane サーバーを初めて起動すると、Octane は RoadRunner バイナリのダウンロードとインストールを提案します。

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner via Laravel Sail -->
#### RoadRunner via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/13.x/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/13.x/sail) を使用してアプリケーションを開発する場合は、次のコマンドを実行して Octane と RoadRunner をインストールする必要があります。

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
次に、Sail シェルを起動し、`rr` 実行可能ファイルを使用して、RoadRunner バイナリの最新の Linux ベース ビルドを取得する必要があります。

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- Then, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
次に、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービス定義に `SUPERVISOR_PHP_COMMAND` 環境変数を追加します。この環境変数には、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供するために使用するコマンドが含まれます。

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, ensure the `rr` binary is executable and build your Sail images: -->
最後に、`rr` バイナリが実行可能であることを確認し、Sail イメージをビルドします。

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
<!-- ### Swoole -->
### Swoole

<!-- If you plan to use the Swoole application server to serve your Laravel Octane application, you must install the Swoole PHP extension. Typically, this can be done via PECL: -->
Swoole アプリケーションサーバーを使用して Laravel Octane アプリケーションを提供する場合は、Swoole PHP 拡張機能をインストールする必要があります。通常、これは PECL 経由で実行できます。

```shell
pecl install swoole
```

<a name="openswoole"></a>
<!-- #### Open Swoole -->
#### Open Swoole

<!-- If you want to use the Open Swoole application server to serve your Laravel Octane application, you must install the Open Swoole PHP extension. Typically, this can be done via PECL: -->
Open Swoole アプリケーション サーバーを使用して Laravel Octane アプリケーションを提供する場合は、Open Swoole PHP 拡張機能をインストールする必要があります。通常、これは PECL 経由で実行できます。

```shell
pecl install openswoole
```

<!-- Using Laravel Octane with Open Swoole grants the same functionality provided by Swoole, such as concurrent tasks, ticks, and intervals. -->
Open Swoole で Laravel Octane を使用すると、同時タスク、ティック、間隔など、Swoole が提供するのと同じ機能が付与されます。

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole via Laravel Sail -->
#### Swoole via Laravel Sail

> [!WARNING]
> Sail 経由で Octane アプリケーションを提供する前に、Laravel Sail が最新バージョンであることを確認し、アプリケーションのルート ディレクトリ内で `./vendor/bin/sail build --no-cache` を実行してください。

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/13.x/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `docker-compose.yml` file used by Sail. -->
あるいは、Laravel の公式 Docker ベース開発環境である [Laravel Sail](/docs/13.x/sail) を使用して、Swoole ベースの Octane アプリケーションを開発することもできます。 Laravel Sail にはデフォルトで Swoole 拡張機能が含まれています。ただし、Sail で使用される `docker-compose.yml` ファイルを調整する必要があります。

<!-- To get started, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
まず、アプリケーションの `docker-compose.yml` ファイル内の `laravel.test` サービス定義に `SUPERVISOR_PHP_COMMAND` 環境変数を追加します。この環境変数には、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供するために使用するコマンドが含まれます。

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, build your Sail images: -->
最後に、Sail イメージを構築します。

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
<!-- #### Swoole Configuration -->
#### Swoole Configuration

<!-- Swoole supports a few additional configuration options that you may add to your `octane` configuration file if necessary. Because they rarely need to be modified, these options are not included in the default configuration file: -->
Swoole は、必要に応じて `octane` 構成ファイルに追加できるいくつかの追加構成オプションをサポートしています。これらのオプションはほとんど変更する必要がないため、デフォルトの構成ファイルには含まれていません。

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
<!-- ## Serving Your Application -->
## Serving Your Application

<!-- The Octane server can be started via the `octane:start` Artisan command. By default, this command will utilize the server specified by the `server` configuration option of your application's `octane` configuration file: -->
Octane サーバーは、`octane:start` Artisan コマンドを使用して起動できます。デフォルトでは、このコマンドは、アプリケーションの `octane` 構成ファイルの `server` 構成オプションで指定されたサーバーを利用します。

```shell
php artisan octane:start
```

<!-- By default, Octane will start the server on port 8000, so you may access your application in a web browser via `http://localhost:8000`. -->
デフォルトでは、Octane はポート 8000 でサーバーを起動するため、`http://localhost:8000` を介して Web ブラウザでアプリケーションにアクセスできます。

<a name="keeping-octane-running-in-production"></a>
<!-- #### Keeping Octane Running in Production -->
#### Keeping Octane Running in Production

<!-- If you are deploying your Octane application to production, you should use a process monitor such as Supervisor to ensure the Octane server stays running. A sample Supervisor configuration file for Octane might look like the following: -->
Octane アプリケーションを実稼働環境にデプロイする場合は、Supervisor などのプロセス モニターを使用して、Octane サーバーが確実に実行され続けるようにする必要があります。 Octane のSupervisor構成ファイルのサンプルは次のようになります。

```ini
[program:octane]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/example.com/artisan octane:start --server=frankenphp --host=127.0.0.1 --port=8000
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/storage/logs/octane.log
stopwaitsecs=3600
```

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application via HTTPS -->
### Serving Your Application via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
デフォルトでは、Octane 経由で実行されるアプリケーションは、`http://` というプレフィックスが付いたリンクを生成します。アプリケーションの `config/octane.php` 構成ファイル内で使用される `OCTANE_HTTPS` 環境変数は、HTTPS 経由でアプリケーションを提供するときに `true` に設定できます。この設定値が `true` に設定されている場合、Octane は、生成されたすべてのリンクに `https://` というプレフィックスを付けるように Laravel に指示します。

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application via Nginx -->
### Serving Your Application via Nginx

> [!NOTE]
> 独自のサーバー構成を管理する準備がまだ整っていない場合、または堅牢な Laravel Octane アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、フルマネージド Laravel Octane サポートを提供する [Laravel Cloud](https://cloud.laravel.com) をチェックしてください。

<!-- In production environments, you should serve your Octane application behind a traditional web server such as Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
運用環境では、Nginx や Apache などの従来の Web サーバーの背後で Octane アプリケーションを提供する必要があります。これにより、Web サーバーが画像やスタイルシートなどの静的資産を提供したり、SSL 証明書の終了を管理したりできるようになります。

<!-- In the Nginx configuration example below, Nginx will serve the site's static assets and proxy requests to the Octane server that is running on port 8000: -->
以下の Nginx 構成例では、Nginx はサイトの静的アセットとプロキシ リクエストをポート 8000 で実行されている Octane サーバーに提供します。

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```

<a name="watching-for-file-changes"></a>
<!-- ### Watching for File Changes -->
### Watching for File Changes

<!-- Since your application is loaded in memory once when the Octane server starts, any changes to your application's files will not be reflected when you refresh your browser. For example, route definitions added to your `routes/web.php` file will not be reflected until the server is restarted. For convenience, you may use the `--watch` flag to instruct Octane to automatically restart the server on any file changes within your application: -->
アプリケーションは Octane サーバーの起動時に一度メモリに読み込まれるため、ブラウザを更新してもアプリケーションのファイルへの変更は反映されません。たとえば、`routes/web.php` ファイルに追加されたルート定義は、サーバーが再起動されるまで反映されません。便宜上、`--watch` フラグを使用して、アプリケーション内のファイル変更時にサーバーを自動的に再起動するように Octane に指示できます。

```shell
php artisan octane:start --watch
```

<!-- Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
この機能を使用する前に、[Node](https://nodejs.org) がローカル開発環境にインストールされていることを確認する必要があります。さらに、プロジェクト内に [Chokidar](https://github.com/paulmillr/chokidar) ファイル監視ライブラリをインストールする必要があります。

```shell
npm install --save-dev chokidar
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/octane.php` configuration file. -->
アプリケーションの `config/octane.php` 構成ファイル内の `watch` 構成オプションを使用して、監視する必要があるディレクトリとファイルを構成できます。

<a name="specifying-the-worker-count"></a>
<!-- ### Specifying the Worker Count -->
### Specifying the Worker Count

<!-- By default, Octane will start an application request worker for each CPU core provided by your machine. These workers will then be used to serve incoming HTTP requests as they enter your application. You may manually specify how many workers you would like to start using the `--workers` option when invoking the `octane:start` command: -->
デフォルトでは、Octane はマシンが提供する各 CPU コアに対してアプリケーション リクエスト ワーカーを開始します。これらのワーカーは、アプリケーションに入ってくる受信 HTTP リクエストを処理するために使用されます。 `octane:start` コマンドを呼び出すときに、`--workers` オプションを使用して、開始するワーカーの数を手動で指定できます。

```shell
php artisan octane:start --workers=4
```

<!-- If you are using the Swoole application server, you may also specify how many ["task workers"](#concurrent-tasks) you wish to start: -->
Swoole アプリケーション サーバーを使用している場合は、起動する ["task workers"](#concurrent-tasks) の数を指定することもできます。

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
<!-- ### Specifying the Max Request Count -->
### Specifying the Max Request Count

<!-- To help prevent stray memory leaks, Octane gracefully restarts any worker once it has handled 500 requests. To adjust this number, you may use the `--max-requests` option: -->
漂遊メモリ リークを防ぐために、Octane は 500 件のリクエストを処理した後、ワーカーを正常に再起動します。この数値を調整するには、`--max-requests` オプションを使用できます。

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
<!-- ### Specifying the Max Execution Time -->
### Specifying the Max Execution Time

<!-- By default, Laravel Octane sets a maximum execution time of 30 seconds for incoming requests via the `max_execution_time` option in your application's `config/octane.php` configuration file: -->
デフォルトでは、Laravel Octaneは、アプリケーションの `config/octane.php` 設定ファイルの `max_execution_time` オプションを介して、受信リクエストの最大実行時間を30秒に設定します。

```php
'max_execution_time' => 30,
```

<!-- This setting defines the maximum number of seconds that an incoming request is allowed to execute before being terminated. Setting this value to `0` will disable the execution time limit entirely. This configuration option is particularly useful for applications that handle long-running requests, such as file uploads, data processing, or API calls to external services. -->
この設定は、受信リクエストが終了するまでに実行を許可される最大秒数を定義します。この値を `0` に設定すると、実行時間制限が完全に無効になります。この構成オプションは、ファイルのアップロード、データ処理、外部サービスへの API 呼び出しなど、長時間実行されるリクエストを処理するアプリケーションに特に役立ちます。

> [!WARNING]
> `max_execution_time` 構成を変更する場合、変更を有効にするために Octane サーバーを再起動する必要があります。

<a name="reloading-the-workers"></a>
<!-- ### Reloading the Workers -->
### Reloading the Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
`octane:reload` コマンドを使用して、Octane サーバーのアプリケーション ワーカーを正常に再起動できます。通常、これは、新しくデプロイされたコードがメモリにロードされ、後続のリクエストに対応するために使用されるように、デプロイ後に実行する必要があります。

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping the Server -->
### Stopping the Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
`octane:stop` Artisan コマンドを使用して、Octane サーバーを停止できます。

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking the Server Status -->
#### Checking the Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
`octane:status` Artisan コマンドを使用して、Octane サーバーの現在のステータスを確認できます。

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection and Octane -->
## Dependency Injection and Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane はアプリケーションを一度起動し、リクエストを処理する間メモリ内に保持するため、アプリケーションを構築する際に考慮すべき注意事項がいくつかあります。たとえば、アプリケーションのサービスプロバイダの `register` メソッドと `boot` メソッドは、リクエスト ワーカーが最初に起動するときに 1 回だけ実行されます。後続のリクエストでは、同じアプリケーション インスタンスが再利用されます。

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a stale version of the container or request on subsequent requests. -->
このため、アプリケーションのサービスコンテナやリクエストをオブジェクトのコンストラクターへ注入する際は、特に注意してください。そうすると、そのオブジェクトが後続のリクエストでコンテナやリクエストの古い状態を保持してしまう可能性があります。

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Octane は、リクエスト間のファーストパーティ フレームワークの状態のリセットを自動的に処理します。ただし、Octane は、アプリケーションによって作成されたグローバル状態をリセットする方法を常に知っているわけではありません。したがって、Octane に適した方法でアプリケーションを構築する方法を認識する必要があります。以下では、Octane の使用中に問題が発生する可能性のある最も一般的な状況について説明します。

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
一般に、アプリケーション サービスコンテナまたは HTTP リクエスト インスタンスを他のオブジェクトのコンストラクターに挿入することは避けてください。たとえば、次のバインディングは、アプリケーション サービスコンテナ全体をシングルトンとしてバインドされたオブジェクトに挿入します。

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the container will be injected into the service and that same container will be held by the `Service` instance on subsequent requests. This **may** not be a problem for your particular application; however, it can lead to the container unexpectedly missing bindings that were added later in the boot cycle or by a subsequent request. -->
この例では、アプリケーションの起動プロセス中に `Service` インスタンスが解決されると、コンテナーがサービスに挿入され、その同じコンテナーが後続のリクエストで `Service` インスタンスによって保持されます。これは、特定のアプリケーションでは問題にならない可能性があります。ただし、ブート サイクルの後半または後続のリクエストによって追加されたバインディングがコンテナーで予期せず失われる可能性があります。

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a container resolver closure into the service that always resolves the current container instance: -->
回避策として、バインディングをシングルトンとして登録するのを停止するか、現在のコンテナ インスタンスを常に解決するサービスにコンテナ リゾルバ クロージャを挿入することができます。

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

<!-- The global `app` helper and the `Container::getInstance()` method will always return the latest version of the application container. -->
グローバル `app` ヘルパと `Container::getInstance()` メソッドは、常にアプリケーション コンテナーの最新バージョンを返します。

<a name="request-injection"></a>
<!-- ### Request Injection -->
### Request Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire request instance into an object that is bound as a singleton: -->
一般に、アプリケーション サービスコンテナまたは HTTP リクエスト インスタンスを他のオブジェクトのコンストラクターに挿入することは避けてください。たとえば、次のバインディングは、リクエスト インスタンス全体をシングルトンとしてバインドされたオブジェクトに挿入します。

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the HTTP request will be injected into the service and that same request will be held by the `Service` instance on subsequent requests. Therefore, all headers, input, and query string data will be incorrect, as well as all other request data. -->
この例では、アプリケーションの起動プロセス中に `Service` インスタンスが解決されると、HTTP リクエストがサービスに挿入され、その同じリクエストは後続のリクエストで `Service` インスタンスによって保持されます。したがって、すべてのヘッダー、入力、およびクエリ文字列データは、他のすべてのリクエスト データと同様に不正になります。

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a request resolver closure into the service that always resolves the current request instance. Or, the most recommended approach is simply to pass the specific request information your object needs to one of the object's methods at runtime: -->
回避策として、バインディングをシングルトンとして登録するのを停止するか、現在のリクエスト インスタンスを常に解決するリクエスト リゾルバー クロージャをサービスに挿入することができます。または、最も推奨されるアプローチは、オブジェクトが必要とする特定のリクエスト情報を実行時にオブジェクトのメソッドの 1 つに単純に渡すことです。

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```

<!-- The global `request` helper will always return the request the application is currently handling and is therefore safe to use within your application. -->
グローバル `request` ヘルパは、アプリケーションが現在処理しているリクエストを常に返すため、アプリケーション内で安全に使用できます。

> [!WARNING]
> コントローラのメソッドとルート クロージャで `Illuminate\Http\Request` インスタンスをタイプヒントすることは許容されます。

<a name="configuration-repository-injection"></a>
<!-- ### Configuration Repository Injection -->
### Configuration Repository Injection

<!-- In general, you should avoid injecting the configuration repository instance into the constructors of other objects. For example, the following binding injects the configuration repository into an object that is bound as a singleton: -->
一般に、構成リポジトリ インスタンスを他のオブジェクトのコンストラクターに挿入することは避けてください。たとえば、次のバインディングは、シングルトンとしてバインドされているオブジェクトに構成リポジトリを挿入します。

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```

<!-- In this example, if the configuration values change between requests, that service will not have access to the new values because it's depending on the original repository instance. -->
この例では、リクエスト間で構成値が変更された場合、そのサービスは元のリポジトリ インスタンスに依存しているため、新しい値にアクセスできなくなります。

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a configuration repository resolver closure to the class: -->
回避策として、バインディングをシングルトンとして登録するのを停止するか、構成リポジトリ リゾルバー クロージャをクラスに挿入することができます。

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

<!-- The global `config` will always return the latest version of the configuration repository and is therefore safe to use within your application. -->
グローバル `config` は常に最新バージョンの構成リポジトリを返すため、アプリケーション内で安全に使用できます。

<a name="managing-memory-leaks"></a>
<!-- ### Managing Memory Leaks -->
### Managing Memory Leaks

<!-- Remember, Octane keeps your application in memory between requests; therefore, adding data to a statically maintained array will result in a memory leak. For example, the following controller has a memory leak since each request to the application will continue to add data to the static `$data` array: -->
Octane はリクエスト間でアプリケーションをメモリに保持することに注意してください。したがって、静的に維持される配列にデータを追加すると、メモリ リークが発生します。たとえば、次のコントローラでは、アプリケーションへの各リクエストが静的 `$data` 配列にデータを追加し続けるため、メモリ リークが発生します。

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```

<!-- While building your application, you should take special care to avoid creating these types of memory leaks. It is recommended that you monitor your application's memory usage during local development to ensure you are not introducing new memory leaks into your application. -->
アプリケーションを構築するときは、このような種類のメモリ リークが発生しないように特別な注意を払う必要があります。ローカル開発中にアプリケーションのメモリ使用量を監視し、アプリケーションに新たなメモリ リークが発生していないことを確認することをお勧めします。

<a name="concurrent-tasks"></a>
<!-- ## Concurrent Tasks -->
## Concurrent Tasks

> [!WARNING]
> この機能には [Swoole](#swoole) が必要です。

<!-- When using Swoole, you may execute operations concurrently via light-weight background tasks. You may accomplish this using Octane's `concurrently` method. You may combine this method with PHP array destructuring to retrieve the results of each operation: -->
Swoole を使用する場合、軽量のバックグラウンド タスクを介して操作を同時に実行できます。これは、Octane の `concurrently` メソッドを使用して実現できます。このメソッドと PHP 配列の構造化を組み合わせて、各操作の結果を取得できます。

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

<!-- Concurrent tasks processed by Octane utilize Swoole's "task workers", and execute within an entirely different process than the incoming request. The amount of workers available to process concurrent tasks is determined by the `--task-workers` directive on the `octane:start` command: -->
Octane によって処理される同時タスクは Swoole の「タスク ワーカー」を利用し、受信リクエストとはまったく異なるプロセス内で実行されます。同時タスクの処理に使用できるワーカーの数は、`octane:start` コマンドの `--task-workers` ディレクティブによって決まります。

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<!-- When invoking the `concurrently` method, you should not provide more than 1024 tasks due to limitations imposed by Swoole's task system. -->
`concurrently` メソッドを呼び出すときは、Swoole のタスク システムによる制限のため、1024 を超えるタスクを指定しないでください。

<a name="ticks-and-intervals"></a>
<!-- ## Ticks and Intervals -->
## Ticks and Intervals

> [!WARNING]
> この機能には [Swoole](#swoole) が必要です。

<!-- When using Swoole, you may register "tick" operations that will be executed every specified number of seconds. You may register "tick" callbacks via the `tick` method. The first argument provided to the `tick` method should be a string that represents the name of the ticker. The second argument should be a callable that will be invoked at the specified interval. -->
Swooleを使用する場合、指定した秒数ごとに実行される「ティック」操作を登録できます。 `tick` メソッドを介して「ティック」コールバックを登録できます。 `tick` メソッドに指定される最初の引数は、ティッカーの名前を表す文字列である必要があります。 2 番目の引数は、指定された間隔で呼び出される呼び出し可能引数である必要があります。

<!-- In this example, we will register a closure to be invoked every 10 seconds. Typically, the `tick` method should be called within the `boot` method of one of your application's service providers: -->
この例では、10 秒ごとに呼び出されるクロージャを登録します。通常、`tick` メソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で呼び出す必要があります。

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

<!-- Using the `immediate` method, you may instruct Octane to immediately invoke the tick callback when the Octane server initially boots, and every N seconds thereafter: -->
`immediate` メソッドを使用すると、Octane サーバーの最初の起動時とその後の N 秒ごとにティック コールバックをすぐに呼び出すように Octane に指示できます。

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
<!-- ## The Octane Cache -->
## The Octane Cache

> [!WARNING]
> この機能には [Swoole](#swoole) が必要です。

<!-- When using Swoole, you may leverage the Octane cache driver, which provides read and write speeds of up to 2 million operations per second. Therefore, this cache driver is an excellent choice for applications that need extreme read / write speeds from their caching layer. -->
Swoole を使用する場合は、1 秒あたり最大 200 万回の読み取りおよび書き込み速度を提供する Octane キャッシュ ドライバを利用できます。したがって、このキャッシュ ドライバは、キャッシュ層から​​の非常に高い読み取り/書き込み速度を必要とするアプリケーションにとって優れた選択肢です。

<!-- This cache driver is powered by [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). All data stored in the cache is available to all workers on the server. However, the cached data will be flushed when the server is restarted: -->
このキャッシュ ドライバは [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table) によって動作します。キャッシュに保存されているすべてのデータは、サーバー上のすべてのワーカーが利用できます。ただし、キャッシュされたデータはサーバーが再起動されるとフラッシュされます。

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane キャッシュで許可されるエントリの最大数は、アプリケーションの `octane` 構成ファイルで定義できます。

<a name="cache-intervals"></a>
<!-- ### Cache Intervals -->
### Cache Intervals

<!-- In addition to the typical methods provided by Laravel's cache system, the Octane cache driver features interval based caches. These caches are automatically refreshed at the specified interval and should be registered within the `boot` method of one of your application's service providers. For example, the following cache will be refreshed every five seconds: -->
Laravel のキャッシュ システムによって提供される一般的なメソッドに加えて、Octane キャッシュ ドライバは間隔ベースのキャッシュを備えています。これらのキャッシュは指定された間隔で自動的に更新され、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内に登録する必要があります。たとえば、次のキャッシュは 5 秒ごとに更新されます。

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

> [!WARNING]
> この機能には [Swoole](#swoole) が必要です。

<!-- When using Swoole, you may define and interact with your own arbitrary [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). Swoole tables provide extreme performance throughput and the data in these tables can be accessed by all workers on the server. However, the data within them will be lost when the server is restarted. -->
Swoole を使用する場合、独自の任意の [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table) を定義して操作できます。 Swoole テーブルは優れたパフォーマンス スループットを提供し、これらのテーブル内のデータにはサーバー上のすべてのワーカーがアクセスできます。ただし、サーバーを再起動すると、その中のデータは失われます。

<!-- Tables should be defined within the `tables` configuration array of your application's `octane` configuration file. An example table that allows a maximum of 1000 rows is already configured for you. The maximum size of string columns may be configured by specifying the column size after the column type as seen below: -->
テーブルは、アプリケーションの `octane` 構成ファイルの `tables` 構成配列内で定義する必要があります。最大 1000 行を許可するテーブルの例は、すでに構成されています。文字列列の最大サイズは、以下に示すように列タイプの後に列サイズを指定することで構成できます。

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

<!-- To access a table, you may use the `Octane::table` method: -->
テーブルにアクセスするには、`Octane::table` メソッドを使用できます。

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole テーブルでサポートされている列タイプは、`string`、`int`、および `float` です。
