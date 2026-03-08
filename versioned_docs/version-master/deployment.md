# 배포 (Deployment)

- [소개](#introduction)
- [서버 요구 사항](#server-requirements)
- [서버 설정](#server-configuration)
    - [Nginx](#nginx)
    - [FrankenPHP](#frankenphp)
    - [디렉터리 권한](#directory-permissions)
- [최적화](#optimization)
    - [설정 파일 캐싱](#optimizing-configuration-loading)
    - [이벤트 캐싱](#caching-events)
    - [라우트 캐싱](#optimizing-route-loading)
    - [뷰 캐싱](#optimizing-view-loading)
- [서비스 재시작](#reloading-services)
- [디버그 모드](#debug-mode)
- [헬스 경로](#the-health-route)
- [Laravel Cloud 또는 Forge를 이용한 배포](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 운영 환경(production)으로 배포할 준비가 되었다면, 애플리케이션이 최대한 효율적으로 동작하도록 몇 가지 중요한 사항을 점검해야 합니다. 이 문서에서는 Laravel 애플리케이션을 올바르게 배포하기 위한 중요한 시작 지점을 안내합니다.

<a name="server-requirements"></a>
## 서버 요구 사항 (Server Requirements)

Laravel 프레임워크는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버가 다음의 최소 PHP 버전 및 확장 기능을 갖추었는지 반드시 확인하십시오.

<div class="content-list" markdown="1">

- PHP >= 8.2
- Ctype PHP 확장
- cURL PHP 확장
- DOM PHP 확장
- Fileinfo PHP 확장
- Filter PHP 확장
- Hash PHP 확장
- Mbstring PHP 확장
- OpenSSL PHP 확장
- PCRE PHP 확장
- PDO PHP 확장
- Session PHP 확장
- Tokenizer PHP 확장
- XML PHP 확장

</div>

<a name="server-configuration"></a>
## 서버 설정 (Server Configuration)

<a name="nginx"></a>
### Nginx

서버에 Nginx를 사용해 애플리케이션을 배포하는 경우, 아래의 설정 파일 예시를 웹 서버 구성의 시작점으로 사용할 수 있습니다. 대부분의 경우, 서버 환경에 맞게 이 파일을 꼭 맞추어 커스터마이즈해야 합니다. **서버 운영을 직접 관리하는 것이 어렵다면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전 관리형 Laravel 플랫폼 사용을 고려해 보십시오.**

아래 설정과 같이 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하도록 반드시 설정해야 합니다. 프로젝트 루트로 `index.php` 파일을 옮겨서 애플리케이션을 제공해서는 안됩니다. 그렇게 하면 많은 민감한 설정 파일이 외부 인터넷에 노출될 위험이 있습니다.

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

[FrankenPHP](https://frankenphp.dev/)를 사용해서도 Laravel 애플리케이션을 운영할 수 있습니다. FrankenPHP는 Go 언어로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 이용해 Laravel 애플리케이션을 제공하려면, 다음과 같이 `php-server` 명령어를 실행하면 됩니다.

```shell
frankenphp php-server -r public/
```

Laravel Octane 통합, HTTP/3, 최신 압축 기능, 독립 실행형 바이너리로의 패키징 등 FrankenPHP가 제공하는 다양한 고급 기능을 활용하려면, FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참고하시기 바랍니다.

<a name="directory-permissions"></a>
### 디렉터리 권한

Laravel은 `bootstrap/cache`와 `storage` 디렉터리에 파일을 기록할 수 있어야 합니다. 따라서 웹 서버 프로세스 소유자가 이 디렉터리에 쓰기 권한이 있는지 반드시 확인해야 합니다.

<a name="optimization"></a>
## 최적화 (Optimization)

운영 환경에 애플리케이션을 배포할 때는 설정 파일, 이벤트, 라우트, 뷰 등 여러 파일을 캐시에 저장해야 합니다. Laravel은 이 모든 파일을 한 번에 캐시하는 편리한 `optimize` Artisan 명령어를 제공합니다. 이 명령어는 보통 애플리케이션 배포 프로세스에서 실행해야 합니다.

```shell
php artisan optimize
```

`optimize:clear` 명령을 사용하면 `optimize` 명령에 의해 생성된 모든 캐시 파일뿐 아니라 기본 캐시 드라이버의 모든 키도 제거할 수 있습니다.

```shell
php artisan optimize:clear
```

아래 문서에서는 `optimize` 명령이 내부적으로 실행하는 각각의 세부 최적화 명령어에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 설정 파일 캐싱

애플리케이션을 운영 환경에 배포할 때는 반드시 배포 과정에서 `config:cache` Artisan 명령을 실행해야 합니다.

```shell
php artisan config:cache
```

이 명령은 Laravel의 모든 설정 파일을 하나의 캐시 파일로 통합하므로, 프레임워크가 설정 값을 불러올 때 파일 시스템 접근 횟수를 크게 줄일 수 있습니다.

> [!WARNING]
> 배포 과정에서 `config:cache` 명령이 실행된다면, 반드시 설정 파일 내에서만 `env` 함수를 호출해야 합니다. 설정이 캐시되면 `.env` 파일은 더 이상 로드되지 않으며, 설정 파일이 아닌 곳에서 `env` 함수를 호출해 `.env` 변수를 읽어오려 하면 `null`이 반환됩니다.

<a name="caching-events"></a>
### 이벤트 캐싱

애플리케이션의 자동 탐지 이벤트-리스너 매핑도 배포 과정에서 캐시해야 합니다. 이를 위해 배포 시점에 `event:cache` Artisan 명령을 실행하십시오.

```shell
php artisan event:cache
```

<a name="optimizing-route-loading"></a>
### 라우트 캐싱

라우트가 많은 대규모 애플리케이션을 개발하는 경우, 배포 시 꼭 `route:cache` Artisan 명령을 실행해야 합니다.

```shell
php artisan route:cache
```

이 명령은 모든 라우트 등록 작업을 하나의 캐시 파일의 메서드 호출로 축약하여, 수백 개의 라우트를 등록할 때 성능 향상 효과가 있습니다.

<a name="optimizing-view-loading"></a>
### 뷰 캐싱

운영 환경에 애플리케이션을 배포할 때는 배포 프로세스에서 `view:cache` Artisan 명령도 꼭 실행하십시오.

```shell
php artisan view:cache
```

이 명령은 모든 Blade 뷰 파일을 미리 컴파일하여, 각 요청마다 뷰가 필요할 때마다 실시간으로 컴파일하는 능력이 필요 없게 만들어 성능이 향상됩니다.

<a name="reloading-services"></a>
## 서비스 재시작 (Reloading Services)

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com) 환경에서는 모든 서비스의 정상적인 재시작이 자동으로 처리되므로, 별도로 `reload` 명령을 사용할 필요가 없습니다.

애플리케이션의 새로운 버전을 배포한 후에는 queue worker, Laravel Reverb, Laravel Octane과 같은 장기 실행 서비스들이 새 코드로 동작하도록 반드시 재시작해야 합니다. Laravel에서는 이런 서비스들을 종료하는 `reload` Artisan 명령을 제공합니다.

```shell
php artisan reload
```

[Laravel Cloud](https://cloud.laravel.com)를 사용하지 않는 경우, 재시작 가능한 프로세스가 종료되는 것을 감지하여 자동으로 재시작할 수 있는 프로세스 모니터를 직접 설정해야 합니다.

<a name="debug-mode"></a>
## 디버그 모드 (Debug Mode)

`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 표시되는 에러 정보의 양을 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따릅니다.

> [!WARNING]
> **운영 환경(production)에서는 이 값을 반드시 `false`로 설정해야 합니다. 만약 `APP_DEBUG` 변수가 운영 환경에서 `true`로 되어 있으면, 민감한 설정값이 최종 사용자에게 노출될 수 있습니다.**

<a name="the-health-route"></a>
## 헬스 경로 (The Health Route)

Laravel은 애플리케이션의 상태를 모니터링할 수 있는 내장 헬스 체크(health check) 라우트를 제공합니다. 운영 환경에서는 이 라우트를 활용해 uptime 모니터링, 로드 밸런서, Kubernetes 같은 오케스트레이션 시스템에 애플리케이션 상태를 보고할 수 있습니다.

기본적으로 헬스 체크 라우트는 `/up` URI에서 제공되며, 애플리케이션이 예외 없이 부팅되었다면 HTTP 200 응답을 반환합니다. 그렇지 않은 경우에는 HTTP 500 응답이 반환됩니다. 이 라우트의 URI는 애플리케이션의 `bootstrap/app` 파일에서 설정할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)
```

이 경로로 HTTP 요청이 들어올 때, Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 디스패치합니다. 이를 통해 애플리케이션에 맞는 추가 상태 점검을 수행할 수 있습니다. 이 이벤트에 [리스너](/docs/master/events)에서 데이터베이스나 캐시 상태를 검사할 수 있으며, 문제가 감지되면 리스너 내부에서 예외를 던지기만 하면 됩니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 이용한 배포 (Deploying With Laravel Cloud or Forge)

<a name="laravel-cloud"></a>
#### Laravel Cloud

Laravel에 최적화되고, 자동 스케일링 기능이 제공되는 완전 관리형 배포 플랫폼이 필요하다면 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보십시오. Laravel Cloud는 관리형 컴퓨트, 데이터베이스, 캐시, 오브젝트 스토리지를 제공하는 강력한 배포 플랫폼입니다.

Cloud에서 Laravel 애플리케이션을 시작해서 확장 가능한, 단순한 배포 경험을 누려 보세요. Laravel Cloud는 Laravel의 창립자들이 프레임워크에 맞게 직접 최적화한 서비스로, 기존에 하던 대로 Laravel 애플리케이션을 작성하는 데 아무런 불편이 없습니다.

<a name="laravel-forge"></a>
#### Laravel Forge

직접 서버를 운영하고 싶지만, 다양한 서비스를 직접 설정하는 일이 부담스럽다면 [Laravel Forge](https://forge.laravel.com)가 좋은 선택이 될 수 있습니다. Laravel Forge는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등 다양한 인프라 제공업체에 서버를 생성할 수 있습니다. 또한, Nginx, MySQL, Redis, Memcached, Beanstalk 등 강력한 Laravel 애플리케이션 구축에 필요한 모든 도구의 설치 및 관리도 Forge가 자동으로 처리합니다.