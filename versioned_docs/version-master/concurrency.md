# 동시성 (Concurrency)

- [소개](#introduction)
- [동시 작업 실행하기](#running-concurrent-tasks)
- [동시 작업 지연 실행하기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개 (Introduction)

여러 개의 느린 작업이 서로 의존하지 않는 경우, 이 작업들을 동시에 실행하면 성능을 크게 개선할 수 있습니다. Laravel의 `Concurrency` 파사드(facade)는 클로저를 동시에 실행할 수 있는 간단하고 편리한 API를 제공합니다.

<a name="how-it-works"></a>
#### 동작 방식

Laravel은 전달받은 클로저를 직렬화하여 숨겨진 Artisan CLI 명령어로 전달합니다. 해당 명령어는 해당 클로저를 역직렬화한 뒤 자체 PHP 프로세스에서 실행합니다. 클로저가 실행된 후에는, 반환된 값을 부모 프로세스로 다시 직렬화하여 돌려줍니다.

`Concurrency` 파사드는 기본값인 `process`를 비롯해 `fork`, `sync` 총 세 가지 드라이버(driver)를 지원합니다.

`fork` 드라이버는 기본값인 `process` 드라이버에 비해 더 나은 성능을 제공하지만, PHP 웹 요청 도중에는 포킹(fork)을 지원하지 않으므로 PHP의 CLI 환경에서만 사용할 수 있습니다. `fork` 드라이버를 사용하려면 먼저 `spatie/fork` 패키지를 설치해야 합니다.

```shell
composer require spatie/fork
```

`sync` 드라이버는 주로 테스트 환경에서 동시성을 끄고, 주어진 클로저들을 부모 프로세스에서 순차적으로 실행할 때 사용됩니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행하기 (Running Concurrent Tasks)

동시 작업을 실행하려면 `Concurrency` 파사드의 `run` 메서드를 호출할 수 있습니다. `run` 메서드는 동시에 자식 PHP 프로세스들에서 실행되어야 하는 클로저 배열을 인수로 받습니다.

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);
```

특정 드라이버를 사용하려면, `driver` 메서드를 사용할 수 있습니다.

```php
$results = Concurrency::driver('fork')->run(...);
```

또는 기본 동시성 드라이버를 변경하려면, `config:publish` Artisan 명령어를 통해 `concurrency` 설정 파일을 공개(publish)하고, 파일 내의 `default` 옵션을 수정해야 합니다.

```shell
php artisan config:publish concurrency
```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연 실행하기 (Deferring Concurrent Tasks)

클로저들의 실행 결과에는 관심이 없지만, 여러 클로저를 동시에 실행하고 싶은 경우에는 `defer` 메서드를 사용하는 것이 좋습니다. `defer` 메서드는 주어진 클로저들을 즉시 실행하지 않습니다. 대신, HTTP 응답이 사용자에게 전송된 이후에 클로저들이 동시에 실행됩니다.

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);
```