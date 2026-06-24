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
- [Dependency Injection and Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controllers are stored in the `app/Http/Controllers` directory. -->
모든 요청 처리 로직을 라우트 파일에 클로저로 직접 작성하는 대신, 이 동작을 "컨트롤러" 클래스에 정리할 수 있습니다. 컨트롤러를 사용하면 관련된 요청 처리 로직을 하나의 클래스로 그룹화할 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리하도록 만들 수 있습니다. 기본적으로 컨트롤러 파일은 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- To quickly generate a new controller, you may run the `make:controller` Artisan command. By default, all of the controllers for your application are stored in the `app/Http/Controllers` directory: -->
새 컨트롤러를 빠르게 생성하려면 `make:controller` 아티즌(Artisan) 명령어를 사용할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다:

```shell
php artisan make:controller UserController
```

<!-- Let's take a look at an example of a basic controller. A controller may have any number of public methods which will respond to incoming HTTP requests: -->
기본적인 컨트롤러의 예제를 살펴보겠습니다. 컨트롤러는 요청을 처리할 공개(public) 메서드를 원하는 만큼 가질 수 있으며, 각각 HTTP 요청에 응답하게 됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<!-- Once you have written a controller class and method, you may define a route to the controller method like so: -->
컨트롤러 클래스와 메서드를 작성한 후에는, 아래와 같이 해당 컨트롤러 메서드로 라우트를 지정할 수 있습니다.

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
요청이 지정한 URI 라우트와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 특정 베이스 클래스를 상속해야 하는 것은 아닙니다. 그러나 베이스 클래스를 상속하지 않으면 `middleware`, `authorize`와 같은 편리한 기능을 사용할 수 없습니다.

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
특정 컨트롤러 액션이 매우 복잡하다면, 하나의 컨트롤러 클래스를 해당 액션만을 위해 전담시키는 것도 좋은 방법입니다. 이를 위해 컨트롤러 내에 `__invoke`라는 단일 메서드만 정의하면 됩니다.

```
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     */
    public function __invoke()
    {
        // ...
    }
}
```

<!-- When registering routes for single action controllers, you do not need to specify a controller method. Instead, you may simply pass the name of the controller to the router: -->
단일 액션 컨트롤러를 라우트에 등록할 때는 컨트롤러 메서드를 명시하지 않고, 컨트롤러 클래스명만 전달해주면 됩니다.

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` 아티즌 명령어에서 `--invokable` 옵션을 사용하면 단일 액션 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁 파일은 [stub publishing](/docs/10.x/artisan#stub-customization) 기능을 통해 커스텀할 수 있습니다.

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/10.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/10.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 직접 할당할 수 있습니다.

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller's constructor. Using the `middleware` method within your controller's constructor, you can assign middleware to the controller's actions: -->
또는 컨트롤러의 생성자에서 미들웨어를 지정해주는 것도 편리합니다. 생성자 내에서 `middleware` 메서드를 사용하면 컨트롤러의 특정 액션에 미들웨어를 지정할 수 있습니다.

```
class UserController extends Controller
{
    /**
     * Instantiate a new controller instance.
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
컨트롤러에서는 미들웨어를 클로저(익명 함수) 형태로 간편하게 등록할 수도 있습니다. 이를 통해, 별도의 미들웨어 클래스를 만들지 않고 컨트롤러 하나에만 적용되는 인라인 미들웨어를 정의할 수 있습니다.

```
use Closure;
use Illuminate\Http\Request;

$this->middleware(function (Request $request, Closure $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
애플리케이션의 각 Eloquent 모델을 "리소스"로 생각할 때, 보통 각 리소스에 대해 동일한 동작(생성, 조회, 수정, 삭제 등)을 반복해서 수행하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스들을 생성, 읽기, 수정, 삭제할 가능성이 높습니다.

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
이런 흔한 상황을 위해, Laravel 리소스 라우팅은 리소스에 대한 일반적인 CRUD(생성, 읽기, 수정, 삭제) 라우트를 한 줄의 코드로 컨트롤러에 할당해줍니다. 먼저, `make:controller` 아티즌 명령어의 `--resource` 옵션을 사용해, 이런 동작을 처리할 컨트롤러를 빠르게 생성할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
이 명령어는 `app/Http/Controllers/PhotoController.php` 위치에 컨트롤러 파일을 생성합니다. 컨트롤러에는 각 리소스 작업에 맞는 메서드가 이미 포함되어 생성됩니다. 이후에는, 컨트롤러로 연결되는 리소스 라우트를 다음과 같이 등록할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
이 단 한 줄의 라우트 선언으로, 해당 리소스에 대해 다양한 동작을 처리하는 여러 개의 라우트가 한 번에 생성됩니다. 생성된 컨트롤러는 이 모든 동작을 위한 스텁 메서드를 이미 가지고 있습니다. 참고로, 아티즌의 `route:list` 명령어로 애플리케이션의 라우트 구조를 빠르게 확인할 수 있습니다.

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
여러 개의 리소스 컨트롤러를 한 번에 등록하고 싶을 때는 `resources` 메서드에 배열을 전달하면 됩니다.

```
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
<a id="actions-handled-by-resource-controller" data-translation-alias="true"></a>
<!-- #### Actions Handled by Resource Controllers -->
#### Actions Handled by Resource Controllers

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
Verb      | URI                    | 액션         | 라우트 이름
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
일반적으로, 암묵적으로 바인딩된 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만, 리소스 라우트를 정의할 때 `missing` 메서드를 호출해 이 동작을 원하는 대로 정의할 수 있습니다. `missing` 메서드는 클로저를 받으며, 리소스의 어떤 라우트에서든 암묵적으로 바인딩된 모델을 찾을 수 없는 경우 호출됩니다.

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

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/10.x/eloquent#soft-deleting), and will instead return a 404 HTTP response. However, you can instruct the framework to allow soft deleted models by invoking the `withTrashed` method when defining your resource route: -->
기본적으로 암묵적 모델 바인딩은 [soft deleted](/docs/10.x/eloquent#soft-deleting)된 모델을 조회하지 않으며, 이런 경우에도 404 HTTP 응답을 반환합니다. 그러나, 라우트 정의 시에 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 허용할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

<!-- Calling `withTrashed` with no arguments will allow soft deleted models for the `show`, `edit`, and `update` resource routes. You may specify a subset of these routes by passing an array to the `withTrashed` method: -->
`withTrashed`를 인수 없이 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. `withTrashed` 메서드에 배열을 전달하면 이 라우트 중 일부만 지정할 수 있습니다.

```
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
<!-- #### Specifying the Resource Model -->
#### Specifying the Resource Model

<!-- If you are using [route model binding](/docs/10.x/routing#route-model-binding) and would like the resource controller's methods to type-hint a model instance, you may use the `--model` option when generating the controller: -->
[route model binding](/docs/10.x/routing#route-model-binding)을 사용할 때, 리소스 컨트롤러의 메서드가 모델 인스턴스를 타입힌트로 받을 수 있도록 하려면, 컨트롤러를 생성할 때 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/10.x/validation#form-request-validation) for the controller's storage and update methods: -->
리소스 컨트롤러를 생성하면서 `--requests` 옵션을 추가하면, 컨트롤러의 저장 및 수정 메서드를 위한 [form request classes](/docs/10.x/validation#form-request-validation)도 함께 생성해줍니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
리소스 라우트를 선언할 때, 컨트롤러가 기본 제공되는 전체 액션 집합이 아니라 일부 액션만 처리하도록 지정할 수도 있습니다.

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
API에서 사용할 리소스 라우트의 경우, 보통 HTML 템플릿을 제공하는 `create`와 `edit` 라우트가 불필요합니다. 이럴 때는 `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다.

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
여러 개의 API 리소스 컨트롤러를 한 번에 등록하려면 `apiResources` 메서드에 배열로 전달하세요.

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`make:controller` 명령을 실행할 때 `--api` 옵션을 주면, `create` 또는 `edit` 메서드 없이 API 용 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
때로는 중첩된 리소스에 대한 라우트를 정의해야 할 때가 있습니다. 예를 들어, 사진 하나에 여러 개의 댓글이 달릴 수 있습니다. 이런 경우, 라우트 선언에 "닷(dot) 표기법"을 사용해 중첩 리소스 컨트롤러를 지정할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
이렇게 하면 다음과 같은 형태의 URI를 통한 중첩 리소스 접근이 가능합니다.

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/10.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel의 [implicit model binding](/docs/10.x/routing#implicit-model-binding-scoping) 기능을 사용하면, 자식 모델이 지정된 부모 모델에 속하는지 자동으로 확인하고 바인딩할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화할 수 있고, 어떤 필드로 자식 리소스를 조회할지도 지정할 수 있습니다. 자세한 방법은 [scoping resource routes](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
대부분의 경우, URI 내에 부모 ID와 자식 ID를 모두 포함하는 것까지 필요하지 않습니다. 자식 ID(예: 자동 증가 기본키)만으로도 모델을 고유하게 식별할 수 있다면 "단순 중첩(shallow nesting)"을 사용할 수 있습니다.

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
이렇게 정의하면 다음과 같은 라우트가 생성됩니다.

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
Verb      | URI                               | 액션         | 라우트 이름
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
기본적으로, 모든 리소스 컨트롤러 액션은 라우트 이름이 자동으로 지정됩니다. 하지만 `names` 배열을 전달해 원하는 대로 이름을 재정의할 수 있습니다.

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
기본적으로 `Route::resource`는 리소스 이름의 "단수형"을 기준으로 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하면 이를 리소스별로 쉽게 변경할 수 있습니다. `parameters` 메서드로 전달하는 배열은 리소스명과 원하는 파라미터명을 대응시키는 연관 배열이어야 합니다.

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!--  The example above generates the following URI for the resource's `show` route: -->
 위 예시는 해당 리소스의 `show` 라우트를 다음과 같은 URI로 만듭니다:

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/10.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel의 [scoped implicit model binding](/docs/10.x/routing#implicit-model-binding-scoping) 기능은, 자식 모델이 지정된 부모 모델에 속하는지 자동으로 확인하는 역할을 합니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 이 자동 스코핑이 활성화되고, 자식 리소스를 어떤 필드로 검색할 지도 설정할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음의 URI 형태로 스코프된 중첩 리소스를 등록합니다.

```
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
중첩 라우트 파라미터로 커스텀 키를 사용하는 암시적 바인딩의 경우에도, Laravel은 부모 모델에 연결된 자식 모델만 검색하도록 쿼리를 자동으로 스코프합니다. 이때, 예시의 경우 `Photo` 모델에 `comments`(파라미터 이름의 복수형)라는 연관관계가 있다고 가정하고 해당 관계를 사용해 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs and plural rules. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\RouteServiceProvider`: -->
기본적으로 `Route::resource`는 영어 동사, 영어 복수화 규칙을 사용해 리소스 URI를 생성합니다. `create`와 `edit` 등 액션에 사용되는 동사만 현지화(다른 언어로 변경)하려면, 애플리케이션의 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드에서 `Route::resourceVerbs` 메서드를 사용하면 됩니다.

```
/**
 * Define your route model bindings, pattern filters, etc.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);

    // ...
}
```

<!-- Laravel's pluralizer supports [several different languages which you may configure based on your needs](/docs/10.x/localization#pluralization-language). Once the verbs and pluralization language have been customized, a resource route registration such as `Route::resource('publicacion', PublicacionController::class)` will produce the following URIs: -->
Laravel의 복수화(pluralizer) 기능은 [several different languages which you may configure based on your needs](/docs/10.x/localization#pluralization-language)합니다. 동사 및 복수화 언어를 변경하면, `Route::resource('publicacion', PublicacionController::class)`와 같은 리소스 라우트를 등록할 때 다음과 같은 URI가 생성됩니다.

```
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
기본 리소스 라우트 외에 특정 컨트롤러에 추가적인 라우트를 등록하려면, 반드시 `Route::resource`를 호출하기 전에 추가 라우트를 먼저 정의해야 합니다. 그렇지 않으면, `resource` 메서드가 만드는 라우트가 보충 라우트를 덮어쓸 수 있습니다.

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러는 한 가지 목적에 집중되게 작성하는 것이 좋습니다. 자주 추가적인 메서드가 필요하다면, 컨트롤러를 두 개 이상의 작은 컨트롤러로 나누는 것도 고려하세요.

<a name="singleton-resource-controllers"></a>
<!-- ### Singleton Resource Controllers -->
### Singleton Resource Controllers

<!-- Sometimes, your application will have resources that may only have a single instance. For example, a user's "profile" can be edited or updated, but a user may not have more than one "profile". Likewise, an image may have a single "thumbnail". These resources are called "singleton resources", meaning one and only one instance of the resource may exist. In these scenarios, you may register a "singleton" resource controller: -->
때때로, 애플리케이션 내에는 한 인스턴스만 존재할 수 있는 리소스가 있습니다. 예를 들어, 사용자의 "프로필"은 한 명의 사용자마다 하나만 존재하며, 이미지의 "썸네일(Thumbnail)" 리소스도 마찬가지입니다. 이렇게 반드시 하나만 존재하는 리소스를 "싱글턴(Singleton) 리소스"라고 하며, 이 경우에는 "싱글턴 리소스 컨트롤러"를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

<!-- The singleton resource definition above will register the following routes. As you can see, "creation" routes are not registered for singleton resources, and the registered routes do not accept an identifier since only one instance of the resource may exist: -->
위의 싱글턴 리소스 라우트 정의는 다음과 같은 라우트를 등록합니다. 보시다시피, 생성용(create) 라우트는 등록되지 않고, 단순히 인스턴스 하나만 표시/수정/업데이트만 가능합니다(식별자 파라미터 없음).

<!--
Verb      | URI                               | Action       | Route Name
----------|-----------------------------------|--------------|---------------------
GET       | `/profile`                        | show         | profile.show
GET       | `/profile/edit`                   | edit         | profile.edit
PUT/PATCH | `/profile`                        | update       | profile.update
-->
Verb      | URI                               | 액션         | 라우트 이름
----------|-----------------------------------|--------------|---------------------
GET       | `/profile`                        | show         | profile.show
GET       | `/profile/edit`                   | edit         | profile.edit
PUT/PATCH | `/profile`                        | update       | profile.update

<!-- Singleton resources may also be nested within a standard resource: -->
싱글턴 리소스는 표준 리소스 내부에 중첩해서 등록할 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

<!-- In this example, the `photos` resource would receive all of the [standard resource routes](#actions-handled-by-resource-controller); however, the `thumbnail` resource would be a singleton resource with the following routes: -->
이 예제에서는 `photos` 리소스는 [standard resource routes](#actions-handled-by-resource-controller)를 모두 갖지만, `thumbnail` 리소스는 다음과 같이 싱글턴 리소스로 등록됩니다.

| Verb      | URI                              | 액션    | 라우트 이름               |
|-----------|----------------------------------|---------|--------------------------|
| GET       | `/photos/{photo}/thumbnail`      | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit` | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update  | photos.thumbnail.update  |

<a name="creatable-singleton-resources"></a>
<!-- #### Creatable Singleton Resources -->
#### Creatable Singleton Resources

<!-- Occasionally, you may want to define creation and storage routes for a singleton resource. To accomplish this, you may invoke the `creatable` method when registering the singleton resource route: -->
때로는 싱글턴 리소스에 대해 생성 및 저장 라우트까지 정의하고 싶을 수 있습니다. 이럴 때는 싱글턴 리소스 등록 시 `creatable` 메서드를 덧붙여 주면 됩니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

<!-- In this example, the following routes will be registered. As you can see, a `DELETE` route will also be registered for creatable singleton resources: -->
이렇게 하면, 아래와 같이 `DELETE` 라우트도 포함해 더 많은 라우트가 등록됩니다.

| Verb      | URI                                | 액션    | 라우트 이름               |
|-----------|------------------------------------|---------|--------------------------|
| GET       | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy |

<!-- If you would like Laravel to register the `DELETE` route for a singleton resource but not register the creation or storage routes, you may utilize the `destroyable` method: -->
싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 싶고, 생성이나 저장 라우트는 굳이 필요 없으면, `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
<!-- #### API Singleton Resources -->
#### API Singleton Resources

<!-- The `apiSingleton` method may be used to register a singleton resource that will be manipulated via an API, thus rendering the `create` and `edit` routes unnecessary: -->
`apiSingleton` 메서드는 API를 통해 제어할 싱글턴 리소스를 등록할 때 사용할 수 있으며, 이 경우에는 `create`, `edit` 라우트가 포함되지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

<!-- Of course, API singleton resources may also be `creatable`, which will register `store` and `destroy` routes for the resource: -->
API 싱글턴 리소스 역시 `creatable` 메서드를 추가해주면 `store`와 `destroy` 라우트까지 등록할 수 있습니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="dependency-injection-and-controllers"></a>
<!-- ## Dependency Injection and Controllers -->
## Dependency Injection and Controllers

<a name="constructor-injection"></a>
<!-- #### Constructor Injection -->
#### Constructor Injection

<!-- The Laravel [service container](/docs/10.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel의 [service container](/docs/10.x/container)는 모든 컨트롤러를 해결(resolve)하는 데 사용됩니다. 덕분에, 컨트롤러의 생성자에서 필요한 의존성을 타입힌트로 선언해주면, 자동으로 인스턴스가 주입됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```

<a name="method-injection"></a>
<!-- #### Method Injection -->
#### Method Injection

<!-- In addition to constructor injection, you may also type-hint dependencies on your controller's methods. A common use-case for method injection is injecting the `Illuminate\Http\Request` instance into your controller methods: -->
생성자 주입 외에도, 컨트롤러의 메서드에서 필요한 의존성을 타입힌트로 선언해 메서드 주입을 사용할 수 있습니다. 가장 대표적인 예시가 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 경우입니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // Store the user...

        return redirect('/users');
    }
}
```

<!-- If your controller method is also expecting input from a route parameter, list your route arguments after your other dependencies. For example, if your route is defined like so: -->
컨트롤러 메서드에서 라우트 파라미터 값을 함께 받아야 한다면, 의존성 인자 다음에 라우트 파라미터 인수를 위치시키면 됩니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다면,

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
아래와 같이 `Illuminate\Http\Request`와 라우트 파라미터인 `id`를 함께 컨트롤러 메서드에서 받을 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```
