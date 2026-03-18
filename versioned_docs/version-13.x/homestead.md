# Laravel Homestead

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [시작하기](#first-steps)
    - [Homestead 설정](#configuring-homestead)
    - [Nginx 사이트 설정](#configuring-nginx-sites)
    - [서비스 설정](#configuring-services)
    - [Vagrant Box 실행](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치](#installing-optional-features)
    - [별칭](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적인 사용법](#daily-usage)
    - [SSH로 접속하기](#connecting-via-ssh)
    - [추가 사이트 등록](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정](#configuring-cron-schedules)
    - [Mailpit 설정](#configuring-mailpit)
    - [MinIO 설정](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug를 사용한 웹 요청 디버깅](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire를 사용한 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장](#extending-homestead)
- [프로바이더별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개 (Introduction)

> [!WARNING]
> Laravel Homestead는 더 이상 적극적으로 유지 관리되지 않는 레거시 패키지입니다. [Laravel Sail](/docs/13.x/sail)을 현대적인 대안으로 사용할 수 있습니다.

Laravel는 로컬 개발 환경을 포함하여 전체 PHP 개발 경험을 즐겁게 만들기 위해 노력하고 있습니다. [Laravel Homestead](https://github.com/laravel/homestead)는 PHP, 웹 서버 또는 기타 서버 소프트웨어를 로컬 컴퓨터에 설치할 필요 없이 멋진 개발 환경을 제공하는 공식 사전 패키지 Vagrant 박스입니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝하는 간단하고 우아한 방법을 제공합니다. Vagrant Box는 완전히 일회용입니다. 문제가 발생하면 몇 분 안에 Box를 삭제하고 다시 만들 수 있습니다!

Homestead는 모든 Windows, macOS 또는 Linux 시스템에서 실행되며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 및 놀라운 Laravel 애플리케이션을 개발하는 데 필요한 기타 모든 소프트웨어를 포함합니다.

> [!WARNING]
> Windows를 사용하는 경우 하드웨어 가상화(VT-x)를 활성화해야 할 수도 있습니다. 일반적으로 BIOS를 통해 활성화할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x에 액세스하려면 Hyper-V를 추가로 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어

<style>{`
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
`}</style>

<div id="software-list" markdown="1">

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
- SQLite3
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

</div>

<a name="optional-software"></a>
### 선택적 소프트웨어

<style>{`
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
`}</style>

<div id="software-list" markdown="1">

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

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정 (Installation and Setup)

<a name="first-steps"></a>
### 첫 번째 단계

Homestead 환경을 시작하기 전에 [Vagrant](https://developer.hashicorp.com/vagrant/downloads)와 지원되는 다음 프로바이더 중 하나를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이러한 모든 소프트웨어 패키지는 널리 사용되는 모든 운영 체제에 대해 사용하기 쉬운 시각적 설치 프로그램을 제공합니다.

Parallels 프로바이더를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치

Homestead 저장소를 호스트 시스템에 복제하여 Homestead를 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로 저장소를 "홈" 디렉터리 내의 `Homestead` 폴더에 복제하는 것을 고려하세요. 이 문서 전체에서 우리는 이 디렉토리를 "Homestead 디렉토리"라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead 저장소를 복제한 후 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치에는 항상 Homestead의 최신 안정 릴리스가 포함되어 있습니다.

```shell
cd ~/Homestead

git checkout release
```

다음으로, Homestead 디렉토리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 구성 파일을 생성합니다. `Homestead.yaml` 파일은 Homestead 설치에 대한 모든 설정을 구성하는 곳입니다. 이 파일은 Homestead 디렉토리에 위치합니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정

<a name="setting-your-provider"></a>
#### 프로바이더 설정

`Homestead.yaml` 파일의 `provider` 키는 어떤 Vagrant 프로바이더를 사용해야 하는지 나타냅니다: `virtualbox` 또는 `parallels`:

    provider: virtualbox

> [!WARNING]
> Apple Silicon을 사용하는 경우 Parallels 프로바이더가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 구성

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유하려는 모든 폴더를 나열합니다. 이 폴더 내의 파일이 변경되면 로컬 컴퓨터와 Homestead 가상 환경 간에 동기화가 유지됩니다. 필요한 만큼 공유 폴더를 구성할 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 구문을 사용해서는 안 되며 대신 `C:\Users\user\Code\project1`와 같은 프로젝트의 전체 경로를 사용해야 합니다.

모든 애플리케이션이 포함된 하나의 큰 디렉터리를 매핑하는 대신 항상 개별 애플리케이션을 자체 폴더 매핑에 매핑해야 합니다. 폴더를 매핑할 때 가상 머신은 폴더의 *모든* 파일에 대한 모든 디스크 IO를 추적해야 합니다. 폴더에 파일 수가 많으면 성능이 저하될 수 있습니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead를 사용할 때 `.`(현재 디렉터리)를 마운트하면 안 됩니다. 이로 인해 Vagrant는 현재 폴더를 `/vagrant`에 매핑하지 않으며 옵션 기능이 중단되고 프로비저닝 중에 예기치 않은 결과가 발생합니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 활성화하려면 폴더 매핑에 `type` 옵션을 추가하면 됩니다.

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용하는 경우 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 고려해야 합니다. 이 플러그인은 Homestead 가상 머신 내의 파일 및 디렉토리에 대한 올바른 사용자/그룹 권한을 유지합니다.

Vagrant의 [동기화된 폴더](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)에서 지원하는 옵션을 `options` 키 아래에 나열하여 전달할 수도 있습니다.

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
### Nginx 사이트 구성

Nginx에 익숙하지 않으신가요? 괜찮아요. `Homestead.yaml` 파일의 `sites` 속성을 사용하면 "도메인"을 Homestead 환경의 폴더에 쉽게 매핑할 수 있습니다. 샘플 사이트 구성은 `Homestead.yaml` 파일에 포함되어 있습니다. 다시 말하지만, Homestead 환경에 필요한 만큼 많은 사이트를 추가할 수 있습니다. Homestead는 작업 중인 모든 Laravel 애플리케이션에 대해 편리한 가상화 환경 역할을 할 수 있습니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

Homestead 가상 머신을 프로비저닝한 후 `sites` 속성을 변경하는 경우 터미널에서 `vagrant reload --provision` 명령을 실행하여 가상 머신의 Nginx 구성을 업데이트해야 합니다.

> [!WARNING]
> Homestead 스크립트는 가능한 한 멱등성을 갖도록 구축되었습니다. 그러나 프로비저닝 중에 문제가 발생하는 경우 `vagrant destroy && vagrant up` 명령을 실행하여 머신을 삭제하고 재구축해야 합니다.

<a name="hostname-resolution"></a>
#### 호스트 이름 확인

Homestead는 자동 호스트 확인을 위해 `mDNS`를 사용하여 호스트 이름을 게시합니다. `Homestead.yaml` 파일에 `hostname: homestead`를 설정하면 `homestead.local`에서 호스트를 사용할 수 있습니다. macOS, iOS 및 Linux 데스크탑 배포에는 기본적으로 `mDNS` 지원이 포함됩니다. Windows를 사용하는 경우 [Windows용 Bonjour 인쇄 서비스](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트 이름을 사용하는 것은 Homestead의 [프로젝트별 설치](#per-project-installation)에 가장 적합합니다. 단일 Homestead 인스턴스에서 여러 사이트를 호스팅하는 경우 웹 사이트의 "도메인"을 컴퓨터의 `hosts` 파일에 추가할 수 있습니다. `hosts` 파일은 Homestead 사이트에 대한 요청을 Homestead 가상 머신으로 리디렉션합니다. macOS 및 Linux에서 이 파일은 `/etc/hosts`에 있습니다. Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다. 이 파일에 추가하는 줄은 다음과 같습니다.

```text
192.168.56.56  homestead.test
```

나열된 IP 주소가 `Homestead.yaml` 파일에 설정된 주소인지 확인하세요. `hosts` 파일에 도메인을 추가하고 Vagrant Box를 실행하면 웹 브라우저를 통해 사이트에 액세스할 수 있습니다.

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 구성

Homestead는 기본적으로 여러 서비스를 시작합니다. 그러나 프로비저닝 중에 활성화 또는 비활성화할 서비스를 사용자 지정할 수 있습니다. 예를 들어, `Homestead.yaml` 파일 내에서 `services` 옵션을 수정하여 PostgreSQL를 활성화하고 MySQL을 비활성화할 수 있습니다.

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

지정된 서비스는 `enabled` 및 `disabled` 지시어의 순서에 따라 시작되거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant Box 실행

원하는 대로 `Homestead.yaml`를 편집한 후 Homestead 디렉토리에서 `vagrant up` 명령을 실행하십시오. Vagrant는 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동으로 구성합니다.

머신을 파괴하려면 `vagrant destroy` 명령을 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역적으로 설치하고 모든 프로젝트에서 동일한 Homestead 가상 머신을 공유하는 대신 관리하는 각 프로젝트에 대해 Homestead 인스턴스를 구성할 수 있습니다. 프로젝트와 함께 `Vagrantfile`를 디스패치하려는 경우 프로젝트별로 Homestead를 설치하면 프로젝트 저장소를 복제한 후 즉시 다른 사람들이 `vagrant up`에서 프로젝트 작업을 할 수 있도록 하여 도움이 될 수 있습니다.

Composer 패키지 관리자를 사용하여 프로젝트에 Homestead를 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```

Homestead가 설치되면 Homestead의 `make` 명령을 호출하여 프로젝트에 대한 `Vagrantfile` 및 `Homestead.yaml` 파일을 생성합니다. 이 파일은 프로젝트의 루트에 배치됩니다. `make` 명령은 `Homestead.yaml` 파일의 `sites` 및 `folders` 지시문을 자동으로 구성합니다.

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

다음으로, 터미널에서 `vagrant up` 명령을 실행하고 브라우저의 `http://homestead.test`에서 프로젝트에 액세스하세요. 자동 [호스트 이름 확인](#hostname-resolution)을 사용하지 않는 경우 `homestead.test` 또는 선택한 도메인에 대한 `/etc/hosts` 파일 항목을 추가해야 한다는 점을 기억하십시오.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml` 파일 내의 `features` 옵션을 사용하여 설치됩니다. 대부분의 기능은 부울 값을 사용하여 활성화하거나 비활성화할 수 있지만 일부 기능은 여러 구성 옵션을 허용합니다.

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
#### Elasticsearch

지원되는 Elasticsearch 버전을 지정할 수 있으며 정확한 버전 번호(major.minor.patch)여야 합니다. 기본 설치에서는 'homestead'라는 클러스터가 생성됩니다. Elasticsearch에 운영 체제 메모리의 절반 이상을 할당해서는 안 되므로 Homestead 가상 머신에 Elasticsearch 할당이 최소한 두 배 이상 있는지 확인하십시오.

> [!NOTE]
> 구성을 사용자 지정하는 방법을 알아보려면 [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 확인하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL가 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL을 즉시 대체하는 역할을 하므로 애플리케이션의 데이터베이스 구성에서는 `mysql` 데이터베이스 드라이버를 계속 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치는 데이터베이스 사용자 이름을 `homestead`로 설정하고 해당 비밀번호를 `secret`로 설정합니다.

<a name="neo4j"></a>
#### Neo4j

기본 Neo4j 설치는 데이터베이스 사용자 이름을 `homestead`로 설정하고 해당 비밀번호를 `secret`로 설정합니다. Neo4j 브라우저에 액세스하려면 웹 브라우저를 통해 `http://homestead.test:7474`를 방문하세요. `7687`(Bolt), `7474`(HTTP) 및 `7473`(HTTPS) 포트는 Neo4j 클라이언트의 요청을 처리할 준비가 되어 있습니다.

<a name="aliases"></a>
### 별칭

Homestead 디렉토리에 있는 `aliases` 파일을 수정하여 Homestead 가상 머신에 Bash 별칭을 추가할 수 있습니다:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일을 업데이트한 후에는 `vagrant reload --provision` 명령을 사용하여 Homestead 가상 머신을 다시 프로비저닝해야 합니다. 이렇게 하면 새 별칭을 시스템에서 사용할 수 있습니다.

<a name="updating-homestead"></a>
## Homestead 업데이트 (Updating Homestead)

Homestead 업데이트를 시작하기 전에 Homestead 디렉토리에서 다음 명령을 실행하여 현재 가상 머신을 제거했는지 확인해야 합니다.

```shell
vagrant destroy
```

다음으로 Homestead 소스 코드를 업데이트해야 합니다. 리포지토리를 복제한 경우 원래 리포지토리를 복제한 위치에서 다음 명령을 실행할 수 있습니다.

```shell
git fetch

git pull origin release
```

이 명령은 GitHub 저장소에서 최신 Homestead 코드를 가져오고 최신 태그를 가져온 다음 최신 태그가 지정된 릴리스를 확인합니다. Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 최신 안정 릴리스 버전을 찾을 수 있습니다.

프로젝트의 `composer.json` 파일을 통해 Homestead를 설치한 경우 `composer.json` 파일에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 의존성을 업데이트해야 합니다.

```shell
composer update
```

다음으로 `vagrant box update` 명령을 사용하여 Vagrant Box를 업데이트해야 합니다.

```shell
vagrant box update
```

Vagrant 박스를 업데이트한 후 Homestead의 추가 구성 파일을 업데이트하려면 Homestead 디렉토리에서 `bash init.sh` 명령을 실행해야 합니다. 기존 `Homestead.yaml`, `after.sh` 및 `aliases` 파일을 덮어쓸지 묻는 메시지가 표시됩니다.

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로 최신 Vagrant 설치를 활용하려면 Homestead 가상 머신을 다시 생성해야 합니다.

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적인 사용법 (Daily Usage)

<a name="connecting-via-ssh"></a>
### SSH를 통해 연결

Homestead 디렉토리에서 `vagrant ssh` 터미널 명령을 실행하여 가상 머신에 SSH를 통해 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가

Homestead 환경이 프로비저닝되고 실행되면 다른 Laravel 프로젝트를 위해 추가 Nginx 사이트를 추가할 수 있습니다. 단일 Homestead 환경에서 원하는 만큼 많은 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트를 추가하려면 해당 사이트를 `Homestead.yaml` 파일에 추가하세요.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트를 추가하기 전에 프로젝트 디렉터리에 대한 [폴더 매핑](#configuring-shared-folders)을 구성했는지 확인해야 합니다.

Vagrant가 "hosts" 파일을 자동으로 관리하지 않는 경우 해당 파일에 새 사이트를 추가해야 할 수도 있습니다. macOS 및 Linux에서 이 파일은 `/etc/hosts`에 있습니다. Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다.

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트가 추가되면 Homestead 디렉토리에서 `vagrant reload --provision` 터미널 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 Laravel을 기반으로 하지 않는 프로젝트를 쉽게 실행할 수 있는 여러 "유형"의 사이트를 지원합니다. 예를 들어, `statamic` 사이트 유형을 사용하여 Homestead에 Statamic 애플리케이션을 쉽게 추가할 수 있습니다.

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 유형은 `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4` 및 `zf`입니다.

<a name="site-parameters"></a>
#### 사이트 매개변수

`params` 사이트 지시문을 통해 추가 Nginx `fastcgi_param` 값을 사이트에 추가할 수 있습니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```

<a name="environment-variables"></a>
### 환경 변수

전역 환경 변수를 `Homestead.yaml` 파일에 추가하여 정의할 수 있습니다.

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 파일을 업데이트한 후 `vagrant reload --provision` 명령을 실행하여 머신을 다시 프로비저닝해야 합니다. 그러면 설치된 모든 PHP 버전에 대한 PHP-FPM 구성이 업데이트되고 `vagrant` 사용자의 환경도 업데이트됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경으로 전달됩니다.

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80으로 전달
- **HTTPS:** 44300 → 443으로 전달

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 전달

원하는 경우 `Homestead.yaml` 파일 내에서 `ports` 구성 항목을 정의하여 추가 포트를 Vagrant Box에 전달할 수 있습니다. `Homestead.yaml` 파일을 업데이트한 후 `vagrant reload --provision` 명령을 실행하여 머신을 다시 프로비저닝해야 합니다.

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

다음은 호스트 시스템에서 Vagrant 박스로 매핑할 수 있는 추가 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 → 22로
- **ngrok UI:** 4040 → 4040으로
- **MySQL:** 33060 → 3306으로
- **PostgreSQL:** 54320 → 5432로
- **MongoDB:** 27017 → 27017로
- **Mailpit:** 8025 → 8025로
- **MinIO:** 9600 → 9600으로

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 동일한 가상 머신에서 여러 버전의 PHP 실행을 지원합니다. `Homestead.yaml` 파일 내에서 특정 사이트에 사용할 PHP 버전을 지정할 수 있습니다. 사용 가능한 PHP 버전은 "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2" 및 "8.3"(기본값)입니다.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내에서](#connecting-via-ssh), CLI를 통해 지원되는 PHP 버전을 사용할 수 있습니다.

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

Homestead 가상 머신 내에서 다음 명령을 실행하여 CLI에서 사용하는 PHP의 기본 버전을 변경할 수 있습니다.

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
### 데이터베이스에 연결

`homestead` 데이터베이스는 기본적으로 MySQL 및 PostgreSQL 모두에 대해 구성됩니다. 호스트 시스템의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL 데이터베이스에 연결하려면 포트 `33060`(MySQL) 또는 `54320`(PostgreSQL)에서 `127.0.0.1`에 연결해야 합니다. 두 데이터베이스의 사용자 이름과 비밀번호는 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트 시스템에서 데이터베이스에 연결할 때는 이러한 비표준 포트만 사용해야 합니다. Laravel가 가상 머신 _내에서_ 실행 중이므로 Laravel 애플리케이션의 `database` 구성 파일에서 기본 3306 및 5432 포트를 사용하게 됩니다.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 Homestead 가상 머신이 파괴되면 자동으로 데이터베이스를 백업할 수 있습니다. 이 기능을 활용하려면 Vagrant 2.1.0 이상을 사용해야 합니다. 또는 이전 버전의 Vagrant를 사용하는 경우 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 데이터베이스 백업을 활성화하려면 `Homestead.yaml` 파일에 다음 줄을 추가하세요.

```yaml
backup: true
```

일단 구성되면 Homestead는 `vagrant destroy` 명령이 실행될 때 데이터베이스를 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉터리로 내보냅니다. 이 디렉토리는 Homestead를 설치한 폴더나 [프로젝트별 설치](#per-project-installation) 방법을 사용하는 경우 프로젝트 루트에서 찾을 수 있습니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정

Laravel는 매분 실행되도록 단일 `schedule:run` Artisan 명령을 예약하여 [cron 작업 예약](/docs/13.x/scheduling)하는 편리한 방법을 제공합니다. `schedule:run` 명령은 `routes/console.php` 파일에 정의된 작업 일정을 검사하여 실행할 예약된 작업을 결정합니다.

Homestead 사이트에 대해 `schedule:run` 명령을 실행하려면 사이트를 정의할 때 `schedule` 옵션을 `true`로 설정할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉토리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정

[Mailpit](https://github.com/axllent/mailpit)을 사용하면 실제로 메일을 수신자에게 보내지 않고도 보내는 이메일을 가로채서 검사할 수 있습니다. 시작하려면 다음 메일 설정을 사용하도록 애플리케이션의 `.env` 파일을 업데이트하세요.

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit이 구성되면 `http://localhost:8025`에서 Mailpit 대시보드에 액세스할 수 있습니다.

<a name="configuring-minio"></a>
### MinIO 설정

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 갖춘 오픈 소스 객체 스토리지 서버입니다. Minio를 설치하려면 [기능](#installing-optional-features) 섹션에서 다음 구성 옵션을 사용하여 `Homestead.yaml` 파일을 업데이트하세요.

    minio: true

기본적으로 Minio는 포트 9600에서 사용할 수 있습니다. `http://localhost:9600`를 방문하여 Minio 제어판에 액세스할 수 있습니다. 기본 액세스 키는 `homestead`이고, 기본 비밀 키는 `secretkey`입니다. Minio에 접근할 때 항상 `us-east-1` 지역을 사용해야 합니다.

Minio를 사용하려면 `.env` 파일에 다음 옵션이 있는지 확인하세요.

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `buckets` 지시어를 `Homestead.yaml` 파일에 추가하세요. 버킷을 정의한 후 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

지원되는 `policy` 값에는 `none`, `download`, `upload` 및 `public`가 포함됩니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 내에서 [Laravel Dusk](/docs/13.x/dusk) 테스트를 실행하려면 Homestead 구성에서 [webdriver 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

`webdriver` 기능을 활성화한 후 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

<a name="sharing-your-environment"></a>
### 환경 공유

때로는 현재 작업 중인 작업을 동료나 고객과 공유하고 싶을 수도 있습니다. Vagrant에는 `vagrant share` 명령을 통해 이를 위한 기본 지원이 있습니다. 그러나 `Homestead.yaml` 파일에 여러 사이트가 구성된 경우에는 작동하지 않습니다.

이 문제를 해결하기 위해 Homestead에는 자체 `share` 명령이 포함되어 있습니다. 시작하려면 `vagrant ssh`를 통해 [Homestead 가상 머신에 SSH를 통해 연결](#connecting-via-ssh)하고 `share homestead.test` 명령을 실행하세요. 이 명령은 `Homestead.yaml` 구성 파일에서 `homestead.test` 사이트를 공유합니다. `homestead.test`를 다른 구성된 사이트로 대체할 수 있습니다.

```shell
share homestead.test
```

명령을 실행하면 활동 로그와 공유 사이트에 대해 공개적으로 액세스할 수 있는 URL이 포함된 Ngrok 화면이 표시됩니다. 사용자 지정 지역, 하위 도메인 또는 기타 Ngrok 런타임 옵션을 지정하려면 이를 `share` 명령에 추가할 수 있습니다.

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTP 대신 HTTPS를 통해 콘텐츠를 공유해야 하는 경우 `share` 대신 `sshare` 명령을 사용하면 그렇게 할 수 있습니다.

> [!WARNING]
> Vagrant는 본질적으로 안전하지 않으며 `share` 명령을 실행할 때 가상 머신이 인터넷에 노출된다는 점을 기억하십시오.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링 (Debugging and Profiling)

<a name="debugging-web-requests"></a>
### Xdebug를 사용하여 웹 요청 디버깅

Homestead에는 [Xdebug](https://xdebug.org)를 사용한 단계 디버깅 지원이 포함되어 있습니다. 예를 들어 브라우저에서 페이지에 액세스하면 PHP가 IDE에 연결되어 실행 중인 코드를 검사하고 수정할 수 있습니다.

기본적으로 Xdebug는 이미 실행 중이며 연결을 수락할 준비가 되어 있습니다. CLI에서 Xdebug를 활성화해야 하는 경우 Homestead 가상 머신 내에서 `sudo phpenmod xdebug` 명령을 실행하세요. 그런 다음 IDE의 지침에 따라 디버깅을 활성화합니다. 마지막으로, 확장 프로그램이나 [북마크릿](https://www.jetbrains.com/phpstorm/marklets/)을 사용하여 Xdebug를 실행하도록 브라우저를 구성하세요.

> [!WARNING]
> Xdebug로 인해 PHP가 상당히 느리게 실행됩니다. Xdebug를 비활성화하려면 Homestead 가상 머신 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 다시 시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작

웹 서버에 요청하는 기능 테스트를 디버깅할 때 사용자 지정 헤더나 쿠키를 통과하여 디버깅을 트리거하도록 테스트를 수정하는 것보다 디버깅을 자동 시작하는 것이 더 쉽습니다. Xdebug가 자동으로 시작되도록 하려면 Homestead 가상 머신 내에서 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하고 다음 구성을 추가하세요.

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 셸 별칭을 사용하세요.

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire를 사용하여 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청 및 CLI 애플리케이션을 프로파일링하는 서비스입니다. 콜 그래프와 타임라인에 프로필 데이터를 표시하는 대화형 사용자 인터페이스를 제공합니다. 최종 사용자에 대한 오버헤드 없이 개발, 스테이징 및 프로덕션에 사용하도록 구축되었습니다. 또한 Blackfire는 코드 및 `php.ini` 구성 설정에 대한 성능, 품질 및 보안 검사를 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 프로파일링 시나리오를 스크립트화하기 위해 Blackfire와 함께 작동할 수 있는 오픈 소스 웹 크롤링, 웹 테스트 및 웹 스크래핑 애플리케이션입니다.

Blackfire를 활성화하려면 Homestead 구성 파일에서 "features" 설정을 사용하십시오:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 자격 증명 및 클라이언트 자격 증명 [Blackfire 계정 필요](https://blackfire.io/signup). Blackfire는 CLI 도구 및 브라우저 확장을 포함하여 애플리케이션을 프로파일링하는 다양한 옵션을 제공합니다. [자세한 내용은 Blackfire 문서를 검토](https://blackfire.io/docs/php/integrations/laravel/index)하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스 (Network Interfaces)

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 구성합니다. 필요한 만큼 인터페이스를 구성할 수 있습니다.

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면 네트워크에 대한 `bridge` 설정을 구성하고 네트워크 유형을 `public_network`로 변경합니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 구성에서 `ip` 옵션을 제거하면 됩니다.

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

네트워크가 사용 중인 장치를 업데이트하려면 네트워크 구성에 `dev` 옵션을 추가할 수 있습니다. 기본 `dev` 값은 `eth0`입니다.

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장 (Extending Homestead)

Homestead 디렉토리의 루트에 있는 `after.sh` 스크립트를 사용하여 Homestead를 확장할 수 있습니다. 이 파일 내에서 가상 머신을 적절하게 구성하고 사용자 지정하는 데 필요한 셸 명령을 추가할 수 있습니다.

Homestead를 사용자 지정할 때 Ubuntu는 패키지의 원래 구성을 유지할 것인지 아니면 새 구성 파일로 덮어쓸 것인지 묻는 메시지를 표시할 수 있습니다. 이를 방지하려면 이전에 Homestead에서 작성한 구성을 덮어쓰지 않도록 패키지를 설치할 때 다음 명령을 사용해야 합니다.

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 지정

팀과 함께 Homestead를 사용할 때 개인 개발 스타일에 더 잘 맞도록 Homestead를 조정할 수 있습니다. 이를 수행하려면 Homestead 디렉토리(`Homestead.yaml` 파일이 포함된 동일한 디렉토리)의 루트에 `user-customizations.sh` 파일을 생성할 수 있습니다. 이 파일 내에서 원하는 대로 사용자 지정할 수 있습니다. 그러나 `user-customizations.sh`는 버전을 제어해서는 안 됩니다.

<a name="provider-specific-settings"></a>
## 프로바이더별 설정 (Provider Specific Settings)

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`로 구성합니다. 이를 통해 Homestead는 호스트 운영 체제의 DNS 설정을 사용할 수 있습니다. 이 동작을 재정의하려면 `Homestead.yaml` 파일에 다음 구성 옵션을 추가하세요.

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```
