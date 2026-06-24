<!-- # Laravel Octane -->
# Laravel Octane

- [Introduction](#introduction)
- [Installation](#installation)
- [Server Prerequisites](#server-prerequisites)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Serving Your Application](#serving-your-application)
    - [Serving Your Application Via HTTPS](#serving-your-application-via-https)
    - [Serving Your Application Via Nginx](#serving-your-application-via-nginx)
    - [Watching For File Changes](#watching-for-file-changes)
    - [Specifying The Worker Count](#specifying-the-worker-count)
    - [Specifying The Max Request Count](#specifying-the-max-request-count)
    - [Reloading The Workers](#reloading-the-workers)
    - [Stopping The Server](#stopping-the-server)
- [Dependency Injection & Octane](#dependency-injection-and-octane)
    - [Container Injection](#container-injection)
    - [Request Injection](#request-injection)
    - [Configuration Repository Injection](#configuration-repository-injection)
- [Managing Memory Leaks](#managing-memory-leaks)
- [Concurrent Tasks](#concurrent-tasks)
- [Ticks & Intervals](#ticks-and-intervals)
- [The Octane Cache](#the-octane-cache)
- [Tables](#tables)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Octane](https://github.com/laravel/octane) supercharges your application's performance by serving your application using high-powered application servers, including [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), and [RoadRunner](https://roadrunner.dev). Octane boots your application once, keeps it in memory, and then feeds it requests at supersonic speeds. -->
[Laravel Octane](https://github.com/laravel/octane)는 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev)와 같은 고성능 애플리케이션 서버를 이용하여 애플리케이션의 성능을 극대화해 줍니다. Octane은 애플리케이션을 한 번만 부팅한 뒤 메모리에 상주시켜, 이후 초고속으로 요청을 처리합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Octane may be installed via the Composer package manager: -->
Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

<!-- After installing Octane, you may execute the `octane:install` Artisan command, which will install Octane's configuration file into your application: -->
Octane을 설치한 후에는 `octane:install` Artisan 명령을 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
<!-- ## Server Prerequisites -->
## Server Prerequisites

> [!WARNING]
> Laravel Octane을 사용하려면 [PHP 8.0+](https://php.net/releases/)이 필요합니다.

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리가 동작의 핵심입니다. RoadRunner 기반 Octane 서버를 처음 실행하면, Octane이 필요한 RoadRunner 바이너리를 자동으로 다운로드 및 설치하도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner Via Laravel Sail -->
#### RoadRunner Via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/9.x/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/9.x/sail) 환경에서 애플리케이션을 개발하려면, 아래 명령어로 Octane과 RoadRunner를 설치할 수 있습니다.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
다음으로, Sail 쉘을 시작한 후 `rr` 실행 파일을 이용해 최신 리눅스용 RoadRunner 바이너리를 받아야 합니다.

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- After installing the RoadRunner binary, you may exit your Sail shell session. You will now need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
RoadRunner 바이너리가 설치되면, Sail 쉘에서 나와도 됩니다. 이제 애플리케이션을 계속 실행하려면, Sail에서 사용하는 `supervisor.conf` 파일을 조정해야 합니다. 우선 `sail:publish` Artisan 명령을 실행합니다.

```shell
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
그 다음, 애플리케이션의 `docker/supervisord.conf` 파일에서 `command` 지시어를 아래와 같이 수정하여 PHP 개발 서버 대신 Octane을 사용하도록 변경합니다.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=80
```

<!-- Finally, ensure the `rr` binary is executable and build your Sail images: -->
마지막으로, `rr` 바이너리의 실행 권한을 부여하고, Sail 이미지를 빌드합니다.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
<!-- ### Swoole -->
### Swoole

<!-- If you plan to use the Swoole application server to serve your Laravel Octane application, you must install the Swoole PHP extension. Typically, this can be done via PECL: -->
Laravel Octane 애플리케이션을 Swoole 애플리케이션 서버로 실행하려면 Swoole PHP 확장(extension)을 먼저 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다.

```shell
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole Via Laravel Sail -->
#### Swoole Via Laravel Sail

> [!WARNING]
> Sail에서 Octane 애플리케이션을 실행하기 전에, Laravel Sail의 최신 버전을 사용 중인지 확인하고, 애플리케이션 루트 디렉토리에서 `./vendor/bin/sail build --no-cache` 명령을 실행하십시오.

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/9.x/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
또는, [Laravel Sail](/docs/9.x/sail) (공식 Docker 기반 개발 환경)을 이용하여 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail에는 Swoole 확장이 기본적으로 포함되어 있습니다. 다만, 애플리케이션을 계속 실행하려면 Sail에서 사용하는 `supervisor.conf` 파일을 조정해야 합니다. 우선 `sail:publish` Artisan 명령을 실행합니다.

```shell
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
그 다음, 애플리케이션의 `docker/supervisord.conf` 파일에서 `command` 지시어를 아래와 같이 수정하여 PHP 개발 서버 대신 Octane을 사용하도록 변경합니다.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

<!-- Finally, build your Sail images: -->
마지막으로 Sail 이미지를 빌드합니다.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
<!-- #### Swoole Configuration -->
#### Swoole Configuration

<!-- Swoole supports a few additional configuration options that you may add to your `octane` configuration file if necessary. Because they rarely need to be modified, these options are not included in the default configuration file: -->
Swoole은 필요에 따라 `octane` 설정 파일에 추가할 수 있는 몇 가지 추가 옵션을 지원합니다. 이 옵션들은 자주 변경하지 않아도 되므로 기본 설정 파일에는 포함되어 있지 않습니다.

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
Octane 서버는 `octane:start` Artisan 명령을 통해 시작할 수 있습니다. 이 명령은 기본적으로 애플리케이션의 `octane` 설정 파일의 `server` 설정 옵션에서 지정한 서버를 사용합니다.

```shell
php artisan octane:start
```

<!-- By default, Octane will start the server on port 8000, so you may access your application in a web browser via `http://localhost:8000`. -->
기본적으로 Octane은 8000번 포트로 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000` 주소로 애플리케이션에 접속할 수 있습니다.

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application Via HTTPS -->
### Serving Your Application Via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
기본적으로 Octane으로 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 만약 HTTPS로 서비스를 제공한다면, 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정할 수 있습니다. 이 값을 `true`로 설정하면, Octane이 Laravel에게 모든 링크를 `https://`로 시작하도록 안내합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application Via Nginx -->
### Serving Your Application Via Nginx

> [!NOTE]
> 직접 서버 설정을 관리하거나 Laravel Octane 애플리케이션을 제대로 운영하기에 아직 익숙하지 않다면, [Laravel Forge](https://forge.laravel.com) 서비스를 검토해 보시기 바랍니다.

<!-- In production environments, you should serve your Octane application behind a traditional web server such as a Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 일반적인 웹 서버 뒤에서 서비스하는 것이 좋습니다. 이렇게 하면 웹 서버가 이미지, 스타일시트 등 정적 자산을 제공하고 SSL 인증서 종료도 처리할 수 있습니다.

<!-- In the Nginx configuration example below, Nginx will serve the site's static assets and proxy requests to the Octane server that is running on port 8000: -->
아래의 Nginx 설정 예시에서는 정적 자산 요청을 Nginx가 처리하고, 나머지 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다.

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
<!-- ### Watching For File Changes -->
### Watching For File Changes

<!-- Since your application is loaded in memory once when the Octane server starts, any changes to your application's files will not be reflected when you refresh your browser. For example, route definitions added to your `routes/web.php` file will not be reflected until the server is restarted. For convenience, you may use the `--watch` flag to instruct Octane to automatically restart the server on any file changes within your application: -->
Octane 서버가 시작될 때 애플리케이션이 메모리에 적재되므로, 애플리케이션 파일을 변경해도 브라우저를 새로고침하는 것만으로는 반영되지 않습니다. (예를 들어, `routes/web.php` 파일에 라우트를 추가하면 서버를 재시작해야 적용됩니다.) 이러한 번거로움을 줄이기 위해, `--watch` 플래그를 사용하여 애플리케이션 파일이 변경될 때마다 Octane 서버를 자동으로 재시작하도록 할 수 있습니다.

```shell
php artisan octane:start --watch
```

<!-- Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
이 기능을 사용하려면, 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감지 라이브러리도 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/octane.php` configuration file. -->
어떤 디렉터리와 파일을 감지할지 여부는 `config/octane.php`의 `watch` 설정 옵션에서 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
<!-- ### Specifying The Worker Count -->
### Specifying The Worker Count

<!-- By default, Octane will start an application request worker for each CPU core provided by your machine. These workers will then be used to serve incoming HTTP requests as they enter your application. You may manually specify how many workers you would like to start using the `--workers` option when invoking the `octane:start` command: -->
기본적으로 Octane은 시스템의 CPU 코어 수에 맞춰 워커(애플리케이션 요청을 담당하는 작업자 프로세스)를 시작합니다. 이 워커들이 HTTP 요청을 받아 애플리케이션을 서비스합니다. 하지만, `octane:start` 명령에서 `--workers` 옵션으로 워커 개수를 직접 지정할 수도 있습니다.

```shell
php artisan octane:start --workers=4
```

<!-- If you are using the Swoole application server, you may also specify how many ["task workers"](#concurrent-tasks) you wish to start: -->
Swoole 애플리케이션 서버를 사용할 경우, 시작할 ["task workers"](#concurrent-tasks) 개수도 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
<!-- ### Specifying The Max Request Count -->
### Specifying The Max Request Count

<!-- To help prevent stray memory leaks, Octane gracefully restarts any worker once it has handled 500 requests. To adjust this number, you may use the `--max-requests` option: -->
메모리 누수 방지를 돕기 위해, Octane은 각 워커가 500개의 요청을 처리하면 자동으로 모아서 재시작합니다. 이 수치는 `--max-requests` 옵션으로 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
<!-- ### Reloading The Workers -->
### Reloading The Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
Octane 서버의 애플리케이션 워커는 `octane:reload` 명령을 사용하여 부드럽게 재시작할 수 있습니다. 일반적으로 신규 코드 배포 후, 새로 배포된 애플리케이션 코드가 메모리에 반영되도록 이 명령을 실행하는 것이 좋습니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping The Server -->
### Stopping The Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
Octane 서버는 `octane:stop` Artisan 명령으로 중지할 수 있습니다.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking The Server Status -->
#### Checking The Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
현재 Octane 서버의 상태는 `octane:status` Artisan 명령으로 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection & Octane -->
## Dependency Injection & Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 보관하고, 요청을 처리할 때마다 이 인스턴스를 재활용합니다. 이 때문에 애플리케이션을 개발할 때 주의해야 할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅될 때 한 번만 실행됩니다. 이후의 요청에서는 같은 애플리케이션 인스턴스를 반복해서 사용합니다.

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a  stale version of the container or request on subsequent requests. -->
이런 이유로, **애플리케이션 서비스 컨테이너나 request 객체를 다른 객체의 생성자에 주입하는 것은 주의해야 합니다.** 그렇게 하면 해당 객체가 이후의 요청에서도 동일한(예전 상태의) 컨테이너나 request를 참조하게 될 수 있습니다.

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Octane은 기본적으로 프레임워크가 유지하는 상태는 요청마다 자동으로 초기화합니다. 하지만, 애플리케이션이 전역(글로벌)으로 만든 상태는 Octane이 초기화 방법을 알지 못할 수 있으니 Octane에 맞는 애플리케이션 설계 방식을 유의해야 합니다. 아래에서는 Octane 사용 시 문제가 될 수 있는 대표적인 상황들을 안내합니다.

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
일반적으로, 애플리케이션 서비스 컨테이너나 HTTP request 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 코드는 애플리케이션 서비스 컨테이너 전체를 싱글턴으로 바인딩된 객체의 생성자에 주입합니다.

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the container will be injected into the service and that same container will be held by the `Service` instance on subsequent requests. This **may** not be a problem for your particular application; however, it can lead to the container unexpectedly missing bindings that were added later in the boot cycle or by a subsequent request. -->
이 예시에서 만약 `Service` 인스턴스가 애플리케이션 부트 과정 중에 해석(resolve)된다면, 컨테이너는 서비스에 주입되고, 그 이후의 요청에서도 같은 `Service` 인스턴스가 같은 컨테이너 인스턴스를 계속해서 참조하게 됩니다. 이 방식이 꼭 문제를 일으키는 것은 아니지만, 부트 순서상 나중이나 다른 요청에서 바인딩된 서비스가 누락되는 등의 문제가 될 수 있습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a container resolver closure into the service that always resolves the current container instance: -->
해결 방법으로는, 해당 바인딩을 싱글턴으로 등록하지 않거나, 서비스 객체에 항상 최신 컨테이너를 가져올 수 있는 클로저를 주입하는 것이 있습니다.

```php
use App\Service;
use Illuminate\Container\Container;

$this->app->bind(Service::class, function ($app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```

<!-- The global `app` helper and the `Container::getInstance()` method will always return the latest version of the application container. -->
전역 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너 인스턴스를 반환합니다.

<a name="request-injection"></a>
<!-- ### Request Injection -->
### Request Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire request instance into an object that is bound as a singleton: -->
일반적으로, 애플리케이션 서비스 컨테이너나 HTTP request 인스턴스를 다른 객체의 생성자에 주입하는 것을 피해야 합니다. 예를 들어, 아래 예시에서는 싱글턴으로 바인딩된 객체의 생성자에 전체 request 인스턴스를 주입합니다.

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app['request']);
    });
}
```

<!-- In this example, if the `Service` instance is resolved during the application boot process, the HTTP request will be injected into the service and that same request will be held by the `Service` instance on subsequent requests. Therefore, all headers, input, and query string data will be incorrect, as well as all other request data. -->
이 경우, `Service` 인스턴스가 애플리케이션 부트 과정 중에 해석되면, HTTP request가 서비스 객체에 주입되고, 이후의 모든 요청에서도 같은 `Service` 인스턴스가 동일한(만들어진 시점의) request를 참조하게 됩니다. 이 때문에 헤더, 입력값, 쿼리스트링 등 모든 요청 데이터가 틀릴 수 있습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a request resolver closure into the service that always resolves the current request instance. Or, the most recommended approach is simply to pass the specific request information your object needs to one of the object's methods at runtime: -->
해결 방법으로는, 바인딩을 싱글턴으로 등록하지 않거나, 서비스 객체에 언제나 현재 request 인스턴스를 반환하는 클로저를 주입하는 것입니다. 또는, 가장 추천하는 방식은 필요한 request 정보만 런타임에 객체의 메서드로 전달하는 것입니다.

```php
use App\Service;

$this->app->bind(Service::class, function ($app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function ($app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```

<!-- The global `request` helper will always return the request the application is currently handling and is therefore safe to use within your application. -->
전역 `request` 헬퍼는 현재 애플리케이션에서 처리되는 요청 인스턴스를 항상 반환하므로, 애플리케이션 내에서 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서는 `Illuminate\Http\Request` 인스턴스를 타입힌트해도 괜찮습니다.

<a name="configuration-repository-injection"></a>
<!-- ### Configuration Repository Injection -->
### Configuration Repository Injection

<!-- In general, you should avoid injecting the configuration repository instance into the constructors of other objects. For example, the following binding injects the configuration repository into an object that is bound as a singleton: -->
일반적으로, 설정 리포지토리 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 아래 예시에서는 설정 리포지토리가 싱글턴으로 바인딩된 객체의 생성자에 주입됩니다.

```php
use App\Service;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->singleton(Service::class, function ($app) {
        return new Service($app->make('config'));
    });
}
```

<!-- In this example, if the configuration values change between requests, that service will not have access to the new values because it's depending on the original repository instance. -->
이렇게 하면, 요청 사이에 설정 값이 변경되더라도, 해당 서비스는 최초(바인딩 시점)의 리포지토리만 참조하게 되어 새로운 값을 접근할 수 없게 됩니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a configuration repository resolver closure to the class: -->
해결 방법으로는, 해당 바인딩을 싱글턴으로 등록하지 않거나, 항상 최신 리포지토리를 반환하는 클로저를 클래스에 주입하는 것입니다.

```php
use App\Service;
use Illuminate\Container\Container;

$this->app->bind(Service::class, function ($app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```

<!-- The global `config` will always return the latest version of the configuration repository and is therefore safe to use within your application. -->
전역 `config` 헬퍼는 항상 최신 설정 리포지토리를 반환하므로, 애플리케이션 내에서 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
<!-- ### Managing Memory Leaks -->
### Managing Memory Leaks

<!-- Remember, Octane keeps your application in memory between requests; therefore, adding data to a statically maintained array will result in a memory leak. For example, the following controller has a memory leak since each request to the application will continue to add data to the static `$data` array: -->
Octane은 애플리케이션을 요청 사이에서도 메모리에 보관하므로, 정적(static) 배열에 데이터를 추가하면 메모리 누수가 발생할 수 있습니다. 예를 들어 아래 컨트롤러 코드는 static `$data` 배열에 값을 계속 추가하여 요청이 올 때마다 메모리가 누적됩니다.

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return void
 */
public function index(Request $request)
{
    Service::$data[] = Str::random(10);

    // ...
}
```

<!-- While building your application, you should take special care to avoid creating these types of memory leaks. It is recommended that you monitor your application's memory usage during local development to ensure you are not introducing new memory leaks into your application. -->
애플리케이션을 개발할 때 이러한 형태의 메모리 누수를 피하도록 주의해야 합니다. 로컬 개발 단계에서 애플리케이션의 메모리 사용량을 주기적으로 모니터링하여, 새로운 메모리 누수가 없는지 확인하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
<!-- ## Concurrent Tasks -->
## Concurrent Tasks

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may execute operations concurrently via light-weight background tasks. You may accomplish this using Octane's `concurrently` method. You may combine this method with PHP array destructuring to retrieve the results of each operation: -->
Swoole을 사용할 때는 경량의 백그라운드 태스크로 작업을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메서드를 활용하면 됩니다. PHP 배열 디스트럭처링 문법과 함께 사용하면 각 작업 결과를 손쉽게 받을 수 있습니다.

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
Octane에서 동시 처리하는 태스크는 Swoole의 "태스크 워커"에서 실행되며, 들어오는 요청과는 완전히 분리된 별도의 프로세스에서 처리됩니다. 사용할 수 있는 태스크 워커의 개수는 `octane:start` 명령의 `--task-workers` 옵션으로 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<!-- When invoking the `concurrently` method, you should not provide more than 1024 tasks due to limitations imposed by Swoole's task system. -->
`concurrently` 메서드를 호출할 때는 Swoole 태스크 시스템의 제한으로 인해, 1024개를 초과하는 태스크를 한 번에 실행하면 안 됩니다.

<a name="ticks-and-intervals"></a>
<!-- ## Ticks & Intervals -->
## Ticks & Intervals

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may register "tick" operations that will be executed every specified number of seconds. You may register "tick" callbacks via the `tick` method. The first argument provided to the `tick` method should be a string that represents the name of the ticker. The second argument should be a callable that will be invoked at the specified interval. -->
Swoole 사용 시, 지정한 초마다 반복적으로 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드를 사용해 "tick" 콜백을 등록합니다. `tick` 메서드의 첫 번째 인자는 티커의 이름을 나타내는 문자열, 두 번째 인자는 지정된 간격마다 실행할 콜러블입니다.

<!-- In this example, we will register a closure to be invoked every 10 seconds. Typically, the `tick` method should be called within the `boot` method of one of your application's service providers: -->
아래 예시는 10초마다 실행될 클로저를 등록하는 방식입니다. 보통 `tick` 메서드는 애플리케이션 서비스 프로바이더의 `boot` 메서드 안에서 호출하는 것이 적합합니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

<!-- Using the `immediate` method, you may instruct Octane to immediately invoke the tick callback when the Octane server initially boots, and every N seconds thereafter: -->
`immediate` 메서드를 사용하면 Octane 서버가 처음 부팅할 때도 tick 콜백을 즉시 실행하고, 이후에도 지정 간격마다 계속 실행합니다.

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
Swoole을 사용할 경우, Octane 캐시 드라이버를 사용할 수 있습니다. 이 캐시는 초당 200만 건까지 읽기∙쓰기가 가능할 정도로 매우 빠릅니다. 캐싱 계층에서 극도의 속도가 필요한 애플리케이션에 적합합니다.

<!-- This cache driver is powered by [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). All data stored in the cache is available to all workers on the server. However, the cached data will be flushed when the server is restarted: -->
이 캐시는 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)에 의해 제공되며, 서버 내 모든 워커에서 데이터에 접근 가능합니다. 하지만, 서버를 재시작하면 캐시된 모든 데이터가 초기화됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에서 허용되는 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
<!-- ### Cache Intervals -->
### Cache Intervals

<!-- In addition to the typical methods provided by Laravel's cache system, the Octane cache driver features interval based caches. These caches are automatically refreshed at the specified interval and should be registered within the `boot` method of one of your application's service providers. For example, the following cache will be refreshed every five seconds: -->
Laravel의 일반적인 캐시 메서드 외에도, Octane 캐시는 인터벌 기반 캐시 기능을 제공합니다. 이 캐시는 설정한 주기마다 자동으로 새로고침되며, 서비스 프로바이더의 `boot` 메서드 안에서 등록하면 됩니다. 아래 예시는 5초마다 갱신되는 캐시입니다.

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
Swoole을 사용할 때, 임의의 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 사용할 수 있습니다. Swoole 테이블은 초고속 처리 성능을 제공하며, 서버 내 모든 워커에서 데이터를 읽고 쓸 수 있습니다. 단, 서버가 재시작되면 테이블 데이터는 모두 사라집니다.

<!-- Tables should be defined within the `tables` configuration array of your application's `octane` configuration file. An example table that allows a maximum of 1000 rows is already configured for you. The maximum size of string columns may be configured by specifying the column size after the column type as seen below: -->
테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에서 정의할 수 있습니다. 최대 1000개의 행을 허용하는 샘플 테이블이 기본으로 설정되어 있습니다. 문자열 컬럼의 크기는 아래와 같이 타입 뒤에 크기 값을 지정해 관리할 수 있습니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

<!-- To access a table, you may use the `Octane::table` method: -->
테이블에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다.

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
