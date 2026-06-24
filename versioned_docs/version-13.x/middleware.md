<!-- # Middleware -->
# Middleware

- [Introduction](#introduction)
- [Defining Middleware](#defining-middleware)
- [Registering Middleware](#registering-middleware)
    - [Global Middleware](#global-middleware)
    - [Assigning Middleware to Routes](#assigning-middleware-to-routes)
    - [Middleware Groups](#middleware-groups)
    - [Middleware Aliases](#middleware-aliases)
    - [Sorting Middleware](#sorting-middleware)
- [Middleware Parameters](#middleware-parameters)
- [Terminable Middleware](#terminable-middleware)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Middleware provide a convenient mechanism for inspecting and filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to your application's login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. -->
Middleware는 애플리케이션으로 들어오는 HTTP 요청을 검사하고 필터링할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 애플리케이션 사용자가 인증되었는지 확인하는 Middleware가 포함되어 있습니다. 사용자가 인증되지 않았다면 Middleware는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반대로 사용자가 인증되었다면 Middleware는 요청이 애플리케이션 안쪽으로 계속 진행되도록 허용합니다.

<!-- Additional middleware can be written to perform a variety of tasks besides authentication. For example, a logging middleware might log all incoming requests to your application. A variety of middleware are included in Laravel, including middleware for authentication and CSRF protection; however, all user-defined middleware are typically located in your application's `app/Http/Middleware` directory. -->
인증 외에도 다양한 작업을 수행하는 Middleware를 추가로 작성할 수 있습니다. 예를 들어, 로깅 Middleware는 애플리케이션으로 들어오는 모든 요청을 로그로 남길 수 있습니다. Laravel에는 인증 및 CSRF 보호를 위한 Middleware를 포함하여 다양한 Middleware가 포함되어 있습니다. 다만 사용자가 직접 정의한 Middleware는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
<!-- ## Defining Middleware -->
## Defining Middleware

<!-- To create a new middleware, use the `make:middleware` Artisan command: -->
새 Middleware를 생성하려면 `make:middleware` Artisan 명령어를 사용합니다.

```shell
php artisan make:middleware EnsureTokenIsValid
```

<!-- This command will place a new `EnsureTokenIsValid` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `token` input matches a specified value. Otherwise, we will redirect the users back to the `/home` URI: -->
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

<!-- As you can see, if the given `token` does not match our secret token, the middleware will return an HTTP redirect to the client; otherwise, the request will be passed further into the application. To pass the request deeper into the application (allowing the middleware to "pass"), you should call the `$next` callback with the `$request`. -->
보시는 것처럼 주어진 `token`이 비밀 토큰과 일치하지 않으면 Middleware는 클라이언트에 HTTP 리디렉션을 반환합니다. 그렇지 않으면 요청은 애플리케이션 안쪽으로 더 전달됩니다. 요청을 애플리케이션 내부로 더 깊이 전달하려면, 즉 Middleware를 "통과"시키려면 `$request`와 함께 `$next` 콜백을 호출해야 합니다.

<!-- It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely. -->
Middleware는 HTTP 요청이 애플리케이션에 도달하기 전에 반드시 통과해야 하는 일련의 "계층"으로 생각하는 것이 좋습니다. 각 계층은 요청을 검사할 수 있으며, 요청을 완전히 거부할 수도 있습니다.

> [!NOTE]
> 모든 Middleware는 [service container](/docs/13.x/container)를 통해 해결되므로, Middleware의 생성자에서 필요한 의존성을 타입 힌트할 수 있습니다.

<a name="middleware-and-responses"></a>
<!-- #### Middleware and Responses -->
#### Middleware and Responses

<!-- Of course, a middleware can perform tasks before or after passing the request deeper into the application. For example, the following middleware would perform some task **before** the request is handled by the application: -->
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

<!-- However, this middleware would perform its task **after** the request is handled by the application: -->
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
<!-- ## Registering Middleware -->
## Registering Middleware

<a name="global-middleware"></a>
<!-- ### Global Middleware -->
### Global Middleware

<!-- If you want a middleware to run during every HTTP request to your application, you may append it to the global middleware stack in your application's `bootstrap/app.php` file: -->
애플리케이션의 모든 HTTP 요청마다 Middleware를 실행하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 전역 Middleware 스택에 해당 Middleware를 추가할 수 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

<!-- The `$middleware` object provided to the `withMiddleware` closure is an instance of `Illuminate\Foundation\Configuration\Middleware` and is responsible for managing the middleware assigned to your application's routes. The `append` method adds the middleware to the end of the list of global middleware. If you would like to add a middleware to the beginning of the list, you should use the `prepend` method. -->
`withMiddleware` 클로저에 제공되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션 라우트에 할당된 Middleware를 관리하는 역할을 합니다. `append` 메서드는 Middleware를 전역 Middleware 목록의 끝에 추가합니다. Middleware를 목록의 앞에 추가하고 싶다면 `prepend` 메서드를 사용해야 합니다.

<a name="manually-managing-laravels-default-global-middleware"></a>
<!-- #### Manually Managing Laravel's Default Global Middleware -->
#### Manually Managing Laravel's Default Global Middleware

<!-- If you would like to manage Laravel's global middleware stack manually, you may provide Laravel's default stack of global middleware to the `use` method. Then, you may adjust the default middleware stack as necessary: -->
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
<!-- ### Assigning Middleware to Routes -->
### Assigning Middleware to Routes

<!-- If you would like to assign middleware to specific routes, you may invoke the `middleware` method when defining the route: -->
특정 라우트에 Middleware를 할당하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

<!-- You may assign multiple middleware to the route by passing an array of middleware names to the `middleware` method: -->
`middleware` 메서드에 Middleware 이름 배열을 전달하여 하나의 라우트에 여러 Middleware를 할당할 수 있습니다.

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
<!-- #### Excluding Middleware -->
#### Excluding Middleware

<!-- When assigning middleware to a group of routes, you may occasionally need to prevent the middleware from being applied to an individual route within the group. You may accomplish this using the `withoutMiddleware` method: -->
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

<!-- You may also exclude a given set of middleware from an entire [group](/docs/13.x/routing#route-groups) of route definitions: -->
특정 Middleware 집합을 전체 라우트 정의 [group](/docs/13.x/routing#route-groups)에서 제외할 수도 있습니다.

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

<!-- The `withoutMiddleware` method can only remove route middleware and does not apply to [global middleware](#global-middleware). -->
`withoutMiddleware` 메서드는 라우트 Middleware만 제거할 수 있으며, [global middleware](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
<!-- ### Middleware Groups -->
### Middleware Groups

<!-- Sometimes you may want to group several middleware under a single key to make them easier to assign to routes. You may accomplish this using the `appendToGroup` method within your application's `bootstrap/app.php` file: -->
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

<!-- Middleware groups may be assigned to routes and controller actions using the same syntax as individual middleware: -->
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
<!-- #### Laravel's Default Middleware Groups -->
#### Laravel's Default Middleware Groups

<!-- Laravel includes predefined `web` and `api` middleware groups that contain common middleware you may want to apply to your web and API routes. Remember, Laravel automatically applies these middleware groups to the corresponding `routes/web.php` and `routes/api.php` files: -->
Laravel에는 웹 라우트와 API 라우트에 적용할 수 있는 일반적인 Middleware가 포함된 미리 정의된 `web` 및 `api` Middleware 그룹이 있습니다. Laravel은 이 Middleware 그룹을 해당 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용한다는 점을 기억하세요.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `web` Middleware 그룹                                   |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

<!-- </div> -->
</div>

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `api` Middleware 그룹                            |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

<!-- </div> -->
</div>

<!-- If you would like to append or prepend middleware to these groups, you may use the `web` and `api` methods within your application's `bootstrap/app.php` file. The `web` and `api` methods are convenient alternatives to the `appendToGroup` method: -->
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

<!-- You may even replace one of Laravel's default middleware group entries with a custom middleware of your own: -->
Laravel의 기본 Middleware 그룹 항목 중 하나를 직접 만든 사용자 정의 Middleware로 교체할 수도 있습니다.

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

<!-- Or, you may remove a middleware entirely: -->
또는 Middleware를 완전히 제거할 수도 있습니다.

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
<!-- #### Manually Managing Laravel's Default Middleware Groups -->
#### Manually Managing Laravel's Default Middleware Groups

<!-- If you would like to manually manage all of the middleware within Laravel's default `web` and `api` middleware groups, you may redefine the groups entirely. The example below will define the `web` and `api` middleware groups with their default middleware, allowing you to customize them as necessary: -->
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
<!-- ### Middleware Aliases -->
### Middleware Aliases

<!-- You may assign aliases to middleware in your application's `bootstrap/app.php` file. Middleware aliases allow you to define a short alias for a given middleware class, which can be especially useful for middleware with long class names: -->
애플리케이션의 `bootstrap/app.php` 파일에서 Middleware에 별칭을 할당할 수 있습니다. Middleware 별칭을 사용하면 특정 Middleware 클래스에 짧은 별칭을 정의할 수 있으며, 클래스명이 긴 Middleware에 특히 유용합니다.

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

<!-- Once the middleware alias has been defined in your application's `bootstrap/app.php` file, you may use the alias when assigning the middleware to routes: -->
애플리케이션의 `bootstrap/app.php` 파일에서 Middleware 별칭을 정의한 후에는, 라우트에 Middleware를 할당할 때 해당 별칭을 사용할 수 있습니다.

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

<!-- For convenience, some of Laravel's built-in middleware are aliased by default. For example, the `auth` middleware is an alias for the `Illuminate\Auth\Middleware\Authenticate` middleware. Below is a list of the default middleware aliases: -->
편의를 위해 Laravel에 내장된 일부 Middleware에는 기본적으로 별칭이 지정되어 있습니다. 예를 들어 `auth` Middleware는 `Illuminate\Auth\Middleware\Authenticate` Middleware의 별칭입니다. 다음은 기본 Middleware 별칭 목록입니다.

<!-- <div class="overflow-auto"> -->
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

<!-- </div> -->
</div>

<a name="sorting-middleware"></a>
<!-- ### Sorting Middleware -->
### Sorting Middleware

<!-- Rarely, you may need your middleware to execute in a specific order but not have control over their order when they are assigned to the route. In these situations, you may specify your middleware priority using the `priority` method in your application's `bootstrap/app.php` file: -->
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
<!-- ## Middleware Parameters -->
## Middleware Parameters
<!-- Middleware can also receive additional parameters. For example, if your application needs to verify that the authenticated user has a given "role" before performing a given action, you could create an `EnsureUserHasRole` middleware that receives a role name as an additional argument. -->
Middleware는 추가 매개변수도 받을 수 있습니다. 예를 들어 애플리케이션에서 특정 작업을 수행하기 전에 인증된 사용자가 지정된 role(역할)을 가지고 있는지 확인해야 한다면, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` Middleware를 만들 수 있습니다.

<!-- Additional middleware parameters will be passed to the middleware after the `$next` argument: -->
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

<!-- Middleware parameters may be specified when defining the route by separating the middleware name and parameters with a `:`: -->
Middleware 매개변수는 라우트를 정의할 때 Middleware 이름과 매개변수를 `:`로 구분하여 지정할 수 있습니다.

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

<!-- Multiple parameters may be delimited by commas: -->
여러 매개변수는 쉼표로 구분할 수 있습니다.

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
<!-- ## Terminable Middleware -->
## Terminable Middleware

<!-- Sometimes a middleware may need to do some work after the HTTP response has been sent to the browser. If you define a `terminate` method on your middleware and your web server is using [FastCGI](https://www.php.net/manual/en/install.fpm.php), the `terminate` method will automatically be called after the response is sent to the browser: -->
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

<!-- The `terminate` method should receive both the request and the response. Once you have defined a terminable middleware, you should add it to the list of routes or global middleware in your application's `bootstrap/app.php` file. -->
`terminate` 메서드는 요청과 응답을 모두 받아야 합니다. 종료 가능 Middleware를 정의한 후에는 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 목록이나 전역 Middleware 목록에 추가해야 합니다.

<!-- When calling the `terminate` method on your middleware, Laravel will resolve a fresh instance of the middleware from the [service container](/docs/13.x/container). If you would like to use the same middleware instance when the `handle` and `terminate` methods are called, register the middleware with the container using the container's `singleton` method. Typically this should be done in the `register` method of your `AppServiceProvider`: -->
Middleware의 `terminate` 메서드를 호출할 때 Laravel은 [service container](/docs/13.x/container)에서 Middleware의 새 인스턴스를 해결합니다. `handle` 메서드와 `terminate` 메서드가 호출될 때 동일한 Middleware 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 사용하여 Middleware를 컨테이너에 등록하십시오. 일반적으로 이 작업은 `AppServiceProvider`의 `register` 메서드에서 수행해야 합니다.

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
