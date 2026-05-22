# ミドルウェア (Middleware)

- [Introduction](#introduction)
- [ミドルウェアの定義](#defining-middleware)
- [ミドルウェアの登録](#registering-middleware)
    - [グローバルミドルウェア](#global-middleware)
    - [ルートへのミドルウェアの割り当て](#assigning-middleware-to-routes)
    - [ミドルウェアグループ](#middleware-groups)
    - [ミドルウェアのエイリアス](#middleware-aliases)
    - [ミドルウェアのソート](#sorting-middleware)
- [ミドルウェアパラメータ](#middleware-parameters)
- [終了可能なミドルウェア](#terminable-middleware)

<a name="introduction"></a>
## 導入 (Introduction)

ミドルウェアは、アプリケーションに入る HTTP リクエストを検査およびフィルタリングするための便利なメカニズムを提供します。たとえば、Laravel には、アプリケーションのユーザーが認証されていることを確認するミドルウェアが含まれています。ユーザーが認証されていない場合、ミドルウェアはユーザーをアプリケーションのログイン画面にリダイレクトします。ただし、ユーザーが認証されている場合、ミドルウェアはリクエストがアプリケーション内にさらに進むことを許可します。

追加のミドルウェアを作成して、認証以外のさまざまなタスクを実行できます。たとえば、ログ ミドルウェアは、アプリケーションに受信したすべてのリクエストをログに記録する場合があります。 Laravel には、認証や CSRF 保護用のミドルウェアなど、さまざまなミドルウェアが含まれています。ただし、ユーザー定義のミドルウェアはすべて、通常、アプリケーションの `app/Http/Middleware` ディレクトリにあります。

<a name="defining-middleware"></a>
## ミドルウェアの定義 (Defining Middleware)

新しいミドルウェアを作成するには、`make:middleware` Artisan コマンドを使用します。

```shell
php artisan make:middleware EnsureTokenIsValid
```

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

ご覧のとおり、指定された `token` がシークレット トークンと一致しない場合、ミドルウェアはクライアントに HTTP リダイレクトを返します。それ以外の場合、リクエストはさらにアプリケーションに渡されます。リクエストをアプリケーションのさらに奥深くに渡すには (ミドルウェアが「渡す」ことができるように)、`$request` を使用して `$next` コールバックを呼び出す必要があります。

ミドルウェアは、HTTP リクエストがアプリケーションに到達する前に通過する必要がある一連の「レイヤー」であると考えるのが最善です。各層はリクエストを検査し、完全に拒否することもできます。

> [!NOTE]
> すべてのミドルウェアは [サービスコンテナ](/docs/{{version}}/container) 経由で解決されるため、ミドルウェアのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="middleware-and-responses"></a>
#### ミドルウェアとレスポンス

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
## ミドルウェアの登録 (Registering Middleware)

<a name="global-middleware"></a>
### グローバルミドルウェア

アプリケーションへのすべての HTTP リクエスト中にミドルウェアを実行したい場合は、アプリケーションの `bootstrap/app.php` ファイル内のグローバル ミドルウェア スタックにミドルウェアを追加できます。

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```

`withMiddleware` クロージャーに提供される `$middleware` オブジェクトは、`Illuminate\Foundation\Configuration\Middleware` のインスタンスであり、アプリケーションのルートに割り当てられたミドルウェアを管理します。 `append` メソッドは、グローバル ミドルウェアのリストの最後にミドルウェアを追加します。リストの先頭にミドルウェアを追加したい場合は、`prepend` メソッドを使用する必要があります。

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravelのデフォルトのグローバルミドルウェアを手動で管理する

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
### ルートへのミドルウェアの割り当て

ミドルウェアを特定のルートに割り当てたい場合は、ルートを定義するときに `middleware` メソッドを呼び出すことができます。

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```

ミドルウェア名の配列を `middleware` メソッドに渡すことで、ルートに複数のミドルウェアを割り当てることができます。

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```

<a name="excluding-middleware"></a>
#### ミドルウェアを除く

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

特定のミドルウェアのセットをルート定義の [group](/docs/{{version}}/routing#route-groups) 全体から除外することもできます。

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```

`withoutMiddleware` メソッドはルート ミドルウェアのみを削除でき、[グローバルミドルウェア](#global-middleware) には適用されません。

<a name="middleware-groups"></a>
### ミドルウェアグループ

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
#### Laravelのデフォルトのミドルウェアグループ

Laravel には、Web ルートや API ルートに適用できる一般的なミドルウェアを含む、事前定義された `web` および `api` ミドルウェア グループが含まれています。 Laravel は、これらのミドルウェア グループを、対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用することに注意してください。

<div class="overflow-auto">

| `web` ミドルウェア グループ                                |
| --------------------------------------------------------- |
| `Illuminate\Cookie\Middleware\EncryptCookies`             |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`              |
| `Illuminate\View\Middleware\ShareErrorsFromSession`       |
| `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` |
| `Illuminate\Routing\Middleware\SubstituteBindings`        |

</div>

<div class="overflow-auto">

| `api` ミドルウェア グループ                         |
| -------------------------------------------------- |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

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

Laravel のデフォルトのミドルウェア グループ エントリの 1 つを独自のカスタム ミドルウェアに置き換えることもできます。

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```

または、ミドルウェアを完全に削除することもできます。

```php
$middleware->web(remove: [
    StartSession::class,
]);
```

<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravelのデフォルトのミドルウェアグループを手動で管理する

Laravel のデフォルトの `web` および `api` ミドルウェア グループ内のすべてのミドルウェアを手動で管理したい場合は、グループ全体を再定義できます。以下の例では、`web` および `api` ミドルウェア グループをデフォルトのミドルウェアで定義し、必要に応じてカスタマイズできるようにします。

```php
->withMiddleware(function (Middleware $middleware): void {
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
> デフォルトでは、`web` および `api` ミドルウェア グループは、`bootstrap/app.php` ファイルによって、アプリケーションの対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用されます。

<a name="middleware-aliases"></a>
### ミドルウェアのエイリアス

アプリケーションの `bootstrap/app.php` ファイルでミドルウェアにエイリアスを割り当てることができます。ミドルウェア エイリアスを使用すると、特定のミドルウェア クラスに短いエイリアスを定義できます。これは、長いクラス名を持つミドルウェアに特に役立ちます。

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```

アプリケーションの `bootstrap/app.php` ファイルでミドルウェア エイリアスを定義したら、ミドルウェアをルートに割り当てるときにそのエイリアスを使用できます。

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```

便宜上、Laravel の組み込みミドルウェアの一部にはデフォルトでエイリアスが付けられています。たとえば、`auth` ミドルウェアは、`Illuminate\Auth\Middleware\Authenticate` ミドルウェアのエイリアスです。以下は、デフォルトのミドルウェア エイリアスのリストです。

<div class="overflow-auto">

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
### ミドルウェアのソート

まれに、ミドルウェアを特定の順序で実行する必要があるが、ルートに割り当てられたときにその順序を制御できない場合があります。このような状況では、アプリケーションの `bootstrap/app.php` ファイルで `priority` メソッドを使用してミドルウェアの優先順位を指定できます。

```php
->withMiddleware(function (Middleware $middleware): void {
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
## ミドルウェアパラメータ (Middleware Parameters)

ミドルウェアは追加のパラメーターを受け取ることもできます。たとえば、アプリケーションが特定のアクションを実行する前に、認証されたユーザーが特定の「ロール」を持っていることを確認する必要がある場合、追加の引数としてロール名を受け取る `EnsureUserHasRole` ミドルウェアを作成できます。

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

ルートを定義するときに、ミドルウェア名とパラメーターを `:` で区切ることにより、ミドルウェア パラメーターを指定できます。

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```

複数のパラメータはカンマで区切ることができます。

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```

<a name="terminable-middleware"></a>
## 終了可能なミドルウェア (Terminable Middleware)

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

`terminate` メソッドは、リクエストとレスポンスの両方を受信する必要があります。終了可能なミドルウェアを定義したら、それをアプリケーションの `bootstrap/app.php` ファイル内のルートまたはグローバル ミドルウェアのリストに追加する必要があります。

ミドルウェアで `terminate` メソッドを呼び出すと、Laravel は [サービスコンテナ](/docs/{{version}}/container) からミドルウェアの新しいインスタンスを解決します。 `handle` メソッドと `terminate` メソッドが呼び出されるときに同じミドルウェア インスタンスを使用したい場合は、コンテナーの `singleton` メソッドを使用してミドルウェアをコンテナーに登録します。通常、これは `AppServiceProvider` の `register` メソッドで実行する必要があります。

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

