# 동시 실행 (Concurrency)

- [소개](#introduction)
- [동시 작업 실행하기](#running-concurrent-tasks)
- [동시 작업 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

때로는 서로 의존하지 않는 여러 느린 작업을 실행해야 할 때가 있습니다. 이런 경우, 작업들을 동시에 실행함으로써 성능을 크게 향상시킬 수 있습니다. Laravel의 `Concurrency` 파사드는 클로저를 동시에 실행할 수 있는 간편하고 편리한 API를 제공합니다.

<a name="how-it-works"></a>
#### 동작 원리

Laravel은 주어진 클로저를 직렬화하여 숨겨진 Artisan CLI 명령어로 전달한 후, 해당 명령어에서 클로저를 역직렬화하고 별도의 PHP 프로세스 내에서 실행하도록 하여 동시 실행을 구현합니다. 클로저가 실행된 후에는 결과 값을 다시 직렬화하여 부모 프로세스로 전달합니다.

`Concurrency` 파사드는 세 가지 드라이버를 지원합니다: 기본값인 `process`, `fork`, 그리고 `sync` 드라이버입니다.

`fork` 드라이버는 기본 `process` 드라이버보다 성능이 개선되지만, PHP가 웹 요청 동안 포킹을 지원하지 않기 때문에 CLI 환경 내에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 먼저 `spatie/fork` 패키지를 설치해야 합니다:

```shell
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트 시 유용하며, 모든 동시 실행을 비활성화하고 주어진 클로저들을 부모 프로세스 내에서 순차적으로 실행할 때 사용됩니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행하기

동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출하면 됩니다. `run` 메서드는 동시 실행할 클로저들의 배열을 인수로 받고, 각 클로저는 자식 PHP 프로세스에서 동시에 실행됩니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

특정 드라이버를 사용하려면 `driver` 메서드를 함께 사용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);
```

또는 기본 동시 실행 드라이버를 변경하려면, `config:publish` Artisan 명령어로 `concurrency` 설정 파일을 발행한 뒤, 파일 내 `default` 옵션을 수정하면 됩니다:

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연 실행하기

클로저 배열을 동시 실행하되, 작업 결과에 관심이 없는 경우 `defer` 메서드를 사용하는 것이 좋습니다. `defer` 메서드가 호출되면 클로저들이 즉시 실행되지 않고, HTTP 응답이 사용자에게 전달된 후에 동시 실행됩니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```