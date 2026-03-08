# Redis

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라인 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스 기반의 고급 키-값 저장소(key-value store)입니다. 키에 [문자열(strings)](https://redis.io/docs/latest/develop/data-types/strings/), [해시(hashes)](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트(lists)](https://redis.io/docs/latest/develop/data-types/lists/), [셋(sets)](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋(sorted sets)](https://redis.io/docs/latest/develop/data-types/sorted-sets/)과 같은 다양한 데이터 구조를 저장할 수 있기 때문에 **데이터 구조 서버(data structure server)**라고도 불립니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장(extension)을 설치하여 사용하는 것을 권장합니다. 이 확장은 "user-land" PHP 패키지보다 설치 과정이 다소 복잡하지만, Redis를 많이 사용하는 애플리케이션에서는 더 높은 성능을 제공할 수 있습니다. 만약 [Laravel Sail](/docs/master/sail)을 사용하고 있다면, 이 확장은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

만약 PhpRedis 확장을 설치할 수 없는 환경이라면, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 순수 PHP로 작성된 Redis 클라이언트이며 추가 확장이 필요하지 않습니다.

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 Redis 설정은 `config/database.php` 설정 파일에서 구성할 수 있습니다. 이 파일에는 애플리케이션에서 사용하는 Redis 서버를 정의한 `redis` 배열이 포함되어 있습니다.

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

설정 파일에 정의된 각 Redis 서버는 이름, 호스트(host), 포트(port)를 가져야 합니다. 단일 URL을 사용해 Redis 연결을 표현하는 경우에는 예외입니다.

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
#### 연결 스킴 구성

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 그러나 Redis 서버 설정 배열에 `scheme` 옵션을 지정하면 TLS / SSL 암호화를 사용할 수 있습니다.

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
### 클러스터 (Clusters)

애플리케이션이 Redis 서버 클러스터를 사용하는 경우, Redis 설정의 `clusters` 키 안에 해당 클러스터를 정의해야 합니다. 이 설정 키는 기본적으로 존재하지 않으므로 애플리케이션의 `config/database.php` 설정 파일에 직접 추가해야 합니다.

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

기본적으로 Laravel은 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에 **Redis 네이티브 클러스터링(native Redis clustering)**을 사용합니다. Redis 클러스터링은 장애 발생 시 자동으로 대체 노드를 사용하는 **failover**를 원활하게 처리하기 때문에 좋은 기본 선택입니다.

Laravel은 Predis를 사용할 경우 **클라이언트 측 샤딩(client-side sharding)**도 지원합니다. 그러나 클라이언트 샤딩은 failover를 처리하지 못하므로, 일반적으로 다른 주요 데이터 저장소에서 다시 가져올 수 있는 **일시적인 캐시 데이터**에 적합합니다.

네이티브 Redis 클러스터 대신 클라이언트 샤딩을 사용하려면 애플리케이션의 `config/database.php` 파일에서 `options.cluster` 설정을 제거하면 됩니다.

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
### Predis

Predis 패키지를 통해 Redis와 상호작용하려면 `REDIS_CLIENT` 환경 변수의 값을 `predis`로 설정해야 합니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에도 Predis는 각 Redis 서버에 대해 추가적인 [connection parameters](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 옵션을 사용하려면 애플리케이션의 `config/database.php` 파일에 Redis 서버 설정에 추가하면 됩니다.

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
### PhpRedis

기본적으로 Laravel은 Redis와 통신하기 위해 PhpRedis 확장을 사용합니다. Laravel이 사용할 Redis 클라이언트는 `redis.client` 설정 값에 의해 결정되며, 일반적으로 `REDIS_CLIENT` 환경 변수 값을 반영합니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

기본 설정 옵션 외에도 PhpRedis는 다음과 같은 추가 연결 매개변수를 지원합니다.

`name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, `context`

이 옵션들은 `config/database.php` 파일의 Redis 서버 설정에 추가할 수 있습니다.

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
#### 재시도 및 백오프 설정

`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap` 옵션을 사용하여 PhpRedis 클라이언트가 Redis 서버에 재연결을 시도하는 방식을 설정할 수 있습니다.

지원되는 백오프 알고리즘은 다음과 같습니다.

`default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, `constant`

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

Predis 3.4.0 이상에서는 `Retry` 클래스를 사용하여 내장된 재시도 및 백오프 설정을 지원합니다. `retry` 옵션을 사용하고 다음 전략 중 하나를 선택하여 구성할 수 있습니다.

`NoBackoff`, `EqualBackoff`, `ExponentialBackoff`

```php
use Predis\Retry;
use Predis\Retry\Strategy\ExponentialBackoff;

'default' => [
    'url' => env('REDIS_URL'),
    // ...
    'retry' => new Retry(
        new ExponentialBackoff(
            env('REDIS_BACKOFF_BASE', 100),
            env('REDIS_BACKOFF_CAP', 1000),
            true, // Enables jitter
        ),
        env('REDIS_MAX_RETRIES', 3)
    )
],
```

<a name="unix-socket-connections"></a>
#### Unix 소켓 연결

Redis 연결은 TCP 대신 Unix 소켓을 사용하도록 구성할 수도 있습니다. 애플리케이션과 동일한 서버에서 실행되는 Redis 인스턴스에 연결하는 경우 TCP 오버헤드를 제거하여 더 나은 성능을 얻을 수 있습니다.

Redis가 Unix 소켓을 사용하도록 설정하려면 `REDIS_HOST` 환경 변수에 Redis 소켓 경로를 설정하고 `REDIS_PORT` 환경 변수 값을 `0`으로 설정합니다.

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장은 다양한 직렬화(serializer) 및 압축 알고리즘을 사용할 수 있도록 설정할 수 있습니다. 이러한 알고리즘은 Redis 설정의 `options` 배열에서 구성할 수 있습니다.

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

현재 지원되는 직렬화 옵션은 다음과 같습니다.

`Redis::SERIALIZER_NONE` (기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`

지원되는 압축 알고리즘은 다음과 같습니다.

`Redis::COMPRESSION_NONE` (기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

`Redis` [facade](/docs/master/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` facade는 **동적 메서드(dynamic methods)**를 지원하므로, 어떤 [Redis command](https://redis.io/commands)라도 facade에서 직접 호출할 수 있으며 해당 명령어는 Redis 서버로 전달됩니다.

다음 예제에서는 `Redis` facade의 `get` 메서드를 호출하여 Redis의 `GET` 명령어를 실행합니다.

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

앞서 설명한 것처럼 Redis의 모든 명령어를 `Redis` facade에서 호출할 수 있습니다. Laravel은 **매직 메서드(magic methods)**를 사용하여 명령어를 Redis 서버로 전달합니다. Redis 명령어가 인수를 요구하는 경우, 해당 인수를 facade 메서드에 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는 `Redis` facade의 `command` 메서드를 사용하여 명령어를 서버로 전달할 수도 있습니다. 이 메서드는 첫 번째 인수로 명령어 이름을, 두 번째 인수로 값 배열을 받습니다.

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 설정 파일에서는 여러 개의 Redis 연결 또는 서버를 정의할 수 있습니다. 특정 Redis 연결을 사용하려면 `Redis` facade의 `connection` 메서드를 사용합니다.

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 가져오려면 인수 없이 `connection` 메서드를 호출하면 됩니다.

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

`Redis` facade의 `transaction` 메서드는 Redis의 `MULTI` 및 `EXEC` 명령어를 편리하게 사용할 수 있도록 감싸는 래퍼(wrapper)를 제공합니다.

`transaction` 메서드는 하나의 인수로 **클로저(closure)**를 받습니다. 이 클로저는 Redis 연결 인스턴스를 전달받으며, 해당 인스턴스에 원하는 Redis 명령어를 실행할 수 있습니다. 클로저 내부에서 실행된 모든 Redis 명령어는 하나의 **원자적 트랜잭션(atomic transaction)**으로 실행됩니다.

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});
```

> [!WARNING]
> Redis 트랜잭션을 정의할 때는 Redis 연결에서 값을 조회할 수 없습니다. 트랜잭션은 하나의 원자적 작업으로 실행되며, 클로저 내부의 모든 명령어 실행이 끝난 뒤에 한 번에 실행된다는 점을 기억해야 합니다.

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 작업으로 실행하는 또 다른 방법을 제공합니다. 또한 이 메서드는 실행 중에 Redis 키 값을 확인하고 조작할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua programming language](https://www.lua.org)로 작성됩니다.

`eval` 메서드는 처음에는 다소 복잡해 보일 수 있지만, 간단한 예제로 살펴보겠습니다. `eval` 메서드는 여러 인수를 받습니다.

1. 첫 번째 인수: Lua 스크립트 문자열
2. 두 번째 인수: 스크립트가 사용하는 키의 개수(정수)
3. 세 번째 이후 인수: 해당 키 이름들
4. 이후 추가 인수: 스크립트 내부에서 사용할 추가 값

다음 예제에서는 카운터를 증가시키고, 그 새로운 값을 확인한 뒤 첫 번째 카운터 값이 5보다 크면 두 번째 카운터를 증가시킵니다. 마지막으로 첫 번째 카운터 값을 반환합니다.

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
> Redis 스크립팅에 대한 자세한 내용은 [Redis documentation](https://redis.io/commands/eval)을 참고하십시오.

<a name="pipelining-commands"></a>
### 파이프라인 명령어 (Pipelining Commands)

때로는 수십 개의 Redis 명령어를 실행해야 할 수도 있습니다. 이때 각 명령어마다 Redis 서버와 네트워크 통신을 수행하는 대신 `pipeline` 메서드를 사용할 수 있습니다.

`pipeline` 메서드는 하나의 인수로 **Redis 인스턴스를 전달받는 클로저**를 받습니다. 이 Redis 인스턴스에 여러 명령어를 실행하면, 해당 명령어들이 한 번에 Redis 서버로 전송되어 네트워크 왕복 횟수를 줄일 수 있습니다. 단, 명령어 실행 순서는 호출한 순서대로 유지됩니다.

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
## Pub / Sub

Laravel은 Redis의 `publish`와 `subscribe` 명령어를 쉽게 사용할 수 있는 인터페이스를 제공합니다. 이 명령어를 사용하면 특정 **채널(channel)**에서 메시지를 수신할 수 있습니다. 다른 애플리케이션이나 다른 프로그래밍 언어에서 해당 채널로 메시지를 발행(publish)할 수 있기 때문에 애플리케이션 간 또는 프로세스 간 통신을 쉽게 구현할 수 있습니다.

먼저 `subscribe` 메서드를 사용하여 채널 리스너를 설정해 보겠습니다. `subscribe` 메서드는 장시간 실행되는 프로세스를 시작하므로, 일반적으로 [Artisan command](/docs/master/artisan) 내부에서 호출합니다.

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

이제 `publish` 메서드를 사용하여 채널에 메시지를 발행할 수 있습니다.

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
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널을 구독할 수 있습니다. 이를 통해 모든 채널의 메시지를 수신하거나 특정 패턴의 채널을 구독할 수 있습니다. 채널 이름은 클로저의 두 번째 인수로 전달됩니다.

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```