<!-- # Authorization -->
# Authorization

- [Introduction](#introduction)
- [Gates](#gates)
    - [Writing Gates](#writing-gates)
    - [Authorizing Actions](#authorizing-actions-via-gates)
    - [Gate Responses](#gate-responses)
    - [Intercepting Gate Checks](#intercepting-gate-checks)
    - [Inline Authorization](#inline-authorization)
- [Creating Policies](#creating-policies)
    - [Generating Policies](#generating-policies)
    - [Registering Policies](#registering-policies)
- [Writing Policies](#writing-policies)
    - [Policy Methods](#policy-methods)
    - [Policy Responses](#policy-responses)
    - [Methods Without Models](#methods-without-models)
    - [Guest Users](#guest-users)
    - [Policy Filters](#policy-filters)
- [Authorizing Actions Using Policies](#authorizing-actions-using-policies)
    - [Via the User Model](#via-the-user-model)
    - [Via the Gate Facade](#via-the-gate-facade)
    - [Via Middleware](#via-middleware)
    - [Via Blade Templates](#via-blade-templates)
    - [Supplying Additional Context](#supplying-additional-context)
- [Authorization & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to providing built-in [authentication](/docs/13.x/authentication) services, Laravel also provides a simple way to authorize user actions against a given resource. For example, even though a user is authenticated, they may not be authorized to update or delete certain Eloquent models or database records managed by your application. Laravel's authorization features provide an easy, organized way of managing these types of authorization checks. -->
Laravel은 내장 [authentication](/docs/13.x/authentication) 서비스를 제공하는 것에 더해, 특정 리소스에 대한 사용자 작업을 인가하는 간단한 방법도 제공합니다. 예를 들어 사용자가 인증되었더라도, 애플리케이션이 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 수정하거나 삭제할 권한은 없을 수 있습니다. Laravel의 인가 기능은 이러한 유형의 인가 검사를 쉽고 체계적으로 관리할 수 있는 방법을 제공합니다.

<!-- Laravel provides two primary ways of authorizing actions: [gates](#gates) and [policies](#creating-policies). Think of gates and policies like routes and controllers. Gates provide a simple, closure-based approach to authorization while policies, like controllers, group logic around a particular model or resource. In this documentation, we'll explore gates first and then examine policies. -->
Laravel은 작업을 인가하는 두 가지 주요 방법을 제공합니다: [gates](#gates)와 [policies](#creating-policies)입니다. 게이트와 정책은 라우트와 컨트롤러와 비슷하다고 생각하면 됩니다. 게이트는 클로저 기반의 간단한 인가 방식을 제공하고, 정책은 컨트롤러처럼 특정 모델이나 리소스를 중심으로 로직을 묶습니다. 이 문서에서는 먼저 게이트를 살펴본 다음 정책을 알아보겠습니다.

<!-- You do not need to choose between exclusively using gates or exclusively using policies when building an application. Most applications will most likely contain some mixture of gates and policies, and that is perfectly fine! Gates are most applicable to actions that are not related to any model or resource, such as viewing an administrator dashboard. In contrast, policies should be used when you wish to authorize an action for a particular model or resource. -->
애플리케이션을 만들 때 게이트만 사용하거나 정책만 사용하도록 선택할 필요는 없습니다. 대부분의 애플리케이션은 게이트와 정책을 함께 사용하게 되며, 이는 전혀 문제가 되지 않습니다. 게이트는 관리자 대시보드 보기처럼 특정 모델이나 리소스와 관련이 없는 작업에 가장 적합합니다. 반대로 특정 모델이나 리소스에 대한 작업을 인가하려는 경우에는 정책을 사용해야 합니다.

<a name="gates"></a>
<!-- ## Gates -->
## Gates

<a name="writing-gates"></a>
<!-- ### Writing Gates -->
### Writing Gates

> [!WARNING]
> 게이트는 Laravel 인가 기능의 기본을 배우기에 좋은 방법입니다. 하지만 견고한 Laravel 애플리케이션을 만들 때는 인가 규칙을 체계적으로 구성하기 위해 [policies](#creating-policies) 사용을 고려해야 합니다.

<!-- Gates are simply closures that determine if a user is authorized to perform a given action. Typically, gates are defined within the `boot` method of the `App\Providers\AppServiceProvider` class using the `Gate` facade. Gates always receive a user instance as their first argument and may optionally receive additional arguments such as a relevant Eloquent model. -->
게이트는 사용자가 특정 작업을 수행할 권한이 있는지 판단하는 클로저입니다. 일반적으로 게이트는 `Gate` 파사드를 사용하여 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받으며, 필요에 따라 관련 Eloquent 모델 같은 추가 인수를 받을 수 있습니다.

<!-- In this example, we'll define a gate to determine if a user can update a given `App\Models\Post` model. The gate will accomplish this by comparing the user's `id` against the `user_id` of the user that created the post: -->
이 예제에서는 사용자가 특정 `App\Models\Post` 모델을 수정할 수 있는지 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`와 게시글을 작성한 사용자의 `user_id`를 비교하여 이를 판단합니다:

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

<!-- Like controllers, gates may also be defined using a class callback array: -->
컨트롤러와 마찬가지로, 게이트도 클래스 콜백 배열을 사용하여 정의할 수 있습니다:

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
<!-- ### Authorizing Actions -->
### Authorizing Actions

<!-- To authorize an action using gates, you should use the `allows` or `denies` methods provided by the `Gate` facade. Note that you are not required to pass the currently authenticated user to these methods. Laravel will automatically take care of passing the user into the gate closure. It is typical to call the gate authorization methods within your application's controllers before performing an action that requires authorization: -->
게이트를 사용하여 작업을 인가하려면 `Gate` 파사드가 제공하는 `allows` 또는 `denies` 메서드를 사용해야 합니다. 이 메서드에 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 사용자를 게이트 클로저에 자동으로 전달합니다. 일반적으로 애플리케이션의 컨트롤러에서 인가가 필요한 작업을 수행하기 전에 게이트 인가 메서드를 호출합니다:

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

<!-- If you would like to determine if a user other than the currently authenticated user is authorized to perform an action, you may use the `forUser` method on the `Gate` facade: -->
현재 인증된 사용자가 아닌 다른 사용자가 작업을 수행할 권한이 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

<!-- You may authorize multiple actions at a time using the `any` or `none` methods: -->
`any` 또는 `none` 메서드를 사용하면 여러 작업을 한 번에 인가할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
<!-- #### Authorizing or Throwing Exceptions -->
#### Authorizing or Throwing Exceptions

<!-- If you would like to attempt to authorize an action and automatically throw an `Illuminate\Auth\Access\AuthorizationException` if the user is not allowed to perform the given action, you may use the `Gate` facade's `authorize` method. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel: -->
작업 인가를 시도하고, 사용자가 해당 작업을 수행할 수 없는 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException`을 던지고 싶다면 `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException` 인스턴스는 Laravel에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
<!-- #### Supplying Additional Context -->
#### Supplying Additional Context

<!-- The gate methods for authorizing abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) and the authorization [Blade directives](#via-blade-templates) (`@can`, `@cannot`, `@canany`) can receive an array as their second argument. These array elements are passed as parameters to the gate closure, and can be used for additional context when making authorization decisions: -->
능력을 인가하는 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 인가 [Blade directives](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인수로 배열을 받을 수 있습니다. 이 배열의 요소는 게이트 클로저에 매개변수로 전달되며, 인가 결정을 내릴 때 추가 컨텍스트로 사용할 수 있습니다:

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
<!-- ### Gate Responses -->
### Gate Responses

<!-- So far, we have only examined gates that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` from your gate: -->
지금까지는 단순한 boolean 값을 반환하는 게이트만 살펴보았습니다. 하지만 때로는 오류 메시지를 포함한 더 자세한 응답을 반환하고 싶을 수 있습니다. 이 경우 게이트에서 `Illuminate\Auth\Access\Response`를 반환하면 됩니다:

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

<!-- Even when you return an authorization response from your gate, the `Gate::allows` method will still return a simple boolean value; however, you may use the `Gate::inspect` method to get the full authorization response returned by the gate: -->
게이트에서 인가 응답을 반환하더라도 `Gate::allows` 메서드는 여전히 단순한 boolean 값을 반환합니다. 하지만 게이트가 반환한 전체 인가 응답을 얻고 싶다면 `Gate::inspect` 메서드를 사용할 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

<!-- When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response: -->
작업이 인가되지 않은 경우 `AuthorizationException`을 던지는 `Gate::authorize` 메서드를 사용할 때는, 인가 응답에서 제공한 오류 메시지가 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
<!-- #### Customizing The HTTP Response Status -->
#### Customizing The HTTP Response Status

<!-- When an action is denied via a Gate, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
Gate를 통해 작업이 거부되면 `403` HTTP 응답이 반환됩니다. 하지만 때로는 다른 HTTP 상태 코드를 반환하는 것이 유용할 수 있습니다. 실패한 인가 검사에 대해 반환할 HTTP 상태 코드는 `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하여 커스터마이징할 수 있습니다:

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

<!-- Because hiding resources via a `404` response is such a common pattern for web applications, the `denyAsNotFound` method is offered for convenience: -->
`404` 응답으로 리소스를 숨기는 방식은 웹 애플리케이션에서 매우 흔한 패턴이기 때문에, 편의를 위해 `denyAsNotFound` 메서드가 제공됩니다:

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
<!-- ### Intercepting Gate Checks -->
### Intercepting Gate Checks

<!-- Sometimes, you may wish to grant all abilities to a specific user. You may use the `before` method to define a closure that is run before all other authorization checks: -->
때로는 특정 사용자에게 모든 능력을 허용하고 싶을 수 있습니다. `before` 메서드를 사용하면 다른 모든 인가 검사보다 먼저 실행되는 클로저를 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

<!-- If the `before` closure returns a non-null result that result will be considered the result of the authorization check. -->
`before` 클로저가 null이 아닌 결과를 반환하면, 그 결과가 인가 검사의 결과로 간주됩니다.

<!-- You may use the `after` method to define a closure to be executed after all other authorization checks: -->
`after` 메서드를 사용하면 다른 모든 인가 검사 이후에 실행될 클로저를 정의할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

<!-- Values returned by `after` closures will not override the result of the authorization check unless the gate or policy returned `null`. -->
게이트나 정책이 `null`을 반환하지 않는 한, `after` 클로저가 반환하는 값은 인가 검사 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
<!-- ### Inline Authorization -->
### Inline Authorization

<!-- Occasionally, you may wish to determine if the currently authenticated user is authorized to perform a given action without writing a dedicated gate that corresponds to the action. Laravel allows you to perform these types of "inline" authorization checks via the `Gate::allowIf` and `Gate::denyIf` methods. Inline authorization does not execute any defined ["before" or "after" authorization hooks](#intercepting-gate-checks): -->
가끔은 특정 작업에 대응하는 전용 게이트를 작성하지 않고도, 현재 인증된 사용자가 해당 작업을 수행할 권한이 있는지 판단하고 싶을 수 있습니다. Laravel은 `Gate::allowIf`와 `Gate::denyIf` 메서드를 통해 이러한 유형의 "인라인" 인가 검사를 수행할 수 있도록 합니다. 인라인 인가는 정의된 ["before" or "after" authorization hooks](#intercepting-gate-checks)을 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

<!-- If the action is not authorized or if no user is currently authenticated, Laravel will automatically throw an `Illuminate\Auth\Access\AuthorizationException` exception. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel's exception handler. -->
작업이 인가되지 않았거나 현재 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. `AuthorizationException` 인스턴스는 Laravel의 예외 핸들러에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
<!-- ## Creating Policies -->
## Creating Policies

<a name="generating-policies"></a>
<!-- ### Generating Policies -->
### Generating Policies

<!-- Policies are classes that organize authorization logic around a particular model or resource. For example, if your application is a blog, you may have an `App\Models\Post` model and a corresponding `App\Policies\PostPolicy` to authorize user actions such as creating or updating posts. -->
정책은 특정 모델이나 리소스를 중심으로 인가 로직을 구성하는 클래스입니다. 예를 들어 애플리케이션이 블로그라면, `App\Models\Post` 모델과 게시글 생성 또는 수정 같은 사용자 작업을 인가하는 해당 `App\Policies\PostPolicy`가 있을 수 있습니다.

<!-- You may generate a policy using the `make:policy` Artisan command. The generated policy will be placed in the `app/Policies` directory. If this directory does not exist in your application, Laravel will create it for you: -->
`make:policy` Artisan 명령어를 사용하여 정책을 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉터리에 배치됩니다. 애플리케이션에 이 디렉터리가 없다면 Laravel이 자동으로 생성합니다:

```shell
php artisan make:policy PostPolicy
```

<!-- The `make:policy` command will generate an empty policy class. If you would like to generate a class with example policy methods related to viewing, creating, updating, and deleting the resource, you may provide a `--model` option when executing the command: -->
`make:policy` 명령어는 비어 있는 정책 클래스를 생성합니다. 리소스 조회, 생성, 수정, 삭제와 관련된 예제 정책 메서드가 포함된 클래스를 생성하고 싶다면, 명령어를 실행할 때 `--model` 옵션을 제공하면 됩니다:

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
<!-- ### Registering Policies -->
### Registering Policies

<a name="policy-discovery"></a>
<!-- #### Policy Discovery -->
#### Policy Discovery

<!-- By default, Laravel automatically discover policies as long as the model and policy follow standard Laravel naming conventions. Specifically, the policies must be in a `Policies` directory at or above the directory that contains your models. So, for example, the models may be placed in the `app/Models` directory while the policies may be placed in the `app/Policies` directory. In this situation, Laravel will check for policies in `app/Models/Policies` then `app/Policies`. In addition, the policy name must match the model name and have a `Policy` suffix. So, a `User` model would correspond to a `UserPolicy` policy class. -->
기본적으로 모델과 정책이 표준 Laravel 명명 규칙을 따르면 Laravel은 정책을 자동으로 발견합니다. 구체적으로 정책은 모델이 들어 있는 디렉터리 또는 그 상위 디렉터리의 `Policies` 디렉터리 안에 있어야 합니다. 예를 들어 모델은 `app/Models` 디렉터리에 있고 정책은 `app/Policies` 디렉터리에 있을 수 있습니다. 이 경우 Laravel은 `app/Models/Policies`를 확인한 다음 `app/Policies`에서 정책을 찾습니다. 또한 정책 이름은 모델 이름과 일치해야 하며 `Policy` 접미사를 가져야 합니다. 따라서 `User` 모델은 `UserPolicy` 정책 클래스에 대응합니다.

<!-- If you would like to define your own policy discovery logic, you may register a custom policy discovery callback using the `Gate::guessPolicyNamesUsing` method. Typically, this method should be called from the `boot` method of your application's `AppServiceProvider`: -->
직접 정책 발견 로직을 정의하고 싶다면 `Gate::guessPolicyNamesUsing` 메서드를 사용하여 커스텀 정책 발견 콜백을 등록할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다:

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
<!-- #### Manually Registering Policies -->
#### Manually Registering Policies

<!-- Using the `Gate` facade, you may manually register policies and their corresponding models within the `boot` method of your application's `AppServiceProvider`: -->
`Gate` 파사드를 사용하면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 정책과 그에 대응하는 모델을 수동으로 등록할 수 있습니다:

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

<!-- Alternatively, you may place the `UsePolicy` attribute on a model class to inform Laravel of the model's corresponding policy: -->
또는 모델 클래스에 `UsePolicy` 속성을 배치하여 Laravel에 모델에 대응하는 정책을 알려줄 수 있습니다:

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
<!-- ## Writing Policies -->
## Writing Policies

<a name="policy-methods"></a>
<!-- ### Policy Methods -->
### Policy Methods

<!-- Once the policy class has been registered, you may add methods for each action it authorizes. For example, let's define an `update` method on our `PostPolicy` which determines if a given `App\Models\User` can update a given `App\Models\Post` instance. -->
정책 클래스가 등록되면, 해당 정책이 인가하는 각 작업에 대한 메서드를 추가할 수 있습니다. 예를 들어 주어진 `App\Models\User`가 주어진 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단하는 `update` 메서드를 `PostPolicy`에 정의해 보겠습니다.

<!-- The `update` method will receive a `User` and a `Post` instance as its arguments, and should return `true` or `false` indicating whether the user is authorized to update the given `Post`. So, in this example, we will verify that the user's `id` matches the `user_id` on the post: -->
`update` 메서드는 인수로 `User`와 `Post` 인스턴스를 받으며, 사용자가 주어진 `Post`를 수정할 권한이 있는지를 나타내는 `true` 또는 `false`를 반환해야 합니다. 따라서 이 예제에서는 사용자의 `id`가 게시글의 `user_id`와 일치하는지 확인합니다:

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

<!-- You may continue to define additional methods on the policy as needed for the various actions it authorizes. For example, you might define `view` or `delete` methods to authorize various `Post` related actions, but remember you are free to give your policy methods any name you like. -->
정책이 인가하는 여러 작업에 맞게 필요한 추가 메서드를 계속 정의할 수 있습니다. 예를 들어 다양한 `Post` 관련 작업을 인가하기 위해 `view` 또는 `delete` 메서드를 정의할 수 있습니다. 다만 정책 메서드 이름은 원하는 대로 자유롭게 정할 수 있다는 점을 기억하세요.

<!-- If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `viewAny`, `view`, `create`, `update`, `delete`, `restore`, and `forceDelete` actions. -->
Artisan 콘솔을 통해 정책을 생성할 때 `--model` 옵션을 사용했다면, 해당 정책에는 이미 `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 작업을 위한 메서드가 포함되어 있습니다.

> [!NOTE]
> 모든 정책은 Laravel [service container](/docs/13.x/container)를 통해 해결되므로, 정책의 생성자에서 필요한 의존성을 타입 힌트하면 자동으로 주입받을 수 있습니다.

<a name="policy-responses"></a>
<!-- ### Policy Responses -->
### Policy Responses

<!-- So far, we have only examined policy methods that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` instance from your policy method: -->
지금까지는 간단한 boolean 값을 반환하는 정책 메서드만 살펴보았습니다. 그러나 때로는 오류 메시지를 포함해 더 자세한 응답을 반환하고 싶을 수 있습니다. 이렇게 하려면 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환하면 됩니다:

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

<!-- When returning an authorization response from your policy, the `Gate::allows` method will still return a simple boolean value; however, you may use the `Gate::inspect` method to get the full authorization response returned by the gate: -->
정책에서 인가 응답을 반환하더라도 `Gate::allows` 메서드는 여전히 간단한 boolean 값을 반환합니다. 하지만 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 인가 응답을 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

<!-- When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response: -->
액션이 인가되지 않았을 때 `AuthorizationException`을 던지는 `Gate::authorize` 메서드를 사용하는 경우, 인가 응답에서 제공한 오류 메시지가 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
<!-- #### Customizing the HTTP Response Status -->
#### Customizing the HTTP Response Status

<!-- When an action is denied via a policy method, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
정책 메서드를 통해 액션이 거부되면 `403` HTTP 응답이 반환됩니다. 하지만 때로는 다른 HTTP 상태 코드를 반환하는 것이 유용할 수 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용해 실패한 인가 확인에 대해 반환되는 HTTP 상태 코드를 커스터마이징할 수 있습니다:

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

<!-- Because hiding resources via a `404` response is such a common pattern for web applications, the `denyAsNotFound` method is offered for convenience: -->
웹 애플리케이션에서 `404` 응답으로 리소스를 숨기는 방식은 매우 흔한 패턴이므로, 편의를 위해 `denyAsNotFound` 메서드가 제공됩니다:

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
<!-- ### Methods Without Models -->
### Methods Without Models

<!-- Some policy methods only receive an instance of the currently authenticated user. This situation is most common when authorizing `create` actions. For example, if you are creating a blog, you may wish to determine if a user is authorized to create any posts at all. In these situations, your policy method should only expect to receive a user instance: -->
일부 정책 메서드는 현재 인증된 사용자의 인스턴스만 받습니다. 이런 상황은 `create` 액션을 인가할 때 가장 흔합니다. 예를 들어 블로그를 만들고 있다면, 어떤 사용자가 게시물을 만들 수 있는지 여부를 판단하고 싶을 수 있습니다. 이런 경우 정책 메서드는 사용자 인스턴스만 받도록 작성해야 합니다:

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
<!-- ### Guest Users -->
### Guest Users

<!-- By default, all gates and policies automatically return `false` if the incoming HTTP request was not initiated by an authenticated user. However, you may allow these authorization checks to pass through to your gates and policies by declaring an "optional" type-hint or supplying a `null` default value for the user argument definition: -->
기본적으로 모든 게이트와 정책은 들어오는 HTTP 요청이 인증된 사용자에 의해 시작되지 않은 경우 자동으로 `false`를 반환합니다. 하지만 사용자 인수 정의에 "선택적" 타입 힌트를 선언하거나 `null` 기본값을 제공하면, 이러한 인가 확인이 게이트와 정책까지 전달되도록 허용할 수 있습니다:

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
<!-- ### Policy Filters -->
### Policy Filters

<!-- For certain users, you may wish to authorize all actions within a given policy. To accomplish this, define a `before` method on the policy. The `before` method will be executed before any other methods on the policy, giving you an opportunity to authorize the action before the intended policy method is actually called. This feature is most commonly used for authorizing application administrators to perform any action: -->
특정 사용자에게는 주어진 정책 안의 모든 액션을 인가하고 싶을 수 있습니다. 이를 위해 정책에 `before` 메서드를 정의합니다. `before` 메서드는 정책의 다른 어떤 메서드보다 먼저 실행되므로, 실제 대상 정책 메서드가 호출되기 전에 액션을 인가할 기회를 제공합니다. 이 기능은 애플리케이션 관리자가 모든 액션을 수행할 수 있도록 인가할 때 가장 흔히 사용됩니다:

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

<!-- If you would like to deny all authorization checks for a particular type of user then you may return `false` from the `before` method. If `null` is returned, the authorization check will fall through to the policy method. -->
특정 유형의 사용자에 대해 모든 인가 확인을 거부하고 싶다면 `before` 메서드에서 `false`를 반환하면 됩니다. `null`이 반환되면 인가 확인은 정책 메서드로 넘어갑니다.

> [!WARNING]
> 정책 클래스에 확인 중인 능력의 이름과 일치하는 이름의 메서드가 없으면, 해당 정책 클래스의 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
<!-- ## Authorizing Actions Using Policies -->
## Authorizing Actions Using Policies

<a name="via-the-user-model"></a>
<!-- ### Via the User Model -->
### Via the User Model

<!-- The `App\Models\User` model that is included with your Laravel application includes two helpful methods for authorizing actions: `can` and `cannot`. The `can` and `cannot` methods receive the name of the action you wish to authorize and the relevant model. For example, let's determine if a user is authorized to update a given `App\Models\Post` model. Typically, this will be done within a controller method: -->
Laravel 애플리케이션에 포함된 `App\Models\User` 모델은 액션을 인가하는 데 유용한 두 메서드인 `can`과 `cannot`을 제공합니다. `can`과 `cannot` 메서드는 인가하려는 액션의 이름과 관련 모델을 받습니다. 예를 들어 사용자가 주어진 `App\Models\Post` 모델을 업데이트할 권한이 있는지 확인해 보겠습니다. 일반적으로 이 작업은 컨트롤러 메서드 안에서 수행됩니다:

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

<!-- If a [policy is registered](#registering-policies) for the given model, the `can` method will automatically call the appropriate policy and return the boolean result. If no policy is registered for the model, the `can` method will attempt to call the closure-based Gate matching the given action name. -->
주어진 모델에 대해 [policy is registered](#registering-policies) 있다면, `can` 메서드는 자동으로 적절한 정책을 호출하고 boolean 결과를 반환합니다. 모델에 등록된 정책이 없다면, `can` 메서드는 주어진 액션 이름과 일치하는 클로저 기반 Gate를 호출하려고 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Remember, some actions may correspond to policy methods like `create` that do not require a model instance. In these situations, you may pass a class name to the `can` method. The class name will be used to determine which policy to use when authorizing the action: -->
일부 액션은 모델 인스턴스가 필요 없는 `create` 같은 정책 메서드에 대응할 수 있다는 점을 기억하십시오. 이런 경우 `can` 메서드에 클래스 이름을 전달할 수 있습니다. 클래스 이름은 액션을 인가할 때 어떤 정책을 사용할지 결정하는 데 사용됩니다:

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
<!-- ### Via the `Gate` Facade -->
### Via the `Gate` Facade

<!-- In addition to helpful methods provided to the `App\Models\User` model, you can always authorize actions via the `Gate` facade's `authorize` method. -->
`App\Models\User` 모델에 제공되는 유용한 메서드 외에도, 언제든지 `Gate` Facade의 `authorize` 메서드를 통해 액션을 인가할 수 있습니다.

<!-- Like the `can` method, this method accepts the name of the action you wish to authorize and the relevant model. If the action is not authorized, the `authorize` method will throw an `Illuminate\Auth\Access\AuthorizationException` exception which the Laravel exception handler will automatically convert to an HTTP response with a 403 status code: -->
`can` 메서드와 마찬가지로, 이 메서드는 인가하려는 액션의 이름과 관련 모델을 받습니다. 액션이 인가되지 않으면 `authorize` 메서드는 `Illuminate\Auth\Access\AuthorizationException` 예외를 던지며, Laravel 예외 핸들러는 이를 자동으로 403 상태 코드를 가진 HTTP 응답으로 변환합니다:

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
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- As previously discussed, some policy methods like `create` do not require a model instance. In these situations, you should pass a class name to the `authorize` method. The class name will be used to determine which policy to use when authorizing the action: -->
앞서 설명했듯이, `create` 같은 일부 정책 메서드는 모델 인스턴스가 필요하지 않습니다. 이런 경우 `authorize` 메서드에 클래스 이름을 전달해야 합니다. 클래스 이름은 액션을 인가할 때 어떤 정책을 사용할지 결정하는 데 사용됩니다:

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
<!-- ### Via Middleware -->
### Via Middleware

<!-- Laravel includes a middleware that can authorize actions before the incoming request even reaches your routes or controllers. By default, the `Illuminate\Auth\Middleware\Authorize` middleware may be attached to a route using the `can` [middleware alias](/docs/13.x/middleware#middleware-aliases), which is automatically registered by Laravel. Let's explore an example of using the `can` middleware to authorize that a user can update a post: -->
Laravel에는 들어오는 요청이 라우트나 컨트롤러에 도달하기 전에 액션을 인가할 수 있는 Middleware가 포함되어 있습니다. 기본적으로 `Illuminate\Auth\Middleware\Authorize` Middleware는 Laravel이 자동으로 등록하는 `can` [middleware alias](/docs/13.x/middleware#middleware-aliases)을 사용해 라우트에 연결할 수 있습니다. 사용자가 게시물을 업데이트할 수 있는지 인가하기 위해 `can` Middleware를 사용하는 예를 살펴보겠습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

<!-- In this example, we're passing the `can` middleware two arguments. The first is the name of the action we wish to authorize and the second is the route parameter we wish to pass to the policy method. In this case, since we are using [implicit model binding](/docs/13.x/routing#implicit-binding), an `App\Models\Post` model will be passed to the policy method. If the user is not authorized to perform the given action, an HTTP response with a 403 status code will be returned by the middleware. -->
이 예제에서는 `can` Middleware에 두 개의 인수를 전달합니다. 첫 번째는 인가하려는 액션의 이름이고, 두 번째는 정책 메서드에 전달하려는 라우트 파라미터입니다. 이 경우 [implicit model binding](/docs/13.x/routing#implicit-binding)을 사용하고 있으므로 `App\Models\Post` 모델이 정책 메서드에 전달됩니다. 사용자가 주어진 액션을 수행할 권한이 없다면, Middleware가 403 상태 코드를 가진 HTTP 응답을 반환합니다.

<!-- For convenience, you may also attach the `can` middleware to your route using the `can` method: -->
편의를 위해 `can` 메서드를 사용해 `can` Middleware를 라우트에 연결할 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

<!-- If you are using [controller middleware attributes](/docs/13.x/controllers#middleware-attributes), you may apply the `can` middleware via the `Authorize` attribute: -->
[controller middleware attributes](/docs/13.x/controllers#middleware-attributes)을 사용하고 있다면, `Authorize` 속성을 통해 `can` Middleware를 적용할 수 있습니다:

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;

#[Authorize('update', 'post')]
public function update(Post $post)
{
    // The current user may update the post...
}
```

<a name="middleware-actions-that-dont-require-models"></a>
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Again, some policy methods like `create` do not require a model instance. In these situations, you may pass a class name to the middleware. The class name will be used to determine which policy to use when authorizing the action: -->
다시 말해, `create` 같은 일부 정책 메서드는 모델 인스턴스가 필요하지 않습니다. 이런 경우 Middleware에 클래스 이름을 전달할 수 있습니다. 클래스 이름은 액션을 인가할 때 어떤 정책을 사용할지 결정하는 데 사용됩니다:

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

<!-- Specifying the entire class name within a string middleware definition can become cumbersome. For that reason, you may choose to attach the `can` middleware to your route using the `can` method: -->
문자열 Middleware 정의 안에 전체 클래스 이름을 지정하는 것은 번거로울 수 있습니다. 따라서 `can` 메서드를 사용해 `can` Middleware를 라우트에 연결하도록 선택할 수 있습니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
<!-- ### Via Blade Templates -->
### Via Blade Templates

<!-- When writing Blade templates, you may wish to display a portion of the page only if the user is authorized to perform a given action. For example, you may wish to show an update form for a blog post only if the user can actually update the post. In this situation, you may use the `@can` and `@cannot` directives: -->
Blade 템플릿을 작성할 때, 사용자가 주어진 액션을 수행할 권한이 있는 경우에만 페이지의 일부를 표시하고 싶을 수 있습니다. 예를 들어 사용자가 실제로 게시물을 업데이트할 수 있는 경우에만 블로그 게시물의 업데이트 폼을 보여주고 싶을 수 있습니다. 이런 경우 `@can` 및 `@cannot` 지시어를 사용할 수 있습니다:

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

<!-- These directives are convenient shortcuts for writing `@if` and `@unless` statements. The `@can` and `@cannot` statements above are equivalent to the following statements: -->
이 지시어들은 `@if`와 `@unless` 문을 작성하기 위한 편리한 단축 표현입니다. 위의 `@can` 및 `@cannot` 문은 다음 문과 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

<!-- You may also determine if a user is authorized to perform any action from a given array of actions. To accomplish this, use the `@canany` directive: -->
주어진 액션 배열 중 어떤 액션이든 사용자가 수행할 권한이 있는지 확인할 수도 있습니다. 이를 위해 `@canany` 지시어를 사용합니다:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Like most of the other authorization methods, you may pass a class name to the `@can` and `@cannot` directives if the action does not require a model instance: -->
대부분의 다른 인가 메서드와 마찬가지로, 액션에 모델 인스턴스가 필요하지 않다면 `@can` 및 `@cannot` 지시어에 클래스 이름을 전달할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```

<a name="supplying-additional-context"></a>
<!-- ### Supplying Additional Context -->
### Supplying Additional Context

<!-- When authorizing actions using policies, you may pass an array as the second argument to the various authorization functions and helpers. The first element in the array will be used to determine which policy should be invoked, while the rest of the array elements are passed as parameters to the policy method and can be used for additional context when making authorization decisions. For example, consider the following `PostPolicy` method definition which contains an additional `$category` parameter: -->
정책을 사용해 액션을 인가할 때, 다양한 인가 함수와 헬퍼의 두 번째 인수로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책을 호출할지 결정하는 데 사용되고, 나머지 배열 요소는 정책 메서드에 파라미터로 전달되어 인가 결정을 내릴 때 추가 컨텍스트로 사용할 수 있습니다. 예를 들어 추가 `$category` 파라미터를 포함하는 다음 `PostPolicy` 메서드 정의를 살펴보십시오:

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
<!-- When attempting to determine if the authenticated user can update a given post, we can invoke this policy method like so: -->
인증된 사용자가 주어진 게시글을 업데이트할 수 있는지 확인하려면, 다음과 같이 이 policy 메서드를 호출할 수 있습니다.

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
<!-- ## Authorization & Inertia -->
## Authorization & Inertia

<!-- Although authorization must always be handled on the server, it can often be convenient to provide your frontend application with authorization data in order to properly render your application's UI. Laravel does not define a required convention for exposing authorization information to an Inertia powered frontend. -->
인가는 항상 서버에서 처리해야 하지만, 애플리케이션의 UI를 적절히 렌더링하기 위해 프론트엔드 애플리케이션에 인가 데이터를 제공하면 편리한 경우가 많습니다. Laravel은 Inertia 기반 프론트엔드에 인가 정보를 노출하는 데 필요한 필수 규약을 정의하지 않습니다.

<!-- However, if you are using one of Laravel's Inertia-based [starter kits](/docs/13.x/starter-kits), your application already contains a `HandleInertiaRequests` middleware. Within this middleware's `share` method, you may return shared data that will be provided to all Inertia pages in your application. This shared data can serve as a convenient location to define authorization information for the user: -->
하지만 Laravel의 Inertia 기반 [starter kits](/docs/13.x/starter-kits) 중 하나를 사용하고 있다면, 애플리케이션에는 이미 `HandleInertiaRequests` middleware가 포함되어 있습니다. 이 middleware의 `share` 메서드 안에서, 애플리케이션의 모든 Inertia 페이지에 제공될 공유 데이터를 반환할 수 있습니다. 이 공유 데이터는 사용자에 대한 인가 정보를 정의하기에 편리한 위치로 사용할 수 있습니다.

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
