<!-- # Redis -->
# Redis

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Clusters](#clusters)
    - [Predis](#predis)
    - [phpredis](#phpredis)
- [Interacting With Redis](#interacting-with-redis)
    - [Transactions](#transactions)
    - [Pipelining Commands](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Redis](https://redis.io) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain [strings](https://redis.io/topics/data-types#strings), [hashes](https://redis.io/topics/data-types#hashes), [lists](https://redis.io/topics/data-types#lists), [sets](https://redis.io/topics/data-types#sets), and [sorted sets](https://redis.io/topics/data-types#sorted-sets). -->
[Redis](https://redis.io)는 오픈 소스의 고급 키-값 저장소입니다. 키에 [strings](https://redis.io/topics/data-types#strings), [hashes](https://redis.io/topics/data-types#hashes), [lists](https://redis.io/topics/data-types#lists), [sets](https://redis.io/topics/data-types#sets), [sorted sets](https://redis.io/topics/data-types#sorted-sets) 등 다양한 데이터 구조를 저장할 수 있어서 종종 데이터 구조 서버라고도 불립니다.

<!-- Before using Redis with Laravel, we encourage you to install and use the [phpredis](https://github.com/phpredis/phpredis) PHP extension via PECL. The extension is more complex to install compared to "user-land" PHP packages but may yield better performance for applications that make heavy use of Redis. If you are using [Laravel Sail](/docs/9.x/sail), this extension is already installed in your application's Docker container. -->
Laravel에서 Redis를 사용하려면 [phpredis](https://github.com/phpredis/phpredis) PHP 확장 프로그램을 PECL을 통해 설치해서 사용하는 것을 권장합니다. 이 확장 프로그램은 일반 사용자용 PHP 패키지에 비해 설치가 다소 복잡하지만, Redis를 많이 활용하는 애플리케이션에서는 더 나은 성능을 기대할 수 있습니다. 만약 [Laravel Sail](/docs/9.x/sail)을 사용한다면, 해당 확장 프로그램이 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

<!-- If you are unable to install the phpredis extension, you may install the `predis/predis` package via Composer. Predis is a Redis client written entirely in PHP and does not require any additional extensions: -->
phpredis 확장 프로그램을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치하여 사용할 수 있습니다. Predis는 PHP로만 작성된 Redis 클라이언트로, 별도의 추가 확장 프로그램이 필요하지 않습니다:

```shell
composer require predis/predis
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- You may configure your application's Redis settings via the `config/database.php` configuration file. Within this file, you will see a `redis` array containing the Redis servers utilized by your application: -->
애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 관리할 수 있습니다. 이 파일에는 애플리케이션에서 사용할 Redis 서버 정보를 담고 있는 `redis` 배열이 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

    'cache' => [
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_CACHE_DB', 1),
    ],

],
```

<!-- Each Redis server defined in your configuration file is required to have a name, host, and a port unless you define a single URL to represent the Redis connection: -->
설정 파일에서 정의하는 각 Redis 서버에는 이름, 호스트, 포트 정보가 필요합니다. 대신, Redis 연결을 하나의 URL로 표현하고자 할 때는 해당 정보를 명시하지 않아도 됩니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],
```

<a name="configuring-the-connection-scheme"></a>
<!-- #### Configuring The Connection Scheme -->
#### Configuring The Connection Scheme

<!-- By default, Redis clients will use the `tcp` scheme when connecting to your Redis servers; however, you may use TLS / SSL encryption by specifying a `scheme` configuration option in your Redis server's configuration array: -->
기본적으로 Redis 클라이언트는 Redis 서버와 연결할 때 `tcp` 방식을 사용합니다. 하지만, `scheme` 설정 옵션을 지정해서 TLS/SSL 암호화 연결도 사용할 수 있습니다. 이 옵션은 각 Redis 서버의 설정 배열에 포함시킵니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'default' => [
        'scheme' => 'tls',
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', 6379),
        'database' => env('REDIS_DB', 0),
    ],

],
```

<a name="clusters"></a>
<!-- ### Clusters -->
### Clusters

<!-- If your application is utilizing a cluster of Redis servers, you should define these clusters within a `clusters` key of your Redis configuration. This configuration key does not exist by default so you will need to create it within your application's `config/database.php` configuration file: -->
애플리케이션에서 여러 대의 Redis 서버로 클러스터를 구성하여 사용한다면, Redis 설정에서 `clusters` 키를 작성하여 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로, 애플리케이션의 `config/database.php` 파일 내에 직접 추가해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        'default' => [
            [
                'host' => env('REDIS_HOST', 'localhost'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', 6379),
                'database' => 0,
            ],
        ],
    ],

],
```

<!-- By default, clusters will perform client-side sharding across your nodes, allowing you to pool nodes and create a large amount of available RAM. However, client-side sharding does not handle failover; therefore, it is primarily suited for transient cached data that is available from another primary data store. -->
기본적으로 클러스터는 클라이언트-사이드 샤딩(Client-side Sharding)을 이용해서 여러 노드에 데이터를 분산 저장하여, 많은 RAM을 사용할 수 있도록 해줍니다. 그러나 클라이언트-사이드 샤딩은 장애 발생 시 자동 복구(Failover)를 지원하지 않기 때문에, 다른 주 데이터 저장소와 연동되는 임시 캐시 데이터 저장용으로 주로 사용됩니다.

<!-- If you would like to use native Redis clustering instead of client-side sharding, you may specify this by setting the `options.cluster` configuration value to `redis` within your application's `config/database.php` configuration file: -->
클라이언트-사이드 샤딩이 아닌, Redis의 네이티브 클러스터링 기능을 사용하려면, `options.cluster` 설정 값을 `redis`로 변경해야 합니다. 이 설정도 애플리케이션의 `config/database.php` 파일에 추가해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
    ],

    'clusters' => [
        // ...
    ],

],
```

<a name="predis"></a>
<!-- ### Predis -->
### Predis

<!-- If you would like your application to interact with Redis via the Predis package, you should ensure the `REDIS_CLIENT` environment variable's value is `predis`: -->
애플리케이션에서 Predis 패키지를 이용해 Redis와 상호작용하려면, `REDIS_CLIENT` 환경 변수 값에 `predis`를 설정해야 합니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

<!-- In addition to the default `host`, `port`, `database`, and `password` server configuration options, Predis supports additional [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters) that may be defined for each of your Redis servers. To utilize these additional configuration options, add them to your Redis server configuration in your application's `config/database.php` configuration file: -->
Predis는 기본 `host`, `port`, `database`, `password` 외에도, 각 Redis 서버별로 추가적인 [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정 옵션들은 애플리케이션의 `config/database.php` 파일에서 각 Redis 서버 설정에 추가할 수 있습니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', 6379),
    'database' => 0,
    'read_write_timeout' => 60,
],
```

<a name="the-redis-facade-alias"></a>
<!-- #### The Redis Facade Alias -->
#### The Redis Facade Alias

<!-- Laravel's `config/app.php` configuration file contains an `aliases` array which defines all of the class aliases that will be registered by the framework. By default, no `Redis` alias is included because it would conflict with the `Redis` class name provided by the phpredis extension. If you are using the Predis client and would like to add a `Redis` alias, you may add it to the `aliases` array in your application's `config/app.php` configuration file: -->
Laravel의 `config/app.php` 설정 파일에는 프레임워크에서 등록할 클래스 별칭(alias)들이 정의된 `aliases` 배열이 있습니다. 기본적으로 `Redis` 별칭은 phpredis 확장 프로그램이 제공하는 `Redis` 클래스명과 충돌할 수 있어서 포함되어 있지 않습니다. Predis 클라이언트를 사용하고 `Redis` 별칭을 추가하고 싶다면, `config/app.php`의 `aliases` 배열에 아래와 같이 추가하면 됩니다:

```
'aliases' => Facade::defaultAliases()->merge([
    'Redis' => Illuminate\Support\Facades\Redis::class,
])->toArray(),
```

<a name="phpredis"></a>
<!-- ### phpredis -->
### phpredis

<!-- By default, Laravel will use the phpredis extension to communicate with Redis. The client that Laravel will use to communicate with Redis is dictated by the value of the `redis.client` configuration option, which typically reflects the value of the `REDIS_CLIENT` environment variable: -->
기본적으로 Laravel은 phpredis 확장 프로그램을 통해 Redis와 통신합니다. 실제로 Laravel이 어떤 클라이언트로 Redis와 통신할지는 `redis.client` 설정 값에 따라 결정되며, 이 값은 보통 `REDIS_CLIENT` 환경 변수와 연동됩니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // Rest of Redis configuration...
],
```

<!-- In addition to the default `scheme`, `host`, `port`, `database`, and `password` server configuration options, phpredis supports the following additional connection parameters: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, and `context`. You may add any of these options to your Redis server configuration in the `config/database.php` configuration file: -->
phpredis는 기본 `scheme`, `host`, `port`, `database`, `password` 외에도 다음과 같은 추가 연결 파라미터를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `timeout`, `context`. 이 중 필요한 옵션을 `config/database.php` 설정 파일 내 Redis 서버 설정에 자유롭게 추가할 수 있습니다:

```
'default' => [
    'host' => env('REDIS_HOST', 'localhost'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', 6379),
    'database' => 0,
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],
```

<a name="phpredis-serialization"></a>
<!-- #### phpredis Serialization & Compression -->
#### phpredis Serialization & Compression

<!-- The phpredis extension may also be configured to use a variety of serialization and compression algorithms. These algorithms can be configured via the `options` array of your Redis configuration: -->
phpredis 확장 프로그램은 다양한 직렬화(Serialization) 및 압축(Compression) 알고리즘을 지원하며, 이는 Redis 설정의 `options` 배열에서 지정할 수 있습니다:

```
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // Rest of Redis configuration...
],
```

<!-- Currently supported serialization algorithms include: `Redis::SERIALIZER_NONE` (default), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, and `Redis::SERIALIZER_MSGPACK`. -->
지원되는 직렬화 알고리즘은 다음과 같습니다: `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`.

<!-- Supported compression algorithms include: `Redis::COMPRESSION_NONE` (default), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, and `Redis::COMPRESSION_LZ4`. -->
지원되는 압축 알고리즘은 다음과 같습니다: `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`.

<a name="interacting-with-redis"></a>
<!-- ## Interacting With Redis -->
## Interacting With Redis

<!-- You may interact with Redis by calling various methods on the `Redis` [facade](/docs/9.x/facades). The `Redis` facade supports dynamic methods, meaning you may call any [Redis command](https://redis.io/commands) on the facade and the command will be passed directly to Redis. In this example, we will call the Redis `GET` command by calling the `get` method on the `Redis` facade: -->
[facade](/docs/9.x/facades)인 `Redis`를 통해 다양한 Redis 메서드를 호출하여 Redis와 직접 상호작용할 수 있습니다. `Redis` 퍼사드는 다이나믹 메서드를 지원하므로, 어떤 [Redis command](https://redis.io/commands)든 그대로 퍼사드에 호출하면 해당 명령어가 Redis 서버로 전달됩니다. 아래 예시에서는 Redis의 `GET` 명령어를 `Redis` 퍼사드의 `get` 메서드로 호출하는 방법을 보여줍니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Redis;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}
```

<!-- As mentioned above, you may call any of Redis' commands on the `Redis` facade. Laravel uses magic methods to pass the commands to the Redis server. If a Redis command expects arguments, you should pass those to the facade's corresponding method: -->
위에서 설명한 것처럼, `Redis` 퍼사드를 통해 어떤 Redis 명령어도 호출할 수 있습니다. Laravel은 매직 메서드(magic method)를 사용해서 명령어를 Redis 서버로 전달합니다. 만약 Redis 명령어에 인수가 필요한 경우, 해당 인수들을 퍼사드의 해당 메서드에 그대로 전달하면 됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

<!-- Alternatively, you may pass commands to the server using the `Redis` facade's `command` method, which accepts the name of the command as its first argument and an array of values as its second argument: -->
또 다른 방법으로, `Redis` 퍼사드의 `command` 메서드를 활용해 서버로 명령어를 직접 전달할 수도 있습니다. 이 방법은 첫 번째 인자로 명령어 이름, 두 번째 인자로 값들의 배열을 받습니다:

```
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
<!-- #### Using Multiple Redis Connections -->
#### Using Multiple Redis Connections

<!-- Your application's `config/database.php` configuration file allows you to define multiple Redis connections / servers. You may obtain a connection to a specific Redis connection using the `Redis` facade's `connection` method: -->
애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결을 사용하려면, `Redis` 퍼사드의 `connection` 메서드를 이용하면 됩니다:

```
$redis = Redis::connection('connection-name');
```

<!-- To obtain an instance of the default Redis connection, you may call the `connection` method without any additional arguments: -->
기본 Redis 연결 인스턴스를 얻고 싶다면 인자 없이 `connection` 메서드를 호출하면 됩니다:

```
$redis = Redis::connection();
```

<a name="transactions"></a>
<!-- ### Transactions -->
### Transactions

<!-- The `Redis` facade's `transaction` method provides a convenient wrapper around Redis' native `MULTI` and `EXEC` commands. The `transaction` method accepts a closure as its only argument. This closure will receive a Redis connection instance and may issue any commands it would like to this instance. All of the Redis commands issued within the closure will be executed in a single, atomic transaction: -->
`Redis` 퍼사드의 `transaction` 메서드는 Redis의 기본 `MULTI`와 `EXEC` 명령어를 래핑해서 편리하게 트랜잭션을 사용할 수 있도록 지원합니다. `transaction` 메서드는 클로저(closure)를 인자로 받는데, 이 클로저는 Redis 연결 인스턴스를 전달받으며, 이 인스턴스에 원하는 Redis 명령어를 자유롭게 사용할 수 있습니다. 클로저 내에서 실행된 모든 Redis 명령어는 하나의 원자적(atomic) 트랜잭션으로 실행됩니다.

```
use Illuminate\Support\Facades\Redis;

Redis::transaction(function ($redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는 명령어 실행 중간에 Redis로부터 값을 조회할 수 없습니다. 트랜잭션은 하나의 원자적 연산으로 처리되므로, 클로저가 모든 명령어를 실행한 뒤에야 실제로 실행됩니다.

<!-- #### Lua Scripts -->
#### Lua Scripts

<!-- The `eval` method provides another method of executing multiple Redis commands in a single, atomic operation. However, the `eval` method has the benefit of being able to interact with and inspect Redis key values during that operation. Redis scripts are written in the [Lua programming language](https://www.lua.org). -->
`eval` 메서드를 사용하면 여러 Redis 명령어를 하나의 원자적 작업으로 처리할 수 있는 또 다른 방법을 제공합니다. 특히, `eval` 메서드는 해당 작업 중에 Redis의 키 값을 조회하거나 조작할 수 있는 장점이 있습니다. Redis 스크립트는 [Lua programming language](https://www.lua.org)로 작성합니다.

<!-- The `eval` method can be a bit scary at first, but we'll explore a basic example to break the ice. The `eval` method expects several arguments. First, you should pass the Lua script (as a string) to the method. Secondly, you should pass the number of keys (as an integer) that the script interacts with. Thirdly, you should pass the names of those keys. Finally, you may pass any other additional arguments that you need to access within your script. -->
`eval` 메서드는 처음에는 다소 어렵게 느껴질 수 있지만, 기본 예시를 통해 차근차근 살펴보겠습니다. `eval` 메서드는 여러 인수를 받습니다. 먼저, 실행할 Lua 스크립트 문자열을 전달해야 합니다. 두 번째는 스크립트가 참조하는 키의 개수(정수)를 지정합니다. 세 번째로는 그 키 이름(들)을 나열합니다. 추가적으로 스크립트 내부에서 사용할 수 있는 기타 인수들도 뒤에 전달할 수 있습니다.

<!-- In this example, we will increment a counter, inspect its new value, and increment a second counter if the first counter's value is greater than five. Finally, we will return the value of the first counter: -->
아래 예시는 카운터 값을 증가시키고, 그 값이 5보다 크면 두 번째 카운터를 추가로 증가시키며, 마지막으로 첫 번째 카운터 값을 반환합니다:

```
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');
```

> [!WARNING]
> Redis 스크립팅에 관한 더 자세한 내용은 [Redis documentation](https://redis.io/commands/eval)를 참고하시기 바랍니다.

<a name="pipelining-commands"></a>
<!-- ### Pipelining Commands -->
### Pipelining Commands

<!-- Sometimes you may need to execute dozens of Redis commands. Instead of making a network trip to your Redis server for each command, you may use the `pipeline` method. The `pipeline` method accepts one argument: a closure that receives a Redis instance. You may issue all of your commands to this Redis instance and they will all be sent to the Redis server at the same time to reduce network trips to the server. The commands will still be executed in the order they were issued: -->
한 번에 수십 개의 Redis 명령어를 실행해야 할 때, 각 명령어마다 서버에 네트워크 요청을 반복적으로 보내는 대신 `pipeline` 메서드를 사용하면 효율적으로 처리할 수 있습니다. `pipeline`은 하나의 인자(클로저)를 받으며, 이 클로저는 Redis 인스턴스를 전달받습니다. 모든 명령어는 이 인스턴스에 대해 실행되고, 명령어들은 한꺼번에 Redis 서버로 전송되어 반복적인 네트워크 왕복을 줄일 수 있습니다. 명령어는 발행된 순서대로 실행됩니다:

```
use Illuminate\Support\Facades\Redis;

Redis::pipeline(function ($pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});
```

<a name="pubsub"></a>
<!-- ## Pub / Sub -->
## Pub / Sub

<!-- Laravel provides a convenient interface to the Redis `publish` and `subscribe` commands. These Redis commands allow you to listen for messages on a given "channel". You may publish messages to the channel from another application, or even using another programming language, allowing easy communication between applications and processes. -->
Laravel은 Redis의 `publish`와 `subscribe` 명령어를 손쉽게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어들을 사용하면 특정 "채널"에서 메시지를 실시간으로 주고받을 수 있습니다. 다른 애플리케이션이나 심지어 다른 프로그래밍 언어로도 자유롭게 채널에 메시지를 발행(publish)할 수 있기 때문에, 여러 애플리케이션과 프로세스 간의 통신이 매우 쉽습니다.

<!-- First, let's setup a channel listener using the `subscribe` method. We'll place this method call within an [Artisan command](/docs/9.x/artisan) since calling the `subscribe` method begins a long-running process: -->
먼저, `subscribe` 메서드를 활용해 채널 리스너(listener)를 설정해봅니다. `subscribe` 메서드는 프로그램이 계속 실행되는 장기 실행 프로세스이기 때문에 [Artisan command](/docs/9.x/artisan) 안에 구현하는 것이 보통입니다:

```
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
     *
     * @return mixed
     */
    public function handle()
    {
        Redis::subscribe(['test-channel'], function ($message) {
            echo $message;
        });
    }
}
```

<!-- Now we may publish messages to the channel using the `publish` method: -->
이제 `publish` 메서드를 사용해서 해당 채널에 메시지를 발행할 수 있습니다:

```
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
`psubscribe` 메서드를 이용하면 와일드카드 패턴을 사용해 여러 채널의 모든 메시지를 구독할 수 있습니다. 이렇게 하면 모든 채널, 혹은 특정 패턴의 채널 메시지를 한 번에 수신할 수 있습니다. 클로저에는 두 번째 인자로 채널 이름이 전달됩니다.

```
Redis::psubscribe(['*'], function ($message, $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function ($message, $channel) {
    echo $message;
});
```
