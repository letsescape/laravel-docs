# イベント (Events)

- [Introduction](#introduction)
- [イベントとリスナの生成](#generating-events-and-listeners)
- [イベントとリスナの登録](#registering-events-and-listeners)
    - [イベントディスカバリ](#event-discovery)
    - [イベントを手動で登録する](#manually-registering-events)
    - [クロージャリスナ](#closure-listeners)
- [イベントの定義](#defining-events)
- [リスナの定義](#defining-listeners)
- [キューに入れられたイベントリスナ](#queued-event-listeners)
    - [手動でキューを操作する](#manually-interacting-with-the-queue)
    - [キューに入れられたイベント リスナとデータベース トランザクション](#queued-event-listeners-and-database-transactions)
    - [キューに入れられたリスナ ミドルウェア](#queued-listener-middleware)
    - [暗号化されたキューに入れられたリスナ](#encrypted-queued-listeners)
    - [固有のイベント リスナ](#unique-event-listeners)
        - [処理が開始されるまでリスナを一意に保つ](#keeping-listeners-unique-until-processing-begins)
        - [固有のリスナ ロック](#unique-listener-locks)
    - [失敗したジョブの処理](#handling-failed-jobs)
- [イベントのディスパッチ](#dispatching-events)
    - [データベーストランザクション後のイベントのディスパッチ](#dispatching-events-after-database-transactions)
    - [イベントの延期](#deferring-events)
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

<a name="generating-events-and-listeners"></a>
## イベントとリスナの生成 (Generating Events and Listeners)

イベントとリスナを迅速に生成するには、`make:event` および `make:listener` Artisan コマンドを使用できます。

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

便宜上、追加の引数なしで `make:event` および `make:listener` Artisan コマンドを呼び出すこともできます。これを行うと、Laravel はクラス名と、リスナの作成時にリッスンするイベントの入力を自動的に求めます。

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## イベントとリスナの登録 (Registering Events and Listeners)

<a name="event-discovery"></a>
### イベントディスカバリ

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

リスナを別のディレクトリまたは複数のディレクトリ内に保存する予定がある場合は、アプリケーションの `bootstrap/app.php` ファイル内の `withEvents` メソッドを使用して、これらのディレクトリをスキャンするように Laravel に指示できます。

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 文字をワイルドカードとして使用して、複数の同様のディレクトリでリスナをスキャンできます。

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` コマンドを使用すると、アプリケーション内に登録されているすべてのリスナを一覧表示できます。

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 本番環境でのイベント検出

アプリケーションの速度を向上させるには、`optimize` または `event:cache` Artisan コマンドを使用して、アプリケーションのすべてのリスナのマニフェストをキャッシュする必要があります。通常、このコマンドはアプリケーションの [導入プロセス](/docs/{{version}}/deployment#optimization) の一部として実行する必要があります。このマニフェストは、イベント登録プロセスを高速化するためにフレームワークによって使用されます。 `event:clear` コマンドを使用してイベント キャッシュを破棄することができます。

<a name="manually-registering-events"></a>
### イベントを手動で登録する

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

`event:list` コマンドを使用すると、アプリケーション内に登録されているすべてのリスナを一覧表示できます。

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### クロージャリスナ

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

<a name="queuable-anonymous-event-listeners"></a>
#### キュー可能な匿名イベント リスナ

クロージャベースのイベントリスナを登録する場合、`Illuminate\Events\queueable` 関数内でリスナクロージャをラップして、[queue](/docs/{{version}}/queues) を使用してリスナを実行するように Laravel に指示できます。

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

キューに入れられたジョブと同様に、`onConnection`、`onQueue`、および `delay` メソッドを使用して、キューに入れられたリスナの実行をカスタマイズできます。

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

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
#### ワイルドカード イベント リスナ

また、ワイルドカード パラメーターとして `*` 文字を使用してリスナを登録し、同じリスナで複数のイベントをキャッチできるようにすることもできます。ワイルドカード リスナは、最初の引数としてイベント名を受け取り、2 番目の引数としてイベント データ配列全体を受け取ります。

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## イベントの定義 (Defining Events)

イベント クラスは本質的に、イベントに関連する情報を保持するデータ コンテナーです。たとえば、`App\Events\OrderShipped` イベントが [Eloquent ORM](/docs/{{version}}/eloquent) オブジェクトを受信すると仮定します。

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

ご覧のとおり、このイベント クラスにはロジックが含まれていません。購入した `App\Models\Order` インスタンスのコンテナーです。イベントで使用される `SerializesModels` トレイトは、イベント オブジェクトが PHP の `serialize` 関数を使用してシリアル化されている場合 ([キューに入れられたリスナ](#queued-event-listeners) を利用している場合など)、Eloquent モデルを適切にシリアル化します。

<a name="defining-listeners"></a>
## リスナの定義 (Defining Listeners)

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
> イベント リスナは、コンストラクターに必要な依存関係をタイプヒントで示すこともできます。すべてのイベント リスナは Laravel [サービスコンテナ](/docs/{{version}}/container) 経由で解決されるため、依存関係は自動的に挿入されます。

<a name="stopping-the-propagation-of-an-event"></a>
#### イベントの伝播の停止

場合によっては、他のリスナへのイベントの伝播を停止したい場合があります。これを行うには、リスナの `handle` メソッドから `false` を返します。

<a name="queued-event-listeners"></a>
## キューに入れられたイベントリスナ (Queued Event Listeners)

リスナのキューイングは、リスナが電子メールの送信や HTTP リクエストの作成などの遅いタスクを実行する場合に有益です。キュー リスナを使用する前に、必ず [キューを設定する](/docs/{{version}}/queues) を実行し、サーバーまたはローカル開発環境でキューワーカーを起動してください。

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

それでおしまい！このリスナによって処理されるイベントがディスパッチされると、リスナは Laravel の [キューシステム](/docs/{{version}}/queues) を使用するイベント ディスパッチャーによって自動的にキューに入れられます。リスナがキューによって実行されたときに例外がスローされなかった場合、キューに入れられたジョブは処理終了後に自動的に削除されます。

<a name="customizing-the-queue-connection-queue-name"></a>
#### キューの接続、名前、遅延のカスタマイズ

イベント リスナのキュー接続、キュー名、またはキュー遅延時間をカスタマイズする場合は、リスナ クラスで `$connection`、`$queue`、または `$delay` プロパティを定義できます。

```php
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
#### 条件付きでリスナをキューイングする

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
### 手動でキューを操作する

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
### キューに入れられたイベント リスナとデータベース トランザクション

キューに入れられたリスナがデータベース トランザクション内でディスパッチされると、データベース トランザクションがコミットされる前にキューによって処理される可能性があります。この問題が発生すると、データベース トランザクション中にモデルまたはデータベース レコードに対して行った更新がまだデータベースに反映されていない可能性があります。さらに、トランザクション内で作成されたモデルやデータベース レコードはデータベースに存在しない可能性があります。リスナがこれらのモデルに依存している場合、キューに入れられたリスナをディスパッチするジョブの処理時に予期しないエラーが発生する可能性があります。

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
> これらの問題の回避方法の詳細については、[キューに入れられたジョブとデータベース トランザクション](/docs/{{version}}/queues#jobs-and-database-transactions) に関するドキュメントを参照してください。

<a name="queued-listener-middleware"></a>
### キューに入れられたリスナ ミドルウェア

キューに登録されたリスナは、[ジョブミドルウェア](/docs/{{version}}/queues#job-middleware) を利用することもできます。ジョブ ミドルウェアを使用すると、キューに入れられたリスナの実行にカスタム ロジックをラップして、リスナ自体の定型文を減らすことができます。ジョブ ミドルウェアを作成した後、リスナの `middleware` メソッドからジョブ ミドルウェアを返すことによって、ジョブ ミドルウェアをリスナにアタッチできます。

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
#### 暗号化されたキューに入れられたリスナ

Laravel を使用すると、[encryption](/docs/{{version}}/encryption) 経由でキューに入れられたリスナのデータのプライバシーと整合性を確保できます。まず、`ShouldBeEncrypted` インターフェイスをリスナ クラスに追加するだけです。このインターフェースがクラスに追加されると、Laravel はリスナをキューにプッシュする前に自動的に暗号化します。

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
### 固有のイベント リスナ

> [!WARNING]
> 固有のリスナには、[locks](/docs/{{version}}/cache#atomic-locks) をサポートするキャッシュ ドライバが必要です。現在、`memcached`、`redis`、`dynamodb`、`database`、`file`、および `array` キャッシュ ドライバはアトミック ロックをサポートしています。

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

上の例では、`AcquireProductKey` リスナは一意です。したがって、リスナの別のインスタンスがすでにキュー上にあり、処理が完了していない場合、リスナはキューに入れられません。これにより、ライセンスが立て続けに複数回保存された場合でも、ライセンスごとにプロダクト キーが 1 つだけ取得されるようになります。

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

上の例では、`AcquireProductKey` リスナはライセンス ID によって一意です。したがって、同じライセンスに対するリスナの新しいディスパッチは、既存のリスナが処理を完了するまで無視されます。これにより、同じライセンスに対して重複したプロダクト キーが取得されるのを防ぎます。さらに、既存のリスナが 1 時間以内に処理されない場合、一意のロックが解放され、同じ一意のキーを持つ別のリスナがキューに追加される可能性があります。

> [!WARNING]
> アプリケーションが複数のWebサーバーまたはコンテナからイベントをディスパッチする場合は、Laravelがリスナが一意であるかどうかを正確に判断できるように、すべてのサーバーが同じ中央キャッシュサーバーと通信していることを確認する必要があります。

<a name="keeping-listeners-unique-until-processing-begins"></a>
#### 処理が開始されるまでリスナを一意に保つ

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
#### 固有のリスナ ロック

バックグラウンドでは、`ShouldBeUnique` リスナがディスパッチされると、Laravel は `uniqueId` キーを使用して [lock](/docs/{{version}}/cache#atomic-locks) を取得しようとします。ロックがすでに保持されている場合、リスナはディスパッチされません。このロックは、リスナが処理を完了するか、すべての再試行に失敗すると解放されます。デフォルトでは、Laravel はデフォルトのキャッシュドライバを使用してこのロックを取得します。ただし、ロックの取得に別のドライバを使用したい場合は、使用するキャッシュ ドライバを返す `uniqueVia` メソッドを定義できます。

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
> リスナの同時処理を制限する必要があるだけの場合は、代わりに [WithoutOverlapping](/docs/{{version}}/queues#preventing-job-overlaps) ジョブ ミドルウェアを使用してください。

<a name="handling-failed-jobs"></a>
### 失敗したジョブの処理

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
#### キューに入れられたリスナの最大試行回数の指定

キューに入れられたリスナの 1 つでエラーが発生した場合、そのリスナが無制限に再試行を続けることは望ましくありません。したがって、Laravel では、リスナの試行回数または試行時間を指定するさまざまな方法が提供されています。

リスナ クラスで `tries` プロパティまたはメソッドを定義して、リスナが失敗したとみなされるまでの試行回数を指定できます。

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
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

失敗するまでにリスナを何回試行できるかを定義する代わりに、リスナを試行しなくなる時間を定義することもできます。これにより、リスナは指定された時間枠内で何度でも試行できます。リスナを試行しなくなる時間を定義するには、`retryUntil` メソッドをリスナ クラスに追加します。このメソッドは `DateTime` インスタンスを返す必要があります。

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

`retryUntil` と `tries` の両方が定義されている場合、Laravel は `retryUntil` メソッドを優先します。

<a name="specifying-queued-listener-backoff"></a>
#### キューに入れられたリスナのバックオフの指定

例外が発生したリスナを再試行する前に Laravel が待機する秒数を設定したい場合は、リスナ クラスで `backoff` プロパティを定義することで設定できます。

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

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
#### キューに入れられたリスナの最大例外の指定

場合によっては、キューに入れられたリスナを何度も試行できるが、(`release` メソッドによって直接解放されるのではなく) 指定された数の未処理の例外によって再試行がトリガーされた場合は失敗するように指定したい場合があります。これを実現するには、リスナ クラスで `maxExceptions` プロパティを定義します。

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
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

この例では、リスナは最大 25 回再試行されます。ただし、リスナによって 3 つの未処理の例外がスローされた場合、リスナは失敗します。

<a name="specifying-queued-listener-timeout"></a>
#### キューに入れられたリスナのタイムアウトの指定

多くの場合、キューに入れられたリスナにかかる時間がおおよそわかっています。このため、Laravel では「タイムアウト」値を指定できます。リスナがタイムアウト値で指定された秒数を超えて処理している場合、リスナを処理しているワーカーはエラーで終了します。リスナ クラスで `timeout` プロパティを定義することで、リスナの実行を許可する最大秒数を定義できます。

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The number of seconds the listener can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;
}
```

リスナをタイムアウト時に失敗としてマークする必要があることを示したい場合は、リスナ クラスで `failOnTimeout` プロパティを定義できます。

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Indicate if the listener should be marked as failed on timeout.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## イベントのディスパッチ (Dispatching Events)

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

条件付きでイベントをディスパッチしたい場合は、`dispatchIf` メソッドと `dispatchUnless` メソッドを使用できます。

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> テストする場合、特定のイベントが実際にリスナをトリガーせずにディスパッチされたことをアサートすると役立つ場合があります。 Laravel の [組み込みのテストヘルパ](#testing) を使えば簡単です。

<a name="dispatching-events-after-database-transactions"></a>
### データベーストランザクション後のイベントのディスパッチ

場合によっては、アクティブなデータベーストランザクションがコミットされた後にのみイベントをディスパッチするようにLaravelに指示したい場合があります。これを行うには、イベント クラスに `ShouldDispatchAfterCommit` インターフェイスを実装します。

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
### イベントの延期

遅延イベントを使用すると、コードの特定のブロックが完了するまで、モデル イベントのディスパッチとイベント リスナの実行を遅らせることができます。これは、イベント リスナがトリガーされる前に、関連するすべてのレコードが確実に作成されるようにする必要がある場合に特に便利です。

イベントを延期するには、`Event::defer()` メソッドにクロージャーを提供します。

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

クロージャ内でトリガーされたすべてのイベントは、クロージャの実行後にディスパッチされます。これにより、イベント リスナは遅延実行中に作成されたすべての関連レコードにアクセスできるようになります。クロージャー内で例外が発生した場合、遅延イベントはディスパッチされません。

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
## イベント購読者 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### イベントサブスクライバの書き込み

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
### イベントサブスクライバの登録

サブスクライバを作成した後、Laravel の [イベント検出の規則](#event-discovery) に従っている場合、Laravel はサブスクライバ内にハンドラー メソッドを自動的に登録します。それ以外の場合は、`Event` ファサードの `subscribe` メソッドを使用してサブスクライバを手動で登録できます。通常、これはアプリケーションの `AppServiceProvider` の `boot` メソッド内で行う必要があります。

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
## テスト (Testing)

イベントを送出するコードをテストする場合、リスナのコードは、対応するイベントを送出するコードとは別に直接テストできるため、イベントのリスナを実際に実行しないように Laravel に指示することもできます。もちろん、リスナ自体をテストするには、リスナ インスタンスをインスタンス化し、テスト内で `handle` メソッドを直接呼び出します。

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

特定の「真実テスト」に合格するイベントがディスパッチされたことをアサートするために、`assertDispatched` メソッドまたは `assertNotDispatched` メソッドにクロージャーを渡すことができます。指定された真実テストに合格する少なくとも 1 つのイベントがディスパッチされた場合、アサーションは成功します。

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

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
### イベントのサブセットを偽装する

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

`except` メソッドを使用すると、指定されたイベントのセットを除くすべてのイベントを偽装できます。

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### スコープ指定されたイベントのフェイク

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

