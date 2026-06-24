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
[Laravel Folio](https://github.com/laravel/folio) は、Laravel アプリケーションでのルーティングを簡素化するように設計された強力なページベースのルーターです。 Laravel Folio を使用すると、アプリケーションの `resources/views/pages` ディレクトリ内に Blade テンプレートを作成するのと同じくらい簡単にルートを生成できます。

<!-- For example, to create a page that is accessible at the `/greeting` URL, just create a `greeting.blade.php` file in your application's `resources/views/pages` directory: -->
たとえば、`/greeting` URL でアクセスできるページを作成するには、アプリケーションの `resources/views/pages` ディレクトリに `greeting.blade.php` ファイルを作成するだけです。

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Folio into your project using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Folio をプロジェクトにインストールします。

```shell
composer require laravel/folio
```

<!-- After installing Folio, you may execute the `folio:install` Artisan command, which will install Folio's service provider into your application. This service provider registers the directory where Folio will search for routes / pages: -->
Folio をインストールした後、`folio:install` Artisan コマンドを実行すると、Folio のサービスプロバイダがアプリケーションにインストールされます。このサービスプロバイダは、Folio がルート/ページを検索するディレクトリを登録します。

```shell
php artisan folio:install
```

<a name="page-paths-uris"></a>
<!-- ### Page Paths / URIs -->
### Page Paths / URIs

<!-- By default, Folio serves pages from your application's `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method. -->
デフォルトでは、Folio はアプリケーションの `resources/views/pages` ディレクトリからページを提供しますが、これらのディレクトリは Folio サービスプロバイダの `boot` メソッドでカスタマイズできます。

<!-- For example, sometimes it may be convenient to specify multiple Folio paths in the same Laravel application. You may wish to have a separate directory of Folio pages for your application's "admin" area, while using another directory for the rest of your application's pages. -->
たとえば、同じ Laravel アプリケーションで複数の Folio パスを指定すると便利な場合があります。アプリケーションの「管理」領域用に Folio ページの別のディレクトリを用意し、アプリケーションの残りのページには別のディレクトリを使用したい場合があります。

<!-- You may accomplish this using the `Folio::path` and `Folio::uri` methods. The `path` method registers a directory that Folio will scan for pages when routing incoming HTTP requests, while the `uri` method specifies the "base URI" for that directory of pages: -->
これは、`Folio::path` メソッドと `Folio::uri` メソッドを使用して実行できます。 `path` メソッドは、受信 HTTP リクエストをルーティングするときに Folio がページをスキャンするディレクトリを登録します。一方、`uri` メソッドは、そのページのディレクトリの「ベース URI」を指定します。

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
受信リクエストのサブドメインに基づいてページにルーティングすることもできます。たとえば、`admin.example.com` からのリクエストを、残りの Folio ページとは異なるページ ディレクトリにルーティングしたい場合があります。これを行うには、`Folio::path` メソッドを呼び出した後に `domain` メソッドを呼び出します。

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

<!-- The `domain` method also allows you to capture parts of the domain or subdomain as parameters. These parameters will be injected into your page template: -->
`domain` メソッドを使用すると、ドメインまたはサブドメインの一部をパラメータとしてキャプチャすることもできます。これらのパラメータはページ テンプレートに挿入されます。

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
<!-- ## Creating Routes -->
## Creating Routes

<!-- You may create a Folio route by placing a Blade template in any of your Folio mounted directories. By default, Folio mounts the `resources/views/pages` directory, but you may customize these directories in your Folio service provider's `boot` method. -->
Folio がマウントされたディレクトリのいずれかに Blade テンプレートを配置することで、Folio ルートを作成できます。デフォルトでは、Folio は `resources/views/pages` ディレクトリをマウントしますが、これらのディレクトリは Folio サービスプロバイダの `boot` メソッドでカスタマイズできます。

<!-- Once a Blade template has been placed in a Folio mounted directory, you may immediately access it via your browser. For example, a page placed in `pages/schedule.blade.php` may be accessed in your browser at `http://example.com/schedule`. -->
Blade テンプレートを Folio にマウントされたディレクトリに配置すると、ブラウザ経由ですぐにアクセスできます。たとえば、`pages/schedule.blade.php` に配置されたページは、ブラウザの `http://example.com/schedule` でアクセスされる可能性があります。

<!-- To quickly view a list of all of your Folio pages / routes, you may invoke the `folio:list` Artisan command: -->
すべての Folio ページ/ルートのリストをすばやく表示するには、`folio:list` Artisan コマンドを呼び出します。

```shell
php artisan folio:list
```

<a name="nested-routes"></a>
<!-- ### Nested Routes -->
### Nested Routes

<!-- You may create a nested route by creating one or more directories within one of Folio's directories. For instance, to create a page that is accessible via `/user/profile`, create a `profile.blade.php` template within the `pages/user` directory: -->
Folio のディレクトリの 1 つに 1 つ以上のディレクトリを作成することで、ネストされたルートを作成できます。たとえば、`/user/profile` 経由でアクセスできるページを作成するには、`pages/user` ディレクトリ内に `profile.blade.php` テンプレートを作成します。

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
<!-- ### Index Routes -->
### Index Routes

<!-- Sometimes, you may wish to make a given page the "index" of a directory. By placing an `index.blade.php` template within a Folio directory, any requests to the root of that directory will be routed to that page: -->
場合によっては、特定のページをディレクトリの「インデックス」にしたい場合があります。 Folio ディレクトリ内に `index.blade.php` テンプレートを配置すると、そのディレクトリのルートへのリクエストはすべてそのページにルーティングされます。

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
<!-- ## Route Parameters -->
## Route Parameters

<!-- Often, you will need to have segments of the incoming request's URL injected into your page so that you can interact with them. For example, you may need to access the "ID" of the user whose profile is being displayed. To accomplish this, you may encapsulate a segment of the page's filename in square brackets: -->
多くの場合、受信リクエストの URL のセグメントをページに挿入して、それらを操作できるようにする必要があります。たとえば、プロフィールが表示されているユーザーの「ID」にアクセスする必要がある場合があります。これを実現するには、ページのファイル名のセグメントを角かっこでカプセル化します。

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

<!-- Captured segments can be accessed as variables within your Blade template: -->
キャプチャされたセグメントは、Blade テンプレート内の変数としてアクセスできます。

```html
<div>
    User {{ $id }}
</div>
```

<!-- To capture multiple segments, you can prefix the encapsulated segment with three dots `...`: -->
複数のセグメントをキャプチャするには、カプセル化されたセグメントの前に 3 つのドット `...` を付けることができます。

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

<!-- When capturing multiple segments, the captured segments will be injected into the page as an array: -->
複数のセグメントをキャプチャする場合、キャプチャされたセグメントは配列としてページに挿入されます。

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
ページ テンプレートのファイル名のワイルドカード セグメントがアプリケーションの Eloquent モデルの 1 つに対応する場合、Folio は自動的に Laravel のルート モデル バインディング機能を利用し、解決されたモデル インスタンスをページに挿入しようとします。

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

<!-- Captured models can be accessed as variables within your Blade template. The model's variable name will be converted to "camel case": -->
キャプチャされたモデルは、Blade テンプレート内の変数としてアクセスできます。モデルの変数名は「キャメルケース」に変換されます。

```html
<div>
    User {{ $user->id }}
</div>
```

<!-- #### Customizing the Key -->
#### Customizing the Key

<!-- Sometimes you may wish to resolve bound Eloquent models using a column other than `id`. To do so, you may specify the column in the page's filename. For example, a page with the filename `[Post:slug].blade.php` will attempt to resolve the bound model via the `slug` column instead of the `id` column. -->
場合によっては、`id` 以外の列を使用してバインドされた Eloquent モデルを解決したい場合があります。これを行うには、ページのファイル名で列を指定できます。たとえば、ファイル名 `[Post:slug].blade.php` のページは、`id` 列ではなく `slug` 列を介してバインドされたモデルを解決しようとします。

<!-- On Windows, you should use `-` to separate the model name from the key: `[Post-slug].blade.php`. -->
Windows では、`-` を使用してモデル名をキーから区切る必要があります: `[Post-slug].blade.php`。

<!-- #### Model Location -->
#### Model Location

<!-- By default, Folio will search for your model within your application's `app/Models` directory. However, if needed, you may specify the fully-qualified model class name in your template's filename: -->
デフォルトでは、Folio はアプリケーションの `app/Models` ディレクトリ内でモデルを検索します。ただし、必要に応じて、テンプレートのファイル名に完全修飾モデル クラス名を指定できます。

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
<!-- ### Soft Deleted Models -->
### Soft Deleted Models

<!-- By default, models that have been soft deleted are not retrieved when resolving implicit model bindings. However, if you wish, you can instruct Folio to retrieve soft deleted models by invoking the `withTrashed` function within the page's template: -->
デフォルトでは、論理的に削除されたモデルは、暗黙的なモデル バインディングを解決するときに取得されません。ただし、必要に応じて、ページのテンプレート内で `withTrashed` 関数を呼び出して、論理的に削除されたモデルを取得するように Folio に指示できます。

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
デフォルトでは、Folio は受信リクエストへの応答としてページの Blade テンプレートのコンテンツを返します。ただし、ページのテンプレート内で `render` 関数を呼び出すことで、応答をカスタマイズできます。

<!-- The `render` function accepts a closure which will receive the `View` instance being rendered by Folio, allowing you to add additional data to the view or customize the entire response. In addition to receiving the `View` instance, any additional route parameters or model bindings will also be provided to the `render` closure: -->
`render` 関数は、Folio によってレンダリングされる `View` インスタンスを受け取るクロージャーを受け入れ、ビューにデータを追加したり、応答全体をカスタマイズしたりできます。 `View` インスタンスの受信に加えて、追加のルート パラメーターまたはモデル バインディングも `render` クロージャに提供されます。

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
`name` 関数を使用して、特定のページのルートの名前を指定できます。

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

<!-- Just like Laravel's named routes, you may use the `route` function to generate URLs to Folio pages that have been assigned a name: -->
Laravel の名前付きルートと同様に、`route` 関数を使用して、名前が割り当てられた Folio ページへの URL を生成できます。

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

<!-- If the page has parameters, you may simply pass their values to the `route` function: -->
ページにパラメータがある場合は、その値を `route` 関数に渡すだけで済みます。

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
<!-- ## Middleware -->
## Middleware

<!-- You can apply middleware to a specific page by invoking the `middleware` function within the page's template: -->
ページのテンプレート内で `middleware` 関数を呼び出すことで、特定のページにミドルウェアを適用できます。

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
または、ページのグループにミドルウェアを割り当てるには、`Folio::path` メソッドを呼び出した後に `middleware` メソッドをチェーンすることもできます。

<!-- To specify which pages the middleware should be applied to, the array of middleware may be keyed using the corresponding URL patterns of the pages they should be applied to. The `*` character may be utilized as a wildcard character: -->
ミドルウェアを適用するページを指定するには、ミドルウェアを適用するページの対応する URL パターンを使用して、ミドルウェアの配列をキー設定します。 `*` 文字はワイルドカード文字として使用できます。

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
ミドルウェアの配列にクロージャを含めて、インラインの匿名ミドルウェアを定義できます。

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

<!-- When using Folio, you should always take advantage of [Laravel's route caching capabilities](/docs/master/routing#route-caching). Folio listens for the `route:cache` Artisan command to ensure that Folio page definitions and route names are properly cached for maximum performance. -->
Folio を使用する場合は、常に [Laravel's route caching capabilities](/docs/master/routing#route-caching) を活用する必要があります。 Folio は、`route:cache` Artisan コマンドをリッスンして、最大限のパフォーマンスを得るために Folio ページ定義とルート名が適切にキャッシュされていることを確認します。

