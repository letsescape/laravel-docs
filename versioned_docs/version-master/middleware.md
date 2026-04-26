# Middleware (Middleware)

- [소개](#introduction)
- [Middleware 정의하기](#defining-middleware)
- [Middleware 등록하기](#registering-middleware)
    - [전역 Middleware](#global-middleware)
    - [라우트에 Middleware 할당하기](#assigning-middleware-to-routes)
    - [Middleware 그룹](#middleware-groups)
    - [Middleware 별칭](#middleware-aliases)
    - [Middleware 정렬하기](#sorting-middleware)
- [Middleware 매개변수](#middleware-parameters)
- [종료 가능한 Middleware](#terminable-middleware)

<a name="introduction"></a>
## 소개 (Introduction)

Middleware는 애플리케이션으로 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 애플리케이션 사용자가 인증되었는지 확인하는 Middleware가 포함되어 있습니다. 사용자가 인증되지 않았다면 Middleware는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반대로 사용자가 인증되었다면 Middleware는 요청이 애플리케이션 안쪽으로 계속 진행되도록 허용합니다.

인증 외에도 다양한 작업을 수행하는 Middleware를 추가로 작성할 수 있습니다. 예를 들어, 로깅 Middleware는 애플리케이션으로 들어오는 모든 요청을 로그로 남길 수 있습니다. Laravel에는 인증 및 CSRF 보호를 위한 Middleware를 포함하여 다양한 Middleware가 포함되어 있습니다. 다만 사용자가 직접 정의한 Middleware는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## Middleware 정의하기 (Defining Middleware)

새 Middleware를 생성하려면 `make:middleware` Artisan 명령어를 사용합니다.

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 애플리케이션의 `app/Http/Middleware` 디렉터리 안에 새 `EnsureTokenIsValid` 클래스를 생성합니다. 이 Middleware에서는 전달된 `token` 입력값이 지정한 값과 일치하는 경우에만 라우트 접근을 허용합니다. 일치하지 않으면 사용자를 `/home` URI로 다시 리디렉션합니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('/home');
        }

        return $next($request);
    }
}
```

보시는 것처럼 주어진 `token`이 비밀 토큰과 일치하지 않으면 Middleware는 클라이언트에 HTTP 리디렉션을 반환합니다. 그렇지 않으면 요청은 애플리케이션 안쪽으로 더 전달됩니다. 요청을 애플리케이션 내부로 더 깊이 전달하려면, 즉 Middleware를 "통과"시키려면 `$request`와 함께 `$next` 콜백을 호출해야 합니다.

Middleware는 HTTP 요청이 애플리케이션에 도달하기 전에 반드시 통과해야 하는 일련의 "계층"으로 생각하는 것이 좋습니다. 각 계층은 요청을 검사할 수 있으며, 요청을 완전히 거부할 수도 있습니다.

> [!NOTE]
> 모든 Middleware는 [서비스 컨테이너](/docs/master/container)를 통해 해결되므로, Middleware의 생성자에서 필요한 의존성을 타입 힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
#### Middleware와 응답

물론 Middleware는 요청을 애플리케이션 안쪽으로 전달하기 전이나 후에 작업을 수행할 수 있습니다. 예를 들어, 다음 Middleware는 요청이 애플리케이션에 의해 처리되기 **전에** 어떤 작업을 수행합니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class BeforeMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Perform action

        return $next($request);
    }
}
```

반면, 다음 Middleware는 요청이 애플리케이션에 의해 처리된 **후에** 작업을 수행합니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AfterMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Perform action

        return $response;
    }
}
```

<a name="registering-middleware"></a>
## Middleware 등록하기 (Registering Middleware)

<a name="global-middleware"></a>
### 전역 Middleware

애플리케이션의 모든 HTTP 요청마다 Middleware를 실행하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 전역 Middleware 스택에 해당 Middleware를 추가할 수 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 제공되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션 라우트에 할당된 Middleware를 관리하는 역할을 합니다. `append` 메서드는 Middleware를 전역 Middleware 목록의 끝에 추가합니다. Middleware를 목록의 앞에 추가하고 싶다면 `prepend` 메서드를 사용해야 합니다.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel의 기본 전역 Middleware 수동 관리

Laravel의 전역 Middleware 스택을 직접 관리하고 싶다면, Laravel의 기본 전역 Middleware 스택을 `use` 메서드에 제공할 수 있습니다. 그런 다음 필요에 따라 기본 Middleware 스택을 조정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->use([
        \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class,
        // \Illuminate\Http\Middleware\TrustHosts::class,
        \Illuminate\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Http\Middleware\ValidatePostSize::class,
        \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ]);
})
```

<a name="assigning-middleware-to-routes"></a>
### 라우트에 Middleware 할당하기

특정 라우트에 Middleware를 할당하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

`middleware` 메서드에 Middleware 이름 배열을 전달하여 하나의 라우트에 여러 Middleware를 할당할 수 있습니다.

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### Middleware 제외하기

라우트 그룹에 Middleware를 할당할 때, 그룹 안의 개별 라우트에는 해당 Middleware가 적용되지 않도록 해야 할 때가 있습니다. 이때는 `withoutMiddleware` 메서드를 사용하면 됩니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        // ...
    });

    Route::get('/profile', function () {
        // ...
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```

특정 Middleware 집합을 전체 라우트 정의 [그룹](/docs/master/routing#route-groups)에서 제외할 수도 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` 메서드는 라우트 Middleware만 제거할 수 있으며, [전역 Middleware](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### Middleware 그룹

여러 Middleware를 하나의 키 아래에 그룹화하여 라우트에 더 쉽게 할당하고 싶을 때가 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `appendToGroup` 메서드를 사용하면 됩니다.

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->appendToGroup('group-name', [
        First::class,
        Second::class,
    ]);

    $middleware->prependToGroup('group-name', [
        First::class,
        Second::class,
    ]);
})
```

Middleware 그룹은 개별 Middleware와 동일한 문법을 사용하여 라우트와 컨트롤러 액션에 할당할 수 있습니다.

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### Laravel의 기본 Middleware 그룹

Laravel에는 웹 라우트와 API 라우트에 적용할 수 있는 일반적인 Middleware가 포함된 미리 정의된 `web` 및 `api` Middleware 그룹이 있습니다. Laravel은 이 Middleware 그룹을 해당 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용한다는 점을 기억하세요.

<div class="overflow-auto">

| `web` Middleware 그룹                                   |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` Middleware 그룹                            |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이 그룹에 Middleware를 추가하거나 앞에 삽입하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 사용할 수 있습니다. `web` 및 `api` 메서드는 `appendToGroup` 메서드를 대신해 편리하게 사용할 수 있는 방법입니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

Laravel의 기본 Middleware 그룹 항목 중 하나를 직접 만든 사용자 정의 Middleware로 교체할 수도 있습니다.

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는 Middleware를 완전히 제거할 수도 있습니다.

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel의 기본 Middleware 그룹 수동 관리

Laravel의 기본 `web` 및 `api` Middleware 그룹 안에 있는 모든 Middleware를 직접 관리하고 싶다면, 그룹 전체를 다시 정의할 수 있습니다. 아래 예제는 `web` 및 `api` Middleware 그룹을 기본 Middleware로 정의하면서, 필요에 따라 사용자 정의할 수 있도록 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
    ]);

    $middleware->group('api', [
        // \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        // 'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ]);
})
```

> [!NOTE]
> 기본적으로 `web` 및 `api` Middleware 그룹은 `bootstrap/app.php` 파일에 의해 애플리케이션의 해당 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### Middleware 별칭

애플리케이션의 `bootstrap/app.php` 파일에서 Middleware에 별칭을 할당할 수 있습니다. Middleware 별칭을 사용하면 특정 Middleware 클래스에 짧은 별칭을 정의할 수 있으며, 클래스명이 긴 Middleware에 특히 유용합니다.

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

애플리케이션의 `bootstrap/app.php` 파일에서 Middleware 별칭을 정의한 후에는, 라우트에 Middleware를 할당할 때 해당 별칭을 사용할 수 있습니다.

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

편의를 위해 Laravel에 내장된 일부 Middleware에는 기본적으로 별칭이 지정되어 있습니다. 예를 들어 `auth` Middleware는 `Illuminate\Auth\Middleware\Authenticate` Middleware의 별칭입니다. 다음은 기본 Middleware 별칭 목록입니다.

<div class="overflow-auto">

| 별칭               | Middleware                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------- |
| `auth`             | `Illuminate\Auth\Middleware\Authenticate`                                                                     |
| `auth.basic`       | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                        |
| `auth.session`     | `Illuminate\Session\Middleware\AuthenticateSession`                                                           |
| `cache.headers`    | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                  |
| `can`              | `Illuminate\Auth\Middleware\Authorize`                                                                        |
| `guest`            | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                          |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword`                                                                  |
| `precognitive`     | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                            |
| `signed`           | `Illuminate\Routing\Middleware\ValidateSignature`                                                             |
| `subscribed`       | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                           |
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                            |

</div>

<a name="sorting-middleware"></a>
### Middleware 정렬하기

드물게 Middleware가 특정 순서로 실행되어야 하지만, 라우트에 할당될 때 그 순서를 제어할 수 없는 경우가 있습니다. 이런 상황에서는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용해 Middleware 우선순위를 지정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ]);
})
```

<a name="middleware-parameters"></a>
## Middleware 매개변수 (Middleware Parameters)
Middleware는 추가 매개변수도 받을 수 있습니다. 예를 들어 애플리케이션에서 특정 작업을 수행하기 전에 인증된 사용자가 지정된 role(역할)을 가지고 있는지 확인해야 한다면, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` Middleware를 만들 수 있습니다.

추가 Middleware 매개변수는 `$next` 인수 뒤에 Middleware로 전달됩니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // Redirect...
        }

        return $next($request);
    }
}
```

Middleware 매개변수는 라우트를 정의할 때 Middleware 이름과 매개변수를 `:`로 구분하여 지정할 수 있습니다.

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

여러 매개변수는 쉼표로 구분할 수 있습니다.

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능 Middleware (Terminable Middleware)

때로는 Middleware가 HTTP 응답이 브라우저로 전송된 후에 일부 작업을 수행해야 할 수 있습니다. Middleware에 `terminate` 메서드를 정의하고 웹 서버가 [FastCGI](https://www.php.net/manual/en/install.fpm.php)를 사용하고 있다면, 응답이 브라우저로 전송된 뒤 `terminate` 메서드가 자동으로 호출됩니다.

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```

`terminate` 메서드는 요청과 응답을 모두 받아야 합니다. 종료 가능 Middleware를 정의한 후에는 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 목록이나 전역 Middleware 목록에 추가해야 합니다.

Middleware의 `terminate` 메서드를 호출할 때 Laravel은 [서비스 컨테이너](/docs/master/container)에서 Middleware의 새 인스턴스를 해결합니다. `handle` 메서드와 `terminate` 메서드가 호출될 때 동일한 Middleware 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 사용하여 Middleware를 컨테이너에 등록하십시오. 일반적으로 이 작업은 `AppServiceProvider`의 `register` 메서드에서 수행해야 합니다.

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```
