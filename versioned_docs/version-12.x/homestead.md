# Laravel Homestead (Laravel Homestead)

- [소개](#introduction)
- [설치 및 설정](#installation-and-setup)
    - [첫 단계](#first-steps)
    - [Homestead 설정하기](#configuring-homestead)
    - [Nginx 사이트 설정하기](#configuring-nginx-sites)
    - [서비스 설정하기](#configuring-services)
    - [Vagrant 박스 실행하기](#launching-the-vagrant-box)
    - [프로젝트별 설치](#per-project-installation)
    - [선택적 기능 설치하기](#installing-optional-features)
    - [별칭(Aliases)](#aliases)
- [Homestead 업데이트](#updating-homestead)
- [일상적 사용](#daily-usage)
    - [SSH 연결](#connecting-via-ssh)
    - [추가 사이트 추가하기](#adding-additional-sites)
    - [환경 변수](#environment-variables)
    - [포트](#ports)
    - [PHP 버전](#php-versions)
    - [데이터베이스 연결](#connecting-to-databases)
    - [데이터베이스 백업](#database-backups)
    - [크론 스케줄 설정하기](#configuring-cron-schedules)
    - [Mailpit 설정하기](#configuring-mailpit)
    - [Minio 설정하기](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [환경 공유하기](#sharing-your-environment)
- [디버깅 및 프로파일링](#debugging-and-profiling)
    - [Xdebug로 웹 요청 디버깅하기](#debugging-web-requests)
    - [CLI 애플리케이션 디버깅](#debugging-cli-applications)
    - [Blackfire로 애플리케이션 프로파일링](#profiling-applications-with-blackfire)
- [네트워크 인터페이스](#network-interfaces)
- [Homestead 확장하기](#extending-homestead)
- [공급자별 설정](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## 소개

> [!WARNING]
> Laravel Homestead는 더 이상 적극적으로 유지 관리되지 않는 레거시 패키지입니다. 최신 대안으로는 [Laravel Sail](/docs/12.x/sail)을 사용할 수 있습니다.

Laravel은 로컬 개발 환경을 포함해 PHP 개발 경험 전체를 쾌적하게 만들기 위해 노력합니다. [Laravel Homestead](https://github.com/laravel/homestead)는 공식으로 제공되는 미리 구성된 Vagrant 박스로, 로컬 머신에 PHP, 웹 서버 또는 기타 서버 소프트웨어를 설치하지 않고도 훌륭한 개발 환경을 제공합니다.

[Vagrant](https://www.vagrantup.com)는 가상 머신을 관리하고 프로비저닝할 수 있는 간단하면서도 세련된 방법을 제공합니다. Vagrant 박스는 완전히 버릴 수 있는 일회용 환경입니다. 문제가 생기면 몇 분 만에 박스를 삭제하고 다시 만들 수 있습니다!

Homestead는 Windows, macOS, Linux 모든 시스템에서 실행 가능하며 Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node 등 훌륭한 Laravel 애플리케이션 개발에 필요한 모든 소프트웨어를 포함합니다.

> [!WARNING]
> Windows를 사용하는 경우 하드웨어 가상화(VT-x)를 BIOS에서 활성화해야 할 수 있습니다. UEFI 시스템에서 Hyper-V를 사용하는 경우 VT-x에 접근하기 위해 Hyper-V를 비활성화해야 할 수도 있습니다.

<a name="included-software"></a>
### 포함된 소프트웨어

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

</div>

<a name="optional-software"></a>
### 선택적 소프트웨어

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
- Trader <small>(PHP extension)</small>
- Webdriver & Laravel Dusk Utilities

</div>

<a name="installation-and-setup"></a>
## 설치 및 설정

<a name="first-steps"></a>
### 첫 단계

Homestead 환경을 실행하기 전에, [Vagrant](https://developer.hashicorp.com/vagrant/downloads)를 설치해야 하며 다음 중 하나의 지원되는 공급자를 설치해야 합니다:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)

이 소프트웨어 패키지들은 모두 주요 운영체제에 맞는 시각적 설치 프로그램을 제공합니다.

Parallels 공급자를 사용하려면, [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 별도로 설치해야 합니다. 이 플러그인은 무료입니다.

<a name="installing-homestead"></a>
#### Homestead 설치하기

호스트 머신에 Homestead 저장소를 클론하여 설치할 수 있습니다. Homestead 가상 머신이 모든 Laravel 애플리케이션의 호스트 역할을 하므로, 홈 디렉터리 안에 `Homestead` 폴더로 클론하는 것을 권장합니다. 이 문서 전체에서는 이 디렉터리를 “Homestead 디렉터리”라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```

Laravel Homestead 저장소를 클론한 후 `release` 브랜치로 전환하세요. 이 브랜치는 항상 최신 안정 릴리스를 포함합니다:

```shell
cd ~/Homestead

git checkout release
```

그 다음, `bash init.sh` 명령을 실행하여 `Homestead.yaml` 설정 파일을 생성하세요. 이 파일에서 Homestead 설치에 필요한 모든 설정을 구성합니다. 파일은 Homestead 디렉터리에 생성됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

<a name="configuring-homestead"></a>
### Homestead 설정하기

<a name="setting-your-provider"></a>
#### 공급자(provider) 설정하기

`Homestead.yaml` 파일의 `provider` 키는 사용할 Vagrant 공급자를 지정합니다: `virtualbox` 또는 `parallels` 중 하나를 선택합니다.

```
provider: virtualbox
```

> [!WARNING]
> Apple Silicon 사용자는 Parallels 공급자를 반드시 사용해야 합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 설정하기

`Homestead.yaml` 파일의 `folders` 속성은 Homestead 환경과 공유할 폴더 목록입니다. 이 폴더 내에서 파일이 변경되면 로컬 머신과 Homestead 가상 환경 간에 자동 동기화됩니다. 필요한 만큼 공유 폴더를 설정할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```

> [!WARNING]
> Windows 사용자는 `~/` 경로 구문을 사용하지 말고, 프로젝트의 전체 경로 예: `C:\Users\user\Code\project1`를 사용해야 합니다.

항상 각 애플리케이션에 대해 개별 폴더 매핑을 설정해야 하며, 여러 애플리케이션이 모여 있는 하나의 큰 디렉터리를 매핑하는 것은 피해야 합니다. 폴더를 매핑하면 가상 머신이 해당 폴더 안의 *모든* 파일에 대한 디스크 IO를 추적해야 하기 때문에, 파일이 많을 경우 성능 저하가 발생할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```

> [!WARNING]
> Homestead 사용 시 절대로 `.` (현재 디렉터리)를 마운트하지 마세요. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않아 선택적 기능이 작동하지 않고 프로비저닝 시 예상하지 못한 문제가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 활성화하려면 폴더 매핑에 `type` 옵션을 추가하면 됩니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```

> [!WARNING]
> Windows에서 NFS를 사용할 경우, [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인 설치를 권장합니다. 이 플러그인은 Homestead 가상 머신 내 파일 및 디렉터리의 올바른 사용자/그룹 권한을 유지합니다.

또한 Vagrant의 [Synced Folders](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)에서 지원하는 옵션을 `options` 키 아래에 나열하여 전달할 수 있습니다:

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
### Nginx 사이트 설정하기

Nginx에 익숙하지 않아도 걱정할 필요 없습니다. `Homestead.yaml` 파일의 `sites` 속성은 쉽게 "도메인"을 Homestead 환경 내 폴더에 매핑할 수 있게 합니다. `Homestead.yaml`에는 샘플 사이트 설정이 포함되어 있습니다. 여러 사이트를 자유롭게 추가해 사용할 수 있으며, Homestead는 여러분이 작업하는 모든 Laravel 애플리케이션에 편리한 가상 환경을 제공합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```

`sites` 속성을 변경한 후에는 가상 머신 내 Nginx 구성을 업데이트하기 위해 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

> [!WARNING]
> Homestead 스크립트는 최대한 아이덴포턴트(idempotent, 반복 실행 시 같은 결과)하게 설계되었지만, 프로비저닝에 문제가 생기면 `vagrant destroy && vagrant up` 명령어로 머신을 파괴 후 다시 구축하는 것을 권장합니다.

<a name="hostname-resolution"></a>
#### 호스트명(Hostname) 해석

Homestead는 자동 호스트 해석을 위한 `mDNS`를 사용하여 호스트명을 게시합니다. `Homestead.yaml` 파일에 `hostname: homestead`를 설정하면, 호스트는 `homestead.local`에서 사용 가능합니다. macOS, iOS, 그리고 대부분 리눅스 데스크톱 배포판은 기본적으로 `mDNS`를 지원합니다. Windows 사용자는 [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US)를 설치해야 합니다.

자동 호스트명 기능은 [프로젝트별 설치](#per-project-installation)에서 가장 잘 작동합니다. 한 대의 Homestead 인스턴스에 여러 사이트를 호스팅하는 경우, `hosts` 파일에 사이트 도메인을 추가해 해당 요청이 Homestead 가상 머신으로 들어오도록 해야 합니다. macOS 및 리눅스에서 이 파일은 `/etc/hosts`에, Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 있습니다. 예시:

```text
192.168.56.56  homestead.test
```

IP 주소는 `Homestead.yaml` 파일에 설정된 것과 일치해야 합니다. `hosts` 파일에 도메인을 추가하고 Vagrant 박스를 실행하면 웹 브라우저를 통해 다음과 같이 사이트에 접속할 수 있습니다:

```shell
http://homestead.test
```

<a name="configuring-services"></a>
### 서비스 설정하기

Homestead는 기본적으로 여러 서비스를 시작하지만, 프로비저닝 중 활성화/비활성화할 서비스를 사용자가 직접 설정할 수 있습니다. 예를 들어, PostgreSQL을 활성화하고 MySQL을 비활성화하려면 `Homestead.yaml` 파일에서 `services` 옵션을 다음과 같이 수정합니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```

`enabled`와 `disabled` 목록에 따라 명시된 서비스가 시작 또는 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 실행하기

`Homestead.yaml` 파일 편집이 완료되면 Homestead 디렉터리에서 `vagrant up` 명령을 실행하세요. Vagrant가 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동 구성합니다.

가상 머신을 삭제하려면 `vagrant destroy` 명령을 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역 설치하고 모든 프로젝트에서 동일한 Homestead 가상 머신을 공유하는 대신, 각 프로젝트마다 별도의 Homestead 인스턴스를 구성할 수도 있습니다. 이렇게 설치하면 프로젝트 저장소에 `Vagrantfile`을 포함시켜 다른 개발자가 저장소 클론 후 즉시 `vagrant up`으로 실행할 수 있어 편리합니다.

Composer 패키지 관리자를 사용해 프로젝트 내에 Homestead를 설치하려면 다음 명령을 실행합니다:

```shell
composer require laravel/homestead --dev
```

설치 후 Homestead의 `make` 명령을 실행하면 프로젝트 루트에 `Vagrantfile`과 `Homestead.yaml`이 생성됩니다. `make` 명령은 `Homestead.yaml` 파일의 `sites`와 `folders` 지시어도 자동 구성합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```

그 후 터미널에서 `vagrant up` 명령을 실행하고 브라우저에서 `http://homestead.test`로 프로젝트에 접속하세요. 자동 [호스트명 해석](#hostname-resolution)을 사용하지 않는 경우, `/etc/hosts` 파일에 `homestead.test` 또는 원하는 도메인을 추가해야 하는 점을 잊지 마세요.

<a name="installing-optional-features"></a>
### 선택적 기능 설치하기

선택적 소프트웨어는 `Homestead.yaml` 파일 내 `features` 옵션을 통해 설치할 수 있습니다. 대부분의 기능은 불리언 값으로 활성화하거나 비활성화하지만, 일부는 여러 설정 옵션을 허용합니다:

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

Elasticsearch의 지원 버전을 명시할 수 있으며, 정확한 버전(major.minor.patch) 번호여야 합니다. 기본 설치는 'homestead'라는 이름의 클러스터를 생성합니다. Elasticsearch가 운영 체제 메모리의 절반 이상을 사용하지 않도록 Homestead 가상 머신의 메모리가 충분한지 확인하세요.

> [!NOTE]
> 자세한 설정 방법은 [Elasticsearch 문서](https://www.elastic.co/guide/en/elasticsearch/reference/current)를 참고하세요.

<a name="mariadb"></a>
#### MariaDB

MariaDB를 활성화하면 MySQL이 제거되고 MariaDB가 설치됩니다. MariaDB는 일반적으로 MySQL과 호환되는 대체품이므로, Laravel 애플리케이션 데이터베이스 설정에서는 여전히 `mysql` 데이터베이스 드라이버를 사용해야 합니다.

<a name="mongodb"></a>
#### MongoDB

기본 MongoDB 설치는 데이터베이스 사용자 이름을 `homestead`로, 비밀번호를 `secret`으로 설정합니다.

<a name="neo4j"></a>
#### Neo4j

Neo4j 기본 설치는 데이터베이스 사용자 이름을 `homestead`, 비밀번호를 `secret`으로 설정합니다. Neo4j 브라우저에 접근하려면 웹 브라우저에서 `http://homestead.test:7474`에 접속하세요. Neo4j 클라이언트용 포트인 `7687`(Bolt), `7474`(HTTP), `7473`(HTTPS)이 준비되어 있습니다.

<a name="aliases"></a>
### 별칭(Aliases)

Homestead 가상 머신에 Bash 별칭을 추가하려면 Homestead 디렉터리 내 `aliases` 파일을 수정하세요:

```shell
alias c='clear'
alias ..='cd ..'
```

`aliases` 파일을 수정한 후에는 `vagrant reload --provision` 명령을 실행해 가상 머신을 다시 프로비저닝해야 새 별칭이 적용됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

업데이트를 시작하기 전에 현재 가상 머신을 먼저 제거하세요. Homestead 디렉터리에서 다음 명령을 실행합니다:

```shell
vagrant destroy
```

다음으로 Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론한 경우, 클론한 위치에서 다음 명령을 실행하세요:

```shell
git fetch

git pull origin release
```

이 명령들이 GitHub 저장소에서 최신 Homestead 코드를 받아오고 태그를 가져와 최신 태그 릴리스를 체크아웃합니다. 최신 안정 릴리스 버전은 Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json`으로 Homestead를 설치한 경우, `"laravel/homestead": "^12"`가 `composer.json`에 포함되어 있는지 확인하고 의존성 업데이트를 실행하세요:

```shell
composer update
```

그 다음 `vagrant box update` 명령으로 Vagrant 박스를 업데이트합니다:

```shell
vagrant box update
```

Vagrant 박스를 업데이트한 이후, Homestead 구성 파일 업데이트를 위해 Homestead 디렉터리에서 `bash init.sh` 명령을 실행하세요. 기존의 `Homestead.yaml`, `after.sh`, `aliases` 파일을 덮어쓸지 묻습니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```

마지막으로, 최신 Vagrant 설치본을 활용하려면 Homestead 가상 머신을 다시 생성해야 합니다:

```shell
vagrant up
```

<a name="daily-usage"></a>
## 일상적 사용

<a name="connecting-via-ssh"></a>
### SSH 연결

Homestead 디렉터리에서 `vagrant ssh` 명령어를 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가하기

Homestead 환경이 프로비저닝되어 실행 중일 때, 다른 Laravel 프로젝트용 Nginx 사이트를 추가할 수 있습니다. 하나의 Homestead 환경에서 여러 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트를 추가하려면 `Homestead.yaml` 파일에 사이트를 추가합니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```

> [!WARNING]
> 사이트를 추가하기 전에 해당 프로젝트 폴더에 대한 [폴더 매핑](#configuring-shared-folders)을 올바르게 설정했는지 반드시 확인하세요.

만약 Vagrant가 "hosts" 파일을 자동으로 관리하지 않는다면, 파일에 새로운 사이트 도메인을 직접 추가해야 합니다. macOS, 리눅스에서는 `/etc/hosts`, Windows에서는 `C:\Windows\System32\drivers\etc\hosts` 위치에 있습니다:

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```

사이트를 추가한 후에는 Homestead 디렉터리에서 `vagrant reload --provision` 명령을 실행해 변경 사항을 적용하세요.

<a name="site-types"></a>
#### 사이트 타입

Homestead에서는 Laravel 기반이 아닌 프로젝트도 쉽게 실행할 수 있도록 여러 "사이트 타입"을 지원합니다. 예를 들어, Statamic 애플리케이션을 Homestead에 추가할 때 `statamic` 타입을 다음과 같이 명시할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```

사용 가능한 사이트 타입은 다음과 같습니다: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel` (기본값), `proxy` (nginx 용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`.

<a name="site-parameters"></a>
#### 사이트 파라미터

`params` 사이트 지시어를 통해 Nginx의 추가 `fastcgi_param` 값을 사이트별로 설정할 수 있습니다:

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

글로벌 환경 변수를 `Homestead.yaml` 파일에 추가할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```

`Homestead.yaml` 수정 후에는 `vagrant reload --provision` 명령을 실행해 가상 머신을 다시 프로비저닝하세요. 이렇게 하면 설치된 모든 PHP 버전에 대해 PHP-FPM 설정이 업데이트되고 `vagrant` 사용자 환경도 갱신됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음과 같은 포트가 Homestead 환경으로 포워딩됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 &rarr; 80 포트로 포워딩
- **HTTPS:** 44300 &rarr; 443 포트로 포워딩

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 포워딩 설정

원한다면 `Homestead.yaml` 파일 내의 `ports` 설정을 사용해 추가 포트를 Vagrant 박스로 포워딩할 수 있습니다. 파일 수정 후 `vagrant reload --provision` 명령으로 적용하세요:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```

추가로 매핑할 수 있는 Homestead 서비스 포트 예시는 다음과 같습니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; 22
- **ngrok UI:** 4040 &rarr; 4040
- **MySQL:** 33060 &rarr; 3306
- **PostgreSQL:** 54320 &rarr; 5432
- **MongoDB:** 27017 &rarr; 27017
- **Mailpit:** 8025 &rarr; 8025
- **Minio:** 9600 &rarr; 9600

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 같은 가상 머신에서 여러 PHP 버전을 실행할 수 있습니다. `Homestead.yaml` 파일에서 각 사이트 별로 사용할 PHP 버전을 지정할 수 있습니다. 지원하는 PHP 버전은 다음과 같습니다: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3" (기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```

[Homestead 가상 머신 내에서](#connecting-via-ssh), CLI에서 지원하는 PHP 버전을 다음과 같이 사용할 수 있습니다:

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

기본 PHP CLI 버전을 변경하려면 Homestead 가상 머신 내에서 다음 명령어를 실행하세요:

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
### 데이터베이스 연결

MySQL과 PostgreSQL 모두 기본적으로 `homestead` 데이터베이스가 생성되어 있습니다. 호스트 머신의 데이터베이스 클라이언트에서 MySQL 또는 PostgreSQL에 접속하려면 각각 포트 `33060`(MySQL), `54320`(PostgreSQL)으로 `127.0.0.1`에 연결하세요. 두 데이터베이스의 사용자 이름과 비밀번호는 모두 `homestead` / `secret`입니다.

> [!WARNING]
> 호스트 머신에서 데이터베이스에 연결할 때에만 위에 명시된 비표준 포트를 사용해야 합니다. Laravel 애플리케이션 내부(가상 머신 내)에서는 기본 포트인 3306(MySQL), 5432(PostgreSQL)을 사용하세요.

<a name="database-backups"></a>
### 데이터베이스 백업

Homestead는 가상 머신이 파괴될 때 데이터베이스를 자동으로 백업할 수 있습니다. 이 기능을 사용하려면 Vagrant 2.1.0 이상이 필요하며, 구버전 사용 시 `vagrant-triggers` 플러그인을 설치해야 합니다. 자동 백업을 활성화하려면 `Homestead.yaml` 파일에 다음을 추가하세요:

```yaml
backup: true
```

설정 후, `vagrant destroy` 명령 실행 시 데이터베이스는 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉터리에 내보내집니다. 이 경로는 Homestead 설치 폴더에 위치하거나 [프로젝트별 설치](#per-project-installation) 시 프로젝트 루트에 위치합니다.

<a name="configuring-cron-schedules"></a>
### 크론 스케줄 설정하기

Laravel은 [크론 작업 스케줄링](/docs/12.x/scheduling)을 간편하게 지원합니다. 모든 스케줄 작업은 단일 `schedule:run` Artisan 명령으로 처리되며, 매 분마다 실행되도록 설정할 수 있습니다. `schedule:run` 명령은 `routes/console.php` 파일에 정의된 작업 스케줄을 참고해 실행할 작업을 결정합니다.

Homestead 사이트에서 `schedule:run` 명령을 실행하려면, 사이트 정의 시 `schedule` 옵션을 `true`로 설정하세요:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```

해당 사이트의 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉터리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 설정하기

[Mailpit](https://github.com/axllent/mailpit)은 발신 이메일을 가로채 실제 발송하지 않고 내용을 확인할 수 있게 해줍니다. 사용하려면 애플리케이션의 `.env` 파일을 다음과 같이 설정합니다:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```

Mailpit이 설정되면 `http://localhost:8025`에서 대시보드에 접속할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 설정하기

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 제공하는 오픈 소스 객체 저장 서버입니다. Minio를 설치하려면 `Homestead.yaml` 파일의 [features](#installing-optional-features) 섹션에 다음을 추가하세요:

```
minio: true
```

기본 포트는 9600이며, `http://localhost:9600`에서 Minio 관리 콘솔에 접속할 수 있습니다. 기본 액세스 키는 `homestead`, 기본 비밀 키는 `secretkey`입니다. Minio 접속 시 항상 `us-east-1` 리전을 사용해야 합니다.

Minio 사용을 위해 `.env` 파일에 다음 옵션을 포함하세요:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```

Minio 기반 "S3" 버킷을 프로비저닝하려면 `Homestead.yaml`에 `buckets` 지시어를 추가하고 Define하세요. 완료 후 `vagrant reload --provision` 명령을 실행해 적용합니다:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```

`policy` 값으로는 `none`, `download`, `upload`, `public`이 지원됩니다.

<a name="laravel-dusk"></a>
### Laravel Dusk

Homestead 안에서 [Laravel Dusk](/docs/12.x/dusk) 테스트를 실행하려면 Homestead 설정에서 [webdriver 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```

`webdriver` 기능 활성화 후에는 터미널에서 `vagrant reload --provision` 명령을 실행하세요.

<a name="sharing-your-environment"></a>
### 환경 공유하기

현재 작업 중인 환경을 동료나 고객과 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령을 갖추고 있지만, `Homestead.yaml`에 여러 사이트가 설정된 경우 이 명령은 작동하지 않습니다.

이 문제를 해결하기 위해 Homestead는 자체 `share` 명령을 제공합니다. 사용하려면 [SSH로 Homestead 가상 머신에 접속](#connecting-via-ssh)한 후 다음 명령을 실행합니다. `homestead.test`는 공유하려는 사이트 이름으로 변경할 수 있습니다:

```shell
share homestead.test
```

명령 실행 후 Ngrok 화면이 나타나며 활동 로그와 공유 사이트의 공개 URL을 확인할 수 있습니다. 커스텀 리전, 서브도메인 등 Ngrok 옵션을 포함하려면 다음과 같이 명령어에 추가하세요:

```shell
share homestead.test -region=eu -subdomain=laravel
```

HTTPS로 공유할 필요가 있다면 `share` 대신 `sshare` 명령을 사용하세요.

> [!WARNING]
> Vagrant는 근본적으로 보안이 취약하며 `share` 명령 실행 시 가상 머신이 인터넷에 노출됩니다.

<a name="debugging-and-profiling"></a>
## 디버깅 및 프로파일링

<a name="debugging-web-requests"></a>
### Xdebug로 웹 요청 디버깅하기

Homestead는 [Xdebug](https://xdebug.org)를 이용한 스텝 디버깅을 지원합니다. 예를 들어, 브라우저에서 페이지를 호출하면 PHP가 IDE와 연결되어 실행 중인 코드를 검사하고 수정할 수 있습니다.

기본적으로 Xdebug는 이미 활성화되어 연결을 기다리고 있습니다. CLI에서 Xdebug를 활성화하려면 Homestead 가상 머신 내부에서 `sudo phpenmod xdebug` 명령을 실행하세요. 그 후 IDE 지침에 따라 디버깅을 활성화하고, 브라우저에서는 확장 프로그램이나 [북마클릿(bookmarklet)](https://www.jetbrains.com/phpstorm/marklets/)을 사용해 Xdebug 트리거를 설정하세요.

> [!WARNING]
> Xdebug는 PHP 실행 속도를 상당히 저하시킵니다. 비활성화하려면 Homestead 내에서 `sudo phpdismod xdebug`를 실행하고 FPM 서비스를 재시작하세요.

<a name="autostarting-xdebug"></a>
#### Xdebug 자동 시작 설정

웹서버에 대한 요청 테스트 중 기능 테스트를 디버깅할 때, 디버깅을 자동으로 시작하는 것이 테스트를 수정해 커스텀 헤더나 쿠키를 전달하는 것보다 편리합니다. 이를 위해 Homestead 가상 머신 내 `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` 파일을 수정하여 다음 설정을 추가하세요:

```ini
; Homestead.yaml에 다른 서브넷 IP가 있을 경우 IP가 다를 수 있습니다...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```

<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 내에서 `xphp` 셸 별칭을 사용하세요:

```shell
xphp /path/to/script
```

<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션 프로파일링을 위한 서비스입니다. 인터랙티브 UI를 통해 호출 그래프와 타임라인으로 프로파일 데이터를 시각화하며, 개발, 스테이징, 운영 환경에서 그대로 사용할 수 있고 최종 사용자에 부담을 주지 않습니다. 또한 Blackfire는 코드와 `php.ini` 설정에 대해 성능, 품질, 보안 점검도 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 조합해 프로파일링 시나리오를 스크립트로 작성할 수 있는 오픈 소스 웹 크롤링, 웹 테스트, 스크래핑 도구입니다.

Blackfire를 활성화하려면 Homestead 설정 파일의 "features" 옵션에 다음과 같이 입력합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```

Blackfire 서버 자격 정보와 클라이언트 자격 정보는 [Blackfire 계정](https://blackfire.io/signup)이 필요합니다. CLI 도구와 브라우저 확장 등 다양한 프로파일링 옵션을 제공합니다. 자세한 내용은 [Blackfire 문서](https://blackfire.io/docs/php/integrations/laravel/index)를 참고하세요.

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 설정합니다. 필요한 만큼 인터페이스를 설정할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```

[브리지 연결](https://developer.hashicorp.com/vagrant/docs/networking/public_network)을 활성화하려면 `bridge` 설정을 추가하고 네트워크 타입을 `public_network`으로 변경하세요:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```

[DHCP](https://developer.hashicorp.com/vagrant/docs/networking/public_network#dhcp)를 활성화하려면 `ip` 옵션을 삭제하면 됩니다:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```

사용할 네트워크 장치를 바꾸려면, `dev` 옵션에 장치명을 지정합니다. 기본값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```

<a name="extending-homestead"></a>
## Homestead 확장하기

Homestead 디렉터리 루트에 있는 `after.sh` 스크립트를 이용해 Homestead를 확장할 수 있습니다. 이 파일 안에 가상 머신을 적절히 커스터마이징하고 설정하기 위한 셸 명령어를 추가하세요.

Ubuntu 패키지 설치 시 기본 구성 파일을 덮어쓰지 않고 유지하려면, 다음과 같은 옵션을 적용해 패키지를 설치하는 것을 권장합니다:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```

<a name="user-customizations"></a>
### 사용자 커스터마이징

팀 내에서 Homestead를 사용할 때 개인 개발 스타일에 맞게 Homestead를 조정하고 싶다면, Homestead 디렉터리 루트( `Homestead.yaml` 파일과 같은 디렉터리)에 `user-customizations.sh` 파일을 생성하세요. 이 파일 안에 원하는 모든 커스터마이징을 추가할 수 있지만, 해당 파일은 버전 관리 대상에서 제외해야 합니다.

<a name="provider-specific-settings"></a>
## 공급자별 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`으로 구성합니다. 이 설정은 Homestead가 호스트 운영체제의 DNS 설정을 사용하도록 합니다. 이를 변경하고 싶다면 `Homestead.yaml` 파일에 다음 설정을 추가하세요:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```