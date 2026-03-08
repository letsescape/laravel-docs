# Laravel Reverb (Laravel Reverb)

- [소개](#introduction)
- [설치](#installation)
- [구성](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
    - [허용된 오리진](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션 환경에서 Reverb 실행](#production)
    - [열린 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 매우 빠르고 확장 가능한 실시간 WebSocket 통신을 라라벨 애플리케이션에 직접 제공하며, Laravel의 기존 [이벤트 브로드캐스팅 도구](/docs/12.x/broadcasting)와 원활하게 통합할 수 있습니다.

<a name="installation"></a>
## 설치

Reverb는 `install:broadcasting` Artisan 명령어를 사용하여 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 구성

내부적으로 `install:broadcasting` Artisan 명령어는 `reverb:install` 명령어를 실행하여, 합리적인 기본 구성 옵션과 함께 Reverb를 설치합니다. 구성 변경이 필요한 경우, Reverb의 환경 변수 또는 `config/reverb.php` 구성 파일을 수정하여 설정할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명

Reverb에 연결을 수립하기 위해서는 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명(application credentials)이 교환되어야 합니다. 이 자격 증명은 서버에 설정되며, 클라이언트 요청을 검증하는 데 사용됩니다. 다음과 같은 환경 변수를 사용해 자격 증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 오리진

클라이언트 요청이 허용되는 오리진(origin)을 지정하려면, `config/reverb.php` 구성 파일의 `apps` 섹션에 있는 `allowed_origins` 구성 값을 업데이트하면 됩니다. 허용된 오리진에 포함되지 않은 오리진에서의 모든 요청은 거부됩니다. 모든 오리진을 허용하려면 `*`을 사용할 수 있습니다:

```php
'apps' => [
    [
        'app_id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]
```

<a name="additional-applications"></a>
### 추가 애플리케이션

일반적으로 Reverb는 설치된 애플리케이션 전용 WebSocket 서버 역할을 합니다. 하지만, 한 번의 Reverb 설치로 여러 애플리케이션을 지원할 수도 있습니다.

예를 들어, 하나의 Laravel 애플리케이션이 여러 다른 애플리케이션에 WebSocket 연결을 제공하도록 Reverb를 사용할 수 있습니다. 이를 위해 `config/reverb.php` 구성 파일에서 여러 개의 `apps`를 정의하면 됩니다:

```php
'apps' => [
    [
        'app_id' => 'my-app-one',
        // ...
    ],
    [
        'app_id' => 'my-app-two',
        // ...
    ],
],
```

<a name="ssl"></a>
### SSL

대부분의 경우, 보안 WebSocket 연결은 (Nginx 등) 상위 웹 서버에서 처리된 후, 요청이 Reverb 서버로 프록시됩니다.

하지만, 로컬 개발 중과 같이 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 때도 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/12.x/valet)를 사용하며 애플리케이션에 [secure 명령어](/docs/12.x/valet#securing-sites)를 실행한 경우, 해당 사이트용으로 생성된 Herd/Valet 인증서를 활용하여 Reverb 연결을 보호할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나, Reverb 서버를 시작할 때 명시적으로 `hostname` 옵션을 전달하십시오:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd 및 Valet 도메인은 `localhost`로 해석되기 때문에, 위 명령을 실행하면 `wss://laravel.test:8080`을 통한 보안 WebSocket 프로토콜(`wss`)로 Reverb 서버에 접근할 수 있습니다.

인증서를 수동으로 선택하려면, 애플리케이션의 `config/reverb.php` 파일에서 `tls` 옵션을 정의할 수 있습니다. `tls` 옵션 배열에는 [PHP의 SSL context 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 지정할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행

Reverb 서버는 `reverb:start` Artisan 명령어로 실행할 수 있습니다:

```shell
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되므로, 모든 네트워크 인터페이스에서 접근 가능합니다.

사용자 지정 호스트나 포트를 지정하려면, 서버 시작 시 `--host` 및 `--port` 옵션을 사용하면 됩니다:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 구성 파일에서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST` 및 `REVERB_PORT`와 혼동하지 않아야 합니다. 전자는 Reverb 서버 자체를 실행할 호스트와 포트를 지정하며, 후자는 Laravel이 브로드캐스트 메시지를 보낼 주소를 지정합니다. 예를 들어, 프로덕션 환경에서는 공개된 Reverb 호스트명(예: 포트 443)에서 요청을 받아, 내부의 `0.0.0.0:8080`에서 작동하는 Reverb 서버로 라우팅할 수 있습니다. 이 경우 환경 변수 설정은 다음과 같습니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능 향상을 위해, Reverb는 기본적으로 어떠한 디버그 정보도 출력하지 않습니다. Reverb 서버를 통해 전달되는 데이터 스트림을 확인하려면, `reverb:start` 명령에 `--debug` 옵션을 추가하십시오:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 지속적으로 실행되는(long-running) 프로세스이므로, 코드 변경 사항이 바로 반영되지 않습니다. 코드를 수정한 후에는 반드시 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

`reverb:restart` 명령어는 서버를 중지하기 전에 모든 연결을 정상적으로 종료(graceful termination)합니다. Supervisor와 같은 프로세스 관리자를 사용하여 Reverb를 실행 중이라면, 모든 연결 종료 후 프로세스 관리자가 자동으로 서버를 재시작합니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링

Reverb는 [Laravel Pulse](/docs/12.x/pulse)와의 통합 기능을 통해 모니터링할 수 있습니다. Reverb의 Pulse 통합을 활성화하면, 서버에서 처리 중인 연결 수와 메시지 수를 추적할 수 있습니다.

통합을 활성화하려면, 우선 [Pulse를 설치](/docs/12.x/pulse#installation)했는지 확인하십시오. 그런 다음, Reverb의 레코더(recorder)를 애플리케이션의 `config/pulse.php` 구성 파일에 추가하면 됩니다:

```php
use Laravel\Reverb\Pulse\Recorders\ReverbConnections;
use Laravel\Reverb\Pulse\Recorders\ReverbMessages;

'recorders' => [
    ReverbConnections::class => [
        'sample_rate' => 1,
    ],

    ReverbMessages::class => [
        'sample_rate' => 1,
    ],

    // ...
],
```

다음으로, 각 레코더의 Pulse 카드(card)를 [Pulse 대시보드](/docs/12.x/pulse#dashboard-customization)에 추가하십시오:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. 이 정보가 Pulse 대시보드에 올바르게 렌더링되려면, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. [수평 확장된](#scaling) 구성에서는 단 한 서버에서만 이 데몬을 실행하면 됩니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행

WebSocket 서버의 지속적인 실행 특성 때문에, 서버와 호스팅 환경을 최적화하여 사용할 수 있는 리소스 범위 내에서 Reverb 서버가 최적의 연결 수를 처리할 수 있도록 해야 합니다.

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com)는 Laravel Reverb 클러스터가 제공하는 완전 관리형 WebSocket 인프라를 통해, 인프라 관리 없이 Reverb 기반 애플리케이션을 스케일 확장 및 배포할 수 있습니다.

<a name="open-files"></a>
### 열린 파일

각 WebSocket 연결은 클라이언트나 서버가 연결을 종료할 때까지 메모리에 유지됩니다. 유닉스 및 유닉스 계열 환경에서는 각 연결이 하나의 파일로 간주됩니다. 하지만, 운영체제와 애플리케이션 레벨 모두에서 열 수 있는 파일의 개수에는 제한이 있습니다.

<a name="operating-system"></a>
#### 운영체제

유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 열린 파일 개수를 확인할 수 있습니다:

```shell
ulimit -n
```

이 명령은 사용자의 열린 파일 제한을 표시합니다. 값을 변경하려면 `/etc/security/limits.conf` 파일을 수정하십시오. 예를 들어, `forge` 사용자에 대해 열린 파일의 최대값을 10,000개로 설정하려면 다음과 같이 하면 됩니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

내부적으로 Reverb는 ReactPHP 이벤트 루프를 사용하여 서버에서 WebSocket 연결을 관리합니다. 기본적으로 이 이벤트 루프는 별도의 확장 없이 사용 가능한 `stream_select`를 사용하여 동작합니다. 하지만, `stream_select`는 일반적으로 1,024개의 열린 파일까지만 지원합니다. 따라서, 1,000개 이상의 동시 연결을 처리하려면 동일한 제약에 묶이지 않는 대안 이벤트 루프를 사용해야 합니다.

`ext-uv` 확장이 설치된 경우 Reverb는 자동으로 `ext-uv` 기반 루프로 전환합니다. 해당 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 경우, Reverb는 서버의 외부 서비스용 포트가 아닌 곳에서 실행됩니다. 따라서, Reverb로 트래픽을 라우팅하려면 리버스 프록시(reverse proxy)를 구성해야 합니다. 예를 들어, Reverb가 `0.0.0.0`의 8080 포트에서 실행 중이고 서버에서 Nginx 웹 서버를 사용한다면, 다음과 같이 Nginx 사이트 구성 파일을 설정할 수 있습니다:

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://0.0.0.0:8080;
    }

    ...
}
```

> [!WARNING]
> Reverb는 `/app`에서 WebSocket 연결을 수신하고, `/apps`에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버는 이 두 URI 경로 모두를 제공할 수 있어야 합니다. [Laravel Forge](https://forge.laravel.com)를 사용하여 서버를 관리하는 경우, 기본적으로 Reverb 서버가 올바르게 구성됩니다.

일반적으로, 웹 서버는 서버 과부하를 막기 위해 허용된 연결 개수에 제한을 둡니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면, `nginx.conf` 파일에서 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 수정해야 합니다:

```nginx
user forge;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
worker_rlimit_nofile 10000;

events {
  worker_connections 10000;
  multi_accept on;
}
```

위 설정은 프로세스당 최대 10,000개의 Nginx 워커를 생성할 수 있게 합니다. 또한, Nginx의 열린 파일 제한도 10,000으로 설정됩니다.

<a name="ports"></a>
### 포트

유닉스 기반 운영체제는 서버에서 열 수 있는 포트의 개수에도 제한이 있습니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력에서 60,999 - 32,768 = 28,231개 포트까지 동시에 연결이 가능하다는 것을 알 수 있습니다. 각 연결마다 사용 가능한 포트가 필요하기 때문입니다. 더 많은 연결을 지원하려면 [수평 확장](#scaling)을 권장하며, 포트 개수를 늘려야 할 경우 서버의 `/etc/sysctl.conf` 파일에서 허용된 포트 범위를 조정하면 됩니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우, Supervisor와 같은 프로세스 관리자를 사용하여 Reverb 서버가 항상 실행되도록 하는 것이 좋습니다. Supervisor로 Reverb를 관리할 경우, `supervisor.conf` 파일의 `minfds` 설정을 조정해서 Supervisor가 Reverb 서버의 연결을 처리할 만큼 충분한 파일을 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

하나의 서버가 처리할 수 있는 연결 수를 초과하는 경우, Reverb 서버를 수평 확장하여 동작할 수 있습니다. Redis의 publish/subscribe 기능을 활용하여, Reverb는 여러 서버에 걸쳐 연결을 관리할 수 있습니다. 한 Reverb 서버로 메시지가 들어오면, 해당 서버는 Redis를 이용해 모든 다른 서버로 해당 메시지를 보냅니다.

수평 확장을 활성화하려면, 애플리케이션의 `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정해야 합니다:

```env
REVERB_SCALING_ENABLED=true
```

그리고 모든 Reverb 서버가 통신할 수 있는 전용 중앙 Redis 서버가 필요합니다. Reverb는 [애플리케이션에 기본으로 구성된 Redis 연결](/docs/12.x/redis#configuration)을 사용하여 모든 Reverb 서버에 메시지를 퍼블리시합니다.

Reverb 스케일링 옵션을 활성화하고 Redis 서버를 구성했다면, Redis 서버와 통신 가능한 여러 대의 서버에서 `reverb:start` 명령어를 실행하기만 하면 됩니다. 이 Reverb 서버들은 로드 밸런서 뒤에 둬서, 수신 요청이 여러 서버에 고르게 분산되도록 배치합니다.

<a name="events"></a>
## 이벤트

Reverb는 연결 및 메시지 처리의 라이프사이클 동안 내부적으로 이벤트를 디스패치(dispatch)합니다. 이러한 이벤트에 [리스너를 등록](/docs/12.x/events)하여, 연결 관리나 메시지 교환 시 특정 동작을 수행할 수 있습니다.

Reverb에서 디스패치되는 주요 이벤트는 다음과 같습니다:

#### `Laravel\Reverb\Events\ChannelCreated`

채널이 생성될 때 디스패치됩니다. 일반적으로 첫 번째 연결이 특정 채널에 가입(서브스크립션)할 때 발생합니다. 이 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달받습니다.

#### `Laravel\Reverb\Events\ChannelRemoved`

채널이 삭제될 때 디스패치됩니다. 이는 마지막 연결이 채널에서 탈퇴(언서브스크립션)할 때 발생합니다. 이 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달받습니다.

#### `Laravel\Reverb\Events\ConnectionPruned`

서버에 의해 오래된(stale) 연결이 정리(prune)될 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스를 전달받습니다.

#### `Laravel\Reverb\Events\MessageReceived`

클라이언트 연결로부터 메시지를 수신할 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`를 전달받습니다.

#### `Laravel\Reverb\Events\MessageSent`

클라이언트 연결에 메시지가 전송될 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`를 전달받습니다.
