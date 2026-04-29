# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [Sail 이미지 다시 빌드하기](#rebuilding-sail-images)
    - [셸 별칭 설정하기](#configuring-a-shell-alias)
- [Sail 시작 및 중지](#starting-and-stopping-sail)
- [명령어 실행](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [파일 스토리지](#file-storage)
- [테스트 실행](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [이메일 미리 보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유](#sharing-your-site)
- [Xdebug로 디버깅하기](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 가벼운 명령줄 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축할 수 있는 좋은 출발점을 제공합니다.

핵심적으로 Sail은 프로젝트 루트에 저장되는 `compose.yaml` 파일과 `sail` 스크립트로 이루어져 있습니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너와 상호작용할 수 있는 편리한 메서드를 갖춘 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)를 통해)를 지원합니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Composer 패키지 관리자를 사용하여 Sail을 설치할 수 있습니다.

```shell
composer require laravel/sail --dev
```

Sail을 설치한 후에는 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 게시하고, Docker 서비스에 연결하는 데 필요한 환경 변수로 `.env` 파일을 수정합니다.

```shell
php artisan sail:install
```

마지막으로 Sail을 시작할 수 있습니다. Sail 사용법을 계속 배우려면 이 문서의 나머지 내용을 계속 읽어보십시오.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용 중이라면 다음 명령어를 실행하여 `default` Docker 컨텍스트를 사용해야 합니다. `docker context use default`. 또한 컨테이너 안에서 파일 권한 오류가 발생하는 경우 `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 설정해야 할 수 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 추가 서비스를 더하고 싶다면 `sail:add` Artisan 명령어를 실행할 수 있습니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 안에서 개발하고 싶다면 `sail:install` 명령어에 `--devcontainer` 옵션을 제공할 수 있습니다. `--devcontainer` 옵션은 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 루트에 게시하도록 지시합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 다시 빌드하기

때로는 이미지의 모든 패키지와 소프트웨어가 최신 상태인지 확인하기 위해 Sail 이미지를 완전히 다시 빌드하고 싶을 수 있습니다. `build` 명령어를 사용하여 이를 수행할 수 있습니다.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭 설정하기

기본적으로 Sail 명령어는 모든 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용하여 호출합니다.

```shell
./vendor/bin/sail up
```

하지만 Sail 명령어를 실행할 때마다 `vendor/bin/sail`을 반복해서 입력하는 대신, Sail 명령어를 더 쉽게 실행할 수 있도록 셸 별칭을 설정할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있게 하려면 홈 디렉터리에 있는 `~/.zshrc` 또는 `~/.bashrc` 같은 셸 설정 파일에 추가한 뒤 셸을 다시 시작하면 됩니다.

셸 별칭을 설정한 후에는 단순히 `sail`을 입력하여 Sail 명령어를 실행할 수 있습니다. 이 문서의 나머지 예제는 이 별칭을 설정했다고 가정합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일은 Laravel 애플리케이션 구축을 돕기 위해 함께 동작하는 다양한 Docker 컨테이너를 정의합니다. 이러한 각 컨테이너는 `compose.yaml` 파일의 `services` 설정 안에 있는 항목입니다. `laravel.test` 컨테이너는 애플리케이션을 제공하는 기본 애플리케이션 컨테이너입니다.

Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인해야 합니다. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행해야 합니다.

```shell
sail up
```

모든 Docker 컨테이너를 백그라운드에서 시작하려면 Sail을 "detached" 모드로 시작할 수 있습니다.

```shell
sail up -d
```

애플리케이션 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 프로젝트에 접근할 수 있습니다. http://localhost.

모든 컨테이너를 중지하려면 Control + C를 눌러 컨테이너 실행을 중지하면 됩니다. 또는 컨테이너가 백그라운드에서 실행 중이라면 `stop` 명령어를 사용할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 안에서 실행되며 로컬 컴퓨터와 격리됩니다. 하지만 Sail은 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어 등 애플리케이션을 대상으로 다양한 명령어를 실행할 수 있는 편리한 방법을 제공합니다.

**Laravel 문서를 읽다 보면 Sail을 언급하지 않는 Composer, Artisan, Node / NPM 명령어 예제를 자주 보게 됩니다.** 해당 예제들은 이러한 도구가 로컬 컴퓨터에 설치되어 있다고 가정합니다. 로컬 Laravel 개발 환경으로 Sail을 사용하고 있다면 해당 명령어를 Sail을 통해 실행해야 합니다.

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령어를 사용하여 실행할 수 있습니다. 물론 이 명령어들은 애플리케이션에 설정된 PHP 버전을 사용하여 실행됩니다. Laravel Sail에서 사용할 수 있는 PHP 버전에 대해 더 알아보려면 [PHP 버전 문서](#sail-php-versions)를 참고하십시오.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령어를 사용하여 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan` 명령어를 사용하여 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 명령어는 `node` 명령어를 사용하여 실행할 수 있으며, NPM 명령어는 `npm` 명령어를 사용하여 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다.

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

이미 알아차렸을 수 있듯이, 애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다.

또한 MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스를 생성합니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수 값을 사용해 이름이 정해지며 로컬 개발용입니다. 두 번째 데이터베이스는 `testing`이라는 전용 테스트 데이터베이스로, 테스트가 개발 데이터에 영향을 주지 않도록 보장합니다.

컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정하여 애플리케이션 안에서 MySQL 인스턴스에 연결할 수 있습니다.

로컬 머신에서 애플리케이션의 MySQL 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근할 수 있으며, 접근 자격 증명은 `DB_USERNAME` 및 `DB_PASSWORD` 환경 변수 값과 일치합니다. 또는 `root` 사용자로 연결할 수도 있으며, 이 경우에도 `DB_PASSWORD` 환경 변수 값을 비밀번호로 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) 같은 Atlas 기능과 함께 MongoDB 문서 데이터베이스를 제공하는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 포함됩니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다.

컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하여 애플리케이션 안에서 MongoDB 인스턴스에 연결할 수 있습니다. 인증은 기본적으로 비활성화되어 있지만, `mongodb` 컨테이너를 시작하기 전에 `MONGODB_USERNAME` 및 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 그런 다음 연결 문자열에 자격 증명을 추가하십시오.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB를 애플리케이션과 매끄럽게 통합하려면 [MongoDB에서 관리하는 공식 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 머신에서 애플리케이션의 MongoDB 데이터베이스에 연결하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 그래픽 인터페이스를 사용할 수 있습니다. 기본적으로 MongoDB 데이터베이스는 `localhost`의 `27017` 포트에서 접근할 수 있습니다.

<a name="redis"></a>
### Redis

애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 Redis 인스턴스에 저장된 데이터가 유지됩니다. 컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `redis`로 설정하여 애플리케이션 안에서 Redis 인스턴스에 연결할 수 있습니다.

로컬 머신에서 애플리케이션의 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택하면 애플리케이션의 `compose.yaml` 파일에 [Valkey](https://valkey.io/) 항목이 포함됩니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 Valkey 인스턴스에 저장된 데이터가 유지됩니다. 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `valkey`로 설정하여 애플리케이션에서 이 컨테이너에 연결할 수 있습니다.

로컬 머신에서 애플리케이션의 Valkey 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Valkey 데이터베이스는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [Laravel Scout](/docs/13.x/scout)와 통합되는 강력한 검색 엔진 항목이 포함됩니다. 컨테이너를 시작한 후에는 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정하여 애플리케이션 안에서 Meilisearch 인스턴스에 연결할 수 있습니다.

로컬 머신에서는 웹 브라우저에서 `http://localhost:7700`으로 이동하여 Meilisearch의 웹 기반 관리 패널에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [Laravel Scout](/docs/13.x/scout#typesense)와 기본적으로 통합되는 매우 빠른 오픈 소스 검색 엔진 항목이 포함됩니다. 컨테이너를 시작한 후에는 다음 환경 변수를 설정하여 애플리케이션 안에서 Typesense 인스턴스에 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 머신에서는 `http://localhost:8108`을 통해 Typesense의 API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 애플리케이션을 실행할 때 파일 저장소로 Amazon S3를 사용할 계획이라면 Sail 설치 시 [RustFS](https://rustfs.com) 서비스를 설치하는 것이 좋습니다. RustFS는 S3 호환 API를 제공하므로, 프로덕션 S3 환경에 "test" 스토리지 버킷을 만들지 않고도 Laravel의 `s3` 파일 스토리지 드라이버를 사용하여 로컬에서 개발할 수 있습니다. Sail 설치 시 RustFS를 설치하도록 선택하면 RustFS 설정 섹션이 애플리케이션의 `compose.yaml` 파일에 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크에 대한 디스크 설정이 포함되어 있습니다. Amazon S3와 상호작용하기 위해 이 디스크를 사용하는 것뿐만 아니라, 관련 설정을 제어하는 환경 변수를 수정하는 것만으로 RustFS 같은 S3 호환 파일 스토리지 서비스와 상호작용하는 데에도 이 디스크를 사용할 수 있습니다. 예를 들어 RustFS를 사용할 때 파일 시스템 환경 변수 설정은 다음과 같이 정의해야 합니다.

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
## 테스트 실행 (Running Tests)

Laravel은 기본적으로 훌륭한 테스트 지원을 제공하며, Sail의 `test` 명령어를 사용하여 애플리케이션의 [기능 테스트와 단위 테스트](/docs/13.x/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 허용하는 모든 CLI 옵션도 `test` 명령어에 전달할 수 있습니다.

```shell
sail test

sail test --group orders
```

Sail `test` 명령어는 `test` Artisan 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

기본적으로 Sail은 전용 `testing` 데이터베이스를 생성하여 테스트가 데이터베이스의 현재 상태에 영향을 주지 않도록 합니다. 기본 Laravel 설치에서는 Sail이 테스트 실행 시 이 데이터베이스를 사용하도록 `phpunit.xml` 파일도 설정합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/13.x/dusk)는 표현력이 좋고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 로컬 컴퓨터에 Selenium이나 다른 도구를 설치하지 않고도 이러한 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스를 주석 해제하십시오.

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

다음으로 애플리케이션의 `compose.yaml` 파일에 있는 `laravel.test` 서비스에 `selenium`에 대한 `depends_on` 항목이 있는지 확인하십시오.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

마지막으로 Sail을 시작하고 `dusk` 명령어를 실행하여 Dusk 테스트 스위트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용하기

로컬 머신에 Apple Silicon 칩이 포함되어 있다면 `selenium` 서비스는 `selenium/standalone-chromium` 이미지를 사용해야 합니다.

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
## 이메일 미리 보기 (Previewing Emails)

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit)에 대한 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션이 보내는 이메일을 가로채고, 브라우저에서 이메일 메시지를 미리 볼 수 있는 편리한 웹 인터페이스를 제공합니다. Sail을 사용할 때 Mailpit의 기본 호스트는 `mailpit`이며 1025 포트를 통해 사용할 수 있습니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중이면 다음 주소에서 Mailpit 웹 인터페이스에 접근할 수 있습니다. http://localhost:8025

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

때로는 애플리케이션 컨테이너 안에서 Bash 세션을 시작하고 싶을 수 있습니다. `shell` 명령어를 사용하여 애플리케이션 컨테이너에 연결할 수 있으며, 이를 통해 컨테이너 안에서 파일과 설치된 서비스를 살펴보고 임의의 셸 명령어를 실행할 수 있습니다.

```shell
sail shell

sail root-shell
```

새 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행할 수 있습니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.5, 8.4, 8.3, 8.2, 8.1 또는 PHP 8.0을 통해 애플리케이션을 제공하는 것을 지원합니다. Sail에서 사용하는 기본 PHP 버전은 현재 PHP 8.5입니다. 애플리케이션을 제공하는 데 사용되는 PHP 버전을 변경하려면 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 정의를 업데이트해야 합니다.

```yaml
# PHP 8.5
context: ./vendor/laravel/sail/runtimes/8.5

# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```
또한 애플리케이션에서 사용하는 PHP 버전을 반영하도록 `image` 이름을 업데이트할 수도 있습니다. 이 옵션도 애플리케이션의 `compose.yaml` 파일에 정의되어 있습니다.

```yaml
image: sail-8.2/app
```

애플리케이션의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 24를 설치합니다. 이미지를 빌드할 때 설치되는 Node 버전을 변경하려면 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 정의를 업데이트하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

애플리케이션의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

때로는 동료에게 사이트를 미리 보여주거나 애플리케이션의 Webhook 연동을 테스트하기 위해 사이트를 공개적으로 공유해야 할 수 있습니다. 사이트를 공유하려면 `share` 명령어를 사용할 수 있습니다. 이 명령어를 실행하면 애플리케이션에 접근하는 데 사용할 수 있는 임의의 `laravel-sail.site` URL이 발급됩니다.

```shell
sail share
```

`share` 명령어로 사이트를 공유할 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 애플리케이션의 신뢰할 수 있는 프록시를 설정해야 합니다. 그렇지 않으면 `url`, `route` 같은 URL 생성 헬퍼가 URL 생성 시 사용할 올바른 HTTP 호스트를 판단할 수 없습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트에 사용할 서브도메인을 직접 선택하고 싶다면 `share` 명령어를 실행할 때 `subdomain` 옵션을 제공할 수 있습니다.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈 소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 PHP에서 널리 사용되는 강력한 디버거인 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면 먼저 [Sail 설정을 게시](#sail-customization)했는지 확인하세요. 그런 다음 Xdebug를 설정하기 위해 애플리케이션의 `.env` 파일에 다음 변수를 추가하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

다음으로, 지정한 모드에서 Xdebug가 활성화되도록 게시된 `php.ini` 파일에 다음 설정이 포함되어 있는지 확인하세요.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정한 후에는 `php.ini` 파일 변경 사항이 적용되도록 Docker 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache
```

#### Linux 호스트 IP 구성

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있으므로 Mac과 Windows(WSL2)에서 Xdebug가 올바르게 설정됩니다. 로컬 머신이 Linux를 실행 중이고 Docker 20.10 이상을 사용하고 있다면 `host.docker.internal`을 사용할 수 있으며, 수동 설정은 필요하지 않습니다.

20.10보다 오래된 Docker 버전에서는 Linux에서 `host.docker.internal`이 지원되지 않으므로 호스트 IP를 직접 정의해야 합니다. 이렇게 하려면 `compose.yaml` 파일에 사용자 정의 네트워크를 정의하여 컨테이너에 정적 IP를 설정하세요.

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```

정적 IP를 설정한 후에는 애플리케이션의 .env 파일 내에 SAIL_XDEBUG_CONFIG 변수를 정의하세요.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

Artisan 명령어를 실행할 때 `sail debug` 명령어를 사용하여 디버깅 세션을 시작할 수 있습니다.

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저를 통해 애플리케이션과 상호작용하면서 애플리케이션을 디버깅하려면 웹 브라우저에서 Xdebug 세션을 시작하는 방법에 대한 [Xdebug에서 제공하는 안내](https://xdebug.org/docs/step_debug#web-application)를 따르세요.

PhpStorm을 사용하고 있다면 [제로 구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrains 문서를 확인하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션을 제공하기 위해 `artisan serve`에 의존합니다. `artisan serve` 명령어는 Laravel 버전 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수만 허용합니다. 이전 Laravel 버전(8.52.0 이하)은 이러한 변수를 지원하지 않으며 디버그 연결을 허용하지 않습니다.

<a name="sail-customization"></a>
## 사용자 정의 (Customization)

Sail은 결국 Docker이므로 거의 모든 것을 자유롭게 사용자 정의할 수 있습니다. Sail 자체 Dockerfile을 게시하려면 `sail:publish` 명령어를 실행하면 됩니다.

```shell
sail artisan sail:publish
```

이 명령어를 실행하면 Laravel Sail에서 사용하는 Dockerfile과 기타 설정 파일이 애플리케이션 루트 디렉터리의 `docker` 디렉터리에 배치됩니다. Sail 설치를 사용자 정의한 후에는 애플리케이션의 `compose.yaml` 파일에서 애플리케이션 컨테이너의 이미지 이름을 변경하고 싶을 수 있습니다. 변경한 뒤에는 `build` 명령어를 사용하여 애플리케이션 컨테이너를 다시 빌드하세요. 하나의 머신에서 Sail을 사용해 여러 Laravel 애플리케이션을 개발하는 경우, 애플리케이션 이미지에 고유한 이름을 지정하는 것이 특히 중요합니다.

```shell
sail build --no-cache
```
