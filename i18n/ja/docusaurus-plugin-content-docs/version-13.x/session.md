<!-- # HTTP Session -->
# HTTP Session

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Interacting With the Session](#interacting-with-the-session)
    - [Retrieving Data](#retrieving-data)
    - [Storing Data](#storing-data)
    - [Flash Data](#flash-data)
    - [Deleting Data](#deleting-data)
    - [Regenerating the Session ID](#regenerating-the-session-id)
- [Session Cache](#session-cache)
- [Session Blocking](#session-blocking)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)
    - [Implementing the Driver](#implementing-the-driver)
    - [Registering the Driver](#registering-the-driver)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Since HTTP driven applications are stateless, sessions provide a way to store information about the user across multiple requests. That user information is typically placed in a persistent store / backend that can be accessed from subsequent requests. -->
HTTP 駆動のアプリケーションはステートレスであるため、セッションは複数のリクエストにわたってユーザーに関する情報を保存する方法を提供します。そのユーザー情報は通常、後続のリクエストからアクセスできる永続ストア/バックエンドに配置されます。

<!-- Laravel ships with a variety of session backends that are accessed through an expressive, unified API. Support for popular backends such as [Memcached](https://memcached.org), [Redis](https://redis.io), and databases is included. -->
Laravel には、表現力豊かな統合 API を通じてアクセスされるさまざまなセッション バックエンドが付属しています。 [Memcached](https://memcached.org)、[Redis](https://redis.io) などの一般的なバックエンドやデータベースのサポートが含まれています。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `database` session driver. -->
アプリケーションのセッション構成ファイルは、`config/session.php` に保存されます。このファイルで使用できるオプションを必ず確認してください。デフォルトでは、Laravel は `database` セッションドライバを使用するように構成されています。

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel includes a variety of drivers: -->
session `driver` 構成オプションは、各リクエストのセッション データが保存される場所を定義します。 Laravel にはさまざまなドライバが含まれています。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `file` - sessions are stored in `storage/framework/sessions`.
- `cookie` - sessions are stored in secure, encrypted cookies.
- `database` - sessions are stored in a relational database.
- `memcached` / `redis` - sessions are stored in one of these fast, cache-based stores.
- `dynamodb` - sessions are stored in AWS DynamoDB.
- `array` - sessions are stored in a PHP array and will not be persisted.
-->
- `file` - セッションは `storage/framework/sessions` に保存されます。
- `cookie` - セッションは安全な暗号化された Cookie に保存されます。
- `database` - セッションはリレーショナル データベースに保存されます。
- `memcached` / `redis` - セッションは、これらの高速なキャッシュベースのストアのいずれかに保存されます。
- `dynamodb` - セッションは AWS DynamoDB に保存されます。
- `array` - セッションは PHP 配列に保存され、永続化されません。

<!-- </div> -->
</div>

> [!NOTE]
> アレイ ドライバは主に [testing](/docs/13.x/testing) 中に使用され、セッションに保存されたデータが永続化されるのを防ぎます。

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to ensure that you have a database table to contain the session data. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` [database migration](/docs/13.x/migrations); however, if for any reason you do not have a `sessions` table, you may use the `make:session-table` Artisan command to generate this migration: -->
`database` セッション ドライバを使用する場合は、セッション データを含むデータベース テーブルがあることを確認する必要があります。通常、これはLaravelのデフォルトの`0001_01_01_000000_create_users_table.php` [database migration](/docs/13.x/migrations)に含まれています。ただし、何らかの理由で `sessions` テーブルがない場合は、`make:session-table` Artisan コマンドを使用してこの移行を生成できます。

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/13.x/redis#configuration). -->
Laravel で Redis セッションを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~1.0) をインストールする必要があります。 Redis の構成の詳細については、Laravel の [Redis documentation](/docs/13.x/redis#configuration) を参照してください。

> [!NOTE]
> `SESSION_CONNECTION` 環境変数、または `session.php` 構成ファイルの `connection` オプションを使用して、セッション ストレージに使用する Redis 接続を指定できます。

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With the Session -->
## Interacting With the Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/13.x/container): -->
Laravel でセッション データを操作するには、主に 2 つの方法があります。グローバル `session` ヘルパを使用する方法と、`Request` インスタンスを使用する方法です。まず、`Request` インスタンスを介してセッションにアクセスする方法を見てみましょう。これは、ルート クロージャまたはコントローラ メソッドでタイプヒントを指定できます。コントローラメソッドの依存関係は、Laravel [service container](/docs/13.x/container) 経由で自動的に挿入されることに注意してください。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(Request $request, string $id): View
    {
        $value = $request->session()->get('key');

        // ...

        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

<!-- When you retrieve an item from the session, you may also pass a default value as the second argument to the `get` method. This default value will be returned if the specified key does not exist in the session. If you pass a closure as the default value to the `get` method and the requested key does not exist, the closure will be executed and its result returned: -->
セッションから項目を取得するときは、`get` メソッドの 2 番目の引数としてデフォルト値を渡すこともできます。指定されたキーがセッションに存在しない場合、このデフォルト値が返されます。クロージャをデフォルト値として `get` メソッドに渡し、要求されたキーが存在しない場合、クロージャが実行され、その結果が返されます。

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
<!-- #### The Global Session Helper -->
#### The Global Session Helper

<!-- You may also use the global `session` PHP function to retrieve and store data in the session. When the `session` helper is called with a single, string argument, it will return the value of that session key. When the helper is called with an array of key / value pairs, those values will be stored in the session: -->
グローバル `session` PHP 関数を使用して、セッション内のデータを取得および保存することもできます。 `session` ヘルパが単一の文字列引数で呼び出されると、そのセッション キーの値が返されます。キーと値のペアの配列を使用してヘルパが呼び出される場合、それらの値はセッションに保存されます。

```php
Route::get('/home', function () {
    // Retrieve a piece of data from the session...
    $value = session('key');

    // Specifying a default value...
    $value = session('key', 'default');

    // Store a piece of data in the session...
    session(['key' => 'value']);
});
```

> [!NOTE]
> HTTP リクエスト インスタンス経由でセッションを使用する場合と、グローバル `session` ヘルパを使用する場合には、実質的な違いはほとんどありません。どちらのメソッドも、すべてのテスト ケースで使用できる `assertSessionHas` メソッドを介した [testable](/docs/13.x/testing) です。

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
セッション内のすべてのデータを取得したい場合は、`all` メソッドを使用できます。

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
<!-- #### Retrieving a Portion of the Session Data -->
#### Retrieving a Portion of the Session Data

<!-- The `only` and `except` methods may be used to retrieve a subset of the session data: -->
`only` メソッドと `except` メソッドを使用して、セッション データのサブセットを取得できます。

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining if an Item Exists in the Session -->
#### Determining if an Item Exists in the Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
項目がセッションに存在するかどうかを確認するには、`has` メソッドを使用できます。項目が存在し、`null` ではない場合、`has` メソッドは `true` を返します。

```php
if ($request->session()->has('users')) {
    // ...
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
アイテムがセッションに存在するかどうかを確認するには、その値が `null` であっても、`exists` メソッドを使用できます。

```php
if ($request->session()->exists('users')) {
    // ...
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is not present: -->
項目がセッション内に存在しないかどうかを確認するには、`missing` メソッドを使用できます。項目が存在しない場合、`missing` メソッドは `true` を返します。

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
セッションにデータを保存するには、通常、リクエスト インスタンスの `put` メソッドまたはグローバル `session` ヘルパを使用します。

```php
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
<!-- #### Pushing to Array Session Values -->
#### Pushing to Array Session Values

<!-- The `push` method may be used to push a new value onto a session value that is an array. For example, if the `user.teams` key contains an array of team names, you may push a new value onto the array like so: -->
`push` メソッドは、配列であるセッション値に新しい値をプッシュするために使用できます。たとえば、`user.teams` キーにチーム名の配列が含まれている場合、次のように新しい値を配列にプッシュできます。

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving and Deleting an Item -->
#### Retrieving and Deleting an Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` メソッドは、単一のステートメントでセッションから項目を取得して削除します。

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing and Decrementing Session Values -->
#### Incrementing and Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
セッション データに増加または減少させたい整数が含まれている場合は、`increment` メソッドと `decrement` メソッドを使用できます。

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
<!-- ### Flash Data -->
### Flash Data

<!-- Sometimes you may wish to store items in the session for the next request. You may do so using the `flash` method. Data stored in the session using this method will be available immediately and during the subsequent HTTP request. After the subsequent HTTP request, the flashed data will be deleted. Flash data is primarily useful for short-lived status messages: -->
場合によっては、次のリクエストに備えてセッションに項目を保存したい場合があります。これは、`flash` メソッドを使用して行うことができます。このメソッドを使用してセッションに保存されたデータは、後続の HTTP リクエスト中にすぐに使用できるようになります。後続の HTTP リクエストの後、フラッシュされたデータは削除されます。フラッシュ データは主に、短期間のステータス メッセージに役立ちます。

```php
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
複数のリクエストに対してフラッシュ データを保持する必要がある場合は、追加のリクエストに備えてすべてのフラッシュ データを保持する `reflash` メソッドを使用できます。特定のフラッシュ データのみを保持する必要がある場合は、`keep` メソッドを使用できます。

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
現在のリクエストに対してのみフラッシュ データを保持するには、`now` メソッドを使用できます。

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` メソッドは、セッションからデータの一部を削除します。セッションからすべてのデータを削除したい場合は、`flush` メソッドを使用できます。

```php
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
<!-- ### Regenerating the Session ID -->
### Regenerating the Session ID

<!-- Regenerating the session ID is often done in order to prevent malicious users from exploiting a [session fixation](https://owasp.org/www-community/attacks/Session_fixation) attack on your application. -->
セッション ID の再生成は、悪意のあるユーザーがアプリケーションに対して [session fixation](https://owasp.org/www-community/attacks/Session_fixation) 攻撃を悪用するのを防ぐために行われることがよくあります。

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/13.x/starter-kits) or [Laravel Fortify](/docs/13.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel [application starter kits](/docs/13.x/starter-kits) または [Laravel Fortify](/docs/13.x/fortify) のいずれかを使用している場合、Laravel は認証中にセッション ID を自動的に再生成します。ただし、セッション ID を手動で再生成する必要がある場合は、`regenerate` メソッドを使用できます。

```php
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
単一のステートメントでセッション ID を再生成し、セッションからすべてのデータを削除する必要がある場合は、`invalidate` メソッドを使用できます。

```php
$request->session()->invalidate();
```

<a name="session-cache"></a>
<!-- ## Session Cache -->
## Session Cache

<!-- Laravel's session cache provides a convenient way to cache data that is scoped to an individual user session. Unlike the global application cache, session cache data is automatically isolated per session and is cleaned up when the session expires or is destroyed. The session cache supports all the familiar [Laravel cache methods](/docs/13.x/cache) like `get`, `put`, `remember`, `forget`, and more, but scoped to the current session. -->
Laravel のセッション キャッシュは、個々のユーザー セッションをスコープとするデータをキャッシュする便利な方法を提供します。グローバル アプリケーション キャッシュとは異なり、セッション キャッシュ データはセッションごとに自動的に分離され、セッションが期限切れになるか破棄されるとクリーンアップされます。セッション キャッシュは、`get`、`put`、`remember`、`forget` などのよく知られたすべての [Laravel cache methods](/docs/13.x/cache) をサポートしますが、スコープは現在のセッションに限定されます。

<!-- The session cache is perfect for storing temporary, user-specific data that you want to persist across multiple requests within the same session, but don't need to store permanently. This includes things like form data, temporary calculations, API responses, or any other ephemeral data that should be tied to a specific user's session. -->
セッション キャッシュは、同じセッション内の複数のリクエストにわたって保持したいが、永続的に保存する必要はない一時的なユーザー固有のデータを保存するのに最適です。これには、フォーム データ、一時的な計算、API 応答、または特定のユーザーのセッションに関連付けられる必要があるその他の一時的なデータなどが含まれます。

<!-- You can access the session cache through the `cache` method on the session: -->
セッションの `cache` メソッドを通じてセッション キャッシュにアクセスできます。

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);
```

<!-- For more information on Laravel's cache methods, consult the [cache documentation](/docs/13.x/cache). -->
Laravel のキャッシュ メソッドの詳細については、[cache documentation](/docs/13.x/cache) を参照してください。

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!WARNING]
> セッション ブロッキングを利用するには、アプリケーションで [atomic locks](/docs/13.x/cache#atomic-locks) をサポートするキャッシュ ドライバを使用する必要があります。現在、これらのキャッシュ ドライバには、`memcached`、`dynamodb`、`redis`、`mongodb` (公式 `mongodb/laravel-mongodb` パッケージに含まれる)、`database`、`file`、および `array` ドライバが含まれます。また、`cookie` セッション ドライバは使用できません。

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
デフォルトでは、Laravel は同じセッションを使用したリクエストの同時実行を許可します。したがって、たとえば、JavaScript HTTP ライブラリを使用してアプリケーションに対して 2 つの HTTP リクエストを作成すると、両方が同時に実行されます。多くのアプリケーションでは、これは問題になりません。ただし、セッション データの損失は、両方ともセッションにデータを書き込む 2 つの異なるアプリケーション エンドポイントに同時にリクエストを行うアプリケーションの小さなサブセットで発生する可能性があります。

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
これを軽減するために、Laravel は特定のセッションの同時リクエストを制限できる機能を提供します。まず、`block` メソッドをルート定義にチェーンするだけです。この例では、`/profile` エンドポイントへの受信リクエストはセッション ロックを取得します。このロックが保持されている間、同じセッション ID を共有する `/profile` または `/order` エンドポイントへの受信リクエストは、最初のリクエストの実行が完了するまで待機してから、実行を続行します。

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` メソッドは 2 つのオプションの引数を受け入れます。 `block` メソッドで受け入れられる最初の引数は、セッション ロックが解放されるまで保持される最大秒数です。もちろん、この時間より前にリクエストの実行が終了した場合、ロックはより早く解放されます。

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
`block` メソッドで受け入れられる 2 番目の引数は、セッション ロックの取得を試行する際にリクエストが待機する秒数です。リクエストが指定された秒数以内にセッション ロックを取得できない場合、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
これらの引数のどちらも渡されない場合、ロックは最大 10 秒間取得され、リクエストはロックの取得を試行する間最大 10 秒待機します。

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
<!-- ## Adding Custom Session Drivers -->
## Adding Custom Session Drivers

<a name="implementing-the-driver"></a>
<!-- ### Implementing the Driver -->
### Implementing the Driver

<!-- If none of the existing session drivers fit your application's needs, Laravel makes it possible to write your own session handler. Your custom session driver should implement PHP's built-in `SessionHandlerInterface`. This interface contains just a few simple methods. A stubbed MongoDB implementation looks like the following: -->
既存のセッションドライバがアプリケーションのニーズに適合しない場合は、Laravel を使用して独自のセッションハンドラーを作成できます。カスタム セッション ドライバは、PHP の組み込み `SessionHandlerInterface` を実装する必要があります。このインターフェイスには、いくつかの簡単なメソッドが含まれています。スタブ化された MongoDB 実装は次のようになります。

```php
<?php

namespace App\Extensions;

class MongoSessionHandler implements \SessionHandlerInterface
{
    public function open($savePath, $sessionName) {}
    public function close() {}
    public function read($sessionId) {}
    public function write($sessionId, $data) {}
    public function destroy($sessionId) {}
    public function gc($lifetime) {}
}
```

<!-- Since Laravel does not include a default directory to house your extensions. You are free to place them anywhere you like. In this example, we have created an `Extensions` directory to house the `MongoSessionHandler`. -->
Laravel には拡張機能を格納するデフォルトのディレクトリが含まれていないためです。好きな場所に自由に配置できます。この例では、`MongoSessionHandler` を格納する `Extensions` ディレクトリを作成しました。

<!-- Since the purpose of these methods is not readily understandable, here is an overview of the purpose of each method: -->
これらのメソッドの目的はすぐには理解できないため、各メソッドの目的の概要を次に示します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will rarely need to put anything in this method. You can simply leave this method empty.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB or another storage system of your choice. Again, you should not perform any serialization - Laravel will have already handled that for you.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.
-->
- `open` メソッドは通常、ファイル ベースのセッション ストア システムで使用されます。 Laravel には `file` セッションドライバが同梱されているため、このメソッドに何も入れる必要はほとんどありません。このメソッドは空のままにすることができます。
- `close` メソッドも、`open` メソッドと同様に、通常は無視できます。ほとんどのドライバでは必要ありません。
- `read` メソッドは、指定された `$sessionId` に関連付けられたセッション データの文字列バージョンを返す必要があります。 Laravel がシリアル化を実行するため、ドライバでセッション データを取得または保存するときにシリアル化やその他のエンコードを行う必要はありません。
- `write` メソッドは、`$sessionId` に関連付けられた特定の `$data` 文字列を、MongoDB や選択した別のストレージ システムなどの永続ストレージ システムに書き込む必要があります。繰り返しますが、シリアル化を実行しないでください。Laravel がすでにシリアル化を処理します。
- `destroy` メソッドは、`$sessionId` に関連付けられたデータを永続ストレージから削除する必要があります。
- `gc` メソッドは、指定された `$lifetime` (UNIX タイムスタンプ) より古いセッション データをすべて破棄する必要があります。 Memcached や Redis などの自己期限切れシステムの場合、このメソッドは空のままにすることができます。

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/13.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/13.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
ドライバが実装されたら、Laravel に登録する準備が整います。 Laravel のセッション バックエンドに追加のドライバを追加するには、`Session` [facade](/docs/13.x/facades) によって提供される `extend` メソッドを使用できます。 [service provider](/docs/13.x/providers) の `boot` メソッドから `extend` メソッドを呼び出す必要があります。既存の `App\Providers\AppServiceProvider` からこれを行うことも、まったく新しいプロバイダを作成することもできます。

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Session::extend('mongo', function (Application $app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}
```

<!-- Once the session driver has been registered, you may specify the `mongo` driver as your application's session driver using the `SESSION_DRIVER` environment variable or within the application's `config/session.php` configuration file. -->
セッション ドライバが登録されたら、`SESSION_DRIVER` 環境変数を使用するか、アプリケーションの `config/session.php` 構成ファイル内で、アプリケーションのセッション ドライバとして `mongo` ドライバを指定できます。

