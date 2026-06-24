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
> <!-- Laravel Homestead is a legacy package that is no longer actively maintained. [Laravel Sail](/docs/master/sail) may be used as a modern alternative. -->
> Laravel Homestead는 더 이상 활발히 유지보수되지 않는 레거시 패키지입니다. 최신 대안으로 [Laravel Sail](/docs/master/sail)을 사용할 수 있습니다.

<!-- Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, or any other server software on your local machine. -->
Laravel은 로컬 개발 환경을 포함한 PHP 개발 경험 전반을 즐겁게 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식 사전 패키징 Vagrant box로, 로컬 머신에 PHP, 웹 서버 또는 그 밖의 서버 소프트웨어를 설치하지 않아도 훌륭한 개발 환경을 제공합니다.

<!-- [Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes! -->
[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝하는 단순하고 세련된 방법을 제공합니다. Vagrant box는 완전히 폐기할 수 있습니다. 문제가 생기면 몇 분 안에 box를 삭제하고 다시 만들 수 있습니다!

<!-- Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications. -->
Homestead는 Windows, macOS, Linux 시스템 어디서나 실행되며, 뛰어난 Laravel 애플리케이션을 개발하는 데 필요한 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node와 기타 모든 소프트웨어를 포함합니다.

> [!WARNING]
> <!-- If you are using Windows, you may need to enable hardware virtualization (VT-x). It can usually be enabled via your BIOS. If you are using Hyper-V on a UEFI system you may additionally need to disable Hyper-V in order to access VT-x. -->
> Windows를 사용한다면 하드웨어 가상화(VT-x)를 활성화해야 할 수 있습니다. 일반적으로 BIOS에서 활성화할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용 중이라면 VT-x에 접근하기 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

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
- Webdriver & Laravel Dusk 유틸리티

<!-- </div> -->
</div>

<a name="installation-and-setup"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- Before launching your Homestead environment, you must install [Vagrant](https://developer.hashicorp.com/vagrant/downloads) as well as one of the following supported providers: -->
Homestead 환경을 실행하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 다음 지원 provider 중 하나를 설치해야 합니다.

<!--
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)
-->
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

<!-- All of these software packages provide easy-to-use visual installers for all popular operating systems. -->
이 소프트웨어 패키지는 모두 주요 운영체제에서 사용하기 쉬운 시각적 설치 프로그램을 제공합니다.

<!-- To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge. -->
Parallels provider를 사용하려면 [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
<!-- #### Installing Homestead -->
#### Installing Homestead

<!-- You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory": -->
호스트 머신에 Homestead 저장소를 클론하여 Homestead를 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로, "home" 디렉터리 안의 `Homestead` 폴더에 저장소를 클론하는 것을 고려해 보십시오. 이 문서에서는 이 디렉터리를 "Homestead 디렉터리"라고 부릅니다.

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

<!-- After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead: -->
Laravel Homestead 저장소를 클론한 후에는 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치에는 항상 Homestead의 최신 안정 릴리스가 들어 있습니다.

```shell
cd ~/Homestead

git checkout release
```

<!-- Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory: -->
다음으로 Homestead 디렉터리에서 `bash init.sh` 명령어를 실행하여 `Homestead.yaml` 설정 파일을 만듭니다. `Homestead.yaml` 파일은 Homestead 설치에 필요한 모든 설정을 구성하는 곳입니다. 이 파일은 Homestead 디렉터리에 생성됩니다.

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
`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant provider를 나타냅니다. 값은 `virtualbox` 또는 `parallels`입니다.

```
provider: virtualbox
```

> [!WARNING]
> <!-- If you are using Apple Silicon the Parallels provider is required. -->
> Apple Silicon을 사용한다면 Parallels provider가 필요합니다.

<a name="configuring-shared-folders"></a>
<!-- #### Configuring Shared Folders -->
#### Configuring Shared Folders

<!-- The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary: -->
`Homestead.yaml` 파일의 `folders` 프로퍼티에는 Homestead 환경과 공유할 모든 폴더를 나열합니다. 이 폴더 안의 파일이 변경되면 로컬 머신과 Homestead 가상 환경 간에 동기화됩니다. 필요한 만큼 공유 폴더를 설정할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> <!-- Windows users should not use the `~/` path syntax and instead should use the full path to their project, such as `C:\Users\user\Code\project1`. -->
> Windows 사용자는 `~/` 경로 문법을 사용하지 말고, `C:\Users\user\Code\project1`처럼 프로젝트의 전체 경로를 사용해야 합니다.

<!-- You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder: -->
모든 애플리케이션이 들어 있는 하나의 큰 디렉터리를 매핑하기보다, 개별 애플리케이션마다 별도의 폴더 매핑을 사용하는 것이 좋습니다. 폴더를 매핑하면 가상 머신은 해당 폴더 안의 *모든* 파일에 대한 디스크 IO를 추적해야 합니다. 폴더에 파일이 많으면 성능이 저하될 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> <!-- You should never mount `.` (the current directory) when using Homestead. This causes Vagrant to not map the current folder to `/vagrant` and will break optional features and cause unexpected results while provisioning. -->
> Homestead를 사용할 때는 절대 `.`(현재 디렉터리)를 마운트하지 않아야 합니다. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 못해 선택 기능이 깨지고 프로비저닝 중 예상치 못한 결과가 발생합니다.

<!-- To enable [NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs), you may add a `type` option to your folder mapping: -->
[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 활성화하려면 폴더 매핑에 `type` 옵션을 추가할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> <!-- When using NFS on Windows, you should consider installing the [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) plug-in. This plug-in will maintain the correct user / group permissions for files and directories within the Homestead virtual machine. -->
> Windows에서 NFS를 사용할 때는 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려해야 합니다. 이 플러그인은 Homestead 가상 머신 안의 파일과 디렉터리에 올바른 사용자 / 그룹 권한을 유지합니다.

<!-- You may also pass any options supported by Vagrant's [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage) by listing them under the `options` key: -->
`options` 키 아래에 옵션을 나열하여 Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)가 지원하는 어떤 옵션이든 전달할 수 있습니다.

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
Nginx에 익숙하지 않아도 괜찮습니다. `Homestead.yaml` 파일의 `sites` 프로퍼티를 사용하면 "domain"을 Homestead 환경의 폴더에 쉽게 매핑할 수 있습니다. `Homestead.yaml` 파일에는 샘플 사이트 설정이 포함되어 있습니다. 마찬가지로 Homestead 환경에 필요한 만큼 사이트를 추가할 수 있습니다. Homestead는 작업 중인 모든 Laravel 애플리케이션에 편리한 가상화 환경을 제공할 수 있습니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

<!-- If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine. -->
Homestead 가상 머신을 프로비저닝한 후 `sites` 프로퍼티를 변경했다면, 터미널에서 `vagrant reload --provision` 명령어를 실행하여 가상 머신의 Nginx 설정을 업데이트해야 합니다.

> [!WARNING]
> <!-- Homestead scripts are built to be as idempotent as possible. However, if you are experiencing issues while provisioning you should destroy and rebuild the machine by executing the `vagrant destroy && vagrant up` command. -->
> Homestead 스크립트는 가능한 한 멱등적으로 동작하도록 만들어져 있습니다. 그러나 프로비저닝 중 문제가 발생한다면 `vagrant destroy && vagrant up` 명령어를 실행하여 머신을 삭제한 뒤 다시 빌드해야 합니다.

<a name="hostname-resolution"></a>
<!-- #### Hostname Resolution -->
#### Hostname Resolution

<!-- Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US). -->
Homestead는 자동 호스트 해석을 위해 `mDNS`를 사용해 호스트명을 게시합니다. `Homestead.yaml` 파일에 `hostname: homestead`를 설정하면 `homestead.local`에서 호스트를 사용할 수 있습니다. macOS, iOS, Linux 데스크톱 배포판은 기본적으로 `mDNS` 지원을 포함합니다. Windows를 사용한다면 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

<!-- Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following: -->
자동 호스트명은 Homestead의 [per project installations](#per-project-installation)에 가장 잘 맞습니다. 하나의 Homestead 인스턴스에서 여러 사이트를 호스팅한다면, 웹 사이트의 "domains"를 머신의 `hosts` 파일에 추가할 수 있습니다. `hosts` 파일은 Homestead 사이트로 향하는 요청을 Homestead 가상 머신으로 리디렉션합니다. macOS와 Linux에서는 이 파일이 `/etc/hosts`에 있습니다. Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다. 이 파일에 추가하는 줄은 다음과 같습니다.

```text
192.168.56.56  homestead.test
```

<!-- Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser: -->
나열된 IP 주소가 `Homestead.yaml` 파일에 설정된 주소와 같은지 확인하십시오. `hosts` 파일에 도메인을 추가하고 Vagrant box를 실행하면 웹 브라우저에서 사이트에 접근할 수 있습니다.

```shell
http://homestead.test
```

<a name="configuring-services"></a>
<!-- ### Configuring Services -->
### Configuring Services

<!-- Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file: -->
Homestead는 기본적으로 여러 서비스를 시작합니다. 다만 프로비저닝 중 어떤 서비스를 활성화하거나 비활성화할지는 직접 지정할 수 있습니다. 예를 들어 `Homestead.yaml` 파일의 `services` 옵션을 수정하여 PostgreSQL을 활성화하고 MySQL을 비활성화할 수 있습니다.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

<!-- The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives. -->
지정한 서비스는 `enabled`와 `disabled` 지시어에 나열된 순서에 따라 시작되거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
<!-- ### Launching the Vagrant Box -->
### Launching the Vagrant Box

<!-- Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites. -->
`Homestead.yaml`을 원하는 대로 수정했다면 Homestead 디렉터리에서 `vagrant up` 명령어를 실행하십시오. Vagrant가 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동으로 설정합니다.

<!-- To destroy the machine, you may use the `vagrant destroy` command. -->
머신을 삭제하려면 `vagrant destroy` 명령어를 사용할 수 있습니다.

<a name="per-project-installation"></a>
<!-- ### Per Project Installation -->
### Per Project Installation

<!-- Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository. -->
Homestead를 전역으로 설치해 모든 프로젝트에서 같은 Homestead 가상 머신을 공유하는 대신, 관리하는 프로젝트마다 Homestead 인스턴스를 설정할 수 있습니다. 프로젝트와 함께 `Vagrantfile`을 제공하여 다른 작업자가 프로젝트 저장소를 클론한 직후 `vagrant up`을 실행할 수 있게 하려면, 프로젝트별 Homestead 설치가 유용할 수 있습니다.

<!-- You may install Homestead into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용하여 프로젝트에 Homestead를 설치할 수 있습니다.

```shell
composer require laravel/homestead --dev
```

<!-- Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file: -->
Homestead가 설치되면 Homestead의 `make` 명령어를 호출하여 프로젝트용 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 이 파일들은 프로젝트 루트에 배치됩니다. `make` 명령어는 `Homestead.yaml` 파일의 `sites`와 `folders` 지시어를 자동으로 설정합니다.

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

<!-- Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution). -->
다음으로 터미널에서 `vagrant up` 명령어를 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접근합니다. 자동 [hostname resolution](#hostname-resolution)을 사용하지 않는다면, `homestead.test` 또는 원하는 도메인에 대한 `/etc/hosts` 파일 항목을 여전히 추가해야 합니다.

<a name="installing-optional-features"></a>
<!-- ### Installing Optional Features -->
### Installing Optional Features

<!-- Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options: -->
선택 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션으로 설치합니다. 대부분의 기능은 boolean 값으로 활성화하거나 비활성화할 수 있으며, 일부 기능은 여러 설정 옵션을 허용합니다.

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
지원되는 Elasticsearch 버전을 지정할 수 있으며, 정확한 버전 번호(major.minor.patch)여야 합니다. 기본 설치는 'homestead'라는 클러스터를 생성합니다. Elasticsearch에는 운영체제 메모리의 절반을 초과하여 할당하면 안 되므로, Homestead 가상 머신에 Elasticsearch 할당량의 최소 두 배에 해당하는 메모리가 있는지 확인하십시오.

> [!NOTE]
> <!-- Check out the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current) to learn how to customize your configuration. -->
> 설정을 사용자 지정하는 방법은 [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 확인하십시오.

<a name="mariadb"></a>
<!-- #### MariaDB -->
#### MariaDB

<!-- Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration. -->
MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL의 드롭인 대체재로 동작하므로, 애플리케이션의 데이터베이스 설정에서는 여전히 `mysql` 데이터베이스 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`. -->
기본 MongoDB 설치는 데이터베이스 사용자명을 `homestead`로, 해당 비밀번호를 `secret`으로 설정합니다.

<a name="neo4j"></a>
<!-- #### Neo4j -->
#### Neo4j

<!-- The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client. -->
기본 Neo4j 설치는 데이터베이스 사용자명을 `homestead`로, 해당 비밀번호를 `secret`으로 설정합니다. Neo4j 브라우저에 접근하려면 웹 브라우저에서 `http://homestead.test:7474`를 방문하십시오. `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS) 포트는 Neo4j 클라이언트의 요청을 처리할 준비가 되어 있습니다.

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory: -->
Homestead 디렉터리 안의 `aliases` 파일을 수정하여 Homestead 가상 머신에 Bash 별칭을 추가할 수 있습니다.

```shell
alias c='clear'
alias ..='cd ..'
```

<!-- After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine. -->
`aliases` 파일을 업데이트한 후에는 `vagrant reload --provision` 명령어를 사용해 Homestead 가상 머신을 다시 프로비저닝해야 합니다. 이렇게 하면 새 별칭을 머신에서 사용할 수 있습니다.

<a name="updating-homestead"></a>
<!-- ## Updating Homestead -->
## Updating Homestead

<!-- Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory: -->
Homestead 업데이트를 시작하기 전에 Homestead 디렉터리에서 다음 명령어를 실행하여 현재 가상 머신을 제거했는지 확인해야 합니다.

```shell
vagrant destroy
```
<!-- Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository: -->
다음으로 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면, 처음 저장소를 클론한 위치에서 다음 명령어를 실행할 수 있습니다.

```shell
git fetch

git pull origin release
```

<!-- These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases). -->
이 명령어들은 GitHub 저장소에서 최신 Homestead 코드를 가져오고, 최신 태그를 가져온 뒤, 가장 최근 태그가 붙은 릴리스를 체크아웃합니다. 최신 안정 릴리스 버전은 Homestead의 [GitHub releases page](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

<!-- If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies: -->
프로젝트의 `composer.json` 파일을 통해 Homestead를 설치했다면, `composer.json` 파일에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 의존성을 업데이트해야 합니다.

```shell
composer update
```

<!-- Next, you should update the Vagrant box using the `vagrant box update` command: -->
다음으로 `vagrant box update` 명령어를 사용해 Vagrant box를 업데이트해야 합니다.

```shell
vagrant box update
```

<!-- After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files: -->
Vagrant box를 업데이트한 뒤에는 Homestead의 추가 설정 파일을 업데이트하기 위해 Homestead 디렉터리에서 `bash init.sh` 명령어를 실행해야 합니다. 기존 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 묻는 메시지가 표시됩니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<!-- Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation: -->
마지막으로 최신 Vagrant 설치를 사용하려면 Homestead 가상 머신을 다시 생성해야 합니다.

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
Homestead 디렉터리에서 `vagrant ssh` 터미널 명령어를 실행하면 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
<!-- ### Adding Additional Sites -->
### Adding Additional Sites

<!-- Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file. -->
Homestead 환경이 프로비저닝되어 실행 중이라면 다른 Laravel 프로젝트를 위해 Nginx 사이트를 추가하고 싶을 수 있습니다. 하나의 Homestead 환경에서 원하는 만큼 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트를 등록하려면 `Homestead.yaml` 파일에 사이트를 추가하십시오.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> <!-- You should ensure that you have configured a [folder mapping](#configuring-shared-folders) for the project's directory before adding the site. -->
> 사이트를 추가하기 전에 프로젝트 디렉터리에 대한 [folder mapping](#configuring-shared-folders)을 설정했는지 확인해야 합니다.

<!-- If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`: -->
Vagrant가 "hosts" 파일을 자동으로 관리하지 않는다면, 새 사이트를 해당 파일에도 추가해야 할 수 있습니다. macOS와 Linux에서는 이 파일이 `/etc/hosts`에 있습니다. Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다.

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

<!-- Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory. -->
사이트를 추가한 뒤 Homestead 디렉터리에서 `vagrant reload --provision` 터미널 명령어를 실행하십시오.

<a name="site-types"></a>
<!-- #### Site Types -->
#### Site Types

<!-- Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type: -->
Homestead는 Laravel 기반이 아닌 프로젝트를 쉽게 실행할 수 있도록 여러 사이트 "타입"을 지원합니다. 예를 들어 `statamic` 사이트 타입을 사용하면 Statamic 애플리케이션을 Homestead에 쉽게 추가할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

<!-- The available site types are: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (the default), `proxy` (for nginx), `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`. -->
사용할 수 있는 사이트 타입은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`입니다.

<a name="site-parameters"></a>
<!-- #### Site Parameters -->
#### Site Parameters

<!-- You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive: -->
`params` 사이트 지시어를 사용해 사이트에 Nginx `fastcgi_param` 값을 추가할 수 있습니다.

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
`Homestead.yaml` 파일에 환경 변수를 추가해 전역 환경 변수를 정의할 수 있습니다.

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

<!-- After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user. -->
`Homestead.yaml` 파일을 업데이트한 뒤에는 반드시 `vagrant reload --provision` 명령어를 실행해 머신을 다시 프로비저닝하십시오. 그러면 설치된 모든 PHP 버전의 PHP-FPM 설정이 업데이트되고 `vagrant` 사용자의 환경도 업데이트됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- By default, the following ports are forwarded to your Homestead environment: -->
기본적으로 다음 포트가 Homestead 환경으로 포워딩됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
-->
- **HTTP:** 8000 &rarr; 80으로 전달
- **HTTPS:** 44300 &rarr; 443으로 전달

<!-- </div> -->
</div>

<a name="forwarding-additional-ports"></a>
<!-- #### Forwarding Additional Ports -->
#### Forwarding Additional Ports

<!-- If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command: -->
필요하다면 `Homestead.yaml` 파일 안에 `ports` 설정 항목을 정의해 추가 포트를 Vagrant box로 포워딩할 수 있습니다. `Homestead.yaml` 파일을 업데이트한 뒤에는 반드시 `vagrant reload --provision` 명령어를 실행해 머신을 다시 프로비저닝하십시오.

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

<!-- Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box: -->
다음은 호스트 머신에서 Vagrant box로 매핑할 수 있는 추가 Homestead 서비스 포트 목록입니다.

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
- **SSH:** 2222 &rarr; 22로
- **ngrok UI:** 4040 &rarr; 4040으로
- **MySQL:** 33060 &rarr; 3306으로
- **PostgreSQL:** 54320 &rarr; 5432로
- **MongoDB:** 27017 &rarr; 27017로
- **Mailpit:** 8025 &rarr; 8025로
- **Minio:** 9600 &rarr; 9600으로

<!-- </div> -->
</div>

<a name="php-versions"></a>
<!-- ### PHP Versions -->
### PHP Versions

<!-- Homestead supports running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", and "8.3", (the default): -->
Homestead는 같은 가상 머신에서 여러 PHP 버전을 실행할 수 있습니다. `Homestead.yaml` 파일에서 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. 사용할 수 있는 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3"(기본값)입니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

<!-- [Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI: -->
[Within your Homestead virtual machine](#connecting-via-ssh) CLI를 통해 지원되는 PHP 버전 중 아무 버전이나 사용할 수 있습니다.

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
Homestead 가상 머신 안에서 다음 명령어를 실행해 CLI가 사용하는 기본 PHP 버전을 변경할 수 있습니다.

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
MySQL과 PostgreSQL 모두 기본적으로 `homestead` 데이터베이스가 설정되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL 데이터베이스에 연결하려면 `127.0.0.1`의 `33060`(MySQL) 또는 `54320`(PostgreSQL) 포트로 연결해야 합니다. 두 데이터베이스의 사용자 이름과 비밀번호는 `homestead` / `secret`입니다.

> [!WARNING]
> <!-- You should only use these non-standard ports when connecting to the databases from your host machine. You will use the default 3306 and 5432 ports in your Laravel application's `database` configuration file since Laravel is running _within_ the virtual machine. -->
> 이 비표준 포트는 호스트 머신에서 데이터베이스에 연결할 때만 사용해야 합니다. Laravel은 가상 머신 _안에서_ 실행되므로 Laravel 애플리케이션의 `database` 설정 파일에서는 기본 포트인 3306과 5432를 사용합니다.

<a name="database-backups"></a>
<!-- ### Database Backups -->
### Database Backups

<!-- Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file: -->
Homestead는 Homestead 가상 머신이 삭제될 때 데이터베이스를 자동으로 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상을 사용해야 합니다. 또는 더 오래된 Vagrant 버전을 사용한다면 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 데이터베이스 백업을 활성화하려면 `Homestead.yaml` 파일에 다음 줄을 추가하십시오.

```yaml
backup: true
```

<!-- Once configured, Homestead will export your databases to `.backup/mysql_backup` and `.backup/postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method. -->
설정을 마치면 `vagrant destroy` 명령어가 실행될 때 Homestead가 데이터베이스를 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉터리로 내보냅니다. 이 디렉터리는 Homestead를 설치한 폴더에 있으며, [per project installation](#per-project-installation) 방식을 사용한다면 프로젝트 루트에 있습니다.

<a name="configuring-cron-schedules"></a>
<!-- ### Configuring Cron Schedules -->
### Configuring Cron Schedules

<!-- Laravel provides a convenient way to [schedule cron jobs](/docs/master/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `routes/console.php` file to determine which scheduled tasks to run. -->
Laravel은 단일 `schedule:run` Artisan 명령어를 매분 실행하도록 예약하는 방식으로 [schedule cron jobs](/docs/master/scheduling)하는 편리한 방법을 제공합니다. `schedule:run` 명령어는 `routes/console.php` 파일에 정의된 잡 스케줄을 확인해 실행할 예약 작업을 결정합니다.

<!-- If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site: -->
Homestead 사이트에서 `schedule:run` 명령어를 실행하고 싶다면, 사이트를 정의할 때 `schedule` 옵션을 `true`로 설정할 수 있습니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

<!-- The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine. -->
해당 사이트의 cron 잡은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailpit"></a>
<!-- ### Configuring Mailpit -->
### Configuring Mailpit

<!-- [Mailpit](https://github.com/axllent/mailpit) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings: -->
[Mailpit](https://github.com/axllent/mailpit)을 사용하면 발신 이메일을 실제 수신자에게 보내지 않고 가로채서 확인할 수 있습니다. 시작하려면 애플리케이션의 `.env` 파일을 업데이트해 다음 메일 설정을 사용하십시오.

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

<!-- Once Mailpit has been configured, you may access the Mailpit dashboard at `http://localhost:8025`. -->
Mailpit 설정을 마치면 `http://localhost:8025`에서 Mailpit 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
<!-- ### Configuring Minio -->
### Configuring Minio

<!-- [Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section: -->
[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 `Homestead.yaml` 파일의 [features](#installing-optional-features) 섹션에 다음 설정 옵션을 추가하십시오.

```
minio: true
```

<!-- By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`. -->
기본적으로 Minio는 9600 포트에서 사용할 수 있습니다. `http://localhost:9600`에 접속해 Minio 제어판에 접근할 수 있습니다. 기본 액세스 키는 `homestead`이고, 기본 시크릿 키는 `secretkey`입니다. Minio에 접근할 때는 항상 `us-east-1` 리전을 사용해야 합니다.

<!-- In order to use Minio, ensure your `.env` file has the following options: -->
Minio를 사용하려면 `.env` 파일에 다음 옵션이 있는지 확인하십시오.

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

<!-- To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal: -->
Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml` 파일에 `buckets` 지시어를 추가하십시오. 버킷을 정의한 뒤에는 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

<!-- Supported `policy` values include: `none`, `download`, `upload`, and `public`. -->
지원되는 `policy` 값에는 `none`, `download`, `upload`, `public`이 있습니다.

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- In order to run [Laravel Dusk](/docs/master/dusk) tests within Homestead, you should enable the [webdriver feature](#installing-optional-features) in your Homestead configuration: -->
Homestead 안에서 [Laravel Dusk](/docs/master/dusk) 테스트를 실행하려면 Homestead 설정에서 [webdriver feature](#installing-optional-features)을 활성화해야 합니다.

```yaml
features:
    - webdriver: true
```

<!-- After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal. -->
`webdriver` 기능을 활성화한 뒤에는 터미널에서 `vagrant reload --provision` 명령어를 실행해야 합니다.

<a name="sharing-your-environment"></a>
<!-- ### Sharing Your Environment -->
### Sharing Your Environment

<!-- Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file. -->
때로는 현재 작업 중인 내용을 동료나 클라이언트와 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령어로 이를 기본 지원합니다. 하지만 `Homestead.yaml` 파일에 여러 사이트가 설정되어 있다면 이 방식은 동작하지 않습니다.

<!-- To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`: -->
이 문제를 해결하기 위해 Homestead는 자체 `share` 명령어를 제공합니다. 시작하려면 `vagrant ssh`로 [SSH into your Homestead virtual machine](#connecting-via-ssh)한 뒤 `share homestead.test` 명령어를 실행하십시오. 이 명령어는 `Homestead.yaml` 설정 파일의 `homestead.test` 사이트를 공유합니다. `homestead.test` 대신 설정된 다른 사이트를 사용할 수도 있습니다.

```shell
share homestead.test
```

<!-- After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command: -->
명령어를 실행하면 활동 로그와 공유 사이트의 공개 접근 URL이 포함된 Ngrok 화면이 나타납니다. 사용자 지정 리전, 서브도메인 또는 다른 Ngrok 런타임 옵션을 지정하려면 `share` 명령어에 해당 옵션을 추가할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

<!-- If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so. -->
HTTP가 아니라 HTTPS로 콘텐츠를 공유해야 한다면 `share` 대신 `sshare` 명령어를 사용하면 됩니다.

> [!WARNING]
> <!-- Remember, Vagrant is inherently insecure and you are exposing your virtual machine to the Internet when running the `share` command. -->
> Vagrant는 본질적으로 안전하지 않으며, `share` 명령어를 실행하면 가상 머신을 인터넷에 노출하게 된다는 점을 기억하십시오.

<a name="debugging-and-profiling"></a>
<!-- ## Debugging and Profiling -->
## Debugging and Profiling

<a name="debugging-web-requests"></a>
<!-- ### Debugging Web Requests With Xdebug -->
### Debugging Web Requests With Xdebug

<!-- Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code. -->
Homestead는 [Xdebug](https://xdebug.org)를 사용한 단계별 디버깅을 지원합니다. 예를 들어 브라우저에서 페이지에 접근하면 PHP가 IDE에 연결되어 실행 중인 코드를 검사하고 수정할 수 있습니다.

<!-- By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/). -->
기본적으로 Xdebug는 이미 실행 중이며 연결을 받을 준비가 되어 있습니다. CLI에서 Xdebug를 활성화해야 한다면 Homestead 가상 머신 안에서 `sudo phpenmod xdebug` 명령어를 실행하십시오. 다음으로 IDE의 안내에 따라 디버깅을 활성화합니다. 마지막으로 확장 프로그램이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)으로 Xdebug를 트리거하도록 브라우저를 설정하십시오.

> [!WARNING]
> <!-- Xdebug causes PHP to run significantly slower. To disable Xdebug, run `sudo phpdismod xdebug` within your Homestead virtual machine and restart the FPM service. -->
> Xdebug는 PHP 실행 속도를 크게 늦춥니다. Xdebug를 비활성화하려면 Homestead 가상 머신 안에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 다시 시작하십시오.

<a name="autostarting-xdebug"></a>
<!-- #### Autostarting Xdebug -->
#### Autostarting Xdebug

<!-- When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration: -->
웹 서버로 요청을 보내는 기능 테스트를 디버깅할 때는 디버깅을 트리거하기 위해 테스트를 수정해 사용자 지정 헤더나 쿠키를 전달하는 것보다 디버깅을 자동으로 시작하는 편이 더 쉽습니다. Xdebug가 자동으로 시작되도록 강제하려면 Homestead 가상 머신 안의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하고 다음 설정을 추가하십시오.

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
PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 안에서 `xphp` 셸 alias를 사용하십시오.

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
<!-- ### Profiling Applications With Blackfire -->
### Profiling Applications With Blackfire

<!-- [Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings. -->
[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션을 프로파일링하는 서비스입니다. 프로파일 데이터를 호출 그래프와 타임라인으로 보여 주는 대화형 사용자 인터페이스를 제공합니다. 개발, 스테이징, 프로덕션 환경에서 사용할 수 있도록 만들어졌으며, 최종 사용자에게는 오버헤드가 없습니다. 또한 Blackfire는 코드와 `php.ini` 설정에 대한 성능, 품질, 보안 검사를 제공합니다.

<!-- The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios. -->
[Blackfire Player](https://blackfire.io/docs/player/index)는 프로파일링 시나리오를 스크립트로 작성하기 위해 Blackfire와 함께 사용할 수 있는 오픈 소스 웹 크롤링, 웹 테스트, 웹 스크래핑 애플리케이션입니다.

<!-- To enable Blackfire, use the "features" setting in your Homestead configuration file: -->
Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 설정을 사용하십시오.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

<!-- Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index). -->
Blackfire 서버 자격 증명과 클라이언트 자격 증명에는 [require a Blackfire account](https://blackfire.io/signup). Blackfire는 CLI 도구와 브라우저 확장을 포함해 애플리케이션을 프로파일링하는 여러 옵션을 제공합니다. 자세한 내용은 [review the Blackfire documentation for more details](https://blackfire.io/docs/php/integrations/laravel/index).

<a name="network-interfaces"></a>
<!-- ## Network Interfaces -->
## Network Interfaces

<!-- The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary: -->
`Homestead.yaml` 파일의 `networks` 프로퍼티는 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 인터페이스를 설정할 수 있습니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

<!-- To enable a [bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) interface, configure a `bridge` setting for the network and change the network type to `public_network`: -->
[bridged](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면 네트워크에 `bridge` 설정을 구성하고 네트워크 타입을 `public_network`로 변경하십시오.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To enable [DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp), just remove the `ip` option from your configuration: -->
[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 설정에서 `ip` 옵션만 제거하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To update what device the network is using, you may add a `dev` option to the network's configuration. The default `dev` value is `eth0`: -->
네트워크가 사용할 장치를 변경하려면 네트워크 설정에 `dev` 옵션을 추가할 수 있습니다. 기본 `dev` 값은 `eth0`입니다.

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
Homestead 디렉터리 루트에 있는 `after.sh` 스크립트를 사용해 Homestead를 확장할 수 있습니다. 이 파일 안에는 가상 머신을 올바르게 설정하고 커스터마이징하는 데 필요한 shell 명령어를 추가할 수 있습니다.

<!-- When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead: -->
Homestead를 커스터마이징할 때 Ubuntu가 패키지의 기존 설정을 유지할지, 새 설정 파일로 덮어쓸지 물을 수 있습니다. 이를 피하려면 패키지를 설치할 때 다음 명령어를 사용해 Homestead가 이전에 작성한 설정이 덮어써지지 않도록 해야 합니다.

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
팀과 함께 Homestead를 사용할 때 개인 개발 스타일에 더 잘 맞도록 Homestead를 조정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리 루트(`Homestead.yaml` 파일이 있는 같은 디렉터리)에 `user-customizations.sh` 파일을 만들 수 있습니다. 이 파일 안에서는 원하는 커스터마이징을 자유롭게 할 수 있습니다. 다만 `user-customizations.sh`는 버전 관리에 포함하면 안 됩니다.

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
기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이렇게 하면 Homestead가 호스트 운영체제의 DNS 설정을 사용할 수 있습니다. 이 동작을 재정의하려면 `Homestead.yaml` 파일에 다음 설정 옵션을 추가합니다.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```
