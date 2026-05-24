# ミドルウェア (Middleware)

- [Introduction](#introduction)
- [ミドルウェアの定義](#defining-middleware)
- [ミドルウェアの登録](#registering-middleware)
    - [グローバルミドルウェア](#global-middleware)
    - [ルートへのミドルウェアの割り当て](#assigning-middleware-to-routes)
    - [ミドルウェアグループ](#middleware-groups)
    - [ミドルウェアのソート](#sorting-middleware)
- [ミドルウェアパラメータ](#middleware-parameters)
- [終了可能なミドルウェア](#terminable-middleware)

<a name="introduction"></a>
## 導入 (Introduction)

ミドルウェアは、アプリケーションに入る HTTP リクエストを検査およびフィルタリングするための便利なメカニズムを提供します。たとえば、Laravel には、アプリケーションのユーザーが認証されていることを確認するミドルウェアが含まれています。ユーザーが認証されていない場合、ミドルウェアはユーザーをアプリケーションのログイン画面にリダイレクトします。ただし、ユーザーが認証されている場合、ミドルウェアはリクエストがアプリケーション内にさらに進むことを許可します。

追加のミドルウェアを作成して、認証以外のさまざまなタスクを実行できます。たとえば、ログ ミドルウェアは、アプリケーションに受信したすべてのリクエストをログに記録する場合があります。 Laravel フレームワークには、認証や CSRF 保護用のミドルウェアなど、いくつかのミドルウェアが含まれています。これらのミドルウェアはすべて、`app/Http/Middleware` ディレクトリにあります。

<a name="defining-middleware"></a>
## ミドルウェアの定義 (Defining Middleware)

新しいミドルウェアを作成するには、`make:middleware` Artisan コマンドを使用します。

```shell
php artisan make:middleware EnsureTokenIsValid
```

このコマンドは、`app/Http/Middleware` ディレクトリ内に新しい `EnsureTokenIsValid` クラスを配置します。このミドルウェアでは、指定された `token` 入力が指定された値と一致する場合にのみルートへのアクセスを許可します。それ以外の場合は、ユーザーを `home` URI にリダイレクトします。

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

ご覧のとおり、指定された `token` がシークレット トークンと一致しない場合、ミドルウェアはクライアントに HTTP リダイレクトを返します。それ以外の場合、リクエストはさらにアプリケーションに渡されます。リクエストをアプリケーションのさらに奥深くに渡すには (ミドルウェアが「渡す」ことができるように)、`$request` を使用して `$next` コールバックを呼び出す必要があります。

ミドルウェアは、HTTP リクエストがアプリケーションに到達する前に通過する必要がある一連の「レイヤー」であると考えるのが最善です。各層はリクエストを検査し、完全に拒否することもできます。

> [!NOTE]  
> すべてのミドルウェアは [サービスコンテナ](/docs/{{version}}/container) 経由で解決されるため、ミドルウェアのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="middleware-and-responses"></a>
#### ミドルウェアとレスポンス

もちろん、ミドルウェアは、リクエストをアプリケーションの奥深くに渡す前または後にタスクを実行できます。たとえば、次のミドルウェアは、アプリケーションによってリクエストが処理される **前** に何らかのタスクを実行します。

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

ただし、このミドルウェアは、リクエストがアプリケーションによって処理された**後**にタスクを実行します。

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

<a name="registering-middleware"></a>
## ミドルウェアの登録 (Registering Middleware)

<a name="global-middleware"></a>
### グローバルミドルウェア

アプリケーションへのすべての HTTP リクエスト中にミドルウェアを実行する場合は、`app/Http/Kernel.php` クラスの `$middleware` プロパティにミドルウェア クラスをリストします。

<a name="assigning-middleware-to-routes"></a>
### ルートへのミドルウェアの割り当て

ミドルウェアを特定のルートに割り当てたい場合は、ルートを定義するときに `middleware` メソッドを呼び出すことができます。

    use App\Http\Middleware\Authenticate;

    Route::get('/profile', function () {
        // ...
    })->middleware(Authenticate::class);

ミドルウェア名の配列を `middleware` メソッドに渡すことで、ルートに複数のミドルウェアを割り当てることができます。

    Route::get('/', function () {
        // ...
    })->middleware([First::class, Second::class]);

便宜上、アプリケーションの `app/Http/Kernel.php` ファイル内のミドルウェアにエイリアスを割り当てることができます。デフォルトでは、このクラスの `$middlewareAliases` プロパティには、Laravel に含まれるミドルウェアのエントリが含まれています。独自のミドルウェアをこのリストに追加し、選択した別名を割り当てることができます。

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

ミドルウェアのエイリアスが HTTP カーネルで定義されたら、ミドルウェアをルートに割り当てるときにそのエイリアスを使用できます。

    Route::get('/profile', function () {
        // ...
    })->middleware('auth');

<a name="excluding-middleware"></a>
#### ミドルウェアを除く

ルートのグループにミドルウェアを割り当てる場合、グループ内の個々のルートにミドルウェアが適用されないようにする必要がある場合があります。これは、`withoutMiddleware` メソッドを使用して実行できます。

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::middleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/', function () {
            // ...
        });

        Route::get('/profile', function () {
            // ...
        })->withoutMiddleware([EnsureTokenIsValid::class]);
    });

特定のミドルウェアのセットをルート定義の [group](/docs/{{version}}/routing#route-groups) 全体から除外することもできます。

    use App\Http\Middleware\EnsureTokenIsValid;

    Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
        Route::get('/profile', function () {
            // ...
        });
    });

`withoutMiddleware` メソッドはルート ミドルウェアのみを削除でき、[グローバルミドルウェア](#global-middleware) には適用されません。

<a name="middleware-groups"></a>
### ミドルウェアグループ

ルートへの割り当てを容易にするために、複数のミドルウェアを 1 つのキーの下にグループ化したい場合があります。これは、HTTP カーネルの `$middlewareGroups` プロパティを使用して実行できます。

Laravel には、Web ルートや API ルートに適用できる一般的なミドルウェアを含む、事前定義された `web` および `api` ミドルウェア グループが含まれています。これらのミドルウェア グループは、アプリケーションの `App\Providers\RouteServiceProvider` サービスプロバイダによって、対応する `web` および `api` ルート ファイル内のルートに自動的に適用されることに注意してください。

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

ミドルウェア グループは、個々のミドルウェアと同じ構文を使用してルートとコントローラ アクションに割り当てることができます。繰り返しになりますが、ミドルウェア グループを使用すると、多くのミドルウェアを一度にルートに割り当てることがより便利になります。

    Route::get('/', function () {
        // ...
    })->middleware('web');

    Route::middleware(['web'])->group(function () {
        // ...
    });

> [!NOTE]  
> すぐに使用できる状態では、`web` および `api` ミドルウェア グループは、`App\Providers\RouteServiceProvider` によって、アプリケーションの対応する `routes/web.php` および `routes/api.php` ファイルに自動的に適用されます。

<a name="sorting-middleware"></a>
### ミドルウェアのソート

まれに、ミドルウェアを特定の順序で実行する必要があるが、ルートに割り当てられたときにその順序を制御できない場合があります。この場合、`app/Http/Kernel.php` ファイルの `$middlewarePriority` プロパティを使用してミドルウェアの優先順位を指定できます。このプロパティは、デフォルトでは HTTP カーネルに存在しない可能性があります。存在しない場合は、以下のデフォルトの定義をコピーできます。

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

<a name="middleware-parameters"></a>
## ミドルウェアパラメータ (Middleware Parameters)

ミドルウェアは追加のパラメーターを受け取ることもできます。たとえば、アプリケーションが特定のアクションを実行する前に、認証されたユーザーが特定の「ロール」を持っていることを確認する必要がある場合、追加の引数としてロール名を受け取る `EnsureUserHasRole` ミドルウェアを作成できます。

追加のミドルウェア パラメーターは、`$next` 引数の後にミドルウェアに渡されます。

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

ルートを定義するときに、ミドルウェア名とパラメーターを `:` で区切ることにより、ミドルウェア パラメーターを指定できます。

    Route::put('/post/{id}', function (string $id) {
        // ...
    })->middleware('role:editor');

複数のパラメータはカンマで区切ることができます。

    Route::put('/post/{id}', function (string $id) {
        // ...
    })->middleware('role:editor,publisher');

<a name="terminable-middleware"></a>
## 終了可能なミドルウェア (Terminable Middleware)

場合によっては、HTTP 応答がブラウザーに送信された後にミドルウェアが何らかの作業を行う必要がある場合があります。ミドルウェアで `terminate` メソッドを定義し、Web サーバーが FastCGI を使用している場合、応答がブラウザに送信された後、`terminate` メソッドが自動的に呼び出されます。

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

`terminate` メソッドは、リクエストとレスポンスの両方を受信する必要があります。終了可能なミドルウェアを定義したら、それを `app/Http/Kernel.php` ファイル内のルートまたはグローバル ミドルウェアのリストに追加する必要があります。

ミドルウェアで `terminate` メソッドを呼び出すと、Laravel は [サービスコンテナ](/docs/{{version}}/container) からミドルウェアの新しいインスタンスを解決します。 `handle` メソッドと `terminate` メソッドが呼び出されるときに同じミドルウェア インスタンスを使用したい場合は、コンテナーの `singleton` メソッドを使用してミドルウェアをコンテナーに登録します。通常、これは `AppServiceProvider` の `register` メソッドで実行する必要があります。

    use App\Http\Middleware\TerminatingMiddleware;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(TerminatingMiddleware::class);
    }

