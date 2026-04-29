# Laravel Passport (Laravel Passport)

- [소개](#introduction)
    - [Passport 또는 Sanctum?](#passport-or-sanctum)
- [설치](#installation)
    - [Passport 배포](#deploying-passport)
    - [Passport 업그레이드](#upgrading-passport)
- [설정](#configuration)
    - [토큰 수명](#token-lifetimes)
    - [기본 모델 재정의](#overriding-default-models)
    - [라우트 재정의](#overriding-routes)
- [인가 코드 승인 방식](#authorization-code-grant)
    - [클라이언트 관리](#managing-clients)
    - [토큰 요청](#requesting-tokens)
    - [토큰 관리](#managing-tokens)
    - [토큰 갱신](#refreshing-tokens)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 정리](#purging-tokens)
- [PKCE를 사용하는 인가 코드 승인 방식](#code-grant-pkce)
    - [클라이언트 생성](#creating-a-auth-pkce-grant-client)
    - [토큰 요청](#requesting-auth-pkce-grant-tokens)
- [디바이스 인가 승인 방식](#device-authorization-grant)
    - [디바이스 코드 승인 클라이언트 생성](#creating-a-device-authorization-grant-client)
    - [토큰 요청](#requesting-device-authorization-grant-tokens)
- [비밀번호 승인 방식](#password-grant)
    - [비밀번호 승인 클라이언트 생성](#creating-a-password-grant-client)
    - [토큰 요청](#requesting-password-grant-tokens)
    - [모든 스코프 요청](#requesting-all-scopes)
    - [사용자 공급자 사용자 정의](#customizing-the-user-provider)
    - [사용자 이름 필드 사용자 정의](#customizing-the-username-field)
    - [비밀번호 검증 사용자 정의](#customizing-the-password-validation)
- [암묵적 승인 방식](#implicit-grant)
- [클라이언트 자격 증명 승인 방식](#client-credentials-grant)
- [개인 액세스 토큰](#personal-access-tokens)
    - [개인 액세스 클라이언트 생성](#creating-a-personal-access-client)
    - [사용자 공급자 사용자 정의](#customizing-the-user-provider-for-pat)
    - [개인 액세스 토큰 관리](#managing-personal-access-tokens)
- [라우트 보호](#protecting-routes)
    - [Middleware를 통해](#via-middleware)
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

[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 완전한 OAuth2 서버 구현을 몇 분 안에 제공합니다. Passport는 Andy Millington과 Simon Hamp가 유지보수하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!NOTE]
> 이 문서는 독자가 이미 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 잘 모른다면 계속 진행하기 전에 OAuth2의 일반적인 [용어](https://oauth2.thephpleague.com/terminology/)와 기능을 먼저 익혀 보시기 바랍니다.

<a name="passport-or-sanctum"></a>
### Passport 또는 Sanctum?

시작하기 전에 애플리케이션에 Laravel Passport가 더 적합한지, 아니면 [Laravel Sanctum](/docs/master/sanctum)이 더 적합한지 판단해 보는 것이 좋습니다. 애플리케이션에서 OAuth2 지원이 반드시 필요하다면 Laravel Passport를 사용해야 합니다.

하지만 단일 페이지 애플리케이션, 모바일 애플리케이션을 인증하거나 API 토큰을 발급하려는 경우에는 [Laravel Sanctum](/docs/master/sanctum)을 사용해야 합니다. Laravel Sanctum은 OAuth2를 지원하지 않지만, 훨씬 더 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` Artisan 명령어로 Laravel Passport를 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

이 명령어는 애플리케이션이 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 테이블을 만들기 위한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 안전한 액세스 토큰을 생성하는 데 필요한 암호화 키도 생성합니다.

`install:api` 명령어를 실행한 뒤, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` trait와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가합니다. 이 trait는 인증된 사용자의 토큰과 스코프를 검사할 수 있는 몇 가지 헬퍼 메서드를 모델에 제공합니다.

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

마지막으로 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 guard를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 들어오는 API 요청을 인증할 때 애플리케이션이 Passport의 `TokenGuard`를 사용하도록 지시합니다.

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
### Passport 배포

Passport를 애플리케이션 서버에 처음 배포할 때는 보통 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 관리에 포함하지 않습니다.

```shell
php artisan passport:keys
```

필요하다면 Passport의 키를 불러올 경로를 정의할 수 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

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
#### 환경에서 키 불러오기

또는 `vendor:publish` Artisan 명령어를 사용하여 Passport의 설정 파일을 게시할 수 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

설정 파일을 게시한 뒤에는 암호화 키를 환경 변수로 정의하여 애플리케이션에서 불러올 수 있습니다.

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
### Passport 업그레이드

Passport의 새로운 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 Passport는 1년 뒤 만료되는 장기 액세스 토큰을 발급합니다. 토큰 수명을 더 길게 또는 더 짧게 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

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
> Passport의 데이터베이스 테이블에 있는 `expires_at` 컬럼은 읽기 전용이며 표시 용도로만 사용됩니다. Passport는 토큰을 발급할 때 만료 정보를 서명되고 암호화된 토큰 안에 저장합니다. 토큰을 무효화해야 한다면 해당 토큰을 [폐기](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Passport 내부에서 사용하는 모델을 확장하려면 직접 모델을 정의하고 해당 Passport 모델을 상속하면 됩니다.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

모델을 정의한 뒤에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 정의 모델을 사용하도록 지정할 수 있습니다. 일반적으로 사용자 정의 모델에 대한 정보는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 Passport에 알려야 합니다.

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
### 라우트 재정의

때로는 Passport가 정의한 라우트를 사용자 정의하고 싶을 수 있습니다. 이를 위해서는 먼저 애플리케이션의 `AppServiceProvider`에 있는 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 등록하는 라우트를 무시해야 합니다.

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

그런 다음 [Passport의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php` 파일로 복사하고 원하는 대로 수정할 수 있습니다.

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
## 인가 코드 승인 방식 (Authorization Code Grant)

인가 코드를 통해 OAuth2를 사용하는 방식은 대부분의 개발자에게 가장 익숙한 OAuth2 사용 방식입니다. 인가 코드를 사용할 때 클라이언트 애플리케이션은 사용자를 여러분의 서버로 리디렉션하고, 사용자는 클라이언트에 액세스 토큰을 발급하는 요청을 승인하거나 거부합니다.

시작하려면 Passport가 "authorization" 뷰를 어떻게 반환해야 하는지 알려 주어야 합니다.

인가 뷰의 모든 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 사용하여 사용자 정의할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::authorizationView('auth.oauth.authorize');

    // By providing a closure...
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

Passport는 이 뷰를 반환하는 `/oauth/authorize` 라우트를 자동으로 정의합니다. `auth.oauth.authorize` 템플릿에는 인가를 승인하기 위해 `passport.authorizations.approve` 라우트로 `POST` 요청을 보내는 폼과, 인가를 거부하기 위해 `passport.authorizations.deny` 라우트로 `DELETE` 요청을 보내는 폼이 포함되어야 합니다. `passport.authorizations.approve` 및 `passport.authorizations.deny` 라우트는 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="managing-clients"></a>
### 클라이언트 관리

애플리케이션의 API와 상호작용해야 하는 애플리케이션을 만드는 개발자는 "client"를 생성하여 자신의 애플리케이션을 여러분의 애플리케이션에 등록해야 합니다. 일반적으로 여기에는 해당 애플리케이션의 이름과, 사용자가 인가 요청을 승인한 뒤 여러분의 애플리케이션이 리디렉션할 URI를 제공하는 과정이 포함됩니다.

<a name="managing-first-party-clients"></a>
#### 퍼스트 파티 클라이언트

클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 퍼스트 파티 클라이언트를 생성하거나 OAuth2 기능을 테스트할 때 사용할 수 있습니다. `passport:client` 명령어를 실행하면 Passport가 클라이언트에 대한 추가 정보를 물어보고 클라이언트 ID와 secret을 제공합니다.

```shell
php artisan passport:client
```

클라이언트에 여러 리디렉션 URI를 허용하려면 `passport:client` 명령어가 URI를 물어볼 때 쉼표로 구분된 목록을 지정하면 됩니다. 쉼표가 포함된 URI는 URI 인코딩해야 합니다.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
#### 서드 파티 클라이언트

애플리케이션의 사용자는 `passport:client` 명령어를 사용할 수 없으므로, 특정 사용자를 위한 클라이언트를 등록하려면 `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용할 수 있습니다.

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// Creating an OAuth app client that belongs to the given user...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// Retrieving all the OAuth app clients that belong to the user...
$clients = $user->oauthApps()->get();
```

`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게 클라이언트 ID로 `$client->id`를, 클라이언트 secret으로 `$client->plainSecret`을 표시할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 인가를 위해 리디렉션하기

클라이언트가 생성되면 개발자는 클라이언트 ID와 secret을 사용하여 여러분의 애플리케이션에서 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 사용하는 쪽 애플리케이션은 다음과 같이 여러분의 애플리케이션의 `/oauth/authorize` 라우트로 리디렉션 요청을 보내야 합니다.

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
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

`prompt` 파라미터는 Passport 애플리케이션의 인증 동작을 지정하는 데 사용할 수 있습니다.

`prompt` 값이 `none`이면 사용자가 Passport 애플리케이션에서 아직 인증되어 있지 않은 경우 Passport는 항상 인증 오류를 발생시킵니다. 값이 `consent`이면 요청된 모든 스코프가 이전에 사용하는 쪽 애플리케이션에 이미 허용되었더라도 Passport는 항상 인가 승인 화면을 표시합니다. 값이 `login`이면 사용자가 이미 기존 세션을 가지고 있더라도 Passport 애플리케이션은 항상 사용자에게 애플리케이션에 다시 로그인하도록 요구합니다.

`prompt` 값이 제공되지 않으면, 요청된 스코프에 대해 사용자가 사용하는 쪽 애플리케이션의 접근을 이전에 승인하지 않은 경우에만 인가를 요청받게 됩니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 이미 Passport에 의해 정의되어 있다는 점을 기억하세요. 이 라우트를 직접 정의할 필요는 없습니다.

<a name="approving-the-request"></a>
#### 요청 승인하기

인가 요청을 받으면 Passport는 `prompt` 파라미터 값이 있는 경우 그 값에 따라 자동으로 응답하며, 사용자가 인가 요청을 승인하거나 거부할 수 있도록 템플릿을 표시할 수 있습니다. 사용자가 요청을 승인하면 사용하는 쪽 애플리케이션이 지정한 `redirect_uri`로 다시 리디렉션됩니다. `redirect_uri`는 클라이언트를 생성할 때 지정한 `redirect` URL과 일치해야 합니다.

때로는 퍼스트 파티 클라이언트를 인가할 때처럼 인가 프롬프트를 건너뛰고 싶을 수 있습니다. 이를 위해 [ `Client` 모델을 확장](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의할 수 있습니다. `skipsAuthorization`가 `true`를 반환하면, 사용하는 쪽 애플리케이션이 인가를 위해 리디렉션할 때 `prompt` 파라미터를 명시적으로 설정하지 않은 한 클라이언트가 승인되고 사용자는 즉시 `redirect_uri`로 다시 리디렉션됩니다.

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
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
#### 인가 코드를 액세스 토큰으로 변환하기

사용자가 인가 요청을 승인하면 사용하는 쪽 애플리케이션으로 다시 리디렉션됩니다. consumer는 먼저 리디렉션 전에 저장해 둔 값과 `state` 파라미터를 비교하여 검증해야 합니다. state 파라미터가 일치하면 consumer는 액세스 토큰을 요청하기 위해 여러분의 애플리케이션에 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인했을 때 여러분의 애플리케이션이 발급한 인가 코드가 포함되어야 합니다.
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

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 초 단위 시간이 들어 있습니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로 `/oauth/token` 라우트도 Passport가 자동으로 정의합니다. 이 라우트를 직접 정의할 필요는 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

`Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하여 사용자가 인가한 토큰을 조회할 수 있습니다. 예를 들어, 사용자가 서드파티 애플리케이션과의 연결 상태를 확인할 수 있는 대시보드를 제공할 때 사용할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Retrieving all of the valid tokens for the user...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// Retrieving all the user's connections to third-party OAuth app clients...
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
### 토큰 갱신

애플리케이션이 수명이 짧은 액세스 토큰을 발급하는 경우, 사용자는 액세스 토큰이 발급될 때 함께 제공된 리프레시 토큰을 통해 액세스 토큰을 갱신해야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 초 단위 시간이 들어 있습니다.

<a name="revoking-tokens"></a>
### 토큰 무효화

`Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용하여 토큰을 무효화할 수 있습니다. 토큰의 리프레시 토큰은 `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용하여 무효화할 수 있습니다.

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Revoke an access token...
$token->revoke();

// Revoke the token's refresh token...
$token->refreshToken?->revoke();

// Revoke all of the user's tokens...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
### 토큰 정리

토큰이 무효화되었거나 만료되면 데이터베이스에서 제거하고 싶을 수 있습니다. Passport에 포함된 `passport:purge` Artisan 명령어가 이 작업을 대신 처리해 줍니다.

```shell
# Purge revoked and expired tokens, auth codes, and device codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens, auth codes, and device codes...
php artisan passport:purge --revoked

# Only purge expired tokens, auth codes, and device codes...
php artisan passport:purge --expired
```

애플리케이션의 `routes/console.php` 파일에서 [스케줄 작업](/docs/master/scheduling)을 설정하여 일정에 따라 토큰을 자동으로 정리할 수도 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
## PKCE를 사용하는 Authorization Code Grant (Authorization Code Grant With PKCE)

"Proof Key for Code Exchange"(PKCE)를 사용하는 Authorization Code grant는 싱글 페이지 애플리케이션이나 모바일 애플리케이션이 API에 접근할 수 있도록 인증하는 안전한 방법입니다. 클라이언트 시크릿을 비밀로 안전하게 저장할 수 있다고 보장할 수 없거나, 공격자가 인가 코드를 가로채는 위협을 완화해야 할 때 이 grant를 사용해야 합니다. 인가 코드를 액세스 토큰으로 교환할 때 클라이언트 시크릿 대신 "code verifier"와 "code challenge"의 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

애플리케이션이 PKCE를 사용하는 Authorization Code grant로 토큰을 발급하려면 먼저 PKCE가 활성화된 클라이언트를 생성해야 합니다. `--public` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### Code Verifier와 Code Challenge

이 인가 grant는 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰을 요청하기 위해 code verifier와 code challenge의 조합을 생성해야 합니다.

code verifier는 [RFC 7636 명세](https://tools.ietf.org/html/rfc7636)에 정의된 것처럼 문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함하는 43자 이상 128자 이하의 무작위 문자열이어야 합니다.

code challenge는 URL과 파일명에 안전한 문자를 사용하는 Base64 인코딩 문자열이어야 합니다. 끝에 붙는 `'='` 문자는 제거해야 하며, 줄바꿈, 공백 또는 다른 추가 문자가 포함되어서는 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 인가를 위한 리다이렉트

클라이언트를 생성한 후에는 클라이언트 ID와 생성된 code verifier 및 code challenge를 사용하여 애플리케이션에 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 소비하는 애플리케이션은 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다.

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
#### 인가 코드를 액세스 토큰으로 변환

사용자가 인가 요청을 승인하면 소비하는 애플리케이션으로 다시 리다이렉트됩니다. 표준 Authorization Code Grant와 마찬가지로, 소비자는 리다이렉트 전에 저장해 둔 값과 `state` 파라미터를 비교하여 검증해야 합니다.

state 파라미터가 일치하면 소비자는 액세스 토큰을 요청하기 위해 애플리케이션에 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인했을 때 애플리케이션이 발급한 인가 코드와, 처음에 생성한 code verifier가 함께 포함되어야 합니다.

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
## Device Authorization Grant (Device Authorization Grant)

OAuth2 device authorization grant를 사용하면 TV나 게임 콘솔처럼 브라우저가 없거나 입력이 제한된 디바이스가 "device code"를 교환하여 액세스 토큰을 얻을 수 있습니다. device flow를 사용할 때 디바이스 클라이언트는 사용자에게 컴퓨터나 스마트폰 같은 보조 디바이스를 사용하도록 안내하고, 사용자가 서버에 접속해 제공된 "user code"를 입력한 뒤 접근 요청을 승인하거나 거부하게 합니다.

시작하려면 Passport에 "user code" 뷰와 "authorization" 뷰를 어떻게 반환할지 알려줘야 합니다.

인가 뷰의 모든 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 사용하여 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // By providing a closure...
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

Passport는 이러한 뷰를 반환하는 라우트를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 포함되어야 합니다. `passport.device.authorizations.authorize` 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

`auth.oauth.device.authorize` 템플릿에는 인가를 승인하기 위해 `passport.device.authorizations.approve` 라우트로 POST 요청을 보내는 폼과, 인가를 거부하기 위해 `passport.device.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어야 합니다. `passport.device.authorizations.approve` 및 `passport.device.authorizations.deny` 라우트는 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### Device Authorization Grant 클라이언트 생성

애플리케이션이 device authorization grant로 토큰을 발급하려면 먼저 device flow가 활성화된 클라이언트를 생성해야 합니다. `--device` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다. 이 명령어는 device flow가 활성화된 first-party 클라이언트를 생성하고 클라이언트 ID와 시크릿을 제공합니다.

```shell
php artisan passport:client --device
```

또한 `ClientRepository` 클래스의 `createDeviceAuthorizationGrantClient` 메서드를 사용하여 지정된 사용자에게 속한 서드파티 클라이언트를 등록할 수 있습니다.

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
### 토큰 요청

<a name="device-code"></a>
#### Device Code 요청

클라이언트가 생성되면 개발자는 클라이언트 ID를 사용하여 애플리케이션에 device code를 요청할 수 있습니다. 먼저, 소비하는 디바이스는 device code를 요청하기 위해 애플리케이션의 `/oauth/device/code` 라우트로 `POST` 요청을 보내야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 device code가 만료되기까지 남은 초 단위 시간이 들어 있습니다. `interval` 속성에는 소비하는 디바이스가 rate limit 오류를 피하기 위해 `/oauth/token` 라우트를 폴링할 때 요청 사이에 기다려야 하는 초 단위 시간이 들어 있습니다.

> [!NOTE]
> 기억하세요. `/oauth/device/code` 라우트는 이미 Passport가 정의합니다. 이 라우트를 직접 정의할 필요는 없습니다.

<a name="user-code"></a>
#### Verification URI와 User Code 표시

device code 요청을 받은 후, 소비하는 디바이스는 사용자에게 다른 디바이스를 사용하여 제공된 `verification_uri`에 방문하고 `user_code`를 입력해서 인가 요청을 승인하도록 안내해야 합니다.

<a name="polling-token-request"></a>
#### 토큰 요청 폴링

사용자가 별도의 디바이스를 사용하여 접근을 승인하거나 거부하므로, 소비하는 디바이스는 사용자가 요청에 응답했는지 확인하기 위해 애플리케이션의 `/oauth/token` 라우트를 폴링해야 합니다. 소비하는 디바이스는 rate limit 오류를 피하기 위해 device code를 요청할 때 JSON 응답으로 제공된 최소 폴링 `interval`을 사용해야 합니다.

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

사용자가 인가 요청을 승인했다면, 이 요청은 `access_token`, `refresh_token`, `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 초 단위 시간이 들어 있습니다.

<a name="password-grant"></a>
## Password Grant (Password Grant)

> [!WARNING]
> 더 이상 password grant 토큰 사용을 권장하지 않습니다. 대신 [OAuth2 Server가 현재 권장하는 grant 유형](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

OAuth2 password grant를 사용하면 모바일 애플리케이션 같은 다른 first-party 클라이언트가 이메일 주소 / 사용자 이름과 비밀번호를 사용하여 액세스 토큰을 얻을 수 있습니다. 이를 통해 사용자가 전체 OAuth2 authorization code 리다이렉트 플로우를 거치지 않아도 first-party 클라이언트에 액세스 토큰을 안전하게 발급할 수 있습니다.

password grant를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출합니다.

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

애플리케이션이 password grant로 토큰을 발급하려면 먼저 password grant 클라이언트를 생성해야 합니다. `--password` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

grant를 활성화하고 password grant 클라이언트를 생성한 후에는 사용자의 이메일 주소와 비밀번호를 포함하여 `/oauth/token` 라우트로 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이 라우트는 이미 Passport가 등록하므로 직접 정의할 필요가 없습니다. 요청이 성공하면 서버의 JSON 응답에서 `access_token`과 `refresh_token`을 받게 됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```
> [!NOTE]
> 액세스 토큰은 기본적으로 수명이 깁니다. 그러나 필요한 경우 [최대 액세스 토큰 수명](#configuration)을 자유롭게 구성할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 스코프 요청

password grant 또는 client credentials grant를 사용할 때, 애플리케이션에서 지원하는 모든 스코프에 대해 토큰을 인가하고 싶을 수 있습니다. 이 경우 `*` 스코프를 요청하면 됩니다. `*` 스코프를 요청하면 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` grant를 사용해 발급된 토큰에만 할당할 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 둘 이상의 [인증 사용자 프로바이더](/docs/master/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 password grant 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 제공한 프로바이더 이름은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 그런 다음 [미들웨어를 사용해 라우트를 보호](#multiple-authentication-guards)하여, guard에 지정된 프로바이더의 사용자만 인가되도록 보장할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자 이름 필드 커스터마이징

password grant를 사용해 인증할 때 Passport는 인증 가능한 모델의 `email` 속성을 "username"으로 사용합니다. 그러나 모델에 `findForPassport` 메서드를 정의하여 이 동작을 커스터마이징할 수 있습니다.

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
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

password grant를 사용해 인증할 때 Passport는 주어진 비밀번호를 검증하기 위해 모델의 `password` 속성을 사용합니다. 모델에 `password` 속성이 없거나 비밀번호 검증 로직을 커스터마이징하고 싶다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

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
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
## 암묵적 Grant (Implicit Grant)

> [!WARNING]
> 더 이상 implicit grant 토큰 사용을 권장하지 않습니다. 대신 [OAuth2 Server에서 현재 권장하는 grant 타입](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

implicit grant는 authorization code grant와 비슷하지만, authorization code를 교환하지 않고 토큰이 클라이언트에 반환됩니다. 이 grant는 클라이언트 자격 증명을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 가장 흔히 사용됩니다. 이 grant를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

애플리케이션이 implicit grant를 통해 토큰을 발급하려면 먼저 implicit grant 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--implicit` 옵션을 사용하면 됩니다.

```shell
php artisan passport:client --implicit
```

grant가 활성화되고 implicit 클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용해 애플리케이션에 액세스 토큰을 요청할 수 있습니다. 토큰을 사용하는 애플리케이션은 다음과 같이 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다.

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
> `/oauth/authorize` 라우트는 이미 Passport에서 정의합니다. 이 라우트를 직접 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## Client Credentials Grant (Client Credentials Grant)

client credentials grant는 머신 간 인증에 적합합니다. 예를 들어, API를 통해 유지보수 작업을 수행하는 스케줄 작업에서 이 grant를 사용할 수 있습니다.

애플리케이션이 client credentials grant를 통해 토큰을 발급하려면 먼저 client credentials grant 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어의 `--client` 옵션을 사용하면 됩니다.

```shell
php artisan passport:client --client
```

다음으로, 라우트에 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 할당합니다.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

특정 스코프로 라우트 접근을 제한하려면 필요한 스코프 목록을 `using` 메서드에 전달할 수 있습니다.

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

<a name="retrieving-tokens"></a>
### 토큰 가져오기

이 grant 타입을 사용해 토큰을 가져오려면 `oauth/token` 엔드포인트로 요청을 보냅니다.

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

때로는 사용자가 일반적인 authorization code 리다이렉트 흐름을 거치지 않고 자신에게 액세스 토큰을 발급하고 싶을 수 있습니다. 애플리케이션의 UI를 통해 사용자가 직접 토큰을 발급할 수 있도록 하면, 사용자가 API를 실험해 볼 수 있게 하거나 일반적으로 액세스 토큰을 발급하는 더 간단한 방법으로 활용할 수 있습니다.

> [!NOTE]
> 애플리케이션에서 Passport를 주로 개인 액세스 토큰 발급 용도로 사용한다면, API 액세스 토큰 발급을 위한 Laravel의 가벼운 first-party 라이브러리인 [Laravel Sanctum](/docs/master/sanctum) 사용을 고려하십시오.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

애플리케이션이 개인 액세스 토큰을 발급하려면 먼저 개인 액세스 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어에 `--personal` 옵션을 사용해 실행하면 됩니다. 이미 `passport:install` 명령어를 실행했다면 이 명령어를 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 프로바이더 커스터마이징

애플리케이션에서 둘 이상의 [인증 사용자 프로바이더](/docs/master/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 personal access grant 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 제공한 프로바이더 이름은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 그런 다음 [미들웨어를 사용해 라우트를 보호](#multiple-authentication-guards)하여, guard에 지정된 프로바이더의 사용자만 인가되도록 보장할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성한 후에는 `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용하여 지정한 사용자에게 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인수로 토큰 이름을 받고, 두 번째 인수로 선택 사항인 [스코프](#token-scopes) 배열을 받습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Creating a token without scopes...
$token = $user->createToken('My Token')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// Creating a token with all scopes...
$token = $user->createToken('My Token', ['*'])->accessToken;

// Retrieving all the valid personal access tokens that belong to the user...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
## 라우트 보호 (Protecting Routes)

<a name="via-middleware"></a>
### 미들웨어를 통해

Passport에는 들어오는 요청의 액세스 토큰을 검증하는 [인증 guard](/docs/master/authentication#adding-custom-guards)가 포함되어 있습니다. `api` guard가 `passport` 드라이버를 사용하도록 설정한 후에는, 유효한 액세스 토큰이 필요한 모든 라우트에 `auth:api` 미들웨어만 지정하면 됩니다.

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```

> [!WARNING]
> [client credentials grant](#client-credentials-grant)를 사용하는 경우, 라우트를 보호할 때 `auth:api` 미들웨어 대신 [`Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 여러 인증 Guard

애플리케이션에서 완전히 다른 Eloquent 모델을 사용할 수도 있는 여러 유형의 사용자를 인증한다면, 애플리케이션의 각 사용자 프로바이더 유형마다 guard 설정을 정의해야 할 가능성이 높습니다. 이렇게 하면 특정 사용자 프로바이더를 대상으로 하는 요청을 보호할 수 있습니다. 예를 들어, `config/auth.php` 설정 파일에 다음 guard 설정이 있다고 가정해 보겠습니다.

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

다음 라우트는 들어오는 요청을 인증하기 위해 `customers` 사용자 프로바이더를 사용하는 `api-customers` guard를 활용합니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 사용하는 방법에 대한 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [password grant 문서](#customizing-the-user-provider)를 참고하십시오.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport로 보호되는 라우트를 호출할 때, 애플리케이션의 API 소비자는 요청의 `Authorization` 헤더에 자신의 액세스 토큰을 `Bearer` 토큰으로 지정해야 합니다. 예를 들어 `Http` Facade를 사용할 때는 다음과 같습니다.

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

스코프를 사용하면 API 클라이언트가 계정에 접근하기 위한 인가를 요청할 때 특정 권한 집합을 요청할 수 있습니다. 예를 들어 전자상거래 애플리케이션을 만들고 있다면, 모든 API 소비자에게 주문 생성 권한이 필요하지는 않습니다. 대신 소비자가 주문 배송 상태에 접근하기 위한 인가만 요청할 수 있도록 허용할 수 있습니다. 즉, 스코프를 통해 애플리케이션 사용자는 서드파티 애플리케이션이 자신을 대신해 수행할 수 있는 작업을 제한할 수 있습니다.

<a name="defining-scopes"></a>
### 스코프 정의

애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용하여 API의 스코프를 정의할 수 있습니다. `tokensCan` 메서드는 스코프 이름과 스코프 설명으로 이루어진 배열을 받습니다. 스코프 설명은 원하는 어떤 내용이든 될 수 있으며, 인가 승인 화면에서 사용자에게 표시됩니다.

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
### 기본 스코프

클라이언트가 특정 스코프를 요청하지 않는 경우, `defaultScopes` 메서드를 사용하여 Passport 서버가 토큰에 기본 스코프를 첨부하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

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
### 토큰에 스코프 할당

<a name="when-requesting-authorization-codes"></a>
#### Authorization Code를 요청할 때

authorization code grant를 사용해 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터는 공백으로 구분된 스코프 목록이어야 합니다.

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
#### 개인 액세스 토큰을 발급할 때

`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급하는 경우, 원하는 스코프 배열을 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
### 스코프 확인

Passport에는 들어오는 요청이 지정된 스코프를 부여받은 토큰으로 인증되었는지 검증하는 데 사용할 수 있는 두 가지 미들웨어가 포함되어 있습니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어를 라우트에 할당하여, 들어오는 요청의 액세스 토큰이 나열된 모든 스코프를 가지고 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
#### 스코프 중 하나라도 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어를 라우트에 할당하여, 들어오는 요청의 액세스 토큰이 나열된 스코프 중 *최소 하나*를 가지고 있는지 검증할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```
<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 스코프 확인

액세스 토큰으로 인증된 요청이 애플리케이션에 들어온 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용하여 토큰에 특정 스코프가 있는지 확인할 수 있습니다:

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

`scopeIds` 메서드는 정의된 모든 ID / 이름의 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다:

```php
Passport::scopes();
```

`scopesFor` 메서드는 주어진 ID / 이름과 일치하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

주어진 스코프가 정의되어 있는지는 `hasScope` 메서드를 사용하여 확인할 수 있습니다:

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

API를 만들 때 자체 API를 JavaScript 애플리케이션에서 사용할 수 있으면 매우 유용합니다. 이러한 API 개발 방식은 외부에 공개하는 것과 동일한 API를 자체 애플리케이션에서도 사용할 수 있게 해줍니다. 동일한 API를 웹 애플리케이션, 모바일 애플리케이션, 타사 애플리케이션, 그리고 다양한 패키지 매니저에 배포할 수 있는 SDK에서 사용할 수 있습니다.

일반적으로 JavaScript 애플리케이션에서 API를 사용하려면 액세스 토큰을 애플리케이션에 직접 전달하고, 애플리케이션으로 보내는 각 요청마다 해당 토큰을 함께 전달해야 합니다. 하지만 Passport에는 이 작업을 대신 처리할 수 있는 Middleware가 포함되어 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `CreateFreshApiToken` Middleware를 `web` Middleware 그룹에 추가하기만 하면 됩니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` Middleware가 Middleware 스택에서 마지막 Middleware로 나열되도록 해야 합니다.

이 Middleware는 나가는 응답에 `laravel_token` 쿠키를 첨부합니다. 이 쿠키에는 Passport가 JavaScript 애플리케이션의 API 요청을 인증하는 데 사용할 암호화된 JWT가 들어 있습니다. JWT의 수명은 `session.lifetime` 설정 값과 같습니다. 이제 브라우저가 이후의 모든 요청에 쿠키를 자동으로 전송하므로, 액세스 토큰을 명시적으로 전달하지 않고도 애플리케이션의 API에 요청할 수 있습니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 사용자 정의

필요하다면 `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키의 이름을 사용자 정의할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다:

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

이 인증 방식을 사용할 때는 요청에 유효한 CSRF 토큰 헤더가 포함되도록 해야 합니다. 스켈레톤 애플리케이션 및 모든 스타터 킷에 포함된 기본 Laravel JavaScript 스캐폴딩에는 [Axios](https://github.com/axios/axios) 인스턴스가 포함되어 있으며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 사용하여 same-origin 요청에 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!NOTE]
> `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 보내기로 선택한 경우, `csrf_token()`에서 제공하는 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

Passport는 액세스 토큰과 리프레시 토큰을 발급할 때 이벤트를 발생시킵니다. 이러한 이벤트를 [수신](/docs/master/events)하여 데이터베이스의 다른 액세스 토큰을 정리하거나 폐기할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## 테스트 (Testing)

Passport의 `actingAs` 메서드는 현재 인증된 사용자와 해당 사용자의 스코프를 지정하는 데 사용할 수 있습니다. `actingAs` 메서드에 전달되는 첫 번째 인수는 사용자 인스턴스이고, 두 번째 인수는 사용자의 토큰에 부여할 스코프 배열입니다:

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

Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 해당 클라이언트의 스코프를 지정하는 데 사용할 수 있습니다. `actingAsClient` 메서드에 전달되는 첫 번째 인수는 클라이언트 인스턴스이고, 두 번째 인수는 클라이언트의 토큰에 부여할 스코프 배열입니다:

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
