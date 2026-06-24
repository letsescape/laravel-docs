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
> 모든 잠재적인 하위 호환성 깨짐(breaking change) 사항을 문서화하려고 노력했으나, 일부 사항은 Laravel의 잘 사용되지 않는 영역에 해당하므로 실제로 여러분의 애플리케이션에 영향을 주는 변경사항은 일부일 수 있습니다.

<a name="php-7.3.0-required"></a>
<!-- ### PHP 7.3.0 Required -->
### PHP 7.3.0 Required

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The new minimum PHP version is now 7.3.0. -->
Laravel 8.0에서 최소 지원 PHP 버전이 7.3.0으로 상향되었습니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- Update the following dependencies in your `composer.json` file: -->
`composer.json` 파일에서 아래 의존성들의 버전을 업데이트해야 합니다.

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
- `guzzlehttp/guzzle`를 `^7.0.1`로
- `facade/ignition`을 `^2.3.6`로
- `laravel/framework`를 `^8.0`로
- `laravel/ui`를 `^3.0`로
- `nunomaduro/collision`을 `^5.0`로
- `phpunit/phpunit`을 `^9.0`로

<!-- </div> -->
</div>

<!-- The following first-party packages have new major releases to support Laravel 8. If applicable, you should read their individual upgrade guides before upgrading: -->
Laravel 8을 지원하기 위해 주요 1st-party 패키지들도 새로운 메이저 릴리스를 제공합니다. 해당 패키지를 사용 중이라면, 업그레이드 전에 개별 업그레이드 가이드를 꼭 참고하시기 바랍니다.

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
또한, Laravel 인스톨러도 `composer create-project` 및 Laravel Jetstream을 지원하도록 업데이트되었습니다. 4.0 미만의 인스톨러는 2020년 10월 이후 동작하지 않으므로, 글로벌 인스톨러를 반드시 `^4.0` 버전 이상으로 업그레이드하시기 바랍니다.

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 8 support. -->
마지막으로, 애플리케이션에서 사용하는 다른 서드파티 패키지들도 Laravel 8과 호환되는 버전을 사용하는지 반드시 확인하세요.

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<a name="the-isset-method"></a>
<!-- #### The `isset` Method -->
#### The `isset` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- To be consistent with typical PHP behavior, the `offsetExists` method of `Illuminate\Support\Collection` has been updated to use `isset` instead of `array_key_exists`. This may present a change in behavior when dealing with collection items that have a value of `null`: -->
일반적인 PHP 동작과의 일관성을 위해, `Illuminate\Support\Collection`의 `offsetExists` 메서드는 이제 `array_key_exists` 대신 `isset`을 사용하도록 변경되었습니다. 이로 인해 값이 `null`인 컬렉션 아이템을 다룰 때 동작이 달라질 수 있습니다.

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
**영향 가능성: 높음**

<!-- Seeders and factories are now namespaced. To accommodate for these changes, add the `Database\Seeders` namespace to your seeder classes. In addition, the previous `database/seeds` directory should be renamed to `database/seeders`: -->
시더(Seeder)와 팩토리(Factory) 클래스가 이제 네임스페이스를 갖게 되었습니다. 이에 따라, 시더 클래스에는 `Database\Seeders` 네임스페이스를 추가해야 합니다. 또한, 기존의 `database/seeds` 디렉토리는 `database/seeders`로 이름을 변경해야 합니다.

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
`laravel/legacy-factories` 패키지를 사용하는 경우 팩토리 클래스는 변경할 필요가 없습니다. 그러나 팩토리를 업그레이드할 경우, 해당 클래스에 `Database\Factories` 네임스페이스를 추가해야 합니다.

<!-- Next, in your `composer.json` file, remove `classmap` block from the `autoload` section and add the new namespaced class directory mappings: -->
그리고 `composer.json` 파일의 `autoload` 섹션에서 `classmap` 블록을 삭제하고, 새 네임스페이스 기반 디렉토리 매핑을 추가해야 합니다.

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
**영향 가능성: 높음**

<!-- Laravel's [model factories](/docs/8.x/database-testing#defining-model-factories) feature has been totally rewritten to support classes and is not compatible with Laravel 7.x style factories. However, to ease the upgrade process, a new `laravel/legacy-factories` package has been created to continue using your existing factories with Laravel 8.x. You may install this package via Composer: -->
Laravel의 [model factories](/docs/8.x/database-testing#defining-model-factories) 기능이 클래스 기반으로 완전히 재작성되어, Laravel 7.x 스타일 팩토리와는 호환되지 않습니다. 업그레이드를 쉽게 하도록, 기존 팩토리를 계속 사용할 수 있는 `laravel/legacy-factories` 패키지가 제공됩니다. Composer로 아래와 같이 설치하세요:

```
composer require laravel/legacy-factories
```

<a name="the-castable-interface"></a>
<!-- #### The `Castable` Interface -->
#### The `Castable` Interface

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `castUsing` method of the `Castable` interface has been updated to accept an array of arguments. If you are implementing this interface you should update your implementation accordingly: -->
`Castable` 인터페이스의 `castUsing` 메서드는 이제 인수로 배열을 받도록 변경되었습니다. 해당 인터페이스를 직접 구현한다면, 아래와 같이 구현을 수정해야 합니다.

```
public static function castUsing(array $arguments);
```

<a name="increment-decrement-events"></a>
<!-- #### Increment / Decrement Events -->
#### Increment / Decrement Events

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Proper "update" and "save" related model events will now be dispatched when executing the `increment` or `decrement` methods on Eloquent model instances. -->
이제 Eloquent 모델 인스턴스에서 `increment`나 `decrement` 메서드를 실행할 경우, 올바른 "update" 및 "save" 관련 모델 이벤트가 디스패치됩니다.

<a name="events"></a>
<!-- ### Events -->
### Events

<a name="the-event-service-provider-class"></a>
<!-- #### The `EventServiceProvider` Class -->
#### The `EventServiceProvider` Class

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- If your `App\Providers\EventServiceProvider` class contains a `register` function, you should ensure that you call `parent::register` at the beginning of this method. Otherwise, your application's events will not be registered. -->
`App\Providers\EventServiceProvider` 클래스에 `register` 메서드가 구현되어 있다면, 이 메서드의 가장 처음에 반드시 `parent::register`를 호출해야 합니다. 그렇지 않을 경우 애플리케이션의 이벤트가 등록되지 않습니다.

<a name="the-dispatcher-contract"></a>
<!-- #### The `Dispatcher` Contract -->
#### The `Dispatcher` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `listen` method of the `Illuminate\Contracts\Events\Dispatcher` contract has been updated to make the `$listener` property optional. This change was made to support automatic detection of handled event types via reflection. If you are manually implementing this interface, you should update your implementation accordingly: -->
`Illuminate\Contracts\Events\Dispatcher` 인터페이스의 `listen` 메서드는 `$listener` 인수를 선택적으로 받도록 변경되었습니다. 이 변경은 리플렉션을 통한 이벤트 타입 자동 감지를 지원하기 위한 것입니다. 해당 인터페이스를 직접 구현할 경우, 아래와 같이 수정해야 합니다.

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
**영향 가능성: 선택적**

<!-- The [maintenance mode](/docs/8.x/configuration#maintenance-mode) feature of Laravel has been improved in Laravel 8.x. Pre-rendering the maintenance mode template is now supported and eliminates the chances of end users encountering errors during maintenance mode. However, to support this, the following lines must be added to your `public/index.php` file. These lines should be placed directly under the existing `LARAVEL_START` constant definition: -->
Laravel의 [maintenance mode](/docs/8.x/configuration#maintenance-mode)가 8.x에서 개선되었습니다. 유지 관리 모드 템플릿을 미리 렌더(pre-render)하는 기능이 추가되어, 유지 관리 도중 사용자에게 오류가 노출될 가능성이 줄어듭니다. 이를 위해서는 아래 코드 라인을 `public/index.php` 파일 내 `LARAVEL_START` 상수 정의문 바로 아래에 추가해야 합니다.

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
**영향 가능성: 중간**

<!-- The `--message` option of the `php artisan down` command has been removed. As an alternative, consider [pre-rendering your maintenance mode views](/docs/8.x/configuration#maintenance-mode) with the message of your choice. -->
`php artisan down` 명령어의 `--message` 옵션이 제거되었습니다. 대신, [pre-rendering your maintenance mode views](/docs/8.x/configuration#maintenance-mode)하는 방법을 참고하세요.

<a name="php-artisan-serve-no-reload-option"></a>
<!-- #### The `php artisan serve --no-reload` Option -->
#### The `php artisan serve --no-reload` Option

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- A `--no-reload` option has been added to the `php artisan serve` command. This will instruct the built-in server to not reload the server when environment file changes are detected. This option is primarily helpful when running Laravel Dusk tests in a CI environment. -->
`php artisan serve` 명령어에 `--no-reload` 옵션이 추가되었습니다. 이 옵션을 사용하면 환경 파일이 변경되어도 내장 서버가 재시작되지 않습니다. 주로 CI 환경에서 Laravel Dusk 테스트를 실행할 때 유용합니다.

<a name="manager-app-property"></a>
<!-- #### Manager `$app` Property -->
#### Manager `$app` Property

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The previously deprecated `$app` property of the `Illuminate\Support\Manager` class has been removed. If you were relying on this property, you should use the `$container` property instead. -->
`Illuminate\Support\Manager` 클래스의 예전 `$app` 프로퍼티가 완전히 제거되었습니다. 이 프로퍼티를 사용 중이었다면, 대신 `$container` 프로퍼티를 사용해야 합니다.

<a name="the-elixir-helper"></a>
<!-- #### The `elixir` Helper -->
#### The `elixir` Helper

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The previously deprecated `elixir` helper has been removed. Applications still using this method are encouraged to upgrade to [Laravel Mix](https://github.com/JeffreyWay/laravel-mix). -->
더 이상 사용되지 않는 `elixir` 헬퍼가 제거되었습니다. 이 메서드를 여전히 사용 중이라면, [Laravel Mix](https://github.com/JeffreyWay/laravel-mix)로 업그레이드하는 것을 권장합니다.

<a name="mail"></a>
<!-- ### Mail -->
### Mail

<a name="the-sendnow-method"></a>
<!-- #### The `sendNow` Method -->
#### The `sendNow` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The previously deprecated `sendNow` method has been removed. Instead, please use the `send` method. -->
이전부터 사용이 중단된 `sendNow` 메서드가 삭제되었습니다. 앞으로는 `send` 메서드를 사용하시기 바랍니다.

<a name="pagination"></a>
<!-- ### Pagination -->
### Pagination

<a name="pagination-defaults"></a>
<!-- #### Pagination Defaults -->
#### Pagination Defaults

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- The paginator now uses the [Tailwind CSS framework](https://tailwindcss.com) for its default styling. In order to keep using Bootstrap, you should add the following method call to the `boot` method of your application's `AppServiceProvider`: -->
페이지네이터의 기본 스타일이 [Tailwind CSS framework](https://tailwindcss.com)로 변경되었습니다. 만약 기존처럼 Bootstrap 스타일을 계속 쓰고 싶다면, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에 아래 메서드 호출을 추가하세요.

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
**영향 가능성: 높음**

<!-- For consistency with other features of Laravel, the `retryAfter` method and `retryAfter` property of queued jobs, mailers, notifications, and listeners have been renamed to `backoff`. You should update the name of this method / property in the relevant classes in your application. -->
Laravel의 기능들과 일관성을 맞추기 위해, 큐잉된 작업·메일러·알림·리스너에서 사용하던 `retryAfter` 메서드와 `retryAfter` 프로퍼티가 `backoff`로 이름이 변경되었습니다. 관련 클래스에서 해당 이름을 모두 수정해야 합니다.

<a name="queue-timeout-at-property"></a>
<!-- #### The `timeoutAt` Property -->
#### The `timeoutAt` Property

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- The `timeoutAt` property of queued jobs, notifications, and listeners has been renamed to `retryUntil`. You should update the name of this property in the relevant classes in your application. -->
큐에 등록된 작업, 알림, 리스너에서 사용하던 `timeoutAt` 프로퍼티가 `retryUntil`로 이름이 변경되었습니다. 해당 클래스의 프로퍼티 이름을 수정해 주세요.

<a name="queue-allOnQueue-allOnConnection"></a>
<!-- #### The `allOnQueue()` / `allOnConnection()` Methods -->
#### The `allOnQueue()` / `allOnConnection()` Methods

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- For consistency with other dispatching methods, the `allOnQueue()` and `allOnConnection()` methods used with job chaining have been removed. You may use the `onQueue()` and `onConnection()` methods instead. These methods should be called before calling the `dispatch` method: -->
작업 체이닝에서 사용되던 `allOnQueue()` 및 `allOnConnection()` 메서드는 제거되었습니다. 대신, `onQueue()`와 `onConnection()` 메서드를 사용해야 하며, 이들은 `dispatch` 메서드 호출 전에 사용해야 합니다.

```
ProcessPodcast::withChain([
    new OptimizePodcast,
    new ReleasePodcast
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<!-- Note that this change only affects code using the `withChain` method. The `allOnQueue()` and `allOnConnection()` are still available when using the global `dispatch()` helper. -->
이 변경은 `withChain` 메서드를 사용할 때만 해당합니다. 전역 `dispatch()` 헬퍼를 쓸 때는 기존의 `allOnQueue()`, `allOnConnection()`이 여전히 사용 가능합니다.

<a name="failed-jobs-table-batch-support"></a>
<!-- #### Failed Jobs Table Batch Support -->
#### Failed Jobs Table Batch Support

<!-- **Likelihood Of Impact: Optional** -->
**영향 가능성: 선택적**

<!-- If you plan to use the [job batching](/docs/8.x/queues#job-batching) features of Laravel 8.x, your `failed_jobs` database table will need to be updated. First, a new `uuid` column should be added to your table: -->
[job batching](/docs/8.x/queues#job-batching) 기능을 사용할 계획이라면, `failed_jobs` 데이터베이스 테이블을 아래와 같이 업데이트해야 합니다. 우선, 테이블에 새로운 `uuid` 컬럼을 추가하세요.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('failed_jobs', function (Blueprint $table) {
    $table->string('uuid')->after('id')->nullable()->unique();
});
```

<!-- Next, the `failed.driver` configuration option within your `queue` configuration file should be updated to `database-uuids`. -->
그리고 `queue` 설정 파일의 `failed.driver` 옵션을 `database-uuids`로 변경하세요.

<!-- In addition, you may wish to generate UUIDs for your existing failed jobs: -->
또한, 기존 실패한 작업에 대해서도 UUID를 부여하려면 아래 코드를 참고하세요.

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
**영향 가능성: 선택적**

<!-- In previous releases of Laravel, the `RouteServiceProvider` class contained a `$namespace` property with a value of `App\Http\Controllers`. The value of this property was used to automatically prefix controller route declarations and controller route URL generation such as when calling the `action` helper. -->
Laravel 이전 버전에서는 `RouteServiceProvider` 클래스에 `$namespace` 프로퍼티가 `App\Http\Controllers`로 지정되어 있었으며, 이 값이 컨트롤러 라우트 선언 및 `action` 헬퍼를 호출할 때처럼 URL 생성 시 자동으로 접두사로 붙었습니다.

<!-- In Laravel 8, this property is set to `null` by default. This allows your controller route declarations to use the standard PHP callable syntax, which provides better support for jumping to the controller class in many IDEs: -->
Laravel 8에서는 이 프로퍼티의 기본값이 `null`이 되었습니다. 이제 표준 PHP 콜러블(callable) 문법을 사용하여 라우트를 선언할 수 있으며, 이는 여러 IDE에서 컨트롤러 클래스를 쉽게 찾아갈 수 있는 장점이 있습니다.

```
use App\Http\Controllers\UserController;

// Using PHP callable syntax...
Route::get('/users', [UserController::class, 'index']);

// Using string syntax...
Route::get('/users', 'App\Http\Controllers\UserController@index');
```

<!-- In most cases, this won't impact applications that are being upgraded because your `RouteServiceProvider` will still contain the `$namespace` property with its previous value. However, if you upgrade your application by creating a brand new Laravel project, you may encounter this as a breaking change. -->
기본적으로, 업그레이드한 애플리케이션에는 기존 `RouteServiceProvider`의 `$namespace` 프로퍼티가 그대로 유지되어 큰 영향이 없지만, 신규 Laravel 프로젝트를 생성해 업그레이드할 경우에는 호환성 문제(구현의 변경점)를 만날 수 있습니다.

<!-- If you would like to continue using the original auto-prefixed controller routing, you can simply set the value of the `$namespace` property within your `RouteServiceProvider` and update the route registrations within the `boot` method to use the `$namespace` property: -->
기존 방식대로 자동 접두 네임스페이스를 계속 사용하려면 `RouteServiceProvider`의 `$namespace` 값을 지정하고, `boot` 메서드에서 라우트 등록 시 아래 예시처럼 `$namespace`를 적용하면 됩니다.

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
**영향 가능성: 낮음**

<!-- Laravel's dependency on `dragonmantank/cron-expression` has been updated from `2.x` to `3.x`. This should not cause any breaking change in your application unless you are interacting with the `cron-expression` library directly. If you are interacting with this library directly, please review its [change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md). -->
Laravel에서 사용하는 `dragonmantank/cron-expression` 패키지의 의존성이 `2.x`에서 `3.x`로 상향되었습니다. Laravel 내부 동작에는 영향을 주지 않으나 `cron-expression` 라이브러리와 직접 상호작용 중이라면 [change log](https://github.com/dragonmantank/cron-expression/blob/master/CHANGELOG.md)을 꼭 확인하세요.

<a name="session"></a>
<!-- ### Session -->
### Session

<a name="the-session-contract"></a>
<!-- #### The `Session` Contract -->
#### The `Session` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Contracts\Session\Session` contract has received a new `pull` method. If you are implementing this contract manually, you should update your implementation accordingly: -->
`Illuminate\Contracts\Session\Session` 인터페이스에 새로운 `pull` 메서드가 추가되었습니다. 이 인터페이스를 직접 구현한다면 아래 선언을 참고하여 구현을 추가해야 합니다.

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
**영향 가능성: 낮음**

<!-- The `decodeResponseJson` method that belongs to the `Illuminate\Testing\TestResponse` class no longer accepts any arguments. Please consider using the `json` method instead. -->
`Illuminate\Testing\TestResponse` 클래스의 `decodeResponseJson` 메서드는 더 이상 인수를 받을 수 없습니다. 대신 `json` 메서드 사용을 권장합니다.

<a name="assert-exact-json-method"></a>
<!-- #### The `assertExactJson` Method -->
#### The `assertExactJson` Method

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The `assertExactJson` method now requires numeric keys of compared arrays to match and be in the same order. If you would like to compare JSON against an array without requiring numerically keyed arrays to have the same order, you may use the `assertSimilarJson` method instead. -->
`assertExactJson` 메서드는 비교하는 배열의 숫자 키(key)까지 순서가 동일해야만 통과됩니다. 만약 순서가 달라도 상관없는 비교를 원한다면 `assertSimilarJson` 메서드를 사용하면 됩니다.

<a name="validation"></a>
<!-- ### Validation -->
### Validation

<a name="database-rule-connections"></a>
<!-- ### Database Rule Connections -->
### Database Rule Connections

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `unique` and `exists` rules will now respect the specified connection name (accessed via the model's `getConnectionName` method) of Eloquent models when performing queries. -->
`unique` 및 `exists` 유효성 검증 규칙이 쿼리 실행 시, Eloquent 모델의 `getConnectionName` 메서드로 지정된 연결명을 이제 올바르게 참조합니다.

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...8.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)에서 변경된 파일 역시 확인해보길 권장합니다. 많은 변경사항이 필수로 적용되진 않지만, 애플리케이션의 상태를 최신으로 유지하고 싶을 수 있습니다. 이 가이드에서 다루지 않는 설정 파일이나 주석, 기타 변경점도 있으니, [GitHub comparison tool](https://github.com/laravel/laravel/compare/7.x...8.x)로 직접 비교하며 필요한 사항을 반영하는 것이 좋습니다.
