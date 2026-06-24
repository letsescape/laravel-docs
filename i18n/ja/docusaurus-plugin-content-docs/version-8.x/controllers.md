<!-- # Controllers -->
# Controllers

- [Introduction](#introduction)
- [Writing Controllers](#writing-controllers)
    - [Basic Controllers](#basic-controllers)
    - [Single Action Controllers](#single-action-controllers)
- [Controller Middleware](#controller-middleware)
- [Resource Controllers](#resource-controllers)
    - [Partial Resource Routes](#restful-partial-resource-routes)
    - [Nested Resources](#restful-nested-resources)
    - [Naming Resource Routes](#restful-naming-resource-routes)
    - [Naming Resource Route Parameters](#restful-naming-resource-route-parameters)
    - [Scoping Resource Routes](#restful-scoping-resource-routes)
    - [Localizing Resource URIs](#restful-localizing-resource-uris)
    - [Supplementing Resource Controllers](#restful-supplementing-resource-controllers)
- [Dependency Injection & Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controllers are stored in the `app/Http/Controllers` directory. -->
すべてのリクエスト処理ロジックをルート ファイル内のクロージャとして定義する代わりに、「コントローラ」クラスを使用してこの動作を整理したい場合があります。コントローラは、関連するリクエスト処理ロジックを 1 つのクラスにグループ化できます。たとえば、`UserController` クラスは、ユーザーの表示、作成、更新、削除など、ユーザーに関連するすべての受信リクエストを処理する場合があります。デフォルトでは、コントローラは `app/Http/Controllers` ディレクトリに保存されます。

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- Let's take a look at an example of a basic controller. Note that the controller extends the base controller class included with Laravel: `App\Http\Controllers\Controller`: -->
基本的なコントローラの例を見てみましょう。コントローラは、Laravel に含まれる基本コントローラ クラス `App\Http\Controllers\Controller` を拡張していることに注意してください。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     *
     * @param  int  $id
     * @return \Illuminate\View\View
     */
    public function show($id)
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<!-- You can define a route to this controller method like so: -->
次のように、このコントローラ メソッドへのルートを定義できます。

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
受信リクエストが指定されたルート URI と一致すると、`App\Http\Controllers\UserController` クラスの `show` メソッドが呼び出され、ルート パラメーターがメソッドに渡されます。

> [!TIP]
> コントローラは、基本クラスを拡張するために**必須**ではありません。ただし、`middleware` メソッドや `authorize` メソッドなどの便利な機能にはアクセスできません。

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
コントローラのアクションが特に複雑な場合は、コントローラ クラス全体をその 1 つのアクション専用にすると便利な場合があります。これを実現するには、コントローラ内で単一の `__invoke` メソッドを定義します。

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     *
     * @return \Illuminate\Http\Response
     */
    public function __invoke()
    {
        // ...
    }
}
```

<!-- When registering routes for single action controllers, you do not need to specify a controller method. Instead, you may simply pass the name of the controller to the router: -->
シングルアクションコントローラのルートを登録する場合、コントローラメソッドを指定する必要はありません。代わりに、単にコントローラの名前をルーターに渡すこともできます。

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` Artisan コマンドの `--invokable` オプションを使用して、呼び出し可能なコントローラを生成できます。

```
php artisan make:controller ProvisionServer --invokable
```

> [!TIP]
> コントローラ スタブは、[stub publishing](/docs/8.x/artisan#stub-customization) を使用してカスタマイズできます。

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/8.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/8.x/middleware) は、ルート ファイル内のコントローラのルートに割り当てることができます。

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller's constructor. Using the `middleware` method within your controller's constructor, you can assign middleware to the controller's actions: -->
または、コントローラのコンストラクター内でミドルウェアを指定すると便利な場合があります。コントローラのコンストラクター内で `middleware` メソッドを使用すると、コントローラのアクションにミドルウェアを割り当てることができます。

```
class UserController extends Controller
{
    /**
     * Instantiate a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->middleware('auth');
        $this->middleware('log')->only('index');
        $this->middleware('subscribed')->except('store');
    }
}
```

<!-- Controllers also allow you to register middleware using a closure. This provides a convenient way to define an inline middleware for a single controller without defining an entire middleware class: -->
コントローラでは、クロージャーを使用してミドルウェアを登録することもできます。これにより、ミドルウェア クラス全体を定義せずに、単一のコントローラのインライン ミドルウェアを定義する便利な方法が提供されます。

```
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
アプリケーション内の各 Eloquent モデルを「リソース」と考えると、アプリケーション内の各リソースに対して同じ一連のアクションを実行するのが一般的です。たとえば、アプリケーションに `Photo` モデルと `Movie` モデルが含まれていると想像してください。ユーザーはこれらのリソースを作成、読み取り、更新、または削除できる可能性があります。

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
この一般的なユースケースのため、Laravel リソースルーティングは、1 行のコードで典型的な作成、読み取り、更新、および削除 (「CRUD」) ルートをコントローラに割り当てます。まず、`make:controller` Artisan コマンドの `--resource` オプションを使用して、これらのアクションを処理するコントローラをすばやく作成できます。

```
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
このコマンドは、`app/Http/Controllers/PhotoController.php` にコントローラを生成します。コントローラには、使用可能なリソース操作ごとにメソッドが含まれます。次に、コントローラを指すリソース ルートを登録できます。

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
この 1 つのルート宣言により、リソースに対するさまざまなアクションを処理するための複数のルートが作成されます。生成されたコントローラには、これらのアクションごとにスタブ化されたメソッドがすでに含まれています。 `route:list` Artisan コマンドを実行すると、アプリケーションのルートの概要をいつでも簡単に取得できることに注意してください。

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
配列を `resources` メソッドに渡すことで、多くのリソース コントローラを一度に登録することもできます。

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controller"></a>
<!-- #### Actions Handled By Resource Controller -->
#### Actions Handled By Resource Controller

<!--
Verb      | URI                    | Action       | Route Name
----------|------------------------|--------------|---------------------
GET       | `/photos`              | index        | photos.index
GET       | `/photos/create`       | create       | photos.create
POST      | `/photos`              | store        | photos.store
GET       | `/photos/{photo}`      | show         | photos.show
GET       | `/photos/{photo}/edit` | edit         | photos.edit
PUT/PATCH | `/photos/{photo}`      | update       | photos.update
DELETE    | `/photos/{photo}`      | destroy      | photos.destroy
-->
動詞      | URI                    | アクション       | 路線名
----------|------------------------|--------------|---------------------
GET       | `/photos`              | index        | photos.index
GET       | `/photos/create`       | create       | photos.create
POST      | `/photos`              | store        | photos.store
GET       | `/photos/{photo}`      | show         | photos.show
GET       | `/photos/{photo}/edit` | edit         | photos.edit
PUT/PATCH | `/photos/{photo}`      | update       | photos.update
DELETE    | `/photos/{photo}`      | destroy      | photos.destroy

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound resource model is not found. However, you may customize this behavior by calling the `missing` method when defining your resource route. The `missing` method accepts a closure that will be invoked if an implicitly bound model can not be found for any of the resource's routes: -->
通常、暗黙的にバインドされたリソース モデルが見つからない場合は、404 HTTP 応答が生成されます。ただし、リソース ルートを定義するときに `missing` メソッドを呼び出すことで、この動作をカスタマイズできます。 `missing` メソッドは、リソースのルートのいずれにも暗黙的にバインドされたモデルが見つからない場合に呼び出されるクロージャを受け入れます。

```
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
        ->missing(function (Request $request) {
            return Redirect::route('photos.index');
        });
```

<a name="specifying-the-resource-model"></a>
<!-- #### Specifying The Resource Model -->
#### Specifying The Resource Model

<!-- If you are using [route model binding](/docs/8.x/routing#route-model-binding) and would like the resource controller's methods to type-hint a model instance, you may use the `--model` option when generating the controller: -->
[route model binding](/docs/8.x/routing#route-model-binding) を使用していて、リソース コントローラのメソッドでモデル インスタンスのタイプヒントを取得したい場合は、コントローラの生成時に `--model` オプションを使用できます。

```
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/8.x/validation#form-request-validation) for the controller's storage and update methods: -->
リソース コントローラを生成するときに `--requests` オプションを指定して、コントローラのストレージおよび更新メソッドに対して [form request classes](/docs/8.x/validation#form-request-validation) を生成するように Artisan に指示できます。

```
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
リソース ルートを宣言するとき、デフォルト アクションの完全なセットの代わりに、コントローラが処理する必要があるアクションのサブセットを指定できます。

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->only([
    'index', 'show'
]);

Route::resource('photos', PhotoController::class)->except([
    'create', 'store', 'update', 'destroy'
]);
```

<a name="api-resource-routes"></a>
<!-- #### API Resource Routes -->
#### API Resource Routes

<!-- When declaring resource routes that will be consumed by APIs, you will commonly want to exclude routes that present HTML templates such as `create` and `edit`. For convenience, you may use the `apiResource` method to automatically exclude these two routes: -->
API によって使用されるリソース ルートを宣言する場合、一般的に、`create` や `edit` などの HTML テンプレートを提示するルートを除外する必要があります。便宜上、`apiResource` メソッドを使用して、これら 2 つのルートを自動的に除外できます。

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
配列を `apiResources` メソッドに渡すことで、多くの API リソース コントローラを一度に登録できます。

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`create` メソッドまたは `edit` メソッドを含まない API リソース コントローラを迅速に生成するには、`make:controller` コマンドの実行時に `--api` スイッチを使用します。

```
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
場合によっては、ネストされたリソースへのルートを定義する必要があるかもしれません。たとえば、写真リソースには、写真に添付できる複数のコメントがある場合があります。リソース コントローラをネストするには、ルート宣言で「ドット」表記を使用できます。

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
このルートは、次のような URI でアクセスできるネストされたリソースを登録します。

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel の [implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) 機能は、解決された子モデルが親モデルに属していることが確認されるように、ネストされたバインディングを自動的にスコープ設定できます。ネストされたリソースを定義するときに `scoped` メソッドを使用すると、自動スコープを有効にしたり、子リソースを取得するフィールドを Laravel に指示したりできます。これを実現する方法の詳細については、[scoping resource routes](#restful-scoping-resource-routes) のドキュメントを参照してください。

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
多くの場合、子 ID はすでに一意の識別子であるため、URI 内に親 ID と子 ID の両方を含める必要は必ずしもありません。自動インクリメント主キーなどの一意の識別子を使用して URI セグメント内のモデルを識別する場合、「浅いネスト」の使用を選択できます。

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
このルート定義では、次のルートが定義されます。

<!--
Verb      | URI                               | Action       | Route Name
----------|-----------------------------------|--------------|---------------------
GET       | `/photos/{photo}/comments`        | index        | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create       | photos.comments.create
POST      | `/photos/{photo}/comments`        | store        | photos.comments.store
GET       | `/comments/{comment}`             | show         | comments.show
GET       | `/comments/{comment}/edit`        | edit         | comments.edit
PUT/PATCH | `/comments/{comment}`             | update       | comments.update
DELETE    | `/comments/{comment}`             | destroy      | comments.destroy
-->
動詞      | URI                               | アクション       | 路線名
----------|-----------------------------------|--------------|---------------------
GET       | `/photos/{photo}/comments`        | index        | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create       | photos.comments.create
POST      | `/photos/{photo}/comments`        | store        | photos.comments.store
GET       | `/comments/{comment}`             | show         | comments.show
GET       | `/comments/{comment}/edit`        | edit         | comments.edit
PUT/PATCH | `/comments/{comment}`             | update       | comments.update
DELETE    | `/comments/{comment}`             | destroy      | comments.destroy

<a name="restful-naming-resource-routes"></a>
<!-- ### Naming Resource Routes -->
### Naming Resource Routes

<!-- By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your desired route names: -->
デフォルトでは、すべてのリソース コントローラ アクションにはルート名が付いています。ただし、希望のルート名を含む `names` 配列を渡すことで、これらの名前をオーバーライドできます。

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
<!-- ### Naming Resource Route Parameters -->
### Naming Resource Route Parameters

<!-- By default, `Route::resource` will create the route parameters for your resource routes based on the "singularized" version of the resource name. You can easily override this on a per resource basis using the `parameters` method. The array passed into the `parameters` method should be an associative array of resource names and parameter names: -->
デフォルトでは、`Route::resource` はリソース名の「単数化」バージョンに基づいてリソース ルートのルート パラメーターを作成します。これは、`parameters` メソッドを使用してリソースごとに簡単にオーバーライドできます。 `parameters` メソッドに渡される配列は、リソース名とパラメーター名の連想配列である必要があります。

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!--  The example above generates the following URI for the resource's `show` route: -->
上記の例では、リソースの `show` ルートに対して次の URI を生成します。

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel の [scoped implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) 機能は、解決された子モデルが親モデルに属していることが確認されるように、ネストされたバインディングを自動的にスコープ設定できます。ネストされたリソースを定義するときに `scoped` メソッドを使用すると、自動スコープを有効にしたり、子リソースを取得するフィールドを Laravel に指示したりできます。

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
このルートは、次のような URI でアクセスできるスコープ付きのネストされたリソースを登録します。

```
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
カスタムのキー付き暗黙的バインディングをネストされたルートパラメーターとして使用する場合、Laravel は、親の関係名を推測する規則を使用して、親によってネストされたモデルを取得するためにクエリのスコープを自動的に設定します。この場合、`Photo` モデルには、`Comment` モデルを取得するために使用できる `comments` (ルート パラメーター名の複数形) という名前のリレーションシップがあると想定されます。

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\RouteServiceProvider`: -->
デフォルトでは、`Route::resource` は英語の動詞を使用してリソース URI を作成します。 `create` および `edit` アクション動詞をローカライズする必要がある場合は、`Route::resourceVerbs` メソッドを使用できます。これは、アプリケーションの `App\Providers\RouteServiceProvider` 内の `boot` メソッドの先頭で行うことができます。

```
/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);

    // ...
}
```

<!-- Once the verbs have been customized, a resource route registration such as `Route::resource('fotos', PhotoController::class)` will produce the following URIs: -->
動詞がカスタマイズされると、`Route::resource('fotos', PhotoController::class)` などのリソース ルート登録によって次の URI が生成されます。

```
/fotos/crear

/fotos/{foto}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
リソース ルートのデフォルト セットを超えて追加のルートをリソース コントローラに追加する必要がある場合は、`Route::resource` メソッドを呼び出す前にそれらのルートを定義する必要があります。そうしないと、`resource` メソッドで定義されたルートが、補助ルートよりも意図せず優先される可能性があります。

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!TIP]
> コントローラに集中することを忘れないでください。一般的なリソース アクションのセット以外のメソッドが日常的に必要な場合は、コントローラを 2 つの小さなコントローラに分割することを検討してください。

<a name="dependency-injection-and-controllers"></a>
<!-- ## Dependency Injection & Controllers -->
## Dependency Injection & Controllers

<a name="constructor-injection"></a>
<!-- #### Constructor Injection -->
#### Constructor Injection

<!-- The Laravel [service container](/docs/8.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel [service container](/docs/8.x/container) は、すべての Laravel コントローラを解決するために使用されます。その結果、コントローラがコンストラクターで必要とする依存関係をタイプヒントで指定できるようになります。宣言された依存関係は自動的に解決され、コントローラ インスタンスに挿入されます。

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * The user repository instance.
     */
    protected $users;

    /**
     * Create a new controller instance.
     *
     * @param  \App\Repositories\UserRepository  $users
     * @return void
     */
    public function __construct(UserRepository $users)
    {
        $this->users = $users;
    }
}
```

<a name="method-injection"></a>
<!-- #### Method Injection -->
#### Method Injection

<!-- In addition to constructor injection, you may also type-hint dependencies on your controller's methods. A common use-case for method injection is injecting the `Illuminate\Http\Request` instance into your controller methods: -->
コンストラクターのインジェクションに加えて、コントローラのメソッドに対するタイプヒントの依存関係を指定することもできます。メソッド インジェクションの一般的な使用例は、コントローラ メソッドに `Illuminate\Http\Request` インスタンスを挿入することです。

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $name = $request->name;

        //
    }
}
```

<!-- If your controller method is also expecting input from a route parameter, list your route arguments after your other dependencies. For example, if your route is defined like so: -->
コントローラ メソッドがルート パラメーターからの入力も期待している場合は、他の依存関係の後にルート引数をリストします。たとえば、ルートが次のように定義されているとします。

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
次のようにコントローラ メソッドを定義することで、`Illuminate\Http\Request` をタイプヒントし、`id` パラメーターにアクセスすることができます。

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }
}
```

