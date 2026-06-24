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

<!-- In addition to support for [sending email](/docs/8.x/mail), Laravel provides support for sending notifications across a variety of delivery channels, including email, SMS (via [Vonage](https://www.vonage.com/communications-apis/), formerly known as Nexmo), and [Slack](https://slack.com). In addition, a variety of [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel) have been created to send notification over dozens of different channels! Notifications may also be stored in a database so they may be displayed in your web interface. -->
Laravel은 [sending email](/docs/8.x/mail) 기능을 기본적으로 제공할 뿐만 아니라, 이메일, SMS([Vonage](https://www.vonage.com/communications-apis/), 예전 명칭은 Nexmo), [Slack](https://slack.com) 등 다양한 전달 채널을 통한 알림 발송도 지원합니다. 또한, [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel)도 마련되어 있어, 수십 가지 이상의 채널로 알림을 손쉽게 전송할 수 있습니다! 알림은 데이터베이스에 저장해 웹 인터페이스 내에서 사용자에게 보여줄 수도 있습니다.

<!-- Typically, notifications should be short, informational messages that notify users of something that occurred in your application. For example, if you are writing a billing application, you might send an "Invoice Paid" notification to your users via the email and SMS channels. -->
일반적으로 알림은 애플리케이션에서 어떤 일이 발생했음을 사용자가 빠르게 알 수 있도록 해주는 짧고 정보성 메시지입니다. 예를 들어, 결제 관련 애플리케이션을 만든다면, 사용자의 청구서가 결제됨을 "Invoice Paid(청구서 결제 완료)" 알림을 이메일이나 SMS 채널을 통해 전달할 수 있습니다.

<a name="generating-notifications"></a>
<!-- ## Generating Notifications -->
## Generating Notifications

<!-- In Laravel, each notification is represented by a single class that is typically stored in the `app/Notifications` directory. Don't worry if you don't see this directory in your application - it will be created for you when you run the `make:notification` Artisan command: -->
Laravel에서 각 알림은 일반적으로 `app/Notifications` 디렉터리에 저장되는 하나의 클래스로 표현됩니다. 만약 이 디렉터리가 애플리케이션에 없다면 걱정하지 마십시오. `make:notification` 아티즌 명령어를 실행하면 자동으로 생성됩니다.

```
php artisan make:notification InvoicePaid
```

<!-- This command will place a fresh notification class in your `app/Notifications` directory. Each notification class contains a `via` method and a variable number of message building methods, such as `toMail` or `toDatabase`, that convert the notification to a message tailored for that particular channel. -->
이 명령은 `app/Notifications` 디렉터리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스는 `via` 메서드, 그리고 `toMail`, `toDatabase`와 같이 특정 채널에 맞춘 메시지를 만들어 내는 다양한 메서드들을 포함합니다. 이 메서드들은 각각의 채널에 알맞게 알림을 메시지로 변환합니다.

<a name="sending-notifications"></a>
<!-- ## Sending Notifications -->
## Sending Notifications

<a name="using-the-notifiable-trait"></a>
<!-- ### Using The Notifiable Trait -->
### Using The Notifiable Trait

<!-- Notifications may be sent in two ways: using the `notify` method of the `Notifiable` trait or using the `Notification` [facade](/docs/8.x/facades). The `Notifiable` trait is included on your application's `App\Models\User` model by default: -->
알림을 보내는 방법에는 두 가지가 있습니다. 첫 번째는 `Notifiable` 트레잇의 `notify` 메서드를 사용하는 것이고, 두 번째는 `Notification` [facade](/docs/8.x/facades)를 사용하는 방법입니다. 애플리케이션의 `App\Models\User` 모델에는 기본적으로 `Notifiable` 트레잇이 포함되어 있습니다.

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
이 트레잇에서 제공하는 `notify` 메서드는 알림 인스턴스를 인수로 받습니다.

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!TIP]
> `Notifiable` 트레잇은 어떤 모델에나 사용할 수 있습니다. 반드시 `User` 모델에만 적용해야 하는 것은 아닙니다.

<a name="using-the-notification-facade"></a>
<!-- ### Using The Notification Facade -->
### Using The Notification Facade

<!-- Alternatively, you may send notifications via the `Notification` [facade](/docs/8.x/facades). This approach is useful when you need to send a notification to multiple notifiable entities such as a collection of users. To send notifications using the facade, pass all of the notifiable entities and the notification instance to the `send` method: -->
또 다른 방법으로, `Notification` [facade](/docs/8.x/facades)를 이용해 알림을 보낼 수도 있습니다. 이 방법은 여러 개의 알림 대상(예: 유저 컬렉션)에게 동시에 알림을 보낼 때 유용합니다. 파사드를 사용할 때는, 모든 알림 대상 엔티티들과 알림 인스턴스를 `send` 메서드에 전달하면 됩니다.

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

<!-- You can also send notifications immediately using the `sendNow` method. This method will send the notification immediately even if the notification implements the `ShouldQueue` interface: -->
또한, `sendNow` 메서드를 사용하면 큐에 상관없이 즉시 알림을 전송할 수 있습니다. 이 메서드는 알림이 `ShouldQueue` 인터페이스를 구현했더라도 무시하고 즉시 전송합니다.

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
<!-- ### Specifying Delivery Channels -->
### Specifying Delivery Channels

<!-- Every notification class has a `via` method that determines on which channels the notification will be delivered. Notifications may be sent on the `mail`, `database`, `broadcast`, `nexmo`, and `slack` channels. -->
모든 알림 클래스에는 해당 알림이 어떤 채널로 전송될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `nexmo`, `slack` 등 다양한 채널로 보낼 수 있습니다.

> [!TIP]
> Telegram, Pusher 등 다른 전달 채널도 사용하고 싶으시다면, 커뮤니티가 운영하는 [Laravel Notification Channels website](http://laravel-notification-channels.com)를 참고해 보세요.

<!-- The `via` method receives a `$notifiable` instance, which will be an instance of the class to which the notification is being sent. You may use `$notifiable` to determine which channels the notification should be delivered on: -->
`via` 메서드는 `$notifiable` 인스턴스를 인수로 받으며, 이 인스턴스는 해당 알림을 전달받게 될 클래스의 인스턴스입니다. `$notifiable` 객체의 정보를 바탕으로 알림을 전달할 채널을 동적으로 지정할 수도 있습니다.

```
/**
 * Get the notification's delivery channels.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function via($notifiable)
{
    return $notifiable->prefers_sms ? ['nexmo'] : ['mail', 'database'];
}
```

<a name="queueing-notifications"></a>
<!-- ### Queueing Notifications -->
### Queueing Notifications

> [!NOTE]
> 알림을 큐에 등록하기 전에, 반드시 큐 설정을 마치고 [start a worker](/docs/8.x/queues)해야 합니다.

<!-- Sending notifications can take time, especially if the channel needs to make an external API call to deliver the notification. To speed up your application's response time, let your notification be queued by adding the `ShouldQueue` interface and `Queueable` trait to your class. The interface and trait are already imported for all notifications generated using the `make:notification` command, so you may immediately add them to your notification class: -->
알림을 보내는 작업은, 외부 API 호출 등이 수반될 경우 시간이 오래 걸릴 수 있습니다. 애플리케이션의 응답 속도를 높이고 싶다면, 알림을 큐에 등록해서 백그라운드로 처리할 수 있습니다. 이를 위해서는 알림 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레잇을 추가해야 합니다. `make:notification` 명령으로 생성한 알림 클래스에는 해당 인터페이스와 트레잇이 이미 임포트되어 있으니, 바로 아래와 같이 사용하시면 됩니다.

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
`ShouldQueue` 인터페이스를 추가한 후에는 평소와 같이 알림을 보내면 됩니다. Laravel은 클래스에 `ShouldQueue` 인터페이스가 있는지 감지해서, 자동으로 알림 전송을 큐에 등록합니다.

```
$user->notify(new InvoicePaid($invoice));
```

<!-- If you would like to delay the delivery of the notification, you may chain the `delay` method onto your notification instantiation: -->
알림 전달을 지연시키고 싶다면, 알림 인스턴스를 만들 때 `delay` 메서드를 체이닝(chaining)하면 됩니다.

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<!-- You may pass an array to the `delay` method to specify the delay amount for specific channels: -->
특정 채널별로 지연 시간을 따로두고 싶은 경우에는 `delay` 메서드에 배열을 넘겨주면 됩니다.

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

<!-- When queueing notifications, a queued job will be created for each recipient and channel combination. For example, six jobs will be dispatched to the queue if your notification has three recipients and two channels. -->
알림을 큐로 보낼 때는, 수신자와 채널의 조합마다 하나씩 큐 작업이 생성됩니다. 예를 들어, 알림 대상이 3명이고 채널도 2개라면, 총 6개의 작업이 큐에 등록됩니다.

<a name="customizing-the-notification-queue-connection"></a>
<!-- #### Customizing The Notification Queue Connection -->
#### Customizing The Notification Queue Connection

<!-- By default, queued notifications will be queued using your application's default queue connection. If you would like to specify a different connection that should be used for a particular notification, you may define a `$connection` property on the notification class: -->
기본적으로 큐잉된 알림은 애플리케이션의 기본 큐 연결을 사용하게 됩니다. 하지만 특정 알림만 별도의 큐 연결을 사용하고 싶다면, 알림 클래스에 `$connection` 속성을 지정할 수 있습니다.

```
/**
 * The name of the queue connection to use when queueing the notification.
 *
 * @var string
 */
public $connection = 'redis';
```

<a name="customizing-notification-channel-queues"></a>
<!-- #### Customizing Notification Channel Queues -->
#### Customizing Notification Channel Queues

<!-- If you would like to specify a specific queue that should be used for each notification channel supported by the notification, you may define a `viaQueues` method on your notification. This method should return an array of channel name / queue name pairs: -->
알림 클래스에서는 채널마다 서로 다른 큐를 사용할 수도 있습니다. 이를 위해 알림 클래스에 `viaQueues` 메서드를 정의하세요. 이 메서드는 채널명과 큐명 쌍을 포함하는 배열을 반환해야 합니다.

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
데이터베이스 트랜잭션 내부에서 큐잉된 알림을 디스패치하면, 트랜잭션 커밋 이전에 큐에서 즉시 처리될 수 있습니다. 이렇게 되면 트랜잭션 내에서 변경된 모델이나 테이블 내용이 실제 DB에 반영되기 전에 알림 작업이 실행될 수 있습니다. 트랜잭션 중 생성된 모델/레코드가 아직 DB에 없다면, 알림에서 해당 모델에 의존하는 경우 예기치 않은 오류가 발생할 수 있습니다.

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued notification should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the notification: -->
만약 큐 연결의 `after_commit` 설정값이 `false`라면, 알림을 보낼 때 `afterCommit` 메서드를 호출하여 반드시 모든 오픈된 DB 트랜잭션 커밋 이후에 큐 작업이 디스패치되도록 지정할 수 있습니다.

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

<!-- Alternatively, you may call the `afterCommit` method from your notification's constructor: -->
또는, 알림 클래스의 생성자에서 `afterCommit` 메서드를 호출할 수도 있습니다.

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

> [!TIP]
> 이런 문제에 대한 자세한 내용은 [queued jobs and database transactions](/docs/8.x/queues#jobs-and-database-transactions) 문서를 참고하십시오.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
<!-- #### Determining If A Queued Notification Should Be Sent -->
#### Determining If A Queued Notification Should Be Sent

<!-- After a queued notification has been dispatched for the queue for background processing, it will typically be accepted by a queue worker and sent to its intended recipient. -->
큐에 등록된 알림은 일반적으로 백그라운드 워커가 받아서 수신자에게 전송합니다.

<!-- However, if you would like to make the final determination on whether the queued notification should be sent after it is being processed by a queue worker, you may define a `shouldSend` method on the notification class. If this method returns `false`, the notification will not be sent: -->
그러나 큐 워커에서 알림을 처리할 때 실제로 보낼지 최종적으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 알림은 전송되지 않습니다.

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
때로는 애플리케이션의 "유저"로 저장되어 있지 않은 사람에게도 알림을 보내야 할 때가 있습니다. 이럴 때는 `Notification` 파사드의 `route` 메서드를 이용해 임의로 전달 경로를 지정한 뒤 알림을 보낼 수 있습니다.

```
Notification::route('mail', 'taylor@example.com')
            ->route('nexmo', '5555555555')
            ->route('slack', 'https://hooks.slack.com/services/...')
            ->notify(new InvoicePaid($invoice));
```

<!-- If you would like to provide the recipient's name when sending an on-demand notification to the `mail` route, you may provide an array that contains the email address as the key and the name as the value of the first element in the array: -->
온디맨드 알림을 `mail` 경로(route)로 보낼 때 수신자 이름까지 함께 전달하고 싶다면, 배열의 첫 번째 요소에 이메일 주소를 키로, 이름을 값으로 갖는 배열을 전달하면 됩니다.

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
알림이 이메일로 발송되는 것을 지원하려면, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받아서, `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

<!-- The `MailMessage` class contains a few simple methods to help you build transactional email messages. Mail messages may contain lines of text as well as a "call to action". Let's take a look at an example `toMail` method: -->
`MailMessage` 클래스에는 트랜잭션성 이메일 메시지 작성을 도와주는 다양한 간단한 메서드가 포함되어 있습니다. 메일 메시지에는 일반 텍스트뿐만 아니라 "콜 투 액션(call to action)" 버튼도 포함시킬 수 있습니다. 다음은 `toMail` 메서드의 예시입니다.

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
                ->action('View Invoice', $url)
                ->line('Thank you for using our application!');
}
```

> [!TIP]
> 위 예시처럼 `toMail` 메서드에서 `$this->invoice->id`를 사용하고 있습니다. 알림 메시지를 만들 때 필요한 모든 데이터를 생성자에 넣어 넘겨줄 수 있습니다.

<!-- In this example, we register a greeting, a line of text, a call to action, and then another line of text. These methods provided by the `MailMessage` object make it simple and fast to format small transactional emails. The mail channel will then translate the message components into a beautiful, responsive HTML email template with a plain-text counterpart. Here is an example of an email generated by the `mail` channel: -->
이 예시에서는 인사말, 한 줄 메시지, 액션 버튼, 그리고 또 한 줄 메시지를 등록합니다. `MailMessage` 객체가 제공하는 이 메서드들을 활용하면 간단하고 빠르게 트랜잭션성 메일을 포맷할 수 있습니다. 메일 채널은 메시지의 각 요소들을 보기 좋은 반응형 HTML 이메일 템플릿(그리고 평문 텍스트 버전)으로 자동 변환합니다. 아래는 `mail` 채널로 발송된 이메일 예시입니다.

<!-- <img src="https://laravel.com/img/docs/notification-example-2.png"/> -->
<img src="https://laravel.com/img/docs/notification-example-2.png" />

> [!TIP]
> 메일 알림을 보낼 때는 `config/app.php` 설정 파일의 `name` 옵션을 꼭 지정하십시오. 이 값은 메일 알림 메시지의 헤더와 푸터에서 사용됩니다.

<a name="other-mail-notification-formatting-options"></a>
<!-- #### Other Mail Notification Formatting Options -->
#### Other Mail Notification Formatting Options

<!-- Instead of defining the "lines" of text in the notification class, you may use the `view` method to specify a custom template that should be used to render the notification email: -->
알림 클래스에서 "라인" 단위 메시지를 직접 정의하는 대신, `view` 메서드를 사용해 커스텀 템플릿을 지정하여 알림 이메일을 렌더링할 수도 있습니다.

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
메일 메시지에 대해 별도의 평문 템플릿을 사용하고 싶다면, `view` 메서드에 이름이 들어있는 배열을 전달하면 됩니다(두 번째 요소에 평문 템플릿).

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

<a name="error-messages"></a>
<!-- #### Error Messages -->
#### Error Messages

<!-- Some notifications inform users of errors, such as a failed invoice payment. You may indicate that a mail message is regarding an error by calling the `error` method when building your message. When using the `error` method on a mail message, the call to action button will be red instead of black: -->
일부 알림은 청구 실패 등 오류 발생 사실을 사용자에게 알려주는 역할도 합니다. 이런 경우 메시지를 만들 때 `error` 메서드를 호출해 해당 메시지가 에러와 관련됨을 표시할 수 있습니다. `error` 메서드를 호출하면, 콜 투 액션 버튼이 검정이 아니라 빨간색으로 바뀝니다.

```
/**
 * Get the mail representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Message
 */
public function toMail($notifiable)
{
    return (new MailMessage)
                ->error()
                ->subject('Notification Subject')
                ->line('...');
}
```

<a name="customizing-the-sender"></a>
<!-- ### Customizing The Sender -->
### Customizing The Sender

<!-- By default, the email's sender / from address is defined in the `config/mail.php` configuration file. However, you may specify the from address for a specific notification using the `from` method: -->
기본적으로 이메일의 발신자/From 주소 정보는 `config/mail.php` 설정 파일에서 정의됩니다. 하지만, 특정 알림에 대해 발신자 주소를 별도로 지정하고 싶을 때는 `from` 메서드를 사용할 수 있습니다.

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
`mail` 채널로 알림을 보낼 때, 시스템은 기본적으로 알림 대상 엔티티의 `email` 속성을 사용합니다. 만약 알림이 다른 이메일 주소로 전달되길 원한다면, 노티피어블(알림을 받을 수 있는) 엔티티에 `routeNotificationForMail` 메서드를 정의하면 됩니다.

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
기본적으로 이메일 제목(subject)은 알림 클래스명을 "Title Case" 형태로 변환한 값입니다. 예를 들어, 알림 클래스가 `InvoicePaid`라면 이메일 제목은 `Invoice Paid`가 됩니다. 다른 제목을 사용하고 싶다면 메시지 작성 시 `subject` 메서드를 호출하면 됩니다.

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
기본적으로 이메일 알림은 `config/mail.php`에서 지정된 기본 메일러를 사용해 발송됩니다. 하지만 메시지를 만들 때 `mailer` 메서드를 호출하면 다른 메일러로 전송할 수 있습니다.

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
메일 알림에서 사용하는 HTML 및 평문 템플릿을 직접 수정할 수도 있습니다. notification 패키지 리소스를 퍼블리싱하면 커스텀 템플릿을 사용할 수 있으며, 다음 명령어를 실행하면 템플릿 파일들이 `resources/views/vendor/notifications`에 복사됩니다.

```
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- To add attachments to an email notification, use the `attach` method while building your message. The `attach` method accepts the absolute path to the file as its first argument: -->
이메일 알림에 파일을 첨부하려면, 메시지 작성 시 `attach` 메서드를 사용하면 됩니다. `attach` 메서드의 첫 번째 인수로는 파일의 절대 경로를 지정합니다.

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

<!-- When attaching files to a message, you may also specify the display name and / or MIME type by passing an `array` as the second argument to the `attach` method: -->
메시지에 파일을 첨부할 때, `attach` 메서드의 두 번째 인수로 `array`를 전달하여 표시될 파일명이나 MIME 타입을 지정할 수도 있습니다.

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

<!-- Unlike attaching files in mailable objects, you may not attach a file directly from a storage disk using `attachFromStorage`. You should rather use the `attach` method with an absolute path to the file on the storage disk. Alternatively, you could return a [mailable](/docs/8.x/mail#generating-mailables) from the `toMail` method: -->
메일러블 객체에서 파일을 첨부할 때와 달리, 알림에서는 `attachFromStorage`를 직접 사용할 수 없습니다. 대신, 파일의 절대 경로를 `attach` 메서드에 전달해야 합니다. 또는, `toMail` 메서드에서 [mailable](/docs/8.x/mail#generating-mailables)을 반환하는 방식도 사용할 수 있습니다.

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

<a name="raw-data-attachments"></a>

<!-- #### Raw Data Attachments -->
#### Raw Data Attachments

<!-- The `attachData` method may be used to attach a raw string of bytes as an attachment. When calling the `attachData` method, you should provide the filename that should be assigned to the attachment: -->
`attachData` 메서드는 바이트로 이루어진 원시 문자열 데이터를 첨부파일로 첨부할 때 사용할 수 있습니다. `attachData` 메서드를 호출할 때는 첨부파일에 지정할 파일명을 함께 전달해야 합니다.

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

<a name="using-mailables"></a>
<!-- ### Using Mailables -->
### Using Mailables

<!-- If needed, you may return a full [mailable object](/docs/8.x/mail) from your notification's `toMail` method. When returning a `Mailable` instead of a `MailMessage`, you will need to specify the message recipient using the mailable object's `to` method: -->
필요하다면, 알림의 `toMail` 메서드에서 [mailable object](/docs/8.x/mail) 전체를 반환할 수 있습니다. `MailMessage` 대신 `Mailable` 객체를 반환하는 경우, 수신자는 mailable 객체의 `to` 메서드로 명시해주어야 합니다.

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
[on-demand notification](#on-demand-notifications)을 보낼 때 알림의 `toMail` 메서드로 전달되는 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스로, `routeNotificationFor` 메서드를 제공해 온디맨드 알림이 발송되어야 할 이메일 주소를 가져올 수 있습니다.

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
메일 알림 템플릿을 디자인할 때, 일반 Blade 템플릿을 렌더링하는 것처럼 브라우저에서 미리보기 기능을 활용하면 편리합니다. 이를 위해, Laravel에서는 메일 알림에서 생성된 mail 메시지를 바로 라우트 클로저나 컨트롤러에서 반환할 수 있습니다. `MailMessage`가 반환되면, 실제 이메일로 발송하지 않고도 브라우저에서 바로 렌더링된 형태로 디자인 결과를 미리 볼 수 있습니다.

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
마크다운(Markdown) 메일 알림은 사전에 준비된 템플릿을 활용하면서도 자유롭게 길고 맞춤화된 메시지를 작성할 수 있는 기능입니다. 메시지가 마크다운으로 작성되므로, Laravel은 메시지를 미려하고 반응형인 HTML 템플릿으로 렌더링할 수 있으며, 동시에 자동으로 일반 텍스트 버전도 생성합니다.

<a name="generating-the-message"></a>
<!-- ### Generating The Message -->
### Generating The Message

<!-- To generate a notification with a corresponding Markdown template, you may use the `--markdown` option of the `make:notification` Artisan command: -->
마크다운 템플릿을 사용하는 알림을 생성하려면, Artisan의 `make:notification` 명령어에 `--markdown` 옵션을 사용할 수 있습니다.

```
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

<!-- Like all other mail notifications, notifications that use Markdown templates should define a `toMail` method on their notification class. However, instead of using the `line` and `action` methods to construct the notification, use the `markdown` method to specify the name of the Markdown template that should be used. An array of data you wish to make available to the template may be passed as the method's second argument: -->
다른 메일 알림과 마찬가지로, 마크다운 템플릿을 사용하는 알림 클래스에도 `toMail` 메서드를 정의해야 합니다. 하지만, 알림 메시지를 구성할 때 `line`과 `action` 메서드 대신, 사용할 마크다운 템플릿의 이름을 `markdown` 메서드로 지정합니다. 템플릿에서 사용할 데이터를 배열 형태로 두 번째 인자로 전달할 수 있습니다.

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
마크다운 메일 알림은 Blade 컴포넌트와 마크다운 구문을 조합하여, Laravel에서 미리 제작한 알림 컴포넌트를 쉽게 활용하며 알림을 구성할 수 있게 해줍니다.

```
@component('mail::message')
# Invoice Paid

Your invoice has been paid!

@component('mail::button', ['url' => $url])
View Invoice
@endcomponent

Thanks,<br>
{{ config('app.name') }}
@endcomponent
```

<a name="button-component"></a>
<!-- #### Button Component -->
#### Button Component

<!-- The button component renders a centered button link. The component accepts two arguments, a `url` and an optional `color`. Supported colors are `primary`, `green`, and `red`. You may add as many button components to a notification as you wish: -->
버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 `url`과 선택적으로 `color` 두 가지 인자를 받을 수 있습니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 한 알림에 필요한 만큼 버튼 컴포넌트를 추가할 수 있습니다.

```
@component('mail::button', ['url' => $url, 'color' => 'green'])
View Invoice
@endcomponent
```

<a name="panel-component"></a>
<!-- #### Panel Component -->
#### Panel Component

<!-- The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the notification. This allows you to draw attention to a given block of text: -->
패널 컴포넌트는 지정한 텍스트 블록을 알림 본문과는 구분된 약간 다른 배경색의 패널로 표시합니다. 강조하고 싶은 특정 텍스트 블록이 있을 때 유용하게 사용할 수 있습니다.

```
@component('mail::panel')
This is the panel content.
@endcomponent
```

<a name="table-component"></a>
<!-- #### Table Component -->
#### Table Component

<!-- The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax: -->
테이블 컴포넌트를 사용하면 마크다운 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트의 내용으로 마크다운 테이블을 넘겨주면 됩니다. 마크다운 기본 테이블 정렬 문법을 활용해 컬럼 정렬도 지원합니다.

```
@component('mail::table')
| Laravel       | Table         | Example  |
| ------------- |:-------------:| --------:|
| Col 2 is      | Centered      | $10      |
| Col 3 is      | Right-Aligned | $20      |
@endcomponent
```

<a name="customizing-the-components"></a>
<!-- ### Customizing The Components -->
### Customizing The Components

<!-- You may export all of the Markdown notification components to your own application for customization. To export the components, use the `vendor:publish` Artisan command to publish the `laravel-mail` asset tag: -->
알림에서 사용하는 마크다운 컴포넌트들은 모두 직접 앱 내에서 복사해 자유롭게 커스터마이즈할 수 있습니다. 컴포넌트를 내 앱에 내보내려면 `laravel-mail` 에셋 태그를 활용해 `vendor:publish` Artisan 명령어를 실행하세요.

```
php artisan vendor:publish --tag=laravel-mail
```

<!-- This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like. -->
이 명령은 마크다운 메일 컴포넌트들을 `resources/views/vendor/mail` 디렉토리에 복사합니다. `mail` 디렉토리 안에는 각 컴포넌트의 HTML, 텍스트 버전이 각각 `html`, `text` 디렉토리에 들어있습니다. 이 컴포넌트들은 원하는 대로 자유롭게 커스터마이즈 가능합니다.

<a name="customizing-the-css"></a>
<!-- #### Customizing The CSS -->
#### Customizing The CSS

<!-- After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be in-lined within the HTML representations of your Markdown notifications. -->
컴포넌트를 내보낸 뒤에는 `resources/views/vendor/mail/html/themes` 디렉토리에 `default.css` 파일이 생성됩니다. 이 파일의 CSS를 수정하면, 스타일이 자동으로 각 마크다운 알림의 HTML 본문에 인라인 방식으로 반영됩니다.

<!-- If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of the `mail` configuration file to match the name of your new theme. -->
만약 Laravel 마크다운 컴포넌트에 대해 완전히 새로운 테마를 생성하고 싶다면, `html/themes` 디렉토리에 CSS 파일을 추가하면 됩니다. 파일명을 지정해 저장한 뒤, `mail` 설정 파일의 `theme` 옵션에서 해당 테마명을 지정하세요.

<!-- To customize the theme for an individual notification, you may call the `theme` method while building the notification's mail message. The `theme` method accepts the name of the theme that should be used when sending the notification: -->
특정 알림 한 건에 대해서만 별도의 테마를 적용하고 싶다면, 알림의 메일 메시지를 빌드하는 과정에서 `theme` 메서드를 활용하면 됩니다. `theme` 메서드는 알림 발송 시 사용할 테마의 이름을 인자로 받습니다.

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
`database` 알림 채널은 알림 정보를 데이터베이스 테이블에 저장합니다. 이 테이블에는 알림 타입과 알림에 대한 정보를 설명하는 JSON 데이터 구조 등이 기록됩니다.

<!-- You can query the table to display the notifications in your application's user interface. But, before you can do that, you will need to create a database table to hold your notifications. You may use the `notifications:table` command to generate a [migration](/docs/8.x/migrations) with the proper table schema: -->
저장된 알림을 애플리케이션 UI에서 조회해 표시할 수 있습니다. 그러나 이를 위해 먼저 알림 정보를 저장할 전용 데이터베이스 테이블이 필요합니다. `notifications:table` 명령어를 사용해 적절한 테이블 스키마를 가진 [migration](/docs/8.x/migrations)을 생성할 수 있습니다.

```
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
<!-- ### Formatting Database Notifications -->
### Formatting Database Notifications

<!-- If a notification supports being stored in a database table, you should define a `toDatabase` or `toArray` method on the notification class. This method will receive a `$notifiable` entity and should return a plain PHP array. The returned array will be encoded as JSON and stored in the `data` column of your `notifications` table. Let's take a look at an example `toArray` method: -->
알림을 데이터베이스 테이블에 저장하려면 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 전달받고, 일반 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `notifications` 테이블의 `data` 컬럼에 저장됩니다. 아래는 예시 `toArray` 메서드입니다.

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
`toArray` 메서드는 `broadcast` 채널이 프론트엔드로 브로드캐스트할 데이터를 결정할 때도 사용됩니다. 만약 `database` 채널과 `broadcast` 채널에서 각각 다르게 배열 구조를 만들고 싶다면, `toArray` 대신 `toDatabase` 메서드를 정의하면 됩니다.

<a name="accessing-the-notifications"></a>
<!-- ### Accessing The Notifications -->
### Accessing The Notifications

<!-- Once notifications are stored in the database, you need a convenient way to access them from your notifiable entities. The `Illuminate\Notifications\Notifiable` trait, which is included on Laravel's default `App\Models\User` model, includes a `notifications` [Eloquent relationship](/docs/8.x/eloquent-relationships) that returns the notifications for the entity. To fetch notifications, you may access this method like any other Eloquent relationship. By default, notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
알림이 데이터베이스에 저장되면, 수신 가능한 엔터티(예: User)로부터 알림을 쉽게 불러와 사용하는 것이 중요합니다. Laravel 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에는 해당 엔터티의 알림들을 반환하는 `notifications` [Eloquent relationship](/docs/8.x/eloquent-relationships)가 있습니다. 이 메서드는 일반 Eloquent 연관관계와 마찬가지로 접근할 수 있으며, 기본적으로 `created_at` 타임스탬프 내림차순(최신순)으로 알림이 정렬됩니다.

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

<!-- If you want to retrieve only the "unread" notifications, you may use the `unreadNotifications` relationship. Again, these notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
"읽지 않은" 알림만 가져오고 싶다면, `unreadNotifications` 연관관계를 사용하면 됩니다. 역시 이 알림들도 `created_at` 타임스탬프 기준 최신순으로 정렬됩니다.

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!TIP]
> 자바스크립트 클라이언트에서 알림에 접근하려면, 현재 사용자와 같은 특정 notifiable 엔터티에 대한 알림을 반환하는 알림 컨트롤러를 만들고, 해당 컨트롤러 URL로 HTTP 요청을 보내면 됩니다.

<a name="marking-notifications-as-read"></a>
<!-- ### Marking Notifications As Read -->
### Marking Notifications As Read

<!-- Typically, you will want to mark a notification as "read" when a user views it. The `Illuminate\Notifications\Notifiable` trait provides a `markAsRead` method, which updates the `read_at` column on the notification's database record: -->
일반적으로 사용자가 알림을 조회하면 '읽음' 상태로 표시하고 싶을 것입니다. `Illuminate\Notifications\Notifiable` 트레이트는 `markAsRead` 메서드를 제공하여 데이터베이스의 알림 레코드의 `read_at` 컬럼을 업데이트합니다.

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

<!-- However, instead of looping through each notification, you may use the `markAsRead` method directly on a collection of notifications: -->
각 알림을 반복 처리하는 대신, 전체 알림 컬렉션에 대해 바로 `markAsRead`를 호출할 수도 있습니다.

```
$user->unreadNotifications->markAsRead();
```

<!-- You may also use a mass-update query to mark all of the notifications as read without retrieving them from the database: -->
모든 알림을 한 번에 읽음 처리하려면, 직접 데이터베이스에 대해 대량 업데이트 쿼리를 실행할 수도 있습니다.

```
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

<!-- You may `delete` the notifications to remove them from the table entirely: -->
알림을 테이블에서 완전히 삭제하고 싶다면 `delete` 메서드를 호출하면 됩니다.

```
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
<!-- ## Broadcast Notifications -->
## Broadcast Notifications

<a name="broadcast-prerequisites"></a>
<!-- ### Prerequisites -->
### Prerequisites

<!-- Before broadcasting notifications, you should configure and be familiar with Laravel's [event broadcasting](/docs/8.x/broadcasting) services. Event broadcasting provides a way to react to server-side Laravel events from your JavaScript powered frontend. -->
알림을 브로드캐스트하기 전에, Laravel의 [event broadcasting](/docs/8.x/broadcasting) 서비스에 대해 설정 및 기본 개념 숙지가 필요합니다. 이벤트 브로드캐스팅은 Laravel의 서버사이드 이벤트에 자바스크립트 프론트엔드가 반응하도록 만드는 기능입니다.

<a name="formatting-broadcast-notifications"></a>
<!-- ### Formatting Broadcast Notifications -->
### Formatting Broadcast Notifications

<!-- The `broadcast` channel broadcasts notifications using Laravel's [event broadcasting](/docs/8.x/broadcasting) services, allowing your JavaScript powered frontend to catch notifications in realtime. If a notification supports broadcasting, you can define a `toBroadcast` method on the notification class. This method will receive a `$notifiable` entity and should return a `BroadcastMessage` instance. If the `toBroadcast` method does not exist, the `toArray` method will be used to gather the data that should be broadcast. The returned data will be encoded as JSON and broadcast to your JavaScript powered frontend. Let's take a look at an example `toBroadcast` method: -->
`broadcast` 채널은 Laravel의 [event broadcasting](/docs/8.x/broadcasting) 서비스를 활용하여 알림을 브로드캐스팅하며, 이를 통해 자바스크립트 프론트엔드에서 실시간으로 알림을 받을 수 있습니다. 브로드캐스트 가능한 알림이라면 알림 클래스에 `toBroadcast` 메서드를 정의할 수 있습니다. 이 메서드는 `$notifiable` 엔터티를 받아, `BroadcastMessage` 인스턴스를 반환해야 합니다. `toBroadcast` 메서드가 없다면 `toArray` 메서드 데이터를 사용해서 브로드캐스트됩니다. 반환된 데이터는 JSON으로 인코딩되어 자바스크립트 프론트엔드에 전달됩니다. 아래는 예제 `toBroadcast` 메서드입니다.

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
모든 브로드캐스트 알림은 큐잉되어 처리됩니다. 브로드캐스트 작업이 사용할 큐 커넥션이나 큐 이름을 설정하려면, `BroadcastMessage`의 `onConnection`, `onQueue` 메서드를 사용할 수 있습니다.

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
<!-- #### Customizing The Notification Type -->
#### Customizing The Notification Type

<!-- In addition to the data you specify, all broadcast notifications also have a `type` field containing the full class name of the notification. If you would like to customize the notification `type`, you may define a `broadcastType` method on the notification class: -->
직접 지정한 데이터 외에도, 모든 브로드캐스트 알림에는 알림의 전체 클래스명을 담은 `type` 필드가 포함됩니다. 이 `type` 값을 직접 정의하고 싶을 경우, 알림 클래스에 `broadcastType` 메서드를 작성하면 됩니다.

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

<!-- Notifications will broadcast on a private channel formatted using a `{notifiable}.{id}` convention. So, if you are sending a notification to an `App\Models\User` instance with an ID of `1`, the notification will be broadcast on the `App.Models.User.1` private channel. When using [Laravel Echo](/docs/8.x/broadcasting#client-side-installation), you may easily listen for notifications on a channel using the `notification` method: -->
알림은 `{notifiable}.{id}` 형태로 구성된 프라이빗 채널을 통해 브로드캐스트됩니다. 예를 들어, ID가 `1`인 `App\Models\User` 인스턴스에게 알림을 전송하면, `App.Models.User.1` 프라이빗 채널로 브로드캐스트됩니다. [Laravel Echo](/docs/8.x/broadcasting#client-side-installation)를 사용할 경우, `notification` 메서드를 사용하여 해당 채널에서 쉽게 알림 이벤트를 청취할 수 있습니다.

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
특정 엔터티의 브로드캐스트 알림이 브로드캐스트되는 채널을 커스터마이즈하고 싶으면, notifiable 엔터티에 `receivesBroadcastNotificationsOn` 메서드를 정의하면 됩니다.

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

<!-- Sending SMS notifications in Laravel is powered by [Vonage](https://www.vonage.com/) (formerly known as Nexmo). Before you can send notifications via Vonage, you need to install the `laravel/nexmo-notification-channel` and `nexmo/laravel` Composer packages -->
Laravel에서 SMS 알림은 [Vonage](https://www.vonage.com/) (이전 Nexmo)로 제공됩니다. Vonage를 통해 알림을 보내려면, `laravel/nexmo-notification-channel` 및 `nexmo/laravel` Composer 패키지를 설치해야 합니다.

```
composer require laravel/nexmo-notification-channel nexmo/laravel
```

<!-- The `nexmo/laravel` package includes [its own configuration file](https://github.com/Nexmo/nexmo-laravel/blob/master/config/nexmo.php). However, you are not required to export this configuration file to your own application. You can simply use the `NEXMO_KEY` and `NEXMO_SECRET` environment variables to set your Vonage public and secret key. -->
`nexmo/laravel` 패키지는 [its own configuration file](https://github.com/Nexmo/nexmo-laravel/blob/master/config/nexmo.php)을 포함하고 있지만, 꼭 설정 파일을 내 앱에 복사해서 사용할 필요는 없습니다. 그냥 `NEXMO_KEY`와 `NEXMO_SECRET` 환경 변수로 Vonage의 공개키와 비밀키를 지정하시면 됩니다.

<!-- Next, you will need to add a `nexmo` configuration entry to your `config/services.php` configuration file. You may copy the example configuration below to get started: -->
그리고 `config/services.php` 설정 파일에 `nexmo` 항목을 추가해야 합니다. 아래 예시 설정을 참고하세요.

```
'nexmo' => [
    'sms_from' => '15556666666',
],
```

<!-- The `sms_from` option is the phone number that your SMS messages will be sent from. You should generate a phone number for your application in the Vonage control panel. -->
`sms_from` 옵션은 SMS를 발신할 전화번호입니다. Vonage 관리 패널에서 애플리케이션에 사용할 발신 번호를 생성할 수 있습니다.

<a name="formatting-sms-notifications"></a>
<!-- ### Formatting SMS Notifications -->
### Formatting SMS Notifications

<!-- If a notification supports being sent as an SMS, you should define a `toNexmo` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\NexmoMessage` instance: -->
알림을 SMS로 보낼 수 있다면, 알림 클래스에 `toNexmo` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 전달받고, `Illuminate\Notifications\Messages\NexmoMessage` 인스턴스를 반환해야 합니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content');
}
```

<a name="unicode-content"></a>
<!-- #### Unicode Content -->
#### Unicode Content

<!-- If your SMS message will contain unicode characters, you should call the `unicode` method when constructing the `NexmoMessage` instance: -->
SMS 메시지에 유니코드 문자가 포함될 경우, `NexmoMessage` 인스턴스를 만들 때 `unicode` 메서드를 함께 호출해야 합니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return \Illuminate\Notifications\Messages\NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your unicode message')
                ->unicode();
}
```

<a name="formatting-shortcode-notifications"></a>
<!-- ### Formatting Shortcode Notifications -->
### Formatting Shortcode Notifications

<!-- Laravel also supports sending shortcode notifications, which are pre-defined message templates in your Vonage account. To send a shortcode SMS notification, you should define a `toShortcode` method on your notification class. From within this method, you may return an array specifying the type of notification (`alert`, `2fa`, or `marketing`) as well as the custom values that will populate the template: -->
Laravel은 Vonage 계정에 미리 등록해둔 메시지 템플릿(쇼트코드) 알림 전송도 지원합니다. 쇼트코드 SMS 알림을 보내려면, 알림 클래스 내에 `toShortcode` 메서드를 정의하세요. 이 메서드에서는 알림 타입(`alert`, `2fa`, `marketing`)과 템플릿 내에 전달할 커스텀 값들을 배열로 반환합니다.

```
/**
 * Get the Vonage / Shortcode representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return array
 */
public function toShortcode($notifiable)
{
    return [
        'type' => 'alert',
        'custom' => [
            'code' => 'ABC123',
        ],
    ];
}
```

> [!TIP]
> [routing SMS Notifications](#routing-sms-notifications)처럼, notifiable 모델에는 `routeNotificationForShortcode` 메서드를 구현해주셔야 합니다.

<a name="customizing-the-from-number"></a>
<!-- ### Customizing The "From" Number -->
### Customizing The "From" Number

<!-- If you would like to send some notifications from a phone number that is different from the phone number specified in your `config/services.php` file, you may call the `from` method on a `NexmoMessage` instance: -->
`config/services.php` 파일에 설정한 발신 번호와 다른 번호로 알림을 보내고 싶다면, `NexmoMessage` 인스턴스에 `from` 메서드로 발신 번호를 지정하면 됩니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->content('Your SMS message content')
                ->from('15554443333');
}
```

<a name="adding-a-client-reference"></a>
<!-- ### Adding a Client Reference -->
### Adding a Client Reference

<!-- If you would like to keep track of costs per user, team, or client, you may add a "client reference" to the notification. Vonage will allow you to generate reports using this client reference so that you can better understand a particular customer's SMS usage. The client reference can be any string up to 40 characters: -->
사용자, 팀, 특정 고객 단위로 SMS 비용을 추적하고 싶다면, 알림에 "클라이언트 참조(client reference)"를 추가할 수 있습니다. Vonage에서는 이 값을 기준으로 각 고객의 SMS 활용 내역 리포트를 생성할 수 있습니다. 클라이언트 참조는 최대 40자 길이의 임의 문자열이면 됩니다.

```
/**
 * Get the Vonage / SMS representation of the notification.
 *
 * @param  mixed  $notifiable
 * @return NexmoMessage
 */
public function toNexmo($notifiable)
{
    return (new NexmoMessage)
                ->clientReference((string) $notifiable->id)
                ->content('Your SMS message content');
}
```

<a name="routing-sms-notifications"></a>
<!-- ### Routing SMS Notifications -->
### Routing SMS Notifications

<!-- To route Vonage notifications to the proper phone number, define a `routeNotificationForNexmo` method on your notifiable entity: -->
Vonage 알림이 올바른 전화번호로 전송되도록 하려면, notifiable 엔터티(예: User)에서 `routeNotificationForNexmo` 메서드를 정의하세요.

```
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Nexmo channel.
     *
     * @param  \Illuminate\Notifications\Notification  $notification
     * @return string
     */
    public function routeNotificationForNexmo($notification)
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
슬랙을 통해 알림을 전송하려면, 먼저 Composer를 사용하여 Slack 알림 채널 패키지를 설치해야 합니다.

```
composer require laravel/slack-notification-channel
```

<!-- You will also need to create a [Slack App](https://api.slack.com/apps?new_app=1) for your team. After creating the App, you should configure an "Incoming Webhook" for the workspace. Slack will then provide you with a webhook URL that you may use when [routing Slack notifications](#routing-slack-notifications). -->
또한, 팀을 위해 [Slack App](https://api.slack.com/apps?new_app=1)을 하나 생성해야 합니다. 앱을 만든 후, 워크스페이스에 대해 "Incoming Webhook"을 설정해야 합니다. 그러면 Slack에서 제공하는 웹훅 URL을 받을 수 있으며, 이 URL을 사용하여 [routing Slack notifications](#routing-slack-notifications)을 진행할 수 있습니다.

<a name="formatting-slack-notifications"></a>
<!-- ### Formatting Slack Notifications -->
### Formatting Slack Notifications

<!-- If a notification supports being sent as a Slack message, you should define a `toSlack` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\SlackMessage` instance. Slack messages may contain text content as well as an "attachment" that formats additional text or an array of fields. Let's take a look at a basic `toSlack` example: -->
알림이 슬랙 메시지로 전송될 수 있도록 하려면, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 인자로 받아야 하며, `Illuminate\Notifications\Messages\SlackMessage` 인스턴스를 반환해야 합니다. 슬랙 메시지는 일반 텍스트 뿐만 아니라 추가 정보를 포함하는 "attachment(첨부)"도 가질 수 있습니다. 기본적인 `toSlack` 예제를 살펴보겠습니다.

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
슬랙 메시지에는 "attachment(첨부)"도 추가할 수 있습니다. 첨부는 단순 텍스트 메시지보다 더 다양한 포맷팅 옵션을 제공합니다. 아래 예제에서는 애플리케이션에서 예외가 발생했을 때 해당 예외에 대한 상세 정보를 볼 수 있는 링크와 함께 에러 알림을 전송합니다.

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
첨부를 사용하면 사용자에게 보여줄 다양한 데이터를 배열 형태로 지정할 수도 있습니다. 지정한 데이터는 표 형식으로 쉽게 읽을 수 있게 표시됩니다.

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
첨부의 일부 필드가 마크다운(Markdown) 포맷을 포함하고 있다면, `markdown` 메서드를 사용하여 Slack이 해당 필드를 마크다운으로 파싱하고 표시하도록 할 수 있습니다. 이 메서드에는 `pretext`, `text`, `fields` 값 중 하나 또는 여러 개를 배열로 전달할 수 있습니다. Slack 첨부 포맷에 대한 자세한 내용은 [Slack API documentation](https://api.slack.com/docs/message-formatting#message_formatting)를 참고하시기 바랍니다.

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
슬랙 알림을 특정 팀과 채널로 전달하려면, 알림을 받을 엔티티에 `routeNotificationForSlack` 메서드를 정의해야 합니다. 이 메서드는 알림이 전송될 웹훅 URL을 반환해야 합니다. 웹훅 URL은 Slack 팀에 "Incoming Webhook" 서비스를 추가해서 생성할 수 있습니다.

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
Laravel에서는 알림을 전송할 때 HTTP 요청의 현재 로케일(locale)이 아닌 다른 언어로 알림을 보낼 수 있으며, 알림이 큐에 저장됐다가 나중에 전송된다 해도 지정한 로케일을 기억합니다.

<!-- To accomplish this, the `Illuminate\Notifications\Notification` class offers a `locale` method to set the desired language. The application will change into this locale when the notification is being evaluated and then revert back to the previous locale when evaluation is complete: -->
이를 위해 `Illuminate\Notifications\Notification` 클래스는 원하는 언어를 지정하는 `locale` 메서드를 제공합니다. 알림을 평가할 때 애플리케이션의 사용 언어가 지정된 로케일로 변경되었다가, 평가가 끝나면 이전 언어로 다시 복원됩니다.

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

<!-- Localization of multiple notifiable entries may also be achieved via the `Notification` facade: -->
여러 명의 알림 수신자를 대상으로 할 경우에는 `Notification` 파사드를 이용해 로케일을 지정할 수도 있습니다.

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
<!-- ### User Preferred Locales -->
### User Preferred Locales

<!-- Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on your notifiable model, you may instruct Laravel to use this stored locale when sending a notification: -->
경우에 따라, 각 사용자의 선호 언어(로케일)를 데이터베이스에 저장하는 경우도 있습니다. 이럴 때에는 알림을 받을 모델에 `HasLocalePreference` 계약(Contract)을 구현하면, Laravel이 알림 전송 시 해당 사용자의 언어 설정을 자동으로 사용합니다.

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
이 인터페이스를 구현하고 나면, Laravel이 자동으로 알림 및 메일 전송 시 각 모델의 선호 언어를 사용합니다. 즉, 별도로 `locale` 메서드를 호출하지 않아도 됩니다.

```
$user->notify(new InvoicePaid($invoice));
```

<a name="notification-events"></a>
<!-- ## Notification Events -->
## Notification Events

<a name="notification-sending-event"></a>
<!-- #### Notification Sending Event -->
#### Notification Sending Event

<!-- When a notification is sending, the `Illuminate\Notifications\Events\NotificationSending` [event](/docs/8.x/events) is dispatched by the notification system. This contains the "notifiable" entity and the notification instance itself. You may register listeners for this event in your application's `EventServiceProvider`: -->
알림이 전송될 때, Laravel 알림 시스템은 `Illuminate\Notifications\Events\NotificationSending` [event](/docs/8.x/events)를 발생시킵니다. 이 이벤트에는 "알림 받을 엔티티"와 "알림 인스턴스" 자체가 포함되어 있습니다. 이 이벤트에 대한 리스너를 애플리케이션의 `EventServiceProvider`에 등록할 수 있습니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSending' => [
        'App\Listeners\CheckNotificationStatus',
    ],
];
```

<!-- The notification will not be sent if an event listener for the `NotificationSending` event returns `false` from its `handle` method: -->
`NotificationSending` 이벤트의 리스너에서 `handle` 메서드가 `false`를 반환하면, 알림이 실제로 전송되지 않습니다.

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
이벤트 리스너 내부에서 `notifiable`, `notification`, `channel` 속성에 접근하여, 알림의 수신자 또는 알림의 세부 정보 등을 확인할 수 있습니다.

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

<!-- When a notification is sent, the `Illuminate\Notifications\Events\NotificationSent` [event](/docs/8.x/events) is dispatched by the notification system. This contains the "notifiable" entity and the notification instance itself. You may register listeners for this event in your `EventServiceProvider`: -->
알림이 실제로 전송이 완료되면, 알림 시스템은 `Illuminate\Notifications\Events\NotificationSent` [event](/docs/8.x/events)를 발생시킵니다. 이 이벤트 역시 "알림 받을 엔티티"와 "알림 인스턴스" 자체를 포함합니다. 해당 이벤트에 대한 리스너를 `EventServiceProvider`에 등록할 수 있습니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Notifications\Events\NotificationSent' => [
        'App\Listeners\LogNotification',
    ],
];
```

> [!TIP]
> `EventServiceProvider`에 리스너를 등록한 후에는, `event:generate` 아티즌 명령어를 사용해서 리스너 클래스를 빠르게 생성할 수 있습니다.

<!-- Within an event listener, you may access the `notifiable`, `notification`, `channel`, and `response` properties on the event to learn more about the notification recipient or the notification itself: -->
리스너 내부에서는 `notifiable`, `notification`, `channel`, `response` 속성에 접근하여 알림 수신자, 알림 자체, 실제 응답 등에 대한 정보를 얻을 수 있습니다.

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
Laravel은 여러 가지 기본 알림 채널을 제공하지만, 필요에 따라 직접 드라이버를 만들어 다른 방식으로 알림을 전달할 수도 있습니다. Laravel은 이를 아주 쉽게 지원합니다. 먼저 `send` 메서드를 가진 클래스를 정의하세요. 이 메서드는 `$notifiable`과 `$notification` 두 개의 인자를 받습니다.

<!-- Within the `send` method, you may call methods on the notification to retrieve a message object understood by your channel and then send the notification to the `$notifiable` instance however you wish: -->
`send` 메서드 내에서 알림의 메서드를 호출하여 채널에서 이해할 수 있는 메시지 객체를 만들고, 원하는 방식으로 `$notifiable` 인스턴스에 알림을 보내면 됩니다.

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
알림 채널 클래스를 정의한 후에는, 각 알림의 `via` 메서드에서 해당 클래스명을 반환할 수 있습니다. 아래 예시에서 보듯, 알림의 `toVoice` 메서드는 여러분이 정의한 음성 메시지를 나타내는 어떤 객체든 반환할 수 있습니다. 예를 들어, 여러분만의 `VoiceMessage` 클래스를 만들어 이 메시지를 구현할 수 있습니다.

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
