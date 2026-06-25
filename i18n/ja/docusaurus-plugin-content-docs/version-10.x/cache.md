<!-- # Cache -->
# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
    - [Obtaining a Cache Instance](#obtaining-a-cache-instance)
    - [Retrieving Items From the Cache](#retrieving-items-from-the-cache)
    - [Storing Items in the Cache](#storing-items-in-the-cache)
    - [Removing Items From the Cache](#removing-items-from-the-cache)
    - [The Cache Helper](#the-cache-helper)
- [Atomic Locks](#atomic-locks)
    - [Driver Prerequisites](#lock-driver-prerequisites)
    - [Managing Locks](#managing-locks)
    - [Managing Locks Across Processes](#managing-locks-across-processes)
- [Adding Custom Cache Drivers](#adding-custom-cache-drivers)
    - [Writing the Driver](#writing-the-driver)
    - [Registering the Driver](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as [Memcached](https://memcached.org) or [Redis](https://redis.io). -->
アプリケーションによって実行されるデータの取得または処理タスクの中には、CPU に負荷がかかるものや、完了までに数秒かかるものもあります。この場合、同じデータに対する後続のリクエストですぐに取得できるように、取得したデータを一時的にキャッシュするのが一般的です。キャッシュされたデータは通常、[Memcached](https://memcached.org) や [Redis](https://redis.io) などの非常に高速なデータ ストアに保存されます。

<!-- Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application. -->
ありがたいことに、Laravel はさまざまなキャッシュ バックエンドに表現力豊かな統合 API を提供しており、その超高速データ取得を活用して Web アプリケーションを高速化できます。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache driver you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests. -->
アプリケーションのキャッシュ構成ファイルは、`config/cache.php` にあります。このファイルでは、アプリケーション全体でデフォルトで使用するキャッシュ ドライバを指定できます。 Laravel は、[Memcached](https://memcached.org)、[Redis](https://redis.io)、[DynamoDB](https://aws.amazon.com/dynamodb) などの一般的なキャッシュ バックエンドやリレーショナル データベースをそのままサポートしています。さらに、ファイル ベースのキャッシュ ドライバも利用でき、`array` および "null" キャッシュ ドライバは自動テストに便利なキャッシュ バックエンドを提供します。

<!-- The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects on the server's filesystem. For larger applications, it is recommended that you use a more robust driver such as Memcached or Redis. You may even configure multiple cache configurations for the same driver. -->
キャッシュ構成ファイルには、ファイル内に文書化されている他のさまざまなオプションも含まれているため、これらのオプションを必ず読んでください。デフォルトでは、Laravel は `file` キャッシュドライバを使用するように構成されており、シリアル化されたキャッシュされたオブジェクトがサーバーのファイルシステムに保存されます。大規模なアプリケーションの場合は、Memcached や Redis などのより堅牢なドライバを使用することをお勧めします。同じドライバに対して複数のキャッシュ構成を構成することもできます。

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to set up a table to contain the cache items. You'll find an example `Schema` declaration for the table below: -->
`database` キャッシュ ドライバを使用する場合は、キャッシュ アイテムを含むテーブルを設定する必要があります。以下の表に、`Schema` 宣言の例を示します。

```
Schema::create('cache', function (Blueprint $table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!NOTE]
> `php artisan cache:table` Artisan コマンドを使用して、適切なスキーマで移行を生成することもできます。

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached ドライバを使用するには、[Memcached PECL package](https://pecl.php.net/package/memcached) をインストールする必要があります。すべての Memcached サーバーを `config/cache.php` 構成ファイルにリストすることができます。このファイルには、すぐに使用できる `memcached.servers` エントリがすでに含まれています。

```
'memcached' => [
    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```

<!-- If needed, you may set the `host` option to a UNIX socket path. If you do this, the `port` option should be set to `0`: -->
必要に応じて、`host` オプションを UNIX ソケット パスに設定できます。これを行う場合、`port` オプションを `0` に設定する必要があります。

```
'memcached' => [
    [
        'host' => '/var/run/memcached/memcached.sock',
        'port' => 0,
        'weight' => 100
    ],
],
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. [Laravel Sail](/docs/10.x/sail) already includes this extension. In addition, official Laravel deployment platforms such as [Laravel Forge](https://forge.laravel.com) and [Laravel Vapor](https://vapor.laravel.com) have the PhpRedis extension installed by default. -->
Laravel で Redis キャッシュを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~1.0) をインストールする必要があります。 [Laravel Sail](/docs/10.x/sail) には、この拡張機能がすでに含まれています。さらに、[Laravel Forge](https://forge.laravel.com) や [Laravel Vapor](https://vapor.laravel.com) などの公式の Laravel デプロイメント プラットフォームには、デフォルトで PhpRedis 拡張機能がインストールされています。

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/10.x/redis#configuration). -->
Redis の構成の詳細については、[Laravel documentation page](/docs/10.x/redis#configuration) を参照してください。

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within your application's `cache` configuration file. -->
[DynamoDB](https://aws.amazon.com/dynamodb) キャッシュ ドライバを使用する前に、すべてのキャッシュ データを保存する DynamoDB テーブルを作成する必要があります。通常、このテーブルには `cache` という名前を付ける必要があります。ただし、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
このテーブルには、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.attributes.key` 構成項目の値に対応する名前を持つ文字列パーティション キーも必要です。デフォルトでは、パーティション キーの名前は `key` である必要があります。

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining a Cache Instance -->
### Obtaining a Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
キャッシュ ストア インスタンスを取得するには、`Cache` ファサードを使用できます。これは、このドキュメント全体で使用するものです。 `Cache` ファサードは、Laravel キャッシュ コントラクトの基礎となる実装への便利で簡潔なアクセスを提供します。

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
<!-- #### Accessing Multiple Cache Stores -->
#### Accessing Multiple Cache Stores

<!-- Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file: -->
`Cache` ファサードを使用すると、`store` メソッド経由でさまざまなキャッシュ ストアにアクセスできます。 `store` メソッドに渡されるキーは、`cache` 構成ファイルの `stores` 構成配列にリストされているストアの 1 つに対応する必要があります。

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From the Cache -->
### Retrieving Items From the Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
`Cache` ファサードの `get` メソッドは、キャッシュから項目を取得するために使用されます。項目がキャッシュに存在しない場合は、`null` が返されます。必要に応じて、項目が存在しない場合に返されるデフォルト値を指定する 2 番目の引数を `get` メソッドに渡すことができます。

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
クロージャをデフォルト値として渡すこともできます。指定された項目がキャッシュに存在しない場合は、クロージャの結果が返されます。クロージャーを渡すと、データベースまたは他の外部サービスからのデフォルト値の取得を延期できます。

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
<!-- #### Determining Item Existence -->
#### Determining Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` メソッドを使用して、アイテムがキャッシュに存在するかどうかを確認できます。項目が存在するが、その値が `null` である場合、このメソッドは `false` も返します。

```
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment` メソッドと `decrement` メソッドは、キャッシュ内の整数項目の値を調整するために使用できます。これらのメソッドはどちらも、項目の値を増減する量を示すオプションの 2 番目の引数を受け入れます。

```
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->addHours(4));

// Increment or decrement the value...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
<!-- #### Retrieve and Store -->
#### Retrieve and Store

<!-- Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. For example, you may wish to retrieve all users from the cache or, if they don't exist, retrieve them from the database and add them to the cache. You may do this using the `Cache::remember` method: -->
キャッシュから項目を取得したい場合がありますが、要求された項目が存在しない場合はデフォルト値を保存することもできます。たとえば、すべてのユーザーをキャッシュから取得したり、ユーザーが存在しない場合はデータベースから取得してキャッシュに追加したりすることができます。これは、`Cache::remember` メソッドを使用して実行できます。

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
項目がキャッシュに存在しない場合、`remember` メソッドに渡されたクロージャが実行され、その結果がキャッシュに配置されます。

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
`rememberForever` メソッドを使用して、キャッシュからアイテムを取得したり、アイテムが存在しない場合は永久に保存したりできます。

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve and Delete -->
#### Retrieve and Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
キャッシュから項目を取得してからその項目を削除する必要がある場合は、`pull` メソッドを使用できます。 `get` メソッドと同様に、項目がキャッシュに存在しない場合は `null` が返されます。

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items in the Cache -->
### Storing Items in the Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
`Cache` ファサードで `put` メソッドを使用して、アイテムをキャッシュに保存できます。

```
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
保管時間が `put` メソッドに渡されない場合、アイテムは無期限に保管されます。

```
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
秒数を整数として渡す代わりに、キャッシュされたアイテムの有効期限を表す `DateTime` インスタンスを渡すこともできます。

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
<!-- #### Store if Not Present -->
#### Store if Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` メソッドは、アイテムがキャッシュ ストアに存在しない場合にのみ、アイテムをキャッシュに追加します。項目が実際にキャッシュに追加される場合、メソッドは `true` を返します。それ以外の場合、メソッドは `false` を返します。 `add` メソッドはアトミック操作です。

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` メソッドを使用して、アイテムをキャッシュに永続的に保存できます。これらのアイテムは期限切れにならないため、`forget` メソッドを使用してキャッシュから手動で削除する必要があります。

```
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached ドライバを使用している場合、キャッシュがサイズ制限に達すると、「永久に」保存されている項目が削除される可能性があります。

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From the Cache -->
### Removing Items From the Cache

<!-- You may remove items from the cache using the `forget` method: -->
`forget` メソッドを使用して、キャッシュから項目を削除できます。

```
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
ゼロまたは負の有効期限秒数を指定してアイテムを削除することもできます。

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
`flush` メソッドを使用してキャッシュ全体をクリアできます。

```
Cache::flush();
```

> [!WARNING]
> キャッシュをフラッシュすると、設定されたキャッシュの「プレフィックス」が考慮されず、キャッシュからすべてのエントリが削除されます。他のアプリケーションによって共有されているキャッシュをクリアするときは、この点を慎重に検討してください。

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` ファサードの使用に加えて、グローバル `cache` 関数を使用して、キャッシュ経由でデータを取得および保存することもできます。単一の文字列引数を指定して `cache` 関数を呼び出すと、指定されたキーの値が返されます。

```
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
キーと値のペアの配列と有効期限を関数に指定すると、指定された期間、値がキャッシュに保存されます。

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
`cache` 関数を引数なしで呼び出すと、`Illuminate\Contracts\Cache\Factory` 実装のインスタンスが返され、他のキャッシュ メソッドを呼び出すことができます。

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> グローバル `cache` 関数の呼び出しをテストするときは、[testing the facade](/docs/10.x/mocking#mocking-facades) であるかのように `Cache::shouldReceive` メソッドを使用できます。

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="lock-driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="atomic-locks-prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to setup a table to contain your application's cache locks. You'll find an example `Schema` declaration for the table below: -->
`database` キャッシュ ドライバを使用する場合は、アプリケーションのキャッシュ ロックを含むテーブルをセットアップする必要があります。以下の表に、`Schema` 宣言の例を示します。

```
Schema::create('cache_locks', function (Blueprint $table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

> [!NOTE]
> `cache:table` Artisan コマンドを使用してデータベース ドライバのキャッシュ テーブルを作成した場合、そのコマンドによって作成された移行には、`cache_locks` テーブルの定義がすでに含まれています。

<a name="managing-locks"></a>
<!-- ### Managing Locks -->
### Managing Locks

<!-- Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Forge](https://forge.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method: -->
アトミック ロックを使用すると、競合状態を気にせずに分散ロックを操作できます。たとえば、[Laravel Forge](https://forge.laravel.com) はアトミック ロックを使用して、サーバー上で一度に 1 つのリモート タスクのみが実行されるようにします。 `Cache::lock` メソッドを使用してロックを作成および管理できます。

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
`get` メソッドはクロージャーも受け入れます。クロージャーが実行されると、Laravel は自動的にロックを解放します。

```
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock can not be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
リクエストした時点でロックが利用できない場合は、Laravel に指定した秒数待機するように指示できます。指定された制限時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

```
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock?->release();
}
```

<!-- The example above may be simplified by passing a closure to the `block` method. When a closure is passed to this method, Laravel will attempt to acquire the lock for the specified number of seconds and will automatically release the lock once the closure has been executed: -->
上記の例は、`block` メソッドにクロージャーを渡すことで簡略化できます。クロージャがこのメソッドに渡されると、Laravel は指定された秒数の間ロックの取得を試み、クロージャが実行されると自動的にロックを解放します。

```
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
場合によっては、あるプロセスでロックを取得し、別のプロセスでロックを解放したい場合があります。たとえば、Web リクエスト中にロックを取得し、そのリクエストによってトリガーされたキューに入れられたジョブの終了時にロックを解放したい場合があります。このシナリオでは、ジョブが指定されたトークンを使用してロックを再インスタンス化できるように、ロックのスコープ指定された「所有者トークン」をキューに入れられたジョブに渡す必要があります。

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
以下の例では、ロックが正常に取得された場合に、キューに入れられたジョブをディスパッチします。さらに、ロックの `owner` メソッドを介して、ロックの所有者トークンをキューに入れられたジョブに渡します。

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
アプリケーションの `ProcessPodcast` ジョブ内で、所有者トークンを使用してロックを復元および解放できます。

```
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
現在の所有者を考慮せずにロックを解放したい場合は、`forceRelease` メソッドを使用できます。

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
<!-- ## Adding Custom Cache Drivers -->
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
<!-- ### Writing the Driver -->
### Writing the Driver

<!-- To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/10.x/contracts). So, a MongoDB cache implementation might look something like this: -->
カスタム キャッシュ ドライバを作成するには、まず `Illuminate\Contracts\Cache\Store` [contract](/docs/10.x/contracts) を実装する必要があります。したがって、MongoDB キャッシュの実装は次のようになります。

```
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```

<!-- We just need to implement each of these methods using a MongoDB connection. For an example of how to implement each of these methods, take a look at the `Illuminate\Cache\MemcachedStore` in the [Laravel framework source code](https://github.com/laravel/framework). Once our implementation is complete, we can finish our custom driver registration by calling the `Cache` facade's `extend` method: -->
MongoDB 接続を使用してこれらの各メソッドを実装するだけです。これらの各メソッドの実装方法の例については、[Laravel framework source code](https://github.com/laravel/framework) の `Illuminate\Cache\MemcachedStore` を参照してください。実装が完了したら、`Cache` ファサードの `extend` メソッドを呼び出して、カスタム ドライバの登録を完了できます。

```
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> カスタム キャッシュ ドライバ コードをどこに配置するか迷っている場合は、`app` ディレクトリ内に `Extensions` 名前空間を作成できます。ただし、Laravel には厳格なアプリケーション構造はなく、好みに応じてアプリケーションを自由に編成できることに注意してください。

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class: -->
カスタム キャッシュ ドライバを Laravel に登録するには、`Cache` ファサードで `extend` メソッドを使用します。他のサービスプロバイダは `boot` メソッド内でキャッシュされた値を読み取ろうとする可能性があるため、`booting` コールバック内でカスタム ドライバを登録します。 `booting` コールバックを使用すると、アプリケーションのサービスプロバイダで `boot` メソッドが呼び出される直前、ただしすべてのサービスプロバイダで `register` メソッドが呼び出された後、カスタム ドライバが確実に登録されます。アプリケーションの `App\Providers\AppServiceProvider` クラスの `register` メソッド内に `booting` コールバックを登録します。

```
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```

<!-- The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/10.x/container). -->
`extend` メソッドに渡される最初の引数はドライバの名前です。これは、`config/cache.php` 構成ファイルの `driver` オプションに対応します。 2 番目の引数は、`Illuminate\Cache\Repository` インスタンスを返すクロージャです。クロージャには、[service container](/docs/10.x/container) のインスタンスである `$app` インスタンスが渡されます。

<!-- Once your extension is registered, update your `config/cache.php` configuration file's `driver` option to the name of your extension. -->
拡張機能が登録されたら、`config/cache.php` 構成ファイルの `driver` オプションを拡張機能の名前に更新します。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for the [events](/docs/10.x/events) fired by the cache. Typically, you should place these event listeners within your application's `App\Providers\EventServiceProvider` class: -->
すべてのキャッシュ操作でコードを実行するには、キャッシュによって起動される [events](/docs/10.x/events) をリッスンできます。通常、これらのイベント リスナはアプリケーションの `App\Providers\EventServiceProvider` クラス内に配置する必要があります。
```

use App\Listeners\LogCacheHit;
use App\Listeners\LogCacheMissed;
use App\Listeners\LogKeyForgotten;
use App\Listeners\LogKeyWritten;
use Illuminate\Cache\Events\CacheHit;
use Illuminate\Cache\Events\CacheMissed;
use Illuminate\Cache\Events\KeyForgotten;
use Illuminate\Cache\Events\KeyWritten;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    CacheHit::class => [
        LogCacheHit::class,
    ],

    CacheMissed::class => [
        LogCacheMissed::class,
    ],

    KeyForgotten::class => [
        LogKeyForgotten::class,
    ],

    KeyWritten::class => [
        LogKeyWritten::class,
    ],
];
```

