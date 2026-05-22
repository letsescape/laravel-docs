# Laravel Homestead (Laravel Homestead)

- [Introduction](#introduction)
- [インストールとセットアップ](#installation-and-setup)
    - [最初のステップ](#first-steps)
    - [Homesteadの構成](#configuring-homestead)
    - [Nginx サイトの構成](#configuring-nginx-sites)
    - [サービスの構成](#configuring-services)
    - [Vagrant Box の起動](#launching-the-vagrant-box)
    - [プロジェクトごとのインストール](#per-project-installation)
    - [オプション機能のインストール](#installing-optional-features)
    - [Aliases](#aliases)
- [Homesteadの更新](#updating-homestead)
- [毎日の使用量](#daily-usage)
    - [SSH経由で接続する](#connecting-via-ssh)
    - [サイトを追加する](#adding-additional-sites)
    - [環境変数](#environment-variables)
    - [Ports](#ports)
    - [PHPのバージョン](#php-versions)
    - [データベースへの接続](#connecting-to-databases)
    - [データベースのバックアップ](#database-backups)
    - [Cron スケジュールの構成](#configuring-cron-schedules)
    - [メールピットの構成](#configuring-mailpit)
    - [Minioの設定](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [環境を共有する](#sharing-your-environment)
- [デバッグとプロファイリング](#debugging-and-profiling)
    - [Xdebug を使用した Web リクエストのデバッグ](#debugging-web-requests)
    - [CLI アプリケーションのデバッグ](#debugging-cli-applications)
    - [Blackfire を使用したアプリケーションのプロファイリング](#profiling-applications-with-blackfire)
- [ネットワークインターフェース](#network-interfaces)
- [Homesteadの拡張](#extending-homestead)
- [プロバイダ固有の設定](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、ローカル開発環境を含む PHP 開発エクスペリエンス全体を楽しいものにするよう努めています。 [Laravel Homestead](https://github.com/laravel/homestead) は、パッケージ化された公式の Vagrant ボックスで、PHP、Web サーバー、またはその他のサーバー ソフトウェアをローカル マシンにインストールする必要なく、素晴らしい開発環境を提供します。

[Vagrant](https://www.vagrantup.com) は、仮想マシンを管理およびプロビジョニングするためのシンプルかつエレガントな方法を提供します。 Vagrant ボックスは完全に使い捨てです。何か問題が発生した場合は、数分でボックスを破壊して再作成できます。

Homestead は Windows、macOS、または Linux システム上で実行でき、Nginx、PHP、MySQL、PostgreSQL、Redis、Memcached、Node、および素晴らしい Laravel アプリケーションの開発に必要なその他のソフトウェアがすべて含まれています。

> [!WARNING]  
> Windows を使用している場合は、ハードウェア仮想化 (VT-x) を有効にする必要がある場合があります。通常、BIOS を介して有効にできます。 UEFI システムで Hyper-V を使用している場合は、VT-x にアクセスするために Hyper-V をさらに無効にする必要がある場合があります。

<a name="included-software"></a>
### 付属ソフトウェア

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Ubuntu 22.04
- Git
- PHP8.3
- PHP8.2
- PHP8.1
- PHP8.0
- PHP7.4
- PHP7.3
- PHP7.2
- PHP7.1
- PHP7.0
- PHP5.6
- Nginx
- MySQL 8.0
- うーん
- スクライト3
- PostgreSQL15
- 作曲家
- ドッカー
- ノード (Yarn、Bower、Grunt、Gulp あり)
- レディス
- Memcached
- 豆の木
- メールピット
- アバヒ
- ングロク
- Xデバッグ
- XHProf / タイドウェイ / XHGui
- wp-cli

</div>

<a name="optional-software"></a>
### オプションのソフトウェア

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- アパッチ
- ブラックファイア
- カサンドラ
- クロノグラフ
- カウチDB
- クリスタル＆ラッキーフレームワーク
- エラスティックサーチ
- イベントストアDB
- フライウェイ
- ギアマン
- 行く
- グラファナ
- 流入DB
- ログスタッシュ
- マリアDB
- メイリサーチ
- MinIO
- モンゴDB
- Neo4j
- オーマイザッシュ
- オープンレスティ
- PM2
- パイソン
- R
- ラビットMQ
- さび
- RVM (Ruby バージョン マネージャー)
- ソルル
- タイムスケールDB
- トレーダー <small>(PHP 拡張機能)</small>
- Webdriver と Laravel Dusk ユーティリティ

</div>

<a name="installation-and-setup"></a>
## インストールとセットアップ (Installation and Setup)

<a name="first-steps"></a>
### 最初のステップ

Homestead 環境を起動する前に、[Vagrant](https://developer.hashicorp.com/vagrant/downloads) と次のサポートされているプロバイダのいずれかをインストールする必要があります。

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

これらのソフトウェア パッケージはすべて、一般的なオペレーティング システムすべてに使いやすいビジュアル インストーラーを提供します。

Parallels プロバイダを使用するには、[Parallels Vagrant プラグイン](https://github.com/Parallels/vagrant-parallels) をインストールする必要があります。無料です。

<a name="installing-homestead"></a>
#### Homesteadの設置

Homestead リポジトリをホスト マシンに複製することで、Homestead をインストールできます。 Homestead仮想マシンはすべてのLaravelアプリケーションのホストとして機能するため、「ホーム」ディレクトリ内の`Homestead`フォルダーにリポジトリのクローンを作成することを検討してください。このドキュメントでは、このディレクトリを「Homestead ディレクトリ」と呼びます。

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead リポジトリのクローンを作成した後、`release` ブランチをチェックアウトする必要があります。このブランチには、Homestead の最新の安定リリースが常に含まれています。

```shell
cd ~/Homestead

git checkout release
```

次に、Homestead ディレクトリから `bash init.sh` コマンドを実行して、`Homestead.yaml` 構成ファイルを作成します。 `Homestead.yaml` ファイルは、Homestead インストールのすべての設定を構成する場所です。このファイルは Homestead ディレクトリに配置されます。

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homesteadの構成

<a name="setting-your-provider"></a>
#### プロバイダの設定

`Homestead.yaml` ファイル内の `provider` キーは、どの Vagrant プロバイダを使用する必要があるかを示します: `virtualbox` または `parallels`:

    provider: virtualbox

> [!WARNING]  
> Apple Silicon を使用している場合は、Parallels プロバイダが必要です。

<a name="configuring-shared-folders"></a>
#### 共有フォルダーの構成

`Homestead.yaml` ファイルの `folders` プロパティには、Homestead 環境と共有するすべてのフォルダーがリストされます。これらのフォルダー内のファイルが変更されると、ローカル マシンと Homestead 仮想環境の間で同期が維持されます。必要な数の共有フォルダーを構成できます。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]  
> Windows ユーザーは、`~/` パス構文を使用せず、代わりに `C:\Users\user\Code\project1` などのプロジェクトへのフル パスを使用する必要があります。

すべてのアプリケーションを含む単一の大きなディレクトリをマッピングするのではなく、常に個々のアプリケーションを独自のフォルダー マッピングにマッピングする必要があります。フォルダーをマップする場合、仮想マシンはフォルダー内の *すべての* ファイルのすべてのディスク IO を追跡する必要があります。フォルダー内に多数のファイルがある場合、パフォーマンスが低下する可能性があります。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]  
> Homestead を使用する場合は、`.` (現在のディレクトリ) をマウントしないでください。これにより、Vagrant は現在のフォルダーを `/vagrant` にマップせず、オプション機能が破損し、プロビジョニング中に予期しない結果が発生します。

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs) を有効にするには、フォルダー マッピングに `type` オプションを追加します。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]  
> Windows で NFS を使用する場合は、[vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) プラグインのインストールを検討する必要があります。このプラグインは、Homestead 仮想マシン内のファイルおよびディレクトリに対する正しいユーザー/グループ権限を維持します。

Vagrant の [同期されたフォルダー](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) でサポートされているオプションを `options` キーの下にリストすることで渡すこともできます。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "rsync"
      options:
          rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
          rsync__exclude: ["node_modules"]
```

<a name="configuring-nginx-sites"></a>
### Nginx サイトの構成

Nginx についてよく知りませんか?問題ない。 `Homestead.yaml` ファイルの `sites` プロパティを使用すると、Homestead 環境上のフォルダーに「ドメイン」を簡単にマップできます。サンプル サイト構成は、`Homestead.yaml` ファイルに含まれています。繰り返しますが、必要なだけサイトを Homestead 環境に追加できます。 Homestead は、作業しているすべての Laravel アプリケーションにとって便利な仮想化環境として機能します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Homestead 仮想マシンをプロビジョニングした後に `sites` プロパティを変更する場合は、ターミナルで `vagrant reload --provision` コマンドを実行して、仮想マシン上の Nginx 構成を更新する必要があります。

> [!WARNING]  
> Homestead スクリプトは、可能な限り冪等になるように構築されています。ただし、プロビジョニング中に問題が発生した場合は、`vagrant destroy && vagrant up` コマンドを実行してマシンを破棄し、再構築する必要があります。

<a name="hostname-resolution"></a>
#### ホスト名の解決

Homestead は、自動ホスト解決のために `mDNS` を使用してホスト名を公開します。 `Homestead.yaml` ファイルで `hostname: homestead` を設定すると、ホストは `homestead.local` で使用できるようになります。 macOS、iOS、および Linux デスクトップ ディストリビューションには、デフォルトで `mDNS` サポートが含まれています。 Windows を使用している場合は、[Windows 用 Bonjour 印刷サービス](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US) をインストールする必要があります。

自動ホスト名の使用は、Homestead の [プロジェクトごとのインストール](#per-project-installation) に最適です。単一の Homestead インスタンスで複数のサイトをホストする場合は、Web サイトの「ドメイン」をマシン上の `hosts` ファイルに追加できます。 `hosts` ファイルは、Homestead サイトへのリクエストを Homestead 仮想マシンにリダイレクトします。 macOS および Linux では、このファイルは `/etc/hosts` にあります。 Windows では、`C:\Windows\System32\drivers\etc\hosts` にあります。このファイルに追加する行は次のようになります。

    192.168.56.56  homestead.test

リストされている IP アドレスが、`Homestead.yaml` ファイルに設定されているものであることを確認してください。ドメインを `hosts` ファイルに追加し、Vagrant ボックスを起動すると、Web ブラウザ経由でサイトにアクセスできるようになります。

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### サービスの構成

Homestead はデフォルトでいくつかのサービスを開始します。ただし、プロビジョニング中にどのサービスを有効または無効にするかをカスタマイズできます。たとえば、`Homestead.yaml` ファイル内の `services` オプションを変更することで、PostgreSQL を有効にし、MySQL を無効にすることができます。

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

指定されたサービスは、`enabled` および `disabled` ディレクティブの順序に基づいて開始または停止されます。

<a name="launching-the-vagrant-box"></a>
### Vagrant Box の起動

`Homestead.yaml` を好みに合わせて編集したら、Homestead ディレクトリから `vagrant up` コマンドを実行します。 Vagrant は仮想マシンを起動し、共有フォルダーと Nginx サイトを自動的に構成します。

マシンを破壊するには、`vagrant destroy` コマンドを使用できます。

<a name="per-project-installation"></a>
### プロジェクトごとのインストール

Homestead をグローバルにインストールし、すべてのプロジェクトで同じ Homestead 仮想マシンを共有する代わりに、管理するプロジェクトごとに Homestead インスタンスを構成できます。プロジェクトに `Vagrantfile` を同梱したい場合は、プロジェクトごとに Homestead をインストールすると有益です。これにより、プロジェクトに取り組んでいる他のユーザーが、プロジェクトのリポジトリを複製した直後に `vagrant up` を利用できるようになります。

Composer パッケージ マネージャーを使用して Homestead をプロジェクトにインストールできます。

```shell
composer require laravel/homestead --dev
```

Homestead がインストールされたら、Homestead の `make` コマンドを呼び出して、プロジェクトの `Vagrantfile` および `Homestead.yaml` ファイルを生成します。これらのファイルはプロジェクトのルートに配置されます。 `make` コマンドは、`Homestead.yaml` ファイル内の `sites` および `folders` ディレクティブを自動的に構成します。

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

次に、ターミナルで `vagrant up` コマンドを実行し、ブラウザで `http://homestead.test` にあるプロジェクトにアクセスします。自動 [ホスト名の解決](#hostname-resolution) を使用していない場合は、`homestead.test` または選択したドメインの `/etc/hosts` ファイル エントリを追加する必要があることに注意してください。

<a name="installing-optional-features"></a>
### オプション機能のインストール

オプションのソフトウェアは、`Homestead.yaml` ファイル内の `features` オプションを使用してインストールされます。ほとんどの機能はブール値で有効または無効にできますが、一部の機能では複数の構成オプションが可能です。

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
    - cassandra: true
    - chronograf: true
    - couchdb: true
    - crystal: true
    - dragonflydb: true
    - elasticsearch:
        version: 7.9.0
    - eventstore: true
        version: 21.2.0
    - flyway: true
    - gearman: true
    - golang: true
    - grafana: true
    - influxdb: true
    - logstash: true
    - mariadb: true
    - meilisearch: true
    - minio: true
    - mongodb: true
    - neo4j: true
    - ohmyzsh: true
    - openresty: true
    - pm2: true
    - python: true
    - r-base: true
    - rabbitmq: true
    - rustc: true
    - rvm: true
    - solr: true
    - timescaledb: true
    - trader: true
    - webdriver: true
```

<a name="elasticsearch"></a>
#### エラスティックサーチ

Elasticsearch のサポートされているバージョンを指定できます。これは正確なバージョン番号 (major.minor.patch) である必要があります。デフォルトのインストールでは、「homestead」という名前のクラスターが作成されます。 Elasticsearch にはオペレーティング システムのメモリの半分を超えて割り当てないでください。そのため、Homestead 仮想マシンには少なくとも 2 倍の Elasticsearch 割り当てがあることを確認してください。

> [!NOTE]  
> 構成をカスタマイズする方法については、[Elasticsearch ドキュメント](https://www.elastic.co/guide/en/elasticsearch/reference/current) を確認してください。

<a name="mariadb"></a>
#### マリアDB

MariaDB を有効にすると、MySQL が削除され、MariaDB がインストールされます。 MariaDB は通常、MySQL のドロップイン代替として機能するため、アプリケーションのデータベース構成では引き続き `mysql` データベース ドライバを使用する必要があります。

<a name="mongodb"></a>
#### モンゴDB

デフォルトの MongoDB インストールでは、データベースのユーザー名が `homestead` に設定され、対応するパスワードが `secret` に設定されます。

<a name="neo4j"></a>
#### Neo4j

デフォルトの Neo4j インストールでは、データベースのユーザー名が `homestead` に設定され、対応するパスワードが `secret` に設定されます。 Neo4j ブラウザにアクセスするには、Web ブラウザから `http://homestead.test:7474` にアクセスします。ポート `7687` (Bolt)、`7474` (HTTP)、および `7473` (HTTPS) は、Neo4j クライアントからのリクエストを処理する準備ができています。

<a name="aliases"></a>
### 別名

Homestead ディレクトリ内の `aliases` ファイルを変更することで、Homestead 仮想マシンに Bash エイリアスを追加できます。

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` ファイルを更新した後、`vagrant reload --provision` コマンドを使用して Homestead 仮想マシンを再プロビジョニングする必要があります。これにより、新しいエイリアスがマシン上で確実に使用できるようになります。

<a name="updating-homestead"></a>
## Homesteadの更新 (Updating Homestead)

Homestead の更新を開始する前に、Homestead ディレクトリで次のコマンドを実行して、現在の仮想マシンが削除されていることを確認する必要があります。

```shell
vagrant destroy
```

次に、Homestead ソース コードを更新する必要があります。リポジトリのクローンを作成した場合は、最初にリポジトリのクローンを作成した場所で次のコマンドを実行できます。

```shell
git fetch

git pull origin release
```

これらのコマンドは、GitHub リポジトリから最新の Homestead コードをプルし、最新のタグを取得して、最新のタグ付きリリースをチェックアウトします。最新の安定リリース バージョンは、Homestead の [GitHub リリースページ](https://github.com/laravel/homestead/releases) で見つけることができます。

プロジェクトの `composer.json` ファイルを介して Homestead をインストールした場合は、`composer.json` ファイルに `"laravel/homestead": "^12"` が含まれていることを確認し、依存関係を更新する必要があります。

```shell
composer update
```

次に、`vagrant box update` コマンドを使用して Vagrant ボックスを更新する必要があります。

```shell
vagrant box update
```

Vagrant ボックスを更新した後、Homestead ディレクトリから `bash init.sh` コマンドを実行して、Homestead の追加構成ファイルを更新する必要があります。既存の `Homestead.yaml`、`after.sh`、および `aliases` ファイルを上書きするかどうかを尋ねられます。

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

最後に、最新の Vagrant インストールを利用するには、Homestead 仮想マシンを再生成する必要があります。

```shell
vagrant up
```

<a name="daily-usage"></a>
## 毎日の使用量 (Daily Usage)

<a name="connecting-via-ssh"></a>
### SSH経由で接続する

Homestead ディレクトリから `vagrant ssh` ターミナル コマンドを実行することで、仮想マシンに SSH 接続できます。

<a name="adding-additional-sites"></a>
### サイトを追加する

Homestead 環境がプロビジョニングされて実行されたら、他の Laravel プロジェクト用に Nginx サイトを追加することもできます。単一の Homestead 環境では、必要なだけ Laravel プロジェクトを実行できます。追加のサイトを追加するには、そのサイトを `Homestead.yaml` ファイルに追加します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]  
> サイトを追加する前に、プロジェクトのディレクトリに [フォルダマッピング](#configuring-shared-folders) が設定されていることを確認する必要があります。

Vagrant が「hosts」ファイルを自動的に管理しない場合は、そのファイルに新しいサイトを追加する必要がある場合もあります。 macOS および Linux では、このファイルは `/etc/hosts` にあります。 Windows では、`C:\Windows\System32\drivers\etc\hosts` にあります。

    192.168.56.56  homestead.test
    192.168.56.56  another.test

サイトが追加されたら、Homestead ディレクトリから `vagrant reload --provision` ターミナル コマンドを実行します。

<a name="site-types"></a>
#### サイトの種類

Homestead は、Laravel に基づいていないプロジェクトを簡単に実行できるようにするいくつかの「タイプ」のサイトをサポートしています。たとえば、`statamic` サイト タイプを使用して、Static アプリケーションを Homestead に簡単に追加できます。

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

利用可能なサイト タイプは次のとおりです: `apache`、`apache-proxy`、`apigility`、`expressive`、`laravel` (デフォルト)、`proxy` (nginx の場合)、`silverstripe`、`statamic`、`symfony2`、 `symfony4`、および `zf`。

<a name="site-parameters"></a>
#### サイトパラメータ

`params` サイト ディレクティブを使用して、追加の Nginx `fastcgi_param` 値をサイトに追加できます。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 環境変数

グローバル環境変数を `Homestead.yaml` ファイルに追加することで定義できます。

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` ファイルを更新した後、必ず `vagrant reload --provision` コマンドを実行してマシンを再プロビジョニングしてください。これにより、インストールされているすべての PHP バージョンの PHP-FPM 構成が更新され、`vagrant` ユーザーの環境も更新されます。

<a name="ports"></a>
### ポート

デフォルトでは、次のポートが Homestead 環境に転送されます。

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80 に転送
- **HTTPS:** 44300 → 443 に転送

</div>

<a name="forwarding-additional-ports"></a>
#### 追加ポートの転送

必要に応じて、`Homestead.yaml` ファイル内で `ports` 構成エントリを定義することで、追加のポートを Vagrant ボックスに転送できます。 `Homestead.yaml` ファイルを更新した後、必ず `vagrant reload --provision` コマンドを実行してマシンを再プロビジョニングしてください。

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

以下は、ホスト マシンから Vagrant ボックスにマッピングする追加の Homestead サービス ポートのリストです。

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22 へ
- **ngrok UI:** 4040 → 4040 へ
- **MySQL:** 33060 → 3306 へ
- **PostgreSQL:** 54320 → 5432 へ
- **MongoDB:** 27017 → 27017 へ
- **メールピット:** 8025 → 8025 へ
- **ミニオ:** 9600 → 9600へ

</div>

<a name="php-versions"></a>
### PHPのバージョン

Homestead は、同じ仮想マシン上で複数のバージョンの PHP の実行をサポートします。 `Homestead.yaml` ファイル内の特定のサイトで使用する PHP のバージョンを指定できます。利用可能な PHP バージョンは、「5.6」、「7.0」、「7.1」、「7.2」、「7.3」、「7.4」、「8.0」、「8.1」、「8.2」、および「8.3」 (デフォルト) です。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 仮想マシン内](#connecting-via-ssh)、CLI 経由でサポートされている PHP バージョンのいずれかを使用できます。

```shell
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
php8.2 artisan list
php8.3 artisan list
```

Homestead 仮想マシン内から次のコマンドを発行することで、CLI で使用される PHP のデフォルト バージョンを変更できます。

```shell
php56
php70
php71
php72
php73
php74
php80
php81
php82
php83
```

<a name="connecting-to-databases"></a>
### データベースへの接続

`homestead` データベースは、すぐに MySQL と PostgreSQL の両方用に構成されています。ホスト マシンのデータベース クライアントから MySQL または PostgreSQL データベースに接続するには、ポート `33060` (MySQL) または `54320` (PostgreSQL) の `127.0.0.1` に接続する必要があります。両方のデータベースのユーザー名とパスワードは、`homestead` / `secret` です。

> [!WARNING]  
> これらの非標準ポートは、ホスト マシンからデータベースに接続する場合にのみ使用してください。 Laravel は仮想マシン内で実行されているため、Laravel アプリケーションの `database` 構成ファイルではデフォルトの 3306 ポートと 5432 ポートを使用します。

<a name="database-backups"></a>
### データベースのバックアップ

Homestead 仮想マシンが破壊された場合、Homestead はデータベースを自動的にバックアップできます。この機能を利用するには、Vagrant 2.1.0 以降を使用する必要があります。または、古いバージョンの Vagrant を使用している場合は、`vagrant-triggers` プラグインをインストールする必要があります。データベースの自動バックアップを有効にするには、`Homestead.yaml` ファイルに次の行を追加します。

    backup: true

構成が完了すると、`vagrant destroy` コマンドの実行時に、Homestead はデータベースを `.backup/mysql_backup` および `.backup/postgres_backup` ディレクトリにエクスポートします。これらのディレクトリは、Homestead をインストールしたフォルダー、または [プロジェクトのインストールごとに](#per-project-installation) メソッドを使用している場合はプロジェクトのルートにあります。

<a name="configuring-cron-schedules"></a>
### Cron スケジュールの構成

Laravel は、単一の `schedule:run` Artisan コマンドを毎分実行するようにスケジュールすることで、[cron ジョブをスケジュールする](/docs/{{version}}/scheduling) を実行する便利な方法を提供します。 `schedule:run` コマンドは、`App\Console\Kernel` クラスで定義されたジョブ スケジュールを調べて、実行するスケジュールされたタスクを決定します。

Homestead サイトに対して `schedule:run` コマンドを実行したい場合は、サイトを定義するときに `schedule` オプションを `true` に設定します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

サイトの cron ジョブは、Homestead 仮想マシンの `/etc/cron.d` ディレクトリで定義されます。

<a name="configuring-mailpit"></a>
### メールピットの構成

[Mailpit](https://github.com/axllent/mailpit) を使用すると、実際に受信者にメールを送信せずに、送信電子メールを傍受して検査できます。まず、次のメール設定を使用するようにアプリケーションの `.env` ファイルを更新します。

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit が構成されたら、`http://localhost:8025` で Mailpit ダッシュボードにアクセスできます。

<a name="configuring-minio"></a>
### Minioの設定

[Minio](https://github.com/minio/minio) は、Amazon S3 互換 API を備えたオープンソースのオブジェクト ストレージ サーバーです。 Minio をインストールするには、[features](#installing-optional-features) セクションの次の構成オプションを使用して `Homestead.yaml` ファイルを更新します。

    minio: true

デフォルトでは、Minio はポート 9600 で使用できます。`http://localhost:9600` にアクセスすると、Minio コントロール パネルにアクセスできます。デフォルトのアクセスキーは `homestead` で、デフォルトの秘密キーは `secretkey` です。 Minio にアクセスするときは、常にリージョン `us-east-1` を使用する必要があります。

Minio を使用するには、アプリケーションの `config/filesystems.php` 構成ファイルで S3 ディスク構成を調整する必要があります。ディスク構成に `use_path_style_endpoint` オプションを追加し、`url` キーを `endpoint` に変更する必要があります。

    's3' => [
        'driver' => 's3',
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
        'endpoint' => env('AWS_URL'),
        'use_path_style_endpoint' => true,
    ]

最後に、`.env` ファイルに次のオプションがあることを確認します。

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

Minio を利用した「S3」バケットをプロビジョニングするには、`buckets` ディレクティブを `Homestead.yaml` ファイルに追加します。バケットを定義した後、ターミナルで `vagrant reload --provision` コマンドを実行する必要があります。

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

サポートされている `policy` 値には、`none`、`download`、`upload`、および `public` が含まれます。

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 内で [Laravel Dusk](/docs/{{version}}/dusk) テストを実行するには、Homestead 構成で [`webdriver` 機能](#installing-optional-features) を有効にする必要があります。

```yaml
features:
    - webdriver: true
```

`webdriver` 機能を有効にした後、端末で `vagrant reload --provision` コマンドを実行する必要があります。

<a name="sharing-your-environment"></a>
### 環境を共有する

現在取り組んでいることを同僚やクライアントと共有したい場合があります。 Vagrant には、`vagrant share` コマンドを介したこれに対するサポートが組み込まれています。ただし、`Homestead.yaml` ファイルで複数のサイトが構成されている場合、これは機能しません。

この問題を解決するために、Homestead には独自の `share` コマンドが含まれています。開始するには、`vagrant ssh` 経由で [Homestead 仮想マシンに SSH で接続します](#connecting-via-ssh) を実行し、`share homestead.test` コマンドを実行します。このコマンドは、`Homestead.yaml` 構成ファイルから `homestead.test` サイトを共有します。 `homestead.test` の代わりに、他の構成済みサイトを使用できます。

```shell
share homestead.test
```

コマンドを実行すると、アクティビティ ログと共有サイトの一般にアクセス可能な URL を含む Ngrok 画面が表示されます。カスタム リージョン、サブドメイン、またはその他の Ngrok ランタイム オプションを指定したい場合は、それらを `share` コマンドに追加できます。

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTP ではなく HTTPS でコンテンツを共有する必要がある場合は、`share` の代わりに `sshare` コマンドを使用すると、これが可能になります。

> [!WARNING]  
> Vagrant は本質的に安全ではないため、`share` コマンドを実行すると仮想マシンがインターネットに公開されることになることに注意してください。

<a name="debugging-and-profiling"></a>
## デバッグとプロファイリング (Debugging and Profiling)

<a name="debugging-web-requests"></a>
### Xdebug を使用した Web リクエストのデバッグ

Homestead には、[Xdebug](https://xdebug.org) を使用したステップ デバッグのサポートが含まれています。たとえば、ブラウザでページにアクセスすると、PHP が IDE に接続して、実行中のコードを検査および変更できるようになります。

デフォルトでは、Xdebug はすでに実行されており、接続を受け入れる準備ができています。 CLI で Xdebug を有効にする必要がある場合は、Homestead 仮想マシン内で `sudo phpenmod xdebug` コマンドを実行します。次に、IDE の指示に従ってデバッグを有効にします。最後に、拡張機能または [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/) を使用して Xdebug をトリガーするようにブラウザを設定します。

> [!WARNING]  
> Xdebug により、PHP の実行が大幅に遅くなります。 Xdebug を無効にするには、Homestead 仮想マシン内で `sudo phpdismod xdebug` を実行し、FPM サービスを再起動します。

<a name="autostarting-xdebug"></a>
#### Xdebugの自動起動

Web サーバーにリクエストを行う機能テストをデバッグする場合、カスタム ヘッダーまたは Cookie を通過するようにテストを変更してデバッグをトリガーするよりも、デバッグを自動開始する方が簡単です。 Xdebug を強制的に自動的に開始するには、Homestead 仮想マシン内の `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` ファイルを変更し、次の構成を追加します。

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI アプリケーションのデバッグ

PHP CLI アプリケーションをデバッグするには、Homestead 仮想マシン内で `xphp` シェル エイリアスを使用します。

    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
### Blackfire を使用したアプリケーションのプロファイリング

[Blackfire](https://blackfire.io/docs/introduction) は、Web リクエストと CLI アプリケーションをプロファイリングするためのサービスです。コールグラフとタイムラインにプロファイル データを表示する対話型ユーザー インターフェイスを提供します。これは、開発、ステージング、実稼働で使用するために構築されており、エンドユーザーにオーバーヘッドはかかりません。さらに、Blackfire は、コードおよび `php.ini` 構成設定のパフォーマンス、品質、セキュリティ チェックを提供します。

[ブラックファイアプレイヤー](https://blackfire.io/docs/player/index) は、プロファイリング シナリオをスクリプト化するために Blackfire と連携できるオープンソースの Web クローリング、Web テスト、および Web スクレイピング アプリケーションです。

Blackfire を有効にするには、Homestead 構成ファイルの「features」設定を使用します。

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire サーバー認証情報とクライアント認証情報 [Blackfire アカウントが必要です](https://blackfire.io/signup)。 Blackfire は、CLI ツールやブラウザ拡張機能など、アプリケーションをプロファイリングするためのさまざまなオプションを提供します。 [詳細については、Blackfire のドキュメントを参照してください。](https://blackfire.io/docs/php/integrations/laravel/index) してください。

<a name="network-interfaces"></a>
## ネットワークインターフェース (Network Interfaces)

`Homestead.yaml` ファイルの `networks` プロパティは、Homestead 仮想マシンのネットワーク インターフェイスを構成します。必要な数のインターフェイスを構成できます。

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) インターフェイスを有効にするには、ネットワークの `bridge` 設定を構成し、ネットワーク タイプを `public_network` に変更します。

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp) を有効にするには、構成から `ip` オプションを削除するだけです。

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

ネットワークが使用しているデバイスを更新するには、ネットワークの構成に `dev` オプションを追加します。デフォルトの `dev` 値は `eth0` です。

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homesteadの拡張 (Extending Homestead)

Homestead ディレクトリのルートにある `after.sh` スクリプトを使用して Homestead を拡張できます。このファイル内に、仮想マシンを適切に構成およびカスタマイズするために必要なシェル コマンドを追加できます。

Homestead をカスタマイズするとき、Ubuntu はパッケージの元の構成を保持するか、新しい構成ファイルで上書きするかを尋ねる場合があります。これを回避するには、パッケージをインストールするときに次のコマンドを使用して、Homestead によって以前に書き込まれた構成が上書きされないようにする必要があります。

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### ユーザーのカスタマイズ

チームで Homestead を使用する場合、個人の開発スタイルに合わせて Homestead を微調整することができます。これを実現するには、Homestead ディレクトリのルート (`Homestead.yaml` ファイルが含まれているのと同じディレクトリ) に `user-customizations.sh` ファイルを作成します。このファイル内で、必要なカスタマイズを行うことができます。ただし、`user-customizations.sh` はバージョン管理しないでください。

<a name="provider-specific-settings"></a>
## プロバイダ固有の設定 (Provider Specific Settings)

<a name="provider-specific-virtualbox"></a>
### バーチャルボックス

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

デフォルトでは、Homestead は `natdnshostresolver` 設定を `on` に構成します。これにより、Homestead はホスト オペレーティング システムの DNS 設定を使用できるようになります。この動作をオーバーライドする場合は、次の構成オプションを `Homestead.yaml` ファイルに追加します。

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

