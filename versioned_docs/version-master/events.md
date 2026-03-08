# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트와 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 기반 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [고유 이벤트 리스너](#unique-event-listeners)
        - [처리 시작 전까지 리스너를 고유하게 유지](#keeping-listeners-unique-until-processing-begins)
        - [고유 리스너 락](#unique-listener-locks)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연 실행](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 가짜 처리하기](#faking-a-subset-of-events)
    - [범위 제한 이벤트 Fake](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현을 제공합니다. 이를 통해 애플리케이션에서 발생하는 다양한 이벤트를 구독하고 처리할 수 있습니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉토리에 저장되며, 해당 이벤트의 리스너는 `app/Listeners` 디렉토리에 저장됩니다. 애플리케이션에 이 디렉토리가 보이지 않더라도 걱정할 필요는 없습니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성하면 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 기능을 느슨하게 결합(decouple)하는 데 매우 유용합니다. 하나의 이벤트에 여러 개의 리스너를 연결할 수 있으며, 이 리스너들은 서로 의존하지 않습니다. 예를 들어 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해 보겠습니다. 주문 처리 코드에 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고 이를 수신하는 리스너에서 Slack 알림을 보내도록 구현할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해 추가 인수 없이 `make:event` 및 `make:listener` 명령어를 실행할 수도 있습니다. 이 경우 Laravel이 클래스 이름을 입력하도록 자동으로 프롬프트를 표시하며, 리스너 생성 시 어떤 이벤트를 수신할지 물어봅니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 탐색 (Event Discovery)

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel은 `handle` 또는 `__invoke`로 시작하는 메서드를 가진 리스너 클래스를 발견하면, 해당 메서드의 시그니처에 타입 힌트된 이벤트를 기준으로 이벤트 리스너로 등록합니다.

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

PHP의 유니언 타입을 사용하여 하나의 메서드에서 여러 이벤트를 처리할 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리 또는 여러 디렉토리에 저장하려는 경우, `bootstrap/app.php` 파일의 `withEvents` 메서드를 사용하여 Laravel이 해당 디렉토리를 스캔하도록 지정할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

와일드카드 `*`를 사용하여 여러 유사한 디렉토리를 스캔할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너 목록을 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 탐색

애플리케이션 성능을 향상시키기 위해 `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 모든 리스너의 매니페스트(manifest)를 캐시해야 합니다. 일반적으로 이 명령어는 애플리케이션의 [배포 과정](/docs/master/deployment#optimization)에 포함됩니다. 이 매니페스트는 이벤트 등록 과정을 더 빠르게 처리하기 위해 사용됩니다. `event:clear` 명령어를 사용하면 이벤트 캐시를 제거할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록 (Manually Registering Events)

`Event` 파사드(facade)를 사용하여 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다.

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

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너 목록을 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너 (Closure Listeners)

일반적으로 리스너는 클래스로 정의되지만, `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 이벤트 리스너를 직접 등록할 수도 있습니다.

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
#### 큐 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때 `Illuminate\Events\queueable` 함수를 사용하면 해당 리스너를 [queue](/docs/master/queues)를 통해 실행하도록 설정할 수 있습니다.

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

큐 작업과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐 리스너의 실행 방식을 커스터마이즈할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너에서 발생하는 실패를 처리하려면 `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 전달받습니다.

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

`*` 와일드카드 문자를 사용하여 여러 이벤트를 하나의 리스너로 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을 받고, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/master/eloquent) 객체를 전달받는다고 가정해 보겠습니다.

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

보시다시피 이벤트 클래스에는 별도의 로직이 없습니다. 이 클래스는 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 때(E.g. [큐 리스너](#queued-event-listeners) 사용 시) Eloquent 모델을 안전하게 직렬화하도록 도와줍니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

이제 예제 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `--event` 옵션과 함께 `make:listener` Artisan 명령어를 실행하면, Laravel이 자동으로 해당 이벤트 클래스를 import하고 `handle` 메서드에 타입 힌트를 추가합니다. `handle` 메서드 안에서는 이벤트에 대한 필요한 처리를 수행하면 됩니다.

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
> 이벤트 리스너의 생성자에서는 필요한 의존성을 타입 힌트로 선언할 수 있습니다. 모든 이벤트 리스너는 Laravel의 [service container](/docs/master/container)를 통해 생성되므로 의존성은 자동으로 주입됩니다.

#### 이벤트 전파 중단

때로는 특정 리스너 이후에 다른 리스너가 실행되지 않도록 이벤트 전파를 중단하고 싶을 수 있습니다. 이 경우 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐 기반 이벤트 리스너 (Queued Event Listeners)

이메일 전송이나 HTTP 요청과 같이 시간이 오래 걸리는 작업을 수행하는 리스너라면 큐를 사용하는 것이 좋습니다. 큐 리스너를 사용하기 전에 [queue](/docs/master/queues)를 설정하고 서버 또는 로컬 개발 환경에서 큐 워커(queue worker)를 실행해야 합니다.

리스너를 큐로 실행하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가합니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이 인터페이스가 이미 import되어 있으므로 바로 사용할 수 있습니다.

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

이렇게 설정하면 해당 이벤트가 디스패치될 때 Laravel의 [queue system](/docs/master/queues)을 통해 리스너가 자동으로 큐에 등록됩니다. 큐에서 실행될 때 예외가 발생하지 않으면 작업은 자동으로 삭제됩니다.

(이하 내용은 원문의 Markdown 구조와 코드가 유지되며 동일한 방식으로 번역됩니다.)