<!-- # Events -->
# Events

- [Introduction](#introduction)
- [Generating Events and Listeners](#generating-events-and-listeners)
- [Registering Events and Listeners](#registering-events-and-listeners)
    - [Event Discovery](#event-discovery)
    - [Manually Registering Events](#manually-registering-events)
    - [Closure Listeners](#closure-listeners)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
    - [Manually Interacting With the Queue](#manually-interacting-with-the-queue)
    - [Queued Event Listeners and Database Transactions](#queued-event-listeners-and-database-transactions)
    - [Queued Listener Middleware](#queued-listener-middleware)
    - [Encrypted Queued Listeners](#encrypted-queued-listeners)
    - [Unique Event Listeners](#unique-event-listeners)
        - [Keeping Listeners Unique Until Processing Begins](#keeping-listeners-unique-until-processing-begins)
        - [Unique Listener Locks](#unique-listener-locks)
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
    - [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)
    - [Deferring Events](#deferring-events)
- [Event Subscribers](#event-subscribers)
    - [Writing Event Subscribers](#writing-event-subscribers)
    - [Registering Event Subscribers](#registering-event-subscribers)
- [Testing](#testing)
    - [Faking a Subset of Events](#faking-a-subset-of-events)
    - [Scoped Events Fakes](#scoped-event-fakes)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands. -->
Laravel のイベントはシンプルなオブザーバ パターンの実装を提供し、アプリケーション内で発生するさまざまなイベントをサブスクライブしてリッスンできるようにします。通常、イベント クラスは `app/Events` ディレクトリに保存され、そのリスナは `app/Listeners` に保存されます。アプリケーションにこれらのディレクトリが表示されない場合でも、Artisan コンソール コマンドを使用してイベントとリスナを生成すると自動的に作成されるため、心配する必要はありません。

<!-- Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification. -->
イベントは、単一のイベントに相互に依存しない複数のリスナを持つことができるため、アプリケーションのさまざまな側面を分離する優れた方法として機能します。たとえば、注文が発送されるたびにユーザーに Slack 通知を送信したい場合があります。注文処理コードを Slack 通知コードに結合する代わりに、リスナが受信して Slack 通知をディスパッチするために使用できる `App\Events\OrderShipped` イベントを発生させることができます。

<a name="generating-events-and-listeners"></a>
<!-- ## Generating Events and Listeners -->
## Generating Events and Listeners

<!-- To quickly generate events and listeners, you may use the `make:event` and `make:listener` Artisan commands: -->
イベントとリスナを迅速に生成するには、`make:event` および `make:listener` Artisan コマンドを使用できます。

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<!-- For convenience, you may also invoke the `make:event` and `make:listener` Artisan commands without additional arguments. When you do so, Laravel will automatically prompt you for the class name and, when creating a listener, the event it should listen to: -->
便宜上、追加の引数なしで `make:event` および `make:listener` Artisan コマンドを呼び出すこともできます。これを行うと、Laravel はクラス名と、リスナの作成時にリッスンするイベントの入力を自動的に求めます。

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
<!-- ## Registering Events and Listeners -->
## Registering Events and Listeners

<a name="event-discovery"></a>
<!-- ### Event Discovery -->
### Event Discovery

<!-- By default, Laravel will automatically find and register your event listeners by scanning your application's `Listeners` directory. When Laravel finds any listener class method that begins with `handle` or `__invoke`, Laravel will register those methods as event listeners for the event that is type-hinted in the method's signature: -->
デフォルトでは、Laravel はアプリケーションの `Listeners` ディレクトリをスキャンすることにより、イベントリスナを自動的に検索して登録します。 Laravel が `handle` または `__invoke` で始まるリスナ クラス メソッドを見つけると、Laravel はそれらのメソッドを、メソッドのシグネチャでタイプヒントされているイベントのイベント リスナとして登録します。

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

<!-- You may listen to multiple events using PHP's union types: -->
PHP の共用体タイプを使用して複数のイベントをリッスンすることができます。

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

<!-- If you plan to store your listeners in a different directory or within multiple directories, you may instruct Laravel to scan those directories using the `withEvents` method in your application's `bootstrap/app.php` file: -->
リスナを別のディレクトリまたは複数のディレクトリ内に保存する予定がある場合は、アプリケーションの `bootstrap/app.php` ファイル内の `withEvents` メソッドを使用して、これらのディレクトリをスキャンするように Laravel に指示できます。

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

<!-- You may scan for listeners in multiple similar directories using the `*` character as a wildcard: -->
`*` 文字をワイルドカードとして使用して、複数の同様のディレクトリでリスナをスキャンできます。

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

<!-- The `event:list` command may be used to list all of the listeners registered within your application: -->
`event:list` コマンドを使用すると、アプリケーション内に登録されているすべてのリスナを一覧表示できます。

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
<!-- #### Event Discovery in Production -->
#### Event Discovery in Production

<!-- To give your application a speed boost, you should cache a manifest of all of your application's listeners using the `optimize` or `event:cache` Artisan commands. Typically, this command should be run as part of your application's [deployment process](/docs/13.x/deployment#optimization). This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the event cache. -->
アプリケーションの速度を向上させるには、`optimize` または `event:cache` Artisan コマンドを使用して、アプリケーションのすべてのリスナのマニフェストをキャッシュする必要があります。通常、このコマンドはアプリケーションの [deployment process](/docs/13.x/deployment#optimization) の一部として実行する必要があります。このマニフェストは、イベント登録プロセスを高速化するためにフレームワークによって使用されます。 `event:clear` コマンドを使用してイベント キャッシュを破棄することができます。

<a name="dynamic-event-discovery"></a>
<!-- #### Dynamic Event Discovery -->
#### Dynamic Event Discovery

<!-- To dynamically control whether a given listener is discovered, you may implement the `ShouldBeDiscovered` interface on the listener class and define a `shouldBeDiscovered` method that returns a boolean value. If the method returns `false`, the listener will not be registered during event discovery: -->
特定のリスナを検出するかどうかを動的に制御するには、リスナクラスに `ShouldBeDiscovered` インターフェースを実装し、真偽値を返す `shouldBeDiscovered` メソッドを定義します。このメソッドが `false` を返すと、そのリスナはイベント検出時に登録されません。

```php
use Illuminate\Contracts\Events\ShouldBeDiscovered;

class SendPodcastNotification implements ShouldBeDiscovered
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }

    /**
     * Determine if the listener should be discovered.
     */
    public static function shouldBeDiscovered(): bool
    {
        return app()->environment('production');
    }
}
```

<a name="manually-registering-events"></a>
<!-- ### Manually Registering Events -->
### Manually Registering Events

<!-- Using the `Event` facade, you may manually register events and their corresponding listeners within the `boot` method of your application's `AppServiceProvider`: -->
`Event` ファサードを使用すると、アプリケーションの `AppServiceProvider` の `boot` メソッド内でイベントとそれに対応するリスナを手動で登録できます。

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

<!-- The `event:list` command may be used to list all of the listeners registered within your application: -->
`event:list` コマンドを使用すると、アプリケーション内に登録されているすべてのリスナを一覧表示できます。

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
<!-- ### Closure Listeners -->
### Closure Listeners

<!-- Typically, listeners are defined as classes; however, you may also manually register closure-based event listeners in the `boot` method of your application's `AppServiceProvider`: -->
通常、リスナはクラスとして定義されます。ただし、アプリケーションの `AppServiceProvider` の `boot` メソッドでクロージャ ベースのイベント リスナを手動で登録することもできます。

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

<a name="queueable-anonymous-event-listeners"></a>
<!-- #### Queueable Anonymous Event Listeners -->
#### Queueable Anonymous Event Listeners

<!-- When registering closure-based event listeners, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/13.x/queues): -->
クロージャベースのイベントリスナを登録する場合、`Illuminate\Events\queueable` 関数内でリスナクロージャをラップして、[queue](/docs/13.x/queues) を使用してリスナを実行するように Laravel に指示できます。

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

<!-- Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener: -->
キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure: -->
匿名のキューに入れられたリスナの失敗を処理したい場合は、`queueable` リスナを定義するときに、`catch` メソッドにクロージャを提供できます。このクロージャは、リスナの失敗の原因となったイベント インスタンスと `Throwable` インスタンスを受け取ります。

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
<!-- #### Wildcard Event Listeners -->
#### Wildcard Event Listeners

<!-- You may also register listeners using the `*` character as a wildcard parameter, allowing you to catch multiple events on the same listener. Wildcard listeners receive the event name as their first argument and the entire event data array as their second argument: -->
また、ワイルドカード パラメーターとして `*` 文字を使用してリスナを登録し、同じリスナで複数のイベントをキャッチできるようにすることもできます。ワイルドカード リスナは、最初の引数としてイベント名を受け取り、2 番目の引数としてイベント データ配列全体を受け取ります。

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
<!-- ## Defining Events -->
## Defining Events

<!-- An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/13.x/eloquent) object: -->
イベント クラスは本質的に、イベントに関連する情報を保持するデータ コンテナーです。たとえば、`App\Events\OrderShipped` イベントが [Eloquent ORM](/docs/13.x/eloquent) オブジェクトを受信すると仮定します。

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

<!-- As you can see, this event class contains no logic. It is a container for the `App\Models\Order` instance that was purchased. The `SerializesModels` trait used by the event will gracefully serialize any Eloquent models if the event object is serialized using PHP's `serialize` function, such as when utilizing [queued listeners](#queued-event-listeners). -->
ご覧のとおり、このイベント クラスにはロジックが含まれていません。購入した `App\Models\Order` インスタンスのコンテナーです。イベントで使用される `SerializesModels` トレイトは、イベント オブジェクトが PHP の `serialize` 関数を使用してシリアル化されている場合 ([queued listeners](#queued-event-listeners) を利用している場合など)、Eloquent モデルを適切にシリアル化します。

<a name="defining-listeners"></a>
<!-- ## Defining Listeners -->
## Defining Listeners

<!-- Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `make:listener` Artisan command, when invoked with the `--event` option, will automatically import the proper event class and type-hint the event in the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event: -->
次に、サンプル イベントのリスナを見てみましょう。イベント リスナは、`handle` メソッドでイベント インスタンスを受け取ります。 `make:listener` Artisan コマンドは、`--event` オプションを指定して呼び出すと、適切なイベント クラスを自動的にインポートし、`handle` メソッドでイベントをタイプヒントします。 `handle` メソッド内で、イベントに応答するために必要なアクションを実行できます。

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
> イベント リスナは、コンストラクターに必要な依存関係をタイプヒントで示すこともできます。すべてのイベント リスナは Laravel [service container](/docs/13.x/container) 経由で解決されるため、依存関係は自動的に挿入されます。

<a name="stopping-the-propagation-of-an-event"></a>
<!-- #### Stopping The Propagation Of An Event -->
#### Stopping The Propagation Of An Event

<!-- Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method. -->
場合によっては、他のリスナへのイベントの伝播を停止したい場合があります。これを行うには、リスナの `handle` メソッドから `false` を返します。

<a name="queued-event-listeners"></a>
<!-- ## Queued Event Listeners -->
## Queued Event Listeners

<!-- Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/13.x/queues) and start a queue worker on your server or local development environment. -->
リスナのキューイングは、リスナが電子メールの送信や HTTP リクエストの作成などの遅いタスクを実行する場合に有益です。キュー リスナを使用する前に、必ず [configure your queue](/docs/13.x/queues) を実行し、サーバーまたはローカル開発環境でキューワーカーを起動してください。

<!-- To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately: -->
リスナをキューに入れるように指定するには、`ShouldQueue` インターフェイスをリスナ クラスに追加します。 `make:listener` Artisan コマンドによって生成されたリスナには、このインターフェイスがすでに現在の名前空間にインポートされているため、すぐに使用できます。

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

<!-- That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/13.x/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing. -->
それでおしまい！このリスナによって処理されるイベントがディスパッチされると、リスナは Laravel の [queue system](/docs/13.x/queues) を使用するイベント ディスパッチャーによって自動的にキューに入れられます。リスナがキューによって実行されたときに例外がスローされなかった場合、キューに入れられたジョブは処理終了後に自動的に削除されます。

<a name="customizing-the-queue-connection-queue-name"></a>
<!-- #### Customizing The Queue Connection, Name, & Delay -->
#### Customizing The Queue Connection, Name, & Delay

<!-- If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may use the `Connection`, `Queue`, and `Delay` attributes on your listener class: -->
イベント リスナのキュー接続、キュー名、またはキュー遅延時間をカスタマイズしたい場合は、リスナ クラスで `Connection`、`Queue`、および `Delay` 属性を使用できます。

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
<!-- If you would like to define the listener's queue connection, queue name, or delay at runtime, you may define `viaConnection`, `viaQueue`, or `withDelay` methods on the listener: -->
リスナのキュー接続、キュー名、または実行時の遅延を定義したい場合は、リスナで `viaConnection`、`viaQueue`、または `withDelay` メソッドを定義できます。

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
<!-- #### Conditionally Queueing Listeners -->
#### Conditionally Queueing Listeners

<!-- Sometimes, you may need to determine whether a listener should be queued based on some data that are only available at runtime. To accomplish this, a `shouldQueue` method may be added to a listener to determine whether the listener should be queued. If the `shouldQueue` method returns `false`, the listener will not be queued: -->
場合によっては、実行時にのみ使用できるデータに基づいて、リスナをキューに入れる必要があるかどうかを決定する必要がある場合があります。これを実現するには、`shouldQueue` メソッドをリスナに追加して、リスナをキューに入れる必要があるかどうかを決定できます。 `shouldQueue` メソッドが `false` を返す場合、リスナはキューに入れられません。

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
<!-- ### Manually Interacting With the Queue -->
### Manually Interacting With the Queue

<!-- If you need to manually access the listener's underlying queue job's `delete` and `release` methods, you may do so using the `Illuminate\Queue\InteractsWithQueue` trait. This trait is imported by default on generated listeners and provides access to these methods: -->
リスナの基になるキュー ジョブの `delete` および `release` メソッドに手動でアクセスする必要がある場合は、`Illuminate\Queue\InteractsWithQueue` 特性を使用してアクセスできます。この特性は、生成されたリスナにデフォルトでインポートされ、次のメソッドへのアクセスを提供します。

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
<!-- ### Queued Event Listeners and Database Transactions -->
### Queued Event Listeners and Database Transactions

<!-- When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed. -->
キューに入れられたリスナがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。リスナがこれらのモデルに依存している場合、キューに入れられたリスナをディスパッチするジョブの処理時に予期しないエラーが発生する可能性があります。

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by implementing the `ShouldQueueAfterCommit` interface on the listener class: -->
キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、リスナ クラスに `ShouldQueueAfterCommit` インターフェイスを実装することで、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられたリスナをディスパッチする必要があることを示すことができます。

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
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/13.x/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="queued-listener-middleware"></a>
<!-- ### Queued Listener Middleware -->
### Queued Listener Middleware

<!-- Queued listeners can also utilize [job middleware](/docs/13.x/queues#job-middleware). Job middleware allow you to wrap custom logic around the execution of queued listeners, reducing boilerplate in the listeners themselves. After creating job middleware, they may be attached to a listener by returning them from the listener's `middleware` method: -->
キューに登録されたリスナは、[job middleware](/docs/13.x/queues#job-middleware) を利用することもできます。ジョブ ミドルウェアを使用すると、キューに入れられたリスナの実行にカスタム ロジックをラップして、リスナ自体の定型文を減らすことができます。ジョブ ミドルウェアを作成した後、リスナの `middleware` メソッドからジョブ ミドルウェアを返すことによって、ジョブ ミドルウェアをリスナにアタッチできます。

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
<!-- #### Encrypted Queued Listeners -->
#### Encrypted Queued Listeners

<!-- Laravel allows you to ensure the privacy and integrity of a queued listener's data via [encryption](/docs/13.x/encryption). To get started, simply add the `ShouldBeEncrypted` interface to the listener class. Once this interface has been added to the class, Laravel will automatically encrypt your listener before pushing it onto a queue: -->
Laravel を使用すると、[encryption](/docs/13.x/encryption) 経由でキューに入れられたリスナのデータのプライバシーと整合性を確保できます。まず、`ShouldBeEncrypted` インターフェイスをリスナ クラスに追加するだけです。このインターフェースがクラスに追加されると、Laravel はリスナをキューにプッシュする前に自動的に暗号化します。

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
<!-- ### Unique Event Listeners -->
### Unique Event Listeners

> [!WARNING]
> 固有のリスナには、[locks](/docs/13.x/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。

<!-- Sometimes, you may want to ensure that only one instance of a specific listener is on the queue at any point in time. You may do so by implementing the `ShouldBeUnique` interface on your listener class: -->
場合によっては、特定のリスナのインスタンスが常に 1 つだけキューに存在するようにしたい場合があります。これを行うには、リスナ クラスに `ShouldBeUnique` インターフェイスを実装します。

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

<!-- In the example above, the `AcquireProductKey` listener is unique. So, the listener will not be queued if another instance of the listener is already on the queue and has not finished processing. This ensures that only one product key is acquired for each license, even if the license is saved multiple times in quick succession. -->
上の例では、`AcquireProductKey` リスナは一意です。したがって、リスナの別のインスタンスがすでにキュー上にあり、処理が完了していない場合、リスナはキューに入れられません。これにより、ライセンスが立て続けに複数回保存された場合でも、ライセンスごとにプロダクト キーが 1 つだけ取得されるようになります。

<!-- In certain cases, you may want to define a specific "key" that makes the listener unique or you may want to specify a timeout beyond which the listener no longer stays unique. To accomplish this, you may define `uniqueId` and `uniqueFor` properties or methods on your listener class. The methods receive the event instance, allowing you to use event data to construct the return value: -->
場合によっては、リスナを一意にする特定の「キー」を定義したり、リスナが一意でなくなるタイムアウトを指定したりすることができます。これを実現するには、リスナ クラスで `uniqueId` および `uniqueFor` プロパティまたはメソッドを定義できます。メソッドはイベント インスタンスを受け取り、イベント データを使用して戻り値を構築できるようになります。

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

<!-- In the example above, the `AcquireProductKey` listener is unique by license ID. So, any new dispatches of the listener for the same license will be ignored until the existing listener has completed processing. This prevents duplicate product keys from being acquired for the same license. In addition, if the existing listener is not processed within one hour, the unique lock will be released and another listener with the same unique key can be queued. -->
上の例では、`AcquireProductKey` リスナはライセンス ID によって一意です。したがって、同じライセンスに対するリスナの新しいディスパッチは、既存のリスナが処理を完了するまで無視されます。これにより、同じライセンスに対して重複したプロダクト キーが取得されるのを防ぎます。さらに、既存のリスナが 1 時間以内に処理されない場合、一意のロックが解放され、同じ一意のキーを持つ別のリスナがキューに追加される可能性があります。

> [!WARNING]
> アプリケーションが複数のWebサーバーまたはコンテナからイベントをディスパッチする場合は、Laravelがリスナが一意であるかどうかを正確に判断できるように、すべてのサーバーが同じ中央キャッシュサーバーと通信していることを確認する必要があります。

<a name="keeping-listeners-unique-until-processing-begins"></a>
<!-- #### Keeping Listeners Unique Until Processing Begins -->
#### Keeping Listeners Unique Until Processing Begins

<!-- By default, unique listeners are "unlocked" after a listener completes processing or fails all of its retry attempts. However, there may be situations where you would like your listener to unlock immediately before it is processed. To accomplish this, your listener should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract: -->
デフォルトでは、リスナが処理を完了するか、すべての再試行に失敗すると、一意のリスナは「ロック解除」されます。ただし、処理される直前にリスナのロックを解除したい場合もあります。これを実現するには、リスナは `ShouldBeUnique` コントラクトの代わりに `ShouldBeUniqueUntilProcessing` コントラクトを実装する必要があります。

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
<!-- #### Unique Listener Locks -->
#### Unique Listener Locks

<!-- Behind the scenes, when a `ShouldBeUnique` listener is dispatched, Laravel attempts to acquire a [lock](/docs/13.x/cache#atomic-locks) with the `uniqueId` key. If the lock is already held, the listener is not dispatched. This lock is released when the listener completes processing or fails all of its retry attempts. By default, Laravel will use the default cache driver to obtain this lock. However, if you wish to use another driver for acquiring the lock, you may define a `uniqueVia` method that returns the cache driver that should be used: -->
バックグラウンドでは、`ShouldBeUnique` リスナがディスパッチされると、Laravel は `uniqueId` キーを使用して [lock](/docs/13.x/cache#atomic-locks) を取得しようとします。ロックがすでに保持されている場合、リスナはディスパッチされません。このロックは、リスナが処理を完了するか、すべての再試行に失敗すると解放されます。デフォルトでは、Laravel はデフォルトのキャッシュドライバを使用してこのロックを取得します。ただし、ロックの取得に別のドライバを使用したい場合は、使用するキャッシュ ドライバを返す `uniqueVia` メソッドを定義できます。

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
> リスナの同時処理を制限する必要があるだけの場合は、代わりに [WithoutOverlapping](/docs/13.x/queues#preventing-job-overlaps) ジョブ ミドルウェアを使用してください。

<a name="handling-failed-jobs"></a>
<!-- ### Handling Failed Jobs -->
### Handling Failed Jobs

<!-- Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure: -->
場合によっては、キューに入れられたイベント リスナが失敗することがあります。キューに入れられたリスナがキューワーカーによって定義された最大試行回数を超えると、`failed` メソッドがリスナで呼び出されます。 `failed` メソッドは、イベント インスタンスと失敗の原因となった `Throwable` を受け取ります。

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
<!-- #### Specifying Queued Listener Maximum Attempts -->
#### Specifying Queued Listener Maximum Attempts

<!-- If one of your queued listeners is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a listener may be attempted. -->
キューに入れられたリスナの 1 つでエラーが発生した場合、そのリスナが無制限に再試行を続けることは望ましくありません。したがって、Laravel では、リスナの試行回数または試行時間を指定するさまざまな方法が提供されています。

<!-- You may use the `Tries` attribute on your listener class to specify how many times the listener may be attempted before it is considered to have failed: -->
リスナ クラスの `Tries` 属性を使用して、リスナが失敗したとみなされるまでの試行回数を指定できます。

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

<!-- As an alternative to defining how many times a listener may be attempted before it fails, you may define a time at which the listener should no longer be attempted. This allows a listener to be attempted any number of times within a given time frame. To define the time at which a listener should no longer be attempted, add a `retryUntil` method to your listener class. This method should return a `DateTimeInterface` instance: -->
失敗するまでにリスナを何回試行できるかを定義する代わりに、リスナを試行しなくなる時間を定義することもできます。これにより、リスナは指定された時間枠内で何度でも試行できます。リスナを試行しなくなる時間を定義するには、`retryUntil` メソッドをリスナ クラスに追加します。このメソッドは `DateTimeInterface` インスタンスを返す必要があります。

```php
use DateTimeInterface;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTimeInterface
{
    return now()->plus(minutes: 5);
}
```

<!-- If both `retryUntil` and `tries` are defined, Laravel gives precedence to the `retryUntil` method. -->
`retryUntil` と `tries` の両方が定義されている場合、Laravel は `retryUntil` メソッドを優先します。

<a name="specifying-queued-listener-backoff"></a>
<!-- #### Specifying Queued Listener Backoff -->
#### Specifying Queued Listener Backoff

<!-- If you would like to configure how many seconds Laravel should wait before retrying a listener that has encountered an exception, you may use the `Backoff` attribute on your listener class: -->
例外が発生したリスナを再試行する前に Laravel が待機する秒数を設定したい場合は、リスナ クラスで `Backoff` 属性を使用できます。

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

<!-- If you require more complex logic for determining the listeners's backoff time, you may define a `backoff` method on your listener class: -->
リスナのバックオフ時間を決定するためにより複雑なロジックが必要な場合は、リスナ クラスで `backoff` メソッドを定義できます。

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

<!-- You may easily configure "exponential" backoffs by returning an array of backoff values from the `backoff` method. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
`backoff` メソッドからバックオフ値の配列を返すことで、「指数関数的」バックオフを簡単に構成できます。この例では、再試行の遅​​延は、最初の再試行では 1 秒、2 回目の再試行では 5 秒、3 回目の再試行では 10 秒、さらに試行が残っている場合はその後の再試行ごとに 10 秒になります。

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
<!-- #### Specifying Queued Listener Max Exceptions -->
#### Specifying Queued Listener Max Exceptions

<!-- Sometimes you may wish to specify that a queued listener may be attempted many times, but should fail if the retries are triggered by a given number of unhandled exceptions (as opposed to being released by the `release` method directly). To accomplish this, you may use the `Tries` and `MaxExceptions` attributes on your listener class: -->
場合によっては、キューに入れられたリスナを何度も試行できるが、(`release` メソッドによって直接解放されるのではなく) 指定された数の未処理の例外によって再試行がトリガーされた場合は失敗するように指定したい場合があります。これを実現するには、リスナ クラスで `Tries` 属性と `MaxExceptions` 属性を使用します。

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

<!-- In this example, the listener will be retried up to 25 times. However, the listener will fail if three unhandled exceptions are thrown by the listener. -->
この例では、リスナは最大 25 回再試行されます。ただし、リスナによって 3 つの未処理の例外がスローされた場合、リスナは失敗します。

<a name="specifying-queued-listener-timeout"></a>
<!-- #### Specifying Queued Listener Timeout -->
#### Specifying Queued Listener Timeout

<!-- Often, you know roughly how long you expect your queued listeners to take. For this reason, Laravel allows you to specify a "timeout" value. If a listener is processing for longer than the number of seconds specified by the timeout value, the worker processing the listener will exit with an error. You may define the maximum number of seconds a listener should be allowed to run by using the `Timeout` attribute on your listener class: -->
多くの場合、キューに入れられたリスナにかかる時間がおおよそわかっています。このため、Laravel では「タイムアウト」値を指定できます。リスナがタイムアウト値で指定された秒数を超えて処理している場合、リスナを処理しているワーカーはエラーで終了します。リスナ クラスの `Timeout` 属性を使用して、リスナの実行を許可する最大秒数を定義できます。

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

<!-- If you would like to indicate that a listener should be marked as failed on timeout, you may use the `FailOnTimeout` attribute on the listener class: -->
リスナをタイムアウト時に失敗としてマークする必要があることを示したい場合は、リスナ クラスで `FailOnTimeout` 属性を使用できます。

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
<!-- ## Dispatching Events -->
## Dispatching Events

<!-- To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor: -->
イベントをディスパッチするには、イベントで静的 `dispatch` メソッドを呼び出すことができます。このメソッドは、`Illuminate\Foundation\Events\Dispatchable` トレイトによってイベントで使用できるようになります。 `dispatch` メソッドに渡される引数はすべて、イベントのコンストラクターに渡されます。

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

<!-- If you would like to conditionally dispatch an event, you may use the `dispatchIf` and `dispatchUnless` methods: -->
条件付きでイベントをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> テストする場合、特定のイベントが実際にリスナをトリガーせずにディスパッチされたことをアサートすると役立つ場合があります。 Laravel の [built-in testing helpers](#testing) を使えば簡単です。

<a name="dispatching-events-after-database-transactions"></a>
<!-- ### Dispatching Events After Database Transactions -->
### Dispatching Events After Database Transactions

<!-- Sometimes, you may want to instruct Laravel to only dispatch an event after the active database transaction has committed. To do so, you may implement the `ShouldDispatchAfterCommit` interface on the event class. -->
場合によっては、アクティブなデータベーストランザクションがコミットされた後にのみイベントをディスパッチするようにLaravelに指示したい場合があります。これを行うには、イベント クラスに `ShouldDispatchAfterCommit` インターフェイスを実装します。

<!-- This interface instructs Laravel to not dispatch the event until the current database transaction is committed. If the transaction fails, the event will be discarded. If no database transaction is in progress when the event is dispatched, the event will be dispatched immediately: -->
このインターフェイスは、現在のデータベーストランザクションがコミットされるまでイベントをディスパッチしないようにLaravelに指示します。トランザクションが失敗した場合、イベントは破棄されます。イベントが送出されるときにデータベース トランザクションが進行中でない場合、イベントはすぐに送出されます。

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
<!-- ### Deferring Events -->
### Deferring Events

<!-- Deferred events allow you to delay the dispatching of model events and execution of event listeners until after a specific block of code has completed. This is particularly useful when you need to ensure that all related records are created before event listeners are triggered. -->
遅延イベントを使用すると、コードの特定のブロックが完了するまで、モデル イベントのディスパッチとイベント リスナの実行を遅らせることができます。これは、イベント リスナがトリガーされる前に、関連するすべてのレコードが確実に作成されるようにする必要がある場合に特に便利です。

<!-- To defer events, provide a closure to the `Event::defer()` method: -->
イベントを延期するには、`Event::defer()` メソッドにクロージャーを提供します。

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

<!-- All events triggered within the closure will be dispatched after the closure is executed. This ensures that event listeners have access to all related records that were created during the deferred execution. If an exception occurs within the closure, the deferred events will not be dispatched. -->
クロージャ内でトリガーされたすべてのイベントは、クロージャの実行後にディスパッチされます。これにより、イベント リスナは遅延実行中に作成されたすべての関連レコードにアクセスできるようになります。クロージャー内で例外が発生した場合、遅延イベントはディスパッチされません。

<!-- To defer only specific events, pass an array of events as the second argument to the `defer` method: -->
特定のイベントのみを延期するには、イベントの配列を 2 番目の引数として `defer` メソッドに渡します。

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
<!-- ## Event Subscribers -->
## Event Subscribers

<a name="writing-event-subscribers"></a>
<!-- ### Writing Event Subscribers -->
### Writing Event Subscribers

<!-- Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which receives an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners: -->
イベント サブスクライバは、サブスクライバ クラス自体内から複数のイベントをサブスクライブできるクラスであり、単一クラス内で複数のイベント ハンドラを定義できます。サブスクライバは、イベント ディスパッチャー インスタンスを受け取る `subscribe` メソッドを定義する必要があります。指定されたディスパッチャーで `listen` メソッドを呼び出して、イベント リスナを登録できます。

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

<!-- If your event listener methods are defined within the subscriber itself, you may find it more convenient to return an array of events and method names from the subscriber's `subscribe` method. Laravel will automatically determine the subscriber's class name when registering the event listeners: -->
イベント リスナ メソッドがサブスクライバ自体内で定義されている場合は、サブスクライバの `subscribe` メソッドからイベントとメソッド名の配列を返す方が便利な場合があります。 Laravel は、イベントリスナを登録するときにサブスクライバのクラス名を自動的に決定します。

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
<!-- ### Registering Event Subscribers -->
### Registering Event Subscribers

<!-- After writing the subscriber, Laravel will automatically register handler methods within the subscriber if they follow Laravel's [event discovery conventions](#event-discovery). Otherwise, you may manually register your subscriber using the `subscribe` method of the `Event` facade. Typically, this should be done within the `boot` method of your application's `AppServiceProvider`: -->
サブスクライバを作成した後、Laravel の [event discovery conventions](#event-discovery) に従っている場合、Laravel はサブスクライバ内にハンドラー メソッドを自動的に登録します。それ以外の場合は、`Event` ファサードの `subscribe` メソッドを使用してサブスクライバを手動で登録できます。通常、これはアプリケーションの `AppServiceProvider` の `boot` メソッド内で行う必要があります。

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
<!-- ## Testing -->
## Testing

<!-- When testing code that dispatches events, you may wish to instruct Laravel to not actually execute the event's listeners, since the listener's code can be tested directly and separately of the code that dispatches the corresponding event. Of course, to test the listener itself, you may instantiate a listener instance and invoke the `handle` method directly in your test. -->
イベントを送出するコードをテストする場合、リスナのコードは、対応するイベントを送出するコードとは別に直接テストできるため、イベントのリスナを実際に実行しないように Laravel に指示することもできます。もちろん、リスナ自体をテストするには、リスナ インスタンスをインスタンス化し、テスト内で `handle` メソッドを直接呼び出します。

<!-- Using the `Event` facade's `fake` method, you may prevent listeners from executing, execute the code under test, and then assert which events were dispatched by your application using the `assertDispatched`, `assertNotDispatched`, and `assertNothingDispatched` methods: -->
`Event` ファサードの `fake` メソッドを使用すると、リスナの実行を防止し、テスト対象のコードを実行してから、`assertDispatched`、`assertNotDispatched`、および `assertNothingDispatched` メソッドを使用してアプリケーションによってどのイベントがディスパッチされたかをアサートできます。

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

<!-- You may pass a closure to the `assertDispatched` or `assertNotDispatched` methods in order to assert that an event was dispatched that passes a given "truth test". If at least one event was dispatched that passes the given truth test then the assertion will be successful: -->
特定の「真実テスト」に合格するイベントがディスパッチされたことをアサートするために、`assertDispatched` メソッドまたは `assertNotDispatched` メソッドにクロージャーを渡すことができます。指定された真実テストに合格する少なくとも 1 つのイベントがディスパッチされた場合、アサーションは成功します。

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

<!-- If you would simply like to assert that an event listener is listening to a given event, you may use the `assertListening` method: -->
イベント リスナが特定のイベントをリッスンしていることを単にアサートしたい場合は、`assertListening` メソッドを使用できます。

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()` を呼び出した後は、イベント リスナは実行されません。したがって、モデルの `creating` イベント中に UUID を作成するなど、イベントに依存するモデル ファクトリをテストで使用する場合は、ファクトリを使用した **後** で `Event::fake()` を呼び出す必要があります。

<a name="faking-a-subset-of-events"></a>
<!-- ### Faking a Subset of Events -->
### Faking a Subset of Events

<!-- If you only want to fake event listeners for a specific set of events, you may pass them to the `fake` or `fakeFor` method: -->
特定のイベント セットに対してのみイベント リスナを偽装したい場合は、それらを `fake` メソッドまたは `fakeFor` メソッドに渡すことができます。

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

<!-- You may fake all events except for a set of specified events using the `except` method: -->
`except` メソッドを使用すると、指定されたイベントのセットを除くすべてのイベントを偽装できます。

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
<!-- ### Scoped Event Fakes -->
### Scoped Event Fakes

<!-- If you only want to fake event listeners for a portion of your test, you may use the `fakeFor` method: -->
テストの一部に対してのみイベント リスナを偽装したい場合は、`fakeFor` メソッドを使用できます。

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

