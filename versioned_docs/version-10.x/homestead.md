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

<!-- Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, or any other server software on your local machine. -->
Laravel은 여러분의 전체 PHP 개발 경험이 즐거울 수 있도록, 로컬 개발 환경을 포함한 모든 부분을 개선하고자 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는, 사전 패키징된 Vagrant 박스로서, 여러분의 로컬 컴퓨터에 PHP, 웹 서버, 그 외 기타 서버 소프트웨어를 직접 설치하지 않고도 훌륭한 개발 환경을 즉시 제공해줍니다.

<!-- [Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes! -->
[Vagrant](https://www.vagrantup.com)는 가상 머신(Virtual Machine)을 손쉽게 관리하고 프로비저닝할 수 있는 우아한 방법을 제공합니다. Vagrant 박스는 언제든 손쉽게 폐기할 수 있습니다. 무언가 잘못되어도 몇 분이면 박스를 삭제하고 다시 만들 수 있습니다!

<!-- Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications. -->
Homestead는 Windows, macOS, Linux 시스템 모두에서 사용할 수 있으며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 애플리케이션 개발에 필요한 모든 주요 소프트웨어를 포함하고 있습니다.

> [!WARNING]
> Windows 사용자는 하드웨어 가상화(VT-x)를 활성화해야 할 수도 있습니다. VT-x는 보통 BIOS에서 활성화할 수 있습니다. 만약 UEFI 시스템에서 Hyper-V를 사용 중이라면, VT-x에 접근하려면 Hyper-V를 비활성화해야 할 수도 있습니다.

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
- Node (Yarn, Bower, Grunt, Gulp 포함)
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
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk Utilities

<!-- </div> -->
</div>

<a name="installation-and-setup"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- Before launching your Homestead environment, you must install [Vagrant](https://developer.hashicorp.com/vagrant/downloads) as well as one of the following supported providers: -->
Homestead 환경을 실행하기 전에, [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 아래의 지원되는 프로바이더 중 하나를 설치해야 합니다.

<!--
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)
-->
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

<!-- All of these software packages provide easy-to-use visual installers for all popular operating systems. -->
위 소프트웨어들은 모두 주요 운영체제에서 쉽게 설치할 수 있는 시각적 설치 프로그램을 제공합니다.

<!-- To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge. -->
Parallels 프로바이더를 사용하려면, 추가적으로 [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
<!-- #### Installing Homestead -->
#### Installing Homestead

<!-- You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory": -->
Homestead는 공식 저장소를 호스트 머신에 클론하여 설치할 수 있습니다. Homestead 가상 머신은 당신이 개발하는 모든 Laravel 애플리케이션의 호스트 역할을 하게 되므로, "홈" 디렉터리 아래에 `Homestead` 폴더를 만들어 해당 위치에 저장소를 클론하는 것이 좋습니다. 이 문서에서 이 폴더를 "Homestead 디렉터리"라고 부르겠습니다.

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

<!-- After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead: -->
저장소를 클론한 후에는 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치에는 Homestead의 최신 안정 버전이 항상 포함되어 있습니다.

```shell
cd ~/Homestead

git checkout release
```

<!-- Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory: -->
그 다음, Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성하세요. `Homestead.yaml` 파일에서 Homestead 설치에 대한 모든 설정을 구성할 수 있습니다. 이 파일은 Homestead 디렉터리 내부에 생성됩니다.

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
`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 프로바이더(`virtualbox` 또는 `parallels`)를 지정합니다.


```
provider: virtualbox
```


> [!WARNING]
> Apple Silicon 사용자라면 Parallels 프로바이더를 반드시 사용해야 합니다.

<a name="configuring-shared-folders"></a>
<!-- #### Configuring Shared Folders -->
#### Configuring Shared Folders

<!-- The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary: -->
`Homestead.yaml` 파일의 `folders` 속성에는 Homestead 환경과 공유하고 싶은 폴더 목록을 정의합니다. 이 폴더 내부의 파일이 변경될 때마다, 로컬 컴퓨터와 Homestead 가상 환경 사이에 자동으로 동기화됩니다. 필요한 만큼 여러 개의 공유 폴더를 설정할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 문법 대신 전체 경로(예: `C:\Users\user\Code\project1`)를 사용해야 합니다.

<!-- You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder: -->
반드시 각각의 애플리케이션을 개별 폴더로 매핑하세요. 모든 애플리케이션이 들어 있는 하나의 대형 폴더 전체를 매핑하면, 가상 머신이 해당 폴더 내 모든 파일의 디스크 IO를 추적하게 되어 매우 많은 파일이 있을 경우 성능 저하가 발생할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 `.`(현재 디렉터리)를 마운트해서는 안 됩니다. 이 경우 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않게 되며, 추가 기능이 제대로 동작하지 않거나 예기치 못한 문제가 발생할 수 있습니다.

<!-- To enable [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), you may add a `type` option to your folder mapping: -->
[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 활성화하려면, 폴더 매핑 설정에 `type` 옵션을 추가하면 됩니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것이 좋습니다. 이 플러그인은 Homestead 가상 머신 내부의 파일과 디렉터리에 대한 올바른 사용자/그룹 권한을 유지해줍니다.

<!-- You may also pass any options supported by Vagrant's [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) by listing them under the `options` key: -->
Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)가 지원하는 옵션은 `options` 키 아래에 추가로 지정할 수 있습니다.

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
Nginx에 익숙하지 않아도 문제 없습니다. `Homestead.yaml`의 `sites` 속성으로 도메인과 Homestead 환경 내 폴더를 손쉽게 매핑할 수 있습니다. 기본 예시가 `Homestead.yaml`에 포함되어 있으며, 필요에 따라 여러 개의 사이트를 추가할 수 있습니다. Homestead는 개발 중인 모든 Laravel 애플리케이션에 대해 편리한 가상 환경을 제공합니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

<!-- If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine. -->
`sites` 속성을 수정한 후에는 Homestead 가상 머신 내의 Nginx 설정을 업데이트하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!WARNING]
> Homestead 스크립트는 가능한 한 idempotent(중복 실행해도 동일한 결과)하도록 설계되어 있지만, 프로비저닝 과정에서 문제가 발생한다면 `vagrant destroy && vagrant up` 명령으로 가상 머신을 삭제 후 재생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
<!-- #### Hostname Resolution -->
#### Hostname Resolution

<!-- Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US). -->
Homestead는 `mDNS`를 이용해 자동으로 호스트네임을 게시합니다. 만약 `Homestead.yaml`에 `hostname: homestead`를 지정하면, `homestead.local`에서 접근할 수 있습니다. macOS, iOS, 대부분의 Linux 데스크톱 배포판에는 기본적으로 `mDNS`가 지원됩니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

<!-- Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following: -->
자동 호스트네임 기능은 [per project installations](#per-project-installation)에 가장 적합합니다. 여러 사이트를 하나의 Homestead 인스턴스 내에 호스팅할 경우, 각 사이트의 도메인 이름을 운영 체제의 `hosts` 파일에 직접 추가해야 합니다. 이 `hosts` 파일은 Homestead 사이트로 향하는 요청을 Homestead 가상 머신으로 리다이렉트합니다. 이 파일은 macOS 및 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 경로에 있습니다. 다음과 같이 추가하면 됩니다.

```
192.168.56.56  homestead.test
```

<!-- Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser: -->
`Homestead.yaml` 파일에 지정한 IP 주소가 위와 일치하는지 반드시 확인해야 합니다. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면 웹 브라우저에서 다음과 같이 접근합니다.

```shell
http://homestead.test
```

<a name="configuring-services"></a>
<!-- ### Configuring Services -->
### Configuring Services

<!-- Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file: -->
Homestead는 여러 가지 서비스를 기본으로 실행하지만, 프로비저닝 시 활성화 또는 비활성화할 서비스를 직접 선택할 수도 있습니다. 예를 들어, PostgreSQL만 활성화하고 MySQL은 비활성화하려면 `Homestead.yaml` 파일의 `services` 옵션을 아래와 같이 수정하면 됩니다.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

<!-- The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives. -->
여기에 명시한 서비스들은 `enabled`와 `disabled`에 따라 순서대로 시작 또는 중지 처리됩니다.

<a name="launching-the-vagrant-box"></a>
<!-- ### Launching the Vagrant Box -->
### Launching the Vagrant Box

<!-- Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites. -->
`Homestead.yaml`을 원하는 대로 수정한 다음, Homestead 디렉터리에서 `vagrant up` 명령을 실행하세요. 그러면 가상 머신이 부팅되고, 공유 폴더와 Nginx 사이트가 자동으로 구성됩니다.

<!-- To destroy the machine, you may use the `vagrant destroy` command. -->
가상 머신을 삭제하려면 `vagrant destroy` 명령을 사용하면 됩니다.

<a name="per-project-installation"></a>
<!-- ### Per Project Installation -->
### Per Project Installation

<!-- Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository. -->
Homestead를 전역(Global)으로 설치하여 모든 프로젝트가 동일한 Homestead 가상 머신을 공유할 수도 있지만, 프로젝트마다 별도의 Homestead 인스턴스를 설정하는 것도 가능합니다. 프로젝트별로 Homestead를 설치하면, 저장소에 `Vagrantfile`을 포함시켜 다른 개발자 역시 해당 프로젝트를 클론한 후 바로 `vagrant up`으로 개발 환경을 실행할 수 있습니다.

<!-- You may install Homestead into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용해 프로젝트 내에 Homestead를 설치할 수 있습니다.

```shell
composer require laravel/homestead --dev
```

<!-- Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file: -->
설치 후, Homestead의 `make` 명령을 실행하면 프로젝트를 위한 `Vagrantfile`과 `Homestead.yaml` 파일이 프로젝트 루트에 생성됩니다. 이 때 `make` 명령이 `Homestead.yaml`의 `sites`, `folders` 지시자를 자동으로 설정합니다.

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

<!-- Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution). -->
이제 터미널에서 `vagrant up`을 실행하고 웹 브라우저에서 `http://homestead.test`로 프로젝트에 접근하면 됩니다. 자동 [hostname resolution](#hostname-resolution) 기능을 사용하지 않는다면, `homestead.test` 또는 원하는 도메인을 `/etc/hosts` 파일에 직접 추가해주어야 합니다.

<a name="installing-optional-features"></a>
<!-- ### Installing Optional Features -->
### Installing Optional Features

<!-- Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options: -->
선택적 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 사용해 설치할 수 있습니다. 대부분의 기능은 불린 값으로 활성화/비활성화하며, 일부 기능은 다양한 구성 옵션을 제공합니다.

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
지원되는 버전의 Elasticsearch를 명확히 지정할 수 있으며, 반드시 정확한 버전 번호(major.minor.patch)여야 합니다. 기본적으로 'homestead'라는 이름의 클러스터가 생성됩니다. Elasticsearch에 운영체제 메모리의 절반 이상을 할당하면 안 되므로, Homestead 가상 머신의 메모리를 Elasticsearch 할당량의 두 배 이상으로 설정해야 합니다.

> [!NOTE]
> [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하여 설정을 자유롭게 커스터마이징할 수 있습니다.

<a name="mariadb"></a>
<!-- #### MariaDB -->
#### MariaDB

<!-- Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration. -->
MariaDB를 활성화하면 MySQL이 제거되고 대신 MariaDB가 설치됩니다. MariaDB는 MySQL과 호환(대체)되므로, 애플리케이션의 데이터베이스 설정에서는 여전히 `mysql` 드라이버를 사용하면 됩니다.

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`. -->
기본 MongoDB 설치 시 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 지정됩니다.

<a name="neo4j"></a>
<!-- #### Neo4j -->
#### Neo4j

<!-- The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client. -->
기본 Neo4j 설치 시 역시 사용자명은 `homestead`, 비밀번호는 `secret`으로 지정됩니다. Neo4j 브라우저는 `http://homestead.test:7474`에서 접근할 수 있습니다. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS) 모두 Neo4j 클라이언트의 요청을 서비스할 준비가 되어 있습니다.

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory: -->
Homestead 가상 머신에 Bash 별칭을 추가하려면, Homestead 디렉터리의 `aliases` 파일을 수정하면 됩니다.

```shell
alias c='clear'
alias ..='cd ..'
```

<!-- After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine. -->
`aliases` 파일을 수정한 후에는 `vagrant reload --provision` 명령으로 Homestead 가상 머신을 재프로비저닝해야 새 별칭이 적용됩니다.

<a name="updating-homestead"></a>
<!-- ## Updating Homestead -->
## Updating Homestead

<!-- Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory: -->
Homestead를 업데이트하기 전에, 현재 사용 중인 가상 머신을 아래 명령어로 먼저 삭제하세요.

```shell
vagrant destroy
```

<!-- Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository: -->
이제 Homestead 소스 코드를 갱신해야 합니다. 저장소를 클론한 경우, 원래 해당 디렉터리에서 다음 명령어를 실행하세요.

```shell
git fetch

git pull origin release
```

<!-- These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases). -->
위 명령들은 최신 Homestead 코드를 GitHub 저장소에서 가져와 최신 태그를 반영합니다. 최신 안정화 버전은 Homestead의 [GitHub releases page](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

<!-- If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies: -->
프로젝트의 `composer.json` 파일을 통해 Homestead를 설치한 경우, `composer.json` 파일에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 의존성을 업데이트해야 합니다.

```shell
composer update
```

<!-- Next, you should update the Vagrant box using the `vagrant box update` command: -->
이후, `vagrant box update` 명령을 실행하여 Vagrant 박스를 갱신합니다.

```shell
vagrant box update
```

<!-- After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files: -->
Vagrant 박스를 업데이트한 뒤에는, Homestead 디렉터리에서 `bash init.sh` 명령을 실행하여 Homestead의 추가 설정 파일을 갱신해야 합니다. 이 과정에서 기존의 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 물어볼 수 있습니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<!-- Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation: -->
마지막으로 최신 Vagrant 환경을 적용하려면 Homestead 가상 머신을 다시 생성해야 합니다.

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
Homestead 디렉터리에서 `vagrant ssh` 명령을 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
<!-- ### Adding Additional Sites -->
### Adding Additional Sites

<!-- Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file. -->
Homestead 환경을 프로비저닝해 실행한 뒤, 추가로 다른 Laravel 프로젝트의 Nginx 사이트를 더 등록하고 싶을 수 있습니다. Homestead 한 대에서 여러 개의 Laravel 프로젝트를 동시에 운영할 수 있습니다. 새로운 사이트를 추가하려면, `Homestead.yaml` 파일에 해당 사이트 정보를 추가하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 해당 프로젝트 폴더가 [folder mapping](#configuring-shared-folders)되어 있는지 꼭 확인하세요.

<!-- If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`: -->
Vagrant가 자동으로 "hosts" 파일을 관리하지 않는 경우, 새 사이트를 직접 등록해야 합니다. macOS, Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 경로를 사용합니다.

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

<!-- Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory. -->
사이트를 추가한 후에는 Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="site-types"></a>
<!-- #### Site Types -->
#### Site Types

<!-- Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type: -->
Homestead는 Laravel 기반이 아닌 프로젝트도 손쉽게 운영할 수 있도록 여러 가지 "사이트 유형"을 지원합니다. 예를 들어, Statamic 애플리케이션을 Homestead에 추가할 땐 아래와 같이 `statamic` 타입을 지정할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

<!-- The available site types are: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (the default), `proxy` (for nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`. -->
지원하는 사이트 유형은 다음과 같습니다: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
<!-- #### Site Parameters -->
#### Site Parameters

<!-- You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive: -->
사이트에 추가적인 Nginx `fastcgi_param` 값을 지정하려면 `params` 지시자를 사용할 수 있습니다.

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
`Homestead.yaml` 파일에 글로벌 환경 변수를 정의할 수 있습니다.

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

<!-- After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user. -->
`Homestead.yaml` 파일을 수정한 후에는 `vagrant reload --provision` 명령을 실행해 머신을 재프로비저닝해야 합니다. 이 과정에서 설치된 모든 PHP 버전에 대해 PHP-FPM 설정이 갱신되며, `vagrant` 사용자 환경도 함께 업데이트됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- By default, the following ports are forwarded to your Homestead environment: -->
기본적으로 아래 포트들이 Homestead 환경에 포워딩됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
-->
- **HTTP:** 8000 &rarr; 80번 포트로 연결됨
- **HTTPS:** 44300 &rarr; 443번 포트로 연결됨

<!-- </div> -->
</div>

<a name="forwarding-additional-ports"></a>
<!-- #### Forwarding Additional Ports -->
#### Forwarding Additional Ports

<!-- If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command: -->
원한다면 `Homestead.yaml` 파일에 `ports` 설정 항목을 정의해 추가적인 포트를 Vagrant 박스에 포워딩할 수 있습니다. `Homestead.yaml` 파일을 수정한 후에는 반드시 `vagrant reload --provision` 명령으로 머신을 재프로비저닝해야 적용됩니다.

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

<!-- Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box: -->
추가로 포워딩할 수 있는 주요 Homestead 서비스 포트는 다음과 같습니다.

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
- **SSH:** 2222 &rarr; 22번 포트로
- **ngrok UI:** 4040 &rarr; 4040번 포트로
- **MySQL:** 33060 &rarr; 3306번 포트로
- **PostgreSQL:** 54320 &rarr; 5432번 포트로
- **MongoDB:** 27017 &rarr; 27017번 포트로
- **Mailpit:** 8025 &rarr; 8025번 포트로
- **Minio:** 9600 &rarr; 9600번 포트로

<!-- </div> -->
</div>

<a name="php-versions"></a>
<!-- ### PHP Versions -->
### PHP Versions

<!-- Homestead supports running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", and "8.3", (the default): -->
Homestead는 하나의 가상 머신 안에서 여러 버전의 PHP를 지원합니다. 특정 사이트에 사용할 PHP 버전을 `Homestead.yaml` 파일에서 지정할 수 있습니다. 사용 가능한 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값)입니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

<!-- [Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI: -->
[Within your Homestead virtual machine](#connecting-via-ssh)에서는 다음과 같이 CLI를 통해 지원되는 PHP 버전을 사용할 수 있습니다.

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
CLI에서 기본 PHP 버전을 변경하려면 Homestead 가상 머신에서 아래 명령어를 사용할 수 있습니다.

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
MySQL과 PostgreSQL 모두에 대해 `homestead`라는 데이터베이스가 기본으로 설정되어 있습니다. 호스트 머신에서 데이터베이스 클라이언트로 접속하려면 `127.0.0.1`의 `33060`번(MySQL) 또는 `54320`번(PostgreSQL) 포트로 접속하면 됩니다. 사용자명, 비밀번호 모두 `homestead` / `secret` 입니다.

> [!WARNING]
> 호스트 머신에서 데이터베이스에 접속할 때만 이 비표준 포트를 사용해야 합니다. Laravel은 가상 머신 _내부에서_ 동작하므로, Laravel 애플리케이션의 `database` 설정 파일에서는 기본 포트인 3306, 5432를 사용하세요.

<a name="database-backups"></a>
<!-- ### Database Backups -->
### Database Backups

<!-- Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file: -->
Homestead는 가상 머신을 삭제할 때 자동으로 데이터베이스 백업을 생성할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요합니다. 더 낮은 버전에서는 `vagrant-triggers` 플러그인을 별도로 설치해야 합니다. 자동 백업 기능을 활성화하려면 `Homestead.yaml` 파일에 다음 한 줄을 추가하세요.


```
backup: true
```


<!-- Once configured, Homestead will export your databases to `.backup/mysql_backup` and `.backup/postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method. -->
구성 후, `vagrant destroy` 명령 실행 시 Homestead가 데이터베이스를 `.backup/mysql_backup` 및 `.backup/postgres_backup` 폴더에 내보냅니다. 이 폴더들은 Homestead를 설치한 위치나, [per project installation](#per-project-installation)를 선택한 경우엔 프로젝트 루트에 생성됩니다.

<a name="configuring-cron-schedules"></a>
<!-- ### Configuring Cron Schedules -->
### Configuring Cron Schedules

<!-- Laravel provides a convenient way to [schedule cron jobs](/docs/10.x/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `App\Console\Kernel` class to determine which scheduled tasks to run. -->
Laravel은 [schedule cron jobs](/docs/10.x/scheduling)을 편리하게 제공하며, 매 분마다 `schedule:run` Artisan 명령을 실행해 예약된 작업이 동작하도록 해줍니다. `schedule:run` 명령은 `App\Console\Kernel` 클래스에 정의된 스케줄 설정을 토대로 실행할 작업을 결정합니다.

<!-- If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site: -->
특정 Homestead 사이트에 대해 `schedule:run` 명령을 실행하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 지정하면 됩니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

<!-- The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine. -->
해당 사이트에 대한 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 등록됩니다.

<a name="configuring-mailpit"></a>
<!-- ### Configuring Mailpit -->
### Configuring Mailpit

<!-- [Mailpit](https://github.com/axllent/mailpit) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings: -->
[Mailpit](https://github.com/axllent/mailpit)은 외부로 실제 메일을 발송하지 않고, 개발 중인 애플리케이션의 메일을 가로채서 내용을 확인할 수 있게 해줍니다. 시작하려면 애플리케이션의 `.env` 파일을 아래와 같이 설정합니다.

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

<!-- Once Mailpit has been configured, you may access the Mailpit dashboard at `http://localhost:8025`. -->
설정이 완료되면, 웹 브라우저에서 `http://localhost:8025`로 Mailpit 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
<!-- ### Configuring Minio -->
### Configuring Minio

<!-- [Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section: -->
[Minio](https://github.com/minio/minio)는 Amazon S3와 호환 가능한 오픈소스 객체 저장소 서버입니다. Minio를 설치하려면, [features](#installing-optional-features) 섹션에 따라 `Homestead.yaml`의 해당 위치에 아래와 같이 옵션을 추가하세요.


```
minio: true
```


<!-- By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`. -->
기본적으로 Minio는 9600번 포트에서 사용 가능합니다. `http://localhost:9600`에서 Minio 관리 패널에 접근할 수 있습니다. 기본 접근 키는 `homestead`, 기본 secret 키는 `secretkey`입니다. region은 항상 `us-east-1`을 사용하면 됩니다.

<!-- In order to use Minio, you will need to adjust the S3 disk configuration in your application's `config/filesystems.php` configuration file. You will need to add the `use_path_style_endpoint` option to the disk configuration as well as change the `url` key to `endpoint`: -->
Minio를 사용하려면 애플리케이션의 `config/filesystems.php` 설정 파일에서 S3 디스크 구성을 다음과 같이 수정해야 합니다. `use_path_style_endpoint` 옵션을 추가하고, `url` 키를 `endpoint`로 변경하세요.

```
's3' => [
    'driver' => 's3',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION'),
    'bucket' => env('AWS_BUCKET'),
    'endpoint' => env('AWS_URL'),
    'use_path_style_endpoint' => true,
]
```

<!-- Finally, ensure your `.env` file has the following options: -->
그리고 `.env` 파일에 아래 옵션들을 반드시 포함해야 합니다.

```ini
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

<!-- To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal: -->
Minio 기반 "S3" 버킷을 프로비저닝하려면, `Homestead.yaml` 파일에 `buckets` 지시자를 추가하세요. 버킷 정의 후 터미널에서 `vagrant reload --provision` 명령을 실행해 적용할 수 있습니다.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

<!-- Supported `policy` values include: `none`, `download`, `upload`, and `public`. -->
지원되는 `policy` 값은 `none`, `download`, `upload`, `public`이 있습니다.

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- In order to run [Laravel Dusk](/docs/10.x/dusk) tests within Homestead, you should enable the [`webdriver` feature](#installing-optional-features) in your Homestead configuration: -->
Homestead 내에서 [Laravel Dusk](/docs/10.x/dusk) 테스트를 실행하려면, Homestead 설정에서 [`webdriver` feature](#installing-optional-features)을 활성화해야 합니다.

```yaml
features:
    - webdriver: true
```

<!-- After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal. -->
`webdriver` 기능을 활성화한 후, 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
<!-- ### Sharing Your Environment -->
### Sharing Your Environment

<!-- Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file. -->
간혹 현재 작업 중인 사이트를 동료나 클라이언트에게 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령을 통해 기본적인 공유 기능을 제공하지만, `Homestead.yaml` 파일에 여러 사이트가 등록되어 있다면 동작하지 않습니다.

<!-- To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`: -->
이 문제를 해결하기 위해 Homestead에는 자체 `share` 명령이 포함되어 있습니다. 먼저 `vagrant ssh`를 통해 [SSH into your Homestead virtual machine](#connecting-via-ssh) 후, `share homestead.test` 명령을 실행하면 됩니다. 이 명령은 `Homestead.yaml` 설정 파일에 정의된 `homestead.test` 사이트를 공유합니다. `homestead.test` 대신 다른 설정된 사이트 이름으로도 실행할 수 있습니다.

```shell
share homestead.test
```

<!-- After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command: -->
명령 실행 후, Ngrok 화면에 공유된 사이트의 활동 로그와 외부에서 접근 가능한 URL이 나타납니다. 지역(region), 서브도메인 등의 Ngrok 실행 옵션이 필요하다면 `share` 명령어에 추가로 지정할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

<!-- If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so. -->
HTTPS로 내용을 공유하고 싶다면, `share` 대신 `sshare` 명령을 사용하면 됩니다.

> [!WARNING]
> 참고로, Vagrant 자체는 안전한 보안 수단이 아니므로, `share` 명령을 실행하면 가상 머신이 인터넷에 노출된다는 점을 꼭 인지하세요.

<a name="debugging-and-profiling"></a>
<!-- ## Debugging and Profiling -->
## Debugging and Profiling

<a name="debugging-web-requests"></a>
<!-- ### Debugging Web Requests With Xdebug -->
### Debugging Web Requests With Xdebug

<!-- Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code. -->
Homestead에는 [Xdebug](https://xdebug.org)를 통한 단계별(스텝) 디버깅 기능이 내장되어 있습니다. 예를 들어 브라우저로 웹 페이지에 접근하면, PHP가 IDE와 연결되어 코드의 동작 과정을 직접 확인하거나 수정할 수 있습니다.

<!-- By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/). -->
기본적으로 Xdebug는 이미 실행 중이며, 연결을 기다리고 있습니다. CLI(명령줄)에서 Xdebug를 활성화하려면 Homestead 가상 머신 안에서 `sudo phpenmod xdebug` 명령을 실행하면 됩니다. 이후에는 사용하는 IDE 설명서에 따라 디버깅을 사용하면 됩니다. 마지막으로, 브라우저에서 Xdebug를 활성화하려면 브라우저 확장 프로그램이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)을 사용할 수도 있습니다.

> [!WARNING]
> Xdebug가 활성화되면 PHP의 실행 속도가 매우 느려질 수 있습니다. 비활성화하려면 Homestead 가상 머신에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하면 됩니다.

<a name="autostarting-xdebug"></a>
<!-- #### Autostarting Xdebug -->
#### Autostarting Xdebug

<!-- When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration: -->
기능 테스트 등에서 웹 서버로의 요청을 디버깅할 때, 매번 테스트 코드에 헤더나 쿠키를 추가해 트리거하지 않고, 디버깅을 자동 시작하는 방법이 더 편리합니다. Xdebug를 항상 자동 시작하게 하려면, Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일에 아래 설정을 추가하세요.

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
PHP CLI 애플리케이션을 디버깅하려면, Homestead 가상 머신 안에서 `xphp` 셸 별칭을 사용할 수 있습니다.

<!--     xphp /path/to/script -->
    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
<!-- ### Profiling Applications With Blackfire -->
### Profiling Applications With Blackfire

<!-- [Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings. -->
[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션의 성능을 분석(프로파일링)할 수 있는 서비스입니다. 인터랙티브한 UI에서 호출 그래프, 실행 타임라인 등 다양한 프로파일 데이터를 확인할 수 있으며, 개발·테스트·운영 환경 모두에서 사용할 수 있습니다. 또한 Blackfire는 코드와 `php.ini` 설정에 대한 성능, 품질, 보안 체크도 제공합니다.

<!-- The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios. -->
[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈소스 웹 크롤링, 웹 테스트, 웹 스크래핑 도구로 Blackfire와 연계해 프로파일링 시나리오를 스크립트로 자동화할 수 있습니다.

<!-- To enable Blackfire, use the "features" setting in your Homestead configuration file: -->
Blackfire를 활성화하려면, Homestead 설정 파일의 "features" 항목을 사용합니다.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

<!-- Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index). -->
Blackfire 서버 인증 정보 및 클라이언트 인증 정보는 [require a Blackfire account](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 방법으로 애플리케이션 프로파일링을 제공합니다. 더 자세한 내용은 [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
<!-- ## Network Interfaces -->
## Network Interfaces

<!-- The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary: -->
`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스 구성을 담당합니다. 원하는 만큼 여러 개의 인터페이스를 설정할 수 있습니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

<!-- To enable a [bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) interface, configure a `bridge` setting for the network and change the network type to `public_network`: -->
[bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 네트워크를 활성화하려면, 네트워크의 type을 `public_network`로 변경하고 `bridge` 설정을 추가하세요.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To enable [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), just remove the `ip` option from your configuration: -->
[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 사용하려면, 설정에서 `ip` 옵션을 제거하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To update what device the network is using, you may add a `dev` option to the network's configuration. The default `dev` value is `eth0`: -->
사용할 디바이스를 변경하려면, 네트워크 설정에 `dev` 옵션을 추가하면 됩니다. 기본 `dev` 값은 `eth0`입니다.

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
Homestead는 Homestead 디렉터리(루트)에 있는 `after.sh` 스크립트를 이용해 확장할 수 있습니다. 이 파일에 필요한 셸 명령어를 추가하면 가상 머신을 원하는 대로 더 세부적으로 설정, 커스터마이징할 수 있습니다.

<!-- When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead: -->
Homestead에 패키지를 설치할 때, Ubuntu에서 기존 설정 파일을 유지할지 새 구성 파일로 덮어쓸지 묻기도 합니다. Homestead에서 기존 환경설정을 보존하려면 아래와 같이 패키지 설치 명령어를 사용하면 됩니다.

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
Homestead를 팀과 함께 사용할 때, 각자 개발 스타일에 맞춰 Homestead를 좀 더 개별적으로 조정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리(동일한 위치에 `Homestead.yaml`이 있음)에 `user-customizations.sh` 파일을 만들고, 필요한 내용을 추가하면 됩니다. 단, `user-customizations.sh` 파일은 버전 관리에 포함하지 않아야 합니다.

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
기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 지정합니다. 이 설정은 Homestead가 호스트 운영체제의 DNS 설정을 사용할 수 있도록 해줍니다. 이 동작을 바꾸고 싶다면, `Homestead.yaml` 파일에 다음 설정을 추가하면 됩니다.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```
