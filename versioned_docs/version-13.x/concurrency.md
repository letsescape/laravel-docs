<!-- # Concurrency -->
# Concurrency

- [Introduction](#introduction)
- [Running Concurrent Tasks](#running-concurrent-tasks)
    - [Named Results](#named-results)
    - [Task Timeouts](#task-timeouts)
- [Deferring Concurrent Tasks](#deferring-concurrent-tasks)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Sometimes you may need to execute several slow tasks which do not depend on one another. In many cases, significant performance improvements can be realized by executing the tasks concurrently. Laravel's `Concurrency` facade provides a simple, convenient API for executing closures concurrently. -->
때로는 서로 의존하지 않는 여러 느린 작업을 실행해야 할 때가 있습니다. 이런 경우, 작업들을 동시에 실행함으로써 성능을 크게 향상시킬 수 있습니다. Laravel의 `Concurrency` 파사드는 클로저를 동시에 실행할 수 있는 간편하고 편리한 API를 제공합니다.

<a name="how-it-works"></a>
<!-- #### How it Works -->
#### How it Works

<!-- Laravel achieves concurrency by serializing the given closures and dispatching them to a hidden Artisan CLI command, which unserializes the closures and invokes it within its own PHP process. After the closure has been invoked, the resulting value is serialized back to the parent process. -->
Laravel은 주어진 클로저를 직렬화하여 숨겨진 Artisan CLI 명령어로 전달한 후, 해당 명령어에서 클로저를 역직렬화하고 별도의 PHP 프로세스 내에서 실행하도록 하여 동시 실행을 구현합니다. 클로저가 실행된 후에는 결과 값을 다시 직렬화하여 부모 프로세스로 전달합니다.

<!-- The `Concurrency` facade supports three drivers: `process` (the default), `fork`, and `sync`. -->
`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, `fork`, 그리고 `sync` 드라이버입니다.

<!-- The `fork` driver offers improved performance compared to the default `process` driver, but it may only be used within PHP's CLI context, as PHP does not support forking during web requests. Before using the `fork` driver, you need to install the `spatie/fork` package: -->
`fork` 드라이버는 기본 `process` 드라이버보다 성능이 개선되지만, PHP가 웹 요청 동안 포킹을 지원하지 않기 때문에 CLI 환경 내에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 먼저 `spatie/fork` 패키지를 설치해야 합니다:

```shell
composer require spatie/fork
```

<!-- The `sync` driver is primarily useful during testing when you want to disable all concurrency and simply execute the given closures in sequence within the parent process. -->
`sync` 드라이버는 주로 테스트 시 유용하며, 모든 동시 실행을 비활성화하고 주어진 클로저들을 부모 프로세스 내에서 순차적으로 실행할 때 사용됩니다.

<a name="running-concurrent-tasks"></a>
<!-- ## Running Concurrent Tasks -->
## Running Concurrent Tasks

<!-- To run concurrent tasks, you may invoke the `Concurrency` facade's `run` method. The `run` method accepts an array of closures which should be executed simultaneously in child PHP processes: -->
동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하면 됩니다. `run` 메서드는 동시 실행할 클로저들의 배열을 인수로 받고, 각 클로저는 자식 PHP 프로세스에서 동시에 실행됩니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

<!-- To use a specific driver, you may use the `driver` method: -->
특정 드라이버를 사용하려면 `driver` 메서드를 함께 사용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

<!-- Or, to change the default concurrency driver, you should publish the `concurrency` configuration file via the `config:publish` Artisan command and update the `default` option within the file: -->
또는 기본 동시 실행 드라이버를 변경하려면, `config:publish` Artisan 명령어로 `concurrency` 설정 파일을 발행한 뒤, 파일 내 `default` 옵션을 수정하면 됩니다:

```shell
php artisan config:publish concurrency
```

<a name="named-results"></a>
<!-- ### Named Results -->
### Named Results

<!-- If you would like to access concurrent task results by name rather than by position, you may provide an associative array of closures. Each result will be returned using the same key as its corresponding closure: -->
동시 작업 결과를 위치가 아니라 이름으로 접근하고 싶다면 클로저의 연관 배열을 제공할 수 있습니다. 각 결과는 해당 클로저와 동일한 키를 사용하여 반환됩니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

$results = Concurrency::run([
    'users' => fn () => DB::table('users')->count(),
    'orders' => fn () => DB::table('orders')->count(),
]);

$userCount = $results['users'];
$orderCount = $results['orders'];
```

<a name="task-timeouts"></a>
<!-- ### Task Timeouts -->
### Task Timeouts

<!-- When using the `process` driver (the default), you may specify a maximum number of seconds a concurrent task is allowed to run before it is terminated by providing a timeout to the `run` method: -->
`process` 드라이버(기본값)를 사용할 때는 `run` 메서드에 timeout을 전달하여, 동시 작업이 종료되기 전에 실행될 수 있는 최대 초 수를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);
```

<!-- You may also provide a `CarbonInterval` instance if you prefer a more expressive timeout definition: -->
시간 제한을 더 명확하게 표현하고 싶다면 `CarbonInterval` 인스턴스를 전달할 수도 있습니다:

```php
use Illuminate\Support\Facades\Concurrency;

use function Illuminate\Support\seconds;

Concurrency::run([...], timeout: seconds(30));
```

<a name="deferring-concurrent-tasks"></a>
<!-- ## Deferring Concurrent Tasks -->
## Deferring Concurrent Tasks

<!-- If you would like to execute an array of closures concurrently, but are not interested in the results returned by those closures, you should consider using the `defer` method. When the `defer` method is invoked, the given closures are not executed immediately. Instead, Laravel will execute the closures concurrently after the HTTP response has been sent to the user: -->
클로저 배열을 동시 실행하되, 작업 결과에 관심이 없는 경우 `defer` 메서드를 사용하는 것이 좋습니다. `defer` 메서드가 호출되면 클로저들이 즉시 실행되지 않고, HTTP 응답이 사용자에게 전달된 후에 동시 실행됩니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```
