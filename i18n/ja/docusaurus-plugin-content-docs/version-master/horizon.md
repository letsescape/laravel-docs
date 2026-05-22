# Laravel Horizon (Laravel Horizon)

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [ダッシュボードの認証](#dashboard-authorization)
    - [ジョブの最大試行回数](#max-job-attempts)
    - [ジョブのタイムアウト](#job-timeout)
    - [ジョブバックオフ](#job-backoff)
    - [サイレントジョブ](#silenced-jobs)
- [戦略のバランスを取る](#balancing-strategies)
    - [自動バランス調整](#auto-balancing)
    - [シンプルなバランス調整](#simple-balancing)
    - [バランス調整なし](#no-balancing)
- [Horizon のアップグレード](#upgrading-horizon)
- [ランニングホライゾン](#running-horizon)
    - [Horizon の導入](#deploying-horizon)
- [Tags](#tags)
- [Notifications](#notifications)
- [Metrics](#metrics)
- [失敗したジョブの削除](#deleting-failed-jobs)
- [キューからジョブをクリアする](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 導入 (Introduction)

> [!NOTE]
> Laravel Horizon について詳しく知る前に、Laravel のベース [キューサービス](/docs/{{version}}/queues) についてよく理解しておく必要があります。 Horizon は、Laravel が提供する基本的なキュー機能にまだ慣れていない場合、混乱を招く可能性がある追加機能で Laravel のキューを強化します。

[Laravel Horizon](https://github.com/laravel/horizon) は、Laravel を利用した [Redisキュー](/docs/{{version}}/queues) に美しいダッシュボードとコード駆動の構成を提供します。 Horizon を使用すると、ジョブのスループット、実行時間、ジョブの失敗など、キュー システムの主要なメトリクスを簡単に監視できます。

Horizon を使用する場合、すべてのキューワーカー構成は 1 つの単純な構成ファイルに保存されます。バージョン管理されたファイルでアプリケーションのワーカー構成を定義すると、アプリケーションのデプロイ時にアプリケーションのキューワーカーを簡単に拡張または変更できます。

<img src="https://laravel.com/img/docs/horizon-example.png">

<a name="installation"></a>
## インストール (Installation)

> [!WARNING]
> Laravel Horizon では、キューに電力を供給するために [Redis](https://redis.io) を使用する必要があります。したがって、アプリケーションの `config/queue.php` 構成ファイルでキュー接続が `redis` に設定されていることを確認する必要があります。現時点では、Horizon は Redis Cluster と互換性がありません。

Composer パッケージ マネージャーを使用して、Horizon をプロジェクトにインストールできます。

```shell
composer require laravel/horizon
```

Horizon をインストールした後、`horizon:install` Artisan コマンドを使用してアセットを公開します。

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 構成

Horizon のアセットを公開すると、そのプライマリ構成ファイルは `config/horizon.php` に配置されます。この構成ファイルを使用すると、アプリケーションのキューワーカー オプションを構成できます。各構成オプションにはその目的の説明が含まれているため、このファイルをよく調べてください。

> [!WARNING]
> Horizon は内部で `horizon` という名前の Redis 接続を使用します。この Redis 接続名は予約されており、`database.php` 構成ファイル内の別の Redis 接続に割り当てたり、`horizon.php` 構成ファイル内の `use` オプションの値として割り当てたりしないでください。

<a name="environments"></a>
#### 環境

インストール後、よく理解しておく必要がある主な Horizon 構成オプションは、`environments` 構成オプションです。この構成オプションは、アプリケーションが実行される環境の配列であり、各環境のワーカー プロセス オプションを定義します。デフォルトでは、このエントリには `production` および `local` 環境が含まれます。ただし、必要に応じて環境を自由に追加できます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],

    'local' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

他に一致する環境が見つからない場合に使用されるワイルドカード環境 (`*`) を定義することもできます。

```php
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

Horizon を起動すると、アプリケーションが実行されている環境のワーカー プロセス構成オプションが使用されます。通常、環境は `APP_ENV` [環境変数](/docs/{{version}}/configuration#determining-the-current-environment) の値によって決まります。たとえば、デフォルトの `local` Horizon 環境は、3 つのワーカー プロセスを開始し、各キューに割り当てられたワーカー プロセスの数のバランスを自動的に調整するように構成されています。デフォルトの `production` 環境は、最大 10 個のワーカー プロセスを開始し、各キューに割り当てられるワーカー プロセスの数のバランスを自動的に調整するように構成されています。

> [!WARNING]
> `horizon` 構成ファイルの `environments` 部分に、Horizon を実行する予定の各 [environment](/docs/{{version}}/configuration#environment-configuration) のエントリが含まれていることを確認する必要があります。

<a name="supervisors"></a>
#### 監督者

Horizon のデフォルト構成ファイルからわかるように、各環境には 1 つ以上の「スーパーバイザ」を含めることができます。デフォルトでは、構成ファイルはこのスーパーバイザを `supervisor-1` として定義します。ただし、Supervisorの名前は自由に付けることができます。各スーパーバイザは基本的に、ワーカー プロセスのグループを「監視」する責任を負い、キュー間でワーカー プロセスのバランスをとります。

特定の環境で実行するワーカー プロセスの新しいグループを定義したい場合は、その環境にスーパーバイザを追加できます。アプリケーションで使用される特定のキューに対して別のバランシング戦略またはワーカー プロセス数を定義したい場合は、これを行うことを選択できます。

<a name="maintenance-mode"></a>
#### メンテナンスモード

アプリケーションが [メンテナンスモード](/docs/{{version}}/configuration#maintenance-mode) にある間は、Horizon 構成ファイル内でスーパーバイザの `force` オプションが `true` として定義されていない限り、キューに入れられたジョブは Horizon によって処理されません。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'force' => true,
        ],
    ],
],
```

<a name="default-values"></a>
#### デフォルト値

Horizon のデフォルト構成ファイル内に、`defaults` 構成オプションがあることがわかります。この構成オプションは、アプリケーションの [supervisors](#supervisors) のデフォルト値を指定します。スーパーバイザのデフォルト設定値は、各環境のスーパーバイザの設定にマージされるため、スーパーバイザを定義する際に不必要な繰り返しを避けることができます。

<a name="dashboard-authorization"></a>
### ダッシュボードの認証

Horizon ダッシュボードには、`/horizon` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。ただし、`app/Providers/HorizonServiceProvider.php` ファイル内には、[認証ゲート](/docs/{{version}}/authorization#gates) 定義があります。この認証ゲートは、**非ローカル**環境での Horizon へのアクセスを制御します。 Horizon インストールへのアクセスを制限するために、必要に応じてこのゲートを自由に変更できます。

```php
/**
 * Register the Horizon gate.
 *
 * This gate determines who can access Horizon in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewHorizon', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

<a name="alternative-authentication-strategies"></a>
#### 代替の認証戦略

Laravel は認証されたユーザーをゲート クロージャに自動的に挿入することに注意してください。アプリケーションが IP 制限などの別の方法で Horizon セキュリティを提供している場合、Horizon ユーザーは「ログイン」する必要がない場合があります。したがって、Laravel に認証を要求しないようにするには、上記の `function (User $user)` クロージャー署名を `function (User $user = null)` に変更する必要があります。

<a name="max-job-attempts"></a>
### ジョブの最大試行回数

> [!NOTE]
> これらのオプションを調整する前に、Laravel のデフォルトの [キューサービス](/docs/{{version}}/queues#max-job-attempts-and-timeout) と「試行」の概念をよく理解してください。

スーパーバイザの設定内でジョブが消費できる最大試行回数を定義できます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'tries' => 10,
        ],
    ],
],
```

> [!NOTE]
> このオプションは、Artisan コマンドを使用してキューを処理する場合の `--tries` オプションに似ています。

`WithoutOverlapping` や `RateLimited` などのミドルウェアを使用する場合、試行回数が消費されるため、`tries` オプションの調整が不可欠です。これに対処するには、Supervisor レベルで、またはジョブ クラスで `$tries` プロパティを定義することによって、`tries` 構成値を調整します。

`tries` オプションを設定しない場合、ジョブ クラスで `$tries` が定義されていない限り、Horizon はデフォルトで 1 回の試行を行います。これは Horizon 設定よりも優先されます。

`tries` または `$tries` を 0 に設定すると、無制限の試行が可能になり、試行回数が不確実な場合に最適です。無限の失敗を防ぐために、ジョブ クラスで `$maxExceptions` プロパティを設定することで、許可される例外の数を制限できます。

<a name="job-timeout"></a>
### ジョブのタイムアウト

同様に、スーパーバイザ レベルで `timeout` 値を設定できます。これは、ワーカー プロセスがジョブを強制終了するまでにジョブを実行できる秒数を指定します。終了すると、ジョブはキュー構成に応じて再試行されるか、失敗としてマークされます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...¨
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> `auto` バランス戦略を使用する場合、Horizon は進行中のワーカーを「ハング」とみなし、スケールダウン中の Horizon タイムアウト後にそれらを強制終了します。 Horizon タイムアウトがどのジョブ レベルのタイムアウトよりも大きいことを常に確認してください。そうしないと、ジョブが実行中に終了する可能性があります。さらに、`timeout` 値は、`config/queue.php` 構成ファイルで定義されている `retry_after` 値よりも常に少なくとも数秒短くする必要があります。そうしないと、ジョブが 2 回処理される可能性があります。

<a name="job-backoff"></a>
### ジョブバックオフ

スーパーバイザ レベルで `backoff` 値を定義して、未処理の例外が発生したジョブを再試行するまでに Horizon が待機する時間を指定できます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => 10,
        ],
    ],
],
```

`backoff` 値の配列を使用して、「指数関数的」バックオフを構成することもできます。この例では、再試行の遅​​延は、最初の再試行では 1 秒、2 回目の再試行では 5 秒、3 回目の再試行では 10 秒、さらに試行が残っている場合はその後の再試行ごとに 10 秒になります。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => [1, 5, 10],
        ],
    ],
],
```

<a name="silenced-jobs"></a>
### サイレントジョブ

場合によっては、アプリケーションまたはサードパーティのパッケージによってディスパッチされた特定のジョブを表示することに興味がない場合があります。これらのジョブが「完了したジョブ」リストのスペースを占める代わりに、それらのジョブを沈黙させることができます。まず、ジョブのクラス名をアプリケーションの `horizon` 構成ファイルの `silenced` 構成オプションに追加します。

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

Horizon は、個々のジョブ クラスのサイレント化に加えて、[tags](#tags) に基づいたジョブのサイレント化もサポートしています。これは、共通のタグを共有する複数のジョブを非表示にする場合に便利です。

```php
'silenced_tags' => [
    'notifications'
],
```

あるいは、沈黙させたいジョブは、`Laravel\Horizon\Contracts\Silenced` インターフェイスを実装できます。ジョブがこのインターフェイスを実装している場合、それが `silenced` 構成配列に存在しない場合でも、ジョブは自動的にサイレント化されます。

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 戦略のバランスを取る (Balancing Strategies)

各スーパーバイザは 1 つ以上のキューを処理できますが、Laravel のデフォルトのキュー システムとは異なり、Horizon では、`auto`、`simple`、`false` の 3 つのワーカー バランシング戦略から選択できます。

<a name="auto-balancing"></a>
### 自動バランス調整

デフォルトの戦略である `auto` 戦略は、キューの現在のワークロードに基づいてキューごとのワーカー プロセスの数を調整します。たとえば、`notifications` キューに 1,000 個の保留中のジョブがあり、`default` キューが空の場合、Horizon はキューが空になるまでより多くのワーカーを `notifications` キューに割り当てます。

`auto` 戦略を使用する場合は、`minProcesses` および `maxProcesses` 構成オプションも構成できます。

<div class="content-list" markdown="1">

- `minProcesses` は、キューごとのワーカー プロセスの最小数を定義します。この値は 1 以上である必要があります。
- `maxProcesses` は、Horizon がすべてのキューにわたってスケールアップできるワーカー プロセスの最大合計数を定義します。この値は通常、キューの数に `minProcesses` 値を乗算した値より大きくなければなりません。スーパーバイザがプロセスを生成しないようにするには、この値を 0 に設定します。

</div>

たとえば、キュ​​ーごとに少なくとも 1 つのプロセスを維持し、合計 10 のワーカー プロセスまでスケールアップするように Horizon を構成できます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default', 'notifications'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
],
```

`autoScalingStrategy` 構成オプションは、Horizon がより多くのワーカー プロセスをキューに割り当てる方法を決定します。次の 2 つの戦略から選択できます。

<div class="content-list" markdown="1">

- `time` 戦略は、キューをクリアするのにかかる推定合計時間に基づいてワーカーを割り当てます。
- `size` ストラテジーは、キュー上のジョブの合計数に基づいてワーカーを割り当てます。

</div>

`balanceMaxShift` および `balanceCooldown` の構成値は、ワーカーの需要を満たすために Horizon がどの程度の速度でスケールするかを決定します。上の例では、3 秒ごとに最大 1 つの新しいプロセスが作成または破棄されます。アプリケーションのニーズに基づいて、必要に応じてこれらの値を自由に調整できます。

<a name="auto-queue-priorities"></a>
#### キューの優先順位と自動バランス

`auto` バランス戦略を使用する場合、Horizon はキュー間の厳密な優先順位を強制しません。スーパーバイザの構成内のキューの順序は、ワーカー プロセスの割り当て方法には影響しません。代わりに、Horizon は選択された `autoScalingStrategy` に依存して、キューの負荷に基づいてワーカー プロセスを動的に割り当てます。

たとえば、次の設定では、上位キューがリストの最初に表示されているにもかかわらず、デフォルト キューよりも優先されません。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['high', 'default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

キュー間の相対的な優先順位を強制する必要がある場合は、複数のスーパーバイザを定義して処理リソースを明示的に割り当てることができます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
        'supervisor-2' => [
            // ...
            'queue' => ['images'],
            'minProcesses' => 1,
            'maxProcesses' => 1,
        ],
    ],
],
```

この例では、デフォルトの `queue` は最大 10 プロセスまでスケールできますが、`images` キューは 1 プロセスに制限されています。この構成により、キューを独立して拡張できるようになります。

> [!NOTE]
> リソースを大量に消費するジョブをディスパッチする場合、`maxProcesses` 値を制限した専用キューにジョブを割り当てることが最善の場合があります。そうしないと、これらのジョブが過剰な CPU リソースを消費し、システムに過負荷がかかる可能性があります。

<a name="simple-balancing"></a>
### シンプルなバランス調整

`simple` 戦略は、指定されたキュー全体にワーカー プロセスを均等に分散します。この戦略では、Horizon はワーカー プロセスの数を自動的にスケールしません。むしろ、固定数のプロセスを使用します。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => 'simple',
            'processes' => 10,
        ],
    ],
],
```

上の例では、Horizon は各キューに 5 つのプロセスを割り当て、合計 10 を均等に分割します。

各キューに割り当てられるワーカー プロセスの数を個別に制御したい場合は、複数のスーパーバイザを定義できます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'balance' => 'simple',
            'processes' => 10,
        ],
        'supervisor-notifications' => [
            // ...
            'queue' => ['notifications'],
            'balance' => 'simple',
            'processes' => 2,
        ],
    ],
],
```

この構成では、Horizon は 10 個のプロセスを `default` キューに割り当て、2 個のプロセスを `notifications` キューに割り当てます。

<a name="no-balancing"></a>
### バランス調整なし

`balance` オプションが `false` に設定されている場合、Horizon は、Laravel のデフォルトのキュー システムと同様に、リストされている順序でキューを厳密に処理します。ただし、ジョブが蓄積され始めると、ワーカー プロセスの数は引き続きスケーリングされます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => false,
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

上の例では、`default` キュー内のジョブは、常に `notifications` キュー内のジョブより優先されます。たとえば、`default` に 1,000 個のジョブがあり、`notifications` には 10 個しかない場合、Horizon は、`notifications` からのジョブを処理する前に、すべての `default` ジョブを完全に処理します。

`minProcesses` および `maxProcesses` オプションを使用して、ワーカー プロセスをスケーリングする Horizon の機能を制御できます。

<div class="content-list" markdown="1">

- `minProcesses` は、ワーカー プロセスの合計の最小数を定義します。この値は 1 以上である必要があります。
- `maxProcesses` は、Horizon がスケールアップできるワーカー プロセスの最大合計数を定義します。

</div>

<a name="upgrading-horizon"></a>
## Horizon のアップグレード (Upgrading Horizon)

Horizon の新しいメジャー バージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/horizon/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="running-horizon"></a>
## ランニングホライゾン (Running Horizon)

アプリケーションの `config/horizon.php` 構成ファイルでSupervisorとワーカーを構成したら、`horizon` Artisan コマンドを使用して Horizon を起動できます。この 1 つのコマンドは、現在の環境で構成されているすべてのワーカー プロセスを開始します。

```shell
php artisan horizon
```

Horizon プロセスを一時停止し、`horizon:pause` および `horizon:continue` Artisan コマンドを使用してジョブの処理を続行するように指示できます。

```shell
php artisan horizon:pause

php artisan horizon:continue
```

`horizon:pause-supervisor` および `horizon:continue-supervisor` Artisan コマンドを使用して、特定の Horizon [supervisors](#supervisors) を一時停止および続行することもできます。

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

`horizon:status` Artisan コマンドを使用して、Horizon プロセスの現在のステータスを確認できます。

```shell
php artisan horizon:status
```

`horizon:supervisor-status` Artisan コマンドを使用して、特定の Horizon [supervisor](#supervisors) の現在のステータスを確認できます。

```shell
php artisan horizon:supervisor-status supervisor-1
```

`horizon:terminate` Artisan コマンドを使用して、Horizon プロセスを正常に終了できます。現在処理中のジョブはすべて完了し、Horizon は実行を停止します。

```shell
php artisan horizon:terminate
```

<a name="automatically-restarting-horizon"></a>
#### Horizon の自動再起動

ローカル開発中に、`horizon:listen` コマンドを実行できます。 `horizon:listen` コマンドを使用すると、更新されたコードをリロードするときに Horizon を手動で再起動する必要がありません。この機能を使用する前に、[Node](https://nodejs.org) がローカル開発環境にインストールされていることを確認する必要があります。さらに、プロジェクト内に [Chokidar](https://github.com/paulmillr/chokidar) ファイル監視ライブラリをインストールする必要があります。

```shell
npm install --save-dev chokidar
```

Chokidar がインストールされたら、`horizon:listen` コマンドを使用して Horizon を起動できます。

```shell
php artisan horizon:listen
```

Docker または Vagrant 内で実行する場合は、`--poll` オプションを使用する必要があります。

```shell
php artisan horizon:listen --poll
```

アプリケーションの `config/horizon.php` 構成ファイル内の `watch` 構成オプションを使用して、監視する必要があるディレクトリとファイルを構成できます。

```php
'watch' => [
    'app',
    'bootstrap',
    'config',
    'database',
    'public/**/*.php',
    'resources/**/*.php',
    'routes',
    'composer.lock',
    '.env',
],
```

<a name="deploying-horizon"></a>
### Horizon の導入

Horizon をアプリケーションの実際のサーバーにデプロイする準備ができたら、`php artisan horizon` コマンドを監視し、予期せず終了した場合にコマンドを再起動するようにプロセス モニターを構成する必要があります。心配しないでください。プロセス モニターのインストール方法については以下で説明します。

アプリケーションのデプロイ プロセス中に、Horizon プロセスがプロセス モニターによって再起動され、コードの変更を受信できるように、プロセスを終了するように指示する必要があります。

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### スーパーバイザのインス​​トール

Supervisorは、Linux オペレーティング システムのプロセス モニターであり、`horizon` プロセスが実行を停止した場合に自動的に再起動します。 Ubuntu に Supervisor をインストールするには、次のコマンドを使用できます。 Ubuntu を使用していない場合は、オペレーティング システムのパッケージ マネージャーを使用して Supervisor をインストールできる可能性があります。

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisorを自分で設定するのが大変だと思われる場合は、Laravel アプリケーションのバックグラウンド プロセスを管理できる [Laravel Cloud](https://cloud.laravel.com) の使用を検討してください。

<a name="supervisor-configuration"></a>
#### スーパーバイザの構成

スーパーバイザ設定ファイルは通常、サーバーの `/etc/supervisor/conf.d` ディレクトリ内に保存されます。このディレクトリ内に、スーパーバイザにプロセスの監視方法を指示する構成ファイルをいくつでも作成できます。たとえば、`horizon` プロセスを開始して監視する `horizon.conf` ファイルを作成してみましょう。

```ini
[program:horizon]
process_name=%(program_name)s
command=php /home/forge/example.com/artisan horizon
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/horizon.log
stopwaitsecs=3600
```

Supervisor構成を定義するときは、`stopwaitsecs` の値が、最も長く実行されているジョブで消費される秒数よりも大きいことを確認する必要があります。そうしないと、Supervisorがジョブの処理が完了する前にジョブを強制終了する可能性があります。

> [!WARNING]
> 上記の例は Ubuntu ベースのサーバに有効ですが、スーパーバイザ設定ファイルに予期される場所とファイル拡張子は、他のサーバ オペレーティング システムでは異なる場合があります。詳細については、サーバーのドキュメントを参照してください。

<a name="starting-supervisor"></a>
#### スーパーバイザの開始

設定ファイルが作成されたら、次のコマンドを使用してスーパーバイザ設定を更新し、監視対象プロセスを開始できます。

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> スーパーバイザの実行の詳細については、[Supervisorの文書](http://supervisord.org/index.html) を参照してください。

<a name="tags"></a>
## タグ (Tags)

Horizon では、メール可能ファイル、ブロードキャスト イベント、通知、キューに入れられたイベント リスナなどのジョブに「タグ」を割り当てることができます。実際、Horizon は、ジョブにアタッチされている Eloquent モデルに応じて、ほとんどのジョブにインテリジェントかつ自動的にタグ付けします。たとえば、次のジョブを見てください。

```php
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class RenderVideo implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...
    }
}
```

このジョブが、`1` の `id` 属性を持つ `App\Models\Video` インスタンスとともにキューに入れられた場合、自動的にタグ `App\Models\Video:1` を受け取ります。これは、Horizon がジョブのプロパティで Eloquent モデルを検索するためです。 Eloquent モデルが見つかった場合、Horizon はモデルのクラス名と主キーを使用してジョブにインテリジェントにタグ付けします。

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### ジョブの手動タグ付け

キュー可能オブジェクトのいずれかのタグを手動で定義したい場合は、クラスに `tags` メソッドを定義できます。

```php
class RenderVideo implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the job.
     *
     * @return array<int, string>
     */
    public function tags(): array
    {
        return ['render', 'video:'.$this->video->id];
    }
}
```

<a name="manually-tagging-event-listeners"></a>
#### イベントリスナの手動タグ付け

キューに入れられたイベント リスナのタグを取得するとき、Horizon は自動的にイベント インスタンスを `tags` メソッドに渡し、イベント データをタグに追加できるようにします。

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the listener.
     *
     * @return array<int, string>
     */
    public function tags(VideoRendered $event): array
    {
        return ['video:'.$event->video->id];
    }
}
```

<a name="notifications"></a>
## 通知 (Notifications)

> [!WARNING]
> Slack または SMS 通知を送信するように Horizon を構成する場合は、[関連する通知チャネルの前提条件](/docs/{{version}}/notifications) を確認する必要があります。

キューの 1 つで長い待ち時間が発生したときに通知を受け取りたい場合は、`Horizon::routeMailNotificationsTo`、`Horizon::routeSlackNotificationsTo`、および `Horizon::routeSmsNotificationsTo` メソッドを使用できます。これらのメソッドは、アプリケーションの `App\Providers\HorizonServiceProvider` の `boot` メソッドから呼び出すことができます。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Horizon::routeSmsNotificationsTo('15556667777');
    Horizon::routeMailNotificationsTo('example@example.com');
    Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
}
```

<a name="configuring-notification-wait-time-thresholds"></a>
#### 通知待機時間のしきい値の構成

アプリケーションの `config/horizon.php` 構成ファイル内で、「長い待機」とみなされる秒数を構成できます。このファイル内の `waits` 構成オプションを使用すると、接続とキューの組み合わせごとに長時間待機のしきい値を制御できます。未定義の接続/キューの組み合わせは、デフォルトで 60 秒の長時間待機しきい値に設定されます。

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

キューのしきい値を `0` に設定すると、そのキューの長時間待機の通知が無効になります。

<a name="metrics"></a>
## メトリクス (Metrics)

Horizon には、ジョブとキューの待機時間とスループットに関する情報を提供するメトリクス ダッシュボードが含まれています。このダッシュボードにデータを入力するには、アプリケーションの `routes/console.php` ファイルで Horizon の `snapshot` Artisan コマンドを 5 分ごとに実行するように構成する必要があります。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

すべてのメトリック データを削除したい場合は、`horizon:clear-metrics` Artisan コマンドを呼び出します。

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 失敗したジョブの削除 (Deleting Failed Jobs)

失敗したジョブを削除したい場合は、`horizon:forget` コマンドを使用できます。 `horizon:forget` コマンドは、失敗したジョブの ID または UUID を唯一の引数として受け入れます。

```shell
php artisan horizon:forget 5
```

失敗したジョブをすべて削除したい場合は、`--all` オプションを `horizon:forget` コマンドに指定します。

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## キューからジョブをクリアする (Clearing Jobs From Queues)

アプリケーションのデフォルト キューからすべてのジョブを削除したい場合は、`horizon:clear` Artisan コマンドを使用して削除できます。

```shell
php artisan horizon:clear
```

`queue` オプションを指定して、特定のキューからジョブを削除できます。

```shell
php artisan horizon:clear --queue=emails
```

