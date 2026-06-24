<!-- # Laravel Octane -->
# Laravel Octane

- [Introduction](#introduction)
- [Installation](#installation)
- [Server Prerequisites](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Serving Your Application](#serving-your-application)
    - [Serving Your Application Via HTTPS](#serving-your-application-via-https)
    - [Serving Your Application Via Nginx](#serving-your-application-via-nginx)
    - [Watching For File Changes](#watching-for-file-changes)
    - [Specifying The Worker Count](#specifying-the-worker-count)
    - [Specifying The Max Request Count](#specifying-the-max-request-count)
    - [Reloading The Workers](#reloading-the-workers)
    - [Stopping The Server](#stopping-the-server)
- [Dependency Injection & Octane](#dependency-injection-and-octane)
    - [Container Injection](#container-injection)
    - [Request Injection](#request-injection)
    - [Configuration Repository Injection](#configuration-repository-injection)
- [Managing Memory Leaks](#managing-memory-leaks)
- [Concurrent Tasks](#concurrent-tasks)
- [Ticks & Intervals](#ticks-and-intervals)
- [The Octane Cache](#the-octane-cache)
- [Tables](#tables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Octane](https://github.com/laravel/octane) supercharges your application's performance by serving your application using high-powered application servers, including [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), and [RoadRunner](https://roadrunner.dev). Octane boots your application once, keeps it in memory, and then feeds it requests at supersonic speeds. -->
[Laravel Octane](https://github.com/laravel/octane) は、[Open Swoole](https://swoole.co.uk)、[Swoole](https://github.com/swoole/swoole-src)、[RoadRunner](https://roadrunner.dev) などの高性能アプリケーション サーバーを使用してアプリケーションを提供することにより、アプリケーションのパフォーマンスを大幅に向上させます。 Octane はアプリケーションを一度起動してメモリに保持し、超音速でリクエストを送ります。

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

> [!WARNING]
> Laravel Octaneには[PHP 8.0+](https://php.net/releases/)が必要です。

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev) は、Go を使用して構築された RoadRunner バイナリを利用しています。 RoadRunner ベースの Octane サーバーを初めて起動すると、Octane は RoadRunner バイナリのダウンロードとインストールを提案します。

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner Via Laravel Sail -->
#### RoadRunner Via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/9.x/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/9.x/sail) を使用してアプリケーションを開発する場合は、次のコマンドを実行して Octane と RoadRunner をインストールする必要があります。

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
次に、Sail シェルを起動し、`rr` 実行可能ファイルを使用して、RoadRunner バイナリの最新の Linux ベース ビルドを取得する必要があります。

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- After installing the RoadRunner binary, you may exit your Sail shell session. You will now need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
RoadRunner バイナリをインストールした後、Sail Shell セッションを終了できます。アプリケーションを実行し続けるために、Sail で使用される `supervisor.conf` ファイルを調整する必要があります。開始するには、`sail:publish` Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
次に、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供できるように、アプリケーションの `docker/supervisord.conf` ファイルの `command` ディレクティブを更新します。

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80
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

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole Via Laravel Sail -->
#### Swoole Via Laravel Sail

> [!WARNING]
> Sail 経由で Octane アプリケーションを提供する前に、Laravel Sail が最新バージョンであることを確認し、アプリケーションのルート ディレクトリ内で `./vendor/bin/sail build --no-cache` を実行してください。

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/9.x/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
あるいは、Laravel の公式 Docker ベース開発環境である [Laravel Sail](/docs/9.x/sail) を使用して、Swoole ベースの Octane アプリケーションを開発することもできます。 Laravel Sail にはデフォルトで Swoole 拡張機能が含まれています。ただし、アプリケーションの実行を継続するには、Sail で使用される `supervisor.conf` ファイルを調整する必要があります。開始するには、`sail:publish` Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
次に、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供できるように、アプリケーションの `docker/supervisord.conf` ファイルの `command` ディレクティブを更新します。

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
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

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application Via HTTPS -->
### Serving Your Application Via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
デフォルトでは、Octane 経由で実行されるアプリケーションは、`http://` というプレフィックスが付いたリンクを生成します。アプリケーションの `config/octane.php` 構成ファイル内で使用される `OCTANE_HTTPS` 環境変数は、HTTPS 経由でアプリケーションを提供するときに `true` に設定できます。この設定値が `true` に設定されている場合、Octane は、生成されたすべてのリンクに `https://` というプレフィックスを付けるように Laravel に指示します。

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application Via Nginx -->
### Serving Your Application Via Nginx

> [!NOTE]
> 独自のサーバー構成を管理する準備がまだ整っていない場合、または堅牢な Laravel Octane アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、[Laravel Forge](https://forge.laravel.com) を確認してください。

<!-- In production environments, you should serve your Octane application behind a traditional web server such as a Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
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
<!-- ### Watching For File Changes -->
### Watching For File Changes

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
<!-- ### Specifying The Worker Count -->
### Specifying The Worker Count

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
<!-- ### Specifying The Max Request Count -->
### Specifying The Max Request Count

<!-- To help prevent stray memory leaks, Octane gracefully restarts any worker once it has handled 500 requests. To adjust this number, you may use the `--max-requests` option: -->
漂遊メモリ リークを防ぐために、Octane は 500 件のリクエストを処理した後、ワーカーを正常に再起動します。この数値を調整するには、`--max-requests` オプションを使用できます。

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
<!-- ### Reloading The Workers -->
### Reloading The Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
`octane:reload` コマンドを使用して、Octane サーバーのアプリケーション ワーカーを正常に再起動できます。通常、これは、新しくデプロイされたコードがメモリにロードされ、後続のリクエストに対応するために使用されるように、デプロイ後に実行する必要があります。

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping The Server -->
### Stopping The Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
`octane:stop` Artisan コマンドを使用して、Octane サーバーを停止できます。

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking The Server Status -->
#### Checking The Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
`octane:status` Artisan コマンドを使用して、Octane サーバーの現在のステータスを確認できます。

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection & Octane -->
## Dependency Injection & Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane はアプリケーションを一度起動し、リクエストを処理する間メモリ内に保持するため、アプリケーションを構築する際に考慮すべき注意事項がいくつかあります。たとえば、アプリケーションのサービスプロバイダの `register` メソッドと `boot` メソッドは、リクエスト ワーカーが最初に起動するときに 1 回だけ実行されます。後続のリクエストでは、同じアプリケーション インスタンスが再利用されます。

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a  stale version of the container or request on subsequent requests. -->
これを考慮して、アプリケーション サービスコンテナまたはリクエストをオブジェクトのコンストラクターに挿入するときは、特別な注意を払う必要があります。そうすると、そのオブジェクトには、後続のリクエストでコンテナまたはリクエストの古いバージョンが含まれる可能性があります。

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Octane は、リクエスト間のファーストパーティ フレームワークの状態のリセットを自動的に処理します。ただし、Octane は、アプリケーションによって作成されたグローバル状態をリセットする方法を常に知っているわけではありません。したがって、Octane に適した方法でアプリケーションを構築する方法を認識する必要があります。以下では、Octane の使用中に問題が発生する可能性のある最も一般的な状況について説明します。

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
一般に、アプリケーション サービスコンテナまたは HTTP リクエスト インスタンスを他のオブジェクトのコンストラクターに挿入することは避けてください。たとえば、次のバインディングは、アプリケーション サービスコンテナ全体をシングルトンとしてバインドされたオブジェクトに挿入します。

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
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

$this->app->bind(Service::class, function ($app) {
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

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
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

$this->app->bind(Service::class, function ($app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function ($app) {
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

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
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

$this->app->bind(Service::class, function ($app) {
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
 *
 * @param  \Illuminate\Http\Request  $request
 * @return void
 */
public function index(Request $request)
{
    Service::$data[] = Str::random(10);

    // ...
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
<!-- ## Ticks & Intervals -->
## Ticks & Intervals

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

