# ルーティング (Routing)

- [基本的なルーティング](#basic-routing)
    - [デフォルトルートファイル](#the-default-route-files)
    - [リダイレクトルート](#redirect-routes)
    - [ルートを見る](#view-routes)
    - [ルートをリストする](#listing-your-routes)
    - [ルーティングのカスタマイズ](#routing-customization)
- [ルートパラメータ](#route-parameters)
    - [必須パラメータ](#required-parameters)
    - [オプションのパラメータ](#parameters-optional-parameters)
    - [正規表現の制約](#parameters-regular-expression-constraints)
- [名前付きルート](#named-routes)
- [ルートグループ](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Controllers](#route-group-controllers)
    - [サブドメインルーティング](#route-group-subdomain-routing)
    - [ルートプレフィックス](#route-group-prefixes)
    - [ルート名のプレフィックス](#route-group-name-prefixes)
- [ルートモデルバインディング](#route-model-binding)
    - [暗黙的なバインド](#implicit-binding)
    - [暗黙的な列挙型バインディング](#implicit-enum-binding)
    - [明示的なバインディング](#explicit-binding)
- [フォールバックルート](#fallback-routes)
- [レート制限](#rate-limiting)
    - [レートリミッターの定義](#defining-rate-limiters)
    - [ルートへのレート リミッターの適用](#attaching-rate-limiters-to-routes)
- [フォームメソッドのスプーフィング](#form-method-spoofing)
- [現在のルートへのアクセス](#accessing-the-current-route)
- [クロスオリジンリソース共有 (CORS)](#cors)
- [ルートキャッシュ](#route-caching)

<a name="basic-routing"></a>
## 基本的なルーティング (Basic Routing)

最も基本的な Laravel ルートは URI とクロージャを受け入れ、複雑なルーティング設定ファイルを使用せずにルートと動作を定義する非常にシンプルで表現力豊かな方法を提供します。

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### デフォルトルートファイル

すべての Laravel ルートは、`routes` ディレクトリにあるルート ファイルで定義されます。これらのファイルは、アプリケーションの `bootstrap/app.php` ファイルで指定された構成を使用して、Laravel によって自動的にロードされます。 `routes/web.php` ファイルは、Web インターフェイスのルートを定義します。これらのルートには、`web` [ミドルウェアグループ](/docs/{{version}}/middleware#laravels-default-middleware-groups) が割り当てられ、セッション状態や CSRF 保護などの機能が提供されます。

ほとんどのアプリケーションでは、`routes/web.php` ファイルでルートを定義することから始めます。 `routes/web.php` で定義されたルートには、定義されたルートの URL をブラウザに入力することでアクセスできます。たとえば、ブラウザで `http://example.com/user` に移動すると、次のルートにアクセスできます。

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### APIルート

アプリケーションがステートレス API も提供する場合は、`install:api` Artisan コマンドを使用して API ルーティングを有効にすることができます。

```shell
php artisan install:api
```

`install:api` コマンドは、[Laravel Sanctum](/docs/{{version}}/sanctum) をインストールします。これは、サードパーティ API コンシューマ、SPA、またはモバイル アプリケーションの認証に使用できる、堅牢かつシンプルな API トークン認証ガードを提供します。さらに、`install:api` コマンドは、`routes/api.php` ファイルを作成します。

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

もちろん、パブリックにアクセスできる必要があるルート上の `auth:sanctum` ミドルウェアを自由に省略できます。

`routes/api.php` のルートはステートレスで、`api` [ミドルウェアグループ](/docs/{{version}}/middleware#laravels-default-middleware-groups) に割り当てられます。さらに、`/api` URI プレフィックスはこれらのルートに自動的に適用されるため、ファイル内のすべてのルートに手動でプレフィックスを適用する必要はありません。アプリケーションの `bootstrap/app.php` ファイルを変更することで、プレフィックスを変更できます。

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 利用可能なルーター方式

ルーターを使用すると、任意の HTTP 動詞に応答するルートを登録できます。

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

場合によっては、複数の HTTP 動詞に応答するルートを登録する必要があるかもしれません。これは、`match` メソッドを使用して行うことができます。または、`any` メソッドを使用して、すべての HTTP 動詞に応答するルートを登録することもできます。

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 同じ URI を共有する複数のルートを定義する場合は、`get`、`post`、`put`、`patch`、`delete`、および `options` メソッドを使用するルートを、`any`、`match`、および`redirect` メソッド。これにより、受信リクエストが正しいルートと一致することが保証されます。

<a name="dependency-injection"></a>
#### 依存関係の注入

ルートのコールバック署名で、ルートに必要な依存関係をタイプヒントで指定できます。宣言された依存関係は自動的に解決され、Laravel [サービスコンテナ](/docs/{{version}}/container) によってコールバックに挿入されます。たとえば、`Illuminate\Http\Request` クラスにタイプヒントを指定して、現在の HTTP リクエストをルート コールバックに自動的に挿入できます。

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF保護

`web` ルート ファイルで定義されている `POST`、`PUT`、`PATCH`、または `DELETE` ルートを指す HTML フォームには、CSRF トークン フィールドが含まれている必要があることに注意してください。それ以外の場合、リクエストは拒否されます。 CSRF 保護の詳細については、[CSRF ドキュメント](/docs/{{version}}/csrf) を参照してください。

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### リダイレクトルート

別の URI にリダイレクトするルートを定義している場合は、`Route::redirect` メソッドを使用できます。このメソッドは便利なショートカットを提供するため、単純なリダイレクトを実行するために完全なルートまたはコントローラを定義する必要はありません。

```php
Route::redirect('/here', '/there');
```

デフォルトでは、`Route::redirect` は `302` ステータス コードを返します。オプションの 3 番目のパラメータを使用してステータス コードをカスタマイズできます。

```php
Route::redirect('/here', '/there', 301);
```

または、`Route::permanentRedirect` メソッドを使用して、`301` ステータス コードを返すこともできます。

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> リダイレクトルートでルートパラメータを使用する場合、`destination`および`status`パラメータはLaravelによって予約されているため使用できません。

<a name="view-routes"></a>
### ルートを見る

ルートが [view](/docs/{{version}}/views) を返すだけでよい場合は、`Route::view` メソッドを使用できます。 `redirect` メソッドと同様に、このメソッドは単純なショートカットを提供するため、完全なルートまたはコントローラを定義する必要はありません。 `view` メソッドは、最初の引数として URI を、2 番目の引数としてビュー名を受け入れます。さらに、オプションの 3 番目の引数としてビューに渡すデータの配列を指定できます。

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> ビュールートでルートパラメーターを使用する場合、`view`、`data`、`status`、および `headers` のパラメーターは Laravel によって予約されているため使用できません。

<a name="listing-your-routes"></a>
### ルートをリストする

`route:list` Artisan コマンドを使用すると、アプリケーションによって定義されているすべてのルートの概要を簡単に提供できます。

```shell
php artisan route:list
```

デフォルトでは、各ルートに割り当てられたルート ミドルウェアは `route:list` 出力には表示されません。ただし、コマンドに `-v` オプションを追加することで、ルートミドルウェアとミドルウェアグループの名前を表示するように Laravel に指示できます。

```shell
php artisan route:list -v

# Expand middleware groups...
php artisan route:list -vv
```

特定の URI で始まるルートのみを表示するように Laravel に指示することもできます。

```shell
php artisan route:list --path=api
```

さらに、`route:list` コマンドの実行時に `--except-vendor` オプションを指定することで、サードパーティのパッケージによって定義されたルートを非表示にするように Laravel に指示することもできます。

```shell
php artisan route:list --except-vendor
```

同様に、`route:list` コマンドの実行時に `--only-vendor` オプションを指定することで、サードパーティのパッケージによって定義されたルートのみを表示するように Laravel に指示することもできます。

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### ルーティングのカスタマイズ

デフォルトでは、アプリケーションのルートは `bootstrap/app.php` ファイルによって構成およびロードされます。

```php
<?php

use Illuminate\Foundation\Application;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )->create();
```

ただし、アプリケーションのルートのサブセットを含めるために、まったく新しいファイルを定義したい場合もあります。これを実現するには、`then` クロージャーを `withRouting` メソッドに提供します。このクロージャ内で、アプリケーションに必要な追加のルートを登録できます。

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
    then: function () {
        Route::middleware('api')
            ->prefix('webhooks')
            ->name('webhooks.')
            ->group(base_path('routes/webhooks.php'));
    },
)
```

または、`using` クロージャーを `withRouting` メソッドに提供することで、ルート登録を完全に制御することもできます。この引数が渡されると、HTTP ルートはフレームワークによって登録されないため、すべてのルートを手動で登録する必要があります。

```php
use Illuminate\Support\Facades\Route;

->withRouting(
    commands: __DIR__.'/../routes/console.php',
    using: function () {
        Route::middleware('api')
            ->prefix('api')
            ->group(base_path('routes/api.php'));

        Route::middleware('web')
            ->group(base_path('routes/web.php'));
    },
)
```

<a name="route-parameters"></a>
## ルートパラメータ (Route Parameters)

<a name="required-parameters"></a>
### 必須パラメータ

場合によっては、ルート内の URI のセグメントをキャプチャする必要があります。たとえば、URL からユーザー ID を取得する必要がある場合があります。これを行うには、ルート パラメーターを定義します。

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

ルートに必要な数のルート パラメータを定義できます。

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

ルート パラメーターは常に `{}` 中括弧で囲まれ、アルファベット文字で構成されている必要があります。ルート パラメーター名内ではアンダースコア (`_`) も使用できます。ルート パラメーターは、その順序に基づいてルート コールバック/コントローラに挿入されます。ルート コールバック/コントローラ引数の名前は関係ありません。

<a name="parameters-and-dependency-injection"></a>
#### パラメータと依存関係の注入

Laravel サービスコンテナがルートのコールバックに自動的に挿入する依存関係がルートにある場合は、依存関係の後にルートパラメーターをリストする必要があります。

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### オプションのパラメータ

場合によっては、URI に常に存在するとは限らないルート パラメーターの指定が必要になることがあります。これを行うには、パラメータ名の後に `?` マークを付けます。ルートの対応する変数にデフォルト値を指定してください。

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 正規表現の制約

ルート インスタンスで `where` メソッドを使用して、ルート パラメーターの形式を制限できます。 `where` メソッドは、パラメーターの名前と、パラメーターを制約する方法を定義する正規表現を受け入れます。

```php
Route::get('/user/{name}', function (string $name) {
    // ...
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function (string $id) {
    // ...
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

便宜上、一般的に使用される一部の正規表現パターンには、パターン制約をルートにすばやく追加できるヘルパ メソッドが用意されています。

```php
Route::get('/user/{id}/{name}', function (string $id, string $name) {
    // ...
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function (string $name) {
    // ...
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUuid('id');

Route::get('/user/{id}', function (string $id) {
    // ...
})->whereUlid('id');

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', ['movie', 'song', 'painting']);

Route::get('/category/{category}', function (string $category) {
    // ...
})->whereIn('category', CategoryEnum::cases());
```

受信リクエストがルート パターン制約と一致しない場合、404 HTTP 応答が返されます。

<a name="parameters-global-constraints"></a>
#### グローバル制約

ルート パラメーターを常に特定の正規表現によって制限したい場合は、`pattern` メソッドを使用できます。これらのパターンは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドで定義する必要があります。

```php
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::pattern('id', '[0-9]+');
}
```

パターンが定義されると、そのパラメータ名を使用してすべてのルートに自動的に適用されます。

```php
Route::get('/user/{id}', function (string $id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### エンコードされたスラッシュ

Laravel ルーティングコンポーネントでは、`/` を除くすべての文字がルートパラメーター値内に存在することが許可されます。 `where` 条件正規表現を使用して、`/` をプレースホルダーの一部として明示的に許可する必要があります。

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> エンコードされたスラッシュは、最後のルート セグメント内でのみサポートされます。

<a name="named-routes"></a>
## 名前付きルート (Named Routes)

名前付きルートを使用すると、特定のルートの URL またはリダイレクトを簡単に生成できます。ルート定義に `name` メソッドを連鎖させることで、ルートの名前を指定できます。

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

コントローラアクションのルート名を指定することもできます。

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> ルート名は常に一意である必要があります。

<a name="generating-urls-to-named-routes"></a>
#### 名前付きルートへの URL の生成

特定のルートに名前を割り当てたら、Laravel の `route` および `redirect` ヘルパ関数を介して URL またはリダイレクトを生成するときにルートの名前を使用できます。

```php
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');

return to_route('profile');
```

名前付きルートがパラメーターを定義している場合、そのパラメーターを 2 番目の引数として `route` 関数に渡すことができます。指定されたパラメータは、生成された URL の正しい位置に自動的に挿入されます。

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

追加のパラメーターを配列で渡すと、それらのキーと値のペアが、生成された URL のクエリ文字列に自動的に追加されます。

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> 現在のロケールなど、URL パラメータにリクエスト全体のデフォルト値を指定したい場合があります。これを実現するには、[URL::defaults method](/docs/{{version}}/urls#default-values) を使用できます。

<a name="inspecting-the-current-route"></a>
#### 現在のルートの検査

現在のリクエストが特定の名前付きルートにルーティングされたかどうかを確認したい場合は、Route インスタンスで `named` メソッドを使用できます。たとえば、ルート ミドルウェアから現在のルート名を確認できます。

```php
use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

/**
 * Handle an incoming request.
 *
 * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
 */
public function handle(Request $request, Closure $next): Response
{
    if ($request->route()->named('profile')) {
        // ...
    }

    return $next($request);
}
```

<a name="route-groups"></a>
## ルートグループ (Route Groups)

ルート グループを使用すると、個別のルートごとにミドルウェアなどのルート属性を定義することなく、多数のルート間でルート属性を共有できます。

ネストされたグループは、属性をその親グループとインテリジェントに「マージ」しようとします。ミドルウェアと `where` 条件はマージされ、名前とプレフィックスが追加されます。名前空間の区切り文字と URI 接頭辞のスラッシュは、必要に応じて自動的に追加されます。

<a name="route-group-middleware"></a>
### ミドルウェア

グループ内のすべてのルートに [middleware](/docs/{{version}}/middleware) を割り当てるには、グループを定義する前に `middleware` メソッドを使用できます。ミドルウェアは、配列にリストされている順序で実行されます。

```php
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // Uses first & second middleware...
    });

    Route::get('/user/profile', function () {
        // Uses first & second middleware...
    });
});
```

<a name="route-group-controllers"></a>
### コントローラ

ルートのグループがすべて同じ [controller](/docs/{{version}}/controllers) を使用する場合、`controller` メソッドを使用して、グループ内のすべてのルートに共通のコントローラを定義できます。次に、ルートを定義するときに、ルートが呼び出すコントローラ メソッドを指定するだけで済みます。

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### サブドメインルーティング

ルート グループは、サブドメイン ルーティングを処理するために使用することもできます。サブドメインには、ルート URI と同様にルート パラメーターを割り当てることができ、ルートまたはコントローラで使用するためにサブドメインの一部をキャプチャできるようになります。サブドメインは、グループを定義する前に `domain` メソッドを呼び出すことで指定できます。

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

> [!WARNING]
> サブドメイン ルートに確実に到達できるようにするには、ルート ドメイン ルートを登録する前にサブドメイン ルートを登録する必要があります。これにより、ルート ドメイン ルートが同じ URI パスを持つサブドメイン ルートを上書きすることがなくなります。

<a name="route-group-prefixes"></a>
### ルートプレフィックス

`prefix` メソッドを使用して、グループ内の各ルートに特定の URI をプレフィックスとして付けることができます。たとえば、グループ内のすべてのルート URI に `admin` というプレフィックスを付けることができます。

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a name="route-group-name-prefixes"></a>
### ルート名のプレフィックス

`name` メソッドを使用して、グループ内の各ルート名に特定の文字列をプレフィックスとして付けることができます。たとえば、グループ内のすべてのルートの名前に `admin` というプレフィックスを付けることができます。指定された文字列は、指定されたとおりにルート名にプレフィックスとして付けられるため、プレフィックスの末尾に `.` 文字を必ず指定します。

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## ルートモデルバインディング (Route Model Binding)

モデル ID をルートまたはコントローラ アクションに挿入する場合、多くの場合、データベースにクエリを実行して、その ID に対応するモデルを取得します。 Laravel ルート モデル バインディングは、モデル インスタンスをルートに直接自動的に挿入する便利な方法を提供します。たとえば、ユーザーの ID を注入する代わりに、指定された ID に一致する `User` モデル インスタンス全体を注入できます。

<a name="implicit-binding"></a>
### 暗黙的なバインド

Laravel は、タイプヒンテッド変数名がルートセグメント名と一致するルートまたはコントローラアクションで定義された Eloquent モデルを自動的に解決します。例えば：

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 変数は `App\Models\User` Eloquent モデルとしてタイプヒントされており、変数名は `{user}` URI セグメントと一致するため、Laravel はリクエスト URI の対応する値に一致する ID を持つモデル インスタンスを自動的に挿入します。一致するモデル インスタンスがデータベース内に見つからない場合、404 HTTP 応答が自動的に生成されます。

もちろん、コントローラ メソッドを使用する場合は、暗黙的なバインディングも可能です。繰り返しますが、`{user}` URI セグメントは、`App\Models\User` タイプ ヒントを含むコントローラ内の `$user` 変数と一致することに注意してください。

```php
use App\Http\Controllers\UserController;
use App\Models\User;

// Route definition...
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller method definition...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
#### ソフト削除されたモデル

通常、暗黙的なモデル バインディングでは、[ソフト削除されました](/docs/{{version}}/eloquent#soft-deleting) になったモデルは取得されません。ただし、ルートの定義に `withTrashed` メソッドをチェーンすることで、これらのモデルを取得するように暗黙的バインディングに指示できます。

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### キーのカスタマイズ

場合によっては、`id` 以外の列を使用して Eloquent モデルを解決したい場合があります。これを行うには、ルート パラメーター定義で列を指定できます。

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

特定のモデル クラスを取得するときに、モデル バインディングで常に `id` 以外のデータベース列を使用するようにしたい場合は、Eloquent モデルで `getRouteKeyName` メソッドをオーバーライドできます。

```php
/**
 * Get the route key for the model.
 */
public function getRouteKeyName(): string
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
#### カスタムキーとスコープ

単一のルート定義で複数の Eloquent モデルを暗黙的にバインドする場合、前の Eloquent モデルの子である必要があるように 2 番目の Eloquent モデルのスコープを設定したい場合があります。たとえば、特定のユーザーのスラッグによってブログ投稿を取得する次のルート定義について考えてみましょう。

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。この場合、`User` モデルには、`Post` モデルを取得するために使用できる `posts` (ルート パラメーター名の複数形) という名前のリレーションシップがあると想定されます。

必要に応じて、カスタムキーが提供されていない場合でも、Laravel に「子」バインディングのスコープを設定するように指示できます。これを行うには、ルートを定義するときに `scopeBindings` メソッドを呼び出します。

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

または、ルート定義のグループ全体にスコープ付きバインディングを使用するように指示することもできます。

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

同様に、`withoutScopedBindings` メソッドを呼び出して、バインディングをスコープしないように Laravel に明示的に指示することもできます。

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 欠落モデルの動作のカスタマイズ

通常、暗黙的にバインドされたモデルが見つからない場合は、404 HTTP 応答が生成されます。ただし、ルートを定義するときに `missing` メソッドを呼び出すことで、この動作をカスタマイズできます。 `missing` メソッドは、暗黙的にバインドされたモデルが見つからない場合に呼び出されるクロージャを受け入れます。

```php
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
    ->name('locations.view')
    ->missing(function (Request $request) {
        return Redirect::route('locations.index');
    });
```

<a name="implicit-enum-binding"></a>
### 暗黙的な列挙型バインディング

PHP 8.1 では、[Enums](https://www.php.net/manual/en/language.enumerations.backed.php) のサポートが導入されました。この機能を補完するために、Laravel ではルート定義で [Enums](https://www.php.net/manual/en/language.enumerations.backed.php) をタイプヒントできるようになり、Laravel はそのルートセグメントが有効な Enum 値に対応する場合にのみルートを呼び出します。それ以外の場合は、404 HTTP 応答が自動的に返されます。たとえば、次の列挙型があるとします。

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

`{category}` ルート セグメントが `fruits` または `people` の場合にのみ呼び出されるルートを定義できます。それ以外の場合、Laravel は 404 HTTP 応答を返します。

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 明示的なバインディング

モデルバインディングを使用するために、Laravel の暗黙的な規約ベースのモデル解決を使用する必要はありません。ルート パラメーターがモデルにどのように対応するかを明示的に定義することもできます。明示的なバインディングを登録するには、ルーターの `model` メソッドを使用して、特定のパラメーターのクラスを指定します。 `AppServiceProvider` クラスの `boot` メソッドの先頭で明示的なモデル バインディングを定義する必要があります。

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::model('user', User::class);
}
```

次に、`{user}` パラメーターを含むルートを定義します。

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

すべての `{user}` パラメーターを `App\Models\User` モデルにバインドしているため、そのクラスのインスタンスがルートに挿入されます。したがって、たとえば、`users/1` へのリクエストは、`1` の ID を持つデータベースから `User` インスタンスを挿入します。

一致するモデル インスタンスがデータベース内に見つからない場合、404 HTTP 応答が自動的に生成されます。

<a name="customizing-the-resolution-logic"></a>
#### 解決ロジックのカスタマイズ

独自のモデル バインディング解決ロジックを定義したい場合は、`Route::bind` メソッドを使用できます。 `bind` メソッドに渡すクロージャは、URI セグメントの値を受け取り、ルートに挿入されるクラスのインスタンスを返す必要があります。繰り返しますが、このカスタマイズは、アプリケーションの `AppServiceProvider` の `boot` メソッドで行う必要があります。

```php
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::bind('user', function (string $value) {
        return User::where('name', $value)->firstOrFail();
    });
}
```

あるいは、Eloquent モデルの `resolveRouteBinding` メソッドをオーバーライドすることもできます。このメソッドは URI セグメントの値を受け取り、ルートに挿入されるクラスのインスタンスを返す必要があります。

```php
/**
 * Retrieve the model for a bound value.
 *
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

ルートが [暗黙的なバインディングのスコープ設定](#implicit-model-binding-scoping) を利用している場合、親モデルの子バインディングを解決するために `resolveChildRouteBinding` メソッドが使用されます。

```php
/**
 * Retrieve the child model for a bound value.
 *
 * @param  string  $childType
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

<a name="fallback-routes"></a>
## フォールバックルート (Fallback Routes)

`Route::fallback` メソッドを使用すると、受信リクエストに一致するルートが他にない場合に実行されるルートを定義できます。通常、未処理のリクエストは、アプリケーションの例外ハンドラーを介して自動的に「404」ページをレンダリングします。ただし、通常は `routes/web.php` ファイル内で `fallback` ルートを定義するため、`web` ミドルウェア グループ内のすべてのミドルウェアがルートに適用されます。必要に応じて、このルートにミドルウェアを自由に追加できます。

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## レート制限 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### レートリミッターの定義

Laravel には、特定のルートまたはルートのグループのトラフィック量を制限するために利用できる、強力でカスタマイズ可能なレート制限サービスが含まれています。まず、アプリケーションのニーズを満たすレート リミッター構成を定義する必要があります。

レート リミッターは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッド内で定義できます。

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。 `for` メソッドは、レート リミッター名と、レート リミッターに割り当てられたルートに適用される制限構成を返すクロージャを受け入れます。制限構成は、`Illuminate\Cache\RateLimiting\Limit` クラスのインスタンスです。このクラスには、制限をすばやく定義できるようにする便利な「ビルダ」メソッドが含まれています。レート リミッタ名には、任意の文字列を指定できます。

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

受信リクエストが指定されたレート制限を超える場合、429 HTTP ステータス コードを含むレスポンスが Laravel によって自動的に返されます。レート制限によって返される独自の応答を定義したい場合は、`response` メソッドを使用できます。

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

レート リミッター コールバックは受信 HTTP リクエスト インスタンスを受け取るため、受信リクエストまたは認証されたユーザーに基づいて適切なレート制限を動的に構築できます。

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### セグメント化レート制限

場合によっては、レート制限を任意の値で分割したい場合があります。たとえば、ユーザーが IP アドレスごとに 1 分あたり 100 回、特定のルートにアクセスできるようにしたい場合があります。これを実現するには、レート制限を構築するときに `by` メソッドを使用します。

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

別の例を使用してこの機能を説明すると、ルートへのアクセスを、認証されたユーザー ID ごとに 1 分あたり 100 回、またはゲストの IP アドレスごとに 1 分あたり 10 回に制限できます。

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 複数のレート制限

必要に応じて、特定のレート リミッター構成のレート制限の配列を返すことができます。各レート制限は、配列内に配置された順序に基づいてルートに対して評価されます。

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

同一の `by` 値でセグメント化された複数のレート制限を割り当てる場合は、各 `by` 値が一意であることを確認する必要があります。これを実現する最も簡単な方法は、`by` メソッドに指定する値にプレフィックスを付けることです。

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### 応答ベースのレート制限

受信リクエストのレート制限に加えて、Laravel では、`after` メソッドを使用してレスポンスに基づいてレート制限を行うことができます。これは、検証エラー、404 応答、その他の特定の HTTP ステータス コードなど、特定の応答のみをレート制限にカウントしたい場合に便利です。

`after` メソッドは、応答を受け取るクロージャを受け入れ、応答をレート制限にカウントする必要がある場合は `true` を返し、無視する必要がある場合は `false` を返す必要があります。これは、連続する 404 応答を制限することによって列挙型攻撃を防止したり、成功した操作のみを制限するエンドポイントのレート制限を使い果たさずに検証に失敗したリクエストをユーザーが再試行できるようにする場合に特に役立ちます。

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Symfony\Component\HttpFoundation\Response;

RateLimiter::for('resource-not-found', function (Request $request) {
    return Limit::perMinute(10)
        ->by($request->user()?->id ?: $request->ip())
        ->after(function (Response $response) {
            // Only count 404 responses toward the rate limit to prevent enumeration...
            return $response->status() === 404;
        });
});
```

<a name="attaching-rate-limiters-to-routes"></a>
### ルートへのレート リミッターの適用

レート リミッターは、`throttle` [middleware](/docs/{{version}}/middleware) を使用してルートまたはルート グループに接続できます。スロットル ミドルウェアは、ルートに割り当てるレート リミッターの名前を受け入れます。

```php
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        // ...
    });

    Route::post('/video', function () {
        // ...
    });
});
```

<a name="throttling-with-redis"></a>
#### Redis を使用したスロットリング

デフォルトでは、`throttle` ミドルウェアは `Illuminate\Routing\Middleware\ThrottleRequests` クラスにマップされます。ただし、アプリケーションのキャッシュドライバとして Redis を使用している場合は、レート制限を管理するために Redis を使用するように Laravel に指示することもできます。これを行うには、アプリケーションの `bootstrap/app.php` ファイルで `throttleWithRedis` メソッドを使用する必要があります。このメソッドは、`throttle` ミドルウェアを `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` ミドルウェア クラスにマップします。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## フォームメソッドのスプーフィング (Form Method Spoofing)

HTML フォームは、`PUT`、`PATCH`、または `DELETE` アクションをサポートしません。したがって、HTML フォームから呼び出される `PUT`、`PATCH`、または `DELETE` ルートを定義する場合は、非表示の `_method` フィールドをフォームに追加する必要があります。 `_method` フィールドで送信された値は、HTTP リクエスト メソッドとして使用されます。

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

便宜上、`@method` [Blade ディレクティブ](/docs/{{version}}/blade) を使用して、`_method` 入力フィールドを生成できます。

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 現在のルートへのアクセス (Accessing the Current Route)

`Route` ファサードで `current`、`currentRouteName`、および `currentRouteAction` メソッドを使用して、受信リクエストを処理するルートに関する情報にアクセスできます。

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

[Route ファサードの基になるクラス](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) と [ルートインスタンス](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Route.html) の両方の API ドキュメントを参照して、ルーターとルート クラスで使用できるすべてのメソッドを確認してください。

<a name="cors"></a>
## クロスオリジンリソース共有 (CORS) (Cross-Origin Resource Sharing (CORS))

Laravel は、設定した値を使用して CORS `OPTIONS` HTTP リクエストに自動的に応答できます。 `OPTIONS` リクエストは、アプリケーションのグローバル ミドルウェア スタックに自動的に含まれる `HandleCors` [middleware](/docs/{{version}}/middleware) によって自動的に処理されます。

場合によっては、アプリケーションの CORS 構成値のカスタマイズが必要になる場合があります。これを行うには、`config:publish` Artisan コマンドを使用して `cors` 構成ファイルを公開します。

```shell
php artisan config:publish cors
```

このコマンドは、アプリケーションの `config` ディレクトリ内に `cors.php` 構成ファイルを配置します。

> [!NOTE]
> CORS および CORS ヘッダーの詳細については、[CORS に関する MDN Web ドキュメント](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers) を参照してください。

<a name="route-caching"></a>
## ルートキャッシュ (Route Caching)

アプリケーションを運用環境にデプロイするときは、Laravel のルート キャッシュを利用する必要があります。ルート キャッシュを使用すると、アプリケーションのすべてのルートを登録するのにかかる時間が大幅に短縮されます。ルート キャッシュを生成するには、`route:cache` Artisan コマンドを実行します。

```shell
php artisan route:cache
```

このコマンドを実行すると、キャッシュされたルート ファイルがリクエストごとにロードされます。新しいルートを追加する場合は、新しいルート キャッシュを生成する必要があることに注意してください。このため、`route:cache` コマンドはプロジェクトのデプロイメント中にのみ実行する必要があります。

`route:clear` コマンドを使用してルート キャッシュをクリアできます。

```shell
php artisan route:clear
```

