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

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for many applications. If your application will be load balanced across multiple web servers, you should choose a centralized store that all servers can access, such as Redis or a database. -->
アプリケーションのセッション構成ファイルは、`config/session.php` に保存されます。このファイルで使用できるオプションを必ず確認してください。デフォルトでは、Laravel は `file` セッションドライバを使用するように構成されており、多くのアプリケーションで適切に機能します。アプリケーションが複数の Web サーバー間で負荷分散される場合は、Redis やデータベースなど、すべてのサーバーがアクセスできる集中ストアを選択する必要があります。

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel ships with several great drivers out of the box: -->
session `driver` 構成オプションは、各リクエストのセッション データが保存される場所を定義します。 Laravel には、すぐに使用できるいくつかの優れたドライバが同梱されています。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `file` - sessions are stored in `storage/framework/sessions`.
- `cookie` - sessions are stored in secure, encrypted cookies.
- `database` - sessions are stored in a relational database.
- `memcached` / `redis` - sessions are stored in one of these fast, cache based stores.
- `dynamodb` - sessions are stored in AWS DynamoDB.
- `array` - sessions are stored in a PHP array and will not be persisted.
-->
- `file` - セッションは `storage/framework/sessions` に保存されます。
- `cookie` - セッションは安全な暗号化された Cookie に保存されます。
- `database` - セッションはリレーショナル データベースに保存されます。
- `memcached` / `redis` - セッションは、これらの高速なキャッシュ ベースのストアのいずれかに保存されます。
- `dynamodb` - セッションは AWS DynamoDB に保存されます。
- `array` - セッションは PHP 配列に保存され、永続化されません。

<!-- </div> -->
</div>

> [!NOTE]
> アレイ ドライバは主に [testing](/docs/10.x/testing) 中に使用され、セッションに保存されたデータが永続化されるのを防ぎます。

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to create a table to contain the session records. An example `Schema` declaration for the table may be found below: -->
`database` セッション ドライバを使用する場合は、セッション レコードを含むテーブルを作成する必要があります。テーブルの `Schema` 宣言の例を以下に示します。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('sessions', function (Blueprint $table) {
    $table->string('id')->primary();
    $table->foreignId('user_id')->nullable()->index();
    $table->string('ip_address', 45)->nullable();
    $table->text('user_agent')->nullable();
    $table->text('payload');
    $table->integer('last_activity')->index();
});
```

<!-- You may use the `session:table` Artisan command to generate this migration. To learn more about database migrations, you may consult the complete [migration documentation](/docs/10.x/migrations): -->
`session:table` Artisan コマンドを使用して、この移行を生成できます。データベース移行の詳細については、完全な [migration documentation](/docs/10.x/migrations) を参照してください。

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/10.x/redis#configuration). -->
Laravel で Redis セッションを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~1.0) をインストールする必要があります。 Redis の構成の詳細については、Laravel の [Redis documentation](/docs/10.x/redis#configuration) を参照してください。

> [!NOTE]
> `session` 構成ファイルでは、`connection` オプションを使用して、セッションで使用される Redis 接続を指定できます。

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With the Session -->
## Interacting With the Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/10.x/container): -->
Laravel でセッション データを操作するには、主に 2 つの方法があります。グローバル `session` ヘルパを使用する方法と、`Request` インスタンスを使用する方法です。まず、`Request` インスタンスを介してセッションにアクセスする方法を見てみましょう。これは、ルート クロージャまたはコントローラ メソッドでタイプヒントを指定できます。コントローラメソッドの依存関係は、Laravel [service container](/docs/10.x/container) 経由で自動的に挿入されることに注意してください。

```
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

```
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

```
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
> HTTP リクエスト インスタンス経由でセッションを使用する場合と、グローバル `session` ヘルパを使用する場合には、実質的な違いはほとんどありません。どちらのメソッドも、すべてのテスト ケースで使用できる `assertSessionHas` メソッドを介した [testable](/docs/10.x/testing) です。

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
セッション内のすべてのデータを取得したい場合は、`all` メソッドを使用できます。

```
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
<!-- #### Retrieving a Portion of the Session Data -->
#### Retrieving a Portion of the Session Data

<!-- The `only` and `except` methods may be used to retrieve a subset of the session data: -->
`only` メソッドと `except` メソッドを使用して、セッション データのサブセットを取得できます。

```
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining if an Item Exists in the Session -->
#### Determining if an Item Exists in the Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
項目がセッションに存在するかどうかを確認するには、`has` メソッドを使用できます。項目が存在し、`null` ではない場合、`has` メソッドは `true` を返します。

```
if ($request->session()->has('users')) {
    // ...
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
アイテムがセッションに存在するかどうかを確認するには、その値が `null` であっても、`exists` メソッドを使用できます。

```
if ($request->session()->exists('users')) {
    // ...
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is not present: -->
項目がセッション内に存在しないかどうかを確認するには、`missing` メソッドを使用できます。項目が存在しない場合、`missing` メソッドは `true` を返します。

```
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
セッションにデータを保存するには、通常、リクエスト インスタンスの `put` メソッドまたはグローバル `session` ヘルパを使用します。

```
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

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving and Deleting an Item -->
#### Retrieving and Deleting an Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` メソッドは、単一のステートメントでセッションから項目を取得して削除します。

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing and Decrementing Session Values -->
#### Incrementing and Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
セッション データに増加または減少させたい整数が含まれている場合は、`increment` メソッドと `decrement` メソッドを使用できます。

```
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

```
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
複数のリクエストに対してフラッシュ データを保持する必要がある場合は、追加のリクエストに備えてすべてのフラッシュ データを保持する `reflash` メソッドを使用できます。特定のフラッシュ データのみを保持する必要がある場合は、`keep` メソッドを使用できます。

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
現在のリクエストに対してのみフラッシュ データを保持するには、`now` メソッドを使用できます。

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` メソッドは、セッションからデータの一部を削除します。セッションからすべてのデータを削除したい場合は、`flush` メソッドを使用できます。

```
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

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/10.x/starter-kits) or [Laravel Fortify](/docs/10.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel [application starter kits](/docs/10.x/starter-kits) または [Laravel Fortify](/docs/10.x/fortify) のいずれかを使用している場合、Laravel は認証中にセッション ID を自動的に再生成します。ただし、セッション ID を手動で再生成する必要がある場合は、`regenerate` メソッドを使用できます。

```
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
単一のステートメントでセッション ID を再生成し、セッションからすべてのデータを削除する必要がある場合は、`invalidate` メソッドを使用できます。

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!WARNING]
> セッション ブロッキングを利用するには、アプリケーションで [atomic locks](/docs/10.x/cache#atomic-locks) をサポートするキャッシュ ドライバを使用する必要があります。現在、これらのキャッシュ ドライバには、`memcached`、`dynamodb`、`redis`、`database`、`file`、および `array` ドライバが含まれます。また、`cookie` セッション ドライバは使用できません。

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
デフォルトでは、Laravel は同じセッションを使用したリクエストの同時実行を許可します。したがって、たとえば、JavaScript HTTP ライブラリを使用してアプリケーションに対して 2 つの HTTP リクエストを作成すると、両方が同時に実行されます。多くのアプリケーションでは、これは問題になりません。ただし、セッション データの損失は、両方ともセッションにデータを書き込む 2 つの異なるアプリケーション エンドポイントに同時にリクエストを行うアプリケーションの小さなサブセットで発生する可能性があります。

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
これを軽減するために、Laravel は特定のセッションの同時リクエストを制限できる機能を提供します。まず、`block` メソッドをルート定義にチェーンするだけです。この例では、`/profile` エンドポイントへの受信リクエストはセッション ロックを取得します。このロックが保持されている間、同じセッション ID を共有する `/profile` または `/order` エンドポイントへの受信リクエストは、最初のリクエストの実行が完了するまで待機してから、実行を続行します。

```
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` メソッドは 2 つのオプションの引数を受け入れます。 `block` メソッドで受け入れられる最初の引数は、セッション ロックが解放されるまで保持される最大秒数です。もちろん、この時間より前にリクエストの実行が終了した場合、ロックはより早く解放されます。

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
`block` メソッドで受け入れられる 2 番目の引数は、セッション ロックの取得を試行する際にリクエストが待機する秒数です。リクエストが指定された秒数以内にセッション ロックを取得できない場合、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
これらの引数のどちらも渡されない場合、ロックは最大 10 秒間取得され、リクエストはロックの取得を試行する間最大 10 秒待機します。

```
Route::post('/profile', function () {
    // ...
})->block()
```

<a name="adding-custom-session-drivers"></a>
<!-- ## Adding Custom Session Drivers -->
## Adding Custom Session Drivers

<a name="implementing-the-driver"></a>
<!-- ### Implementing the Driver -->
### Implementing the Driver

<!-- If none of the existing session drivers fit your application's needs, Laravel makes it possible to write your own session handler. Your custom session driver should implement PHP's built-in `SessionHandlerInterface`. This interface contains just a few simple methods. A stubbed MongoDB implementation looks like the following: -->
既存のセッションドライバがアプリケーションのニーズに適合しない場合は、Laravel を使用して独自のセッションハンドラーを作成できます。カスタム セッション ドライバは、PHP の組み込み `SessionHandlerInterface` を実装する必要があります。このインターフェイスには、いくつかの簡単なメソッドが含まれています。スタブ化された MongoDB 実装は次のようになります。

```
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

> [!NOTE]
> Laravel には、拡張機能を含めるディレクトリは付属していません。好きな場所に自由に配置できます。この例では、`MongoSessionHandler` を格納する `Extensions` ディレクトリを作成しました。

<!-- Since the purpose of these methods is not readily understandable, let's quickly cover what each of the methods do: -->
これらのメソッドの目的はすぐには理解できないため、各メソッドの機能を簡単に説明します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will rarely need to put anything in this method. You can simply leave this method empty.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB or another storage system of your choice.  Again, you should not perform any serialization - Laravel will have already handled that for you.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.
-->
- `open` メソッドは通常、ファイル ベースのセッション ストア システムで使用されます。 Laravel には `file` セッションドライバが同梱されているため、このメソッドに何も入れる必要はほとんどありません。このメソッドは空のままにすることができます。
- `close` メソッドも、`open` メソッドと同様に、通常は無視できます。ほとんどのドライバでは必要ありません。
- `read` メソッドは、指定された `$sessionId` に関連付けられたセッション データの文字列バージョンを返す必要があります。 Laravel がシリアル化を実行するため、ドライバでセッション データを取得または保存するときにシリアル化やその他のエンコードを行う必要はありません。
- `write` メソッドは、`$sessionId` に関連付けられた特定の `$data` 文字列を、MongoDB や選択した別のストレージ システムなどの永続ストレージ システムに書き込む必要があります。  繰り返しますが、シリアル化を実行しないでください。Laravel がすでにシリアル化を処理します。
- `destroy` メソッドは、`$sessionId` に関連付けられたデータを永続ストレージから削除する必要があります。
- `gc` メソッドは、指定された `$lifetime` (UNIX タイムスタンプ) より古いセッション データをすべて破棄する必要があります。 Memcached や Redis などの自己期限切れシステムの場合、このメソッドは空のままにすることができます。

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/10.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/10.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
ドライバが実装されたら、Laravel に登録する準備が整います。 Laravel のセッション バックエンドに追加のドライバを追加するには、`Session` [facade](/docs/10.x/facades) によって提供される `extend` メソッドを使用できます。 [service provider](/docs/10.x/providers) の `boot` メソッドから `extend` メソッドを呼び出す必要があります。既存の `App\Providers\AppServiceProvider` からこれを行うことも、まったく新しいプロバイダを作成することもできます。

```
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

<!-- Once the session driver has been registered, you may use the `mongo` driver in your `config/session.php` configuration file. -->
セッションドライバが登録されると、`config/session.php` 構成ファイルで `mongo` ドライバを使用できるようになります。

