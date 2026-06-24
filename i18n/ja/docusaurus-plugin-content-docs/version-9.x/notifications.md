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
[sending email](/docs/9.x/mail) のサポートに加えて、Laravel は、電子メール、SMS (旧 Nexmo である [Vonage](https://www.vonage.com/communications-apis/) 経由)、[Slack](https://slack.com) など、さまざまな配信チャネルで通知を送信するためのサポートを提供します。さらに、数十の異なるチャネルで通知を送信するために、さまざまな [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel) が作成されています。通知はデータベースに保存され、Web インターフェイスに表示される場合もあります。

<!-- Typically, notifications should be short, informational messages that notify users of something that occurred in your application. For example, if you are writing a billing application, you might send an "Invoice Paid" notification to your users via the email and SMS channels. -->
通常、通知は、アプリケーションで発生した何かをユーザーに通知する短い情報メッセージである必要があります。たとえば、請求アプリケーションを作成している場合、電子メールと SMS チャネルを介してユーザーに「請求書支払い済み」通知を送信できます。

<a name="generating-notifications"></a>
<!-- ## Generating Notifications -->
## Generating Notifications

<!-- In Laravel, each notification is represented by a single class that is typically stored in the `app/Notifications` directory. Don't worry if you don't see this directory in your application - it will be created for you when you run the `make:notification` Artisan command: -->
Laravel では、各通知は単一のクラスで表され、通常は `app/Notifications` ディレクトリに保存されます。アプリケーションにこのディレクトリが表示されなくても心配する必要はありません。`make:notification` Artisan コマンドを実行すると作成されます。

```shell
php artisan make:notification InvoicePaid
```

<!-- This command will place a fresh notification class in your `app/Notifications` directory. Each notification class contains a `via` method and a variable number of message building methods, such as `toMail` or `toDatabase`, that convert the notification to a message tailored for that particular channel. -->
このコマンドは、新しい通知クラスを `app/Notifications` ディレクトリに配置します。各通知クラスには、`via` メソッドと、通知をその特定のチャネルに合わせたメッセージに変換する `toMail` や `toDatabase` などの可変数のメッセージ構築メソッドが含まれています。

<a name="sending-notifications"></a>
<!-- ## Sending Notifications -->
## Sending Notifications

<a name="using-the-notifiable-trait"></a>
<!-- ### Using The Notifiable Trait -->
### Using The Notifiable Trait

<!-- Notifications may be sent in two ways: using the `notify` method of the `Notifiable` trait or using the `Notification` [facade](/docs/9.x/facades). The `Notifiable` trait is included on your application's `App\Models\User` model by default: -->
通知は 2 つの方法で送信できます。`Notifiable` 特性の `notify` メソッドを使用する方法と、`Notification` [facade](/docs/9.x/facades) を使用する方法です。 `Notifiable` 特性は、デフォルトでアプリケーションの `App\Models\User` モデルに含まれています。

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
この特性によって提供される `notify` メソッドは、通知インスタンスを受信することを想定しています。

```
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> どのモデルでも `Notifiable` トレイトを使用できることに注意してください。 `User` モデルに含めるだけに限定されるわけではありません。

<a name="using-the-notification-facade"></a>
<!-- ### Using The Notification Facade -->
### Using The Notification Facade

<!-- Alternatively, you may send notifications via the `Notification` [facade](/docs/9.x/facades). This approach is useful when you need to send a notification to multiple notifiable entities such as a collection of users. To send notifications using the facade, pass all of the notifiable entities and the notification instance to the `send` method: -->
あるいは、`Notification` [facade](/docs/9.x/facades) 経由で通知を送信することもできます。このアプローチは、ユーザーのコレクションなど、複数の通知対象エンティティに通知を送信する必要がある場合に便利です。ファサードを使用して通知を送信するには、すべての通知可能なエンティティと通知インスタンスを `send` メソッドに渡します。

```
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

<!-- You can also send notifications immediately using the `sendNow` method. This method will send the notification immediately even if the notification implements the `ShouldQueue` interface: -->
`sendNow` メソッドを使用して、すぐに通知を送信することもできます。このメソッドは、通知が `ShouldQueue` インターフェイスを実装している場合でも、通知をすぐに送信します。

```
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
<!-- ### Specifying Delivery Channels -->
### Specifying Delivery Channels

<!-- Every notification class has a `via` method that determines on which channels the notification will be delivered. Notifications may be sent on the `mail`, `database`, `broadcast`, `vonage`, and `slack` channels. -->
すべての通知クラスには、通知が配信されるチャネルを決定する `via` メソッドがあります。通知は、`mail`、`database`、`broadcast`、`vonage`、および `slack` チャネルで送信される場合があります。

> [!NOTE]
> Telegram や Pusher などの他の配信チャネルを使用したい場合は、コミュニティ主導の [Laravel Notification Channels website](http://laravel-notification-channels.com) をチェックしてください。

<!-- The `via` method receives a `$notifiable` instance, which will be an instance of the class to which the notification is being sent. You may use `$notifiable` to determine which channels the notification should be delivered on: -->
`via` メソッドは、通知の送信先となるクラスのインスタンスとなる `$notifiable` インスタンスを受け取ります。 `$notifiable` を使用して、通知を配信するチャネルを決定できます。

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
> 通知をキューに入れる前に、キューと [start a worker](/docs/9.x/queues) を設定する必要があります。

<!-- Sending notifications can take time, especially if the channel needs to make an external API call to deliver the notification. To speed up your application's response time, let your notification be queued by adding the `ShouldQueue` interface and `Queueable` trait to your class. The interface and trait are already imported for all notifications generated using the `make:notification` command, so you may immediately add them to your notification class: -->
特にチャネルが通知を配信するために外部 API 呼び出しを行う必要がある場合、通知の送信には時間がかかることがあります。アプリケーションの応答時間を短縮するには、`ShouldQueue` インターフェイスと `Queueable` トレイトをクラスに追加して、通知をキューに入れます。インターフェイスと特性は、`make:notification` コマンドを使用して生成されたすべての通知に対してすでにインポートされているため、通知クラスにすぐに追加できます。

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
`ShouldQueue` インターフェイスが通知に追加されたら、通常どおり通知を送信できます。 Laravel はクラス上の `ShouldQueue` インターフェイスを検出し、通知の配信を自動的にキューに入れます。

```
$user->notify(new InvoicePaid($invoice));
```

<!-- When queueing notifications, a queued job will be created for each recipient and channel combination. For example, six jobs will be dispatched to the queue if your notification has three recipients and two channels. -->
通知をキューに入れると、受信者とチャネルの組み合わせごとにキューに入れられたジョブが作成されます。たとえば、通知に 3 人の受信者と 2 つのチャネルがある場合、6 つのジョブがキューにディスパッチされます。

<a name="delaying-notifications"></a>
<!-- #### Delaying Notifications -->
#### Delaying Notifications

<!-- If you would like to delay the delivery of the notification, you may chain the `delay` method onto your notification instantiation: -->
通知の配信を遅らせたい場合は、通知のインスタンス化に `delay` メソッドを連鎖させます。

```
$delay = now()->addMinutes(10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

<a name="delaying-notifications-per-channel"></a>
<!-- #### Delaying Notifications Per Channel -->
#### Delaying Notifications Per Channel

<!-- You may pass an array to the `delay` method to specify the delay amount for specific channels: -->
配列を `delay` メソッドに渡して、特定のチャネルの遅​​延量を指定できます。

```
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->addMinutes(5),
    'sms' => now()->addMinutes(10),
]));
```

<!-- Alternatively, you may define a `withDelay` method on the notification class itself. The `withDelay` method should return an array of channel names and delay values: -->
あるいは、通知クラス自体に `withDelay` メソッドを定義することもできます。 `withDelay` メソッドは、チャネル名と遅延値の配列を返す必要があります。

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
デフォルトでは、キューに入れられた通知は、アプリケーションのデフォルトのキュー接続を使用してキューに入れられます。特定の通知に使用する別の接続を指定したい場合は、通知クラスで `$connection` プロパティを定義できます。

```
/**
 * The name of the queue connection to use when queueing the notification.
 *
 * @var string
 */
public $connection = 'redis';
```

<!-- Or, if you would like to specify a specific queue connection that should be used for each notification channel supported by the notification, you may define a `viaConnections` method on your notification. This method should return an array of channel name / queue connection name pairs: -->
または、通知でサポートされる各通知チャネルに使用する特定のキュー接続を指定したい場合は、通知で `viaConnections` メソッドを定義できます。このメソッドは、チャネル名とキュー接続名のペアの配列を返す必要があります。

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
通知でサポートされる各通知チャネルに使用する特定のキューを指定したい場合は、通知で `viaQueues` メソッドを定義できます。このメソッドは、チャネル名とキュー名のペアの配列を返す必要があります。

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
キューに入れられた通知がデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって通知が処理される場合があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。通知がこれらのモデルに依存している場合、キューに入れられた通知を送信するジョブの処理時に予期しないエラーが発生する可能性があります。

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued notification should be dispatched after all open database transactions have been committed by calling the `afterCommit` method when sending the notification: -->
キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、通知の送信時に `afterCommit` メソッドを呼び出すことにより、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられた通知を送信する必要があることを示すことができます。

```
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

<!-- Alternatively, you may call the `afterCommit` method from your notification's constructor: -->
あるいは、通知のコンストラクターから `afterCommit` メソッドを呼び出すこともできます。

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
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/9.x/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="determining-if-the-queued-notification-should-be-sent"></a>
<!-- #### Determining If A Queued Notification Should Be Sent -->
#### Determining If A Queued Notification Should Be Sent

<!-- After a queued notification has been dispatched for the queue for background processing, it will typically be accepted by a queue worker and sent to its intended recipient. -->
キューに入れられた通知は、バックグラウンド処理のためにキューにディスパッチされた後、通常、キューワーカーによって受け入れられ、目的の受信者に送信されます。

<!-- However, if you would like to make the final determination on whether the queued notification should be sent after it is being processed by a queue worker, you may define a `shouldSend` method on the notification class. If this method returns `false`, the notification will not be sent: -->
ただし、キューに入れられた通知がキューワーカーによって処理された後に送信するかどうかを最終決定したい場合は、通知クラスで `shouldSend` メソッドを定義できます。このメソッドが `false` を返した場合、通知は送信されません。

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
場合によっては、アプリケーションの「ユーザー」として保存されていない人に通知を送信する必要がある場合があります。 `Notification` ファサードの `route` メソッドを使用すると、通知を送信する前にアドホック通知ルーティング情報を指定できます。

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
オンデマンド通知を `mail` ルートに送信するときに受信者の名前を指定したい場合は、電子メール アドレスをキーとして、名前を配列の最初の要素の値として含む配列を指定できます。

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
通知が電子メールとして送信されることをサポートしている場合は、通知クラスで `toMail` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Messages\MailMessage` インスタンスを返す必要があります。

<!-- The `MailMessage` class contains a few simple methods to help you build transactional email messages. Mail messages may contain lines of text as well as a "call to action". Let's take a look at an example `toMail` method: -->
`MailMessage` クラスには、トランザクション電子メール メッセージの作成に役立ついくつかの簡単なメソッドが含まれています。メールメッセージには、テキスト行と「行動喚起」が含まれる場合があります。 `toMail` メソッドの例を見てみましょう。

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
> `toMail` メソッドで `$this->invoice->id` を使用していることに注意してください。通知がメッセージを生成するために必要なデータを通知のコンストラクターに渡すことができます。

<!-- In this example, we register a greeting, a line of text, a call to action, and then another line of text. These methods provided by the `MailMessage` object make it simple and fast to format small transactional emails. The mail channel will then translate the message components into a beautiful, responsive HTML email template with a plain-text counterpart. Here is an example of an email generated by the `mail` channel: -->
この例では、挨拶、テキスト行、行動喚起、そして別のテキスト行を登録します。 `MailMessage` オブジェクトによって提供されるこれらのメソッドにより、小規模なトランザクション電子メールのフォーマットが簡単かつ迅速になります。次に、メール チャネルは、メッセージ コンポーネントを、対応するプレーン テキストを含む美しく応答性の高い HTML 電子メール テンプレートに変換します。 `mail` チャネルによって生成された電子メールの例を次に示します。

<!-- <img src="https://laravel.com/img/docs/notification-example-2.png"/> -->
<img src="https://laravel.com/img/docs/notification-example-2.png"/>

> [!NOTE]
> メール通知を送信するときは、`config/app.php` 構成ファイルで `name` 構成オプションを必ず設定してください。この値は、メール通知メッセージのヘッダーとフッターで使用されます。

<a name="error-messages"></a>
<!-- #### Error Messages -->
#### Error Messages

<!-- Some notifications inform users of errors, such as a failed invoice payment. You may indicate that a mail message is regarding an error by calling the `error` method when building your message. When using the `error` method on a mail message, the call to action button will be red instead of black: -->
一部の通知は、請求書支払いの失敗などのエラーをユーザーに通知します。メッセージの作成時に `error` メソッドを呼び出すことで、メール メッセージがエラーに関するものであることを示すことができます。メール メッセージで `error` メソッドを使用すると、CTA ボタンが黒ではなく赤になります。

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
通知クラスでテキストの「行」を定義する代わりに、`view` メソッドを使用して、通知電子メールのレンダリングに使用するカスタム テンプレートを指定できます。

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
`view` メソッドに与えられる配列の 2 番目の要素としてビュー名を渡すことで、メール メッセージのプレーンテキスト ビューを指定できます。

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
デフォルトでは、電子メールの送信者/差出人のアドレスは、`config/mail.php` 構成ファイルで定義されます。ただし、`from` メソッドを使用して、特定の通知の送信元アドレスを指定できます。

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
`mail` チャネル経由で通知を送信すると、通知システムは通知対象エンティティの `email` プロパティを自動的に検索します。通知可能なエンティティで `routeNotificationForMail` メソッドを定義することにより、通知の配信に使用される電子メール アドレスをカスタマイズできます。

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
デフォルトでは、電子メールの件名は、「Title Case」にフォーマットされた通知のクラス名です。したがって、通知クラスの名前が `InvoicePaid` の場合、電子メールの件名は `Invoice Paid` になります。メッセージに別の件名を指定したい場合は、メッセージの作成時に `subject` メソッドを呼び出すことができます。

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
デフォルトでは、電子メール通知は、`config/mail.php` 構成ファイルで定義されたデフォルトのメーラーを使用して送信されます。ただし、メッセージの作成時に `mailer` メソッドを呼び出すことで、実行時に別のメーラーを指定できます。

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
通知パッケージのリソースを公開することで、メール通知で使用される HTML およびプレーンテキストのテンプレートを変更できます。このコマンドを実行すると、メール通知テンプレートが `resources/views/vendor/notifications` ディレクトリに配置されます。

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
<!-- ### Attachments -->
### Attachments

<!-- To add attachments to an email notification, use the `attach` method while building your message. The `attach` method accepts the absolute path to the file as its first argument: -->
電子メール通知に添付ファイルを追加するには、メッセージの作成時に `attach` メソッドを使用します。 `attach` メソッドは、最初の引数としてファイルへの絶対パスを受け入れます。

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
> 通知メール メッセージによって提供される `attach` メソッドは、[attachable objects](/docs/9.x/mail#attachable-objects) も受け入れます。詳細については、包括的な [attachable object documentation](/docs/9.x/mail#attachable-objects) を参照してください。

<!-- When attaching files to a message, you may also specify the display name and / or MIME type by passing an `array` as the second argument to the `attach` method: -->
メッセージにファイルを添付するときは、`array` を `attach` メソッドの 2 番目の引数として渡すことで、表示名や MIME タイプを指定することもできます。

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
メール可能オブジェクトにファイルを添付する場合とは異なり、`attachFromStorage` を使用してストレージ ディスクからファイルを直接添付することはできません。むしろ、ストレージ ディスク上のファイルへの絶対パスを指定して `attach` メソッドを使用する必要があります。あるいは、`toMail` メソッドから [mailable](/docs/9.x/mail#generating-mailables) を返すこともできます。

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
必要に応じて、`attachMany` メソッドを使用して複数のファイルをメッセージに添付できます。

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
`attachData` メソッドを使用して、生のバイト文字列を添付ファイルとして添付できます。 `attachData` メソッドを呼び出すときは、添付ファイルに割り当てるファイル名を指定する必要があります。

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
Mailgun や Postmark などの一部のサードパーティ電子メール プロバイダは、メッセージの「タグ」と「メタデータ」をサポートしています。これらは、アプリケーションによって送信された電子メールをグループ化し、追跡するために使用される場合があります。 `tag` および `metadata` メソッドを使用して、電子メール メッセージにタグとメタデータを追加できます。

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
アプリケーションが Mailgun ドライバを使用している場合、[tags](https://documentation.mailgun.com/en/latest/user_manual.html#tagging-1) および [metadata](https://documentation.mailgun.com/en/latest/user_manual.html#attaching-data-to-messages) の詳細については、Mailgun のドキュメントを参照してください。同様に、[tags](https://postmarkapp.com/blog/tags-support-for-smtp) および [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) のサポートの詳細については、Postmark のドキュメントを参照することもできます。

<!-- If your application is using Amazon SES to send emails, you should use the `metadata` method to attach [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) to the message. -->
アプリケーションが Amazon SES を使用して E メールを送信している場合は、`metadata` メソッドを使用してメッセージに [SES "tags"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) を添付する必要があります。

<a name="customizing-the-symfony-message"></a>
<!-- ### Customizing The Symfony Message -->
### Customizing The Symfony Message

<!-- The `withSymfonyMessage` method of the `MailMessage` class allows you to register a closure which will be invoked with the Symfony Message instance before sending the message. This gives you an opportunity to deeply customize the message before it is delivered: -->
`MailMessage` クラスの `withSymfonyMessage` メソッドを使用すると、メッセージを送信する前に Symfony Message インスタンスで呼び出されるクロージャを登録できます。これにより、メッセージを配信する前に詳細にカスタマイズする機会が得られます。

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
必要に応じて、通知の `toMail` メソッドから完全な [mailable object](/docs/9.x/mail) を返すことができます。 `MailMessage` の代わりに `Mailable` を返す場合は、メール可能オブジェクトの `to` メソッドを使用してメッセージ受信者を指定する必要があります。

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
[on-demand notification](#on-demand-notifications) を送信する場合、`toMail` メソッドに指定される `$notifiable` インスタンスは、オンデマンド通知の送信先となる電子メール アドレスを取得するために使用できる `routeNotificationFor` メソッドを提供する `Illuminate\Notifications\AnonymousNotifiable` のインスタンスになります。

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
メール通知テンプレートを設計する場合、一般的な Blade テンプレートと同様に、レンダリングされたメール メッセージをブラウザですばやくプレビューできると便利です。このため、Laravel では、メール通知によって生成されたメール メッセージをルート クロージャーまたはコントローラから直接返すことができます。 `MailMessage` が返されると、ブラウザーにレンダリングされて表示されるため、実際の電子メール アドレスに送信しなくても、そのデザインをすばやくプレビューできます。

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
マークダウン メール通知を使用すると、メール通知の事前に構築されたテンプレートを利用できると同時に、カスタマイズされた長いメッセージをより自由に作成できるようになります。メッセージは Markdown で記述されているため、Laravel はメッセージ用の美しく応答性の高い HTML テンプレートをレンダリングできると同時に、対応するプレーンテキストも自動的に生成します。

<a name="generating-the-message"></a>
<!-- ### Generating The Message -->
### Generating The Message

<!-- To generate a notification with a corresponding Markdown template, you may use the `--markdown` option of the `make:notification` Artisan command: -->
対応するマークダウン テンプレートで通知を生成するには、`make:notification` Artisan コマンドの `--markdown` オプションを使用できます。

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

<!-- Like all other mail notifications, notifications that use Markdown templates should define a `toMail` method on their notification class. However, instead of using the `line` and `action` methods to construct the notification, use the `markdown` method to specify the name of the Markdown template that should be used. An array of data you wish to make available to the template may be passed as the method's second argument: -->
他のすべてのメール通知と同様、Markdown テンプレートを使用する通知は、通知クラスで `toMail` メソッドを定義する必要があります。ただし、`line` メソッドと `action` メソッドを使用して通知を作成する代わりに、`markdown` メソッドを使用して、使用する必要がある Markdown テンプレートの名前を指定します。テンプレートで使用できるようにしたいデータの配列は、メソッドの 2 番目の引数として渡すことができます。

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
Markdown メール通知では、Blade コンポーネントと Markdown 構文の組み合わせを使用するため、Laravel の事前に作成された通知コンポーネントを活用しながら、通知を簡単に構築できます。

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
ボタン コンポーネントは、中央にボタン リンクをレンダリングします。このコンポーネントは、`url` とオプションの `color` の 2 つの引数を受け入れます。サポートされている色は、`primary`、`green`、および `red` です。ボタン コンポーネントは必要なだけ通知に追加できます。

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
<!-- #### Panel Component -->
#### Panel Component

<!-- The panel component renders the given block of text in a panel that has a slightly different background color than the rest of the notification. This allows you to draw attention to a given block of text: -->
パネル コンポーネントは、通知の残りの部分とはわずかに異なる背景色を持つパネルに指定されたテキスト ブロックをレンダリングします。これにより、特定のテキスト ブロックに注意を向けることができます。

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
<!-- #### Table Component -->
#### Table Component

<!-- The table component allows you to transform a Markdown table into an HTML table. The component accepts the Markdown table as its content. Table column alignment is supported using the default Markdown table alignment syntax: -->
table コンポーネントを使用すると、Markdown テーブルを HTML テーブルに変換できます。コンポーネントは、Markdown テーブルをコンテンツとして受け入れます。テーブル列の配置は、デフォルトの Markdown テーブル配置構文を使用してサポートされます。

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
すべての Markdown 通知コンポーネントを独自のアプリケーションにエクスポートしてカスタマイズできます。コンポーネントをエクスポートするには、`vendor:publish` Artisan コマンドを使用して、`laravel-mail` アセット タグを公開します。

```shell
php artisan vendor:publish --tag=laravel-mail
```

<!-- This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like. -->
このコマンドは、Markdown メール コンポーネントを `resources/views/vendor/mail` ディレクトリに公開します。 `mail` ディレクトリには、`html` ディレクトリと `text` ディレクトリが含まれ、それぞれに使用可能なすべてのコンポーネントのそれぞれの表現が含まれます。これらのコンポーネントは自由にカスタマイズできます。

<a name="customizing-the-css"></a>
<!-- #### Customizing The CSS -->
#### Customizing The CSS

<!-- After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be in-lined within the HTML representations of your Markdown notifications. -->
コンポーネントをエクスポートすると、`resources/views/vendor/mail/html/themes` ディレクトリに `default.css` ファイルが含まれます。このファイルの CSS をカスタマイズすると、スタイルは Markdown 通知の HTML 表現内に自動的にインラインで組み込まれます。

<!-- If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of the `mail` configuration file to match the name of your new theme. -->
Laravel の Markdown コンポーネント用にまったく新しいテーマを構築したい場合は、CSS ファイルを `html/themes` ディレクトリ内に配置できます。 CSS ファイルに名前を付けて保存した後、`mail` 構成ファイルの `theme` オプションを新しいテーマの名前と一致するように更新します。

<!-- To customize the theme for an individual notification, you may call the `theme` method while building the notification's mail message. The `theme` method accepts the name of the theme that should be used when sending the notification: -->
個々の通知のテーマをカスタマイズするには、通知のメール メッセージを作成するときに `theme` メソッドを呼び出すことができます。 `theme` メソッドは、通知の送信時に使用するテーマの名前を受け入れます。

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
`database` 通知チャネルは、通知情報をデータベース テーブルに保存します。このテーブルには、通知タイプや通知を説明する JSON データ構造などの情報が含まれます。

<!-- You can query the table to display the notifications in your application's user interface. But, before you can do that, you will need to create a database table to hold your notifications. You may use the `notifications:table` command to generate a [migration](/docs/9.x/migrations) with the proper table schema: -->
テーブルをクエリして、アプリケーションのユーザー インターフェイスに通知を表示できます。ただし、その前に、通知を保持するデータベース テーブルを作成する必要があります。 `notifications:table` コマンドを使用して、適切なテーブル スキーマを持つ [migration](/docs/9.x/migrations) を生成できます。

```shell
php artisan notifications:table

php artisan migrate
```

<a name="formatting-database-notifications"></a>
<!-- ### Formatting Database Notifications -->
### Formatting Database Notifications

<!-- If a notification supports being stored in a database table, you should define a `toDatabase` or `toArray` method on the notification class. This method will receive a `$notifiable` entity and should return a plain PHP array. The returned array will be encoded as JSON and stored in the `data` column of your `notifications` table. Let's take a look at an example `toArray` method: -->
通知がデータベース テーブルへの保存をサポートしている場合は、通知クラスで `toDatabase` メソッドまたは `toArray` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、プレーンな PHP 配列を返す必要があります。返された配列は JSON としてエンコードされ、`notifications` テーブルの `data` 列に保存されます。 `toArray` メソッドの例を見てみましょう。

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
`toArray` メソッドは、JavaScript を利用したフロントエンドにブロードキャストするデータを決定するために、`broadcast` チャネルでも使用されます。 `database` チャネルと `broadcast` チャネルに 2 つの異なる配列表現を使用したい場合は、`toArray` メソッドの代わりに `toDatabase` メソッドを定義する必要があります。

<a name="accessing-the-notifications"></a>
<!-- ### Accessing The Notifications -->
### Accessing The Notifications

<!-- Once notifications are stored in the database, you need a convenient way to access them from your notifiable entities. The `Illuminate\Notifications\Notifiable` trait, which is included on Laravel's default `App\Models\User` model, includes a `notifications` [Eloquent relationship](/docs/9.x/eloquent-relationships) that returns the notifications for the entity. To fetch notifications, you may access this method like any other Eloquent relationship. By default, notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
通知がデータベースに保存されたら、通知対象エンティティから通知にアクセスする便利な方法が必要になります。 Laravel のデフォルトの `App\Models\User` モデルに含まれる `Illuminate\Notifications\Notifiable` トレイトには、エンティティの通知を返す `notifications` [Eloquent relationship](/docs/9.x/eloquent-relationships) が含まれています。通知を取得するには、他の Eloquent 関係と同様に、このメソッドにアクセスできます。デフォルトでは、通知は `created_at` タイムスタンプによって並べ替えられ、最新の通知がコレクションの先頭に表示されます。

```
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

<!-- If you want to retrieve only the "unread" notifications, you may use the `unreadNotifications` relationship. Again, these notifications will be sorted by the `created_at` timestamp with the most recent notifications at the beginning of the collection: -->
「未読」通知のみを取得したい場合は、`unreadNotifications` 関係を使用できます。繰り返しますが、これらの通知は `created_at` タイムスタンプによって並べ替えられ、最新の通知がコレクションの先頭に表示されます。

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript クライアントから通知にアクセスするには、現在のユーザーなどの通知可能なエンティティに通知を返すアプリケーションの通知コントローラを定義する必要があります。その後、JavaScript クライアントからそのコントローラの URL に対して HTTP リクエストを行うことができます。

<a name="marking-notifications-as-read"></a>
<!-- ### Marking Notifications As Read -->
### Marking Notifications As Read

<!-- Typically, you will want to mark a notification as "read" when a user views it. The `Illuminate\Notifications\Notifiable` trait provides a `markAsRead` method, which updates the `read_at` column on the notification's database record: -->
通常、ユーザーが通知を表示したときに、通知を「既読」としてマークする必要があります。 `Illuminate\Notifications\Notifiable` トレイトは、通知のデータベース レコードの `read_at` 列を更新する `markAsRead` メソッドを提供します。

```
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

<!-- However, instead of looping through each notification, you may use the `markAsRead` method directly on a collection of notifications: -->
ただし、各通知をループする代わりに、通知のコレクションに対して `markAsRead` メソッドを直接使用することもできます。

```
$user->unreadNotifications->markAsRead();
```

<!-- You may also use a mass-update query to mark all of the notifications as read without retrieving them from the database: -->
一括更新クエリを使用して、データベースから通知を取得せずに、すべての通知を既読としてマークすることもできます。

```
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

<!-- You may `delete` the notifications to remove them from the table entirely: -->
通知を `delete` してテーブルから完全に削除できます。

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
通知をブロードキャストする前に、Laravel の [event broadcasting](/docs/9.x/broadcasting) サービスを設定し、よく理解しておく必要があります。イベントブロードキャストは、JavaScript を利用したフロントエンドからサーバーサイドの Laravel イベントに反応する方法を提供します。

<a name="formatting-broadcast-notifications"></a>
<!-- ### Formatting Broadcast Notifications -->
### Formatting Broadcast Notifications

<!-- The `broadcast` channel broadcasts notifications using Laravel's [event broadcasting](/docs/9.x/broadcasting) services, allowing your JavaScript powered frontend to catch notifications in realtime. If a notification supports broadcasting, you can define a `toBroadcast` method on the notification class. This method will receive a `$notifiable` entity and should return a `BroadcastMessage` instance. If the `toBroadcast` method does not exist, the `toArray` method will be used to gather the data that should be broadcast. The returned data will be encoded as JSON and broadcast to your JavaScript powered frontend. Let's take a look at an example `toBroadcast` method: -->
`broadcast` チャネルは、Laravel の [event broadcasting](/docs/9.x/broadcasting) サービスを使用して通知をブロードキャストし、JavaScript を利用したフロントエンドがリアルタイムで通知をキャッチできるようにします。通知がブロードキャストをサポートしている場合は、通知クラスで `toBroadcast` メソッドを定義できます。このメソッドは `$notifiable` エンティティを受け取り、`BroadcastMessage` インスタンスを返す必要があります。 `toBroadcast` メソッドが存在しない場合は、ブロードキャストするデータを収集するために `toArray` メソッドが使用されます。返されたデータは JSON としてエンコードされ、JavaScript を利用したフロントエンドにブロードキャストされます。 `toBroadcast` メソッドの例を見てみましょう。

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
すべてのブロードキャスト通知はブロードキャストのためにキューに入れられます。ブロードキャスト操作をキューに入れるために使用されるキュー接続またはキュー名を構成したい場合は、`BroadcastMessage` の `onConnection` および `onQueue` メソッドを使用できます。

```
return (new BroadcastMessage($data))
                ->onConnection('sqs')
                ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
<!-- #### Customizing The Notification Type -->
#### Customizing The Notification Type

<!-- In addition to the data you specify, all broadcast notifications also have a `type` field containing the full class name of the notification. If you would like to customize the notification `type`, you may define a `broadcastType` method on the notification class: -->
指定したデータに加えて、すべてのブロードキャスト通知には、通知の完全なクラス名を含む `type` フィールドもあります。通知 `type` をカスタマイズしたい場合は、通知クラスで `broadcastType` メソッドを定義できます。

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
通知は、`{notifiable}.{id}` 規則を使用してフォーマットされたプライベート チャネルでブロードキャストされます。したがって、`1` の ID を持つ `App\Models\User` インスタンスに通知を送信する場合、通知は `App.Models.User.1` プライベート チャネルでブロードキャストされます。 [Laravel Echo](/docs/9.x/broadcasting#client-side-installation) を使用する場合、`notification` メソッドを使用してチャネル上の通知を簡単にリッスンできます。

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
エンティティのブロードキャスト通知がどのチャネルでブロードキャストされるかをカスタマイズしたい場合は、通知可能なエンティティで `receivesBroadcastNotificationsOn` メソッドを定義できます。

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
Laravel での SMS 通知の送信は、[Vonage](https://www.vonage.com/) (旧名 Nexmo) を利用しています。 Vonage 経由で通知を送信する前に、`laravel/vonage-notification-channel` および `guzzlehttp/guzzle` パッケージをインストールする必要があります。

```
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

<!-- The package includes a [configuration file](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php). However, you are not required to export this configuration file to your own application. You can simply use the `VONAGE_KEY` and `VONAGE_SECRET` environment variables to define your Vonage public and secret keys. -->
パッケージには [configuration file](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php) が含まれています。ただし、この構成ファイルを独自のアプリケーションにエクスポートする必要はありません。 `VONAGE_KEY` および `VONAGE_SECRET` 環境変数を使用するだけで、Vonage の公開キーと秘密キーを定義できます。

<!-- After defining your keys, you should set a `VONAGE_SMS_FROM` environment variable that defines the phone number that your SMS messages should be sent from by default. You may generate this phone number within the Vonage control panel: -->
キーを定義した後、デフォルトで SMS メッセージの送信元となる電話番号を定義する `VONAGE_SMS_FROM` 環境変数を設定する必要があります。この電話番号は、Vonage コントロール パネル内で生成できます。

```
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
<!-- ### Formatting SMS Notifications -->
### Formatting SMS Notifications

<!-- If a notification supports being sent as an SMS, you should define a `toVonage` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\VonageMessage` instance: -->
通知が SMS としての送信をサポートしている場合は、通知クラスで `toVonage` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Messages\VonageMessage` インスタンスを返す必要があります。

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
SMS メッセージに Unicode 文字が含まれる場合は、`VonageMessage` インスタンスを構築するときに `unicode` メソッドを呼び出す必要があります。

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
`VONAGE_SMS_FROM` 環境変数で指定された電話番号とは異なる電話番号から通知を送信したい場合は、`VonageMessage` インスタンスで `from` メソッドを呼び出すことができます。

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
ユーザー、チーム、またはクライアントごとのコストを追跡したい場合は、通知に「クライアント参照」を追加できます。 Vonage では、このクライアント リファレンスを使用してレポートを生成できるため、特定の顧客の SMS の使用状況をよりよく理解できます。クライアント参照には、最大 40 文字の任意の文字列を指定できます。

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
Vonage 通知を適切な電話番号にルーティングするには、通知対象エンティティで `routeNotificationForVonage` メソッドを定義します。

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
Slack 経由で通知を送信するには、Composer 経由で Slack 通知チャネルをインストールする必要があります。

```shell
composer require laravel/slack-notification-channel
```

<!-- You will also need to create a [Slack App](https://api.slack.com/apps?new_app=1) for your team. After creating the App, you should configure an "Incoming Webhook" for the workspace. Slack will then provide you with a webhook URL that you may use when [routing Slack notifications](#routing-slack-notifications). -->
チーム用に [Slack App](https://api.slack.com/apps?new_app=1) を作成する必要もあります。アプリを作成した後、ワークスペースの「受信 Webhook」を構成する必要があります。 Slack は、[routing Slack notifications](#routing-slack-notifications) のときに使用できる Webhook URL を提供します。

<a name="formatting-slack-notifications"></a>
<!-- ### Formatting Slack Notifications -->
### Formatting Slack Notifications

<!-- If a notification supports being sent as a Slack message, you should define a `toSlack` method on the notification class. This method will receive a `$notifiable` entity and should return an `Illuminate\Notifications\Messages\SlackMessage` instance. Slack messages may contain text content as well as an "attachment" that formats additional text or an array of fields. Let's take a look at a basic `toSlack` example: -->
通知が Slack メッセージとしての送信をサポートしている場合は、通知クラスで `toSlack` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Messages\SlackMessage` インスタンスを返す必要があります。 Slack メッセージには、テキスト コンテンツに加えて、追加のテキストやフィールドの配列をフォーマットする「添付ファイル」が含まれる場合があります。基本的な `toSlack` の例を見てみましょう。

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
Slack メッセージに「添付ファイル」を追加することもできます。添付ファイルには、単純なテキスト メッセージよりも豊富な書式設定オプションが用意されています。この例では、アプリケーションで発生した例外に関するエラー通知を、例外の詳細を表示するリンクを含めて送信します。

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
添付ファイルを使用すると、ユーザーに表示するデータの配列を指定することもできます。指定されたデータは、読みやすいように表形式で表示されます。

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
添付ファイル フィールドの一部に Markdown が含まれている場合は、`markdown` メソッドを使用して、指定された添付フィールドを解析して Markdown 形式のテキストとして表示するように Slack に指示できます。このメソッドで受け入れられる値は、`pretext`、`text`、および/または `fields` です。 Slack の添付ファイルの形式の詳細については、[Slack API documentation](https://api.slack.com/docs/message-formatting#message_formatting) を確認してください。

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
Slack 通知を適切な Slack チームとチャネルにルーティングするには、通知対象エンティティで `routeNotificationForSlack` メソッドを定義します。これにより、通知の配信先となる Webhook URL が返されます。 Webhook URL は、Slack チームに「Incoming Webhook」サービスを追加することで生成できます。

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
Laravel では、HTTP リクエストの現在のロケール以外のロケールで通知を送信することができ、通知がキューに入れられている場合でもこのロケールを記憶します。

<!-- To accomplish this, the `Illuminate\Notifications\Notification` class offers a `locale` method to set the desired language. The application will change into this locale when the notification is being evaluated and then revert back to the previous locale when evaluation is complete: -->
これを実現するために、`Illuminate\Notifications\Notification` クラスは、希望の言語を設定するための `locale` メソッドを提供します。アプリケーションは、通知の評価中にこのロケールに変更され、評価が完了すると前のロケールに戻ります。

```
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

<!-- Localization of multiple notifiable entries may also be achieved via the `Notification` facade: -->
複数の通知可能なエントリのローカライズは、`Notification` ファサードを介して実現することもできます。

```
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
<!-- ### User Preferred Locales -->
### User Preferred Locales

<!-- Sometimes, applications store each user's preferred locale. By implementing the `HasLocalePreference` contract on your notifiable model, you may instruct Laravel to use this stored locale when sending a notification: -->
場合によっては、アプリケーションが各ユーザーの優先ロケールを保存することがあります。通知可能モデルに `HasLocalePreference` コントラクトを実装することで、通知を送信するときにこの保存されたロケールを使用するように Laravel に指示できます。

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
インターフェースを実装すると、Laravel は通知とメール可能ファイルをモデルに送信するときに優先ロケールを自動的に使用します。したがって、このインターフェイスを使用する場合は、`locale` メソッドを呼び出す必要はありません。

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
通知の送信中に、通知システムによって `Illuminate\Notifications\Events\NotificationSending` [event](/docs/9.x/events) がディスパッチされます。これには、「通知可能な」エンティティと通知インスタンス自体が含まれます。アプリケーションの `EventServiceProvider` でこのイベントのリスナを登録できます。

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
`NotificationSending` イベントのイベント リスナが `handle` メソッドから `false` を返した場合、通知は送信されません。

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
イベント リスナ内で、イベントの `notifiable`、`notification`、および `channel` プロパティにアクセスして、通知受信者または通知自体の詳細を確認できます。

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
通知が送信されると、通知システムによって `Illuminate\Notifications\Events\NotificationSent` [event](/docs/9.x/events) がディスパッチされます。これには、「通知可能な」エンティティと通知インスタンス自体が含まれます。 `EventServiceProvider` でこのイベントのリスナを登録できます。

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
> `EventServiceProvider` にリスナを登録した後、`event:generate` Artisan コマンドを使用してリスナ クラスをすばやく生成します。

<!-- Within an event listener, you may access the `notifiable`, `notification`, `channel`, and `response` properties on the event to learn more about the notification recipient or the notification itself: -->
イベント リスナ内で、イベントの `notifiable`、`notification`、`channel`、および `response` プロパティにアクセスして、通知受信者または通知自体の詳細を確認できます。

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
Laravel にはいくつかの通知チャネルが付属していますが、他のチャネル経由で通知を配信する独自​​のドライバを作成することもできます。 Laravel を使えば簡単になります。まず、`send` メソッドを含むクラスを定義します。このメソッドは、`$notifiable` と `$notification` の 2 つの引数を受け取る必要があります。

<!-- Within the `send` method, you may call methods on the notification to retrieve a message object understood by your channel and then send the notification to the `$notifiable` instance however you wish: -->
`send` メソッド内で、通知のメソッドを呼び出して、チャネルによって理解されるメッセージ オブジェクトを取得し、通知を `$notifiable` インスタンスに送信することができます。

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
通知チャネル クラスを定義したら、任意の通知の `via` メソッドからクラス名を返すことができます。この例では、通知の `toVoice` メソッドは、音声メッセージを表すために選択したオブジェクトを返すことができます。たとえば、次のメッセージを表す独自の `VoiceMessage` クラスを定義できます。

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

