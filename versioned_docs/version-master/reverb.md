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
    - [열린 파일 수](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Reverb](https://github.com/laravel/reverb)는 강력하고 확장성 높은 실시간 WebSocket 통신을 여러분의 Laravel 애플리케이션에 직접 구축할 수 있도록 하며, 기존의 [이벤트 브로드캐스팅 도구](/docs/master/broadcasting)와도 완벽하게 통합됩니다.

<a name="installation"></a>
## 설치

`install:broadcasting` Artisan 명령어를 사용하여 Reverb를 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
## 구성

백그라운드에서는, `install:broadcasting` Artisan 명령어가 실제로 `reverb:install` 명령어를 실행하여, 합리적인 기본 설정값으로 Reverb를 설치합니다. 추가로 설정을 변경하고 싶다면, Reverb의 환경 변수 또는 `config/reverb.php` 구성 파일을 직접 업데이트하여 조정할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명

Reverb에 연결하려면, 클라이언트와 서버 사이에서 Reverb "애플리케이션" 자격 증명을 교환해야 합니다. 이 자격 증명은 서버 측에서 설정되며, 클라이언트의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용해 자격 증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 허용된 오리진

클라이언트 요청이 어디에서 올 수 있는지 설정하려면, `config/reverb.php` 구성 파일의 `apps` 섹션 안에 있는 `allowed_origins` 값을 수정하면 됩니다. 허용된 오리진에 포함되지 않은 오리진에서의 요청은 거부됩니다. 모든 오리진을 허용하려면 `*`를 사용할 수 있습니다:

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

일반적으로 Reverb는 설치된 애플리케이션의 WebSocket 서버 역할만 하지만, 하나의 Reverb 설치로 여러 애플리케이션을 동시에 서비스하는 것도 가능합니다.

예를 들어, 하나의 Laravel 애플리케이션이 여러 애플리케이션에 WebSocket 연결을 제공하도록 Reverb를 구성하고 싶을 수 있습니다. 이를 위해서는, `config/reverb.php` 구성 파일에 여러 `apps`를 정의하면 됩니다:

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

대부분의 경우, 보안 WebSocket 연결은 업스트림 웹 서버(Nginx 등)가 요청을 Reverb 서버로 프록시하기 전에 처리합니다.

하지만, 예를 들어 로컬 개발 환경 등에서 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 때도 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/master/valet)에서 [secure 명령어](/docs/master/valet#securing-sites)를 실행한 경우라면, Herd/Valet가 생성한 인증서를 이용해 Reverb 연결을 보안 처리할 수 있습니다. 이를 위해서는, `REVERB_HOST` 환경 변수에 사이트의 호스트명을 설정하거나, Reverb 서버를 시작할 때 명시적으로 호스트명 옵션을 전달하면 됩니다:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd와 Valet 도메인은 `localhost`로 해석되므로, 위 명령어로 Reverb 서버를 실행하면 `wss://laravel.test:8080`과 같이 보안 WebSocket 프로토콜(`wss`)로 접속할 수 있습니다.

또한, `config/reverb.php` 구성 파일의 `tls` 옵션 배열을 통해 직접 인증서를 지정할 수도 있습니다. `tls` 옵션 배열에는 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 옵션을 설정할 수 있습니다:

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## 서버 실행

Reverb 서버는 `reverb:start` Artisan 명령어로 시작할 수 있습니다:

```shell
php artisan reverb:start
```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접속할 수 있습니다.

커스텀 호스트나 포트가 필요하다면, 서버 시작 시 `--host` 및 `--port` 옵션을 사용할 수 있습니다:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

또는, 애플리케이션의 `.env` 구성 파일에서 `REVERB_SERVER_HOST`, `REVERB_SERVER_PORT` 환경 변수를 정의할 수 있습니다.

여기서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT`는, 서버 자체가 바인딩되는 호스트와 포트를 지정하는 것이고, `REVERB_HOST`와 `REVERB_PORT`는 Laravel이 브로드캐스트 메시지를 어디로 전송할지 결정하도록 하는 값입니다. 예를 들어, 프로덕션 환경에서 퍼블릭 Reverb 호스트명을 포트 `443`에서 요청받아 이를 `0.0.0.0:8080`에서 작동하는 Reverb 서버로 라우팅하려면, 환경 변수는 아래처럼 설정해야 합니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### 디버깅

성능을 높이기 위해, Reverb는 기본적으로 어떤 디버그 정보도 출력하지 않습니다. Reverb 서버를 통과하는 데이터 스트림을 보고 싶다면, `reverb:start` 명령어에 `--debug` 옵션을 추가하여 사용할 수 있습니다:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 재시작

Reverb는 장시간 동작하는 프로세스이기 때문에, 코드 변경사항이 서버에 바로 반영되지 않습니다. 따라서 `reverb:restart` Artisan 명령어로 서버를 재시작해야 변경 내용이 적용됩니다.

`reverb:restart` 명령어는 서버를 멈추기 전에 모든 연결을 정상적으로 종료시켜 줍니다. 프로세스 매니저(Supervisor 등)로 Reverb를 실행 중이라면, 모든 연결이 종료된 후 프로세스 매니저가 서버를 자동으로 재시작해줍니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
## 모니터링

Reverb는 [Laravel Pulse](/docs/master/pulse)와의 통합을 통해 모니터링할 수 있습니다. Reverb의 Pulse 연동 기능을 활성화하면, 서버에서 처리되는 연결 수와 메시지 수를 추적할 수 있습니다.

통합을 활성화하려면, 먼저 [Pulse를 설치](/docs/master/pulse#installation)해야 합니다. 이후, 애플리케이션의 `config/pulse.php` 파일에 Reverb 관련 리코더를 추가합니다:

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

그 다음, 각각의 리코더에 Pulse 카드를 [Pulse 대시보드](/docs/master/pulse#dashboard-customization)에 추가합니다:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. 이 정보를 Pulse 대시보드에서 올바르게 렌더링하려면, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. [수평 확장](#scaling) 구성을 사용할 경우, 이 데몬은 한 대의 서버에서만 실행해야 합니다.

<a name="production"></a>
## 프로덕션 환경에서 Reverb 실행

WebSocket 서버의 장시간 실행 특성상, Reverb 서버가 서버 자원에 맞게 충분한 수의 연결을 처리할 수 있도록 서버 및 호스팅 환경을 최적화할 필요가 있습니다.

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com)는 Laravel Reverb 클러스터 기반의 완전 관리형 WebSocket 인프라를 제공하여, 인프라 관리 없이 확장 가능한 Reverb 기반 애플리케이션을 손쉽게 구축하고 배포할 수 있도록 지원합니다.

<a name="open-files"></a>
### 열린 파일 수

각 WebSocket 연결은, 클라이언트 또는 서버에서 연결을 끊을 때까지 메모리상에 유지됩니다. Unix 및 Unix 계열 환경에서는, 각 연결이 파일로 처리됩니다. 하지만 운영 체제 및 애플리케이션 수준에서 허용된 열린 파일 수에는 제한이 있습니다.

<a name="operating-system"></a>
#### 운영 체제

Unix 기반 운영 체제에서, `ulimit` 명령어로 허용된 열린 파일 수를 확인할 수 있습니다:

```shell
ulimit -n
```

이 명령어는 사용자별로 허용된 열린 파일 제한을 보여줍니다. 값을 변경하려면 `/etc/security/limits.conf` 파일을 수정합니다. 예를 들어, `forge` 사용자에 대한 최대 열린 파일 수를 10,000으로 설정하려면 다음과 같이 입력합니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### 이벤트 루프

Reverb는 내부적으로 서버의 WebSocket 연결을 관리하기 위해 ReactPHP 이벤트 루프를 사용합니다. 기본적으로 이 이벤트 루프는 `stream_select`를 기반으로 하며, 추가적인 확장 없이도 사용 가능합니다. 하지만 `stream_select`는 일반적으로 1,024개의 열린 파일만 다룰 수 있습니다. 따라서 1,000개가 넘는 동시 연결을 처리하려면 이와 같은 제한이 없는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 `ext-uv` 확장 기능이 사용 가능한 경우 자동으로 해당 루프로 전환됩니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv
```

<a name="web-server"></a>
### 웹 서버

대부분의 환경에서 Reverb는 서버의 외부에 노출되지 않은 포트에서 실행됩니다. 따라서, 트래픽을 Reverb로 라우팅하려면 리버스 프록시를 구성해야 합니다. 예를 들어 Reverb가 `0.0.0.0` 호스트의 포트 `8080`에서 실행되고 있고, 서버가 Nginx 웹 서버를 사용한다면 아래와 같이 리버스 프록시를 설정할 수 있습니다:

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
> Reverb는 `/app`에서 WebSocket 연결을 수신하고, `/apps`에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버가 이 두 URI 모두를 서빙할 수 있도록 반드시 설정해야 합니다. [Laravel Forge](https://forge.laravel.com)로 서버를 관리하는 경우, Reverb 서버는 기본적으로 올바르게 설정되어 있습니다.

일반적으로, 웹 서버는 과부하 방지를 위해 허용 가능한 연결 수를 제한합니다. Nginx 웹 서버에서 최대 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 조정합니다:

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

위 설정으로 Nginx는 프로세스당 최대 10,000개의 워커를 생성할 수 있습니다. 또한, Nginx의 열린 파일 제한도 10,000으로 설정됩니다.

<a name="ports"></a>
### 포트

Unix 기반 운영 체제는 서버에서 열 수 있는 포트 수를 제한합니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

위 출력 결과는 서버에서 최대 28,231개(60,999 - 32,768) 연결이 가능함을 의미합니다. 각 연결이 하나의 포트를 점유하기 때문입니다. 더 많은 연결을 처리하고 싶다면 [수평 스케일링](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 허용 포트 범위를 수정하여 사용 가능한 열려있는 포트 수를 늘릴 수도 있습니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우 Supervisor와 같은 프로세스 매니저를 사용해 Reverb 서버가 지속적으로 실행되도록 하는 것이 좋습니다. Supervisor로 Reverb를 운영하는 경우, `supervisor.conf` 파일에서 `minfds` 설정 값을 조정하여 Supervisor가 Reverb 서버의 연결을 관리하는 데 필요한 파일을 충분히 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### 스케일링

한 대의 서버만으로 처리할 수 있는 연결 수보다 더 많은 연결이 필요하다면, Reverb 서버를 수평 확장할 수 있습니다. Redis의 publish/subscribe 기능을 이용하면, Reverb가 여러 서버에 걸쳐 연결을 관리할 수 있습니다. 한 Reverb 서버에서 메시지를 수신할 경우, 해당 서버는 이 메시지를 Redis를 통해 다른 모든 서버로 전파합니다.

수평 확장을 활성화하려면 애플리케이션의 `.env` 파일에 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정하세요:

```env
REVERB_SCALING_ENABLED=true
```

다음으로, 모든 Reverb 서버가 통신하는 전용 중앙 Redis 서버를 구성해야 합니다. Reverb는 애플리케이션에 [설정된 기본 Redis 연결](/docs/master/redis#configuration)을 통해 메시지를 모든 Reverb 서버에 게시합니다.

Reverb의 스케일링 옵션을 활성화하고 Redis 서버를 구성하면, 이제 여러 서버에서 `reverb:start` 명령어를 각각 실행하기만 하면 됩니다. 이 Reverb 서버들은 로드 밸런서 뒤에 배치하여 들어오는 요청을 서버 간에 고르게 분산시켜야 합니다.

<a name="events"></a>
## 이벤트

Reverb는 연결 및 메시지 처리 과정에서 내부 이벤트를 발생시킵니다. 이 이벤트들에 [리스닝하여](/docs/master/events) 연결이 관리되거나 메시지가 주고받을 때 필요한 작업을 수행할 수 있습니다.

아래는 Reverb가 발생시키는 이벤트 목록입니다:

#### `Laravel\Reverb\Events\ChannelCreated`

채널이 생성될 때(일반적으로 첫 번째 연결이 특정 채널에 구독할 때) 발생합니다. 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달합니다.

#### `Laravel\Reverb\Events\ChannelRemoved`

채널이 제거될 때(일반적으로 마지막 연결이 채널에서 구독 해지할 때) 발생합니다. 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달합니다.

#### `Laravel\Reverb\Events\ConnectionPruned`

오래된(stale) 연결이 서버에 의해 정리(prune)될 때 발생합니다. 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스를 전달합니다.

#### `Laravel\Reverb\Events\MessageReceived`

클라이언트 연결로부터 메시지를 수신할 때 발생합니다. 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와, 원본 문자열 `$message`를 전달합니다.

#### `Laravel\Reverb\Events\MessageSent`

클라이언트 연결로 메시지를 전송할 때 발생합니다. 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와, 원본 문자열 `$message`를 전달합니다.
