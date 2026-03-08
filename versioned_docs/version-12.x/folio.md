# Laravel Folio

- [소개](#introduction)
- [설치](#installation)
    - [페이지 경로 / URI](#page-paths-uris)
    - [서브도메인 라우팅](#subdomain-routing)
- [라우트 생성하기](#creating-routes)
    - [중첩 라우트](#nested-routes)
    - [인덱스 라우트](#index-routes)
- [라우트 파라미터](#route-parameters)
- [라우트 모델 바인딩](#route-model-binding)
    - [소프트 삭제된 모델](#soft-deleted-models)
- [렌더 훅](#render-hooks)
- [이름이 지정된 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Folio](https://github.com/laravel/folio)는 Laravel 애플리케이션의 라우팅을 간소화하기 위해 설계된 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿을 만드는 것만으로도 라우트를 쉽게 생성할 수 있습니다.

예를 들어, `/greeting` URL로 접근할 수 있는 페이지를 만들고 싶다면, 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 생성하면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치 (Installation)

시작하려면, Composer 패키지 관리자를 이용해 프로젝트에 Folio를 설치하세요:

```shell
composer require laravel/folio
```

Folio를 설치한 후, `folio:install` Artisan 명령어를 실행하면 Folio의 서비스 프로바이더가 애플리케이션에 설치됩니다. 이 서비스 프로바이더는 Folio가 라우트/페이지를 검색할 디렉터리를 등록합니다:

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI (Page Paths / URIs)

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 하지만 Folio 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리들을 커스터마이즈할 수 있습니다.

예를 들어, 동일한 Laravel 애플리케이션 내에서 여러 Folio 경로를 지정하는 것이 편리할 때가 있습니다. 애플리케이션의 "admin" 영역을 위한 별도의 Folio 페이지 디렉터리와 나머지 페이지용 디렉터리를 분리해서 사용할 수도 있죠.

이는 `Folio::path` 와 `Folio::uri` 메서드를 사용해 구현할 수 있습니다. `path` 메서드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 스캔할 디렉터리를 등록하고, `uri` 메서드는 해당 페이지 디렉터리의 "기본 URI"를 지정합니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages/guest'))->uri('/');

Folio::path(resource_path('views/pages/admin'))
    ->uri('/admin')
    ->middleware([
        '*' => [
            'auth',
            'verified',

            // ...
        ],
    ]);
```

<a name="subdomain-routing"></a>
### 서브도메인 라우팅 (Subdomain Routing)

들어오는 요청의 서브도메인에 따라 페이지를 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`의 요청을 나머지 Folio 페이지들과 다른 디렉터리로 라우팅하고 싶을 때가 있죠. 이럴 때는 `Folio::path`를 호출한 후 `domain` 메서드를 함께 호출하면 됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드는 도메인이나 서브도메인의 일부를 파라미터로 캡처할 수도 있습니다. 이렇게 캡처한 파라미터는 페이지 템플릿에 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성하기 (Creating Routes)

Folio에 마운트된 디렉터리에 Blade 템플릿을 배치하면 Folio 라우트를 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리를 마운트하지만, Folio 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리들을 커스터마이즈할 수 있습니다.

Blade 템플릿을 Folio 마운트 디렉터리에 두면, 바로 브라우저에서 접근할 수 있습니다. 예를 들어, `pages/schedule.blade.php`에 있는 페이지는 `http://example.com/schedule`에서 접근할 수 있습니다.

Folio 페이지 또는 라우트 목록을 빠르게 확인하려면, `folio:list` Artisan 명령어를 호출하세요:

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트 (Nested Routes)

중첩 라우트는 Folio 디렉터리 내에 하나 이상의 하위 디렉터리를 생성해 만들 수 있습니다. 예를 들어 `/user/profile` URL로 접근 가능한 페이지를 만들고 싶다면, `pages/user` 디렉터리 내에 `profile.blade.php` 템플릿을 생성하세요:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트 (Index Routes)

특정 페이지를 디렉터리 내의 "인덱스"로 지정하고 싶을 때가 있습니다. Folio 디렉터리에 `index.blade.php` 템플릿을 배치하면, 해당 디렉터리의 루트 URL 요청이 그 페이지로 라우팅됩니다:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 파라미터 (Route Parameters)

종종, 들어오는 요청 URL의 세그먼트를 페이지에 주입해서 사용할 필요가 있습니다. 예를 들어, 표시할 사용자 프로필의 "ID"를 가져와야 할 때가 그렇습니다. 이럴 땐 페이지 파일명에서 세그먼트를 대괄호로 감싸면 됩니다:

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

캡처된 세그먼트는 Blade 템플릿 내에서 변수로 접근할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>
```

여러 세그먼트를 캡처하려면, 대괄호 안 세그먼트 이름 앞에 `...` 세 개를 붙이면 됩니다:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트를 캡처할 때는, 데이터가 배열 형태로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

페이지 템플릿의 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델에 매칭되면, Folio는 Laravel의 라우트 모델 바인딩 기능을 자동으로 활용하여 모델 인스턴스를 페이지에 주입합니다:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

캡처된 모델은 Blade 템플릿 내에서 변수로 접근할 수 있으며, 변수명은 카멜 케이스(camel case)로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 키 커스터마이징

바인딩 된 Eloquent 모델을 `id` 컬럼이 아닌 다른 컬럼을 사용해 조회하고 싶을 때가 있습니다. 이 경우, 페이지 파일명에서 컬럼명을 지정할 수 있습니다. 예를 들어, `[Post:slug].blade.php`는 `id` 대신 `slug` 컬럼으로 바인딩을 시도합니다.

Windows 환경에서는 모델명과 키를 `-` 문자로 구분해 `[Post-slug].blade.php` 형태로 작성하세요.

#### 모델 위치 지정

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리에서 모델을 찾습니다. 하지만 필요하다면 템플릿 파일명에 완전한 네임스페이스를 포함한 모델 클래스명을 명시할 수 있습니다:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델 (Soft Deleted Models)

기본적으로 암묵적 모델 바인딩 시, 소프트 삭제된 모델은 조회되지 않습니다. 그렇지만 원한다면, 페이지 템플릿 내에서 `withTrashed` 함수를 호출하여 소프트 삭제된 모델도 조회할 수 있도록 Folio에 지시할 수 있습니다:

```php
<?php

use function Laravel\Folio\{withTrashed};

withTrashed();

?>

<div>
    User {{ $user->id }}
</div>
```

<a name="render-hooks"></a>
## 렌더 훅 (Render Hooks)

기본적으로 Folio는 페이지의 Blade 템플릿 내용을 HTTP 응답으로 반환합니다. 하지만 페이지 템플릿 내에서 `render` 함수를 호출해 응답을 커스터마이징할 수 있습니다.

`render` 함수는 클로저를 인자로 받으며, 이 클로저는 Folio가 렌더링하는 `View` 인스턴스를 전달받습니다. 이를 통해 추가 데이터를 뷰에 전달하거나 전체 응답을 커스터마이징할 수 있습니다. 또한 클로저는 다른 라우트 파라미터나 모델 바인딩 값들도 인자로 제공합니다:

```php
<?php

use App\Models\Post;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

use function Laravel\Folio\render;

render(function (View $view, Post $post) {
    if (! Auth::user()->can('view', $post)) {
        return response('Unauthorized', 403);
    }

    return $view->with('photos', $post->author->photos);
}); ?>

<div>
    {{ $post->content }}
</div>

<div>
    This author has also taken {{ count($photos) }} photos.
</div>
```

<a name="named-routes"></a>
## 이름이 지정된 라우트 (Named Routes)

`name` 함수를 사용해 특정 페이지 라우트의 이름을 지정할 수 있습니다:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Laravel의 이름이 지정된 라우트처럼, `route` 함수를 이용해 이름이 지정된 Folio 페이지에 대한 URL을 생성할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지가 파라미터를 가질 경우, `route` 함수에 해당 파라미터 값을 전달하면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어 (Middleware)

특정 페이지에 미들웨어를 적용하려면, 페이지 템플릿 내에서 `middleware` 함수를 호출하세요:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는 여러 페이지 그룹에 미들웨어를 할당하려면, `Folio::path` 메서드 뒤에 `middleware` 메서드를 체인으로 호출할 수 있습니다.

미들웨어를 적용할 페이지를 지정하려면, 미들웨어 배열의 키를 해당 페이지 URL 패턴으로 지정하세요. `*` 문자는 와일드카드로 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        // ...
    ],
]);
```

배열 내에 클로저를 포함해 인라인 익명 미들웨어도 정의할 수 있습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        function (Request $request, Closure $next) {
            // ...

            return $next($request);
        },
    ],
]);
```

<a name="route-caching"></a>
## 라우트 캐싱 (Route Caching)

Folio를 사용할 때는 항상 [Laravel의 라우트 캐싱 기능](/docs/12.x/routing#route-caching)을 활용해야 합니다. Folio는 `route:cache` Artisan 명령어를 감지하여, Folio 페이지 정의와 라우트 이름이 최대 성능을 위해 제대로 캐싱되도록 합니다.