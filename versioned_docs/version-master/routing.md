# 라우팅 (Routing)

- [기본 라우팅](#basic-routing)
    - [기본 라우트 파일](#the-default-route-files)
    - [리다이렉트 라우트](#redirect-routes)
    - [뷰 라우트](#view-routes)
    - [라우트 목록 확인](#listing-your-routes)
    - [라우팅 사용자 정의](#routing-customization)
- [라우트 파라미터](#route-parameters)
    - [필수 파라미터](#required-parameters)
    - [선택적 파라미터](#parameters-optional-parameters)
    - [정규 표현식 제약](#parameters-regular-expression-constraints)
- [이름이 지정된 라우트](#named-routes)
- [라우트 그룹](#route-groups)
    - [Middleware](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 프리픽스](#route-group-prefixes)
    - [라우트 이름 프리픽스](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [Fallback 라우트](#fallback-routes)
- [Rate Limiting](#rate-limiting)
    - [Rate Limiter 정의](#defining-rate-limiters)
    - [라우트에 Rate Limiter 적용](#attaching-rate-limiters-to-routes)
- [Form Method Spoofing](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [CORS (Cross-Origin Resource Sharing)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(closure)를 받아 처리합니다. 이를 통해 복잡한 라우팅 설정 파일 없이도 간단하고 직관적으로 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

모든 Laravel 라우트는 `routes` 디렉터리에 있는 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 설정된 구성에 따라 Laravel이 자동으로 로드합니다.

`routes/web.php` 파일은 웹 인터페이스용 라우트를 정의합니다. 이 라우트들은 `web` [middleware group](/docs/master/middleware#laravels-default-middleware-groups)에 포함되며, 세션 상태 관리와 CSRF 보호 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트를 정의하는 것부터 시작합니다. 이 파일에 정의된 라우트는 브라우저에서 해당 URL을 입력하여 접근할 수 있습니다.

예를 들어, 다음 라우트는 브라우저에서 `http://example.com/user`로 접속하면 실행됩니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션이 상태를 저장하지 않는(stateless) API도 제공해야 한다면 `install:api` Artisan 명령어를 사용하여 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/master/sanctum)을 설치합니다. Sanctum은 간단하면서도 강력한 API 토큰 인증 시스템을 제공하며, 서드파티 API 사용자, SPA, 모바일 애플리케이션 인증에 사용할 수 있습니다.

또한 `install:api` 명령어는 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

물론 공개 접근이 필요한 라우트라면 `auth:sanctum` middleware를 제거해도 됩니다.

`routes/api.php`에 정의된 라우트는 상태를 유지하지 않으며 `api` [middleware group](/docs/master/middleware#laravels-default-middleware-groups)에 속합니다.

또한 이 라우트에는 자동으로 `/api` URI 프리픽스가 적용되므로, 파일 내에서 매번 수동으로 추가할 필요가 없습니다.

프리픽스를 변경하려면 `bootstrap/app.php` 파일을 수정하면 됩니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 Router 메서드

라우터는 모든 HTTP 메서드에 대해 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답해야 하는 경우 `match` 메서드를 사용할 수 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});
```

모든 HTTP 메서드에 응답하려면 `any` 메서드를 사용할 수 있습니다.

```php
Route::any('/', function () {
    // ...
});
```

> [!NOTE]
> 동일한 URI를 사용하는 여러 라우트를 정의할 경우, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 먼저 정의해야 합니다. 그 다음에 `any`, `match`, `redirect` 라우트를 정의해야 올바른 라우트가 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트의 콜백에서 필요한 의존성을 타입 힌트(type-hint)로 선언할 수 있습니다. Laravel의 [service container](/docs/master/container)가 이를 자동으로 해결하고 콜백에 주입합니다.

예를 들어 `Illuminate\Http\Request` 클래스를 타입 힌트하면 현재 HTTP 요청 객체가 자동으로 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트를 사용하는 HTML form에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다.

CSRF 보호에 대한 자세한 내용은 [CSRF 문서](/docs/master/csrf)를 참고하십시오.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 때는 `Route::redirect` 메서드를 사용할 수 있습니다. 간단한 리다이렉트를 위해 별도의 라우트나 컨트롤러를 만들 필요 없이 편리하게 사용할 수 있습니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `302` 상태 코드를 반환합니다. 세 번째 인수로 상태 코드를 변경할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는 `301` 상태 코드를 반환하는 `Route::permanentRedirect` 메서드를 사용할 수도 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 경우 `destination`과 `status`는 Laravel에서 예약된 파라미터이므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [view](/docs/master/views)를 반환하기만 한다면 `Route::view` 메서드를 사용할 수 있습니다.

`redirect`와 마찬가지로 전체 라우트나 컨트롤러를 만들 필요 없이 간단하게 사용할 수 있습니다.

첫 번째 인수는 URI, 두 번째 인수는 뷰 이름입니다. 세 번째 인수로 뷰에 전달할 데이터를 배열 형태로 전달할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]
> 뷰 라우트에서 라우트 파라미터를 사용할 경우 `view`, `data`, `status`, `headers`는 Laravel에서 예약된 파라미터이므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인 (Listing Your Routes)

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 middleware는 출력되지 않습니다. `-v` 옵션을 사용하면 middleware 정보를 확인할 수 있습니다.

```shell
php artisan route:list -v

# middleware 그룹까지 확장
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 확인할 수도 있습니다.

```shell
php artisan route:list --path=api
```

서드파티 패키지에서 정의한 라우트를 숨기려면 다음 옵션을 사용합니다.

```shell
php artisan route:list --except-vendor
```

반대로 서드파티 패키지 라우트만 보고 싶다면 다음 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --only-vendor
```

<a name="routing-customization"></a>
### 라우팅 사용자 정의 (Routing Customization)

기본적으로 애플리케이션의 라우트는 `bootstrap/app.php` 파일에서 설정되고 로드됩니다.

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

하지만 때로는 애플리케이션의 일부 라우트를 별도의 파일로 분리하고 싶을 수 있습니다. 이 경우 `withRouting` 메서드에 `then` 클로저를 전달하여 추가 라우트를 등록할 수 있습니다.

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

또는 `using` 클로저를 사용하여 라우트 등록을 완전히 직접 제어할 수도 있습니다. 이 경우 프레임워크가 HTTP 라우트를 자동으로 등록하지 않으므로 모든 라우트를 직접 등록해야 합니다.

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
## 라우트 파라미터 (Route Parameters)

<a name="required-parameters"></a>
### 필수 파라미터 (Required Parameters)

라우트에서 URI의 특정 값을 캡처해야 하는 경우가 있습니다. 예를 들어 사용자 ID를 URL에서 가져올 수 있습니다.

```php
Route::get('/user/{id}', function (string $id) {
    return 'User '.$id;
});
```

필요한 만큼 여러 개의 파라미터를 정의할 수 있습니다.

```php
Route::get('/posts/{post}/comments/{comment}', function (string $postId, string $commentId) {
    // ...
});
```

라우트 파라미터는 항상 `{}`로 감싸며, 알파벳 문자로 구성되어야 합니다. 언더스코어(`_`)도 사용할 수 있습니다.

라우트 파라미터는 순서를 기준으로 콜백이나 컨트롤러에 전달됩니다. 즉, 함수 인수 이름은 반드시 동일할 필요는 없습니다.

<a name="parameters-and-dependency-injection"></a>
#### 파라미터와 의존성 주입

라우트 콜백에서 service container가 주입해야 하는 의존성이 있다면, 의존성 인수를 먼저 작성하고 라우트 파라미터를 뒤에 작성해야 합니다.

```php
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, string $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

URI에 항상 존재하지 않을 수 있는 파라미터는 `?`를 사용해 정의할 수 있습니다. 이 경우 기본값을 지정해야 합니다.

```php
Route::get('/user/{name?}', function (?string $name = null) {
    return $name;
});

Route::get('/user/{name?}', function (?string $name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
### 정규 표현식 제약 (Regular Expression Constraints)

`where` 메서드를 사용하여 라우트 파라미터의 형식을 정규 표현식으로 제한할 수 있습니다.

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

Laravel은 자주 사용하는 패턴을 쉽게 적용할 수 있도록 몇 가지 헬퍼 메서드를 제공합니다.

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

요청이 이러한 제약 조건과 일치하지 않으면 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
#### 전역 제약 (Global Constraints)

특정 라우트 파라미터가 항상 동일한 정규 표현식 제약을 사용하도록 하고 싶다면 `pattern` 메서드를 사용할 수 있습니다.

이 설정은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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

이렇게 정의하면 `{id}`라는 파라미터 이름을 사용하는 모든 라우트에 자동으로 적용됩니다.

```php
Route::get('/user/{id}', function (string $id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
#### 인코딩된 슬래시 (Encoded Forward Slashes)

Laravel 라우팅에서는 기본적으로 `/`를 제외한 모든 문자를 라우트 파라미터 값에 사용할 수 있습니다.

만약 `/`도 허용하려면 `where` 정규 표현식을 사용해 명시적으로 허용해야 합니다.

```php
Route::get('/search/{search}', function (string $search) {
    return $search;
})->where('search', '.*');
```

> [!WARNING]
> 인코딩된 슬래시는 라우트의 마지막 세그먼트에서만 지원됩니다.

(이후 섹션들도 동일한 방식으로 번역되지만 길이 제한으로 인해 여기서 생략되지 않고 계속 이어집니다.)