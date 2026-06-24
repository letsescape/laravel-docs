<!-- # Laravel Octane -->
# Laravel Octane

- [Introduction](#introduction)
- [Installation](#installation)
- [Server Prerequisites](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Serving Your Application](#serving-your-application)
    - [Serving Your Application via HTTPS](#serving-your-application-via-https)
    - [Serving Your Application via Nginx](#serving-your-application-via-nginx)
    - [Watching for File Changes](#watching-for-file-changes)
    - [Specifying the Worker Count](#specifying-the-worker-count)
    - [Specifying the Max Request Count](#specifying-the-max-request-count)
    - [Reloading the Workers](#reloading-the-workers)
    - [Stopping the Server](#stopping-the-server)
- [Dependency Injection and Octane](#dependency-injection-and-octane)
    - [Container Injection](#container-injection)
    - [Request Injection](#request-injection)
    - [Configuration Repository Injection](#configuration-repository-injection)
- [Managing Memory Leaks](#managing-memory-leaks)
- [Concurrent Tasks](#concurrent-tasks)
- [Ticks and Intervals](#ticks-and-intervals)
- [The Octane Cache](#the-octane-cache)
- [Tables](#tables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Octane](https://github.com/laravel/octane) supercharges your application's performance by serving your application using high-powered application servers, including [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), and [RoadRunner](https://roadrunner.dev). Octane boots your application once, keeps it in memory, and then feeds it requests at supersonic speeds. -->
[Laravel Octane](https://github.com/laravel/octane)은 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 활용하여 여러분의 애플리케이션 성능을 극대화합니다. Octane은 애플리케이션을 단 한 번 부팅한 뒤 메모리에 유지하고, 이후 번개처럼 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Octane may be installed via the Composer package manager: -->
Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

<!-- After installing Octane, you may execute the `octane:install` Artisan command, which will install Octane's configuration file into your application: -->
Octane 설치 후, `octane:install` Artisan 명령어를 실행하면 Octane의 설정 파일이 애플리케이션에 추가됩니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
<!-- ## Server Prerequisites -->
## Server Prerequisites

> [!WARNING]
> Laravel Octane은 [PHP 8.1+](https://php.net/releases/)이 필요합니다.

<a name="frankenphp"></a>
<!-- ### FrankenPHP -->
### FrankenPHP

<!-- [FrankenPHP](https://frankenphp.dev) is a PHP application server, written in Go, that supports modern web features like early hints, Brotli, and Zstandard compression. When you install Octane and choose FrankenPHP as your server, Octane will automatically download and install the FrankenPHP binary for you. -->
[FrankenPHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면 Octane이 FrankenPHP 실행 파일을 자동으로 다운로드 및 설치해 줍니다.

<a name="frankenphp-via-laravel-sail"></a>
<!-- #### FrankenPHP via Laravel Sail -->
#### FrankenPHP via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/11.x/sail), you should run the following commands to install Octane and FrankenPHP: -->
[Laravel Sail](/docs/11.x/sail) 환경에서 개발할 예정이라면 다음과 같은 명령어로 Octane과 FrankenPHP를 설치해야 합니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

<!-- Next, you should use the `octane:install` Artisan command to install the FrankenPHP binary: -->
그 다음, `octane:install` Artisan 명령어를 사용해 FrankenPHP 실행 파일을 설치합니다.

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

<!-- Finally, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가해야 합니다. 이 환경 변수는 Sail에서 Octane을 사용해 애플리케이션을 서비스하기 위해 실행할 명령어를 지정합니다(기본 PHP 개발 서버 대신 Octane을 사용).

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

<!-- To enable HTTPS, HTTP/2, and HTTP/3, apply these modifications instead: -->
HTTPS, HTTP/2, HTTP/3 지원을 활성화하려면 다음과 같이 추가 설정을 적용합니다.

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

<!-- Typically, you should access your FrankenPHP Sail application via `https://localhost`, as using `https://127.0.0.1` requires additional configuration and is [discouraged](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker). -->
일반적으로 FrankenPHP Sail 애플리케이션에는 `https://localhost`를 통해 접근해야 하며, `https://127.0.0.1` 사용은 추가 구성이 필요하므로 [discouraged](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
<!-- #### FrankenPHP via Docker -->
#### FrankenPHP via Docker

<!-- Using FrankenPHP's official Docker images can offer improved performance and the use of additional extensions not included with static installations of FrankenPHP. In addition, the official Docker images provide support for running FrankenPHP on platforms it doesn't natively support, such as Windows. FrankenPHP's official Docker images are suitable for both local development and production usage. -->
공식 FrankenPHP Docker 이미지를 사용하면 성능이 향상되고, 정적 설치에는 없는 추가 확장 기능도 사용할 수 있습니다. 또한, 공식 Docker 이미지는 FrankenPHP가 네이티브로 지원하지 않는 플랫폼(예: Windows)에서도 구동이 가능합니다. 공식 Docker 이미지는 로컬 개발과 운영 환경 모두에 적합합니다.

<!-- You may use the following Dockerfile as a starting point for containerizing your FrankenPHP powered Laravel application: -->
아래 예제 Dockerfile을 활용해 FrankenPHP 기반의 Laravel 애플리케이션을 컨테이너화할 수 있습니다.

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

<!-- Then, during development, you may utilize the following Docker Compose file to run your application: -->
개발 시에는 다음과 같은 Docker Compose 파일로 애플리케이션을 실행할 수 있습니다.

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

<!-- If the `--log-level` option is explicitly passed to the `php artisan octane:start` command, Octane will use FrankenPHP's native logger and, unless configured differently, will produce structured JSON logs. -->
`php artisan octane:start` 명령에 `--log-level` 옵션을 명시적으로 지정하면 Octane은 FrankenPHP 고유의 로거를 사용하며, 별도의 설정이 없으면 구조화된 JSON 로그가 생성됩니다.

<!-- You may consult [the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/) for more information on running FrankenPHP with Docker. -->
Docker에서 FrankenPHP를 실행하는 자세한 방법은 [the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev)는 Go로 구현된 RoadRunner 실행 파일을 사용합니다. RoadRunner 기반 Octane 서버를 처음 시작하면 Octane이 RoadRunner 실행 파일을 다운로드 및 설치해 줄 것인지 확인합니다.

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner via Laravel Sail -->
#### RoadRunner via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/11.x/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/11.x/sail) 환경에서 개발할 예정이라면 다음 명령어로 Octane과 RoadRunner를 설치합니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
그 다음 Sail 셸을 시작하고 `rr` 실행 파일을 사용하여 최신 리눅스용 RoadRunner 바이너리 빌드를 받아야 합니다.

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- Then, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
그리고 `docker-compose.yml` 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 환경 변수는 Octane을 사용하여 애플리케이션을 서비스할 때 사용됩니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, ensure the `rr` binary is executable and build your Sail images: -->
마지막으로, `rr` 바이너리의 실행 권한을 부여하고 Sail 이미지를 빌드합니다.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
<!-- ### Swoole -->
### Swoole

<!-- If you plan to use the Swoole application server to serve your Laravel Octane application, you must install the Swoole PHP extension. Typically, this can be done via PECL: -->
Swoole 애플리케이션 서버를 이용해 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 일반적으로 PECL을 통해 설치할 수 있습니다.

```shell
pecl install swoole
```

<a name="openswoole"></a>
<!-- #### Open Swoole -->
#### Open Swoole

<!-- If you want to use the Open Swoole application server to serve your Laravel Octane application, you must install the Open Swoole PHP extension. Typically, this can be done via PECL: -->
Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 모듈을 설치해야 합니다. PECL을 통해 설치할 수 있습니다.

```shell
pecl install openswoole
```

<!-- Using Laravel Octane with Open Swoole grants the same functionality provided by Swoole, such as concurrent tasks, ticks, and intervals. -->
Laravel Octane을 Open Swoole과 함께 사용하면 Swoole과 동일한 동시 작업, 틱(tick), 인터벌(interval) 등의 기능을 모두 누릴 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole via Laravel Sail -->
#### Swoole via Laravel Sail

> [!WARNING]
> Sail로 Octane 애플리케이션을 서비스하기 전에 Laravel Sail의 최신 버전을 사용하고 있는지 확인하고, 애플리케이션 루트 디렉토리에서 `./vendor/bin/sail build --no-cache` 명령을 실행하세요.

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/11.x/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `docker-compose.yml` file used by Sail. -->
또는, [Laravel Sail](/docs/11.x/sail)을 사용해 Docker 기반 공식 개발 환경에서 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail은 Swoole 확장을 기본적으로 포함하고 있지만, `docker-compose.yml` 파일을 추가로 조정해야 합니다.

<!-- To get started, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
먼저, `docker-compose.yml` 파일에서 `laravel.test` 서비스의 환경 변수에 `SUPERVISOR_PHP_COMMAND`를 추가하세요. 이 변수는 Octane을 사용해 애플리케이션을 서비스할 때 실행할 명령어입니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, build your Sail images: -->
마지막으로, Sail 이미지를 빌드합니다.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
<!-- #### Swoole Configuration -->
#### Swoole Configuration

<!-- Swoole supports a few additional configuration options that you may add to your `octane` configuration file if necessary. Because they rarely need to be modified, these options are not included in the default configuration file: -->
필요하다면, `octane` 설정 파일에 몇 가지 Swoole 추가 옵션을 지정할 수 있습니다. 대부분의 경우 수정할 일이 드물기 때문에 기본값에는 포함되어 있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
<!-- ## Serving Your Application -->
## Serving Your Application

<!-- The Octane server can be started via the `octane:start` Artisan command. By default, this command will utilize the server specified by the `server` configuration option of your application's `octane` configuration file: -->
Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일에 있는 `server` 옵션에 설정된 서버를 사용합니다.

```shell
php artisan octane:start
```

<!-- By default, Octane will start the server on port 8000, so you may access your application in a web browser via `http://localhost:8000`. -->
기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`으로 애플리케이션에 접근할 수 있습니다.

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application via HTTPS -->
### Serving Your Application via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
기본적으로 Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 만약 HTTPS로 서비스를 제공한다면, 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 지정해야 합니다. 이 값을 `true`로 설정하면 Octane이 Laravel에게 모든 링크를 `https://`로 시작하도록 안내합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application via Nginx -->
### Serving Your Application via Nginx

> [!NOTE]
> 직접 서버 설정을 관리하거나 다양한 서비스 설정에 익숙하지 않다면, [Laravel Forge](https://forge.laravel.com) 활용을 고려해보세요.

<!-- In production environments, you should serve your Octane application behind a traditional web server such as Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
운영 환경에서는 Octane 애플리케이션을 Nginx나 Apache와 같은 전통적인 웹 서버 뒤에서 서비스해야 합니다. 이렇게 하면 웹 서버가 정적 자산(이미지, 스타일시트 등)을 직접 제공하고, SSL 인증서 종료도 처리할 수 있습니다.

<!-- In the Nginx configuration example below, Nginx will serve the site's static assets and proxy requests to the Octane server that is running on port 8000: -->
아래 Nginx 설정 예시에서는 정적 자산은 Nginx가 제공하고, 나머지 모든 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시하게 됩니다.

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```

<a name="watching-for-file-changes"></a>
<!-- ### Watching for File Changes -->
### Watching for File Changes

<!-- Since your application is loaded in memory once when the Octane server starts, any changes to your application's files will not be reflected when you refresh your browser. For example, route definitions added to your `routes/web.php` file will not be reflected until the server is restarted. For convenience, you may use the `--watch` flag to instruct Octane to automatically restart the server on any file changes within your application: -->
Octane 서버는 시작 시 애플리케이션을 메모리에 올려둡니다. 따라서, 파일을 수정해도 바로 반영되지 않으며, 예를 들어 `routes/web.php`에서 라우트를 추가해도 서버를 재시작하기 전까지는 브라우저에서 볼 수 없습니다. 이를 편리하게 처리하기 위해 `--watch` 플래그를 사용하면, 애플리케이션 파일에 변경이 감지될 때마다 자동으로 서버가 재시작됩니다.

```shell
php artisan octane:start --watch
```

<!-- Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
이 기능을 사용하려면, 먼저 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 합니다. 또한 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/octane.php` configuration file. -->
어떤 디렉터리와 파일을 감시할지 설정하려면, 애플리케이션의 `config/octane.php` 파일의 `watch` 설정 옵션을 조정하면 됩니다.

<a name="specifying-the-worker-count"></a>
<!-- ### Specifying the Worker Count -->
### Specifying the Worker Count

<!-- By default, Octane will start an application request worker for each CPU core provided by your machine. These workers will then be used to serve incoming HTTP requests as they enter your application. You may manually specify how many workers you would like to start using the `--workers` option when invoking the `octane:start` command: -->
기본적으로 Octane은 시스템의 각 CPU 코어당 하나의 애플리케이션 요청 워커를 시작합니다. 이 워커들이 들어오는 HTTP 요청을 처리하게 됩니다. 그러나, `octane:start` 명령어에 `--workers` 옵션을 추가하여 워커 수를 직접 지정할 수도 있습니다.

```shell
php artisan octane:start --workers=4
```

<!-- If you are using the Swoole application server, you may also specify how many ["task workers"](#concurrent-tasks) you wish to start: -->
Swoole 애플리케이션 서버를 사용하는 경우, ["task workers"](#concurrent-tasks)의 수 또한 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
<!-- ### Specifying the Max Request Count -->
### Specifying the Max Request Count

<!-- To help prevent stray memory leaks, Octane gracefully restarts any worker once it has handled 500 requests. To adjust this number, you may use the `--max-requests` option: -->
의도치 않은 메모리 누수를 예방하기 위해, Octane은 각 워커가 500건의 요청을 처리하면 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션을 사용해 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
<!-- ### Reloading the Workers -->
### Reloading the Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
`octane:reload` 명령어로 Octane 서버의 애플리케이션 워커를 부드럽게 재시작할 수 있습니다. 일반적으로, 배포 후에 새로 배포된 코드가 메모리에 반영되도록 수행합니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping the Server -->
### Stopping the Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
`octane:stop` Artisan 명령어로 Octane 서버를 중지할 수 있습니다.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking the Server Status -->
#### Checking the Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
`octane:status` Artisan 명령어로 현재 Octane 서버의 상태를 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection and Octane -->
## Dependency Injection and Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane은 애플리케이션을 한 번만 부팅해서 메모리에 올리고, 요청을 처리할 때마다 같은 애플리케이션 인스턴스를 계속 재사용합니다. 이로 인해 애플리케이션을 개발할 때 유의해야 할 사항이 있습니다. 예를 들어, 서비스 프로바이더의 `register`나 `boot` 메서드는 워커가 처음 부팅될 때 단 한 번만 실행됩니다. 이후 요청에서는 항상 같은 애플리케이션 인스턴스가 사용됩니다.

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a  stale version of the container or request on subsequent requests. -->
이로 인해, 애플리케이션 서비스 컨테이너나 요청(Request) 객체 등을 클래스의 생성자에 주입하면 이후 요청에서 오래된 컨테이너나 요청 인스턴스를 참조하게 되므로 주의가 필요합니다.

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Laravel 프레임워크의 기본 상태는 Octane이 자동으로 요청마다 초기화해줍니다. 하지만 애플리케이션이 전역 상태를 직접 관리하는 경우에는 Octane이 이를 알 수 없으므로 주의해서 개발해야 합니다. 아래에서는 Octane 사용 시 문제가 될 수 있는 대표적인 상황을 안내합니다.

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
일반적으로, 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 직접 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 다음 바인딩은 서비스 전체에 애플리케이션 컨테이너를 싱글톤 형태로 주입하고 있습니다.

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the container will be injected into the service and that same container will be held by the `Service` instance on subsequent requests. This **may** not be a problem for your particular application; however, it can lead to the container unexpectedly missing bindings that were added later in the boot cycle or by a subsequent request. -->
이 예제에서 만약 `Service` 인스턴스가 애플리케이션 부트 과정에서 생성된다면, 그 시점의 컨테이너 인스턴스가 서비스에 주입되고 이후 요청에서도 같은 `Service` 인스턴스가 계속 그 컨테이너를 사용하게 됩니다. 이는 실제로 문제가 되지 않을 수도 있지만, 이후 부트 단계나 다음 요청에서 컨테이너에 새로운 바인딩이 추가돼도 이 서비스에서는 이를 인식하지 못하는 문제가 생길 수 있습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a container resolver closure into the service that always resolves the current container instance: -->
이를 해결하려면, 싱글톤 대신 일반 바인딩을 사용하거나, 컨테이너를 항상 최신 인스턴스로 반환하는 클로저를 서비스에 주입하는 방식으로 개선할 수 있습니다.

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

<!-- The global `app` helper and the `Container::getInstance()` method will always return the latest version of the application container. -->
`app` 헬퍼 함수와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
<!-- ### Request Injection -->
### Request Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire request instance into an object that is bound as a singleton: -->
애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 다른 객체의 생성자에 직접 주입하는 것도 역시 지양해야 합니다. 예를 들어, 다음 바인딩은 싱글톤 객체에 전체 요청 인스턴스를 주입하고 있습니다.

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the HTTP request will be injected into the service and that same request will be held by the `Service` instance on subsequent requests. Therefore, all headers, input, and query string data will be incorrect, as well as all other request data. -->
이 예제에서 `Service` 인스턴스가 부트 과정에서 생성되면, 그 시점의 HTTP 요청이 서비스에 주입되고 이후 요청에서도 같은 `Service` 인스턴스가 같은 요청 인스턴스를 사용하게 됩니다. 결과적으로 헤더, 입력값, 쿼리스트링 등 모든 요청 데이터가 올바르지 않게 됩니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a request resolver closure into the service that always resolves the current request instance. Or, the most recommended approach is simply to pass the specific request information your object needs to one of the object's methods at runtime: -->
이 문제를 피하려면, 싱글톤 대신 일반 바인딩을 사용하거나, 항상 최신 요청 인스턴스를 반환하는 클로저를 주입하는 방식, 혹은 가장 추천되는 방법으로 필요한 요청 데이터를 런타임에 객체의 메서드에 직접 전달하는 방식이 있습니다.

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```

<!-- The global `request` helper will always return the request the application is currently handling and is therefore safe to use within your application. -->
전역 `request` 헬퍼는 항상 현재 처리 중인 요청 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 타입힌트는 사용해도 괜찮습니다.

<a name="configuration-repository-injection"></a>
<!-- ### Configuration Repository Injection -->
### Configuration Repository Injection

<!-- In general, you should avoid injecting the configuration repository instance into the constructors of other objects. For example, the following binding injects the configuration repository into an object that is bound as a singleton: -->
설정(Configuration) 리포지토리 인스턴스를 다른 객체의 생성자에 직접 주입하는 것도 일반적으로 피하는 것이 좋습니다. 아래 예시는 싱글톤 객체에 설정 리포지토리를 주입하고 있습니다.

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```

<!-- In this example, if the configuration values change between requests, that service will not have access to the new values because it's depending on the original repository instance. -->
이 경우, 요청 사이에 설정값이 변경돼도 해당 서비스에서는 항상 최초의 설정 리포지토리 인스턴스만 참조하게 되어 새로운 설정 값에 접근할 수 없습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a configuration repository resolver closure to the class: -->
해결 방안으로는, 싱글톤 대신 일반 바인딩을 사용하거나, 항상 최신 설정 리포지토리를 반환하는 클로저를 주입할 수 있습니다.

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

<!-- The global `config` will always return the latest version of the configuration repository and is therefore safe to use within your application. -->
전역 `config` 헬퍼는 항상 최신 설정 리포지토리를 반환하므로 애플리케이션에서 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
<!-- ### Managing Memory Leaks -->
### Managing Memory Leaks

<!-- Remember, Octane keeps your application in memory between requests; therefore, adding data to a statically maintained array will result in a memory leak. For example, the following controller has a memory leak since each request to the application will continue to add data to the static `$data` array: -->
Octane은 요청 사이에도 애플리케이션을 메모리에 유지하므로, 정적(static) 배열 등에 데이터를 계속 추가할 경우 메모리 누수가 발생합니다. 예를 들어, 아래 컨트롤러 코드는 요청이 들어올 때마다 정적 `$data` 배열에 데이터를 추가하므로 메모리 누수를 일으킵니다.

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```

<!-- While building your application, you should take special care to avoid creating these types of memory leaks. It is recommended that you monitor your application's memory usage during local development to ensure you are not introducing new memory leaks into your application. -->
애플리케이션을 개발할 때 이런 유형의 메모리 누수를 만들지 않도록 각별히 주의해야 합니다. 개발 환경에서 애플리케이션의 메모리 사용량을 모니터링하여, 새로운 메모리 누수가 있는지 점검하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
<!-- ## Concurrent Tasks -->
## Concurrent Tasks

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may execute operations concurrently via light-weight background tasks. You may accomplish this using Octane's `concurrently` method. You may combine this method with PHP array destructuring to retrieve the results of each operation: -->
Swoole을 사용할 때, 경량 백그라운드 작업을 통해 여러 동작을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메서드를 사용하면 이를 쉽게 구현할 수 있습니다. PHP 배열 디스트럭처링과 결합하여 각 동작의 결과를 받을 수 있습니다.

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

<!-- Concurrent tasks processed by Octane utilize Swoole's "task workers", and execute within an entirely different process than the incoming request. The amount of workers available to process concurrent tasks is determined by the `--task-workers` directive on the `octane:start` command: -->
동시 작업은 Swoole의 "작업 워커(task workers)"에서 별도의 프로세스로 처리되며, 요청과는 완전히 분리되어 동작합니다. 이 작업 워커의 수는 `octane:start` 명령어에서 `--task-workers` 옵션으로 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<!-- When invoking the `concurrently` method, you should not provide more than 1024 tasks due to limitations imposed by Swoole's task system. -->
`concurrently` 메서드 사용 시에는 Swoole 태스크 시스템의 제한으로 1024개 이하의 작업만 제공해야 합니다.

<a name="ticks-and-intervals"></a>
<!-- ## Ticks and Intervals -->
## Ticks and Intervals

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may register "tick" operations that will be executed every specified number of seconds. You may register "tick" callbacks via the `tick` method. The first argument provided to the `tick` method should be a string that represents the name of the ticker. The second argument should be a callable that will be invoked at the specified interval. -->
Swoole 사용 시, 특정 초마다 실행되는 "틱(tick)" 작업을 등록할 수 있습니다. `tick` 메서드를 사용해 "tick" 콜백을 지정하며, `tick` 메서드의 첫 번째 인자는 ticker의 이름을 나타내는 문자열이고, 두 번째 인자는 지정된 간격마다 호출될 콜러블(callable)입니다.

<!-- In this example, we will register a closure to be invoked every 10 seconds. Typically, the `tick` method should be called within the `boot` method of one of your application's service providers: -->
아래 예시는 매 10초마다 실행되는 클로저를 등록합니다. 보통 `tick` 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출합니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

<!-- Using the `immediate` method, you may instruct Octane to immediately invoke the tick callback when the Octane server initially boots, and every N seconds thereafter: -->
`immediate` 메서드를 활용하면 Octane 서버 최초 부팅 시에도 틱 콜백이 즉시 한 번 실행되고, 이후에는 지정한 간격만큼 계속 반복됩니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
<!-- ## The Octane Cache -->
## The Octane Cache

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may leverage the Octane cache driver, which provides read and write speeds of up to 2 million operations per second. Therefore, this cache driver is an excellent choice for applications that need extreme read / write speeds from their caching layer. -->
Swoole 환경에서 Octane 캐시 드라이버를 사용하면 초당 최대 2백만 번의 읽기/쓰기가 가능한 매우 빠른 캐시를 구현할 수 있습니다. 극한의 캐시 속도가 필요한 애플리케이션에는 최적의 선택입니다.

<!-- This cache driver is powered by [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). All data stored in the cache is available to all workers on the server. However, the cached data will be flushed when the server is restarted: -->
이 캐시 드라이버는 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 모든 워커에서 동일한 데이터를 공유할 수 있습니다. 다만, 서버가 재시작되면 모든 캐시 데이터는 초기화됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 허용되는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
<!-- ### Cache Intervals -->
### Cache Intervals

<!-- In addition to the typical methods provided by Laravel's cache system, the Octane cache driver features interval based caches. These caches are automatically refreshed at the specified interval and should be registered within the `boot` method of one of your application's service providers. For example, the following cache will be refreshed every five seconds: -->
Laravel의 일반적인 캐시 시스템 기능 외에도 Octane 캐시는 "인터벌 기반 캐시"를 제공합니다. 이 캐시는 지정한 간격마다 자동으로 갱신되며, 서비스 프로바이더의 `boot` 메서드 내에서 등록해야 합니다. 아래 예시에서는 5초마다 캐시가 새 랜덤 문자열로 갱신됩니다.

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may define and interact with your own arbitrary [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). Swoole tables provide extreme performance throughput and the data in these tables can be accessed by all workers on the server. However, the data within them will be lost when the server is restarted. -->
Swoole 환경에서는 여러분이 직접 임의의 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 제공하며, 모든 서버 워커에서 데이터 접근이 가능합니다. 단, 서버 재시작 시 데이터는 모두 사라집니다.

<!-- Tables should be defined within the `tables` configuration array of your application's `octane` configuration file. An example table that allows a maximum of 1000 rows is already configured for you. The maximum size of string columns may be configured by specifying the column size after the column type as seen below: -->
테이블은 애플리케이션 `octane` 설정 파일의 `tables` 배열에서 정의하며, 최대 행(row) 수를 설정할 수 있습니다. 아래는 최대 1000개의 행과 string 컬럼 크기를 설정한 예시입니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

<!-- To access a table, you may use the `Octane::table` method: -->
테이블에 접근하려면 `Octane::table` 메서드를 사용합니다.

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float` 세 가지입니다.
