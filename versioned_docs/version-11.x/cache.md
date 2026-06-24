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
애플리케이션에서 실행하는 데이터 조회나 처리 작업 중 일부는 CPU를 많이 사용하거나 여러 초가 소요될 수 있습니다. 이런 경우, 한 번 조회한 데이터를 일정 시간 동안 캐시에 넣어두고, 같은 데이터에 대한 후속 요청이 들어오면 신속하게 캐시에서 데이터를 반환하는 것이 일반적입니다. 이렇게 캐싱된 데이터는 보통 매우 빠른 데이터 저장소인 [Memcached](https://memcached.org)나 [Redis](https://redis.io) 등에 보관됩니다.

<!-- Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application. -->
Laravel은 다양한 캐시 백엔드를 하나의 통일된, 간단명료한 API로 사용할 수 있도록 지원하므로, 빠른 데이터 접근 속도를 활용하여 웹 애플리케이션의 성능을 쉽게 높일 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache store you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), and relational databases out of the box. In addition, a file based cache driver is available, while `array` and "null" cache drivers provide convenient cache backends for your automated tests. -->
애플리케이션의 캐시 설정 파일은 `config/cache.php`에 있습니다. 이 파일에서 애플리케이션 전체에서 기본으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스 등의 유명한 캐시 백엔드를 기본적으로 지원합니다. 이외에도 파일 기반 캐시 드라이버가 있으며, `array`와 "null" 캐시 드라이버는 자동화된 테스트에 편리하게 사용할 수 있는 옵션입니다.

<!-- The cache configuration file also contains a variety of other options that you may review. By default, Laravel is configured to use the `database` cache driver, which stores the serialized, cached objects in your application's database. -->
캐시 설정 파일에는 이 외에도 다양한 설정 옵션이 포함되어 있으니 필요에 따라 참고하실 수 있습니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있는데, 이는 직렬화된(serialize) 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="prerequisites-database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` cache driver, you will need a database table to contain the cache data. Typically, this is included in Laravel's default `0001_01_01_000001_create_cache_table.php` [database migration](/docs/11.x/migrations); however, if your application does not contain this migration, you may use the `make:cache-table` Artisan command to create it: -->
`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 이 테이블은 Laravel 기본 제공 마이그레이션 파일인 `0001_01_01_000001_create_cache_table.php` [database migration](/docs/11.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없을 경우, `make:cache-table` Artisan 명령어로 마이그레이션 파일을 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
<!-- #### Memcached -->
#### Memcached

<!-- Using the Memcached driver requires the [Memcached PECL package](https://pecl.php.net/package/memcached) to be installed. You may list all of your Memcached servers in the `config/cache.php` configuration file. This file already contains a `memcached.servers` entry to get you started: -->
Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)를 설치해야 합니다. 여러 Memcached 서버를 `config/cache.php` 설정 파일에 나열할 수 있습니다. 기본적으로 이 파일에는 시작을 돕기 위한 `memcached.servers` 항목이 포함되어 있습니다:

```
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
필요하다면 `host` 옵션에 유닉스 소켓 경로를 지정할 수도 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

```
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

<!-- Before using a Redis cache with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~2.0) via Composer. [Laravel Sail](/docs/11.x/sail) already includes this extension. In addition, official Laravel deployment platforms such as [Laravel Forge](https://forge.laravel.com) and [Laravel Vapor](https://vapor.laravel.com) have the PhpRedis extension installed by default. -->
Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/11.x/sail) 환경에는 이 확장 프로그램이 이미 포함되어 있습니다. 또한, [Laravel Forge](https://forge.laravel.com)나 [Laravel Vapor](https://vapor.laravel.com)와 같은 공식 Laravel 배포 플랫폼에는 기본적으로 PhpRedis가 설치되어 있습니다.

<!-- For more information on configuring Redis, consult its [Laravel documentation page](/docs/11.x/redis#configuration). -->
Redis 설정 방법에 대한 자세한 내용은 [Laravel documentation page](/docs/11.x/redis#configuration)를 참조하세요.

<a name="dynamodb"></a>
<!-- #### DynamoDB -->
#### DynamoDB

<!-- Before using the [DynamoDB](https://aws.amazon.com/dynamodb) cache driver, you must create a DynamoDB table to store all of the cached data. Typically, this table should be named `cache`. However, you should name the table based on the value of the `stores.dynamodb.table` configuration value within the `cache` configuration file. The table name may also be set via the `DYNAMODB_CACHE_TABLE` environment variable. -->
[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블 이름은 `cache`로 지정합니다. 하지만, 설정 파일(`cache` 설정 파일)의 `stores.dynamodb.table` 값에 따라 테이블 이름을 정해야 합니다. 테이블 이름은 환경 변수 `DYNAMODB_CACHE_TABLE`을 통해서도 지정할 수 있습니다.

<!-- This table should also have a string partition key with a name that corresponds to the value of the `stores.dynamodb.attributes.key` configuration item within your application's `cache` configuration file. By default, the partition key should be named `key`. -->
이 테이블에는 파티션 키로 사용할 문자열 타입의 키가 필요하며, 이 키의 이름은 `cache` 설정 파일의 `stores.dynamodb.attributes.key`에 지정된 값과 일치해야 합니다. 기본적으로 파티션 키 이름은 `key`입니다.

<!-- Typically, DynamoDB will not proactively remove expired items from a table. Therefore, you should [enable Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) on the table. When configuring the table's TTL settings, you should set the TTL attribute name to `expires_at`. -->
대부분의 경우 DynamoDB는 만료된 아이템을 테이블에서 능동적으로 제거하지 않으므로, [enable Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) 기능을 테이블에 활성화하는 것이 좋습니다. 테이블의 TTL 속성 이름은 `expires_at`으로 지정해야 합니다.

<!-- Next, install the AWS SDK so that your Laravel application can communicate with DynamoDB: -->
다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다:

```shell
composer require aws/aws-sdk-php
```

<!-- In addition, you should ensure that values are provided for the DynamoDB cache store configuration options. Typically these options, such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, should be defined in your application's `.env` configuration file: -->
또한, DynamoDB 캐시 저장소의 설정 옵션(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 등)도 반드시 값이 지정되어 있어야 합니다. 보통 이 값들은 애플리케이션의 `.env` 설정 파일에 정의합니다:

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
MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지가 `mongodb` 캐시 드라이버를 제공합니다. 이 패키지는 `mongodb` 데이터베이스 연결을 사용해 캐시 드라이버를 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로, 만료된 캐시 아이템을 자동으로 삭제할 수 있습니다.

<!-- For more information on configuring MongoDB, please refer to the MongoDB [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/). -->
MongoDB 관련 추가 설정 방법은 [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하세요.

<a name="cache-usage"></a>
<!-- ## Cache Usage -->
## Cache Usage

<a name="obtaining-a-cache-instance"></a>
<!-- ### Obtaining a Cache Instance -->
### Obtaining a Cache Instance

<!-- To obtain a cache store instance, you may use the `Cache` facade, which is what we will use throughout this documentation. The `Cache` facade provides convenient, terse access to the underlying implementations of the Laravel cache contracts: -->
캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(Facade)를 사용할 수 있습니다. 본 문서 전체에서 이 파사드를 사용할 예정입니다. `Cache` 파사드는 Laravel 캐시 컨트랙트의 실제 구현체에 간결하게 접근할 수 있도록 해줍니다.

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
`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다.

```
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
<!-- ### Retrieving Items From the Cache -->
### Retrieving Items From the Cache

<!-- The `Cache` facade's `get` method is used to retrieve items from the cache. If the item does not exist in the cache, `null` will be returned. If you wish, you may pass a second argument to the `get` method specifying the default value you wish to be returned if the item doesn't exist: -->
`Cache` 파사드의 `get` 메서드는 캐시에서 아이템을 가져오는 데 사용합니다. 캐시에 해당 아이템이 없으면 `null`이 반환됩니다. 원한다면 `get` 메서드에 두 번째 인수로 아이템이 없을 때 반환할 기본값을 지정할 수도 있습니다.

```
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

<!-- You may even pass a closure as the default value. The result of the closure will be returned if the specified item does not exist in the cache. Passing a closure allows you to defer the retrieval of default values from a database or other external service: -->
기본값으로 클로저(Closure)를 전달할 수도 있습니다. 캐시에 해당 아이템이 없으면 해당 클로저가 실행되어 반환값이 사용됩니다. 이를 통해 기본값을 데이터베이스나 외부 서비스에서 가져오도록 지연 처리할 수 있습니다.

```
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
<!-- #### Determining Item Existence -->
#### Determining Item Existence

<!-- The `has` method may be used to determine if an item exists in the cache. This method will also return `false` if the item exists but its value is `null`: -->
`has` 메서드를 사용하면 캐시에 아이템이 존재하는지 확인할 수 있습니다. 이 메서드는 아이템이 존재하지만 값이 `null`일 때도 `false`를 반환합니다.

```
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
<!-- #### Incrementing / Decrementing Values -->
#### Incrementing / Decrementing Values

<!-- The `increment` and `decrement` methods may be used to adjust the value of integer items in the cache. Both of these methods accept an optional second argument indicating the amount by which to increment or decrement the item's value: -->
`increment`와 `decrement` 메서드를 사용하면 캐시에 저장된 정수 값을 증가시키거나 감소시킬 수 있습니다. 두 메서드 모두 두 번째 인수로 증가/감소시킬 값을 지정할 수 있습니다.

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
필요에 따라 캐시에서 아이템을 가져오되, 없으면 기본값을 저장하고 싶은 경우가 있습니다. 예를 들어, 모든 사용자를 캐시에서 가져오거나 없다면 데이터베이스에서 로드한 뒤 캐시에 저장할 수 있습니다. 이는 `Cache::remember` 메서드로 처리할 수 있습니다.

```
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

<!-- If the item does not exist in the cache, the closure passed to the `remember` method will be executed and its result will be placed in the cache. -->
캐시에 아이템이 없다면, `remember` 메서드에 전달한 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

<!-- You may use the `rememberForever` method to retrieve an item from the cache or store it forever if it does not exist: -->
영구적으로(만료 없이) 저장하거나, 없으면 저장하고 싶다면 `rememberForever` 메서드를 사용할 수 있습니다.

```
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
<!-- #### Stale While Revalidate -->
#### Stale While Revalidate

<!-- When using the `Cache::remember` method, some users may experience slow response times if the cached value has expired. For certain types of data, it can be useful to allow partially stale data to be served while the cached value is recalculated in the background, preventing some users from experiencing slow response times while cached values are calculated. This is often referred to as the "stale-while-revalidate" pattern, and the `Cache::flexible` method provides an implementation of this pattern. -->
`Cache::remember` 메서드를 사용할 때, 캐시가 만료된 경우 일부 사용자는 느린 응답을 경험할 수 있습니다. 특정 데이터의 경우, 캐시된 값이 만료된 상태(stale)라도 캐시를 백그라운드에서 재계산하는 동안 임시로 반환하게 하는 것이 유용할 수 있습니다. 이를 통해 사용자가 느린 응답을 받지 않도록 할 수 있습니다. 이러한 방식을 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드가 이 패턴을 구현합니다.

<!-- The flexible method accepts an array that specifies how long the cached value is considered “fresh” and when it becomes “stale.” The first value in the array represents the number of seconds the cache is considered fresh, while the second value defines how long it can be served as stale data before recalculation is necessary. -->
flexible 메서드는 캐시된 값이 "신선(fresh)"하다고 간주되는 시간과 "stale"로 간주되어 다시 계산이 필요한 시점을 배열로 지정합니다. 배열의 첫 번째 값은 신선 기간(초 단위), 두 번째 값은 stale 상태로 허용되는 총 시간(초 단위)입니다.

<!-- If a request is made within the fresh period (before the first value), the cache is returned immediately without recalculation. If a request is made during the stale period (between the two values), the stale value is served to the user, and a [deferred function](/docs/11.x/helpers#deferred-functions) is registered to refresh the cached value after the response is sent to the user. If a request is made after the second value, the cache is considered expired, and the value is recalculated immediately, which may result in a slower response for the user: -->
첫 번째 값 이내의 요청에는 즉시 캐시가 반환됩니다. 두 값 사이(stale 기간)에는 이전 캐시 값을 사용자에게 반환하면서, 응답 후에 [deferred function](/docs/11.x/helpers#deferred-functions)를 이용해 캐시 값을 갱신합니다. 두 번째 값(총 유효기간) 이후에는 캐시가 만료된 것으로 간주되어, 즉시 다시 계산하여 반환합니다(이 경우 사용자는 느린 응답을 받을 수 있습니다).

```
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
<!-- #### Retrieve and Delete -->
#### Retrieve and Delete

<!-- If you need to retrieve an item from the cache and then delete the item, you may use the `pull` method. Like the `get` method, `null` will be returned if the item does not exist in the cache: -->
캐시에서 아이템을 가져온 후, 바로 해당 아이템을 삭제하고 싶을 때는 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 해당 아이템이 없으면 `null`이 반환됩니다.

```
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
<!-- ### Storing Items in the Cache -->
### Storing Items in the Cache

<!-- You may use the `put` method on the `Cache` facade to store items in the cache: -->
`Cache` 파사드의 `put` 메서드를 사용하여 캐시에 아이템을 저장할 수 있습니다.

```
Cache::put('key', 'value', $seconds = 10);
```

<!-- If the storage time is not passed to the `put` method, the item will be stored indefinitely: -->
`put` 메서드에 저장 시간을 전달하지 않으면 해당 아이템은 만료 없이 영구적으로 저장됩니다.

```
Cache::put('key', 'value');
```

<!-- Instead of passing the number of seconds as an integer, you may also pass a `DateTime` instance representing the desired expiration time of the cached item: -->
초 단위 정수 대신 원하는 만료 시점을 `DateTime` 인스턴스로도 전달할 수 있습니다.

```
Cache::put('key', 'value', now()->addMinutes(10));
```

<a name="store-if-not-present"></a>
<!-- #### Store if Not Present -->
#### Store if Not Present

<!-- The `add` method will only add the item to the cache if it does not already exist in the cache store. The method will return `true` if the item is actually added to the cache. Otherwise, the method will return `false`. The `add` method is an atomic operation: -->
`add` 메서드는 해당 키가 캐시에 이미 없을 때만 아이템을 추가합니다. 실제로 아이템이 저장될 경우 `true`를, 이미 존재할 경우 `false`를 반환합니다. `add` 메서드는 원자적(atomic)으로 동작합니다.

```
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
<!-- #### Storing Items Forever -->
#### Storing Items Forever

<!-- The `forever` method may be used to store an item in the cache permanently. Since these items will not expire, they must be manually removed from the cache using the `forget` method: -->
`forever` 메서드는 아이템을 만료 없이 영구적으로 캐시에 저장합니다. 이런 아이템은 직접 `forget` 메서드를 사용해서 삭제해야 합니다.

```
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용 중인 경우, "forever"로 저장한 아이템이더라도 캐시 크기 한도에 도달하면 삭제될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
<!-- ### Removing Items From the Cache -->
### Removing Items From the Cache

<!-- You may remove items from the cache using the `forget` method: -->
`forget` 메서드로 캐시에서 아이템을 삭제할 수 있습니다.

```
Cache::forget('key');
```

<!-- You may also remove items by providing a zero or negative number of expiration seconds: -->
만료 시간을 0 또는 음수로 지정해도 아이템을 삭제할 수 있습니다.

```
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

<!-- You may clear the entire cache using the `flush` method: -->
캐시 전체를 비우려면 `flush` 메서드를 사용할 수 있습니다.

```
Cache::flush();
```

> [!WARNING]
> 캐시를 flush하면 설정한 캐시 "prefix"와는 상관없이 모든 캐시 엔트리가 삭제되므로, 여러 애플리케이션이 캐시를 공유하는 경우 주의해서 사용해야 합니다.

<a name="the-cache-helper"></a>
<!-- ### The Cache Helper -->
### The Cache Helper

<!-- In addition to using the `Cache` facade, you may also use the global `cache` function to retrieve and store data via the cache. When the `cache` function is called with a single, string argument, it will return the value of the given key: -->
`Cache` 파사드 외에도, 전역 `cache` 함수를 사용하여 캐시 데이터에 접근하거나 저장할 수 있습니다. `cache` 함수에 문자열 인수 한 개를 전달해 호출하면 해당 키의 값을 반환합니다.

```
$value = cache('key');
```

<!-- If you provide an array of key / value pairs and an expiration time to the function, it will store values in the cache for the specified duration: -->
키/값 쌍의 배열과 만료 시간을 함수에 전달하면, 해당 값들을 지정한 시간 동안 캐시에 저장합니다.

```
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->addMinutes(10));
```

<!-- When the `cache` function is called without any arguments, it returns an instance of the `Illuminate\Contracts\Cache\Factory` implementation, allowing you to call other caching methods: -->
`cache` 함수를 인수 없이 호출하면 `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하며, 이를 통해 다른 캐시 메서드도 호출할 수 있습니다.

```
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는 [testing the facade](/docs/11.x/mocking#mocking-facades)와 동일하게 `Cache::shouldReceive`를 사용할 수 있습니다.

<a name="atomic-locks"></a>
<!-- ## Atomic Locks -->
## Atomic Locks

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버에 연결되어 있어야 합니다.

<a name="managing-locks"></a>
<!-- ### Managing Locks -->
### Managing Locks

<!-- Atomic locks allow for the manipulation of distributed locks without worrying about race conditions. For example, [Laravel Forge](https://forge.laravel.com) uses atomic locks to ensure that only one remote task is being executed on a server at a time. You may create and manage locks using the `Cache::lock` method: -->
원자적(atomic) 락을 이용하면 레이스 컨디션(race condition) 걱정 없이 분산 환경에서 락을 조작할 수 있습니다. 예를 들어, [Laravel Forge](https://forge.laravel.com)에서는 원자적 락을 사용해 한 서버에서 한 번에 한 개의 원격 작업만 실행되도록 보장합니다. 락은 `Cache::lock` 메서드로 생성하고 관리합니다.

```
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

<!-- The `get` method also accepts a closure. After the closure is executed, Laravel will automatically release the lock: -->
`get` 메서드는 클로저도 받을 수 있습니다. 클로저 실행이 끝나면 락은 자동으로 해제됩니다.

```
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

<!-- If the lock is not available at the moment you request it, you may instruct Laravel to wait for a specified number of seconds. If the lock cannot be acquired within the specified time limit, an `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown: -->
락을 요청하는 시점에 이미 락이 잡혀 있다면, Laravel이 지정한 시간(초 단위)만큼 락이 풀릴 때까지 대기하도록 할 수 있습니다. 제한 시간 내 락을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

```
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
위 예시에서처럼, `block` 메서드에 클로저를 전달해 코드를 더욱 간결하게 작성할 수도 있습니다. 이 경우 Laravel이 지정한 시간(초) 동안 락을 기다렸다가 획득하면 클로저 실행 후 자동으로 락을 해제합니다.

```
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
<!-- ### Managing Locks Across Processes -->
### Managing Locks Across Processes

<!-- Sometimes, you may wish to acquire a lock in one process and release it in another process. For example, you may acquire a lock during a web request and wish to release the lock at the end of a queued job that is triggered by that request. In this scenario, you should pass the lock's scoped "owner token" to the queued job so that the job can re-instantiate the lock using the given token. -->
때로는 한 프로세스에서 락을 획득한 뒤, 다른 프로세스에서 해당 락을 해제하고 싶을 수 있습니다. 예컨대, 웹 요청 중에 락을 획득하고, 이 요청에서 생성된 대기 중인(queued) 작업의 마지막에서 락을 해제하는 경우 등입니다. 이런 때는 락에 할당된 "owner token(소유자 토큰)"을 큐 작업으로 전달하여, 받은 토큰으로 락을 재생성해야 합니다.

<!-- In the example below, we will dispatch a queued job if a lock is successfully acquired. In addition, we will pass the lock's owner token to the queued job via the lock's `owner` method: -->
아래는 락을 성공적으로 획득하면 큐 작업을 디스패치하고, 락의 `owner` 메서드를 통해 락의 소유자 토큰을 큐 작업에 함께 전달하는 예시입니다.

```
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

<!-- Within our application's `ProcessPodcast` job, we can restore and release the lock using the owner token: -->
큐 작업인 `ProcessPodcast` 내부에서는, 소유자 토큰을 이용해 락을 복원하고 해제할 수 있습니다.

```
Cache::restoreLock('processing', $this->owner)->release();
```

<!-- If you would like to release a lock without respecting its current owner, you may use the `forceRelease` method: -->
현재 소유자를 고려하지 않고 강제로 락을 해제하고 싶다면 `forceRelease` 메서드를 사용할 수 있습니다.

```
Cache::lock('processing')->forceRelease();
```

<a name="adding-custom-cache-drivers"></a>
<!-- ## Adding Custom Cache Drivers -->
## Adding Custom Cache Drivers

<a name="writing-the-driver"></a>
<!-- ### Writing the Driver -->
### Writing the Driver

<!-- To create our custom cache driver, we first need to implement the `Illuminate\Contracts\Cache\Store` [contract](/docs/11.x/contracts). So, a MongoDB cache implementation might look something like this: -->
커스텀 캐시 드라이버를 만들려면, 먼저 `Illuminate\Contracts\Cache\Store` [contract](/docs/11.x/contracts)를 구현해야 합니다. 예를 들어, MongoDB 캐시를 구현한다면 다음과 같이 작성할 수 있습니다.

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
이제 각 메서드를 MongoDB 연결로 구현하면 됩니다. 실제 구현 예시는 [Laravel framework source code](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고할 수 있습니다. 구현이 끝나면, `Cache` 파사드의 `extend` 메서드로 커스텀 드라이버 등록을 마무리합니다.

```
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 안에 `Extensions` 네임스페이스를 만들어 관리할 수 있습니다. 하지만 Laravel은 엄격한 구조를 강제하지 않으므로, 원하는 대로 폴더 구조를 설계하셔도 됩니다.

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- To register the custom cache driver with Laravel, we will use the `extend` method on the `Cache` facade. Since other service providers may attempt to read cached values within their `boot` method, we will register our custom driver within a `booting` callback. By using the `booting` callback, we can ensure that the custom driver is registered just before the `boot` method is called on our application's service providers but after the `register` method is called on all of the service providers. We will register our `booting` callback within the `register` method of our application's `App\Providers\AppServiceProvider` class: -->
Laravel에서 커스텀 캐시 드라이버를 등록하려면, `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드 안에서 캐시 값을 읽으려 할 수 있으므로, 커스텀 드라이버는 `booting` 콜백 안에서 등록합니다. `booting` 콜백을 사용하면, 애플리케이션의 서비스 프로바이더에서 `boot` 메서드가 호출되기 직전이면서 모든 서비스 프로바이더에서 `register` 메서드가 호출된 이후에 커스텀 드라이버가 등록되도록 보장할 수 있습니다. 이를 위해 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에서 `booting` 콜백을 등록합니다.

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

<!-- The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/11.x/container). -->
`extend` 메서드의 첫 번째 인수로 드라이버의 이름을 지정합니다. 이 이름은 `config/cache.php`의 `driver` 옵션 값과 일치해야 합니다. 두 번째 인수로는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저를 지정하며, 이 클로저에는 [service container](/docs/11.x/container) 인스턴스인 `$app`이 전달됩니다.

<!-- Once your extension is registered, update the `CACHE_STORE` environment variable or `default` option within your application's `config/cache.php` configuration file to the name of your extension. -->
등록이 끝나면, 애플리케이션의 환경 변수 `CACHE_STORE` 또는 `config/cache.php` 파일의 `default` 옵션을 확장한 커스텀 드라이버 이름으로 변경하세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- To execute code on every cache operation, you may listen for various [events](/docs/11.x/events) dispatched by the cache: -->
모든 캐시 작업 시마다 특정 코드를 실행하고 싶다면, 캐시에서 발생하는 다양한 [events](/docs/11.x/events)를 리스닝할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트명 |
| --- |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWritten` |

<!-- </div> -->
</div>

<!-- To increase performance, you may disable cache events by setting the `events` configuration option to `false` for a given cache store in your application's `config/cache.php` configuration file: -->
성능 향상을 위해, 특정 캐시 저장소의 캐시 이벤트를 비활성화하려면 `config/cache.php` 설정 파일에서 해당 저장소의 `events` 옵션을 `false`로 지정하세요.

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
