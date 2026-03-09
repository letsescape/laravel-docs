# 알림 (Notifications)

- [소개](#introduction)
- [알림 생성하기](#generating-notifications)
- [알림 보내기](#sending-notifications)
    - [Notifiable 트레이트 사용하기](#using-the-notifiable-trait)
    - [Notification 파사드 사용하기](#using-the-notification-facade)
    - [전달 채널 지정하기](#specifying-delivery-channels)
    - [알림 큐 처리하기](#queueing-notifications)
    - [온디맨드 알림](#on-demand-notifications)
- [메일 알림](#mail-notifications)
    - [메일 메시지 포맷팅](#formatting-mail-messages)
    - [발신자 사용자 지정](#customizing-the-sender)
    - [수신자 사용자 지정](#customizing-the-recipient)
    - [제목 사용자 지정](#customizing-the-subject)
    - [메일러 사용자 지정](#customizing-the-mailer)
    - [템플릿 사용자 지정](#customizing-the-templates)
    - [첨부파일](#mail-attachments)
    - [태그와 메타데이터 추가하기](#adding-tags-metadata)
    - [Symfony 메시지 사용자 지정](#customizing-the-symfony-message)
    - [Mailable 사용하기](#using-mailables)
    - [메일 알림 미리보기](#previewing-mail-notifications)
- [마크다운 메일 알림](#markdown-mail-notifications)
    - [메시지 생성하기](#generating-the-message)
    - [메시지 작성하기](#writing-the-message)
    - [컴포넌트 사용자 지정](#customizing-the-components)
- [데이터베이스 알림](#database-notifications)
    - [사전 준비사항](#database-prerequisites)
    - [데이터베이스 알림 포맷팅](#formatting-database-notifications)
    - [알림 접근하기](#accessing-the-notifications)
    - [알림을 읽음으로 표시하기](#marking-notifications-as-read)
- [브로드캐스트 알림](#broadcast-notifications)
    - [사전 준비사항](#broadcast-prerequisites)
    - [브로드캐스트 알림 포맷팅](#formatting-broadcast-notifications)
    - [알림 수신 대기하기](#listening-for-notifications)
- [SMS 알림](#sms-notifications)
    - [사전 준비사항](#sms-prerequisites)
    - [SMS 알림 포맷팅](#formatting-sms-notifications)
    - ["발신" 번호 사용자 지정](#customizing-the-from-number)
    - [클라이언트 참조 추가하기](#adding-a-client-reference)
    - [SMS 알림 라우팅](#routing-sms-notifications)
- [Slack 알림](#slack-notifications)
    - [사전 준비사항](#slack-prerequisites)
    - [Slack 알림 포맷팅](#formatting-slack-notifications)
    - [Slack 인터랙티비티](#slack-interactivity)
    - [Slack 알림 라우팅](#routing-slack-notifications)
    - [외부 Slack 워크스페이스에 알림 보내기](#notifying-external-slack-workspaces)
- [알림 현지화](#localizing-notifications)
- [테스트](#testing)
- [알림 이벤트](#notification-events)
- [커스텀 채널](#custom-channels)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [이메일 전송](/docs/12.x/mail) 지원 외에도 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전의 Nexmo), [Slack](https://slack.com) 등 다양한 전달 채널을 통해 알림을 보내는 기능을 지원합니다. 또한, 다양한 [커뮤니티 제작 알림 채널](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)이 만들어져 수십 가지 채널을 통해 알림을 보낼 수 있습니다! 알림은 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

일반적으로 알림은 애플리케이션에서 발생한 사항을 사용자에게 알리는 짧은 정보성 메시지여야 합니다. 예를 들어, 결제 애플리케이션을 작성하는 경우 이메일과 SMS 채널을 통해 사용자에게 "청구서 결제 완료" 알림을 보낼 수 있습니다.

<a name="generating-notifications"></a>
## 알림 생성하기 (Generating Notifications)

Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉토리에 저장되는 단일 클래스로 표현됩니다. 애플리케이션에서 이 디렉토리가 보이지 않더라도 걱정하지 마세요 - `make:notification` Artisan 명령어를 실행하면 자동으로 생성됩니다.

```shell
php artisan make:notification InvoicePaid
```

이 명령어는 `app/Notifications` 디렉토리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와 `toMail` 또는 `toDatabase`와 같이 알림을 특정 채널에 맞는 메시지로 변환하는 여러 메시지 빌드 메서드가 포함됩니다.

<a name="sending-notifications"></a>
## 알림 보내기 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 두 가지 방법으로 보낼 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드를 사용하거나 `Notification` [파사드](/docs/12.x/facades)를 사용하는 것입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다.

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

이 트레이트가 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에든 사용할 수 있다는 점을 기억하세요. `User` 모델에만 포함하는 것에 국한되지 않습니다.

<a name="using-the-notification-facade"></a>
### Notification 파사드 사용하기

또는 `Notification` [파사드](/docs/12.x/facades)를 통해 알림을 보낼 수도 있습니다. 이 방법은 사용자 컬렉션과 같이 여러 알림 가능한 엔티티에 알림을 보내야 할 때 유용합니다. 파사드를 사용하여 알림을 보내려면, 모든 알림 가능한 엔티티와 알림 인스턴스를 `send` 메서드에 전달하세요.

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` 메서드를 사용하여 알림을 즉시 보낼 수도 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하더라도 즉시 알림을 전송합니다.

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 전달 채널 지정하기

모든 알림 클래스에는 알림이 어떤 채널로 전달될지를 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널을 통해 보낼 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher와 같은 다른 전달 채널을 사용하고 싶다면 커뮤니티 주도의 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 확인하세요.

`via` 메서드는 알림이 전송되는 클래스의 인스턴스인 `$notifiable` 인스턴스를 받습니다. `$notifiable`을 사용하여 알림이 어떤 채널로 전달되어야 하는지 결정할 수 있습니다.

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
### 알림 큐 처리하기

> [!WARNING]
> 알림을 큐에 넣기 전에 큐를 설정하고 [워커를 시작](/docs/12.x/queues#running-the-queue-worker)해야 합니다.

알림을 보내는 데는 시간이 걸릴 수 있으며, 특히 채널이 알림을 전달하기 위해 외부 API를 호출해야 할 때 더욱 그렇습니다. 애플리케이션의 응답 시간을 단축하려면 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하여 알림을 큐에 넣으세요. `make:notification` 명령어로 생성된 모든 알림에는 인터페이스와 트레이트가 이미 임포트되어 있으므로, 알림 클래스에 바로 추가할 수 있습니다.

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

`ShouldQueue` 인터페이스가 알림에 추가되면, 평소처럼 알림을 보낼 수 있습니다. Laravel은 클래스에서 `ShouldQueue` 인터페이스를 감지하고 자동으로 알림 전달을 큐에 넣습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

알림을 큐에 넣을 때, 각 수신자와 채널 조합에 대해 큐 작업이 생성됩니다. 예를 들어, 알림에 세 명의 수신자와 두 개의 채널이 있으면 여섯 개의 작업이 큐에 디스패치됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연하기

알림 전달을 지연시키려면, 알림 인스턴스에 `delay` 메서드를 체이닝할 수 있습니다.

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

특정 채널에 대한 지연 시간을 지정하기 위해 `delay` 메서드에 배열을 전달할 수 있습니다.

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

또는 알림 클래스 자체에 `withDelay` 메서드를 정의할 수 있습니다. `withDelay` 메서드는 채널 이름과 지연 값의 배열을 반환해야 합니다.

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
#### 알림 큐 커넥션 사용자 지정

기본적으로 큐에 넣은 알림은 애플리케이션의 기본 큐 커넥션을 사용합니다. 특정 알림에 다른 커넥션을 지정하려면 알림의 생성자에서 `onConnection` 메서드를 호출할 수 있습니다.

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

또는 알림이 지원하는 각 알림 채널에 사용될 특정 큐 커넥션을 지정하려면 알림에 `viaConnections` 메서드를 정의할 수 있습니다. 이 메서드는 채널 이름/큐 커넥션 이름 쌍의 배열을 반환해야 합니다.

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
#### 알림 채널 큐 사용자 지정

알림이 지원하는 각 알림 채널에 사용될 특정 큐를 지정하려면 알림에 `viaQueues` 메서드를 정의할 수 있습니다. 이 메서드는 채널 이름/큐 이름 쌍의 배열을 반환해야 합니다.

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
#### 큐에 넣은 알림 작업 속성 사용자 지정

알림 클래스에 속성을 정의하여 기본 큐 작업의 동작을 사용자 지정할 수 있습니다. 이러한 속성은 알림을 전송하는 큐 작업에 상속됩니다.

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

큐에 넣은 알림 데이터의 개인정보 보호와 무결성을 [암호화](/docs/12.x/encryption)를 통해 보장하려면 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요.

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

알림 클래스에 이러한 속성을 직접 정의하는 것 외에도, `backoff`와 `retryUntil` 메서드를 정의하여 큐에 넣은 알림 작업의 백오프 전략과 재시도 타임아웃을 지정할 수 있습니다.

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
> 이러한 작업 속성과 메서드에 대한 자세한 내용은 [큐 작업](/docs/12.x/queues#max-job-attempts-and-timeout) 문서를 참조하세요.

<a name="queued-notification-middleware"></a>
#### 큐에 넣은 알림 미들웨어

큐에 넣은 알림은 [큐 작업과 마찬가지로](/docs/12.x/queues#job-middleware) 미들웨어를 정의할 수 있습니다. 시작하려면 알림 클래스에 `middleware` 메서드를 정의하세요. `middleware` 메서드는 `$notifiable`과 `$channel` 변수를 받으며, 이를 통해 알림의 대상에 따라 반환되는 미들웨어를 사용자 지정할 수 있습니다.

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
#### 큐에 넣은 알림과 데이터베이스 트랜잭션

큐에 넣은 알림이 데이터베이스 트랜잭션 내에서 디스패치되면, 데이터베이스 트랜잭션이 커밋되기 전에 큐에서 처리될 수 있습니다. 이 경우 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 대한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수 있습니다. 알림이 이러한 모델에 의존하는 경우, 큐에 넣은 알림을 처리하는 작업에서 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정 옵션이 `false`로 설정되어 있는 경우에도, 알림을 보낼 때 `afterCommit` 메서드를 호출하여 열려 있는 모든 데이터베이스 트랜잭션이 커밋된 후에 특정 큐 알림이 디스패치되도록 지정할 수 있습니다.

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

또는 알림의 생성자에서 `afterCommit` 메서드를 호출할 수 있습니다.

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
> 이러한 문제를 해결하는 방법에 대해 자세히 알아보려면 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참조하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 큐에 넣은 알림의 전송 여부 결정하기

큐에 넣은 알림이 백그라운드 처리를 위해 큐에 디스패치된 후, 일반적으로 큐 워커에 의해 수락되고 의도한 수신자에게 전송됩니다.

그러나 큐 워커가 처리한 후 큐에 넣은 알림의 전송 여부를 최종적으로 결정하려면 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 알림이 전송되지 않습니다.

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
#### 알림 전송 후

알림이 전송된 후 코드를 실행하려면 알림 클래스에 `afterSending` 메서드를 정의할 수 있습니다. 이 메서드는 알림 가능한 엔티티, 채널 이름, 채널의 응답을 받습니다.

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

때로는 애플리케이션의 "사용자"로 저장되지 않은 사람에게 알림을 보내야 할 수 있습니다. `Notification` 파사드의 `route` 메서드를 사용하면 알림을 보내기 전에 임시 알림 라우팅 정보를 지정할 수 있습니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

`mail` 라우트로 온디맨드 알림을 보낼 때 수신자의 이름을 제공하려면, 이메일 주소를 키로 하고 이름을 배열의 첫 번째 요소 값으로 하는 배열을 제공할 수 있습니다.

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` 메서드를 사용하면 여러 알림 채널에 대한 임시 라우팅 정보를 한 번에 제공할 수 있습니다.

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## 메일 알림 (Mail Notifications)

<a name="formatting-mail-messages"></a>
### 메일 메시지 포맷팅

알림이 이메일로 전송되는 것을 지원하는 경우, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받고 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스에는 트랜잭션 이메일 메시지를 구성하는 데 도움이 되는 몇 가지 간단한 메서드가 포함되어 있습니다. 메일 메시지에는 텍스트 라인과 "콜 투 액션"이 포함될 수 있습니다. `toMail` 메서드의 예를 살펴보겠습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->greeting('Hello!')
        ->line('One of your invoices has been paid!')
        ->lineIf($this->amount > 0, "Amount paid: {$this->amount}")
        ->action('View Invoice', $url)
        ->line('Thank you for using our application!');
}
```

> [!NOTE]
> `toMail` 메서드에서 `$this->invoice->id`를 사용하고 있다는 점에 주목하세요. 알림이 메시지를 생성하는 데 필요한 모든 데이터를 알림의 생성자에 전달할 수 있습니다.

이 예제에서는 인사말, 텍스트 라인, 콜 투 액션, 그리고 또 다른 텍스트 라인을 등록합니다. `MailMessage` 객체가 제공하는 이러한 메서드들은 작은 트랜잭션 이메일을 간단하고 빠르게 포맷팅할 수 있게 해줍니다. 그런 다음 메일 채널이 메시지 컴포넌트를 아름답고 반응형인 HTML 이메일 템플릿과 텍스트 전용 대응 템플릿으로 변환합니다. 다음은 `mail` 채널에서 생성된 이메일 예시입니다.

<img src="https://laravel.com/img/docs/notification-example-2.png">

> [!NOTE]
> 메일 알림을 보낼 때 `config/app.php` 설정 파일에서 `name` 설정 옵션을 설정했는지 확인하세요. 이 값은 메일 알림 메시지의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
#### 오류 메시지

일부 알림은 실패한 청구서 결제와 같이 사용자에게 오류를 알려줍니다. 메시지를 빌드할 때 `error` 메서드를 호출하여 메일 메시지가 오류에 관한 것임을 나타낼 수 있습니다. 메일 메시지에서 `error` 메서드를 사용하면 콜 투 액션 버튼이 검은색 대신 빨간색이 됩니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->error()
        ->subject('Invoice Payment Failed')
        ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
#### 기타 메일 알림 포맷팅 옵션

알림 클래스에서 텍스트 "라인"을 정의하는 대신, `view` 메서드를 사용하여 알림 이메일을 렌더링하는 데 사용할 커스텀 템플릿을 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```

`view` 메서드에 전달되는 배열의 두 번째 요소로 뷰 이름을 전달하여 메일 메시지의 텍스트 전용 뷰를 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```

또는, 메시지에 텍스트 전용 뷰만 있는 경우 `text` 메서드를 활용할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
### 발신자 사용자 지정

기본적으로 이메일의 발신자/보낸이 주소는 `config/mail.php` 설정 파일에서 정의됩니다. 그러나 `from` 메서드를 사용하여 특정 알림에 대한 발신자 주소를 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```

<a name="customizing-the-recipient"></a>
### 수신자 사용자 지정

`mail` 채널을 통해 알림을 보낼 때, 알림 시스템은 자동으로 알림 가능한 엔티티의 `email` 속성을 찾습니다. 알림 가능한 엔티티에 `routeNotificationForMail` 메서드를 정의하여 알림 전달에 사용되는 이메일 주소를 사용자 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the mail channel.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // Return email address only...
        return $this->email_address;

        // Return email address and name...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
### 제목 사용자 지정

기본적으로 이메일의 제목은 "Title Case"로 포맷된 알림 클래스 이름입니다. 따라서 알림 클래스 이름이 `InvoicePaid`인 경우, 이메일의 제목은 `Invoice Paid`가 됩니다. 메시지에 다른 제목을 지정하려면 메시지를 빌드할 때 `subject` 메서드를 호출할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```

<a name="customizing-the-mailer"></a>
### 메일러 사용자 지정

기본적으로 이메일 알림은 `config/mail.php` 설정 파일에 정의된 기본 메일러를 사용하여 전송됩니다. 그러나 메시지를 빌드할 때 `mailer` 메서드를 호출하여 런타임에 다른 메일러를 지정할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```

<a name="customizing-the-templates"></a>
### 템플릿 사용자 지정

알림 패키지의 리소스를 퍼블리시하여 메일 알림에서 사용하는 HTML 및 텍스트 전용 템플릿을 수정할 수 있습니다. 이 명령어를 실행하면 메일 알림 템플릿이 `resources/views/vendor/notifications` 디렉토리에 위치하게 됩니다.

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 첨부파일

이메일 알림에 첨부파일을 추가하려면 메시지를 빌드할 때 `attach` 메서드를 사용하세요. `attach` 메서드는 파일의 절대 경로를 첫 번째 인수로 받습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림 메일 메시지가 제공하는 `attach` 메서드는 [첨부 가능한 객체](/docs/12.x/mail#attachable-objects)도 허용합니다. 자세한 내용은 종합적인 [첨부 가능한 객체 문서](/docs/12.x/mail#attachable-objects)를 참조하세요.

메시지에 파일을 첨부할 때, `attach` 메서드의 두 번째 인수로 `array`를 전달하여 표시 이름 및/또는 MIME 타입을 지정할 수도 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file', [
            'as' => 'name.pdf',
            'mime' => 'application/pdf',
        ]);
}
```

Mailable 객체에서 파일을 첨부하는 것과 달리, `attachFromStorage`를 사용하여 스토리지 디스크에서 직접 파일을 첨부할 수 없습니다. 대신 스토리지 디스크에 있는 파일의 절대 경로를 사용하여 `attach` 메서드를 사용해야 합니다. 또는 `toMail` 메서드에서 [mailable](/docs/12.x/mail#generating-mailables)을 반환할 수 있습니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorage('/path/to/file');
}
```

필요한 경우, `attachMany` 메서드를 사용하여 메시지에 여러 파일을 첨부할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachMany([
            '/path/to/forge.svg',
            '/path/to/vapor.svg' => [
                'as' => 'Logo.svg',
                'mime' => 'image/svg+xml',
            ],
        ]);
}
```

<a name="raw-data-attachments"></a>
#### 원시 데이터 첨부파일

`attachData` 메서드를 사용하여 원시 바이트 문자열을 첨부파일로 첨부할 수 있습니다. `attachData` 메서드를 호출할 때 첨부파일에 할당할 파일 이름을 제공해야 합니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachData($this->pdf, 'name.pdf', [
            'mime' => 'application/pdf',
        ]);
}
```

<a name="adding-tags-metadata"></a>
### 태그와 메타데이터 추가하기

Mailgun이나 Postmark과 같은 일부 서드파티 이메일 제공업체는 메시지 "태그"와 "메타데이터"를 지원하며, 이를 사용하여 애플리케이션에서 보낸 이메일을 그룹화하고 추적할 수 있습니다. `tag`와 `metadata` 메서드를 통해 이메일 메시지에 태그와 메타데이터를 추가할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```

애플리케이션이 Mailgun 드라이버를 사용하는 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags)와 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 자세한 내용은 Mailgun 문서를 참조할 수 있습니다. 마찬가지로, [태그](https://postmarkapp.com/blog/tags-support-for-smtp)와 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 대한 지원에 관해 Postmark 문서도 참조할 수 있습니다.

애플리케이션이 Amazon SES를 사용하여 이메일을 보내는 경우, `metadata` 메서드를 사용하여 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 사용자 지정

`MailMessage` 클래스의 `withSymfonyMessage` 메서드를 사용하면 메시지를 보내기 전에 Symfony Message 인스턴스로 호출될 클로저를 등록할 수 있습니다. 이를 통해 메시지가 전달되기 전에 깊이 있게 사용자 지정할 수 있는 기회를 제공합니다.

```php
use Symfony\Component\Mime\Email;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->withSymfonyMessage(function (Email $message) {
            $message->getHeaders()->addTextHeader(
                'Custom-Header', 'Header Value'
            );
        });
}
```

<a name="using-mailables"></a>
### Mailable 사용하기

필요한 경우, 알림의 `toMail` 메서드에서 완전한 [mailable 객체](/docs/12.x/mail)를 반환할 수 있습니다. `MailMessage` 대신 `Mailable`을 반환할 때는 mailable 객체의 `to` 메서드를 사용하여 메시지 수신자를 지정해야 합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
#### Mailable과 온디맨드 알림

[온디맨드 알림](#on-demand-notifications)을 보내는 경우, `toMail` 메서드에 전달되는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스가 되며, 이는 온디맨드 알림이 전송되어야 할 이메일 주소를 검색하는 데 사용할 수 있는 `routeNotificationFor` 메서드를 제공합니다.

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    $address = $notifiable instanceof AnonymousNotifiable
        ? $notifiable->routeNotificationFor('mail')
        : $notifiable->email;

    return (new InvoicePaidMailable($this->invoice))
        ->to($address);
}
```

<a name="previewing-mail-notifications"></a>
### 메일 알림 미리보기

메일 알림 템플릿을 디자인할 때, 일반적인 Blade 템플릿처럼 렌더링된 메일 메시지를 브라우저에서 빠르게 미리 볼 수 있으면 편리합니다. 이러한 이유로 Laravel에서는 메일 알림으로 생성된 모든 메일 메시지를 라우트 클로저나 컨트롤러에서 직접 반환할 수 있습니다. `MailMessage`가 반환되면 브라우저에서 렌더링되어 표시되므로, 실제 이메일 주소로 보내지 않고도 디자인을 빠르게 미리 볼 수 있습니다.

```php
use App\Models\Invoice;
use App\Notifications\InvoicePaid;

Route::get('/notification', function () {
    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))
        ->toMail($invoice->user);
});
```

<a name="markdown-mail-notifications"></a>
## 마크다운 메일 알림 (Markdown Mail Notifications)

마크다운 메일 알림을 사용하면 메일 알림의 사전 제작된 템플릿을 활용하면서 더 길고 사용자 지정된 메시지를 작성할 수 있는 자유를 제공합니다. 메시지가 마크다운으로 작성되므로, Laravel은 메시지에 대해 아름답고 반응형인 HTML 템플릿을 렌더링하면서 동시에 텍스트 전용 대응 템플릿을 자동으로 생성할 수 있습니다.

<a name="generating-the-message"></a>
### 메시지 생성하기

해당 마크다운 템플릿이 포함된 알림을 생성하려면 `make:notification` Artisan 명령어의 `--markdown` 옵션을 사용할 수 있습니다.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

다른 모든 메일 알림과 마찬가지로, 마크다운 템플릿을 사용하는 알림은 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 그러나 `line`과 `action` 메서드를 사용하여 알림을 구성하는 대신, `markdown` 메서드를 사용하여 사용할 마크다운 템플릿의 이름을 지정합니다. 템플릿에서 사용할 수 있도록 할 데이터 배열을 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
### 메시지 작성하기

마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법의 조합을 사용하여 Laravel의 사전 제작된 알림 컴포넌트를 활용하면서 쉽게 알림을 구성할 수 있도록 합니다.

```blade
<x-mail::message>
# Invoice Paid

Your invoice has been paid!

<x-mail::button :url="$url">
View Invoice
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

> [!NOTE]
> 마크다운 이메일을 작성할 때 과도한 들여쓰기를 사용하지 마세요. 마크다운 표준에 따라 마크다운 파서는 들여쓴 콘텐츠를 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 중앙 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적 `color` 두 가지 인수를 받습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 알림에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 알림의 나머지 부분과 약간 다른 배경색을 가진 패널에 렌더링합니다. 이를 통해 특정 텍스트 블록에 주의를 끌 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 마크다운 테이블을 콘텐츠로 받습니다. 기본 마크다운 테이블 정렬 문법을 사용하여 테이블 열 정렬을 지원합니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### 컴포넌트 사용자 지정

사용자 지정을 위해 모든 마크다운 알림 컴포넌트를 자신의 애플리케이션으로 내보낼 수 있습니다. 컴포넌트를 내보내려면 `vendor:publish` Artisan 명령어를 사용하여 `laravel-mail` 에셋 태그를 퍼블리시합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

이 명령어는 마크다운 메일 컴포넌트를 `resources/views/vendor/mail` 디렉토리에 퍼블리시합니다. `mail` 디렉토리에는 사용 가능한 모든 컴포넌트의 각각의 표현을 포함하는 `html` 디렉토리와 `text` 디렉토리가 포함됩니다. 이 컴포넌트들을 원하는 대로 자유롭게 사용자 지정할 수 있습니다.

<a name="customizing-the-css"></a>
#### CSS 사용자 지정

컴포넌트를 내보낸 후, `resources/views/vendor/mail/html/themes` 디렉토리에 `default.css` 파일이 있습니다. 이 파일에서 CSS를 사용자 지정하면 스타일이 마크다운 알림의 HTML 표현에 자동으로 인라인됩니다.

Laravel의 마크다운 컴포넌트를 위한 완전히 새로운 테마를 빌드하려면 `html/themes` 디렉토리에 CSS 파일을 배치하세요. CSS 파일의 이름을 지정하고 저장한 후, `mail` 설정 파일의 `theme` 옵션을 새 테마의 이름과 일치하도록 업데이트합니다.

개별 알림의 테마를 사용자 지정하려면, 알림의 메일 메시지를 빌드할 때 `theme` 메서드를 호출할 수 있습니다. `theme` 메서드는 알림을 보낼 때 사용할 테마의 이름을 받습니다.

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->theme('invoice')
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="database-notifications"></a>
## 데이터베이스 알림 (Database Notifications)

<a name="database-prerequisites"></a>
### 사전 준비사항

`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 유형과 알림을 설명하는 JSON 데이터 구조 같은 정보가 포함됩니다.

테이블을 쿼리하여 애플리케이션의 사용자 인터페이스에 알림을 표시할 수 있습니다. 하지만 그 전에, 알림을 보관할 데이터베이스 테이블을 생성해야 합니다. `make:notifications-table` 명령어를 사용하여 적절한 테이블 스키마가 포함된 [마이그레이션](/docs/12.x/migrations)을 생성할 수 있습니다.

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 알림 가능한 모델이 [UUID 또는 ULID 기본 키](/docs/12.x/eloquent#uuid-and-ulid-keys)를 사용하는 경우, 알림 테이블 마이그레이션에서 `morphs` 메서드를 [uuidMorphs](/docs/12.x/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/12.x/migrations#column-method-ulidMorphs)로 교체해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

알림이 데이터베이스 테이블에 저장되는 것을 지원하는 경우, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받고 일반 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. `toArray` 메서드의 예를 살펴보겠습니다.

```php
/**
 * Get the array representation of the notification.
 *
 * @return array<string, mixed>
 */
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

알림이 애플리케이션의 데이터베이스에 저장될 때, `type` 컬럼은 기본적으로 알림의 클래스 이름으로 설정되며, `read_at` 컬럼은 `null`이 됩니다. 그러나 알림 클래스에 `databaseType`과 `initialDatabaseReadAtValue` 메서드를 정의하여 이 동작을 사용자 지정할 수 있습니다.

```php
use Illuminate\Support\Carbon;

/**
 * Get the notification's database type.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * Get the initial value for the "read_at" column.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```

<a name="todatabase-vs-toarray"></a>
#### `toDatabase` vs. `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 JavaScript 기반 프론트엔드에 브로드캐스트할 데이터를 결정하는 데 사용됩니다. `database`와 `broadcast` 채널에 대해 서로 다른 배열 표현을 사용하려면 `toArray` 메서드 대신 `toDatabase` 메서드를 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 알림 접근하기

알림이 데이터베이스에 저장되면, 알림 가능한 엔티티에서 편리하게 접근할 수 있는 방법이 필요합니다. Laravel의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트는 엔티티의 알림을 반환하는 `notifications` [Eloquent 관계](/docs/12.x/eloquent-relationships)를 포함합니다. 알림을 가져오려면 다른 Eloquent 관계처럼 이 메서드에 접근할 수 있습니다. 기본적으로 알림은 `created_at` 타임스탬프를 기준으로 정렬되며 가장 최근 알림이 컬렉션의 앞에 위치합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

"읽지 않은" 알림만 가져오려면 `unreadNotifications` 관계를 사용할 수 있습니다. 마찬가지로, 이 알림들은 `created_at` 타임스탬프를 기준으로 정렬되며 가장 최근 알림이 컬렉션의 앞에 위치합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

"읽은" 알림만 가져오려면 `readNotifications` 관계를 사용할 수 있습니다.

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript 클라이언트에서 알림에 접근하려면 현재 사용자와 같은 알림 가능한 엔티티의 알림을 반환하는 알림 컨트롤러를 애플리케이션에 정의해야 합니다. 그런 다음 JavaScript 클라이언트에서 해당 컨트롤러의 URL로 HTTP 요청을 보낼 수 있습니다.

<a name="marking-notifications-as-read"></a>
### 알림을 읽음으로 표시하기

일반적으로 사용자가 알림을 볼 때 "읽음"으로 표시하려 할 것입니다. `Illuminate\Notifications\Notifiable` 트레이트는 알림의 데이터베이스 레코드에서 `read_at` 컬럼을 업데이트하는 `markAsRead` 메서드를 제공합니다.

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

그러나 각 알림을 반복하는 대신, 알림 컬렉션에서 직접 `markAsRead` 메서드를 사용할 수 있습니다.

```php
$user->unreadNotifications->markAsRead();
```

데이터베이스에서 가져오지 않고 모든 알림을 읽음으로 표시하기 위해 대량 업데이트 쿼리를 사용할 수도 있습니다.

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

테이블에서 알림을 완전히 제거하기 위해 `delete`를 사용할 수 있습니다.

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## 브로드캐스트 알림 (Broadcast Notifications)

<a name="broadcast-prerequisites"></a>
### 사전 준비사항

알림을 브로드캐스트하기 전에 Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 설정하고 숙지해야 합니다. 이벤트 브로드캐스팅은 JavaScript 기반 프론트엔드에서 서버 측 Laravel 이벤트에 반응할 수 있는 방법을 제공합니다.

<a name="formatting-broadcast-notifications"></a>
### 브로드캐스트 알림 포맷팅

`broadcast` 채널은 Laravel의 [이벤트 브로드캐스팅](/docs/12.x/broadcasting) 서비스를 사용하여 알림을 브로드캐스트하며, JavaScript 기반 프론트엔드에서 실시간으로 알림을 캐치할 수 있습니다. 알림이 브로드캐스팅을 지원하는 경우, 알림 클래스에 `toBroadcast` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable` 엔티티를 받고 `BroadcastMessage` 인스턴스를 반환해야 합니다. `toBroadcast` 메서드가 존재하지 않으면 `toArray` 메서드가 브로드캐스트할 데이터를 수집하는 데 사용됩니다. 반환된 데이터는 JSON으로 인코딩되어 JavaScript 기반 프론트엔드에 브로드캐스트됩니다. `toBroadcast` 메서드의 예를 살펴보겠습니다.

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the broadcastable representation of the notification.
 */
public function toBroadcast(object $notifiable): BroadcastMessage
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
#### 브로드캐스트 큐 설정

모든 브로드캐스트 알림은 브로드캐스팅을 위해 큐에 넣어집니다. 브로드캐스트 작업을 큐에 넣는 데 사용되는 큐 커넥션이나 큐 이름을 설정하려면 `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다.

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 알림 타입 사용자 지정

지정한 데이터 외에도, 모든 브로드캐스트 알림에는 알림의 전체 클래스 이름을 포함하는 `type` 필드가 있습니다. 알림 `type`을 사용자 지정하려면 알림 클래스에 `broadcastType` 메서드를 정의할 수 있습니다.

```php
/**
 * Get the type of the notification being broadcast.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
### 알림 수신 대기하기

알림은 `{notifiable}.{id}` 규칙을 사용하여 포맷된 프라이빗 채널에 브로드캐스트됩니다. 따라서 ID가 `1`인 `App\Models\User` 인스턴스에 알림을 보내는 경우, 알림은 `App.Models.User.1` 프라이빗 채널에 브로드캐스트됩니다. [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 사용할 때 `notification` 메서드를 사용하여 채널에서 알림을 쉽게 수신 대기할 수 있습니다.

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React 또는 Vue 사용하기

Laravel Echo에는 알림 수신 대기를 간편하게 해주는 React와 Vue 훅이 포함되어 있습니다. 시작하려면 알림을 수신 대기하는 데 사용되는 `useEchoNotification` 훅을 호출합니다. `useEchoNotification` 훅은 소비하는 컴포넌트가 언마운트될 때 자동으로 채널을 떠납니다.

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```

기본적으로 훅은 모든 알림을 수신 대기합니다. 수신 대기할 알림 유형을 지정하려면 `useEchoNotification`에 문자열 또는 유형 배열을 제공할 수 있습니다.

```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```

알림 페이로드 데이터의 형태를 지정하여 더 높은 타입 안전성과 편집 편의성을 제공할 수도 있습니다.

```ts
type InvoicePaidNotification = {
    invoice_id: number;
    created_at: string;
};

useEchoNotification<InvoicePaidNotification>(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.invoice_id);
        console.log(notification.created_at);
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

<a name="customizing-the-notification-channel"></a>
#### 알림 채널 사용자 지정

엔티티의 브로드캐스트 알림이 브로드캐스트되는 채널을 사용자 지정하려면 알림 가능한 엔티티에 `receivesBroadcastNotificationsOn` 메서드를 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The channels the user receives notification broadcasts on.
     */
    public function receivesBroadcastNotificationsOn(): string
    {
        return 'users.'.$this->id;
    }
}
```

<a name="sms-notifications"></a>
## SMS 알림 (SMS Notifications)

<a name="sms-prerequisites"></a>
### 사전 준비사항

Laravel에서 SMS 알림 전송은 [Vonage](https://www.vonage.com/)(이전의 Nexmo)에 의해 구동됩니다. Vonage를 통해 알림을 보내려면 `laravel/vonage-notification-channel`과 `guzzlehttp/guzzle` 패키지를 설치해야 합니다.

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

이 패키지에는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있습니다. 그러나 이 설정 파일을 자신의 애플리케이션으로 내보낼 필요는 없습니다. `VONAGE_KEY`와 `VONAGE_SECRET` 환경 변수를 사용하여 Vonage 공개 키와 비밀 키를 정의하면 됩니다.

키를 정의한 후, 기본적으로 SMS 메시지가 발송될 전화번호를 정의하는 `VONAGE_SMS_FROM` 환경 변수를 설정해야 합니다. Vonage 제어 패널에서 이 전화번호를 생성할 수 있습니다.

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 알림 포맷팅

알림이 SMS로 전송되는 것을 지원하는 경우, 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받고 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
#### 유니코드 콘텐츠

SMS 메시지에 유니코드 문자가 포함되는 경우, `VonageMessage` 인스턴스를 생성할 때 `unicode` 메서드를 호출해야 합니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```

<a name="customizing-the-from-number"></a>
### "발신" 번호 사용자 지정

`VONAGE_SMS_FROM` 환경 변수에 지정된 전화번호와 다른 전화번호에서 일부 알림을 보내려면 `VonageMessage` 인스턴스에서 `from` 메서드를 호출할 수 있습니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가하기

사용자, 팀 또는 클라이언트별 비용을 추적하려면 알림에 "클라이언트 참조"를 추가할 수 있습니다. Vonage를 사용하면 이 클라이언트 참조를 사용하여 보고서를 생성할 수 있어 특정 고객의 SMS 사용량을 더 잘 이해할 수 있습니다. 클라이언트 참조는 최대 40자까지의 문자열이 될 수 있습니다.

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림을 적절한 전화번호로 라우팅하려면 알림 가능한 엔티티에 `routeNotificationForVonage` 메서드를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Vonage channel.
     */
    public function routeNotificationForVonage(Notification $notification): string
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
## Slack 알림 (Slack Notifications)

<a name="slack-prerequisites"></a>
### 사전 준비사항

Slack 알림을 보내기 전에 Composer를 통해 Slack 알림 채널을 설치해야 합니다.

```shell
composer require laravel/slack-notification-channel
```

또한 Slack 워크스페이스를 위한 [Slack 앱](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

앱이 생성된 동일한 Slack 워크스페이스에만 알림을 보내면 되는 경우, 앱에 `chat:write`, `chat:write.public`, `chat:write.customize` 스코프가 있는지 확인해야 합니다. 이 스코프는 Slack의 "OAuth & Permissions" 앱 관리 탭에서 추가할 수 있습니다.

다음으로, 앱의 "Bot User OAuth Token"을 복사하여 애플리케이션의 `services.php` 설정 파일의 `slack` 설정 배열에 배치합니다. 이 토큰은 Slack의 "OAuth & Permissions" 탭에서 찾을 수 있습니다.

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### 앱 배포

애플리케이션이 사용자가 소유한 외부 Slack 워크스페이스에 알림을 보내야 하는 경우, Slack을 통해 앱을 "배포"해야 합니다. 앱 배포는 Slack의 "Manage Distribution" 탭에서 관리할 수 있습니다. 앱이 배포되면 [Socialite](/docs/12.x/socialite)를 사용하여 애플리케이션 사용자를 대신하여 [Slack 봇 토큰을 획득](/docs/12.x/socialite#slack-bot-scopes)할 수 있습니다.

<a name="formatting-slack-notifications"></a>
### Slack 알림 포맷팅

알림이 Slack 메시지로 전송되는 것을 지원하는 경우, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받고 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)를 사용하여 풍부한 알림을 구성할 수 있습니다. 다음 예제는 [Slack의 Block Kit 빌더](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 볼 수 있습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
            $block->field("*Invoice No:*\n1000")->markdown();
            $block->field("*Invoice Recipient:*\ntaylor@laravel.com")->markdown();
        })
        ->dividerBlock()
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('Congratulations!');
        });
}
```

<a name="using-slacks-block-kit-builder-template"></a>
#### Slack의 Block Kit 빌더 템플릿 사용하기

유창한 메시지 빌더 메서드를 사용하여 Block Kit 메시지를 구성하는 대신, Slack의 Block Kit 빌더에서 생성된 원시 JSON 페이로드를 `usingBlockKitTemplate` 메서드에 제공할 수 있습니다.

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    $template = <<<JSON
        {
          "blocks": [
            {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": "Team Announcement"
              }
            },
            {
              "type": "section",
              "text": {
                "type": "plain_text",
                "text": "We are hiring!"
              }
            }
          ]
        }
    JSON;

    return (new SlackMessage)
        ->usingBlockKitTemplate($template);
}
```

<a name="slack-interactivity"></a>
### Slack 인터랙티비티

Slack의 Block Kit 알림 시스템은 [사용자 상호작용을 처리](https://api.slack.com/interactivity/handling)하는 강력한 기능을 제공합니다. 이 기능을 활용하려면 Slack 앱에서 "Interactivity"를 활성화하고 애플리케이션이 서비스하는 URL을 가리키는 "Request URL"을 설정해야 합니다. 이 설정은 Slack의 "Interactivity & Shortcuts" 앱 관리 탭에서 관리할 수 있습니다.

다음 예제에서는 `actionsBlock` 메서드를 활용하며, Slack은 버튼을 클릭한 Slack 사용자, 클릭된 버튼의 ID 등이 포함된 페이로드와 함께 "Request URL"로 `POST` 요청을 보냅니다. 그러면 애플리케이션은 페이로드에 따라 수행할 동작을 결정할 수 있습니다. 또한 요청이 Slack에 의해 만들어졌는지 [검증](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
             // ID defaults to "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // Manually configure the ID...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```

<a name="slack-confirmation-modals"></a>
#### 확인 모달

사용자가 동작을 수행하기 전에 확인을 요구하려면, 버튼을 정의할 때 `confirm` 메서드를 호출할 수 있습니다. `confirm` 메서드는 메시지와 `ConfirmObject` 인스턴스를 받는 클로저를 받습니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
            $block->button('Acknowledge Invoice')
                ->primary()
                ->confirm(
                    'Acknowledge the payment and send a thank you email?',
                    function (ConfirmObject $dialog) {
                        $dialog->confirm('Yes');
                        $dialog->deny('No');
                    }
                );
        });
}
```

<a name="inspecting-slack-blocks"></a>
#### Slack 블록 검사하기

빌드하고 있는 블록을 빠르게 검사하려면 `SlackMessage` 인스턴스에서 `dd` 메서드를 호출할 수 있습니다. `dd` 메서드는 Slack의 [Block Kit 빌더](https://app.slack.com/block-kit-builder/)에 대한 URL을 생성하고 덤프하며, 브라우저에서 페이로드와 알림의 미리보기를 표시합니다. `dd` 메서드에 `true`를 전달하면 원시 페이로드를 덤프할 수 있습니다.

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

Slack 알림을 적절한 Slack 팀과 채널로 보내려면 알림 가능한 모델에 `routeNotificationForSlack` 메서드를 정의합니다. 이 메서드는 세 가지 값 중 하나를 반환할 수 있습니다.

- `null` - 알림 자체에 설정된 채널로 라우팅을 위임합니다. `SlackMessage`를 빌드할 때 `to` 메서드를 사용하여 알림 내에서 채널을 설정할 수 있습니다.
- 알림을 보낼 Slack 채널을 지정하는 문자열, 예: `#support-channel`.
- OAuth 토큰과 채널 이름을 지정할 수 있는 `SlackRoute` 인스턴스, 예: `SlackRoute::make($this->slack_channel, $this->slack_token)`. 이 메서드는 외부 워크스페이스에 알림을 보내는 데 사용해야 합니다.

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`을 반환하면 애플리케이션의 `services.php` 설정 파일에 있는 Bot User OAuth 토큰과 연결된 워크스페이스의 `#support-channel` 채널로 알림이 전송됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```

<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스에 알림 보내기

> [!NOTE]
> 외부 Slack 워크스페이스에 알림을 보내기 전에 Slack 앱이 [배포](#slack-app-distribution)되어 있어야 합니다.

물론 애플리케이션 사용자가 소유한 Slack 워크스페이스에 알림을 보내고 싶은 경우가 많을 것입니다. 그러려면 먼저 사용자에 대한 Slack OAuth 토큰을 획득해야 합니다. 다행히도 [Laravel Socialite](/docs/12.x/socialite)에는 애플리케이션 사용자를 Slack으로 쉽게 인증하고 [봇 토큰을 획득](/docs/12.x/socialite#slack-bot-scopes)할 수 있는 Slack 드라이버가 포함되어 있습니다.

봇 토큰을 획득하고 애플리케이션의 데이터베이스에 저장한 후, `SlackRoute::make` 메서드를 사용하여 사용자의 워크스페이스로 알림을 라우팅할 수 있습니다. 또한 애플리케이션은 사용자가 알림을 보낼 채널을 지정할 수 있는 기회를 제공해야 할 것입니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Slack\SlackRoute;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```

<a name="localizing-notifications"></a>
## 알림 현지화 (Localizing Notifications)

Laravel은 HTTP 요청의 현재 로케일이 아닌 다른 로케일로 알림을 보낼 수 있으며, 알림이 큐에 넣어지더라도 이 로케일을 기억합니다.

이를 위해 `Illuminate\Notifications\Notification` 클래스는 원하는 언어를 설정하는 `locale` 메서드를 제공합니다. 알림이 평가될 때 애플리케이션은 이 로케일로 변경되고, 평가가 완료되면 이전 로케일로 되돌아갑니다.

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

여러 알림 가능한 엔트리의 현지화는 `Notification` 파사드를 통해서도 가능합니다.

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### 사용자 선호 로케일

때로는 애플리케이션이 각 사용자의 선호 로케일을 저장합니다. 알림 가능한 모델에 `HasLocalePreference` 계약을 구현하면, 알림을 보낼 때 이 저장된 로케일을 사용하도록 Laravel에 지시할 수 있습니다.

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```

인터페이스를 구현하면 Laravel은 모델에 알림과 mailable을 보낼 때 자동으로 선호 로케일을 사용합니다. 따라서 이 인터페이스를 사용할 때 `locale` 메서드를 호출할 필요가 없습니다.

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## 테스트 (Testing)

`Notification` 파사드의 `fake` 메서드를 사용하여 알림이 전송되지 않도록 할 수 있습니다. 일반적으로 알림 전송은 실제로 테스트하고 있는 코드와 관련이 없습니다. 대부분의 경우 Laravel이 주어진 알림을 보내도록 지시받았다는 것을 단순히 assert하는 것으로 충분합니다.

`Notification` 파사드의 `fake` 메서드를 호출한 후, 알림이 사용자에게 전송하도록 지시받았는지 assert하고 알림이 받은 데이터를 검사할 수도 있습니다.

```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
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

    // Assert a notification was sent twice...
    Notification::assertSentTimes(WeeklyReminder::class, 2);

    // Assert that a given number of notifications were sent...
    Notification::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
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

        // Assert a notification was sent twice...
        Notification::assertSentTimes(WeeklyReminder::class, 2);

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```

주어진 "진실 테스트"를 통과하는 알림이 전송되었는지 assert하기 위해 `assertSentTo` 또는 `assertNotSentTo` 메서드에 클로저를 전달할 수 있습니다. 주어진 진실 테스트를 통과하는 알림이 최소 하나 전송되었다면 assertion이 성공합니다.

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림

테스트하는 코드가 [온디맨드 알림](#on-demand-notifications)을 보내는 경우, `assertSentOnDemand` 메서드를 통해 온디맨드 알림이 전송되었는지 테스트할 수 있습니다.

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드의 두 번째 인수로 클로저를 전달하면, 온디맨드 알림이 올바른 "라우트" 주소로 전송되었는지 확인할 수 있습니다.

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="notification-events"></a>
## 알림 이벤트 (Notification Events)

<a name="notification-sending-event"></a>
#### 알림 전송 이벤트

알림이 전송될 때, 알림 시스템에 의해 `Illuminate\Notifications\Events\NotificationSending` 이벤트가 디스패치됩니다. 이 이벤트에는 "알림 가능한" 엔티티와 알림 인스턴스 자체가 포함됩니다. 애플리케이션 내에서 이 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```

`NotificationSending` 이벤트의 이벤트 리스너가 `handle` 메서드에서 `false`를 반환하면 알림이 전송되지 않습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

이벤트 리스너 내에서 이벤트의 `notifiable`, `notification`, `channel` 속성에 접근하여 알림 수신자 또는 알림 자체에 대해 더 자세히 알 수 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
#### 알림 전송 완료 이벤트

알림이 전송되면, 알림 시스템에 의해 `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/12.x/events)가 디스패치됩니다. 이 이벤트에는 "알림 가능한" 엔티티와 알림 인스턴스 자체가 포함됩니다. 애플리케이션 내에서 이 이벤트에 대한 [이벤트 리스너](/docs/12.x/events)를 생성할 수 있습니다.

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```

이벤트 리스너 내에서 이벤트의 `notifiable`, `notification`, `channel`, `response` 속성에 접근하여 알림 수신자 또는 알림 자체에 대해 더 자세히 알 수 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(NotificationSent $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
## 커스텀 채널 (Custom Channels)

Laravel에는 몇 가지 알림 채널이 포함되어 있지만, 다른 채널을 통해 알림을 전달하는 자체 드라이버를 작성하고 싶을 수 있습니다. Laravel은 이를 간단하게 만들어줍니다. 시작하려면 `send` 메서드를 포함하는 클래스를 정의합니다. 이 메서드는 `$notifiable`과 `$notification` 두 가지 인수를 받아야 합니다.

`send` 메서드 내에서 알림의 메서드를 호출하여 채널이 이해하는 메시지 객체를 가져온 다음 원하는 방식으로 `$notifiable` 인스턴스에 알림을 보낼 수 있습니다.

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * Send the given notification.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // Send notification to the $notifiable instance...
    }
}
```

알림 채널 클래스가 정의되면, 알림의 `via` 메서드에서 클래스 이름을 반환할 수 있습니다. 이 예제에서 알림의 `toVoice` 메서드는 음성 메시지를 나타내기 위해 선택한 객체를 반환할 수 있습니다. 예를 들어, 이러한 메시지를 나타내기 위해 자체 `VoiceMessage` 클래스를 정의할 수 있습니다.

```php
<?php

namespace App\Notifications;

use App\Notifications\Messages\VoiceMessage;
use App\Notifications\VoiceChannel;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification
{
    use Queueable;

    /**
     * Get the notification channels.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * Get the voice representation of the notification.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```
