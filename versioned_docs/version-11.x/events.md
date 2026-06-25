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
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
    - [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)
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
Laravel의 이벤트는 간단한 옵저버 패턴(Observer Pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 리스닝할 수 있도록 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에, 관련 리스너는 `app/Listeners` 디렉터리에 보관됩니다. 이 디렉터리들이 애플리케이션에 없다면 걱정하지 마십시오. Artisan 콘솔 명령어로 이벤트나 리스너를 생성하면 자동으로 만들어집니다.

<!-- Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification. -->
이벤트는 애플리케이션의 다양한 기능을 분리(디커플링)할 수 있는 훌륭한 방법입니다. 하나의 이벤트에 여러 개의 리스너가 존재할 수 있으며, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보낼 수 있습니다. 주문 처리 코드와 Slack 알림 코드를 서로 엮지 않고, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너가 이 이벤트를 받아 Slack 알림을 보낼 수 있습니다.

<a name="generating-events-and-listeners"></a>
<!-- ## Generating Events and Listeners -->
## Generating Events and Listeners

<!-- To quickly generate events and listeners, you may use the `make:event` and `make:listener` Artisan commands: -->
이벤트와 리스너를 빠르게 생성하려면, `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<!-- For convenience, you may also invoke the `make:event` and `make:listener` Artisan commands without additional arguments. When you do so, Laravel will automatically prompt you for the class name and, when creating a listener, the event it should listen to: -->
보다 편리하게, `make:event` 또는 `make:listener` 명령어를 인자 없이 실행하면 Laravel에서 클래스명을 입력하도록 안내하고, 리스너 생성 시에는 어떤 이벤트를 리스닝할지 물어봅니다.

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
기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel이 메서드명이 `handle` 또는 `__invoke`로 시작하는 리스너 클래스를 발견하면, 해당 메서드의 시그니처에 타입힌트된 이벤트를 리스닝하는 이벤트 리스너로 자동 등록합니다.

```
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the given event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

<!-- You may listen to multiple events using PHP's union types: -->
PHP의 유니언 타입을 활용해서 여러 이벤트를 동시에 수신할 수도 있습니다.

```
/**
 * Handle the given event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

<!-- If you plan to store your listeners in a different directory or within multiple directories, you may instruct Laravel to scan those directories using the `withEvents` method in your application's `bootstrap/app.php` file: -->
리스너를 다른 디렉터리나 여러 디렉터리에 저장하고자 한다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉터리들을 스캔하도록 Laravel에 지시할 수 있습니다.

```
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

<!-- You may scan for listeners in multiple similar directories using the `*` character as a wildcard: -->
`*` 와일드카드 문자를 사용하면 비슷한 여러 디렉터리도 한 번에 스캔할 수 있습니다.

```
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

<!-- The `event:list` command may be used to list all of the listeners registered within your application: -->
`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너 목록을 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
<!-- #### Event Discovery in Production -->
#### Event Discovery in Production

<!-- To give your application a speed boost, you should cache a manifest of all of your application's listeners using the `optimize` or `event:cache` Artisan commands. Typically, this command should be run as part of your application's [deployment process](/docs/11.x/deployment#optimization). This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the event cache. -->
애플리케이션의 속도를 높이기 위해서는 `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너의 매니페스트를 캐시하는 것이 좋습니다. 이 명령어는 일반적으로 [deployment process](/docs/11.x/deployment#optimization)의 일부로 실행되어야 하며, 만들어진 매니페스트는 프레임워크가 이벤트 등록을 더 빠르게 처리할 수 있게 도와줍니다. 캐시를 비우려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
<!-- ### Manually Registering Events -->
### Manually Registering Events

<!-- Using the `Event` facade, you may manually register events and their corresponding listeners within the `boot` method of your application's `AppServiceProvider`: -->
`Event` 파사드를 사용해 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 직접 이벤트와 그에 대응하는 리스너를 수동으로 등록할 수 있습니다.

```
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
`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
<!-- ### Closure Listeners -->
### Closure Listeners

<!-- Typically, listeners are defined as classes; however, you may also manually register closure-based event listeners in the `boot` method of your application's `AppServiceProvider`: -->
일반적으로 리스너는 클래스로 정의되지만, `AppServiceProvider`의 `boot` 메서드 내에서 클로저(익명 함수) 기반의 이벤트 리스너도 직접 등록할 수 있습니다.

```
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

<!-- When registering closure based event listeners, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/11.x/queues): -->
클로저 기반 이벤트 리스너를 등록할 때, 해당 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸주면 Laravel이 [queue](/docs/11.x/queues)를 사용해 비동기적으로 실행하게 할 수 있습니다.

```
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
큐잉된 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 활용해서 큐잉된 리스너의 실행 방법도 커스터마이징할 수 있습니다.

```
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure: -->
익명 큐잉 리스너의 실패를 별도로 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드로 실패 시 실행할 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너의 실패를 일으킨 `Throwable` 인스턴스를 전달받게 됩니다.

```
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
`*` 문자를 와일드카드 파라미터로 사용해, 여러 이벤트를 하나의 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 이벤트명을 첫 번째 인수, 이벤트 데이터 배열 전체를 두 번째 인수로 전달받습니다.

```
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
<!-- ## Defining Events -->
## Defining Events

<!-- An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/11.x/eloquent) object: -->
이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너라고 할 수 있습니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/11.x/eloquent) 객체를 전달받는다고 가정해보겠습니다.

```
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
보시다시피 이 이벤트 클래스에는 별도의 로직이 없습니다. `App\Models\Order` 인스턴스를 담고 있는 컨테이너 역할을 합니다. 이 이벤트에 사용된 `SerializesModels` 트레이트는, [queued listeners](#queued-event-listeners) 등 이벤트 객체가 PHP의 `serialize` 함수를 통해 직렬화될 때 Eloquent 모델을 안전하게 직렬화할 수 있도록 해줍니다.

<a name="defining-listeners"></a>
<!-- ## Defining Listeners -->
## Defining Listeners

<!-- Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `make:listener` Artisan command, when invoked with the `--event` option, will automatically import the proper event class and type-hint the event in the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event: -->
다음으로, 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드에서 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 실행하면 해당 이벤트 클래스가 자동으로 임포트되고 `handle` 메서드에 타입힌트까지 추가됩니다. `handle` 메서드 내부에서 이벤트에 응답하기 위해 필요한 모든 작업을 수행할 수 있습니다.

```
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
> 이벤트 리스너의 생성자에서도 필요한 의존성을 타입힌트로 지정할 수 있습니다. 모든 이벤트 리스너는 Laravel의 [service container](/docs/11.x/container)를 통해 생성되므로, 필요한 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
<!-- #### Stopping The Propagation Of An Event -->
#### Stopping The Propagation Of An Event

<!-- Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method. -->
때로는 해당 이벤트가 다른 리스너로 더 이상 전달되지 않도록 중단하고 싶을 때가 있을 수 있습니다. 이런 경우 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파를 중단할 수 있습니다.

<a name="queued-event-listeners"></a>
<!-- ## Queued Event Listeners -->
## Queued Event Listeners

<!-- Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/11.x/queues) and start a queue worker on your server or local development environment. -->
이벤트 리스너에서 이메일 발송, HTTP 요청 등 시간이 오래 걸리는 작업을 처리한다면, 리스너를 큐잉(비동기 처리)하는 것이 좋습니다. 큐잉 리스너를 사용하기 전에 [configure your queue](/docs/11.x/queues)을 마치고, 서버나 로컬 개발 환경에서 큐 워커를 실행해야 합니다.

<!-- To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately: -->
특정 리스너를 큐잉하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가합니다. `make:listener` Artisan 명령어로 생성할 경우, 이 인터페이스가 네임스페이스에 이미 임포트되어 있어 바로 사용할 수 있습니다.

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<!-- That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/11.x/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing. -->
이것만으로도 충분합니다! 이제 이 리스너에서 처리하는 이벤트가 발생하면, 해당 리스너는 Laravel의 [queue system](/docs/11.x/queues)을 통해 자동으로 큐에 등록됩니다. 리스너 실행 중 예외가 발생하지 않으면, 큐 작업이 성공적으로 끝난 뒤 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
<!-- #### Customizing The Queue Connection, Name, & Delay -->
#### Customizing The Queue Connection, Name, & Delay

<!-- If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may define the `$connection`, `$queue`, or `$delay` properties on your listener class: -->
리스너가 사용할 큐 연결명, 큐 이름 또는 딜레이(작업 지연 시간)를 커스터마이징하고 싶다면, 리스너 클래스에서 `$connection`, `$queue`, `$delay` 속성을 정의할 수 있습니다.

```
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
큐 연결, 큐 이름, 딜레이 값을 런타임에서 동적으로 정하고 싶다면, 리스너 클래스에 `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현하면 됩니다.

```
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
경우에 따라 리스너가 큐잉되어야 하는지 여부를 런타임 데이터에 따라 정해야 할 때가 있습니다. 이런 경우, 리스너 클래스에 `shouldQueue` 메서드를 추가해 큐잉 여부를 판단할 수 있습니다. `shouldQueue` 메서드가 `false`를 반환하면 해당 리스너는 큐잉되지 않습니다.

```
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
리스너 내부에서 underlying 큐 작업의 `delete`, `release` 메서드에 직접 접근할 필요가 있다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 기본적으로 생성된 리스너에 이미 포함되어 있습니다.

```
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
        if (true) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
<!-- ### Queued Event Listeners and Database Transactions -->
### Queued Event Listeners and Database Transactions

<!-- When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed. -->
큐잉 리스너가 데이터베이스 트랜잭션 내에서 디스패치 될 때, 큐가 데이터베이스 트랜잭션이 커밋되기 전에 해당 리스너를 처리할 수도 있습니다. 이 경우, 트랜잭션 중에 모델이나 레코드에 대한 변경이 아직 DB에 반영되지 않았을 수 있으며, 트랜잭션 내에서 생성된 모델/레코드가 DB에 없을 수도 있습니다. 리스너가 이런 모델에 의존할 경우, 큐 작업 처리 중 예기치 않은 에러가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by implementing the `ShouldQueueAfterCommit` interface on the listener class: -->
큐 연결 설정 파일의 `after_commit` 옵션이 `false`로 되어 있더라도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 해당 리스너는 모든 열린 트랜잭션이 커밋된 후 디스패치됩니다.

```
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
> 이러한 문제를 안전하게 해결하는 방법은 [queued jobs and database transactions](/docs/11.x/queues#jobs-and-database-transactions) 문서를 참고하시기 바랍니다.

<a name="handling-failed-jobs"></a>
<!-- ### Handling Failed Jobs -->
### Handling Failed Jobs

<!-- Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure: -->
때로는 큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐 워커가 허용하는 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. `failed` 메서드는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 인스턴스를 전달받습니다.

```
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
큐잉된 리스너에서 오류가 반복 발생할 경우, 무한으로 재시도하는 것을 방지하기 위해 시도 횟수나 재시도 허용 시간을 지정할 수 있습니다.

<!-- You may define a `$tries` property on your listener class to specify how many times the listener may be attempted before it is considered to have failed: -->
리스너 클래스에 `$tries` 속성을 정의하면, 리스너가 실패로 간주되기 전까지 몇 번까지 시도할지 정할 수 있습니다.

```
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
실패 전 최대 시도 횟수 대신, 언제까지 시도할 지 타임아웃(만료 시각)을 정하고 싶으면, 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
<!-- #### Specifying Queued Listener Backoff -->
#### Specifying Queued Listener Backoff

<!-- If you would like to configure how many seconds Laravel should wait before retrying a listener that has encountered an exception, you may do so by defining a `backoff` property on your listener class: -->
리스너에서 예외가 발생해 재시도가 필요할 때, Laravel이 몇 초 후에 다시 시도할지 지정하고 싶다면 리스너 클래스에 `backoff` 속성을 설정할 수 있습니다.
```

/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

<!-- If you require more complex logic for determining the listeners's backoff time, you may define a `backoff` method on your listener class: -->
리스너의 백오프 시간을 더 복잡한 방식으로 산출하고 싶다면, 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(): int
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
`backoff` 메서드에서 백오프 값의 배열을 반환하면 "지수(exponential)" 백오프를 쉽게 설정할 수도 있습니다. 아래 예시에서는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 시도가 더 남아 있다면 이후 모든 재시도는 10초씩 대기하게 됩니다.

```
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="dispatching-events"></a>

<!-- ## Dispatching Events -->
## Dispatching Events

<!-- To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor: -->
이벤트를 디스패치하려면, 해당 이벤트에서 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 이벤트에 적용할 때 사용할 수 있습니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트의 생성자로 전달됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Http\Controllers\Controller;
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
조건에 따라 이벤트를 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트를 작성할 때는 실제로 리스너가 실행되지 않더라도 특정 이벤트가 디스패치됐는지 확인(assert)할 수 있으면 편리합니다. Laravel의 [built-in testing helpers](#testing)를 사용하면 매우 쉽게 확인할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
<!-- ### Dispatching Events After Database Transactions -->
### Dispatching Events After Database Transactions

<!-- Sometimes, you may want to instruct Laravel to only dispatch an event after the active database transaction has committed. To do so, you may implement the `ShouldDispatchAfterCommit` interface on the event class. -->
때로는 데이터베이스의 현재 트랜잭션이 커밋된 이후에만 Laravel이 이벤트를 디스패치하도록 하고 싶을 수 있습니다. 이 경우에는 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

<!-- This interface instructs Laravel to not dispatch the event until the current database transaction is committed. If the transaction fails, the event will be discarded. If no database transaction is in progress when the event is dispatched, the event will be dispatched immediately: -->
이 인터페이스를 구현하면 Laravel은 현재 진행 중인 데이터베이스 트랜잭션이 커밋되기 전까지 이벤트를 디스패치하지 않습니다. 만약 트랜잭션이 실패하면, 이벤트는 폐기됩니다. 이벤트가 디스패치될 때 진행 중인 트랜잭션이 없다면 즉시 이벤트가 디스패치됩니다.

```
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

<a name="event-subscribers"></a>
<!-- ## Event Subscribers -->
## Event Subscribers

<a name="writing-event-subscribers"></a>
<!-- ### Writing Event Subscribers -->
### Writing Event Subscribers

<!-- Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which will be passed an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners: -->
이벤트 구독자는 하나의 클래스 안에서 여러 이벤트를 구독(subscribe)할 수 있는 클래스를 의미합니다. 즉, 여러 이벤트 처리 메서드를 하나의 클래스에서 정의할 수 있습니다. 구독자 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드에는 이벤트 디스패처 인스턴스가 전달됩니다. 전달된 디스패처에서 `listen` 메서드를 호출해 이벤트 리스너를 등록합니다.

```
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
이벤트 리스너 메서드가 구독자 클래스 내에 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하는 것이 좀 더 편리할 수 있습니다. Laravel은 이벤트 리스너를 등록할 때 구독자 클래스명을 자동으로 결정해줍니다.

```
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
구독자 클래스를 작성한 후, 해당 구독자의 핸들러 메서드들이 Laravel의 [event discovery conventions](#event-discovery)를 따르도록 정의되어 있다면 Laravel이 자동으로 등록해줍니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 사용해 구독자를 직접 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이 작업을 수행합니다.

```
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
이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트의 리스너를 실행시키지 않도록 Laravel에 지시하고 싶을 수 있습니다. 리스너의 코드는 직접적으로, 그리고 이벤트를 디스패치하는 코드와 별개로 테스트할 수 있기 때문입니다. 물론, 리스너 자체를 테스트할 때는 테스트에서 리스너 인스턴스를 생성해서 `handle` 메서드를 직접 호출해주면 됩니다.

<!-- Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods: -->
`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행을 방지하면서 테스트하고자 하는 코드가 실행된 후, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드를 이용해 애플리케이션에서 어떤 이벤트가 디스패치됐는지 확인할 수 있습니다.

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

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

<!-- You may pass a closure to the `assertDispatched` or `assertNotDispatched` methods in order to assert that an event was dispatched that passes a given "truth test". If at least one event was dispatched that passes the given truth test then the assertion will be successful: -->
`assertDispatched`나 `assertNotDispatched` 메서드에 클로저(익명 함수)를 전달하면, 해당 조건(truth test)에 부합하는 이벤트가 디스패치됐는지 확인할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 디스패치됐다면 assert 문은 통과합니다.

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

<!-- If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method: -->
특정 이벤트에 리스너가 바인딩(listen)되어 있는지만 단순히 확인하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 이벤트 리스너가 모두 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트에서 UUID를 생성하는 등 이벤트에 의존하는 모델 팩토리를 사용하는 경우, 팩토리를 사용한 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
<!-- ### Faking a Subset of Events -->
### Faking a Subset of Events

<!-- If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method: -->
특정 이벤트 리스너만 가짜로 처리하고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트 목록을 전달하면 됩니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([...]);
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
    $order->update([...]);
}
```

<!-- You may fake all events except for a set of specified events using the `except` method: -->
`except` 메서드를 사용하면 특정 이벤트를 제외한 나머지 모든 이벤트에 대해 가짜 처리를 할 수 있습니다.

```
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
<!-- ### Scoped Event Fakes -->
### Scoped Event Fakes

<!-- If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method: -->
테스트 코드의 특정 부분에서만 이벤트 리스너를 가짜로 처리하고 싶을 때는, `fakeFor` 메서드를 사용할 수 있습니다.

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

    // Events are dispatched as normal and observers will run ...
    $order->update([...]);
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

        // Events are dispatched as normal and observers will run ...
        $order->update([...]);
    }
}
```
