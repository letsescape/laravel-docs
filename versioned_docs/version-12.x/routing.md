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
    - [미들웨어](#route-group-middleware)
    - [컨트롤러](#route-group-controllers)
    - [서브도메인 라우팅](#route-group-subdomain-routing)
    - [라우트 접두사](#route-group-prefixes)
    - [라우트 이름 접두사](#route-group-name-prefixes)
- [라우트 모델 바인딩](#route-model-binding)
    - [암묵적 바인딩](#implicit-binding)
    - [암묵적 Enum 바인딩](#implicit-enum-binding)
    - [명시적 바인딩](#explicit-binding)
- [Fallback 라우트](#fallback-routes)
- [요청 속도 제한 (Rate Limiting)](#rate-limiting)
    - [Rate Limiter 정의](#defining-rate-limiters)
    - [라우트에 Rate Limiter 연결](#attaching-rate-limiters-to-routes)
- [폼 메서드 스푸핑](#form-method-spoofing)
- [현재 라우트 접근](#accessing-the-current-route)
- [CORS (Cross-Origin Resource Sharing)](#cors)
- [라우트 캐싱](#route-caching)

<a name="basic-routing"></a>
## 기본 라우팅 (Basic Routing)

가장 기본적인 Laravel 라우트는 URI와 클로저(closure)를 받아들입니다. 이를 통해 복잡한 라우팅 설정 파일 없이도 간단하고 표현력 있는 방식으로 라우트와 동작을 정의할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
### 기본 라우트 파일

Laravel의 모든 라우트는 `routes` 디렉토리에 위치한 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `bootstrap/app.php` 파일에 지정된 설정에 따라 Laravel이 자동으로 로드합니다.

`routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의합니다. 이 라우트들은 `web` [middleware group](/docs/12.x/middleware#laravels-default-middleware-groups)에 속하며, 세션 상태 관리나 CSRF 보호와 같은 기능을 제공합니다.

대부분의 애플리케이션에서는 `routes/web.php` 파일에서 라우트 정의를 시작합니다. 이 파일에 정의된 라우트는 브라우저에서 해당 URL로 접근하여 실행할 수 있습니다.

예를 들어 다음 라우트는 브라우저에서 `http://example.com/user`로 접근하면 실행됩니다.

```php
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<a name="api-routes"></a>
#### API 라우트

애플리케이션에서 상태를 저장하지 않는(stateless) API를 제공하려는 경우 `install:api` Artisan 명령어를 사용해 API 라우팅을 활성화할 수 있습니다.

```shell
php artisan install:api
```

`install:api` 명령어는 [Laravel Sanctum](/docs/12.x/sanctum)을 설치합니다. Sanctum은 서드파티 API 소비자, SPA, 모바일 애플리케이션을 인증할 수 있는 간단하면서도 강력한 API 토큰 인증 기능을 제공합니다.

또한 이 명령어는 `routes/api.php` 파일을 생성합니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

물론 공개적으로 접근 가능해야 하는 라우트라면 `auth:sanctum` 미들웨어를 제거할 수 있습니다.

`routes/api.php`에 정의된 라우트는 상태를 유지하지 않는(stateless) 라우트이며 `api` [middleware group](/docs/12.x/middleware#laravels-default-middleware-groups)에 속합니다.

또한 `/api` URI 접두사가 자동으로 적용되므로 각 라우트마다 수동으로 추가할 필요가 없습니다. 접두사를 변경하려면 `bootstrap/app.php` 파일을 수정하면 됩니다.

```php
->withRouting(
    api: __DIR__.'/../routes/api.php',
    apiPrefix: 'api/admin',
    // ...
)
```

<a name="available-router-methods"></a>
#### 사용 가능한 Router 메서드

라우터는 모든 HTTP 메서드에 대응하는 라우트를 등록할 수 있습니다.

```php
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

여러 HTTP 메서드에 응답하는 라우트를 등록해야 하는 경우 `match` 메서드를 사용할 수 있습니다. 또는 모든 HTTP 메서드에 응답하는 라우트를 `any` 메서드로 등록할 수도 있습니다.

```php
Route::match(['get', 'post'], '/', function () {
    // ...
});

Route::any('/', function () {
    // ...
});
```

> [!NOTE]  
> 동일한 URI를 공유하는 여러 라우트를 정의할 때는 `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 라우트보다 먼저 정의해야 합니다. 그래야 들어오는 요청이 올바른 라우트와 매칭됩니다.

<a name="dependency-injection"></a>
#### 의존성 주입 (Dependency Injection)

라우트 콜백의 매개변수에 필요한 의존성을 타입 힌트로 선언할 수 있습니다. 선언된 의존성은 Laravel의 [service container](/docs/12.x/container)에 의해 자동으로 해결되고 콜백에 주입됩니다.

예를 들어 `Illuminate\Http\Request` 클래스를 타입 힌트로 지정하면 현재 HTTP 요청 객체가 자동으로 주입됩니다.

```php
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
#### CSRF 보호

`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 라우트로 요청하는 HTML 폼에는 반드시 CSRF 토큰 필드를 포함해야 합니다. 그렇지 않으면 요청이 거부됩니다.

CSRF 보호에 대한 자세한 내용은 [CSRF documentation](/docs/12.x/csrf)을 참고하십시오.

```blade
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
### 리다이렉트 라우트 (Redirect Routes)

다른 URI로 리다이렉트하는 라우트를 정의할 때 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 간단한 리다이렉트를 위해 별도의 라우트나 컨트롤러를 작성할 필요가 없도록 해주는 편리한 단축 기능입니다.

```php
Route::redirect('/here', '/there');
```

기본적으로 `Route::redirect`는 `302` 상태 코드를 반환합니다. 세 번째 매개변수를 사용해 상태 코드를 변경할 수 있습니다.

```php
Route::redirect('/here', '/there', 301);
```

또는 `Route::permanentRedirect` 메서드를 사용해 `301` 상태 코드를 반환할 수도 있습니다.

```php
Route::permanentRedirect('/here', '/there');
```

> [!WARNING]  
> 리다이렉트 라우트에서 라우트 파라미터를 사용할 경우 `destination`과 `status` 파라미터 이름은 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="view-routes"></a>
### 뷰 라우트 (View Routes)

라우트가 단순히 [view](/docs/12.x/views)만 반환하면 되는 경우 `Route::view` 메서드를 사용할 수 있습니다. `redirect`와 마찬가지로 별도의 라우트나 컨트롤러를 작성할 필요가 없는 간단한 단축 방식입니다.

`view` 메서드는 첫 번째 인수로 URI, 두 번째 인수로 뷰 이름을 받습니다. 세 번째 인수로는 뷰에 전달할 데이터를 배열로 전달할 수 있습니다.

```php
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!WARNING]  
> 뷰 라우트에서 라우트 파라미터를 사용할 경우 `view`, `data`, `status`, `headers` 파라미터 이름은 Laravel에서 예약되어 있으므로 사용할 수 없습니다.

<a name="listing-your-routes"></a>
### 라우트 목록 확인 (Listing Your Routes)

`route:list` Artisan 명령어를 사용하면 애플리케이션에 정의된 모든 라우트를 쉽게 확인할 수 있습니다.

```shell
php artisan route:list
```

기본적으로 각 라우트에 할당된 미들웨어는 출력에 표시되지 않습니다. `-v` 옵션을 사용하면 라우트 미들웨어와 미들웨어 그룹 이름을 확인할 수 있습니다.

```shell
php artisan route:list -v

# Expand middleware groups...
php artisan route:list -vv
```

특정 URI로 시작하는 라우트만 보고 싶다면 다음과 같이 사용할 수 있습니다.

```shell
php artisan route:list --path=api
```

서드파티 패키지에서 정의된 라우트를 제외하려면 `--except-vendor` 옵션을 사용할 수 있습니다.

```shell
php artisan route:list --except-vendor
```

반대로 서드파티 패키지에서 정의된 라우트만 표시하려면 `--only-vendor` 옵션을 사용합니다.

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

때로는 애플리케이션의 일부 라우트를 별도의 파일에 정의하고 싶을 수 있습니다. 이를 위해 `withRouting` 메서드에 `then` 클로저를 전달할 수 있습니다.

이 클로저 내부에서 애플리케이션에 필요한 추가 라우트를 등록할 수 있습니다.

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

또는 `using` 클로저를 전달하여 라우트 등록 과정을 완전히 직접 제어할 수도 있습니다. 이 인수를 사용하면 프레임워크는 HTTP 라우트를 자동으로 등록하지 않으며, 모든 라우트를 직접 등록해야 합니다.

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