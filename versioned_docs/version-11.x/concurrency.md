<!-- # Concurrency -->
# Concurrency

- [Introduction](#introduction)
- [Running Concurrent Tasks](#running-concurrent-tasks)
- [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!WARNING]
> Laravel의 `Concurrency` 파사드는 현재 베타 버전으로, 커뮤니티 피드백을 수집하는 중입니다.

<!-- Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently. -->
여러 개의 느린 작업이 서로 의존하지 않는 경우, 이 작업들을 동시에 실행해서 성능을 크게 향상시킬 수 있습니다. Laravel의 `Concurrency` 파사드는 클로저(익명 함수)를 동시에 실행할 수 있게 해주는 간편한 API를 제공합니다.

<a name="concurrency-compatibility"></a>
<!-- #### Concurrency Compatibility -->
#### Concurrency Compatibility

<!-- If you upgraded to Laravel 11.x from a Laravel 10.x application, you may need to add the `ConcurrencyServiceProvider` to the `providers` array in your application's `config/app.php` configuration file: -->
Laravel 10.x에서 11.x로 업그레이드한 경우, 애플리케이션의 `config/app.php` 설정 파일 내 `providers` 배열에 `ConcurrencyServiceProvider`를 추가해야 할 수 있습니다:

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
Laravel은 전달된 클로저를 직렬화하여 숨겨진 아티즌 명령어로 전달하고, 해당 명령어가 클로저를 역직렬화해 각각의 독립된 PHP 프로세스에서 실행합니다. 클로저의 실행이 끝나면, 그 결과 값을 다시 직렬화해 부모 프로세스로 전달합니다.

<!-- The `Concurrency` facade supports three drivers: `process` (the default), `fork`, and `sync`. -->
`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: `process`(기본값), `fork`, `sync`.

<!-- The `fork` driver offers improved performance compared to the default `process` driver, but it may only be used within PHP's CLI context, as PHP does not support forking during web requests. Before using the `fork` driver, you need to install the `spatie/fork` package: -->
`fork` 드라이버는 기본 `process` 드라이버보다 더 나은 성능을 제공하지만, PHP의 웹 요청 환경에서는 포킹을 지원하지 않으므로 CLI 환경에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 `spatie/fork` 패키지를 먼저 설치해야 합니다.

```bash
composer require spatie/fork
```

<!-- The `sync` driver is primarily useful during testing when you want to disable all concurrency and simply execute the given closures in sequence within the parent process. -->
`sync` 드라이버는 주로 테스트 상황에서 모든 동시성을 비활성화하고, 클로저들을 부모 프로세스에서 순차적으로 실행하고 싶을 때 유용합니다.

<a name="running-concurrent-tasks"></a>
<!-- ## Running Concurrent Tasks -->
## Running Concurrent Tasks

<!-- To run concurrent tasks, you may invoke the `Concurrency` facade's `run` method. The `run` method accepts an array of closures which should be executed simultaneously in child PHP processes: -->
여러 작업을 동시에 실행하려면, `Concurrency` 파사드의 `run` 메서드를 사용하면 됩니다. `run` 메서드는 동시에 실행할 클로저들의 배열을 받아, 각각의 PHP 자식 프로세스에서 동시에 실행합니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

<!-- To use a specific driver, you may use the `driver` method: -->
특정 드라이버를 사용하려면 `driver` 메서드를 이용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

<!-- Or, to change the default concurrency driver, you should publish the `concurrency` configuration file via the `config:publish` Artisan command and update the `default` option within the file: -->
기본 동시성 드라이버를 변경하고 싶다면, `config:publish` 아티즌 명령어로 `concurrency` 설정 파일을 발행한 후, 해당 파일의 `default` 옵션을 수정하면 됩니다.

```bash
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
<!-- ## Deferring Concurrent Tasks -->
## Deferring Concurrent Tasks

<!-- If you would like to execute an array of closures concurrently, but are not interested in the results returned by those closures, you should consider using the `defer` method. When the `defer` method is invoked, the given closures are not executed immediately. Instead, Laravel will execute the closures concurrently after the HTTP response has been sent to the user: -->
클로저 배열을 동시에 실행하되, 각 클로저의 반환값에는 관심이 없는 경우 `defer` 메서드를 사용할 수 있습니다. `defer` 메서드는 즉시 클로저를 실행하지 않고, HTTP 응답이 사용자에게 전달된 이후 클로저들을 동시에 실행합니다.

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```