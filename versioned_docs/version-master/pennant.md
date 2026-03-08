# Laravel Pennant (Laravel Pennant)

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
- [기능 플래그 정의](#defining-features)
    - [클래스 기반 기능 플래그](#class-based-features)
- [기능 플래그 확인](#checking-features)
    - [조건부 실행](#conditional-execution)
    - [`HasFeatures` 트레이트](#the-has-features-trait)
    - [Blade 지시어](#blade-directive)
    - [미들웨어](#middleware)
    - [기능 플래그 확인 가로채기](#intercepting-feature-checks)
    - [인메모리 캐시](#in-memory-cache)
- [스코프](#scope)
    - [스코프 지정하기](#specifying-the-scope)
    - [기본 스코프](#default-scope)
    - [Nullable 스코프](#nullable-scope)
    - [스코프 식별](#identifying-scope)
    - [스코프 직렬화](#serializing-scope)
- [리치 값 기능 플래그](#rich-feature-values)
- [여러 기능 플래그 값 조회](#retrieving-multiple-features)
- [Eager 로딩](#eager-loading)
- [값 업데이트](#updating-values)
    - [일괄 업데이트](#bulk-updates)
    - [기능 플래그 일괄 정리](#purging-features)
- [테스트](#testing)
- [커스텀 Pennant 드라이버 추가](#adding-custom-pennant-drivers)
    - [드라이버 구현](#implementing-the-driver)
    - [드라이버 등록](#registering-the-driver)
    - [외부에서 기능 플래그 정의](#defining-features-externally)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel Pennant](https://github.com/laravel/pennant)는 복잡함 없이 간단하고 가벼운 기능 플래그(feature flag) 패키지입니다. 기능 플래그를 사용하면 새로운 애플리케이션 기능을 점진적으로 사용자에게 배포할 수 있으며, 새로운 인터페이스 디자인에 대한 A/B 테스트를 하거나 trunk-based 개발 전략을 보완하는 등 다양한 목적으로 활용할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 Pennant를 프로젝트에 설치합니다:

```shell
composer require laravel/pennant
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pennant의 설정 파일과 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이를 통해 Pennant의 `database` 드라이버 구동에 필요한 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
## 설정

Pennant의 에셋을 게시한 후에는 설정 파일이 `config/pennant.php`에 위치하게 됩니다. 이 설정 파일을 통해 Pennant가 기능 플래그 값을 저장할 기본 저장소 방식을 지정할 수 있습니다.

Pennant는 `array` 드라이버를 통해 인메모리 배열에 기능 플래그 값을 저장하거나, 기본값으로 설정된 `database` 드라이버를 사용하여 관계형 데이터베이스에 값들을 영구적으로 저장할 수 있습니다.

<a name="defining-features"></a>
## 기능 플래그 정의

기능(feature)을 정의하려면 `Feature` 파사드의 `define` 메서드를 사용합니다. 이때 기능의 이름과, 기능의 초깃값을 결정할 클로저를 제공해야 합니다.

일반적으로 기능은 서비스 프로바이더 내에서 `Feature` 파사드를 이용해 정의합니다. 클로저에는 기능 확인을 위한 "스코프(scope)"가 전달되는데, 주로 현재 인증된 사용자입니다. 아래 예시에서는 애플리케이션 사용자에게 새로운 API를 점진적으로 배포하는 기능을 정의하고 있습니다:

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
     * 애플리케이션 서비스 부트스트랩.
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

위 예시에서, 기능 활성화에 대한 규칙은 다음과 같습니다:

- 모든 내부 팀원은 새로운 API를 사용해야 합니다.
- 트래픽이 많은 고객은 새로운 API를 사용하지 않습니다.
- 그 외의 경우, 1/100의 확률로 사용자에게 기능이 활성화됩니다.

처음으로 특정 사용자에 대해 `new-api` 기능이 확인될 때, 클로저의 반환 결과가 저장소 드라이버에 저장됩니다. 이후 동일한 사용자에 대해 기능을 다시 확인하면 저장된 값이 반환되며, 클로저가 다시 호출되지 않습니다.

편의상, 기능이 단순히 로터리(lottery)만 반환하는 경우라면, 클로저 생략도 가능합니다:

```
Feature::define('site-redesign', Lottery::odds(1, 1000));
```

<a name="class-based-features"></a>
### 클래스 기반 기능 플래그

Pennant는 클래스 기반 기능 플래그 정의도 지원합니다. 클로저 기반과 달리, 클래스 기반 기능은 서비스 프로바이더에 등록할 필요가 없습니다. 클래스 기반 기능을 생성하려면 `pennant:feature` Artisan 명령어를 사용합니다. 기본적으로 해당 클래스는 애플리케이션의 `app/Features` 디렉토리에 생성됩니다:

```shell
php artisan pennant:feature NewApi
```

기능 클래스에서는 "resolve" 메서드만 정의하면 됩니다. 이 메서드는 주어진 스코프에 대한 기능의 초기 값을 결정합니다. 역시 스코프는 보통 인증된 사용자입니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 기능의 초기값을 결정합니다.
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

클래스 기반 기능의 인스턴스를 수동으로 생성하고 싶다면, `Feature` 파사드의 `instance` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Feature;

$instance = Feature::instance(NewApi::class);
```

> [!NOTE]
> 기능 클래스는 라라벨 [컨테이너](/docs/master/container)를 통해 인스턴스화되므로, 필요에 따라 기능 클래스의 생성자에 의존성을 주입할 수 있습니다.

#### 저장 기능 이름 커스터마이징

기본적으로 Pennant는 기능 클래스의 전체 네임스페이스(class name)을 저장합니다. 만약 저장되는 기능 이름을 애플리케이션 내부 구조와 분리하고 싶다면, 기능 클래스에 `Name` 속성을 부여할 수 있습니다. 이 속성 값이 클래스명 대신 저장됩니다:

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
## 기능 플래그 확인

기능이 활성화되어 있는지 판단하려면, `Feature` 파사드의 `active` 메서드를 사용하면 됩니다. 기본적으로 현재 인증된 사용자를 대상으로 기능을 확인합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * 리소스의 목록을 표시합니다.
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

물론, 인증된 사용자 외의 다른 사용자 또는 [스코프](#scope)에 대해 기능을 확인하는 것도 쉽습니다. 이때는 `Feature` 파사드의 `for` 메서드를 사용하면 됩니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

Pennant는 기능 활성 여부를 판단할 때 유용하게 사용할 수 있는 몇 가지 편리한 메서드도 제공합니다:

```php
// 주어진 모든 기능이 활성화되어 있는지 확인...
Feature::allAreActive(['new-api', 'site-redesign']);

// 주어진 기능들 중 하나라도 활성화되어 있는지 확인...
Feature::someAreActive(['new-api', 'site-redesign']);

// 기능이 비활성화 상태인지 확인...
Feature::inactive('new-api');

// 주어진 모든 기능이 비활성화 상태인지 확인...
Feature::allAreInactive(['new-api', 'site-redesign']);

// 주어진 기능들 중 하나라도 비활성화 상태인지 확인...
Feature::someAreInactive(['new-api', 'site-redesign']);
```

> [!NOTE]
> Artisan 명령어, 큐 작업 등 HTTP 컨텍스트 외부에서 Pennant를 사용할 때는 [기능의 스코프를 명시적으로 지정](#specifying-the-scope)하는 것이 일반적입니다. 또는 인증된 HTTP 컨텍스트와 비인증 컨텍스트 모두를 고려한 [기본 스코프](#default-scope)를 정의할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 플래그 확인

클래스 기반 기능의 경우, 기능 확인 시 클래스명을 전달해야 합니다:

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
     * 리소스의 목록을 표시합니다.
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
### 조건부 실행

`when` 메서드를 사용하면, 특정 기능이 활성화된 경우에만 클로저(익명 함수)를 실행할 수 있습니다. 또한, 두 번째 클로저를 통해 기능이 비활성화된 경우 실행할 로직도 지정할 수 있습니다:

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
     * 리소스의 목록을 표시합니다.
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

`unless` 메서드는 `when` 메서드의 반대로, 기능이 비활성화된 경우 첫 번째 클로저가 실행됩니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```

<a name="the-has-features-trait"></a>
### `HasFeatures` 트레이트

Pennant의 `HasFeatures` 트레이트를 애플리케이션의 `User` 모델(또는 기능 플래그를 사용하는 다른 모델)에 추가하면, 모델을 통해 직접 기능을 손쉽게 확인할 수 있습니다:

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

트레이트를 추가한 후에는 `features` 메서드를 통해 기능을 바로 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```

이 외에도 다양한 편의 메서드를 사용할 수 있습니다:

```php
// 값 가져오기...
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// 상태 확인...
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// 조건부 실행...
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
### Blade 지시어

Blade에서 기능 플래그를 손쉽게 확인할 수 있도록 Pennant는 `@feature` 및 `@featureany` 지시어를 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign'가 활성화되어 있을 때 -->
@else
    <!-- 'site-redesign'가 비활성화되어 있을 때 -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' 또는 `beta`가 활성화되어 있을 때 -->
@endfeatureany
```

<a name="middleware"></a>
### 미들웨어

Pennant는 [미들웨어](/docs/master/middleware)도 제공하여, 현재 인증된 사용자가 기능 플래그를 사용할 수 있는지 라우트가 실행되기 전에 검증할 수 있습니다. 해당 미들웨어를 라우트에 지정하고, 접근에 필요한 기능들을 명시할 수 있습니다. 지정된 기능 중 하나라도 비활성화되어 있다면, 해당 라우트는 `400 Bad Request` HTTP 응답을 반환합니다. 다수의 기능을 static `using` 메서드로 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```

<a name="customizing-the-response"></a>
#### 응답 커스터마이징

리스트된 기능이 비활성 상태일 때 미들웨어가 반환하는 응답을 커스터마이즈하고 싶다면, `EnsureFeaturesAreActive` 미들웨어의 `whenInactive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 서비스 프로바이더의 `boot` 메서드 내에서 호출합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * 애플리케이션 서비스 부트스트랩.
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
### 기능 플래그 확인 가로채기

경우에 따라, 저장소에서 값을 조회하기 전에 메모리 내에서 몇 가지 추가 확인을 하고 싶을 수 있습니다. 예를 들어, 새로운 API를 기능 플래그로 감싸 개발 중이고, 저장된 기능 값들을 삭제하지 않고도 전체 사용자를 대상으로 API를 비활성화하고 싶을 때가 있습니다. 만약 API에 버그가 발견되면, 내부 팀원을 제외한 모든 사용자를 대상으로 해당 API를 쉽게 비활성화하고 버그를 고친 뒤, 기존에 접근이 허용되었던 사용자에게만 다시 활성화할 수 있습니다.

이런 경우에는 [클래스 기반 기능 플래그](#class-based-features)의 `before` 메서드를 활용할 수 있습니다. 해당 메서드가 존재한다면, 항상 저장된 값을 가져오기 전에 메모리 내에서 실행됩니다. 이 메서드에서 `null` 이외의 값을 반환하면, 해당 요청 동안 저장된 값 대신 반환됩니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 실행되는 메모리 내 확인.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * 기능의 초기값을 결정합니다.
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

또한 이 패턴을 활용해, 이전까지 기능 플래그로 제한했던 기능을 전체적으로 배포하는 일정도 예약할 수 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * 저장된 값 조회 전에 항상 실행되는 메모리 내 확인.
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
### 인메모리 캐시

기능 플래그를 확인할 때, Pennant는 결과값을 인메모리로 캐싱합니다. `database` 드라이버를 사용하는 경우, 동일한 요청 내에서 같은 기능 플래그를 다시 확인해도 추가적인 데이터베이스 쿼리가 발생하지 않습니다. 이렇게 하면 요청이 완료되기까지 기능의 결과가 일관되게 유지됩니다.

인메모리 캐시를 수동으로 비울 필요가 있다면, `Feature` 파사드의 `flushCache` 메서드를 사용할 수 있습니다:

```php
Feature::flushCache();
```

<a name="scope"></a>
## 스코프

<a name="specifying-the-scope"></a>
### 스코프 지정하기

앞서 언급했듯이, 기능은 주로 현재 인증된 사용자를 대상으로 확인합니다. 그러나 반드시 그럴 필요는 없으며, `Feature` 파사드의 `for` 메서드를 사용해 원하는 스코프를 지정할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```

스코프는 사용자에만 한정되지 않습니다. 예를 들어, 새로운 결제 경험(billing experience)을 개별 사용자가 아닌 전체 팀 단위로 점진 배포한다면, 아래와 같이 팀별로 기능 활성화를 정의할 수도 있습니다:

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

이때 클로저에는 `User` 대신 `Team` 모델이 전달되고, 사용자의 팀 단위로 기능을 확인하려면 다음과 같이 `for` 메서드에 팀을 넘기면 됩니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```

<a name="default-scope"></a>
### 기본 스코프

Pennant가 기능을 확인할 때 사용하는 기본 스코프도 커스터마이즈할 수 있습니다. 예를 들어, 모든 기능을 현재 인증된 사용자의 팀 기준으로 확인하고 싶다면, 매번 `Feature::for($user->team)`를 호출하는 대신, 아래처럼 애플리케이션의 서비스 프로바이더에서 팀을 기본 스코프로 지정할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```

이렇게 하면 명시적으로 `for` 메서드를 사용하지 않아도, 기능 확인 시 현재 인증된 사용자의 팀이 자동으로 스코프로 사용됩니다:

```php
Feature::active('billing-v2');

// 위 코드는 아래와 동일하게 동작합니다.

Feature::for($user->team)->active('billing-v2');
```

<a name="nullable-scope"></a>
### Nullable 스코프

기능 확인 시 전달된 스코프가 `null`이고 기능 정의에서 `null`을 허용하지 않으면(즉, nullable 타입 또는 union 타입에 `null`이 포함되어 있지 않으면), Pennant는 자동으로 `false`를 반환합니다.

따라서 Artisan 명령어, 큐 작업, 인증이 필요 없는 라우트 등에서 기능을 확인할 때 스코프가 `null`될 수 있음을 고려해 기능 정의에서 이를 처리해야 합니다. 스코프 타입을 "nullable"로 지정하고, `null`인 경우도 로직에서 처리해주는 식입니다:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User|null $user) => match (true) {
    $user === null => true,
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```

<a name="identifying-scope"></a>
### 스코프 식별

Pennant의 내장 `array` 및 `database` 저장소 드라이버는 PHP의 모든 데이터 타입과 Eloquent 모델의 스코프 식별자를 제대로 저장할 수 있습니다. 그러나 서드파티 Pennant 드라이버를 사용하는 경우, 해당 드라이버가 Eloquent 모델이나 애플리케이션의 커스텀 타입 식별자를 제대로 저장하지 못할 수 있습니다.

Pennant에서는 애플리케이션에서 스코프 역할을 하는 객체에 `FeatureScopeable` 계약(interface)을 구현하여, 저장소에 맞는 스코프 식별자 형식을 반환하게 할 수 있습니다.

예를 들어, 한 애플리케이션에서 내장 `database` 드라이버와 "Flag Rocket"이라는 서드파티 드라이버를 동시에 사용하는데, "Flag Rocket" 드라이버는 Eloquent 모델을 인식하지 못하고 대신 `FlagRocketUser` 인스턴스를 필요로 한다고 가정해봅시다. 이럴 때 `FeatureScopeable` 계약의 `toFeatureIdentifier`를 구현하여 각 드라이버별로 적합한 값을 반환할 수 있습니다:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * 지정한 드라이버에 맞게 객체를 기능 스코프 식별자로 변환.
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
### 스코프 직렬화

Pennant는 기본적으로 Eloquent 모델과 연결된 기능을 저장할 때, 완전한 클래스명을 사용합니다. 이미 [Eloquent morph map](/docs/master/eloquent-relationships#custom-polymorphic-types)을 사용하는 경우, Pennant도 morph map을 사용하도록 하여 저장되는 기능 정보와 애플리케이션 구조를 분리할 수 있습니다.

이를 위해 서비스 프로바이더에서 morph map을 정의한 후, `Feature` 파사드의 `useMorphMap` 메서드를 호출하면 됩니다:

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
## 리치 값 기능 플래그

지금까지는 기능 플래그가 "활성" 또는 "비활성"의 이진 상태만 가지는 것으로 보았습니다. 하지만 Pennant는 더 풍부한 값도 저장할 수 있습니다.

예를 들어, "즉시 구매" 버튼의 색상을 세 가지 중에서 실험하고 싶을 때, 기능 정의에서 `true` 또는 `false` 대신 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

`purchase-button` 기능의 값을 조회하려면 `value` 메서드를 사용합니다:

```php
$color = Feature::value('purchase-button');
```

Pennant의 Blade 지시어를 이용하면, 현재 기능의 값에 따라 조건부로 콘텐츠를 편하게 렌더링할 수 있습니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire'가 활성 -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green'이 활성 -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange'가 활성 -->
@endfeature
```

> [!NOTE]
> 리치 값을 사용할 때는, 기능 값이 `false`가 아니기만 하면 "활성"으로 간주된다는 점을 참고하세요.

[조건부 `when`](#conditional-execution) 메서드를 호출할 때는, 기능의 리치 값이 첫 번째 클로저로 전달됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```

마찬가지로, 조건부 `unless` 메서드를 사용할 때는 기능의 리치 값이 두 번째(옵션) 클로저로 전달됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```

<a name="retrieving-multiple-features"></a>
## 여러 기능 플래그 값 조회

`values` 메서드는 주어진 스코프에 대해 복수의 기능 값을 한 번에 조회합니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```

또는 `all` 메서드를 사용하여 현재 정의된 모든 기능 값을 조회할 수 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```

단, 클래스 기반 기능은 동적으로 등록되므로, 현재 요청에서 한 번이라도 조회된 경우에만 `all`의 결과에 나타납니다.

항상 기능 클래스가 `all` 결과에 포함되길 원한다면, Pennant의 기능 디스커버리 기능을 사용할 수 있습니다. 사용법은 다음과 같습니다. 서비스 프로바이더에서 `discover` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```

`discover` 메서드는 애플리케이션의 `app/Features` 디렉토리에 위치한 모든 기능 클래스를 등록합니다. 이제 `all` 메서드를 호출하면 현재 요청에서 아직 확인되지 않은 클래스 기반 기능도 결과에 포함됩니다:

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
## Eager 로딩

Pennant는 단일 요청 내에서 해석된 기능 플래그 값을 인메모리 캐시에 저장하지만, 많은 양의 기능 플래그를 반복적으로 확인하는 경우 성능 이슈가 발생할 수 있습니다. 이를 완화하기 위해 Pennant는 기능 값의 eager 로딩을 지원합니다.

예를 들어, 루프 내에서 사용자마다 기능 플래그를 확인하는 경우를 생각해봅시다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

`database` 드라이버를 사용하는 경우, 위 코드는 사용자마다 데이터베이스 쿼리를 실행하게 됩니다. Pennant의 `load` 메서드를 사용하면, 사용자 컬렉션 또는 스코프 컬렉션에 대해 기능 값을 미리 로딩할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```

이미 로드되지 않은 기능 값만 미리 로딩하려면 `loadMissing` 메서드를 사용할 수 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```

정의된 모든 기능을 한 번에 로딩하려면 `loadAll` 메서드를 사용할 수 있습니다:

```php
Feature::for($users)->loadAll();
```

<a name="updating-values"></a>
## 값 업데이트

기능의 값이 처음 해석(resolved)되면, 해당 값은 저장소에 기록됩니다. 이는 여러 요청에 걸쳐 사용자 경험을 일관성 있게 유지하기 위해 필요합니다. 그러나, 저장된 기능 값을 수동으로 업데이트하고 싶을 때도 있습니다.

`activate`, `deactivate` 메서드를 이용해 기능을 "on" 또는 "off"로 수동 토글할 수 있습니다:

```php
use Laravel\Pennant\Feature;

// 기본 스코프에 대해 기능 활성화...
Feature::activate('new-api');

// 특정 스코프(예시: 팀)에 대해 기능 비활성화...
Feature::for($user->team)->deactivate('billing-v2');
```

리치 값을 저장할 때는 `activate` 메서드의 두 번째 인수에 값을 전달할 수 있습니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```

저장된 기능 값을 삭제하고 다시 해석하도록 하려면, `forget` 메서드를 사용합니다. 기능이 다시 확인될 때, Pennant는 기능 정의로부터 값을 다시 해석합니다:

```php
Feature::forget('purchase-button');
```

<a name="bulk-updates"></a>
### 일괄 업데이트

`activateForEveryone`, `deactivateForEveryone` 메서드를 통해 전체 사용자를 대상으로 저장된 기능 값을 일괄 업데이트할 수 있습니다.

예를 들어, `new-api` 기능이 충분히 안정적이며, 결제 버튼의 최적의 색상을 확정했다고 가정합시다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```

또는 기능을 전체 사용자를 대상으로 비활성화할 수도 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```

> [!NOTE]
> 이 메서드는 Pennant의 저장소 드라이버에 저장된 값만 일괄 변경합니다. 또한, 애플리케이션 내에서 기능 정의 자체도 함께 업데이트해야 합니다.

<a name="purging-features"></a>
### 기능 플래그 일괄 정리

애플리케이션에서 기능 플래그를 제거했거나, 전체 사용자에게 새로운 정의를 재적용해야할 경우 저장소에서 해당 기능 플래그 정보를 완전히 삭제하는 것이 유용할 수 있습니다.

`purge` 메서드를 사용해 특정 기능의 저장된 값을 모두 삭제할 수 있습니다:

```php
// 단일 기능 삭제
Feature::purge('new-api');

// 여러 기능 삭제
Feature::purge(['new-api', 'purchase-button']);
```

모든 기능을 삭제하려면 인수 없이 `purge`를 호출합니다:

```php
Feature::purge();
```

배포 파이프라인에서 기능 정리가 필요한 경우를 대비해, Pennant는 `pennant:purge` Artisan 명령어를 제공합니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```

특정 기능을 제외하고 모두 삭제해야 한다면, `--except` 옵션을 사용할 수 있습니다:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```

편의를 위해 `pennant:purge` 명령어는 `--except-registered` 플래그를 지원합니다. 해당 플래그를 사용하면 서비스 프로바이더에 등록된 기능을 제외하고 모두 삭제할 수 있습니다:

```shell
php artisan pennant:purge --except-registered
```

<a name="testing"></a>
## 테스트

기능 플래그가 관여하는 코드를 테스트할 때, 테스트 내에서 기능 값을 임의로 재정의하는 것이 가장 쉬운 방법입니다. 예를 들어, 서비스 프로바이더에 아래와 같이 기능이 정의되어 있다고 가정합시다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```

테스트에서는 기능의 반환 값이 항상 같도록, 테스트 시작 시 기능을 다시 정의해줄 수 있습니다. 아래 테스트는 서비스 프로바이더에 `Arr::random()`이 그대로 남아있어도 항상 통과합니다:

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

클래스 기반 기능에도 동일한 접근법을 적용할 수 있습니다:

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

기능이 `Lottery` 인스턴스를 반환하는 경우, 몇 가지 유용한 [테스트 헬퍼](/docs/master/helpers#testing-lotteries)도 사용할 수 있습니다.

<a name="store-configuration"></a>
#### 저장소 설정

테스트 중 Pennant가 사용할 저장소를 지정하려면, 애플리케이션의 `phpunit.xml` 파일에 `PENNANT_STORE` 환경 변수를 추가하면 됩니다:

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
## 커스텀 Pennant 드라이버 추가

<a name="implementing-the-driver"></a>
#### 드라이버 구현

내장 저장소 드라이버가 애플리케이션에 맞지 않는 경우, 직접 저장소 드라이버를 작성할 수 있습니다. 커스텀 드라이버는 반드시 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

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

이제 Redis 연결을 활용해 위 각 메서드의 구현을 작성하면 됩니다. 구체적인 구현 예시는 [Pennant 소스 코드의 `DatabaseDriver`](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)를 참고하세요.

> [!NOTE]
> Laravel은 확장 기능을 위한 디렉토리를 기본 제공하지 않습니다. 원하는 위치 어디든 생성해서 사용하면 됩니다. 이 예제에서는 `Extensions` 디렉토리를 생성해 `RedisFeatureDriver`를 배치했습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록

드라이버 구현이 완료되면, Laravel에 등록할 차례입니다. Pennant에 추가 드라이버를 등록하려면, `Feature` 파사드의 `extend` 메서드를 사용하세요. 이 메서드는 서비스 프로바이더의 `boot` 메서드 내에서 호출하는 것이 좋습니다:

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
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```

드라이버를 등록한 후에는, 애플리케이션의 `config/pennant.php` 설정 파일에서 `redis` 드라이버를 사용할 수 있습니다:

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
### 외부에서 기능 플래그 정의

드라이버가 서드파티 기능 플래그 플랫폼을 래핑하는 경우, Pennant의 `Feature::define` 메서드가 아니라 플랫폼에서 직접 기능을 정의하게 될 것입니다. 이때 커스텀 드라이버는 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스도 반드시 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * 주어진 스코프에 대해 정의된 기능 목록 반환.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```

`definedFeaturesForScope` 메서드는 해당 스코프에 정의된 기능 플래그 이름 목록을 반환하면 됩니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 전반에서 기능 플래그와 관련해 추적 가능한 여러 이벤트를 발생시킵니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

이벤트는 [기능이 확인](#checking-features)될 때마다 발생합니다. 기능 플래그 사용 지표 추적 등에 활용할 수 있습니다.

### `Laravel\Pennant\Events\FeatureResolved`

특정 스코프에 대해 기능 플래그가 처음 해석(resolved)될 때 발생합니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

애플리케이션 내에 남아 있는 참조로 인해, 의도치 않게 삭제된 기능 플래그가 처음으로 해석될 때 발생합니다. 이 이벤트를 활용하여 해당 상황을 감지할 수 있습니다:

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
     * 애플리케이션 서비스 부트스트랩.
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

[클래스 기반 기능 플래그](#class-based-features)가 요청에서 처음으로 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

[null을 지원하지 않는](#nullable-scope) 기능 정의에 `null` 스코프가 전달될 때 발생합니다.

이 경우 Pennant는 기본적으로 문제 없이 값을 `false`로 반환합니다. 만약 이 기본 동작 대신 별도의 처리가 필요하다면, `AppServiceProvider`의 `boot` 메서드에서 해당 이벤트 리스너를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

스코프에 대해 기능을 업데이트할 때(주로 `activate` 또는 `deactivate` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

모든 스코프에 대해 기능을 업데이트할 때(`activateForEveryone` 또는 `deactivateForEveryone` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeatureDeleted`

스코프에 대해 기능을 삭제할 때(`forget` 호출 시) 발생합니다.

### `Laravel\Pennant\Events\FeaturesPurged`

특정 기능들을 정리할 때 발생합니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

모든 기능을 정리할 때 발생합니다.
