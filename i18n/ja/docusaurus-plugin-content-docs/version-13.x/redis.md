<!-- # Redis -->
# Redis

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Clusters](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Interacting With Redis](#interacting-with-redis)
    - [Transactions](#transactions)
    - [Pipelining Commands](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Redis](https://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](https://redis.io/docs/latest/develop/data-types/strings/), [hashes](https://redis.io/docs/latest/develop/data-types/hashes/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [sets](https://redis.io/docs/latest/develop/data-types/sets/), and [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/). -->
[Redis](https://redis.io) は、オープンソースの高度な Key-Value ストアです。キーには [strings](https://redis.io/docs/latest/develop/data-types/strings/)、[hashes](https://redis.io/docs/latest/develop/data-types/hashes/)、[lists](https://redis.io/docs/latest/develop/data-types/lists/)、[sets](https://redis.io/docs/latest/develop/data-types/sets/)、[sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) を含めることができるため、データ構造サーバーと呼ばれることがよくあります。

<!-- Before using Redis with Laravel, we encourage you to install and use the [PhpRedis](https://github.com/phpredis/phpredis) PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using [Laravel Sail](/docs/13.x/sail), this extension is already installed in your application's Docker container. -->
Laravel で Redis を使用する前に、PECL 経由で [PhpRedis](https://github.com/phpredis/phpredis) PHP 拡張機能をインストールして使用することをお勧めします。この拡張機能は、「ユーザーランド」PHP パッケージに比べてインストールが複雑ですが、Redis を頻繁に使用するアプリケーションではパフォーマンスが向上する可能性があります。 [Laravel Sail](/docs/13.x/sail) を使用している場合、この拡張機能はアプリケーションの Docker コンテナーにすでにインストールされています。

<!-- If you are unable to install the PhpRedis extension, you may install the `predis/predis` package via Composer. Predis is a Redis client written entirely in PHP and does not require any additional extensions: -->
PhpRedis 拡張機能をインストールできない場合は、Composer 経由で `predis/predis` パッケージをインストールできます。 Predis は、完全に PHP で書かれた Redis クライアントであり、追加の拡張機能は必要ありません。

```shell
composer require predis/predis
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- You may configure your application's Redis settings via the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers utilized by your application: -->
`config/database.php` 構成ファイルを介してアプリケーションの Redis 設定を構成できます。このファイル内には、アプリケーションで使用される Redis サーバーを含む `redis` 配列が表示されます。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],

],
```

<!-- Each Redis server defined in your configuration file is required to have a name, host, and a port unless you define a single URL to represent the Redis connection: -->
Redis 接続を表す単一の URL を定義しない限り、構成ファイルで定義された各 Redis サーバーには、名前、ホスト、およびポートが必要です。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a name="configuring-the-connection-scheme"></a>
<!-- #### Configuring the Connection Scheme -->
#### Configuring the Connection Scheme

<!-- By default, Redis clients will use the `tcp` scheme when connecting to your Redis servers; however, you may use TLS / SSL encryption by specifying a `scheme` configuration option in your Redis server's configuration array: -->
デフォルトでは、Redis クライアントは Redis サーバーに接続するときに `tcp` スキームを使用します。ただし、Redis サーバーの構成配列で `scheme` 構成オプションを指定することで、TLS / SSL 暗号化を使用できます。

```php
'default' => [
    'scheme' => 'tls',
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
],
```

<a name="clusters"></a>
<!-- ### Clusters -->
### Clusters

<!-- If your application is utilizing a cluster of Redis servers, you should define these clusters within a `clusters` key of your Redis configuration. This configuration key does not exist by default so you will need to create it within your application's `config/database.php` configuration file: -->
アプリケーションが Redis サーバーのクラスターを利用している場合は、Redis 構成の `clusters` キー内でこれらのクラスターを定義する必要があります。この構成キーはデフォルトでは存在しないため、アプリケーションの `config/database.php` 構成ファイル内に作成する必要があります。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'clusters' => [
        'default' => [
            [
                'url' => env('REDIS_URL'),
                'host' => env('REDIS_HOST', '127.0.0.1'),
                'username' => env('REDIS_USERNAME'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', '6379'),
                'database' => env('REDIS_DB', '0'),
            ],
        ],
    ],

    // ...
],
```

<!-- By default, Laravel will use native Redis clustering since the `options.cluster` configuration value is set to `redis`. Redis clustering is a great default option, as it gracefully handles failover. -->
デフォルトでは、`options.cluster` 構成値が `redis` に設定されているため、Laravel はネイティブ Redis クラスタリングを使用します。 Redis クラスタリングは、フェールオーバーを適切に処理するため、優れたデフォルト オプションです。

<!-- Laravel also supports client-side sharding when using Predis. However, client-side sharding does not handle failover; therefore, it is primarily suited for transient cached data that is available from another primary data store. -->
Laravel は、Predis を使用する場合のクライアント側のシャーディングもサポートします。ただし、クライアント側のシャーディングはフェイルオーバーを処理しません。したがって、これは主に、別のプライマリ データ ストアから利用できる一時的なキャッシュ データに適しています。

<!-- If you would like to use client-side sharding instead of native Redis clustering, you may remove the `options.cluster` configuration value within your application's `config/database.php` configuration file: -->
ネイティブ Redis クラスタリングの代わりにクライアント側シャーディングを使用したい場合は、アプリケーションの `config/database.php` 構成ファイル内の `options.cluster` 構成値を削除できます。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        // ...
    ],

    // ...
],
```

<a name="predis"></a>
<!-- ### Predis -->
### Predis

<!-- If you would like your application to interact with Redis via the Predis package, you should ensure the `REDIS_CLIENT` environment variable's value is `predis`: -->
アプリケーションが Predis パッケージ経由で Redis と対話できるようにする場合は、`REDIS_CLIENT` 環境変数の値が `predis` であることを確認する必要があります。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

<!-- In addition to the default configuration options, Predis supports additional [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) that may be defined for each of your Redis servers. To utilize these additional configuration options, add them to your Redis server configuration in your application's `config/database.php` configuration file: -->
デフォルトの構成オプションに加えて、Predis は、Redis サーバーごとに定義できる追加の [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) をサポートします。これらの追加の構成オプションを利用するには、アプリケーションの `config/database.php` 構成ファイル内の Redis サーバー構成に追加します。

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_write_timeout' => 60,
],
```

<a name="phpredis"></a>
<!-- ### PhpRedis -->
### PhpRedis

<!-- By default, Laravel will use the PhpRedis extension to communicate with Redis. The client that Laravel will use to communicate with Redis is dictated by the value of the `redis.client` configuration option, which typically reflects the value of the `REDIS_CLIENT` environment variable: -->
デフォルトでは、Laravel は PhpRedis 拡張機能を使用して Redis と通信します。 Laravel が Redis と通信するために使用するクライアントは、`redis.client` 構成オプションの値によって決まります。これは通常、`REDIS_CLIENT` 環境変数の値を反映します。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

<!-- In addition to the default configuration options, PhpRedis supports the following additional connection parameters: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, and `context`. You may add any of these options to your Redis server configuration in the `config/database.php` configuration file: -->
デフォルトの構成オプションに加えて、PhpRedis は次の追加接続パラメータをサポートします: `name`、`persistent`、`persistent_id`、`prefix`、`read_timeout`、`retry_interval`、`max_retries`、`backoff_algorithm`、 `backoff_base`、`backoff_cap`、`timeout`、および `context`。 `config/database.php` 構成ファイル内の Redis サーバー構成に、次のオプションのいずれかを追加できます。

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a name="retry-and-backoff-configuration"></a>
<!-- #### Retry and Backoff Configuration -->
#### Retry and Backoff Configuration

<!-- The `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, and `backoff_cap` options may be used to configure how the PhpRedis client should attempt to reconnect to a Redis server. The following backoff algorithms are supported: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, and `constant`: -->
`retry_interval`、`max_retries`、`backoff_algorithm`、`backoff_base`、および `backoff_cap` オプションは、PhpRedis クライアントが Redis サーバーへの再接続を試行する方法を構成するために使用できます。次のバックオフ アルゴリズムがサポートされています: `default`、`decorrelated_jitter`、`equal_jitter`、`exponential`、`uniform`、および `constant`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),
    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),
    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),
],
```
<!-- Predis 3.4.0 and later supports built-in retry and backoff configuration via the `Retry` class. You may configure retries using the `max_retries` option and configure the backoff strategy using the `retry` option. The `retry` option should be an array keyed by one of the following strategy classes: `NoBackoff`, `EqualBackoff`, or `ExponentialBackoff`: -->
Predis 3.4.0 以降では、`Retry` クラスを介した組み込みの再試行およびバックオフ構成がサポートされています。`max_retries` オプションで再試行回数を設定し、`retry` オプションでバックオフ戦略を設定できます。`retry` オプションは、次のいずれかの戦略クラスをキーにした配列にする必要があります: `NoBackoff`、`EqualBackoff`、または `ExponentialBackoff`:

```php
use Predis\Retry\Strategy\ExponentialBackoff;

'default' => [
    'url' => env('REDIS_URL'),
    // ...
    'retry' => [
        ExponentialBackoff::class => [
            env('REDIS_BACKOFF_BASE', 100),
            env('REDIS_BACKOFF_CAP', 1000),
            true, // Enable jitter...
        ],
    ],
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
],
```

<!-- When using Predis with a Redis cluster, you may define retry configuration in the `parameters` option of your cluster configuration: -->
Predis を Redis クラスターと併用する場合は、クラスター設定の `parameters` オプションで再試行設定を定義できます:

```php
use Predis\Retry\Strategy\NoBackoff;

'clusters' => [
    'default' => [
        // ...
    ],
],

'options' => [
    'cluster' => env('REDIS_CLUSTER', 'redis'),
    'parameters' => [
        'retry' => [
            NoBackoff::class => [],
        ],
        'max_retries' => env('REDIS_MAX_RETRIES', 3),
    ],
],
```

<a name="unix-socket-connections"></a>
<!-- #### Unix Socket Connections -->
#### Unix Socket Connections

<!-- Redis connections can also be configured to use Unix sockets instead of TCP. This can offer improved performance by eliminating TCP overhead for connections to Redis instances on the same server as your application. To configure Redis to use a Unix socket, set your `REDIS_HOST` environment variable to the path of the Redis socket and the `REDIS_PORT` environment variable to `0`: -->
Redis 接続は、TCP の代わりに Unix ソケットを使用するように構成することもできます。これにより、アプリケーションと同じサーバー上の Redis インスタンスへの接続の TCP オーバーヘッドが排除され、パフォーマンスが向上します。 Unix ソケットを使用するように Redis を構成するには、`REDIS_HOST` 環境変数を Redis ソケットのパスに設定し、`REDIS_PORT` 環境変数を `0` に設定します。

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
<!-- #### PhpRedis Serialization and Compression -->
#### PhpRedis Serialization and Compression

<!-- The PhpRedis extension may also be configured to use a variety of serializers and compression algorithms. These algorithms can be configured via the `options` array of your Redis configuration: -->
PhpRedis 拡張機能は、さまざまなシリアライザーや圧縮アルゴリズムを使用するように構成することもできます。これらのアルゴリズムは、Redis 構成の `options` 配列を介して構成できます。

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // ...
],
```

<!-- Currently supported serializers include: `Redis::SERIALIZER_NONE` (default), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, and `Redis::SERIALIZER_MSGPACK`. -->
現在サポートされているシリアライザーには、`Redis::SERIALIZER_NONE` (デフォルト)、`Redis::SERIALIZER_PHP`、`Redis::SERIALIZER_JSON`、`Redis::SERIALIZER_IGBINARY`、および `Redis::SERIALIZER_MSGPACK` が含まれます。

<!-- Supported compression algorithms include: `Redis::COMPRESSION_NONE` (default), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, and `Redis::COMPRESSION_LZ4`. -->
サポートされている圧縮アルゴリズムには、`Redis::COMPRESSION_NONE` (デフォルト)、`Redis::COMPRESSION_LZF`、`Redis::COMPRESSION_ZSTD`、および `Redis::COMPRESSION_LZ4` があります。

<a name="interacting-with-redis"></a>
<!-- ## Interacting With Redis -->
## Interacting With Redis

<!-- You may interact with Redis by calling various methods on the `Redis` [facade](/docs/13.x/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](https://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the Redis `GET` command by calling the `get` method on the `Redis` facade: -->
`Redis` [facade](/docs/13.x/facades) でさまざまなメソッドを呼び出すことで、Redis と対話できます。 `Redis` ファサードは動的メソッドをサポートしています。つまり、ファサードで任意の [Redis command](https://redis.io/commands) を呼び出すことができ、コマンドは Redis に直接渡されます。この例では、`Redis` ファサードで `get` メソッドを呼び出して、Redis `GET` コマンドを呼び出します。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

<!-- As mentioned above, you may call any of Redis' commands on the `Redis` facade. Laravel uses magic methods to pass the commands to the Redis server. If a Redis command expects arguments, you should pass those to the facade's corresponding method: -->
上で述べたように、`Redis` ファサードで Redis のコマンドを呼び出すことができます。 Laravel はマジック メソッドを使用してコマンドを Redis サーバーに渡します。 Redis コマンドが引数を必要とする場合は、それらをファサードの対応するメソッドに渡す必要があります。

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

<!-- Alternatively, you may pass commands to the server using the `Redis` facade's `command` method, which accepts the name of the command as its first argument and an array of values as its second argument: -->
あるいは、`Redis` ファサードの `command` メソッドを使用してサーバーにコマンドを渡すこともできます。このメソッドは、最初の引数としてコマンドの名前を受け取り、2 番目の引数として値の配列を受け取ります。

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
<!-- #### Using Multiple Redis Connections -->
#### Using Multiple Redis Connections

<!-- Your application's `config/database.php` configuration file allows you to define multiple Redis connections / servers. You may obtain a connection to a specific Redis connection using the `Redis` facade's `connection` method: -->
アプリケーションの `config/database.php` 構成ファイルを使用すると、複数の Redis 接続/サーバーを定義できます。 `Redis` ファサードの `connection` メソッドを使用して、特定の Redis 接続への接続を取得できます。

```php
$redis = Redis::connection('connection-name');
```

<!-- To obtain an instance of the default Redis connection, you may call the `connection` method without any additional arguments: -->
デフォルトの Redis 接続のインスタンスを取得するには、追加の引数を指定せずに `connection` メソッドを呼び出すことができます。

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
<!-- ### Transactions -->
### Transactions

<!-- The `Redis` facade's `transaction` method provides a convenient wrapper around Redis' native `MULTI` and `EXEC` commands. The `transaction` method accepts a closure as its only argument. This closure will receive a Redis connection instance and may issue any commands it would like to this instance. All of the Redis commands issued within the closure will be executed in a single, atomic transaction: -->
`Redis` ファサードの `transaction` メソッドは、Redis のネイティブ `MULTI` および `EXEC` コマンドの便利なラッパーを提供します。 `transaction` メソッドは、唯一の引数としてクロージャを受け入れます。このクロージャは Redis 接続インスタンスを受け取り、このインスタンスに対して必要なコマンドを発行できます。クロージャ内で発行されるすべての Redis コマンドは、単一のアトミック トランザクションで実行されます。

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis トランザクションを定義する場合、Redis 接続から値を取得することはできません。トランザクションは単一のアトミックな操作として実行され、その操作はクロージャー全体がコマンドの実行を完了するまで実行されないことに注意してください。

<!-- #### Lua Scripts -->
#### Lua Scripts

<!-- The `eval` method provides another method of executing multiple Redis commands in a single, atomic operation. However, the `eval` method has the benefit of being able to interact with and inspect Redis key values during that operation. Redis scripts are written in the [Lua programming language](https://www.lua.org). -->
`eval` メソッドは、単一のアトミック操作で複数の Redis コマンドを実行する別の方法を提供します。ただし、`eval` メソッドには、操作中に Redis キー値を操作して検査できるという利点があります。 Redis スクリプトは [Lua programming language](https://www.lua.org) に記述されます。

<!-- The `eval` method can be a bit scary at first, but we'll explore a basic example to break the ice. The `eval` method expects several arguments. First, you should pass the Lua script (as a string) to the method. Secondly, you should pass the number of keys (as an integer) that the script interacts with. Thirdly, you should pass the names of those keys. Finally, you may pass any other additional arguments that you need to access within your script. -->
`eval` メソッドは最初は少し怖いかもしれませんが、緊張を解くための基本的な例を見ていきます。 `eval` メソッドは複数の引数を必要とします。まず、Lua スクリプトを (文字列として) メソッドに渡す必要があります。次に、スクリプトが対話するキーの数を (整数として) 渡す必要があります。第三に、それらのキーの名前を渡す必要があります。最後に、スクリプト内でアクセスする必要があるその他の追加の引数を渡すことができます。

<!-- In this example, we will increment a counter, inspect its new value, and increment a second counter if the first counter's value is greater than five. Finally, we will return the value of the first counter: -->
この例では、カウンタをインクリメントし、その新しい値を検査し、最初のカウンタの値が 5 より大きい場合は 2 番目のカウンタをインクリメントします。最後に、最初のカウンターの値を返します。

```php
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!WARNING]
> Redis スクリプトの詳細については、[Redis documentation](https://redis.io/commands/eval) を参照してください。

<a name="pipelining-commands"></a>
<!-- ### Pipelining Commands -->
### Pipelining Commands

<!-- Sometimes you may need to execute dozens of Redis commands. Instead of making a network trip to your Redis server for each command, you may use the `pipeline` method. The `pipeline` method accepts one argument: a closure that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be sent to the Redis server at the same time to reduce network trips to the server. The commands will still be executed in the order they were issued: -->
場合によっては、数十の Redis コマンドを実行する必要がある場合があります。コマンドごとに Redis サーバーへのネットワーク トリップを行う代わりに、`pipeline` メソッドを使用できます。 `pipeline` メソッドは、Redis インスタンスを受け取るクロージャーという 1 つの引数を受け入れます。すべてのコマンドをこの Redis インスタンスに発行すると、それらはすべて Redis サーバーに同時に送信され、サーバーへのネットワーク トリップが削減されます。コマンドは発行された順序で引き続き実行されます。

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
<!-- ## Pub / Sub -->
## Pub / Sub

<!-- Laravel provides a convenient interface to the Redis `publish` and `subscribe` commands. These Redis commands allow you to listen for messages on a given "channel". You may publish messages to the channel from another application, or even using another programming language, allowing easy communication between applications and processes. -->
Laravel は、Redis `publish` および `subscribe` コマンドへの便利なインターフェイスを提供します。これらの Redis コマンドを使用すると、特定の「チャネル」でメッセージをリッスンできます。別のアプリケーションから、または別のプログラミング言語を使用してメッセージをチャネルにパブリッシュすると、アプリケーションとプロセス間の通信が容易になります。

<!-- First, let's set up a channel listener using the `subscribe` method. We'll place this method call within an [Artisan command](/docs/13.x/artisan) since calling the `subscribe` method begins a long-running process: -->
まず、`subscribe` メソッドを使用してチャネル リスナを設定しましょう。 `subscribe` メソッドを呼び出すと長時間実行プロセスが開始されるため、このメソッド呼び出しを [Artisan command](/docs/13.x/artisan) 内に配置します。

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}
```

<!-- Now we may publish messages to the channel using the `publish` method: -->
ここで、`publish` メソッドを使用してメッセージをチャネルにパブリッシュできます。

```php
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});
```

<a name="wildcard-subscriptions"></a>
<!-- #### Wildcard Subscriptions -->
#### Wildcard Subscriptions

<!-- Using the `psubscribe` method, you may subscribe to a wildcard channel, which may be useful for catching all messages on all channels. The channel name will be passed as the second argument to the provided closure: -->
`psubscribe` メソッドを使用すると、ワイルドカード チャネルをサブスクライブできます。これは、すべてのチャネル上のすべてのメッセージをキャッチするのに便利です。チャネル名は、提供されたクロージャの 2 番目の引数として渡されます。

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
