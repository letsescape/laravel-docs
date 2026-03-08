# 라라벨 소셜라이트 (Laravel Socialite)

- [소개](#introduction)
- [설치](#installation)
- [소셜라이트 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 스코프](#access-scopes)
    - [Slack 봇 스코프](#slack-bot-scopes)
    - [옵션 파라미터](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 외에도, Laravel은 [라라벨 소셜라이트](https://github.com/laravel/socialite)를 이용하여 OAuth 제공자와의 인증을 쉽고 간편하게 처리할 수 있는 방법을 제공합니다. 소셜라이트는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티에서 운영하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 확인할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

소셜라이트를 시작하려면 Composer 패키지 관리자를 사용하여 해당 패키지를 프로젝트의 의존성에 추가해야 합니다:

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## 소셜라이트 업그레이드 (Upgrading Socialite)

소셜라이트의 새로운 주요 버전으로 업그레이드할 때는, 반드시 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

<a name="configuration"></a>
## 설정 (Configuration)

소셜라이트를 사용하기 전에, 애플리케이션에서 활용할 각 OAuth 제공자의 자격 증명을 추가해야 합니다. 일반적으로, 해당 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하면 자격 증명을 확인할 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용하는 제공자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid`와 같은 키를 사용해야 합니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> 만약 `redirect` 옵션에 상대 경로를 사용하면, 자동으로 전체 URL로 변환되어 사용됩니다.

<a name="authentication"></a>
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 제공자를 이용해 사용자를 인증하려면, 사용자를 OAuth 제공자로 리다이렉트하는 라우트와, 인증 후 콜백을 받는 라우트, 이렇게 두 개의 라우트가 필요합니다. 아래 예제는 두 가지 라우트의 구현을 보여줍니다:

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

`Socialite` 파사드가 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리다이렉트하는 작업을 담당하며, `user` 메서드는 인증 요청이 승인된 후에 들어온 요청을 분석하고 제공자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 제공자에서 사용자를 조회한 후에는, 해당 사용자가 애플리케이션의 데이터베이스에 존재하는지 확인하고 [사용자를 인증](/docs/master/authentication#authenticate-a-user-instance)해야 합니다. 데이터베이스에 사용자가 없다면, 일반적으로 해당 사용자를 나타내는 새로운 레코드를 생성하게 됩니다:

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
> 특정 OAuth 제공자로부터 획득할 수 있는 사용자 정보에 대한 자세한 내용은 [사용자 정보 조회](#retrieving-user-details) 문서를 참고하세요.

<a name="access-scopes"></a>
### 액세스 스코프 (Access Scopes)

사용자를 리다이렉트하기 전에, `scopes` 메서드를 사용하여 인증 요청에 포함할 "스코프(scope)"를 지정할 수 있습니다. 이 메서드는 이전에 지정된 모든 스코프와, 새롭게 지정한 스코프를 합쳐서 요청에 적용합니다:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

기존의 모든 스코프를 덮어쓰고 싶다면 `setScopes` 메서드를 사용할 수 있습니다:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 스코프 (Slack Bot Scopes)

Slack의 API는 [여러 유형의 액세스 토큰](https://api.slack.com/authentication/token-types)과 각각의 [권한 스코프](https://api.slack.com/scopes)를 제공합니다. 소셜라이트는 다음 두 가지 Slack 액세스 토큰 타입 모두를 지원합니다:

<div class="content-list" markdown="1">

- 봇(Bot): `xoxb-`로 시작
- 사용자(User): `xoxp-`로 시작

</div>

기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자 정보를 반환합니다.

봇 토큰은 애플리케이션의 사용자가 소유한 외부 Slack 워크스페이스에 알림을 보낼 때 유용합니다. 봇 토큰을 생성하려면, 사용자를 Slack 인증 페이지로 리다이렉트하기 전에 `asBotUser` 메서드를 호출해야 합니다:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한, Slack에서 인증 후 사용자를 다시 애플리케이션으로 리다이렉트할 때에도, `user` 메서드를 호출하기 전에 반드시 `asBotUser`를 호출해야 합니다:

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성하면, `user` 메서드가 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 이 경우에는 `token` 속성만 채워집니다. 이 토큰은 [외부 Slack 워크스페이스로 알림을 보낼 때](/docs/master/notifications#notifying-external-slack-workspaces) 저장해두고 사용할 수 있습니다.

<a name="optional-parameters"></a>
### 옵션 파라미터 (Optional Parameters)

여러 OAuth 제공자에서는 리다이렉트 요청에 추가적인 옵션 파라미터를 지원합니다. 이런 옵션 파라미터를 요청에 포함하려면, `with` 메서드에 연관 배열을 전달하면 됩니다:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드 사용 시, `state`나 `response_type`처럼 예약된 키워드는 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 후, 소셜라이트의 `user` 메서드를 이용해 사용자 정보를 조회할 수 있습니다. 이 `user` 메서드가 반환하는 사용자 객체에는, 데이터베이스에 저장할 수 있는 여러 속성과 메서드가 포함되어 있습니다.

연결된 OAuth 제공자가 OAuth 1.0 또는 OAuth 2.0 중 어떤 방식을 사용하는지에 따라, 이 객체의 속성과 메서드가 다를 수 있습니다:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 제공자...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 제공자...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // 모든 제공자에서...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 사용자 정보 조회

이미 유효한 액세스 토큰을 가지고 있다면, 소셜라이트의 `userFromToken` 메서드를 사용해서 해당 사용자의 정보를 조회할 수 있습니다:

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 애플리케이션에서 Facebook Limited Login을 사용하는 경우, Facebook이 액세스 토큰 대신 OIDC 토큰을 반환할 수 있습니다. 이 경우에도, OIDC 토큰을 `userFromToken` 메서드에 전달하여 사용자 정보를 확인할 수 있습니다.

<a name="stateless-authentication"></a>
#### 상태 비저장(stateless) 인증

`stateless` 메서드는 세션 상태 검증을 비활성화할 때 사용할 수 있습니다. 이 기능은 쿠키 기반 세션을 사용하지 않는 상태 비저장 API에 소셜 인증을 추가할 때 유용합니다:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
## 테스트 (Testing)

라라벨 소셜라이트는 실제로 OAuth 제공자에 요청을 보내지 않고도, OAuth 인증 플로우를 테스트할 수 있는 편리한 방법을 제공합니다. `fake` 메서드를 활용하면 OAuth 제공자의 동작을 모킹(mocking)하여, 지정한 사용자 데이터를 반환하도록 할 수 있습니다.

<a name="faking-the-redirect"></a>
#### 리다이렉트 모킹 (Faking the Redirect)

애플리케이션이 올바르게 OAuth 제공자로 사용자를 리다이렉트하는지 테스트하려면, 리다이렉트 라우트로 요청을 보내기 전에 `fake` 메서드를 호출하세요. 그러면 실제 OAuth 제공자가 아니라, 가짜 인증 URL로 리다이렉트가 발생합니다:

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a name="faking-the-callback"></a>
#### 콜백 모킹 (Faking the Callback)

애플리케이션의 콜백 라우트를 테스트하려면, `fake` 메서드를 호출한 뒤, 제공자로부터 사용자 정보 조회 시 반환할 `User` 인스턴스를 지정할 수 있습니다. `User` 인스턴스는 `map` 메서드를 사용해서 생성합니다:

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

기본적으로, `User` 인스턴스에는 `token` 속성도 포함됩니다. 필요하다면, `User` 인스턴스에 추가 속성을 직접 지정할 수도 있습니다:

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
