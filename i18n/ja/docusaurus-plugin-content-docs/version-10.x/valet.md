# Laravel Valet (Laravel Valet)

- [Introduction](#introduction)
- [Installation](#installation)
    - [バレットのアップグレード](#upgrading-valet)
- [サービスを提供しているサイト](#serving-sites)
    - [「パーク」コマンド](#the-park-command)
    - [「リンク」コマンド](#the-link-command)
    - [TLS によるサイトの保護](#securing-sites)
    - [デフォルトのサイトの提供](#serving-a-default-site)
    - [サイトごとの PHP バージョン](#per-site-php-versions)
- [共有サイト](#sharing-sites)
    - [ローカルネットワーク上でサイトを共有する](#sharing-sites-on-your-local-network)
- [サイト固有の環境変数](#site-specific-environment-variables)
- [プロキシサービス](#proxying-services)
- [カスタム Valet ドライバ](#custom-valet-drivers)
    - [地元のドライバ](#local-drivers)
- [その他の Valet コマンド](#other-valet-commands)
- [バレットのディレクトリとファイル](#valet-directories-and-files)
    - [ディスクアクセス](#disk-access)

<a name="introduction"></a>
## 導入 (Introduction)

> [!NOTE]  
> macOS 上で Laravel アプリケーションを開発するさらに簡単な方法をお探しですか? [LaravelのHerd](https://herd.laravel.com) をチェックしてください。 Herd には、Valet、PHP、Composer など、Laravel 開発を始めるために必要なものがすべて含まれています。

[Laravel Valet](https://github.com/laravel/valet) は、macOS ミニマリストのための開発環境です。 Laravel Valet は、マシンの起動時に常に [Nginx](https://www.nginx.com/) をバックグラウンドで実行するように Mac を設定します。次に、Valet は [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq) を使用して、`*.test` ドメイン上のすべてのリクエストをプロキシし、ローカル マシンにインストールされているサイトをポイントします。

言い換えれば、Valet は約 7 MB の RAM を使用する非常に高速な Laravel 開発環境です。 Valet は、[Sail](/docs/{{version}}/sail) または [Homestead](/docs/{{version}}/homestead) の完全な代替品ではありませんが、柔軟な基本が必要な場合、極端な速度を好む場合、または RAM の量が限られているマシンで作業している場合に優れた代替手段となります。

すぐに使えるバレット サポートには次のものが含まれますが、これらに限定されません。

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [ケーキPHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- 静的HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

ただし、独自の [カスタムドライバ](#custom-valet-drivers) を使用して Valet を拡張することはできます。

<a name="installation"></a>
## インストール (Installation)

> [!WARNING]  
> Valet には macOS と [Homebrew](https://brew.sh/) が必要です。インストールする前に、Apache や Nginx などの他のプログラムがローカル マシンのポート 80 にバインドされていないことを確認する必要があります。

開始するには、まず `update` コマンドを使用して Homebrew が最新であることを確認する必要があります。

```shell
brew update
```

次に、Homebrew を使用して PHP をインストールする必要があります。

```shell
brew install php
```

PHP をインストールしたら、[Composer パッケージマネージャー](https://getcomposer.org) をインストールする準備が整います。さらに、`$HOME/.composer/vendor/bin` ディレクトリがシステムの「PATH」にあることを確認する必要があります。 Composer がインストールされた後、Laravel Valet をグローバル Composer パッケージとしてインストールできます。

```shell
composer global require laravel/valet
```

最後に、Valet の `install` コマンドを実行できます。これにより、Valet と DnsMasq が構成され、インストールされます。さらに、Valet が依存するデーモンは、システムの起動時に起動するように構成されます。

```shell
valet install
```

Valet がインストールされたら、`ping foobar.test` などのコマンドを使用して、端末上の任意の `*.test` ドメインに ping を実行してみてください。 Valet が正しくインストールされている場合は、このドメインが `127.0.0.1` で応答しているのが確認できるはずです。

Valet は、マシンが起動するたびに必要なサービスを自動的に開始します。

<a name="php-versions"></a>
#### PHPのバージョン

> [!NOTE]  
> グローバル PHP バージョンを変更する代わりに、`isolate` [command](#per-site-php-versions) を介してサイトごとの PHP バージョンを使用するように Valet に指示できます。

Valet では、`valet use php@version` コマンドを使用して PHP バージョンを切り替えることができます。 Valet は、指定された PHP バージョンがまだインストールされていない場合、Homebrew 経由でインストールします。

```shell
valet use php@8.1

valet use php
```

プロジェクトのルートに `.valetrc` ファイルを作成することもできます。 `.valetrc` ファイルには、サイトで使用する必要がある PHP バージョンが含まれている必要があります。

```shell
php=php@8.1
```

このファイルが作成されたら、`valet use` コマンドを実行するだけで、コマンドはファイルを読み取ってサイトの優先 PHP バージョンを決定します。

> [!WARNING]  
> Valet は、複数の PHP バージョンがインストールされている場合でも、一度に 1 つの PHP バージョンのみを提供します。

<a name="database"></a>
#### データベース

アプリケーションにデータベースが必要な場合は、[DBngin](https://dbngin.com) をチェックしてください。これは、MySQL、PostgreSQL、Redis を含む無料のオールインワン データベース管理ツールを提供します。 DBngin がインストールされたら、ユーザー名 `root` とパスワードに空の文字列を使用して、`127.0.0.1` でデータベースに接続できます。

<a name="resetting-your-installation"></a>
#### インストールをリセットする

Valet インストールを適切に実行するのに問題がある場合は、`composer global require laravel/valet` コマンドに続いて `valet install` を実行すると、インストールがリセットされ、さまざまな問題が解決される可能性があります。まれに、`valet uninstall --force` に続いて `valet install` を実行して、Valet を「ハード リセット」する必要がある場合があります。

<a name="upgrading-valet"></a>
### バレットのアップグレード

端末で `composer global require laravel/valet` コマンドを実行すると、Valet インストールを更新できます。アップグレード後、必要に応じて Valet が構成ファイルに追加のアップグレードを行えるように、`valet install` コマンドを実行することをお勧めします。

<a name="upgrading-to-valet-4"></a>
#### Valet 4 へのアップグレード

Valet 3 から Valet 4 にアップグレードする場合は、次の手順に従って Valet インストールを適切にアップグレードしてください。

<div class="content-list" markdown="1">

- サイトの PHP バージョンをカスタマイズするために `.valetphprc` ファイルを追加した場合は、各 `.valetphprc` ファイルの名前を `.valetrc` に変更します。次に、`php=` を `.valetrc` ファイルの既存のコンテンツの先頭に追加します。
- 新しいドライバ システムの名前空間、拡張子、タイプ ヒントに一致するようにカスタム ドライバを更新し、タイプ ヒントを返します。例として、Valet の [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) を参照してください。
- PHP 7.1 ～ 7.4 を使用してサイトを提供している場合は、Homebrew を使用して 8.0 以降の PHP バージョンをインストールしていることを確認してください。Valet は、プライマリ リンクされたバージョンではない場合でも、このバージョンを使用してスクリプトの一部を実行します。

</div>

<a name="serving-sites"></a>
## サービスを提供しているサイト (Serving Sites)

Valet がインストールされたら、Laravel アプリケーションの提供を開始する準備が整います。 Valet は、アプリケーションの提供に役立つ 2 つのコマンド、`park` と `link` を提供します。

<a name="the-park-command"></a>
### `park` コマンド

`park` コマンドは、アプリケーションを含むマシン上のディレクトリを登録します。ディレクトリが Valet で「パーク」されると、そのディレクトリ内のすべてのディレクトリに、Web ブラウザの `http://<directory-name>.test` でアクセスできるようになります。

```shell
cd ~/Sites

valet park
```

それだけです。これで、「パーク」ディレクトリ内に作成したアプリケーションはすべて、`http://<directory-name>.test` 規則を使用して自動的に提供されるようになります。したがって、パークされたディレクトリに「laravel」という名前のディレクトリが含まれている場合、そのディレクトリ内のアプリケーションには `http://laravel.test` でアクセスできます。さらに、Valet では、ワイルドカード サブドメイン (`http://foo.laravel.test`) を使用してサイトにアクセスすることが自動的に許可されます。

<a name="the-link-command"></a>
### `link` コマンド

`link` コマンドを使用して、Laravel アプリケーションを提供することもできます。このコマンドは、ディレクトリ全体ではなく、ディレクトリ内の単一のサイトを提供する場合に便利です。

```shell
cd ~/Sites/laravel

valet link
```

`link` コマンドを使用してアプリケーションが Valet にリンクされると、そのディレクトリ名を使用してアプリケーションにアクセスできるようになります。したがって、上記の例でリンクされていたサイトには、`http://laravel.test` でアクセスされる可能性があります。さらに、Valet では、ワイルドカード サブドメイン (`http://foo.laravel.test`) を使用してサイトにアクセスすることが自動的に許可されます。

別のホスト名でアプリケーションを提供したい場合は、ホスト名を `link` コマンドに渡すことができます。たとえば、次のコマンドを実行して、アプリケーションを `http://application.test` で利用できるようにします。

```shell
cd ~/Sites/laravel

valet link application
```

もちろん、`link` コマンドを使用して、サブドメインでアプリケーションを提供することもできます。

```shell
valet link api.application
```

`links` コマンドを実行して、リンクされたすべてのディレクトリのリストを表示できます。

```shell
valet links
```

`unlink` コマンドは、サイトのシンボリック リンクを破棄するために使用できます。

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### TLS によるサイトの保護

デフォルトでは、Valet は HTTP 経由でサイトを提供します。ただし、HTTP/2 を使用して暗号化された TLS 経由でサイトを提供したい場合は、`secure` コマンドを使用できます。たとえば、サイトが `laravel.test` ドメインの Valet によって提供されている場合は、次のコマンドを実行してサイトを保護する必要があります。

```shell
valet secure laravel
```

サイトの「保護を解除」し、プレーン HTTP 経由でトラフィックを提供する状態に戻すには、`unsecure` コマンドを使用します。 `secure` コマンドと同様に、このコマンドは保護を解除するホスト名を受け入れます。

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### デフォルトのサイトの提供

場合によっては、未知の `test` ドメインにアクセスしたときに、`404` ではなく「デフォルト」サイトを提供するように Valet を設定したい場合があります。これを実現するには、デフォルト サイトとして機能するサイトへのパスを含む `default` オプションを `~/.config/valet/config.json` 構成ファイルに追加します。

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### サイトごとの PHP バージョン

デフォルトでは、Valet はグローバル PHP インストールを使用してサイトにサービスを提供します。ただし、さまざまなサイトで複数の PHP バージョンをサポートする必要がある場合は、`isolate` コマンドを使用して、特定のサイトで使用する PHP バージョンを指定できます。 `isolate` コマンドは、現在の作業ディレクトリにあるサイトで指定された PHP バージョンを使用するように Valet を構成します。

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

サイト名がそのサイトを含むディレクトリの名前と一致しない場合は、`--site` オプションを使用してサイト名を指定できます。

```shell
valet isolate php@8.0 --site="site-name"
```

便宜上、`valet php`、`composer`、および `which-php` コマンドを使用して、サイトの構成された PHP バージョンに基づいて、適切な PHP CLI またはツールへの呼び出しをプロキシすることができます。

```shell
valet php
valet composer
valet which-php
```

`isolated` コマンドを実行すると、すべての分離サイトとその PHP バージョンのリストを表示できます。

```shell
valet isolated
```

サイトを Valet のグローバルにインストールされた PHP バージョンに戻すには、サイトのルート ディレクトリから `unisolate` コマンドを呼び出します。

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## 共有サイト (Sharing Sites)

Valet には、ローカル サイトを世界と共有するコマンドが含まれており、モバイル デバイスでサイトをテストしたり、チーム メンバーやクライアントと共有したりする簡単な方法を提供します。

Valet は、デフォルトで、ngrok または Expose を介したサイトの共有をサポートしています。サイトを共有する前に、`share-tool` コマンドを使用して、`ngrok` または `expose` を指定して Valet 構成を更新する必要があります。

```shell
valet share-tool ngrok
```

ツールを選択し、Homebrew (ngrok の場合) または Composer (Expose の場合) 経由でインストールしていない場合、Valet は自動的にそのツールをインストールするように求めるプロンプトを表示します。もちろん、どちらのツールでも、サイトの共有を開始する前に、ngrok または Expose アカウントを認証する必要があります。

サイトを共有するには、ターミナルでサイトのディレクトリに移動し、Valet の `share` コマンドを実行します。一般にアクセス可能な URL がクリップボードに配置され、ブラウザに直接貼り付けたり、チームと共有したりできるようになります。

```shell
cd ~/Sites/laravel

valet share
```

サイトの共有を停止するには、`Control + C` を押してください。

> [!WARNING]  
> カスタム DNS サーバー (`1.1.1.1` など) を使用している場合、ngrok 共有が正しく機能しない可能性があります。お使いのマシンでこれに該当する場合は、Mac のシステム設定を開き、ネットワーク設定に移動し、詳細設定を開いて、DNS タブに移動して、最初の DNS サーバーとして `127.0.0.1` を追加します。

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok 経由でサイトを共有する

ngrok を使用してサイトを共有するには、[ngrokアカウントを作成する](https://dashboard.ngrok.com/signup) および [認証トークンをセットアップする](https://dashboard.ngrok.com/get-started/your-authtoken) が必要です。認証トークンを取得したら、そのトークンを使用して Valet 構成を更新できます。

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]  
> 追加の ngrok パラメーター (`valet share --region=eu` など) を share コマンドに渡すことができます。詳細については、[ngrok ドキュメント](https://ngrok.com/docs) を参照してください。

<a name="sharing-sites-via-expose"></a>
#### Expose 経由でサイトを共有する

Expose を使用してサイトを共有するには、[Expose アカウントを作成する](https://expose.dev/register) および [認証トークンを介して Expose で認証する](https://expose.dev/docs/getting-started/getting-your-token) が必要です。

サポートされる追加のコマンドライン パラメーターに関する情報については、[ドキュメントを公開する](https://expose.dev/docs) を参照してください。

<a name="sharing-sites-on-your-local-network"></a>
### ローカルネットワーク上でサイトを共有する

Valet は、開発マシンがインターネットからのセキュリティ リスクにさらされないように、デフォルトで内部 `127.0.0.1` インターフェイスへの受信トラフィックを制限します。

ローカル ネットワーク上の他のデバイスがマシンの IP アドレス (例: `192.168.1.10/application.test`) を介してマシン上の Valet サイトにアクセスできるようにしたい場合は、そのサイトの適切な Nginx 構成ファイルを手動で編集して、`listen` ディレクティブの制限を削除する必要があります。ポート 80 および 443 の `listen` ディレクティブの `127.0.0.1:` プレフィックスを削除する必要があります。

プロジェクトで `valet secure` を実行していない場合は、`/usr/local/etc/nginx/valet/valet.conf` ファイルを編集することで、すべての非 HTTPS サイトへのネットワーク アクセスを開くことができます。ただし、HTTPS 経由でプロジェクト サイトを提供している場合 (サイトに対して `valet secure` を実行している場合)、`~/.config/valet/Nginx/app-name.test` ファイルを編集する必要があります。

Nginx 構成を更新したら、`valet restart` コマンドを実行して構成の変更を適用します。

<a name="site-specific-environment-variables"></a>
## サイト固有の環境変数 (Site Specific Environment Variables)

他のフレームワークを使用する一部のアプリケーションはサーバー環境変数に依存する場合がありますが、それらの変数をプロジェクト内で構成する方法は提供されません。 Valet を使用すると、プロジェクトのルート内に `.valet-env.php` ファイルを追加することで、サイト固有の環境変数を構成できます。このファイルは、配列で指定された各サイトのグローバル `$_SERVER` 配列に追加されるサイト/環境変数のペアの配列を返す必要があります。

    <?php

    return [
        // Set $_SERVER['key'] to "value" for the laravel.test site...
        'laravel' => [
            'key' => 'value',
        ],

        // Set $_SERVER['key'] to "value" for all sites...
        '*' => [
            'key' => 'value',
        ],
    ];

<a name="proxying-services"></a>
## プロキシサービス (Proxying Services)

Valet ドメインをローカル マシン上の別のサービスにプロキシしたい場合があります。たとえば、Docker で別のサイトを実行しながら、Valet を実行することが必要になる場合があります。ただし、Valet と Docker の両方を同時にポート 80 にバインドすることはできません。

これを解決するには、`proxy` コマンドを使用してプロキシを生成します。たとえば、`http://elasticsearch.test` から `http://127.0.0.1:9200` へのすべてのトラフィックをプロキシできます。

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

`unproxy` コマンドを使用してプロキシを削除できます。

```shell
valet unproxy elasticsearch
```

`proxies` コマンドを使用して、プロキシされているすべてのサイト構成を一覧表示できます。

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## カスタム Valet ドライバ (Custom Valet Drivers)

独自の Valet 「ドライバ」を作成して、Valet でネイティブにサポートされていないフレームワークまたは CMS 上で実行される PHP アプリケーションにサービスを提供することができます。 Valet をインストールすると、`SampleValetDriver.php` ファイルを含む `~/.config/valet/Drivers` ディレクトリが作成されます。このファイルには、カスタム ドライバの作成方法を示すサンプル ドライバ実装が含まれています。ドライバを作成するには、`serves`、`isStaticFile`、および `frontControllerPath` の 3 つのメソッドを実装するだけで済みます。

3 つのメソッドはすべて、引数として `$sitePath`、`$siteName`、および `$uri` の値を受け取ります。 `$sitePath` は、`/Users/Lisa/Sites/my-project` など、マシン上で提供されているサイトへの完全修飾パスです。 `$siteName` は、ドメイン (`my-project`) の「ホスト」/「サイト名」部分です。 `$uri` は、受信リクエスト URI (`/foo/bar`) です。

カスタム Valet ドライバが完成したら、`FrameworkValetDriver.php` 命名規則を使用して、それを `~/.config/valet/Drivers` ディレクトリに配置します。たとえば、WordPress 用のカスタム バレット ドライバを作成している場合、ファイル名は `WordPressValetDriver.php` にする必要があります。

カスタム Valet ドライバが実装する必要がある各メソッドのサンプル実装を見てみましょう。

<a name="the-serves-method"></a>
#### `serves` メソッド

ドライバが受信リクエストを処理する必要がある場合、`serves` メソッドは `true` を返す必要があります。それ以外の場合、メソッドは `false` を返す必要があります。したがって、このメソッド内で、指定された `$sitePath` に、提供しようとしているタイプのプロジェクトが含まれているかどうかを判断する必要があります。

たとえば、`WordPressValetDriver` を作成していると想像してみましょう。 `serves` メソッドは次のようになります。

    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return is_dir($sitePath.'/wp-admin');
    }

<a name="the-isstaticfile-method"></a>
#### `isStaticFile` メソッド

`isStaticFile` は、受信リクエストが画像やスタイルシートなどの「静的」ファイルに対するものであるかどうかを判断する必要があります。ファイルが静的な場合、メソッドはディスク上の静的ファイルへの完全修飾パスを返す必要があります。受信リクエストが静的ファイルに対するものではない場合、メソッドは `false` を返す必要があります。

    /**
     * Determine if the incoming request is for a static file.
     *
     * @return string|false
     */
    public function isStaticFile(string $sitePath, string $siteName, string $uri)
    {
        if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
            return $staticFilePath;
        }

        return false;
    }

> [!WARNING]  
> `isStaticFile` メソッドは、`serves` メソッドが受信リクエストに対して `true` を返し、リクエスト URI が `/` ではない場合にのみ呼び出されます。

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` メソッド

`frontControllerPath` メソッドは、アプリケーションの「フロント コントローラ」への完全修飾パスを返す必要があります。通常は、「index.php」ファイルまたは同等のファイルです。

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public/index.php';
    }

<a name="local-drivers"></a>
### 地元のドライバ

単一アプリケーションのカスタム Valet ドライバを定義する場合は、アプリケーションのルート ディレクトリに `LocalValetDriver.php` ファイルを作成します。カスタム ドライバは、基本 `ValetDriver` クラスを拡張することも、`LaravelValetDriver` などの既存のアプリケーション固有のドライバを拡張することもできます。

    use Valet\Drivers\LaravelValetDriver;

    class LocalValetDriver extends LaravelValetDriver
    {
        /**
         * Determine if the driver serves the request.
         */
        public function serves(string $sitePath, string $siteName, string $uri): bool
        {
            return true;
        }

        /**
         * Get the fully resolved path to the application's front controller.
         */
        public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
        {
            return $sitePath.'/public_html/index.php';
        }
    }

<a name="other-valet-commands"></a>
## その他の Valet コマンド (Other Valet Commands)

<div class="overflow-auto">

コマンド |説明
------------- | -------------
`valet list` |すべての Valet コマンドのリストを表示します。
`valet diagnose` | Valet のデバッグに役立つ診断を出力します。
`valet directory-listing` |ディレクトリ一覧の動作を決定します。デフォルトは「オフ」で、ディレクトリの 404 ページをレンダリングします。
`valet forget` | 「パーク」ディレクトリからこのコマンドを実行して、パーク ディレクトリ リストから削除します。
`valet log` | Valet のサービスによって書き込まれたログのリストを表示します。
`valet paths` |すべての「駐車」パスを表示します。
`valet restart` | Valet デーモンを再起動します。
`valet start` | Valet デーモンを開始します。
`valet stop` | Valet デーモンを停止します。
`valet trust` | Brew と Valet の sudoers ファイルを追加して、パスワードの入力を求めるプロンプトを表示せずに Valet コマンドを実行できるようにします。
`valet uninstall` | Valet のアンインストール: 手動アンインストールの手順を示します。 Valet のリソースをすべて積極的に削除するには、`--force` オプションを渡します。

</div>

<a name="valet-directories-and-files"></a>
## バレットのディレクトリとファイル (Valet Directories and Files)

Valet 環境の問題のトラブルシューティングを行う際には、次のディレクトリとファイルの情報が役立つ場合があります。

#### `~/.config/valet`

Valet のすべての設定が含まれています。このディレクトリのバックアップを保持しておくとよいでしょう。

#### `~/.config/valet/dnsmasq.d/`

このディレクトリには DNSMasq の設定が含まれています。

#### `~/.config/valet/Drivers/`

このディレクトリには Valet のドライバが含まれています。ドライバは、特定のフレームワーク/CMS がどのように提供されるかを決定します。

#### `~/.config/valet/Nginx/`

このディレクトリには、Valet の Nginx サイト構成がすべて含まれています。これらのファイルは、`install` および `secure` コマンドを実行すると再構築されます。

#### `~/.config/valet/Sites/`

このディレクトリには、[リンクされたプロジェクト](#the-link-command) のすべてのシンボリック リンクが含まれています。

#### `~/.config/valet/config.json`

このファイルは、Valet のマスター構成ファイルです。

#### `~/.config/valet/valet.sock`

このファイルは、Valet の Nginx インストールで使用される PHP-FPM ソケットです。これは、PHP が適切に実行されている場合にのみ存在します。

#### `~/.config/valet/Log/fpm-php.www.log`

このファイルは、PHP エラーのユーザー ログです。

#### `~/.config/valet/Log/nginx-error.log`

このファイルは、Nginx エラーのユーザー ログです。

#### `/usr/local/var/log/php-fpm.log`

このファイルは、PHP-FPM エラーのシステム ログです。

#### `/usr/local/var/log/nginx`

このディレクトリには、Nginx のアクセス ログとエラー ログが含まれます。

#### `/usr/local/etc/php/X.X/conf.d`

このディレクトリには、さまざまな PHP 構成設定用の `*.ini` ファイルが含まれています。

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

このファイルは、PHP-FPM プール構成ファイルです。

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

このファイルは、サイトの SSL 証明書を構築するために使用されるデフォルトの Nginx 構成です。

<a name="disk-access"></a>
### ディスクアクセス

macOS 10.14 以降、[一部のファイルとディレクトリへのアクセスはデフォルトで制限されています](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf)。これらの制限には、デスクトップ、ドキュメント、およびダウンロード ディレクトリが含まれます。さらに、ネットワーク ボリュームとリムーバブル ボリュームへのアクセスが制限されます。したがって、Valet では、サイト フォルダーをこれらの保護された場所の外に配置することをお勧めします。

ただし、これらの場所のいずれかからサイトにサービスを提供したい場合は、Nginx に「フル ディスク アクセス」を与える必要があります。そうしないと、特に静的アセットを提供する場合に、サーバー エラーや Nginx によるその他の予期しない動作が発生する可能性があります。通常、macOS では、これらの場所へのフル アクセスを Nginx に許可するように求めるプロンプトが自動的に表示されます。または、`System Preferences` > `Security & Privacy` > `Privacy` を選択し、`Full Disk Access` を選択して手動で行うこともできます。次に、メイン ウィンドウ ペインで `nginx` エントリを有効にします。

