# 通知 (Notifications)

- [Introduction](#introduction)
- [通知の生成](#generating-notifications)
- [通知の送信](#sending-notifications)
    - [通知可能な特性の使用](#using-the-notifiable-trait)
    - [通知ファサードの使用](#using-the-notification-facade)
    - [配信チャネルの指定](#specifying-delivery-channels)
    - [通知のキューイング](#queueing-notifications)
    - [オンデマンド通知](#on-demand-notifications)
- [メール通知](#mail-notifications)
    - [メールメッセージのフォーマット](#formatting-mail-messages)
    - [送信者のカスタマイズ](#customizing-the-sender)
    - [受信者のカスタマイズ](#customizing-the-recipient)
    - [件名のカスタマイズ](#customizing-the-subject)
    - [メーラーのカスタマイズ](#customizing-the-mailer)
    - [テンプレートのカスタマイズ](#customizing-the-templates)
    - [Attachments](#mail-attachments)
    - [タグとメタデータの追加](#adding-tags-metadata)
    - [Symfony メッセージのカスタマイズ](#customizing-the-symfony-message)
    - [メール可能ファイルの使用](#using-mailables)
    - [メール通知のプレビュー](#previewing-mail-notifications)
- [マークダウンメール通知](#markdown-mail-notifications)
    - [メッセージの生成](#generating-the-message)
    - [メッセージを書く](#writing-the-message)
    - [コンポーネントのカスタマイズ](#customizing-the-components)
- [データベース通知](#database-notifications)
    - [Prerequisites](#database-prerequisites)
    - [データベース通知のフォーマット](#formatting-database-notifications)
    - [通知へのアクセス](#accessing-the-notifications)
    - [通知を既読としてマークする](#marking-notifications-as-read)
- [ブロードキャスト通知](#broadcast-notifications)
    - [Prerequisites](#broadcast-prerequisites)
    - [ブロードキャスト通知のフォーマット](#formatting-broadcast-notifications)
    - [通知を聞く](#listening-for-notifications)
- [SMS通知](#sms-notifications)
    - [Prerequisites](#sms-prerequisites)
    - [SMS 通知のフォーマット](#formatting-sms-notifications)
    - [「差出人」番号のカスタマイズ](#customizing-the-from-number)
    - [クライアント参照の追加](#adding-a-client-reference)
    - [SMS 通知のルーティング](#routing-sms-notifications)
- [Slack 通知](#slack-notifications)
    - [Prerequisites](#slack-prerequisites)
    - [Slack 通知の書式設定](#formatting-slack-notifications)
    - [Slack のインタラクティブ性](#slack-interactivity)
    - [Slack 通知のルーティング](#routing-slack-notifications)
    - [外部 Slack ワークスペースへの通知](#notifying-external-slack-workspaces)
- [通知のローカライズ](#localizing-notifications)
- [Testing](#testing)
- [通知イベント](#notification-events)
- [カスタムチャンネル](#custom-channels)

<a name="introduction"></a>
## 導入 (Introduction)

[電子メールの送信](/docs/{{version}}/mail) のサポートに加えて、Laravel は、電子メール、SMS (旧 Nexmo である [Vonage](https://www.vonage.com/communications-apis/) 経由)、[Slack](https://slack.com) など、さまざまな配信チャネルで通知を送信するためのサポートを提供します。さらに、数十の異なるチャネルで通知を送信するために、さまざまな [コミュニティが構築した通知チャネル](https://laravel-notification-channels.com/about/#suggesting-a-new-channel) が作成されています。通知はデータベースに保存され、Web インターフェイスに表示される場合もあります。

通常、通知は、アプリケーションで発生した何かをユーザーに通知する短い情報メッセージである必要があります。たとえば、請求アプリケーションを作成している場合、電子メールと SMS チャネルを介してユーザーに「請求書支払い済み」通知を送信できます。

<a name="generating-notifications"></a>
## 通知の生成 (Generating Notifications)

Laravel では、各通知は単一のクラスで表され、通常は `app/Notifications` ディレクトリに保存されます。アプリケーションにこのディレクトリが表示されなくても心配する必要はありません。`make:notification` Artisan コマンドを実行すると作成されます。

```shell
php artisan make:notification InvoicePaid
```

このコマンドは、新しい通知クラスを `app/Notifications` ディレクトリに配置します。各通知クラスには、`via` メソッドと、通知をその特定のチャネルに合わせたメッセージに変換する `toMail` や `toDatabase` などの可変数のメッセージ構築メソッドが含まれています。

<a name="sending-notifications"></a>
## 通知の送信 (Sending Notifications)

<a name="using-the-notifiable-trait"></a>
### 通知可能な特性の使用

通知は 2 つの方法で送信できます。`Notifiable` 特性の `notify` メソッドを使用する方法と、`Notification` [facade](/docs/{{version}}/facades) を使用する方法です。 `Notifiable` 特性は、デフォルトでアプリケーションの `App\Models\User` モデルに含まれています。

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

この特性によって提供される `notify` メソッドは、通知インスタンスを受信することを想定しています。

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```

> [!NOTE]
> どのモデルでも `Notifiable` トレイトを使用できることに注意してください。 `User` モデルに含めるだけに限定されるわけではありません。

<a name="using-the-notification-facade"></a>
### 通知ファサードの使用

あるいは、`Notification` [facade](/docs/{{version}}/facades) 経由で通知を送信することもできます。このアプローチは、ユーザーのコレクションなど、複数の通知対象エンティティに通知を送信する必要がある場合に便利です。ファサードを使用して通知を送信するには、すべての通知可能なエンティティと通知インスタンスを `send` メソッドに渡します。

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```

`sendNow` メソッドを使用して、すぐに通知を送信することもできます。このメソッドは、通知が `ShouldQueue` インターフェイスを実装している場合でも、通知をすぐに送信します。

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```

<a name="specifying-delivery-channels"></a>
### 配信チャネルの指定

すべての通知クラスには、通知が配信されるチャネルを決定する `via` メソッドがあります。通知は、`mail`、`database`、`broadcast`、`vonage`、および `slack` チャネルで送信される場合があります。

> [!NOTE]
> Telegram や Pusher などの他の配信チャネルを使用したい場合は、コミュニティ主導の [Laravel 通知チャネル Web サイト](http://laravel-notification-channels.com) をチェックしてください。

`via` メソッドは、通知の送信先となるクラスのインスタンスとなる `$notifiable` インスタンスを受け取ります。 `$notifiable` を使用して、通知を配信するチャネルを決定できます。

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
### 通知のキューイング

> [!WARNING]
> 通知をキューに入れる前に、キューと [ワーカーを始める](/docs/{{version}}/queues#running-the-queue-worker) を設定する必要があります。

特にチャネルが通知を配信するために外部 API 呼び出しを行う必要がある場合、通知の送信には時間がかかることがあります。アプリケーションの応答時間を短縮するには、`ShouldQueue` インターフェイスと `Queueable` トレイトをクラスに追加して、通知をキューに入れます。インターフェイスと特性は、`make:notification` コマンドを使用して生成されたすべての通知に対してすでにインポートされているため、通知クラスにすぐに追加できます。

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

`ShouldQueue` インターフェイスが通知に追加されたら、通常どおり通知を送信できます。 Laravel はクラス上の `ShouldQueue` インターフェイスを検出し、通知の配信を自動的にキューに入れます。

```php
$user->notify(new InvoicePaid($invoice));
```

通知をキューに入れると、受信者とチャネルの組み合わせごとにキューに入れられたジョブが作成されます。たとえば、通知に 3 人の受信者と 2 つのチャネルがある場合、6 つのジョブがキューにディスパッチされます。

<a name="delaying-notifications"></a>
#### 通知の遅延

通知の配信を遅らせたい場合は、通知のインスタンス化に `delay` メソッドを連鎖させます。

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```

配列を `delay` メソッドに渡して、特定のチャネルの遅​​延量を指定できます。

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```

あるいは、通知クラス自体に `withDelay` メソッドを定義することもできます。 `withDelay` メソッドは、チャネル名と遅延値の配列を返す必要があります。

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
#### 通知キュー接続のカスタマイズ

デフォルトでは、キューに入れられた通知は、アプリケーションのデフォルトのキュー接続を使用してキューに入れられます。特定の通知に使用する別の接続を指定したい場合は、通知のコンストラクターから `onConnection` メソッドを呼び出すことができます。

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

または、通知でサポートされる各通知チャネルに使用する特定のキュー接続を指定したい場合は、通知で `viaConnections` メソッドを定義できます。このメソッドは、チャネル名とキュー接続名のペアの配列を返す必要があります。

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
#### 通知チャネルキューのカスタマイズ

通知でサポートされる各通知チャネルに使用する特定のキューを指定したい場合は、通知で `viaQueues` メソッドを定義できます。このメソッドは、チャネル名とキュー名のペアの配列を返す必要があります。

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
#### キューに入れられた通知ジョブのプロパティのカスタマイズ

通知クラスのプロパティを定義することで、基になるキューに入れられたジョブの動作をカスタマイズできます。これらのプロパティは、通知を送信するキューに入れられたジョブによって継承されます。

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

[encryption](/docs/{{version}}/encryption) 経由でキューに入れられた通知データのプライバシーと整合性を確保したい場合は、通知クラスに `ShouldBeEncrypted` インターフェイスを追加します。

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

これらのプロパティを通知クラスで直接定義することに加えて、`backoff` メソッドと `retryUntil` メソッドを定義して、キューに入れられた通知ジョブのバックオフ戦略と再試行タイムアウトを指定することもできます。

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
> これらのジョブのプロパティとメソッドの詳細については、[キューに入れられたジョブ](/docs/{{version}}/queues#max-job-attempts-and-timeout) のドキュメントを参照してください。

<a name="queued-notification-middleware"></a>
#### キューに入れられた通知ミドルウェア

キューに入れられた通知はミドルウェア [キューに入れられたジョブと同じように](/docs/{{version}}/queues#job-middleware) を定義する場合があります。まず、通知クラスで `middleware` メソッドを定義します。 `middleware` メソッドは `$notifiable` 変数と `$channel` 変数を受け取ります。これにより、返されるミドルウェアを通知の宛先に基づいてカスタマイズできます。

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
#### キューに入れられた通知とデータベーストランザクション

キューに入れられた通知がデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって通知が処理される場合があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。通知がこれらのモデルに依存している場合、キューに入れられた通知を送信するジョブの処理時に予期しないエラーが発生する可能性があります。

キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、通知の送信時に `afterCommit` メソッドを呼び出すことにより、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられた通知を送信する必要があることを示すことができます。

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```

あるいは、通知のコンストラクターから `afterCommit` メソッドを呼び出すこともできます。

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
> これらの問題の回避方法の詳細については、[キューに入れられたジョブとデータベース トランザクション](/docs/{{version}}/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### キューに入れられた通知を送信するかどうかの決定

キューに入れられた通知は、バックグラウンド処理のためにキューにディスパッチされた後、通常、キューワーカーによって受け入れられ、目的の受信者に送信されます。

ただし、キューに入れられた通知がキューワーカーによって処理された後に送信するかどうかを最終決定したい場合は、通知クラスで `shouldSend` メソッドを定義できます。このメソッドが `false` を返した場合、通知は送信されません。

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
#### 通知の送信後

通知の送信後にコードを実行したい場合は、通知クラスで `afterSending` メソッドを定義できます。このメソッドは、通知対象エンティティ、チャネル名、チャネルからの応答を受け取ります。

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
### オンデマンド通知

場合によっては、アプリケーションの「ユーザー」として保存されていない人に通知を送信する必要がある場合があります。 `Notification` ファサードの `route` メソッドを使用すると、通知を送信する前にアドホック通知ルーティング情報を指定できます。

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```

オンデマンド通知を `mail` ルートに送信するときに受信者の名前を指定したい場合は、電子メール アドレスをキーとして、名前を配列の最初の要素の値として含む配列を指定できます。

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```

`routes` メソッドを使用すると、複数の通知チャネルにアドホック ルーティング情報を一度に提供できます。

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```

<a name="mail-notifications"></a>
## メール通知 (Mail Notifications)

<a name="formatting-mail-messages"></a>
### メールメッセージのフォーマット

通知が電子メールとして送信されることをサポートしている場合は、通知クラスで `toMail` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Messages\MailMessage` インスタンスを返す必要があります。

`MailMessage` クラスには、トランザクション電子メール メッセージの作成に役立ついくつかの簡単なメソッドが含まれています。メールメッセージには、テキスト行と「行動喚起」が含まれる場合があります。 `toMail` メソッドの例を見てみましょう。

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
> `toMail` メソッドで `$this->invoice->id` を使用していることに注意してください。通知がメッセージを生成するために必要なデータを通知のコンストラクターに渡すことができます。

この例では、挨拶、テキスト行、行動喚起、そして別のテキスト行を登録します。 `MailMessage` オブジェクトによって提供されるこれらのメソッドにより、小規模なトランザクション電子メールのフォーマットが簡単かつ迅速になります。次に、メール チャネルは、メッセージ コンポーネントを、対応するプレーン テキストを含む美しく応答性の高い HTML 電子メール テンプレートに変換します。 `mail` チャネルによって生成された電子メールの例を次に示します。

<img src="https://laravel.com/img/docs/notification-example-2.png">

> [!NOTE]
> メール通知を送信するときは、`config/app.php` 構成ファイルで `name` 構成オプションを必ず設定してください。この値は、メール通知メッセージのヘッダーとフッターで使用されます。

<a name="error-messages"></a>
#### エラーメッセージ

一部の通知は、請求書支払いの失敗などのエラーをユーザーに通知します。メッセージの作成時に `error` メソッドを呼び出すことで、メール メッセージがエラーに関するものであることを示すことができます。メール メッセージで `error` メソッドを使用すると、CTA ボタンが黒ではなく赤になります。

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
#### その他のメール通知の形式オプション

通知クラスでテキストの「行」を定義する代わりに、`view` メソッドを使用して、通知電子メールのレンダリングに使用するカスタム テンプレートを指定できます。

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

`view` メソッドに与えられる配列の 2 番目の要素としてビュー名を渡すことで、メール メッセージのプレーンテキスト ビューを指定できます。

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

または、メッセージにプレーンテキスト ビューのみがある場合は、`text` メソッドを利用できます。

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
### 送信者のカスタマイズ

デフォルトでは、電子メールの送信者/差出人のアドレスは、`config/mail.php` 構成ファイルで定義されます。ただし、`from` メソッドを使用して、特定の通知の送信元アドレスを指定できます。

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
### 受信者のカスタマイズ

`mail` チャネル経由で通知を送信すると、通知システムは通知対象エンティティの `email` プロパティを自動的に検索します。通知可能なエンティティで `routeNotificationForMail` メソッドを定義することにより、通知の配信に使用される電子メール アドレスをカスタマイズできます。

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
### 件名のカスタマイズ

デフォルトでは、電子メールの件名は、「Title Case」にフォーマットされた通知のクラス名です。したがって、通知クラスの名前が `InvoicePaid` の場合、電子メールの件名は `Invoice Paid` になります。メッセージに別の件名を指定したい場合は、メッセージの作成時に `subject` メソッドを呼び出すことができます。

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
### メーラーのカスタマイズ

デフォルトでは、電子メール通知は、`config/mail.php` 構成ファイルで定義されたデフォルトのメーラーを使用して送信されます。ただし、メッセージの作成時に `mailer` メソッドを呼び出すことで、実行時に別のメーラーを指定できます。

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
### テンプレートのカスタマイズ

通知パッケージのリソースを公開することで、メール通知で使用される HTML およびプレーンテキストのテンプレートを変更できます。このコマンドを実行すると、メール通知テンプレートが `resources/views/vendor/notifications` ディレクトリに配置されます。

```shell
php artisan vendor:publish --tag=laravel-notifications
```

<a name="mail-attachments"></a>
### 添付ファイル

電子メール通知に添付ファイルを追加するには、メッセージの作成時に `attach` メソッドを使用します。 `attach` メソッドは、最初の引数としてファイルへの絶対パスを受け入れます。

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
> 通知メール メッセージによって提供される `attach` メソッドは、[取り付け可能なオブジェクト](/docs/{{version}}/mail#attachable-objects) も受け入れます。詳細については、包括的な [アタッチ可能なオブジェクトのドキュメント](/docs/{{version}}/mail#attachable-objects) を参照してください。

メッセージにファイルを添付するときは、`array` を `attach` メソッドの 2 番目の引数として渡すことで、表示名や MIME タイプを指定することもできます。

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

メール可能オブジェクトにファイルを添付する場合とは異なり、`attachFromStorage` を使用してストレージ ディスクからファイルを直接添付することはできません。むしろ、ストレージ ディスク上のファイルへの絶対パスを指定して `attach` メソッドを使用する必要があります。あるいは、`toMail` メソッドから [mailable](/docs/{{version}}/mail#generating-mailables) を返すこともできます。

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

必要に応じて、`attachMany` メソッドを使用して複数のファイルをメッセージに添付できます。

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
#### 生データの添付ファイル

`attachData` メソッドを使用して、生のバイト文字列を添付ファイルとして添付できます。 `attachData` メソッドを呼び出すときは、添付ファイルに割り当てるファイル名を指定する必要があります。

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
### タグとメタデータの追加

Mailgun や Postmark などの一部のサードパーティ電子メール プロバイダは、メッセージの「タグ」と「メタデータ」をサポートしています。これらは、アプリケーションによって送信された電子メールをグループ化し、追跡するために使用される場合があります。 `tag` および `metadata` メソッドを使用して、電子メール メッセージにタグとメタデータを追加できます。

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

アプリケーションが Mailgun ドライバを使用している場合、[tags](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) および [metadata](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages) の詳細については、Mailgun のドキュメントを参照してください。同様に、[tags](https://postmarkapp.com/blog/tags-support-for-smtp) および [metadata](https://postmarkapp.com/support/article/1125-custom-metadata-faq) のサポートの詳細については、消印のドキュメントを参照することもできます。

アプリケーションが Amazon SES を使用して E メールを送信している場合は、`metadata` メソッドを使用してメッセージに [SESの「タグ」](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html) を添付する必要があります。

<a name="customizing-the-symfony-message"></a>
### Symfony メッセージのカスタマイズ

`MailMessage` クラスの `withSymfonyMessage` メソッドを使用すると、メッセージを送信する前に Symfony Message インスタンスで呼び出されるクロージャを登録できます。これにより、メッセージを配信する前に詳細にカスタマイズする機会が得られます。

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
### メール可能ファイルの使用

必要に応じて、通知の `toMail` メソッドから完全な [郵送可能なオブジェクト](/docs/{{version}}/mail) を返すことができます。 `MailMessage` の代わりに `Mailable` を返す場合は、メール可能オブジェクトの `to` メソッドを使用してメッセージ受信者を指定する必要があります。

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
#### メール可能アイテムとオンデマンド通知

[オンデマンド通知](#on-demand-notifications) を送信する場合、`toMail` メソッドに指定される `$notifiable` インスタンスは、オンデマンド通知の送信先となる電子メール アドレスを取得するために使用できる `routeNotificationFor` メソッドを提供する `Illuminate\Notifications\AnonymousNotifiable` のインスタンスになります。

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
### メール通知のプレビュー

メール通知テンプレートを設計する場合、一般的な Blade テンプレートと同様に、レンダリングされたメール メッセージをブラウザですばやくプレビューできると便利です。このため、Laravel では、メール通知によって生成されたメール メッセージをルート クロージャーまたはコントローラから直接返すことができます。 `MailMessage` が返されると、ブラウザーにレンダリングされて表示されるため、実際の電子メール アドレスに送信しなくても、そのデザインをすばやくプレビューできます。

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
## マークダウンメール通知 (Markdown Mail Notifications)

マークダウン メール通知を使用すると、メール通知の事前に構築されたテンプレートを利用できると同時に、カスタマイズされた長いメッセージをより自由に作成できるようになります。メッセージは Markdown で記述されているため、Laravel はメッセージ用の美しく応答性の高い HTML テンプレートをレンダリングできると同時に、対応するプレーンテキストも自動的に生成します。

<a name="generating-the-message"></a>
### メッセージの生成

対応するマークダウン テンプレートで通知を生成するには、`make:notification` Artisan コマンドの `--markdown` オプションを使用できます。

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```

他のすべてのメール通知と同様、Markdown テンプレートを使用する通知は、通知クラスで `toMail` メソッドを定義する必要があります。ただし、`line` メソッドと `action` メソッドを使用して通知を作成する代わりに、`markdown` メソッドを使用して、使用する必要がある Markdown テンプレートの名前を指定します。テンプレートで使用できるようにしたいデータの配列は、メソッドの 2 番目の引数として渡すことができます。

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
### メッセージを書く

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

> [!NOTE]
> Markdown メールを作成するときは、過剰なインデントを使用しないでください。 Markdown 標準に従って、Markdown パーサーはインデントされたコンテンツをコード ブロックとしてレンダリングします。

<a name="button-component"></a>
#### ボタンコンポーネント

ボタン コンポーネントは、中央にボタン リンクをレンダリングします。このコンポーネントは、`url` とオプションの `color` の 2 つの引数を受け入れます。サポートされている色は、`primary`、`green`、および `red` です。ボタン コンポーネントは必要なだけ通知に追加できます。

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```

<a name="panel-component"></a>
#### パネルコンポーネント

パネル コンポーネントは、通知の残りの部分とはわずかに異なる背景色を持つパネルに指定されたテキスト ブロックをレンダリングします。これにより、特定のテキスト ブロックに注意を向けることができます。

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```

<a name="table-component"></a>
#### テーブルコンポーネント

table コンポーネントを使用すると、Markdown テーブルを HTML テーブルに変換できます。コンポーネントは、Markdown テーブルをコンテンツとして受け入れます。テーブル列の配置は、デフォルトの Markdown テーブル配置構文を使用してサポートされます。

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```

<a name="customizing-the-components"></a>
### コンポーネントのカスタマイズ

すべての Markdown 通知コンポーネントを独自のアプリケーションにエクスポートしてカスタマイズできます。コンポーネントをエクスポートするには、`vendor:publish` Artisan コマンドを使用して、`laravel-mail` アセット タグを公開します。

```shell
php artisan vendor:publish --tag=laravel-mail
```

このコマンドは、Markdown メール コンポーネントを `resources/views/vendor/mail` ディレクトリに公開します。 `mail` ディレクトリには、`html` ディレクトリと `text` ディレクトリが含まれ、それぞれに使用可能なすべてのコンポーネントのそれぞれの表現が含まれます。これらのコンポーネントは自由にカスタマイズできます。

<a name="customizing-the-css"></a>
#### CSSのカスタマイズ

コンポーネントをエクスポートすると、`resources/views/vendor/mail/html/themes` ディレクトリに `default.css` ファイルが含まれます。このファイルの CSS をカスタマイズすると、スタイルは Markdown 通知の HTML 表現内に自動的にインラインで組み込まれます。

Laravel の Markdown コンポーネント用にまったく新しいテーマを構築したい場合は、CSS ファイルを `html/themes` ディレクトリ内に配置できます。 CSS ファイルに名前を付けて保存した後、`mail` 構成ファイルの `theme` オプションを新しいテーマの名前と一致するように更新します。

個々の通知のテーマをカスタマイズするには、通知のメール メッセージを作成するときに `theme` メソッドを呼び出すことができます。 `theme` メソッドは、通知の送信時に使用するテーマの名前を受け入れます。

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
## データベース通知 (Database Notifications)

<a name="database-prerequisites"></a>
### 前提条件

`database` 通知チャネルは、通知情報をデータベース テーブルに保存します。このテーブルには、通知タイプや通知を説明する JSON データ構造などの情報が含まれます。

テーブルをクエリして、アプリケーションのユーザー インターフェイスに通知を表示できます。ただし、その前に、通知を保持するデータベース テーブルを作成する必要があります。 `make:notifications-table` コマンドを使用して、適切なテーブル スキーマを持つ [migration](/docs/{{version}}/migrations) を生成できます。

```shell
php artisan make:notifications-table

php artisan migrate
```

> [!NOTE]
> 通知対象モデルが [UUID または ULID の主キー](/docs/{{version}}/eloquent#uuid-and-ulid-keys) を使用している場合は、通知テーブルの移行で `morphs` メソッドを [uuidMorphs](/docs/{{version}}/migrations#column-method-uuidMorphs) または [ulidMorphs](/docs/{{version}}/migrations#column-method-ulidMorphs) に置き換える必要があります。

<a name="formatting-database-notifications"></a>
### データベース通知のフォーマット

通知がデータベース テーブルへの保存をサポートしている場合は、通知クラスで `toDatabase` メソッドまたは `toArray` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、プレーンな PHP 配列を返す必要があります。返された配列は JSON としてエンコードされ、`notifications` テーブルの `data` 列に保存されます。 `toArray` メソッドの例を見てみましょう。

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

通知がアプリケーションのデータベースに保存されると、`type` 列はデフォルトで通知のクラス名に設定され、`read_at` 列は `null` になります。ただし、通知クラスで `databaseType` メソッドと `initialDatabaseReadAtValue` メソッドを定義することで、この動作をカスタマイズできます。

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

`toArray` メソッドは、JavaScript を利用したフロントエンドにブロードキャストするデータを決定するために、`broadcast` チャネルでも使用されます。 `database` チャネルと `broadcast` チャネルに 2 つの異なる配列表現を使用したい場合は、`toArray` メソッドの代わりに `toDatabase` メソッドを定義する必要があります。

<a name="accessing-the-notifications"></a>
### 通知へのアクセス

通知がデータベースに保存されたら、通知対象エンティティから通知にアクセスする便利な方法が必要になります。 Laravel のデフォルトの `App\Models\User` モデルに含まれる `Illuminate\Notifications\Notifiable` トレイトには、エンティティの通知を返す `notifications` [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) が含まれています。通知を取得するには、他の Eloquent 関係と同様に、このメソッドにアクセスできます。デフォルトでは、通知は `created_at` タイムスタンプによって並べ替えられ、最新の通知がコレクションの先頭に表示されます。

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```

「未読」通知のみを取得したい場合は、`unreadNotifications` 関係を使用できます。繰り返しますが、これらの通知は `created_at` タイムスタンプによって並べ替えられ、最新の通知がコレクションの先頭に表示されます。

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```

「既読」通知のみを取得したい場合は、`readNotifications` 関係を使用できます。

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```

> [!NOTE]
> JavaScript クライアントから通知にアクセスするには、現在のユーザーなどの通知可能なエンティティに通知を返すアプリケーションの通知コントローラを定義する必要があります。その後、JavaScript クライアントからそのコントローラの URL に対して HTTP リクエストを行うことができます。

<a name="marking-notifications-as-read"></a>
### 通知を既読としてマークする

通常、ユーザーが通知を表示したときに、通知を「既読」としてマークする必要があります。 `Illuminate\Notifications\Notifiable` トレイトは、通知のデータベース レコードの `read_at` 列を更新する `markAsRead` メソッドを提供します。

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```

ただし、各通知をループする代わりに、通知のコレクションに対して `markAsRead` メソッドを直接使用することもできます。

```php
$user->unreadNotifications->markAsRead();
```

一括更新クエリを使用して、データベースから通知を取得せずに、すべての通知を既読としてマークすることもできます。

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```

通知を `delete` してテーブルから完全に削除できます。

```php
$user->notifications()->delete();
```

<a name="broadcast-notifications"></a>
## ブロードキャスト通知 (Broadcast Notifications)

<a name="broadcast-prerequisites"></a>
### 前提条件

通知をブロードキャストする前に、Laravel の [イベント放送](/docs/{{version}}/broadcasting) サービスを設定し、よく理解しておく必要があります。イベントブロードキャストは、JavaScript を利用したフロントエンドからサーバーサイドの Laravel イベントに反応する方法を提供します。

<a name="formatting-broadcast-notifications"></a>
### ブロードキャスト通知のフォーマット

`broadcast` チャネルは、Laravel の [イベント放送](/docs/{{version}}/broadcasting) サービスを使用して通知をブロードキャストし、JavaScript を利用したフロントエンドがリアルタイムで通知をキャッチできるようにします。通知がブロードキャストをサポートしている場合は、通知クラスで `toBroadcast` メソッドを定義できます。このメソッドは `$notifiable` エンティティを受け取り、`BroadcastMessage` インスタンスを返す必要があります。 `toBroadcast` メソッドが存在しない場合は、ブロードキャストするデータを収集するために `toArray` メソッドが使用されます。返されたデータは JSON としてエンコードされ、JavaScript を利用したフロントエンドにブロードキャストされます。 `toBroadcast` メソッドの例を見てみましょう。

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
#### ブロードキャストキューの設定

すべてのブロードキャスト通知はブロードキャストのためにキューに入れられます。ブロードキャスト操作をキューに入れるために使用されるキュー接続またはキュー名を構成したい場合は、`BroadcastMessage` の `onConnection` および `onQueue` メソッドを使用できます。

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```

<a name="customizing-the-notification-type"></a>
#### 通知タイプのカスタマイズ

指定したデータに加えて、すべてのブロードキャスト通知には、通知の完全なクラス名を含む `type` フィールドもあります。通知 `type` をカスタマイズしたい場合は、通知クラスで `broadcastType` メソッドを定義できます。

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
### 通知を聞く

通知は、`{notifiable}.{id}` 規則を使用してフォーマットされたプライベート チャネルでブロードキャストされます。したがって、`1` の ID を持つ `App\Models\User` インスタンスに通知を送信する場合、通知は `App.Models.User.1` プライベート チャネルでブロードキャストされます。 [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) を使用する場合、`notification` メソッドを使用してチャネル上の通知を簡単にリッスンできます。

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```

<a name="using-react-or-vue"></a>
#### React または Vue の使用

Laravel Echo には、通知を簡単にリッスンできるようにする React フックと Vue フックが含まれています。まず、通知をリッスンするために使用される `useEchoNotification` フックを呼び出します。 `useEchoNotification` フックは、使用側コンポーネントがアンマウントされると自動的にチャネルを離れます。

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

デフォルトでは、フックはすべての通知をリッスンします。リッスンする通知タイプを指定するには、タイプの文字列または配列を `useEchoNotification` に提供します。

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

通知ペイロード データの形式を指定して、タイプ セーフ性と編集の利便性を高めることもできます。

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
#### 通知チャネルのカスタマイズ

エンティティのブロードキャスト通知がどのチャネルでブロードキャストされるかをカスタマイズしたい場合は、通知可能なエンティティで `receivesBroadcastNotificationsOn` メソッドを定義できます。

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
## SMS通知 (SMS Notifications)

<a name="sms-prerequisites"></a>
### 前提条件

Laravel での SMS 通知の送信は、[Vonage](https://www.vonage.com/) (旧名 Nexmo) を利用しています。 Vonage 経由で通知を送信する前に、`laravel/vonage-notification-channel` および `guzzlehttp/guzzle` パッケージをインストールする必要があります。

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```

パッケージには [設定ファイル](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php) が含まれています。ただし、この構成ファイルを独自のアプリケーションにエクスポートする必要はありません。 `VONAGE_KEY` および `VONAGE_SECRET` 環境変数を使用するだけで、Vonage の公開キーと秘密キーを定義できます。

キーを定義した後、デフォルトで SMS メッセージの送信元となる電話番号を定義する `VONAGE_SMS_FROM` 環境変数を設定する必要があります。この電話番号は、Vonage コントロール パネル内で生成できます。

```ini
VONAGE_SMS_FROM=15556666666
```

<a name="formatting-sms-notifications"></a>
### SMS 通知のフォーマット

通知が SMS としての送信をサポートしている場合は、通知クラスで `toVonage` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Messages\VonageMessage` インスタンスを返す必要があります。

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
#### Unicode コンテンツ

SMS メッセージに Unicode 文字が含まれる場合は、`VonageMessage` インスタンスを構築するときに `unicode` メソッドを呼び出す必要があります。

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
### 「差出人」番号のカスタマイズ

`VONAGE_SMS_FROM` 環境変数で指定された電話番号とは異なる電話番号から通知を送信したい場合は、`VonageMessage` インスタンスで `from` メソッドを呼び出すことができます。

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
### クライアント参照の追加

ユーザー、チーム、またはクライアントごとのコストを追跡したい場合は、通知に「クライアント参照」を追加できます。 Vonage では、このクライアント リファレンスを使用してレポートを生成できるため、特定の顧客の SMS の使用状況をよりよく理解できます。クライアント参照には、最大 40 文字の任意の文字列を指定できます。

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
### SMS 通知のルーティング

Vonage 通知を適切な電話番号にルーティングするには、通知対象エンティティで `routeNotificationForVonage` メソッドを定義します。

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
## Slack 通知 (Slack Notifications)

<a name="slack-prerequisites"></a>
### 前提条件

Slack 通知を送信する前に、Composer 経由で Slack 通知チャネルをインストールする必要があります。

```shell
composer require laravel/slack-notification-channel
```

さらに、Slack ワークスペース用に [スラックアプリ](https://api.slack.com/apps?new_app=1) を作成する必要があります。

アプリが作成されているのと同じ Slack ワークスペースにのみ通知を送信する必要がある場合は、アプリに `chat:write`、`chat:write.public`、および `chat:write.customize` スコープがあることを確認する必要があります。これらのスコープは、Slack 内の「OAuth と権限」アプリ管理タブから追加できます。

次に、アプリの「ボット ユーザー OAuth トークン」をコピーし、アプリケーションの `services.php` 構成ファイルの `slack` 構成配列内に配置します。このトークンは、Slack 内の [OAuth & Permissions] タブにあります。

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```

<a name="slack-app-distribution"></a>
#### アプリの配布

アプリケーションが、アプリケーションのユーザーが所有する外部 Slack ワークスペースに通知を送信する場合は、Slack 経由でアプリケーションを「配布」する必要があります。アプリの配布は、Slack 内のアプリの「配布の管理」タブから管理できます。アプリが配布されたら、アプリケーションのユーザーに代わって [Socialite](/docs/{{version}}/socialite) から [Slack Botトークンを取得する](/docs/{{version}}/socialite#slack-bot-scopes) を使用できます。

<a name="formatting-slack-notifications"></a>
### Slack 通知の書式設定

通知が Slack メッセージとしての送信をサポートしている場合は、通知クラスで `toSlack` メソッドを定義する必要があります。このメソッドは `$notifiable` エンティティを受け取り、`Illuminate\Notifications\Slack\SlackMessage` インスタンスを返す必要があります。 [Slack のブロック キット API](https://api.slack.com/block-kit) を使用してリッチ通知を構築できます。次の例は、[Slack の Block Kit ビルダ](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D) でプレビューできます。

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
#### Slack の Block Kit Builder テンプレートの使用

Block Kit メッセージを構築するために流暢なメッセージ ビルダ メソッドを使用する代わりに、Slack の Block Kit Builder によって生成された生の JSON ペイロードを `usingBlockKitTemplate` メソッドに提供することもできます。

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
### Slack のインタラクティブ性

Slack の Block Kit 通知システムは、[ユーザーインタラクションを処理する](https://api.slack.com/interactivity/handling) に強力な機能を提供します。これらの機能を利用するには、Slack アプリで「インタラクティブ性」を有効にし、アプリケーションによって提供される URL を指すように「リクエスト URL」を構成する必要があります。これらの設定は、Slack 内の「インタラクティブ性とショートカット」アプリ管理タブから管理できます。

`actionsBlock` メソッドを利用する次の例では、Slack は、ボタンをクリックした Slack ユーザー、クリックされたボタンの ID などを含むペイロードを含む `POST` リクエストを「リクエスト URL」に送信します。その後、アプリケーションはペイロードに基づいて実行するアクションを決定できます。 [リクエストを確認する](https://api.slack.com/authentication/verifying-requests-from-slack) は Slack によって作成されたものであることも確認してください。

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
#### 確認モーダル

アクションを実行する前にユーザーに確認を要求したい場合は、ボタンを定義するときに `confirm` メソッドを呼び出すことができます。 `confirm` メソッドは、メッセージと、`ConfirmObject` インスタンスを受け取るクロージャを受け入れます。

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
#### スラックブロックの検査

構築しているブロックをすぐに検査したい場合は、`SlackMessage` インスタンスで `dd` メソッドを呼び出すことができます。 `dd` メソッドは、Slack の [ブロックキットビルダ](https://app.slack.com/block-kit-builder/) への URL を生成してダンプします。これにより、ブラウザーにペイロードと通知のプレビューが表示されます。 `true` を `dd` メソッドに渡して、生のペイロードをダンプできます。

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```

<a name="routing-slack-notifications"></a>
### Slack 通知のルーティング

Slack 通知を適切な Slack チームとチャネルに送信するには、通知可能なモデルで `routeNotificationForSlack` メソッドを定義します。このメソッドは、次の 3 つの値のいずれかを返します。

- `null` - 通知自体で構成されたチャネルへのルーティングを延期します。 `SlackMessage` を構築するときに `to` メソッドを使用して、通知内のチャネルを構成できます。
- 通知の送信先となる Slack チャネルを指定する文字列。 `#support-channel`。
- `SlackRoute` インスタンス。OAuth トークンとチャネル名を指定できます。 `SlackRoute::make($this->slack_channel, $this->slack_token)`。このメソッドは、外部ワークスペースに通知を送信するために使用する必要があります。

たとえば、`routeNotificationForSlack` メソッドから `#support-channel` を返すと、アプリケーションの `services.php` 構成ファイルにあるボット ユーザー OAuth トークンに関連付けられたワークスペースの `#support-channel` チャネルに通知が送信されます。

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
### 外部 Slack ワークスペースへの通知

> [!NOTE]
> 外部 Slack ワークスペースに通知を送信する前に、Slack アプリが [distributed](#slack-app-distribution) である必要があります。

もちろん、アプリケーションのユーザーが所有する Slack ワークスペースに通知を送信したい場合もよくあります。これを行うには、まずユーザーの Slack OAuth トークンを取得する必要があります。ありがたいことに、[Laravel Socialite](/docs/{{version}}/socialite) には、Slack と [ボットトークンを取得する](/docs/{{version}}/socialite#slack-bot-scopes) を使用してアプリケーションのユーザーを簡単に認証できるようにする Slack ドライバが含まれています。

ボット トークンを取得してアプリケーションのデータベース内に保存したら、`SlackRoute::make` メソッドを利用してユーザーのワークスペースに通知をルーティングできます。さらに、アプリケーションでは、どのチャネル通知を送信するかをユーザーに指定する機会を提供する必要がある可能性があります。

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
## 通知のローカライズ (Localizing Notifications)

Laravel では、HTTP リクエストの現在のロケール以外のロケールで通知を送信することができ、通知がキューに入れられている場合でもこのロケールを記憶します。

これを実現するために、`Illuminate\Notifications\Notification` クラスは、希望の言語を設定するための `locale` メソッドを提供します。アプリケーションは、通知の評価中にこのロケールに変更され、評価が完了すると前のロケールに戻ります。

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```

複数の通知可能なエントリのローカライズは、`Notification` ファサードを介して実現することもできます。

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```

<a name="user-preferred-locales"></a>
#### ユーザーの優先ロケール

場合によっては、アプリケーションが各ユーザーの優先ロケールを保存することがあります。通知可能モデルに `HasLocalePreference` コントラクトを実装することで、通知を送信するときにこの保存されたロケールを使用するように Laravel に指示できます。

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

インターフェースを実装すると、Laravel は通知とメール可能ファイルをモデルに送信するときに優先ロケールを自動的に使用します。したがって、このインターフェイスを使用する場合は、`locale` メソッドを呼び出す必要はありません。

```php
$user->notify(new InvoicePaid($invoice));
```

<a name="testing"></a>
## テスト (Testing)

`Notification` ファサードの `fake` メソッドを使用して、通知が送信されないようにすることができます。通常、通知の送信は、実際にテストしているコードとは無関係です。おそらく、Laravel が特定の通知を送信するように指示されたと主張するだけで十分です。

`Notification` ファサードの `fake` メソッドを呼び出した後、通知がユーザーに送信されるように指示されたことをアサートし、通知が受信したデータを検査することもできます。

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

特定の「真実テスト」に合格する通知が送信されたことをアサートするために、`assertSentTo` メソッドまたは `assertNotSentTo` メソッドにクロージャを渡すことができます。指定された真実テストに合格する少なくとも 1 つの通知が送信された場合、アサーションは成功します。

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### オンデマンド通知

テストしているコードが [オンデマンド通知](#on-demand-notifications) を送信する場合、オンデマンド通知が `assertSentOnDemand` メソッド経由で送信されたことをテストできます。

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` メソッドの 2 番目の引数としてクロージャーを渡すことで、オンデマンド通知が正しい「ルート」アドレスに送信されたかどうかを判断できます。

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="notification-events"></a>
## 通知イベント (Notification Events)

<a name="notification-sending-event"></a>
#### 通知送信イベント

通知の送信中に、通知システムによって `Illuminate\Notifications\Events\NotificationSending` イベントが送出されます。これには、「通知可能な」エンティティと通知インスタンス自体が含まれます。アプリケーション内でこのイベント用に [イベントリスナ](/docs/{{version}}/events) を作成できます。

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

`NotificationSending` イベントのイベント リスナが `handle` メソッドから `false` を返した場合、通知は送信されません。

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```

イベント リスナ内で、イベントの `notifiable`、`notification`、および `channel` プロパティにアクセスして、通知受信者または通知自体の詳細を確認できます。

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
#### 通知送信イベント

通知が送信されると、通知システムによって `Illuminate\Notifications\Events\NotificationSent` [event](/docs/{{version}}/events) がディスパッチされます。これには、「通知可能な」エンティティと通知インスタンス自体が含まれます。アプリケーション内でこのイベント用に [event](/docs/{{version}}/events) を作成できます。

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

イベント リスナ内で、イベントの `notifiable`、`notification`、`channel`、および `response` プロパティにアクセスして、通知受信者または通知自体の詳細を確認できます。

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
## カスタムチャンネル (Custom Channels)

Laravel にはいくつかの通知チャネルが付属していますが、他のチャネル経由で通知を配信する独自​​のドライバを作成することもできます。 Laravel を使えば簡単になります。まず、`send` メソッドを含むクラスを定義します。このメソッドは、`$notifiable` と `$notification` の 2 つの引数を受け取る必要があります。

`send` メソッド内で、通知のメソッドを呼び出して、チャネルによって理解されるメッセージ オブジェクトを取得し、通知を `$notifiable` インスタンスに送信することができます。

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

通知チャネル クラスを定義したら、任意の通知の `via` メソッドからクラス名を返すことができます。この例では、通知の `toVoice` メソッドは、音声メッセージを表すために選択したオブジェクトを返すことができます。たとえば、次のメッセージを表す独自の `VoiceMessage` クラスを定義できます。

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

