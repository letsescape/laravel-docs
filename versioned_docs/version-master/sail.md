# Laravel Sail (Laravel Sail)

- [소개](#introduction)
- [설치 및 설정](#installation)
    - [기존 애플리케이션에 Sail 설치하기](#installing-sail-into-existing-applications)
    - [Sail 이미지 재빌드](#rebuilding-sail-images)
    - [셸(alias) 설정](#configuring-a-shell-alias)
- [Sail 시작과 중지](#starting-and-stopping-sail)
- [명령어 실행하기](#executing-sail-commands)
    - [PHP 명령어 실행](#executing-php-commands)
    - [Composer 명령어 실행](#executing-composer-commands)
    - [Artisan 명령어 실행](#executing-artisan-commands)
    - [Node / NPM 명령어 실행](#executing-node-npm-commands)
- [데이터베이스와 상호작용하기](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
- [파일 스토리지](#file-storage)
- [테스트 실행하기](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [이메일 미리보기](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [Node 버전](#sail-node-versions)
- [사이트 공유하기](#sharing-your-site)
- [Xdebug로 디버깅하기](#debugging-with-xdebug)
  - [Xdebug CLI 사용법](#xdebug-cli-usage)
  - [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경을 손쉽게 다룰 수 있도록 해주는 경량화된 명령줄 인터페이스입니다. Sail을 사용하면 Docker에 대한 사전 지식 없이도 PHP, MySQL, Redis를 이용한 Laravel 애플리케이션을 구축할 수 있는 강력한 시작점을 제공합니다.

Sail의 핵심은 프로젝트 루트에 위치한 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너들을 손쉽게 조작할 수 있는 CLI를 제공합니다.

Laravel Sail은 macOS, Linux, Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 환경)에서 지원됩니다.

<a name="installation"></a>
## 설치 및 설정 (Installation and Setup)

Laravel Sail은 새로운 Laravel 애플리케이션을 생성할 때 자동으로 설치되므로, 별도의 과정 없이 바로 사용할 수 있습니다.

<a name="installing-sail-into-existing-applications"></a>
### 기존 애플리케이션에 Sail 설치하기

기존 Laravel 애플리케이션에서 Sail을 사용하고 싶다면 Composer 패키지 관리자를 통해 간단히 Sail을 설치할 수 있습니다. (이 과정은 로컬 개발 환경에서 Composer 의존성 설치가 가능하다는 전제 하에 진행됩니다.)

```shell
composer require laravel/sail --dev
```

Sail 설치 후에는 `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 복사하며, Docker 서비스 연결을 위해 `.env` 파일에 필요한 환경 변수를 추가합니다.

```shell
php artisan sail:install
```

마지막으로 Sail을 실행할 수 있습니다. Sail 사용법을 계속 학습하려면 이 문서를 이어서 참고하세요.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux 환경에서 Docker Desktop을 사용하는 경우, 반드시 아래 명령어로 `default` Docker 콘텍스트를 사용해야 합니다: `docker context use default`. 또한 컨테이너 내부에서 파일 권한 에러가 발생한다면, `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 설정해야 할 수 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 등록하기

기존 Sail 설치에 추가 서비스를 포함하고 싶다면, `sail:add` Artisan 명령어를 사용하세요.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
#### Devcontainer 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고자 할 때는, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하세요. 이 옵션은 애플리케이션 루트에 `.devcontainer/devcontainer.json` 파일을 생성합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

Sail 이미지의 모든 패키지와 소프트웨어를 최신 상태로 유지하고자 할 때, 이미지를 완전히 재빌드할 수 있습니다. 다음과 같이 실행하세요:

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
### 셸(alias) 설정

기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함되는 `vendor/bin/sail` 스크립트로 실행됩니다.

```shell
./vendor/bin/sail up
```

하지만 번거롭게 매번 `vendor/bin/sail`을 입력하는 대신, 다음과 같이 셸(alias)을 설정하면 더 쉽게 Sail 명령어를 사용할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

이 alias를 항상 사용할 수 있도록 하려면, 홈 디렉터리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 위 명령을 추가한 후 셸을 재시작하세요.

Alias 설정이 끝나면 단순히 `sail`만 입력해 Sail 명령어를 실행할 수 있습니다. 문서의 나머지 예제도 이 alias를 적용한 것으로 가정합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
## Sail 시작과 중지 (Starting and Stopping Sail)

Laravel Sail의 `compose.yaml` 파일에는 Laravel 애플리케이션 개발에 필요한 다양한 Docker 컨테이너가 정의되어 있습니다. 각각의 컨테이너는 `compose.yaml` 파일의 `services` 설정에 등록되어 있습니다. 그 중 `laravel.test` 컨테이너가 실제 애플리케이션을 서빙하는 주체입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스 서버가 실행 중이지 않은지 반드시 확인하세요. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 실행하려면 `up` 명령어를 사용합니다.

```shell
sail up
```

모든 컨테이너를 백그라운드(Detached) 모드로 실행하려면 다음과 같이 합니다.

```shell
sail up -d
```

컨테이너가 모두 시작되고 나면 웹 브라우저에서 http://localhost 주소로 프로젝트에 접근할 수 있습니다.

컨테이너를 종료하려면 Control + C를 누르면 실행 중인 컨테이너가 정지됩니다. 백그라운드 모드로 실행 중이라면 `stop` 명령어를 사용하세요.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
## 명령어 실행하기 (Executing Commands)

Laravel Sail 환경에서 애플리케이션은 Docker 컨테이너 내부에서 실행되므로, 로컬 컴퓨터와는 분리되어 있습니다. 하지만 Sail을 통해 PHP 명령어, Artisan 명령어, Composer 명령어, Node/NPM 명령어 등 다양한 작업을 편리하게 실행할 수 있습니다.

**Laravel 공식 문서에서는 Composer, Artisan, Node/NPM 명령어 사용 예시가 Sail을 참조하지 않는 경우가 많습니다.** 이는 해당 도구들이 로컬 컴퓨터에 설치되어 있다는 전제입니다. Sail 환경을 사용할 때는 이들 명령어를 Sail을 통해 실행해야 합니다.

```shell
# 로컬에서 Artisan 명령어 실행 예시...
php artisan queue:work

# Laravel Sail 환경에서 Artisan 명령어 실행 예시...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
### PHP 명령어 실행

PHP 명령어는 `php` 명령어를 사용해 실행할 수 있습니다. 이 명령어는 애플리케이션에 맞게 설정된 PHP 버전으로 동작합니다. Sail에서 지원하는 PHP 버전에 대해서는 [PHP 버전 문서](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
### Composer 명령어 실행

Composer 명령어는 `composer` 명령어로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 이미 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
### Artisan 명령어 실행

Laravel Artisan 명령어는 `artisan` 명령어로 실행합니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
### Node / NPM 명령어 실행

Node 관련 작업은 `node`, NPM 관련 명령어는 `npm` 명령어로 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

원한다면 NPM 대신 Yarn을 사용할 수도 있습니다.

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와 상호작용하기 (Interacting With Databases)

<a name="mysql"></a>
### MySQL

애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하고 다시 시작해도 데이터베이스의 데이터가 유지됩니다.

또한 MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 생성됩니다. 첫 번째 데이터베이스는 `.env` 파일의 `DB_DATABASE` 환경 변수 값으로 명명되며, 로컬 개발용입니다. 두 번째는 `testing`이라는 이름의 전용 테스트 데이터베이스로, 테스트가 개발 데이터에 영향을 주지 않도록 분리되어 있습니다.

컨테이너가 시작된 후, `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정하면 애플리케이션 내에서 MySQL에 연결할 수 있습니다.

로컬 컴퓨터에서 애플리케이션의 MySQL 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com)와 같은 그래픽 데이터베이스 관리 툴을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근 가능하며, 접속 정보는 `DB_USERNAME`, `DB_PASSWORD` 환경 변수와 일치합니다. 또는 `root` 사용자로 접속할 수도 있으며, 이 때 비밀번호도 `DB_PASSWORD` 값을 사용합니다.

<a name="mongodb"></a>
### MongoDB

Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, `compose.yaml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 포함됩니다. 이 컨테이너는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) 등 Atlas의 기능을 사용할 수 있으며, Docker 볼륨을 통해 데이터 지속성이 보장됩니다.

컨테이너가 시작되면, `.env` 파일의 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 지정하여 애플리케이션에서 MongoDB에 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있지만, 컨테이너 시작 전에 `MONGODB_USERNAME` 및 `MONGODB_PASSWORD` 환경 변수로 인증을 활성화할 수 있습니다. 이후 연결 문자열에 인증 정보를 추가하세요.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

애플리케이션에 MongoDB를 원활히 연동하려면 [MongoDB 공식 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

로컬 컴퓨터에서 MongoDB 데이터베이스에 접속하려면 [Compass](https://www.mongodb.com/products/tools/compass)와 같은 GUI 툴을 사용할 수 있습니다. 기본적으로 MongoDB는 `localhost`의 27017 포트에서 접근 가능합니다.

<a name="redis"></a>
### Redis

`compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너는 Docker 볼륨을 사용하여, 중지와 재시작에도 Redis 인스턴스의 데이터가 보존됩니다. 컨테이너를 시작한 후, `.env` 파일의 `REDIS_HOST` 환경 변수를 `redis`로 설정하면 애플리케이션에서 연결할 수 있습니다.

로컬에서 Redis 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 GUI 툴을 사용할 수 있습니다. 기본 포트는 6379입니다.

<a name="valkey"></a>
### Valkey

Sail 설치 시 Valkey 서비스를 선택했다면, `compose.yaml` 파일에 [Valkey](https://valkey.io/) 컨테이너 항목도 추가됩니다. 이 컨테이너는 Docker 볼륨을 사용하므로 데이터가 지속적으로 보존됩니다. `.env` 파일의 `REDIS_HOST` 환경 변수를 `valkey`로 설정하면 애플리케이션에서 Valkey 컨테이너로 연결할 수 있습니다.

로컬 컴퓨터에서는 [TablePlus](https://tableplus.com) 같은 툴을 통해 `localhost` 6379 포트로 Valkey 데이터베이스에 접근할 수 있습니다.

<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com) 서비스를 설치했다면, `compose.yaml` 파일에 이 강력한 검색 엔진이 등록됩니다. [Laravel Scout](/docs/master/scout)와 통합되어 사용할 수 있습니다. 컨테이너 시작 이후, `.env` 파일의 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정해 Meilisearch에 연결하세요.

로컬 브라우저에서 [http://localhost:7700](http://localhost:7700) 주소로 접속해 Meilisearch의 웹 관리 패널도 이용할 수 있습니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org) 서비스를 포함시켰다면, `compose.yaml` 파일에 최적화된 오픈소스 검색 엔진이 추가됩니다. [Laravel Scout](/docs/master/scout#typesense)와 기본 통합됩니다. 다음 환경 변수를 추가해 Typesense 인스턴스에 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

로컬 컴퓨터에서 `http://localhost:8108`로 API에 접근할 수 있습니다.

<a name="file-storage"></a>
## 파일 스토리지 (File Storage)

프로덕션 환경에서 Amazon S3를 사용해 파일을 저장할 계획이라면, Sail 설치 시 [RustFS](https://rustfs.com) 서비스를 함께 설치하는 것이 좋습니다. RustFS는 S3 호환 API를 제공하므로, 실제 S3 환경에 테스트 버킷을 만들지 않고도 Laravel의 `s3` 파일스토리지 드라이버를 로컬에서 개발할 수 있습니다. RustFS를 설치했다면, `compose.yaml` 파일에 RustFS 설정이 자동으로 추가됩니다.

애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 설정이 존재합니다. 이 설정을 그대로 Amazon S3뿐 아니라 RustFS와 같은 S3 호환 스토리지 서비스와도 연동할 수 있습니다. RustFS를 사용할 때는 다음과 같이 환경 변수로 설정할 수 있습니다.

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
## 테스트 실행하기 (Running Tests)

Laravel은 뛰어난 테스트 지원 기능을 제공합니다. Sail의 `test` 명령어를 활용해 [기능 및 단위 테스트](/docs/master/testing)를 실행할 수 있습니다. Pest 또는 PHPUnit에서 사용하는 모든 CLI 옵션을 함께 사용할 수 있습니다.

```shell
sail test

sail test --group orders
```

Sail의 `test` 명령어는 `test` Artisan 명령어와 동일합니다.

```shell
sail artisan test
```

기본적으로 Sail은 테스트 실행 시 별도의 `testing` 데이터베이스를 생성해, 실제 데이터베이스에 영향을 주지 않습니다. 기본 Laravel 설치에서는 Sail이 `phpunit.xml` 파일을 자동 설정하여 테스트 실행 시 해당 데이터베이스를 사용합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
### Laravel Dusk

[Laravel Dusk](/docs/master/dusk)는 직관적이고 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium과 같은 별도 설치 없이도 곧장 Dusk 테스트를 실행할 수 있습니다. 시작하려면, 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스를 주석 해제하세요.

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

그리고 `laravel.test` 서비스가 `selenium`에 의존하도록 `depends_on` 속성을 추가하세요.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

설정 후, Sail을 실행한 뒤 `dusk` 명령어로 Dusk 테스트를 실행하세요.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
#### 애플 실리콘에서 Selenium 사용

Mac에 Apple Silicon 칩이 탑재된 경우, `selenium/standalone-chromium` 이미지를 사용해야 합니다.

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

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 애플리케이션에서 발송되는 이메일을 가로채고, 웹 인터페이스를 통해 브라우저에서 미리볼 수 있게 도와줍니다. Sail 환경에서는 기본적으로 `mailpit` 호스트, 1025 포트로 설정되어 있습니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

Sail이 실행 중일 때, 브라우저에서 http://localhost:8025 에 접속하면 Mailpit 웹 인터페이스를 확인할 수 있습니다.

<a name="sail-container-cli"></a>
## 컨테이너 CLI (Container CLI)

가끔은 애플리케이션 컨테이너 내부에서 Bash 세션을 시작하고 싶을 때가 있습니다. `shell` 명령어로 컨테이너에 접속해, 파일 및 설치된 서비스를 확인하고 임의의 셸 명령도 실행할 수 있습니다.

```shell
sail shell

sail root-shell
```

[Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면, `tinker` 명령어를 실행하세요.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
## PHP 버전 (PHP Versions)

Sail은 현재 PHP 8.5, 8.4, 8.3, 8.2, 8.1 또는 PHP 8.0을 통해 애플리케이션을 서빙할 수 있습니다. 기본값으로는 PHP 8.4가 사용됩니다. 사용 중인 PHP 버전을 변경하고 싶다면, `compose.yaml` 파일의 `laravel.test` 컨테이너에서 `build` 설정을 수정하면 됩니다.

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

또한 애플리케이션에서 어떤 PHP 버전이 사용되는지 구분하려면 `image` 이름도 같이 수정할 수 있습니다.

```yaml
image: sail-8.2/app
```

`compose.yaml` 파일을 수정한 뒤에는 컨테이너 이미지를 다시 빌드해야 변경 사항이 적용됩니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
## Node 버전 (Node Versions)

Sail은 기본적으로 Node 22를 설치합니다. 빌드 과정에서 설치될 Node 버전을 바꾸고 싶으면, `compose.yaml` 파일 내 `laravel.test` 서비스의 `build.args`를 수정하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

수정 후에는 컨테이너 이미지를 다시 빌드하세요.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
## 사이트 공유하기 (Sharing Your Site)

동료에게 사이트를 미리 보여주거나, 웹훅 연동 등에서 공개적으로 사이트를 공유해야 할 필요가 생길 수 있습니다. 이럴 때는 `share` 명령어를 사용하면 됩니다. 명령을 실행하면 임시로 접근 가능한 `laravel-sail.site` URL이 발급되어 애플리케이션을 외부에 공개할 수 있습니다.

```shell
sail share
```

이 기능을 이용할 때는, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 신뢰할 수 있는 프록시 설정을 해주어야 합니다. 그렇지 않으면 `url`, `route` 등 URL을 생성할 때 올바른 HTTP 호스트가 인식되지 않습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

공유될 사이트의 서브도메인을 직접 지정하고자 한다면, `share` 명령 실행시 `subdomain` 옵션을 추가하세요.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기 (Debugging With Xdebug)

Laravel Sail의 Docker 설정에는 [Xdebug](https://xdebug.org/) 지원이 포함되어 있어, PHP 디버깅을 강력하게 도와줍니다. Xdebug를 활성화하려면 [Sail 설정을 퍼블리시](#sail-customization)한 뒤, `.env` 파일에 다음 환경 변수를 추가하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

그리고 퍼블리시된 `php.ini` 파일에 아래 설정이 포함되어 있어야 합니다.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

`php.ini` 파일을 수정했다면, 변경 사항이 Docker에 반영될 수 있도록 이미지를 반드시 재빌드해야 합니다.

```shell
sail build --no-cache
```

#### Linux 호스트 IP 설정

내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어, Xdebug가 Mac 및 Windows(WSL2)에서 정상 작동하도록 합니다. 리눅스에서 Docker 20.10 이상을 사용한다면 추가 설정은 필요 없습니다.

20.10 미만 버전에서는 `host.docker.internal`이 지원되지 않으므로, 직접 호스트 IP를 지정해야 합니다. 이 경우 `compose.yaml` 파일에 커스텀 네트워크와 정적 IP를 설정하세요.

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

정적 IP를 설정했다면, `.env` 파일에 아래와 같이 SAIL_XDEBUG_CONFIG 변수를 지정합니다.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

Artisan 명령어를 디버깅 세션을 통해 실행하려면 `sail debug` 명령어를 사용할 수 있습니다.

```shell
# Xdebug 없이 Artisan 명령어 실행...
sail artisan migrate

# Xdebug 활성화 후 Artisan 명령어 실행...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

브라우저로 애플리케이션을 테스트하면서 디버깅하려면 [Xdebug 공식 안내](https://xdebug.org/docs/step_debug#web-application)를 참고해 브라우저에서 Xdebug 세션을 시작하세요.

PhpStorm을 사용한다면 [제로-구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrains의 공식 문서를 참고하시기 바랍니다.

> [!WARNING]
> Laravel Sail은 애플리케이션을 서비스할 때 `artisan serve`를 사용합니다. `artisan serve` 명령어는 Laravel 8.53.0 이상부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 인식합니다. 8.52.0 이하 버전은 이 변수를 지원하지 않으므로 디버깅 연결이 되지 않습니다.

<a name="sail-customization"></a>
## 커스터마이징 (Customization)

Sail은 기본적으로 Docker이므로 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail에서 사용하는 Dockerfile을 퍼블리시하려면 다음 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

명령 실행 후 Dockerfile과 기타 설정 파일들이 애플리케이션 루트의 `docker` 디렉터리에 복사됩니다. Sail 환경을 커스터마이즈한 뒤에는, `compose.yaml` 파일 내 애플리케이션 컨테이너의 이미지 이름을 원하는 대로 변경하면 됩니다. 그런 다음 `build` 명령어로 이미지를 재빌드하세요. 여러 Laravel 애플리케이션을 한 대의 컴퓨터에서 동시에 개발할 시에는 특히 컨테이너 이미지 이름을 유일하게 지정하는 것이 좋습니다.

```shell
sail build --no-cache
```
