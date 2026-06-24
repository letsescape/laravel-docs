<!-- # Laravel Sanctum -->
# Laravel Sanctum

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Overriding Default Models](#overriding-default-models)
- [API Token Authentication](#api-token-authentication)
    - [Issuing API Tokens](#issuing-api-tokens)
    - [Token Abilities](#token-abilities)
    - [Protecting Routes](#protecting-routes)
    - [Revoking Tokens](#revoking-tokens)
- [SPA Authentication](#spa-authentication)
    - [Configuration](#spa-configuration)
    - [Authenticating](#spa-authenticating)
    - [Protecting Routes](#protecting-spa-routes)
    - [Authorizing Private Broadcast Channels](#authorizing-private-broadcast-channels)
- [Mobile Application Authentication](#mobile-application-authentication)
    - [Issuing API Tokens](#issuing-mobile-api-tokens)
    - [Protecting Routes](#protecting-mobile-api-routes)
    - [Revoking Tokens](#revoking-mobile-api-tokens)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Sanctum](https://github.com/laravel/sanctum) provides a featherweight authentication system for SPAs (single page applications), mobile applications, and simple, token based APIs. Sanctum allows each user of your application to generate multiple API tokens for their account. These tokens may be granted abilities / scopes which specify which actions the tokens are allowed to perform. -->
[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가볍고 단순한 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 본인 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰에는 특정 권한(abilities/scopes)을 부여하여 해당 토큰으로 허용된 작업을 세분화할 수 있습니다.

<a name="how-it-works"></a>
<!-- ### How It Works -->
### How It Works

<!-- Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library. -->
Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 만들어졌습니다. 본격적으로 살펴보기 전에 각각의 목적을 먼저 설명합니다.

<a name="how-it-works-api-tokens"></a>
<!-- #### API Tokens -->
#### API Tokens

<!-- First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime. -->
첫 번째로, Sanctum은 OAuth 같은 복잡한 방식을 사용하지 않고도 사용자에게 API 토큰을 발급할 수 있게 해 주는 단순한 패키지입니다. 이 기능은 GitHub 등에서 제공하는 "개인 액세스 토큰(Personal Access Token)"에서 영감을 받았습니다. 예를 들어, 애플리케이션의 '계정 설정' 화면에서 사용자가 본인의 API 토큰을 직접 발급받을 수 있는 기능이 있다고 생각해보겠습니다. 이런 경우에 Sanctum을 활용하여 토큰을 생성하고 관리할 수 있습니다. 이러한 토큰은 보통 매우 긴 유효기간(수년 이상)을 가지지만, 사용자가 언제든 직접 폐기(삭제)할 수 있습니다.

<!-- Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token. -->
Laravel Sanctum은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고, 클라이언트의 HTTP 요청에는 `Authorization` 헤더에 유효한 API 토큰을 포함시켜 인증을 처리합니다.

<a name="how-it-works-spa-authentication"></a>
<!-- #### SPA Authentication -->
#### SPA Authentication

<!-- Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI or a Next.js application. -->
두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 인증하는 간단한 방법을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소(Repository)에 존재할 수도 있고, 예를 들어 Vue CLI나 Next.js로 제작된 별도 저장소의 SPA일 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능을 위해 Sanctum은 별도의 토큰을 사용하지 않습니다. 대신, Laravel이 기본적으로 제공하는 쿠키 기반 세션 인증 방식을 활용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 사용하여 인증을 처리합니다. 이를 통해 CSRF 보호, 세션 기반 인증, 인증 정보가 XSS로 인해 노출되는 것을 방지하는 다양한 보안 혜택을 누릴 수 있습니다.

<!-- Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token. -->
Sanctum은 클라이언트 요청이 여러분의 SPA 프런트엔드에서 왔을 때에만 쿠키 인증을 시도합니다. 요청을 받으면 우선 인증 쿠키가 있는지 확인하고, 쿠키가 없을 경우 `Authorization` 헤더에 유효한 API 토큰이 있는지 검사합니다.

> [!TIP]
> Sanctum을 오직 API 토큰 인증 목적이나 SPA 인증 중 한 가지 만으로만 사용하는 것도 완전히 정상적입니다. 반드시 두 기능을 모두 쓸 필요는 없습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!TIP]
> 최신 버전의 Laravel에는 Sanctum이 이미 포함되어 있습니다. 하지만 애플리케이션의 `composer.json`에 `laravel/sanctum`이 없다면 아래의 설치 방법을 따라 진행하시면 됩니다.

<!-- You may install Laravel Sanctum via the Composer package manager: -->
Composer 패키지 매니저로 Laravel Sanctum을 설치할 수 있습니다.

```
composer require laravel/sanctum
```

<!-- Next, you should publish the Sanctum configuration and migration files using the `vendor:publish` Artisan command. The `sanctum` configuration file will be placed in your application's `config` directory: -->
다음으로, `vendor:publish` 아티즌 명령어를 이용해 Sanctum의 설정 파일과 마이그레이션을 퍼블리시(publish)해야 합니다. `sanctum` 설정 파일은 애플리케이션의 `config` 디렉터리에 생성됩니다.

```
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

<!-- Finally, you should run your database migrations. Sanctum will create one database table in which to store API tokens: -->
마지막으로 데이터베이스 마이그레이션을 실행합니다. Sanctum은 API 토큰을 저장할 테이블 하나를 생성합니다.

```
php artisan migrate
```

<!-- Next, if you plan to utilize Sanctum to authenticate an SPA, you should add Sanctum's middleware to your `api` middleware group within your application's `app/Http/Kernel.php` file: -->
또한 SPA 인증 기능을 사용할 예정이라면, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가해야 합니다.

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
<!-- #### Migration Customization -->
#### Migration Customization

<!-- If you are not going to use Sanctum's default migrations, you should call the `Sanctum::ignoreMigrations` method in the `register` method of your `App\Providers\AppServiceProvider` class. You may export the default migrations by executing the following command: `php artisan vendor:publish --tag=sanctum-migrations` -->
Sanctum의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일을 내보내려면 다음 명령어를 실행하십시오: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum: -->
일반적으로 필요하지는 않지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장하여 직접 커스터마이징할 수 있습니다.

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

<!-- Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of one of your application's service providers: -->
이후 Sanctum에서 커스텀 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드를 호출해야 합니다. 주로 서비스 프로바이더의 `boot` 메서드 내에서 이 메서드를 사용합니다.

```
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
<!-- ## API Token Authentication -->
## API Token Authentication

> [!TIP]
> 여러분이 직접 만든 SPA에서는 API 토큰 인증을 사용하지 않아야 합니다. 대신 Sanctum의 [SPA authentication features](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token. -->
Sanctum을 사용하면 API 요청을 인증할 수 있도록 API 토큰(개인 액세스 토큰)을 발급할 수 있습니다. API 토큰을 사용할 때는 요청 헤더의 `Authorization`에 `Bearer` 토큰 형식으로 토큰을 포함시켜야 합니다.

<!-- To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait: -->
사용자를 위한 토큰 발급을 시작하려면, User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 추가해야 합니다.

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created: -->
토큰을 발급하려면 `createToken` 메서드를 사용하면 됩니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. 생성된 API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시 처리되지만, 토큰의 원본 값을 `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 바로 확인할 수 있습니다. 반드시 토큰이 생성된 직후 사용자에게 이 값을 보여주어야 합니다.

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

<!-- You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait: -->
`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 사용해 사용자가 가지고 있는 모든 토큰을 조회할 수도 있습니다.

```
foreach ($user->tokens as $token) {
    //
}
```

<a name="token-abilities"></a>
<!-- ### Token Abilities -->
### Token Abilities

<!-- Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method: -->
Sanctum을 이용하면 토큰에 '권한(abilities)'을 부여할 수 있습니다. 이는 OAuth의 '스코프(scopes)'와 유사한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 권한 목록을 지정할 수 있습니다.

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

<!-- When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` method: -->
이후 Sanctum으로 인증된 요청에서 해당 토큰에 특정 권한이 있는지 확인하려면 `tokenCan` 메서드를 사용합니다.

```
if ($user->tokenCan('server:update')) {
    //
}
```

<a name="token-ability-middleware"></a>
<!-- #### Token Ability Middleware -->
#### Token Ability Middleware

<!-- Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, add the following middleware to the `$routeMiddleware` property of your application's `app/Http/Kernel.php` file: -->
Sanctum에는 주어진 권한을 가진 토큰으로 요청이 인증되었는지 검증할 수 있는 미들웨어도 두 가지 포함되어 있습니다. 먼저, 아래와 같이 애플리케이션의 `app/Http/Kernel.php` 파일의 `$routeMiddleware` 속성에 미들웨어를 등록하세요.

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

<!-- The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities: -->
`abilities` 미들웨어는 해당 요청의 토큰이 지정된 모든 권한을 가지고 있는지 확인합니다.

```
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

<!-- The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities: -->
`ability` 미들웨어는 지정된 권한 중 *하나 이상*만 가지고 있으면 허용합니다.

```
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
<!-- #### First-Party UI Initiated Requests -->
#### First-Party UI Initiated Requests

<!-- For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication). -->
편의를 위해, 인증된 요청이 여러분의 자체 SPA에서 왔고 Sanctum의 [SPA authentication](#spa-authentication)을 사용한 경우에는 `tokenCan` 메서드는 항상 `true`를 반환합니다.

<!-- However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/8.x/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action. -->
하지만 이는 해당 사용자가 직접적으로 허용된 작업을 반드시 수행할 수 있다는 의미는 아닙니다. 실제로는 애플리케이션의 [authorization policies](/docs/8.x/authorization#creating-policies)에서 토큰에 주어진 권한 및 해당 사용자 인스턴스가 해당 권한을 행사할 자격이 있는지 별도로 다시 확인해야 합니다.

<!-- For example, if we imagine an application that manages servers, this might mean checking that token is authorized to update servers **and** that the server belongs to the user: -->
예를 들어, 서버를 관리하는 애플리케이션에서, 토큰이 서버 업데이트 권한을 가지고 있고, 해당 서버가 실제로 이 사용자에 속하는지도 추가로 검사할 수 있습니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

<!-- At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorizations policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers. -->
SPA에서 발생한 요청에 대해 항상 `tokenCan`이 `true`를 반환하는 것에 대해 생소하게 느껴질 수 있습니다. 그러나 이 덕분에 항상 API 토큰이 존재하며, 해당 토큰에 대해 `tokenCan`으로 권한을 검사할 수 있다고 가정할 수 있으므로, 애플리케이션의 인가 정책 내부 어디서든 `tokenCan`을 호출해 일관성 있게 권한 체크를 할 수 있습니다.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party. -->
인증이 반드시 필요한 라우트는 `routes/web.php` 및 `routes/api.php` 파일에서 해당 라우트에 `sanctum` 인증 가드를 적용하여 보호해야 합니다. 이 가드는 stateful(쿠키 인증) 방식이든, 서드파티 요청에서 API 토큰 헤더를 통해서든, 모든 경우에 요청이 인증되었는지 확인합니다.

<!-- You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance: -->
특히 `routes/web.php` 파일에서도 `sanctum` 가드를 적용하는 이유는, Sanctum이 먼저 Laravel의 세션 인증 쿠키를 우선적으로 사용해 요청을 인증하고, 쿠키가 없으면 요청의 `Authorization` 헤더 내 토큰을 사용하기 때문입니다. 모든 요청에 Sanctum 인증을 통일해서 적용하면, 현재 인증된 사용자 인스턴스에서 언제든지 `tokenCan`을 호출하여 토큰 권한 검증을 일관성 있게 할 수 있습니다.

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may "revoke" tokens by deleting them from your database using the `tokens` relationship that is provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
`Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 연관관계를 이용해 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기"할 수 있습니다.

```
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository. -->
Sanctum은 SPA(싱글 페이지 애플리케이션)에서 Laravel 기반 API와 통신해야 하는 경우에도 간단하게 인증을 처리할 수 있는 기능을 제공합니다. 이 SPA는 Laravel 프로젝트 안에 있어도 되고, 외부에 별도로 관리되는 프로젝트일 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능에서는 별도의 토큰을 발급하지 않고, Laravel의 쿠키 기반 세션 인증 서비스를 그대로 사용합니다. 이 방식은 CSRF 보호, 세션 기반 인증, 인증 정보가 XSS 등으로 외부에 노출되는 것을 막는 다양한 보안상의 장점을 제공합니다.

> [!NOTE]
> SPA와 API는 반드시 같은 최상위 도메인을 공유해야 인증이 가능합니다. 단, 서로 다른 서브도메인에서는 사용 가능합니다. 또한, 요청 시 `Accept: application/json` 헤더를 반드시 함께 보내야 합니다.

<a name="spa-configuration"></a>
<!-- ### Configuration -->
### Configuration

<a name="configuring-your-first-party-domains"></a>
<!-- #### Configuring Your First-Party Domains -->
#### Configuring Your First-Party Domains

<!-- First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API. -->
먼저, SPA가 요청을 보내는 도메인을 지정해야 합니다. Sanctum의 `sanctum` 설정 파일의 `stateful` 옵션에 도메인을 설정할 수 있습니다. 이 설정은 어떤 도메인이 Laravel 세션 쿠키와 함께 "stateful" 인증을 유지할 수 있을지를 결정합니다.

> [!NOTE]
> URL에 포트 번호(예: `127.0.0.1:8000`)가 포함된 경우 포트 번호까지 포함하여 도메인을 설정해야 합니다.

<a name="sanctum-middleware"></a>
<!-- #### Sanctum Middleware -->
#### Sanctum Middleware

<!-- Next, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file. This middleware is responsible for ensuring that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens: -->
그 다음 `app/Http/Kernel.php` 파일에서 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가해야 합니다. 이 미들웨어는 SPA가 세션 쿠키를 이용하여 인증할 수 있도록 해주며, 서드파티나 모바일 앱의 토큰 인증도 지원합니다.

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
<!-- #### CORS & Cookies -->
#### CORS & Cookies

<!-- If you are having trouble authenticating with your application from a SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings. -->
SPA가 별도의 서브도메인에서 Laravel 애플리케이션에 인증 요청을 보낼 때 인증이 잘 되지 않는다면, CORS(크로스-오리진 리소스 공유)나 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

<!-- You should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`. -->
먼저, CORS 설정에서 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되도록 해야 합니다. 이를 위해, 애플리케이션의 `config/cors.php` 설정 파일에서 `supports_credentials` 옵션을 `true`로 변경해야 합니다.

<!-- In addition, you should enable the `withCredentials` option on your application's global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client: -->
또한 프런트엔드에서 HTTP 요청을 보낼 때, `axios`의 경우 전역 설정에서 `withCredentials` 옵션도 켜야 합니다. 주로 `resources/js/bootstrap.js` 파일에서 다음과 같이 설정합니다. 만약 Axios 대신 다른 HTTP 클라이언트를 사용한다면, 해당 라이브러리의 방법에 맞게 동일하게 설정해야 합니다.

```
axios.defaults.withCredentials = true;
```

<!-- Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file: -->
마지막으로, 세션 쿠키가 루트 도메인의 모든 서브도메인에서 동작하도록 하려면, 애플리케이션의 `config/session.php`에서 도메인 값을 앞에 점(`.`)을 붙여 설정하십시오.

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
<!-- ### Authenticating -->
### Authenticating

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- To authenticate your SPA, your SPA's "login" page should first make a request to the `/sanctum/csrf-cookie` endpoint to initialize CSRF protection for the application: -->
SPA의 인증을 위해서는, 우선 "로그인" 페이지에서 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다.

```
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

<!-- During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the value of the `XSRF-TOKEN` cookie that is set by this route. -->
이 요청 시 Laravel은 현재 CSRF 토큰이 들어 있는 `XSRF-TOKEN` 쿠키를 응답에 포함시킵니다. 이 토큰은 이후의 요청에서 `X-XSRF-TOKEN` 헤더에 넣어주어야 하며, Axios나 Angular HttpClient 등 일부 HTTP 라이브러리는 이 과정을 자동으로 처리해줍니다. 만약 직접 사용하는 HTTP 라이브러리에서 자동으로 처리해주지 않는다면, 수동으로 `XSRF-TOKEN` 쿠키의 값을 읽어서 `X-XSRF-TOKEN` 헤더에 넣어주어야 합니다.

<a name="logging-in"></a>
<!-- #### Logging In -->
#### Logging In

<!-- Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/8.x/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/8.x/fortify). -->
CSRF 보호가 초기화되면, 이제 Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내 로그인 처리를 할 수 있습니다. 이 `/login` 라우트는 [implemented manually](/docs/8.x/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/8.x/fortify) 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

<!-- If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header. -->
로그인 요청에 성공하면 인증이 완료되고, 이후의 모든 요청에 자동으로 세션 쿠키가 포함되어 있으므로 별도의 작업 없이 인증 상태가 유지됩니다. 또한, 앞서 `/sanctum/csrf-cookie`에 요청한 덕분에 CSRF 보호도 정상적으로 적용됩니다(단, HTTP 클라이언트가 반드시 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 전송해야 함).

<!-- Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page. -->
만약 일정 시간 활동이 없어 세션이 만료되면, 이후의 요청에 대해 401 또는 419 HTTP 오류가 발생할 수 있습니다. 이 경우 사용자를 SPA의 로그인 페이지로 리다이렉트해야 합니다.

> [!NOTE]
> `/login` 엔드포인트를 직접 작성해도 상관 없습니다. 단, [session based authentication services that Laravel provides](/docs/8.x/authentication#authenticating-users)를 통해 인증을 처리하도록 구현해야 하며, 대개 `web` 인증 가드를 사용해야 합니다.

<a name="protecting-spa-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party: -->
API 라우트를 인증이 필요한 상태로 보호하려면, `routes/api.php` 파일의 해당 라우트에 `sanctum` 인증 가드를 적용하세요. 이 가드는 SPA에서 온 stateful 인증 요청에는 세션 쿠키를, 서드파티 요청에는 API 토큰 헤더 인증을 지원합니다.

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
<!-- ### Authorizing Private Broadcast Channels -->
### Authorizing Private Broadcast Channels

<!-- If your SPA needs to authenticate with [private / presence broadcast channels](/docs/8.x/broadcasting#authorizing-channels), you should place the `Broadcast::routes` method call within your `routes/api.php` file: -->
SPA에서 [private / presence broadcast channels](/docs/8.x/broadcasting#authorizing-channels) 인증이 필요하다면, `routes/api.php` 파일에 `Broadcast::routes` 메서드를 다음과 같이 작성해야 합니다.

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

<!-- Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/8.x/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies): -->
그리고 Pusher의 인증 요청이 올바르게 처리되도록, [Laravel Echo](/docs/8.x/broadcasting#client-side-installation)를 초기화할 때 Pusher의 `authorizer` 옵션을 커스텀으로 지정해 주어야 합니다. 이렇게 하면 [properly configured for cross-domain requests](#cors-and-cookies) `axios` 인스턴스를 사용할 수 있습니다.

```
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: process.env.MIX_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a name="mobile-application-authentication"></a>
<!-- ## Mobile Application Authentication -->
## Mobile Application Authentication

<!-- You may also use Sanctum tokens to authenticate your mobile application's requests to your API. The process for authenticating mobile application requests is similar to authenticating third-party API requests; however, there are small differences in how you will issue the API tokens. -->
모바일 애플리케이션의 API 요청을 인증하려면 Sanctum 토큰을 사용할 수 있습니다. 모바일 인증 방식은 서드파티 API 요청 인증 방식과 유사하지만, 토큰 발급 방법에 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 12". -->
먼저, 사용자의 이메일/이름, 비밀번호, 그리고 기기 이름(device name)을 받아서 새로운 Sanctum 토큰을 발급해주는 라우트를 만듭니다. 이때의 "기기 이름" 값은 단순 참고용으로 어떤 문자열이든 지정할 수 있지만, 사용자가 쉽게 식별할 수 있게(예: "민수의 iPhone 12") 지정하는 것이 좋습니다.

<!-- Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests: -->
보통은 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내 토큰을 받고, 발급된 API 토큰을 디바이스에 저장하여 이후 추가적인 API 요청에 사용합니다.

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

<!-- When the mobile application uses the token to make an API request to your application, it should pass the token in the `Authorization` header as a `Bearer` token. -->
모바일 앱이 API 요청 시에는 토큰을 `Authorization` 헤더에 `Bearer` 토큰 형식으로 포함해 전달해야 합니다.

> [!TIP]
> 모바일 앱에 토큰을 발급할 때도 [token abilities](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes: -->
앞서 살펴본 것과 같이, `sanctum` 인증 가드를 라우트에 적용하여 모든 요청이 인증되었는지 확인할 수 있습니다.

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
모바일 기기에 발급된 API 토큰을 사용자가 폐기(무효화)할 수 있도록 하려면, 웹 애플리케이션의 '계정 설정' UI 등에서 토큰 이름과 함께 "폐기" 버튼을 제공하는 것이 좋습니다. 사용자가 폐기 버튼을 누르면 데이터베이스에서 해당 토큰을 삭제하면 됩니다. 토큰 목록은 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 연관관계를 통해 조회할 수 있습니다.

```
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, the `Sanctum::actingAs` method may be used to authenticate a user and specify which abilities should be granted to their token: -->
테스트 환경에서는, `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 해당 토큰에 특정 권한을 지정할 수 있습니다.

```
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved()
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

<!-- If you would like to grant all abilities to the token, you should include `*` in the ability list provided to the `actingAs` method: -->
만약 토큰에 모든 권한을 부여하고 싶다면, `actingAs` 메서드의 권한 목록에 `*`를 포함하면 됩니다.

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
