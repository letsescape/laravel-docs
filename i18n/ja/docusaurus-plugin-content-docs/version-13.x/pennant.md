# Laravel Pennant (Laravel Pennant)

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [機能の定義](#defining-features)
    - [クラスベースの機能](#class-based-features)
- [機能の確認](#checking-features)
    - [条件付き実行](#conditional-execution)
    - [`HasFeatures` 特性](#the-has-features-trait)
    - [Blade ディレクティブ](#blade-directive)
    - [Middleware](#middleware)
    - [インターセプト機能チェック](#intercepting-feature-checks)
    - [インメモリキャッシュ](#in-memory-cache)
- [Scope](#scope)
    - [スコープの指定](#specifying-the-scope)
    - [デフォルトのスコープ](#default-scope)
    - [NULL 可能スコープ](#nullable-scope)
    - [範囲の特定](#identifying-scope)
    - [シリアル化スコープ](#serializing-scope)
- [豊富な特徴量](#rich-feature-values)
- [複数の特徴の取得](#retrieving-multiple-features)
- [熱心な読み込み](#eager-loading)
- [値の更新](#updating-values)
    - [一括更新](#bulk-updates)
    - [パージ機能](#purging-features)
- [Testing](#testing)
- [カスタム Pennant ドライバの追加](#adding-custom-pennant-drivers)
    - [ドライバの実装](#implementing-the-driver)
    - [ドライバを登録する](#registering-the-driver)
    - [機能の外部定義](#defining-features-externally)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Pennant](https://github.com/laravel/pennant) は、無駄のない、シンプルで軽量な機能フラグ パッケージです。機能フラグを使用すると、新しいアプリケーション機能を自信を持って段階的にロールアウトしたり、新しいインターフェイス設計の A/B テストを行ったり、トランクベースの開発戦略を補完したりすることができます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して、Pennant をプロジェクトにインストールします。

```shell
composer require laravel/pennant
```

次に、`vendor:publish` Artisan コマンドを使用して、Pennant構成ファイルと移行ファイルを公開する必要があります。

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

最後に、アプリケーションのデータベース移行を実行する必要があります。これにより、Pennant が `database` ドライバを駆動するために使用する `features` テーブルが作成されます。

```shell
php artisan migrate
```

<a name="configuration"></a>
## 構成 (Configuration)

Pennant のアセットを公開すると、その構成ファイルは `config/pennant.php` に配置されます。この構成ファイルを使用すると、解決された機能フラグ値を保存するためにPennant が使用するデフォルトのストレージ メカニズムを指定できます。

Pennant には、`array` ドライバを介して、解決された機能フラグ値をメモリ内配列に保存するためのサポートが含まれています。または、Pennant は、Pennant が使用するデフォルトのストレージ メカニズムである `database` ドライバを介して、解決された機能フラグ値をリレーショナル データベースに永続的に保存できます。

<a name="defining-features"></a>
## 機能の定義 (Defining Features)

機能を定義するには、`Feature` ファサードによって提供される `define` メソッドを使用できます。機能の名前と、機能の初期値を解決するために呼び出されるクロージャを指定する必要があります。

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

ご覧のとおり、この機能には次のルールがあります。

- すべての内部チーム メンバーは新しい API を使用する必要があります。
- トラフィック量の多い顧客は、新しい API を使用しないでください。
- それ以外の場合、機能は 100 分の 1 の確率でアクティブになるユーザーにランダムに割り当てられる必要があります。

特定のユーザーに対して初めて `new-api` 機能がチェックされると、クロージャーの結果がストレージ ドライバによって保存されます。次回この機能が同じユーザーに対してチェックされるとき、値はストレージから取得され、クロージャは呼び出されません。

便宜上、機能定義が宝くじのみを返す場合は、クロージャーを完全に省略できます。

    Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### クラスベースの機能

Pennant では、クラスベースの機能を定義することもできます。クロージャベースの機能定義とは異なり、サービスプロバイダにクラスベースの機能を登録する必要はありません。クラスベースのフィーチャーを作成するには、`pennant:feature` Artisan コマンドを呼び出します。デフォルトでは、フィーチャクラスはアプリケーションの `app/Features` ディレクトリに配置されます。

```shell
php artisan pennant:feature NewApi
```

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

クラスベースの機能のインスタンスを手動で解決したい場合は、`Feature` ファサードで `instance` メソッドを呼び出すことができます。

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> フィーチャクラスは [container](/docs/{{version}}/container) 経由で解決されるため、必要に応じてフィーチャクラスのコンストラクターに依存関係を注入できます。

#### 保存された機能名のカスタマイズ

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
## 機能の確認 (Checking Features)

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

デフォルトでは、現在認証されているユーザーに対して機能がチェックされますが、別のユーザーまたは [scope](#scope) に対して機能を簡単にチェックできます。これを実現するには、`Feature` ファサードによって提供される `for` メソッドを使用します。

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

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
> Artisan コマンドやキューに入れられたジョブなど、HTTP コンテキストの外部でPennant を使用する場合は、通常、[機能のスコープを明示的に指定する](#specifying-the-scope) を使用する必要があります。あるいは、認証された HTTP コンテキストと未認証のコンテキストの両方を考慮した [デフォルトのスコープ](#default-scope) を定義することもできます。

<a name="checking-class-based-features"></a>
#### クラスベースの機能の確認

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
### 条件付き実行

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

`unless` メソッドは、`when` メソッドの逆として機能し、機能が非アクティブな場合に最初のクロージャを実行します。

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 特性

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

特性をモデルに追加したら、`features` メソッドを呼び出して特徴を簡単にチェックできます。

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

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
### Blade ディレクティブ

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
### ミドルウェア

Pennant には、ルートが呼び出される前に、現在認証されているユーザーが機能にアクセスできることを確認するために使用できる [middleware](/docs/{{version}}/middleware) も含まれています。ミドルウェアをルートに割り当て、ルートへのアクセスに必要な機能を指定できます。指定された機能のいずれかが現在認証されているユーザーに対して非アクティブである場合、`400 Bad Request` HTTP 応答がルートによって返されます。複数の機能を静的 `using` メソッドに渡すことができます。

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 応答のカスタマイズ

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
### インターセプト機能チェック

特定の機能の保存された値を取得する前に、メモリ内チェックを実行すると便利な場合があります。機能フラグの背後で新しい API を開発していて、ストレージ内の解決された機能値を失わずに新しい API を無効にする機能が必要だと想像してください。新しい API のバグに気付いた場合は、内部チーム メンバーを除くすべてのユーザーに対してその API を簡単に無効にし、バグを修正してから、以前にその機能にアクセスしていたユーザーに対して新しい API を再度有効にすることができます。

これは、[クラスベースの機能](#class-based-features) `before` メソッドで実現できます。存在する場合、`before` メソッドは、ストレージから値を取得する前に常にメモリ内で実行されます。非 `null` 値がメソッドから返された場合、その値はリクエストの間、機能に保存されている値の代わりに使用されます。

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
### インメモリキャッシュ

特徴をチェックすると、Pennant は結果のメモリ内キャッシュを作成します。 `database` ドライバを使用している場合、これは、単一のリクエスト内で同じ機能フラグを再チェックしても、追加のデータベース クエリがトリガーされないことを意味します。これにより、リクエストの期間中、機能が一貫した結果を得ることが保証されます。

メモリ内キャッシュを手動でフラッシュする必要がある場合は、`Feature` ファサードが提供する `flushCache` メソッドを使用できます。

```php
Feature::flushCache();
```

<a name="scope"></a>
## 範囲 (Scope)

<a name="specifying-the-scope"></a>
### スコープの指定

説明したように、機能は通常、現在認証されているユーザーに対してチェックされます。ただし、これが必ずしもニーズに合うとは限りません。したがって、`Feature` ファサードの `for` メソッドを使用して、特定の機能をチェックするスコープを指定することができます。

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

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

定義したクロージャーは `User` を予期しておらず、代わりに `Team` モデルを予期していることがわかります。この機能がユーザーのチームに対してアクティブであるかどうかを判断するには、`Feature` ファサードによって提供される `for` メソッドにチームを渡す必要があります。

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### デフォルトのスコープ

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

`for` メソッドでスコープが明示的に指定されていない場合、機能チェックでは現在認証されているユーザーのチームがデフォルトのスコープとして使用されます。

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### NULL 可能スコープ

フィーチャーをチェックするときに指定したスコープが `null` で、フィーチャーの定義が null 許容型または共用体型に `null` を含めることによって `null` をサポートしていない場合、Pennant はフィーチャーの結果値として `false` を自動的に返します。

したがって、機能に渡すスコープが `null` である可能性があり、その機能の値リゾルバーを呼び出す必要がある場合は、機能の定義でそれを考慮する必要があります。 Artisan コマンド、キューに入れられたジョブ、または認証されていないルート内の機能をチェックすると、`null` スコープが発生する可能性があります。通常、これらのコンテキストには認証されたユーザーが存在しないため、デフォルトのスコープは `null` になります。

常に [機能範囲を明示的に指定する](#specifying-the-scope) ではない場合は、スコープのタイプが「nullable」であることを確認し、機能定義ロジック内で `null` スコープ値を処理する必要があります。

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
### 範囲の特定

Pennant の組み込み `array` および `database` ストレージ ドライバは、すべての PHP データ型および Eloquent モデルのスコープ識別子を適切に保存する方法を認識しています。ただし、アプリケーションがサードパーティのPennant ドライバを利用している場合、そのドライバは Eloquent モデルまたはその他のカスタム タイプの識別子をアプリケーションに適切に保存する方法を知らない可能性があります。

これを考慮して、Pennant では、Pennant スコープとして使用されるアプリケーション内のオブジェクトに `FeatureScopeable` コントラクトを実装することで、ストレージのスコープ値をフォーマットできます。

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
### シリアル化スコープ

デフォルトでは、Pennant は Eloquent モデルに関連付けられた機能を保存するときに完全修飾クラス名を使用します。すでに [Eloquent モーフマップ](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types) を使用している場合は、Pennant でモーフ マップも使用して、保存されたフィーチャをアプリケーション構造から分離することを選択できます。

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
## 豊富な特徴量 (Rich Feature Values)

これまでは、主にフィーチャがバイナリ状態、つまり「アクティブ」または「非アクティブ」のいずれかであるものとして示してきましたが、Pennant ではリッチな値も保存することもできます。

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

`value` メソッドを使用して、`purchase-button` 機能の値を取得できます。

```php
$color = Feature::value('purchase-button');
```

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

[条件付き `when`](#conditional-execution) メソッドを呼び出すと、機能の豊富な値が最初のクロージャに提供されます。

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

同様に、条件付き `unless` メソッドを呼び出すと、機能の豊富な値がオプションの 2 番目のクロージャに提供されます。

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 複数の特徴の取得 (Retrieving Multiple Features)

`values` メソッドを使用すると、指定されたスコープの複数の機能を取得できます。

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

または、`all` メソッドを使用して、特定のスコープに対して定義されたすべての機能の値を取得することもできます。

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

ただし、クラスベースの機能は動的に登録されるため、明示的にチェックされるまでPennant には認識されません。これは、現在のリクエスト中にまだチェックされていない場合、アプリケーションのクラスベースの機能が `all` メソッドによって返される結果に表示されない可能性があることを意味します。

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
## 熱心な読み込み (Eager Loading)

Pennant は 1 つのリクエストに対して解決されたすべての機能のメモリ内キャッシュを保持しますが、それでもパフォーマンスの問題が発生する可能性があります。これを軽減するために、Pennant は特徴値を一括ロードする機能を提供します。

これを説明するために、ループ内で機能がアクティブかどうかをチェックしていると想像してください。

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

データベース ドライバを使用していると仮定すると、このコードはループ内のすべてのユーザーに対してデータベース クエリを実行します。これにより、数百のクエリが実行される可能性があります。ただし、Pennant の `load` メソッドを使用すると、ユーザーまたはスコープのコレクションの特徴値を積極的にロードすることで、この潜在的なパフォーマンスのボトルネックを取り除くことができます。

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

特徴値がまだロードされていない場合にのみロードするには、`loadMissing` メソッドを使用できます。

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

`loadAll` メソッドを使用して、定義されたすべての機能をロードできます。

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 値の更新 (Updating Values)

機能の値が初めて解決されると、基礎となるドライバは結果をストレージに保存します。これは、リクエスト間でユーザーに一貫したエクスペリエンスを保証するために必要となることがよくあります。ただし、場合によっては、機能に保存されている値を手動で更新することが必要になる場合があります。

これを実現するには、`activate` メソッドと `deactivate` メソッドを使用して、機能を「オン」または「オフ」に切り替えます。

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```

`activate` メソッドに 2 番目の引数を指定することで、機能に豊富な値を手動で設定することもできます。

```php
Feature::activate('purchase-button', 'seafoam-green');
```

Pennant に保存された機能の値を忘れるように指示するには、`forget` メソッドを使用できます。フィーチャーが再度チェックされると、Pennant はフィーチャー定義からフィーチャーの値を解決します。

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 一括更新

保存された特徴値を一括更新するには、`activateForEveryone` メソッドと `deactivateForEveryone` メソッドを使用できます。

たとえば、`new-api` 機能の安定性に自信があり、チェックアウト フローに最適な `'purchase-button'` カラーを見つけたと想像してください。それに応じて、すべてのユーザーの保存値を更新できます。

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

あるいは、すべてのユーザーに対してこの機能を無効にすることもできます。

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> これにより、Pennant のストレージ ドライバによって保存されている解決された特徴値のみが更新されます。アプリケーションの機能定義も更新する必要があります。

<a name="purging-features"></a>
### パージ機能

場合によっては、機能全体をストレージから削除すると便利な場合があります。これは通常、アプリケーションから機能を削除した場合、またはすべてのユーザーにロールアウトする機能の定義を調整した場合に必要です。

`purge` メソッドを使用して、機能に保存されているすべての値を削除できます。

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```

ストレージからすべての機能を削除したい場合は、引数なしで `purge` メソッドを呼び出すことができます。

```php
Feature::purge();
```

アプリケーションのデプロイメント パイプラインの一部として機能をパージすると便利なため、Pennant には、提供された機能をストレージからパージする `pennant:purge` Artisan コマンドが含まれています。

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

特定の機能リスト内の機能を除くすべての機能を削除することもできます。たとえば、すべての機能を削除し、「new-api」機能と「purchase-button」機能の値をストレージに保持したいとします。これを実現するには、これらの機能名を `--except` オプションに渡すことができます。

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

便宜上、`pennant:purge` コマンドは `--except-registered` フラグもサポートします。このフラグは、サービスプロバイダに明示的に登録されている機能を除くすべての機能をパージする必要があることを示します。

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## テスト (Testing)

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

機能が `Lottery` インスタンスを返す場合、役立つ [テストヘルパが利用可能](/docs/{{version}}/helpers#testing-lotteries) がいくつかあります。

<a name="store-configuration"></a>
#### ストア構成

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
## カスタム Pennant ドライバの追加 (Adding Custom Pennant Drivers)

<a name="implementing-the-driver"></a>
#### ドライバの実装

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

ここで、Redis 接続を使用してこれらの各メソッドを実装するだけです。これらの各メソッドの実装方法の例については、[Pennant のソースコード](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php) の `Laravel\Pennant\Drivers\DatabaseDriver` を参照してください。

> [!NOTE]
> Laravel には、拡張機能を含めるディレクトリは付属していません。好きな場所に自由に配置できます。この例では、`RedisFeatureDriver` を格納する `Extensions` ディレクトリを作成しました。

<a name="registering-the-driver"></a>
#### ドライバを登録する

ドライバが実装されたら、Laravel に登録する準備が整います。追加のドライバをPennant に追加するには、`Feature` ファサードによって提供される `extend` メソッドを使用できます。アプリケーションの [サービスプロバイダ](/docs/{{version}}/providers) のいずれかの `boot` メソッドから `extend` メソッドを呼び出す必要があります。

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
### 機能の外部定義

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

`definedFeaturesForScope` メソッドは、指定されたスコープに対して定義された機能名のリストを返す必要があります。

<a name="events"></a>
## イベント (Events)

Pennant は、アプリケーション全体で機能フラグを追跡するときに役立つさまざまなイベントを送出します。

### `Laravel\Pennant\Events\FeatureRetrieved`

このイベントは、[機能がチェックされています](#checking-features) が発生するたびに送出されます。このイベントは、アプリケーション全体での機能フラグの使用状況に対するメトリクスの作成と追跡に役立つ場合があります。

### `Laravel\Pennant\Events\FeatureResolved`

このイベントは、特定のスコープに対して機能の値が初めて解決されるときに送出されます。

### `Laravel\Pennant\Events\UnknownFeatureResolved`

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

### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

このイベントは、リクエスト中に [クラスベースの機能](#class-based-features) が初めて動的にチェックされるときに送出されます。

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

このイベントは、`null` スコープが [nullはサポートしていません](#nullable-scope) の機能定義に渡されたときに送出されます。

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

### `Laravel\Pennant\Events\FeatureUpdated`

このイベントは、通常は `activate` または `deactivate` を呼び出すことによって、スコープの機能を更新するときに送出されます。

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

このイベントは、通常は `activateForEveryone` または `deactivateForEveryone` を呼び出すことによって、すべてのスコープの機能を更新するときに送出されます。

### `Laravel\Pennant\Events\FeatureDeleted`

このイベントは、通常は `forget` を呼び出すことによって、スコープの機能を削除するときに送出されます。

### `Laravel\Pennant\Events\FeaturesPurged`

このイベントは、特定の機能を削除するときに送出されます。

### `Laravel\Pennant\Events\AllFeaturesPurged`

このイベントは、すべての機能を削除するときに送出されます。

