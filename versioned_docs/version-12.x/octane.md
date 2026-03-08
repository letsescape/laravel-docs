# Laravel Octane (Laravel Octane)

- [소개](#introduction)
- [설치](#installation)
- [서버 사전 준비 사항](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [애플리케이션 서비스](#serving-your-application)
    - [HTTPS로 애플리케이션 서비스](#serving-your-application-via-https)
    - [Nginx로 애플리케이션 서비스](#serving-your-application-via-nginx)
    - [파일 변경 감지](#watching-for-file-changes)
    - [워커 개수 지정](#specifying-the-worker-count)
    - [최대 요청 횟수 지정](#specifying-the-max-request-count)
    - [최대 실행 시간 지정](#specifying-the-max-execution-time)
    - [워커 재시작](#reloading-the-workers)
    - [서버 중지](#stopping-the-server)
- [의존성 주입과 Octane](#dependency-injection-and-octane)
    - [컨테이너 주입](#container-injection)
    - [Request 주입](#request-injection)
    - [설정 저장소 주입](#configuration-repository-injection)
- [메모리 누수 관리](#managing-memory-leaks)
- [동시 작업](#concurrent-tasks)
- [틱(Tick)과 간격(Interval)](#ticks-and-intervals)
- [Octane 캐시](#the-octane-cache)
- [테이블](#tables)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Octane](https://github.com/laravel/octane)는 [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), [RoadRunner](https://roadrunner.dev) 등 고성능 애플리케이션 서버를 활용하여 애플리케이션의 성능을 극대화합니다. Octane은 애플리케이션을 한 번 부팅한 뒤 메모리에 유지하고, 초고속으로 요청을 처리합니다.

<a name="installation"></a>
## 설치 (Installation)

Octane은 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require laravel/octane
```

Octane 설치 후 `octane:install` Artisan 명령어를 실행하여 Octane의 설정 파일을 애플리케이션에 추가할 수 있습니다:

```shell
php artisan octane:install
```

<a name="server-prerequisites"></a>
## 서버 사전 준비 사항 (Server Prerequisites)

<a name="frankenphp"></a>
### FrankenPHP

[FrankenPHP](https://frankenphp.dev)는 Go 언어로 작성된 PHP 애플리케이션 서버로, early hints, Brotli, Zstandard 압축 등 최신 웹 기능을 지원합니다. Octane과 함께 FrankenPHP를 서버로 선택하면, 필요 시 Octane이 FrankenPHP 바이너리를 자동으로 다운로드 및 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 FrankenPHP

[Larael Sail](/docs/12.x/sail)을 사용하여 애플리케이션을 개발할 계획이라면, 다음 명령어들로 Octane 및 FrankenPHP를 설치하세요:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```

이어 `octane:install` Artisan 명령어를 사용해 FrankenPHP 바이너리를 설치합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```

마지막으로, 애플리케이션의 `docker-compose.yml` 파일 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수에는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```

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

보통 FrankenPHP Sail 애플리케이션은 `https://localhost`로 접근해야 합니다. `https://127.0.0.1`로 접근하려면 추가 설정이 필요하며, 이는 [권장되지 않습니다](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker).

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP

FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 향상되고, 정적 설치 버전에서는 포함되지 않은 추가 확장 기능도 사용할 수 있습니다. 또한 공식 Docker 이미지는 FrankenPHP가 기본적으로 지원하지 않는 Windows 등 다양한 플랫폼에서 구동할 수 있도록 지원합니다. FrankenPHP의 공식 Docker 이미지는 로컬 개발과 운영 환경 모두에 적합합니다.

FrankenPHP 기반의 Laravel 애플리케이션 컨테이너화의 시작점으로 아래 Dockerfile을 참고할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```

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

`php artisan octane:start` 명령어에 `--log-level` 옵션을 명시적으로 전달하면, Octane은 FrankenPHP의 기본 로거를 사용하며, 별도의 설정이 없다면 구조화된 JSON 로그를 생성합니다.

Docker로 FrankenPHP를 실행하는 방법은 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참고하세요.

<a name="frankenphp-caddyfile"></a>
#### 커스텀 Caddyfile 설정

FrankenPHP를 사용할 때, Octane을 시작할 때 `--caddyfile` 옵션을 활용해 사용자 지정 Caddyfile을 지정할 수 있습니다:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```

이렇게 하면 기본 설정을 넘어 사용자 지정 미들웨어 추가, 고급 라우팅 구성, 사용자 지정 지시어 설정 등 FrankenPHP의 구성을 세밀하게 제어할 수 있습니다. Caddyfile 문법 및 설정에 관한 자세한 내용은 [공식 Caddy 문서](https://caddyserver.com/docs/caddyfile)를 참고하세요.

<a name="roadrunner"></a>
### RoadRunner

[RoadRunner](https://roadrunner.dev)는 Go로 작성된 RoadRunner 바이너리 기반으로 동작합니다. RoadRunner 기반 Octane 서버를 처음 시작할 때 Octane이 자동으로 RoadRunner 바이너리를 다운로드하고 설치할 수 있도록 안내합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 RoadRunner

[Larael Sail](/docs/12.x/sail)을 사용하여 애플리케이션을 개발할 경우, Octane과 RoadRunner를 다음 명령어로 설치합니다:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```

이어 Sail 셸을 시작하고, 최신 리눅스 기반 RoadRunner 바이너리를 얻으려면 `rr` 실행 파일을 사용합니다:

```shell
./vendor/bin/sail shell

# Sail 셸 내부에서...
./vendor/bin/rr get-binary
```

`docker-compose.yml` 내 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용하는 명령어입니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 `rr` 바이너리의 실행 권한을 부여하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```

<a name="swoole"></a>
### Swoole

Swoole 애플리케이션 서버로 Laravel Octane 애플리케이션을 서비스하려면 Swoole PHP 확장 기능을 설치해야 합니다. 보통 PECL을 통해 설치할 수 있습니다:

```shell
pecl install swoole
```

<a name="openswoole"></a>
#### Open Swoole

Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 기능을 설치해야 합니다. 보통 PECL을 통해 설치합니다:

```shell
pecl install openswoole
```

Laravel Octane을 Open Swoole과 함께 사용할 경우, 동시 작업, 틱, 간격 등 Swoole과 동일한 기능을 사용할 수 있습니다.

<a name="swoole-via-laravel-sail"></a>
#### Laravel Sail을 통한 Swoole

> [!WARNING]
> Sail로 Octane 애플리케이션을 서비스하기 전, Laravel Sail의 최신 버전이 설치되어 있는지 확인하고, 애플리케이션 루트에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는 [Laravel Sail](/docs/12.x/sail)이라는 공식 Docker 기반 개발 환경을 사용하여 Swoole 기반 Octane 애플리케이션을 개발할 수도 있습니다. Laravel Sail에는 기본적으로 Swoole 확장이 포함되어 있습니다. 하지만 Sail에서 사용하는 `docker-compose.yml` 파일에는 별도 설정이 필요합니다.

먼저 `docker-compose.yml`의 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 변수에는 Sail이 PHP 개발 서버 대신 Octane으로 애플리케이션을 서비스할 때 사용할 명령어가 들어갑니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```

마지막으로 Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```

<a name="swoole-configuration"></a>
#### Swoole 설정

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
## 애플리케이션 서비스 (Serving Your Application)

Octane 서버는 `octane:start` Artisan 명령어로 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 설정 파일의 `server` 옵션에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```

기본적으로 Octane은 8000번 포트에서 서버를 시작하므로, 웹 브라우저에서 `http://localhost:8000`을 통해 애플리케이션에 접근할 수 있습니다.

<a name="keeping-octane-running-in-production"></a>
#### 운영 환경에서 Octane 실행 유지

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
### HTTPS로 애플리케이션 서비스

기본적으로 Octane으로 실행되는 애플리케이션은 `http://`가 붙은 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일에서 `OCTANE_HTTPS` 환경 변수를 `true`로 설정하면 HTTPS로 서비스할 때 모든 생성된 링크에 `https://`가 자동으로 접두사로 붙습니다:

```php
'https' => env('OCTANE_HTTPS', false),
```

<a name="serving-your-application-via-nginx"></a>
### Nginx로 애플리케이션 서비스

> [!NOTE]
> 서버 설정을 직접 관리하거나 다양한 서비스를 직접 구성하는 것에 익숙하지 않다면, [Laravel Cloud](https://cloud.laravel.com)를 참고하세요. Laravel Cloud는 완전 관리형 Laravel Octane 서비스를 제공합니다.

운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 서비스하는 것이 좋습니다. 이렇게 하면 정적 자산(이미지, 스타일시트 등) 서비스와 SSL 인증서 종료를 전통적 웹 서버에서 처리할 수 있습니다.

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
### 파일 변경 감지

Octane 서버가 시작될 때 애플리케이션이 한 번 메모리에 로드되므로, 소스 코드를 수정해도 브라우저 새로고침만으로 변경 내용이 반영되지 않습니다. 예를 들어, `routes/web.php`에 새로운 라우트를 추가하면 서버를 재시작해야 반영됩니다. 편의상, `--watch` 플래그를 사용하면 애플리케이션 내 파일 변경 시 Octane이 자동으로 서버를 재시작하도록 할 수 있습니다:

```shell
php artisan octane:start --watch
```

이 기능을 사용하려면, 먼저 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 합니다. 또한, 프로젝트 내에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

감시할 디렉터리와 파일은 애플리케이션의 `config/octane.php` 설정 파일의 `watch` 옵션으로 지정할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 워커 개수 지정

기본적으로 Octane은 시스템의 CPU 코어 개수만큼 애플리케이션 요청 워커를 시작합니다. 이 워커들은 HTTP 요청을 처리합니다. 워커 개수를 수동으로 지정하려면 `octane:start` 명령어 실행 시 `--workers` 옵션을 사용할 수 있습니다:

```shell
php artisan octane:start --workers=4
```

Swoole 애플리케이션 서버를 사용하는 경우, ["task workers"](#concurrent-tasks)도 개수 지정이 가능합니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

<a name="specifying-the-max-request-count"></a>
### 최대 요청 횟수 지정

메모리 누수 방지를 위해, Octane은 각 워커가 500개의 요청을 처리하면 자동으로 워커를 재시작합니다. 이 수치는 `--max-requests` 옵션으로 조정할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```

<a name="specifying-the-max-execution-time"></a>
### 최대 실행 시간 지정

기본적으로 Laravel Octane은 애플리케이션의 `config/octane.php` 설정 파일의 `max_execution_time` 옵션을 통해 요청별 최대 실행 시간을 30초로 지정합니다:

```php
'max_execution_time' => 30,
```

이 설정은 각 요청이 종료되기 전 허용되는 최대 초(second)를 의미합니다. 이 값을 `0`으로 설정하면 실행 시간 제한이 해제됩니다. 이 옵션은 파일 업로드, 데이터 처리, 외부 서비스 API 호출 등 장시간 실행되는 요청을 처리하는 애플리케이션에서 특히 유용합니다.

> [!WARNING]
> `max_execution_time` 설정을 변경했다면, 변경 사항을 적용하기 위해 Octane 서버를 반드시 재시작해야 합니다.

<a name="reloading-the-workers"></a>
### 워커 재시작

`octane:reload` 명령어를 사용하면 Octane 서버의 애플리케이션 워커를 안전하게 재시작할 수 있습니다. 일반적으로 코드 배포 후, 새로 배포된 코드가 메모리에 로드되고 이후의 요청에 사용될 수 있도록 이 명령어를 실행해야 합니다:

```shell
php artisan octane:reload
```

<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어로 Octane 서버를 중지시킬 수 있습니다:

```shell
php artisan octane:stop
```

<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령어로 Octane 서버의 현재 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```

<a name="dependency-injection-and-octane"></a>
## 의존성 주입과 Octane (Dependency Injection and Octane)

Octane은 애플리케이션을 한 번 부팅한 후, 요청을 처리하는 동안 메모리에 유지합니다. 이로 인해 애플리케이션 구성시 고려해야 할 몇 가지 유의 사항이 있습니다. 예를 들어, 애플리케이션의 서비스 프로바이더 내 `register`와 `boot` 메서드는 워커가 처음 부팅될 때 딱 한 번만 실행됩니다. 이후의 모든 요청은 동일한 애플리케이션 인스턴스를 재사용하게 됩니다.

이 점을 염두에 두고, 애플리케이션 서비스 컨테이너나 request를 객체 생성자에 주입하는 것은 주의해야 합니다. 만약 그렇게 해두면, 해당 객체가 이후 요청에서도 오래된 컨테이너나 request 인스턴스를 참조할 수 있습니다.

Octane은 Laravel의 핵심 프레임워크 상태는 요청 사이마다 자동으로 리셋합니다. 하지만 애플리케이션이 생성한 전역 상태까지 항상 자동으로 리셋할 수는 없으므로, Octane 친화적인(Octane friendly) 방식으로 애플리케이션을 설계해야 합니다. 아래 예시들은 Octane 사용 시 자주 문제가 되는 상황들을 설명합니다.

<a name="container-injection"></a>
### 컨테이너 주입

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

이 경우, 애플리케이션 부팅 시 `Service` 인스턴스가 생성되면 서비스 컨테이너가 주입되고, 이후에도 해당 객체가 동일한(초기) 컨테이너를 계속 참조합니다. 이는 애플리케이션마다 반드시 문제가 되는 것은 아니지만, 부팅 후 나중 혹은 별도 요청에서 추가된 바인딩을 인식하지 못하는 등의 예기치 않은 상황을 유발할 수 있습니다.

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

글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 최신 애플리케이션 컨테이너를 반환합니다.

<a name="request-injection"></a>
### Request 주입

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

이 경우에도 애플리케이션 부팅 시 생성된 request 인스턴스가 계속 남아, 모든 이후 요청에서 해당 request(초기 요청의 헤더, 입력값, 쿼리스트링 등)를 참조하게 되어 올바른 데이터가 전달되지 않습니다.

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

// 또는...

$service->method($request->input('name'));
```

글로벌 `request` 헬퍼는 항상 현재 애플리케이션이 처리 중인 최신 request를 반환하므로 안전하게 사용할 수 있습니다.

> [!WARNING]
> 컨트롤러 메서드나 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입힌트하는 것은 안전합니다.

<a name="configuration-repository-injection"></a>
### 설정 저장소 주입

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

이 경우, 요청 사이에서 설정 값이 변경된다면 해당 서비스는 새로운 값을 가져올 수 없습니다(초기 저장소 인스턴스만 참조하기 때문입니다).

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

글로벌 `config` 헬퍼는 항상 최신 설정 저장소 인스턴스를 반환하므로 애플리케이션 내에서 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

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

애플리케이션을 구축할 때 이러한 메모리 누수 패턴이 생기지 않도록 각별히 주의해야 합니다. 로컬 개발 시 점검 도구 등을 통해 애플리케이션 메모리 사용량을 주기적으로 확인하는 것이 좋습니다.

<a name="concurrent-tasks"></a>
## 동시 작업 (Concurrent Tasks)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

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

동시 작업은 Swoole의 "task worker" 프로세스를 이용하며, 요청을 처리하는 프로세스와는 완전히 별도의 프로세스에서 실행됩니다. 동시 작업 워커 개수는 `octane:start` 명령어의 `--task-workers` 옵션으로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```

`concurrently` 메서드에 전달할 작업 개수는 Swoole의 과제 시스템(task system) 제한에 따라 1024개를 넘지 않도록 해야 합니다.

<a name="ticks-and-intervals"></a>
## 틱(Tick)과 간격(Interval)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 특정 초 간격마다 실행되는 "tick" 작업을 등록할 수 있습니다. `tick` 메서드로 콜백을 등록할 수 있고, 첫 번째 인자로 ticker의 이름(문자열), 두 번째 인자로 호출될 콜러블을 전달합니다.

아래 예시는 10초마다 closure를 실행하는 tick을 등록합니다. 일반적으로 이 메서드는 애플리케이션의 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```

`immediate` 메서드를 사용하면 Octane 서버가 부팅될 때 즉시 tick 콜백을 실행하고, 이후 지정된 간격마다 반복 실행하도록 할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```

<a name="the-octane-cache"></a>
## Octane 캐시 (The Octane Cache)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, Octane 캐시 드라이버를 사용할 수 있습니다. 이 드라이버는 최대 초당 200만 회의 읽기/쓰기 속도를 자랑하며, 극한의 캐싱이 필요한 애플리케이션에서 강력한 선택지입니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 기반으로 하며, 서버의 모든 워커가 캐시된 데이터에 접근할 수 있습니다. 단, 서버를 재시작하면 캐시된 데이터는 모두 초기화됩니다:

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```

> [!NOTE]
> Octane 캐시에 허용되는 최대 항목 수는 애플리케이션의 `octane` 설정 파일에서 지정할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 간격(Interval)

라라벨의 기본 캐시 시스템 메서드 외에도, Octane 캐시 드라이버는 간격 기반(interval based) 캐시 기능을 지원합니다. 이 캐시는 지정한 시간 간격마다 자동으로 최신 값으로 갱신되며, 보통 서비스 프로바이더의 `boot` 메서드 내에서 정의해야 합니다. 아래 예시는 5초마다 새 값으로 갱신되는 캐시를 만듭니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```

<a name="tables"></a>
## 테이블 (Tables)

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 경우, [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 직접 정의하고 사용할 수 있습니다. Swoole 테이블은 매우 높은 성능을 제공하며, 서버의 모든 워커가 테이블의 데이터에 접근할 수 있습니다. 단, 서버 재시작 시 테이블의 모든 데이터는 손실됩니다.

테이블은 애플리케이션의 `octane` 설정 파일 내 `tables` 설정 배열에 정의해야 합니다. 기본적으로 최대 1000개의 row를 허용하는 예시 테이블이 이미 준비되어 있습니다. 문자열 컬럼의 최대 크기는 타입 뒤에 바로 명시할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```

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
