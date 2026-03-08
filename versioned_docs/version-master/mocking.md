# 모킹 (Mocking)

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간과의 상호작용](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 특정 기능이 실제로 실행되지 않도록 "모킹(mock)"하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치(dispatch)하는 컨트롤러를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 모킹할 수 있습니다. 이를 통해 이벤트 리스너의 동작을 신경 쓰지 않고 컨트롤러의 HTTP 응답만을 테스트할 수 있으며, 이벤트 리스너는 별도의 테스트 케이스에서 검증할 수 있습니다.

Laravel은 이벤트, 작업(job), 기타 파사드(facade)를 기본적으로 쉽게 모킹할 수 있는 다양한 메서드를 제공합니다. 이러한 도우미는 주로 Mockery 위에 편의 기능을 덧씌운 것이므로, 복잡한 Mockery 호출을 직접 작성하지 않아도 됩니다.

<a name="mocking-objects"></a>
## 객체 모킹 (Mocking Objects)

Laravel의 [서비스 컨테이너](/docs/master/container)를 통해 애플리케이션에 주입되는 객체를 모킹하려면, 모킹한 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 해당 객체를 직접 생성하는 대신, 여러분이 모킹한 인스턴스를 사용하게 됩니다.

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

이를 더 편리하게 사용하려면, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예시는 위와 동일한 동작을 합니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

객체의 일부 메서드만 모킹하고 싶을 때는 `partialMock` 메서드를 사용할 수 있습니다. 모킹하지 않은 메서드는 호출 시 정상적으로 동작합니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

또한, 객체에 대해 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)를 적용하고 싶다면, Laravel의 기본 테스트 케이스 클래스에서 `Mockery::spy`를 감싼 `spy` 메서드를 사용할 수 있습니다. 스파이는 모킹과 유사하지만, 스파이는 테스트 중 객체와 코드 간의 모든 상호작용을 기록하여, 코드 실행 후에도 상호작용 여부를 검증할 수 있도록 해줍니다.

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹 (Mocking Facades)

전통적인 정적(static) 메서드 호출과 달리, [파사드(facade)](/docs/master/facades) (및 [실시간 파사드](/docs/master/facades#real-time-facades))는 모킹이 가능합니다. 이는 전통적인 정적 메서드와 비교해 큰 장점으로, 의존성 주입을 사용하는 것과 같은 수준의 테스트 용이성을 제공합니다. 테스트 시, 컨트롤러에서 발생하는 특정 Laravel 파사드 호출을 모킹하는 사례가 많습니다. 예를 들어, 다음과 같은 컨트롤러 액션을 생각해보겠습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 조회합니다.
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

`Cache` 파사드 호출은 `expects` 메서드를 사용해 모킹할 수 있습니다. 이는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/master/container)에 의해 해석되고 관리되기 때문에 일반적인 정적 클래스보다 테스트 용이성이 훨씬 뛰어납니다. 아래는 `Cache` 파사드의 `get` 메서드 호출을 모킹하는 예시입니다.

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
> `Request` 파사드는 모킹하지 않아야 합니다. 대신, 테스트를 실행할 때 원하는 입력값을 [HTTP 테스트 메서드](/docs/master/http-tests)인 `get`이나 `post` 등에 인자로 전달하세요. 마찬가지로, `Config` 파사드도 모킹하지 말고, 테스트 내에서 직접 `Config::set` 메서드를 호출하여 값을 설정하세요.

<a name="facade-spies"></a>
### 파사드 스파이 (Facade Spies)

파사드에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 적용하고 싶다면, 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 유사하지만, 테스트 중 해당 파사드와 코드 간의 모든 상호작용을 기록하여 코드 실행 후에 검증할 수 있습니다.

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
## 시간과의 상호작용 (Interacting With Time)

테스트를 진행하면서 `now`나 `Illuminate\Support\Carbon::now()`와 같은 도우미가 반환하는 시간을 조작해야 할 때가 있습니다. 다행히도, Laravel의 기본 기능 테스트 클래스는 현재 시간을 마음대로 조작할 수 있도록 돕는 유틸리티를 포함하고 있습니다.

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

    // 명시적인 특정 시점으로 이동...
    $this->travelTo(now()->minus(hours: 6));

    // 현재 시점으로 복귀...
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

    // 명시적인 특정 시점으로 이동...
    $this->travelTo(now()->minus(hours: 6));

    // 현재 시점으로 복귀...
    $this->travelBack();
}
```

또한, 다양한 시간 이동(travel) 메서드에 클로저를 전달할 수 있습니다. 이 경우 해당 시간으로 시간이 고정된 상태에서 클로저가 실행되고, 클로저가 끝나면 시간이 원래대로 돌아옵니다.

```php
$this->travel(5)->days(function () {
    // 미래 5일 후의 상황을 테스트...
});

$this->travelTo(now()->mins(days: 10), function () {
    // 특정 순간의 동작을 테스트...
});
```

현재 시간을 고정(freeze)하려면 `freezeTime` 메서드를 사용할 수 있습니다. 마찬가지로, 현재 초(second) 단위에서 시간을 고정하려면 `freezeSecond` 메서드를 사용합니다.

```php
use Illuminate\Support\Carbon;

// 시간을 고정한 후 클로저 실행이 끝나면 원래 시간으로 돌아감...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초에서 시간을 고정한 후, 클로저 실행이 끝나면 원래 시간으로 돌아감...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

설명한 방식들은 주로 시간에 민감한 애플리케이션 동작(예: 포럼에서 일정 기간 비활성 상태인 글을 자동으로 잠그는 기능) 테스트에 유용하게 사용됩니다.

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