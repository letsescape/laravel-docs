# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
    - [미들웨어 속성](#middleware-attributes)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 이름 지정](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 이름 지정](#restful-naming-resource-route-parameters)
    - [리소스 라우트 스코핑](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 확장](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어와 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일에서 모든 요청 처리 로직을 클로저(closure)로 정의하는 대신, 이러한 동작을 "컨트롤러(controller)" 클래스를 사용하여 구성할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스에 그룹화할 수 있도록 합니다. 예를 들어 `UserController` 클래스는 사용자와 관련된 모든 요청(사용자 조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러

새로운 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 실행하면 됩니다. 기본적으로 애플리케이션의 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

```shell
php artisan make:controller UserController
```

다음은 기본적인 컨트롤러 예시입니다. 컨트롤러에는 들어오는 HTTP 요청을 처리할 수 있는 여러 개의 public 메서드를 정의할 수 있습니다.

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

컨트롤러 클래스와 메서드를 작성한 후에는 다음과 같이 해당 메서드를 호출하는 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정된 라우트 URI와 일치하면 `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]  
> 컨트롤러가 반드시 기본 클래스를 상속해야 하는 것은 아닙니다. 하지만 모든 컨트롤러에서 공통으로 사용되는 메서드를 포함한 기본 컨트롤러 클래스를 만들어 상속하는 것이 편리한 경우가 많습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러 액션이 특히 복잡한 경우, 하나의 액션을 위해 별도의 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 위해 컨트롤러에 단일 `__invoke` 메서드를 정의할 수 있습니다.

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

단일 액션 컨트롤러의 라우트를 등록할 때는 메서드를 지정할 필요가 없습니다. 대신 컨트롤러 클래스 이름만 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하면 invokable 컨트롤러를 생성할 수 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]  
> 컨트롤러 스텁(controller stub)은 [stub publishing](/docs/master/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[Middleware](/docs/master/middleware)는 라우트 파일에서 컨트롤러의 라우트에 다음과 같이 할당할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

또는 컨트롤러 클래스 내부에서 미들웨어를 지정할 수도 있습니다. 이를 위해 컨트롤러는 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러에 정적 `middleware` 메서드를 정의하도록 요구합니다. 이 메서드에서 컨트롤러의 액션에 적용할 미들웨어 배열을 반환할 수 있습니다.

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

또한 컨트롤러 미들웨어를 클로저로 정의할 수도 있습니다. 이렇게 하면 별도의 미들웨어 클래스를 만들지 않고도 인라인 미들웨어를 간편하게 정의할 수 있습니다.

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
### 미들웨어 속성 (Middleware Attributes)

PHP 속성(attribute)을 사용하여 컨트롤러에 미들웨어를 할당할 수도 있습니다.

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

미들웨어 속성은 개별 컨트롤러 메서드에도 적용할 수 있습니다. 메서드에 할당된 미들웨어는 클래스 레벨에서 지정된 미들웨어와 병합됩니다.

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

<a name="resource-controllers"></a>
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션에서 각 Eloquent 모델을 하나의 "리소스(resource)"로 생각하면, 일반적으로 모든 리소스에 대해 동일한 작업을 수행하게 됩니다. 예를 들어 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다고 가정해 보겠습니다. 사용자는 이 리소스를 생성(Create), 조회(Read), 수정(Update), 삭제(Delete)할 수 있을 가능성이 높습니다.

이러한 일반적인 사용 사례를 위해 Laravel의 리소스 라우팅(resource routing)은 단 한 줄의 코드로 컨트롤러에 CRUD(Create, Read, Update, Delete) 라우트를 자동으로 할당합니다. 먼저 `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 이러한 작업을 처리할 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령어는 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 생성된 컨트롤러에는 각 리소스 작업에 대한 메서드가 미리 작성된 형태로 포함됩니다. 다음으로 해당 컨트롤러를 가리키는 리소스 라우트를 등록합니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언은 리소스에 대한 다양한 동작을 처리하는 여러 개의 라우트를 생성합니다. 생성된 컨트롤러에는 이미 각 액션에 대한 메서드 스텁이 포함되어 있습니다. 또한 `route:list` Artisan 명령어를 실행하면 애플리케이션의 모든 라우트를 빠르게 확인할 수 있습니다.

여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`softDeletableResources` 메서드는 모든 리소스 컨트롤러에 대해 `withTrashed` 메서드를 사용하는 리소스 컨트롤러를 등록합니다.

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

| Verb      | URI                    | Action  | Route Name     |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 처리 동작 사용자 정의

일반적으로 암묵적 모델 바인딩된 리소스 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 리소스 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 사용자 정의할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델을 찾지 못했을 때 실행될 클로저를 받습니다.

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
#### Soft Deleted 모델

일반적으로 암묵적 모델 바인딩은 [soft deleted](/docs/master/eloquent#soft-deleting)된 모델을 조회하지 않으며, 대신 404 HTTP 응답을 반환합니다. 하지만 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하면 soft deleted 모델도 허용하도록 설정할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인수를 전달하지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 리소스 라우트에서 soft deleted 모델을 허용합니다. 특정 라우트에만 적용하려면 배열을 전달하면 됩니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[route model binding](/docs/master/routing#route-model-binding)을 사용하면서 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입 힌트로 받고 싶다면, 컨트롤러 생성 시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### Form Request 생성

리소스 컨트롤러 생성 시 `--requests` 옵션을 제공하면 Artisan이 컨트롤러의 저장(store) 및 수정(update) 메서드에 사용할 [form request classes](/docs/master/validation#form-request-validation)를 자동으로 생성합니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```