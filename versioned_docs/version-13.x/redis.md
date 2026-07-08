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
[Redis](https://redis.io)는 오픈 소스이자 고급 키-값 저장소입니다. 종종 데이터 구조 서버(data structure server)라고도 불리는데, 이는 키에 [strings](https://redis.io/docs/latest/develop/data-types/strings/), [hashes](https://redis.io/docs/latest/develop/data-types/hashes/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [sets](https://redis.io/docs/latest/develop/data-types/sets/), [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 데이터 구조를 담을 수 있기 때문입니다.

<!-- Before using Redis with Laravel, we encourage you to install and use the [PhpRedis](https://github.com/phpredis/phpredis) PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using [Laravel Sail](/docs/13.x/sail), this extension is already installed in your application's Docker container. -->
Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 프로그램을 설치하고 사용하는 것을 권장합니다. 이 확장 프로그램은 PHP 패키지보다 설치가 더 복잡할 수 있지만, Redis를 빈번하게 사용하는 애플리케이션에서는 더 나은 성능을 보여줄 수 있습니다. 만약 [Laravel Sail](/docs/13.x/sail)을 사용 중이라면, 이 확장 프로그램은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

<!-- If you are unable to install the PhpRedis extension, you may install the `predis/predis` package via Composer. Predis is a Redis client written entirely in PHP and does not require any additional extensions: -->
PhpRedis 확장 프로그램을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로만 작성된 Redis 클라이언트이며, 추가 확장 프로그램 없이 사용할 수 있습니다.

```shell
composer require predis/predis
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- You may configure your application's Redis settings via the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers utilized by your application: -->
애플리케이션의 Redis 설정은 `config/database.php` 설정 파일을 통해 구성할 수 있습니다. 이 파일 안에는 애플리케이션에서 사용하는 Redis 서버들을 정의하는 `redis` 배열이 있습니다.

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
설정 파일에 정의된 각 Redis 서버는 이름, 호스트, 그리고 포트를 반드시 지정해야 하며, 또는 Redis 연결을 나타내는 하나의 URL을 정의할 수도 있습니다.

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
기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 하지만, `scheme` 설정 옵션을 Redis 서버 설정 배열에 지정하면 TLS / SSL 암호화를 사용할 수 있습니다.

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
애플리케이션이 여러 대의 Redis 서버로 구성된 클러스터를 사용하는 경우, Redis 설정에서 `clusters` 키에 이 클러스터들을 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 설정 파일에 직접 추가해야 합니다.

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
기본적으로 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에, Laravel은 기본적으로 네이티브 Redis 클러스터링을 사용합니다. 네이티브 Redis 클러스터링은 장애 조치(failover)를 원활하게 처리하므로, 기본값으로 적합합니다.

<!-- Laravel also supports client-side sharding when using Predis. However, client-side sharding does not handle failover; therefore, it is primarily suited for transient cached data that is available from another primary data store. -->
Predis를 사용할 때는 클라이언트 측 샤딩(client-side sharding)도 지원합니다. 하지만, 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로, 다른 주요 데이터 저장소에서 다시 구할 수 있는 임시 캐시 데이터에 주로 적합합니다.

<!-- If you would like to use client-side sharding instead of native Redis clustering, you may remove the `options.cluster` configuration value within your application's `config/database.php` configuration file: -->
네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하려면, 애플리케이션의 `config/database.php` 설정 파일에서 `options.cluster` 설정 값을 제거하면 됩니다.

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
Predis 패키지를 통해 Redis와 상호작용하고 싶다면, `REDIS_CLIENT` 환경 변수의 값을 반드시 `predis`로 지정해야 합니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

<!-- In addition to the default configuration options, Predis supports additional [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) that may be defined for each of your Redis servers. To utilize these additional configuration options, add them to your Redis server configuration in your application's `config/database.php` configuration file: -->
기본 설정 옵션 외에, Predis는 각각의 Redis 서버에 대해 추가적인 [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정 옵션을 사용하고자 한다면, `config/database.php` 설정 파일의 Redis 서버 설정에 해당 옵션들을 추가하세요.

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
기본적으로 Laravel은 Redis와 통신하기 위해 PhpRedis 확장 프로그램을 사용합니다. Laravel에서 Redis와 통신할 때 사용할 클라이언트는 `redis.client` 설정 옵션의 값에 따라 결정되며, 이는 일반적으로 `REDIS_CLIENT` 환경 변수 값을 따릅니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

<!-- In addition to the default configuration options, PhpRedis supports the following additional connection parameters: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, and `context`. You may add any of these options to your Redis server configuration in the `config/database.php` configuration file: -->
기본 설정 옵션 외에도, PhpRedis는 다음과 같은 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`. 이 중 어떤 옵션이든 `config/database.php`의 Redis 서버 설정에 추가할 수 있습니다.

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
`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap` 옵션을 사용해 PhpRedis 클라이언트가 Redis 서버에 재연결할 때의 동작을 설정할 수 있습니다. 다음 백오프 알고리즘을 지원합니다: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, `constant`.

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
Predis 3.4.0 이상에서는 `Retry` 클래스를 통해 내장된 재시도 및 백오프 설정을 지원합니다. `max_retries` 옵션으로 재시도를 구성하고, `retry` 옵션으로 백오프 전략을 구성할 수 있습니다. `retry` 옵션은 다음 전략 클래스 중 하나를 키로 하는 배열이어야 합니다: `NoBackoff`, `EqualBackoff`, `ExponentialBackoff`:

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
Predis를 Redis 클러스터와 함께 사용할 때는 클러스터 설정의 `parameters` 옵션에 재시도 구성을 정의할 수 있습니다.

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
Redis 연결은 TCP 대신 Unix 소켓을 사용하도록 설정할 수 있습니다. 이렇게 하면, 동일 서버 내 Redis 인스턴스와의 통신에서 TCP 오버헤드가 제거되어 더 나은 성능을 낼 수 있습니다. Unix 소켓을 사용하려면 `REDIS_HOST` 환경 변수를 Redis 소켓의 경로로, `REDIS_PORT`는 `0`으로 설정하면 됩니다.

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
<!-- #### PhpRedis Serialization and Compression -->
#### PhpRedis Serialization and Compression

<!-- The PhpRedis extension may also be configured to use a variety of serializers and compression algorithms. These algorithms can be configured via the `options` array of your Redis configuration: -->
PhpRedis 확장 프로그램은 다양한 직렬화(serializer) 및 압축(compression) 알고리즘 사용도 지원합니다. 이 알고리즘들은 Redis 설정의 `options` 배열을 통해 지정할 수 있습니다.

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
현재 지원되는 직렬화기는 다음과 같습니다:
- `Redis::SERIALIZER_NONE` (기본값)
- `Redis::SERIALIZER_PHP`
- `Redis::SERIALIZER_JSON`
- `Redis::SERIALIZER_IGBINARY`
- `Redis::SERIALIZER_MSGPACK`

<!-- Supported compression algorithms include: `Redis::COMPRESSION_NONE` (default), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, and `Redis::COMPRESSION_LZ4`. -->
지원되는 압축 알고리즘은 다음과 같습니다:
- `Redis::COMPRESSION_NONE` (기본값)
- `Redis::COMPRESSION_LZF`
- `Redis::COMPRESSION_ZSTD`
- `Redis::COMPRESSION_LZ4`

<a name="interacting-with-redis"></a>
<!-- ## Interacting With Redis -->
## Interacting With Redis

<!-- You may interact with Redis by calling various methods on the `Redis` [facade](/docs/13.x/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](https://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the Redis `GET` command by calling the `get` method on the `Redis` facade: -->
여러 가지 메서드를 사용해 `Redis` [facade](/docs/13.x/facades)를 통해 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 다이나믹 메서드를 지원하므로, [Redis command](https://redis.io/commands)라면 어떤 것이든 파사드를 통해 호출할 수 있고, 해당 명령어가 직접 Redis로 전달됩니다. 아래 예시에서는 `Redis` 파사드의 `get` 메서드를 통해 Redis의 `GET` 명령어를 호출합니다.

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
앞서 언급한 것처럼, Redis의 모든 명령어는 `Redis` 파사드를 통해 호출할 수 있습니다. Laravel은 매직 메서드를 이용해 명령어를 Redis 서버에 전달합니다. 만약 Redis 명령어가 인수를 필요로 한다면, 파사드의 해당 메서드에 그 인수를 그대로 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

<!-- Alternatively, you may pass commands to the server using the `Redis` facade's `command` method, which accepts the name of the command as its first argument and an array of values as its second argument: -->
또는, `Redis` 파사드의 `command` 메서드를 사용해서 명령어 이름을 첫 번째 인수로, 값들을 배열 형태로 두 번째 인수로 넘겨 명령어를 전달할 수도 있습니다.

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
<!-- #### Using Multiple Redis Connections -->
#### Using Multiple Redis Connections

<!-- Your application's `config/database.php` configuration file allows you to define multiple Redis connections / servers. You may obtain a connection to a specific Redis connection using the `Redis` facade's `connection` method: -->
애플리케이션의 `config/database.php` 파일에서 여러 개의 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결 인스턴스를 얻으려면 `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다.

```php
$redis = Redis::connection('connection-name');
```

<!-- To obtain an instance of the default Redis connection, you may call the `connection` method without any additional arguments: -->
기본 Redis 연결 인스턴스를 얻으려면, 추가 인수 없이 `connection` 메서드를 호출하세요.

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
<!-- ### Transactions -->
### Transactions

<!-- The `Redis` facade's `transaction` method provides a convenient wrapper around Redis' native `MULTI` and `EXEC` commands. The `transaction` method accepts a closure as its only argument. This closure will receive a Redis connection instance and may issue any commands it would like to this instance. All of the Redis commands issued within the closure will be executed in a single, atomic transaction: -->
`Redis` 파사드의 `transaction` 메서드는 Redis의 `MULTI`와 `EXEC` 명령어를 간편하게 감싸주는 래퍼입니다. `transaction` 메서드는 하나의 클로저(익명 함수)를 받아, 이 클로저로 Redis 연결 인스턴스를 전달합니다. 클로저 내부에서는 원하는 만큼 명령어를 실행할 수 있고, 해당 명령어들은 모두 하나의 원자적(atomic) 트랜잭션으로 실행됩니다.

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는, 트랜잭션 내에서 Redis로부터 값을 조회할 수 없습니다. 트랜잭션은 완전히 원자적으로 실행되며, 클로저 내부의 모든 명령어가 끝난 후에야 실제 실행이 시작됨을 기억하세요.

<!-- #### Lua Scripts -->
#### Lua Scripts

<!-- The `eval` method provides another method of executing multiple Redis commands in a single, atomic operation. However, the `eval` method has the benefit of being able to interact with and inspect Redis key values during that operation. Redis scripts are written in the [Lua programming language](https://www.lua.org). -->
`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 작업으로 실행하는 또 다른 방법입니다. 특히 `eval` 메서드는 해당 작업에서 Redis 키의 값을 읽고, 조건을 판단하여 동적으로 명령을 실행할 수 있습니다. Redis 스크립트는 [Lua programming language](https://www.lua.org)로 작성해야 합니다.

<!-- The `eval` method can be a bit scary at first, but we'll explore a basic example to break the ice. The `eval` method expects several arguments. First, you should pass the Lua script (as a string) to the method. Secondly, you should pass the number of keys (as an integer) that the script interacts with. Thirdly, you should pass the names of those keys. Finally, you may pass any other additional arguments that you need to access within your script. -->
`eval` 메서드는 처음에는 다소 어렵게 느껴질 수 있지만, 기본 예시를 통해 차근차근 살펴보겠습니다. `eval` 메서드는 여러 개의 인수를 받습니다. 먼저 Lua 스크립트 자체(문자열), 두 번째로는 이 스크립트에서 다루는 키의 개수(정수), 세 번째부터는 해당 키들의 이름, 마지막으로 나머지 추가 인수들을 순서대로 전달해야 합니다.

<!-- In this example, we will increment a counter, inspect its new value, and increment a second counter if the first counter's value is greater than five. Finally, we will return the value of the first counter: -->
아래 예시는 카운터를 증가시키고 새 값을 검사하여, 5보다 크면 두 번째 카운터를 추가로 증가시킵니다. 마지막엔 첫 번째 카운터의 값을 반환합니다.

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
> Redis 스크립팅에 관한 더 자세한 내용은 [Redis documentation](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
<!-- ### Pipelining Commands -->
### Pipelining Commands

<!-- Sometimes you may need to execute dozens of Redis commands. Instead of making a network trip to your Redis server for each command, you may use the `pipeline` method. The `pipeline` method accepts one argument: a closure that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be sent to the Redis server at the same time to reduce network trips to the server. The commands will still be executed in the order they were issued: -->
수십 개의 Redis 명령어를 실행해야 할 때, 각각을 서버에 따로따로 전송하면 네트워크 비용이 큽니다. 이럴 때는 `pipeline` 메서드를 사용하세요. `pipeline` 메서드는 Redis 인스턴스를 인수로 받는 클로저를 전달받아, 해당 클로저 내에서 수행한 모든 명령어를 한 번에 처리합니다. 명령어들은 실행 순서를 그대로 유지합니다.

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
Laravel은 Redis의 `publish` 및 `subscribe` 명령어에 대한 편리한 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에 대해 메시지를 듣고(publish: 송신, subscribe: 수신) 보낼 수 있도록 해줍니다. 다른 애플리케이션이나, 심지어 다른 언어로도 메시지를 동일 채널로 발행할 수 있으므로, 애플리케이션 또는 프로세스 간의 손쉬운 통신이 가능합니다.

<!-- First, let's set up a channel listener using the `subscribe` method. We'll place this method call within an [Artisan command](/docs/13.x/artisan) since calling the `subscribe` method begins a long-running process: -->
먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해봅니다. `subscribe` 메서드는 장시간 실행되는 프로세스이므로, 보통 [Artisan command](/docs/13.x/artisan) 내에 구현합니다.

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
이제 `publish` 메서드를 사용하여 해당 채널에 메시지를 발행할 수 있습니다.

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
`psubscribe` 메서드를 사용하면 와일드카드 채널에 구독할 수 있습니다. 이를 통해 모든 채널에 전송되는 메시지를 받아볼 수 있어, 활용도가 높습니다. 이때 채널 이름은 전달된 클로저의 두 번째 인수로 제공됩니다.

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
