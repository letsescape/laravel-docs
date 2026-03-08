# 인가 (Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성하기](#writing-gates)
    - [게이트를 통한 작업 인가](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 체크 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책(Policies) 생성하기](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성하기](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델이 없는 메서드](#methods-without-models)
    - [게스트 사용자 처리](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 사용한 작업 인가](#authorizing-actions-using-policies)
    - [User 모델을 통한 인가](#via-the-user-model)
    - [Gate Facade를 통한 인가](#via-the-gate-facade)
    - [미들웨어를 통한 인가](#via-middleware)
    - [Blade 템플릿을 통한 인가](#via-blade-templates)
    - [추가 컨텍스트 공급](#supplying-additional-context)
- [인가와 Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개

Laravel은 내장된 [인증(authentication)](/docs/12.x/authentication) 서비스뿐만 아니라, 주어진 리소스에 대해 사용자의 작업 권한을 간단히 확인할 수 있는 인가(authorization) 기능도 제공합니다. 예를 들어, 사용자가 인증되었더라도 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 수정하거나 삭제할 권한이 없을 수 있습니다. Laravel의 인가 기능은 이러한 종류의 권한 검사를 쉽고 체계적으로 관리할 수 있는 방법을 제공합니다.

Laravel은 작업 인가를 위한 두 가지 주요 방식을 지원합니다: [게이트(gates)](#gates)와 [정책(policies)](#creating-policies). 게이트와 정책은 각각 라우트(routes)와 컨트롤러(controllers)와 비슷한 개념으로 생각할 수 있습니다. 게이트는 클로저 기반의 간단한 인가 방식을 제공하는 반면 정책은 컨트롤러처럼 특정 모델이나 리소스에 대한 인가 로직을 그룹화합니다. 이 문서에서는 먼저 게이트를 살펴보고 그다음 정책을 다룹니다.

애플리케이션을 만들 때 게이트만 사용하거나 정책만 사용하는 식으로 엄격히 선택할 필요는 없습니다. 대부분 애플리케이션은 게이트와 정책을 적절히 혼합해서 사용할 것이며, 이는 전혀 문제 없습니다! 게이트는 관리 페이지 조회 등 모델 또는 리소스와 직접 관련이 없는 작업에 적합합니다. 정책은 특정 모델이나 리소스에 대한 작업 인가가 필요할 때 사용하는 것이 좋습니다.

<a name="gates"></a>
## 게이트(Gates)

<a name="writing-gates"></a>
### 게이트 작성하기

> [!WARNING]
> 게이트는 Laravel 인가 기능의 기본을 배우기에 좋지만, 튼튼한 Laravel 애플리케이션을 만들 때는 인가 규칙을 체계적으로 관리하기 위해 [정책](#creating-policies) 사용을 권장합니다.

게이트는 단순히 사용자가 특정 작업을 수행할 수 있는지 여부를 판단하는 클로저입니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` facade를 사용해 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요에 따라 관련 Eloquent 모델 같은 추가 인수를 받을 수도 있습니다.

다음 예시는 사용자에게 주어진 `App\Models\Post` 모델을 수정할 권한이 있는지 확인하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`가 포스트의 `user_id`와 일치하는지 확인합니다.

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```

컨트롤러 방식처럼, 게이트는 클래스 콜백 배열로도 정의할 수 있습니다:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```

<a name="authorizing-actions-via-gates"></a>
### 작업 인가하기

게이트로 작업을 인가하려면 `Gate` facade에서 제공하는 `allows` 또는 `denies` 메서드를 사용합니다. 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 게이트 클로저에 자동으로 사용자를 전달합니다. 보통 컨트롤러 내에서 인가가 필요한 작업 전에 이 메서드들을 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * 주어진 포스트를 수정합니다.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // 포스트 수정 작업...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자가 아닌 다른 사용자의 인가 여부를 확인하려면 `Gate` facade의 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // 사용자가 포스트를 수정할 수 있습니다...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // 사용자가 포스트를 수정할 수 없습니다...
}
```

한 번에 여러 작업에 대해 인가 여부를 확인하려면 `any` 또는 `none` 메서드를 사용할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // 사용자가 포스트를 수정하거나 삭제할 수 있습니다...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // 사용자가 포스트를 수정하거나 삭제할 수 없습니다...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 인가 시도 및 예외 발생

작업 인가를 시도하고 사용자가 권한이 없으면 `Illuminate\Auth\Access\AuthorizationException` 예외를 자동으로 발생시키려면 `Gate` facade의 `authorize` 메서드를 사용하세요. 이 예외는 Laravel에서 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// 작업 인가 완료...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 전달하기

게이트의 인가 메서드들 (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)과 인가용 [Blade 디렉티브](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열에 담긴 인수들은 게이트 클로저의 추가 파라미터로 전달되어 인가 결정 시 참고할 수 있습니다:

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, bool $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // 사용자가 포스트를 생성할 수 있습니다...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 간단한 불리언값을 반환하는 게이트만 살펴봤습니다. 그러나 때때로 에러 메시지 같은 자세한 응답을 반환하고 싶을 때가 있습니다. 이럴 경우 `Illuminate\Auth\Access\Response` 객체를 반환할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('관리자여야 합니다.');
});
```

인가 응답을 반환하더라도 `Gate::allows` 메서드는 단순 불리언 값만 반환합니다. 전체 응답 객체가 필요하면 `Gate::inspect` 메서드를 사용하세요:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // 작업 인가 완료...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용할 때 인가되지 않으면 `AuthorizationException`을 던지는데, 이때 응답 메시지는 HTTP 응답으로 전파됩니다:

```php
Gate::authorize('edit-settings');

// 작업 인가 완료...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 커스터마이징

게이트에서 작업이 거부되면 기본적으로 403 HTTP 응답이 반환됩니다. 하지만 다른 상태 코드를 반환하고 싶을 때가 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 메서드를 사용해 실패시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```

웹 애플리케이션에서 리소스를 숨기기 위해 404 응답을 반환하는 경우가 많으므로, 편의용으로 `denyAsNotFound` 메서드도 제공합니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyAsNotFound();
});
```

<a name="intercepting-gate-checks"></a>
### 게이트 체크 가로채기

특정 사용자에게 모든 권한을 부여하고 싶을 때가 있습니다. `before` 메서드로 모든 인가 검사 전에 실행할 클로저를 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 널이 아닌 값을 반환하면 이 값이 인가 검사 결과가 됩니다.

`after` 메서드로는 모든 권한 검사 후 실행할 클로저를 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after`에서 반환된 값은, 게이트나 정책이 `null`을 반환하지 않는 한 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 인가

가끔 특정 작업에 대응하는 전용 게이트를 정의하지 않고 현재 인증된 사용자가 작업 권한이 있는지 바로 확인하고 싶을 때가 있습니다. Laravel은 `Gate::allowIf`와 `Gate::denyIf` 메서드로 이런 인라인 인가를 수행할 수 있습니다. 인라인 인가는 정의된 ["before" 또는 "after" 인가 훅](#intercepting-gate-checks)을 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

인가되지 않았거나 인증된 사용자가 없으면 Laravel이 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel이 403 HTTP 응답으로 자동 변환합니다.

<a name="creating-policies"></a>
## 정책 생성하기 (Creating Policies)

<a name="generating-policies"></a>
### 정책 생성

정책은 특정 모델이나 리소스에 대한 인가 로직을 조직하는 클래스입니다. 예를 들어 블로그를 만들 경우 `App\Models\Post` 모델과, 포스트 생성이나 수정 권한을 판단하는 `App\Policies\PostPolicy` 클래스가 있을 수 있습니다.

`make:policy` Artisan 명령어로 정책 클래스를 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉토리에 위치합니다. 이 디렉토리가 없으면 Laravel이 자동으로 생성합니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령은 빈 정책 클래스를 만듭니다. 만약 조회, 생성, 수정, 삭제 등의 예제 정책 메서드를 미리 포함하려면 `--model` 옵션과 함께 사용하세요:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 발견

기본적으로 Laravel은 모델과 정책 이름이 표준 규칙을 따르기만 하면 자동으로 정책을 찾아줍니다. 예를 들어, 모델은 `app/Models`에, 정책은 `app/Policies` 디렉토리에 위치한 경우, Laravel은 `app/Models/Policies`와 `app/Policies`에서 정책을 탐색합니다. 또한 정책 이름은 모델명과 같고 `Policy` 접미어가 붙어 있어야 합니다. 예를 들어 `User` 모델은 `UserPolicy` 정책과 연결됩니다.

직접 정책 탐색 방식을 정의하고 싶으면 `Gate::guessPolicyNamesUsing` 메서드로 커스텀 콜백을 등록할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider` 클래스 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // 주어진 모델에 해당하는 정책 클래스명을 반환하세요...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` facade를 사용해 직접 모델과 정책을 연결할 수도 있습니다. 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 등록합니다:

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::policy(Order::class, OrderPolicy::class);
}
```

대신 모델 클래스에 `UsePolicy` 속성(attribute)을 붙여 정책을 연결할 수도 있습니다:

```php
<?php

namespace App\Models;

use App\Policies\OrderPolicy;
use Illuminate\Database\Eloquent\Attributes\UsePolicy;
use Illuminate\Database\Eloquent\Model;

#[UsePolicy(OrderPolicy::class)]
class Order extends Model
{
    //
}
```

<a name="writing-policies"></a>
## 정책 작성하기 (Writing Policies)

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되면, 인가할 각 작업에 대응하는 메서드를 추가하세요. 예를 들어, `PostPolicy`에 `update` 메서드를 정의해, 특정 `App\Models\User`가 주어진 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단합니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인수로 받아, 인가 여부를 불리언값으로 반환해야 합니다. 예제로 사용자의 `id`가 포스트의 소유자 `user_id`와 같은지 확인합니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

필요에 따라 정책에 다른 메서드도 정의할 수 있습니다. 예를 들어 `view`나 `delete` 메서드를 정의할 수 있지만, 정책 메서드는 자유롭게 원하는 이름을 붙여도 됩니다.

`--model` 옵션을 사용해 정책을 생성했다면, 이미 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 같은 메서드가 포함되어 있습니다.

> [!NOTE]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로, 정책 클래스 생성자에 필요한 의존성을 타입힌트하면 자동 의존성 주입을 받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 간단한 불리언값을 반환하는 정책 메서드를 다뤘지만, 때로는 에러 메시지도 같이 포함하는 상세한 응답을 넣고 싶을 수 있습니다. 이럴 때는 정책 메서드에서 `Illuminate\Auth\Access\Response` 객체를 반환할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('이 포스트의 소유자가 아닙니다.');
}
```

정책에서 인가 응답을 반환할 때도, `Gate::allows` 메서드는 여전히 불리언 값만 반환합니다. 전체 응답이 필요하면 `Gate::inspect` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // 작업 인가 완료...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드로 인가 시도 시 인가 실패하면 예외를 던지며, 이때 응답 메시지는 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('update', $post);

// 작업 인가 완료...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 커스터마이징

정책 메서드에서 작업 거부 시 기본으로 403 HTTP 응답을 반환하지만, 다른 상태코드도 반환하고 싶을 수 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 메서드로 실패 시 반환할 상태코드를 지정할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

웹 애플리케이션에서 자원을 숨기기 위해 404 응답을 자주 사용하는 만큼, 편의용으로 `denyAsNotFound` 메서드도 제공합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```

<a name="methods-without-models"></a>
### 모델이 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 이런 경우가 가장 흔한 예가 `create` 작업 인가입니다. 예를 들어 블로그를 만든다면, 어떤 사용자가 포스트를 생성할 수 있는지 판단하는 경우 정책 메서드는 사용자 인스턴스만 인수로 받도록 합니다:

```php
/**
 * 사용자가 포스트를 생성할 수 있는지 판단합니다.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자 (Guest Users)

기본적으로, 게이트와 정책은 인증되지 않은 사용자가 요청을 보냈을 경우 자동으로 `false`를 반환합니다. 그러나 “optional” 타입힌트를 추가하거나 사용자 인자에 `null` 기본값을 주어 인증되지 않은 사용자도 허용할 수 있습니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게 주어진 정책 내 모든 작업을 허용하고 싶을 때, 정책 클래스에 `before` 메서드를 정의하세요. 이 메서드는 정책의 다른 모든 메서드 전에 실행되며, 인가를 미리 처리할 수 있습니다. 주로 관리자 권한이 있는 사용자가 모든 작업을 수행하도록 할 때 사용합니다:

```php
use App\Models\User;

/**
 * 사전 인가 검사를 수행합니다.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 유형의 사용자에게 모든 작업을 거부하려면 `before` 메서드에서 `false`를 반환하면 됩니다. `null`을 반환하면 정책의 개별 메서드로 인가 검사가 넘어갑니다.

> [!WARNING]
> 정책 클래스에 `before` 메서드가 있더라도 인가할 작업명이 정책 클래스 내 메서드 이름과 일치하지 않으면 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 작업 인가

<a name="via-the-user-model"></a>
### User 모델을 통한 인가

Laravel에서 기본 제공하는 `App\Models\User` 모델은 작업 인가를 위한 `can`과 `cannot` 메서드를 제공합니다. 이들 메서드는 인가하려는 작업명과 관련 모델을 인수로 받습니다. 예를 들어 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 판단할 수 있습니다. 보통 이것은 컨트롤러 메서드 내에서 사용합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 주어진 포스트를 수정합니다.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // 포스트 수정 작업...

        return redirect('/posts');
    }
}
```

주어진 모델에 대해 [정책이 등록](#registering-policies)되어 있으면 `can` 메서드는 자동으로 적합한 정책을 호출해 불리언 결과를 반환합니다. 정책이 없으면 게이트에서 해당 작업과 일치하는 클로저 기반 함수를 호출합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

`create` 같은 정책 메서드는 모델 인스턴스가 필요 없을 수 있습니다. 이런 경우 `can` 메서드에 클래스명을 넘기면 해당 클래스에 매핑된 정책을 찾아서 인가를 수행합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * 포스트 생성.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // 포스트 생성 작업...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Gate Facade를 통한 인가

`App\Models\User` 모델에 제공된 메서드 외에도, `Gate` facade의 `authorize` 메서드를 통해 작업 인가를 수행할 수 있습니다.

이 메서드는 인가하려는 작업명과 관련 모델을 받으며, 인가 실패 시 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. 이 예외는 Laravel이 자동으로 403 HTTP 응답으로 변환합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * 블로그 포스트 수정.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // 현재 사용자가 블로그 포스트 수정 가능...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞서 설명한 대로 `create` 같은 작업엔 모델 인스턴스가 필요 없습니다. 이런 경우에는 클래스명을 `authorize` 메서드에 넘겨서 인가할 정책을 결정합니다:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * 새 블로그 포스트 생성.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // 현재 사용자가 블로그 포스트 생성 가능...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통한 인가

Laravel은 요청이 라우트나 컨트롤러에 도달하기 전에 작업 인가를 수행하는 미들웨어를 제공합니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 등록됩니다. 다음은 `can` 미들웨어로 사용자가 포스트를 수정할 수 있는지 인가하는 예시입니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 포스트 수정 가능...
})->middleware('can:update,post');
```

이 예시에서 `can` 미들웨어에 두 인수를 전달했습니다. 첫 번째는 인가할 작업명이며, 두 번째는 정책 메서드에 전달할 라우트 파라미터명입니다. 이 경우, [암묵적 모델 바인딩](/docs/12.x/routing#implicit-binding) 덕분에 `App\Models\Post` 모델 인스턴스가 정책 메서드에 주입됩니다. 만약 사용자가 작업 권한이 없으면 미들웨어는 403 HTTP 응답을 반환합니다.

편의를 위해, 라우트에 `can` 메서드를 사용해 미들웨어를 붙일 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // 현재 사용자가 포스트 수정 가능...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

`create` 같은 정책 메서드는 모델 인스턴스 없이 동작할 수 있습니다. 이런 경우, 미들웨어에 클래스명을 넘겨서 인가할 정책을 결정합니다:

```php
Route::post('/post', function () {
    // 현재 사용자가 포스트 생성 가능...
})->middleware('can:create,App\Models\Post');
```

문자열 형태 미들웨어 등록에서 전체 클래스명을 쓰는 것이 번거로울 수 있으므로, `can` 메서드를 사용해 라우트에 미들웨어를 붙이는 방식을 권장합니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // 현재 사용자가 포스트 생성 가능...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿에서 인가

Blade 템플릿을 작성할 때, 사용자가 특정 작업을 수행할 수 있을 때만 일부 페이지를 표시하고 싶을 수 있습니다. 예를 들어, 호텔 블로그 포스트 수정폼을 사용자가 수정 권한이 있을 때만 보여줄 수 있습니다. 이럴 때는 `@can`과 `@cannot` 디렉티브를 사용합니다:

```blade
@can('update', $post)
    <!-- 현재 사용자가 포스트를 수정할 수 있습니다... -->
@elsecan('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 포스트를 생성할 수 있습니다... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- 현재 사용자가 포스트를 수정할 수 없습니다... -->
@elsecannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 새 포스트를 생성할 수 없습니다... -->
@endcannot
```

이 디렉티브들은 `@if`, `@unless` 구문의 편리한 단축키입니다. 위 예제는 다음과 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 포스트를 수정할 수 있습니다... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- 현재 사용자가 포스트를 수정할 수 없습니다... -->
@endunless
```

특정 작업 배열 중 하나라도 인가되는지 확인하려면 `@canany` 디렉티브를 사용하세요:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- 현재 사용자가 포스트를 수정, 조회, 삭제할 수 있습니다... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 생성할 수 있습니다... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

다른 인가 방식과 마찬가지로, 작업에 모델 인스턴스가 필요 없으면 클래스명을 `@can`과 `@cannot`에 넘길 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 생성할 수 있습니다... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- 현재 사용자가 포스트를 생성할 수 없습니다... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 공급

정책을 통한 작업 인가 시, 여러 인가 함수와 헬퍼의 두 번째 인수로 배열을 넘길 수 있습니다. 배열의 첫 요소는 인가할 정책을 결정하는 데 쓰이고, 나머지 요소들은 정책 메서드에 추가 파라미터로 전달되어 인가 판단에 참고할 수 있습니다. 예를 들어, 다음은 부가적인 `$category` 파라미터를 가진 `PostPolicy`의 `update` 메서드 예시입니다:

```php
/**
 * 사용자가 주어진 포스트를 수정할 수 있는지 판단합니다.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

인증된 사용자가 포스트 수정 권한이 있는지 판단할 때, 이렇게 호출합니다:

```php
/**
 * 블로그 포스트 수정.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // 현재 사용자가 블로그 포스트 수정 가능...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 인가와 Inertia

인가 처리는 항상 서버에서 수행되어야 하지만, 프론트엔드 애플리케이션에 인가 정보를 제공해 UI를 적절히 렌더링하는 것이 편리할 때도 많습니다. Laravel은 Inertia 기반 프론트엔드에 인가 정보를 노출하는 강제 규칙을 정의하지 않습니다.

그러나 Laravel의 Inertia 기반 [스타터킷](/docs/12.x/starter-kits) 중 하나를 사용한다면 `HandleInertiaRequests` 미들웨어가 이미 포함되어 있습니다. 이 미들웨어의 `share` 메서드에서 모든 Inertia 페이지에 공통으로 전달할 공유 데이터를 반환할 수 있습니다. 이 위치에서 사용자의 인가 정보도 정의할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    // ...

    /**
     * 기본으로 공유할 프로퍼티를 정의합니다.
     *
     * @return array<string, mixed>
     */
    public function share(Request $request)
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user(),
                'permissions' => [
                    'post' => [
                        'create' => $request->user()->can('create', Post::class),
                    ],
                ],
            ],
        ];
    }
}
```