# Laravel Passport (Laravel Passport)

- [소개](#introduction)
    - [Passport와 Sanctum 중 무엇을 사용할까?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포하기](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 유효기간](#token-lifetimes)
    - [기본 모델 오버라이드](#overriding-default-models)
    - [라우트 오버라이드](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [클라이언트 관리하기](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리하기](#managing-tokens)
    - [토큰 새로고침](#refreshing-tokens)
    - [토큰 폐기하기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Device Code Grant 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Password Grant 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [User Provider 커스터마이징](#customizing-the-user-provider)
    - [Username 필드 커스터마이징](#customizing-the-username-field)
    - [Password 유효성 검증 커스터마이징](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Personal Access Client 생성](#creating-a-personal-access-client)
    - [User Provider 커스터마이징](#customizing-the-user-provider-for-pat)
    - [Personal Access Token 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어 사용](#via-middleware)
    - [Access Token 전달](#passing-the-access-token)
- [Token Scope](#token-scopes)
    - [Scope 정의](#defining-scopes)
    - [기본 Scope](#default-scope)
    - [토큰에 Scope 할당](#assigning-scopes-to-tokens)
    - [Scope 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 여러분의 Laravel 애플리케이션에 OAuth2 서버 전체 구현을 몇 분 만에 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server) 위에 구축되어 있습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 대해 알고 있다고 가정합니다. OAuth2에 대해 아무 정보가 없다면, 계속하기 전에 [용어](https://oauth2.thephpleague.com/terminology/) 및 OAuth2의 주요 기능에 익숙해지길 권장합니다.

<a name="passport-or-sanctum"></a>
### Passport와 Sanctum 중 무엇을 사용할까? (Passport or Sanctum?)

시작하기 전에 여러분의 애플리케이션에 Laravel Passport와 [Laravel Sanctum](/docs/12.x/sanctum) 중 어떤 것이 더 적합한지 결정하는 것이 좋습니다. 애플리케이션이 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션, 또는 API 토큰 발급이 목적이라면 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 좋습니다. Laravel Sanctum은 OAuth2를 지원하지 않으나 훨씬 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` Artisan 명령어를 통해 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 OAuth2 클라이언트 및 접근 토큰을 저장할 테이블 생성을 위해 필요한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 보안 Access Token을 생성하는 데 필요한 암호화 키도 생성합니다.

`install:api` 명령 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` trait과 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 trait은 인증된 사용자의 토큰과 스코프를 확인할 수 있는 몇 가지 헬퍼 메서드를 모델에 제공합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 지정해야 합니다. 이렇게 하면 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하도록 애플리케이션이 동작합니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```

<a name="deploying-passport"></a>
### Passport 배포하기 (Deploying Passport)

Passport를 서버에 처음 배포할 때는 `passport:keys` 명령어를 실행해야 할 가능성이 높습니다. 이 명령은 Access Token 생성에 필요한 암호화 키를 Passport가 만들도록 합니다. 생성된 키는 보통 소스 컨트롤에 포함하지 않습니다:

```shell
php artisan passport:keys
```

필요하다면 Passport의 키를 로드할 경로도 지정할 수 있습니다. `Passport::loadKeysFrom` 메서드를 사용하여 경로를 설정할 수 있으며, 보통 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
#### 환경변수에서 키 불러오기

또는, `vendor:publish` Artisan 명령어를 사용해 Passport의 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일 게시 후에는 다음과 같이 애플리케이션의 암호화 키를 환경변수로 지정하여 불러올 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드 (Upgrading Passport)

Passport를 새로운 메이저 버전으로 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 유효기간 (Token Lifetimes)

기본적으로 Passport는 만료까지 1년의 유효기간을 가진 Access Token을 발급합니다. 만일 토큰의 유효기간을 더 길거나 짧게 조정하고 싶다면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```

> [!WARNING]
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며 단순 표시용입니다. 토큰을 발급할 때 실제 만료 정보는 암호화된 토큰 내에 저장됩니다. 토큰을 무효화하려면 반드시 [폐기(revoke) 작업](#revoking-tokens)을 해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 오버라이드 (Overriding Default Models)

Passport에서 내부적으로 사용하는 모델을 확장하고 싶다면, 자신만의 모델을 정의한 뒤 해당 Passport 모델을 확장하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

커스텀 모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 여러분의 모델을 사용하도록 알려줘야 합니다. 일반적으로 이 작업은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 진행합니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```

<a name="overriding-routes"></a>
### 라우트 오버라이드 (Overriding Routes)

Passport가 기본적으로 등록하는 라우트를 커스터마이징하고 싶다면, 우선 애플리케이션의 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 라우트를 등록하지 않도록 해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

이후 [Passport의 routes 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php`로 복사해서 수정할 수 있습니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="authorization-code-grant"></a>
## Authorization Code Grant

대부분의 개발자들이 익숙한 OAuth2 방식은 권한 코드(authorization code)를 사용하는 방식입니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 여러분의 서버로 리디렉션하고, 사용자는 클라이언트에게 Access Token 발급 요청을 승인하거나 거절하게 됩니다.

우선, Passport가 'authorization' 뷰를 반환하도록 지시할 필요가 있습니다.

이 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 메서드를 통해 커스터마이징할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 경우...
    Passport::authorizationView('auth.oauth.authorize');

    // Closure로 지정하는 경우...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```

Passport는 `/oauth/authorize` 라우트를 자동으로 정의하여 이 뷰를 반환합니다. 여러분의 `auth.oauth.authorize` 템플릿에는 권한 승인을 위한 `passport.authorizations.approve` 라우트로의 POST 요청 폼과, 권한 거절을 위한 `passport.authorizations.deny` 라우트로의 DELETE 요청 폼이 포함되어야 합니다. 이 두 라우트는 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리하기 (Managing Clients)

여러분의 애플리케이션 API와 상호작용하려는 개발자들은 자신의 애플리케이션을 "클라이언트"로 등록해야 합니다. 보통은 애플리케이션 이름과, 인증 후 사용자를 리디렉션할 URI를 제공해야 합니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트파티(자체) 클라이언트

가장 간단하게 클라이언트를 생성하려면 `passport:client` Artisan 명령어를 사용하면 됩니다. 이 명령은 퍼스트파티(자체) 클라이언트 생성이나 OAuth2 기능 테스트용으로 사용할 수 있습니다. 명령 실행시 클라이언트 정보들을 입력하면, 클라이언트 ID와 시크릿이 제공됩니다:

```shell
php artisan passport:client
```

여러 개의 리디렉션 URI를 사용하고 싶으면, 파라미터 입력 시 콤마로 구분된 목록을 입력하면 됩니다. URI에 콤마가 포함된다면, 반드시 URI 인코딩을 사용하세요:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 서드파티(제3자) 클라이언트

여러분의 애플리케이션의 일반 사용자는 `passport:client` 명령어를 사용할 수 없으므로, 특정 사용자에게 클라이언트를 등록하려면 `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 주어진 사용자 소유의 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 해당 사용자가 소유한 OAuth 앱 클라이언트 전체 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게는 `$client->id`(클라이언트 ID), `$client->plainSecret`(클라이언트 시크릿)을 제공할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리디렉션

클라이언트가 생성된 후, 개발자는 클라이언트 ID와 시크릿을 사용하여 애플리케이션으로부터 권한 코드와 Access Token을 요청할 수 있습니다. 우선, 사용하고자 하는 애플리케이션은 `/oauth/authorize` 엔드포인트로 리디렉션 요청을 보냅니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 파라미터를 통해 Passport 애플리케이션의 인증 동작을 지정할 수 있습니다.

- `prompt` 값이 `none`이라면, 사용자가 Passport 애플리케이션에 이미 인증되어 있지 않으면 무조건 인증 오류가 발생합니다.
- `consent`일 경우, 이전에 모든 Scope를 승인했더라도 항상 권한 승인 화면이 표시됩니다.
- `login`은 사용자에게 항상 재로그인을 요구합니다.

`prompt` 값을 지정하지 않으면, 사용자가 해당 Scope에 대해 이미 클라이언트를 승인했다면 별도 승인 없이 처리됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 등록해둡니다. 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인

Passport는 `prompt` 파라미터 값(있다면)에 따라 자동으로 반응하며, 사용자가 권한을 승인 또는 거절할 수 있는 화면을 표시합니다. 사용자가 요청을 승인하면, 승인 시 지정된 `redirect_uri`로 리디렉션됩니다. 단, `redirect_uri`는 클라이언트 생성 시 등록한 리디렉션 URL과 일치해야 합니다.

퍼스트파티 클라이언트 등, 권한 승인 화면을 건너뛰고 싶은 경우에는 [Client 모델을 확장](#overriding-default-models)하고, `skipsAuthorization` 메서드를 정의해 `true`를 반환하도록 하면 됩니다. 단, `prompt` 파라미터가 명시적으로 지정된 경우에는 무시하지 않습니다:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 해당 클라이언트가 권한 승인 화면을 건너뛰는지 결정합니다.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 권한 코드를 Access Token으로 교환

사용자가 권한 요청을 승인하면, 클라이언트 애플리케이션으로 리디렉션됩니다. 이때는 리디렉션 전에 저장한 `state` 파라미터를 검증해야 합니다. 일치한다면, 서버에 `POST` 요청으로 Access Token을 다음과 같이 요청합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

`/oauth/token` 엔드포인트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다. `expires_in` 필드는 토큰 만료까지 남은 초(seconds) 단위의 값을 의미합니다.

> [!NOTE]
> `/oauth/authorize`와 마찬가지로, `/oauth/token` 라우트도 Passport가 자체적으로 등록하므로 수동 등록이 필요 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리하기 (Managing Tokens)

`Laravel\Passport\HasApiTokens` trait의 `tokens` 메서드를 통해 사용자가 승인한 토큰을 가져올 수 있습니다. 예를 들어, 사용자의 서드파티 앱 연결 내역 대시보드를 만들 때 활용할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 유효한 토큰 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 서드파티 OAuth 앱과 연결된 정보 조회...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```

<a name="refreshing-tokens"></a>
### 토큰 새로고침 (Refreshing Tokens)

Access Token이 짧게 발급될 경우 사용자는 함께 제공된 Refresh Token을 사용해서 Access Token을 새로 받아야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Confidential 클라이언트일 때만 필요...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 역시 `access_token`, `refresh_token`, `expires_in` 속성을 포함한 JSON 응답을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 폐기하기 (Revoking Tokens)

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 통해 토큰을 폐기할 수 있습니다. Refresh Token도 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드로 폐기 가능합니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Access Token 폐기
$token->revoke();

// Refresh Token도 폐기
$token->refreshToken?->revoke();

// 특정 사용자의 모든 토큰 폐기
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리 (Purging Tokens)

폐기되었거나 만료된 토큰을 데이터베이스에서 정리하려면 Passport의 `passport:purge` Artisan 명령어를 사용하세요:

```shell
# 폐기, 만료된 토큰, auth code, device code 모두 정리...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리...
php artisan passport:purge --hours=6

# 폐기된 토큰, auth code, device code만 정리...
php artisan passport:purge --revoked

# 만료된 토큰, auth code, device code만 정리...
php artisan passport:purge --expired
```

애플리케이션의 `routes/console.php` 파일에 [스케줄러 작업](/docs/12.x/scheduling)을 등록하여 자동으로 주기적으로 토큰을 정리할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## Authorization Code Grant With PKCE

Authorization Code Grant에 "Proof Key for Code Exchange(PKCE)"를 더하는 방식은 싱글 페이지 애플리케이션이나 모바일 앱과 같이 클라이언트 시크릿 보관이 어렵거나 권한 코드가 도청될 위험을 막으려 할 때 권장되는 매우 안전한 인증 방식입니다. "code verifier"와 "code challenge" 쌍이 클라이언트 시크릿의 역할을 대신합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성 (Creating the Client)

PKCE가 활성화된 클라이언트를 만들려면 `passport:client` Artisan 명령어에 `--public` 옵션을 추가하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### Code Verifier와 Code Challenge

이 인증 방식은 클라이언트 시크릿을 제공하지 않으므로, 개발자는 코드를 요청할 때 code verifier와 code challenge 쌍을 생성해야 합니다.

code verifier는 RFC 7636 사양에 따라 43~128자 길이의 영문 대소문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자로 이루어진 랜덤 문자열이어야 합니다.

code challenge는 URL·파일이름 안전한 Base64 인코딩 문자열로, 마지막의 `'='` 패딩은 제거하며 줄바꿈이나 추가 공백 문자가 없어야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리디렉션

클라이언트를 만든 뒤에는, PKCE 인증을 위해 code verifier와 code challenge를 생성해서 아래와 같이 `/oauth/authorize`에 리디렉션 요청을 보냅니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 권한 코드를 Access Token으로 교환

사용자가 권한을 승인하면 리디렉션된 클라이언트는 표준 Authorization Code Grant와 동일하게 state 값을 검증하고, 초기 생성한 코드 verifier도 함께 제출하여 Access Token을 요청합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="device-authorization-grant"></a>
## Device Authorization Grant

OAuth2 Device Authorization Grant는 TV나 콘솔 등 브라우저나 입력장치가 제한된 디바이스가 "디바이스 코드"를 통해 access token을 얻을 수 있도록 해줍니다. 기기에서 사용자에게 별도의 기기(예: PC·스마트폰)로 "user code"를 입력해 인증을 완료하라고 안내하는 방식입니다.

처음 시작할 때는 Passport에게 "user code" 및 "authorization" 뷰 반환 방식을 지시해야 합니다.

이 뷰의 렌더링은 `Laravel\Passport\Passport` 클래스의 메서드를 이용해 커스터마이징할 수 있으며, 일반적으로 `App\Providers\AppServiceProvider`의 `boot`에서 설정합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // Closure로 지정
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```

Passport는 이러한 뷰를 반환하는 라우트를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보낼 폼을 포함해야 하며, 이때 `user_code` 쿼리 파라미터가 필요합니다.

`auth.oauth.device.authorize` 템플릿에는 권한 승인용 `passport.device.authorizations.approve`(POST), 거절용 `passport.device.authorizations.deny`(DELETE) 폼이 있어야 하며, 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### Device Authorization Grant 클라이언트 생성

디바이스 인증 플로우로 토큰을 발급하려면, 우선 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. `passport:client` 명령어에 `--device` 옵션을 붙이면 퍼스트파티 디바이스 클라이언트를 생성할 수 있습니다:

```shell
php artisan passport:client --device
```

추가로, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 통해 특정 사용자의 서드파티 디바이스 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```

<a name="requesting-device-authorization-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="device-code"></a>
#### 디바이스 코드 요청

클라이언트가 생성되면, 클라이언트 ID로 `/oauth/device/code`에 POST 요청하여 device code를 요청할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답으로 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성이 반환됩니다. `expires_in`은 device code의 만료까지 남은 초(seconds)이며, `interval`은 `/oauth/token`을 polling(반복 요청)할 때 두 요청 사이에 기다려야 하는 초 단위 시간입니다.

> [!NOTE]
> `/oauth/device/code` 라우트도 Passport가 미리 등록해두기 때문에 따로 정의할 필요가 없습니다.

<a name="user-code"></a>
#### Verification URI 및 User Code 안내

디바이스 코드 발급 후, 해당 기기는 사용자에게 다른 기기로 `verification_uri`를 방문하고 `user_code`를 입력하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 Polling

별도의 기기에서 사용자가 승인 또는 거절할 수 있으므로, 토큰을 받기 전까지 `/oauth/token`을 `interval` 주기로 polling해야 합니다:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Confidential 클라이언트만 필요
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 승인을 완료하면 `access_token`, `refresh_token`, `expires_in` 정보를 포함한 JSON이 반환됩니다.

<a name="password-grant"></a>
## Password Grant

> [!WARNING]
> 더 이상 Password Grant token 사용을 권장하지 않습니다. 반드시 [OAuth2 Server에서 현재 권장하는 grant 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

OAuth2 Password Grant는 모바일 앱 등의 퍼스트파티 클라이언트에서 이메일/사용자명과 비밀번호로 Access Token을 획득할 수 있게 해줍니다. 즉, 사용자가 전체 OAuth2 권한 승인을 하지 않아도 클라이언트에서 직접 토큰을 발급받을 수 있습니다.

Password Grant를 활성화하려면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant`를 호출하십시오:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
### Password Grant 클라이언트 생성

Password Grant로 토큰을 발급하려면, 해당 grant 타입이 활성화된 클라이언트를 만들어야 합니다. `passport:client` Artisan 명령어에 `--password` 옵션을 붙이세요.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

grant를 활성화하고 클라이언트를 만들었으면, `/oauth/token`에 POST 요청으로 사용자의 이메일/비밀번호를 전송해 토큰을 요청하세요. 이 라우트는 Passport가 미리 등록해둡니다. 성공 시 JSON 응답으로 `access_token`, `refresh_token`이 반환됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Confidential 클라이언트만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> Access Token은 기본적으로 장기(valid)합니다. 필요에 따라 [최대 Access Token 유효기간](#configuration)을 직접 설정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

Password Grant 혹은 Client Credentials Grant 사용 시, 애플리케이션의 모든 Scope를 허용하도록 토큰을 승인하고 싶다면, `*` Scope를 요청하세요. 이 Scope가 부여된 토큰의 `can` 메서드는 항상 `true`를 반환합니다. `*` Scope는 반드시 `password` 혹은 `client_credentials` grant 방식으로 발급된 토큰에서만 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Confidential 클라이언트만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### User Provider 커스터마이징

[여러 인증 User Provider](/docs/12.x/authentication#introduction)를 사용하는 애플리케이션에서는 `artisan passport:client --password` 명령어 실행시 `--provider` 옵션으로 Password Grant 클라이언트가 사용할 provider를 지정할 수 있습니다. provider 명은 반드시 `config/auth.php`에 정의된 provider 중 하나여야 합니다. 이후 [미들웨어로 라우트를 보호](#multiple-authentication-guards)하여 해당 provider의 사용자만 승인할 수 있도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
### Username 필드 커스터마이징

Password Grant 인증 시, Passport는 기본적으로 인증 모델의 `email` 속성을 Username으로 사용합니다. 만약 변경하고 싶다면 모델에 `findForPassport` 메서드를 정의하여 원하는 컬럼을 사용하도록 할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Bridge\Client;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * 주어진 username 값에 해당하는 사용자 인스턴스를 반환합니다.
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### Password 유효성 검증 커스터마이징

Password Grant 인증 시, Passport는 모델의 `password` 속성을 검사해 비밀번호 유효성 검증을 수행합니다. 만약 `password` 속성이 없거나 검증 로직을 직접 커스터마이징하고 싶다면, `validateForPassportPasswordGrant` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Passport Grant를 위한 비밀번호 검증 로직
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## Implicit Grant

> [!WARNING]
> Implicit Grant token 사용은 더 이상 권장되지 않으니, [OAuth2 Server에서 현재 권장하는 grant 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택하세요.

Implicit Grant 방식은 Authorization Code Grant와 유사하지만, 권한 코드 교환 없이 바로 토큰이 반환됩니다. 주로 자바스크립트 혹은 모바일 앱 등 클라이언트 시크릿 보관이 불가능한 경우에 사용합니다. 사용하려면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `enableImplicitGrant`를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

Implicit Grant 토큰을 발급하려면, `passport:client` Artisan 명령어에 `--implicit` 옵션을 붙여 클라이언트를 생성합니다.

```shell
php artisan passport:client --implicit
```

Implicit Grant 활성화 후, 생성된 클라이언트 ID로 다음과 같이 `/oauth/authorize`로 Access Token을 요청할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 라우트 역시 Passport가 자동으로 등록하므로 수동정의할 필요 없습니다.

<a name="client-credentials-grant"></a>
## Client Credentials Grant

Client Credentials Grant는 서버 간(Machine-to-Machine) 인증이 필요할 때 적합합니다. 예를 들어, API 유지관리 작업을 수행하는 예약 작업 등에 사용할 수 있습니다.

이 방식을 사용하려면 `passport:client` Artisan 명령어에 `--client` 옵션을 붙여 클라이언트를 만드세요:

```shell
php artisan passport:client --client
```

그리고 다음과 같이 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 지정합니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 토큰 유효 및 클라이언트가 자원 소유자임을 검증...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 Scope만 허용하고 싶다면, `using` 메서드에 필요한 Scope들을 나열할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // "servers:read", "servers:create" 두 Scope가 모두 부여되어야 접근 가능...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 발급받기

이 방식으로 토큰을 받으려면 `oauth/token` 엔드포인트에 다음과 같이 요청합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
## Personal Access Tokens

사용자가 별도의 권한 승인 플로우(리디렉션) 없이 스스로 Access Token을 발급받고 싶을 때 Personal Access Token을 사용할 수 있습니다. 이를 통해, 사용자에게 여러분의 API를 실험해보거나 손쉽게 토큰을 발급하는 UI를 제공할 수 있습니다.

> [!NOTE]
> 만약 Passport를 주로 personal access token 발급용으로만 사용한다면, Laravel의 경량 API 토큰 라이브러리인 [Laravel Sanctum](/docs/12.x/sanctum)을 고려하세요.

<a name="creating-a-personal-access-client"></a>
### Personal Access Client 생성

Personal Access Token 발급을 위해서는 Personal Access Client를 만들어야 합니다. 이미 `passport:install` 명령을 실행했다면 아래 명령어는 필요 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### User Provider 커스터마이징

[여러 인증 User Provider](/docs/12.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령시에 `--provider` 옵션으로 provider를 지정할 수 있습니다. 지정한 provider는 `config/auth.php`의 provider 명과 일치해야 하며, [미들웨어를 활용](#multiple-authentication-guards)해 해당 provider만 접근 허용할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### Personal Access Token 관리

Personal Access Client를 만든 뒤에는, `App\Models\User` 인스턴스의 `createToken` 메서드를 이용해 해당 사용자에 대한 토큰을 발급할 수 있습니다. 첫 번째 인수는 토큰의 이름, 두 번째(선택) 인수는 [Scopes](#token-scopes) 배열입니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성
$token = $user->createToken('My Token')->accessToken;

// 특정 스코프 지정
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프 허용
$token = $user->createToken('My Token', ['*'])->accessToken;

// 해당 사용자 소유의 유효한 PAT만 조회
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호하기 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 통한 인증

Passport는 [인증 가드](/docs/12.x/authentication#adding-custom-guards) 기능을 제공해, Access Token이 포함된 API 요청을 검증합니다. `api` 가드가 `passport` 드라이버를 사용하도록 설정했다면, 접근 제한이 필요한 라우트에 `auth:api` 미들웨어만 추가하면 됩니다:

```php
Route::get('/user', function () {
    // 토큰 인증이 완료된 사용자만 접근 가능
})->middleware('auth:api');
```

> [!WARNING]
> [Client Credentials Grant](#client-credentials-grant)를 사용하는 경우, [`Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어](#client-credentials-grant)를 사용하세요. `auth:api` 미들웨어 대신 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 다중 인증 가드

다양한(Eloquent 모델이 다를 수 있는) 사용자 유형을 인증해야 하는 경우, 각 User Provider에 맞는 Guard를 별도로 정의해야 할 수 있습니다. 예를 들어, 아래처럼 `config/auth.php`에서 설정할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```

그러면 아래와 같이 `api-customers` 가드를 사용하는 라우트를 만들 수 있습니다. 즉, `customers` provider의 사용자만 인증 가능합니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> 여러 User Provider 사용 시 자세한 사항은 [PAT 관련 문서](#customizing-the-user-provider-for-pat), [Password Grant 관련 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### Access Token 전달

Passport로 보호된 라우트에 요청할 때, API 사용자는 요청 헤더의 `Authorization`에 `Bearer` 형식으로 Access Token을 전달해야 합니다. 예를 들어, `Http` 파사드를 사용할 때는 아래와 같습니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## Token Scope (Token Scopes)

Scope는 API 클라이언트가 인증 과정에서 계정에 요청할 수 있는 권한 범위를 세분화한 것입니다. 예를 들어, 이커머스 앱에서 모든 API 사용자에게 주문 생성 권한이 필요하지 않을 수 있습니다. Scope를 통해 주문 상태 조회 권한만 필요한 경우 소비자에게 제한된 권한만 부여할 수 있습니다. 즉, Scope는 서드파티 앱이 대신 수행할 수 있는 작업을 명확하게 제한할 수 있습니다.

<a name="defining-scopes"></a>
### Scope 정의

API Scope는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드로 정의할 수 있습니다. 이 메서드는 Scope 이름과 설명이 담긴 배열을 받으며, 이 설명은 권한 승인 화면에 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
### 기본 Scope

클라이언트가 특정 Scope를 요청하지 않은 경우, `defaultScopes` 메서드로 기본 Scope를 자동 부여할 수도 있습니다. 역시 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하세요:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 Scope 할당

<a name="when-requesting-authorization-codes"></a>
#### Authorization Code Grant 요청 시

Authorization Code Grant로 Access Token을 요청할 경우, 클라이언트는 `scope` 쿼리 파라미터에 원하는 Scope명을 공백으로 구분해 나열해야 합니다:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
#### Personal Access Token 발급 시

`App\Models\User`의 `createToken` 메서드에서 두 번째 인수로 Scope 배열을 지정할 수 있습니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### Scope 확인 (Checking Scopes)

Passport는 토큰의 Scope를 검증할 수 있는 두 가지 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 Scope 검사

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어는 지정한 모든 Scope가 Access Token에 포함되어 있어야 접근을 허용합니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // "orders:read"와 "orders:create" Scope 모두 필요
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 하나라도 일치하는 Scope 검사

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 나열한 Scope 중 하나라도 있으면 접근을 허용합니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // "orders:read" 또는 "orders:create" 중 하나만 있어도 허용
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 Scope 검사

Access Token으로 인증된 요청에서, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 통해 Scope 보유 여부를 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 기타 Scope 관련 메서드

`scopeIds` 메서드는 정의된 모든 Scope의 ID/이름 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 Scope를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다:

```php
Passport::scopes();
```

`scopesFor` 메서드는 지정한 Scope ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 Scope가 정의되어 있는지 확인하려면 `hasScope`를 사용하세요:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

애플리케이션에서 API를 구축할 때, 자바스크립트(프론트엔드) 앱이 같은 API를 직접 소비할 수 있다면 매우 편리합니다. 이 방식은 웹, 모바일, 서드파티, 다양한 SDK 어디서든 동일한 API를 사용할 수 있게 해줍니다.

이때 일반적으로 매 요청마다 액세스 토큰을 직접 보내야 하지만, Passport는 이를 단순화하는 미들웨어를 제공합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 마지막에 추가하세요:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 반드시 미들웨어 스택의 마지막에 배치되어야 합니다.

이 미들웨어는 모든 응답에 `laravel_token` 쿠키(JWT)를 추가하고, Passport가 이 JWT를 사용하여 자바스크립트 앱의 API 요청을 인증할 수 있도록 합니다. 이 쿠키는 `session.lifetime` 설정과 동일한 만료시간을 가집니다. 브라우저가 자동으로 쿠키를 함께 전송하므로 토큰을 직접 헤더로 전달하지 않아도 다음과 같이 단순하게 요청할 수 있습니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면 `Passport::cookie` 메서드로 JWT 쿠키의 이름을 직접 지정할 수 있습니다. 역시 `App\Providers\AppServiceProvider`의 `boot`에서 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
#### CSRF 보호

이 방식 인증을 사용할 땐 요청에 CSRF 토큰 헤더가 반드시 포함되어야 합니다. 라라벨 스캐폴딩 및 모든 스타터킷은 [Axios](https://github.com/axios/axios)를 기본 포함하며, `XSRF-TOKEN` 쿠키 값을 이용해 `X-XSRF-TOKEN` 헤더를 자동으로 보내도록 설정되어 있습니다.

> [!NOTE]
> 만약 `X-CSRF-TOKEN` 헤더를 직접 보내고 싶으면, 반드시 `csrf_token()` 함수가 제공하는 **암호화되지 않은 토큰**을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 Access Token 및 Refresh Token을 발급하거나 폐기하면 아래와 같은 이벤트를 발생시킵니다. [이벤트 리스너를 등록](/docs/12.x/events)해 토큰 관리/일괄 폐기 처리를 할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                      |
| ----------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`    |
| `Laravel\Passport\Events\AccessTokenRevoked`    |
| `Laravel\Passport\Events\RefreshTokenCreated`   |

</div>

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 부여할 Scope를 지정할 수 있게 해줍니다. 첫 번째 인수로 User 인스턴스, 두 번째로 부여할 Scope 배열을 전달하면 됩니다:

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트 및 Scope를 지정합니다. 첫 번째 인수는 Client 인스턴스, 두 번째는 토큰에 부여할 Scope 배열입니다:

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```
