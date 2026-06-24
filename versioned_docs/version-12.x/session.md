<!-- # HTTP Session -->
# HTTP Session

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Interacting With the Session](#interacting-with-the-session)
    - [Retrieving Data](#retrieving-data)
    - [Storing Data](#storing-data)
    - [Flash Data](#flash-data)
    - [Deleting Data](#deleting-data)
    - [Regenerating the Session ID](#regenerating-the-session-id)
- [Session Cache](#session-cache)
- [Session Blocking](#session-blocking)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)
    - [Implementing the Driver](#implementing-the-driver)
    - [Registering the Driver](#registering-the-driver)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Since HTTP driven applications are stateless, sessions provide a way to store information about the user across multiple requests. That user information is typically placed in a persistent store / backend that can be accessed from subsequent requests. -->
HTTP 기반 애플리케이션은 상태를 저장하지 않으므로, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 이러한 사용자 정보는 일반적으로 이후의 요청에서 접근할 수 있는 영속성 저장소 또는 백엔드에 저장됩니다.

<!-- Laravel ships with a variety of session backends that are accessed through an expressive, unified API. Support for popular backends such as [Memcached](https://memcached.org), [Redis](https://redis.io), and databases is included. -->
Laravel은 다양한 세션 백엔드를 기본적으로 제공하며, 이를 표현력 있고 통합된 API를 통해 사용할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등과 같은 인기 있는 백엔드를 지원합니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `database` session driver. -->
애플리케이션의 세션 구성 파일은 `config/session.php`에 위치합니다. 이 파일에서 제공되는 옵션들을 반드시 검토하시기 바랍니다. Laravel은 기본적으로 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel includes a variety of drivers: -->
세션의 `driver` 구성 옵션은 각 요청에서 세션 데이터가 저장될 위치를 정의합니다. Laravel은 다양한 드라이버를 포함합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `file` - sessions are stored in `storage/framework/sessions`.
- `cookie` - sessions are stored in secure, encrypted cookies.
- `database` - sessions are stored in a relational database.
- `memcached` / `redis` - sessions are stored in one of these fast, cache-based stores.
- `dynamodb` - sessions are stored in AWS DynamoDB.
- `array` - sessions are stored in a PHP array and will not be persisted.
-->
- `file` - 세션이 `storage/framework/sessions` 디렉토리에 저장됩니다.
- `cookie` - 세션이 보안이 유지되고 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 빠른 캐시 기반 저장소 중 하나에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영속적으로 저장되지 않습니다.

<!-- </div> -->
</div>

> [!NOTE]
> `array` 드라이버는 주로 [testing](/docs/12.x/testing)할 때 사용되며, 세션에 저장된 데이터가 영속적으로 남지 않습니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to ensure that you have a database table to contain the session data. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` [database migration](/docs/12.x/migrations); however, if for any reason you do not have a `sessions` table, you may use the `make:session-table` Artisan command to generate this migration: -->
`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel 기본 [database migration](/docs/12.x/migrations)인 `0001_01_01_000000_create_users_table.php`에 포함되어 있지만, 만약 `sessions` 테이블이 없다면, 다음과 같이 `make:session-table` Artisan 명령어를 사용해 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/12.x/redis#configuration). -->
Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 자세한 내용은 Laravel의 [Redis documentation](/docs/12.x/redis#configuration)를 참고하십시오.

> [!NOTE]
> 세션 스토리지로 사용할 Redis 연결을 지정하려면 `SESSION_CONNECTION` 환경 변수 또는 `session.php` 구성 파일의 `connection` 옵션을 사용할 수 있습니다.

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With the Session -->
## Interacting With the Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/12.x/container): -->
Laravel에서 세션 데이터를 다루는 대표적인 방법은 두 가지가 있습니다: 전역 `session` 헬퍼를 사용하는 방법과 `Request` 인스턴스를 사용하는 방법입니다. 먼저 `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이 방법은 라우트 클로저나 컨트롤러 메서드의 타입힌트로 주입할 수 있습니다. 컨트롤러의 의존성은 Laravel [service container](/docs/12.x/container)를 통해 자동으로 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(Request $request, string $id): View
    {
        $value = $request->session()->get('key');

        // ...

        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}
```

<!-- When you retrieve an item from the session, you may also pass a default value as the second argument to the `get` method. This default value will be returned if the specified key does not exist in the session. If you pass a closure as the default value to the `get` method and the requested key does not exist, the closure will be executed and its result returned: -->
세션에서 항목을 조회할 때는 `get` 메서드의 두 번째 인수로 기본값을 지정할 수 있습니다. 지정한 키가 세션에 존재하지 않을 경우, 해당 기본값이 반환됩니다. 또한, `get` 메서드의 기본값에 클로저를 전달하면, 요청한 키가 존재하지 않을 때 클로저가 실행되어 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
<!-- #### The Global Session Helper -->
#### The Global Session Helper

<!-- You may also use the global `session` PHP function to retrieve and store data in the session. When the `session` helper is called with a single, string argument, it will return the value of that session key. When the helper is called with an array of key / value pairs, those values will be stored in the session: -->
세션 데이터를 조회하거나 저장할 때 전역 `session` PHP 함수를 사용할 수 있습니다. `session` 헬퍼를 문자열 하나로 호출하면 해당 세션 키의 값을 반환합니다. 배열 형태로 키/값 쌍을 전달하면 해당 값들이 세션에 저장됩니다:

```php
Route::get('/home', function () {
    // Retrieve a piece of data from the session...
    $value = session('key');

    // Specifying a default value...
    $value = session('key', 'default');

    // Store a piece of data in the session...
    session(['key' => 'value']);
});
```

> [!NOTE]
> HTTP 요청 인스턴스를 통해 세션을 사용하는 것과 전역 session 헬퍼를 사용하는 것 사이에는 거의 실질적인 차이가 없습니다. 두 방법 모두 테스트 시 `assertSessionHas` 메서드를 사용하여 [testable](/docs/12.x/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
세션에 저장된 모든 데이터를 조회하려면 `all` 메서드를 사용하면 됩니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
<!-- #### Retrieving a Portion of the Session Data -->
#### Retrieving a Portion of the Session Data

<!-- The `only` and `except` methods may be used to retrieve a subset of the session data: -->
세션 데이터 일부만 조회하려면 `only` 및 `except` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining if an Item Exists in the Session -->
#### Determining if an Item Exists in the Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
세션에 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 해당 항목이 존재하고 값이 `null`이 아니면 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
값이 `null`이어도 세션에 항목이 존재하는지 확인하려면 `exists` 메서드를 사용할 수 있습니다:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is not present: -->
세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용합니다. `missing` 메서드는 항목이 없으면 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
세션에 데이터를 저장할 때는 보통 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
<!-- #### Pushing to Array Session Values -->
#### Pushing to Array Session Values

<!-- The `push` method may be used to push a new value onto a session value that is an array. For example, if the `user.teams` key contains an array of team names, you may push a new value onto the array like so: -->
세션 값이 배열일 경우, `push` 메서드를 사용해 새로운 값을 배열에 추가할 수 있습니다. 예를 들어, `user.teams` 키가 팀 이름의 배열을 포함하고 있다면 다음과 같이 새로운 값 추가가 가능합니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving and Deleting an Item -->
#### Retrieving and Deleting an Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` 메서드는 세션에서 항목을 조회함과 동시에 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing and Decrementing Session Values -->
#### Incrementing and Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
세션 데이터에 정수형 값을 저장하고 있고, 이를 증가 또는 감소시키고 싶다면 `increment`, `decrement` 메서드를 사용할 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
<!-- ### Flash Data -->
### Flash Data

<!-- Sometimes you may wish to store items in the session for the next request. You may do so using the `flash` method. Data stored in the session using this method will be available immediately and during the subsequent HTTP request. After the subsequent HTTP request, the flashed data will be deleted. Flash data is primarily useful for short-lived status messages: -->
가끔 특정 데이터를 다음 요청까지 세션에 임시로 저장하고 싶을 때가 있습니다. 이럴 때 `flash` 메서드를 사용합니다. 이 메서드로 세션에 저장된 데이터는 즉시 사용할 수 있으며, 다음 HTTP 요청에도 접근할 수 있습니다. 이후의 요청이 끝나면 플래시 데이터는 삭제됩니다. 플래시 데이터는 주로 단기간의 상태 메시지 등에 유용합니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
플래시 데이터를 여러 요청에 걸쳐 유지하고 싶다면 `reflash` 메서드를 사용할 수 있습니다. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용합니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
현재 요청에만 플래시 데이터를 유지하고 싶다면 `now` 메서드를 사용할 수 있습니다:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 만약 세션의 모든 데이터를 삭제하고 싶다면 `flush` 메서드를 사용할 수 있습니다:

```php
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
<!-- ### Regenerating the Session ID -->
### Regenerating the Session ID

<!-- Regenerating the session ID is often done in order to prevent malicious users from exploiting a [session fixation](https://owasp.org/www-community/attacks/Session_fixation) attack on your application. -->
세션 ID를 재생성하는 것은 주로 악의적인 사용자가 애플리케이션에 [session fixation](https://owasp.org/www-community/attacks/Session_fixation) 공격을 시도하는 것을 방지하기 위해 사용됩니다.

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/12.x/starter-kits) or [Laravel Fortify](/docs/12.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel은 [application starter kits](/docs/12.x/starter-kits)나 [Laravel Fortify](/docs/12.x/fortify)를 사용할 경우 인증 시 자동으로 세션 ID를 재생성합니다. 다만, 수동으로 세션 ID를 재생성해야 한다면 `regenerate` 메서드를 사용할 수 있습니다:

```php
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
세션 ID를 재생성하면서 동시에 모든 세션 데이터를 삭제하려면 `invalidate` 메서드를 사용할 수 있습니다:

```php
$request->session()->invalidate();
```

<a name="session-cache"></a>
<!-- ## Session Cache -->
## Session Cache

<!-- Laravel's session cache provides a convenient way to cache data that is scoped to an individual user session. Unlike the global application cache, session cache data is automatically isolated per session and is cleaned up when the session expires or is destroyed. The session cache supports all the familiar [Laravel cache methods](/docs/12.x/cache) like `get`, `put`, `remember`, `forget`, and more, but scoped to the current session. -->
Laravel의 세션 캐시는 개별 사용자 세션에 범위가 한정된 데이터를 편리하게 캐싱할 수 있는 기능을 제공합니다. 글로벌 애플리케이션 캐시와 달리, 세션 캐시 데이터는 세션마다 자동으로 분리되어 관리되며, 세션이 만료되거나 삭제될 때 함께 정리됩니다. 세션 캐시는 현재 세션에 한정해서 [Laravel cache methods](/docs/12.x/cache)인 `get`, `put`, `remember`, `forget` 등 익숙한 기능들을 사용할 수 있습니다.

<!-- The session cache is perfect for storing temporary, user-specific data that you want to persist across multiple requests within the same session, but don't need to store permanently. This includes things like form data, temporary calculations, API responses, or any other ephemeral data that should be tied to a specific user's session. -->
세션 캐시는 동일 세션 내에서 여러 요청에 걸쳐 임시로 사용자별 데이터를 저장하고 싶을 때 적합합니다. 예를 들어, 폼 데이터, 임시 계산 값, API 응답 등 특정 사용자의 세션에만 일시적으로 남아 있어야 할 휘발성 데이터를 저장할 수 있습니다.

<!-- You can access the session cache through the `cache` method on the session: -->
세션 캐시는 `session`의 `cache` 메서드를 통해 접근할 수 있습니다:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);
```

<!-- For more information on Laravel's cache methods, consult the [cache documentation](/docs/12.x/cache). -->
Laravel 캐시 메서드에 대한 자세한 정보는 [cache documentation](/docs/12.x/cache)를 참고하십시오.

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!WARNING]
> 세션 블로킹을 사용하려면, 애플리케이션이 [atomic locks](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, array 드라이버입니다. 또한 `cookie` 세션 드라이버는 사용할 수 없습니다.

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
Laravel은 기본적으로 동일한 세션을 사용하는 여러 요청이 동시에 실행될 수 있도록 허용합니다. 예를 들어 JavaScript HTTP 라이브러리를 사용하여 동시에 두 번의 HTTP 요청을 보내면, 두 요청이 동시에 처리됩니다. 대부분의 애플리케이션에서는 큰 문제가 없으나, 서로 다른 엔드포인트로 동시에 데이터를 쓰는 일부 케이스에서는 세션 데이터가 유실될 수 있습니다.

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
이 문제를 예방하기 위해, Laravel은 특정 세션에 대한 동시 요청을 제한하는 기능을 제공합니다. 사용하려면 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래 예시에서 `/profile` 엔드포인트로 들어오는 요청은 세션 락을 획득합니다. 락이 유지되는 동안 동일 세션 ID를 공유하는 또 다른 `/profile` 또는 `/order` 요청은 첫 번째 요청이 끝날 때까지 대기합니다:

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` 메서드는 2개의 선택적 인수를 받습니다. `block` 메서드가 받는 첫 번째 인수는 세션 락이 최대 몇 초간 유지될지 지정합니다. 요청이 더 빨리 끝나면 락도 더 빨리 해제됩니다.

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
두 번째 인수는 요청이 세션 락 획득을 시도하면서 얼마나 오래 대기할지 지정합니다. `block` 메서드가 받은 시간 내에 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
두 인수를 모두 생략하면 기본값은 각각 최대 10초 동안 락을 잡고, 10초 동안 락을 얻으려고 시도하게 됩니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
<!-- ## Adding Custom Session Drivers -->
## Adding Custom Session Drivers

<a name="implementing-the-driver"></a>
<!-- ### Implementing the Driver -->
### Implementing the Driver

<!-- If none of the existing session drivers fit your application's needs, Laravel makes it possible to write your own session handler. Your custom session driver should implement PHP's built-in `SessionHandlerInterface`. This interface contains just a few simple methods. A stubbed MongoDB implementation looks like the following: -->
기존 세션 드라이버가 애플리케이션의 요구 사항에 맞지 않는 경우, 직접 세션 핸들러를 구현할 수 있습니다. 사용자 정의 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드만을 포함합니다. 다음은 MongoDB를 예시로 삼은 기본적인 구조입니다:

```php
<?php

namespace App\Extensions;

class MongoSessionHandler implements \SessionHandlerInterface
{
    public function open($savePath, $sessionName) {}
    public function close() {}
    public function read($sessionId) {}
    public function write($sessionId, $data) {}
    public function destroy($sessionId) {}
    public function gc($lifetime) {}
}
```

<!-- Since Laravel does not include a default directory to house your extensions. You are free to place them anywhere you like. In this example, we have created an `Extensions` directory to house the `MongoSessionHandler`. -->
Laravel은 확장 코드를 저장할 기본 디렉터리를 제공하지 않으므로, 원하는 위치에 자유롭게 파일을 둘 수 있습니다. 여기서는 `Extensions` 디렉터리에 `MongoSessionHandler`를 생성했습니다.

<!-- Since the purpose of these methods is not readily understandable, here is an overview of the purpose of each method: -->
각 메서드의 목적이 명확하지 않을 수 있으니, 아래에 간단히 설명합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will rarely need to put anything in this method. You can simply leave this method empty.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB or another storage system of your choice. Again, you should not perform any serialization - Laravel will have already handled that for you.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.
-->
- `open` 메서드는 주로 파일 기반 세션 스토리지 시스템에서 사용됩니다. Laravel은 이미 `file` 세션 드라이버를 제공하므로, 일반적으로 이 메서드는 비워두어도 됩니다.
- `close` 메서드도 `open`과 마찬가지로 대부분의 드라이버에서는 신경 쓰지 않아도 됩니다.
- `read` 메서드는 주어진 `$sessionId`와 연결된 세션 데이터를 문자열로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩은 신경 쓸 필요가 없으며, Laravel이 자동으로 처리해줍니다.
- `write` 메서드는 주어진 `$sessionId`에 대해 `$data` 문자열을 MongoDB 등 원하는 영속성 저장소에 저장해야 합니다. 이 또한 직접 직렬화는 하지 않아도 됩니다.
- `destroy` 메서드는 주어진 `$sessionId`와 연결된 데이터를 영속성 저장소에서 삭제해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 세션 데이터를 모두 삭제해야 합니다. Memcached나 Redis처럼 유효기간이 자동 만료되는 시스템에서는 비워두어도 괜찮습니다.

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/12.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/12.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
드라이버 구현이 완료되었다면 Laravel에 이를 등록해야 합니다. 추가적인 세션 드라이버는 `Session` [facade](/docs/12.x/facades)가 제공하는 `extend` 메서드로 등록할 수 있습니다. [service provider](/docs/12.x/providers)의 `boot` 메서드에서 `extend`를 호출해야 하며, 기존 `App\Providers\AppServiceProvider`에서 하거나 별도의 프로바이더를 새로 만들어도 됩니다:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Session::extend('mongo', function (Application $app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}
```

<!-- Once the session driver has been registered, you may specify the `mongo` driver as your application's session driver using the `SESSION_DRIVER` environment variable or within the application's `config/session.php` configuration file. -->
세션 드라이버 등록이 완료되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 구성 파일을 통해 세션 드라이버로 `mongo`를 지정할 수 있습니다.
