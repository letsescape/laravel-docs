<!-- # Mocking -->
# Mocking

- [Introduction](#introduction)
- [Mocking Objects](#mocking-objects)
- [Mocking Facades](#mocking-facades)
    - [Facade Spies](#facade-spies)
- [Bus Fake](#bus-fake)
    - [Job Chains](#bus-job-chains)
    - [Job Batches](#job-batches)
- [Event Fake](#event-fake)
    - [Scoped Event Fakes](#scoped-event-fakes)
- [HTTP Fake](#http-fake)
- [Mail Fake](#mail-fake)
- [Notification Fake](#notification-fake)
- [Queue Fake](#queue-fake)
    - [Job Chains](#job-chains)
- [Storage Fake](#storage-fake)
- [Interacting With Time](#interacting-with-time)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When testing Laravel applications, you may wish to "mock" certain aspects of your application so they are not actually executed during a given test. For example, when testing a controller that dispatches an event, you may wish to mock the event listeners so they are not actually executed during the test. This allows you to only test the controller's HTTP response without worrying about the execution of the event listeners since the event listeners can be tested in their own test case. -->
Laravel 애플리케이션을 테스트할 때, 실제로 실행되면 안 되는 애플리케이션의 특정 부분을 "모킹"하고 싶을 수 있습니다. 예를 들어 이벤트를 디스패치(dispatch)하는 컨트롤러를 테스트할 때, 테스트 중 이벤트 리스너가 실제로 실행되지 않길 원할 수 있습니다. 이렇게 하면 이벤트 리스너의 동작은 별도 테스트 케이스에서 검증하고, 이 테스트에서는 오직 컨트롤러의 HTTP 응답만 집중해서 테스트할 수 있습니다.

<!-- Laravel provides helpful methods for mocking events, jobs, and other facades out of the box. These helpers primarily provide a convenience layer over Mockery so you do not have to manually make complicated Mockery method calls. -->
Laravel은 기본적으로 이벤트, 잡, 다양한 파사드의 모킹을 위한 많은 편의 메서드를 제공합니다. 이러한 헬퍼들은 복잡한 Mockery 호출을 직접 작성할 필요 없이, Mockery 위에서 동작하는 간결한 인터페이스를 제공합니다.

<a name="mocking-objects"></a>
<!-- ## Mocking Objects -->
## Mocking Objects

<!-- When mocking an object that is going to be injected into your application via Laravel's [service container](/docs/9.x/container), you will need to bind your mocked instance into the container as an `instance` binding. This will instruct the container to use your mocked instance of the object instead of constructing the object itself: -->
Laravel의 [service container](/docs/9.x/container)를 통해 애플리케이션에 주입될 객체를 모킹하려면, 모킹된 인스턴스를 `instance` 바인딩 형태로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너는 직접 객체를 생성하지 않고, 대신 여러분이 준비한 모킹 인스턴스를 사용하게 됩니다.

```
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked()
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
보다 간편하게 사용하려면, Laravel의 기본 테스트 케이스 클래스가 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예시는 위 코드와 동일한 효과를 냅니다.

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- You may use the `partialMock` method when you only need to mock a few methods of an object. The methods that are not mocked will be executed normally when called: -->
특정 메서드만 모킹(=일부 메서드만 대체)하고, 나머지는 실제로 동작하게 하고 싶다면 `partialMock` 메서드를 사용하세요. 모킹하지 않은 메서드는 평소처럼 동작합니다.

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- Similarly, if you want to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on an object, Laravel's base test case class offers a `spy` method as a convenient wrapper around the `Mockery::spy` method. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
또한 [spy](http://docs.mockery.io/en/latest/reference/spies.html) 기능이 필요한 경우, Laravel의 기본 테스트 케이스 클래스가 `Mockery::spy` 메서드를 편리하게 감싸는 `spy` 메서드도 제공합니다. 스파이는 모킹과 비슷하지만, 코드 실행 도중 해당 객체가 어떻게 활용되었는지(호출 여부·인자 등)를 기록하여, 이후에 assert(검증)를 할 수 있습니다.

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
<!-- ## Mocking Facades -->
## Mocking Facades

<!-- Unlike traditional static method calls, [facades](/docs/9.x/facades) (including [real-time facades](/docs/9.x/facades#real-time-facades)) may be mocked. This provides a great advantage over traditional static methods and grants you the same testability that you would have if you were using traditional dependency injection. When testing, you may often want to mock a call to a Laravel facade that occurs in one of your controllers. For example, consider the following controller action: -->
기존의 정적(static) 메서드 호출과 달리, [facades](/docs/9.x/facades) (그리고 [real-time facades](/docs/9.x/facades#real-time-facades))는 모킹이 가능합니다. 이는 기존의 정적 메서드 기반 접근 방식보다 테스트 측면에서 큰 장점이 있으며, 마치 의존성 주입(DI)으로 객체를 사용하는 것과 동일한 수준의 테스트 용이성을 제공합니다. 컨트롤러에서 발생하는 파사드 호출을 테스트할 때도 매우 유용합니다. 다음 컨트롤러 예제를 보겠습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Retrieve a list of all users of the application.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $value = Cache::get('key');

        //
    }
}
```

<!-- We can mock the call to the `Cache` facade by using the `shouldReceive` method, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock. Since facades are actually resolved and managed by the Laravel [service container](/docs/9.x/container), they have much more testability than a typical static class. For example, let's mock our call to the `Cache` facade's `get` method: -->
`shouldReceive` 메서드를 사용해 `Cache` 파사드의 메서드 호출을 모킹할 수 있습니다. 이는 [Mockery](https://github.com/padraic/mockery)의 mock 인스턴스를 반환합니다. 파사드는 실제로 Laravel의 [service container](/docs/9.x/container)를 통해 해결되고 관리되므로, 일반적인 정적 클래스보다 훨씬 테스트하기 쉽습니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 다음과 같이 모킹할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function testGetIndex()
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
> `Request` 파사드는 모킹하지 않는 것이 좋습니다. 대신, HTTP 테스트 실행 시 `get`, `post` 등 [HTTP testing methods](/docs/9.x/http-tests)에 원하는 입력값을 전달하세요. 마찬가지로, `Config` 파사드도 모킹하는 대신, 테스트 내에서 직접 `Config::set` 메서드를 사용해 값을 설정해야 합니다.

<a name="facade-spies"></a>
<!-- ### Facade Spies -->
### Facade Spies

<!-- If you would like to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on a facade, you may call the `spy` method on the corresponding facade. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
[spy](http://docs.mockery.io/en/latest/reference/spies.html) 기능을 파사드에 적용하고 싶다면, 해당 파사드의 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 비슷하지만, 코드 실행 중 해당 파사드가 어떤 식으로 호출되었는지 기록하며, 실행 이후 다양한 검증이 가능합니다.

```
use Illuminate\Support\Facades\Cache;

public function test_values_are_be_stored_in_cache()
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
}
```

<a name="bus-fake"></a>
<!-- ## Bus Fake -->
## Bus Fake

<!-- When testing code that dispatches jobs, you typically want to assert that a given job was dispatched but not actually queue or execute the job. This is because the job's execution can normally be tested in a separate test class. -->
잡(jobs)을 디스패치(dispatch)하는 코드를 테스트할 때, 해당 잡이 실제로 큐에 올라가거나 실행되지 않고, 디스패치 여부만 검증하면 충분한 경우가 많습니다. 잡 자체의 동작은 별도의 테스트 클래스에서 검증하는 것이 일반적입니다.

<!-- You may use the `Bus` facade's `fake` method to prevent jobs from being dispatched to the queue. Then, after executing the code under test, you may inspect which jobs the application attempted to dispatch using the `assertDispatched` and `assertNotDispatched` methods: -->
`Bus` 파사드의 `fake` 메서드를 사용하면 잡이 실제로 큐에 디스패치되는 것을 방지할 수 있습니다. 그리고 테스트 실행 후, `assertDispatched`, `assertNotDispatched` 등의 메서드로 어떤 잡이 디스패치되었는지 검증할 수 있습니다.

```
<?php

namespace Tests\Feature;

use App\Jobs\ShipOrder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Bus;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Bus::fake();

        // Perform order shipping...

        // Assert that a job was dispatched...
        Bus::assertDispatched(ShipOrder::class);

        // Assert a job was not dispatched...
        Bus::assertNotDispatched(AnotherJob::class);

        // Assert that a job was dispatched synchronously...
        Bus::assertDispatchedSync(AnotherJob::class);

        // Assert that a job was not dispatched synchronously...
        Bus::assertNotDispatchedSync(AnotherJob::class);

        // Assert that a job was dispatched after the response was sent...
        Bus::assertDispatchedAfterResponse(AnotherJob::class);

        // Assert a job was not dispatched after response was sent...
        Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

        // Assert no jobs were dispatched...
        Bus::assertNothingDispatched();
    }
}
```

<!-- You may pass a closure to the available methods in order to assert that a job was dispatched that passes a given "truth test". If at least one job was dispatched that passes the given truth test then the assertion will be successful. For example, you may wish to assert that a job was dispatched for a specific order: -->
이러한 메서드들에는 클로저를 전달할 수도 있어, "진리 검사(truth test)"를 통과하는 조건의 잡이 최소 1개라도 디스패치되었는지 검증할 수 있습니다. 예를 들어, 특정 주문에 대해 잡이 디스패치되었는지 확인하려면 다음과 같이 할 수 있습니다.

```
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
<!-- #### Faking A Subset Of Jobs -->
#### Faking A Subset Of Jobs

<!-- If you only want to prevent certain jobs from being dispatched, you may pass the jobs that should be faked to the `fake` method: -->
모든 잡이 아니라, 특정 잡만 디스패치되지 않게 하고 싶다면, 페이크할 잡들의 클래스명을 `fake` 메서드에 배열로 전달하세요.

```
/**
 * Test order process.
 */
public function test_orders_can_be_shipped()
{
    Bus::fake([
        ShipOrder::class,
    ]);

    // ...
}
```

<!-- You may fake all jobs except for a set of specified jobs using the `except` method: -->
반대로 특정 잡만 실제로 디스패치되게 하고 나머지는 모두 페이크로 대체하려면, `except` 메서드를 사용할 수 있습니다.

```
Bus::fake()->except([
    ShipOrder::class,
]);
```

<a name="bus-job-chains"></a>
<!-- ### Job Chains -->
### Job Chains

<!-- The `Bus` facade's `assertChained` method may be used to assert that a [chain of jobs](/docs/9.x/queues#job-chaining) was dispatched. The `assertChained` method accepts an array of chained jobs as its first argument: -->
`Bus` 파사드의 `assertChained` 메서드를 사용하면, [chain of jobs](/docs/9.x/queues#job-chaining)이 정상적으로 디스패치되었는지 검증할 수 있습니다. `assertChained`는 체이닝된 잡들의 배열을 첫 인자로 받습니다.

```
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```

<!-- As you can see in the example above, the array of chained jobs may be an array of the job's class names. However, you may also provide an array of actual job instances. When doing so, Laravel will ensure that the job instances are of the same class and have the same property values of the chained jobs dispatched by your application: -->
위 예제처럼, 체이닝된 잡의 배열에는 클래스명만 나열할 수도 있지만, 실제 잡 인스턴스 배열을 전달할 수도 있습니다. 이 경우, Laravel은 각 인스턴스의 클래스와 속성 값이 애플리케이션에서 디스패치된 잡과 일치하는지 확인해줍니다.

```
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<a name="job-batches"></a>
<!-- ### Job Batches -->
### Job Batches

<!-- The `Bus` facade's `assertBatched` method may be used to assert that a [batch of jobs](/docs/9.x/queues#job-batching) was dispatched. The closure given to the `assertBatched` method receives an instance of `Illuminate\Bus\PendingBatch`, which may be used to inspect the jobs within the batch: -->
`Bus` 파사드의 `assertBatched` 메서드를 사용하면, [batch of jobs](/docs/9.x/queues#job-batching)가 정상적으로 디스패치되었는지 검증할 수 있습니다. `assertBatched` 메서드에 넘기는 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 전달되어, 배치에 포함된 잡들을 검사할 수 있습니다.

```
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="testing-job-batch-interaction"></a>
<!-- #### Testing Job / Batch Interaction -->
#### Testing Job / Batch Interaction

<!-- In addition, you may occasionally need to test an individual job's interaction with its underlying batch. For example, you may need to test if a job cancelled further processing for its batch. To accomplish this, you need to assign a fake batch to the job via the `withFakeBatch` method. The `withFakeBatch` method returns a tuple containing the job instance and the fake batch: -->
잡이 자신이 속한 배치와 상호작용하는 동작을 테스트해야 할 때가 있습니다. 예를 들어, 잡이 실행 도중 배치 처리 자체를 취소하는지 테스트하고 싶을 수 있습니다. 이때는 `withFakeBatch` 메서드를 사용해 잡에 페이크 배치를 할당해야 합니다. `withFakeBatch` 메서드는 잡 인스턴스와 페이크 배치를 담은 튜플을 반환합니다.

```
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="event-fake"></a>
<!-- ## Event Fake -->
## Event Fake

<!-- When testing code that dispatches events, you may wish to instruct Laravel to not actually execute the event's listeners. Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods: -->
이벤트를 디스패치하는 코드를 테스트할 때, 이벤트의 리스너가 실제로 실행되지 않도록 하고 싶을 수 있습니다. `Event` 파사드의 `fake` 메서드를 이용하면 리스너 실행을 막을 수 있고, 테스트가 실행된 후 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등으로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다.

```
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order shipping.
     */
    public function test_orders_can_be_shipped()
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

<!-- You may pass a closure to the `assertDispatched` or `assertNotDispatched` methods in order to assert that an event was dispatched that passes a given "truth test". If at least one event was dispatched that passes the given truth test then the assertion will be successful: -->
`assertDispatched`, `assertNotDispatched`에 클로저를 넘겨 "진리 검사"를 통과하는 이벤트가 디스패치되었는지 검증할 수 있습니다. 아래는 예시입니다.

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

<!-- If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method: -->
특정 이벤트에 대해 리스너가 실제로 연결되어 있는지 검증하려면 `assertListening` 메서드를 사용할 수 있습니다.

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면, 한 번도 이벤트 리스너가 실행되지 않습니다. 따라서 모델의 이벤트(예: `creating` 이벤트에서 UUID 생성 등)에 의존하는 팩토리를 사용하는 테스트라면, 팩토리 실행 **이후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
<!-- #### Faking A Subset Of Events -->
#### Faking A Subset Of Events

<!-- If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method: -->
특정 이벤트 리스너만 페이크 처리하고 싶다면, 그 이벤트들을 `fake` 또는 `fakeFor` 메서드에 배열로 전달하면 됩니다.

```
/**
 * Test order process.
 */
public function test_orders_can_be_processed()
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([...]);
}
```

<!-- You may fake all events except for a set of specified events using the `except` method: -->
반대로, 특정 이벤트만 실제 동작하게 하고 나머지는 모두 페이크 처리하고 싶다면, `except` 메서드를 사용하세요.

```
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
<!-- ### Scoped Event Fakes -->
### Scoped Event Fakes

<!-- If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method: -->
테스트의 특정 구간에서만 이벤트 리스너 페이크 기능을 적용하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다.

```
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order process.
     */
    public function test_orders_can_be_processed()
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run ...
        $order->update([...]);
    }
}
```

<a name="http-fake"></a>
<!-- ## HTTP Fake -->
## HTTP Fake

<!-- The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. For more information on faking outgoing HTTP requests, please consult the [HTTP Client testing documentation](/docs/9.x/http-client#testing). -->
`Http` 파사드의 `fake` 메서드를 이용하면, HTTP 클라이언트 사용 시 실제 요청이 아닌 더미/스텁 응답을 반환하도록 설정할 수 있습니다. 외부 HTTP 요청을 모킹하는 방법에 대한 자세한 내용은 [HTTP Client testing documentation](/docs/9.x/http-client#testing)를 참고하세요.

<a name="mail-fake"></a>
<!-- ## Mail Fake -->
## Mail Fake

<!-- You may use the `Mail` facade's `fake` method to prevent mail from being sent. Typically, sending mail is unrelated to the code you are actually testing. Most likely, it is sufficient to simply assert that Laravel was instructed to send a given mailable. -->
`Mail` 파사드의 `fake` 메서드를 사용하면 실제 메일 발송을 막을 수 있습니다. 일반적으로 메일 발송 자체는 테스트하려는 코드와는 무관한 경우가 많으니, "특정 메일러블(mailable)을 Laravel이 발송하려고 시도했는지만" 검증하면 충분합니다.

<!-- After calling the `Mail` facade's `fake` method, you may then assert that [mailables](/docs/9.x/mail) were instructed to be sent to users and even inspect the data the mailables received: -->
`Mail` 파사드의 `fake` 메서드 호출 후, [mailables](/docs/9.x/mail)의 발송 여부, 발송 대상, 전달 데이터 등을 다양한 방식으로 검증할 수 있습니다.

```
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);
    }
}
```

<!-- If you are queueing mailables for delivery in the background, you should use the `assertQueued` method instead of `assertSent`: -->
메시지를 백그라운드로 큐에 넣어 발송하는 경우라면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

<!-- You may pass a closure to the `assertSent`, `assertNotSent`, `assertQueued`, or `assertNotQueued` methods in order to assert that a mailable was sent that passes a given "truth test". If at least one mailable was sent that passes the given truth test then the assertion will be successful: -->
`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 메서드에 클로저를 전달하면, 원하는 조건을 만족하는 메일러블이 있는지 검증할 수 있습니다.

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<!-- When calling the `Mail` facade's assertion methods, the mailable instance accepted by the provided closure exposes helpful methods for examining the mailable: -->
`Mail` 파사드의 검증 메서드를 호출할 때, 제공한 클로저가 받는 메일러블 인스턴스에서는 다양한 헬퍼 메서드로 메일러블의 내용을 자세히 검증할 수 있습니다.

```
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...');
});
```

<!-- The mailable instance also includes several helpful methods for examining the attachments on a mailable: -->
첨부 파일 관련 내용도 다음과 같이 손쉽게 검증할 수 있습니다.

```
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function ($mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function ($mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function ($mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

<!-- You may have noticed that there are two methods for asserting that mail was not sent: `assertNotSent` and `assertNotQueued`. Sometimes you may wish to assert that no mail was sent **or** queued. To accomplish this, you may use the `assertNothingOutgoing` and `assertNotOutgoing` methods: -->
메일 발송 관련 부정 검증에는 `assertNotSent`와 `assertNotQueued` 두 가지 메서드가 있습니다. "메일이 전송도, 큐 등록도 안 됐는지" 한 번에 검증하려면 `assertNothingOutgoing`와 `assertNotOutgoing`을 사용하세요.

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="testing-mailable-content"></a>
<!-- #### Testing Mailable Content -->
#### Testing Mailable Content

<!-- We suggest testing the content of your mailables separately from your tests that assert that a given mailable was "sent" to a specific user. To learn how to test the content of your mailables, check out our documentation on the [testing mailables](/docs/9.x/mail#testing-mailables). -->
특정 대상에게 "메일이 발송되었는지"와 "메일 내용"의 테스트는 분리하는 것이 좋습니다. 메일러블의 내용 검증 방법은 [testing mailables](/docs/9.x/mail#testing-mailables)를 참고하세요.

<a name="notification-fake"></a>
<!-- ## Notification Fake -->
## Notification Fake

<!-- You may use the `Notification` facade's `fake` method to prevent notifications from being sent. Typically, sending notifications is unrelated to the code you are actually testing. Most likely, it is sufficient to simply assert that Laravel was instructed to send a given notification. -->
`Notification` 파사드의 `fake` 메서드를 사용하면 실제 알림 전송을 막을 수 있습니다. 대부분의 경우, 특정 알림이 전송 명령을 받았는지만 검증하면 충분합니다.

<!-- After calling the `Notification` facade's `fake` method, you may then assert that [notifications](/docs/9.x/notifications) were instructed to be sent to users and even inspect the data the notifications received: -->
`Notification` 파사드의 `fake` 메서드 호출 후, [notifications](/docs/9.x/notifications)이 실제로 어떤 사용자에게, 어떤 데이터와 함께 전송 시도되었는지 다양한 검증도 가능합니다.

```
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Notification::fake();

        // Perform order shipping...

        // Assert that no notifications were sent...
        Notification::assertNothingSent();

        // Assert a notification was sent to the given users...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // Assert a notification was not sent...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```

<!-- You may pass a closure to the `assertSentTo` or `assertNotSentTo` methods in order to assert that a notification was sent that passes a given "truth test". If at least one notification was sent that passes the given truth test then the assertion will be successful: -->
`assertSentTo`, `assertNotSentTo` 메서드에 클로저를 전달하여, 원하는 조건을 만족하는 알림이 있었는지 검증할 수 있습니다.

```
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
<!-- #### On-Demand Notifications -->
#### On-Demand Notifications

<!-- If the code you are testing sends [on-demand notifications](/docs/9.x/notifications#on-demand-notifications), you can test that the on-demand notification was sent via the `assertSentOnDemand` method: -->
테스트 대상 코드가 [on-demand notifications](/docs/9.x/notifications#on-demand-notifications)을 전송했다면, `assertSentOnDemand` 메서드로 검증할 수 있습니다.

```
Notification::assertSentOnDemand(OrderShipped::class);
```

<!-- By passing a closure as the second argument to the `assertSentOnDemand` method, you may determine if an on-demand notification was sent to the correct "route" address: -->
`assertSentOnDemand`에 클로저를 두 번째 인자로 넘기면, 온디맨드 알림이 올바른 "route" 주소로 전송되었는지까지 확인할 수 있습니다.

```
Notification::assertSentOnDemand(
    OrderShipped::class,
    function ($notification, $channels, $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="queue-fake"></a>
<!-- ## Queue Fake -->
## Queue Fake

<!-- You may use the `Queue` facade's `fake` method to prevent queued jobs from being pushed to the queue. Most likely, it is sufficient to simply assert that Laravel was instructed to push a given job to the queue since the queued jobs themselves may be tested in another test class. -->
`Queue` 파사드의 `fake` 메서드를 사용하면, 큐잉된 잡이 실제로 큐에 쌓이지 않게 할 수 있습니다. 대부분의 경우, "잡 자체"의 동작은 별도 테스트 클래스에서 검증하고, 여기서는 잡이 큐에 쌓였는지 여부만 assert(검증)하면 충분합니다.

<!-- After calling the `Queue` facade's `fake` method, you may then assert that the application attempted to push jobs to the queue: -->
`Queue` 파사드의 `fake` 메서드 호출 후, 애플리케이션이 실제로 잡을 큐에 푸시(push)하려고 했는지 다양한 방식으로 검증 가능합니다.

```
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Queue::fake();

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);
    }
}
```

<!-- You may pass a closure to the `assertPushed` or `assertNotPushed` methods in order to assert that a job was pushed that passes a given "truth test". If at least one job was pushed that passes the given truth test then the assertion will be successful: -->
`assertPushed`, `assertNotPushed` 메서드에 클로저를 넘기면, 원하는 조건의 잡이 푸시되었는지 검증할 수 있습니다.

```
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<!-- If you only need to fake specific jobs while allowing your other jobs to execute normally, you may pass the class names of the jobs that should be faked to the `fake` method: -->
특정 잡만 페이크 처리하고 나머지 잡은 실제로 실행되게 하고 싶다면, `fake` 메서드에 페이크로 처리할 잡 클래스명을 배열로 넘기세요.

```
public function test_orders_can_be_shipped()
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

<a name="job-chains"></a>
<!-- ### Job Chains -->
### Job Chains

<!-- The `Queue` facade's `assertPushedWithChain` and `assertPushedWithoutChain` methods may be used to inspect the job chain of a pushed job. The `assertPushedWithChain` method accepts the primary job as its first argument and an array of chained jobs as its second argument: -->
`Queue` 파사드의 `assertPushedWithChain`, `assertPushedWithoutChain` 메서드로, 잡 체이닝 여부를 세밀하게 검증할 수 있습니다. `assertPushedWithChain`은 첫 인자에 기본 잡, 두 번째 인자에 체이닝된 잡 배열을 전달합니다.

```
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Queue;

Queue::assertPushedWithChain(ShipOrder::class, [
    RecordShipment::class,
    UpdateInventory::class
]);
```

<!-- As you can see in the example above, the array of chained jobs may be an array of the job's class names. However, you may also provide an array of actual job instances. When doing so, Laravel will ensure that the job instances are of the same class and have the same property values of the chained jobs dispatched by your application: -->
체이닝된 잡 배열에는 클래스명 또는 잡 인스턴스를 사용할 수 있으며, 인스턴스 배열로 전달하면 클래스와 속성 값까지 모두 일치하는지 비교합니다.

```
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

<!-- You may use the `assertPushedWithoutChain` method to assert that a job was pushed without a chain of jobs: -->
잡에 체이닝 없이 단독으로 푸시되었는지 검증하려면 `assertPushedWithoutChain`을 사용하세요.

```
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
<!-- ## Storage Fake -->
## Storage Fake

<!-- The `Storage` facade's `fake` method allows you to easily generate a fake disk that, combined with the file generation utilities of the `Illuminate\Http\UploadedFile` class, greatly simplifies the testing of file uploads. For example: -->
`Storage` 파사드의 `fake` 메서드를 사용하면, 테스트용 가짜 디스크를 쉽게 만들 수 있습니다. 그리고 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 기능과 조합해 파일 업로드 테스트를 매우 단순화할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded()
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // Assert one or more files were stored...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // Assert one or more files were not stored...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // Assert that a given directory is empty...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

<!-- By default, the `fake` method will delete all files in its temporary directory. If you would like to keep these files, you may use the "persistentFake" method instead. For more information on testing file uploads, you may consult the [HTTP testing documentation's information on file uploads](/docs/9.x/http-tests#testing-file-uploads). -->
기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 자동 삭제합니다. 테스트 파일을 보존하려면 "persistentFake" 메서드를 사용할 수도 있습니다. 파일 업로드 테스트에 대한 자세한 내용은 [HTTP testing documentation's information on file uploads](/docs/9.x/http-tests#testing-file-uploads)을 참고하세요.

> [!WARNING]
> `image` 메서드는 [GD extension](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="interacting-with-time"></a>
<!-- ## Interacting With Time -->
## Interacting With Time

<!-- When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Thankfully, Laravel's base feature test class includes helpers that allow you to manipulate the current time: -->
테스트를 수행하다 보면, `now` 같은 헬퍼나 `Illuminate\Support\Carbon::now()`에서 반환하는 시간을 임의로 조작할 필요가 있을 수 있습니다. Laravel의 기본 기능 테스트 클래스는 현재 시간을 자유롭게 변형할 수 있게 도와주는 다양한 헬퍼를 제공합니다.

```
use Illuminate\Support\Carbon;

public function testTimeCanBeManipulated()
{
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Freeze time and resume normal time after executing closure...
    $this->freezeTime(function (Carbon $time) {
        // ...
    });

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->subHours(6));

    // Return back to the present time...
    $this->travelBack();
}
```
