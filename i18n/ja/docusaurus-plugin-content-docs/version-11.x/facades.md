# ファサード (Facades)

- [Introduction](#introduction)
- [ファサードを使用する場合](#when-to-use-facades)
    - [ファサードと依存関係の注入](#facades-vs-dependency-injection)
    - [ファサードとヘルパ関数](#facades-vs-helper-functions)
- [ファサードの仕組み](#how-facades-work)
- [リアルタイムファサード](#real-time-facades)
- [ファサードクラスリファレンス](#facade-class-reference)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel ドキュメント全体を通して、「ファサード」を介して Laravel の機能と対話するコードの例が表示されます。ファサードは、アプリケーションの [サービスコンテナ](/docs/{{version}}/container) で使用できるクラスへの「静的」インターフェイスを提供します。 Laravel には、Laravel のほぼすべての機能へのアクセスを提供する多くのファサードが付属しています。

Laravel ファサードは、サービスコンテナ内の基礎となるクラスに対する「静的プロキシ」として機能し、従来の静的メソッドよりも高いテスト容易性と柔軟性を維持しながら、簡潔で表現力豊かな構文の利点を提供します。ファサードがどのように機能するかを完全に理解していなくても、まったく問題ありません。流れに身を任せて、Laravel について学び続けてください。

Laravel のファサードはすべて、`Illuminate\Support\Facades` 名前空間で定義されます。したがって、次のようにしてファサードに簡単にアクセスできます。

    use Illuminate\Support\Facades\Cache;
    use Illuminate\Support\Facades\Route;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

Laravel ドキュメント全体を通じて、例の多くはフレームワークのさまざまな機能を示すためにファサードを使用します。

<a name="helper-functions"></a>
#### ヘルパ関数

ファサードを補完するために、Laravel は一般的な Laravel 機能との対話をさらに容易にするさまざまなグローバル「ヘルパ関数」を提供します。操作できる一般的なヘルパ関数には、`view`、`response`、`url`、`config` などがあります。 Laravel が提供する各ヘルパ関数は、対応する機能とともに文書化されています。ただし、完全なリストは専用の [ヘルパのドキュメント](/docs/{{version}}/helpers) 内で入手できます。

たとえば、`Illuminate\Support\Facades\Response` ファサードを使用して JSON 応答を生成する代わりに、単に `response` 関数を使用することもできます。ヘルパ関数はグローバルに利用できるため、使用するためにクラスをインポートする必要はありません。

    use Illuminate\Support\Facades\Response;

    Route::get('/users', function () {
        return Response::json([
            // ...
        ]);
    });

    Route::get('/users', function () {
        return response()->json([
            // ...
        ]);
    });

<a name="when-to-use-facades"></a>
## ファサードを使用する場合 (When to Utilize Facades)

ファサードには多くの利点があります。これらは、手動で挿入または設定する必要がある長いクラス名を覚えなくても、Laravel の機能を使用できる簡潔で覚えやすい構文を提供します。さらに、PHP の動的メソッドを独自に使用しているため、テストが簡単です。

ただし、ファサードを使用する場合は注意が必要です。ファサードの主な危険は「スコープクリープ」クラスです。ファサードは非常に使いやすく、注入の必要がないため、クラスを成長させ続けて 1 つのクラスで多くのファサードを使用することも簡単です。依存関係の注入を使用すると、大規模なコンストラクターがクラスが大きくなりすぎていることを視覚的にフィードバックすることで、この可能性が軽減されます。したがって、ファサードを使用するときは、クラスの責任範囲が狭くならないように、クラスの規模に特に注意してください。クラスが大きくなりすぎる場合は、複数の小さなクラスに分割することを検討してください。

<a name="facades-vs-dependency-injection"></a>
### ファサードと依存関係の注入

依存注入の主な利点の 1 つは、注入されたクラスの実装を交換できることです。これは、モックまたはスタブを挿入し、スタブでさまざまなメソッドが呼び出されたことをアサートできるため、テスト中に役立ちます。

通常、真に静的なクラス メソッドをモックしたりスタブしたりすることはできません。ただし、ファサードは動的メソッドを使用して、サービスコンテナから解決されたオブジェクトへのメソッド呼び出しをプロキシするため、実際には、挿入されたクラス インスタンスをテストするのと同じようにファサードをテストできます。たとえば、次のルートがあるとします。

    use Illuminate\Support\Facades\Cache;

    Route::get('/cache', function () {
        return Cache::get('key');
    });

Laravel のファサード テスト メソッドを使用すると、次のテストを作成して、予想した引数を使用して `Cache::get` メソッドが呼び出されたことを確認できます。

```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}
```

<a name="facades-vs-helper-functions"></a>
### ファサードとヘルパ関数

ファサードに加えて、Laravel には、ビューの生成、イベントの起動、ジョブのディスパッチ、HTTP 応答の送信などの一般的なタスクを実行できるさまざまな「ヘルパ」関数が含まれています。これらのヘルパ関数の多くは、対応するファサードと同じ機能を実行します。たとえば、次のファサード呼び出しとヘルパ呼び出しは同等です。

    return Illuminate\Support\Facades\View::make('profile');

    return view('profile');

ファサードとヘルパ関数の間には実質的な違いはまったくありません。ヘルパ関数を使用する場合でも、対応するファサードとまったく同じようにテストできます。たとえば、次のルートがあるとします。

    Route::get('/cache', function () {
        return cache('key');
    });

`cache` ヘルパは、`Cache` ファサードの基礎となるクラスで `get` メソッドを呼び出します。したがって、ヘルパ関数を使用している場合でも、次のテストを作成して、メソッドが予期した引数で呼び出されたことを確認できます。

    use Illuminate\Support\Facades\Cache;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        Cache::shouldReceive('get')
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/cache');

        $response->assertSee('value');
    }

<a name="how-facades-work"></a>
## ファサードの仕組み (How Facades Work)

Laravel アプリケーションでは、ファサードはコンテナからオブジェクトへのアクセスを提供するクラスです。これを機能させる機械は、`Facade` クラスにあります。 Laravel のファサード、および作成するカスタム ファサードは、基本 `Illuminate\Support\Facades\Facade` クラスを拡張します。

`Facade` 基本クラスは、`__callStatic()` マジック メソッドを利用して、ファサードからコンテナーから解決されたオブジェクトへの呼び出しを延期します。以下の例では、Laravel キャッシュ システムへの呼び出しが行われます。このコードを一目見ると、静的 `get` メソッドが `Cache` クラスで呼び出されていると思われるかもしれません。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Support\Facades\Cache;
    use Illuminate\View\View;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         */
        public function showProfile(string $id): View
        {
            $user = Cache::get('user:'.$id);

            return view('profile', ['user' => $user]);
        }
    }

ファイルの先頭近くで、`Cache` ファサードを「インポート」していることに注目してください。このファサードは、`Illuminate\Contracts\Cache\Factory` インターフェイスの基礎となる実装にアクセスするためのプロキシとして機能します。ファサードを使用して行う呼び出しはすべて、Laravel のキャッシュ サービスの基礎となるインスタンスに渡されます。

その `Illuminate\Support\Facades\Cache` クラスを見ると、静的メソッド `get` がないことがわかります。

    class Cache extends Facade
    {
        /**
         * Get the registered name of the component.
         */
        protected static function getFacadeAccessor(): string
        {
            return 'cache';
        }
    }

代わりに、`Cache` ファサードは、基本 `Facade` クラスを拡張し、メソッド `getFacadeAccessor()` を定義します。このメソッドの仕事は、サービスコンテナ バインディングの名前を返すことです。ユーザーが`Cache`ファサードの静的メソッドを参照すると、Laravelは[サービスコンテナ](/docs/{{version}}/container)からの`cache`バインディングを解決し、そのオブジェクトに対して要求されたメソッド(この場合は`get`)を実行します。

<a name="real-time-facades"></a>
## リアルタイムファサード (Real-Time Facades)

リアルタイム ファサードを使用すると、アプリケーション内の任意のクラスをファサードであるかのように扱うことができます。これがどのように使用できるかを説明するために、まずリアルタイム ファサードを使用しないコードを調べてみましょう。たとえば、`Podcast` モデルに `publish` メソッドがあると仮定します。ただし、ポッドキャストを公開するには、`Publisher` インスタンスを挿入する必要があります。

    <?php

    namespace App\Models;

    use App\Contracts\Publisher;
    use Illuminate\Database\Eloquent\Model;

    class Podcast extends Model
    {
        /**
         * Publish the podcast.
         */
        public function publish(Publisher $publisher): void
        {
            $this->update(['publishing' => now()]);

            $publisher->publish($this);
        }
    }

パブリッシャー実装をメソッドに挿入すると、挿入されたパブリッシャーをモックできるため、メソッドを分離して簡単にテストできます。ただし、`publish` メソッドを呼び出すたびに、常にパブリッシャー インスタンスを渡す必要があります。リアルタイム ファサードを使用すると、`Publisher` インスタンスを明示的に渡す必要がなく、同じテスト容易性を維持できます。リアルタイム ファサードを生成するには、インポートされたクラスの名前空間に `Facades` というプレフィックスを付けます。

    <?php

    namespace App\Models;

    use App\Contracts\Publisher; // [tl! remove]
    use Facades\App\Contracts\Publisher; // [tl! add]
    use Illuminate\Database\Eloquent\Model;

    class Podcast extends Model
    {
        /**
         * Publish the podcast.
         */
        public function publish(Publisher $publisher): void // [tl! remove]
        public function publish(): void // [tl! add]
        {
            $this->update(['publishing' => now()]);

            $publisher->publish($this); // [tl! remove]
            Publisher::publish($this); // [tl! add]
        }
    }

リアルタイム ファサードが使用される場合、パブリッシャーの実装は、`Facades` プレフィックスの後に表示されるインターフェイスまたはクラス名の一部を使用して、サービスコンテナーから解決されます。テストするときは、Laravel の組み込みファサード テスト ヘルパを使用して、このメソッド呼び出しをモックできます。

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}
```

<a name="facade-class-reference"></a>
## ファサードクラスリファレンス (Facade Class Reference)

以下に、すべてのファサードとその基礎となるクラスが表示されます。これは、特定のファサード ルートの API ドキュメントをすばやく調べるのに便利なツールです。該当する場合、[サービスコンテナのバインディング](/docs/{{version}}/container) キーも含まれます。

<div class="overflow-auto">

| ファサード | クラス | サービスコンテナのバインド |
| --- | --- | --- |
| アプリ | [Illuminate\Foundation\Application](https://laravel.com/api/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://laravel.com/api/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| 認証 (インスタンス) | [Illuminate\Contracts\Auth\Guard](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| 認証 | [Illuminate\Auth\AuthManager](https://laravel.com/api/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://laravel.com/api/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| ブロードキャスト (インスタンス) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| 放送 | [Illuminate\Contracts\Broadcasting\Factory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| バス | [Illuminate\Contracts\Bus\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| キャッシュ(インスタンス) | [Illuminate\Cache\Repository](https://laravel.com/api/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| キャッシュ | [Illuminate\Cache\CacheManager](https://laravel.com/api/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| 構成 | [Illuminate\Config\Repository](https://laravel.com/api/{{version}}/Illuminate/Config/Repository.html) | `config` |
| コンテクスト | [Illuminate\Log\Context\Repository](https://laravel.com/api/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| クッキー | [Illuminate\Cookie\CookieJar](https://laravel.com/api/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| 地下室 | [Illuminate\Encryption\Encrypter](https://laravel.com/api/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| 日付 | [Illuminate\Support\DateFactory](https://laravel.com/api/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB（インスタンス） | [Illuminate\Database\Connection](https://laravel.com/api/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://laravel.com/api/{{version}}/Illuminate/Database/DatabaseManager.html) | `db` |
| イベント | [Illuminate\Events\Dispatcher](https://laravel.com/api/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| 例外 (インスタンス) | [Illuminate\Contracts\Debug\ExceptionHandler](https://laravel.com/api/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| 例外 | [Illuminate\Foundation\Exceptions\Handler](https://laravel.com/api/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| ファイル | [Illuminate\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| ゲート | [Illuminate\Contracts\Auth\Access\Gate](https://laravel.com/api/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| ハッシュ | [Illuminate\Contracts\Hashing\Hasher](https://laravel.com/api/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| HTTP | [Illuminate\Http\Client\Factory](https://laravel.com/api/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
| ラング | [Illuminate\Translation\Translator](https://laravel.com/api/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| ログ | [Illuminate\Log\LogManager](https://laravel.com/api/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| 郵便 | [Illuminate\Mail\Mailer](https://laravel.com/api/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| 通知 | [Illuminate\Notifications\ChannelManager](https://laravel.com/api/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| パスワード(インスタンス) | [Illuminate\Auth\Passwords\PasswordBroker](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| パスワード | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://laravel.com/api/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| パイプライン (インスタンス) | [Illuminate\Pipeline\Pipeline](https://laravel.com/api/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| プロセス | [Illuminate\Process\Factory](https://laravel.com/api/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
| キュー (基本クラス) | [Illuminate\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
| キュー (インスタンス) | [Illuminate\Contracts\Queue\Queue](https://laravel.com/api/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| 列 | [Illuminate\Queue\QueueManager](https://laravel.com/api/{{version}}/Illuminate/Queue/QueueManager.html) | `queue` |
| レートリミッター | [Illuminate\Cache\RateLimiter](https://laravel.com/api/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| リダイレクト | [Illuminate\Routing\Redirector](https://laravel.com/api/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (インスタンス) | [Illuminate\Redis\Connections\Connection](https://laravel.com/api/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| レディス | [Illuminate\Redis\RedisManager](https://laravel.com/api/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| リクエスト | [Illuminate\Http\Request](https://laravel.com/api/{{version}}/Illuminate/Http/Request.html) | `request` |
| 応答 (インスタンス) | [Illuminate\Http\Response](https://laravel.com/api/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| 応答 | [Illuminate\Contracts\Routing\ResponseFactory](https://laravel.com/api/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| ルート | [Illuminate\Routing\Router](https://laravel.com/api/{{version}}/Illuminate/Routing/Router.html) | `router` |
| スケジュール | [Illuminate\Console\Scheduling\Schedule](https://laravel.com/api/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| スキーマ | [Illuminate\Database\Schema\Builder](https://laravel.com/api/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| セッション（インスタンス） | [Illuminate\Session\Store](https://laravel.com/api/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| セッション | [Illuminate\Session\SessionManager](https://laravel.com/api/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| ストレージ (インスタンス) | [Illuminate\Contracts\Filesystem\Filesystem](https://laravel.com/api/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| ストレージ | [Illuminate\Filesystem\FilesystemManager](https://laravel.com/api/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://laravel.com/api/{{version}}/Illuminate/Routing/UrlGenerator.html) | `url` |
| バリデーター (インスタンス) | [Illuminate\Validation\Validator](https://laravel.com/api/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| バリデーター | [Illuminate\Validation\Factory](https://laravel.com/api/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| ビュー(インスタンス) | [Illuminate\View\View](https://laravel.com/api/{{version}}/Illuminate/View/View.html) | &nbsp; |
| ビュー | [Illuminate\View\Factory](https://laravel.com/api/{{version}}/Illuminate/View/Factory.html) | `view` |
| ヴィーテ | [Illuminate\Foundation\Vite](https://laravel.com/api/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>

