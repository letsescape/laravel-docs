# Laravel Reverb (Laravel Reverb)

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
    - [アプリケーションの資格情報](#application-credentials)
    - [許可されたオリジン](#allowed-origins)
    - [追加のアプリケーション](#additional-applications)
    - [SSL](#ssl)
- [サーバーの実行](#running-server)
    - [Debugging](#debugging)
    - [Restarting](#restarting)
- [Monitoring](#monitoring)
- [本番環境でReverbを実行する](#production)
    - [ファイルを開く](#open-files)
    - [イベントループ](#event-loop)
    - [ウェブサーバー](#web-server)
    - [Ports](#ports)
    - [プロセス管理](#process-management)
    - [Scaling](#scaling)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Reverb](https://github.com/laravel/reverb) は、超高速でスケーラブルなリアルタイム WebSocket 通信を Laravel アプリケーションに直接もたらし、Laravel の既存の [イベント配信ツール](/docs/{{version}}/broadcasting) スイートとのシームレスな統合を提供します。

<a name="installation"></a>
## インストール (Installation)

`install:broadcasting` Artisan コマンドを使用してReverbをインストールできます。

```
php artisan install:broadcasting
```

<a name="configuration"></a>
## 構成 (Configuration)

バックグラウンドでは、`install:broadcasting` Artisan コマンドが `reverb:install` コマンドを実行し、適切なデフォルト設定オプションのセットを使用して Reverb をインストールします。設定を変更したい場合は、Reverb の環境変数を更新するか、`config/reverb.php` 設定ファイルを更新することで変更できます。

<a name="application-credentials"></a>
### アプリケーションの資格情報

Reverb への接続を確立するには、クライアントとサーバーの間で Reverb の「アプリケーション」資格情報のセットを交換する必要があります。これらの資格情報はサーバー上で構成され、クライアントからの要求を検証するために使用されます。これらの資格情報は、次の環境変数を使用して定義できます。

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret
```

<a name="allowed-origins"></a>
### 許可されたオリジン

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
### 追加のアプリケーション

通常、Reverb は、インストールされているアプリケーションに WebSocket サーバーを提供します。ただし、単一の Reverb インストールを使用して複数のアプリケーションを提供することは可能です。

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
### SSL

ほとんどの場合、安全な WebSocket 接続は、リクエストが Reverb サーバーにプロキシされる前に、上流の Web サーバー (Nginx など) によって処理されます。

ただし、ローカル開発中など、Reverb サーバーが安全な接続を直接処理すると便利な場合があります。 [Laravel・ハードの](https://herd.laravel.com) セキュア サイト機能を使用している場合、または [Laravel Valet](/docs/{{version}}/valet) を使用していてアプリケーションに対して [安全なコマンド](/docs/{{version}}/valet#securing-sites) を実行している場合は、サイト用に生成された Herd / Valet 証明書を使用して Reverb 接続を保護できます。これを行うには、`REVERB_HOST` 環境変数をサイトのホスト名に設定するか、Reverb サーバーの起動時にホスト名オプションを明示的に渡します。

```sh
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"
```

Herd ドメインと Valet ドメインは `localhost` に解決されるため、上記のコマンドを実行すると、`wss://laravel.test:8080` で安全な WebSocket プロトコル (`wss`) を介して Reverb サーバーにアクセスできるようになります。

アプリケーションの `config/reverb.php` 構成ファイルで `tls` オプションを定義して、証明書を手動で選択することもできます。 `tls` オプションの配列内で、[PHP の SSL コンテキスト オプション](https://www.php.net/manual/en/context.ssl.php) でサポートされているオプションのいずれかを指定できます。

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],
```

<a name="running-server"></a>
## サーバーの実行 (Running the Server)

Reverb サーバーは、`reverb:start` Artisan コマンドを使用して起動できます。

```sh
php artisan reverb:start
```

デフォルトでは、Reverb サーバーは `0.0.0.0:8080` で起動され、すべてのネットワーク インターフェイスからアクセスできるようになります。

カスタム ホストまたはポートを指定する必要がある場合は、サーバーの起動時に `--host` および `--port` オプションを使用して指定できます。

```sh
php artisan reverb:start --host=127.0.0.1 --port=9000
```

あるいは、アプリケーションの `.env` 構成ファイルで `REVERB_SERVER_HOST` および `REVERB_SERVER_PORT` 環境変数を定義することもできます。

`REVERB_SERVER_HOST` および `REVERB_SERVER_PORT` 環境変数を、`REVERB_HOST` および `REVERB_PORT` と混同しないでください。前者はReverbサーバー自体を実行するホストとポートを指定し、後者のペアはブロードキャストメッセージの送信先をLaravelに指示します。たとえば、運用環境では、ポート `443` のパブリック Reverb ホスト名からのリクエストを、`0.0.0.0:8080` で動作する Reverb サーバーにルーティングできます。このシナリオでは、環境変数は次のように定義されます。

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443
```

<a name="debugging"></a>
### デバッグ

パフォーマンスを向上させるために、Reverb はデフォルトではデバッグ情報を出力しません。 Reverb サーバーを通過するデータのストリームを確認したい場合は、`--debug` オプションを `reverb:start` コマンドに指定できます。

```sh
php artisan reverb:start --debug
```

<a name="restarting"></a>
### 再起動中

Reverb は長時間実行されるプロセスであるため、`reverb:restart` Artisan コマンドを使用してサーバーを再起動しない限り、コードへの変更は反映されません。

`reverb:restart` コマンドは、サーバーを停止する前にすべての接続が正常に終了することを保証します。 Supervisor などのプロセス マネージャーを使用して Reverb を実行している場合、すべての接続が終了した後、サーバーはプロセス マネージャーによって自動的に再起動されます。

```sh
php artisan reverb:restart
```

<a name="monitoring"></a>
## 監視 (Monitoring)

Reverbは、[Laravel Pulse](/docs/{{version}}/pulse) との統合を通じてモニタリングできます。 Reverb の Pulse 統合を有効にすると、サーバーによって処理される接続とメッセージの数を追跡できます。

統合を有効にするには、まず [インストールされたPulse](/docs/{{version}}/pulse#installation) があることを確認する必要があります。次に、Reverb のレコーダーのいずれかをアプリケーションの `config/pulse.php` 構成ファイルに追加します。

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

次に、各レコーダーの Pulse カードを [Pulseダッシュボード](/docs/{{version}}/pulse#dashboard-customization) に追加します。

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>
```

接続アクティビティは、定期的に新しい更新をポーリングすることによって記録されます。この情報が Pulse ダッシュボードに正しく表示されるようにするには、Reverb サーバーで `pulse:check` デーモンを実行する必要があります。 [水平方向に拡大縮小した](#scaling) 構成で Reverb を実行している場合は、このデーモンをサーバーの 1 つでのみ実行する必要があります。

<a name="production"></a>
## 本番環境でReverbを実行する (Running Reverb in Production)

WebSocket サーバーは長時間実行される性質があるため、Reverb サーバーがサーバー上で利用可能なリソースに対して最適な接続数を効果的に処理できるように、サーバーとホスティング環境を最適化する必要がある場合があります。

> [!NOTE]  
> サイトが [Laravel Forge](https://forge.laravel.com) によって管理されている場合は、[アプリケーション] パネルから直接サーバーをReverb用に自動的に最適化できます。 Reverb 統合を有効にすることで、Forge は、必要な拡張機能のインストールや許可される接続数の増加など、サーバーを運用準備が整った状態にします。

<a name="open-files"></a>
### ファイルを開く

各 WebSocket 接続は、クライアントまたはサーバーのいずれかが切断されるまでメモリ内に保持されます。 Unix および Unix 類似の環境では、各接続はファイルによって表されます。ただし、多くの場合、オペレーティング システム レベルとアプリケーション レベルの両方で、開くことを許可されるファイルの数に制限があります。

<a name="operating-system"></a>
#### オペレーティング·システム

Unix ベースのオペレーティング システムでは、`ulimit` コマンドを使用して、開くことのできるファイルの数を決定できます。

```sh
ulimit -n
```

このコマンドは、さまざまなユーザーに許可されているオープン ファイルの制限を表示します。これらの値は、`/etc/security/limits.conf` ファイルを編集することで更新できます。たとえば、`forge` ユーザーのオープン ファイルの最大数を 10,000 に更新すると、次のようになります。

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000
```

<a name="event-loop"></a>
### イベントループ

内部では、Reverb は ReactPHP イベント ループを使用してサーバー上の WebSocket 接続を管理します。デフォルトでは、このイベント ループは `stream_select` によって強化されており、追加の拡張機能は必要ありません。ただし、`stream_select` は通常、開いているファイルの数が 1,024 に制限されています。そのため、1,000 を超える同時接続を処理する予定がある場合は、同じ制限に束縛されない代替イベント ループを使用する必要があります。

利用可能な場合、Reverbは自動的に `ext-uv` パワード ループに切り替わります。この PHP 拡張機能は、PECL 経由でインストールできます。

```sh
pecl install uv
```

<a name="web-server"></a>
### ウェブサーバー

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

上記の構成では、プロセスごとに最大 10,000 個の Nginx ワーカーを生成できます。さらに、この構成では、Nginx のオープン ファイル制限が 10,000 に設定されます。

<a name="ports"></a>
### ポート

Unix ベースのオペレーティング システムでは、通常、サーバー上で開くことができるポートの数が制限されています。次のコマンドを使用して、現在の許可範囲を確認できます。

 ```sh
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999
```

上記の出力は、各接続に空きポートが必要なため、サーバーが最大 28,231 (60,999 ～ 32,768) の接続を処理できることを示しています。許可される接続数を増やすには [水平スケーリング](#scaling) をお勧めしますが、サーバーの `/etc/sysctl.conf` 構成ファイルで許可されるポート範囲を更新することで、使用可能なオープン ポートの数を増やすこともできます。

<a name="process-management"></a>
### プロセス管理

ほとんどの場合、Reverb サーバーが継続的に実行されるようにするには、Supervisor などのプロセス マネージャーを使用する必要があります。 Supervisor を使用して Reverb を実行している場合は、サーバーの `supervisor.conf` ファイルの `minfds` 設定を更新して、Reverb サーバーへの接続を処理するために必要なファイルを Supervisor が確実に開けるようにする必要があります。

```ini
[supervisord]
...
minfds=10000
```

<a name="scaling"></a>
### スケーリング

単一サーバーで許容されるより多くの接続を処理する必要がある場合は、Reverb サーバーを水平方向に拡張できます。 Redis のパブリッシュ/サブスクライブ機能を利用して、Reverb は複数のサーバー間の接続を管理できます。アプリケーションの Reverb サーバーの 1 つでメッセージが受信されると、サーバーは Redis を使用して受信メッセージを他のすべてのサーバーにパブリッシュします。

水平スケーリングを有効にするには、アプリケーションの `.env` 構成ファイルで `REVERB_SCALING_ENABLED` 環境変数を `true` に設定する必要があります。

```env
REVERB_SCALING_ENABLED=true
```

次に、すべての Reverb サーバーが通信する専用の中央 Redis サーバーを用意する必要があります。 Reverb は [アプリケーション用に構成されたデフォルトの Redis 接続](/docs/{{version}}/redis#configuration) を使用して、すべての Reverb サーバーにメッセージをパブリッシュします。

Reverb のスケーリング オプションを有効にして Redis サーバーを構成したら、Redis サーバーと通信できる複数のサーバー上で `reverb:start` コマンドを呼び出すだけで済みます。これらの Reverb サーバーは、受信リクエストをサーバー間で均等に分散するロード バランサーの背後に配置する必要があります。

