<!-- # Laravel Homestead -->
# Laravel Homestead

- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
    - [First Steps](#first-steps)
    - [Configuring Homestead](#configuring-homestead)
    - [Configuring Nginx Sites](#configuring-nginx-sites)
    - [Configuring Services](#configuring-services)
    - [Launching the Vagrant Box](#launching-the-vagrant-box)
    - [Per Project Installation](#per-project-installation)
    - [Installing Optional Features](#installing-optional-features)
    - [Aliases](#aliases)
- [Updating Homestead](#updating-homestead)
- [Daily Usage](#daily-usage)
    - [Connecting via SSH](#connecting-via-ssh)
    - [Adding Additional Sites](#adding-additional-sites)
    - [Environment Variables](#environment-variables)
    - [Ports](#ports)
    - [PHP Versions](#php-versions)
    - [Connecting to Databases](#connecting-to-databases)
    - [Database Backups](#database-backups)
    - [Configuring Cron Schedules](#configuring-cron-schedules)
    - [Configuring Mailpit](#configuring-mailpit)
    - [Configuring Minio](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [Sharing Your Environment](#sharing-your-environment)
- [Debugging and Profiling](#debugging-and-profiling)
    - [Debugging Web Requests With Xdebug](#debugging-web-requests)
    - [Debugging CLI Applications](#debugging-cli-applications)
    - [Profiling Applications With Blackfire](#profiling-applications-with-blackfire)
- [Network Interfaces](#network-interfaces)
- [Extending Homestead](#extending-homestead)
- [Provider Specific Settings](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!WARNING]
> Laravel Homestead は、現在は積極的にメンテナンスされていないレガシー パッケージです。 [Laravel Sail](/docs/master/sail) は最新の代替手段として使用できます。

<!-- Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, or any other server software on your local machine. -->
Laravel は、ローカル開発環境を含む PHP 開発エクスペリエンス全体を楽しいものにするよう努めています。 [Laravel Homestead](https://github.com/laravel/homestead) は、パッケージ化された公式の Vagrant ボックスで、PHP、Web サーバー、またはその他のサーバー ソフトウェアをローカル マシンにインストールする必要なく、素晴らしい開発環境を提供します。

<!-- [Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes! -->
[Vagrant](https://www.vagrantup.com) は、仮想マシンを管理およびプロビジョニングするためのシンプルかつエレガントな方法を提供します。 Vagrant ボックスは完全に使い捨てです。何か問題が発生した場合は、数分でボックスを破壊して再作成できます。

<!-- Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications. -->
Homestead は Windows、macOS、または Linux システム上で実行でき、Nginx、PHP、MySQL、PostgreSQL、Redis、Memcached、Node、および素晴らしい Laravel アプリケーションの開発に必要なその他のソフトウェアがすべて含まれています。

> [!WARNING]
> Windows を使用している場合は、ハードウェア仮想化 (VT-x) を有効にする必要がある場合があります。通常、BIOS を介して有効にできます。 UEFI システムで Hyper-V を使用している場合は、VT-x にアクセスするために Hyper-V をさらに無効にする必要がある場合があります。

<a name="included-software"></a>
<!-- ### Included Software -->
### Included Software

<!-- <div id="software-list" markdown="1"> -->
<div id="software-list" markdown="1">

<!--
- Ubuntu 22.04
- Git
- PHP 8.3
- PHP 8.2
- PHP 8.1
- PHP 8.0
- PHP 7.4
- PHP 7.3
- PHP 7.2
- PHP 7.1
- PHP 7.0
- PHP 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 15
- Composer
- Docker
- Node (With Yarn, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli
-->
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
- lmm
- Sqlite3
- PostgreSQL15
- Composer
- Docker
- ノード (Yarn、Bower、Grunt、Gulp あり)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

<!-- </div> -->
</div>

<a name="optional-software"></a>
<!-- ### Optional Software -->
### Optional Software

<!-- <div id="software-list" markdown="1"> -->
<div id="software-list" markdown="1">

<!--
- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP extension)</small>
- Webdriver & Laravel Dusk Utilities
-->
- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP 拡張機能)</small>
- Webdriver と Laravel Dusk ユーティリティ

<!-- </div> -->
</div>

<a name="installation-and-setup"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- Before launching your Homestead environment, you must install [Vagrant](https://developer.hashicorp.com/vagrant/downloads) as well as one of the following supported providers: -->
Homestead 環境を起動する前に、[Vagrant](https://developer.hashicorp.com/vagrant/downloads) と次のサポートされているプロバイダのいずれかをインストールする必要があります。

<!--
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)
-->
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

<!-- All of these software packages provide easy-to-use visual installers for all popular operating systems. -->
これらのソフトウェア パッケージはすべて、一般的なオペレーティング システムすべてに使いやすいビジュアル インストーラーを提供します。

<!-- To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge. -->
Parallels プロバイダを使用するには、[Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels) をインストールする必要があります。無料です。

<a name="installing-homestead"></a>
<!-- #### Installing Homestead -->
#### Installing Homestead

<!-- You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory": -->
Homestead リポジトリをホスト マシンに複製することで、Homestead をインストールできます。 Homestead仮想マシンはすべてのLaravelアプリケーションのホストとして機能するため、「ホーム」ディレクトリ内の`Homestead`フォルダーにリポジトリのクローンを作成することを検討してください。このドキュメントでは、このディレクトリを「Homestead ディレクトリ」と呼びます。

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

<!-- After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead: -->
Laravel Homestead リポジトリのクローンを作成した後、`release` ブランチをチェックアウトする必要があります。このブランチには、Homestead の最新の安定リリースが常に含まれています。

```shell
cd ~/Homestead

git checkout release
```

<!-- Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory: -->
次に、Homestead ディレクトリから `bash init.sh` コマンドを実行して、`Homestead.yaml` 構成ファイルを作成します。 `Homestead.yaml` ファイルは、Homestead インストールのすべての設定を構成する場所です。このファイルは Homestead ディレクトリに配置されます。

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
<!-- ### Configuring Homestead -->
### Configuring Homestead

<a name="setting-your-provider"></a>
<!-- #### Setting Your Provider -->
#### Setting Your Provider

<!-- The `provider` key in your `Homestead.yaml` file indicates which Vagrant provider should be used: `virtualbox` or `parallels`: -->
`Homestead.yaml` ファイル内の `provider` キーは、どの Vagrant プロバイダを使用する必要があるかを示します: `virtualbox` または `parallels`:

```
provider: virtualbox
```

> [!WARNING]
> Apple Silicon を使用している場合は、Parallels プロバイダが必要です。

<a name="configuring-shared-folders"></a>
<!-- #### Configuring Shared Folders -->
#### Configuring Shared Folders

<!-- The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary: -->
`Homestead.yaml` ファイルの `folders` プロパティには、Homestead 環境と共有するすべてのフォルダーがリストされます。これらのフォルダー内のファイルが変更されると、ローカル マシンと Homestead 仮想環境の間で同期が維持されます。必要な数の共有フォルダーを構成できます。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows ユーザーは、`~/` パス構文を使用せず、代わりに `C:\Users\user\Code\project1` などのプロジェクトへのフル パスを使用する必要があります。

<!-- You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder: -->
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

<!-- To enable [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), you may add a `type` option to your folder mapping: -->
[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs) を有効にするには、フォルダー マッピングに `type` オプションを追加します。

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows で NFS を使用する場合は、[vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) プラグインのインストールを検討する必要があります。このプラグインは、Homestead 仮想マシン内のファイルおよびディレクトリに対する正しいユーザー/グループ権限を維持します。

<!-- You may also pass any options supported by Vagrant's [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) by listing them under the `options` key: -->
Vagrant の [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) でサポートされているオプションを `options` キーの下にリストすることで渡すこともできます。

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
<!-- ### Configuring Nginx Sites -->
### Configuring Nginx Sites

<!-- Not familiar with Nginx? No problem. Your `Homestead.yaml` file's `sites` property allows you to easily map a "domain" to a folder on your Homestead environment. A sample site configuration is included in the `Homestead.yaml` file. Again, you may add as many sites to your Homestead environment as necessary. Homestead can serve as a convenient, virtualized environment for every Laravel application you are working on: -->
Nginx についてよく知りませんか?問題ない。 `Homestead.yaml` ファイルの `sites` プロパティを使用すると、Homestead 環境上のフォルダーに「ドメイン」を簡単にマップできます。サンプル サイト構成は、`Homestead.yaml` ファイルに含まれています。繰り返しますが、必要なだけサイトを Homestead 環境に追加できます。 Homestead は、作業しているすべての Laravel アプリケーションにとって便利な仮想化環境として機能します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

<!-- If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine. -->
Homestead 仮想マシンをプロビジョニングした後に `sites` プロパティを変更する場合は、ターミナルで `vagrant reload --provision` コマンドを実行して、仮想マシン上の Nginx 構成を更新する必要があります。

> [!WARNING]
> Homestead スクリプトは、可能な限り冪等になるように構築されています。ただし、プロビジョニング中に問題が発生した場合は、`vagrant destroy && vagrant up` コマンドを実行してマシンを破棄し、再構築する必要があります。

<a name="hostname-resolution"></a>
<!-- #### Hostname Resolution -->
#### Hostname Resolution

<!-- Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US). -->
Homestead は、自動ホスト解決のために `mDNS` を使用してホスト名を公開します。 `Homestead.yaml` ファイルで `hostname: homestead` を設定すると、ホストは `homestead.local` で使用できるようになります。 macOS、iOS、および Linux デスクトップ ディストリビューションには、デフォルトで `mDNS` サポートが含まれています。 Windows を使用している場合は、[Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US) をインストールする必要があります。

<!-- Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following: -->
自動ホスト名の使用は、Homestead の [per project installations](#per-project-installation) に最適です。単一の Homestead インスタンスで複数のサイトをホストする場合は、Web サイトの「ドメイン」をマシン上の `hosts` ファイルに追加できます。 `hosts` ファイルは、Homestead サイトへのリクエストを Homestead 仮想マシンにリダイレクトします。 macOS および Linux では、このファイルは `/etc/hosts` にあります。 Windows では、`C:\Windows\System32\drivers\etc\hosts` にあります。このファイルに追加する行は次のようになります。

```text
192.168.56.56  homestead.test
```

<!-- Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser: -->
リストされている IP アドレスが、`Homestead.yaml` ファイルに設定されているものであることを確認してください。ドメインを `hosts` ファイルに追加し、Vagrant ボックスを起動すると、Web ブラウザ経由でサイトにアクセスできるようになります。

```shell
http://homestead.test
```

<a name="configuring-services"></a>
<!-- ### Configuring Services -->
### Configuring Services

<!-- Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file: -->
Homestead はデフォルトでいくつかのサービスを開始します。ただし、プロビジョニング中にどのサービスを有効または無効にするかをカスタマイズできます。たとえば、`Homestead.yaml` ファイル内の `services` オプションを変更することで、PostgreSQL を有効にし、MySQL を無効にすることができます。

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

<!-- The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives. -->
指定されたサービスは、`enabled` および `disabled` ディレクティブの順序に基づいて開始または停止されます。

<a name="launching-the-vagrant-box"></a>
<!-- ### Launching the Vagrant Box -->
### Launching the Vagrant Box

<!-- Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites. -->
`Homestead.yaml` を好みに合わせて編集したら、Homestead ディレクトリから `vagrant up` コマンドを実行します。 Vagrant は仮想マシンを起動し、共有フォルダーと Nginx サイトを自動的に構成します。

<!-- To destroy the machine, you may use the `vagrant destroy` command. -->
マシンを破壊するには、`vagrant destroy` コマンドを使用できます。

<a name="per-project-installation"></a>
<!-- ### Per Project Installation -->
### Per Project Installation

<!-- Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository. -->
Homestead をグローバルにインストールし、すべてのプロジェクトで同じ Homestead 仮想マシンを共有する代わりに、管理するプロジェクトごとに Homestead インスタンスを構成できます。プロジェクトに `Vagrantfile` を同梱したい場合は、プロジェクトごとに Homestead をインストールすると有益です。これにより、プロジェクトに取り組んでいる他のユーザーが、プロジェクトのリポジトリを複製した直後に `vagrant up` を利用できるようになります。

<!-- You may install Homestead into your project using the Composer package manager: -->
Composer パッケージ マネージャーを使用して Homestead をプロジェクトにインストールできます。

```shell
composer require laravel/homestead --dev
```

<!-- Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file: -->
Homestead がインストールされたら、Homestead の `make` コマンドを呼び出して、プロジェクトの `Vagrantfile` および `Homestead.yaml` ファイルを生成します。これらのファイルはプロジェクトのルートに配置されます。 `make` コマンドは、`Homestead.yaml` ファイル内の `sites` および `folders` ディレクティブを自動的に構成します。

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

<!-- Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution). -->
次に、ターミナルで `vagrant up` コマンドを実行し、ブラウザで `http://homestead.test` にあるプロジェクトにアクセスします。自動 [hostname resolution](#hostname-resolution) を使用していない場合は、`homestead.test` または選択したドメインの `/etc/hosts` ファイル エントリを追加する必要があることに注意してください。

<a name="installing-optional-features"></a>
<!-- ### Installing Optional Features -->
### Installing Optional Features

<!-- Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options: -->
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
<!-- #### Elasticsearch -->
#### Elasticsearch

<!-- You may specify a supported version of Elasticsearch, which must be an exact version number (major.minor.patch). The default installation will create a cluster named 'homestead'. You should never give Elasticsearch more than half of the operating system's memory, so make sure your Homestead virtual machine has at least twice the Elasticsearch allocation. -->
Elasticsearch のサポートされているバージョンを指定できます。これは正確なバージョン番号 (major.minor.patch) である必要があります。デフォルトのインストールでは、「homestead」という名前のクラスターが作成されます。 Elasticsearch にはオペレーティング システムのメモリの半分を超えて割り当てないでください。そのため、Homestead 仮想マシンには少なくとも 2 倍の Elasticsearch 割り当てがあることを確認してください。

> [!NOTE]
> 構成をカスタマイズする方法については、[Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current) を確認してください。

<a name="mariadb"></a>
<!-- #### MariaDB -->
#### MariaDB

<!-- Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration. -->
MariaDB を有効にすると、MySQL が削除され、MariaDB がインストールされます。 MariaDB は通常、MySQL のドロップイン代替として機能するため、アプリケーションのデータベース構成では引き続き `mysql` データベース ドライバを使用する必要があります。

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`. -->
デフォルトの MongoDB インストールでは、データベースのユーザー名が `homestead` に設定され、対応するパスワードが `secret` に設定されます。

<a name="neo4j"></a>
<!-- #### Neo4j -->
#### Neo4j

<!-- The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client. -->
デフォルトの Neo4j インストールでは、データベースのユーザー名が `homestead` に設定され、対応するパスワードが `secret` に設定されます。 Neo4j ブラウザにアクセスするには、Web ブラウザから `http://homestead.test:7474` にアクセスします。ポート `7687` (Bolt)、`7474` (HTTP)、および `7473` (HTTPS) は、Neo4j クライアントからのリクエストを処理する準備ができています。

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory: -->
Homestead ディレクトリ内の `aliases` ファイルを変更することで、Homestead 仮想マシンに Bash エイリアスを追加できます。

```shell
alias c='clear'
alias ..='cd ..'
```

<!-- After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine. -->
`aliases` ファイルを更新した後、`vagrant reload --provision` コマンドを使用して Homestead 仮想マシンを再プロビジョニングする必要があります。これにより、新しいエイリアスがマシン上で確実に使用できるようになります。

<a name="updating-homestead"></a>
<!-- ## Updating Homestead -->
## Updating Homestead

<!-- Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory: -->
Homestead の更新を開始する前に、Homestead ディレクトリで次のコマンドを実行して、現在の仮想マシンが削除されていることを確認する必要があります。

```shell
vagrant destroy
```

<!-- Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository: -->
次に、Homestead ソース コードを更新する必要があります。リポジトリのクローンを作成した場合は、最初にリポジトリのクローンを作成した場所で次のコマンドを実行できます。

```shell
git fetch

git pull origin release
```

<!-- These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases). -->
これらのコマンドは、GitHub リポジトリから最新の Homestead コードをプルし、最新のタグを取得して、最新のタグ付きリリースをチェックアウトします。最新の安定リリース バージョンは、Homestead の [GitHub releases page](https://github.com/laravel/homestead/releases) で見つけることができます。

<!-- If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies: -->
プロジェクトの `composer.json` ファイルを介して Homestead をインストールした場合は、`composer.json` ファイルに `"laravel/homestead": "^12"` が含まれていることを確認し、依存関係を更新する必要があります。

```shell
composer update
```

<!-- Next, you should update the Vagrant box using the `vagrant box update` command: -->
次に、`vagrant box update` コマンドを使用して Vagrant ボックスを更新する必要があります。

```shell
vagrant box update
```

<!-- After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files: -->
Vagrant ボックスを更新した後、Homestead ディレクトリから `bash init.sh` コマンドを実行して、Homestead の追加構成ファイルを更新する必要があります。既存の `Homestead.yaml`、`after.sh`、および `aliases` ファイルを上書きするかどうかを尋ねられます。

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<!-- Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation: -->
最後に、最新の Vagrant インストールを利用するには、Homestead 仮想マシンを再生成する必要があります。

```shell
vagrant up
```

<a name="daily-usage"></a>
<!-- ## Daily Usage -->
## Daily Usage

<a name="connecting-via-ssh"></a>
<!-- ### Connecting via SSH -->
### Connecting via SSH

<!-- You can SSH into your virtual machine by executing the `vagrant ssh` terminal command from your Homestead directory. -->
Homestead ディレクトリから `vagrant ssh` ターミナル コマンドを実行することで、仮想マシンに SSH 接続できます。

<a name="adding-additional-sites"></a>
<!-- ### Adding Additional Sites -->
### Adding Additional Sites

<!-- Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file. -->
Homestead 環境がプロビジョニングされて実行されたら、他の Laravel プロジェクト用に Nginx サイトを追加することもできます。単一の Homestead 環境では、必要なだけ Laravel プロジェクトを実行できます。追加のサイトを追加するには、そのサイトを `Homestead.yaml` ファイルに追加します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> サイトを追加する前に、プロジェクトのディレクトリに [folder mapping](#configuring-shared-folders) が設定されていることを確認する必要があります。

<!-- If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`: -->
Vagrant が「hosts」ファイルを自動的に管理しない場合は、そのファイルに新しいサイトを追加する必要がある場合もあります。 macOS および Linux では、このファイルは `/etc/hosts` にあります。 Windows では、`C:\Windows\System32\drivers\etc\hosts` にあります。

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

<!-- Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory. -->
サイトが追加されたら、Homestead ディレクトリから `vagrant reload --provision` ターミナル コマンドを実行します。

<a name="site-types"></a>
<!-- #### Site Types -->
#### Site Types

<!-- Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type: -->
Homestead は、Laravel に基づいていないプロジェクトを簡単に実行できるようにするいくつかの「タイプ」のサイトをサポートしています。たとえば、`statamic` サイト タイプを使用して、Statamic アプリケーションを Homestead に簡単に追加できます。

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

<!-- The available site types are: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (the default), `proxy` (for nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`. -->
利用可能なサイト タイプは次のとおりです: `apache`、`apache-proxy`、`apigility`、`expressive`、`laravel` (デフォルト)、`proxy` (nginx の場合)、`silverstripe`、`statamic`、`symfony2`、 `symfony4`、および `zf`。

<a name="site-parameters"></a>
<!-- #### Site Parameters -->
#### Site Parameters

<!-- You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive: -->
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
<!-- ### Environment Variables -->
### Environment Variables

<!-- You can define global environment variables by adding them to your `Homestead.yaml` file: -->
グローバル環境変数を `Homestead.yaml` ファイルに追加することで定義できます。

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

<!-- After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user. -->
`Homestead.yaml` ファイルを更新した後、必ず `vagrant reload --provision` コマンドを実行してマシンを再プロビジョニングしてください。これにより、インストールされているすべての PHP バージョンの PHP-FPM 構成が更新され、`vagrant` ユーザーの環境も更新されます。

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- By default, the following ports are forwarded to your Homestead environment: -->
デフォルトでは、次のポートが Homestead 環境に転送されます。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
-->
- **HTTP:** 8000 → 80 に転送
- **HTTPS:** 44300 → 443 に転送

<!-- </div> -->
</div>

<a name="forwarding-additional-ports"></a>
<!-- #### Forwarding Additional Ports -->
#### Forwarding Additional Ports

<!-- If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command: -->
必要に応じて、`Homestead.yaml` ファイル内で `ports` 構成エントリを定義することで、追加のポートを Vagrant ボックスに転送できます。 `Homestead.yaml` ファイルを更新した後、必ず `vagrant reload --provision` コマンドを実行してマシンを再プロビジョニングしてください。

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

<!-- Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box: -->
以下は、ホスト マシンから Vagrant ボックスにマッピングする追加の Homestead サービス ポートのリストです。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **SSH:** 2222 &rarr; To 22
- **ngrok UI:** 4040 &rarr; To 4040
- **MySQL:** 33060 &rarr; To 3306
- **PostgreSQL:** 54320 &rarr; To 5432
- **MongoDB:** 27017 &rarr; To 27017
- **Mailpit:** 8025 &rarr; To 8025
- **Minio:** 9600 &rarr; To 9600
-->
- **SSH:** 2222 → 22 へ
- **ngrok UI:** 4040 → 4040 へ
- **MySQL:** 33060 → 3306 へ
- **PostgreSQL:** 54320 → 5432 へ
- **MongoDB:** 27017 → 27017 へ
- **Mailpit:** 8025 → 8025 へ
- **Minio:** 9600 → 9600へ

<!-- </div> -->
</div>

<a name="php-versions"></a>
<!-- ### PHP Versions -->
### PHP Versions

<!-- Homestead supports running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", and "8.3", (the default): -->
Homestead は、同じ仮想マシン上で複数のバージョンの PHP の実行をサポートします。 `Homestead.yaml` ファイル内の特定のサイトで使用する PHP のバージョンを指定できます。利用可能な PHP バージョンは、「5.6」、「7.0」、「7.1」、「7.2」、「7.3」、「7.4」、「8.0」、「8.1」、「8.2」、および「8.3」 (デフォルト) です。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

<!-- [Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI: -->
[Within your Homestead virtual machine](#connecting-via-ssh)、CLI 経由でサポートされている PHP バージョンのいずれかを使用できます。

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

<!-- You may change the default version of PHP used by the CLI by issuing the following commands from within your Homestead virtual machine: -->
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
<!-- ### Connecting to Databases -->
### Connecting to Databases

<!-- A `homestead` database is configured for both MySQL and PostgreSQL out of the box. To connect to your MySQL or PostgreSQL database from your host machine's database client, you should connect to `127.0.0.1` on port `33060` (MySQL) or `54320` (PostgreSQL). The username and password for both databases is `homestead` / `secret`. -->
`homestead` データベースは、すぐに MySQL と PostgreSQL の両方用に構成されています。ホスト マシンのデータベース クライアントから MySQL または PostgreSQL データベースに接続するには、ポート `33060` (MySQL) または `54320` (PostgreSQL) の `127.0.0.1` に接続する必要があります。両方のデータベースのユーザー名とパスワードは、`homestead` / `secret` です。

> [!WARNING]
> これらの非標準ポートは、ホスト マシンからデータベースに接続する場合にのみ使用してください。 Laravel は仮想マシン内で実行されているため、Laravel アプリケーションの `database` 構成ファイルではデフォルトの 3306 ポートと 5432 ポートを使用します。

<a name="database-backups"></a>
<!-- ### Database Backups -->
### Database Backups

<!-- Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file: -->
Homestead 仮想マシンが破壊された場合、Homestead はデータベースを自動的にバックアップできます。この機能を利用するには、Vagrant 2.1.0 以降を使用する必要があります。または、古いバージョンの Vagrant を使用している場合は、`vagrant-triggers` プラグインをインストールする必要があります。データベースの自動バックアップを有効にするには、`Homestead.yaml` ファイルに次の行を追加します。

```yaml
backup: true
```

<!-- Once configured, Homestead will export your databases to `.backup/mysql_backup` and `.backup/postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method. -->
構成が完了すると、`vagrant destroy` コマンドの実行時に、Homestead はデータベースを `.backup/mysql_backup` および `.backup/postgres_backup` ディレクトリにエクスポートします。これらのディレクトリは、Homestead をインストールしたフォルダー、または [per project installation](#per-project-installation) 方法を使用している場合はプロジェクトのルートにあります。

<a name="configuring-cron-schedules"></a>
<!-- ### Configuring Cron Schedules -->
### Configuring Cron Schedules

<!-- Laravel provides a convenient way to [schedule cron jobs](/docs/master/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `routes/console.php` file to determine which scheduled tasks to run. -->
Laravel は、単一の `schedule:run` Artisan コマンドを毎分実行するようにスケジュールすることで、[schedule cron jobs](/docs/master/scheduling) を実行する便利な方法を提供します。 `schedule:run` コマンドは、`routes/console.php` ファイルに定義されているジョブ スケジュールを調べて、実行するスケジュールされたタスクを決定します。

<!-- If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site: -->
Homestead サイトに対して `schedule:run` コマンドを実行したい場合は、サイトを定義するときに `schedule` オプションを `true` に設定します。

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

<!-- The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine. -->
サイトの cron ジョブは、Homestead 仮想マシンの `/etc/cron.d` ディレクトリで定義されます。

<a name="configuring-mailpit"></a>
<!-- ### Configuring Mailpit -->
### Configuring Mailpit

<!-- [Mailpit](https://github.com/axllent/mailpit) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings: -->
[Mailpit](https://github.com/axllent/mailpit) を使用すると、実際に受信者にメールを送信せずに、送信電子メールを傍受して検査できます。まず、次のメール設定を使用するようにアプリケーションの `.env` ファイルを更新します。

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

<!-- Once Mailpit has been configured, you may access the Mailpit dashboard at `http://localhost:8025`. -->
Mailpit が構成されたら、`http://localhost:8025` で Mailpit ダッシュボードにアクセスできます。

<a name="configuring-minio"></a>
<!-- ### Configuring Minio -->
### Configuring Minio

<!-- [Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section: -->
[Minio](https://github.com/minio/minio) は、Amazon S3 互換 API を備えたオープンソースのオブジェクト ストレージ サーバーです。 Minio をインストールするには、[features](#installing-optional-features) セクションの次の構成オプションを使用して `Homestead.yaml` ファイルを更新します。

```
minio: true
```

<!-- By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`. -->
デフォルトでは、Minio はポート 9600 で使用できます。`http://localhost:9600` にアクセスすると、Minio コントロール パネルにアクセスできます。デフォルトのアクセスキーは `homestead` で、デフォルトの秘密キーは `secretkey` です。 Minio にアクセスするときは、常にリージョン `us-east-1` を使用する必要があります。

<!-- In order to use Minio, ensure your `.env` file has the following options: -->
Minio を使用するには、`.env` ファイルに次のオプションがあることを確認してください。

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

<!-- To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal: -->
Minio を利用した「S3」バケットをプロビジョニングするには、`buckets` ディレクティブを `Homestead.yaml` ファイルに追加します。バケットを定義した後、ターミナルで `vagrant reload --provision` コマンドを実行する必要があります。

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

<!-- Supported `policy` values include: `none`, `download`, `upload`, and `public`. -->
サポートされている `policy` 値には、`none`、`download`、`upload`、および `public` が含まれます。

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- In order to run [Laravel Dusk](/docs/master/dusk) tests within Homestead, you should enable the [webdriver feature](#installing-optional-features) in your Homestead configuration: -->
Homestead 内で [Laravel Dusk](/docs/master/dusk) テストを実行するには、Homestead 構成で [webdriver feature](#installing-optional-features) を有効にする必要があります。

```yaml
features:
    - webdriver: true
```

<!-- After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal. -->
`webdriver` 機能を有効にした後、端末で `vagrant reload --provision` コマンドを実行する必要があります。

<a name="sharing-your-environment"></a>
<!-- ### Sharing Your Environment -->
### Sharing Your Environment

<!-- Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file. -->
現在取り組んでいることを同僚やクライアントと共有したい場合があります。 Vagrant には、`vagrant share` コマンドを介したこれに対するサポートが組み込まれています。ただし、`Homestead.yaml` ファイルで複数のサイトが構成されている場合、これは機能しません。

<!-- To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`: -->
この問題を解決するために、Homestead には独自の `share` コマンドが含まれています。開始するには、`vagrant ssh` 経由で [SSH into your Homestead virtual machine](#connecting-via-ssh) を実行し、`share homestead.test` コマンドを実行します。このコマンドは、`Homestead.yaml` 構成ファイルから `homestead.test` サイトを共有します。 `homestead.test` の代わりに、他の構成済みサイトを使用できます。

```shell
share homestead.test
```

<!-- After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command: -->
コマンドを実行すると、アクティビティ ログと共有サイトの一般にアクセス可能な URL を含む Ngrok 画面が表示されます。カスタム リージョン、サブドメイン、またはその他の Ngrok ランタイム オプションを指定したい場合は、それらを `share` コマンドに追加できます。

```shell
share homestead.test -region=eu -subdomain=laravel
```

<!-- If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so. -->
HTTP ではなく HTTPS でコンテンツを共有する必要がある場合は、`share` の代わりに `sshare` コマンドを使用すると、これが可能になります。

> [!WARNING]
> Vagrant は本質的に安全ではないため、`share` コマンドを実行すると仮想マシンがインターネットに公開されることになることに注意してください。

<a name="debugging-and-profiling"></a>
<!-- ## Debugging and Profiling -->
## Debugging and Profiling

<a name="debugging-web-requests"></a>
<!-- ### Debugging Web Requests With Xdebug -->
### Debugging Web Requests With Xdebug

<!-- Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code. -->
Homestead には、[Xdebug](https://xdebug.org) を使用したステップ デバッグのサポートが含まれています。たとえば、ブラウザでページにアクセスすると、PHP が IDE に接続して、実行中のコードを検査および変更できるようになります。

<!-- By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/). -->
デフォルトでは、Xdebug はすでに実行されており、接続を受け入れる準備ができています。 CLI で Xdebug を有効にする必要がある場合は、Homestead 仮想マシン内で `sudo phpenmod xdebug` コマンドを実行します。次に、IDE の指示に従ってデバッグを有効にします。最後に、拡張機能または [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/) を使用して Xdebug をトリガーするようにブラウザを設定します。

> [!WARNING]
> Xdebug により、PHP の実行が大幅に遅くなります。 Xdebug を無効にするには、Homestead 仮想マシン内で `sudo phpdismod xdebug` を実行し、FPM サービスを再起動します。

<a name="autostarting-xdebug"></a>
<!-- #### Autostarting Xdebug -->
#### Autostarting Xdebug

<!-- When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration: -->
Web サーバーにリクエストを行う機能テストをデバッグする場合、カスタム ヘッダーまたは Cookie を通過するようにテストを変更してデバッグをトリガーするよりも、デバッグを自動開始する方が簡単です。 Xdebug を強制的に自動的に開始するには、Homestead 仮想マシン内の `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` ファイルを変更し、次の構成を追加します。

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
<!-- ### Debugging CLI Applications -->
### Debugging CLI Applications

<!-- To debug a PHP CLI application, use the `xphp` shell alias inside your Homestead virtual machine: -->
PHP CLI アプリケーションをデバッグするには、Homestead 仮想マシン内で `xphp` シェル エイリアスを使用します。

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
<!-- ### Profiling Applications With Blackfire -->
### Profiling Applications With Blackfire

<!-- [Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings. -->
[Blackfire](https://blackfire.io/docs/introduction) は、Web リクエストと CLI アプリケーションをプロファイリングするためのサービスです。コールグラフとタイムラインにプロファイル データを表示する対話型ユーザー インターフェイスを提供します。これは、開発、ステージング、実稼働で使用するために構築されており、エンドユーザーにオーバーヘッドはかかりません。さらに、Blackfire は、コードおよび `php.ini` 構成設定のパフォーマンス、品質、セキュリティ チェックを提供します。

<!-- The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios. -->
[Blackfire Player](https://blackfire.io/docs/player/index) は、プロファイリング シナリオをスクリプト化するために Blackfire と連携できるオープンソースの Web クローリング、Web テスト、および Web スクレイピング アプリケーションです。

<!-- To enable Blackfire, use the "features" setting in your Homestead configuration file: -->
Blackfire を有効にするには、Homestead 構成ファイルの「features」設定を使用します。

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

<!-- Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index). -->
Blackfire サーバー認証情報とクライアント認証情報 [require a Blackfire account](https://blackfire.io/signup)。 Blackfire は、CLI ツールやブラウザ拡張機能など、アプリケーションをプロファイリングするためのさまざまなオプションを提供します。 [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index) してください。

<a name="network-interfaces"></a>
<!-- ## Network Interfaces -->
## Network Interfaces

<!-- The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary: -->
`Homestead.yaml` ファイルの `networks` プロパティは、Homestead 仮想マシンのネットワーク インターフェイスを構成します。必要な数のインターフェイスを構成できます。

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

<!-- To enable a [bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) interface, configure a `bridge` setting for the network and change the network type to `public_network`: -->
[bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) インターフェイスを有効にするには、ネットワークの `bridge` 設定を構成し、ネットワーク タイプを `public_network` に変更します。

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To enable [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), just remove the `ip` option from your configuration: -->
[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp) を有効にするには、構成から `ip` オプションを削除するだけです。

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To update what device the network is using, you may add a `dev` option to the network's configuration. The default `dev` value is `eth0`: -->
ネットワークが使用しているデバイスを更新するには、ネットワークの構成に `dev` オプションを追加します。デフォルトの `dev` 値は `eth0` です。

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
<!-- ## Extending Homestead -->
## Extending Homestead

<!-- You may extend Homestead using the `after.sh` script in the root of your Homestead directory. Within this file, you may add any shell commands that are necessary to properly configure and customize your virtual machine. -->
Homestead ディレクトリのルートにある `after.sh` スクリプトを使用して Homestead を拡張できます。このファイル内に、仮想マシンを適切に構成およびカスタマイズするために必要なシェル コマンドを追加できます。

<!-- When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead: -->
Homestead をカスタマイズするとき、Ubuntu はパッケージの元の構成を保持するか、新しい構成ファイルで上書きするかを尋ねる場合があります。これを回避するには、パッケージをインストールするときに次のコマンドを使用して、Homestead によって以前に書き込まれた構成が上書きされないようにする必要があります。

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
<!-- ### User Customizations -->
### User Customizations

<!-- When using Homestead with your team, you may want to tweak Homestead to better fit your personal development style. To accomplish this, you may create a `user-customizations.sh` file in the root of your Homestead directory (the same directory containing your `Homestead.yaml` file). Within this file, you may make any customization you would like; however, the `user-customizations.sh` should not be version controlled. -->
チームで Homestead を使用する場合、個人の開発スタイルに合わせて Homestead を微調整することができます。これを実現するには、Homestead ディレクトリのルート (`Homestead.yaml` ファイルが含まれているのと同じディレクトリ) に `user-customizations.sh` ファイルを作成します。このファイル内で、必要なカスタマイズを行うことができます。ただし、`user-customizations.sh` はバージョン管理しないでください。

<a name="provider-specific-settings"></a>
<!-- ## Provider Specific Settings -->
## Provider Specific Settings

<a name="provider-specific-virtualbox"></a>
<!-- ### VirtualBox -->
### VirtualBox

<a name="natdnshostresolver"></a>
<!-- #### `natdnshostresolver` -->
#### `natdnshostresolver`

<!-- By default, Homestead configures the `natdnshostresolver` setting to `on`. This allows Homestead to use your host operating system's DNS settings. If you would like to override this behavior, add the following configuration options to your `Homestead.yaml` file: -->
デフォルトでは、Homestead は `natdnshostresolver` 設定を `on` に構成します。これにより、Homestead はホスト オペレーティング システムの DNS 設定を使用できるようになります。この動作をオーバーライドする場合は、次の構成オプションを `Homestead.yaml` ファイルに追加します。

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

