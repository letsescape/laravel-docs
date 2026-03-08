# 미들웨어 (Middleware)

- [소개](#introduction)
- [미들웨어 정의하기](#defining-middleware)
- [미들웨어 등록하기](#registering-middleware)
    - [글로벌 미들웨어](#global-middleware)
    - [라우트에 미들웨어 할당하기](#assigning-middleware-to-routes)
    - [미들웨어 그룹](#middleware-groups)
    - [미들웨어 별칭](#middleware-aliases)
    - [미들웨어 정렬](#sorting-middleware)
- [미들웨어 파라미터](#middleware-parameters)
- [종료 가능한 미들웨어](#terminable-middleware)

<a name="introduction"></a>
## 소개 (Introduction)

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 기본적으로 포함되어 있습니다. 사용자가 인증되지 않은 경우, 해당 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리다이렉트합니다. 반면, 인증된 사용자의 경우 요청이 애플리케이션 내부로 더 진행될 수 있도록 허용합니다.

인증 외에도 다양한 작업을 수행하는 미들웨어를 별도로 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션으로 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증, CSRF 보호 등 다양한 미들웨어가 기본 제공되며, 사용자가 직접 작성한 미들웨어는 보통 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
## 미들웨어 정의하기 (Defining Middleware)

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령어를 사용합니다:

```shell
php artisan make:middleware EnsureTokenIsValid
```

이 명령어는 새로운 `EnsureTokenIsValid` 클래스를 `app/Http/Middleware` 디렉터리에 생성합니다. 이 미들웨어에서는, 전달받은 `token` 입력값이 특정 값과 일치하는 경우에만 라우트 접근을 허용합니다. 일치하지 않으면 사용자를 `/home` URI로 리다이렉트합니다:

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

위 예시에서처럼, 주어진 `token`이 비밀 토큰과 일치하지 않으면 미들웨어가 클라이언트에 HTTP 리다이렉트를 반환합니다. 반면, 일치한다면 요청이 애플리케이션 더 안쪽으로 전달됩니다. 요청을 더 깊이 전달하려면(즉, 미들웨어를 "통과"시키려면) `$next` 콜백에 `$request`를 전달해야 합니다.

미들웨어는 애플리케이션에 도달하기 전에 HTTP 요청이 여러 "레이어"를 통과하는 것으로 상상하면 이해하기 쉽습니다. 각 레이어에서 요청을 검사하거나 아예 요청을 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 미들웨어 생성자의 의존성 타입힌트가 가능합니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론, 미들웨어는 요청이 애플리케이션에 전달되기 전이나 후에도 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에서 처리되기 **전**에 작업을 수행하게 됩니다:

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

반면에, 아래 미들웨어는 요청이 애플리케이션에서 처리된 **후**에 작업을 수행합니다:

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
## 미들웨어 등록하기 (Registering Middleware)

<a name="global-middleware"></a>
### 글로벌 미들웨어 (Global Middleware)

애플리케이션의 모든 HTTP 요청에서 특정 미들웨어가 항상 실행되도록 하려면, `bootstrap/app.php` 파일의 글로벌 미들웨어 스택에 추가하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` 클로저에 전달된 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션 라우트에 할당된 미들웨어를 관리합니다. `append` 메서드는 글로벌 미들웨어 리스트의 맨 끝에 미들웨어를 추가합니다. 맨 앞에 추가하고 싶다면 `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel 기본 글로벌 미들웨어 직접 관리하기

글로벌 미들웨어 스택을 직접 관리하고 싶다면, Laravel의 기본 글로벌 미들웨어 스택을 `use` 메서드에 직접 제공할 수 있습니다. 필요한 경우 기본 스택을 수정하세요:

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
### 라우트에 미들웨어 할당하기 (Assigning Middleware to Routes)

특정 라우트에만 미들웨어를 할당하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 사용하면 됩니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

여러 개의 미들웨어를 할당할 수도 있으며, 이 경우 미들웨어 이름의 배열을 전달합니다:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### 미들웨어 제외하기

라우트 그룹에 미들웨어를 할당할 때, 그룹 내의 특정 라우트에서 해당 미들웨어를 적용하지 않으려면 `withoutMiddleware` 메서드를 사용할 수 있습니다:

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

[그룹](/docs/master/routing#route-groups) 전체에서 특정 미들웨어를 제외시킬 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹 (Middleware Groups)

여러 미들웨어를 하나의 키로 묶어두면 라우트에 할당할 때 더 편리합니다. 이를 위해 `bootstrap/app.php` 파일에서 `appendToGroup` 메서드를 사용할 수 있습니다:

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

미들웨어 그룹은 개별 미들웨어와 동일한 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```

<a name="laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹

Laravel에는 웹 라우트와 API 라우트에 적용할 일반적인 미들웨어가 포함된 `web`, `api` 그룹이 미리 정의되어 있습니다. Laravel은 이 두 미들웨어 그룹을 각 파일에 자동으로 적용합니다(`routes/web.php`, `routes/api.php`):

<div class="overflow-auto">

| `web` 미들웨어 그룹                                   |
| ---------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹                        |
| ------------------------------------------ |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이러한 그룹에 미들웨어를 추가(append)하거나 앞에 추가(prepend)하려면, `bootstrap/app.php` 파일에서 `web`, `api` 메서드를 사용할 수 있습니다. 이 메서드는 `appendToGroup`의 편의 메서드입니다:

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

Laravel의 기본 미들웨어 그룹 항목 중 하나를 직접 만든 사용자 미들웨어로 교체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

또는 미들웨어를 아예 삭제할 수도 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel 기본 미들웨어 그룹 직접 관리하기

Laravel의 기본 `web`, `api` 그룹 내 모든 미들웨어를 직접 관리하고 싶다면, 그룹 전체를 다시 정의할 수 있습니다. 아래 예시는 기본 미들웨어로 `web`과 `api` 그룹을 다시 정의하며, 필요하다면 자유롭게 수정해 사용할 수 있습니다:

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
> 기본적으로, `web`과 `api` 미들웨어 그룹은 애플리케이션의 각 `routes/web.php`, `routes/api.php` 파일에 `bootstrap/app.php`에서 자동 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭 (Middleware Aliases)

`bootstrap/app.php` 파일에서 미들웨어에 별칭(alias)을 지정할 수 있습니다. 별칭을 이용하면, 주로 긴 클래스명을 가진 미들웨어를 라우트에 단축된 이름으로 할당할 수 있어 더 간편합니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

별칭이 등록된 후에는 라우트에 미들웨어를 할당할 때 별칭으로 사용하면 됩니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

편의를 위해, Laravel에서 기본 제공하는 일부 미들웨어는 이미 별칭이 지정되어 있습니다. 예를 들어, `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 클래스에 대한 별칭입니다. 아래는 기본 미들웨어 별칭 목록입니다:

<div class="overflow-auto">

| 별칭                  | 미들웨어                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `auth`                | `Illuminate\Auth\Middleware\Authenticate`                                                                         |
| `auth.basic`          | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`                                                            |
| `auth.session`        | `Illuminate\Session\Middleware\AuthenticateSession`                                                               |
| `cache.headers`       | `Illuminate\Http\Middleware\SetCacheHeaders`                                                                      |
| `can`                 | `Illuminate\Auth\Middleware\Authorize`                                                                            |
| `guest`               | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`                                                              |
| `password.confirm`    | `Illuminate\Auth\Middleware\RequirePassword`                                                                      |
| `precognitive`        | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`                                                |
| `signed`              | `Illuminate\Routing\Middleware\ValidateSignature`                                                                 |
| `subscribed`          | `\Spark\Http\Middleware\VerifyBillableIsSubscribed`                                                               |
| `throttle`            | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis`    |
| `verified`            | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                                |

</div>

<a name="sorting-middleware"></a>
### 미들웨어 정렬 (Sorting Middleware)

드물지만, 미들웨어의 실행 순서가 중요할 수 있으나 라우트에 할당할 때 그 순서를 직접 제어할 수 없는 경우가 있을 수 있습니다. 이럴 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용하여 미들웨어 실행 우선순위를 지정할 수 있습니다:

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
## 미들웨어 파라미터 (Middleware Parameters)

미들웨어는 추가적인 파라미터를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가져야지만 어떤 동작을 허용해야 한다면, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

이런 추가적인 미들웨어 파라미터는 `$next` 인수 다음에 전달됩니다:

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

미들웨어에 파라미터를 지정할 때는, 미들웨어 이름 뒤에 `:`로 구분해 입력합니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

파라미터가 여러 개라면 쉼표로 구분해서 전달할 수 있습니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어 (Terminable Middleware)

간혹 미들웨어가 HTTP 응답이 브라우저에 전송된 **후에도** 추가 작업을 해야 할 수 있습니다. 미들웨어에 `terminate` 메서드를 정의하고, 웹 서버로 [FastCGI](https://www.php.net/manual/en/install.fpm.php)를 사용하고 있다면, 응답이 브라우저로 전송된 후 `terminate` 메서드가 자동으로 호출됩니다:

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

`terminate` 메서드는 요청과 응답 두 개의 파라미터를 전달받아야 합니다. 종료 가능한 미들웨어를 정의했다면, 해당 미들웨어를 반드시 라우트 또는 글로벌 미들웨어 리스트에 등록해야 합니다(`bootstrap/app.php`).

미들웨어의 `terminate` 메서드를 호출할 때, Laravel은 [서비스 컨테이너](/docs/master/container)에서 미들웨어 인스턴스를 새롭게 해석합니다. 만약 `handle`과 `terminate` 메서드 호출 시 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 이용해 미들웨어를 등록해야 합니다. 일반적으로는 `AppServiceProvider`의 `register` 메서드에서 아래와 같이 처리합니다:

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
