<!-- # Deployment -->
# Deployment

- [Introduction](#introduction)
- [Server Requirements](#server-requirements)
- [Server Configuration](#server-configuration)
    - [Nginx](#nginx)
- [Optimization](#optimization)
    - [Autoloader Optimization](#autoloader-optimization)
    - [Optimizing Configuration Loading](#optimizing-configuration-loading)
    - [Optimizing Route Loading](#optimizing-route-loading)
    - [Optimizing View Loading](#optimizing-view-loading)
- [Debug Mode](#debug-mode)
- [Deploying With Forge / Vapor](#deploying-with-forge-or-vapor)

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
- PHP >= 8.0
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

<!-- </div> -->
</div>

<a name="server-configuration"></a>
<!-- ## Server Configuration -->
## Server Configuration

<a name="nginx"></a>
<!-- ### Nginx -->
### Nginx

<!-- If you are deploying your application to a server that is running Nginx, you may use the following configuration file as a starting point for configuring your web server. Most likely, this file will need to be customized depending on your server's configuration. **If you would like assistance in managing your server, consider using a first-party Laravel server management and deployment service such as [Laravel Forge](https://forge.laravel.com).** -->
Nginx を実行しているサーバーにアプリケーションをデプロイする場合は、Web サーバーを構成する開始点として次の構成ファイルを使用できます。ほとんどの場合、このファイルはサーバーの構成に応じてカスタマイズする必要があります。 **サーバー管理のサポートが必要な場合は、[Laravel Forge](https://forge.laravel.com) などのファーストパーティの Laravel サーバー管理および展開サービスの使用を検討してください。**

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
<!-- ## Optimization -->
## Optimization

<a name="autoloader-optimization"></a>
<!-- ### Autoloader Optimization -->
### Autoloader Optimization

<!-- When deploying to production, make sure that you are optimizing Composer's class autoloader map so Composer can quickly find the proper file to load for a given class: -->
運用環境にデプロイするときは、Composer が特定のクラスにロードする適切なファイルをすぐに見つけられるように、Composer のクラス オートローダー マップを最適化していることを確認してください。

```shell
composer install --optimize-autoloader --no-dev
```

> [!NOTE]
> オートローダーの最適化に加えて、プロジェクトのソース管理リポジトリに `composer.lock` ファイルを必ず含める必要があります。 `composer.lock` ファイルが存在すると、プロジェクトの依存関係をより速くインストールできます。

<a name="optimizing-configuration-loading"></a>
<!-- ### Optimizing Configuration Loading -->
### Optimizing Configuration Loading

<!-- When deploying your application to production, you should make sure that you run the `config:cache` Artisan command during your deployment process: -->
アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `config:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan config:cache
```

<!-- This command will combine all of Laravel's configuration files into a single, cached file, which greatly reduces the number of trips the framework must make to the filesystem when loading your configuration values. -->
このコマンドは、Laravel のすべての設定ファイルを単一のキャッシュされたファイルに結合します。これにより、設定値をロードするときにフレームワークがファイルシステムにアクセスする必要がある回数が大幅に削減されます。

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされなくなり、`.env` 変数に対する `env` 関数の呼び出しはすべて `null` を返します。

<a name="optimizing-route-loading"></a>
<!-- ### Optimizing Route Loading -->
### Optimizing Route Loading

<!-- If you are building a large application with many routes, you should make sure that you are running the `route:cache` Artisan command during your deployment process: -->
多くのルートを持つ大規模なアプリケーションを構築している場合は、デプロイメント プロセス中に `route:cache` Artisan コマンドを実行していることを確認する必要があります。

```shell
php artisan route:cache
```

<!-- This command reduces all of your route registrations into a single method call within a cached file, improving the performance of route registration when registering hundreds of routes. -->
このコマンドにより、すべてのルート登録がキャッシュされたファイル内の 1 つのメソッド呼び出しに減らされ、数百のルートを登録する場合のルート登録のパフォーマンスが向上します。

<a name="optimizing-view-loading"></a>
<!-- ### Optimizing View Loading -->
### Optimizing View Loading

<!-- When deploying your application to production, you should make sure that you run the `view:cache` Artisan command during your deployment process: -->
アプリケーションを運用環境にデプロイする場合は、デプロイメント プロセス中に `view:cache` Artisan コマンドを必ず実行する必要があります。

```shell
php artisan view:cache
```

<!-- This command precompiles all your Blade views so they are not compiled on demand, improving the performance of each request that returns a view. -->
このコマンドは、すべての Blade ビューをプリコンパイルするので、オンデマンドでコンパイルされなくなり、ビューを返す各リクエストのパフォーマンスが向上します。

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The debug option in your config/app.php configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your application's `.env` file. -->
config/app.php 設定ファイルのデバッグ オプションにより、エラーに関する情報が実際にユーザーにどの程度表示されるかが決まります。デフォルトでは、このオプションは、アプリケーションの `.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

<!-- **In your production environment, this value should always be `false`. If the `APP_DEBUG` variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
**運用環境では、この値は常に `false` である必要があります。本番環境で `APP_DEBUG` 変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="deploying-with-forge-or-vapor"></a>
<!-- ## Deploying With Forge / Vapor -->
## Deploying With Forge / Vapor

<a name="laravel-forge"></a>
<!-- #### Laravel Forge -->
#### Laravel Forge

<!-- If you aren't quite ready to manage your own server configuration or aren't comfortable configuring all of the various services needed to run a robust Laravel application, [Laravel Forge](https://forge.laravel.com) is a wonderful alternative. -->
独自のサーバー構成を管理する準備がまだ整っていない場合、または堅牢な Laravel アプリケーションを実行するために必要なさまざまなサービスをすべて構成することに慣れていない場合は、[Laravel Forge](https://forge.laravel.com) が優れた代替手段となります。

<!-- Laravel Forge can create servers on various infrastructure providers such as DigitalOcean, Linode, AWS, and more. In addition, Forge installs and manages all of the tools needed to build robust Laravel applications, such as Nginx, MySQL, Redis, Memcached, Beanstalk, and more. -->
Laravel Forge は、DigitalOcean、Linode、AWS などのさまざまなインフラストラクチャプロバイダ上にサーバーを作成できます。さらに、Forge は、Nginx、MySQL、Redis、Memcached、Beanstalk など、堅牢な Laravel アプリケーションの構築に必要なすべてのツールをインストールして管理します。

> [!NOTE]
> Laravel Forge を使用してデプロイするための完全なガイドが必要ですか? [Laravel Bootcamp](https://bootcamp.laravel.com/deploying) と Forge [video series available on Laracasts](https://laracasts.com/series/learn-laravel-forge-2022-edition) をチェックしてください。

<a name="laravel-vapor"></a>
<!-- #### Laravel Vapor -->
#### Laravel Vapor

<!-- If you would like a totally serverless, auto-scaling deployment platform tuned for Laravel, check out [Laravel Vapor](https://vapor.laravel.com). Laravel Vapor is a serverless deployment platform for Laravel, powered by AWS. Launch your Laravel infrastructure on Vapor and fall in love with the scalable simplicity of serverless. Laravel Vapor is fine-tuned by Laravel's creators to work seamlessly with the framework so you can keep writing your Laravel applications exactly like you're used to. -->
Laravel 用に調整された完全にサーバーレスで自動スケーリングのデプロイメント プラットフォームが必要な場合は、[Laravel Vapor](https://vapor.laravel.com) をチェックしてください。 Laravel Vapor は、AWS を利用した Laravel のサーバーレス デプロイメント プラットフォームです。 Vapor で Laravel インフラストラクチャを起動し、サーバーレスのスケーラブルなシンプルさに夢中になってください。 Laravel Vapor は、フレームワークとシームレスに連携できるように Laravel の作成者によって微調整されているため、これまでとまったく同じように Laravel アプリケーションを書き続けることができます。

