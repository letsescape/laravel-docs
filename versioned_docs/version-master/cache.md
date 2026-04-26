# 캐시 (Cache)

- [소개](#introduction)
- [설정](#configuration)
    - [드라이버 사전 요구 사항](#driver-prerequisites)
- [캐시 사용법](#cache-usage)
    - [캐시 인스턴스 얻기](#obtaining-a-cache-instance)
    - [캐시에서 항목 조회하기](#retrieving-items-from-the-cache)
    - [캐시에 항목 저장하기](#storing-items-in-the-cache)
    - [항목 수명 연장하기](#extending-item-lifetime)
    - [캐시에서 항목 제거하기](#removing-items-from-the-cache)
    - [캐시 메모이제이션](#cache-memoization)
    - [Cache 헬퍼](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자적 잠금](#atomic-locks)
    - [잠금 관리하기](#managing-locks)
    - [프로세스 간 잠금 관리하기](#managing-locks-across-processes)
    - [동시성 제한](#concurrency-limiting)
- [캐시 장애 조치](#cache-failover)
- [커스텀 캐시 드라이버 추가하기](#adding-custom-cache-drivers)
    - [드라이버 작성하기](#writing-the-driver)
    - [드라이버 등록하기](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행하는 일부 데이터 조회 또는 처리 작업은 CPU를 많이 사용하거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이런 경우에는 조회한 데이터를 일정 시간 동안 캐시에 저장해 두고, 이후 같은 데이터에 대한 요청이 들어오면 빠르게 가져오는 방식이 일반적입니다. 캐시된 데이터는 보통 [Memcached](https://memcached.org)나 [Redis](https://redis.io)처럼 매우 빠른 데이터 저장소에 저장됩니다.

다행히 Laravel은 다양한 캐시 백엔드를 위한 표현력 있고 통합된 API를 제공합니다. 이를 통해 매우 빠른 데이터 조회 기능을 활용하고 웹 애플리케이션의 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 캐시 설정 파일은 `config/cache.php`에 있습니다. 이 파일에서 애플리케이션 전체에서 기본으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel은 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), 관계형 데이터베이스처럼 널리 사용되는 캐시 백엔드를 기본으로 지원합니다. 또한 파일 기반 캐시 드라이버도 제공되며, `array`와 `null` 캐시 드라이버는 자동화 테스트에서 편리하게 사용할 수 있는 캐시 백엔드를 제공합니다.

캐시 설정 파일에는 검토할 수 있는 다양한 다른 옵션도 포함되어 있습니다. 기본적으로 Laravel은 직렬화된 캐시 객체를 애플리케이션 데이터베이스에 저장하는 `database` 캐시 드라이버를 사용하도록 설정되어 있습니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구 사항

<a name="prerequisites-database"></a>
#### 데이터베이스

`database` 캐시 드라이버를 사용할 때는 캐시 데이터를 담을 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 하지만 애플리케이션에 이 마이그레이션이 없다면, `make:cache-table` Artisan 명령어를 사용해 생성할 수 있습니다.

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL package](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버는 `config/cache.php` 설정 파일에 나열할 수 있습니다. 이 파일에는 시작할 수 있도록 `memcached.servers` 항목이 이미 포함되어 있습니다.

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

필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이 경우 `port` 옵션은 `0`으로 설정해야 합니다.

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

Laravel에서 Redis 캐시를 사용하기 전에, PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/master/sail)에는 이 확장이 이미 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com), [Laravel Forge](https://forge.laravel.com) 같은 공식 Laravel 애플리케이션 플랫폼에는 PhpRedis 확장이 기본으로 설치되어 있습니다.

Redis 설정에 대한 자세한 내용은 [Laravel 문서 페이지](/docs/master/redis#configuration)를 참고하십시오.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시 데이터를 저장할 DynamoDB 테이블을 만들어야 합니다. 일반적으로 이 테이블 이름은 `cache`로 지정합니다. 하지만 실제 테이블 이름은 `cache` 설정 파일 안의 `stores.dynamodb.table` 설정값을 기준으로 정해야 합니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수를 통해서도 설정할 수 있습니다.

이 테이블에는 애플리케이션의 `cache` 설정 파일 안에 있는 `stores.dynamodb.attributes.key` 설정 항목의 값과 일치하는 이름을 가진 문자열 파티션 키도 있어야 합니다. 기본적으로 파티션 키 이름은 `key`여야 합니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 능동적으로 제거하지 않습니다. 따라서 테이블에서 [Time to Live (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 테이블의 TTL 설정을 구성할 때는 TTL 속성 이름을 `expires_at`으로 설정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소 설정 옵션에 값이 제공되어 있는지 확인해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` 같은 옵션은 애플리케이션의 `.env` 설정 파일에 정의해야 합니다.

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

MongoDB를 사용하는 경우, 공식 `mongodb/laravel-mongodb` 패키지에서 제공하는 `mongodb` 캐시 드라이버를 사용할 수 있으며, `mongodb` 데이터베이스 연결을 사용해 설정할 수 있습니다. MongoDB는 TTL 인덱스를 지원하며, 이를 사용해 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 설정에 대한 자세한 내용은 MongoDB [Cache and Locks 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참고하십시오.

<a name="cache-usage"></a>
## 캐시 사용법 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 `Cache` 파사드를 사용할 수 있습니다. 이 문서 전체에서도 `Cache` 파사드를 사용합니다. `Cache` 파사드는 Laravel 캐시 계약의 기반 구현에 간결하고 편리하게 접근할 수 있게 해줍니다.

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
#### 여러 캐시 저장소에 접근하기

`Cache` 파사드를 사용하면 `store` 메서드를 통해 여러 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달하는 키는 `cache` 설정 파일의 `stores` 설정 배열에 나열된 저장소 중 하나와 일치해야 합니다.

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 조회하기

`Cache` 파사드의 `get` 메서드는 캐시에서 항목을 조회할 때 사용합니다. 항목이 캐시에 없으면 `null`이 반환됩니다. 원한다면 `get` 메서드의 두 번째 인수로 기본값을 전달하여 항목이 없을 때 반환할 값을 지정할 수 있습니다.

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

기본값으로 클로저를 전달할 수도 있습니다. 지정한 항목이 캐시에 없으면 클로저의 실행 결과가 반환됩니다. 클로저를 전달하면 데이터베이스나 다른 외부 서비스에서 기본값을 가져오는 작업을 실제로 필요할 때까지 미룰 수 있습니다.

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 항목 존재 여부 확인하기

`has` 메서드는 항목이 캐시에 존재하는지 확인할 때 사용할 수 있습니다. 이 메서드는 항목이 존재하더라도 그 값이 `null`이면 `false`를 반환합니다.

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소하기

`increment`와 `decrement` 메서드는 캐시에 저장된 정수 항목의 값을 조정할 때 사용할 수 있습니다. 두 메서드 모두 선택적으로 두 번째 인수를 받으며, 이 인수는 항목 값을 얼마나 증가시키거나 감소시킬지를 나타냅니다.

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
#### 조회하고 저장하기

때로는 캐시에서 항목을 조회하되, 요청한 항목이 없으면 기본값을 저장하고 싶을 수 있습니다. 예를 들어 모든 사용자를 캐시에서 가져오고, 캐시에 없으면 데이터베이스에서 조회한 뒤 캐시에 추가하고 싶을 수 있습니다. 이런 경우 `Cache::remember` 메서드를 사용할 수 있습니다.

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 없으면 `remember` 메서드에 전달된 클로저가 실행되고, 그 결과가 캐시에 저장됩니다.

`rememberForever` 메서드를 사용하면 항목을 캐시에서 조회하거나, 존재하지 않는 경우 영구적으로 저장할 수 있습니다.

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### Stale While Revalidate

`Cache::remember` 메서드를 사용할 때, 캐시된 값이 만료되면 일부 사용자는 느린 응답 시간을 경험할 수 있습니다. 특정 유형의 데이터에서는 캐시된 값을 백그라운드에서 다시 계산하는 동안 부분적으로 오래된 데이터를 제공하는 방식이 유용할 수 있습니다. 이렇게 하면 캐시 값이 계산되는 동안 일부 사용자가 느린 응답을 경험하지 않도록 할 수 있습니다. 이를 흔히 "stale-while-revalidate" 패턴이라고 하며, `Cache::flexible` 메서드는 이 패턴의 구현을 제공합니다.

`flexible` 메서드는 캐시된 값이 얼마나 오래 "fresh"로 간주되는지, 그리고 언제 "stale" 상태가 되는지를 지정하는 배열을 받습니다. 배열의 첫 번째 값은 캐시가 fresh로 간주되는 초 수를 나타내고, 두 번째 값은 다시 계산이 필요해지기 전까지 stale 데이터로 제공할 수 있는 시간을 정의합니다.

요청이 fresh 기간 안에 들어오면(첫 번째 값 이전), 캐시는 다시 계산하지 않고 즉시 반환됩니다. 요청이 stale 기간 중에 들어오면(두 값 사이), stale 값이 사용자에게 제공되고, 응답이 사용자에게 전송된 뒤 캐시된 값을 새로 고치기 위해 [지연 함수](/docs/master/helpers#deferred-functions)가 등록됩니다. 요청이 두 번째 값 이후에 들어오면 캐시는 만료된 것으로 간주되고 값이 즉시 다시 계산되며, 이로 인해 사용자의 응답이 느려질 수 있습니다.

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 조회하고 삭제하기

캐시에서 항목을 조회한 다음 그 항목을 삭제해야 한다면 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 항목이 캐시에 없으면 `null`이 반환됩니다.

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장하기

`Cache` 파사드의 `put` 메서드를 사용해 캐시에 항목을 저장할 수 있습니다.

```php
Cache::put('key', 'value', $seconds = 10);
```

저장 시간이 `put` 메서드에 전달되지 않으면 항목은 무기한 저장됩니다.

```php
Cache::put('key', 'value');
```

초 단위 정수를 전달하는 대신, 캐시 항목의 원하는 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다.

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않을 때만 저장하기

`add` 메서드는 항목이 캐시 저장소에 이미 존재하지 않는 경우에만 캐시에 추가합니다. 항목이 실제로 캐시에 추가되면 메서드는 `true`를 반환합니다. 그렇지 않으면 `false`를 반환합니다. `add` 메서드는 원자적 작업입니다.

```php
Cache::add('key', 'value', $seconds);
```

<a name="extending-item-lifetime"></a>
### 항목 수명 연장하기

`touch` 메서드를 사용하면 기존 캐시 항목의 수명(TTL)을 연장할 수 있습니다. 캐시 항목이 존재하고 만료 시간이 성공적으로 연장되면 `touch` 메서드는 `true`를 반환합니다. 항목이 캐시에 없으면 메서드는 `false`를 반환합니다.

```php
Cache::touch('key', 3600);
```

정확한 만료 시간을 지정하기 위해 `DateTimeInterface`, `DateInterval`, 또는 `Carbon` 인스턴스를 제공할 수 있습니다.

```php
Cache::touch('key', now()->addHours(2));
```

<a name="storing-items-forever"></a>
#### 항목 영구 저장하기

`forever` 메서드는 항목을 캐시에 영구적으로 저장할 때 사용할 수 있습니다. 이러한 항목은 만료되지 않으므로, `forget` 메서드를 사용해 캐시에서 수동으로 제거해야 합니다.

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우, "forever"로 저장된 항목도 캐시가 크기 제한에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용해 캐시에서 항목을 제거할 수 있습니다.

```php
Cache::forget('key');
```

만료 초 수로 0 또는 음수를 제공하여 항목을 제거할 수도 있습니다.

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메서드를 사용해 전체 캐시를 비울 수 있습니다.

```php
Cache::flush();
```

`flushLocks` 메서드를 사용해 캐시에 있는 모든 원자적 잠금을 비울 수 있습니다.

```php
Cache::flushLocks();
```

> [!WARNING]
> 캐시를 비우는 작업은 설정된 캐시 "prefix"를 고려하지 않으며, 캐시의 모든 항목을 제거합니다. 다른 애플리케이션과 공유하는 캐시를 비울 때는 이 점을 신중히 고려하십시오.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버를 사용하면 단일 요청 또는 작업 실행 중에 확인된 캐시 값을 메모리에 임시로 저장할 수 있습니다. 이렇게 하면 같은 실행 안에서 반복적으로 캐시에 접근하는 일을 막아 성능을 크게 향상시킬 수 있습니다.

메모이즈된 캐시를 사용하려면 `memo` 메서드를 호출합니다.

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메서드는 선택적으로 캐시 저장소의 이름을 받을 수 있습니다. 이 이름은 메모이즈된 드라이버가 감싸서 사용할 기반 캐시 저장소를 지정합니다.

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

특정 키에 대한 첫 번째 `get` 호출은 캐시 저장소에서 값을 가져오지만, 같은 요청 또는 작업 안에서 이후 호출은 메모리에서 값을 가져옵니다.

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

캐시 값을 수정하는 메서드(`put`, `increment`, `remember` 등)를 호출하면, 메모이즈된 캐시는 메모리에 저장된 값을 자동으로 잊고 변경 메서드 호출을 기반 캐시 저장소에 위임합니다.

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
### Cache 헬퍼
`Cache` 파사드를 사용하는 것 외에도, 전역 `cache` 함수를 사용하여 캐시를 통해 데이터를 조회하고 저장할 수 있습니다. `cache` 함수가 하나의 문자열 인수로 호출되면 지정된 키의 값을 반환합니다:

```php
$value = cache('key');
```

키 / 값 쌍의 배열과 만료 시간을 함수에 전달하면, 지정된 기간 동안 값을 캐시에 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

`cache` 함수가 아무 인수 없이 호출되면 `Illuminate\Contracts\Cache\Factory` 구현의 인스턴스를 반환하므로, 다른 캐싱 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수 호출을 테스트할 때는 [파사드를 테스트하는 것](/docs/master/mocking#mocking-facades)과 마찬가지로 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> `file`, `dynamodb`, `database` 캐시 드라이버를 사용할 때는 캐시 태그가 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 캐시에 있는 관련 항목에 태그를 붙이고, 특정 태그가 할당된 모든 캐시 값을 한 번에 비울 수 있습니다. 태그 이름의 순서 있는 배열을 전달하여 태그가 지정된 캐시에 접근할 수 있습니다. 예를 들어, 태그가 지정된 캐시에 접근하여 캐시에 값을 `put`해 보겠습니다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 접근

태그를 통해 저장된 항목은 값을 저장할 때 사용한 태그를 함께 제공하지 않으면 접근할 수 없습니다. 태그가 지정된 캐시 항목을 가져오려면 동일한 순서의 태그 목록을 `tags` 메서드에 전달한 뒤, 가져오려는 키와 함께 `get` 메서드를 호출합니다:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

하나의 태그 또는 태그 목록이 할당된 모든 항목을 비울 수 있습니다. 예를 들어, 다음 코드는 `people`, `authors`, 또는 두 태그가 모두 지정된 모든 캐시를 제거합니다. 따라서 `Anne`과 `John`이 모두 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```

반대로, 아래 코드는 `authors` 태그가 지정된 캐시 값만 제거하므로 `Anne`은 제거되지만 `John`은 제거되지 않습니다:

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자적 락 (Atomic Locks)

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 락 관리

원자적 락을 사용하면 경쟁 상태를 걱정하지 않고 분산 락을 다룰 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자적 락을 사용하여 한 서버에서 동시에 하나의 원격 작업만 실행되도록 보장합니다. `Cache::lock` 메서드를 사용하여 락을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

`get` 메서드는 클로저도 받을 수 있습니다. 클로저가 실행된 후 Laravel은 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

락을 요청한 시점에 사용할 수 없다면, Laravel이 지정된 초만큼 기다리도록 지시할 수 있습니다. 지정된 시간 제한 안에 락을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

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

위 예제는 `block` 메서드에 클로저를 전달하여 더 간단하게 작성할 수 있습니다. 이 메서드에 클로저를 전달하면 Laravel은 지정된 초 동안 락 획득을 시도하고, 클로저 실행이 끝나면 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때로는 한 프로세스에서 락을 획득하고 다른 프로세스에서 해제해야 할 수 있습니다. 예를 들어, 웹 요청 중에 락을 획득하고 해당 요청에 의해 트리거된 큐 작업이 끝날 때 락을 해제하고 싶을 수 있습니다. 이 경우 작업이 주어진 토큰을 사용하여 락을 다시 인스턴스화할 수 있도록, 락의 범위가 지정된 "owner token"을 큐 작업에 전달해야 합니다.

아래 예제에서는 락을 성공적으로 획득한 경우 큐 작업을 디스패치합니다. 또한 락의 `owner` 메서드를 통해 락의 owner token을 큐 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 안에서는 owner token을 사용하여 락을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 소유자를 고려하지 않고 락을 해제하려면 `forceRelease` 메서드를 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```

<a name="concurrency-limiting"></a>
### 동시성 제한

Laravel의 원자적 락 기능은 클로저의 동시 실행을 제한하는 몇 가지 방법도 제공합니다. 인프라 전체에서 실행 중인 인스턴스를 하나만 허용하려면 `withoutOverlapping`을 사용합니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

기본적으로 락은 클로저 실행이 끝날 때까지 유지되며, 이 메서드는 락을 획득하기 위해 최대 10초까지 기다립니다. 추가 인수를 사용하여 이 값을 조정할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

지정된 대기 시간 안에 락을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다.

제어된 병렬 처리가 필요하다면 `funnel` 메서드를 사용하여 최대 동시 실행 수를 설정합니다. `funnel` 메서드는 락을 지원하는 모든 캐시 드라이버에서 동작합니다:

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

`funnel` 키는 제한할 리소스를 식별합니다. `limit` 메서드는 최대 동시 실행 수를 정의합니다. `releaseAfter` 메서드는 획득한 슬롯이 자동으로 해제되기 전까지의 안전 타임아웃을 초 단위로 설정합니다. `block` 메서드는 사용 가능한 슬롯을 기다릴 초 수를 설정합니다.

실패 클로저를 제공하는 대신 예외로 타임아웃을 처리하고 싶다면 두 번째 클로저를 생략할 수 있습니다. 지정된 대기 시간 안에 락을 획득할 수 없으면 `Illuminate\Cache\Limiters\LimiterTimeoutException`이 발생합니다:

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

동시성 제한기에 특정 캐시 저장소를 사용하려면 원하는 저장소에서 `funnel` 메서드를 호출할 수 있습니다:

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> `funnel` 메서드는 캐시 저장소가 `Illuminate\Contracts\Cache\LockProvider` 인터페이스를 구현해야 합니다. 락을 지원하지 않는 캐시 저장소에서 `funnel`을 사용하려고 하면 `BadMethodCallException`이 발생합니다.

<a name="cache-failover"></a>
## 캐시 장애 조치 (Cache Failover)

`failover` 캐시 드라이버는 캐시와 상호작용할 때 자동 장애 조치 기능을 제공합니다. `failover` 저장소의 기본 캐시 저장소가 어떤 이유로든 실패하면 Laravel은 목록에 설정된 다음 저장소를 자동으로 사용하려고 시도합니다. 이는 캐시 신뢰성이 중요한 프로덕션 환경에서 고가용성을 보장하는 데 특히 유용합니다.

장애 조치 캐시 저장소를 설정하려면 `failover` 드라이버를 지정하고, 순서대로 시도할 저장소 이름 배열을 제공합니다. 기본적으로 Laravel은 애플리케이션의 `config/cache.php` 설정 파일에 예제 장애 조치 설정을 포함합니다:

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 설정한 후에는 장애 조치 기능을 사용하기 위해 애플리케이션의 `.env` 파일에서 장애 조치 저장소를 기본 캐시 저장소로 설정해야 합니다:

```ini
CACHE_STORE=failover
```

캐시 저장소 작업이 실패하고 장애 조치가 활성화되면 Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 디스패치하므로, 캐시 저장소 실패를 보고하거나 로그로 남길 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 커스텀 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

커스텀 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/master/contracts)을 구현해야 합니다. 예를 들어 MongoDB 캐시 구현은 다음과 비슷할 수 있습니다:

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

이제 MongoDB 연결을 사용하여 각 메서드를 구현하기만 하면 됩니다. 각 메서드를 구현하는 방법의 예시는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 참고하십시오. 구현이 완료되면 `Cache` 파사드의 `extend` 메서드를 호출하여 커스텀 드라이버 등록을 마무리할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 둘지 고민된다면, `app` 디렉터리 안에 `Extensions` 네임스페이스를 만들 수 있습니다. 다만 Laravel은 엄격한 애플리케이션 구조를 강제하지 않으므로, 원하는 방식으로 애플리케이션을 자유롭게 구성할 수 있다는 점을 기억하십시오.

<a name="registering-the-driver"></a>
### 드라이버 등록

커스텀 캐시 드라이버를 Laravel에 등록하려면 `Cache` 파사드의 `extend` 메서드를 사용합니다. 다른 서비스 프로바이더가 자신의 `boot` 메서드 안에서 캐시된 값을 읽으려고 할 수 있으므로, 커스텀 드라이버는 `booting` 콜백 안에서 등록합니다. `booting` 콜백을 사용하면 애플리케이션의 서비스 프로바이더에서 `boot` 메서드가 호출되기 직전이면서, 모든 서비스 프로바이더의 `register` 메서드가 호출된 이후에 커스텀 드라이버가 등록되도록 보장할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 안에서 `booting` 콜백을 등록하겠습니다:

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

`extend` 메서드에 전달되는 첫 번째 인수는 드라이버의 이름입니다. 이 이름은 `config/cache.php` 설정 파일의 `driver` 옵션에 대응됩니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 클로저에는 [서비스 컨테이너](/docs/master/container)의 인스턴스인 `$app` 인스턴스가 전달됩니다.

확장이 등록되면 애플리케이션의 `CACHE_STORE` 환경 변수 또는 `config/cache.php` 설정 파일의 `default` 옵션을 확장 이름으로 업데이트합니다.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업에서 코드를 실행하려면 캐시가 디스패치하는 다양한 [이벤트](/docs/master/events)를 수신할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                      |
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

성능을 높이려면 애플리케이션의 `config/cache.php` 설정 파일에서 특정 캐시 저장소의 `events` 설정 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
