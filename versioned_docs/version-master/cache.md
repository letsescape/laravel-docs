# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 요구 사항](#driver-prerequisites)
- [캐시 사용](#cache-usage)
    - [캐시 인스턴스 가져오기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [항목 수명 연장](#extending-item-lifetime)
    - [캐시에서 항목 제거](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 잠금 (Atomic Locks)](#atomic-locks)
    - [잠금 관리](#managing-locks)
    - [프로세스 간 잠금 관리](#managing-locks-across-processes)
    - [동시성 제한](#concurrency-limiting)
- [캐시 장애 조치](#cache-failover)
- [사용자 정의 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행되는 일부 데이터 조회 또는 처리 작업은 CPU 사용량이 높거나 완료까지 몇 초가 걸릴 수 있습니다. 이러한 경우 동일한 데이터에 대한 이후 요청에서 더 빠르게 가져올 수 있도록 일정 시간 동안 조회된 데이터를 캐시에 저장하는 것이 일반적입니다. 캐시된 데이터는 보통 매우 빠른 데이터 저장소인 [Memcached](https://memcached.org) 또는 [Redis](https://redis.io) 등에 저장됩니다.

다행히도 Laravel은 다양한 캐시 백엔드를 위한 표현력 있고 통합된 API를 제공합니다. 이를 통해 매우 빠른 데이터 조회 성능을 활용하여 웹 애플리케이션의 속도를 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 위치합니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 저장소(cache store)를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스 등 널리 사용되는 캐시 백엔드를 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 `null` 캐시 드라이버는 자동화 테스트에서 사용하기에 편리한 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 이 외에도 다양한 옵션이 포함되어 있으므로 필요에 따라 검토할 수 있습니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구 사항

<a name="prerequisites-database"></a>
#### Database

`database` 캐시 드라이버를 사용하는 경우 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel 기본 [database migration](/docs/master/migrations)인 `0001_01_01_000001_create_cache_table.php`에 포함되어 있습니다. 만약 애플리케이션에 해당 migration이 없다면 `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. `config/cache.php` 설정 파일에서 모든 Memcached 서버를 나열할 수 있습니다. 이 파일에는 이미 시작을 위한 `memcached.servers` 항목이 포함되어 있습니다:

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다:

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
#### Redis

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/master/sail)은 이미 이 확장을 포함하고 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel Redis 문서](/docs/master/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에 모든 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`로 지정합니다. 그러나 실제 테이블 이름은 `cache` 설정 파일의 `stores.dynamodb.table` 설정 값에 따라 지정해야 합니다. 또한 `DYNAMODB_CACHE_TABLE` 환경 변수를 통해서도 테이블 이름을 설정할 수 있습니다.

이 테이블에는 문자열 파티션 키가 필요하며, 해당 키의 이름은 애플리케이션 `cache` 설정 파일의 `stores.dynamodb.attributes.key` 설정 값과 일치해야 합니다. 기본적으로 이 파티션 키의 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 자동으로 즉시 삭제하지 않습니다. 따라서 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. TTL 설정 시 TTL 속성 이름을 `expires_at`으로 지정해야 합니다.

다음으로 Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소 설정 옵션에 값이 제공되어야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`와 같은 옵션은 애플리케이션의 `.env` 설정 파일에 정의됩니다:

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
#### MongoDB

MongoDB를 사용하는 경우 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 통해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로 만료된 캐시 항목을 자동으로 제거할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB의 [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참고하십시오.

<a name="cache-usage"></a>
## 캐시 사용 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 가져오기

캐시 저장소 인스턴스를 가져오기 위해 `Cache` facade를 사용할 수 있으며, 이 문서 전반에서도 이를 사용합니다. `Cache` facade는 Laravel 캐시 계약(cache contracts)의 기본 구현체에 간결하고 편리하게 접근할 수 있도록 제공합니다:

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
#### 여러 캐시 저장소 접근

`Cache` facade의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` facade의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 캐시에 해당 항목이 존재하지 않으면 `null`이 반환됩니다. 항목이 존재하지 않을 경우 반환할 기본값을 두 번째 인수로 전달할 수도 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정된 항목이 캐시에 없을 경우 해당 클로저의 실행 결과가 반환됩니다. 이렇게 하면 데이터베이스나 외부 서비스에서 기본값을 가져오는 작업을 지연 실행할 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 사용하면 캐시에 특정 항목이 존재하는지 확인할 수 있습니다. 단, 항목이 존재하더라도 값이 `null`이면 `false`가 반환됩니다:

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메서드를 사용하면 캐시에 저장된 정수 값을 증가 또는 감소시킬 수 있습니다. 두 메서드는 증가 또는 감소시킬 값을 나타내는 두 번째 인수를 선택적으로 받을 수 있습니다:

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
#### 조회 후 저장

캐시에서 항목을 가져오되, 존재하지 않으면 기본값을 저장하고 싶을 때가 있습니다. 예를 들어 모든 사용자를 캐시에서 가져오고, 캐시에 없으면 데이터베이스에서 가져와 캐시에 저장할 수 있습니다. 이때 `Cache::remember` 메서드를 사용할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 존재하지 않으면 `remember` 메서드에 전달된 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

항목이 존재하지 않을 경우 영구적으로 저장하려면 `rememberForever` 메서드를 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember`를 사용할 때 캐시가 만료된 경우 일부 사용자는 느린 응답을 경험할 수 있습니다. 특정 데이터 유형에서는 캐시 값을 백그라운드에서 재계산하는 동안 부분적으로 오래된(stale) 데이터를 제공하는 것이 유용할 수 있습니다. 이렇게 하면 캐시 값을 다시 계산하는 동안 일부 사용자가 느린 응답을 경험하는 문제를 줄일 수 있습니다. 이를 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드가 이를 구현합니다.

`flexible` 메서드는 캐시가 "fresh"로 간주되는 기간과 "stale"로 간주되는 기간을 정의하는 배열을 인수로 받습니다. 배열의 첫 번째 값은 캐시가 신선한 상태로 간주되는 초 단위 시간이며, 두 번째 값은 재계산이 필요하기 전까지 오래된 데이터로 제공될 수 있는 기간을 의미합니다.

첫 번째 값 이전(신선한 기간)에는 캐시가 즉시 반환되며 재계산이 발생하지 않습니다. 두 값 사이(오래된 기간)에는 오래된 값이 사용자에게 반환되며, 사용자에게 응답을 보낸 후 캐시 값을 갱신하는 [deferred function](/docs/master/helpers#deferred-functions)이 등록됩니다. 두 번째 값 이후에는 캐시가 만료된 것으로 간주되어 즉시 재계산이 수행되며, 이 경우 사용자 응답이 느려질 수 있습니다:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 항목을 가져온 뒤 삭제해야 하는 경우 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로 캐시에 항목이 없으면 `null`이 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` facade의 `put` 메서드를 사용하여 캐시에 항목을 저장할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간을 전달하지 않으면 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```

정수 초 단위 대신 캐시 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시 저장소에 해당 항목이 아직 존재하지 않을 때만 항목을 추가합니다. 항목이 실제로 캐시에 추가되면 `true`를 반환하고, 이미 존재하면 `false`를 반환합니다. `add` 메서드는 원자적(atomic) 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### 항목 수명 연장

`touch` 메서드를 사용하면 기존 캐시 항목의 수명(TTL)을 연장할 수 있습니다. 캐시 항목이 존재하고 만료 시간이 성공적으로 연장되면 `true`를 반환합니다. 캐시에 항목이 존재하지 않으면 `false`를 반환합니다:

```php
Cache::touch('key', 3600);
```

정확한 만료 시간을 지정하려면 `DateTimeInterface`, `DateInterval`, 또는 `Carbon` 인스턴스를 전달할 수 있습니다:

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드를 사용하면 캐시에 항목을 영구적으로 저장할 수 있습니다. 이러한 항목은 만료되지 않으므로 `forget` 메서드를 사용하여 수동으로 제거해야 합니다:

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우 "영구 저장"된 항목도 캐시 용량 한도에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거

`forget` 메서드를 사용하여 캐시 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 지정하여 항목을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 전체 캐시를 비울 수 있습니다:

```php
Cache::flush();
```

`flushLocks` 메서드를 사용하면 캐시에 저장된 모든 원자적 잠금을 제거할 수 있습니다:

```php
Cache::flushLocks();
```

> [!WARNING]
> 캐시를 비우는 작업은 설정된 캐시 `prefix`를 고려하지 않으며 캐시에 있는 모든 항목을 삭제합니다. 다른 애플리케이션과 캐시를 공유하는 경우 특히 주의해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션 (Cache Memoization)

Laravel의 `memo` 캐시 드라이버를 사용하면 단일 요청 또는 작업(job) 실행 동안 이미 해결된 캐시 값을 메모리에 임시 저장할 수 있습니다. 이를 통해 동일한 실행 내에서 반복적인 캐시 조회를 방지하여 성능을 크게 향상시킬 수 있습니다.

메모이제이션 캐시를 사용하려면 `memo` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 선택적으로 캐시 저장소 이름을 받을 수 있으며, 이는 메모이제이션 드라이버가 감싸는 기본 캐시 저장소를 지정합니다:

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

특정 키에 대해 첫 번째 `get` 호출은 실제 캐시 저장소에서 값을 가져오지만, 같은 요청 또는 작업 내의 이후 호출은 메모리에 저장된 값을 반환합니다:

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

캐시 값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면 메모이제이션 캐시는 자동으로 기존 메모이제이션 값을 삭제하고 실제 캐시 저장소에 작업을 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` facade 외에도 전역 `cache` 함수를 사용하여 캐시에서 데이터를 조회하거나 저장할 수 있습니다. `cache` 함수에 하나의 문자열 인수를 전달하면 해당 키의 값을 반환합니다:

```php
$value = cache('key');
```

키/값 쌍 배열과 만료 시간을 전달하면 지정된 기간 동안 캐시에 값을 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수 없이 `cache` 함수를 호출하면 `Illuminate\Contracts\Cache\Factory` 구현 인스턴스를 반환하므로 다른 캐시 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는 [facade 테스트](/docs/master/mocking#mocking-facades)와 동일하게 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다.

### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 서로 관련된 캐시 항목에 태그를 지정하고 특정 태그가 지정된 모든 캐시 값을 한 번에 삭제할 수 있습니다. 태그 이름 배열을 전달하여 태그 캐시에 접근할 수 있습니다. 예를 들어 다음과 같이 태그 캐시에 값을 저장할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

### 태그가 지정된 캐시 항목 접근

태그를 사용하여 저장된 항목은 동일한 태그를 제공하지 않으면 접근할 수 없습니다. 캐시 항목을 가져오려면 동일한 순서의 태그 배열을 `tags` 메서드에 전달한 후 `get` 메서드를 호출합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

### 태그가 지정된 캐시 항목 제거

특정 태그 또는 태그 목록이 지정된 모든 캐시 항목을 삭제할 수 있습니다. 예를 들어 다음 코드는 `people`, `authors`, 또는 두 태그가 모두 지정된 모든 캐시를 제거합니다. 따라서 `Anne`과 `John` 모두 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반대로 아래 코드는 `authors` 태그가 지정된 캐시만 제거하므로 `Anne`은 삭제되지만 `John`은 삭제되지 않습니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 잠금 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

### 잠금 관리

원자적 잠금은 레이스 컨디션(race condition)을 걱정하지 않고 분산 잠금을 제어할 수 있도록 합니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com)는 원자적 잠금을 사용하여 한 번에 하나의 원격 작업만 서버에서 실행되도록 보장합니다. `Cache::lock` 메서드를 사용하여 잠금을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

`get` 메서드는 클로저를 받을 수도 있으며, 클로저 실행이 끝나면 Laravel이 자동으로 잠금을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

잠금을 요청했을 때 사용할 수 없는 경우 지정된 시간 동안 기다리도록 할 수 있습니다. 지정된 시간 내에 잠금을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

클로저를 `block` 메서드에 전달하면 코드를 더 간단하게 작성할 수 있습니다. Laravel은 지정된 시간 동안 잠금을 시도하고 클로저 실행이 끝나면 자동으로 잠금을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

### 프로세스 간 잠금 관리

때로는 한 프로세스에서 잠금을 획득하고 다른 프로세스에서 해제해야 할 수도 있습니다. 예를 들어 웹 요청에서 잠금을 획득하고 해당 요청으로 트리거된 큐 작업이 끝날 때 잠금을 해제하고 싶을 수 있습니다. 이런 경우 잠금의 범위가 지정된 "owner token"을 큐 작업에 전달해야 합니다.

다음 예제에서는 잠금을 성공적으로 획득하면 큐 작업을 디스패치하고, `owner` 메서드를 통해 owner token을 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

`ProcessPodcast` 작업 내부에서는 owner token을 사용하여 잠금을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 owner를 무시하고 잠금을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

### 동시성 제한

Laravel의 원자적 잠금 기능은 클로저 실행의 동시성을 제한하는 여러 방법도 제공합니다. 전체 인프라에서 한 번에 하나의 실행만 허용하려면 `withoutOverlapping`을 사용합니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

기본적으로 잠금은 클로저 실행이 끝날 때까지 유지되며, 잠금을 획득하기 위해 최대 10초 동안 기다립니다. 추가 인수를 사용하여 값을 변경할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

지정된 대기 시간 내에 잠금을 획득하지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

제어된 병렬 실행을 허용하려면 `funnel` 메서드를 사용하여 동시에 실행할 수 있는 최대 개수를 설정할 수 있습니다. `funnel` 메서드는 잠금을 지원하는 모든 캐시 드라이버에서 작동합니다:

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

`funnel` 키는 제한하려는 리소스를 식별합니다. `limit` 메서드는 최대 동시 실행 수를 정의합니다. `releaseAfter` 메서드는 획득된 슬롯이 자동으로 해제되기 전까지의 안전 시간(초)을 설정합니다. `block` 메서드는 사용 가능한 슬롯을 기다릴 최대 시간을 설정합니다.

실패 클로저 대신 예외로 처리하고 싶다면 두 번째 클로저를 생략할 수 있습니다. 지정된 시간 내에 잠금을 획득하지 못하면 `Illuminate\Cache\Limiters\LimiterTimeoutException`이 발생합니다:

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

동시성 제한에 특정 캐시 저장소를 사용하려면 원하는 저장소에서 `funnel` 메서드를 호출할 수 있습니다:

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> `funnel` 메서드는 캐시 저장소가 `Illuminate\Contracts\Cache\LockProvider` 인터페이스를 구현해야 합니다. 잠금을 지원하지 않는 캐시 저장소에서 `funnel`을 사용하면 `BadMethodCallException`이 발생합니다.

<a name="cache-failover"></a>
## 캐시 장애 조치 (Cache Failover)

`failover` 캐시 드라이버는 캐시 작업 중 자동 장애 조치 기능을 제공합니다. `failover` 저장소의 기본 캐시 저장소가 어떤 이유로든 실패하면 Laravel은 자동으로 목록에 정의된 다음 저장소를 사용하려고 시도합니다. 이는 캐시 안정성이 중요한 프로덕션 환경에서 높은 가용성을 보장하는 데 매우 유용합니다.

장애 조치 캐시 저장소를 구성하려면 `failover` 드라이버를 지정하고 시도할 저장소 이름 배열을 순서대로 제공하면 됩니다. 기본적으로 Laravel은 `config/cache.php` 설정 파일에 예시 구성을 포함하고 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 구성한 후에는 `.env` 파일에서 해당 저장소를 기본 캐시 저장소로 설정해야 장애 조치 기능이 동작합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 작업이 실패하여 장애 조치가 발생하면 Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치합니다. 이를 통해 캐시 저장소 실패를 로깅하거나 보고할 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가 (Adding Custom Cache Drivers)

### 드라이버 작성

사용자 정의 캐시 드라이버를 만들기 위해 먼저 `Illuminate\Contracts\Cache\Store` [contract](/docs/master/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 같이 작성할 수 있습니다:

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

각 메서드는 MongoDB 연결을 사용하여 구현하면 됩니다. 각 메서드를 구현하는 방법의 예시는 [Laravel framework source code](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore` 클래스를 참고하십시오. 구현이 완료되면 `Cache` facade의 `extend` 메서드를 호출하여 사용자 정의 드라이버 등록을 마무리할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 사용자 정의 캐시 드라이버 코드를 어디에 둘지 고민된다면 `app` 디렉토리 내에 `Extensions` 네임스페이스를 생성할 수 있습니다. 다만 Laravel은 엄격한 애플리케이션 구조를 강제하지 않으므로 원하는 방식으로 구조를 구성할 수 있습니다.

### 드라이버 등록

Laravel에 사용자 정의 캐시 드라이버를 등록하려면 `Cache` facade의 `extend` 메서드를 사용합니다. 다른 ServiceProvider가 `boot` 메서드에서 캐시 값을 읽을 수 있으므로 사용자 정의 드라이버는 `booting` 콜백에서 등록하는 것이 좋습니다. `booting` 콜백을 사용하면 모든 ServiceProvider의 `register` 메서드가 실행된 이후이면서 `boot` 메서드가 호출되기 직전에 드라이버가 등록되도록 보장할 수 있습니다. 이 콜백은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에서 등록합니다:

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

`extend` 메서드의 첫 번째 인수는 드라이버 이름이며, 이는 `config/cache.php` 설정 파일의 `driver` 옵션과 일치해야 합니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환하는 클로저입니다. 이 클로저는 [service container](/docs/master/container)의 인스턴스인 `$app`을 전달받습니다.

확장이 등록된 후 `.env` 파일의 `CACHE_STORE` 환경 변수 또는 `config/cache.php` 파일의 `default` 옵션을 확장 드라이버 이름으로 변경하면 됩니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업에서 코드를 실행하려면 캐시가 디스패치하는 다양한 [events](/docs/master/events)를 리스닝할 수 있습니다:

<div class="overflow-auto">

| Event Name                                      |
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

성능 향상을 위해 `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```