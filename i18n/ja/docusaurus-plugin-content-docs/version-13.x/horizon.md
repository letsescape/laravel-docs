<!-- # Laravel Horizon -->
# Laravel Horizon

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Dashboard Authorization](#dashboard-authorization)
    - [Max Job Attempts](#max-job-attempts)
    - [Job Timeout](#job-timeout)
    - [Job Backoff](#job-backoff)
    - [Other Worker Options](#other-worker-options)
    - [Silenced Jobs](#silenced-jobs)
- [Balancing Strategies](#balancing-strategies)
    - [Auto Balancing](#auto-balancing)
    - [Simple Balancing](#simple-balancing)
    - [No Balancing](#no-balancing)
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
> Laravel Horizon について詳しく知る前に、Laravel のベース [queue services](/docs/13.x/queues) についてよく理解しておく必要があります。 Horizon は、Laravel が提供する基本的なキュー機能にまだ慣れていない場合、混乱を招く可能性がある追加機能で Laravel のキューを強化します。

<!-- [Laravel Horizon](https://github.com/laravel/horizon) provides a beautiful dashboard and code-driven configuration for your Laravel powered [Redis queues](/docs/13.x/queues). Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. -->
[Laravel Horizon](https://github.com/laravel/horizon) は、Laravel を利用した [Redis queues](/docs/13.x/queues) に美しいダッシュボードとコード駆動の構成を提供します。 Horizon を使用すると、ジョブのスループット、実行時間、ジョブの失敗など、キュー システムの主要なメトリクスを簡単に監視できます。

<!-- When using Horizon, all of your queue worker configuration is stored in a single, simple configuration file. By defining your application's worker configuration in a version controlled file, you may easily scale or modify your application's queue workers when deploying your application. -->
Horizon を使用する場合、すべてのキューワーカー構成は 1 つの単純な構成ファイルに保存されます。バージョン管理されたファイルでアプリケーションのワーカー構成を定義すると、アプリケーションのデプロイ時にアプリケーションのキューワーカーを簡単に拡張または変更できます。

<img src="https://laravel.com/img/docs/horizon-example.png"/>

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Horizon では、キューに電力を供給するために [Redis](https://redis.io) を使用する必要があります。したがって、アプリケーションの `config/queue.php` 構成ファイルでキュー接続が `redis` に設定されていることを確認する必要があります。現時点では、Horizon は Redis Cluster と互換性がありません。

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

<a name="content-security-policy-csp-nonce"></a>
<!-- #### Content Security Policy (CSP) Nonce -->
#### Content Security Policy (CSP) Nonce

<!-- If you would like to use a [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce) on the script and style tags used in Horizon views as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may use the `Horizon::cspNonce` method to specify the nonce to use. This method should typically be invoked within middleware so that a new nonce is assigned for each request: -->
Horizon のビューで使用する script タグと style タグに、[Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) の一部として [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce) を指定したい場合は、`Horizon::cspNonce` メソッドを使用して nonce を指定できます。通常、このメソッドはミドルウェア内で呼び出し、リクエストごとに新しい nonce が割り当てられるようにします。

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Horizon\Horizon;
use Symfony\Component\HttpFoundation\Response;

public function handle(Request $request, Closure $next): Response
{
    Horizon::cspNonce('csp-nonce');

    return $next($request);
}
```

<!-- You may add this middleware to the `middleware` option in your application's `config/horizon.php` configuration file: -->
このミドルウェアは、アプリケーションの `config/horizon.php` 設定ファイルにある `middleware` オプションへ追加できます。

```php
'middleware' => [
    'web',
    App\Http\Middleware\AddHorizonCspNonce::class,
],
```

<a name="environments"></a>
<!-- #### Environments -->
#### Environments

<!-- After installation, the primary Horizon configuration option that you should familiarize yourself with is the `environments` configuration option. This configuration option is an array of environments that your application runs on and defines the worker process options for each environment. By default, this entry contains a `production` and `local` environment. However, you are free to add more environments as needed: -->
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

<!-- You may also define a wildcard environment (`*`) which will be used when no other matching environment is found: -->
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

<!-- When you start Horizon, it will use the worker process configuration options for the environment that your application is running on. Typically, the environment is determined by the value of the `APP_ENV` [environment variable](/docs/13.x/configuration#determining-the-current-environment). For example, the default `local` Horizon environment is configured to start three worker processes and automatically balance the number of worker processes assigned to each queue. The default `production` environment is configured to start a maximum of 10 worker processes and automatically balance the number of worker processes assigned to each queue. -->
Horizon を起動すると、アプリケーションが実行されている環境のワーカー プロセス構成オプションが使用されます。通常、環境は `APP_ENV` [environment variable](/docs/13.x/configuration#determining-the-current-environment) の値によって決まります。たとえば、デフォルトの `local` Horizon 環境は、3 つのワーカー プロセスを開始し、各キューに割り当てられたワーカー プロセスの数のバランスを自動的に調整するように構成されています。デフォルトの `production` 環境は、最大 10 個のワーカー プロセスを開始し、各キューに割り当てられるワーカー プロセスの数のバランスを自動的に調整するように構成されています。

> [!WARNING]
> `horizon` 構成ファイルの `environments` 部分に、Horizon を実行する予定の各 [environment](/docs/13.x/configuration#environment-configuration) のエントリが含まれていることを確認する必要があります。

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

<!-- While your application is in [maintenance mode](/docs/13.x/configuration#maintenance-mode), queued jobs will not be processed by Horizon unless the supervisor's `force` option is defined as `true` within the Horizon configuration file: -->
アプリケーションが [maintenance mode](/docs/13.x/configuration#maintenance-mode) にある間は、Horizon 構成ファイル内でスーパーバイザの `force` オプションが `true` として定義されていない限り、キューに入れられたジョブは Horizon によって処理されません。

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
<!-- #### Default Values -->
#### Default Values

<!-- Within Horizon's default configuration file, you will notice a `defaults` configuration option. This configuration option specifies the default values for your application's [supervisors](#supervisors). The supervisor's default configuration values will be merged into the supervisor's configuration for each environment, allowing you to avoid unnecessary repetition when defining your supervisors. -->
Horizon のデフォルト構成ファイル内に、`defaults` 構成オプションがあることがわかります。この構成オプションは、アプリケーションの [supervisors](#supervisors) のデフォルト値を指定します。スーパーバイザのデフォルト設定値は、各環境のスーパーバイザの設定にマージされるため、スーパーバイザを定義する際に不必要な繰り返しを避けることができます。

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Horizon dashboard may be accessed via the `/horizon` route. By default, you will only be able to access this dashboard in the `local` environment. However, within your `app/Providers/HorizonServiceProvider.php` file, there is an [authorization gate](/docs/13.x/authorization#gates) definition. This authorization gate controls access to Horizon in **non-local** environments. You are free to modify this gate as needed to restrict access to your Horizon installation: -->
Horizon ダッシュボードには、`/horizon` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。ただし、`app/Providers/HorizonServiceProvider.php` ファイル内には、[authorization gate](/docs/13.x/authorization#gates) 定義があります。この認可ゲートは、**非ローカル**環境での Horizon へのアクセスを制御します。 Horizon インストールへのアクセスを制限するために、必要に応じてこのゲートを自由に変更できます。

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
<!-- #### Alternative Authentication Strategies -->
#### Alternative Authentication Strategies

<!-- Remember that Laravel automatically injects the authenticated user into the gate closure. If your application is providing Horizon security via another method, such as IP restrictions, then your Horizon users may not need to "login". Therefore, you will need to change `function (User $user)` closure signature above to `function (User $user = null)` in order to force Laravel to not require authentication. -->
Laravel は認証されたユーザーをゲート クロージャに自動的に挿入することに注意してください。アプリケーションが IP 制限などの別の方法で Horizon セキュリティを提供している場合、Horizon ユーザーは「ログイン」する必要がない場合があります。したがって、Laravel に認証を要求しないようにするには、上記の `function (User $user)` クロージャー署名を `function (User $user = null)` に変更する必要があります。

<a name="max-job-attempts"></a>
<!-- ### Max Job Attempts -->
### Max Job Attempts

> [!NOTE]
> これらのオプションを調整する前に、Laravel のデフォルトの [queue services](/docs/13.x/queues#max-job-attempts-and-timeout) と「試行」の概念をよく理解してください。

<!-- You can define the maximum number of attempts a job can consume within a supervisor's configuration: -->
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

<!-- Adjusting the `tries` option is essential when using middlewares such as `WithoutOverlapping` or `RateLimited` because they consume attempts. To handle this, adjust the `tries` configuration value either at the supervisor level or by defining the `$tries` property on the job class. -->
`WithoutOverlapping` や `RateLimited` などのミドルウェアを使用する場合、試行回数が消費されるため、`tries` オプションの調整が不可欠です。これに対処するには、Supervisor レベルで、またはジョブ クラスで `$tries` プロパティを定義することによって、`tries` 構成値を調整します。

<!-- If you don't set the `tries` option, Horizon defaults to a single attempt, unless the job class defines `$tries`, which takes precedence over the Horizon configuration. -->
`tries` オプションを設定しない場合、ジョブ クラスで `$tries` が定義されていない限り、Horizon はデフォルトで 1 回の試行を行います。これは Horizon 設定よりも優先されます。

<!-- Setting `tries` or `$tries` to 0 allows unlimited attempts, which is ideal when the number of attempts is uncertain. To prevent endless failures, you can limit the number of exceptions allowed by setting the `$maxExceptions` property on the job class. -->
`tries` または `$tries` を 0 に設定すると、無制限の試行が可能になり、試行回数が不確実な場合に最適です。無限の失敗を防ぐために、ジョブ クラスで `$maxExceptions` プロパティを設定することで、許可される例外の数を制限できます。

<a name="job-timeout"></a>
<!-- ### Job Timeout -->
### Job Timeout

<!-- Similarly, you can set a `timeout` value at the supervisor level, which specifies how many seconds a worker process can run a job before it's forcefully terminated. Once terminated, the job will either be retried or marked as failed, depending on your queue configuration: -->
同様に、スーパーバイザ レベルで `timeout` 値を設定できます。これは、ワーカー プロセスがジョブを強制終了するまでにジョブを実行できる秒数を指定します。終了すると、ジョブはキュー構成に応じて再試行されるか、失敗としてマークされます。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> `auto` バランス戦略を使用する場合、Horizon は進行中のワーカーを「ハング」とみなし、スケールダウン中の Horizon タイムアウト後にそれらを強制終了します。 Horizon タイムアウトがどのジョブ レベルのタイムアウトよりも大きいことを常に確認してください。そうしないと、ジョブが実行中に終了する可能性があります。さらに、`timeout` 値は、`config/queue.php` 構成ファイルで定義されている `retry_after` 値よりも常に少なくとも数秒短くする必要があります。そうしないと、ジョブが 2 回処理される可能性があります。

<a name="job-backoff"></a>
<!-- ### Job Backoff -->
### Job Backoff

<!-- You can define the `backoff` value at the supervisor level to specify how long Horizon should wait before retrying a job that encounters an unhandled exception: -->
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

<!-- You may also configure "exponential" backoffs by using an array for the `backoff` value. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
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

<a name="other-worker-options"></a>
<!-- ### Other Worker Options -->
### Other Worker Options

<!-- In addition to `tries`, `timeout`, and `backoff`, each supervisor accepts several other options that control how its worker processes behave and when they are automatically restarted. Periodically restarting workers is a good practice for long-running processes, as it helps guard against memory leaks: -->
`tries`、`timeout`、`backoff` に加えて、各 supervisor は、ワーカープロセスの動作や自動的に再起動されるタイミングを制御する複数のオプションを受け付けます。長時間実行されるプロセスでは、ワーカーを定期的に再起動することをおすすめします。メモリリークの防止に役立つためです。

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'memory' => 128,
            'maxJobs' => 1000,
            'maxTime' => 3600,
            'sleep' => 3,
            'rest' => 0,
            'nice' => 0,
        ],
    ],
],
```

<div class="content-list" markdown="1">

<!-- - `memory` defines the maximum amount of memory, in megabytes, that a single worker process may consume before it is restarted. By default, this value is `128`. - `maxJobs` defines the number of jobs a worker should process before restarting. A value of `0` indicates that workers should not be restarted based on the number of jobs processed. By default, this value is `0`. - `maxTime` defines the number of seconds a worker should run before restarting. A value of `0` indicates that workers should not be restarted based on time. By default, this value is `0`. - `sleep` defines the number of seconds a worker should wait when no job is available before polling the queue for new jobs again. By default, this value is `3`. - `rest` defines the number of seconds to pause between processing each job. By default, this value is `0`. - `nice` defines the "niceness" (scheduling priority) of the worker processes. A higher value gives the process a lower priority. By default, this value is `0`. -->
- `memory` は、単一のワーカープロセスが再起動されるまでに使用できるメモリの最大量をメガバイト単位で定義します。デフォルト値は `128` です。
- `maxJobs` は、ワーカーが再起動されるまでに処理するジョブ数を定義します。値に `0` を指定すると、処理したジョブ数に基づくワーカーの再起動を無効にします。デフォルト値は `0` です。
- `maxTime` は、ワーカーが再起動されるまでの実行時間を秒単位で定義します。値に `0` を指定すると、時間に基づくワーカーの再起動を無効にします。デフォルト値は `0` です。
- `sleep` は、利用可能なジョブがない場合に、ワーカーが新しいジョブを再びポーリングするまで待機する秒数を定義します。デフォルト値は `3` です。
- `rest` は、各ジョブの処理間に一時停止する秒数を定義します。デフォルト値は `0` です。
- `nice` は、ワーカープロセスの「nice 値」（スケジューリング優先度）を定義します。値を大きくすると、プロセスの優先度が下がります。デフォルト値は `0` です。

</div>

<a name="silenced-jobs"></a>
<!-- ### Silenced Jobs -->
### Silenced Jobs

<!-- Sometimes, you may not be interested in viewing certain jobs dispatched by your application or third-party packages. Instead of these jobs taking up space in your "Completed Jobs" list, you can silence them. To get started, add the job's class name to the `silenced` configuration option in your application's `horizon` configuration file: -->
場合によっては、アプリケーションまたはサードパーティのパッケージによってディスパッチされた特定のジョブを表示することに興味がない場合があります。これらのジョブが「完了したジョブ」リストのスペースを占める代わりに、それらのジョブを沈黙させることができます。まず、ジョブのクラス名をアプリケーションの `horizon` 構成ファイルの `silenced` 構成オプションに追加します。

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

<!-- In addition to silencing individual job classes, Horizon also supports silencing jobs based on [tags](#tags). This can be useful if you want to hide multiple jobs that share a common tag: -->
Horizon は、個々のジョブ クラスのサイレント化に加えて、[tags](#tags) に基づいたジョブのサイレント化もサポートしています。これは、共通のタグを共有する複数のジョブを非表示にする場合に便利です。

```php
'silenced_tags' => [
    'notifications'
],
```

<!-- Alternatively, the job you wish to silence can implement the `Laravel\Horizon\Contracts\Silenced` interface. If a job implements this interface, it will automatically be silenced, even if it is not present in the `silenced` configuration array: -->
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
<!-- ## Balancing Strategies -->
## Balancing Strategies

<!-- Each supervisor can process one or more queues but unlike Laravel's default queue system, Horizon allows you to choose from three worker balancing strategies: `auto`, `simple`, and `false`. -->
各スーパーバイザは 1 つ以上のキューを処理できますが、Laravel のデフォルトのキュー システムとは異なり、Horizon では、`auto`、`simple`、`false` の 3 つのワーカー バランシング戦略から選択できます。

<a name="auto-balancing"></a>
<!-- ### Auto Balancing -->
### Auto Balancing

<!-- The `auto` strategy, which is the default strategy, adjusts the number of worker processes per queue based on the current workload of the queue. For example, if your `notifications` queue has 1,000 pending jobs while your `default` queue is empty, Horizon will allocate more workers to your `notifications` queue until the queue is empty. -->
デフォルトの戦略である `auto` 戦略は、キューの現在のワークロードに基づいてキューごとのワーカー プロセスの数を調整します。たとえば、`notifications` キューに 1,000 個の保留中のジョブがあり、`default` キューが空の場合、Horizon はキューが空になるまでより多くのワーカーを `notifications` キューに割り当てます。

<!-- When using the `auto` strategy, you may also configure the `minProcesses` and `maxProcesses` configuration options: -->
`auto` 戦略を使用する場合は、`minProcesses` および `maxProcesses` 構成オプションも構成できます。

<div class="content-list" markdown="1">

<!-- - `minProcesses` defines the minimum number of worker processes per queue. This value must be greater than or equal to 1. - `maxProcesses` defines the maximum total number of worker processes Horizon may scale up to across all queues. This value should typically be greater than the number of queues multiplied by the `minProcesses` value. To prevent the supervisor from spawning any processes, you may set this value to 0. -->
- `minProcesses` は、キューごとのワーカー プロセスの最小数を定義します。この値は 1 以上である必要があります。
- `maxProcesses` は、Horizon がすべてのキューにわたってスケールアップできるワーカー プロセスの最大合計数を定義します。この値は通常、キューの数に `minProcesses` 値を乗算した値より大きくなければなりません。スーパーバイザがプロセスを生成しないようにするには、この値を 0 に設定します。

</div>

<!-- For example, you may configure Horizon to maintain at least one process per queue and scale up to a total of 10 worker processes: -->
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

<!-- The `autoScalingStrategy` configuration option determines how Horizon will assign more worker processes to queues. You can choose between two strategies: -->
`autoScalingStrategy` 構成オプションは、Horizon がより多くのワーカー プロセスをキューに割り当てる方法を決定します。次の 2 つの戦略から選択できます。

<div class="content-list" markdown="1">

<!-- - The `time` strategy will assign workers based on the total estimated amount of time it will take to clear the queue. - The `size` strategy will assign workers based on the total number of jobs on the queue. -->
- `time` 戦略は、キューをクリアするのにかかる推定合計時間に基づいてワーカーを割り当てます。
- `size` ストラテジーは、キュー上のジョブの合計数に基づいてワーカーを割り当てます。

</div>

<!-- The `balanceMaxShift` and `balanceCooldown` configuration values determine how quickly Horizon will scale to meet worker demand. In the example above, a maximum of one new process will be created or destroyed every three seconds. You are free to tweak these values as necessary based on your application's needs. -->
`balanceMaxShift` および `balanceCooldown` の構成値は、ワーカーの需要を満たすために Horizon がどの程度の速度でスケールするかを決定します。上の例では、3 秒ごとに最大 1 つの新しいプロセスが作成または破棄されます。アプリケーションのニーズに基づいて、必要に応じてこれらの値を自由に調整できます。

<a name="auto-queue-priorities"></a>
<!-- #### Queue Priorities and Auto Balancing -->
#### Queue Priorities and Auto Balancing

<!-- When using the `auto` balancing strategy, Horizon does not enforce strict priority between queues. The order of queues in a supervisor's configuration does not affect how worker processes are assigned. Instead, Horizon relies on the selected `autoScalingStrategy` to dynamically allocate worker processes based on queue load. -->
`auto` バランス戦略を使用する場合、Horizon はキュー間の厳密な優先順位を強制しません。スーパーバイザの構成内のキューの順序は、ワーカー プロセスの割り当て方法には影響しません。代わりに、Horizon は選択された `autoScalingStrategy` に依存して、キューの負荷に基づいてワーカー プロセスを動的に割り当てます。

<!-- For example, in the following configuration, the high queue is not prioritized over the default queue, despite appearing first in the list: -->
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

<!-- If you need to enforce a relative priority between queues, you may define multiple supervisors and explicitly allocate processing resources: -->
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

<!-- In this example, the default `queue` can scale up to 10 processes, while the `images` queue is limited to one process. This configuration ensures that your queues can scale independently. -->
この例では、デフォルトの `queue` は最大 10 プロセスまでスケールできますが、`images` キューは 1 プロセスに制限されています。この構成により、キューを独立して拡張できるようになります。

> [!NOTE]
> リソースを大量に消費するジョブをディスパッチする場合、`maxProcesses` 値を制限した専用キューにジョブを割り当てることが最善の場合があります。そうしないと、これらのジョブが過剰な CPU リソースを消費し、システムに過負荷がかかる可能性があります。

<a name="simple-balancing"></a>
<!-- ### Simple Balancing -->
### Simple Balancing

<!-- The `simple` strategy distributes worker processes evenly across the specified queues. With this strategy, Horizon does not automatically scale the number of worker processes. Rather, it uses a fixed number of processes: -->
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

<!-- In the example above, Horizon will assign 5 processes to each queue, splitting the total of 10 evenly. -->
上の例では、Horizon は各キューに 5 つのプロセスを割り当て、合計 10 を均等に分割します。

<!-- If you'd like to control the number of worker processes assigned to each queue individually, you can define multiple supervisors: -->
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

<!-- With this configuration, Horizon will assign 10 processes to the `default` queue and 2 processes to the `notifications` queue. -->
この構成では、Horizon は 10 個のプロセスを `default` キューに割り当て、2 個のプロセスを `notifications` キューに割り当てます。

<a name="no-balancing"></a>
<!-- ### No Balancing -->
### No Balancing

<!-- When the `balance` option is set to `false`, Horizon processes queues strictly in the order they're listed, similar to Laravel's default queue system. However, it will still scale the number of worker processes if jobs begin to accumulate: -->
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

<!-- In the example above, jobs in the `default` queue are always prioritized over jobs in the `notifications` queue. For instance, if there are 1,000 jobs in `default` and only 10 in `notifications`, Horizon will fully process all `default` jobs before handling any from `notifications`. -->
上の例では、`default` キュー内のジョブは、常に `notifications` キュー内のジョブより優先されます。たとえば、`default` に 1,000 個のジョブがあり、`notifications` には 10 個しかない場合、Horizon は、`notifications` からのジョブを処理する前に、すべての `default` ジョブを完全に処理します。

<!-- You can control Horizon's ability to scale worker processes using the `minProcesses` and `maxProcesses` options: -->
`minProcesses` および `maxProcesses` オプションを使用して、ワーカー プロセスをスケーリングする Horizon の機能を制御できます。

<div class="content-list" markdown="1">

<!-- - `minProcesses` defines the minimum number of worker processes in total. This value must be greater than or equal to 1. - `maxProcesses` defines the maximum total number of worker processes Horizon may scale up to. -->
- `minProcesses` は、ワーカー プロセスの合計の最小数を定義します。この値は 1 以上である必要があります。
- `maxProcesses` は、Horizon がスケールアップできるワーカー プロセスの最大合計数を定義します。

</div>

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

<a name="automatically-restarting-horizon"></a>
<!-- #### Automatically Restarting Horizon -->
#### Automatically Restarting Horizon

<!-- During local development, you may run the `horizon:listen` command. When using the `horizon:listen` command, you don't have to manually restart Horizon when you want to reload your updated code. Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
ローカル開発中に、`horizon:listen` コマンドを実行できます。 `horizon:listen` コマンドを使用すると、更新されたコードをリロードするときに Horizon を手動で再起動する必要がありません。この機能を使用する前に、[Node](https://nodejs.org) がローカル開発環境にインストールされていることを確認する必要があります。さらに、プロジェクト内に [Chokidar](https://github.com/paulmillr/chokidar) ファイル監視ライブラリをインストールする必要があります。

```shell
npm install --save-dev chokidar
```

<!-- Once Chokidar is installed, you may start Horizon using the `horizon:listen` command: -->
Chokidar がインストールされたら、`horizon:listen` コマンドを使用して Horizon を起動できます。

```shell
php artisan horizon:listen
```

<!-- When running within Docker or Vagrant, you should use the `--poll` option: -->
Docker または Vagrant 内で実行する場合は、`--poll` オプションを使用する必要があります。

```shell
php artisan horizon:listen --poll
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/horizon.php` configuration file: -->
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
> Supervisorを自分で設定するのが大変だと思われる場合は、Laravel アプリケーションのバックグラウンド プロセスを管理できる [Laravel Cloud](https://cloud.laravel.com) の使用を検討してください。

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

<!-- Horizon allows you to assign "tags" to jobs, including mailables, broadcast events, notifications, and queued event listeners. In fact, Horizon will intelligently and automatically tag most jobs depending on the Eloquent models that are attached to the job. For example, take a look at the following job: -->
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

<!-- If this job is queued with an `App\Models\Video` instance that has an `id` attribute of `1`, it will automatically receive the tag `App\Models\Video:1`. This is because Horizon will search the job's properties for any Eloquent models. If Eloquent models are found, Horizon will intelligently tag the job using the model's class name and primary key: -->
このジョブが、`1` の `id` 属性を持つ `App\Models\Video` インスタンスとともにキューに入れられた場合、自動的にタグ `App\Models\Video:1` を受け取ります。これは、Horizon がジョブのプロパティで Eloquent モデルを検索するためです。 Eloquent モデルが見つかった場合、Horizon はモデルのクラス名と主キーを使用してジョブにインテリジェントにタグ付けします。

```php
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
<!-- #### Manually Tagging Event Listeners -->
#### Manually Tagging Event Listeners

<!-- When retrieving the tags for a queued event listener, Horizon will automatically pass the event instance to the `tags` method, allowing you to add event data to the tags: -->
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
<!-- ## Notifications -->
## Notifications

> [!WARNING]
> Slack または SMS 通知を送信するように Horizon を構成する場合は、[prerequisites for the relevant notification channel](/docs/13.x/notifications) を確認する必要があります。

<!-- If you would like to be notified when one of your queues has a long wait time, you may use the `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, and `Horizon::routeSmsNotificationsTo` methods. You may call these methods from the `boot` method of your application's `App\Providers\HorizonServiceProvider`: -->
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
<!-- #### Configuring Notification Wait Time Thresholds -->
#### Configuring Notification Wait Time Thresholds

<!-- You may configure how many seconds are considered a "long wait" within your application's `config/horizon.php` configuration file. The `waits` configuration option within this file allows you to control the long wait threshold for each connection / queue combination. Any undefined connection / queue combinations will default to a long wait threshold of 60 seconds: -->
アプリケーションの `config/horizon.php` 構成ファイル内で、「長い待機」とみなされる秒数を構成できます。このファイル内の `waits` 構成オプションを使用すると、接続とキューの組み合わせごとに長時間待機のしきい値を制御できます。未定義の接続/キューの組み合わせは、デフォルトで 60 秒の長時間待機しきい値に設定されます。

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<!-- Setting a queue's threshold to `0` will disable long wait notifications for that queue. -->
キューのしきい値を `0` に設定すると、そのキューの長時間待機の通知が無効になります。

<a name="metrics"></a>
<!-- ## Metrics -->
## Metrics

<!-- Horizon includes a metrics dashboard which provides information regarding your job and queue wait times and throughput. In order to populate this dashboard, you should configure Horizon's `snapshot` Artisan command to run every five minutes in your application's `routes/console.php` file: -->
Horizon には、ジョブとキューの待機時間とスループットに関する情報を提供するメトリクス ダッシュボードが含まれています。このダッシュボードにデータを入力するには、アプリケーションの `routes/console.php` ファイルで Horizon の `snapshot` Artisan コマンドを 5 分ごとに実行するように構成する必要があります。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<!-- You may configure how many snapshots Horizon retains for its metrics graphs using the `metrics.trim_snapshots` option in your application's `config/horizon.php` configuration file. Because this option limits the number of snapshots rather than their age, the retention period depends on how frequently the `horizon:snapshot` command runs: -->
Horizon がメトリクスグラフ用に保持するスナップショットの数は、アプリケーションの `config/horizon.php` 設定ファイルにある `metrics.trim_snapshots` オプションで設定できます。このオプションはスナップショットの経過時間ではなく数を制限するため、保持期間は `horizon:snapshot` コマンドの実行頻度によって異なります。

```php
'metrics' => [
    'trim_snapshots' => [
        'job' => 24,
        'queue' => 24,
    ],
],
```

<!-- If you would like to delete all metric data, you can invoke the `horizon:clear-metrics` Artisan command: -->
すべてのメトリック データを削除したい場合は、`horizon:clear-metrics` Artisan コマンドを呼び出します。

```shell
php artisan horizon:clear-metrics
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
