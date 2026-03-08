# 컨트롤러 (Controllers)

- [소개](#introduction)
- [컨트롤러 작성](#writing-controllers)
    - [기본 컨트롤러](#basic-controllers)
    - [단일 액션 컨트롤러](#single-action-controllers)
- [컨트롤러 미들웨어](#controller-middleware)
- [리소스 컨트롤러](#resource-controllers)
    - [부분 리소스 라우트](#restful-partial-resource-routes)
    - [중첩 리소스](#restful-nested-resources)
    - [리소스 라우트 명명](#restful-naming-resource-routes)
    - [리소스 라우트 파라미터 명명](#restful-naming-resource-route-parameters)
    - [리소스 라우트 범위 지정](#restful-scoping-resource-routes)
    - [리소스 URI 현지화](#restful-localizing-resource-uris)
    - [리소스 컨트롤러 보완](#restful-supplementing-resource-controllers)
    - [싱글턴 리소스 컨트롤러](#singleton-resource-controllers)
    - [미들웨어 및 리소스 컨트롤러](#middleware-and-resource-controllers)
- [의존성 주입과 컨트롤러](#dependency-injection-and-controllers)

<a name="introduction"></a>
## 소개 (Introduction)

라우트 파일에 모든 요청 처리 로직을 클로저(Closure)로 정의하는 대신, `"컨트롤러(controller)"` 클래스를 사용해 이 동작을 구조화할 수 있습니다. 컨트롤러는 관련된 요청 처리 로직을 하나의 클래스에 모을 수 있습니다. 예를 들어, `UserController` 클래스는 사용자와 관련된 모든 요청(조회, 생성, 수정, 삭제 등)을 처리할 수 있습니다. 기본적으로 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

<a name="writing-controllers"></a>
## 컨트롤러 작성 (Writing Controllers)

<a name="basic-controllers"></a>
### 기본 컨트롤러 (Basic Controllers)

새 컨트롤러를 빠르게 생성하려면 `make:controller` Artisan 명령어를 사용할 수 있습니다. 기본적으로 모든 컨트롤러는 `app/Http/Controllers` 디렉토리에 저장됩니다.

```shell
php artisan make:controller UserController
```

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

컨트롤러 클래스와 메서드를 작성한 후에는 다음과 같이 해당 컨트롤러 메서드로 라우트를 정의할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```

들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되며, 라우트 파라미터가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러가 반드시 베이스 클래스를 상속할 필요는 **없습니다**. 하지만, 모든 컨트롤러에서 공통으로 사용할 메서드를 포함하는 베이스 컨트롤러 클래스를 상속하는 것이 편리할 때도 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러 (Single Action Controllers)

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

단일 액션 컨트롤러를 라우트에 등록할 때는, 메서드명을 지정할 필요 없이 컨트롤러 이름만 전달하면 됩니다.

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```

`--invokable` 옵션을 사용하여 단일 액션 컨트롤러를 Artisan으로 생성할 수도 있습니다.

```shell
php artisan make:controller ProvisionServer --invokable
```

> [!NOTE]
> 컨트롤러 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어 (Controller Middleware)

[미들웨어](/docs/12.x/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다.

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```

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
## 리소스 컨트롤러 (Resource Controllers)

애플리케이션 내의 각 Eloquent 모델을 "리소스(resource)"로 본다면, 보통 해당 리소스에 대해 동일한 패턴의 동작을 적용하게 됩니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다면, 사용자들은 이 리소스들을 생성, 조회, 수정, 삭제할 수 있을 것입니다.

이처럼 흔하게 사용되는 패턴을 위해, Laravel의 리소스 라우팅은 일반적인 생성(Create), 조회(Read), 수정(Update), 삭제(Delete) 즉, "CRUD" 라우트를 한 줄의 코드로 컨트롤러에 할당해줍니다. 먼저, `make:controller` Artisan 명령어의 `--resource` 옵션을 사용하여 이러한 동작을 처리할 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --resource
```

이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성하며, 각 리소스 동작에 맞는 메서드를 포함하고 있습니다. 그 다음, 해당 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```

이 한 줄의 라우트 선언은 리소스에 다양한 동작을 처리하는 여러 라우트를 자동으로 생성합니다. 생성된 컨트롤러에는 이미 이러한 동작을 위한 스텁 메서드들이 정의되어 있습니다. 참고로, `route:list` Artisan 명령어를 실행하면 애플리케이션의 모든 라우트를 빠르게 확인할 수 있습니다.

여러 리소스 컨트롤러를 동시에 등록하려면 배열을 `resources` 메서드에 전달하면 됩니다.

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 여러 리소스 컨트롤러를 한 번에 등록합니다.

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

<a name="actions-handled-by-resource-controllers"></a>
#### 리소스 컨트롤러가 처리하는 액션

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

</div>

<a name="customizing-missing-model-behavior"></a>
#### 모델 미존재 시 동작 커스터마이징

보통, 암묵적으로 바인딩된 리소스 모델을 찾을 수 없을 때는 404 HTTP 응답이 반환됩니다. 그러나, 리소스 라우트 정의 시 `missing` 메서드를 호출하여 이 동작을 커스터마이징할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델이 각 리소스의 라우트에서 발견되지 않았을 때 실행할 클로저를 받습니다.

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
#### 소프트 삭제된(soft deleted) 모델

일반적으로, 암묵적 모델 바인딩은 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)된 모델을 조회하지 않으며, 대신 404 HTTP 응답을 반환합니다. 하지만, `withTrashed` 메서드를 라우트에 적용하면 소프트 삭제된 모델도 조회하도록 할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```

인자를 주지 않고 `withTrashed`를 호출하면 `show`, `edit`, `update` 라우트에 대해 소프트 삭제된 모델을 허용합니다. 배열을 전달하여 이 라우트들 중 일부만 지정할 수도 있습니다.

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```

<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정

[라우트 모델 바인딩](/docs/12.x/routing#route-model-binding)을 사용하고, 리소스 컨트롤러의 메서드에서 모델 인스턴스를 타입힌트하고 싶다면, 컨트롤러 생성시 `--model` 옵션을 사용할 수 있습니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource
```

<a name="generating-form-requests"></a>
#### 폼 요청 클래스(Form Request) 생성

리소스 컨트롤러 생성 시 `--requests` 옵션을 추가하면, Artisan이 컨트롤러의 저장 및 갱신 메서드를 위한 [폼 요청 클래스](/docs/12.x/validation#form-request-validation)도 함께 생성합니다.

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```

<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트 (Partial Resource Routes)

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
#### API 리소스 라우트

API에서 사용될 리소스 라우트를 선언할 경우, 보통은 HTML 템플릿을 보여주는 `create`, `edit` 라우트가 필요하지 않습니다. 편의를 위해, `apiResource` 메서드를 사용하면 이 두 라우트가 자동으로 제외됩니다.

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```

배열을 전달하여 여러 API 리소스 컨트롤러를 한 번에 등록할 수도 있습니다.

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```

`make:controller` 명령어 실행 시 `--api` 옵션을 사용하면, `create`와 `edit` 메서드가 포함되지 않는 API 리소스 컨트롤러를 빠르게 생성할 수 있습니다.

```shell
php artisan make:controller PhotoController --api
```

<a name="restful-nested-resources"></a>
### 중첩 리소스 (Nested Resources)

때때로 한 리소스에 중첩된 하위 리소스가 필요할 수 있습니다. 예를 들어, 하나의 사진에는 여러 개의 댓글이 달릴 수 있습니다. 이러한 중첩 리소스를 위해 라우트 선언 시 "점(dot) 표기법"을 사용합니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```

이 라우트는 다음과 같은 URI로 중첩 리소스를 사용할 수 있게 해줍니다.

```text
/photos/{photo}/comments/{comment}
```

<a name="scoping-nested-resources"></a>
#### 중첩 리소스의 범위 지정(Scoping)

Laravel의 [암묵적 모델 바인딩(implicit model binding)](/docs/12.x/routing#implicit-model-binding-scoping) 기능을 활용하면, 중첩된 리소스가 부모 모델에 속하는지 자동으로 확인하고 바인딩할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화하고, 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다. 자세한 내용은 [리소스 라우트 범위 지정](#restful-scoping-resource-routes) 문서를 참고하세요.

<a name="shallow-nesting"></a>
#### Shallow(얕은) 중첩

종종, 자식 ID가 이미 고유 식별자인 경우에는 URI에 부모와 자식 ID를 모두 포함할 필요가 없습니다. 예를 들어, 자동 증가하는 기본 키 등의 고유 식별자를 URI 세그먼트로 사용하는 경우, "shallow nesting(얕은 중첩)"을 사용할 수 있습니다.

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```

이 라우트 정의는 아래와 같은 라우트를 생성합니다.

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

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 명명 (Naming Resource Routes)

기본적으로, 모든 리소스 컨트롤러의 액션에는 라우트 이름이 자동으로 부여됩니다. 그러나, `names` 배열을 전달하여 원하는 라우트 이름으로 오버라이드할 수 있습니다.

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```

<a name="restful-naming-resource-route-parameters"></a>
### 리소스 라우트 파라미터 명명 (Naming Resource Route Parameters)

`Route::resource`는 리소스 이름의 "단수형"을 사용해 기본적으로 라우트 파라미터를 생성합니다. 이 동작은 `parameters` 메서드를 통해 리소스별로 변경할 수 있습니다. `parameters`에는 리소스 이름과 파라미터 이름을 매핑한 연관 배열을 전달합니다.

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```

위 예시에서 생성되는 라우트의 `show` URI는 다음과 같습니다.

```text
/users/{admin_user}
```

<a name="restful-scoping-resource-routes"></a>
### 리소스 라우트 범위 지정 (Scoping Resource Routes)

Laravel의 [스코프드(범위 지정된) 암묵적 모델 바인딩](/docs/12.x/routing#implicit-model-binding-scoping) 기능을 활용하면, 중첩된 모델의 부모-자식 소속이 자동으로 검증됩니다. `scoped` 메서드로 자식 리소스를 어떤 필드로 조회할지 지정할 수 있습니다.

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```

이 라우트는 다음과 같은 URI로 중첩된 리소스를 스코프하여 활용할 수 있습니다.

```text
/photos/{photo}/comments/{comment:slug}
```

사용자 정의 키(예: slug)로 암묵 바인딩할 때, Laravel은 부모 모델의 연관관계 이름(예시에서는 `comments`)을 자동으로 추정해 쿼리 범위를 지정합니다. 즉, 위 예시에서는 `Photo` 모델에 `comments`라는 연관관계가 있어야 하며, 이를 통해 `Comment` 모델을 자동으로 조회합니다.

<a name="restful-localizing-resource-uris"></a>
### 리소스 URI 현지화 (Localizing Resource URIs)

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

Laravel의 복수화(pluralizer) 기능은 [여러 언어를 지원](https://laravel.com/docs/12.x/localization#pluralization-language)하며, 필요에 따라 설정할 수 있습니다. 동사와 복수화 언어를 커스터마이즈하면, 예를 들어 `Route::resource('publicacion', PublicacionController::class)`은 아래와 같은 URI를 생성합니다.

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```

<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보완 (Supplementing Resource Controllers)

리소스 컨트롤러에 기본 리소스 라우트 외에 추가적인 라우트를 더해야 하는 경우, 반드시 `Route::resource` 호출 **이전**에 직접 라우트를 정의해야 합니다. 그렇지 않으면 `resource`에서 생성된 라우트가 추가 라우트보다 우선 처리되어 의도와 다르게 동작할 수 있습니다.

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```

> [!NOTE]
> 컨트롤러의 책임을 명확하게 유지하세요. 일반적인 리소스 액션 외에 별도의 메서드가 자주 필요하다면, 컨트롤러를 두 개의 더 작은 컨트롤러로 분리하는 것이 더 좋을 수 있습니다.

<a name="singleton-resource-controllers"></a>
### 싱글턴 리소스 컨트롤러 (Singleton Resource Controllers)

애플리케이션 내에는 단일 인스턴스만 존재할 수 있는 리소스가 있을 수 있습니다. 예를 들어, 사용자 "프로필"은 수정할 수 있지만 하나만 존재하며, 이미지의 "썸네일"도 한 개만 존재해야 할 수 있습니다. 이런 리소스는 "싱글턴 리소스(singleton resource)"라고 하며, 오직 하나의 인스턴스만 허용합니다. 이 경우, `"singleton"` 리소스 컨트롤러를 등록할 수 있습니다.

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```

위의 싱글턴 리소스 정의는 아래와 같은 라우트를 등록합니다. "생성"용 라우트는 등록되지 않으며, 단일 인스턴스만 존재하므로 파라미터 없이 라우트가 정의됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI               | 액션   | 라우트 이름        |
| ----------- | ----------------- | ------ | ------------------ |
| GET         | `/profile`        | show   | profile.show       |
| GET         | `/profile/edit`   | edit   | profile.edit       |
| PUT/PATCH   | `/profile`        | update | profile.update     |

</div>

싱글턴 리소스는 표준 리소스에 중첩시킬 수도 있습니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```

이 경우, `photos` 리소스는 [표준 리소스 라우트](#actions-handled-by-resource-controllers)를 모두 가지게 되며, `thumbnail` 리소스는 아래와 같은 싱글턴 리소스 라우트를 갖게 됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                              | 액션   | 라우트 이름                  |
| ----------- | -------------------------------- | ------ | ---------------------------- |
| GET         | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show        |
| GET         | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit        |
| PUT/PATCH   | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update      |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글턴 리소스 (Creatable Singleton Resources)

경우에 따라, 싱글턴 리소스에 대한 생성(create) 및 저장(store) 라우트가 필요할 수 있습니다. 이럴 때는 싱글턴 리소스 라우트 등록 시 `creatable` 메서드를 호출합니다.

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```

이 경우 아래의 라우트들이 등록됩니다. 또한 `DELETE` 라우트도 생성됩니다.

<div class="overflow-auto">

| HTTP 메서드 | URI                                    | 액션    | 라우트 이름                    |
| ----------- | -------------------------------------- | ------- | ------------------------------ |
| GET         | `/photos/{photo}/thumbnail/create`     | create  | photos.thumbnail.create        |
| POST        | `/photos/{photo}/thumbnail`            | store   | photos.thumbnail.store         |
| GET         | `/photos/{photo}/thumbnail`            | show    | photos.thumbnail.show          |
| GET         | `/photos/{photo}/thumbnail/edit`       | edit    | photos.thumbnail.edit          |
| PUT/PATCH   | `/photos/{photo}/thumbnail`            | update  | photos.thumbnail.update        |
| DELETE      | `/photos/{photo}/thumbnail`            | destroy | photos.thumbnail.destroy       |

</div>

싱글턴 리소스에 대해 `DELETE` 라우트만 등록하고 싶고, 생성(create) 또는 저장(store) 라우트는 필요가 없다면 `destroyable` 메서드를 사용할 수 있습니다.

```php
Route::singleton(...)->destroyable();
```

<a name="api-singleton-resources"></a>
#### API 싱글턴 리소스 (API Singleton Resources)

`apiSingleton` 메서드는 API에서 사용할 싱글턴 리소스를 등록할 때 사용합니다. 이 경우 `create`와 `edit` 라우트가 등록되지 않습니다.

```php
Route::apiSingleton('profile', ProfileController::class);
```

물론, API 싱글턴 리소스도 `creatable`로 지정하면 해당 리소스에 대한 `store`, `destroy` 라우트가 등록됩니다.

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어 및 리소스 컨트롤러 (Middleware and Resource Controllers)

Laravel은 리소스 또는 싱글턴 리소스 라우트에서, 전체 또는 특정 메서드에 미들웨어를 할당할 수 있도록 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 지원합니다. 이 메서드들은 각 리소스 액션별로 미들웨어 적용을 세밀하게 제어할 수 있게 합니다.

#### 모든 메서드에 미들웨어 적용

`middleware` 메서드를 사용하면 리소스 또는 싱글턴 리소스 라우트에서 생성된 모든 라우트에 미들웨어를 할당할 수 있습니다.

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```

#### 특정 메서드에 미들웨어 적용

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

`middlewareFor` 메서드는 싱글턴 및 API 싱글턴 리소스 컨트롤러와도 함께 사용할 수 있습니다.

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```

#### 특정 메서드에서 미들웨어 제외

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
## 의존성 주입과 컨트롤러 (Dependency Injection and Controllers)

<a name="constructor-injection"></a>
#### 생성자 인젝션 (Constructor Injection)

Laravel의 [서비스 컨테이너](/docs/12.x/container)는 모든 컨트롤러 인스턴스를 생성할 때 사용됩니다. 따라서, 컨트롤러 생성자에서 타입힌트된 어떤 의존성(dependency)도 주입받을 수 있습니다. 명시한 의존성은 자동으로 주입되어 컨트롤러 인스턴스에서 사용할 수 있습니다.

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
#### 메서드 인젝션 (Method Injection)

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

컨트롤러 메서드에서 라우트 파라미터 값도 필요하다면, 의존성 객체 다음에 라우트 인수를 명시하면 됩니다. 예를 들어, 아래와 같이 라우트를 정의했다면

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

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