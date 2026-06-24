<!-- # Events -->
# Events

- [Introduction](#introduction)
- [Generating Events and Listeners](#generating-events-and-listeners)
- [Registering Events and Listeners](#registering-events-and-listeners)
    - [Event Discovery](#event-discovery)
    - [Manually Registering Events](#manually-registering-events)
    - [Closure Listeners](#closure-listeners)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
    - [Manually Interacting With the Queue](#manually-interacting-with-the-queue)
    - [Queued Event Listeners and Database Transactions](#queued-event-listeners-and-database-transactions)
    - [Queued Listener Middleware](#queued-listener-middleware)
    - [Encrypted Queued Listeners](#encrypted-queued-listeners)
    - [Unique Event Listeners](#unique-event-listeners)
        - [Keeping Listeners Unique Until Processing Begins](#keeping-listeners-unique-until-processing-begins)
        - [Unique Listener Locks](#unique-listener-locks)
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
    - [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)
    - [Deferring Events](#deferring-events)
- [Event Subscribers](#event-subscribers)
    - [Writing Event Subscribers](#writing-event-subscribers)
    - [Registering Event Subscribers](#registering-event-subscribers)
- [Testing](#testing)
    - [Faking a Subset of Events](#faking-a-subset-of-events)
    - [Scoped Events Fakes](#scoped-event-fakes)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands. -->
Laravel의 이벤트는 간단한 관찰자 패턴 구현을 제공하므로 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 수신할 수 있습니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되고 해당 리스너는 `app/Listeners`에 저장됩니다. Artisan 콘솔 명령을 사용하여 이벤트 및 리스너를 생성할 때 이러한 디렉토리가 생성되므로 애플리케이션에 이러한 디렉토리가 표시되지 않더라도 걱정하지 마십시오.

<!-- Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification. -->
이벤트는 단일 이벤트가 서로 의존하지 않는 여러 리스너를 가질 수 있으므로 애플리케이션의 다양한 측면을 분리하는 훌륭한 방법으로 사용됩니다. 예를 들어, 주문이 디스패치될 때마다 사용자에게 Slack 알림을 보내려고 할 수 있습니다. 주문 처리 코드를 Slack 알림 코드에 연결하는 대신 리스너가 Slack 알림을 디스패치에 수신하고 사용할 수 있는 `App\Events\OrderShipped` 이벤트를 발생시킬 수 있습니다.

<a name="generating-events-and-listeners"></a>
<!-- ## Generating Events and Listeners -->
## Generating Events and Listeners

<!-- To quickly generate events and listeners, you may use the `make:event` and `make:listener` Artisan commands: -->
이벤트 및 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령을 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<!-- For convenience, you may also invoke the `make:event` and `make:listener` Artisan commands without additional arguments. When you do so, Laravel will automatically prompt you for the class name and, when creating a listener, the event it should listen to: -->
편의를 위해 추가 인수 없이 `make:event` 및 `make:listener` Artisan 명령을 호출할 수도 있습니다. 그렇게 하면 Laravel가 자동으로 클래스 이름을 묻는 메시지를 표시하며, 리스너를 생성할 때 수신해야 하는 이벤트는 다음과 같습니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
<!-- ## Registering Events and Listeners -->
## Registering Events and Listeners

<a name="event-discovery"></a>
<!-- ### Event Discovery -->
### Event Discovery

<!-- By default, Laravel will automatically find and register your event listeners by scanning your application's `Listeners` directory. When Laravel finds any listener class method that begins with `handle` or `__invoke`, Laravel will register those methods as event listeners for the event that is type-hinted in the method's signature: -->
기본적으로 Laravel는 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel가 `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 찾으면 Laravel는 해당 메서드를 메서드 시그니처에 형식 힌트가 있는 이벤트에 대해 이벤트 리스너로 등록합니다.

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

<!-- You may listen to multiple events using PHP's union types: -->
PHP의 공용체 유형을 사용하여 여러 이벤트를 들을 수 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

<!-- If you plan to store your listeners in a different directory or within multiple directories, you may instruct Laravel to scan those directories using the `withEvents` method in your application's `bootstrap/app.php` file: -->
리스너를 다른 디렉터리나 여러 디렉터리 내에 저장하려는 경우 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 해당 디렉터리를 검색하도록 Laravel에 지시할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

<!-- You may scan for listeners in multiple similar directories using the `*` character as a wildcard: -->
`*` 문자를 와일드카드로 사용하여 여러 유사한 디렉터리에서 리스너를 검색할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

<!-- The `event:list` command may be used to list all of the listeners registered within your application: -->
`event:list` 명령을 사용하면 애플리케이션 내에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
<!-- #### Event Discovery in Production -->
#### Event Discovery in Production

<!-- To give your application a speed boost, you should cache a manifest of all of your application's listeners using the `optimize` or `event:cache` Artisan commands. Typically, this command should be run as part of your application's [deployment process](/docs/12.x/deployment#optimization). This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the event cache. -->
애플리케이션 속도를 높이려면 `optimize` 또는 `event:cache` Artisan 명령을 사용하여 애플리케이션의 모든 리스너 매니페스트를 캐시해야 합니다. 일반적으로 이 명령은 애플리케이션의 [deployment process](/docs/12.x/deployment#optimization)의 일부로 실행되어야 합니다. 이 매니페스트는 프레임워크에서 이벤트 등록 프로세스 속도를 높이는 데 사용됩니다. `event:clear` 명령을 사용하여 이벤트 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
<!-- ### Manually Registering Events -->
### Manually Registering Events

<!-- Using the `Event` facade, you may manually register events and their corresponding listeners within the `boot` method of your application's `AppServiceProvider`: -->
`Event` 파사드를 사용하여, 애플리케이션 `AppServiceProvider`의 `boot` 메소드 내에서 이벤트 및 해당 리스너를 수동으로 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

<!-- The `event:list` command may be used to list all of the listeners registered within your application: -->
`event:list` 명령을 사용하면 애플리케이션 내에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
<!-- ### Closure Listeners -->
### Closure Listeners

<!-- Typically, listeners are defined as classes; however, you may also manually register closure-based event listeners in the `boot` method of your application's `AppServiceProvider`: -->
일반적으로 리스너는 클래스로 정의됩니다. 그러나 애플리케이션 `AppServiceProvider`의 `boot` 메소드에서 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다.

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
<!-- #### Queueable Anonymous Event Listeners -->
#### Queueable Anonymous Event Listeners

<!-- When registering closure-based event listeners, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/12.x/queues): -->
클로저 기반 이벤트 리스너를 등록할 때 Laravel에 [queue](/docs/12.x/queues)를 사용하여 리스너를 실행하도록 지시하기 위해 `Illuminate\Events\queueable` 함수 내에서 리스너 클로저를 래핑할 수 있습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

<!-- Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener: -->
큐에 있는 작업과 마찬가지로 `onConnection`, `onQueue` 및 `delay` 메서드를 사용하여 큐에 있는 리스너의 실행을 사용자 지정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure: -->
익명 대기 리스너 오류를 처리하려면 `queueable` 리스너를 정의하는 동안 `catch` 메서드에 대한 클로저를 제공할 수 있습니다. 이 클로저는 리스너의 실패를 일으킨 이벤트 인스턴스와 `Throwable` 인스턴스를 수신합니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="wildcard-event-listeners"></a>
<!-- #### Wildcard Event Listeners -->
#### Wildcard Event Listeners

<!-- You may also register listeners using the `*` character as a wildcard parameter, allowing you to catch multiple events on the same listener. Wildcard listeners receive the event name as their first argument and the entire event data array as their second argument: -->
또한 `*` 문자를 와일드카드 매개변수로 사용하여 리스너를 등록하면 동일한 리스너에서 여러 이벤트를 포착할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을 받고 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
<!-- ## Defining Events -->
## Defining Events

<!-- An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/12.x/eloquent) object: -->
이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 보유하는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 수신한다고 가정해 보겠습니다.

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<!-- As you can see, this event class contains no logic. It is a container for the `App\Models\Order` instance that was purchased. The `SerializesModels` trait used by the event will gracefully serialize any Eloquent models if the event object is serialized using PHP's `serialize` function, such as when utilizing [queued listeners](#queued-event-listeners). -->
보시다시피 이 이벤트 클래스에는 로직이 없습니다. 구매한 `App\Models\Order` 인스턴스용 컨테이너입니다. 이벤트에서 사용하는 `SerializesModels` 특성은 [queued listeners](#queued-event-listeners)를 사용할 때와 같이 PHP의 `serialize` 기능을 사용하여 이벤트 개체가 직렬화되는 경우 모든 Eloquent 모델을 우아하게 직렬화합니다.

<a name="defining-listeners"></a>
<!-- ## Defining Listeners -->
## Defining Listeners

<!-- Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `make:listener` Artisan command, when invoked with the `--event` option, will automatically import the proper event class and type-hint the event in the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event: -->
다음으로 이벤트 예제의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드로 이벤트 인스턴스를 수신합니다. `make:listener` Artisan 명령은 `--event` 옵션과 함께 호출되면 적절한 이벤트 클래스를 자동으로 가져오고 `handle` 메서드에서 이벤트를 유형 힌트합니다. `handle` 메서드 내에서 이벤트에 응답하는 데 필요한 모든 작업을 수행할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct() {}

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Access the order using $event->order...
    }
}
```

> [!NOTE]
> 이벤트 리스너는 생성자에 필요한 종속성을 유형 힌트할 수도 있습니다. 모든 이벤트 리스너는 Laravel [service container](/docs/12.x/container)를 통해 확인되므로 종속성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
<!-- #### Stopping The Propagation Of An Event -->
#### Stopping The Propagation Of An Event

<!-- Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method. -->
때로는 이벤트가 다른 리스너로 전파되는 것을 중지하고 싶을 수도 있습니다. 리스너의 `handle` 메소드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
<!-- ## Queued Event Listeners -->
## Queued Event Listeners

<!-- Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/12.x/queues) and start a queue worker on your server or local development environment. -->
리스너가 이메일을 보내거나 HTTP 요청을 하는 등 느린 작업을 수행하는 경우 리스너를 큐에 추가하는 것이 도움이 될 수 있습니다. 대기 중인 리스너를 사용하기 전에 [configure your queue](/docs/12.x/queues)을 확인하고 서버 또는 로컬 개발 환경에서 큐 워커를 시작하세요.

<!-- To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately: -->
리스너가 큐에 추가되도록 지정하려면 `ShouldQueue` 인터페이스를 리스너 클래스에 추가합니다. `make:listener` Artisan 명령으로 생성된 리스너에는 이미 이 인터페이스를 현재 네임스페이스로 가져왔으므로 즉시 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<!-- That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/12.x/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing. -->
그게 다야! 이제 이 리스너가 처리하는 이벤트가 디스패치이면 리스너는 Laravel의 [queue system](/docs/12.x/queues)을 사용하여 이벤트 디스패처에 의해 자동으로 큐에 추가됩니다. 리스너가 큐에 의해 실행될 때 예외가 발생하지 않으면 대기 중인 작업은 처리가 완료된 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
<!-- #### Customizing The Queue Connection, Name, & Delay -->
#### Customizing The Queue Connection, Name, & Delay

<!-- If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may define the `$connection`, `$queue`, or `$delay` properties on your listener class: -->
큐 연결, 큐 이름 또는 이벤트 리스너의 큐 지연 시간을 사용자 지정하려는 경우 리스너 클래스에서 `$connection`, `$queue` 또는 `$delay` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The name of the connection the job should be sent to.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * The name of the queue the job should be sent to.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * The time (seconds) before the job should be processed.
     *
     * @var int
     */
    public $delay = 60;
}
```

<!-- If you would like to define the listener's queue connection, queue name, or delay at runtime, you may define `viaConnection`, `viaQueue`, or `withDelay` methods on the listener: -->
리스너의 큐 연결, 큐 이름 또는 런타임 지연을 정의하려는 경우 리스너에서 `viaConnection`, `viaQueue` 또는 `withDelay` 메서드를 정의할 수 있습니다.

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
<!-- #### Conditionally Queueing Listeners -->
#### Conditionally Queueing Listeners

<!-- Sometimes, you may need to determine whether a listener should be queued based on some data that are only available at runtime. To accomplish this, a `shouldQueue` method may be added to a listener to determine whether the listener should be queued. If the `shouldQueue` method returns `false`, the listener will not be queued: -->
때로는 런타임에만 사용할 수 있는 일부 데이터를 기반으로 리스너를 큐에 넣어야 하는지 여부를 결정해야 할 수도 있습니다. 이를 달성하기 위해 리스너가 큐에 있어야 하는지 여부를 결정하기 위해 리스너에 `shouldQueue` 메서드를 추가할 수 있습니다. `shouldQueue` 메서드가 `false`를 반환하는 경우 리스너는 큐에 추가되지 않습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
<!-- ### Manually Interacting With the Queue -->
### Manually Interacting With the Queue

<!-- If you need to manually access the listener's underlying queue job's `delete` and `release` methods, you may do so using the `Illuminate\Queue\InteractsWithQueue` trait. This trait is imported by default on generated listeners and provides access to these methods: -->
리스너의 기본 큐 작업의 `delete` 및 `release` 메서드에 수동으로 액세스해야 하는 경우 `Illuminate\Queue\InteractsWithQueue` 특성을 사용하여 액세스할 수 있습니다. 이 특성은 생성된 리스너에서 기본적으로 가져오며 다음 메서드에 대한 액세스를 제공합니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        if ($condition) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
<!-- ### Queued Event Listeners and Database Transactions -->
### Queued Event Listeners and Database Transactions

<!-- When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed. -->
큐에 있는 리스너가 데이터베이스 트랜잭션 내의 디스패치인 경우 데이터베이스 트랜잭션이 커밋되기 전에 큐에 의해 처리될 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델 또는 데이터베이스 레코드에 대해 수행한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델 또는 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다. 리스너가 이러한 모델에 의존하는 경우 큐에 있는 디스패치인 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by implementing the `ShouldQueueAfterCommit` interface on the listener class: -->
큐 연결의 `after_commit` 구성 옵션이 `false`로 설정된 경우에도 리스너 클래스에서 `ShouldQueueAfterCommit` 인터페이스를 구현하여 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후에도 대기 중인 특정 리스너가 디스패치여야 함을 나타낼 수 있습니다.

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueueAfterCommit
{
    use InteractsWithQueue;
}
```

> [!NOTE]
> 이러한 문제를 해결하는 방법에 대해 자세히 알아보려면 [queued jobs and database transactions](/docs/12.x/queues#jobs-and-database-transactions)에 관한 설명서를 검토하세요.

<a name="queued-listener-middleware"></a>
<!-- ### Queued Listener Middleware -->
### Queued Listener Middleware

<!-- Queued listeners can also utilize [job middleware](/docs/12.x/queues#job-middleware). Job middleware allow you to wrap custom logic around the execution of queued listeners, reducing boilerplate in the listeners themselves. After creating job middleware, they may be attached to a listener by returning them from the listener's `middleware` method: -->
대기 중인 리스너는 [job middleware](/docs/12.x/queues#job-middleware)도 활용할 수 있습니다. 작업 미들웨어를 사용하면 큐에 있는 리스너 실행에 대한 사용자 지정 논리를 래핑하여 리스너 자체의 상용구를 줄일 수 있습니다. 작업 미들웨어를 생성한 후 리스너의 `middleware` 메서드에서 반환하여 리스너에 연결할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```

<a name="encrypted-queued-listeners"></a>
<!-- #### Encrypted Queued Listeners -->
#### Encrypted Queued Listeners

<!-- Laravel allows you to ensure the privacy and integrity of a queued listener's data via [encryption](/docs/12.x/encryption). To get started, simply add the `ShouldBeEncrypted` interface to the listener class. Once this interface has been added to the class, Laravel will automatically encrypt your listener before pushing it onto a queue: -->
Laravel을 사용하면 [encryption](/docs/12.x/encryption)를 통해 대기 중인 리스너 데이터의 개인정보 보호와 무결성을 보장할 수 있습니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 클래스에 추가되면 Laravel는 리스너를 큐에 푸시하기 전에 자동으로 암호화합니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="unique-event-listeners"></a>
<!-- ### Unique Event Listeners -->
### Unique Event Listeners

> [!WARNING]
> 고유한 리스너에는 [locks](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자 잠금을 지원합니다.

<!-- Sometimes, you may want to ensure that only one instance of a specific listener is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your listener class: -->
때로는 특정 리스너의 인스턴스 하나만 특정 시점에 큐에 있는지 확인하고 싶을 수도 있습니다. 리스너 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }
}
```

<!-- In the example above, the `AcquireProductKey` listener is unique. So, the listener will not be queued if another instance of the listener is already on the queue and has not finished processing. This ensures that only one product key is acquired for each license, even if the license is saved multiple times in quick succession. -->
위의 예에서 `AcquireProductKey` 리스너는 고유합니다. 따라서 리스너의 다른 인스턴스가 이미 큐에 있고 처리가 완료되지 않은 경우 리스너는 큐에 추가되지 않습니다. 이렇게 하면 라이선스가 빠르게 연속해서 여러 번 저장되더라도 각 라이선스에 대해 하나의 제품 키만 획득됩니다.

<!-- In certain cases, you may want to define a specific "key" that makes the listener unique or you may want to specify a timeout beyond which the listener no longer stays unique. To accomplish this, you may define `uniqueId` and `uniqueFor` properties or methods on your listener class. The methods receive the event instance, allowing you to use event data to construct the return value: -->
어떤 경우에는 리스너를 고유하게 만드는 특정 "키"를 정의하거나 리스너가 더 이상 고유한 상태를 유지하지 않는 시간 초과를 지정할 수 있습니다. 이를 수행하려면 리스너 클래스에 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의하면 됩니다. 메서드는 이벤트 인스턴스를 수신하므로 이벤트 데이터를 사용하여 반환 값을 구성할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    /**
     * The number of seconds after which the listener's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }

    /**
     * Get the unique ID for the listener.
     */
    public function uniqueId(LicenseSaved $event): string
    {
        return 'listener:'.$event->license->id;
    }
}
```

<!-- In the example above, the `AcquireProductKey` listener is unique by license ID. So, any new dispatches of the listener for the same license will be ignored until the existing listener has completed processing. This prevents duplicate product keys from being acquired for the same license. In addition, if the existing listener is not processed within one hour, the unique lock will be released and another listener with the same unique key can be queued. -->
위의 예에서 `AcquireProductKey` 리스너는 라이선스 ID별로 고유합니다. 따라서 동일한 라이선스에 대한 리스너의 새로운 디스패치는 기존 리스너의 처리가 완료될 때까지 무시됩니다. 이렇게 하면 동일한 라이선스에 대해 중복된 제품 키를 획득하는 것을 방지할 수 있습니다. 또한 기존 리스너가 1시간 이내에 처리되지 않으면 고유 잠금이 해제되고 동일한 고유 키를 가진 다른 리스너가 대기할 수 있습니다.

> [!WARNING]
> 여러 웹 서버 또는 컨테이너에서 애플리케이션 디스패치 이벤트를 사용하는 경우 Laravel가 리스너가 고유한지 정확하게 확인할 수 있도록 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="keeping-listeners-unique-until-processing-begins"></a>
<!-- #### Keeping Listeners Unique Until Processing Begins -->
#### Keeping Listeners Unique Until Processing Begins

<!-- By default, unique listeners are "unlocked" after a listener completes processing or fails all of its retry attempts. However, there may be situations where you would like your listener to unlock immediately before it is processed. To accomplish this, your listener should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract: -->
기본적으로 고유한 리스너는 리스너가 처리를 완료하거나 모든 재시도 시도에 실패한 후 "잠금 해제"됩니다. 그러나 리스너가 처리되기 직전에 잠금 해제되기를 원하는 상황이 있을 수 있습니다. 이를 달성하려면 리스너는 `ShouldBeUnique` 계약 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현해야 합니다.

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-listener-locks"></a>
<!-- #### Unique Listener Locks -->
#### Unique Listener Locks

<!-- Behind the scenes, when a `ShouldBeUnique` listener is dispatched, Laravel attempts to acquire a [lock](/docs/12.x/cache#atomic-locks) with the `uniqueId` key. If the lock is already held, the listener is not dispatched. This lock is released when the listener completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used: -->
뒤에서는 `ShouldBeUnique` 리스너가 디스패치일 때 Laravel가 `uniqueId` 키를 사용하여 [lock](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 잠금이 이미 유지된 경우 리스너는 디스패치가 아닙니다. 이 잠금은 리스너가 처리를 완료하거나 모든 재시도 시도에 실패하면 해제됩니다. 기본적으로 Laravel는 기본 캐시 드라이버를 사용하여 이 잠금을 획득합니다. 그러나 잠금 획득을 위해 다른 드라이버를 사용하려는 경우 사용해야 하는 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique listener lock.
     */
    public function uniqueVia(LicenseSaved $event): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 리스너의 동시 처리만 제한해야 하는 경우 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 작업 미들웨어를 대신 사용하세요.

<a name="handling-failed-jobs"></a>
<!-- ### Handling Failed Jobs -->
### Handling Failed Jobs

<!-- Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure: -->
때때로 대기 중인 이벤트 리스너가 실패할 수 있습니다. 큐에 있는 리스너가 큐 워커에 정의된 최대 시도 횟수를 초과하는 경우 `failed` 메서드가 리스너에서 호출됩니다. `failed` 메서드는 오류를 일으킨 이벤트 인스턴스와 `Throwable`를 수신합니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
<!-- #### Specifying Queued Listener Maximum Attempts -->
#### Specifying Queued Listener Maximum Attempts

<!-- If one of your queued listeners is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a listener may be attempted. -->
대기 중인 리스너 중 하나에 오류가 발생한 경우 무한정 계속 재시도하는 것을 원하지 않을 것입니다. 따라서 Laravel는 리스너를 시도할 수 있는 횟수 또는 기간을 지정하는 다양한 방법을 제공합니다.

<!-- You may define a `tries` property or method on your listener class to specify how many times the listener may be attempted before it is considered to have failed: -->
리스너 클래스에 `tries` 속성이나 메서드를 정의하여 리스너가 실패한 것으로 간주되기 전에 시도할 수 있는 횟수를 지정할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

<!-- As an alternative to defining how many times a listener may be attempted before it fails, you may define a time at which the listener should no longer be attempted. This allows a listener to be attempted any number of times within a given time frame. To define the time at which a listener should no longer be attempted, add a `retryUntil` method to your listener class. This method should return a `DateTime` instance: -->
리스너가 실패하기 전에 시도할 수 있는 횟수를 정의하는 대신 리스너를 더 이상 시도하지 않아야 하는 시간을 정의할 수 있습니다. 이를 통해 주어진 시간 내에 리스너를 여러 번 시도할 수 있습니다. 리스너를 더 이상 시도하지 않아야 하는 시간을 정의하려면 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메소드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

<!-- If both `retryUntil` and `tries` are defined, Laravel gives precedence to the `retryUntil` method. -->
`retryUntil` 및 `tries`가 모두 정의된 경우 Laravel는 `retryUntil` 메서드에 우선 순위를 부여합니다.

<a name="specifying-queued-listener-backoff"></a>
<!-- #### Specifying Queued Listener Backoff -->
#### Specifying Queued Listener Backoff

<!-- If you would like to configure how many seconds Laravel should wait before retrying a listener that has encountered an exception, you may do so by defining a `backoff` property on your listener class: -->
예외가 발생한 리스너를 재시도하기 전에 Laravel가 기다려야 하는 시간(초)을 구성하려면 리스너 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

<!-- If you require more complex logic for determining the listeners's backoff time, you may define a `backoff` method on your listener class: -->
리스너의 백오프 시간을 결정하기 위해 더 복잡한 로직이 필요한 경우 리스너 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
`backoff` 메서드에서 백오프 값 배열을 반환하여 "지수" 백오프를 쉽게 구성할 수 있습니다. 이 예에서 재시도 지연은 첫 번째 재시도의 경우 1초, 두 번째 재시도의 경우 5초, 세 번째 재시도의 경우 10초, 남은 시도가 더 있는 경우 모든 후속 재시도의 경우 10초입니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
<!-- #### Specifying Queued Listener Max Exceptions -->
#### Specifying Queued Listener Max Exceptions

<!-- Sometimes you may wish to specify that a queued listener may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may define a `maxExceptions` property on your listener class: -->
때로는 큐에 있는 리스너를 여러 번 시도할 수 있지만 처리되지 않은 예외의 지정된 수에 의해 재시도가 트리거되는 경우(`release` 메서드에 의해 직접 해제되는 것과 반대) 실패해야 함을 지정하고 싶을 수도 있습니다. 이를 수행하려면 리스너 클래스에 `maxExceptions` 속성을 정의하면 됩니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

<!-- In this example, the listener will be retried up to 25 times. However, the listener will fail if three unhandled exceptions are thrown by the listener. -->
이 예에서는 리스너가 최대 25번까지 재시도됩니다. 그러나 리스너에서 처리되지 않은 세 가지 예외가 발생하면 리스너가 실패합니다.

<a name="specifying-queued-listener-timeout"></a>
<!-- #### Specifying Queued Listener Timeout -->
#### Specifying Queued Listener Timeout

<!-- Often, you know roughly how long you expect your queued listeners to take. For this reason, Laravel allows you to specify a "timeout" value. If a listener is processing for longer than the number of seconds specified by the timeout value, the worker processing the listener will exit with an error. You may define the maximum number of seconds a listener should be allowed to run by defining a `timeout` property on your listener class: -->
큐에 있는 리스너가 예상되는 시간이 대략 얼마나 될지 아는 경우가 많습니다. 이러한 이유로 Laravel을 사용하면 "시간 초과" 값을 지정할 수 있습니다. 리스너가 시간 초과 값으로 지정된 시간(초)보다 오랫동안 처리하는 경우 리스너를 처리하는 워커는 오류와 함께 종료됩니다. 리스너 클래스에 `timeout` 속성을 정의하여 리스너 실행을 허용해야 하는 최대 시간(초)을 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The number of seconds the listener can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;
}
```

<!-- If you would like to indicate that a listener should be marked as failed on timeout, you may define the `failOnTimeout` property on the listener class: -->
리스너가 시간 초과 시 실패로 표시되어야 함을 나타내려면 리스너 클래스에 `failOnTimeout` 속성을 정의하면 됩니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Indicate if the listener should be marked as failed on timeout.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
<!-- ## Dispatching Events -->
## Dispatching Events

<!-- To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor: -->
디스패치 및 이벤트를 수행하려면 이벤트에서 정적 `dispatch` 메서드를 호출할 수 있습니다. 이 방법은 `Illuminate\Foundation\Events\Dispatchable` 특성을 통해 이벤트에서 사용할 수 있습니다. `dispatch` 메소드에 전달된 모든 인수는 이벤트의 생성자에 전달됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

<!-- If you would like to conditionally dispatch an event, you may use the `dispatchIf` and `dispatchUnless` methods: -->
이벤트를 조건부로 디스패치하려는 경우 `dispatchIf` 및 `dispatchUnless` 방법을 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트할 때 실제로 리스너를 트리거하지 않고 특정 이벤트가 디스패치였다고 주장하는 것이 도움이 될 수 있습니다. Laravel의 [built-in testing helpers](#testing)를 사용하면 문제가 해결됩니다.

<a name="dispatching-events-after-database-transactions"></a>
<!-- ### Dispatching Events After Database Transactions -->
### Dispatching Events After Database Transactions

<!-- Sometimes, you may want to instruct Laravel to only dispatch an event after the active database transaction has committed. To do so, you may implement the `ShouldDispatchAfterCommit` interface on the event class. -->
때로는 활성 데이터베이스 트랜잭션이 커밋된 후 디스패치 및 이벤트만 수행하도록 Laravel에 지시할 수도 있습니다. 이렇게 하려면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현할 수 있습니다.

<!-- This interface instructs Laravel to not dispatch the event until the current database transaction is committed. If the transaction fails, the event will be discarded. If no database transaction is in progress when the event is dispatched, the event will be dispatched immediately: -->
이 인터페이스는 현재 데이터베이스 트랜잭션이 커밋될 때까지 이벤트를 디스패치하지 않도록 Laravel에 지시합니다. 거래가 실패하면 이벤트가 폐기됩니다. 이벤트가 디스패치일 때 진행 중인 데이터베이스 트랜잭션이 없으면 이벤트는 즉시 디스패치가 됩니다.

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldDispatchAfterCommit
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="deferring-events"></a>
<!-- ### Deferring Events -->
### Deferring Events

<!-- Deferred events allow you to delay the dispatching of model events and execution of event listeners until after a specific block of code has completed. This is particularly useful when you need to ensure that all related records are created before event listeners are triggered. -->
지연된 이벤트를 사용하면 특정 코드 블록이 완료될 때까지 모델 이벤트의 디스패치 및 이벤트 리스너의 실행을 지연할 수 있습니다. 이는 이벤트 리스너가 트리거되기 전에 모든 관련 레코드가 생성되었는지 확인해야 할 때 특히 유용합니다.

<!-- To defer events, provide a closure to the `Event::defer()` method: -->
이벤트를 연기하려면 `Event::defer()` 메서드에 대한 클로저를 제공하세요.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

<!-- All events triggered within the closure will be dispatched after the closure is executed. This ensures that event listeners have access to all related records that were created during the deferred execution. If an exception occurs within the closure, the deferred events will not be dispatched. -->
클로저 내에서 트리거된 모든 이벤트는 클로저가 실행된 후 디스패치가 됩니다. 이렇게 하면 이벤트 리스너가 지연된 실행 중에 생성된 모든 관련 레코드에 액세스할 수 있습니다. 클로저 내에서 예외가 발생하면 지연된 이벤트는 디스패치가 아닙니다.

<!-- To defer only specific events, pass an array of events as the second argument to the `defer` method: -->
특정 이벤트만 연기하려면 이벤트 배열을 `defer` 메서드의 두 번째 인수로 전달합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
<!-- ## Event Subscribers -->
## Event Subscribers

<a name="writing-event-subscribers"></a>
<!-- ### Writing Event Subscribers -->
### Writing Event Subscribers

<!-- Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which receives an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners: -->
이벤트 구독자는 구독자 클래스 자체 내에서 여러 이벤트를 구독할 수 있는 클래스이므로 단일 클래스 내에서 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자는 이벤트 디스패처 인스턴스를 수신하는 `subscribe` 메서드를 정의해야 합니다. 이벤트 리스너를 등록하기 위해 주어진 디스패처에서 `listen` 메소드를 호출할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     */
    public function subscribe(Dispatcher $events): void
    {
        $events->listen(
            Login::class,
            [UserEventSubscriber::class, 'handleUserLogin']
        );

        $events->listen(
            Logout::class,
            [UserEventSubscriber::class, 'handleUserLogout']
        );
    }
}
```

<!-- If your event listener methods are defined within the subscriber itself, you may find it more convenient to return an array of events and method names from the subscriber's `subscribe` method. Laravel will automatically determine the subscriber's class name when registering the event listeners: -->
이벤트 리스너 메서드가 구독자 자체 내에 정의된 경우 구독자의 `subscribe` 메서드에서 이벤트 배열과 메서드 이름을 반환하는 것이 더 편리할 수 있습니다. Laravel는 이벤트 리스너를 등록할 때 구독자의 클래스 이름을 자동으로 결정합니다.

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     *
     * @return array<string, string>
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            Login::class => 'handleUserLogin',
            Logout::class => 'handleUserLogout',
        ];
    }
}
```

<a name="registering-event-subscribers"></a>
<!-- ### Registering Event Subscribers -->
### Registering Event Subscribers

<!-- After writing the subscriber, Laravel will automatically register handler methods within the subscriber if they follow Laravel's [event discovery conventions](#event-discovery). Otherwise, you may manually register your subscriber using the `subscribe` method of the `Event` facade. Typically, this should be done within the `boot` method of your application's `AppServiceProvider`: -->
구독자를 작성한 후 Laravel는 Laravel의 [event discovery conventions](#event-discovery)을 따르는 경우 구독자 내에 처리기 메서드를 자동으로 등록합니다. 그렇지 않으면 `Event` 파사드의 `subscribe` 메소드를 사용하여 구독자를 수동으로 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션 `AppServiceProvider`의 `boot` 메서드 내에서 수행되어야 합니다.

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing code that dispatches events, you may wish to instruct Laravel to not actually execute the event's listeners, since the listener's code can be tested directly and separately of the code that dispatches the corresponding event. Of course, to test the listener itself, you may instantiate a listener instance and invoke the `handle` method directly in your test. -->
디스패치 이벤트 코드를 테스트할 때 Laravel에 이벤트의 리스너를 실제로 실행하지 않도록 지시할 수 있습니다. 왜냐하면 리스너의 코드는 해당 디스패치 코드와 별도로 직접 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트하려면 리스너 인스턴스를 인스턴스화하고 테스트에서 `handle` 메서드를 직접 호출할 수 있습니다.

<!-- Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods: -->
`Event` 파사드의 `fake` 메소드를 사용하면 리스너 실행을 방지하고 테스트인 코드를 실행한 다음 `assertDispatched`, `assertNotDispatched` 및 `assertNothingDispatched` 메소드를 사용하여 애플리케이션에서 어떤 이벤트가 디스패치인지 확인할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
    Event::assertNothingDispatched();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

<!-- You may pass a closure to the `assertDispatched` or `assertNotDispatched` methods in order to assert that an event was dispatched that passes a given "truth test". If at least one event was dispatched that passes the given truth test then the assertion will be successful: -->
이벤트가 주어진 "진실 테스트"를 통과한 디스패치였다고 주장하기 위해 `assertDispatched` 또는 `assertNotDispatched` 메소드에 클로저를 전달할 수 있습니다. 적어도 하나의 이벤트가 주어진 진리 테스트를 통과하는 디스패치라면 어설션은 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

<!-- If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method: -->
이벤트 리스너가 주어진 이벤트를 듣고 있다고 주장하고 싶다면 `assertListening` 메소드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 후에는 이벤트 리스너가 실행되지 않습니다. 따라서 테스트에서 이벤트를 사용하는 모델 팩토리를 사용하는 경우(예: 모델의 `creating` 이벤트 중에 UUID를 생성하는 경우) 팩토리를 사용한 **후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
<!-- ### Faking a Subset of Events -->
### Faking a Subset of Events

<!-- If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method: -->
특정 이벤트 집합에 대해서만 이벤트 리스너를 위조하려는 경우 `fake` 또는 `fakeFor` 메서드에 전달할 수 있습니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```

<!-- You may fake all events except for a set of specified events using the `except` method: -->
`except` 메소드를 사용하여 지정된 이벤트 세트를 제외한 모든 이벤트를 위조할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
<!-- ### Scoped Event Fakes -->
### Scoped Event Fakes

<!-- If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method: -->
테스트의 일부에 대해서만 이벤트 리스너를 위조하려는 경우 `fakeFor` 메서드를 사용할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // Events are dispatched as normal and observers will run...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```
