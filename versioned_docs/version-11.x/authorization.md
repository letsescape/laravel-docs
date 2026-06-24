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

<!-- In addition to providing built-in [authentication](/docs/11.x/authentication) services, Laravel also provides a simple way to authorize user actions against a given resource. For example, even though a user is authenticated, they may not be authorized to update or delete certain Eloquent models or database records managed by your application. Laravel's authorization features provide an easy, organized way of managing these types of authorization checks. -->
Laravel은 기본적인 [authentication](/docs/11.x/authentication) 서비스 외에도, 주어진 리소스에 대해 사용자의 행동을 인가(권한 부여)할 수 있는 간단한 방법을 제공합니다. 예를 들어, 사용자가 인증되었다고 해도, 애플리케이션에서 관리하는 특정 Eloquent 모델이나 데이터베이스 레코드를 업데이트하거나 삭제할 권한이 없을 수 있습니다. Laravel의 인가 기능은 이러한 인가 검사를 쉽고 체계적으로 관리할 수 있도록 도와줍니다.

<!-- Laravel provides two primary ways of authorizing actions: [gates](#gates) and [policies](#creating-policies). Think of gates and policies like routes and controllers. Gates provide a simple, closure-based approach to authorization while policies, like controllers, group logic around a particular model or resource. In this documentation, we'll explore gates first and then examine policies. -->
Laravel에서는 행동을 인가하는 주요 방법으로 [gates](#gates)와 [policies](#creating-policies) 두 가지가 있습니다. 게이트와 정책의 관계를 라우트와 컨트롤러에 비유할 수 있습니다. 게이트는 단순히 클로저 기반의 인가 방식을 제공하며, 정책은 컨트롤러처럼 특정 모델이나 리소스에 관련된 인가 로직을 그룹핑합니다. 이 문서에서는 먼저 게이트를 살펴보고 이후 정책에 대해 설명합니다.

<!-- You do not need to choose between exclusively using gates or exclusively using policies when building an application. Most applications will most likely contain some mixture of gates and policies, and that is perfectly fine! Gates are most applicable to actions that are not related to any model or resource, such as viewing an administrator dashboard. In contrast, policies should be used when you wish to authorize an action for a particular model or resource. -->
애플리케이션을 구축할 때 반드시 게이트만 사용하거나 정책만 사용해야 하는 것은 아닙니다. 대부분의 애플리케이션은 게이트와 정책이 혼합되어 사용하는 경우가 많으며, 이는 전혀 문제가 되지 않습니다! 게이트는 주로 모델이나 리소스와 직접 관련이 없는 행동(예: 관리자 대시보드 보기 등)에 적합합니다. 반면, 정책은 특정 모델이나 리소스에 대한 행동을 인가하고자 할 때 사용합니다.

<a name="gates"></a>
<!-- ## Gates -->
## Gates

<a name="writing-gates"></a>
<!-- ### Writing Gates -->
### Writing Gates

> [!WARNING]
> 게이트는 Laravel 인가 기능의 기본을 배우기에 좋은 방법입니다. 하지만 더 견고한 Laravel 애플리케이션을 만들고자 한다면, 인가 규칙을 체계적으로 관리하기 위해 [policies](#creating-policies) 사용을 고려하시기 바랍니다.

<!-- Gates are simply closures that determine if a user is authorized to perform a given action. Typically, gates are defined within the `boot` method of the `App\Providers\AppServiceProvider` class using the `Gate` facade. Gates always receive a user instance as their first argument and may optionally receive additional arguments such as a relevant Eloquent model. -->
게이트는 사용자가 특정 행동을 수행할 수 있는지 판단하는 단순한 클로저입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 `Gate` 파사드를 사용해 정의합니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요하다면 관련 Eloquent 모델 등 추가적인 인수를 받을 수 있습니다.

<!-- In this example, we'll define a gate to determine if a user can update a given `App\Models\Post` model. The gate will accomplish this by comparing the user's `id` against the `user_id` of the user that created the post: -->
다음 예제에서는 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는지 판단하는 게이트를 정의합니다. 이 게이트는 사용자의 `id`와 게시글 작성자의 `user_id`를 비교하여 권한 여부를 정합니다:

```
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
컨트롤러처럼, 게이트도 클래스 콜백 배열 방식을 사용할 수 있습니다:

```
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
게이트를 통해 행동을 인가하려면, `Gate` 파사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용하면 됩니다. 이때, 현재 인증된 사용자를 직접 전달할 필요는 없습니다. Laravel이 자동으로 게이트 클로저에 사용자를 전달합니다. 일반적으로 컨트롤러에서 인가가 필요한 행동을 수행하기 전에 게이트 인가 메서드를 호출합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
현재 인증된 사용자가 아닌, 다른 사용자가 특정 행동을 수행할 수 있는지 확인하려면 `Gate` 파사드의 `forUser` 메서드를 사용할 수 있습니다:

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

<!-- You may authorize multiple actions at a time using the `any` or `none` methods: -->
`any` 또는 `none` 메서드를 사용하면 한 번에 여러 행동에 대해 인가를 확인할 수 있습니다:

```
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
행동에 대해 인가를 시도하고, 만약 권한이 없을 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키길 원한다면, `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException` 인스턴스는 Laravel에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

```
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
<!-- #### Supplying Additional Context -->
#### Supplying Additional Context

<!-- The gate methods for authorizing abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) and the authorization [Blade directives](#via-blade-templates) (`@can`, `@cannot`, `@canany`) can receive an array as their second argument. These array elements are passed as parameters to the gate closure, and can be used for additional context when making authorization decisions: -->
인가와 관련된 `allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot` 등 다양한 게이트 메서드와, [Blade directives](#via-blade-templates)(`@can`, `@cannot`, `@canany`)에는 두 번째 인자로 배열을 전달할 수 있습니다. 이 배열 요소들은 게이트 클로저의 매개변수로 전달되어, 인가 결정을 내릴 때 추가적인 컨텍스트로 사용할 수 있습니다:

```
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
지금까지는 게이트가 단순히 불리언 값을 반환하는 방식만 살펴보았습니다. 하지만 때로는 더 자세한 응답(에러 메시지 등)이 필요할 때가 있습니다. 이럴 경우, 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

```
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
게이트에서 인가 응답 객체를 반환하더라도, `Gate::allows` 메서드는 단순한 불리언 값을 반환합니다. 하지만, `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 인가 응답(Response)을 받아올 수 있습니다:

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

<!-- When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response: -->
`Gate::authorize` 메서드를 사용할 때, 인가에 실패하면 발생하는 `AuthorizationException`의 에러 메시지는 인가 응답에서 제공한 메시지가 HTTP 응답으로 전달됩니다:

```
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
<!-- #### Customizing The HTTP Response Status -->
#### Customizing The HTTP Response Status

<!-- When an action is denied via a Gate, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
게이트에서 행동이 거부될 경우 기본적으로 `403` HTTP 응답이 반환됩니다. 하지만 필요에 따라 다른 HTTP 상태 코드를 반환하고 싶을 때도 있습니다. 이런 경우, `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하면 인가 실패 시 반환할 HTTP 상태 코드를 지정할 수 있습니다:

```
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
웹 애플리케이션에서 자원을 숨기기 위해 `404` 응답을 반환하는 패턴이 매우 흔하므로, 이를 위한 간편한 `denyAsNotFound` 메서드도 제공됩니다:

```
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
특정 사용자에게 모든 권한을 부여하고 싶은 경우, `before` 메서드를 통해 모든 인가 검사 전에 실행되는 클로저를 정의할 수 있습니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

<!-- If the `before` closure returns a non-null result that result will be considered the result of the authorization check. -->
`before` 클로저에서 null이 아닌 값을 반환하면, 해당 값이 인가 검사 결과로 사용됩니다.

<!-- You may use the `after` method to define a closure to be executed after all other authorization checks: -->
또한, 모든 인가 검사 후에 실행할 수 있는 `after` 메서드도 정의할 수 있습니다:

```
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

<!-- Values returned by `after` closures will not override the result of the authorization check unless the gate or policy returned `null`. -->
`after` 클로저에서 반환된 값은 게이트나 정책에서 `null`이 반환된 경우에만 인가 결과를 덮어씁니다.

<a name="inline-authorization"></a>
<!-- ### Inline Authorization -->
### Inline Authorization

<!-- Occasionally, you may wish to determine if the currently authenticated user is authorized to perform a given action without writing a dedicated gate that corresponds to the action. Laravel allows you to perform these types of "inline" authorization checks via the `Gate::allowIf` and `Gate::denyIf` methods. Inline authorization does not execute any defined ["before" or "after" authorization hooks](#intercepting-gate-checks): -->
가끔은 특정 행동에 대해 전용 게이트를 미리 정의하지 않고, 현재 인증된 사용자가 그 행동을 할 수 있는지만 바로 확인하고 싶을 때가 있습니다. 이런 인라인 인가 처리는 `Gate::allowIf`와 `Gate::denyIf` 메서드를 사용해 간단히 구현할 수 있습니다. 인라인 인가 처리에서는 ["before" or "after" authorization hooks](#intercepting-gate-checks)이 실행되지 않습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

<!-- If the action is not authorized or if no user is currently authenticated, Laravel will automatically throw an `Illuminate\Auth\Access\AuthorizationException` exception. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel's exception handler. -->
만약 해당 행동에 인가되지 않았거나 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. `AuthorizationException` 인스턴스는 Laravel 예외 처리기에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
<!-- ## Creating Policies -->
## Creating Policies

<a name="generating-policies"></a>
<!-- ### Generating Policies -->
### Generating Policies

<!-- Policies are classes that organize authorization logic around a particular model or resource. For example, if your application is a blog, you may have an `App\Models\Post` model and a corresponding `App\Policies\PostPolicy` to authorize user actions such as creating or updating posts. -->
정책(Policy)은 특정 모델이나 리소스를 중심으로 인가 로직을 조직화하는 클래스입니다. 예를 들어 블로그 애플리케이션이 있다면, `App\Models\Post` 모델과 해당 모델의 인가를 담당하는 `App\Policies\PostPolicy`를 만들어, 게시글 생성이나 수정 등의 행동에 대한 인가를 처리할 수 있습니다.

<!-- You may generate a policy using the `make:policy` Artisan command. The generated policy will be placed in the `app/Policies` directory. If this directory does not exist in your application, Laravel will create it for you: -->
정책 클래스는 `make:policy` 아티즌 명령어로 생성할 수 있습니다. 생성된 정책 클래스는 `app/Policies` 디렉터리에 위치하게 되며, 해당 디렉터리가 없다면 Laravel이 자동으로 생성해 줍니다:

```shell
php artisan make:policy PostPolicy
```

<!-- The `make:policy` command will generate an empty policy class. If you would like to generate a class with example policy methods related to viewing, creating, updating, and deleting the resource, you may provide a `--model` option when executing the command: -->
`make:policy` 명령어로 생성된 클래스는 기본적으로 비어 있습니다. 리소스에 대한 보기(view), 생성(create), 수정(update), 삭제(delete) 등의 예시 정책 메서드가 포함된 클래스를 생성하려면, 명령 실행 시 `--model` 옵션을 추가하면 됩니다:

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
Laravel은 기본적으로 모델과 정책이 표준 네이밍 규칙을 따르고 있으면 정책을 자동으로 발견합니다. 구체적으로, 정책은 모델이 들어 있는 디렉터리이거나 그 상위에 위치한 `Policies` 디렉터리에 있어야 합니다. 예를 들어 모델이 `app/Models` 디렉터리에 있고 정책이 `app/Policies` 디렉터리에 있다면, Laravel은 `app/Models/Policies`를 먼저, 그다음 `app/Policies`에서 정책을 찾습니다. 또한 정책 이름은 모델 이름과 일치하고 `Policy` 접미사가 붙어야 합니다. 예를 들어 `User` 모델이라면 관련 정책 클래스는 `UserPolicy`가 됩니다.

<!-- If you would like to define your own policy discovery logic, you may register a custom policy discovery callback using the `Gate::guessPolicyNamesUsing` method. Typically, this method should be called from the `boot` method of your application's `AppServiceProvider`: -->
정책 자동 발견 로직을 직접 정의하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용해 커스텀 콜백을 등록할 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내부에서 호출합니다:

```
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
<!-- #### Manually Registering Policies -->
#### Manually Registering Policies

<!-- Using the `Gate` facade, you may manually register policies and their corresponding models within the `boot` method of your application's `AppServiceProvider`: -->
`Gate` 파사드를 사용해 `AppServiceProvider`의 `boot` 메서드에서 정책과 해당 모델을 수동으로 연결할 수도 있습니다:

```
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

<a name="writing-policies"></a>
<!-- ## Writing Policies -->
## Writing Policies

<a name="policy-methods"></a>
<!-- ### Policy Methods -->
### Policy Methods

<!-- Once the policy class has been registered, you may add methods for each action it authorizes. For example, let's define an `update` method on our `PostPolicy` which determines if a given `App\Models\User` can update a given `App\Models\Post` instance. -->
정책 클래스가 등록되면, 각 행동 별로 인가를 담당할 메서드를 추가할 수 있습니다. 예시로, `PostPolicy`에 주어진 `App\Models\User` 사용자가 특정 `App\Models\Post` 인스턴스를 수정할 수 있는지 판단하는 `update` 메서드를 정의해 보겠습니다.

<!-- The `update` method will receive a `User` and a `Post` instance as its arguments, and should return `true` or `false` indicating whether the user is authorized to update the given `Post`. So, in this example, we will verify that the user's `id` matches the `user_id` on the post: -->
`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받고, 해당 사용자가 주어진 `Post`를 수정할 권한이 있는지 나타내는 `true` 또는 `false` 값을 반환해야 합니다. 아래 예제에서는 게시글의 `user_id`와 사용자의 `id`가 일치하는지 확인합니다:

```
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
정책이 인가하는 다양한 행동에 맞춰 필요한 만큼 메서드를 추가로 정의할 수 있습니다. 예를 들어 다양한 `Post` 관련 행동을 인가하기 위해 `view`나 `delete` 메서드를 정의할 수 있으며, 정책 메서드 이름은 자유롭게 정할 수 있습니다.

<!-- If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `viewAny`, `view`, `create`, `update`, `delete`, `restore`, and `forceDelete` actions. -->
아티즌 콘솔에서 정책을 생성할 때 `--model` 옵션을 사용했다면, `viewAny`, `view`, `create`, `update`, `delete`, `restore`, `forceDelete` 행동에 대한 메서드가 이미 포함되어 생성됩니다.

> [!NOTE]
> 모든 정책은 Laravel [service container](/docs/11.x/container)를 통해 resolve되므로, 정책의 생성자에 필요에 따라 의존성을 타입힌트하면 자동으로 주입받아 사용할 수 있습니다.

<a name="policy-responses"></a>
<!-- ### Policy Responses -->
### Policy Responses

<!-- So far, we have only examined policy methods that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` instance from your policy method: -->
지금까지 살펴본 정책 메서드는 불리언을 반환하지만, 때로는 더 자세한 응답(예: 에러 메시지 등)이 필요할 수 있습니다. 이런 경우, 정책 메서드에서 `Illuminate\Auth\Access\Response` 인스턴스를 반환할 수 있습니다:

```
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
정책에서 인가 응답 객체를 반환하더라도, `Gate::allows`는 항상 단순 불리언 값을 반환합니다. 그러나 `Gate::inspect` 메서드를 사용하면 정책이 반환한 전체 인가 응답(Response)을 받아올 수 있습니다:

```
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

<!-- When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response: -->
`Gate::authorize` 메서드를 사용하면, 인가 실패 시 발생하는 `AuthorizationException` 예외에 정책에서 제공한 에러 메시지가 반영되어 HTTP 응답에 포함됩니다:

```
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
<!-- #### Customizing the HTTP Response Status -->
#### Customizing the HTTP Response Status

<!-- When an action is denied via a policy method, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
정책 메서드를 통해 행동이 거부되면 기본적으로 `403` HTTP 응답이 반환됩니다. 필요하다면, `Illuminate\Auth\Access\Response`의 `denyWithStatus` 정적 생성자를 사용해 인가 실패 시 원하는 HTTP 상태 코드를 반환할 수 있습니다:

```
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
특히, 웹 애플리케이션에서 자원을 숨기기 위해 `404` 응답을 반환하는 경우가 많으므로, 이를 손쉽게 구현할 수 있도록 `denyAsNotFound` 메서드도 제공합니다:

```
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
일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받는 경우가 있습니다. 대표적으로 `create` 행동에 대한 인가가 그러합니다. 예를 들어, 블로그에서 사용자가 게시글을 생성할 권한이 있는지 확인하고자 할 때는 정책 메서드에서 사용자 인스턴스만 받게 됩니다:

```
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
기본적으로, 인증되지 않은 사용자가 요청을 보낸 경우 모든 게이트와 정책은 자동으로 `false`를 반환합니다. 하지만, 사용자 인자에 "optional" 타입힌트나 `null` 기본값을 지정하여, 이와 같은 인가 검사가 게이트나 정책까지 통과되도록 할 수 있습니다:

```
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
일부 사용자에 대해 해당 정책의 모든 행동을 인가하고 싶을 때가 있습니다. 이럴 땐 정책 클래스에 `before` 메서드를 정의하면 됩니다. `before` 메서드는 정책의 다른 메서드 실행 전에 먼저 호출되므로, 실제 정책 메서드가 실행되기 전 행동을 인가할 기회를 가집니다. 대표적으로, 애플리케이션 관리자에게 모든 행동 권한을 부여할 때 사용합니다:

```
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
특정 유형의 사용자에 대해 모든 인가 검사를 거부하고 싶을 경우 `before` 메서드에서 `false`를 반환하면 됩니다. `null`을 반환하면 이후 실제 정책 메서드에서 인가 검사가 계속 진행됩니다.

> [!WARNING]
> 정책 클래스의 `before` 메서드는 해당 클래스에 인가하려는 행동 이름에 대응하는 메서드가 실제로 존재해야만 호출됩니다.

<a name="authorizing-actions-using-policies"></a>
<!-- ## Authorizing Actions Using Policies -->
## Authorizing Actions Using Policies

<a name="via-the-user-model"></a>
<!-- ### Via the User Model -->
### Via the User Model

<!-- The `App\Models\User` model that is included with your Laravel application includes two helpful methods for authorizing actions: `can` and `cannot`. The `can` and `cannot` methods receive the name of the action you wish to authorize and the relevant model. For example, let's determine if a user is authorized to update a given `App\Models\Post` model. Typically, this will be done within a controller method: -->
Laravel 애플리케이션에 기본 포함된 `App\Models\User` 모델에는 행동 인가를 위한 `can` 및 `cannot` 두 가지 주요 메서드가 있습니다. `can`과 `cannot` 메서드는 인가하려는 행동의 이름과 관련된 모델을 인수로 받습니다. 예를 들어, 사용자가 주어진 `App\Models\Post` 모델을 수정할 권한이 있는지 확인하려면(주로 컨트롤러 메서드에서 수행):

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
주어진 모델에 대해 [policy is registered](#registering-policies)되어 있다면, `can` 메서드는 자동으로 해당 정책을 호출하고, 그 결과에 따라 불리언 값을 반환합니다. 정책이 등록되어 있지 않다면, `can` 메서드는 해당 행동 이름과 매칭되는 클로저 기반 게이트가 존재하는지 찾아 호출하려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>

<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Remember, some actions may correspond to policy methods like `create` that do not require a model instance. In these situations, you may pass a class name to the `can` method. The class name will be used to determine which policy to use when authorizing the action: -->
일부 액션은 `create`와 같이 정책(policy) 메서드에 해당하지만, 실제로 모델 인스턴스가 필요하지 않은 경우가 있습니다. 이런 상황에서는 `can` 메서드에 클래스명을 전달할 수 있습니다. 클래스명은 어떤 정책을 사용할지 결정하는 데 활용됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
`App\Models\User` 모델에서 제공하는 여러 편리한 메서드 외에도, 항상 `Gate` 파사드의 `authorize` 메서드를 사용해 액션을 인가할 수 있습니다.

<!-- Like the `can` method, this method accepts the name of the action you wish to authorize and the relevant model. If the action is not authorized, the `authorize` method will throw an `Illuminate\Auth\Access\AuthorizationException` exception which the Laravel exception handler will automatically convert to an HTTP response with a 403 status code: -->
`can` 메서드와 마찬가지로 이 메서드는 인가하려는 액션의 이름과 관련된 모델을 전달받습니다. 만약 해당 액션이 인가되지 않은 경우, `authorize` 메서드는 `Illuminate\Auth\Access\AuthorizationException` 예외를 던집니다. Laravel의 예외 핸들러는 이 예외를 자동으로 HTTP 403 상태 코드 응답으로 변환합니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
앞서 설명했듯이, `create`와 같은 일부 정책 메서드는 모델 인스턴스를 필요로 하지 않습니다. 이럴 때는 `authorize` 메서드에 클래스명을 전달하면 됩니다. 클래스명은 어떤 정책을 사용할지 결정하는 데 사용됩니다.

```
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

<!-- Laravel includes a middleware that can authorize actions before the incoming request even reaches your routes or controllers. By default, the `Illuminate\Auth\Middleware\Authorize` middleware may be attached to a route using the `can` [middleware alias](/docs/11.x/middleware#middleware-aliases), which is automatically registered by Laravel. Let's explore an example of using the `can` middleware to authorize that a user can update a post: -->
Laravel은 요청이 라우트나 컨트롤러로 도달하기 전에 액션을 인가할 수 있는 미들웨어를 기본 제공합니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 `can` [middleware alias](/docs/11.x/middleware#middleware-aliases)을 통해 라우트에 연결할 수 있습니다. 이 별칭은 Laravel에서 자동으로 등록해줍니다. 아래는 사용자가 게시글을 수정할 권한이 있는지를 `can` 미들웨어로 인가하는 예시입니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

<!-- In this example, we're passing the `can` middleware two arguments. The first is the name of the action we wish to authorize and the second is the route parameter we wish to pass to the policy method. In this case, since we are using [implicit model binding](/docs/11.x/routing#implicit-binding), an `App\Models\Post` model will be passed to the policy method. If the user is not authorized to perform the given action, an HTTP response with a 403 status code will be returned by the middleware. -->
이 예시에서는 `can` 미들웨어에 두 개의 인수를 전달합니다. 첫 번째는 인가를 원하는 액션의 이름이고, 두 번째는 정책 메서드에 전달할 라우트 파라미터입니다. 여기서는 [implicit model binding](/docs/11.x/routing#implicit-binding)을 사용하므로, `App\Models\Post` 모델이 정책 메서드로 전달됩니다. 만약 사용자가 주어진 액션을 수행할 권한이 없다면, 미들웨어에서 HTTP 403 상태 코드 응답이 반환됩니다.

<!-- For convenience, you may also attach the `can` middleware to your route using the `can` method: -->
더욱 편리하게, `can` 미들웨어를 라우트에 붙일 때 `can` 메서드를 사용할 수도 있습니다:

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

<a name="middleware-actions-that-dont-require-models"></a>
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Again, some policy methods like `create` do not require a model instance. In these situations, you may pass a class name to the middleware. The class name will be used to determine which policy to use when authorizing the action: -->
`create`와 같은 일부 정책 메서드는 모델 인스턴스를 요구하지 않습니다. 이런 경우에는 미들웨어에 클래스명을 전달할 수 있습니다. 클래스명은 어떤 정책을 사용할지 결정하는 데 사용됩니다.

```
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

<!-- Specifying the entire class name within a string middleware definition can become cumbersome. For that reason, you may choose to attach the `can` middleware to your route using the `can` method: -->
문자열로 클래스명을 입력하여 미들웨어를 정의하는 것은 번거로울 수 있습니다. 이런 이유로, 라우트에 `can` 미들웨어를 연결할 때 `can` 메서드를 선택적으로 사용할 수 있습니다:

```
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
<!-- ### Via Blade Templates -->
### Via Blade Templates

<!-- When writing Blade templates, you may wish to display a portion of the page only if the user is authorized to perform a given action. For example, you may wish to show an update form for a blog post only if the user can actually update the post. In this situation, you may use the `@can` and `@cannot` directives: -->
Blade 템플릿을 작성할 때, 사용자가 특정 액션을 수행할 수 있을 때만 페이지의 일부 내용을 노출하고 싶을 수 있습니다. 예를 들어 사용자가 실제로 게시글을 수정할 수 있을 때만 수정 폼을 보여주고자 한다면, `@can`과 `@cannot` 디렉티브를 사용할 수 있습니다.

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
이러한 디렉티브는 `@if`와 `@unless` 문을 작성하는 것보다 더 간단하게 사용할 수 있는 편리한 단축 문법입니다. 위의 `@can`과 `@cannot` 문은 다음과 같은 문장과 동일합니다.

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

<!-- You may also determine if a user is authorized to perform any action from a given array of actions. To accomplish this, use the `@canany` directive: -->
또한, 한 사용자에게 여러 액션 중 하나라도 권한이 있는지 확인하려면 `@canany` 디렉티브를 사용할 수 있습니다:

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
다른 인가 방식들과 마찬가지로, 액션이 모델 인스턴스를 필요로 하지 않는 경우, `@can` 및 `@cannot` 디렉티브에 클래스명을 전달할 수 있습니다.

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
정책을 통해 액션 인가 시, 다양한 인가 함수와 헬퍼의 두 번째 인수에 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책을 사용할지 결정하는 데 쓰이고, 나머지는 정책 메서드에 파라미터로 전달되어 인가 판단 시 추가적인 컨텍스트로 활용됩니다. 예를 들어, 다음과 같이 `PostPolicy` 메서드가 `$category`라는 추가 인수를 받을 수 있습니다:

```
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
로그인한 사용자가 특정 게시글을 수정할 수 있는지 판단할 때, 아래와 같이 정책 메서드를 호출할 수 있습니다:

```
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
인가(authorization)는 항상 서버에서 처리해야 하지만, 경우에 따라 프론트엔드에서 인가 데이터를 활용해 사용자 인터페이스를 적절하게 렌더링하는 것이 편할 때도 있습니다. Laravel은 Inertia 기반 프론트엔드에 인가 정보를 노출하는 표준 방식을 따로 정의하지는 않습니다.

<!-- However, if you are using one of Laravel's Inertia-based [starter kits](/docs/11.x/starter-kits), your application already contains a `HandleInertiaRequests` middleware. Within this middleware's `share` method, you may return shared data that will be provided to all Inertia pages in your application. This shared data can serve as a convenient location to define authorization information for the user: -->
하지만, Laravel의 Inertia 기반 [starter kits](/docs/11.x/starter-kits)를 사용한다면 `HandleInertiaRequests` 미들웨어가 이미 내장되어 있습니다. 이 미들웨어의 `share` 메서드에서, 애플리케이션 내 모든 Inertia 페이지에 제공할 공유 데이터를 반환할 수 있습니다. 이 공유 데이터는 사용자에 대한 인가 정보를 정의하는 데 편리하게 활용할 수 있습니다.

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