<!-- # Routing -->
# Routing

- [Basic Routing](#basic-routing)
    - [Redirect Routes](#redirect-routes)
    - [View Routes](#view-routes)
- [Route Parameters](#route-parameters)
    - [Required Parameters](#required-parameters)
    - [Optional Parameters](#parameters-optional-parameters)
    - [Regular Expression Constraints](#parameters-regular-expression-constraints)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Controllers](#route-group-controllers)
    - [Subdomain Routing](#route-group-subdomain-routing)
    - [Route Prefixes](#route-group-prefixes)
    - [Route Name Prefixes](#route-group-name-prefixes)
- [Route Model Binding](#route-model-binding)
    - [Implicit Binding](#implicit-binding)
    - [Explicit Binding](#explicit-binding)
- [Fallback Routes](#fallback-routes)
- [Rate Limiting](#rate-limiting)
    - [Defining Rate Limiters](#defining-rate-limiters)
    - [Attaching Rate Limiters To Routes](#attaching-rate-limiters-to-routes)
- [Form Method Spoofing](#form-method-spoofing)
- [Accessing The Current Route](#accessing-the-current-route)
- [Cross-Origin Resource Sharing (CORS)](#cors)
- [Route Caching](#route-caching)

<a name="basic-routing"></a>
<!-- ## Basic Routing -->
## Basic Routing

<!-- The most basic Laravel routes accept a URI and a closure, providing a very simple and expressive method of defining routes and behavior without complicated routing configuration files: -->
最も基本的な Laravel ルートは URI とクロージャを受け入れ、複雑なルーティング設定ファイルを使用せずにルートと動作を定義する非常にシンプルで表現力豊かな方法を提供します。

```
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
<!-- #### The Default Route Files -->
#### The Default Route Files

<!-- All Laravel routes are defined in your route files, which are located in the `routes` directory. These files are automatically loaded by your application's `App\Providers\RouteServiceProvider`. The `routes/web.php` file defines routes that are for your web interface. These routes are assigned the `web` middleware group, which provides features like session state and CSRF protection. The routes in `routes/api.php` are stateless and are assigned the `api` middleware group. -->
すべての Laravel ルートは、`routes` ディレクトリにあるルート ファイルで定義されます。これらのファイルは、アプリケーションの `App\Providers\RouteServiceProvider` によって自動的にロードされます。 `routes/web.php` ファイルは、Web インターフェイスのルートを定義します。これらのルートには、セッション状態や CSRF 保護などの機能を提供する `web` ミドルウェア グループが割り当てられます。 `routes/api.php` のルートはステートレスであり、`api` ミドルウェア グループに割り当てられます。

<!-- For most applications, you will begin by defining routes in your `routes/web.php` file. The routes defined in `routes/web.php` may be accessed by entering the defined route's URL in your browser. For example, you may access the following route by navigating to `http://example.com/user` in your browser: -->
ほとんどのアプリケーションでは、`routes/web.php` ファイルでルートを定義することから始めます。 `routes/web.php` で定義されたルートには、定義されたルートの URL をブラウザに入力することでアクセスできます。たとえば、ブラウザで `http://example.com/user` に移動すると、次のルートにアクセスできます。

```
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<!-- Routes defined in the `routes/api.php` file are nested within a route group by the `RouteServiceProvider`. Within this group, the `/api` URI prefix is automatically applied so you do not need to manually apply it to every route in the file. You may modify the prefix and other route group options by modifying your `RouteServiceProvider` class. -->
`routes/api.php` ファイルで定義されたルートは、`RouteServiceProvider` によってルート グループ内にネストされます。このグループ内では、`/api` URI プレフィックスが自動的に適用されるため、ファイル内のすべてのルートに手動で適用する必要はありません。 `RouteServiceProvider` クラスを変更することで、プレフィックスおよびその他のルート グループ オプションを変更できます。

<a name="available-router-methods"></a>
<!-- #### Available Router Methods -->
#### Available Router Methods

<!-- The router allows you to register routes that respond to any HTTP verb: -->
ルーターを使用すると、任意の HTTP 動詞に応答するルートを登録できます。

```
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

<!-- Sometimes you may need to register a route that responds to multiple HTTP verbs. You may do so using the `match` method. Or, you may even register a route that responds to all HTTP verbs using the `any` method: -->
場合によっては、複数の HTTP 動詞に応答するルートを登録する必要があるかもしれません。これは、`match` メソッドを使用して行うことができます。または、`any` メソッドを使用して、すべての HTTP 動詞に応答するルートを登録することもできます。

```
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> [!TIP]
> 同じ URI を共有する複数のルートを定義する場合、`get`、`post`、`put`、`patch`、`delete`、および `options` メソッドを使用するルートを、`any`、`match`、および`redirect` メソッド。これにより、受信リクエストが正しいルートと一致することが保証されます。

<a name="dependency-injection"></a>
<!-- #### Dependency Injection -->
#### Dependency Injection

<!-- You may type-hint any dependencies required by your route in your route's callback signature. The declared dependencies will automatically be resolved and injected into the callback by the Laravel [service container](/docs/8.x/container). For example, you may type-hint the `Illuminate\Http\Request` class to have the current HTTP request automatically injected into your route callback: -->
ルートのコールバック署名で、ルートに必要な依存関係をタイプヒントで指定できます。宣言された依存関係は自動的に解決され、Laravel [service container](/docs/8.x/container) によってコールバックに挿入されます。たとえば、`Illuminate\Http\Request` クラスにタイプヒントを指定して、現在の HTTP リクエストをルート コールバックに自動的に挿入できます。

```
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- Remember, any HTML forms pointing to `POST`, `PUT`, `PATCH`, or `DELETE` routes that are defined in the `web` routes file should include a CSRF token field. Otherwise, the request will be rejected. You can read more about CSRF protection in the [CSRF documentation](/docs/8.x/csrf): -->
`web` ルート ファイルで定義されている `POST`、`PUT`、`PATCH`、または `DELETE` ルートを指す HTML フォームには、CSRF トークン フィールドが含まれている必要があることに注意してください。それ以外の場合、リクエストは拒否されます。 CSRF 保護の詳細については、[CSRF documentation](/docs/8.x/csrf) を参照してください。

```
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
<!-- ### Redirect Routes -->
### Redirect Routes

<!-- If you are defining a route that redirects to another URI, you may use the `Route::redirect` method. This method provides a convenient shortcut so that you do not have to define a full route or controller for performing a simple redirect: -->
別の URI にリダイレクトするルートを定義している場合は、`Route::redirect` メソッドを使用できます。このメソッドは便利なショートカットを提供するため、単純なリダイレクトを実行するために完全なルートまたはコントローラを定義する必要はありません。

```
Route::redirect('/here', '/there');
```

<!-- By default, `Route::redirect` returns a `302` status code. You may customize the status code using the optional third parameter: -->
デフォルトでは、`Route::redirect` は `302` ステータス コードを返します。オプションの 3 番目のパラメータを使用してステータス コードをカスタマイズできます。

```
Route::redirect('/here', '/there', 301);
```

<!-- Or, you may use the `Route::permanentRedirect` method to return a `301` status code: -->
または、`Route::permanentRedirect` メソッドを使用して、`301` ステータス コードを返すこともできます。

```
Route::permanentRedirect('/here', '/there');
```

> [!NOTE]
> リダイレクトルートでルートパラメーターを使用する場合、`destination` および `status` パラメーターは Laravel によって予約されているため使用できません。

<a name="view-routes"></a>
<!-- ### View Routes -->
### View Routes

<!-- If your route only needs to return a [view](/docs/8.x/views), you may use the `Route::view` method. Like the `redirect` method, this method provides a simple shortcut so that you do not have to define a full route or controller. The `view` method accepts a URI as its first argument and a view name as its second argument. In addition, you may provide an array of data to pass to the view as an optional third argument: -->
ルートが [view](/docs/8.x/views) を返すだけでよい場合は、`Route::view` メソッドを使用できます。 `redirect` メソッドと同様に、このメソッドは単純なショートカットを提供するため、完全なルートまたはコントローラを定義する必要はありません。 `view` メソッドは、最初の引数として URI を、2 番目の引数としてビュー名を受け入れます。さらに、オプションの 3 番目の引数としてビューに渡すデータの配列を指定できます。

```
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!NOTE]
> ビュールートでルートパラメータを使用する場合、`view`、`data`、`status`、`headers`のパラメータはLaravelによって予約されているため使用できません。

<a name="route-parameters"></a>
<!-- ## Route Parameters -->
## Route Parameters

<a name="required-parameters"></a>
<!-- ### Required Parameters -->
### Required Parameters

<!-- Sometimes you will need to capture segments of the URI within your route. For example, you may need to capture a user's ID from the URL. You may do so by defining route parameters: -->
場合によっては、ルート内の URI のセグメントをキャプチャする必要があります。たとえば、URL からユーザー ID を取得する必要がある場合があります。これを行うには、ルート パラメーターを定義します。

```
Route::get('/user/{id}', function ($id) {
    return 'User '.$id;
});
```

<!-- You may define as many route parameters as required by your route: -->
ルートに必要な数のルート パラメータを定義できます。

```
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

<!-- Route parameters are always encased within `{}` braces and should consist of alphabetic characters. Underscores (`_`) are also acceptable within route parameter names. Route parameters are injected into route callbacks / controllers based on their order - the names of the route callback / controller arguments do not matter. -->
ルート パラメーターは常に `{}` 中括弧で囲まれ、アルファベット文字で構成されている必要があります。ルート パラメーター名内ではアンダースコア (`_`) も使用できます。ルート パラメーターは、その順序に基づいてルート コールバック/コントローラに挿入されます。ルート コールバック/コントローラ引数の名前は関係ありません。

<a name="parameters-and-dependency-injection"></a>
<!-- #### Parameters & Dependency Injection -->
#### Parameters & Dependency Injection

<!-- If your route has dependencies that you would like the Laravel service container to automatically inject into your route's callback, you should list your route parameters after your dependencies: -->
Laravel サービスコンテナがルートのコールバックに自動的に挿入する依存関係がルートにある場合は、依存関係の後にルートパラメーターをリストする必要があります。

```
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- Occasionally you may need to specify a route parameter that may not always be present in the URI. You may do so by placing a `?` mark after the parameter name. Make sure to give the route's corresponding variable a default value: -->
場合によっては、URI に常に存在するとは限らないルート パラメーターの指定が必要になることがあります。これを行うには、パラメータ名の後に `?` マークを付けます。ルートの対応する変数にデフォルト値を指定してください。

```
Route::get('/user/{name?}', function ($name = null) {
    return $name;
});

Route::get('/user/{name?}', function ($name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
<!-- ### Regular Expression Constraints -->
### Regular Expression Constraints

<!-- You may constrain the format of your route parameters using the `where` method on a route instance. The `where` method accepts the name of the parameter and a regular expression defining how the parameter should be constrained: -->
ルート インスタンスで `where` メソッドを使用して、ルート パラメーターの形式を制限できます。 `where` メソッドは、パラメーターの名前と、パラメーターを制約する方法を定義する正規表現を受け入れます。

```
Route::get('/user/{name}', function ($name) {
    //
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function ($id) {
    //
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

<!-- For convenience, some commonly used regular expression patterns have helper methods that allow you to quickly add pattern constraints to your routes: -->
便宜上、一般的に使用される一部の正規表現パターンには、パターン制約をルートにすばやく追加できるヘルパ メソッドが用意されています。

```
Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function ($name) {
    //
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function ($id) {
    //
})->whereUuid('id');
```

<!-- If the incoming request does not match the route pattern constraints, a 404 HTTP response will be returned. -->
受信リクエストがルート パターン制約と一致しない場合、404 HTTP 応答が返されます。

<a name="parameters-global-constraints"></a>
<!-- #### Global Constraints -->
#### Global Constraints

<!-- If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `boot` method of your `App\Providers\RouteServiceProvider` class: -->
ルート パラメーターを常に特定の正規表現によって制限したい場合は、`pattern` メソッドを使用できます。これらのパターンは、`App\Providers\RouteServiceProvider` クラスの `boot` メソッドで定義する必要があります。

```
/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::pattern('id', '[0-9]+');
}
```

<!-- Once the pattern has been defined, it is automatically applied to all routes using that parameter name: -->
パターンが定義されると、そのパラメータ名を使用してすべてのルートに自動的に適用されます。

```
Route::get('/user/{id}', function ($id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
<!-- #### Encoded Forward Slashes -->
#### Encoded Forward Slashes

<!-- The Laravel routing component allows all characters except `/` to be present within route parameter values. You must explicitly allow `/` to be part of your placeholder using a `where` condition regular expression: -->
Laravel ルーティングコンポーネントでは、`/` を除くすべての文字がルートパラメーター値内に存在することが許可されます。 `where` 条件正規表現を使用して、`/` をプレースホルダーの一部として明示的に許可する必要があります。

```
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> [!NOTE]
> エンコードされたスラッシュは、最後のルート セグメント内でのみサポートされます。

<a name="named-routes"></a>
<!-- ## Named Routes -->
## Named Routes

<!-- Named routes allow the convenient generation of URLs or redirects for specific routes. You may specify a name for a route by chaining the `name` method onto the route definition: -->
名前付きルートを使用すると、特定のルートの URL またはリダイレクトを簡単に生成できます。ルート定義に `name` メソッドを連鎖させることで、ルートの名前を指定できます。

```
Route::get('/user/profile', function () {
    //
})->name('profile');
```

<!-- You may also specify route names for controller actions: -->
コントローラアクションのルート名を指定することもできます。

```
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!NOTE]
> ルート名は常に一意である必要があります。

<a name="generating-urls-to-named-routes"></a>
<!-- #### Generating URLs To Named Routes -->
#### Generating URLs To Named Routes

<!-- Once you have assigned a name to a given route, you may use the route's name when generating URLs or redirects via Laravel's `route` and `redirect` helper functions: -->
特定のルートに名前を割り当てたら、Laravel の `route` および `redirect` ヘルパ関数を介して URL またはリダイレクトを生成するときにルートの名前を使用できます。

```
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');
```

<!-- If the named route defines parameters, you may pass the parameters as the second argument to the `route` function. The given parameters will automatically be inserted into the generated URL in their correct positions: -->
名前付きルートがパラメーターを定義している場合、そのパラメーターを 2 番目の引数として `route` 関数に渡すことができます。指定されたパラメータは、生成された URL の正しい位置に自動的に挿入されます。

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

<!-- If you pass additional parameters in the array, those key / value pairs will automatically be added to the generated URL's query string: -->
追加のパラメーターを配列で渡すと、それらのキーと値のペアが、生成された URL のクエリ文字列に自動的に追加されます。

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!TIP]
> 現在のロケールなど、URL パラメータにリクエスト全体のデフォルト値を指定したい場合があります。これを実現するには、[`URL::defaults` method](/docs/8.x/urls#default-values) を使用できます。

<a name="inspecting-the-current-route"></a>
<!-- #### Inspecting The Current Route -->
#### Inspecting The Current Route

<!-- If you would like to determine if the current request was routed to a given named route, you may use the `named` method on a Route instance. For example, you may check the current route name from a route middleware: -->
現在のリクエストが特定の名前付きルートにルーティングされたかどうかを確認したい場合は、Route インスタンスで `named` メソッドを使用できます。たとえば、ルート ミドルウェアから現在のルート名を確認できます。

```
/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  \Closure  $next
 * @return mixed
 */
public function handle($request, Closure $next)
{
    if ($request->route()->named('profile')) {
        //
    }

    return $next($request);
}
```

<a name="route-groups"></a>
<!-- ## Route Groups -->
## Route Groups

<!-- Route groups allow you to share route attributes, such as middleware, across a large number of routes without needing to define those attributes on each individual route. -->
ルート グループを使用すると、個別のルートごとにミドルウェアなどのルート属性を定義することなく、多数のルート間でルート属性を共有できます。

<!-- Nested groups attempt to intelligently "merge" attributes with their parent group. Middleware and `where` conditions are merged while names and prefixes are appended. Namespace delimiters and slashes in URI prefixes are automatically added where appropriate. -->
ネストされたグループは、属性をその親グループとインテリジェントに「マージ」しようとします。ミドルウェアと `where` 条件はマージされ、名前とプレフィックスが追加されます。名前空間の区切り文字と URI 接頭辞のスラッシュは、必要に応じて自動的に追加されます。

<a name="route-group-middleware"></a>
<!-- ### Middleware -->
### Middleware

<!-- To assign [middleware](/docs/8.x/middleware) to all routes within a group, you may use the `middleware` method before defining the group. Middleware are executed in the order they are listed in the array: -->
グループ内のすべてのルートに [middleware](/docs/8.x/middleware) を割り当てるには、グループを定義する前に `middleware` メソッドを使用できます。ミドルウェアは、配列にリストされている順序で実行されます。

```
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
<!-- ### Controllers -->
### Controllers

<!-- If a group of routes all utilize the same [controller](/docs/8.x/controllers), you may use the `controller` method to define the common controller for all of the routes within the group. Then, when defining the routes, you only need to provide the controller method that they invoke: -->
ルートのグループがすべて同じ [controller](/docs/8.x/controllers) を使用する場合、`controller` メソッドを使用して、グループ内のすべてのルートに共通のコントローラを定義できます。次に、ルートを定義するときに、ルートが呼び出すコントローラ メソッドを指定するだけで済みます。

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
<!-- ### Subdomain Routing -->
### Subdomain Routing

<!-- Route groups may also be used to handle subdomain routing. Subdomains may be assigned route parameters just like route URIs, allowing you to capture a portion of the subdomain for usage in your route or controller. The subdomain may be specified by calling the `domain` method before defining the group: -->
ルート グループは、サブドメイン ルーティングを処理するために使用することもできます。サブドメインには、ルート URI と同様にルート パラメーターを割り当てることができ、ルートまたはコントローラで使用するためにサブドメインの一部をキャプチャできるようになります。サブドメインは、グループを定義する前に `domain` メソッドを呼び出すことで指定できます。

```
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> [!NOTE]
> サブドメイン ルートに確実に到達できるようにするには、ルート ドメイン ルートを登録する前にサブドメイン ルートを登録する必要があります。これにより、ルート ドメイン ルートが同じ URI パスを持つサブドメイン ルートを上書きすることがなくなります。

<a name="route-group-prefixes"></a>
<!-- ### Route Prefixes -->
### Route Prefixes

<!-- The `prefix` method may be used to prefix each route in the group with a given URI. For example, you may want to prefix all route URIs within the group with `admin`: -->
`prefix` メソッドを使用して、グループ内の各ルートに特定の URI をプレフィックスとして付けることができます。たとえば、グループ内のすべてのルート URI に `admin` というプレフィックスを付けることができます。

```
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a name="route-group-name-prefixes"></a>
<!-- ### Route Name Prefixes -->
### Route Name Prefixes

<!-- The `name` method may be used to prefix each route name in the group with a given string. For example, you may want to prefix all of the grouped route's names with `admin`. The given string is prefixed to the route name exactly as it is specified, so we will be sure to provide the trailing `.` character in the prefix: -->
`name` メソッドを使用して、グループ内の各ルート名に特定の文字列をプレフィックスとして付けることができます。たとえば、グループ化されたすべてのルート名に `admin` というプレフィックスを付けることができます。指定された文字列は、指定されたとおりにルート名にプレフィックスとして付けられるため、プレフィックスの末尾に `.` 文字を必ず指定します。

```
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
<!-- ## Route Model Binding -->
## Route Model Binding

<!-- When injecting a model ID to a route or controller action, you will often query the database to retrieve the model that corresponds to that ID. Laravel route model binding provides a convenient way to automatically inject the model instances directly into your routes. For example, instead of injecting a user's ID, you can inject the entire `User` model instance that matches the given ID. -->
モデル ID をルートまたはコントローラ アクションに挿入する場合、多くの場合、データベースにクエリを実行して、その ID に対応するモデルを取得します。 Laravel ルート モデル バインディングは、モデル インスタンスをルートに直接自動的に挿入する便利な方法を提供します。たとえば、ユーザーの ID を注入する代わりに、指定された ID に一致する `User` モデル インスタンス全体を注入できます。

<a name="implicit-binding"></a>
<!-- ### Implicit Binding -->
### Implicit Binding

<!-- Laravel automatically resolves Eloquent models defined in routes or controller actions whose type-hinted variable names match a route segment name. For example: -->
Laravel は、タイプヒンテッド変数名がルートセグメント名と一致するルートまたはコントローラアクションで定義された Eloquent モデルを自動的に解決します。例えば：

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

<!-- Since the `$user` variable is type-hinted as the `App\Models\User` Eloquent model and the variable name matches the `{user}` URI segment, Laravel will automatically inject the model instance that has an ID matching the corresponding value from the request URI. If a matching model instance is not found in the database, a 404 HTTP response will automatically be generated. -->
`$user` 変数は `App\Models\User` Eloquent モデルとしてタイプヒントされており、変数名は `{user}` URI セグメントと一致するため、Laravel はリクエスト URI の対応する値に一致する ID を持つモデル インスタンスを自動的に挿入します。一致するモデル インスタンスがデータベース内に見つからない場合、404 HTTP 応答が自動的に生成されます。

<!-- Of course, implicit binding is also possible when using controller methods. Again, note the `{user}` URI segment matches the `$user` variable in the controller which contains an `App\Models\User` type-hint: -->
もちろん、コントローラ メソッドを使用する場合は、暗黙的なバインディングも可能です。繰り返しますが、`{user}` URI セグメントは、`App\Models\User` タイプ ヒントを含むコントローラ内の `$user` 変数と一致することに注意してください。

```
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
<!-- #### Soft Deleted Models -->
#### Soft Deleted Models

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/8.x/eloquent#soft-deleting). However, you may instruct the implicit binding to retrieve these models by chaining the `withTrashed` method onto your route's definition: -->
通常、暗黙的なモデル バインディングでは、[soft deleted](/docs/8.x/eloquent#soft-deleting) になったモデルは取得されません。ただし、ルートの定義に `withTrashed` メソッドをチェーンすることで、これらのモデルを取得するように暗黙的バインディングに指示できます。

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
<!-- #### Customizing The Key -->
#### Customizing The Key

<!-- Sometimes you may wish to resolve Eloquent models using a column other than `id`. To do so, you may specify the column in the route parameter definition: -->
場合によっては、`id` 以外の列を使用して Eloquent モデルを解決したい場合があります。これを行うには、ルート パラメーター定義で列を指定できます。

```
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

<!-- If you would like model binding to always use a database column other than `id` when retrieving a given model class, you may override the `getRouteKeyName` method on the Eloquent model: -->
特定のモデル クラスを取得するときに、モデル バインディングで常に `id` 以外のデータベース列を使用するようにしたい場合は、Eloquent モデルで `getRouteKeyName` メソッドをオーバーライドできます。

```
/**
 * Get the route key for the model.
 *
 * @return string
 */
public function getRouteKeyName()
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
<!-- #### Custom Keys & Scoping -->
#### Custom Keys & Scoping

<!-- When implicitly binding multiple Eloquent models in a single route definition, you may wish to scope the second Eloquent model such that it must be a child of the previous Eloquent model. For example, consider this route definition that retrieves a blog post by slug for a specific user: -->
単一のルート定義で複数の Eloquent モデルを暗黙的にバインドする場合、前の Eloquent モデルの子である必要があるように 2 番目の Eloquent モデルのスコープを設定したい場合があります。たとえば、特定のユーザーのスラッグによってブログ投稿を取得する次のルート定義について考えてみましょう。

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `User` model has a relationship named `posts` (the plural form of the route parameter name) which can be used to retrieve the `Post` model. -->
カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。この場合、`User` モデルには、`Post` モデルを取得するために使用できる `posts` (ルート パラメーター名の複数形) という名前のリレーションシップがあると想定されます。

<!-- If you wish, you may instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route: -->
必要に応じて、カスタムキーが提供されていない場合でも、Laravel に「子」バインディングのスコープを設定するように指示できます。これを行うには、ルートを定義するときに `scopeBindings` メソッドを呼び出します。

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

<!-- Or, you may instruct an entire group of route definitions to use scoped bindings: -->
または、ルート定義のグループ全体にスコープ付きバインディングを使用するように指示することもできます。

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound model is not found. However, you may customize this behavior by calling the `missing` method when defining your route. The `missing` method accepts a closure that will be invoked if an implicitly bound model can not be found: -->
通常、暗黙的にバインドされたモデルが見つからない場合は、404 HTTP 応答が生成されます。ただし、ルートを定義するときに `missing` メソッドを呼び出すことで、この動作をカスタマイズできます。 `missing` メソッドは、暗黙的にバインドされたモデルが見つからない場合に呼び出されるクロージャを受け入れます。

```
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
        ->name('locations.view')
        ->missing(function (Request $request) {
            return Redirect::route('locations.index');
        });
```

<a name="explicit-binding"></a>
<!-- ### Explicit Binding -->
### Explicit Binding

<!-- You are not required to use Laravel's implicit, convention based model resolution in order to use model binding. You can also explicitly define how route parameters correspond to models. To register an explicit binding, use the router's `model` method to specify the class for a given parameter. You should define your explicit model bindings at the beginning of the `boot` method of your `RouteServiceProvider` class: -->
モデルバインディングを使用するために、Laravel の暗黙的な規約ベースのモデル解決を使用する必要はありません。ルート パラメーターがモデルにどのように対応するかを明示的に定義することもできます。明示的なバインディングを登録するには、ルーターの `model` メソッドを使用して、特定のパラメーターのクラスを指定します。 `RouteServiceProvider` クラスの `boot` メソッドの先頭で明示的なモデル バインディングを定義する必要があります。

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::model('user', User::class);

    // ...
}
```

<!-- Next, define a route that contains a `{user}` parameter: -->
次に、`{user}` パラメーターを含むルートを定義します。

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

<!-- Since we have bound all `{user}` parameters to the `App\Models\User` model, an instance of that class will be injected into the route. So, for example, a request to `users/1` will inject the `User` instance from the database which has an ID of `1`. -->
すべての `{user}` パラメーターを `App\Models\User` モデルにバインドしているため、そのクラスのインスタンスがルートに挿入されます。したがって、たとえば、`users/1` へのリクエストは、`1` の ID を持つデータベースから `User` インスタンスを挿入します。

<!-- If a matching model instance is not found in the database, a 404 HTTP response will be automatically generated. -->
一致するモデル インスタンスがデータベース内に見つからない場合、404 HTTP 応答が自動的に生成されます。

<a name="customizing-the-resolution-logic"></a>
<!-- #### Customizing The Resolution Logic -->
#### Customizing The Resolution Logic

<!-- If you wish to define your own model binding resolution logic, you may use the `Route::bind` method. The closure you pass to the `bind` method will receive the value of the URI segment and should return the instance of the class that should be injected into the route. Again, this customization should take place in the `boot` method of your application's `RouteServiceProvider`: -->
独自のモデル バインディング解決ロジックを定義したい場合は、`Route::bind` メソッドを使用できます。 `bind` メソッドに渡すクロージャは、URI セグメントの値を受け取り、ルートに挿入されるクラスのインスタンスを返す必要があります。繰り返しますが、このカスタマイズは、アプリケーションの `RouteServiceProvider` の `boot` メソッドで行う必要があります。

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::bind('user', function ($value) {
        return User::where('name', $value)->firstOrFail();
    });

    // ...
}
```

<!-- Alternatively, you may override the `resolveRouteBinding` method on your Eloquent model. This method will receive the value of the URI segment and should return the instance of the class that should be injected into the route: -->
あるいは、Eloquent モデルの `resolveRouteBinding` メソッドをオーバーライドすることもできます。このメソッドは URI セグメントの値を受け取り、ルートに挿入されるクラスのインスタンスを返す必要があります。

```
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

<!-- If a route is utilizing [implicit binding scoping](#implicit-model-binding-scoping), the `resolveChildRouteBinding` method will be used to resolve the child binding of the parent model: -->
ルートが [implicit binding scoping](#implicit-model-binding-scoping) を利用している場合、親モデルの子バインディングを解決するために `resolveChildRouteBinding` メソッドが使用されます。

```
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
<!-- ## Fallback Routes -->
## Fallback Routes

<!-- Using the `Route::fallback` method, you may define a route that will be executed when no other route matches the incoming request. Typically, unhandled requests will automatically render a "404" page via your application's exception handler. However, since you would typically define the `fallback` route within your `routes/web.php` file, all middleware in the `web` middleware group will apply to the route. You are free to add additional middleware to this route as needed: -->
`Route::fallback` メソッドを使用すると、受信リクエストに一致するルートが他にない場合に実行されるルートを定義できます。通常、未処理のリクエストは、アプリケーションの例外ハンドラーを介して自動的に「404」ページをレンダリングします。ただし、通常は `routes/web.php` ファイル内で `fallback` ルートを定義するため、`web` ミドルウェア グループ内のすべてのミドルウェアがルートに適用されます。必要に応じて、このルートにミドルウェアを自由に追加できます。

```
Route::fallback(function () {
    //
});
```

> [!NOTE]
> フォールバック ルートは常に、アプリケーションによって登録された最後のルートである必要があります。

<a name="rate-limiting"></a>
<!-- ## Rate Limiting -->
## Rate Limiting

<a name="defining-rate-limiters"></a>
<!-- ### Defining Rate Limiters -->
### Defining Rate Limiters

<!-- Laravel includes powerful and customizable rate limiting services that you may utilize to restrict the amount of traffic for a given route or group of routes. To get started, you should define rate limiter configurations that meet your application's needs. Typically, this should be done within the `configureRateLimiting` method of your application's `App\Providers\RouteServiceProvider` class. -->
Laravel には、特定のルートまたはルートのグループのトラフィック量を制限するために利用できる、強力でカスタマイズ可能なレート制限サービスが含まれています。まず、アプリケーションのニーズを満たすレート リミッター構成を定義する必要があります。通常、これはアプリケーションの `App\Providers\RouteServiceProvider` クラスの `configureRateLimiting` メソッド内で実行する必要があります。

<!-- Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned to the rate limiter. Limit configuration are instances of the `Illuminate\Cache\RateLimiting\Limit` class. This class contains helpful "builder" methods so that you can quickly define your limit. The rate limiter name may be any string you wish: -->
レート リミッターは、`RateLimiter` ファサードの `for` メソッドを使用して定義されます。 `for` メソッドは、レート リミッター名と、レート リミッターに割り当てられたルートに適用される制限構成を返すクロージャを受け入れます。制限構成は、`Illuminate\Cache\RateLimiting\Limit` クラスのインスタンスです。このクラスには、制限をすばやく定義できるようにする便利な「ビルダ」メソッドが含まれています。レート リミッタ名には、任意の文字列を指定できます。

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Configure the rate limiters for the application.
 *
 * @return void
 */
protected function configureRateLimiting()
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

<!-- If the incoming request exceeds the specified rate limit, a response with a 429 HTTP status code will automatically be returned by Laravel. If you would like to define your own response that should be returned by a rate limit, you may use the `response` method: -->
受信リクエストが指定されたレート制限を超える場合、429 HTTP ステータス コードを含むレスポンスが Laravel によって自動的に返されます。レート制限によって返される独自の応答を定義したい場合は、`response` メソッドを使用できます。

```
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function () {
        return response('Custom response...', 429);
    });
});
```

<!-- Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user: -->
レート リミッター コールバックは受信 HTTP リクエスト インスタンスを受け取るため、受信リクエストまたは認証されたユーザーに基づいて適切なレート制限を動的に構築できます。

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
<!-- #### Segmenting Rate Limits -->
#### Segmenting Rate Limits

<!-- Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit: -->
場合によっては、レート制限を任意の値で分割したい場合があります。たとえば、ユーザーが IP アドレスごとに 1 分あたり 100 回、特定のルートにアクセスできるようにしたい場合があります。これを実現するには、レート制限を構築するときに `by` メソッドを使用します。

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

<!-- To illustrate this feature using another example, we can limit access to the route to 100 times per minute per authenticated user ID or 10 times per minute per IP address for guests: -->
別の例を使用してこの機能を説明すると、ルートへのアクセスを、認証されたユーザー ID ごとに 1 分あたり 100 回、またはゲストの IP アドレスごとに 1 分あたり 10 回に制限できます。

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
<!-- #### Multiple Rate Limits -->
#### Multiple Rate Limits

<!-- If needed, you may return an array of rate limits for a given rate limiter configuration. Each rate limit will be evaluated for the route based on the order they are placed within the array: -->
必要に応じて、特定のレート リミッター構成のレート制限の配列を返すことができます。各レート制限は、配列内に配置された順序に基づいてルートに対して評価されます。

```
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
<!-- ### Attaching Rate Limiters To Routes -->
### Attaching Rate Limiters To Routes

<!-- Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/8.x/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route: -->
レート リミッターは、`throttle` [middleware](/docs/8.x/middleware) を使用してルートまたはルート グループに接続できます。スロットル ミドルウェアは、ルートに割り当てるレート リミッターの名前を受け入れます。

```
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

<a name="throttling-with-redis"></a>
<!-- #### Throttling With Redis -->
#### Throttling With Redis

<!-- Typically, the `throttle` middleware is mapped to the `Illuminate\Routing\Middleware\ThrottleRequests` class. This mapping is defined in your application's HTTP kernel (`App\Http\Kernel`). However, if you are using Redis as your application's cache driver, you may wish to change this mapping to use the `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` class. This class is more efficient at managing rate limiting using Redis: -->
通常、`throttle` ミドルウェアは `Illuminate\Routing\Middleware\ThrottleRequests` クラスにマップされます。このマッピングは、アプリケーションの HTTP カーネル (`App\Http\Kernel`) で定義されます。ただし、アプリケーションのキャッシュ ドライバとして Redis を使用している場合は、`Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` クラスを使用するようにこのマッピングを変更することができます。このクラスは、Redis を使用したレート制限の管理においてより効率的です。

```
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
<!-- ## Form Method Spoofing -->
## Form Method Spoofing

<!-- HTML forms do not support `PUT`, `PATCH`, or `DELETE` actions. So, when defining `PUT`, `PATCH`, or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form. The value sent with the `_method` field will be used as the HTTP request method: -->
HTML フォームは、`PUT`、`PATCH`、または `DELETE` アクションをサポートしません。したがって、HTML フォームから呼び出される `PUT`、`PATCH`、または `DELETE` ルートを定義する場合は、非表示の `_method` フィールドをフォームに追加する必要があります。 `_method` フィールドで送信された値は、HTTP リクエスト メソッドとして使用されます。

```
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

<!-- For convenience, you may use the `@method` [Blade directive](/docs/8.x/blade) to generate the `_method` input field: -->
便宜上、`@method` [Blade directive](/docs/8.x/blade) を使用して、`_method` 入力フィールドを生成できます。

```
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
<!-- ## Accessing The Current Route -->
## Accessing The Current Route

<!-- You may use the `current`, `currentRouteName`, and `currentRouteAction` methods on the `Route` facade to access information about the route handling the incoming request: -->
`Route` ファサードで `current`、`currentRouteName`、および `currentRouteAction` メソッドを使用して、受信リクエストを処理するルートに関する情報にアクセスできます。

```
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

<!-- You may refer to the API documentation for both the [underlying class of the Route facade](https://laravel.com/api/8.x/Illuminate/Routing/Router.html) and [Route instance](https://laravel.com/api/8.x/Illuminate/Routing/Route.html) to review all of the methods that are available on the router and route classes. -->
[underlying class of the Route facade](https://laravel.com/api/8.x/Illuminate/Routing/Router.html) と [Route instance](https://laravel.com/api/8.x/Illuminate/Routing/Route.html) の両方の API ドキュメントを参照して、ルーターとルート クラスで使用できるすべてのメソッドを確認してください。

<a name="cors"></a>
<!-- ## Cross-Origin Resource Sharing (CORS) -->
## Cross-Origin Resource Sharing (CORS)

<!-- Laravel can automatically respond to CORS `OPTIONS` HTTP requests with values that you configure. All CORS settings may be configured in your application's `config/cors.php` configuration file. The `OPTIONS` requests will automatically be handled by the `HandleCors` [middleware](/docs/8.x/middleware) that is included by default in your global middleware stack. Your global middleware stack is located in your application's HTTP kernel (`App\Http\Kernel`). -->
Laravel は、設定した値を使用して CORS `OPTIONS` HTTP リクエストに自動的に応答できます。すべての CORS 設定は、アプリケーションの `config/cors.php` 構成ファイルで構成できます。 `OPTIONS` リクエストは、グローバル ミドルウェア スタックにデフォルトで含まれている `HandleCors` [middleware](/docs/8.x/middleware) によって自動的に処理されます。グローバル ミドルウェア スタックは、アプリケーションの HTTP カーネル (`App\Http\Kernel`) にあります。

> [!TIP]
> CORS および CORS ヘッダーの詳細については、[MDN web documentation on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers) を参照してください。

<a name="route-caching"></a>
<!-- ## Route Caching -->
## Route Caching

<!-- When deploying your application to production, you should take advantage of Laravel's route cache. Using the route cache will drastically decrease the amount of time it takes to register all of your application's routes. To generate a route cache, execute the `route:cache` Artisan command: -->
アプリケーションを運用環境にデプロイするときは、Laravel のルート キャッシュを利用する必要があります。ルート キャッシュを使用すると、アプリケーションのすべてのルートを登録するのにかかる時間が大幅に短縮されます。ルート キャッシュを生成するには、`route:cache` Artisan コマンドを実行します。

```
php artisan route:cache
```

<!-- After running this command, your cached routes file will be loaded on every request. Remember, if you add any new routes you will need to generate a fresh route cache. Because of this, you should only run the `route:cache` command during your project's deployment. -->
このコマンドを実行すると、キャッシュされたルート ファイルがリクエストごとにロードされます。新しいルートを追加する場合は、新しいルート キャッシュを生成する必要があることに注意してください。このため、`route:cache` コマンドはプロジェクトのデプロイメント中にのみ実行する必要があります。

<!-- You may use the `route:clear` command to clear the route cache: -->
`route:clear` コマンドを使用してルート キャッシュをクリアできます。

```
php artisan route:clear
```

