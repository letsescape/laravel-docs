<!-- # Laravel Valet -->
# Laravel Valet

- [Introduction](#introduction)
- [Installation](#installation)
    - [Upgrading Valet](#upgrading-valet)
- [Serving Sites](#serving-sites)
    - [The "Park" Command](#the-park-command)
    - [The "Link" Command](#the-link-command)
    - [Securing Sites With TLS](#securing-sites)
    - [Serving a Default Site](#serving-a-default-site)
- [Sharing Sites](#sharing-sites)
    - [Sharing Sites Via Ngrok](#sharing-sites-via-ngrok)
    - [Sharing Sites Via Expose](#sharing-sites-via-expose)
    - [Sharing Sites On Your Local Network](#sharing-sites-on-your-local-network)
- [Site Specific Environment Variables](#site-specific-environment-variables)
- [Proxying Services](#proxying-services)
- [Custom Valet Drivers](#custom-valet-drivers)
    - [Local Drivers](#local-drivers)
- [Other Valet Commands](#other-valet-commands)
- [Valet Directories & Files](#valet-directories-and-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Valet](https://github.com/laravel/valet) is a development environment for macOS minimalists. Laravel Valet configures your Mac to always run [Nginx](https://www.nginx.com/) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.test` domain to point to sites installed on your local machine. -->
[Laravel Valet](https://github.com/laravel/valet) は、macOS ミニマリストのための開発環境です。 Laravel Valet は、マシンの起動時に常に [Nginx](https://www.nginx.com/) をバックグラウンドで実行するように Mac を設定します。次に、Valet は [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq) を使用して、`*.test` ドメイン上のすべてのリクエストをプロキシし、ローカル マシンにインストールされているサイトをポイントします。

<!-- In other words, Valet is a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for [Sail](/docs/8.x/sail) or [Homestead](/docs/8.x/homestead), but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM. -->
言い換えれば、Valet は約 7 MB の RAM を使用する非常に高速な Laravel 開発環境です。 Valet は、[Sail](/docs/8.x/sail) または [Homestead](/docs/8.x/homestead) の完全な代替品ではありませんが、柔軟な基本が必要な場合、極端な速度を好む場合、または RAM の量が限られているマシンで作業している場合に優れた代替手段となります。

<!-- Out of the box, Valet support includes, but is not limited to: -->
すぐに使えるValet サポートには次のものが含まれますが、これらに限定されません。

<!-- <div id="valet-support" markdown="1"> -->
<div id="valet-support" markdown="1">

<!--
- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
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
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)
-->
- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [Concrete5](https://www.concrete5.org/)
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

<!-- </div> -->
</div>

<!-- However, you may extend Valet with your own [custom drivers](#custom-valet-drivers). -->
ただし、独自の [custom drivers](#custom-valet-drivers) を使用して Valet を拡張することはできます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!NOTE]
> Valet には macOS と [Homebrew](https://brew.sh/) が必要です。インストールする前に、Apache や Nginx などの他のプログラムがローカル マシンのポート 80 にバインドされていないことを確認する必要があります。

<!-- To get started, you first need to ensure that Homebrew is up to date using the `update` command: -->
開始するには、まず `update` コマンドを使用して Homebrew が最新であることを確認する必要があります。

<!--     brew update -->
    brew update

<!-- Next, you should use Homebrew to install PHP: -->
次に、Homebrew を使用して PHP をインストールする必要があります。

<!--     brew install php -->
    brew install php

<!-- After installing PHP, you are ready to install the [Composer package manager](https://getcomposer.org). In addition, you should make sure the `~/.composer/vendor/bin` directory is in your system's "PATH". After Composer has been installed, you may install Laravel Valet as a global Composer package: -->
PHP をインストールしたら、[Composer package manager](https://getcomposer.org) をインストールする準備が整います。さらに、`~/.composer/vendor/bin` ディレクトリがシステムの「PATH」にあることを確認する必要があります。 Composer がインストールされた後、Laravel Valet をグローバル Composer パッケージとしてインストールできます。

```
composer global require laravel/valet
```

<!-- Finally, you may execute Valet's `install` command. This will configure and install Valet and DnsMasq. In addition, the daemons Valet depends on will be configured to launch when your system starts: -->
最後に、Valet の `install` コマンドを実行できます。これにより、Valet と DnsMasq が構成され、インストールされます。さらに、Valet が依存するデーモンは、システムの起動時に起動するように構成されます。

<!--     valet install -->
    valet install

<!-- Once Valet is installed, try pinging any `*.test` domain on your terminal using a command such as `ping foobar.test`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`. -->
Valet がインストールされたら、`ping foobar.test` などのコマンドを使用して、端末上の任意の `*.test` ドメインに ping を実行してみてください。 Valet が正しくインストールされている場合は、このドメインが `127.0.0.1` で応答しているのが確認できるはずです。

<!-- Valet will automatically start its required services each time your machine boots. -->
Valet は、マシンが起動するたびに必要なサービスを自動的に開始します。

<a name="php-versions"></a>
<!-- #### PHP Versions -->
#### PHP Versions

<!-- Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Homebrew if it is not already installed: -->
Valet では、`valet use php@version` コマンドを使用して PHP バージョンを切り替えることができます。 Valet は、指定された PHP バージョンがまだインストールされていない場合、Homebrew 経由でインストールします。

```
valet use php@7.2

valet use php
```

<!-- You may also create a `.valetphprc` file in the root of your project. The `.valetphprc` file should contain the PHP version the site should use: -->
プロジェクトのルートに `.valetphprc` ファイルを作成することもできます。 `.valetphprc` ファイルには、サイトで使用する必要がある PHP バージョンが含まれている必要があります。

<!--     php@7.2 -->
    php@7.2

<!-- Once this file has been created, you may simply execute the `valet use` command and the command will determine the site's preferred PHP version by reading the file. -->
このファイルが作成されたら、`valet use` コマンドを実行するだけで、コマンドはファイルを読み取ってサイトの優先 PHP バージョンを決定します。

> [!NOTE]
> Valet は、複数の PHP バージョンがインストールされている場合でも、一度に 1 つの PHP バージョンのみを提供します。

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- If your application needs a database, check out [DBngin](https://dbngin.com). DBngin provides a free, all-in-one database management tool that includes MySQL, PostgreSQL, and Redis. After DBngin has been installed, you can connect to your database at `127.0.0.1` using the `root` username and an empty string for the password. -->
アプリケーションにデータベースが必要な場合は、[DBngin](https://dbngin.com) を確認してください。 DBngin は、MySQL、PostgreSQL、Redis を含む無料のオールインワン データベース管理ツールを提供します。 DBngin がインストールされたら、ユーザー名 `root` とパスワードに空の文字列を使用して、`127.0.0.1` でデータベースに接続できます。

<a name="resetting-your-installation"></a>
<!-- #### Resetting Your Installation -->
#### Resetting Your Installation

<!-- If you are having trouble getting your Valet installation to run properly, executing the `composer global update` command followed by `valet install` will reset your installation and can solve a variety of problems. In rare cases, it may be necessary to "hard reset" Valet by executing `valet uninstall --force` followed by `valet install`. -->
Valet インストールを適切に実行するのに問題がある場合は、`composer global update` コマンドに続いて `valet install` を実行すると、インストールがリセットされ、さまざまな問題が解決される可能性があります。まれに、`valet uninstall --force` に続いて `valet install` を実行して、Valet を「ハード リセット」する必要がある場合があります。

<a name="upgrading-valet"></a>
<!-- ### Upgrading Valet -->
### Upgrading Valet

<!-- You may update your Valet installation by executing the `composer global update` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary. -->
端末で `composer global update` コマンドを実行すると、Valet インストールを更新できます。アップグレード後、必要に応じて Valet が構成ファイルに追加のアップグレードを行えるように、`valet install` コマンドを実行することをお勧めします。

<a name="serving-sites"></a>
<!-- ## Serving Sites -->
## Serving Sites

<!-- Once Valet is installed, you're ready to start serving your Laravel applications. Valet provides two commands to help you serve your applications: `park` and `link`. -->
Valet がインストールされたら、Laravel アプリケーションの提供を開始する準備が整います。 Valet は、アプリケーションの提供に役立つ 2 つのコマンド、`park` と `link` を提供します。

<a name="the-park-command"></a>
<!-- ### The `park` Command -->
### The `park` Command

<!-- The `park` command registers a directory on your machine that contains your applications. Once the directory has been "parked" with Valet, all of the directories within that directory will be accessible in your web browser at `http://<directory-name>.test`: -->
`park` コマンドは、アプリケーションを含むマシン上のディレクトリを登録します。ディレクトリが Valet で「パーク」されると、そのディレクトリ内のすべてのディレクトリに、Web ブラウザの `http://<directory-name>.test` でアクセスできるようになります。

```
cd ~/Sites

valet park
```

<!-- That's all there is to it. Now, any application you create within your "parked" directory will automatically be served using the `http://<directory-name>.test` convention. So, if your parked directory contains a directory named "laravel", the application within that directory will be accessible at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard subdomains (`http://foo.laravel.test`). -->
それだけです。これで、「パーク」ディレクトリ内に作成したアプリケーションはすべて、`http://<directory-name>.test` 規則を使用して自動的に提供されるようになります。したがって、パークされたディレクトリに「laravel」という名前のディレクトリが含まれている場合、そのディレクトリ内のアプリケーションには `http://laravel.test` でアクセスできます。さらに、Valet では、ワイルドカード サブドメイン (`http://foo.laravel.test`) を使用してサイトにアクセスすることが自動的に許可されます。

<a name="the-link-command"></a>
<!-- ### The `link` Command -->
### The `link` Command

<!-- The `link` command can also be used to serve your Laravel applications. This command is useful if you want to serve a single site in a directory and not the entire directory: -->
`link` コマンドを使用して、Laravel アプリケーションを提供することもできます。このコマンドは、ディレクトリ全体ではなく、ディレクトリ内の単一のサイトを提供する場合に便利です。

```
cd ~/Sites/laravel

valet link
```

<!-- Once an application has been linked to Valet using the `link` command, you may access the application using its directory name. So, the site that was linked in the example above may be accessed at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard sub-domains (`http://foo.laravel.test`). -->
`link` コマンドを使用してアプリケーションが Valet にリンクされると、そのディレクトリ名を使用してアプリケーションにアクセスできるようになります。したがって、上記の例でリンクされていたサイトには、`http://laravel.test` でアクセスされる可能性があります。さらに、Valet では、ワイルドカード サブドメイン (`http://foo.laravel.test`) を使用してサイトにアクセスすることが自動的に許可されます。

<!-- If you would like to serve the application at a different hostname, you may pass the hostname to the `link` command. For example, you may run the following command to make an application available at `http://application.test`: -->
別のホスト名でアプリケーションを提供したい場合は、ホスト名を `link` コマンドに渡すことができます。たとえば、次のコマンドを実行して、アプリケーションを `http://application.test` で利用できるようにします。

```
cd ~/Sites/laravel

valet link application
```

<!-- You may execute the `links` command to display a list of all of your linked directories: -->
`links` コマンドを実行して、リンクされたすべてのディレクトリのリストを表示できます。

<!--     valet links -->
    valet links

<!-- The `unlink` command may be used to destroy the symbolic link for a site: -->
`unlink` コマンドは、サイトのシンボリック リンクを破棄するために使用できます。

```
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
<!-- ### Securing Sites With TLS -->
### Securing Sites With TLS

<!-- By default, Valet serves sites over HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, you may use the `secure` command. For example, if your site is being served by Valet on the `laravel.test` domain, you should run the following command to secure it: -->
デフォルトでは、Valet は HTTP 経由でサイトを提供します。ただし、HTTP/2 を使用して暗号化された TLS 経由でサイトを提供したい場合は、`secure` コマンドを使用できます。たとえば、サイトが `laravel.test` ドメインの Valet によって提供されている場合は、次のコマンドを実行してサイトを保護する必要があります。

<!--     valet secure laravel -->
    valet secure laravel

<!-- To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the hostname that you wish to unsecure: -->
サイトの「保護を解除」し、プレーン HTTP 経由でトラフィックを提供する状態に戻すには、`unsecure` コマンドを使用します。 `secure` コマンドと同様に、このコマンドは保護を解除するホスト名を受け入れます。

<!--     valet unsecure laravel -->
    valet unsecure laravel

<a name="serving-a-default-site"></a>
<!-- ### Serving A Default Site -->
### Serving A Default Site

<!-- Sometimes, you may wish to configure Valet to serve a "default" site instead of a `404` when visiting an unknown `test` domain. To accomplish this, you may add a `default` option to your `~/.config/valet/config.json` configuration file containing the path to the site that should serve as your default site: -->
場合によっては、未知の `test` ドメインにアクセスしたときに、`404` ではなく「デフォルト」サイトを提供するように Valet を設定したい場合があります。これを実現するには、デフォルト サイトとして機能するサイトへのパスを含む `default` オプションを `~/.config/valet/config.json` 構成ファイルに追加します。

<!--     "default": "/Users/Sally/Sites/foo", -->
    "default": "/Users/Sally/Sites/foo",

<a name="sharing-sites"></a>
<!-- ## Sharing Sites -->
## Sharing Sites

<!-- Valet even includes a command to share your local sites with the world, providing an easy way to test your site on mobile devices or share it with team members and clients. -->
Valet には、ローカル サイトを世界と共有するコマンドも含まれており、モバイル デバイスでサイトをテストしたり、チーム メンバーやクライアントと共有したりする簡単な方法を提供します。

<a name="sharing-sites-via-ngrok"></a>
<!-- ### Sharing Sites Via Ngrok -->
### Sharing Sites Via Ngrok

<!-- To share a site, navigate to the site's directory in your terminal and run Valet's `share` command. A publicly accessible URL will be inserted into your clipboard and is ready to paste directly into your browser or share with your team: -->
サイトを共有するには、ターミナルでサイトのディレクトリに移動し、Valet の `share` コマンドを実行します。一般にアクセス可能な URL がクリップボードに挿入され、ブラウザに直接貼り付けたり、チームと共有したりできるようになります。

```
cd ~/Sites/laravel

valet share
```

<!-- To stop sharing your site, you may press `Control + C`. Sharing your site using Ngrok requires you to [create an Ngrok account](https://dashboard.ngrok.com/signup) and [setup an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken). -->
サイトの共有を停止するには、`Control + C` を押してください。 Ngrok を使用してサイトを共有するには、[create an Ngrok account](https://dashboard.ngrok.com/signup) および [setup an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken) を行う必要があります。

> [!TIP]
> `valet share --region=eu` など、追加の Ngrok パラメータを共有コマンドに渡すことができます。詳細については、[ngrok documentation](https://ngrok.com/docs) を参照してください。

<a name="sharing-sites-via-expose"></a>
<!-- ### Sharing Sites Via Expose -->
### Sharing Sites Via Expose

<!-- If you have [Expose](https://expose.dev) installed, you can share your site by navigating to the site's directory in your terminal and running the `expose` command. Consult the [Expose documentation](https://expose.dev/docs) for information regarding the additional command-line parameters it supports. After sharing the site, Expose will display the sharable URL that you may use on your other devices or amongst team members: -->
[Expose](https://expose.dev) がインストールされている場合は、ターミナルでサイトのディレクトリに移動し、`expose` コマンドを実行することで、サイトを共有できます。サポートされる追加のコマンドライン パラメーターに関する情報については、[Expose documentation](https://expose.dev/docs) を参照してください。サイトを共有すると、他のデバイスやチーム メンバー間で使用できる共有可能な URL が Expose に表示されます。

```
cd ~/Sites/laravel

expose
```

<!-- To stop sharing your site, you may press `Control + C`. -->
サイトの共有を停止するには、`Control + C` を押してください。

<a name="sharing-sites-on-your-local-network"></a>
<!-- ### Sharing Sites On Your Local Network -->
### Sharing Sites On Your Local Network

<!-- Valet restricts incoming traffic to the internal `127.0.0.1` interface by default so that your development machine isn't exposed to security risks from the Internet. -->
Valet は、開発マシンがインターネットからのセキュリティ リスクにさらされないように、デフォルトで内部 `127.0.0.1` インターフェイスへの受信トラフィックを制限します。

<!-- If you wish to allow other devices on your local network to access the Valet sites on your machine via your machine's IP address (eg: `192.168.1.10/application.test`), you will need to manually edit the appropriate Nginx configuration file for that site to remove the restriction on the `listen` directive. You should remove the `127.0.0.1:` prefix on the `listen` directive for ports 80 and 443. -->
ローカル ネットワーク上の他のデバイスがマシンの IP アドレス (例: `192.168.1.10/application.test`) を介してマシン上の Valet サイトにアクセスできるようにしたい場合は、そのサイトの適切な Nginx 構成ファイルを手動で編集して、`listen` ディレクティブの制限を削除する必要があります。ポート 80 および 443 の `listen` ディレクティブの `127.0.0.1:` プレフィックスを削除する必要があります。

<!-- If you have not run `valet secure` on the project, you can open up network access for all non-HTTPS sites by editing the `/usr/local/etc/nginx/valet/valet.conf` file. However, if you're serving the project site over HTTPS (you have run `valet secure` for the site) then you should edit the `~/.config/valet/Nginx/app-name.test` file. -->
プロジェクトで `valet secure` を実行していない場合は、`/usr/local/etc/nginx/valet/valet.conf` ファイルを編集することで、すべての非 HTTPS サイトへのネットワーク アクセスを開くことができます。ただし、HTTPS 経由でプロジェクト サイトを提供している場合 (サイトに対して `valet secure` を実行している場合)、`~/.config/valet/Nginx/app-name.test` ファイルを編集する必要があります。

<!-- Once you have updated your Nginx configuration, run the `valet restart` command to apply the configuration changes. -->
Nginx 構成を更新したら、`valet restart` コマンドを実行して構成の変更を適用します。

<a name="site-specific-environment-variables"></a>
<!-- ## Site Specific Environment Variables -->
## Site Specific Environment Variables

<!-- Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. This file should return an array of site / environment variable pairs which will be added to the global `$_SERVER` array for each site specified in the array: -->
他のフレームワークを使用する一部のアプリケーションはサーバー環境変数に依存する場合がありますが、それらの変数をプロジェクト内で構成する方法は提供されません。 Valet を使用すると、プロジェクトのルート内に `.valet-env.php` ファイルを追加することで、サイト固有の環境変数を構成できます。このファイルは、配列で指定された各サイトのグローバル `$_SERVER` 配列に追加されるサイト/環境変数のペアの配列を返す必要があります。

```
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
```

<a name="proxying-services"></a>
<!-- ## Proxying Services -->
## Proxying Services

<!-- Sometimes you may wish to proxy a Valet domain to another service on your local machine. For example, you may occasionally need to run Valet while also running a separate site in Docker; however, Valet and Docker can't both bind to port 80 at the same time. -->
Valet ドメインをローカル マシン上の別のサービスにプロキシしたい場合があります。たとえば、Docker で別のサイトを実行しながら、Valet を実行することが必要になる場合があります。ただし、Valet と Docker の両方を同時にポート 80 にバインドすることはできません。

<!-- To solve this, you may use the `proxy` command to generate a proxy. For example, you may proxy all traffic from `http://elasticsearch.test` to `http://127.0.0.1:9200`: -->
これを解決するには、`proxy` コマンドを使用してプロキシを生成します。たとえば、`http://elasticsearch.test` から `http://127.0.0.1:9200` へのすべてのトラフィックをプロキシできます。

```bash
// Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

// Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

<!-- You may remove a proxy using the `unproxy` command: -->
`unproxy` コマンドを使用してプロキシを削除できます。

<!--     valet unproxy elasticsearch -->
    valet unproxy elasticsearch

<!-- You may use the `proxies` command to list all site configurations that are proxied: -->
`proxies` コマンドを使用して、プロキシされているすべてのサイト構成を一覧表示できます。

<!--     valet proxies -->
    valet proxies

<a name="custom-valet-drivers"></a>
<!-- ## Custom Valet Drivers -->
## Custom Valet Drivers

<!-- You can write your own Valet "driver" to serve PHP applications running on a framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.config/valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`. -->
独自の Valet 「ドライバ」を作成して、Valet でネイティブにサポートされていないフレームワークまたは CMS 上で実行される PHP アプリケーションにサービスを提供することができます。 Valet をインストールすると、`SampleValetDriver.php` ファイルを含む `~/.config/valet/Drivers` ディレクトリが作成されます。このファイルには、カスタム ドライバの作成方法を示すサンプル ドライバ実装が含まれています。ドライバを作成するには、`serves`、`isStaticFile`、および `frontControllerPath` の 3 つのメソッドを実装するだけで済みます。

<!-- All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`). -->
3 つのメソッドはすべて、引数として `$sitePath`、`$siteName`、および `$uri` の値を受け取ります。 `$sitePath` は、`/Users/Lisa/Sites/my-project` など、マシン上で提供されているサイトへの完全修飾パスです。 `$siteName` は、ドメイン (`my-project`) の「ホスト」/「サイト名」部分です。 `$uri` は、受信リクエスト URI (`/foo/bar`) です。

<!-- Once you have completed your custom Valet driver, place it in the `~/.config/valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your filename should be `WordPressValetDriver.php`. -->
カスタム Valet ドライバが完成したら、`FrameworkValetDriver.php` 命名規則を使用して、それを `~/.config/valet/Drivers` ディレクトリに配置します。たとえば、WordPress 用のカスタム Valet ドライバを作成している場合、ファイル名は `WordPressValetDriver.php` にする必要があります。

<!-- Let's take a look at a sample implementation of each method your custom Valet driver should implement. -->
カスタム Valet ドライバが実装する必要がある各メソッドのサンプル実装を見てみましょう。

<a name="the-serves-method"></a>
<!-- #### The `serves` Method -->
#### The `serves` Method

<!-- The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method, you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve. -->
ドライバが受信リクエストを処理する必要がある場合、`serves` メソッドは `true` を返す必要があります。それ以外の場合、メソッドは `false` を返す必要があります。したがって、このメソッド内で、指定された `$sitePath` に、提供しようとしているタイプのプロジェクトが含まれているかどうかを判断する必要があります。

<!-- For example, let's imagine we are writing a `WordPressValetDriver`. Our `serves` method might look something like this: -->
たとえば、`WordPressValetDriver` を作成していると想像してみましょう。 `serves` メソッドは次のようになります。

```
/**
 * Determine if the driver serves the request.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return bool
 */
public function serves($sitePath, $siteName, $uri)
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
<!-- #### The `isStaticFile` Method -->
#### The `isStaticFile` Method

<!-- The `isStaticFile` should determine if the incoming request is for a file that is "static", such as an image or a stylesheet. If the file is static, the method should return the fully qualified path to the static file on disk. If the incoming request is not for a static file, the method should return `false`: -->
`isStaticFile` は、受信リクエストが画像やスタイルシートなどの「静的」ファイルに対するものであるかどうかを判断する必要があります。ファイルが静的な場合、メソッドはディスク上の静的ファイルへの完全修飾パスを返す必要があります。受信リクエストが静的ファイルに対するものではない場合、メソッドは `false` を返す必要があります。

```
/**
 * Determine if the incoming request is for a static file.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return string|false
 */
public function isStaticFile($sitePath, $siteName, $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!NOTE]
> `isStaticFile` メソッドは、受信リクエストに対して `serves` メソッドが `true` を返し、リクエスト URI が `/` ではない場合にのみ呼び出されます。

<a name="the-frontcontrollerpath-method"></a>
<!-- #### The `frontControllerPath` Method -->
#### The `frontControllerPath` Method

<!-- The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically an "index.php" file or equivalent: -->
`frontControllerPath` メソッドは、アプリケーションの「フロント コントローラ」への完全修飾パスを返す必要があります。通常は、「index.php」ファイルまたは同等のファイルです。

```
/**
 * Get the fully resolved path to the application's front controller.
 *
 * @param  string  $sitePath
 * @param  string  $siteName
 * @param  string  $uri
 * @return string
 */
public function frontControllerPath($sitePath, $siteName, $uri)
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
<!-- ### Local Drivers -->
### Local Drivers

<!-- If you would like to define a custom Valet driver for a single application, create a `LocalValetDriver.php` file in the application's root directory. Your custom driver may extend the base `ValetDriver` class or extend an existing application specific driver such as the `LaravelValetDriver`: -->
単一アプリケーションのカスタム Valet ドライバを定義する場合は、アプリケーションのルート ディレクトリに `LocalValetDriver.php` ファイルを作成します。カスタム ドライバは、基本 `ValetDriver` クラスを拡張することも、`LaravelValetDriver` などの既存のアプリケーション固有のドライバを拡張することもできます。

```
class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return bool
     */
    public function serves($sitePath, $siteName, $uri)
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string
     */
    public function frontControllerPath($sitePath, $siteName, $uri)
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
<!-- ## Other Valet Commands -->
## Other Valet Commands

<!--
Command  | Description
------------- | -------------
`valet forget` | Run this command from a "parked" directory to remove it from the parked directory list.
`valet log` | View a list of logs which are written by Valet's services.
`valet paths` | View all of your "parked" paths.
`valet restart` | Restart the Valet daemons.
`valet start` | Start the Valet daemons.
`valet stop` | Stop the Valet daemons.
`valet trust` | Add sudoers files for Brew and Valet to allow Valet commands to be run without prompting for your password.
`valet uninstall` | Uninstall Valet: shows instructions for manual uninstall. Pass the `--force` option to aggressively delete all of Valet's resources.
-->
コマンド |説明
------------- | -------------
`valet forget` | 「パーク」ディレクトリからこのコマンドを実行して、パーク ディレクトリ リストから削除します。
`valet log` | Valet のサービスによって書き込まれたログのリストを表示します。
`valet paths` |すべての「駐車」パスを表示します。
`valet restart` | Valet デーモンを再起動します。
`valet start` | Valet デーモンを開始します。
`valet stop` | Valet デーモンを停止します。
`valet trust` | Brew と Valet の sudoers ファイルを追加して、パスワードの入力を求めるプロンプトを表示せずに Valet コマンドを実行できるようにします。
`valet uninstall` | Valet のアンインストール: 手動アンインストールの手順を示します。 Valet のリソースをすべて積極的に削除するには、`--force` オプションを渡します。

<a name="valet-directories-and-files"></a>
<!-- ## Valet Directories & Files -->
## Valet Directories & Files

<!-- You may find the following directory and file information helpful while troubleshooting issues with your Valet environment: -->
Valet 環境の問題のトラブルシューティングを行う際には、次のディレクトリとファイルの情報が役立つ場合があります。

<!-- #### `~/.config/valet` -->
#### `~/.config/valet`

<!-- Contains all of Valet's configuration. You may wish to maintain a backup of this directory. -->
Valet のすべての設定が含まれています。このディレクトリのバックアップを保持しておくとよいでしょう。

<!-- #### `~/.config/valet/dnsmasq.d/` -->
#### `~/.config/valet/dnsmasq.d/`

<!-- This directory contains DNSMasq's configuration. -->
このディレクトリには DNSMasq の設定が含まれています。

<!-- #### `~/.config/valet/Drivers/` -->
#### `~/.config/valet/Drivers/`

<!-- This directory contains Valet's drivers. Drivers determine how a particular framework / CMS is served. -->
このディレクトリには Valet のドライバが含まれています。ドライバは、特定のフレームワーク/CMS がどのように提供されるかを決定します。

<!-- #### `~/.config/valet/Extensions/` -->
#### `~/.config/valet/Extensions/`

<!-- This directory contains custom Valet extensions / commands. -->
このディレクトリには、カスタム Valet 拡張機能/コマンドが含まれています。

<!-- #### `~/.config/valet/Nginx/` -->
#### `~/.config/valet/Nginx/`

<!-- This directory contains all of Valet's Nginx site configurations. These files are rebuilt when running the `install`, `secure`, and `tld` commands. -->
このディレクトリには、Valet の Nginx サイト構成がすべて含まれています。これらのファイルは、`install`、`secure`、および `tld` コマンドの実行時に再構築されます。

<!-- #### `~/.config/valet/Sites/` -->
#### `~/.config/valet/Sites/`

<!-- This directory contains all of the symbolic links for your [linked projects](#the-link-command). -->
このディレクトリには、[linked projects](#the-link-command) のすべてのシンボリック リンクが含まれています。

<!-- #### `~/.config/valet/config.json` -->
#### `~/.config/valet/config.json`

<!-- This file is Valet's master configuration file. -->
このファイルは、Valet のマスター構成ファイルです。

<!-- #### `~/.config/valet/valet.sock` -->
#### `~/.config/valet/valet.sock`

<!-- This file is the PHP-FPM socket used by Valet's Nginx installation. This will only exist if PHP is running properly. -->
このファイルは、Valet の Nginx インストールで使用される PHP-FPM ソケットです。これは、PHP が適切に実行されている場合にのみ存在します。

<!-- #### `~/.config/valet/Log/fpm-php.www.log` -->
#### `~/.config/valet/Log/fpm-php.www.log`

<!-- This file is the user log for PHP errors. -->
このファイルは、PHP エラーのユーザー ログです。

<!-- #### `~/.config/valet/Log/nginx-error.log` -->
#### `~/.config/valet/Log/nginx-error.log`

<!-- This file is the user log for Nginx errors. -->
このファイルは、Nginx エラーのユーザー ログです。

<!-- #### `/usr/local/var/log/php-fpm.log` -->
#### `/usr/local/var/log/php-fpm.log`

<!-- This file is the system log for PHP-FPM errors. -->
このファイルは、PHP-FPM エラーのシステム ログです。

<!-- #### `/usr/local/var/log/nginx` -->
#### `/usr/local/var/log/nginx`

<!-- This directory contains the Nginx access and error logs. -->
このディレクトリには、Nginx のアクセス ログとエラー ログが含まれます。

<!-- #### `/usr/local/etc/php/X.X/conf.d` -->
#### `/usr/local/etc/php/X.X/conf.d`

<!-- This directory contains the `*.ini` files for various PHP configuration settings. -->
このディレクトリには、さまざまな PHP 構成設定用の `*.ini` ファイルが含まれています。

<!-- #### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf` -->
#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

<!-- This file is the PHP-FPM pool configuration file. -->
このファイルは、PHP-FPM プール構成ファイルです。

<!-- #### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf` -->
#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

<!-- This file is the default Nginx configuration used for building SSL certificates for your sites. -->
このファイルは、サイトの SSL 証明書を構築するために使用されるデフォルトの Nginx 構成です。

