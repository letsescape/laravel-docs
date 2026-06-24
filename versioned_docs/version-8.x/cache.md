<!-- # Cache -->
# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
    - [Obtaining A Cache Instance](#obtaining-a-cache-instance)
    - [Retrieving Items From The Cache](#retrieving-items-from-the-cache)
    - [Storing Items In The Cache](#storing-items-in-the-cache)
    - [Removing Items From The Cache](#removing-items-from-the-cache)
    - [The Cache Helper](#the-cache-helper)
- [Cache Tags](#cache-tags)
    - [Storing Tagged Cache Items](#storing-tagged-cache-items)
    - [Accessing Tagged Cache Items](#accessing-tagged-cache-items)
    - [Removing Tagged Cache Items](#removing-tagged-cache-items)
- [Atomic Locks](#atomic-locks)
    - [Driver Prerequisites](#lock-driver-prerequisites)
    - [Managing Locks](#managing-locks)
    - [Managing Locks Across Processes](#managing-locks-across-processes)
- [Adding Custom Cache Drivers](#adding-custom-cache-drivers)
    - [Writing The Driver](#writing-the-driver)
    - [Registering The Driver](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as [Memcached](https://memcached.org) or [Redis](https://redis.io). -->
애플리케이션에서 수행되는 데이터 조회나 처리 작업 가운데 일부는 CPU를 많이 사용하거나, 완료까지 몇 초가 걸릴 수 있습니다. 이런 경우, 조회된 데이터를 일정 시간 동안 캐시에 저장하여 동일한 데이터에 대한 이후 요청이 훨씬 빠르게 처리되도록 하는 것이 일반적입니다. 캐시된 데이터는 대개 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관합니다.

<!-- Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application. -->
다행히 Laravel은 다양한 캐시 백엔드를 위한 표현력 있고 통합된 API를 제공하며, 이를 통해 매우 빠른 데이터 조회 속도를 활용하고 웹 애플리케이션의 성능을 높일 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache driver you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests. -->
애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서는 어떤 캐시 드라이버를 애플리케이션 전반에서 기본으로 사용할지 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스와 같은 인기 있는 캐싱 백엔드를 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 "null" 드라이버는 자동화된 테스트에 유용한 간편한 캐시 백엔드를 제공합니다.

<!-- The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects on the server's filesystem. For larger applications, it is recommended that you use a more robust driver such as Memcached or Redis. You may even configure multiple cache configurations for the same driver. -->
캐시 설정 파일엔 그 외에도 여러 옵션이 포함되어 있으니, 반드시 파일 내용을 꼼꼼히 확인해 주세요. 기본적으로 Laravel은 `file` 캐시 드라이버를 사용하도록 설정되어 있는데, 이는 직렬화된 캐시 객체를 서버의 파일 시스템에 저장합니다. 규모가 더 큰 애플리케이션의 경우 Memcached 또는 Redis와 같은 더 견고한 드라이버 사용을 권장합니다. 동일한 드라이버에 대해 여러 개의 캐시 구성을 설정할 수도 있습니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to setup a table to contain the cache items. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버를 사용할 때는 캐시 항목을 저장할 테이블을 먼저 준비해야 합니다. 아래는 해당 테이블의 예시 `Schema` 선언입니다:

```
Schema::create('cache', function ($table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!TIP]
> `php artisan cache:table` 아티즌 명령어를 활용하면 위 구조에 맞는 마이그레이션 파일을 자동 생성할 수 있습니다.

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 명시할 수 있습니다. 해당 파일에는 시작용으로 사용할 수 있는 `memcached.servers` 항목이 이미 포함되어 있습니다:

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
필요하다면 `host` 옵션에 UNIX 소켓 경로를 지정할 수도 있습니다. 이때 `port` 옵션은 `0`으로 설정해야 합니다:

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

<!-- Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. [Laravel Sail](/docs/8.x/sail) already includes this extension. In addition, official Laravel deployment platforms such as [Laravel Forge](https://forge.laravel.com) and [Laravel Vapor](https://vapor.laravel.com) have the PhpRedis extension installed by default. -->
Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 이용해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/8.x/sail)은 이미 이 확장 모듈을 포함하고 있습니다. 또한 [Laravel Forge](https://forge.laravel.com)와 [Laravel Vapor](https://vapor.laravel.com)와 같은 공식 Laravel 배포 플랫폼에도 기본적으로 PhpRedis 확장 모듈이 설치되어 있습니다.

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/8.x/redis#configuration). -->
Redis 설정에 대한 자세한 내용은 [Laravel documentation page](/docs/8.x/redis#configuration)를 참고해 주세요.

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within your application's `cache` configuration file. -->
[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 반드시 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`로 지정합니다. 단, 애플리케이션의 `cache` 설정 파일에서 `stores.dynamodb.table` 항목에 지정한 값을 따라야 합니다.

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
또한, 이 테이블에는 파티션 키로 사용할 문자열 컬럼이 필요하며, 이 컬럼명은 애플리케이션의 `cache` 설정 파일의 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본값은 `key`입니다.

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining A Cache Instance -->
### Obtaining A Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
캐시 저장소 인스턴스를 얻으려면, 이 문서 전체에서 사용하게 될 `Cache` 파사드를 사용하면 됩니다. `Cache` 파사드는 Laravel에서 제공하는 캐시 계약의 실제 구현체에 간단하고 효율적으로 접근할 수 있게 해줍니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
     *
     * @return Response
     */
    public function index()
    {
        $value = Cache::get('key');

        //
    }
}
```

<a name="accessing-multiple-cache-stores"></a>
<!-- #### Accessing Multiple Cache Stores -->
#### Accessing Multiple Cache Stores

<!-- Using the `Cache` facade, you may access various cache stores via the `store` method. The key passed to the `store` method should correspond to one of the stores listed in the `stores` configuration array in your `cache` configuration file: -->
`Cache` 파사드를 사용하면 `store` 메서드를 통해 여러 캐시 저장소에 접근할 수 있습니다. `store`에 전달하는 키 값은 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From The Cache -->
### Retrieving Items From The Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
캐시에서 데이터를 가져올 때는 `Cache` 파사드의 `get` 메서드를 사용합니다. 해당 항목이 캐시에 존재하지 않으면 `null`이 반환됩니다. 원한다면 `get` 메서드에 두 번째 인수를 전달하여 해당 항목이 없을 때 반환받고 싶은 기본값을 지정할 수 있습니다:

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
기본값으로 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없을 때, 클로저의 반환값이 기본값으로 사용됩니다. 클로저를 사용하면 데이터베이스나 외부 서비스 등에서 기본값을 지연해서 조회할 수 있습니다:

```
$value = Cache::get('key', function () {
    return DB::table(...)->get();
});
```

<a name="checking-for-item-existence"></a>
<!-- #### Checking For Item Existence -->
#### Checking For Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` 메서드를 사용하면 캐시에 해당 항목이 존재하는지 확인할 수 있습니다. 이 메서드는 항목이 존재하더라도 값이 `null`이면 `false`를 반환합니다:

```
if (Cache::has('key')) {
    //
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment`와 `decrement` 메서드를 사용하면 캐시에 저장된 정수값을 손쉽게 증가 또는 감소시킬 수 있습니다. 두 메서드 모두 항목 값을 얼마나 증감할지 선택적으로 두 번째 인수로 전달할 수 있습니다:

```
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```

<a name="retrieve-store"></a>
<!-- #### Retrieve & Store -->
#### Retrieve & Store

<!-- Sometimes you may wish to retrieve an item from the cache, but also store a default value if the requested item doesn't exist. For example, you may wish to retrieve all users from the cache or, if they don't exist, retrieve them from the database and add them to the cache. You may do this using the `Cache::remember` method: -->
캐시에서 항목을 조회하되, 없으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어, 모든 사용자를 캐시에서 조회하고, 없으면 데이터베이스에서 가져와 캐시에 저장하는 경우입니다. 이런 경우는 `Cache::remember` 메서드를 사용하면 쉽게 처리할 수 있습니다:

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
지정한 항목이 캐시에 없으면, `remember` 메서드에 전달한 클로저가 실행되어 그 반환값이 캐시에 저장됩니다.

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
항목을 영구적으로 저장하거나 없으면 가져오는 작업은 `rememberForever` 메서드로 할 수 있습니다:

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve & Delete -->
#### Retrieve & Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
캐시에서 항목을 가져오고 즉시 삭제하고 싶을 때는 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 캐시에 항목이 없으면 `null`을 반환합니다:

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items In The Cache -->
### Storing Items In The Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
`Cache` 파사드의 `put` 메서드를 사용하면 캐시에 원하는 값을 저장할 수 있습니다:

```
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
`put` 메서드에 저장 시간을 전달하지 않으면, 해당 항목은 무기한 저장됩니다:

```
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
정수형 초(for 만료시간) 대신 캐시 만료 시점을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
<!-- #### Store If Not Present -->
#### Store If Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` 메서드는 해당 항목이 캐시에 없을 때만 추가합니다. 실제로 캐시에 값이 추가되면 `true`를 반환하며, 이미 존재하는 경우엔 `false`를 반환합니다. `add` 메서드는 원자적으로 동작합니다:

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` 메서드를 사용하면 항목을 만료 기간 없이 영구적으로 저장할 수 있습니다. 이 항목들은 만료되지 않으므로, `forget` 메서드를 사용해 수동으로 삭제해야 합니다:

```
Cache::forever('key', 'value');
```

> [!TIP]
> Memcached 드라이버를 사용할 때, "forever"로 저장된 항목도 캐시의 크기 제한에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From The Cache -->
### Removing Items From The Cache

<!-- You may remove items from the cache using the `forget` method: -->
`forget` 메서드를 사용해 캐시 항목을 제거할 수 있습니다:

```
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
만료 시간을 0이나 음수로 지정하면 항목을 삭제할 수도 있습니다:

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
캐시 전체를 비우고 싶은 경우엔 `flush` 메서드를 사용합니다:

```
Cache::flush();
```

> [!NOTE]
> 캐시를 비우면 설정한 캐시 "prefix"와 상관없이 모든 캐시 항목이 삭제됩니다. 여러 애플리케이션이 캐시를 공유하는 환경이라면 이 점을 신중하게 고려해야 합니다.

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` 파사드 외에도, 전역 `cache` 함수를 사용하여 캐시에 데이터를 저장하거나 조회할 수 있습니다. `cache` 함수에 하나의 문자열 인수만 전달하면, 해당 키의 값을 반환합니다:

```
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
함수에 키-값 쌍의 배열과 만료시간을 함께 전달하면, 지정한 기간 동안 캐시에 저장됩니다:

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
아무 인수도 주지 않고 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 구현체의 인스턴스를 반환하므로, 다양한 캐시 관련 메서드를 사용할 수 있습니다:

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!TIP]
> 전역 `cache` 함수 호출을 테스트할 때는, [testing the facade](/docs/8.x/mocking#mocking-facades)에서와 같이 `Cache::shouldReceive` 메서드를 활용할 수 있습니다.

<a name="cache-tags"></a>
<!-- ## Cache Tags -->
## Cache Tags

> [!NOTE]
> `file`, `dynamodb`, `database` 캐시 드라이버에서는 캐시 태그를 사용할 수 없습니다. 또, 여러 태그를 사용하면서 "forever"로 저장된 캐시에서도, 오래된 레코드를 자동으로 제거해 주는 `memcached`와 같은 드라이버를 사용할 때 가장 좋은 성능을 기대할 수 있습니다.

<a name="storing-tagged-cache-items"></a>
<!-- ### Storing Tagged Cache Items -->
### Storing Tagged Cache Items

<!-- Cache tags allow you to tag related items in the cache and then flush all cached values that have been assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` a value into the cache: -->
캐시 태그를 활용하면 관련된 여러 캐시 항목에 동일한 태그를 부여하고, 특정 태그가 부여된 캐시 값만 한 번에 비울 수 있습니다. 태그가 적용된 캐시에 접근하려면 원하는 태그명을 배열로 전달하면 됩니다. 예를 들어, 아래처럼 태그가 적용된 캐시에 접근하여 `put`으로 값을 저장할 수 있습니다:

```
Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
<!-- ### Accessing Tagged Cache Items -->
### Accessing Tagged Cache Items

<!-- To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method and then call the `get` method with the key you wish to retrieve: -->
태그가 적용된 캐시 항목을 조회하려면, 동일한 순서의 태그 목록을 `tags` 메서드에 전달한 뒤, 조회할 키로 `get` 메서드를 호출하면 됩니다:

```
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
<!-- ### Removing Tagged Cache Items -->
### Removing Tagged Cache Items

<!-- You may flush all items that are assigned a tag or list of tags. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache: -->
특정 태그가 지정된 모든 캐시 항목을 한 번에 제거할 수 있습니다. 예를 들어, 아래 코드는 `people`, `authors` 또는 두 태그 모두가 지정된 모든 캐시를 비웁니다. 즉, `Anne`과 `John`이 모두 제거됩니다:

```
Cache::tags(['people', 'authors'])->flush();
```

<!-- In contrast, this statement would remove only cached values tagged with `authors`, so `Anne` would be removed, but not `John`: -->
반면, 아래 코드는 `authors` 태그가 붙은 값만 제거하므로 `Anne`만 삭제되고, `John`은 그대로 남아 있게 됩니다:

```
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!NOTE]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 설정해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="atomic-locks-prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to setup a table to contain your application's cache locks. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버를 사용할 경우, 애플리케이션의 캐시 락 정보를 저장할 테이블을 미리 생성해야 합니다. 아래는 예시 `Schema` 선언입니다:

```
Schema::create('cache_locks', function ($table) {
    $table->string('key')->primary();
    $table->string('owner');
    $table->integer('expiration');
});
```

<a name="managing-locks"></a>
<!-- ### Managing Locks -->
### Managing Locks

<!-- Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Forge](https://forge.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method: -->
원자적 락은 레이스 컨디션 걱정 없이 분산 락을 다룰 수 있도록 해줍니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 한 번에 하나의 원격 작업만 서버에서 실행하도록 원자적 락을 사용합니다. 락은 `Cache::lock` 메서드를 활용해 생성 및 관리할 수 있습니다:

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
`get` 메서드에는 클로저도 전달할 수 있습니다. 클로저 실행 후 Laravel이 자동으로 락을 해제합니다:

```
Cache::lock('foo')->get(function () {
    // Lock acquired indefinitely and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock can not be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
락이 요청 시점에 사용 불가능하면, Laravel에 일정 시간만큼 대기하라고 지시할 수 있습니다. 락을 해당 시간 내에 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다:

```
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    optional($lock)->release();
}
```

<!-- The example above may be simplified by passing a closure to the `block` method. When a closure is passed to this method, Laravel will attempt to acquire the lock for the specified number of seconds and will automatically release the lock once the closure has been executed: -->
위 예시를 더 간소화하려면 `block` 메서드에 클로저를 전달하면 됩니다. 이 메서드로 Laravel이 지정된 시간 동안 락 획득을 시도하고, 클로저 실행 후 자동으로 락을 해제합니다:

```
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
때로는 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제해야 할 수 있습니다. 예를 들어, 웹 요청 중 락을 잡고, 해당 요청에서 발생하는 큐 작업이 끝날 때 락을 해제하는 경우입니다. 이때는 락의 범위가 지정된 "owner token"을 큐 작업에 전달해서, 작업 내에서 동일한 락을 다시 인스턴스화해 해제할 수 있습니다.

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
아래 예시에서는 락을 성공적으로 획득했을 때 큐 작업을 디스패치합니다. 또한 락의 `owner` 메서드를 통해 락의 소유자 토큰을 작업에 전달합니다:

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
`ProcessPodcast` 작업 내에서는 owner 토큰을 활용해 락을 복원하고 해제할 수 있습니다:

```
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
현재 owner를 무시하고 강제로 락을 해제하고 싶다면 `forceRelease` 메서드를 사용할 수 있습니다:

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
<!-- ## Adding Custom Cache Drivers -->
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
<!-- ### Writing The Driver -->
### Writing The Driver

<!-- To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/8.x/contracts). So, a MongoDB cache implementation might look something like this: -->
커스텀 캐시 드라이버를 만들려면, 우선 `Illuminate\Contracts\Cache\Store` [contract](/docs/8.x/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 드라이버는 아래와 같이 구현할 수 있습니다:

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
각 메서드는 MongoDB 연결을 이용해 구현해야 합니다. 구체적인 구현 방법은 [Laravel framework source code](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고해 볼 수 있습니다. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드를 호출해 커스텀 드라이버 등록을 마무리합니다:

```
Cache::extend('mongo', function ($app) {
    return Cache::repository(new MongoStore);
});
```

> [!TIP]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들어 둘 수 있습니다. 물론 Laravel의 애플리케이션 구조에는 정해진 틀이 없으므로, 자유롭게 구조를 조직해도 무방합니다.

<a name="registering-the-driver"></a>
<!-- ### Registering The Driver -->
### Registering The Driver

<!-- To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class: -->
커스텀 캐시 드라이버를 Laravel에 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용해야 합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드에서 캐시 값을 읽을 수 있으므로, 커스텀 드라이버 등록은 `booting` 콜백 안에서 진행하는 것이 좋습니다. `booting` 콜백을 사용하면 애플리케이션의 서비스 프로바이더의 `boot` 메서드가 호출되기 직전에, 그리고 모든 서비스 프로바이더의 `register` 메서드가 호출된 직후에 드라이버가 등록됩니다. 아래처럼 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `booting` 콜백을 사용해 등록할 수 있습니다:

```
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class CacheServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function ($app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        //
    }
}
```

<!-- The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/8.x/container). -->
`extend` 메서드의 첫 번째 인자는 드라이버 이름이며, 이는 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저인데, 이 클로저에는 [service container](/docs/8.x/container) 인스턴스인 `$app`이 전달됩니다.

<!-- Once your extension is registered, update your `config/cache.php` configuration file's `driver` option to the name of your extension. -->
드라이버 확장이 등록되면, `config/cache.php` 설정 파일의 `driver` 항목에 해당 확장 이름을 지정해주면 됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for the [events](/docs/8.x/events) fired by the cache. Typically, you should place these event listeners within your application's `App\Providers\EventServiceProvider` class: -->
각 캐시 동작 시마다 코드를 실행하려면, 캐시에서 발생하는 [events](/docs/8.x/events)를 구독하면 됩니다. 보통 이 이벤트 리스너들은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 등록합니다:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Cache\Events\CacheHit' => [
        'App\Listeners\LogCacheHit',
    ],

    'Illuminate\Cache\Events\CacheMissed' => [
        'App\Listeners\LogCacheMissed',
    ],

    'Illuminate\Cache\Events\KeyForgotten' => [
        'App\Listeners\LogKeyForgotten',
    ],

    'Illuminate\Cache\Events\KeyWritten' => [
        'App\Listeners\LogKeyWritten',
    ],
];
```
