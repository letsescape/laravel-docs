# 목(mock) 처리 (Mocking)

- [소개](#introduction)
- [객체 목(mock) 처리](#mocking-objects)
- [파사드 목(mock) 처리](#mocking-facades)
    - [파사드 스파이(Spy)](#facade-spies)
- [시간 조작](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 테스트 중에 실제로 실행되지 않도록 특정 동작을 "목(mock)" 처리하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 경우 테스트 중에는 실제로 이벤트 리스너가 실행되지 않도록 목 처리할 수 있습니다. 이렇게 하면 이벤트 리스너의 실행을 신경 쓰지 않고 컨트롤러의 HTTP 응답만 테스트할 수 있으며, 이벤트 리스너 자체는 별도의 테스트 케이스에서 따로 테스트할 수 있습니다.

Laravel은 이벤트, 잡(jobs), 그 외 파사드(facade)들을 손쉽게 목 처리할 수 있는 다양한 헬퍼 메서드를 기본적으로 제공합니다. 이 헬퍼들은 Mockery 위에 편리함을 더한 래퍼로, 복잡한 Mockery 메서드 호출을 직접 작성할 필요 없이 쉽게 사용할 수 있도록 도와줍니다.

<a name="mocking-objects"></a>
## 객체 목(mock) 처리 (Mocking Objects)

Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 애플리케이션에 의존성 주입되는 객체를 목 처리할 때는, 해당 목 인스턴스를 `instance` 바인딩으로 컨테이너에 직접 바인딩해야 합니다. 이렇게 하면 Laravel 컨테이너가 객체를 직접 생성하는 대신, 바인딩된 목 인스턴스를 사용합니다:

```php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
});
```

```php tab=PHPUnit
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked(): void
{
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
}
```

이 과정을 더 편리하게 하기 위해, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래의 예시는 위 코드와 동일한 동작을 합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

만약 객체의 일부 메서드만 목 처리하고 싶다면 `partialMock` 메서드를 사용할 수 있습니다. 목 처리하지 않은 메서드는 호출 시 원래의 실제 구현대로 동작합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

또한, 객체를 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶을 때, Laravel의 기본 테스트 케이스 클래스에서 `Mockery::spy` 메서드를 감싸는 `spy` 메서드를 제공합니다. 스파이는 목과 비슷하지만, 코드와의 모든 상호작용을 기록해두었다가 코드 실행 이후에 원하는 어서션(assertion)을 할 수 있습니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 목(mock) 처리 (Mocking Facades)

전통적인 정적(static) 메서드 호출과 달리, [파사드(facade)](/docs/12.x/facades) (그리고 [실시간 파사드(real-time facade)](/docs/12.x/facades#real-time-facades))는 목 처리할 수 있습니다. 이로 인해 기존의 정적 메서드보다 훨씬 뛰어난 테스트 편의성을 제공하며, 전통적인 의존성 주입을 사용할 때와 마찬가지로 테스트가 용이해집니다. 실제로 컨트롤러 내에서 Laravel 파사드 호출이 이루어지는 경우, 테스트 시 파사드의 동작을 목 처리하고 싶을 때가 많습니다. 다음과 같은 컨트롤러 액션을 예로 들어보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Retrieve a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

`Cache` 파사드에 대한 호출을 목 처리하기 위해, `expects` 메서드를 사용할 수 있습니다. 이 메서드는 [Mockery](https://github.com/padraic/mockery) 목 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/12.x/container)에서 해결되고 관리되므로, 일반적인 정적 클래스보다 훨씬 더 높은 수준의 테스트 용이성을 가집니다. 예를 들어, 다음과 같이 `Cache` 파사드의 `get` 메서드 호출을 목 처리할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::expects('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/users');

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function test_get_index(): void
    {
        Cache::expects('get')
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}
```

> [!WARNING]
> `Request` 파사드는 목 처리하지 않는 것이 좋습니다. 대신, 테스트를 실행할 때 [HTTP 테스트 메서드](/docs/12.x/http-tests)인 `get`이나 `post` 등으로 원하는 입력을 전달하면 됩니다. `Config` 파사드 역시 목 처리하기보다는, 테스트 내에서 `Config::set` 메서드를 호출해 값을 지정하세요.

<a name="facade-spies"></a>
### 파사드 스파이(Spy)

파사드에 대해 [스파이(Spy)](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶을 경우, 해당 파사드에서 `spy` 메서드를 호출할 수 있습니다. 스파이는 목과 유사하지만, 테스트 코드 실행 도중의 모든 상호작용을 기록해두었다가 어서션에 활용할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
## 시간 조작 (Interacting With Time)

테스트를 진행하다 보면 `now` 또는 `Illuminate\Support\Carbon::now()` 등에서 반환되는 시간을 조작해야 할 때가 있습니다. 다행히, Laravel의 기본 기능 테스트 클래스에는 현재 시간을 자유롭게 조작할 수 있는 헬퍼들이 포함되어 있습니다:

```php tab=Pest
test('time can be manipulated', function () {
    // 미래로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 이동...
    $this->travel(-5)->hours();

    // 명시적 시간으로 이동...
    $this->travelTo(now()->minus(hours: 6));

    // 현재 시간으로 되돌아오기...
    $this->travelBack();
});
```

```php tab=PHPUnit
public function test_time_can_be_manipulated(): void
{
    // 미래로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 이동...
    $this->travel(-5)->hours();

    // 명시적 시간으로 이동...
    $this->travelTo(now()->minus(hours: 6));

    // 현재 시간으로 되돌아오기...
    $this->travelBack();
}
```

여러 시간 이동 메서드에는 클로저(Closure)를 전달할 수도 있습니다. 클로저 내부에서는 지정한 시점의 시간이 고정된 채로 실행되며, 클로저 실행이 끝나면 시간이 정상적으로 다시 흐릅니다:

```php
$this->travel(5)->days(function () {
    // 5일 뒤의 미래에서 무언가를 테스트...
});

$this->travelTo(now()->mins(days: 10), function () {
    // 특정 시점에서 무언가를 테스트...
});
```

현재 시간을 완전히 고정하려면 `freezeTime` 메서드를 사용할 수 있습니다. 비슷하게, `freezeSecond`는 현재 초 단위로 시간을 고정합니다:

```php
use Illuminate\Support\Carbon;

// 시간을 고정하고, 클로저 실행 후 정상 시간으로 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 초 단위로 시간을 고정하고, 클로저 실행 후 정상 시간으로 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

이런 메서드들은 주로 시간에 민감한 애플리케이션 동작(예: 포럼에서 비활성 포스트 자동 잠금) 등을 테스트할 때 효과적입니다:

```php tab=Pest
use App\Models\Thread;

test('forum threads lock after one week of inactivity', function () {
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    expect($thread->isLockedByInactivity())->toBeTrue();
});
```

```php tab=PHPUnit
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    $this->assertTrue($thread->isLockedByInactivity());
}
```