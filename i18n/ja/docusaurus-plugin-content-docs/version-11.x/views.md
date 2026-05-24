# ビュー (Views)

- [Introduction](#introduction)
    - [React / Vue でのビューの作成](#writing-views-in-react-or-vue)
- [ビューの作成とレンダリング](#creating-and-rendering-views)
    - [ネストされたビューのディレクトリ](#nested-view-directories)
    - [最初に使用可能なビューの作成](#creating-the-first-available-view)
    - [ビューが存在するかどうかの確認](#determining-if-a-view-exists)
- [データをビューに渡す](#passing-data-to-views)
    - [すべてのビューでデータを共有する](#sharing-data-with-all-views)
- [作曲家を見る](#view-composers)
    - [クリエイターを見る](#view-creators)
- [ビューの最適化](#optimizing-views)

<a name="introduction"></a>
## 導入 (Introduction)

もちろん、HTML ドキュメントの文字列全体をルートやコントローラから直接返すのは現実的ではありません。ありがたいことに、ビューはすべての HTML を個別のファイルに配置する便利な方法を提供します。

ビューは、コントローラ/アプリケーション ロジックをプレゼンテーション ロジックから分離し、`resources/views` ディレクトリに保存されます。 Laravel を使用する場合、ビュー テンプレートは通常、[Blade テンプレート言語](/docs/{{version}}/blade) を使用して記述されます。単純なビューは次のようになります。

```blade
<!-- View stored in resources/views/greeting.blade.php -->

<html>
    <body>
        <h1>Hello, {{ $name }}</h1>
    </body>
</html>
```

このビューは `resources/views/greeting.blade.php` に保存されているため、次のようにグローバル `view` ヘルパを使用してビューを返すことができます。

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

> [!NOTE]  
> Blade テンプレートの作成方法に関する詳細情報をお探しですか?開始するには、[Bladeのドキュメント](/docs/{{version}}/blade) の全文を確認してください。

<a name="writing-views-in-react-or-vue"></a>
### React / Vue でのビューの作成

多くの開発者は、Blade を介して PHP でフロントエンド テンプレートを作成する代わりに、React または Vue を使用してテンプレートを作成することを好み始めています。 Laravel では、SPA の構築によくある複雑さを必要とせずに、React / Vue フロントエンドを Laravel バックエンドに簡単に接続できるライブラリ [Inertia](https://inertiajs.com/) のおかげで、これを簡単に実行できます。

Breeze と Jetstream [スターターキット](/docs/{{version}}/starter-kits) は、Inertia を利用した次の Laravel アプリケーションの優れた出発点となります。さらに、[Laravelブートキャンプ](https://bootcamp.laravel.com) は、Vue と React の例を含む、Inertia を利用した Laravel アプリケーションの構築に関する完全なデモンストレーションを提供します。

<a name="creating-and-rendering-views"></a>
## ビューの作成とレンダリング (Creating and Rendering Views)

アプリケーションの `resources/views` ディレクトリに `.blade.php` 拡張子を持つファイルを配置するか、`make:view` Artisan コマンドを使用して、ビューを作成できます。

```shell
php artisan make:view greeting
```

`.blade.php` 拡張子は、ファイルに [Blade テンプレート](/docs/{{version}}/blade) が含まれていることをフレームワークに通知します。 Blade テンプレートには、HTML と Blade ディレクティブが含まれており、値のエコー、「if」ステートメントの作成、データの反復などを簡単に行うことができます。

ビューを作成したら、グローバル `view` ヘルパを使用して、アプリケーションのルートまたはコントローラの 1 つからビューを返すことができます。

    Route::get('/', function () {
        return view('greeting', ['name' => 'James']);
    });

ビューは、`View` ファサードを使用して返すこともできます。

    use Illuminate\Support\Facades\View;

    return View::make('greeting', ['name' => 'James']);

ご覧のとおり、`view` ヘルパに渡される最初の引数は、`resources/views` ディレクトリ内のビュー ファイルの名前に対応します。 2 番目の引数は、ビューで使用できるようにするデータの配列です。この場合、`name` 変数を渡しており、[Blade 構文](/docs/{{version}}/blade) を使用してビューに表示されます。

<a name="nested-view-directories"></a>
### ネストされたビューのディレクトリ

ビューは、`resources/views` ディレクトリのサブディレクトリ内にネストすることもできます。 「ドット」表記は、ネストされたビューを参照するために使用できます。たとえば、ビューが `resources/views/admin/profile.blade.php` に保存されている場合、次のようにアプリケーションのルート/コントローラの 1 つからビューを返すことができます。

    return view('admin.profile', $data);

> [!WARNING]  
> ビュー ディレクトリ名には、`.` 文字を含めないでください。

<a name="creating-the-first-available-view"></a>
### 最初に使用可能なビューの作成

`View` ファサードの `first` メソッドを使用すると、指定されたビューの配列に存在する最初のビューを作成できます。これは、アプリケーションまたはパッケージでビューのカスタマイズまたは上書きが許可されている場合に便利です。

    use Illuminate\Support\Facades\View;

    return View::first(['custom.admin', 'admin'], $data);

<a name="determining-if-a-view-exists"></a>
### ビューが存在するかどうかの確認

ビューが存在するかどうかを確認する必要がある場合は、`View` ファサードを使用できます。ビューが存在する場合、`exists` メソッドは `true` を返します。

    use Illuminate\Support\Facades\View;

    if (View::exists('admin.profile')) {
        // ...
    }

<a name="passing-data-to-views"></a>
## データをビューに渡す (Passing Data to Views)

前の例で見たように、データの配列をビューに渡して、そのデータをビューで使用できるようにすることができます。

    return view('greetings', ['name' => 'Victoria']);

この方法で情報を渡す場合、データはキーと値のペアを含む配列である必要があります。データをビューに提供した後、`<?php echo $name; ?>` などのデータのキーを使用してビュー内の各値にアクセスできます。

データの完全な配列を `view` ヘルパ関数に渡す代わりに、`with` メソッドを使用して個々のデータをビューに追加できます。 `with` メソッドはビュー オブジェクトのインスタンスを返すため、ビューを返す前にメソッドの連鎖を続けることができます。

    return view('greeting')
        ->with('name', 'Victoria')
        ->with('occupation', 'Astronaut');

<a name="sharing-data-with-all-views"></a>
### すべてのビューでデータを共有する

場合によっては、アプリケーションによってレンダリングされるすべてのビューとデータを共有することが必要になる場合があります。これは、`View` ファサードの `share` メソッドを使用して行うことができます。通常、サービスプロバイダの `boot` メソッド内で `share` メソッドの呼び出しを行う必要があります。これらを `App\Providers\AppServiceProvider` クラスに自由に追加することも、それらを格納する別のサービスプロバイダを生成することもできます。

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

<a name="view-composers"></a>
## 作曲家を見る (View Composers)

ビュー コンポーザーは、ビューのレンダリング時に呼び出されるコールバックまたはクラス メソッドです。ビューがレンダリングされるたびにビューにバインドしたいデータがある場合、ビュー コンポーザーを使用すると、そのロジックを 1 つの場所に整理できます。ビュー コンポーザーは、アプリケーション内の複数のルートまたはコントローラから同じビューが返され、常に特定のデータを必要とする場合に特に便利です。

通常、ビュー コンポーザーはアプリケーションの [サービスプロバイダ](/docs/{{version}}/providers) の 1 つに登録されます。この例では、`App\Providers\AppServiceProvider` にこのロジックが格納されると想定します。

`View` ファサードの `composer` メソッドを使用して、ビュー コンポーザーを登録します。 Laravel にはクラスベースのビューコンポーザー用のデフォルトディレクトリが含まれていないため、必要に応じて自由に編成できます。たとえば、アプリケーションのすべてのビュー コンポーザを格納する `app/View/Composers` ディレクトリを作成できます。

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

コンポーザーを登録したので、`profile` ビューがレンダリングされるたびに、`App\View\Composers\ProfileComposer` クラスの `compose` メソッドが実行されます。 Composer クラスの例を見てみましょう。

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

ご覧のとおり、すべてのビュー コンポーザーは [サービスコンテナ](/docs/{{version}}/container) 経由で解決されるため、コンポーザーのコンストラクター内で必要な依存関係をタイプヒントで指定できます。

<a name="attaching-a-composer-to-multiple-views"></a>
#### コンポーザを複数のビューにアタッチする

ビューの配列を最初の引数として `composer` メソッドに渡すことで、ビュー コンポーザーを複数のビューに一度にアタッチできます。

    use App\Views\Composers\MultiComposer;
    use Illuminate\Support\Facades\View;

    View::composer(
        ['profile', 'dashboard'],
        MultiComposer::class
    );

`composer` メソッドは、ワイルドカードとして `*` 文字も受け入れ、すべてのビューにコンポーザーをアタッチできます。

    use Illuminate\Support\Facades;
    use Illuminate\View\View;

    Facades\View::composer('*', function (View $view) {
        // ...
    });

<a name="view-creators"></a>
### クリエイターを見る

ビューの「クリエイター」はビューのコンポーザーと非常によく似ています。ただし、ビューがレンダリングされる直前まで待機するのではなく、ビューがインスタンス化された直後に実行されます。ビュークリエーターを登録するには、`creator` メソッドを使用します。

    use App\View\Creators\ProfileCreator;
    use Illuminate\Support\Facades\View;

    View::creator('profile', ProfileCreator::class);

<a name="optimizing-views"></a>
## ビューの最適化 (Optimizing Views)

デフォルトでは、Blade テンプレート ビューはオンデマンドでコンパイルされます。ビューをレンダリングするリクエストが実行されると、Laravel はビューのコンパイルされたバージョンが存在するかどうかを判断します。ファイルが存在する場合、Laravel は、コンパイルされていないビューがコンパイルされたビューよりも最近に変更されたかどうかを判断します。コンパイル済みビューが存在しないか、アンコンパイル済みビューが変更されている場合、Laravel はビューを再コンパイルします。

リクエスト中にビューをコンパイルすると、パフォーマンスにわずかな悪影響を及ぼす可能性があるため、Laravel は、アプリケーションで使用されるすべてのビューをプリコンパイルするための `view:cache` Artisan コマンドを提供します。パフォーマンスを向上させるために、展開プロセスの一部として次のコマンドを実行するとよいでしょう。

```shell
php artisan view:cache
```

`view:clear` コマンドを使用してビュー キャッシュをクリアできます。

```shell
php artisan view:clear
```

