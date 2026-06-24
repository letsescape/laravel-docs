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
ミドルウェアは、アプリケーションに入る HTTP リクエストを検査およびフィルタリングするための便利なメカニズムを提供します。たとえば、Laravel には、アプリケーションのユーザーが認証されていることを確認するミドルウェアが含まれています。ユーザーが認証されていない場合、ミドルウェアはユーザーをアプリケーションのログイン画面にリダイレクトします。ただし、ユーザーが認証されている場合、ミドルウェアはリクエストがアプリケーション内にさらに進むことを許可します。

<!-- Additional middleware can be written to perform a variety of tasks besides authentication. For example, a logging middleware might log all incoming requests to your application. There are several middleware included in the Laravel framework, including middleware for authentication and CSRF protection. All of these middleware are located in the `app/Http/Middleware` directory. -->
追加のミドルウェアを作成して、認証以外のさまざまなタスクを実行できます。たとえば、ログ ミドルウェアは、アプリケーションに受信したすべてのリクエストをログに記録する場合があります。 Laravel フレームワークには、認証や CSRF 保護用のミドルウェアなど、いくつかのミドルウェアが含まれています。これらのミドルウェアはすべて、`app/Http/Middleware` ディレクトリにあります。

<a name="defining-middleware"></a>
<!-- ## Defining Middleware -->
## Defining Middleware

<!-- To create a new middleware, use the `make:middleware` Artisan command: -->
新しいミドルウェアを作成するには、`make:middleware` Artisan コマンドを使用します。

```shell
php artisan make:middleware EnsureTokenIsValid
```

<!-- This command will place a new `EnsureTokenIsValid` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `token` input matches a specified value. Otherwise, we will redirect the users back to the `home` URI: -->
このコマンドは、`app/Http/Middleware` ディレクトリ内に新しい `EnsureTokenIsValid` クラスを配置します。このミドルウェアでは、指定された `token` 入力が指定された値と一致する場合にのみルートへのアクセスを許可します。それ以外の場合は、ユーザーを `home` URI にリダイレクトします。

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
ご覧のとおり、指定された `token` がシークレット トークンと一致しない場合、ミドルウェアはクライアントに HTTP リダイレクトを返します。それ以外の場合、リクエストはさらにアプリケーションに渡されます。リクエストをアプリケーションのさらに奥深くに渡すには (ミドルウェアが「渡す」ことができるように)、`$request` を使用して `$next` コールバックを呼び出す必要があります。

<!-- It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely. -->
ミドルウェアは、HTTP リクエストがアプリケーションに到達する前に通過する必要がある一連の「レイヤー」であると考えるのが最善です。各層はリクエストを検査し、完全に拒否することもできます。

> [!NOTE]
> すべてのミドルウェアは [service container](/docs/10.x/container) 経由で解決されるため、ミドルウェアのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="middleware-and-responses"></a>
<!-- #### Middleware and Responses -->
#### Middleware and Responses

<!-- Of course, a middleware can perform tasks before or after passing the request deeper into the application. For example, the following middleware would perform some task **before** the request is handled by the application: -->
もちろん、ミドルウェアは、リクエストをアプリケーションの奥深くに渡す前または後にタスクを実行できます。たとえば、次のミドルウェアは、アプリケーションによってリクエストが処理される **前** に何らかのタスクを実行します。

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
ただし、このミドルウェアは、リクエストがアプリケーションによって処理された**後**にタスクを実行します。

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
アプリケーションへのすべての HTTP リクエスト中にミドルウェアを実行する場合は、`app/Http/Kernel.php` クラスの `$middleware` プロパティにミドルウェア クラスをリストします。

<a name="assigning-middleware-to-routes"></a>
<!-- ### Assigning Middleware to Routes -->
### Assigning Middleware to Routes

<!-- If you would like to assign middleware to specific routes, you may invoke the `middleware` method when defining the route: -->
ミドルウェアを特定のルートに割り当てたい場合は、ルートを定義するときに `middleware` メソッドを呼び出すことができます。

```
use App\Http\Middleware\Authenticate;

Route::get('/profile', function () {
    // ...
})->middleware(Authenticate::class);
```

<!-- You may assign multiple middleware to the route by passing an array of middleware names to the `middleware` method: -->
ミドルウェア名の配列を `middleware` メソッドに渡すことで、ルートに複数のミドルウェアを割り当てることができます。

```
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<!-- For convenience, you may assign aliases to middleware in your application's `app/Http/Kernel.php` file. By default, the `$middlewareAliases` property of this class contains entries for the middleware included with Laravel. You may add your own middleware to this list and assign it an alias of your choosing: -->
便宜上、アプリケーションの `app/Http/Kernel.php` ファイル内のミドルウェアにエイリアスを割り当てることができます。デフォルトでは、このクラスの `$middlewareAliases` プロパティには、Laravel に含まれるミドルウェアのエントリが含まれています。独自のミドルウェアをこのリストに追加し、選択した別名を割り当てることができます。

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
ミドルウェアのエイリアスが HTTP カーネルで定義されたら、ミドルウェアをルートに割り当てるときにそのエイリアスを使用できます。

```
Route::get('/profile', function () {
    // ...
})->middleware('auth');
```

<a name="excluding-middleware"></a>
<!-- #### Excluding Middleware -->
#### Excluding Middleware

<!-- When assigning middleware to a group of routes, you may occasionally need to prevent the middleware from being applied to an individual route within the group. You may accomplish this using the `withoutMiddleware` method: -->
ルートのグループにミドルウェアを割り当てる場合、グループ内の個々のルートにミドルウェアが適用されないようにする必要がある場合があります。これは、`withoutMiddleware` メソッドを使用して実行できます。

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
特定のミドルウェアのセットをルート定義の [group](/docs/10.x/routing#route-groups) 全体から除外することもできます。

```
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

<!-- The `withoutMiddleware` method can only remove route middleware and does not apply to [global middleware](#global-middleware). -->
`withoutMiddleware` メソッドはルート ミドルウェアのみを削除でき、[global middleware](#global-middleware) には適用されません。

<a name="middleware-groups"></a>
<!-- ### Middleware Groups -->
### Middleware Groups

<!-- Sometimes you may want to group several middleware under a single key to make them easier to assign to routes. You may accomplish this using the `$middlewareGroups` property of your HTTP kernel. -->
ルートへの割り当てを容易にするために、複数のミドルウェアを 1 つのキーの下にグループ化したい場合があります。これは、HTTP カーネルの `$middlewareGroups` プロパティを使用して実行できます。

<!-- Laravel includes predefined `web` and `api` middleware groups that contain common middleware you may want to apply to your web and API routes. Remember, these middleware groups are automatically applied by your application's `App\Providers\RouteServiceProvider` service provider to routes within your corresponding `web` and `api` route files: -->
Laravel には、Web ルートや API ルートに適用できる一般的なミドルウェアを含む、事前定義された `web` および `api` ミドルウェア グループが含まれています。これらのミドルウェア グループは、アプリケーションの `App\Providers\RouteServiceProvider` サービスプロバイダによって、対応する `web` および `api` ルート ファイル内のルートに自動的に適用されることに注意してください。

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
ミドルウェア グループは、個々のミドルウェアと同じ構文を使用してルートとコントローラ アクションに割り当てることができます。繰り返しになりますが、ミドルウェア グループを使用すると、多くのミドルウェアを一度にルートに割り当てることがより便利になります。

```
Route::get('/', function () {
    // ...
})->middleware('web');

Route::middleware(['web'])->group(function () {
    // ...
});
```

> [!NOTE]
> すぐに使用できる状態では、`web` および `api` ミドルウェア グループは、`App\Providers\RouteServiceProvider` によって、アプリケーションの対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用されます。

<a name="sorting-middleware"></a>
<!-- ### Sorting Middleware -->
### Sorting Middleware

<!-- Rarely, you may need your middleware to execute in a specific order but not have control over their order when they are assigned to the route. In this case, you may specify your middleware priority using the `$middlewarePriority` property of your `app/Http/Kernel.php` file. This property may not exist in your HTTP kernel by default. If it does not exist, you may copy its default definition below: -->
まれに、ミドルウェアを特定の順序で実行する必要があるが、ルートに割り当てられたときにその順序を制御できない場合があります。この場合、`app/Http/Kernel.php` ファイルの `$middlewarePriority` プロパティを使用してミドルウェアの優先順位を指定できます。このプロパティは、デフォルトでは HTTP カーネルに存在しない可能性があります。存在しない場合は、以下のデフォルトの定義をコピーできます。

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
ミドルウェアは追加のパラメーターを受け取ることもできます。たとえば、アプリケーションが特定のアクションを実行する前に、認証されたユーザーが特定の「ロール」を持っていることを確認する必要がある場合、追加の引数としてロール名を受け取る `EnsureUserHasRole` ミドルウェアを作成できます。

<!-- Additional middleware parameters will be passed to the middleware after the `$next` argument: -->
追加のミドルウェア パラメーターは、`$next` 引数の後にミドルウェアに渡されます。

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
ルートを定義するときに、ミドルウェア名とパラメーターを `:` で区切ることにより、ミドルウェア パラメーターを指定できます。

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor');
```

<!-- Multiple parameters may be delimited by commas: -->
複数のパラメータはカンマで区切ることができます。

```
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware('role:editor,publisher');
```

<a name="terminable-middleware"></a>
<!-- ## Terminable Middleware -->
## Terminable Middleware

<!-- Sometimes a middleware may need to do some work after the HTTP response has been sent to the browser. If you define a `terminate` method on your middleware and your web server is using FastCGI, the `terminate` method will automatically be called after the response is sent to the browser: -->
場合によっては、HTTP 応答がブラウザーに送信された後にミドルウェアが何らかの作業を行う必要がある場合があります。ミドルウェアで `terminate` メソッドを定義し、Web サーバーが FastCGI を使用している場合、応答がブラウザに送信された後、`terminate` メソッドが自動的に呼び出されます。

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
`terminate` メソッドは、リクエストとレスポンスの両方を受信する必要があります。終了可能なミドルウェアを定義したら、それを `app/Http/Kernel.php` ファイル内のルートまたはグローバル ミドルウェアのリストに追加する必要があります。

<!-- When calling the `terminate` method on your middleware, Laravel will resolve a fresh instance of the middleware from the [service container](/docs/10.x/container). If you would like to use the same middleware instance when the `handle` and `terminate` methods are called, register the middleware with the container using the container's `singleton` method. Typically this should be done in the `register` method of your `AppServiceProvider`: -->
ミドルウェアで `terminate` メソッドを呼び出すと、Laravel は [service container](/docs/10.x/container) からミドルウェアの新しいインスタンスを解決します。 `handle` メソッドと `terminate` メソッドが呼び出されるときに同じミドルウェア インスタンスを使用したい場合は、コンテナーの `singleton` メソッドを使用してミドルウェアをコンテナーに登録します。通常、これは `AppServiceProvider` の `register` メソッドで実行する必要があります。

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

