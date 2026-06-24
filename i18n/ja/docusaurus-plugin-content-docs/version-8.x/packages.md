<!-- # Package Development -->
# Package Development

- [Introduction](#introduction)
    - [A Note On Facades](#a-note-on-facades)
- [Package Discovery](#package-discovery)
- [Service Providers](#service-providers)
- [Resources](#resources)
    - [Configuration](#configuration)
    - [Migrations](#migrations)
    - [Routes](#routes)
    - [Translations](#translations)
    - [Views](#views)
    - [View Components](#view-components)
- [Commands](#commands)
- [Public Assets](#public-assets)
- [Publishing File Groups](#publishing-file-groups)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Packages are the primary way of adding functionality to Laravel. Packages might be anything from a great way to work with dates like [Carbon](https://github.com/briannesbitt/Carbon) or a package that allows you to associate files with Eloquent models like Spatie's [Laravel Media Library](https://github.com/spatie/laravel-medialibrary). -->
パッケージは、Laravel に機能を追加する主な方法です。パッケージには、[Carbon](https://github.com/briannesbitt/Carbon) のような日付を扱うための優れた方法から、Spatie の [Laravel Media Library](https://github.com/spatie/laravel-medialibrary) のような Eloquent モデルにファイルを関連付けることができるパッケージまで、さまざまなものが含まれます。

<!-- There are different types of packages. Some packages are stand-alone, meaning they work with any PHP framework. Carbon and PHPUnit are examples of stand-alone packages. Any of these packages may be used with Laravel by requiring them in your `composer.json` file. -->
パッケージにはさまざまな種類があります。一部のパッケージはスタンドアロンです。つまり、任意の PHP フレームワークで動作します。 Carbon と PHPUnit はスタンドアロン パッケージの例です。これらのパッケージはいずれも、`composer.json` ファイルで要求することで Laravel で使用できます。

<!-- On the other hand, other packages are specifically intended for use with Laravel. These packages may have routes, controllers, views, and configuration specifically intended to enhance a Laravel application. This guide primarily covers the development of those packages that are Laravel specific. -->
一方、他のパッケージは特に Laravel で使用することを目的としています。これらのパッケージには、特に Laravel アプリケーションを強化することを目的としたルート、コントローラ、ビュー、構成が含まれている場合があります。このガイドでは主に、Laravel 固有のパッケージの開発について説明します。

<a name="a-note-on-facades"></a>
<!-- ### A Note On Facades -->
### A Note On Facades

<!-- When writing a Laravel application, it generally does not matter if you use contracts or facades since both provide essentially equal levels of testability. However, when writing packages, your package will not typically have access to all of Laravel's testing helpers. If you would like to be able to write your package tests as if the package were installed inside a typical Laravel application, you may use the [Orchestral Testbench](https://github.com/orchestral/testbench) package. -->
Laravel アプリケーションを作成する場合、コントラクトを使用するかファサードを使用するかは、どちらも本質的に同じレベルのテスト容易性を提供するため、通常は問題になりません。ただし、パッケージを作成する場合、パッケージは通常、Laravel のテスト ヘルパのすべてにアクセスできるわけではありません。パッケージが典型的な Laravel アプリケーション内にインストールされているかのようにパッケージ テストを作成できるようにしたい場合は、[Orchestral Testbench](https://github.com/orchestral/testbench) パッケージを使用できます。

<a name="package-discovery"></a>
<!-- ## Package Discovery -->
## Package Discovery

<!-- In a Laravel application's `config/app.php` configuration file, the `providers` option defines a list of service providers that should be loaded by Laravel. When someone installs your package, you will typically want your service provider to be included in this list. Instead of requiring users to manually add your service provider to the list, you may define the provider in the `extra` section of your package's `composer.json` file. In addition to service providers, you may also list any [facades](/docs/8.x/facades) you would like to be registered: -->
Laravel アプリケーションの `config/app.php` 構成ファイルでは、`providers` オプションにより、Laravel によってロードされるサービスプロバイダのリストが定義されます。誰かがパッケージをインストールするときは、通常、サービスプロバイダをこのリストに含めることが必要になります。ユーザーにサービスプロバイダをリストに手動で追加するよう要求する代わりに、パッケージの `composer.json` ファイルの `extra` セクションでプロバイダを定義できます。サービスプロバイダに加えて、登録したい [facades](/docs/8.x/facades) をリストすることもできます。

```
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

<!-- Once your package has been configured for discovery, Laravel will automatically register its service providers and facades when it is installed, creating a convenient installation experience for your package's users. -->
パッケージが検出用に設定されると、Laravel はインストール時にサービスプロバイダとファサードを自動的に登録し、パッケージのユーザーにとって便利なインストールエクスペリエンスを作成します。

<a name="opting-out-of-package-discovery"></a>
<!-- ### Opting Out Of Package Discovery -->
### Opting Out Of Package Discovery

<!-- If you are the consumer of a package and would like to disable package discovery for a package, you may list the package name in the `extra` section of your application's `composer.json` file: -->
あなたがパッケージのコンシューマであり、パッケージのパッケージ検出を無効にしたい場合は、アプリケーションの `composer.json` ファイルの `extra` セクションにパッケージ名をリストすることができます。

```
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},
```

<!-- You may disable package discovery for all packages using the `*` character inside of your application's `dont-discover` directive: -->
アプリケーションの `dont-discover` ディレクティブ内で `*` 文字を使用すると、すべてのパッケージのパッケージ検出を無効にすることができます。

```
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},
```

<a name="service-providers"></a>
<!-- ## Service Providers -->
## Service Providers

<!-- [Service providers](/docs/8.x/providers) are the connection point between your package and Laravel. A service provider is responsible for binding things into Laravel's [service container](/docs/8.x/container) and informing Laravel where to load package resources such as views, configuration, and localization files. -->
[Service providers](/docs/8.x/providers) は、パッケージと Laravel の間の接続ポイントです。サービスプロバイダは、物事をLaravelの[service container](/docs/8.x/container)にバインドし、ビュー、構成、ローカリゼーションファイルなどのパッケージリソースをロードする場所をLaravelに通知する責任があります。

<!-- A service provider extends the `Illuminate\Support\ServiceProvider` class and contains two methods: `register` and `boot`. The base `ServiceProvider` class is located in the `illuminate/support` Composer package, which you should add to your own package's dependencies. To learn more about the structure and purpose of service providers, check out [their documentation](/docs/8.x/providers). -->
サービスプロバイダは `Illuminate\Support\ServiceProvider` クラスを拡張し、`register` と `boot` の 2 つのメソッドを含みます。基本 `ServiceProvider` クラスは `illuminate/support` Composer パッケージにあり、これを独自のパッケージの依存関係に追加する必要があります。サービスプロバイダの構造と目的の詳細については、[their documentation](/docs/8.x/providers) を確認してください。

<a name="resources"></a>
<!-- ## Resources -->
## Resources

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Typically, you will need to publish your package's configuration file to the application's `config` directory. This will allow users of your package to easily override your default configuration options. To allow your configuration files to be published, call the `publishes` method from the `boot` method of your service provider: -->
通常、パッケージの構成ファイルをアプリケーションの `config` ディレクトリに公開する必要があります。これにより、パッケージのユーザーがデフォルトの構成オプションを簡単にオーバーライドできるようになります。構成ファイルを公開できるようにするには、サービスプロバイダの `boot` メソッドから `publishes` メソッドを呼び出します。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` command, your file will be copied to the specified publish location. Once your configuration has been published, its values may be accessed like any other configuration file: -->
これで、パッケージのユーザーが Laravel の `vendor:publish` コマンドを実行すると、ファイルは指定された公開場所にコピーされます。構成が公開されると、他の構成ファイルと同様にその値にアクセスできるようになります。

```
$value = config('courier.option');
```

> [!NOTE]
> 設定ファイルでクロージャを定義しないでください。ユーザーが `config:cache` Artisan コマンドを実行すると、正しくシリアル化できません。

<a name="default-package-configuration"></a>
<!-- #### Default Package Configuration -->
#### Default Package Configuration

<!-- You may also merge your own package configuration file with the application's published copy. This will allow your users to define only the options they actually want to override in the published copy of the configuration file. To merge the configuration file values, use the `mergeConfigFrom` method within your service provider's `register` method. -->
独自のパッケージ構成ファイルをアプリケーションの公開されたコピーとマージすることもできます。これにより、ユーザーは、公開された構成ファイルのコピーで実際にオーバーライドしたいオプションのみを定義できるようになります。構成ファイルの値をマージするには、サービスプロバイダの `register` メソッド内で `mergeConfigFrom` メソッドを使用します。

<!-- The `mergeConfigFrom` method accepts the path to your package's configuration file as its first argument and the name of the application's copy of the configuration file as its second argument: -->
`mergeConfigFrom` メソッドは、パッケージの構成ファイルへのパスを最初の引数として受け入れ、アプリケーションの構成ファイルのコピーの名前を 2 番目の引数として受け入れます。

```
/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}
```

> [!NOTE]
> このメソッドは、構成配列の最初のレベルのみをマージします。ユーザーが多次元構成配列を部分的に定義した場合、不足しているオプションはマージされません。

<a name="routes"></a>
<!-- ### Routes -->
### Routes

<!-- If your package contains routes, you may load them using the `loadRoutesFrom` method. This method will automatically determine if the application's routes are cached and will not load your routes file if the routes have already been cached: -->
パッケージにルートが含まれている場合は、`loadRoutesFrom` メソッドを使用してルートをロードできます。このメソッドは、アプリケーションのルートがキャッシュされているかどうかを自動的に判断し、ルートがすでにキャッシュされている場合はルート ファイルをロードしません。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}
```

<a name="migrations"></a>
<!-- ### Migrations -->
### Migrations

<!-- If your package contains [database migrations](/docs/8.x/migrations), you may use the `loadMigrationsFrom` method to inform Laravel how to load them. The `loadMigrationsFrom` method accepts the path to your package's migrations as its only argument: -->
パッケージに [database migrations](/docs/8.x/migrations) が含まれている場合は、`loadMigrationsFrom` メソッドを使用して、それらをロードする方法を Laravel に通知できます。 `loadMigrationsFrom` メソッドは、パッケージの移行へのパスを唯一の引数として受け入れます。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadMigrationsFrom(__DIR__.'/../database/migrations');
}
```

<!-- Once your package's migrations have been registered, they will automatically be run when the `php artisan migrate` command is executed. You do not need to export them to the application's `database/migrations` directory. -->
パッケージの移行が登録されると、`php artisan migrate` コマンドの実行時に自動的に実行されます。これらをアプリケーションの `database/migrations` ディレクトリにエクスポートする必要はありません。

<a name="translations"></a>
<!-- ### Translations -->
### Translations

<!-- If your package contains [translation files](/docs/8.x/localization), you may use the `loadTranslationsFrom` method to inform Laravel how to load them. For example, if your package is named `courier`, you should add the following to your service provider's `boot` method: -->
パッケージに [translation files](/docs/8.x/localization) が含まれている場合は、`loadTranslationsFrom` メソッドを使用して、それらをロードする方法を Laravel に通知できます。たとえば、パッケージの名前が `courier` の場合、サービスプロバイダの `boot` メソッドに次のコードを追加する必要があります。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');
}
```

<!-- Package translations are referenced using the `package::file.line` syntax convention. So, you may load the `courier` package's `welcome` line from the `messages` file like so: -->
パッケージ翻訳は、`package::file.line` 構文規則を使用して参照されます。したがって、次のように `messages` ファイルから `courier` パッケージの `welcome` 行をロードできます。

```
echo trans('courier::messages.welcome');
```

<a name="publishing-translations"></a>
<!-- #### Publishing Translations -->
#### Publishing Translations

<!-- If you would like to publish your package's translations to the application's `resources/lang/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package paths and their desired publish locations. For example, to publish the translation files for the `courier` package, you may do the following: -->
パッケージの翻訳をアプリケーションの `resources/lang/vendor` ディレクトリに公開したい場合は、サービスプロバイダの `publishes` メソッドを使用できます。 `publishes` メソッドは、パッケージ パスとその必要な公開場所の配列を受け入れます。たとえば、`courier` パッケージの翻訳ファイルを公開するには、次の手順を実行します。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadTranslationsFrom(__DIR__.'/../resources/lang', 'courier');

    $this->publishes([
        __DIR__.'/../resources/lang' => resource_path('lang/vendor/courier'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's translations will be published to the specified publish location. -->
これで、パッケージのユーザーが Laravel の `vendor:publish` Artisan コマンドを実行すると、パッケージの翻訳が指定された公開場所に公開されます。

<a name="views"></a>
<!-- ### Views -->
### Views

<!-- To register your package's [views](/docs/8.x/views) with Laravel, you need to tell Laravel where the views are located. You may do this using the service provider's `loadViewsFrom` method. The `loadViewsFrom` method accepts two arguments: the path to your view templates and your package's name. For example, if your package's name is `courier`, you would add the following to your service provider's `boot` method: -->
パッケージの [views](/docs/8.x/views) を Laravel に登録するには、ビューがどこにあるかを Laravel に伝える必要があります。これは、サービスプロバイダの `loadViewsFrom` メソッドを使用して実行できます。 `loadViewsFrom` メソッドは、ビュー テンプレートへのパスとパッケージの名前という 2 つの引数を受け入れます。たとえば、パッケージの名前が `courier` の場合、サービスプロバイダの `boot` メソッドに次のコードを追加します。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}
```

<!-- Package views are referenced using the `package::view` syntax convention. So, once your view path is registered in a service provider, you may load the `dashboard` view from the `courier` package like so: -->
パッケージ ビューは、`package::view` 構文規則を使用して参照されます。したがって、ビュー パスがサービスプロバイダに登録されたら、次のように `courier` パッケージから `dashboard` ビューをロードできます。

```
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});
```

<a name="overriding-package-views"></a>
<!-- #### Overriding Package Views -->
#### Overriding Package Views

<!-- When you use the `loadViewsFrom` method, Laravel actually registers two locations for your views: the application's `resources/views/vendor` directory and the directory you specify. So, using the `courier` package as an example, Laravel will first check if a custom version of the view has been placed in the `resources/views/vendor/courier` directory by the developer. Then, if the view has not been customized, Laravel will search the package view directory you specified in your call to `loadViewsFrom`. This makes it easy for package users to customize / override your package's views. -->
`loadViewsFrom` メソッドを使用すると、Laravel は実際にビュー用に 2 つの場所 (アプリケーションの `resources/views/vendor` ディレクトリと指定したディレクトリ) を登録します。したがって、例として `courier` パッケージを使用すると、Laravel は最初に、ビューのカスタム バージョンが開発者によって `resources/views/vendor/courier` ディレクトリに配置されているかどうかを確認します。次に、ビューがカスタマイズされていない場合、Laravel は `loadViewsFrom` の呼び出しで指定したパッケージ ビュー ディレクトリを検索します。これにより、パッケージ ユーザーがパッケージのビューを簡単にカスタマイズ/オーバーライドできるようになります。

<a name="publishing-views"></a>
<!-- #### Publishing Views -->
#### Publishing Views

<!-- If you would like to make your views available for publishing to the application's `resources/views/vendor` directory, you may use the service provider's `publishes` method. The `publishes` method accepts an array of package view paths and their desired publish locations: -->
ビューをアプリケーションの `resources/views/vendor` ディレクトリに公開できるようにしたい場合は、サービスプロバイダの `publishes` メソッドを使用できます。 `publishes` メソッドは、パッケージ ビュー パスとその必要な公開場所の配列を受け入れます。

```
/**
 * Bootstrap the package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}
```

<!-- Now, when users of your package execute Laravel's `vendor:publish` Artisan command, your package's views will be copied to the specified publish location. -->
これで、パッケージのユーザーが Laravel の `vendor:publish` Artisan コマンドを実行すると、パッケージのビューが指定された公開場所にコピーされます。

<a name="view-components"></a>
<!-- ### View Components -->
### View Components

<!-- If your package contains [view components](/docs/8.x/blade#components), you may use the `loadViewComponentsAs` method to inform Laravel how to load them. The `loadViewComponentsAs` method accepts two arguments: the tag prefix for your view components and an array of your view component class names. For example, if your package's prefix is `courier` and you have `Alert` and `Button` view components, you would add the following to your service provider's `boot` method: -->
パッケージに [view components](/docs/8.x/blade#components) が含まれている場合は、`loadViewComponentsAs` メソッドを使用して、それらをロードする方法を Laravel に通知できます。 `loadViewComponentsAs` メソッドは、ビュー コンポーネントのタグ プレフィックスとビュー コンポーネント クラス名の配列の 2 つの引数を受け入れます。たとえば、パッケージのプレフィックスが `courier` で、`Alert` および `Button` ビュー コンポーネントがある場合、サービスプロバイダの `boot` メソッドに以下を追加します。

```
use Courier\Components\Alert;
use Courier\Components\Button;

/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->loadViewComponentsAs('courier', [
        Alert::class,
        Button::class,
    ]);
}
```

<!-- Once your view components are registered in a service provider, you may reference them in your view like so: -->
ビュー コンポーネントがサービスプロバイダに登録されたら、次のようにビュー内でそれらを参照できます。

```
<x-courier-alert />

<x-courier-button />
```

<a name="anonymous-components"></a>
<!-- #### Anonymous Components -->
#### Anonymous Components

<!-- If your package contains anonymous components, they must be placed within a `components` directory of your package's "views" directory (as specified by `loadViewsFrom`). Then, you may render them by prefixing the component name with the package's view namespace: -->
パッケージに匿名コンポーネントが含まれている場合は、パッケージの「views」ディレクトリ (`loadViewsFrom` で指定) の `components` ディレクトリ内に配置する必要があります。次に、コンポーネント名にパッケージのビュー名前空間をプレフィックスとして付けることで、それらをレンダリングできます。

```
<x-courier::alert />
```

<a name="commands"></a>
<!-- ## Commands -->
## Commands

<!-- To register your package's Artisan commands with Laravel, you may use the `commands` method. This method expects an array of command class names. Once the commands have been registered, you may execute them using the [Artisan CLI](/docs/8.x/artisan): -->
パッケージの Artisan コマンドを Laravel に登録するには、`commands` メソッドを使用できます。このメソッドはコマンド クラス名の配列を必要とします。コマンドが登録されたら、[Artisan CLI](/docs/8.x/artisan) を使用してコマンドを実行できます。

```
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}
```

<a name="public-assets"></a>
<!-- ## Public Assets -->
## Public Assets

<!-- Your package may have assets such as JavaScript, CSS, and images. To publish these assets to the application's `public` directory, use the service provider's `publishes` method. In this example, we will also add a `public` asset group tag, which may be used to easily publish groups of related assets: -->
パッケージには、JavaScript、CSS、画像などのアセットが含まれる場合があります。これらのアセットをアプリケーションの `public` ディレクトリに公開するには、サービスプロバイダの `publishes` メソッドを使用します。この例では、関連アセットのグループを簡単に公開するために使用できる `public` アセット グループ タグも追加します。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}
```

<!-- Now, when your package's users execute the `vendor:publish` command, your assets will be copied to the specified publish location. Since users will typically need to overwrite the assets every time the package is updated, you may use the `--force` flag: -->
これで、パッケージのユーザーが `vendor:publish` コマンドを実行すると、アセットが指定された公開場所にコピーされます。通常、ユーザーはパッケージが更新されるたびにアセットを上書きする必要があるため、`--force` フラグを使用できます。

```
php artisan vendor:publish --tag=public --force
```

<a name="publishing-file-groups"></a>
<!-- ## Publishing File Groups -->
## Publishing File Groups

<!-- You may want to publish groups of package assets and resources separately. For instance, you might want to allow your users to publish your package's configuration files without being forced to publish your package's assets. You may do this by "tagging" them when calling the `publishes` method from a package's service provider. For example, let's use tags to define two publish groups for the `courier` package (`courier-config` and `courier-migrations`) in the `boot` method of the package's service provider: -->
パッケージ アセットとリソースのグループを個別に公開したい場合があります。たとえば、パッケージのアセットの公開を強制せずに、ユーザーがパッケージの構成ファイルを公開できるようにしたい場合があります。これを行うには、パッケージのサービスプロバイダから `publishes` メソッドを呼び出すときに、それらを「タグ付け」します。たとえば、タグを使用して、パッケージのサービスプロバイダの `boot` メソッドで `courier` パッケージの 2 つの公開グループ (`courier-config` および `courier-migrations`) を定義してみましょう。

```
/**
 * Bootstrap any package services.
 *
 * @return void
 */
public function boot()
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishes([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}
```

<!-- Now your users may publish these groups separately by referencing their tag when executing the `vendor:publish` command: -->
これで、ユーザーは `vendor:publish` コマンドの実行時にタグを参照することで、これらのグループを個別に公開できるようになります。

```
php artisan vendor:publish --tag=courier-config
```

