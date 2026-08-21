<!-- # Cache -->
# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
    - [Obtaining a Cache Instance](#obtaining-a-cache-instance)
    - [Retrieving Items From the Cache](#retrieving-items-from-the-cache)
    - [Storing Items in the Cache](#storing-items-in-the-cache)
    - [Extending Item Lifetime](#extending-item-lifetime)
    - [Removing Items From the Cache](#removing-items-from-the-cache)
    - [Cache Memoization](#cache-memoization)
    - [The Cache Helper](#the-cache-helper)
- [Cache Tags](#cache-tags)
    - [Storing Tagged Cache Items](#storing-tagged-cache-items)
    - [Accessing Tagged Cache Items](#accessing-tagged-cache-items)
    - [Removing Tagged Cache Items](#removing-tagged-cache-items)
- [Atomic Locks](#atomic-locks)
    - [Managing Locks](#managing-locks)
    - [Managing Locks Across Processes](#managing-locks-across-processes)
    - [Refreshing Locks](#refreshing-locks)
    - [Concurrency Limiting](#concurrency-limiting)
- [Cache Failover](#cache-failover)
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

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache store you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), relational databases, and filesystem disks out of the box. In addition, a file based cache driver is available, while `array` and `null` cache drivers provide convenient cache backends for your automated tests. -->
アプリケーションのキャッシュ構成ファイルは、`config/cache.php` にあります。このファイルでは、アプリケーション全体でデフォルトで使用するキャッシュ ストアを指定できます。 Laravel は、[Memcached](https://memcached.org)、[Redis](https://redis.io)、[DynamoDB](https://aws.amazon.com/dynamodb) などの一般的なキャッシュ バックエンド、リレーショナル データベース、ファイル システム ディスクをすぐにサポートします。さらに、ファイル ベースのキャッシュ ドライバも利用でき、`array` および `null` キャッシュ ドライバは自動テストに便利なキャッシュ バックエンドを提供します。

<!-- The cache configuration file also contains a variety of other options that you may review. By default, Laravel is configured to use the `database` cache driver, which stores the serialized, cached objects in your application's database. -->
キャッシュ構成ファイルには、検討できる他のさまざまなオプションも含まれています。デフォルトでは、Laravel は `database` キャッシュドライバを使用するように構成されており、シリアル化されたキャッシュされたオブジェクトがアプリケーションのデータベースに保存されます。

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need a database table to contain the cache data. Typically, this is included in Laravel's default `0001_01_01_000001_create_cache_table.php` [database migration](/docs/13.x/migrations); however, if your application does not contain this migration, you may use the `make:cache-table` Artisan command to create it: -->
`database` キャッシュ ドライバを使用する場合、キャッシュ データを含むデータベース テーブルが必要になります。通常、これはLaravelのデフォルトの `0001_01_01_000001_create_cache_table.php` [database migration](/docs/13.x/migrations)に含まれています。ただし、アプリケーションにこの移行が含まれていない場合は、`make:cache-table` Artisan コマンドを使用して移行を作成できます。

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached ドライバを使用するには、[Memcached PECL package](https://pecl.php.net/package/memcached) をインストールする必要があります。すべての Memcached サーバーを `config/cache.php` 構成ファイルにリストすることができます。このファイルには、すぐに使用できる `memcached.servers` エントリがすでに含まれています。

```php
'memcached' => [
    // ...

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

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package via Composer. [Laravel Sail](/docs/13.x/sail) already includes this extension. In addition, official Laravel application platforms such as [Laravel Cloud](https://cloud.laravel.com) and [Laravel Forge](https://forge.laravel.com) have the PhpRedis extension installed by default. -->
Laravel で Redis キャッシュを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージをインストールする必要があります。[Laravel Sail](/docs/13.x/sail) には、この拡張機能がすでに含まれています。さらに、[Laravel Cloud](https://cloud.laravel.com) や [Laravel Forge](https://forge.laravel.com) などの公式 Laravel アプリケーションプラットフォームには、デフォルトで PhpRedis 拡張機能がインストールされています。

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/13.x/redis#configuration). -->
Redis の構成の詳細については、[Laravel documentation page](/docs/13.x/redis#configuration) を参照してください。

<a name="storage"></a>
<!-- #### Storage -->
#### Storage

<!-- The `storage` cache driver allows you to store cached values on any of your application's configured [filesystem disks](/docs/13.x/filesystem). This can be useful when you want to use an existing disk, such as an S3 disk, as a key / value cache store: -->
`storage` キャッシュ ドライバを使用すると、アプリケーションの構成済み [filesystem disks](/docs/13.x/filesystem) にキャッシュされた値を保存できます。これは、S3 ディスクなどの既存のディスクをキー/値キャッシュ ストアとして使用する場合に便利です。

```php
'storage' => [
    'driver' => 'storage',
    'disk' => env('CACHE_STORAGE_DISK'),
    'path' => env('CACHE_STORAGE_PATH', 'framework/cache/data'),
],
```

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within the `cache` configuration file. The table name may also be set via the `DYNAMODB_CACHE_TABLE` environment variable. -->
[DynamoDB](https://aws.amazon.com/dynamodb) キャッシュ ドライバを使用する前に、すべてのキャッシュ データを保存する DynamoDB テーブルを作成する必要があります。通常、このテーブルには `cache` という名前を付ける必要があります。ただし、`cache` 構成ファイル内の `stores.dynamodb.table` 構成値の値に基づいてテーブルに名前を付ける必要があります。テーブル名は、`DYNAMODB_CACHE_TABLE` 環境変数を介して設定することもできます。

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
このテーブルには、アプリケーションの `cache` 構成ファイル内の `stores.dynamodb.attributes.key` 構成項目の値に対応する名前を持つ文字列パーティション キーも必要です。デフォルトでは、パーティション キーの名前は `key` である必要があります。

<!-- Typically, DynamoDB will not proactively remove expired items from a table. Therefore, you should [enable Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) on the table. When configuring the table's TTL settings, you should set the TTL attribute name to `expires_at`. -->
通常、DynamoDB は有効期限切れのアイテムをテーブルから積極的に削除しません。したがって、テーブル上で [enable Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) を実行する必要があります。テーブルの TTL 設定を構成するときは、TTL 属性名を `expires_at` に設定する必要があります。

<!-- Next, install the AWS SDK so that your Laravel application can communicate with DynamoDB: -->
次に、Laravel アプリケーションが DynamoDB と通信できるように AWS SDK をインストールします。

```shell
composer require aws/aws-sdk-php
```

<!-- In addition, you should ensure that values are provided for the DynamoDB cache store configuration options. Typically these options, such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, should be defined in your application's `.env` configuration file: -->
さらに、DynamoDB キャッシュ ストア設定オプションに値が指定されていることを確認する必要があります。通常、`AWS_ACCESS_KEY_ID` や `AWS_SECRET_ACCESS_KEY` などのオプションは、アプリケーションの `.env` 構成ファイルで定義する必要があります。

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```

<a name="mongodb"></a>
<!-- #### MongoDB -->
#### MongoDB

<!-- If you are using MongoDB, a `mongodb` cache driver is provided by the official `mongodb/laravel-mongodb` package and can be configured using a `mongodb` database connection. MongoDB supports TTL indexes, which can be used to automatically clear expired cache items. -->
MongoDB を使用している場合、`mongodb` キャッシュ ドライバは公式 `mongodb/laravel-mongodb` パッケージによって提供され、`mongodb` データベース接続を使用して構成できます。 MongoDB は TTL インデックスをサポートしており、期限切れのキャッシュ アイテムを自動的にクリアするために使用できます。

<!-- For more information on configuring MongoDB, please refer to the MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/). -->
MongoDB の構成の詳細については、MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) を参照してください。

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining a Cache Instance -->
### Obtaining a Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
キャッシュ ストア インスタンスを取得するには、`Cache` ファサードを使用できます。これは、このドキュメント全体で使用するものです。 `Cache` ファサードは、Laravel キャッシュ コントラクトの基礎となる実装への便利で簡潔なアクセスを提供します。

```php
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

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From the Cache -->
### Retrieving Items From the Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
`Cache` ファサードの `get` メソッドは、キャッシュから項目を取得するために使用されます。項目がキャッシュに存在しない場合は、`null` が返されます。必要に応じて、項目が存在しない場合に返されるデフォルト値を指定する 2 番目の引数を `get` メソッドに渡すことができます。

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
クロージャをデフォルト値として渡すこともできます。指定された項目がキャッシュに存在しない場合は、クロージャの結果が返されます。クロージャーを渡すと、データベースまたは他の外部サービスからのデフォルト値の取得を延期できます。

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
<!-- #### Determining Item Existence -->
#### Determining Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` メソッドを使用して、アイテムがキャッシュに存在するかどうかを確認できます。項目が存在するが、その値が `null` である場合、このメソッドは `false` も返します。

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment` メソッドと `decrement` メソッドは、キャッシュ内の整数項目の値を調整するために使用できます。これらのメソッドはどちらも、項目の値を増減する量を示すオプションの 2 番目の引数を受け入れます。

```php
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->plus(hours: 4));

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

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
項目がキャッシュに存在しない場合、`remember` メソッドに渡されたクロージャが実行され、その結果がキャッシュに配置されます。

<!-- If you need to know whether the item was retrieved from the cache instead of by executing the given closure, you may use the `rememberWithWarmth` method. This method returns an array containing the cached value and a boolean indicating whether the item was "warm", meaning it was retrieved from the cache and not resolved from the closure: -->
項目が指定したクロージャを実行して取得されたのか、それともキャッシュから取得されたのかを知る必要がある場合は、`rememberWithWarmth` メソッドを使用できます。このメソッドは、キャッシュされた値と、その項目が「ウォーム」だったかどうか（つまり、クロージャから解決されたのではなくキャッシュから取得されたかどうか）を示すブール値を含む配列を返します。

```php
[$value, $warm] = Cache::rememberWithWarmth('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
`rememberForever` メソッドを使用して、キャッシュからアイテムを取得したり、アイテムが存在しない場合は永久に保存したりできます。

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
<!-- #### Stale While Revalidate -->
#### Stale While Revalidate

<!-- When using the `Cache::remember` method, some users may experience slow response times if the cached value has expired. For certain types of data, it can be useful to allow partially stale data to be served while the cached value is recalculated in the background, preventing some users from experiencing slow response times while cached values are calculated. This is often referred to as the "stale-while-revalidate" pattern, and the `Cache::flexible` method provides an implementation of this pattern. -->
`Cache::remember` メソッドを使用する場合、キャッシュされた値の有効期限が切れていると、一部のユーザーは応答時間が遅くなる可能性があります。特定の種類のデータの場合、キャッシュされた値がバックグラウンドで再計算されている間、部分的に古いデータを提供できるようにすると、キャッシュされた値の計算中に一部のユーザーが応答時間の低下を経験するのを防ぐことができると便利です。これは、「再検証中に失効する」パターンと呼ばれることが多く、`Cache::flexible` メソッドはこのパターンの実装を提供します。

<!-- The flexible method accepts an array that specifies how long the cached value is considered "fresh" and when it becomes "stale". The first value in the array represents the number of seconds the cache is considered fresh, while the second value defines how long it can be served as stale data before recalculation is necessary. -->
この柔軟なメソッドは、キャッシュされた値が「新しい」とみなされる期間と、いつ「古くなった」とみなされるかを指定する配列を受け入れます。配列の最初の値はキャッシュが新しいとみなされる秒数を表し、2 番目の値は再計算が必要になるまで古いデータとして提供できる期間を定義します。

<!-- If a request is made within the fresh period (before the first value), the cache is returned immediately without recalculation. If a request is made during the stale period (between the two values), the stale value is served to the user, and a [deferred function](/docs/13.x/helpers#deferred-functions) is registered to refresh the cached value after the response is sent to the user. If a request is made after the second value, the cache is considered expired, and the value is recalculated immediately, which may result in a slower response for the user: -->
新しい期間内 (最初の値の前) にリクエストが行われた場合、キャッシュは再計算されずにすぐに返されます。古い期間 (2 つの値の間) にリクエストが行われた場合、古い値がユーザーに提供され、応答がユーザーに送信された後にキャッシュされた値を更新するために [deferred function](/docs/13.x/helpers#deferred-functions) が登録されます。 2 番目の値の後にリクエストが行われた場合、キャッシュは期限切れとみなされ、値はすぐに再計算されます。その結果、ユーザーの応答が遅くなる可能性があります。

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve and Delete -->
#### Retrieve and Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
キャッシュから項目を取得してからその項目を削除する必要がある場合は、`pull` メソッドを使用できます。 `get` メソッドと同様に、項目がキャッシュに存在しない場合は `null` が返されます。

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items in the Cache -->
### Storing Items in the Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
`Cache` ファサードで `put` メソッドを使用して、アイテムをキャッシュに保存できます。

```php
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
保管時間が `put` メソッドに渡されない場合、アイテムは無期限に保管されます。

```php
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
秒数を整数として渡す代わりに、キャッシュされたアイテムの有効期限を表す `DateTime` インスタンスを渡すこともできます。

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
<!-- #### Store if Not Present -->
#### Store if Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` メソッドは、アイテムがキャッシュ ストアに存在しない場合にのみ、アイテムをキャッシュに追加します。項目が実際にキャッシュに追加される場合、メソッドは `true` を返します。それ以外の場合、メソッドは `false` を返します。 `add` メソッドはアトミック操作です。

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
<!-- ### Extending Item Lifetime -->
### Extending Item Lifetime

<!-- The `touch` method allows you to extend the lifetime (TTL) of an existing cache item. The `touch` method will return `true` if the cache item exists and its expiration time was successfully extended. If the item does not exist in the cache, the method will return `false`: -->
`touch` メソッドを使用すると、既存のキャッシュ アイテムの有効期間 (TTL) を延長できます。キャッシュ項目が存在し、その有効期限が正常に延長された場合、`touch` メソッドは `true` を返します。項目がキャッシュに存在しない場合、メソッドは `false` を返します。

```php
Cache::touch('key', 3600);
```

<!-- You may provide a `DateTimeInterface`, `DateInterval`, or `Carbon` instance to specify an exact expiration time: -->
`DateTimeInterface`、`DateInterval`、または `Carbon` インスタンスを指定して、正確な有効期限を指定できます。

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` メソッドを使用して、アイテムをキャッシュに永続的に保存できます。これらのアイテムは期限切れにならないため、`forget` メソッドを使用してキャッシュから手動で削除する必要があります。

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached ドライバを使用している場合、キャッシュがサイズ制限に達すると、「永久に」保存されている項目が削除される可能性があります。

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From the Cache -->
### Removing Items From the Cache

<!-- You may remove items from the cache using the `forget` method: -->
`forget` メソッドを使用して、キャッシュから項目を削除できます。

```php
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
ゼロまたは負の有効期限秒数を指定してアイテムを削除することもできます。

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
`flush` メソッドを使用してキャッシュ全体をクリアできます。

```php
Cache::flush();
```

<!-- You may clear all atomic locks in the cache using the `flushLocks` method: -->
`flushLocks` メソッドを使用して、キャッシュ内のすべてのアトミック ロックをクリアできます。

```php
Cache::flushLocks();
```

> [!WARNING]
> キャッシュをフラッシュすると、設定されたキャッシュの「プレフィックス」が考慮されず、キャッシュからすべてのエントリが削除されます。他のアプリケーションによって共有されているキャッシュをクリアするときは、この点を慎重に検討してください。

<a name="cache-memoization"></a>
<!-- ### Cache Memoization -->
### Cache Memoization

<!-- Laravel's `memo` cache driver allows you to temporarily store resolved cache values in memory during a single request or job execution. This prevents repeated cache hits within the same execution, significantly improving performance. -->
Laravel の `memo` キャッシュ ドライバを使用すると、単一のリクエストまたはジョブの実行中に、解決されたキャッシュ値をメモリに一時的に保存できます。これにより、同じ実行内でキャッシュ ヒットが繰り返されることがなくなり、パフォーマンスが大幅に向上します。

<!-- To use the memoized cache, invoke the `memo` method: -->
メモ化されたキャッシュを使用するには、`memo` メソッドを呼び出します。

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

<!-- The `memo` method optionally accepts the name of a cache store, which specifies the underlying cache store the memoized driver will decorate: -->
`memo` メソッドは、オプションでキャッシュ ストアの名前を受け入れます。これは、メモ化されたドライバが修飾する基になるキャッシュ ストアを指定します。

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

<!-- The first `get` call for a given key retrieves the value from your cache store, but subsequent calls within the same request or job will retrieve the value from memory: -->
特定のキーに対する最初の `get` 呼び出しではキャッシュ ストアから値が取得されますが、同じリクエストまたはジョブ内での後続の呼び出しではメモリから値が取得されます。

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

<!-- When calling methods that modify cache values (such as `put`, `increment`, `remember`, etc.), the memoized cache automatically forgets the memoized value and delegates the mutating method call to the underlying cache store: -->
キャッシュ値を変更するメソッド (`put`、`increment`、`remember` など) を呼び出すと、メモ化されたキャッシュは自動的にメモ化された値を忘れ、変更メソッドの呼び出しを基になるキャッシュ ストアに委任します。

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` ファサードの使用に加えて、グローバル `cache` 関数を使用して、キャッシュ経由でデータを取得および保存することもできます。単一の文字列引数を指定して `cache` 関数を呼び出すと、指定されたキーの値が返されます。

```php
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
キーと値のペアの配列と有効期限を関数に指定すると、指定された期間、値がキャッシュに保存されます。

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
`cache` 関数を引数なしで呼び出すと、`Illuminate\Contracts\Cache\Factory` 実装のインスタンスが返され、他のキャッシュ メソッドを呼び出すことができます。

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> グローバル `cache` 関数への呼び出しをテストするときは、[testing the facade](/docs/13.x/mocking#mocking-facades) であるかのように `Cache::shouldReceive` メソッドを使用できます。

<a name="cache-tags"></a>
<!-- ## Cache Tags -->
## Cache Tags

> [!WARNING]
> `file`、`dynamodb`、`database`、または `storage` キャッシュ ドライバを使用する場合、キャッシュ タグはサポートされません。

<a name="storing-tagged-cache-items"></a>
<!-- ### Storing Tagged Cache Items -->
### Storing Tagged Cache Items

<!-- Cache tags allow you to tag related items in the cache and then flush all cached values that have been assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` a value into the cache: -->
キャッシュ タグを使用すると、キャッシュ内の関連アイテムにタグを付けて、特定のタグが割り当てられているすべてのキャッシュされた値をフラッシュできます。タグ名の順序付き配列を渡すことで、タグ付きキャッシュにアクセスできます。たとえば、タグ付きキャッシュにアクセスし、キャッシュ内の値を `put` してみましょう。

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
<!-- ### Accessing Tagged Cache Items -->
### Accessing Tagged Cache Items

<!-- Items stored via tags may not be accessed without also providing the tags that were used to store the value. To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method, then call the `get` method with the key you wish to retrieve: -->
タグを介して保存されたアイテムには、値の保存に使用されたタグも提供しないとアクセスできません。タグ付きキャッシュ アイテムを取得するには、同じ順序のタグ リストを `tags` メソッドに渡し、取得するキーを指定して `get` メソッドを呼び出します。

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
<!-- ### Removing Tagged Cache Items -->
### Removing Tagged Cache Items

<!-- You may flush all items that are assigned a tag or list of tags. For example, the following code would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache: -->
タグまたはタグのリストが割り当てられているすべての項目をフラッシュできます。たとえば、次のコードは、`people`、`authors`、またはその両方でタグ付けされたすべてのキャッシュを削除します。したがって、`Anne` と `John` の両方がキャッシュから削除されます。

```php
Cache::tags(['people', 'authors'])->flush();
```

<!-- In contrast, the code below would remove only cached values tagged with `authors`, so `Anne` would be removed, but not `John`: -->
対照的に、以下のコードは、`authors` でタグ付けされたキャッシュされた値のみを削除するため、`Anne` は削除されますが、`John` は削除されません。

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="managing-locks"></a>
<!-- ### Managing Locks -->
### Managing Locks

<!-- Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Cloud](https://cloud.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method: -->
アトミック ロックを使用すると、競合状態を気にせずに分散ロックを操作できます。たとえば、[Laravel Cloud](https://cloud.laravel.com) はアトミック ロックを使用して、サーバー上で一度に 1 つのリモート タスクのみが実行されるようにします。 `Cache::lock` メソッドを使用してロックを作成および管理できます。

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
`get` メソッドはクロージャーも受け入れます。クロージャーが実行されると、Laravel は自動的にロックを解放します。

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock cannot be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
リクエストした時点でロックが利用できない場合は、Laravel に指定した秒数待機するように指示できます。指定された制限時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock->release();
}
```

<!-- The example above may be simplified by passing a closure to the `block` method. When a closure is passed to this method, Laravel will attempt to acquire the lock for the specified number of seconds and will automatically release the lock once the closure has been executed: -->
上記の例は、`block` メソッドにクロージャーを渡すことで簡略化できます。クロージャがこのメソッドに渡されると、Laravel は指定された秒数の間ロックの取得を試み、クロージャが実行されると自動的にロックを解放します。

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
場合によっては、あるプロセスでロックを取得し、別のプロセスでロックを解放したい場合があります。たとえば、Web リクエスト中にロックを取得し、そのリクエストによってトリガーされたキューに入れられたジョブの終了時にロックを解放したい場合があります。このシナリオでは、ジョブが指定されたトークンを使用してロックを再インスタンス化できるように、ロックのスコープ指定された「所有者トークン」をキューに入れられたジョブに渡す必要があります。

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
以下の例では、ロックが正常に取得された場合に、キューに入れられたジョブをディスパッチします。さらに、ロックの `owner` メソッドを介して、ロックの所有者トークンをキューに入れられたジョブに渡します。

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
アプリケーションの `ProcessPodcast` ジョブ内で、所有者トークンを使用してロックを復元および解放できます。

```php
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
現在の所有者を考慮せずにロックを解放したい場合は、`forceRelease` メソッドを使用できます。

```php
Cache::lock('processing')->forceRelease();
```

<a name="refreshing-locks"></a>
<!-- ### Refreshing Locks -->
### Refreshing Locks

<!-- If you need to extend the expiration of a lock that you currently own, you may use the `refresh` method. If no number of seconds is provided, the lock's original duration will be used. This is useful for long-running operations where you prefer to acquire a short lock and periodically extend it instead of acquiring a lock with a very long expiration time: -->
現在所有しているロックの有効期限を延長する必要がある場合は、`refresh` メソッドを使用できます。秒数を指定しない場合は、ロックの元の期間が使用されます。これは、有効期限の非常に長いロックを取得する代わりに、短いロックを取得して定期的に延長したい長時間実行の処理で便利です。

```php
$lock = Cache::lock('generate-reports', 60);

if ($lock->get()) {
    foreach ($reports as $report) {
        $report->generate();

        // Extend the lock for another 60 seconds...
        $lock->refresh();
    }

    $lock->release();
}
```

<a name="concurrency-limiting"></a>
<!-- ### Concurrency Limiting -->
### Concurrency Limiting

<!-- Laravel's atomic lock functionality also provides a few ways to limit concurrent execution of closures. Use `withoutOverlapping` when you want to allow only one running instance across your infrastructure: -->
Laravel のアトミック ロック機能は、クロージャの同時実行を制限するいくつかの方法も提供します。インフラストラクチャ全体で 1 つのインスタンスのみの実行を許可する場合は、`withoutOverlapping` を使用します。

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

<!-- By default, the lock is held until the closure finishes executing, and the method waits up to 10 seconds to acquire the lock. You may customize these values using additional arguments: -->
デフォルトでは、ロックはクロージャの実行が完了するまで保持され、メソッドはロックを取得するまで最大 10 秒待機します。追加の引数を使用してこれらの値をカスタマイズできます。

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

<!-- If the lock cannot be acquired within the specified wait time, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown. -->
指定された待機時間内にロックを取得できない場合は、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

<!-- If you want controlled parallelism, use the `funnel` method to set a maximum number of concurrent executions. The `funnel` method works with any cache driver that supports locks: -->
並列処理を制御したい場合は、`funnel` メソッドを使用して最大同時実行数を設定します。 `funnel` メソッドは、ロックをサポートするキャッシュ ドライバで動作します。

```php
Cache::funnel('foo')
    ->limit(3)
    ->releaseAfter(60)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired...
    }, function () {
        // Could not acquire concurrency lock...
    });
```

<!-- The `funnel` key identifies the resource being limited. The `limit` method defines the maximum concurrent executions. The `releaseAfter` method sets a safety timeout in seconds before an acquired slot is automatically released. The `block` method sets how many seconds to wait for an available slot. -->
`funnel` キーは、制限されているリソースを識別します。 `limit` メソッドは、最大同時実行数を定義します。 `releaseAfter` メソッドは、取得したスロットが自動的に解放される前に、安全タイムアウトを秒単位で設定します。 `block` メソッドは、使用可能なスロットを待機する秒数を設定します。

<!-- If you prefer to handle the timeout via exceptions instead of providing a failure closure, you may omit the second closure. An `Illuminate\Cache\Limiters\LimiterTimeoutException` will be thrown if the lock cannot be acquired within the specified wait time: -->
失敗クロージャを提供する代わりに例外によってタイムアウトを処理したい場合は、2 番目のクロージャを省略できます。指定された待機時間内にロックを取得できない場合は、`Illuminate\Cache\Limiters\LimiterTimeoutException` がスローされます。

```php
use Illuminate\Cache\Limiters\LimiterTimeoutException;

try {
    Cache::funnel('foo')
        ->limit(3)
        ->releaseAfter(60)
        ->block(10)
        ->then(function () {
            // Concurrency lock acquired...
        });
} catch (LimiterTimeoutException $e) {
    // Unable to acquire concurrency lock...
}
```

<!-- If you would like to use a specific cache store for the concurrency limiter, you may invoke the `funnel` method on the desired store: -->
同時実行リミッターに特定のキャッシュ ストアを使用したい場合は、目的のストアで `funnel` メソッドを呼び出すことができます。

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> `funnel` メソッドでは、キャッシュ ストアが `Illuminate\Contracts\Cache\LockProvider` インターフェイスを実装する必要があります。ロックをサポートしていないキャッシュ ストアで `funnel` を使用しようとすると、`BadMethodCallException` がスローされます。

<a name="cache-failover"></a>
<!-- ## Cache Failover -->
## Cache Failover

<!-- The `failover` cache driver provides automatic failover functionality when interacting with the cache. If the primary cache store of the `failover` store fails for any reason, Laravel will automatically attempt to use the next configured store in the list. This is particularly useful for ensuring high availability in production environments where cache reliability is critical. -->
`failover` キャッシュ ドライバは、キャッシュとの対話時に自動フェイルオーバー機能を提供します。 `failover` ストアのプライマリ キャッシュ ストアが何らかの理由で失敗した場合、Laravel はリスト内の次に設定されているストアを自動的に使用しようとします。これは、キャッシュの信頼性が重要な実稼働環境で高可用性を確保する場合に特に役立ちます。

<!-- To configure a failover cache store, specify the `failover` driver and provide an array of store names to attempt in order. By default, Laravel includes an example failover configuration in your application's `config/cache.php` configuration file: -->
フェイルオーバー キャッシュ ストアを構成するには、`failover` ドライバを指定し、順番に試行するストア名の配列を指定します。デフォルトでは、Laravel にはアプリケーションの `config/cache.php` 構成ファイルにサンプルのフェイルオーバー構成が含まれています。

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

<!-- Once you have configured a store that uses the `failover` driver, you will need to set the failover store as your default cache store in your application's `.env` file to make use of the failover functionality: -->
`failover` ドライバを使用するストアを構成したら、フェイルオーバー機能を利用するには、アプリケーションの `.env` ファイルでフェイルオーバー ストアをデフォルトのキャッシュ ストアとして設定する必要があります。

```ini
CACHE_STORE=failover
```

<!-- When a cache store operation fails and failover is activated, Laravel will dispatch the `Illuminate\Cache\Events\CacheFailedOver` event, allowing you to report or log that a cache store has failed. -->
キャッシュストア操作が失敗し、フェイルオーバーがアクティブ化されると、Laravel は `Illuminate\Cache\Events\CacheFailedOver` イベントを送出し、キャッシュストアが失敗したことをレポートまたはログに記録できるようにします。

<a name="adding-custom-cache-drivers"></a>
<!-- ## Adding Custom Cache Drivers -->
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
<!-- ### Writing the Driver -->
### Writing the Driver

<!-- To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/13.x/contracts). So, a MongoDB cache implementation might look something like this: -->
カスタム キャッシュ ドライバを作成するには、まず `Illuminate\Contracts\Cache\Store` [contract](/docs/13.x/contracts) を実装する必要があります。したがって、MongoDB キャッシュの実装は次のようになります。

```php
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

```php
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

```php
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

<!-- The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/13.x/container). -->
`extend` メソッドに渡される最初の引数はドライバの名前です。これは、`config/cache.php` 構成ファイルの `driver` オプションに対応します。 2 番目の引数は、`Illuminate\Cache\Repository` インスタンスを返すクロージャです。クロージャには、[service container](/docs/13.x/container) のインスタンスである `$app` インスタンスが渡されます。

<!-- Once your extension is registered, update the `CACHE_STORE` environment variable or `default` option within your application's `config/cache.php` configuration file to the name of your extension. -->
拡張機能が登録されたら、アプリケーションの `config/cache.php` 構成ファイル内の `CACHE_STORE` 環境変数または `default` オプションを拡張機能の名前に更新します。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for various [events](/docs/13.x/events) dispatched by the cache: -->
すべてのキャッシュ操作でコードを実行するには、キャッシュによってディスパッチされるさまざまな [events](/docs/13.x/events) をリッスンできます。

<div class="overflow-auto">

<!-- | Event Name | |-------------------------------------------------| | `Illuminate\Cache\Events\CacheFlushed` | | `Illuminate\Cache\Events\CacheFlushing` | | `Illuminate\Cache\Events\CacheFlushFailed` | | `Illuminate\Cache\Events\CacheLocksFlushed` | | `Illuminate\Cache\Events\CacheLocksFlushing` | | `Illuminate\Cache\Events\CacheLocksFlushFailed` | | `Illuminate\Cache\Events\CacheHit` | | `Illuminate\Cache\Events\CacheMissed` | | `Illuminate\Cache\Events\ForgettingKey` | | `Illuminate\Cache\Events\KeyForgetFailed` | | `Illuminate\Cache\Events\KeyForgotten` | | `Illuminate\Cache\Events\KeyWriteFailed` | | `Illuminate\Cache\Events\KeyWritten` | | `Illuminate\Cache\Events\RetrievingKey` | | `Illuminate\Cache\Events\RetrievingManyKeys` | | `Illuminate\Cache\Events\WritingKey` | | `Illuminate\Cache\Events\WritingManyKeys` | -->
| イベント名                                      |
|-------------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`          |
| `Illuminate\Cache\Events\CacheFlushing`         |
| `Illuminate\Cache\Events\CacheFlushFailed`      |
| `Illuminate\Cache\Events\CacheLocksFlushed`     |
| `Illuminate\Cache\Events\CacheLocksFlushing`    |
| `Illuminate\Cache\Events\CacheLocksFlushFailed` |
| `Illuminate\Cache\Events\CacheHit`              |
| `Illuminate\Cache\Events\CacheMissed`           |
| `Illuminate\Cache\Events\ForgettingKey`         |
| `Illuminate\Cache\Events\KeyForgetFailed`       |
| `Illuminate\Cache\Events\KeyForgotten`          |
| `Illuminate\Cache\Events\KeyWriteFailed`        |
| `Illuminate\Cache\Events\KeyWritten`            |
| `Illuminate\Cache\Events\RetrievingKey`         |
| `Illuminate\Cache\Events\RetrievingManyKeys`    |
| `Illuminate\Cache\Events\WritingKey`            |
| `Illuminate\Cache\Events\WritingManyKeys`       |

</div>

<!-- To increase performance, you may disable cache events by setting the `events` configuration option to `false` for a given cache store in your application's `config/cache.php` configuration file: -->
パフォーマンスを向上させるには、アプリケーションの `config/cache.php` 構成ファイル内の特定のキャッシュ ストアの `events` 構成オプションを `false` に設定して、キャッシュ イベントを無効にすることができます。

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
