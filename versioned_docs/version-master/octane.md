# 라라벨 Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 준비 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스 시작](#serving-your-application)
    - [HTTPS를 통한 애플리케이션 서비스 시작](#serving-your-application-via-https)
    - [Nginx를 통한 애플리케이션 서비스 시작](#serving-your-application-via-nginx)
    - [파일 변경 사항 감지](#watching-for-file-changes)
    - [워커 개수 지정](#specifying-the-worker-count)
    - [최대 요청 개수 지정](#specifying-the-max-request-count)
    - [최대 실행 시간 지정](#specifying-the-max-execution-time)
    - [워커 재시작](#reloading-the-workers)
    - [서버 정지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [요청 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱(Tick) 및 인터벌(Interval)](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 활용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 후 메모리에 유지하며, 매우 빠른 속도로 요청을 처리할 수 있도록 해줍니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

```shell
composer require laravel/octane
```

Octane 설치 후, `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 설치할 수 있습니다.

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 준비 사항 (Server Prerequisites)

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, Early Hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 FrankenPHP를 선택하면, Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치해줍니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP 사용

[Laravel Sail](/docs/master/sail)로 애플리케이션 개발을 계획하고 있다면, 다음 명령어들로 Octane 및 FrankenPHP를 설치하세요.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

다음으로, `octane:install` Artisan 명령어에 `--server=frankenphp` 옵션을 추가해 FrankenPHP 바이너리를 설치합니다.

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가해야 합니다. 이 변수에는 Sail이 Octane을 이용해 애플리케이션을 서비스하기 위한 명령어가 들어갑니다(PHP 개발 서버 대신 사용).

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

HTTPS, HTTP/2, HTTP/3를 활성화하려면 아래와 같이 설정을 변경하세요.

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

일반적으로 FrankenPHP Sail 애플리케이션은 `https://localhost`로 접속하는 것이 권장됩니다. `https://127.0.0.1` 사용 시 추가 구성이 필요하며, [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP 사용

FrankenPHP의 공식 Docker 이미지를 활용하면 성능이 향상되고, 정적 설치에서는 사용할 수 없는 추가 확장 기능을 사용할 수 있습니다. 또한, 공식 Docker 이미지는 Windows 등 FrankenPHP가 기본적으로 지원하지 않는 플랫폼에서도 실행할 수 있게 해줍니다. FrankenPHP의 공식 Docker 이미지는 로컬 개발 및 운영 환경 모두에 적합합니다.

아래 Dockerfile 예시를 참고해 FrankenPHP 기반의 Laravel 애플리케이션의 컨테이너화를 시작할 수 있습니다.

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

개발 도중에는 아래와 같이 Docker Compose 파일을 이용합니다.

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달하면, Octane은 FrankenPHP의 자체 로거를 사용하고, 별도 설정이 없으면 구조화된 JSON 로그를 생성합니다.

FrankenPHP와 Docker 관련 더 자세한 정보는 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="frankenphp-caddyfile"></a>
#### 사용자 지정 Caddyfile 설정

FrankenPHP를 사용할 경우, Octane 시작 시 `--caddyfile` 옵션을 이용해 사용자 지정 Caddyfile을 지정할 수 있습니다.

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

이로써 FrankenPHP의 기본 설정을 넘어, 고급 라우팅, 미들웨어 추가, 커스텀 디렉티브 설정 등 다양한 항목을 자유롭게 구성할 수 있습니다. Caddyfile 문법과 옵션에 대한 자세한 내용은 [공식 Caddy 문서](https://caddyserver.com/docs/caddyfile)를 참고하시기 바랍니다.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go 언어로 만들어진 RoadRunner 바이너리가 기반입니다. RoadRunner 기반 Octane 서버를 처음 시작할 때, Octane이 RoadRunner 바이너리를 다운로드 및 설치할지 물어봅니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner 사용

[Laravel Sail](/docs/master/sail)로 개발할 계획이라면 아래와 같이 Octane과 RoadRunner 관련 패키지를 설치하세요.

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

그 다음, Sail shell을 시작해 `rr` 실행 파일을 이용하여 최신 Linux용 RoadRunner 바이너리를 받아야 합니다.

```shell
./vendor/bin/sail shell

# Sail shell 내에서...
./vendor/bin/rr get-binary
```

그리고 애플리케이션의 `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리에 실행 권한을 부여하고, Sail 이미지를 빌드합니다.

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 통해 아래와 같이 설치할 수 있습니다.

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 모듈을 설치해야 합니다. 보통 PECL을 이용해 아래와 같이 설치할 수 있습니다.

```shell
pecl install openswoole
```

Open Swoole을 사용해 Laravel Octane을 실행하면, Swoole에서 제공하는 동시 작업, 틱, 인터벌 등의 기능을 동일하게 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole 사용

> [!WARNING]
> Octane 애플리케이션을 Sail로 서비스하기 전에 반드시 Laravel Sail의 최신 버전을 사용하고, 프로젝트 루트 디렉터리에서 `./vendor/bin/sail build --no-cache`를 실행해야 합니다.

또는, [Laravel Sail](/docs/master/sail) 공식 Docker 기반 개발 환경을 이용해 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel Sail에는 기본적으로 Swoole 확장 모듈이 포함되어 있지만, `docker-compose.yml` 파일을 수정해야 합니다.

먼저, `docker-compose.yml` 파일의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane을 이용해 애플리케이션을 서비스하는 데 사용하는 명령어입니다.

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 빌드합니다.

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

Swoole은 `octane` 설정 파일에서 추가 설정 옵션을 지원합니다. 이러한 옵션들은 자주 변경할 필요가 없으므로, 기본 설정 파일에는 포함되어 있지 않습니다.

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```

<a name="serving-your-application"></a>
## 애플리케이션 서비스 시작 (Serving Your Application)

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 이용합니다.

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000` 으로 접속하면 애플리케이션을 확인할 수 있습니다.

<a name="keeping-octane-running-in-production"></a>
#### 운영 환경에서 Octane 유지 실행

Octane 애플리케이션을 운영 환경에 배포하는 경우, Supervisor 같은 프로세스 모니터링 도구를 사용해 Octane 서버가 항상 실행 중인지 반드시 확인해야 합니다. 아래는 Octane용 Supervisor 설정 파일 예시입니다.

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
### HTTPS를 통한 애플리케이션 서비스 시작

기본적으로 Octane에서 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일 내 `OCTANE_HTTPS` 환경 변수를 `true`로 지정하면, Octane은 Laravel이 모든 링크를 `https://`로 시작하게 합니다.

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 서비스 시작

> [!NOTE]
> 서버 설정이 익숙하지 않거나 모든 구성 작업을 직접 관리할 준비가 되어 있지 않다면, 완전 관리형 라라벨 Octane 환경을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 참고하세요.

운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache 같은 기존 웹 서버 뒤에서 서비스해야 합니다. 이렇게 하면 웹 서버가 정적 리소스(예: 이미지, 스타일시트 등)를 직접 서비스하고, SSL 인증서 종료도 관리할 수 있습니다.

아래 Nginx 예시에서는 정적 리소스는 Nginx가 직접 서비스하고, 나머지 요청은 8000번 포트에서 실행 중인 Octane 서버로 프록시합니다.

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
### 파일 변경 사항 감지

Octane 서버가 시작되면 애플리케이션이 한 번 메모리에 적재되기 때문에, 코드 파일을 수정해도 브라우저를 새로고침하면 바로 반영되지 않습니다. 예를 들어, `routes/web.php`에 라우트를 새로 추가해도 서버를 재시작하지 않으면 반영되지 않습니다. 편의를 위해 `--watch` 플래그를 사용하면 애플리케이션 파일이 변경될 때마다 Octane 서버를 자동으로 재시작하도록 할 수 있습니다.

```shell
php artisan octane:start --watch
```

이 기능을 사용하기 전 [Node](https://nodejs.org) 가 로컬 개발 환경에 설치되어 있는지 확인하고, [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 프로젝트에 설치하세요.

```shell
npm install --save-dev chokidar
```

감시해야 하는 파일 및 디렉터리는 애플리케이션의 `config/octane.php` 설정 파일 내 `watch` 옵션을 사용해 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정

기본적으로 Octane은 서버의 CPU 코어 개수만큼 애플리케이션 요청 워커를 생성합니다. 각 워커가 들어오는 HTTP 요청을 처리하게 됩니다. 워커 개수를 직접 지정하려면 `octane:start` 명령어에 `--workers` 옵션을 추가하세요.

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용하는 경우, ["task worker"](동시 작업) 개수도 추가로 지정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 개수 지정

불필요한 메모리 누수를 방지하기 위해, Octane은 기본적으로 워커가 500개의 요청을 처리하면 자동으로 재시작합니다. 이 숫자는 `--max-requests` 옵션으로 조정할 수 있습니다.

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
### 최대 실행 시간 지정

기본적으로 Laravel Octane은 각 요청의 최대 실행 시간을 애플리케이션의 `config/octane.php` 파일 내 `max_execution_time` 옵션에서 30초로 지정합니다.

```php
'max_execution_time' => 30,
```

이 설정은 요청이 몇 초간 실행 가능한지의 최대치를 의미하며, 초과 시 강제 종료됩니다. 이 값을 `0`으로 설정하면 실행 시간 제한이 아예 비활성화됩니다. 대용량 파일 업로드, 데이터 처리, 외부 API 호출 등 장시간 요청이 많은 애플리케이션에서 유용하게 사용할 수 있습니다.

> [!WARNING]
> `max_execution_time` 설정을 변경할 경우, 반영을 위해 Octane 서버를 재시작해야 합니다.

<a name="reloading-the-workers"></a>
### 워커 재시작

`octane:reload` 명령어를 사용하면 Octane 서버의 애플리케이션 워커를 정상적으로 재시작할 수 있습니다. 주로 코드 배포 후 새 코드를 메모리에 반영하기 위해 사용합니다.

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 정지

`octane:stop` Artisan 명령어를 이용해 Octane 서버를 정지할 수 있습니다.

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

현재 Octane 서버의 상태는 `octane:status` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에서 계속 실행하므로, 개발 시 몇 가지 주의점이 있습니다. 예를 들어, 서비스 프로바이더의 `register` 및 `boot` 메서드는 워커 부팅 시 한 번만 실행됩니다. 이후 들어오는 요청들은 항상 같은 애플리케이션 인스턴스를 사용하게 됩니다.

이로 인해, 애플리케이션 서비스 컨테이너 혹은 요청 객체를 어떤 객체의 생성자에서 주입(inject)할 경우, 해당 객체는 다음 요청에서 항상 "옛날" 컨테이너나 요청을 참조할 수 있습니다.

Octane은 기본적으로 라라벨 프레임워크의 상태는 요청마다 잘 초기화해주지만, 여러분의 애플리케이션에서 만들어진 글로벌 상태까지는 자동으로 관리하지 못합니다. Octane에 맞는 개발 방법을 익혀 두세요. 아래에서 주로 많이 마주치는 문제 상황들을 다루겠습니다.

<a name="container-injection"></a>
### 컨테이너 주입

일반적으로 애플리케이션 서비스 컨테이너 또는 HTTP 요청 인스턴스를 다른 객체의 생성자에 주입하는 것은 피하는 것이 좋습니다. 예를 들어, 아래 바인딩은 전체 애플리케이션 서비스 컨테이너를 싱글톤 객체에 주입하고 있습니다.

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

이 예시에서, `Service` 인스턴스가 애플리케이션 부팅 과정에서 생성되면, 컨테이너가 서비스에 주입되고 그 같은 컨테이너가 이후 요청들에도 계속 사용됩니다. 상황에 따라 문제를 일으키지 않을 수도 있으나, 컨테이너에 나중에 바인딩된 값이나 요청에 따라 바뀌는 값이 누락될 수 있습니다.

해결 방법은 이 바인딩을 싱글톤이 아닌 일반 바인딩으로 바꾸거나, 항상 최신 컨테이너 인스턴스를 반환하는 클로저를 주입하는 것입니다.

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환하므로 안전하게 활용할 수 있습니다.

<a name="request-injection"></a>
### 요청 주입

서비스 컨테이너와 마찬가지로, HTTP 요청 인스턴스를 다른 객체 생성자에 주입하는 것도 일반적으로 피해야 합니다. 아래 예시처럼 바인딩이 싱글톤 객체에 전체 요청을 주입하는 방법도 문제가 될 수 있습니다.

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

위에서처럼 `Service` 인스턴스가 처음 생성될 때 주입된 요청 인스턴스가 이후 모든 요청에서 그대로 남아 있어, 헤더, 입력값, 쿼리스트링 등 요청 데이터가 올바르게 동작하지 않습니다.

이 문제도 바인딩을 일반 객체로 바꾸거나, 요청을 항상 동적으로 반환하는 클로저를 주입할 수 있습니다. 혹은, 가장 추천되는 방식은 객체가 필요로 하는 요청 정보를 메서드의 인자로 런타임에 전달하는 것입니다.

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// 또는...

$service->method($request->input('name'));
```

글로벌 `request` 헬퍼는 항상 현재 처리 중인 요청 인스턴스를 반환하므로, 애플리케이션 전반에서 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드 및 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트로 사용하는 것은 괜찮습니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

설정 저장소 인스턴스를 다른 객체 컨스트럭터에 주입하는 것도 역시 주의가 필요합니다. 예를 들어, 아래 바인딩은 설정 저장소 인스턴스를 싱글톤 객체에 주입합니다.

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

이 경우, 만약 요청 사이에 설정값이 변경된다면 이 서비스는 새로운 값을 사용할 수 없습니다. 항상 최초 주입된 저장소 인스턴스만 참조하게 되기 때문입니다.

이때도 바인딩을 일반 객체로 바꾸거나, 설정 저장소 클로저를 동적으로 주입해야 합니다.

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

글로벌 `config` 헬퍼는 항상 최신 설정 저장소를 반환하므로, 애플리케이션 내 어느 곳에서나 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

Octane은 요청 간에도 애플리케이션을 메모리에 유지하므로, 정적 변수와 같이 메모리에 남아있는 배열에 데이터를 추가할 경우 메모리 누수가 발생할 수 있습니다. 예를 들어 아래 컨트롤러는 static `$data` 배열에 데이터를 계속 추가하므로 메모리가 점차 증가합니다.

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

애플리케이션을 개발할 때 이런 유형의 메모리 누수가 발생하지 않도록 각별히 유의해야 합니다. 새 메모리 누수가 생기지 않도록 로컬 개발 환경에서 애플리케이션의 메모리 사용량을 주기적으로 모니터링하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 경우, Octane의 경량 백그라운드 태스크 기능을 통해 여러 작업을 동시에 실행할 수 있습니다. Octane의 `concurrently` 메서드를 이용해 다음과 같이 작성하면, PHP 배열 디스트럭처링(Array Destructuring)과 결합해 각 결과를 편리하게 사용할 수 있습니다.

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```

Octane의 동시 작업은 Swoole의 "task worker"가 처리하며, 요청을 처리하는 프로세스와는 별도 프로세스에서 실행됩니다. 동시 작업을 처리할 워커 수는 `octane:start` 명령어의 `--task-workers` 옵션으로 정할 수 있습니다.

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드 사용 시 Swoole 태스크 시스템의 제한으로 인해 1024개 이하의 태스크만 등록할 수 있습니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick) 및 인터벌(Interval) (Ticks and Intervals)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 경우, 지정된 초마다 "틱" 작업을 실행하도록 등록할 수 있습니다. `tick` 메서드를 이용해 틱 콜백을 등록할 수 있으며, 첫 번째 인자는 틱 이름(문자열), 두 번째는 호출될 콜러블입니다.

예를 들어 10초마다 실행될 클로저를 등록할 수 있습니다. 보통 이 방법은 서비스 프로바이더의 `boot` 메서드에서 호출됩니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면, Octane 서버 시작 시 틱 콜백을 즉시 한 번 실행하고, 그 이후 지정한 초마다 반복 실행할 수도 있습니다.

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole 사용 시 Octane 캐시 드라이버를 활용할 수 있으며, 초당 200만 건 이상의 읽기/쓰기 속도를 제공합니다. 매우 빠른 캐싱 레이어가 필요한 애플리케이션에 적합합니다.

이 캐시는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table) 기반이며, 서버 내 모든 워커가 동일한 캐시 데이터를 공유할 수 있습니다. 단, 서버가 재시작되면 캐시 데이터는 모두 사라집니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에서 허용되는 최대 엔트리 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 인터벌 (Cache Intervals)

Laravel의 기본 캐시 시스템 메서드 외에도, Octane 캐시 드라이버는 간격 기반(Interval based) 캐시를 지원합니다. 이런 캐시는 지정된 간격마다 자동 갱신되며, 보통 서비스 프로바이더의 `boot` 메서드에서 등록합니다. 아래 예시는 5초마다 갱신되는 캐시입니다.

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)가 필요합니다.

Swoole을 사용할 경우, 자신만의 Swoole 테이블을 자유롭게 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 처리량을 보장하며, 서버의 모든 워커에서 동일한 데이터를 읽고 쓸 수 있습니다. 다만, 서버가 재시작되면 테이블의 데이터는 모두 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 배열에 정의하면 됩니다. 아래는 최대 1000행을 저장하도록 미리 구성된 테이블 예시이며, 문자열 컬럼의 최대 크기는 아래와 같이 `컬럼 타입:크기`로 지정할 수 있습니다.

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

테이블에 접근하려면 `Octane::table` 메서드를 사용하면 됩니다.

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
