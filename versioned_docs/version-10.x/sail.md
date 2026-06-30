<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Configuring A Shell Alias](#configuring-a-shell-alias)
- [Starting and Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [Redis](#redis)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
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
[Laravel Sail](https://github.com/laravel/sail)은 Laravel 기본 Docker 개발 환경과 상호작용할 수 있는 가벼운 명령줄 인터페이스(CLI)입니다. Sail을 사용하면 Docker 사용 경험이 없어도 PHP, MySQL, Redis를 활용하여 Laravel 애플리케이션을 쉽게 구축할 수 있습니다.

<!-- At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file. -->
Sail의 핵심은 프로젝트 최상위 디렉터리에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml`로 정의된 Docker 컨테이너들과 편리하게 상호작용할 수 있는 CLI를 제공합니다.

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail은 macOS, Linux, 그리고 Windows( [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 를 통해)에서 지원됩니다.

<a name="installation"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<!-- Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/10.x/installation#docker-installation-using-sail) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with. -->
Laravel Sail은 모든 새로운 Laravel 애플리케이션에 자동으로 설치되므로 바로 사용할 수 있습니다. 새로운 Laravel 애플리케이션을 만드는 방법은 운영체제에 맞는 Laravel [installation documentation](/docs/10.x/installation#docker-installation-using-sail)를 참고하세요. 설치 과정에서 Sail이 지원하는 서비스 중, 어떤 서비스를 사용할지 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
<!-- ### Installing Sail Into Existing Applications -->
### Installing Sail Into Existing Applications

<!-- If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies: -->
기존 Laravel 애플리케이션에서 Sail을 사용하고 싶은 경우, Composer 패키지 관리자를 이용해 Sail을 설치할 수 있습니다. (이 단계는 로컬 개발 환경에서 Composer 패키지 설치가 가능한 상황을 전제로 합니다.)

```shell
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services: -->
Sail 설치가 완료되면, `sail:install` 아티즌 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 최상위 디렉터리에 복사하고, Docker 서비스에 연결하기 위해 `.env` 파일에 필요한 환경 변수도 자동으로 추가해줍니다.

```shell
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
마지막으로 Sail을 시작하면 됩니다. Sail 사용법에 대해 더 알아보고 싶으시다면 아래 설명을 계속 읽어주세요.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> 만약 Linux에서 Docker Desktop을 사용한다면, 아래 명령어를 실행해서 `default` Docker 컨텍스트를 사용하도록 설정해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
<!-- #### Adding Additional Services -->
#### Adding Additional Services

<!-- If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command: -->
이미 Sail이 설치된 환경에 다른 서비스를 추가하고 싶다면, `sail:add` 아티즌 명령어를 실행하면 됩니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고자 할 경우, `sail:install` 명령어에 `--devcontainer` 옵션을 추가할 수 있습니다. `--devcontainer` 옵션을 추가하면 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 최상위 디렉터리에 생성하도록 지시합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="configuring-a-shell-alias"></a>
<!-- ### Configuring A Shell Alias -->
### Configuring A Shell Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
기본적으로 Sail 명령어는 모든 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 통해 실행합니다.

```shell
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily: -->
하지만 매번 `vendor/bin/sail`를 입력하는 대신 shell 별칭을 설정하면 Sail 명령어를 더 쉽게 실행할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

<!-- To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell. -->
이 별칭이 항상 적용되도록 하려면, 사용 중인 shell의 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 위 명령어를 추가한 후, shell을 재시작하면 됩니다.

<!-- Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
별칭을 설정한 후에는 `sail`만 입력하여 Sail 명령어를 실행할 수 있습니다. 본 문서의 나머지 예제들도 이 별칭을 설정했다고 가정합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting and Stopping Sail -->
## Starting and Stopping Sail

<!-- Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail의 `docker-compose.yml` 파일은 Laravel 애플리케이션 개발을 위해 함께 작동하는 다양한 Docker 컨테이너를 정의합니다. 각 컨테이너는 `docker-compose.yml`의 `services` 설정 안에 항목으로 포함되어 있고, 이 중 `laravel.test` 컨테이너가 주요 애플리케이션 서버 역할을 합니다.

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command: -->
Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이 아닌지 확인하세요. 애플리케이션의 `docker-compose.yml`에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행합니다.

```shell
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
컨테이너들을 백그라운드(Detached) 모드로 실행하려면 다음과 같이 입력합니다.

```shell
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
컨테이너들이 시작되면 웹 브라우저를 통해 http://localhost 에서 프로젝트에 접속할 수 있습니다.

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
모든 컨테이너를 종료하려면 단순히 Control + C를 누르면 됩니다. 백그라운드로 실행 중인 경우에는 `stop` 명령어를 사용하면 됩니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되며 로컬 컴퓨터와 분리되어 있습니다. 하지만 Sail은 다양한 명령어(PHP, Artisan, Composer, Node / NPM 등)를 간편하게 실행할 수 있는 방법을 제공합니다.

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel 공식 문서를 보면 Composer, Artisan, Node / NPM 명령어 예제가 있는데, Sail을 명시하지 않은 경우가 많습니다.** 이는 해당 도구들이 로컬에 직접 설치되어 있다는 전제를 가진 예시입니다. Sail을 이용한다면, 이러한 명령어도 아래와 같이 Sail을 통해 실행해야 합니다.

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
PHP 명령어는 `php` 커맨드를 통해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에서 설정한 버전이 사용됩니다. Sail에서 지원하는 PHP 버전에 대해 자세히 알고 싶다면 [PHP version documentation](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer 2.x installation: -->
Composer 명령어는 `composer` 커맨드를 통해 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer 2.x가 기본 설치되어 있습니다.

```nothing
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
<!-- #### Installing Composer Dependencies for Existing Applications -->
#### Installing Composer Dependencies for Existing Applications

<!-- If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer. -->
여러 명이 함께 개발하는 프로젝트라면, 처음 Laravel 프로젝트를 만든 사람이 아닐 수 있습니다. 따라서, 애플리케이션의 Composer 의존성(즉, Sail 포함)이 프로젝트 복제 후 설치되어 있지 않을 수 있습니다.

<!-- You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies: -->
이런 경우 애플리케이션 디렉터리 안에서 다음 명령어를 실행해 의존 패키지를 설치할 수 있습니다. 이 명령어는 PHP와 Composer가 포함된 작은 Docker 컨테이너를 사용합니다.

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

<!-- When using the `laravelsail/phpXX-composer` image, you should use the same version of PHP that you plan to use for your application (`80`, `81`, `82`, or `83`). -->
`laravelsail/phpXX-composer` 이미지를 사용할 때는 애플리케이션에서 사용하려는 PHP 버전(`80`, `81`, `82`, `83` 중 하나)을 맞추어 사용해야 합니다.

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel Artisan 명령어는 `artisan` 커맨드를 통해 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
Node 명령어는 `node`, NPM 명령어는 `npm`을 사용해 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

<!-- If you wish, you may use Yarn instead of NPM: -->
원한다면 NPM 대신 Yarn을 사용할 수도 있습니다.

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
애플리케이션의 `docker-compose.yml` 파일에는 MySQL 컨테이너에 대한 항목이 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하거나 다시 시작해도 데이터가 보존됩니다.

<!-- In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data. -->
또한, MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 자동으로 생성됩니다. 첫 번째는 `DB_DATABASE` 환경 변수의 값으로 된 데이터베이스로, 개발용입니다. 두 번째는 테스트 전용 데이터베이스인 `testing`이며, 테스트 데이터와 개발 데이터가 섞이지 않도록 해줍니다.

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
컨테이너를 시작한 후에는, 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정하면 컨테이너 내부 MySQL에 연결할 수 있습니다.

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password. -->
로컬 PC에서 애플리케이션의 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com)와 같은 GUI 데이터베이스 관리 앱을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근할 수 있으며, 접속 계정은 `DB_USERNAME`, `DB_PASSWORD` 환경 변수 값을 사용합니다. 혹은 `root` 유저로 접속해도 되며, 이때도 비밀번호는 `DB_PASSWORD` 값을 사용합니다.

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis data is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
애플리케이션의 `docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너에 대한 항목도 포함되어 있습니다. 이 컨테이너 역시 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용해, 컨테이너가 중지되거나 재시작되어도 데이터가 보존됩니다. 컨테이너를 시작한 후에는, 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `redis`로 설정하여 내부 Redis에 접속할 수 있습니다.

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
로컬 머신에서 Redis 데이터베이스에 연결할 때는 [TablePlus](https://tableplus.com)와 같은 앱을 활용할 수 있습니다. 기본적으로 Redis는 `localhost` 포트 6379에서 접근할 수 있습니다.

<a name="meilisearch"></a>
<!-- ### Meilisearch -->
### Meilisearch

<!-- If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search-engine that is [compatible](https://github.com/meilisearch/meilisearch-laravel-scout) with [Laravel Scout](/docs/10.x/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면, 애플리케이션의 `docker-compose.yml` 파일에 이 강력한 검색엔진에 대한 항목이 추가됩니다. Meilisearch는 [compatible](https://github.com/meilisearch/meilisearch-laravel-scout)와 [Laravel Scout](/docs/10.x/scout)됩니다. 컨테이너를 시작한 후, 애플리케이션의 `MEILISEARCH_HOST` 환경변수를 `http://meilisearch:7700`으로 설정해 연결할 수 있습니다.

<!-- From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
로컬 머신에서는 브라우저로 `http://localhost:7700`에 접속해 Meilisearch 웹 관리자 패널에 접근할 수 있습니다.

<a name="typesense"></a>
<!-- ### Typesense -->
### Typesense

<!-- If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this lightning fast, open-source search-engine that is natively integrated with [Laravel Scout](/docs/10.x/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables: -->
Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml`에 네이티브로 [Laravel Scout](/docs/10.x/scout#typesense)와 통합된 고성능 오픈소스 검색 엔진 항목이 추가됩니다. 컨테이너 기동 후, 아래와 같이 환경변수를 설정하여 Typesense 인스턴스에 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

<!-- From your local machine, you may access Typesense's API via `http://localhost:8108`. -->
로컬 머신에서는 `http://localhost:8108`에서 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file. -->
프로덕션 환경에서 파일을 Amazon S3에 저장할 계획이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 함께 설치하는 것이 좋습니다. MinIO는 S3와 호환되는 API를 제공하므로, 실제 S3에 테스트 버킷을 만들지 않아도 Laravel에서 `s3` 드라이버로 로컬에서 개발할 수 있습니다. MinIO를 선택하면, `docker-compose.yml`에 MinIO 설정이 추가됩니다.

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows: -->
기본적으로 애플리케이션의 파일 시스템 설정(`filesystems` 설정 파일)에는 이미 `s3` 디스크 구성이 들어 있습니다. Amazon S3뿐만 아니라 MinIO처럼 S3 호환 파일 저장소도 연동할 수 있는데, 환경 변수만 적절히 변경하면 됩니다. 예를 들어 MinIO를 사용할 때는 다음과 같이 설정합니다.

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
Laravel의 Flysystem 연동에서 MinIO를 사용할 때 올바른 URL을 생성하려면, `AWS_URL` 환경 변수를 애플리케이션의 로컬 주소와 버킷 이름까지 포함해 지정해야 합니다.

```ini
AWS_URL=http://localhost:9000/local
```

<!-- You may create buckets via the MinIO console, which is available at `http://localhost:8900`. The default username for the MinIO console is `sail` while the default password is `password`. -->
버킷은 MinIO 콘솔(`http://localhost:8900`)에서 생성할 수 있습니다. MinIO 콘솔의 기본 아이디는 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO를 사용할 때는 `temporaryUrl` 메서드로 임시 저장소 URL을 생성하는 기능이 지원되지 않습니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/10.x/testing). Any CLI options that are accepted by PHPUnit may also be passed to the `test` command: -->
Laravel은 강력한 테스트 도구를 기본으로 제공합니다. Sail의 `test` 명령어를 통해 [feature and unit tests](/docs/10.x/testing)를 실행할 수 있습니다. 그리고 PHPUnit에서 사용하는 모든 CLI 옵션 역시 `test` 명령어에 그대로 전달할 수 있습니다.

```shell
sail test

sail test --group orders
```

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail의 `test` 명령어는 사실상 `test` 아티즌 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

<!-- By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests: -->
Sail은 기본적으로 테스트 전용 `testing` 데이터베이스를 생성해, 테스트 수행 시 여러분의 실제 데이터베이스 상태를 변경하지 않도록 해줍니다. Laravel 기본 설치에서는 `phpunit.xml` 파일도 이 데이터베이스를 사용하도록 자동으로 설정되어 있습니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/10.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file: -->
[Laravel Dusk](/docs/10.x/dusk)는 쉽고 강력한 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 Selenium이나 다른 도구를 로컬에 설치하지 않아도 Dusk 테스트를 실행할 수 있습니다. 우선, 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스 부분을 주석 해제(uncomment) 하세요.

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

<!-- Next, ensure that the `laravel.test` service in your application's `docker-compose.yml` file has a `depends_on` entry for `selenium`: -->
그리고 애플리케이션의 `docker-compose.yml` 파일에 있는 `laravel.test` 서비스에 `selenium`을 `depends_on` 항목으로 추가해야 합니다.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
이후 Sail을 시작하고, 아래처럼 `dusk` 명령어로 Dusk 테스트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium on Apple Silicon -->
#### Selenium on Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `seleniarm/standalone-chromium` image: -->
Apple Silicon 칩이 탑재된 머신을 사용할 경우, `selenium` 서비스는 `seleniarm/standalone-chromium` 이미지를 사용해야 합니다.

```yaml
selenium:
    image: 'seleniarm/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```

<a name="previewing-emails"></a>
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `docker-compose.yml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025: -->
Laravel Sail의 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 발송된 이메일을 가로채어, 브라우저에서 이메일 메시지를 미리볼 수 있는 웹 인터페이스를 제공합니다. Sail 사용 시 Mailpit의 호스트명은 `mailpit`이고, 포트는 1025입니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the Mailpit web interface at: http://localhost:8025 -->
Sail이 실행 중이면, http://localhost:8025 에서 Mailpit 웹 인터페이스에 접속할 수 있습니다.

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well execute arbitrary shell commands within the container: -->
때때로 애플리케이션 컨테이너 내에서 Bash 세션을 시작해 파일이나 설치된 서비스를 직접 살펴보거나, 임의의 shell 명령어를 실행하고 싶을 수 있습니다. 이럴 때는 `shell` 명령어를 사용해 컨테이너에 접속할 수 있습니다.

```shell
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
[Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하고 싶다면, `tinker` 명령어를 실행하면 됩니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.3. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file: -->
Sail은 현재 PHP 8.3, 8.2, 8.1, 8.0을 지원합니다. 기본적으로 Sail에서 사용하는 PHP 버전은 8.3입니다. 다른 PHP 버전으로 변경하려면, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 설정을 아래와 같이 업데이트하면 됩니다.

```yaml
# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file: -->
또한, `image` 이름도 현재 사용 중인 PHP 버전에 맞게 변경하는 것이 좋습니다. 이 설정 역시 `docker-compose.yml`에서 정의합니다.

```yaml
image: sail-8.1/app
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일을 수정한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 20 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file: -->
Sail은 기본적으로 Node 20을 설치합니다. 이미지를 빌드할 때 설치되는 Node 버전을 바꾸고 싶다면, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스의 `build.args` 설정을 업데이트하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일을 수정한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
동료에게 사이트를 미리 보여주거나, 웹훅(Webhook) 같은 외부 연동 기능을 테스트할 때 사이트를 외부에 공개해야 할 수도 있습니다. 이럴 땐 `share` 명령어를 이용해 사이트를 공유할 수 있습니다. 명령어 실행 후, 애플리케이션에 접근할 수 있는 임의의 `laravel-sail.site` URL이 발급됩니다.

```shell
sail share
```

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies within the `TrustProxies` middleware. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` 명령어로 사이트를 외부에 공유할 때는, 애플리케이션의 `TrustProxies` 미들웨어에서 신뢰할 수 있는 프록시를 올바르게 설정해야 합니다. 그렇지 않으면 `url`, `route` 등 URL 생성 관련 헬퍼에서 올바른 HTTP 호스트 정보를 얻지 못할 수 있습니다.

```
/**
 * The trusted proxies for this application.
 *
 * @var array|string|null
 */
protected $proxies = '*';
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
공유 사이트의 서브도메인을 직접 지정하고 싶다면, `share` 명령어를 실행할 때 `subdomain` 옵션을 추가하면 됩니다.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [Expose](https://github.com/beyondcode/expose) 기반으로 동작하며, 이는 [BeyondCode](https://beyondco.de)에서 만든 오픈 소스 터널링 서비스입니다.

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. In order to enable Xdebug, you will need to add a few variables to your application's `.env` file to [configure Xdebug](https://xdebug.org/docs/step_debug#mode). To enable Xdebug you must set the appropriate mode(s) before starting Sail: -->
Laravel Sail의 Docker 구성에는 [Xdebug](https://xdebug.org/) 지원이 내장되어 있습니다. Xdebug는 PHP 개발에 널리 사용되는 강력한 디버거입니다. Xdebug를 활성화하려면 `.env` 파일에 몇 가지 환경 변수를 추가해 [configure Xdebug](https://xdebug.org/docs/step_debug#mode)해야 하며, Sail을 시작하기 전에 모드 값을 지정해야 합니다.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux, you should ensure that you are running Docker Engine 17.06.0+ and Compose 1.16.0+. Otherwise, you will need to manually define this environment variable as shown below. -->
내부적으로 `XDEBUG_CONFIG` 환경 변수에 `client_host=host.docker.internal`이 지정되어 있으므로, Mac이나 Windows(WSL2)에서는 별도의 설정 없이도 Xdebug를 바로 사용할 수 있습니다. 하지만 Linux 환경에서는 Docker Engine 17.06.0+와 Compose 1.16.0+ 이상을 사용해야 하며, 그렇지 않은 경우에는 아래와 같이 직접 환경 변수를 지정해야 합니다.

<!-- First, you should determine the correct host IP address to add to the environment variable by running the following command. Typically, the `<container-name>` should be the name of the container that serves your application and often ends with `_laravel.test_1`: -->
먼저, 다음 명령어를 활용해 올바른 호스트 IP 주소를 구해야 합니다. `<container-name>`에는 실제로 애플리케이션을 제공하는 컨테이너 이름(보통 `_laravel.test_1`로 끝남)을 사용하세요.

```shell
docker inspect -f {{range.NetworkSettings.Networks}}{{.Gateway}}{{end}} <container-name>
```

<!-- Once you have obtained the correct host IP address, you should define the `SAIL_XDEBUG_CONFIG` variable within your application's `.env` file: -->
IP 주소를 확인했다면, 해당 값을 `.env` 파일의 `SAIL_XDEBUG_CONFIG` 환경 변수에 지정해주세요.

```ini
SAIL_XDEBUG_CONFIG="client_host=<host-ip-address>"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
Artisan 명령어를 실행할 때 디버깅 세션을 시작하려면, `sail debug` 명령어를 사용할 수 있습니다.

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
애플리케이션에 웹브라우저로 접속할 때 디버깅을 원한다면, Xdebug에서 제공하는 [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application)을 참고해 세션을 시작하세요.

<!-- If you're using PhpStorm, please review JetBrain's documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
만약 PhpStorm을 사용한다면, [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrain 공식 문서를 참고하면 도움이 됩니다.

> [!WARNING]
> Laravel Sail은 애플리케이션 구동 시 `artisan serve` 명령어를 사용합니다. `artisan serve` 명령어는 Laravel 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수를 지원합니다. Laravel 8.52.0 이하 버전에서는 해당 변수를 지원하지 않으므로, 디버깅 연결이 되지 않습니다.

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail은 Docker 기반이므로, 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail의 자체 Dockerfile을 퍼블리시하려면 `sail:publish` 명령어를 실행하면 됩니다.

```shell
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
이 명령어를 실행하면, Laravel Sail이 사용하는 Dockerfile 및 기타 설정 파일들이 애플리케이션의 `docker` 디렉터리에 복사됩니다. Sail 설치를 커스터마이즈한 후에는, 애플리케이션 컨테이너의 이미지 이름을 `docker-compose.yml`에서 변경할 수 있습니다. 그 후, `build` 명령어로 컨테이너를 다시 빌드해야 합니다. 특히 한 컴퓨터에서 여러 Laravel 애플리케이션을 개발한다면, 각 애플리케이션마다 이미지 이름을 다르게 지정하는 것이 좋습니다.

```shell
sail build --no-cache
```
