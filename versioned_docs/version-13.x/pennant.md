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
    - [Global Scope](#global-scope)
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
[Laravel Pennant](https://github.com/laravel/pennant)는 불필요한 요소 없이 간단하고 가벼운 기능 플래그(feature flag) 패키지입니다. 기능 플래그는 새로운 애플리케이션 기능을 점진적으로 배포하거나, 인터페이스 디자인에 대한 A/B 테스트를 실행하거나, trunk 기반 개발 전략을 보완하는 등 다양한 활용이 가능합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Pennant into your project using the Composer package manager: -->
먼저, Composer 패키지 관리자를 사용해 Pennant를 프로젝트에 설치합니다.

```shell
composer require laravel/pennant
```

<!-- Next, you should publish the Pennant configuration and migration files using the `vendor:publish` Artisan command: -->
다음으로, `vendor:publish` Artisan 명령어를 통해 Pennant의 구성 및 마이그레이션 파일을 퍼블리시합니다.

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

<!-- Finally, you should run your application's database migrations. This will create a `features` table that Pennant uses to power its `database` driver: -->
마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 과정에서 Pennant가 사용하는 `features` 테이블이 생성되어 `database` 드라이버를 사용할 수 있게 됩니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to specify the default storage mechanism that will be used by Pennant to store resolved feature flag values. -->
Pennant의 자산을 퍼블리시 한 후에는 `config/pennant.php`에서 구성 파일을 확인할 수 있습니다. 이 파일에서는 Pennant가 기능 플래그의 값을 저장할 때 사용할 기본 저장소 방식을 지정할 수 있습니다.

<!-- Pennant includes support for storing resolved feature flag values in an in-memory array via the `array` driver. Or, Pennant can store resolved feature flag values persistently in a relational database via the `database` driver, which is the default storage mechanism used by Pennant. -->
Pennant는 인메모리 배열에 기능 값을 저장할 수 있는 `array` 드라이버와, 영구적으로 관계형 데이터베이스에 기능 값을 저장하는 `database` 드라이버(기본값)를 지원합니다.

<a name="defining-features"></a>
<!-- ## Defining Features -->
## Defining Features

<!-- To define a feature, you may use the `define` method offered by the `Feature` facade. You will need to provide a name for the feature, as well as a closure that will be invoked to resolve the feature's initial value. -->
기능을 정의하려면 `Feature` 파사드의 `define` 메서드를 사용합니다. 기능의 이름과 해당 기능의 초기 값을 반환할 클로저를 지정해야 합니다.

<!-- Typically, features are defined in a service provider using the `Feature` facade. The closure will receive the "scope" for the feature check. Most commonly, the scope is the currently authenticated user. In this example, we will define a feature for incrementally rolling out a new API to our application's users: -->
일반적으로 기능 정의는 서비스 프로바이더에서 `Feature` 파사드를 사용하여 이루어집니다. 클로저는 기능 확인 시 "스코프"를 전달받으며, 가장 흔하게는 현재 인증된 사용자가 스코프가 됩니다. 다음은 애플리케이션 사용자들을 대상으로 새로운 API를 점진적으로 롤아웃하는 예시입니다.

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
위 예시처럼 다음과 같은 규칙으로 기능을 정의할 수 있습니다.

<!-- - All internal team members should be using the new API. - Any high traffic customers should not be using the new API. - Otherwise, the feature should be randomly assigned to users with a 1 in 100 chance of being active. -->
- 내부 팀 멤버는 모두 새로운 API를 사용해야 합니다.
- 트래픽이 많은 고객은 새로운 API를 사용하지 않습니다.
- 그 외 나머지 사용자에 대해서는 1/100 확률로 기능이 활성화됩니다.

<!-- The first time the `new-api` feature is checked for a given user, the result of the closure will be stored by the storage driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the closure will not be invoked. -->
특정 사용자에 대한 `new-api` 기능이 처음으로 확인될 때, 클로저의 결과가 저장소 드라이버에 저장됩니다. 이후 같은 사용자에 대해 기능이 다시 확인되면, 저장하고 있던 값을 사용하며, 클로저는 다시 호출되지 않습니다.

<!-- For convenience, if a feature definition only returns a lottery, you may omit the closure completely: -->
편의를 위해, 기능 정의가 단순히 Lottery만 반환한다면 클로저를 생략할 수 있습니다.

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
<!-- ### Class Based Features -->
### Class Based Features

<!-- Pennant also allows you to define class-based features. Unlike closure-based feature definitions, there is no need to register a class-based feature in a service provider. To create a class-based feature, you may invoke the `pennant:feature` Artisan command. By default, the feature class will be placed in your application's `app/Features` directory: -->
Pennant는 클로저 기반 정의 외에 클래스 기반으로도 기능을 정의할 수 있습니다. 클래스 기반 기능은 서비스 프로바이더에 직접 등록할 필요가 없습니다. 클래스 기반 기능을 만들려면 `pennant:feature` Artisan 명령어를 사용하세요. 기본적으로 해당 클래스는 `app/Features` 디렉터리에 생성됩니다.

```shell
php artisan pennant:feature NewApi
```

<!-- When writing a feature class, you only need to define a `resolve` method, which will be invoked to resolve the feature's initial value for a given scope. Again, the scope will typically be the currently authenticated user: -->
기능 클래스에서는 `resolve` 메서드만 정의하면 됩니다. 이 메서드는 주어진 스코프(보통 인증된 사용자)에 대해 기능의 초기 값을 반환합니다.

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
클래스 기반 기능의 인스턴스를 직접 생성하고 싶다면 `Feature` 파사드의 `instance` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 [container](/docs/13.x/container)로부터 해결되므로, 생성자에 의존성을 자유롭게 주입할 수 있습니다.

<!-- #### Customizing the Stored Feature Name -->
#### Customizing the Stored Feature Name

<!-- By default, Pennant will store the feature class's fully qualified class name. If you would like to decouple the stored feature name from the application's internal structure, you may add the `Name` attribute on the feature class. The value of this attribute will be stored in place of the class name: -->
기본적으로 Pennant는 기능 클래스의 전체 네임스페이스를 저장합니다. 저장되는 기능 이름을 코드 구조와 분리하고 싶다면, 클래스에 `Name` 속성(attribute)을 달 수 있습니다. 이 속성의 값이 클래스 이름 대신 저장됩니다.

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
기능이 활성화되어 있는지 확인하려면 `Feature` 파사드의 `active` 메서드 사용이 가장 기본적인 방법입니다. 기본적으로, 기능은 현재 인증된 사용자를 기준으로 확인됩니다.

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
기본 동작은 현재 인증된 사용자로 기능을 확인하지만, `Feature` 파사드가 제공하는 `for` 메서드를 사용해 특정 사용자나 [scope](#scope)를 지정해 확인할 수도 있습니다.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

<!-- Pennant also offers some additional convenience methods that may prove useful when determining if a feature is active or not: -->
Pennant에는 기능의 활성/비활성 여부를 확인할 때 유용한 여러 가지 편의 메서드도 제공됩니다.

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
> Artisan 명령어 또는 큐 작업 등 HTTP 컨텍스트 밖에서 Pennant를 사용할 경우, [explicitly specify the feature's scope](#specifying-the-scope)하는 것이 일반적입니다. 또는, [default scope](#default-scope)를 지정해 인증된 HTTP/비인증 상황 모두에 대응할 수 있습니다.

<a name="checking-class-based-features"></a>
<!-- #### Checking Class Based Features -->
#### Checking Class Based Features

<!-- For class-based features, you should provide the class name when checking the feature: -->
클래스 기반 기능을 확인할 때는 기능 클래스의 이름을 전달해야 합니다.

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
`when` 메서드를 사용하면 기능이 활성화된 경우 지정한 클로저를, 비활성화된 경우 두 번째 클로저를 실행할 수 있습니다.

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
`unless` 메서드는 `when`의 반대로, 기능이 비활성 상태일 때 첫 번째 클로저가 실행됩니다.

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
Pennant의 `HasFeatures` 트레이트를 `User` 모델 또는 기능을 가져야 하는 다른 모델에 추가하면, 모델에서 직접 기능을 편리하게 확인할 수 있는 메서드를 제공합니다.

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
트레이트를 모델에 추가하면, `features` 메서드를 통해 기능을 쉽게 확인할 수 있습니다.

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

<!-- Of course, the `features` method provides access to many other convenient methods for interacting with features: -->
`features` 메서드는 다양한 편의 메서드를 제공합니다.

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
Pennant는 Blade에서 기능을 쉽게 확인할 수 있도록 `@feature`와 `@featureany` 디렉티브를 제공합니다.

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
Pennant에는 인증된 사용자가 기능에 접근 권한이 있는지 라우트 호출 전에 검사할 수 있는 [middleware](/docs/13.x/middleware)가 포함되어 있습니다. 미들웨어를 라우트에 할당하고, 접근이 필요한 기능을 지정하면, 지정된 기능들 중 하나라도 비활성 상태라면 해당 라우트는 `400 Bad Request` HTTP 응답을 반환합니다. 여러 기능은 `using` 메서드에 나열할 수 있습니다.

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
지정한 기능 중 하나라도 비활성 상태라면 미들웨어가 반환하는 응답을 사용자 지정 하고 싶다면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용하세요. 이 메서드는 주로 애플리케이션의 서비스 프로바이더 `boot` 메서드 내에서 호출합니다.

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
경우에 따라 저장된 기능 값을 가져오기 전에 인메모리에서 추가적인 검사를 하는 것이 필요할 수 있습니다. 예를 들어, 새로운 API를 기능 플래그 뒤에서 개발하고 있는데, 저장소의 기존 기능 값은 유지하면서도 API를 신속하게 전체 비활성화하고 싶을 수 있습니다. 버그가 발견되면 내부 팀을 제외한 모든 사용자에게 기능을 끄고 수정 후 다시 활성화할 수도 있습니다.

<!-- You can achieve this with a [class-based feature's](#class-based-features) `before` method. When present, the `before` method is always run in-memory before retrieving the value from storage. If a non-`null` value is returned from the method, it will be used in place of the feature's stored value for the duration of the request: -->
이런 상황에서는 [class-based feature's](#class-based-features)의 `before` 메서드를 활용할 수 있습니다. `before` 메서드는 저장소에서 값을 가져오기 전에 항상 인메모리에서 실행되며, 이 메서드에서 `null`이 아닌 값을 반환하면 저장된 값 대신 해당 값을 이번 요청 동안 사용합니다.

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
기능 플래그 뒤에 있던 기능을 글로벌하게 롤아웃 하고 싶을 때도 사용할 수 있습니다.

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
기능을 확인하면 Pennant는 결과를 인메모리 캐시에 저장합니다. `database` 드라이버를 사용할 경우, 한 요청 내에서 동일한 기능에 대해 반복적으로 확인해도 추가 데이터베이스 쿼리가 발생하지 않습니다. 따라서 요청이 끝날 때까지 일관된 결과를 얻을 수 있습니다.

<!-- If you need to manually flush the in-memory cache, you may use the `flushCache` method offered by the `Feature` facade: -->
인메모리 캐시를 수동으로 비우려면 `Feature` 파사드의 `flushCache` 메서드를 사용하세요.

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
기능은 주로 현재 인증된 사용자를 기준으로 확인하지만, 언제나 이런 방식이 적합한 것은 아닙니다. 따라서, `Feature` 파사드의 `for` 메서드를 사용해 기능을 확인하려는 스코프를 명시할 수 있습니다.

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

<!-- Of course, feature scopes are not limited to "users". Imagine you have built a new billing experience that you are rolling out to entire teams rather than individual users. Perhaps you would like the oldest teams to have a slower rollout than the newer teams. Your feature resolution closure might look something like the following: -->
스코프는 "사용자"에만 제한되지 않습니다. 예를 들어, 개별 사용자 대신 전체 팀 단위로 새로운 결제 경험을 롤아웃한다고 가정해봅시다. 오래된 팀일수록 롤아웃 속도를 조절할 수도 있습니다.

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
예시처럼 기능 확인 클로저에서 `User` 대신 `Team` 모델을 파라미터로 받을 수도 있습니다. 이 경우 사용자 팀의 기능 활성 여부를 확인하려면 `Feature` 파사드가 제공하는 `for` 메서드에 팀을 전달하세요.

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="global-scope"></a>
<!-- ### Global Scope -->
### Global Scope

<!-- To check or interact with a feature using a global scope, regardless of the configured default scope resolver, use the `globally` method. This is useful for application-wide feature flags, such as temporarily enabling maintenance behavior or rolling out a feature to every user: -->
글로벌 스코프를 사용해 기능을 확인하거나 상호작용하려면, 설정된 기본 스코프 리졸버와 관계없이 `globally` 메서드를 사용합니다. 이는 애플리케이션 전체에 적용되는 기능 플래그에 유용하며, 예를 들어 유지보수 동작을 일시적으로 활성화하거나 모든 사용자에게 기능을 단계적으로 출시할 때 사용할 수 있습니다:

```php
Feature::globally()->active('new-api');

Feature::globally()->activate('new-api');
```

<a name="default-scope"></a>
<!-- ### Default Scope -->
### Default Scope

<!-- It is also possible to customize the default scope Pennant uses to check features. For example, maybe all of your features are checked against the currently authenticated user's team instead of the user. Instead of having to call `Feature::for($user->team)` every time you check a feature, you may instead specify the team as the default scope. Typically, this should be done in one of your application's service providers: -->
Pennant가 기능 확인 시 사용할 기본 스코프를 변경할 수도 있습니다. 예를 들어, 모든 기능을 인증된 사용자가 아닌, 사용자의 팀 단위로 확인하도록 하고 싶을 때마다 `Feature::for($user->team)`을 반복적으로 작성하지 않아도 됩니다. 이 경우 서비스 프로바이더에서 기본 스코프를 지정하세요.

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
이제 `for` 메서드를 명시적으로 사용하지 않아도, 기능 확인 시 인증된 사용자의 팀이 기본 스코프로 사용됩니다.

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
<!-- ### Nullable Scope -->
### Nullable Scope

<!-- If the scope you provide when checking a feature is `null` and the feature's definition does not support `null` via a nullable type or by including `null` in a union type, Pennant will automatically return `false` as the feature's result value. -->
기능 확인 시 지정하는 스코프가 `null`이고, 해당 기능 정의에서 nullable 타입이나 union 타입에 `null`을 포함하는 방식으로 `null`을 지원하지 않는다면, Pennant는 자동으로 해당 기능의 결과를 `false`로 반환합니다.

<!-- So, if the scope you are passing to a feature is potentially `null` and you want the feature's value resolver to be invoked, you should account for that in your feature's definition. A `null` scope may occur if you check a feature within an Artisan command, queued job, or unauthenticated route. Since there is usually not an authenticated user in these contexts, the default scope will be `null`. -->
따라서, 전달하는 스코프가 `null`일 수 있고, 스코프가 `null`이어도 기능 값 해석기를 실행하고 싶다면, 기능 정의에서 이를 처리해야 합니다. Artisan 명령, 큐 작업, 인증되지 않은 라우트 등에서는 보통 인증된 사용자가 없어 기본 스코프가 `null`이 될 수 있습니다.

<!-- If you do not always [explicitly specify your feature scope](#specifying-the-scope) then you should ensure the scope's type is "nullable" and handle the `null` scope value within your feature definition logic: -->
명시적으로 [explicitly specify your feature scope](#specifying-the-scope)하지 않는 경우, 파라미터 타입에 `null`을 허용하고 기능 정의 내에서 적절히 처리해야 합니다.

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
Pennant 기본 제공 `array` 및 `database` 저장소 드라이버는 모든 PHP 데이터 타입 및 Eloquent 모델에 대해 스코프 식별자를 알맞게 저장할 수 있습니다. 그러나 서드파티 Pennant 드라이버를 사용하는 경우, 해당 드라이버가 Eloquent 모델이나 커스텀 타입을 올바르게 처리하지 못할 수도 있습니다.

<!-- In light of this, Pennant allows you to format scope values for storage by implementing the `FeatureScopeable` contract on the objects in your application that are used as Pennant scopes. -->
이러한 상황에서는 애플리케이션 내 Pennant 스코프로 사용하는 객체에 `FeatureScopeable` 계약(Contract)을 구현하여, 저장 시 사용할 값을 직접 지정할 수 있습니다.

<!-- For example, imagine you are using two different feature drivers in a single application: the built-in `database` driver and a third-party "Flag Rocket" driver. The "Flag Rocket" driver does not know how to properly store an Eloquent model. Instead, it requires a `FlagRocketUser` instance. By implementing the `toFeatureIdentifier` defined by the `FeatureScopeable` contract, we can customize the storable scope value provided to each driver used by our application: -->
예를 들어, 하나의 애플리케이션 내에서 기본 `database` 드라이버와 서드파티 "Flag Rocket" 드라이버를 사용하는 상황이라고 가정해봅시다. "Flag Rocket" 드라이버는 Eloquent 모델이 아닌 `FlagRocketUser` 인스턴스를 필요로 합니다. 이럴 때 `FeatureScopeable` 계약의 `toFeatureIdentifier` 메서드를 구현하여, 각 드라이버별로 알맞은 값을 반환할 수 있습니다.

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
Pennant는 기본적으로, Eloquent 모델에 연관된 기능을 저장할 때 완전한 클래스 이름(fully qualified class name)을 사용합니다. 이미 [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant도 morph map을 이용해 저장된 기능과 애플리케이션 구조 간의 결합도를 낮출 수 있습니다.

<!-- To achieve this, after defining your Eloquent morph map in a service provider, you may invoke the `Feature` facade's `useMorphMap` method: -->
서비스 프로바이더에서 morph map을 정의한 후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하세요.

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
지금까지 주로 기능의 상태를 "활성/비활성"의 이진(binary) 값으로 다뤘지만, Pennant는 다양한 값도 저장할 수 있습니다.

<!-- For example, imagine you are testing three new colors for the "Buy now" button of your application. Instead of returning `true` or `false` from the feature definition, you may instead return a string: -->
예를 들어, "구매하기" 버튼의 색상을 세 가지로 테스트한다고 할 때, 기능 정의에서 `true` 또는 `false` 대신 임의의 문자열 값을 반환하게 할 수 있습니다.

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
`purchase-button` 기능의 값을 조회할 때는 `value` 메서드를 사용합니다.

```php
$color = Feature::value('purchase-button');
```

<!-- Pennant's included Blade directive also makes it easy to conditionally render content based on the current value of the feature: -->
Pennant의 Blade 디렉티브를 사용하면, 해당 기능 값에 따라 템플릿을 다르게 렌더링 할 수 있습니다.

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
> 풍부한 값을 사용하는 경우, 값이 `false`가 아니기만 하면 기능이 "활성"으로 간주됩니다.

<!-- When calling the [conditional `when`](#conditional-execution) method, the feature's rich value will be provided to the first closure: -->
[conditional `when`](#conditional-execution) 메서드를 사용할 때는, 기능의 풍부한 값이 첫 번째 클로저에 전달됩니다.

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

<!-- Likewise, when calling the conditional `unless` method, the feature's rich value will be provided to the optional second closure: -->
마찬가지로 `unless` 메서드를 사용할 경우, 두 번째(옵션) 클로저에 풍부한 값이 전달됩니다.

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
`values` 메서드를 사용하면, 주어진 스코프에서 여러 기능 값을 한꺼번에 조회할 수 있습니다.

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

<!-- Or, you may use the `all` method to retrieve the values of all defined features for a given scope: -->
또는, `all` 메서드로 주어진 스코프에 대해 정의된 모든 기능의 값을 가져올 수 있습니다.

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

<!-- However, class-based features are dynamically registered and are not known by Pennant until they are explicitly checked. This means your application's class-based features may not appear in the results returned by the `all` method if they have not already been checked during the current request. -->
단, Pennant는 클래스 기반 기능을 요청 시 동적으로 등록하므로, 해당 기능이 현재 요청에서 이미 확인된 적이 없다면 `all` 메서드가 반환하는 결과에 나타나지 않을 수 있습니다.

<!-- If you would like to ensure that feature classes are always included when using the `all` method, you may use Pennant's feature discovery capabilities. To get started, invoke the `discover` method in one of your application's service providers: -->
모든 feature 클래스가 `all` 호출 시 항상 포함되게 하려면, Pennant의 기능 자동 발견(discovery) 기능을 활용해야 합니다. 서비스 프로바이더에서 `discover` 메서드를 호출해보세요.

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
`discover` 메서드는 애플리케이션의 `app/Features` 디렉터리 내 모든 feature 클래스를 등록합니다. 이후 `all` 메서드의 결과에 체크되지 않았던 클래스도 포함됩니다.

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
Pennant는 한 요청 내에 확인된 모든 기능 값을 인메모리 캐시에 유지하지만, 퍼포먼스 문제가 발생할 수도 있습니다. 이를 해결하기 위해 Pennant는 기능 값을 미리 적재(eager loading)하는 기능을 제공합니다.

<!-- To illustrate this, imagine that we are checking if a feature is active within a loop: -->
예를 들어, 아래처럼 루프 내부에서 기능을 확인할 때를 생각해보세요.

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

<!-- Assuming we are using the database driver, this code will execute a database query for every user in the loop - executing potentially hundreds of queries. However, using Pennant's `load` method, we can remove this potential performance bottleneck by eager loading the feature values for a collection of users or scopes: -->
database 드라이버를 사용할 경우, 각 사용자마다 쿼리가 발생해 수백 번 쿼리될 수 있습니다. 하지만 Pennant의 `load` 메서드를 사용하면, 전체 컬렉션에 대해 기능 값을 미리 적재하여 퍼포먼스 병목을 제거할 수 있습니다.

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

<!-- To load feature values only when they have not already been loaded, you may use the `loadMissing` method: -->
이미 적재된 기능 값은 다시 적재하지 않고 필요한 것만 불러오고 싶다면 `loadMissing` 메서드를 사용합니다.

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

<!-- You may load all defined features using the `loadAll` method: -->
정의된 모든 기능을 한꺼번에 로딩하려면 `loadAll` 메서드를 사용합니다.

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
<!-- ## Updating Values -->
## Updating Values

<!-- When a feature's value is resolved for the first time, the underlying driver will store the result in storage. This is often necessary to ensure a consistent experience for your users across requests. However, at times, you may want to manually update the feature's stored value. -->
처음 기능 값이 결정될 때, 해당 값은 저장소에 저장됩니다. 이는 여러 요청에서 사용자 경험을 일관되게 제공하기 위해 필요합니다. 하지만, 때로는 저장된 값을 수동으로 업데이트해야 할 수도 있습니다.

<!-- To accomplish this, you may use the `activate` and `deactivate` methods to toggle a feature "on" or "off": -->
이럴 때는 `activate`와 `deactivate` 메서드를 사용해 기능을 "켜기" 또는 "끄기" 할 수 있습니다.

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```

<!-- It is also possible to manually set a rich value for a feature by providing a second argument to the `activate` method: -->
풍부한 값을 설정하려면 `activate` 메서드에 값을 두 번째 인자로 전달하면 됩니다.

```php
Feature::activate('purchase-button', 'seafoam-green');
```

<!-- To instruct Pennant to forget the stored value for a feature, you may use the `forget` method. When the feature is checked again, Pennant will resolve the feature's value from its feature definition: -->
저장된 기능 값을 제거하려면 `forget` 메서드를 사용하세요. 다시 기능이 확인될 때, 기능 정의에서 새 값을 가져옵니다.

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
<!-- ### Bulk Updates -->
### Bulk Updates

<!-- To update stored feature values in bulk, you may use the `activateForEveryone` and `deactivateForEveryone` methods. -->
저장된 기능 값을 대량으로 업데이트하려면 `activateForEveryone`과 `deactivateForEveryone`을 사용하세요.

<!-- For example, imagine you are now confident in the `new-api` feature's stability and have landed on the best `'purchase-button'` color for your checkout flow - you can update the stored value for all users accordingly: -->
예를 들어, `new-api`의 안정성을 확신하게 되었고 결제 플로우에 가장 적합한 `'purchase-button'` 색상을 채택했다면, 모든 사용자에 대해 값을 다음과 같이 변경할 수 있습니다.

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

<!-- Alternatively, you may deactivate the feature for all users: -->
모든 사용자에 대해 기능을 비활성화하려면 아래처럼 사용합니다.

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 작업은 Pennant 저장소에 저장된 resolved 값을 업데이트합니다. 애플리케이션의 기능 정의도 함께 변경하는 것이 필요합니다.

<a name="purging-features"></a>
<!-- ### Purging Features -->
### Purging Features

<!-- Sometimes, it can be useful to purge an entire feature from storage. This is typically necessary if you have removed the feature from your application or you have made adjustments to the feature's definition that you would like to rollout to all users. -->
경우에 따라 전체 기능을 저장소에서 삭제(purge)하는 것이 유용합니다. 일반적으로 기능 자체를 애플리케이션에서 제거하거나, 기능 정의 자체를 조정해 모든 사용자에게 일괄 반영할 때 사용합니다.

<!-- You may remove all stored values for a feature using the `purge` method: -->
`purge` 메서드를 사용해 특정 기능의 모든 저장값을 제거할 수 있습니다.

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```

<!-- If you would like to purge _all_ features from storage, you may invoke the `purge` method without any arguments: -->
모든 기능을 한꺼번에 삭제하려면 인자 없이 `purge`를 호출하세요.

```php
Feature::purge();
```

<!-- As it can be useful to purge features as part of your application's deployment pipeline, Pennant includes a `pennant:purge` Artisan command which will purge the provided features from storage: -->
배포 파이프라인의 일부로 purge하는 것이 필요할 때가 있으므로, Pennant에는 편리하게 `pennant:purge` Artisan 명령어가 준비되어 있습니다.

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

<!-- It is also possible to purge all features _except_ those in a given feature list. For example, imagine you wanted to purge all features but keep the values for the "new-api" and "purchase-button" features in storage. To accomplish this, you can pass those feature names to the `--except` option: -->
특정 기능은 그대로 두고 나머지만 삭제하고 싶다면 `--except` 옵션에 보존할 기능 이름을 전달하세요.

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

<!-- For convenience, the `pennant:purge` command also supports an `--except-registered` flag. This flag indicates that all features except those explicitly registered in a service provider should be purged: -->
또한, 편의를 위해 `pennant:purge` 명령어는 `--except-registered` 플래그도 지원합니다. 이 플래그는 서비스 프로바이더에 명시적으로 등록된 기능을 제외한 나머지 모든 기능을 삭제하도록 지정합니다.

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- When testing code that interacts with feature flags, the easiest way to control the feature flag's returned value in your tests is to simply re-define the feature. For example, imagine you have the following feature defined in one of your application's service provider: -->
기능 플래그와 상호작용하는 코드를 테스트할 때, 테스트 내에서 간단히 기능을 재정의하여 원하는 반환 값을 지정하는 것이 가장 쉬운 방법입니다. 예를 들어, 아래처럼 서비스 프로바이더에서 기능을 정의했다고 가정해봅시다.

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
테스트에서는 기능의 반환 값을 고정하여 재정의할 수 있습니다. 아래 테스트는 서비스 프로바이더의 `Arr::random()` 구현과 상관없이 항상 통과합니다.

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
클래스 기반 기능에도 동일한 방식이 적용됩니다.

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
기능이 `Lottery` 인스턴스를 반환하는 경우, [testing helpers available](/docs/13.x/helpers#testing-lotteries)를 활용할 수 있습니다.

<a name="store-configuration"></a>
<!-- #### Store Configuration -->
#### Store Configuration

<!-- You may configure the store that Pennant will use during testing by defining the `PENNANT_STORE` environment variable in your application's `phpunit.xml` file: -->
테스트 중 사용할 Pennant 저장소는 `phpunit.xml` 파일 내 `PENNANT_STORE` 환경 변수로 지정할 수 있습니다.

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
기존 Pennant 저장소 드라이버로 애플리케이션 요구사항을 충족할 수 없다면, 직접 저장소 드라이버를 구현할 수 있습니다. 커스텀 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 반드시 구현해야 합니다.

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
이제 각 메서드는 Redis 커넥션 등을 이용해 구현하면 됩니다. 자세한 구현 예시는 [Pennant source code](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)의 `Laravel\Pennant\Drivers\DatabaseDriver`를 참고하세요.

> [!NOTE]
> Laravel은 확장 기능(Extension)을 위한 디렉터리를 제공하지 않습니다. 자유롭게 원하시는 곳에 두시면 됩니다. 본 예시에서는 `Extensions` 디렉터리에 `RedisFeatureDriver`를 생성했습니다.

<a name="registering-the-driver"></a>
<!-- #### Registering the Driver -->
#### Registering the Driver

<!-- Once your driver has been implemented, you are ready to register it with Laravel. To add additional drivers to Pennant, you may use the `extend` method provided by the `Feature` facade. You should call the `extend` method from the `boot` method of one of your application's [service provider](/docs/13.x/providers): -->
드라이버 구현을 마쳤다면, Laravel에 등록해서 사용할 수 있습니다. 추가 드라이버 등록은 `Feature` 파사드가 제공하는 `extend` 메서드로 할 수 있습니다. `extend` 메서드는 애플리케이션의 [service provider](/docs/13.x/providers) 중 하나의 `boot` 메서드에서 호출하세요.

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
이제 드라이버를 등록하면, `config/pennant.php` 구성 파일에서 `redis` 드라이버를 사용할 수 있습니다.

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
드라이버가 서드파티 기능 플래그 플랫폼을 감싸는(wrapper) 형태라면, Pennant의 `Feature::define` 메서드를 사용하지 않고 외부 플랫폼에서 기능을 정의할 가능성이 높습니다. 이 경우, 커스텀 드라이버에는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 구현해야 합니다.

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
`definedFeaturesForScope` 메서드는 주어진 스코프에 대해 정의된 기능 이름 목록을 반환해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Pennant dispatches a variety of events that can be useful when tracking feature flags throughout your application. -->
Pennant는 기능 플래그를 추적할 때 유용한 다양한 이벤트를 디스패치합니다.

<!-- ### `Laravel\Pennant\Events\FeatureRetrieved` -->
### `Laravel\Pennant\Events\FeatureRetrieved`

<!-- This event is dispatched whenever a [feature is checked](#checking-features). This event may be useful for creating and tracking metrics against a feature flag's usage throughout your application. -->
이 이벤트는 [feature is checked](#checking-features)될 때마다 발생합니다. 기능 플래그 사용량 메트릭을 기록하는 데 활용할 수 있습니다.

<!-- ### `Laravel\Pennant\Events\FeatureResolved` -->
### `Laravel\Pennant\Events\FeatureResolved`

<!-- This event is dispatched the first time a feature's value is resolved for a specific scope. -->
이벤트는 특정 스코프에 대해 처음으로 기능 값이 결정(resolved)될 때 발생합니다.

<!-- ### `Laravel\Pennant\Events\UnknownFeatureResolved` -->
### `Laravel\Pennant\Events\UnknownFeatureResolved`

<!-- This event is dispatched the first time an unknown feature is resolved for a specific scope. Listening to this event may be useful if you have intended to remove a feature flag but have accidentally left stray references to it throughout your application: -->
이 이벤트는 특정 스코프에 대해 처음으로 "알 수 없는" 기능이 확인된 경우 발생합니다. 기능 플래그를 제거할 의도로 남겨둔 코드에서 실수로 참조가 남아 있을 때 추적할 수 있습니다.

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
이 이벤트는 [class-based feature](#class-based-features)이 요청 중 처음 동적으로 확인될 때 디스패치됩니다.

<!-- ### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered` -->
### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

<!-- This event is dispatched when a `null` scope is passed to a feature definition that [doesn't support null](#nullable-scope). -->
이 이벤트는 [doesn't support null](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

<!-- This situation is handled gracefully and the feature will return `false`. However, if you would like to opt out of this feature's default graceful behavior, you may register a listener for this event in the `boot` method of your application's `AppServiceProvider`: -->
이 상황은 기본적으로 문제없이 처리되어 해당 기능의 반환 값은 `false`가 됩니다. 그러나 이러한 동작을 비활성화하고 싶을 때는, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에 이 이벤트에 대한 리스너를 등록할 수 있습니다.

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
이벤트는 보통 `activate` 또는 `deactivate` 호출 등으로 특정 스코프의 기능을 업데이트할 때 발생합니다.

<!-- ### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes` -->
### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

<!-- This event is dispatched when updating a feature for all scopes, usually by calling `activateForEveryone` or `deactivateForEveryone`. -->
이벤트는 보통 `activateForEveryone` 또는 `deactivateForEveryone` 호출 등으로 모든 스코프의 기능을 업데이트할 때 발생합니다.

<!-- ### `Laravel\Pennant\Events\FeatureDeleted` -->
### `Laravel\Pennant\Events\FeatureDeleted`

<!-- This event is dispatched when deleting a feature for a scope, usually by calling `forget`. -->
이 이벤트는 보통 `forget` 메서드 호출 등으로 특정 스코프의 기능을 삭제할 때 발생합니다.

<!-- ### `Laravel\Pennant\Events\FeaturesPurged` -->
### `Laravel\Pennant\Events\FeaturesPurged`

<!-- This event is dispatched when purging specific features. -->
이벤트는 특정 기능들을 purge(삭제)할 때 발생합니다.

<!-- ### `Laravel\Pennant\Events\AllFeaturesPurged` -->
### `Laravel\Pennant\Events\AllFeaturesPurged`

<!-- This event is dispatched when purging all features. -->
이벤트는 모든 기능을 purge(삭제)할 때 발생합니다.
