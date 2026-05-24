# 嘲笑する (Mocking)

- [Introduction](#introduction)
- [オブジェクトのモック化](#mocking-objects)
- [モッキングファサード](#mocking-facades)
    - [ファサードスパイ](#facade-spies)
- [バスフェイク](#bus-fake)
    - [ジョブチェーン](#bus-job-chains)
    - [ジョブバッチ](#job-batches)
- [イベントフェイク](#event-fake)
    - [スコープ指定されたイベントのフェイク](#scoped-event-fakes)
- [HTTPフェイク](#http-fake)
- [偽メール](#mail-fake)
- [偽の通知](#notification-fake)
- [フェイクをキューに入れる](#queue-fake)
    - [ジョブチェーン](#job-chains)
- [ストレージフェイク](#storage-fake)
- [時間との相互作用](#interacting-with-time)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel アプリケーションをテストするとき、アプリケーションの特定の側面を「モック」して、特定のテスト中に実際には実行されないようにしたい場合があります。たとえば、イベントを送出するコントローラをテストする場合、イベント リスナをモックして、テスト中にイベント リスナが実際に実行されないようにすることができます。これにより、イベント リスナは独自のテスト ケースでテストできるため、イベント リスナの実行を気にせずにコントローラの HTTP 応答のみをテストできます。

Laravel は、イベント、ジョブ、その他のファサードをすぐにモックするための便利なメソッドを提供します。これらのヘルパは主に Mockery 上の便利なレイヤーを提供するため、複雑な Mockery メソッド呼び出しを手動で行う必要はありません。

<a name="mocking-objects"></a>
## オブジェクトのモック化 (Mocking Objects)

Laravel の [サービスコンテナ](/docs/{{version}}/container) 経由でアプリケーションに挿入されるオブジェクトをモックする場合、モックされたインスタンスを `instance` バインディングとしてコンテナにバインドする必要があります。これにより、オブジェクト自体を構築する代わりに、オブジェクトのモックされたインスタンスを使用するようにコンテナーに指示されます。

    use App\Service;
    use Mockery;
    use Mockery\MockInterface;

    public function test_something_can_be_mocked()
    {
        $this->instance(
            Service::class,
            Mockery::mock(Service::class, function (MockInterface $mock) {
                $mock->shouldReceive('process')->once();
            })
        );
    }

これをより便利にするために、Laravel の基本テスト ケース クラスによって提供される `mock` メソッドを使用できます。たとえば、次の例は上記の例と同等です。

    use App\Service;
    use Mockery\MockInterface;

    $mock = $this->mock(Service::class, function (MockInterface $mock) {
        $mock->shouldReceive('process')->once();
    });

オブジェクトのいくつかのメソッドのみをモックする必要がある場合は、`partialMock` メソッドを使用できます。モック化されていないメソッドは、呼び出されたときに通常どおり実行されます。

    use App\Service;
    use Mockery\MockInterface;

    $mock = $this->partialMock(Service::class, function (MockInterface $mock) {
        $mock->shouldReceive('process')->once();
    });

同様に、オブジェクトに対して [spy](http://docs.mockery.io/en/latest/reference/spies.html) を実行したい場合、Laravel の基本テスト ケース クラスは、`Mockery::spy` メソッドの便利なラッパーとして `spy` メソッドを提供します。スパイはモックに似ています。ただし、スパイはスパイとテスト対象のコード間のやり取りを記録するため、コードの実行後にアサーションを行うことができます。

    use App\Service;

    $spy = $this->spy(Service::class);

    // ...

    $spy->shouldHaveReceived('process');

<a name="mocking-facades"></a>
## モッキングファサード (Mocking Facades)

従来の静的メソッド呼び出しとは異なり、[facades](/docs/{{version}}/facades) ([リアルタイムのファサード](/docs/{{version}}/facades#real-time-facades) を含む) はモックされる可能性があります。これにより、従来の静的メソッドに比べて大きな利点が得られ、従来の依存注入を使用した場合と同じテスト容易性が得られます。テストする場合、コントローラの 1 つで発生する Laravel ファサードへの呼び出しをモックしたい場合があります。たとえば、次のコントローラ アクションを考えてみましょう。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * Retrieve a list of all users of the application.
         *
         * @return \Illuminate\Http\Response
         */
        public function index()
        {
            $value = Cache::get('key');

            //
        }
    }

`shouldReceive` メソッドを使用して、`Cache` ファサードへの呼び出しをモックできます。このメソッドは、[Mockery](https://github.com/padraic/mockery) モックのインスタンスを返します。ファサードは実際には Laravel [サービスコンテナ](/docs/{{version}}/container) によって解決および管理されるため、一般的な静的クラスよりもはるかにテストしやすくなっています。たとえば、`Cache` ファサードの `get` メソッドへの呼び出しをモックしてみましょう。

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Cache;
    use Tests\TestCase;

    class UserControllerTest extends TestCase
    {
        public function testGetIndex()
        {
            Cache::shouldReceive('get')
                        ->once()
                        ->with('key')
                        ->andReturn('value');

            $response = $this->get('/users');

            // ...
        }
    }

> **警告**
> `Request` ファサードを嘲笑しないでください。代わりに、テストを実行するときに、`get` や `post` などの必要な入力を [HTTP テスト方法](/docs/{{version}}/http-tests) に渡します。同様に、`Config` ファサードをモックする代わりに、テストで `Config::set` メソッドを呼び出します。

<a name="facade-spies"></a>
### ファサードスパイ

ファサードで [spy](http://docs.mockery.io/en/latest/reference/spies.html) を実行したい場合は、対応するファサードで `spy` メソッドを呼び出すことができます。スパイはモックに似ています。ただし、スパイはスパイとテスト対象のコード間のやり取りを記録するため、コードの実行後にアサーションを行うことができます。

    use Illuminate\Support\Facades\Cache;

    public function test_values_are_be_stored_in_cache()
    {
        Cache::spy();

        $response = $this->get('/');

        $response->assertStatus(200);

        Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
    }

<a name="bus-fake"></a>
## バスフェイク (Bus Fake)

ジョブをディスパッチするコードをテストするときは、通常、特定のジョブがディスパッチされたことをアサートする必要がありますが、実際にジョブをキューに入れたり実行したりすることはできません。これは、ジョブの実行は通常、別のテスト クラスでテストできるためです。

`Bus` ファサードの `fake` メソッドを使用して、ジョブがキューにディスパッチされるのを防ぐことができます。次に、テスト対象のコードを実行した後、`assertDispatched` メソッドと `assertNotDispatched` メソッドを使用して、アプリケーションがディスパッチしようとしたジョブを検査できます。

    <?php

    namespace Tests\Feature;

    use App\Jobs\ShipOrder;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Bus;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_orders_can_be_shipped()
        {
            Bus::fake();

            // Perform order shipping...

            // Assert that a job was dispatched...
            Bus::assertDispatched(ShipOrder::class);

            // Assert a job was not dispatched...
            Bus::assertNotDispatched(AnotherJob::class);

            // Assert that a job was dispatched synchronously...
            Bus::assertDispatchedSync(AnotherJob::class);

            // Assert that a job was not dispatched synchronously...
            Bus::assertNotDispatchedSync(AnotherJob::class);

            // Assert that a job was dispatched after the response was sent...
            Bus::assertDispatchedAfterResponse(AnotherJob::class);

            // Assert a job was not dispatched after response was sent...
            Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

            // Assert no jobs were dispatched...
            Bus::assertNothingDispatched();
        }
    }

特定の「真実テスト」に合格するジョブがディスパッチされたことを主張するために、利用可能なメソッドにクロージャを渡すことができます。指定された真実テストに合格する少なくとも 1 つのジョブがディスパッチされた場合、アサーションは成功します。たとえば、ジョブが特定の注文に対してディスパッチされたことを主張したい場合があります。

    Bus::assertDispatched(function (ShipOrder $job) use ($order) {
        return $job->order->id === $order->id;
    });

<a name="faking-a-subset-of-jobs"></a>
#### ジョブの一部を偽装する

特定のジョブがディスパッチされることだけを防ぎたい場合は、偽装するジョブを `fake` メソッドに渡すことができます。

    /**
     * Test order process.
     */
    public function test_orders_can_be_shipped()
    {
        Bus::fake([
            ShipOrder::class,
        ]);

        // ...
    }

`except` メソッドを使用すると、指定したジョブのセットを除くすべてのジョブを偽装できます。

    Bus::fake()->except([
        ShipOrder::class,
    ]);

<a name="bus-job-chains"></a>
### ジョブチェーン

`Bus` ファサードの `assertChained` メソッドを使用して、[仕事の連鎖](/docs/{{version}}/queues#job-chaining) がディスパッチされたことをアサートできます。 `assertChained` メソッドは、最初の引数としてチェーンされたジョブの配列を受け入れます。

    use App\Jobs\RecordShipment;
    use App\Jobs\ShipOrder;
    use App\Jobs\UpdateInventory;
    use Illuminate\Support\Facades\Bus;

    Bus::assertChained([
        ShipOrder::class,
        RecordShipment::class,
        UpdateInventory::class
    ]);

上の例でわかるように、チェーンされたジョブの配列は、ジョブのクラス名の配列である場合があります。ただし、実際のジョブ インスタンスの配列を提供することもできます。これを行うと、Laravel はジョブ インスタンスが同じクラスであり、アプリケーションによってディスパッチされたチェーン ジョブのプロパティ値が同じであることを確認します。

    Bus::assertChained([
        new ShipOrder,
        new RecordShipment,
        new UpdateInventory,
    ]);

<a name="job-batches"></a>
### ジョブバッチ

`Bus` ファサードの `assertBatched` メソッドを使用して、[ジョブのバッチ](/docs/{{version}}/queues#job-batching) がディスパッチされたことをアサートできます。 `assertBatched` メソッドに指定されたクロージャは、バッチ内のジョブを検査するために使用される `Illuminate\Bus\PendingBatch` のインスタンスを受け取ります。

    use Illuminate\Bus\PendingBatch;
    use Illuminate\Support\Facades\Bus;

    Bus::assertBatched(function (PendingBatch $batch) {
        return $batch->name == 'import-csv' &&
               $batch->jobs->count() === 10;
    });

<a name="testing-job-batch-interaction"></a>
#### ジョブ/バッチインタラクションのテスト

さらに、場合によっては、個々のジョブとその基礎となるバッチとの対話をテストする必要があるかもしれません。たとえば、ジョブがそのバッチのさらなる処理をキャンセルしたかどうかをテストする必要がある場合があります。これを実現するには、`withFakeBatch` メソッドを介してジョブに偽のバッチを割り当てる必要があります。 `withFakeBatch` メソッドは、ジョブ インスタンスと偽のバッチを含むタプルを返します。

    [$job, $batch] = (new ShipOrder)->withFakeBatch();

    $job->handle();

    $this->assertTrue($batch->cancelled());
    $this->assertEmpty($batch->added);

<a name="event-fake"></a>
## イベントフェイク (Event Fake)

イベントを送出するコードをテストするとき、イベントのリスナを実際に実行しないように Laravel に指示したい場合があります。 `Event` ファサードの `fake` メソッドを使用すると、リスナの実行を防止し、テスト対象のコードを実行してから、`assertDispatched`、`assertNotDispatched`、および `assertNothingDispatched` メソッドを使用してアプリケーションによってどのイベントがディスパッチされたかをアサートできます。

    <?php

    namespace Tests\Feature;

    use App\Events\OrderFailedToShip;
    use App\Events\OrderShipped;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Event;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * Test order shipping.
         */
        public function test_orders_can_be_shipped()
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

> **警告**
> `Event::fake()` を呼び出した後は、イベント リスナは実行されません。したがって、モデルの `creating` イベント中に UUID を作成するなど、イベントに依存するモデル ファクトリをテストで使用する場合は、ファクトリを使用した **後** で `Event::fake()` を呼び出す必要があります。

<a name="faking-a-subset-of-events"></a>
#### イベントのサブセットを偽装する

特定のイベント セットに対してのみイベント リスナを偽装したい場合は、それらを `fake` メソッドまたは `fakeFor` メソッドに渡すことができます。

    /**
     * Test order process.
     */
    public function test_orders_can_be_processed()
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
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Support\Facades\Event;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        /**
         * Test order process.
         */
        public function test_orders_can_be_processed()
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

<a name="http-fake"></a>
## HTTPフェイク (HTTP Fake)

`Http` ファサードの `fake` メソッドを使用すると、リクエストが行われたときにスタブ/ダミー応答を返すように HTTP クライアントに指示できます。偽装送信 HTTP リクエストの詳細については、[HTTP クライアントのテストに関するドキュメント](/docs/{{version}}/http-client#testing) を参照してください。

<a name="mail-fake"></a>
## 偽メール (Mail Fake)

`Mail` ファサードの `fake` メソッドを使用して、メールが送信されないようにすることができます。通常、メールの送信は、実際にテストしているコードとは無関係です。おそらく、Laravel が特定のメール可能ファイルを送信するように指示されたと主張するだけで十分です。

`Mail` ファサードの `fake` メソッドを呼び出した後、[mailables](/docs/{{version}}/mail) がユーザーに送信されるように指示されたことをアサートし、メール可能ファイルが受信したデータを検査することもできます。

    <?php

    namespace Tests\Feature;

    use App\Mail\OrderShipped;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Mail;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_orders_can_be_shipped()
        {
            Mail::fake();

            // Perform order shipping...

            // Assert that no mailables were sent...
            Mail::assertNothingSent();

            // Assert that a mailable was sent...
            Mail::assertSent(OrderShipped::class);

            // Assert a mailable was sent twice...
            Mail::assertSent(OrderShipped::class, 2);

            // Assert a mailable was not sent...
            Mail::assertNotSent(AnotherMailable::class);
        }
    }

バックグラウンドで配信のためにメール可能ファイルをキューに入れている場合は、`assertSent` の代わりに `assertQueued` メソッドを使用する必要があります。

    Mail::assertQueued(OrderShipped::class);

    Mail::assertNotQueued(OrderShipped::class);

    Mail::assertNothingQueued();

特定の「真実テスト」に合格したメール可能ファイルが送信されたことをアサートするために、`assertSent`、`assertNotSent`、`assertQueued`、または `assertNotQueued` メソッドにクロージャを渡すことができます。指定された真実テストに合格する少なくとも 1 つのメール可能ファイルが送信された場合、アサーションは成功します。

    Mail::assertSent(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

`Mail` ファサードのアサーション メソッドを呼び出すと、提供されたクロージャによって受け入れられるメール可能インスタンスは、メール可能を調べるための役立つメソッドを公開します。

    Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email) &&
               $mail->hasCc('...') &&
               $mail->hasBcc('...') &&
               $mail->hasReplyTo('...') &&
               $mail->hasFrom('...') &&
               $mail->hasSubject('...');
    });

メール可能インスタンスには、メール可能ファイルの添付ファイルを調べるための便利なメソッドもいくつか含まれています。

    use Illuminate\Mail\Mailables\Attachment;

    Mail::assertSent(OrderShipped::class, function ($mail) {
        return $mail->hasAttachment(
            Attachment::fromPath('/path/to/file')
                    ->as('name.pdf')
                    ->withMime('application/pdf')
        );
    });

    Mail::assertSent(OrderShipped::class, function ($mail) {
        return $mail->hasAttachment(
            Attachment::fromStorageDisk('s3', '/path/to/file')
        );
    });

    Mail::assertSent(OrderShipped::class, function ($mail) use ($pdfData) {
        return $mail->hasAttachment(
            Attachment::fromData(fn () => $pdfData, 'name.pdf')
        );
    });

メールが送信されなかったことを確認するには、`assertNotSent` と `assertNotQueued` という 2 つの方法があることに気づいたかもしれません。場合によっては、メールが送信されなかったり、キューに入れられたりしていないことを主張したい場合があります。これを実現するには、`assertNothingOutgoing` メソッドと `assertNotOutgoing` メソッドを使用できます。

    Mail::assertNothingOutgoing();

    Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
        return $mail->order->id === $order->id;
    });

<a name="testing-mailable-content"></a>
#### メール可能なコンテンツのテスト

特定のメール可能ファイルが特定のユーザーに「送信された」ことを確認するテストとは別に、メール可能ファイルのコンテンツをテストすることをお勧めします。メール可能ファイルのコンテンツをテストする方法については、[メール可能ファイルのテスト](/docs/{{version}}/mail#testing-mailables) のドキュメントを参照してください。

<a name="notification-fake"></a>
## 偽の通知 (Notification Fake)

`Notification` ファサードの `fake` メソッドを使用して、通知が送信されないようにすることができます。通常、通知の送信は、実際にテストしているコードとは無関係です。おそらく、Laravel が特定の通知を送信するように指示されたと主張するだけで十分です。

`Notification` ファサードの `fake` メソッドを呼び出した後、[notifications](/docs/{{version}}/notifications) がユーザーに送信されるように指示されたことをアサートし、通知で受信したデータを検査することもできます。

    <?php

    namespace Tests\Feature;

    use App\Notifications\OrderShipped;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Notification;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_orders_can_be_shipped()
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

            // Assert that a given number of notifications were sent...
            Notification::assertCount(3);
        }
    }

特定の「真実テスト」に合格する通知が送信されたことをアサートするために、`assertSentTo` メソッドまたは `assertNotSentTo` メソッドにクロージャを渡すことができます。指定された真実テストに合格する少なくとも 1 つの通知が送信された場合、アサーションは成功します。

    Notification::assertSentTo(
        $user,
        function (OrderShipped $notification, $channels) use ($order) {
            return $notification->order->id === $order->id;
        }
    );

<a name="on-demand-notifications"></a>
#### オンデマンド通知

テストしているコードが [オンデマンド通知](/docs/{{version}}/notifications#on-demand-notifications) を送信する場合、オンデマンド通知が `assertSentOnDemand` メソッド経由で送信されたことをテストできます。

    Notification::assertSentOnDemand(OrderShipped::class);

`assertSentOnDemand` メソッドの 2 番目の引数としてクロージャーを渡すことで、オンデマンド通知が正しい「ルート」アドレスに送信されたかどうかを判断できます。

    Notification::assertSentOnDemand(
        OrderShipped::class,
        function ($notification, $channels, $notifiable) use ($user) {
            return $notifiable->routes['mail'] === $user->email;
        }
    );

<a name="queue-fake"></a>
## フェイクをキューに入れる (Queue Fake)

`Queue` ファサードの `fake` メソッドを使用して、キューに入れられたジョブがキューにプッシュされるのを防ぐことができます。おそらく、キューに入れられたジョブ自体は別のテストクラスでテストされる可能性があるため、Laravel が特定のジョブをキューにプッシュするように指示されたと主張するだけで十分であると考えられます。

`Queue` ファサードの `fake` メソッドを呼び出した後、アプリケーションがジョブをキューにプッシュしようとしたことをアサートできます。

    <?php

    namespace Tests\Feature;

    use App\Jobs\AnotherJob;
    use App\Jobs\FinalJob;
    use App\Jobs\ShipOrder;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Support\Facades\Queue;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_orders_can_be_shipped()
        {
            Queue::fake();

            // Perform order shipping...

            // Assert that no jobs were pushed...
            Queue::assertNothingPushed();

            // Assert a job was pushed to a given queue...
            Queue::assertPushedOn('queue-name', ShipOrder::class);

            // Assert a job was pushed twice...
            Queue::assertPushed(ShipOrder::class, 2);

            // Assert a job was not pushed...
            Queue::assertNotPushed(AnotherJob::class);
        }
    }

特定の「真実テスト」に合格するジョブがプッシュされたことをアサートするために、`assertPushed` メソッドまたは `assertNotPushed` メソッドにクロージャーを渡すことができます。指定された真実テストに合格する少なくとも 1 つのジョブがプッシュされた場合、アサーションは成功します。

    Queue::assertPushed(function (ShipOrder $job) use ($order) {
        return $job->order->id === $order->id;
    });

他のジョブを通常どおり実行できるようにしながら、特定のジョブのみを偽装する必要がある場合は、偽装するジョブのクラス名を `fake` メソッドに渡すことができます。

    public function test_orders_can_be_shipped()
    {
        Queue::fake([
            ShipOrder::class,
        ]);
        
        // Perform order shipping...

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);
    }

<a name="job-chains"></a>
### ジョブチェーン

`Queue` ファサードの `assertPushedWithChain` メソッドと `assertPushedWithoutChain` メソッドを使用して、プッシュされたジョブのジョブ チェーンを検査できます。 `assertPushedWithChain` メソッドは、最初の引数としてプライマリ ジョブを受け入れ、2 番目の引数としてチェーン ジョブの配列を受け入れます。

    use App\Jobs\RecordShipment;
    use App\Jobs\ShipOrder;
    use App\Jobs\UpdateInventory;
    use Illuminate\Support\Facades\Queue;

    Queue::assertPushedWithChain(ShipOrder::class, [
        RecordShipment::class,
        UpdateInventory::class
    ]);

上の例でわかるように、チェーンされたジョブの配列は、ジョブのクラス名の配列である場合があります。ただし、実際のジョブ インスタンスの配列を提供することもできます。これを行うと、Laravel はジョブ インスタンスが同じクラスであり、アプリケーションによってディスパッチされたチェーン ジョブのプロパティ値が同じであることを確認します。

    Queue::assertPushedWithChain(ShipOrder::class, [
        new RecordShipment,
        new UpdateInventory,
    ]);

`assertPushedWithoutChain` メソッドを使用して、ジョブがチェーンなしでプッシュされたことをアサートできます。

    Queue::assertPushedWithoutChain(ShipOrder::class);

<a name="storage-fake"></a>
## ストレージフェイク (Storage Fake)

`Storage` ファサードの `fake` メソッドを使用すると、偽のディスクを簡単に生成でき、`Illuminate\Http\UploadedFile` クラスのファイル生成ユーティリティと組み合わせることで、ファイルのアップロードのテストが大幅に簡素化されます。例えば：

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Http\UploadedFile;
    use Illuminate\Support\Facades\Storage;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        public function test_albums_can_be_uploaded()
        {
            Storage::fake('photos');

            $response = $this->json('POST', '/photos', [
                UploadedFile::fake()->image('photo1.jpg'),
                UploadedFile::fake()->image('photo2.jpg')
            ]);

            // Assert one or more files were stored...
            Storage::disk('photos')->assertExists('photo1.jpg');
            Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

            // Assert one or more files were not stored...
            Storage::disk('photos')->assertMissing('missing.jpg');
            Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

            // Assert that a given directory is empty...
            Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
        }
    }

デフォルトでは、`fake` メソッドは一時ディレクトリ内のすべてのファイルを削除します。これらのファイルを保持したい場合は、代わりに「persistentFake」メソッドを使用できます。ファイルのアップロードのテストの詳細については、[ファイルのアップロードに関する HTTP テストのドキュメントの情報](/docs/{{version}}/http-tests#testing-file-uploads) を参照してください。

> **警告**
> `image` メソッドには、[GD拡張](https://www.php.net/manual/en/book.image.php) が必要です。

<a name="interacting-with-time"></a>
## 時間との相互作用 (Interacting With Time)

テスト時に、`now` や `Illuminate\Support\Carbon::now()` などのヘルパによって返される時間を変更する必要がある場合があります。ありがたいことに、Laravel の基本機能テスト クラスには、現在時刻を操作できるヘルパが含まれています。

    use Illuminate\Support\Carbon;

    public function testTimeCanBeManipulated()
    {
        // Travel into the future...
        $this->travel(5)->milliseconds();
        $this->travel(5)->seconds();
        $this->travel(5)->minutes();
        $this->travel(5)->hours();
        $this->travel(5)->days();
        $this->travel(5)->weeks();
        $this->travel(5)->years();

        // Freeze time and resume normal time after executing closure...
        $this->freezeTime(function (Carbon $time) {
            // ...
        });

        // Travel into the past...
        $this->travel(-5)->hours();

        // Travel to an explicit time...
        $this->travelTo(now()->subHours(6));

        // Return back to the present time...
        $this->travelBack();
    }

