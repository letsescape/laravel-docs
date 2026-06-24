<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 8.0 From 7.x](#upgrade-8.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Model Factories](#model-factories)
- [Queue `retryAfter` Method](#queue-retry-after-method)
- [Queue `timeoutAt` Property](#queue-timeout-at-property)
- [Queue `allOnQueue` and `allOnConnection`](#queue-allOnQueue-allOnConnection)
- [Pagination Defaults](#pagination-defaults)
- [Seeder & Factory Namespaces](#seeder-factory-namespaces)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [PHP 7.3.0 Required](#php-7.3.0-required)
- [Failed Jobs Table Batch Support](#failed-jobs-table-batch-support)
- [Maintenance Mode Updates](#maintenance-mode-updates)
- [The `php artisan down --message` Option](#artisan-down-message)
- [The `assertExactJson` Method](#assert-exact-json-method)

<!-- </div> -->
</div>

<a name="upgrade-8.0"></a>
<!-- ## Upgrading To 8.0 From 7.x -->
## Upgrading To 8.0 From 7.x

<a name="estimated-upgrade-time-15-minutes"></a>
<!-- #### Estimated Upgrade Time: 15 Minutes -->
#### Estimated Upgrade Time: 15 Minutes

> [!NOTE]
> 私たちは、考えられるすべての重大な変更を文書化するよう努めています。これらの重大な変更の一部はフレームワークのあいまいな部分にあるため、実際にアプリケーションに影響を与える可能性があるのは、これらの変更の一部だけです。

<a name="php-7.3.0-required"></a>
<!-- ### PHP 7.3.0 Required -->
### PHP 7.3.0 Required

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The new minimum PHP version is now 7.3.0. -->
新しい PHP の最小バージョンは 7.3.0 になりました。

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- Update the following dependencies in your `composer.json` file: -->
`composer.json` ファイル内の次の依存関係を更新します。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `guzzlehttp/guzzle` to `^7.0.1`
- `facade/ignition` to `^2.3.6`
- `laravel/framework` to `^8.0`
- `laravel/ui` to `^3.0`
- `nunomaduro/collision` to `^5.0`
- `phpunit/phpunit` to `^9.0`
-->
- `guzzlehttp/guzzle` ～ `^7.0.1`
- `facade/ignition` ～ `^2.3.6`
- `laravel/framework` ～ `^8.0`
- `laravel/ui` ～ `^3.0`
- `nunomaduro/collision` ～ `^5.0`
- `phpunit/phpunit` ～ `^9.0`

<!-- </div> -->
</div>

<!-- The following first-party packages have new major releases to support Laravel 8. If applicable, you should read their individual upgrade guides before upgrading: -->
次のファーストパーティ パッケージには、Laravel 8 をサポートするための新しいメジャー リリースがあります。該当する場合は、アップグレードする前に、それぞれの個別のアップグレード ガイドを読む必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Horizon v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)
-->
- [Horizon v5.0](https://github.com/laravel/horizon/blob/master/UPGRADE.md)
- [Passport v10.0](https://github.com/laravel/passport/blob/master/UPGRADE.md)
- [Socialite v5.0](https://github.com/laravel/socialite/blob/master/UPGRADE.md)
- [Telescope v4.0](https://github.com/laravel/telescope/blob/master/UPGRADE.md)

<!-- </div> -->
</div>

<!-- In addition, the Laravel installer has been updated to support `composer create-project` and Laravel Jetstream. Any installer older than 4.0 will cease to work after October 2020. You should upgrade your global installer to `^4.0` as soon as possible. -->
さらに、Laravel インストーラーは、`composer create-project` と Laravel Jetstream をサポートするように更新されました。 4.0 より古いインストーラーは、2020 年 10 月以降機能しなくなります。できるだけ早くグローバル インストーラーを `^4.0` にアップグレードする必要があります。

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 8 support. -->
最後に、アプリケーションで使用される他のサードパーティパッケージを調べて、Laravel 8 をサポートする適切なバージョンを使用していることを確認します。

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<a name="the-isset-method"></a>
<!-- #### The `isset` Method -->
#### The `isset` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- To be consistent with typical PHP behavior, the `offsetExists` method of `Illuminate\Support\Collection` has been updated to use `isset` instead of `array_key_exists`. This may present a change in behavior when dealing with collection items that have a value of `null`: -->
一般的な PHP の動作と一致させるために、`Illuminate\Support\Collection` の `offsetExists` メソッドは、`array_key_exists` の代わりに `isset` を使用するように更新されました。これにより、`null` の値を持つコレクション項目を処理するときの動作が変わる可能性があります。

```
$collection = collect([null]);

// Laravel 7.x - true
isset($collection[0]);

// Laravel 8.x - false
isset($collection[0]);
```

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="seeder-factory-namespaces"></a>
<!-- #### Seeder & Factory Namespaces -->
#### Seeder & Factory Namespaces

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Seeders and factories are now namespaced. To accommodate for these changes, add the `Database\Seeders` namespace to your seeder classes. In addition, the previous `database/seeds` directory should be renamed to `database/seeders`: -->
シーダーとファクトリーには名前空間が設定されるようになりました。これらの変更に対応するには、`Database\Seeders` 名前空間をシーダー クラスに追加します。さらに、以前の `database/seeds` ディレクトリの名前を `database/seeders` に変更する必要があります。

```
<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        ...
    }
}
```

<!-- If you are choosing to use the `laravel/legacy-factories` package, no changes to your factory classes are required. However, if you are upgrading your factories, you should add the `Database\Factories` namespace to those classes. -->
`laravel/legacy-factories` パッケージの使用を選択した場合、ファクトリ クラスを変更する必要はありません。ただし、ファクトリーをアップグレードする場合は、それらのクラスに `Database\Factories` 名前空間を追加する必要があります。

<!-- Next, in your `composer.json` file, remove `classmap` block from the `autoload` section and add the new namespaced class directory mappings: -->
次に、`composer.json` ファイルで、`autoload` セクションから `classmap` ブロックを削除し、新しい名前空間クラスのディレクトリ マッピングを追加します。

```
"autoload": {
    "psr-4": {
        "App\\": "app/",
        "Database\\Factories\\": "database/factories/",
        "Database\\Seeders\\": "database/seeders/"
    }
},
```

<a name="eloquent"></a>
<!-- ### Eloquent -->
### Eloquent

<a name="model-factories"></a>
<!-- #### Model Factories -->
#### Model Factories

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- Laravel's [model factories](/docs/8.x/database-testing#defining-model-factories) feature has been totally rewritten to support classes and is not compatible with Laravel 7.x style factories. However, to ease the upgrade process, a new `laravel/legacy-factories` package has been created to continue using your existing factories with Laravel 8.x. You may install this package via Composer: -->
Laravel の [model factories](/docs/8.x/database-testing#defining-model-factories) 機能はクラスをサポートするために完全に書き直されており、Laravel 7.x スタイルのファクトリーとは互換性がありません。ただし、アップグレードプロセスを容易にするために、Laravel 8.x で既存のファクトリーを引き続き使用できるように、新しい `laravel/legacy-factories` パッケージが作成されました。このパッケージは Composer 経由でインストールできます。

```
composer require laravel/legacy-factories
```

<a name="the-castable-interface"></a>
<!-- #### The `Castable` Interface -->
#### The `Castable` Interface

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `castUsing` method of the `Castable` interface has been updated to accept an array of arguments. If you are implementing this interface you should update your implementation accordingly: -->
`Castable` インターフェイスの `castUsing` メソッドが、引数の配列を受け入れるように更新されました。このインターフェースを実装している場合は、それに応じて実装を更新する必要があります。

```
public static function castUsing(array $arguments);
```

<a name="increment-decrement-events"></a>
<!-- #### Increment / Decrement Events -->
#### Increment / Decrement Events

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Proper "update" and "save" related model events will now be dispatched when executing the `increment` or `decrement` methods on Eloquent model instances. -->
Eloquent モデル インスタンスで `increment` メソッドまたは `decrement` メソッドを実行するときに、適切な「更新」および「保存」関連のモデル イベントが送出されるようになりました。

<a name="events"></a>
<!-- ### Events -->
### Events

<a name="the-event-service-provider-class"></a>
<!-- #### The `EventServiceProvider` Class -->
#### The `EventServiceProvider` Class

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- If your `App\Providers\EventServiceProvider` class contains a `register` function, you should ensure that you call `parent::register` at the beginning of this method. Otherwise, your application's events will not be registered. -->
`App\Providers\EventServiceProvider` クラスに `register` 関数が含まれている場合は、このメソッドの先頭で `parent::register` を必ず呼び出す必要があります。そうしないと、アプリケーションのイベントは登録されません。

<a name="the-dispatcher-contract"></a>
<!-- #### The `Dispatcher` Contract -->
#### The `Dispatcher` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `listen` method of the `Illuminate\Contracts\Events\Dispatcher` contract has been updated to make the `$listener` property optional. This change was made to support automatic detection of handled event types via reflection. If you are manually implementing this interface, you should update your implementation accordingly: -->
`Illuminate\Contracts\Events\Dispatcher` コントラクトの `listen` メソッドが更新され、`$listener` プロパティがオプションになりました。この変更は、リフレクションによる処理されたイベント タイプの自動検出をサポートするために行われました。このインターフェースを手動で実装している場合は、それに応じて実装を更新する必要があります。

```
public function listen($events, $listener = null);
```

<a name="framework"></a>
<!-- ### Framework -->
### Framework

<a name="maintenance-mode-updates"></a>
<!-- #### Maintenance Mode Updates -->
#### Maintenance Mode Updates

<!-- **Likelihood Of Impact: Optional** -->
**影響の可能性: オプション**

<!-- The [maintenance mode](/docs/8.x/configuration#maintenance-mode) feature of Laravel has been improved in Laravel 8.x. Pre-rendering the maintenance mode template is now supported and eliminates the chances of end users encountering errors during maintenance mode. However, to support this, the following lines must be added to your `public/index.php` file. These lines should be placed directly under the existing `LARAVEL_START` constant definition: -->
Laravel の [maintenance mode](/docs/8.x/configuration#maintenance-mode) 機能は、Laravel 8.x で改善されました。メンテナンス モード テンプレートの事前レンダリングがサポートされるようになり、メンテナンス モード中にエンド ユーザーがエラーに遭遇する可能性がなくなりました。ただし、これをサポートするには、`public/index.php` ファイルに次の行を追加する必要があります。これらの行は、既存の `LARAVEL_START` 定数定義の直下に配置する必要があります。

```
define('LARAVEL_START', microtime(true));

if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
    require $maintenance;
}
```

<a name="artisan-down-message"></a>
<!-- #### The `php artisan down --message` Option -->
#### The `php artisan down --message` Option

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `--message` option of the `php artisan down` command has been removed. As an alternative, consider [pre-rendering your maintenance mode views](/docs/8.x/configuration#maintenance-mode) with the message of your choice. -->
`php artisan down` コマンドの `--message` オプションは削除されました。代わりに、選択したメッセージを含む [pre-rendering your maintenance mode views](/docs/8.x/configuration#maintenance-mode) を検討してください。

<a name="php-artisan-serve-no-reload-option"></a>
<!-- #### The `php artisan serve --no-reload` Option -->
#### The `php artisan serve --no-reload` Option

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- A `--no-reload` option has been added to the `php artisan serve` command. This will instruct the built-in server to not reload the server when environment file changes are detected. This option is primarily helpful when running Laravel Dusk tests in a CI environment. -->
`--no-reload` オプションが `php artisan serve` コマンドに追加されました。これにより、環境ファイルの変更が検出されたときにサーバーをリロードしないように組み込みサーバーに指示されます。このオプションは主に、CI 環境で Laravel Dusk テストを実行する場合に役立ちます。

<a name="manager-app-property"></a>
<!-- #### Manager `$app` Property -->
#### Manager `$app` Property

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The previously deprecated `$app` property of the `Illuminate\Support\Manager` class has been removed. If you were relying on this property, you should use the `$container` property instead. -->
以前に非推奨となった `Illuminate\Support\Manager` クラスの `$app` プロパティは削除されました。このプロパティに依存していた場合は、代わりに `$container` プロパティを使用する必要があります。

<a name="the-elixir-helper"></a>
<!-- #### The `elixir` Helper -->
#### The `elixir` Helper

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The previously deprecated `elixir` helper has been removed. Applications still using this method are encouraged to upgrade to [Laravel Mix](https://github.com/JeffreyWay/laravel-mix). -->
以前に非推奨となった `elixir` ヘルパは削除されました。この方法をまだ使用しているアプリケーションは、[Laravel Mix](https://github.com/JeffreyWay/laravel-mix) にアップグレードすることをお勧めします。

<a name="mail"></a>
<!-- ### Mail -->
### Mail

<a name="the-sendnow-method"></a>
<!-- #### The `sendNow` Method -->
#### The `sendNow` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The previously deprecated `sendNow` method has been removed. Instead, please use the `send` method. -->
以前に非推奨となった `sendNow` メソッドは削除されました。代わりに、`send` メソッドを使用してください。

<a name="pagination"></a>
<!-- ### Pagination -->
### Pagination

<a name="pagination-defaults"></a>
<!-- #### Pagination Defaults -->
#### Pagination Defaults

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- The paginator now uses the [Tailwind CSS framework](https://tailwindcss.com) for its default styling. In order to keep using Bootstrap, you should add the following method call to the `boot` method of your application's `AppServiceProvider`: -->
ページネータはデフォルトのスタイルに [Tailwind CSS framework](https://tailwindcss.com) を使用するようになりました。ブートストラップを引き続き使用するには、アプリケーションの `AppServiceProvider` の `boot` メソッドに次のメソッド呼び出しを追加する必要があります。

```
use Illuminate\Pagination\Paginator;

Paginator::useBootstrap();
```

<a name="queue"></a>
<!-- ### Queue -->
### Queue

<a name="queue-retry-after-method"></a>
<!-- #### The `retryAfter` Method -->
#### The `retryAfter` Method

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- For consistency with other features of Laravel, the `retryAfter` method and `retryAfter` property of queued jobs, mailers, notifications, and listeners have been renamed to `backoff`. You should update the name of this method / property in the relevant classes in your application. -->
Laravel の他の機能との一貫性を保つために、キューに入れられたジョブ、メーラー、通知、リスナの `retryAfter` メソッドと `retryAfter` プロパティの名前が `backoff` に変更されました。アプリケーションの関連クラスでこのメソッド/プロパティの名前を更新する必要があります。

<a name="queue-timeout-at-property"></a>
<!-- #### The `timeoutAt` Property -->
#### The `timeoutAt` Property

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- The `timeoutAt` property of queued jobs, notifications, and listeners has been renamed to `retryUntil`. You should update the name of this property in the relevant classes in your application. -->
キューに入れられたジョブ、通知、およびリスナの `timeoutAt` プロパティの名前が `retryUntil` に変更されました。アプリケーションの関連クラスでこのプロパティの名前を更新する必要があります。

<a name="queue-allOnQueue-allOnConnection"></a>
<!-- #### The `allOnQueue()` / `allOnConnection()` Methods -->
#### The `allOnQueue()` / `allOnConnection()` Methods

<!-- **Likelihood Of Impact: High** -->
**影響の可能性: 高**

<!-- For consistency with other dispatching methods, the `allOnQueue()` and `allOnConnection()` methods used with job chaining have been removed. You may use the `onQueue()` and `onConnection()` methods instead. These methods should be called before calling the `dispatch` method: -->
他のディスパッチ方法との一貫性を保つために、ジョブ チェーンで使用される `allOnQueue()` メソッドと `allOnConnection()` メソッドは削除されました。代わりに、`onQueue()` メソッドと `onConnection()` メソッドを使用することもできます。これらのメソッドは、`dispatch` メソッドを呼び出す前に呼び出す必要があります。

```
ProcessPodcast::withChain([
    new OptimizePodcast,
    new ReleasePodcast
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<!-- Note that this change only affects code using the `withChain` method. The `allOnQueue()` and `allOnConnection()` are still available when using the global `dispatch()` helper. -->
この変更は、`withChain` メソッドを使用するコードにのみ影響することに注意してください。グローバル `dispatch()` ヘルパを使用する場合、`allOnQueue()` および `allOnConnection()` は引き続き使用できます。

<a name="failed-jobs-table-batch-support"></a>
<!-- #### Failed Jobs Table Batch Support -->
#### Failed Jobs Table Batch Support

<!-- **Likelihood Of Impact: Optional** -->
**影響の可能性: オプション**

<!-- If you plan to use the [job batching](/docs/8.x/queues#job-batching) features of Laravel 8.x, your `failed_jobs` database table will need to be updated. First, a new `uuid` column should be added to your table: -->
Laravel 8.x の [job batching](/docs/8.x/queues#job-batching) 機能を使用する場合は、`failed_jobs` データベース テーブルを更新する必要があります。まず、新しい `uuid` 列をテーブルに追加する必要があります。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('failed_jobs', function (Blueprint $table) {
    $table->string('uuid')->after('id')->nullable()->unique();
});
```

<!-- Next, the `failed.driver` configuration option within your `queue` configuration file should be updated to `database-uuids`. -->
次に、`queue` 構成ファイル内の `failed.driver` 構成オプションを `database-uuids` に更新する必要があります。

<!-- In addition, you may wish to generate UUIDs for your existing failed jobs: -->
さらに、失敗した既存のジョブの UUID を生成することもできます。

```
DB::table('failed_jobs')->whereNull('uuid')->cursor()->each(function ($job) {
    DB::table('failed_jobs')
        ->where('id', $job->id)
        ->update(['uuid' => (string) Illuminate\Support\Str::uuid()]);
});
```

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<a name="automatic-controller-namespace-prefixing"></a>
<!-- #### Automatic Controller Namespace Prefixing -->
#### Automatic Controller Namespace Prefixing

<!-- **Likelihood Of Impact: Optional** -->
**影響の可能性: オプション**

<!-- In previous releases of Laravel, the `RouteServiceProvider` class contained a `$namespace` property with a value of `App\Http\Controllers`. The value of this property was used to automatically prefix controller route declarations and controller route URL generation such as when calling the `action` helper. -->
Laravel の以前のリリースでは、`RouteServiceProvider` クラスには、値 `App\Http\Controllers` を持つ `$namespace` プロパティが含まれていました。このプロパティの値は、`action` ヘルパを呼び出すときなど、コントローラ ルート宣言とコントローラ ルート URL生成に自動的にプレフィックスを付けるために使用されていました。

<!-- In Laravel 8, this property is set to `null` by default. This allows your controller route declarations to use the standard PHP callable syntax, which provides better support for jumping to the controller class in many IDEs: -->
Laravel 8 では、このプロパティはデフォルトで `null` に設定されます。これにより、コントローラのルート宣言で標準の PHP 呼び出し可能構文を使用できるようになり、多くの IDE でコントローラ クラスへのジャンプのサポートが強化されます。

```
use App\Http\Controllers\UserController;

// Using PHP callable syntax...
Route::get('/users', [UserController::class, 'index']);

// Using string syntax...
Route::get('/users', 'App\Http\Controllers\UserController@index');
```

<!-- In most cases, this won't impact applications that are being upgraded because your `RouteServiceProvider` will still contain the `$namespace` property with its previous value. However, if you upgrade your application by creating a brand new Laravel project, you may encounter this as a breaking change. -->
ほとんどの場合、`RouteServiceProvider` には以前の値の `$namespace` プロパティが含まれているため、アップグレード中のアプリケーションには影響しません。ただし、新しい Laravel プロジェクトを作成してアプリケーションをアップグレードする場合、これは重大な変更として発生する可能性があります。

<!-- If you would like to continue using the original auto-prefixed controller routing, you can simply set the value of the `$namespace` property within your `RouteServiceProvider` and update the route registrations within the `boot` method to use the `$namespace` property: -->
元の自動プレフィックス付きコントローラ ルーティングを引き続き使用したい場合は、`RouteServiceProvider` 内の `$namespace` プロパティの値を設定し、`boot` メソッド内のルート登録を更新して、`$namespace` プロパティを使用することができます。

```
class RouteServiceProvider extends ServiceProvider
{
    /**
     * The path to the "home" route for your application.
     *
     * This is used by Laravel authentication to redirect users after login.
     *
     * @var string
     */
    public const HOME = '/home';

    /**
     * If specified, this namespace is automatically applied to your controller routes.
     *
     * In addition, it is set as the URL generator's root namespace.
     *
     * @var string
     */
    protected $namespace = 'App\Http\Controllers';

    /**
     * Define your route model bindings, pattern filters, etc.
     *
     * @return void
     */
    public function boot()
    {
        $this->configureRateLimiting();

        $this->routes(function () {
            Route::middleware('web')
                ->namespace($this->namespace)
                ->group(base_path('routes/web.php'));

            Route::prefix('api')
                ->middleware('api')
                ->namespace($this->namespace)
                ->group(base_path('routes/api.php'));
        });
    }

    /**
     * Configure the rate limiters for the application.
     *
     * @return void
     */
    protected function configureRateLimiting()
    {
        RateLimiter::for('api', function (Request $request) {
            return Limit::perMinute(60)->by(optional($request->user())->id ?: $request->ip());
        });
    }
}
```

<a name="scheduling"></a>
<!-- ### Scheduling -->
### Scheduling

<a name="the-cron-expression-library"></a>
<!-- #### The `cron-expression` Library -->
#### The `cron-expression` Library

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- Laravel's dependency on `dragonmantank/cron-expression` has been updated from `2.x` to `3.x`. This should not cause any breaking change in your application unless you are interacting with the `cron-expression` library directly. If you are interacting with this library directly, please review its [change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md). -->
Laravel の `dragonmantank/cron-expression` への依存関係が `2.x` から `3.x` に更新されました。 `cron-expression` ライブラリを直接操作しない限り、これによってアプリケーションに重大な変更が生じることはありません。このライブラリを直接操作している場合は、[change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md) を確認してください。

<a name="session"></a>
<!-- ### Session -->
### Session

<a name="the-session-contract"></a>
<!-- #### The `Session` Contract -->
#### The `Session` Contract

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `Illuminate\Contracts\Session\Session` contract has received a new `pull` method. If you are implementing this contract manually, you should update your implementation accordingly: -->
`Illuminate\Contracts\Session\Session` コントラクトは、新しい `pull` メソッドを受け取りました。このコントラクトを手動で実装している場合は、それに応じて実装を更新する必要があります。

```
/**
 * Get the value of a given key and then forget it.
 *
 * @param  string  $key
 * @param  mixed  $default
 * @return mixed
 */
public function pull($key, $default = null);
```

<a name="testing"></a>
<!-- ### Testing -->
### Testing

<a name="decode-response-json-method"></a>
<!-- #### The `decodeResponseJson` Method -->
#### The `decodeResponseJson` Method

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `decodeResponseJson` method that belongs to the `Illuminate\Testing\TestResponse` class no longer accepts any arguments. Please consider using the `json` method instead. -->
`Illuminate\Testing\TestResponse` クラスに属する `decodeResponseJson` メソッドは引数を受け入れなくなりました。代わりに、`json` メソッドの使用を検討してください。

<a name="assert-exact-json-method"></a>
<!-- #### The `assertExactJson` Method -->
#### The `assertExactJson` Method

<!-- **Likelihood Of Impact: Medium** -->
**影響の可能性: 中**

<!-- The `assertExactJson` method now requires numeric keys of compared arrays to match and be in the same order. If you would like to compare JSON against an array without requiring numerically keyed arrays to have the same order, you may use the `assertSimilarJson` method instead. -->
`assertExactJson` メソッドでは、比較される配列の数値キーが一致し、同じ順序であることが必要になりました。数値キー付き配列の順序を同じにすることなく、JSON を配列と比較したい場合は、代わりに `assertSimilarJson` メソッドを使用できます。

<a name="validation"></a>
<!-- ### Validation -->
### Validation

<a name="database-rule-connections"></a>
<!-- ### Database Rule Connections -->
### Database Rule Connections

<!-- **Likelihood Of Impact: Low** -->
**影響の可能性: 低い**

<!-- The `unique` and `exists` rules will now respect the specified connection name (accessed via the model's `getConnectionName` method) of Eloquent models when performing queries. -->
`unique` ルールと `exists` ルールは、クエリを実行するときに Eloquent モデルの指定された接続名 (モデルの `getConnectionName` メソッドを介してアクセスされる) を尊重するようになりました。

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...8.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel) の変更内容も確認することをお勧めします。これらの変更の多くは必要ありませんが、これらのファイルをアプリケーションと同期させておきたい場合があります。これらの変更の一部はこのアップグレード ガイドで説明されますが、構成ファイルやコメントへの変更などのその他の変更については説明されません。 [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...8.x) を使用して変更を簡単に表示し、どの更新が自分にとって重要かを選択できます。

