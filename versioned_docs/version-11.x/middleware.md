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
미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링할 수 있도록 도와주는 편리한 기능입니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우, 해당 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 반대로 인증이 된 사용자의 경우에는 요청이 애플리케이션 내부로 더 진행될 수 있도록 허용합니다.

<!-- Additional middleware can be written to perform a variety of tasks besides authentication. For example, a logging middleware might log all incoming requests to your application. A variety of middleware are included in Laravel, including middleware for authentication and CSRF protection; however, all user-defined middleware are typically located in your application's `app/Http/Middleware` directory. -->
인증 외에도 다양한 작업을 수행하는 추가 미들웨어를 직접 작성할 수 있습니다. 예를 들어, 로깅 미들웨어는 애플리케이션에 들어오는 모든 요청을 기록할 수 있습니다. Laravel에는 인증, CSRF 보호 등 다양한 미들웨어가 기본적으로 포함되어 있지만, 모든 사용자 정의 미들웨어는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉터리에 위치하게 됩니다.

<a name="defining-middleware"></a>
<!-- ## Defining Middleware -->
## Defining Middleware

<!-- To create a new middleware, use the `make:middleware` Artisan command: -->
새로운 미들웨어를 생성하려면, `make:middleware` 아티즌 명령어를 사용하세요.

```shell
php artisan make:middleware EnsureTokenIsValid
```

<!-- This command will place a new `EnsureTokenIsValid` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `token` input matches a specified value. Otherwise, we will redirect the users back to the `/home` URI: -->
이 명령을 실행하면 `app/Http/Middleware` 디렉터리에 `EnsureTokenIsValid` 클래스가 생성됩니다. 여기서는 전달받은 `token` 입력 값이 지정한 값과 일치하는 경우에만 해당 라우트에 접근을 허용할 것입니다. 그렇지 않으면 사용자를 `/home` URI로 리디렉션합니다.

```
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
코드를 보면, 제공된 `token` 값이 우리의 비밀 토큰과 일치하지 않을 때 미들웨어가 HTTP 리디렉션을 클라이언트에 반환합니다. 일치할 경우에는 요청이 애플리케이션 내부로 더 진행됩니다. 미들웨어를 통과시키고 싶다면 `$next` 콜백에 `$request`를 전달해야 합니다.

<!-- It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely. -->
미들웨어는 애플리케이션에 도달하기 전 HTTP 요청이 여러 "레이어"를 통과해야 하는 구조로 생각하면 이해가 쉽습니다. 각 레이어는 요청을 검사하고, 필요하다면 전체적으로 거절할 수 있습니다.

> [!NOTE]
> 모든 미들웨어는 [service container](/docs/11.x/container)를 통해 resolve되므로, 미들웨어의 생성자에 필요한 의존성을 타입힌트로 선언할 수 있습니다.

<a name="middleware-and-responses"></a>
<!-- #### Middleware and Responses -->
#### Middleware and Responses

<!-- Of course, a middleware can perform tasks before or after passing the request deeper into the application. For example, the following middleware would perform some task **before** the request is handled by the application: -->
물론, 미들웨어는 요청이 애플리케이션 내부로 전달되기 **전**이나 **후**에 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 요청이 애플리케이션에서 처리되기 **전**에 특정 작업을 수행합니다.

```
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
반면에, 아래 미들웨어는 요청이 애플리케이션에서 처리된 **후**에 작업을 수행합니다.

```
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
애플리케이션으로 들어오는 모든 HTTP 요청마다 미들웨어를 실행하고 싶다면, `bootstrap/app.php` 파일의 글로벌 미들웨어 스택에 해당 미들웨어를 추가하면 됩니다.

```
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware) {
     $middleware->append(EnsureTokenIsValid::class);
})
```

<!-- The `$middleware` object provided to the `withMiddleware` closure is an instance of `Illuminate\Foundation\Configuration\Middleware` and is responsible for managing the middleware assigned to your application's routes. The `append` method adds the middleware to the end of the list of global middleware. If you would like to add a middleware to the beginning of the list, you should use the `prepend` method. -->
`withMiddleware` 클로저에 전달되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware` 인스턴스이며, 애플리케이션의 라우트에 할당된 미들웨어를 관리합니다. `append` 메서드는 해당 미들웨어를 글로벌 미들웨어 리스트의 **끝**에 추가합니다. 만약 리스트의 **앞**에 추가하고 싶다면, `prepend` 메서드를 사용하세요.

<a name="manually-managing-laravels-default-global-middleware"></a>
<!-- #### Manually Managing Laravel's Default Global Middleware -->
#### Manually Managing Laravel's Default Global Middleware

<!-- If you would like to manage Laravel's global middleware stack manually, you may provide Laravel's default stack of global middleware to the `use` method. Then, you may adjust the default middleware stack as necessary: -->
Laravel의 글로벌 미들웨어 스택을 직접 관리하고 싶다면, 기본 글로벌 미들웨어 스택을 `use` 메서드에 전달하여 필요에 따라 수정할 수 있습니다.

```
->withMiddleware(function (Middleware $middleware) {
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
특정 라우트에만 미들웨어를 적용하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 호출하면 됩니다.

```
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

<!-- You may assign multiple middleware to the route by passing an array of middleware names to the `middleware` method: -->
여러 개의 미들웨어를 라우트에 할당하려면, 미들웨어 이름의 배열을 `middleware` 메서드에 전달하면 됩니다.

```
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
<!-- #### Excluding Middleware -->
#### Excluding Middleware

<!-- When assigning middleware to a group of routes, you may occasionally need to prevent the middleware from being applied to an individual route within the group. You may accomplish this using the `withoutMiddleware` method: -->
여러 라우트가 하나의 그룹으로 묶여 있고 그 그룹 전체에 미들웨어가 적용되어 있는 경우, 특정 라우트만 미들웨어에서 제외하고 싶을 때가 있습니다. 이럴 때는 `withoutMiddleware` 메서드를 사용하세요.

```
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

<!-- You may also exclude a given set of middleware from an entire [group](/docs/11.x/routing#route-groups) of route definitions: -->
또는 [group](/docs/11.x/routing#route-groups) 전체에서 지정된 미들웨어를 제외할 수도 있습니다.

```
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

<!-- The `withoutMiddleware` method can only remove route middleware and does not apply to [global middleware](#global-middleware). -->
`withoutMiddleware` 메서드는 오직 라우트 미들웨어만 제거할 수 있고, [global middleware](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
<!-- ### Middleware Groups -->
### Middleware Groups

<!-- Sometimes you may want to group several middleware under a single key to make them easier to assign to routes. You may accomplish this using the `appendToGroup` method within your application's `bootstrap/app.php` file: -->
여러 미들웨어를 하나의 키 이름 아래로 묶어서 라우트에 쉽게 할당하고 싶을 때가 있습니다. 이럴 때는 `bootstrap/app.php` 파일 내에서 `appendToGroup` 메서드를 사용해 미들웨어 그룹을 생성하세요.

```
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware) {
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
미들웨어 그룹은 개별 미들웨어와 동일한 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다.

```
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
Laravel에서는 웹과 API 라우트에 자주 사용되는 미들웨어를 미리 묶어둔 `web` 및 `api` 그룹을 제공합니다. 이 미들웨어 그룹들은 Laravel이 자동으로 `routes/web.php`와 `routes/api.php` 파일에 적용합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `web` 미들웨어 그룹 |
| --- |
| `Illuminate\Cookie\Middleware\EncryptCookies` |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession` |
| `Illuminate\View\Middleware\ShareErrorsFromSession` |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

<!-- </div> -->
</div>

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `api` 미들웨어 그룹 |
| --- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

<!-- </div> -->
</div>

<!-- If you would like to append or prepend middleware to these groups, you may use the `web` and `api` methods within your application's `bootstrap/app.php` file. The `web` and `api` methods are convenient alternatives to the `appendToGroup` method: -->
이 그룹에 미들웨어를 추가하거나 앞에 삽입하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 및 `api` 메서드를 활용할 수 있습니다. `web` 및 `api` 메서드는 `appendToGroup` 메서드의 간편한 대안입니다.

```
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```

<!-- You may even replace one of Laravel's default middleware group entries with a custom middleware of your own: -->
Laravel이 기본적으로 제공하는 미들웨어 그룹 엔트리를 커스텀 미들웨어로 교체할 수도 있습니다.

```
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

<!-- Or, you may remove a middleware entirely: -->
혹은 미들웨어를 아예 제거할 수도 있습니다.

```
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
<!-- #### Manually Managing Laravel's Default Middleware Groups -->
#### Manually Managing Laravel's Default Middleware Groups

<!-- If you would like to manually manage all of the middleware within Laravel's default `web` and `api` middleware groups, you may redefine the groups entirely. The example below will define the `web` and `api` middleware groups with their default middleware, allowing you to customize them as necessary: -->
Laravel에서 기본으로 제공하는 `web` 및 `api` 미들웨어 그룹을 직접 완전히 관리하고 싶다면, 그룹을 처음부터 다시 정의하면 됩니다. 아래 예시는 `web` 및 `api` 미들웨어 그룹을 기본 미들웨어로 정의하여, 필요에 따라 자유롭게 수정할 수 있게 해 줍니다.

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
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
> 기본적으로 `web` 및 `api` 미들웨어 그룹은 `bootstrap/app.php` 파일에서 자동으로 각 라우트 파일(`routes/web.php`, `routes/api.php`)에 적용됩니다.

<a name="middleware-aliases"></a>
<!-- ### Middleware Aliases -->
### Middleware Aliases

<!-- You may assign aliases to middleware in your application's `bootstrap/app.php` file. Middleware aliases allow you to define a short alias for a given middleware class, which can be especially useful for middleware with long class names: -->
애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어에 별칭을 붙일 수 있습니다. 미들웨어 별칭(aliases)을 사용하면 긴 클래스명을 짧고 간단하게 참조할 수 있어서 편리합니다.

```
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware) {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

<!-- Once the middleware alias has been defined in your application's `bootstrap/app.php` file, you may use the alias when assigning the middleware to routes: -->
애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어 별칭을 정의한 뒤에는, 라우트에 미들웨어를 할당할 때 별칭을 사용하면 됩니다.

```
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

<!-- For convenience, some of Laravel's built-in middleware are aliased by default. For example, the `auth` middleware is an alias for the `Illuminate\Auth\Middleware\Authenticate` middleware. Below is a list of the default middleware aliases: -->
기본적으로 Laravel에 내장된 몇몇 미들웨어는 이미 별칭이 지정되어 있습니다. 예를 들어, `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 미들웨어의 별칭입니다. 기본 미들웨어 별칭은 아래와 같습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 별칭 | 미들웨어 |
| --- | --- |
| `auth` | `Illuminate\Auth\Middleware\Authenticate` |
| `auth.basic` | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth` |
| `auth.session` | `Illuminate\Session\Middleware\AuthenticateSession` |
| `cache.headers` | `Illuminate\Http\Middleware\SetCacheHeaders` |
| `can` | `Illuminate\Auth\Middleware\Authorize` |
| `guest` | `Illuminate\Auth\Middleware\RedirectIfAuthenticated` |
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword` |
| `precognitive` | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests` |
| `signed` | `Illuminate\Routing\Middleware\ValidateSignature` |
| `subscribed` | `\Spark\Http\Middleware\VerifyBillableIsSubscribed` |
| `throttle` | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified` | `Illuminate\Auth\Middleware\EnsureEmailIsVerified` |

<!-- </div> -->
</div>

<a name="sorting-middleware"></a>
<!-- ### Sorting Middleware -->
### Sorting Middleware

<!-- Rarely, you may need your middleware to execute in a specific order but not have control over their order when they are assigned to the route. In these situations, you may specify your middleware priority using the `priority` method in your application's `bootstrap/app.php` file: -->
특별한 경우에 한해, 어떤 미들웨어가 우선적으로 실행되어야 하는데 라우트에 할당된 순서를 제어할 수 없는 상황일 때가 있습니다. 이럴 때는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용하여 미들웨어의 우선순위를 지정할 수 있습니다.

```
->withMiddleware(function (Middleware $middleware) {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
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
미들웨어는 추가적인 파라미터(매개변수)를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인하고 싶을 때, 역할 이름을 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

<!-- Additional middleware parameters will be passed to the middleware after the `$next` argument: -->
추가 미들웨어 파라미터는 `$next` 인자 이후 순서로 미들웨어에 전달됩니다.

```
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
미들웨어 파라미터는 라우트 정의에서 `:`(콜론)으로 미들웨어 이름과 파라미터를 구분하여 지정할 수 있습니다.

```
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

<!-- Multiple parameters may be delimited by commas: -->
여러 개의 파라미터가 필요하다면, 쉼표로 구분하여 전달할 수 있습니다.

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
<!-- ## Terminable Middleware -->
## Terminable Middleware

<!-- Sometimes a middleware may need to do some work after the HTTP response has been sent to the browser. If you define a `terminate` method on your middleware and your web server is using FastCGI, the `terminate` method will automatically be called after the response is sent to the browser: -->
때로는 HTTP 응답이 브라우저로 전송된 후에 미들웨어가 추가 작업을 해야 하는 상황도 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용 중이라면, 응답이 브라우저로 전송된 뒤에 이 `terminate` 메서드가 자동으로 호출됩니다.

```
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
`terminate` 메서드는 요청과 응답 객체를 모두 받아야 합니다. 종료 가능한 미들웨어를 정의한 후에는 해당 미들웨어를 꼭 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 또는 글로벌 미들웨어 목록에 추가해야 작동합니다.

<!-- When calling the `terminate` method on your middleware, Laravel will resolve a fresh instance of the middleware from the [service container](/docs/11.x/container). If you would like to use the same middleware instance when the `handle` and `terminate` methods are called, register the middleware with the container using the container's `singleton` method. Typically this should be done in the `register` method of your `AppServiceProvider`: -->
Laravel이 미들웨어의 `terminate` 메서드를 호출할 때, [service container](/docs/11.x/container)에서 새로운 미들웨어 인스턴스를 resolve합니다. 만약 `handle`과 `terminate` 메서드 호출 시 동일한 미들웨어 인스턴스를 사용하고 싶다면, 해당 미들웨어를 컨테이너의 `singleton` 메서드로 등록해야 합니다. 보통은 `AppServiceProvider`의 `register` 메서드에서 이 작업을 수행합니다.

```
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```
