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
- [Debug Mode](#debug-mode)
- [The Health Route](#the-health-route)
- [Easy Deployment With Forge / Vapor](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you're ready to deploy your Laravel application to production, there are some important things you can do to make sure your application is running as efficiently as possible. In this document, we'll cover some great starting points for making sure your Laravel application is deployed properly. -->
Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 동작하도록 하기 위해 신경 쓸 중요한 사항들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 적절히 배포하기 위한 주요 출발점을 다룹니다.

<a name="server-requirements"></a>
<!-- ## Server Requirements -->
## Server Requirements

<!-- The Laravel framework has a few system requirements. You should ensure that your web server has the following minimum PHP version and extensions: -->
Laravel 프레임워크를 실행하기 위해서는 몇 가지 시스템 요구사항이 있습니다. 웹 서버에 다음의 최소 PHP 버전 및 확장 기능들이 설치되어 있는지 반드시 확인해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- PHP >= 8.2
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
- PHP >= 8.2
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

<!-- If you are deploying your application to a server that is running Nginx, you may use the following configuration file as a starting point for configuring your web server. Most likely, this file will need to be customized depending on your server's configuration. **If you would like assistance in managing your server, consider using a first-party Laravel server management and deployment service such as [Laravel Forge](https://forge.laravel.com).** -->
애플리케이션을 Nginx 서버에 배포한다면, 아래의 설정 파일을 웹 서버 구성의 시작점으로 사용할 수 있습니다. 대부분의 경우, 해당 파일은 서버 환경에 맞게 추가로 커스터마이즈해야 합니다. **만약 서버 관리에 도움이 필요하다면 [Laravel Forge](https://forge.laravel.com)와 같이 Laravel 공식의 서버 관리 및 배포 서비스를 이용하는 것도 고려해보시길 권장합니다.**

<!-- Please ensure, like the configuration below, your web server directs all requests to your application's `public/index.php` file. You should never attempt to move the `index.php` file to your project's root, as serving the application from the project root will expose many sensitive configuration files to the public Internet: -->
아래 예시와 같이 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 반드시 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 옮기려는 시도는 절대 하지 말아야 하며, 프로젝트 루트에서 애플리케이션을 서비스하면 다수의 민감한 설정 파일이 외부에 노출되어 보안 위험이 발생할 수 있습니다.

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
        fastcgi_pass unix:/var/run/php/php8.2-fpm.sock;
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
[FrankenPHP](https://frankenphp.dev/)를 사용하여 Laravel 애플리케이션을 서비스할 수도 있습니다. FrankenPHP는 Go 언어로 개발된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 사용해 Laravel PHP 애플리케이션을 서비스하려면, 간단히 다음과 같이 `php-server` 명령어를 실행하면 됩니다.

```shell
frankenphp php-server -r public/
```

<!-- To take advantage of more powerful features supported by FrankenPHP, such as its [Laravel Octane](/docs/11.x/octane) integration, HTTP/3, modern compression, or the ability to package Laravel applications as standalone binaries, please consult FrankenPHP's [Laravel documentation](https://frankenphp.dev/docs/laravel/). -->
FrankenPHP가 제공하는 [Laravel Octane](/docs/11.x/octane) 연동, HTTP/3, 최신 압축 기술, 또는 Laravel 애플리케이션을 단일 실행 파일로 패키징하는 등의 고급 기능을 사용하려면, FrankenPHP의 [Laravel documentation](https://frankenphp.dev/docs/laravel/)를 참고해 주시기 바랍니다.

<a name="directory-permissions"></a>
<!-- ### Directory Permissions -->
### Directory Permissions

<!-- Laravel will need to write to the `bootstrap/cache` and `storage` directories, so you should ensure the web server process owner has permission to write to these directories. -->
Laravel은 `bootstrap/cache`와 `storage` 디렉터리에 파일을 쓸 수 있어야 하므로, 반드시 웹 서버 프로세스 소유자가 이들 디렉터리에 쓸 수 있는 권한을 가지고 있어야 합니다.

<a name="optimization"></a>
<!-- ## Optimization -->
## Optimization

<!-- When deploying your application to production, there are a variety of files that should be cached, including your configuration, events, routes, and views. Laravel provides a single, convenient `optimize` Artisan command that will cache all of these files. This command should typically be invoked as part of your application's deployment process: -->
프로덕션 환경에 애플리케이션을 배포할 때는, 설정, 이벤트, 라우트, 뷰 파일을 캐시에 저장해두는 것이 좋습니다. Laravel은 이러한 파일들을 한 번에 캐싱해 주는 편리한 `optimize` Artisan 명령어를 제공합니다. 이 명령어는 일반적으로 배포 과정의 일부로 실행하는 것을 권장합니다.

```shell
php artisan optimize
```

<!-- The `optimize:clear` method may be used to remove all of the cache files generated by the `optimize` command as well as all keys in the default cache driver: -->
`optimize:clear` 명령어는 `optimize` 명령어로 생성된 모든 캐시 파일과, 기본 캐시 드라이버에 저장된 모든 키를 제거하는 데 사용할 수 있습니다.

```shell
php artisan optimize:clear
```

<!-- In the following documentation, we will discuss each of the granular optimization commands that are executed by the `optimize` command. -->
다음 문서에서는 위의 `optimize` 명령어가 내부에서 실행하는 각각의 세부 최적화 명령어들에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
<!-- ### Caching Configuration -->
### Caching Configuration

<!-- When deploying your application to production, you should make sure that you run the `config:cache` Artisan command during your deployment process: -->
프로덕션 환경에 배포할 때는, 반드시 배포 프로세스 중에 `config:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan config:cache
```

<!-- This command will combine all of Laravel's configuration files into a single, cached file, which greatly reduces the number of trips the framework must make to the filesystem when loading your configuration values. -->
이 명령어는 Laravel의 모든 구성 파일을 하나의 캐시 파일로 합치므로, 프레임워크가 설정 값을 불러올 때 파일 시스템 접근 횟수를 크게 줄여줍니다.

> [!WARNING]
> 배포 시 `config:cache` 명령어를 실행하면, 반드시 구성 파일 내에서만 `env` 함수를 호출해야 합니다. 구성 캐시가 생성된 이후에는 `.env` 파일이 더 이상 로드되지 않고, `.env` 파일의 변수를 사용하기 위해 호출한 모든 `env` 함수는 `null`을 반환하게 됩니다.

<a name="caching-events"></a>
<!-- ### Caching Events -->
### Caching Events

<!-- You should cache your application's auto-discovered event to listener mappings during your deployment process. This can be accomplished by invoking the `event:cache` Artisan command during deployment: -->
애플리케이션에서 자동으로 발견된 이벤트와 리스너의 매핑 또한 배포 프로세스 중에 캐싱해두는 것이 좋습니다. 이를 위해 배포 시점에 `event:cache` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
<!-- ### Caching Routes -->
### Caching Routes

<!-- If you are building a large application with many routes, you should make sure that you are running the `route:cache` Artisan command during your deployment process: -->
라우트가 많은 대규모 애플리케이션을 빌드할 경우, 배포 프로세스에서 `route:cache` Artisan 명령어를 반드시 실행해 주세요.

```shell
php artisan route:cache
```

<!-- This command reduces all of your route registrations into a single method call within a cached file, improving the performance of route registration when registering hundreds of routes. -->
이 명령어는 모든 라우트 등록 정보를 단일 메서드 호출로 압축하여 캐시 파일에 저장하므로, 수백 개의 라우트를 한 번에 등록할 때 훨씬 더 빠르게 처리할 수 있습니다.

<a name="optimizing-view-loading"></a>
<!-- ### Caching Views -->
### Caching Views

<!-- When deploying your application to production, you should make sure that you run the `view:cache` Artisan command during your deployment process: -->
애플리케이션을 프로덕션 환경에 배포할 때는, 배포 과정에서 반드시 `view:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan view:cache
```

<!-- This command precompiles all your Blade views so they are not compiled on demand, improving the performance of each request that returns a view. -->
이 명령어는 모든 Blade 뷰를 미리 컴파일해두기 때문에, 매 요청마다 뷰를 그때그때 컴파일할 필요가 없어져 뷰를 반환하는 요청의 성능이 향상됩니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The debug option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your application's `.env` file. -->
`config/app.php` 설정 파일의 debug 옵션은 오류 발생 시 사용자에게 얼마나 많은 정보를 표시할지 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

> [!WARNING]
> **프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 만약 `APP_DEBUG` 변수가 프로덕션에서 `true`로 되어 있다면, 민감한 설정 값들이 애플리케이션 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
<!-- ## The Health Route -->
## The Health Route

<!-- Laravel includes a built-in health check route that can be used to monitor the status of your application. In production, this route may be used to report the status of your application to an uptime monitor, load balancer, or orchestration system such as Kubernetes. -->
Laravel은 애플리케이션의 상태를 확인할 수 있는 내장 헬스 체크 라우트를 제공합니다. 프로덕션 환경에서는 이 라우트를 사용해 업타임 모니터, 로드 밸런서, 또는 Kubernetes와 같은 오케스트레이션 시스템에 애플리케이션의 상태를 보고할 수 있습니다.

<!-- By default, the health check route is served at `/up` and will return a 200 HTTP response if the application has booted without exceptions. Otherwise, a 500 HTTP response will be returned. You may configure the URI for this route in your application's `bootstrap/app` file: -->
기본적으로 헬스 체크 라우트는 `/up` 경로에서 서비스되며, 애플리케이션이 예외 없이 부팅되었다면 200 HTTP 응답을 반환합니다. 문제가 있을 경우 500 HTTP 응답이 반환됩니다. 해당 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다.

```
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

<!-- When HTTP requests are made to this route, Laravel will also dispatch a `Illuminate\Foundation\Events\DiagnosingHealth` event, allowing you to perform additional health checks relevant to your application. Within a [listener](/docs/11.x/events) for this event, you may check your application's database or cache status. If you detect a problem with your application, you may simply throw an exception from the listener. -->
이 경로로 HTTP 요청이 오면, Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트를 자동으로 디스패치합니다. 이를 통해 추가적인 헬스 체크(예: 데이터베이스나 캐시 상태 확인 등)를 할 수 있습니다. 관련 [listener](/docs/11.x/events)에서 문제를 감지했다면 예외를 던져 처리할 수 있습니다.

<a name="deploying-with-forge-or-vapor"></a>
<!-- ## Easy Deployment With Forge / Vapor -->
## Easy Deployment With Forge / Vapor

<a name="laravel-forge"></a>
<!-- #### Laravel Forge -->
#### Laravel Forge

<!-- If you aren't quite ready to manage your own server configuration or aren't comfortable configuring all of the various services needed to run a robust Laravel application, [Laravel Forge](https://forge.laravel.com) is a wonderful alternative. -->
서버 설정을 직접 관리하거나 다양한 서비스를 직접 구성하는 데 익숙하지 않다면, [Laravel Forge](https://forge.laravel.com)라는 훌륭한 대안이 있습니다.

<!-- Laravel Forge can create servers on various infrastructure providers such as DigitalOcean, Linode, AWS, and more. In addition, Forge installs and manages all of the tools needed to build robust Laravel applications, such as Nginx, MySQL, Redis, Memcached, Beanstalk, and more. -->
Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 공급자에 서버를 자동으로 생성할 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 robust한 Laravel 애플리케이션 운용에 필요한 모든 도구를 설치 및 관리해줍니다.

> [!NOTE]
> Laravel Forge를 활용한 배포에 대한 전체 가이드가 필요하다면 [Laravel Bootcamp](https://bootcamp.laravel.com/deploying)와 Forge [video series available on Laracasts](https://laracasts.com/series/learn-laravel-forge-2022-edition)를 참고해보세요.

<a name="laravel-vapor"></a>
<!-- #### Laravel Vapor -->
#### Laravel Vapor

<!-- If you would like a totally serverless, auto-scaling deployment platform tuned for Laravel, check out [Laravel Vapor](https://vapor.laravel.com). Laravel Vapor is a serverless deployment platform for Laravel, powered by AWS. Launch your Laravel infrastructure on Vapor and fall in love with the scalable simplicity of serverless. Laravel Vapor is fine-tuned by Laravel's creators to work seamlessly with the framework so you can keep writing your Laravel applications exactly like you're used to. -->
Laravel에 최적화된 완전 서버리스, 자동 확장형 배포 플랫폼을 찾는다면 [Laravel Vapor](https://vapor.laravel.com)를 살펴보세요. Laravel Vapor는 AWS 기반의 Laravel 서버리스 배포 플랫폼입니다. Vapor를 통해 Laravel 인프라를 손쉽게 런칭하고, 서버리스의 뛰어난 확장성과 단순함에 빠져보세요. Laravel Vapor는 Laravel 공식 팀에 의해 프레임워크와 완벽하게 통합되어 동작하므로, 기존처럼 Laravel 애플리케이션을 자유롭게 개발할 수 있습니다.