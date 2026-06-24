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
[Laravel Reverb](https://github.com/laravel/reverb) は、超高速でスケーラブルなリアルタイム WebSocket 通信を Laravel アプリケーションに直接もたらし、Laravel の既存の [event broadcasting tools](/docs/11.x/broadcasting) スイートとのシームレスな統合を提供します。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Reverb using the `install:broadcasting` Artisan command: -->
`install:broadcasting` Artisan コマンドを使用してReverbをインストールできます。

```
php artisan install:broadcasting
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Behind the scenes, the `install:broadcasting` Artisan command will run the `reverb:install` command, which will install Reverb with a sensible set of default configuration options. If you would like to make any configuration changes, you may do so by updating Reverb's environment variables or by updating the `config/reverb.php` configuration file. -->
バックグラウンドでは、`install:broadcasting` Artisan コマンドが `reverb:install` コマンドを実行し、適切なデフォルト設定オプションのセットを使用して Reverb をインストールします。設定を変更したい場合は、Reverb の環境変数を更新するか、`config/reverb.php` 設定ファイルを更新することで変更できます。

<a name="application-credentials"></a>
<!-- ### Application Credentials -->
### Application Credentials

<!-- In order to establish a connection to Reverb, a set of Reverb "application" credentials must be exchanged between the client and server. These credentials are configured on the server and are used to verify the request from the client. You may define these credentials using the following environment variables: -->
Reverb への接続を確立するには、クライアントとサーバーの間で Reverb の「アプリケーション」資格情報のセットを交換する必要があります。これらの資格情報はサーバー上で構成され、クライアントからの要求を検証するために使用されます。これらの資格情報は、次の環境変数を使用して定義できます。

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
<!-- ### Allowed Origins -->
### Allowed Origins

<!-- You may also define the origins from which client requests may originate by updating the value of the `allowed_origins` configuration value within the `apps` section of the `config/reverb.php` configuration file. Any requests from an origin not listed in your allowed origins will be rejected. You may allow all origins using `*`: -->
`config/reverb.php` 構成ファイルの `apps` セクション内の `allowed_origins` 構成値の値を更新することで、クライアント リクエストの発信元を定義することもできます。許可されたオリジンにリストされていないオリジンからのリクエストは拒否されます。 `*` を使用して、すべてのオリジンを許可できます。

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
通常、Reverb は、インストールされているアプリケーションに WebSocket サーバーを提供します。ただし、単一の Reverb インストールを使用して複数のアプリケーションを提供することは可能です。

<!-- For example, you may wish to maintain a single Laravel application which, via Reverb, provides WebSocket connectivity for multiple applications. This can be achieved by defining multiple `apps` in your application's `config/reverb.php` configuration file: -->
たとえば、Reverb を介して複数のアプリケーションに WebSocket 接続を提供する単一の Laravel アプリケーションを維持したい場合があります。これは、アプリケーションの `config/reverb.php` 構成ファイルで複数の `apps` を定義することで実現できます。

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
ほとんどの場合、安全な WebSocket 接続は、リクエストが Reverb サーバーにプロキシされる前に、上流の Web サーバー (Nginx など) によって処理されます。

<!-- However, it can sometimes be useful, such as during local development, for the Reverb server to handle secure connections directly. If you are using [Laravel Herd's](https://herd.laravel.com) secure site feature or you are using [Laravel Valet](/docs/11.x/valet) and have run the [secure command](/docs/11.x/valet#securing-sites) against your application, you may use the Herd / Valet certificate generated for your site to secure your Reverb connections. To do so, set the `REVERB_HOST` environment variable to your site's hostname or explicitly pass the hostname option when starting the Reverb server: -->
ただし、ローカル開発中など、Reverb サーバーが安全な接続を直接処理すると便利な場合があります。 [Laravel Herd's](https://herd.laravel.com) のセキュア サイト機能を使用している場合、または [Laravel Valet](/docs/11.x/valet) を使用していてアプリケーションに対して [secure command](/docs/11.x/valet#securing-sites) を実行している場合は、サイト用に生成された Herd / Valet 証明書を使用して Reverb 接続を保護できます。これを行うには、`REVERB_HOST` 環境変数をサイトのホスト名に設定するか、Reverb サーバーの起動時にホスト名オプションを明示的に渡します。

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

<!-- Since Herd and Valet domains resolve to `localhost`, running the command above will result in your Reverb server being accessible via the secure WebSocket protocol (`wss`) at `wss://laravel.test:8080`. -->
Herd ドメインと Valet ドメインは `localhost` に解決されるため、上記のコマンドを実行すると、`wss://laravel.test:8080` で安全な WebSocket プロトコル (`wss`) を介して Reverb サーバーにアクセスできるようになります。

<!-- You may also manually choose a certificate by defining `tls` options in your application's `config/reverb.php` configuration file. Within the array of `tls` options, you may provide any of the options supported by [PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php): -->
アプリケーションの `config/reverb.php` 構成ファイルで `tls` オプションを定義して、証明書を手動で選択することもできます。 `tls` オプションの配列内で、[PHP's SSL context options](https://www.php.net/manual/en/context.ssl.php) でサポートされているオプションのいずれかを指定できます。

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
Reverb サーバーは、`reverb:start` Artisan コマンドを使用して起動できます。

```sh
php artisan reverb:start
```

<!-- By default, the Reverb server will be started at `0.0.0.0:8080`, making it accessible from all network interfaces. -->
デフォルトでは、Reverb サーバーは `0.0.0.0:8080` で起動され、すべてのネットワーク インターフェイスからアクセスできるようになります。

<!-- If you need to specify a custom host or port, you may do so via the `--host` and `--port` options when starting the server: -->
カスタム ホストまたはポートを指定する必要がある場合は、サーバーの起動時に `--host` および `--port` オプションを使用して指定できます。

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

<!-- Alternatively, you may define `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables in your application's `.env` configuration file. -->
あるいは、アプリケーションの `.env` 構成ファイルで `REVERB_SERVER_HOST` および `REVERB_SERVER_PORT` 環境変数を定義することもできます。

<!-- The `REVERB_SERVER_HOST` and `REVERB_SERVER_PORT` environment variables should not be confused with `REVERB_HOST` and `REVERB_PORT`. The former specify the host and port on which to run the Reverb server itself, while the latter pair instruct Laravel where to send broadcast messages. For example, in a production environment, you may route requests from your public Reverb hostname on port `443` to a Reverb server operating on `0.0.0.0:8080`. In this scenario, your environment variables would be defined as follows: -->
`REVERB_SERVER_HOST` および `REVERB_SERVER_PORT` 環境変数を、`REVERB_HOST` および `REVERB_PORT` と混同しないでください。前者はReverbサーバー自体を実行するホストとポートを指定し、後者のペアはブロードキャストメッセージの送信先をLaravelに指示します。たとえば、運用環境では、ポート `443` のパブリック Reverb ホスト名からのリクエストを、`0.0.0.0:8080` で動作する Reverb サーバーにルーティングできます。このシナリオでは、環境変数は次のように定義されます。

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
パフォーマンスを向上させるために、Reverb はデフォルトではデバッグ情報を出力しません。 Reverb サーバーを通過するデータのストリームを確認したい場合は、`--debug` オプションを `reverb:start` コマンドに指定できます。

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
<!-- ### Restarting -->
### Restarting

<!-- Since Reverb is a long-running process, changes to your code will not be reflected without restarting the server via the `reverb:restart` Artisan command. -->
Reverb は長時間実行されるプロセスであるため、`reverb:restart` Artisan コマンドを使用してサーバーを再起動しない限り、コードへの変更は反映されません。

<!-- The `reverb:restart` command ensures all connections are gracefully terminated before stopping the server. If you are running Reverb with a process manager such as Supervisor, the server will be automatically restarted by the process manager after all connections have been terminated: -->
`reverb:restart` コマンドは、サーバーを停止する前にすべての接続が正常に終了することを保証します。 Supervisor などのプロセス マネージャーを使用して Reverb を実行している場合、すべての接続が終了した後、サーバーはプロセス マネージャーによって自動的に再起動されます。

```sh
php artisan reverb:restart
```

<a name="monitoring"></a>
<!-- ## Monitoring -->
## Monitoring

<!-- Reverb may be monitored via an integration with [Laravel Pulse](/docs/11.x/pulse). By enabling Reverb's Pulse integration, you may track the number of connections and messages being handled by your server. -->
Reverbは、[Laravel Pulse](/docs/11.x/pulse) との統合を通じてモニタリングできます。 Reverb の Pulse 統合を有効にすると、サーバーによって処理される接続とメッセージの数を追跡できます。

<!-- To enable the integration, you should first ensure you have [installed Pulse](/docs/11.x/pulse#installation). Then, add any of Reverb's recorders to your application's `config/pulse.php` configuration file: -->
統合を有効にするには、まず [installed Pulse](/docs/11.x/pulse#installation) があることを確認する必要があります。次に、Reverb のレコーダーのいずれかをアプリケーションの `config/pulse.php` 構成ファイルに追加します。

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
次に、各レコーダーの Pulse カードを [Pulse dashboard](/docs/11.x/pulse#dashboard-customization) に追加します。

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

<!-- Connection activity is recorded by polling for new updates on a periodic basis. To ensure this information is rendered correctly on the Pulse dashboard, you must run the `pulse:check` daemon on your Reverb server. If you are running Reverb in a [horizontally scaled](#scaling) configuration, you should only run this daemon on one of your servers. -->
接続アクティビティは、定期的に新しい更新をポーリングすることによって記録されます。この情報が Pulse ダッシュボードに正しく表示されるようにするには、Reverb サーバーで `pulse:check` デーモンを実行する必要があります。 [horizontally scaled](#scaling) 構成で Reverb を実行している場合は、このデーモンをサーバーの 1 つでのみ実行する必要があります。

<a name="production"></a>
<!-- ## Running Reverb in Production -->
## Running Reverb in Production

<!-- Due to the long-running nature of WebSocket servers, you may need to make some optimizations to your server and hosting environment to ensure your Reverb server can effectively handle the optimal number of connections for the resources available on your server. -->
WebSocket サーバーは長時間実行される性質があるため、Reverb サーバーがサーバー上で利用可能なリソースに対して最適な接続数を効果的に処理できるように、サーバーとホスティング環境を最適化する必要がある場合があります。

> [!NOTE]
> サイトが [Laravel Forge](https://forge.laravel.com) によって管理されている場合は、[アプリケーション] パネルから直接サーバーをReverb用に自動的に最適化できます。 Reverb 統合を有効にすることで、Forge は、必要な拡張機能のインストールや許可される接続数の増加など、サーバーを運用準備が整った状態にします。

<a name="open-files"></a>
<!-- ### Open Files -->
### Open Files

<!-- Each WebSocket connection is held in memory until either the client or server disconnects. In Unix and Unix-like environments, each connection is represented by a file. However, there are often limits on the number of allowed open files at both the operating system and application level. -->
各 WebSocket 接続は、クライアントまたはサーバーのいずれかが切断されるまでメモリ内に保持されます。 Unix および Unix 類似の環境では、各接続はファイルによって表されます。ただし、多くの場合、オペレーティング システム レベルとアプリケーション レベルの両方で、開くことを許可されるファイルの数に制限があります。

<a name="operating-system"></a>
<!-- #### Operating System -->
#### Operating System

<!-- On a Unix based operating system, you may determine the allowed number of open files using the `ulimit` command: -->
Unix ベースのオペレーティング システムでは、`ulimit` コマンドを使用して、開くことのできるファイルの数を決定できます。

```sh
ulimit -n
```

<!-- This command will display the open file limits allowed for different users. You may update these values by editing the `/etc/security/limits.conf` file. For example, updating the maximum number of open files to 10,000 for the `forge` user would look like the following: -->
このコマンドは、さまざまなユーザーに許可されているオープン ファイルの制限を表示します。これらの値は、`/etc/security/limits.conf` ファイルを編集することで更新できます。たとえば、`forge` ユーザーのオープン ファイルの最大数を 10,000 に更新すると、次のようになります。

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
<!-- ### Event Loop -->
### Event Loop

<!-- Under the hood, Reverb uses a ReactPHP event loop to manage WebSocket connections on the server. By default, this event loop is powered by `stream_select`, which doesn't require any additional extensions. However, `stream_select` is typically limited to 1,024 open files. As such, if you plan to handle more than 1,000 concurrent connections, you will need to use an alternative event loop not bound to the same restrictions. -->
内部では、Reverb は ReactPHP イベント ループを使用してサーバー上の WebSocket 接続を管理します。デフォルトでは、このイベント ループは `stream_select` によって強化されており、追加の拡張機能は必要ありません。ただし、`stream_select` は通常、開いているファイルの数が 1,024 に制限されています。そのため、1,000 を超える同時接続を処理する予定がある場合は、同じ制限に束縛されない代替イベント ループを使用する必要があります。

<!-- Reverb will automatically switch to an `ext-uv` powered loop when available. This PHP extension is available for install via PECL: -->
利用可能な場合、Reverbは自動的に `ext-uv` パワード ループに切り替わります。この PHP 拡張機能は、PECL 経由でインストールできます。

```sh
pecl install uv
```

<a name="web-server"></a>
<!-- ### Web Server -->
### Web Server

<!-- In most cases, Reverb runs on a non web-facing port on your server. So, in order to route traffic to Reverb, you should configure a reverse proxy. Assuming Reverb is running on host `0.0.0.0` and port `8080` and your server utilizes the Nginx web server, a reverse proxy can be defined for your Reverb server using the following Nginx site configuration: -->
ほとんどの場合、Reverb はサーバー上の Web に接続されていないポートで実行されます。したがって、トラフィックを Reverb にルーティングするには、リバース プロキシを構成する必要があります。 Reverb がホスト `0.0.0.0` およびポート `8080` で実行されており、サーバーが Nginx Web サーバーを利用していると仮定すると、次の Nginx サイト構成を使用して Reverb サーバーにリバース プロキシを定義できます。

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
> Reverb は、`/app` で WebSocket 接続をリッスンし、`/apps` で API リクエストを処理します。Reverb リクエストを処理する Web サーバーがこれらの URI の両方に対応できることを確認する必要があります。 [Laravel Forge](https://forge.laravel.com) を使用してサーバーを管理している場合、Reverb サーバーはデフォルトで正しく設定されます。

<!-- Typically, web servers are configured to limit the number of allowed connections in order to prevent overloading the server. To increase the number of allowed connections on an Nginx web server to 10,000, the `worker_rlimit_nofile` and `worker_connections` values of the `nginx.conf` file should be updated: -->
通常、Web サーバーは、サーバーの過負荷を防ぐために、許可される接続の数を制限するように構成されています。 Nginx Web サーバーで許可される接続数を 10,000 に増やすには、`nginx.conf` ファイルの `worker_rlimit_nofile` 値と `worker_connections` 値を更新する必要があります。

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
上記の構成では、プロセスごとに最大 10,000 個の Nginx ワーカーを生成できます。さらに、この構成では、Nginx のオープン ファイル制限が 10,000 に設定されます。

<a name="ports"></a>
<!-- ### Ports -->
### Ports

<!-- Unix-based operating systems typically limit the number of ports which can be opened on the server. You may see the current allowed range via the following command: -->
Unix ベースのオペレーティング システムでは、通常、サーバー上で開くことができるポートの数が制限されています。次のコマンドを使用して、現在の許可範囲を確認できます。

 ```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

<!-- The output above shows the server can handle a maximum of 28,231 (60,999 - 32,768) connections since each connection requires a free port. Although we recommend [horizontal scaling](#scaling) to increase the number of allowed connections, you may increase the number of available open ports by updating the allowed port range in your server's `/etc/sysctl.conf` configuration file. -->
上記の出力は、各接続に空きポートが必要なため、サーバーが最大 28,231 (60,999 ～ 32,768) の接続を処理できることを示しています。許可される接続数を増やすには [horizontal scaling](#scaling) をお勧めしますが、サーバーの `/etc/sysctl.conf` 構成ファイルで許可されるポート範囲を更新することで、使用可能なオープン ポートの数を増やすこともできます。

<a name="process-management"></a>
<!-- ### Process Management -->
### Process Management

<!-- In most cases, you should use a process manager such as Supervisor to ensure the Reverb server is continually running. If you are using Supervisor to run Reverb, you should update the `minfds` setting of your server's `supervisor.conf` file to ensure Supervisor is able to open the files required to handle connections to your Reverb server: -->
ほとんどの場合、Reverb サーバーが継続的に実行されるようにするには、Supervisor などのプロセス マネージャーを使用する必要があります。 Supervisor を使用して Reverb を実行している場合は、サーバーの `supervisor.conf` ファイルの `minfds` 設定を更新して、Reverb サーバーへの接続を処理するために必要なファイルを Supervisor が確実に開けるようにする必要があります。

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
<!-- ### Scaling -->
### Scaling

<!-- If you need to handle more connections than a single server will allow, you may scale your Reverb server horizontally. Utilizing the publish / subscribe capabilities of Redis, Reverb is able to manage connections across multiple servers. When a message is received by one of your application's Reverb servers, the server will use Redis to publish the incoming message to all other servers. -->
単一サーバーで許容されるより多くの接続を処理する必要がある場合は、Reverb サーバーを水平方向に拡張できます。 Redis のパブリッシュ/サブスクライブ機能を利用して、Reverb は複数のサーバー間の接続を管理できます。アプリケーションの Reverb サーバーの 1 つでメッセージが受信されると、サーバーは Redis を使用して受信メッセージを他のすべてのサーバーにパブリッシュします。

<!-- To enable horizontal scaling, you should set the `REVERB_SCALING_ENABLED` environment variable to `true` in your application's `.env` configuration file: -->
水平スケーリングを有効にするには、アプリケーションの `.env` 構成ファイルで `REVERB_SCALING_ENABLED` 環境変数を `true` に設定する必要があります。

```env
REVERB_SCALING_ENABLED=true
```

<!-- Next, you should have a dedicated, central Redis server to which all of the Reverb servers will communicate. Reverb will use the [default Redis connection configured for your application](/docs/11.x/redis#configuration) to publish messages to all of your Reverb servers. -->
次に、すべての Reverb サーバーが通信する専用の中央 Redis サーバーを用意する必要があります。 Reverb は [default Redis connection configured for your application](/docs/11.x/redis#configuration) を使用して、すべての Reverb サーバーにメッセージをパブリッシュします。

<!-- Once you have enabled Reverb's scaling option and configured a Redis server, you may simply invoke the `reverb:start` command on multiple servers that are able to communicate with your Redis server. These Reverb servers should be placed behind a load balancer that distributes incoming requests evenly among the servers. -->
Reverb のスケーリング オプションを有効にして Redis サーバーを構成したら、Redis サーバーと通信できる複数のサーバー上で `reverb:start` コマンドを呼び出すだけで済みます。これらの Reverb サーバーは、受信リクエストをサーバー間で均等に分散するロード バランサーの背後に配置する必要があります。

