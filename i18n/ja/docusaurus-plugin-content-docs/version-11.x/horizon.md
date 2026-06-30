<!-- # Laravel Horizon -->
# Laravel Horizon

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Balancing Strategies](#balancing-strategies)
    - [Dashboard Authorization](#dashboard-authorization)
    - [Silenced Jobs](#silenced-jobs)
- [Upgrading Horizon](#upgrading-horizon)
- [Running Horizon](#running-horizon)
    - [Deploying Horizon](#deploying-horizon)
- [Tags](#tags)
- [Notifications](#notifications)
- [Metrics](#metrics)
- [Deleting Failed Jobs](#deleting-failed-jobs)
- [Clearing Jobs From Queues](#clearing-jobs-from-queues)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!NOTE]
> Laravel Horizon について詳しく知る前に、Laravel のベース [queue services](/docs/11.x/queues) についてよく理解しておく必要があります。 Horizon は、Laravel が提供する基本的なキュー機能にまだ慣れていない場合、混乱を招く可能性がある追加機能で Laravel のキューを強化します。

<!-- [Laravel Horizon](https://github.com/laravel/horizon) provides a beautiful dashboard and code-driven configuration for your Laravel powered [Redis queues](/docs/11.x/queues). Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. -->
[Laravel Horizon](https://github.com/laravel/horizon) は、Laravel を利用した [Redis queues](/docs/11.x/queues) に美しいダッシュボードとコード駆動の構成を提供します。 Horizon を使用すると、ジョブのスループット、実行時間、ジョブの失敗など、キュー システムの主要なメトリクスを簡単に監視できます。

<!-- When using Horizon, all of your queue worker configuration is stored in a single, simple configuration file. By defining your application's worker configuration in a version controlled file, you may easily scale or modify your application's queue workers when deploying your application. -->
Horizon を使用する場合、すべてのキューワーカー構成は 1 つの単純な構成ファイルに保存されます。バージョン管理されたファイルでアプリケーションのワーカー構成を定義すると、アプリケーションのデプロイ時にアプリケーションのキューワーカーを簡単に拡張または変更できます。

<!-- <img src="https://laravel.com/img/docs/horizon-example.png"/> -->
<img src="https://laravel.com/img/docs/horizon-example.png"/>

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Horizon では、キューに電力を供給するために [Redis](https://redis.io) を使用する必要があります。したがって、アプリケーションの `config/queue.php` 構成ファイルでキュー接続が `redis` に設定されていることを確認する必要があります。

<!-- You may install Horizon into your project using the Composer package manager: -->
Composer パッケージ マネージャーを使用して、Horizon をプロジェクトにインストールできます。

```shell
composer require laravel/horizon
```

<!-- After installing Horizon, publish its assets using the `horizon:install` Artisan command: -->
Horizon をインストールした後、`horizon:install` Artisan コマンドを使用してアセットを公開します。

```shell
php artisan horizon:install
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Horizon's assets, its primary configuration file will be located at `config/horizon.php`. This configuration file allows you to configure the queue worker options for your application. Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
Horizon のアセットを公開すると、そのプライマリ構成ファイルは `config/horizon.php` に配置されます。この構成ファイルを使用すると、アプリケーションのキューワーカー オプションを構成できます。各構成オプションにはその目的の説明が含まれているため、このファイルをよく調べてください。

> [!WARNING]
> Horizon は内部で `horizon` という名前の Redis 接続を使用します。この Redis 接続名は予約されており、`database.php` 構成ファイル内の別の Redis 接続に割り当てたり、`horizon.php` 構成ファイル内の `use` オプションの値として割り当てたりしないでください。

<a name="environments"></a>
<!-- #### Environments -->
#### Environments

<!-- After installation, the primary Horizon configuration option that you should familiarize yourself with is the `environments` configuration option. This configuration option is an array of environments that your application runs on and defines the worker process options for each environment. By default, this entry contains a `production` and `local` environment. However, you are free to add more environments as needed: -->
インストール後、よく理解しておく必要がある主な Horizon 構成オプションは、`environments` 構成オプションです。この構成オプションは、アプリケーションが実行される環境の配列であり、各環境のワーカー プロセス オプションを定義します。デフォルトでは、このエントリには `production` および `local` 環境が含まれます。ただし、必要に応じて環境を自由に追加できます。

```
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

<!-- You may also define a wildcard environment (`*`) which will be used when no other matching environment is found: -->
他に一致する環境が見つからない場合に使用されるワイルドカード環境 (`*`) を定義することもできます。

```
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

<!-- When you start Horizon, it will use the worker process configuration options for the environment that your application is running on. Typically, the environment is determined by the value of the `APP_ENV` [environment variable](/docs/11.x/configuration#determining-the-current-environment). For example, the default `local` Horizon environment is configured to start three worker processes and automatically balance the number of worker processes assigned to each queue. The default `production` environment is configured to start a maximum of 10 worker processes and automatically balance the number of worker processes assigned to each queue. -->
Horizon を起動すると、アプリケーションが実行されている環境のワーカー プロセス構成オプションが使用されます。通常、環境は `APP_ENV` [environment variable](/docs/11.x/configuration#determining-the-current-environment) の値によって決まります。たとえば、デフォルトの `local` Horizon 環境は、3 つのワーカー プロセスを開始し、各キューに割り当てられたワーカー プロセスの数のバランスを自動的に調整するように構成されています。デフォルトの `production` 環境は、最大 10 個のワーカー プロセスを開始し、各キューに割り当てられるワーカー プロセスの数のバランスを自動的に調整するように構成されています。

> [!WARNING]
> `horizon` 構成ファイルの `environments` 部分に、Horizon を実行する予定の各 [environment](/docs/11.x/configuration#environment-configuration) のエントリが含まれていることを確認する必要があります。

<a name="supervisors"></a>
<!-- #### Supervisors -->
#### Supervisors

<!-- As you can see in Horizon's default configuration file, each environment can contain one or more "supervisors". By default, the configuration file defines this supervisor as `supervisor-1`; however, you are free to name your supervisors whatever you want. Each supervisor is essentially responsible for "supervising" a group of worker processes and takes care of balancing worker processes across queues. -->
Horizon のデフォルト構成ファイルからわかるように、各環境には 1 つ以上の「スーパーバイザ」を含めることができます。デフォルトでは、構成ファイルはこのスーパーバイザを `supervisor-1` として定義します。ただし、Supervisorの名前は自由に付けることができます。各スーパーバイザは基本的に、ワーカー プロセスのグループを「監視」する責任を負い、キュー間でワーカー プロセスのバランスをとります。

<!-- You may add additional supervisors to a given environment if you would like to define a new group of worker processes that should run in that environment. You may choose to do this if you would like to define a different balancing strategy or worker process count for a given queue used by your application. -->
特定の環境で実行するワーカー プロセスの新しいグループを定義したい場合は、その環境にスーパーバイザを追加できます。アプリケーションで使用される特定のキューに対して別のバランシング戦略またはワーカー プロセス数を定義したい場合は、これを行うことを選択できます。

<a name="maintenance-mode"></a>
<!-- #### Maintenance Mode -->
#### Maintenance Mode

<!-- While your application is in [maintenance mode](/docs/11.x/configuration#maintenance-mode), queued jobs will not be processed by Horizon unless the supervisor's `force` option is defined as `true` within the Horizon configuration file: -->
アプリケーションが [maintenance mode](/docs/11.x/configuration#maintenance-mode) にある間は、Horizon 構成ファイル内でスーパーバイザの `force` オプションが `true` として定義されていない限り、キューに入れられたジョブは Horizon によって処理されません。

```
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
<!-- #### Default Values -->
#### Default Values

<!-- Within Horizon's default configuration file, you will notice a `defaults` configuration option. This configuration option specifies the default values for your application's [supervisors](#supervisors). The supervisor's default configuration values will be merged into the supervisor's configuration for each environment, allowing you to avoid unnecessary repetition when defining your supervisors. -->
Horizon のデフォルト構成ファイル内に、`defaults` 構成オプションがあることがわかります。この構成オプションは、アプリケーションの [supervisors](#supervisors) のデフォルト値を指定します。スーパーバイザのデフォルト設定値は、各環境のスーパーバイザの設定にマージされるため、スーパーバイザを定義する際に不必要な繰り返しを避けることができます。

<a name="balancing-strategies"></a>
<!-- ### Balancing Strategies -->
### Balancing Strategies

<!-- Unlike Laravel's default queue system, Horizon allows you to choose from three worker balancing strategies: `simple`, `auto`, and `false`. The `simple` strategy splits incoming jobs evenly between worker processes: -->
Laravel のデフォルトのキュー システムとは異なり、Horizon では、`simple`、`auto`、`false` の 3 つのワーカー バランシング戦略から選択できます。 `simple` 戦略は、受信ジョブをワーカー プロセス間で均等に分割します。

```
'balance' => 'simple',
```

<!-- The `auto` strategy, which is the configuration file's default, adjusts the number of worker processes per queue based on the current workload of the queue. For example, if your `notifications` queue has 1,000 pending jobs while your `render` queue is empty, Horizon will allocate more workers to your `notifications` queue until the queue is empty. -->
構成ファイルのデフォルトである `auto` 戦略は、キューの現在のワークロードに基づいてキューごとのワーカー プロセスの数を調整します。たとえば、`notifications` キューに 1,000 個の保留中のジョブがあり、`render` キューが空の場合、Horizon はキューが空になるまでより多くのワーカーを `notifications` キューに割り当てます。

<!-- When using the `auto` strategy, you may define the `minProcesses` and `maxProcesses` configuration options to control the minimum number of processes per queue and the maximum number of worker processes in total Horizon should scale up and down to: -->
`auto` 戦略を使用する場合、`minProcesses` および `maxProcesses` 構成オプションを定義して、キューあたりの最小プロセス数と合計ワーカー プロセスの最大数を制御できます。Horizon は次のようにスケールアップおよびスケールダウンする必要があります。

```
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
            'tries' => 3,
        ],
    ],
],
```

<!-- The `autoScalingStrategy` configuration value determines if Horizon will assign more worker processes to queues based on the total amount of time it will take to clear the queue (`time` strategy) or by the total number of jobs on the queue (`size` strategy). -->
`autoScalingStrategy` 構成値は、キューをクリアするのにかかる合計時間 (`time` 戦略) に基づいて、またはキュー上のジョブの総数 (`size` 戦略) に基づいて、Horizon がより多くのワーカー プロセスをキューに割り当てるかを決定します。

<!-- The `balanceMaxShift` and `balanceCooldown` configuration values determine how quickly Horizon will scale to meet worker demand. In the example above, a maximum of one new process will be created or destroyed every three seconds. You are free to tweak these values as necessary based on your application's needs. -->
`balanceMaxShift` および `balanceCooldown` の構成値は、ワーカーの需要を満たすために Horizon がどの程度の速度でスケールするかを決定します。上の例では、3 秒ごとに最大 1 つの新しいプロセスが作成または破棄されます。アプリケーションのニーズに基づいて、必要に応じてこれらの値を自由に調整できます。

<!-- When the `balance` option is set to `false`, the default Laravel behavior will be used, wherein queues are processed in the order they are listed in your configuration. -->
`balance` オプションが `false` に設定されている場合、デフォルトの Laravel 動作が使用され、キューは設定にリストされている順序で処理されます。

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Horizon dashboard may be accessed via the `/horizon` route. By default, you will only be able to access this dashboard in the `local` environment. However, within your `app/Providers/HorizonServiceProvider.php` file, there is an [authorization gate](/docs/11.x/authorization#gates) definition. This authorization gate controls access to Horizon in **non-local** environments. You are free to modify this gate as needed to restrict access to your Horizon installation: -->
Horizon ダッシュボードには、`/horizon` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。ただし、`app/Providers/HorizonServiceProvider.php` ファイル内には、[authorization gate](/docs/11.x/authorization#gates) 定義があります。この認可ゲートは、**非ローカル**環境での Horizon へのアクセスを制御します。 Horizon インストールへのアクセスを制限するために、必要に応じてこのゲートを自由に変更できます。

```
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
<!-- #### Alternative Authentication Strategies -->
#### Alternative Authentication Strategies

<!-- Remember that Laravel automatically injects the authenticated user into the gate closure. If your application is providing Horizon security via another method, such as IP restrictions, then your Horizon users may not need to "login". Therefore, you will need to change `function (User $user)` closure signature above to `function (User $user = null)` in order to force Laravel to not require authentication. -->
Laravel は認証されたユーザーをゲート クロージャに自動的に挿入することに注意してください。アプリケーションが IP 制限などの別の方法で Horizon セキュリティを提供している場合、Horizon ユーザーは「ログイン」する必要がない場合があります。したがって、Laravel に認証を要求しないようにするには、上記の `function (User $user)` クロージャー署名を `function (User $user = null)` に変更する必要があります。

<a name="silenced-jobs"></a>
<!-- ### Silenced Jobs -->
### Silenced Jobs

<!-- Sometimes, you may not be interested in viewing certain jobs dispatched by your application or third-party packages. Instead of these jobs taking up space in your "Completed Jobs" list, you can silence them. To get started, add the job's class name to the `silenced` configuration option in your application's `horizon` configuration file: -->
場合によっては、アプリケーションまたはサードパーティのパッケージによってディスパッチされた特定のジョブを表示することに興味がない場合があります。これらのジョブが「完了したジョブ」リストのスペースを占める代わりに、それらのジョブを沈黙させることができます。まず、ジョブのクラス名をアプリケーションの `horizon` 構成ファイルの `silenced` 構成オプションに追加します。

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

<!-- Alternatively, the job you wish to silence can implement the `Laravel\Horizon\Contracts\Silenced` interface. If a job implements this interface, it will automatically be silenced, even if it is not present in the `silenced` configuration array: -->
あるいは、沈黙させたいジョブは、`Laravel\Horizon\Contracts\Silenced` インターフェイスを実装できます。ジョブがこのインターフェイスを実装している場合、それが `silenced` 構成配列に存在しない場合でも、ジョブは自動的にサイレント化されます。

```
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="upgrading-horizon"></a>
<!-- ## Upgrading Horizon -->
## Upgrading Horizon

<!-- When upgrading to a new major version of Horizon, it's important that you carefully review [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md). -->
Horizon の新しいメジャー バージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="running-horizon"></a>
<!-- ## Running Horizon -->
## Running Horizon

<!-- Once you have configured your supervisors and workers in your application's `config/horizon.php` configuration file, you may start Horizon using the `horizon` Artisan command. This single command will start all of the configured worker processes for the current environment: -->
アプリケーションの `config/horizon.php` 構成ファイルでSupervisorとワーカーを構成したら、`horizon` Artisan コマンドを使用して Horizon を起動できます。この 1 つのコマンドは、現在の環境で構成されているすべてのワーカー プロセスを開始します。

```shell
php artisan horizon
```

<!-- You may pause the Horizon process and instruct it to continue processing jobs using the `horizon:pause` and `horizon:continue` Artisan commands: -->
Horizon プロセスを一時停止し、`horizon:pause` および `horizon:continue` Artisan コマンドを使用してジョブの処理を続行するように指示できます。

```shell
php artisan horizon:pause

php artisan horizon:continue
```

<!-- You may also pause and continue specific Horizon [supervisors](#supervisors) using the `horizon:pause-supervisor` and `horizon:continue-supervisor` Artisan commands: -->
`horizon:pause-supervisor` および `horizon:continue-supervisor` Artisan コマンドを使用して、特定の Horizon [supervisors](#supervisors) を一時停止および続行することもできます。

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

<!-- You may check the current status of the Horizon process using the `horizon:status` Artisan command: -->
`horizon:status` Artisan コマンドを使用して、Horizon プロセスの現在のステータスを確認できます。

```shell
php artisan horizon:status
```

<!-- You may check the current status of a specific Horizon [supervisor](#supervisors) using the `horizon:supervisor-status` Artisan command: -->
`horizon:supervisor-status` Artisan コマンドを使用して、特定の Horizon [supervisor](#supervisors) の現在のステータスを確認できます。

```shell
php artisan horizon:supervisor-status supervisor-1
```

<!-- You may gracefully terminate the Horizon process using the `horizon:terminate` Artisan command. Any jobs that are currently being processed will be completed and then Horizon will stop executing: -->
`horizon:terminate` Artisan コマンドを使用して、Horizon プロセスを正常に終了できます。現在処理中のジョブはすべて完了し、Horizon は実行を停止します。

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
<!-- ### Deploying Horizon -->
### Deploying Horizon

<!-- When you're ready to deploy Horizon to your application's actual server, you should configure a process monitor to monitor the `php artisan horizon` command and restart it if it exits unexpectedly. Don't worry, we'll discuss how to install a process monitor below. -->
Horizon をアプリケーションの実際のサーバーにデプロイする準備ができたら、`php artisan horizon` コマンドを監視し、予期せず終了した場合にコマンドを再起動するようにプロセス モニターを構成する必要があります。心配しないでください。プロセス モニターのインストール方法については以下で説明します。

<!-- During your application's deployment process, you should instruct the Horizon process to terminate so that it will be restarted by your process monitor and receive your code changes: -->
アプリケーションのデプロイ プロセス中に、Horizon プロセスがプロセス モニターによって再起動され、コードの変更を受信できるように、プロセスを終了するように指示する必要があります。

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system and will automatically restart your `horizon` process if it stops executing. To install Supervisor on Ubuntu, you may use the following command. If you are not using Ubuntu, you can likely install Supervisor using your operating system's package manager: -->
Supervisorは、Linux オペレーティング システムのプロセス モニターであり、`horizon` プロセスが実行を停止した場合に自動的に再起動します。 Ubuntu に Supervisor をインストールするには、次のコマンドを使用できます。 Ubuntu を使用していない場合は、オペレーティング システムのパッケージ マネージャーを使用して Supervisor をインストールできる可能性があります。

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor を自分で設定するのが面倒に思える場合は、Laravel プロジェクト用に Supervisor を自動的にインストールして設定する [Laravel Forge](https://forge.laravel.com) の使用を検討してください。

<a name="supervisor-configuration"></a>
<!-- #### Supervisor Configuration -->
#### Supervisor Configuration

<!-- Supervisor configuration files are typically stored within your server's `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `horizon.conf` file that starts and monitors a `horizon` process: -->
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

<!-- When defining your Supervisor configuration, you should ensure that the value of `stopwaitsecs` is greater than the number of seconds consumed by your longest running job. Otherwise, Supervisor may kill the job before it is finished processing. -->
Supervisor構成を定義するときは、`stopwaitsecs` の値が、最も長く実行されているジョブで消費される秒数よりも大きいことを確認する必要があります。そうしないと、Supervisorがジョブの処理が完了する前にジョブを強制終了する可能性があります。

> [!WARNING]
> 上記の例は Ubuntu ベースのサーバに有効ですが、スーパーバイザ設定ファイルに予期される場所とファイル拡張子は、他のサーバ オペレーティング システムでは異なる場合があります。詳細については、サーバーのドキュメントを参照してください。

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the monitored processes using the following commands: -->
設定ファイルが作成されたら、次のコマンドを使用してスーパーバイザ設定を更新し、監視対象プロセスを開始できます。

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> スーパーバイザの実行の詳細については、[Supervisor documentation](http://supervisord.org/index.html) を参照してください。

<a name="tags"></a>
<!-- ## Tags -->
## Tags

<!-- Horizon allows you to assign “tags” to jobs, including mailables, broadcast events, notifications, and queued event listeners. In fact, Horizon will intelligently and automatically tag most jobs depending on the Eloquent models that are attached to the job. For example, take a look at the following job: -->
Horizon では、メール可能ファイル、ブロードキャスト イベント、通知、キューに入れられたイベント リスナなどのジョブに「タグ」を割り当てることができます。実際、Horizon は、ジョブにアタッチされている Eloquent モデルに応じて、ほとんどのジョブにインテリジェントかつ自動的にタグ付けします。たとえば、次のジョブを見てください。

```
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

<!-- If this job is queued with an `App\Models\Video` instance that has an `id` attribute of `1`, it will automatically receive the tag `App\Models\Video:1`. This is because Horizon will search the job's properties for any Eloquent models. If Eloquent models are found, Horizon will intelligently tag the job using the model's class name and primary key: -->
このジョブが、`1` の `id` 属性を持つ `App\Models\Video` インスタンスとともにキューに入れられた場合、自動的にタグ `App\Models\Video:1` を受け取ります。これは、Horizon がジョブのプロパティで Eloquent モデルを検索するためです。 Eloquent モデルが見つかった場合、Horizon はモデルのクラス名と主キーを使用してジョブにインテリジェントにタグ付けします。

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
<!-- #### Manually Tagging Jobs -->
#### Manually Tagging Jobs

<!-- If you would like to manually define the tags for one of your queueable objects, you may define a `tags` method on the class: -->
キュー可能オブジェクトのいずれかのタグを手動で定義したい場合は、クラスに `tags` メソッドを定義できます。

```
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
<!-- #### Manually Tagging Event Listeners -->
#### Manually Tagging Event Listeners

<!-- When retrieving the tags for a queued event listener, Horizon will automatically pass the event instance to the `tags` method, allowing you to add event data to the tags: -->
キューに入れられたイベント リスナのタグを取得するとき、Horizon は自動的にイベント インスタンスを `tags` メソッドに渡し、イベント データをタグに追加できるようにします。

```
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
<!-- ## Notifications -->
## Notifications

> [!WARNING]
> Slack または SMS 通知を送信するように Horizon を構成する場合は、[prerequisites for the relevant notification channel](/docs/11.x/notifications) を確認する必要があります。

<!-- If you would like to be notified when one of your queues has a long wait time, you may use the `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, and `Horizon::routeSmsNotificationsTo` methods. You may call these methods from the `boot` method of your application's `App\Providers\HorizonServiceProvider`: -->
キューの 1 つで長い待ち時間が発生したときに通知を受け取りたい場合は、`Horizon::routeMailNotificationsTo`、`Horizon::routeSlackNotificationsTo`、および `Horizon::routeSmsNotificationsTo` メソッドを使用できます。これらのメソッドは、アプリケーションの `App\Providers\HorizonServiceProvider` の `boot` メソッドから呼び出すことができます。

```
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
<!-- #### Configuring Notification Wait Time Thresholds -->
#### Configuring Notification Wait Time Thresholds

<!-- You may configure how many seconds are considered a "long wait" within your application's `config/horizon.php` configuration file. The `waits` configuration option within this file allows you to control the long wait threshold for each connection / queue combination. Any undefined connection / queue combinations will default to a long wait threshold of 60 seconds: -->
アプリケーションの `config/horizon.php` 構成ファイル内で、「長い待機」とみなされる秒数を構成できます。このファイル内の `waits` 構成オプションを使用すると、接続とキューの組み合わせごとに長時間待機のしきい値を制御できます。未定義の接続/キューの組み合わせは、デフォルトで 60 秒の長時間待機しきい値に設定されます。

```
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
<!-- ## Metrics -->
## Metrics

<!-- Horizon includes a metrics dashboard which provides information regarding your job and queue wait times and throughput. In order to populate this dashboard, you should configure Horizon's `snapshot` Artisan command to run every five minutes in your application's `routes/console.php` file: -->
Horizon には、ジョブとキューの待機時間とスループットに関する情報を提供するメトリクス ダッシュボードが含まれています。このダッシュボードにデータを入力するには、アプリケーションの `routes/console.php` ファイルで Horizon の `snapshot` Artisan コマンドを 5 分ごとに実行するように構成する必要があります。

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
<!-- ## Deleting Failed Jobs -->
## Deleting Failed Jobs

<!-- If you would like to delete a failed job, you may use the `horizon:forget` command. The `horizon:forget` command accepts the ID or UUID of the failed job as its only argument: -->
失敗したジョブを削除したい場合は、`horizon:forget` コマンドを使用できます。 `horizon:forget` コマンドは、失敗したジョブの ID または UUID を唯一の引数として受け入れます。

```shell
php artisan horizon:forget 5
```

<!-- If you would like to delete all failed jobs, you may provide the `--all` option to the `horizon:forget` command: -->
失敗したジョブをすべて削除したい場合は、`--all` オプションを `horizon:forget` コマンドに指定します。

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
<!-- ## Clearing Jobs From Queues -->
## Clearing Jobs From Queues

<!-- If you would like to delete all jobs from your application's default queue, you may do so using the `horizon:clear` Artisan command: -->
アプリケーションのデフォルト キューからすべてのジョブを削除したい場合は、`horizon:clear` Artisan コマンドを使用して削除できます。

```shell
php artisan horizon:clear
```

<!-- You may provide the `queue` option to delete jobs from a specific queue: -->
`queue` オプションを指定して、特定のキューからジョブを削除できます。

```shell
php artisan horizon:clear --queue=emails
```

