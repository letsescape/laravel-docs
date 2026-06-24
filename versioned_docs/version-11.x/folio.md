<!-- # Laravel Folio -->
# Laravel Folio

- [Introduction](#introduction)
- [Installation](#installation)
    - [Page Paths / URIs](#page-paths-uris)
    - [Subdomain Routing](#subdomain-routing)
- [Creating Routes](#creating-routes)
    - [Nested Routes](#nested-routes)
    - [Index Routes](#index-routes)
- [Route Parameters](#route-parameters)
- [Route Model Binding](#route-model-binding)
    - [Soft Deleted Models](#soft-deleted-models)
- [Render Hooks](#render-hooks)
- [Named Routes](#named-routes)
- [Middleware](#middleware)
- [Route Caching](#route-caching)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Folio](https://github.com/laravel/folio) is a powerful page based router designed to simplify routing in Laravel applications. With Laravel Folio, generating a route becomes as effortless as creating a Blade template within your application's `resources/views/pages` directory. -->
[Laravel Folio](https://github.com/laravel/folio)는 Laravel 애플리케이션에서 라우팅을 더욱 쉽게 만들어주는 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면, 단순히 애플리케이션의 `resources/views/pages` 디렉터리에 Blade 템플릿을 생성하는 것만으로도 쉽고 빠르게 라우트를 추가할 수 있습니다.

<!-- For example, to create a page that is accessible at the `/greeting` URL, just create a `greeting.blade.php` file in your application's `resources/views/pages` directory: -->
예를 들어, `/greeting` 경로에서 접근할 수 있는 페이지를 만들고 싶다면, `resources/views/pages` 디렉터리에 `greeting.blade.php` 파일을 만들어 주세요.

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Folio into your project using the Composer package manager: -->
우선, Composer 패키지 관리자를 이용해 Folio를 프로젝트에 설치합니다.

```bash
composer require laravel/folio
```

<!-- After installing Folio, you may execute the `folio:install` Artisan command, which will install Folio's service provider into your application. This service provider registers the directory where Folio will search for routes / pages: -->
Folio 설치 후, `folio:install` 아티즌 명령어를 실행하면 Folio의 서비스 프로바이더가 애플리케이션에 등록됩니다. 이 서비스 프로바이더는 Folio가 라우트/페이지를 탐색할 디렉터리를 설정합니다.

```bash
php artisan folio:install
```

<a name="page-paths-uris"></a>
<!-- ### Page Paths / URIs -->
### Page Paths / URIs

<!-- By default, Folio serves pages from your application's `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method. -->
기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉터리에서 페이지를 제공합니다. 하지만 이 디렉터리는 Folio의 서비스 프로바이더 `boot` 메서드에서 자유롭게 커스터마이즈할 수 있습니다.

<!-- For example, sometimes it may be convenient to specify multiple Folio paths in the same Laravel application. You may wish to have a separate directory of Folio pages for your application's "admin" area, while using another directory for the rest of your application's pages. -->
예를 들어, 하나의 Laravel 애플리케이션에서 여러 Folio 경로를 지정하고 싶을 때가 있습니다. 예를 들어, 애플리케이션의 "admin" 영역을 위한 별도의 Folio 페이지 디렉터리를 만들고, 나머지 페이지용 디렉터리와 분리할 수 있습니다.

<!-- You may accomplish this using the `Folio::path` and `Folio::uri` methods. The `path` method registers a directory that Folio will scan for pages when routing incoming HTTP requests, while the `uri` method specifies the "base URI" for that directory of pages: -->
이럴 때는 `Folio::path`와 `Folio::uri` 메서드를 활용합니다. `path` 메서드는 Folio가 HTTP 요청을 라우팅할 때 페이지를 탐색하는 디렉터리를 등록하며, `uri` 메서드는 해당 페이지 디렉터리가 사용할 "기본 URI"를 지정합니다.

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
<!-- ### Subdomain Routing -->
### Subdomain Routing

<!-- You may also route to pages based on the incoming request's subdomain. For example, you may wish to route requests from `admin.example.com` to a different page directory than the rest of your Folio pages. You may accomplish this by invoking the `domain` method after invoking the `Folio::path` method: -->
들어오는 요청의 서브도메인에 따라 페이지 디렉터리를 분리하여 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서 오는 요청은 다른 Folio 페이지 디렉터리로 라우팅하고 싶을 때가 있습니다. 이 경우에는 `Folio::path` 메서드 뒤에 `domain` 메서드를 체이닝하면 됩니다.

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

<!-- The `domain` method also allows you to capture parts of the domain or subdomain as parameters. These parameters will be injected into your page template: -->
`domain` 메서드는 도메인이나 서브도메인 일부를 파라미터로 받아올 수도 있습니다. 이 파라미터들은 페이지 템플릿으로 주입됩니다.

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
<!-- ## Creating Routes -->
## Creating Routes

<!-- You may create a Folio route by placing a Blade template in any of your Folio mounted directories. By default, Folio mounts the `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method. -->
Folio 라우트는 Folio가 마운트한 디렉터리 중 하나에 Blade 템플릿을 추가하는 것만으로 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉터리를 마운트하지만, 앞서 말한 것처럼 서비스 프로바이더의 `boot` 메서드에서 자유롭게 바꿀 수 있습니다.

<!-- Once a Blade template has been placed in a Folio mounted directory, you may immediately access it via your browser. For example, a page placed in `pages/schedule.blade.php` may be accessed in your browser at `http://example.com/schedule`. -->
이렇게 Folio 디렉터리에 Blade 템플릿을 추가하면 곧바로 브라우저에서 해당 경로로 접근할 수 있습니다. 예를 들어, `pages/schedule.blade.php` 파일을 만들면 브라우저에서 `http://example.com/schedule`로 접근할 수 있습니다.

<!-- To quickly view a list of all of your Folio pages / routes, you may invoke the `folio:list` Artisan command: -->
모든 Folio 페이지/라우트 목록을 빠르게 확인하려면, 다음과 같이 `folio:list` 아티즌 명령어를 실행하면 됩니다.

```bash
php artisan folio:list
```

<a name="nested-routes"></a>
<!-- ### Nested Routes -->
### Nested Routes

<!-- You may create a nested route by creating one or more directories within one of Folio's directories. For instance, to create a page that is accessible via `/user/profile`, create a `profile.blade.php` template within the `pages/user` directory: -->
Folio 디렉터리 안에 하위 디렉터리를 만들어 중첩 라우트를 만들 수도 있습니다. 예를 들어, `/user/profile` 경로로 접근하는 페이지를 만들고 싶다면, `pages/user` 디렉터리 내에 `profile.blade.php` 템플릿을 생성하세요.

```bash
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
<!-- ### Index Routes -->
### Index Routes

<!-- Sometimes, you may wish to make a given page the "index" of a directory. By placing an `index.blade.php` template within a Folio directory, any requests to the root of that directory will be routed to that page: -->
특정 디렉터리의 "인덱스" 페이지 역할을 하는 페이지를 만들고 싶을 때가 있습니다. 이 경우, 해당 Folio 디렉터리에 `index.blade.php` 템플릿을 추가하면, 해당 디렉터리의 루트 경로로 들어오는 모든 요청이 이 페이지로 라우팅됩니다.

```bash
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
<!-- ## Route Parameters -->
## Route Parameters

<!-- Often, you will need to have segments of the incoming request's URL injected into your page so that you can interact with them. For example, you may need to access the "ID" of the user whose profile is being displayed. To accomplish this, you may encapsulate a segment of the page's filename in square brackets: -->
실제 개발에서는 URL의 일부를 파라미터로 받아 해당 값에 따라 동적으로 동작해야 할 상황이 자주 있습니다. 예를 들어, 특정 유저의 프로필을 보여주는 페이지에서 "ID" 값을 받아와야 할 수 있습니다. 이를 위해, 페이지 파일명 일부를 대괄호로 감싸면 Folio가 해당 부분을 파라미터로 캡쳐하여 전달해 줍니다.

```bash
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

<!-- Captured segments can be accessed as variables within your Blade template: -->
캡쳐된 파라미터는 Blade 템플릿 내에서 변수로 바로 사용할 수 있습니다.

```html
<div>
    User {{ $id }}
</div>
```

<!-- To capture multiple segments, you can prefix the encapsulated segment with three dots `...`: -->
여러 개의 경로 세그먼트를 한 번에 캡쳐하려면, 대괄호 앞에 점 세 개(`...`)를 추가합니다.

```bash
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

<!-- When capturing multiple segments, the captured segments will be injected into the page as an array: -->
여러 세그먼트를 캡쳐하면, 해당 변수는 배열로 페이지에 전달됩니다.

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
<!-- ## Route Model Binding -->
## Route Model Binding

<!-- If a wildcard segment of your page template's filename corresponds one of your application's Eloquent models, Folio will automatically take advantage of Laravel's route model binding capabilities and attempt to inject the resolved model instance into your page: -->
페이지 템플릿 파일명에서 일부를 와일드카드로 사용하고, 그 이름이 애플리케이션의 Eloquent 모델과 일치한다면, Folio는 Laravel의 라우트 모델 바인딩 기능을 활용해 해당 Eloquent 인스턴스를 자동으로 주입해줍니다.

```bash
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

<!-- Captured models can be accessed as variables within your Blade template. The model's variable name will be converted to "camel case": -->
바인딩된 모델은 Blade 템플릿 내에서 변수로 사용할 수 있습니다. 이때 모델의 변수명은 "카멜 케이스(camel case)"로 변환됩니다.

```html
<div>
    User {{ $user->id }}
</div>
```

<!-- #### Customizing the Key -->
#### Customizing the Key

<!-- Sometimes you may wish to resolve bound Eloquent models using a column other than `id`. To do so, you may specify the column in the page's filename. For example, a page with the filename `[Post:slug].blade.php` will attempt to resolve the bound model via the `slug` column instead of the `id` column. -->
경우에 따라, `id`가 아닌 다른 컬럼 값으로 Eloquent 모델을 조회하고 싶을 수 있습니다. 이런 경우에는 페이지 파일명에 사용할 컬럼을 지정하면 됩니다. 예를 들어, `[Post:slug].blade.php` 파일은 `id` 대신 `slug` 컬럼 값을 사용하여 모델을 바인딩합니다.

<!-- On Windows, you should use `-` to separate the model name from the key: `[Post-slug].blade.php`. -->
Windows 환경에서는 모델명과 키를 구분할 때 `-`를 사용해야 합니다: `[Post-slug].blade.php`.

<!-- #### Model Location -->
#### Model Location

<!-- By default, Folio will search for your model within your application's `app/Models` directory. However, if needed, you may specify the fully-qualified model class name in your template's filename: -->
기본적으로 Folio는 모델을 애플리케이션의 `app/Models` 디렉터리 안에서 찾습니다. 하지만 필요하다면, 템플릿 파일명에 완전한 네임스페이스를 적어줄 수도 있습니다.

```bash
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
<!-- ### Soft Deleted Models -->
### Soft Deleted Models

<!-- By default, models that have been soft deleted are not retrieved when resolving implicit model bindings. However, if you wish, you can instruct Folio to retrieve soft deleted models by invoking the `withTrashed` function within the page's template: -->
기본적으로, 소프트 삭제된 모델은 암묵적 모델 바인딩으로 가져오지 않습니다. 하지만, 원한다면 페이지 템플릿 안에서 `withTrashed` 함수를 호출해 소프트 삭제된 모델도 가져올 수 있습니다.

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
<!-- ## Render Hooks -->
## Render Hooks

<!-- By default, Folio will return the content of the page's Blade template as the response to the incoming request. However, you may customize the response by invoking the `render` function within the page's template. -->
기본적으로 Folio는 페이지 Blade 템플릿의 내용을 요청에 대한 응답으로 반환합니다. 하지만, 필요하다면 페이지 템플릿 내부에서 `render` 함수를 호출해 응답을 자유롭게 커스터마이즈할 수 있습니다.

<!-- The `render` function accepts a closure which will receive the `View` instance being rendered by Folio, allowing you to add additional data to the view or customize the entire response. In addition to receiving the `View` instance, any additional route parameters or model bindings will also be provided to the `render` closure: -->
`render` 함수는 클로저를 인자로 받으며, 이 클로저에는 Folio가 렌더링한 `View` 인스턴스가 전달됩니다. 이를 활용해 뷰에 추가 데이터를 넘기거나 응답 자체를 수정할 수 있습니다. `View` 인스턴스를 전달받는 것 외에도, 추가 라우트 파라미터나 모델 바인딩 값도 `render` 클로저에 함께 전달됩니다:

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
<!-- ## Named Routes -->
## Named Routes

<!-- You may specify a name for a given page's route using the `name` function: -->
특정 페이지 라우트에 이름을 부여하고 싶다면, `name` 함수를 사용하면 됩니다.

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

<!-- Just like Laravel's named routes, you may use the `route` function to generate URLs to Folio pages that have been assigned a name: -->
Laravel의 네임드 라우트와 마찬가지로, `route` 함수를 사용해 이름이 지정된 Folio 페이지로의 URL을 손쉽게 생성할 수 있습니다.

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

<!-- If the page has parameters, you may simply pass their values to the `route` function: -->
페이지에 파라미터가 필요하다면, `route` 함수에 그 값을 넘기면 됩니다.

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
<!-- ## Middleware -->
## Middleware

<!-- You can apply middleware to a specific page by invoking the `middleware` function within the page's template: -->
특정 페이지에만 미들웨어를 적용하려면, 해당 페이지의 템플릿 내부에서 `middleware` 함수를 호출하세요.

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>
```

<!-- Or, to assign middleware to a group of pages, you may chain the `middleware` method after invoking the `Folio::path` method. -->
또한 다수의 페이지에 미들웨어를 적용하려면, `Folio::path` 메서드 이후에 `middleware` 메서드를 체이닝해서 사용할 수도 있습니다.

<!-- To specify which pages the middleware should be applied to, the array of middleware may be keyed using the corresponding URL patterns of the pages they should be applied to. The `*` character may be utilized as a wildcard character: -->
어떤 페이지에 어떤 미들웨어를 적용할 지를 URL 패턴별로 배열의 키로 지정할 수 있으며, `*`는 와일드카드로 사용됩니다.

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

<!-- You may include closures in the array of middleware to define inline, anonymous middleware: -->
미들웨어 배열에 클로저를 포함시켜, 인라인(익명) 미들웨어를 지정할 수도 있습니다.

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
<!-- ## Route Caching -->
## Route Caching

<!-- When using Folio, you should always take advantage of [Laravel's route caching capabilities](/docs/11.x/routing#route-caching). Folio listens for the `route:cache` Artisan command to ensure that Folio page definitions and route names are properly cached for maximum performance. -->
Folio를 사용할 때는 [Laravel's route caching capabilities](/docs/11.x/routing#route-caching)을 꼭 활용해야 합니다. Folio는 `route:cache` 아티즌 명령어를 감지하여, Folio 페이지 정의와 라우트 이름이 최대한 빠르게 동작할 수 있도록 제대로 캐싱됩니다.