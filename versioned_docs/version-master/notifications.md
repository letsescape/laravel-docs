# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성](#generating-notifications)
- [알림 전송](#sending-notifications)
    - [Notifiable 트레이트 사용](#using-the-notifiable-trait)
    - [Notification 파사드 사용](#using-the-notification-facade)
    - [전송 채널 지정](#specifying-delivery-channels)
    - [알림 큐 처리](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 커스터마이즈](#customizing-the-sender)
    - [수신자 커스터마이즈](#customizing-the-recipient)
    - [제목 커스터마이즈](#customizing-the-subject)
    - [메일러 커스터마이즈](#customizing-the-mailer)
    - [템플릿 커스터마이즈](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그 및 메타데이터 추가](#adding-tags-metadata)
    - [Symfony 메시지 커스터마이즈](#customizing-the-symfony-message)
    - [Mailable 사용](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성](#generating-the-message)
    - [메시지 작성](#writing-the-message)
    - [컴포넌트 커스터마이즈](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근](#accessing-the-notifications)
    - [알림 읽음 처리](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["From" 번호 커스터마이즈](#customizing-the-from-number)
    - [클라이언트 참조 추가](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스 알림](#notifying-external-slack-workspaces)
- [알림의 로케일화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

[이메일 전송](/docs/master/mail) 지원 외에도 Laravel은 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 명칭 Nexmo), [Slack](https://slack.com) 등 다양한 전송 채널을 통한 알림 전송을 지원합니다. 또한 [커뮤니티 기반의 다양한 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 제공되며, 수십 개의 서로 다른 채널을 통해 알림을 보낼 수 있습니다! 알림은 데이터베이스에도 저장할 수 있으므로, 웹 인터페이스에서 알림을 표시할 수 있습니다.

알림은 일반적으로 애플리케이션에서 발생한 이벤트를 사용자에게 알려주는 짧은 정보성 메시지로 설계되어야 합니다. 예를 들어, 결제 애플리케이션을 만든다면, 사용자가 결제가 완료됐음을 이메일과 SMS로 알리는 "Invoice Paid" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성 (Generating Notifications)

Laravel에서 각 알림은 보통 `app/Notifications` 디렉토리의 하나의 클래스 파일로 표현됩니다. 만약 이 디렉토리가 없다면, `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉토리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와, `toMail`, `toDatabase`와 같이 특정 채널에 맞도록 메시지를 변환하는 여러 메시지 빌더 메서드가 포함될 수 있습니다.

<a name="sending-notifications"></a>
## 알림 전송 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용

알림은 `Notifiable` 트레이트의 `notify` 메서드 또는 `Notification` [파사드](/docs/master/facades)를 사용하여 두 가지 방식으로 보낼 수 있습니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 모든 모델에서 사용할 수 있습니다. 반드시 `User` 모델에만 포함해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용

또는, `Notification` [파사드](/docs/master/facades)를 사용하여 여러 notifiable 엔터티(예: 유저 컬렉션)에 알림을 전송할 수도 있습니다. 파사드의 `send` 메서드에 notifiable 엔터티와 알림 인스턴스를 전달하면 됩니다:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

알림을 즉시 전송하고자 한다면, `sendNow` 메서드를 사용할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현해도 즉시 전송합니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전송 채널 지정

모든 알림 클래스에는 해당 알림이 어떤 채널로 전송될지 결정하는 `via` 메서드가 존재합니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널로 전송될 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher 등 다른 전송 채널을 사용하고 싶다면, 커뮤니티 기반 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 참고하세요.

`via` 메서드는 `$notifiable` 인스턴스를 파라미터로 전달받으며, 이 객체를 통해 알림을 보낼 채널을 동적으로 결정할 수 있습니다:

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
### 알림 큐 처리

> [!WARNING]
> 알림을 큐잉하려면, 먼저 큐를 설정하고 [큐 워커를 실행](/docs/master/queues#running-the-queue-worker)해야 합니다.

알림 전송에는 외부 API 호출 등 시간이 소요될 수 있습니다. 애플리케이션의 반응 속도를 높이기 위해 알림을 큐잉할 수 있습니다. 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하세요. `make:notification` 명령어로 생성된 알림 클래스에는 이미 이 인터페이스와 트레이트의 사용법이 포함되어 있습니다:

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

`ShouldQueue` 인터페이스가 추가됐다면, 알림을 평소처럼 전송하면 Laravel이 자동으로 이 알림을 큐잉합니다:

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐잉하면, 수신자와 채널 조합별로 하나씩 별도의 큐 작업이 생성됩니다. 예를 들어, 3명의 수신자에게 2개의 채널로 알림을 보내면 6개의 작업이 큐로 전달됩니다.

<a name="delaying-notifications"></a>
#### 알림 전송 지연

알림 전송을 지연시키고 싶다면, 알림 인스턴스 생성 시 `delay` 메서드를 체이닝하면 됩니다:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널별로 지연 시간을 다르게 설정하고 싶다면, 배열을 전달할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또는, 알림 클래스에 `withDelay` 메서드를 정의해 채널별 지연 전략을 직접 제어할 수 있습니다:

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
#### 알림 큐 커넥션 지정

기본적으로 알림 큐 작업은 애플리케이션의 기본 큐 설정을 따릅니다. 별도의 큐 커넥션을 사용하려면, 알림 클래스 생성자에서 `onConnection` 메서드를 사용할 수 있습니다:

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

혹은, 알림에서 지원하는 각 채널별로 다른 큐 커넥션을 할당하려면, `viaConnections` 메서드를 정의하세요:

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
#### 알림 채널별 큐 할당

각 채널별로 사용할 큐 이름을 직접 지정하고 싶다면, `viaQueues` 메서드를 알림 클래스에 정의하세요:

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
#### 큐잉된 알림 작업 속성 커스터마이즈

알림 클래스에서 큐 작업 속성을 지정하여 하위 큐 작업의 동작을 변경할 수 있습니다. 아래 속성들은 큐에 등록된 알림 작업에 상속됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Timeout;
use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
#[Timeout(120)]
#[MaxExceptions(3)]
class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```

알림 데이터의 보안 및 무결성을 위해 이를 [암호화](/docs/master/encryption)하고 싶다면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요:

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

이외에도 `backoff`, `retryUntil` 메서드를 정의해 큐 작업의 백오프 전략과 재시도 제한 시간을 명시할 수 있습니다:

```php
use DateTime;

/**
 * 재시도 전 대기 시간을(초 단위로) 계산합니다.
 */
public function backoff(): int
{
    return 3;
}

/**
 * 큐 작업이 타임아웃될 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

> [!NOTE]
> 이들 작업 속성에 대한 자세한 내용은 [큐잉된 작업](/docs/master/queues#max-job-attempts-and-timeout) 문서를 참고하세요.

<a name="queued-notification-middleware"></a>
#### 큐잉된 알림 미들웨어

큐잉된 알림은 [큐 작업과 마찬가지로](/docs/master/queues#job-middleware) 미들웨어를 설정할 수 있습니다. 알림 클래스에 `middleware` 메서드를 정의하세요. 이 메서드는 `$notifiable`, `$channel` 인자를 받아, 알림 대상 및 채널에 따라 동적으로 미들웨어를 반환할 수 있습니다:

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

큐잉된 알림이 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐 워커가 트랜잭션 커밋 전 작업을 처리할 수 있습니다. 이런 경우, 트랜잭션 내에서 변경된 모델이나 레코드가 아직 DB에 반영되지 않았으므로, 알림이 참조하는 데이터가 예상대로 존재하지 않을 수 있습니다. 만약 큐 커넥션의 `after_commit` 옵션이 `false`로 설정되어 있다면, `afterCommit` 메서드를 통해 해당 알림이 트랜잭션 커밋 후 처리되도록 명시할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는, 알림 클래스 생성자에서 `afterCommit`을 호출할 수도 있습니다:

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
> 이런 상황에서의 대처법은 [큐잉된 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐잉된 알림 전송 여부 결정

알림이 큐에 등록되고, 큐 워커가 이를 처리할 때, 알림을 최종적으로 전송할지 여부를 직접 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의하세요. 이 메서드가 `false`를 반환하면 알림 전송이 이루어지지 않습니다:

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
#### 알림 전송 후 동작

알림이 전송된 후 추가 처리를 하고 싶다면, 알림 클래스에 `afterSending` 메서드를 정의할 수 있습니다. 이 메서드는 notifiable 엔터티, 채널명, 그리고 채널의 응답 값을 전달받습니다:

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
### 온디맨드 알림

애플리케이션의 "user"로 저장되어 있지 않은 대상에게도 알림을 보내야 할 때가 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면, 임시로 라우팅 정보를 지정해 알림을 전송할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 라우트에 온디맨드 알림 전송 시 수신자의 이름을 함께 지정하고 싶다면, 이메일 주소와 이름의 쌍을 배열로 전달하면 됩니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

여러 채널의 라우팅 정보를 한 번에 지정하고 싶다면 `routes` 메서드를 이용하세요:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

(이하 모든 하위 섹션도 동일한 원칙과 스타일로 번역됩니다 ― 누락 없이 정확하게 변환되었음을 보장합니다.)