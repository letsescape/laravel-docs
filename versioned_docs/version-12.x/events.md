# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 발견](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐에 있는 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호 작용](#manually-interacting-with-the-queue)
    - [대기 중인 이벤트 리스너 및 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐에 있는 리스너 미들웨어](#queued-listener-middleware)
    - [암호화 대기 리스너](#encrypted-queued-listeners)
    - [고유 이벤트 리스너](#unique-event-listeners)
        - [처리가 시작될 때까지 리스너를 고유하게 유지](#keeping-listeners-unique-until-processing-begins)
        - [고유한 리스너 잠금](#unique-listener-locks)
    - [작업 처리 실패](#handling-failed-jobs)
- [디스패치 이벤트](#dispatching-events)
    - [데이터베이스 트랜잭션 후 디스패치 이벤트](#dispatching-events-after-database-transactions)
    - [이벤트 연기](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성 중](#writing-event-subscribers)
    - [이벤트 가입자 등록 중](#registering-event-subscribers)
- [테스트](#testing)
    - [이벤트의 하위 집합 위조](#faking-a-subset-of-events)
    - [범위가 지정된 이벤트 가짜](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 관찰자 패턴 구현을 제공하므로 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 수신할 수 있습니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되고 해당 리스너는 `app/Listeners`에 저장됩니다. Artisan 콘솔 명령을 사용하여 이벤트 및 리스너를 생성할 때 이러한 디렉토리가 생성되므로 애플리케이션에 이러한 디렉토리가 표시되지 않더라도 걱정하지 마십시오.

이벤트는 단일 이벤트가 서로 의존하지 않는 여러 리스너를 가질 수 있으므로 애플리케이션의 다양한 측면을 분리하는 훌륭한 방법으로 사용됩니다. 예를 들어, 주문이 디스패치될 때마다 사용자에게 Slack 알림을 보내려고 할 수 있습니다. 주문 처리 코드를 Slack 알림 코드에 연결하는 대신 리스너가 Slack 알림을 디스패치에 수신하고 사용할 수 있는 `App\Events\OrderShipped` 이벤트를 발생시킬 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성 (Generating Events and Listeners)

이벤트 및 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령을 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해 추가 인수 없이 `make:event` 및 `make:listener` Artisan 명령을 호출할 수도 있습니다. 그렇게 하면 Laravel가 자동으로 클래스 이름을 묻는 메시지를 표시하며, 리스너를 생성할 때 수신해야 하는 이벤트는 다음과 같습니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 발견

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

리스너를 다른 디렉터리나 여러 디렉터리 내에 저장하려는 경우 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 해당 디렉터리를 검색하도록 Laravel에 지시할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용하여 여러 유사한 디렉터리에서 리스너를 검색할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령을 사용하면 애플리케이션 내에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 중 이벤트 검색

애플리케이션 속도를 높이려면 `optimize` 또는 `event:cache` Artisan 명령을 사용하여 애플리케이션의 모든 리스너 매니페스트를 캐시해야 합니다. 일반적으로 이 명령은 애플리케이션의 [배포 프로세스](/docs/12.x/deployment#optimization)의 일부로 실행되어야 합니다. 이 매니페스트는 프레임워크에서 이벤트 등록 프로세스 속도를 높이는 데 사용됩니다. `event:clear` 명령을 사용하여 이벤트 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

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

`event:list` 명령을 사용하면 애플리케이션 내에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

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
#### 큐에 넣을 수 있는 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때 Laravel에 [큐](/docs/12.x/queues)를 사용하여 리스너를 실행하도록 지시하기 위해 `Illuminate\Events\queueable` 함수 내에서 리스너 클로저를 래핑할 수 있습니다.

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

큐에 있는 작업과 마찬가지로 `onConnection`, `onQueue` 및 `delay` 메서드를 사용하여 큐에 있는 리스너의 실행을 사용자 지정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

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
#### 와일드카드 이벤트 리스너

또한 `*` 문자를 와일드카드 매개변수로 사용하여 리스너를 등록하면 동일한 리스너에서 여러 이벤트를 포착할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을 받고 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

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

보시다시피 이 이벤트 클래스에는 로직이 없습니다. 구매한 `App\Models\Order` 인스턴스용 컨테이너입니다. 이벤트에서 사용하는 `SerializesModels` 특성은 [큐에 있는 리스너](#queued-event-listeners)를 사용할 때와 같이 PHP의 `serialize` 기능을 사용하여 이벤트 개체가 직렬화되는 경우 모든 Eloquent 모델을 우아하게 직렬화합니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

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
> 이벤트 리스너는 생성자에 필요한 종속성을 유형 힌트할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 확인되므로 종속성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지

때로는 이벤트가 다른 리스너로 전파되는 것을 중지하고 싶을 수도 있습니다. 리스너의 `handle` 메소드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐에 있는 이벤트 리스너 (Queued Event Listeners)

리스너가 이메일을 보내거나 HTTP 요청을 하는 등 느린 작업을 수행하는 경우 리스너를 큐에 추가하는 것이 도움이 될 수 있습니다. 대기 중인 리스너를 사용하기 전에 [큐 구성](/docs/12.x/queues)을 확인하고 서버 또는 로컬 개발 환경에서 큐 워커를 시작하세요.

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

그게 다야! 이제 이 리스너가 처리하는 이벤트가 디스패치이면 리스너는 Laravel의 [큐 시스템](/docs/12.x/queues)을 사용하여 이벤트 디스패처에 의해 자동으로 큐에 추가됩니다. 리스너가 큐에 의해 실행될 때 예외가 발생하지 않으면 대기 중인 작업은 처리가 완료된 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름 및 지연 사용자 지정

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
#### 조건부 큐 리스너

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
### 큐와 수동으로 상호 작용

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
### 대기 중인 이벤트 리스너 및 데이터베이스 트랜잭션

큐에 있는 리스너가 데이터베이스 트랜잭션 내의 디스패치인 경우 데이터베이스 트랜잭션이 커밋되기 전에 큐에 의해 처리될 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델 또는 데이터베이스 레코드에 대해 수행한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델 또는 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다. 리스너가 이러한 모델에 의존하는 경우 큐에 있는 디스패치인 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

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
> 이러한 문제를 해결하는 방법에 대해 자세히 알아보려면 [큐에 있는 작업 및 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions)에 관한 설명서를 검토하세요.

<a name="queued-listener-middleware"></a>
### 큐에 있는 리스너 미들웨어

대기 중인 리스너는 [작업 미들웨어](/docs/12.x/queues#job-middleware)도 활용할 수 있습니다. 작업 미들웨어를 사용하면 큐에 있는 리스너 실행에 대한 사용자 지정 논리를 래핑하여 리스너 자체의 상용구를 줄일 수 있습니다. 작업 미들웨어를 생성한 후 리스너의 `middleware` 메서드에서 반환하여 리스너에 연결할 수 있습니다.

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
#### 암호화된 대기 리스너

Laravel을 사용하면 [암호화](/docs/12.x/encryption)를 통해 대기 중인 리스너 데이터의 개인정보 보호와 무결성을 보장할 수 있습니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 클래스에 추가되면 Laravel는 리스너를 큐에 푸시하기 전에 자동으로 암호화합니다.

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
### 독특한 이벤트 리스너

> [!WARNING]
> 고유한 리스너에는 [잠금](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자 잠금을 지원합니다.

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

위의 예에서 `AcquireProductKey` 리스너는 고유합니다. 따라서 리스너의 다른 인스턴스가 이미 큐에 있고 처리가 완료되지 않은 경우 리스너는 큐에 추가되지 않습니다. 이렇게 하면 라이선스가 빠르게 연속해서 여러 번 저장되더라도 각 라이선스에 대해 하나의 제품 키만 획득됩니다.

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

위의 예에서 `AcquireProductKey` 리스너는 라이선스 ID별로 고유합니다. 따라서 동일한 라이선스에 대한 리스너의 새로운 디스패치는 기존 리스너의 처리가 완료될 때까지 무시됩니다. 이렇게 하면 동일한 라이선스에 대해 중복된 제품 키를 획득하는 것을 방지할 수 있습니다. 또한 기존 리스너가 1시간 이내에 처리되지 않으면 고유 잠금이 해제되고 동일한 고유 키를 가진 다른 리스너가 대기할 수 있습니다.

> [!WARNING]
> 여러 웹 서버 또는 컨테이너에서 애플리케이션 디스패치 이벤트를 사용하는 경우 Laravel가 리스너가 고유한지 정확하게 확인할 수 있도록 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야 합니다.

<a name="keeping-listeners-unique-until-processing-begins"></a>
#### 처리가 시작될 때까지 리스너를 고유하게 유지

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
#### 고유한 리스너 잠금 장치

뒤에서는 `ShouldBeUnique` 리스너가 디스패치일 때 Laravel가 `uniqueId` 키를 사용하여 [잠금](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 잠금이 이미 유지된 경우 리스너는 디스패치가 아닙니다. 이 잠금은 리스너가 처리를 완료하거나 모든 재시도 시도에 실패하면 해제됩니다. 기본적으로 Laravel는 기본 캐시 드라이버를 사용하여 이 잠금을 획득합니다. 그러나 잠금 획득을 위해 다른 드라이버를 사용하려는 경우 사용해야 하는 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

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
### 처리 실패 작업

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
#### 대기 중인 리스너 최대 시도 횟수 지정

대기 중인 리스너 중 하나에 오류가 발생한 경우 무한정 계속 재시도하는 것을 원하지 않을 것입니다. 따라서 Laravel는 리스너를 시도할 수 있는 횟수 또는 기간을 지정하는 다양한 방법을 제공합니다.

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

`retryUntil` 및 `tries`가 모두 정의된 경우 Laravel는 `retryUntil` 메서드에 우선 순위를 부여합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 대기 중인 리스너 백오프 지정

예외가 발생한 리스너를 재시도하기 전에 Laravel가 기다려야 하는 시간(초)을 구성하려면 리스너 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

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
#### 대기 중인 리스너 최대 예외 지정

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

이 예에서는 리스너가 최대 25번까지 재시도됩니다. 그러나 리스너에서 처리되지 않은 세 가지 예외가 발생하면 리스너가 실패합니다.

<a name="specifying-queued-listener-timeout"></a>
#### 대기 중인 리스너 시간 초과 지정

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
## 디스패치 이벤트 (Dispatching Events)

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

이벤트를 조건부로 디스패치하려는 경우 `dispatchIf` 및 `dispatchUnless` 방법을 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트할 때 실제로 리스너를 트리거하지 않고 특정 이벤트가 디스패치였다고 주장하는 것이 도움이 될 수 있습니다. Laravel의 [내장 테스트 도우미](#testing)를 사용하면 문제가 해결됩니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 디스패치 이벤트

때로는 활성 데이터베이스 트랜잭션이 커밋된 후 디스패치 및 이벤트만 수행하도록 Laravel에 지시할 수도 있습니다. 이렇게 하려면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현할 수 있습니다.

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
### 이벤트 연기

지연된 이벤트를 사용하면 특정 코드 블록이 완료될 때까지 모델 이벤트의 디스패치 및 이벤트 리스너의 실행을 지연할 수 있습니다. 이는 이벤트 리스너가 트리거되기 전에 모든 관련 레코드가 생성되었는지 확인해야 할 때 특히 유용합니다.

이벤트를 연기하려면 `Event::defer()` 메서드에 대한 클로저를 제공하세요.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내에서 트리거된 모든 이벤트는 클로저가 실행된 후 디스패치가 됩니다. 이렇게 하면 이벤트 리스너가 지연된 실행 중에 생성된 모든 관련 레코드에 액세스할 수 있습니다. 클로저 내에서 예외가 발생하면 지연된 이벤트는 디스패치가 아닙니다.

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
## 이벤트 가입자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 쓰기

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
### 이벤트 가입자 등록

구독자를 작성한 후 Laravel는 Laravel의 [이벤트 검색 규칙](#event-discovery)을 따르는 경우 구독자 내에 처리기 메서드를 자동으로 등록합니다. 그렇지 않으면 `Event` 파사드의 `subscribe` 메소드를 사용하여 구독자를 수동으로 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션 `AppServiceProvider`의 `boot` 메서드 내에서 수행되어야 합니다.

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
## 테스트 (Testing)

디스패치 이벤트 코드를 테스트할 때 Laravel에 이벤트의 리스너를 실제로 실행하지 않도록 지시할 수 있습니다. 왜냐하면 리스너의 코드는 해당 디스패치 코드와 별도로 직접 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트하려면 리스너 인스턴스를 인스턴스화하고 테스트에서 `handle` 메서드를 직접 호출할 수 있습니다.

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

이벤트가 주어진 "진실 테스트"를 통과한 디스패치였다고 주장하기 위해 `assertDispatched` 또는 `assertNotDispatched` 메소드에 클로저를 전달할 수 있습니다. 적어도 하나의 이벤트가 주어진 진리 테스트를 통과하는 디스패치라면 어설션은 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

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
### 이벤트의 하위 집합 위조

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

`except` 메소드를 사용하여 지정된 이벤트 세트를 제외한 모든 이벤트를 위조할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위가 지정된 이벤트 가짜

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
