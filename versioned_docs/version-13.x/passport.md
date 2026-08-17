<!-- # Laravel Passport -->
# Laravel Passport

- [Introduction](#introduction)
    - [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
    - [Overriding Routes](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Managing Tokens](#managing-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [Creating the Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Creating a Device Code Grant Client](#creating-a-device-authorization-grant-client)
    - [Requesting Tokens](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Creating a Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing the User Provider](#customizing-the-user-provider)
    - [Customizing the Username Field](#customizing-the-username-field)
    - [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating a Personal Access Client](#creating-a-personal-access-client)
    - [Customizing the User Provider](#customizing-the-user-provider-for-pat)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [SPA Authentication](#spa-authentication)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp. -->
[Laravel Passport](https://github.com/laravel/passport)는 Laravel 애플리케이션에 완전한 OAuth2 서버 구현을 몇 분 안에 제공합니다. Passport는 Andy Millington과 Simon Hamp가 관리하는 [League OAuth2 server](https://github.com/thephpleague/oauth2-server)를 기반으로 만들어졌습니다.

> [!NOTE]
> 이 문서는 사용자가 이미 OAuth2에 익숙하다고 가정합니다. OAuth2에 대해 전혀 모른다면 계속 진행하기 전에 OAuth2의 일반적인 [terminology](https://oauth2.thephpleague.com/terminology/)와 기능을 먼저 익혀 두는 것이 좋습니다.

<a name="passport-or-sanctum"></a>
<!-- ### Passport or Sanctum? -->
### Passport or Sanctum?

<!-- Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/13.x/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport. -->
시작하기 전에 애플리케이션에 Laravel Passport가 더 적합한지, 아니면 [Laravel Sanctum](/docs/13.x/sanctum)이 더 적합한지 판단해 볼 수 있습니다. 애플리케이션에서 반드시 OAuth2를 지원해야 한다면 Laravel Passport를 사용해야 합니다.

<!-- However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/13.x/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience. -->
하지만 단일 페이지 애플리케이션, 모바일 애플리케이션을 인증하거나 API 토큰을 발급하려는 경우에는 [Laravel Sanctum](/docs/13.x/sanctum)을 사용해야 합니다. Laravel Sanctum은 OAuth2를 지원하지 않습니다. 대신 훨씬 더 단순한 API 인증 개발 경험을 제공합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Laravel Passport via the `install:api` Artisan command: -->
`install:api` Artisan 명령어를 통해 Laravel Passport를 설치할 수 있습니다.

```shell
php artisan install:api --passport
```

<!-- This command will publish and run the database migrations necessary for creating the tables your application needs to store OAuth2 clients and access tokens. The command will also create the encryption keys required to generate secure access tokens. -->
이 명령어는 애플리케이션이 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 테이블을 만들기 위한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 보안 액세스 토큰을 생성하는 데 필요한 암호화 키도 생성합니다.

<!-- After running the `install:api` command, add the `Laravel\Passport\HasApiTokens` trait and `Laravel\Passport\Contracts\OAuthenticatable` interface to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes: -->
`install:api` 명령어를 실행한 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` trait와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가합니다. 이 trait는 인증된 사용자의 토큰과 스코프를 확인할 수 있는 몇 가지 헬퍼 메서드를 모델에 제공합니다.

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

<!-- Finally, in your application's `config/auth.php` configuration file, you should define an `api` authentication guard and set the `driver` option to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests: -->
마지막으로 애플리케이션의 `config/auth.php` 설정 파일에서 `api` 인증 guard를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 애플리케이션은 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용합니다.

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
<!-- ### Deploying Passport -->
### Deploying Passport

<!-- When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control: -->
Passport를 애플리케이션 서버에 처음 배포할 때는 보통 `passport:keys` 명령어를 실행해야 합니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 관리에 포함하지 않습니다.

```shell
php artisan passport:keys
```

<!-- If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
필요하다면 Passport의 키를 불러올 경로를 정의할 수 있습니다. 이를 위해 `Passport::loadKeysFrom` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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
<!-- #### Loading Keys From the Environment -->
#### Loading Keys From the Environment

<!-- Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command: -->
또는 `vendor:publish` Artisan 명령어를 사용하여 Passport의 설정 파일을 게시할 수 있습니다.

```shell
php artisan vendor:publish --tag=passport-config
```

<!-- After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables: -->
설정 파일이 게시된 후에는 환경 변수로 정의하여 애플리케이션의 암호화 키를 불러올 수 있습니다.

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
<!-- ### Upgrading Passport -->
### Upgrading Passport

<!-- When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md). -->
Passport의 새로운 메이저 버전으로 업그레이드할 때는 [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="token-lifetimes"></a>
<!-- ### Token Lifetimes -->
### Token Lifetimes

<!-- By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
기본적으로 Passport는 1년 후에 만료되는 장기 액세스 토큰을 발급합니다. 더 길거나 짧은 토큰 수명을 설정하려면 `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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
> Passport 데이터베이스 테이블의 `expires_at` 컬럼은 읽기 전용이며 표시 목적으로만 사용됩니다. 토큰을 발급할 때 Passport는 만료 정보를 서명되고 암호화된 토큰 안에 저장합니다. 토큰을 무효화해야 한다면 [revoke it](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model: -->
직접 모델을 정의하고 해당 Passport 모델을 확장하여 Passport 내부에서 사용하는 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

<!-- After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 정의 모델을 사용하도록 지정할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Passport에 사용자 정의 모델을 알려야 합니다.

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
<!-- ### Overriding Routes -->
### Overriding Routes

<!-- Sometimes you may wish to customize the routes defined by Passport. To achieve this, you first need to ignore the routes registered by Passport by adding `Passport::ignoreRoutes` to the `register` method of your application's `AppServiceProvider`: -->
때로는 Passport가 정의한 라우트를 커스터마이징하고 싶을 수 있습니다. 이를 위해 먼저 애플리케이션의 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하여 Passport가 등록하는 라우트를 무시해야 합니다.

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

<!-- Then, you may copy the routes defined by Passport in [its routes file](https://github.com/laravel/passport/blob/master/routes/web.php) to your application's `routes/web.php` file and modify them to your liking: -->
그런 다음 [its routes file](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의된 라우트를 애플리케이션의 `routes/web.php` 파일로 복사하고 원하는 대로 수정할 수 있습니다.

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
<!-- ## Authorization Code Grant -->
## Authorization Code Grant

<!-- Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client. -->
인가 코드를 통해 OAuth2를 사용하는 방식은 대부분의 개발자에게 익숙한 OAuth2 사용 방식입니다. 인가 코드를 사용할 때 클라이언트 애플리케이션은 사용자를 사용자의 서버로 리디렉션하며, 사용자는 클라이언트에 액세스 토큰을 발급하는 요청을 승인하거나 거부합니다.

<!-- To get started, we need to instruct Passport how to return our "authorization" view. -->
시작하려면 Passport가 "authorization" 뷰를 어떻게 반환해야 하는지 지정해야 합니다.

<!-- All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
인가 뷰의 모든 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 사용하여 커스터마이징할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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

<!-- Passport will automatically define the `/oauth/authorize` route that returns this view. Your `auth.oauth.authorize` template should include a form that makes a POST request to the `passport.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.authorizations.deny` route to deny the authorization. The `passport.authorizations.approve` and `passport.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields. -->
Passport는 이 뷰를 반환하는 `/oauth/authorize` 라우트를 자동으로 정의합니다. `auth.oauth.authorize` 템플릿에는 인가를 승인하기 위해 `passport.authorizations.approve` 라우트로 POST 요청을 보내는 폼과, 인가를 거부하기 위해 `passport.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어야 합니다. `passport.authorizations.approve` 및 `passport.authorizations.deny` 라우트는 `state`, `client_id`, `auth_token` 필드를 필요로 합니다.

<a name="managing-clients"></a>
<!-- ### Managing Clients -->
### Managing Clients

<!-- Developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URI that your application can redirect to after users approve their request for authorization. -->
애플리케이션의 API와 상호작용해야 하는 애플리케이션을 만드는 개발자는 "client"를 생성하여 자신의 애플리케이션을 사용자의 애플리케이션에 등록해야 합니다. 일반적으로 이는 애플리케이션 이름과 사용자가 인가 요청을 승인한 후 사용자의 애플리케이션이 리디렉션할 URI를 제공하는 방식으로 이루어집니다.

<a name="managing-first-party-clients"></a>
<!-- #### First-Party Clients -->
#### First-Party Clients

<!-- The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create first-party clients or testing your OAuth2 functionality. When you run the `passport:client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret: -->
클라이언트를 생성하는 가장 간단한 방법은 `passport:client` Artisan 명령어를 사용하는 것입니다. 이 명령어는 퍼스트 파티 클라이언트를 생성하거나 OAuth2 기능을 테스트하는 데 사용할 수 있습니다. `passport:client` 명령어를 실행하면 Passport는 클라이언트에 대한 추가 정보를 입력하라고 요청하고, 클라이언트 ID와 secret을 제공합니다.

```shell
php artisan passport:client
```

<!-- If you would like to allow multiple redirect URIs for your client, you may specify them using a comma-delimited list when prompted for the URI by the `passport:client` command. Any URIs which contain commas should be URI encoded: -->
클라이언트에 여러 리디렉션 URI를 허용하려면 `passport:client` 명령어가 URI를 요청할 때 쉼표로 구분된 목록을 지정할 수 있습니다. 쉼표가 포함된 URI는 URI 인코딩해야 합니다.

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
<!-- #### Third-Party Clients -->
#### Third-Party Clients

<!-- Since your application's users will not be able to utilize the `passport:client` command, you may use `createAuthorizationCodeGrantClient` method of the `Laravel\Passport\ClientRepository` class to register a client for a given user: -->
애플리케이션의 사용자는 `passport:client` 명령어를 사용할 수 없으므로, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용하여 특정 사용자를 위한 클라이언트를 등록할 수 있습니다.

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

<!-- The `createAuthorizationCodeGrantClient` method returns an instance of `Laravel\Passport\Client`. You may display the `$client->id` as the client ID and `$client->plainSecret` as the client secret to the user. -->
`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client` 인스턴스를 반환합니다. 사용자에게 `$client->id`를 클라이언트 ID로, `$client->plainSecret`을 클라이언트 secret으로 표시할 수 있습니다.

<a name="requesting-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="requesting-tokens-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
클라이언트가 생성되면 개발자는 클라이언트 ID와 secret을 사용하여 애플리케이션에서 인가 코드와 액세스 토큰을 요청할 수 있습니다. 먼저 소비 애플리케이션은 다음과 같이 사용자의 애플리케이션의 `/oauth/authorize` 라우트로 리디렉션 요청을 보내야 합니다.

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

<!-- The `prompt` parameter may be used to specify the authentication behavior of the Passport application. -->
`prompt` 파라미터를 사용하여 Passport 애플리케이션의 인증 동작을 지정할 수 있습니다.

<!-- If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session. -->
`prompt` 값이 `none`이면, 사용자가 Passport 애플리케이션에 이미 인증되어 있지 않은 경우 Passport는 항상 인증 오류를 발생시킵니다. 값이 `consent`이면, 요청된 모든 스코프가 이전에 소비 애플리케이션에 부여되었더라도 Passport는 항상 인가 승인 화면을 표시합니다. 값이 `login`이면, 사용자가 이미 기존 세션을 가지고 있더라도 Passport 애플리케이션은 항상 사용자에게 애플리케이션에 다시 로그인하도록 요청합니다.

<!-- If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes. -->
`prompt` 값이 제공되지 않으면, 사용자가 요청된 스코프에 대해 소비 애플리케이션의 접근을 이전에 인가하지 않은 경우에만 인가를 요청합니다.

> [!NOTE]
> `/oauth/authorize` 라우트는 이미 Passport가 정의합니다. 이 라우트를 수동으로 정의할 필요가 없습니다.

<a name="approving-the-request"></a>
<!-- #### Approving the Request -->
#### Approving the Request

<!-- When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created. -->
인가 요청을 받으면 Passport는 `prompt` 파라미터 값이 있는 경우 그 값에 따라 자동으로 응답하며, 사용자가 인가 요청을 승인하거나 거부할 수 있는 템플릿을 표시할 수 있습니다. 사용자가 요청을 승인하면 소비 애플리케이션이 지정한 `redirect_uri`로 다시 리디렉션됩니다. `redirect_uri`는 클라이언트를 생성할 때 지정한 `redirect` URL과 일치해야 합니다.

<!-- Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization: -->
퍼스트 파티 클라이언트를 인가하는 경우처럼, 때로는 인가 프롬프트를 건너뛰고 싶을 수 있습니다. 이는 [extending the `Client` model](#overriding-default-models)하고 `skipsAuthorization` 메서드를 정의하여 처리할 수 있습니다. `skipsAuthorization`가 `true`를 반환하면, 소비 애플리케이션이 인가를 위해 리디렉션할 때 `prompt` 파라미터를 명시적으로 설정하지 않은 한 클라이언트는 승인되고 사용자는 즉시 `redirect_uri`로 다시 리디렉션됩니다.

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
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request: -->
사용자가 인가 요청을 승인하면 소비 애플리케이션으로 다시 리디렉션됩니다. 소비자는 먼저 `state` 파라미터를 리디렉션 전에 저장해 둔 값과 비교하여 검증해야 합니다. state 파라미터가 일치하면 소비자는 액세스 토큰을 요청하기 위해 사용자의 애플리케이션에 `POST` 요청을 보내야 합니다. 요청에는 사용자가 인가 요청을 승인했을 때 사용자의 애플리케이션이 발급한 인가 코드가 포함되어야 합니다.
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

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 시간이 초 단위로 들어 있습니다.

> [!NOTE]
> `/oauth/authorize` 라우트와 마찬가지로, `/oauth/token` 라우트는 Passport가 자동으로 정의합니다. 이 라우트를 직접 정의할 필요는 없습니다.

<a name="managing-tokens"></a>
<!-- ### Managing Tokens -->
### Managing Tokens

<!-- You may retrieve user's authorized tokens using the `tokens` method of the `Laravel\Passport\HasApiTokens` trait. For example, this may be used to offer your users a dashboard to keep track of their connections with third-party applications: -->
`Laravel\Passport\HasApiTokens` trait의 `tokens` 메서드를 사용하여 사용자가 인가한 토큰을 조회할 수 있습니다. 예를 들어, 사용자가 서드파티 애플리케이션과의 연결을 확인할 수 있는 대시보드를 제공할 때 사용할 수 있습니다.

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
<!-- ### Refreshing Tokens -->
### Refreshing Tokens

<!-- If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued: -->
애플리케이션이 수명이 짧은 액세스 토큰을 발급하는 경우, 사용자는 액세스 토큰이 발급될 때 함께 제공된 refresh token(갱신 토큰)을 통해 액세스 토큰을 갱신해야 합니다.

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

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
이 `/oauth/token` 라우트는 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 시간이 초 단위로 들어 있습니다.

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may revoke a token by using the `revoke` method on the `Laravel\Passport\Token` model. You may revoke a token's refresh token using the `revoke` method on the `Laravel\Passport\RefreshToken` model: -->
`Laravel\Passport\Token` 모델의 `revoke` 메서드를 사용하여 토큰을 철회할 수 있습니다. `Laravel\Passport\RefreshToken` 모델의 `revoke` 메서드를 사용하여 토큰의 refresh token도 철회할 수 있습니다.

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
<!-- ### Purging Tokens -->
### Purging Tokens

<!-- When tokens have been revoked or expired, you might want to purge them from the database. Passport's included `passport:purge` Artisan command can do this for you: -->
토큰이 철회되었거나 만료된 경우, 데이터베이스에서 해당 토큰을 정리하고 싶을 수 있습니다. Passport에 포함된 `passport:purge` Artisan 명령어로 이 작업을 수행할 수 있습니다.

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

<!-- You may also configure a [scheduled job](/docs/13.x/scheduling) in your application's `routes/console.php` file to automatically prune your tokens on a schedule: -->
애플리케이션의 `routes/console.php` 파일에서 [scheduled job](/docs/13.x/scheduling)을 설정하여 일정에 따라 토큰을 자동으로 정리할 수도 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
<!-- ## Authorization Code Grant With PKCE -->
## Authorization Code Grant With PKCE

<!-- The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or mobile applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token. -->
"Proof Key for Code Exchange"(PKCE)를 사용하는 Authorization Code grant는 단일 페이지 애플리케이션이나 모바일 애플리케이션이 API에 접근할 수 있도록 인증하는 안전한 방법입니다. 클라이언트 secret을 기밀로 저장할 수 있다고 보장할 수 없거나, 공격자가 authorization code를 가로채는 위협을 완화하려는 경우 이 grant를 사용해야 합니다. authorization code를 액세스 토큰으로 교환할 때 클라이언트 secret 대신 "code verifier"와 "code challenge"의 조합을 사용합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
<!-- ### Creating the Client -->
### Creating the Client

<!-- Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option: -->
애플리케이션이 PKCE를 사용하는 Authorization Code grant를 통해 토큰을 발급하려면, 먼저 PKCE가 활성화된 클라이언트를 생성해야 합니다. `--public` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="code-verifier-code-challenge"></a>
<!-- #### Code Verifier and Code Challenge -->
#### Code Verifier and Code Challenge

<!-- As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token. -->
이 authorization grant는 클라이언트 secret을 제공하지 않으므로, 개발자는 토큰을 요청하기 위해 code verifier(코드 검증자)와 code challenge(코드 챌린지)의 조합을 생성해야 합니다.

<!-- The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636). -->
code verifier는 [RFC 7636 specification](https://tools.ietf.org/html/rfc7636)에 정의된 대로 문자, 숫자, `"-"`, `"."`, `"_"`, `"~"` 문자를 포함하는 43자 이상 128자 이하의 임의 문자열이어야 합니다.

<!-- The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present. -->
code challenge는 URL과 파일명에 안전한 문자를 사용하는 Base64 인코딩 문자열이어야 합니다. 끝에 붙는 `'='` 문자는 제거해야 하며, 줄바꿈, 공백 또는 기타 추가 문자가 포함되어서는 안 됩니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route: -->
클라이언트가 생성되면, 클라이언트 ID와 생성된 code verifier 및 code challenge를 사용하여 애플리케이션에서 authorization code와 액세스 토큰을 요청할 수 있습니다. 먼저, 사용하는 애플리케이션은 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다.

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
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant. -->
사용자가 인가 요청을 승인하면, 사용하는 애플리케이션으로 다시 리다이렉트됩니다. 소비자 측은 표준 Authorization Code Grant에서와 같이 리다이렉트 전에 저장해 둔 값과 `state` 파라미터를 비교하여 검증해야 합니다.

<!-- If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier: -->
state 파라미터가 일치하면, 소비자 측은 액세스 토큰을 요청하기 위해 애플리케이션에 `POST` 요청을 보내야 합니다. 이 요청에는 사용자가 인가 요청을 승인했을 때 애플리케이션이 발급한 authorization code와, 처음 생성했던 code verifier가 함께 포함되어야 합니다.

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
<!-- ## Device Authorization Grant -->
## Device Authorization Grant

<!-- The OAuth2 device authorization grant allows browserless or limited input devices, such as TVs and game consoles, to obtain an access token by exchanging a "device code". When using device flow, the device client will instruct the user to use a secondary device, such as a computer or a smartphone and connect to your server where they will enter the provided "user code" and either approve or deny the access request. -->
OAuth2 device authorization grant는 TV나 게임 콘솔처럼 브라우저가 없거나 입력이 제한된 장치가 "device code"를 교환하여 액세스 토큰을 얻을 수 있게 합니다. device flow를 사용할 때 장치 클라이언트는 사용자에게 컴퓨터나 스마트폰 같은 보조 장치를 사용하도록 안내하고, 사용자는 해당 장치에서 서버에 접속하여 제공된 "user code"를 입력한 뒤 접근 요청을 승인하거나 거부합니다.

<!-- To get started, we need to instruct Passport how to return our "user code" and "authorization" views. -->
시작하려면 Passport가 "user code"와 "authorization" 뷰를 어떻게 반환해야 하는지 알려주어야 합니다.

<!-- All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class. -->
authorization 뷰의 모든 렌더링 로직은 `Laravel\Passport\Passport` 클래스를 통해 제공되는 적절한 메서드를 사용하여 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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

<!-- Passport will automatically define routes that return these views. Your `auth.oauth.device.user-code` template should include a form that makes a GET request to the `passport.device.authorizations.authorize` route. The `passport.device.authorizations.authorize` route expects a `user_code` query parameter. -->
Passport는 이러한 뷰를 반환하는 라우트를 자동으로 정의합니다. `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 라우트로 GET 요청을 보내는 폼이 포함되어야 합니다. `passport.device.authorizations.authorize` 라우트는 `user_code` 쿼리 파라미터를 기대합니다.

<!-- Your `auth.oauth.device.authorize` template should include a form that makes a POST request to the `passport.device.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.device.authorizations.deny` route to deny the authorization. The `passport.device.authorizations.approve` and `passport.device.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields. -->
`auth.oauth.device.authorize` 템플릿에는 인가를 승인하기 위해 `passport.device.authorizations.approve` 라우트로 POST 요청을 보내는 폼과, 인가를 거부하기 위해 `passport.device.authorizations.deny` 라우트로 DELETE 요청을 보내는 폼이 포함되어야 합니다. `passport.device.authorizations.approve` 및 `passport.device.authorizations.deny` 라우트는 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="creating-a-device-authorization-grant-client"></a>
<!-- ### Creating a Device Authorization Grant Client -->
### Creating a Device Authorization Grant Client

<!-- Before your application can issue tokens via the device authorization grant, you will need to create a device flow enabled client. You may do this using the `passport:client` Artisan command with the `--device` option. This command will create a first-party device flow enabled client and provide you with a client ID and secret: -->
애플리케이션이 device authorization grant를 통해 토큰을 발급하려면, 먼저 device flow가 활성화된 클라이언트를 생성해야 합니다. `--device` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다. 이 명령어는 device flow가 활성화된 first-party 클라이언트를 생성하고, 클라이언트 ID와 secret을 제공합니다.

```shell
php artisan passport:client --device
```

<!-- Additionally, you may use `createDeviceAuthorizationGrantClient` method on the `ClientRepository` class to register a third-party client that belongs to the given user: -->
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
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="device-code"></a>
<!-- #### Requesting a Device Code -->
#### Requesting a Device Code

<!-- Once a client has been created, developers may use their client ID to request a device code from your application. First, the consuming device should make a `POST` request to your application's `/oauth/device/code` route to request a device code: -->
클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용하여 애플리케이션에 device code를 요청할 수 있습니다. 먼저, 사용하는 장치는 device code를 요청하기 위해 애플리케이션의 `/oauth/device/code` 라우트로 `POST` 요청을 보내야 합니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

<!-- This will return a JSON response containing `device_code`, `user_code`, `verification_uri`, `interval`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the device code expires. The `interval` attribute contains the number of seconds the consuming device should wait between requests when polling `/oauth/token` route to avoid rate limit errors. -->
이 요청은 `device_code`, `user_code`, `verification_uri`, `interval`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 속성에는 device code가 만료되기까지 남은 시간이 초 단위로 들어 있습니다. `interval` 속성에는 rate limit 오류를 피하기 위해 사용하는 장치가 `/oauth/token` 라우트를 폴링할 때 요청 사이에 기다려야 하는 시간이 초 단위로 들어 있습니다.

> [!NOTE]
> 기억하세요. `/oauth/device/code` 라우트는 이미 Passport가 정의합니다. 이 라우트를 직접 정의할 필요는 없습니다.

<a name="user-code"></a>
<!-- #### Displaying the Verification URI and User Code -->
#### Displaying the Verification URI and User Code

<!-- Once a device code request has been obtained, the consuming device should instruct the user to use another device and visit the provided `verification_uri` and enter the `user_code` in order to approve the authorization request. -->
device code 요청을 통해 응답을 받으면, 사용하는 장치는 사용자에게 다른 장치를 사용하여 제공된 `verification_uri`에 접속하고 `user_code`를 입력해 인가 요청을 승인하도록 안내해야 합니다.

<a name="polling-token-request"></a>
<!-- #### Polling Token Request -->
#### Polling Token Request

<!-- Since the user will be using a separate device to grant (or deny) access, the consuming device should poll your application's `/oauth/token` route to determine when the user has responded to the request. The consuming device should use the minimum polling `interval` provided in the JSON response when requesting device code to avoid rate limit errors: -->
사용자는 별도의 장치를 사용하여 접근을 승인하거나 거부하므로, 사용하는 장치는 사용자가 요청에 응답했는지 확인하기 위해 애플리케이션의 `/oauth/token` 라우트를 폴링해야 합니다. rate limit 오류를 피하려면, 사용하는 장치는 device code를 요청할 때 JSON 응답으로 제공된 최소 폴링 `interval`을 사용해야 합니다.

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

<!-- If the user has approved the authorization request, this will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
사용자가 인가 요청을 승인한 경우, 이 요청은 `access_token`, `refresh_token`, `expires_in` 속성이 포함된 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료되기까지 남은 시간이 초 단위로 들어 있습니다.

<a name="password-grant"></a>
<!-- ## Password Grant -->
## Password Grant

> [!WARNING]
> 더 이상 password grant 토큰 사용을 권장하지 않습니다. 대신 [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

<!-- The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow. -->
OAuth2 password grant를 사용하면 모바일 애플리케이션 같은 다른 first-party 클라이언트가 이메일 주소 / 사용자명과 비밀번호를 사용하여 액세스 토큰을 얻을 수 있습니다. 이를 통해 사용자가 전체 OAuth2 authorization code 리다이렉트 흐름을 거치지 않아도, first-party 클라이언트에 액세스 토큰을 안전하게 발급할 수 있습니다.

<!-- To enable the password grant, call the `enablePasswordGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
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
<!-- ### Creating a Password Grant Client -->
### Creating a Password Grant Client

<!-- Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option. -->
애플리케이션이 password grant를 통해 토큰을 발급하려면, 먼저 password grant 클라이언트를 생성해야 합니다. `--password` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<!-- Once you have enabled the grant and have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by Passport so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server: -->
grant를 활성화하고 password grant 클라이언트를 생성한 뒤에는 사용자의 이메일 주소와 비밀번호를 포함하여 `/oauth/token` 라우트로 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이 라우트는 이미 Passport가 등록하므로 직접 정의할 필요가 없다는 점을 기억하세요. 요청이 성공하면 서버의 JSON 응답에서 `access_token`과 `refresh_token`을 받게 됩니다.

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
> 액세스 토큰은 기본적으로 수명이 길게 설정되어 있다는 점을 기억하세요. 그러나 필요한 경우 [configure your maximum access token lifetime](#configuration)을 자유롭게 설정할 수 있습니다.

<a name="requesting-all-scopes"></a>
<!-- ### Requesting All Scopes -->
### Requesting All Scopes

<!-- When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant: -->
패스워드 그랜트 또는 클라이언트 자격 증명 그랜트를 사용할 때, 애플리케이션이 지원하는 모든 스코프에 대해 토큰을 인가하고 싶을 수 있습니다. 이 경우 `*` 스코프를 요청하면 됩니다. `*` 스코프를 요청하면 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 스코프는 `password` 또는 `client_credentials` 그랜트를 사용해 발급된 토큰에만 할당할 수 있습니다.

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
<!-- ### Customizing the User Provider -->
### Customizing the User Provider

<!-- If your application uses more than one [authentication user provider](/docs/13.x/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized. -->
애플리케이션에서 둘 이상의 [authentication user provider](/docs/13.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 패스워드 그랜트 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 지정한 프로바이더 이름은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 그런 다음 [protect your route using middleware](#multiple-authentication-guards)하여 해당 guard에 지정된 프로바이더의 사용자만 인가되도록 할 수 있습니다.

<a name="customizing-the-username-field"></a>
<!-- ### Customizing the Username Field -->
### Customizing the Username Field

<!-- When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model: -->
패스워드 그랜트로 인증할 때 Passport는 인증 가능한 모델의 `email` 속성을 "사용자 이름"으로 사용합니다. 그러나 모델에 `findForPassport` 메서드를 정의하여 이 동작을 커스터마이징할 수 있습니다.

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
<!-- ### Customizing the Password Validation -->
### Customizing the Password Validation

<!-- When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model: -->
패스워드 그랜트로 인증할 때 Passport는 전달된 비밀번호를 검증하기 위해 모델의 `password` 속성을 사용합니다. 모델에 `password` 속성이 없거나 비밀번호 유효성 검증 로직을 커스터마이징하고 싶다면, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다.

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
<!-- ## Implicit Grant -->
## Implicit Grant

> [!WARNING]
> 더 이상 암묵적 그랜트 토큰 사용을 권장하지 않습니다. 대신 [a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

<!-- The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
암묵적 그랜트는 인가 코드 그랜트와 비슷하지만, 인가 코드를 교환하지 않고 토큰이 클라이언트에 반환됩니다. 이 그랜트는 클라이언트 자격 증명을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 가장 흔히 사용됩니다. 이 그랜트를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

<!-- Before your application can issue tokens via the implicit grant, you will need to create an implicit grant client. You may do this using the `passport:client` Artisan command with the `--implicit` option. -->
애플리케이션이 암묵적 그랜트를 통해 토큰을 발급하려면 먼저 암묵적 그랜트 클라이언트를 생성해야 합니다. `--implicit` 옵션과 함께 `passport:client` Artisan 명령어를 사용하면 됩니다.

```shell
php artisan passport:client --implicit
```

<!-- Once the grant has been enabled and an implicit client has been created, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
그랜트가 활성화되고 암묵적 클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용해 애플리케이션에 액세스 토큰을 요청할 수 있습니다. 토큰을 사용하는 애플리케이션은 다음과 같이 애플리케이션의 `/oauth/authorize` 라우트로 리다이렉트 요청을 보내야 합니다.

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
> `/oauth/authorize` 라우트는 이미 Passport에서 정의한다는 점을 기억하세요. 이 라우트를 직접 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
<!-- ## Client Credentials Grant -->
## Client Credentials Grant

<!-- The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API. -->
클라이언트 자격 증명 그랜트는 머신 간 인증에 적합합니다. 예를 들어 API를 통해 유지보수 작업을 수행하는 예약 작업에서 이 그랜트를 사용할 수 있습니다.

<!-- Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command: -->
애플리케이션이 클라이언트 자격 증명 그랜트를 통해 토큰을 발급하려면 먼저 클라이언트 자격 증명 그랜트 클라이언트를 생성해야 합니다. `passport:client` Artisan 명령어의 `--client` 옵션을 사용하면 됩니다.

```shell
php artisan passport:client --client
```

<!-- Next, assign the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware to a route: -->
다음으로 `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` Middleware를 라우트에 할당하세요.

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

<!-- To restrict access to the route to specific scopes, you may provide a list of the required scopes to the `using` method`: -->
특정 스코프로 라우트 접근을 제한하려면 필요한 스코프 목록을 `using` 메서드에 전달할 수 있습니다.

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

> [!WARNING]
> [underlying OAuth2 server](https://oauth2.thephpleague.com/database-setup/#:~:text=Please%20note%20that,the%20bearer%20token.)는 클라이언트 자격 증명 토큰의 `sub` claim을 클라이언트 식별자로 설정합니다. 기본적으로 Passport는 클라이언트에 UUID를 사용하므로 사용자의 정수형 기본 키와 충돌할 수 없습니다. 그러나 `Passport::$clientUuids`를 `false`로 설정했다면, 클라이언트 자격 증명 토큰이 클라이언트 ID와 같은 ID를 가진 사용자로 의도치 않게 해석될 수 있습니다. 이런 경우 이 Middleware를 사용하더라도 들어오는 토큰이 클라이언트 자격 증명 토큰임을 보장할 수 없습니다.

<a name="retrieving-tokens"></a>
<!-- ### Retrieving Tokens -->
### Retrieving Tokens

<!-- To retrieve a token using this grant type, make a request to the `oauth/token` endpoint: -->
이 그랜트 타입을 사용해 토큰을 가져오려면 `oauth/token` 엔드포인트로 요청을 보내세요.

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
<!-- ## Personal Access Tokens -->
## Personal Access Tokens

<!-- Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general. -->
때때로 사용자는 일반적인 인가 코드 리다이렉트 흐름을 거치지 않고 자신에게 액세스 토큰을 발급하고 싶을 수 있습니다. 애플리케이션 UI를 통해 사용자가 자신에게 직접 토큰을 발급할 수 있게 하면, 사용자가 API를 실험해 볼 수 있도록 하거나 일반적으로 액세스 토큰을 발급하는 더 단순한 방법으로 활용할 수 있습니다.

> [!NOTE]
> 애플리케이션에서 Passport를 주로 개인 액세스 토큰 발급 용도로 사용한다면, Laravel의 가벼운 퍼스트 파티 API 액세스 토큰 발급 라이브러리인 [Laravel Sanctum](/docs/13.x/sanctum) 사용을 고려하세요.

<a name="creating-a-personal-access-client"></a>
<!-- ### Creating a Personal Access Client -->
### Creating a Personal Access Client

<!-- Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command: -->
애플리케이션이 개인 액세스 토큰을 발급하려면 먼저 개인 액세스 클라이언트를 생성해야 합니다. `--personal` 옵션과 함께 `passport:client` Artisan 명령어를 실행하면 됩니다. 이미 `passport:install` 명령어를 실행했다면 이 명령어를 실행할 필요가 없습니다.

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
<!-- ### Customizing the User Provider -->
### Customizing the User Provider

<!-- If your application uses more than one [authentication user provider](/docs/13.x/authentication#introduction), you may specify which user provider the personal access grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --personal` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized. -->
애플리케이션에서 둘 이상의 [authentication user provider](/docs/13.x/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령어로 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 개인 액세스 그랜트 클라이언트가 사용할 사용자 프로바이더를 지정할 수 있습니다. 지정한 프로바이더 이름은 애플리케이션의 `config/auth.php` 설정 파일에 정의된 유효한 프로바이더와 일치해야 합니다. 그런 다음 [protect your route using middleware](#multiple-authentication-guards)하여 해당 guard에 지정된 프로바이더의 사용자만 인가되도록 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
<!-- ### Managing Personal Access Tokens -->
### Managing Personal Access Tokens

<!-- Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument: -->
개인 액세스 클라이언트를 생성한 후에는 `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용해 지정한 사용자에 대한 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인수로 토큰 이름을 받고, 두 번째 인수로 선택 사항인 [scopes](#token-scopes) 배열을 받습니다.

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
<!-- ## Protecting Routes -->
## Protecting Routes

<a name="via-middleware"></a>
<!-- ### Via Middleware -->
### Via Middleware

<!-- Passport includes an [authentication guard](/docs/13.x/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token: -->
Passport에는 들어오는 요청의 액세스 토큰을 검증하는 [authentication guard](/docs/13.x/authentication#adding-custom-guards)가 포함되어 있습니다. `api` guard가 `passport` 드라이버를 사용하도록 설정한 후에는, 유효한 액세스 토큰이 필요한 모든 라우트에 `auth:api` Middleware만 지정하면 됩니다.

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```

> [!WARNING]
> [client credentials grant](#client-credentials-grant)를 사용하는 경우, 라우트를 보호할 때 `auth:api` Middleware 대신 [the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware](#client-credentials-grant)를 사용해야 합니다.

<a name="multiple-authentication-guards"></a>
<!-- #### Multiple Authentication Guards -->
#### Multiple Authentication Guards

<!-- If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file: -->
애플리케이션에서 서로 완전히 다른 Eloquent 모델을 사용할 수 있는 여러 유형의 사용자를 인증한다면, 각 사용자 프로바이더 타입마다 guard 설정을 정의해야 할 가능성이 큽니다. 이렇게 하면 특정 사용자 프로바이더를 대상으로 하는 요청을 보호할 수 있습니다. 예를 들어 `config/auth.php` 설정 파일에 다음과 같은 guard 설정이 있다고 가정해 보겠습니다.

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

<!-- The following route will utilize the `api-customers` guard, which uses the `customers` user provider, to authenticate incoming requests: -->
다음 라우트는 `customers` 사용자 프로바이더를 사용하는 `api-customers` guard를 활용하여 들어오는 요청을 인증합니다.

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport에서 여러 사용자 프로바이더를 사용하는 방법에 대한 자세한 내용은 [personal access tokens documentation](#customizing-the-user-provider-for-pat)와 [password grant documentation](#customizing-the-user-provider)를 참고하세요.

<a name="passing-the-access-token"></a>
<!-- ### Passing the Access Token -->
### Passing the Access Token

<!-- When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the `Http` Facade: -->
Passport로 보호된 라우트를 호출할 때, 애플리케이션의 API 소비자는 요청의 `Authorization` 헤더에 액세스 토큰을 `Bearer` 토큰으로 지정해야 합니다. 예를 들어 `Http` Facade를 사용할 때는 다음과 같습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
<!-- ## Token Scopes -->
## Token Scopes

<!-- Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf. -->
스코프를 사용하면 API 클라이언트가 계정에 접근할 권한을 요청할 때 특정 권한 집합만 요청할 수 있습니다. 예를 들어 이커머스 애플리케이션을 만들고 있다면 모든 API 소비자에게 주문 생성 권한이 필요하지는 않습니다. 대신 소비자가 주문 배송 상태에 접근할 권한만 요청하도록 허용할 수 있습니다. 다시 말해, 스코프는 사용자를 대신해 서드 파티 애플리케이션이 수행할 수 있는 작업을 애플리케이션 사용자가 제한할 수 있게 해 줍니다.

<a name="defining-scopes"></a>
<!-- ### Defining Scopes -->
### Defining Scopes

<!-- You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen: -->
애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `Passport::tokensCan` 메서드를 사용해 API의 스코프를 정의할 수 있습니다. `tokensCan` 메서드는 스코프 이름과 스코프 설명으로 이루어진 배열을 받습니다. 스코프 설명은 원하는 내용으로 작성할 수 있으며, 사용자에게 인가 승인 화면에 표시됩니다.

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
<!-- ### Default Scope -->
### Default Scope

<!-- If a client does not request any specific scopes, you may configure your Passport server to attach default scopes to the token using the `defaultScopes` method. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
클라이언트가 특정 스코프를 요청하지 않는 경우, `defaultScopes` 메서드를 사용해 Passport 서버가 토큰에 기본 스코프를 첨부하도록 설정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

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
<!-- ### Assigning Scopes to Tokens -->
### Assigning Scopes to Tokens

<a name="when-requesting-authorization-codes"></a>
<!-- #### When Requesting Authorization Codes -->
#### When Requesting Authorization Codes

<!-- When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes: -->
인가 코드 그랜트를 사용해 액세스 토큰을 요청할 때, 소비자는 원하는 스코프를 `scope` 쿼리 문자열 파라미터로 지정해야 합니다. `scope` 파라미터는 공백으로 구분된 스코프 목록이어야 합니다.

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
<!-- #### When Issuing Personal Access Tokens -->
#### When Issuing Personal Access Tokens

<!-- If you are issuing personal access tokens using the `App\Models\User` model's `createToken` method, you may pass the array of desired scopes as the second argument to the method: -->
`App\Models\User` 모델의 `createToken` 메서드를 사용해 개인 액세스 토큰을 발급하는 경우, 원하는 스코프 배열을 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
<!-- ### Checking Scopes -->
### Checking Scopes

<!-- Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope. -->
Passport에는 들어오는 요청이 지정된 스코프를 부여받은 토큰으로 인증되었는지 확인하는 데 사용할 수 있는 두 가지 Middleware가 포함되어 있습니다.

<a name="check-for-all-scopes"></a>
<!-- #### Check For All Scopes -->
#### Check For All Scopes

<!-- The `Laravel\Passport\Http\Middleware\CheckToken` middleware may be assigned to a route to verify that the incoming request's access token has all the listed scopes: -->
`Laravel\Passport\Http\Middleware\CheckToken` Middleware를 라우트에 할당하여 들어오는 요청의 액세스 토큰에 나열된 모든 스코프가 있는지 확인할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
<!-- #### Check for Any Scopes -->
#### Check for Any Scopes

<!-- The `Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes: -->
`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` Middleware를 라우트에 할당하여 들어오는 요청의 액세스 토큰에 나열된 스코프 중 *하나 이상*이 있는지 확인할 수 있습니다.

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```
<a name="scope-attributes"></a>
<!-- #### Scope Attributes -->
#### Scope Attributes

<!-- If your application uses [controller middleware attributes](/docs/13.x/controllers#middleware-attributes), you may use the `Laravel\Passport\Attributes\AuthorizeToken` attribute as a convenient shortcut for Passport's scope middleware: -->
애플리케이션에서 [controller middleware attributes](/docs/13.x/controllers#middleware-attributes)을 사용한다면, Passport의 스코프 Middleware를 편리하게 사용하기 위한 단축 방식으로 `Laravel\Passport\Attributes\AuthorizeToken` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Laravel\Passport\Attributes\AuthorizeToken;

#[AuthorizeToken('orders:read')]
#[AuthorizeToken('orders:create', only: ['store'])]
class OrderController
{
    #[AuthorizeToken(['orders:read', 'orders:create'], anyScope: true)]
    public function index()
    {
        // Access token has either "orders:read" or "orders:create" scope...
    }

    public function store()
    {
        // Access token has both "orders:read" and "orders:create" scopes...
    }
}
```

<!-- By default, the `AuthorizeToken` attribute requires all given scopes. If you pass `anyScope: true`, the request is authorized when the token has at least one of the given scopes. -->
기본적으로 `AuthorizeToken` 속성은 전달된 모든 스코프를 요구합니다. `anyScope: true`를 전달하면, 토큰이 전달된 스코프 중 하나 이상을 가지고 있을 때 요청이 인가됩니다.

<a name="checking-scopes-on-a-token-instance"></a>
<!-- #### Checking Scopes on a Token Instance -->
#### Checking Scopes on a Token Instance

<!-- Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance: -->
액세스 토큰으로 인증된 요청이 애플리케이션에 들어온 후에도, 인증된 `App\Models\User` 인스턴스의 `tokenCan` 메서드를 사용하여 토큰이 특정 스코프를 가지고 있는지 확인할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
<!-- #### Additional Scope Methods -->
#### Additional Scope Methods

<!-- The `scopeIds` method will return an array of all defined IDs / names: -->
`scopeIds` 메서드는 정의된 모든 ID / 이름의 배열을 반환합니다.

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

<!-- The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`: -->
`scopes` 메서드는 정의된 모든 스코프를 `Laravel\Passport\Scope` 인스턴스 배열로 반환합니다.

```php
Passport::scopes();
```

<!-- The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names: -->
`scopesFor` 메서드는 주어진 ID / 이름과 일치하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다.

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

<!-- You may determine if a given scope has been defined using the `hasScope` method: -->
`hasScope` 메서드를 사용하여 특정 스코프가 정의되어 있는지 확인할 수 있습니다.

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers. -->
API를 구축할 때, JavaScript 애플리케이션에서 직접 자신의 API를 사용할 수 있으면 매우 유용합니다. 이러한 API 개발 방식에서는 공개적으로 제공하는 것과 동일한 API를 자신의 애플리케이션에서도 사용할 수 있습니다. 같은 API를 웹 애플리케이션, 모바일 애플리케이션, 서드파티 애플리케이션, 그리고 여러 패키지 매니저에 게시할 수 있는 SDK에서 함께 사용할 수 있습니다.

<!-- Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is append the `CreateFreshApiToken` middleware to the `web` middleware group in your application's `bootstrap/app.php` file: -->
일반적으로 JavaScript 애플리케이션에서 API를 사용하려면 액세스 토큰을 애플리케이션에 직접 전달하고, 애플리케이션으로 보내는 각 요청에 그 토큰을 함께 전달해야 합니다. 하지만 Passport에는 이 작업을 대신 처리해 주는 Middleware가 포함되어 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `web` Middleware 그룹에 `CreateFreshApiToken` Middleware를 추가하기만 하면 됩니다.

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` Middleware가 Middleware 스택에서 마지막 Middleware로 나열되어 있는지 확인해야 합니다.

<!-- This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token: -->
이 Middleware는 나가는 응답에 `laravel_token` 쿠키를 첨부합니다. 이 쿠키에는 Passport가 JavaScript 애플리케이션의 API 요청을 인증하는 데 사용할 암호화된 JWT가 들어 있습니다. JWT의 수명은 `session.lifetime` 설정값과 같습니다. 이제 브라우저가 이후의 모든 요청에 쿠키를 자동으로 전송하므로, 액세스 토큰을 명시적으로 전달하지 않고도 애플리케이션의 API에 요청을 보낼 수 있습니다.

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
<!-- #### Customizing the Cookie Name -->
#### Customizing the Cookie Name

<!-- If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
필요하다면 `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키의 이름을 커스터마이징할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

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
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding included with the skeleton application and all starter kits includes an [Axios](https://github.com/axios/axios) instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests. -->
이 인증 방식을 사용할 때는 요청에 유효한 CSRF 토큰 헤더가 포함되어 있는지 확인해야 합니다. 스켈레톤 애플리케이션과 모든 스타터 킷에 포함된 기본 Laravel JavaScript 스캐폴딩에는 [Axios](https://github.com/axios/axios) 인스턴스가 포함되어 있으며, 이 인스턴스는 암호화된 `XSRF-TOKEN` 쿠키 값을 자동으로 사용하여 동일 출처(same-origin) 요청에 `X-XSRF-TOKEN` 헤더를 전송합니다.

> [!NOTE]
> `X-XSRF-TOKEN` 대신 `X-CSRF-TOKEN` 헤더를 보내기로 했다면, `csrf_token()`이 제공하는 암호화되지 않은 토큰을 사용해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Passport raises events when issuing access tokens and refresh tokens. You may [listen for these events](/docs/13.x/events) to prune or revoke other access tokens in your database: -->
Passport는 액세스 토큰과 리프레시 토큰을 발급할 때 이벤트를 발생시킵니다. 데이터베이스의 다른 액세스 토큰을 정리하거나 취소하기 위해 [listen for these events](/docs/13.x/events)할 수 있습니다.

<div class="overflow-auto">

<!-- | Event Name | | --------------------------------------------- | | `Laravel\Passport\Events\AccessTokenCreated` | | `Laravel\Passport\Events\AccessTokenRevoked` | | `Laravel\Passport\Events\RefreshTokenCreated` | -->
| 이벤트 이름                                   |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token: -->
Passport의 `actingAs` 메서드는 현재 인증된 사용자와 해당 스코프를 지정하는 데 사용할 수 있습니다. `actingAs` 메서드에 전달하는 첫 번째 인수는 사용자 인스턴스이고, 두 번째 인수는 사용자의 토큰에 부여할 스코프 배열입니다.

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

<!-- Passport's `actingAsClient` method may be used to specify the currently authenticated client as well as its scopes. The first argument given to the `actingAsClient` method is the client instance and the second is an array of scopes that should be granted to the client's token: -->
Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 해당 스코프를 지정하는 데 사용할 수 있습니다. `actingAsClient` 메서드에 전달하는 첫 번째 인수는 클라이언트 인스턴스이고, 두 번째 인수는 클라이언트의 토큰에 부여할 스코프 배열입니다.

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
