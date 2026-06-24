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
- [Session Blocking](#session-blocking)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)
    - [Implementing the Driver](#implementing-the-driver)
    - [Registering the Driver](#registering-the-driver)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Since HTTP driven applications are stateless, sessions provide a way to store information about the user across multiple requests. That user information is typically placed in a persistent store / backend that can be accessed from subsequent requests. -->
HTTP 기반 애플리케이션은 상태를 저장하지 못하기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장할 수 있는 방법을 제공합니다. 이 사용자 정보는 일반적으로 추후의 요청에서 접근할 수 있는 영속적인 저장소(백엔드)에 보관됩니다.

<!-- Laravel ships with a variety of session backends that are accessed through an expressive, unified API. Support for popular backends such as [Memcached](https://memcached.org), [Redis](https://redis.io), and databases is included. -->
Laravel은 다양한 세션 백엔드를 제공하며, 이들은 모두 표현력 있고 통합된 API를 통해 접근할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스와 같은 널리 사용되는 백엔드도 기본적으로 지원합니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `database` session driver. -->
애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에서 다양한 옵션을 확인하고 필요한 설정을 진행하시기 바랍니다. Laravel은 기본적으로 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel includes a variety of drivers: -->
세션의 `driver` 설정 옵션은 각 요청에 대해 세션 데이터가 어디에 저장될지를 정의합니다. Laravel은 다음과 같은 여러 드라이버를 제공합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `file` - sessions are stored in `storage/framework/sessions`.
- `cookie` - sessions are stored in secure, encrypted cookies.
- `database` - sessions are stored in a relational database.
- `memcached` / `redis` - sessions are stored in one of these fast, cache based stores.
- `dynamodb` - sessions are stored in AWS DynamoDB.
- `array` - sessions are stored in a PHP array and will not be persisted.
-->
- `file` - 세션이 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션이 보안 처리된 암호화 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영구적으로 남지 않습니다.

<!-- </div> -->
</div>

> [!NOTE]
> array 드라이버는 주로 [testing](/docs/11.x/testing) 용도로 사용되며, 세션에 저장된 데이터가 영구적으로 유지되지 않습니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to ensure that you have a database table to contain the session data. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` [database migration](/docs/11.x/migrations); however, if for any reason you do not have a `sessions` table, you may use the `make:session-table` Artisan command to generate this migration: -->
`database` 세션 드라이버를 사용할 경우, 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 이 테이블은 보통 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [database migration](/docs/11.x/migrations)에 포함되어 있습니다. 하지만 만약 `sessions` 테이블이 없다면, `make:session-table` Artisan 명령어를 사용해서 해당 마이그레이션 파일을 생성할 수 있습니다.

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/11.x/redis#configuration). -->
Laravel에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나 Composer를 이용해 `predis/predis` 패키지(~1.0 버전)를 설치해야 합니다. Redis 설정에 대한 보다 자세한 내용은 Laravel의 [Redis documentation](/docs/11.x/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션을 이용해 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With the Session -->
## Interacting With the Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/11.x/container): -->
Laravel에서는 세션 데이터와 상호작용하는 대표적인 방법이 두 가지 있습니다. 전역 `session` 헬퍼 사용과 `Request` 인스턴스를 통한 접근입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에 타입 힌트로 전달되는 `Request` 인스턴스를 이용한 접근 방법을 보겠습니다. 참고로, 컨트롤러 메서드의 의존성은 Laravel [service container](/docs/11.x/container)를 통해 자동으로 주입됩니다.

```
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
세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 지정할 수 있습니다. 지정한 키가 세션에 없다면 이 기본값이 반환됩니다. 만약 `get` 메서드의 기본값으로 클로저를 전달하면, 해당 키가 없을 때 클로저가 실행되고 그 반환값이 사용됩니다.

```
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
<!-- #### The Global Session Helper -->
#### The Global Session Helper

<!-- You may also use the global `session` PHP function to retrieve and store data in the session. When the `session` helper is called with a single, string argument, it will return the value of that session key. When the helper is called with an array of key / value pairs, those values will be stored in the session: -->
또한 전역 `session` PHP 함수를 사용해 세션 데이터 조회 및 저장이 가능합니다. `session` 헬퍼에 하나의 문자열 인수를 전달하면 해당 세션 키의 값을 반환합니다. 배열 형태의 키/값 쌍을 전달하면 해당 값들이 세션에 저장됩니다.

```
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
> HTTP 요청 인스턴스를 통한 세션 접근과 글로벌 `session` 헬퍼 사용에는 실질적인 차이가 거의 없습니다. 두 방법 모두 테스트 코드에서 `assertSessionHas` 메서드(모든 테스트 케이스에서 사용 가능)를 통해 [testable](/docs/11.x/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
세션의 모든 데이터를 한 번에 조회하고 싶다면, `all` 메서드를 사용할 수 있습니다.

```
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
<!-- #### Retrieving a Portion of the Session Data -->
#### Retrieving a Portion of the Session Data

<!-- The `only` and `except` methods may be used to retrieve a subset of the session data: -->
`only`와 `except` 메서드를 사용하면 세션 데이터의 일부만 추출할 수 있습니다.

```
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining if an Item Exists in the Session -->
#### Determining if an Item Exists in the Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has`는 해당 항목이 존재하며 `null`이 아닌 경우에 `true`를 반환합니다.

```
if ($request->session()->has('users')) {
    // ...
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
값이 `null`이더라도 항목 자체가 세션에 존재하는지 확인하려면 `exists` 메서드를 사용합니다.

```
if ($request->session()->exists('users')) {
    // ...
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is not present: -->
세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. `missing` 메서드는 항목이 없으면 `true`를 반환합니다.

```
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
세션에 데이터를 저장하려면 보통 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다.

```
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
<!-- #### Pushing to Array Session Values -->
#### Pushing to Array Session Values

<!-- The `push` method may be used to push a new value onto a session value that is an array. For example, if the `user.teams` key contains an array of team names, you may push a new value onto the array like so: -->
`push` 메서드는 세션에서 배열 타입 값을 가진 키에 새 값을 추가할 때 사용합니다. 예를 들어 `user.teams` 키가 팀 이름 배열을 가지고 있다면, 아래와 같이 값을 추가할 수 있습니다.

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving and Deleting an Item -->
#### Retrieving and Deleting an Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` 메서드는 세션에서 항목을 조회하는 동시에 삭제합니다.

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing and Decrementing Session Values -->
#### Incrementing and Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
세션 데이터가 정수이고 이를 증가시키거나 감소시켜야 한다면, `increment`와 `decrement` 메서드를 사용할 수 있습니다.

```
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
<!-- ### Flash Data -->
### Flash Data

<!-- Sometimes you may wish to store items in the session for the next request. You may do so using the `flash` method. Data stored in the session using this method will be available immediately and during the subsequent HTTP request. After the subsequent HTTP request, the flashed data will be deleted. Flash data is primarily useful for short-lived status messages: -->
때로는 특정 항목을 다음 요청에서만 일시적으로 저장하고 싶을 때가 있습니다. 이 경우 `flash` 메서드를 사용하면 현재 요청과 그 다음 HTTP 요청까지 데이터를 사용할 수 있고, 그 후에는 자동으로 삭제됩니다. Flash 데이터는 주로 짧은 상태 메시지 등에 활용됩니다.

```
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
Flash 데이터를 여러 요청에 걸쳐 유지하고 싶다면, `reflash` 메서드를 사용하면 모든 flash 데이터를 추가 한 번의 요청 동안 더 유지할 수 있습니다. 특정 flash 데이터만 유지하려면 `keep` 메서드를 사용합니다.

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
Flash 데이터를 오직 현재 요청에만 저장하고 싶다면, `now` 메서드를 사용할 수 있습니다.

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 세션의 모든 데이터를 한 번에 삭제하려면 `flush` 메서드를 사용할 수 있습니다.

```
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
세션 고정 [session fixation](https://owasp.org/www-community/attacks/Session_fixation)을 방지하기 위해 세션 ID를 재생성하는 것이 좋습니다.

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/11.x/starter-kits) or [Laravel Fortify](/docs/11.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel은 [application starter kits](/docs/11.x/starter-kits) 또는 [Laravel Fortify](/docs/11.x/fortify)를 사용하는 경우 인증 과정에서 세션 ID를 자동으로 재생성합니다. 하지만 수동으로 세션 ID를 재생성해야 할 경우, 다음과 같이 `regenerate` 메서드를 사용할 수 있습니다.

```
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
세션 ID를 재생성하면서 세션의 모든 데이터까지 한 번에 삭제하려면 `invalidate` 메서드를 사용할 수 있습니다.

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!WARNING]
> 세션 블로킹 기능을 사용하려면, [atomic locks](/docs/11.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 지원되는 드라이버에는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 드라이버가 있으며, `cookie` 세션 드라이버는 사용할 수 없습니다.

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
기본적으로 Laravel에서는 동일한 세션을 사용하는 요청이 동시에 실행될 수 있습니다. 예를 들어 HTTP 라이브러리를 써서 두 개의 HTTP 요청을 동시에 보내면, 이 요청들은 동시에 처리됩니다. 대부분의 애플리케이션에서는 문제가 없지만, 서로 다른 엔드포인트에 동시에 요청을 보내고 둘 다 세션에 데이터를 기록하는 일부 경우에는 세션 데이터가 손실될 수 있습니다.

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
이를 방지하기 위해 Laravel은 세션별 동시 요청을 제한할 수 있는 기능을 제공합니다. 사용 방법은 간단히 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래 예시에서는 `/profile` 엔드포인트로의 들어오는 요청이 세션 락을 획득하게 됩니다. 이 락이 유지되는 동안, 같은 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 다른 요청들은 첫 번째 요청이 완료될 때까지 대기하게 됩니다.

```
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` 메서드는 두 개의 선택적 인수를 받을 수 있습니다. `block` 메서드가 받는 첫 번째 인수는 세션 락이 해제되기 전까지 유지할 최대 시간(초)입니다. 요청이 더 빨리 처리되면 그에 따라 락도 빨리 해제됩니다.

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
`block` 메서드가 받는 두 번째 인수는 락을 얻기 위해 요청이 기다리는 시간(초)입니다. 지정한 시간 내에 세션 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
이 두 인수를 지정하지 않으면, 락은 최대 10초 동안 유지되고, 요청은 락 획득을 위해 최대 10초 동안 대기합니다.

```
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
기존의 세션 드라이버가 애플리케이션에 맞지 않을 경우, Laravel에서 직접 세션 핸들러를 구현할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface` 를 구현해야 합니다. 이 인터페이스에는 몇 가지 기본 메서드만 필요합니다. 아래는 MongoDB를 예시로 한 구현의 골격입니다.

```
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
Laravel은 확장 기능을 둘 기본 디렉토리를 제공하지 않으니, 원하는 위치에 저장해도 괜찮습니다. 여기서는 `Extensions` 디렉토리에 `MongoSessionHandler`를 생성했습니다.

<!-- Since the purpose of these methods is not readily understandable, here is an overview of the purpose of each method: -->
아래에 각 메서드의 용도를 간략히 설명합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `open` method would typically be used in file based session store systems. Since Laravel ships with a `file` session driver, you will rarely need to put anything in this method. You can simply leave this method empty.
- The `close` method, like the `open` method, can also usually be disregarded. For most drivers, it is not needed.
- The `read` method should return the string version of the session data associated with the given `$sessionId`. There is no need to do any serialization or other encoding when retrieving or storing session data in your driver, as Laravel will perform the serialization for you.
- The `write` method should write the given `$data` string associated with the `$sessionId` to some persistent storage system, such as MongoDB or another storage system of your choice.  Again, you should not perform any serialization - Laravel will have already handled that for you.
- The `destroy` method should remove the data associated with the `$sessionId` from persistent storage.
- The `gc` method should destroy all session data that is older than the given `$lifetime`, which is a UNIX timestamp. For self-expiring systems like Memcached and Redis, this method may be left empty.
-->
- `open` 메서드는 보통 파일 기반 세션 저장 시스템에서 사용합니다. Laravel에도 `file` 세션 드라이버가 포함되어 있으므로, 이 메서드는 비워 두어도 무방합니다.
- `close` 메서드는 `open`과 마찬가지로 대개 신경 쓸 필요가 없습니다. 대부분의 드라이버에서는 필요 없습니다.
- `read` 메서드는 주어진 `$sessionId`에 대응되는 세션 데이터를 문자열 형태로 반환해야 합니다. 세션 데이터의 직렬화나 인코딩 처리는 직접 하지 않아도 되며, Laravel이 알아서 처리합니다.
- `write` 메서드는 `$sessionId`에 대응되는 `$data` 문자열을 MongoDB 등 영구 저장소에 기록해야 합니다. 마찬가지로, 직접 직렬화 처리를 하지 않아도 됩니다.
- `destroy` 메서드는 `$sessionId`에 대응되는 데이터를 영구 저장소에서 삭제합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached, Redis처럼 자동 만료되는 시스템의 경우 비워 둬도 괜찮습니다.

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/11.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/11.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
드라이버를 구현했다면 이제 Laravel에 등록할 차례입니다. Laravel 세션 백엔드에 추가적인 드라이버를 등록하려면, `Session` [facade](/docs/11.x/facades)의 `extend` 메서드를 사용할 수 있습니다. [service provider](/docs/11.x/providers)의 `boot` 메서드 안에서 `extend` 메서드를 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에서 설정할 수도 있고, 별도의 프로바이더를 만들어도 됩니다.

```
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
세션 드라이버 등록이 완료되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 설정 파일을 통해 세션 드라이버를 `mongo`로 지정할 수 있습니다.
