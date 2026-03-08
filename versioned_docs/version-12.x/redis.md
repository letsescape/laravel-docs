# Redis (Redis)

- [소개](#introduction)
- [설정](#configuration)
    - [클러스터](#clusters)
    - [Predis](#predis)
    - [PhpRedis](#phpredis)
- [Redis와 상호작용하기](#interacting-with-redis)
    - [트랜잭션](#transactions)
    - [파이프라이닝 명령어](#pipelining-commands)
- [Pub / Sub](#pubsub)

<a name="introduction"></a>
## 소개 (Introduction)

[Redis](https://redis.io)는 오픈 소스이자 고급 키-값 저장소입니다. 종종 데이터 구조 서버(data structure server)라고도 불리는데, 이는 키에 [문자열](https://redis.io/docs/latest/develop/data-types/strings/), [해시](https://redis.io/docs/latest/develop/data-types/hashes/), [리스트](https://redis.io/docs/latest/develop/data-types/lists/), [셋](https://redis.io/docs/latest/develop/data-types/sets/), [정렬된 셋](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 등 다양한 데이터 구조를 담을 수 있기 때문입니다.

Laravel에서 Redis를 사용하기 전에, PECL을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장 프로그램을 설치하고 사용하는 것을 권장합니다. 이 확장 프로그램은 PHP 패키지보다 설치가 더 복잡할 수 있지만, Redis를 빈번하게 사용하는 애플리케이션에서는 더 나은 성능을 보여줄 수 있습니다. 만약 [Laravel Sail](/docs/12.x/sail)을 사용 중이라면, 이 확장 프로그램은 이미 애플리케이션의 Docker 컨테이너에 설치되어 있습니다.

PhpRedis 확장 프로그램을 설치할 수 없는 경우, Composer를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis는 PHP로만 작성된 Redis 클라이언트이며, 추가 확장 프로그램 없이 사용할 수 있습니다.

```shell
composer require predis/predis
```

<a name="configuration"></a>
## 설정 (Configuration)

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
#### 연결 스킴 설정

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
### 클러스터 (Clusters)

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

기본적으로 `options.cluster` 설정 값이 `redis`로 지정되어 있기 때문에, Laravel은 기본적으로 네이티브 Redis 클러스터링을 사용합니다. 네이티브 Redis 클러스터링은 장애 조치(failover)를 원활하게 처리하므로, 기본값으로 적합합니다.

Predis를 사용할 때는 클라이언트 측 샤딩(client-side sharding)도 지원합니다. 하지만, 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로, 다른 주요 데이터 저장소에서 다시 구할 수 있는 임시 캐시 데이터에 주로 적합합니다.

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
### Predis

Predis 패키지를 통해 Redis와 상호작용하고 싶다면, `REDIS_CLIENT` 환경 변수의 값을 반드시 `predis`로 지정해야 합니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],
```

기본 설정 옵션 외에, Predis는 각각의 Redis 서버에 대해 추가적인 [연결 파라미터](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이 추가 설정 옵션을 사용하고자 한다면, `config/database.php` 설정 파일의 Redis 서버 설정에 해당 옵션들을 추가하세요.

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

기본적으로 Laravel은 Redis와 통신하기 위해 PhpRedis 확장 프로그램을 사용합니다. Laravel에서 Redis와 통신할 때 사용할 클라이언트는 `redis.client` 설정 옵션의 값에 따라 결정되며, 이는 일반적으로 `REDIS_CLIENT` 환경 변수 값을 따릅니다.

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],
```

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
#### 재시도 및 백오프 설정

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

Predis 3.4.0 이상에서는 내장된 Retry 설정을 `Retry` 클래스를 통해 지원하며, `retry` 옵션을 설정하여 `NoBackoff`, `EqualBackoff`, `ExponentialBackoff` 중 원하는 전략을 사용할 수 있습니다.

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

Redis 연결은 TCP 대신 Unix 소켓을 사용하도록 설정할 수 있습니다. 이렇게 하면, 동일 서버 내 Redis 인스턴스와의 통신에서 TCP 오버헤드가 제거되어 더 나은 성능을 낼 수 있습니다. Unix 소켓을 사용하려면 `REDIS_HOST` 환경 변수를 Redis 소켓의 경로로, `REDIS_PORT`는 `0`으로 설정하면 됩니다.

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0
```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

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

현재 지원되는 직렬화기는 다음과 같습니다:
- `Redis::SERIALIZER_NONE` (기본값)
- `Redis::SERIALIZER_PHP`
- `Redis::SERIALIZER_JSON`
- `Redis::SERIALIZER_IGBINARY`
- `Redis::SERIALIZER_MSGPACK`

지원되는 압축 알고리즘은 다음과 같습니다:
- `Redis::COMPRESSION_NONE` (기본값)
- `Redis::COMPRESSION_LZF`
- `Redis::COMPRESSION_ZSTD`
- `Redis::COMPRESSION_LZ4`

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기 (Interacting With Redis)

여러 가지 메서드를 사용해 `Redis` [파사드](/docs/12.x/facades)를 통해 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 다이나믹 메서드를 지원하므로, [Redis 명령어](https://redis.io/commands)라면 어떤 것이든 파사드를 통해 호출할 수 있고, 해당 명령어가 직접 Redis로 전달됩니다. 아래 예시에서는 `get` 메서드를 통해 Redis의 `GET` 명령어를 호출합니다.

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

앞서 언급한 것처럼, Redis의 모든 명령어는 `Redis` 파사드를 통해 호출할 수 있습니다. Laravel은 매직 메서드를 이용해 명령어를 Redis 서버에 전달합니다. 만약 Redis 명령어가 인수를 필요로 한다면, 파사드의 해당 메서드에 그 인수를 그대로 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);
```

또는, `Redis` 파사드의 `command` 메서드를 사용해서 명령어 이름을 첫 번째 인수로, 값들을 배열 형태로 두 번째 인수로 넘겨 명령어를 전달할 수도 있습니다.

```php
$values = Redis::command('lrange', ['name', 5, 10]);
```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 파일에서 여러 개의 Redis 연결(서버)을 정의할 수 있습니다. 특정 Redis 연결 인스턴스를 얻으려면 `Redis` 파사드의 `connection` 메서드를 사용하면 됩니다.

```php
$redis = Redis::connection('connection-name');
```

기본 Redis 연결 인스턴스를 얻으려면, 추가 인수 없이 `connection` 메서드를 호출하세요.

```php
$redis = Redis::connection();
```

<a name="transactions"></a>
### 트랜잭션 (Transactions)

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

#### Lua 스크립트

`eval` 메서드는 여러 Redis 명령어를 하나의 원자적 작업으로 실행하는 또 다른 방법입니다. 특히 이 방법은 해당 작업에서 Redis 키의 값을 읽고, 조건을 판단하여 동적으로 명령을 실행할 수 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org)로 작성해야 합니다.

`eval` 메서드는 여러 개의 인수를 받습니다. 먼저 Lua 스크립트 자체(문자열), 두 번째로는 이 스크립트에서 다루는 키의 개수(정수), 세 번째부터는 해당 키들의 이름, 마지막으로 나머지 추가 인수들을 순서대로 전달해야 합니다.

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
> Redis 스크립팅에 관한 더 자세한 내용은 [Redis 공식 문서](https://redis.io/commands/eval)를 참고하세요.

<a name="pipelining-commands"></a>
### 파이프라이닝 명령어 (Pipelining Commands)

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
## Pub / Sub

Laravel은 Redis의 `publish` 및 `subscribe` 명령어에 대한 편리한 인터페이스를 제공합니다. 이 명령어들은 특정 "채널"에 대해 메시지를 듣고(publish: 송신, subscribe: 수신) 보낼 수 있도록 해줍니다. 다른 애플리케이션이나, 심지어 다른 언어로도 메시지를 동일 채널로 발행할 수 있으므로, 애플리케이션 또는 프로세스 간의 손쉬운 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용해 채널 리스너를 설정해봅니다. 이 메서드는 장시간 실행되는 프로세스이므로, 보통 [Artisan 명령어](/docs/12.x/artisan) 내에 구현합니다.

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
#### 와일드카드 구독

`psubscribe` 메서드를 사용하면 와일드카드 채널에 구독할 수 있습니다. 이를 통해 모든 채널에 전송되는 메시지를 받아볼 수 있어, 활용도가 높습니다. 이때 채널 이름은 전달된 클로저의 두 번째 인수로 제공됩니다.

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});
```
