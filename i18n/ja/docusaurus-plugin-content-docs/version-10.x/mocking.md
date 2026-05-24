# 嘲笑する (Mocking)

- [Introduction](#introduction)
- [オブジェクトのモック化](#mocking-objects)
- [モッキングファサード](#mocking-facades)
    - [ファサードスパイ](#facade-spies)
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

    public function test_something_can_be_mocked(): void
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
         */
        public function index(): array
        {
            $value = Cache::get('key');

            return [
                // ...
            ];
        }
    }

`shouldReceive` メソッドを使用して、`Cache` ファサードへの呼び出しをモックできます。このメソッドは、[Mockery](https://github.com/padraic/mockery) モックのインスタンスを返します。ファサードは実際には Laravel [サービスコンテナ](/docs/{{version}}/container) によって解決および管理されるため、一般的な静的クラスよりもはるかにテストしやすくなっています。たとえば、`Cache` ファサードの `get` メソッドへの呼び出しをモックしてみましょう。

    <?php

    namespace Tests\Feature;

    use Illuminate\Support\Facades\Cache;
    use Tests\TestCase;

    class UserControllerTest extends TestCase
    {
        public function test_get_index(): void
        {
            Cache::shouldReceive('get')
                        ->once()
                        ->with('key')
                        ->andReturn('value');

            $response = $this->get('/users');

            // ...
        }
    }

> [!WARNING]  
> `Request` ファサードを嘲笑しないでください。代わりに、テストを実行するときに、`get` や `post` などの必要な入力を [HTTP テスト方法](/docs/{{version}}/http-tests) に渡します。同様に、`Config` ファサードをモックする代わりに、テストで `Config::set` メソッドを呼び出します。

<a name="facade-spies"></a>
### ファサードスパイ

ファサードで [spy](http://docs.mockery.io/en/latest/reference/spies.html) を実行したい場合は、対応するファサードで `spy` メソッドを呼び出すことができます。スパイはモックに似ています。ただし、スパイはスパイとテスト対象のコード間のやり取りを記録するため、コードの実行後にアサーションを行うことができます。

    use Illuminate\Support\Facades\Cache;

    public function test_values_are_be_stored_in_cache(): void
    {
        Cache::spy();

        $response = $this->get('/');

        $response->assertStatus(200);

        Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
    }

<a name="interacting-with-time"></a>
## 時間との相互作用 (Interacting With Time)

テスト時に、`now` や `Illuminate\Support\Carbon::now()` などのヘルパによって返される時間を変更する必要がある場合があります。ありがたいことに、Laravel の基本機能テスト クラスには、現在時刻を操作できるヘルパが含まれています。

    use Illuminate\Support\Carbon;

    public function test_time_can_be_manipulated(): void
    {
        // Travel into the future...
        $this->travel(5)->milliseconds();
        $this->travel(5)->seconds();
        $this->travel(5)->minutes();
        $this->travel(5)->hours();
        $this->travel(5)->days();
        $this->travel(5)->weeks();
        $this->travel(5)->years();

        // Travel into the past...
        $this->travel(-5)->hours();

        // Travel to an explicit time...
        $this->travelTo(now()->subHours(6));

        // Return back to the present time...
        $this->travelBack();
    }

さまざまなタイムトラベル方法にクロージャを提供することもできます。クロージャは、指定された時刻に時間を凍結して呼び出されます。クロージャーが実行されると、時間は通常どおりに再開されます。

    $this->travel(5)->days(function () {
        // Test something five days into the future...
    });
    
    $this->travelTo(now()->subDays(10), function () {
        // Test something during a given moment...
    });

`freezeTime` メソッドを使用して、現在時刻を固定することができます。同様に、`freezeSecond` メソッドは現在時刻をフリーズしますが、現在の秒の始まりをフリーズします。

    use Illuminate\Support\Carbon;

    // Freeze time and resume normal time after executing closure...
    $this->freezeTime(function (Carbon $time) {
        // ...
    });

    // Freeze time at the current second and resume normal time after executing closure...
    $this->freezeSecond(function (Carbon $time) {
        // ...
    })

ご想像のとおり、上記で説明した方法はすべて、ディスカッション フォーラムの非アクティブな投稿をロックするなど、時間に敏感なアプリケーションの動作をテストするのに主に役立ちます。

    use App\Models\Thread;
    
    public function test_forum_threads_lock_after_one_week_of_inactivity()
    {
        $thread = Thread::factory()->create();
        
        $this->travel(1)->week();
        
        $this->assertTrue($thread->isLockedByInactivity());
    }

