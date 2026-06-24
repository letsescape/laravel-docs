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
HTTP 기반 애플리케이션은 본질적으로 상태를 저장하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 이렇게 저장된 사용자 정보는 일반적으로 영속적인 저장소(백엔드)에 저장되어, 이후의 요청에서도 접근할 수 있습니다.

<!-- Laravel ships with a variety of session backends that are accessed through an expressive, unified API. Support for popular backends such as [Memcached](https://memcached.org), [Redis](https://redis.io), and databases is included. -->
Laravel은 다양한 세션 백엔드를 지원하며, 이를 일관성 있고 직관적인 API로 사용할 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 여러 인기 있는 백엔드를 기본적으로 지원합니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's session configuration file is stored at `config/session.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `file` session driver, which will work well for many applications. If your application will be load balanced across multiple web servers, you should choose a centralized store that all servers can access, such as Redis or a database. -->
애플리케이션의 세션 설정 파일은 `config/session.php`에 위치합니다. 이 파일에 제공되는 다양한 옵션들을 꼭 확인해 보시기 바랍니다. Laravel은 기본적으로 `file` 세션 드라이버가 설정되어 있는데, 이 방식은 많은 애플리케이션에서 무리 없이 사용할 수 있습니다. 만약 애플리케이션이 여러 웹 서버에 걸쳐 로드밸런싱될 경우, 모든 서버에서 접근할 수 있는 Redis나 데이터베이스와 같은 중앙 집중식 저장소를 사용하는 것이 좋습니다.

<!-- The session `driver` configuration option defines where session data will be stored for each request. Laravel ships with several great drivers out of the box: -->
세션 `driver` 설정 옵션은 각 요청마다 세션 데이터가 어디에 저장될지를 정의합니다. Laravel은 기본적으로 여러 훌륭한 드라이버를 제공합니다.

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
- `file` - 세션이 `storage/framework/sessions` 디렉터리에 저장됩니다.
- `cookie` - 세션이 보안처리되고 암호화된 쿠키에 저장됩니다.
- `database` - 세션이 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션이 속도가 빠른 캐시 기반 저장소 중 하나에 저장됩니다.
- `dynamodb` - 세션이 AWS DynamoDB에 저장됩니다.
- `array` - 세션이 PHP 배열에 저장되며, 영구적으로 저장되지 않습니다.

<!-- </div> -->
</div>

> [!NOTE]
> array 드라이버는 주로 [testing](/docs/10.x/testing) 시에 사용되며, 세션에 저장되는 데이터가 영구적으로 유지되지 않게 합니다.

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the `database` session driver, you will need to create a table to contain the session records. An example `Schema` declaration for the table may be found below: -->
`database` 세션 드라이버를 사용할 경우, 세션 정보를 저장할 테이블을 생성해야 합니다. 아래는 해당 테이블에 대한 예시적인 `Schema` 선언입니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('sessions', function (Blueprint $table) {
    $table->string('id')->primary();
    $table->foreignId('user_id')->nullable()->index();
    $table->string('ip_address', 45)->nullable();
    $table->text('user_agent')->nullable();
    $table->text('payload');
    $table->integer('last_activity')->index();
});
```

<!-- You may use the `session:table` Artisan command to generate this migration. To learn more about database migrations, you may consult the complete [migration documentation](/docs/10.x/migrations): -->
`session:table` 아티즌 명령어를 사용하면 이 마이그레이션을 생성할 수 있습니다. 데이터베이스 마이그레이션에 대한 더 자세한 정보는 [migration documentation](/docs/10.x/migrations)를 참고하십시오.

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
<!-- #### Redis -->
#### Redis

<!-- Before using Redis sessions with Laravel, you will need to either install the PhpRedis PHP extension via PECL or install the `predis/predis` package (~1.0) via Composer. For more information on configuring Redis, consult Laravel's [Redis documentation](/docs/10.x/redis#configuration). -->
Laravel에서 Redis 세션을 사용하려면, PECL을 통해 PhpRedis PHP 확장 모듈을 설치하거나, Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 더 자세한 내용은 Laravel의 [Redis documentation](/docs/10.x/redis#configuration)를 참고하세요.

> [!NOTE]
> `session` 설정 파일에서 `connection` 옵션을 사용하여 세션에서 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
<!-- ## Interacting With the Session -->
## Interacting With the Session

<a name="retrieving-data"></a>
<!-- ### Retrieving Data -->
### Retrieving Data

<!-- There are two primary ways of working with session data in Laravel: the global `session` helper and via a `Request` instance. First, let's look at accessing the session via a `Request` instance, which can be type-hinted on a route closure or controller method. Remember, controller method dependencies are automatically injected via the Laravel [service container](/docs/10.x/container): -->
Laravel에서 세션 데이터를 다루는 대표적인 방법은 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방식, 두 가지가 있습니다. 먼저, `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보면, 이 인스턴스는 라우트 클로저나 컨트롤러 메서드의 타입힌트로 전달받을 수 있습니다. 참고로, 컨트롤러 메서드의 의존성은 Laravel [service container](/docs/10.x/container)에 의해 자동으로 주입됩니다.

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
세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 지정할 수 있습니다. 요청한 키가 세션에 존재하지 않을 경우 이 기본값이 반환됩니다. 또한, `get` 메서드의 기본값으로 클로저를 전달하면 해당 키가 없을 때 클로저가 실행되어 그 결과가 반환됩니다.

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
세션에 데이터를 저장하거나 조회할 때, 전역 `session` PHP 함수를 사용할 수도 있습니다. `session` 헬퍼에 문자열 하나를 전달하면 해당 세션 키의 값을 반환합니다. 배열 형태로 key/value 쌍을 전달하면, 해당 값들이 세션에 저장됩니다.

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
> HTTP 요청 인스턴스를 통한 세션 사용과 전역 `session` 헬퍼를 사용하는 것 사이에는 실질적인 차이가 거의 없습니다. 두 방식 모두 테스트 케이스에서 `assertSessionHas` 메서드를 이용해 [testable](/docs/10.x/testing)할 수 있습니다.

<a name="retrieving-all-session-data"></a>
<!-- #### Retrieving All Session Data -->
#### Retrieving All Session Data

<!-- If you would like to retrieve all the data in the session, you may use the `all` method: -->
세션에 저장된 모든 데이터를 한번에 조회하려면 `all` 메서드를 사용할 수 있습니다.

```
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
<!-- #### Retrieving a Portion of the Session Data -->
#### Retrieving a Portion of the Session Data

<!-- The `only` and `except` methods may be used to retrieve a subset of the session data: -->
`only`와 `except` 메서드를 사용하면, 세션 데이터 중 일부 키만 골라서 조회할 수 있습니다.

```
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
<!-- #### Determining if an Item Exists in the Session -->
#### Determining if an Item Exists in the Session

<!-- To determine if an item is present in the session, you may use the `has` method. The `has` method returns `true` if the item is present and is not `null`: -->
세션에 특정 항목이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 해당 항목이 존재하고 값이 `null`이 아니면 `true`를 반환합니다.

```
if ($request->session()->has('users')) {
    // ...
}
```

<!-- To determine if an item is present in the session, even if its value is `null`, you may use the `exists` method: -->
해당 항목이 존재하는지만 확인하고 싶을 때(값이 `null`이어도 상관없을 때)는 `exists` 메서드를 사용하세요.

```
if ($request->session()->exists('users')) {
    // ...
}
```

<!-- To determine if an item is not present in the session, you may use the `missing` method. The `missing` method returns `true` if the item is not present: -->
세션에 해당 항목이 없는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. `missing` 메서드는 항목이 없을 때 `true`를 반환합니다.

```
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
<!-- ### Storing Data -->
### Storing Data

<!-- To store data in the session, you will typically use the request instance's `put` method or the global `session` helper: -->
세션에 데이터를 저장하려면 일반적으로 요청 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다.

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
`push` 메서드를 사용하면 세션의 배열 값에 새 값을 추가할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름들의 배열이 들어있다고 할 때, 다음과 같이 새로운 팀을 추가할 수 있습니다.

```
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
<!-- #### Retrieving and Deleting an Item -->
#### Retrieving and Deleting an Item

<!-- The `pull` method will retrieve and delete an item from the session in a single statement: -->
`pull` 메서드는 세션에서 항목을 조회하고, 해당 항목을 곧바로 삭제합니다.

```
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
<!-- #### Incrementing and Decrementing Session Values -->
#### Incrementing and Decrementing Session Values

<!-- If your session data contains an integer you wish to increment or decrement, you may use the `increment` and `decrement` methods: -->
세션 데이터에 정수형 값이 들어있고, 해당 값을 증가시키거나 감소시키고 싶을 때는 `increment`, `decrement` 메서드를 사용할 수 있습니다.

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
특정 데이터를 다음 요청에서만 일시적으로 사용하고 싶을 때 `flash` 메서드를 사용하면 됩니다. 이 방식으로 저장된 데이터는 즉시 그리고 바로 이어지는 다음 HTTP 요청에서만 사용할 수 있고, 그 이후에는 자동으로 삭제됩니다. Flash 데이터는 주로 단기적인 상태 메시지 등에 유용합니다.

```
$request->session()->flash('status', 'Task was successful!');
```

<!-- If you need to persist your flash data for several requests, you may use the `reflash` method, which will keep all of the flash data for an additional request. If you only need to keep specific flash data, you may use the `keep` method: -->
만약 Flash 데이터를 여러 번의 요청에 걸쳐서 유지하고 싶다면, `reflash` 메서드를 사용해 모든 Flash 데이터를 한 번 더 연장할 수 있습니다. 또는, `keep` 메서드로 특정 Flash 데이터만 유지할 수도 있습니다.

```
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

<!-- To persist your flash data only for the current request, you may use the `now` method: -->
Flash 데이터를 현재 요청에서만 유지하고 싶다면, `now` 메서드를 사용할 수 있습니다.

```
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
<!-- ### Deleting Data -->
### Deleting Data

<!-- The `forget` method will remove a piece of data from the session. If you would like to remove all data from the session, you may use the `flush` method: -->
`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 모든 데이터를 전부 제거하고 싶다면 `flush` 메서드를 사용하세요.

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
세션 ID를 재발급하는 것은 [session fixation](https://owasp.org/www-community/attacks/Session_fixation) 공격으로부터 애플리케이션을 보호하기 위해 자주 사용됩니다.

<!-- Laravel automatically regenerates the session ID during authentication if you are using one of the Laravel [application starter kits](/docs/10.x/starter-kits) or [Laravel Fortify](/docs/10.x/fortify); however, if you need to manually regenerate the session ID, you may use the `regenerate` method: -->
Laravel의 [application starter kits](/docs/10.x/starter-kits) 또는 [Laravel Fortify](/docs/10.x/fortify)를 사용한다면, 인증 중에 Laravel이 자동으로 세션 ID를 재발급합니다. 그러나, 수동으로 세션 ID를 재생성해야 할 때는 `regenerate` 메서드를 사용할 수 있습니다.

```
$request->session()->regenerate();
```

<!-- If you need to regenerate the session ID and remove all data from the session in a single statement, you may use the `invalidate` method: -->
세션 ID를 재발급하면서 세션 내 모든 데이터도 한 번에 삭제하고 싶다면, `invalidate` 메서드를 사용하면 됩니다.

```
$request->session()->invalidate();
```

<a name="session-blocking"></a>
<!-- ## Session Blocking -->
## Session Blocking

> [!WARNING]
> 세션 블로킹을 사용하려면, 애플리케이션이 [atomic locks](/docs/10.x/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 캐시 드라이버는 `memcached`, `dynamodb`, `redis`, `database`, `file`, `array` 입니다. 단, `cookie` 세션 드라이버는 사용할 수 없습니다.

<!-- By default, Laravel allows requests using the same session to execute concurrently. So, for example, if you use a JavaScript HTTP library to make two HTTP requests to your application, they will both execute at the same time. For many applications, this is not a problem; however, session data loss can occur in a small subset of applications that make concurrent requests to two different application endpoints which both write data to the session. -->
기본적으로 Laravel은 동일한 세션을 사용하는 요청들이 동시에 실행되도록 허용합니다. 예를 들어, 자바스크립트 HTTP 라이브러리를 사용하여 두 개의 HTTP 요청을 동시에 보내면, 두 요청이 동시에 처리됩니다. 대부분의 애플리케이션에서는 큰 문제가 없지만, 서로 다른 엔드포인트로 동시에 요청이 들어와 모두 세션에 데이터를 기록할 경우, 세션 데이터가 유실될 위험이 있습니다.

<!-- To mitigate this, Laravel provides functionality that allows you to limit concurrent requests for a given session. To get started, you may simply chain the `block` method onto your route definition. In this example, an incoming request to the `/profile` endpoint would acquire a session lock. While this lock is being held, any incoming requests to the `/profile` or `/order` endpoints which share the same session ID will wait for the first request to finish executing before continuing their execution: -->
이런 상황을 방지하기 위해, Laravel은 특정 세션에 대해 동시 요청 수를 제한할 수 있는 기능을 제공합니다. 시작은 route 정의에 `block` 메서드를 체이닝하는 것부터 할 수 있습니다. 아래 예시에서, `/profile` 엔드포인트로 들어온 요청은 세션 락을 획득합니다. 이 락이 유지되는 동안 같은 세션 ID를 공유하는 `/profile`이나 `/order` 엔드포인트로 들어온 추가 요청들은 첫 번째 요청이 끝날 때까지 대기하게 됩니다.

```
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10)
```

<!-- The `block` method accepts two optional arguments. The first argument accepted by the `block` method is the maximum number of seconds the session lock should be held for before it is released. Of course, if the request finishes executing before this time the lock will be released earlier. -->
`block` 메서드는 두 개의 선택적 인수를 받을 수 있습니다. `block` 메서드가 받는 첫 번째 인수는 세션 락이 최대로 유지되어야 하는 시간을 초 단위로 지정합니다. 물론, 요청이 이 시간보다 먼저 종료되면 락도 그 시점에 해제됩니다.

<!-- The second argument accepted by the `block` method is the number of seconds a request should wait while attempting to obtain a session lock. An `Illuminate\Contracts\Cache\LockTimeoutException` will be thrown if the request is unable to obtain a session lock within the given number of seconds. -->
`block` 메서드가 받는 두 번째 인수는 세션 락을 얻기 위해 요청이 대기할 최대 시간을 초 단위로 지정합니다. 만약 해당 시간 내에 세션 락을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

<!-- If neither of these arguments is passed, the lock will be obtained for a maximum of 10 seconds and requests will wait a maximum of 10 seconds while attempting to obtain a lock: -->
이 두 인수를 모두 생략하면, 기본으로 락은 최대 10초 동안 유지되고, 요청은 락 획득을 위해 최대 10초까지 대기합니다.

```
Route::post('/profile', function () {
    // ...
})->block()
```

<a name="adding-custom-session-drivers"></a>
<!-- ## Adding Custom Session Drivers -->
## Adding Custom Session Drivers

<a name="implementing-the-driver"></a>
<!-- ### Implementing the Driver -->
### Implementing the Driver

<!-- If none of the existing session drivers fit your application's needs, Laravel makes it possible to write your own session handler. Your custom session driver should implement PHP's built-in `SessionHandlerInterface`. This interface contains just a few simple methods. A stubbed MongoDB implementation looks like the following: -->
기존의 세션 드라이버가 애플리케이션의 요구에 맞지 않는다면, 직접 세션 핸들러를 작성할 수도 있습니다. 사용자 정의 세션 드라이버는 PHP 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드로 이루어져 있습니다. 아래는 MongoDB에 적용한 예제 기본 구조입니다.

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

> [!NOTE]
> Laravel은 커스텀 확장 기능을 위한 폴더를 따로 제공하지 않습니다. 예제에서는 `Extensions` 디렉터리를 생성하여 `MongoSessionHandler`를 보관하고 있습니다. 이처럼, 자유롭게 원하는 경로에 파일을 생성하면 됩니다.

<!-- Since the purpose of these methods is not readily understandable, let's quickly cover what each of the methods do: -->
각 메서드의 역할이 직관적으로 와닿지 않을 수 있으니, 간단히 설명하겠습니다.

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
- `open` 메서드는 주로 파일 기반 세션 저장소에서 사용됩니다. Laravel이 이미 `file` 세션 드라이버를 제공하기 때문에, 대부분의 경우 이 부분은 비워도 무방합니다.
- `close` 메서드는 `open`과 비슷하게 대개 무시할 수 있습니다. 대부분의 드라이버에서 코드 작성이 필요하지 않습니다.
- `read` 메서드는 주어진 `$sessionId`와 연결된 세션 데이터를 문자열 형태로 반환해야 합니다. 데이터 직렬화 등 부가적인 처리는 할 필요가 없습니다. Laravel이 알아서 처리해줍니다.
- `write` 메서드는 `$sessionId`와 연결된 `$data` 문자열을 MongoDB나 다른 영구 저장소에 기록해야 합니다. 여기서도 별도의 직렬화 처리는 필요 없습니다. 이미 Laravel이 처리합니다.
- `destroy` 메서드는 주어진 `$sessionId`와 연관된 데이터를 영구 저장소에서 제거해야 합니다.
- `gc`(garbage collection) 메서드는 주어진 `$lifetime` UNIX 타임스탬프보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached나 Redis처럼 자동으로 만료되는 시스템의 경우, 이 메서드는 비워둬도 괜찮습니다.

<!-- </div> -->
</div>

<a name="registering-the-driver"></a>
<!-- ### Registering the Driver -->
### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Laravel's session backend, you may use the `extend` method provided by the `Session` [facade](/docs/10.x/facades). You should call the `extend` method from the `boot` method of a [service provider](/docs/10.x/providers). You may do this from the existing `App\Providers\AppServiceProvider` or create an entirely new provider: -->
드라이버를 구현했다면, 이제 Laravel에 해당 드라이버를 등록할 차례입니다. Laravel의 세션 백엔드에 드라이버를 추가할 때는, `Session` [facade](/docs/10.x/facades)가 제공하는 `extend` 메서드를 사용합니다. `extend` 메서드는 [service provider](/docs/10.x/providers)의 `boot` 메서드 안에서 호출하는 것이 좋습니다. 기본적으로 제공되는 `App\Providers\AppServiceProvider`에서 작성해도 되고, 완전히 새로운 프로바이더를 만들어도 무방합니다.

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

<!-- Once the session driver has been registered, you may use the `mongo` driver in your `config/session.php` configuration file. -->
드라이버를 등록한 이후에는, `config/session.php` 설정 파일에서 `mongo` 드라이버를 사용할 수 있습니다.
