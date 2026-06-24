<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation & Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Configuring A Bash Alias](#configuring-a-bash-alias)
- [Starting & Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [MeiliSearch](#meilisearch)
- [File Storage](#file-storage)
- [Running Tests](#running-tests)
    - [Laravel Dusk](#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [Container CLI](#sail-container-cli)
- [PHP Versions](#sail-php-versions)
- [Node Versions](#sail-node-versions)
- [Sharing Your Site](#sharing-your-site)
- [Debugging With Xdebug](#debugging-with-xdebug)
  - [Xdebug CLI Usage](#xdebug-cli-usage)
  - [Xdebug Browser Usage](#xdebug-browser-usage)
- [Customization](#sail-customization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Sail](https://github.com/laravel/sail) is a light-weight command-line interface for interacting with Laravel's default Docker development environment. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience. -->
[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있도록 해주는 경량 커맨드라인 인터페이스(CLI)입니다. Sail을 사용하면 Docker에 대한 별도의 경험 없이도 PHP, MySQL, Redis로 Laravel 애플리케이션을 손쉽게 시작할 수 있습니다.

<!-- At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file. -->
Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. 이 `sail` 스크립트는 `docker-compose.yml`에 정의된 Docker 컨테이너들과 편리하게 상호작용할 수 있는 CLI 기능을 제공합니다.

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail은 macOS, Linux, Windows(및 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)) 환경에서 지원됩니다.

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<!-- Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/8.x/installation) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with. -->
Laravel Sail은 새로운 Laravel 프로젝트를 생성할 때 자동으로 함께 설치됩니다. 즉시 사용하실 수 있습니다. 새로운 Laravel 애플리케이션을 만드는 방법은 각 운영체제에 맞는 Laravel의 [installation documentation](/docs/8.x/installation)를 참고하시기 바랍니다. 설치 과정 중, Sail에서 지원하는 어떤 서비스를 함께 사용할 것인지 묻게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
<!-- ### Installing Sail Into Existing Applications -->
### Installing Sail Into Existing Applications

<!-- If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies: -->
이미 개발 중인 기존 Laravel 애플리케이션에 Sail을 도입하고 싶다면, Composer 패키지 매니저를 이용해 Sail을 쉽게 설치할 수 있습니다. 물론, 아래 단계는 Composer 의존성 설치가 가능한 개발 환경이 마련된 경우를 전제로 합니다.

```
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application: -->
Sail 설치가 완료되면, `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트 경로에 복사해 줍니다.

```
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
마지막으로 Sail을 시작하면 됩니다. Sail 사용법에 대해 더 자세히 알아보려면, 이 문서의 다음 내용을 계속 읽어 내려가세요.


<!--     ./vendor/bin/sail up -->
    ./vendor/bin/sail up


<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶다면, `sail:install` 명령에 `--devcontainer` 옵션을 추가해서 실행할 수 있습니다. `--devcontainer` 옵션을 적용하면 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 루트에 배포합니다.

```
php artisan sail:install --devcontainer
```

<a name="configuring-a-bash-alias"></a>
<!-- ### Configuring A Bash Alias -->
### Configuring A Bash Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함되는 `vendor/bin/sail` 스크립트를 사용해 실행합니다.

```bash
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a Bash alias that allows you to execute Sail's commands more easily: -->
하지만 매번 `vendor/bin/sail`을 입력하는 대신, Bash 별칭(alias)을 만들어 좀 더 쉽게 Sail 명령어를 사용할 수 있습니다.

```bash
alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'
```

<!-- Once the Bash alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
이렇게 Bash 별칭을 설정하면, 단순히 `sail`만 입력해 Sail 명령어를 실행할 수 있습니다. 이 문서의 이후 예제들은 해당 별칭이 등록되어 있다고 가정하고 설명합니다.

```bash
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting & Stopping Sail -->
## Starting & Stopping Sail

<!-- Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 개발을 위해 함께 동작하는 다양한 Docker 컨테이너가 정의되어 있습니다. 이들 각각은 `docker-compose.yml` 파일의 `services` 항목에 등록되어 있으며, `laravel.test` 컨테이너가 주 애플리케이션 컨테이너 역할을 담당합니다.

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command: -->
Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인해야 합니다. 애플리케이션의 `docker-compose.yml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 아래와 같이 `up` 명령어를 입력합니다.

```bash
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
모든 Docker 컨테이너를 백그라운드에서 실행하고 싶다면 "detached" 모드로 시작하면 됩니다.

```bash
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
컨테이너가 모두 정상적으로 시작되면, 브라우저에서 http://localhost 주소로 프로젝트를 확인하실 수 있습니다.

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
모든 컨테이너를 중지하려면 Control + C 단축키로 실행을 멈추면 됩니다. 만약 컨테이너가 백그라운드에서 실행 중이라면, 다음과 같이 `stop` 명령어로 중지할 수 있습니다.

```bash
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail을 사용하는 경우, 여러분의 애플리케이션은 Docker 컨테이너 안에서 실행되며 로컬 컴퓨터와 분리된 환경에 있습니다. 하지만 Sail을 사용하면 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node/NPM 명령어 등 다양한 명령어를 손쉽게 실행할 수 있습니다.

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel 공식 문서에서 Composer, Artisan, Node/NPM 명령어가 Sail을 명시하지 않고 안내되는 경우가 많습니다.** 이런 예제들은 해당 도구가 로컬 컴퓨터에 설치되어 있다는 전제로 작성되어 있습니다. 그러나 Sail 환경에서 개발한다면, 이런 명령어들도 Sail을 통해 실행해야 합니다.

```bash
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
<!-- ### Executing PHP Commands -->
### Executing PHP Commands

<!-- PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions): -->
PHP 명령어는 `php` 명령어를 사용해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전입니다. Sail에서 지원하는 PHP 버전에 대한 자세한 내용은 [PHP version documentation](#sail-php-versions)를 참고하세요.

```bash
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer 2.x installation: -->
Composer 명령어는 `composer` 명령어를 사용해 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer 2.x가 미리 설치되어 있습니다.

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
<!-- #### Installing Composer Dependencies For Existing Applications -->
#### Installing Composer Dependencies For Existing Applications

<!-- If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer. -->
여러 명이 함께 개발하는 프로젝트의 경우, 여러분이 처음 Laravel 애플리케이션을 만드는 사람이 아닐 수도 있습니다. 따라서 프로젝트의 Composer 의존성(및 Sail)들은 저장소를 클론한 뒤 자동으로 설치되지 않습니다.

<!-- You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies: -->
이럴 때는 프로젝트 디렉터리에서 아래 명령어를 실행해 의존성을 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 경량 Docker 컨테이너를 사용하여 애플리케이션 의존성을 설치합니다.

```nothing
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v $(pwd):/var/www/html \
    -w /var/www/html \
    laravelsail/php81-composer:latest \
    composer install --ignore-platform-reqs
```

<!-- When using the `laravelsail/phpXX-composer` image, you should use the same version of PHP that you plan to use for your application (`74`, `80`, or `81`). -->
`laravelsail/phpXX-composer` 이미지를 사용할 때는 여러분이 실제 사용할 PHP 버전(`74`, `80`, `81` 등)과 맞추어 선택해야 합니다.

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel의 Artisan 명령어는 `artisan` 명령어를 사용해 실행할 수 있습니다.

```bash
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
Node 관련 명령어는 `node`로, NPM 명령어는 `npm`으로 실행할 수 있습니다.

```nothing
sail node --version

sail npm run prod
```

<!-- If you wish, you may use Yarn instead of NPM: -->
원한다면 NPM 대신 Yarn을 사용해도 됩니다.

```nothing
sail yarn
```

<a name="interacting-with-sail-databases"></a>
<!-- ## Interacting With Databases -->
## Interacting With Databases

<a name="mysql"></a>
<!-- ### MySQL -->
### MySQL

<!-- As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. In addition, when the MySQL container is starting, it will ensure a database exists whose name matches the value of your `DB_DATABASE` environment variable. -->
애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용해 데이터베이스의 데이터가 컨테이너를 중지ㆍ재시작해도 보존되도록 합니다. 또한 MySQL 컨테이너가 시작될 때, 여러분의 `DB_DATABASE` 환경 변수 값과 동일한 데이터베이스가 자동으로 생성됩니다.

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
컨테이너가 모두 실행된 후, 애플리케이션 내에서 MySQL 인스턴스에 접속하려면 `.env` 파일에서 `DB_HOST`를 `mysql`로 지정하면 됩니다.

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306. -->
로컬 컴퓨터에서 애플리케이션의 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 GUI 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트로 접근이 가능합니다.

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너 역시 포함되어 있습니다. 이 컨테이너도 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하여 컨테이너 중지나 재시작 시에도 Redis 데이터를 보존합니다. 컨테이너 실행 후 `.env` 파일에서 `REDIS_HOST`를 `redis`로 지정하면 애플리케이션 내에서 Redis 인스턴스에 접근할 수 있습니다.

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
로컬 컴퓨터에서 애플리케이션의 Redis 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 등의 데이터베이스 관리 도구를 사용할 수 있습니다. 기본적으로 Redis는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="meilisearch"></a>
<!-- ### MeiliSearch -->
### MeiliSearch

<!-- If you chose to install the [MeiliSearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search-engine that is [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) with [Laravel Scout](/docs/8.x/scout). Once you have started your containers, you may connect to the MeiliSearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail 설치 시 [MeiliSearch](https://www.meilisearch.com) 서비스를 함께 설치하도록 선택했다면, 애플리케이션의 `docker-compose.yml` 파일에 MeiliSearch 컨테이너 설정이 추가됩니다. MeiliSearch는 [compatible](/docs/8.x/scout)과 [Laravel Scout](https://github.com/meilisearch/meilisearch-laravel-scout)되며, 강력한 검색 엔진을 제공합니다. 컨테이너 실행 후 `MEILISEARCH_HOST` 환경 변수 값을 `http://meilisearch:7700`으로 설정하면 애플리케이션 내에서 MeiliSearch에 연결할 수 있습니다.

<!-- From your local machine, you may access MeiliSearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
로컬 컴퓨터에서 MeiliSearch의 웹 기반 관리 패널은 브라우저에서 `http://localhost:7700`으로 접속해 사용합니다.

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file. -->
프로덕션 환경에서 Amazon S3를 이용해 파일을 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 함께 추가하는 것을 추천합니다. MinIO는 S3와 호환되는 API를 제공하며, 프로덕션 환경의 S3에서 "테스트" 버킷을 만들 필요 없이 Laravel의 `s3` 파일 스토리지 드라이버를 로컬 환경에서 개발용으로 사용할 수 있게 해 줍니다. Sail 설치 시 MinIO를 선택하면, 애플리케이션의 `docker-compose.yml` 파일에 MinIO 구성 항목이 추가됩니다.

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows: -->
기본적으로 여러분의 애플리케이션 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 포함되어 있습니다. 이 디스크를 Amazon S3뿐 아니라 MinIO 등 S3 호환 파일 스토리지 서비스와도 함께 사용할 수 있으며, 관련 환경 변수를 적절히 설정하면 바로 동작합니다. 예를 들어 MinIO 사용할 경우 아래와 같이 환경 변수를 지정합니다.

```ini
FILESYSTEM_DRIVER=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/8.x/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command: -->
Laravel은 기본적으로 강력한 테스트 기능을 제공합니다. Sail에서는 `test` 명령어를 통해 [feature and unit tests](/docs/8.x/testing)를 실행할 수 있습니다. PHPUnit이 지원하는 모든 CLI 옵션 역시 `test` 명령어에 함께 사용할 수 있습니다.


<!--     sail test -->
    sail test

<!--     sail test --group orders -->
    sail test --group orders


<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail의 `test` 명령어는 아래와 같이 `test` Artisan 명령어를 실행하는 것과 동일합니다.


<!--     sail artisan test -->
    sail artisan test


<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/8.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file: -->
[Laravel Dusk](/docs/8.x/dusk)는 편리하고 직관적인 브라우저 자동화 및 테스트 API를 제공합니다. Sail을 이용하면 Selenium 등 별도의 도구를 로컬에 설치하지 않고도 이런 테스트를 실행할 수 있습니다. 먼저, 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요.

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<!-- Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`: -->
그리고 `docker-compose.yml` 파일에서 `laravel.test` 서비스의 `depends_on` 항목에 `selenium`도 추가되어 있는지 확인하세요.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
이제 Sail을 시작한 뒤 아래와 같이 `dusk` 명령어로 Dusk 테스트를 실행할 수 있습니다.


<!--     sail dusk -->
    sail dusk


<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium On Apple Silicon -->
#### Selenium On Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `seleniarm/standalone-chromium` image: -->
로컬 컴퓨터가 Apple Silicon 칩(M1/M2 등)을 사용한다면, `selenium` 서비스에서 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다.

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `docker-compose.yml` file contains a service entry for [MailHog](https://github.com/mailhog/MailHog). MailHog intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, MailHog's default host is `mailhog` and is available via port 1025: -->
Laravel Sail의 기본 `docker-compose.yml` 파일에는 [MailHog](https://github.com/mailhog/MailHog) 서비스가 포함되어 있습니다. MailHog는 개발 중 애플리케이션에서 전송되는 이메일을 가로채 웹 인터페이스로 미리볼 수 있게 해줍니다. Sail을 사용할 때 MailHog의 기본 호스트명은 `mailhog`이고, 1025 포트를 사용합니다.

```bash
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the MailHog web interface at: http://localhost:8025 -->
Sail이 실행 중이라면 브라우저에서 http://localhost:8025 주소를 입력해 MailHog 웹 인터페이스에 접속할 수 있습니다.

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well execute arbitrary shell commands within the container: -->
때로는 애플리케이션의 컨테이너 안에서 Bash 세션을 열고 싶을 수 있습니다. `shell` 명령어를 사용하면 애플리케이션 컨테이너에 접속해 파일 확인, 설치된 서비스 점검, 임의의 shell 명령 실행 등을 할 수 있습니다.

```nothing
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
또한 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 새로 시작하고 싶을 때는 다음과 같이 `tinker` 명령어를 실행하면 됩니다.

```bash
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.1, PHP 8.0, or PHP 7.4. The default PHP version used by Sail is currently PHP 8.1. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file: -->
Sail은 현재 PHP 8.1, PHP 8.0, PHP 7.4 버전으로 애플리케이션을 실행할 수 있습니다. Sail의 기본 PHP 버전은 8.1입니다. 애플리케이션에서 사용하는 PHP 버전을 변경하려면, `docker-compose.yml` 파일의 `laravel.test` 컨테이너의 `build` 정의를 아래처럼 수정하면 됩니다.

```yaml
# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file: -->
또한 이미지 이름(`image`) 역시 PHP 버전과 맞춰서 변경해 주는 것이 좋습니다. 이 설정도 `docker-compose.yml` 파일에서 조정할 수 있습니다.

```yaml
image: sail-8.1/app
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일을 수정한 이후 컨테이너 이미지를 재빌드합니다.


<!--     sail build --no-cache -->
    sail build --no-cache

<!--     sail up -->
    sail up


<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 16 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file: -->
Sail은 기본적으로 Node 16을 설치합니다. 빌드 시 설치되는 Node 버전을 변경하려면, `docker-compose.yml` 파일에서 `laravel.test` 서비스의 `build.args`를 아래와 같이 수정하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일을 수정한 이후 컨테이너 이미지를 다시 빌드해주어야 합니다.


<!--     sail build --no-cache -->
    sail build --no-cache

<!--     sail up -->
    sail up


<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
동료에게 사이트를 보여주거나, 외부에서 애플리케이션에 webhook 테스트를 할 때 사이트를 임시로 외부에 공개하고 싶을 수 있습니다. 이럴 때는 `share` 명령어를 사용해서 사이트를 공유할 수 있습니다. 명령어를 실행하면, 애플리케이션에 접근할 수 있는 임의의 `laravel-sail.site` 도메인이 발급됩니다.


<!--     sail share -->
    sail share


<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies within the `TrustProxies` middleware. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` 명령어로 사이트를 공유할 때는 애플리케이션의 trusted proxy 미들웨어(`TrustProxies`)를 올바르게 설정해야 합니다. 그렇지 않으면, `url`이나 `route` 등의 URL 생성 헬퍼가 올바른 HTTP 호스트를 판단할 수 없습니다.

```
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
공유 URL의 서브도메인을 직접 지정하고 싶을 때는 `share` 명령어를 실행할 때 `subdomain` 옵션을 함께 사용할 수 있습니다.


<!--     sail share --subdomain=my-sail-site -->
    sail share --subdomain=my-sail-site


> [!TIP]
> `share` 명령어는 [Expose](https://beyondco.de)에서 제공하는 오픈소스 터널링 서비스 [BeyondCode](https://github.com/beyondcode/expose)를 사용합니다.

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. In order to enable Xdebug, you will need to add a few variables to your application's `.env` file to [configure Xdebug](https://xdebug.org/docs/step_debug#mode). To enable Xdebug you must set the appropriate mode(s) before starting Sail: -->
Laravel Sail의 Docker 설정에는 [Xdebug](https://xdebug.org/) 지원이 내장되어 있습니다. Xdebug는 PHP에서 널리 사용되는 강력한 디버거입니다. Xdebug를 사용하려면 애플리케이션 `.env` 파일에 몇 가지 변수를 추가해 [configure Xdebug](https://xdebug.org/docs/step_debug#mode)을 준비해야 합니다. Xdebug를 활성화하려면, Sail을 시작하기 전에 아래와 같이 모드를 지정하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux, you will need to manually define this environment variable. -->
내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 설정되어 Mac과 Windows(WSL2) 환경에 맞게 작동합니다. 하지만 리눅스 사용자의 경우, 이 환경 변수를 별도로 지정해야 할 수 있습니다.

<!-- First, you should determine the correct host IP address to add to the environment variable by running the following command. Typically, the `<container-name>` should be the name of the container that serves your application and often ends with `_laravel.test_1`: -->
먼저 아래 명령어로 올바른 호스트 IP 주소를 확인합니다. `<container-name>`에는 보통 `_laravel.test_1`로 끝나는 애플리케이션 컨테이너의 이름을 입력합니다.

```bash
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

<!-- Once you have obtained the correct host IP address, you should define the `SAIL_XDEBUG_CONFIG` variable within your application's `.env` file: -->
획득한 IP 주소로 `.env` 파일에 `SAIL_XDEBUG_CONFIG` 변수를 다음과 같이 정의합니다.

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
Artisan 명령어 실행 시 디버깅 세션을 시작하려면 `sail debug` 명령어를 사용합니다.

```bash
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
<!-- ### Xdebug Browser Usage -->
### Xdebug Browser Usage

<!-- To debug your application while interacting with the application via a web browser, follow the [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) for initiating an Xdebug session from the web browser. -->
웹 브라우저를 통해 애플리케이션을 이용하면서 디버깅하려면, Xdebug의 [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application)를 참고해 세션을 시작하십시오.

<!-- If you're using PhpStorm, please review JetBrain's documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm을 사용한다면, JetBrain 공식 문서에서 [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html) 내용을 확인하시기 바랍니다.

> [!NOTE]
> Laravel Sail은 애플리케이션 서비스를 위해 `artisan serve`를 사용합니다. `artisan serve` 명령은 Laravel 8.53.0 이상에서만 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 지원합니다. 8.52.0 이하 버전의 Laravel에서는 이 변수들이 지원되지 않으므로 디버그 접속이 동작하지 않습니다.

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail은 Docker 기반이므로 거의 모든 부분을 자유롭게 변경할 수 있습니다. Sail의 Dockerfile 등을 프로젝트에 복사하려면 아래와 같이 `sail:publish` 명령어를 실행합니다.

```bash
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
이 명령을 실행하면, Laravel Sail이 사용하는 Dockerfile 등 각종 설정 파일이 애플리케이션 루트의 `docker` 디렉터리에 복사됩니다. Sail 환경을 원하는 대로 커스터마이징한 뒤, `docker-compose.yml`에서 애플리케이션 컨테이너의 이미지 이름을 변경하고, 아래와 같이 `build` 명령어로 컨테이너를 재빌드할 수 있습니다. 여러 개의 Laravel 애플리케이션을 한 대의 머신에서 개발하는 경우, 애플리케이션마다 이미지 이름을 다르게 지정하는 것이 특히 유용합니다.

```bash
sail build --no-cache
```
