# HTTP 세션 (HTTP Session)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
- [세션과 상호작용하기](#interacting-with-the-session)
    - [데이터 조회](#retrieving-data)
    - [데이터 저장](#storing-data)
    - [플래시 데이터](#flash-data)
    - [데이터 삭제](#deleting-data)
    - [세션 ID 재생성](#regenerating-the-session-id)
- [세션 캐시](#session-cache)
- [세션 블로킹](#session-blocking)
- [커스텀 세션 드라이버 추가하기](#adding-custom-session-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개 (Introduction)

HTTP 기반 애플리케이션은 상태를 저장하지 않기 때문에, 세션은 여러 요청에 걸쳐 사용자 정보를 저장할 수 있는 방법을 제공합니다. 그러한 사용자 정보는 일반적으로 다음 요청에서도 접근할 수 있도록 영속적인 저장소나 백엔드에 저장됩니다.

Laravel은 다양한 세션 백엔드를 갖추고 있으며, 이를 표현적이고 통합된 API로 다룰 수 있습니다. [Memcached](https://memcached.org), [Redis](https://redis.io), 데이터베이스 등 인기 있는 백엔드가 기본 지원됩니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 세션 구성 파일은 `config/session.php` 경로에 저장되어 있습니다. 이 파일 내의 다양한 옵션을 반드시 검토하시기 바랍니다. Laravel은 기본적으로 `database` 세션 드라이버를 사용하도록 설정되어 있습니다.

세션의 `driver` 설정 옵션은 각 요청의 세션 데이터가 어디에 저장될지 정의합니다. Laravel에서 사용할 수 있는 드라이버는 다음과 같습니다:

<div class="content-list" markdown="1">

- `file` - 세션은 `storage/framework/sessions`에 저장됩니다.
- `cookie` - 세션은 보안 암호화된 쿠키에 저장됩니다.
- `database` - 세션은 관계형 데이터베이스에 저장됩니다.
- `memcached` / `redis` - 세션은 빠르고 캐시 기반의 저장소인 이들 중 하나에 저장됩니다.
- `dynamodb` - 세션은 AWS DynamoDB에 저장됩니다.
- `array` - 세션은 PHP 배열에 저장되며, 영속적으로 저장되지 않습니다.

</div>

> [!NOTE]
> `array` 드라이버는 주로 [테스트 시](/docs/master/testing) 사용되며, 세션에 저장된 데이터가 실제로 저장되지 않도록 방지합니다.

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 세션 드라이버를 사용할 때는, 세션 데이터를 저장할 데이터베이스 테이블이 필요합니다. 보통, 이는 Laravel 기본의 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 그러나 `sessions` 테이블이 없다면, `make:session-table` Artisan 명령어를 사용해 마이그레이션 파일을 생성하고 데이터베이스에 테이블을 만들 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장 기능을 설치하거나 Composer를 통해 `predis/predis` 패키지(~1.0)를 설치해야 합니다. Redis 설정에 대한 더 자세한 내용은 Laravel의 [Redis 문서](/docs/master/redis#configuration)를 참고하세요.

> [!NOTE]
> `SESSION_CONNECTION` 환경 변수 또는 `session.php` 설정 파일의 `connection` 옵션을 사용해 세션 저장에 사용할 Redis 연결을 지정할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션과 상호작용하기 (Interacting With the Session)

<a name="retrieving-data"></a>
### 데이터 조회 (Retrieving Data)

Laravel에서 세션 데이터를 다루는 주요 방법은 두 가지입니다. 전역 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 먼저, `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이 인스턴스는 라우트 클로저나 컨트롤러 메서드에서 타입힌트로 주입받을 수 있습니다. 참고로, 컨트롤러 메서드의 의존성은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 자동으로 주입됩니다.

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

세션에서 항목을 조회할 때, `get` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 지정한 키가 세션에 없을 경우 이 기본값이 반환됩니다. 또한, 기본값으로 클로저를 전달하면, 키가 존재하지 않을 때 이 클로저가 실행되어 그 결과가 반환됩니다.

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});
```

<a name="the-global-session-helper"></a>
#### 전역 세션 헬퍼 (The Global Session Helper)

전역 `session` PHP 함수를 사용하여 세션에 데이터를 저장하거나 조회할 수 있습니다. 이 헬퍼를 문자열 인수 하나로 호출하면 해당 세션 키의 값을 반환합니다. 배열 형태의 키/값 쌍으로 호출하면 해당 값들을 세션에 저장합니다:

```php
Route::get('/home', function () {
    // 세션에서 데이터 조회...
    $value = session('key');

    // 기본값 지정...
    $value = session('key', 'default');

    // 세션에 데이터 저장...
    session(['key' => 'value']);
});
```

> [!NOTE]
> HTTP 요청 인스턴스를 통한 세션 접근과 전역 `session` 헬퍼를 사용하는 것 사이에는 실질적인 차이가 거의 없습니다. 이 두 방법 모두 테스트 코드에서 사용할 수 있으며, 모든 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 활용해 [테스트할 수 있습니다](/docs/master/testing).

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 조회

세션의 전체 데이터를 조회하려면, `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();
```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 일부 세션 데이터만 조회

`only` 및 `except` 메서드를 이용해 세션 데이터의 일부만 가져올 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);
```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목 존재 여부 확인

세션에 항목이 있는지 확인하려면, `has` 메서드를 사용할 수 있습니다. 이 메서드는 해당 값이 `null`이 아니고 존재할 때 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}
```

값이 `null`일지라도 키가 세션에 존재하는지 확인하려면 `exists` 메서드를 사용합니다:

```php
if ($request->session()->exists('users')) {
    // ...
}
```

세션에 해당 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. 이 메서드는 해당 항목이 없을 때 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}
```

<a name="storing-data"></a>
### 데이터 저장 (Storing Data)

세션에 데이터를 저장하려면, 보통 Request 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// Request 인스턴스를 통해 저장...
$request->session()->put('key', 'value');

// 전역 "session" 헬퍼를 통해 저장...
session(['key' => 'value']);
```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 데이터 추가

배열 타입의 세션 값에 새 값을 추가하려면 `push` 메서드를 사용할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름의 배열이 있다면 다음과 같이 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');
```

<a name="retrieving-deleting-an-item"></a>
#### 항목 조회와 동시에 삭제

`pull` 메서드를 사용하면 세션에서 항목을 조회한 뒤 한 번에 삭제할 수 있습니다:

```php
$value = $request->session()->pull('key', 'default');
```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가/감소시키기

세션 데이터에 정수가 저장되어 있다면, `increment`와 `decrement` 메서드로 값을 증가시키거나 감소시킬 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);
```

<a name="flash-data"></a>
### 플래시 데이터 (Flash Data)

때로는 세션에 데이터를 저장하되, 다음 요청까지 잠깐만 유지하고 싶을 때가 있습니다. 이때는 `flash` 메서드를 사용할 수 있습니다. 이 메서드로 저장한 데이터는 바로 사용할 수 있으며, 다음 HTTP 요청까지 유지됩니다. 이후에는 이 플래시 데이터가 자동으로 삭제됩니다. 플래시 데이터는 짧게 유지되어도 되는 상태 메시지 등에 주로 사용됩니다:

```php
$request->session()->flash('status', 'Task was successful!');
```

플래시 데이터를 여러 요청 동안 유지하려면 `reflash` 메서드를 사용하면 됩니다. 필요한 플래시 데이터만 유지하려면 `keep` 메서드를 이용할 수 있습니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);
```

현재 요청에서만 플래시 데이터를 유지하려면 `now` 메서드를 사용할 수 있습니다:

```php
$request->session()->now('status', 'Task was successful!');
```

<a name="deleting-data"></a>
### 데이터 삭제 (Deleting Data)

`forget` 메서드는 세션에서 특정 데이터를 제거합니다. 모든 세션 데이터를 삭제하려면 `flush` 메서드를 사용할 수 있습니다:

```php
// 단일 키 삭제...
$request->session()->forget('name');

// 여러 키 삭제...
$request->session()->forget(['name', 'status']);

$request->session()->flush();
```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성 (Regenerating the Session ID)

세션 ID 재생성은 악의적인 사용자가 여러분의 애플리케이션에서 [세션 고정(session fixation)](https://owasp.org/www-community/attacks/Session_fixation) 공격을 시도하는 것을 방지하기 위해 자주 사용됩니다.

Laravel에서 [애플리케이션 스타터 키트](/docs/master/starter-kits) 또는 [Laravel Fortify](/docs/master/fortify)를 사용하는 경우, 인증 과정에서 세션 ID가 자동으로 재생성됩니다. 하지만 직접 수동으로 세션 ID를 재생성하려면 `regenerate` 메서드를 사용할 수 있습니다:

```php
$request->session()->regenerate();
```

세션 ID를 재생성하면서 모든 세션 데이터도 한 번에 삭제하려면 `invalidate` 메서드를 사용합니다:

```php
$request->session()->invalidate();
```

<a name="session-cache"></a>
## 세션 캐시 (Session Cache)

Laravel의 세션 캐시는 개별 사용자 세션 범위에서 데이터를 쉽게 캐시할 수 있는 방법을 제공합니다. 전역 애플리케이션 캐시와 달리, 세션 캐시 데이터는 각 세션마다 자동으로 분리되어 관리되며, 해당 세션이 만료되거나 삭제될 때 함께 정리됩니다. 세션 캐시는 [Laravel 캐시 메서드](/docs/master/cache)에서 자주 쓰이는 `get`, `put`, `remember`, `forget` 등을 동일하게 사용할 수 있지만, 현재 세션 범위에만 적용됩니다.

세션 캐시는 여러 요청 사이에 임시로 사용자별 데이터를 저장하고자 할 때 적합합니다. 예를 들어, 폼 데이터, 임시 계산 결과, API 응답 등과 같이 오랫동안 저장할 필요는 없지만 특정 사용자 세션에 묶어 저장하고 싶을 때 사용할 수 있습니다.

세션의 `cache` 메서드를 통해 세션 캐시에 접근할 수 있습니다:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);
```

Laravel의 캐시 메서드에 대한 더 자세한 내용은 [캐시 문서](/docs/master/cache)를 참고하세요.

<a name="session-blocking"></a>
## 세션 블로킹 (Session Blocking)

> [!WARNING]
> 세션 블로킹을 활용하려면, 여러분의 애플리케이션이 [원자적 락(atomic locks)](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버를 사용해야 합니다. 현재 지원되는 드라이버는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지 포함), `database`, `file`, `array` 드라이버입니다. 또한, `cookie` 세션 드라이버는 사용할 수 없습니다.

Laravel은 기본적으로 동일한 세션을 사용하는 요청들이 동시에 실행될 수 있습니다. 예를 들어, 자바스크립트 HTTP 라이브러리를 사용해 두 개의 HTTP 요청을 동시에 보낸다면, 이 요청들은 동시에 처리됩니다. 대부분의 애플리케이션에는 문제가 없지만, 두 개 이상의 엔드포인트가 동시에 같은 세션에 데이터를 기록하면 일부 애플리케이션에서는 세션 데이터 손실이 발생할 수 있습니다.

이를 방지하기 위해, Laravel에서는 특정 세션에 대해 동시 요청을 제한하는 기능을 제공합니다. 사용 방법은 간단하게 라우트 정의에 `block` 메서드를 체이닝하면 됩니다. 아래의 예시에서는 `/profile` 엔드포인트로 들어오는 요청이 세션 락을 획득하게 됩니다. 락이 유지되는 동안 동일한 세션 ID를 공유하는 `/profile` 또는 `/order` 엔드포인트로 들어오는 다른 요청들은 첫 번째 요청이 끝날 때까지 대기하게 됩니다.

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);
```

`block` 메서드는 두 개의 선택적 인수를 받습니다. 첫 번째 인수는 세션 락을 최대 몇 초간 유지할지 지정합니다. 요청이 더 빨리 끝나면 락이 더 일찍 해제됩니다.

두 번째 인수는 요청이 세션 락을 얻기 위해 최대 몇 초간 대기할지 지정합니다. 만약 정해진 시간 내에 락을 얻지 못하면, `Illuminate\Contracts\Cache\LockTimeoutException` 예외가 발생합니다.

인수를 모두 생략하면 락이 최대 10초간 유지되며, 락을 얻기 위해 최대 10초간 대기하게 됩니다:

```php
Route::post('/profile', function () {
    // ...
})->block();
```

<a name="adding-custom-session-drivers"></a>
## 커스텀 세션 드라이버 추가하기 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
### 드라이버 구현 (Implementing the Driver)

기존 세션 드라이버가 애플리케이션의 니즈에 맞지 않는다면, Laravel에서는 직접 세션 핸들러를 구현할 수 있습니다. 커스텀 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드로 구성되어 있습니다. 예를 들어 MongoDB를 사용하는 기본 구조는 다음과 같습니다:

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

Laravel에는 확장 코드를 위한 기본 디렉터리가 포함되어 있지 않으므로, 여러분이 원하는 위치에 파일을 저장하면 됩니다. 위의 예시에서는 `Extensions` 디렉터리에 `MongoSessionHandler`를 생성하였습니다.

각 메서드의 용도가 바로 이해되지 않을 수 있으므로 아래에 간단히 설명합니다:

<div class="content-list" markdown="1">

- `open` 메서드는 파일 기반 세션 저장 시스템에서 주로 사용됩니다. Laravel은 기본적으로 `file` 세션 드라이버를 함께 제공하므로, 대부분의 경우 이 메서드는 비워두어도 무방합니다.
- `close` 메서드 역시 `open`과 마찬가지로 보통 무시해도 됩니다. 대부분의 드라이버에서 필요하지 않습니다.
- `read` 메서드는 주어진 `$sessionId`와 연관된 세션 데이터를 문자열 형태로 반환해야 합니다. 데이터의 직렬화나 인코딩은 직접 할 필요가 없습니다. Laravel이 알아서 처리해줍니다.
- `write` 메서드는 주어진 `$sessionId`에 해당하는 `$data` 문자열을 MongoDB 등 영속적인 저장소에 기록해야 합니다. 이때도 직렬화는 직접 할 필요 없습니다.
- `destroy` 메서드는 지정된 `$sessionId`와 연관된 세션 데이터를 영속 저장소에서 제거해야 합니다.
- `gc` 메서드는 주어진 `$lifetime`(UNIX 타임스탬프)보다 오래된 모든 세션 데이터를 삭제해야 합니다. Memcached, Redis와 같이 자동으로 데이터를 만료시키는 시스템의 경우 비워두어도 됩니다.

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록 (Registering the Driver)

드라이버를 구현했다면, 이제 Laravel에 해당 드라이버를 등록할 차례입니다. 추가 드라이버는 `Session` [파사드](/docs/master/facades)에서 제공하는 `extend` 메서드를 사용해 Laravel의 세션 백엔드에 등록할 수 있습니다. 이 메서드는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 호출해야 합니다. 기존의 `App\Providers\AppServiceProvider`에 추가할 수도 있고, 별도 프로바이더를 생성해도 됩니다:

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
            // SessionHandlerInterface 구현체를 반환...
            return new MongoSessionHandler;
        });
    }
}
```

세션 드라이버가 등록되면, `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 설정 파일에서 세션 드라이버로 `mongo`를 지정할 수 있습니다.
