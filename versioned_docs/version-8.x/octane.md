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
[Laravel Octane](https://github.com/laravel/octane)는 [Open Swoole](https://swoole.co.uk), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 같은 고성능 애플리케이션 서버를 활용하여 애플리케이션의 성능을 획기적으로 향상시켜줍니다. Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 상주시켜 극도로 빠른 속도로 요청을 처리합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Octane may be installed via the Composer package manager: -->
Octane은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

```bash
composer require laravel/octane
```

<!-- After installing Octane, you may execute the `octane:install` Artisan command, which will install Octane's configuration file into your application: -->
Octane 설치 후에는 `octane:install` 아티즌 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다.

```bash
php artisan octane:install
```

<a name="server-prerequisites"></a>
<!-- ## Server Prerequisites -->
## Server Prerequisites

> [!NOTE]
> Laravel Octane을 사용하려면 [PHP 8.0+](https://php.net/releases/) 버전이 필요합니다.

<a name="roadrunner"></a>
<!-- ### RoadRunner -->
### RoadRunner

<!-- [RoadRunner](https://roadrunner.dev) is powered by the RoadRunner binary, which is built using Go. The first time you start a RoadRunner based Octane server, Octane will offer to download and install the RoadRunner binary for you. -->
[RoadRunner](https://roadrunner.dev)는 Go로 빌드된 RoadRunner 바이너리를 기반으로 동작합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane은 RoadRunner 바이너리를 자동으로 다운로드 및 설치해줍니다.

<a name="roadrunner-via-laravel-sail"></a>
<!-- #### RoadRunner Via Laravel Sail -->
#### RoadRunner Via Laravel Sail

<!-- If you plan to develop your application using [Laravel Sail](/docs/8.x/sail), you should run the following commands to install Octane and RoadRunner: -->
[Laravel Sail](/docs/8.x/sail)로 애플리케이션을 개발하려면, 아래 명령어를 실행하여 Octane과 RoadRunner를 설치해야 합니다.

```bash
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner
```

<!-- Next, you should start a Sail shell and use the `rr` executable to retrieve the latest Linux based build of the RoadRunner binary: -->
그 다음, Sail 셸을 실행하고 `rr` 실행 파일을 이용하여 리눅스용 RoadRunner 바이너리를 최신 버전으로 받아야 합니다.

```bash
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```

<!-- After installing the RoadRunner binary, you may exit your Sail shell session. You will now need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
RoadRunner 바이너리 설치가 끝나면 Sail 셸 세션에서 나올 수 있습니다. 이제 `supervisor.conf` 파일을 수정하여 애플리케이션이 동작하도록 설정해줘야 합니다. 먼저, `sail:publish` 아티즌 명령어를 실행하세요.

```bash
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
그리고 애플리케이션의 `docker/supervisord.conf` 파일 내 `command` 지시어를 아래와 같이 수정하여, Sail이 Octane으로 애플리케이션을 실행하도록 변경하세요.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port=8000
```

<!-- Finally, ensure the `rr` binary is executable and build your Sail images: -->
마지막으로, `rr` 바이너리가 실행 가능하도록 권한을 부여하고, Sail 이미지를 빌드합니다.

```bash
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
<!-- ### Swoole -->
### Swoole

<!-- If you plan to use the Swoole application server to serve your Laravel Octane application, you must install the Swoole PHP extension. Typically, this can be done via PECL: -->
Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장(extension)을 설치해야 합니다. 일반적으로 PECL을 통해 간단히 설치할 수 있습니다.

```bash
pecl install swoole
```

<a name="swoole-via-laravel-sail"></a>
<!-- #### Swoole Via Laravel Sail -->
#### Swoole Via Laravel Sail

> [!NOTE]
> Octane 애플리케이션을 Sail에서 실행하기 전에 꼭 최신 버전의 Laravel Sail을 사용하고, 프로젝트 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행해주시기 바랍니다.

<!-- Alternatively, you may develop your Swoole based Octane application using [Laravel Sail](/docs/8.x/sail), the official Docker based development environment for Laravel. Laravel Sail includes the Swoole extension by default. However, you will still need to adjust the `supervisor.conf` file used by Sail to keep your application running. To get started, execute the `sail:publish` Artisan command: -->
[Laravel Sail](/docs/8.x/sail)로 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail은 기본적으로 Swoole 확장을 포함하고 있습니다. 하지만, Sail로 애플리케이션을 계속 실행되게 하려면 `supervisor.conf` 파일을 수정해야 합니다. 먼저, 다음 명령어로 `sail:publish` 아티즌 명령어를 실행하세요.

```bash
./vendor/bin/sail artisan sail:publish
```

<!-- Next, update the `command` directive of your application's `docker/supervisord.conf` file so that Sail serves your application using Octane instead of the PHP development server: -->
그리고 `docker/supervisord.conf` 파일의 `command` 지시어를 아래와 같이 Octane이 애플리케이션을 제공하게끔 수정합니다.

```ini
command=/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port=80
```

<!-- Finally, build your Sail images: -->
마지막으로 Sail 이미지를 빌드해줍니다.

```bash
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
<!-- #### Swoole Configuration -->
#### Swoole Configuration

<!-- Swoole supports a few additional configuration options that you may add to your `octane` configuration file if necessary. Because they rarely need to be modified, these options are not included in the default configuration file: -->
Swoole은 추가적으로 몇 가지 설정 옵션들을 제공합니다. 필요하다면 이 옵션들을 `octane` 설정 파일에 추가할 수 있습니다. 보통은 변경할 일이 드물기 때문에, 기본 설정 파일에는 포함되어 있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
];
```

<a name="serving-your-application"></a>
<!-- ## Serving Your Application -->
## Serving Your Application

<!-- The Octane server can be started via the `octane:start` Artisan command. By default, this command will utilize the server specified by the `server` configuration option of your application's `octane` configuration file: -->
Octane 서버는 `octane:start` 아티즌 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 설정 옵션에서 지정한 서버를 사용합니다.

```bash
php artisan octane:start
```

<!-- By default, Octane will start the server on port 8000, so you may access your application in a web browser via `http://localhost:8000`. -->
기본적으로 Octane은 8000 포트에서 서버를 실행하므로, 웹 브라우저에서 `http://localhost:8000`으로 접속하면 애플리케이션을 확인할 수 있습니다.

<a name="serving-your-application-via-https"></a>
<!-- ### Serving Your Application Via HTTPS -->
### Serving Your Application Via HTTPS

<!-- By default, applications running via Octane generate links prefixed with `http://`. The `OCTANE_HTTPS` environment variable, used within your application's `config/octane.php` configuration file, can be set to `true` when serving your application via HTTPS. When this configuration value is set to `true`, Octane will instruct Laravel to prefix all generated links with `https://`: -->
Octane으로 실행되는 애플리케이션은 기본적으로 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일에서 사용되는 `OCTANE_HTTPS` 환경 변수는 HTTPS로 서비스할 때 `true`로 설정할 수 있습니다. 이 설정값이 `true`로 지정되면, Octane은 Laravel에게 생성되는 모든 링크에 `https://` 접두사를 붙이도록 지시합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
<!-- ### Serving Your Application Via Nginx -->
### Serving Your Application Via Nginx

> [!TIP]
> 별도의 서버 구성을 직접 관리하는 것이 익숙하지 않거나, Octane 애플리케이션 운영에 필요한 다양한 서비스를 하나하나 설정하는 게 어렵다면 [Laravel Forge](https://forge.laravel.com)를 참고하세요.

<!-- In production environments, you should serve your Octane application behind a traditional web server such as a Nginx or Apache. Doing so will allow the web server to serve your static assets such as images and stylesheets, as well as manage your SSL certificate termination. -->
실제 운영 환경(프로덕션)에서는 반드시 Octane 애플리케이션을 Nginx 혹은 Apache 같은 일반적인 웹 서버 뒤에서 서비스하는 것이 좋습니다. 이렇게 하면 이미지, 스타일시트 같은 정적 자산들은 웹 서버가 직접 제공하고, SSL 인증서 관리 등도 쉽게 할 수 있습니다.

<!-- In the Nginx configuration example below, Nginx will serve the site's static assets and proxy requests to the Octane server that is running on port 8000: -->
아래 Nginx 설정 예시에서는 Nginx가 사이트의 정적 파일들은 직접 서빙하고, 그 외 요청은 8000 포트에서 실행 중인 Octane 서버로 프록시합니다.

```conf
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
Octane 서버는 최초 시작 시 애플리케이션을 메모리에 적재하기 때문에, 애플리케이션 파일이 변경되어도 웹 브라우저를 새로고침해서 바로 반영되지 않습니다. 예를 들어, `routes/web.php`에 새로운 라우트를 추가해도 서버를 재시작하기 전에는 반영되지 않습니다. 편의상 Octane에 `--watch` 옵션을 사용해 파일 변경이 발생할 때마다 자동으로 서버를 재시작하게 할 수 있습니다.

```bash
php artisan octane:start --watch
```

<!-- Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project:library: -->
이 기능을 사용하려면, 먼저 로컬 개발 환경에 [Node](https://nodejs.org)를 설치해야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리도 설치해야 합니다.

```bash
npm install --save-dev chokidar
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/octane.php` configuration file. -->
어떤 디렉터리나 파일들을 감시할지 여부는 애플리케이션의 `config/octane.php` 파일 내 `watch` 설정 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
<!-- ### Specifying The Worker Count -->
### Specifying The Worker Count

<!-- By default, Octane will start an application request worker for each CPU core provided by your machine. These workers will then be used to serve incoming HTTP requests as they enter your application. You may manually specify how many workers you would like to start using the `--workers` option when invoking the `octane:start` command: -->
기본적으로 Octane은 머신에 탑재된 각 CPU 코어마다 하나씩 애플리케이션 요청 워커를 시작합니다. 이 워커들은 들어오는 HTTP 요청을 처리하게 됩니다. 만약 원하는 워커 수를 수동으로 지정하고자 한다면, `octane:start` 명령에 `--workers` 옵션을 사용할 수 있습니다.

```bash
php artisan octane:start --workers=4
```

<!-- If you are using the Swoole application server, you may also specify how many ["task workers"](#concurrent-tasks) you wish to start: -->
Swoole 애플리케이션 서버를 사용하는 경우, ["task workers"](#concurrent-tasks)를 몇 개 실행할지도 추가로 지정할 수 있습니다.

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
<!-- ### Specifying The Max Request Count -->
### Specifying The Max Request Count

<!-- To help prevent stray memory leaks, Octane can gracefully restart a worker once it has handled a given number of requests. To instruct Octane to do this, you may use the `--max-requests` option: -->
메모리 누수 방지를 위해 Octane은 워커가 정해진 수의 요청을 처리한 뒤 정상적으로 재시작할 수 있도록 지원합니다. 이를 위해 `--max-requests` 옵션을 사용할 수 있습니다.

```bash
php artisan octane:start --max-requests=250
```

<a name="reloading-the-workers"></a>
<!-- ### Reloading The Workers -->
### Reloading The Workers

<!-- You may gracefully restart the Octane server's application workers using the `octane:reload` command. Typically, this should be done after deployment so that your newly deployed code is loaded into memory and is used to serve to subsequent requests: -->
Octane 서버의 애플리케이션 워커는 `octane:reload` 명령으로 정상적으로 재시작할 수 있습니다. 주로 새 코드 배포 후 새롭게 배포된 코드가 메모리에 반영되도록 하고자 할 때 활용합니다.

```bash
php artisan octane:reload
```

<a name="stopping-the-server"></a>
<!-- ### Stopping The Server -->
### Stopping The Server

<!-- You may stop the Octane server using the `octane:stop` Artisan command: -->
Octane 서버는 `octane:stop` 아티즌 명령어로 중지할 수 있습니다.

```bash
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
<!-- #### Checking The Server Status -->
#### Checking The Server Status

<!-- You may check the current status of the Octane server using the `octane:status` Artisan command: -->
Octane 서버의 현재 상태는 `octane:status` 아티즌 명령어로 확인할 수 있습니다.

```bash
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
<!-- ## Dependency Injection & Octane -->
## Dependency Injection & Octane

<!-- Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused. -->
Octane은 애플리케이션을 한 번만 부팅하고, 그 상태를 계속 메모리에 남겨두고 요청을 처리합니다. 이런 특성 때문에 애플리케이션을 개발할 때 몇 가지 주의해야 할 점이 있습니다. 예를 들어, 서비스 프로바이더의 `register`와 `boot` 메서드는 요청 워커가 처음 부팅될 때 한 번만 실행됩니다. 이후의 요청에서는 같은 애플리케이션 인스턴스가 재사용됩니다.

<!-- In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a  stale version of the container or request on subsequent requests. -->
따라서, 서비스 컨테이너나 리퀘스트(Request)를 객체의 생성자(Constructor)에 주입한다면, 이후 요청에서는 오래된 컨테이너나 리퀘스트 인스턴스가 사용될 수 있습니다.

<!-- Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane. -->
Octane은 프레임워크의 1차적인 상태는 요청마다 자동으로 초기화합니다. 하지만, 여러분의 애플리케이션이 생성하는 전역 상태까지 항상 초기화할 수는 없기 때문에 Octane 친화적으로 코드를 작성해야 합니다. 아래는 Octane 사용 시 주로 문제가 되는 대표적인 상황들입니다.

<a name="container-injection"></a>
<!-- ### Container Injection -->
### Container Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton: -->
서비스 컨테이너나 HTTP 리퀘스트 인스턴스를 다른 객체의 생성자에서 직접 주입하는 일은 일반적으로 피해야 합니다. 아래 예시는 전체 애플리케이션 서비스 컨테이너를 싱글턴으로 바인딩하는 상황입니다.

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
이 예시에서 만약 `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성된다면, 컨테이너가 서비스 객체에 주입되고 이후 요청에서도 같은 `Service` 인스턴스가 계속 같은 컨테이너 인스턴스를 사용하게 됩니다. 이 현상은 애플리케이션에 따라 문제가 되지 않을 수 있지만, 경우에 따라 컨테이너에 나중에 추가된 바인딩이나 요청에 따라 달라진 바인딩을 사용할 수 없는 결과로 이어질 수 있습니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a container resolver closure into the service that always resolves the current container instance: -->
대안으로는, 이 바인딩을 싱글턴(singleton) 대신 일반 바인드로 변경하거나, 컨테이너를 항상 새롭게 가져오는 클로저(익명 함수)를 Service에 주입하는 방법이 있습니다.

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
글로벌 `app` 헬퍼나 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
<!-- ### Request Injection -->
### Request Injection

<!-- In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire request instance into an object that is bound as a singleton: -->
서비스 컨테이너 또는 HTTP 리퀘스트 인스턴스를 다른 객체의 생성자에서 직접 주입하는 것은 일반적으로 피해야 합니다. 아래 예시는 요청 인스턴스 전체를 싱글턴으로 객체에 주입하는 코드입니다.

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
이 경우 만약 부팅 과정에서 `Service` 인스턴스가 생성된다면, 그 시점의 HTTP 리퀘스트가 서비스에 주입되고, 이후 모든 요청에서도 같은 `Service` 인스턴스가 동일한(오래된) 리퀘스트 정보를 사용하게 됩니다. 그 결과, 헤더, 입력값, 쿼리 스트링 등 모든 요청 데이터가 올바르지 않게 됩니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a request resolver closure into the service that always resolves the current request instance. Or, the most recommended approach is simply to pass the specific request information your object needs to one of the object's methods at runtime: -->
해결책으로는 싱글턴 바인딩 대신 일반 바인드로 변경하거나, 항상 최신 리퀘스트를 가져오는 클로저를 주입하는 방법이 있습니다. 혹은 가장 추천되는 방법은, 그 객체가 실제로 필요한 데이터만 런타임 시 객체의 메서드로 넘기는 것입니다.

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
글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청 객체를 반환하므로 애플리케이션에서 안전하게 사용할 수 있습니다.

> [!NOTE]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 타입힌트는 사용해도 무방합니다.

<a name="configuration-repository-injection"></a>
<!-- ### Configuration Repository Injection -->
### Configuration Repository Injection

<!-- In general, you should avoid injecting the configuration repository instance into the constructors of other objects. For example, the following binding injects the configuration repository into an object that is bound as a singleton: -->
설정 저장소 인스턴스를 객체 생성자에 주입하는 것도 일반적으로 피해야 합니다. 예를 들어, 아래의 경우 설정 저장소가 싱글턴으로 객체에 주입됩니다.

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
이렇게 하면 요청 사이에서 설정 값이 변경되더라도, Service 인스턴스에서는 최초 저장소 인스턴스에만 접근하게 됩니다.

<!-- As a work-around, you could either stop registering the binding as a singleton, or you could inject a configuration repository resolver closure to the class: -->
이 문제를 해결하려면, 싱글턴 대신 일반 바인딩을 사용하거나, 항상 최신 설정 저장소를 가져오는 클로저를 객체에 주입할 수 있습니다.

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
글로벌 `config` 헬퍼는 항상 최신 설정 저장소 인스턴스를 반환하므로 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
<!-- ### Managing Memory Leaks -->
### Managing Memory Leaks

<!-- Remember, Octane keeps your application in memory between requests; therefore, adding data to a statically maintained array will result in a memory leak. For example, the following controller has a memory leak since each request to the application will continue to add data to the static `$data` array: -->
Octane은 애플리케이션을 여러 요청 사이에 메모리에 유지하므로, 정적으로 관리되는 배열 등에 데이터를 누적시키면 메모리 누수가 발생합니다. 다음 예시는 요청마다 static `$data` 배열에 데이터가 계속 쌓이기 때문에 메모리 누수가 생기는 컨트롤러 코드입니다.

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
애플리케이션을 개발하면서 이런 종류의 메모리 누수가 발생하지 않도록 특히 조심해야 합니다. 로컬 개발 과정에서 애플리케이션의 메모리 사용량을 모니터링하여 새로 유입된 누수가 없는지 확인하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
<!-- ## Concurrent Tasks -->
## Concurrent Tasks

> [!NOTE]
> 이 기능을 사용하려면 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may execute operations concurrently via light-weight background tasks. You may accomplish this using Octane's `concurrently` method. You may combine this method with PHP array destructuring to retrieve the results of each operation: -->
Swoole을 사용할 때, 경량의 백그라운드 작업을 통해 여러 동작을 동시에 처리할 수 있습니다. Octane의 `concurrently` 메서드를 사용해 이를 구현할 수 있고, PHP의 배열 구조 분해 기능과 결합해서 각 작업의 결과를 받아올 수 있습니다.

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
Octane에서 처리되는 동시 작업은 Swoole의 "태스크 워커"가 이용되며, 들어오는 요청과는 완전히 다른 프로세스에서 실행됩니다. 동시에 동작하는 태스크 워커의 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 정할 수 있습니다.

```bash
php artisan octane:start --workers=4 --task-workers=6
```

<a name="ticks-and-intervals"></a>
<!-- ## Ticks & Intervals -->
## Ticks & Intervals

> [!NOTE]
> 이 기능을 사용하려면 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may register "tick" operations that will be executed every specified number of seconds. You may register "tick" callbacks via the `tick` method. The first argument provided to the `tick` method should be a string that represents the name of the ticker. The second argument should be a callable that will be invoked at the specified interval. -->
Swoole을 사용하는 경우, 일정 시간마다 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드를 이용하면 "tick" 콜백을 등록할 수 있는데, `tick` 메서드의 첫 번째 인자에는 틱커의 이름을 나타내는 문자열을, 두 번째 인자에는 지정된 간격마다 호출될 콜러블을 넣습니다.

<!-- In this example, we will register a closure to be invoked every 10 seconds. Typically, the `tick` method should be called within the `boot` method of one of your application's service providers: -->
아래 예시는 10초마다 한 번씩 클로저가 실행되도록 등록하는 방식입니다. 주로 애플리케이션의 서비스 프로바이더 `boot` 메서드 내에서 `tick` 메서드를 호출하게 됩니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10);
```

<!-- Using the `immediate` method, you may instruct Octane to immediately invoke the tick callback when the Octane server initially boots, and every N seconds thereafter: -->
`immediate` 메서드를 사용하면, Octane 서버가 처음 부팅될 때 즉시 틱 콜백이 실행되고 이후에는 N초마다 계속 반복됩니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
        ->seconds(10)
        ->immediate();
```

<a name="the-octane-cache"></a>
<!-- ## The Octane Cache -->
## The Octane Cache

> [!NOTE]
> 이 기능을 사용하려면 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may leverage the Octane cache driver, which provides read and write speeds of up to 2 million operations per second. Therefore, this cache driver is an excellent choice for applications that need extreme read / write speeds from their caching layer. -->
Swoole을 사용할 때는 Octane 캐시 드라이버를 활용할 수 있습니다. Octane 캐시는 초당 최대 2백만 건 이상의 읽기/쓰기 작업이 가능한 매우 빠른 캐시 드라이버로, 극한의 성능이 필요한 상황에 적합합니다.

<!-- This cache driver is powered by [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). All data stored in the cache is available to all workers on the server. However, the cached data will be flushed when the server is restarted: -->
이 캐시 드라이버는 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table) 위에서 동작합니다. 저장된 데이터는 서버 내 모든 워커가 접근할 수 있지만, 서버가 재시작되면 캐시된 데이터는 모두 사라집니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!TIP]
> Octane 캐시에 저장할 수 있는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
<!-- ### Cache Intervals -->
### Cache Intervals

<!-- In addition to the typical methods provided by Laravel's cache system, the Octane cache driver features interval based caches. These caches are automatically refreshed at the specified interval and should be registered within the `boot` method of one of your application's service providers. For example, the following cache will be refreshed every five seconds: -->
Laravel의 일반적인 캐시 시스템 메서드 외에도, Octane 캐시 드라이버는 주기적으로 자동 갱신되는 인터벌 기반 캐시를 제공합니다. 이런 캐시는 지정한 인터벌마다 자동으로 새롭게 값이 반환되며, 주로 서비스 프로바이더의 `boot` 메서드 안에서 등록합니다. 다음의 예는 5초마다 캐시가 새롭게 갱신되는 방식입니다.

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5)
```

<a name="tables"></a>
<!-- ## Tables -->
## Tables

> [!NOTE]
> 이 기능을 사용하려면 [Swoole](#swoole)이 필요합니다.

<!-- When using Swoole, you may define and interact with your own arbitrary [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table). Swoole tables provide extreme performance throughput and the data in these tables can be accessed by all workers on the server. However, the data within them will be lost when the server is restarted. -->
Swoole을 사용할 때는 직접 임의의 [Swoole tables](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 상호작용할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 제공하며, 서버 내 모든 워커에서 이 데이터를 읽고 쓸 수 있습니다. 단, 서버가 재시작되면 테이블 내 데이터는 모두 삭제됩니다.

<!-- Tables should be defined within the `tables` configuration array of your application's `octane` configuration file. An example table that allows a maximum of 1000 rows is already configured for you. The maximum size of string columns may be configured by specifying the column size after the column type as seen below: -->
테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에 정의해야 합니다. 1000개 행까지 허용하는 예시 테이블이 기본적으로 설정되어 있습니다. 문자열 컬럼의 최대 길이 등은 컬럼 타입명 뒤에 크기를 지정해서 설정할 수 있습니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

<!-- To access a table, you may use the `Octane::table` method: -->
테이블에 접근하려면 `Octane::table` 메서드를 사용하세요.

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!NOTE]
> Swoole 테이블에서 지원하는 컬럼 타입은 `string`, `int`, `float`입니다.
