# 導入 (Deployment)

- [Introduction](#introduction)
- [サーバー要件](#server-requirements)
- [サーバー構成](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [ディレクトリのアクセス許可](#directory-permissions)
- [Optimization](#optimization)
    - [キャッシュ構成](#optimizing-configuration-loading)
    - [イベントのキャッシュ](#caching-events)
    - [キャッシュルート](#optimizing-route-loading)
    - [ビューのキャッシュ](#optimizing-view-loading)
- [サービスをリロードしています](#reloading-services)
- [デバッグモード](#debug-mode)
- [健康ルート](#the-health-route)
- [Laravel Cloud または Forge を使用したデプロイ](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel アプリケーションを本番環境にデプロイする準備ができたら、アプリケーションが可能な限り効率的に実行されるようにするために実行できる重要なことがいくつかあります。このドキュメントでは、Laravel アプリケーションが適切にデプロイされていることを確認するための優れた出発点をいくつか説明します。

<a name="server-requirements"></a>
## サーバー要件 (Server Requirements)

Laravel フレームワークにはいくつかのシステム要件があります。 Web サーバーに次の最小 PHP バージョンと拡張機能が備わっていることを確認する必要があります。

<div class="content-list" markdown="1">

- PHP >= 8.2
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

</div>

<a name="server-configuration"></a>
## サーバー構成 (Server Configuration)

<a name="nginx"></a>
### Nginx

Nginx を実行しているサーバーにアプリケーションをデプロイする場合は、Web サーバーを構成する開始点として次の構成ファイルを使用できます。ほとんどの場合、このファイルはサーバーの構成に応じてカスタマイズする必要があります。 **サーバー管理の支援が必要な場合は、[Laravel Cloud](https://cloud.laravel.com) のようなフルマネージド Laravel プラットフォームの使用を検討してください。**

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
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
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
### フランケンPHP

[FrankenPHP](https://frankenphp.dev/) は、Laravel アプリケーションを提供するために使用することもできます。 FrankenPHP は、Go で書かれた最新の PHP アプリケーション サーバーです。 FrankenPHP を使用して Laravel PHP アプリケーションを提供するには、その `php-server` コマンドを呼び出すだけです。

```shell
frankenphp php-server -r public/
```

FrankenPHP がサポートする強力な機能 ([Laravel Octane](/docs/{{version}}/octane) 統合、HTTP/3、最新の圧縮、Laravel アプリケーションをスタンドアロン バイナリとしてパッケージ化する機能など) を利用するには、FrankenPHP の [Laravelのドキュメント](https://frankenphp.dev/docs/laravel/) を参照してください。

<a name="directory-permissions"></a>
### ディレクトリのアクセス許可

Laravel は `bootstrap/cache` および `storage` ディレクトリに書き込む必要があるため、Web サーバーのプロセス所有者にこれらのディレクトリへの書き込み権限があることを確認する必要があります。

<a name="optimization"></a>
## 最適化 (Optimization)

アプリケーションを実稼働環境にデプロイする場合、構成、イベント、ルート、ビューなど、さまざまなファイルをキャッシュする必要があります。 Laravel は、これらすべてのファイルをキャッシュする単一の便利な `optimize` Artisan コマンドを提供します。このコマンドは通常、アプリケーションの展開プロセスの一部として呼び出す必要があります。

```shell
php artisan optimize
```

`optimize:clear` メソッドは、`optimize` コマンドによって生成されたすべてのキャッシュ ファイルと、デフォルトのキャッシュ ドライバ内のすべてのキーを削除するために使用できます。

```shell
php artisan optimize:clear
```

次のドキュメントでは、`optimize` コマンドによって実行される詳細な最適化コマンドのそれぞれについて説明します。

<a name="optimizing-configuration-loading"></a>
### キャッシュ構成

アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `config:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan config:cache
```

このコマンドは、Laravel のすべての設定ファイルを単一のキャッシュされたファイルに結合します。これにより、設定値をロードするときにフレームワークがファイルシステムにアクセスする必要がある回数が大幅に削減されます。

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされなくなり、`.env` 変数に対する `env` 関数の呼び出しはすべて `null` を返します。

<a name="caching-events"></a>
### イベントのキャッシュ

デプロイメントプロセス中に、アプリケーションの自動検出イベントとリスナのマッピングをキャッシュする必要があります。これは、デプロイメント中に `event:cache` Artisan コマンドを呼び出すことで実現できます。

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### キャッシュルート

多くのルートを持つ大規模なアプリケーションを構築している場合は、デプロイメント プロセス中に `route:cache` Artisan コマンドを実行していることを確認する必要があります。

```shell
php artisan route:cache
```

このコマンドにより、すべてのルート登録がキャッシュされたファイル内の 1 つのメソッド呼び出しに減らされ、数百のルートを登録する場合のルート登録のパフォーマンスが向上します。

<a name="optimizing-view-loading"></a>
### ビューのキャッシュ

アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `view:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan view:cache
```

このコマンドは、すべての Blade ビューをプリコンパイルするので、オンデマンドでコンパイルされなくなり、ビューを返す各リクエストのパフォーマンスが向上します。

<a name="reloading-services"></a>
## サービスをリロードしています (Reloading Services)

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com) にデプロイする場合、すべてのサービスの正常なリロードが自動的に処理されるため、`reload` コマンドを使用する必要はありません。

アプリケーションの新しいバージョンをデプロイした後、キューワーカー、Laravel Reverb、Laravel Octane などの長時間実行されるサービスは、新しいコードを使用するために再ロード/再起動する必要があります。 Laravel は、これらのサービスを終了する単一の `reload` Artisan コマンドを提供します。

```shell
php artisan reload
```

[Laravel Cloud](https://cloud.laravel.com) を使用していない場合は、リロード可能なプロセスの終了を検出し、自動的に再起動できるプロセス モニターを手動で構成する必要があります。

<a name="debug-mode"></a>
## デバッグモード (Debug Mode)

`config/app.php` 構成ファイルのデバッグ オプションにより、エラーに関する情報が実際にユーザーにどの程度表示されるかが決まります。デフォルトでは、このオプションは、アプリケーションの `.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

> [!WARNING]
> **運用環境では、この値は常に `false` である必要があります。本番環境で `APP_DEBUG` 変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="the-health-route"></a>
## 健康ルート (The Health Route)

Laravel には、アプリケーションのステータスを監視するために使用できる組み込みのヘルスチェック ルートが含まれています。運用環境では、このルートを使用して、アプリケーションのステータスを稼働時間モニター、ロード バランサー、または Kubernetes などのオーケストレーション システムに報告することができます。

デフォルトでは、ヘルスチェックルートは `/up` で提供され、アプリケーションが例外なく起動した場合は 200 HTTP 応答を返します。それ以外の場合は、500 HTTP 応答が返されます。アプリケーションの `bootstrap/app` ファイルでこのルートの URI を構成できます。

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

このルートに対して HTTP リクエストが行われると、Laravel は `Illuminate\Foundation\Events\DiagnosingHealth` イベントも送出し、アプリケーションに関連する追加のヘルスチェックを実行できるようにします。このイベントの [listener](/docs/{{version}}/events) 内で、アプリケーションのデータベースまたはキャッシュのステータスを確認できます。アプリケーションに問題が検出された場合は、リスナから例外をスローするだけで済みます。

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud または Forge を使用したデプロイ (Deploying With Laravel Cloud or Forge)

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel 用に調整されたフルマネージドの自動スケーリング展開プラットフォームが必要な場合は、[Laravel Cloud](https://cloud.laravel.com) をチェックしてください。 Laravel Cloud は、マネージド コンピューティング、データベース、キャッシュ、オブジェクト ストレージを提供する、Laravel の堅牢なデプロイメント プラットフォームです。

Laravel アプリケーションをクラウド上で起動して、スケーラブルなシンプルさに夢中になってください。 Laravel Cloud は、フレームワークとシームレスに連携できるように Laravel の作成者によって微調整されているため、これまでとまったく同じように Laravel アプリケーションを書き続けることができます。

<a name="laravel-forge"></a>
#### Laravel Forge

独自のサーバーを管理したいが、堅牢な Laravel アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、Laravel アプリケーション用の VPS サーバー管理プラットフォームである [Laravel Forge](https://forge.laravel.com) を使用してください。

Laravel Forge は、DigitalOcean、Linode、AWS などのさまざまなインフラストラクチャプロバイダ上にサーバーを作成できます。さらに、Forge は、Nginx、MySQL、Redis、Memcached、Beanstalk など、堅牢な Laravel アプリケーションの構築に必要なすべてのツールをインストールして管理します。

