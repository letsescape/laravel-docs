<!-- # Laravel Pennant -->
# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Defining Features](#defining-features)
    - [Class Based Features](#class-based-features)
- [Checking Features](#checking-features)
    - [Conditional Execution](#conditional-execution)
    - [The `HasFeatures` Trait](#the-has-features-trait)
    - [Blade Directive](#blade-directive)
    - [Middleware](#middleware)
    - [Intercepting Feature Checks](#intercepting-feature-checks)
    - [In-Memory Cache](#in-memory-cache)
- [Scope](#scope)
    - [Specifying the Scope](#specifying-the-scope)
    - [Default Scope](#default-scope)
    - [Nullable Scope](#nullable-scope)
    - [Identifying Scope](#identifying-scope)
    - [Serializing Scope](#serializing-scope)
- [Rich Feature Values](#rich-feature-values)
- [Retrieving Multiple Features](#retrieving-multiple-features)
- [Eager Loading](#eager-loading)
- [Updating Values](#updating-values)
    - [Bulk Updates](#bulk-updates)
    - [Purging Features](#purging-features)
- [Testing](#testing)
- [Adding Custom Pennant Drivers](#adding-custom-pennant-drivers)
    - [Implementing the Driver](#implementing-the-driver)
    - [Registering the Driver](#registering-the-driver)
    - [Defining Features Externally](#defining-features-externally)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pennant](https://github.com/laravel/pennant) is a simple and light-weight feature flag package - without the cruft. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, complement a trunk-based development strategy, and much more. -->
[Laravel Pennant](https://github.com/laravel/pennant) は、無駄のない、シンプルで軽量な機能フラグ パッケージです。機能フラグを使用すると、新しいアプリケーション機能を自信を持って段階的にロールアウトしたり、新しいインターフェイス設計の A/B テストを行ったり、トランクベースの開発戦略を補完したりすることができます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Pennant into your project using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して、Pennant をプロジェクトにインストールします。

```shell
composer require laravel/pennant
```

<!-- Next, you should publish the Pennant configuration and migration files using the `vendor:publish` Artisan command: -->
次に、`vendor:publish` Artisan コマンドを使用して、Pennant構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

<!-- Finally, you should run your application's database migrations. This will create a `features` table that Pennant uses to power its `database` driver: -->
最後に、アプリケーションのデータベース移行を実行する必要があります。これにより、Pennant が `database` ドライバを駆動するために使用する `features` テーブルが作成されます。

```shell
php artisan migrate
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to specify the default storage mechanism that will be used by Pennant to store resolved feature flag values. -->
Pennant のアセットを公開すると、その構成ファイルは `config/pennant.php` に配置されます。この構成ファイルを使用すると、解決された機能フラグ値を保存するためにPennant が使用するデフォルトのストレージ メカニズムを指定できます。

<!-- Pennant includes support for storing resolved feature flag values in an in-memory array via the `array` driver. Or, Pennant can store resolved feature flag values persistently in a relational database via the `database` driver, which is the default storage mechanism used by Pennant. -->
Pennant には、`array` ドライバを介して、解決された機能フラグ値をメモリ内配列に保存するためのサポートが含まれています。または、Pennant は、Pennant が使用するデフォルトのストレージ メカニズムである `database` ドライバを介して、解決された機能フラグ値をリレーショナル データベースに永続的に保存できます。

<a name="defining-features"></a>
<!-- ## Defining Features -->
## Defining Features

<!-- To define a feature, you may use the `define` method offered by the `Feature` facade. You will need to provide a name for the feature, as well as a closure that will be invoked to resolve the feature's initial value. -->
機能を定義するには、`Feature` ファサードによって提供される `define` メソッドを使用できます。機能の名前と、機能の初期値を解決するために呼び出されるクロージャを指定する必要があります。

<!-- Typically, features are defined in a service provider using the `Feature` facade. The closure will receive the "scope" for the feature check. Most commonly, the scope is the currently authenticated user. In this example, we will define a feature for incrementally rolling out a new API to our application's users: -->
通常、機能は `Feature` ファサードを使用してサービスプロバイダで定義されます。クロージャーは機能チェックの「スコープ」を受け取ります。最も一般的には、スコープは現在認証されているユーザーです。この例では、アプリケーションのユーザーに新しい API を段階的にロールアウトするための機能を定義します。

```php
<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Support\Lottery;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', fn (User $user) => match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        });
    }
}
```

<!-- As you can see, we have the following rules for our feature: -->
ご覧のとおり、この機能には次のルールがあります。

<!--
- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise, the feature should be randomly assigned to users with a 1 in 100 chance of being active.
-->
- すべての内部チーム メンバーは新しい API を使用する必要があります。
- トラフィック量の多い顧客は、新しい API を使用しないでください。
- それ以外の場合、機能は 100 分の 1 の確率でアクティブになるユーザーにランダムに割り当てられる必要があります。

<!-- The first time the `new-api` feature is checked for a given user, the result of the closure will be stored by the storage driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the closure will not be invoked. -->
特定のユーザーに対して初めて `new-api` 機能がチェックされると、クロージャーの結果がストレージ ドライバによって保存されます。次回この機能が同じユーザーに対してチェックされるとき、値はストレージから取得され、クロージャは呼び出されません。

<!-- For convenience, if a feature definition only returns a lottery, you may omit the closure completely: -->
便宜上、機能定義が Lottery のみを返す場合は、クロージャーを完全に省略できます。

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
<!-- ### Class Based Features -->
### Class Based Features

<!-- Pennant also allows you to define class-based features. Unlike closure-based feature definitions, there is no need to register a class-based feature in a service provider. To create a class-based feature, you may invoke the `pennant:feature` Artisan command. By default, the feature class will be placed in your application's `app/Features` directory: -->
Pennant では、クラスベースの機能を定義することもできます。クロージャベースの機能定義とは異なり、サービスプロバイダにクラスベースの機能を登録する必要はありません。クラスベースのフィーチャーを作成するには、`pennant:feature` Artisan コマンドを呼び出します。デフォルトでは、フィーチャクラスはアプリケーションの `app/Features` ディレクトリに配置されます。

```shell
php artisan pennant:feature NewApi
```

<!-- When writing a feature class, you only need to define a `resolve` method, which will be invoked to resolve the feature's initial value for a given scope. Again, the scope will typically be the currently authenticated user: -->
フィーチャクラスを作成する場合、`resolve` メソッドを定義するだけで済みます。このメソッドは、指定されたスコープのフィーチャの初期値を解決するために呼び出されます。繰り返しますが、スコープは通常、現在認証されているユーザーになります。

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

<!-- If you would like to manually resolve an instance of a class-based feature, you may invoke the `instance` method on the `Feature` facade: -->
クラスベースの機能のインスタンスを手動で解決したい場合は、`Feature` ファサードで `instance` メソッドを呼び出すことができます。

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> フィーチャクラスは [container](/docs/13.x/container) 経由で解決されるため、必要に応じてフィーチャクラスのコンストラクターに依存関係を注入できます。

<!-- #### Customizing the Stored Feature Name -->
#### Customizing the Stored Feature Name

<!-- By default, Pennant will store the feature class's fully qualified class name. If you would like to decouple the stored feature name from the application's internal structure, you may add the `Name` attribute on the feature class. The value of this attribute will be stored in place of the class name: -->
デフォルトでは、Pennant はフィーチャクラスの完全修飾クラス名を保存します。保存されたフィーチャ名をアプリケーションの内部構造から分離したい場合は、フィーチャクラスに `Name` 属性を追加できます。この属性の値はクラス名の代わりに保存されます。

```php
<?php

namespace App\Features;

use Laravel\Pennant\Attributes\Name;

#[Name('new-api')]
class NewApi
{
    // ...
}
```

<a name="checking-features"></a>
<!-- ## Checking Features -->
## Checking Features

<!-- To determine if a feature is active, you may use the `active` method on the `Feature` facade. By default, features are checked against the currently authenticated user: -->
機能がアクティブかどうかを確認するには、`Feature` ファサードで `active` メソッドを使用できます。デフォルトでは、現在認証されているユーザーに対して機能がチェックされます。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active('new-api')
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

<!-- Although features are checked against the currently authenticated user by default, you may easily check the feature against another user or [scope](#scope). To accomplish this, use the `for` method offered by the `Feature` facade: -->
デフォルトでは、現在認証されているユーザーに対して機能がチェックされますが、別のユーザーまたは [scope](#scope) に対して機能を簡単にチェックできます。これを実現するには、`Feature` ファサードによって提供される `for` メソッドを使用します。

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

<!-- Pennant also offers some additional convenience methods that may prove useful when determining if a feature is active or not: -->
Pennant には、機能がアクティブかどうかを判断するときに便利な追加のメソッドも用意されています。

```php
// Determine if all of the given features are active...
Feature::allAreActive(['new-api', 'site-redesign']);

// Determine if any of the given features are active...
Feature::someAreActive(['new-api', 'site-redesign']);

// Determine if a feature is inactive...
Feature::inactive('new-api');

// Determine if all of the given features are inactive...
Feature::allAreInactive(['new-api', 'site-redesign']);

// Determine if any of the given features are inactive...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan コマンドやキューに入れられたジョブなど、HTTP コンテキストの外部でPennant を使用する場合は、通常、[explicitly specify the feature's scope](#specifying-the-scope) を使用する必要があります。あるいは、認証された HTTP コンテキストと未認証のコンテキストの両方を考慮した [default scope](#default-scope) を定義することもできます。

<a name="checking-class-based-features"></a>
<!-- #### Checking Class Based Features -->
#### Checking Class Based Features

<!-- For class-based features, you should provide the class name when checking the feature: -->
クラスベースの機能の場合、機能を確認するときにクラス名を指定する必要があります。

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active(NewApi::class)
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```

<a name="conditional-execution"></a>
<!-- ### Conditional Execution -->
### Conditional Execution

<!-- The `when` method may be used to fluently execute a given closure if a feature is active. Additionally, a second closure may be provided and will be executed if the feature is inactive: -->
`when` メソッドは、機能がアクティブな場合に特定のクロージャをスムーズに実行するために使用できます。さらに、2 番目のクロージャを提供することができ、機能が非アクティブな場合に実行されます。

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::when(NewApi::class,
            fn () => $this->resolveNewApiResponse($request),
            fn () => $this->resolveLegacyApiResponse($request),
        );
    }

    // ...
}
```

<!-- The `unless` method serves as the inverse of the `when` method, executing the first closure if the feature is inactive: -->
`unless` メソッドは、`when` メソッドの逆として機能し、機能が非アクティブな場合に最初のクロージャを実行します。

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
<!-- ### The `HasFeatures` Trait -->
### The `HasFeatures` Trait

<!-- Pennant's `HasFeatures` trait may be added to your application's `User` model (or any other model that has features) to provide a fluent, convenient way to check features directly from the model: -->
Pennant の `HasFeatures` トレイトをアプリケーションの `User` モデル (または機能を持つ他のモデル) に追加すると、モデルから機能を直接チェックするためのスムーズで便利な方法が提供されます。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Pennant\Concerns\HasFeatures;

class User extends Authenticatable
{
    use HasFeatures;

    // ...
}
```

<!-- Once the trait has been added to your model, you may easily check features by invoking the `features` method: -->
特性をモデルに追加したら、`features` メソッドを呼び出して特徴を簡単にチェックできます。

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

<!-- Of course, the `features` method provides access to many other convenient methods for interacting with features: -->
もちろん、`features` メソッドは、機能を操作するための他の多くの便利なメソッドへのアクセスを提供します。

```php
// Values...
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// State...
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// Conditional execution...
$user->features()->when('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);

$user->features()->unless('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);
```

<a name="blade-directive"></a>
<!-- ### Blade Directive -->
### Blade Directive

<!-- To make checking features in Blade a seamless experience, Pennant offers the `@feature` and `@featureany` directive: -->
Blade のチェック機能をシームレスに行うために、Pennant では `@feature` および `@featureany` ディレクティブを提供しています。

```blade
@feature('site-redesign')
    <!-- 'site-redesign' is active -->
@else
    <!-- 'site-redesign' is inactive -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' or `beta` is active -->
@endfeatureany
```

<a name="middleware"></a>
<!-- ### Middleware -->
### Middleware

<!-- Pennant also includes a [middleware](/docs/13.x/middleware) that may be used to verify the currently authenticated user has access to a feature before a route is even invoked. You may assign the middleware to a route and specify the features that are required to access the route. If any of the specified features are inactive for the currently authenticated user, a `400 Bad Request` HTTP response will be returned by the route. Multiple features may be passed to the static `using` method. -->
Pennant には、ルートが呼び出される前に、現在認証されているユーザーが機能にアクセスできることを確認するために使用できる [middleware](/docs/13.x/middleware) も含まれています。ミドルウェアをルートに割り当て、ルートへのアクセスに必要な機能を指定できます。指定された機能のいずれかが現在認証されているユーザーに対して非アクティブである場合、`400 Bad Request` HTTP 応答がルートによって返されます。複数の機能を静的 `using` メソッドに渡すことができます。

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
<!-- #### Customizing the Response -->
#### Customizing the Response

<!-- If you would like to customize the response that is returned by the middleware when one of the listed features is inactive, you may use the `whenInactive` method provided by the `EnsureFeaturesAreActive` middleware. Typically, this method should be invoked within the `boot` method of one of your application's service providers: -->
リストされた機能のいずれかが非アクティブなときにミドルウェアによって返される応答をカスタマイズしたい場合は、`EnsureFeaturesAreActive` ミドルウェアによって提供される `whenInactive` メソッドを使用できます。通常、このメソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で呼び出す必要があります。

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return new Response(status: 403);
        }
    );

    // ...
}
```

<a name="intercepting-feature-checks"></a>
<!-- ### Intercepting Feature Checks -->
### Intercepting Feature Checks

<!-- Sometimes it can be useful to perform some in-memory checks before retrieving the stored value of a given feature. Imagine you are developing a new API behind a feature flag and want the ability to disable the new API without losing any of the resolved feature values in storage. If you notice a bug in the new API, you could easily disable it for everyone except internal team members, fix the bug, and then re-enable the new API for the users that previously had access to the feature. -->
特定の機能の保存された値を取得する前に、メモリ内チェックを実行すると便利な場合があります。機能フラグの背後で新しい API を開発していて、ストレージ内の解決された機能値を失わずに新しい API を無効にする機能が必要だと想像してください。新しい API のバグに気付いた場合は、内部チーム メンバーを除くすべてのユーザーに対してその API を簡単に無効にし、バグを修正してから、以前にその機能にアクセスしていたユーザーに対して新しい API を再度有効にすることができます。

<!-- You can achieve this with a [class-based feature's](#class-based-features) `before` method. When present, the `before` method is always run in-memory before retrieving the value from storage. If a non-`null` value is returned from the method, it will be used in place of the feature's stored value for the duration of the request: -->
これは、[class-based feature's](#class-based-features) `before` メソッドで実現できます。存在する場合、`before` メソッドは、ストレージから値を取得する前に常にメモリ内で実行されます。非 `null` 値がメソッドから返された場合、その値はリクエストの間、機能に保存されている値の代わりに使用されます。

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```

<!-- You could also use this feature to schedule the global rollout of a feature that was previously behind a feature flag: -->
この機能を使用して、以前は機能フラグの背後にあった機能のグローバル ロールアウトをスケジュールすることもできます。

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }

        if (Carbon::parse(Config::get('features.new-api.rollout-date'))->isPast()) {
            return true;
        }
    }

    // ...
}
```

<a name="in-memory-cache"></a>
<!-- ### In-Memory Cache -->
### In-Memory Cache

<!-- When checking a feature, Pennant will create an in-memory cache of the result. If you are using the `database` driver, this means that re-checking the same feature flag within a single request will not trigger additional database queries. This also ensures that the feature has a consistent result for the duration of the request. -->
特徴をチェックすると、Pennant は結果のメモリ内キャッシュを作成します。 `database` ドライバを使用している場合、これは、単一のリクエスト内で同じ機能フラグを再チェックしても、追加のデータベース クエリがトリガーされないことを意味します。これにより、リクエストの期間中、機能が一貫した結果を得ることが保証されます。

<!-- If you need to manually flush the in-memory cache, you may use the `flushCache` method offered by the `Feature` facade: -->
メモリ内キャッシュを手動でフラッシュする必要がある場合は、`Feature` ファサードが提供する `flushCache` メソッドを使用できます。

```php
Feature::flushCache();
```

<a name="scope"></a>
<!-- ## Scope -->
## Scope

<a name="specifying-the-scope"></a>
<!-- ### Specifying the Scope -->
### Specifying the Scope

<!-- As discussed, features are typically checked against the currently authenticated user. However, this may not always suit your needs. Therefore, it is possible to specify the scope you would like to check a given feature against via the `Feature` facade's `for` method: -->
説明したように、機能は通常、現在認証されているユーザーに対してチェックされます。ただし、これが必ずしもニーズに合うとは限りません。したがって、`Feature` ファサードの `for` メソッドを使用して、特定の機能をチェックするスコープを指定することができます。

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

<!-- Of course, feature scopes are not limited to "users". Imagine you have built a new billing experience that you are rolling out to entire teams rather than individual users. Perhaps you would like the oldest teams to have a slower rollout than the newer teams. Your feature resolution closure might look something like the following: -->
もちろん、機能の範囲は「ユーザー」に限定されません。新しい請求エクスペリエンスを構築し、それを個々のユーザーではなくチーム全体に展開していると想像してください。おそらく、最も古いチームのロールアウトを新しいチームよりも遅くしたいと考えるかもしれません。機能解決のクロージャは次のようになります。

```php
use App\Models\Team;
use Illuminate\Support\Carbon;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('billing-v2', function (Team $team) {
    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
        return true;
    }

    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
        return Lottery::odds(1 / 100);
    }

    return Lottery::odds(1 / 1000);
});
```

<!-- You will notice that the closure we have defined is not expecting a `User`, but is instead expecting a `Team` model. To determine if this feature is active for a user's team, you should pass the team to the `for` method offered by the `Feature` facade: -->
定義したクロージャーは `User` を予期しておらず、代わりに `Team` モデルを予期していることがわかります。この機能がユーザーのチームに対してアクティブであるかどうかを判断するには、`Feature` ファサードによって提供される `for` メソッドにチームを渡す必要があります。

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
<!-- ### Default Scope -->
### Default Scope

<!-- It is also possible to customize the default scope Pennant uses to check features. For example, maybe all of your features are checked against the currently authenticated user's team instead of the user. Instead of having to call `Feature::for($user->team)` every time you check a feature, you may instead specify the team as the default scope. Typically, this should be done in one of your application's service providers: -->
Pennant が機能をチェックするために使用するデフォルトのスコープをカスタマイズすることもできます。たとえば、すべての機能がユーザーではなく、現在認証されているユーザーのチームに対してチェックされる可能性があります。機能をチェックするたびに `Feature::for($user->team)` を呼び出す必要はなく、代わりにチームをデフォルトのスコープとして指定できます。通常、これはアプリケーションのサービスプロバイダの 1 つで行う必要があります。

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

<!-- If no scope is explicitly provided via the `for` method, the feature check will now use the currently authenticated user's team as the default scope: -->
`for` メソッドでスコープが明示的に指定されていない場合、機能チェックでは現在認証されているユーザーのチームがデフォルトのスコープとして使用されます。

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
<!-- ### Nullable Scope -->
### Nullable Scope

<!-- If the scope you provide when checking a feature is `null` and the feature's definition does not support `null` via a nullable type or by including `null` in a union type, Pennant will automatically return `false` as the feature's result value. -->
フィーチャーをチェックするときに指定したスコープが `null` で、フィーチャーの定義が null 許容型または共用体型に `null` を含めることによって `null` をサポートしていない場合、Pennant はフィーチャーの結果値として `false` を自動的に返します。

<!-- So, if the scope you are passing to a feature is potentially `null` and you want the feature's value resolver to be invoked, you should account for that in your feature's definition. A `null` scope may occur if you check a feature within an Artisan command, queued job, or unauthenticated route. Since there is usually not an authenticated user in these contexts, the default scope will be `null`. -->
したがって、機能に渡すスコープが `null` である可能性があり、その機能の値リゾルバーを呼び出す必要がある場合は、機能の定義でそれを考慮する必要があります。 Artisan コマンド、キューに入れられたジョブ、または認証されていないルート内の機能をチェックすると、`null` スコープが発生する可能性があります。通常、これらのコンテキストには認証されたユーザーが存在しないため、デフォルトのスコープは `null` になります。

<!-- If you do not always [explicitly specify your feature scope](#specifying-the-scope) then you should ensure the scope's type is "nullable" and handle the `null` scope value within your feature definition logic: -->
常に [explicitly specify your feature scope](#specifying-the-scope) ではない場合は、スコープのタイプが「nullable」であることを確認し、機能定義ロジック内で `null` スコープ値を処理する必要があります。

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User $user) => match (true) {// [tl! remove]
Feature::define('new-api', fn (User|null $user) => match (true) {// [tl! add]
    $user === null => true,// [tl! add]
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
<!-- ### Identifying Scope -->
### Identifying Scope

<!-- Pennant's built-in `array` and `database` storage drivers know how to properly store scope identifiers for all PHP data types as well as Eloquent models. However, if your application utilizes a third-party Pennant driver, that driver may not know how to properly store an identifier for an Eloquent model or other custom types in your application. -->
Pennant の組み込み `array` および `database` ストレージ ドライバは、すべての PHP データ型および Eloquent モデルのスコープ識別子を適切に保存する方法を認識しています。ただし、アプリケーションがサードパーティのPennant ドライバを利用している場合、そのドライバは Eloquent モデルまたはその他のカスタム タイプの識別子をアプリケーションに適切に保存する方法を知らない可能性があります。

<!-- In light of this, Pennant allows you to format scope values for storage by implementing the `FeatureScopeable` contract on the objects in your application that are used as Pennant scopes. -->
これを考慮して、Pennant では、Pennant スコープとして使用されるアプリケーション内のオブジェクトに `FeatureScopeable` コントラクトを実装することで、ストレージのスコープ値をフォーマットできます。

<!-- For example, imagine you are using two different feature drivers in a single application: the built-in `database` driver and a third-party "Flag Rocket" driver. The "Flag Rocket" driver does not know how to properly store an Eloquent model. Instead, it requires a `FlagRocketUser` instance. By implementing the `toFeatureIdentifier` defined by the `FeatureScopeable` contract, we can customize the storable scope value provided to each driver used by our application: -->
たとえば、1 つのアプリケーションで 2 つの異なる機能ドライバ (組み込みの `database` ドライバとサードパーティの "Flag Rocket" ドライバ) を使用しているとします。 「Flag Rocket」ドライバは、Eloquent モデルを適切に保存する方法を知りません。代わりに、`FlagRocketUser` インスタンスが必要です。 `FeatureScopeable` コントラクトで定義された `toFeatureIdentifier` を実装することで、アプリケーションで使用される各ドライバに提供される保存可能なスコープ値をカスタマイズできます。

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * Cast the object to a feature scope identifier for the given driver.
     */
    public function toFeatureIdentifier(string $driver): mixed
    {
        return match($driver) {
            'database' => $this,
            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),
        };
    }
}
```

<a name="serializing-scope"></a>
<!-- ### Serializing Scope -->
### Serializing Scope

<!-- By default, Pennant will use a fully qualified class name when storing a feature associated with an Eloquent model. If you are already using an [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types), you may choose to have Pennant also use the morph map to decouple the stored feature from your application structure. -->
デフォルトでは、Pennant は Eloquent モデルに関連付けられた機能を保存するときに完全修飾クラス名を使用します。すでに [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types) を使用している場合は、Pennant でモーフ マップも使用して、保存されたフィーチャをアプリケーション構造から分離することを選択できます。

<!-- To achieve this, after defining your Eloquent morph map in a service provider, you may invoke the `Feature` facade's `useMorphMap` method: -->
これを実現するには、サービスプロバイダで Eloquent モーフ マップを定義した後、`Feature` ファサードの `useMorphMap` メソッドを呼び出すことができます。

```php
use Illuminate\Database\Eloquent\Relations\Relation;
use Laravel\Pennant\Feature;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);

Feature::useMorphMap();
```

<a name="rich-feature-values"></a>
<!-- ## Rich Feature Values -->
## Rich Feature Values

<!-- Until now, we have primarily shown features as being in a binary state, meaning they are either "active" or "inactive", but Pennant also allows you to store rich values as well. -->
これまでは、主にフィーチャがバイナリ状態、つまり「アクティブ」または「非アクティブ」のいずれかであるものとして示してきましたが、Pennant ではリッチな値も保存することもできます。

<!-- For example, imagine you are testing three new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string: -->
たとえば、アプリケーションの「今すぐ購入」ボタン用に 3 つの新しい色をテストしていると想像してください。機能定義から `true` または `false` を返す代わりに、文字列を返すこともできます。

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

<!-- You may retrieve the value of the `purchase-button` feature using the `value` method: -->
`value` メソッドを使用して、`purchase-button` 機能の値を取得できます。

```php
$color = Feature::value('purchase-button');
```

<!-- Pennant's included Blade directive also makes it easy to conditionally render content based on the current value of the feature: -->
Pennant に含まれる Blade ディレクティブを使用すると、機能の現在の値に基づいてコンテンツを条件付きでレンダリングすることも簡単になります。

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' is active -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' is active -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' is active -->
@endfeature
```

> [!NOTE]
> 豊富な値を使用する場合、`false` 以外の値を持つ機能は「アクティブ」であるとみなされることを知っておくことが重要です。

<!-- When calling the [conditional `when`](#conditional-execution) method, the feature's rich value will be provided to the first closure: -->
[conditional `when`](#conditional-execution) メソッドを呼び出すと、機能の豊富な値が最初のクロージャに提供されます。

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

<!-- Likewise, when calling the conditional `unless` method, the feature's rich value will be provided to the optional second closure: -->
同様に、条件付き `unless` メソッドを呼び出すと、機能の豊富な値がオプションの 2 番目のクロージャに提供されます。

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
<!-- ## Retrieving Multiple Features -->
## Retrieving Multiple Features

<!-- The `values` method allows the retrieval of multiple features for a given scope: -->
`values` メソッドを使用すると、指定されたスコープの複数の機能を取得できます。

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

<!-- Or, you may use the `all` method to retrieve the values of all defined features for a given scope: -->
または、`all` メソッドを使用して、特定のスコープに対して定義されたすべての機能の値を取得することもできます。

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<!-- However, class-based features are dynamically registered and are not known by Pennant until they are explicitly checked. This means your application's class-based features may not appear in the results returned by the `all` method if they have not already been checked during the current request. -->
ただし、クラスベースの機能は動的に登録されるため、明示的にチェックされるまでPennant には認識されません。これは、現在のリクエスト中にまだチェックされていない場合、アプリケーションのクラスベースの機能が `all` メソッドによって返される結果に表示されない可能性があることを意味します。

<!-- If you would like to ensure that feature classes are always included when using the `all` method, you may use Pennant's feature discovery capabilities. To get started, invoke the `discover` method in one of your application's service providers: -->
`all` メソッドを使用するときにフィーチャクラスが常に含まれるようにしたい場合は、Pennant のフィーチャ検出機能を使用できます。まず、アプリケーションのサービスプロバイダの 1 つで `discover` メソッドを呼び出します。

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

<!-- The `discover` method will register all of the feature classes in your application's `app/Features` directory. The `all` method will now include these classes in its results, regardless of whether they have been checked during the current request: -->
`discover` メソッドは、アプリケーションの `app/Features` ディレクトリにすべてのフィーチャクラスを登録します。 `all` メソッドは、現在のリクエスト中にチェックされたかどうかに関係なく、これらのクラスを結果に含めるようになりました。

```php
Feature::all();

// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<a name="eager-loading"></a>
<!-- ## Eager Loading -->
## Eager Loading

<!-- Although Pennant keeps an in-memory cache of all resolved features for a single request, it is still possible to encounter performance issues. To alleviate this, Pennant offers the ability to eager load feature values. -->
Pennant は 1 つのリクエストに対して解決されたすべての機能のメモリ内キャッシュを保持しますが、それでもパフォーマンスの問題が発生する可能性があります。これを軽減するために、Pennant は特徴値を一括ロードする機能を提供します。

<!-- To illustrate this, imagine that we are checking if a feature is active within a loop: -->
これを説明するために、ループ内で機能がアクティブかどうかをチェックしていると想像してください。

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

<!-- Assuming we are using the database driver, this code will execute a database query for every user in the loop - executing potentially hundreds of queries. However, using Pennant's `load` method, we can remove this potential performance bottleneck by eager loading the feature values for a collection of users or scopes: -->
データベース ドライバを使用していると仮定すると、このコードはループ内のすべてのユーザーに対してデータベース クエリを実行します。これにより、数百のクエリが実行される可能性があります。ただし、Pennant の `load` メソッドを使用すると、ユーザーまたはスコープのコレクションの特徴値を積極的にロードすることで、この潜在的なパフォーマンスのボトルネックを取り除くことができます。

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

<!-- To load feature values only when they have not already been loaded, you may use the `loadMissing` method: -->
特徴値がまだロードされていない場合にのみロードするには、`loadMissing` メソッドを使用できます。

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

<!-- You may load all defined features using the `loadAll` method: -->
`loadAll` メソッドを使用して、定義されたすべての機能をロードできます。

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
<!-- ## Updating Values -->
## Updating Values

<!-- When a feature's value is resolved for the first time, the underlying driver will store the result in storage. This is often necessary to ensure a consistent experience for your users across requests. However, at times, you may want to manually update the feature's stored value. -->
機能の値が初めて解決されると、基礎となるドライバは結果をストレージに保存します。これは、リクエスト間でユーザーに一貫したエクスペリエンスを保証するために必要となることがよくあります。ただし、場合によっては、機能に保存されている値を手動で更新することが必要になる場合があります。

<!-- To accomplish this, you may use the `activate` and `deactivate` methods to toggle a feature "on" or "off": -->
これを実現するには、`activate` メソッドと `deactivate` メソッドを使用して、機能を「オン」または「オフ」に切り替えます。

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```

<!-- It is also possible to manually set a rich value for a feature by providing a second argument to the `activate` method: -->
`activate` メソッドに 2 番目の引数を指定することで、機能に豊富な値を手動で設定することもできます。

```php
Feature::activate('purchase-button', 'seafoam-green');
```

<!-- To instruct Pennant to forget the stored value for a feature, you may use the `forget` method. When the feature is checked again, Pennant will resolve the feature's value from its feature definition: -->
Pennant に保存された機能の値を忘れるように指示するには、`forget` メソッドを使用できます。フィーチャーが再度チェックされると、Pennant はフィーチャー定義からフィーチャーの値を解決します。

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
<!-- ### Bulk Updates -->
### Bulk Updates

<!-- To update stored feature values in bulk, you may use the `activateForEveryone` and `deactivateForEveryone` methods. -->
保存された特徴値を一括更新するには、`activateForEveryone` メソッドと `deactivateForEveryone` メソッドを使用できます。

<!-- For example, imagine you are now confident in the `new-api` feature's stability and have landed on the best `'purchase-button'` color for your checkout flow - you can update the stored value for all users accordingly: -->
たとえば、`new-api` 機能の安定性に自信があり、チェックアウト フローに最適な `'purchase-button'` カラーを見つけたと想像してください。それに応じて、すべてのユーザーの保存値を更新できます。

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

<!-- Alternatively, you may deactivate the feature for all users: -->
あるいは、すべてのユーザーに対してこの機能を無効にすることもできます。

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> これにより、Pennant のストレージ ドライバによって保存されている解決された特徴値のみが更新されます。アプリケーションの機能定義も更新する必要があります。

<a name="purging-features"></a>
<!-- ### Purging Features -->
### Purging Features

<!-- Sometimes, it can be useful to purge an entire feature from storage. This is typically necessary if you have removed the feature from your application or you have made adjustments to the feature's definition that you would like to rollout to all users. -->
場合によっては、機能全体をストレージから削除すると便利な場合があります。これは通常、アプリケーションから機能を削除した場合、またはすべてのユーザーにロールアウトする機能の定義を調整した場合に必要です。

<!-- You may remove all stored values for a feature using the `purge` method: -->
`purge` メソッドを使用して、機能に保存されているすべての値を削除できます。

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```

<!-- If you would like to purge _all_ features from storage, you may invoke the `purge` method without any arguments: -->
ストレージからすべての機能を削除したい場合は、引数なしで `purge` メソッドを呼び出すことができます。

```php
Feature::purge();
```

<!-- As it can be useful to purge features as part of your application's deployment pipeline, Pennant includes a `pennant:purge` Artisan command which will purge the provided features from storage: -->
アプリケーションのデプロイメント パイプラインの一部として機能をパージすると便利なため、Pennant には、提供された機能をストレージからパージする `pennant:purge` Artisan コマンドが含まれています。

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

<!-- It is also possible to purge all features _except_ those in a given feature list. For example, imagine you wanted to purge all features but keep the values for the "new-api" and "purchase-button" features in storage. To accomplish this, you can pass those feature names to the `--except` option: -->
特定の機能リスト内の機能を除くすべての機能を削除することもできます。たとえば、すべての機能を削除し、「new-api」機能と「purchase-button」機能の値をストレージに保持したいとします。これを実現するには、これらの機能名を `--except` オプションに渡すことができます。

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

<!-- For convenience, the `pennant:purge` command also supports an `--except-registered` flag. This flag indicates that all features except those explicitly registered in a service provider should be purged: -->
便宜上、`pennant:purge` コマンドは `--except-registered` フラグもサポートします。このフラグは、サービスプロバイダに明示的に登録されている機能を除くすべての機能をパージする必要があることを示します。

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing code that interacts with feature flags, the easiest way to control the feature flag's returned value in your tests is to simply re-define the feature. For example, imagine you have the following feature defined in one of your application's service provider: -->
機能フラグと対話するコードをテストする場合、テストで機能フラグの戻り値を制御する最も簡単な方法は、単純に機能を再定義することです。たとえば、アプリケーションのサービスプロバイダの 1 つで次の機能が定義されていると想像してください。

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

<!-- To modify the feature's returned value in your tests, you may re-define the feature at the beginning of the test. The following test will always pass, even though the `Arr::random()` implementation is still present in the service provider: -->
テストで機能の戻り値を変更するには、テストの開始時に機能を再定義します。 `Arr::random()` 実装がサービスプロバイダにまだ存在している場合でも、次のテストは常に合格します。

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define('purchase-button', 'seafoam-green');

    expect(Feature::value('purchase-button'))->toBe('seafoam-green');
});
```

```php tab=PHPUnit
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```

<!-- The same approach may be used for class-based features: -->
同じアプローチをクラスベースの機能にも使用できます。

```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define(NewApi::class, true);

    expect(Feature::value(NewApi::class))->toBeTrue();
});
```

```php tab=PHPUnit
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```

<!-- If your feature is returning a `Lottery` instance, there are a handful of useful [testing helpers available](/docs/13.x/helpers#testing-lotteries). -->
機能が `Lottery` インスタンスを返す場合、役立つ [testing helpers available](/docs/13.x/helpers#testing-lotteries) がいくつかあります。

<a name="store-configuration"></a>
<!-- #### Store Configuration -->
#### Store Configuration

<!-- You may configure the store that Pennant will use during testing by defining the `PENNANT_STORE` environment variable in your application's `phpunit.xml` file: -->
アプリケーションの `phpunit.xml` ファイルで `PENNANT_STORE` 環境変数を定義することで、Pennant がテスト中に使用するストアを構成できます。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit colors="true">
    <!-- ... -->
    <php>
        <env name="PENNANT_STORE" value="array"/>
        <!-- ... -->
    </php>
</phpunit>
```

<a name="adding-custom-pennant-drivers"></a>
<!-- ## Adding Custom Pennant Drivers -->
## Adding Custom Pennant Drivers

<a name="implementing-the-driver"></a>
<!-- #### Implementing the Driver -->
#### Implementing the Driver

<!-- If none of Pennant's existing storage drivers fit your application's needs, you may write your own storage driver. Your custom driver should implement the `Laravel\Pennant\Contracts\Driver` interface: -->
Pennant の既存のストレージ ドライバがアプリケーションのニーズに適合しない場合は、独自のストレージ ドライバを作成できます。カスタム ドライバは、`Laravel\Pennant\Contracts\Driver` インターフェイスを実装する必要があります。

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;

class RedisFeatureDriver implements Driver
{
    public function define(string $feature, callable $resolver): void {}
    public function defined(): array {}
    public function getAll(array $features): array {}
    public function get(string $feature, mixed $scope): mixed {}
    public function set(string $feature, mixed $scope, mixed $value): void {}
    public function setForAllScopes(string $feature, mixed $value): void {}
    public function delete(string $feature, mixed $scope): void {}
    public function purge(array|null $features): void {}
}
```

<!-- Now, we just need to implement each of these methods using a Redis connection. For an example of how to implement each of these methods, take a look at the `Laravel\Pennant\Drivers\DatabaseDriver` in the [Pennant source code](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php) -->
ここで、Redis 接続を使用してこれらの各メソッドを実装するだけです。これらの各メソッドの実装方法の例については、[Pennant source code](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php) の `Laravel\Pennant\Drivers\DatabaseDriver` を参照してください。

> [!NOTE]
> Laravel には、拡張機能を含めるディレクトリは付属していません。好きな場所に自由に配置できます。この例では、`RedisFeatureDriver` を格納する `Extensions` ディレクトリを作成しました。

<a name="registering-the-driver"></a>
<!-- #### Registering the Driver -->
#### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Pennant, you may use the `extend` method provided by the `Feature` facade. You should call the `extend` method from the `boot` method of one of your application's [service provider](/docs/13.x/providers): -->
ドライバが実装されたら、Laravel に登録する準備が整います。追加のドライバをPennant に追加するには、`Feature` ファサードによって提供される `extend` メソッドを使用できます。アプリケーションの [service provider](/docs/13.x/providers) のいずれかの `boot` メソッドから `extend` メソッドを呼び出す必要があります。

```php
<?php

namespace App\Providers;

use App\Extensions\RedisFeatureDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

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
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

<!-- Once the driver has been registered, you may use the `redis` driver in your application's `config/pennant.php` configuration file: -->
ドライバが登録されたら、アプリケーションの `config/pennant.php` 構成ファイルで `redis` ドライバを使用できます。

```php
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```

<a name="defining-features-externally"></a>
<!-- ### Defining Features Externally -->
### Defining Features Externally

<!-- If your driver is a wrapper around a third-party feature flag platform, you will likely define features on the platform rather than using Pennant's `Feature::define` method. If that is the case, your custom driver should also implement the `Laravel\Pennant\Contracts\DefinesFeaturesExternally` interface: -->
ドライバがサードパーティの機能フラグ プラットフォームのラッパーである場合は、Pennant の `Feature::define` メソッドを使用するのではなく、プラットフォーム上で機能を定義する可能性があります。その場合、カスタム ドライバは `Laravel\Pennant\Contracts\DefinesFeaturesExternally` インターフェイスも実装する必要があります。

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * Get the features defined for the given scope.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

<!-- The `definedFeaturesForScope` method should return a list of feature names defined for the provided scope. -->
`definedFeaturesForScope` メソッドは、指定されたスコープに対して定義された機能名のリストを返す必要があります。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Pennant dispatches a variety of events that can be useful when tracking feature flags throughout your application. -->
Pennant は、アプリケーション全体で機能フラグを追跡するときに役立つさまざまなイベントを送出します。

<!-- ### `Laravel\Pennant\Events\FeatureRetrieved` -->
### `Laravel\Pennant\Events\FeatureRetrieved`

<!-- This event is dispatched whenever a [feature is checked](#checking-features). This event may be useful for creating and tracking metrics against a feature flag's usage throughout your application. -->
このイベントは、[feature is checked](#checking-features)たびに送出されます。このイベントは、アプリケーション全体での機能フラグの使用状況に対するメトリクスの作成と追跡に役立つ場合があります。

<!-- ### `Laravel\Pennant\Events\FeatureResolved` -->
### `Laravel\Pennant\Events\FeatureResolved`

<!-- This event is dispatched the first time a feature's value is resolved for a specific scope. -->
このイベントは、特定のスコープに対して機能の値が初めて解決されるときに送出されます。

<!-- ### `Laravel\Pennant\Events\UnknownFeatureResolved` -->
### `Laravel\Pennant\Events\UnknownFeatureResolved`

<!-- This event is dispatched the first time an unknown feature is resolved for a specific scope. Listening to this event may be useful if you have intended to remove a feature flag but have accidentally left stray references to it throughout your application: -->
このイベントは、特定のスコープで不明な機能が初めて解決されたときに送出されます。このイベントをリッスンすることは、機能フラグを削除するつもりが、誤ってアプリケーション全体にその機能フラグへの参照を残した場合に役立つことがあります。

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnknownFeatureResolved;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::listen(function (UnknownFeatureResolved $event) {
            Log::error("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```

<!-- ### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass` -->
### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

<!-- This event is dispatched when a [class-based feature](#class-based-features) is dynamically checked for the first time during a request. -->
このイベントは、リクエスト中に [class-based feature](#class-based-features) が初めて動的にチェックされるときに送出されます。

<!-- ### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered` -->
### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

<!-- This event is dispatched when a `null` scope is passed to a feature definition that [doesn't support null](#nullable-scope). -->
このイベントは、`null` スコープが [doesn't support null](#nullable-scope) 機能定義に渡されたときに送出されます。

<!-- This situation is handled gracefully and the feature will return `false`. However, if you would like to opt out of this feature's default graceful behavior, you may register a listener for this event in the `boot` method of your application's `AppServiceProvider`: -->
この状況は適切に処理され、機能は `false` を返します。ただし、この機能のデフォルトの正常な動作をオプトアウトしたい場合は、アプリケーションの `AppServiceProvider` の `boot` メソッドでこのイベントのリスナを登録できます。

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

<!-- ### `Laravel\Pennant\Events\FeatureUpdated` -->
### `Laravel\Pennant\Events\FeatureUpdated`

<!-- This event is dispatched when updating a feature for a scope, usually by calling `activate` or `deactivate`. -->
このイベントは、通常は `activate` または `deactivate` を呼び出すことによって、スコープの機能を更新するときに送出されます。

<!-- ### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes` -->
### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

<!-- This event is dispatched when updating a feature for all scopes, usually by calling `activateForEveryone` or `deactivateForEveryone`. -->
このイベントは、通常は `activateForEveryone` または `deactivateForEveryone` を呼び出すことによって、すべてのスコープの機能を更新するときに送出されます。

<!-- ### `Laravel\Pennant\Events\FeatureDeleted` -->
### `Laravel\Pennant\Events\FeatureDeleted`

<!-- This event is dispatched when deleting a feature for a scope, usually by calling `forget`. -->
このイベントは、通常は `forget` を呼び出すことによって、スコープの機能を削除するときに送出されます。

<!-- ### `Laravel\Pennant\Events\FeaturesPurged` -->
### `Laravel\Pennant\Events\FeaturesPurged`

<!-- This event is dispatched when purging specific features. -->
このイベントは、特定の機能を削除するときに送出されます。

<!-- ### `Laravel\Pennant\Events\AllFeaturesPurged` -->
### `Laravel\Pennant\Events\AllFeaturesPurged`

<!-- This event is dispatched when purging all features. -->
このイベントは、すべての機能を削除するときに送出されます。

