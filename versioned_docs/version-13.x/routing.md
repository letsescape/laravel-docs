# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 보기](#listing-your-routes)
    - [라우팅 사용자 지정](#routing-customization)
- [라우트 매개변수](#route-parameters)
    - [필수 매개변수](#required-parameters)
    - [선택적 매개변수](#parameters-optional-parameters)
    - [정규식 제약](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [하위 도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 열거형 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [대체 라우트](#fallback-routes)
- [속도 제한](#rate-limiting)
    - [속도 제한기 정의](#defining-rate-limiters)
    - [라우트에 속도 제한기 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근하기](#accessing-the-current-route)
- [교차 출처 리소스 공유(CORS)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저를 허용하여 복잡한 라우팅 구성 파일 없이 라우트 및 동작을 정의하는 매우 간단하고 표현력 있는 방법을 제공합니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 있는 라우트 파일에 정의되어 있습니다. 이러한 파일은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 구성을 사용하여 Laravel에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이러한 라우트에는 세션 상태 및 CSRF 보호와 같은 기능을 제공하는 `web` [미들웨어 그룹](/docs/13.x/middleware#laravels-default-middleware-groups)이 할당됩니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트를 정의하는 것부터 시작합니다. `routes/web.php`에 정의된 라우트는 정의된 라우트의 URL를 브라우저에 입력하여 액세스할 수 있습니다. 예를 들어, 브라우저에서 `http://example.com/user`로 이동하여 다음 라우트에 액세스할 수 있습니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태 비저장 API도 제공하는 경우 `install:api` Artisan 명령을 사용하여 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령은 타사 API 소비자, SPA 또는 모바일 애플리케이션을 인증하는 데 사용할 수 있는 강력하면서도 간단한 API 토큰 인증 가드를 제공하는 [Laravel Sanctum](/docs/13.x/sanctum)를 설치합니다. 또한 `install:api` 명령은 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

물론 공개적으로 액세스할 수 있는 라우트의 `auth:sanctum` 미들웨어를 자유롭게 생략할 수 있습니다.

`routes/api.php`의 라우트는 상태 비저장이며 `api` [미들웨어 그룹](/docs/13.x/middleware#laravels-default-middleware-groups)에 할당됩니다. 또한 `/api` URI 접두사는 이러한 라우트에 자동으로 적용되므로 파일의 모든 라우트에 수동으로 적용할 필요가 없습니다. 애플리케이션의 `bootstrap/app.php` 파일을 수정하여 접두사를 변경할 수 있습니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 라우터 메서드

라우터를 사용하면 모든 HTTP 동사에 응답하는 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

때로는 여러 HTTP 동사에 응답하는 라우트를 등록해야 할 수도 있습니다. `match` 메서드를 사용하면 됩니다. 또는 `any` 메서드를 사용하여 모든 HTTP 동사에 응답하는 라우트를 등록할 수도 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 공유하는 여러 개의 라우트를 정의하는 경우, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트는 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의되어야 합니다. 이렇게 해야 들어오는 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입

라우트의 콜백 시그니처에서 필요한 의존성을 타입힌트로 지정할 수 있습니다. 선언된 의존성은 Laravel [서비스 컨테이너](/docs/13.x/container)에 의해 자동으로 해석되어 콜백에 주입됩니다. 예를 들어, 현재 HTTP 요청이 라우트 콜백에 자동으로 주입되도록 `Illuminate\Http\Request` 클래스를 타입힌트로 지정할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH` 또는 `DELETE` 라우트를 가리키는 모든 HTML 양식에는 CSRF 토큰 필드가 포함되어야 합니다. 그렇지 않으면 요청이 거부됩니다. [CSRF 문서](/docs/13.x/csrf)에서 CSRF 보호에 대해 자세히 알아볼 수 있습니다.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트

다른 URI로 리다이렉트하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉트를 위해 전체 라우트나 컨트롤러를 정의할 필요 없이 편리한 단축 기능을 제공합니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 선택적으로 세 번째 매개변수를 사용하여 상태 코드를 변경할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용하여 `301` 상태 코드를 반환할 수 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 매개변수를 사용하는 경우, `destination`과 `status` 매개변수는 Laravel에 의해 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트

라우트가 [뷰](/docs/13.x/views)만 반환해야 하는 경우 `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드와 마찬가지로, 전체 라우트나 컨트롤러를 정의할 필요 없이 간단한 단축 기능을 제공합니다. `view` 메서드는 첫 번째 인수로 URI를, 두 번째 인수로 뷰 이름을 받습니다. 또한 선택적으로 세 번째 인수로 뷰에 전달할 데이터 배열을 지정할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 매개변수를 사용하는 경우 다음 매개변수는 Laravel에 의해 예약되어 있으므로 사용할 수 없습니다: `view`, `data`, `status` 및 `headers`.

<a name="listing-your-routes"></a>
### 라우트 목록 보기

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트의 개요를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 라우트 미들웨어는 `route:list` 출력에 표시되지 않습니다. 그러나 명령에 `-v` 옵션을 추가하여 Laravel에 라우트 미들웨어 및 미들웨어 그룹 이름을 표시하도록 지시할 수 있습니다.

```shell
php artisan route:list -v

# Expand middleware groups...
php artisan route:list -vv
```

또한 주어진 URI로 시작하는 라우트만 표시하도록 Laravel에 지시할 수도 있습니다.

```shell
php artisan route:list --path=api
```

또한 `route:list` 명령을 실행할 때 `--except-vendor` 옵션을 제공하여 타사 패키지에서 정의한 라우트를 숨기도록 Laravel에 지시할 수 있습니다.

```shell
php artisan route:list --except-vendor
```

마찬가지로 `route:list` 명령을 실행할 때 `--only-vendor` 옵션을 제공하여 타사 패키지에서 정의한 라우트만 표시하도록 Laravel에 지시할 수도 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 사용자 지정

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에 의해 구성되고 로드됩니다.

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

그러나 때로는 애플리케이션의 라우트 하위 집합을 포함하도록 완전히 새로운 파일을 정의해야 할 수도 있습니다. 이를 달성하기 위해 `withRouting` 메서드에 `then` 클로저를 제공할 수 있습니다. 이 클로저 내에서 애플리케이션에 필요한 추가 라우트를 등록할 수 있습니다.

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

또는 `withRouting` 메서드에 `using` 클로저를 제공하여 라우트 등록을 완전히 제어할 수도 있습니다. 이 인수가 전달되면 HTTP 라우트가 프레임워크에 의해 등록되지 않으며 모든 라우트를 수동으로 등록해야 합니다.

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
## 라우트 매개변수 (Route Parameters)

<a name="required-parameters"></a>
### 필수 매개변수

때로는 라우트 내에서 URI의 세그먼트를 캡처해야 할 수도 있습니다. 예를 들어, URL에서 사용자 ID를 캡처해야 할 수 있습니다. 라우트 매개변수를 정의하여 그렇게 할 수 있습니다:

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

라우트에 필요한 만큼 라우트 매개변수를 정의할 수 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 매개변수는 항상 `{}` 중괄호 안에 포함되며 영문자로 구성되어야 합니다. 라우트 매개변수 이름에는 밑줄(`_`)도 허용됩니다. 라우트 매개변수는 순서에 따라 라우트 콜백 / 컨트롤러에 주입됩니다. 라우트 콜백 / 컨트롤러 인수의 이름은 중요하지 않습니다.

<a name="parameters-and-dependency-injection"></a>
#### 매개변수 및 의존성 주입

라우트에 Laravel 서비스 컨테이너가 라우트 콜백에 자동으로 주입할 의존성이 있는 경우, 의존성 뒤에 라우트 매개변수를 나열해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 매개변수

때로는 URI에 항상 존재하지 않을 수도 있는 라우트 매개변수를 지정해야 할 수도 있습니다. 매개변수 이름 뒤에 `?` 표시를 배치하면 됩니다. 라우트의 해당 변수에 기본값을 지정하십시오.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규식 제약

라우트 인스턴스에서 `where` 메서드를 사용하여 라우트 매개변수의 형식을 제한할 수 있습니다. `where` 메서드는 매개변수의 이름과 매개변수가 어떻게 제한되어야 하는지를 정의하는 정규식을 받습니다.

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

편의를 위해, 자주 사용되는 일부 정규식 패턴에는 라우트에 패턴 제약 조건을 빠르게 추가할 수 있는 헬퍼 메서드가 제공됩니다.

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

들어오는 요청이 라우트 패턴 제약 조건과 일치하지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약

라우트 매개변수가 항상 주어진 정규 표현식에 의해 제한되도록 하려면 `pattern` 메서드를 사용할 수 있습니다. 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이러한 패턴을 정의해야 합니다.

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

패턴이 정의되면 해당 매개변수 이름을 사용하여 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시

Laravel 라우팅 구성요소를 사용하면 `/`를 제외한 모든 문자가 라우트 매개변수 값 내에 존재할 수 있습니다. `where` 조건 정규식을 사용하여 `/`가 자리 표시자의 일부가 되도록 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 마지막 라우트 세그먼트 내에서만 지원됩니다.

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

이름이 지정된 라우트를 사용하면 특정 라우트에 대한 URL이나 리다이렉트를 편리하게 생성할 수 있습니다. `name` 메서드를 라우트 정의에 체이닝하여 라우트에 이름을 지정할 수 있습니다.

```php
Route::get('/user/profile', function () {
    // ...
})->name('profile');
```

컨트롤러 액션에 대해서도 라우트 이름을 지정할 수 있습니다.

```php
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!WARNING]
> 라우트 이름은 항상 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
#### 이름이 지정된 라우트의 URL 생성

특정 라우트에 이름을 할당하면, Laravel의 `route`와 `redirect` 헬퍼 함수를 통해 URL을 생성하거나 리다이렉트할 때 라우트 이름을 사용할 수 있습니다.

```php
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');

return to_route('profile');
```

이름이 지정된 라우트가 매개변수를 정의하는 경우, 해당 매개변수를 `route` 함수의 두 번째 인수로 전달할 수 있습니다. 전달된 매개변수는 생성된 URL의 올바른 위치에 자동으로 삽입됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1]);
```

배열에 추가 매개변수를 전달하면 해당 키/값 쌍이 생성된 URL의 쿼리 문자열에 자동으로 추가됩니다.

```php
Route::get('/user/{id}/profile', function (string $id) {
    // ...
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// http://example.com/user/1/profile?photos=yes
```

> [!NOTE]
> 때로는 현재 로케일과 같은 URL 매개변수에 대해 요청 전체에 걸친 기본값을 지정하고 싶을 수 있습니다. 이를 위해 [`URL::defaults` 메서드](/docs/13.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
#### 현재 라우트 검사

현재 요청이 지정된 라우트로 라우팅되었는지 확인하려면 라우트 인스턴스에서 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어에서 현재 라우트 이름을 확인할 수 있습니다.

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
## 라우트 그룹 (Route Groups)

라우트 그룹을 사용하면 각 개별 라우트에서 해당 속성을 정의할 필요 없이 다수의 라우트에서 미들웨어와 같은 라우트 속성을 공유할 수 있습니다.

중첩된 그룹은 속성을 상위 그룹과 지능적으로 "병합"하려고 시도합니다. 미들웨어 및 `where` 조건은 이름과 접두사가 추가되는 동안 병합됩니다. URI 접두사의 네임스페이스 구분 기호와 슬래시는 적절한 곳에 자동으로 추가됩니다.

<a name="route-group-middleware"></a>
### 미들웨어

그룹 내의 모든 라우트에 [미들웨어](/docs/13.x/middleware)를 할당하려면 그룹을 정의하기 전에 `middleware` 메서드를 사용할 수 있습니다. 미들웨어는 배열에 나열된 순서대로 실행됩니다.

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
### 컨트롤러

라우트 그룹이 모두 동일한 [컨트롤러](/docs/13.x/controllers)를 사용하는 경우, `controller` 메서드를 사용하여 그룹 내의 모든 라우트에 대한 공통 컨트롤러를 정의할 수 있습니다. 그런 다음 라우트를 정의할 때 호출할 컨트롤러 메서드만 지정하면 됩니다.

```php
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
### 하위 도메인 라우팅

라우트 그룹은 하위 도메인 라우팅을 처리하는 데 사용될 수도 있습니다. 하위 도메인에는 라우트 URI와 마찬가지로 라우트 매개변수가 할당될 수 있으므로 라우트 또는 컨트롤러에서 사용할 하위 도메인의 일부를 캡처할 수 있습니다. 하위 도메인은 그룹을 정의하기 전에 `domain` 메서드를 호출하여 지정할 수 있습니다.

```php
Route::domain('{account}.example.com')->group(function () {
    Route::get('/user/{id}', function (string $account, string $id) {
        // ...
    });
});
```

<a name="route-group-prefixes"></a>
### 라우트 접두사

`prefix` 메서드는 그룹의 각 라우트 앞에 지정된 URI를 붙이는 데 사용될 수 있습니다. 예를 들어, 그룹 내의 모든 라우트 URI 앞에 `admin`를 붙일 수 있습니다.

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a name="route-group-name-prefixes"></a>
### 라우트 이름 접두사

`name` 메서드는 그룹의 각 라우트 이름 앞에 주어진 문자열을 붙이는 데 사용될 수 있습니다. 예를 들어, 그룹에 있는 모든 라우트의 이름 앞에 `admin`를 붙일 수 있습니다. 주어진 문자열은 지정된 그대로 정확하게 라우트 이름 앞에 붙으므로 접두사에 후행 `.` 문자를 제공해야 합니다.

```php
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

모델 ID를 라우트 또는 컨트롤러 액션에 주입할 때, 해당 ID에 해당하는 모델을 검색하기 위해 데이터베이스를 쿼리하는 경우가 많습니다. Laravel 라우트 모델 바인딩은 모델 인스턴스를 라우트에 직접 자동으로 주입하는 편리한 방법을 제공합니다. 예를 들어, 사용자의 ID를 주입하는 대신 해당 ID와 일치하는 전체 `User` 모델 인스턴스를 주입할 수 있습니다.

<a name="implicit-binding"></a>
### 암묵적 바인딩

Laravel은 라우트 또는 컨트롤러 액션에서 타입힌트된 변수 이름이 라우트 세그먼트 이름과 일치하는 Eloquent 모델을 자동으로 해석합니다. 예를 들어:

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

`$user` 변수는 `App\Models\User` Eloquent 모델로 타입힌트되어 있고 변수 이름이 `{user}` URI 세그먼트와 일치하므로, Laravel은 요청 URI의 해당 값과 일치하는 ID를 가진 모델 인스턴스를 자동으로 주입합니다. 일치하는 모델 인스턴스가 데이터베이스에서 발견되지 않으면 404 HTTP 응답이 자동으로 생성됩니다.

물론 컨트롤러 메서드를 사용하는 경우에도 암묵적 바인딩이 가능합니다. 마찬가지로 `{user}` URI 세그먼트는 `App\Models\User` 타입힌트를 포함하는 컨트롤러의 `$user` 변수와 일치합니다.

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
#### 소프트 삭제된 모델

일반적으로 암묵적 모델 바인딩은 [소프트 삭제](/docs/13.x/eloquent#soft-deleting)된 모델을 검색하지 않습니다. 그러나 라우트 정의에 `withTrashed` 메서드를 연결하여 암묵적 바인딩에 이러한 모델을 검색하도록 지시할 수 있습니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
#### 키 사용자 지정

때로는 `id` 이외의 열을 사용하여 Eloquent 모델을 확인하고 싶을 수도 있습니다. 이렇게 하려면 라우트 매개변수 정의에 열을 지정할 수 있습니다.

```php
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

주어진 모델 클래스를 검색할 때 모델 바인딩이 항상 `id` 이외의 데이터베이스 열을 사용하도록 하려면 Eloquent 모델에서 `getRouteKeyName` 메서드를 재정의할 수 있습니다.

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
#### 사용자 지정 키 및 범위 지정

단일 라우트 정의에서 여러 Eloquent 모델을 암묵적으로 바인딩하는 경우 두 번째 Eloquent 모델의 범위를 지정하여 이전 Eloquent 모델의 하위 항목이어야 할 수 있습니다. 예를 들어, 특정 사용자에 대한 슬러그로 블로그 게시물을 검색하는 다음 라우트 정의를 고려해 보세요.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

사용자 지정 키 암묵적 바인딩을 중첩된 라우트 매개변수로 사용하는 경우, Laravel은 부모 모델의 연관관계 이름을 규칙에 따라 추정하여 쿼리 범위를 자동으로 지정하고 중첩된 모델을 검색합니다. 이 경우 `User` 모델에 `Post` 모델을 검색하는 데 사용할 수 있는 `posts`(라우트 매개변수 이름의 복수형)라는 연관관계가 있다고 가정합니다.

원하는 경우 사용자 지정 키가 제공되지 않은 경우에도 "하위" 바인딩 범위를 지정하도록 Laravel에 지시할 수 있습니다. 이렇게 하려면 라우트를 정의할 때 `scopeBindings` 메서드를 호출하면 됩니다.

```php
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

또는 전체 라우트 정의 그룹에 범위 바인딩을 사용하도록 지시할 수 있습니다.

```php
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

마찬가지로, `withoutScopedBindings` 메서드를 호출하여 바인딩 범위를 지정하지 않도록 Laravel에 명시적으로 지시할 수 있습니다.

```php
Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
})->withoutScopedBindings();
```

<a name="customizing-missing-model-behavior"></a>
#### 누락된 모델 동작 사용자 지정

일반적으로 암묵적으로 바인딩된 모델을 찾을 수 없는 경우 404 HTTP 응답이 생성됩니다. 그러나 라우트를 정의할 때 `missing` 메서드를 호출하여 이 동작을 사용자 지정할 수 있습니다. `missing` 메서드는 암묵적으로 바인딩된 모델을 찾을 수 없는 경우 호출되는 클로저를 허용합니다.

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
### 암묵적 열거형 바인딩

PHP 8.1에서는 [Enums](https://www.php.net/manual/en/language.enumerations.backed.php)에 대한 지원이 도입되었습니다. 이 기능을 보완하기 위해, Laravel에서는 라우트 정의에서 [문자열 기반 Enum](https://www.php.net/manual/en/language.enumerations.backed.php)을 타입힌트할 수 있으며, 해당 라우트 세그먼트가 유효한 Enum 값에 해당하는 경우에만 라우트가 호출됩니다. 그렇지 않으면 404 HTTP 응답이 자동으로 반환됩니다. 예를 들어, 다음과 같은 Enum이 있다고 가정해 보겠습니다.

```php
<?php

namespace App\Enums;

enum Category: string
{
    case Fruits = 'fruits';
    case People = 'people';
}
```

`{category}` 라우트 세그먼트가 `fruits` 또는 `people`인 경우에만 호출되는 라우트를 정의할 수 있습니다. 그렇지 않으면 Laravel은 404 HTTP 응답을 반환합니다.

```php
use App\Enums\Category;
use Illuminate\Support\Facades\Route;

Route::get('/categories/{category}', function (Category $category) {
    return $category->value;
});
```

<a name="explicit-binding"></a>
### 명시적 바인딩

모델 바인딩을 사용하기 위해 Laravel의 암묵적 규칙 기반 모델 확인을 사용할 필요는 없습니다. 라우트 매개변수가 모델에 대응하는 방식을 명시적으로 정의할 수도 있습니다. 명시적 바인딩을 등록하려면 라우터의 `model` 메서드를 사용하여 지정된 매개변수에 대한 클래스를 지정합니다. `AppServiceProvider` 클래스의 `boot` 메서드 시작 부분에 명시적인 모델 바인딩을 정의해야 합니다.

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

다음으로 `{user}` 매개변수가 포함된 라우트를 정의합니다.

```php
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    // ...
});
```

모든 `{user}` 매개변수를 `App\Models\User` 모델에 바인딩했으므로 해당 클래스의 인스턴스가 라우트에 주입됩니다. 예를 들어 `users/1`에 대한 요청은 ID가 `1`인 데이터베이스에서 `User` 인스턴스를 삽입합니다.

일치하는 모델 인스턴스가 데이터베이스에서 발견되지 않으면 404 HTTP 응답이 자동으로 생성됩니다.

<a name="customizing-the-resolution-logic"></a>
#### 해석 로직 사용자 지정

자신만의 모델 바인딩 해석 로직을 정의하려면 `Route::bind` 메서드를 사용할 수 있습니다. `bind` 메서드에 전달하는 클로저는 URI 세그먼트의 값을 받아서 라우트에 주입할 클래스의 인스턴스를 반환해야 합니다. 이 작업은 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 수행해야 합니다.

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

또는 Eloquent 모델에서 `resolveRouteBinding` 메서드를 재정의할 수도 있습니다. 이 메서드는 URI 세그먼트의 값을 받아서 라우트에 주입할 클래스의 인스턴스를 반환해야 합니다.

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

라우트가 [암묵적 바인딩 범위 지정](#implicit-model-binding-scoping)을 활용하는 경우 `resolveChildRouteBinding` 메서드는 상위 모델의 하위 바인딩을 해결하는 데 사용됩니다.

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
## 대체 라우트 (Fallback Routes)

`Route::fallback` 메서드를 사용하면 수신 요청과 일치하는 다른 라우트가 없을 때 실행될 라우트를 정의할 수 있습니다. 일반적으로 처리되지 않은 요청은 애플리케이션의 예외 처리기를 통해 자동으로 "404" 페이지를 렌더링합니다. 그러나 일반적으로 `routes/web.php` 파일 내에서 `fallback` 라우트를 정의하므로 `web` 미들웨어 그룹의 모든 미들웨어는 라우트에 적용됩니다. 필요에 따라 이 라우트에 추가 미들웨어를 자유롭게 추가할 수 있습니다.

```php
Route::fallback(function () {
    // ...
});
```

<a name="rate-limiting"></a>
## 속도 제한 (Rate Limiting)

<a name="defining-rate-limiters"></a>
### 속도 제한기 정의

Laravel에는 특정 라우트 또는 라우트 그룹의 트래픽 양을 제한하는 데 활용할 수 있는 강력하고 사용자 지정 가능한 속도 제한 서비스가 포함되어 있습니다. 시작하려면 애플리케이션의 요구 사항을 충족하는 속도 제한기 구성을 정의해야 합니다.

속도 제한기는 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 정의될 수 있습니다.

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

속도 제한기는 `RateLimiter` 파사드의 `for` 메서드를 사용하여 정의됩니다. `for` 메서드는 속도 제한기 이름과 속도 제한기에 할당된 라우트에 적용해야 하는 제한 구성을 반환하는 클로저를 허용합니다. 제한 구성은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스입니다. 이 클래스에는 제한을 신속하게 정의할 수 있는 유용한 "빌더" 메서드가 포함되어 있습니다. 속도 제한기 이름은 원하는 문자열일 수 있습니다.

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

들어오는 요청이 지정된 속도 제한을 초과하는 경우 429 HTTP 상태 코드가 포함된 응답이 Laravel에 의해 자동으로 반환됩니다. 속도 제한에 따라 반환되어야 하는 자체 응답을 정의하려면 `response` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function (Request $request, array $headers) {
        return response('Custom response...', 429, $headers);
    });
});
```

속도 제한기 콜백은 들어오는 HTTP 요청 인스턴스를 수신하므로 들어오는 요청 또는 인증된 사용자를 기반으로 적절한 속도 제한을 동적으로 구축할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()?->vipCustomer()
        ? Limit::none()
        : Limit::perHour(10);
});
```

<a name="segmenting-rate-limits"></a>
#### 분할 속도 제한

때로는 임의의 값으로 속도 제한을 분할하고 싶을 수도 있습니다. 예를 들어, 사용자가 IP 주소별로 지정된 라우트에 분당 100회 접근하도록 허용할 수 있습니다. 이를 위해 속도 제한을 구성할 때 `by` 메서드를 사용할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
        ? Limit::none()
        : Limit::perMinute(100)->by($request->ip());
});
```

다른 예를 사용하여 이 기능을 설명하기 위해 라우트에 대한 액세스를 인증된 사용자 ID당 분당 100회 또는 게스트의 IP 주소당 분당 10회로 제한할 수 있습니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
        ? Limit::perMinute(100)->by($request->user()->id)
        : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
#### 다중 속도 제한

필요한 경우 지정된 속도 제한기 구성에 대한 속도 제한 배열을 반환할 수 있습니다. 각 속도 제한은 어레이 내에 배치된 순서에 따라 라우트에 대해 평가됩니다.

```php
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

동일한 `by` 값으로 분할된 여러 속도 제한을 할당하는 경우, 각 `by` 값이 고유한지 확인해야 합니다. 이를 위한 가장 쉬운 방법은 `by` 메서드에 전달하는 값에 접두사를 붙이는 것입니다.

```php
RateLimiter::for('uploads', function (Request $request) {
    return [
        Limit::perMinute(10)->by('minute:'.$request->user()->id),
        Limit::perDay(1000)->by('day:'.$request->user()->id),
    ];
});
```

<a name="response-base-rate-limiting"></a>
#### 응답 기반 속도 제한

들어오는 요청의 속도를 제한하는 것 외에도, Laravel에서는 `after` 메서드를 사용하여 응답을 기반으로 속도를 제한할 수 있습니다. 이는 유효성 검증 오류, 404 응답 또는 기타 특정 HTTP 상태 코드에 대해서만 속도 제한을 적용하고 싶을 때 유용합니다.

`after` 메서드는 응답을 받는 클로저를 인수로 받으며, 해당 응답이 속도 제한에 포함되어야 하면 `true`를, 무시해야 하면 `false`를 반환해야 합니다. 이는 연속적인 404 응답을 제한하여 열거 공격을 방지하거나, 성공적인 작업만 제한해야 하는 엔드포인트에서 유효성 검증에 실패한 요청을 속도 제한 소진 없이 재시도할 수 있도록 할 때 특히 유용합니다.

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
### 라우트에 속도 제한기 연결

`throttle` [미들웨어](/docs/13.x/middleware)를 사용하여 속도 제한기를 라우트 또는 라우트 그룹에 연결할 수 있습니다. 스로틀 미들웨어는 라우트에 할당하려는 속도 제한기의 이름을 허용합니다.

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
#### Redis로 조절

기본적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑됩니다. 그러나 Redis를 애플리케이션 캐시 드라이버로 사용하는 경우 Laravel에 Redis를 사용하여 속도 제한을 관리하도록 지시할 수 있습니다. 이렇게 하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `throttleWithRedis` 메서드를 사용해야 합니다. 이 메서드는 `throttle` 미들웨어를 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 미들웨어 클래스에 매핑합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->throttleWithRedis();
    // ...
})
```

<a name="form-method-spoofing"></a>
## 폼 메서드 스푸핑 (Form Method Spoofing)

HTML 폼은 `PUT`, `PATCH`, `DELETE` 액션을 지원하지 않습니다. 따라서 HTML 폼에서 호출되는 `PUT`, `PATCH`, `DELETE` 라우트를 정의할 때는 숨겨진 `_method` 필드를 폼에 추가해야 합니다. `_method` 필드로 전송된 값이 HTTP 요청 메서드로 사용됩니다.

```blade
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

편의를 위해 `@method` [Blade 지시어](/docs/13.x/blade)를 사용하여 `_method` 입력 필드를 생성할 수 있습니다.

```blade
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
## 현재 라우트 접근하기 (Accessing the Current Route)

들어오는 요청을 처리하는 라우트에 대한 정보를 얻으려면 `Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

[라우트 파사드의 기본 클래스](https://api.laravel.com/docs/13.x/Illuminate/Routing/Router.html) 및 [라우트 인스턴스](https://api.laravel.com/docs/13.x/Illuminate/Routing/Route.html)에 대한 API 문서를 참조하여 라우터 및 라우트 클래스에서 사용할 수 있는 모든 메서드를 검토할 수 있습니다.

<a name="cors"></a>
## 교차 출처 리소스 공유(CORS) (Cross-Origin Resource Sharing (CORS))

Laravel은 사용자가 설정한 값을 사용하여 CORS `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. `OPTIONS` 요청은 애플리케이션의 글로벌 미들웨어 스택에 자동으로 포함되는 `HandleCors` [미들웨어](/docs/13.x/middleware)에 의해 자동으로 처리됩니다.

때때로 애플리케이션의 CORS 설정 값을 사용자 지정해야 할 수 있습니다. `config:publish` Artisan 명령어를 사용하여 `cors` 설정 파일을 퍼블리시하면 됩니다.

```shell
php artisan config:publish cors
```

이 명령어는 애플리케이션의 `config` 디렉토리에 `cors.php` 설정 파일을 생성합니다.

> [!NOTE]
> CORS 및 CORS 헤더에 대한 자세한 내용은 [CORS에 대한 MDN 웹 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참조하세요.

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

애플리케이션을 프로덕션에 배포할 때 Laravel의 라우트 캐시를 활용해야 합니다. 라우트 캐시를 사용하면 애플리케이션의 모든 라우트를 등록하는 데 걸리는 시간이 크게 줄어듭니다. 라우트 캐시를 생성하려면 `route:cache` Artisan 명령을 실행합니다.

```shell
php artisan route:cache
```

이 명령을 실행하면 캐시된 라우트 파일이 모든 요청에 ​​로드됩니다. 새로운 라우트를 추가하는 경우 새로운 라우트 캐시를 생성해야 한다는 점을 기억하세요. 따라서 프로젝트 배포 중에만 `route:cache` 명령을 실행해야 합니다.

`route:clear` 명령을 사용하여 라우트 캐시를 지울 수 있습니다.

```shell
php artisan route:clear
```
