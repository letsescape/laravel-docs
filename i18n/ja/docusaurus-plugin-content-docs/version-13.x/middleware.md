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
ミドルウェアは、アプリケーションに入る HTTP リクエストを検査およびフィルタリングするための便利なメカニズムを提供します。たとえば、Laravel には、アプリケーションのユーザーが認証されていることを確認するミドルウェアが含まれています。ユーザーが認証されていない場合、ミドルウェアはユーザーをアプリケーションのログイン画面にリダイレクトします。ただし、ユーザーが認証されている場合、ミドルウェアはリクエストがアプリケーション内にさらに進むことを許可します。

<!-- Additional middleware can be written to perform a variety of tasks besides authentication. For example, a logging middleware might log all incoming requests to your application. A variety of middleware are included in Laravel, including middleware for authentication and CSRF protection; however, all user-defined middleware are typically located in your application's `app/Http/Middleware` directory. -->
追加のミドルウェアを作成して、認証以外のさまざまなタスクを実行できます。たとえば、ログ ミドルウェアは、アプリケーションに受信したすべてのリクエストをログに記録する場合があります。 Laravel には、認証や CSRF 保護用のミドルウェアなど、さまざまなミドルウェアが含まれています。ただし、ユーザー定義のミドルウェアはすべて、通常、アプリケーションの `app/Http/Middleware` ディレクトリにあります。

<a name="defining-middleware"></a>
<!-- ## Defining Middleware -->
## Defining Middleware

<!-- To create a new middleware, use the `make:middleware` Artisan command: -->
新しいミドルウェアを作成するには、`make:middleware` Artisan コマンドを使用します。

```shell
php artisan make:middleware EnsureTokenIsValid
```

<!-- This command will place a new `EnsureTokenIsValid` class within your `app/Http/Middleware` directory. In this middleware, we will only allow access to the route if the supplied `token` input matches a specified value. Otherwise, we will redirect the users back to the `/home` URI: -->
このコマンドは、`app/Http/Middleware` ディレクトリ内に新しい `EnsureTokenIsValid` クラスを配置します。このミドルウェアでは、指定された `token` 入力が指定された値と一致する場合にのみルートへのアクセスを許可します。それ以外の場合は、ユーザーを `/home` URI にリダイレクトします。

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
ご覧のとおり、指定された `token` がシークレット トークンと一致しない場合、ミドルウェアはクライアントに HTTP リダイレクトを返します。それ以外の場合、リクエストはさらにアプリケーションに渡されます。リクエストをアプリケーションのさらに奥深くに渡すには (ミドルウェアが「渡す」ことができるように)、`$request` を使用して `$next` コールバックを呼び出す必要があります。

<!-- It's best to envision middleware as a series of "layers" HTTP requests must pass through before they hit your application. Each layer can examine the request and even reject it entirely. -->
ミドルウェアは、HTTP リクエストがアプリケーションに到達する前に通過する必要がある一連の「レイヤー」であると考えるのが最善です。各層はリクエストを検査し、完全に拒否することもできます。

> [!NOTE]
> すべてのミドルウェアは [service container](/docs/13.x/container) 経由で解決されるため、ミドルウェアのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="middleware-and-responses"></a>
<!-- #### Middleware and Responses -->
#### Middleware and Responses

<!-- Of course, a middleware can perform tasks before or after passing the request deeper into the application. For example, the following middleware would perform some task **before** the request is handled by the application: -->
もちろん、ミドルウェアは、リクエストをアプリケーションの奥深くに渡す前または後にタスクを実行できます。たとえば、次のミドルウェアは、アプリケーションによってリクエストが処理される **前** に何らかのタスクを実行します。

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
ただし、このミドルウェアは、リクエストがアプリケーションによって処理された**後**にタスクを実行します。

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
アプリケーションへのすべての HTTP リクエスト中にミドルウェアを実行したい場合は、アプリケーションの `bootstrap/app.php` ファイル内のグローバル ミドルウェア スタックにミドルウェアを追加できます。

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

<!-- The `$middleware` object provided to the `withMiddleware` closure is an instance of `Illuminate\Foundation\Configuration\Middleware` and is responsible for managing the middleware assigned to your application's routes. The `append` method adds the middleware to the end of the list of global middleware. If you would like to add a middleware to the beginning of the list, you should use the `prepend` method. -->
`withMiddleware` クロージャーに提供される `$middleware` オブジェクトは、`Illuminate\Foundation\Configuration\Middleware` のインスタンスであり、アプリケーションのルートに割り当てられたミドルウェアを管理します。 `append` メソッドは、グローバル ミドルウェアのリストの最後にミドルウェアを追加します。リストの先頭にミドルウェアを追加したい場合は、`prepend` メソッドを使用する必要があります。

<a name="manually-managing-laravels-default-global-middleware"></a>
<!-- #### Manually Managing Laravel's Default Global Middleware -->
#### Manually Managing Laravel's Default Global Middleware

<!-- If you would like to manage Laravel's global middleware stack manually, you may provide Laravel's default stack of global middleware to the `use` method. Then, you may adjust the default middleware stack as necessary: -->
Laravel のグローバルミドルウェアスタックを手動で管理したい場合は、Laravel のグローバルミドルウェアのデフォルトスタックを `use` メソッドに提供できます。次に、必要に応じてデフォルトのミドルウェア スタックを調整できます。

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
ミドルウェアを特定のルートに割り当てたい場合は、ルートを定義するときに `middleware` メソッドを呼び出すことができます。

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

<!-- You may assign multiple middleware to the route by passing an array of middleware names to the `middleware` method: -->
ミドルウェア名の配列を `middleware` メソッドに渡すことで、ルートに複数のミドルウェアを割り当てることができます。

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
<!-- #### Excluding Middleware -->
#### Excluding Middleware

<!-- When assigning middleware to a group of routes, you may occasionally need to prevent the middleware from being applied to an individual route within the group. You may accomplish this using the `withoutMiddleware` method: -->
ルートのグループにミドルウェアを割り当てる場合、グループ内の個々のルートにミドルウェアが適用されないようにする必要がある場合があります。これは、`withoutMiddleware` メソッドを使用して実行できます。

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
特定のミドルウェアのセットをルート定義の [group](/docs/13.x/routing#route-groups) 全体から除外することもできます。

```php
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

<!-- Sometimes you may want to group several middleware under a single key to make them easier to assign to routes. You may accomplish this using the `appendToGroup` method within your application's `bootstrap/app.php` file: -->
ルートへの割り当てを容易にするために、複数のミドルウェアを 1 つのキーの下にグループ化したい場合があります。これは、アプリケーションの `bootstrap/app.php` ファイル内で `appendToGroup` メソッドを使用して実行できます。

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
ミドルウェア グループは、個々のミドルウェアと同じ構文を使用してルートとコントローラ アクションに割り当てることができます。

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
Laravel には、Web ルートや API ルートに適用できる一般的なミドルウェアを含む、事前定義された `web` および `api` ミドルウェア グループが含まれています。 Laravel は、これらのミドルウェア グループを、対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用することに注意してください。

<div class="overflow-auto">

<!-- | The `web` Middleware Group | | --------------------------------------------------------- | | `Illuminate\Cookie\Middleware\EncryptCookies` | | `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` | | `Illuminate\Session\Middleware\StartSession` | | `Illuminate\View\Middleware\ShareErrorsFromSession` | | `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` | | `Illuminate\Routing\Middleware\SubstituteBindings` | -->
| `web` ミドルウェア グループ                                |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

<!-- | The `api` Middleware Group | | -------------------------------------------------- | | `Illuminate\Routing\Middleware\SubstituteBindings` | -->
| `api` ミドルウェア グループ                         |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

<!-- If you would like to append or prepend middleware to these groups, you may use the `web` and `api` methods within your application's `bootstrap/app.php` file. The `web` and `api` methods are convenient alternatives to the `appendToGroup` method: -->
これらのグループにミドルウェアを追加または先頭に追加したい場合は、アプリケーションの `bootstrap/app.php` ファイル内で `web` および `api` メソッドを使用できます。 `web` メソッドと `api` メソッドは、`appendToGroup` メソッドの便利な代替手段です。

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
Laravel のデフォルトのミドルウェア グループ エントリの 1 つを独自のカスタム ミドルウェアに置き換えることもできます。

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

<!-- Or, you may remove a middleware entirely: -->
または、ミドルウェアを完全に削除することもできます。

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
<!-- #### Manually Managing Laravel's Default Middleware Groups -->
#### Manually Managing Laravel's Default Middleware Groups

<!-- If you would like to manually manage all of the middleware within Laravel's default `web` and `api` middleware groups, you may redefine the groups entirely. The example below will define the `web` and `api` middleware groups with their default middleware, allowing you to customize them as necessary: -->
Laravel のデフォルトの `web` および `api` ミドルウェア グループ内のすべてのミドルウェアを手動で管理したい場合は、グループ全体を再定義できます。以下の例では、`web` および `api` ミドルウェア グループをデフォルトのミドルウェアで定義し、必要に応じてカスタマイズできるようにします。

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
> デフォルトでは、`web` および `api` ミドルウェア グループは、`bootstrap/app.php` ファイルによって、アプリケーションの対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用されます。

<a name="middleware-aliases"></a>
<!-- ### Middleware Aliases -->
### Middleware Aliases

<!-- You may assign aliases to middleware in your application's `bootstrap/app.php` file. Middleware aliases allow you to define a short alias for a given middleware class, which can be especially useful for middleware with long class names: -->
アプリケーションの `bootstrap/app.php` ファイルでミドルウェアにエイリアスを割り当てることができます。ミドルウェア エイリアスを使用すると、特定のミドルウェア クラスに短いエイリアスを定義できます。これは、長いクラス名を持つミドルウェアに特に役立ちます。

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

<!-- Once the middleware alias has been defined in your application's `bootstrap/app.php` file, you may use the alias when assigning the middleware to routes: -->
アプリケーションの `bootstrap/app.php` ファイルでミドルウェア エイリアスを定義したら、ミドルウェアをルートに割り当てるときにそのエイリアスを使用できます。

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

<!-- For convenience, some of Laravel's built-in middleware are aliased by default. For example, the `auth` middleware is an alias for the `Illuminate\Auth\Middleware\Authenticate` middleware. Below is a list of the default middleware aliases: -->
便宜上、Laravel の組み込みミドルウェアの一部にはデフォルトでエイリアスが付けられています。たとえば、`auth` ミドルウェアは、`Illuminate\Auth\Middleware\Authenticate` ミドルウェアのエイリアスです。以下は、デフォルトのミドルウェア エイリアスのリストです。

<div class="overflow-auto">

<!-- | Alias | Middleware | | ------------------ | ------------------------------------------------------------------------------------------------------------- | | `auth` | `Illuminate\Auth\Middleware\Authenticate` | | `auth.basic` | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth` | | `auth.session` | `Illuminate\Session\Middleware\AuthenticateSession` | | `cache.headers` | `Illuminate\Http\Middleware\SetCacheHeaders` | | `can` | `Illuminate\Auth\Middleware\Authorize` | | `guest` | `Illuminate\Auth\Middleware\RedirectIfAuthenticated` | | `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword` | | `precognitive` | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests` | | `signed` | `Illuminate\Routing\Middleware\ValidateSignature` | | `subscribed` | `\Spark\Http\Middleware\VerifyBillableIsSubscribed` | | `throttle` | `Illuminate\Routing\Middleware\ThrottleRequests` or `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` | | `verified` | `Illuminate\Auth\Middleware\EnsureEmailIsVerified` | -->
| エイリアス              | ミドルウェア                                                                                                    |
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
| `throttle`         | `Illuminate\Routing\Middleware\ThrottleRequests` または `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`         | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`                                                            |

</div>

<a name="sorting-middleware"></a>
<!-- ### Sorting Middleware -->
### Sorting Middleware

<!-- Rarely, you may need your middleware to execute in a specific order but not have control over their order when they are assigned to the route. In these situations, you may specify your middleware priority using the `priority` method in your application's `bootstrap/app.php` file: -->
まれに、ミドルウェアを特定の順序で実行する必要があるが、ルートに割り当てられたときにその順序を制御できない場合があります。このような状況では、アプリケーションの `bootstrap/app.php` ファイルで `priority` メソッドを使用してミドルウェアの優先順位を指定できます。

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

<!-- If you would like to add middleware to the existing priority list without replacing it, you may use the `prependToPriorityList` or `appendToPriorityList` methods. The `prependToPriorityList` method inserts the given middleware before another middleware, while the `appendToPriorityList` method inserts it after another middleware: -->
既存の優先順位リストを置き換えずにミドルウェアを追加する場合は、`prependToPriorityList` メソッドまたは `appendToPriorityList` メソッドを使用できます。`prependToPriorityList` メソッドは指定したミドルウェアを別のミドルウェアの前に挿入し、`appendToPriorityList` メソッドは後に挿入します。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\EnsureTokenIsValid::class,
    );

    $middleware->appendToPriorityList(
        after: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        append: \App\Http\Middleware\EnsureUserIsSubscribed::class,
    );
})
```

<!-- The `before` and `after` arguments may also be an array of middleware classes. -->
`before` 引数と `after` 引数には、ミドルウェアクラスの配列を指定することもできます。

<a name="middleware-parameters"></a>
<!-- ## Middleware Parameters -->
## Middleware Parameters

<!-- Middleware can also receive additional parameters. For example, if your application needs to verify that the authenticated user has a given "role" before performing a given action, you could create an `EnsureUserHasRole` middleware that receives a role name as an additional argument. -->
ミドルウェアは追加のパラメーターを受け取ることもできます。たとえば、アプリケーションが特定のアクションを実行する前に、認証されたユーザーが特定の「ロール」を持っていることを確認する必要がある場合、追加の引数としてロール名を受け取る `EnsureUserHasRole` ミドルウェアを作成できます。

<!-- Additional middleware parameters will be passed to the middleware after the `$next` argument: -->
追加のミドルウェア パラメーターは、`$next` 引数の後にミドルウェアに渡されます。

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
ルートを定義するときに、ミドルウェア名とパラメーターを `:` で区切ることにより、ミドルウェア パラメーターを指定できます。

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

<!-- Multiple parameters may be delimited by commas: -->
複数のパラメータはカンマで区切ることができます。

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
<!-- ## Terminable Middleware -->
## Terminable Middleware

<!-- Sometimes a middleware may need to do some work after the HTTP response has been sent to the browser. If you define a `terminate` method on your middleware and your web server is using [FastCGI](https://www.php.net/manual/en/install.fpm.php), the `terminate` method will automatically be called after the response is sent to the browser: -->
場合によっては、HTTP 応答がブラウザーに送信された後にミドルウェアが何らかの作業を行う必要がある場合があります。ミドルウェアで `terminate` メソッドを定義し、Web サーバーが [FastCGI](https://www.php.net/manual/en/install.fpm.php) を使用している場合、応答がブラウザに送信された後、`terminate` メソッドが自動的に呼び出されます。

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
`terminate` メソッドは、リクエストとレスポンスの両方を受信する必要があります。終了可能なミドルウェアを定義したら、それをアプリケーションの `bootstrap/app.php` ファイル内のルートまたはグローバル ミドルウェアのリストに追加する必要があります。

<!-- When calling the `terminate` method on your middleware, Laravel will resolve a fresh instance of the middleware from the [service container](/docs/13.x/container). If you would like to use the same middleware instance when the `handle` and `terminate` methods are called, register the middleware with the container using the container's `singleton` method. Typically this should be done in the `register` method of your `AppServiceProvider`: -->
ミドルウェアで `terminate` メソッドを呼び出すと、Laravel は [service container](/docs/13.x/container) からミドルウェアの新しいインスタンスを解決します。 `handle` メソッドと `terminate` メソッドが呼び出されるときに同じミドルウェア インスタンスを使用したい場合は、コンテナーの `singleton` メソッドを使用してミドルウェアをコンテナーに登録します。通常、これは `AppServiceProvider` の `register` メソッドで実行する必要があります。

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
