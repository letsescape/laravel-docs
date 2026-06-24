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
Laravel は、組み込みの [authentication](/docs/11.x/authentication) サービスを提供するだけでなく、特定のリソースに対するユーザーのアクションを承認する簡単な方法も提供します。たとえば、ユーザーが認証されていても、アプリケーションによって管理されている特定の Eloquent モデルやデータベース レコードを更新または削除する権限が与えられていない場合があります。 Laravel の認可機能は、この種の認可チェックを管理する簡単で体系的な方法を提供します。

<!-- Laravel provides two primary ways of authorizing actions: [gates](#gates) and [policies](#creating-policies). Think of gates and policies like routes and controllers. Gates provide a simple, closure-based approach to authorization while policies, like controllers, group logic around a particular model or resource. In this documentation, we'll explore gates first and then examine policies. -->
Laravel は、アクションを承認する 2 つの主な方法、[gates](#gates) と [policies](#creating-policies) を提供します。ゲートとポリシーをルートやコントローラのように考えてください。ゲートはシンプルなクロージャベースの認可アプローチを提供し、コントローラなどのポリシーは特定のモデルまたはリソースのロジックをグループ化します。このドキュメントでは、最初にゲートを調べてから、ポリシーを調べます。

<!-- You do not need to choose between exclusively using gates or exclusively using policies when building an application. Most applications will most likely contain some mixture of gates and policies, and that is perfectly fine! Gates are most applicable to actions that are not related to any model or resource, such as viewing an administrator dashboard. In contrast, policies should be used when you wish to authorize an action for a particular model or resource. -->
アプリケーションを構築するときに、ゲートのみを使用するかポリシーのみを使用するかを選択する必要はありません。ほとんどのアプリケーションにはゲートとポリシーが混在している可能性が高く、それはまったく問題ありません。ゲートは、管理者ダッシュボードの表示など、モデルやリソースに関連しないアクションに最も適しています。対照的に、ポリシーは、特定のモデルまたはリソースに対するアクションを承認する場合に使用する必要があります。

<a name="gates"></a>
<!-- ## Gates -->
## Gates

<a name="writing-gates"></a>
<!-- ### Writing Gates -->
### Writing Gates

> [!WARNING]
> Gates は、Laravel の認証機能の基本を学ぶのに最適な方法です。ただし、堅牢な Laravel アプリケーションを構築する場合は、[policies](#creating-policies) を使用して承認ルールを整理することを検討する必要があります。

<!-- Gates are simply closures that determine if a user is authorized to perform a given action. Typically, gates are defined within the `boot` method of the `App\Providers\AppServiceProvider` class using the `Gate` facade. Gates always receive a user instance as their first argument and may optionally receive additional arguments such as a relevant Eloquent model. -->
ゲートは、ユーザーが特定のアクションを実行する権限を持っているかどうかを決定する単なるクロージャです。通常、ゲートは、`Gate` ファサードを使用して、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内で定義されます。ゲートは常に最初の引数としてユーザー インスタンスを受け取り、オプションで関連する Eloquent モデルなどの追加の引数を受け取ることもあります。

<!-- In this example, we'll define a gate to determine if a user can update a given `App\Models\Post` model. The gate will accomplish this by comparing the user's `id` against the `user_id` of the user that created the post: -->
この例では、ユーザーが特定の `App\Models\Post` モデルを更新できるかどうかを判断するゲートを定義します。ゲートは、ユーザーの `id` を投稿を作成したユーザーの `user_id` と比較することでこれを実現します。

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
コントローラと同様に、ゲートもクラス コールバック配列を使用して定義できます。

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
ゲートを使用してアクションを承認するには、`Gate` ファサードによって提供される `allows` メソッドまたは `denies` メソッドを使用する必要があります。現在認証されているユーザーをこれらのメソッドに渡す必要はないことに注意してください。 Laravel は、ユーザーをゲートクロージャーに渡す処理を自動的に処理します。認可が必要なアクションを実行する前に、アプリケーションのコントローラ内でゲート認可メソッドを呼び出すのが一般的です。

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
現在認証されているユーザー以外のユーザーにアクションの実行が許可されているかどうかを確認したい場合は、`Gate` ファサードで `forUser` メソッドを使用できます。

```
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

<!-- You may authorize multiple actions at a time using the `any` or `none` methods: -->
`any` メソッドまたは `none` メソッドを使用して、一度に複数のアクションを承認できます。

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
アクションを承認しようとして、ユーザーが指定されたアクションの実行を許可されていない場合に `Illuminate\Auth\Access\AuthorizationException` を自動的にスローしたい場合は、`Gate` ファサードの `authorize` メソッドを使用できます。 `AuthorizationException` のインスタンスは、Laravel によって 403 HTTP 応答に自動的に変換されます。

```
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
<!-- #### Supplying Additional Context -->
#### Supplying Additional Context

<!-- The gate methods for authorizing abilities (`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`) and the authorization [Blade directives](#via-blade-templates) (`@can`, `@cannot`, `@canany`) can receive an array as their second argument. These array elements are passed as parameters to the gate closure, and can be used for additional context when making authorization decisions: -->
アビリティを認証するためのゲート メソッド (`allows`、`denies`、`check`、`any`、`none`、`authorize`、`can`、`cannot`) と認証 [Blade directives](#via-blade-templates) (`@can`、`@cannot`、`@canany`) は、第 2 引数として配列を受け取ることができます。これらの配列要素はパラメータとしてゲート クロージャに渡され、認可の決定を行う際の追加のコンテキストとして使用できます。

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
これまでは、単純なブール値を返すゲートのみを調べてきました。ただし、エラー メッセージを含む、より詳細な応答を返したい場合もあります。そのためには、ゲートから `Illuminate\Auth\Access\Response` を返すことができます。

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
ゲートから認証応答を返した場合でも、`Gate::allows` メソッドは単純なブール値を返します。ただし、`Gate::inspect` メソッドを使用して、ゲートから返される完全な承認応答を取得することもできます。

```
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

<!-- When using the `Gate::authorize` method, which throws an `AuthorizationException` if the action is not authorized, the error message provided by the authorization response will be propagated to the HTTP response: -->
アクションが承認されていない場合に `AuthorizationException` をスローする `Gate::authorize` メソッドを使用すると、承認応答によって提供されるエラー メッセージが HTTP 応答に伝播されます。

```
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
<!-- #### Customizing The HTTP Response Status -->
#### Customizing The HTTP Response Status

<!-- When an action is denied via a Gate, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
アクションがゲート経由で拒否されると、`403` HTTP 応答が返されます。ただし、代替の HTTP ステータス コードを返すと便利な場合もあります。 `Illuminate\Auth\Access\Response` クラスの `denyWithStatus` 静的コンストラクターを使用して、失敗した認証チェックに対して返される HTTP ステータス コードをカスタマイズできます。

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
`404` 応答によるリソースの非表示は Web アプリケーションでは一般的なパターンであるため、利便性を考慮して `denyAsNotFound` メソッドが提供されています。

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
場合によっては、特定のユーザーにすべての権限を付与したい場合があります。 `before` メソッドを使用して、他のすべての承認チェックの前に実行されるクロージャーを定義できます。

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
`before` クロージャが null 以外の結果を返した場合、その結果は承認チェックの結果とみなされます。

<!-- You may use the `after` method to define a closure to be executed after all other authorization checks: -->
`after` メソッドを使用して、他のすべての承認チェックの後に実行されるクロージャを定義できます。

```
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

<!-- Values returned by `after` closures will not override the result of the authorization check unless the gate or policy returned `null`. -->
ゲートまたはポリシーが `null` を返さない限り、`after` クロージャによって返される値は認可チェックの結果をオーバーライドしません。

<a name="inline-authorization"></a>
<!-- ### Inline Authorization -->
### Inline Authorization

<!-- Occasionally, you may wish to determine if the currently authenticated user is authorized to perform a given action without writing a dedicated gate that corresponds to the action. Laravel allows you to perform these types of "inline" authorization checks via the `Gate::allowIf` and `Gate::denyIf` methods. Inline authorization does not execute any defined ["before" or "after" authorization hooks](#intercepting-gate-checks): -->
場合によっては、アクションに対応する専用ゲートを作成せずに、現在認証されているユーザーが特定のアクションを実行する権限を持っているかどうかを判断したい場合があります。 Laravel では、`Gate::allowIf` および `Gate::denyIf` メソッドを介して、この種の「インライン」承認チェックを実行できます。インライン認証では、定義された ["before" or "after" authorization hooks](#intercepting-gate-checks) は実行されません。

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

<!-- If the action is not authorized or if no user is currently authenticated, Laravel will automatically throw an `Illuminate\Auth\Access\AuthorizationException` exception. Instances of `AuthorizationException` are automatically converted to a 403 HTTP response by Laravel's exception handler. -->
アクションが承認されていない場合、または現在認証されているユーザーがいない場合、Laravel は自動的に `Illuminate\Auth\Access\AuthorizationException` 例外をスローします。 `AuthorizationException` のインスタンスは、Laravel の例外ハンドラーによって 403 HTTP 応答に自動的に変換されます。

<a name="creating-policies"></a>
<!-- ## Creating Policies -->
## Creating Policies

<a name="generating-policies"></a>
<!-- ### Generating Policies -->
### Generating Policies

<!-- Policies are classes that organize authorization logic around a particular model or resource. For example, if your application is a blog, you may have an `App\Models\Post` model and a corresponding `App\Policies\PostPolicy` to authorize user actions such as creating or updating posts. -->
ポリシーは、特定のモデルまたはリソースに基づいて認可ロジックを編成するクラスです。たとえば、アプリケーションがブログの場合、投稿の作成や更新などのユーザー アクションを承認するために、`App\Models\Post` モデルと対応する `App\Policies\PostPolicy` が必要になる場合があります。

<!-- You may generate a policy using the `make:policy` Artisan command. The generated policy will be placed in the `app/Policies` directory. If this directory does not exist in your application, Laravel will create it for you: -->
`make:policy` Artisan コマンドを使用してポリシーを生成できます。生成されたポリシーは、`app/Policies` ディレクトリに配置されます。このディレクトリがアプリケーションに存在しない場合は、Laravel が作成します。

```shell
php artisan make:policy PostPolicy
```

<!-- The `make:policy` command will generate an empty policy class. If you would like to generate a class with example policy methods related to viewing, creating, updating, and deleting the resource, you may provide a `--model` option when executing the command: -->
`make:policy` コマンドは空のポリシー クラスを生成します。リソースの表示、作成、更新、削除に関連するポリシー メソッドの例を含むクラスを生成したい場合は、コマンドの実行時に `--model` オプションを指定できます。

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
デフォルトでは、モデルとポリシーが標準の Laravel 命名規則に従っている限り、Laravel は自動的にポリシーを検出します。具体的には、ポリシーは、モデルが含まれているディレクトリ以上の `Policies` ディレクトリに存在する必要があります。したがって、たとえば、モデルは `app/Models` ディレクトリに配置され、ポリシーは `app/Policies` ディレクトリに配置されることがあります。この状況では、Laravel は `app/Models/Policies` の次に `app/Policies` でポリシーをチェックします。さらに、ポリシー名はモデル名と一致し、`Policy` サフィックスが付いている必要があります。したがって、`User` モデルは、`UserPolicy` ポリシー クラスに対応します。

<!-- If you would like to define your own policy discovery logic, you may register a custom policy discovery callback using the `Gate::guessPolicyNamesUsing` method. Typically, this method should be called from the `boot` method of your application's `AppServiceProvider`: -->
独自のポリシー検出ロジックを定義したい場合は、`Gate::guessPolicyNamesUsing` メソッドを使用してカスタム ポリシー検出コールバックを登録できます。通常、このメソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッドから呼び出す必要があります。

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
`Gate` ファサードを使用すると、アプリケーションの `AppServiceProvider` の `boot` メソッド内でポリシーとそれに対応するモデルを手動で登録できます。

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
ポリシー クラスが登録されたら、それが許可するアクションごとにメソッドを追加できます。たとえば、特定の `App\Models\User` が特定の `App\Models\Post` インスタンスを更新できるかどうかを決定する `update` メソッドを `PostPolicy` に定義してみましょう。

<!-- The `update` method will receive a `User` and a `Post` instance as its arguments, and should return `true` or `false` indicating whether the user is authorized to update the given `Post`. So, in this example, we will verify that the user's `id` matches the `user_id` on the post: -->
`update` メソッドは、引数として `User` および `Post` インスタンスを受け取り、ユーザーが指定された `Post` を更新する権限があるかどうかを示す `true` または `false` を返す必要があります。したがって、この例では、ユーザーの `id` が投稿の `user_id` と一致することを確認します。

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
必要に応じて、ポリシーで承認されるさまざまなアクションに追加のメソッドを定義し続けることができます。たとえば、`view` メソッドまたは `delete` メソッドを定義して、さまざまな `Post` 関連アクションを承認できますが、ポリシー メソッドには自由に任意の名前を付けることができることに注意してください。

<!-- If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `viewAny`, `view`, `create`, `update`, `delete`, `restore`, and `forceDelete` actions. -->
Artisan コンソール経由でポリシーを生成するときに `--model` オプションを使用した場合、そのオプションには、`viewAny`、`view`、`create`、`update`、`delete`、`restore`、および `forceDelete` アクションのメソッドがすでに含まれています。

> [!NOTE]
> すべてのポリシーは Laravel [service container](/docs/11.x/container) を介して解決されるため、ポリシーのコンストラクターで必要な依存関係をタイプヒントして自動的に挿入することができます。

<a name="policy-responses"></a>
<!-- ### Policy Responses -->
### Policy Responses

<!-- So far, we have only examined policy methods that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` instance from your policy method: -->
これまでは、単純なブール値を返すポリシー メソッドのみを調べてきました。ただし、エラー メッセージを含む、より詳細な応答を返したい場合もあります。これを行うには、ポリシー メソッドから `Illuminate\Auth\Access\Response` インスタンスを返すことができます。

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
ポリシーから認可応答を返す場合、`Gate::allows` メソッドは単純なブール値を返します。ただし、`Gate::inspect` メソッドを使用して、ゲートから返される完全な承認応答を取得することもできます。

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
アクションが承認されていない場合に `AuthorizationException` をスローする `Gate::authorize` メソッドを使用すると、承認応答によって提供されるエラー メッセージが HTTP 応答に伝播されます。

```
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
<!-- #### Customizing the HTTP Response Status -->
#### Customizing the HTTP Response Status

<!-- When an action is denied via a policy method, a `403` HTTP response is returned; however, it can sometimes be useful to return an alternative HTTP status code. You may customize the HTTP status code returned for a failed authorization check using the `denyWithStatus` static constructor on the `Illuminate\Auth\Access\Response` class: -->
アクションがポリシー メソッドによって拒否された場合、`403` HTTP 応答が返されます。ただし、代替の HTTP ステータス コードを返すと便利な場合もあります。 `Illuminate\Auth\Access\Response` クラスの `denyWithStatus` 静的コンストラクターを使用して、失敗した認証チェックに対して返される HTTP ステータス コードをカスタマイズできます。

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
`404` 応答によるリソースの非表示は Web アプリケーションでは一般的なパターンであるため、利便性を考慮して `denyAsNotFound` メソッドが提供されています。

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
一部のポリシー メソッドは、現在認証されているユーザーのインスタンスのみを受け取ります。この状況は、`create` アクションを承認するときに最も一般的です。たとえば、ブログを作成している場合、ユーザーに投稿を作成する権限が与えられているかどうかを確認したい場合があります。このような状況では、ポリシー メソッドはユーザー インスタンスの受信のみを期待する必要があります。

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
デフォルトでは、受信 HTTP リクエストが認証されたユーザーによって開始されたものでない場合、すべてのゲートとポリシーは自動的に `false` を返します。ただし、「オプション」のタイプヒントを宣言するか、ユーザー引数の定義に `null` のデフォルト値を指定することで、これらの認可チェックがゲートやポリシーを通過できるようにすることができます。

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
特定のユーザーに対して、特定のポリシー内のすべてのアクションを承認したい場合があります。これを実現するには、ポリシーで `before` メソッドを定義します。 `before` メソッドは、ポリシーの他のメソッドよりも前に実行されるため、目的のポリシー メソッドが実際に呼び出される前にアクションを承認する機会が得られます。この機能は、アプリケーション管理者にアクションの実行を許可するために最も一般的に使用されます。

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
特定のタイプのユーザーに対するすべての認証チェックを拒否したい場合は、`before` メソッドから `false` を返すことができます。 `null` が返された場合、認可チェックはポリシー メソッドに渡されます。

> [!WARNING]
> チェック対象の機能の名前と一致する名前のメソッドがクラスに含まれていない場合、ポリシー クラスの `before` メソッドは呼び出されません。

<a name="authorizing-actions-using-policies"></a>
<!-- ## Authorizing Actions Using Policies -->
## Authorizing Actions Using Policies

<a name="via-the-user-model"></a>
<!-- ### Via the User Model -->
### Via the User Model

<!-- The `App\Models\User` model that is included with your Laravel application includes two helpful methods for authorizing actions: `can` and `cannot`. The `can` and `cannot` methods receive the name of the action you wish to authorize and the relevant model. For example, let's determine if a user is authorized to update a given `App\Models\Post` model. Typically, this will be done within a controller method: -->
Laravel アプリケーションに含まれる `App\Models\User` モデルには、アクションを承認するための 2 つの便利なメソッド、`can` と `cannot` が含まれています。 `can` メソッドと `cannot` メソッドは、承認するアクションの名前と関連モデルを受け取ります。たとえば、ユーザーが特定の `App\Models\Post` モデルを更新する権限を持っているかどうかを確認してみましょう。通常、これはコントローラ メソッド内で行われます。

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
指定されたモデルの [policy is registered](#registering-policies) の場合、`can` メソッドは自動的に適切なポリシーを呼び出し、ブール値の結果を返します。モデルにポリシーが登録されていない場合、`can` メソッドは、指定されたアクション名に一致するクロージャーベースのゲートの呼び出しを試みます。

<a name="user-model-actions-that-dont-require-models"></a>
<!-- #### Actions That Don't Require Models -->
#### Actions That Don't Require Models

<!-- Remember, some actions may correspond to policy methods like `create` that do not require a model instance. In these situations, you may pass a class name to the `can` method. The class name will be used to determine which policy to use when authorizing the action: -->
一部のアクションは、モデル インスタンスを必要としない `create` などのポリシー メソッドに対応する場合があることに注意してください。このような状況では、クラス名を `can` メソッドに渡すことができます。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

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
`App\Models\User` モデルに提供される便利なメソッドに加えて、`Gate` ファサードの `authorize` メソッドを介してアクションをいつでも承認できます。

<!-- Like the `can` method, this method accepts the name of the action you wish to authorize and the relevant model. If the action is not authorized, the `authorize` method will throw an `Illuminate\Auth\Access\AuthorizationException` exception which the Laravel exception handler will automatically convert to an HTTP response with a 403 status code: -->
`can` メソッドと同様に、このメソッドは承認するアクションの名前と関連モデルを受け入れます。アクションが承認されていない場合、`authorize` メソッドは `Illuminate\Auth\Access\AuthorizationException` 例外をスローします。Laravel 例外ハンドラーは、この例外を 403 ステータス コードの HTTP 応答に自動的に変換します。

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
前に説明したように、`create` などの一部のポリシー メソッドはモデル インスタンスを必要としません。このような状況では、クラス名を `authorize` メソッドに渡す必要があります。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

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
Laravel には、受信リクエストがルートやコントローラに到達する前にアクションを承認できるミドルウェアが含まれています。デフォルトでは、`Illuminate\Auth\Middleware\Authorize` ミドルウェアは、Laravel によって自動的に登録される `can` [middleware alias](/docs/11.x/middleware#middleware-aliases) を使用してルートに接続できます。 `can` ミドルウェアを使用して、ユーザーが投稿を更新できることを承認する例を見てみましょう。

```
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

<!-- In this example, we're passing the `can` middleware two arguments. The first is the name of the action we wish to authorize and the second is the route parameter we wish to pass to the policy method. In this case, since we are using [implicit model binding](/docs/11.x/routing#implicit-binding), an `App\Models\Post` model will be passed to the policy method. If the user is not authorized to perform the given action, an HTTP response with a 403 status code will be returned by the middleware. -->
この例では、`can` ミドルウェアに 2 つの引数を渡します。 1 つ目は承認するアクションの名前で、2 つ目はポリシー メソッドに渡すルート パラメーターです。この場合、[implicit model binding](/docs/11.x/routing#implicit-binding) を使用しているため、`App\Models\Post` モデルがポリシー メソッドに渡されます。ユーザーが指定されたアクションを実行する権限を持たない場合、ミドルウェアから 403 ステータス コードを含む HTTP 応答が返されます。

<!-- For convenience, you may also attach the `can` middleware to your route using the `can` method: -->
便宜上、`can` メソッドを使用して、`can` ミドルウェアをルートにアタッチすることもできます。

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
繰り返しますが、`create` などの一部のポリシー メソッドはモデル インスタンスを必要としません。このような状況では、クラス名をミドルウェアに渡すことができます。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

```
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

<!-- Specifying the entire class name within a string middleware definition can become cumbersome. For that reason, you may choose to attach the `can` middleware to your route using the `can` method: -->
文字列ミドルウェア定義内でクラス名全体を指定すると、面倒になる場合があります。このため、`can` メソッドを使用して、`can` ミドルウェアをルートにアタッチすることを選択できます。

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
Blade テンプレートを作成するとき、ユーザーが特定のアクションの実行を許可されている場合にのみページの一部を表示したい場合があります。たとえば、ユーザーが実際に投稿を更新できる場合にのみ、ブログ投稿の更新フォームを表示したい場合があります。この状況では、`@can` および `@cannot` ディレクティブを使用できます。

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
これらのディレクティブは、`@if` および `@unless` ステートメントを作成するための便利なショートカットです。上記の `@can` ステートメントと `@cannot` ステートメントは、次のステートメントと同等です。

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

<!-- You may also determine if a user is authorized to perform any action from a given array of actions. To accomplish this, use the `@canany` directive: -->
また、ユーザーが特定のアクションの配列から任意のアクションを実行することを許可されているかどうかを判断することもできます。これを実現するには、`@canany` ディレクティブを使用します。

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
他のほとんどの認証メソッドと同様に、アクションにモデル インスタンスが必要ない場合は、クラス名を `@can` および `@cannot` ディレクティブに渡すことができます。

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
ポリシーを使用してアクションを承認する場合、さまざまな承認関数およびヘルパに 2 番目の引数として配列を渡すことができます。配列の最初の要素はどのポリシーを呼び出すかを決定するために使用され、配列の残りの要素はパラメータとしてポリシー メソッドに渡され、承認の決定を行う際の追加のコンテキストに使用できます。たとえば、追加の `$category` パラメータを含む次の `PostPolicy` メソッド定義を考えてみましょう。

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
認証されたユーザーが特定の投稿を更新できるかどうかを判断する場合、次のようにこのポリシー メソッドを呼び出すことができます。

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
承認は常にサーバーで処理する必要がありますが、アプリケーションの UI を適切にレンダリングするために、フロントエンド アプリケーションに承認データを提供すると便利な場合があります。 Laravel は、Inertia を利用したフロントエンドに認証情報を公開するために必要な規則を定義していません。

<!-- However, if you are using one of Laravel's Inertia-based [starter kits](/docs/11.x/starter-kits), your application already contains a `HandleInertiaRequests` middleware. Within this middleware's `share` method, you may return shared data that will be provided to all Inertia pages in your application. This shared data can serve as a convenient location to define authorization information for the user: -->
ただし、Laravel の Inertia ベースの [starter kits](/docs/11.x/starter-kits) のいずれかを使用している場合、アプリケーションにはすでに `HandleInertiaRequests` ミドルウェアが含まれています。このミドルウェアの `share` メソッド内で、アプリケーション内のすべての Inertia ページに提供される共有データを返すことができます。この共有データは、ユーザーの認証情報を定義するための便利な場所として機能します。

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

