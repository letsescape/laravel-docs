<!-- # Middleware -->
# Middleware

- [Introduction](#introduction)
- [Defining Middleware](#defining-middleware)
- [Registering Middleware](#registering-middleware)
    - [Global Middleware](#global-middleware)
    - [Assigning Middleware to Routes](#assigning-middleware-to-routes)
    - [Middleware Groups](#middleware-groups)
    - [Sorting Middleware](#sorting-middleware)
- [Middleware Parameters](#middleware-parameters)
- [Terminable Middleware](#terminable-middleware)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Middleware provide a convenient mechanism for inspecting and filtering HTTP requests entering your application. For example, Laravel includes a middleware that verifies the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to your application's login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. -->
미들웨어는 애플리케이션으로 들어오는 HTTP 요청을 검사하고 걸러내는 데 유용한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지를 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않았다면, 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리다이렉트합니다. 반대로 사용자가 인증된 경우에는 요청이 계속 애플리케이션 안쪽으로 진행될 수 있도록 허용합니다.

<!-- Additional middleware can be written to perform a variety of tasks besides authentication. For example, a logging middleware might log all incoming requests to your application. There are several middleware included in the Laravel framework, including middleware for authentication and CSRF protection. All of these middleware are located in the `app/Http/Middleware` directory. -->
인증 외에도 다양한 작업을 수행하는 여러 미들웨어를 추가로 작성할 수 있습니다. 예를 들어, 요청을 기록(logging)하는 미들웨어는 애플리케이션에 들어오는 모든 요청을 로그로 남길 수 있습니다. Laravel 프레임워크에는 인증, CSRF 보호 등 다양한 미들웨어가 기본적으로 포함되어 있으며, 이런 미들웨어들은 모두 `app/Http/Middleware` 디렉터리에 위치합니다.

<a name="defining-middleware"></a>
<!-- ## Defining Middleware -->
## Defining Middleware

<!-- To create a new middleware, use the `make:middleware` Artisan command: -->
새로운 미들웨어를 생성하려면 `make:middleware` 아티즌 명령어를 사용합니다.

```shell
php artisan make:middleware EnsureTokenIsValid
```

<!-- This command will place a new `EnsureTokenIsValid` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `token` input matches a specified value. Otherwise, we will redirect the users back to the `home` URI: -->
이 명령어를 실행하면, 새로운 `EnsureTokenIsValid` 클래스가 `app/Http/Middleware` 디렉터리에 생성됩니다. 예시 미들웨어에서는 전달받은 `token` 입력값이 미리 지정된 값과 일치하는 경우에만 라우트에 접근을 허용합니다. 그렇지 않으면 사용자를 `home` URI로 리다이렉트합니다.

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
            return redirect('home');
        }

        return $next($request);
    }
}
```

<!-- As you can see, if the given `token` does not match our secret token, the middleware will return an HTTP redirect to the client; otherwise, the request will be passed further into the application. To pass the request deeper into the application (allowing the middleware to "pass"), you should call the `$next` callback with the `$request`. -->
위 예제에서 볼 수 있듯이, 전달된 `token` 값이 예상하는 값과 일치하지 않으면 미들웨어가 클라이언트에게 HTTP 리다이렉트 응답을 반환합니다. 반대로 일치하면 요청이 애플리케이션 내부로 더 깊이 전달됩니다. 미들웨어를 "통과"시켜 요청을 더 깊이 전달하려면 `$next` 콜백에 `$request`를 넘겨 호출하면 됩니다.

<!-- It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely. -->
미들웨어는 애플리케이션으로 들어오는 HTTP 요청이 여러 "레이어"를 차례로 통과해야 하는 구조로 생각하는 것이 이해하기 쉽습니다. 각 레이어마다 요청을 검사하고, 필요에 따라 요청을 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [service container](/docs/10.x/container)를 통해 해결(resolution)되므로, 미들웨어 생성자에서 필요한 의존성을 타입힌트 방식으로 자유롭게 주입받을 수 있습니다.

<a name="middleware-and-responses"></a>
<!-- #### Middleware and Responses -->
#### Middleware and Responses

<!-- Of course, a middleware can perform tasks before or after passing the request deeper into the application. For example, the following middleware would perform some task **before** the request is handled by the application: -->
물론, 미들웨어는 요청을 더 깊이 전달하기 **전** 또는 **후**에 원하는 작업을 수행할 수 있습니다. 예를 들어, 아래 미들웨어는 애플리케이션이 요청을 처리하기 **전에** 특정 작업을 실행합니다.

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
다음 미들웨어는 애플리케이션이 요청을 처리한 **후에** 작업을 실행합니다.

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

<!-- If you want a middleware to run during every HTTP request to your application, list the middleware class in the `$middleware` property of your `app/Http/Kernel.php` class. -->
모든 HTTP 요청마다 특정 미들웨어를 실행하고 싶다면, 해당 미들웨어 클래스를 `app/Http/Kernel.php` 파일의 `$middleware` 속성에 추가하면 됩니다.

<a name="assigning-middleware-to-routes"></a>
<!-- ### Assigning Middleware to Routes -->
### Assigning Middleware to Routes

<!-- If you would like to assign middleware to specific routes, you may invoke the `middleware` method when defining the route: -->
특정 라우트에만 미들웨어를 할당하고 싶다면, 라우트 정의 시 `middleware` 메서드를 사용할 수 있습니다.

```
use App\Http\Middleware\Authenticate;

Route::get('/profile', function () {
    // ...
})->middleware(Authenticate::class);
```

<!-- You may assign multiple middleware to the route by passing an array of middleware names to the `middleware` method: -->
미들웨어 이름의 배열을 `middleware` 메서드에 전달하여 여러 개의 미들웨어를 하나의 라우트에 할당할 수도 있습니다.

```
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<!-- For convenience, you may assign aliases to middleware in your application's `app/Http/Kernel.php` file. By default, the `$middlewareAliases` property of this class contains entries for the middleware included with Laravel. You may add your own middleware to this list and assign it an alias of your choosing: -->
편의를 위해, `app/Http/Kernel.php` 파일에서 미들웨어에 별칭(alias)을 부여할 수 있습니다. 기본적으로 이 클래스의 `$middlewareAliases` 속성에는 Laravel에서 제공하는 미들웨어에 대한 별칭이 등록되어 있습니다. 여기에 직접 만든 미들웨어를 추가해 원하는 별칭을 할당할 수 있습니다.

```
// Within App\Http\Kernel class...

protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'bindings' => \Illuminate\Routing\Middleware\SubstituteBindings::class,
    'cache.headers' => \Illuminate\Http\Middleware\SetCacheHeaders::class,
    'can' => \Illuminate\Auth\Middleware\Authorize::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
    'verified' => \Illuminate\Auth\Middleware\EnsureEmailIsVerified::class,
];
```

<!-- Once the middleware alias has been defined in the HTTP kernel, you may use the alias when assigning middleware to routes: -->
이렇게 별칭을 등록해 두면, 라우트에서 미들웨어를 지정할 때 별칭만 간단히 사용할 수 있습니다.

```
Route::get('/profile', function () {
    // ...
})->middleware('auth');
```

<a name="excluding-middleware"></a>
<!-- #### Excluding Middleware -->
#### Excluding Middleware

<!-- When assigning middleware to a group of routes, you may occasionally need to prevent the middleware from being applied to an individual route within the group. You may accomplish this using the `withoutMiddleware` method: -->
여러 라우트에 한 번에 미들웨어를 할당할 때, 특정 라우트만 예외적으로 미들웨어를 적용하지 않으려면 `withoutMiddleware` 메서드를 사용할 수 있습니다.

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

<!-- You may also exclude a given set of middleware from an entire [group](/docs/10.x/routing#route-groups) of route definitions: -->
또는, [group](/docs/10.x/routing#route-groups) 전체에 대해 미들웨어 적용을 제외할 수도 있습니다.

```
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

<!-- The `withoutMiddleware` method can only remove route middleware and does not apply to [global middleware](#global-middleware). -->
`withoutMiddleware` 메서드는 라우트 미들웨어만 제거할 수 있으며, [global middleware](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
<!-- ### Middleware Groups -->
### Middleware Groups

<!-- Sometimes you may want to group several middleware under a single key to make them easier to assign to routes. You may accomplish this using the `$middlewareGroups` property of your HTTP kernel. -->
여러 개의 미들웨어를 하나의 키로 묶어서 라우트에 편리하게 적용하고 싶을 때는, HTTP 커널의 `$middlewareGroups` 속성을 사용해 미들웨어 그룹을 만들 수 있습니다.

<!-- Laravel includes predefined `web` and `api` middleware groups that contain common middleware you may want to apply to your web and API routes. Remember, these middleware groups are automatically applied by your application's `App\Providers\RouteServiceProvider` service provider to routes within your corresponding `web` and `api` route files: -->
Laravel에는 `web`과 `api`라는 미들웨어 그룹이 기본으로 정의되어 있는데, 각각 웹 라우트와 API 라우트에 일반적으로 적용할 미들웨어들을 포함하고 있습니다. 이 미들웨어 그룹들은 애플리케이션의 `App\Providers\RouteServiceProvider` 서비스 프로바이더에 의해 해당하는 `web`과 `api` 라우트 파일에 자동으로 적용됩니다.

```
/**
 * The application's route middleware groups.
 *
 * @var array
 */
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \App\Http\Middleware\VerifyCsrfToken::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

    'api' => [
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

<!-- Middleware groups may be assigned to routes and controller actions using the same syntax as individual middleware. Again, middleware groups make it more convenient to assign many middleware to a route at once: -->
미들웨어 그룹도 개별 미들웨어와 같은 방식으로 라우트나 컨트롤러 액션에 할당할 수 있습니다. 여러 미들웨어를 한 번에 라우트에 지정하고 싶을 때 매우 유용합니다.

```
Route::get('/', function () {
    // ...
})->middleware('web');

Route::middleware(['web'])->group(function () {
    // ...
});
```

> [!NOTE]
> 기본적으로, `web`과 `api` 미들웨어 그룹은 각각 애플리케이션의 `routes/web.php`와 `routes/api.php` 파일에 `App\Providers\RouteServiceProvider`가 자동으로 적용합니다.

<a name="sorting-middleware"></a>
<!-- ### Sorting Middleware -->
### Sorting Middleware

<!-- Rarely, you may need your middleware to execute in a specific order but not have control over their order when they are assigned to the route. In this case, you may specify your middleware priority using the `$middlewarePriority` property of your `app/Http/Kernel.php` file. This property may not exist in your HTTP kernel by default. If it does not exist, you may copy its default definition below: -->
드물지만, 미들웨어가 특정한 순서로 실행되어야 하는데 라우트에서 그 순서를 제어할 수 없는 상황이 있을 수 있습니다. 이 경우 `app/Http/Kernel.php` 파일의 `$middlewarePriority` 속성을 이용해 미들웨어 우선순위를 지정할 수 있습니다. 이 속성은 기본적으로 없을 수도 있기에, 필요하다면 아래 예시처럼 정의하면 됩니다.

```
/**
 * The priority-sorted list of middleware.
 *
 * This forces non-global middleware to always be in the given order.
 *
 * @var string[]
 */
protected $middlewarePriority = [
    \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
    \Illuminate\Cookie\Middleware\EncryptCookies::class,
    \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
    \Illuminate\Session\Middleware\StartSession::class,
    \Illuminate\View\Middleware\ShareErrorsFromSession::class,
    \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class,
    \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
    \Illuminate\Contracts\Session\Middleware\AuthenticatesSessions::class,
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
    \Illuminate\Auth\Middleware\Authorize::class,
];
```

<a name="middleware-parameters"></a>
<!-- ## Middleware Parameters -->
## Middleware Parameters

<!-- Middleware can also receive additional parameters. For example, if your application needs to verify that the authenticated user has a given "role" before performing a given action, you could create an `EnsureUserHasRole` middleware that receives a role name as an additional argument. -->
미들웨어는 추가적인 파라미터를 받을 수도 있습니다. 예를 들어, 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인한 후에만 어떤 행동을 허용하고 싶다면, 추가 인수로 역할 이름을 전달받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

<!-- Additional middleware parameters will be passed to the middleware after the `$next` argument: -->
추가 미들웨어 파라미터는 `$next` 인수 다음에 전달됩니다.

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
미들웨어에 파라미터를 전달할 때는 미들웨어 이름 뒤에 `:` 로 구분해 작성하면 됩니다.

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor');
```

<!-- Multiple parameters may be delimited by commas: -->
여러 개의 파라미터는 쉼표로 구분합니다.

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor,publisher');
```

<a name="terminable-middleware"></a>
<!-- ## Terminable Middleware -->
## Terminable Middleware

<!-- Sometimes a middleware may need to do some work after the HTTP response has been sent to the browser. If you define a `terminate` method on your middleware and your web server is using FastCGI, the `terminate` method will automatically be called after the response is sent to the browser: -->
가끔 미들웨어가 HTTP 응답이 브라우저에 전송된 **이후**에 어떤 작업을 해야 할 때가 있습니다. 만약 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 FastCGI를 사용하고 있다면, 응답이 브라우저로 전송된 후에 자동으로 `terminate` 메서드가 호출됩니다.

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

<!-- The `terminate` method should receive both the request and the response. Once you have defined a terminable middleware, you should add it to the list of routes or global middleware in the `app/Http/Kernel.php` file. -->
`terminate` 메서드는 요청(Request)과 응답(Response)을 모두 매개변수로 전달받아야 합니다. 종결형 미들웨어를 정의했다면, 반드시 해당 미들웨어를 `app/Http/Kernel.php` 파일의 라우트 또는 전역 미들웨어 목록에 등록해야 합니다.

<!-- When calling the `terminate` method on your middleware, Laravel will resolve a fresh instance of the middleware from the [service container](/docs/10.x/container). If you would like to use the same middleware instance when the `handle` and `terminate` methods are called, register the middleware with the container using the container's `singleton` method. Typically this should be done in the `register` method of your `AppServiceProvider`: -->
Laravel이 미들웨어의 `terminate` 메서드를 호출할 때는 [service container](/docs/10.x/container)로부터 미들웨어의 새로운 인스턴스를 해결(resolution)하게 됩니다. 만약 `handle`과 `terminate` 메서드 호출 시 동일한 미들웨어 인스턴스를 사용하고 싶다면, 컨테이너의 `singleton` 메서드를 통해 미들웨어를 단일 인스턴스로 등록해야 합니다. 일반적으로는 `AppServiceProvider`의 `register` 메서드에서 아래와 같이 처리합니다.

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
