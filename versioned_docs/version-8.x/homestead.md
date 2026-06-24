<!-- # Laravel Homestead -->
# Laravel Homestead

- [Introduction](#introduction)
- [Installation & Setup](#installation-and-setup)
    - [First Steps](#first-steps)
    - [Configuring Homestead](#configuring-homestead)
    - [Configuring Nginx Sites](#configuring-nginx-sites)
    - [Configuring Services](#configuring-services)
    - [Launching The Vagrant Box](#launching-the-vagrant-box)
    - [Per Project Installation](#per-project-installation)
    - [Installing Optional Features](#installing-optional-features)
    - [Aliases](#aliases)
- [Updating Homestead](#updating-homestead)
- [Daily Usage](#daily-usage)
    - [Connecting Via SSH](#connecting-via-ssh)
    - [Adding Additional Sites](#adding-additional-sites)
    - [Environment Variables](#environment-variables)
    - [Ports](#ports)
    - [PHP Versions](#php-versions)
    - [Connecting To Databases](#connecting-to-databases)
    - [Database Backups](#database-backups)
    - [Configuring Cron Schedules](#configuring-cron-schedules)
    - [Configuring MailHog](#configuring-mailhog)
    - [Configuring Minio](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [Sharing Your Environment](#sharing-your-environment)
- [Debugging & Profiling](#debugging-and-profiling)
    - [Debugging Web Requests With Xdebug](#debugging-web-requests)
    - [Debugging CLI Applications](#debugging-cli-applications)
    - [Profiling Applications with Blackfire](#profiling-applications-with-blackfire)
- [Network Interfaces](#network-interfaces)
- [Extending Homestead](#extending-homestead)
- [Provider Specific Settings](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, and any other server software on your local machine. -->
Laravel은 개발자가 더욱 즐겁게 PHP 개발을 할 수 있도록, 로컬 개발 환경까지 포함하여 전체 개발 경험을 향상시키는 것을 목표로 합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 PHP, 웹 서버, 기타 서버 관련 소프트웨어들을 별도로 설치하지 않아도 바로 사용할 수 있는, 공식적으로 제공되는 사전 구성된 Vagrant 박스입니다. 이로써 여러분은 훌륭한 개발 환경을 간단하게 구축할 수 있습니다.

<!-- [Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes! -->
[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝하는 매우 간단하고 우아한 방법을 제공합니다. Vagrant 박스는 언제든지 손쉽게 삭제할 수 있어, 문제가 생기더라도 몇 분만에 새로운 박스를 다시 만들 수 있습니다.

<!-- Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications. -->
Homestead는 Windows, macOS, Linux 등 모든 운영체제에서 동작하며, Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 Laravel 개발에 필요한 대부분의 소프트웨어가 포함되어 있습니다.

> [!NOTE]
> Windows를 사용하는 경우, 하드웨어 가상화(VT-x) 기능을 BIOS에서 활성화해야 할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용 중이라면, VT-x 사용을 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
<!-- ### Included Software -->
### Included Software

<!-- <div id="software-list" markdown="1"> -->
<div id="software-list" markdown="1">

<!--
- Ubuntu 20.04
- Git
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
- PostgreSQL 13
- Composer
- Node (With Yarn, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailhog
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli
-->
- Ubuntu 20.04
- Git
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
- PostgreSQL 13
- Composer
- Node (Yarn, Bower, Grunt, Gulp 포함)
- Redis
- Memcached
- Beanstalkd
- Mailhog
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
- Docker
- Elasticsearch
- EventStoreDB
- Gearman
- Go
- Grafana
- InfluxDB
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
- Docker
- Elasticsearch
- EventStoreDB
- Gearman
- Go
- Grafana
- InfluxDB
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
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP 확장)</small>
- Webdriver & Laravel Dusk 유틸리티

<!-- </div> -->
</div>

<a name="installation-and-setup"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- Before launching your Homestead environment, you must install [Vagrant](https://www.vagrantup.com/downloads.html) as well as one of the following supported providers: -->
Homestead 환경을 실행하기 전에 [Vagrant](https://www.vagrantup.com/downloads.html)와 아래 지원되는 프로바이더 중 하나를 반드시 설치해야 합니다.

<!--
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)
-->
- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Downloads)
- [Parallels](https://www.parallels.com/products/desktop/)

<!-- All of these software packages provide easy-to-use visual installers for all popular operating systems. -->
위 소프트웨어들은 주요 운영체제에서 사용할 수 있는 간편한 설치 프로그램을 제공합니다.

<!-- To use the Parallels provider, you will need to install [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels). It is free of charge. -->
Parallels 프로바이더를 사용하려면 [Parallels Vagrant plug-in](https://github.com/Parallels/vagrant-parallels)을 별도로 설치해야 하며, 해당 플러그인은 무료입니다.

<a name="installing-homestead"></a>
<!-- #### Installing Homestead -->
#### Installing Homestead

<!-- You may install Homestead by cloning the Homestead repository onto your host machine. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead virtual machine will serve as the host to all of your Laravel applications. Throughout this documentation, we will refer to this directory as your "Homestead directory": -->
Homestead를 설치하려면, Homestead 저장소를 호스트 머신(내 컴퓨터)에 클론해 주세요. Homestead 박스는 여러 Laravel 애플리케이션의 호스트 역할을 하므로, 홈 디렉터리 내에 `Homestead` 폴더를 만들고 여기에 클론하는 것을 추천합니다. 이 문서에서는 해당 폴더를 "Homestead 디렉터리"라고 부릅니다.

```bash
git clone https://github.com/laravel/homestead.git ~/Homestead
```

<!-- After cloning the Laravel Homestead repository, you should checkout the `release` branch. This branch always contains the latest stable release of Homestead: -->
저장소를 클론한 후, 항상 최신 안정 버전이 존재하는 `release` 브랜치를 체크아웃해야 합니다.


```
cd ~/Homestead

git checkout release
```


<!-- Next, execute the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file. The `Homestead.yaml` file is where you will configure all of the settings for your Homestead installation. This file will be placed in the Homestead directory: -->
이제 Homestead 디렉터리에서 `bash init.sh` 명령을 실행하면, Homestead 설정을 위한 `Homestead.yaml` 파일이 생성됩니다. `Homestead.yaml` 파일에서 Homestead의 모든 설정을 구성할 수 있으며, 생성된 파일은 Homestead 디렉터리에 위치하게 됩니다.


```
// macOS / Linux...
bash init.sh

// Windows...
init.bat
```


<a name="configuring-homestead"></a>
<!-- ### Configuring Homestead -->
### Configuring Homestead

<a name="setting-your-provider"></a>
<!-- #### Setting Your Provider -->
#### Setting Your Provider

<!-- The `provider` key in your `Homestead.yaml` file indicates which Vagrant provider should be used: `virtualbox` or `parallels`: -->
`Homestead.yaml` 파일의 `provider` 항목은 사용할 Vagrant 프로바이더를 지정합니다. 예를 들어 `virtualbox` 또는 `parallels` 중 하나를 설정할 수 있습니다.


```
provider: virtualbox
```


> [!NOTE]
> Apple Silicon(M1, M2 등)을 사용하는 경우, `Homestead.yaml` 파일에 `box: laravel/homestead-arm`을 추가해야 하며, 반드시 Parallels 프로바이더를 사용해야 합니다.

<a name="configuring-shared-folders"></a>
<!-- #### Configuring Shared Folders -->
#### Configuring Shared Folders

<!-- The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead virtual environment. You may configure as many shared folders as necessary: -->
`Homestead.yaml`의 `folders` 항목에서는 Homestead 환경과 공유할 폴더를 지정합니다. 이 목록에 포함된 폴더들은 변경 시, 로컬 환경과 가상 머신 환경 간에 자동으로 동기화됩니다. 여러 폴더를 자유롭게 공유 설정할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!NOTE]
> Windows 사용자는 `~/` 형태 대신 전체 경로를 사용해야 합니다. 예: `C:\Users\user\Code\project1`

<!-- You should always map individual applications to their own folder mapping instead of mapping a single large directory that contains all of your applications. When you map a folder, the virtual machine must keep track of all disk IO for *every* file in the folder. You may experience reduced performance if you have a large number of files in a folder: -->
여러 애플리케이션을 한 폴더에 몰아서 매핑하기보다, 각 애플리케이션마다 별도의 폴더 매핑을 사용하는 것이 좋습니다. 매핑한 폴더의 파일 개수가 많을수록 디스크 IO 부하 때문에 성능이 저하될 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!NOTE]
> Homestead를 사용할 때에는 `.`(현재 디렉터리)를 절대로 마운트하지 마십시오. 이 경우 Vagrant가 현재 폴더를 `/vagrant`로 매핑하지 않으므로, 다양한 옵션 기능이 정상 동작하지 않을 수 있습니다.

<!-- To enable [NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html), you may add a `type` option to your folder mapping: -->
[NFS](https://www.vagrantup.com/docs/synced-folders/nfs.html) 방식을 사용하려면, 폴더 매핑에 `type` 옵션을 추가하면 됩니다.


```
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```


> [!NOTE]
> Windows 환경에서 NFS를 사용하려면 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것을 권장합니다. 이 플러그인은 Homestead 가상머신 안의 파일 및 디렉터리 권한을 적절히 유지시켜줍니다.

<!-- You may also pass any options supported by Vagrant's [Synced Folders](https://www.vagrantup.com/docs/synced-folders/basic_usage.html) by listing them under the `options` key: -->
또한 Vagrant의 [Synced Folders](https://www.vagrantup.com/docs/synced-folders/basic_usage.html)에서 지원하는 옵션들도 `options` 항목 아래에 추가해서 사용할 수 있습니다.


```
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
Nginx가 낯설어도 걱정하지 마십시오. `Homestead.yaml` 파일에서 `sites` 항목을 활용하면, 원하는 "도메인"을 Homestead 환경 내의 특정 폴더에 쉽게 매핑할 수 있습니다. `Homestead.yaml` 파일에는 예제 사이트 설정이 기본 포함되어 있으며, 여러 사이트를 자유롭게 추가할 수 있습니다. 이처럼 Homestead는 여러분이 작업하는 모든 Laravel 애플리케이션의 가상 실행 환경이 될 수 있습니다.


```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```


<!-- If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine. -->
만약 Homestead 가상머신을 프로비저닝(세팅)한 후에 `sites` 항목을 변경했다면, Nginx 설정을 적용하려면 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!NOTE]
> Homestead의 프로비저닝 스크립트는 가능하면 항상 동일한 결과가 나오도록(idempotent) 설계되어 있습니다. 하지만 프로비저닝 중 오류가 발생한다면, `vagrant destroy && vagrant up`으로 가상머신을 삭제 후 재생성하는 것이 가장 확실한 방법입니다.

<a name="hostname-resolution"></a>
<!-- #### Hostname Resolution -->
#### Hostname Resolution

<!-- Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US). -->
Homestead는 `mDNS`를 사용해 호스트네임을 자동으로 등록합니다. 예를 들어, `Homestead.yaml` 파일에 `hostname: homestead`를 지정하면, `homestead.local`로 접속이 가능합니다. macOS, iOS, 대부분의 리눅스 데스크탑은 기본적으로 `mDNS`를 지원하지만, Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 별도 설치해야 합니다.

<!-- Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following: -->
자동 호스트네임 기능은 [per project installations](#per-project-installation) 방식에서 특히 잘 동작합니다. 한 Homestead 인스턴스에 여러 사이트를 호스팅하는 경우, 각 웹사이트의 "도메인"을 자신의 `hosts` 파일에 직접 추가해주면 됩니다. 이 `hosts` 파일은 Homestead 사이트로 향하는 요청을 Homestead 가상머신으로 리다이렉트해 줍니다. 이 파일은 macOS, Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 경로에 위치합니다. 다음과 같이 추가합니다.

```
192.168.56.56  homestead.test
```

<!-- Make sure the IP address listed is the one set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file and launched the Vagrant box you will be able to access the site via your web browser: -->
위에 나열한 IP 주소가 `Homestead.yaml` 파일에 설정한 값과 일치하는지 확인하세요. 도메인을 `hosts` 파일에 추가하고 Vagrant 박스를 실행하면 이제 브라우저에서 해당 사이트로 접근할 수 있습니다.

```bash
http://homestead.test
```

<a name="configuring-services"></a>
<!-- ### Configuring Services -->
### Configuring Services

<!-- Homestead starts several services by default; however, you may customize which services are enabled or disabled during provisioning. For example, you may enable PostgreSQL and disable MySQL by modifying the `services` option within your `Homestead.yaml` file: -->
Homestead는 기본적으로 여러 서비스들을 자동으로 실행합니다. 하지만, 프로비저닝 시 어떤 서비스를 활성화하거나 비활성화할지는 자유롭게 지정할 수 있습니다. 예를 들어 PostgreSQL만 활성화하고 MySQL은 비활성화하고 싶다면 아래와 같이 `Homestead.yaml` 파일의 `services` 옵션을 수정하면 됩니다.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

<!-- The specified services will be started or stopped based on their order in the `enabled` and `disabled` directives. -->
`enabled`, `disabled` 하위에 나열된 항목 순서와 관계없이, 해당 서비스가 실행 또는 중단됩니다.

<a name="launching-the-vagrant-box"></a>
<!-- ### Launching The Vagrant Box -->
### Launching The Vagrant Box

<!-- Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory. Vagrant will boot the virtual machine and automatically configure your shared folders and Nginx sites. -->
`Homestead.yaml` 파일의 설정을 마쳤다면, Homestead 디렉터리에서 `vagrant up` 명령을 실행하면 됩니다. Vagrant가 가상머신을 부팅하고 자동으로 공유 폴더와 Nginx 사이트 설정도 함께 완료합니다.

<!-- To destroy the machine, you may use the `vagrant destroy` command. -->
가상머신을 삭제하려면 `vagrant destroy` 명령을 사용할 수 있습니다.

<a name="per-project-installation"></a>
<!-- ### Per Project Installation -->
### Per Project Installation

<!-- Instead of installing Homestead globally and sharing the same Homestead virtual machine across all of your projects, you may instead configure a Homestead instance for each project you manage. Installing Homestead per project may be beneficial if you wish to ship a `Vagrantfile` with your project, allowing others working on the project to `vagrant up` immediately after cloning the project's repository. -->
Homestead를 전역(global)으로 설치해서 모든 프로젝트에서 하나의 Homestead 인스턴스를 공유할 수도 있지만, 각 프로젝트별로 Homestead 인스턴스를 따로 사용할 수도 있습니다. 프로젝트 단위로 Homestead를 설치하면, `Vagrantfile`을 프로젝트에 함께 제공할 수 있으므로, 다른 협업자가 프로젝트 저장소를 클론(clone) 받은 뒤 즉시 `vagrant up`으로 동일한 개발 환경을 구축할 수 있습니다.

<!-- You may install Homestead into your project using the Composer package manager: -->
Composer 패키지 매니저로 프로젝트에 Homestead를 추가할 수 있습니다.

```bash
composer require laravel/homestead --dev
```

<!-- Once Homestead has been installed, invoke Homestead's `make` command to generate the `Vagrantfile` and `Homestead.yaml` file for your project. These files will be placed in the root of your project. The `make` command will automatically configure the `sites` and `folders` directives in the `Homestead.yaml` file: -->
설치가 끝나면, Homestead의 `make` 명령어로 프로젝트 전용 `Vagrantfile`과 `Homestead.yaml` 파일을 생성합니다. 두 파일 모두 프로젝트 루트에 생성되며, `make` 명령이 `Homestead.yaml`에서 `sites`와 `folders` 항목도 자동으로 설정해줍니다.


```
// macOS / Linux...
php vendor/bin/homestead make

// Windows...
vendor\\bin\\homestead make
```


<!-- Next, run the `vagrant up` command in your terminal and access your project at `http://homestead.test` in your browser. Remember, you will still need to add an `/etc/hosts` file entry for `homestead.test` or the domain of your choice if you are not using automatic [hostname resolution](#hostname-resolution). -->
이제 터미널에서 `vagrant up`을 실행하고, 브라우저에서 `http://homestead.test`로 프로젝트에 접근하면 됩니다. 자동 [hostname resolution](#hostname-resolution) 기능을 사용하지 않는다면, `homestead.test` 혹은 원하는 도메인을 반드시 `/etc/hosts` 파일에 등록해야 정상적으로 접속 가능합니다.

<a name="installing-optional-features"></a>
<!-- ### Installing Optional Features -->
### Installing Optional Features

<!-- Optional software is installed using the `features` option within your `Homestead.yaml` file. Most features can be enabled or disabled with a boolean value, while some features allow multiple configuration options: -->
옵션 소프트웨어는 `Homestead.yaml` 파일의 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 true/false 값으로 활성화 또는 비활성화를 결정하며, 일부 기능은 추가 구성 옵션이 필요합니다.


<!--
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
        - docker: true
        - elasticsearch:
            version: 7.9.0
        - eventstore: true
            version: 21.2.0
        - gearman: true
        - golang: true
        - grafana: true
        - influxdb: true
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
        - rvm: true
        - solr: true
        - timescaledb: true
        - trader: true
        - webdriver: true
-->
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
        - docker: true
        - elasticsearch:
            version: 7.9.0
        - eventstore: true
            version: 21.2.0
        - gearman: true
        - golang: true
        - grafana: true
        - influxdb: true
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
        - rvm: true
        - solr: true
        - timescaledb: true
        - trader: true
        - webdriver: true


<a name="elasticsearch"></a>
<!-- #### Elasticsearch -->
#### Elasticsearch

<!-- You may specify a supported version of Elasticsearch, which must be an exact version number (major.minor.patch). The default installation will create a cluster named 'homestead'. You should never give Elasticsearch more than half of the operating system's memory, so make sure your Homestead virtual machine has at least twice the Elasticsearch allocation. -->
지원되는 Elasticsearch 버전을 정확하게 지정하여 설치할 수 있습니다(예: major.minor.patch 형식). 기본적으로 'homestead'라는 이름의 클러스터가 생성됩니다. Elasticsearch는 OS 메모리의 절반 이상을 할당하면 안 되므로, Homestead 가상머신 메모리는 Elasticsearch에서 필요한 용량의 두 배 이상이 필요합니다.

> [!TIP]
> [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current)에서 상세한 설정 방법을 확인할 수 있습니다.

<a name="mariadb"></a>
<!-- #### MariaDB -->
#### MariaDB

<!-- Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration. -->
MariaDB 활성화 시 MySQL을 제거하고 MariaDB를 설치합니다. MariaDB는 대체로 MySQL과 호환되므로, 애플리케이션의 데이터베이스 설정에서는 그대로 `mysql` 드라이버를 사용하면 됩니다.

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`. -->
기본 MongoDB 설치의 데이터베이스 사용자명은 `homestead`, 비밀번호는 `secret`으로 설정됩니다.

<a name="neo4j"></a>
<!-- #### Neo4j -->
#### Neo4j

<!-- The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client. -->
Neo4j도 기본적으로 사용자명 `homestead`, 비밀번호 `secret`으로 구성됩니다. Neo4j 브라우저를 사용하려면 브라우저에서 `http://homestead.test:7474`로 접속하면 됩니다. 포트 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)가 Neo4j 클라이언트의 요청을 처리할 준비가 되어 있습니다.

<a name="aliases"></a>
<!-- ### Aliases -->
### Aliases

<!-- You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory: -->
Homestead 가상머신에서 bash 별칭을 추가하려면, Homestead 디렉터리의 `aliases` 파일을 수정하면 됩니다.

```
alias c='clear'
alias ..='cd ..'
```

<!-- After you have updated the `aliases` file, you should re-provision the Homestead virtual machine using the `vagrant reload --provision` command. This will ensure that your new aliases are available on the machine. -->
`aliases` 파일을 수정한 후, 반드시 `vagrant reload --provision` 명령으로 가상머신을 다시 프로비저닝해주어야 별칭이 적용됩니다.

<a name="updating-homestead"></a>
<!-- ## Updating Homestead -->
## Updating Homestead

<!-- Before you begin updating Homestead you should ensure you have removed your current virtual machine by running the following command in your Homestead directory: -->
Homestead를 업데이트하기 전에는, 먼저 현재 사용 중인 가상머신을 반드시 종료 및 삭제해야 합니다. Homestead 디렉터리에서 아래 명령어를 실행하여 삭제합니다.


<!--     vagrant destroy -->
    vagrant destroy


<!-- Next, you need to update the Homestead source code. If you cloned the repository, you can execute the following commands at the location you originally cloned the repository: -->
다음으로 Homestead 소스코드를 업데이트합니다. 저장소를 클론해서 설치했다면, 저장소를 클론했던 위치에서 아래 명령어를 차례로 실행하세요.


```
git fetch

git pull origin release
```


<!-- These commands pull the latest Homestead code from the GitHub repository, fetch the latest tags, and then check out the latest tagged release. You can find the latest stable release version on Homestead's [GitHub releases page](https://github.com/laravel/homestead/releases). -->
위 명령어는 최신 Homestead 코드를 GitHub 저장소에서 받아와 최신 안정 릴리스 브랜치를 체크아웃합니다. 최신 안정 버전은 Homestead의 [GitHub releases page](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

<!-- If you have installed Homestead via your project's `composer.json` file, you should ensure your `composer.json` file contains `"laravel/homestead": "^12"` and update your dependencies: -->
만약 프로젝트의 `composer.json` 파일을 통해 Homestead를 설치했다면, `composer.json`에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 아래처럼 패키지 업데이트를 진행해야 합니다.

```
composer update
```

<!-- Next, you should update the Vagrant box using the `vagrant box update` command: -->
그 다음, `vagrant box update` 명령으로 Vagrant 박스를 최신 버전으로 갱신합니다.


<!--     vagrant box update -->
    vagrant box update


<!-- After updating the Vagrant box, you should run the `bash init.sh` command from the Homestead directory in order to update Homestead's additional configuration files. You will be asked whether you wish to overwrite your existing `Homestead.yaml`, `after.sh`, and `aliases` files: -->
Vagrant 박스를 갱신한 후에는, Homestead 디렉터리에서 `bash init.sh`를 실행하여 추가 설정 파일도 함께 업데이트해야 합니다. 진행 과정에서 기존의 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 여부를 물어봅니다.


```
// macOS / Linux...
bash init.sh

// Windows...
init.bat
```


<!-- Finally, you will need to regenerate your Homestead virtual machine to utilize the latest Vagrant installation: -->
마지막으로, 아래 명령어로 Homestead 가상머신을 재생성하여 최신 Vagrant 설정을 적용하세요.


<!--     vagrant up -->
    vagrant up


<a name="daily-usage"></a>
<!-- ## Daily Usage -->
## Daily Usage

<a name="connecting-via-ssh"></a>
<!-- ### Connecting Via SSH -->
### Connecting Via SSH

<!-- You can SSH into your virtual machine by executing the `vagrant ssh` terminal command from your Homestead directory. -->
Homestead 디렉터리에서 터미널에 `vagrant ssh` 명령을 입력하여 가상머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
<!-- ### Adding Additional Sites -->
### Adding Additional Sites

<!-- Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your other Laravel projects. You can run as many Laravel projects as you wish on a single Homestead environment. To add an additional site, add the site to your `Homestead.yaml` file. -->
Homestead 환경을 실행한 이후에도, 다른 Laravel 프로젝트를 위한 Nginx 사이트를 추가로 등록할 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 얼마든지 실행할 수 있으며, 각 사이트는 `Homestead.yaml` 파일에 추가하여 관리합니다.


```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```


> [!NOTE]
> 해당 프로젝트 폴더에 대한 [folder mapping](#configuring-shared-folders)이 먼저 설정되어 있어야 합니다.

<!-- If Vagrant is not automatically managing your "hosts" file, you may need to add the new site to that file as well. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`: -->
"hosts" 파일을 Vagrant가 자동으로 관리하지 않는 경우, 새로 추가하는 사이트의 주소도 직접 등록해야 할 수 있습니다. macOS 및 Linux에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 파일을 사용합니다.

```
192.168.56.56  homestead.test
192.168.56.56  another.test
```

<!-- Once the site has been added, execute the `vagrant reload --provision` terminal command from your Homestead directory. -->
사이트 추가가 끝나면, Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행하여 변경 내용을 반영해야 합니다.

<a name="site-types"></a>
<!-- #### Site Types -->
#### Site Types

<!-- Homestead supports several "types" of sites which allow you to easily run projects that are not based on Laravel. For example, we may easily add a Statamic application to Homestead using the `statamic` site type: -->
Homestead는 다양한 "사이트 타입"을 지원하여, Laravel 기반이 아닌 다른 프레임워크/프로젝트도 손쉽게 실행할 수 있습니다. 예를 들어 Statamic 애플리케이션을 `statamic` 타입으로 다음과 같이 추가할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

<!-- The available site types are: `apache`, `apigility`, `expressive`, `laravel` (the default), `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, and `zf`. -->
지원되는 사이트 타입은: `apache`, `apigility`, `expressive`, `laravel`(기본값), `proxy`, `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf` 등입니다.

<a name="site-parameters"></a>
<!-- #### Site Parameters -->
#### Site Parameters

<!-- You may add additional Nginx `fastcgi_param` values to your site via the `params` site directive: -->
사이트 설정에서 추가적인 Nginx `fastcgi_param` 값을 지정하고 싶다면, `params` 옵션을 사용할 수 있습니다.


```
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
글로벌 환경 변수는 `Homestead.yaml` 파일에 아래처럼 정의할 수 있습니다.


```
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```


<!-- After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command. This will update the PHP-FPM configuration for all of the installed PHP versions and also update the environment for the `vagrant` user. -->
`Homestead.yaml` 파일을 수정한 후에는 반드시 `vagrant reload --provision`을 실행해주어야 합니다. 이로써 설치된 모든 PHP 버전의 PHP-FPM 구성과 `vagrant` 계정의 환경 변수까지 자동으로 갱신됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- By default, the following ports are forwarded to your Homestead environment: -->
기본적으로, 아래와 같은 포트가 Homestead 환경에 포워딩되어 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
-->
- **HTTP:** 8000 &rarr; 80으로 포워딩
- **HTTPS:** 44300 &rarr; 443으로 포워딩

<!-- </div> -->
</div>

<a name="forwarding-additional-ports"></a>
<!-- #### Forwarding Additional Ports -->
#### Forwarding Additional Ports

<!-- If you wish, you may forward additional ports to the Vagrant box by defining a `ports` configuration entry within your `Homestead.yaml` file. After updating the `Homestead.yaml` file, be sure to re-provision the machine by executing the `vagrant reload --provision` command: -->
필요하다면, `Homestead.yaml` 파일에 `ports` 설정 항목을 정의해 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. `Homestead.yaml` 파일을 수정한 뒤에는 역시 `vagrant reload --provision` 명령을 실행해야 적용됩니다.


```
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```


<!-- Below is a list of additional Homestead service ports that you may wish to map from your host machine to your Vagrant box: -->
아래는 호스트 머신과 Vagrant 박스 간에 맵핑이 필요한 주요 Homestead 서비스 포트 목록입니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- **SSH:** 2222 &rarr; To 22
- **ngrok UI:** 4040 &rarr; To 4040
- **MySQL:** 33060 &rarr; To 3306
- **PostgreSQL:** 54320 &rarr; To 5432
- **MongoDB:** 27017 &rarr; To 27017
- **Mailhog:** 8025 &rarr; To 8025
- **Minio:** 9600 &rarr; To 9600
-->
- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailhog:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

<!-- </div> -->
</div>

<a name="php-versions"></a>
<!-- ### PHP Versions -->
### PHP Versions

<!-- Homestead 6 introduced support for running multiple versions of PHP on the same virtual machine. You may specify which version of PHP to use for a given site within your `Homestead.yaml` file. The available PHP versions are: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0" (the default), and "8.1": -->
Homestead 6부터는 하나의 가상머신에서 여러 PHP 버전을 동시에 사용할 수 있게 되었습니다. 각 사이트별로 사용할 PHP 버전을 `Homestead.yaml`에서 직접 지정할 수 있습니다. 지원 버전: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0"(기본값), "8.1".


```
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```


<!-- [Within your Homestead virtual machine](#connecting-via-ssh), you may use any of the supported PHP versions via the CLI: -->
[Within your Homestead virtual machine](#connecting-via-ssh)에서는 CLI에서 아래와 같이 각 PHP 버전으로 Artisan 명령어를 실행할 수 있습니다.

```
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
```

<!-- You may change the default version of PHP used by the CLI by issuing the following commands from within your Homestead virtual machine: -->
CLI에서 기본 PHP 버전을 바꾸려면 아래 명령 중 하나를 Homestead 가상머신 내에서 실행하면 됩니다.

```
php56
php70
php71
php72
php73
php74
php80
php81
```

<a name="connecting-to-databases"></a>
<!-- ### Connecting To Databases -->
### Connecting To Databases

<!-- A `homestead` database is configured for both MySQL and PostgreSQL out of the box. To connect to your MySQL or PostgreSQL database from your host machine's database client, you should connect to `127.0.0.1` on port `33060` (MySQL) or `54320` (PostgreSQL). The username and password for both databases is `homestead` / `secret`. -->
MySQL과 PostgreSQL 모두 `homestead`라는 이름의 데이터베이스가 기본 생성되어 있습니다. 로컬 머신의 DB 클라이언트에서 MySQL 또는 PostgreSQL에 연결하려면, `127.0.0.1`의 `33060`(MySQL) 또는 `54320`(PostgreSQL) 포트로 접속해야 합니다. 사용자명과 비밀번호는 각각 `homestead` / `secret` 입니다.

> [!NOTE]
> 이 비표준 포트는 *호스트 머신*에서 데이터베이스에 접속할 때만 사용합니다. Laravel은 가상머신 _내부에서_ 동작하므로, Laravel 애플리케이션의 `database` 설정 파일에서는 기본 포트인 3306, 5432를 그대로 사용해야 합니다.

<a name="database-backups"></a>
<!-- ### Database Backups -->
### Database Backups

<!-- Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file: -->
Homestead는 가상머신 삭제 시, 데이터베이스 자동 백업 기능을 지원합니다. 이 기능은 Vagrant 2.1.0 이상 버전에서 사용할 수 있으며, 구버전이라면 `vagrant-triggers` 플러그인을 설치하면 됩니다. 자동 백업을 활성화하려면 아래 설정을 `Homestead.yaml`에 추가하세요.


```
backup: true
```


<!-- Once configured, Homestead will export your databases to `mysql_backup` and `postgres_backup` directories when the `vagrant destroy` command is executed. These directories can be found in the folder where you installed Homestead or in the root of your project if you are using the [per project installation](#per-project-installation) method. -->
설정 후, `vagrant destroy` 명령을 실행할 때마다 `mysql_backup` 및 `postgres_backup` 디렉터리에 각 데이터베이스가 백업됩니다. 이 폴더들은 Homestead를 설치한 디렉터리(혹은 [per project installation](#per-project-installation)를 했다면 프로젝트 루트)에 생성됩니다.

<a name="configuring-cron-schedules"></a>
<!-- ### Configuring Cron Schedules -->
### Configuring Cron Schedules

<!-- Laravel provides a convenient way to [schedule cron jobs](/docs/8.x/scheduling) by scheduling a single `schedule:run` Artisan command to run every minute. The `schedule:run` command will examine the job schedule defined in your `App\Console\Kernel` class to determine which scheduled tasks to run. -->
Laravel은 [schedule cron jobs](/docs/8.x/scheduling)을 매우 간편하게 할 수 있도록, 매 분마다 `schedule:run` 아티즌 명령만 실행하면 됩니다. `schedule:run` 명령은 `App\Console\Kernel` 클래스에 정의된 예약 작업을 검사하여 실행할 작업이 있으면 실행합니다.

<!-- If you would like the `schedule:run` command to be run for a Homestead site, you may set the `schedule` option to `true` when defining the site: -->
특정 Homestead 사이트에서 `schedule:run` 명령을 매 분마다 실행하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 지정하면 됩니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

<!-- The cron job for the site will be defined in the `/etc/cron.d` directory of the Homestead virtual machine. -->
해당 사이트의 크론 작업은 Homestead 가상머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailhog"></a>
<!-- ### Configuring MailHog -->
### Configuring MailHog

<!-- [MailHog](https://github.com/mailhog/MailHog) allows you to intercept your outgoing email and examine it without actually sending the mail to its recipients. To get started, update your application's `.env` file to use the following mail settings: -->
[MailHog](https://github.com/mailhog/MailHog)는 실제 수신자에게 메일을 발송하지 않고, 애플리케이션에서 보내는 메일을 가로채어 확인할 수 있도록 해주는 도구입니다. 다음과 같이 애플리케이션의 `.env` 파일을 수정해서 사용할 수 있습니다.

```
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

<!-- Once MailHog has been configured, you may access the MailHog dashboard at `http://localhost:8025`. -->
MailHog 설정을 완료하면, 브라우저에서 `http://localhost:8025`로 MailHog 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
<!-- ### Configuring Minio -->
### Configuring Minio

<!-- [Minio](https://github.com/minio/minio) is an open source object storage server with an Amazon S3 compatible API. To install Minio, update your `Homestead.yaml` file with the following configuration option in the [features](#installing-optional-features) section: -->
[Minio](https://github.com/minio/minio)는 Amazon S3와 호환되는 API를 가진 오픈 소스 객체 저장소 서버입니다. Minio 설치를 위해서는 `Homestead.yaml` 파일의 [features](#installing-optional-features) 항목에 아래와 같이 추가해야 합니다.


```
minio: true
```


<!-- By default, Minio is available on port 9600. You may access the Minio control panel by visiting `http://localhost:9600`. The default access key is `homestead`, while the default secret key is `secretkey`. When accessing Minio, you should always use region `us-east-1`. -->
Minio는 기본적으로 9600번 포트에서 사용 가능합니다. 브라우저에서 `http://localhost:9600`로 Minio 제어판에 접속할 수 있으며, 기본 access key는 `homestead`, secret key는 `secretkey`입니다. Minio를 사용할 때는 항상 region `us-east-1`을 지정해야 합니다.

<!-- In order to use Minio, you will need to adjust the S3 disk configuration in your application's `config/filesystems.php` configuration file. You will need to add the `use_path_style_endpoint` option to the disk configuration as well as change the `url` key to `endpoint`: -->
Minio를 제대로 사용하려면 애플리케이션의 `config/filesystems.php` 파일에서 S3 디스크 설정을 아래처럼 수정해야 합니다. `use_path_style_endpoint` 옵션을 추가하고, `url` 대신 `endpoint`를 써야 합니다.

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
그리고 `.env` 파일에는 다음 값을 추가해야 합니다.

```bash
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
AWS_URL=http://localhost:9600
```

<!-- To provision Minio powered "S3" buckets, add a `buckets` directive to your `Homestead.yaml` file. After defining your buckets, you should execute the `vagrant reload --provision` command in your terminal: -->
Minio 기반의 "S3" 버킷 생성을 위해, `Homestead.yaml` 파일에 `buckets` 항목을 추가하고 버킷 정의를 완료한 뒤 `vagrant reload --provision` 명령을 실행하세요.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

<!-- Supported `policy` values include: `none`, `download`, `upload`, and `public`. -->
정책(`policy`) 값으로는 `none`, `download`, `upload`, `public`을 사용할 수 있습니다.

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- In order to run [Laravel Dusk](/docs/8.x/dusk) tests within Homestead, you should enable the [`webdriver` feature](#installing-optional-features) in your Homestead configuration: -->
[Laravel Dusk](/docs/8.x/dusk) 테스트를 Homestead에서 실행하려면 [`webdriver` feature](#installing-optional-features)을 Homestead 설정에서 반드시 활성화해야 합니다.

```yaml
features:
    - webdriver: true
```

<!-- After enabling the `webdriver` feature, you should execute the `vagrant reload --provision` command in your terminal. -->
`webdriver` 기능을 활성화했다면, `vagrant reload --provision` 명령을 터미널에서 실행해야 합니다.

<a name="sharing-your-environment"></a>
<!-- ### Sharing Your Environment -->
### Sharing Your Environment

<!-- Sometimes you may wish to share what you're currently working on with coworkers or a client. Vagrant has built-in support for this via the `vagrant share` command; however, this will not work if you have multiple sites configured in your `Homestead.yaml` file. -->
동료나 클라이언트와 현재 개발 중인 사이트를 임시로 공유하고 싶을 때가 있습니다. Vagrant의 기본 `vagrant share` 명령을 이용할 수 있지만, `Homestead.yaml` 파일에 여러 사이트가 등록된 경우에는 제대로 동작하지 않을 수 있습니다.

<!-- To solve this problem, Homestead includes its own `share` command. To get started, [SSH into your Homestead virtual machine](#connecting-via-ssh) via `vagrant ssh` and execute the `share homestead.test` command. This command will share the `homestead.test` site from your `Homestead.yaml` configuration file. You may substitute any of your other configured sites for `homestead.test`: -->
이 문제를 해결하기 위해, Homestead는 자체적인 `share` 명령을 제공합니다. 먼저 `vagrant ssh`로 [SSH into your Homestead virtual machine](#connecting-via-ssh)한 뒤 `share homestead.test` 명령을 실행하세요. 이 명령은 `Homestead.yaml` 설정 파일에 등록된 `homestead.test` 사이트를 공유합니다. `homestead.test` 대신 설정해 둔 다른 사이트로 대체할 수 있습니다.

<!--     share homestead.test -->
    share homestead.test

<!-- After running the command, you will see an Ngrok screen appear which contains the activity log and the publicly accessible URLs for the shared site. If you would like to specify a custom region, subdomain, or other Ngrok runtime option, you may add them to your `share` command: -->
명령을 실행하면 Ngrok 화면이 나타나며, 공유된 사이트의 활동 로그와 외부에서 접근 가능한 URL을 확인할 수 있습니다. 커스텀 region, 서브도메인 등 Ngrok 실행 옵션을 지정하고 싶다면 `share` 명령에 함께 추가할 수 있습니다.

<!--     share homestead.test -region=eu -subdomain=laravel -->
    share homestead.test -region=eu -subdomain=laravel

> [!NOTE]
> 주의: Vagrant 자체는 보안이 강력하지 않으므로, `share` 명령 실행 시 여러분의 가상머신은 인터넷에 노출된다는 사실을 꼭 명심해야 합니다.

<a name="debugging-and-profiling"></a>
<!-- ## Debugging & Profiling -->
## Debugging & Profiling

<a name="debugging-web-requests"></a>
<!-- ### Debugging Web Requests With Xdebug -->
### Debugging Web Requests With Xdebug

<!-- Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code. -->
Homestead에는 [Xdebug](https://xdebug.org) 기반의 스텝 디버깅 기능이 내장되어 있습니다. 브라우저에서 페이지를 열면, PHP가 IDE로 연결되어 코드 실행 중 값을 점검, 수정할 수 있습니다.

<!-- By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/). -->
기본적으로 Xdebug는 이미 실행 중이며, 언제든 연결을 대기합니다. CLI에서 Xdebug를 사용하려면, Homestead 가상머신 내에서 `sudo phpenmod xdebug` 명령을 실행하세요. 이후 IDE에서 디버깅을 활성화하면 됩니다. 브라우저 확장이나 [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/)을 사용해 Xdebug 트리거도 가능합니다.

> [!NOTE]
> Xdebug가 활성화되면 PHP 실행 속도가 크게 느려질 수 있습니다. 사용을 중지하려면 `sudo phpdismod xdebug` 명령으로 비활성화하고, FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
<!-- #### Autostarting Xdebug -->
#### Autostarting Xdebug

<!-- When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration: -->
웹서버를 통한 통합 테스트(퍼스트널 테스트)에서 디버깅을 좀 더 쉽게 하려면, Xdebug를 자동 시작하도록 설정할 수 있습니다. Homestead 가상머신 내부의 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하여 아래 설정을 추가합니다.

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.remote_host = 192.168.10.1
xdebug.remote_autostart = 1
```

<a name="debugging-cli-applications"></a>
<!-- ### Debugging CLI Applications -->
### Debugging CLI Applications

<!-- To debug a PHP CLI application, use the `xphp` shell alias inside your Homestead virtual machine: -->
PHP CLI 애플리케이션 디버깅은 Homestead 가상머신 내에서 `xphp` 쉘 별칭을 사용해 실행하면 됩니다.

<!--     xphp /path/to/script -->
    xphp /path/to/script

<a name="profiling-applications-with-blackfire"></a>
<!-- ### Profiling Applications with Blackfire -->
### Profiling Applications with Blackfire

<!-- [Blackfire](https://blackfire.io/docs/introduction) is a service for profiling web requests and CLI applications. It offers an interactive user interface which displays profile data in call-graphs and timelines. It is built for use in development, staging, and production, with no overhead for end users. In addition, Blackfire provides performance, quality, and security checks on code and `php.ini` configuration settings. -->
[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션의 프로파일링을 위한 서비스입니다. 호출 그래프와 타임라인 형태로 프로파일링 데이터를 직관적으로 보여주며, 개발·스테이징·운영 환경을 모두 지원(엔드 유저에게는 오버헤드 없음)합니다. 또한 `php.ini`와 코드 품질, 성능, 보안을 자동으로 점검해줍니다.

<!-- The [Blackfire Player](https://blackfire.io/docs/player/index) is an open-source Web Crawling, Web Testing, and Web Scraping application which can work jointly with Blackfire in order to script profiling scenarios. -->
[Blackfire Player](https://blackfire.io/docs/player/index)는 웹 크롤링, 웹 테스트, 웹 스크래핑을 위한 오픈소스 도구로, Blackfire와 연동해 시나리오 기반 프로파일링을 할 수 있습니다.

<!-- To enable Blackfire, use the "features" setting in your Homestead configuration file: -->
Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 항목에 아래처럼 추가하세요.

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

<!-- Blackfire server credentials and client credentials [require a Blackfire account](https://blackfire.io/signup). Blackfire offers various options to profile an application, including a CLI tool and browser extension. Please [review the Blackfire documentation for more details](https://blackfire.io/docs/cookbooks/index). -->
Blackfire 서버 및 클라이언트 인증 정보는 [require a Blackfire account](https://blackfire.io/signup)이 필요합니다. CLI 도구, 브라우저 확장 등 다양한 방법으로 프로파일링이 가능합니다. 보다 상세한 정보는 [review the Blackfire documentation for more details](https://blackfire.io/docs/cookbooks/index)를 확인하세요.

<a name="network-interfaces"></a>
<!-- ## Network Interfaces -->
## Network Interfaces

<!-- The `networks` property of the `Homestead.yaml` file configures network interfaces for your Homestead virtual machine. You may configure as many interfaces as necessary: -->
`Homestead.yaml` 파일의 `networks` 항목에서는 Homestead 가상머신의 네트워크 인터페이스를 설정할 수 있습니다. 여러 인터페이스도 자유롭게 구성 가능합니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

<!-- To enable a [bridged](https://www.vagrantup.com/docs/networking/public_network.html) interface, configure a `bridge` setting for the network and change the network type to `public_network`: -->
[bridged](https://www.vagrantup.com/docs/networking/public_network.html) 인터페이스를 활성화하려면, 네트워크 타입을 `public_network`로 변경하고 `bridge` 값을 설정합니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

<!-- To enable [DHCP](https://www.vagrantup.com/docs/networking/public_network.html), just remove the `ip` option from your configuration: -->
[DHCP](https://www.vagrantup.com/docs/networking/public_network.html)를 사용하려면, `ip` 항목을 생략하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

<a name="extending-homestead"></a>
<!-- ## Extending Homestead -->
## Extending Homestead

<!-- You may extend Homestead using the `after.sh` script in the root of your Homestead directory. Within this file, you may add any shell commands that are necessary to properly configure and customize your virtual machine. -->
Homestead는 Homestead 디렉터리 루트에 위치한 `after.sh` 스크립트를 통해 확장할 수 있습니다. 이 파일에는 가상머신을 사용자 맞춤으로 추가 설정하거나, 필요한 쉘 명령을 자유롭게 추가할 수 있습니다.

<!-- When customizing Homestead, Ubuntu may ask you if you would like to keep a package's original configuration or overwrite it with a new configuration file. To avoid this, you should use the following command when installing packages in order to avoid overwriting any configuration previously written by Homestead: -->
패키지 설치 등으로 Homestead에서 이미 작성한 설정 파일이 덮어써지는 것을 방지하려면 Homestead에서 아래와 같이 설치 명령어를 사용하는 것이 안전합니다.

```
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
<!-- ### User Customizations -->
### User Customizations

<!-- When using Homestead with your team, you may want to tweak Homestead to better fit your personal development style. To accomplish this, you may create a `user-customizations.sh` file in the root of your Homestead directory (the same directory containing your `Homestead.yaml` file). Within this file, you may make any customization you would like; however, the `user-customizations.sh` should not be version controlled. -->
팀에서 Homestead를 사용할 경우, 각 개발자의 개발 스타일에 맞는 사용자 맞춤 설정을 추가하고 싶을 수 있습니다. 이를 위해 Homestead 디렉터리(`Homestead.yaml` 파일이 있는 위치)에 `user-customizations.sh` 파일을 생성해서 원하는 모든 커스텀 설정을 진행할 수 있습니다. 단, `user-customizations.sh` 파일은 버전관리에는 포함하지 않는 것이 좋습니다.

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
기본적으로 Homestead는 `natdnshostresolver` 옵션을 `on`으로 설정하여, 호스트 운영체제의 DNS 정보를 사용할 수 있습니다. 만약 이 값을 직접 제어하고 싶다면, `Homestead.yaml`에 아래처럼 옵션을 추가하면 됩니다.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```

<a name="symbolic-links-on-windows"></a>
<!-- #### Symbolic Links On Windows -->
#### Symbolic Links On Windows

<!-- If symbolic links are not working properly on your Windows machine, you may need to add the following block to your `Vagrantfile`: -->
Windows 환경에서 심볼릭 링크가 제대로 동작하지 않는다면, `Vagrantfile`에 아래 코드를 추가해야 할 수 있습니다.

```ruby
config.vm.provider "virtualbox" do |v|
    v.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```