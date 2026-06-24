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

<!-- [Laravel Reverb](https://github.com/laravel/reverb) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel’s existing suite of event broadcasting tools. -->
[Laravel Reverb](https://github.com/laravel/reverb)는 Laravel 애플리케이션에 초고속이면서 확장 가능한 실시간 WebSocket 통신 기능을 직접 제공하며, Laravel의 기존 이벤트 브로드캐스팅 도구와도 완벽하게 통합됩니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Reverb는 PHP 8.2 이상, Laravel 10.47 이상이 필요합니다.

<!-- You may use the Composer package manager to install Reverb into your Laravel project: -->
Composer 패키지 매니저를 사용하여 Laravel 프로젝트에 리버브를 설치할 수 있습니다.

```sh
composer require laravel/reverb
```

<!-- Once the package is installed, you may run Reverb's installation command to publish the configuration, add Reverb's required environment variables, and enable event broadcasting in your application: -->
패키지 설치가 완료되면, 리버브의 설치 명령어를 실행하여 설정 파일을 배포하고, 리버브에 필요한 환경 변수들을 추가하며, 애플리케이션의 이벤트 브로드캐스트가 활성화되도록 할 수 있습니다.

```sh
php artisan reverb:install
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The `reverb:install` command will automatically configure Reverb using a sensible set of default options. If you would like to make any configuration changes, you may do so by updating Reverb's environment variables or by updating the `config/reverb.php` configuration file. -->
`reverb:install` 명령어는 합리적인 기본 옵션으로 리버브를 자동으로 설정해줍니다. 만약 설정을 변경하고 싶다면, 리버브와 관련된 환경 변수나 `config/reverb.php` 설정 파일을 직접 수정하면 됩니다.

<a name="application-credentials"></a>
<!-- ### Application Credentials -->
### Application Credentials

<!-- In order to establish a connection to Reverb, a set of Reverb "application" credentials must be exchanged between the client and server. These credentials are configured on the server and are used to verify the request from the client. You may define these credentials using the following environment variables: -->
리버브 서버와 연결을 맺으려면 클라이언트와 서버 간에 리버브 "애플리케이션" 자격 증명을 교환해야 합니다. 이 자격 증명은 서버 측에서 설정되며, 클라이언트의 요청을 검증하는 데 사용됩니다. 다음과 같은 환경 변수로 이 자격 증명을 지정할 수 있습니다.

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
<!-- ### Allowed Origins -->
### Allowed Origins

<!-- You may also define the origins from which client requests may originate by updating the value of the `allowed_origins` configuration value within the `apps` section of the `config/reverb.php` configuration file. Any requests from an origin not listed in your allowed origins will be rejected. You may allow all origins using `*`: -->
클라이언트 요청이 허용되는 오리진(origin)을 지정하고 싶다면, `config/reverb.php` 설정 파일의 `apps` 섹션에 있는 `allowed_origins` 값을 수정하면 됩니다. 해당 리스트에 포함되지 않은 오리진에서의 요청은 모두 거부됩니다. 모든 오리진에서의 요청을 허용하고 싶다면 `*`를 사용할 수 있습니다.

```php
'apps' => [
    [
        'id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]
```

<a name="additional-applications"></a>
<!-- ### Additional Applications -->
### Additional Applications

<!-- Typically, Reverb provides a WebSocket server for the application in which it is installed. However, it is possible to serve more than one application using a single Reverb installation. -->
일반적으로 리버브는 설치된 애플리케이션의 WebSocket 서버 역할만 수행합니다. 그러나 하나의 리버브 인스턴스로 여러 애플리케이션을 동시에 서비스할 수도 있습니다.

<!-- For example, you may wish to maintain a single Laravel application which, via Reverb, provides WebSocket connectivity for multiple applications. This can be achieved by defining multiple `apps` in your application's `config/reverb.php` configuration file: -->
예를 들어, 하나의 Laravel 애플리케이션이 리버브를 통해 여러 개의 다른 애플리케이션에 WebSocket 연결을 제공하도록 구성할 수 있습니다. 이를 위해서는 `config/reverb.php` 파일 내에 여러 개의 `apps`를 정의하면 됩니다.

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

<!-- In most cases, secure WebSocket connections are likely handled by an upstream web server (Nginx, etc.) before the request is proxied to your Reverb server. -->
대부분의 경우, 보안 WebSocket 연결(wss://)은 리버브 서버 앞단의 웹 서버(Nginx 등)에서 처리한 후, 리버브 서버로 프록시 요청을 전달하는 방식으로 동작합니다.

<!-- However, it can sometimes be useful, such as during local development, for the Reverb server to handle secure connections directly. If you are using [Laravel Herd's](https://herd.laravel.com) secure site functionality, or you are using [Laravel Valet](/docs/10.x/valet) and have run the [secure command](/docs/10.x/valet#securing-sites) against your application, you may use the Herd / Valet certificate generated for your site to secure your Reverb connections. To do so, set the `REVERB_HOST` environment variable to your site's hostname or explicitly pass the hostname option when starting the Reverb server: -->
하지만, 예를 들어 로컬 개발 환경처럼 리버브 서버가 직접 보안 연결을 처리해야 하는 상황이 있을 수 있습니다. 만약 [Laravel Herd's](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나, [Laravel Valet](/docs/10.x/valet)에서 [secure command](/docs/10.x/valet#securing-sites)를 실행했다면, 사이트용으로 생성된 Herd/Valet 인증서를 리버브 연결 보안에 그대로 사용할 수 있습니다. 이때는 `REVERB_HOST` 환경 변수를 사이트의 호스트명으로 설정하거나, 리버브 서버 실행 시 hostname 옵션을 명시적으로 전달하면 됩니다.

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

<!-- Since Herd and Valet domains resolve to `localhost`, running the commmand above will result in your Reverb server being accessible via the secure WebSocket protocol (wss) at `wss://laravel.test:8080`. -->
Herd와 Valet의 도메인은 `localhost`로 resolve되므로, 위 명령을 실행하면 리버브 서버는 보안 WebSocket 프로토콜(wss)로 `wss://laravel.test:8080`에서 접속이 가능합니다.

<!-- You may also manually choose a certificate by defining `tls` options in your application's `config/reverb.php` configuration file. Within the array of `tls` options, you may provide any of the options supported by [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php): -->
또한, `config/reverb.php` 설정 파일의 `tls` 옵션을 직접 지정하여 원하는 인증서를 지정할 수도 있습니다. `tls` 옵션 배열에는 [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 어떤 옵션이든 지정할 수 있습니다.

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
리버브 서버는 `reverb:start` 아티즌 명령어로 실행할 수 있습니다.

```sh
php artisan reverb:start
```

<!-- By default, the Reverb server will be started at `0.0.0.0:8080`, making it accessible from all network interfaces. -->
기본적으로 리버브 서버는 `0.0.0.0:8080`에서 시작되며, 이로 인해 모든 네트워크 인터페이스에서 접근할 수 있습니다.

<!-- If you need to specify a custom host or port, you may do so via the `--host` and `--port` options when starting the server: -->
별도의 호스트나 포트를 지정해야 한다면, 서버 실행 시 `--host`와 `--port` 옵션을 사용할 수 있습니다.

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

<!-- Alternatively, you may define `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables in your application's `.env` configuration file. -->
또는, 애플리케이션의 `.env` 설정 파일에 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT` 환경 변수를 정의할 수도 있습니다.

<!-- The `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables should not be confused with `REVERB_HOST` and `REVERB_PORT`. The former specify the host and port on which to run the Reverb server itself, while the latter pair instruct Laravel where to send broadcast messages. For example, in a production environment, you may route requests from your public Reverb hostname on port `443` to a Reverb server operating on `0.0.0.0:8080`. In this scenario, your environment variables would be defined as follows: -->
여기서 `REVERB_SERVER_HOST`와 `REVERB_SERVER_PORT`는 리버브 서버 자체가 운영되는 호스트와 포트를 지정하는 것이고, `REVERB_HOST`와 `REVERB_PORT`는 Laravel이 브로드캐스트 메시지를 보낼 대상을 지정하는 것임에 주의해야 합니다. 예를 들어 운영 환경에서는, 퍼블릭 리버브 호스트의 `443` 포트로 들어온 요청을 `0.0.0.0:8080`에서 동작하는 리버브 서버로 전달할 수 있습니다. 이런 경우 환경 변수는 다음과 같이 정의됩니다.

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
성능을 높이기 위해 리버브는 기본적으로 디버그 정보를 출력하지 않습니다. 리버브 서버를 통과하는 데이터 스트림을 확인하고 싶을 때는, `reverb:start` 명령어에 `--debug` 옵션을 추가하면 됩니다.

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
<!-- ### Restarting -->
### Restarting

<!-- Since Reverb is a long-running process, changes to your code will not be reflected without restarting the server via the `reverb:restart` Artisan command. -->
리버브는 장시간 실행되는 프로세스이므로, 코드를 변경해도 서버를 재시작하지 않으면 변경 사항이 적용되지 않습니다. 이럴 때는 `reverb:restart` 아티즌 명령어를 사용해 서버를 재시작해야 합니다.

<!-- The `reverb:restart` command ensures all connections are gracefully terminated before stopping the server. If you are running Reverb with a process manager such as Supervisor, the server will be automatically restarted by the process manager after all connections have been terminated: -->
`reverb:restart` 명령은 모든 연결을 정상적으로 종료한 후 서버를 종료합니다. Supervisor 같은 프로세스 관리 도구로 리버브를 실행 중이라면, 연결이 모두 종료된 후 프로세스 관리자가 자동으로 서버를 다시 시작하게 됩니다.

```sh
php artisan reverb:restart
```

<a name="production"></a>
<!-- ## Running Reverb in Production -->
## Running Reverb in Production

<!-- Due to the long-running nature of WebSocket servers, you may need to make some optimizations to your server and hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the resources available on your server. -->
WebSocket 서버의 특성상, 리버브 서버가 각 서버의 리소스에 맞게 충분한 수의 연결을 처리할 수 있도록 하기 위해, 서버 및 호스팅 환경에 추가 최적화 작업이 필요할 수 있습니다.

> [!NOTE]
> 만약 [Laravel Forge](https://forge.laravel.com)로 사이트를 관리 중이라면, "Application" 패널에서 리버브 통합 기능을 활성화하여 서버를 자동으로 최적화할 수 있습니다. 이 기능을 켜면, 필요한 확장 프로그램 설치 및 연결 허용 수 조정 등 서버를 운영 환경에 맞게 자동으로 구성해줍니다.

<a name="open-files"></a>
<!-- ### Open Files -->
### Open Files

<!-- Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. However, there are often limits on the number of allowed open files at both the operating system and application level. -->
각 WebSocket 연결은 클라이언트나 서버가 연결을 끊을 때까지 메모리에 유지됩니다. 유닉스 및 유닉스 계열 환경에서는, 각 연결이 하나의 파일로 표현됩니다. 그런데 운영 체제 및 애플리케이션 수준에서 동시에 열 수 있는 파일 수에는 보통 제한이 있습니다.

<a name="operating-system"></a>
<!-- #### Operating System -->
#### Operating System

<!-- On a Unix based operating system, you may determine the allowed number of open files using the `ulimit` command: -->
유닉스 계열 운영체제에서는 `ulimit` 명령어를 통해 허용된 오픈 파일 수를 확인할 수 있습니다.

```sh
ulimit -n
```

<!-- This command will display the open file limits allowed for different users. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like the following: -->
이 명령어는 사용자별로 허용된 오픈 파일 제한을 보여줍니다. 제한값을 변경하려면 `/etc/security/limits.conf` 파일을 편집하면 됩니다. 예를 들어, `forge` 사용자에 대한 오픈 파일 최대치를 10,000으로 늘리려면 다음과 같이 설정합니다.

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
<!-- ### Event Loop -->
### Event Loop

<!-- Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select`, which doesn't require any additional extensions. However, `stream_select` is typically limited to 1,024 open files. As such, if you plan to handle more than 1,000 concurrent connections, you will need to use an alternative event loop not bound by the same restrictions. -->
리버브는 내부적으로 ReactPHP 이벤트 루프(event loop)를 사용해 서버에서 WebSocket 연결을 관리합니다. 기본적으로는 추가 확장 모듈이 필요 없는 `stream_select` 기반의 루프가 동작합니다. 하지만 `stream_select`는 일반적으로 1,024개의 오픈 파일까지만 지원합니다. 따라서 1,000개 이상의 동시 연결이 필요하다면 제한을 받지 않는 다른 이벤트 루프를 사용해야 합니다.

<!-- Reverb will automatically switch to an `ext-event`, `ext-ev`, or `ext-uv` powered loop when available. All of these PHP extensions are available for install via PECL: -->
리버브는 `ext-event`, `ext-ev`, 또는 `ext-uv` PHP 확장 프로그램이 설치되어 있을 경우 자동으로 이를 사용하도록 전환합니다. 이 확장들은 PECL을 통해 설치할 수 있습니다.

```sh
pecl install event
# or
pecl install ev
# or
pecl install uv
```

<a name="web-server"></a>
<!-- ### Web Server -->
### Web Server

<!-- In most cases, Reverb runs on a non web-facing port on your server. So, in order to route traffic to Reverb, you should configure a reverse proxy. Assuming Reverb is running on host `0.0.0.0` and port `8080` and your server utilizes the Nginx web server, a reverse proxy can be defined for your Reverb server using the following Nginx site configuration: -->
대부분의 경우, 리버브는 서버에서 직접 외부에 노출되지 않는 비공개 포트에서 실행됩니다. 따라서 트래픽을 리버브로 라우팅하려면 리버스 프록시를 설정해야 합니다. 예를 들어 리버브를 호스트 `0.0.0.0`, 포트 `8080`에서 실행 중이고 서버가 Nginx 웹 서버를 사용한다면, 다음과 같이 해당 사이트의 Nginx 설정 파일에서 리버스 프록시를 지정할 수 있습니다.

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

<!-- Typically, web servers are configured to limit the number of allowed connections in order to prevent overloading the server. To increase the number of allowed connections on an Nginx web server to 10,000, the `worker_rlimit_nofile` and `worker_connections` values of the `nginx.conf` file should be updated: -->
대부분의 웹 서버에는 과도한 서버 리소스 사용을 막기 위해 연결 수 제한이 기본적으로 적용되어 있습니다. Nginx에서 허용 가능한 연결 수를 10,000개로 늘리려면, `nginx.conf` 파일 내 `worker_rlimit_nofile` 및 `worker_connections` 값을 다음과 같이 조정하면 됩니다.

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
위 설정을 적용하면 Nginx 프로세스당 최대 10,000개의 워커가 생성될 수 있으며, 오픈 파일 제한도 10,000개로 설정됩니다.

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- Unix-based operating systems typically limit the number of ports which can be opened on the server. You may see the current allowed range via the following command: -->
유닉스 계열 운영체제에서는 서버에서 열 수 있는 포트 수에도 한계가 있습니다. 아래 명령어를 통해 현재 허용된 포트 범위를 확인할 수 있습니다.

 ```sh
 cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

<!-- The output above shows the server can handle a maximum of 28,231 (60,999 - 32,768) connections since each connection requires a free port. Although we recommend [horizontal scaling](#scaling) to increase the number of allowed connections, you may increase the number of available open ports by updating the allowed port range in your server's `/etc/sysctl.conf` configuration file. -->
위 출력에서 60,999에서 32,768을 뺀 28,231개의 연결이 가능함을 알 수 있습니다. (각 연결마다 사용 가능한 포트가 필요하기 때문입니다.) 더 많은 연결이 필요할 경우, [horizontal scaling](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 파일에서 포트 범위를 늘려 허용 가능한 오픈 포트 수 자체를 늘릴 수도 있습니다.

<a name="process-management"></a>
<!-- ### Process Management -->
### Process Management

<!-- In most cases, you should use a process manager such as Supervisor to ensure the Reverb server is continually running. If you are using Supervisor to run Reverb, you should update the `minfds` setting of your server's `supervisor.conf` file to ensure Supervisor is able to open the files required to handle connections to your Reverb server: -->
대부분의 경우, 리버브 서버가 항상 실행되도록 Supervisor 같은 프로세스 관리 도구를 사용하는 것이 좋습니다. Supervisor로 리버브를 실행하는 경우, 서버의 `supervisor.conf` 파일에서 `minfds` 옵션 값을 늘려, 리버브 서버가 필요한 만큼 파일을 열 수 있도록 해야 합니다.

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
<!-- ### Scaling -->
### Scaling

<!-- If you need to handle more connections than a single server will allow, you may scale your Reverb server horizontally. Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers. When a message is received by one of your application's Reverb servers, the server will use Redis to publish the incoming message to all other servers. -->
단일 서버에서 처리할 수 있는 연결 수 이상의 동시 연결이 필요하다면, 리버브 서버를 수평 확장할 수 있습니다. Redis의 publish/subscribe 기능을 활용하여, 여러 서버에 걸쳐 연결을 처리할 수 있습니다. 하나의 리버브 서버가 메시지를 수신하면, Redis를 통해 해당 메시지를 모든 다른 서버에도 브로드캐스팅합니다.

<!-- To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` environment variable to `true` in your application's `.env` configuration file: -->
수평 확장을 활성화하려면, 애플리케이션의 `.env` 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정해야 합니다.

```env
REVERB_SCALING_ENABLED=true
```

<!-- Next, you should have a dedicated, central Redis server to which all of the Reverb servers will communicate. Reverb will use the [default Redis connection configured for your application](/docs/10.x/redis#configuration) to publish messages to all of your Reverb servers. -->
그 다음, 모든 리버브 서버가 접근할 수 있는 전용 중앙 Redis 서버를 준비해야 합니다. 리버브는 [default Redis connection configured for your application](/docs/10.x/redis#configuration)을 사용해 모든 리버브 서버에 메시지를 전파합니다.

<!-- Once you have enabled Reverb's scaling option and configured a Redis server, you may simply invoke the `reverb:start` command on multiple servers that are able to communicate with your Redis server. These Reverb servers should be placed behind a load balancer that distributes incoming requests evenly among the servers. -->
이제 리버브 스케일링 옵션을 활성화하고 Redis 서버 설정까지 완료했다면, Redis와 통신 가능한 여러 대의 서버에서 각각 `reverb:start` 명령을 실행하면 됩니다. 이러한 리버브 서버들은 로드 밸런서 뒤에 두어, 들어오는 요청이 여러 서버에 균등하게 분산되도록 해야 합니다.
