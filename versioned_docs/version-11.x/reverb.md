<!-- # Laravel Reverb -->
# Laravel Reverb

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Application Credentials](#application-credentials)
    - [Allowed Origins](#allowed-origins)
    - [Additional Applications](#additional-applications)
    - [SSL](#ssl)
- [Running the Server](#running-server)
    - [Debugging](#debugging)
    - [Restarting](#restarting)
- [Monitoring](#monitoring)
- [Running Reverb in Production](#production)
    - [Open Files](#open-files)
    - [Event Loop](#event-loop)
    - [Web Server](#web-server)
    - [Ports](#ports)
    - [Process Management](#process-management)
    - [Scaling](#scaling)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Reverb](https://github.com/laravel/reverb) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel’s existing suite of [event broadcasting tools](/docs/11.x/broadcasting). -->
[Laravel Reverb](https://github.com/laravel/reverb)는 매우 빠르고 확장 가능한 실시간 WebSocket 통신을 여러분의 Laravel 애플리케이션에 직접 제공합니다. 또한 Laravel이 제공하는 기존 [event broadcasting tools](/docs/11.x/broadcasting)와도 완벽하게 통합됩니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Reverb using the `install:broadcasting` Artisan command: -->
Reverb는 `install:broadcasting` 아티즌 명령어를 사용해 설치할 수 있습니다.

```
php artisan install:broadcasting
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Behind the scenes, the `install:broadcasting` Artisan command will run the `reverb:install` command, which will install Reverb with a sensible set of default configuration options. If you would like to make any configuration changes, you may do so by updating Reverb's environment variables or by updating the `config/reverb.php` configuration file. -->
사실상, `install:broadcasting` 아티즌 명령어는 내부적으로 `reverb:install` 명령어를 실행하여 기본적으로 적절한 설정 옵션을 사용해 Reverb를 설치합니다. 만약 설정을 변경하고 싶다면, Reverb 관련 환경 변수나 `config/reverb.php` 설정 파일을 수정하면 됩니다.

<a name="application-credentials"></a>
<!-- ### Application Credentials -->
### Application Credentials

<!-- In order to establish a connection to Reverb, a set of Reverb "application" credentials must be exchanged between the client and server. These credentials are configured on the server and are used to verify the request from the client. You may define these credentials using the following environment variables: -->
Reverb에 연결하기 위해서는 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명 세트가 교환되어야 합니다. 이 자격 증명은 서버에서 설정하며, 클라이언트의 요청을 검증하는 데 사용됩니다. 아래 환경 변수로 자격 증명을 설정할 수 있습니다.

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
<!-- ### Allowed Origins -->
### Allowed Origins

<!-- You may also define the origins from which client requests may originate by updating the value of the `allowed_origins` configuration value within the `apps` section of the `config/reverb.php` configuration file. Any requests from an origin not listed in your allowed origins will be rejected. You may allow all origins using `*`: -->
클라이언트 요청을 허용할 오리진을 지정하려면, `config/reverb.php` 설정 파일의 `apps` 섹션 안에 있는 `allowed_origins` 값을 수정하면 됩니다. 명시되지 않은 오리진에서 들어오는 모든 요청은 거부됩니다. 모든 오리진을 허용하려면 `*` 를 사용할 수 있습니다.

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
<!-- ### Additional Applications -->
### Additional Applications

<!-- Typically, Reverb provides a WebSocket server for the application in which it is installed. However, it is possible to serve more than one application using a single Reverb installation. -->
일반적으로 Reverb는 설치된 애플리케이션에 대해 WebSocket 서버를 제공합니다. 하지만 단일 Reverb 설치로 여러 애플리케이션을 동시에 서비스할 수도 있습니다.

<!-- For example, you may wish to maintain a single Laravel application which, via Reverb, provides WebSocket connectivity for multiple applications. This can be achieved by defining multiple `apps` in your application's `config/reverb.php` configuration file: -->
예를 들어, 단일 Laravel 애플리케이션이 여러 애플리케이션을 위해 Reverb를 통해 WebSocket 연결을 제공하도록 운영할 수 있습니다. 이를 위해서는 애플리케이션의 `config/reverb.php` 설정 파일에 여러 개의 `apps`를 정의하면 됩니다.

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
<!-- ### SSL -->
### SSL

<!-- In most cases, secure WebSocket connections are handled by the upstream web server (Nginx, etc.) before the request is proxied to your Reverb server. -->
대부분의 경우, WebSocket 보안 연결(SSL/TLS)은 요청이 Reverb 서버로 프록시되기 전에 Nginx 등 업스트림 웹 서버가 처리합니다.

<!-- However, it can sometimes be useful, such as during local development, for the Reverb server to handle secure connections directly. If you are using [Laravel Herd's](https://herd.laravel.com) secure site feature or you are using [Laravel Valet](/docs/11.x/valet) and have run the [secure command](/docs/11.x/valet#securing-sites) against your application, you may use the Herd / Valet certificate generated for your site to secure your Reverb connections. To do so, set the `REVERB_HOST` environment variable to your site's hostname or explicitly pass the hostname option when starting the Reverb server: -->
하지만, 로컬 개발 환경과 같이 Reverb 서버가 직접 보안 연결을 처리해야 하는 상황도 있을 수 있습니다. 만약 [Laravel Herd's](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/11.x/valet)에서 [secure command](/docs/11.x/valet#securing-sites)를 실행해 애플리케이션을 보호했다면, Herd 또는 Valet이 사이트를 위해 생성한 인증서를 Reverb 연결에도 사용할 수 있습니다. 이 경우, `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 지정하거나, Reverb 서버를 시작할 때 명령어 옵션으로 직접 호스트명을 지정합니다.

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

<!-- Since Herd and Valet domains resolve to `localhost`, running the command above will result in your Reverb server being accessible via the secure WebSocket protocol (`wss`) at `wss://laravel.test:8080`. -->
Herd 및 Valet 도메인은 `localhost`로 연결되므로, 위와 같이 명령어를 실행하면 Reverb 서버에 보안 WebSocket 프로토콜(`wss`)로 `wss://laravel.test:8080`을 통해 접근할 수 있습니다.

<!-- You may also manually choose a certificate by defining `tls` options in your application's `config/reverb.php` configuration file. Within the array of `tls` options, you may provide any of the options supported by [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php): -->
또는, 애플리케이션의 `config/reverb.php` 설정 파일에서 `tls` 옵션을 추가해 인증서를 직접 지정할 수도 있습니다. `tls` 옵션 배열에는 [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 사용할 수 있습니다.

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
<!-- ## Running the Server -->
## Running the Server

<!-- The Reverb server can be started using the `reverb:start` Artisan command: -->
Reverb 서버는 `reverb:start` 아티즌 명령어로 실행할 수 있습니다.

```sh
php artisan reverb:start
```

<!-- By default, the Reverb server will be started at `0.0.0.0:8080`, making it accessible from all network interfaces. -->
기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접근할 수 있습니다.

<!-- If you need to specify a custom host or port, you may do so via the `--host` and `--port` options when starting the server: -->
만약 별도의 호스트나 포트를 지정하고 싶다면 서버 시작 시 `--host` 와 `--port` 옵션을 쓸 수 있습니다.

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

<!-- Alternatively, you may define `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables in your application's `.env` configuration file. -->
또는, 애플리케이션의 `.env` 설정 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 지정할 수 있습니다.

<!-- The `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables should not be confused with `REVERB_HOST` and `REVERB_PORT`. The former specify the host and port on which to run the Reverb server itself, while the latter pair instruct Laravel where to send broadcast messages. For example, in a production environment, you may route requests from your public Reverb hostname on port `443` to a Reverb server operating on `0.0.0.0:8080`. In this scenario, your environment variables would be defined as follows: -->
`REVERB_SERVER_HOST`, `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST`, `REVERB_PORT`와 혼동해서는 안 됩니다. 전자는 Reverb 서버 자체가 실행될 호스트와 포트를 지정하고, 후자는 Laravel이 브로드캐스트 메시지를 보낼 위치를 알려주는 역할을 합니다. 예를 들어 운영 환경에서는, 공개 Reverb 호스트네임의 `443` 포트로 들어온 요청을 실제 동작 중인 `0.0.0.0:8080`의 Reverb 서버로 프록시 할 수 있습니다. 이때 환경 변수는 아래와 같이 설정합니다.

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
<!-- ### Debugging -->
### Debugging

<!-- To improve performance, Reverb does not output any debug information by default. If you would like to see the stream of data passing through your Reverb server, you may provide the `--debug` option to the `reverb:start` command: -->
성능 향상을 위해, Reverb는 기본적으로 어떠한 디버그 정보도 출력하지 않습니다. 서버를 통과하는 데이터 스트림을 확인하고 싶다면, `reverb:start` 명령어에 `--debug` 옵션을 추가하면 됩니다.

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
<!-- ### Restarting -->
### Restarting

<!-- Since Reverb is a long-running process, changes to your code will not be reflected without restarting the server via the `reverb:restart` Artisan command. -->
Reverb는 장시간 동작하는 프로세스이기 때문에, 코드 변경 사항이 서버에 바로 반영되지 않습니다. 따라서, 서버 코드를 변경한 경우 `reverb:restart` 아티즌 명령어로 서버를 재시작해야 합니다.

<!-- The `reverb:restart` command ensures all connections are gracefully terminated before stopping the server. If you are running Reverb with a process manager such as Supervisor, the server will be automatically restarted by the process manager after all connections have been terminated: -->
`reverb:restart` 명령어는 서버를 중지하기 전에 모든 연결이 정상적으로 종료될 수 있도록 처리합니다. 만약 Supervisor와 같은 프로세스 관리 도구를 사용해 Reverb를 실행 중이라면, 모든 연결이 종료된 후 프로세스 관리자에 의해 서버가 자동으로 재시작됩니다.

```sh
php artisan reverb:restart
```

<a name="monitoring"></a>
<!-- ## Monitoring -->
## Monitoring

<!-- Reverb may be monitored via an integration with [Laravel Pulse](/docs/11.x/pulse). By enabling Reverb's Pulse integration, you may track the number of connections and messages being handled by your server. -->
Reverb는 [Laravel Pulse](/docs/11.x/pulse)와의 통합을 통해 서버의 연결 수와 메시지 처리 현황을 모니터링할 수 있습니다.

<!-- To enable the integration, you should first ensure you have [installed Pulse](/docs/11.x/pulse#installation). Then, add any of Reverb's recorders to your application's `config/pulse.php` configuration file: -->
통합을 활성화하려면, 먼저 [installed Pulse](/docs/11.x/pulse#installation)한 뒤, Reverb의 recorder를 애플리케이션의 `config/pulse.php` 설정 파일에 추가해야 합니다.

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

    ...
],
```

<!-- Next, add the Pulse cards for each recorder to your [Pulse dashboard](/docs/11.x/pulse#dashboard-customization): -->
그리고 각각의 recorder에 맞는 Pulse 카드를 [Pulse dashboard](/docs/11.x/pulse#dashboard-customization)에 추가합니다.

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

<!-- Connection activity is recorded by polling for new updates on a periodic basis. To ensure this information is rendered correctly on the Pulse dashboard, you must run the `pulse:check` daemon on your Reverb server. If you are running Reverb in a [horizontally scaled](#scaling) configuration, you should only run this daemon on one of your servers. -->
연결 활동 정보는 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. Pulse 대시보드에 이 정보가 올바르게 표시되려면, Reverb 서버에서 `pulse:check` 데몬을 반드시 실행해야 합니다. 만약 [horizontally scaled](#scaling) 환경에서 여러 대의 서버를 운영하고 있다면, 데몬은 하나의 서버에서만 실행하면 됩니다.

<a name="production"></a>
<!-- ## Running Reverb in Production -->
## Running Reverb in Production

<!-- Due to the long-running nature of WebSocket servers, you may need to make some optimizations to your server and hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the resources available on your server. -->
WebSocket 서버의 특성상 오랜 시간 실행되는 프로세스이므로, 서버의 자원(메모리 등) 상황에서 적절한 연결 수를 효과적으로 처리할 수 있도록 서버와 호스팅 환경에 몇 가지 최적화가 필요합니다.

> [!NOTE]
> 여러분의 사이트를 [Laravel Forge](https://forge.laravel.com)에서 관리 중이라면, "Application" 패널에서 Reverb 통합 기능을 활성화하여 서버를 자동으로 최적화할 수 있습니다. 해당 통합을 켜면 Forge에서 필요한 확장 프로그램 설치와 연결 수 한도 조정까지 자동으로 처리해주어 운영 환경 준비가 완료됩니다.

<a name="open-files"></a>
<!-- ### Open Files -->
### Open Files

<!-- Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. However, there are often limits on the number of allowed open files at both the operating system and application level. -->
각 WebSocket 연결은 클라이언트나 서버에서 연결이 끊길 때까지 메모리에 유지됩니다. 유닉스 계열 환경에서는 각 연결이 파일로 취급되며, 시스템 및 애플리케이션 레벨에서 열 수 있는 파일 수에 제한이 있을 수 있습니다.

<a name="operating-system"></a>
<!-- #### Operating System -->
#### Operating System

<!-- On a Unix based operating system, you may determine the allowed number of open files using the `ulimit` command: -->
유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 열 수 있는 파일 개수를 확인할 수 있습니다.

```sh
ulimit -n
```

<!-- This command will display the open file limits allowed for different users. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like the following: -->
이 명령어로 사용자의 오픈 파일 수 제한을 확인할 수 있습니다. 값을 수정하려면 `/etc/security/limits.conf` 파일을 편집하면 됩니다. 예를 들어, `forge` 사용자의 오픈 파일 수를 10,000개로 늘리려면 다음과 같이 작성합니다.

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
<!-- ### Event Loop -->
### Event Loop

<!-- Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select`, which doesn't require any additional extensions. However, `stream_select` is typically limited to 1,024 open files. As such, if you plan to handle more than 1,000 concurrent connections, you will need to use an alternative event loop not bound to the same restrictions. -->
Reverb는 서버에서 WebSocket 연결을 관리하기 위해 ReactPHP 이벤트 루프를 사용합니다. 기본적으로 이 이벤트 루프는 `stream_select` 기반으로 동작하며, 별도의 확장 프로그램 없이 사용할 수 있습니다. 하지만, `stream_select`는 일반적으로 1,024개의 오픈 파일 제한을 가지므로, 1,000개가 넘는 동시 연결을 처리하려면 이러한 제약이 없는 다른 이벤트 루프를 사용해야 합니다.

<!-- Reverb will automatically switch to an `ext-uv` powered loop when available. This PHP extension is available for install via PECL: -->
Reverb는 `ext-uv` 확장 프로그램이 설치되어 있는 경우 자동으로 해당 루프로 전환합니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다.

```sh
pecl install uv
```

<a name="web-server"></a>
<!-- ### Web Server -->
### Web Server

<!-- In most cases, Reverb runs on a non web-facing port on your server. So, in order to route traffic to Reverb, you should configure a reverse proxy. Assuming Reverb is running on host `0.0.0.0` and port `8080` and your server utilizes the Nginx web server, a reverse proxy can be defined for your Reverb server using the following Nginx site configuration: -->
일반적으로 리버브는 서버의 외부에서 바로 접근할 수 없는 포트에서 동작합니다. 따라서 트래픽을 리버브로 전달하려면 리버스 프록시를 설정해야 합니다. Reverb가 `0.0.0.0`의 `8080` 포트에서 동작하고, 서버에 Nginx 웹서버를 사용하고 있다면, 아래와 같이 Nginx 사이트 설정에서 리버스 프록시를 지정할 수 있습니다.

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
> Reverb는 `/app`에서 WebSocket 연결을 받고 `/apps`에서 API 요청을 처리합니다. Reverb 연결을 처리하는 웹 서버가 두 URI 모두를 지원할 수 있도록 설정해야 합니다. [Laravel Forge](https://forge.laravel.com)에서 서버를 관리 중이라면, 기본적으로 Reverb 서버가 올바르게 구성됩니다.

<!-- Typically, web servers are configured to limit the number of allowed connections in order to prevent overloading the server. To increase the number of allowed connections on an Nginx web server to 10,000, the `worker_rlimit_nofile` and `worker_connections` values of the `nginx.conf` file should be updated: -->
일반적으로 웹 서버는 서버 과부하를 방지하기 위해 연결 수에 제한을 두고 있습니다. 만약 Nginx 웹 서버에서 연결 수를 10,000개까지 늘리고 싶다면, `nginx.conf` 파일에서 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 수정해야 합니다.

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

<!-- The configuration above will allow up to 10,000 Nginx workers per process to be spawned. In addition, this configuration sets Nginx's open file limit to 10,000. -->
위 설정은 프로세스당 Nginx 워커를 최대 10,000개까지 사용할 수 있게 하며, 동시에 Nginx의 오픈 파일 제한도 10,000개로 맞춰줍니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- Unix-based operating systems typically limit the number of ports which can be opened on the server. You may see the current allowed range via the following command: -->
유닉스 기반 운영체제는 서버에서 오픈할 수 있는 포트의 개수에도 제한이 있습니다. 현재 허용된 포트 범위는 다음 명령어로 확인 가능합니다.

 ```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

<!-- The output above shows the server can handle a maximum of 28,231 (60,999 - 32,768) connections since each connection requires a free port. Although we recommend [horizontal scaling](#scaling) to increase the number of allowed connections, you may increase the number of available open ports by updating the allowed port range in your server's `/etc/sysctl.conf` configuration file. -->
위와 같은 출력이라면, 서버는 최대 28,231개(60,999 - 32,768)의 연결을 동시에 처리할 수 있습니다. 각 연결마다 하나의 포트가 필요하기 때문입니다. 더 많은 연결을 지원하려면 [horizontal scaling](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 허용 포트 범위를 늘려 더 많은 포트를 사용할 수도 있습니다.

<a name="process-management"></a>
<!-- ### Process Management -->
### Process Management

<!-- In most cases, you should use a process manager such as Supervisor to ensure the Reverb server is continually running. If you are using Supervisor to run Reverb, you should update the `minfds` setting of your server's `supervisor.conf` file to ensure Supervisor is able to open the files required to handle connections to your Reverb server: -->
대부분의 경우, Reverb 서버가 항상 실행 상태를 유지하도록 Supervisor와 같은 프로세스 관리 도구를 이용하는 것이 좋습니다. Supervisor로 Reverb를 실행하는 경우, `supervisor.conf` 파일의 `minfds` 설정을 늘려서 Supervisor가 연결을 관리하는데 필요한 만큼 파일을 열 수 있도록 해야 합니다.

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
<!-- ### Scaling -->
### Scaling

<!-- If you need to handle more connections than a single server will allow, you may scale your Reverb server horizontally. Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers. When a message is received by one of your application's Reverb servers, the server will use Redis to publish the incoming message to all other servers. -->
단일 서버에서 허용 가능한 연결 수가 부족하다면, Reverb 서버를 수평 확장(여러 대로 분산)할 수 있습니다. Redis의 pub/sub 기능을 활용해, 여러 서버에서 연결을 동시에 관리할 수 있습니다. 메시지가 애플리케이션의 어떤 Reverb 서버에 도착하더라도, 해당 서버가 Redis를 통해 다른 모든 서버에도 메시지를 전달합니다.

<!-- To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` environment variable to `true` in your application's `.env` configuration file: -->
수평 확장을 활성화하려면, 애플리케이션의 `.env` 설정 파일에 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 지정하세요.

```env
REVERB_SCALING_ENABLED=true
```

<!-- Next, you should have a dedicated, central Redis server to which all of the Reverb servers will communicate. Reverb will use the [default Redis connection configured for your application](/docs/11.x/redis#configuration) to publish messages to all of your Reverb servers. -->
그리고 모든 Reverb 서버가 통신할 수 있게, 하나의 중앙 Redis 서버를 반드시 운영해야 합니다. 메시지 전파에는 [default Redis connection configured for your application](/docs/11.x/redis#configuration)이 자동으로 사용됩니다.

<!-- Once you have enabled Reverb's scaling option and configured a Redis server, you may simply invoke the `reverb:start` command on multiple servers that are able to communicate with your Redis server. These Reverb servers should be placed behind a load balancer that distributes incoming requests evenly among the servers. -->
이제 리버브 스케일링 옵션과 Redis 서버를 준비했다면, Redis 서버와 통신 가능한 여러 서버에서 동시에 `reverb:start` 명령어를 실행하면 됩니다. 이들 Reverb 서버는 반드시 로드밸런서 뒤에 위치하여, 들어오는 요청이 서버들 사이에 고르게 분산되도록 해야 합니다.
