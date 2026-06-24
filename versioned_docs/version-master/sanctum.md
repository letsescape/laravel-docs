<!-- # Laravel Sanctum -->
# Laravel Sanctum

- [Introduction](#introduction)
    - [How it Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Overriding Default Models](#overriding-default-models)
- [API Token Authentication](#api-token-authentication)
    - [Issuing API Tokens](#issuing-api-tokens)
    - [Token Abilities](#token-abilities)
    - [Protecting Routes](#protecting-routes)
    - [Revoking Tokens](#revoking-tokens)
    - [Token Expiration](#token-expiration)
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
[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 매우 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 API 토큰을 생성할 수 있습니다. 이러한 토큰에는 해당 토큰이 수행할 수 있는 작업을 지정하는 능력 / 스코프를 부여할 수 있습니다.

<a name="how-it-works"></a>
<!-- ### How it Works -->
### How it Works

<!-- Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library. -->
Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 자세히 살펴보기 전에 각각을 먼저 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
<!-- #### API Tokens -->
#### API Tokens

<!-- First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user anytime. -->
첫째, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급하는 데 사용할 수 있는 단순한 패키지입니다. 이 기능은 "personal access tokens"를 발급하는 GitHub 및 기타 애플리케이션에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "account settings"에 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있는 화면이 있다고 가정해 보겠습니다. Sanctum을 사용하여 이러한 토큰을 생성하고 관리할 수 있습니다. 이러한 토큰은 일반적으로 만료 시간이 매우 길지만(몇 년), 사용자가 언제든지 직접 폐기할 수 있습니다.

<!-- Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token. -->
Laravel Sanctum은 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, 유효한 API 토큰을 포함해야 하는 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증함으로써 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
<!-- #### SPA Authentication -->
#### SPA Authentication

<!-- Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as an SPA created using Next.js or Nuxt. -->
둘째, Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 인증하는 간단한 방법을 제공하기 위해 존재합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js나 Nuxt를 사용해 만든 SPA처럼 완전히 별도의 저장소에 있을 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능에서 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum은 Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum은 이를 수행하기 위해 Laravel의 `web` 인증 guard를 사용합니다. 이 방식은 CSRF 보호와 세션 인증의 이점을 제공하며, XSS를 통한 인증 자격 증명 유출도 방지합니다.

<!-- Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token. -->
Sanctum은 들어오는 요청이 여러분의 SPA 프론트엔드에서 온 경우에만 쿠키를 사용한 인증을 시도합니다. Sanctum이 들어오는 HTTP 요청을 검사할 때 먼저 인증 쿠키를 확인하고, 쿠키가 없으면 유효한 API 토큰이 있는지 `Authorization` 헤더를 검사합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용하는 것은 전혀 문제없습니다. Sanctum을 사용한다고 해서 Sanctum이 제공하는 두 기능을 모두 반드시 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Laravel Sanctum via the `install:api` Artisan command: -->
`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다.

```shell
php artisan install:api
```

<!-- Next, if you plan to utilize Sanctum to authenticate an SPA, please refer to the [SPA Authentication](#spa-authentication) section of this documentation. -->
다음으로, Sanctum을 사용하여 SPA를 인증할 계획이라면 이 문서의 [SPA Authentication](#spa-authentication) 섹션을 참고하십시오.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum: -->
일반적으로 필요하지는 않지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

<!-- Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of your application's `AppServiceProvider` file: -->
그런 다음 Sanctum이 제공하는 `usePersonalAccessTokenModel` 메서드를 통해 Sanctum이 사용자 지정 모델을 사용하도록 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일에 있는 `boot` 메서드에서 호출해야 합니다.

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
<!-- ## API Token Authentication -->
## API Token Authentication

> [!NOTE]
> 직접 만든 퍼스트파티 SPA를 인증하는 데 API 토큰을 사용해서는 안 됩니다. 대신 Sanctum에 내장된 [SPA authentication features](#spa-authentication)을 사용하십시오.

<a name="issuing-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token. -->
Sanctum을 사용하면 애플리케이션에 대한 API 요청을 인증하는 데 사용할 수 있는 API 토큰 / 개인 액세스 토큰을 발급할 수 있습니다. API 토큰을 사용해 요청할 때는 토큰을 `Bearer` 토큰으로 `Authorization` 헤더에 포함해야 합니다.

<!-- To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait: -->
사용자에게 토큰을 발급하려면 User 모델에서 `Laravel\Sanctum\HasApiTokens` trait를 사용해야 합니다.

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created: -->
토큰을 발급하려면 `createToken` 메서드를 사용할 수 있습니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해싱을 사용해 해시되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 사용하면 토큰의 평문 값을 가져올 수 있습니다. 토큰이 생성된 직후 이 값을 사용자에게 보여주어야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

<!-- You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait: -->
`HasApiTokens` trait가 제공하는 `tokens` Eloquent 연관관계를 사용하여 사용자의 모든 토큰에 접근할 수 있습니다.

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
<!-- ### Token Abilities -->
### Token Abilities

<!-- Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method: -->
Sanctum을 사용하면 토큰에 "능력"을 할당할 수 있습니다. 능력은 OAuth의 "스코프"와 비슷한 목적을 가집니다. `createToken` 메서드의 두 번째 인수로 문자열 능력 배열을 전달할 수 있습니다.

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

<!-- When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` or `tokenCant` methods: -->
Sanctum으로 인증된 들어오는 요청을 처리할 때, `tokenCan` 또는 `tokenCant` 메서드를 사용하여 토큰에 특정 능력이 있는지 확인할 수 있습니다.

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
<!-- #### Token Ability Middleware -->
#### Token Ability Middleware

<!-- Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, define the following middleware aliases in your application's `bootstrap/app.php` file: -->
Sanctum에는 들어오는 요청이 특정 능력을 부여받은 토큰으로 인증되었는지 확인하는 데 사용할 수 있는 두 개의 Middleware도 포함되어 있습니다. 시작하려면 애플리케이션의 `bootstrap/app.php` 파일에 다음 Middleware 별칭을 정의하십시오.

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

<!-- The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities: -->
`abilities` Middleware는 들어오는 요청의 토큰이 나열된 모든 능력을 가지고 있는지 확인하도록 라우트에 할당할 수 있습니다.

```php
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

<!-- The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities: -->
`ability` Middleware는 들어오는 요청의 토큰이 나열된 능력 중 *하나 이상*을 가지고 있는지 확인하도록 라우트에 할당할 수 있습니다.

```php
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
<!-- #### First-Party UI Initiated Requests -->
#### First-Party UI Initiated Requests

<!-- For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication). -->
편의를 위해, 들어오는 인증된 요청이 여러분의 퍼스트파티 SPA에서 온 것이고 Sanctum에 내장된 [SPA authentication](#spa-authentication)을 사용하고 있다면 `tokenCan` 메서드는 항상 `true`를 반환합니다.

<!-- However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/master/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action. -->
하지만 이것이 애플리케이션이 반드시 사용자에게 해당 작업 수행을 허용해야 한다는 의미는 아닙니다. 일반적으로 애플리케이션의 [authorization policies](/docs/master/authorization#creating-policies)이 토큰에 해당 능력을 수행할 권한이 부여되었는지 판단하고, 사용자 인스턴스 자체가 해당 작업을 수행할 수 있어야 하는지도 함께 확인합니다.

<!-- For example, if we imagine an application that manages servers, this might mean checking that the token is authorized to update servers **and** that the server belongs to the user: -->
예를 들어 서버를 관리하는 애플리케이션을 상상해 보면, 이는 토큰이 서버를 업데이트할 권한이 있는지 **그리고** 해당 서버가 사용자에게 속해 있는지를 확인하는 것을 의미할 수 있습니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

<!-- At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorization policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers. -->
처음에는 퍼스트파티 UI에서 시작된 요청에 대해 `tokenCan` 메서드를 호출할 수 있고 항상 `true`를 반환하도록 허용하는 것이 이상해 보일 수 있습니다. 하지만 API 토큰이 항상 사용 가능하며 `tokenCan` 메서드를 통해 검사할 수 있다고 가정할 수 있다는 점은 편리합니다. 이 접근 방식을 사용하면 요청이 애플리케이션 UI에서 발생했는지, 아니면 API의 서드파티 소비자 중 하나가 시작했는지 걱정하지 않고 애플리케이션의 인가 정책 내에서 항상 `tokenCan` 메서드를 호출할 수 있습니다.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party. -->
들어오는 모든 요청이 인증되어야 하도록 라우트를 보호하려면, `routes/web.php`와 `routes/api.php` 라우트 파일의 보호된 라우트에 `sanctum` 인증 guard를 연결해야 합니다. 이 guard는 들어오는 요청이 상태 유지 방식의 쿠키 인증 요청으로 인증되었거나, 서드파티에서 온 요청인 경우 유효한 API 토큰 헤더를 포함하는지 확인합니다.

<!-- You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance: -->
애플리케이션의 `routes/web.php` 파일에 있는 라우트를 `sanctum` guard로 인증하라고 권장하는 이유가 궁금할 수 있습니다. Sanctum은 먼저 Laravel의 일반적인 세션 인증 쿠키를 사용하여 들어오는 요청을 인증하려고 시도한다는 점을 기억하십시오. 해당 쿠키가 없으면 Sanctum은 요청의 `Authorization` 헤더에 있는 토큰을 사용하여 요청을 인증하려고 시도합니다. 또한 Sanctum을 사용하여 모든 요청을 인증하면 현재 인증된 사용자 인스턴스에서 언제나 `tokenCan` 메서드를 호출할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may "revoke" tokens by deleting them from your database using the `tokens` relationship that is provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
`Laravel\Sanctum\HasApiTokens` trait가 제공하는 `tokens` 연관관계를 사용해 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기"할 수 있습니다.

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
<!-- ### Token Expiration -->
### Token Expiration

<!-- By default, Sanctum tokens never expire and may only be invalidated by [revoking the token](#revoking-tokens). However, if you would like to configure an expiration time for your application's API tokens, you may do so via the `expiration` configuration option defined in your application's `sanctum` configuration file. This configuration option defines the number of minutes until an issued token will be considered expired: -->
기본적으로 Sanctum 토큰은 만료되지 않으며, [revoking the token](#revoking-tokens)해야만 무효화할 수 있습니다. 하지만 애플리케이션의 API 토큰에 만료 시간을 설정하고 싶다면, 애플리케이션의 `sanctum` 설정 파일에 정의된 `expiration` 설정 옵션을 통해 설정할 수 있습니다. 이 설정 옵션은 발급된 토큰이 만료된 것으로 간주되기까지의 시간을 분 단위로 정의합니다.

```php
'expiration' => 525600,
```

<!-- If you would like to specify the expiration time of each token independently, you may do so by providing the expiration time as the third argument to the `createToken` method: -->
각 토큰의 만료 시간을 독립적으로 지정하고 싶다면, `createToken` 메서드의 세 번째 인수로 만료 시간을 제공하면 됩니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

<!-- If you have configured a token expiration time for your application, you may also wish to [schedule a task](/docs/master/scheduling) to prune your application's expired tokens. Thankfully, Sanctum includes a `sanctum:prune-expired` Artisan command that you may use to accomplish this. For example, you may configure a scheduled task to delete all expired token database records that have been expired for at least 24 hours: -->
애플리케이션에 토큰 만료 시간을 설정했다면, 애플리케이션의 만료된 토큰을 정리하기 위해 [schedule a task](/docs/master/scheduling)하고 싶을 수도 있습니다. 다행히 Sanctum에는 이를 수행하는 데 사용할 수 있는 `sanctum:prune-expired` Artisan 명령어가 포함되어 있습니다. 예를 들어, 최소 24시간 전에 만료된 모든 만료 토큰 데이터베이스 레코드를 삭제하도록 예약 작업을 설정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository. -->
Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 인증하는 간단한 방법도 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, 완전히 별도의 저장소에 있을 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능에서 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum은 Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 이 인증 방식은 CSRF 보호와 세션 인증의 이점을 제공하며, XSS를 통한 인증 자격 증명 유출도 방지합니다.

> [!WARNING]
> 인증을 위해서는 SPA와 API가 동일한 최상위 도메인을 공유해야 합니다. 하지만 서로 다른 하위 도메인에 배치될 수는 있습니다. 또한 요청에 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더 중 하나를 반드시 함께 보내야 합니다.

<a name="spa-configuration"></a>
<!-- ### Configuration -->
### Configuration

<a name="configuring-your-first-party-domains"></a>
<!-- #### Configuring Your First-Party Domains -->
#### Configuring Your First-Party Domains

<!-- First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API. -->
먼저 SPA가 어떤 도메인에서 요청을 보낼지 설정해야 합니다. 이러한 도메인은 `sanctum` 설정 파일의 `stateful` 설정 옵션을 사용하여 구성할 수 있습니다. 이 설정은 API에 요청할 때 Laravel 세션 쿠키를 사용하여 "상태 유지" 인증을 유지할 도메인을 결정합니다.

<!-- To assist you in setting up your first-party stateful domains, Sanctum provides two helper functions that you can include in the configuration. First, `Sanctum::currentApplicationUrlWithPort()` will return the current application URL from the `APP_URL` environment variable, and `Sanctum::currentRequestHost()` will inject a placeholder into the stateful domain list which, at runtime, will be replaced by the host from the current request so that all requests with the same domain are considered stateful. -->
퍼스트파티 상태 유지 도메인을 설정하는 데 도움을 주기 위해 Sanctum은 설정에 포함할 수 있는 두 가지 헬퍼 함수를 제공합니다. 먼저 `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경 변수에서 현재 애플리케이션 URL을 반환합니다. 그리고 `Sanctum::currentRequestHost()`는 상태 유지 도메인 목록에 플레이스홀더를 삽입하며, 런타임에는 현재 요청의 호스트로 대체됩니다. 따라서 동일한 도메인의 모든 요청이 상태 유지 요청으로 간주됩니다.

> [!WARNING]
> 포트가 포함된 URL(`127.0.0.1:8000`)을 통해 애플리케이션에 접근하는 경우, 도메인에 포트 번호를 포함해야 합니다.

<a name="sanctum-middleware"></a>
<!-- #### Sanctum Middleware -->
#### Sanctum Middleware

<!-- Next, you should instruct Laravel that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens. This can be easily accomplished by invoking the `statefulApi` middleware method in your application's `bootstrap/app.php` file: -->
다음으로, SPA에서 들어오는 요청은 Laravel의 세션 쿠키를 사용해 인증할 수 있도록 하고, 동시에 서드파티나 모바일 애플리케이션에서 오는 요청은 API 토큰을 사용해 인증할 수 있도록 Laravel에 지시해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `statefulApi` Middleware 메서드를 호출하여 쉽게 수행할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
<!-- #### CORS and Cookies -->
#### CORS and Cookies

<!-- If you are having trouble authenticating with your application from an SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings. -->
별도의 하위 도메인에서 실행되는 SPA에서 애플리케이션 인증에 문제가 있다면, CORS(Cross-Origin Resource Sharing) 또는 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

<!-- The `config/cors.php` configuration file is not published by default. If you need to customize Laravel's CORS options, you should publish the complete `cors` configuration file using the `config:publish` Artisan command: -->
`config/cors.php` 설정 파일은 기본적으로 공개되지 않습니다. Laravel의 CORS 옵션을 사용자 지정해야 한다면, `config:publish` Artisan 명령어를 사용하여 전체 `cors` 설정 파일을 공개해야 합니다.

```shell
php artisan config:publish cors
```

<!-- Next, you should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`. -->
다음으로, 애플리케이션의 CORS 설정이 `True` 값을 가진 `Access-Control-Allow-Credentials` 헤더를 반환하는지 확인해야 합니다. 이는 애플리케이션의 `config/cors.php` 설정 파일에서 `supports_credentials` 옵션을 `true`로 설정하여 수행할 수 있습니다.

<!-- In addition, you should enable the `withCredentials` and `withXSRFToken` options on your application's global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client: -->
또한 애플리케이션의 전역 `axios` 인스턴스에서 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 일반적으로 이는 `resources/js/bootstrap.js` 파일에서 수행해야 합니다. 프론트엔드에서 HTTP 요청을 보내는 데 Axios를 사용하지 않는다면, 사용 중인 HTTP 클라이언트에서 이에 해당하는 설정을 수행해야 합니다.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

<!-- Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file: -->
마지막으로, 애플리케이션의 세션 쿠키 도메인 설정이 루트 도메인의 모든 하위 도메인을 지원하는지 확인해야 합니다. 애플리케이션의 `config/session.php` 설정 파일에서 도메인 앞에 `.`을 붙이면 이를 수행할 수 있습니다.

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
<!-- ### Authenticating -->
### Authenticating

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- To authenticate your SPA, your SPA's "login" page should first make a request to the `/sanctum/csrf-cookie` endpoint to initialize CSRF protection for the application: -->
SPA를 인증하려면, SPA의 "login" 페이지에서 먼저 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

<!-- During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be URL decoded and passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the URL decoded value of the `XSRF-TOKEN` cookie that is set by this route. -->
이 요청 중에 Laravel은 현재 CSRF 토큰을 포함하는 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청에서는 이 토큰을 URL 디코딩한 뒤 `X-XSRF-TOKEN` 헤더에 전달해야 합니다. Axios나 Angular HttpClient 같은 일부 HTTP 클라이언트 라이브러리는 이를 자동으로 처리합니다. 사용 중인 JavaScript HTTP 라이브러리가 이 값을 자동으로 설정하지 않는다면, 이 라우트가 설정한 `XSRF-TOKEN` 쿠키의 URL 디코딩된 값과 일치하도록 `X-XSRF-TOKEN` 헤더를 직접 설정해야 합니다.

<a name="logging-in"></a>
<!-- #### Logging In -->
#### Logging In

<!-- Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/master/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/master/fortify). -->
CSRF 보호가 초기화되면 Laravel 애플리케이션의 `/login` 라우트로 `POST` 요청을 보내야 합니다. 이 `/login` 라우트는 [implemented manually](/docs/master/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/master/fortify)와 같은 헤드리스 인증 패키지를 사용하여 구현할 수도 있습니다.

<!-- If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header. -->
로그인 요청이 성공하면 인증된 상태가 되며, 이후 애플리케이션의 라우트에 대한 요청은 Laravel 애플리케이션이 클라이언트에 발급한 세션 쿠키를 통해 자동으로 인증됩니다. 또한 애플리케이션이 이미 `/sanctum/csrf-cookie` 라우트에 요청했으므로, JavaScript HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 보내는 한 이후 요청은 자동으로 CSRF 보호를 받습니다.

<!-- Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive a 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page. -->
물론 사용자의 세션이 활동 부족으로 만료되면, 이후 Laravel 애플리케이션에 대한 요청은 401 또는 419 HTTP 오류 응답을 받을 수 있습니다. 이 경우 사용자를 SPA의 로그인 페이지로 리디렉션해야 합니다.

> [!WARNING]
> 자체 `/login` 엔드포인트를 자유롭게 작성할 수 있습니다. 하지만 Laravel이 제공하는 표준 [session based authentication services that Laravel provides](/docs/master/authentication#authenticating-users)를 사용하여 사용자를 인증하도록 해야 합니다. 일반적으로 이는 `web` 인증 guard를 사용하는 것을 의미합니다.

<a name="protecting-spa-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party: -->
들어오는 모든 요청이 인증되어야 하도록 라우트를 보호하려면, `routes/api.php` 파일의 API 라우트에 `sanctum` 인증 guard를 연결해야 합니다. 이 guard는 들어오는 요청이 SPA에서 온 상태 유지 인증 요청으로 인증되었거나, 서드파티에서 온 요청인 경우 유효한 API 토큰 헤더를 포함하는지 확인합니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
<!-- ### Authorizing Private Broadcast Channels -->
### Authorizing Private Broadcast Channels

<!-- If your SPA needs to authenticate with [private / presence broadcast channels](/docs/master/broadcasting#authorizing-channels), you should remove the `channels` entry from the `withRouting` method contained in your application's `bootstrap/app.php` file. Instead, you should invoke the `withBroadcasting` method so that you may specify the correct middleware for your application's broadcasting routes: -->
SPA가 [private / presence broadcast channels](/docs/master/broadcasting#authorizing-channels)로 인증해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일에 있는 `withRouting` 메서드에서 `channels` 항목을 제거해야 합니다. 대신 애플리케이션의 브로드캐스팅 라우트에 올바른 Middleware를 지정할 수 있도록 `withBroadcasting` 메서드를 호출해야 합니다.

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
```

<!-- Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/master/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies): -->
다음으로 Pusher의 인가 요청이 성공하려면 [Laravel Echo](/docs/master/broadcasting#client-side-installation)를 초기화할 때 사용자 지정 Pusher `authorizer`를 제공해야 합니다. 이를 통해 애플리케이션은 Pusher가 [properly configured for cross-domain requests](#cors-and-cookies) `axios` 인스턴스를 사용하도록 구성할 수 있습니다.

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
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
Sanctum 토큰을 사용하여 모바일 애플리케이션이 API에 보내는 요청을 인증할 수도 있습니다. 모바일 애플리케이션 요청을 인증하는 과정은 서드파티 API 요청을 인증하는 과정과 비슷합니다. 다만 API 토큰을 발급하는 방식에는 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 12". -->
시작하려면 사용자의 이메일 / 사용자명, 비밀번호, 디바이스 이름을 받아 해당 자격 증명을 새 Sanctum 토큰으로 교환하는 라우트를 생성합니다. 이 엔드포인트에 전달되는 "디바이스 이름"은 참고용 정보이며, 원하는 어떤 값이든 사용할 수 있습니다. 일반적으로 디바이스 이름 값은 "Nuno's iPhone 12"처럼 사용자가 알아볼 수 있는 이름이어야 합니다.

<!-- Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests: -->
보통 모바일 애플리케이션의 "로그인" 화면에서 토큰 엔드포인트로 요청을 보냅니다. 엔드포인트는 평문 API 토큰을 반환하며, 이 토큰은 모바일 디바이스에 저장한 뒤 추가 API 요청을 보낼 때 사용할 수 있습니다.

```php
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
모바일 애플리케이션이 토큰을 사용하여 애플리케이션에 API 요청을 보낼 때는 `Authorization` 헤더에 `Bearer` 토큰으로 토큰을 전달해야 합니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰을 발급할 때 [token abilities](#token-abilities)를 지정할 수도 있습니다.

<a name="protecting-mobile-api-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes: -->
앞서 설명한 것처럼, 라우트에 `sanctum` 인증 가드를 연결하여 들어오는 모든 요청이 반드시 인증되도록 라우트를 보호할 수 있습니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
사용자가 모바일 디바이스에 발급된 API 토큰을 폐기할 수 있도록 하려면, 웹 애플리케이션 UI의 "계정 설정" 영역에서 토큰 이름과 함께 "폐기" 버튼을 표시할 수 있습니다. 사용자가 "폐기" 버튼을 클릭하면 데이터베이스에서 해당 토큰을 삭제할 수 있습니다. `Laravel\Sanctum\HasApiTokens` trait이 제공하는 `tokens` 연관관계를 통해 사용자의 API 토큰에 접근할 수 있다는 점을 기억하세요.

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, the `Sanctum::actingAs` method may be used to authenticate a user and specify which abilities should be granted to their token: -->
테스트 중에는 `Sanctum::actingAs` 메서드를 사용하여 사용자를 인증하고, 해당 토큰에 어떤 권한을 부여할지 지정할 수 있습니다.

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
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
토큰에 모든 권한을 부여하려면 `actingAs` 메서드에 전달하는 권한 목록에 `*`를 포함해야 합니다.

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
