<!-- # HTTP Session -->
# HTTP Session

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Interacting With The Session](#interacting-with-the-session)
    - [Retrieving Data](#retrieving-data)
    - [Storing Data](#storing-data)
    - [Flash Data](#flash-data)
    - [Deleting Data](#deleting-data)
    - [Regenerating The Session ID](#regenerating-the-session-id)
- [Session Blocking](#session-blocking)
- [Adding Custom Session Drivers](#adding-custom-session-drivers)
    - [Implementing The Driver](#implementing-the-driver)
    - [Registering The Driver](#registering-the-driver)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Since HTTP driven applications are stateless, sessions provide a way to store information about the user across multiple requests. That user information is typically placed in a persistent store / backend that can be accessed from subsequent requests. -->
HTTP 기반 애플리케이션은 기본적으로 상태를 유지하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장할 수 있는 방법을 제공합니다. 이런 사용자 정보는 일반적으로 여러 요청에서 접근할 수 있도록 영속적인 저장소(백엔드)에 저장합니다.

<!-- Laravel ships with a variety of session backends that are accessed through an expressive, unified API. Support for popular backends such as [Memcached](https://memcached.org), [Redis](https://redis.io), and databases is included. -->
Laravel은 다양한 세션 백엔드를 제공하며, 이를 표현력이 뛰어나고 통합된 API로 접근할 수 있도록 지원합니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 인기 있는 백엔드도 기본 지원에 포함되어 있습니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for many applications. If your application will be load balanced across multiple web servers, you should choose a centralized store that all servers can access, such as Redis or a database. -->
애플리케이션의 세션 설정 파일은 `config/session.php`에 위치해 있습니다. 이 파일에서 제공되는 다양한 옵션을 반드시 검토하시기 바랍니다. 기본적으로 Laravel은 `file` 세션 드라이버를 사용하도록 설정되어 있는데, 이는 대부분의 애플리케이션에서 잘 동작합니다. 만약 애플리케이션을 여러 웹 서버에 로드 밸런싱 처리할 계획이라면, 모든 서버가 접근할 수 있는 중앙 집중형 저장소(예: Redis나 데이터베이스)를 사용하는 것이 좋습니다.

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel ships with several great drivers out of the box: -->
세션 `driver` 설정 옵션은 각 요청마다 세션 데이터가 저장되는 위치를 정의합니다. Laravel은 여러 훌륭한 드라이버를 기본으로 제공합니다.

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
- `cookie` - 세션이 보안 및 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 이러한 빠른 캐시 기반 저장소에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영속적으로 저장되지 않습니다.

<!-- </div> -->
</div>

> [!TIP]
> array 드라이버는 주로 [testing](/docs/8.x/testing) 과정에서 사용되며, 세션에 저장된 데이터가 영속적으로 저장되지 않습니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to create a table to contain the session records. An example `Schema` declaration for the table may be found below: -->
`database` 세션 드라이버를 사용할 때는 세션 데이터를 저장할 테이블을 생성해야 합니다. 아래는 이 테이블에 대한 예시 `Schema` 선언입니다.

```
Schema::create('sessions', function ($table) {
    $table->string('id')->primary();
    $table->foreignId('user_id')->nullable()->index();
    $table->string('ip_address', 45)->nullable();
    $table->text('user_agent')->nullable();
    $table->text('payload');
    $table->integer('last_activity')->index();
});
```

<!-- You may use the `session:table` Artisan command to generate this migration. To learn more about database migrations, you may consult the complete [migration documentation](/docs/8.x/migrations): -->
`session:table` 아티즌 명령어를 사용하면 이 마이그레이션 파일을 생성할 수 있습니다. 데이터베이스 마이그레이션에 대해 더 자세히 알아보고 싶다면, [migration documentation](/docs/8.x/migrations)를 참고하세요.

```
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/8.x/redis#configuration). -->
Laravel에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정 방법에 대해서는 Laravel [Redis documentation](/docs/8.x/redis#configuration)를 참고하세요.

> [!TIP]
> `session` 설정 파일의 `connection` 옵션을 사용하여 세션이 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With The Session -->
## Interacting With The Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/8.x/container): -->
Laravel에서 세션 데이터를 다루는 기본적인 방법은 두 가지입니다: 전역 `session` 헬퍼 함수 사용 및 `Request` 인스턴스 활용입니다. 먼저, 라우트 클로저나 컨트롤러 메서드에서 타입힌트를 통해 주입받을 수 있는 `Request` 인스턴스를 사용하는 방법을 살펴보겠습니다. 참고로 컨트롤러 메서드의 의존성들은 Laravel [service container](/docs/8.x/container)를 통해 자동 주입됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     *
     * @param  Request  $request
     * @param  int  $id
     * @return Response
     */
    public function show(Request $request, $id)
    {
        $value = $request->session()->get('key');

        //
    }
}
```

<!-- When you retrieve an item from the session, you may also pass a default value as the second argument to the `get` method. This default value will be returned if the specified key does not exist in the session. If you pass a closure as the default value to the `get` method and the requested key does not exist, the closure will be executed and its result returned: -->
세션에서 항목을 가져올 때, `get` 메서드의 두 번째 인수로 기본값을 함께 전달할 수 있습니다. 해당 키가 세션에 존재하지 않으면 이 기본값이 반환됩니다. 만약 `get` 메서드의 기본값으로 클로저를 전달한다면, 요청한 키가 존재하지 않을 때 해당 클로저가 실행되어 그 결과가 반환됩니다.

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
`session`이라는 전역 PHP 함수를 사용해도 세션에서 데이터를 가져오거나 저장할 수 있습니다. `session` 헬퍼에 하나의 문자열 인자를 전달하면 해당 세션 키의 값을 반환합니다. 키/값 쌍의 배열을 전달하면, 그 값들이 세션에 저장됩니다.

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

> [!TIP]
> HTTP 요청 인스턴스로 세션에 접근하는 방법과 전역 `session` 헬퍼를 사용하는 방법은 실질적으로 차이가 거의 없습니다. 두 방법 모두 테스트 케이스에서 사용 가능한 `assertSessionHas` 메서드를 통해 [testable](/docs/8.x/testing)가 가능합니다.

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
세션에 저장된 모든 데이터를 얻으려면, `all` 메서드를 사용할 수 있습니다.

```
$data = $request->session()->all();
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining If An Item Exists In The Session -->
#### Determining If An Item Exists In The Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 항목이 존재하고 그 값이 `null`이 아니면 `true`를 반환합니다.

```
if ($request->session()->has('users')) {
    //
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
값이 `null`이어도 키가 존재하는지만 확인하려면 `exists` 메서드를 사용하세요.

```
if ($request->session()->exists('users')) {
    //
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is `null` or if the item is not present: -->
세션에 특정 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. `missing` 메서드는 해당 항목이 `null`이거나 존재하지 않을 때 `true`를 반환합니다.

```
if ($request->session()->missing('users')) {
    //
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메서드 또는 전역 `session` 헬퍼를 사용합니다.

```
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
<!-- #### Pushing To Array Session Values -->
#### Pushing To Array Session Values

<!-- The `push` method may be used to push a new value onto a session value that is an array. For example, if the `user.teams` key contains an array of team names, you may push a new value onto the array like so: -->
`push` 메서드는 세션에 저장된 배열 값에 새 값을 추가할 때 사용합니다. 예를 들어, `user.teams` 키에 팀 이름 배열이 저장되어 있다면, 아래와 같이 새 값을 추가할 수 있습니다.

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving & Deleting An Item -->
#### Retrieving & Deleting An Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` 메서드는 세션에서 항목을 가져오면서 동시에 삭제할 때 사용합니다.

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing & Decrementing Session Values -->
#### Incrementing & Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
세션에 저장된 값이 정수이고, 그 값을 증가시키거나 감소시키고 싶다면 `increment`와 `decrement` 메서드를 사용할 수 있습니다.

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
다음 요청에서만 임시로 세션에 값을 저장하고 싶다면, `flash` 메서드를 사용할 수 있습니다. 이 방식으로 세션에 저장된 데이터는 즉시 사용 가능하며, 다음 HTTP 요청까지 유지됩니다. 그 이후에는 플래시 데이터가 삭제됩니다. 이런 플래시 데이터는 주로 짧은 처리 결과 메시지를 전달할 때 유용합니다.

```
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
플래시 데이터를 여러 요청에도 계속 유지하고 싶다면, `reflash` 메서드를 사용해 플래시 데이터를 한 번 더 유지할 수 있습니다. 특정 플래시 데이터만 유지하려면 `keep` 메서드를 사용할 수 있습니다.

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
플래시 데이터를 현재 요청에서만 유지하고 싶다면 `now` 메서드를 사용하세요.

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` 메서드는 세션에서 특정 데이터를 삭제합니다. 세션의 모든 데이터를 삭제하려면 `flush` 메서드를 사용하세요.

```
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
<!-- ### Regenerating The Session ID -->
### Regenerating The Session ID

<!-- Regenerating the session ID is often done in order to prevent malicious users from exploiting a [session fixation](https://owasp.org/www-community/attacks/Session_fixation) attack on your application. -->
세션 ID를 재생성하는 것은 [session fixation](https://owasp.org/www-community/attacks/Session_fixation)을 예방하기 위해 자주 사용됩니다.

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/8.x/starter-kits) or [Laravel Fortify](/docs/8.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel의 [application starter kits](/docs/8.x/starter-kits)이나 [Laravel Fortify](/docs/8.x/fortify)를 사용하는 경우, 인증 과정에서 세션 ID가 자동으로 재생성됩니다. 만약 수동으로 세션 ID를 재생성해야 한다면, `regenerate` 메서드를 사용할 수 있습니다.

```
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
세션 ID를 재생성하면서, 동시에 세션 내 모든 데이터를 삭제하려면 `invalidate` 메서드를 사용하세요.

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!NOTE]
> 세션 블로킹을 사용하려면, 애플리케이션에서 [atomic locks](/docs/8.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `database`입니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
기본적으로 Laravel에서는 동일한 세션을 사용하는 요청들이 동시에 실행될 수 있습니다. 예를 들어, 자바스크립트 HTTP 라이브러리를 사용해 두 개의 HTTP 요청을 동시에 보내면 두 요청이 동시에 처리됩니다. 대부분의 애플리케이션에서는 큰 문제가 없지만, 두 개의 서로 다른 엔드포인트에서 동시에 세션 데이터를 기록하는 경우엔 일부 애플리케이션에서 세션 데이터 손실이 발생할 수 있습니다.

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
이를 방지하기 위해, Laravel은 특정 세션에 대해 동시 요청을 제한할 수 있는 기능을 제공합니다. 가장 간단하게는, 라우트 정의에 `block` 메서드를 체이닝해서 사용할 수 있습니다. 아래 예시는 `/profile` 엔드포인트로 들어오는 요청이 세션 락을 획득하도록 합니다. 이 락이 유지되는 동안 동일한 세션 ID를 가진 다른 요청(`/profile`, `/order` 등)은 첫 번째 요청이 실행을 마칠 때까지 대기했다가 계속 수행됩니다.

```
Route::post('/profile', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    //
})->block($lockSeconds = 10, $waitSeconds = 10)
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` 메서드는 두 개의 선택적 인자를 받습니다. `block` 메서드가 받는 첫 번째 인자는 세션 락이 유지될 최대 시간을 초 단위로 지정합니다. 요청이 이 시간 전에 끝나면 락은 더 일찍 해제됩니다.

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
`block` 메서드가 받는 두 번째 인자는 세션 락을 얻기 위해 요청이 대기할 최대 시간을 초 단위로 지정합니다. 만약 정해진 시간 내에 세션 락을 얻지 못한다면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
만약 인자를 전달하지 않으면, 기본적으로 락은 최대 10초간 획득되고, 최대 10초까지 락 획득을 대기합니다.

```
Route::post('/profile', function () {
    //
})->block()
```

<a name="adding-custom-session-drivers"></a>
<!-- ## Adding Custom Session Drivers -->
## Adding Custom Session Drivers

<a name="implementing-the-driver"></a>
<!-- #### Implementing The Driver -->
#### Implementing The Driver

<!-- If none of the existing session drivers fit your application's needs, Laravel makes it possible to write your own session handler. Your custom session driver should implement PHP's built-in `SessionHandlerInterface`. This interface contains just a few simple methods. A stubbed MongoDB implementation looks like the following: -->
기존의 세션 드라이버들이 애플리케이션의 요구사항에 맞지 않는 경우, Laravel에서는 직접 세션 핸들러를 작성할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드만 포함하고 있습니다. 아래는 MongoDB를 예시로 한 구현 스텁입니다.

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

> [!TIP]
> Laravel은 확장 기능을 담기 위한 디렉터리를 기본 제공하지 않습니다. 원하는 위치에 자유롭게 생성해서 사용하실 수 있습니다. 이 예시에서는 `Extensions` 디렉터리를 만들어 `MongoSessionHandler`를 저장했습니다.

<!-- Since the purpose of these methods is not readily understandable, let's quickly cover what each of the methods do: -->
이 메서드들의 역할이 직관적으로 와닿지 않을 수 있으니, 각각의 역할을 간단히 설명하겠습니다.

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
- `open` 메서드는 주로 파일 기반 세션 스토어에서 사용합니다. Laravel에도 `file` 세션 드라이버가 있으나, 대부분의 경우 이 메서드는 비워두어도 괜찮습니다.
- `close` 메서드 역시 `open`과 마찬가지로 대부분의 드라이버에서는 딱히 구현이 필요하지 않습니다.
- `read` 메서드는 주어진 `$sessionId`에 해당하는 세션 데이터를 문자열로 반환해야 합니다. 세션 데이터 직렬화나 인코딩 처리는 Laravel이 알아서 하므로 여기서는 신경 쓰지 않아도 됩니다.
- `write` 메서드는 주어진 `$sessionId`와 함께 `$data` 문자열을 MongoDB 같은 영속적 저장소에 저장해야 합니다. 역시, 별도의 직렬화 처리는 필요하지 않습니다. Laravel이 알아서 처리합니다.
- `destroy` 메서드는 해당 `$sessionId`와 관련된 데이터를 영속적 저장소에서 제거해야 합니다.
- `gc`(garbage collection) 메서드는 주어진 `$lifetime`(유닉스 타임스탬프)보다 오래된 모든 세션 데이터를 제거하는 역할입니다. Memcached나 Redis처럼 자체적으로 만료 처리를 하는 시스템에선 비워 두어도 무방합니다.

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- #### Registering The Driver -->
#### Registering The Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/8.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/8.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
드라이버를 모두 구현했다면, 이제 Laravel에 등록할 준비가 되었습니다. 추가 드라이버를 Laravel 세션 백엔드에 등록하려면, `Session` [facade](/docs/8.x/facades)에서 제공하는 `extend` 메서드를 사용할 수 있습니다. `extend` 메서드는 [service provider](/docs/8.x/providers)의 `boot` 메서드에서 호출해야 하며, 기존의 `App\Providers\AppServiceProvider`에서 하거나, 별도의 프로바이더를 새로 만들어도 됩니다.

```
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Session::extend('mongo', function ($app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}
```

<!-- Once the session driver has been registered, you may use the `mongo` driver in your `config/session.php` configuration file. -->
세션 드라이버가 등록되었다면, `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.
