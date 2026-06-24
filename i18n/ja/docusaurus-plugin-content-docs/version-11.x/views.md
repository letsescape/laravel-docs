<!-- # Views -->
# Views

- [Introduction](#introduction)
    - [Writing Views in React / Vue](#writing-views-in-react-or-vue)
- [Creating and Rendering Views](#creating-and-rendering-views)
    - [Nested View Directories](#nested-view-directories)
    - [Creating the First Available View](#creating-the-first-available-view)
    - [Determining if a View Exists](#determining-if-a-view-exists)
- [Passing Data to Views](#passing-data-to-views)
    - [Sharing Data With All Views](#sharing-data-with-all-views)
- [View Composers](#view-composers)
    - [View Creators](#view-creators)
- [Optimizing Views](#optimizing-views)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Of course, it's not practical to return entire HTML documents strings directly from your routes and controllers. Thankfully, views provide a convenient way to place all of our HTML in separate files. -->
もちろん、HTML ドキュメントの文字列全体をルートやコントローラから直接返すのは現実的ではありません。ありがたいことに、ビューはすべての HTML を個別のファイルに配置する便利な方法を提供します。

<!-- Views separate your controller / application logic from your presentation logic and are stored in the `resources/views` directory. When using Laravel, view templates are usually written using the [Blade templating language](/docs/11.x/blade). A simple view might look something like this: -->
ビューは、コントローラ/アプリケーション ロジックをプレゼンテーション ロジックから分離し、`resources/views` ディレクトリに保存されます。 Laravel を使用する場合、ビュー テンプレートは通常、[Blade templating language](/docs/11.x/blade) を使用して記述されます。単純なビューは次のようになります。

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

<!-- Since this view is stored at `resources/views/greeting.blade.php`, we may return it using the global `view` helper like so: -->
このビューは `resources/views/greeting.blade.php` に保存されているため、次のようにグローバル `view` ヘルパを使用してビューを返すことができます。

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

> [!NOTE]
> Blade テンプレートの作成方法に関する詳細情報をお探しですか?開始するには、[Blade documentation](/docs/11.x/blade) の全文を確認してください。

<a name="writing-views-in-react-or-vue"></a>
<!-- ### Writing Views in React / Vue -->
### Writing Views in React / Vue

<!-- Instead of writing their frontend templates in PHP via Blade, many developers have begun to prefer to write their templates using React or Vue. Laravel makes this painless thanks to [Inertia](https://inertiajs.com/), a library that makes it a cinch to tie your React / Vue frontend to your Laravel backend without the typical complexities of building an SPA. -->
多くの開発者は、Blade を介して PHP でフロントエンド テンプレートを作成する代わりに、React または Vue を使用してテンプレートを作成することを好み始めています。 Laravel では、SPA の構築によくある複雑さを必要とせずに、React / Vue フロントエンドを Laravel バックエンドに簡単に接続できるライブラリ [Inertia](https://inertiajs.com/) のおかげで、これを簡単に実行できます。

<!-- Our Breeze and Jetstream [starter kits](/docs/11.x/starter-kits) give you a great starting point for your next Laravel application powered by Inertia. In addition, the [Laravel Bootcamp](https://bootcamp.laravel.com) provides a full demonstration of building a Laravel application powered by Inertia, including examples in Vue and React. -->
Breeze と Jetstream [starter kits](/docs/11.x/starter-kits) は、Inertia を利用した次の Laravel アプリケーションの優れた出発点となります。さらに、[Laravel Bootcamp](https://bootcamp.laravel.com) は、Vue と React の例を含む、Inertia を利用した Laravel アプリケーションの構築に関する完全なデモンストレーションを提供します。

<a name="creating-and-rendering-views"></a>
<!-- ## Creating and Rendering Views -->
## Creating and Rendering Views

<!-- You may create a view by placing a file with the `.blade.php` extension in your application's `resources/views` directory or by using the `make:view` Artisan command: -->
アプリケーションの `resources/views` ディレクトリに `.blade.php` 拡張子を持つファイルを配置するか、`make:view` Artisan コマンドを使用して、ビューを作成できます。

```shell
php artisan make:view greeting
```

<!-- The `.blade.php` extension informs the framework that the file contains a [Blade template](/docs/11.x/blade). Blade templates contain HTML as well as Blade directives that allow you to easily echo values, create "if" statements, iterate over data, and more. -->
`.blade.php` 拡張子は、ファイルに [Blade template](/docs/11.x/blade) が含まれていることをフレームワークに通知します。 Blade テンプレートには、HTML と Blade ディレクティブが含まれており、値のエコー、「if」ステートメントの作成、データの反復などを簡単に行うことができます。

<!-- Once you have created a view, you may return it from one of your application's routes or controllers using the global `view` helper: -->
ビューを作成したら、グローバル `view` ヘルパを使用して、アプリケーションのルートまたはコントローラの 1 つからビューを返すことができます。

```
Route::get('/', function () {
    return view('greeting', ['name' => 'James']);
});
```

<!-- Views may also be returned using the `View` facade: -->
ビューは、`View` ファサードを使用して返すこともできます。

```
use Illuminate\Support\Facades\View;

return View::make('greeting', ['name' => 'James']);
```

<!-- As you can see, the first argument passed to the `view` helper corresponds to the name of the view file in the `resources/views` directory. The second argument is an array of data that should be made available to the view. In this case, we are passing the `name` variable, which is displayed in the view using [Blade syntax](/docs/11.x/blade). -->
ご覧のとおり、`view` ヘルパに渡される最初の引数は、`resources/views` ディレクトリ内のビュー ファイルの名前に対応します。 2 番目の引数は、ビューで使用できるようにするデータの配列です。この場合、`name` 変数を渡しており、[Blade syntax](/docs/11.x/blade) を使用してビューに表示されます。

<a name="nested-view-directories"></a>
<!-- ### Nested View Directories -->
### Nested View Directories

<!-- Views may also be nested within subdirectories of the `resources/views` directory. "Dot" notation may be used to reference nested views. For example, if your view is stored at `resources/views/admin/profile.blade.php`, you may return it from one of your application's routes / controllers like so: -->
ビューは、`resources/views` ディレクトリのサブディレクトリ内にネストすることもできます。 「ドット」表記は、ネストされたビューを参照するために使用できます。たとえば、ビューが `resources/views/admin/profile.blade.php` に保存されている場合、次のようにアプリケーションのルート/コントローラの 1 つからビューを返すことができます。

```
return view('admin.profile', $data);
```

> [!WARNING]
> ビュー ディレクトリ名には、`.` 文字を含めないでください。

<a name="creating-the-first-available-view"></a>
<!-- ### Creating the First Available View -->
### Creating the First Available View

<!-- Using the `View` facade's `first` method, you may create the first view that exists in a given array of views. This may be useful if your application or package allows views to be customized or overwritten: -->
`View` ファサードの `first` メソッドを使用すると、指定されたビューの配列に存在する最初のビューを作成できます。これは、アプリケーションまたはパッケージでビューのカスタマイズまたは上書きが許可されている場合に便利です。

```
use Illuminate\Support\Facades\View;

return View::first(['custom.admin', 'admin'], $data);
```

<a name="determining-if-a-view-exists"></a>
<!-- ### Determining if a View Exists -->
### Determining if a View Exists

<!-- If you need to determine if a view exists, you may use the `View` facade. The `exists` method will return `true` if the view exists: -->
ビューが存在するかどうかを確認する必要がある場合は、`View` ファサードを使用できます。ビューが存在する場合、`exists` メソッドは `true` を返します。

```
use Illuminate\Support\Facades\View;

if (View::exists('admin.profile')) {
    // ...
}
```

<a name="passing-data-to-views"></a>
<!-- ## Passing Data to Views -->
## Passing Data to Views

<!-- As you saw in the previous examples, you may pass an array of data to views to make that data available to the view: -->
前の例で見たように、データの配列をビューに渡して、そのデータをビューで使用できるようにすることができます。

```
return view('greetings', ['name' => 'Victoria']);
```

<!-- When passing information in this manner, the data should be an array with key / value pairs. After providing data to a view, you can then access each value within your view using the data's keys, such as `<?php echo $name; ?>`. -->
この方法で情報を渡す場合、データはキーと値のペアを含む配列である必要があります。データをビューに提供した後、`<?php echo $name; ?>` などのデータのキーを使用してビュー内の各値にアクセスできます。

<!-- As an alternative to passing a complete array of data to the `view` helper function, you may use the `with` method to add individual pieces of data to the view. The `with` method returns an instance of the view object so that you can continue chaining methods before returning the view: -->
データの完全な配列を `view` ヘルパ関数に渡す代わりに、`with` メソッドを使用して個々のデータをビューに追加できます。 `with` メソッドはビュー オブジェクトのインスタンスを返すため、ビューを返す前にメソッドの連鎖を続けることができます。

```
return view('greeting')
    ->with('name', 'Victoria')
    ->with('occupation', 'Astronaut');
```

<a name="sharing-data-with-all-views"></a>
<!-- ### Sharing Data With All Views -->
### Sharing Data With All Views

<!-- Occasionally, you may need to share data with all views that are rendered by your application. You may do so using the `View` facade's `share` method. Typically, you should place calls to the `share` method within a service provider's `boot` method. You are free to add them to the `App\Providers\AppServiceProvider` class or generate a separate service provider to house them: -->
場合によっては、アプリケーションによってレンダリングされるすべてのビューとデータを共有することが必要になる場合があります。これは、`View` ファサードの `share` メソッドを使用して行うことができます。通常、サービスプロバイダの `boot` メソッド内で `share` メソッドの呼び出しを行う必要があります。これらを `App\Providers\AppServiceProvider` クラスに自由に追加することも、それらを格納する別のサービスプロバイダを生成することもできます。

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::share('key', 'value');
    }
}
```

<a name="view-composers"></a>
<!-- ## View Composers -->
## View Composers

<!-- View composers are callbacks or class methods that are called when a view is rendered. If you have data that you want to be bound to a view each time that view is rendered, a view composer can help you organize that logic into a single location. View composers may prove particularly useful if the same view is returned by multiple routes or controllers within your application and always needs a particular piece of data. -->
ビュー コンポーザーは、ビューのレンダリング時に呼び出されるコールバックまたはクラス メソッドです。ビューがレンダリングされるたびにビューにバインドしたいデータがある場合、ビュー コンポーザーを使用すると、そのロジックを 1 つの場所に整理できます。ビュー コンポーザーは、アプリケーション内の複数のルートまたはコントローラから同じビューが返され、常に特定のデータを必要とする場合に特に便利です。

<!-- Typically, view composers will be registered within one of your application's [service providers](/docs/11.x/providers). In this example, we'll assume that the `App\Providers\AppServiceProvider` will house this logic. -->
通常、ビュー コンポーザーはアプリケーションの [service providers](/docs/11.x/providers) の 1 つに登録されます。この例では、`App\Providers\AppServiceProvider` にこのロジックが格納されると想定します。

<!-- We'll use the `View` facade's `composer` method to register the view composer. Laravel does not include a default directory for class based view composers, so you are free to organize them however you wish. For example, you could create an `app/View/Composers` directory to house all of your application's view composers: -->
`View` ファサードの `composer` メソッドを使用して、ビュー コンポーザーを登録します。 Laravel にはクラスベースのビューコンポーザー用のデフォルトディレクトリが含まれていないため、必要に応じて自由に編成できます。たとえば、アプリケーションのすべてのビュー コンポーザを格納する `app/View/Composers` ディレクトリを作成できます。

```
<?php

namespace App\Providers;

use App\View\Composers\ProfileComposer;
use Illuminate\Support\Facades;
use Illuminate\Support\ServiceProvider;
use Illuminate\View\View;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // Using class based composers...
        Facades\View::composer('profile', ProfileComposer::class);

        // Using closure based composers...
        Facades\View::composer('welcome', function (View $view) {
            // ...
        });

        Facades\View::composer('dashboard', function (View $view) {
            // ...
        });
    }
}
```

<!-- Now that we have registered the composer, the `compose` method of the `App\View\Composers\ProfileComposer` class will be executed each time the `profile` view is being rendered. Let's take a look at an example of the composer class: -->
コンポーザーを登録したので、`profile` ビューがレンダリングされるたびに、`App\View\Composers\ProfileComposer` クラスの `compose` メソッドが実行されます。 Composer クラスの例を見てみましょう。

```
<?php

namespace App\View\Composers;

use App\Repositories\UserRepository;
use Illuminate\View\View;

class ProfileComposer
{
    /**
     * Create a new profile composer.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}

    /**
     * Bind data to the view.
     */
    public function compose(View $view): void
    {
        $view->with('count', $this->users->count());
    }
}
```

<!-- As you can see, all view composers are resolved via the [service container](/docs/11.x/container), so you may type-hint any dependencies you need within a composer's constructor. -->
ご覧のとおり、すべてのビュー コンポーザーは [service container](/docs/11.x/container) 経由で解決されるため、コンポーザーのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="attaching-a-composer-to-multiple-views"></a>
<!-- #### Attaching a Composer to Multiple Views -->
#### Attaching a Composer to Multiple Views

<!-- You may attach a view composer to multiple views at once by passing an array of views as the first argument to the `composer` method: -->
ビューの配列を最初の引数として `composer` メソッドに渡すことで、ビュー コンポーザーを複数のビューに一度にアタッチできます。

```
use App\Views\Composers\MultiComposer;
use Illuminate\Support\Facades\View;

View::composer(
    ['profile', 'dashboard'],
    MultiComposer::class
);
```

<!-- The `composer` method also accepts the `*` character as a wildcard, allowing you to attach a composer to all views: -->
`composer` メソッドは、ワイルドカードとして `*` 文字も受け入れ、すべてのビューにコンポーザーをアタッチできます。

```
use Illuminate\Support\Facades;
use Illuminate\View\View;

Facades\View::composer('*', function (View $view) {
    // ...
});
```

<a name="view-creators"></a>
<!-- ### View Creators -->
### View Creators

<!-- View "creators" are very similar to view composers; however, they are executed immediately after the view is instantiated instead of waiting until the view is about to render. To register a view creator, use the `creator` method: -->
ビューの「クリエイター」はビューのコンポーザーと非常によく似ています。ただし、ビューがレンダリングされる直前まで待機するのではなく、ビューがインスタンス化された直後に実行されます。ビュークリエーターを登録するには、`creator` メソッドを使用します。

```
use App\View\Creators\ProfileCreator;
use Illuminate\Support\Facades\View;

View::creator('profile', ProfileCreator::class);
```

<a name="optimizing-views"></a>
<!-- ## Optimizing Views -->
## Optimizing Views

<!-- By default, Blade template views are compiled on demand. When a request is executed that renders a view, Laravel will determine if a compiled version of the view exists. If the file exists, Laravel will then determine if the uncompiled view has been modified more recently than the compiled view. If the compiled view either does not exist, or the uncompiled view has been modified, Laravel will recompile the view. -->
デフォルトでは、Blade テンプレート ビューはオンデマンドでコンパイルされます。ビューをレンダリングするリクエストが実行されると、Laravel はビューのコンパイルされたバージョンが存在するかどうかを判断します。ファイルが存在する場合、Laravel は、コンパイルされていないビューがコンパイルされたビューよりも最近に変更されたかどうかを判断します。コンパイル済みビューが存在しないか、アンコンパイル済みビューが変更されている場合、Laravel はビューを再コンパイルします。

<!-- Compiling views during the request may have a small negative impact on performance, so Laravel provides the `view:cache` Artisan command to precompile all of the views utilized by your application. For increased performance, you may wish to run this command as part of your deployment process: -->
リクエスト中にビューをコンパイルすると、パフォーマンスにわずかな悪影響を及ぼす可能性があるため、Laravel は、アプリケーションで使用されるすべてのビューをプリコンパイルするための `view:cache` Artisan コマンドを提供します。パフォーマンスを向上させるために、展開プロセスの一部として次のコマンドを実行するとよいでしょう。

```shell
php artisan view:cache
```

<!-- You may use the `view:clear` command to clear the view cache: -->
`view:clear` コマンドを使用してビュー キャッシュをクリアできます。

```shell
php artisan view:clear
```

