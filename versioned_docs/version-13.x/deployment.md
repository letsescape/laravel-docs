<!-- # Deployment -->
# Deployment

- [Introduction](#introduction)
- [Server Requirements](#server-requirements)
- [Server Configuration](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [Directory Permissions](#directory-permissions)
- [Optimization](#optimization)
    - [Caching Configuration](#optimizing-configuration-loading)
    - [Caching Events](#caching-events)
    - [Caching Routes](#optimizing-route-loading)
    - [Caching Views](#optimizing-view-loading)
- [Reloading Services](#reloading-services)
- [Debug Mode](#debug-mode)
- [The Health Route](#the-health-route)
- [Deploying With Laravel Cloud or Forge](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you're ready to deploy your Laravel application to production, there are some important things you can do to make sure your application is running as efficiently as possible. In this document, we'll cover some great starting points for making sure your Laravel application is deployed properly. -->
Laravel 애플리케이션을 프로덕션에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 실행되도록 하기 위해 수행할 수 있는 몇 가지 중요한 작업이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 좋은 시작점을 다룹니다.

<a name="server-requirements"></a>
<!-- ## Server Requirements -->
## Server Requirements

<!-- The Laravel framework has a few system requirements. You should ensure that your web server has the following minimum PHP version and extensions: -->
Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버에 다음의 최소 PHP 버전과 확장이 있는지 확인해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- PHP >= 8.3
- Ctype PHP Extension
- cURL PHP Extension
- DOM PHP Extension
- Fileinfo PHP Extension
- Filter PHP Extension
- Hash PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PCRE PHP Extension
- PDO PHP Extension
- Session PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension
-->
- PHP >= 8.3
- Ctype PHP Extension
- cURL PHP Extension
- DOM PHP Extension
- Fileinfo PHP Extension
- Filter PHP Extension
- Hash PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PCRE PHP Extension
- PDO PHP Extension
- Session PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension

<!-- </div> -->
</div>

<a name="server-configuration"></a>
<!-- ## Server Configuration -->
## Server Configuration

<a name="nginx"></a>
<!-- ### Nginx -->
### Nginx

<!-- If you are deploying your application to a server that is running Nginx, you may use the following configuration file as a starting point for configuring your web server. Most likely, this file will need to be customized depending on your server's configuration. **If you would like assistance in managing your server, consider using a fully-managed Laravel platform like [Laravel Cloud](https://cloud.laravel.com).** -->
Nginx가 실행 중인 서버에 애플리케이션을 배포하는 경우, 다음 설정 파일을 웹 서버 설정의 출발점으로 사용할 수 있습니다. 대부분의 경우 이 파일은 서버 설정에 맞게 수정해야 합니다. **서버 관리에 도움이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 Laravel 플랫폼 사용을 고려해 보십시오.**

<!-- Please ensure, like the configuration below, your web server directs all requests to your application's `public/index.php` file. You should never attempt to move the `index.php` file to your project's root, as serving the application from the project root will expose many sensitive configuration files to the public Internet: -->
아래 설정처럼 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하는지 확인하십시오. `index.php` 파일을 프로젝트 루트로 옮기려고 해서는 절대 안 됩니다. 프로젝트 루트에서 애플리케이션을 제공하면 민감한 설정 파일이 공개 인터넷에 노출됩니다.

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="frankenphp"></a>
<!-- ### FrankenPHP -->
### FrankenPHP

<!-- [FrankenPHP](https://frankenphp.dev/) may also be used to serve your Laravel applications. FrankenPHP is a modern PHP application server written in Go. To serve a Laravel PHP application using FrankenPHP, you may simply invoke its `php-server` command: -->
[FrankenPHP](https://frankenphp.dev/)도 Laravel 애플리케이션을 제공하는 데 사용할 수 있습니다. FrankenPHP는 Go로 작성된 현대적인 PHP 애플리케이션 서버입니다. FrankenPHP를 사용하여 Laravel PHP 애플리케이션을 제공하려면 `php-server` 명령어를 실행하면 됩니다.

```shell
frankenphp php-server -r public/
```

<!-- To take advantage of more powerful features supported by FrankenPHP, such as its [Laravel Octane](/docs/13.x/octane) integration, HTTP/3, modern compression, or the ability to package Laravel applications as standalone binaries, please consult FrankenPHP's [Laravel documentation](https://frankenphp.dev/docs/laravel/). -->
[Laravel Octane](/docs/13.x/octane) 통합, HTTP/3, 현대적인 압축, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능 등 FrankenPHP가 지원하는 더 강력한 기능을 활용하려면 FrankenPHP의 [Laravel documentation](https://frankenphp.dev/docs/laravel/)를 참고하십시오.

<a name="directory-permissions"></a>
<!-- ### Directory Permissions -->
### Directory Permissions

<!-- Laravel will need to write to the `bootstrap/cache` and `storage` directories, so you should ensure the web server process owner has permission to write to these directories. -->
Laravel은 `bootstrap/cache` 및 `storage` 디렉터리에 파일을 쓸 수 있어야 하므로, 웹 서버 프로세스 소유자에게 이 디렉터리에 쓸 권한이 있는지 확인해야 합니다.

<a name="optimization"></a>
<!-- ## Optimization -->
## Optimization

<!-- When deploying your application to production, there are a variety of files that should be cached, including your configuration, events, routes, and views. Laravel provides a single, convenient `optimize` Artisan command that will cache all of these files. This command should typically be invoked as part of your application's deployment process: -->
애플리케이션을 프로덕션에 배포할 때는 설정, 이벤트, 라우트, 뷰를 포함한 여러 파일을 캐싱해야 합니다. Laravel은 이러한 파일을 모두 캐싱하는 하나의 편리한 `optimize` Artisan 명령어를 제공합니다. 일반적으로 이 명령어는 애플리케이션 배포 과정의 일부로 실행해야 합니다.

```shell
php artisan optimize
```

<!-- The `optimize:clear` method may be used to remove all of the cache files generated by the `optimize` command as well as all keys in the default cache driver: -->
`optimize:clear` 메서드는 `optimize` 명령어가 생성한 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거하는 데 사용할 수 있습니다.

```shell
php artisan optimize:clear
```

<!-- In the following documentation, we will discuss each of the granular optimization commands that are executed by the `optimize` command. -->
다음 문서에서는 `optimize` 명령어가 실행하는 각각의 세부 최적화 명령어를 살펴봅니다.

<a name="optimizing-configuration-loading"></a>
<!-- ### Caching Configuration -->
### Caching Configuration

<!-- When deploying your application to production, you should make sure that you run the `config:cache` Artisan command during your deployment process: -->
애플리케이션을 프로덕션에 배포할 때는 배포 과정에서 `config:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan config:cache
```

<!-- This command will combine all of Laravel's configuration files into a single, cached file, which greatly reduces the number of trips the framework must make to the filesystem when loading your configuration values. -->
이 명령어는 Laravel의 모든 설정 파일을 하나의 캐시된 파일로 결합합니다. 이를 통해 설정 값을 로드할 때 프레임워크가 파일 시스템에 접근해야 하는 횟수가 크게 줄어듭니다.

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, `env` 함수는 설정 파일 안에서만 호출해야 합니다. 설정이 캐싱되면 `.env` 파일은 로드되지 않으며, `.env` 변수에 대한 모든 `env` 함수 호출은 `null`을 반환합니다.

<a name="caching-events"></a>
<!-- ### Caching Events -->
### Caching Events

<!-- You should cache your application's auto-discovered event to listener mappings during your deployment process. This can be accomplished by invoking the `event:cache` Artisan command during deployment: -->
배포 과정에서 애플리케이션의 자동 감지된 이벤트와 리스너 매핑을 캐싱해야 합니다. 배포 중 `event:cache` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
<!-- ### Caching Routes -->
### Caching Routes

<!-- If you are building a large application with many routes, you should make sure that you are running the `route:cache` Artisan command during your deployment process: -->
많은 라우트를 가진 대규모 애플리케이션을 빌드하고 있다면, 배포 과정에서 `route:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan route:cache
```

<!-- This command reduces all of your route registrations into a single method call within a cached file, improving the performance of route registration when registering hundreds of routes. -->
이 명령어는 모든 라우트 등록을 캐시된 파일 안의 단일 메서드 호출로 줄여, 수백 개의 라우트를 등록할 때 라우트 등록 성능을 향상합니다.

<a name="optimizing-view-loading"></a>
<!-- ### Caching Views -->
### Caching Views

<!-- When deploying your application to production, you should make sure that you run the `view:cache` Artisan command during your deployment process: -->
애플리케이션을 프로덕션에 배포할 때는 배포 과정에서 `view:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan view:cache
```

<!-- This command precompiles all your Blade views so they are not compiled on demand, improving the performance of each request that returns a view. -->
이 명령어는 모든 Blade 뷰를 미리 컴파일하여 요청 시점에 컴파일되지 않도록 하며, 뷰를 반환하는 각 요청의 성능을 향상합니다.

<a name="reloading-services"></a>
<!-- ## Reloading Services -->
## Reloading Services

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com)에 배포하는 경우 모든 서비스의 중단 없는 다시 로드가 자동으로 처리되므로 `reload` 명령어를 사용할 필요가 없습니다.

<!-- After deploying a new version of your application, any long-running services such as queue workers, Laravel Reverb, or Laravel Octane should be reloaded / restarted to use the new code. Laravel provides a single `reload` Artisan command that will terminate these services: -->
애플리케이션의 새 버전을 배포한 후에는 queue worker, Laravel Reverb, Laravel Octane과 같이 오래 실행되는 서비스가 새 코드를 사용하도록 다시 로드하거나 다시 시작해야 합니다. Laravel은 이러한 서비스를 종료하는 하나의 `reload` Artisan 명령어를 제공합니다.

```shell
php artisan reload
```

<!-- If you are not using [Laravel Cloud](https://cloud.laravel.com), you should manually configure a process monitor that can detect when your reloadable processes exit and automatically restart them. -->
[Laravel Cloud](https://cloud.laravel.com)를 사용하지 않는다면, 다시 로드할 수 있는 프로세스가 종료될 때 이를 감지하고 자동으로 다시 시작할 수 있는 프로세스 모니터를 직접 설정해야 합니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The debug option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your application's `.env` file. -->
`config/app.php` 설정 파일의 debug 옵션은 오류에 대한 정보를 사용자에게 실제로 얼마나 표시할지 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따르도록 설정되어 있습니다.

> [!WARNING]
> **프로덕션 환경에서는 이 값이 항상 `false`여야 합니다. 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되어 있으면, 애플리케이션의 최종 사용자에게 민감한 설정 값이 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
<!-- ## The Health Route -->
## The Health Route

<!-- Laravel includes a built-in health check route that can be used to monitor the status of your application. In production, this route may be used to report the status of your application to an uptime monitor, load balancer, or orchestration system such as Kubernetes. -->
Laravel에는 애플리케이션 상태를 모니터링하는 데 사용할 수 있는 내장 헬스 체크 라우트가 포함되어 있습니다. 프로덕션에서는 이 라우트를 사용하여 애플리케이션 상태를 uptime monitor, load balancer 또는 Kubernetes와 같은 오케스트레이션 시스템에 보고할 수 있습니다.

<!-- By default, the health check route is served at `/up` and will return a 200 HTTP response if the application has booted without exceptions. Otherwise, a 500 HTTP response will be returned. You may configure the URI for this route in your application's `bootstrap/app` file: -->
기본적으로 헬스 체크 라우트는 `/up`에서 제공되며, 애플리케이션이 예외 없이 부팅되었다면 200 HTTP 응답을 반환합니다. 그렇지 않으면 500 HTTP 응답이 반환됩니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

<!-- When HTTP requests are made to this route, Laravel will also dispatch a `Illuminate\Foundation\Events\DiagnosingHealth` event, allowing you to perform additional health checks relevant to your application. Within a [listener](/docs/13.x/events) for this event, you may check your application's database or cache status. If you detect a problem with your application, you may simply throw an exception from the listener. -->
이 라우트에 HTTP 요청이 들어오면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 디스패치하므로, 애플리케이션에 맞는 추가 헬스 체크를 수행할 수 있습니다. 이 이벤트의 [listener](/docs/13.x/events) 안에서 애플리케이션의 데이터베이스 또는 캐시 상태를 확인할 수 있습니다. 애플리케이션에 문제가 감지되면 리스너에서 예외를 던지면 됩니다.

<a name="deploying-with-cloud-or-forge"></a>
<!-- ## Deploying With Laravel Cloud or Forge -->
## Deploying With Laravel Cloud or Forge

<a name="laravel-cloud"></a>
<!-- #### Laravel Cloud -->
#### Laravel Cloud

<!-- If you would like a fully-managed, auto-scaling deployment platform tuned for Laravel, check out [Laravel Cloud](https://cloud.laravel.com). Laravel Cloud is a robust deployment platform for Laravel, offering managed compute, databases, caches, and object storage. -->
Laravel에 맞게 조정된 완전 관리형 자동 확장 배포 플랫폼이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보십시오. Laravel Cloud는 Laravel을 위한 강력한 배포 플랫폼으로, 관리형 컴퓨팅, 데이터베이스, 캐시, 객체 스토리지를 제공합니다.

<!-- Launch your Laravel application on Cloud and fall in love with the scalable simplicity. Laravel Cloud is fine-tuned by Laravel's creators to work seamlessly with the framework so you can keep writing your Laravel applications exactly like you're used to. -->
Laravel 애플리케이션을 Cloud에서 실행하고, 확장 가능한 단순함을 경험해 보십시오. Laravel Cloud는 Laravel 제작자들이 프레임워크와 매끄럽게 작동하도록 세밀하게 조정했기 때문에, 지금까지 익숙한 방식 그대로 Laravel 애플리케이션을 계속 작성할 수 있습니다.

<a name="laravel-forge"></a>
<!-- #### Laravel Forge -->
#### Laravel Forge

<!-- If you prefer to manage your own servers but aren't comfortable configuring all of the various services needed to run a robust Laravel application, [Laravel Forge](https://forge.laravel.com) is a VPS server management platform for Laravel applications. -->
직접 서버를 관리하고 싶지만 강력한 Laravel 애플리케이션을 실행하는 데 필요한 여러 서비스를 설정하는 일이 익숙하지 않다면, [Laravel Forge](https://forge.laravel.com)는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

<!-- Laravel Forge can create servers on various infrastructure providers such as DigitalOcean, Linode, AWS, and more. In addition, Forge installs and manages all of the tools needed to build robust Laravel applications, such as Nginx, MySQL, Redis, Memcached, Beanstalk, and more. -->
Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에서 서버를 생성할 수 있습니다. 또한 Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구를 설치하고 관리합니다.
