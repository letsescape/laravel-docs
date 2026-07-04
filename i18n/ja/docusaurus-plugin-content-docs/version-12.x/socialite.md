<!-- # Laravel Socialite -->
# Laravel Socialite

- [Introduction](#introduction)
- [Installation](#installation)
- [Upgrading Socialite](#upgrading-socialite)
- [Configuration](#configuration)
- [Authentication](#authentication)
    - [Routing](#routing)
    - [Authentication and Storage](#authentication-and-storage)
    - [Access Scopes](#access-scopes)
    - [Slack Bot Scopes](#slack-bot-scopes)
    - [Optional Parameters](#optional-parameters)
- [Retrieving User Details](#retrieving-user-details)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication via Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, and Slack. -->
一般的なフォームベースの認証に加えて、Laravel は、[Laravel Socialite](https://github.com/laravel/socialite) を使用して OAuth プロバイダで認証する簡単で便利な方法も提供します。 Socialite は現在、Facebook、X、LinkedIn、Google、GitHub、GitLab、Bitbucket、Slack による認証をサポートしています。

> [!NOTE]
> 他のプラットフォーム用のアダプターは、コミュニティ主導の [Socialite Providers](https://socialiteproviders.com/) Web サイトから入手できます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started with Socialite, use the Composer package manager to add the package to your project's dependencies: -->
Socialite の使用を開始するには、Composer パッケージ マネージャーを使用して、プロジェクトの依存関係にパッケージを追加します。

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
<!-- ## Upgrading Socialite -->
## Upgrading Socialite

<!-- When upgrading to a new major version of Socialite, it's important that you carefully review [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md). -->
Socialite の新しいメジャー バージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Socialite, you will need to add credentials for the OAuth providers your application utilizes. Typically, these credentials may be retrieved by creating a "developer application" within the dashboard of the service you will be authenticating with. -->
Socialite を使用する前に、アプリケーションが使用する OAuth プロバイダの資格情報を追加する必要があります。通常、これらの資格情報は、認証に使用するサービスのダッシュボード内に「開発者アプリケーション」を作成することによって取得できます。

<!-- These credentials should be placed in your application's `config/services.php` configuration file, and should use the key `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, or `slack-openid`, depending on the providers your application requires: -->
これらの資格情報はアプリケーションの `config/services.php` 構成ファイルに配置する必要があり、キー `facebook`、`x`、`linkedin-openid`、`google`、`github`、`gitlab`、`bitbucket`、を使用する必要があります。アプリケーションが必要とするプロバイダに応じて、`slack` または `slack-openid`:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` オプションに相対パスが含まれている場合、完全修飾 URL に自動的に解決されます。

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- To authenticate users using an OAuth provider, you will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. The example routes below demonstrate the implementation of both routes: -->
OAuth プロバイダを使用してユーザーを認証するには、2 つのルートが必要です。1 つはユーザーを OAuth プロバイダにリダイレクトするルート、もう 1 つは認証後にプロバイダからコールバックを受信するルートです。以下のルート例は、両方のルートの実装を示しています。

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

<!-- The `redirect` method provided by the `Socialite` facade takes care of redirecting the user to the OAuth provider, while the `user` method will examine the incoming request and retrieve the user's information from the provider after they have approved the authentication request. -->
`Socialite` ファサードによって提供される `redirect` メソッドは、ユーザーを OAuth プロバイダにリダイレクトします。一方、`user` メソッドは受信リクエストを検査し、認証リクエストが承認された後にプロバイダからユーザーの情報を取得します。

<a name="authentication-and-storage"></a>
<!-- ### Authentication and Storage -->
### Authentication and Storage

<!-- Once the user has been retrieved from the OAuth provider, you may determine if the user exists in your application's database and [authenticate the user](/docs/12.x/authentication#authenticate-a-user-instance). If the user does not exist in your application's database, you will typically create a new record in your database to represent the user: -->
OAuth プロバイダからユーザーを取得したら、そのユーザーがアプリケーションのデータベースと [authenticate the user](/docs/12.x/authentication#authenticate-a-user-instance) に存在するかどうかを確認できます。ユーザーがアプリケーションのデータベースに存在しない場合は、通常、ユーザーを表す新しいレコードをデータベースに作成します。

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::updateOrCreate([
        'github_id' => $githubUser->id,
    ], [
        'name' => $githubUser->name,
        'email' => $githubUser->email,
        'github_token' => $githubUser->token,
        'github_refresh_token' => $githubUser->refreshToken,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
});
```

> [!NOTE]
> 特定の OAuth プロバイダからどのようなユーザー情報が入手できるかについて詳しくは、[retrieving user details](#retrieving-user-details) のドキュメントを参照してください。

<a name="access-scopes"></a>
<!-- ### Access Scopes -->
### Access Scopes

<!-- Before redirecting the user, you may use the `scopes` method to specify the "scopes" that should be included in the authentication request. This method will merge all previously specified scopes with the scopes that you specify: -->
ユーザーをリダイレクトする前に、`scopes` メソッドを使用して、認証リクエストに含める必要がある「スコープ」を指定できます。このメソッドは、以前に指定したすべてのスコープを指定したスコープとマージします。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

<!-- You can overwrite all existing scopes on the authentication request using the `setScopes` method: -->
`setScopes` メソッドを使用して、認証リクエストの既存のスコープをすべて上書きできます。

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
<!-- ### Slack Bot Scopes -->
### Slack Bot Scopes

<!-- Slack's API provides [different types of access tokens](https://api.slack.com/authentication/token-types), each with their own set of [permission scopes](https://api.slack.com/scopes). Socialite is compatible with both of the following Slack access tokens types: -->
Slack の API は [different types of access tokens](https://api.slack.com/authentication/token-types) を提供し、それぞれに独自の [permission scopes](https://api.slack.com/scopes) セットが含まれます。 Socialite は、次の両方の Slack アクセス トークン タイプと互換性があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Bot (prefixed with `xoxb-`)
- User (prefixed with `xoxp-`)
-->
- ボット (接頭辞 `xoxb-`)
- ユーザー (接頭辞 `xoxp-`)

<!-- </div> -->
</div>

<!-- By default, the `slack` driver will generate a `user` token and invoking the driver's `user` method will return the user's details. -->
デフォルトでは、`slack` ドライバは `user` トークンを生成し、ドライバの `user` メソッドを呼び出すとユーザーの詳細が返されます。

<!-- Bot tokens are primarily useful if your application will be sending notifications to external Slack workspaces that are owned by your application's users. To generate a bot token, invoke the `asBotUser` method before redirecting the user to Slack for authentication: -->
ボット トークンは、アプリケーションのユーザーが所有する外部 Slack ワークスペースにアプリケーションが通知を送信する場合に主に役立ちます。ボット トークンを生成するには、認証のためにユーザーを Slack にリダイレクトする前に、`asBotUser` メソッドを呼び出します。

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

<!-- In addition, you must invoke the `asBotUser` method before invoking the `user` method after Slack redirects the user back to your application after authentication: -->
さらに、認証後に Slack がユーザーをアプリケーションにリダイレクトした後、`user` メソッドを呼び出す前に、`asBotUser` メソッドを呼び出す必要があります。

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

<!-- When generating a bot token, the `user` method will still return a `Laravel\Socialite\Two\User` instance; however, only the `token` property will be hydrated. This token may be stored in order to [send notifications to the authenticated user's Slack workspaces](/docs/12.x/notifications#notifying-external-slack-workspaces). -->
ボット トークンを生成する場合、`user` メソッドは引き続き `Laravel\Socialite\Two\User` インスタンスを返します。ただし、`token` プロパティのみがハイドレートされます。このトークンは、[send notifications to the authenticated user's Slack workspaces](/docs/12.x/notifications#notifying-external-slack-workspaces) に保存される場合があります。

<a name="optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- A number of OAuth providers support other optional parameters on the redirect request. To include any optional parameters in the request, call the `with` method with an associative array: -->
多くの OAuth プロバイダは、リダイレクト要求の他のオプションのパラメーターをサポートしています。リクエストにオプションのパラメーターを含めるには、連想配列を使用して `with` メソッドを呼び出します。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` メソッドを使用する場合は、`state` や `response_type` などの予約キーワードを渡さないように注意してください。

<a name="retrieving-user-details"></a>
<!-- ## Retrieving User Details -->
## Retrieving User Details

<!-- After the user is redirected back to your application's authentication callback route, you may retrieve the user's details using Socialite's `user` method. The user object returned by the `user` method provides a variety of properties and methods you may use to store information about the user in your own database. -->
ユーザーがアプリケーションの認証コールバック ルートにリダイレクトされた後、Socialite の `user` メソッドを使用してユーザーの詳細を取得できます。 `user` メソッドによって返されるユーザー オブジェクトは、ユーザーに関する情報を独自のデータベースに保存するために使用できるさまざまなプロパティとメソッドを提供します。

<!-- Differing properties and methods may be available on this object depending on whether the OAuth provider you are authenticating with supports OAuth 1.0 or OAuth 2.0: -->
認証に使用する OAuth プロバイダが OAuth 1.0 と OAuth 2.0 のどちらをサポートしているかに応じて、このオブジェクトでは異なるプロパティとメソッドを使用できる場合があります。

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 providers...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 providers...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All providers...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
<!-- #### Retrieving User Details From a Token -->
#### Retrieving User Details From a Token

<!-- If you already have a valid access token for a user, you can retrieve their user details using Socialite's `userFromToken` method: -->
ユーザーの有効なアクセス トークンをすでに持っている場合は、Socialite の `userFromToken` メソッドを使用してユーザーの詳細を取得できます。

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<!-- If you are using Facebook Limited Login via an iOS application, Facebook will return an OIDC token instead of an access token. Like an access token, the OIDC token can be provided to the `userFromToken` method in order to retrieve user details. -->
iOS アプリケーション経由で Facebook 限定ログインを使用している場合、Facebook はアクセス トークンの代わりに OIDC トークンを返します。アクセス トークンと同様に、ユーザーの詳細を取得するために、OIDC トークンを `userFromToken` メソッドに提供できます。

<a name="stateless-authentication"></a>
<!-- #### Stateless Authentication -->
#### Stateless Authentication

<!-- The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to a stateless API that does not utilize cookie based sessions: -->
`stateless` メソッドを使用して、セッション状態の検証を無効にすることができます。これは、Cookie ベースのセッションを使用しないステートレス API にソーシャル認証を追加する場合に便利です。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Laravel Socialite provides a convenient way to test OAuth authentication flows without making actual requests to OAuth providers. The `fake` method allows you to mock the OAuth provider's behavior and define the user data that should be returned. -->
Laravel Socialite は、OAuth プロバイダに実際のリクエストを行わずに OAuth 認証フローをテストする便利な方法を提供します。 `fake` メソッドを使用すると、OAuth プロバイダの動作を模擬し、返されるユーザー データを定義できます。

<a name="faking-the-redirect"></a>
<!-- #### Faking the Redirect -->
#### Faking the Redirect

<!-- To test that your application correctly redirects users to an OAuth provider, you may invoke the `fake` method before making a request to your redirect route. This will cause Socialite to return a redirect to a fake authorization URL instead of redirecting to the actual OAuth provider: -->
アプリケーションがユーザーを OAuth プロバイダに正しくリダイレ​​クトすることをテストするには、リダイレクト ルートにリクエストを行う前に `fake` メソッドを呼び出します。これにより、Socialite は実際の OAuth プロバイダにリダイレクトするのではなく、偽の認可 URL へのリダイレクトを返します。

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a name="faking-the-callback"></a>
<!-- #### Faking the Callback -->
#### Faking the Callback

<!-- To test your application's callback route, you may invoke the `fake` method and provide a `User` instance that should be returned when your application requests the user's details from the provider. The `User` instance may be created using the `map` method: -->
アプリケーションのコールバック ルートをテストするには、`fake` メソッドを呼び出し、アプリケーションがプロバイダにユーザーの詳細を要求したときに返される `User` インスタンスを指定します。 `User` インスタンスは、`map` メソッドを使用して作成できます。

```php
use Laravel\Socialite\Socialite;
use Laravel\Socialite\Two\User;

test('user can login with github', function () {
    Socialite::fake('github', (new User)->map([
        'id' => 'github-123',
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
    ]));

    $response = $this->get('/auth/github/callback');

    $response->assertRedirect('/dashboard');

    $this->assertDatabaseHas('users', [
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
        'github_id' => 'github-123',
    ]);
});
```

<!-- By default, the `User` instance will also include a `token` property. If needed, you may manually specify additional properties on the `User` instance: -->
デフォルトでは、`User` インスタンスには `token` プロパティも含まれます。必要に応じて、`User` インスタンスに追加のプロパティを手動で指定できます。

```php
$fakeUser = (new User)->map([
    'id' => 'github-123',
    'name' => 'Jason Beggs',
    'email' => 'jason@example.com',
])->setToken('fake-token')
  ->setRefreshToken('fake-refresh-token')
  ->setExpiresIn(3600)
  ->setApprovedScopes(['read', 'write'])
```

