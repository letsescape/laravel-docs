# 인가 (Authorization)

- [소개](#introduction)
- [게이트(Gates)](#gates)
    - [게이트 작성](#writing-gates)
    - [액션 인가](#authorizing-actions-via-gates)
    - [게이트 응답](#gate-responses)
    - [게이트 체크 가로채기](#intercepting-gate-checks)
    - [인라인 인가](#inline-authorization)
- [정책(Policies) 생성](#creating-policies)
    - [정책 생성](#generating-policies)
    - [정책 등록](#registering-policies)
- [정책 작성](#writing-policies)
    - [정책 메서드](#policy-methods)
    - [정책 응답](#policy-responses)
    - [모델 없는 메서드](#methods-without-models)
    - [게스트 사용자](#guest-users)
    - [정책 필터](#policy-filters)
- [정책을 이용한 액션 인가](#authorizing-actions-using-policies)
    - [User 모델을 통한 인가](#via-the-user-model)
    - [Gate 파사드를 통해](#via-the-gate-facade)
    - [미들웨어를 통해](#via-middleware)
    - [Blade 템플릿을 통해](#via-blade-templates)
    - [추가 컨텍스트 제공](#supplying-additional-context)
- [인가 & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [인증](/docs/master/authentication) 기능 외에도 사용자가 특정 리소스에 대하여 특정 작업을 수행할 수 있는지 인가(authorization)하는 간단한 방법을 제공합니다. 예를 들어, 사용자가 인증되어 있더라도, 해당 사용자가 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 업데이트하거나 삭제할 권한이 없을 수 있습니다. Laravel의 인가 기능은 이러한 인가 체크를 쉽게 관리하고 구조적으로 조직할 수 있게 도와줍니다.

Laravel은 주요 인가 방식으로 [게이트](#gates)와 [정책](#creating-policies) 두 가지를 제공합니다. 게이트와 정책은 각각 라우트와 컨트롤러와 유사하게 생각할 수 있습니다. 게이트는 클로저 기반의 단순한 인가 방법을 제공하고, 정책은 컨트롤러처럼 특정 모델이나 리소스 중심으로 인가 로직을 그룹화합니다. 이 문서에서는 우선 게이트에 대해 살펴보고, 이후 정책에 대해 설명합니다.

애플리케이션을 개발할 때 게이트만 사용하거나 정책만 써야 할 필요는 없습니다. 대부분의 애플리케이션에서는 게이트와 정책을 혼합해서 사용하게 되며, 이는 매우 자연스러운 일입니다! 게이트는 관리자 대시보드 조회와 같이 모델 혹은 리소스와 직접적으로 연관되지 않은 액션에 더 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대한 액션을 인가할 때 사용하는 것이 좋습니다.

<a name="gates"></a>
## 게이트 (Gates)

<a name="writing-gates"></a>
### 게이트 작성

> [!WARNING]
> 게이트는 Laravel의 인가 기능의 기초를 익히기에 매우 좋은 방법입니다. 하지만 실제로 강력한 Laravel 애플리케이션을 만들 때는 인가 규칙을 체계적으로 구성할 수 있도록 [정책(Policies)](#creating-policies) 사용을 고려하시기 바랍니다.

게이트는 사용자가 특정 액션을 수행할 수 있는지 여부를 판단하는 클로저(Closure)일 뿐입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 파사드를 사용해 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요에 따라 추가 인수(예: 관련 Eloquent 모델)도 받을 수 있습니다.

아래 예제에서는 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 확인하는 게이트를 정의합니다. 게이트는 사용자의 `id` 값과 게시물을 생성한 사용자의 `user_id` 값을 비교하여 인가 여부를 결정합니다:

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

컨트롤러와 마찬가지로, 게이트를 클래스 콜백 배열로도 정의할 수 있습니다:

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
### 액션 인가

게이트를 통해 액션을 인가하려면 `Gate` 파사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 게이트 클로저로 자동 전달해줍니다. 일반적으로 애플리케이션의 컨트롤러에서 인가가 필요한 액션 전에 게이트 인가 메서드를 호출합니다:

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
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

현재 인증된 사용자 외의 다른 사용자가 특정 액션에 대해 인가되었는지 확인하고 싶을 때는 `Gate` 파사드의 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

`any` 또는 `none` 메서드를 이용하여 여러 액션을 한 번에 인가할 수도 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 인가 또는 예외 발생

액션을 인가 시도하고, 인가되지 않았을 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키려면 `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException` 인스턴스는 Laravel에서 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

인가 능력(abilities)을 판별하는 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 인가 [Blade 지시문](#via-blade-templates) (`@can`, `@cannot`, `@canany`)에는 두 번째 인수로 배열을 전달할 수 있습니다. 이 배열의 요소들은 게이트 클로저의 파라미터로 전달되어, 인가 결정에 추가적인 컨텍스트로 활용할 수 있습니다:

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
    // The user can create the post...
}
```

<a name="gate-responses"></a>
### 게이트 응답

지금까지는 게이트에서 단순히 참/거짓 값을 반환하는 예제만 살펴보았습니다. 하지만 때로는 보다 자세한 응답, 예를 들어 오류 메시지 등이 필요한 경우도 있을 수 있습니다. 이럴 때는 게이트에서 `Illuminate\Auth\Access\Response`를 반환하면 됩니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('You must be an administrator.');
});
```

게이트에서 인가 응답 객체를 반환하더라도, `Gate::allows` 메서드는 여전히 단순 불리언 값을 반환합니다. 그러나, `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 인가 응답을 확인할 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드를 사용해 인가되지 않은 경우 `AuthorizationException`이 발생할 수 있는데, 이때 응답 메시지는 HTTP 응답에 그대로 전달됩니다:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이즈

게이트에서 액션이 거부된 경우 기본적으로 `403` HTTP 응답이 반환됩니다. 그러나 상황에 따라 다른 HTTP 상태 코드를 반환해야 할 때도 있습니다. 이럴 때는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하여 커스텀 상태 코드를 지정할 수 있습니다:

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

웹 애플리케이션에서 자원을 숨기기 위해 `404` 응답을 사용하는 패턴이 흔하기 때문에, 편의상 `denyAsNotFound` 메서드도 제공합니다:

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

특정 사용자에게 모든 인가를 허용하고 싶을 때가 있습니다. 이럴 때는 `before` 메서드를 이용해, 모든 인가 체크 이전에 실행되는 클로저를 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` 클로저가 `null`이 아닌 값을 반환하면, 이 값이 인가 체크의 결과로 간주됩니다.

또한 `after` 메서드를 사용하여 모든 인가 체크 후에 실행되는 클로저도 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`after` 클로저에서 반환된 값은 게이트 또는 정책의 반환값이 `null`인 경우에만 인가 체크 결과를 덮어씁니다.

<a name="inline-authorization"></a>
### 인라인 인가

때때로, 특정 액션에 맞는 게이트를 따로 만들지 않고, 현재 인증된 사용자가 어떤 액션을 수행할 수 있는지 간단하게 확인하고 싶을 수 있습니다. Laravel은 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 이러한 "인라인" 인가 체크를 지원합니다. 인라인 인가는 별도 ["before" 또는 "after" 인가 훅](#intercepting-gate-checks)을 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

액션에 대한 인가가 거부되거나 현재 인증된 사용자가 없다면, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. 이 예외는 Laravel의 예외 핸들러에 의해 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책(Policies) 생성

<a name="generating-policies"></a>
### 정책 생성

정책 클래스는 특정 모델이나 리소스에 대한 인가 로직을 그룹화합니다. 예를 들어, 블로그 애플리케이션이라면, `App\Models\Post` 모델과 이 모델의 인가를 담당할 `App\Policies\PostPolicy` 정책이 있을 수 있습니다.

정책 생성은 `make:policy` Artisan 명령어를 사용합니다. 생성된 정책은 `app/Policies` 디렉터리에 위치하게 됩니다. 이 디렉터리가 없다면, Laravel이 직접 생성합니다:

```shell
php artisan make:policy PostPolicy
```

`make:policy` 명령어는 기본적으로 비어있는 정책 클래스를 만듭니다. 리소스와 관련된 view, create, update, delete 예제 정책 메서드를 가지고 시작하고 싶다면, `--model` 옵션을 추가로 사용할 수 있습니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 자동 감지(Policy Discovery)

기본적으로, Laravel은 모델과 정책이 표준 네이밍 규칙을 따르면 자동으로 정책을 감지합니다. 구체적으로, 정책은 모델이 위치한 디렉터리와 동일하거나 상위의 `Policies` 디렉터리에 있어야 합니다. 예를 들어, 모델이 `app/Models`에 있고, 정책이 `app/Policies`에 있다면, Laravel은 먼저 `app/Models/Policies`를 확인한 후 `app/Policies`에서 정책을 찾습니다. 또한 정책 클래스명은 모델명과 일치하며 뒤에 `Policy`가 붙어야 합니다. 따라서 `User` 모델은 `UserPolicy` 정책 클래스와 연결됩니다.

정책 감지 로직을 직접 정의하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 통해 커스텀 콜백을 등록할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 파사드를 이용해, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 모델과 정책을 수동으로 등록할 수 있습니다:

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

또는, 모델 클래스에 `UsePolicy` 속성을 부여하여 정책을 지정할 수도 있습니다:

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
## 정책 작성

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되면, 각 인가 액션(즉, 능력)에 대한 메서드를 추가할 수 있습니다. 예를 들어, `PostPolicy`에 주어진 `App\Models\User`가 해당 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 판단하는 `update` 메서드를 정의할 수 있습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받아 해당 사용자가 해당 게시물을 수정할 수 있는지 여부(즉, `true` 또는 `false`)를 반환해야 합니다. 아래 예제는 게시물의 `user_id`와 사용자의 `id`가 일치하는지 확인합니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```

정책에서 인가할 각 액션에 대해 이렇게 추가적인 메서드를 계속 정의할 수 있습니다. 예를 들어, 관련 액션에 대해 `view`, `delete` 같은 메서드를 만들 수도 있습니다. 메서드명은 자유롭게 지정할 수 있습니다.

Artisan 콘솔로 정책 생성 시 `--model` 옵션을 사용했다면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 액션에 대한 메서드가 포함되어 있습니다.

> [!NOTE]
> 모든 정책은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 정책 생성자에서 필요한 의존성을 타입힌트하면 자동으로 주입받을 수 있습니다.

<a name="policy-responses"></a>
### 정책 응답

지금까지는 정책 메서드에서 단순히 불리언(true/false) 값만 반환하는 예시만 보았습니다. 그러나 때때로 보다 자세한 응답(예: 오류 메시지 등)을 원할 수 있습니다. 이 경우, 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환하면 됩니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('You do not own this post.');
}
```

정책 메서드에서 인가 응답을 반환하더라도, `Gate::allows` 메서드는 단순 불리언 값만 반환합니다. 게이트가 반환한 인가 응답 전체를 확인하고 싶을 땐 `Gate::inspect`를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

`Gate::authorize` 메서드 사용 시 인가되지 않은 경우(즉 거절일 때) 발생하는 `AuthorizationException` 역시 정책 인가 응답 메시지를 HTTP 응답으로 그대로 전달합니다:

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 코드 커스터마이즈

정책 메서드를 통해 액션이 거부된 경우에도 기본적으로 `403` HTTP 응답이 반환됩니다. 그러나 다른 HTTP 상태 코드를 반환하고 싶다면, `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```

자원을 `404` 응답으로 숨기는 것이 웹 애플리케이션에서 자주 쓰이는 패턴이기 때문에, 편의상 `denyAsNotFound` 메서드도 제공합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```

<a name="methods-without-models"></a>
### 모델 없는 메서드

어떤 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 이런 상황은 주로 `create` 액션 인가에 해당하는데, 예를 들어 블로그에서 사용자가 게시물을 작성할 자격이 있는지 판단하고 싶을 수 있습니다. 이런 경우에는 정책 메서드가 사용자 인스턴스만 인수로 받으면 됩니다:

```php
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```

<a name="guest-users"></a>
### 게스트 사용자

기본적으로 인증되지 않은 사용자가 HTTP 요청을 수행한 경우, 모든 게이트 및 정책은 자동으로 `false`를 반환합니다. 다만, 이러한 인가 체크도 게이트나 정책 메서드에서 직접 처리하고 싶다면, 사용자 인수 정의에 "옵셔널(Nullable)" 타입힌트 또는 `null` 기본값을 사용할 수 있습니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```

<a name="policy-filters"></a>
### 정책 필터

특정 사용자에게 주어진 정책 내 모든 액션을 인가하고 싶은 경우, 정책에 `before` 메서드를 정의하면 됩니다. 이 메서드는 실제 정책 메서드가 호출되기 전에 실행되므로, 우선적으로 인가 여부를 판단할 수 있습니다. 주로 애플리케이션 관리자에게 모든 인가 권한을 주고 싶을 때 사용됩니다:

```php
use App\Models\User;

/**
 * Perform pre-authorization checks.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```

특정 사용자 유형에게 모든 인가를 거부하고 싶다면, `before` 메서드에서 `false`를 반환하시면 됩니다. `null`을 반환하면 인가 체크가 정책 메서드로 넘어갑니다.

> [!WARNING]
> 정책 클래스의 `before` 메서드는, 인가 능력 이름과 동일한 이름의 메서드가 해당 클래스에 있을 때만 호출됩니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 이용한 액션 인가

<a name="via-the-user-model"></a>
### User 모델을 통한 인가

Laravel에 내장된 `App\Models\User` 모델에는 인가를 도와주는 두 가지 메서드(`can`, `cannot`)가 있습니다. 여기에 인가하고 싶은 액션명과 관련 모델을 넘겨주면 됩니다. 예를 들어, 사용자가 특정 `App\Models\Post` 모델을 업데이트할 자격이 있는지 컨트롤러에서 아래와 같이 확인할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```

[정책이 등록](#registering-policies)되어 있다면, `can` 메서드는 자동으로 적절한 정책 메서드를 찾아 호출하고 결과값(불리언)을 반환합니다. 정책이 없는 경우, 액션명과 일치하는 클로저 기반 게이트를 호출하게 됩니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

어떤 액션은 `create` 같은 정책 메서드처럼 모델 인스턴스가 필요하지 않은 경우도 있습니다. 이럴 때는 클래스명을 `can` 메서드에 전달하면 됩니다. 클래스명을 이용해 어떤 정책을 사용할지 결정하게 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // Create the post...

        return redirect('/posts');
    }
}
```

<a name="via-the-gate-facade"></a>
### Gate 파사드를 통해

`App\Models\User` 모델의 메서드 외에도, 언제든지 `Gate` 파사드의 `authorize` 메서드를 통해 액션을 인가할 수 있습니다.

이 메서드 역시 인가할 액션명과 관련 모델을 받으며, 인가되지 않은 경우 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. 이 예외는 Laravel 예외 핸들러에 의해 403 상태 코드로 변환됩니다:

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
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // The current user can update the blog post...

        return redirect('/posts');
    }
}
```

<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

앞서 설명한 것처럼, `create` 같은 정책 메서드는 모델 인스턴스가 필요없습니다. 이때도 클래스명을 `authorize` 메서드에 전달하면 됩니다. 클래스명을 이용해 어떤 정책을 사용할지 결정하게 됩니다:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // The current user can create blog posts...

    return redirect('/posts');
}
```

<a name="via-middleware"></a>
### 미들웨어를 통해

Laravel은 요청이 라우트 또는 컨트롤러에 도달하기 전, 액션 인가를 수행하는 미들웨어를 제공합니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [미들웨어 별칭](/docs/master/middleware#middleware-aliases)을 이용해 라우트에 연결할 수 있는데, 이 별칭은 Laravel이 자동으로 등록합니다. 사용 예시는 다음과 같습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

위 예제에서 `can` 미들웨어의 첫 번째 인수는 인가할 액션명, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. [암묵적 모델 바인딩](/docs/master/routing#implicit-binding)을 이용하므로 `App\Models\Post` 모델 인스턴스를 자동으로 주입받게 됩니다. 인가에 실패하면 미들웨어는 403 상태 코드와 함께 HTTP 응답을 반환합니다.

편의상, `can` 미들웨어를 라우트에 `can` 메서드로 붙일 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

`create`와 같이 모델 인스턴스가 필요없는 정책 메서드는 미들웨어에 클래스명을 전달하면 됩니다. 이 클래스명이 어떤 정책을 사용할지 결정합니다:

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

문자열로 클래스 전체 이름을 작성하는 것이 번거롭다면, `can` 메서드를 통해 더 간단히 연결할 수 있습니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade 템플릿을 통해

Blade 템플릿을 작성할 때, 특정 액션에 대해 인가된 사용자만 볼 수 있는 영역을 표시하고 싶을 수 있습니다. 예를 들어, 블로그 게시물의 수정 폼을 사용자가 실제로 수정할 권한이 있을 때만 보여주고 싶을 때, 다음과 같이 `@can` 및 `@cannot` 지시문을 쓸 수 있습니다:

```blade
@can('update', $post)
    <!-- The current user can update the post... -->
@elsecan('create', App\Models\Post::class)
    <!-- The current user can create new posts... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- The current user cannot update the post... -->
@elsecannot('create', App\Models\Post::class)
    <!-- The current user cannot create new posts... -->
@endcannot
```

이 지시문들은 `@if`, `@unless` 문을 줄여 쓰는 편리한 방법입니다. 위 `@can`, `@cannot` 구문은 아래와 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

여러 액션 중 하나라도 인가되었을 때를 확인하려면 `@canany` 지시문을 사용할 수 있습니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

기타 인가 방법과 마찬가지로, 모델 인스턴스가 필요 없는 액션이라면 클래스명을 `@can` 및 `@cannot` 지시문에 전달하면 됩니다:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```

<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공

정책을 통해 액션을 인가할 때 여러 인자를 컨텍스트로 넘기고 싶다면, 두 번째 인수에 배열을 전달할 수 있습니다. 이 배열의 첫 번째 요소는 사용할 정책을 결정하며, 이후 요소들은 정책 메서드의 파라미터로 전달되어 추가 컨텍스트로 사용할 수 있습니다. 예를 들어, 다음과 같이 추가 `$category` 파라미터가 있는 `PostPolicy` 메서드를 가정해보겠습니다:

```php
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```

이런 경우, 인증된 사용자가 게시물을 수정할 수 있는지 정책 메서드를 아래와 같이 호출할 수 있습니다:

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // The current user can update the blog post...

    return redirect('/posts');
}
```

<a name="authorization-and-inertia"></a>
## 인가 & Inertia

인가(authorization)는 항상 서버 측에서 처리해야 하지만, 프런트엔드 애플리케이션에서 인가 정보를 활용해 UI를 적절히 렌더링하는 것도 편리할 때가 많습니다. Laravel은 Inertia 기반 프런트엔드에 인가 정보를 노출하고 사용하는 데 대한 공식 규칙을 지정하지 않습니다.

그러나, Laravel의 Inertia 기반 [스타터 키트](/docs/master/starter-kits)를 사용 중이라면, 이미 애플리케이션에 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드에서 모든 Inertia 페이지에 제공할 공통 데이터를 반환할 수 있습니다. 이 공통 데이터에 인가 정보를 정의하면 편리하게 활용할 수 있습니다:

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
     * Define the props that are shared by default.
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
