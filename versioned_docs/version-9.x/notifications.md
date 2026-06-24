<!-- # Notifications -->
# Notifications

- [Introduction](#introduction)
- [Generating Notifications](#generating-notifications)
- [Sending Notifications](#sending-notifications)
    - [Using The Notifiable Trait](#using-the-notifiable-trait)
    - [Using The Notification Facade](#using-the-notification-facade)
    - [Specifying Delivery Channels](#specifying-delivery-channels)
    - [Queueing Notifications](#queueing-notifications)
    - [On-Demand Notifications](#on-demand-notifications)
- [Mail Notifications](#mail-notifications)
    - [Formatting Mail Messages](#formatting-mail-messages)
    - [Customizing The Sender](#customizing-the-sender)
    - [Customizing The Recipient](#customizing-the-recipient)
    - [Customizing The Subject](#customizing-the-subject)
    - [Customizing The Mailer](#customizing-the-mailer)
    - [Customizing The Templates](#customizing-the-templates)
    - [Attachments](#mail-attachments)
    - [Adding Tags & Metadata](#adding-tags-metadata)
    - [Customizing The Symfony Message](#customizing-the-symfony-message)
    - [Using Mailables](#using-mailables)
    - [Previewing Mail Notifications](#previewing-mail-notifications)
- [Markdown Mail Notifications](#markdown-mail-notifications)
    - [Generating The Message](#generating-the-message)
    - [Writing The Message](#writing-the-message)
    - [Customizing The Components](#customizing-the-components)
- [Database Notifications](#database-notifications)
    - [Prerequisites](#database-prerequisites)
    - [Formatting Database Notifications](#formatting-database-notifications)
    - [Accessing The Notifications](#accessing-the-notifications)
    - [Marking Notifications As Read](#marking-notifications-as-read)
- [Broadcast Notifications](#broadcast-notifications)
    - [Prerequisites](#broadcast-prerequisites)
    - [Formatting Broadcast Notifications](#formatting-broadcast-notifications)
    - [Listening For Notifications](#listening-for-notifications)
- [SMS Notifications](#sms-notifications)
    - [Prerequisites](#sms-prerequisites)
    - [Formatting SMS Notifications](#formatting-sms-notifications)
    - [Formatting Shortcode Notifications](#formatting-shortcode-notifications)
    - [Customizing The "From" Number](#customizing-the-from-number)
    - [Adding A Client Reference](#adding-a-client-reference)
    - [Routing SMS Notifications](#routing-sms-notifications)
- [Slack Notifications](#slack-notifications)
    - [Prerequisites](#slack-prerequisites)
    - [Formatting Slack Notifications](#formatting-slack-notifications)
    - [Slack Attachments](#slack-attachments)
    - [Routing Slack Notifications](#routing-slack-notifications)
- [Localizing Notifications](#localizing-notifications)
- [Notification Events](#notification-events)
- [Custom Channels](#custom-channels)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to support for [sending email](/docs/9.x/mail), Laravel provides support for sending notifications across a variety of delivery channels, including email, SMS (via [Vonage](https://www.vonage.com/communications-apis/), formerly known as Nexmo), and [Slack](https://slack.com). In addition, a variety of [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel) have been created to send notifications over dozens of different channels! Notifications may also be stored in a database so they may be displayed in your web interface. -->
Laravel은 [sending email](/docs/9.x/mail) 기능 외에도 다양한 전송 채널을 통해 알림을 보낼 수 있도록 지원합니다. 이메일뿐만 아니라, SMS([Vonage](https://www.vonage.com/communications-apis/), 이전 명칭 Nexmo), [Slack](https://slack.com) 같은 채널로도 알림을 전송할 수 있습니다. 이 외에도 [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)이 있어, 수많은 채널로 손쉽게 알림을 보낼 수 있습니다! 또한 알림을 데이터베이스에 저장하여 웹 인터페이스에서 표시할 수도 있습니다.

<!-- Typically, notifications should be short, informational messages that notify users of something that occurred in your application. For example, if you are writing a billing application, you might send an "Invoice Paid" notification to your users via the email and SMS channels. -->
일반적으로 알림은 사용자가 애플리케이션에서 발생한 특정 이벤트를 바로 알 수 있도록 도와주는, 짧고 정보성 위주의 메시지여야 합니다. 예를 들어, 결제 기능이 있는 애플리케이션을 만든다고 가정하면, 사용자의 송장 결제가 완료되었을 때 "송장 결제 완료" 알림을 이메일과 SMS로 전송할 수 있습니다.

<a name="generating-notifications"></a>
<!-- ## Generating Notifications -->
## Generating Notifications

<!-- In Laravel, each notification is represented by a single class that is typically stored in the `app/Notifications` directory. Don't worry if you don't see this directory in your application - it will be created for you when you run the `make:notification` Artisan command: -->
Laravel에서 각 알림은 하나의 클래스로 표현되며, 보통 `app/Notifications` 디렉터리에 저장됩니다. 만약 이 디렉터리가 존재하지 않더라도 걱정하지 마세요. `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:notification InvoicePaid
```

<!-- This command will place a fresh notification class in your `app/Notifications` directory. Each notification class contains a `via` method and a variable number of message building methods, such as `toMail` or `toDatabase`, that convert the notification to a message tailored for that particular channel. -->
이 명령어를 실행하면 새로운 알림 클래스가 `app/Notifications` 디렉터리에 생성됩니다. 각 알림 클래스에는 `via` 메서드와 여러 개의 메시지 빌더 메서드(예: `toMail`, `toDatabase` 등)가 포함되어 있으며, 각 채널에 맞는 메시지로 알림을 변환합니다.

<a name="sending-notifications"></a>
<!-- ## Sending Notifications -->
## Sending Notifications

<a name="using-the-notifiable-trait"></a>
<!-- ### Using The Notifiable Trait -->
### Using The Notifiable Trait

<!-- Notifications may be sent in two ways: using the `notify` method of the `Notifiable` trait or using the `Notification` [facade](/docs/9.x/facades). The `Notifiable` trait is included on your application's `App\Models\User` model by default: -->
알림을 보내는 방법에는 두 가지가 있습니다. 첫 번째는 `Notifiable` 트레이트의 `notify` 메서드를 사용하는 방법이고, 두 번째는 `Notification` [facade](/docs/9.x/facades)를 이용하는 방법입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 이미 포함되어 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```

<!-- The `notify` method that is provided by this trait expects to receive a notification instance: -->
이 트레이트에서 제공하는 `notify` 메서드는 알림 인스턴스를 파라미터로 받습니다:

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> `Notifiable` 트레이트는 어떤 모델에도 사용할 수 있습니다. 반드시 `User` 모델에만 추가할 필요는 없습니다.

<a name="using-the-notification-facade"></a>
<!-- ### Using The Notification Facade -->
### Using The Notification Facade

<!-- Alternatively, you may send notifications via the `Notification` [facade](/docs/9.x/facades). This approach is useful when you need to send a notification to multiple notifiable entities such as a collection of users. To send notifications using the facade, pass all of the notifiable entities and the notification instance to the `send` method: -->
또 다른 방법으로, `Notification` [facade](/docs/9.x/facades)를 사용해 알림을 보낼 수 있습니다. 이 방식은 여러 명의 수신자(예: 사용자 컬렉션)에게 동시에 알림을 보내야 할 때 유용합니다. 파사드를 사용할 때는, 모든 수신자와 알림 인스턴스를 `send` 메서드에 전달하면 됩니다:

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

<!-- You can also send notifications immediately using the `sendNow` method. This method will send the notification immediately even if the notification implements the `ShouldQueue` interface: -->
또한 `sendNow` 메서드를 사용하면 알림을 즉시 전송할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현하고 있더라도 대기열 처리 없이 바로 전송합니다:

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
<!-- ### Specifying Delivery Channels -->
### Specifying Delivery Channels

<!-- Every notification class has a `via` method that determines on which channels the notification will be delivered. Notifications may be sent on the `mail`, `database`, `broadcast`, `vonage`, and `slack` channels. -->
모든 알림 클래스에는 어떤 채널로 알림을 보낼지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 등 다양한 채널 중 하나 이상으로 보낼 수 있습니다.

> [!NOTE]
> Telegram, Pusher와 같은 추가 채널을 사용하고 싶다면, 커뮤니티 주도로 운영되는 [Laravel Notification Channels website](http://laravel-notification-channels.com)를 참고하세요.

<!-- The `via` method receives a `$notifiable` instance, which will be an instance of the class to which the notification is being sent. You may use `$notifiable` to determine which channels the notification should be delivered on: -->
`via` 메서드는 `$notifiable` 인스턴스를 파라미터로 받는데, 이 인스턴스는 알림을 받을 대상 클래스의 인스턴스입니다. `$notifiable`을 사용해 어떤 채널로 알림을 보낼지 동적으로 결정할 수 있습니다:

```
/**
 * Get the notification's delivery channels.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function via($notifiable)
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
<!-- ### Queueing Notifications -->
### Queueing Notifications

> [!WARNING]
> 알림을 큐로 처리하기 전에 반드시 큐 구성을 마치고, [start a worker](/docs/9.x/queues)해야 합니다.

<!-- Sending notifications can take time, especially if the channel needs to make an external API call to deliver the notification. To speed up your application's response time, let your notification be queued by adding the `ShouldQueue` interface and `Queueable` trait to your class. The interface and trait are already imported for all notifications generated using the `make:notification` command, so you may immediately add them to your notification class: -->
알림을 보내는 과정은 시간이 꽤 걸릴 수 있습니다. 특히 외부 API 호출을 해야 할 때 더 그렇습니다. 애플리케이션의 응답 속도를 빠르게 유지하기 위해, 알림을 큐로 보내서 비동기 처리하도록 할 수 있습니다. 이를 위해서는 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 알림 클래스에 추가하세요. 이 인터페이스와 트레이트는 `make:notification` 명령어로 생성된 알림 클래스에 이미 임포트되어 있으니 바로 추가할 수 있습니다:

```
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

<!-- Once the `ShouldQueue` interface has been added to your notification, you may send the notification like normal. Laravel will detect the `ShouldQueue` interface on the class and automatically queue the delivery of the notification: -->
`ShouldQueue` 인터페이스를 추가한 후에는 평소처럼 알림을 보내면 됩니다. Laravel은 해당 클래스에 `ShouldQueue` 인터페이스가 있는지 자동으로 감지해서, 알림 전송을 큐에 대기시킵니다:

```
$user->notify(new InvoicePaid($invoice));
```

<!-- When queueing notifications, a queued job will be created for each recipient and channel combination. For example, six jobs will be dispatched to the queue if your notification has three recipients and two channels. -->
알림을 큐에 등록하면, 수신자와 채널 조합별로 각각의 대기열(job)이 생성됩니다. 예를 들어, 수신자가 3명이고 두 개의 채널로 보낼 경우, 총 6개의 작업이 큐에 할당됩니다.

<a name="delaying-notifications"></a>
<!-- #### Delaying Notifications -->
#### Delaying Notifications

<!-- If you would like to delay the delivery of the notification, you may chain the `delay` method onto your notification instantiation: -->
알림을 일정 시간 뒤에 보내고 싶다면, 알림 인스턴스 생성 시 `delay` 메서드를 체이닝해서 사용할 수 있습니다:

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<a name="delaying-notifications-per-channel"></a>
<!-- #### Delaying Notifications Per Channel -->
#### Delaying Notifications Per Channel

<!-- You may pass an array to the `delay` method to specify the delay amount for specific channels: -->
특정 채널에만 따로 전송 지연을 적용하고 싶다면, `delay` 메서드에 배열을 전달하면 됩니다:

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

<!-- Alternatively, you may define a `withDelay` method on the notification class itself. The `withDelay` method should return an array of channel names and delay values: -->
또는, 알림 클래스에 `withDelay` 메서드를 직접 정의할 수도 있습니다. `withDelay` 메서드는 채널명과 지연 값을 갖는 배열을 반환해야 합니다:

```
/**
 * Determine the notification's delivery delay.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function withDelay($notifiable)
{
    return [
        'mail' => now()->addMinutes(5),
        'sms' => now()->addMinutes(10),
    ];
}
```

<a name="customizing-the-notification-queue-connection"></a>
<!-- #### Customizing The Notification Queue Connection -->
#### Customizing The Notification Queue Connection

<!-- By default, queued notifications will be queued using your application's default queue connection. If you would like to specify a different connection that should be used for a particular notification, you may define a `$connection` property on the notification class: -->
기본적으로 큐 처리되는 알림은 애플리케이션의 기본 큐 연결(커넥션)을 사용합니다. 하지만 특정 알림에 대해 다른 연결을 사용하고 싶다면, 알림 클래스에 `$connection` 속성을 지정할 수 있습니다:

```
/**
 * The name of the queue connection to use when queueing the notification.
 *
 * @var string
 */
public $connection = 'redis';
```

<!-- Or, if you would like to specify a specific queue connection that should be used for each notification channel supported by the notification, you may define a `viaConnections` method on your notification. This method should return an array of channel name / queue connection name pairs: -->
알림이 지원하는 각 채널별로 큐 연결을 다르게 지정하고 싶을 경우, 알림 클래스에 `viaConnections` 메서드를 정의하면 됩니다. 이 메서드는 채널명과 큐 연결명을 짝지은 배열을 반환해야 합니다:

```
/**
 * Determine which connections should be used for each notification channel.
 *
 * @return array
 */
public function viaConnections()
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```

<a name="customizing-notification-channel-queues"></a>
<!-- #### Customizing Notification Channel Queues -->
#### Customizing Notification Channel Queues

<!-- If you would like to specify a specific queue that should be used for each notification channel supported by the notification, you may define a `viaQueues` method on your notification. This method should return an array of channel name / queue name pairs: -->
특정 알림 채널별로 사용할 큐 이름을 지정하고 싶다면, 알림 클래스에 `viaQueues` 메서드를 정의하세요. 이 메서드는 채널명과 큐 이름의 쌍으로 이루어진 배열을 반환해야 합니다:

```
/**
 * Determine which queues should be used for each notification channel.
 *
 * @return array
 */
public function viaQueues()
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```

<a name="queued-notifications-and-database-transactions"></a>
<!-- #### Queued Notifications & Database Transactions -->
#### Queued Notifications & Database Transactions

<!-- When queued notifications are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your notification depends on these models, unexpected errors can occur when the job that sends the queued notification is processed. -->
데이터베이스 트랜잭션 내에서 큐 알림을 디스패치할 경우, 데이터베이스 트랜잭션이 커밋되기 전에 큐 워커가 작업을 처리할 수 있습니다. 이런 상황에서는 트랜잭션에서 변경한 모델 또는 데이터베이스 레코드가 아직 저장되지 않았을 수 있습니다. 또한 트랜잭션 내에서 새로 생성된 레코드가 데이터베이스에 존재하지 않을 수도 있습니다. 만약 알림에서 이런 모델에 의존한다면, 큐 워커에서 작업할 때 예기치 않은 오류가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued notification should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the notification: -->
큐 연결의 `after_commit` 설정 옵션이 `false`로 되어 있다면, 알림 전송 시 `afterCommit` 메서드를 호출하여, 모든 데이터베이스 트랜잭션이 커밋된 이후에만 큐 알림이 처리되도록 지정할 수 있습니다:

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

<!-- Alternatively, you may call the `afterCommit` method from your notification's constructor: -->
또는, 알림 클래스 생성자에서 `afterCommit` 메서드를 호출해도 됩니다:

```
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
     *
     * @return void
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```

> [!NOTE]
> 이러한 문제를 우회하는 방법 등 자세한 내용은 [queued jobs and database transactions](/docs/9.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
<!-- #### Determining If A Queued Notification Should Be Sent -->
#### Determining If A Queued Notification Should Be Sent

<!-- After a queued notification has been dispatched for the queue for background processing, it will typically be accepted by a queue worker and sent to its intended recipient. -->
큐에 알림이 등록된 후, 보통은 큐 워커가 해당 작업을 받아서 실제로 수신자에게 알림을 전송하게 됩니다.

<!-- However, if you would like to make the final determination on whether the queued notification should be sent after it is being processed by a queue worker, you may define a `shouldSend` method on the notification class. If this method returns `false`, the notification will not be sent: -->
하지만 알림이 큐 워커에서 처리되는 시점에 전송 여부를 최종적으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 알림은 전송되지 않습니다:

```
/**
 * Determine if the notification should be sent.
 *
 * @param  mixed  $notifiable
 * @param  string  $channel
 * @return bool
 */
public function shouldSend($notifiable, $channel)
{
    return $this->invoice->isPaid();
}
```

<a name="on-demand-notifications"></a>
<!-- ### On-Demand Notifications -->
### On-Demand Notifications

<!-- Sometimes you may need to send a notification to someone who is not stored as a "user" of your application. Using the `Notification` facade's `route` method, you may specify ad-hoc notification routing information before sending the notification: -->
어떤 경우에는 애플리케이션에 저장된 "User" 엔티티가 아닌 대상자에게도 알림을 보내야 할 수 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 사용해, 임의의 알림 라우팅 정보를 지정한 뒤 알림을 보낼 수 있습니다:

```
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
            ->route('vonage', '5555555555')
            ->route('slack', 'https://hooks.slack.com/services/...')
            ->route('broadcast', [new Channel('channel-name')])
            ->notify(new InvoicePaid($invoice));
```

<!-- If you would like to provide the recipient's name when sending an on-demand notification to the `mail` route, you may provide an array that contains the email address as the key and the name as the value of the first element in the array: -->
온디맨드 알림을 `mail` 경로(route)로 보낼 때 수신자의 이름까지 지정하고 싶다면 이메일 주소와 이름을 배열 형태로 제공하면 됩니다. 배열의 첫 번째 원소에 이메일 주소가 키, 이름이 값이 되도록 설정합니다:

```
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
<!-- ## Mail Notifications -->
## Mail Notifications

<a name="formatting-mail-messages"></a>
<!-- ### Formatting Mail Messages -->
### Formatting Mail Messages

<!-- If a notification supports being sent as an email, you should define a `toMail` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\MailMessage` instance. -->
알림을 이메일로도 전송하고 싶다면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아서, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

<!-- The `MailMessage` class contains a few simple methods to help you build transactional email messages. Mail messages may contain lines of text as well as a "call to action". Let's take a look at an example `toMail` method: -->
`MailMessage` 클래스에는 트랜잭션 메일을 쉽게 만들기 위한 간단한 메서드들이 있습니다. 메일 메시지는 텍스트 줄과 함께, "콜 투 액션(call to action)" 버튼도 포함할 수 있습니다. 아래는 `toMail` 메서드의 예시입니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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
> 여기서 `$this->invoice->id`를 `toMail` 메서드에서 사용하고 있습니다. 알림 생성자에 메시지 생성을 위해 필요한 어떠한 데이터도 전달할 수 있습니다.

<!-- In this example, we register a greeting, a line of text, a call to action, and then another line of text. These methods provided by the `MailMessage` object make it simple and fast to format small transactional emails. The mail channel will then translate the message components into a beautiful, responsive HTML email template with a plain-text counterpart. Here is an example of an email generated by the `mail` channel: -->
이 예제에서는 인사 메시지, 텍스트 줄, 콜 투 액션, 마지막 안내 메시지를 차례로 등록합니다. `MailMessage` 객체가 제공하는 이러한 메서드들을 이용하면 간단하고 빠르게 트랜잭션 메일을 만들 수 있습니다. 메일 채널은 메시지의 요소들을 자동으로 아름답고 반응형인 HTML 메일 템플릿(그리고 텍스트-only 버전)으로 변환해줍니다. 다음은 `mail` 채널을 통해 생성된 메일 예시입니다:

<!-- <img src="https://laravel.com/img/docs/notification-example-2.png"/> -->
<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!NOTE]
> 메일 알림을 보낼 때는 반드시 `config/app.php` 설정 파일의 `name` 옵션을 설정해야 합니다. 이 값은 메일 알림 메시지의 헤더와 푸터에 사용됩니다.

<a name="error-messages"></a>
<!-- #### Error Messages -->
#### Error Messages

<!-- Some notifications inform users of errors, such as a failed invoice payment. You may indicate that a mail message is regarding an error by calling the `error` method when building your message. When using the `error` method on a mail message, the call to action button will be red instead of black: -->
일부 알림은 예를 들어 송장 결제 실패와 같은 오류 상황을 사용자에게 알려줄 필요가 있습니다. 이런 경우, 메시지 빌드 시 `error` 메서드를 호출하면 메일 메시지가 오류와 관련된 것으로 표시됩니다. `error`를 사용하면 콜 투 액션 버튼이 검은색 대신 빨간색으로 바뀝니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->error()
                ->subject('Invoice Payment Failed')
                ->line('...');
}
```

<a name="other-mail-notification-formatting-options"></a>
<!-- #### Other Mail Notification Formatting Options -->
#### Other Mail Notification Formatting Options

<!-- Instead of defining the "lines" of text in the notification class, you may use the `view` method to specify a custom template that should be used to render the notification email: -->
알림 클래스 내에서 텍스트 줄을 직접 정의하지 않고, `view` 메서드를 사용해 커스텀 템플릿을 지정할 수도 있습니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        'emails.name', ['invoice' => $this->invoice]
    );
}
```

<!-- You may specify a plain-text view for the mail message by passing the view name as the second element of an array that is given to the `view` method: -->
또한, 메일 메시지에 대해 plain-text 전용 뷰를 지정하고 싶다면, `view` 메서드에 전달하는 배열의 두 번째 원소로 plain-text 뷰명을 전달하면 됩니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)->view(
        ['emails.name.html', 'emails.name.plain'],
        ['invoice' => $this->invoice]
    );
}
```

<a name="customizing-the-sender"></a>
<!-- ### Customizing The Sender -->
### Customizing The Sender

<!-- By default, the email's sender / from address is defined in the `config/mail.php` configuration file. However, you may specify the from address for a specific notification using the `from` method: -->
기본적으로 이메일의 발신자(From) 주소는 `config/mail.php` 설정 파일에서 정의됩니다. 그러나 특정 알림에 대해 발신자 주소를 다르게 지정하고 싶다면, `from` 메서드를 사용하면 됩니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->from('barrett@example.com', 'Barrett Blair')
                ->line('...');
}
```

<a name="customizing-the-recipient"></a>
<!-- ### Customizing The Recipient -->
### Customizing The Recipient

<!-- When sending notifications via the `mail` channel, the notification system will automatically look for an `email` property on your notifiable entity. You may customize which email address is used to deliver the notification by defining a `routeNotificationForMail` method on the notifiable entity: -->
`mail` 채널을 통해 알림을 보낼 때, 알림 시스템은 수신자 엔티티에서 자동으로 `email` 속성을 찾아 메일을 보냅니다. 만약 사용할 이메일 주소를 직접 지정하고 싶다면, 수신자 모델에 `routeNotificationForMail` 메서드를 정의하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the mail channel.
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return array|string
     */
    public function routeNotificationForMail($notification)
    {
        // Return email address only...
        return $this->email_address;

        // Return email address and name...
        return [$this->email_address => $this->name];
    }
}
```

<a name="customizing-the-subject"></a>
<!-- ### Customizing The Subject -->
### Customizing The Subject

<!-- By default, the email's subject is the class name of the notification formatted to "Title Case". So, if your notification class is named `InvoicePaid`, the email's subject will be `Invoice Paid`. If you would like to specify a different subject for the message, you may call the `subject` method when building your message: -->
기본적으로 이메일의 제목은 알림 클래스의 이름을 “타이틀 케이스” 형식으로 변환해서 사용합니다. 예를 들어 알림 클래스가 `InvoicePaid`라면, 이메일 제목은 `Invoice Paid`가 됩니다. 직접 제목을 정하고 싶다면 메시지를 만들 때 `subject` 메서드를 사용할 수 있습니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-mailer"></a>
<!-- ### Customizing The Mailer -->
### Customizing The Mailer

<!-- By default, the email notification will be sent using the default mailer defined in the `config/mail.php` configuration file. However, you may specify a different mailer at runtime by calling the `mailer` method when building your message: -->
알림이 이메일로 전송될 때는 기본적으로 `config/mail.php` 파일에 정의된 기본 메일러를 사용합니다. 하지만 런타임에 다른 메일러를 사용하고 싶다면, 메시지를 빌드할 때 `mailer` 메서드를 호출하면 됩니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->mailer('postmark')
                ->line('...');
}
```

<a name="customizing-the-templates"></a>
<!-- ### Customizing The Templates -->
### Customizing The Templates

<!-- You can modify the HTML and plain-text template used by mail notifications by publishing the notification package's resources. After running this command, the mail notification templates will be located in the `resources/views/vendor/notifications` directory: -->
메일 알림에서 사용하는 HTML, plain-text 템플릿을 직접 수정하고 싶다면, notification 패키지의 리소스를 퍼블리시(publish)하면 됩니다. 아래 명령어를 실행한 후에는 템플릿 파일들이 `resources/views/vendor/notifications` 디렉터리에 위치하게 됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- To add attachments to an email notification, use the `attach` method while building your message. The `attach` method accepts the absolute path to the file as its first argument: -->
메일 알림에 첨부 파일을 추가하려면 메시지 빌드 시 `attach` 메서드를 사용하세요. `attach` 메서드는 첫 번째 인자로 첨부할 파일의 절대 경로를 받습니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file');
}
```

> [!NOTE]
> 알림 메일 메시지에서 제공하는 `attach` 메서드는 [attachable objects](/docs/9.x/mail#attachable-objects)도 지원합니다. 자세한 내용은 [attachable object documentation](/docs/9.x/mail#attachable-objects)를 참고하세요.

<!-- When attaching files to a message, you may also specify the display name and / or MIME type by passing an `array` as the second argument to the `attach` method: -->
메시지에 파일을 첨부할 때, `attach` 메서드의 두 번째 인수로 `array`를 전달하여 표시 이름 또는 MIME 타입을 지정할 수도 있습니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attach('/path/to/file', [
                    'as' => 'name.pdf',
                    'mime' => 'application/pdf',
                ]);
}
```

<!-- Unlike attaching files in mailable objects, you may not attach a file directly from a storage disk using `attachFromStorage`. You should rather use the `attach` method with an absolute path to the file on the storage disk. Alternatively, you could return a [mailable](/docs/9.x/mail#generating-mailables) from the `toMail` method: -->
mailable 객체에서 파일을 첨부할 때와 달리, 알림에서는 `attachFromStorage` 메서드를 직접 사용할 수 없습니다. 대신, storage 디스크 내 파일의 절대 경로를 `attach` 메서드에 전달해야 합니다. 또는, `toMail` 메서드에서 [mailable](/docs/9.x/mail#generating-mailables)을 반환하는 것도 가능합니다:

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email)
                ->attachFromStorage('/path/to/file');
}
```

<!-- When necessary, multiple files may be attached to a message using the `attachMany` method: -->
메일에 여러 파일을 첨부해야 할 경우, `attachMany` 메서드를 사용할 수 있습니다:

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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

<!-- #### Raw Data Attachments -->
#### Raw Data Attachments

<!-- The `attachData` method may be used to attach a raw string of bytes as an attachment. When calling the `attachData` method, you should provide the filename that should be assigned to the attachment: -->
`attachData` 메서드를 사용하면 바이트 문자열 형태의 원시 데이터를 첨부파일로 메일에 첨부할 수 있습니다. `attachData` 메서드를 호출할 때 첨부될 파일의 파일명을 직접 지정해야 합니다.

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Hello!')
                ->attachData($this->pdf, 'name.pdf', [
                    'mime' => 'application/pdf',
                ]);
}
```

<a name="adding-tags-metadata"></a>
<!-- ### Adding Tags & Metadata -->
### Adding Tags & Metadata

<!-- Some third-party email providers such as Mailgun and Postmark support message "tags" and "metadata", which may be used to group and track emails sent by your application. You may add tags and metadata to an email message via the `tag` and `metadata` methods: -->
Mailgun, Postmark와 같은 일부 외부 이메일 서비스들은 애플리케이션에서 발송하는 이메일을 그룹화하거나 추적할 수 있도록 "태그(tag)"와 "메타데이터(metadata)" 기능을 지원합니다. 이메일 메시지에 태그와 메타데이터를 추가하려면 각각 `tag`와 `metadata` 메서드를 사용할 수 있습니다.

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->greeting('Comment Upvoted!')
                ->tag('upvote')
                ->metadata('comment_id', $this->comment->id);
}
```

<!-- If your application is using the Mailgun driver, you may consult Mailgun's documentation for more information on [tags](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) and [metadata](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages). Likewise, the Postmark documentation may also be consulted for more information on their support for [tags](https://postmarkapp.com/blog/tags-support-for-smtp) and [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq). -->
애플리케이션에서 Mailgun 드라이버를 사용하는 경우, [tags](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) 및 [metadata](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) 관련 공식 문서를 참고하여 자세한 정보를 확인할 수 있습니다. 마찬가지로, Postmark의 [tags](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) 관련 문서도 참고하시기 바랍니다.

<!-- If your application is using Amazon SES to send emails, you should use the `metadata` method to attach [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) to the message. -->
만약 Amazon SES를 통해 이메일을 발송하는 경우, 메시지에 [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 추가하고 싶다면 `metadata` 메서드를 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
<!-- ### Customizing The Symfony Message -->
### Customizing The Symfony Message

<!-- The `withSymfonyMessage` method of the `MailMessage` class allows you to register a closure which will be invoked with the Symfony Message instance before sending the message. This gives you an opportunity to deeply customize the message before it is delivered: -->
`MailMessage` 클래스의 `withSymfonyMessage` 메서드는 메시지 전송 전에 Symfony Message 인스턴스를 인자로 받아 원하는 방식으로 커스터마이징할 수 있는 클로저를 등록할 수 있습니다. 이를 통해 메시지가 실제로 전송되기 전에 깊이 있는 커스터마이징이 가능합니다.

```
use Symfony\Component\Mime\Email;

/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
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
<!-- ### Using Mailables -->
### Using Mailables

<!-- If needed, you may return a full [mailable object](/docs/9.x/mail) from your notification's `toMail` method. When returning a `Mailable` instead of a `MailMessage`, you will need to specify the message recipient using the mailable object's `to` method: -->
필요하다면 알림 클래스의 `toMail` 메서드에서 [mailable object](/docs/9.x/mail)를 그대로 반환할 수 있습니다. `MailMessage` 대신 `Mailable`을 반환할 때는, mailable 객체의 `to` 메서드를 사용하여 수신자를 지정해주어야 합니다.

```
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
{
    return (new InvoicePaidMailable($this->invoice))
                ->to($notifiable->email);
}
```

<a name="mailables-and-on-demand-notifications"></a>
<!-- #### Mailables & On-Demand Notifications -->
#### Mailables & On-Demand Notifications

<!-- If you are sending an [on-demand notification](#on-demand-notifications), the `$notifiable` instance given to the `toMail` method will be an instance of `Illuminate\Notifications\AnonymousNotifiable`, which offers a `routeNotificationFor` method that may be used to retrieve the email address the on-demand notification should be sent to: -->
[on-demand notification](#on-demand-notifications)을 발송할 경우, `toMail` 메서드에 전달되는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스입니다. 이 객체에서는 `routeNotificationFor` 메서드를 활용해 해당 on-demand 알림을 보내야 할 이메일 주소를 쉽게 가져올 수 있습니다.

```
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;

/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return Mailable
 */
public function toMail($notifiable)
{
    $address = $notifiable instanceof AnonymousNotifiable
            ? $notifiable->routeNotificationFor('mail')
            : $notifiable->email;

    return (new InvoicePaidMailable($this->invoice))
                ->to($address);
}
```

<a name="previewing-mail-notifications"></a>
<!-- ### Previewing Mail Notifications -->
### Previewing Mail Notifications

<!-- When designing a mail notification template, it is convenient to quickly preview the rendered mail message in your browser like a typical Blade template. For this reason, Laravel allows you to return any mail message generated by a mail notification directly from a route closure or controller. When a `MailMessage` is returned, it will be rendered and displayed in the browser, allowing you to quickly preview its design without needing to send it to an actual email address: -->
메일 알림 템플릿을 디자인할 때 실제 이메일로 전송하지 않고 바로 브라우저에서 Blade 템플릿처럼 결과를 미리 확인할 수 있으면 매우 편리합니다. Laravel에서는 라우트 클로저나 컨트롤러에서 알림에서 생성한 mail 메시지를 직접 반환할 수 있습니다. `MailMessage`가 반환되면, 해당 메시지를 렌더링해서 브라우저에서 바로 미리 볼 수 있으므로, 실제로 이메일 주소로 발송하지 않고 빠르게 디자인을 확인할 수 있습니다.

```
use App\Models\Invoice;
use App\Notifications\InvoicePaid;

Route::get('/notification', function () {
    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))
                ->toMail($invoice->user);
});
```

<a name="markdown-mail-notifications"></a>
<!-- ## Markdown Mail Notifications -->
## Markdown Mail Notifications

<!-- Markdown mail notifications allow you to take advantage of the pre-built templates of mail notifications, while giving you more freedom to write longer, customized messages. Since the messages are written in Markdown, Laravel is able to render beautiful, responsive HTML templates for the messages while also automatically generating a plain-text counterpart. -->
마크다운 메일 알림을 사용하면 Laravel이 제공하는 다양한 미리 만들어진 템플릿의 장점을 활용하면서, 더 길고 자유로운 커스텀 문구를 사용할 수 있습니다. 해당 메시지들은 마크다운으로 작성되므로, Laravel은 메시지를 아름답고 반응형인 HTML 템플릿으로 렌더링할 뿐 아니라, 자동으로 일반 텍스트 버전도 함께 생성해줍니다.

<a name="generating-the-message"></a>
<!-- ### Generating The Message -->
### Generating The Message

<!-- To generate a notification with a corresponding Markdown template, you may use the `--markdown` option of the `make:notification` Artisan command: -->
마크다운 템플릿과 연동되는 알림 클래스를 생성하려면, Artisan의 `make:notification` 명령어에 `--markdown` 옵션을 함께 사용하면 됩니다.

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

<!-- Like all other mail notifications, notifications that use Markdown templates should define a `toMail` method on their notification class. However, instead of using the `line` and `action` methods to construct the notification, use the `markdown` method to specify the name of the Markdown template that should be used. An array of data you wish to make available to the template may be passed as the method's second argument: -->
기존의 메일 알림과 마찬가지로, 마크다운 템플릿을 사용하는 알림 클래스도 `toMail` 메서드를 정의해야 합니다. 단, 알림을 구성할 때 `line`과 `action` 대신 `markdown` 메서드를 사용해 사용할 마크다운 템플릿의 이름을 지정해야 합니다. 두 번째 인수로는 템플릿 내에서 사용할 데이터를 배열로 전달할 수 있습니다.

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="writing-the-message"></a>
<!-- ### Writing The Message -->
### Writing The Message

<!-- Markdown mail notifications use a combination of Blade components and Markdown syntax which allow you to easily construct notifications while leveraging Laravel's pre-crafted notification components: -->
마크다운 메일 알림은 Blade 컴포넌트와 마크다운 문법이 결합되어 있습니다. 이를 통해 Laravel이 미리 제작해둔 알림용 컴포넌트를 손쉽게 활용해 알림 메시지를 만들 수 있습니다.

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

<a name="button-component"></a>
<!-- #### Button Component -->
#### Button Component

<!-- The button component renders a centered button link. The component accepts two arguments, a `url` and an optional `color`. Supported colors are `primary`, `green`, and `red`. You may add as many button components to a notification as you wish: -->
버튼 컴포넌트는 화면 중앙에 버튼 형태의 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 인수를 받을 수 있습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 한 알림 내에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
<!-- #### Panel Component -->
#### Panel Component

<!-- The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the notification. This allows you to draw attention to a given block of text: -->
패널 컴포넌트는 전달된 텍스트 블록을 다른 부분과 확연히 다른 배경색을 갖는 패널 안쪽에 표시합니다. 이를 통해 특정 부분의 텍스트를 강조할 수 있습니다.

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
<!-- #### Table Component -->
#### Table Component

<!-- The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax: -->
테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블 형태로 변환하여 보여줄 수 있습니다. 컴포넌트의 콘텐츠로 마크다운 테이블을 직접 작성하면 됩니다. 컬럼 정렬 또한 기본 마크다운 정렬 문법으로 손쉽게 지정할 수 있습니다.

```blade
<x-mail::table>
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
</x-mail::table>
```

<a name="customizing-the-components"></a>
<!-- ### Customizing The Components -->
### Customizing The Components

<!-- You may export all of the Markdown notification components to your own application for customization. To export the components, use the `vendor:publish` Artisan command to publish the `laravel-mail` asset tag: -->
모든 마크다운 알림 컴포넌트는 직접 애플리케이션으로 내보내 커스터마이징할 수 있습니다. 컴포넌트를 내보내려면 `vendor:publish` Artisan 명령어에 `laravel-mail` 태그를 지정해 실행합니다.

```shell
php artisan vendor:publish --tag=laravel-mail
```

<!-- This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like. -->
이 명령을 실행하면 마크다운 메일 컴포넌트가 `resources/views/vendor/mail` 디렉터리에 복사됩니다. `mail` 디렉터리 아래에는 각각의 컴포넌트에 대해 HTML 버전과 텍스트 버전(plain text)이 들어있는 `html`과 `text` 디렉터리가 생성됩니다. 이 컴포넌트들은 원하는 대로 자유롭게 수정할 수 있습니다.

<a name="customizing-the-css"></a>
<!-- #### Customizing The CSS -->
#### Customizing The CSS

<!-- After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be in-lined within the HTML representations of your Markdown notifications. -->
컴포넌트 내보내기 작업을 완료하면, `resources/views/vendor/mail/html/themes` 경로 아래에 `default.css` 파일이 만들어집니다. 이 CSS 파일을 수정하면 스타일이 자동으로 마크다운 알림의 HTML 표현에 인라인되어 적용됩니다.

<!-- If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of the `mail` configuration file to match the name of your new theme. -->
Laravel 마크다운 컴포넌트에 대해 완전히 새로운 테마를 만들고 싶은 경우, `html/themes` 디렉터리에 새 CSS 파일을 생성해서 넣으면 됩니다. 파일명을 정한 후, `mail` 설정 파일의 `theme` 옵션을 새로운 테마명과 일치하도록 변경해주면 적용됩니다.

<!-- To customize the theme for an individual notification, you may call the `theme` method while building the notification's mail message. The `theme` method accepts the name of the theme that should be used when sending the notification: -->
특정 알림 하나에만 별도의 테마를 적용하려면, 알림의 메일 메시지를 생성할 때 `theme` 메서드를 호출하면 됩니다. `theme` 메서드는 알림을 보낼 때 사용할 테마 이름을 인수로 받습니다.

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\MailMessage
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->theme('invoice')
                ->subject('Invoice Paid')
                ->markdown('mail.invoice.paid', ['url' => $url]);
}
```

<a name="database-notifications"></a>
<!-- ## Database Notifications -->
## Database Notifications

<a name="database-prerequisites"></a>
<!-- ### Prerequisites -->
### Prerequisites

<!-- The `database` notification channel stores the notification information in a database table. This table will contain information such as the notification type as well as a JSON data structure that describes the notification. -->
`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 종류, 그리고 알림을 설명하는 JSON 구조의 데이터 등이 포함됩니다.

<!-- You can query the table to display the notifications in your application's user interface. But, before you can do that, you will need to create a database table to hold your notifications. You may use the `notifications:table` command to generate a [migration](/docs/9.x/migrations) with the proper table schema: -->
저장된 알림들은 애플리케이션 UI에서 조회해 보여줄 수 있습니다. 하지만 먼저 알림 데이터를 저장할 데이터베이스 테이블을 생성해야 합니다. [migration](/docs/9.x/migrations)을 위한 적절한 테이블 스키마를 자동으로 생성하려면 `notifications:table` Artisan 명령어를 사용하세요.

```shell
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
<!-- ### Formatting Database Notifications -->
### Formatting Database Notifications

<!-- If a notification supports being stored in a database table, you should define a `toDatabase` or `toArray` method on the notification class. This method will receive a `$notifiable` entity and should return a plain PHP array. The returned array will be encoded as JSON and stored in the `data` column of your `notifications` table. Let's take a look at an example `toArray` method: -->
알림을 데이터베이스 테이블에 저장하려면, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 전달받고, 순수 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON 형태로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 아래는 `toArray` 메서드 예시입니다.

```
/**
 * Get the array representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function toArray($notifiable)
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```

<a name="todatabase-vs-toarray"></a>
<!-- #### `toDatabase` Vs. `toArray` -->
#### `toDatabase` Vs. `toArray`

<!-- The `toArray` method is also used by the `broadcast` channel to determine which data to broadcast to your JavaScript powered frontend. If you would like to have two different array representations for the `database` and `broadcast` channels, you should define a `toDatabase` method instead of a `toArray` method. -->
`toArray` 메서드는 `broadcast` 채널에서도 데이터를 수집하는 데에 사용됩니다. 만약 `database` 채널과 `broadcast` 채널에서 서로 다른 데이터 구조를 반환하고 싶다면, `toArray` 대신 `toDatabase` 메서드를 별도로 정의해야 합니다.

<a name="accessing-the-notifications"></a>
<!-- ### Accessing The Notifications -->
### Accessing The Notifications

<!-- Once notifications are stored in the database, you need a convenient way to access them from your notifiable entities. The `Illuminate\Notifications\Notifiable` trait, which is included on Laravel's default `App\Models\User` model, includes a `notifications` [Eloquent relationship](/docs/9.x/eloquent-relationships) that returns the notifications for the entity. To fetch notifications, you may access this method like any other Eloquent relationship. By default, notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
알림이 데이터베이스에 저장된 후에는, 알림을 받을 엔터티에서 쉽게 접근할 수 있어야 합니다. Laravel의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트는 해당 엔터티의 알림들을 반환하는 `notifications` [Eloquent relationship](/docs/9.x/eloquent-relationships)를 제공합니다. 이 메서드는 다른 Eloquent 연관관계와 똑같이 접근할 수 있습니다. 알림은 기본적으로 `created_at` 타임스탬프 기준으로 가장 최근 것이 맨 앞에 오도록 정렬됩니다.

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

<!-- If you want to retrieve only the "unread" notifications, you may use the `unreadNotifications` relationship. Again, these notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
읽지 않은(unread) 알림만 가져오고 싶다면, `unreadNotifications` 연관관계를 사용할 수 있습니다. 역시 이 알림들도 `created_at` 타임스탬프 기준으로 최근 알림이 우선 정렬되어 있습니다.

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> 자바스크립트 클라이언트에서 알림에 접근하려면, 애플리케이션에 알림 컨트롤러를 만들고, 현재 사용자 등 특정 notifiable 엔터티의 알림을 반환해야 합니다. 그런 뒤 클라이언트에서 HTTP 요청을 해당 컨트롤러 URL로 보내 알림을 받아올 수 있습니다.

<a name="marking-notifications-as-read"></a>
<!-- ### Marking Notifications As Read -->
### Marking Notifications As Read

<!-- Typically, you will want to mark a notification as "read" when a user views it. The `Illuminate\Notifications\Notifiable` trait provides a `markAsRead` method, which updates the `read_at` column on the notification's database record: -->
일반적으로 사용자가 알림을 확인(조회)하면 해당 알림의 상태를 "읽음(read)"으로 표시하게 됩니다. `Illuminate\Notifications\Notifiable` 트레이트의 `markAsRead` 메서드를 사용하면, 알림의 데이터베이스 레코드의 `read_at` 컬럼을 업데이트하여 읽음 처리할 수 있습니다.

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

<!-- However, instead of looping through each notification, you may use the `markAsRead` method directly on a collection of notifications: -->
각각의 알림에 대해 일일이 반복문을 돌릴 필요 없이, 알림 컬렉션 전체에 대해 직접 `markAsRead`를 호출할 수도 있습니다.

```
$user->unreadNotifications->markAsRead();
```

<!-- You may also use a mass-update query to mark all of the notifications as read without retrieving them from the database: -->
알림을 모두 읽음 상태로 일괄 처리하면서 데이터베이스에서 가져오지 않고 직접 업데이트 쿼리를 실행하고 싶다면 다음과 같이 할 수 있습니다.

```
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

<!-- You may `delete` the notifications to remove them from the table entirely: -->
테이블에서 알림을 완전히 삭제하려면 `delete` 메서드를 사용합니다.

```
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
<!-- ## Broadcast Notifications -->
## Broadcast Notifications

<a name="broadcast-prerequisites"></a>
<!-- ### Prerequisites -->
### Prerequisites

<!-- Before broadcasting notifications, you should configure and be familiar with Laravel's [event broadcasting](/docs/9.x/broadcasting) services. Event broadcasting provides a way to react to server-side Laravel events from your JavaScript powered frontend. -->
브로드캐스트 알림을 사용하려면 Laravel의 [event broadcasting](/docs/9.x/broadcasting) 기능을 사전에 구성하고 익숙해지는 것이 필요합니다. 이벤트 브로드캐스팅은 서버에서 발생한 Laravel 이벤트에 자바스크립트 기반 프론트엔드가 즉시 반응할 수 있도록 해주는 기술입니다.

<a name="formatting-broadcast-notifications"></a>
<!-- ### Formatting Broadcast Notifications -->
### Formatting Broadcast Notifications

<!-- The `broadcast` channel broadcasts notifications using Laravel's [event broadcasting](/docs/9.x/broadcasting) services, allowing your JavaScript powered frontend to catch notifications in realtime. If a notification supports broadcasting, you can define a `toBroadcast` method on the notification class. This method will receive a `$notifiable` entity and should return a `BroadcastMessage` instance. If the `toBroadcast` method does not exist, the `toArray` method will be used to gather the data that should be broadcast. The returned data will be encoded as JSON and broadcast to your JavaScript powered frontend. Let's take a look at an example `toBroadcast` method: -->
`broadcast` 채널은 Laravel의 [event broadcasting](/docs/9.x/broadcasting) 기능을 이용하여 알림을 실시간으로 자바스크립트 프론트엔드로 브로드캐스트합니다. 알림을 브로드캐스트하도록 지원하려면 알림 클래스에 `toBroadcast` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable` 엔터티를 전달받고, `BroadcastMessage` 인스턴스를 반환해야 합니다. 만약 `toBroadcast`가 없다면, `toArray` 메서드의 반환값으로 브로드캐스트할 데이터를 자동으로 수집합니다. 반환된 데이터는 JSON으로 변환되어 자바스크립트 프론트엔드로 전달됩니다. 아래는 `toBroadcast` 메서드의 예시입니다.

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the broadcastable representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return BroadcastMessage
 */
public function toBroadcast($notifiable)
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```

<a name="broadcast-queue-configuration"></a>
<!-- #### Broadcast Queue Configuration -->
#### Broadcast Queue Configuration

<!-- All broadcast notifications are queued for broadcasting. If you would like to configure the queue connection or queue name that is used to queue the broadcast operation, you may use the `onConnection` and `onQueue` methods of the `BroadcastMessage`: -->
모든 브로드캐스트 알림은 큐에 등록되어 비동기적으로 전송됩니다. 브로드캐스트 작업을 어떤 큐 커넥션이나 큐 이름을 사용해 처리할지 지정하려면 `BroadcastMessage`의 `onConnection`과 `onQueue` 메서드를 사용하면 됩니다.

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
<!-- #### Customizing The Notification Type -->
#### Customizing The Notification Type

<!-- In addition to the data you specify, all broadcast notifications also have a `type` field containing the full class name of the notification. If you would like to customize the notification `type`, you may define a `broadcastType` method on the notification class: -->
직접 지정한 데이터 이외에도, 모든 브로드캐스트 알림에는 알림 전체 클래스 이름을 담고 있는 `type` 필드가 포함됩니다. 이 `type` 값을 커스터마이즈하고 싶다면, 알림 클래스에 `broadcastType` 메서드를 정의하십시오.

```
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the type of the notification being broadcast.
 *
 * @return string
 */
public function broadcastType()
{
    return 'broadcast.message';
}
```

<a name="listening-for-notifications"></a>
<!-- ### Listening For Notifications -->
### Listening For Notifications

<!-- Notifications will broadcast on a private channel formatted using a `{notifiable}.{id}` convention. So, if you are sending a notification to an `App\Models\User` instance with an ID of `1`, the notification will be broadcast on the `App.Models.User.1` private channel. When using [Laravel Echo](/docs/9.x/broadcasting#client-side-installation), you may easily listen for notifications on a channel using the `notification` method: -->
알림은 `{notifiable}.{id}` 규칙에 따라 생성되는 프라이빗 채널에 브로드캐스트됩니다. 예를 들어, `App\Models\User` 인스턴스의 ID가 `1`이면 `App.Models.User.1` 프라이빗 채널로 알림이 전송됩니다. [Laravel Echo](/docs/9.x/broadcasting#client-side-installation)를 이용하면, 해당 채널에서 손쉽게 `notification` 메서드로 알림 이벤트를 구독할 수 있습니다.

```
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="customizing-the-notification-channel"></a>
<!-- #### Customizing The Notification Channel -->
#### Customizing The Notification Channel

<!-- If you would like to customize which channel that an entity's broadcast notifications are broadcast on, you may define a `receivesBroadcastNotificationsOn` method on the notifiable entity: -->
엔터티가 어떤 채널로 브로드캐스트 알림을 받을지 직접 지정하려면, notifiable 엔터티 내에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다.

```
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
     *
     * @return string
     */
    public function receivesBroadcastNotificationsOn()
    {
        return 'users.'.$this->id;
    }
}
```

<a name="sms-notifications"></a>
<!-- ## SMS Notifications -->
## SMS Notifications

<a name="sms-prerequisites"></a>
<!-- ### Prerequisites -->
### Prerequisites

<!-- Sending SMS notifications in Laravel is powered by [Vonage](https://www.vonage.com/) (formerly known as Nexmo). Before you can send notifications via Vonage, you need to install the `laravel/vonage-notification-channel` and `guzzlehttp/guzzle` packages: -->
Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 이름: Nexmo)를 이용해 전송됩니다. Vonage를 통해 알림을 전송하려면, `laravel/vonage-notification-channel` 및 `guzzlehttp/guzzle` 패키지를 설치해야 합니다.

```
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

<!-- The package includes a [configuration file](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php). However, you are not required to export this configuration file to your own application. You can simply use the `VONAGE_KEY` and `VONAGE_SECRET` environment variables to define your Vonage public and secret keys. -->
이 패키지에는 [configuration file](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있습니다. 하지만 반드시 이 설정 파일을 직접 애플리케이션에 복사할 필요는 없습니다. `VONAGE_KEY`, `VONAGE_SECRET` 환경 변수를 통해 공개키와 시크릿키를 지정해주면 충분합니다.

<!-- After defining your keys, you should set a `VONAGE_SMS_FROM` environment variable that defines the phone number that your SMS messages should be sent from by default. You may generate this phone number within the Vonage control panel: -->
키를 정의한 후에는, SMS를 전송할 기본 전화번호를 결정하기 위해 `VONAGE_SMS_FROM` 환경 변수를 설정해야 합니다. 이 번호는 Vonage 관리자 패널에서 생성할 수 있습니다.

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
<!-- ### Formatting SMS Notifications -->
### Formatting SMS Notifications

<!-- If a notification supports being sent as an SMS, you should define a `toVonage` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\VonageMessage` instance: -->
SMS로 알림을 발송할 때는 알림 클래스에 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 전달받고, `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
<!-- #### Unicode Content -->
#### Unicode Content

<!-- If your SMS message will contain unicode characters, you should call the `unicode` method when constructing the `VonageMessage` instance: -->
SMS 메시지에 유니코드 문자를 포함해야 할 경우, `VonageMessage` 인스턴스를 생성할 때 `unicode` 메서드를 반드시 호출해야 합니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="customizing-the-from-number"></a>
<!-- ### Customizing The "From" Number -->
### Customizing The "From" Number

<!-- If you would like to send some notifications from a phone number that is different from the phone number specified by your `VONAGE_SMS_FROM` environment variable, you may call the `from` method on a `VonageMessage` instance: -->
일부 알림을 `VONAGE_SMS_FROM` 환경 변수에 지정된 번호가 아닌 다른 번호로 발송하고 싶다면, `VonageMessage` 인스턴스의 `from` 메서드를 통해 발신 번호를 개별적으로 지정할 수 있습니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
<!-- ### Adding a Client Reference -->
### Adding a Client Reference

<!-- If you would like to keep track of costs per user, team, or client, you may add a "client reference" to the notification. Vonage will allow you to generate reports using this client reference so that you can better understand a particular customer's SMS usage. The client reference can be any string up to 40 characters: -->
사용자, 팀, 또는 고객별로 SMS 비용을 추적하고 싶다면 알림에 "client reference" 값을 추가할 수 있습니다. Vonage는 이 참조 값을 활용해서 특정 고객의 SMS 사용량을 포함하는 보고서를 제공합니다. client reference는 최대 40자까지 임의의 문자열을 지정할 수 있습니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\VonageMessage
 */
public function toVonage($notifiable)
{
    return (new VonageMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>

<!-- ### Routing SMS Notifications -->
### Routing SMS Notifications

<!-- To route Vonage notifications to the proper phone number, define a `routeNotificationForVonage` method on your notifiable entity: -->
Vonage 알림을 올바른 전화번호로 전송하려면, 알림을 받을 엔티티에 `routeNotificationForVonage` 메서드를 정의해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Vonage channel.
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForVonage($notification)
    {
        return $this->phone_number;
    }
}
```

<a name="slack-notifications"></a>
<!-- ## Slack Notifications -->
## Slack Notifications

<a name="slack-prerequisites"></a>
<!-- ### Prerequisites -->
### Prerequisites

<!-- Before you can send notifications via Slack, you must install the Slack notification channel via Composer: -->
Slack을 통해 알림을 전송하려면, 먼저 Composer를 이용해 Slack 알림 채널을 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```

<!-- You will also need to create a [Slack App](https://api.slack.com/apps?new_app=1) for your team. After creating the App, you should configure an "Incoming Webhook" for the workspace. Slack will then provide you with a webhook URL that you may use when [routing Slack notifications](#routing-slack-notifications). -->
또한 팀을 위한 [Slack App](https://api.slack.com/apps?new_app=1)을 생성해야 합니다. 앱을 만들고 나서 워크스페이스에 대해 "Incoming Webhook"을 설정해야 하며, 설정이 완료되면 Slack에서 웹훅 URL을 제공합니다. 이 URL은 [routing Slack notifications](#routing-slack-notifications) 시 사용하게 됩니다.

<a name="formatting-slack-notifications"></a>
<a id="formatting-shortcode-notifications" data-translation-alias="true"></a>
<!-- ### Formatting Slack Notifications -->
### Formatting Slack Notifications

<!-- If a notification supports being sent as a Slack message, you should define a `toSlack` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\SlackMessage` instance. Slack messages may contain text content as well as an "attachment" that formats additional text or an array of fields. Let's take a look at a basic `toSlack` example: -->
알림을 Slack 메시지로 전송하고 싶다면 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받으며, 반드시 `Illuminate\Notifications\Messages\SlackMessage` 인스턴스를 반환해야 합니다. Slack 메시지는 텍스트 콘텐츠뿐 아니라 추가 정보를 표현할 수 있는 "첨부(attachment)"도 포함할 수 있습니다. 기본적인 `toSlack` 예시를 살펴보겠습니다:

```
/**
 * Get the Slack representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\SlackMessage
 */
public function toSlack($notifiable)
{
    return (new SlackMessage)
                ->content('One of your invoices has been paid!');
}
```

<a name="slack-attachments"></a>
<!-- ### Slack Attachments -->
### Slack Attachments

<!-- You may also add "attachments" to Slack messages. Attachments provide richer formatting options than simple text messages. In this example, we will send an error notification about an exception that occurred in an application, including a link to view more details about the exception: -->
Slack 메시지에는 "첨부(attachment)"도 추가할 수 있습니다. 첨부 기능을 사용하면 단순한 텍스트 메시지보다 더 풍부한 포맷을 제공할 수 있습니다. 아래는 애플리케이션에서 발생한 예외에 대해 오류 메시지와 추가 상세 페이지 링크를 첨부하여 알림을 보내는 예시입니다:

```
/**
 * Get the Slack representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was not found.');
                });
}
```

<!-- Attachments also allow you to specify an array of data that should be presented to the user. The given data will be presented in a table-style format for easy reading: -->
첨부를 이용하면 사용자에게 보여줄 데이터 배열도 지정할 수 있습니다. 이 데이터는 표 형태로 정리되어 읽기 쉽게 표시됩니다:

```
/**
 * Get the Slack representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/invoices/'.$this->invoice->id);

    return (new SlackMessage)
                ->success()
                ->content('One of your invoices has been paid!')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Invoice 1322', $url)
                               ->fields([
                                    'Title' => 'Server Expenses',
                                    'Amount' => '$1,234',
                                    'Via' => 'American Express',
                                    'Was Overdue' => ':-1:',
                                ]);
                });
}
```

<a name="markdown-attachment-content"></a>
<!-- #### Markdown Attachment Content -->
#### Markdown Attachment Content

<!-- If some of your attachment fields contain Markdown, you may use the `markdown` method to instruct Slack to parse and display the given attachment fields as Markdown formatted text. The values accepted by this method are: `pretext`, `text`, and / or `fields`. For more information about Slack attachment formatting, check out the [Slack API documentation](https://api.slack.com/docs/message-formatting#message_formatting): -->
첨부 필드 중에 마크다운(Markdown)이 포함된 경우, `markdown` 메서드를 사용하여 Slack에게 해당 첨부 필드를 마크다운 형식으로 파싱하여 보여줄 것을 지정할 수 있습니다. 이 메서드에는 `pretext`, `text`, 그리고/또는 `fields` 값을 전달할 수 있습니다. Slack 첨부 포맷에 대한 자세한 정보는 [Slack API documentation](https://api.slack.com/docs/message-formatting#message_formatting)를 참고하시기 바랍니다:

```
/**
 * Get the Slack representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return SlackMessage
 */
public function toSlack($notifiable)
{
    $url = url('/exceptions/'.$this->exception->id);

    return (new SlackMessage)
                ->error()
                ->content('Whoops! Something went wrong.')
                ->attachment(function ($attachment) use ($url) {
                    $attachment->title('Exception: File Not Found', $url)
                               ->content('File [background.jpg] was *not found*.')
                               ->markdown(['text']);
                });
}
```

<a name="routing-slack-notifications"></a>
<!-- ### Routing Slack Notifications -->
### Routing Slack Notifications

<!-- To route Slack notifications to the proper Slack team and channel, define a `routeNotificationForSlack` method on your notifiable entity. This should return the webhook URL to which the notification should be delivered. Webhook URLs may be generated by adding an "Incoming Webhook" service to your Slack team: -->
Slack 알림을 올바른 팀 및 채널로 전송하려면, 알림을 받을 엔티티에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 이 메서드는 알림을 보내야 할 웹훅 URL을 반환해야 합니다. 웹훅 URL은 Slack 팀에 "Incoming Webhook" 서비스를 추가하여 생성할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForSlack($notification)
    {
        return 'https://hooks.slack.com/services/...';
    }
}
```

<a name="localizing-notifications"></a>
<!-- ## Localizing Notifications -->
## Localizing Notifications

<!-- Laravel allows you to send notifications in a locale other than the HTTP request's current locale, and will even remember this locale if the notification is queued. -->
Laravel에서는 HTTP 요청의 현재 로케일과 다른 언어로 알림을 전송할 수 있으며, 알림이 큐에 쌓인 경우에도 선택한 로케일 값을 기억하게 됩니다.

<!-- To accomplish this, the `Illuminate\Notifications\Notification` class offers a `locale` method to set the desired language. The application will change into this locale when the notification is being evaluated and then revert back to the previous locale when evaluation is complete: -->
이 기능을 사용하려면 `Illuminate\Notifications\Notification` 클래스의 `locale` 메서드를 활용하여 원하는 언어를 설정할 수 있습니다. 알림이 처리되는 동안 애플리케이션의 로케일이 해당 언어로 변경되었다가, 처리가 끝나면 다시 이전 로케일로 돌아갑니다:

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

<!-- Localization of multiple notifiable entries may also be achieved via the `Notification` facade: -->
여러 사용자에게 알림을 다국어로 전송하려면 `Notification` 파사드를 통해서도 가능합니다:

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
<!-- ### User Preferred Locales -->
### User Preferred Locales

<!-- Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on your notifiable model, you may instruct Laravel to use this stored locale when sending a notification: -->
애플리케이션에서 각 사용자의 기본 로케일 정보를 저장하고 있다면, 알림을 받을 모델에 `HasLocalePreference` 컨트랙트를 구현하면 저장된 로케일을 알림 전송 시 자동으로 사용할 수 있습니다:

```
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     *
     * @return string
     */
    public function preferredLocale()
    {
        return $this->locale;
    }
}
```

<!-- Once you have implemented the interface, Laravel will automatically use the preferred locale when sending notifications and mailables to the model. Therefore, there is no need to call the `locale` method when using this interface: -->
이 인터페이스를 구현한 후에는 Laravel이 자동으로 해당 모델에 대한 알림과 메일 전송 시 선호 로케일을 적용합니다. 따라서 별도로 `locale` 메서드를 호출할 필요가 없습니다:

```
$user->notify(new InvoicePaid($invoice));
```

<a name="notification-events"></a>
<!-- ## Notification Events -->
## Notification Events

<a name="notification-sending-event"></a>
<!-- #### Notification Sending Event -->
#### Notification Sending Event

<!-- When a notification is sending, the `Illuminate\Notifications\Events\NotificationSending` [event](/docs/9.x/events) is dispatched by the notification system. This contains the "notifiable" entity and the notification instance itself. You may register listeners for this event in your application's `EventServiceProvider`: -->
알림이 전송될 때마다, Laravel의 알림 시스템은 `Illuminate\Notifications\Events\NotificationSending` [event](/docs/9.x/events)를 발생시킵니다. 이 이벤트에는 "알림 대상" 엔티티와 알림 인스턴스가 포함됩니다. `EventServiceProvider`에서 이 이벤트 리스너를 등록할 수 있습니다:

```
use App\Listeners\CheckNotificationStatus;
use Illuminate\Notifications\Events\NotificationSending;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    NotificationSending::class => [
        CheckNotificationStatus::class,
    ],
];
```

<!-- The notification will not be sent if an event listener for the `NotificationSending` event returns `false` from its `handle` method: -->
`NotificationSending` 이벤트 리스너의 `handle` 메서드에서 `false`를 반환하면 해당 알림은 실제로 전송되지 않습니다:

```
use Illuminate\Notifications\Events\NotificationSending;

/**
 * Handle the event.
 *
 * @param  \Illuminate\Notifications\Events\NotificationSending  $event
 * @return void
 */
public function handle(NotificationSending $event)
{
    return false;
}
```

<!-- Within an event listener, you may access the `notifiable`, `notification`, and `channel` properties on the event to learn more about the notification recipient or the notification itself: -->
이벤트 리스너 내에서는 이벤트 객체의 `notifiable`, `notification`, `channel` 속성을 통해, 알림 수신자 및 알림에 대한 추가 정보를 조회할 수 있습니다:

```
/**
 * Handle the event.
 *
 * @param  \Illuminate\Notifications\Events\NotificationSending  $event
 * @return void
 */
public function handle(NotificationSending $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```

<a name="notification-sent-event"></a>
<!-- #### Notification Sent Event -->
#### Notification Sent Event

<!-- When a notification is sent, the `Illuminate\Notifications\Events\NotificationSent` [event](/docs/9.x/events) is dispatched by the notification system. This contains the "notifiable" entity and the notification instance itself. You may register listeners for this event in your `EventServiceProvider`: -->
알림이 전송된 후에는 `Illuminate\Notifications\Events\NotificationSent` [event](/docs/9.x/events)가 Dispatcher에 의해 발생합니다. 이 이벤트에도 역시 "알림 대상" 엔티티와 알림 인스턴스가 포함되어 있습니다. `EventServiceProvider`에 아래와 같이 리스너를 등록할 수 있습니다:

```
use App\Listeners\LogNotification;
use Illuminate\Notifications\Events\NotificationSent;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    NotificationSent::class => [
        LogNotification::class,
    ],
];
```

> [!NOTE]
> `EventServiceProvider`에 리스너를 등록한 후에는, `event:generate` 아티즌 명령어를 사용하여 리스너 클래스를 빠르게 생성할 수 있습니다.

<!-- Within an event listener, you may access the `notifiable`, `notification`, `channel`, and `response` properties on the event to learn more about the notification recipient or the notification itself: -->
이벤트 리스너 내에서는 이벤트 객체의 `notifiable`, `notification`, `channel`, `response` 속성을 통해 알림 수신자나 알림 자체에 대한 다양한 정보를 얻을 수 있습니다:

```
/**
 * Handle the event.
 *
 * @param  \Illuminate\Notifications\Events\NotificationSent  $event
 * @return void
 */
public function handle(NotificationSent $event)
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```

<a name="custom-channels"></a>
<!-- ## Custom Channels -->
## Custom Channels

<!-- Laravel ships with a handful of notification channels, but you may want to write your own drivers to deliver notifications via other channels. Laravel makes it simple. To get started, define a class that contains a `send` method. The method should receive two arguments: a `$notifiable` and a `$notification`. -->
Laravel은 여러 기본 알림 채널을 제공하지만, 필요에 따라 직접 드라이버(커스텀 채널)를 만들어 알림을 다른 방식으로 전송할 수 있습니다. Laravel에서 이를 구현하는 방법은 매우 간단합니다. 우선, `send` 메서드를 포함한 클래스를 하나 정의합니다. 이 메서드는 `$notifiable`과 `$notification` 두 개의 인자를 받게 됩니다.

<!-- Within the `send` method, you may call methods on the notification to retrieve a message object understood by your channel and then send the notification to the `$notifiable` instance however you wish: -->
`send` 메서드 내부에서는 알림 객체에서 각 채널이 이해할 수 있는 메시지 오브젝트를 꺼내고, 원하는 방식대로 `$notifiable` 인스턴스에 알림을 전송하면 됩니다:

```
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * Send the given notification.
     *
     * @param  mixed  $notifiable
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return void
     */
    public function send($notifiable, Notification $notification)
    {
        $message = $notification->toVoice($notifiable);

        // Send notification to the $notifiable instance...
    }
}
```

<!-- Once your notification channel class has been defined, you may return the class name from the `via` method of any of your notifications. In this example, the `toVoice` method of your notification can return whatever object you choose to represent voice messages. For example, you might define your own `VoiceMessage` class to represent these messages: -->
알림 채널 클래스를 정의했다면, 이제 알림 클래스의 `via` 메서드에서 해당 클래스명을 반환하면 됩니다. 아래 예제에서는 알림의 `toVoice` 메서드가 음성 메시지를 표현하는 임의의 객체를 반환합니다. 필요하다면 알림 메시지에 맞는 `VoiceMessage` 클래스를 직접 정의해서 활용할 수 있습니다:

```
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
     *
     * @param  mixed  $notifiable
     * @return array|string
     */
    public function via($notifiable)
    {
        return [VoiceChannel::class];
    }

    /**
     * Get the voice representation of the notification.
     *
     * @param  mixed  $notifiable
     * @return VoiceMessage
     */
    public function toVoice($notifiable)
    {
        // ...
    }
}
```
