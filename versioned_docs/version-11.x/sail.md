<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
    - [Installing Sail Into Existing Applications](#installing-sail-into-existing-applications)
    - [Rebuilding Sail Images](#rebuilding-sail-images)
    - [Configuring A Shell Alias](#configuring-a-shell-alias)
- [Starting and Stopping Sail](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
    - [Executing PHP Commands](#executing-php-commands)
    - [Executing Composer Commands](#executing-composer-commands)
    - [Executing Artisan Commands](#executing-artisan-commands)
    - [Executing Node / NPM Commands](#executing-node-npm-commands)
- [Interacting With Databases](#interacting-with-sail-databases)
    - [MySQL](#mysql)
    - [MongoDB](#mongodb)
    - [Redis](#redis)
    - [Valkey](#valkey)
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
[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용할 수 있는 가볍고 간단한 커맨드라인 인터페이스(CLI)입니다. Sail을 사용하면 Docker에 대해 사전 지식이 없어도 PHP, MySQL, Redis로 Laravel 애플리케이션을 쉽게 시작할 수 있습니다.

<!-- At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file. -->
Sail의 핵심은 프로젝트 루트에 위치한 `docker-compose.yml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `docker-compose.yml`에 정의된 Docker 컨테이너들과 쉽게 상호작용할 수 있는 CLI 명령들을 제공합니다.

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail은 macOS, Linux, 그리고 Windows([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about) 통해)에서 지원됩니다.

<a name="installation"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<!-- Laravel Sail is automatically installed with all new Laravel applications so you may start using it immediately. To learn how to create a new Laravel application, please consult Laravel's [installation documentation](/docs/11.x/installation#docker-installation-using-sail) for your operating system. During installation, you will be asked to choose which Sail supported services your application will be interacting with. -->
Laravel Sail은 새로운 Laravel 애플리케이션 생성 시 자동으로 설치되므로 바로 사용을 시작할 수 있습니다. 새 Laravel 애플리케이션 생성 방법은 운영체제별 Laravel [installation documentation](/docs/11.x/installation#docker-installation-using-sail)를 참고해 주세요. 설치 과정 중, Sail이 지원하는 서비스 중 어떤 서비스를 사용할지 선택하게 됩니다.

<a name="installing-sail-into-existing-applications"></a>
<!-- ### Installing Sail Into Existing Applications -->
### Installing Sail Into Existing Applications

<!-- If you are interested in using Sail with an existing Laravel application, you may simply install Sail using the Composer package manager. Of course, these steps assume that your existing local development environment allows you to install Composer dependencies: -->
기존 Laravel 애플리케이션에 Sail을 추가해 사용하고 싶다면, Composer 패키지 관리자를 이용해 Sail을 설치할 수 있습니다. 이 단계는 로컬 개발 환경에 Composer 의존성 패키지 설치가 가능한 경우를 전제로 합니다.

```shell
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `docker-compose.yml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services: -->
Sail 설치가 완료되면, `sail:install` Artisan 명령어를 실행하세요. 이 명령어는 Sail의 `docker-compose.yml` 파일을 애플리케이션 루트에 복사해주고, Docker 서비스에 연결에 필요한 환경 변수를 `.env` 파일에 추가/수정합니다.

```shell
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
이제 Sail을 시작할 수 있습니다. Sail 사용법에 대해 더 알고 싶으시면, 아래 문서를 계속 읽어주세요.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> 만약 Docker Desktop for Linux를 사용 중이라면, 아래 명령어로 반드시 `default` Docker 컨텍스트를 활성화해야 합니다: `docker context use default`.

<a name="adding-additional-services"></a>
<!-- #### Adding Additional Services -->
#### Adding Additional Services

<!-- If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command: -->
기존 Sail 설치 환경에 새로운 서비스를 추가하고 싶은 경우엔 `sail:add` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 환경에서 개발하고 싶을 때는, `sail:install` 명령어에 `--devcontainer` 옵션을 추가하면 됩니다. `--devcontainer` 옵션을 사용하면 `sail:install` 명령어가 애플리케이션 루트에 기본 `.devcontainer/devcontainer.json ` 파일을 생성합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
<!-- ### Rebuilding Sail Images -->
### Rebuilding Sail Images

<!-- Sometimes you may want to completely rebuild your Sail images to ensure all of the image's packages and software are up to date. You may accomplish this using the `build` command: -->
가끔 모든 패키지와 소프트웨어를 최신 상태로 맞추기 위해 Sail 이미지를 완전히 다시 빌드해야 할 수 있습니다. `build` 명령어를 사용해서 이미지 재빌드를 할 수 있습니다.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
<!-- ### Configuring A Shell Alias -->
### Configuring A Shell Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
기본적으로 Sail 명령어는 신규 Laravel 프로젝트에 포함된 `vendor/bin/sail` 스크립트를 사용해서 실행합니다.

```shell
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily: -->
하지만 매번 `vendor/bin/sail`을 입력하는 대신, 셸 별칭(alias)을 설정해 더 쉽게 Sail 명령어를 실행할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

<!-- To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell. -->
이 별칭이 항상 적용되도록, 홈 디렉터리의 셸 설정 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 위 내용을 추가한 뒤 셸을 재시작하세요.

<!-- Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
별칭 설정 이후에는 단순히 `sail` 만 입력하면 Sail 명령어가 실행됩니다. 이 문서의 이후 예시들도 별칭이 설정된 것을 전제로 작성됩니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting and Stopping Sail -->
## Starting and Stopping Sail

<!-- Laravel Sail's `docker-compose.yml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `docker-compose.yml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail의 `docker-compose.yml` 파일에는 Laravel 애플리케이션 개발을 돕기 위한 다양한 Docker 컨테이너들이 정의되어 있습니다. 각각의 컨테이너는 `docker-compose.yml`의 `services` 설정에 하나씩 등록되어 있으며, 그중 `laravel.test` 컨테이너가 실제 애플리케이션을 제공하는 주요 컨테이너입니다.

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `docker-compose.yml` file, you should execute the `up` command: -->
Sail을 시작하기 전에, 로컬 컴퓨터에 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인하세요. 애플리케이션의 `docker-compose.yml` 파일에 정의된 모든 컨테이너를 시작하려면 아래와 같이 `up` 명령어를 실행합니다.

```shell
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
모든 컨테이너를 백그라운드에서 실행하고자 한다면 "detached" 모드로 실행할 수 있습니다.

```shell
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
컨테이너가 모두 실행되면 웹 브라우저에서 http://localhost 에 접속해 프로젝트를 확인할 수 있습니다.

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
모든 컨테이너를 종료하려면 Control + C 를 눌러 종료할 수 있습니다. 백그라운드 실행 시에는 `stop` 명령어로 중지할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 내에서 실행되며, 로컬 컴퓨터와 격리되어 있습니다. 하지만 Sail이 제공하는 인터페이스를 통해 다양한 명령어(PHP 실행, Artisan 명령, Composer 명령, Node/NPM 명령 등)를 쉽게 실행할 수 있습니다.

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel 공식 문서에서 Sail이 언급되지 않은 Composer, Artisan, Node/NPM 명령어 예시가 자주 등장합니다.** 그런 예제는 해당 도구들이 로컬 환경에 직접 설치되었다고 가정합니다. Sail을 사용하는 경우, 다음처럼 Sail을 통해 명령어를 실행해야 합니다.

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
PHP 명령어는 `php` 커맨드를 이용해 실행할 수 있습니다. 이때 사용되는 PHP 버전은 애플리케이션에 설정된 버전을 따릅니다. Sail에서 지원하는 PHP 버전은 [PHP version documentation](#sail-php-versions)를 참고하세요.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer installation: -->
Composer 관련 명령은 `composer` 커맨드로 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 이미 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="installing-composer-dependencies-for-existing-projects"></a>
<!-- #### Installing Composer Dependencies for Existing Applications -->
#### Installing Composer Dependencies for Existing Applications

<!-- If you are developing an application with a team, you may not be the one that initially creates the Laravel application. Therefore, none of the application's Composer dependencies, including Sail, will be installed after you clone the application's repository to your local computer. -->
팀 프로젝트에서 개발을 시작할 때는, Laravel 애플리케이션 자체를 직접 생성하지 않고 리포지터리를 클론만 하는 경우가 많습니다. 이런 경우에는 Composer 의존성, 포함하여 Sail도 아직 설치 전일 수 있습니다.

<!-- You may install the application's dependencies by navigating to the application's directory and executing the following command. This command uses a small Docker container containing PHP and Composer to install the application's dependencies: -->
애플리케이션 폴더로 이동한 뒤, 아래와 같이 Docker 컨테이너(PHP와 Composer 포함)를 임시로 띄워서 의존성을 설치할 수 있습니다.

```shell
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php84-composer:latest \
    composer install --ignore-platform-reqs
```

<!-- When using the `laravelsail/phpXX-composer` image, you should use the same version of PHP that you plan to use for your application (`80`, `81`, `82`, `83`, or `84`). -->
`laravelsail/phpXX-composer` 이미지를 사용할 때는, 애플리케이션에서 사용할 PHP 버전(`80`, `81`, `82`, `83`, `84` 중 하나)과 일치하는 이미지를 사용해야 합니다.

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel의 Artisan 명령어들은 `artisan` 커맨드를 통해 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
Node 관련 명령은 `node`로, NPM 관련 명령은 `npm`으로 실행할 수 있습니다.

```shell
sail node --version

sail npm run dev
```

<!-- If you wish, you may use Yarn instead of NPM: -->
원하면 NPM 대신 Yarn을 사용할 수도 있습니다.

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
`docker-compose.yml` 파일에는 MySQL 컨테이너 항목이 기본적으로 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용해 데이터베이스 데이터를 보존하므로, 컨테이너를 중지하거나 재시작해도 데이터가 유지됩니다.

<!-- In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data. -->
MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 자동으로 만들어집니다. 하나는 `DB_DATABASE` 환경변수의 값을 사용하여 생성된 로컬 개발용 데이터베이스이고, 다른 하나는 `testing`이라는 별도의 테스트 전용 데이터베이스입니다. 이렇게 분리하면 테스트가 개발 데이터에 영향을 주지 않습니다.

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
컨테이너 실행 이후에는 `.env` 파일의 `DB_HOST` 값을 `mysql`로 설정해서 애플리케이션 내에서 MySQL에 접속할 수 있습니다.

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password. -->
로컬 머신에서 MySQL 데이터베이스에 접속하려면 [TablePlus](https://tableplus.com) 같은 GUI 데이터베이스 도구를 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접속할 수 있고, 로그인 정보는 .env의 `DB_USERNAME`, `DB_PASSWORD` 값을 따릅니다. 또는, `root` 사용자로도 접속할 수 있으며 이때 패스워드는 동일하게 `DB_PASSWORD` 값이 사용됩니다.

<a name="mongodb"></a>
<!-- ### MongoDB -->
### MongoDB

<!-- If you chose to install the [MongoDB](https://www.mongodb.com/) service when installing Sail, your application's `docker-compose.yml` file contains an entry for a [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) container which provides the MongoDB document database with Atlas features like [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면, 애플리케이션의 `docker-compose.yml` 파일에 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 추가되어, [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/)와 같은 Atlas 기능을 갖춘 MongoDB 도큐먼트 데이터베이스를 제공합니다. 이 컨테이너 역시 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로, 컨테이너를 중지하거나 재시작해도 데이터가 유지됩니다.

<!-- Once you have started your containers, you may connect to the MongoDB instance within your application by setting your `MONGODB_URI` environment variable within your application's `.env` file to `mongodb://mongodb:27017`. Authentication is disabled by default, but you can set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables to enable authentication before starting the `mongodb` container. Then, add the credentials to the connection string: -->
컨테이너를 시작한 후에는, 애플리케이션의 `.env` 파일에서 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하면 애플리케이션 내에서 MongoDB 인스턴스에 연결할 수 있습니다. 기본적으로 인증은 비활성화되어 있지만, `mongodb` 컨테이너를 시작하기 전에 `MONGODB_USERNAME`과 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 그런 다음, 연결 문자열에 인증 정보를 추가합니다.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

<!-- For seamless integration of MongoDB with your application, you can install the [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/). -->
애플리케이션에 MongoDB를 원활히 통합하려면 [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

<!-- To connect to your application's MongoDB database from your local machine, you may use a graphical interface such as [Compass](https://www.mongodb.com/products/tools/compass). By default, the MongoDB database is accessible at `localhost` port `27017`. -->
로컬 머신에서 MongoDB 데이터를 직접 확인하려면 [Compass](https://www.mongodb.com/products/tools/compass)와 같은 GUI를 사용할 수 있습니다. 기본적으로 MongoDB는 `localhost`의 `27017` 포트에 열려 있습니다.

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `docker-compose.yml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis instance is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
`docker-compose.yml` 파일에는 [Redis](https://redis.io) 컨테이너도 포함되어 있습니다. 이 컨테이너 역시 [Docker volume](https://docs.docker.com/storage/volumes/)을 통해 데이터가 유지됩니다. 컨테이너 실행 후, `.env`의 `REDIS_HOST` 값을 `redis`로 설정하면 애플리케이션에서 Redis에 연결할 수 있습니다.

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
로컬 머신에서는 [TablePlus](https://tableplus.com) 같은 GUI를 쓰거나, `localhost`의 6379 포트로 직접 접근할 수 있습니다.

<a name="valkey"></a>
<!-- ### Valkey -->
### Valkey

<!-- If you choose to install Valkey service when installing Sail, your application's `docker-compose.yml` file will contain an entry for [Valkey](https://valkey.io/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Valkey instance is persisted even when stopping and restarting your containers. You can connect to this container in you application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `valkey`. -->
Sail 설치 시 Valkey 서비스를 선택하면, 애플리케이션의 `docker-compose.yml` 파일에 [Valkey](https://valkey.io/) 컨테이너가 추가됩니다. 이 컨테이너 역시 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용해 데이터가 보존되며, 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 값을 `valkey`로 설정해 연결할 수 있습니다.

<!-- To connect to your application's Valkey database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Valkey database is accessible at `localhost` port 6379. -->
로컬 머신에서는 [TablePlus](https://tableplus.com)와 같은 데이터베이스 관리 도구로 `localhost` 6379 포트에 접속할 수 있습니다.

<a name="meilisearch"></a>
<!-- ### Meilisearch -->
### Meilisearch

<!-- If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this powerful search engine that is integrated with [Laravel Scout](/docs/11.x/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택하면, `docker-compose.yml`에 이 강력한 검색 엔진 컨테이너가 추가됩니다. [Laravel Scout](/docs/11.x/scout)와 함께 통합해 사용할 수 있습니다. 컨테이너 실행 후 .env의 `MEILISEARCH_HOST` 변수를 `http://meilisearch:7700`으로 설정해 연결할 수 있습니다.

<!-- From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
로컬 머신에서는 웹 브라우저로 `http://localhost:7700`에 접속해 Meilisearch 관리 패널을 사용할 수 있습니다.

<a name="typesense"></a>
<!-- ### Typesense -->
### Typesense

<!-- If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `docker-compose.yml` file will contain an entry for this lightning fast, open-source search engine that is natively integrated with [Laravel Scout](/docs/11.x/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables: -->
Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면, `docker-compose.yml`에 초고속의 오픈소스 검색 엔진 컨테이너가 추가됩니다. 이 엔진 역시 [Laravel Scout](/docs/11.x/scout#typesense)와 통합 지원됩니다. 컨테이너 실행 후, 아래 환경변수를 설정하여 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

<!-- From your local machine, you may access Typesense's API via `http://localhost:8108`. -->
로컬 머신에서는 `http://localhost:8108`을 통해 Typesense API에 접근할 수 있습니다.

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [MinIO](https://min.io) service when installing Sail. MinIO provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install MinIO while installing Sail, a MinIO configuration section will be added to your application's `docker-compose.yml` file. -->
프로덕션 환경에서 Amazon S3를 파일 스토리지로 사용할 예정이라면, Sail 설치 시 [MinIO](https://min.io) 서비스를 함께 설치할 수 있습니다. MinIO는 S3 호환 API를 제공하기 때문에, 실제 S3 환경에서 "테스트"용 버킷을 만들 필요 없이 로컬 개발 환경에서 `s3` 드라이버 테스트가 가능합니다. MinIO 설치 시, 관련 설정이 `docker-compose.yml`에 자동으로 추가됩니다.

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as MinIO by simply modifying the associated environment variables that control its configuration. For example, when using MinIO, your filesystem environment variable configuration should be defined as follows: -->
기본적으로 Laravel의 `filesystems` 설정 파일에는 이미 `s3` 디스크 구성이 포함되어 있습니다. Amazon S3 뿐만 아니라 MinIO 등 S3 호환 스토리지를 사용하고 싶다면 관련 환경변수만 적절히 변경하면 됩니다. 예를 들어, MinIO를 쓸 경우 아래와 같이 설정할 수 있습니다.

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
Flysystem 통합을 통해 URL이 올바르게 생성되도록 하려면, `AWS_URL` 환경변수도 아래처럼 정의해야 합니다(로컬 URL 및 버킷명을 포함).

```ini
AWS_URL=http://localhost:9000/local
```

<!-- You may create buckets via the MinIO console, which is available at `http://localhost:8900`. The default username for the MinIO console is `sail` while the default password is `password`. -->
MinIO 콘솔에서 버킷 생성을 할 수 있습니다. 콘솔은 `http://localhost:8900` 에서 사용할 수 있고, 기본 아이디는 `sail`, 비밀번호는 `password`입니다.

> [!WARNING]
> MinIO를 사용할 경우 `temporaryUrl` 메서드를 통한 임시 스토리지 URL 생성은 지원되지 않습니다.

<a name="running-tests"></a>
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/11.x/testing). Any CLI options that are accepted by Pest / PHPUnit may also be passed to the `test` command: -->
Laravel은 기본적으로 강력한 테스트 지원을 제공합니다. Sail의 `test` 명령어를 사용해 [feature and unit tests](/docs/11.x/testing)를 바로 실행할 수 있습니다. Pest / PHPUnit에서 사용 가능한 모든 CLI 옵션 역시 `test` 명령어에 전달할 수 있습니다.

```shell
sail test

sail test --group orders
```

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail의 `test` 명령은 `test` Artisan 명령어와 동일합니다.

```shell
sail artisan test
```

<!-- By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests: -->
기본적으로 Sail에서는 별도의 `testing` 데이터베이스를 만들어 테스트 중 실제 데이터베이스에 영향을 주지 않도록 구성되어 있습니다. 기본 Laravel 프로젝트에서는 Sail이 `phpunit.xml` 파일 또한 테스트용 데이터베이스를 사용하도록 자동 설정합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/11.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `docker-compose.yml` file: -->
[Laravel Dusk](/docs/11.x/dusk)는 쉽고 표현력 있는 브라우저 자동화 및 테스트를 위한 API를 제공합니다. Sail 덕분에 Selenium이나 별도의 도구를 로컬에 설치하지 않아도 Dusk 테스트를 실행할 수 있습니다. 우선, 애플리케이션의 `docker-compose.yml` 파일에서 Selenium 서비스를 주석 해제하세요.

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
그리고 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스가 `selenium`에 대해 `depends_on` 항목을 갖도록 추가해야 합니다.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
이제 Sail을 시작하고 `dusk` 명령어로 Dusk 테스트 스위트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium on Apple Silicon -->
#### Selenium on Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `selenium/standalone-chromium` image: -->
로컬 머신이 Apple Silicon 칩(M1, M2 등)인 경우, `selenium` 서비스는 `selenium/standalone-chromium` 이미지를 사용해야 합니다.

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
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `docker-compose.yml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025: -->
Laravel Sail 기본 `docker-compose.yml` 파일에는 [Mailpit](https://github.com/axllent/mailpit) 서비스가 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션에서 발송되는 이메일들을 가로채서, 브라우저에서 바로 이메일 내용을 미리볼 수 있도록 해줍니다. Sail을 사용할 때 Mailpit의 기본 호스트는 `mailpit`이고, 포트는 1025번입니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the Mailpit web interface at: http://localhost:8025 -->
Sail이 실행 중이라면, 브라우저에서 http://localhost:8025 을 열어서 Mailpit 인터페이스를 사용할 수 있습니다.

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well as execute arbitrary shell commands within the container: -->
가끔 애플리케이션 컨테이너 내부에서 Bash 세션을 직접 실행하고 싶을 때가 있습니다. `shell` 명령어를 쓰면 컨테이너에 접속해 파일이나 서비스 확인, 임의의 쉘 명령 실행이 가능합니다.

```shell
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
[Laravel Tinker](https://github.com/laravel/tinker) 세션도 `tinker` 명령어로 바로 실행할 수 있습니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.4, 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.4. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `docker-compose.yml` file: -->
Sail은 현재 PHP 8.4, 8.3, 8.2, 8.1, 8.0을 지원합니다. 기본값은 PHP 8.4입니다. 사용하려는 PHP 버전을 변경하려면, `docker-compose.yml` 파일에서 `laravel.test` 컨테이너의 `build` 섹션을 아래와 같이 수정하세요.

```yaml
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

<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `docker-compose.yml` file: -->
또한, 애플리케이션에 사용 중인 PHP 버전에 맞춰 `image` 값도 업데이트할 수 있습니다. 이 설정 역시 `docker-compose.yml`에 있습니다.

```yaml
image: sail-8.2/app
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일 설정 변경 후에는 반드시 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 20 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `docker-compose.yml` file: -->
Sail은 기본적으로 Node 20을 설치합니다. 이미지 빌드시 설치할 Node 버전을 변경하고 싶다면 `docker-compose.yml` 내 `laravel.test` 서비스의 `build.args` 항목을 수정하세요.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

<!-- After updating your application's `docker-compose.yml` file, you should rebuild your container images: -->
애플리케이션의 `docker-compose.yml` 파일 설정 변경 후에는 컨테이너 이미지를 재빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
동료에게 웹사이트를 미리 보여주거나, 외부 서비스와 웹훅 연동 테스트를 하고 싶을 때가 있습니다. `share` 명령어를 사용하면 임시 `laravel-sail.site` URL을 발급받아 외부에서 애플리케이션에 접근할 수 있습니다.

```shell
sail share
```

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies using the `trustProxies` middleware method in your application's `bootstrap/app.php` file. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` 명령어로 사이트를 공유할 때는, 애플리케이션의 `bootstrap/app.php`에서 `trustProxies` 미들웨어 메서드를 통해 신뢰할 수 있는 프록시를 적절히 설정해야 합니다. 이 설정이 없으면 `url`이나 `route` 헬퍼에서 올바른 HTTP 호스트를 결정하지 못해 URL이 잘못 생성될 수 있습니다.

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->trustProxies(at: '*');
})
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
공유 사이트의 서브도메인을 직접 지정하고 싶을 땐, `share` 명령어를 실행할 때 `subdomain` 옵션을 사용하세요.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [Expose](https://beyondco.de)가 만든 오픈 소스 터널링 서비스 [BeyondCode](https://github.com/beyondcode/expose)를 기반으로 동작합니다.

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. To enable Xdebug, ensure you have [published your Sail configuration](#sail-customization). Then, add the following variables to your application's `.env` file to configure Xdebug: -->
Laravel Sail의 Docker 구성에는 [Xdebug](https://xdebug.org/) 지원이 내장되어 있어, PHP 환경에서 강력한 디버깅이 가능합니다. 먼저 [published your Sail configuration](#sail-customization)한 뒤, 아래와 같이 `.env` 파일에 관련 변수를 추가해 Xdebug를 활성화하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

<!-- Next, ensure that your published `php.ini` file includes the following configuration so that Xdebug is activated in the specified modes: -->
`php.ini` 파일에도 아래와 같이 Xdebug 모드가 명시되어 있어야 합니다.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

<!-- After modifying the `php.ini` file, remember to rebuild your Docker images so that your changes to the `php.ini` file take effect: -->
이후 `php.ini` 파일 변경 사항이 `php.ini`에 적용되도록 Docker 이미지를 반드시 다시 빌드해야 합니다.

```shell
sail build --no-cache
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux and you're using Docker 20.10+, `host.docker.internal` is available, and no manual configuration is required. -->
내부적으로 `XDEBUG_CONFIG` 환경변수는 `client_host=host.docker.internal`로 지정되어, Mac 및 Windows(WSL2)에서는 별도 설정 없이 제대로 동작합니다. 리눅스에서 Docker 20.10 이상을 쓰는 경우에도 `host.docker.internal` 지원으로 추가 설정이 필요 없습니다.

<!-- For Docker versions older than 20.10, `host.docker.internal` is not supported on Linux, and you will need to manually define the host IP. To do this, configure a static IP for your container by defining a custom network in your `docker-compose.yml` file: -->
만약 Docker 20.10 미만의 Linux 환경에서는 `host.docker.internal`이 지원되지 않으므로, 컨테이너에 고정 IP를 할당하고 별도로 설정해야 합니다. 이를 위해 `docker-compose.yml` 파일에 네트워크와 IP를 아래처럼 지정합니다.

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

<!-- Once you have set the static IP, define the SAIL_XDEBUG_CONFIG variable within your application's .env file: -->
이후, 애플리케이션의 .env 파일에 SAIL_XDEBUG_CONFIG 값을 추가로 작성합니다.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
`sail debug` 명령어로 Artisan 명령어를 실행할 때 디버깅 세션을 시작할 수 있습니다.

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
애플리케이션을 웹 브라우저를 통해 동작시켜 디버깅하려면, 브라우저에서 Xdebug 세션을 시작하는 방법은 [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application)를 참고하세요.

<!-- If you're using PhpStorm, please review JetBrains' documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm을 사용하는 경우에는 [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)를 살펴보시기 바랍니다.

> [!WARNING]
> Laravel Sail은 애플리케이션을 제공하기 위해 `artisan serve` 명령어를 사용합니다. `artisan serve`는 Laravel 8.53.0 이상에서만 `XDEBUG_CONFIG`, `XDEBUG_MODE` 환경 변수를 지원하며, 8.52.0 이하 버전에서는 해당 변수 지원이 없어 디버깅 연결이 정상적으로 동작하지 않습니다.

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail은 Docker 기반이므로 거의 모든 부분을 자유롭게 커스터마이즈할 수 있습니다. Sail 관련 Dockerfile을 직접 수정하고 싶다면 `sail:publish` Artisan 명령어를 실행하세요.

```shell
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `docker-compose.yml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
이렇게 하면 Laravel Sail이 사용하는 Dockerfile과 기타 설정 파일들이 애플리케이션 루트의 `docker` 디렉토리에 복사됩니다. Sail 환경을 수정한 후엔, 애플리케이션 컨테이너의 이미지 이름을 `docker-compose.yml`에서 별도로 지정할 수도 있습니다. 이렇게 이미지 이름을 분리하면 같은 컴퓨터에서 여러 Laravel 프로젝트를 개발할 때 이미지 충돌을 막을 수 있습니다. 변경 후에는 컨테이너 이미지를 반드시 `build` 명령어로 다시 빌드해야 하며, 다음 명령어로 빌드를 수행합니다.

```shell
sail build --no-cache
```
