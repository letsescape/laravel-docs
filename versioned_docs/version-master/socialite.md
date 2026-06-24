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
일반적인 폼 기반 인증 외에도 Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용해 OAuth provider로 간편하게 인증할 수 있는 방법을 제공합니다. Socialite는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티가 주도하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started with Socialite, use the Composer package manager to add the package to your project's dependencies: -->
Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 해당 패키지를 프로젝트의 의존성에 추가합니다.

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
<!-- ## Upgrading Socialite -->
## Upgrading Socialite

<!-- When upgrading to a new major version of Socialite, it's important that you carefully review [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md). -->
Socialite의 새로운 주요 버전으로 업그레이드할 때에는 [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 반드시 꼼꼼히 검토해야 합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Socialite, you will need to add credentials for the OAuth providers your application utilizes. Typically, these credentials may be retrieved by creating a "developer application" within the dashboard of the service you will be authenticating with. -->
Socialite를 사용하기 전에 애플리케이션에서 사용할 OAuth provider의 인증 정보를 추가해야 합니다. 일반적으로 이 정보는 해당 서비스의 대시보드에서 "개발자 애플리케이션"을 생성해 얻을 수 있습니다.

<!-- These credentials should be placed in your application's `config/services.php` configuration file, and should use the key `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, or `slack-openid`, depending on the providers your application requires: -->
이 인증 정보는 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용할 provider에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid` 같은 키를 사용합니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 들어갈 경우, 자동으로 완전한 형태의 URL로 변환됩니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- To authenticate users using an OAuth provider, you will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. The example routes below demonstrate the implementation of both routes: -->
OAuth provider로 사용자를 인증하려면, 하나는 사용자를 OAuth provider로 리다이렉트하는 라우트와 하나는 인증이 끝난 뒤 provider에서 콜백을 받는 라우트가 필요합니다. 아래 예시는 두 라우트의 구현 예시입니다.

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
`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth provider로 리다이렉트하고, `user` 메서드는 콜백 요청을 분석해 인증이 승인된 뒤 provider에서 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
<!-- ### Authentication and Storage -->
### Authentication and Storage

<!-- Once the user has been retrieved from the OAuth provider, you may determine if the user exists in your application's database and [authenticate the user](/docs/master/authentication#authenticate-a-user-instance). If the user does not exist in your application's database, you will typically create a new record in your database to represent the user: -->
OAuth provider에서 사용자 정보를 받아오면, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인한 뒤 [authenticate the user](/docs/master/authentication#authenticate-a-user-instance)을 진행할 수 있습니다. 데이터베이스에 사용자가 없다면 일반적으로 새 사용자 레코드를 생성하게 됩니다.

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
> 각 OAuth provider에서 어떤 사용자 정보를 받을 수 있는지 더 알아보려면 [retrieving user details](#retrieving-user-details) 섹션을 참고하세요.

<a name="access-scopes"></a>
<!-- ### Access Scopes -->
### Access Scopes

<!-- Before redirecting the user, you may use the `scopes` method to specify the "scopes" that should be included in the authentication request. This method will merge all previously specified scopes with the scopes that you specify: -->
사용자를 리다이렉트하기 전에, `scopes` 메서드를 사용하여 인증 요청에 포함시킬 "범위(scope)"를 지정할 수 있습니다. 이 메서드는 이미 지정된 범위에 새 범위를 추가하여 병합합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

<!-- You can overwrite all existing scopes on the authentication request using the `setScopes` method: -->
인증 요청에서 기존의 모든 범위를 새 범위로 덮어쓰려면 `setScopes` 메서드를 사용할 수 있습니다.

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
<!-- ### Slack Bot Scopes -->
### Slack Bot Scopes

<!-- Slack's API provides [different types of access tokens](https://api.slack.com/authentication/token-types), each with their own set of [permission scopes](https://api.slack.com/scopes). Socialite is compatible with both of the following Slack access tokens types: -->
Slack의 API는 [different types of access tokens](https://api.slack.com/authentication/token-types)과 각각의 [permission scopes](https://api.slack.com/scopes)를 제공합니다. Socialite는 아래 두 가지 Slack 액세스 토큰 유형 모두와 호환됩니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Bot (prefixed with `xoxb-`)
- User (prefixed with `xoxp-`)
-->
- Bot(봇, `xoxb-` 접두사)
- User(사용자, `xoxp-` 접두사)

<!-- </div> -->
</div>

<!-- By default, the `slack` driver will generate a `user` token and invoking the driver's `user` method will return the user's details. -->
기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자 정보를 반환합니다.

<!-- Bot tokens are primarily useful if your application will be sending notifications to external Slack workspaces that are owned by your application's users. To generate a bot token, invoke the `asBotUser` method before redirecting the user to Slack for authentication: -->
봇 토큰은 애플리케이션을 사용하는 사용자가 소유한 외부 Slack 워크스페이스에 알림을 보내야 할 경우에 주로 활용됩니다. 봇 토큰을 생성하려면, 사용자를 Slack 인증으로 리다이렉트하기 전에 `asBotUser` 메서드를 호출하면 됩니다.

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

<!-- In addition, you must invoke the `asBotUser` method before invoking the `user` method after Slack redirects the user back to your application after authentication: -->
또한, 인증 후 Slack이 사용자를 다시 애플리케이션으로 리다이렉트한 후에 `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 호출해야 합니다.

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

<!-- When generating a bot token, the `user` method will still return a `Laravel\Socialite\Two\User` instance; however, only the `token` property will be hydrated. This token may be stored in order to [send notifications to the authenticated user's Slack workspaces](/docs/master/notifications#notifying-external-slack-workspaces). -->
봇 토큰을 생성할 때도 `user` 메서드는 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 이때는 오직 `token` 속성만 채워져 있습니다. 이 토큰은 [send notifications to the authenticated user's Slack workspaces](/docs/master/notifications#notifying-external-slack-workspaces)에 활용할 수 있도록 저장해둘 수 있습니다.

<a name="optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- A number of OAuth providers support other optional parameters on the redirect request. To include any optional parameters in the request, call the `with` method with an associative array: -->
여러 OAuth provider는 리다이렉트 요청에서 추가 선택 파라미터를 지원합니다. 이러한 파라미터를 요청에 포함하려면 연관 배열 형태로 `with` 메서드를 호출하면 됩니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state`, `response_type`과 같은 예약어는 전달하지 않도록 주의해야 합니다.

<a name="retrieving-user-details"></a>
<!-- ## Retrieving User Details -->
## Retrieving User Details

<!-- After the user is redirected back to your application's authentication callback route, you may retrieve the user's details using Socialite's `user` method. The user object returned by the `user` method provides a variety of properties and methods you may use to store information about the user in your own database. -->
사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 이후에 Socialite의 `user` 메서드를 사용하여 사용자 정보를 조회할 수 있습니다. `user` 메서드로 반환되는 사용자 객체는 다양한 속성과 메서드를 제공하므로, 이를 사용해 사용자의 정보를 데이터베이스에 저장할 수 있습니다.

<!-- Differing properties and methods may be available on this object depending on whether the OAuth provider you are authenticating with supports OAuth 1.0 or OAuth 2.0: -->
OAuth 1.0 또는 OAuth 2.0 지원 여부에 따라 해당 객체에서 사용할 수 있는 속성과 메서드가 다를 수 있습니다.

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
이미 해당 사용자의 유효한 액세스 토큰을 가지고 있다면, Socialite의 `userFromToken` 메서드를 이용해서 사용자 정보를 조회할 수 있습니다.

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<!-- If you are using Facebook Limited Login via an iOS application, Facebook will return an OIDC token instead of an access token. Like an access token, the OIDC token can be provided to the `userFromToken` method in order to retrieve user details. -->
iOS 애플리케이션을 통해 Facebook Limited Login을 사용하는 경우, Facebook에서는 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰도 액세스 토큰과 마찬가지로 `userFromToken` 메서드에 전달하여 사용자 정보를 조회할 수 있습니다.

<a name="stateless-authentication"></a>
<!-- #### Stateless Authentication -->
#### Stateless Authentication

<!-- The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to a stateless API that does not utilize cookie based sessions: -->
`stateless` 메서드는 세션 상태 검증을 비활성화할 때 사용합니다. 이 기능은 쿠키 기반 세션을 사용하지 않는 무상태 API에 소셜 인증 기능을 추가할 때 유용합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Laravel Socialite provides a convenient way to test OAuth authentication flows without making actual requests to OAuth providers. The `fake` method allows you to mock the OAuth provider's behavior and define the user data that should be returned. -->
Laravel Socialite는 실제 OAuth provider에 요청을 보내지 않고도 OAuth 인증 흐름을 테스트할 수 있는 편리한 기능을 제공합니다. `fake` 메서드를 사용하면 OAuth provider의 동작을 모의(Mock)하고 반환할 사용자 데이터를 지정할 수 있습니다.

<a name="faking-the-redirect"></a>
<!-- #### Faking the Redirect -->
#### Faking the Redirect

<!-- To test that your application correctly redirects users to an OAuth provider, you may invoke the `fake` method before making a request to your redirect route. This will cause Socialite to return a redirect to a fake authorization URL instead of redirecting to the actual OAuth provider: -->
애플리케이션이 사용자를 올바르게 OAuth provider로 리다이렉트하는지 테스트하려면 리다이렉트 라우트 테스트 전에 `fake` 메서드를 호출할 수 있습니다. 그러면 Socialite는 실제 OAuth provider 대신 모의 인증 URL로 리다이렉트합니다.

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
애플리케이션의 콜백 라우트를 테스트하려면 `fake` 메서드를 호출할 때 provider에서 사용자 정보를 조회할 때 반환할 `User` 인스턴스를 직접 지정할 수 있습니다. `User` 인스턴스는 `map` 메서드로 생성합니다.

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
`User` 인스턴스는 기본적으로 `token` 속성을 포함합니다. 추가로 필요한 값이 있다면 `User` 인스턴스에 직접 속성을 지정할 수도 있습니다.

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
