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
모든 요청 처리 로직을 라우트 파일에서 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이러한 동작을 체계적으로 관리할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스에 모아둘 수 있습니다. 예를 들어, `UserController` 클래스가 사용자의 조회, 생성, 수정, 삭제 등과 같이 사용자와 관련된 모든 요청을 처리하도록 할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- Let's take a look at an example of a basic controller. Note that the controller extends the base controller class included with Laravel: `App\Http\Controllers\Controller`: -->
기본적인 컨트롤러 예제를 살펴보겠습니다. 이 컨트롤러는 Laravel에 내장된 기본 컨트롤러 클래스인 `App\Http\Controllers\Controller`를 확장합니다.

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
아래와 같이 이 컨트롤러 메서드에 대한 라우트를 정의할 수 있습니다.

```
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
들어오는 요청이 지정한 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 해당 메서드에 전달됩니다.

> [!TIP]
> 컨트롤러는 반드시 기본 클래스를 **상속할 필요는 없습니다**. 그러나 기본 클래스를 상속하지 않으면 `middleware`, `authorize`와 같은 편리한 기능을 사용할 수 없습니다.

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
컨트롤러에서 처리하는 액션이 아주 복잡하다면, 해당 액션만을 위한 전용 컨트롤러 클래스를 만드는 것이 편할 수 있습니다. 이럴 때는 컨트롤러 안에 `__invoke` 메서드만 하나 정의하면 됩니다.

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
단일 액션 컨트롤러에 라우트를 등록할 때는, 컨트롤러 메서드명을 따로 지정하지 않고, 컨트롤러 이름만 라우터에 넘기면 됩니다.

```
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용해 인보커블(단일 액션) 컨트롤러를 생성할 수 있습니다.

```
php artisan make:controller ProvisionServer --invokable
```

> [!TIP]
> 컨트롤러 스텁은 [stub publishing](/docs/8.x/artisan#stub-customization)를 통해 커스터마이즈 할 수 있습니다.

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/8.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/8.x/middleware)는 라우트 파일 내 컨트롤러 라우트에 지정할 수 있습니다.

```
Route::get('profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller's constructor. Using the `middleware` method within your controller's constructor, you can assign middleware to the controller's actions: -->
혹은 컨트롤러의 생성자에서 미들웨어를 지정하는 것이 더 편리할 수도 있습니다. 컨트롤러의 생성자 안에서 `middleware` 메서드를 사용하면, 컨트롤러의 특정 액션에 미들웨어를 할당할 수 있습니다.

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
컨트롤러에서는 미들웨어를 클로저로도 등록할 수 있습니다. 즉, 하나의 컨트롤러에서만 사용할 인라인 미들웨어를 전체 미들웨어 클래스를 따로 정의하지 않고 쉽게 만들 수 있습니다.

```
$this->middleware(function ($request, $next) {
    return $next($request);
});
```

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
애플리케이션의 각 Eloquent 모델을 "리소스"로 생각해 보면, 보통 각 리소스별로 비슷한 작업(생성, 조회, 수정, 삭제 등)을 반복하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스들을 생성, 조회, 수정, 삭제할 가능성이 높습니다.

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
이처럼 자주 반복되는 경우를 위해, Laravel의 리소스 라우팅은 한 줄의 코드로 전형적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 컨트롤러에 할당해 줍니다. 먼저, `make:controller` Artisan 명령어에 `--resource` 옵션을 사용해 이러한 동작을 처리할 컨트롤러를 쉽게 생성할 수 있습니다.

```
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
위 명령어는 `app/Http/Controllers/PhotoController.php` 경로에 컨트롤러를 생성하며, 리소스별 작업을 위한 메서드가 포함되어 있습니다. 다음으로, 생성한 컨트롤러로 리소스 라우트를 등록합니다.

```
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
이 한 줄의 라우트 선언으로 해당 리소스에 다양한 작업을 처리하는 여러 라우트가 즉시 생성됩니다. 만들어진 컨트롤러는 각각의 액션에 대한 스텁 메서드를 이미 포함하고 있습니다. 애플리케이션의 전체 라우트를 빠르게 확인하고 싶을 때는 `route:list` Artisan 명령어를 실행하면 됩니다.

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
아래와 같이 `resources` 메서드에 배열을 넘기면 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

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
일반적으로, 암묵적으로 바인딩된 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만, `missing` 메서드를 이용해 리소스 라우트에 대한 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델을 찾을 수 없을 때 호출되는 클로저를 인자로 받습니다.

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
[route model binding](/docs/8.x/routing#route-model-binding)을 활용하며, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트로 지정하고 싶다면, 컨트롤러를 생성할 때 `--model` 옵션을 사용할 수 있습니다.

```
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/8.x/validation#form-request-validation) for the controller's storage and update methods: -->
리소스 컨트롤러를 생성할 때 `--requests` 옵션도 함께 주면, 컨트롤러의 저장 및 수정 메서드에서 사용할 [form request classes](/docs/8.x/validation#form-request-validation)가 Artisan에 의해 자동 생성됩니다.

```
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
리소스 라우트를 선언할 때, 컨트롤러가 전체 기본 액션 대신 일부 액션만 처리하도록 지정할 수 있습니다.

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
API에서 사용될 리소스 라우트를 선언할 때는, `create`와 `edit`처럼 HTML 템플릿을 제공하는 라우트를 보통 제외하게 됩니다. 이런 경우를 위해 `apiResource` 메서드를 사용하면 두 라우트가 자동으로 빠집니다.

```
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
`apiResources` 메서드에 배열을 전달하면 여러 API 리소스 컨트롤러를 한 번에 등록할 수 있습니다.

```
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면, `create`나 `edit` 메서드 없이 빠르게 API 리소스 컨트롤러를 생성할 수 있습니다.

```
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
경우에 따라 중첩된 리소스에 대한 라우트가 필요할 수 있습니다. 예를 들어, 포토 리소스에는 여러 개의 댓글이 달릴 수 있습니다. 이런 중첩 리소스 컨트롤러를 라우트 선언에서 "점" 표기법으로 정의할 수 있습니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같은 URI로 중첩 리소스를 접근할 수 있게 됩니다.

```
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel의 [implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) 기능을 이용하면, 고유적으로 스코프된 중첩 바인딩이 가능해집니다. 즉, 자식 모델이 반드시 부모 모델에 속해 있는지 확인하는 방식입니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 스코핑을 활성화할 수 있고, 자식 리소스를 어떤 필드로 조회할지도 지정할 수 있습니다. 자세한 내용은 [scoping resource routes](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
일반적으로, 자식 리소스의 ID가 이미 고유한 경우 URI에 부모와 자식 ID를 모두 포함할 필요가 없습니다. 예를 들어, 오토 인크리먼트된 기본 키 등 고유 식별자를 URI 세그먼트로 사용하는 경우, "얕은(Shallow) 중첩"을 선택할 수 있습니다.

```
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
해당 라우트 정의는 아래와 같은 라우트를 만듭니다.

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
기본적으로 리소스 컨트롤러의 모든 액션에는 라우트 이름이 자동으로 지정되지만, `names` 배열을 넘겨 원하는 이름으로 직접 지정할 수도 있습니다.

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
기본적으로 `Route::resource`는 "단수화된" 리소스 이름을 기준으로 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하면 이를 리소스별로 쉽게 변경할 수 있습니다. `parameters` 메서드에 넘기는 배열은 리소스명과 파라미터명을 매칭하는 연관 배열이어야 합니다.

```
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!--  The example above generates the following URI for the resource's `show` route: -->
위 예제는 리소스의 `show` 라우트에 대해 다음과 같은 URI를 생성합니다.

```
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel의 [scoped implicit model binding](/docs/8.x/routing#implicit-model-binding-scoping)는 중첩된 라우트에서 자식 모델이 반드시 부모 모델에 속하는지 자동으로 확인해 줍니다. 중첩 리소스를 정의할 때 `scoped` 메서드로 자동 스코핑을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회할지도 간편하게 지정 가능합니다.

```
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같이 스코프된 중첩 리소스를 사용할 수 있게 만듭니다.

```
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
커스텀 키를 사용하는 암묵적 바인딩을 중첩 라우트 파라미터로 쓰면, Laravel은 부모 관계명을 추측해서 쿼리를 자동으로 스코프 처리합니다. 위 예시에서는 `Photo` 모델에 `comments`(파라미터 이름의 복수형)라는 관계가 있다고 간주하여 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\RouteServiceProvider`: -->
기본적으로 `Route::resource`는 리소스 URI에 영어 동사를 사용합니다. 만약 `create`와 `edit` 액션의 동사를 현지화(다른 언어로 변경)하려면, 애플리케이션의 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드 초입에서 `Route::resourceVerbs` 메서드를 사용할 수 있습니다.

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
동사를 커스터마이징 한 뒤, 예를 들어 `Route::resource('fotos', PhotoController::class)`를 등록하면, 아래와 같은 URI가 생성됩니다.

```
/fotos/crear

/fotos/{foto}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
기본 리소스 라우트 외에 추가 라우트가 필요하다면, 반드시 `Route::resource` 호출 **이전**에 보조 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드가 생성하는 라우트가 직접 정의한 추가 라우트보다 우선 적용될 수 있습니다.

```
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!TIP]
> 컨트롤러의 책임을 명확히 하세요. 만약 리소스 기본 액션 외의 메서드가 자주 필요하다면, 컨트롤러를 더 작고 목적별로 분리하는 것이 좋습니다.

<a name="dependency-injection-and-controllers"></a>
<!-- ## Dependency Injection & Controllers -->
## Dependency Injection & Controllers

<a name="constructor-injection"></a>
<!-- #### Constructor Injection -->
#### Constructor Injection

<!-- The Laravel [service container](/docs/8.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel의 [service container](/docs/8.x/container)는 모든 컨트롤러를 자동으로 resolve(해결)합니다. 따라서, 컨트롤러의 생성자에 필요한 의존성을 타입힌트로 지정하면 Laravel이 자동으로 주입해 줍니다. 아래 예제를 참고하세요.

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
생성자 인젝션 외에도, 컨트롤러의 메서드에 타입힌트로 의존성을 전달받을 수 있습니다. 가장 흔한 예시로, `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입할 수 있습니다.

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
컨트롤러 메서드가 라우트 파라미터도 함께 받는 경우, 의존성 뒤에 라우트 인수를 차례로 나열하면 됩니다. 예를 들어, 다음과 같은 라우트가 있다면

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
컨트롤러 메서드를 아래와 같이 정의해 `Illuminate\Http\Request`를 타입힌트로 받고, 라우트 인수인 `id`를 뒤에 추가로 받을 수 있습니다.

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
