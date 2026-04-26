# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성](#generating-events-and-listeners)
- [이벤트와 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 발견](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리되는 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐 처리되는 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 Middleware](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [고유 이벤트 리스너](#unique-event-listeners)
        - [처리가 시작될 때까지 리스너를 고유하게 유지하기](#keeping-listeners-unique-until-processing-begins)
        - [고유 리스너 잠금](#unique-listener-locks)
    - [실패한 Job 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [이벤트 일부만 Fake 처리](#faking-a-subset-of-events)
    - [범위가 지정된 이벤트 Fake](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴 구현을 제공하여, 애플리케이션 안에서 발생하는 다양한 이벤트를 구독하고 수신할 수 있게 합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되며, 해당 리스너는 `app/Listeners`에 저장됩니다. 애플리케이션에서 이 디렉터리가 보이지 않아도 걱정하지 않아도 됩니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 부분을 서로 분리하는 좋은 방법입니다. 하나의 이벤트가 서로 의존하지 않는 여러 리스너를 가질 수 있기 때문입니다. 예를 들어 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶을 수 있습니다. 주문 처리 코드를 Slack 알림 코드와 직접 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시킬 수 있습니다. 그러면 리스너가 이 이벤트를 받아 Slack 알림을 전송하는 데 사용할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해 추가 인수 없이 `make:event` 및 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이렇게 하면 Laravel은 클래스 이름을 자동으로 묻고, 리스너를 생성할 때는 어떤 이벤트를 수신해야 하는지도 묻습니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 발견

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. Laravel이 `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 발견하면, 해당 메서드 시그니처에 타입 힌트로 지정된 이벤트의 이벤트 리스너로 그 메서드를 등록합니다.

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

PHP의 union 타입을 사용하면 여러 이벤트를 수신할 수 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리나 여러 디렉터리에 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 Laravel이 해당 디렉터리를 스캔하도록 지정할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용하여 비슷한 여러 디렉터리에서 리스너를 스캔할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션에서의 이벤트 자동 발견

애플리케이션 성능을 높이려면 `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 애플리케이션의 모든 리스너 매니페스트를 캐시해야 합니다. 일반적으로 이 명령어는 애플리케이션의 [배포 과정](/docs/master/deployment#optimization)의 일부로 실행해야 합니다. 프레임워크는 이 매니페스트를 사용하여 이벤트 등록 과정을 더 빠르게 처리합니다. `event:clear` 명령어를 사용하면 이벤트 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` facade를 사용하면 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드 안에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다.

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

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스로 정의합니다. 하지만 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드 안에서 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다.

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
#### 큐 처리 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 Laravel이 해당 리스너를 [큐](/docs/master/queues)를 사용해 실행하도록 지정할 수 있습니다.

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

큐 처리되는 Job과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐 처리되는 리스너의 실행 방식을 사용자 정의할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너의 실패를 처리하려면 `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 제공할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패의 원인이 된 `Throwable` 인스턴스를 받습니다.

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

`*` 문자를 와일드카드 파라미터로 사용하여 리스너를 등록할 수도 있습니다. 이를 통해 같은 리스너에서 여러 이벤트를 잡아낼 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을 받고, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/master/eloquent) 객체를 받는다고 가정해 보겠습니다.

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

보다시피 이 이벤트 클래스에는 로직이 없습니다. 이 클래스는 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너입니다. 이벤트에서 사용하는 `SerializesModels` trait는 [큐 처리되는 리스너](#queued-event-listeners)를 사용할 때처럼 PHP의 `serialize` 함수로 이벤트 객체가 직렬화되는 경우, 모든 Eloquent 모델을 적절하게 직렬화합니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

다음으로 예제 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `--event` 옵션과 함께 `make:listener` Artisan 명령어를 실행하면 적절한 이벤트 클래스를 자동으로 import하고, `handle` 메서드에 해당 이벤트를 타입 힌트로 지정합니다. `handle` 메서드 안에서는 이벤트에 응답하기 위해 필요한 어떤 작업이든 수행할 수 있습니다.

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
> 이벤트 리스너의 생성자에는 필요한 의존성을 타입 힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/master/container)를 통해 resolve되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

때로는 이벤트가 다른 리스너로 전파되지 않도록 중단하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐 처리되는 이벤트 리스너 (Queued Event Listeners)

리스너가 이메일 전송이나 HTTP 요청처럼 느린 작업을 수행한다면 리스너를 큐에 넣는 것이 유용할 수 있습니다. 큐 처리되는 리스너를 사용하기 전에 [큐를 설정](/docs/master/queues)하고 서버 또는 로컬 개발 환경에서 큐 워커를 시작해야 합니다.

리스너가 큐 처리되어야 함을 지정하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가합니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이 인터페이스가 현재 네임스페이스에 이미 import되어 있으므로 바로 사용할 수 있습니다.

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

이것으로 충분합니다. 이제 이 리스너가 처리하는 이벤트가 디스패치되면, 이벤트 dispatcher가 Laravel의 [큐 시스템](/docs/master/queues)을 사용하여 리스너를 자동으로 큐에 넣습니다. 큐가 리스너를 실행하는 동안 예외가 발생하지 않으면, 큐 처리된 Job은 처리가 끝난 뒤 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 사용자 정의

이벤트 리스너의 큐 연결, 큐 이름, 큐 지연 시간을 사용자 정의하려면 리스너 클래스에 `Connection`, `Queue`, `Delay` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Delay;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('listeners')]
#[Delay(60)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```
리스너의 큐 연결, 큐 이름, 지연 시간을 런타임에 정의하고 싶다면 리스너에 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다.

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
#### 조건에 따라 리스너 큐 처리하기

때로는 런타임에만 사용할 수 있는 일부 데이터를 기준으로 리스너를 큐에 넣을지 결정해야 할 수 있습니다. 이를 위해 리스너에 `shouldQueue` 메서드를 추가하여 리스너를 큐에 넣을지 판단할 수 있습니다. `shouldQueue` 메서드가 `false`를 반환하면 리스너는 큐에 들어가지 않습니다.

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
### 큐와 수동으로 상호작용하기

리스너 내부에 있는 큐 Job의 `delete` 및 `release` 메서드에 직접 접근해야 한다면 `Illuminate\Queue\InteractsWithQueue` trait를 사용하면 됩니다. 이 trait는 생성된 리스너에 기본적으로 import되어 있으며, 이러한 메서드에 접근할 수 있게 해 줍니다.
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
### 큐에 저장된 이벤트 리스너와 데이터베이스 트랜잭션

큐에 저장되는 리스너가 데이터베이스 트랜잭션 안에서 디스패치되면, 데이터베이스 트랜잭션이 커밋되기 전에 큐에서 먼저 처리될 수 있습니다. 이런 일이 발생하면 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 적용한 변경 사항이 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한 트랜잭션 안에서 생성한 모델이나 데이터베이스 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다. 리스너가 이러한 모델에 의존한다면, 큐 리스너를 디스패치한 job이 처리될 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`로 설정되어 있더라도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 특정 큐 리스너가 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 뒤에 디스패치되어야 함을 지정할 수 있습니다.

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
> 이러한 문제를 처리하는 방법에 대해 더 자세히 알아보려면 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 확인하십시오.

<a name="queued-listener-middleware"></a>
### 큐 리스너 Middleware

큐 리스너도 [job Middleware](/docs/master/queues#job-middleware)를 사용할 수 있습니다. job Middleware를 사용하면 큐 리스너 실행 전후에 사용자 정의 로직을 감쌀 수 있어, 리스너 자체의 반복 코드를 줄일 수 있습니다. job Middleware를 만든 뒤에는 리스너의 `middleware` 메서드에서 반환하여 리스너에 연결할 수 있습니다.

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
#### 암호화된 큐 리스너

Laravel은 [암호화](/docs/master/encryption)를 통해 큐 리스너 데이터의 개인정보 보호와 무결성을 보장할 수 있게 해줍니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 클래스에 추가되면, Laravel은 리스너를 큐에 넣기 전에 자동으로 암호화합니다.

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
### 고유 이벤트 리스너

> [!WARNING]
> 고유 리스너에는 [잠금](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 잠금을 지원합니다.

때로는 특정 리스너의 인스턴스가 어느 시점에도 큐에 하나만 존재하도록 보장하고 싶을 수 있습니다. 이를 위해 리스너 클래스에 `ShouldBeUnique` 인터페이스를 구현할 수 있습니다.

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

위 예시에서 `AcquireProductKey` 리스너는 고유합니다. 따라서 동일한 리스너의 다른 인스턴스가 이미 큐에 있고 아직 처리가 끝나지 않았다면, 이 리스너는 큐에 추가되지 않습니다. 이렇게 하면 라이선스가 짧은 시간 안에 여러 번 저장되더라도 각 라이선스에 대해 제품 키가 하나만 발급됩니다.

특정한 경우에는 리스너를 고유하게 만드는 특정 "키"를 정의하거나, 리스너가 더 이상 고유 상태로 유지되지 않는 제한 시간을 지정하고 싶을 수 있습니다. 이를 위해 리스너 클래스에 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의할 수 있습니다. 메서드는 이벤트 인스턴스를 받으므로, 이벤트 데이터를 사용해 반환값을 구성할 수 있습니다.

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

위 예시에서 `AcquireProductKey` 리스너는 라이선스 ID별로 고유합니다. 따라서 같은 라이선스에 대한 이 리스너의 새로운 디스패치는 기존 리스너 처리가 완료될 때까지 무시됩니다. 이렇게 하면 같은 라이선스에 대해 중복된 제품 키가 발급되는 일을 방지할 수 있습니다. 또한 기존 리스너가 1시간 안에 처리되지 않으면 고유 잠금이 해제되고, 같은 고유 키를 가진 다른 리스너를 큐에 추가할 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 이벤트를 디스패치한다면, Laravel이 리스너의 고유 여부를 정확히 판단할 수 있도록 모든 서버가 동일한 중앙 캐시 서버와 통신하고 있는지 확인해야 합니다.

<a name="keeping-listeners-unique-until-processing-begins"></a>
#### 처리가 시작될 때까지 리스너를 고유하게 유지하기

기본적으로 고유 리스너는 처리를 완료하거나 모든 재시도 횟수를 소진해 실패한 뒤에 "잠금 해제"됩니다. 하지만 리스너가 처리되기 직전에 즉시 잠금 해제되기를 원하는 상황도 있을 수 있습니다. 이를 위해 리스너는 `ShouldBeUnique` contract 대신 `ShouldBeUniqueUntilProcessing` contract를 구현해야 합니다.

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
#### 고유 리스너 잠금

내부적으로 `ShouldBeUnique` 리스너가 디스패치되면, Laravel은 `uniqueId` 키로 [잠금](/docs/master/cache#atomic-locks)을 획득하려고 시도합니다. 잠금이 이미 보유 중이면 리스너는 디스패치되지 않습니다. 이 잠금은 리스너가 처리를 완료하거나 모든 재시도 횟수를 소진해 실패하면 해제됩니다. 기본적으로 Laravel은 이 잠금을 얻기 위해 기본 캐시 드라이버를 사용합니다. 하지만 잠금을 획득할 때 다른 드라이버를 사용하고 싶다면, 사용할 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

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
> 리스너의 동시 처리를 제한하기만 하면 된다면, 대신 [WithoutOverlapping](/docs/master/queues#preventing-job-overlaps) job Middleware를 사용하십시오.

<a name="handling-failed-jobs"></a>
### 실패한 Job 처리하기

때로는 큐 이벤트 리스너가 실패할 수 있습니다. 큐 리스너가 큐 워커에 정의된 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. `failed` 메서드는 이벤트 인스턴스와 실패를 일으킨 `Throwable`을 받습니다.

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
#### 큐 리스너의 최대 시도 횟수 지정하기

큐 리스너 중 하나에서 오류가 발생한다면, 대개 무기한으로 계속 재시도되기를 원하지 않을 것입니다. 따라서 Laravel은 리스너를 몇 번까지 또는 얼마나 오랫동안 시도할 수 있는지 지정하는 여러 방법을 제공합니다.

리스너가 실패한 것으로 간주되기 전에 몇 번까지 시도할 수 있는지 지정하려면 리스너 클래스에 `Tries` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(5)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    // ...
}
```

리스너가 실패하기 전에 몇 번까지 시도할 수 있는지 정의하는 대신, 리스너를 더 이상 시도하지 않아야 하는 시점을 정의할 수도 있습니다. 이렇게 하면 주어진 시간 범위 안에서는 리스너를 횟수 제한 없이 시도할 수 있습니다. 리스너를 더 이상 시도하지 않아야 하는 시점을 정의하려면 리스너 클래스에 `retryUntil` 메서드를 추가하십시오. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

`retryUntil`과 `tries`가 모두 정의되어 있으면, Laravel은 `retryUntil` 메서드를 우선합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 Backoff 지정하기

예외가 발생한 리스너를 재시도하기 전에 Laravel이 몇 초 동안 기다려야 하는지 설정하고 싶다면, 리스너 클래스에 `Backoff` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

리스너의 backoff 시간을 결정하는 데 더 복잡한 로직이 필요하다면, 리스너 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

`backoff` 메서드에서 backoff 값의 배열을 반환하면 "지수적" backoff를 쉽게 설정할 수 있습니다. 이 예시에서는 첫 번째 재시도 지연 시간이 1초, 두 번째 재시도는 5초, 세 번째 재시도는 10초이며, 이후에도 남은 시도가 있다면 각 재시도마다 10초가 됩니다.

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
#### 큐 리스너의 최대 예외 횟수 지정하기

때로는 큐 리스너를 여러 번 시도할 수는 있지만, 재시도가 `release` 메서드로 직접 해제되어 발생한 것이 아니라 처리되지 않은 예외가 일정 횟수 발생해 트리거된 경우에는 실패하도록 지정하고 싶을 수 있습니다. 이를 위해 리스너 클래스에 `Tries` 및 `MaxExceptions` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(25)]
#[MaxExceptions(3)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

이 예시에서 리스너는 최대 25번까지 재시도됩니다. 하지만 리스너에서 처리되지 않은 예외가 세 번 발생하면 리스너는 실패합니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 Timeout 지정하기

대부분의 경우 큐 리스너가 대략 얼마나 오래 걸릴지 알고 있습니다. 이러한 이유로 Laravel은 "timeout" 값을 지정할 수 있게 해줍니다. 리스너가 timeout 값으로 지정된 초보다 더 오래 처리되고 있으면, 해당 리스너를 처리하던 워커는 오류와 함께 종료됩니다. 리스너가 실행될 수 있는 최대 초 수는 리스너 클래스에 `Timeout` 속성을 사용해 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```
리스너가 타임아웃될 때 실패로 표시되어야 함을 나타내려면, 리스너 클래스에 `FailOnTimeout` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치하기 (Dispatching Events)

이벤트를 디스패치하려면 이벤트에서 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 통해 이벤트에서 사용할 수 있습니다. `dispatch` 메서드에 전달된 모든 인수는 이벤트의 생성자로 전달됩니다.

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

조건에 따라 이벤트를 디스패치하고 싶다면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트할 때는 특정 이벤트가 디스패치되었는지만 확인하고, 실제 리스너는 실행하지 않도록 처리하면 도움이 됩니다. Laravel의 [내장 테스트 헬퍼](#testing)를 사용하면 매우 쉽게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치하기

때로는 활성 데이터베이스 트랜잭션이 커밋된 이후에만 Laravel이 이벤트를 디스패치하도록 지시하고 싶을 수 있습니다. 이를 위해 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스는 현재 데이터베이스 트랜잭션이 커밋되기 전까지 이벤트를 디스패치하지 않도록 Laravel에 지시합니다. 트랜잭션이 실패하면 이벤트는 폐기됩니다. 이벤트가 디스패치될 때 진행 중인 데이터베이스 트랜잭션이 없다면 이벤트는 즉시 디스패치됩니다.

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
### 이벤트 지연하기

지연된 이벤트를 사용하면 특정 코드 블록이 완료된 뒤에 모델 이벤트를 디스패치하고 이벤트 리스너를 실행하도록 미룰 수 있습니다. 이는 이벤트 리스너가 실행되기 전에 관련 레코드가 모두 생성되었음을 보장해야 할 때 특히 유용합니다.

이벤트를 지연하려면 `Event::defer()` 메서드에 클로저를 전달합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 안에서 트리거된 모든 이벤트는 클로저 실행이 끝난 뒤 디스패치됩니다. 이를 통해 이벤트 리스너는 지연 실행 중에 생성된 모든 관련 레코드에 접근할 수 있습니다. 클로저 안에서 예외가 발생하면 지연된 이벤트는 디스패치되지 않습니다.

특정 이벤트만 지연하려면 `defer` 메서드의 두 번째 인수로 이벤트 배열을 전달합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 구독자 클래스 내부에서 여러 이벤트를 구독할 수 있는 클래스입니다. 이를 통해 하나의 클래스 안에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자는 이벤트 디스패처 인스턴스를 받는 `subscribe` 메서드를 정의해야 합니다. 전달된 디스패처에서 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다.

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

이벤트 리스너 메서드가 구독자 자체에 정의되어 있다면, 구독자의 `subscribe` 메서드에서 이벤트와 메서드 이름으로 이루어진 배열을 반환하는 방식이 더 편리할 수 있습니다. Laravel은 이벤트 리스너를 등록할 때 구독자의 클래스명을 자동으로 확인합니다.

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
### 이벤트 구독자 등록하기

구독자를 작성한 뒤, 해당 구독자가 Laravel의 [이벤트 탐색 규칙](#event-discovery)을 따른다면 Laravel은 구독자 안의 핸들러 메서드를 자동으로 등록합니다. 그렇지 않은 경우에는 `Event` 파사드의 `subscribe` 메서드를 사용하여 구독자를 수동으로 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드 안에서 수행합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때는 Laravel이 실제로 이벤트 리스너를 실행하지 않도록 지시하고 싶을 수 있습니다. 리스너 코드는 해당 이벤트를 디스패치하는 코드와 별도로 직접 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트하려면 테스트 안에서 리스너 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 막고, 테스트 대상 코드를 실행한 뒤, 애플리케이션에서 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다.

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

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하면, 주어진 "참 여부 검사"를 통과하는 이벤트가 디스패치되었는지 검증할 수 있습니다. 주어진 참 여부 검사를 통과하는 이벤트가 하나 이상 디스패치되었다면 검증은 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트를 어떤 이벤트 리스너가 수신하고 있는지만 간단히 검증하고 싶다면 `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 뒤에는 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 모델의 `creating` 이벤트에서 UUID를 생성하는 경우처럼 이벤트에 의존하는 모델 팩토리를 테스트에서 사용한다면, 팩토리를 사용한 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 Fake 처리하기

특정 이벤트 집합에 대해서만 이벤트 리스너를 Fake 처리하고 싶다면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 전달할 수 있습니다.

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

`except` 메서드를 사용하면 지정한 이벤트 집합을 제외한 모든 이벤트를 Fake 처리할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위가 제한된 이벤트 Fake

테스트의 일부 구간에서만 이벤트 리스너를 Fake 처리하고 싶다면 `fakeFor` 메서드를 사용할 수 있습니다.

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
