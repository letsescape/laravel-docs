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
Laravel은 전체 PHP 개발 경험이 즐거울 수 있도록, 로컬 개발 환경까지 포함해 모두를 쉽게 만들어 주고자 합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식적으로 제공되는, 미리 구성된 Vagrant 박스로, 여러분의 로컬 컴퓨터에 PHP, 웹 서버, 또는 그 외 서버용 소프트웨어를 직접 설치하지 않고도 쾌적한 개발 환경을 사용할 수 있도록 도와줍니다.

<!-- [Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes! -->
[Vagrant](https://www.vagrantup.com)는 가상 머신을 쉽게 관리하고 구성할 수 있는 간단하고 우아한 방식을 제공합니다. Vagrant 박스는 완전히 재사용이 가능합니다. 무언가 잘못되더라도 박스를 삭제하고 몇 분 만에 다시 생성할 수 있습니다!

<!-- Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications. -->
Homestead는 Windows, macOS, Linux 등 어떤 운영체제에서도 실행 가능하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 다양한 소프트웨어를 함께 포함하고 있어서 Laravel 프로젝트 개발에 필요한 모든 환경을 제공합니다.

> [!WARNING]
> Windows를 사용하는 경우에는 하드웨어 가상화(VT-x) 기능을 활성화해야 할 수 있습니다. 이 기능은 주로 BIOS에서 켤 수 있습니다. UEFI 시스템에서 Hyper-V를 사용 중이라면, VT-x 사용을 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

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
Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 아래 지원되는 공급자(provider) 중 하나를 먼저 설치해야 합니다:

<!--
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)
-->
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

<!-- All of these software packages provide easy-to-use visual installers for all popular operating systems. -->
이 소프트웨어들은 모두 주요 운영체제에서 손쉽게 설치할 수 있도록 시각적인 설치 프로그램을 제공합니다.

<!-- To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge. -->
Parallels 공급자를 사용하려면 [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels)을 추가로 설치해야 하며, 무료로 사용할 수 있습니다.

<a name="installing-homestead"></a>
<!-- #### Installing Homestead -->
#### Installing Homestead

<!-- You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory": -->
Homestead는 해당 저장소를 호스트 머신에 클론하여 설치할 수 있습니다. Homestead 가상머신이 Laravel 애플리케이션 전체의 호스트 역할을 하게 되므로, 저장소를 "홈" 디렉터리 아래의 `Homestead` 폴더로 클론하는 것을 권장합니다. 이 문서 전반에서는 이 폴더를 “Homestead 디렉터리”라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

<!-- After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead: -->
Laravel Homestead 저장소를 클론한 후에는, 반드시 `release` 브랜치를 체크아웃하세요. 이 브랜치에는 항상 Homestead의 최신 안정 릴리스가 포함되어 있습니다:

```shell
cd ~/Homestead

git checkout release
```

<!-- Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory: -->
그 다음, Homestead 디렉터리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 설정 파일을 생성합니다. `Homestead.yaml`은 Homestead의 모든 설정을 지정하는 파일로, Homestead 디렉터리 내부에 생성됩니다:

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
`Homestead.yaml` 파일의 `provider` 키를 통해 사용할 Vagrant 공급자(예: `virtualbox` 또는 `parallels`)를 지정할 수 있습니다:


```
provider: virtualbox
```


> [!WARNING]
> Apple 실리콘(M1/M2) 칩을 사용하는 경우 Parallels 공급자를 반드시 사용해야 합니다.

<a name="configuring-shared-folders"></a>
<!-- #### Configuring Shared Folders -->
#### Configuring Shared Folders

<!-- The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary: -->
`Homestead.yaml` 파일의 `folders` 속성에는 Homestead 환경과 공유할 폴더 목록을 지정할 수 있습니다. 이 폴더에 있는 파일이 변경되면, 로컬 머신과 Homestead 가상환경 간에 동기화됩니다. 필요한 만큼 여러 개의 공유 폴더를 지정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 문법 대신 프로젝트의 전체 경로(예: `C:\Users\user\Code\project1`)를 사용해야 합니다.

<!-- You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder: -->
각 애플리케이션은 개별 폴더 매핑을 통해 연결하는 것이 좋습니다. 단일 대용량 디렉터리를 통째로 매핑하면, 가상머신이 해당 폴더 내부 '모든' 파일의 디스크 IO를 추적해야 하므로, 파일 개수가 많을 경우 성능이 저하될 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 절대로 `.`(현재 디렉터리)를 마운트하지 마십시오. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않고, 선택적 기능들이 손상되거나 예기치 않은 현상이 발생할 수 있습니다.

<!-- To enable [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), you may add a `type` option to your folder mapping: -->
[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs) 기능을 활성화하고 싶다면 폴더 매핑에 `type` 옵션을 추가하면 됩니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 해당 플러그인은 가상머신 내 폴더와 파일의 사용자/그룹 권한 문제를 올바르게 관리해 줍니다.

<!-- You may also pass any options supported by Vagrant's [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) by listing them under the `options` key: -->
Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)에서 지원하는 다양한 옵션을 `options` 키를 통해 전달할 수도 있습니다:

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
Nginx가 익숙하지 않더라도 걱정하지 마세요. `Homestead.yaml` 파일의 `sites` 속성을 사용하면, Homestead 내 "도메인"을 간단히 원하는 폴더에 매핑할 수 있습니다. `Homestead.yaml` 파일에는 예제 사이트 구성도 기본 포함되어 있습니다. 여러 개의 사이트를 추가해도 무방하며, Homestead는 작업 중인 모든 Laravel 애플리케이션에 대해 편리한 가상 환경 역할을 할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

<!-- If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine. -->
Homestead 가상머신을 프로비저닝한 뒤에 `sites` 속성을 수정했다면, 변경 내용을 적용하려면 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다. 이 명령어는 가상머신 내 Nginx 설정을 자동으로 갱신합니다.

> [!WARNING]
> Homestead 스크립트는 최대한 idempotent(여러 번 반복 실행해도 결과가 같은)하게 동작하도록 만들어졌으나, 프로비저닝 중 문제가 발생하면 `vagrant destroy && vagrant up` 명령어를 사용하여 머신을 완전히 삭제 후 재생성하는 것이 좋습니다.

<a name="hostname-resolution"></a>
<!-- #### Hostname Resolution -->
#### Hostname Resolution

<!-- Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US). -->
Homestead는 자동 호스트명 해석을 위해 `mDNS`를 사용하여 호스트명을 퍼블리시합니다. 예를 들어, `Homestead.yaml` 파일에 `hostname: homestead`를 설정했다면, `homestead.local` 주소로 접속할 수 있습니다. macOS, iOS, 그리고 대부분의 Linux 데스크톱 배포판에는 `mDNS` 지원이 기본 내장되어 있습니다. Windows 사용자의 경우, [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 추가로 설치해야 합니다.

<!-- Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following: -->
[per project installations](#per-project-installation) 방식의 Homestead에서 자동 호스트명을 사용하는 것이 가장 편리합니다. 하나의 Homestead 인스턴스에 여러 사이트를 운영하는 경우, 웹사이트의 "도메인"을 자신의 컴퓨터 `hosts` 파일에 추가해야 합니다. 이 `hosts` 파일은 Homestead 사이트로 향하는 요청을 Homestead 가상 머신으로 리다이렉트해 줍니다. macOS나 Linux는 `/etc/hosts` 위치에, Windows는 `C:\Windows\System32\drivers\etc\hosts`에 해당 파일이 있습니다. 다음과 같은 형식으로 추가하면 됩니다:

```
192.168.56.56  homestead.test
```

<!-- Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser: -->
입력한 IP 주소가 `Homestead.yaml` 파일에 지정한 값과 일치하는지 반드시 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스 실행이 완료되면, 브라우저에서 다음과 같이 사이트를 접근할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
<!-- ### Configuring Services -->
### Configuring Services

<!-- Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file: -->
Homestead는 여러 서비스를 기본으로 시작하지만, 프로비저닝 시점에 활성화하거나 비활성화할 서비스를 직접 지정할 수도 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL은 비활성화하려면 `Homestead.yaml` 파일의 `services` 옵션을 아래와 같이 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

<!-- The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives. -->
여기서 지정한 서비스는 `enabled` 및 `disabled` 지시어의 순서에 따라 시작되거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
<!-- ### Launching the Vagrant Box -->
### Launching the Vagrant Box

<!-- Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites. -->
`Homestead.yaml` 파일의 설정을 완료했다면, Homestead 디렉터리에서 `vagrant up` 명령어를 실행하세요. 그러면 Vagrant가 가상머신을 부팅하고, 공유 폴더와 Nginx 사이트 역시 자동으로 구성합니다.

<!-- To destroy the machine, you may use the `vagrant destroy` command. -->
머신을 삭제하고 싶을 때는 `vagrant destroy` 명령어를 사용할 수 있습니다.

<a name="per-project-installation"></a>
<!-- ### Per Project Installation -->
### Per Project Installation

<!-- Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository. -->
Homestead를 전역(global)으로 설치하여 여러 프로젝트에서 같은 가상머신을 공유하는 대신, 각 프로젝트마다 개별 Homestead 인스턴스를 구성할 수도 있습니다. 만약 프로젝트와 함께 `Vagrantfile`을 포함해 전달하고 싶거나, 저장소를 복제한 팀원들도 바로 `vagrant up`만으로 환경을 띄우게 하려면 프로젝트별 Homestead 설치가 매우 유용합니다.

<!-- You may install Homestead into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용해 프로젝트에 Homestead를 설치하세요:

```shell
composer require laravel/homestead --dev
```

<!-- Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file: -->
설치가 완료되면, Homestead의 `make` 명령어를 실행해 프로젝트를 위한 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 두 파일 모두 프로젝트의 루트에 위치하게 되며, `make` 명령어는 `Homestead.yaml`의 `sites` 및 `folders` 설정을 자동으로 구성해 줍니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

<!-- Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution). -->
이제 터미널에서 `vagrant up` 명령어를 실행한 뒤, 브라우저에서 `http://homestead.test` 주소로 프로젝트에 접속할 수 있습니다. 단, 자동 [hostname resolution](#hostname-resolution)을 사용하지 않을 경우, `homestead.test`(또는 원하는 도메인명)를 `/etc/hosts` 파일에 등록해야 함을 잊지 마세요.

<a name="installing-optional-features"></a>
<!-- ### Installing Optional Features -->
### Installing Optional Features

<!-- Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options: -->
선택적인 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 true/false 값으로 간단히 활성화 또는 비활성화할 수 있으며, 일부는 여러 옵션을 설정할 수도 있습니다:

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
Elasticsearch의 지원되는 버전(정확한 major.minor.patch 형태의 버전 번호)을 지정할 수 있습니다. 기본 설치 시 클러스터 이름은 'homestead'로 생성됩니다. Elasticsearch는 운영체제 메모리의 절반 이상을 할당하면 안 되므로, Homestead 가상머신의 메모리가 할당량의 두 배 이상이 되도록 조정하세요.

> [!NOTE]
> [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하여 환경 설정을 커스터마이즈하는 방법을 확인할 수 있습니다.

<a name="mariadb"></a>
<!-- #### MariaDB -->
#### MariaDB

<!-- Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration. -->
MariaDB를 활성화하면 MySQL은 제거되고 MariaDB가 설치됩니다. MariaDB는 MySQL의 대체재로 사용할 수 있으니, 애플리케이션의 데이터베이스 설정에서 여전히 `mysql` 데이터베이스 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`. -->
MongoDB를 기본 설치할 경우 기본 데이터베이스의 사용자명은 `homestead`, 비밀번호는 `secret`으로 지정됩니다.

<a name="neo4j"></a>
<!-- #### Neo4j -->
#### Neo4j

<!-- The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client. -->
Neo4j를 기본 설치할 경우, 데이터베이스의 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다. Neo4j 브라우저에 접속하려면 웹 브라우저에서 `http://homestead.test:7474`로 접속하세요. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)이 Neo4j 클라이언트 요청을 처리하도록 준비되어 있습니다.

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory: -->
Homestead 가상머신 내에서 Bash 별칭을 사용하려면, Homestead 디렉터리 안의 `aliases` 파일을 수정하세요:

```shell
alias c='clear'
alias ..='cd ..'
```

<!-- After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine. -->
`aliases` 파일을 수정한 후에는 반드시 `vagrant reload --provision` 명령어로 Homestead 가상머신을 다시 프로비저닝해야 새로운 별칭이 적용됩니다.

<a name="updating-homestead"></a>
<!-- ## Updating Homestead -->
## Updating Homestead

<!-- Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory: -->
Homestead를 업데이트하기 전에, 먼저 Homestead 디렉터리 내에서 아래 명령어로 기존 가상머신을 삭제해야 합니다:

```shell
vagrant destroy
```

<!-- Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository: -->
그 다음, Homestead 소스 코드를 업데이트해야 합니다. 저장소를 직접 클론해서 설치했다면, 저장소 경로에서 다음 명령어를 차례로 실행하면 됩니다:

```shell
git fetch

git pull origin release
```

<!-- These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases). -->
위 명령들은 GitHub 저장소에서 최신 Homestead 코드를 가져오고, 최신 태그를 설치한 뒤 최신 릴리스 버전을 체크아웃합니다. Homestead의 안정화된 최신 릴리스 버전은 [GitHub releases page](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

<!-- If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies: -->
만약 프로젝트의 `composer.json` 파일을 통해 Homestead를 설치한 경우, `composer.json` 파일이 `"laravel/homestead": "^12"`를 포함하는지 확인한 뒤 아래와 같이 의존성을 업데이트하세요:

```shell
composer update
```

<!-- Next, you should update the Vagrant box using the `vagrant box update` command: -->
그리고 나서, Vagrant 박스를 `vagrant box update` 명령어로 업데이트해야 합니다:

```shell
vagrant box update
```

<!-- After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files: -->
Vagrant 박스를 업데이트한 후, Homestead 디렉터리에서 `bash init.sh` 명령어로 추가 설정 파일을 업데이트하세요. 이 과정에서 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸 것인지 묻는 안내가 나타납니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<!-- Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation: -->
마지막으로, 최신 Vagrant 설치 내용을 적용하려면 Homestead 가상머신을 재생성해야 합니다:

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
Homestead 디렉터리 내에서 터미널로 `vagrant ssh` 명령어를 실행하면 가상머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
<!-- ### Adding Additional Sites -->
### Adding Additional Sites

<!-- Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file. -->
Homestead 환경이 프로비저닝되어 실행 중이라면, 다른 Laravel 프로젝트를 위한 추가 Nginx 사이트도 편리하게 등록할 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 동시에 운영할 수 있습니다. 추가 사이트를 등록하려면, 해당 사이트 정보를 `Homestead.yaml` 파일에 추가하십시오.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트 추가 시 반드시 먼저 해당 프로젝트의 [folder mapping](#configuring-shared-folders)이 설정되어 있는지 확인하세요.

<!-- If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`: -->
만약 Vagrant가 자동으로 "hosts" 파일을 관리하지 않는다면, 새 사이트 정보도 추가로 hosts 파일에 등록해야 합니다. macOS나 Linux의 경우 `/etc/hosts`, Windows의 경우 `C:\Windows\System32\drivers\etc\hosts`에 다음과 같이 입력하세요:

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

<!-- Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory. -->
사이트를 추가했다면, Homestead 디렉터리에서 터미널로 `vagrant reload --provision` 명령어를 실행하여 변경 사항을 적용하세요.

<a name="site-types"></a>
<!-- #### Site Types -->
#### Site Types

<!-- Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type: -->
Homestead는 다양한 "타입(type)"의 사이트를 지원합니다. 이를 이용하면 Laravel 기반이 아닌 프로젝트도 쉽게 실행할 수 있습니다. 예를 들어, `statamic` 사이트 타입을 활용하여 Statamic 애플리케이션을 Homestead에 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

<!-- The available site types are: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (the default), `proxy` (for nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`. -->
지원되는 사이트 타입은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 등이 있습니다.

<a name="site-parameters"></a>
<!-- #### Site Parameters -->
#### Site Parameters

<!-- You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive: -->
`params` 사이트 지시어를 사용하면, 사이트별로 추가 Nginx `fastcgi_param` 값을 지정할 수 있습니다:

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
글로벌 환경 변수는 `Homestead.yaml` 파일에 추가하여 지정할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

<!-- After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user. -->
`Homestead.yaml` 파일 변경 후 반드시 `vagrant reload --provision` 명령어로 머신을 다시 프로비저닝해야 합니다. 이렇게 하면 모든 PHP 버전의 PHP-FPM 설정과 `vagrant` 사용자 환경 변수도 함께 업데이트됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- By default, the following ports are forwarded to your Homestead environment: -->
기본적으로 아래 포트들은 Homestead 환경으로 포워딩됩니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
-->
- **HTTP:** 8000 → 80 포트로 포워딩
- **HTTPS:** 44300 → 443 포트로 포워딩

<!-- </div> -->
</div>

<a name="forwarding-additional-ports"></a>
<!-- #### Forwarding Additional Ports -->
#### Forwarding Additional Ports

<!-- If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command: -->
필요하다면 `Homestead.yaml` 파일에 `ports` 설정 항목을 정의해 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. `Homestead.yaml` 파일을 수정한 후에는 반드시 `vagrant reload --provision` 명령어로 머신을 다시 프로비저닝해야 합니다:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

<!-- Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box: -->
아래는 호스트 머신에서 Vagrant 박스로 매핑할 수 있는 Homestead 서비스 포트 목록입니다:

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
- **SSH:** 2222 → 22 포트로
- **ngrok UI:** 4040 → 4040 포트로
- **MySQL:** 33060 → 3306 포트로
- **PostgreSQL:** 54320 → 5432 포트로
- **MongoDB:** 27017 → 27017 포트로
- **Mailpit:** 8025 → 8025 포트로
- **Minio:** 9600 → 9600 포트로

<!-- </div> -->
</div>

<a name="php-versions"></a>
<!-- ### PHP Versions -->
### PHP Versions

<!-- Homestead supports running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", and "8.3", (the default): -->
Homestead는 한 대의 가상머신에서 여러 PHP 버전을 지원합니다. `Homestead.yaml` 파일에서 사이트별로 사용할 PHP 버전을 지정할 수 있습니다. 지원되는 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값)입니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

<!-- [Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI: -->
[Within your Homestead virtual machine](#connecting-via-ssh)에서는 CLI 환경에서 아래처럼 지원되는 PHP 버전을 사용할 수 있습니다:

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
CLI에서 기본적으로 사용할 PHP 버전을 변경하고 싶다면, Homestead 가상머신 내에서 아래 명령어들을 실행하면 됩니다:

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
MySQL과 PostgreSQL 모두에서 `homestead` 데이터베이스가 기본적으로 구성되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL 데이터베이스에 연결하려면 `127.0.0.1`의 `33060` 포트(MySQL) 또는 `54320` 포트(PostgreSQL)로 접속해야 합니다. 두 데이터베이스의 사용자명과 비밀번호는 각각 `homestead` / `secret`입니다.

> [!WARNING]
> 이러한 비표준 포트는 오직 호스트 머신에서 데이터베이스에 접속할 때만 사용해야 합니다. Laravel 애플리케이션의 `database` 설정 파일에서는 기본 포트인 3306과 5432를 사용해야 합니다. Laravel 애플리케이션은 가상 머신 _내부_ 에서 실행되기 때문입니다.

<a name="database-backups"></a>
<!-- ### Database Backups -->
### Database Backups

<!-- Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file: -->
Homestead는 Homestead 가상 머신이 삭제될 때 데이터베이스를 자동으로 백업해줄 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요합니다. 만약 더 이전 버전의 Vagrant를 사용한다면, `vagrant-triggers` 플러그인을 설치해야 합니다. 데이터베이스 자동 백업 기능을 활성화하려면, `Homestead.yaml` 파일에 다음과 같이 추가합니다.


```
backup: true
```


<!-- Once configured, Homestead will export your databases to `.backup/mysql_backup` and `.backup/postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method. -->
이렇게 설정한 후에는 `vagrant destroy` 명령어가 실행될 때 Homestead가 데이터베이스를 `.backup/mysql_backup`과 `.backup/postgres_backup` 디렉터리에 내보냅니다. 이 디렉터리들은 Homestead를 설치한 폴더 안에 생성되며, [per project installation](#per-project-installation) 방식을 사용할 경우 프로젝트 루트에서 확인할 수 있습니다.

<a name="configuring-cron-schedules"></a>
<!-- ### Configuring Cron Schedules -->
### Configuring Cron Schedules

<!-- Laravel provides a convenient way to [schedule cron jobs](/docs/11.x/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `routes/console.php` file to determine which scheduled tasks to run. -->
Laravel은 [schedule cron jobs](/docs/11.x/scheduling)을 편리하게 제공하며, `schedule:run` 아티즌 명령어를 1분마다 실행하도록 스케줄만 등록하면 됩니다. `schedule:run` 명령어는 `routes/console.php` 파일에 정의된 작업 스케줄을 확인해 어떤 예약 작업을 실행할지 결정합니다.

<!-- If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site: -->
Homestead 사이트에서 `schedule:run` 명령어가 실행되도록 하고 싶다면, 사이트를 설정할 때 `schedule` 옵션을 `true`로 지정하면 됩니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

<!-- The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine. -->
해당 사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 생성됩니다.

<a name="configuring-mailpit"></a>
<!-- ### Configuring Mailpit -->
### Configuring Mailpit

<!-- [Mailpit](https://github.com/axllent/mailpit) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings: -->
[Mailpit](https://github.com/axllent/mailpit)은 메일을 실제 수신자에게 전송하지 않고도, 발송되는 이메일을 가로채어 내용을 직접 확인할 수 있도록 도와줍니다. 사용을 시작하려면 애플리케이션의 `.env` 파일을 아래와 같이 수정하세요.

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

<!-- Once Mailpit has been configured, you may access the Mailpit dashboard at `http://localhost:8025`. -->
Mailpit 설정을 마치면, 브라우저에서 `http://localhost:8025`로 접속하여 Mailpit 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
<!-- ### Configuring Minio -->
### Configuring Minio

<!-- [Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section: -->
[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 API를 갖춘 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 [features](#installing-optional-features) 섹션에 아래와 같이 `Homestead.yaml` 파일을 수정하세요.


```
minio: true
```


<!-- By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`. -->
기본적으로 Minio는 9600 포트에서 사용할 수 있습니다. `http://localhost:9600`으로 접속하면 Minio 관리 패널에 접근할 수 있습니다. 기본 access key는 `homestead`, secret key는 `secretkey`입니다. Minio에 접근할 때는 반드시 `us-east-1` 지역(region)을 사용해야 합니다.

<!-- In order to use Minio, ensure your `.env` file has the following options: -->
Minio를 제대로 사용하려면 아래처럼 `.env` 파일을 설정해야 합니다.

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

<!-- To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal: -->
Minio를 이용한 "S3" 버킷을 생성하려면, `Homestead.yaml` 파일에 `buckets` 항목을 추가하세요. 버킷을 정의한 후, 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

<!-- Supported `policy` values include: `none`, `download`, `upload`, and `public`. -->
지정 가능한 `policy` 값에는 `none`, `download`, `upload`, `public`이 있습니다.

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- In order to run [Laravel Dusk](/docs/11.x/dusk) tests within Homestead, you should enable the [`webdriver` feature](#installing-optional-features) in your Homestead configuration: -->
[Laravel Dusk](/docs/11.x/dusk) 테스트를 Homestead 내부에서 실행하고 싶다면, Homestead 설정에서 [`webdriver` feature](#installing-optional-features)을 활성화해야 합니다.

```yaml
features:
    - webdriver: true
```

<!-- After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal. -->
`webdriver` 기능을 활성화한 후 터미널에서 `vagrant reload --provision` 명령어를 실행하세요.

<a name="sharing-your-environment"></a>
<!-- ### Sharing Your Environment -->
### Sharing Your Environment

<!-- Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file. -->
동료나 클라이언트와 현재 작업하고 있는 내용을 공유하고 싶을 때가 있습니다. Vagrant는 `vagrant share` 명령어를 통해 이런 기능을 기본으로 제공합니다. 하지만 `Homestead.yaml` 파일에 여러 사이트를 설정해 둔 경우에는 이 기능이 정상적으로 작동하지 않습니다.

<!-- To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`: -->
이 문제를 해결하기 위해 Homestead에는 자체적으로 `share` 명령어가 제공됩니다. 먼저 `vagrant ssh`로 [SSH into your Homestead virtual machine](#connecting-via-ssh)한 뒤, `share homestead.test` 명령어를 실행합니다. 이 명령어는 `Homestead.yaml` 설정 파일에 정의된 `homestead.test` 사이트를 공유합니다. `homestead.test` 대신 설정해 둔 다른 사이트 이름으로 대체할 수 있습니다.

```shell
share homestead.test
```

<!-- After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command: -->
명령어를 실행하면 Ngrok 화면이 열리며, 활동 로그와 공유 사이트에 접근할 수 있는 공개 URL이 나타납니다. 별도의 region(지역), subdomain(서브도메인), 또는 기타 Ngrok 런타임 옵션을 지정하고 싶다면 아래와 같이 `share` 명령어에 추가할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

<!-- If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so. -->
HTTP 대신 HTTPS로 콘텐츠를 공유해야 한다면, `share` 대신 `sshare` 명령어를 사용하면 됩니다.

> [!WARNING]
> Vagrant는 본질적으로 안전하지 않으므로, `share` 명령어를 사용하는 동안에는 가상 머신이 인터넷에 노출된다는 점을 반드시 유념하세요.

<a name="debugging-and-profiling"></a>
<!-- ## Debugging and Profiling -->
## Debugging and Profiling

<a name="debugging-web-requests"></a>
<!-- ### Debugging Web Requests With Xdebug -->
### Debugging Web Requests With Xdebug

<!-- Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code. -->
Homestead는 [Xdebug](https://xdebug.org)를 이용한 단계별(step) 디버깅을 지원합니다. 예를 들어, 브라우저에서 어떤 페이지에 접근하면 PHP가 IDE와 연결되어 동작 중인 코드를 확인하거나 수정할 수 있습니다.

<!-- By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/). -->
기본적으로 Xdebug는 이미 활성화되어 있으며 연결할 준비가 되어 있습니다. CLI에서 Xdebug를 활성화해야 할 경우, Homestead 가상 머신 내에서 `sudo phpenmod xdebug` 명령어를 실행하세요. IDE의 안내에 따라 디버깅을 적용하고, 브라우저에는 확장 프로그램이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)을 추가해 Xdebug가 동작하도록 설정합니다.

> [!WARNING]
> Xdebug를 활성화하면 PHP 실행 속도가 현저히 느려집니다. Xdebug를 비활성화하고 싶다면 Homestead 가상 머신 내에서 `sudo phpdismod xdebug` 명령어를 실행한 뒤 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
<!-- #### Autostarting Xdebug -->
#### Autostarting Xdebug

<!-- When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration: -->
웹 서버에 요청을 보내는 기능 테스트를 디버깅할 때, 디버깅을 수동으로 트리거하지 않고 자동으로 시작되게 하는 것이 더 편리합니다. Xdebug를 자동 실행하도록 강제하려면, Homestead 가상 머신 내부의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하고 아래 설정을 추가하세요.

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
PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신에서 `xphp` 셸 별칭을 사용하세요.

<!--     xphp /path/to/script -->
    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
<!-- ### Profiling Applications With Blackfire -->
### Profiling Applications With Blackfire

<!-- [Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings. -->
[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션의 실행 프로파일링을 위한 서비스입니다. 프로파일 데이터를 호출 그래프 및 타임라인으로 보여주는 인터랙티브한 사용자 인터페이스를 제공합니다. 개발 환경뿐 아니라 스테이징, 프로덕션 환경에서도 사용할 수 있으며, 최종 사용자에겐 오버헤드가 없습니다. 추가로, Blackfire는 코드 및 `php.ini` 설정에 대해 성능, 품질, 보안 점검 기능을 제공합니다.

<!-- The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios. -->
[Blackfire Player](https://blackfire.io/docs/player/index)는 오픈소스 웹 크롤링, 웹 테스트, 웹 스크래핑 애플리케이션으로, Blackfire와 연동하여 프로파일링 시나리오를 스크립트로 작성할 수 있습니다.

<!-- To enable Blackfire, use the "features" setting in your Homestead configuration file: -->
Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 항목에 아래와 같이 추가합니다.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

<!-- Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index). -->
Blackfire 서버 및 클라이언트 인증 정보는 [require a Blackfire account](https://blackfire.io/signup)이 필요합니다. Blackfire는 CLI 도구, 브라우저 확장 등 다양한 방법으로 애플리케이션을 프로파일링할 수 있습니다. 자세한 내용은 [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
<!-- ## Network Interfaces -->
## Network Interfaces

<!-- The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary: -->
`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 여러 개의 인터페이스를 구성할 수 있습니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

<!-- To enable a [bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) interface, configure a `bridge` setting for the network and change the network type to `public_network`: -->
[bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면 네트워크의 설정에 `bridge`를 추가하고, network 타입을 `public_network`로 변경하세요.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To enable [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), just remove the `ip` option from your configuration: -->
[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 사용하려면, 설정에서 `ip` 옵션만 제거하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To update what device the network is using, you may add a `dev` option to the network's configuration. The default `dev` value is `eth0`: -->
네트워크가 사용하는 디바이스를 변경하려면, network 설정에 `dev` 옵션을 추가할 수 있습니다. 기본 `dev` 값은 `eth0`입니다.

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
Homestead는 Homestead 디렉터리의 루트에 있는 `after.sh` 스크립트를 이용해 확장할 수 있습니다. 이 파일에서 가상 머신을 적절하게 구성, 커스터마이즈하는 데 필요한 모든 셸 명령어를 추가할 수 있습니다.

<!-- When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead: -->
Homestead를 커스터마이즈할 때, 우분투가 패키지의 원본 설정을 유지할지 아니면 새 설정 파일로 덮어쓸지 물어볼 수 있습니다. 이를 방지하려면 패키지 설치 시, 기존에 Homestead에서 작성했던 설정을 보존하는 다음 명령어를 사용하세요.

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
팀과 함께 Homestead를 사용하다 보면 개인의 개발 스타일에 맞게 Homestead를 조정하고 싶을 수 있습니다. 이럴 때를 위해 `Homestead.yaml` 파일과 같은 위치(루트)에 `user-customizations.sh` 파일을 만들 수 있습니다. 여기에는 원하는 모든 커스터마이징 내용을 적용하면 되지만, `user-customizations.sh` 파일은 버전 관리 대상에 포함시키지 않아야 합니다.

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
기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이로 인해 Homestead는 호스트 운영 체제의 DNS 설정을 사용할 수 있습니다. 이 동작을 직접 제어하고 싶다면, `Homestead.yaml` 파일에 아래와 같이 설정 옵션을 추가하세요.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```