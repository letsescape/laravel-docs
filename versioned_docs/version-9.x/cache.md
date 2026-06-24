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
애플리케이션에서 수행하는 데이터 조회나 처리 작업 중 일부는 CPU를 많이 사용하거나, 몇 초 이상 걸릴 수 있습니다. 이런 경우, 한 번 조회한 데이터를 일정 시간 동안 캐시에 저장해서, 같은 데이터에 대한 이후 요청에서는 빠르게 가져올 수 있도록 하는 것이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 보관됩니다.

<!-- Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application. -->
Laravel은 다양한 캐시 백엔드를 위한 쉽고 통합된 API를 제공하여, 이런 고성능 데이터 저장소의 빠른 조회 속도를 쉽게 활용하고 웹 애플리케이션을 더욱 빠르게 만들 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache driver you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests. -->
애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서, 애플리케이션 전반에서 기본으로 사용할 캐시 드라이버를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등과 같은 널리 쓰이는 캐싱 백엔드를 기본적으로 지원합니다. 또한 파일 기반 캐시 드라이버도 사용할 수 있으며, `array`와 "null" 캐시 드라이버는 자동화된 테스트 환경에서 유용하게 쓸 수 있는 편리한 백엔드입니다.

<!-- The cache configuration file also contains various other options, which are documented within the file, so make sure to read over these options. By default, Laravel is configured to use the `file` cache driver, which stores the serialized, cached objects on the server's filesystem. For larger applications, it is recommended that you use a more robust driver such as Memcached or Redis. You may even configure multiple cache configurations for the same driver. -->
캐시 설정 파일에는 이 외에도 다양한 옵션들이 포함되어 있으니, 파일 내용을 꼭 확인해 보시기 바랍니다. 기본적으로 Laravel은 `file` 캐시 드라이버를 사용하도록 설정되어 있으며, 이는 직렬화된 캐시 객체를 서버 파일 시스템에 저장합니다. 대규모 애플리케이션에서는 Memcached나 Redis와 같은 더욱 강력한 드라이버 사용을 권장합니다. 또한 동일한 드라이버에 대해 여러 개의 캐시 구성을 분리해서 사용할 수도 있습니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to set up a table to contain the cache items. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버를 사용할 때는, 캐시 항목을 저장할 테이블을 직접 만들어야 합니다. 아래는 테이블을 위한 예시 `Schema` 선언 예시입니다.

```
Schema::create('cache', function ($table) {
    $table->string('key')->unique();
    $table->text('value');
    $table->integer('expiration');
});
```

> [!NOTE]
> 올바른 스키마로 마이그레이션 파일을 생성하려면 `php artisan cache:table` Artisan 명령어를 사용할 수도 있습니다.

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached 드라이버를 이용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)를 설치해야 합니다. 모든 Memcached 서버 정보를 `config/cache.php` 설정 파일에 나열할 수 있습니다. 기본적으로 이 파일에는 시작용 `memcached.servers` 항목이 포함되어 있습니다.

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
필요에 따라, `host` 옵션에 UNIX 소켓 경로를 지정할 수도 있습니다. 이 경우에는, `port` 옵션을 `0`으로 설정해야 합니다.

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

<!-- Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. [Laravel Sail](/docs/9.x/sail) already includes this extension. In addition, official Laravel deployment platforms such as [Laravel Forge](https://forge.laravel.com) and [Laravel Vapor](https://vapor.laravel.com) have the PhpRedis extension installed by default. -->
Laravel에서 Redis 캐시를 사용하려면, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 이용해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. [Laravel Sail](/docs/9.x/sail)은 이미 이 확장 모듈을 포함하고 있습니다. 또한, [Laravel Forge](https://forge.laravel.com) 및 [Laravel Vapor](https://vapor.laravel.com)와 같은 공식 Laravel 배포 플랫폼도 PhpRedis 확장을 기본적으로 설치하고 있습니다.

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/9.x/redis#configuration). -->
Redis 구성에 대한 더 자세한 내용은 [Laravel documentation page](/docs/9.x/redis#configuration)를 참고하세요.

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within your application's `cache` configuration file. -->
[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에는, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 먼저 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`로 지정하지만, 애플리케이션의 `cache` 설정 파일 내 `stores.dynamodb.table` 설정 값에 따라 이름을 지정하면 됩니다.

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
또한, 이 테이블에는 `cache` 설정 파일의 `stores.dynamodb.attributes.key` 설정값에 해당하는 이름의 문자열 파티션 키가 하나 있어야 합니다. 기본적으로 파티션 키는 `key`라는 이름이어야 합니다.

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining A Cache Instance -->
### Obtaining A Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
캐시 저장소 인스턴스를 얻으려면, 이 문서 전반에서 사용할 `Cache` 파사드를 활용하면 됩니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 실제 구현체에 간결하게 접근할 수 있도록 해줍니다.

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
`Cache` 파사드를 이용해, `store` 메서드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. 이때 `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다.

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From The Cache -->
### Retrieving Items From The Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회할 때 사용합니다. 캐시에 해당 항목이 없으면 `null`이 반환됩니다. 원한다면 `get` 메서드에 두 번째 인자를 전달하여 항목이 없을 경우 반환할 기본값을 지정할 수도 있습니다.

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
기본값으로 클로저를 전달할 수도 있습니다. 만약 지정한 키가 캐시에 없다면, 이 클로저가 실행된 결과가 반환됩니다. 클로저를 사용하면, 기본값을 데이터베이스나 외부 서비스에서 가져올 필요가 있을 때, 해당 작업을 실제로 필요한 경우에만 수행할 수 있습니다.

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="checking-for-item-existence"></a>
<!-- #### Checking For Item Existence -->
#### Checking For Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` 메서드는 캐시에 항목이 존재하는지 확인할 때 사용할 수 있습니다. 이 메서드는 항목이 존재하지만 값이 `null`인 경우에도 `false`를 반환합니다.

```
if (Cache::has('key')) {
    //
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment`와 `decrement` 메서드를 사용하면, 캐시에 저장된 정수형 값에 대해 값을 증감시킬 수 있습니다. 두 메서드 모두 증가/감소할 값(정수)을 두 번째 인자로 전달할 수 있습니다.

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
캐시에서 항목을 조회하면서, 만약 없다면 기본값을 저장하고 싶을 때도 있습니다. 예를 들어 모든 사용자를 캐시에서 가져오거나, 없다면 데이터베이스에서 읽어서 캐시에 저장하는 경우입니다. 이럴 때는 `Cache::remember` 메서드를 사용할 수 있습니다.

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
캐시에 항목이 없으면, `remember` 메서드에 전달한 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
항목을 영구적으로 저장하거나 조회하려면 `rememberForever` 메서드를 사용할 수 있습니다.

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve & Delete -->
#### Retrieve & Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
캐시에서 항목을 조회한 후, 바로 삭제하고 싶다면 `pull` 메서드를 사용할 수 있습니다. `get`과 마찬가지로, 항목이 없으면 `null`이 반환됩니다.

```
$value = Cache::pull('key');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items In The Cache -->
### Storing Items In The Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
캐시에 항목을 저장하려면, `Cache` 파사드의 `put` 메서드를 사용할 수 있습니다.

```
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
`put` 메서드에 저장 시간을 전달하지 않으면, 해당 항목은 무기한 저장됩니다.

```
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
저장 시간을 정수 (초) 대신 `DateTime` 인스턴스로 전달하여, 만료 시점을 지정할 수도 있습니다.

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
<!-- #### Store If Not Present -->
#### Store If Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` 메서드는 캐시에 해당 키가 존재하지 않을 때만 항목을 저장합니다. 실제로 저장된다면 `true`를, 이미 존재해서 저장되지 않으면 `false`를 반환합니다. `add`는 원자적(atomic) 연산입니다.

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` 메서드를 이용하면 항목을 영구히 캐시에 저장할 수 있습니다. 이렇게 저장된 항목은 만료되지 않으므로, 필요하다면 `forget` 메서드로 직접 삭제해야 합니다.

```
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용할 경우, "영구" 저장된 항목도 캐시 용량이 가득 차면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From The Cache -->
### Removing Items From The Cache

<!-- You may remove items from the cache using the `forget` method: -->
`forget` 메서드를 이용해 캐시에서 특정 항목을 삭제할 수 있습니다.

```
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
만료 시간을 0 또는 음수로 지정하여 항목을 삭제하는 것도 가능합니다.

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
캐시에 저장된 모든 항목을 한 번에 지우려면 `flush` 메서드를 사용하세요.

```
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시(전체 삭제)하면 설정한 캐시 "prefix"와 관계없이 모든 항목이 삭제됩니다. 여러 애플리케이션에서 동일한 캐시 서버를 공유하는 경우, 플러시 사용 시 주의해야 합니다.

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` 파사드 외에도, 글로벌 `cache` 함수를 통해 데이터를 캐시로 저장하거나 조회할 수 있습니다. `cache` 함수에 문자열 하나만 전달하면, 해당 키의 값을 반환합니다.

```
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
키/값 쌍의 배열과 만료 시간을 함께 제공하면, 지정한 기간 동안 값을 캐시에 저장합니다.

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
인자를 전달하지 않고 `cache` 함수를 호출하면, `Illuminate\Contracts\Cache\Factory` 구현체 인스턴스를 반환하여 다양한 캐싱 메서드를 사용할 수 있습니다.

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 글로벌 `cache` 함수 호출을 테스트할 때는, [testing the facade](/docs/9.x/mocking#mocking-facades)와 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
<!-- ## Cache Tags -->
## Cache Tags

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다. 또한, 여러 개의 태그와 "영구" 저장을 동시에 사용할 때는, 오래된 데이터를 자동으로 정리할 수 있는 `memcached`와 같은 드라이버를 사용하는 것이 가장 좋습니다.

<a name="storing-tagged-cache-items"></a>
<!-- ### Storing Tagged Cache Items -->
### Storing Tagged Cache Items

<!-- Cache tags allow you to tag related items in the cache and then flush all cached values that have been assigned a given tag. You may access a tagged cache by passing in an ordered array of tag names. For example, let's access a tagged cache and `put` a value into the cache: -->
캐시 태그 기능을 이용하면, 관련 항목에 태그를 달고, 해당 태그가 붙은 모든 항목을 한 번에 삭제할 수 있습니다. 태그명 배열을 순서대로 전달하면 태그가 적용된 캐시에 접근할 수 있습니다. 예를 들어, 태그가 적용된 캐시에 접근하여 `put`으로 값을 저장하는 방법은 아래와 같습니다.

```
Cache::tags(['people', 'artists'])->put('John', $john, $seconds);

Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
<!-- ### Accessing Tagged Cache Items -->
### Accessing Tagged Cache Items

<!-- Items stored via tags may not be accessed without also providing the tags that were used to store the value. To retrieve a tagged cache item, pass the same ordered list of tags to the `tags` method and then call the `get` method with the key you wish to retrieve: -->
태그를 이용해 저장한 항목은, 저장할 때 사용한 태그를 함께 제공해야만 조회할 수 있습니다. 아래 예시처럼, 동일한 순서의 태그 배열을 `tags` 메서드에 전달한 후, 원하는 키로 `get`을 호출하세요.

```
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
<!-- ### Removing Tagged Cache Items -->
### Removing Tagged Cache Items

<!-- You may flush all items that are assigned a tag or list of tags. For example, this statement would remove all caches tagged with either `people`, `authors`, or both. So, both `Anne` and `John` would be removed from the cache: -->
특정 태그나 태그 목록이 지정된 모든 캐시 항목을 한 번에 삭제할 수 있습니다. 예를 들어, 아래 코드는 `people`, `authors` 중 하나라도 포함된 모든 캐시를 삭제합니다. 따라서, `Anne`과 `John` 모두 캐시에서 삭제됩니다.

```
Cache::tags(['people', 'authors'])->flush();
```

<!-- In contrast, this statement would remove only cached values tagged with `authors`, so `Anne` would be removed, but not `John`: -->
반면, 아래 코드는 `authors` 태그가 붙은 항목만 삭제합니다. 즉, `Anne`만 삭제되고 `John`은 남게 됩니다.

```
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 합니다. 추가로, 모든 서버가 중앙의 같은 캐시 서버와 통신해야 합니다.

<a name="lock-driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="atomic-locks-prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need to setup a table to contain your application's cache locks. You'll find an example `Schema` declaration for the table below: -->
`database` 캐시 드라이버로 원자적 락을 사용하려면, 애플리케이션의 락 정보를 저장할 테이블을 별도로 생성해야 합니다. 아래는 예시 `Schema` 선언입니다.

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
원자적 락을 사용하면, 경쟁 상태(race condition)를 걱정할 필요 없이 분산 락을 안전하게 제어할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 한 번에 하나의 원격 작업만 서버에서 실행되도록 원자적 락을 사용합니다. 락은 `Cache::lock` 메서드로 만들고 제어할 수 있습니다.

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
`get` 메서드에는 클로저도 전달할 수 있습니다. 클로저 실행이 끝나면 Laravel이 자동으로 락을 해제합니다.

```
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock can not be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
락을 요청할 때 즉시 얻을 수 없다면, Laravel에 특정 시간(초) 동안 기다려 달라고 요청할 수 있습니다. 이 시간 내에 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

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
위 예시는 `block` 메서드에 클로저를 넘겨 더 간단하게 구현할 수 있습니다. 클로저가 실행되면 락이 자동으로 해제됩니다.

```
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
경우에 따라 한 프로세스에서 락을 획득하고, 다른 프로세스에서 락을 해제하고 싶을 수도 있습니다. 예를 들어, 웹 요청 도중 락을 획득하고, 해당 요청에 의해 트리거된 큐 작업(잡)의 마지막에서 락을 해제하기를 원할 수 있습니다. 이럴 때는 락의 범위(owner) 토큰을 잡(job)으로 전달한 후, 해당 토큰을 이용해 락을 다시 생성해 해제하면 됩니다.

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
아래 예시에서는, 락을 성공적으로 획득하면 큐 작업을 디스패치합니다. 그리고 락의 `owner` 메서드를 통해 락의 소유자 토큰을 큐 작업으로 전달합니다.

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
애플리케이션의 `ProcessPodcast` 잡에서는 소유자 토큰으로 락을 복원해 해제할 수 있습니다.

```
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
현재 락의 소유자를 고려하지 않고 강제로 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다.

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
<!-- ## Adding Custom Cache Drivers -->
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
<!-- ### Writing The Driver -->
### Writing The Driver

<!-- To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/9.x/contracts). So, a MongoDB cache implementation might look something like this: -->
커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [contract](/docs/9.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB용 캐시 구현은 다음과 같을 수 있습니다.

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
이제 각 메서드를 MongoDB 연결로 구현하면 됩니다. 각 메서드의 실제 예제 구현 방법은 [Laravel framework source code](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하시면 됩니다. 구현이 완료되면, `Cache` 파사드의 `extend` 메서드를 이용해 커스텀 드라이버를 등록할 수 있습니다.

```
Cache::extend('mongo', function ($app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 두어야 할지 궁금하다면, `app` 디렉터리 내에 `Extensions` 네임스페이스를 만드는 것도 하나의 방법입니다. 다만, Laravel의 애플리케이션 구조는 엄격하지 않으므로, 원하는 방식으로 자유롭게 구성하셔도 무방합니다.

<a name="registering-the-driver"></a>
<!-- ### Registering The Driver -->
### Registering The Driver

<!-- To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class: -->
Laravel에 커스텀 캐시 드라이버를 등록할 때는, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더들이 자신의 `boot` 메서드에서 캐시 값 읽기 작업을 시도할 수 있으므로, 커스텀 드라이버는 `booting` 콜백 내에서 등록하는 것이 중요합니다. `booting` 콜백을 사용하면, 애플리케이션의 모든 서비스 프로바이더의 `register` 메서드가 호출된 이후, 그리고 `boot` 메서드가 호출되기 직전에 커스텀 드라이버가 등록되도록 할 수 있습니다. `booting` 콜백은 주로 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 등록합니다.

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

<!-- The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/9.x/container). -->
`extend` 메서드의 첫 번째 인자는 드라이버의 이름입니다. 이는 `config/cache.php` 설정 파일의 `driver` 옵션에 지정하는 이름과 일치해야 합니다. 두 번째 인자는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저이며, 이 클로저는 [service container](/docs/9.x/container) 인스턴스인 `$app`을 파라미터로 전달받습니다.

<!-- Once your extension is registered, update your `config/cache.php` configuration file's `driver` option to the name of your extension. -->
드라이버 확장 기능을 등록한 후에는, `config/cache.php` 파일의 `driver` 값을 해당 확장 드라이버 이름으로 변경해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for the [events](/docs/9.x/events) fired by the cache. Typically, you should place these event listeners within your application's `App\Providers\EventServiceProvider` class: -->
모든 캐시 동작마다 특정 코드를 실행하려면, 캐시에서 발생하는 [events](/docs/9.x/events)를 리스닝할 수 있습니다. 보통 이런 이벤트 리스너는 애플리케이션의 `App\Providers\EventServiceProvider` 클래스에 작성합니다.
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
