# データベース: ページネーション (Database: Pagination)

- [Introduction](#introduction)
- [基本的な使い方](#basic-usage)
    - [クエリビルダ結果のページ分割](#paginating-query-builder-results)
    - [Eloquent の結果のページネーション](#paginating-eloquent-results)
    - [カーソルのページネーション](#cursor-pagination)
    - [ページネータを手動で作成する](#manually-creating-a-paginator)
    - [ページネーション URL のカスタマイズ](#customizing-pagination-urls)
- [ページネーション結果の表示](#displaying-pagination-results)
    - [ページネーションリンクウィンドウの調整](#adjusting-the-pagination-link-window)
    - [結果を JSON に変換する](#converting-results-to-json)
- [ページネーションビューのカスタマイズ](#customizing-the-pagination-view)
    - [ブートストラップの使用](#using-bootstrap)
- [Paginator および LengthAwarePaginator インスタンス メソッド](#paginator-instance-methods)
- [カーソル ページネータ インスタンス メソッド](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 導入 (Introduction)

他のフレームワークでは、ページネーションは非常に面倒な場合があります。 Laravel のページネーションへのアプローチが新風となることを願っています。 Laravel のページネータは [クエリビルダ](/docs/{{version}}/queries) および [Eloquent ORM](/docs/{{version}}/eloquent) と統合されており、設定なしでデータベース レコードの便利で使いやすいページネーションを提供します。

デフォルトでは、ページネータによって生成された HTML は [Tailwind CSS フレームワーク](https://tailwindcss.com/) と互換性があります。ただし、Bootstrap ページネーションのサポートも利用できます。

<a name="tailwind"></a>
#### Tailwind

Tailwind 4.x で Laravel のデフォルトの Tailwind ページネーション ビューを使用している場合、アプリケーションの `resources/css/app.css` ファイルはすでに `@source` Laravel のページネーション ビューに適切に設定されています。

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```

<a name="basic-usage"></a>
## 基本的な使い方 (Basic Usage)

<a name="paginating-query-builder-results"></a>
### クエリビルダ結果のページ分割

アイテムをページ分割するにはいくつかの方法があります。最も簡単な方法は、[クエリビルダ](/docs/{{version}}/queries) または [Eloquent クエリ](/docs/{{version}}/eloquent) で `paginate` メソッドを使用することです。 `paginate` メソッドは、ユーザーが表示している現在のページに基づいてクエリの「制限」と「オフセット」の設定を自動的に処理します。デフォルトでは、現在のページは、HTTP リクエストの `page` クエリ文字列引数の値によって検出されます。この値は Laravel によって自動的に検出され、ページネータによって生成されたリンクにも自動的に挿入されます。

この例では、`paginate` メソッドに渡される唯一の引数は、「ページごとに」表示する項目の数です。この場合、ページごとに `15` アイテムを表示することを指定しましょう。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```

<a name="simple-pagination"></a>
#### 単純なページネーション

`paginate` メソッドは、データベースからレコードを取得する前に、クエリに一致するレコードの総数をカウントします。これは、ページネータがレコードの合計ページ数を知るために行われます。ただし、アプリケーションの UI に合計ページ数を表示する予定がない場合は、レコード数クエリは不要です。

したがって、アプリケーションの UI に単純な「次へ」リンクと「前へ」リンクのみを表示する必要がある場合は、`simplePaginate` メソッドを使用して単一の効率的なクエリを実行できます。

```php
$users = DB::table('users')->simplePaginate(15);
```

<a name="paginating-eloquent-results"></a>
### Eloquent の結果のページネーション

[Eloquent](/docs/{{version}}/eloquent) クエリをページ分割することもできます。この例では、`App\Models\User` モデルをページ分割し、1 ページあたり 15 レコードを表示する予定であることを示します。ご覧のとおり、構文はページ分割クエリビルダの結果とほぼ同じです。

```php
use App\Models\User;

$users = User::paginate(15);
```

もちろん、クエリに `where` 句などの他の制約を設定した後に、`paginate` メソッドを呼び出すこともできます。

```php
$users = User::where('votes', '>', 100)->paginate(15);
```

Eloquent モデルをページ分割するときに、`simplePaginate` メソッドを使用することもできます。

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```

同様に、`cursorPaginate` メソッドを使用して、Eloquent モデルをカーソルでページネーションすることもできます。

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```

<a name="multiple-paginator-instances-per-page"></a>
#### ページごとに複数のページネータ インスタンス

場合によっては、アプリケーションによってレンダリングされる 1 つの画面上に 2 つの別個のページネータをレンダリングする必要がある場合があります。ただし、両方のページネータ インスタンスが `page` クエリ文字列パラメータを使用して現在のページを保存する場合、2 つのページネータは競合します。この競合を解決するには、`paginate`、`simplePaginate`、および `cursorPaginate` メソッドに提供される 3 番目の引数を介して、ページネータの現在のページを保存するために使用するクエリ文字列パラメーターの名前を渡すことができます。

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```

<a name="cursor-pagination"></a>
### カーソルのページネーション

`paginate` と `simplePaginate` は SQL の「offset」句を使用してクエリを作成しますが、カーソルのページネーションは、クエリに含まれる順序付けされた列の値を比較する「where」句を構築することによって機能し、Laravel のすべてのページネーション メソッドの中で最も効率的なデータベース パフォーマンスを提供します。このページネーション方法は、大規模なデータセットや「無限」スクロールのユーザー インターフェイスに特に適しています。

ページネーションによって生成された URL のクエリ文字列にページ番号が含まれるオフセット ベースのページネーションとは異なり、カーソル ベースのページネーションでは、クエリ文字列に「カーソル」文字列が配置されます。カーソルは、次のページ分割されたクエリがページ分割を開始する位置とページ分割の方向を含むエンコードされた文字列です。

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```

クエリビルダが提供する `cursorPaginate` メソッドを使用して、カーソル ベースのページネータ インスタンスを作成できます。このメソッドは、`Illuminate\Pagination\CursorPaginator` のインスタンスを返します。

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```

カーソル ページネータ インスタンスを取得したら、`paginate` および `simplePaginate` メソッドを使用するときに通常行うのと同じように、[ページネーションの結果を表示する](#displaying-pagination-results) を実行できます。カーソル ページネータによって提供されるインスタンス メソッドの詳細については、[カーソル ページネータ インスタンス メソッドのドキュメント](#cursor-paginator-instance-methods) を参照してください。

> [!WARNING]
> カーソルのページネーションを利用するには、クエリに「order by」句が含まれている必要があります。さらに、クエリの順序付けに使用される列は、ページ分割するテーブルに属している必要があります。

<a name="cursor-vs-offset-pagination"></a>
#### カーソルとオフセットのページネーション

オフセット ページネーションとカーソル ページネーションの違いを説明するために、いくつかの SQL クエリの例を見てみましょう。次のクエリはどちらも、`id` で順序付けされた `users` テーブルの結果の「2 ページ目」を表示します。

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

カーソル ページネーション クエリには、オフセット ページネーションに比べて次の利点があります。

- 大規模なデータセットの場合、「order by」列にインデックスが付けられている場合、カーソルのページネーションのパフォーマンスが向上します。これは、「offset」句が以前に一致したすべてのデータをスキャンするためです。
- 書き込みが頻繁に行われるデータセットの場合、ユーザーが現在表示しているページに最近結果が追加または削除された場合、オフセット ページネーションによってレコードがスキップされたり、重複が表示されたりする可能性があります。

ただし、カーソルのページネーションには次の制限があります。

- `simplePaginate` と同様、カーソル ページネーションは「次へ」と「前へ」リンクを表示するためにのみ使用でき、ページ番号付きのリンクの生成はサポートされていません。
- 少なくとも 1 つの一意の列、または一意の列の組み合わせに基づいて順序付けする必要があります。 `null` 値を含む列はサポートされていません。
- 「order by」句のクエリ式は、エイリアス化され、「select」句にも追加されている場合にのみサポートされます。
- パラメータを含むクエリ式はサポートされていません。

<a name="manually-creating-a-paginator"></a>
### ページネータを手動で作成する

場合によっては、ページネーション インスタンスを手動で作成し、メモリ内にすでにある項目の配列を渡したい場合があります。これを行うには、ニーズに応じて、`Illuminate\Pagination\Paginator`、`Illuminate\Pagination\LengthAwarePaginator`、または `Illuminate\Pagination\CursorPaginator` インスタンスを作成します。

`Paginator` クラスと `CursorPaginator` クラスは、結果セット内の項目の合計数を知る必要はありません。ただし、このため、これらのクラスには最後のページのインデックスを取得するメソッドがありません。 `LengthAwarePaginator` は、`Paginator` とほぼ同じ引数を受け入れます。ただし、結果セット内の項目の総数をカウントする必要があります。

つまり、`Paginator` はクエリビルダの `simplePaginate` メソッドに対応し、`CursorPaginator` は `cursorPaginate` メソッドに対応し、`LengthAwarePaginator` は `paginate` メソッドに対応します。

> [!WARNING]
> ページネータ インスタンスを手動で作成する場合は、ページネータに渡す結果の配列を手動で「スライス」する必要があります。これを行う方法がわからない場合は、[array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 関数を確認してください。

<a name="customizing-pagination-urls"></a>
### ページネーション URL のカスタマイズ

デフォルトでは、ページネータによって生成されたリンクは現在のリクエストの URI と一致します。ただし、ページネータの `withPath` メソッドを使用すると、リンクの生成時にページネータによって使用される URI をカスタマイズできます。たとえば、ページネータで `http://example.com/admin/users?page=N` のようなリンクを生成したい場合は、`/admin/users` を `withPath` メソッドに渡す必要があります。

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```

<a name="appending-query-string-values"></a>
#### クエリ文字列値の追加

`appends` メソッドを使用して、ページ分割リンクのクエリ文字列に追加できます。たとえば、各ページネーション リンクに `sort=votes` を追加するには、`appends` に対して次の呼び出しを行う必要があります。

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```

現在のリクエストのすべてのクエリ文字列値をページネーション リンクに追加したい場合は、`withQueryString` メソッドを使用できます。

```php
$users = User::paginate(15)->withQueryString();
```

<a name="appending-hash-fragments"></a>
#### ハッシュフラグメントの追加

ページネータによって生成された URL に「ハッシュ フラグメント」を追加する必要がある場合は、`fragment` メソッドを使用できます。たとえば、各ページネーション リンクの末尾に `#users` を追加するには、次のように `fragment` メソッドを呼び出す必要があります。

```php
$users = User::paginate(15)->fragment('users');
```

<a name="displaying-pagination-results"></a>
## ページネーション結果の表示 (Displaying Pagination Results)

`paginate` メソッドを呼び出すと、`Illuminate\Pagination\LengthAwarePaginator` のインスタンスを受け取りますが、`simplePaginate` メソッドを呼び出すと、`Illuminate\Pagination\Paginator` のインスタンスを返します。最後に、`cursorPaginate` メソッドを呼び出すと、`Illuminate\Pagination\CursorPaginator` のインスタンスが返されます。

これらのオブジェクトは、結果セットを記述するいくつかのメソッドを提供します。これらのヘルパ メソッドに加えて、ページネータ インスタンスはイテレータであり、配列としてループすることができます。したがって、結果を取得したら、[Blade](/docs/{{version}}/blade) を使用して結果を表示し、ページ リンクをレンダリングできます。

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```

`links` メソッドは、結果セット内の残りのページへのリンクをレンダリングします。これらの各リンクには、適切な `page` クエリ文字列変数がすでに含まれています。 `links` メソッドによって生成された HTML は、[Tailwind CSS フレームワーク](https://tailwindcss.com) と互換性があることに注意してください。

<a name="adjusting-the-pagination-link-window"></a>
### ページネーションリンクウィンドウの調整

ページネータにページネーション リンクが表示されると、現在のページ番号に加えて、現在のページの前後 3 ページのリンクも表示されます。 `onEachSide` メソッドを使用すると、ページネータによって生成されたリンクの中央のスライディング ウィンドウ内の現在のページの両側に表示される追加リンクの数を制御できます。

```blade
{{ $users->onEachSide(5)->links() }}
```

<a name="converting-results-to-json"></a>
### 結果を JSON に変換する

Laravel のページネータ クラスは、`Illuminate\Contracts\Support\Jsonable` インターフェイス コントラクトを実装し、`toJson` メソッドを公開するため、ページネーションの結果を JSON に変換するのは非常に簡単です。ルートまたはコントローラ アクションからページネータ インスタンスを返すことによって、ページネータ インスタンスを JSON に変換することもできます。

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```

ページネータからの JSON には、`total`、`current_page`、`last_page` などのメタ情報が含まれます。結果レコードは、JSON 配列の `data` キーを介して利用できます。以下は、ルートからページネータ インスタンスを返すことによって作成された JSON の例です。

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```

<a name="customizing-the-pagination-view"></a>
## ページネーションビューのカスタマイズ (Customizing the Pagination View)

デフォルトでは、ページネーション リンクを表示するためにレンダリングされるビューは、[Tailwind CSS](https://tailwindcss.com) フレームワークと互換性があります。ただし、Tailwind を使用していない場合は、これらのリンクをレンダリングする独自のビューを自由に定義できます。ページネータ インスタンスで `links` メソッドを呼び出す場合、最初の引数としてビュー名をメソッドに渡すことができます。

```blade
{{ $paginator->links('view.name') }}

<!-- Passing additional data to the view... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```

ただし、ページネーション ビューをカスタマイズする最も簡単な方法は、`vendor:publish` コマンドを使用してページネーション ビューを `resources/views/vendor` ディレクトリにエクスポートすることです。

```shell
php artisan vendor:publish --tag=laravel-pagination
```

このコマンドは、アプリケーションの `resources/views/vendor/pagination` ディレクトリにビューを配置します。このディレクトリ内の `tailwind.blade.php` ファイルは、デフォルトのページネーション ビューに対応します。このファイルを編集して、ページネーション HTML を変更できます。

別のファイルをデフォルトのページネーション ビューとして指定したい場合は、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内で、ページネータの `defaultView` メソッドと `defaultSimpleView` メソッドを呼び出すことができます。

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```

<a name="using-bootstrap"></a>
### ブートストラップの使用

Laravel には、[ブートストラップCSS](https://getbootstrap.com/) を使用して構築されたページ分割ビューが含まれています。デフォルトの Tailwind ビューの代わりにこれらのビューを使用するには、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内で、ページネータの `useBootstrapFour` メソッドまたは `useBootstrapFive` メソッドを呼び出すことができます。

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## Paginator / LengthAwarePaginator インスタンス メソッド (Paginator / LengthAwarePaginator Instance Methods)

各ページネータ インスタンスは、次のメソッドを介して追加のページネーション情報を提供します。

<div class="overflow-auto">

| 方法                                  | 説明                                                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `$paginator->count()`                   | 現在のページの項目数を取得します。                                                                |
| `$paginator->currentPage()`             | 現在のページ番号を取得します。                                                                                 |
| `$paginator->firstItem()`               | 結果の最初の項目の結果番号を取得します。                                                      |
| `$paginator->getOptions()`              | ページネータのオプションを取得します。                                                                                   |
| `$paginator->getUrlRange($start, $end)` | 一連のページネーション URL を作成します。                                                                           |
| `$paginator->hasPages()`                | 複数のページに分割するのに十分な項目があるかどうかを判断します。                                            |
| `$paginator->hasMorePages()`            | データ ストアにさらにアイテムがあるかどうかを確認します。                                                         |
| `$paginator->items()`                   | 現在のページのアイテムを取得します。                                                                          |
| `$paginator->lastItem()`                | 結果の最後の項目の結果番号を取得します。                                                       |
| `$paginator->lastPage()`                | 最後に利用可能なページのページ番号を取得します。 (`simplePaginate` を使用する場合は使用できません)。                 |
| `$paginator->nextPageUrl()`             | 次のページの URL を取得します。                                                                               |
| `$paginator->onFirstPage()`             | ページネータが最初のページにあるかどうかを確認します。                                                             |
| `$paginator->onLastPage()`              | ページネータが最後のページにあるかどうかを確認します。                                                              |
| `$paginator->perPage()`                 | ページごとに表示される項目の数。                                                                    |
| `$paginator->previousPageUrl()`         | 前のページの URL を取得します。                                                                           |
| `$paginator->total()`                   | データ ストア内の一致するアイテムの総数を確認します。 (`simplePaginate` を使用する場合は使用できません)。 |
| `$paginator->url($page)`                | 指定されたページ番号の URL を取得します。                                                                         |
| `$paginator->getPageName()`             | ページの保存に使用されるクエリ文字列変数を取得します。                                                        |
| `$paginator->setPageName($name)`        | ページの保存に使用されるクエリ文字列変数を設定します。                                                        |
| `$paginator->through($callback)`        | コールバックを使用して各項目を変換します。                                                                        |

</div>

<a name="cursor-paginator-instance-methods"></a>
## カーソル ページネータ インスタンス メソッド (Cursor Paginator Instance Methods)

各カーソル ページネーション インスタンスは、次のメソッドを介して追加のページネーション情報を提供します。

<div class="overflow-auto">

| 方法                          | 説明                                                       |
| ------------------------------- | ----------------------------------------------------------------- |
| `$paginator->count()`           | 現在のページの項目数を取得します。                     |
| `$paginator->cursor()`          | 現在のカーソルインスタンスを取得します。                                  |
| `$paginator->getOptions()`      | ページネータのオプションを取得します。                                        |
| `$paginator->hasPages()`        | 複数のページに分割するのに十分な項目があるかどうかを判断します。 |
| `$paginator->hasMorePages()`    | データ ストアにさらにアイテムがあるかどうかを確認します。              |
| `$paginator->getCursorName()`   | カーソルを格納するために使用されるクエリ文字列変数を取得します。           |
| `$paginator->items()`           | 現在のページのアイテムを取得します。                               |
| `$paginator->nextCursor()`      | 次の項目セットのカーソル インスタンスを取得します。                |
| `$paginator->nextPageUrl()`     | 次のページの URL を取得します。                                    |
| `$paginator->onFirstPage()`     | ページネータが最初のページにあるかどうかを確認します。                  |
| `$paginator->onLastPage()`      | ページネータが最後のページにあるかどうかを確認します。                   |
| `$paginator->perPage()`         | ページごとに表示される項目の数。                         |
| `$paginator->previousCursor()`  | 前の項目セットのカーソル インスタンスを取得します。            |
| `$paginator->previousPageUrl()` | 前のページの URL を取得します。                                |
| `$paginator->setCursorName()`   | カーソルを格納するために使用されるクエリ文字列変数を設定します。           |
| `$paginator->url($cursor)`      | 指定されたカーソル インスタンスの URL を取得します。                          |

</div>

