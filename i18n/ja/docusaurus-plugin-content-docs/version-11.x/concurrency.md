<!-- # Concurrency -->
# Concurrency

- [Introduction](#introduction)
- [Running Concurrent Tasks](#running-concurrent-tasks)
- [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!WARNING]
> Laravel の `Concurrency` ファサードは、コミュニティからのフィードバックを収集している間、現在ベータ版です。

<!-- Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently. -->
場合によっては、相互に依存しないいくつかの遅いタスクを実行する必要がある場合があります。多くの場合、タスクを同時に実行することで大幅なパフォーマンスの向上を実現できます。 Laravel の `Concurrency` ファサードは、クロージャを同時に実行するためのシンプルで便利な API を提供します。

<a name="concurrency-compatibility"></a>
<!-- #### Concurrency Compatibility -->
#### Concurrency Compatibility

<!-- If you upgraded to Laravel 11.x from a Laravel 10.x application, you may need to add the `ConcurrencyServiceProvider` to the `providers` array in your application's `config/app.php` configuration file: -->
Laravel 10.x アプリケーションから Laravel 11.x にアップグレードした場合は、アプリケーションの `config/app.php` 構成ファイルの `providers` 配列に `ConcurrencyServiceProvider` を追加する必要がある場合があります。

```php
'providers' => ServiceProvider::defaultProviders()->merge([
    /*
     * Package Service Providers...
     */
    Illuminate\Concurrency\ConcurrencyServiceProvider::class, // [tl! add]

    /*
     * Application Service Providers...
     */
    App\Providers\AppServiceProvider::class,
    App\Providers\AuthServiceProvider::class,
    // App\Providers\BroadcastServiceProvider::class,
    App\Providers\EventServiceProvider::class,
    App\Providers\RouteServiceProvider::class,
])->toArray(),
```

<a name="how-it-works"></a>
<!-- #### How it Works -->
#### How it Works

<!-- Laravel achieves concurrency by serializing the given closures and dispatching them to a hidden Artisan CLI command, which unserializes the closures and invokes it within its own PHP process. After the closure has been invoked, the resulting value is serialized back to the parent process. -->
Laravel は、指定されたクロージャをシリアル化し、隠された Artisan CLI コマンドにディスパッチすることで同時実行性を実現します。このコマンドは、クロージャをシリアル化解除して、独自の PHP プロセス内で呼び出します。クロージャが呼び出された後、結果の値は親プロセスにシリアル化されて戻されます。

<!-- The `Concurrency` facade supports three drivers: `process` (the default), `fork`, and `sync`. -->
`Concurrency` ファサードは、`process` (デフォルト)、`fork`、および `sync` の 3 つのドライバをサポートします。

<!-- The `fork` driver offers improved performance compared to the default `process` driver, but it may only be used within PHP's CLI context, as PHP does not support forking during web requests. Before using the `fork` driver, you need to install the `spatie/fork` package: -->
`fork` ドライバは、デフォルトの `process` ドライバと比較してパフォーマンスが向上していますが、PHP は Web リクエスト中のフォークをサポートしていないため、PHP の CLI コンテキスト内でのみ使用できます。 `fork` ドライバを使用する前に、`spatie/fork` パッケージをインストールする必要があります。

```bash
composer require spatie/fork
```

<!-- The `sync` driver is primarily useful during testing when you want to disable all concurrency and simply execute the given closures in sequence within the parent process. -->
`sync` ドライバは、すべての同時実行性を無効にして、親プロセス内で指定されたクロージャを順番に実行するだけのテスト中に主に役立ちます。

<a name="running-concurrent-tasks"></a>
<!-- ## Running Concurrent Tasks -->
## Running Concurrent Tasks

<!-- To run concurrent tasks, you may invoke the `Concurrency` facade's `run` method. The `run` method accepts an array of closures which should be executed simultaneously in child PHP processes: -->
同時タスクを実行するには、`Concurrency` ファサードの `run` メソッドを呼び出します。 `run` メソッドは、子 PHP プロセスで同時に実行する必要があるクロージャの配列を受け入れます。

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

<!-- To use a specific driver, you may use the `driver` method: -->
特定のドライバを使用するには、`driver` メソッドを使用できます。

```php
$results = Concurrency::driver('fork')->run(...);
```

<!-- Or, to change the default concurrency driver, you should publish the `concurrency` configuration file via the `config:publish` Artisan command and update the `default` option within the file: -->
または、デフォルトの同時実行ドライバを変更するには、`config:publish` Artisan コマンドを使用して `concurrency` 構成ファイルを公開し、ファイル内の `default` オプションを更新する必要があります。

```bash
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
<!-- ## Deferring Concurrent Tasks -->
## Deferring Concurrent Tasks

<!-- If you would like to execute an array of closures concurrently, but are not interested in the results returned by those closures, you should consider using the `defer` method. When the `defer` method is invoked, the given closures are not executed immediately. Instead, Laravel will execute the closures concurrently after the HTTP response has been sent to the user: -->
クロージャの配列を同時に実行したいが、それらのクロージャによって返される結果には興味がない場合は、`defer` メソッドの使用を検討する必要があります。 `defer` メソッドが呼び出されたとき、指定されたクロージャはすぐには実行されません。代わりに、Laravel は HTTP 応答がユーザーに送信された後にクロージャーを同時に実行します。

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```

