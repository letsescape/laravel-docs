# Laravel Passport (Laravel Passport)

- [소개](#introduction)
    - [Passport와 Sanctum 중 무엇을 사용할까요?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 만료 시간 설정](#token-lifetimes)
    - [기본 모델 재정의](#overriding-default-models)
    - [라우트 재정의](#overriding-routes)
- [인증 코드 그랜트](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청하기](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 취소](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE가 적용된 인증 코드 그랜트](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청하기](#requesting-auth-pkce-grant-tokens)
- [디바이스 인증 그랜트](#device-authorization-grant)
    - [디바이스 코드 그랜트 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청하기](#requesting-device-authorization-grant-tokens)
- [패스워드 그랜트](#password-grant)
    - [패스워드 그랜트 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청하기](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider)
    - [사용자명 필드 커스터마이징](#customizing-the-username-field)
    - [비밀번호 유효성 검증 커스터마이징](#customizing-the-password-validation)
- [임플리싯 그랜트](#implicit-grant)
- [클라이언트 크레덴셜 그랜트](#client-credentials-grant)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [사용자 프로바이더 커스터마이징](#customizing-the-user-provider-for-pat)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호하기](#protecting-routes)
    - [미들웨어를 통한 보호](#via-middleware)
    - [액세스 토큰 전달](#passing-the-access-token)
- [토큰 스코프](#token-scopes)
    - [스코프 정의](#defining-scopes)
    - [기본 스코프](#default-scope)
    - [토큰에 스코프 할당](#assigning-scopes-to-tokens)
    - [스코프 확인](#checking-scopes)
- [SPA 인증](#spa-authentication)
- [이벤트](#events)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 몇 분 만에 완전한 OAuth2 서버 구현을 제공하는 패키지입니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 서버](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!NOTE]
> 이 문서는 여러분이 이미 OAuth2에 대해 숙지하고 있다고 가정합니다. 만약 OAuth2에 대해 잘 모른다면, 계속하기 전에 [용어](https://oauth2.thephpleague.com/terminology/)와 기능에 대해 익히는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
### Passport와 Sanctum 중 무엇을 사용할까요? (Passport or Sanctum?)

시작하기 전에, Laravel Passport와 [Laravel Sanctum](/docs/master/sanctum) 중 어느 것이 더 적합한지 결정할 필요가 있습니다. 애플리케이션이 OAuth2를 반드시 지원해야 한다면 Laravel Passport를 사용해야 합니다.

하지만, 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션, 또는 단순히 API 토큰이 필요한 경우라면 [Laravel Sanctum](/docs/master/sanctum)을 사용하는 것이 좋습니다. Sanctum은 OAuth2를 지원하지 않으나, 훨씬 간단한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` Artisan 명령어를 통해 Laravel Passport를 설치할 수 있습니다:

```shell
php artisan install:api --passport
```

이 명령어는 애플리케이션에 필요한 OAuth2 클라이언트 및 액세스 토큰 저장용 테이블을 생성하기 위해 데이터베이스 마이그레이션을 퍼블리시하고 실행합니다. 또한, 보안 액세스 토큰 생성을 위한 암호화 키도 생성합니다.

`install:api` 실행 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가해야 합니다. 이 트레이트는 인증된 사용자의 토큰과 스코프를 확인할 수 있는 헬퍼 메서드들을 제공합니다:

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

마지막으로, 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정합니다. 이렇게 하면 API 요청 인증 시 Passport의 `TokenGuard`를 사용하게 됩니다:

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
### Passport 배포 (Deploying Passport)

Passport를 처음 서버에 배포할 때는 `passport:keys` 명령어를 실행해야 할 수도 있습니다. 이 명령은 Passport가 액세스 토큰 생성을 위해 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 컨트롤에 포함되지 않습니다.

```shell
php artisan passport:keys
```

필요하다면 Passport의 키를 불러올 경로를 정의할 수도 있습니다. `Passport::loadKeysFrom` 메서드를 사용하여 이를 지정할 수 있습니다. 이 메서드는 보통 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

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
#### 환경변수에서 키 로드하기

또는 `vendor:publish` Artisan 명령어로 Passport의 설정 파일을 퍼블리시할 수도 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일이 퍼블리시 된 후에는 환경변수로 암호화 키를 정의하여 불러올 수 있습니다:

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

Passport의 새 주요 버전으로 업그레이드할 때는, [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼭 꼼꼼히 확인해야 합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 만료 시간 설정 (Token Lifetimes)

Passport는 기본적으로 1년이 지나야 만료되는 장기간 유효한 액세스 토큰을 발급합니다. 토큰의 만료 시간을 더 길거나 짧게 조정하고 싶다면, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며, 단순히 표시용입니다. 토큰을 발급할 때, 만료 정보는 서명되고 암호화된 토큰 안에 저장됩니다. 토큰을 무효화해야 한다면 [토큰 취소](#revoking-tokens)를 사용하세요.

<a name="overriding-default-models"></a>
### 기본 모델 재정의 (Overriding Default Models)

Passport가 내부적으로 사용하는 모델을 확장하려면, 직접 모델을 정의하고 해당 Passport 모델을 상속하면 됩니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 지정 모델을 사용하도록 알려야 합니다. 일반적으로 이 동작은 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 설정합니다:

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
### 라우트 재정의 (Overriding Routes)

Passport가 등록하는 라우트를 커스터마이즈 하려면, 먼저 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가해야 합니다:

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

그 다음, [Passport 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 복사해 애플리케이션의 `routes/web.php`에 붙여넣고 필요에 맞게 수정할 수 있습니다:

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
## 인증 코드 그랜트 (Authorization Code Grant)

OAuth2를 사용할 때 인증 코드(authorization code)를 사용하는 방식이 가장 일반적입니다. 이 방식에서는 클라이언트 애플리케이션이 사용자를 서버로 리디렉션하여, 사용자가 클라이언트에 토큰 발급 요청을 승인하거나 거부할 수 있도록 합니다.

시작하려면 "authorization" 뷰를 Passport가 어떻게 반환할 지 지정해야 합니다.

인증 관련 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 메서드들을 통해 커스터마이즈할 수 있습니다. 이 설정도 보통 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이뤄집니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름을 지정하는 방법...
    Passport::authorizationView('auth.oauth.authorize');

    // 클로저를 사용하는 방법...
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

Passport는 `/oauth/authorize` 라우트를 자동으로 정의해서 이 뷰를 반환합니다. `auth.oauth.authorize` 템플릿에는 인증을 승인하기 위한 `passport.authorizations.approve` 라우트로의 POST 요청 폼과, 거부를 위한 `passport.authorizations.deny` 라우트로의 DELETE 요청 폼이 포함되어야 합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리 (Managing Clients)

API와 통신해야 하는 애플리케이션을 개발하는 개발자라면, 자신의 애플리케이션을 여러분의 애플리케이션에 "클라이언트"로 등록해야 합니다. 보통 클라이언트의 이름, 그리고 사용자가 인증 승인 후 리디렉션될 URI 정도를 제공해야 합니다.

<a name="managing-first-party-clients"></a>
#### 1st-Party(자사) 클라이언트

가장 간단하게 클라이언트를 생성하는 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 자사 클라이언트나 OAuth2 기능 테스트를 위해 사용할 수 있습니다. 실행하면 추가 정보를 입력받고, 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client
```

여러 개의 리디렉션 URI를 허용하려면, URI를 쉼표로 구분하여 입력하면 됩니다. 쉼표가 포함된 URI는 URI 인코딩되어야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 3rd-Party(외부) 클라이언트

여러분의 애플리케이션 사용자들은 `passport:client` 명령어를 직접 사용할 수 없으므로, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용해 사용자를 위한 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// 지정한 사용자의 OAuth 앱 클라이언트 생성...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// 사용자가 소유한 모든 OAuth 앱 클라이언트 조회...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자는 `$client->id`를 클라이언트 ID로, `$client->plainSecret`를 클라이언트 시크릿으로 사용합니다.

<a name="requesting-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인증을 위한 리디렉션

클라이언트가 생성되었다면, 개발자는 클라이언트 ID와 시크릿을 사용해 인증 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 소비 애플리케이션이 여러분의 애플리케이션 `/oauth/authorize` 라우트로 리디렉션 요청을 해야 합니다:

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

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 지정할 때 사용합니다.

- `prompt` 값이 `none`이면 Passport는 사용자가 이미 Passport 애플리케이션에 인증되지 않은 경우 인증 오류를 반환합니다.
- `prompt` 값이 `consent`면, 기존에 모든 스코프를 허용했더라도 항상 승인 화면이 표시됩니다.
- `prompt` 값이 `login`이면, 세션이 있더라도 항상 재로그인을 요구합니다.

`prompt` 파라미터가 없으면, 사용자가 해당 스코프에 대해 이미 클라이언트를 승인한 경우엔 추가 인증이 필요하지 않습니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 이미 Passport에 의해 정의되어 있으므로, 직접 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인

Passport는 `prompt` 파라미터의 값에 따라 자동으로 인증 요청에 응답하며, 필요시 승인/거부할 수 있는 화면을 사용자에게 표시합니다. 사용자가 요청을 승인하면, 지정했던 `redirect_uri`로 리디렉션됩니다. 이 `redirect_uri`는 클라이언트 생성 시 등록한 것과 일치해야 합니다.

경우에 따라, 1st-party 클라이언트라면 인증 프롬프트를 건너뛰고 싶을 수 있습니다. 이 때는 [Client 모델을 확장](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하면 됩니다. `skipsAuthorization`이 `true`를 반환하면, 클라이언트가 즉시 승인되어 사용자가 `redirect_uri`로 바로 이동하게 됩니다. 단, 소비 애플리케이션이 `prompt` 파라미터를 설정한 경우에는 제외됩니다.

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * 클라이언트가 인증 프롬프트를 건너뛰어야 하는지 여부를 판단합니다.
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
#### 인증 코드를 액세스 토큰으로 변환

사용자가 인증 요청을 승인하면 소비 애플리케이션으로 리디렉션됩니다. 먼저 소비자는 리디렉션 이전에 저장했던 `state` 파라미터와 반환된 값이 일치하는지 검증해야 합니다. 이후, 액세스 토큰을 요청하기 위해 애플리케이션에 `POST` 요청을 보내야 하며, 요청에는 인증 승인 시 발급된 인증 코드가 포함되어야 합니다:

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

`/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 값은 액세스 토큰의 만료(초, 단위)를 의미합니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트도 Passport에 의해 정의되어 있으므로, 따로 정의하지 않아도 됩니다.

<a name="managing-tokens"></a>
### 토큰 관리 (Managing Tokens)

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하면 사용자의 모든 인가된 토큰을 조회할 수 있습니다. 예를 들어, 사용자가 여러 서드파티 애플리케이션과의 연결을 한눈에 관리할 수 있는 대시보드를 제공할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 사용자의 유효한 토큰 모두 조회...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// 사용자의 3rd-party OAuth 앱 연결 목록 집계...
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
### 토큰 갱신 (Refreshing Tokens)

애플리케이션에서 단기(짧은 만료 시간) 액세스 토큰을 발급한다면, 사용자는 토큰 만료 시 refresh token을 사용해 토큰을 갱신해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 컨피덴셜(Confidential) 클라이언트에만 필요...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 엔드포인트도 마찬가지로 `access_token`, `refresh_token`, `expires_in` 값을 포함한 JSON 응답을 반환합니다.

<a name="revoking-tokens"></a>
### 토큰 취소 (Revoking Tokens)

토큰을 취소(무효화)하려면 `Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용하면 됩니다. 토큰의 refresh token을 취소하려면 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용합니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// 액세스 토큰 취소...
$token->revoke();

// 토큰의 리프레시 토큰 취소...
$token->refreshToken?->revoke();

// 사용자의 모든 토큰 일괄 취소...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리 (Purging Tokens)

토큰이 취소되거나 만료되면, 데이터베이스에서 이를 정리할 수 있습니다. 이를 위해 Passport는 `passport:purge` Artisan 명령어를 제공합니다:

```shell
# 취소되거나 만료된 토큰/인증 코드/디바이스 코드 정리...
php artisan passport:purge

# 6시간 이상 만료된 토큰만 정리...
php artisan passport:purge --hours=6

# 취소된 토큰/인증 코드/디바이스 코드만 정리...
php artisan passport:purge --revoked

# 만료된 토큰/인증 코드/디바이스 코드만 정리...
php artisan passport:purge --expired
```

또한, 애플리케이션의 `routes/console.php` 파일에서 [스케줄러 작업](/docs/master/scheduling)을 설정하면 정기적으로 자동 정리가 가능합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE가 적용된 인증 코드 그랜트 (Authorization Code Grant With PKCE)

"Proof Key for Code Exchange"(PKCE)가 적용된 인증 코드 그랜트는, 싱글 페이지 애플리케이션(SPA)이나 모바일 앱처럼 클라이언트 시크릿을 안전하게 저장하기 어려운 환경에서 API 인증에 사용할 수 있는 보안 강화 방식입니다. 이 방식에서는 인증 코드 탈취 위험을 줄이기 위해, "코드 검증기(code verifier)"와 "코드 챌린지(code challenge)" 조합이 클라이언트 시크릿을 대신합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성 (Creating the Client)

PKCE 인증 코드 그랜트로 토큰을 발급하려면, PKCE가 활성화된 클라이언트를 먼저 생성해야 합니다. `passport:client` Artisan 명령어에 `--public` 옵션을 사용하세요:

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청하기 (Requesting Tokens)

<a name="code-verifier-code-challenge"></a>
#### 코드 검증기와 코드 챌린지

이 그랜트에서는 클라이언트 시크릿이 제공되지 않기 때문에, 개발자는 코드 검증기와 코드 챌린지 조합을 생성해야 합니다.

- 코드 검증기는 43~128자리의 임의 문자열로, 영문자·숫자 및 `"-"`, `"."`, `"_"`, `"~"` 등의 문자를 포함할 수 있습니다. ([RFC 7636 명세](https://tools.ietf.org/html/rfc7636) 참고)
- 코드 챌린지는 URL 및 파일명에 안전한 Base64 인코딩된 문자열로, 끝의 `'='` 문자는 제거하며 줄바꿈, 공백, 기타 문자는 포함되지 않아야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인증을 위한 리디렉션

클라이언트를 생성한 뒤엔, 클라이언트 ID와 생성한 코드 검증기·챌린지를 사용해 인증 코드를 요청할 수 있습니다. 우선 소비 애플리케이션에서 `/oauth/authorize` 라우트로 리디렉션 요청을 보냅니다:

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
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인증 코드를 액세스 토큰으로 변환

사용자가 인증을 승인하면 소비 애플리케이션으로 리디렉션됩니다. 표준 인증 코드 그랜트와 마찬가지로, `state` 값 검증 후 액세스 토큰을 요청하되, 원래 생성했던 코드 검증기도 함께 전송해야 합니다:

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
## 디바이스 인증 그랜트 (Device Authorization Grant)

OAuth2 디바이스 인증 그랜트는 TV, 콘솔 등 입력 수단이 제한된 디바이스에서 "디바이스 코드"를 교환하여 액세스 토큰을 받을 수 있는 방식을 의미합니다. 디바이스 플로우를 사용할 때, 디바이스에서는 사용자에게 별도의 기기(컴퓨터나 스마트폰 등)에서 서버에 접속해 "user code"를 입력하라는 안내를 표시합니다.

먼저 Passport에 "user code"와 "authorization" 뷰 반환 방식을 지정해야 합니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Passport\Passport` 클래스의 메서드로 커스터마이즈할 수 있습니다. 이 설정도 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 처리합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // 뷰 이름 지정...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // 클로저 사용...
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

Passport는 이 뷰를 반환하는 라우트들을 자동 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 포함되어야 하며, `passport.device.authorizations.authorize` 라우트는 `user_code` 쿼리 파라미터를 요구합니다.

`auth.oauth.device.authorize` 템플릿에는 인증 승인을 위한 `passport.device.authorizations.approve`로의 POST와, 거부를 위한 `passport.device.authorizations.deny`로의 DELETE 요청 폼이 필요합니다. 두 라우트 모두 `state`, `client_id`, `auth_token` 필드를 사용합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 코드 그랜트 클라이언트 생성 (Creating a Device Authorization Grant Client)

디바이스 인증 그랜트를 사용할 경우, 디바이스 플로우가 활성화된 클라이언트를 먼저 생성해야 합니다. `passport:client` Artisan 명령어에 `--device` 옵션을 사용하면, 1st-party 디바이스 플로우 클라이언트가 생성되며, 클라이언트 ID와 시크릿을 확인할 수 있습니다:

```shell
php artisan passport:client --device
```

또는, `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용해 특정 사용자를 소유자로 가진 3rd-party 클라이언트도 등록할 수 있습니다:

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

클라이언트가 생성되었다면, 개발자는 클라이언트 ID를 사용하여 애플리케이션에 디바이스 코드를 요청할 수 있습니다. 먼저, 소비 디바이스에서 `/oauth/device/code` 라우트로 `POST` 요청을 보냅니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

응답으로는 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함한 JSON이 반환됩니다. `expires_in`은 디바이스 코드 만료까지 남은 초, `interval`은 `/oauth/token`을 폴링할 때 디바이스가 대기해야 하는 최소 초(second)입니다.

> [!NOTE]
> `/oauth/device/code` 라우트는 Passport가 이미 정의하므로, 직접 정의할 필요가 없습니다.

<a name="user-code"></a>
#### 인증 URI 및 사용자 코드 표시

디바이스 코드가 발급되면, 디바이스는 사용자가 별도 기기를 사용해 응답에서 제공된 `verification_uri`에 접속하여 `user_code`를 입력하라고 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자가 별도 기기로 인증을 승인(혹은 거부)하게 되므로, 디바이스는 `/oauth/token` 라우트를 폴링하여 사용자의 응답을 기다려야 합니다. 폴링 시에는 디바이스 코드 발급 응답에서 받은 최소 `interval` 만큼 대기해야 합니다(속도 제한 방지):

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // 컨피덴셜(Confidential) 클라이언트에만 필요...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 인증을 승인하면 `access_token`, `refresh_token`, `expires_in`을 포함한 JSON이 반환됩니다.

<a name="password-grant"></a>
## 패스워드 그랜트 (Password Grant)

> [!WARNING]
> 패스워드 그랜트 토큰 발급은 더 이상 권장되지 않습니다. 대신, [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 사용하는 것이 좋습니다.

OAuth2 패스워드 그랜트는 모바일 앱 등 다른 1st-party 클라이언트가 이메일/사용자명과 비밀번호를 통해 직접 액세스 토큰을 받을 수 있도록 해줍니다. 패스워드 그랜트는 OAuth2 인증 코드 리디렉트 절차를 거치지 않고도, 보안적으로 1st-party 클라이언트에서 토큰 발급이 가능한 방법입니다.

패스워드 그랜트를 활성화 하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `enablePasswordGrant`를 호출하세요:

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
### 패스워드 그랜트 클라이언트 생성

패스워드 그랜트로 토큰을 발급하려면, `passport:client` Artisan 명령어에 `--password` 옵션을 사용하세요:

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청하기

패스워드 그랜트를 활성화하고 클라이언트를 생성했다면, `/oauth/token` 라우트에 사용자의 이메일과 비밀번호를 포함한 `POST` 요청을 하여 액세스 토큰을 받을 수 있습니다. 이 라우트는 Passport가 자동 등록하므로 직접 등록할 필요가 없습니다. 요청이 성공하면 서버로부터 `access_token`과 `refresh_token`이 포함된 JSON 응답을 받게 됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // 컨피덴셜(Confidential) 클라이언트에만 필요...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> 액세스 토큰은 기본적으로 장기 유효합니다. 필요하다면 [토큰 만료 시간](#configuration)을 원하는 대로 재설정할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

패스워드 그랜트 또는 클라이언트 크레덴셜 그랜트 사용 시, 애플리케이션에서 지원하는 모든 스코프에 대해 토큰 인가를 요청하고 싶다면, `*` 스코프를 요청하면 됩니다. `*` 스코프가 토큰에 할당되면, `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 오직 `password` 또는 `client_credentials` 그랜트로 발급되는 토큰에만 할당됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 한 개 이상의 [사용자 인증 프로바이더](/docs/master/authentication#introduction)를 사용할 경우, `--provider` 옵션을 사용하여 패스워드 그랜트 클라이언트가 어떤 프로바이더를 사용할 지 지정할 수 있습니다. 이 옵션의 이름은 `config/auth.php`에 정의된 유효한 프로바이더와 일치해야 합니다. 이후 해당 가드를 사용하는 미들웨어로 라우트 보호가 가능합니다.

<a name="customizing-the-username-field"></a>
### 사용자명 필드 커스터마이징

패스워드 그랜트 인증 시, Passport는 인증 가능한 모델의 `email` 속성을 기본 사용자명으로 사용합니다. 이 동작을 바꾸려면 모델에 `findForPassport` 메서드를 정의하세요:

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
     * 주어진 사용자명으로 사용자 인스턴스 찾기
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 유효성 검증 커스터마이징

패스워드 그랜트 사용 시, Passport는 모델의 `password` 속성을 사용해 입력받은 비밀번호를 검증합니다. 만약 `password` 속성이 없거나, 검증 로직을 수정하고 싶다면 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다:

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
     * Passport 패스워드 그랜트용 비밀번호 검증
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 임플리싯 그랜트 (Implicit Grant)

> [!WARNING]
> 임플리싯 그랜트 토큰 사용은 더 이상 권장되지 않습니다. [OAuth2 서버에서 현재 권장하는 그랜트 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 참조하세요.

임플리싯 그랜트는 인증 코드 그랜트와 유사하지만, 인증 코드 교환 없이 바로 클라이언트에 토큰이 전달됩니다. 이 방식은 클라이언트 시크릿을 안전하게 저장할 수 없는 자바스크립트나 모바일 앱에서 주로 사용되었습니다. 활성화 하려면, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `enableImplicitGrant` 를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

임플리싯 그랜트로 토큰을 발급하려면, 다음과 같이 `--implicit` 옵션을 사용해 클라이언트를 생성해야 합니다:

```shell
php artisan passport:client --implicit
```

임플리싯 그랜트를 활성화하고 클라이언트 생성이 완료되면, 소비 애플리케이션은 클라이언트 ID로 다음과 같이 액세스 토큰을 요청할 수 있습니다. 이때 `/oauth/authorize` 라우트로 리디렉션 요청을 보냅니다:

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
        // 'prompt' => '', // "none", "consent", 또는 "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` 라우트는 Passport가 이미 정의하므로 직접 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 크레덴셜 그랜트 (Client Credentials Grant)

클라이언트 크레덴셜 그랜트는 시스템 간 통신(Machine-to-Machine) 인증에 적합합니다. 예를 들어, 예약 작업에서 API를 통해 주기적으로 유지보수 작업을 수행하고자 할 때 사용할 수 있습니다.

클라이언트 크레덴셜 그랜트로 토큰을 발급하려면 먼저 `passport:client` 명령어에 `--client` 옵션을 사용해 클라이언트를 생성해야 합니다:

```shell
php artisan passport:client --client
```

다음은 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당하는 예시입니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자임...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프에 대한 접근만 허용하려면, `using` 메서드에 스코프 목록을 넘겨주세요:

```php
Route::get('/orders', function (Request $request) {
    // 액세스 토큰이 유효하고, 클라이언트가 리소스 소유자이며 "servers:read" 및 "servers:create" 스코프가 모두 있음...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 조회

이 방식으로 토큰을 받으려면 `oauth/token` 엔드포인트로 요청하면 됩니다:

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
## 개인 액세스 토큰 (Personal Access Tokens)

사용자가 별도의 인증 절차 없이 직접 액세스 토큰을 발급받길 원할 수도 있습니다. 이를 통해 사용자에게 API 실험이나 간단한 토큰 발급 인터페이스를 제공할 수 있습니다.

> [!NOTE]
> 주로 개인 액세스 토큰만을 위해 Passport를 사용한다면, [Laravel Sanctum](/docs/master/sanctum) 사용을 고려하세요. 이는 API 액세스 토큰 발급에 특화된 경량 라이브러리입니다.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성 (Creating a Personal Access Client)

개인 액세스 토큰을 발급하려면, 먼저 개인 액세스 클라이언트를 생성해야 합니다. 이때 `passport:client` Artisan 명령어에서 `--personal` 옵션을 사용합니다. `passport:install`을 이미 실행했다면 이 과정은 생략해도 됩니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이징

여러 [사용자 인증 프로바이더](/docs/master/authentication#introduction)를 사용하는 경우, `--provider` 옵션을 통해 어떤 프로바이더를 쓸지 지정할 수 있습니다. 이 옵션의 값은 `config/auth.php`에 정의된 유효한 프로바이더여야 하고, 라우트를 미들웨어로 보호해 특정 프로바이더 사용자만 인가 가능하도록 만들 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성했다면, `App\Models\User` 인스턴스에서 `createToken` 메서드를 사용해 특정 사용자에 대한 토큰을 발급할 수 있습니다. 첫 번째 인자는 토큰 이름, 두 번째 인자는 [스코프](#token-scopes) 배열입니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// 스코프 없이 토큰 생성...
$token = $user->createToken('My Token')->accessToken;

// 스코프가 지정된 토큰 생성...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// 모든 스코프 허용 토큰 생성...
$token = $user->createToken('My Token', ['*'])->accessToken;

// 사용자의 유효한 개인 액세스 토큰만 조회...
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
### 미들웨어를 통한 보호 (Via Middleware)

Passport는 요청에 포함된 액세스 토큰을 검증하는 [인증 가드](/docs/master/authentication#adding-custom-guards)를 제공합니다. `api` 가드를 `passport`로 설정한 후, 인증이 필요한 라우트에 `auth:api` 미들웨어만 지정하면 됩니다:

```php
Route::get('/user', function () {
    // API 인증 사용자만 접근 가능...
})->middleware('auth:api');
```

> [!WARNING]
> [클라이언트 크레덴셜 그랜트](#client-credentials-grant)를 사용 중이라면, `auth:api` 미들웨어 대신 [EnsureClientIsResourceOwner 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 여러 인증 가드

여러 유형의 사용자(예: 서로 다른 Eloquent 모델)가 각각 다른 인증 체계를 쓰는 경우, 사용자 프로바이더별로 가드 설정이 필요할 수 있습니다. 이렇게 하면 특정 프로바이더에 대응하는 라우트만을 보호할 수 있습니다. 예를 들어, 다음과 같이 `config/auth.php`에 정의했다면:

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

다음 라우트는 `api-customers` 가드를 사용하여 `customers` 프로바이더의 사용자만 인증할 수 있습니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> 여러 사용자 프로바이더와 Passport 조합에 대해 더 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [패스워드 그랜트 문서](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달 (Passing the Access Token)

Passport로 보호되는 라우트를 호출할 때, API 소비자는 요청 헤더의 `Authorization` 항목에 `Bearer` 토큰 형식으로 액세스 토큰을 명시해야 합니다. 예를 들어, `Http` 파사드를 사용할 때는 다음과 같이 지정합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
## 토큰 스코프 (Token Scopes)

스코프는 API 클라이언트가 계정 접근 권한을 요청할 때, 구체적으로 어떤 권한이 필요한지 명시할 수 있게 해줍니다. 예를 들어, 이커머스 앱이라면 모든 API 소비자가 주문 생성 권한이 필요하지 않을 수 있습니다. 대신, 배송 현황 조회 등 일부 권한만 요청할 수 있도록 스코프를 정의할 수 있습니다. 즉, 스코프를 활용해 3rd-party 애플리케이션이 사용자를 대신해 할 수 있는 행동의 범위를 제어할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의 (Defining Scopes)

`App\Providers\AppServiceProvider`의 `boot`에서 `Passport::tokensCan` 메서드를 사용해 API 스코프를 정의할 수 있습니다. 이 메서드는 스코프 이름과 설명으로 구성된 배열을 받으며, 설명은 승인 화면에 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => '사용자 정보 조회',
        'orders:create' => '주문 생성',
        'orders:read:status' => '주문 상태 조회',
    ]);
}
```

<a name="default-scope"></a>
### 기본 스코프 (Default Scope)

클라이언트가 특별한 스코프를 요청하지 않은 경우, Passport 서버가 토큰에 기본 스코프를 부여하도록 할 수 있습니다. 역시 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `defaultScopes`로 지정합니다:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => '사용자 정보 조회',
    'orders:create' => '주문 생성',
    'orders:read:status' => '주문 상태 조회',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
### 토큰에 스코프 할당 (Assigning Scopes to Tokens)

<a name="when-requesting-authorization-codes"></a>
#### 인증 코드 요청 시

인증 코드 그랜트로 액세스 토큰을 요청할 때, 원하는 스코프를 `scope` 쿼리 파라미터에 스페이스로 구분하여 명시합니다:

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
#### 개인 액세스 토큰 발급 시

`App\Models\User`의 `createToken` 메서드를 사용할 때, 두 번째 인자로 원하는 스코프 배열을 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인 (Checking Scopes)

Passport는 토큰의 스코프 인가 여부를 확인할 수 있는 두 개의 미들웨어를 제공합니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하면, 요청하는 액세스 토큰이 나열된 *모든* 스코프를 포함하고 있는지 확인할 수 있습니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read"와 "orders:create" 스코프 모두를 가지고 있음...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 일부(하나 이상) 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 나열된 스코프 중 *하나라도* 포함되었는지 검사합니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // 액세스 토큰이 "orders:read" 또는 "orders:create" 중 하나의 스코프라도 가지고 있음...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰으로 인증된 요청이라면, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 통해 스코프를 직접 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
#### 추가 스코프 메서드

모든 정의된 스코프 ID/이름 배열은 `scopeIds` 메서드로 반환할 수 있습니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환하려면 `scopes`를 사용하세요:

```php
Passport::scopes();
```

특정 ID/이름에 해당하는 `Laravel\Passport\Scope` 인스턴스 배열은 `scopesFor`로 얻을 수 있습니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

특정 스코프가 정의되어 있는지 확인하려면 `hasScope` 메서드를 쓰세요:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

API를 만들 땐, 자바스크립트 애플리케이션에서 API를 직접 호출할 수 있으면 매우 유용합니다. 이 구조를 사용하면 직접 만든 웹/모바일/3rd-party 애플리케이션/SKD 등에서도 동일한 API를 사용할 수 있습니다.

보통 자바스크립트 앱에서 API를 사용하려면, 액세스 토큰을 수동으로 전송하고, 각 요청마다 헤더에 포함해야 합니다. 그러나 Passport의 미들웨어를 활용하면 이 과정을 자동화할 수 있습니다. `CreateFreshApiToken` 미들웨어를 애플리케이션의 `bootstrap/app.php` 파일의 `web` 미들웨어 그룹에 추가하세요:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` 미들웨어는 미들웨어 스택의 마지막에 위치하도록 해야 합니다.

이 미들웨어는 응답에 `laravel_token` 쿠키(JWT 암호화)를 첨부합니다. Passport는 이 쿠키(JWT)를 사용하여 자바스크립트 앱의 API 요청 인증을 처리합니다. JWT의 수명은 `session.lifetime` 설정값과 같습니다. 브라우저가 이 쿠키를 자동으로 전송하므로, 개발자는 별도로 액세스 토큰을 명시하지 않아도 됩니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 커스터마이징

필요하다면, `Passport::cookie` 메서드로 `laravel_token` 쿠키명을 변경할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 클래스의 `boot`에서 설정합니다:

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

이 인증 방식 사용 시, 요청에 유효한 CSRF 토큰 헤더가 포함되어야 합니다. 기본 Laravel 자바스크립트 스캐폴딩 및 모든 스타터 키트는 [Axios](https://github.com/axios/axios)를 내장하고 있으며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 사용해 자동으로 같은 도메인 요청마다 `X-XSRF-TOKEN` 헤더를 보냅니다.

> [!NOTE]
> 만약 `X-CSRF-TOKEN` 헤더를 사용하고 싶다면, 암호화되지 않은 `csrf_token()`의 값을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰과 리프레시 토큰이 발급되는 시점에 이벤트를 발생시킵니다. [이벤트를 리스닝](/docs/master/events)하여 데이터베이스의 기타 액세스 토큰을 정리하거나 취소 등의 작업을 수행할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                       |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드를 사용하면 인증 사용자와 해당 스코프를 테스트 세션에 명시할 수 있습니다. 첫 번째 인자는 사용자 인스턴스, 두 번째 인자는 부여할 스코프 배열입니다:

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

Passport의 `actingAsClient` 메서드를 사용하면 인증된 클라이언트와 해당 스코프를 지정할 수 있습니다. 첫 번째 인자는 클라이언트 인스턴스, 두 번째는 부여할 스코프 배열입니다:

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
