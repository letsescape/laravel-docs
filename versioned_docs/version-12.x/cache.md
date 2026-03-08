# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 가져오기](#obtaining-a-cache-instance)
    - [캐시에서 항목 가져오기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [Cache 태그](#cache-tags)
- [Atomic Locks](#atomic-locks)
    - [락 관리](#managing-locks)
    - [프로세스 간 락 관리](#managing-locks-across-processes)
    - [동시성 제한](#concurrency-limiting)
- [Cache Failover](#cache-failover)
- [커스텀 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션이 수행하는 일부 데이터 조회 또는 처리 작업은 CPU 사용량이 많거나 완료까지 몇 초가 걸릴 수 있습니다. 이런 경우 동일한 데이터에 대한 이후 요청에서 더 빠르게 응답할 수 있도록, 일정 시간 동안 조회된 데이터를 캐시에 저장하는 것이 일반적입니다. 캐시된 데이터는 보통 매우 빠른 데이터 저장소인 [Memcached](https://memcached.org) 또는 [Redis](https://redis.io)에 저장됩니다.

Laravel은 다양한 캐시 백엔드를 위한 표현력 있고 통합된 API를 제공합니다. 이를 통해 매우 빠른 데이터 조회 성능을 활용하여 웹 애플리케이션의 속도를 향상시킬 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 있습니다. 이 파일에서 애플리케이션 전반에서 기본적으로 사용할 캐시 저장소(store)를 지정할 수 있습니다. Laravel은 기본적으로 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 그리고 관계형 데이터베이스를 캐시 백엔드로 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 `null` 캐시 드라이버는 자동화 테스트에서 유용한 캐시 백엔드로 사용할 수 있습니다.

캐시 설정 파일에는 검토할 수 있는 다양한 옵션도 포함되어 있습니다. 기본적으로 Laravel은 `database` 캐시 드라이버를 사용하도록 설정되어 있으며, 직렬화된 캐시 객체를 애플리케이션의 데이터베이스에 저장합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="prerequisites-database"></a>
#### Database

`database` 캐시 드라이버를 사용할 경우 캐시 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [database migration](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 이 migration이 없다면 `make:cache-table` Artisan 명령어를 사용하여 생성할 수 있습니다.

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. `config/cache.php` 설정 파일에서 모든 Memcached 서버를 나열할 수 있습니다. 이 파일에는 시작을 위한 `memcached.servers` 항목이 이미 포함되어 있습니다.

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

필요한 경우 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다.

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

Laravel에서 Redis 캐시를 사용하려면 PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이 확장이 이미 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 플랫폼에는 PhpRedis 확장이 기본적으로 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel Redis 문서](/docs/12.x/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에 캐시 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 테이블 이름은 `cache`로 지정합니다. 그러나 `cache` 설정 파일의 `stores.dynamodb.table` 설정 값에 맞게 테이블 이름을 지정해야 합니다. 또한 `DYNAMODB_CACHE_TABLE` 환경 변수로도 테이블 이름을 설정할 수 있습니다.

이 테이블에는 문자열 타입의 파티션 키가 필요하며, 이름은 애플리케이션 `cache` 설정 파일의 `stores.dynamodb.attributes.key` 값과 일치해야 합니다. 기본적으로 파티션 키 이름은 `key`입니다.

일반적으로 DynamoDB는 만료된 항목을 자동으로 삭제하지 않습니다. 따라서 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. TTL 설정 시 TTL 속성 이름은 `expires_at`으로 설정해야 합니다.

다음으로 Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소 설정 옵션에 값이 제공되었는지 확인해야 합니다. 보통 `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY`와 같은 옵션은 애플리케이션의 `.env` 파일에 정의합니다.

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

MongoDB를 사용하는 경우 공식 `mongodb/laravel-mongodb` 패키지가 `mongodb` 캐시 드라이버를 제공합니다. 이 드라이버는 `mongodb` 데이터베이스 연결을 사용하여 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하므로 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB의 [Cache and Locks documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)을 참고하십시오.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 가져오기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드(facade)를 사용할 수 있습니다. 이 문서에서는 계속해서 `Cache` 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 계약(contract)의 실제 구현체에 간결하고 편리하게 접근할 수 있는 방법을 제공합니다.

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

`Cache` 파사드의 `store` 메서드를 사용하면 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달되는 키는 `cache` 설정 파일의 `stores` 배열에 정의된 저장소 이름과 일치해야 합니다.

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 가져올 때 사용합니다. 캐시에 해당 항목이 없으면 `null`이 반환됩니다. 필요하다면 두 번째 인수로 기본값을 지정할 수 있습니다.

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 캐시에 값이 없을 경우 클로저가 실행되고 그 결과가 반환됩니다. 이 방식은 데이터베이스나 외부 서비스에서 기본값을 지연 조회할 때 유용합니다.

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인

`has` 메서드를 사용하면 캐시에 항목이 존재하는지 확인할 수 있습니다. 단, 항목이 존재하더라도 값이 `null`이면 `false`가 반환됩니다.

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메서드는 캐시에 저장된 정수 값을 증가 또는 감소시키는 데 사용합니다. 두 메서드 모두 두 번째 인수로 증가 또는 감소할 값을 선택적으로 받을 수 있습니다.

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

캐시에서 값을 조회하면서, 값이 없을 경우 기본값을 저장하고 싶을 때가 있습니다. 예를 들어 모든 사용자 목록을 캐시에서 가져오거나, 캐시에 없으면 데이터베이스에서 조회한 후 캐시에 저장할 수 있습니다. 이때 `Cache::remember` 메서드를 사용할 수 있습니다.

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

캐시에 항목이 없으면 `remember`에 전달된 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

항목을 영구적으로 저장하려면 `rememberForever` 메서드를 사용할 수 있습니다.

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember`를 사용할 때 캐시가 만료되면 일부 사용자가 느린 응답을 경험할 수 있습니다. 특정 데이터의 경우 캐시를 다시 계산하는 동안에도 약간 오래된 데이터를 제공하면 성능을 개선할 수 있습니다. 이를 **stale-while-revalidate 패턴**이라고 합니다. `Cache::flexible` 메서드는 이 패턴을 구현합니다.

`flexible` 메서드는 캐시가 "fresh" 상태로 간주되는 시간과 "stale" 상태로 제공될 수 있는 시간을 배열로 받습니다. 첫 번째 값은 캐시가 fresh 상태로 유지되는 시간(초), 두 번째 값은 stale 상태로 제공될 수 있는 최대 시간입니다.

- fresh 기간 내 요청 → 캐시 값 즉시 반환
- stale 기간 내 요청 → 오래된 값을 반환하고 응답 이후 캐시를 재계산
- 두 번째 값 이후 요청 → 캐시 만료로 간주되어 즉시 재계산

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회 후 삭제

캐시에서 값을 가져온 뒤 삭제해야 한다면 `pull` 메서드를 사용할 수 있습니다. `get`과 마찬가지로 항목이 없으면 `null`이 반환됩니다.

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용하여 캐시에 값을 저장할 수 있습니다.

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간을 지정하지 않으면 항목은 무기한 저장됩니다.

```php
Cache::put('key', 'value');
```

정수 초 대신 `DateTime` 인스턴스를 전달하여 만료 시점을 지정할 수도 있습니다.

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장

`add` 메서드는 캐시에 해당 키가 존재하지 않을 때만 값을 저장합니다. 실제로 저장되면 `true`, 이미 존재하면 `false`를 반환합니다. 이 메서드는 **원자적(atomic) 연산**입니다.

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 영구 저장

`forever` 메서드를 사용하면 값을 영구적으로 저장할 수 있습니다. 이 값은 자동으로 만료되지 않으므로 `forget` 메서드로 수동 삭제해야 합니다.

```php
Cache::forever('key', 'value');
```

> [!NOTE]  
> Memcached 드라이버를 사용하는 경우 캐시가 용량 제한에 도달하면 "영구 저장"된 항목도 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하여 특정 캐시 항목을 제거할 수 있습니다.

```php
Cache::forget('key');
```

만료 시간을 0 또는 음수로 설정하여 제거할 수도 있습니다.

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용하면 전체 캐시를 비울 수 있습니다.

```php
Cache::flush();
```

> [!WARNING]  
> `flush`는 설정된 캐시 `prefix`를 고려하지 않고 캐시 저장소의 모든 항목을 제거합니다. 다른 애플리케이션과 캐시를 공유하는 경우 특히 주의해야 합니다.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버는 하나의 요청 또는 작업 실행 동안 해결된 캐시 값을 메모리에 임시 저장합니다. 이를 통해 같은 실행 중 반복되는 캐시 조회를 방지하여 성능을 크게 향상시킬 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 선택적으로 캐시 저장소 이름을 받을 수 있습니다.

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

같은 요청 내에서 첫 번째 `get` 호출은 실제 캐시 저장소에 접근하지만, 이후 호출은 메모리에서 값을 반환합니다.

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Memoized value...
$value = Cache::memo()->get('key');
```

캐시 값을 변경하는 메서드(`put`, `increment`, `remember` 등)를 호출하면 메모이즈된 값은 자동으로 제거되고 실제 캐시 저장소에 위임됩니다.

```php
Cache::memo()->put('name', 'Taylor');
Cache::memo()->get('name');
Cache::memo()->get('name');

Cache::memo()->put('name', 'Tim');
Cache::memo()->get('name');
```

<a name="the-cache-helper"></a>
### Cache 헬퍼

`Cache` 파사드 외에도 전역 `cache` 함수를 사용할 수 있습니다.

```php
$value = cache('key');
```

배열과 만료 시간을 전달하면 캐시에 값을 저장합니다.

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수 없이 호출하면 `Illuminate\Contracts\Cache\Factory` 인스턴스를 반환합니다.

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]  
> 전역 `cache` 함수 테스트 시에도 [facade 테스트](/docs/12.x/mocking#mocking-facades)와 동일하게 `Cache::shouldReceive`를 사용할 수 있습니다.

<a name="cache-tags"></a>
## Cache 태그 (Cache Tags)

> [!WARNING]  
> Cache 태그는 `file`, `dynamodb`, `database` 캐시 드라이버에서는 지원되지 않습니다.