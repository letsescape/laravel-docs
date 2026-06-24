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
Laravel 애플리케이션을 테스트할 때, 테스트 실행 중 실제로 실행되지 않도록 애플리케이션의 특정 부분을 "목(mock)"으로 대체하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때는 이벤트 리스너가 실제로 실행되는 걸 막고, 오직 컨트롤러의 HTTP 응답만 테스트하고 싶을 수 있습니다. 이벤트 리스너는 별도의 테스트 케이스에서 따로 검증할 수 있기 때문입니다.

<!-- Laravel provides helpful methods for mocking events, jobs, and other facades out of the box. These helpers primarily provide a convenience layer over Mockery so you do not have to manually make complicated Mockery method calls. -->
Laravel에는 이벤트, 잡, 그리고 기타 파사드(facade) 등을 손쉽게 목 처리할 수 있는 다양한 메서드가 내장되어 있습니다. 이러한 헬퍼들은 Mockery보다 훨씬 간편하게 목 객체를 만들고 사용할 수 있게 해줍니다.

<a name="mocking-objects"></a>
<!-- ## Mocking Objects -->
## Mocking Objects

<!-- When mocking an object that is going to be injected into your application via Laravel's [service container](/docs/8.x/container), you will need to bind your mocked instance into the container as an `instance` binding. This will instruct the container to use your mocked instance of the object instead of constructing the object itself: -->
Laravel의 [service container](/docs/8.x/container)를 통해 주입되는 객체를 목(mock)으로 테스트하려면, 목 객체를 `instance` 바인딩으로 컨테이너에 등록해야 합니다. 이렇게 하면 컨테이너는 객체를 직접 생성하는 대신, 여러분이 생성한 목 객체를 주입하게 됩니다.

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
이 과정을 더 편리하게 하기 위해, Laravel의 기본 테스트 케이스 클래스에는 `mock` 메서드가 준비되어 있습니다. 아래 예시는 위와 같은 효과를 갖습니다.

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- You may use the `partialMock` method when you only need to mock a few methods of an object. The methods that are not mocked will be executed normally when called: -->
객체의 일부 메서드만 목으로 대체하고 싶다면, `partialMock` 메서드를 사용할 수 있습니다. 목 처리하지 않은 다른 메서드들은 호출 시 실제로 동작합니다.

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

<!-- Similarly, if you want to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on an object, Laravel's base test case class offers a `spy` method as a convenient wrapper around the `Mockery::spy` method. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
비슷하게, [spy](http://docs.mockery.io/en/latest/reference/spies.html)를 사용해 객체의 실제 동작을 기록만 하고 싶을 때는, Laravel 테스트 기본 클래스에서 `Mockery::spy` 메서드를 편리하게 감싸는 `spy` 메서드를 이용할 수 있습니다. 스파이는 목과 유사하지만, 테스트 코드 실행 후 해당 메서드가 실제로 호출됐는지 검증할 수 있도록 상호작용을 기록합니다.

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
<!-- ## Mocking Facades -->
## Mocking Facades

<!-- Unlike traditional static method calls, [facades](/docs/8.x/facades) (including [real-time facades](/docs/8.x/facades#real-time-facades)) may be mocked. This provides a great advantage over traditional static methods and grants you the same testability that you would have if you were using traditional dependency injection. When testing, you may often want to mock a call to a Laravel facade that occurs in one of your controllers. For example, consider the following controller action: -->
전통적인 static 메서드 호출과 달리, [facades](/docs/8.x/facades)([real-time facades](/docs/8.x/facades#real-time-facades) 포함)는 목(mock) 처리가 가능합니다. 이는 전통적인 static 메서드보다 뛰어난 테스트 작성 가능성을 제공하며, DI(의존성 주입)처럼 쉽게 테스트할 수 있도록 해줍니다. 테스트할 때 컨트롤러 내부에서 발생하는 Laravel 파사드 호출을 목 처리하고 싶은 경우가 많습니다. 예를 들어, 다음과 같은 컨트롤러 액션을 살펴보겠습니다.

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

<!-- We can mock the call to the `Cache` facade by using the `shouldReceive` method, which will return an instance of a [Mockery](https://github.com/padraic/mockery) mock. Since facades are actually resolved and managed by the Laravel [service container](/docs/8.x/container), they have much more testability than a typical static class. For example, let's mock our call to the `Cache` facade's `get` method: -->
`Cache` 파사드에 대한 호출을 목으로 대체하려면 `shouldReceive` 메서드를 사용하면 됩니다. 이는 [Mockery](https://github.com/padraic/mockery)의 목 객체를 반환합니다. 파사드는 실제로 Laravel [service container](/docs/8.x/container)에서 resolve(해결)되고 관리되므로, 일반 static 클래스보다 높은 테스트 유연성을 제공합니다. `Cache` 파사드의 `get` 메서드 호출을 목 처리하려면 다음과 같이 작성할 수 있습니다.

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

> [!NOTE]
> `Request` 파사드는 목(mock) 처리하지 마시기 바랍니다. 대신, 테스트를 실행할 때 `get`, `post`와 같은 [HTTP testing methods](/docs/8.x/http-tests)에 원하는 입력값을 전달하세요. 마찬가지로, `Config` 파사드를 목 처리하는 대신 테스트 안에서 `Config::set` 메서드를 호출하면 됩니다.

<a name="facade-spies"></a>
<!-- ### Facade Spies -->
### Facade Spies

<!-- If you would like to [spy](http://docs.mockery.io/en/latest/reference/spies.html) on a facade, you may call the `spy` method on the corresponding facade. Spies are similar to mocks; however, spies record any interaction between the spy and the code being tested, allowing you to make assertions after the code is executed: -->
파사드를 [spy](http://docs.mockery.io/en/latest/reference/spies.html)로 감시하고 싶다면, 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 목 객체와 유사하지만, 실제 호출 기록이 남아 이후 검증(assertion)이 가능합니다.

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
잡(jobs)을 디스패치(dispatch)하는 코드를 테스트할 때, 실제로 잡이 큐(queue)에 들어가거나 실행되는 것까지 테스트하고 싶지 않을 수 있습니다. 잡 자체의 실행은 대개 별도의 테스트에서 검증할 수 있기 때문입니다.

<!-- You may use the `Bus` facade's `fake` method to prevent jobs from being dispatched to the queue. Then, after executing the code under test, you may inspect which jobs the application attempted to dispatch using the `assertDispatched` and `assertNotDispatched` methods: -->
잡이 실제로 큐에 들어가지 않게 하려면, `Bus` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이후 테스트 코드 실행 후 `assertDispatched`, `assertNotDispatched` 등의 메서드로 어떤 잡이 디스패치되려고 했는지 간단히 검증할 수 있습니다.

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

        // Assert that a job was not dipatched synchronously...
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
이러한 메서드들에는 클로저를 전달하여, 주어진 "조건"을 만족하는 잡이 실제로 디스패치됐는지 세밀하게 검증할 수도 있습니다. 예를 들어, 특정 주문에 대한 잡이 디스패치됐는지 확인하려면 다음과 같이 작성합니다.

```
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="bus-job-chains"></a>
<!-- ### Job Chains -->
### Job Chains

<!-- The `Bus` facade's `assertChained` method may be used to assert that a [chain of jobs](/docs/8.x/queues#job-chaining) was dispatched. The `assertChained` method accepts an array of chained jobs as its first argument: -->
`Bus` 파사드의 `assertChained` 메서드를 사용하면, [chain of jobs](/docs/8.x/queues#job-chaining)이 디스패치 되었는지 검증할 수 있습니다. `assertChained` 메서드는 첫 번째 인자로 체인에 포함된 잡들의 배열을 받습니다.

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
위 예시처럼, 잡 클래스명을 배열로 제공할 수도 있고, 실제 잡 인스턴스의 배열을 넘겨도 됩니다. 잡 인스턴스를 사용할 경우 Laravel은 인스턴스의 클래스명과 속성 값이 실제 디스패치된 잡과 동일한지까지 확인합니다.

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

<!-- The `Bus` facade's `assertBatched` method may be used to assert that a [batch of jobs](/docs/8.x/queues#job-batching) was dispatched. The closure given to the `assertBatched` method receives an instance of `Illuminate\Bus\PendingBatch`, which may be used to inspect the jobs within the batch: -->
`Bus` 파사드의 `assertBatched` 메서드는 [batch of jobs](/docs/8.x/queues#job-batching)가 디스패치 되었는지 검증합니다. `assertBatched` 메서드에 전달한 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 전달되며, 배치에 포함된 잡을 확인할 수 있습니다.

```
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="event-fake"></a>
<!-- ## Event Fake -->
## Event Fake

<!-- When testing code that dispatches events, you may wish to instruct Laravel to not actually execute the event's listeners. Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods: -->
이벤트를 디스패치하는 코드를 테스트할 때 실제로 이벤트 리스너가 실행되지 않도록 하려면, `Event` 파사드의 `fake` 메서드를 사용하세요. 이렇게 하면, 리스너가 동작하지 않고도 테스트 코드를 실행한 뒤, 어떤 이벤트가 디스패치 됐는지를 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다.

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
`assertDispatched`, `assertNotDispatched` 등의 메서드에도 클로저를 전달할 수 있습니다. 클로저는 "조건"을 만족하는 이벤트가 디스패치 됐는지를 세부적으로 검증할 때 유용합니다.

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

<!-- If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method: -->
이벤트 리스너가 특정 이벤트를 청취(listen)하는지 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!NOTE]
> `Event::fake()`를 호출하면 모든 이벤트 리스너가 실제로 실행되지 않습니다. 만약 테스트에서 이벤트에 의존하는 모델 팩토리(예: 모델 `creating` 이벤트에서 UUID를 생성) 등을 사용하는 경우, 팩토리를 먼저 사용한 뒤 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
<!-- #### Faking A Subset Of Events -->
#### Faking A Subset Of Events

<!-- If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method: -->
특정 이벤트에 대해서만 리스너가 실행되지 않도록 하고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트 목록을 배열로 전달하면 됩니다.

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

<a name="scoped-event-fakes"></a>
<!-- ### Scoped Event Fakes -->
### Scoped Event Fakes

<!-- If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method: -->
테스트의 특정 구간에서만 이벤트 리스너를 실행하지 않도록 페이크 처리하려면, `fakeFor` 메서드를 사용하면 됩니다.

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

<!-- The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. For more information on faking outgoing HTTP requests, please consult the [HTTP Client testing documentation](/docs/8.x/http-client#testing). -->
`Http` 파사드의 `fake` 메서드를 사용하면, HTTP 클라이언트가 외부로 요청을 보내는 대신 미리 준비한 더미/가짜 응답을 반환하도록 변경할 수 있습니다. 외부 HTTP 요청 페이크 처리 방법은 [HTTP Client testing documentation](/docs/8.x/http-client#testing)를 참고하세요.

<a name="mail-fake"></a>
<!-- ## Mail Fake -->
## Mail Fake

<!-- You may use the `Mail` facade's `fake` method to prevent mail from being sent. Typically, sending mail is unrelated to the code you are actually testing. Most likely, it is sufficient to simply assert that Laravel was instructed to send a given mailable. -->
`Mail` 파사드의 `fake` 메서드를 사용하면, 실제로 메일이 전송되는 것을 막을 수 있습니다. 일반적으로 메일 전송 자체는 실제로 테스트할 대상과는 직접적 관련이 없는 경우가 많으니, Laravel이 특정 전달 객체(mailable)를 전송하도록 지시했는지만 검증하는 것으로 충분합니다.

<!-- After calling the `Mail` facade's `fake` method, you may then assert that [mailables](/docs/8.x/mail) were instructed to be sent to users and even inspect the data the mailables received: -->
`Mail` 파사드의 `fake` 메서드를 호출한 후에는, [mailables](/docs/8.x/mail)가 실제로 전송 요청됐는지 여부를 검증하거나, 전달된 데이터까지 확인할 수 있습니다.

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
만약 mailable을 백그라운드에서 큐로 전송한다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다.

```
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

<!-- You may pass a closure to the `assertSent`, `assertNotSent`, `assertQueued`, or `assertNotQueued` methods in order to assert that a mailable was sent that passes a given "truth test". If at least one mailable was sent that passes the given truth test then the assertion will be successful: -->
`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등에는 클로저를 전달해, 조건을 만족하는 mailable이 실제 전송됐는지 세밀하게 검증할 수 있습니다.

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<!-- When calling the `Mail` facade's assertion methods, the mailable instance accepted by the provided closure exposes helpful methods for examining the recipients of the mailable: -->
`Mail` 파사드의 검증 메서드를 호출할 때, 제공한 클로저가 전달받는 mailable 인스턴스는 mailable의 수신자를 확인할 수 있는 편리한 메서드들을 제공합니다.

```
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...');
});
```

<!-- You may have noticed that there are two methods for asserting that mail was not sent: `assertNotSent` and `assertNotQueued`. Sometimes you may wish to assert that no mail was sent **or** queued. To accomplish this, you may use the `assertNothingOutgoing` and `assertNotOutgoing` methods: -->
메시지가 전송되지 않았음을 검증하는 메서드는 `assertNotSent`와 `assertNotQueued` 두 가지가 있습니다. 메일이 전송되지 **않았고** 큐에도 들어가지 않았음을 한 번에 확인하려면, `assertNothingOutgoing` 또는 `assertNotOutgoing` 메서드를 사용할 수 있습니다.

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="notification-fake"></a>
<!-- ## Notification Fake -->
## Notification Fake

<!-- You may use the `Notification` facade's `fake` method to prevent notifications from being sent. Typically, sending notifications is unrelated to the code you are actually testing. Most likely, it is sufficient to simply assert that Laravel was instructed to send a given notification. -->
`Notification` 파사드의 `fake` 메서드를 사용하면, 실제로 알림이 전송되지 않도록 할 수 있습니다. 거의 대부분의 경우, 전달된 알림이 실제로 사용자에게 전송되는지 보다는, "Laravel이 해당 알림을 전송하도록 지시했는가"만을 확인하는 것으로 충분합니다.

<!-- After calling the `Notification` facade's `fake` method, you may then assert that [notifications](/docs/8.x/notifications) were instructed to be sent to users and even inspect the data the notifications received: -->
`Notification` 파사드의 `fake` 메서드를 호출한 후에는, [notifications](/docs/8.x/notifications)이 실제로 전송됐는지, 그리고 어떤 데이터가 전달됐는지 아래와 같이 검증할 수 있습니다.

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
    }
}
```

<!-- You may pass a closure to the `assertSentTo` or `assertNotSentTo` methods in order to assert that a notification was sent that passes a given "truth test". If at least one notification was sent that passes the given truth test then the assertion will be successful: -->
`assertSentTo`, `assertNotSentTo`에 클로저를 전달해, 특정 조건을 만족하는 알림이 실제 전송됐는지 세부적으로 검증할 수 있습니다.

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

<!-- If the code you are testing sends [on-demand notifications](/docs/8.x/notifications#on-demand-notifications), you will need to assert that the notification was sent to an `Illuminate\Notifications\AnonymousNotifiable` instance: -->
테스트하는 코드가 [on-demand notifications](/docs/8.x/notifications#on-demand-notifications)을 전송했다면, 알림이 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스에 전송됐는지 검증해야 합니다.

```
use Illuminate\Notifications\AnonymousNotifiable;

Notification::assertSentTo(
    new AnonymousNotifiable, OrderShipped::class
);
```

<!-- By passing a closure as the third argument to the notification assertion methods, you may determine if an on-demand notification was sent to the correct "route" address: -->
알림 검증 메서드의 세 번째 인자로 클로저를 전달하면, 온디맨드 알림이 올바른 "route" 주소로 전송됐는지 추가적으로 확인할 수 있습니다.

```
Notification::assertSentTo(
    new AnonymousNotifiable,
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
`Queue` 파사드의 `fake` 메서드를 사용하면, 큐에 들어가는 잡이 실제로 큐에 push 되지 않도록 막을 수 있습니다. 대부분의 경우, "Laravel이 특정 잡을 큐에 푸시(push)하도록 지시했는가"만 따져 보고, 잡의 구현 및 실행은 별도 테스트에서 검증하면 충분합니다.

<!-- After calling the `Queue` facade's `fake` method, you may then assert that the application attempted to push jobs to the queue: -->
`Queue` 파사드의 `fake` 메서드를 호출한 후에는, 애플리케이션에서 잡을 큐에 보내려 했는지 다양하게 검증할 수 있습니다.

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
`assertPushed`, `assertNotPushed` 등의 메서드에는 클로저를 활용해, 조건을 만족하는 잡이 실제로 푸시됐는지 세밀하게 확인할 수 있습니다.

```
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="job-chains"></a>
<!-- ### Job Chains -->
### Job Chains

<!-- The `Queue` facade's `assertPushedWithChain` and `assertPushedWithoutChain` methods may be used to inspect the job chain of a pushed job. The `assertPushedWithChain` method accepts the primary job as its first argument and an array of chained jobs as its second argument: -->
`Queue` 파사드의 `assertPushedWithChain` 및 `assertPushedWithoutChain` 메서드는, 큐에 푸시된 잡의 체인(chain)을 검증하는 용도로 활용할 수 있습니다. `assertPushedWithChain`는 첫 번째 인자로 기본 잡, 두 번째 인자로 체인에 연결될 잡들의 배열을 받습니다.

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
위 예시처럼 잡 클래스명을 배열로 넘길 수도 있고, 실제 잡 인스턴스의 배열도 막힘없이 사용할 수 있습니다. 잡 인스턴스를 넘기면, Laravel이 해당 인스턴스의 클래스와 속성 값이 실제 체인과 같은지까지 확인합니다.

```
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

<!-- You may use the `assertPushedWithoutChain` method to assert that a job was pushed without a chain of jobs: -->
잡 체인 없이 잡이 푸시됐는지 확인하려면 `assertPushedWithoutChain` 메서드를 사용할 수 있습니다.

```
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
<!-- ## Storage Fake -->
## Storage Fake

<!-- The `Storage` facade's `fake` method allows you to easily generate a fake disk that, combined with the file generation utilities of the `Illuminate\Http\UploadedFile` class, greatly simplifies the testing of file uploads. For example: -->
`Storage` 파사드의 `fake` 메서드를 활용하면, 가짜 디스크를 쉽게 생성해 테스트 파일 업로드를 훨씬 쉽고 빠르게 진행할 수 있습니다. `Illuminate\Http\UploadedFile` 클래스의 파일 생성 기능과 조합해 사용하면 매우 편리합니다.

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
    }
}
```

<!-- For more information on testing file uploads, you may consult the [HTTP testing documentation's information on file uploads](/docs/8.x/http-tests#testing-file-uploads). -->
파일 업로드 테스트에 대한 자세한 내용은 [HTTP testing documentation's information on file uploads](/docs/8.x/http-tests#testing-file-uploads) 항목을 참고하세요.

> [!TIP]
> 기본적으로 `fake` 메서드는 임시 디렉토리 내의 파일을 모두 삭제합니다. 테스트가 끝난 후에도 파일을 유지하고 싶다면, "persistentFake" 메서드를 사용하세요.

<a name="interacting-with-time"></a>
<!-- ## Interacting With Time -->
## Interacting With Time

<!-- When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Thankfully, Laravel's base feature test class includes helpers that allow you to manipulate the current time: -->
테스트 도중, `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 임의로 조정해야 할 때가 있습니다. 다행히 Laravel의 기본 feature 테스트 클래스에는 현재 시간을 쉽게 조작할 수 있는 헬퍼 메서드가 포함되어 있습니다.

```
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

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->subHours(6));

    // Return back to the present time...
    $this->travelBack();
}
```
