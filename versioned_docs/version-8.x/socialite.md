<!-- # Laravel Socialite -->
# Laravel Socialite

- [Introduction](#introduction)
- [Installation](#installation)
- [Upgrading Socialite](#upgrading-socialite)
- [Configuration](#configuration)
- [Authentication](#authentication)
    - [Routing](#routing)
    - [Authentication & Storage](#authentication-and-storage)
    - [Access Scopes](#access-scopes)
    - [Optional Parameters](#optional-parameters)
- [Retrieving User Details](#retrieving-user-details)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to typical, form based authentication, Laravel also provides a simple, convenient way to authenticate with OAuth providers using [Laravel Socialite](https://github.com/laravel/socialite). Socialite currently supports authentication with Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, and Bitbucket. -->
일반적인 폼 기반 인증과 더불어, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용해 OAuth 제공자와 쉽게 인증할 수 있는 간편한 방법도 제공합니다. 소셜라이트는 현재 Facebook, Twitter, LinkedIn, Google, GitHub, GitLab, Bitbucket 인증을 지원합니다.

> [!TIP]
> 기타 플랫폼용 어댑터는 커뮤니티에서 운영하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 확인할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started with Socialite, use the Composer package manager to add the package to your project's dependencies: -->
Socialite를 사용하려면 Composer 패키지 매니저로 프로젝트에 패키지를 추가하세요.

```
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
<!-- ## Upgrading Socialite -->
## Upgrading Socialite

<!-- When upgrading to a new major version of Socialite, it's important that you carefully review [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md). -->
Socialite의 새로운 메이저 버전으로 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- Before using Socialite, you will need to add credentials for the OAuth providers your application utilizes. These credentials should be placed in your application's `config/services.php` configuration file, and should use the key `facebook`, `twitter`, `linkedin`, `google`, `github`, `gitlab`, or `bitbucket`, depending on the providers your application requires: -->
Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 제공자의 자격 증명을 추가해야 합니다. 이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용하려는 제공자에 따라 `facebook`, `twitter`, `linkedin`, `google`, `github`, `gitlab`, `bitbucket` 중 하나의 키를 사용해야 합니다.

```
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!TIP]
> 만약 `redirect` 옵션에 상대 경로가 포함되어 있다면, 전체 URL로 자동 변환됩니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- To authenticate users using an OAuth provider, you will need two routes: one for redirecting the user to the OAuth provider, and another for receiving the callback from the provider after authentication. The example controller below demonstrates the implementation of both routes: -->
OAuth 제공자를 사용해 사용자를 인증하려면 두 개의 라우트가 필요합니다. 첫 번째는 사용자를 OAuth 제공자로 리디렉션하는 라우트, 두 번째는 인증 후 제공자로부터 콜백을 받는 라우트입니다. 아래 컨트롤러 예제는 두 라우트 구현 방식을 보여줍니다.

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

<!-- The `redirect` method provided by the `Socialite` facade takes care of redirecting the user to the OAuth provider, while the `user` method will read the incoming request and retrieve the user's information from the provider after they are authenticated. -->
`Socialite` 파사드의 `redirect` 메서드는 사용자를 OAuth 제공자로 리디렉션하는 역할을 하며, `user` 메서드는 인증이 완료된 후 콜백 요청을 읽어와 제공자로부터 사용자 정보를 받아옵니다.

<a name="authentication-and-storage"></a>
<!-- ### Authentication & Storage -->
### Authentication & Storage

<!-- Once the user has been retrieved from the OAuth provider, you may determine if the user exists in your application's database and [authenticate the user](/docs/8.x/authentication#authenticate-a-user-instance). If the user does not exist in your application's database, you will typically create a new record in your database to represent the user: -->
OAuth 제공자로부터 사용자를 받아온 후, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하여 [authenticate the user](/docs/8.x/authentication#authenticate-a-user-instance)이 가능합니다. 만약 사용자가 아직 데이터베이스에 없다면, 일반적으로 사용자를 나타내는 새로운 레코드를 생성하게 됩니다.

```
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Facades\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::where('github_id', $githubUser->id)->first();

    if ($user) {
        $user->update([
            'github_token' => $githubUser->token,
            'github_refresh_token' => $githubUser->refreshToken,
        ]);
    } else {
        $user = User::create([
            'name' => $githubUser->name,
            'email' => $githubUser->email,
            'github_id' => $githubUser->id,
            'github_token' => $githubUser->token,
            'github_refresh_token' => $githubUser->refreshToken,
        ]);
    }

    Auth::login($user);

    return redirect('/dashboard');
});
```

> [!TIP]
> 특정 OAuth 제공자로부터 어떤 사용자 정보를 받을 수 있는지 더 알고 싶다면, [retrieving user details](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
<!-- ### Access Scopes -->
### Access Scopes

<!-- Before redirecting the user, you may also add additional "scopes" to the authentication request using the `scopes` method. This method will merge all existing scopes with the scopes that you supply: -->
사용자를 리디렉션하기 전에, 인증 요청에 추가 "스코프(scope)"를 `scopes` 메서드로 지정할 수 있습니다. 이 메서드는 기존 스코프에 전달한 스코프를 합쳐줍니다.

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

<!-- You can overwrite all existing scopes on the authentication request using the `setScopes` method: -->
`setScopes` 메서드를 사용하면 인증 요청의 모든 기존 스코프를 덮어쓸 수 있습니다.

```
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- A number of OAuth providers support optional parameters in the redirect request. To include any optional parameters in the request, call the `with` method with an associative array: -->
여러 OAuth 제공자는 리디렉션 요청에서 선택적 파라미터를 지원합니다. 선택적 파라미터를 포함하려면, 연관 배열을 `with` 메서드에 전달하면 됩니다.

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!NOTE]
> `with` 메서드를 사용할 때는 `state`, `response_type`과 같은 예약어는 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
<!-- ## Retrieving User Details -->
## Retrieving User Details

<!-- After the user is redirected back to your authentication callback route, you may retrieve the user's details using Socialite's `user` method. The user object returned by the `user` method provides a variety of properties and methods you may use to store information about the user in your own database. Different properties and methods may be available depending on whether the OAuth provider you are authenticating with supports OAuth 1.0 or OAuth 2.0: -->
사용자가 인증 콜백 라우트로 리디렉션된 이후, Socialite의 `user` 메서드로 사용자의 정보를 받아올 수 있습니다. `user` 메서드에서 반환되는 사용자 객체는 데이터베이스에 사용자 정보를 저장할 때 사용할 다양한 속성과 메서드를 제공합니다. 어떤 속성과 메서드가 제공되는지는 인증에 사용하는 OAuth 제공자가 OAuth 1.0인지, OAuth 2.0인지에 따라 다릅니다.

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
<!-- #### Retrieving User Details From A Token (OAuth2) -->
#### Retrieving User Details From A Token (OAuth2)

<!-- If you already have a valid access token for a user, you can retrieve their details using Socialite's `userFromToken` method: -->
이미 사용자의 유효한 액세스 토큰이 있다면, Socialite의 `userFromToken` 메서드로 사용자 정보를 받아올 수 있습니다.

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
<!-- #### Retrieving User Details From A Token And Secret (OAuth1) -->
#### Retrieving User Details From A Token And Secret (OAuth1)

<!-- If you already have a valid token and secret for a user, you can retrieve their details using Socialite's `userFromTokenAndSecret` method: -->
이미 사용자의 토큰과 시크릿이 있다면, Socialite의 `userFromTokenAndSecret` 메서드로 사용자 정보를 받아올 수 있습니다.

```
use Laravel\Socialite\Facades\Socialite;

$user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);
```

<a name="stateless-authentication"></a>
<!-- #### Stateless Authentication -->
#### Stateless Authentication

<!-- The `stateless` method may be used to disable session state verification. This is useful when adding social authentication to an API: -->
`stateless` 메서드를 사용하면 세션 상태 검증을 비활성화할 수 있습니다. 이는 API에 소셜 인증을 추가할 때 유용합니다.

```
use Laravel\Socialite\Facades\Socialite;

return Socialite::driver('google')->stateless()->user();
```

> [!NOTE]
> 상태 비저장 인증은 Twitter 드라이버에서는 사용할 수 없습니다. Twitter 드라이버는 인증 시 OAuth 1.0을 사용합니다.
