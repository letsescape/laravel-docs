# Laravel Folio (Laravel Folio)

- [Introduction](#introduction)
- [Installation](#installation)
    - [ページパス/URI](#page-paths-uris)
    - [サブドメインルーティング](#subdomain-routing)
- [ルートの作成](#creating-routes)
    - [ネストされたルート](#nested-routes)
    - [インデックスルート](#index-routes)
- [ルートパラメータ](#route-parameters)
- [ルートモデルバインディング](#route-model-binding)
    - [ソフト削除されたモデル](#soft-deleted-models)
- [レンダリングフック](#render-hooks)
- [名前付きルート](#named-routes)
- [Middleware](#middleware)
- [ルートキャッシュ](#route-caching)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Folio](https://github.com/laravel/folio) は、Laravel アプリケーションでのルーティングを簡素化するように設計された強力なページベースのルーターです。 Laravel Folio を使用すると、アプリケーションの `resources/views/pages` ディレクトリ内に Blade テンプレートを作成するのと同じくらい簡単にルートを生成できます。

たとえば、`/greeting` URL でアクセスできるページを作成するには、アプリケーションの `resources/views/pages` ディレクトリに `greeting.blade.php` ファイルを作成するだけです。

```php
<div>
    Hello World
</div>
```

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Folio をプロジェクトにインストールします。

```bash
composer require laravel/folio
```

Folio をインストールした後、`folio:install` Artisan コマンドを実行すると、Folio のサービスプロバイダがアプリケーションにインストールされます。このサービスプロバイダは、Folio がルート/ページを検索するディレクトリを登録します。

```bash
php artisan folio:install
```

<a name="page-paths-uris"></a>
### ページパス/URI

デフォルトでは、Folio はアプリケーションの `resources/views/pages` ディレクトリからページを提供しますが、これらのディレクトリは Folio サービスプロバイダの `boot` メソッドでカスタマイズできます。

たとえば、同じ Laravel アプリケーションで複数の Folio パスを指定すると便利な場合があります。アプリケーションの「管理」領域用に Folio ページの別のディレクトリを用意し、アプリケーションの残りのページには別のディレクトリを使用したい場合があります。

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
### サブドメインルーティング

受信リクエストのサブドメインに基づいてページにルーティングすることもできます。たとえば、`admin.example.com` からのリクエストを、残りの Folio ページとは異なるページ ディレクトリにルーティングしたい場合があります。これを行うには、`Folio::path` メソッドを呼び出した後に `domain` メソッドを呼び出します。

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));
```

`domain` メソッドを使用すると、ドメインまたはサブドメインの一部をパラメータとしてキャプチャすることもできます。これらのパラメータはページ テンプレートに挿入されます。

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));
```

<a name="creating-routes"></a>
## ルートの作成 (Creating Routes)

Folio がマウントされたディレクトリのいずれかに Blade テンプレートを配置することで、Folio ルートを作成できます。デフォルトでは、Folio は `resources/views/pages` ディレクトリをマウントしますが、これらのディレクトリは Folio サービスプロバイダの `boot` メソッドでカスタマイズできます。

Blade テンプレートを Folio にマウントされたディレクトリに配置すると、ブラウザ経由ですぐにアクセスできます。たとえば、`pages/schedule.blade.php` に配置されたページは、ブラウザの `http://example.com/schedule` でアクセスされる可能性があります。

すべての Folio ページ/ルートのリストをすばやく表示するには、`folio:list` Artisan コマンドを呼び出します。

```bash
php artisan folio:list
```

<a name="nested-routes"></a>
### ネストされたルート

Folio のディレクトリの 1 つに 1 つ以上のディレクトリを作成することで、ネストされたルートを作成できます。たとえば、`/user/profile` 経由でアクセスできるページを作成するには、`pages/user` ディレクトリ内に `profile.blade.php` テンプレートを作成します。

```bash
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile
```

<a name="index-routes"></a>
### インデックスルート

場合によっては、特定のページをディレクトリの「インデックス」にしたい場合があります。 Folio ディレクトリ内に `index.blade.php` テンプレートを配置すると、そのディレクトリのルートへのリクエストはすべてそのページにルーティングされます。

```bash
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users
```

<a name="route-parameters"></a>
## ルートパラメータ (Route Parameters)

多くの場合、受信リクエストの URL のセグメントをページに挿入して、それらを操作できるようにする必要があります。たとえば、プロフィールが表示されているユーザーの「ID」にアクセスする必要がある場合があります。これを実現するには、ページのファイル名のセグメントを角かっこでカプセル化します。

```bash
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1
```

キャプチャされたセグメントは、Blade テンプレート内の変数としてアクセスできます。

```html
<div>
    User {{ $id }}
</div>
```

複数のセグメントをキャプチャするには、カプセル化されたセグメントの前に 3 つのドット `...` を付けることができます。

```bash
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3
```

複数のセグメントをキャプチャする場合、キャプチャされたセグメントは配列としてページに挿入されます。

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>
```

<a name="route-model-binding"></a>
## ルートモデルバインディング (Route Model Binding)

ページ テンプレートのファイル名のワイルドカード セグメントがアプリケーションの Eloquent モデルの 1 つに対応する場合、Folio は自動的に Laravel のルート モデル バインディング機能を利用し、解決されたモデル インスタンスをページに挿入しようとします。

```bash
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1
```

キャプチャされたモデルは、Blade テンプレート内の変数としてアクセスできます。モデルの変数名は「キャメルケース」に変換されます。

```html
<div>
    User {{ $user->id }}
</div>
```

#### キーのカスタマイズ

場合によっては、`id` 以外の列を使用してバインドされた Eloquent モデルを解決したい場合があります。これを行うには、ページのファイル名で列を指定できます。たとえば、ファイル名 `[Post:slug].blade.php` のページは、`id` 列ではなく `slug` 列を介してバインドされたモデルを解決しようとします。

Windows では、`-` を使用してモデル名をキーから区切る必要があります: `[Post-slug].blade.php`。

#### モデルの場所

デフォルトでは、Folio はアプリケーションの `app/Models` ディレクトリ内でモデルを検索します。ただし、必要に応じて、テンプレートのファイル名に完全修飾モデル クラス名を指定できます。

```bash
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1
```

<a name="soft-deleted-models"></a>
### ソフト削除されたモデル

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
## レンダリングフック (Render Hooks)

デフォルトでは、Folio は受信リクエストへの応答としてページの Blade テンプレートのコンテンツを返します。ただし、ページのテンプレート内で `render` 関数を呼び出すことで、応答をカスタマイズできます。

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
## 名前付きルート (Named Routes)

`name` 関数を使用して、特定のページのルートの名前を指定できます。

```php
<?php

use function Laravel\Folio\name;

name('users.index');
```

Laravel の名前付きルートと同様に、`route` 関数を使用して、名前が割り当てられた Folio ページへの URL を生成できます。

```php
<a href="{{ route('users.index') }}">
    All Users
</a>
```

ページにパラメータがある場合は、その値を `route` 関数に渡すだけで済みます。

```php
route('users.show', ['user' => $user]);
```

<a name="middleware"></a>
## ミドルウェア (Middleware)

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

または、ページのグループにミドルウェアを割り当てるには、`Folio::path` メソッドを呼び出した後に `middleware` メソッドをチェーンすることもできます。

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
## ルートキャッシュ (Route Caching)

Folio を使用する場合は、常に [Laravelのルートキャッシュ機能](/docs/{{version}}/routing#route-caching) を活用する必要があります。 Folio は、`route:cache` Artisan コマンドをリッスンして、最大限のパフォーマンスを得るために Folio ページ定義とルート名が適切にキャッシュされていることを確認します。

