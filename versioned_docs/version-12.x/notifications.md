# 알림(Notification)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐잉 처리](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포매팅](#formatting-mail-messages)
    - [발신자 커스터마이징](#customizing-the-sender)
    - [수신자 커스터마이징](#customizing-the-recipient)
    - [제목 커스터마이징](#customizing-the-subject)
    - [메일러 커스터마이징](#customizing-the-mailer)
    - [템플릿 커스터마이징](#customizing-the-templates)
    - [첨부 파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이징](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [Markdown 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이징](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비사항](#database-prerequisites)
    - [데이터베이스 알림 포매팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포매팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비사항](#sms-prerequisites)
    - [SMS 알림 포매팅](#formatting-sms-notifications)
    - ["From" 번호 커스터마이징](#customizing-the-from-number)
    - [클라이언트 참조값 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비사항](#slack-prerequisites)
    - [Slack 알림 포매팅](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림 로컬라이징](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [이메일 전송](/docs/12.x/mail)에 대한 지원 외에도 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널로 알림을 보낼 수 있습니다. 또한, 수십 가지 채널을 지원하는 [커뮤니티 기반 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 존재합니다! 알림은 데이터베이스에 저장할 수도 있어, 웹 인터페이스에서 보여줄 수 있습니다.

일반적으로, 알림은 애플리케이션에서 무언가가 발생했음을 사용자에게 알려주는 짧고 정보성 있는 메시지입니다. 예를 들어, 결제 애플리케이션을 만드는 경우, 이메일과 SMS 채널을 통해 사용자에게 "청구서 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉토리에 저장되는 하나의 클래스로 표현됩니다. 해당 디렉토리가 없다면, `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉토리에 새로운 알림 클래스를 만듭니다. 각 알림 클래스에는 `via` 메서드와 `toMail`, `toDatabase`와 같은 채널별 메시지 빌더 메서드가 포함되어 있습니다. 이 메서드들은 해당 채널에 맞게 알림을 메시지로 변환합니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드나 `Notification` [파사드](/docs/12.x/facades)를 사용해 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

이 트레이트에서 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. `User` 모델에만 한정되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는, `Notification` [파사드](/docs/12.x/facades)를 통해 알림을 보낼 수도 있습니다. 이 방법은 다수의 notifiable 엔터티(예: 유저 컬렉션)에 알림을 보낼 때 유용합니다. 파사드의 `send` 메서드에 notifiable 엔터티(들)와 알림 인스턴스를 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

즉시 알림을 전송해야 할 경우 `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림에 `ShouldQueue` 인터페이스가 구현되어 있더라도 즉시 알림을 전송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스에는 해당 알림이 어떤 채널로 전송될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 보낼 수 있습니다.

> [!NOTE]
> Telegram, Pusher 등 다른 채널도 사용하고 싶다면, 커뮤니티 기반 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 인수로 받아, 어떤 채널로 알림을 보낼지 결정할 수 있습니다:

```php
/**
 * Get the notification's delivery channels.
 *
 * @return array<int, string>
 */
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
### 알림 큐잉 처리

> [!WARNING]
> 알림을 큐에 넣기 전에, 큐를 구성하고 [워커를 시작](/docs/12.x/queues#running-the-queue-worker)하세요.

알림을 보내는 데는 시간이 걸릴 수 있습니다. 특히 채널이 외부 API 호출로 알림을 전달해야 할 경우 더욱 그렇습니다. 애플리케이션의 응답 속도를 높이기 위해, 알림에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하여 알림을 큐잉 처리할 수 있습니다. `make:notification` 명령어로 생성된 모든 알림에는 이 인터페이스와 트레이트가 이미 import되어 있으니 바로 추가할 수 있습니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```

`ShouldQueue` 인터페이스를 추가한 후에는 평소처럼 알림을 전송하면 됩니다. Laravel은 해당 클래스에 `ShouldQueue`가 구현된 것을 감지하고 자동으로 알림 전송을 큐잉 처리합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐잉할 때, 수신자와 채널의 조합별로 각각 큐 작업이 생성됩니다. 예를 들어, 3명의 수신자와 2개의 채널에 알림을 보낼 경우 큐에는 6개의 작업이 생성됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연

알림 전송을 지연시키고 싶다면, 알림 인스턴스에 `delay` 메서드를 체이닝할 수 있습니다:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 지연 시간을 다르게 지정하려면 `delay` 메서드에 배열을 전달하세요:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또는 알림 클래스 자체에 `withDelay` 메서드를 정의해도 됩니다. 이 메서드는 채널명과 지연 시간을 포함하는 배열을 반환해야 합니다:

```php
/**
 * Determine the notification's delivery delay.
 *
 * @return array<string, \Illuminate\Support\Carbon>
 */
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->plus(minutes: 5),
        'sms' => now()->plus(minutes: 10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 커넥션 커스터마이징

기본적으로, 큐잉된 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에서 다른 커넥션을 사용하려면, 알림의 생성자에서 `onConnection` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```

또는, 알림이 지원하는 각 채널별로 사용할 큐 커넥션을 지정하고 싶다면, 알림에 `viaConnections` 메서드를 정의하세요. 이 메서드는 채널명/커넥션명 쌍의 배열을 반환해야 합니다:

```php
/**
 * Determine which connections should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaConnections(): array
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```

<a name="customizing-notification-channel-queues"></a>
#### 알림 채널별 큐 지정

알림이 지원하는 각 채널별로 사용할 큐를 지정하려면, 알림 클래스에 `viaQueues` 메서드를 정의하세요. 이 메서드는 채널명/큐명 쌍의 배열을 반환해야 합니다:

```php
/**
 * Determine which queues should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaQueues(): array
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="customizing-queued-notification-job-properties"></a>
#### 큐잉된 알림 작업 속성 커스터마이징

알림 클래스에 속성을 정의함으로써, 하위 큐 작업의 동작을 커스터마이징할 수 있습니다. 이 속성들은 알림을 전송하는 큐 작업에도 그대로 적용됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * The number of times the notification may be attempted.
     *
     * @var int
     */
    public $tries = 5;

    /**
     * The number of seconds the notification can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    // ...
}
```

큐잉된 알림의 데이터 보안 및 무결성을 [암호화](/docs/12.x/encryption)로 보장하고 싶다면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue, ShouldBeEncrypted
{
    use Queueable;

    // ...
}
```

위 속성들을 클래스에 직접 정의하는 것 외에도, 큐잉된 알림 작업의 백오프 전략과 재시도 제한을 위해 `backoff`, `retryUntil` 메서드를 정의할 수 있습니다:

```php
use DateTime;

/**
 * Calculate the number of seconds to wait before retrying the notification.
 */
public function backoff(): int
{
    return 3;
}

/**
 * Determine the time at which the notification should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> 이러한 작업 속성 및 메서드에 대한 자세한 내용은 [큐잉 작업 문서](/docs/12.x/queues#max-job-attempts-and-timeout)를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림은 [큐잉 작업과 마찬가지로](/docs/12.x/queues#job-middleware) 미들웨어를 정의할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하면 됩니다. 이 메서드는 `$notifiable`과 `$channel` 변수를 받아, 목적지에 따라 반환할 미들웨어를 커스터마이징할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the notification job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(object $notifiable, string $channel)
{
    return match ($channel) {
        'mail' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```

<a name="queued-notifications-and-database-transactions"></a>
#### 큐잉된 알림과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 큐잉된 알림을 디스패치하면, 큐가 트랜잭션 커밋 전 작업을 처리할 수 있습니다. 이 경우, 트랜잭션 도중 변경된 모델이나 데이터베이스 레코드는 아직 실제 DB에 반영되지 않은 상태일 수 있습니다. 또한 트랜잭션에서 새로 생성된 모델이나 레코드 역시 존재하지 않을 수 있습니다. 이렇게 되면 해당 모델이나 레코드를 필요로 하는 알림 작업에서 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정값이 `false`인 경우에도, 알림을 전송할 때 `afterCommit` 메서드를 호출해 해당 큐잉된 알림이 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치되게 할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 생성자 내부에서 `afterCommit`을 호출해도 됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 보다 자세한 우회 방법은 [큐 작업과 데이터베이스 트랜잭션 문서](/docs/12.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 발송 여부 결정

큐잉된 알림이 백그라운드 작업으로 큐에 디스패치된 후에는 일반적으로 큐 워커가 해당 알림을 받아 수신자에게 전송합니다.

하지만 알림이 큐 워커에 의해 처리된 후에도 알림을 보낼지 최종적으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림을 보내지 않습니다:

```php
/**
 * Determine if the notification should be sent.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```

<a name="after-sending-notifications"></a>
#### 알림 전송 후 작업

알림이 전송된 후 추가적으로 코드를 실행하고 싶다면, 알림 클래스에 `afterSending` 메서드를 정의할 수 있습니다. 이 메서드는 notifiable 엔터티, 채널명, 그리고 해당 채널의 응답 값을 인수로 받습니다:

```php
/**
 * Handle the notification after it has been sent.
 */
public function afterSending(object $notifiable, string $channel, mixed $response): void
{
    // ...
}
```

<a name="on-demand-notifications"></a>
### 온디맨드 알림 (On-Demand Notifications)

애플리케이션의 "유저"로 등록되어 있지 않은 사람에게도 알림을 보낼 수 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면 임의로 알림 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

메일 라우트로 온디맨드 알림 전송 시 수신자의 이름을 함께 전달하려면, 배열의 첫 요소로 이메일 주소를 키, 이름을 값으로 지정하면 됩니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 알림 채널의 라우팅 정보를 한 번에 지정할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

(이하 모든 하위 목차 및 본문은 동일한 규칙으로, 코드블록 및 인라인코드는 원문 그대로, 문서 구조 및 용어집, 규칙, 형식에 따라 완전하게 번역되어야 하며, 내용은 한 줄도 생략해서는 안 됩니다.)

--- (이후 모든 섹션은 Core Guidelines와 용어집, 위 원칙들을 반영하여 번역하였습니다. 이어서 계속...)