# Laravel Socialite (Laravel Socialite)

- [소개](#introduction)
- [설치](#installation)
- [Socialite 업그레이드](#upgrading-socialite)
- [설정](#configuration)
- [인증](#authentication)
    - [라우팅](#routing)
    - [인증 및 저장](#authentication-and-storage)
    - [액세스 범위](#access-scopes)
    - [Slack 봇 범위](#slack-bot-scopes)
    - [선택적 파라미터](#optional-parameters)
- [사용자 정보 조회](#retrieving-user-details)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

일반적인 폼 기반 인증 이외에도, Laravel은 [Laravel Socialite](https://github.com/laravel/socialite)를 사용하여 OAuth(오쓰) 제공자와 간편하게 인증할 수 있는 방법을 제공합니다. Socialite는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket, Slack을 통한 인증을 지원합니다.

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티가 주도하는 [Socialite Providers](https://socialiteproviders.com/) 웹사이트에서 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Socialite를 시작하려면 Composer 패키지 관리자를 사용하여 해당 패키지를 프로젝트의 의존성에 추가합니다.

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite 업그레이드 (Upgrading Socialite)

Socialite의 새로운 주요 버전으로 업그레이드할 때에는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 반드시 꼼꼼히 검토해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

Socialite를 사용하기 전에, 애플리케이션에서 사용할 OAuth 제공자에 대한 인증 정보를 추가해야 합니다. 일반적으로 이 인증 정보는 해당 서비스의 대시보드에서 "개발자 애플리케이션"을 생성하여 얻을 수 있습니다.

이 인증 정보는 애플리케이션의 `config/services.php` 설정 파일에 위치해야 하며, 사용하려는 제공자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack`, `slack-openid` 등 다양한 키를 사용할 수 있습니다:

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
## 인증 (Authentication)

<a name="routing"></a>
### 라우팅 (Routing)

OAuth 제공자를 사용하여 사용자를 인증하려면, 하나는 사용자를 OAuth 제공자로 리다이렉트하는 라우트와 하나는 인증 완료 후 제공자로부터 콜백을 받는 라우트, 이 두 개의 라우트가 필요합니다. 아래 예시는 두 라우트의 구현 예시입니다.

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

`Socialite` 파사드에서 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자로 리다이렉트해주며, `user` 메서드는 콜백 요청을 분석해 인증이 승인된 후 제공자로부터 사용자 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장 (Authentication and Storage)

OAuth 제공자로부터 사용자를 받아오면, 해당 사용자가 애플리케이션 데이터베이스에 존재하는지 확인하고 [사용자 인증](/docs/12.x/authentication#authenticate-a-user-instance)을 진행할 수 있습니다. 데이터베이스에 사용자가 존재하지 않는 경우, 일반적으로 새로운 사용자 레코드를 생성하게 됩니다.

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
> 각 OAuth 제공자로부터 어떤 사용자 정보를 받을 수 있는지 더 알아보려면, [사용자 정보 조회](#retrieving-user-details) 섹션을 참고하세요.

<a name="access-scopes"></a>
### 액세스 범위 (Access Scopes)

사용자를 리다이렉트하기 전에, `scopes` 메서드를 사용하여 인증 요청에 포함시킬 "범위(scope)"를 지정할 수 있습니다. 이 메서드는 이미 지정된 범위에 새 범위를 추가하여 병합합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

인증 요청에서 기존의 모든 범위를 새 범위로 덮어쓰려면 `setScopes` 메서드를 사용할 수 있습니다.

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack 봇 범위 (Slack Bot Scopes)

Slack의 API는 [여러 유형의 액세스 토큰](https://api.slack.com/authentication/token-types)과 각각의 [권한 범위(scope)](https://api.slack.com/scopes)를 제공합니다. Socialite는 아래 두 가지 Slack 액세스 토큰 유형 모두와 호환됩니다.

<div class="content-list" markdown="1">

- Bot(봇, `xoxb-` 접두사)
- User(사용자, `xoxp-` 접두사)

</div>

기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며, 드라이버의 `user` 메서드를 호출하면 사용자 정보를 반환합니다.

봇 토큰은 애플리케이션을 사용하는 사용자가 소유한 외부 Slack 워크스페이스에 알림을 보내야 할 경우에 주로 활용됩니다. 봇 토큰을 생성하려면, 사용자를 Slack 인증으로 리다이렉트하기 전에 `asBotUser` 메서드를 호출하면 됩니다.

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

또한, 인증 후 Slack이 사용자를 다시 애플리케이션으로 리다이렉트한 후에 `user` 메서드를 호출하기 전에 반드시 `asBotUser` 메서드를 호출해야 합니다.

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

봇 토큰을 생성할 때도 `user` 메서드는 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, 이때는 오직 `token` 속성만 채워져 있습니다. 이 토큰은 [인증된 사용자의 Slack 워크스페이스에 알림 발송](/docs/12.x/notifications#notifying-external-slack-workspaces)에 활용할 수 있도록 저장해둘 수 있습니다.

<a name="optional-parameters"></a>
### 선택적 파라미터 (Optional Parameters)

여러 OAuth 제공자들은 리다이렉트 요청에서 추가적인 선택적 파라미터를 지원합니다. 이러한 파라미터를 요청에 포함하려면, 연관 배열 형태로 `with` 메서드를 호출하면 됩니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` 메서드를 사용할 때는 `state`, `response_type`과 같은 예약어는 전달하지 않도록 주의해야 합니다.

<a name="retrieving-user-details"></a>
## 사용자 정보 조회 (Retrieving User Details)

사용자가 애플리케이션의 인증 콜백 라우트로 리다이렉트된 이후에 Socialite의 `user` 메서드를 사용하여 사용자 정보를 조회할 수 있습니다. `user` 메서드로 반환되는 사용자 객체는 다양한 속성과 메서드를 제공하므로, 이를 사용해 사용자의 정보를 데이터베이스에 저장할 수 있습니다.

OAuth 1.0 또는 OAuth 2.0 지원 여부에 따라 해당 객체에서 사용할 수 있는 속성과 메서드가 다를 수 있습니다.

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

    // 모든 제공자에서 사용 가능...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰으로 사용자 정보 조회

이미 해당 사용자의 유효한 액세스 토큰을 가지고 있다면, Socialite의 `userFromToken` 메서드를 이용해서 사용자 정보를 조회할 수 있습니다.

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS 애플리케이션을 통해 Facebook Limited Login을 사용하는 경우, Facebook에서는 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰도 액세스 토큰과 마찬가지로 `userFromToken` 메서드에 전달하여 사용자 정보를 조회할 수 있습니다.

<a name="stateless-authentication"></a>
#### 무상태 인증 (Stateless Authentication)

`stateless` 메서드는 세션 상태 검증을 비활성화할 때 사용합니다. 이 기능은 쿠키 기반 세션을 사용하지 않는 무상태 API에 소셜 인증 기능을 추가할 때 유용합니다.

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel Socialite는 실제 OAuth 제공자에게 요청을 보내지 않고도 OAuth 인증 흐름을 테스트할 수 있는 편리한 기능을 제공합니다. `fake` 메서드를 사용하면 OAuth 제공자의 동작을 모의(Mock)하고 반환할 사용자 데이터를 지정할 수 있습니다.

<a name="faking-the-redirect"></a>
#### 리다이렉트 모의하기

애플리케이션이 사용자를 올바르게 OAuth 제공자로 리다이렉트하는지 테스트하려면, 리다이렉트 라우트 테스트 전에 `fake` 메서드를 호출할 수 있습니다. 그러면 Socialite는 실제 OAuth 제공자 대신, 모의 인증 URL로 리다이렉트하게 됩니다.

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a name="faking-the-callback"></a>
#### 콜백 모의하기

애플리케이션의 콜백 라우트를 테스트하려면, `fake` 메서드를 호출하면서, 제공자로부터 사용자 정보를 조회할 때 반환할 `User` 인스턴스를 직접 지정할 수 있습니다. `User` 인스턴스는 `map` 메서드를 사용하여 생성합니다.

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

`User` 인스턴스는 기본적으로 `token` 속성을 포함합니다. 추가로 필요한 값이 있다면 직접 속성을 지정할 수도 있습니다.

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
