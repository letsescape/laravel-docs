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
    - [Singleton Resource Controllers](#singleton-resource-controllers)
- [Dependency Injection & Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controllers are stored in the `app/Http/Controllers` directory. -->
모든 요청 처리 로직을 라우트 파일의 클로저로 작성하기보다, "컨트롤러" 클래스를 사용해 이 로직을 더 체계적으로 정리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶어 관리할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- Let's take a look at an example of a basic controller. Note that the controller extends the base controller class included with Laravel: `App\Http\Controllers\Controller`: -->
기본 컨트롤러의 예제를 살펴보겠습니다. 컨트롤러는 Laravel에서 제공하는 기본 컨트롤러 클래스인 `App\Http\Controllers\Controller`를 확장합니다.

```
<?php

namespace App\Http\Controllers;

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
이 컨트롤러 메서드로 라우트를 정의하려면 다음과 같이 작성합니다.

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
요청이 해당 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 **반드시** 기본 클래스를 상속해야 하는 것은 아닙니다. 하지만 상속하지 않으면 `middleware`나 `authorize`와 같은 편리한 기능을 사용할 수 없습니다.

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
컨트롤러의 액션이 특히 복잡하다면, 그 액션만을 위한 별도의 컨트롤러 클래스를 만들 수도 있습니다. 이를 위해 컨트롤러에 `__invoke` 메서드 하나만 정의하면 됩니다.

```
<?php

namespace App\Http\Controllers;

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
단일 액션 컨트롤러를 라우트에 등록할 때는 메서드명을 따로 지정하지 않고, 컨트롤러 이름만 전달하면 됩니다.

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` Artisan 명령어에서 `--invokable` 옵션을 사용하면 단일 액션 컨트롤러를 쉽게 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [stub publishing](/docs/9.x/artisan#stub-customization)을 통해 사용자 정의가 가능합니다.

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/9.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/9.x/middleware)는 라우트 파일에서 해당 컨트롤러의 라우트에 직접 지정할 수 있습니다.

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller's constructor. Using the `middleware` method within your controller's constructor, you can assign middleware to the controller's actions: -->
또는, 컨트롤러의 생성자에서 미들웨어를 지정할 수도 있습니다. 컨트롤러 생성자에서 `middleware` 메서드를 사용하면 컨트롤러의 액션에 미들웨어를 할당할 수 있습니다.

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
컨트롤러에서는 미들웨어를 클로저(익명 함수)로도 등록할 수 있습니다. 이를 통해 컨트롤러 내에서만 사용하는 간단한 미들웨어를 별도의 클래스 없이 정의할 수 있습니다.

```
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
애플리케이션의 각 Eloquent 모델을 "리소스"로 생각할 수 있다면, 일반적으로 각각의 리소스에 대해 비슷한 작업(생성, 조회, 수정, 삭제 등)을 수행하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자는 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
이처럼 반복해서 사용되는 작업을 위해, Laravel의 리소스 라우팅은 이러한 CRUD(생성, 조회, 수정, 삭제) 작업을 단 한 줄의 코드로 컨트롤러에 할당할 수 있게 해줍니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용해 이런 작업을 담당할 컨트롤러를 빠르게 만들 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
이 명령어는 `app/Http/Controllers/PhotoController.php` 경로에 컨트롤러를 생성합니다. 생성된 컨트롤러에는 각각의 리소스 작업에 해당하는 메서드가 포함되어 있습니다. 이후, 해당 컨트롤러에 연결되는 리소스 라우트를 다음과 같이 등록할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
이렇게 선언된 한 줄의 라우트는 해당 리소스에 대한 다양한 작업을 처리하는 여러 개의 라우트를 자동으로 생성합니다. 컨트롤러에는 각 작업에 대한 메서드가 이미 기본으로 작성되어 있으며, `route:list` Artisan 명령어를 통해 애플리케이션의 모든 라우트를 빠르게 확인할 수 있습니다.

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
여러 개의 리소스 컨트롤러를 한 번에 등록하려면 `resources` 메서드에 배열을 전달하면 됩니다.

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
Verb      | URI                    | 액션        | 라우트 이름
----------|------------------------|-------------|---------------------
GET       | `/photos`              | index       | photos.index
GET       | `/photos/create`       | create      | photos.create
POST      | `/photos`              | store       | photos.store
GET       | `/photos/{photo}`      | show        | photos.show
GET       | `/photos/{photo}/edit` | edit        | photos.edit
PUT/PATCH | `/photos/{photo}`      | update      | photos.update
DELETE    | `/photos/{photo}`      | destroy     | photos.destroy

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound resource model is not found. However, you may customize this behavior by calling the `missing` method when defining your resource route. The `missing` method accepts a closure that will be invoked if an implicitly bound model can not be found for any of the resource's routes: -->
일반적으로 암묵적 모델 바인딩에서 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 `missing` 메서드를 사용하면 이 동작을 직접 정의할 수 있습니다. `missing` 메서드는 모델을 찾을 수 없는 경우에 실행될 클로저를 받아들입니다.

```
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
        ->missing(function (Request $request) {
            return Redirect::route('photos.index');
        });
```

<a name="soft-deleted-models"></a>
<!-- #### Soft Deleted Models -->
#### Soft Deleted Models

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/9.x/eloquent#soft-deleting), and will instead return a 404 HTTP response. However, you can instruct the framework to allow soft deleted models by invoking the `withTrashed` method when defining your resource route: -->
기본적으로 암묵적 모델 바인딩은 [soft deleted](/docs/9.x/eloquent#soft-deleting)된 모델을 조회하지 않고, 대신 404 HTTP 응답을 반환합니다. 하지만 라우트 정의 시 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델도 허용하도록 할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

<!-- Calling `withTrashed` with no arguments will allow soft deleted models for the `show`, `edit`, and `update` resource routes. You may specify a subset of these routes by passing an array to the `withTrashed` method: -->
`withTrashed`에 인자를 전달하지 않으면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델도 허용하게 됩니다. `withTrashed` 메서드에 배열을 전달하면 이 라우트 중 일부만 지정할 수 있습니다.

```
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
<!-- #### Specifying The Resource Model -->
#### Specifying The Resource Model

<!-- If you are using [route model binding](/docs/9.x/routing#route-model-binding) and would like the resource controller's methods to type-hint a model instance, you may use the `--model` option when generating the controller: -->
[route model binding](/docs/9.x/routing#route-model-binding)을 사용하며, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트로 받고 싶을 때는 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/9.x/validation#form-request-validation) for the controller's storage and update methods: -->
리소스 컨트롤러를 생성할 때 `--requests` 옵션을 추가하면, 저장 및 업데이트 메서드용 [form request classes](/docs/9.x/validation#form-request-validation)도 자동 생성됩니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
리소스 라우트를 선언할 때 기본 액션 전체가 아닌, 일부 액션만 컨트롤러에서 처리하도록 지정할 수 있습니다.

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
API에서 사용할 리소스 라우트를 선언할 때는, 일반적으로 `create`, `edit`처럼 HTML 템플릿을 제공하는 라우트는 제외하는 것이 일반적입니다. `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
여러 API 리소스 컨트롤러를 함께 등록하려면 `apiResources` 메서드를 사용하세요.

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면 `create` 및 `edit` 메서드를 제외한 API 전용 리소스 컨트롤러가 생성됩니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
때로는 중첩 리소스에 대한 라우트를 정의해야 할 수 있습니다. 예를 들어 포토 리소스에 여러 개의 코멘트가 연결될 수 있습니다. 중첩 리소스 컨트롤러를 지정하려면 라우트 선언에서 "dot" 표기법을 사용하면 됩니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같이 접근할 수 있는 중첩 리소스를 등록합니다.

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/9.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel의 [implicit model binding](/docs/9.x/routing#implicit-model-binding-scoping) 기능을 활용해, 중첩 리소스의 하위 모델이 반드시 상위 모델에 속하는지 자동으로 확인(스코핑)할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하여 자동 범위 지정을 활성화하거나, 하위 리소스를 어떤 필드로 조회할지 지정할 수 있습니다. 자세한 방법은 [scoping resource routes](#restful-scoping-resource-routes)를 참고하세요.

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
때로는 URI에 상위와 하위 ID 둘 다 있을 필요가 없습니다. 예를 들어, 하위 리소스의 ID가 고유하다면, "shallow nesting"을 사용할 수 있습니다.

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
이 정의는 다음과 같은 라우트를 만듭니다.

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
Verb      | URI                               | 액션        | 라우트 이름
----------|-----------------------------------|-------------|---------------------
GET       | `/photos/{photo}/comments`        | index       | photos.comments.index
GET       | `/photos/{photo}/comments/create` | create      | photos.comments.create
POST      | `/photos/{photo}/comments`        | store       | photos.comments.store
GET       | `/comments/{comment}`             | show        | comments.show
GET       | `/comments/{comment}/edit`        | edit        | comments.edit
PUT/PATCH | `/comments/{comment}`             | update      | comments.update
DELETE    | `/comments/{comment}`             | destroy     | comments.destroy

<a name="restful-naming-resource-routes"></a>
<!-- ### Naming Resource Routes -->
### Naming Resource Routes

<!-- By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your desired route names: -->
리소스 컨트롤러의 각 액션은 기본적으로 라우트 이름이 지정되어 있지만, `names` 배열을 전달해 원하는 라우트 이름으로 덮어쓸 수 있습니다.

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
기본적으로 `Route::resource`는 리소스 이름의 "단수형"을 기준으로 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하면 이를 리소스별로 쉽게 변경할 수 있습니다. `parameters` 메서드에 전달하는 배열은 리소스명과 파라미터명을 대응시키는 연관 배열이어야 합니다.

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!--  The example above generates the following URI for the resource's `show` route: -->
위 예제의 경우, 해당 리소스의 `show` 라우트 URI는 다음과 같이 생성됩니다.

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/9.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel의 [scoped implicit model binding](/docs/9.x/routing#implicit-model-binding-scoping) 기능을 이용해, 중첩 모델의 범위가 상위 모델에 속하는지를 자동으로 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑과 함께 하위 리소스가 어떤 필드로 조회되는지 지정할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
이렇게 하면, 다음과 같이 접근 가능한 스코프된 중첩 리소스가 등록됩니다.

```
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
커스텀 키를 사용하는 암묵적 바인딩이 중첩 라우트 파라미터로 사용될 때, Laravel은 해당 중첩 모델을 상위 모델의 관계를 통해 범위(스코프)로 제한합니다. 즉, 위 예제에서는 `Photo` 모델이 `comments`라는 관계를 가지고 있다고 가정하여 `Comment` 모델을 조회하게 됩니다.

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs and plural rules. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\RouteServiceProvider`: -->
기본적으로 `Route::resource`는 리소스 URI를 영어 동사와 복수 규칙으로 생성합니다. `create`와 `edit` 같은 액션 동사를 현지화하려면, 애플리케이션의 `App\Providers\RouteServiceProvider` 내에서 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 보통 `boot` 메서드에 작성합니다.

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

<!-- Laravel's pluralizer supports [several different languages which you may configure based on your needs](/docs/9.x/localization#pluralization-language). Once the verbs and pluralization language have been customized, a resource route registration such as `Route::resource('publicacion', PublicacionController::class)` will produce the following URIs: -->
Laravel의 복수화 기능은 [several different languages which you may configure based on your needs](/docs/9.x/localization#pluralization-language)하며, 필요에 따라 설정할 수 있습니다. 동사와 복수화 언어를 변경한 뒤에는, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`와 같이 등록하면 다음과 같은 URI가 생성됩니다.

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
기본 리소스 라우트 외에 추가적인 라우트를 컨트롤러에 등록해야 할 경우, `Route::resource`를 호출하기 **이전에** 직접 추가 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드로 정의된 라우트가 의도치 않게 덮어쓸 수 있습니다.

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 한 가지 책임에 집중하도록 설계하는 것이 좋습니다. 만약 자주 기본 리소스 액션 외의 별도 메서드가 필요하다면, 컨트롤러를 더 작고 여러 개로 분리하는 것을 고려해보세요.

<a name="singleton-resource-controllers"></a>
<!-- ### Singleton Resource Controllers -->
### Singleton Resource Controllers

<!-- Sometimes, your application will have resources that may only have a single instance. For example, a user's "profile" can be edited or updated, but a user may not have more than one "profile". Likewise, an image may have a single "thumbnail". These resources are called "singleton resources", meaning one and only one instance of the resource may exist. In these scenarios, you may register a "singleton" resource controller: -->
애플리케이션에 하나의 인스턴스만 존재할 수 있는 리소스도 있을 수 있습니다. 예를 들어 한 사용자의 "프로필"은 하나만 존재하며, 이미지를 대표하는 "썸네일"도 마찬가지입니다. 이처럼 하나만 존재할 수 있는 자원을 "싱글턴 리소스"라고 하며, 이런 경우 "싱글턴" 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

<!-- The singleton resource definition above will register the following routes. As you can see, "creation" routes are not registered for singleton resources, and the registered routes do not accept an identifier since only one instance of the resource may exist: -->
위의 싱글턴 리소스 등록은 다음과 같은 라우트를 생성합니다. "생성" 라우트는 등록되지 않으며, 해당 리소스는 한 개만 존재하기 때문에 식별자를 따로 받지 않습니다.

<!--
Verb      | URI                               | Action       | Route Name
----------|-----------------------------------|--------------|---------------------
GET       | `/profile`                        | show         | profile.show
GET       | `/profile/edit`                   | edit         | profile.edit
PUT/PATCH | `/profile`                        | update       | profile.update
-->
Verb      | URI                               | 액션       | 라우트 이름
----------|-----------------------------------|------------|---------------------
GET       | `/profile`                        | show       | profile.show
GET       | `/profile/edit`                   | edit       | profile.edit
PUT/PATCH | `/profile`                        | update     | profile.update

<!-- Singleton resources may also be nested within a standard resource: -->
싱글턴 리소스는 표준 리소스 내부에 중첩시킬 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

<!-- In this example, the `photos` resource would receive all of the [standard resource routes](#actions-handled-by-resource-controller); however, the `thumbnail` resource would be a singleton resource with the following routes: -->
이 예시에서는, `photos` 리소스는 [standard resource routes](#actions-handled-by-resource-controller)를 모두 가지게 되고, `thumbnail`은 아래와 같은 싱글턴 리소스로 제공됩니다.

| Verb      | URI                              | 액션   | 라우트 이름                |
|-----------|----------------------------------|--------|----------------------------|
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show      |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit      |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update    |

<a name="creatable-singleton-resources"></a>
<!-- #### Creatable Singleton Resources -->
#### Creatable Singleton Resources

<!-- Occasionally, you may want to define creation and storage routes for a singleton resource. To accomplish this, you may invoke the `creatable` method when registering the singleton resource route: -->
때로는 싱글턴 리소스에 대해 생성 및 저장 라우트도 필요할 수 있습니다. 이럴 때는 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 사용하면 됩니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

<!-- In this example, the following routes will be registered. As you can see, a `DELETE` route will also be registered for creatable singleton resources: -->
이 예제에서는 다음과 같은 라우트가 추가로 등록됩니다. 생성/저장의 라우트 외에도, `DELETE` 라우트 또한 등록됩니다.

| Verb      | URI                                | 액션    | 라우트 이름                |
|-----------|------------------------------------|---------|----------------------------|
| GET       | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create    |
| POST      | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store     |
| GET       | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show      |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit      |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update    |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy   |

<!-- If you would like Laravel to register the `DELETE` route for a singleton resource but not register the creation or storage routes, you may utilize the `destroyable` method: -->
만약 싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 생성/저장 라우트는 등록하지 않으려면, `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
<!-- #### API Singleton Resources -->
#### API Singleton Resources

<!-- The `apiSingleton` method may be used to register a singleton resource that will be manipulated via an API, thus rendering the `create` and `edit` routes unnecessary: -->
`apiSingleton` 메서드를 사용하면 API를 통해 조작할 싱글턴 리소스를 등록할 수 있으며, 이 경우 `create`와 `edit` 라우트는 생성되지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

<!-- Of course, API singleton resources may also be `creatable`, which will register `store` and `destroy` routes for the resource: -->
또한 API 싱글턴 리소스에서도 `creatable` 메서드를 적용해 `store`와 `destroy` 라우트를 등록할 수 있습니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
<!-- ## Dependency Injection & Controllers -->
## Dependency Injection & Controllers

<a name="constructor-injection"></a>
<!-- #### Constructor Injection -->
#### Constructor Injection

<!-- The Laravel [service container](/docs/9.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel의 [service container](/docs/9.x/container)는 모든 컨트롤러를 자동으로 해석(resolve)해줍니다. 따라서 컨트롤러 생성자에 필요로 하는 의존성 타입을 지정(타입힌트)하면, 서비스 컨테이너가 자동으로 주입해줍니다.

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
생성자 주입 외에도 컨트롤러 메서드의 인자로 의존성을 타입힌트로 지정할 수 있습니다. 가장 일반적인 예로는, 컨트롤러 메서드에서 `Illuminate\Http\Request` 인스턴스를 주입받는 경우가 많습니다.

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
컨트롤러 메서드에서 라우트 파라미터의 값도 함께 전달받아야 할 경우, 의존성 인자 뒤에 라우트 인수를 나열하면 됩니다. 예를 들어 라우트가 다음과 같이 정의되어 있다면,

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
컨트롤러 메서드에서 `Illuminate\Http\Request`와 함께 `id` 파라미터도 다음과 같이 받을 수 있습니다.

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
