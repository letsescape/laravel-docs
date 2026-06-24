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
애플리케이션에서 데이터를 가져오거나 처리하는 작업 중에는 CPU를 많이 사용하거나 완료하는 데 몇 초가 걸리는 경우가 있을 수 있습니다. 이런 경우, 가져온 데이터를 일정 시간 동안 캐시에 저장해 두면 동일한 데이터에 대한 이후 요청에서 빠르게 값을 가져올 수 있습니다. 일반적으로 캐시된 데이터는 [Memcached](https://memcached.org)나 [Redis](https://redis.io)처럼 속도가 매우 빠른 데이터 저장소에 보관됩니다.

<!-- Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application. -->
다행히도, Laravel은 다양한 캐시 백엔드를 위한 직관적이고 통합된 API를 제공하므로, 빠른 데이터 조회의 이점을 누리면서 웹 애플리케이션의 속도를 크게 향상시킬 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache driver you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests. -->
애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전체에 기본으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등 널리 사용되는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버도 사용할 수 있으며, `array` 및 "null" 캐시 드라이버는 자동화된 테스트에 편리하게 활용할 수 있습니다.

<!-- The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects on the server's filesystem. For larger applications, it is recommended that you use a more robust driver such as Memcached or Redis. You may even configure multiple cache configurations for the same driver. -->
캐시 설정 파일에는 이 외에도 여러 가지 옵션들이 포함되어 있으며, 파일 내부에 주석으로 설명되어 있으므로 꼭 한 번씩 읽어보는 것이 좋습니다. 기본적으로 Laravel은 `file` 캐시 드라이버를 사용하도록 구성되어 있으며, 이는 직렬화된 캐시 객체를 서버 파일 시스템에 저장합니다. 더 규모가 큰 애플리케이션에서는 Memcached나 Redis처럼 성능이 뛰어난 드라이버 사용을 권장합니다. 동일한 드라이버에 대해 여러 개의 캐시 설정을 구성하는 것도 가능합니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to set up a table to contain the cache items. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 테이블을 먼저 생성해야 합니다. 아래는 테이블 생성을 위한 예시 `Schema` 선언입니다:

```
Schema::create('cache', function (Blueprint $table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!NOTE]
> `php artisan cache:table` Artisan 명령어를 사용하면 위와 같은 스키마로 마이그레이션 파일을 쉽게 생성할 수 있습니다.

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)를 설치해야 합니다. `config/cache.php` 설정 파일에서 모든 Memcached 서버를 나열할 수 있습니다. 해당 파일에는 시작을 위한 `memcached.servers` 항목이 이미 포함되어 있습니다:

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
필요하다면, `host` 옵션에 UNIX 소켓 경로를 지정할 수도 있습니다. 이 경우 `port` 옵션은 반드시 `0`으로 설정해야 합니다:

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
Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/10.x/sail)에는 이미 이 확장 기능이 포함되어 있으며, [Laravel Forge](https://forge.laravel.com)나 [Laravel Vapor](https://vapor.laravel.com) 같은 공식 Laravel 호스팅 플랫폼에서도 기본적으로 PhpRedis 확장 기능이 설치되어 있습니다.

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/10.x/redis#configuration). -->
Redis 설정 방법에 대한 더 자세한 내용은 [Laravel documentation page](/docs/10.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within your application's `cache` configuration file. -->
[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블 이름은 `cache`가 되어야 합니다. 하지만 실제로는 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.table` 값에 따라 테이블 이름을 결정해야 합니다.

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
이 테이블에는 또한 문자열 타입의 파티션 키가 필요하며, 키의 이름 역시 `cache` 설정 파일 내 `stores.dynamodb.attributes.key` 항목과 일치해야 합니다. 기본적으로 이 파티션 키의 이름은 `key`입니다.

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining a Cache Instance -->
### Obtaining a Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
캐시 스토어 인스턴스를 얻기 위해 `Cache` 파사드를 사용할 수 있으며, 이 문서 전반에서도 이를 사용해 설명하겠습니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 실제 구현체에 간단하고 편리하게 접근할 수 있도록 해줍니다:

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
`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 스토어에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일 내 `stores` 배열에 정의된 이름과 일치해야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From the Cache -->
### Retrieving Items From the Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
캐시에서 값을 가져올 때는 `Cache` 파사드의 `get` 메서드를 사용합니다. 만약 해당 아이템이 캐시에 없으면 `null`이 반환됩니다. 필요하다면 `get` 메서드에 두 번째 인자로 아이템이 없을 때 반환할 기본값을 설정할 수도 있습니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
기본값을 클로저로 전달할 수도 있습니다. 이 경우, 지정한 아이템이 캐시에 없으면 클로저 결과가 반환됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
<!-- #### Determining Item Existence -->
#### Determining Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` 메서드는 캐시에 해당 아이템이 있는지 확인할 때 사용합니다. 아이템이 존재하더라도 값이 `null`이면 `false`를 반환합니다:

```
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment`와 `decrement` 메서드는 캐시에 저장된 정수 값을 증가 또는 감소시킬 때 사용합니다. 두 메서드 모두 두 번째 인자로 얼마나 증가/감소시킬지 숫자 값을 받을 수 있습니다:

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
캐시에서 값을 가져오되, 없다면 기본 값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오되, 존재하지 않으면 데이터베이스에서 가져와서 캐시에 추가하고 싶을 수 있습니다. 이럴 때는 `Cache::remember` 메서드를 사용합니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
만약 캐시에 해당 아이템이 없다면, `remember` 메서드에 전달한 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
항상 캐시에 값을 가져오거나, 없으면 영구적으로 저장하고 싶다면 `rememberForever` 메서드를 사용할 수 있습니다:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve and Delete -->
#### Retrieve and Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
캐시에서 아이템을 가져온 뒤, 해당 아이템을 즉시 삭제해야 한다면 `pull` 메서드를 사용합니다. `get` 메서드와 마찬가지로, 만약 캐시에 값이 없으면 `null`이 반환됩니다:

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items in the Cache -->
### Storing Items in the Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
캐시에 값을 저장할 때는 `Cache` 파사드의 `put` 메서드를 사용합니다:

```
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
`put` 메서드에 저장 시간을 전달하지 않으면, 값은 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
저장 시간은 정수(초) 값 대신, 캐시 만료 시점을 나타내는 `DateTime` 인스턴스로도 지정할 수 있습니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
<!-- #### Store if Not Present -->
#### Store if Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` 메서드는 해당 아이템이 캐시에 이미 없다면 추가해 줍니다. 실제로 캐시에 추가된 경우에는 `true`를, 그렇지 않으면(이미 존재할 경우) `false`를 반환합니다. `add`는 원자적 연산입니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` 메서드를 사용하면 값을 캐시에 영구적으로 저장할 수 있습니다. 이 값들은 만료되지 않으므로, 삭제할 때는 반드시 `forget` 메서드로 수동 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "영구"로 저장된 아이템도 캐시 용량이 가득 차면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From the Cache -->
### Removing Items From the Cache

<!-- You may remove items from the cache using the `forget` method: -->
캐시에서 값을 제거하려면 `forget` 메서드를 사용합니다:

```
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
만료 시간을 0 또는 음수로 주면 해당 아이템이 즉시 삭제됩니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
캐시에 저장된 모든 값을 한 번에 삭제하려면 `flush` 메서드를 사용하세요:

```
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시하면 설정한 캐시 "접두사(prefix)"와 관계없이 모든 항목이 삭제됩니다. 여러 애플리케이션이 캐시를 공유 중이라면 이 점을 반드시 유의하세요.

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` 파사드를 사용하는 것 외에도, 전역 `cache` 함수를 통해서도 값을 저장하거나 가져올 수 있습니다. `cache` 함수에 문자열 인자 하나만 전달하면 해당 키에 해당하는 값을 반환합니다:

```
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
키-값 쌍의 배열과 만료 시간을 인자로 주면, 해당 값들을 지정한 시간 동안 캐시에 저장합니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
아무 인수 없이 `cache` 함수를 호출하면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환하므로, 다른 캐싱 관련 메서드도 사용할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수를 테스트할 때에도 [testing the facade](/docs/10.x/mocking#mocking-facades)처럼 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 드라이버 중 하나가 설정되어 있어야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="atomic-locks-prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to setup a table to contain your application's cache locks. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버를 사용하여 원자적 락 기능을 이용하려면, 캐시 락 정보를 저장할 테이블을 생성해야 합니다. 아래는 테이블을 위한 예시 `Schema` 선언입니다:

```
Schema::create('cache_locks', function (Blueprint $table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

> [!NOTE]
> `cache:table` Artisan 명령어로 데이터베이스용 캐시 테이블을 생성했다면, 해당 마이그레이션에는 이미 `cache_locks` 테이블 정의가 포함되어 있습니다.

<a name="managing-locks"></a>
<!-- ### Managing Locks -->
### Managing Locks

<!-- Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Forge](https://forge.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method: -->
원자적 락을 사용하면 분산 환경에서도 레이스 컨디션을 걱정하지 않고 락을 제어할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 한 번에 하나의 원격 작업만 실행하도록 원자적 락을 사용합니다. 락 생성과 관리는 `Cache::lock` 메서드로 할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
또한, `get` 메서드에 클로저를 전달할 수도 있습니다. 이 클로저가 실행된 후 락은 자동으로 해제됩니다:

```
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock can not be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
락을 요청할 때 곧바로 획득할 수 없으면, 지정한 시간(초) 동안 락이 풀릴 때까지 대기시키는 것도 가능합니다. 만약 해당 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

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
위의 예시는 `block` 메서드에 클로저를 전달하여 더 간결하게 사용할 수 있습니다. 클로저를 넘기면 지정한 시간만큼 락 획득을 시도하고, 클로저 실행 후 자동으로 락을 해제합니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
때로는 하나의 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 할 수도 있습니다. 예를 들어, 웹 요청에서 락을 획득하고, 그 요청으로 트리거된 큐 작업이 끝날 때 락을 해제하고 싶을 수 있습니다. 이런 경우엔 락이 가진 "오너 토큰(owner token)"을 큐 작업에 전달해서, 해당 토큰을 사용해 락을 복원하고 해제해야 합니다.

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
예를 들어, 아래 코드에서는 락을 획득하면 큐 작업을 디스패치하며, 락의 오너 토큰을 `owner` 메서드를 통해 같이 전달합니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
큐 작업(`ProcessPodcast` 잡)에서는 전달받은 오너 토큰을 사용해 락을 복원하고 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
현재 오너와 관계없이 즉시 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

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
커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [contract](/docs/10.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시 구현은 다음과 비슷할 수 있습니다:

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
이제 각 메서드를 MongoDB 연결을 사용하여 실제로 동작하도록 구현하면 됩니다. 각 메서드의 구현 예시는 [Laravel framework source code](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore` 클래스를 참고해 보세요. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 통해 커스텀 드라이버 등록을 완료할 수 있습니다:

```
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 두는 것도 좋은 방법입니다. Laravel은 디렉터리 구조를 강제하지 않으니 본인에게 맞게 자유롭게 구성해도 괜찮습니다.

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class: -->
Laravel에 커스텀 캐시 드라이버를 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 일부 서비스 프로바이더가 `boot` 메서드 내에서 캐시 값을 읽을 수 있기 때문에, 커스텀 드라이버 등록은 `booting` 콜백 내에서 처리해야 합니다. `booting` 콜백을 사용하면 커스텀 드라이버 등록이 모든 서비스 프로바이더의 `register` 메서드가 호출된 뒤, 각 서비스 프로바이더의 `boot` 메서드가 호출되기 직전에 완료됩니다. 다음과 같이, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 등록할 수 있습니다:

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
`extend` 메서드에 전달하는 첫 번째 인자는 드라이버 이름입니다. 이 값은 `config/cache.php`의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 클로저에는 [service container](/docs/10.x/container) 인스턴스인 `$app`이 전달됩니다.

<!-- Once your extension is registered, update your `config/cache.php` configuration file's `driver` option to the name of your extension. -->
확장이 모두 등록되면, `config/cache.php` 설정 파일의 `driver` 옵션을 커스텀 드라이버 이름으로 변경하세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for the [events](/docs/10.x/events) fired by the cache. Typically, you should place these event listeners within your application's `App\Providers\EventServiceProvider` class: -->
캐시 작업마다 코드를 실행하고 싶다면, 캐시에서 발생하는 [events](/docs/10.x/events)를 리스닝하면 됩니다. 이벤트 리스너는 보통 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 정의합니다:
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
