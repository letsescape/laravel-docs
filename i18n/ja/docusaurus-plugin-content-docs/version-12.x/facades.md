<!-- # Facades -->
# Facades

- [Introduction](#introduction)
- [When to Utilize Facades](#when-to-use-facades)
    - [Facades vs. Dependency Injection](#facades-vs-dependency-injection)
    - [Facades vs. Helper Functions](#facades-vs-helper-functions)
- [How Facades Work](#how-facades-work)
- [Real-Time Facades](#real-time-facades)
- [Facade Class Reference](#facade-class-reference)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Throughout the Laravel documentation, you will see examples of code that interacts with Laravel's features via "facades". Facades provide a "static" interface to classes that are available in the application's [service container](/docs/12.x/container). Laravel ships with many facades which provide access to almost all of Laravel's features. -->
Laravel ドキュメント全体を通して、「ファサード」を介して Laravel の機能と対話するコードの例が表示されます。ファサードは、アプリケーションの [service container](/docs/12.x/container) で使用できるクラスへの「静的」インターフェイスを提供します。 Laravel には、Laravel のほぼすべての機能へのアクセスを提供する多くのファサードが付属しています。

<!-- Laravel facades serve as "static proxies" to underlying classes in the service container, providing the benefit of a terse, expressive syntax while maintaining more testability and flexibility than traditional static methods. It's perfectly fine if you don't totally understand how facades work - just go with the flow and continue learning about Laravel. -->
Laravel ファサードは、サービスコンテナ内の基礎となるクラスに対する「静的プロキシ」として機能し、従来の静的メソッドよりも高いテスト容易性と柔軟性を維持しながら、簡潔で表現力豊かな構文の利点を提供します。ファサードがどのように機能するかを完全に理解していなくても、まったく問題ありません。流れに身を任せて、Laravel について学び続けてください。

<!-- All of Laravel's facades are defined in the `Illuminate\Support\Facades` namespace. So, we can easily access a facade like so: -->
Laravel のファサードはすべて、`Illuminate\Support\Facades` 名前空間で定義されます。したがって、次のようにしてファサードに簡単にアクセスできます。

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Throughout the Laravel documentation, many of the examples will use facades to demonstrate various features of the framework. -->
Laravel ドキュメント全体を通じて、例の多くはフレームワークのさまざまな機能を示すためにファサードを使用します。

<a name="helper-functions"></a>
<!-- #### Helper Functions -->
#### Helper Functions

<!-- To complement facades, Laravel offers a variety of global "helper functions" that make it even easier to interact with common Laravel features. Some of the common helper functions you may interact with are `view`, `response`, `url`, `config`, and more. Each helper function offered by Laravel is documented with their corresponding feature; however, a complete list is available within the dedicated [helper documentation](/docs/12.x/helpers). -->
ファサードを補完するために、Laravel は一般的な Laravel 機能との対話をさらに容易にするさまざまなグローバル「ヘルパ関数」を提供します。操作できる一般的なヘルパ関数には、`view`、`response`、`url`、`config` などがあります。 Laravel が提供する各ヘルパ関数は、対応する機能とともに文書化されています。ただし、完全なリストは専用の [helper documentation](/docs/12.x/helpers) 内で入手できます。

<!-- For example, instead of using the `Illuminate\Support\Facades\Response` facade to generate a JSON response, we may simply use the `response` function. Because helper functions are globally available, you do not need to import any classes in order to use them: -->
たとえば、`Illuminate\Support\Facades\Response` ファサードを使用して JSON 応答を生成する代わりに、単に `response` 関数を使用することもできます。ヘルパ関数はグローバルに利用できるため、使用するためにクラスをインポートする必要はありません。

```php
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
```

<a name="when-to-use-facades"></a>
<!-- ## When to Utilize Facades -->
## When to Utilize Facades

<!-- Facades have many benefits. They provide a terse, memorable syntax that allows you to use Laravel's features without remembering long class names that must be injected or configured manually. Furthermore, because of their unique usage of PHP's dynamic methods, they are easy to test. -->
ファサードには多くの利点があります。これらは、手動で挿入または設定する必要がある長いクラス名を覚えなくても、Laravel の機能を使用できる簡潔で覚えやすい構文を提供します。さらに、PHP の動的メソッドを独自に使用しているため、テストが簡単です。

<!-- However, some care must be taken when using facades. The primary danger of facades is class "scope creep". Since facades are so easy to use and do not require injection, it can be easy to let your classes continue to grow and use many facades in a single class. Using dependency injection, this potential is mitigated by the visual feedback a large constructor gives you that your class is growing too large. So, when using facades, pay special attention to the size of your class so that its scope of responsibility stays narrow. If your class is getting too large, consider splitting it into multiple smaller classes. -->
ただし、ファサードを使用する場合は注意が必要です。ファサードの主な危険は「スコープクリープ」クラスです。ファサードは非常に使いやすく、注入の必要がないため、クラスを成長させ続けて 1 つのクラスで多くのファサードを使用することも簡単です。依存関係の注入を使用すると、大規模なコンストラクターがクラスが大きくなりすぎていることを視覚的にフィードバックすることで、この可能性が軽減されます。したがって、ファサードを使用するときは、クラスの責任範囲が狭くならないように、クラスの規模に特に注意してください。クラスが大きくなりすぎる場合は、複数の小さなクラスに分割することを検討してください。

<a name="facades-vs-dependency-injection"></a>
<!-- ### Facades vs. Dependency Injection -->
### Facades vs. Dependency Injection

<!-- One of the primary benefits of dependency injection is the ability to swap implementations of the injected class. This is useful during testing since you can inject a mock or stub and assert that various methods were called on the stub. -->
依存注入の主な利点の 1 つは、注入されたクラスの実装を交換できることです。これは、モックまたはスタブを挿入し、スタブでさまざまなメソッドが呼び出されたことをアサートできるため、テスト中に役立ちます。

<!-- Typically, it would not be possible to mock or stub a truly static class method. However, since facades use dynamic methods to proxy method calls to objects resolved from the service container, we actually can test facades just as we would test an injected class instance. For example, given the following route: -->
通常、真に静的なクラス メソッドをモックしたりスタブしたりすることはできません。ただし、ファサードは動的メソッドを使用して、サービスコンテナから解決されたオブジェクトへのメソッド呼び出しをプロキシするため、実際には、挿入されたクラス インスタンスをテストするのと同じようにファサードをテストできます。たとえば、次のルートがあるとします。

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});
```

<!-- Using Laravel's facade testing methods, we can write the following test to verify that the `Cache::get` method was called with the argument we expected: -->
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
<!-- ### Facades vs. Helper Functions -->
### Facades vs. Helper Functions

<!-- In addition to facades, Laravel includes a variety of "helper" functions which can perform common tasks like generating views, firing events, dispatching jobs, or sending HTTP responses. Many of these helper functions perform the same function as a corresponding facade. For example, this facade call and helper call are equivalent: -->
ファサードに加えて、Laravel には、ビューの生成、イベントの起動、ジョブのディスパッチ、HTTP 応答の送信などの一般的なタスクを実行できるさまざまな「ヘルパ」関数が含まれています。これらのヘルパ関数の多くは、対応するファサードと同じ機能を実行します。たとえば、次のファサード呼び出しとヘルパ呼び出しは同等です。

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');
```

<!-- There is absolutely no practical difference between facades and helper functions. When using helper functions, you may still test them exactly as you would the corresponding facade. For example, given the following route: -->
ファサードとヘルパ関数の間には実質的な違いはまったくありません。ヘルパ関数を使用する場合でも、対応するファサードとまったく同じようにテストできます。たとえば、次のルートがあるとします。

```php
Route::get('/cache', function () {
    return cache('key');
});
```

<!-- The `cache` helper is going to call the `get` method on the class underlying the `Cache` facade. So, even though we are using the helper function, we can write the following test to verify that the method was called with the argument we expected: -->
`cache` ヘルパは、`Cache` ファサードの基礎となるクラスで `get` メソッドを呼び出します。したがって、ヘルパ関数を使用している場合でも、次のテストを作成して、メソッドが予期した引数で呼び出されたことを確認できます。

```php
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

<a name="how-facades-work"></a>
<!-- ## How Facades Work -->
## How Facades Work

<!-- In a Laravel application, a facade is a class that provides access to an object from the container. The machinery that makes this work is in the `Facade` class. Laravel's facades, and any custom facades you create, will extend the base `Illuminate\Support\Facades\Facade` class. -->
Laravel アプリケーションでは、ファサードはコンテナからオブジェクトへのアクセスを提供するクラスです。これを機能させる機械は、`Facade` クラスにあります。 Laravel のファサード、および作成するカスタム ファサードは、基本 `Illuminate\Support\Facades\Facade` クラスを拡張します。

<!-- The `Facade` base class makes use of the `__callStatic()` magic-method to defer calls from your facade to an object resolved from the container. In the example below, a call is made to the Laravel cache system. By glancing at this code, one might assume that the static `get` method is being called on the `Cache` class: -->
`Facade` 基本クラスは、`__callStatic()` マジック メソッドを利用して、ファサードからコンテナーから解決されたオブジェクトへの呼び出しを延期します。以下の例では、Laravel キャッシュ システムへの呼び出しが行われます。このコードを一目見ると、静的 `get` メソッドが `Cache` クラスで呼び出されていると思われるかもしれません。

```php
<?php

namespace App\Http\Controllers;

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
```

<!-- Notice that near the top of the file we are "importing" the `Cache` facade. This facade serves as a proxy for accessing the underlying implementation of the `Illuminate\Contracts\Cache\Factory` interface. Any calls we make using the facade will be passed to the underlying instance of Laravel's cache service. -->
ファイルの先頭近くで、`Cache` ファサードを「インポート」していることに注目してください。このファサードは、`Illuminate\Contracts\Cache\Factory` インターフェイスの基礎となる実装にアクセスするためのプロキシとして機能します。ファサードを使用して行う呼び出しはすべて、Laravel のキャッシュ サービスの基礎となるインスタンスに渡されます。

<!-- If we look at that `Illuminate\Support\Facades\Cache` class, you'll see that there is no static method `get`: -->
その `Illuminate\Support\Facades\Cache` クラスを見ると、静的メソッド `get` がないことがわかります。

```php
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
```

<!-- Instead, the `Cache` facade extends the base `Facade` class and defines the method `getFacadeAccessor()`. This method's job is to return the name of a service container binding. When a user references any static method on the `Cache` facade, Laravel resolves the `cache` binding from the [service container](/docs/12.x/container) and runs the requested method (in this case, `get`) against that object. -->
代わりに、`Cache` ファサードは、基本 `Facade` クラスを拡張し、メソッド `getFacadeAccessor()` を定義します。このメソッドの仕事は、サービスコンテナ バインディングの名前を返すことです。ユーザーが`Cache`ファサードの静的メソッドを参照すると、Laravelは[service container](/docs/12.x/container)からの`cache`バインディングを解決し、そのオブジェクトに対して要求されたメソッド(この場合は`get`)を実行します。

<a name="real-time-facades"></a>
<!-- ## Real-Time Facades -->
## Real-Time Facades

<!-- Using real-time facades, you may treat any class in your application as if it was a facade. To illustrate how this can be used, let's first examine some code that does not use real-time facades. For example, let's assume our `Podcast` model has a `publish` method. However, in order to publish the podcast, we need to inject a `Publisher` instance: -->
リアルタイム ファサードを使用すると、アプリケーション内の任意のクラスをファサードであるかのように扱うことができます。これがどのように使用できるかを説明するために、まずリアルタイム ファサードを使用しないコードを調べてみましょう。たとえば、`Podcast` モデルに `publish` メソッドがあると仮定します。ただし、ポッドキャストを公開するには、`Publisher` インスタンスを挿入する必要があります。

```php
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
```

<!-- Injecting a publisher implementation into the method allows us to easily test the method in isolation since we can mock the injected publisher. However, it requires us to always pass a publisher instance each time we call the `publish` method. Using real-time facades, we can maintain the same testability while not being required to explicitly pass a `Publisher` instance. To generate a real-time facade, prefix the namespace of the imported class with `Facades`: -->
パブリッシャー実装をメソッドに挿入すると、挿入されたパブリッシャーをモックできるため、メソッドを分離して簡単にテストできます。ただし、`publish` メソッドを呼び出すたびに、常にパブリッシャー インスタンスを渡す必要があります。リアルタイム ファサードを使用すると、`Publisher` インスタンスを明示的に渡す必要がなく、同じテスト容易性を維持できます。リアルタイム ファサードを生成するには、インポートされたクラスの名前空間に `Facades` というプレフィックスを付けます。

```php
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
```

<!-- When the real-time facade is used, the publisher implementation will be resolved out of the service container using the portion of the interface or class name that appears after the `Facades` prefix. When testing, we can use Laravel's built-in facade testing helpers to mock this method call: -->
リアルタイム ファサードが使用される場合、パブリッシャーの実装は、`Facades` プレフィックスの後に表示されるインターフェイスまたはクラス名の一部を使用して、サービスコンテナーから解決されます。テストするときは、Laravel の組み込みファサード テスト ヘルパを使用して、このメソッド呼び出しをモックできます。

```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

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
<!-- ## Facade Class Reference -->
## Facade Class Reference

<!-- Below you will find every facade and its underlying class. This is a useful tool for quickly digging into the API documentation for a given facade root. The [service container binding](/docs/12.x/container) key is also included where applicable. -->
以下に、すべてのファサードとその基礎となるクラスが表示されます。これは、特定のファサード ルートの API ドキュメントをすばやく調べるのに便利なツールです。該当する場合、[service container binding](/docs/12.x/container) キーも含まれます。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| ファサード | クラス | サービスコンテナのバインド |
| --- | --- | --- |
| アプリ | [Illuminate\Foundation\Application](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Application.html) | `app` |
| Artisan | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| 認証 (インスタンス) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| 認証 | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/12.x/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/12.x/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| ブロードキャスト (インスタンス) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| Broadcast | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| バス | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| キャッシュ(インスタンス) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/12.x/Illuminate/Cache/Repository.html) | `cache.store` |
| キャッシュ | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/12.x/Illuminate/Cache/CacheManager.html) | `cache` |
| 構成 | [Illuminate\Config\Repository](https://api.laravel.com/docs/12.x/Illuminate/Config/Repository.html) | `config` |
| コンテクスト | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/12.x/Illuminate/Log/Context/Repository.html) | &nbsp; |
| クッキー | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/12.x/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/12.x/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| 日付 | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/12.x/Illuminate/Support/DateFactory.html) | `date` |
| DB（インスタンス） | [Illuminate\Database\Connection](https://api.laravel.com/docs/12.x/Illuminate/Database/Connection.html) | `db.connection` |
| DB | [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/12.x/Illuminate/Database/DatabaseManager.html) | `db` |
| イベント | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/12.x/Illuminate/Events/Dispatcher.html) | `events` |
| 例外 (インスタンス) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| 例外 | [Illuminate\Foundation\Exceptions\Handler](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| ファイル | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/12.x/Illuminate/Filesystem/Filesystem.html) | `files` |
| ゲート | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| ハッシュ | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| HTTP | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/12.x/Illuminate/Http/Client/Factory.html) | &nbsp; |
| ラング | [Illuminate\Translation\Translator](https://api.laravel.com/docs/12.x/Illuminate/Translation/Translator.html) | `translator` |
| ログ | [Illuminate\Log\LogManager](https://api.laravel.com/docs/12.x/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/12.x/Illuminate/Mail/Mailer.html) | `mailer` |
| 通知 | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/12.x/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| パスワード(インスタンス) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/12.x/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| パスワード | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/12.x/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| パイプライン (インスタンス) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/12.x/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| プロセス | [Illuminate\Process\Factory](https://api.laravel.com/docs/12.x/Illuminate/Process/Factory.html) | &nbsp; |
| キュー (基本クラス) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/12.x/Illuminate/Queue/Queue.html) | &nbsp; |
| キュー (インスタンス) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
| Queue | [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/12.x/Illuminate/Queue/QueueManager.html) | `queue` |
| レートリミッター | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/12.x/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| リダイレクト | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/12.x/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis (インスタンス) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/12.x/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| レディス | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/12.x/Illuminate/Redis/RedisManager.html) | `redis` |
| リクエスト | [Illuminate\Http\Request](https://api.laravel.com/docs/12.x/Illuminate/Http/Request.html) | `request` |
| 応答 (インスタンス) | [Illuminate\Http\Response](https://api.laravel.com/docs/12.x/Illuminate/Http/Response.html) | &nbsp; |
| 応答 | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| ルート | [Illuminate\Routing\Router](https://api.laravel.com/docs/12.x/Illuminate/Routing/Router.html) | `router` |
| スケジュール | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/12.x/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| スキーマ | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/12.x/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| セッション（インスタンス） | [Illuminate\Session\Store](https://api.laravel.com/docs/12.x/Illuminate/Session/Store.html) | `session.store` |
| セッション | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/12.x/Illuminate/Session/SessionManager.html) | `session` |
| ストレージ (インスタンス) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/12.x/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| ストレージ | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/12.x/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
| URL | [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/12.x/Illuminate/Routing/UrlGenerator.html) | `url` |
| バリデーター (インスタンス) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/12.x/Illuminate/Validation/Validator.html) | &nbsp; |
| バリデーター | [Illuminate\Validation\Factory](https://api.laravel.com/docs/12.x/Illuminate/Validation/Factory.html) | `validator` |
| ビュー(インスタンス) | [Illuminate\View\View](https://api.laravel.com/docs/12.x/Illuminate/View/View.html) | &nbsp; |
| ビュー | [Illuminate\View\Factory](https://api.laravel.com/docs/12.x/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/12.x/Illuminate/Foundation/Vite.html) | &nbsp; |

<!-- </div> -->
</div>

