<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation & Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Configuring A Shell Alias](#configuring-a-shell-alias)
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
[Laravel Sail](https://github.com/laravel/sail)은 Laravel 기본 Docker 개발 환경과 상호작용하기 위한 가볍고 편리한 커맨드라인 도구입니다. Sail을 이용하면 Docker에 대한 사전 지식 없이도 PHP, MySQL, Redis를 활용해 Laravel 애플리케이션을 쉽게 구축할 수 있습니다.

<!-- At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file. -->
Sail의 핵심은 프로젝트 루트에 저장된 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml` 파일에 정의된 Docker 컨테이너들과 쉽게 상호작용할 수 있는 CLI를 제공합니다.

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail은 macOS, Linux, 그리고 Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 를 통해)에서 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation & Setup -->
## Installation & Setup

<!-- Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/9.x/installation) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with. -->
Laravel Sail은 모든 신규 Laravel 애플리케이션에 자동으로 설치되므로 즉시 사용할 수 있습니다. 새로운 Laravel 애플리케이션을 만드는 방법은 운영체제에 맞는 Laravel [installation documentation](/docs/9.x/installation)를 참고하세요. 설치 과정에서 Sail이 지원하는 서비스 중 어떤 것과 연동할지 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
<!-- ### Installing Sail Into Existing Applications -->
### Installing Sail Into Existing Applications

<!-- If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies: -->
기존의 Laravel 애플리케이션에서 Sail을 사용하고 싶다면, Composer 패키지 관리자를 통해 Sail을 설치할 수 있습니다. 당연히, 이 과정은 현재의 로컬 개발 환경에서 Composer 패키지 설치가 가능한 경우를 가정합니다.

```shell
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application: -->
Sail 설치 후, `sail:install` Artisan 명령어를 실행하면 Sail의 `docker-compose.yml` 파일이 애플리케이션의 루트에 생성됩니다.

```shell
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
마지막으로 Sail을 시작할 수 있습니다. Sail의 사용 방법에 대해 더 자세히 알아보고 싶다면 아래 문서를 계속 참고하시면 됩니다.

```shell
./vendor/bin/sail up
```

<a name="adding-additional-services"></a>
<!-- #### Adding Additional Services -->
#### Adding Additional Services

<!-- If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command: -->
기존 Sail 설치 환경에 다른 서비스를 추가하고 싶으면, `sail:add` Artisan 명령어를 실행할 수 있습니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 내에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 추가합니다. `--devcontainer` 옵션은 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 루트에 생성하도록 합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
<!-- ### Configuring A Shell Alias -->
### Configuring A Shell Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
기본적으로 Sail 명령어는 신규 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용해서 실행합니다.

```shell
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily: -->
하지만, 매번 `vendor/bin/sail`을 입력하는 대신 간편하게 사용할 수 있도록 셸 alias를 설정할 수 있습니다.

```shell
alias sail='[ -f sail ] && sh sail || sh vendor/bin/sail'
```

<!-- To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell. -->
이 alias가 항상 사용 가능하도록 하려면, 홈 디렉터리의 셸 설정 파일(`~/.zshrc`, `~/.bashrc` 등)에 이 내용을 추가한 뒤 셸을 재시작하세요.

<!-- Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
별칭이 설정되면 이제 간단하게 `sail`만 입력해도 Sail 명령어를 사용할 수 있습니다. 이후 이 문서의 모든 예제에서는 alias 설정을 했다고 가정합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting & Stopping Sail -->
## Starting & Stopping Sail

<!-- Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 개발에 필요한 다양한 Docker 컨테이너 설정이 담겨 있습니다. 각 컨테이너는 `docker-compose.yml` 파일의 `services` 항목에 정의됩니다. 이 중 `laravel.test` 컨테이너가 실제로 애플리케이션을 서비스하는 기본 컨테이너입니다.

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command: -->
Sail을 시작하기 전에, 컴퓨터에 기존의 웹 서버나 데이터베이스가 실행되고 있지 않은지 확인하세요. 애플리케이션의 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 실행하려면 아래와 같이 `up` 명령어를 사용합니다.

```shell
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
컨테이너를 백그라운드에서 실행하려면, "detached" 모드로 시작할 수 있습니다.

```shell
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
컨테이너가 모두 시작되면, 웹 브라우저에서 http://localhost 로 접속해 프로젝트를 확인할 수 있습니다.

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
모든 컨테이너를 중지하려면 Control + C를 누르거나, 백그라운드에서 컨테이너가 실행 중일 때는 `stop` 명령어를 사용할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되어 로컬 컴퓨터와 분리되어 있습니다. 하지만, Sail은 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어 등 다양한 명령어를 편리하게 실행할 수 있는 방법을 제공합니다.

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel 공식 문서에서 Composer, Artisan, Node / NPM 명령어 등이 Sail을 언급하지 않고 나오는 경우가 많습니다.** 이러한 예시는 해당 도구들이 로컬 컴퓨터에 설치되어 있다고 가정하기 때문입니다. Sail을 이용해 개발 환경을 구축한 경우, 반드시 Sail 명령어로 해당 작업을 실행해야 합니다.

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```

<a name="executing-php-commands"></a>
<!-- ### Executing PHP Commands -->
### Executing PHP Commands

<!-- PHP commands may be executed using the `php` command. Of course, these commands will execute using the PHP version that is configured for your application. To learn more about the PHP versions available to Laravel Sail, consult the [PHP version documentation](#sail-php-versions): -->
PHP 명령어는 `php` 명령어를 통해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전이 사용됩니다. Sail에서 지원하는 PHP 버전에 대한 자세한 내용은 [PHP version documentation](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer 2.x installation: -->
Composer 명령어는 `composer` 명령어를 통해 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer 2.x가 이미 설치되어 있습니다.

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
<!-- #### Installing Composer Dependencies For Existing Applications -->
#### Installing Composer Dependencies For Existing Applications

<!-- If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer. -->
여러 명이 함께 개발하는 프로젝트에서는, 자신이 직접 Laravel 애플리케이션을 생성하지 않았을 가능성이 높습니다. 이 경우, 애플리케이션의 Composer 의존성(즉, Sail을 포함한 모든 패키지)이 새로 clone한 로컬 컴퓨터에 설치되지 않은 상태일 수 있습니다.

<!-- You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies: -->
이런 경우, 애플리케이션 디렉터리로 이동한 후 아래 명령어를 실행해 Composer 의존성을 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 들어있는 작은 Docker 컨테이너를 사용합니다.

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php82-composer:latest \
    composer install --ignore-platform-reqs
```

<!-- When using the `laravelsail/phpXX-composer` image, you should use the same version of PHP that you plan to use for your application (`74`, `80`, `81`, or `82`). -->
`laravelsail/phpXX-composer` 이미지를 사용할 때는, 실제 애플리케이션에서 사용할 PHP 버전(`74`, `80`, `81`, `82`)과 동일한 버전을 선택해야 합니다.

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel Artisan 명령어는 `artisan` 명령어를 이용해 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
Node 명령어는 `node` 명령어로, NPM 명령어는 `npm` 명령어로 각각 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

<!-- If you wish, you may use Yarn instead of NPM: -->
필요하다면 NPM 대신 Yarn을 사용할 수도 있습니다.

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
<!-- ## Interacting With Databases -->
## Interacting With Databases

<a name="mysql"></a>
<!-- ### MySQL -->
### MySQL

<!-- As you may have noticed, your application's `docker-compose.yml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너가 정의되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너 중지나 재시작에도 데이터가 안전하게 유지됩니다.

<!-- In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data. -->
또한 MySQL 컨테이너가 처음 시작될 때, 두 개의 데이터베이스가 자동으로 생성됩니다. 첫 번째는 `DB_DATABASE` 환경 변수 값으로 명명되어 실제 개발에 사용하며, 두 번째는 `testing`이라는 테스트 전용 데이터베이스로, 테스트 실행 시 개발 데이터에 영향을 주지 않도록 분리되어 있습니다.

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
컨테이너가 모두 시작된 후, `.env` 파일의 `DB_HOST` 환경 변수 값을 `mysql`로 설정해야 애플리케이션에서 MySQL 인스턴스에 정상적으로 연결됩니다.

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password. -->
로컬 컴퓨터에서 MySQL DB에 접속하려면 [TablePlus](https://tableplus.com)와 같은 GUI DB 관리 도구를 사용할 수 있습니다. 기본적으로 MySQL DB는 `localhost`, 포트 3306에서 열려 있으며, 접근 계정 정보는 `DB_USERNAME`, `DB_PASSWORD` 환경 변수 값을 따릅니다. 또는 `root` 사용자로, 비밀번호는 역시 `DB_PASSWORD` 값을 사용해 접속할 수도 있습니다.

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
애플리케이션의 `docker-compose.yml` 파일엔 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너 역시 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용해 데이터를 보존합니다. 컨테이너가 모두 시작되면, `.env` 파일의 `REDIS_HOST` 변수 값을 `redis`로 설정해 애플리케이션에서 Redis 인스턴스에 접속할 수 있습니다.

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
로컬 컴퓨터에서는 [TablePlus](https://tableplus.com)와 같은 GUI 도구로 Redis 데이터베이스에 접속할 수 있습니다. 기본적으로 Redis는 `localhost`, 포트 6379에서 접근할 수 있습니다.

<a name="meilisearch"></a>
<!-- ### MeiliSearch -->
### MeiliSearch

<!-- If you chose to install the [MeiliSearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search-engine that is [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) with [Laravel Scout](/docs/9.x/scout). Once you have started your containers, you may connect to the MeiliSearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail 설치할 때 [MeiliSearch](https://www.meilisearch.com) 서비스를 선택했다면, 애플리케이션의 `docker-compose.yml` 파일에 강력한 검색 엔진인 MeiliSearch 컨테이너가 추가됩니다. MeiliSearch는 [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) 와 [Laravel Scout](/docs/9.x/scout)됩니다. 컨테이너가 모두 시작되면, .env 파일의 `MEILISEARCH_HOST` 환경 변수 값을 `http://meilisearch:7700`으로 설정해 사용합니다.

<!-- From your local machine, you may access MeiliSearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
로컬 컴퓨터에서 MeiliSearch의 웹 관리 패널에 접속하려면 브라우저에서 `http://localhost:7700`으로 이동하면 됩니다.

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file. -->
프로덕션 환경에서 파일 저장 용도로 Amazon S3를 사용할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 추가할 수 있습니다. MinIO는 로컬 개발 중 별도의 프로덕션 S3 환경에 "테스트" 버킷을 만들 필요 없이 Laravel의 `s3` 파일 스토리지 드라이버와 호환되는 S3 API를 제공합니다. MinIO를 설치하면 `docker-compose.yml` 파일에 MinIO 관련 설정이 추가됩니다.

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows: -->
기본적으로 애플리케이션의 `filesystems` 설정 파일에는 이미 `s3` 디스크 설정이 포함되어 있습니다. Amazon S3뿐만 아니라 MinIO 등 S3 호환 파일 스토리지와 연동하려면 관련 환경 변수를 다음과 같이 수정하면 됩니다.

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://minio:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```

<!-- In order for Laravel's Flysystem integration to generate proper URLs when using MinIO, you should define the `AWS_URL` environment variable so that it matches your application's local URL and includes the bucket name in the URL path: -->
Laravel의 Flysystem 통합 기능이 MinIO를 사용할 때 올바른 URL을 생성하도록 하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 URL과 버킷명이 포함된 경로로 지정해 주어야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

<!-- You may create buckets via the MinIO console, which is available at `http://localhost:8900`. The default username for the MinIO console is `sail` while the default password is `password`. -->
MinIO의 콘솔(관리자 페이지)은 `http://localhost:8900`에서 접속할 수 있으며, 기본 사용자명은 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> `temporaryUrl` 메서드를 이용해 임시 저장소 URL을 생성하는 기능은 MinIO 사용 시 지원되지 않습니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/9.x/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command: -->
Laravel은 기본적으로 뛰어난 테스트 지원 기능을 제공합니다. Sail의 `test` 명령어를 이용해 애플리케이션의 [feature and unit tests](/docs/9.x/testing)를 실행할 수 있습니다. PHPUnit이 지원하는 모든 CLI 옵션도 `test` 명령어에 함께 사용할 수 있습니다.

```shell
sail test

sail test --group orders
```

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail의 `test` 명령어는 다음과 같이 Artisan의 `test` 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

<!-- By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests: -->
Sail은 기본적으로 테스트 실행 시 기존 데이터베이스와 충돌하지 않도록 전용 `testing` 데이터베이스를 생성하고, 애플리케이션의 `phpunit.xml` 파일에도 이를 사용하도록 자동으로 설정합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/9.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file: -->
[Laravel Dusk](/docs/9.x/dusk)는 쉽고 직관적으로 브라우저 자동화 및 테스트를 작성할 수 있는 API를 제공합니다. Sail을 사용하면 로컬에 Selenium이나 기타 도구를 별도로 설치하지 않고 Dusk 테스트를 실행할 수 있습니다. 우선, `docker-compose.yml` 파일에서 Selenium 서비스의 주석을 해제합니다.

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<!-- Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`: -->
그런 다음, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스에 `selenium`이 `depends_on`에 포함되어 있는지 확인합니다.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
이제 Sail을 실행한 뒤, 아래와 같이 `dusk` 명령어로 Dusk 테스트를 수행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium On Apple Silicon -->
#### Selenium On Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `seleniarm/standalone-chromium` image: -->
로컬 컴퓨터에 Apple Silicon 칩이 있다면, `selenium` 서비스는 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다.

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

<!-- Laravel Sail's default `docker-compose.yml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025: -->
Laravel Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스도 포함되어 있습니다. Mailpit은 로컬 개발 환경에서 애플리케이션이 보내는 이메일을 가로채 웹 인터페이스에서 직접 미리볼 수 있는 편리한 도구입니다. Sail 환경에서 Mailpit의 기본 호스트는 `mailpit`이며, 포트 1025를 사용합니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the Mailpit web interface at: http://localhost:8025 -->
Sail이 실행 중일 때 웹 브라우저로 http://localhost:8025 에 접속해 Mailpit 웹 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well execute arbitrary shell commands within the container: -->
가끔 애플리케이션 컨테이너에서 Bash 세션을 시작해 내부 파일이나 설치된 서비스 확인, 임의의 셸 명령어 실행 등이 필요할 수 있습니다. 이럴 땐 `shell` 명령어를 사용해 컨테이너에 직접 접속할 수 있습니다.

```shell
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
또한, [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 다음과 같이 `tinker` 명령어를 사용합니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.2, 8.1, PHP 8.0, or PHP 7.4. The default PHP version used by Sail is currently PHP 8.2. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file: -->
Sail은 PHP 8.2, 8.1, 8.0, 7.4 등 다양한 버전으로 애플리케이션을 실행할 수 있게 지원합니다. 기본적으로는 PHP 8.2가 사용됩니다. PHP 버전을 변경하려면 `docker-compose.yml`의 `laravel.test` 컨테이너의 `build` 항목을 다음과 같이 수정하면 됩니다.

```yaml
# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0

# PHP 7.4
context: ./vendor/laravel/sail/runtimes/7.4
```

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file: -->
또한, 사용하는 PHP 버전에 맞게 `image` 이름도 변경할 수 있습니다. 이 설정 역시 `docker-compose.yml` 파일에서 관리합니다.

```yaml
image: sail-8.1/app
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일 설정을 변경한 뒤에는 반드시 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 18 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file: -->
기본적으로 Sail은 Node 18을 설치합니다. 빌드 이미지에 설치되는 Node 버전을 바꾸고 싶다면, `docker-compose.yml` 파일의 `laravel.test` 서비스에서 `build.args` 항목 값을 원하는 버전으로 변경하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '14'
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일 변경 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
동료에게 웹사이트를 미리 보여주거나, 웹훅 등 외부와의 연동 테스트를 위해 사이트를 외부에 임시로 공개해야 할 때가 있습니다. 이럴 때 `share` 명령어를 사용하면 됩니다. 명령어 실행 시 무작위로 생성된 `laravel-sail.site` 도메인이 할당되어 외부에서 접속할 수 있게 됩니다.

```shell
sail share
```

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies within the `TrustProxies` middleware. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` 명령어로 사이트를 공유할 때는, 애플리케이션의 `TrustProxies` 미들웨어에서 신뢰할 수 있는 프록시 설정을 해주어야 URL 생성 헬퍼(`url`, `route` 등)가 올바른 HTTP 호스트 정보를 사용할 수 있습니다.

```
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
특정 서브도메인으로 사이트를 공유하고 싶을 때는 `share` 명령어 실행 시 `subdomain` 옵션을 지정할 수 있습니다.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [Expose](https://github.com/beyondcode/expose)에서 제공하는 오픈소스 터널링 서비스 [BeyondCode](https://beyondco.de)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. In order to enable Xdebug, you will need to add a few variables to your application's `.env` file to [configure Xdebug](https://xdebug.org/docs/step_debug#mode). To enable Xdebug you must set the appropriate mode(s) before starting Sail: -->
Laravel Sail의 Docker 설정에는 PHP를 위한 강력한 디버거인 [Xdebug](https://xdebug.org/)가 지원됩니다. Xdebug를 활성화하려면 몇 가지 변수를 애플리케이션의 `.env` 파일에 추가해 [configure Xdebug](https://xdebug.org/docs/step_debug#mode)을 해야 하며, Sail을 시작하기 전에 올바른 모드 값을 지정해야 합니다.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux, you should ensure that you are running Docker Engine 17.06.0+ and Compose 1.16.0+. Otherwise, you will need to manually define this environment variable as shown below. -->
내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 지정되어 있어서 Mac 및 Windows(WSL2) 환경에서 자동으로 Xdebug가 동작합니다. 만약 로컬 머신이 Linux라면, Docker Engine 17.06.0+ 및 Compose 1.16.0+ 버전 이상을 사용하는지 확인해야 하며, 그렇지 않다면 아래와 같이 환경 변수를 수동으로 정의해야 할 수도 있습니다.

<!-- First, you should determine the correct host IP address to add to the environment variable by running the following command. Typically, the `<container-name>` should be the name of the container that serves your application and often ends with `_laravel.test_1`: -->
가장 먼저 아래 명령어로 환경 변수에 추가할 올바른 호스트 IP 주소를 알아내야 합니다. `<container-name>`에는 애플리케이션을 구동하는 컨테이너명을 입력합니다. 일반적으로 `_laravel.test_1`로 끝나는 이름입니다.

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

<!-- Once you have obtained the correct host IP address, you should define the `SAIL_XDEBUG_CONFIG` variable within your application's `.env` file: -->
알맞은 호스트 IP를 알게 됐다면, `.env` 파일에 `SAIL_XDEBUG_CONFIG` 변수를 다음과 같이 추가합니다.

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
`sail debug` 명령어를 활용하면 Artisan 명령어 실행 시 디버깅 세션을 시작할 수 있습니다.

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```

<a name="xdebug-browser-usage"></a>
<!-- ### Xdebug Browser Usage -->
### Xdebug Browser Usage

<!-- To debug your application while interacting with the application via a web browser, follow the [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application) for initiating an Xdebug session from the web browser. -->
웹 브라우저에서 애플리케이션을 직접 조작하면서 디버깅하려면, [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application)를 참고해 브라우저에서 Xdebug 세션을 시작하세요.

<!-- If you're using PhpStorm, please review JetBrain's documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm을 사용하는 경우, [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 대해 JetBrain 공식 문서를 참고하면 도움이 됩니다.

> [!WARNING]
> Laravel Sail은 애플리케이션을 서비스할 때 `artisan serve`를 사용합니다. `artisan serve` 명령은 Laravel 8.53.0 버전부터서만 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수를 인식합니다. 8.52.0 이하의 버전은 이 변수를 지원하지 않아 디버깅 연결이 불가능합니다.

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail은 기본적으로 Docker 환경을 사용하기 때문에 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail에서 사용하는 Dockerfile들을 직접 프로젝트에 복사하려면 `sail:publish` 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
명령 실행 후, Laravel Sail에 사용되는 Dockerfile과 기타 설정 파일들이 애플리케이션의 루트에 `docker` 디렉터리 내부에 생성됩니다. 커스터마이즈를 마친 뒤에는 `docker-compose.yml` 파일에서 애플리케이션 컨테이너의 이미지 이름 변경을 고려할 수 있고, 변경 후에는 반드시 `build` 명령어로 컨테이너를 다시 빌드해야 합니다. 여러 개의 Laravel 애플리케이션을 한 컴퓨터에서 개발할 때, 이미지를 고유하게 지정하는 것이 특히 중요합니다.

```shell
sail build --no-cache
```
