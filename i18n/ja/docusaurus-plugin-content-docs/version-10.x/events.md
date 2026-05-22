# イベント (Events)

- [Introduction](#introduction)
- [イベントとリスナの登録](#registering-events-and-listeners)
    - [イベントとリスナの生成](#generating-events-and-listeners)
    - [イベントを手動で登録する](#manually-registering-events)
    - [イベントディスカバリ](#event-discovery)
- [イベントの定義](#defining-events)
- [リスナの定義](#defining-listeners)
- [キューに入れられたイベントリスナ](#queued-event-listeners)
    - [手動でキューを操作する](#manually-interacting-with-the-queue)
    - [キューに入れられたイベント リスナとデータベース トランザクション](#queued-event-listeners-and-database-transactions)
    - [失敗したジョブの処理](#handling-failed-jobs)
- [イベントのディスパッチ](#dispatching-events)
    - [データベーストランザクション後のイベントのディスパッチ](#dispatching-events-after-database-transactions)
- [イベント購読者](#event-subscribers)
    - [イベントサブスクライバの書き込み](#writing-event-subscribers)
    - [イベントサブスクライバの登録](#registering-event-subscribers)
- [Testing](#testing)
    - [イベントのサブセットを偽装する](#faking-a-subset-of-events)
    - [スコープ付きイベントのフェイク](#scoped-event-fakes)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel のイベントはシンプルなオブザーバ パターンの実装を提供し、アプリケーション内で発生するさまざまなイベントをサブスクライブしてリッスンできるようにします。通常、イベント クラスは `app/Events` ディレクトリに保存され、そのリスナは `app/Listeners` に保存されます。アプリケーションにこれらのディレクトリが表示されない場合でも、Artisan コンソール コマンドを使用してイベントとリスナを生成すると自動的に作成されるため、心配する必要はありません。

イベントは、単一のイベントに相互に依存しない複数のリスナを持つことができるため、アプリケーションのさまざまな側面を分離する優れた方法として機能します。たとえば、注文が発送されるたびにユーザーに Slack 通知を送信したい場合があります。注文処理コードを Slack 通知コードに結合する代わりに、リスナが受信して Slack 通知をディスパッチするために使用できる `App\Events\OrderShipped` イベントを発生させることができます。

<a name="registering-events-and-listeners"></a>
## イベントとリスナの登録 (Registering Events and Listeners)

Laravel アプリケーションに含まれる `App\Providers\EventServiceProvider` は、アプリケーションのすべてのイベント リスナを登録する便利な場所を提供します。 `listen` プロパティには、すべてのイベント (キー) とそのリスナ (値) の配列が含まれます。アプリケーションが必要とするだけの数のイベントをこの配列に追加できます。たとえば、`OrderShipped` イベントを追加してみましょう。

    use App\Events\OrderShipped;
    use App\Listeners\SendShipmentNotification;

    /**
     * The event listener mappings for the application.
     *
     * @var array<class-string, array<int, class-string>>
     */
    protected $listen = [
        OrderShipped::class => [
            SendShipmentNotification::class,
        ],
    ];

> [!NOTE]  
> `event:list` コマンドを使用すると、アプリケーションによって登録されたすべてのイベントとリスナのリストを表示できます。

<a name="generating-events-and-listeners"></a>
### イベントとリスナの生成

もちろん、イベントやリスナごとに手動でファイルを作成するのは面倒です。代わりに、`EventServiceProvider` にリスナとイベントを追加し、`event:generate` Artisan コマンドを使用します。このコマンドは、`EventServiceProvider` にリストされているまだ存在しないイベントまたはリスナを生成します。

```shell
php artisan event:generate
```

あるいは、`make:event` および `make:listener` Artisan コマンドを使用して、個別のイベントとリスナを生成することもできます。

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### イベントを手動で登録する

通常、イベントは `EventServiceProvider` `$listen` 配列経由で登録する必要があります。ただし、`EventServiceProvider` の `boot` メソッドでクラスまたはクロージャ ベースのイベント リスナを手動で登録することもできます。

    use App\Events\PodcastProcessed;
    use App\Listeners\SendPodcastNotification;
    use Illuminate\Support\Facades\Event;

    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(
            PodcastProcessed::class,
            SendPodcastNotification::class,
        );

        Event::listen(function (PodcastProcessed $event) {
            // ...
        });
    }

<a name="queuable-anonymous-event-listeners"></a>
#### キュー可能な匿名イベント リスナ

クロージャベースのイベントリスナを手動で登録する場合、`Illuminate\Events\queueable` 関数内でリスナクロージャをラップして、[queue](/docs/{{version}}/queues) を使用してリスナを実行するように Laravel に指示できます。

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;

    /**
     * Register any other events for your application.
     */
    public function boot(): void
    {
        Event::listen(queueable(function (PodcastProcessed $event) {
            // ...
        }));
    }

キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

匿名のキューに入れられたリスナの失敗を処理したい場合は、`queueable` リスナを定義するときに、`catch` メソッドにクロージャを提供できます。このクロージャは、リスナの失敗の原因となったイベント インスタンスと `Throwable` インスタンスを受け取ります。

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // The queued listener failed...
    }));

<a name="wildcard-event-listeners"></a>
#### ワイルドカード イベント リスナ

`*` をワイルドカード パラメーターとして使用してリスナを登録することもでき、同じリスナで複数のイベントをキャッチできるようになります。ワイルドカード リスナは、最初の引数としてイベント名を受け取り、2 番目の引数としてイベント データ配列全体を受け取ります。

    Event::listen('event.*', function (string $eventName, array $data) {
        // ...
    });

<a name="event-discovery"></a>
### イベントディスカバリ

`EventServiceProvider` の `$listen` 配列にイベントとリスナを手動で登録する代わりに、自動イベント検出を有効にすることができます。イベント検出が有効になっている場合、Laravel はアプリケーションの `Listeners` ディレクトリをスキャンすることにより、イベントとリスナを自動的に検索して登録します。さらに、`EventServiceProvider` にリストされている明示的に定義されたイベントは引き続き登録されます。

Laravel は、PHP のリフレクション サービスを使用してリスナ クラスをスキャンすることにより、イベント リスナを見つけます。 Laravel が `handle` または `__invoke` で始まるリスナ クラス メソッドを見つけると、Laravel はそれらのメソッドを、メソッドのシグネチャでタイプヒントされているイベントのイベント リスナとして登録します。

    use App\Events\PodcastProcessed;

    class SendPodcastNotification
    {
        /**
         * Handle the given event.
         */
        public function handle(PodcastProcessed $event): void
        {
            // ...
        }
    }

イベント検出はデフォルトでは無効になっていますが、アプリケーションの `EventServiceProvider` の `shouldDiscoverEvents` メソッドをオーバーライドすることで有効にできます。

    /**
     * Determine if events and listeners should be automatically discovered.
     */
    public function shouldDiscoverEvents(): bool
    {
        return true;
    }

デフォルトでは、アプリケーションの `app/Listeners` ディレクトリ内のすべてのリスナがスキャンされます。スキャンする追加のディレクトリを定義したい場合は、`EventServiceProvider` の `discoverEventsWithin` メソッドをオーバーライドできます。

    /**
     * Get the listener directories that should be used to discover events.
     *
     * @return array<int, string>
     */
    protected function discoverEventsWithin(): array
    {
        return [
            $this->app->path('Listeners'),
        ];
    }

<a name="event-discovery-in-production"></a>
#### 本番環境でのイベント検出

運用環境では、フレームワークがリクエストごとにすべてのリスナをスキャンするのは効率的ではありません。したがって、デプロイメントプロセス中に、`event:cache` Artisan コマンドを実行して、アプリケーションのすべてのイベントとリスナのマニフェストをキャッシュする必要があります。このマニフェストは、イベント登録プロセスを高速化するためにフレームワークによって使用されます。 `event:clear` コマンドを使用してキャッシュを破棄することができます。

<a name="defining-events"></a>
## イベントの定義 (Defining Events)

イベント クラスは本質的に、イベントに関連する情報を保持するデータ コンテナーです。たとえば、`App\Events\OrderShipped` イベントが [Eloquent ORM](/docs/{{version}}/eloquent) オブジェクトを受信すると仮定します。

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

ご覧のとおり、このイベント クラスにはロジックが含まれていません。購入した `App\Models\Order` インスタンスのコンテナーです。イベントで使用される `SerializesModels` トレイトは、イベント オブジェクトが PHP の `serialize` 関数を使用してシリアル化されている場合 ([キューに入れられたリスナ](#queued-event-listeners) を利用している場合など)、Eloquent モデルを適切にシリアル化します。

<a name="defining-listeners"></a>
## リスナの定義 (Defining Listeners)

次に、サンプル イベントのリスナを見てみましょう。イベント リスナは、`handle` メソッドでイベント インスタンスを受け取ります。 `event:generate` および `make:listener` Artisan コマンドは、適切なイベント クラスを自動的にインポートし、`handle` メソッドでイベントをタイプヒントします。 `handle` メソッド内で、イベントに応答するために必要なアクションを実行できます。

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;

    class SendShipmentNotification
    {
        /**
         * Create the event listener.
         */
        public function __construct()
        {
            // ...
        }

        /**
         * Handle the event.
         */
        public function handle(OrderShipped $event): void
        {
            // Access the order using $event->order...
        }
    }

> [!NOTE]  
> イベント リスナは、コンストラクターに必要な依存関係をタイプヒントで示すこともできます。すべてのイベント リスナは Laravel [サービスコンテナ](/docs/{{version}}/container) 経由で解決されるため、依存関係は自動的に挿入されます。

<a name="stopping-the-propagation-of-an-event"></a>
#### イベントの伝播の停止

場合によっては、他のリスナへのイベントの伝播を停止したい場合があります。これを行うには、リスナの `handle` メソッドから `false` を返します。

<a name="queued-event-listeners"></a>
## キューに入れられたイベントリスナ (Queued Event Listeners)

リスナのキューイングは、リスナが電子メールの送信や HTTP リクエストの作成などの遅いタスクを実行する場合に有益です。キュー リスナを使用する前に、必ず [キューを設定する](/docs/{{version}}/queues) を実行し、サーバーまたはローカル開発環境でキューワーカーを起動してください。

リスナをキューに入れるように指定するには、`ShouldQueue` インターフェイスをリスナ クラスに追加します。 `event:generate` および `make:listener` Artisan コマンドによって生成されたリスナには、このインターフェイスがすでに現在のネームスペースにインポートされているため、すぐに使用できます。

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        // ...
    }

それでおしまい！このリスナによって処理されるイベントがディスパッチされると、リスナは Laravel の [キューシステム](/docs/{{version}}/queues) を使用するイベント ディスパッチャーによって自動的にキューに入れられます。リスナがキューによって実行されたときに例外がスローされなかった場合、キューに入れられたジョブは処理終了後に自動的に削除されます。

<a name="customizing-the-queue-connection-queue-name"></a>
#### キューの接続、名前、遅延のカスタマイズ

イベント リスナのキュー接続、キュー名、またはキュー遅延時間をカスタマイズする場合は、リスナ クラスで `$connection`、`$queue`、または `$delay` プロパティを定義できます。

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

リスナのキュー接続、キュー名、または実行時の遅延を定義したい場合は、リスナで `viaConnection`、`viaQueue`、または `withDelay` メソッドを定義できます。

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

<a name="conditionally-queueing-listeners"></a>
#### 条件付きでリスナをキューイングする

場合によっては、実行時にのみ使用できるデータに基づいて、リスナをキューに入れる必要があるかどうかを決定する必要がある場合があります。これを実現するには、`shouldQueue` メソッドをリスナに追加して、リスナをキューに入れる必要があるかどうかを決定できます。 `shouldQueue` メソッドが `false` を返した場合、リスナは実行されません。

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

<a name="manually-interacting-with-the-queue"></a>
### 手動でキューを操作する

リスナの基になるキュー ジョブの `delete` および `release` メソッドに手動でアクセスする必要がある場合は、`Illuminate\Queue\InteractsWithQueue` 特性を使用してアクセスできます。この特性は、生成されたリスナにデフォルトでインポートされ、次のメソッドへのアクセスを提供します。

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
            if (true) {
                $this->release(30);
            }
        }
    }

<a name="queued-event-listeners-and-database-transactions"></a>
### キューに入れられたイベント リスナとデータベース トランザクション

キューに入れられたリスナがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。リスナがこれらのモデルに依存している場合、キューに入れられたリスナをディスパッチするジョブの処理時に予期しないエラーが発生する可能性があります。

キュー接続の `after_commit` 構成オプションが `false` に設定されている場合でも、リスナ クラスに `ShouldHandleEventsAfterCommit` インターフェイスを実装することで、開いているすべてのデータベース トランザクションがコミットされた後に特定のキューに入れられたリスナをディスパッチする必要があることを示すことができます。

    <?php

    namespace App\Listeners;

    use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue, ShouldHandleEventsAfterCommit
    {
        use InteractsWithQueue;
    }

> [!NOTE]  
> これらの問題の回避方法の詳細については、[キューに入れられたジョブとデータベース トランザクション](/docs/{{version}}/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="handling-failed-jobs"></a>
### 失敗したジョブの処理

場合によっては、キューに入れられたイベント リスナが失敗することがあります。キューに入れられたリスナがキューワーカーによって定義された最大試行回数を超えると、`failed` メソッドがリスナで呼び出されます。 `failed` メソッドは、イベント インスタンスと失敗の原因となった `Throwable` を受け取ります。

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

<a name="specifying-queued-listener-maximum-attempts"></a>
#### キューに入れられたリスナの最大試行回数の指定

キューに入れられたリスナの 1 つでエラーが発生した場合、そのリスナが無制限に再試行を続けることは望ましくありません。したがって、Laravel では、リスナの試行回数または試行時間を指定するさまざまな方法が提供されています。

リスナ クラスで `$tries` プロパティを定義して、リスナが失敗したとみなされるまでの試行回数を指定できます。

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

失敗するまでにリスナを何回試行できるかを定義する代わりに、リスナを試行しなくなる時間を定義することもできます。これにより、リスナは指定された時間枠内で何度でも試行できます。リスナを試行しなくなる時間を定義するには、`retryUntil` メソッドをリスナ クラスに追加します。このメソッドは `DateTime` インスタンスを返す必要があります。

    use DateTime;

    /**
     * Determine the time at which the listener should timeout.
     */
    public function retryUntil(): DateTime
    {
        return now()->addMinutes(5);
    }

<a name="dispatching-events"></a>
## イベントのディスパッチ (Dispatching Events)

イベントをディスパッチするには、イベントで静的 `dispatch` メソッドを呼び出すことができます。このメソッドは、`Illuminate\Foundation\Events\Dispatchable` トレイトによってイベントで使用できるようになります。 `dispatch` メソッドに渡される引数はすべて、イベントのコンストラクターに渡されます。

    <?php

    namespace App\Http\Controllers;

    use App\Events\OrderShipped;
    use App\Http\Controllers\Controller;
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
    
条件付きでイベントをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

    OrderShipped::dispatchIf($condition, $order);

    OrderShipped::dispatchUnless($condition, $order);

> [!NOTE]  
> テストする場合、特定のイベントが実際にリスナをトリガーせずにディスパッチされたことをアサートすると役立つ場合があります。 Laravel の [組み込みのテストヘルパ](#testing) を使えば簡単です。

<a name="dispatching-events-after-database-transactions"></a>
### データベーストランザクション後のイベントのディスパッチ

場合によっては、アクティブなデータベーストランザクションがコミットされた後にのみイベントをディスパッチするようにLaravelに指示したい場合があります。これを行うには、イベント クラスに `ShouldDispatchAfterCommit` インターフェイスを実装します。

このインターフェイスは、現在のデータベーストランザクションがコミットされるまでイベントをディスパッチしないようにLaravelに指示します。トランザクションが失敗した場合、イベントは破棄されます。イベントが送出されるときにデータベース トランザクションが進行中でない場合、イベントはすぐに送出されます。

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

<a name="event-subscribers"></a>
## イベント購読者 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### イベントサブスクライバの書き込み

イベント サブスクライバは、サブスクライバ クラス自体内から複数のイベントをサブスクライブできるクラスであり、単一クラス内で複数のイベント ハンドラを定義できます。サブスクライバは、イベント ディスパッチャー インスタンスに渡される `subscribe` メソッドを定義する必要があります。指定されたディスパッチャーで `listen` メソッドを呼び出して、イベント リスナを登録できます。

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

イベント リスナ メソッドがサブスクライバ自体内で定義されている場合は、サブスクライバの `subscribe` メソッドからイベントとメソッド名の配列を返す方が便利な場合があります。 Laravel は、イベントリスナを登録するときにサブスクライバのクラス名を自動的に決定します。

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

<a name="registering-event-subscribers"></a>
### イベントサブスクライバの登録

サブスクライバを作成したら、それをイベント ディスパッチャーに登録する準備が整います。 `EventServiceProvider` の `$subscribe` プロパティを使用してサブスクライバを登録できます。たとえば、`UserEventSubscriber` をリストに追加してみましょう。

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
            // ...
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

<a name="testing"></a>
## テスト (Testing)

イベントを送出するコードをテストする場合、リスナのコードは、対応するイベントを送出するコードとは別に直接テストできるため、イベントのリスナを実際に実行しないように Laravel に指示することもできます。もちろん、リスナ自体をテストするには、リスナ インスタンスをインスタンス化し、テスト内で `handle` メソッドを直接呼び出します。

`Event` ファサードの `fake` メソッドを使用すると、リスナの実行を防止し、テスト対象のコードを実行してから、`assertDispatched`、`assertNotDispatched`、および `assertNothingDispatched` メソッドを使用してアプリケーションによってどのイベントがディスパッチされたかをアサートできます。

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

            // Assert an event was not dispatched...
            Event::assertNotDispatched(OrderFailedToShip::class);

            // Assert that no events were dispatched...
            Event::assertNothingDispatched();
        }
    }

特定の「真実テスト」に合格するイベントがディスパッチされたことをアサートするために、`assertDispatched` メソッドまたは `assertNotDispatched` メソッドにクロージャーを渡すことができます。指定された真実テストに合格する少なくとも 1 つのイベントがディスパッチされた場合、アサーションは成功します。

    Event::assertDispatched(function (OrderShipped $event) use ($order) {
        return $event->order->id === $order->id;
    });

イベント リスナが特定のイベントをリッスンしていることを単にアサートしたい場合は、`assertListening` メソッドを使用できます。

    Event::assertListening(
        OrderShipped::class,
        SendShipmentNotification::class
    );

> [!WARNING]  
> `Event::fake()` を呼び出した後は、イベント リスナは実行されません。したがって、モデルの `creating` イベント中に UUID を作成するなど、イベントに依存するモデル ファクトリをテストで使用する場合は、ファクトリを使用した **後** で `Event::fake()` を呼び出す必要があります。

<a name="faking-a-subset-of-events"></a>
### イベントのサブセットを偽装する

特定のイベント セットに対してのみイベント リスナを偽装したい場合は、それらを `fake` メソッドまたは `fakeFor` メソッドに渡すことができます。

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
        $order->update([...]);
    }

`except` メソッドを使用すると、指定されたイベントのセットを除くすべてのイベントを偽装できます。

    Event::fake()->except([
        OrderCreated::class,
    ]);

<a name="scoped-event-fakes"></a>
### スコープ指定されたイベントのフェイク

テストの一部に対してのみイベント リスナを偽装したい場合は、`fakeFor` メソッドを使用できます。

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

            // Events are dispatched as normal and observers will run ...
            $order->update([...]);
        }
    }

