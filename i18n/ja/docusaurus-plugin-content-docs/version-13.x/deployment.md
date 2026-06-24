<!-- # Deployment -->
# Deployment

- [Introduction](#introduction)
- [Server Requirements](#server-requirements)
- [Server Configuration](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [Directory Permissions](#directory-permissions)
- [Optimization](#optimization)
    - [Caching Configuration](#optimizing-configuration-loading)
    - [Caching Events](#caching-events)
    - [Caching Routes](#optimizing-route-loading)
    - [Caching Views](#optimizing-view-loading)
- [Reloading Services](#reloading-services)
- [Debug Mode](#debug-mode)
- [The Health Route](#the-health-route)
- [Deploying With Laravel Cloud or Forge](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you're ready to deploy your Laravel application to production, there are some important things you can do to make sure your application is running as efficiently as possible. In this document, we'll cover some great starting points for making sure your Laravel application is deployed properly. -->
Laravel アプリケーションを本番環境にデプロイする準備ができたら、アプリケーションが可能な限り効率的に実行されるようにするために実行できる重要なことがいくつかあります。このドキュメントでは、Laravel アプリケーションが適切にデプロイされていることを確認するための優れた出発点をいくつか説明します。

<a name="server-requirements"></a>
<!-- ## Server Requirements -->
## Server Requirements

<!-- The Laravel framework has a few system requirements. You should ensure that your web server has the following minimum PHP version and extensions: -->
Laravel フレームワークにはいくつかのシステム要件があります。 Web サーバーに次の最小 PHP バージョンと拡張機能が備わっていることを確認する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- PHP >= 8.3
- Ctype PHP Extension
- cURL PHP Extension
- DOM PHP Extension
- Fileinfo PHP Extension
- Filter PHP Extension
- Hash PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PCRE PHP Extension
- PDO PHP Extension
- Session PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension
-->
- PHP >= 8.3
- Ctype PHP 拡張機能
- cURL PHP 拡張機能
- DOM PHP 拡張機能
- ファイル情報 PHP 拡張機能
- PHP 拡張機能のフィルター
- ハッシュ PHP 拡張機能
- Mbstring PHP 拡張機能
- OpenSSL PHP 拡張機能
- PCRE PHP 拡張機能
- PDO PHP 拡張機能
- セッション PHP 拡張機能
- トークナイザー PHP 拡張機能
- XML PHP 拡張機能

<!-- </div> -->
</div>

<a name="server-configuration"></a>
<!-- ## Server Configuration -->
## Server Configuration

<a name="nginx"></a>
<!-- ### Nginx -->
### Nginx

<!-- If you are deploying your application to a server that is running Nginx, you may use the following configuration file as a starting point for configuring your web server. Most likely, this file will need to be customized depending on your server's configuration. **If you would like assistance in managing your server, consider using a fully-managed Laravel platform like [Laravel Cloud](https://cloud.laravel.com).** -->
Nginx を実行しているサーバーにアプリケーションをデプロイする場合は、Web サーバーを構成する開始点として次の構成ファイルを使用できます。ほとんどの場合、このファイルはサーバーの構成に応じてカスタマイズする必要があります。 **サーバー管理の支援が必要な場合は、[Laravel Cloud](https://cloud.laravel.com) のようなフルマネージド Laravel プラットフォームの使用を検討してください。**

<!-- Please ensure, like the configuration below, your web server directs all requests to your application's `public/index.php` file. You should never attempt to move the `index.php` file to your project's root, as serving the application from the project root will expose many sensitive configuration files to the public Internet: -->
以下の構成のように、Web サーバーがすべてのリクエストをアプリケーションの `public/index.php` ファイルに送信していることを確認してください。プロジェクト ルートからアプリケーションを提供すると、多くの機密設定ファイルがパブリック インターネットに公開されるため、`index.php` ファイルをプロジェクトのルートに移動しないでください。

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="frankenphp"></a>
<!-- ### FrankenPHP -->
### FrankenPHP

<!-- [FrankenPHP](https://frankenphp.dev/) may also be used to serve your Laravel applications. FrankenPHP is a modern PHP application server written in Go. To serve a Laravel PHP application using FrankenPHP, you may simply invoke its `php-server` command: -->
[FrankenPHP](https://frankenphp.dev/) は、Laravel アプリケーションを提供するために使用することもできます。 FrankenPHP は、Go で書かれた最新の PHP アプリケーション サーバーです。 FrankenPHP を使用して Laravel PHP アプリケーションを提供するには、その `php-server` コマンドを呼び出すだけです。

```shell
frankenphp php-server -r public/
```

<!-- To take advantage of more powerful features supported by FrankenPHP, such as its [Laravel Octane](/docs/13.x/octane) integration, HTTP/3, modern compression, or the ability to package Laravel applications as standalone binaries, please consult FrankenPHP's [Laravel documentation](https://frankenphp.dev/docs/laravel/). -->
FrankenPHP がサポートする強力な機能 ([Laravel Octane](/docs/13.x/octane) 統合、HTTP/3、最新の圧縮、Laravel アプリケーションをスタンドアロン バイナリとしてパッケージ化する機能など) を利用するには、FrankenPHP の [Laravel documentation](https://frankenphp.dev/docs/laravel/) を参照してください。

<a name="directory-permissions"></a>
<!-- ### Directory Permissions -->
### Directory Permissions

<!-- Laravel will need to write to the `bootstrap/cache` and `storage` directories, so you should ensure the web server process owner has permission to write to these directories. -->
Laravel は `bootstrap/cache` および `storage` ディレクトリに書き込む必要があるため、Web サーバーのプロセス所有者にこれらのディレクトリへの書き込み権限があることを確認する必要があります。

<a name="optimization"></a>
<!-- ## Optimization -->
## Optimization

<!-- When deploying your application to production, there are a variety of files that should be cached, including your configuration, events, routes, and views. Laravel provides a single, convenient `optimize` Artisan command that will cache all of these files. This command should typically be invoked as part of your application's deployment process: -->
アプリケーションを実稼働環境にデプロイする場合、構成、イベント、ルート、ビューなど、さまざまなファイルをキャッシュする必要があります。 Laravel は、これらすべてのファイルをキャッシュする単一の便利な `optimize` Artisan コマンドを提供します。このコマンドは通常、アプリケーションの展開プロセスの一部として呼び出す必要があります。

```shell
php artisan optimize
```

<!-- The `optimize:clear` method may be used to remove all of the cache files generated by the `optimize` command as well as all keys in the default cache driver: -->
`optimize:clear` メソッドは、`optimize` コマンドによって生成されたすべてのキャッシュ ファイルと、デフォルトのキャッシュ ドライバ内のすべてのキーを削除するために使用できます。

```shell
php artisan optimize:clear
```

<!-- In the following documentation, we will discuss each of the granular optimization commands that are executed by the `optimize` command. -->
次のドキュメントでは、`optimize` コマンドによって実行される詳細な最適化コマンドのそれぞれについて説明します。

<a name="optimizing-configuration-loading"></a>
<!-- ### Caching Configuration -->
### Caching Configuration

<!-- When deploying your application to production, you should make sure that you run the `config:cache` Artisan command during your deployment process: -->
アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `config:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan config:cache
```

<!-- This command will combine all of Laravel's configuration files into a single, cached file, which greatly reduces the number of trips the framework must make to the filesystem when loading your configuration values. -->
このコマンドは、Laravel のすべての設定ファイルを単一のキャッシュされたファイルに結合します。これにより、設定値をロードするときにフレームワークがファイルシステムにアクセスする必要がある回数が大幅に削減されます。

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされなくなり、`.env` 変数に対する `env` 関数の呼び出しはすべて `null` を返します。

<a name="caching-events"></a>
<!-- ### Caching Events -->
### Caching Events

<!-- You should cache your application's auto-discovered event to listener mappings during your deployment process. This can be accomplished by invoking the `event:cache` Artisan command during deployment: -->
デプロイメントプロセス中に、アプリケーションの自動検出イベントとリスナのマッピングをキャッシュする必要があります。これは、デプロイメント中に `event:cache` Artisan コマンドを呼び出すことで実現できます。

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
<!-- ### Caching Routes -->
### Caching Routes

<!-- If you are building a large application with many routes, you should make sure that you are running the `route:cache` Artisan command during your deployment process: -->
多くのルートを持つ大規模なアプリケーションを構築している場合は、デプロイメント プロセス中に `route:cache` Artisan コマンドを実行していることを確認する必要があります。

```shell
php artisan route:cache
```

<!-- This command reduces all of your route registrations into a single method call within a cached file, improving the performance of route registration when registering hundreds of routes. -->
このコマンドにより、すべてのルート登録がキャッシュされたファイル内の 1 つのメソッド呼び出しに減らされ、数百のルートを登録する場合のルート登録のパフォーマンスが向上します。

<a name="optimizing-view-loading"></a>
<!-- ### Caching Views -->
### Caching Views

<!-- When deploying your application to production, you should make sure that you run the `view:cache` Artisan command during your deployment process: -->
アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `view:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan view:cache
```

<!-- This command precompiles all your Blade views so they are not compiled on demand, improving the performance of each request that returns a view. -->
このコマンドは、すべての Blade ビューをプリコンパイルするので、オンデマンドでコンパイルされなくなり、ビューを返す各リクエストのパフォーマンスが向上します。

<a name="reloading-services"></a>
<!-- ## Reloading Services -->
## Reloading Services

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com) にデプロイする場合、すべてのサービスの正常なリロードが自動的に処理されるため、`reload` コマンドを使用する必要はありません。

<!-- After deploying a new version of your application, any long-running services such as queue workers, Laravel Reverb, or Laravel Octane should be reloaded / restarted to use the new code. Laravel provides a single `reload` Artisan command that will terminate these services: -->
アプリケーションの新しいバージョンをデプロイした後、キューワーカー、Laravel Reverb、Laravel Octane などの長時間実行されるサービスは、新しいコードを使用するために再ロード/再起動する必要があります。 Laravel は、これらのサービスを終了する単一の `reload` Artisan コマンドを提供します。

```shell
php artisan reload
```

<!-- If you are not using [Laravel Cloud](https://cloud.laravel.com), you should manually configure a process monitor that can detect when your reloadable processes exit and automatically restart them. -->
[Laravel Cloud](https://cloud.laravel.com) を使用していない場合は、リロード可能なプロセスの終了を検出し、自動的に再起動できるプロセス モニターを手動で構成する必要があります。

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The debug option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your application's `.env` file. -->
`config/app.php` 構成ファイルのデバッグ オプションにより、エラーに関する情報が実際にユーザーにどの程度表示されるかが決まります。デフォルトでは、このオプションは、アプリケーションの `.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

> [!WARNING]
> **運用環境では、この値は常に `false` である必要があります。本番環境で `APP_DEBUG` 変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="the-health-route"></a>
<!-- ## The Health Route -->
## The Health Route

<!-- Laravel includes a built-in health check route that can be used to monitor the status of your application. In production, this route may be used to report the status of your application to an uptime monitor, load balancer, or orchestration system such as Kubernetes. -->
Laravel には、アプリケーションのステータスを監視するために使用できる組み込みのヘルスチェック ルートが含まれています。運用環境では、このルートを使用して、アプリケーションのステータスを稼働時間モニター、ロード バランサー、または Kubernetes などのオーケストレーション システムに報告することができます。

<!-- By default, the health check route is served at `/up` and will return a 200 HTTP response if the application has booted without exceptions. Otherwise, a 500 HTTP response will be returned. You may configure the URI for this route in your application's `bootstrap/app` file: -->
デフォルトでは、ヘルスチェックルートは `/up` で提供され、アプリケーションが例外なく起動した場合は 200 HTTP 応答を返します。それ以外の場合は、500 HTTP 応答が返されます。アプリケーションの `bootstrap/app` ファイルでこのルートの URI を構成できます。

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

<!-- When HTTP requests are made to this route, Laravel will also dispatch a `Illuminate\Foundation\Events\DiagnosingHealth` event, allowing you to perform additional health checks relevant to your application. Within a [listener](/docs/13.x/events) for this event, you may check your application's database or cache status. If you detect a problem with your application, you may simply throw an exception from the listener. -->
このルートに対して HTTP リクエストが行われると、Laravel は `Illuminate\Foundation\Events\DiagnosingHealth` イベントも送出し、アプリケーションに関連する追加のヘルスチェックを実行できるようにします。このイベントの [listener](/docs/13.x/events) 内で、アプリケーションのデータベースまたはキャッシュのステータスを確認できます。アプリケーションに問題が検出された場合は、リスナから例外をスローするだけで済みます。

<a name="deploying-with-cloud-or-forge"></a>
<!-- ## Deploying With Laravel Cloud or Forge -->
## Deploying With Laravel Cloud or Forge

<a name="laravel-cloud"></a>
<!-- #### Laravel Cloud -->
#### Laravel Cloud

<!-- If you would like a fully-managed, auto-scaling deployment platform tuned for Laravel, check out [Laravel Cloud](https://cloud.laravel.com). Laravel Cloud is a robust deployment platform for Laravel, offering managed compute, databases, caches, and object storage. -->
Laravel 用に調整されたフルマネージドの自動スケーリング展開プラットフォームが必要な場合は、[Laravel Cloud](https://cloud.laravel.com) をチェックしてください。 Laravel Cloud は、マネージド コンピューティング、データベース、キャッシュ、オブジェクト ストレージを提供する、Laravel の堅牢なデプロイメント プラットフォームです。

<!-- Launch your Laravel application on Cloud and fall in love with the scalable simplicity. Laravel Cloud is fine-tuned by Laravel's creators to work seamlessly with the framework so you can keep writing your Laravel applications exactly like you're used to. -->
Laravel アプリケーションをクラウド上で起動して、スケーラブルなシンプルさに夢中になってください。 Laravel Cloud は、フレームワークとシームレスに連携できるように Laravel の作成者によって微調整されているため、これまでとまったく同じように Laravel アプリケーションを書き続けることができます。

<a name="laravel-forge"></a>
<!-- #### Laravel Forge -->
#### Laravel Forge

<!-- If you prefer to manage your own servers but aren't comfortable configuring all of the various services needed to run a robust Laravel application, [Laravel Forge](https://forge.laravel.com) is a VPS server management platform for Laravel applications. -->
独自のサーバーを管理したいが、堅牢な Laravel アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、Laravel アプリケーション用の VPS サーバー管理プラットフォームである [Laravel Forge](https://forge.laravel.com) を使用してください。

<!-- Laravel Forge can create servers on various infrastructure providers such as DigitalOcean, Linode, AWS, and more. In addition, Forge installs and manages all of the tools needed to build robust Laravel applications, such as Nginx, MySQL, Redis, Memcached, Beanstalk, and more. -->
Laravel Forge は、DigitalOcean、Linode、AWS などのさまざまなインフラストラクチャプロバイダ上にサーバーを作成できます。さらに、Forge は、Nginx、MySQL、Redis、Memcached、Beanstalk など、堅牢な Laravel アプリケーションの構築に必要なすべてのツールをインストールして管理します。

