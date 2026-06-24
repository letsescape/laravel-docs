<!-- # Deployment -->
# Deployment

- [Introduction](#introduction)
- [Server Requirements](#server-requirements)
- [Server Configuration](#server-configuration)
    - [Nginx](#nginx)
- [Optimization](#optimization)
    - [Autoloader Optimization](#autoloader-optimization)
    - [Optimizing Configuration Loading](#optimizing-configuration-loading)
    - [Optimizing Route Loading](#optimizing-route-loading)
    - [Optimizing View Loading](#optimizing-view-loading)
- [Debug Mode](#debug-mode)
- [Deploying With Forge / Vapor](#deploying-with-forge-or-vapor)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you're ready to deploy your Laravel application to production, there are some important things you can do to make sure your application is running as efficiently as possible. In this document, we'll cover some great starting points for making sure your Laravel application is deployed properly. -->
Laravel 애플리케이션을 실제 프로덕션 환경에 배포할 준비가 되었다면, 효율적인 운영을 위해 꼭 확인하고 적용해야 할 중요한 사항들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위해 체크해야 할 주요 포인트들을 안내합니다.

<a name="server-requirements"></a>
<!-- ## Server Requirements -->
## Server Requirements

<!-- The Laravel framework has a few system requirements. You should ensure that your web server has the following minimum PHP version and extensions: -->
Laravel 프레임워크는 몇 가지 필수 시스템 요구 사항이 있습니다. 웹 서버가 다음 최소 PHP 버전과 확장 모듈을 갖추고 있는지 반드시 확인해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- PHP >= 7.3
- BCMath PHP Extension
- Ctype PHP Extension
- Fileinfo PHP Extension
- JSON PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PDO PHP Extension
- Tokenizer PHP Extension
- XML PHP Extension
-->
- PHP >= 7.3
- BCMath PHP Extension
- Ctype PHP Extension
- Fileinfo PHP Extension
- JSON PHP Extension
- Mbstring PHP Extension
- OpenSSL PHP Extension
- PDO PHP Extension
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
애플리케이션을 Nginx가 실행 중인 서버에 배포한다면 아래 제공된 설정 파일을 참고하여 웹 서버를 설정할 수 있습니다. 대부분의 경우, 이 파일은 서버의 환경에 맞게 일부 커스터마이징이 필요합니다. **서버 관리에 직접 신경 쓰고 싶지 않으시다면, [Laravel Forge](https://forge.laravel.com)와 같은 Laravel 공식 서버 관리·배포 서비스를 활용하는 것도 좋은 방법입니다.**

<!-- Please ensure, like the configuration below, your web server directs all requests to your application's `public/index.php` file. You should never attempt to move the `index.php` file to your project's root, as serving the application from the project root will expose many sensitive configuration files to the public Internet: -->
아래 설정 예시와 같이, 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 반드시 설정해야 합니다. 절대로 `index.php` 파일을 프로젝트 루트로 이동해서는 안 되며, 프로젝트 루트에서 애플리케이션을 서비스하면 중요한 설정 파일들이 외부에 노출될 수 있습니다.

```
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

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
```

<a name="optimization"></a>
<!-- ## Optimization -->
## Optimization

<a name="autoloader-optimization"></a>
<!-- ### Autoloader Optimization -->
### Autoloader Optimization

<!-- When deploying to production, make sure that you are optimizing Composer's class autoloader map so Composer can quickly find the proper file to load for a given class: -->
프로덕션 환경에 배포할 때는 Composer의 클래스 자동 로더 맵을 꼭 최적화하여, 필요한 클래스 파일을 빠르게 로드할 수 있도록 해주십시오.

```
composer install --optimize-autoloader --no-dev
```

> [!TIP]
> 자동 로더를 최적화하는 것 외에도, 반드시 프로젝트의 소스 제어 저장소에 `composer.lock` 파일을 포함시키는 것이 좋습니다. `composer.lock` 파일이 있으면 프로젝트의 의존성 설치 속도가 훨씬 빨라집니다.

<a name="optimizing-configuration-loading"></a>
<!-- ### Optimizing Configuration Loading -->
### Optimizing Configuration Loading

<!-- When deploying your application to production, you should make sure that you run the `config:cache` Artisan command during your deployment process: -->
프로덕션 환경에 애플리케이션을 배포할 때, 반드시 배포 과정에서 `config:cache` 아티즌 명령어를 실행해야 합니다.

```
php artisan config:cache
```

<!-- This command will combine all of Laravel's configuration files into a single, cached file, which greatly reduces the number of trips the framework must make to the filesystem when loading your configuration values. -->
이 명령어는 Laravel의 모든 설정 파일을 하나로 합쳐 캐시된 파일로 만들어주며, 설정값을 불러올 때 파일 시스템 접근 횟수를 대폭 줄여줍니다.

> [!NOTE]
> 배포 과정에서 `config:cache` 명령어를 사용한다면, 오직 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐시된 후에는 `.env` 파일이 로드되지 않으며, `.env` 변수에 대한 모든 `env` 함수 호출은 `null`을 반환하게 됩니다.

<a name="optimizing-route-loading"></a>
<!-- ### Optimizing Route Loading -->
### Optimizing Route Loading

<!-- If you are building a large application with many routes, you should make sure that you are running the `route:cache` Artisan command during your deployment process: -->
많은 라우트를 가진 대규모 애플리케이션을 개발한다면, 배포 시 반드시 `route:cache` 아티즌 명령어를 실행하는 것이 좋습니다.

```
php artisan route:cache
```

<!-- This command reduces all of your route registrations into a single method call within a cached file, improving the performance of route registration when registering hundreds of routes. -->
이 명령어는 모든 라우트 등록 정보를 하나의 캐시 파일 내의 메서드 호출로 압축하여, 수백 개 이상의 라우트를 등록할 때 라우트 등록 성능을 크게 개선해 줍니다.

<a name="optimizing-view-loading"></a>
<!-- ### Optimizing View Loading -->
### Optimizing View Loading

<!-- When deploying your application to production, you should make sure that you run the `view:cache` Artisan command during your deployment process: -->
프로덕션 환경에 애플리케이션을 배포할 때, 반드시 배포 과정에서 `view:cache` 아티즌 명령어를 실행하는 것이 좋습니다.

```
php artisan view:cache
```

<!-- This command precompiles all your Blade views so they are not compiled on demand, improving the performance of each request that returns a view. -->
이 명령어는 모든 Blade 뷰 파일을 미리 컴파일해 두므로, 뷰가 요청될 때마다 즉석에서 컴파일하는 대신 미리 준비한 결과를 반환함으로써 성능을 높일 수 있습니다.

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The debug option in your config/app.php configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the APP_DEBUG environment variable, which is stored in your .env file. -->
config/app.php 설정 파일의 debug 옵션은 오류가 발생했을 때 사용자가 얼마나 많은 정보를 확인할 수 있는지를 결정합니다. 기본적으로 이 옵션은 .env 파일에 저장된 APP_DEBUG 환경 변수 값을 따릅니다.

<!-- **In your production environment, this value should always be `false`. If the `APP_DEBUG` variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
**프로덕션 환경에서는 이 값을 반드시 `false`로 설정해야 합니다. 만약 프로덕션에서 `APP_DEBUG` 변수가 `true`로 설정되어 있으면, 민감한 설정 정보가 애플리케이션 사용자에게 노출될 위험이 있습니다.**

<a name="deploying-with-forge-or-vapor"></a>
<!-- ## Deploying With Forge / Vapor -->
## Deploying With Forge / Vapor

<a name="laravel-forge"></a>
<!-- #### Laravel Forge -->
#### Laravel Forge

<!-- If you aren't quite ready to manage your own server configuration or aren't comfortable configuring all of the various services needed to run a robust Laravel application, [Laravel Forge](https://forge.laravel.com) is a wonderful alternative. -->
직접 서버 설정을 관리할 준비가 아직 되지 않았거나, Laravel 애플리케이션을 안정적으로 운영하는 데 필요한 다양한 서비스 설정이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)를 이용하는 것도 좋은 선택입니다.

<!-- Laravel Forge can create servers on various infrastructure providers such as DigitalOcean, Linode, AWS, and more. In addition, Forge installs and manages all of the tools needed to build robust Laravel applications, such as Nginx, MySQL, Redis, Memcached, Beanstalk, and more. -->
Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공자 위에 서버를 생성할 수 있으며, Laravel 애플리케이션을 운영하는 데 필요한 Nginx, MySQL, Redis, Memcached, Beanstalk 등 각종 도구를 자동 설치·관리해 줍니다.

<a name="laravel-vapor"></a>
<!-- #### Laravel Vapor -->
#### Laravel Vapor

<!-- If you would like a totally serverless, auto-scaling deployment platform tuned for Laravel, check out [Laravel Vapor](https://vapor.laravel.com). Laravel Vapor is a serverless deployment platform for Laravel, powered by AWS. Launch your Laravel infrastructure on Vapor and fall in love with the scalable simplicity of serverless. Laravel Vapor is fine-tuned by Laravel's creators to work seamlessly with the framework so you can keep writing your Laravel applications exactly like you're used to. -->
Laravel에 최적화된 완전 서버리스·오토 스케일링 배포 플랫폼을 원한다면 [Laravel Vapor](https://vapor.laravel.com)를 고려해 보세요. Laravel Vapor는 AWS 기반의 서버리스 배포 플랫폼으로, Vapor 위에서 Laravel 인프라를 손쉽게 구축하고 서버리스의 뛰어난 확장성과 심플함을 경험할 수 있습니다. 이 플랫폼은 Laravel 제작진이 직접 미세 조정하여, 기존의 Laravel 개발 방식 그대로 원활하게 사용할 수 있습니다.