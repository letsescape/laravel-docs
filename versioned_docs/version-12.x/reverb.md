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
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Reverb](https://github.com/laravel/reverb) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel's existing suite of [event broadcasting tools](/docs/12.x/broadcasting). -->
[Laravel Reverb](https://github.com/laravel/reverb)는 매우 빠르고 확장 가능한 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 [event broadcasting tools](/docs/12.x/broadcasting)와 원활하게 통합할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Reverb using the `install:broadcasting` Artisan command: -->
Reverb는 `install:broadcasting` Artisan 명령어를 사용하여 설치할 수 있습니다:

```shell
php artisan install:broadcasting
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Behind the scenes, the `install:broadcasting` Artisan command will run the `reverb:install` command, which will install Reverb with a sensible set of default configuration options. If you would like to make any configuration changes, you may do so by updating Reverb's environment variables or by updating the `config/reverb.php` configuration file. -->
내부적으로 `install:broadcasting` Artisan 명령어는 `reverb:install` 명령어를 실행하여, 합리적인 기본 구성 옵션과 함께 Reverb를 설치합니다. 구성 변경이 필요한 경우, Reverb의 환경 변수 또는 `config/reverb.php` 구성 파일을 수정하여 설정할 수 있습니다.

<a name="application-credentials"></a>
<!-- ### Application Credentials -->
### Application Credentials

<!-- In order to establish a connection to Reverb, a set of Reverb "application" credentials must be exchanged between the client and server. These credentials are configured on the server and are used to verify the request from the client. You may define these credentials using the following environment variables: -->
Reverb에 연결을 수립하기 위해서는 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명(application credentials)이 교환되어야 합니다. 이 자격 증명은 서버에 설정되며, 클라이언트 요청을 검증하는 데 사용됩니다. 다음과 같은 환경 변수를 사용해 자격 증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
<!-- ### Allowed Origins -->
### Allowed Origins

<!-- You may also define the origins from which client requests may originate by updating the value of the `allowed_origins` configuration value within the `apps` section of the `config/reverb.php` configuration file. Any requests from an origin not listed in your allowed origins will be rejected. You may allow all origins using `*`: -->
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
<!-- ### Additional Applications -->
### Additional Applications

<!-- Typically, Reverb provides a WebSocket server for the application in which it is installed. However, it is possible to serve more than one application using a single Reverb installation. -->
일반적으로 Reverb는 설치된 애플리케이션 전용 WebSocket 서버 역할을 합니다. 하지만, 한 번의 Reverb 설치로 여러 애플리케이션을 지원할 수도 있습니다.

<!-- For example, you may wish to maintain a single Laravel application which, via Reverb, provides WebSocket connectivity for multiple applications. This can be achieved by defining multiple `apps` in your application's `config/reverb.php` configuration file: -->
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
<!-- ### SSL -->
### SSL

<!-- In most cases, secure WebSocket connections are handled by the upstream web server (Nginx, etc.) before the request is proxied to your Reverb server. -->
대부분의 경우, 보안 WebSocket 연결은 (Nginx 등) 상위 웹 서버에서 처리된 후, 요청이 Reverb 서버로 프록시됩니다.

<!-- However, it can sometimes be useful, such as during local development, for the Reverb server to handle secure connections directly. If you are using [Laravel Herd's](https://herd.laravel.com) secure site feature or you are using [Laravel Valet](/docs/12.x/valet) and have run the [secure command](/docs/12.x/valet#securing-sites) against your application, you may use the Herd / Valet certificate generated for your site to secure your Reverb connections. To do so, set the `REVERB_HOST` environment variable to your site's hostname or explicitly pass the hostname option when starting the Reverb server: -->
하지만, 로컬 개발 중과 같이 Reverb 서버가 직접 보안 연결을 처리하는 것이 유용할 때도 있습니다. [Laravel Herd's](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/12.x/valet)를 사용하며 애플리케이션에 [secure command](/docs/12.x/valet#securing-sites)를 실행한 경우, 해당 사이트용으로 생성된 Herd/Valet 인증서를 활용하여 Reverb 연결을 보호할 수 있습니다. 이를 위해 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나, Reverb 서버를 시작할 때 명시적으로 hostname 옵션을 전달하십시오:

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

<!-- Since Herd and Valet domains resolve to `localhost`, running the command above will result in your Reverb server being accessible via the secure WebSocket protocol (`wss`) at `wss://laravel.test:8080`. -->
Herd 및 Valet 도메인은 `localhost`로 해석되기 때문에, 위 명령을 실행하면 `wss://laravel.test:8080`을 통한 보안 WebSocket 프로토콜(`wss`)로 Reverb 서버에 접근할 수 있습니다.

<!-- You may also manually choose a certificate by defining `tls` options in your application's `config/reverb.php` configuration file. Within the array of `tls` options, you may provide any of the options supported by [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php): -->
인증서를 수동으로 선택하려면, 애플리케이션의 `config/reverb.php` 파일에서 `tls` 옵션을 정의할 수 있습니다. `tls` 옵션 배열에는 [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 지정할 수 있습니다:

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
Reverb 서버는 `reverb:start` Artisan 명령어로 실행할 수 있습니다:

```shell
php artisan reverb:start
```

<!-- By default, the Reverb server will be started at `0.0.0.0:8080`, making it accessible from all network interfaces. -->
기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되므로, 모든 네트워크 인터페이스에서 접근 가능합니다.

<!-- If you need to specify a custom host or port, you may do so via the `--host` and `--port` options when starting the server: -->
사용자 지정 호스트나 포트를 지정하려면, 서버 시작 시 `--host` 및 `--port` 옵션을 사용하면 됩니다:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000
```

<!-- Alternatively, you may define `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables in your application's `.env` configuration file. -->
또는, 애플리케이션의 `.env` 구성 파일에서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

<!-- The `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables should not be confused with `REVERB_HOST` and `REVERB_PORT`. The former specify the host and port on which to run the Reverb server itself, while the latter pair instruct Laravel where to send broadcast messages. For example, in a production environment, you may route requests from your public Reverb hostname on port `443` to a Reverb server operating on `0.0.0.0:8080`. In this scenario, your environment variables would be defined as follows: -->
`REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST` 및 `REVERB_PORT`와 혼동하지 않아야 합니다. 전자는 Reverb 서버 자체를 실행할 호스트와 포트를 지정하며, 후자는 Laravel이 브로드캐스트 메시지를 보낼 주소를 지정합니다. 예를 들어, 프로덕션 환경에서는 공개된 Reverb 호스트명의 `443` 포트로 들어온 요청을, `0.0.0.0:8080`에서 작동하는 Reverb 서버로 라우팅할 수 있습니다. 이 경우 환경 변수 설정은 다음과 같습니다:

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
성능 향상을 위해, Reverb는 기본적으로 어떠한 디버그 정보도 출력하지 않습니다. Reverb 서버를 통해 전달되는 데이터 스트림을 확인하려면, `reverb:start` 명령에 `--debug` 옵션을 추가하십시오:

```shell
php artisan reverb:start --debug
```

<a name="restarting"></a>
<!-- ### Restarting -->
### Restarting

<!-- Since Reverb is a long-running process, changes to your code will not be reflected without restarting the server via the `reverb:restart` Artisan command. -->
Reverb는 지속적으로 실행되는(long-running) 프로세스이므로, 코드 변경 사항이 바로 반영되지 않습니다. 코드를 수정한 후에는 반드시 `reverb:restart` Artisan 명령어로 서버를 재시작해야 합니다.

<!-- The `reverb:restart` command ensures all connections are gracefully terminated before stopping the server. If you are running Reverb with a process manager such as Supervisor, the server will be automatically restarted by the process manager after all connections have been terminated: -->
`reverb:restart` 명령어는 서버를 중지하기 전에 모든 연결을 정상적으로 종료(graceful termination)합니다. Supervisor와 같은 프로세스 관리자를 사용하여 Reverb를 실행 중이라면, 모든 연결 종료 후 프로세스 관리자가 자동으로 서버를 재시작합니다:

```shell
php artisan reverb:restart
```

<a name="monitoring"></a>
<!-- ## Monitoring -->
## Monitoring

<!-- Reverb may be monitored via an integration with [Laravel Pulse](/docs/12.x/pulse). By enabling Reverb's Pulse integration, you may track the number of connections and messages being handled by your server. -->
Reverb는 [Laravel Pulse](/docs/12.x/pulse)와의 통합 기능을 통해 모니터링할 수 있습니다. Reverb의 Pulse 통합을 활성화하면, 서버에서 처리 중인 연결 수와 메시지 수를 추적할 수 있습니다.

<!-- To enable the integration, you should first ensure you have [installed Pulse](/docs/12.x/pulse#installation). Then, add any of Reverb's recorders to your application's `config/pulse.php` configuration file: -->
통합을 활성화하려면, 우선 [installed Pulse](/docs/12.x/pulse#installation)했는지 확인하십시오. 그런 다음, Reverb의 레코더(recorder)를 애플리케이션의 `config/pulse.php` 구성 파일에 추가하면 됩니다:

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

<!-- Next, add the Pulse cards for each recorder to your [Pulse dashboard](/docs/12.x/pulse#dashboard-customization): -->
다음으로, 각 레코더의 Pulse 카드(card)를 [Pulse dashboard](/docs/12.x/pulse#dashboard-customization)에 추가하십시오:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

<!-- Connection activity is recorded by polling for new updates on a periodic basis. To ensure this information is rendered correctly on the Pulse dashboard, you must run the `pulse:check` daemon on your Reverb server. If you are running Reverb in a [horizontally scaled](#scaling) configuration, you should only run this daemon on one of your servers. -->
연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. 이 정보가 Pulse 대시보드에 올바르게 렌더링되려면, Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. [horizontally scaled](#scaling) 구성에서는 단 한 서버에서만 이 데몬을 실행하면 됩니다.

<a name="production"></a>
<!-- ## Running Reverb in Production -->
## Running Reverb in Production

<!-- Due to the long-running nature of WebSocket servers, you may need to make some optimizations to your server and hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the resources available on your server. -->
WebSocket 서버의 지속적인 실행 특성 때문에, 서버와 호스팅 환경을 최적화하여 사용할 수 있는 리소스 범위 내에서 Reverb 서버가 최적의 연결 수를 처리할 수 있도록 해야 합니다.

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com)는 Laravel Reverb 클러스터가 제공하는 완전 관리형 WebSocket 인프라를 통해, 인프라 관리 없이 Reverb 기반 애플리케이션을 스케일 확장 및 배포할 수 있습니다.

<a name="open-files"></a>
<!-- ### Open Files -->
### Open Files

<!-- Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. However, there are often limits on the number of allowed open files at both the operating system and application level. -->
각 WebSocket 연결은 클라이언트나 서버가 연결을 종료할 때까지 메모리에 유지됩니다. 유닉스 및 유닉스 계열 환경에서는 각 연결이 하나의 파일로 간주됩니다. 하지만, 운영체제와 애플리케이션 레벨 모두에서 열 수 있는 파일의 개수에는 제한이 있습니다.

<a name="operating-system"></a>
<!-- #### Operating System -->
#### Operating System

<!-- On a Unix based operating system, you may determine the allowed number of open files using the `ulimit` command: -->
유닉스 기반 운영체제에서는 `ulimit` 명령어로 허용된 열린 파일 개수를 확인할 수 있습니다:

```shell
ulimit -n
```

<!-- This command will display the open file limits allowed for different users. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like the following: -->
이 명령은 사용자의 열린 파일 제한을 표시합니다. 값을 변경하려면 `/etc/security/limits.conf` 파일을 수정하십시오. 예를 들어, `forge` 사용자에 대해 열린 파일의 최대값을 10,000개로 설정하려면 다음과 같이 하면 됩니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
<!-- ### Event Loop -->
### Event Loop

<!-- Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select`, which doesn't require any additional extensions. However, `stream_select` is typically limited to 1,024 open files. As such, if you plan to handle more than 1,000 concurrent connections, you will need to use an alternative event loop not bound to the same restrictions. -->
내부적으로 Reverb는 ReactPHP 이벤트 루프를 사용하여 서버에서 WebSocket 연결을 관리합니다. 기본적으로 이 이벤트 루프는 별도의 확장 없이 사용 가능한 `stream_select`를 사용하여 동작합니다. 하지만, `stream_select`는 일반적으로 1,024개의 열린 파일까지만 지원합니다. 따라서, 1,000개 이상의 동시 연결을 처리하려면 동일한 제약에 묶이지 않는 대안 이벤트 루프를 사용해야 합니다.

<!-- Reverb will automatically switch to an `ext-uv` powered loop when available. This PHP extension is available for install via PECL: -->
Reverb는 사용 가능한 경우 자동으로 `ext-uv` 기반 루프로 전환합니다. 해당 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv
```

<a name="web-server"></a>
<!-- ### Web Server -->
### Web Server

<!-- In most cases, Reverb runs on a non web-facing port on your server. So, in order to route traffic to Reverb, you should configure a reverse proxy. Assuming Reverb is running on host `0.0.0.0` and port `8080` and your server utilizes the Nginx web server, a reverse proxy can be defined for your Reverb server using the following Nginx site configuration: -->
대부분의 경우, Reverb는 서버의 외부 서비스용 포트가 아닌 곳에서 실행됩니다. 따라서, Reverb로 트래픽을 라우팅하려면 리버스 프록시(reverse proxy)를 구성해야 합니다. 예를 들어, Reverb가 호스트 `0.0.0.0`, 포트 `8080`에서 실행 중이고 서버에서 Nginx 웹 서버를 사용한다면, 다음과 같이 Nginx 사이트 구성 파일을 설정할 수 있습니다:

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

<!-- Typically, web servers are configured to limit the number of allowed connections in order to prevent overloading the server. To increase the number of allowed connections on an Nginx web server to 10,000, the `worker_rlimit_nofile` and `worker_connections` values of the `nginx.conf` file should be updated: -->
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

<!-- The configuration above will allow up to 10,000 Nginx workers per process to be spawned. In addition, this configuration sets Nginx's open file limit to 10,000. -->
위 설정은 프로세스당 최대 10,000개의 Nginx 워커를 생성할 수 있게 합니다. 또한, Nginx의 열린 파일 제한도 10,000으로 설정됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- Unix-based operating systems typically limit the number of ports which can be opened on the server. You may see the current allowed range via the following command: -->
유닉스 기반 운영체제는 서버에서 열 수 있는 포트의 개수에도 제한이 있습니다. 현재 허용된 포트 범위는 다음 명령어로 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

<!-- The output above shows the server can handle a maximum of 28,231 (60,999 - 32,768) connections since each connection requires a free port. Although we recommend [horizontal scaling](#scaling) to increase the number of allowed connections, you may increase the number of available open ports by updating the allowed port range in your server's `/etc/sysctl.conf` configuration file. -->
위 출력에서 60,999 - 32,768 = 28,231개 포트까지 동시에 연결이 가능하다는 것을 알 수 있습니다. 각 연결마다 사용 가능한 포트가 필요하기 때문입니다. 더 많은 연결을 지원하려면 [horizontal scaling](#scaling)을 권장하며, 포트 개수를 늘려야 할 경우 서버의 `/etc/sysctl.conf` 파일에서 허용된 포트 범위를 조정하면 됩니다.

<a name="process-management"></a>
<!-- ### Process Management -->
### Process Management

<!-- In most cases, you should use a process manager such as Supervisor to ensure the Reverb server is continually running. If you are using Supervisor to run Reverb, you should update the `minfds` setting of your server's `supervisor.conf` file to ensure Supervisor is able to open the files required to handle connections to your Reverb server: -->
대부분의 경우, Supervisor와 같은 프로세스 관리자를 사용하여 Reverb 서버가 항상 실행되도록 하는 것이 좋습니다. Supervisor로 Reverb를 관리할 경우, `supervisor.conf` 파일의 `minfds` 설정을 조정해서 Supervisor가 Reverb 서버의 연결을 처리할 만큼 충분한 파일을 열 수 있도록 해야 합니다:

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
<!-- ### Scaling -->
### Scaling

<!-- If you need to handle more connections than a single server will allow, you may scale your Reverb server horizontally. Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers. When a message is received by one of your application's Reverb servers, the server will use Redis to publish the incoming message to all other servers. -->
하나의 서버가 처리할 수 있는 연결 수를 초과하는 경우, Reverb 서버를 수평 확장하여 동작할 수 있습니다. Redis의 publish/subscribe 기능을 활용하여, Reverb는 여러 서버에 걸쳐 연결을 관리할 수 있습니다. 한 Reverb 서버로 메시지가 들어오면, 해당 서버는 Redis를 이용해 모든 다른 서버로 해당 메시지를 보냅니다.

<!-- To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` environment variable to `true` in your application's `.env` configuration file: -->
수평 확장을 활성화하려면, 애플리케이션의 `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정해야 합니다:

```env
REVERB_SCALING_ENABLED=true
```

<!-- Next, you should have a dedicated, central Redis server to which all of the Reverb servers will communicate. Reverb will use the [default Redis connection configured for your application](/docs/12.x/redis#configuration) to publish messages to all of your Reverb servers. -->
그리고 모든 Reverb 서버가 통신할 수 있는 전용 중앙 Redis 서버가 필요합니다. Reverb는 [default Redis connection configured for your application](/docs/12.x/redis#configuration)을 사용하여 모든 Reverb 서버에 메시지를 퍼블리시합니다.

<!-- Once you have enabled Reverb's scaling option and configured a Redis server, you may simply invoke the `reverb:start` command on multiple servers that are able to communicate with your Redis server. These Reverb servers should be placed behind a load balancer that distributes incoming requests evenly among the servers. -->
Reverb 스케일링 옵션을 활성화하고 Redis 서버를 구성했다면, Redis 서버와 통신 가능한 여러 대의 서버에서 `reverb:start` 명령어를 실행하기만 하면 됩니다. 이 Reverb 서버들은 로드 밸런서 뒤에 둬서, 수신 요청이 여러 서버에 고르게 분산되도록 배치합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Reverb dispatches internal events during the lifecycle of a connection and message handling. You may [listen for these events](/docs/12.x/events) to perform actions when connections are managed or messages are exchanged. -->
Reverb는 연결 및 메시지 처리의 라이프사이클 동안 내부적으로 이벤트를 디스패치(dispatch)합니다. 이러한 이벤트에 [listen for these events](/docs/12.x/events)하여, 연결 관리나 메시지 교환 시 특정 동작을 수행할 수 있습니다.

<!-- The following events are dispatched by Reverb: -->
Reverb에서 디스패치되는 주요 이벤트는 다음과 같습니다:

<!-- #### `Laravel\Reverb\Events\ChannelCreated` -->
#### `Laravel\Reverb\Events\ChannelCreated`

<!-- Dispatched when a channel is created. This typically occurs when the first connection subscribes to a specific channel. The event receives the `Laravel\Reverb\Protocols\Pusher\Channel` instance. -->
채널이 생성될 때 디스패치됩니다. 일반적으로 첫 번째 연결이 특정 채널에 가입(서브스크립션)할 때 발생합니다. 이 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달받습니다.

<!-- #### `Laravel\Reverb\Events\ChannelRemoved` -->
#### `Laravel\Reverb\Events\ChannelRemoved`

<!-- Dispatched when a channel is removed. This typically occurs when the last connection unsubscribes from a channel. The event receives the `Laravel\Reverb\Protocols\Pusher\Channel` instance. -->
채널이 삭제될 때 디스패치됩니다. 이는 마지막 연결이 채널에서 탈퇴(언서브스크립션)할 때 발생합니다. 이 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 전달받습니다.

<!-- #### `Laravel\Reverb\Events\ConnectionPruned` -->
#### `Laravel\Reverb\Events\ConnectionPruned`

<!-- Dispatched when a stale connection is pruned by the server. The event receives the `Laravel\Reverb\Contracts\Connection` instance. -->
서버에 의해 오래된(stale) 연결이 정리(prune)될 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스를 전달받습니다.

<!-- #### `Laravel\Reverb\Events\MessageReceived` -->
#### `Laravel\Reverb\Events\MessageReceived`

<!-- Dispatched when a message is received from a client connection. The event receives the `Laravel\Reverb\Contracts\Connection` instance and the raw string `$message`. -->
클라이언트 연결로부터 메시지를 수신할 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`를 전달받습니다.

<!-- #### `Laravel\Reverb\Events\MessageSent` -->
#### `Laravel\Reverb\Events\MessageSent`

<!-- Dispatched when a message is sent to a client connection. The event receives the `Laravel\Reverb\Contracts\Connection` instance and the raw string `$message`. -->
클라이언트 연결에 메시지가 전송될 때 디스패치됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원본 문자열 `$message`를 전달받습니다.
