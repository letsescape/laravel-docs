# 導入 (Deployment)

- [Introduction](#introduction)
- [サーバー要件](#server-requirements)
- [サーバー構成](#server-configuration)
    - [Nginx](#nginx)
- [Optimization](#optimization)
    - [オートローダーの最適化](#autoloader-optimization)
    - [設定読み込みの最適化](#optimizing-configuration-loading)
    - [ルート読み込みの最適化](#optimizing-route-loading)
    - [ビューの読み込みの最適化](#optimizing-view-loading)
- [デバッグモード](#debug-mode)
- [Forge / Vapor を使用した展開](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel アプリケーションを本番環境にデプロイする準備ができたら、アプリケーションが可能な限り効率的に実行されるようにするために実行できる重要なことがいくつかあります。このドキュメントでは、Laravel アプリケーションが適切にデプロイされていることを確認するための優れた出発点をいくつか説明します。

<a name="server-requirements"></a>
## サーバー要件 (Server Requirements)

Laravel フレームワークにはいくつかのシステム要件があります。 Web サーバーに次の最小 PHP バージョンと拡張機能が備わっていることを確認する必要があります。

<div class="content-list" markdown="1">

- PHP >= 8.0
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

Nginx を実行しているサーバーにアプリケーションをデプロイする場合は、Web サーバーを構成する開始点として次の構成ファイルを使用できます。ほとんどの場合、このファイルはサーバーの構成に応じてカスタマイズする必要があります。 **サーバー管理のサポートが必要な場合は、[Laravel Forge](https://forge.laravel.com) などのファーストパーティの Laravel サーバー管理および展開サービスの使用を検討してください。**

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

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="optimization"></a>
## 最適化 (Optimization)

<a name="autoloader-optimization"></a>
### オートローダーの最適化

運用環境にデプロイするときは、Composer が特定のクラスにロードする適切なファイルをすぐに見つけられるように、Composer のクラス オートローダー マップを最適化していることを確認してください。

```shell
composer install --optimize-autoloader --no-dev
```

> **注記**
> オートローダーの最適化に加えて、プロジェクトのソース管理リポジトリに `composer.lock` ファイルを必ず含める必要があります。 `composer.lock` ファイルが存在すると、プロジェクトの依存関係をより速くインストールできます。

<a name="optimizing-configuration-loading"></a>
### 設定読み込みの最適化

アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `config:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan config:cache
```

このコマンドは、Laravel のすべての設定ファイルを単一のキャッシュされたファイルに結合します。これにより、設定値をロードするときにフレームワークがファイルシステムにアクセスする必要がある回数が大幅に削減されます。

> **警告**
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされなくなり、`.env` 変数に対する `env` 関数の呼び出しはすべて `null` を返します。

<a name="optimizing-route-loading"></a>
### ルート読み込みの最適化

多くのルートを持つ大規模なアプリケーションを構築している場合は、デプロイメント プロセス中に `route:cache` Artisan コマンドを実行していることを確認する必要があります。

```shell
php artisan route:cache
```

このコマンドにより、すべてのルート登録がキャッシュされたファイル内の 1 つのメソッド呼び出しに減らされ、数百のルートを登録する場合のルート登録のパフォーマンスが向上します。

<a name="optimizing-view-loading"></a>
### ビューの読み込みの最適化

アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `view:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan view:cache
```

このコマンドは、すべての Blade ビューをプリコンパイルするので、オンデマンドでコンパイルされなくなり、ビューを返す各リクエストのパフォーマンスが向上します。

<a name="debug-mode"></a>
## デバッグモード (Debug Mode)

config/app.php 設定ファイルのデバッグ オプションにより、エラーに関する情報が実際にユーザーにどの程度表示されるかが決まります。デフォルトでは、このオプションは、アプリケーションの `.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

**運用環境では、この値は常に `false` である必要があります。本番環境で `APP_DEBUG` 変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="deploying-with-forge-or-vapor"></a>
## Forge / Vapor を使用した展開 (Deploying With Forge / Vapor)

<a name="laravel-forge"></a>
#### Laravel Forge

独自のサーバー構成を管理する準備がまだ整っていない場合、または堅牢な Laravel アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、[Laravel Forge](https://forge.laravel.com) が優れた代替手段となります。

Laravel Forge は、DigitalOcean、Linode、AWS などのさまざまなインフラストラクチャプロバイダ上にサーバーを作成できます。さらに、Forge は、Nginx、MySQL、Redis、Memcached、Beanstalk など、堅牢な Laravel アプリケーションの構築に必要なすべてのツールをインストールして管理します。

> **注記**
> Laravel Forge を使用してデプロイするための完全なガイドが必要ですか? [Laravelブートキャンプ](https://bootcamp.laravel.com/deploying) と Forge [Laracasts で利用できるビデオ シリーズ](https://laracasts.com/series/learn-laravel-forge-2022-edition) をチェックしてください。

<a name="laravel-vapor"></a>
#### Laravel Vapor

Laravel 用に調整された完全にサーバーレスで自動スケーリングのデプロイメント プラットフォームが必要な場合は、[Laravel Vapor](https://vapor.laravel.com) をチェックしてください。 Laravel Vapor は、AWS を利用した Laravel のサーバーレス デプロイメント プラットフォームです。 Vapor で Laravel インフラストラクチャを起動し、サーバーレスのスケーラブルなシンプルさに夢中になってください。 Laravel Vapor は、フレームワークとシームレスに連携できるように Laravel の作成者によって微調整されているため、これまでとまったく同じように Laravel アプリケーションを書き続けることができます。

