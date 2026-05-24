# 認可 (Authorization)

- [Introduction](#introduction)
- [Gates](#gates)
    - [ゲートの書き込み](#writing-gates)
    - [アクションの承認](#authorizing-actions-via-gates)
    - [ゲート応答](#gate-responses)
    - [ゲートチェックの傍受](#intercepting-gate-checks)
    - [インライン認証](#inline-authorization)
- [ポリシーの作成](#creating-policies)
    - [ポリシーの生成](#generating-policies)
    - [ポリシーの登録](#registering-policies)
- [ポリシーの作成](#writing-policies)
    - [ポリシーの方法](#policy-methods)
    - [政策対応](#policy-responses)
    - [モデルのないメソッド](#methods-without-models)
    - [ゲストユーザー](#guest-users)
    - [ポリシーフィルター](#policy-filters)
- [ポリシーを使用したアクションの承認](#authorizing-actions-using-policies)
    - [ユーザーモデル経由](#via-the-user-model)
    - [門のファサード経由](#via-the-gate-facade)
    - [ミドルウェア経由](#via-middleware)
    - [Blade テンプレート経由](#via-blade-templates)
    - [追加のコンテキストの提供](#supplying-additional-context)
- [認可とInertia](#authorization-and-inertia)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、組み込みの [authentication](/docs/{{version}}/authentication) サービスを提供するだけでなく、特定のリソースに対するユーザーのアクションを承認する簡単な方法も提供します。たとえば、ユーザーが認証されていても、アプリケーションによって管理されている特定の Eloquent モデルやデータベース レコードを更新または削除する権限が与えられていない場合があります。 Laravel の認可機能は、この種の認可チェックを管理する簡単で体系的な方法を提供します。

Laravel は、アクションを承認する 2 つの主な方法、[gates](#gates) と [policies](#creating-policies) を提供します。ゲートとポリシーをルートやコントローラのように考えてください。ゲートはシンプルなクロージャベースの認可アプローチを提供し、コントローラなどのポリシーは特定のモデルまたはリソースのロジックをグループ化します。このドキュメントでは、最初にゲートを調べてから、ポリシーを調べます。

アプリケーションを構築するときに、ゲートのみを使用するかポリシーのみを使用するかを選択する必要はありません。ほとんどのアプリケーションにはゲートとポリシーが混在している可能性が高く、それはまったく問題ありません。ゲートは、管理者ダッシュボードの表示など、モデルやリソースに関連しないアクションに最も適しています。対照的に、ポリシーは、特定のモデルまたはリソースに対するアクションを承認する場合に使用する必要があります。

<a name="gates"></a>
## ゲイツ (Gates)

<a name="writing-gates"></a>
### ゲートの書き込み

> [!WARNING]
> Gates は、Laravel の認証機能の基本を学ぶのに最適な方法です。ただし、堅牢な Laravel アプリケーションを構築する場合は、[policies](#creating-policies) を使用して承認ルールを整理することを検討する必要があります。

ゲートは、ユーザーが特定のアクションを実行する権限を持っているかどうかを決定する単なるクロージャです。通常、ゲートは、`Gate` ファサードを使用して、`App\Providers\AppServiceProvider` クラスの `boot` メソッド内で定義されます。ゲートは常に最初の引数としてユーザー インスタンスを受け取り、オプションで関連する Eloquent モデルなどの追加の引数を受け取ることもあります。

この例では、ユーザーが特定の `App\Models\Post` モデルを更新できるかどうかを判断するゲートを定義します。ゲートは、ユーザーの `id` を投稿を作成したユーザーの `user_id` と比較することでこれを実現します。

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

コントローラと同様に、ゲートもクラス コールバック配列を使用して定義できます。

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
### アクションの承認

ゲートを使用してアクションを承認するには、`Gate` ファサードによって提供される `allows` メソッドまたは `denies` メソッドを使用する必要があります。現在認証されているユーザーをこれらのメソッドに渡す必要はないことに注意してください。 Laravel は、ユーザーをゲートクロージャーに渡す処理を自動的に処理します。認可が必要なアクションを実行する前に、アプリケーションのコントローラ内でゲート認可メソッドを呼び出すのが一般的です。

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

現在認証されているユーザー以外のユーザーにアクションの実行が許可されているかどうかを確認したい場合は、`Gate` ファサードで `forUser` メソッドを使用できます。

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```

`any` メソッドまたは `none` メソッドを使用して、一度に複数のアクションを承認できます。

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```

<a name="authorizing-or-throwing-exceptions"></a>
#### 例外の許可またはスロー

アクションを承認しようとして、ユーザーが指定されたアクションの実行を許可されていない場合に `Illuminate\Auth\Access\AuthorizationException` を自動的にスローしたい場合は、`Gate` ファサードの `authorize` メソッドを使用できます。 `AuthorizationException` のインスタンスは、Laravel によって 403 HTTP 応答に自動的に変換されます。

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```

<a name="gates-supplying-additional-context"></a>
#### 追加のコンテキストの提供

アビリティを認証するためのゲート メソッド (`allows`、`denies`、`check`、`any`、`none`、`authorize`、`can`、`cannot`) と認証 [Blade ディレクティブ](#via-blade-templates) (`@can`、`@cannot`、`@canany`) は、第 2 引数として配列を受け取ることができます。これらの配列要素はパラメータとしてゲート クロージャに渡され、認可の決定を行う際の追加のコンテキストとして使用できます。

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
### ゲート応答

これまでは、単純なブール値を返すゲートのみを調べてきました。ただし、エラー メッセージを含む、より詳細な応答を返したい場合もあります。そのためには、ゲートから `Illuminate\Auth\Access\Response` を返すことができます。

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

ゲートから認証応答を返した場合でも、`Gate::allows` メソッドは単純なブール値を返します。ただし、`Gate::inspect` メソッドを使用して、ゲートから返される完全な承認応答を取得することもできます。

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

アクションが承認されていない場合に `AuthorizationException` をスローする `Gate::authorize` メソッドを使用すると、承認応答によって提供されるエラー メッセージが HTTP 応答に伝播されます。

```php
Gate::authorize('edit-settings');

// The action is authorized...
```

<a name="customizing-gate-response-status"></a>
#### HTTP 応答ステータスのカスタマイズ

アクションがゲート経由で拒否されると、`403` HTTP 応答が返されます。ただし、代替の HTTP ステータス コードを返すと便利な場合もあります。 `Illuminate\Auth\Access\Response` クラスの `denyWithStatus` 静的コンストラクターを使用して、失敗した認証チェックに対して返される HTTP ステータス コードをカスタマイズできます。

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

`404` 応答によるリソースの非表示は Web アプリケーションでは一般的なパターンであるため、利便性を考慮して `denyAsNotFound` メソッドが提供されています。

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
### ゲートチェックの傍受

場合によっては、特定のユーザーにすべての権限を付与したい場合があります。 `before` メソッドを使用して、他のすべての承認チェックの前に実行されるクロージャーを定義できます。

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

`before` クロージャが null 以外の結果を返した場合、その結果は承認チェックの結果とみなされます。

`after` メソッドを使用して、他のすべての承認チェックの後に実行されるクロージャを定義できます。

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```

ゲートまたはポリシーが `null` を返さない限り、`after` クロージャによって返される値は認可チェックの結果をオーバーライドしません。

<a name="inline-authorization"></a>
### インライン認証

場合によっては、アクションに対応する専用ゲートを作成せずに、現在認証されているユーザーが特定のアクションを実行する権限を持っているかどうかを判断したい場合があります。 Laravel では、`Gate::allowIf` および `Gate::denyIf` メソッドを介して、この種の「インライン」承認チェックを実行できます。インライン認証では、定義された [認可フックの「前」または「後」](#intercepting-gate-checks) は実行されません。

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```

アクションが承認されていない場合、または現在認証されているユーザーがいない場合、Laravel は自動的に `Illuminate\Auth\Access\AuthorizationException` 例外をスローします。 `AuthorizationException` のインスタンスは、Laravel の例外ハンドラーによって 403 HTTP 応答に自動的に変換されます。

<a name="creating-policies"></a>
## ポリシーの作成 (Creating Policies)

<a name="generating-policies"></a>
### ポリシーの生成

ポリシーは、特定のモデルまたはリソースに基づいて認可ロジックを編成するクラスです。たとえば、アプリケーションがブログの場合、投稿の作成や更新などのユーザー アクションを承認するために、`App\Models\Post` モデルと対応する `App\Policies\PostPolicy` が必要になる場合があります。

`make:policy` Artisan コマンドを使用してポリシーを生成できます。生成されたポリシーは、`app/Policies` ディレクトリに配置されます。このディレクトリがアプリケーションに存在しない場合は、Laravel が作成します。

```shell
php artisan make:policy PostPolicy
```

`make:policy` コマンドは空のポリシー クラスを生成します。リソースの表示、作成、更新、削除に関連するポリシー メソッドの例を含むクラスを生成したい場合は、コマンドの実行時に `--model` オプションを指定できます。

```shell
php artisan make:policy PostPolicy --model=Post
```

<a name="registering-policies"></a>
### ポリシーの登録

<a name="policy-discovery"></a>
#### ポリシーの発見

デフォルトでは、モデルとポリシーが標準の Laravel 命名規則に従っている限り、Laravel は自動的にポリシーを検出します。具体的には、ポリシーは、モデルが含まれているディレクトリ以上の `Policies` ディレクトリに存在する必要があります。したがって、たとえば、モデルは `app/Models` ディレクトリに配置され、ポリシーは `app/Policies` ディレクトリに配置されることがあります。この状況では、Laravel は `app/Models/Policies` の次に `app/Policies` でポリシーをチェックします。さらに、ポリシー名はモデル名と一致し、`Policy` サフィックスが付いている必要があります。したがって、`User` モデルは、`UserPolicy` ポリシー クラスに対応します。

独自のポリシー検出ロジックを定義したい場合は、`Gate::guessPolicyNamesUsing` メソッドを使用してカスタム ポリシー検出コールバックを登録できます。通常、このメソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッドから呼び出す必要があります。

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```

<a name="manually-registering-policies"></a>
#### ポリシーを手動で登録する

`Gate` ファサードを使用すると、アプリケーションの `AppServiceProvider` の `boot` メソッド内でポリシーとそれに対応するモデルを手動で登録できます。

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

あるいは、モデルクラスに `UsePolicy` 属性を配置して、モデルの対応するポリシーを Laravel に通知することもできます。

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
## ポリシーの作成 (Writing Policies)

<a name="policy-methods"></a>
### ポリシーの方法

ポリシー クラスが登録されたら、それが許可するアクションごとにメソッドを追加できます。たとえば、特定の `App\Models\User` が特定の `App\Models\Post` インスタンスを更新できるかどうかを決定する `update` メソッドを `PostPolicy` に定義してみましょう。

`update` メソッドは、引数として `User` および `Post` インスタンスを受け取り、ユーザーが指定された `Post` を更新する権限があるかどうかを示す `true` または `false` を返す必要があります。したがって、この例では、ユーザーの `id` が投稿の `user_id` と一致することを確認します。

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

必要に応じて、ポリシーで承認されるさまざまなアクションに追加のメソッドを定義し続けることができます。たとえば、`view` メソッドまたは `delete` メソッドを定義して、さまざまな `Post` 関連アクションを承認できますが、ポリシー メソッドには自由に任意の名前を付けることができることに注意してください。

Artisan コンソール経由でポリシーを生成するときに `--model` オプションを使用した場合、そのオプションには、`viewAny`、`view`、`create`、`update`、`delete`、`restore`、および `forceDelete` アクションのメソッドがすでに含まれています。

> [!NOTE]
> すべてのポリシーは Laravel [サービスコンテナ](/docs/{{version}}/container) を介して解決されるため、ポリシーのコンストラクターで必要な依存関係をタイプヒントして自動的に挿入することができます。

<a name="policy-responses"></a>
### 政策対応

これまでは、単純なブール値を返すポリシー メソッドのみを調べてきました。ただし、エラー メッセージを含む、より詳細な応答を返したい場合もあります。これを行うには、ポリシー メソッドから `Illuminate\Auth\Access\Response` インスタンスを返すことができます。

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

ポリシーから認可応答を返す場合、`Gate::allows` メソッドは単純なブール値を返します。ただし、`Gate::inspect` メソッドを使用して、ゲートから返される完全な承認応答を取得することもできます。

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```

アクションが承認されていない場合に `AuthorizationException` をスローする `Gate::authorize` メソッドを使用すると、承認応答によって提供されるエラー メッセージが HTTP 応答に伝播されます。

```php
Gate::authorize('update', $post);

// The action is authorized...
```

<a name="customizing-policy-response-status"></a>
#### HTTP 応答ステータスのカスタマイズ

アクションがポリシー メソッドによって拒否された場合、`403` HTTP 応答が返されます。ただし、代替の HTTP ステータス コードを返すと便利な場合もあります。 `Illuminate\Auth\Access\Response` クラスの `denyWithStatus` 静的コンストラクターを使用して、失敗した認証チェックに対して返される HTTP ステータス コードをカスタマイズできます。

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

`404` 応答によるリソースの非表示は Web アプリケーションでは一般的なパターンであるため、利便性を考慮して `denyAsNotFound` メソッドが提供されています。

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
### モデルのないメソッド

一部のポリシー メソッドは、現在認証されているユーザーのインスタンスのみを受け取ります。この状況は、`create` アクションを承認するときに最も一般的です。たとえば、ブログを作成している場合、ユーザーに投稿を作成する権限が与えられているかどうかを確認したい場合があります。このような状況では、ポリシー メソッドはユーザー インスタンスの受信のみを期待する必要があります。

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
### ゲストユーザー

デフォルトでは、受信 HTTP リクエストが認証されたユーザーによって開始されたものでない場合、すべてのゲートとポリシーは自動的に `false` を返します。ただし、「オプション」のタイプヒントを宣言するか、ユーザー引数の定義に `null` のデフォルト値を指定することで、これらの認可チェックがゲートやポリシーを通過できるようにすることができます。

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
### ポリシーフィルター

特定のユーザーに対して、特定のポリシー内のすべてのアクションを承認したい場合があります。これを実現するには、ポリシーで `before` メソッドを定義します。 `before` メソッドは、ポリシーの他のメソッドよりも前に実行されるため、目的のポリシー メソッドが実際に呼び出される前にアクションを承認する機会が得られます。この機能は、アプリケーション管理者にアクションの実行を許可するために最も一般的に使用されます。

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

特定のタイプのユーザーに対するすべての認証チェックを拒否したい場合は、`before` メソッドから `false` を返すことができます。 `null` が返された場合、認可チェックはポリシー メソッドに渡されます。

> [!WARNING]
> チェック対象の機能の名前と一致する名前のメソッドがクラスに含まれていない場合、ポリシー クラスの `before` メソッドは呼び出されません。

<a name="authorizing-actions-using-policies"></a>
## ポリシーを使用したアクションの承認 (Authorizing Actions Using Policies)

<a name="via-the-user-model"></a>
### ユーザーモデル経由

Laravel アプリケーションに含まれる `App\Models\User` モデルには、アクションを承認するための 2 つの便利なメソッド、`can` と `cannot` が含まれています。 `can` メソッドと `cannot` メソッドは、承認するアクションの名前と関連モデルを受け取ります。たとえば、ユーザーが特定の `App\Models\Post` モデルを更新する権限を持っているかどうかを確認してみましょう。通常、これはコントローラ メソッド内で行われます。

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

指定されたモデルの [ポリシーが登録されています](#registering-policies) の場合、`can` メソッドは自動的に適切なポリシーを呼び出し、ブール値の結果を返します。モデルにポリシーが登録されていない場合、`can` メソッドは、指定されたアクション名に一致するクロージャーベースのゲートの呼び出しを試みます。

<a name="user-model-actions-that-dont-require-models"></a>
#### モデルを必要としないアクション

一部のアクションは、モデル インスタンスを必要としない `create` などのポリシー メソッドに対応する場合があることに注意してください。このような状況では、クラス名を `can` メソッドに渡すことができます。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

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
### `Gate` ファサード経由

`App\Models\User` モデルに提供される便利なメソッドに加えて、`Gate` ファサードの `authorize` メソッドを介してアクションをいつでも承認できます。

`can` メソッドと同様に、このメソッドは承認するアクションの名前と関連モデルを受け入れます。アクションが承認されていない場合、`authorize` メソッドは `Illuminate\Auth\Access\AuthorizationException` 例外をスローします。Laravel 例外ハンドラーは、この例外を 403 ステータス コードの HTTP 応答に自動的に変換します。

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
#### モデルを必要としないアクション

前に説明したように、`create` などの一部のポリシー メソッドはモデル インスタンスを必要としません。このような状況では、クラス名を `authorize` メソッドに渡す必要があります。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

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
### ミドルウェア経由

Laravel には、受信リクエストがルートやコントローラに到達する前にアクションを承認できるミドルウェアが含まれています。デフォルトでは、`Illuminate\Auth\Middleware\Authorize` ミドルウェアは、Laravel によって自動的に登録される `can` [ミドルウェアのエイリアス](/docs/{{version}}/middleware#middleware-aliases) を使用してルートに接続できます。 `can` ミドルウェアを使用して、ユーザーが投稿を更新できることを承認する例を見てみましょう。

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```

この例では、`can` ミドルウェアに 2 つの引数を渡します。 1 つ目は承認するアクションの名前で、2 つ目はポリシー メソッドに渡すルート パラメーターです。この場合、[暗黙的なモデルバインディング](/docs/{{version}}/routing#implicit-binding) を使用しているため、`App\Models\Post` モデルがポリシー メソッドに渡されます。ユーザーが指定されたアクションを実行する権限を持たない場合、ミドルウェアから 403 ステータス コードを含む HTTP 応答が返されます。

便宜上、`can` メソッドを使用して、`can` ミドルウェアをルートにアタッチすることもできます。

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```

[コントローラミドルウェアの属性](/docs/{{version}}/controllers#middleware-attributes) を使用している場合は、`Authorize` 属性を介して `can` ミドルウェアを適用できます。

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;

#[Authorize('update', 'post')]
public function update(Post $post)
{
    // The current user may update the post...
}
```

<a name="middleware-actions-that-dont-require-models"></a>
#### モデルを必要としないアクション

繰り返しますが、`create` などの一部のポリシー メソッドはモデル インスタンスを必要としません。このような状況では、クラス名をミドルウェアに渡すことができます。クラス名は、アクションを承認するときにどのポリシーを使用するかを決定するために使用されます。

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```

文字列ミドルウェア定義内でクラス名全体を指定すると、面倒になる場合があります。このため、`can` メソッドを使用して、`can` ミドルウェアをルートにアタッチすることを選択できます。

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```

<a name="via-blade-templates"></a>
### Blade テンプレート経由

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

これらのディレクティブは、`@if` および `@unless` ステートメントを作成するための便利なショートカットです。上記の `@can` ステートメントと `@cannot` ステートメントは、次のステートメントと同等です。

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```

また、ユーザーが特定のアクションの配列から任意のアクションを実行することを許可されているかどうかを判断することもできます。これを実現するには、`@canany` ディレクティブを使用します。

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```

<a name="blade-actions-that-dont-require-models"></a>
#### モデルを必要としないアクション

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
### 追加のコンテキストの提供

ポリシーを使用してアクションを承認する場合、さまざまな承認関数およびヘルパに 2 番目の引数として配列を渡すことができます。配列の最初の要素はどのポリシーを呼び出すかを決定するために使用され、配列の残りの要素はパラメータとしてポリシー メソッドに渡され、承認の決定を行う際の追加のコンテキストに使用できます。たとえば、追加の `$category` パラメータを含む次の `PostPolicy` メソッド定義を考えてみましょう。

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

認証されたユーザーが特定の投稿を更新できるかどうかを判断する場合、次のようにこのポリシー メソッドを呼び出すことができます。

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
## 認可とInertia (Authorization & Inertia)

承認は常にサーバーで処理する必要がありますが、アプリケーションの UI を適切にレンダリングするために、フロントエンド アプリケーションに承認データを提供すると便利な場合があります。 Laravel は、Inertia を利用したフロントエンドに認証情報を公開するために必要な規則を定義していません。

ただし、Laravel の Inertia ベースの [スターターキット](/docs/{{version}}/starter-kits) のいずれかを使用している場合、アプリケーションにはすでに `HandleInertiaRequests` ミドルウェアが含まれています。このミドルウェアの `share` メソッド内で、アプリケーション内のすべての Inertia ページに提供される共有データを返すことができます。この共有データは、ユーザーの認証情報を定義するための便利な場所として機能します。

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

