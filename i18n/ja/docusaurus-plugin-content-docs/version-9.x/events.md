<!-- # Events -->
# Events

- [Introduction](#introduction)
- [Registering Events & Listeners](#registering-events-and-listeners)
    - [Generating Events & Listeners](#generating-events-and-listeners)
    - [Manually Registering Events](#manually-registering-events)
    - [Event Discovery](#event-discovery)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
    - [Manually Interacting With The Queue](#manually-interacting-with-the-queue)
    - [Queued Event Listeners & Database Transactions](#queued-event-listeners-and-database-transactions)
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
- [Event Subscribers](#event-subscribers)
    - [Writing Event Subscribers](#writing-event-subscribers)
    - [Registering Event Subscribers](#registering-event-subscribers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands. -->
Laravel のイベントはシンプルなオブザーバ パターンの実装を提供し、アプリケーション内で発生するさまざまなイベントをサブスクライブしてリッスンできるようにします。通常、イベント クラスは `app/Events` ディレクトリに保存され、そのリスナは `app/Listeners` に保存されます。アプリケーションにこれらのディレクトリが表示されない場合でも、Artisan コンソール コマンドを使用してイベントとリスナを生成すると自動的に作成されるため、心配する必要はありません。

<!-- Events serve as a great way to decouple various aspects of your application, since a single event can have multiple listeners that do not depend on each other. For example, you may wish to send a Slack notification to your user each time an order has shipped. Instead of coupling your order processing code to your Slack notification code, you can raise an `App\Events\OrderShipped` event which a listener can receive and use to dispatch a Slack notification. -->
イベントは、単一のイベントに相互に依存しない複数のリスナを持つことができるため、アプリケーションのさまざまな側面を分離する優れた方法として機能します。たとえば、注文が発送されるたびにユーザーに Slack 通知を送信したい場合があります。注文処理コードを Slack 通知コードに結合する代わりに、リスナが受信して Slack 通知をディスパッチするために使用できる `App\Events\OrderShipped` イベントを発生させることができます。

<a name="registering-events-and-listeners"></a>
<!-- ## Registering Events & Listeners -->
## Registering Events & Listeners

<!-- The `App\Providers\EventServiceProvider` included with your Laravel application provides a convenient place to register all of your application's event listeners. The `listen` property contains an array of all events (keys) and their listeners (values). You may add as many events to this array as your application requires. For example, let's add an `OrderShipped` event: -->
Laravel アプリケーションに含まれる `App\Providers\EventServiceProvider` は、アプリケーションのすべてのイベント リスナを登録する便利な場所を提供します。 `listen` プロパティには、すべてのイベント (キー) とそのリスナ (値) の配列が含まれます。アプリケーションが必要とするだけの数のイベントをこの配列に追加できます。たとえば、`OrderShipped` イベントを追加してみましょう。

```
use App\Events\OrderShipped;
use App\Listeners\SendShipmentNotification;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    OrderShipped::class => [
        SendShipmentNotification::class,
    ],
];
```

> [!NOTE]
> `event:list` コマンドを使用すると、アプリケーションによって登録されたすべてのイベントとリスナのリストを表示できます。

<a name="generating-events-and-listeners"></a>
<!-- ### Generating Events & Listeners -->
### Generating Events & Listeners

<!-- Of course, manually creating the files for each event and listener is cumbersome. Instead, add listeners and events to your `EventServiceProvider` and use the `event:generate` Artisan command. This command will generate any events or listeners that are listed in your `EventServiceProvider` that do not already exist: -->
もちろん、イベントやリスナごとに手動でファイルを作成するのは面倒です。代わりに、`EventServiceProvider` にリスナとイベントを追加し、`event:generate` Artisan コマンドを使用します。このコマンドは、`EventServiceProvider` にリストされているまだ存在しないイベントまたはリスナを生成します。

```shell
php artisan event:generate
```

<!-- Alternatively, you may use the `make:event` and `make:listener` Artisan commands to generate individual events and listeners: -->
あるいは、`make:event` および `make:listener` Artisan コマンドを使用して、個別のイベントとリスナを生成することもできます。

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
<!-- ### Manually Registering Events -->
### Manually Registering Events

<!-- Typically, events should be registered via the `EventServiceProvider` `$listen` array; however, you may also register class or closure based event listeners manually in the `boot` method of your `EventServiceProvider`: -->
通常、イベントは `EventServiceProvider` `$listen` 配列経由で登録する必要があります。ただし、`EventServiceProvider` の `boot` メソッドでクラスまたはクロージャ ベースのイベント リスナを手動で登録することもできます。

```
use App\Events\PodcastProcessed;
use App\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
{
    Event::listen(
        PodcastProcessed::class,
        [SendPodcastNotification::class, 'handle']
    );

    Event::listen(function (PodcastProcessed $event) {
        //
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
<!-- #### Queueable Anonymous Event Listeners -->
#### Queueable Anonymous Event Listeners

<!-- When registering closure based event listeners manually, you may wrap the listener closure within the `Illuminate\Events\queueable` function to instruct Laravel to execute the listener using the [queue](/docs/9.x/queues): -->
クロージャベースのイベントリスナを手動で登録する場合、`Illuminate\Events\queueable` 関数内でリスナクロージャをラップして、[queue](/docs/9.x/queues) を使用してリスナを実行するように Laravel に指示できます。

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    }));
}
```

<!-- Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener: -->
キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

```
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener. This closure will receive the event instance and the `Throwable` instance that caused the listener's failure: -->
匿名のキューに入れられたリスナの失敗を処理したい場合は、`queueable` リスナを定義するときに、`catch` メソッドにクロージャを提供できます。このクロージャは、リスナの失敗の原因となったイベント インスタンスと `Throwable` インスタンスを受け取ります。

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="wildcard-event-listeners"></a>
<!-- #### Wildcard Event Listeners -->
#### Wildcard Event Listeners

<!-- You may even register listeners using the `*` as a wildcard parameter, allowing you to catch multiple events on the same listener. Wildcard listeners receive the event name as their first argument and the entire event data array as their second argument: -->
`*` をワイルドカード パラメーターとして使用してリスナを登録することもでき、同じリスナで複数のイベントをキャッチできるようになります。ワイルドカード リスナは、最初の引数としてイベント名を受け取り、2 番目の引数としてイベント データ配列全体を受け取ります。

```
Event::listen('event.*', function ($eventName, array $data) {
    //
});
```

<a name="event-discovery"></a>
<!-- ### Event Discovery -->
### Event Discovery

<!-- Instead of registering events and listeners manually in the `$listen` array of the `EventServiceProvider`, you can enable automatic event discovery. When event discovery is enabled, Laravel will automatically find and register your events and listeners by scanning your application's `Listeners` directory. In addition, any explicitly defined events listed in the `EventServiceProvider` will still be registered. -->
`EventServiceProvider` の `$listen` 配列にイベントとリスナを手動で登録する代わりに、自動イベント検出を有効にすることができます。イベント検出が有効になっている場合、Laravel はアプリケーションの `Listeners` ディレクトリをスキャンすることにより、イベントとリスナを自動的に検索して登録します。さらに、`EventServiceProvider` にリストされている明示的に定義されたイベントは引き続き登録されます。

<!-- Laravel finds event listeners by scanning the listener classes using PHP's reflection services. When Laravel finds any listener class method that begins with `handle` or `__invoke`, Laravel will register those methods as event listeners for the event that is type-hinted in the method's signature: -->
Laravel は、PHP のリフレクション サービスを使用してリスナ クラスをスキャンすることにより、イベント リスナを見つけます。 Laravel が `handle` または `__invoke` で始まるリスナ クラス メソッドを見つけると、Laravel はそれらのメソッドを、メソッドのシグネチャでタイプヒントされているイベントのイベント リスナとして登録します。

```
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the given event.
     *
     * @param  \App\Events\PodcastProcessed  $event
     * @return void
     */
    public function handle(PodcastProcessed $event)
    {
        //
    }
}
```

<!-- Event discovery is disabled by default, but you can enable it by overriding the `shouldDiscoverEvents` method of your application's `EventServiceProvider`: -->
イベント検出はデフォルトでは無効になっていますが、アプリケーションの `EventServiceProvider` の `shouldDiscoverEvents` メソッドをオーバーライドすることで有効にできます。

```
/**
 * Determine if events and listeners should be automatically discovered.
 *
 * @return bool
 */
public function shouldDiscoverEvents()
{
    return true;
}
```

<!-- By default, all listeners within your application's `app/Listeners` directory will be scanned. If you would like to define additional directories to scan, you may override the `discoverEventsWithin` method in your `EventServiceProvider`: -->
デフォルトでは、アプリケーションの `app/Listeners` ディレクトリ内のすべてのリスナがスキャンされます。スキャンする追加のディレクトリを定義したい場合は、`EventServiceProvider` の `discoverEventsWithin` メソッドをオーバーライドできます。

```
/**
 * Get the listener directories that should be used to discover events.
 *
 * @return array
 */
protected function discoverEventsWithin()
{
    return [
        $this->app->path('Listeners'),
    ];
}
```

<a name="event-discovery-in-production"></a>
<!-- #### Event Discovery In Production -->
#### Event Discovery In Production

<!-- In production, it is not efficient for the framework to scan all of your listeners on every request. Therefore, during your deployment process, you should run the `event:cache` Artisan command to cache a manifest of all of your application's events and listeners. This manifest will be used by the framework to speed up the event registration process. The `event:clear` command may be used to destroy the cache. -->
運用環境では、フレームワークがリクエストごとにすべてのリスナをスキャンするのは効率的ではありません。したがって、デプロイメントプロセス中に、`event:cache` Artisan コマンドを実行して、アプリケーションのすべてのイベントとリスナのマニフェストをキャッシュする必要があります。このマニフェストは、イベント登録プロセスを高速化するためにフレームワークによって使用されます。 `event:clear` コマンドを使用してキャッシュを破棄することができます。

<a name="defining-events"></a>
<!-- ## Defining Events -->
## Defining Events

<!-- An event class is essentially a data container which holds the information related to the event. For example, let's assume an `App\Events\OrderShipped` event receives an [Eloquent ORM](/docs/9.x/eloquent) object: -->
イベント クラスは本質的に、イベントに関連する情報を保持するデータ コンテナーです。たとえば、`App\Events\OrderShipped` イベントが [Eloquent ORM](/docs/9.x/eloquent) オブジェクトを受信すると仮定します。

```
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
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * Create a new event instance.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }
}
```

<!-- As you can see, this event class contains no logic. It is a container for the `App\Models\Order` instance that was purchased. The `SerializesModels` trait used by the event will gracefully serialize any Eloquent models if the event object is serialized using PHP's `serialize` function, such as when utilizing [queued listeners](#queued-event-listeners). -->
ご覧のとおり、このイベント クラスにはロジックが含まれていません。購入した `App\Models\Order` インスタンスのコンテナーです。イベントで使用される `SerializesModels` トレイトは、イベント オブジェクトが PHP の `serialize` 関数を使用してシリアル化されている場合 ([queued listeners](#queued-event-listeners) を利用している場合など)、Eloquent モデルを適切にシリアル化します。

<a name="defining-listeners"></a>
<!-- ## Defining Listeners -->
## Defining Listeners

<!-- Next, let's take a look at the listener for our example event. Event listeners receive event instances in their `handle` method. The `event:generate` and `make:listener` Artisan commands will automatically import the proper event class and type-hint the event on the `handle` method. Within the `handle` method, you may perform any actions necessary to respond to the event: -->
次に、サンプル イベントのリスナを見てみましょう。イベント リスナは、`handle` メソッドでイベント インスタンスを受け取ります。 `event:generate` および `make:listener` Artisan コマンドは、適切なイベント クラスを自動的にインポートし、`handle` メソッドでイベントをタイプヒントします。 `handle` メソッド内で、イベントに応答するために必要なアクションを実行できます。

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Handle the event.
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        // Access the order using $event->order...
    }
}
```

> [!NOTE]
> イベント リスナは、コンストラクターに必要な依存関係をタイプヒントで示すこともできます。すべてのイベント リスナは Laravel [service container](/docs/9.x/container) 経由で解決されるため、依存関係は自動的に挿入されます。

<a name="stopping-the-propagation-of-an-event"></a>
<!-- #### Stopping The Propagation Of An Event -->
#### Stopping The Propagation Of An Event

<!-- Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method. -->
場合によっては、他のリスナへのイベントの伝播を停止したい場合があります。これを行うには、リスナの `handle` メソッドから `false` を返します。

<a name="queued-event-listeners"></a>
<!-- ## Queued Event Listeners -->
## Queued Event Listeners

<!-- Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/9.x/queues) and start a queue worker on your server or local development environment. -->
リスナのキューイングは、リスナが電子メールの送信や HTTP リクエストの作成などの遅いタスクを実行する場合に有益です。キュー リスナを使用する前に、必ず [configure your queue](/docs/9.x/queues) を実行し、サーバーまたはローカル開発環境でキューワーカーを起動してください。

<!-- To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `event:generate` and `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately: -->
リスナをキューに入れるように指定するには、`ShouldQueue` インターフェイスをリスナ クラスに追加します。 `event:generate` および `make:listener` Artisan コマンドによって生成されたリスナには、このインターフェイスがすでに現在のネームスペースにインポートされているため、すぐに使用できます。

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    //
}
```

<!-- That's it! Now, when an event handled by this listener is dispatched, the listener will automatically be queued by the event dispatcher using Laravel's [queue system](/docs/9.x/queues). If no exceptions are thrown when the listener is executed by the queue, the queued job will automatically be deleted after it has finished processing. -->
それでおしまい！このリスナによって処理されるイベントがディスパッチされると、リスナは Laravel の [queue system](/docs/9.x/queues) を使用するイベント ディスパッチャーによって自動的にキューに入れられます。リスナがキューによって実行されたときに例外がスローされなかった場合、キューに入れられたジョブは処理終了後に自動的に削除されます。

<a name="customizing-the-queue-connection-queue-name"></a>
<!-- #### Customizing The Queue Connection & Queue Name -->
#### Customizing The Queue Connection & Queue Name

<!-- If you would like to customize the queue connection, queue name, or queue delay time of an event listener, you may define the `$connection`, `$queue`, or `$delay` properties on your listener class: -->
イベント リスナのキュー接続、キュー名、またはキュー遅延時間をカスタマイズする場合は、リスナ クラスで `$connection`、`$queue`、または `$delay` プロパティを定義できます。

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The name of the connection the job should be sent to.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * The name of the queue the job should be sent to.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * The time (seconds) before the job should be processed.
     *
     * @var int
     */
    public $delay = 60;
}
```

<!-- If you would like to define the listener's queue connection or queue name at runtime, you may define `viaConnection` or `viaQueue` methods on the listener: -->
実行時にリスナのキュー接続またはキュー名を定義したい場合は、リスナで `viaConnection` メソッドまたは `viaQueue` メソッドを定義できます。

```
/**
 * Get the name of the listener's queue connection.
 *
 * @return string
 */
public function viaConnection()
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 *
 * @return string
 */
public function viaQueue()
{
    return 'listeners';
}
```

<a name="conditionally-queueing-listeners"></a>
<!-- #### Conditionally Queueing Listeners -->
#### Conditionally Queueing Listeners

<!-- Sometimes, you may need to determine whether a listener should be queued based on some data that are only available at runtime. To accomplish this, a `shouldQueue` method may be added to a listener to determine whether the listener should be queued. If the `shouldQueue` method returns `false`, the listener will not be executed: -->
場合によっては、実行時にのみ使用できるデータに基づいて、リスナをキューに入れる必要があるかどうかを決定する必要がある場合があります。これを実現するには、`shouldQueue` メソッドをリスナに追加して、リスナをキューに入れる必要があるかどうかを決定できます。 `shouldQueue` メソッドが `false` を返した場合、リスナは実行されません。

```
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return void
     */
    public function handle(OrderCreated $event)
    {
        //
    }

    /**
     * Determine whether the listener should be queued.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return bool
     */
    public function shouldQueue(OrderCreated $event)
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
<!-- ### Manually Interacting With The Queue -->
### Manually Interacting With The Queue

<!-- If you need to manually access the listener's underlying queue job's `delete` and `release` methods, you may do so using the `Illuminate\Queue\InteractsWithQueue` trait. This trait is imported by default on generated listeners and provides access to these methods: -->
リスナの基になるキュー ジョブの `delete` および `release` メソッドに手動でアクセスする必要がある場合は、`Illuminate\Queue\InteractsWithQueue` 特性を使用してアクセスできます。この特性は、生成されたリスナにデフォルトでインポートされ、次のメソッドへのアクセスを提供します。

```
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
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        if (true) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
<!-- ### Queued Event Listeners & Database Transactions -->
### Queued Event Listeners & Database Transactions

<!-- When queued listeners are dispatched within database transactions, they may be processed by the queue before the database transaction has committed. When this happens, any updates you have made to models or database records during the database transaction may not yet be reflected in the database. In addition, any models or database records created within the transaction may not exist in the database. If your listener depends on these models, unexpected errors can occur when the job that dispatches the queued listener is processed. -->
キューに入れられたリスナがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。リスナがこれらのモデルに依存している場合、キューに入れられたリスナをディスパッチするジョブの処理時に予期しないエラーが発生する可能性があります。

<!-- If your queue connection's `after_commit` configuration option is set to `false`, you may still indicate that a particular queued listener should be dispatched after all open database transactions have been committed by defining an `$afterCommit` property on the listener class: -->
キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、リスナ クラスで `$afterCommit` プロパティを定義することで、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられたリスナをディスパッチする必要があることを示すことができます。

```
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    public $afterCommit = true;
}
```

> [!NOTE]
> これらの問題の回避方法の詳細については、[queued jobs and database transactions](/docs/9.x/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="handling-failed-jobs"></a>
<!-- ### Handling Failed Jobs -->
### Handling Failed Jobs

<!-- Sometimes your queued event listeners may fail. If the queued listener exceeds the maximum number of attempts as defined by your queue worker, the `failed` method will be called on your listener. The `failed` method receives the event instance and the `Throwable` that caused the failure: -->
場合によっては、キューに入れられたイベント リスナが失敗することがあります。キューに入れられたリスナがキューワーカーによって定義された最大試行回数を超えると、`failed` メソッドがリスナで呼び出されます。 `failed` メソッドは、イベント インスタンスと失敗の原因となった `Throwable` を受け取ります。

```
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
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        //
    }

    /**
     * Handle a job failure.
     *
     * @param  \App\Events\OrderShipped  $event
     * @param  \Throwable  $exception
     * @return void
     */
    public function failed(OrderShipped $event, $exception)
    {
        //
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
<!-- #### Specifying Queued Listener Maximum Attempts -->
#### Specifying Queued Listener Maximum Attempts

<!-- If one of your queued listeners is encountering an error, you likely do not want it to keep retrying indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a listener may be attempted. -->
キューに入れられたリスナの 1 つでエラーが発生した場合、そのリスナが無制限に再試行を続けることは望ましくありません。したがって、Laravel では、リスナの試行回数または試行時間を指定するさまざまな方法が提供されています。

<!-- You may define a `$tries` property on your listener class to specify how many times the listener may be attempted before it is considered to have failed: -->
リスナ クラスで `$tries` プロパティを定義して、リスナが失敗したとみなされるまでの試行回数を指定できます。

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

<!-- As an alternative to defining how many times a listener may be attempted before it fails, you may define a time at which the listener should no longer be attempted. This allows a listener to be attempted any number of times within a given time frame. To define the time at which a listener should no longer be attempted, add a `retryUntil` method to your listener class. This method should return a `DateTime` instance: -->
失敗するまでにリスナを何回試行できるかを定義する代わりに、リスナを試行しなくなる時間を定義することもできます。これにより、リスナは指定された時間枠内で何度でも試行できます。リスナを試行しなくなる時間を定義するには、`retryUntil` メソッドをリスナ クラスに追加します。このメソッドは `DateTime` インスタンスを返す必要があります。

```
/**
 * Determine the time at which the listener should timeout.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

<a name="dispatching-events"></a>
<!-- ## Dispatching Events -->
## Dispatching Events

<!-- To dispatch an event, you may call the static `dispatch` method on the event. This method is made available on the event by the `Illuminate\Foundation\Events\Dispatchable` trait. Any arguments passed to the `dispatch` method will be passed to the event's constructor: -->
イベントをディスパッチするには、イベントで静的 `dispatch` メソッドを呼び出すことができます。このメソッドは、`Illuminate\Foundation\Events\Dispatchable` トレイトによってイベントで使用できるようになります。 `dispatch` メソッドに渡される引数はすべて、イベントのコンストラクターに渡されます。

```
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);
    }
}
```
<!--  If you would like to conditionally dispatch an event, you may use the `dispatchIf` and `dispatchUnless` methods: -->
条件付きでイベントをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

```
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> テストする場合、特定のイベントが実際にリスナをトリガーせずにディスパッチされたことをアサートすると役立つ場合があります。 Laravel の [built-in testing helpers](/docs/9.x/mocking#event-fake) を使えば簡単です。

<a name="event-subscribers"></a>
<!-- ## Event Subscribers -->
## Event Subscribers

<a name="writing-event-subscribers"></a>
<!-- ### Writing Event Subscribers -->
### Writing Event Subscribers

<!-- Event subscribers are classes that may subscribe to multiple events from within the subscriber class itself, allowing you to define several event handlers within a single class. Subscribers should define a `subscribe` method, which will be passed an event dispatcher instance. You may call the `listen` method on the given dispatcher to register event listeners: -->
イベント サブスクライバは、サブスクライバ クラス自体内から複数のイベントをサブスクライブできるクラスであり、単一クラス内で複数のイベント ハンドラを定義できます。サブスクライバは、イベント ディスパッチャー インスタンスに渡される `subscribe` メソッドを定義する必要があります。指定されたディスパッチャーで `listen` メソッドを呼び出して、イベント リスナを登録できます。

```
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin($event) {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout($event) {}

    /**
     * Register the listeners for the subscriber.
     *
     * @param  \Illuminate\Events\Dispatcher  $events
     * @return void
     */
    public function subscribe($events)
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

```
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin($event) {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout($event) {}

    /**
     * Register the listeners for the subscriber.
     *
     * @param  \Illuminate\Events\Dispatcher  $events
     * @return array
     */
    public function subscribe($events)
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

<!-- After writing the subscriber, you are ready to register it with the event dispatcher. You may register subscribers using the `$subscribe` property on the `EventServiceProvider`. For example, let's add the `UserEventSubscriber` to the list: -->
サブスクライバを作成したら、それをイベント ディスパッチャーに登録する準備が整います。 `EventServiceProvider` の `$subscribe` プロパティを使用してサブスクライバを登録できます。たとえば、`UserEventSubscriber` をリストに追加してみましょう。

```
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        //
    ];

    /**
     * The subscriber classes to register.
     *
     * @var array
     */
    protected $subscribe = [
        UserEventSubscriber::class,
    ];
}
```

