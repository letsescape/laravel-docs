# 캐시 (Cache)

- [소개](#introduction)
- [구성](#configuration)
    - [드라이버 전제조건](#driver-prerequisites)
- [캐시 사용량](#cache-usage)
    - [캐시 인스턴스 획득](#obtaining-a-cache-instance)
    - [캐시에서 항목 검색](#retrieving-items-from-the-cache)
    - [캐시에 아이템 저장하기](#storing-items-in-the-cache)
    - [캐시에서 항목 제거](#removing-items-from-the-cache)
    - [캐시 메모](#cache-memoization)
    - [캐시 도우미](#the-cache-helper)
- [캐시 태그](#cache-tags)
- [원자 잠금](#atomic-locks)
    - [잠금 관리](#managing-locks)
    - [프로세스 간 잠금 관리](#managing-locks-across-processes)
    - [동시성 제한](#concurrency-limiting)
- [캐시 장애 조치](#cache-failover)
- [사용자 지정 캐시 드라이버 추가](#adding-custom-cache-drivers)
    - [드라이버 작성](#writing-the-driver)
    - [드라이버 등록](#registering-the-driver)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 수행되는 일부 데이터 검색 또는 처리 작업은 CPU를 많이 사용하거나 완료하는 데 몇 초가 걸릴 수 있습니다. 이 경우 동일한 데이터에 대한 후속 요청에서 신속하게 검색할 수 있도록 검색된 데이터를 일정 기간 동안 캐시하는 것이 일반적입니다. 캐시된 데이터는 일반적으로 [Memcached](https://memcached.org) 또는 [Redis](https://redis.io)와 같은 매우 빠른 데이터 저장소에 저장됩니다.

다행히도 Laravel는 다양한 캐시 백엔드를 위한 표현력이 뛰어나고 통합된 API를 제공하여 매우 빠른 데이터 검색을 활용하고 웹 애플리케이션 속도를 높일 수 있습니다.

<a name="configuration"></a>
## 구성 (Configuration)

애플리케이션의 캐시 구성 파일은 `config/cache.php`에 있습니다. 이 파일에서는 애플리케이션 전체에서 기본적으로 사용할 캐시 저장소를 지정할 수 있습니다. Laravel는 [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb)와 같은 널리 사용되는 캐싱 백엔드 및 관계형 데이터베이스를 즉시 지원합니다. 또한 파일 기반 캐시 드라이버를 사용할 수 있으며, `array` 및 `null` 캐시 드라이버는 자동화된 테스트를 위한 편리한 캐시 백엔드를 제공합니다.

캐시 구성 파일에는 검토할 수 있는 다양한 기타 옵션도 포함되어 있습니다. 기본적으로 Laravel는 직렬화되고 캐시된 개체를 애플리케이션 데이터베이스에 저장하는 `database` 캐시 드라이버를 사용하도록 구성됩니다.

<a name="driver-prerequisites"></a>
### 드라이버 전제 조건

<a name="prerequisites-database"></a>
#### 데이터 베이스

`database` 캐시 드라이버를 사용하는 경우 캐시 데이터를 포함할 데이터베이스 테이블이 필요합니다. 일반적으로 이는 Laravel의 기본 `0001_01_01_000001_create_cache_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 그러나 애플리케이션에 이 마이그레이션이 포함되어 있지 않으면 `make:cache-table` Artisan 명령을 사용하여 생성할 수 있습니다.

```shell
php artisan make:cache-table

php artisan migrate
```

<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. `config/cache.php` 구성 파일에 모든 Memcached 서버를 나열할 수 있습니다. 이 파일에는 시작하는 데 도움이 되는 `memcached.servers` 항목이 이미 포함되어 있습니다.

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

필요한 경우 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이렇게 하면 `port` 옵션이 `0`로 설정되어야 합니다.

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

Laravel와 함께 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지(~2.0)를 설치해야 합니다. [Laravel Sail](/docs/12.x/sail)에는 이미 이 확장 기능이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 기본적으로 PhpRedis 확장이 설치되어 있습니다.

Redis 구성에 대한 자세한 내용은 [Laravel 설명서 페이지](/docs/12.x/redis#configuration)를 참조하세요.

<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에 캐시된 모든 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`로 지정되어야 합니다. 그러나 `cache` 구성 파일 내의 `stores.dynamodb.table` 구성 값을 기반으로 테이블 이름을 지정해야 합니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수를 통해 설정할 수도 있습니다.

이 테이블에는 애플리케이션의 `cache` 구성 파일에 있는 `stores.dynamodb.attributes.key` 구성 항목의 값에 해당하는 이름의 문자열 파티션 키도 있어야 합니다. 기본적으로 파티션 키 이름은 `key`로 지정되어야 합니다.

일반적으로 DynamoDB는 만료된 항목을 테이블에서 사전에 제거하지 않습니다. 따라서 테이블에서 [TTL(Time to Live)을 활성화](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)해야 합니다. 테이블의 TTL 설정을 구성할 때 TTL 속성 이름을 `expires_at`로 설정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

또한 DynamoDB 캐시 저장소 구성 옵션에 대한 값이 제공되었는지 확인해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY`와 같은 옵션은 애플리케이션의 `.env` 구성 파일에 정의되어야 합니다.

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

MongoDB를 사용하는 경우 `mongodb` 캐시 드라이버는 공식 `mongodb/laravel-mongodb` 패키지에서 제공되며 `mongodb` 데이터베이스 연결을 사용하여 구성할 수 있습니다. MongoDB는 만료된 캐시 항목을 자동으로 지우는 데 사용할 수 있는 TTL 인덱스를 지원합니다.

MongoDB 구성에 대한 자세한 내용은 MongoDB [캐시 및 잠금 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참조하세요.

<a name="cache-usage"></a>
## 캐시 사용량 (Cache Usage)

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 저장소 인스턴스를 얻으려면 이 문서 전체에서 사용할 `Cache` 외관을 사용할 수 있습니다. `Cache` 외관은 Laravel 캐시 계약의 기본 구현에 대한 편리하고 간결한 액세스를 제공합니다.

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
#### 여러 캐시 저장소에 액세스

`Cache` 파사드를 사용하면 `store` 메소드를 통해 다양한 캐시 저장소에 접근할 수 있습니다. `store` 메서드에 전달된 키는 `cache` 구성 파일의 `stores` 구성 배열에 나열된 저장소 중 하나와 일치해야 합니다.

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```

<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 검색

`Cache` 파사드의 `get` 메소드는 캐시에서 항목을 검색하는 데 사용됩니다. 항목이 캐시에 없으면 `null`가 반환됩니다. 원하는 경우 항목이 존재하지 않는 경우 반환하려는 기본값을 지정하는 두 번째 인수를 `get` 메서드에 전달할 수 있습니다.

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```

클로저를 기본값으로 전달할 수도 있습니다. 지정된 항목이 캐시에 없으면 폐쇄 결과가 반환됩니다. 클로저를 전달하면 데이터베이스나 기타 외부 서비스에서 기본값 검색을 연기할 수 있습니다.

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```

<a name="determining-item-existence"></a>
#### 아이템 존재 여부 확인

`has` 메서드는 캐시에 항목이 있는지 확인하는 데 사용될 수 있습니다. 항목이 존재하지만 해당 값이 `null`인 경우에도 이 메서드는 `false`를 반환합니다.

```php
if (Cache::has('key')) {
    // ...
}
```

<a name="incrementing-decrementing-values"></a>
#### 값 증가/감소

`increment` 및 `decrement` 메소드는 캐시의 정수 항목 값을 조정하는 데 사용될 수 있습니다. 이 두 메소드 모두 항목 값을 늘리거나 줄일 양을 나타내는 선택적인 두 번째 인수를 허용합니다.

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
#### 검색 및 저장

때로는 캐시에서 항목을 검색하고 싶을 수도 있지만, 요청한 항목이 존재하지 않는 경우 기본값을 저장할 수도 있습니다. 예를 들어 캐시에서 모든 사용자를 검색하거나, 존재하지 않는 경우 데이터베이스에서 검색하여 캐시에 추가할 수 있습니다. `Cache::remember` 메소드를 사용하여 이 작업을 수행할 수 있습니다.

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

항목이 캐시에 없으면 `remember` 메서드에 전달된 클로저가 실행되고 해당 결과가 캐시에 저장됩니다.

`rememberForever` 메소드를 사용하여 캐시에서 항목을 검색하거나 항목이 존재하지 않는 경우 영원히 저장할 수 있습니다.

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```

<a name="swr"></a>
#### 재검증하는 동안 유효하지 않음

`Cache::remember` 방법을 사용할 때 캐시된 값이 만료되면 일부 사용자는 응답 시간이 느려질 수 있습니다. 특정 유형의 데이터의 경우 캐시된 값이 백그라운드에서 다시 계산되는 동안 부분적으로 오래된 데이터가 제공되도록 허용하여 캐시된 값이 계산되는 동안 일부 사용자의 응답 시간이 느려지는 것을 방지하는 것이 유용할 수 있습니다. 이를 종종 "재검증 중 오래된" 패턴이라고 하며, `Cache::flexible` 메서드는 이 패턴의 구현을 제공합니다.

유연한 메서드는 캐시된 값이 "최신"으로 간주되는 기간과 "부실" 상태가 되는 시기를 지정하는 배열을 허용합니다. 배열의 첫 번째 값은 캐시가 새로운 것으로 간주되는 시간(초)을 나타내고, 두 번째 값은 재계산이 필요하기 전에 오래된 데이터로 제공될 수 있는 기간을 정의합니다.

신규 기간(첫 번째 값 이전) 내에 요청이 이루어지면 재계산 없이 즉시 캐시를 반환합니다. 오래된 값(두 값 사이) 동안 요청이 이루어지면 오래된 값을 사용자에게 제공하고, 사용자에게 응답이 전송된 후 캐시된 값을 새로 고치도록 [지연 함수](/docs/12.x/helpers#deferred-functions)가 등록됩니다. 두 번째 값 이후에 요청이 이루어지면 캐시가 만료된 것으로 간주되고 값이 즉시 다시 계산되므로 사용자에 대한 응답이 느려질 수 있습니다.

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```

<a name="retrieve-delete"></a>
#### 검색 및 삭제

캐시에서 항목을 검색한 후 해당 항목을 삭제해야 하는 경우 `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로 `null`는 항목이 캐시에 없으면 반환됩니다.

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```

<a name="storing-items-in-the-cache"></a>
### 캐시에 항목 저장

캐시에 항목을 저장하기 위해 `Cache` 파사드의 `put` 메소드를 사용할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```

`put` 메소드에 저장 시간이 전달되지 않으면 항목이 무기한 저장됩니다.

```php
Cache::put('key', 'value');
```

초 수를 정수로 전달하는 대신 캐시된 항목의 원하는 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다.

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```

<a name="store-if-not-present"></a>
#### 존재하지 않는 경우 저장

`add` 메서드는 항목이 캐시 저장소에 아직 없는 경우에만 캐시에 항목을 추가합니다. 항목이 실제로 캐시에 추가되면 메서드는 `true`를 반환합니다. 그렇지 않으면 메서드는 `false`를 반환합니다. `add` 메서드는 원자성 작업입니다.

```php
Cache::add('key', 'value', $seconds);
```

<a name="storing-items-forever"></a>
#### 아이템을 영원히 보관하기

`forever` 메소드는 항목을 캐시에 영구적으로 저장하는 데 사용될 수 있습니다. 이러한 항목은 만료되지 않으므로 `forget` 메서드를 사용하여 캐시에서 수동으로 제거해야 합니다.

```php
Cache::forever('key', 'value');
```

> [!NOTE]
> Memcached 드라이버를 사용하는 경우 "영원히" 저장된 항목은 캐시가 크기 제한에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거

`forget` 메소드를 사용하여 캐시에서 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```

만료 시간(초)을 0 또는 음수로 제공하여 항목을 제거할 수도 있습니다.

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```

`flush` 메소드를 사용하여 전체 캐시를 지울 수 있습니다:

```php
Cache::flush();
```

> [!WARNING]
> 캐시를 플러시하면 구성된 캐시 "접두사"가 적용되지 않으며 캐시에서 모든 항목이 제거됩니다. 다른 애플리케이션에서 공유하는 캐시를 지울 때 이 점을 주의 깊게 고려하십시오.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버를 사용하면 단일 요청 또는 작업 실행 중에 확인된 캐시 값을 메모리에 일시적으로 저장할 수 있습니다. 이는 동일한 실행 내에서 반복되는 캐시 적중을 방지하여 성능을 크게 향상시킵니다.

메모된 캐시를 사용하려면 `memo` 메소드를 호출하십시오.

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```

`memo` 메소드는 메모된 드라이버가 장식할 기본 캐시 저장소를 지정하는 캐시 저장소의 이름을 선택적으로 허용합니다.

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```

특정 키에 대한 첫 번째 `get` 호출은 캐시 저장소에서 값을 검색하지만 동일한 요청 또는 작업 내의 후속 호출은 메모리에서 값을 검색합니다.

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```

캐시 값을 수정하는 메서드(예: `put`, `increment`, `remember` 등)를 호출하면 메모된 캐시는 자동으로 메모된 값을 잊어버리고 변경 메서드 호출을 기본 캐시 저장소에 위임합니다.

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```

<a name="the-cache-helper"></a>
### 캐시 도우미

`Cache` 파사드를 사용하는 것 외에도 전역 `cache` 함수를 사용하여 캐시를 통해 데이터를 검색하고 저장할 수도 있습니다. 단일 문자열 인수를 사용하여 `cache` 함수를 호출하면 지정된 키의 값이 반환됩니다.

```php
$value = cache('key');
```

함수에 키/값 쌍 배열과 만료 시간을 제공하면 지정된 기간 동안 값이 캐시에 저장됩니다.

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```

인수 없이 `cache` 함수를 호출하면 `Illuminate\Contracts\Cache\Factory` 구현의 인스턴스가 반환되므로 다른 캐싱 메서드를 호출할 수 있습니다.

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```

> [!NOTE]
> 전역 `cache` 함수에 대한 호출을 테스트할 때 마치 [외관을 테스트](/docs/12.x/mocking#mocking-facades)하는 것처럼 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그 (Cache Tags)

> [!WARNING]
> `file`, `dynamodb` 또는 `database` 캐시 드라이버를 사용하는 경우 캐시 태그가 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 저장

캐시 태그를 사용하면 캐시의 관련 항목에 태그를 지정한 다음 특정 태그에 할당된 캐시된 값을 모두 플러시할 수 있습니다. 태그 이름의 정렬된 배열을 전달하여 태그된 캐시에 액세스할 수 있습니다. 예를 들어 태그가 지정된 캐시에 액세스하고 `put` 값을 캐시에 액세스해 보겠습니다.

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```

<a name="accessing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목에 액세스

태그를 통해 저장된 항목은 값을 저장하는 데 사용된 태그를 제공하지 않으면 액세스할 수 없습니다. 태그가 지정된 캐시 항목을 검색하려면 동일한 순서의 태그 목록을 `tags` 메서드에 전달한 다음 검색하려는 키를 사용하여 `get` 메서드를 호출하세요.

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```

<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

태그 또는 태그 목록이 할당된 모든 항목을 플러시할 수 있습니다. 예를 들어 다음 코드는 `people`, `authors` 또는 둘 다로 태그가 지정된 모든 캐시를 제거합니다. 따라서 `Anne` 및 `John`는 모두 캐시에서 제거됩니다.

```php
Cache::tags(['people', 'authors'])->flush();
```

대조적으로, 아래 코드는 `authors`로 태그된 캐시된 값만 제거하므로 `Anne`는 제거되지만 `John`는 제거되지 않습니다.

```php
Cache::tags('authors')->flush();
```

<a name="atomic-locks"></a>
## 원자 잠금 (Atomic Locks)

> [!WARNING]
> 이 기능을 활용하려면 애플리케이션에서 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 캐시 드라이버를 애플리케이션의 기본 캐시 드라이버로 사용해야 합니다. 또한 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="managing-locks"></a>
### 잠금 관리

원자 잠금을 사용하면 경쟁 조건을 걱정하지 않고 분산 잠금을 조작할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자 잠금을 사용하여 서버에서 한 번에 하나의 원격 작업만 실행되도록 합니다. `Cache::lock` 메소드를 사용하여 잠금을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```

`get` 메소드는 클로저도 허용합니다. 클로저가 실행된 후 Laravel는 자동으로 잠금을 해제합니다.

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```

요청하는 순간 잠금을 사용할 수 없는 경우 Laravel에 지정된 시간(초) 동안 기다리도록 지시할 수 있습니다. 지정된 시간 제한 내에 잠금을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`가 발생합니다.

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

위의 예는 클로저를 `block` 메소드에 전달하여 단순화할 수 있습니다. 클로저가 이 메소드에 전달되면 Laravel는 지정된 시간(초) 동안 잠금을 획득하려고 시도하고 클로저가 실행되면 자동으로 잠금을 해제합니다.

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```

<a name="managing-locks-across-processes"></a>
### 프로세스 간 잠금 관리

때로는 한 프로세스에서 잠금을 획득하고 다른 프로세스에서 잠금을 해제하고 싶을 수도 있습니다. 예를 들어, 웹 요청 중에 잠금을 획득하고 해당 요청에 의해 트리거되는 대기 중인 작업이 끝날 때 잠금을 해제하려고 할 수 있습니다. 이 시나리오에서는 작업이 지정된 토큰을 사용하여 잠금을 다시 인스턴스화할 수 있도록 잠금의 범위가 지정된 "소유자 토큰"을 큐에 있는 작업에 전달해야 합니다.

아래 예에서는 잠금이 성공적으로 획득되면 대기 중인 작업을 디스패치합니다. 또한 잠금의 `owner` 메서드를 통해 잠금의 소유자 토큰을 큐에 있는 작업에 전달합니다.

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```

애플리케이션의 `ProcessPodcast` 작업 내에서 소유자 토큰을 사용하여 잠금을 복원하고 해제할 수 있습니다.

```php
Cache::restoreLock('processing', $this->owner)->release();
```

현재 소유자를 고려하지 않고 잠금을 해제하려면 `forceRelease` 메소드를 사용할 수 있습니다.

```php
Cache::lock('processing')->forceRelease();
```

<a name="concurrency-limiting"></a>
### 동시성 제한

Laravel의 원자 잠금 기능은 클로저의 동시 실행을 제한하는 몇 가지 방법도 제공합니다. 인프라 전체에서 실행 중인 인스턴스를 하나만 허용하려면 `withoutOverlapping`를 사용하세요.

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```

기본적으로 잠금은 클로저 실행이 완료될 때까지 유지되며 메서드는 잠금을 획득하기 위해 최대 10초를 기다립니다. 추가 인수를 사용하여 이러한 값을 맞춤설정할 수 있습니다.

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```

지정된 대기 시간 내에 잠금을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`가 발생합니다.

병렬 처리를 제어하려면 `funnel` 메서드를 사용하여 최대 동시 실행 수를 설정하세요. `funnel` 방법은 잠금을 지원하는 모든 캐시 드라이버에서 작동합니다.

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

`funnel` 키는 제한되는 리소스를 식별합니다. `limit` 메서드는 최대 동시 실행을 정의합니다. `releaseAfter` 방법은 획득한 슬롯이 자동으로 해제되기 전에 안전 시간 초과를 초 단위로 설정합니다. `block` 방법은 사용 가능한 슬롯을 기다리는 시간(초)을 설정합니다.

실패 종료를 제공하는 대신 예외를 통해 시간 초과를 처리하려는 경우 두 번째 종료를 생략할 수 있습니다. 지정된 대기 시간 내에 잠금을 획득할 수 없으면 `Illuminate\Cache\Limiters\LimiterTimeoutException`가 발생합니다.

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

동시성 제한에 대해 특정 캐시 저장소를 사용하려면 원하는 저장소에서 `funnel` 메서드를 호출할 수 있습니다.

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```

> [!NOTE]
> `funnel` 방법에는 `Illuminate\Contracts\Cache\LockProvider` 인터페이스를 구현하기 위한 캐시 저장소가 필요합니다. 잠금을 지원하지 않는 캐시 저장소와 함께 `funnel`를 사용하려고 하면 `BadMethodCallException`가 발생합니다.

<a name="cache-failover"></a>
## 캐시 장애 조치 (Cache Failover)

`failover` 캐시 드라이버는 캐시와 상호 작용할 때 자동 장애 조치 기능을 제공합니다. 어떤 이유로든 `failover` 저장소의 기본 캐시 저장소가 실패하면 Laravel는 자동으로 목록에 구성된 다음 저장소를 사용하려고 시도합니다. 이는 캐시 안정성이 중요한 프로덕션 환경에서 고가용성을 보장하는 데 특히 유용합니다.

장애 조치 캐시 저장소를 구성하려면 `failover` 드라이버를 지정하고 순서대로 시도할 저장소 이름 배열을 제공합니다. 기본적으로 Laravel에는 애플리케이션의 `config/cache.php` 구성 파일에 장애 조치 구성 예시가 포함되어 있습니다.

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```

`failover` 드라이버를 사용하는 저장소를 구성한 후에는 장애 조치 기능을 활용하려면 애플리케이션의 `.env` 파일에서 장애 조치 저장소를 기본 캐시 저장소로 설정해야 합니다.

```ini
CACHE_STORE=failover
```

캐시 저장소 작업이 실패하고 장애 조치가 활성화되면 Laravel는 디스패치를 `Illuminate\Cache\Events\CacheFailedOver` 이벤트로 지정하여 캐시 저장소가 실패했음을 보고하거나 기록할 수 있습니다.

<a name="adding-custom-cache-drivers"></a>
## 사용자 지정 캐시 드라이버 추가 (Adding Custom Cache Drivers)

<a name="writing-the-driver"></a>
### 드라이버 작성

사용자 지정 캐시 드라이버를 생성하려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/12.x/contracts)을 구현해야 합니다. 따라서 MongoDB 캐시 구현은 다음과 같을 수 있습니다.

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

MongoDB 연결을 사용하여 이러한 각 메서드를 구현하면 됩니다. 이러한 각 메서드를 구현하는 방법에 대한 예는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)의 `Illuminate\Cache\MemcachedStore`를 살펴보세요. 구현이 완료되면 `Cache` 파사드의 `extend` 메소드를 호출하여 사용자 지정 드라이버 등록을 완료할 수 있습니다.

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```

> [!NOTE]
> 사용자 지정 캐시 드라이버 코드를 어디에 넣을지 궁금하다면 `app` 디렉터리 내에 `Extensions` 네임스페이스를 만들 수 있습니다. 그러나 Laravel에는 엄격한 애플리케이션 구조가 없으며 원하는 대로 애플리케이션을 자유롭게 구성할 수 있다는 점을 명심하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록

사용자 지정 캐시 드라이버를 Laravel에 등록하기 위해 `Cache` 파사드에서 `extend` 메소드를 사용합니다. 다른 서비스 프로바이더가 `boot` 메서드 내에서 캐시된 값을 읽으려고 시도할 수 있으므로 `booting` 콜백 내에 사용자 지정 드라이버를 등록하겠습니다. `booting` 콜백을 사용하면 애플리케이션의 서비스 프로바이더에서 `boot` 메서드가 호출되기 직전에 `register` 메서드가 모든 서비스 프로바이더에서 호출된 후에 사용자 지정 드라이버가 등록되도록 할 수 있습니다. 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에 `booting` 콜백을 등록합니다.

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

`extend` 메소드에 전달된 첫 번째 인수는 드라이버의 이름입니다. 이는 `config/cache.php` 구성 파일의 `driver` 옵션에 해당합니다. 두 번째 인수는 `Illuminate\Cache\Repository` 인스턴스를 반환해야 하는 클로저입니다. 클로저에는 [서비스 컨테이너](/docs/12.x/container)의 인스턴스인 `$app` 인스턴스가 전달됩니다.

확장이 등록되면 애플리케이션의 `config/cache.php` 구성 파일 내 `CACHE_STORE` 환경 변수 또는 `default` 옵션을 확장 이름으로 업데이트하세요.

<a name="events"></a>
## 이벤트 (Events)

모든 캐시 작업에서 코드를 실행하려면 캐시를 통해 다양한 [이벤트](/docs/12.x/events) 디스패치를 수신할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
|----------------------|
| `Illuminate\Cache\Events\CacheFlushed` |
| `Illuminate\Cache\Events\CacheFlushing` |
| `Illuminate\Cache\Events\CacheHit` |
| `Illuminate\Cache\Events\CacheMissed` |
| `Illuminate\Cache\Events\ForgettingKey` |
| `Illuminate\Cache\Events\KeyForgetFailed` |
| `Illuminate\Cache\Events\KeyForgotten` |
| `Illuminate\Cache\Events\KeyWriteFailed` |
| `Illuminate\Cache\Events\KeyWritten` |
| `Illuminate\Cache\Events\RetrievingKey` |
| `Illuminate\Cache\Events\RetrievingManyKeys` |
| `Illuminate\Cache\Events\WritingKey` |
| `Illuminate\Cache\Events\WritingManyKeys` |

</div>

성능을 높이려면 애플리케이션의 `config/cache.php` 구성 파일에서 특정 캐시 저장소에 대해 `events` 구성 옵션을 `false`로 설정하여 캐시 이벤트를 비활성화할 수 있습니다.

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
