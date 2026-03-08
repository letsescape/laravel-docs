# Laravel Folio

- [소개](#introduction)
- [설치](#installation)
    - [페이지 경로 / URI](#page-paths-uris)
    - [서브도메인 라우팅](#subdomain-routing)
- [라우트 생성하기](#creating-routes)
    - [중첩 라우트](#nested-routes)
    - [인덱스 라우트](#index-routes)
- [라우트 매개변수](#route-parameters)
- [라우트 모델 바인딩](#route-model-binding)
    - [소프트 삭제된 모델](#soft-deleted-models)
- [렌더 훅](#render-hooks)
- [이름 있는 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Folio](https://github.com/laravel/folio)는 Laravel 애플리케이션의 라우팅을 단순화하기 위해 설계된 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 라우트를 생성하는 일이 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿을 생성하는 것만큼 간단해집니다.

예를 들어, `/greeting` URL에서 접근 가능한 페이지를 만들고 싶다면 애플리케이션의 `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 생성하기만 하면 됩니다:

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## 설치 (Installation)

시작하려면 Composer 패키지 매니저를 이용해 Folio를 프로젝트에 설치하세요:

```shell
composer require laravel/folio
```

Folio를 설치한 후, `folio:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Folio의 서비스 프로바이더를 애플리케이션에 설치하며, Folio가 라우트/페이지를 검색할 디렉터리를 등록합니다:

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI (Page Paths / URIs)

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 하지만 Folio 서비스 프로바이더의 `boot` 메서드에서 이 디렉터리들을 자유롭게 커스터마이징할 수 있습니다.

예를 들어, 하나의 Laravel 애플리케이션 내에서 여러 Folio 경로를 지정하는 것이 편리할 때가 있습니다. 예를 들어, 애플리케이션의 "admin" 영역을 위한 별도의 Folio 페이지 디렉터리를 두고, 나머지 애플리케이션 페이지를 위한 다른 디렉터리를 사용하는 경우가 그렇습니다.

이럴 경우 `Folio::path`와 `Folio::uri` 메서드를 사용해 설정할 수 있습니다. `path` 메서드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 스캔할 디렉터리를 등록하며, `uri` 메서드는 해당 페이지 디렉터리에 대한 "기본 URI"를 지정합니다:

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

또한, 들어오는 요청의 서브도메인에 따라 페이지로 라우트할 수도 있습니다. 예를 들어, `admin.example.com`에서 들어오는 요청을 애플리케이션의 나머지 Folio 페이지와 다른 페이지 디렉터리로 라우팅하고 싶을 수도 있습니다. 이런 경우 `Folio::path` 호출 후 `domain` 메서드를 호출하면 됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` 메서드는 도메인 또는 서브도메인의 일부를 매개변수로 캡처할 수도 있습니다. 이렇게 캡처된 매개변수는 페이지 템플릿에 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## 라우트 생성하기 (Creating Routes)

Folio 라우트는 Folio가 마운트한 디렉터리에 Blade 템플릿을 배치함으로써 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리를 마운트하지만 Folio 서비스 프로바이더의 `boot` 메서드에서 이러한 경로를 자유롭게 바꿀 수 있습니다.

Blade 템플릿을 Folio 마운트 디렉터리에 배치하면, 브라우저를 통해 바로 접근할 수 있습니다. 예를 들어 `pages/schedule.blade.php`에 배치된 페이지는 브라우저에서 `http://example.com/schedule` URL로 접근할 수 있습니다.

모든 Folio 페이지/라우트 목록을 빠르게 보고 싶을 때는 `folio:list` Artisan 명령어를 실행하세요:

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
### 중첩 라우트 (Nested Routes)

하나 이상의 서브디렉터리를 생성하여 중첩 라우트를 만들 수 있습니다. 예를 들어 `/user/profile` 경로로 접근 가능한 페이지를 만들려면 `pages/user` 디렉터리 안에 `profile.blade.php` 템플릿을 생성하세요:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### 인덱스 라우트 (Index Routes)

특정 페이지를 디렉터리의 "인덱스"로 만들고 싶을 때가 있습니다. Folio 디렉터리에 `index.blade.php` 템플릿을 두면, 해당 디렉터리의 루트 요청은 그 페이지로 라우팅됩니다:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## 라우트 매개변수 (Route Parameters)

종종 들어오는 요청 URL의 일부 세그먼트를 페이지로 주입해서 사용해야 할 때가 있습니다. 예를 들어, 프로필을 보여줄 사용자의 "ID"에 접근해야 할 수도 있습니다. 이럴 때는 페이지 파일명에서 세그먼트 부분을 대괄호 `[]`로 감싸면 됩니다:

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

여러 세그먼트를 캡처하려면 세그먼트 앞에 세 개의 점 `...`을 붙이세요:

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

여러 세그먼트로 캡처한 경우, 해당 값들은 배열로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩 (Route Model Binding)

페이지 템플릿 파일명 내 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델과 일치하면 Folio는 Laravel의 라우트 모델 바인딩 기능을 자동으로 활용하여 해결된 모델 인스턴스를 페이지에 주입합니다:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

캡처된 모델은 Blade 템플릿의 변수로 접근할 수 있습니다. 모델 변수명은 카멜 케이스(camel case)로 변환됩니다:

```html
<div>
    User {{ $user->id }}
</div>
```

#### 키 커스터마이징

바운딩된 Eloquent 모델을 기본 `id` 컬럼이 아닌 다른 컬럼 기준으로 조회하고 싶을 때가 있습니다. 이럴 경우 페이지 파일명에서 컬럼명을 지정할 수 있습니다. 예를 들어 `[Post:slug].blade.php` 파일은 `id` 대신 `slug` 컬럼을 사용해 바인딩된 모델을 조회합니다.

Windows 환경에서는 모델 이름과 키를 구분할 때 `-` 문자를 사용하세요: `[Post-slug].blade.php`.

#### 모델 위치 지정

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리 내에서 모델을 찾습니다. 하지만 필요하다면 템플릿 파일명에 완전한 네임스페이스를 지정할 수도 있습니다:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델 (Soft Deleted Models)

기본적으로는 암묵적 모델 바인딩 시 소프트 삭제된 모델은 조회되지 않습니다. 하지만 원한다면 페이지 템플릿 안에서 `withTrashed` 함수를 호출하여 소프트 삭제된 모델도 조회하도록 Folio에 지시할 수 있습니다:

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

기본적으로 Folio는 해당 페이지 Blade 템플릿의 내용을 들어오는 요청에 대한 응답으로 반환합니다. 하지만 페이지 템플릿 내에서 `render` 함수를 호출하여 응답을 커스터마이징할 수 있습니다.

`render` 함수는 Folio가 렌더링하는 `View` 인스턴스를 인자로 받는 클로저(익명 함수)를 지정할 수 있게 해줍니다. 이를 활용해 뷰에 추가 데이터를 붙이거나 응답 전체를 변경할 수 있습니다. 이 클로저에서는 `View` 인스턴스뿐 아니라 라우트 매개변수나 모델 바인딩도 함께 전달받습니다:

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
## 이름 있는 라우트 (Named Routes)

특정 페이지 라우트에 이름을 지정하려면 `name` 함수를 사용하세요:

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Laravel의 이름 있는 라우트처럼 `route` 함수를 활용해 이름이 지정된 Folio 페이지의 URL을 생성할 수 있습니다:

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

페이지가 매개변수를 가진 경우, 그 값들을 `route` 함수에 전달하면 됩니다:

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## 미들웨어 (Middleware)

특정 페이지에 미들웨어를 적용하려면 해당 페이지 템플릿 내에서 `middleware` 함수를 호출하면 됩니다:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

또는 여러 페이지 그룹에 미들웨어를 할당하고 싶으면 `Folio::path` 호출 후 `middleware` 메서드를 체인으로 호출할 수 있습니다.

미들웨어를 적용할 페이지를 지정하기 위해, 미들웨어 배열을 적용할 URL 패턴을 키로 하여 지정할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다:

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

미들웨어 목록에 클로저를 포함해 인라인 익명 미들웨어도 정의할 수 있습니다:

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

Folio를 사용할 때는 항상 [Laravel의 라우트 캐싱 기능](/docs/master/routing#route-caching)을 활용하는 것이 좋습니다. Folio는 `route:cache` Artisan 명령어를 감지해 Folio 페이지 정의와 라우트 이름이 최대 성능을 위해 올바르게 캐싱되도록 처리합니다.