<!-- # Controllers -->
# Controllers

- [Introduction](#introduction)
- [Writing Controllers](#writing-controllers)
    - [Basic Controllers](#basic-controllers)
    - [Single Action Controllers](#single-action-controllers)
- [Controller Middleware](#controller-middleware)
    - [Middleware Attributes](#middleware-attributes)
    - [Authorization Attributes](#authorization-attributes)
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
라우트 파일에서 모든 요청 처리 로직을 클로저로 정의하는 대신, "컨트롤러" 클래스를 사용해 이러한 동작을 구성할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스로 묶을 수 있습니다. 예를 들어 `UserController` 클래스는 사용자 표시, 생성, 수정, 삭제를 포함하여 사용자와 관련된 모든 들어오는 요청을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

<a name="writing-controllers"></a>
<!-- ## Writing Controllers -->
## Writing Controllers

<a name="basic-controllers"></a>
<!-- ### Basic Controllers -->
### Basic Controllers

<!-- To quickly generate a new controller, you may run the `make:controller` Artisan command. By default, all of the controllers for your application are stored in the `app/Http/Controllers` directory: -->
새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행할 수 있습니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉터리에 저장됩니다.

```shell
php artisan make:controller UserController
```

<!-- Let's take a look at an example of a basic controller. A controller may have any number of public methods which will respond to incoming HTTP requests: -->
기본 컨트롤러의 예제를 살펴보겠습니다. 컨트롤러는 들어오는 HTTP 요청에 응답할 public 메서드를 원하는 만큼 가질 수 있습니다.

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
컨트롤러 클래스와 메서드를 작성한 뒤에는 다음과 같이 컨트롤러 메서드로 연결되는 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

<!-- When an incoming request matches the specified route URI, the `show` method on the `App\Http\Controllers\UserController` class will be invoked and the route parameters will be passed to the method. -->
들어오는 요청이 지정된 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고, 라우트 파라미터가 메서드에 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 기본 클래스를 확장해야 하는 것은 **아닙니다**. 하지만 모든 컨트롤러에서 공유해야 하는 메서드를 포함한 기본 컨트롤러 클래스를 확장하면 편리할 때가 있습니다.

<a name="single-action-controllers"></a>
<!-- ### Single Action Controllers -->
### Single Action Controllers

<!-- If a controller action is particularly complex, you might find it convenient to dedicate an entire controller class to that single action. To accomplish this, you may define a single `__invoke` method within the controller: -->
컨트롤러 액션이 특히 복잡하다면, 해당 단일 액션만을 위한 컨트롤러 클래스 전체를 따로 두는 것이 편리할 수 있습니다. 이를 위해 컨트롤러 안에 하나의 `__invoke` 메서드를 정의할 수 있습니다.

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
단일 액션 컨트롤러의 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요가 없습니다. 대신 컨트롤러 이름만 라우터에 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

<!-- You may generate an invokable controller by using the `--invokable` option of the `make:controller` Artisan command: -->
`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하여 invokable 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [stub publishing](/docs/13.x/artisan#stub-customization)를 사용해 커스터마이즈할 수 있습니다.

<a name="controller-middleware"></a>
<!-- ## Controller Middleware -->
## Controller Middleware

<!-- [Middleware](/docs/13.x/middleware) may be assigned to the controller's routes in your route files: -->
[Middleware](/docs/13.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

<!-- Or, you may find it convenient to specify middleware within your controller class. To do so, your controller should implement the `HasMiddleware` interface, which dictates that the controller should have a static `middleware` method. From this method, you may return an array of middleware that should be applied to the controller's actions: -->
또는 컨트롤러 클래스 안에서 Middleware를 지정하는 것이 편리할 수 있습니다. 그러려면 컨트롤러가 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 static `middleware` 메서드가 있어야 한다고 규정합니다. 이 메서드에서는 컨트롤러의 액션에 적용할 Middleware 배열을 반환할 수 있습니다.

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
컨트롤러 Middleware를 클로저로 정의할 수도 있습니다. 이렇게 하면 별도의 Middleware 클래스 전체를 작성하지 않고도 인라인 Middleware를 편리하게 정의할 수 있습니다.

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

<a name="middleware-attributes"></a>
<!-- ### Middleware Attributes -->
### Middleware Attributes

<!-- You may also assign middleware to controllers using PHP attributes: -->
PHP 속성을 사용해 컨트롤러에 Middleware를 할당할 수도 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
#[Middleware('log', only: ['index'])]
#[Middleware('subscribed', except: ['store'])]
class UserController
{
    // ...
}
```

<!-- You may place middleware attributes on individual controller methods as well. Middleware assigned to methods will be merged with middleware assigned at the class level: -->
개별 컨트롤러 메서드에도 Middleware 속성을 배치할 수 있습니다. 메서드에 할당된 Middleware는 클래스 수준에서 할당된 Middleware와 병합됩니다.

```php
<?php

namespace App\Http\Controllers;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class UserController
{
    #[Middleware('log')]
    #[Middleware('subscribed')]
    public function index()
    {
        // ...
    }

    #[Middleware(static function (Request $request, Closure $next) {
        // ...

        return $next($request);
    })]
    public function store()
    {
        // ...
    }
}
```

<!-- To exclude middleware from a controller or individual controller methods, use the `WithoutMiddleware` attribute. You may use the `only` and `except` arguments to limit a class-level attribute to particular controller methods: -->
컨트롤러 또는 개별 컨트롤러 메서드에서 미들웨어를 제외하려면 `WithoutMiddleware` 속성을 사용합니다. `only` 및 `except` 인수를 사용하면 클래스 수준 속성이 특정 컨트롤러 메서드에만 적용되도록 제한할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Http\Middleware\EnsureTokenIsValid;
use Illuminate\Routing\Attributes\Controllers\WithoutMiddleware;

#[WithoutMiddleware('subscribed', except: ['index'])]
class UserController
{
    #[WithoutMiddleware(EnsureTokenIsValid::class)]
    public function index()
    {
        // ...
    }

    public function show()
    {
        // ...
    }
}
```

<!-- Class-level `WithoutMiddleware` attributes are inherited by child controllers. The attribute can only remove route middleware and does not apply to [global middleware](/docs/13.x/middleware#global-middleware). -->
클래스 수준의 `WithoutMiddleware` 속성은 자식 컨트롤러에 상속됩니다. 이 속성은 라우트 미들웨어만 제거할 수 있으며 [global middleware](/docs/13.x/middleware#global-middleware)에는 적용되지 않습니다.

<a name="authorization-attributes"></a>
<!-- ### Authorization Attributes -->
### Authorization Attributes

<!-- If you are authorizing controller actions via policies, you may use the `Authorize` attribute as a convenient shortcut for the `can` middleware: -->
정책을 통해 컨트롤러 액션을 인가하고 있다면, `can` Middleware의 편리한 단축 표현으로 `Authorize` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;

class CommentController
{
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }

    #[Authorize('delete', 'comment')]
    public function destroy(Comment $comment)
    {
        // ...
    }
}
```

<!-- The first argument is the ability you wish to authorize. The second argument is the model class, route parameter, or parameters that should be passed to the policy. -->
첫 번째 인수는 인가하려는 ability입니다. 두 번째 인수는 정책에 전달해야 하는 모델 클래스, 라우트 파라미터 또는 파라미터들입니다.

<a name="resource-controllers"></a>
<!-- ## Resource Controllers -->
## Resource Controllers

<!-- If you think of each Eloquent model in your application as a "resource", it is typical to perform the same sets of actions against each resource in your application. For example, imagine your application contains a `Photo` model and a `Movie` model. It is likely that users can create, read, update, or delete these resources. -->
애플리케이션의 각 Eloquent 모델을 하나의 "리소스"로 생각하면, 애플리케이션의 각 리소스에 대해 동일한 동작 묶음을 수행하는 것이 일반적입니다. 예를 들어 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다고 가정해 보겠습니다. 사용자는 이러한 리소스를 생성, 조회, 수정 또는 삭제할 수 있을 가능성이 높습니다.

<!-- Because of this common use case, Laravel resource routing assigns the typical create, read, update, and delete ("CRUD") routes to a controller with a single line of code. To get started, we can use the `make:controller` Artisan command's `--resource` option to quickly create a controller to handle these actions: -->
이처럼 흔한 사용 사례 때문에 Laravel 리소스 라우팅은 일반적인 생성, 조회, 수정, 삭제("CRUD") 라우트를 단 한 줄의 코드로 컨트롤러에 할당합니다. 시작하려면 `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 이러한 액션을 처리할 컨트롤러를 빠르게 만들 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

<!-- This command will generate a controller at `app/Http/Controllers/PhotoController.php`. The controller will contain a method for each of the available resource operations. Next, you may register a resource route that points to the controller: -->
이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 컨트롤러에는 사용 가능한 각 리소스 작업에 해당하는 메서드가 포함됩니다. 다음으로, 해당 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

<!-- This single route declaration creates multiple routes to handle a variety of actions on the resource. The generated controller will already have methods stubbed for each of these actions. Remember, you can always get a quick overview of your application's routes by running the `route:list` Artisan command. -->
이 하나의 라우트 선언은 리소스에 대한 다양한 액션을 처리하기 위해 여러 라우트를 생성합니다. 생성된 컨트롤러에는 이미 각 액션에 대한 메서드 스텁이 들어 있습니다. `route:list` Artisan 명령어를 실행하면 언제든 애플리케이션 라우트를 빠르게 살펴볼 수 있다는 점을 기억하세요.

<!-- You may even register many resource controllers at once by passing an array to the `resources` method: -->
`resources` 메서드에 배열을 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<!-- The `softDeletableResources` method registers many resources controllers that all use the `withTrashed` method: -->
`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 여러 리소스 컨트롤러를 등록합니다.

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
<!-- #### Actions Handled by Resource Controllers -->
#### Actions Handled by Resource Controllers

<div class="overflow-auto">

<!-- | Verb | URI | Action | Route Name | | --------- | ---------------------- | ------- | -------------- | | GET | `/photos` | index | photos.index | | GET | `/photos/create` | create | photos.create | | POST | `/photos` | store | photos.store | | GET | `/photos/{photo}` | show | photos.show | | GET | `/photos/{photo}/edit` | edit | photos.edit | | PUT/PATCH | `/photos/{photo}` | update | photos.update | | DELETE | `/photos/{photo}` | destroy | photos.destroy | -->
| HTTP 메서드 | URI                    | 액션    | 라우트 이름    |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

</div>

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound resource model is not found. However, you may customize this behavior by calling the `missing` method when defining your resource route. The `missing` method accepts a closure that will be invoked if an implicitly bound model cannot be found for any of the resource's routes: -->
일반적으로 암묵적으로 바인딩된 리소스 모델을 찾을 수 없으면 404 HTTP 응답이 생성됩니다. 하지만 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 커스터마이즈할 수 있습니다. `missing` 메서드는 리소스의 어떤 라우트에서든 암묵적으로 바인딩된 모델을 찾을 수 없을 때 호출될 클로저를 받습니다.

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

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/13.x/eloquent#soft-deleting), and will instead return a 404 HTTP response. However, you can instruct the framework to allow soft deleted models by invoking the `withTrashed` method when defining your resource route: -->
일반적으로 암묵적 모델 바인딩은 [soft deleted](/docs/13.x/eloquent#soft-deleting)된 모델을 조회하지 않고, 대신 404 HTTP 응답을 반환합니다. 하지만 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하면 프레임워크가 소프트 삭제된 모델을 허용하도록 지시할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

<!-- Calling `withTrashed` with no arguments will allow soft deleted models for the `show`, `edit`, and `update` resource routes. You may specify a subset of these routes by passing an array to the `withTrashed` method: -->
인수 없이 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 소프트 삭제된 모델을 허용합니다. `withTrashed` 메서드에 배열을 전달하여 이러한 라우트의 하위 집합을 지정할 수 있습니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
<!-- #### Specifying the Resource Model -->
#### Specifying the Resource Model

<!-- If you are using [route model binding](/docs/13.x/routing#route-model-binding) and would like the resource controller's methods to type-hint a model instance, you may use the `--model` option when generating the controller: -->
[route model binding](/docs/13.x/routing#route-model-binding)을 사용하고 있으며 리소스 컨트롤러의 메서드가 모델 인스턴스를 타입 힌트하도록 하고 싶다면, 컨트롤러를 생성할 때 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
<!-- #### Generating Form Requests -->
#### Generating Form Requests

<!-- You may provide the `--requests` option when generating a resource controller to instruct Artisan to generate [form request classes](/docs/13.x/validation#form-request-validation) for the controller's storage and update methods: -->
리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면 Artisan이 컨트롤러의 저장 및 수정 메서드를 위한 [form request classes](/docs/13.x/validation#form-request-validation)를 생성하도록 지시할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
<!-- ### Partial Resource Routes -->
### Partial Resource Routes

<!-- When declaring a resource route, you may specify a subset of actions the controller should handle instead of the full set of default actions: -->
리소스 라우트를 선언할 때, 전체 기본 액션 묶음 대신 컨트롤러가 처리해야 하는 액션의 일부만 지정할 수 있습니다.

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
API에서 사용할 리소스 라우트를 선언할 때는 일반적으로 `create`와 `edit`처럼 HTML 템플릿을 표시하는 라우트를 제외하고 싶을 것입니다. 편의를 위해 `apiResource` 메서드를 사용하면 이 두 라우트를 자동으로 제외할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

<!-- You may register many API resource controllers at once by passing an array to the `apiResources` method: -->
`apiResources` 메서드에 배열을 전달하여 여러 API 리소스 컨트롤러를 한 번에 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```
<!-- To quickly generate an API resource controller that does not include the `create` or `edit` methods, use the `--api` switch when executing the `make:controller` command: -->
`create` 또는 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령어를 실행할 때 `--api` 스위치를 사용합니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
<!-- ### Nested Resources -->
### Nested Resources

<!-- Sometimes you may need to define routes to a nested resource. For example, a photo resource may have multiple comments that may be attached to the photo. To nest the resource controllers, you may use "dot" notation in your route declaration: -->
때로는 중첩 리소스에 대한 라우트를 정의해야 할 수 있습니다. 예를 들어 사진 리소스에는 해당 사진에 연결되는 여러 댓글이 있을 수 있습니다. 리소스 컨트롤러를 중첩하려면 라우트 선언에서 "dot" 표기법을 사용할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

<!-- This route will register a nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같은 URI로 접근할 수 있는 중첩 리소스를 등록합니다.

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
<!-- #### Scoping Nested Resources -->
#### Scoping Nested Resources

<!-- Laravel's [implicit model binding](/docs/13.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by. For more information on how to accomplish this, please see the documentation on [scoping resource routes](#restful-scoping-resource-routes). -->
Laravel의 [implicit model binding](/docs/13.x/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩의 범위를 자동으로 지정하여, 해석된 자식 모델이 부모 모델에 속하는지 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회해야 하는지도 Laravel에 알려줄 수 있습니다. 이를 수행하는 방법에 대한 자세한 내용은 [scoping resource routes](#restful-scoping-resource-routes) 문서를 참고하십시오.

<a name="shallow-nesting"></a>
<!-- #### Shallow Nesting -->
#### Shallow Nesting

<!-- Often, it is not entirely necessary to have both the parent and the child IDs within a URI since the child ID is already a unique identifier. When using unique identifiers such as auto-incrementing primary keys to identify your models in URI segments, you may choose to use "shallow nesting": -->
자식 ID 자체가 이미 고유한 식별자인 경우가 많기 때문에, URI 안에 부모 ID와 자식 ID를 모두 포함할 필요가 항상 있는 것은 아닙니다. URI 세그먼트에서 모델을 식별하기 위해 자동 증가 기본 키와 같은 고유 식별자를 사용하는 경우 "얕은 중첩"을 사용할 수 있습니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

<!-- This route definition will define the following routes: -->
이 라우트 정의는 다음 라우트를 정의합니다.

<div class="overflow-auto">

<!-- | Verb | URI | Action | Route Name | | --------- | --------------------------------- | ------- | ---------------------- | | GET | `/photos/{photo}/comments` | index | photos.comments.index | | GET | `/photos/{photo}/comments/create` | create | photos.comments.create | | POST | `/photos/{photo}/comments` | store | photos.comments.store | | GET | `/comments/{comment}` | show | comments.show | | GET | `/comments/{comment}/edit` | edit | comments.edit | | PUT/PATCH | `/comments/{comment}` | update | comments.update | | DELETE | `/comments/{comment}` | destroy | comments.destroy | -->
| 동사      | URI                               | 동작    | 라우트 이름            |
| --------- | --------------------------------- | ------- | ---------------------- |
| GET       | `/photos/{photo}/comments`        | index   | photos.comments.index  |
| GET       | `/photos/{photo}/comments/create` | create  | photos.comments.create |
| POST      | `/photos/{photo}/comments`        | store   | photos.comments.store  |
| GET       | `/comments/{comment}`             | show    | comments.show          |
| GET       | `/comments/{comment}/edit`        | edit    | comments.edit          |
| PUT/PATCH | `/comments/{comment}`             | update  | comments.update        |
| DELETE    | `/comments/{comment}`             | destroy | comments.destroy       |

</div>

<a name="restful-naming-resource-routes"></a>
<!-- ### Naming Resource Routes -->
### Naming Resource Routes

<!-- By default, all resource controller actions have a route name; however, you can override these names by passing a `names` array with your desired route names: -->
기본적으로 모든 리소스 컨트롤러 동작에는 라우트 이름이 있습니다. 하지만 원하는 라우트 이름을 담은 `names` 배열을 전달하여 이 이름을 재정의할 수 있습니다.

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
기본적으로 `Route::resource`는 리소스 이름의 "단수형" 버전을 기반으로 리소스 라우트의 라우트 파라미터를 생성합니다. `parameters` 메서드를 사용하면 리소스별로 이를 쉽게 재정의할 수 있습니다. `parameters` 메서드에 전달하는 배열은 리소스 이름과 파라미터 이름의 연관 배열이어야 합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

<!-- The example above generates the following URI for the resource's `show` route: -->
위 예제는 리소스의 `show` 라우트에 대해 다음 URI를 생성합니다.

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
<!-- ### Scoping Resource Routes -->
### Scoping Resource Routes

<!-- Laravel's [scoped implicit model binding](/docs/13.x/routing#implicit-model-binding-scoping) feature can automatically scope nested bindings such that the resolved child model is confirmed to belong to the parent model. By using the `scoped` method when defining your nested resource, you may enable automatic scoping as well as instruct Laravel which field the child resource should be retrieved by: -->
Laravel의 [scoped implicit model binding](/docs/13.x/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩의 범위를 자동으로 지정하여, 해석된 자식 모델이 부모 모델에 속하는지 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화할 수 있으며, 자식 리소스를 어떤 필드로 조회해야 하는지도 Laravel에 알려줄 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

<!-- This route will register a scoped nested resource that may be accessed with URIs like the following: -->
이 라우트는 다음과 같은 URI로 접근할 수 있는 범위 지정된 중첩 리소스를 등록합니다.

```text
/photos/{photo}/comments/{comment:slug}
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `Photo` model has a relationship named `comments` (the plural of the route parameter name) which can be used to retrieve the `Comment` model. -->
사용자 정의 키를 사용하는 암묵적 바인딩을 중첩 라우트 파라미터로 사용할 때, Laravel은 규칙에 따라 부모 모델의 연관관계 이름을 추측하여 부모를 기준으로 중첩 모델을 조회하도록 쿼리 범위를 자동으로 지정합니다. 이 경우 `Photo` 모델에 `comments`라는 이름의 연관관계(라우트 파라미터 이름의 복수형)가 있으며, 이를 사용해 `Comment` 모델을 조회할 수 있다고 가정합니다.

<a name="restful-localizing-resource-uris"></a>
<!-- ### Localizing Resource URIs -->
### Localizing Resource URIs

<!-- By default, `Route::resource` will create resource URIs using English verbs and plural rules. If you need to localize the `create` and `edit` action verbs, you may use the `Route::resourceVerbs` method. This may be done at the beginning of the `boot` method within your application's `App\Providers\AppServiceProvider`: -->
기본적으로 `Route::resource`는 영어 동사와 복수형 규칙을 사용하여 리소스 URI를 생성합니다. `create`와 `edit` 동작 동사를 현지화해야 하는 경우 `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\AppServiceProvider` 안에 있는 `boot` 메서드 시작 부분에서 수행할 수 있습니다.

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

<!-- Laravel's pluralizer supports [several different languages which you may configure based on your needs](/docs/13.x/localization#pluralization-language). Once the verbs and pluralization language have been customized, a resource route registration such as `Route::resource('publicacion', PublicacionController::class)` will produce the following URIs: -->
Laravel의 복수형 변환기는 [several different languages which you may configure based on your needs](/docs/13.x/localization#pluralization-language)를 지원합니다. 동사와 복수형 언어를 사용자 지정한 후에는 `Route::resource('publicacion', PublicacionController::class)`와 같은 리소스 라우트 등록이 다음 URI를 생성합니다.

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
<!-- ### Supplementing Resource Controllers -->
### Supplementing Resource Controllers

<!-- If you need to add additional routes to a resource controller beyond the default set of resource routes, you should define those routes before your call to the `Route::resource` method; otherwise, the routes defined by the `resource` method may unintentionally take precedence over your supplemental routes: -->
기본 리소스 라우트 집합 외에 리소스 컨트롤러에 추가 라우트를 더해야 하는 경우, `Route::resource` 메서드를 호출하기 전에 해당 라우트를 정의해야 합니다. 그렇지 않으면 `resource` 메서드가 정의한 라우트가 보완 라우트보다 의도치 않게 우선될 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러의 책임을 집중된 상태로 유지해야 한다는 점을 기억하십시오. 일반적인 리소스 동작 집합에 속하지 않는 메서드가 반복적으로 필요하다면, 컨트롤러를 더 작은 두 개의 컨트롤러로 나누는 것을 고려하십시오.

<a name="singleton-resource-controllers"></a>
<!-- ### Singleton Resource Controllers -->
### Singleton Resource Controllers

<!-- Sometimes, your application will have resources that may only have a single instance. For example, a user's "profile" can be edited or updated, but a user may not have more than one "profile". Likewise, an image may have a single "thumbnail". These resources are called "singleton resources", meaning one and only one instance of the resource may exist. In these scenarios, you may register a "singleton" resource controller: -->
때로는 애플리케이션에 단 하나의 인스턴스만 가질 수 있는 리소스가 있을 수 있습니다. 예를 들어 사용자의 "profile"은 편집하거나 업데이트할 수 있지만, 사용자가 하나 이상의 "profile"을 가질 수는 없습니다. 마찬가지로 이미지는 하나의 "thumbnail"만 가질 수 있습니다. 이러한 리소스를 "싱글턴 리소스"라고 하며, 이는 해당 리소스의 인스턴스가 오직 하나만 존재할 수 있음을 의미합니다. 이런 상황에서는 "singleton" 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

<!-- The singleton resource definition above will register the following routes. As you can see, "creation" routes are not registered for singleton resources, and the registered routes do not accept an identifier since only one instance of the resource may exist: -->
위의 싱글턴 리소스 정의는 다음 라우트를 등록합니다. 보시다시피 싱글턴 리소스에는 "생성" 라우트가 등록되지 않으며, 리소스 인스턴스가 하나만 존재할 수 있으므로 등록된 라우트는 식별자를 받지 않습니다.

<div class="overflow-auto">

<!-- | Verb | URI | Action | Route Name | | --------- | --------------- | ------ | -------------- | | GET | `/profile` | show | profile.show | | GET | `/profile/edit` | edit | profile.edit | | PUT/PATCH | `/profile` | update | profile.update | -->
| 동사      | URI             | 동작   | 라우트 이름    |
| --------- | --------------- | ------ | -------------- |
| GET       | `/profile`      | show   | profile.show   |
| GET       | `/profile/edit` | edit   | profile.edit   |
| PUT/PATCH | `/profile`      | update | profile.update |

</div>

<!-- Singleton resources may also be nested within a standard resource: -->
싱글턴 리소스는 표준 리소스 안에 중첩될 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

<!-- In this example, the `photos` resource would receive all of the [standard resource routes](#actions-handled-by-resource-controllers); however, the `thumbnail` resource would be a singleton resource with the following routes: -->
이 예제에서 `photos` 리소스는 모든 [standard resource routes](#actions-handled-by-resource-controllers)를 받습니다. 하지만 `thumbnail` 리소스는 다음 라우트를 가진 싱글턴 리소스가 됩니다.

<div class="overflow-auto">

<!-- | Verb | URI | Action | Route Name | | --------- | -------------------------------- | ------ | ----------------------- | | GET | `/photos/{photo}/thumbnail` | show | photos.thumbnail.show | | GET | `/photos/{photo}/thumbnail/edit` | edit | photos.thumbnail.edit | | PUT/PATCH | `/photos/{photo}/thumbnail` | update | photos.thumbnail.update | -->
| 동사      | URI                              | 동작   | 라우트 이름             |
| --------- | -------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
<!-- #### Creatable Singleton Resources -->
#### Creatable Singleton Resources

<!-- Occasionally, you may want to define creation and storage routes for a singleton resource. To accomplish this, you may invoke the `creatable` method when registering the singleton resource route: -->
가끔 싱글턴 리소스에 대해 생성 및 저장 라우트를 정의하고 싶을 수 있습니다. 이를 위해 싱글턴 리소스 라우트를 등록할 때 `creatable` 메서드를 호출할 수 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

<!-- In this example, the following routes will be registered. As you can see, a `DELETE` route will also be registered for creatable singleton resources: -->
이 예제에서는 다음 라우트가 등록됩니다. 보시다시피 생성 가능한 싱글턴 리소스에는 `DELETE` 라우트도 함께 등록됩니다.

<div class="overflow-auto">

<!-- | Verb | URI | Action | Route Name | | --------- | ---------------------------------- | ------- | ------------------------ | | GET | `/photos/{photo}/thumbnail/create` | create | photos.thumbnail.create | | POST | `/photos/{photo}/thumbnail` | store | photos.thumbnail.store | | GET | `/photos/{photo}/thumbnail` | show | photos.thumbnail.show | | GET | `/photos/{photo}/thumbnail/edit` | edit | photos.thumbnail.edit | | PUT/PATCH | `/photos/{photo}/thumbnail` | update | photos.thumbnail.update | | DELETE | `/photos/{photo}/thumbnail` | destroy | photos.thumbnail.destroy | -->
| 동사      | URI                                | 동작    | 라우트 이름              |
| --------- | ---------------------------------- | ------- | ------------------------ |
| GET       | `/photos/{photo}/thumbnail/create` | create  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | store   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | show    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | edit    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | update  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | destroy | photos.thumbnail.destroy |

</div>

<!-- If you would like Laravel to register the `DELETE` route for a singleton resource but not register the creation or storage routes, you may utilize the `destroyable` method: -->
싱글턴 리소스에 대해 `DELETE` 라우트는 등록하되 생성 또는 저장 라우트는 등록하지 않으려면 `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
<!-- #### API Singleton Resources -->
#### API Singleton Resources

<!-- The `apiSingleton` method may be used to register a singleton resource that will be manipulated via an API, thus rendering the `create` and `edit` routes unnecessary: -->
API를 통해 조작될 싱글턴 리소스를 등록할 때는 `apiSingleton` 메서드를 사용할 수 있습니다. 이 경우 `create`와 `edit` 라우트는 필요하지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

<!-- Of course, API singleton resources may also be `creatable`, which will register `store` and `destroy` routes for the resource: -->
물론 API 싱글턴 리소스도 `creatable`이 될 수 있으며, 이 경우 해당 리소스에 대해 `store`와 `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```
<a name="middleware-and-resource-controllers"></a>
<!-- ### Middleware and Resource Controllers -->
### Middleware and Resource Controllers

<!-- Laravel allows you to assign middleware to all, or only specific, methods of resource routes using the `middleware`, `middlewareFor`, and `withoutMiddlewareFor` methods. These methods provide fine-grained control over which middleware is applied to each resource action. -->
Laravel은 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 사용하여 리소스 라우트의 모든 메서드 또는 특정 메서드에만 Middleware를 지정할 수 있도록 합니다. 이 메서드들은 각 리소스 동작에 어떤 Middleware가 적용되는지 세밀하게 제어할 수 있게 해줍니다.

<!-- #### Applying Middleware to all Methods -->
#### Applying Middleware to all Methods

<!-- You may use the `middleware` method to assign middleware to all routes generated by a resource or singleton resource route: -->
`middleware` 메서드를 사용하여 리소스 또는 싱글턴 리소스 라우트가 생성하는 모든 라우트에 Middleware를 지정할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

<!-- #### Applying Middleware to Specific Methods -->
#### Applying Middleware to Specific Methods

<!-- You may use the `middlewareFor` method to assign middleware to one or more specific methods of a given resource controller: -->
`middlewareFor` 메서드를 사용하여 주어진 리소스 컨트롤러의 하나 이상의 특정 메서드에 Middleware를 지정할 수 있습니다.

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
`middlewareFor` 메서드는 싱글턴 및 API 싱글턴 리소스 컨트롤러와 함께 사용할 수도 있습니다.

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

<!-- #### Excluding Middleware from Specific Methods -->
#### Excluding Middleware from Specific Methods

<!-- You may use the `withoutMiddlewareFor` method to exclude middleware from specific methods of a resource controller: -->
`withoutMiddlewareFor` 메서드를 사용하여 리소스 컨트롤러의 특정 메서드에서 Middleware를 제외할 수 있습니다.

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

<!-- The Laravel [service container](/docs/13.x/container) is used to resolve all Laravel controllers. As a result, you are able to type-hint any dependencies your controller may need in its constructor. The declared dependencies will automatically be resolved and injected into the controller instance: -->
Laravel [service container](/docs/13.x/container)는 모든 Laravel 컨트롤러를 해석하는 데 사용됩니다. 따라서 컨트롤러 생성자에서 컨트롤러가 필요로 하는 모든 의존성을 타입 힌트로 선언할 수 있습니다. 선언된 의존성은 자동으로 해석되어 컨트롤러 인스턴스에 주입됩니다.

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
생성자 주입 외에도 컨트롤러의 메서드에 의존성을 타입 힌트로 선언할 수 있습니다. 메서드 주입의 일반적인 사용 사례는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메서드에 주입하는 것입니다.

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
컨트롤러 메서드가 라우트 파라미터의 입력도 기대하는 경우, 다른 의존성 뒤에 라우트 인수를 나열하십시오. 예를 들어 라우트가 다음과 같이 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` parameter by defining your controller method as follows: -->
여전히 `Illuminate\Http\Request`를 타입 힌트로 선언하면서, 컨트롤러 메서드를 다음과 같이 정의하여 `id` 파라미터에 접근할 수 있습니다.

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
