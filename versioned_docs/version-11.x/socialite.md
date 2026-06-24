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

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication via Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, and Slack. -->
일반적인 폼 기반 인증 외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth 공급자와 쉽게 인증할 수 있는 간편한 방법을 제공합니다. 현재 Socialite는 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 기타 플랫폼용 어댑터는 커뮤니티에서 운영하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트를 통해 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started with Socialite, use the Composer package manager to add the package to your project's dependencies: -->
Socialite를 사용하려면, Composer 패키지 매니저를 이용해 프로젝트에 패키지를 추가하세요:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
<!-- ## Upgrading Socialite -->
## Upgrading Socialite

<!-- When upgrading to a new major version of Socialite, it's important that you carefully review [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md). -->
Socialite의 새 주요 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인하시기 바랍니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Socialite, you will need to add credentials for the OAuth providers your application utilizes. Typically, these credentials may be retrieved by creating a "developer application" within the dashboard of the service you will be authenticating with. -->
Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 공급자용 자격 증명을 추가해야 합니다. 일반적으로, 해당 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하면 자격 증명을 얻을 수 있습니다.

<!-- These credentials should be placed in your application's `config/services.php` configuration file, and should use the key `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, or `slack-openid`, depending on the providers your application requires: -->
이러한 자격 증명 정보는 애플리케이션의 `config/services.php` 설정 파일에 추가해야 하며, 필요한 공급자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid` 중 하나의 키를 사용해야 합니다:

```
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 포함되어 있다면, 자동으로 전체 URL로 변환됩니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- To authenticate users using an OAuth provider, you will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. The example routes below demonstrate the implementation of both routes: -->
OAuth 공급자를 이용해 사용자를 인증하려면, 사용자를 공급자로 리디렉션하는 라우트와 인증 완료 후 콜백을 받는 라우트, 이렇게 두 개의 라우트가 필요합니다. 아래 예시 라우트는 두 라우트를 어떻게 구현하는지 보여줍니다:

```
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

<!-- The `redirect` method provided by the `Socialite` facade takes care of redirecting the user to the OAuth provider, while the `user` method will examine the incoming request and retrieve the user's information from the provider after they have approved the authentication request. -->
`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth 공급자로 리디렉션하는 역할을 하며, `user` 메서드는 인증 승인이 완료된 후 전달받은 요청을 검사하여 공급자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
<!-- ### Authentication and Storage -->
### Authentication and Storage

<!-- Once the user has been retrieved from the OAuth provider, you may determine if the user exists in your application's database and [authenticate the user](/docs/11.x/authentication#authenticate-a-user-instance). If the user does not exist in your application's database, you will typically create a new record in your database to represent the user: -->
OAuth 공급자로부터 사용자를 가져온 뒤, 해당 사용자가 데이터베이스에 이미 존재하는지 확인하고 [authenticate the user](/docs/11.x/authentication#authenticate-a-user-instance)할 수 있습니다. 만약 사용자가 데이터베이스에 없다면, 일반적으로 신규 레코드를 생성하여 사용자를 저장합니다:

```
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Facades\Socialite;

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
> 특정 OAuth 공급자에서 제공하는 사용자 정보에 대한 자세한 내용은 [retrieving user details](#retrieving-user-details) 문서를 참고해주세요.

<a name="access-scopes"></a>
<!-- ### Access Scopes -->
### Access Scopes

<!-- Before redirecting the user, you may use the `scopes` method to specify the "scopes" that should be included in the authentication request. This method will merge all previously specified scopes with the scopes that you specify: -->
사용자를 리디렉션하기 전에, `scopes` 메서드를 이용해 인증 요청에 포함할 "스코프(scope)"를 지정할 수 있습니다. 이 메서드를 사용하면 이전에 지정한 스코프에 현재 지정한 스코프가 합쳐집니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

<!-- You can overwrite all existing scopes on the authentication request using the `setScopes` method: -->
`setScopes` 메서드를 사용하면, 기존에 설정된 모든 스코프를 덮어써서 요청에 새로운 스코프만 포함시킬 수 있습니다:

```
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
<!-- ### Slack Bot Scopes -->
### Slack Bot Scopes

<!-- Slack's API provides [different types of access tokens](https://api.slack.com/authentication/token-types), each with their own set of [permission scopes](https://api.slack.com/scopes). Socialite is compatible with both of the following Slack access tokens types: -->
Slack의 API는 [different types of access tokens](https://api.slack.com/authentication/token-types)을 제공하며, 각각의 [permission scopes](https://api.slack.com/scopes)가 존재합니다. Socialite는 다음 두 가지 Slack 액세스 토큰 타입 모두를 지원합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Bot (prefixed with `xoxb-`)
- User (prefixed with `xoxp-`)
-->
- Bot(접두사 `xoxb-`)
- User(접두사 `xoxp-`)

<!-- </div> -->
</div>

<!-- By default, the `slack` driver will generate a `user` token and invoking the driver's `user` method will return the user's details. -->
기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자 정보를 반환합니다.

<!-- Bot tokens are primarily useful if your application will be sending notifications to external Slack workspaces that are owned by your application's users. To generate a bot token, invoke the `asBotUser` method before redirecting the user to Slack for authentication: -->
봇 토큰(Bot token)은 애플리케이션이 외부 Slack 워크스페이스(여러분의 애플리케이션 사용자가 소유한 워크스페이스)에 알림을 전송해야 할 때 유용합니다. 봇 토큰을 생성하려면, 사용자를 Slack으로 인증시키기 전에 `asBotUser` 메서드를 호출해야 합니다:

```
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

<!-- In addition, you must invoke the `asBotUser` method before invoking the `user` method after Slack redirects the user back to your application after authentication: -->
또한 Slack에서 인증 완료 후 사용자를 다시 돌려보내면, `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 호출해야 합니다:

```
$user = Socialite::driver('slack')->asBotUser()->user();
```

<!-- When generating a bot token, the `user` method will still return a `Laravel\Socialite\Two\User` instance; however, only the `token` property will be hydrated. This token may be stored in order to [send notifications to the authenticated user's Slack workspaces](/docs/11.x/notifications#notifying-external-slack-workspaces). -->
봇 토큰을 생성할 때도, `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환합니다. 단, 이 경우에는 오직 `token` 속성만 값이 채워집니다. 이렇게 획득한 토큰은 [send notifications to the authenticated user's Slack workspaces](/docs/11.x/notifications#notifying-external-slack-workspaces) 사용할 수 있습니다.

<a name="optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- A number of OAuth providers support other optional parameters on the redirect request. To include any optional parameters in the request, call the `with` method with an associative array: -->
일부 OAuth 공급자는 리디렉션 요청 시 다양한 옵션 파라미터를 지원합니다. 옵션 파라미터를 요청에 추가하려면, `with` 메서드에 연관 배열을 전달하세요:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state`, `response_type`과 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
<!-- ## Retrieving User Details -->
## Retrieving User Details

<!-- After the user is redirected back to your application's authentication callback route, you may retrieve the user's details using Socialite's `user` method. The user object returned by the `user` method provides a variety of properties and methods you may use to store information about the user in your own database. -->
사용자가 인증 콜백 라우트로 리디렉션된 후, Socialite의 `user` 메서드를 사용해 사용자 정보를 가져올 수 있습니다. 이때 `user` 메서드로 반환되는 사용자 객체는 여러분이 데이터베이스에 저장할 수 있도록 다양한 속성과 메서드를 제공합니다.

<!-- Differing properties and methods may be available on this object depending on whether the OAuth provider you are authenticating with supports OAuth 1.0 or OAuth 2.0: -->
OAuth 공급자가 OAuth 1.0 또는 OAuth 2.0 중 어떤 버전을 사용하는지에 따라 사용할 수 있는 속성과 메서드가 다를 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

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
이미 사용자의 액세스 토큰이 있다면, Socialite의 `userFromToken` 메서드를 사용해 사용자 정보를 가져올 수 있습니다:

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<!-- If you are using Facebook Limited Login via an iOS application, Facebook will return an OIDC token instead of an access token. Like an access token, the OIDC token can be provided to the `userFromToken` method in order to retrieve user details. -->
iOS 애플리케이션에서 Facebook Limited Login을 사용하는 경우, Facebook은 액세스 토큰 대신 OIDC 토큰을 반환합니다. 이 OIDC 토큰도 액세스 토큰과 마찬가지로 `userFromToken` 메서드에 전달해 사용자 정보를 가져올 수 있습니다.

<a name="stateless-authentication"></a>
<!-- #### Stateless Authentication -->
#### Stateless Authentication

<!-- The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to a stateless API that does not utilize cookie based sessions: -->
`stateless` 메서드를 사용하면 세션 상태 검증을 비활성화할 수 있습니다. 이 방법은 쿠키 기반 세션을 사용하지 않는 무상태 API에 소셜 로그인을 추가할 때 유용합니다:

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```
