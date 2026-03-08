# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [디렉터리 권한](#directory-permissions)
- [최적화](#optimization)
    - [설정 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [서비스 재시작](#reloading-services)
- [디버그 모드](#debug-mode)
- [헬스(Health) 라우트](#the-health-route)
- [Laravel Cloud 또는 Forge로 배포하기](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 동작할 수 있도록 하기 위해 반드시 확인해야 할 중요한 사항들이 있습니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포할 수 있도록 도와주는 유용한 시작 지점을 다룹니다.

<a name="server-requirements"></a>
## 서버 요구사항 (Server Requirements)

Laravel 프레임워크는 몇 가지 시스템 요구사항이 있습니다. 웹 서버가 다음의 최소 PHP 버전 및 확장 모듈을 갖추고 있는지 반드시 확인해야 합니다.

<div class="content-list" markdown="1">

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

</div>

<a name="server-configuration"></a>
## 서버 설정 (Server Configuration)

<a name="nginx"></a>
### Nginx

서버에서 Nginx를 사용하여 애플리케이션을 배포하는 경우, 웹 서버 설정의 시작점으로 아래 설정 파일을 참고할 수 있습니다. 대부분 서버 환경에 따라 해당 파일을 커스터마이즈해야 할 필요가 있습니다. **서버 관리에 도움이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 Laravel 플랫폼 사용을 고려해 보십시오.**

아래 예시와 같이, 모든 요청이 애플리케이션의 `public/index.php` 파일로 라우팅되도록 웹 서버를 설정해야 합니다. `index.php` 파일을 프로젝트 루트로 이동시키는 시도는 절대 하지 마십시오. 프로젝트 루트에서 애플리케이션을 서비스하면 많은 민감한 설정 파일들이 외부에 노출될 수 있습니다.

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
### FrankenPHP

[FrankenPHP](https://frankenphp.dev/)를 사용하여 Laravel 애플리케이션을 서비스할 수도 있습니다. FrankenPHP는 Go 언어로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 이용해 Laravel PHP 애플리케이션을 서비스하려면, 아래와 같이 `php-server` 명령어를 실행하면 됩니다.

```shell
frankenphp php-server -r public/
```

HTTP/3, 최신 압축, Laravel Octane 연동 등 FrankenPHP가 지원하는 고급 기능이나, Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 것과 같은 기능을 활용하려면 FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하십시오.

<a name="directory-permissions"></a>
### 디렉터리 권한

Laravel은 `bootstrap/cache`와 `storage` 디렉터리에 파일을 쓸 수 있어야 하므로, 웹 서버 프로세스 소유자가 해당 디렉터리에 쓸 수 있는 권한을 갖고 있는지 반드시 확인해야 합니다.

<a name="optimization"></a>
## 최적화 (Optimization)

애플리케이션을 프로덕션 환경에 배포할 때는, 설정, 이벤트, 라우트, 뷰 등 다양한 파일을 캐싱하는 것이 권장됩니다. Laravel은 이 모든 파일을 한 번에 캐싱할 수 있는 편리한 `optimize` Artisan 명령어를 제공합니다. 이 명령어는 일반적으로 배포 과정의 일부로 실행해야 합니다.

```shell
php artisan optimize
```

`optimize:clear` 명령어는 `optimize` 명령어로 생성된 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거할 수 있습니다.

```shell
php artisan optimize:clear
```

이후 문서에서는 `optimize` 명령어에서 실행되는 각 세부 최적화 명령어에 대해 다룹니다.

<a name="optimizing-configuration-loading"></a>
### 설정 캐싱

프로덕션 환경에 애플리케이션을 배포할 때는, 배포 과정 중에 반드시 `config:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan config:cache
```

이 명령어를 실행하면 Laravel의 모든 설정 파일이 하나의 캐시 파일로 병합되어, 설정 값을 불러올 때 프레임워크가 파일 시스템에 접근하는 횟수를 크게 줄일 수 있습니다.

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행했다면, 반드시 설정 파일 내에서만 `env` 함수를 사용해야 합니다. 설정이 캐시된 이후에는 `.env` 파일이 더 이상 로드되지 않으며, 해당 시점 이후 `.env` 변수를 불러오려는 `env` 함수 호출은 모두 `null`을 반환합니다.

<a name="caching-events"></a>
### 이벤트 캐싱

배포 과정 중에, 애플리케이션에서 자동으로 탐지된 이벤트와 리스너 매핑 정보를 캐싱해야 합니다. 이를 위해 배포 과정에서 `event:cache` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

많은 라우트를 사용하는 대형 애플리케이션을 개발하는 경우, 배포 과정에 `route:cache` Artisan 명령어를 반드시 실행해야 합니다.

```shell
php artisan route:cache
```

이 명령어는 모든 라우트 등록을 하나의 메서드 호출로 축약해서 캐시 파일로 저장하며, 수백 개의 라우트를 등록할 때 성능을 크게 개선합니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

프로덕션 환경에 배포할 때는, 배포 과정에 반드시 `view:cache` Artisan 명령어를 실행해야 합니다.

```shell
php artisan view:cache
```

이 명령어는 모든 Blade 뷰를 미리 컴파일하여, 요청 시 뷰를 즉석에서 컴파일하지 않아도 되어 각 요청의 응답 성능이 향상됩니다.

<a name="reloading-services"></a>
## 서비스 재시작 (Reloading Services)

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com) 환경에서는 `reload` 명령어를 사용할 필요가 없습니다. 모든 서비스의 정상적인 재시작이 자동으로 처리됩니다.

애플리케이션의 새 버전을 배포한 후에는, queue 워커, Laravel Reverb, Laravel Octane 등과 같은 장기 실행 서비스들이 새로운 코드를 반영할 수 있도록 반드시 재시작해야 합니다. Laravel은 이 서비스들을 종료시키는 단일 `reload` Artisan 명령어를 제공합니다.

```shell
php artisan reload
```

[Laravel Cloud](https://cloud.laravel.com)를 사용하지 않는 경우, 재시작이 필요한 프로세스가 종료되는 것을 감지하고 자동으로 재시작할 수 있도록 프로세스 모니터를 직접 구성해야 합니다.

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 debug 옵션은 에러 발생 시 사용자에게 얼마나 자세한 정보를 보여줄지를 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 `APP_DEBUG`가 프로덕션 환경에서 `true`로 되어 있다면, 민감한 설정 정보가 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 헬스(Health) 라우트 (The Health Route)

Laravel은 애플리케이션의 상태를 점검할 수 있는 기본 헬스 체크(health check) 라우트를 제공합니다. 프로덕션 환경에서는 이 라우트를 이용하여 업타임 모니터, 로드 밸런서, 또는 Kubernetes와 같은 오케스트레이션 시스템에 애플리케이션의 상태를 보고할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up`에서 서비스되며, 애플리케이션이 예외 없이 부팅된 경우 HTTP 200 응답을 반환합니다. 그렇지 않으면, HTTP 500 응답을 반환하게 됩니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 라우트에 HTTP 요청이 오면, Laravel은 또한 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트를 디스패치합니다. 이를 통해 애플리케이션에서 추가적인 상태 점검을 할 수 있습니다. 이 이벤트의 [리스너](/docs/12.x/events) 내부에서 데이터베이스나 캐시 상태를 점검할 수 있으며, 문제가 감지되었다면 리스너에서 예외를 던지면 됩니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge로 배포하기 (Deploying With Laravel Cloud or Forge)

<a name="laravel-cloud"></a>
#### Laravel Cloud

완전 관리형, 자동 확장 배포 플랫폼을 원한다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보십시오. Laravel Cloud는 관리형 컴퓨트, 데이터베이스, 캐시, 오브젝트 스토리지를 제공하는 강력한 Laravel 배포 플랫폼입니다.

Laravel Cloud에서 애플리케이션을 시작하고, 확장 가능한 간편함에 반해보십시오. Laravel Cloud는 Laravel 제작진이 프레임워크와 매끄럽게 통합되도록 미세 조정하였으므로, 이전과 동일하게 편하게 Laravel 애플리케이션을 개발할 수 있습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

서버를 직접 관리하고 싶지만, 강력한 Laravel 애플리케이션 실행을 위해 필요한 다양한 서비스를 직접 설정하는 것이 어렵다면, [Laravel Forge](https://forge.laravel.com)는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에서 서버를 생성할 수 있으며, Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션 구성을 위해 필요한 모든 도구를 설치 및 관리해줍니다.
