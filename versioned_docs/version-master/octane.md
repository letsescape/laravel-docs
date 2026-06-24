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
    - [Specifying the Max Execution Time](#specifying-the-max-execution-time)
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
[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 활용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 유지하고, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Octane may be installed via the Composer package manager: -->
Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

<!-- After installing Octane, you may execute the `octane:install` Artisan command, which will install Octane's configuration file into your application: -->
Octane 설치 후 `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
<!-- ## Server Prerequisites -->
## Server Prerequisites

<a name="frankenphp"></a>
<!-- ### FrankenPHP -->
### FrankenPHP

<!-- [FrankenPHP](https://frankenphp.dev) is a PHP application server, written in Go, that supports modern web features like early hints, Brotli, and Zstandard compression. When you install Octane and choose FrankenPHP as your server, Octane will automatically download and install the FrankenPHP binary for you. -->
[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane과 함께 FrankenPHP를 서버로 선택하면, 필요 시 Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
<!-- #### FrankenPHP via Laravel Sail -->
#### FrankenPHP via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/master/sail), you should run the following commands to install Octane and FrankenPHP: -->
[Laravel Sail](/docs/master/sail)을 사용하여 애플리케이션을 개발할 계획이라면, 다음 명령어들로 Octane 및 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

<!-- Next, you should use the `octane:install` Artisan command to install the FrankenPHP binary: -->
이어 `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

<!-- Finally, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수에는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

<!-- To enable HTTPS, HTTP/2, and HTTP/3, apply these modifications instead: -->
HTTPS, HTTP/2, HTTP/3를 활성화하려면 다음과 같이 수정하세요:

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
보통 FrankenPHP Sail 애플리케이션은 `https://localhost`로 접근해야 합니다. `https://127.0.0.1`로 접근하려면 추가 설정이 필요하며, 이는 [discouraged](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
<!-- #### FrankenPHP via Docker -->
#### FrankenPHP via Docker

<!-- Using FrankenPHP's official Docker images can offer improved performance and the use of additional extensions not included with static installations of FrankenPHP. In addition, the official Docker images provide support for running FrankenPHP on platforms it doesn't natively support, such as Windows. FrankenPHP's official Docker images are suitable for both local development and production usage. -->
FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 향상되고, 정적 설치 버전에서는 포함되지 않은 추가 확장 기능도 사용할 수 있습니다. 또한 공식 Docker 이미지는 FrankenPHP가 기본적으로 지원하지 않는 Windows 등 다양한 플랫폼에서 구동할 수 있도록 지원합니다. FrankenPHP의 공식 Docker 이미지는 로컬 개발과 운영 환경 모두에 적합합니다.

<!-- You may use the following Dockerfile as a starting point for containerizing your FrankenPHP powered Laravel application: -->
FrankenPHP 기반의 Laravel 애플리케이션 컨테이너화의 시작점으로 아래 Dockerfile을 참고할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

<!-- Then, during development, you may utilize the following Docker Compose file to run your application: -->
개발 중에는 다음 Docker Compose 파일을 활용하여 애플리케이션을 실행할 수 있습니다:

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
`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달하면, Octane은 FrankenPHP의 기본 로거를 사용하며, 별도의 설정이 없다면 구조화된 JSON 로그를 생성합니다.

<!-- You may consult [the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/) for more information on running FrankenPHP with Docker. -->
Docker로 FrankenPHP를 실행하는 방법은 [the official FrankenPHP documentation](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="frankenphp-caddyfile"></a>
<!-- #### Custom Caddyfile Configuration -->
#### Custom Caddyfile Configuration

<!-- When using FrankenPHP, you may specify a custom Caddyfile using the `--caddyfile` option when starting Octane: -->
FrankenPHP를 사용할 때, Octane을 시작할 때 `--caddyfile` 옵션을 활용해 사용자 지정 Caddyfile을 지정할 수 있습니다:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

<!-- This allows you to customize FrankenPHP's configuration beyond the default settings, such as adding custom middleware, configuring advanced routing, or setting up custom directives. You may consult the [official Caddy documentation](https://caddyserver.com/docs/caddyfile) for more information on Caddyfile syntax and configuration options. -->
이렇게 하면 기본 설정을 넘어 사용자 지정 미들웨어 추가, 고급 라우팅 구성, 사용자 지정 지시어 설정 등 FrankenPHP의 구성을 세밀하게 제어할 수 있습니다. Caddyfile 문법 및 설정에 관한 자세한 내용은 [official Caddy documentation](https://caddyserver.com/docs/caddyfile)를 참고하세요.

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리 기반으로 동작합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 자동으로 RoadRunner 바이너리를 다운로드하고 설치할 수 있도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner via Laravel Sail -->
#### RoadRunner via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/master/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/master/sail)을 사용하여 애플리케이션을 개발할 경우, Octane과 RoadRunner를 다음 명령어로 설치합니다:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
이어 Sail 셸을 시작하고, 최신 리눅스 기반 RoadRunner 바이너리를 얻으려면 `rr` 실행 파일을 사용합니다:

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- Then, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
`docker-compose.yml` 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, ensure the `rr` binary is executable and build your Sail images: -->
마지막으로 `rr` 바이너리의 실행 권한을 부여하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
<!-- ### Swoole -->
### Swoole

<!-- If you plan to use the Swoole application server to serve your Laravel Octane application, you must install the Swoole PHP extension. Typically, this can be done via PECL: -->
Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 기능을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
<!-- #### Open Swoole -->
#### Open Swoole

<!-- If you want to use the Open Swoole application server to serve your Laravel Octane application, you must install the Open Swoole PHP extension. Typically, this can be done via PECL: -->
Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 기능을 설치해야 합니다. 보통 PECL을 통해 설치합니다:

```shell
pecl install openswoole
```

<!-- Using Laravel Octane with Open Swoole grants the same functionality provided by Swoole, such as concurrent tasks, ticks, and intervals. -->
Laravel Octane을 Open Swoole과 함께 사용할 경우, 동시 작업, 틱, 간격 등 Swoole과 동일한 기능을 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole via Laravel Sail -->
#### Swoole via Laravel Sail

> [!WARNING]
> Sail로 Octane 애플리케이션을 서비스하기 전, Laravel Sail의 최신 버전이 설치되어 있는지 확인하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/master/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `docker-compose.yml` file used by Sail. -->
또는 [Laravel Sail](/docs/master/sail)이라는 공식 Docker 기반 개발 환경을 사용하여 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 포함되어 있습니다. 하지만 Sail에서 사용하는 `docker-compose.yml` 파일에는 별도 설정이 필요합니다.

<!-- To get started, add a `SUPERVISOR_PHP_COMMAND` environment variable to the `laravel.test` service definition in your application's `docker-compose.yml` file. This environment variable will contain the command that Sail will use to serve your application using Octane instead of the PHP development server: -->
먼저 `docker-compose.yml`의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수에는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

<!-- Finally, build your Sail images: -->
마지막으로 Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
<!-- #### Swoole Configuration -->
#### Swoole Configuration

<!-- Swoole supports a few additional configuration options that you may add to your `octane` configuration file if necessary. Because they rarely need to be modified, these options are not included in the default configuration file: -->
Swoole은 필요하다면 `octane` 설정 파일에 추가할 수 있는 몇 가지 옵션을 지원합니다. 이 옵션들은 자주 변경할 필요가 없으므로 기본 설정 파일에는 포함되어 있지 않습니다:

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
Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

<!-- By default, Octane will start the server on port 8000, so you may access your application in a web browser via `http://localhost:8000`. -->
기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`을 통해 애플리케이션에 접근할 수 있습니다.

<a name="keeping-octane-running-in-production"></a>
<!-- #### Keeping Octane Running in Production -->
#### Keeping Octane Running in Production

<!-- If you are deploying your Octane application to production, you should use a process monitor such as Supervisor to ensure the Octane server stays running. A sample Supervisor configuration file for Octane might look like the following: -->
Octane 애플리케이션을 운영 환경에 배포할 경우 프로세스 모니터(Supervisor 등)를 이용해 Octane 서버가 항상 실행 중인지 확인해야 합니다. Octane을 위한 Supervisor 예시 설정 파일은 다음과 같습니다:

```ini
[program:octane]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/example.com/artisan octane:start --server=frankenphp --host=127.0.0.1 --port=8000
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/storage/logs/octane.log
stopwaitsecs=3600
```

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application via HTTPS -->
### Serving Your Application via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
기본적으로 Octane으로 실행되는 애플리케이션은 `http://`가 붙은 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일에서 사용되는 `OCTANE_HTTPS` 환경 변수를 HTTPS로 서비스할 때 `true`로 설정할 수 있습니다. 이 설정값이 `true`로 지정되면, Octane은 Laravel이 생성하는 모든 링크에 `https://` 접두사를 붙이도록 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application via Nginx -->
### Serving Your Application via Nginx

> [!NOTE]
> 서버 설정을 직접 관리하거나 다양한 서비스를 직접 구성하는 것에 익숙하지 않다면, [Laravel Cloud](https://cloud.laravel.com)를 참고하세요. Laravel Cloud는 완전 관리형 Laravel Octane 서비스를 제공합니다.

<!-- In production environments, you should serve your Octane application behind a traditional web server such as Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 서비스하는 것이 좋습니다. 이렇게 하면 정적 자산(이미지, 스타일시트 등) 서비스와 SSL 인증서 종료를 전통적 웹 서버에서 처리할 수 있습니다.

<!-- In the Nginx configuration example below, Nginx will serve the site's static assets and proxy requests to the Octane server that is running on port 8000: -->
아래 Nginx 설정 예시에서 Nginx는 사이트의 정적 자산을 서비스하고, 8000번 포트에서 실행 중인 Octane 서버로 요청을 프록시합니다:

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
Octane 서버가 시작될 때 애플리케이션이 한 번 메모리에 로드되므로, 소스 코드를 수정해도 브라우저 새로고침만으로 변경 내용이 반영되지 않습니다. 예를 들어, `routes/web.php`에 새로운 라우트를 추가하면 서버를 재시작해야 반영됩니다. 편의상, `--watch` 플래그를 사용하면 애플리케이션 내 파일 변경 시 Octane이 자동으로 서버를 재시작하도록 할 수 있습니다:

```shell
php artisan octane:start --watch
```

<!-- Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
이 기능을 사용하려면, 먼저 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 합니다. 또한, 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/octane.php` configuration file. -->
감시할 디렉터리와 파일은 애플리케이션의 `config/octane.php` 설정 파일의 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
<!-- ### Specifying the Worker Count -->
### Specifying the Worker Count

<!-- By default, Octane will start an application request worker for each CPU core provided by your machine. These workers will then be used to serve incoming HTTP requests as they enter your application. You may manually specify how many workers you would like to start using the `--workers` option when invoking the `octane:start` command: -->
기본적으로 Octane은 시스템의 CPU 코어 개수만큼 애플리케이션 요청 워커를 시작합니다. 이 워커들은 HTTP 요청을 처리합니다. 워커 개수를 수동으로 지정하려면 `octane:start` 명령어 실행 시 `--workers` 옵션을 사용할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

<!-- If you are using the Swoole application server, you may also specify how many ["task workers"](#concurrent-tasks) you wish to start: -->
Swoole 애플리케이션 서버를 사용하는 경우, ["task workers"](#concurrent-tasks)도 개수 지정이 가능합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
<!-- ### Specifying the Max Request Count -->
### Specifying the Max Request Count

<!-- To help prevent stray memory leaks, Octane gracefully restarts any worker once it has handled 500 requests. To adjust this number, you may use the `--max-requests` option: -->
메모리 누수 방지를 위해, Octane은 각 워커가 500개의 요청을 처리하면 자동으로 워커를 재시작합니다. 이 수치는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
<!-- ### Specifying the Max Execution Time -->
### Specifying the Max Execution Time

<!-- By default, Laravel Octane sets a maximum execution time of 30 seconds for incoming requests via the `max_execution_time` option in your application's `config/octane.php` configuration file: -->
기본적으로 Laravel Octane은 애플리케이션의 `config/octane.php` 설정 파일의 `max_execution_time` 옵션을 통해 요청별 최대 실행 시간을 30초로 지정합니다:

```php
'max_execution_time' => 30,
```

<!-- This setting defines the maximum number of seconds that an incoming request is allowed to execute before being terminated. Setting this value to `0` will disable the execution time limit entirely. This configuration option is particularly useful for applications that handle long-running requests, such as file uploads, data processing, or API calls to external services. -->
이 설정은 각 요청이 종료되기 전 허용되는 최대 초(second)를 의미합니다. 이 값을 `0`으로 설정하면 실행 시간 제한이 해제됩니다. 이 옵션은 파일 업로드, 데이터 처리, 외부 서비스 API 호출 등 장시간 실행되는 요청을 처리하는 애플리케이션에서 특히 유용합니다.

> [!WARNING]
> `max_execution_time` 설정을 변경했다면, 변경 사항을 적용하기 위해 Octane 서버를 반드시 재시작해야 합니다.

<a name="reloading-the-workers"></a>
<!-- ### Reloading the Workers -->
### Reloading the Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
`octane:reload` 명령어를 사용하면 Octane 서버의 애플리케이션 워커를 안전하게 재시작할 수 있습니다. 일반적으로 코드 배포 후, 새로 배포된 코드가 메모리에 로드되고 이후의 요청에 사용될 수 있도록 이 명령어를 실행해야 합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping the Server -->
### Stopping the Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
`octane:stop` Artisan 명령어로 Octane 서버를 중지시킬 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking the Server Status -->
#### Checking the Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
`octane:status` Artisan 명령어로 Octane 서버의 현재 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection and Octane -->
## Dependency Injection and Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane은 애플리케이션을 한 번 부팅한 후, 요청을 처리하는 동안 메모리에 유지합니다. 이로 인해 애플리케이션 구성시 고려해야 할 몇 가지 유의 사항이 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더 내 `register`와 `boot` 메서드는 워커가 처음 부팅될 때 딱 한 번만 실행됩니다. 이후의 모든 요청은 동일한 애플리케이션 인스턴스를 재사용하게 됩니다.

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a  stale version of the container or request on subsequent requests. -->
이 점을 염두에 두고, 애플리케이션 서비스 컨테이너나 request를 객체 생성자에 주입하는 것은 주의해야 합니다. 만약 그렇게 해두면, 해당 객체가 이후 요청에서도 오래된 컨테이너나 request 인스턴스를 참조할 수 있습니다.

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Octane은 Laravel의 핵심 프레임워크 상태는 요청 사이마다 자동으로 리셋합니다. 하지만 애플리케이션이 생성한 전역 상태까지 항상 자동으로 리셋할 수는 없으므로, Octane 친화적인(Octane friendly) 방식으로 애플리케이션을 설계해야 합니다. 아래 예시들은 Octane 사용 시 자주 문제가 되는 상황들을 설명합니다.

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
일반적으로, 애플리케이션 서비스 컨테이너나 HTTP request 인스턴스를 다른 객체의 생성자에 주입하지 않는 것이 좋습니다. 예를 들어, 다음 바인딩은 전체 서비스 컨테이너를 singleton으로 바인딩되는 객체에 주입합니다:

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
이 경우, 애플리케이션 부팅 시 `Service` 인스턴스가 생성되면 서비스 컨테이너가 주입되고, 이후 요청에서도 같은 `Service` 인스턴스가 동일한(초기) 컨테이너를 계속 참조합니다. 이는 애플리케이션마다 반드시 문제가 되는 것은 아니지만, 부팅 후 나중 혹은 별도 요청에서 추가된 바인딩을 인식하지 못하는 등의 예기치 않은 상황을 유발할 수 있습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a container resolver closure into the service that always resolves the current container instance: -->
우회 방법으로 singleton으로 등록하는 대신 일반 바인딩을 사용하거나, 항상 최신 컨테이너 인스턴스를 가져오도록 컨테이너 리졸버 클로저를 주입할 수 있습니다:

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
글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
<!-- ### Request Injection -->
### Request Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire request instance into an object that is bound as a singleton: -->
일반적으로, 애플리케이션 서비스 컨테이너나 HTTP request 인스턴스를 다른 객체의 생성자에 주입하지 않는 것이 좋습니다. 다음 예시는 전체 request 인스턴스를 singleton으로 바인딩되는 객체에 주입합니다:

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
이 경우, 애플리케이션 부팅 시 `Service` 인스턴스가 생성되면 HTTP 요청이 서비스에 주입되고, 이후 요청에서도 같은 `Service` 인스턴스가 동일한 요청을 계속 참조하게 됩니다. 따라서 헤더, 입력값, 쿼리스트링 등 모든 요청 데이터뿐 아니라 그 밖의 모든 요청 정보가 올바르지 않게 됩니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a request resolver closure into the service that always resolves the current request instance. Or, the most recommended approach is simply to pass the specific request information your object needs to one of the object's methods at runtime: -->
우회 방법으로 singleton 대신 일반 바인딩을 사용하거나, 항상 최신 request 인스턴스를 가져오는 리졸버 클로저를 주입할 수 있습니다. 가장 권장되는 방식은, 필요한 request 정보만 런타임에 객체의 메서드에 직접 전달하는 것입니다:

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
글로벌 `request` 헬퍼는 항상 현재 애플리케이션이 처리 중인 최신 request를 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 안전합니다.

<a name="configuration-repository-injection"></a>
<!-- ### Configuration Repository Injection -->
### Configuration Repository Injection

<!-- In general, you should avoid injecting the configuration repository instance into the constructors of other objects. For example, the following binding injects the configuration repository into an object that is bound as a singleton: -->
일반적으로, 설정 저장소 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 다음 예시는 설정 저장소를 singleton 객체에 주입합니다:

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
이 경우, 요청 사이에서 설정 값이 변경된다면 해당 서비스는 새로운 값을 가져올 수 없습니다(초기 저장소 인스턴스만 참조하기 때문입니다).

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a configuration repository resolver closure to the class: -->
우회 방법으로 singleton 등록 대신 일반 바인딩을 사용하거나, 항상 최신 설정 저장소를 가져오는 리졸버 클로저를 클래스에 주입할 수 있습니다:

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
글로벌 `config` 헬퍼는 항상 최신 설정 저장소 인스턴스를 반환하므로 애플리케이션 내에서 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
<!-- ### Managing Memory Leaks -->
### Managing Memory Leaks

<!-- Remember, Octane keeps your application in memory between requests; therefore, adding data to a statically maintained array will result in a memory leak. For example, the following controller has a memory leak since each request to the application will continue to add data to the static `$data` array: -->
Octane은 요청 사이에 애플리케이션을 메모리에 유지합니다. 그래서 정적으로 관리되는 배열 등에 데이터를 누적하면 메모리 누수가 발생합니다. 아래 컨트롤러 예시는 메모리 누수가 발생하는 패턴입니다. 매 요청마다 static `$data` 배열에 값이 추가됩니다:

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
애플리케이션을 구축할 때 이러한 메모리 누수 패턴이 생기지 않도록 각별히 주의해야 합니다. 로컬 개발 시 점검 도구 등을 통해 애플리케이션 메모리 사용량을 주기적으로 확인하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
<!-- ## Concurrent Tasks -->
## Concurrent Tasks

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may execute operations concurrently via light-weight background tasks. You may accomplish this using Octane's `concurrently` method. You may combine this method with PHP array destructuring to retrieve the results of each operation: -->
Swoole을 사용할 때, 가벼운 백그라운드 작업을 통해 여러 작업을 동시 실행할 수 있습니다. Octane의 `concurrently` 메서드를 활용하면 여러 작업을 손쉽게 병렬로 실행할 수 있습니다. PHP 배열 구조분해(destructuring)와 결합해, 각 작업 결과를 바로 받아올 수 있습니다:

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
동시 작업은 Swoole의 "task worker" 프로세스를 이용하며, 요청을 처리하는 프로세스와는 완전히 별도의 프로세스에서 실행됩니다. 동시 작업 워커 개수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<!-- When invoking the `concurrently` method, you should not provide more than 1024 tasks due to limitations imposed by Swoole's task system. -->
`concurrently` 메서드에 전달할 작업 개수는 Swoole의 과제 시스템(task system) 제한에 따라 1024개를 넘지 않도록 해야 합니다.

<a name="ticks-and-intervals"></a>
<!-- ## Ticks and Intervals -->
## Ticks and Intervals

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may register "tick" operations that will be executed every specified number of seconds. You may register "tick" callbacks via the `tick` method. The first argument provided to the `tick` method should be a string that represents the name of the ticker. The second argument should be a callable that will be invoked at the specified interval. -->
Swoole을 사용할 때, 특정 초 간격마다 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드로 "tick" 콜백을 등록할 수 있고, `tick` 메서드의 첫 번째 인자로 ticker의 이름을 나타내는 문자열, 두 번째 인자로 지정된 간격마다 호출될 콜러블을 전달합니다.

<!-- In this example, we will register a closure to be invoked every 10 seconds. Typically, the `tick` method should be called within the `boot` method of one of your application's service providers: -->
아래 예시는 10초마다 closure를 실행하는 tick을 등록합니다. 일반적으로 `tick` 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

<!-- Using the `immediate` method, you may instruct Octane to immediately invoke the tick callback when the Octane server initially boots, and every N seconds thereafter: -->
`immediate` 메서드를 사용하면 Octane 서버가 부팅될 때 즉시 tick 콜백을 실행하고, 이후 지정된 간격마다 반복 실행하도록 할 수 있습니다:

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
Swoole을 사용할 때, Octane 캐시 드라이버를 사용할 수 있습니다. 이 드라이버는 최대 초당 200만 회의 읽기/쓰기 속도를 자랑하며, 극한의 캐싱이 필요한 애플리케이션에서 강력한 선택지입니다.

<!-- This cache driver is powered by [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). All data stored in the cache is available to all workers on the server. However, the cached data will be flushed when the server is restarted: -->
이 캐시 드라이버는 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 서버의 모든 워커가 캐시된 데이터에 접근할 수 있습니다. 단, 서버를 재시작하면 캐시된 데이터는 모두 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 허용되는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
<!-- ### Cache Intervals -->
### Cache Intervals

<!-- In addition to the typical methods provided by Laravel's cache system, the Octane cache driver features interval based caches. These caches are automatically refreshed at the specified interval and should be registered within the `boot` method of one of your application's service providers. For example, the following cache will be refreshed every five seconds: -->
Laravel의 기본 캐시 시스템 메서드 외에도, Octane 캐시 드라이버는 간격 기반(interval based) 캐시 기능을 지원합니다. 이 캐시는 지정한 시간 간격마다 자동으로 최신 값으로 갱신되며, 보통 서비스 프로바이더의 `boot` 메서드 내에서 정의해야 합니다. 아래 예시는 5초마다 새 값으로 갱신되는 캐시를 만듭니다:

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
Swoole을 사용할 경우, [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 성능을 제공하며, 서버의 모든 워커가 테이블의 데이터에 접근할 수 있습니다. 단, 서버 재시작 시 테이블의 모든 데이터는 손실됩니다.

<!-- Tables should be defined within the `tables` configuration array of your application's `octane` configuration file. An example table that allows a maximum of 1000 rows is already configured for you. The maximum size of string columns may be configured by specifying the column size after the column type as seen below: -->
테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에 정의해야 합니다. 기본적으로 최대 1000개의 row를 허용하는 예시 테이블이 이미 준비되어 있습니다. 문자열 컬럼의 최대 크기는 타입 뒤에 바로 명시할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

<!-- To access a table, you may use the `Octane::table` method: -->
테이블에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.
