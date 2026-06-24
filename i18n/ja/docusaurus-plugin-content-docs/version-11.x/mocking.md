<!-- # Mocking -->
# Mocking

- [Introduction](#introduction)
- [Mocking Objects](#mocking-objects)
- [Mocking Facades](#mocking-facades)
    - [Facade Spies](#facade-spies)
- [Interacting With Time](#interacting-with-time)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When testing Laravel applications, you may wish to "mock" certain aspects of your application so they are not actually executed during a given test. For example, when testing a controller that dispatches an event, you may wish to mock the event listeners so they are not actually executed during the test. This allows you to only test the controller's HTTP response without worrying about the execution of the event listeners since the event listeners can be tested in their own test case. -->
Laravel アプリケーションをテストするとき、アプリケーションの特定の側面を「モック」して、特定のテスト中に実際には実行されないようにしたい場合があります。たとえば、イベントを送出するコントローラをテストする場合、イベント リスナをモックして、テスト中にイベント リスナが実際に実行されないようにすることができます。これにより、イベント リスナは独自のテスト ケースでテストできるため、イベント リスナの実行を気にせずにコントローラの HTTP 応答のみをテストできます。

<!-- Laravel provides helpful methods for mocking events, jobs, and other facades out of the box. These helpers primarily provide a convenience layer over Mockery so you do not have to manually make complicated Mockery method calls. -->
Laravel は、イベント、ジョブ、その他のファサードをすぐにモックするための便利なメソッドを提供します。これらのヘルパは主に Mockery 上の便利なレイヤーを提供するため、複雑な Mockery メソッド呼び出しを手動で行う必要はありません。

<a name="mocking-objects"></a>
<!-- ## Mocking Objects -->
## Mocking Objects

<!-- When mocking an object that is going to be injected into your application via Laravel's [service container](/docs/11.x/container), you will need to bind your mocked instance into the container as an `instance` binding. This will instruct the container to use your mocked instance of the object instead of constructing the object itself: -->
Laravel の [service container](/docs/11.x/container) 経由でアプリケーションに挿入されるオブジェクトをモックする場合、モックされたインスタンスを `instance` バインディングとしてコンテナにバインドする必要があります。これにより、オブジェクト自体を構築する代わりに、オブジェクトのモックされたインスタンスを使用するようにコンテナーに指示されます。

```php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->shouldReceive('process')->once();
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
            $mock->shouldReceive('process')->once();
        })
    );
}
```

<!-- In order to make this more convenient, you may use the `mock` method that is provided by Laravel's base test case class. For example, the following example is equivalent to the example above: -->
これをより便利にするために、Laravel の基本テスト ケース クラスによって提供される `mock` メソッドを使用できます。たとえば、次の例は上記の例と同等です。

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- You may use the `partialMock` method when you only need to mock a few methods of an object. The methods that are not mocked will be executed normally when called: -->
オブジェクトのいくつかのメソッドのみをモックする必要がある場合は、`partialMock` メソッドを使用できます。モック化されていないメソッドは、呼び出されたときに通常どおり実行されます。

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- Similarly, if you want to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on an object, Laravel's base test case class offers a `spy` method as a convenient wrapper around the `Mockery::spy` method. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
同様に、オブジェクトに対して [spy](http://docs.mockery.io/en/latest/reference/spies.html) を実行したい場合、Laravel の基本テスト ケース クラスは、`Mockery::spy` メソッドの便利なラッパーとして `spy` メソッドを提供します。スパイはモックに似ています。ただし、スパイはスパイとテスト対象のコード間のやり取りを記録するため、コードの実行後にアサーションを行うことができます。

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
<!-- ## Mocking Facades -->
## Mocking Facades

<!-- Unlike traditional static method calls, [facades](/docs/11.x/facades) (including [real-time facades](/docs/11.x/facades#real-time-facades)) may be mocked. This provides a great advantage over traditional static methods and grants you the same testability that you would have if you were using traditional dependency injection. When testing, you may often want to mock a call to a Laravel facade that occurs in one of your controllers. For example, consider the following controller action: -->
従来の静的メソッド呼び出しとは異なり、[facades](/docs/11.x/facades) ([real-time facades](/docs/11.x/facades#real-time-facades) を含む) はモックされる可能性があります。これにより、従来の静的メソッドに比べて大きな利点が得られ、従来の依存注入を使用した場合と同じテスト容易性が得られます。テストする場合、コントローラの 1 つで発生する Laravel ファサードへの呼び出しをモックしたい場合があります。たとえば、次のコントローラ アクションを考えてみましょう。

```
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

<!-- We can mock the call to the `Cache` facade by using the `shouldReceive` method, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock. Since facades are actually resolved and managed by the Laravel [service container](/docs/11.x/container), they have much more testability than a typical static class. For example, let's mock our call to the `Cache` facade's `get` method: -->
`shouldReceive` メソッドを使用して、`Cache` ファサードへの呼び出しをモックできます。このメソッドは、[Mockery](https://github.com/padraic/mockery) モックのインスタンスを返します。ファサードは実際には Laravel [service container](/docs/11.x/container) によって解決および管理されるため、一般的な静的クラスよりもはるかにテストしやすくなっています。たとえば、`Cache` ファサードの `get` メソッドへの呼び出しをモックしてみましょう。

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::shouldReceive('get')
        ->once()
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
        Cache::shouldReceive('get')
            ->once()
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}
```

> [!WARNING]
> `Request` ファサードをモックしないでください。代わりに、テストを実行するときに、`get` や `post` などの必要な入力を [HTTP testing methods](/docs/11.x/http-tests) に渡します。同様に、`Config` ファサードをモックする代わりに、テストで `Config::set` メソッドを呼び出します。

<a name="facade-spies"></a>
<!-- ### Facade Spies -->
### Facade Spies

<!-- If you would like to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on a facade, you may call the `spy` method on the corresponding facade. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
ファサードで [spy](http://docs.mockery.io/en/latest/reference/spies.html) を実行したい場合は、対応するファサードで `spy` メソッドを呼び出すことができます。スパイはモックに似ています。ただし、スパイはスパイとテスト対象のコード間のやり取りを記録するため、コードの実行後にアサーションを行うことができます。

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are be stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_be_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
<!-- ## Interacting With Time -->
## Interacting With Time

<!-- When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Thankfully, Laravel's base feature test class includes helpers that allow you to manipulate the current time: -->
テスト時に、`now` や `Illuminate\Support\Carbon::now()` などのヘルパによって返される時間を変更する必要がある場合があります。ありがたいことに、Laravel の基本機能テスト クラスには、現在時刻を操作できるヘルパが含まれています。

```php tab=Pest
test('time can be manipulated', function () {
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->subHours(6));

    // Return back to the present time...
    $this->travelBack();
});
```

```php tab=PHPUnit
public function test_time_can_be_manipulated(): void
{
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->subHours(6));

    // Return back to the present time...
    $this->travelBack();
}
```

<!-- You may also provide a closure to the various time travel methods. The closure will be invoked with time frozen at the specified time. Once the closure has executed, time will resume as normal: -->
さまざまなタイムトラベル方法にクロージャを提供することもできます。クロージャは、指定された時刻に時間を凍結して呼び出されます。クロージャーが実行されると、時間は通常どおりに再開されます。

```
$this->travel(5)->days(function () {
    // Test something five days into the future...
});

$this->travelTo(now()->subDays(10), function () {
    // Test something during a given moment...
});
```

<!-- The `freezeTime` method may be used to freeze the current time. Similarly, the `freezeSecond` method will freeze the current time but at the start of the current second: -->
`freezeTime` メソッドを使用して、現在時刻を固定することができます。同様に、`freezeSecond` メソッドは現在時刻をフリーズしますが、現在の秒の始まりをフリーズします。

```
use Illuminate\Support\Carbon;

// Freeze time and resume normal time after executing closure...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// Freeze time at the current second and resume normal time after executing closure...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

<!-- As you would expect, all of the methods discussed above are primarily useful for testing time sensitive application behavior, such as locking inactive posts on a discussion forum: -->
ご想像のとおり、上記で説明した方法はすべて、ディスカッション フォーラムの非アクティブな投稿をロックするなど、時間に敏感なアプリケーションの動作をテストするのに主に役立ちます。

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

