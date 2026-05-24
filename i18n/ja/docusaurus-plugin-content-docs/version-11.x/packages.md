# パッケージ開発 (Package Development)

- [Introduction](#introduction)
    - [ファサードに関する注意事項](#a-note-on-facades)
- [パッケージの発見](#package-discovery)
- [サービスプロバイダ](#service-providers)
- [Resources](#resources)
    - [Configuration](#configuration)
    - [Migrations](#migrations)
    - [Routes](#routes)
    - [言語ファイル](#language-files)
    - [Views](#views)
    - [コンポーネントの表示](#view-components)
    - [Artisan コマンド「について」](#about-artisan-command)
- [Commands](#commands)
    - [最適化コマンド](#optimize-commands)
- [公共資産](#public-assets)
- [ファイルグループの公開](#publishing-file-groups)

<a name="introduction"></a>
## 導入 (Introduction)

パッケージは、Laravel に機能を追加する主な方法です。パッケージには、[Carbon](https://github.com/briannesbitt/Carbon) のような日付を扱うための優れた方法から、Spatie の [Laravelメディアライブラリ](https://github.com/spatie/laravel-medialibrary) のような Eloquent モデルにファイルを関連付けることができるパッケージまで、さまざまなものが含まれます。

パッケージにはさまざまな種類があります。一部のパッケージはスタンドアロンです。つまり、任意の PHP フレームワークで動作します。 Carbon と Pest はスタンドアロン パッケージの例です。これらのパッケージはいずれも、`composer.json` ファイルで要求することで Laravel で使用できます。

一方、他のパッケージは特に Laravel で使用することを目的としています。これらのパッケージには、特に Laravel アプリケーションを強化することを目的としたルート、コントローラ、ビュー、構成が含まれている場合があります。このガイドでは主に、Laravel 固有のパッケージの開発について説明します。

<a name="a-note-on-facades"></a>
### ファサードに関する注意事項

Laravel アプリケーションを作成する場合、コントラクトを使用するかファサードを使用するかは、どちらも本質的に同じレベルのテスト容易性を提供するため、通常は問題になりません。ただし、パッケージを作成する場合、パッケージは通常、Laravel のテスト ヘルパのすべてにアクセスできるわけではありません。パッケージが典型的な Laravel アプリケーション内にインストールされているかのようにパッケージ テストを作成できるようにしたい場合は、[オーケストラテストベンチ](https://github.com/orchestral/testbench) パッケージを使用できます。

<a name="package-discovery"></a>
## パッケージの発見 (Package Discovery)

Laravel アプリケーションの `bootstrap/providers.php` ファイルには、Laravel によってロードされる必要があるサービスプロバイダのリストが含まれています。ただし、ユーザーにサービスプロバイダを手動でリストに追加する代わりに、パッケージの `composer.json` ファイルの `extra` セクションでプロバイダを定義して、Laravel によって自動的にロードされるようにすることもできます。サービスプロバイダに加えて、登録したい [facades](/docs/{{version}}/facades) をリストすることもできます。

```json
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},
```

パッケージが検出用に設定されると、Laravel はインストール時にサービスプロバイダとファサードを自動的に登録し、パッケージのユーザーにとって便利なインストールエクスペリエンスを作成します。

<a name="opting-out-of-package-discovery"></a>
#### パッケージディスカバリーのオプトアウト

あなたがパッケージのコンシューマであり、パッケージのパッケージ検出を無効にしたい場合は、アプリケーションの `composer.json` ファイルの `extra` セクションにパッケージ名をリストすることができます。

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

アプリケーションの `dont-discover` ディレクティブ内で `*` 文字を使用すると、すべてのパッケージのパッケージ検出を無効にすることができます。

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
## サービスプロバイダ (Service Providers)

[サービスプロバイダ](/docs/{{version}}/providers) は、パッケージと Laravel の間の接続ポイントです。サービスプロバイダは、物事をLaravelの[サービスコンテナ](/docs/{{version}}/container)にバインドし、ビュー、構成、言語ファイルなどのパッケージリソースをロードする場所をLaravelに通知する責任があります。

サービスプロバイダは `Illuminate\Support\ServiceProvider` クラスを拡張し、`register` と `boot` の 2 つのメソッドを含みます。基本 `ServiceProvider` クラスは `illuminate/support` Composer パッケージにあり、これを独自のパッケージの依存関係に追加する必要があります。サービスプロバイダの構造と目的の詳細については、[彼らの文書](/docs/{{version}}/providers) を確認してください。

<a name="resources"></a>
## リソース (Resources)

<a name="configuration"></a>
### 構成

通常、パッケージの構成ファイルをアプリケーションの `config` ディレクトリに公開する必要があります。これにより、パッケージのユーザーがデフォルトの構成オプションを簡単にオーバーライドできるようになります。構成ファイルを公開できるようにするには、サービスプロバイダの `boot` メソッドから `publishes` メソッドを呼び出します。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/courier.php' => config_path('courier.php'),
        ]);
    }

これで、パッケージのユーザーが Laravel の `vendor:publish` コマンドを実行すると、ファイルは指定された公開場所にコピーされます。構成が公開されると、他の構成ファイルと同様にその値にアクセスできるようになります。

    $value = config('courier.option');

> [!WARNING]  
> 構成ファイルでクロージャを定義しないでください。ユーザーが `config:cache` Artisan コマンドを実行すると、これらを正しくシリアル化できません。

<a name="default-package-configuration"></a>
#### デフォルトのパッケージ構成

独自のパッケージ構成ファイルをアプリケーションの公開されたコピーとマージすることもできます。これにより、ユーザーは、公開された構成ファイルのコピーで実際にオーバーライドしたいオプションのみを定義できるようになります。構成ファイルの値をマージするには、サービスプロバイダの `register` メソッド内で `mergeConfigFrom` メソッドを使用します。

`mergeConfigFrom` メソッドは、パッケージの構成ファイルへのパスを最初の引数として受け入れ、アプリケーションの構成ファイルのコピーの名前を 2 番目の引数として受け入れます。

    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->mergeConfigFrom(
            __DIR__.'/../config/courier.php', 'courier'
        );
    }

> [!WARNING]  
> このメソッドは、構成配列の最初のレベルのみをマージします。ユーザーが多次元構成配列を部分的に定義した場合、不足しているオプションはマージされません。

<a name="routes"></a>
### ルート

パッケージにルートが含まれている場合は、`loadRoutesFrom` メソッドを使用してルートをロードできます。このメソッドは、アプリケーションのルートがキャッシュされているかどうかを自動的に判断し、ルートがすでにキャッシュされている場合はルート ファイルをロードしません。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
    }

<a name="migrations"></a>
### 移行

パッケージに [データベースの移行](/docs/{{version}}/migrations) が含まれている場合は、`publishesMigrations` メソッドを使用して、指定されたディレクトリまたはファイルに移行が含まれていることを Laravel に通知できます。 Laravel が移行を公開すると、ファイル名の中のタイムスタンプが現在の日付と時刻を反映するように自動的に更新されます。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->publishesMigrations([
            __DIR__.'/../database/migrations' => database_path('migrations'),
        ]);
    }

<a name="language-files"></a>
### 言語ファイル

パッケージに [言語ファイル](/docs/{{version}}/localization) が含まれている場合は、`loadTranslationsFrom` メソッドを使用して、それらをロードする方法を Laravel に通知できます。たとえば、パッケージの名前が `courier` の場合、サービスプロバイダの `boot` メソッドに次のコードを追加する必要があります。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
    }

パッケージ変換行は、`package::file.line` 構文規則を使用して参照されます。したがって、次のように `messages` ファイルから `courier` パッケージの `welcome` 行をロードできます。

    echo trans('courier::messages.welcome');

`loadJsonTranslationsFrom` メソッドを使用して、パッケージの JSON 翻訳ファイルを登録できます。このメソッドは、パッケージの JSON 翻訳ファイルを含むディレクトリへのパスを受け入れます。

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}
```

<a name="publishing-language-files"></a>
#### 言語ファイルの公開

パッケージの言語ファイルをアプリケーションの `lang/vendor` ディレクトリに公開したい場合は、サービスプロバイダの `publishes` メソッドを使用できます。 `publishes` メソッドは、パッケージ パスとその必要な公開場所の配列を受け入れます。たとえば、`courier` パッケージの言語ファイルを公開するには、次の手順を実行します。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

        $this->publishes([
            __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
        ]);
    }

これで、パッケージのユーザーが Laravel の `vendor:publish` Artisan コマンドを実行すると、パッケージの言語ファイルが指定された公開場所に公開されます。

<a name="views"></a>
### ビュー

パッケージの [views](/docs/{{version}}/views) を Laravel に登録するには、ビューがどこにあるかを Laravel に伝える必要があります。これは、サービスプロバイダの `loadViewsFrom` メソッドを使用して実行できます。 `loadViewsFrom` メソッドは、ビュー テンプレートへのパスとパッケージの名前という 2 つの引数を受け入れます。たとえば、パッケージの名前が `courier` の場合、サービスプロバイダの `boot` メソッドに次のコードを追加します。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
    }

パッケージ ビューは、`package::view` 構文規則を使用して参照されます。したがって、ビュー パスがサービスプロバイダに登録されたら、次のように `courier` パッケージから `dashboard` ビューをロードできます。

    Route::get('/dashboard', function () {
        return view('courier::dashboard');
    });

<a name="overriding-package-views"></a>
#### パッケージビューの上書き

`loadViewsFrom` メソッドを使用すると、Laravel は実際にビュー用に 2 つの場所 (アプリケーションの `resources/views/vendor` ディレクトリと指定したディレクトリ) を登録します。したがって、例として `courier` パッケージを使用すると、Laravel は最初に、ビューのカスタム バージョンが開発者によって `resources/views/vendor/courier` ディレクトリに配置されているかどうかを確認します。次に、ビューがカスタマイズされていない場合、Laravel は `loadViewsFrom` の呼び出しで指定したパッケージ ビュー ディレクトリを検索します。これにより、パッケージ ユーザーがパッケージのビューを簡単にカスタマイズ/オーバーライドできるようになります。

<a name="publishing-views"></a>
#### ビューの公開

ビューをアプリケーションの `resources/views/vendor` ディレクトリに公開できるようにしたい場合は、サービスプロバイダの `publishes` メソッドを使用できます。 `publishes` メソッドは、パッケージ ビュー パスとその必要な公開場所の配列を受け入れます。

    /**
     * Bootstrap the package services.
     */
    public function boot(): void
    {
        $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

        $this->publishes([
            __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
        ]);
    }

これで、パッケージのユーザーが Laravel の `vendor:publish` Artisan コマンドを実行すると、パッケージのビューが指定された公開場所にコピーされます。

<a name="view-components"></a>
### コンポーネントの表示

Bladeコンポーネントを利用するパッケージを構築している場合、またはコンポーネントを従来とは異なるディレクトリに配置している場合は、Laravelがコンポーネントの場所を認識できるように、コンポーネントクラスとそのHTMLタグエイリアスを手動で登録する必要があります。通常、コンポーネントはパッケージのサービスプロバイダの `boot` メソッドに登録する必要があります。

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * Bootstrap your package's services.
     */
    public function boot(): void
    {
        Blade::component('package-alert', AlertComponent::class);
    }

コンポーネントが登録されると、そのタグ エイリアスを使用してレンダリングできます。

```blade
<x-package-alert/>
```

<a name="autoloading-package-components"></a>
#### パッケージコンポーネントの自動ロード

あるいは、`componentNamespace` メソッドを使用して、規則に従ってコンポーネント クラスを自動ロードすることもできます。たとえば、`Nightshade` パッケージには、`Nightshade\Views\Components` 名前空間内に存在する `Calendar` コンポーネントと `ColorPicker` コンポーネントが含まれる場合があります。

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     */
    public function boot(): void
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

これにより、`package-name::` 構文を使用して、ベンダー名前空間によるパッケージ コンポーネントの使用が許可されます。

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade は、コンポーネント名をパスカル文字に変換することで、このコンポーネントにリンクされているクラスを自動的に検出します。サブディレクトリは、「ドット」表記を使用してサポートされています。

<a name="anonymous-components"></a>
#### 匿名コンポーネント

パッケージに匿名コンポーネントが含まれている場合は、パッケージの「views」ディレクトリ ([`loadViewsFrom`メソッド](#views) で指定) の `components` ディレクトリ内に配置する必要があります。次に、コンポーネント名にパッケージのビュー名前空間をプレフィックスとして付けることで、それらをレンダリングできます。

```blade
<x-courier::alert />
```

<a name="about-artisan-command"></a>
### Artisan コマンド「について」

Laravel の組み込み `about` Artisan コマンドは、アプリケーションの環境と構成の概要を提供します。パッケージは、`AboutCommand` クラスを介してこのコマンドの出力に追加情報をプッシュする場合があります。通常、この情報はパッケージ サービスプロバイダの `boot` メソッドから追加できます。

    use Illuminate\Foundation\Console\AboutCommand;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
    }

<a name="commands"></a>
## コマンド (Commands)

パッケージの Artisan コマンドを Laravel に登録するには、`commands` メソッドを使用できます。このメソッドはコマンド クラス名の配列を必要とします。コマンドが登録されたら、[Artisan CLI](/docs/{{version}}/artisan) を使用してコマンドを実行できます。

    use Courier\Console\Commands\InstallCommand;
    use Courier\Console\Commands\NetworkCommand;

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->commands([
                InstallCommand::class,
                NetworkCommand::class,
            ]);
        }
    }

<a name="optimize-commands"></a>
### 最適化コマンド

Laravel の [`optimize` コマンド](/docs/{{version}}/deployment#optimization) は、アプリケーションの構成、イベント、ルート、ビューをキャッシュします。 `optimizes` メソッドを使用すると、`optimize` および `optimize:clear` コマンドの実行時に呼び出されるパッケージ独自のArtisan コマンドを登録できます。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->optimizes(
                optimize: 'package:optimize',
                clear: 'package:clear-optimizations',
            );
        }
    }

<a name="public-assets"></a>
## 公共資産 (Public Assets)

パッケージには、JavaScript、CSS、画像などのアセットが含まれる場合があります。これらのアセットをアプリケーションの `public` ディレクトリに公開するには、サービスプロバイダの `publishes` メソッドを使用します。この例では、関連アセットのグループを簡単に公開するために使用できる `public` アセット グループ タグも追加します。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../public' => public_path('vendor/courier'),
        ], 'public');
    }

これで、パッケージのユーザーが `vendor:publish` コマンドを実行すると、アセットが指定された公開場所にコピーされます。通常、ユーザーはパッケージが更新されるたびにアセットを上書きする必要があるため、`--force` フラグを使用できます。

```shell
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
## ファイルグループの公開 (Publishing File Groups)

パッケージ アセットとリソースのグループを個別に公開したい場合があります。たとえば、パッケージのアセットの公開を強制せずに、ユーザーがパッケージの構成ファイルを公開できるようにしたい場合があります。これを行うには、パッケージのサービスプロバイダから `publishes` メソッドを呼び出すときに、それらを「タグ付け」します。たとえば、タグを使用して、パッケージのサービスプロバイダの `boot` メソッドで `courier` パッケージの 2 つの公開グループ (`courier-config` および `courier-migrations`) を定義してみましょう。

    /**
     * Bootstrap any package services.
     */
    public function boot(): void
    {
        $this->publishes([
            __DIR__.'/../config/package.php' => config_path('package.php')
        ], 'courier-config');

        $this->publishesMigrations([
            __DIR__.'/../database/migrations/' => database_path('migrations')
        ], 'courier-migrations');
    }

これで、ユーザーは `vendor:publish` コマンドの実行時にタグを参照することで、これらのグループを個別に公開できるようになります。

```shell
php artisan vendor:publish --tag=courier-config
```

