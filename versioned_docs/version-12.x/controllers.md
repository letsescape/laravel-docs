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
    - [Middleware and Resource Controllers](#middleware-and-resource-controllers)
- [Dependency Injection and Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controllers are stored in the `app/Http/Controllers` directory. -->
라우트 파일에 모든 요청 처리 로직을 클로저(Closure)로 정의하는 대신, "컨트롤러(controller)" 클래스를 사용해 이 동작을 구조화할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스에 모을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- To quickly generate a new controller, you may run the `make:controller` Artisan command. By default, all of the controllers for your application are stored in the `app/Http/Controllers` directory: -->
새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 사용할 수 있습니다. 기본적으로 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

```shell
php artisan make:controller UserController
```

<!-- Let's take a look at an example of a basic controller. A controller may have any number of public methods which will respond to incoming HTTP requests: -->
기본적인 컨트롤러 예제를 살펴보겠습니다. 컨트롤러는 여러 개의 public 메서드를 가질 수 있으며, 각각 HTTP 요청을 처리합니다.

```php
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
컨트롤러 클래스와 메서드를 작성한 후에는 다음과 같이 해당 컨트롤러 메서드로 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 베이스 클래스를 상속할 필요는 **없습니다**. 하지만, 모든 컨트롤러에서 공통으로 사용할 메서드를 포함하는 베이스 컨트롤러 클래스를 상속하는 것이 편리할 때도 있습니다.

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
컨트롤러 액션이 특별히 복잡하다면, 단일 액션을 전담하는 컨트롤러 클래스를 따로 만드는 것이 더 편리할 수 있습니다. 이를 위해 컨트롤러 내에 단일 `__invoke` 메서드를 정의하면 됩니다.

```php
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
단일 액션 컨트롤러를 라우트에 등록할 때는, 메서드명을 지정할 필요 없이 컨트롤러 이름만 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` Artisan 명령어에서 `--invokable` 옵션을 사용하면 호출 가능한(invokable) 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [stub publishing](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/12.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/12.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller class. To do so, your controller should implement the `HasMiddleware` interface, which dictates that the controller should have a static `middleware` method. From this method, you may return an array of middleware that should be applied to the controller's actions: -->
또는, 컨트롤러 클래스 내부에서 미들웨어를 지정하는 방식이 더 편리할 수 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 static `middleware` 메서드가 있어야 함을 명시합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    /**
     * Get the middleware that should be assigned to the controller.
     */
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }

    // ...
}
```

<!-- You may also define controller middleware as closures, which provides a convenient way to define an inline middleware without writing an entire middleware class: -->
클로저(Closure) 형태로 컨트롤러 미들웨어를 정의할 수도 있어, 별도의 미들웨어 클래스를 작성하지 않고 인라인 미들웨어를 간편하게 사용할 수 있습니다.

```php
use Closure;
use Illuminate\Http\Request;

/**
 * Get the middleware that should be assigned to the controller.
 */
public static function middleware(): array
{
    return [
        function (Request $request, Closure $next) {
            return $next($request);
        },
    ];
}
```

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
애플리케이션 내의 각 Eloquent 모델을 "리소스(resource)"로 본다면, 보통 해당 리소스에 대해 동일한 패턴의 동작을 적용하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
이처럼 흔하게 사용되는 패턴을 위해, Laravel의 리소스 라우팅은 일반적인 생성(Create), 조회(Read), 수정(Update), 삭제(Delete) 즉, "CRUD" 라우트를 한 줄의 코드로 컨트롤러에 할당해줍니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 이러한 동작을 처리할 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각 리소스 동작에 맞는 메서드를 포함하고 있습니다. 그 다음, 해당 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
이 한 줄의 라우트 선언은 리소스에 다양한 동작을 처리하는 여러 라우트를 자동으로 생성합니다. 생성된 컨트롤러에는 이미 이러한 동작을 위한 스텁 메서드들이 정의되어 있습니다. 참고로, `route:list` Artisan 명령어를 실행하면 애플리케이션의 모든 라우트를 빠르게 확인할 수 있습니다.

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
여러 리소스 컨트롤러를 동시에 등록하려면 배열을 `resources` 메서드에 전달하면 됩니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- The `softDeletableResources` method registers many resources controllers that all use the `withTrashed` method: -->
`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 여러 리소스 컨트롤러를 한 번에 등록합니다.

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
<!-- #### Actions Handled by Resource Controllers -->
#### Actions Handled by Resource Controllers

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| HTTP 메서드 | URI                        | 액션    | 라우트 이름           |
| ----------- | -------------------------- | ------- | --------------------- |
| GET         | `/photos`                  | index   | photos.index          |
| GET         | `/photos/create`           | create  | photos.create         |
| POST        | `/photos`                  | store   | photos.store          |
| GET         | `/photos/{photo}`          | show    | photos.show           |
| GET         | `/photos/{photo}/edit`     | edit    | photos.edit           |
| PUT/PATCH   | `/photos/{photo}`          | update  | photos.update         |
| DELETE      | `/photos/{photo}`          | destroy | photos.destroy        |

<!-- </div> -->
</div>

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound resource model is not found. However, you may customize this behavior by calling the `missing` method when defining your resource route. The `missing` method accepts a closure that will be invoked if an implicitly bound model cannot be found for any of the resource's routes: -->
보통, 암묵적으로 바인딩된 리소스 모델을 찾을 수 없을 때는 404 HTTP 응답이 반환됩니다. 그러나, 리소스 라우트 정의 시 `missing` 메서드를 호출하여 이 동작을 사용자 지정할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델이 각 리소스의 라우트에서 발견되지 않았을 때 실행할 클로저를 받습니다.

```php
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

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/12.x/eloquent#soft-deleting), and will instead return a 404 HTTP response. However, you can instruct the framework to allow soft deleted models by invoking the `withTrashed` method when defining your resource route: -->
일반적으로, 암묵적 모델 바인딩은 [soft deleted](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않으며, 대신 404 HTTP 응답을 반환합니다. 하지만, `withTrashed` 메서드를 라우트에 적용하면 소프트 삭제된 모델도 조회하도록 할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

<!-- Calling `withTrashed` with no arguments will allow soft deleted models for the `show`, `edit`, and `update` resource routes. You may specify a subset of these routes by passing an array to the `withTrashed` method: -->
인자를 주지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 라우트에 대해 소프트 삭제된 모델을 허용합니다. `withTrashed` 메서드에 배열을 전달하면 이 라우트들 중 일부만 지정할 수도 있습니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
<!-- #### Specifying the Resource Model -->
#### Specifying the Resource Model

<!-- If you are using [route model binding](/docs/12.x/routing#route-model-binding) and would like the resource controller's methods to type-hint a model instance, you may use the `--model` option when generating the controller: -->
[route model binding](/docs/12.x/routing#route-model-binding)을 사용하고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트하고 싶다면, 컨트롤러 생성시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/12.x/validation#form-request-validation) for the controller's storage and update methods: -->
리소스 컨트롤러 생성 시 `--requests` 옵션을 추가하면, Artisan이 컨트롤러의 저장 및 갱신 메서드를 위한 [form request classes](/docs/12.x/validation#form-request-validation)도 함께 생성합니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
리소스 라우트를 선언할 때, 전체 기본 액션 대신 컨트롤러가 처리할 액션만 부분적으로 지정할 수 있습니다.

```php
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
API에서 사용될 리소스 라우트를 선언할 경우, 보통은 HTML 템플릿을 보여주는 `create`, `edit` 라우트가 필요하지 않습니다. 편의를 위해, `apiResource` 메서드를 사용하면 이 두 라우트가 자동으로 제외됩니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
`apiResources` 메서드에 배열을 전달하면 여러 API 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면, `create`와 `edit` 메서드가 포함되지 않는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
때때로 한 리소스에 중첩된 하위 리소스가 필요할 수 있습니다. 예를 들어, 하나의 사진에는 여러 개의 댓글이 달릴 수 있습니다. 이러한 중첩 리소스를 위해 라우트 선언 시 "점(dot) 표기법"을 사용합니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같은 URI로 중첩 리소스를 사용할 수 있게 해줍니다.

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/12.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel의 [implicit model binding](/docs/12.x/routing#implicit-model-binding-scoping) 기능을 활용하면, 중첩된 리소스가 부모 모델에 속하는지 자동으로 확인하고 바인딩할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화하고, 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다. 자세한 내용은 [scoping resource routes](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
종종, 자식 ID가 이미 고유 식별자인 경우에는 URI에 부모와 자식 ID를 모두 포함할 필요가 없습니다. 예를 들어, 자동 증가하는 기본 키 등의 고유 식별자를 URI 세그먼트로 사용하는 경우, "shallow nesting(얕은 중첩)"을 사용할 수 있습니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
이 라우트 정의는 아래와 같은 라우트를 생성합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| HTTP 메서드 | URI                                   | 액션    | 라우트 이름                |
| ----------- | ------------------------------------- | ------- | -------------------------- |
| GET         | `/photos/{photo}/comments`            | index   | photos.comments.index      |
| GET         | `/photos/{photo}/comments/create`     | create  | photos.comments.create     |
| POST        | `/photos/{photo}/comments`            | store   | photos.comments.store      |
| GET         | `/comments/{comment}`                 | show    | comments.show              |
| GET         | `/comments/{comment}/edit`            | edit    | comments.edit              |
| PUT/PATCH   | `/comments/{comment}`                 | update  | comments.update            |
| DELETE      | `/comments/{comment}`                 | destroy | comments.destroy           |

<!-- </div> -->
</div>

<a name="restful-naming-resource-routes"></a>
<!-- ### Naming Resource Routes -->
### Naming Resource Routes

<!-- By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your desired route names: -->
기본적으로, 모든 리소스 컨트롤러의 액션에는 라우트 이름이 자동으로 부여됩니다. 그러나, `names` 배열을 전달하여 원하는 라우트 이름으로 오버라이드할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
<!-- ### Naming Resource Route Parameters -->
### Naming Resource Route Parameters

<!-- By default, `Route::resource` will create the route parameters for your resource routes based on the "singularized" version of the resource name. You can easily override this on a per resource basis using the `parameters` method. The array passed into the `parameters` method should be an associative array of resource names and parameter names: -->
`Route::resource`는 리소스 이름의 "단수형"을 사용해 기본적으로 라우트 파라미터를 생성합니다. 이 동작은 `parameters` 메서드를 통해 리소스별로 변경할 수 있습니다. `parameters`에는 리소스 이름과 파라미터 이름을 매핑한 연관 배열을 전달합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!-- The example above generates the following URI for the resource's `show` route: -->
위 예시에서 생성되는 라우트의 `show` URI는 다음과 같습니다.

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/12.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel의 [scoped implicit model binding](/docs/12.x/routing#implicit-model-binding-scoping) 기능을 활용하면, 중첩된 모델의 부모-자식 소속이 자동으로 검증됩니다. `scoped` 메서드로 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같은 URI로 중첩된 리소스를 스코프하여 활용할 수 있습니다.

```text
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
사용자 정의 키가 적용된 암묵적 바인딩을 중첩 라우트 파라미터로 사용할 때, Laravel은 관례에 따라 부모 모델의 연관관계 이름을 추측하여 부모를 통해 중첩 모델을 조회하도록 쿼리 범위를 자동으로 지정합니다. 이 경우 `Photo` 모델에 `comments`(라우트 파라미터 이름의 복수형)라는 연관관계가 있다고 가정하며, 이를 사용해 `Comment` 모델을 조회합니다.

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs and plural rules. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\AppServiceProvider`: -->
기본적으로 `Route::resource`는 영어 동사와 복수화 규칙(plural rule)을 사용해 리소스 URI를 생성합니다. `create`와 `edit` 액션의 동사를 현지화해야 한다면, `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이 설정은 애플리케이션의 `App\Providers\AppServiceProvider` 내의 `boot` 메서드에서 지정할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```

<!-- Laravel's pluralizer supports [several different languages which you may configure based on your needs](/docs/12.x/localization#pluralization-language). Once the verbs and pluralization language have been customized, a resource route registration such as `Route::resource('publicacion', PublicacionController::class)` will produce the following URIs: -->
Laravel의 복수화(pluralizer) 기능은 [several different languages which you may configure based on your needs](/docs/12.x/localization#pluralization-language)하며, 필요에 따라 설정할 수 있습니다. 동사와 복수화 언어를 사용자 지정하면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`은 아래와 같은 URI를 생성합니다.

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
리소스 컨트롤러에 기본 리소스 라우트 외에 추가적인 라우트를 더해야 하는 경우, 반드시 `Route::resource` 호출 **이전**에 직접 라우트를 정의해야 합니다. 그렇지 않으면 `resource`에서 생성된 라우트가 추가 라우트보다 우선 처리되어 의도와 다르게 동작할 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러의 책임을 명확하게 유지하세요. 일반적인 리소스 액션 외에 별도의 메서드가 자주 필요하다면, 컨트롤러를 두 개의 더 작은 컨트롤러로 분리하는 것이 더 좋을 수 있습니다.

<a name="singleton-resource-controllers"></a>
<!-- ### Singleton Resource Controllers -->
### Singleton Resource Controllers

<!-- Sometimes, your application will have resources that may only have a single instance. For example, a user's "profile" can be edited or updated, but a user may not have more than one "profile". Likewise, an image may have a single "thumbnail". These resources are called "singleton resources", meaning one and only one instance of the resource may exist. In these scenarios, you may register a "singleton" resource controller: -->
애플리케이션 내에는 단일 인스턴스만 존재할 수 있는 리소스가 있을 수 있습니다. 예를 들어, 사용자 "프로필"은 수정할 수 있지만 하나만 존재하며, 이미지의 "썸네일"도 한 개만 존재해야 할 수 있습니다. 이런 리소스는 "싱글턴 리소스(singleton resource)"라고 하며, 오직 하나의 인스턴스만 허용합니다. 이 경우, "singleton" 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

<!-- The singleton resource definition above will register the following routes. As you can see, "creation" routes are not registered for singleton resources, and the registered routes do not accept an identifier since only one instance of the resource may exist: -->
위의 싱글턴 리소스 정의는 아래와 같은 라우트를 등록합니다. "생성"용 라우트는 등록되지 않으며, 단일 인스턴스만 존재하므로 파라미터 없이 라우트가 정의됩니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| HTTP 메서드 | URI               | 액션   | 라우트 이름        |
| ----------- | ----------------- | ------ | ------------------ |
| GET         | `/profile`        | show   | profile.show       |
| GET         | `/profile/edit`   | edit   | profile.edit       |
| PUT/PATCH   | `/profile`        | update | profile.update     |

<!-- </div> -->
</div>

<!-- Singleton resources may also be nested within a standard resource: -->
싱글턴 리소스는 표준 리소스에 중첩시킬 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

<!-- In this example, the `photos` resource would receive all of the [standard resource routes](#actions-handled-by-resource-controllers); however, the `thumbnail` resource would be a singleton resource with the following routes: -->
이 경우, `photos` 리소스는 [standard resource routes](#actions-handled-by-resource-controllers)를 모두 가지게 되며, `thumbnail` 리소스는 아래와 같은 싱글턴 리소스 라우트를 갖게 됩니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| HTTP 메서드 | URI                              | 액션   | 라우트 이름                  |
| ----------- | -------------------------------- | ------ | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update      |

<!-- </div> -->
</div>

<a name="creatable-singleton-resources"></a>
<!-- #### Creatable Singleton Resources -->
#### Creatable Singleton Resources

<!-- Occasionally, you may want to define creation and storage routes for a singleton resource. To accomplish this, you may invoke the `creatable` method when registering the singleton resource route: -->
경우에 따라, 싱글턴 리소스에 대한 생성(create) 및 저장(store) 라우트가 필요할 수 있습니다. 이럴 때는 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 호출합니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

<!-- In this example, the following routes will be registered. As you can see, a `DELETE` route will also be registered for creatable singleton resources: -->
이 경우 아래의 라우트들이 등록됩니다. 또한 `DELETE` 라우트도 생성됩니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| HTTP 메서드 | URI                                    | 액션    | 라우트 이름                    |
| ----------- | -------------------------------------- | ------- | ------------------------------ |
| GET         | `/photos/{photo}/thumbnail/create`     | create  | photos.thumbnail.create        |
| POST        | `/photos/{photo}/thumbnail`            | store   | photos.thumbnail.store         |
| GET         | `/photos/{photo}/thumbnail`            | show    | photos.thumbnail.show          |
| GET         | `/photos/{photo}/thumbnail/edit`       | edit    | photos.thumbnail.edit          |
| PUT/PATCH   | `/photos/{photo}/thumbnail`            | update  | photos.thumbnail.update        |
| DELETE      | `/photos/{photo}/thumbnail`            | destroy | photos.thumbnail.destroy       |

<!-- </div> -->
</div>

<!-- If you would like Laravel to register the `DELETE` route for a singleton resource but not register the creation or storage routes, you may utilize the `destroyable` method: -->
싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 싶고, 생성(create) 또는 저장(store) 라우트는 필요가 없다면 `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
<!-- #### API Singleton Resources -->
#### API Singleton Resources

<!-- The `apiSingleton` method may be used to register a singleton resource that will be manipulated via an API, thus rendering the `create` and `edit` routes unnecessary: -->
`apiSingleton` 메서드는 API에서 사용할 싱글턴 리소스를 등록할 때 사용합니다. 이 경우 `create`와 `edit` 라우트가 등록되지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

<!-- Of course, API singleton resources may also be `creatable`, which will register `store` and `destroy` routes for the resource: -->
물론, API 싱글턴 리소스도 `creatable`로 지정하면 해당 리소스에 대한 `store`, `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```
<a name="middleware-and-resource-controllers"></a>
<!-- ### Middleware and Resource Controllers -->
### Middleware and Resource Controllers

<!-- Laravel allows you to assign middleware to all, or only specific, methods of resource routes using the `middleware`, `middlewareFor`, and `withoutMiddlewareFor` methods. These methods provide fine-grained control over which middleware is applied to each resource action. -->
Laravel은 리소스 또는 싱글턴 리소스 라우트에서, 전체 또는 특정 메서드에 미들웨어를 할당할 수 있도록 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 지원합니다. 이 메서드들은 각 리소스 액션별로 미들웨어 적용을 세밀하게 제어할 수 있게 합니다.

<!-- #### Applying Middleware to all Methods -->
#### Applying Middleware to all Methods

<!-- You may use the `middleware` method to assign middleware to all routes generated by a resource or singleton resource route: -->
`middleware` 메서드를 사용하면 리소스 또는 싱글턴 리소스 라우트에서 생성된 모든 라우트에 미들웨어를 할당할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

<!-- #### Applying Middleware to Specific Methods -->
#### Applying Middleware to Specific Methods

<!-- You may use the `middlewareFor` method to assign middleware to one or more specific methods of a given resource controller: -->
`middlewareFor` 메서드는 지정한 리소스 컨트롤러의 특정 메서드에 미들웨어를 할당할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```

<!-- The `middlewareFor` method may also be used in conjunction with singleton and API singleton resource controllers: -->
`middlewareFor` 메서드는 싱글턴 및 API 싱글턴 리소스 컨트롤러와도 함께 사용할 수 있습니다.

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

<!-- #### Excluding Middleware from Specific Methods -->
#### Excluding Middleware from Specific Methods

<!-- You may use the `withoutMiddlewareFor` method to exclude middleware from specific methods of a resource controller: -->
`withoutMiddlewareFor` 메서드를 사용하면 리소스 컨트롤러의 특정 메서드에서 지정한 미들웨어를 제외할 수 있습니다.

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```

<a name="dependency-injection-and-controllers"></a>
<!-- ## Dependency Injection and Controllers -->
## Dependency Injection and Controllers

<a name="constructor-injection"></a>
<!-- #### Constructor Injection -->
#### Constructor Injection

<!-- The Laravel [service container](/docs/12.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel의 [service container](/docs/12.x/container)는 모든 컨트롤러 인스턴스를 생성할 때 사용됩니다. 따라서, 컨트롤러 생성자에서 타입힌트된 어떤 의존성(dependency)도 주입받을 수 있습니다. 명시한 의존성은 자동으로 주입되어 컨트롤러 인스턴스에서 사용할 수 있습니다.

```php
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
생성자 인젝션뿐만 아니라, 컨트롤러의 메서드에서도 의존성을 타입힌트로 지정할 수 있습니다. 대표적인 예로, `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 경우가 많습니다.

```php
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
컨트롤러 메서드에서 라우트 파라미터 값도 필요하다면, 의존성 객체 다음에 라우트 인수를 명시하면 됩니다. 예를 들어, 아래와 같이 라우트를 정의했다면

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
컨트롤러 메서드에서 다음과 같이 `Illuminate\Http\Request`와 `id` 파라미터를 받을 수 있습니다.

```php
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
