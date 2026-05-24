# Laravel Octane (Laravel Octane)

- [Introduction](#introduction)
- [Installation](#installation)
- [サーバーの前提条件](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [アプリケーションの提供](#serving-your-application)
    - [HTTPS 経由でアプリケーションを提供する](#serving-your-application-via-https)
    - [Nginx 経由でアプリケーションを提供する](#serving-your-application-via-nginx)
    - [ファイルの変更を監視する](#watching-for-file-changes)
    - [ワーカー数の指定](#specifying-the-worker-count)
    - [最大リクエスト数の指定](#specifying-the-max-request-count)
    - [労働者をリロードする](#reloading-the-workers)
    - [サーバーの停止](#stopping-the-server)
- [依存関係の注入とOctane](#dependency-injection-and-octane)
    - [コンテナインジェクション](#container-injection)
    - [インジェクションのリクエスト](#request-injection)
    - [構成リポジトリのインジェクション](#configuration-repository-injection)
- [メモリ リークの管理](#managing-memory-leaks)
- [同時タスク](#concurrent-tasks)
- [ティックと間隔](#ticks-and-intervals)
- [Octaneキャッシュ](#the-octane-cache)
- [Tables](#tables)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Octane](https://github.com/laravel/octane) は、[Open Swoole](https://swoole.co.uk)、[Swoole](https://github.com/swoole/swoole-src)、[RoadRunner](https://roadrunner.dev) などの高性能アプリケーション サーバーを使用してアプリケーションを提供することにより、アプリケーションのパフォーマンスを大幅に向上させます。 Octane はアプリケーションを一度起動してメモリに保持し、超音速でリクエストを送ります。

<a name="installation"></a>
## インストール (Installation)

Octane は Composer パッケージ マネージャー経由でインストールできます。

```shell
composer require laravel/octane
```

Octane をインストールした後、`octane:install` Artisan コマンドを実行すると、Octane の構成ファイルがアプリケーションにインストールされます。

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## サーバーの前提条件 (Server Prerequisites)

> **警告**
> Laravel Octaneには[PHP8.0以上](https://php.net/releases/)が必要です。

<a name="roadrunner"></a>
### ロードランナー

[RoadRunner](https://roadrunner.dev) は、Go を使用して構築された RoadRunner バイナリを利用しています。 RoadRunner ベースの Octane サーバーを初めて起動すると、Octane は RoadRunner バイナリのダウンロードとインストールを提案します。

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail 経由の RoadRunner

[Laravel Sail](/docs/{{version}}/sail) を使用してアプリケーションを開発する場合は、次のコマンドを実行して Octane と RoadRunner をインストールする必要があります。

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

次に、Sail シェルを起動し、`rr` 実行可能ファイルを使用して、RoadRunner バイナリの最新の Linux ベース ビルドを取得する必要があります。

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

RoadRunner バイナリをインストールした後、Sail Shell セッションを終了できます。アプリケーションを実行し続けるために、Sail で使用される `supervisor.conf` ファイルを調整する必要があります。開始するには、`sail:publish` Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan sail:publish
```

次に、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供できるように、アプリケーションの `docker/supervisord.conf` ファイルの `command` ディレクティブを更新します。

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80
```

最後に、`rr` バイナリが実行可能であることを確認し、Sail イメージをビルドします。

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole アプリケーションサーバーを使用して Laravel Octane アプリケーションを提供する場合は、Swoole PHP 拡張機能をインストールする必要があります。通常、これは PECL 経由で実行できます。

```shell
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail経由のSwoole

> **警告**
> Sail 経由で Octane アプリケーションを提供する前に、Laravel Sail が最新バージョンであることを確認し、アプリケーションのルート ディレクトリ内で `./vendor/bin/sail build --no-cache` を実行してください。

あるいは、Laravel の公式 Docker ベース開発環境である [Laravel Sail](/docs/{{version}}/sail) を使用して、Swoole ベースの Octane アプリケーションを開発することもできます。 Laravel Sail にはデフォルトで Swoole 拡張機能が含まれています。ただし、アプリケーションの実行を継続するには、Sail で使用される `supervisor.conf` ファイルを調整する必要があります。開始するには、`sail:publish` Artisan コマンドを実行します。

```shell
./vendor/bin/sail artisan sail:publish
```

次に、Sail が PHP 開発サーバーの代わりに Octane を使用してアプリケーションを提供できるように、アプリケーションの `docker/supervisord.conf` ファイルの `command` ディレクティブを更新します。

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

最後に、Sail イメージを構築します。

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swooleの構成

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
## アプリケーションの提供 (Serving Your Application)

Octane サーバーは、`octane:start` Artisan コマンドを使用して起動できます。デフォルトでは、このコマンドは、アプリケーションの `octane` 構成ファイルの `server` 構成オプションで指定されたサーバーを利用します。

```shell
php artisan octane:start
```

デフォルトでは、Octane はポート 8000 でサーバーを起動するため、`http://localhost:8000` を介して Web ブラウザでアプリケーションにアクセスできます。

<a name="serving-your-application-via-https"></a>
### HTTPS 経由でアプリケーションを提供する

デフォルトでは、Octane 経由で実行されるアプリケーションは、`http://` というプレフィックスが付いたリンクを生成します。アプリケーションの `config/octane.php` 構成ファイル内で使用される `OCTANE_HTTPS` 環境変数は、HTTPS 経由でアプリケーションを提供するときに `true` に設定できます。この設定値が `true` に設定されている場合、Octane は、生成されたすべてのリンクに `https://` というプレフィックスを付けるように Laravel に指示します。

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx 経由でアプリケーションを提供する

> **注記**
> 独自のサーバー構成を管理する準備がまだ整っていない場合、または堅牢な Laravel Octane アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、[Laravel Forge](https://forge.laravel.com) を確認してください。

運用環境では、Nginx や Apache などの従来の Web サーバーの背後で Octane アプリケーションを提供する必要があります。これにより、Web サーバーが画像やスタイルシートなどの静的資産を提供したり、SSL 証明書の終了を管理したりできるようになります。

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
### ファイルの変更を監視する

アプリケーションは Octane サーバーの起動時に一度メモリに読み込まれるため、ブラウザを更新してもアプリケーションのファイルへの変更は反映されません。たとえば、`routes/web.php` ファイルに追加されたルート定義は、サーバーが再起動されるまで反映されません。便宜上、`--watch` フラグを使用して、アプリケーション内のファイル変更時にサーバーを自動的に再起動するように Octane に指示できます。

```shell
php artisan octane:start --watch
```

この機能を使用する前に、[Node](https://nodejs.org) がローカル開発環境にインストールされていることを確認する必要があります。さらに、プロジェクト内に [Chokidar](https://github.com/paulmillr/chokidar) ファイル監視ライブラリをインストールする必要があります。

```shell
npm install --save-dev chokidar
```

アプリケーションの `config/octane.php` 構成ファイル内の `watch` 構成オプションを使用して、監視する必要があるディレクトリとファイルを構成できます。

<a name="specifying-the-worker-count"></a>
### ワーカー数の指定

デフォルトでは、Octane はマシンが提供する各 CPU コアに対してアプリケーション リクエスト ワーカーを開始します。これらのワーカーは、アプリケーションに入ってくる受信 HTTP リクエストを処理するために使用されます。 `octane:start` コマンドを呼び出すときに、`--workers` オプションを使用して、開始するワーカーの数を手動で指定できます。

```shell
php artisan octane:start --workers=4
```

Swoole アプリケーション サーバーを使用している場合は、起動する [「タスクワーカー」](#concurrent-tasks) の数を指定することもできます。

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 最大リクエスト数の指定

漂遊メモリ リークを防ぐために、Octane は 500 件のリクエストを処理した後、ワーカーを正常に再起動します。この数値を調整するには、`--max-requests` オプションを使用できます。

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
### 労働者をリロードする

`octane:reload` コマンドを使用して、Octane サーバーのアプリケーション ワーカーを正常に再起動できます。通常、これは、新しくデプロイされたコードがメモリにロードされ、後続のリクエストに対応するために使用されるように、デプロイ後に実行する必要があります。

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### サーバーの停止

`octane:stop` Artisan コマンドを使用して、Octane サーバーを停止できます。

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### サーバーのステータスを確認する

`octane:status` Artisan コマンドを使用して、Octane サーバーの現在のステータスを確認できます。

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 依存関係の注入とOctane (Dependency Injection & Octane)

Octane はアプリケーションを一度起動し、リクエストを処理する間メモリ内に保持するため、アプリケーションを構築する際に考慮すべき注意事項がいくつかあります。たとえば、アプリケーションのサービスプロバイダの `register` メソッドと `boot` メソッドは、リクエスト ワーカーが最初に起動するときに 1 回だけ実行されます。後続のリクエストでは、同じアプリケーション インスタンスが再利用されます。

これを考慮して、アプリケーション サービスコンテナまたはリクエストをオブジェクトのコンストラクターに挿入するときは、特別な注意を払う必要があります。そうすると、そのオブジェクトには、後続のリクエストでコンテナまたはリクエストの古いバージョンが含まれる可能性があります。

Octane は、リクエスト間のファーストパーティ フレームワークの状態のリセットを自動的に処理します。ただし、Octane は、アプリケーションによって作成されたグローバル状態をリセットする方法を常に知っているわけではありません。したがって、Octane に適した方法でアプリケーションを構築する方法を認識する必要があります。以下では、Octane の使用中に問題が発生する可能性のある最も一般的な状況について説明します。

<a name="container-injection"></a>
### コンテナインジェクション

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

この例では、アプリケーションの起動プロセス中に `Service` インスタンスが解決されると、コンテナーがサービスに挿入され、その同じコンテナーが後続のリクエストで `Service` インスタンスによって保持されます。これは、特定のアプリケーションでは問題にならない可能性があります。ただし、ブート サイクルの後半または後続のリクエストによって追加されたバインディングがコンテナーで予期せず失われる可能性があります。

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

グローバル `app` ヘルパと `Container::getInstance()` メソッドは、常にアプリケーション コンテナーの最新バージョンを返します。

<a name="request-injection"></a>
### インジェクションのリクエスト

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

この例では、アプリケーションの起動プロセス中に `Service` インスタンスが解決されると、HTTP リクエストがサービスに挿入され、その同じリクエストは後続のリクエストで `Service` インスタンスによって保持されます。したがって、すべてのヘッダー、入力、およびクエリ文字列データは、他のすべてのリクエスト データと同様に不正になります。

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

グローバル `request` ヘルパは、アプリケーションが現在処理しているリクエストを常に返すため、アプリケーション内で安全に使用できます。

> **警告**
> コントローラのメソッドとルート クロージャで `Illuminate\Http\Request` インスタンスをタイプヒントすることは許容されます。

<a name="configuration-repository-injection"></a>
### 構成リポジトリのインジェクション

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

この例では、リクエスト間で構成値が変更された場合、そのサービスは元のリポジトリ インスタンスに依存しているため、新しい値にアクセスできなくなります。

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

グローバル `config` は常に最新バージョンの構成リポジトリを返すため、アプリケーション内で安全に使用できます。

<a name="managing-memory-leaks"></a>
### メモリ リークの管理

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

アプリケーションを構築するときは、このような種類のメモリ リークが発生しないように特別な注意を払う必要があります。ローカル開発中にアプリケーションのメモリ使用量を監視し、アプリケーションに新たなメモリ リークが発生していないことを確認することをお勧めします。

<a name="concurrent-tasks"></a>
## 同時タスク (Concurrent Tasks)

> **警告**
> この機能には [Swoole](#swoole) が必要です。

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

Octane によって処理される同時タスクは Swoole の「タスク ワーカー」を利用し、受信リクエストとはまったく異なるプロセス内で実行されます。同時タスクの処理に使用できるワーカーの数は、`octane:start` コマンドの `--task-workers` ディレクティブによって決まります。

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` メソッドを呼び出すときは、Swoole のタスク システムによる制限のため、1024 を超えるタスクを指定しないでください。

<a name="ticks-and-intervals"></a>
## ティックと間隔 (Ticks & Intervals)

> **警告**
> この機能には [Swoole](#swoole) が必要です。

Swooleを使用する場合、指定した秒数ごとに実行される「ティック」操作を登録できます。 `tick` メソッドを介して「ティック」コールバックを登録できます。 `tick` メソッドに指定される最初の引数は、ティッカーの名前を表す文字列である必要があります。 2 番目の引数は、指定された間隔で呼び出される呼び出し可能引数である必要があります。

この例では、10 秒ごとに呼び出されるクロージャを登録します。通常、`tick` メソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で呼び出す必要があります。

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

`immediate` メソッドを使用すると、Octane サーバーの最初の起動時とその後の N 秒ごとにティック コールバックをすぐに呼び出すように Octane に指示できます。

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
## Octaneキャッシュ (The Octane Cache)

> **警告**
> この機能には [Swoole](#swoole) が必要です。

Swoole を使用する場合は、1 秒あたり最大 200 万回の読み取りおよび書き込み速度を提供する Octane キャッシュ ドライバを利用できます。したがって、このキャッシュ ドライバは、キャッシュ層から​​の非常に高い読み取り/書き込み速度を必要とするアプリケーションにとって優れた選択肢です。

このキャッシュ ドライバは [Swooleテーブル](https://www.swoole.co.uk/docs/modules/swoole-table) によって動作します。キャッシュに保存されているすべてのデータは、サーバー上のすべてのワーカーが利用できます。ただし、キャッシュされたデータはサーバーが再起動されるとフラッシュされます。

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> **注記**
> Octane キャッシュで許可されるエントリの最大数は、アプリケーションの `octane` 構成ファイルで定義できます。

<a name="cache-intervals"></a>
### キャッシュ間隔

Laravel のキャッシュ システムによって提供される一般的なメソッドに加えて、Octane キャッシュ ドライバは間隔ベースのキャッシュを備えています。これらのキャッシュは指定された間隔で自動的に更新され、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内に登録する必要があります。たとえば、次のキャッシュは 5 秒ごとに更新されます。

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## テーブル (Tables)

> **警告**
> この機能には [Swoole](#swoole) が必要です。

Swoole を使用する場合、独自の任意の [Swooleテーブル](https://www.swoole.co.uk/docs/modules/swoole-table) を定義して操作できます。 Swoole テーブルは優れたパフォーマンス スループットを提供し、これらのテーブル内のデータにはサーバー上のすべてのワーカーがアクセスできます。ただし、サーバーを再起動すると、その中のデータは失われます。

テーブルは、アプリケーションの `octane` 構成ファイルの `tables` 構成配列内で定義する必要があります。最大 1000 行を許可するテーブルの例は、すでに構成されています。文字列列の最大サイズは、以下に示すように列タイプの後に列サイズを指定することで構成できます。

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

テーブルにアクセスするには、`Octane::table` メソッドを使用できます。

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> **警告**
> Swoole テーブルでサポートされている列タイプは、`string`、`int`、および `float` です。

