# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [셸 별칭(shell alias) 설정](#configuring-a-shell-alias)
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
- [이메일 미리보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유](#sharing-your-site)
- [Xdebug로 디버깅](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 경량의 커맨드라인 인터페이스입니다. Sail을 사용하면 Docker 경험이 없어도 PHP, MySQL, Redis를 활용한 Laravel 애플리케이션을 쉽게 시작할 수 있습니다.

Sail의 핵심은 프로젝트 루트에 위치한 `compose.yaml` 파일과, 같은 위치에 있는 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml`에 정의된 Docker 컨테이너와 손쉽게 상호작용할 수 있는 CLI(커맨드라인 인터페이스)를 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 를 통해)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 모든 새로운 Laravel 애플리케이션에 자동으로 설치되므로, 설치 즉시 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치 (Installing Sail Into Existing Applications)

기존 Laravel 애플리케이션에서 Sail을 사용하고 싶다면, Composer 패키지 매니저를 통해 Sail을 설치할 수 있습니다. 당연히, 이 과정은 로컬 개발 환경에서 Composer 패키지 설치가 가능하다는 전제에서 진행됩니다.

```shell
composer require laravel/sail --dev
```

Sail 설치가 완료되면, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트 디렉터리에 배포하고, Docker 서비스와 연결할 수 있도록 `.env` 파일에 필요한 환경 변수를 추가 및 수정합니다.

```shell
php artisan sail:install
```

이제 Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 알아보고 싶다면, 이 문서의 다음 내용을 계속 참고하세요.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용하는 경우, 다음 명령어로 반드시 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`. 또한, 컨테이너 내에서 파일 권한 관련 오류가 발생할 경우, 환경 변수 `SUPERVISOR_PHP_USER`를 `root`로 설정해야 할 수도 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 등록

기존 Sail 설치에 추가적인 서비스를 더하고 싶다면, `sail:add` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. `--devcontainer` 옵션은 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json` 파일을 배포합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드 (Rebuilding Sail Images)

Sail 이미지의 모든 패키지 및 소프트웨어를 최신 상태로 유지하려면 이미지를 완전히 재빌드할 수 있습니다. 이를 위해 `build` 명령어를 사용하세요.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸 별칭(shell alias) 설정 (Configuring A Shell Alias)

기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 이용해 실행합니다.

```shell
./vendor/bin/sail up
```

하지만 Sail 명령어를 실행할 때마다 `vendor/bin/sail`을 계속 입력하는 대신, 셸 별칭(alias)을 만들어 좀 더 간편하게 Sail을 사용할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 별칭을 항상 사용할 수 있도록 하려면, 홈 디렉터리의 `~/.zshrc` 또는 `~/.bashrc` 등 셸 환경설정 파일에 추가한 후 셸을 재시작하세요.

셸 별칭 설정 이후에는 그냥 `sail`만 입력해서 Sail 명령어를 실행할 수 있습니다. 이후 예제들은 별칭이 설정되어 있다는 전제 하에 설명됩니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일에는 Laravel 애플리케이션 개발을 지원하는 다양한 Docker 컨테이너가 정의되어 있습니다. 각각의 컨테이너는 `compose.yaml`의 `services` 설정에 항목으로 등록되어 있습니다. 이 중 `laravel.test` 컨테이너가 애플리케이션을 실제로 서비스하는 기본 컨테이너입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 웹 서버나 데이터베이스가 실행 중이 아닌지 확인하세요. 애플리케이션의 `compose.yaml`에서 정의된 모든 Docker 컨테이너를 실행하려면 `up` 명령어를 사용하세요.

```shell
sail up
```

모든 컨테이너를 백그라운드(detached)에서 실행하려면 아래처럼 입력합니다.

```shell
sail up -d
```

컨테이너가 시작되면 웹 브라우저에서 http://localhost 에 접속해 프로젝트를 확인할 수 있습니다.

모든 컨테이너를 중지하려면 Control + C 키로 실행을 멈출 수 있으며, 백그라운드로 실행 중일 때는 아래 명령어로 중지할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행 (Executing Commands)

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 안에서 실행되기 때문에 로컬 컴퓨터와는 분리되어 있습니다. 하지만 Sail은 다양한 명령어(PHP, Artisan, Composer, Node/NPM 등)를 해당 컨테이너에서 편리하게 실행할 수 있도록 돕습니다.

**Laravel 공식 문서 곳곳에서는 Sail을 언급하지 않고 Composer, Artisan, Node/NPM 명령어 예시가 종종 등장합니다.** 이 예시들은 해당 도구들이 로컬에 설치된 환경을 전제로 합니다. Sail을 사용하여 로컬에서 Laravel을 개발하는 경우, 반드시 Sail을 통해 해당 명령어를 실행해야 합니다.

```shell
# 로컬 환경에서 Artisan 명령어 실행...
php artisan queue:work

# Laravel Sail에서 Artisan 명령어 실행...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행 (Executing PHP Commands)

`php` 명령어를 사용해 PHP 명령어를 실행할 수 있습니다. 이 명령어들은 애플리케이션의 현재 설정된 PHP 버전으로 동작합니다. Laravel Sail에서 사용 가능한 PHP 버전은 [PHP 버전 문서](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행 (Executing Composer Commands)

`composer` 명령어로 Composer 관련 작업을 실행할 수 있습니다. Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행 (Executing Artisan Commands)

Laravel의 Artisan 명령어는 `artisan` 명령어를 통해 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행 (Executing Node / NPM Commands)

`node` 명령어로 Node 관련 명령을, `npm` 명령어로 NPM 관련 명령을 실행할 수 있습니다.

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

애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해, 컨테이너를 중지하거나 재시작해도 데이터가 유지되도록 합니다.

또한, MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스를 자동 생성합니다. 첫 번째 데이터베이스는 `.env` 파일의 `DB_DATABASE` 환경 변수 값을 이름으로 사용하며, 로컬 개발용입니다. 두 번째 데이터베이스는 `testing`이라는 이름의 전용 테스트용 데이터베이스로, 테스트 실행 시 개발 데이터와 충돌을 방지해줍니다.

컨테이너가 실행된 이후에는 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정해 MySQL 인스턴스와 연결할 수 있습니다.

로컬 컴퓨터에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 등의 GUI 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 MySQL은 `localhost` 3306 포트에서 접근할 수 있으며, 접속 자격 증명은 `.env` 파일의 `DB_USERNAME`, `DB_PASSWORD` 값을 사용합니다. 또는, `root` 계정으로 접속할 수도 있으며, 이 때도 비밀번호는 `DB_PASSWORD` 값과 동일합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 추가로 선택했다면, 애플리케이션의 `compose.yaml` 파일에는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 포함됩니다. 이 컨테이너는 Atlas의 [검색 인덱스](https://www.mongodb.com/docs/atlas/atlas-search/) 등 기능을 제공하며, [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다.

컨테이너 실행 후, `.env` 파일에 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정해 MongoDB 인스턴스를 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있지만, 인증을 활성화하려면 `MONGODB_USERNAME`, `MONGODB_PASSWORD` 환경 변수를 지정 후, 아래처럼 연결 문자열에 포함해야 합니다.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB와 Laravel 애플리케이션을 연동하려면 [MongoDB에서 공식적으로 관리하는 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 컴퓨터에서 MongoDB 데이터베이스를 사용하려면 [Compass](https://www.mongodb.com/products/tools/compass) 등의 GUI 툴을 활용하세요. 기본적으로 `localhost` 27017 포트에서 접근할 수 있습니다.

<a name="redis"></a>
### Redis

애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 보존됩니다. 컨테이너 실행 후, `.env` 파일의 `REDIS_HOST` 환경 변수를 `redis`로 설정하면 Redis 인스턴스에 연결할 수 있습니다.

로컬 컴퓨터에서 Redis 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 등의 GUI 툴을 사용할 수 있습니다. 기본적으로 Redis는 `localhost` 6379 포트에서 접근 가능합니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 추가로 선택했다면, 애플리케이션의 `compose.yaml` 파일에 [Valkey](https://valkey.io/) 항목이 추가됩니다. 이 컨테이너도 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 유지됩니다. 애플리케이션에서 해당 컨테이너에 연결하려면, `.env` 파일의 `REDIS_HOST` 환경 변수를 `valkey`로 설정하면 됩니다.

로컬 컴퓨터에서 Valkey 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 등 GUI 툴을 사용할 수 있으며, 기본 포트는 `localhost` 6379입니다.

<a name="meilisearch"></a>
### Meilisearch

Sail 설치 과정에서 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, 애플리케이션의 `compose.yaml` 파일에는 이 강력한 검색 엔진이 등록됩니다. [Laravel Scout](/docs/12.x/scout)에 통합되어 있으며, 컨테이너가 기동된 후 `.env` 파일의 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 지정해 연결할 수 있습니다.

로컬 컴퓨터에서는 웹 브라우저에서 `http://localhost:7700`에 접속해 Meilisearch 관리 패널에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택하면, 애플리케이션의 `compose.yaml` 파일에 이 초고속 오픈소스 검색 엔진 항목이 추가됩니다. [Laravel Scout](/docs/12.x/scout#typesense)와 기본적으로 통합되어 있습니다. 컨테이너 실행 후에는 다음 환경 변수를 설정하여 Typesense 인스턴스에 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서는 `http://localhost:8108`로 API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 Amazon S3를 사용해 파일을 저장하려는 경우, Sail 설치 시 [RustFS](https://rustfs.com) 서비스를 추가로 설치할 수 있습니다. RustFS는 호환되는 S3 API를 제공하므로, 실제 S3 환경에 별도의 "테스트" 버킷을 만들지 않고도 Laravel의 `s3` 파일 스토리지 드라이버를 활용해 로컬에서 개발할 수 있습니다. 만약 RustFS를 설치했다면, 애플리케이션의 `compose.yaml` 파일에 RustFS 설정이 추가됩니다.

기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크를 Amazon S3 뿐 아니라 RustFS와 같은 S3 호환 파일 스토리지 서비스와도 사용할 수 있으며, 관련 환경 변수만 설정하면 됩니다. 예를 들어 RustFS를 사용할 경우, 환경 변수 설정 예시는 다음과 같습니다.

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

Laravel은 기본적으로 뛰어난 테스트 지원 기능을 제공합니다. Sail의 `test` 명령어로 [기능 및 단위 테스트](/docs/12.x/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 사용할 수 있는 모든 CLI 옵션도 함께 지정할 수 있습니다.

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 실제로 `test` Artisan 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

기본적으로 Sail은 테스트 실행 시 현재 데이터베이스 상태와 충돌하지 않도록 전용 `testing` 데이터베이스를 생성합니다. Laravel 기본 설치에서는 Sail이 자동으로 `phpunit.xml` 파일을 아래와 같이 테스트용 데이터베이스를 사용하도록 설정합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/12.x/dusk)는 직관적이고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium 등 별도의 도구를 설치하지 않고도 Dusk 테스트를 실행할 수 있습니다. 우선, 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스 항목의 주석을 해제해 주세요.

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

그 다음, `compose.yaml` 파일의 `laravel.test` 서비스에 `depends_on`에 `selenium`을 추가했는지 확인하세요.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

준비가 끝나면 Sail을 시작한 후, 아래 명령어로 Dusk 테스트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### Apple Silicon에서 Selenium 사용

로컬 컴퓨터가 Apple Silicon 칩을 사용할 경우, `selenium` 서비스에서 `selenium/standalone-chromium` 이미지를 사용해야 합니다.

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
## 이메일 미리보기 (Previewing Emails)

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 전송되는 이메일을 가로채 웹 인터페이스로 확인할 수 있도록 해줍니다. Sail을 사용할 때, Mailpit의 기본 호스트는 `mailpit`이고 포트는 1025입니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail 실행 중에는 http://localhost:8025 에 접속해 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

애플리케이션 컨테이너에서 Bash 세션을 시작해보고 싶을 때가 있습니다. `shell` 명령어를 사용하면, 컨테이너 내부에 접속하여 파일이나 설치된 서비스 확인, 임의의 셸 명령 실행 등이 가능합니다.

```shell
sail shell

sail root-shell
```

새로운 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 사용하세요.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.5, 8.4, 8.3, 8.2, 8.1, 8.0 버전으로 애플리케이션을 서비스 할 수 있습니다. 기본 사용 버전은 PHP 8.4입니다. 사용 중인 PHP 버전을 변경하고 싶다면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 경로를 아래와 같이 수정하세요.

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

또한, 애플리케이션에서 실제 사용하는 PHP 버전을 반영하여 `image` 이름도 함께 업데이트하는 것이 좋습니다. 이 설정도 `compose.yaml` 파일에 정의되어 있습니다.

```yaml
image: sail-8.2/app
```

`compose.yaml` 파일을 수정한 후에는 반드시 컨테이너 이미지를 재빌드해야 변경이 적용됩니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 시 설치되는 Node 버전을 변경하려면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 설정을 수정하세요.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

설정 후, 컨테이너 이미지를 재빌드하세요.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유 (Sharing Your Site)

웹사이트를 공개적으로 공유해 동료와 미리보기 하거나, Webhook 통합 테스트 등을 진행해야 할 때가 있습니다. 이때 `share` 명령어를 사용하면 됩니다. 실행 시 임의로 생성된 `laravel-sail.site` 도메인 주소가 발급되며, 이를 통해 외부에서 애플리케이션에 접속할 수 있습니다.

```shell
sail share
```

`share` 명령어로 사이트를 공유할 때는, 반드시 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 이용해 신뢰할 수 있는 프록시를 설정해야 합니다. 그렇지 않으면 `url`, `route` 등 URL 생성 헬퍼들이 올바른 HTTP 호스트를 인식하지 못하게 됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유 사이트의 서브도메인을 직접 지정하고 싶다면, `subdomain` 옵션을 함께 지정하세요.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)에서 개발한 오픈소스 터널링 서비스 [Expose](https://github.com/beyondcode/expose)로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 PHP의 강력한 디버거 [Xdebug](https://xdebug.org/)를 지원하는 기능이 포함되어 있습니다. Xdebug를 사용하려면, [Sail 설정을 먼저 배포한 후](#sail-customization) 아래와 같이 `.env` 파일에 관련 변수를 추가하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고, 배포된 `php.ini` 파일에 아래 설정이 포함되어 있어야 합니다.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정했다면 반드시 Docker 이미지 재빌드 과정을 거쳐야 설정이 적용됩니다.

```shell
sail build --no-cache
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어, Mac 및 Windows(WSL2)에서 정상 동작하게 구성되어 있습니다. Linux에서 Docker 20.10 이상을 사용한다면 별도의 설정은 필요 없습니다.

Docker 20.10 미만 버전에서는 Linux에서 `host.docker.internal`이 지원되지 않으므로 호스트 IP를 직접 지정해야 합니다. 이 경우, `compose.yaml` 파일에서 사용자 정의 네트워크를 통해 컨테이너에 고정 IP를 할당하세요.

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

이제 `.env` 파일에서 SAIL_XDEBUG_CONFIG 변수를 다음과 같이 지정합니다.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법 (Xdebug CLI Usage)

`debug` 명령어를 사용하면 Artisan 명령어 실행 시 디버깅 세션을 시작할 수 있습니다.

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug와 함께 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법 (Xdebug Browser Usage)

웹 브라우저를 통해 애플리케이션을 조작하며 디버깅하려면, [Xdebug에서 안내하는 방법](https://xdebug.org/docs/step_debug#web-application)에 따라 Xdebug 세션을 시작하세요.

PhpStorm을 사용하는 경우, [제로 설정 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 관련 JetBrains 공식 문서를 참고하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션을 서비스할 때 `artisan serve`를 사용합니다. `artisan serve` 명령어는 Laravel 8.53.0 버전부터 `XDEBUG_CONFIG`, `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하의 Laravel 버전에서는 해당 변수를 인식하지 않아 디버깅 연결이 작동하지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 본질적으로 Docker 기반이므로 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 Dockerfile 및 설정 파일을 직접 프로젝트로 가져와 수정하려면, 아래 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

이 명령어를 실행하면, Laravel Sail에서 사용하는 Dockerfile과 기타 설정 파일이 애플리케이션 루트의 `docker` 디렉터리로 복사됩니다. 이후 Sail 설정을 원하는 대로 수정할 수 있으며, 애플리케이션 컨테이너의 이미지 이름도 `compose.yaml` 파일에서 변경 가능합니다. 여러 개의 Laravel 프로젝트를 하나의 컴퓨터에서 Sail로 동시 개발할 때는 이미지 이름을 고유하게 지정하는 것이 특히 중요합니다. 변경 후에는 반드시 아래처럼 컨테이너를 다시 빌드해야 합니다.

```shell
sail build --no-cache
```
