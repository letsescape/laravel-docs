<!-- # Laravel Sail -->
# Laravel Sail

- [Introduction](#introduction)
- [Installation and Setup](#installation)
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
    - [Additional PHP Extensions](#sail-php-extensions)
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
[Laravel Sail](https://github.com/laravel/sail)은 Laravel의 기본 Docker 개발 환경과 상호작용하기 위한 가벼운 명령줄 인터페이스입니다. Sail은 Docker 경험이 없어도 PHP, MySQL, Redis를 사용하여 Laravel 애플리케이션을 구축할 수 있는 좋은 출발점을 제공합니다.

<!-- At its heart, Sail is the `compose.yaml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `compose.yaml` file. -->
핵심적으로 Sail은 프로젝트 루트에 저장되는 `compose.yaml` 파일과 `sail` 스크립트로 이루어져 있습니다. `sail` 스크립트는 `compose.yaml` 파일에 정의된 Docker 컨테이너와 상호작용할 수 있는 편리한 메서드를 갖춘 CLI를 제공합니다.

<!-- Laravel Sail is supported on macOS, Linux, and Windows (via [WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)). -->
Laravel Sail은 macOS, Linux, Windows([WSL2](https://docs.microsoft.com/en-us/windows/wsl/about)를 통해)를 지원합니다.

<a name="installation"></a>
<!-- ## Installation and Setup -->
## Installation and Setup

<!-- You may install Sail using the Composer package manager: -->
Composer 패키지 관리자를 사용하여 Sail을 설치할 수 있습니다.

```shell
composer require laravel/sail --dev
```

<!-- After Sail has been installed, you may run the `sail:install` Artisan command. This command will publish Sail's `compose.yaml` file to the root of your application and modify your `.env` file with the required environment variables in order to connect to the Docker services: -->
Sail을 설치한 후에는 `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션 루트에 게시하고, Docker 서비스에 연결하는 데 필요한 환경 변수로 `.env` 파일을 수정합니다.

```shell
php artisan sail:install
```

<!-- Finally, you may start Sail. To continue learning how to use Sail, please continue reading the remainder of this documentation: -->
마지막으로 Sail을 시작할 수 있습니다. Sail 사용법을 계속 배우려면 이 문서의 나머지 내용을 계속 읽어보십시오.

```shell
./vendor/bin/sail up
```

> [!WARNING]
> Linux용 Docker Desktop을 사용 중이라면 다음 명령어를 실행하여 `default` Docker 컨텍스트를 사용해야 합니다. `docker context use default`. 또한 컨테이너 안에서 파일 권한 오류가 발생하는 경우 `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 설정해야 할 수 있습니다.

<a name="adding-additional-services"></a>
<!-- #### Adding Additional Services -->
#### Adding Additional Services

<!-- If you would like to add an additional service to your existing Sail installation, you may run the `sail:add` Artisan command: -->
기존 Sail 설치에 추가 서비스를 더하고 싶다면 `sail:add` Artisan 명령어를 실행할 수 있습니다.

```shell
php artisan sail:add
```

<a name="using-devcontainers"></a>
<!-- #### Using Devcontainers -->
#### Using Devcontainers

<!-- If you would like to develop within a [Devcontainer](https://code.visualstudio.com/docs/remote/containers), you may provide the `--devcontainer` option to the `sail:install` command. The `--devcontainer` option will instruct the `sail:install` command to publish a default `.devcontainer/devcontainer.json ` file to the root of your application: -->
[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 안에서 개발하고 싶다면 `sail:install` 명령어에 `--devcontainer` 옵션을 제공할 수 있습니다. `--devcontainer` 옵션은 `sail:install` 명령어가 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 루트에 게시하도록 지시합니다.

```shell
php artisan sail:install --devcontainer
```

<a name="rebuilding-sail-images"></a>
<!-- ### Rebuilding Sail Images -->
### Rebuilding Sail Images

<!-- Sometimes you may want to completely rebuild your Sail images to ensure all of the image's packages and software are up to date. You may accomplish this using the `build` command: -->
때로는 이미지의 모든 패키지와 소프트웨어가 최신 상태인지 확인하기 위해 Sail 이미지를 완전히 다시 빌드하고 싶을 수 있습니다. `build` 명령어를 사용하여 이를 수행할 수 있습니다.

```shell
docker compose down -v

sail build --no-cache

sail up
```

<a name="configuring-a-shell-alias"></a>
<!-- ### Configuring A Shell Alias -->
### Configuring A Shell Alias

<!-- By default, Sail commands are invoked using the `vendor/bin/sail` script that is included with all new Laravel applications: -->
기본적으로 Sail 명령어는 모든 새 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용하여 호출합니다.

```shell
./vendor/bin/sail up
```

<!-- However, instead of repeatedly typing `vendor/bin/sail` to execute Sail commands, you may wish to configure a shell alias that allows you to execute Sail's commands more easily: -->
하지만 Sail 명령어를 실행할 때마다 `vendor/bin/sail`을 반복해서 입력하는 대신, Sail 명령어를 더 쉽게 실행할 수 있도록 셸 별칭을 설정할 수 있습니다.

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```

<!-- To make sure this is always available, you may add this to your shell configuration file in your home directory, such as `~/.zshrc` or `~/.bashrc`, and then restart your shell. -->
이 별칭을 항상 사용할 수 있게 하려면 홈 디렉터리에 있는 `~/.zshrc` 또는 `~/.bashrc` 같은 셸 설정 파일에 추가한 뒤 셸을 다시 시작하면 됩니다.

<!-- Once the shell alias has been configured, you may execute Sail commands by simply typing `sail`. The remainder of this documentation's examples will assume that you have configured this alias: -->
셸 별칭을 설정한 후에는 단순히 `sail`을 입력하여 Sail 명령어를 실행할 수 있습니다. 이 문서의 나머지 예제는 이 별칭을 설정했다고 가정합니다.

```shell
sail up
```

<a name="starting-and-stopping-sail"></a>
<!-- ## Starting and Stopping Sail -->
## Starting and Stopping Sail

<!-- Laravel Sail's `compose.yaml` file defines a variety of Docker containers that work together to help you build Laravel applications. Each of these containers is an entry within the `services` configuration of your `compose.yaml` file. The `laravel.test` container is the primary application container that will be serving your application. -->
Laravel Sail의 `compose.yaml` 파일은 Laravel 애플리케이션 구축을 돕기 위해 함께 동작하는 다양한 Docker 컨테이너를 정의합니다. 이러한 각 컨테이너는 `compose.yaml` 파일의 `services` 설정 안에 있는 항목입니다. `laravel.test` 컨테이너는 애플리케이션을 제공하는 기본 애플리케이션 컨테이너입니다.

<!-- Before starting Sail, you should ensure that no other web servers or databases are running on your local computer. To start all of the Docker containers defined in your application's `compose.yaml` file, you should execute the `up` command: -->
Sail을 시작하기 전에 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행 중이지 않은지 확인해야 합니다. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면 `up` 명령어를 실행해야 합니다.

```shell
sail up
```

<!-- To start all of the Docker containers in the background, you may start Sail in "detached" mode: -->
모든 Docker 컨테이너를 백그라운드에서 시작하려면 Sail을 "detached" 모드로 시작할 수 있습니다.

```shell
sail up -d
```

<!-- Once the application's containers have been started, you may access the project in your web browser at: http://localhost. -->
애플리케이션 컨테이너가 시작되면 웹 브라우저에서 다음 주소로 프로젝트에 접근할 수 있습니다. http://localhost.

<!-- To stop all of the containers, you may simply press Control + C to stop the container's execution. Or, if the containers are running in the background, you may use the `stop` command: -->
모든 컨테이너를 중지하려면 Control + C를 눌러 컨테이너 실행을 중지하면 됩니다. 또는 컨테이너가 백그라운드에서 실행 중이라면 `stop` 명령어를 사용할 수 있습니다.

```shell
sail stop
```

<a name="executing-sail-commands"></a>
<!-- ## Executing Commands -->
## Executing Commands

<!-- When using Laravel Sail, your application is executing within a Docker container and is isolated from your local computer. However, Sail provides a convenient way to run various commands against your application such as arbitrary PHP commands, Artisan commands, Composer commands, and Node / NPM commands. -->
Laravel Sail을 사용할 때 애플리케이션은 Docker 컨테이너 안에서 실행되며 로컬 컴퓨터와 격리됩니다. 하지만 Sail은 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어 등 애플리케이션을 대상으로 다양한 명령어를 실행할 수 있는 편리한 방법을 제공합니다.

<!-- **When reading the Laravel documentation, you will often see references to Composer, Artisan, and Node / NPM commands that do not reference Sail.** Those examples assume that these tools are installed on your local computer. If you are using Sail for your local Laravel development environment, you should execute those commands using Sail: -->
**Laravel 문서를 읽다 보면 Sail을 언급하지 않는 Composer, Artisan, Node / NPM 명령어 예제를 자주 보게 됩니다.** 해당 예제들은 이러한 도구가 로컬 컴퓨터에 설치되어 있다고 가정합니다. 로컬 Laravel 개발 환경으로 Sail을 사용하고 있다면 해당 명령어를 Sail을 통해 실행해야 합니다.

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
PHP 명령어는 `php` 명령어를 사용하여 실행할 수 있습니다. 물론 이 명령어들은 애플리케이션에 설정된 PHP 버전을 사용하여 실행됩니다. Laravel Sail에서 사용할 수 있는 PHP 버전에 대해 더 알아보려면 [PHP version documentation](#sail-php-versions)를 참고하십시오.

```shell
sail php --version

sail php script.php
```

<a name="executing-composer-commands"></a>
<!-- ### Executing Composer Commands -->
### Executing Composer Commands

<!-- Composer commands may be executed using the `composer` command. Laravel Sail's application container includes a Composer installation: -->
Composer 명령어는 `composer` 명령어를 사용하여 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다.

```shell
sail composer require laravel/sanctum
```

<a name="executing-artisan-commands"></a>
<!-- ### Executing Artisan Commands -->
### Executing Artisan Commands

<!-- Laravel Artisan commands may be executed using the `artisan` command: -->
Laravel Artisan 명령어는 `artisan` 명령어를 사용하여 실행할 수 있습니다.

```shell
sail artisan queue:work
```

<a name="executing-node-npm-commands"></a>
<!-- ### Executing Node / NPM Commands -->
### Executing Node / NPM Commands

<!-- Node commands may be executed using the `node` command while NPM commands may be executed using the `npm` command: -->
Node 명령어는 `node` 명령어를 사용하여 실행할 수 있으며, NPM 명령어는 `npm` 명령어를 사용하여 실행할 수 있습니다.

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

<!-- As you may have noticed, your application's `compose.yaml` file contains an entry for a MySQL container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
이미 알아차렸을 수 있듯이, 애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너 항목이 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다.

<!-- In addition, the first time the MySQL container starts, it will create two databases for you. The first database is named using the value of your `DB_DATABASE` environment variable and is for your local development. The second is a dedicated testing database named `testing` and will ensure that your tests do not interfere with your development data. -->
또한 MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스를 생성합니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수 값을 사용해 이름이 정해지며 로컬 개발용입니다. 두 번째 데이터베이스는 `testing`이라는 전용 테스트 데이터베이스로, 테스트가 개발 데이터에 영향을 주지 않도록 보장합니다.

<!-- Once you have started your containers, you may connect to the MySQL instance within your application by setting your `DB_HOST` environment variable within your application's `.env` file to `mysql`. -->
컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `DB_HOST` 환경 변수를 `mysql`로 설정하여 애플리케이션 안에서 MySQL 인스턴스에 연결할 수 있습니다.

<!-- To connect to your application's MySQL database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the MySQL database is accessible at `localhost` port 3306 and the access credentials correspond to the values of your `DB_USERNAME` and `DB_PASSWORD` environment variables. Or, you may connect as the `root` user, which also utilizes the value of your `DB_PASSWORD` environment variable as its password. -->
로컬 머신에서 애플리케이션의 MySQL 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost`의 3306 포트에서 접근할 수 있으며, 접근 자격 증명은 `DB_USERNAME` 및 `DB_PASSWORD` 환경 변수 값과 일치합니다. 또는 `root` 사용자로 연결할 수도 있으며, 이 경우에도 `DB_PASSWORD` 환경 변수 값을 비밀번호로 사용합니다.

<a name="mongodb"></a>
<!-- ### MongoDB -->
### MongoDB

<!-- If you chose to install the [MongoDB](https://www.mongodb.com/) service when installing Sail, your application's `compose.yaml` file contains an entry for a [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) container which provides the MongoDB document database with Atlas features like [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your database is persisted even when stopping and restarting your containers. -->
Sail 설치 시 [MongoDB](https://www.mongodb.com/) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너 항목이 포함되며, 이 컨테이너는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) 같은 Atlas 기능과 함께 MongoDB 문서 데이터베이스를 제공합니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다.

<!-- Once you have started your containers, you may connect to the MongoDB instance within your application by setting your `MONGODB_URI` environment variable within your application's `.env` file to `mongodb://mongodb:27017`. Authentication is disabled by default, but you can set the `MONGODB_USERNAME` and `MONGODB_PASSWORD` environment variables to enable authentication before starting the `mongodb` container. Then, add the credentials to the connection string: -->
컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하여 애플리케이션 안에서 MongoDB 인스턴스에 연결할 수 있습니다. 인증은 기본적으로 비활성화되어 있지만, `mongodb` 컨테이너를 시작하기 전에 `MONGODB_USERNAME` 및 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 그런 다음 연결 문자열에 자격 증명을 추가하십시오.

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

<!-- For seamless integration of MongoDB with your application, you can install the [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/). -->
MongoDB를 애플리케이션과 매끄럽게 통합하려면 [official package maintained by MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/)를 설치할 수 있습니다.

<!-- To connect to your application's MongoDB database from your local machine, you may use a graphical interface such as [Compass](https://www.mongodb.com/products/tools/compass). By default, the MongoDB database is accessible at `localhost` port `27017`. -->
로컬 머신에서 애플리케이션의 MongoDB 데이터베이스에 연결하려면 [Compass](https://www.mongodb.com/products/tools/compass) 같은 그래픽 인터페이스를 사용할 수 있습니다. 기본적으로 MongoDB 데이터베이스는 `localhost`의 `27017` 포트에서 접근할 수 있습니다.

<a name="redis"></a>
<!-- ### Redis -->
### Redis

<!-- Your application's `compose.yaml` file also contains an entry for a [Redis](https://redis.io) container. This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Redis instance is persisted even when stopping and restarting your containers. Once you have started your containers, you may connect to the Redis instance within your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `redis`. -->
애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너 항목도 포함되어 있습니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 Redis 인스턴스에 저장된 데이터가 유지됩니다. 컨테이너를 시작한 후에는 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `redis`로 설정하여 애플리케이션 안에서 Redis 인스턴스에 연결할 수 있습니다.

<!-- To connect to your application's Redis database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Redis database is accessible at `localhost` port 6379. -->
로컬 머신에서 애플리케이션의 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="valkey"></a>
<!-- ### Valkey -->
### Valkey

<!-- If you choose to install Valkey service when installing Sail, your application's `compose.yaml` file will contain an entry for [Valkey](https://valkey.io/). This container uses a [Docker volume](https://docs.docker.com/storage/volumes/) so that the data stored in your Valkey instance is persisted even when stopping and restarting your containers. You can connect to this container in your application by setting your `REDIS_HOST` environment variable within your application's `.env` file to `valkey`. -->
Sail 설치 시 Valkey 서비스를 선택하면 애플리케이션의 `compose.yaml` 파일에 [Valkey](https://valkey.io/) 항목이 포함됩니다. 이 컨테이너는 [Docker volume](https://docs.docker.com/storage/volumes/)을 사용하므로 컨테이너를 중지하고 다시 시작해도 Valkey 인스턴스에 저장된 데이터가 유지됩니다. 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `valkey`로 설정하여 애플리케이션에서 이 컨테이너에 연결할 수 있습니다.

<!-- To connect to your application's Valkey database from your local machine, you may use a graphical database management application such as [TablePlus](https://tableplus.com). By default, the Valkey database is accessible at `localhost` port 6379. -->
로컬 머신에서 애플리케이션의 Valkey 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Valkey 데이터베이스는 `localhost`의 6379 포트에서 접근할 수 있습니다.

<a name="meilisearch"></a>
<!-- ### Meilisearch -->
### Meilisearch

<!-- If you chose to install the [Meilisearch](https://www.meilisearch.com) service when installing Sail, your application's `compose.yaml` file will contain an entry for this powerful search engine that is integrated with [Laravel Scout](/docs/13.x/scout). Once you have started your containers, you may connect to the Meilisearch instance within your application by setting your `MEILISEARCH_HOST` environment variable to `http://meilisearch:7700`. -->
Sail 설치 시 [Meilisearch](https://www.meilisearch.com) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [Laravel Scout](/docs/13.x/scout)와 통합되는 강력한 검색 엔진 항목이 포함됩니다. 컨테이너를 시작한 후에는 `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700`으로 설정하여 애플리케이션 안에서 Meilisearch 인스턴스에 연결할 수 있습니다.

<!-- From your local machine, you may access Meilisearch's web based administration panel by navigating to `http://localhost:7700` in your web browser. -->
로컬 머신에서는 웹 브라우저에서 `http://localhost:7700`으로 이동하여 Meilisearch의 웹 기반 관리 패널에 접근할 수 있습니다.

<a name="typesense"></a>
<!-- ### Typesense -->
### Typesense

<!-- If you chose to install the [Typesense](https://typesense.org) service when installing Sail, your application's `compose.yaml` file will contain an entry for this lightning fast, open-source search engine that is natively integrated with [Laravel Scout](/docs/13.x/scout#typesense). Once you have started your containers, you may connect to the Typesense instance within your application by setting the following environment variables: -->
Sail 설치 시 [Typesense](https://typesense.org) 서비스를 선택했다면 애플리케이션의 `compose.yaml` 파일에는 [Laravel Scout](/docs/13.x/scout#typesense)와 기본적으로 통합되는 매우 빠른 오픈 소스 검색 엔진 항목이 포함됩니다. 컨테이너를 시작한 후에는 다음 환경 변수를 설정하여 애플리케이션 안에서 Typesense 인스턴스에 연결할 수 있습니다.

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```

<!-- From your local machine, you may access Typesense's API via `http://localhost:8108`. -->
로컬 머신에서는 `http://localhost:8108`을 통해 Typesense의 API에 접근할 수 있습니다.

<a name="file-storage"></a>
<!-- ## File Storage -->
## File Storage

<!-- If you plan to use Amazon S3 to store files while running your application in its production environment, you may wish to install the [RustFS](https://rustfs.com) service when installing Sail. RustFS provides an S3 compatible API that you may use to develop locally using Laravel's `s3` file storage driver without creating "test" storage buckets in your production S3 environment. If you choose to install RustFS while installing Sail, a RustFS configuration section will be added to your application's `compose.yaml` file. -->
프로덕션 환경에서 애플리케이션을 실행할 때 파일 저장소로 Amazon S3를 사용할 계획이라면 Sail 설치 시 [RustFS](https://rustfs.com) 서비스를 설치하는 것이 좋습니다. RustFS는 S3 호환 API를 제공하므로, 프로덕션 S3 환경에 "test" 스토리지 버킷을 만들지 않고도 Laravel의 `s3` 파일 스토리지 드라이버를 사용하여 로컬에서 개발할 수 있습니다. Sail 설치 시 RustFS를 설치하도록 선택하면 RustFS 설정 섹션이 애플리케이션의 `compose.yaml` 파일에 추가됩니다.

<!-- By default, your application's `filesystems` configuration file already contains a disk configuration for the `s3` disk. In addition to using this disk to interact with Amazon S3, you may use it to interact with any S3 compatible file storage service such as RustFS by simply modifying the associated environment variables that control its configuration. For example, when using RustFS, your filesystem environment variable configuration should be defined as follows: -->
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
<!-- ## Running Tests -->
## Running Tests

<!-- Laravel provides amazing testing support out of the box, and you may use Sail's `test` command to run your applications [feature and unit tests](/docs/13.x/testing). Any CLI options that are accepted by Pest / PHPUnit may also be passed to the `test` command: -->
Laravel은 기본적으로 훌륭한 테스트 지원을 제공하며, Sail의 `test` 명령어를 사용하여 애플리케이션의 [feature and unit tests](/docs/13.x/testing)를 실행할 수 있습니다. Pest / PHPUnit에서 허용하는 모든 CLI 옵션도 `test` 명령어에 전달할 수 있습니다.

```shell
sail test

sail test --group orders
```

<!-- The Sail `test` command is equivalent to running the `test` Artisan command: -->
Sail `test` 명령어는 `test` Artisan 명령어를 실행하는 것과 동일합니다.

```shell
sail artisan test
```

<!-- By default, Sail will create a dedicated `testing` database so that your tests do not interfere with the current state of your database. In a default Laravel installation, Sail will also configure your `phpunit.xml` file to use this database when executing your tests: -->
기본적으로 Sail은 전용 `testing` 데이터베이스를 생성하여 테스트가 데이터베이스의 현재 상태에 영향을 주지 않도록 합니다. 기본 Laravel 설치에서는 Sail이 테스트 실행 시 이 데이터베이스를 사용하도록 `phpunit.xml` 파일도 설정합니다.

```xml
<env name="DB_DATABASE" value="testing"/>
```

<a name="laravel-dusk"></a>
<!-- ### Laravel Dusk -->
### Laravel Dusk

<!-- [Laravel Dusk](/docs/13.x/dusk) provides an expressive, easy-to-use browser automation and testing API. Thanks to Sail, you may run these tests without ever installing Selenium or other tools on your local computer. To get started, uncomment the Selenium service in your application's `compose.yaml` file: -->
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

<!-- Next, ensure that the `laravel.test` service in your application's `compose.yaml` file has a `depends_on` entry for `selenium`: -->
다음으로 애플리케이션의 `compose.yaml` 파일에 있는 `laravel.test` 서비스에 `selenium`에 대한 `depends_on` 항목이 있는지 확인하십시오.

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```

<!-- Finally, you may run your Dusk test suite by starting Sail and running the `dusk` command: -->
마지막으로 Sail을 시작하고 `dusk` 명령어를 실행하여 Dusk 테스트 스위트를 실행할 수 있습니다.

```shell
sail dusk
```

<a name="selenium-on-apple-silicon"></a>
<!-- #### Selenium on Apple Silicon -->
#### Selenium on Apple Silicon

<!-- If your local machine contains an Apple Silicon chip, your `selenium` service must use the `selenium/standalone-chromium` image: -->
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
<!-- ## Previewing Emails -->
## Previewing Emails

<!-- Laravel Sail's default `compose.yaml` file contains a service entry for [Mailpit](https://github.com/axllent/mailpit). Mailpit intercepts emails sent by your application during local development and provides a convenient web interface so that you can preview your email messages in your browser. When using Sail, Mailpit's default host is `mailpit` and is available via port 1025: -->
Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit)에 대한 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중 애플리케이션이 보내는 이메일을 가로채고, 브라우저에서 이메일 메시지를 미리 볼 수 있는 편리한 웹 인터페이스를 제공합니다. Sail을 사용할 때 Mailpit의 기본 호스트는 `mailpit`이며 1025 포트를 통해 사용할 수 있습니다.

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```

<!-- When Sail is running, you may access the Mailpit web interface at: http://localhost:8025 -->
Sail이 실행 중이면 다음 주소에서 Mailpit 웹 인터페이스에 접근할 수 있습니다. http://localhost:8025

<a name="sail-container-cli"></a>
<!-- ## Container CLI -->
## Container CLI

<!-- Sometimes you may wish to start a Bash session within your application's container. You may use the `shell` command to connect to your application's container, allowing you to inspect its files and installed services as well as execute arbitrary shell commands within the container: -->
때로는 애플리케이션 컨테이너 안에서 Bash 세션을 시작하고 싶을 수 있습니다. `shell` 명령어를 사용하여 애플리케이션 컨테이너에 연결할 수 있으며, 이를 통해 컨테이너 안에서 파일과 설치된 서비스를 살펴보고 임의의 셸 명령어를 실행할 수 있습니다.

```shell
sail shell

sail root-shell
```

<!-- To start a new [Laravel Tinker](https://github.com/laravel/tinker) session, you may execute the `tinker` command: -->
새 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면 `tinker` 명령어를 실행할 수 있습니다.

```shell
sail tinker
```

<a name="sail-php-versions"></a>
<!-- ## PHP Versions -->
## PHP Versions

<!-- Sail currently supports serving your application via PHP 8.5, 8.4, 8.3, 8.2, 8.1, or PHP 8.0. The default PHP version used by Sail is currently PHP 8.5. To change the PHP version that is used to serve your application, you should update the `build` definition of the `laravel.test` container in your application's `compose.yaml` file: -->
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
<!-- In addition, you may wish to update your `image` name to reflect the version of PHP being used by your application. This option is also defined in your application's `compose.yaml` file: -->
또한 애플리케이션에서 사용하는 PHP 버전을 반영하도록 `image` 이름을 업데이트할 수도 있습니다. 이 옵션도 애플리케이션의 `compose.yaml` 파일에 정의되어 있습니다.

```yaml
image: sail-8.2/app
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images: -->
애플리케이션의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sail-php-extensions"></a>
<!-- ### Additional PHP Extensions -->
### Additional PHP Extensions

<!-- Sail's runtime images include a common set of PHP extensions. If your application requires additional extensions, you may install them when building the image by adding a space-separated `PHP_EXTENSIONS` build argument to the `laravel.test` service in your application's `compose.yaml` file: -->
Sail의 런타임 이미지는 일반적으로 사용되는 PHP 확장 집합을 포함합니다. 애플리케이션에 추가 확장이 필요하다면, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 서비스에 공백으로 구분된 `PHP_EXTENSIONS` 빌드 인수를 추가하여 이미지를 빌드할 때 설치할 수 있습니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        PHP_EXTENSIONS: 'gmp imagick'
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images. -->
애플리케이션의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

<a name="sail-node-versions"></a>
<!-- ## Node Versions -->
## Node Versions

<!-- Sail installs Node 24 by default. To change the Node version that is installed when building your images, you may update the `build.args` definition of the `laravel.test` service in your application's `compose.yaml` file: -->
Sail은 기본적으로 Node 24를 설치합니다. 이미지를 빌드할 때 설치되는 Node 버전을 변경하려면 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 정의를 업데이트하면 됩니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```

<!-- After updating your application's `compose.yaml` file, you should rebuild your container images: -->
애플리케이션의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache

sail up
```

<a name="sharing-your-site"></a>
<!-- ## Sharing Your Site -->
## Sharing Your Site

<!-- Sometimes you may need to share your site publicly in order to preview your site for a colleague or to test webhook integrations with your application. To share your site, you may use the `share` command. After executing this command, you will be issued a random `laravel-sail.site` URL that you may use to access your application: -->
때로는 동료에게 사이트를 미리 보여주거나 애플리케이션의 Webhook 연동을 테스트하기 위해 사이트를 공개적으로 공유해야 할 수 있습니다. 사이트를 공유하려면 `share` 명령어를 사용할 수 있습니다. 이 명령어를 실행하면 애플리케이션에 접근하는 데 사용할 수 있는 임의의 `laravel-sail.site` URL이 발급됩니다.

```shell
sail share
```

<!-- When sharing your site via the `share` command, you should configure your application's trusted proxies using the `trustProxies` middleware method in your application's `bootstrap/app.php` file. Otherwise, URL generation helpers such as `url` and `route` will be unable to determine the correct HTTP host that should be used during URL generation: -->
`share` 명령어로 사이트를 공유할 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 애플리케이션의 신뢰할 수 있는 프록시를 설정해야 합니다. 그렇지 않으면 `url`, `route` 같은 URL 생성 헬퍼가 URL 생성 시 사용할 올바른 HTTP 호스트를 판단할 수 없습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<!-- If you would like to choose the subdomain for your shared site, you may provide the `subdomain` option when executing the `share` command: -->
공유 사이트에 사용할 서브도메인을 직접 선택하고 싶다면 `share` 명령어를 실행할 때 `subdomain` 옵션을 제공할 수 있습니다.

```shell
sail share --subdomain=my-sail-site
```

> [!NOTE]
> `share` 명령어는 [Expose](https://github.com/beyondcode/expose)를 기반으로 동작하며, Expose는 [BeyondCode](https://beyondco.de)가 만든 오픈 소스 터널링 서비스입니다.

<a name="debugging-with-xdebug"></a>
<!-- ## Debugging With Xdebug -->
## Debugging With Xdebug

<!-- Laravel Sail's Docker configuration includes support for [Xdebug](https://xdebug.org/), a popular and powerful debugger for PHP. To enable Xdebug, ensure you have [published your Sail configuration](#sail-customization). Then, add the following variables to your application's `.env` file to configure Xdebug: -->
Laravel Sail의 Docker 설정에는 PHP에서 널리 사용되는 강력한 디버거인 [Xdebug](https://xdebug.org/) 지원이 포함되어 있습니다. Xdebug를 활성화하려면 먼저 [published your Sail configuration](#sail-customization)했는지 확인하세요. 그런 다음 Xdebug를 설정하기 위해 애플리케이션의 `.env` 파일에 다음 변수를 추가하세요.

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```

<!-- Next, ensure that your published `php.ini` file includes the following configuration so that Xdebug is activated in the specified modes: -->
다음으로, 지정한 모드에서 Xdebug가 활성화되도록 게시된 `php.ini` 파일에 다음 설정이 포함되어 있는지 확인하세요.

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```

<!-- After modifying the `php.ini` file, remember to rebuild your Docker images so that your changes to the `php.ini` file take effect: -->
`php.ini` 파일을 수정한 후에는 `php.ini` 파일 변경 사항이 적용되도록 Docker 이미지를 다시 빌드해야 합니다.

```shell
sail build --no-cache
```

<!-- #### Linux Host IP Configuration -->
#### Linux Host IP Configuration

<!-- Internally, the `XDEBUG_CONFIG` environment variable is defined as `client_host=host.docker.internal` so that Xdebug will be properly configured for Mac and Windows (WSL2). If your local machine is running Linux and you're using Docker 20.10+, `host.docker.internal` is available, and no manual configuration is required. -->
내부적으로 `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있으므로 Mac과 Windows(WSL2)에서 Xdebug가 올바르게 설정됩니다. 로컬 머신이 Linux를 실행 중이고 Docker 20.10 이상을 사용하고 있다면 `host.docker.internal`을 사용할 수 있으며, 수동 설정은 필요하지 않습니다.

<!-- For Docker versions older than 20.10, `host.docker.internal` is not supported on Linux, and you will need to manually define the host IP. To do this, configure a static IP for your container by defining a custom network in your `compose.yaml` file: -->
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

<!-- Once you have set the static IP, define the SAIL_XDEBUG_CONFIG variable within your application's .env file: -->
정적 IP를 설정한 후에는 애플리케이션의 .env 파일 내에 SAIL_XDEBUG_CONFIG 변수를 정의하세요.

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```

<a name="xdebug-cli-usage"></a>
<!-- ### Xdebug CLI Usage -->
### Xdebug CLI Usage

<!-- A `sail debug` command may be used to start a debugging session when running an Artisan command: -->
Artisan 명령어를 실행할 때 `sail debug` 명령어를 사용하여 디버깅 세션을 시작할 수 있습니다.

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
웹 브라우저를 통해 애플리케이션과 상호작용하면서 애플리케이션을 디버깅하려면 웹 브라우저에서 Xdebug 세션을 시작하는 방법에 대한 [instructions provided by Xdebug](https://xdebug.org/docs/step_debug#web-application)를 따르세요.

<!-- If you're using PhpStorm, please review JetBrains' documentation regarding [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html). -->
PhpStorm을 사용하고 있다면 [zero-configuration debugging](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrains 문서를 확인하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션을 제공하기 위해 `artisan serve`에 의존합니다. `artisan serve` 명령어는 Laravel 버전 8.53.0부터 `XDEBUG_CONFIG`와 `XDEBUG_MODE` 변수만 허용합니다. 이전 Laravel 버전(8.52.0 이하)은 이러한 변수를 지원하지 않으며 디버그 연결을 허용하지 않습니다.

<a name="sail-customization"></a>
<!-- ## Customization -->
## Customization

<!-- Since Sail is just Docker, you are free to customize nearly everything about it. To publish Sail's own Dockerfiles, you may execute the `sail:publish` command: -->
Sail은 결국 Docker이므로 거의 모든 것을 자유롭게 사용자 정의할 수 있습니다. Sail 자체 Dockerfile을 게시하려면 `sail:publish` 명령어를 실행하면 됩니다.

```shell
sail artisan sail:publish
```

<!-- After running this command, the Dockerfiles and other configuration files used by Laravel Sail will be placed within a `docker` directory in your application's root directory. After customizing your Sail installation, you may wish to change the image name for the application container in your application's `compose.yaml` file. After doing so, rebuild your application's containers using the `build` command. Assigning a unique name to the application image is particularly important if you are using Sail to develop multiple Laravel applications on a single machine: -->
이 명령어를 실행하면 Laravel Sail에서 사용하는 Dockerfile과 기타 설정 파일이 애플리케이션 루트 디렉터리의 `docker` 디렉터리에 배치됩니다. Sail 설치를 사용자 정의한 후에는 애플리케이션의 `compose.yaml` 파일에서 애플리케이션 컨테이너의 이미지 이름을 변경하고 싶을 수 있습니다. 변경한 뒤에는 `build` 명령어를 사용하여 애플리케이션 컨테이너를 다시 빌드하세요. 하나의 머신에서 Sail을 사용해 여러 Laravel 애플리케이션을 개발하는 경우, 애플리케이션 이미지에 고유한 이름을 지정하는 것이 특히 중요합니다.

```shell
sail build --no-cache
```
