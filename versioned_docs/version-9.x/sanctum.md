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
[Laravel Sanctum](https://github.com/laravel/sanctum)은 싱글 페이지 애플리케이션(SPA), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가볍고 효율적인 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰에는 권한(abilities)이나 범위(scopes)를 지정하여, 토큰이 수행할 수 있는 작업을 세밀하게 제어할 수 있습니다.

<a name="how-it-works"></a>
<!-- ### How It Works -->
### How It Works

<!-- Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library. -->
Laravel Sanctum은 서로 다른 두 가지 문제를 해결하기 위해 만들어졌습니다. 각 문제에 대해 간단히 살펴본 후, 라이브러리의 세부 사항을 알아보겠습니다.

<a name="how-it-works-api-tokens"></a>
<!-- #### API Tokens -->
#### API Tokens

<!-- First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime. -->
Sanctum은 우선 OAuth 같은 복잡한 방식이 아닌, 간단하게 사용자에게 API 토큰을 발급할 수 있도록 도와주는 패키지입니다. 이 기능은 GitHub 등 여러 서비스에서 제공하는 "개인용 접근 토큰"에서 영감을 받아 만들어졌습니다. 예를 들어, 여러분의 애플리케이션 내 "계정 설정" 화면에서 사용자가 자신의 계정용 API 토큰을 직접 생성할 수 있다고 가정해봅시다. Sanctum은 이러한 토큰을 쉽게 생성하고 관리할 수 있게 도와줍니다. 이 토큰들은 보통 매우 긴 만료 기간(수년)을 가지지만, 사용자가 직접 언제든지 토큰을 수동으로 회수(삭제)할 수 있습니다.

<!-- Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token. -->
Laravel Sanctum은 모든 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, 들어오는 HTTP 요청의 `Authorization` 헤더에 유효한 API 토큰이 포함되어 있는지 확인하여 인증을 처리합니다.

<a name="how-it-works-spa-authentication"></a>
<!-- #### SPA Authentication -->
#### SPA Authentication

<!-- Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI or a Next.js application. -->
둘째, Sanctum은 Laravel 기반 API와 통신하는 싱글 페이지 애플리케이션(SPA)을 인증하는 간단한 방식을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소(repo)에 있을 수도 있고, 별도의 저장소(예: Vue CLI로 만든 SPA, Next.js 애플리케이션 등)에 있을 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능에서는 별도의 토큰을 사용하지 않습니다. Sanctum은 Laravel의 기본 쿠키 기반 세션 인증 기능을 그대로 활용합니다. 일반적으로 이 방식을 위해 Laravel의 `web` 인증 가드가 사용됩니다. 이 방법은 CSRF 보호, 세션 인증, 그리고 인증 정보가 XSS를 통해 노출되는 위험을 막는 등 여러 보안상 이점을 함께 제공합니다.

<!-- Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token. -->
Sanctum은 오직 여러분의 SPA 프론트엔드에서 시작된 요청에 대해서만 쿠키 기반 인증을 시도합니다. 들어오는 HTTP 요청을 처리할 때, 먼저 인증 쿠키가 있는지 확인하고(있다면 세션 기반 인증), 쿠키가 없다면 `Authorization` 헤더를 확인해서 유효한 API 토큰이 있는지 검사합니다.

> [!NOTE]
> Sanctum의 단일 기능만 사용해도 전혀 문제 없습니다. 즉, API 토큰 인증만 하거나 SPA 인증만 사용할 수 있습니다. Sanctum을 사용한다고 두 가지 모두 반드시 써야 하는 것은 아닙니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!NOTE]
> 최신 버전의 Laravel에는 Sanctum이 이미 포함되어 있습니다. 하지만 애플리케이션의 `composer.json`에 `laravel/sanctum`이 없다면, 아래 설명에 따라 직접 설치하면 됩니다.

<!-- You may install Laravel Sanctum via the Composer package manager: -->
Composer 패키지 매니저를 이용해 Laravel Sanctum을 설치할 수 있습니다:

```shell
composer require laravel/sanctum
```

<!-- Next, you should publish the Sanctum configuration and migration files using the `vendor:publish` Artisan command. The `sanctum` configuration file will be placed in your application's `config` directory: -->
다음으로, `vendor:publish` 아티즌 명령어를 사용해 Sanctum의 설정 파일과 마이그레이션 파일을 발행합니다. `sanctum` 설정 파일은 애플리케이션의 `config` 디렉터리에 생성됩니다.

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

<!-- Finally, you should run your database migrations. Sanctum will create one database table in which to store API tokens: -->
마지막으로, 데이터베이스 마이그레이션을 실행해야 합니다. Sanctum은 API 토큰을 저장할 하나의 데이터베이스 테이블을 생성합니다:

```shell
php artisan migrate
```

<!-- Next, if you plan to utilize Sanctum to authenticate a SPA, you should add Sanctum's middleware to your `api` middleware group within your application's `app/Http/Kernel.php` file: -->
만약 SPA 인증도 함께 사용하려 한다면, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 아래와 같이 Sanctum 미들웨어를 추가해야 합니다:

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
Sanctum의 기본 마이그레이션을 사용하지 않을 예정이라면, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 또는, 아래 명령어로 기본 마이그레이션 파일만 따로 내보낼 수도 있습니다: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum: -->
보통은 필요 없지만, Sanctum에서 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장해서 커스터마이즈할 수 있습니다:

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

<!-- Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of one of your application's service providers: -->
그런 다음, Sanctum이 여러분의 커스텀 모델을 사용하도록 `usePersonalAccessTokenModel` 메서드를 호출합니다. 보통 이 코드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 안에 작성합니다.

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

> [!NOTE]
> 여러분이 직접 만든 SPA에서 인증할 때는 API 토큰을 사용해서는 안 됩니다. 이 경우에는 Sanctum의 [SPA authentication features](#spa-authentication)을 활용하세요.

<a name="issuing-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token. -->
Sanctum을 활용하면, API 요청을 인증하기 위한 API 토큰 또는 개인용 접근 토큰을 손쉽게 발급할 수 있습니다. API 토큰을 사용하는 경우, 해당 토큰을 `Authorization` 헤더의 `Bearer` 토큰 형식으로 포함시켜 요청해야 합니다.

<!-- To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait: -->
토큰 발급을 시작하려면, User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 추가해야 합니다:

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created: -->
토큰 발급은 `createToken` 메서드를 사용합니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. 발급된 API 토큰은 SHA-256 해시로 데이터베이스에 저장되지만, 토큰이 생성된 직후 `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 원본 토큰 값을 얻을 수 있습니다. 이 값은 반드시 토큰 생성 직후 사용자에게 보여주어야 합니다:

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

<!-- You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait: -->
`HasApiTokens` 트레이트에서 제공하는 Eloquent 연관관계인 `tokens`를 이용해 사용자의 모든 토큰을 조회할 수도 있습니다:

```
foreach ($user->tokens as $token) {
    //
}
```

<a name="token-abilities"></a>
<!-- ### Token Abilities -->
### Token Abilities

<!-- Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method: -->
Sanctum에서는 토큰에 "권한(abilities)"을 지정할 수 있습니다. 권한은 OAuth의 "scopes"와 비슷한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 권한 리스트를 전달할 수 있습니다:

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

<!-- When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` method: -->
Sanctum 인증된 요청을 처리할 때, 토큰에 특정 권한이 있는지 `tokenCan` 메서드로 확인할 수 있습니다:

```
if ($user->tokenCan('server:update')) {
    //
}
```

<a name="token-ability-middleware"></a>
<!-- #### Token Ability Middleware -->
#### Token Ability Middleware

<!-- Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, add the following middleware to the `$routeMiddleware` property of your application's `app/Http/Kernel.php` file: -->
Sanctum에는, 요청을 인증할 때 해당 토큰에 특정 권한이 부여되어 있는지 확인할 수 있도록 해주는 두 가지 미들웨어가 포함되어 있습니다. 먼저, 아래 미들웨어를 애플리케이션의 `app/Http/Kernel.php` 파일 내 `$routeMiddleware` 속성에 추가하세요:

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

<!-- The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities: -->
`abilities` 미들웨어는 지정된 모든 권한을 토큰이 반드시 가지고 있어야 라우트 요청을 허용합니다:

```
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

<!-- The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities: -->
`ability` 미들웨어는 지정된 권한 중 하나라도 토큰이 가지고 있으면 라우트 요청을 허용합니다:

```
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
<!-- #### First-Party UI Initiated Requests -->
#### First-Party UI Initiated Requests

<!-- For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication). -->
편의상, 자체 SPA에서 발생한 인증된 요청에 대해 `tokenCan` 메서드는 무조건 `true`를 반환합니다. (즉, 여러분이 Sanctum의 [SPA authentication](#spa-authentication)을 사용하고 있는 경우에 한함)

<!-- However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/9.x/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action. -->
하지만, 이것이 무조건 사용자가 모든 작업을 수행할 수 있음을 의미하지는 않습니다. 실제로는 [authorization policies](/docs/9.x/authorization#creating-policies)이 해당 권한이 부여되었는지와 함께, 사용자 인스턴스 자체가 해당 작업을 수행할 수 있는지도 함께 검사하게 됩니다.

<!-- For example, if we imagine an application that manages servers, this might mean checking that token is authorized to update servers **and** that the server belongs to the user: -->
예를 들어, 서버 관리 애플리케이션이라면 토큰이 서버 업데이트 권한을 가지고 있을 뿐 아니라, 해당 서버가 현재 사용자 소유임도 함께 검사해야 합니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

<!-- At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorizations policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers. -->
이처럼 자체(1st-party) UI에서 발생한 요청에 대해 `tokenCan`이 항상 `true`를 반환하는 것이 처음에는 다소 생소할 수 있습니다. 하지만, 이렇게 하면 항상 API 토큰이 존재한다고 가정하고, 언제든지 `tokenCan`을 통해 권한을 검사할 수 있어 정책 코드가 더 간단해집니다. 요청이 UI에서 발생했는지, 외부 API 소비자에서 발생했는지 신경쓰지 않고 `tokenCan`을 호출할 수 있으므로 편리합니다.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party. -->
모든 들어오는 요청에 대해 인증을 강제하려면, `routes/web.php` 또는 `routes/api.php` 라우트 파일에서 보호하려는 라우트에 `sanctum` 인증 가드를 적용해야 합니다. 이 가드를 사용하면 요청이 상태를 가진(쿠키 기반 인증) 요청이든, 또는 외부에서 오는 API 토큰 인증이든 모두 처리할 수 있습니다.

<!-- You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance: -->
특히 `routes/web.php` 파일에서 `sanctum` 가드를 직접 사용하도록 안내하는 이유는, Sanctum이 우선적으로 Laravel의 일반적인 세션 인증 쿠키를 통해 인증을 시도하기 때문입니다. 만약 쿠키가 없다면 그 다음에 요청의 `Authorization` 헤더에 토큰이 있는지 확인합니다. 이렇게 모든 요청에 대해 Sanctum으로 인증하면, 언제든지 현재 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 사용할 수 있습니다:

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
토큰을 더이상 사용하지 않게 하려면(=회수), `Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 연관관계를 통해 해당 토큰을 데이터베이스에서 삭제하면 됩니다:

```
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
기본적으로 Sanctum의 토큰은 만료되지 않으며, 오직 [revoking the token](#revoking-tokens)할 때만 무효화됩니다. 하지만 원한다면 `sanctum` 설정 파일의 `expiration` 옵션을 통해 API 토큰의 만료 시간을 분 단위로 설정할 수 있습니다:

```php
'expiration' => 525600,
```

<!-- If you have configured a token expiration time for your application, you may also wish to [schedule a task](/docs/9.x/scheduling) to prune your application's expired tokens. Thankfully, Sanctum includes a `sanctum:prune-expired` Artisan command that you may use to accomplish this. For example, you may configure a scheduled tasks to delete all expired token database records that have been expired for at least 24 hours: -->
만약 토큰 만료 시간을 설정했다면, 만료된 토큰을 정기적으로 정리(삭제)하도록 [schedule a task](/docs/9.x/scheduling)을 등록하는 것이 좋습니다. 다행히 Sanctum에선 만료된 토큰을 삭제하는 `sanctum:prune-expired` 아티즌 명령어를 제공합니다. 예시로, 만료된 지 24시간이 지난 토큰 레코드를 매일 삭제하도록 예약할 수 있습니다:

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository. -->
Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 간단하게 인증하기 위한 메서드도 제공합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도, 별도의 저장소일 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능에서는 별도 토큰을 사용하지 않고, Laravel의 내장 쿠키 기반 세션 인증 서비스를 그대로 활용합니다. 이런 접근 방식은 CSRF 보호, 세션 인증, 인증 자격 증명의 XSS(스크립트 삽입 공격)로 인한 유출 방지 등 여러 장점을 제공합니다.

> [!WARNING]
> SPA와 API가 반드시 동일한 최상위 도메인을 공유해야 인증이 가능합니다. 하지만 서로 다른 서브도메인에 위치해 있어도 무방합니다. 또한, 요청 보낼 때 `Accept: application/json` 헤더가 포함되어 있어야 합니다.

<a name="spa-configuration"></a>
<!-- ### Configuration -->
### Configuration

<a name="configuring-your-first-party-domains"></a>
<!-- #### Configuring Your First-Party Domains -->
#### Configuring Your First-Party Domains

<!-- First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API. -->
먼저, SPA가 어느 도메인에서 요청을 보낼지 지정해야 합니다. 이는 `sanctum` 설정 파일의 `stateful` 옵션에서 지정할 수 있습니다. 이 옵션 목록에 추가된 도메인에서 들어오는 요청에 대해서는 Laravel 세션 쿠키를 통해 "상태를 유지(stateful)"하며 인증하게 됩니다.

> [!WARNING]
> 포트가 포함된 URL(예: `127.0.0.1:8000`)로 접속 중이라면, 반드시 domain에 포트 번호까지 포함해야 합니다.

<a name="sanctum-middleware"></a>
<!-- #### Sanctum Middleware -->
#### Sanctum Middleware

<!-- Next, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file. This middleware is responsible for ensuring that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens: -->
다음으로, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가합니다. 이러한 미들웨어를 적용해야 SPA 프론트엔드에서 세션 쿠키 인증을 이용할 수 있으며, 외부나 모바일 앱에서는 계속해서 토큰 인증을 사용할 수 있습니다:

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
별도의 서브도메인에서 실행되는 SPA가 인증에 실패한다면, CORS(크로스 도메인) 또는 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

<!-- You should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`. -->
CORS 설정에서 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되고 있는지 확인하세요. 이는 `config/cors.php`의 `supports_credentials` 옵션을 `true`로 설정해 처리할 수 있습니다.

<!-- In addition, you should enable the `withCredentials` option on your application's global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client: -->
또한, 프론트엔드에서 `axios`를 사용한다면 반드시 전역 인스턴스에서 `withCredentials` 옵션을 활성화해야 합니다. 보통 이 설정은 `resources/js/bootstrap.js` 파일에 작성합니다. axios 대신 다른 HTTP 클라이언트를 쓴다면 해당 방식에 맞게 설정하세요:

```js
axios.defaults.withCredentials = true;
```

<!-- Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file: -->
마지막으로, 루트 도메인 아래 모든 서브도메인에서 세션 쿠키를 사용할 수 있게 쿠키 도메인 설정을 맞추어야 합니다. `config/session.php` 설정 파일에서 domain 앞에 점(`.`)을 붙여주세요:

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
SPA에서 인증할 때, 먼저 login 페이지에서 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 CSRF 보호를 활성화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

<!-- During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the value of the `XSRF-TOKEN` cookie that is set by this route. -->
이 요청을 보내면 Laravel에서 현재 CSRF 토큰이 포함된 `XSRF-TOKEN` 쿠키를 설정해줍니다. 이 토큰은 이후 요청 들에서 `X-XSRF-TOKEN` 헤더에 같이 보내야 하며, axios나 Angular HttpClient 등 일부 HTTP 클라이언트는 이를 자동으로 처리합니다. 만약 여러분이 사용하는 자바스크립트 HTTP 라이브러리가 자동으로 처리해주지 않는다면, 반드시 `XSRF-TOKEN` 쿠키 값을 직접 `X-XSRF-TOKEN` 헤더로 넣어야 합니다.

<a name="logging-in"></a>
<!-- #### Logging In -->
#### Logging In

<!-- Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/9.x/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/9.x/fortify). -->
CSRF 보호가 설정됐다면, 이제 Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내 인증할 수 있습니다. `/login` 라우트는 [implemented manually](/docs/9.x/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/9.x/fortify)와 같은 헤드리스 인증 패키지로 제공해도 됩니다.

<!-- If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header. -->
로그인 요청에 성공하면 인증이 완료되고, 이후의 모든 요청에는 Laravel에서 발급한 세션 쿠키가 자동으로 함께 전송되어 인증이 계속 유지됩니다. 또한, 이미 `/sanctum/csrf-cookie`로 CSRF 토큰을 받아왔기 때문에, 자바스크립트 HTTP 클라이언트가 `XSRF-TOKEN` 값을 적절하게 `X-XSRF-TOKEN` 헤더로 보내는 한 추가 설정 없이 CSRF 보호가 계속 동작합니다.

<!-- Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page. -->
물론, 사용자의 세션이 만료된 상태(오랜 시간 활동 없음 등)에서 요청을 보낼 경우 HTTP 401 또는 419 에러가 발생할 수 있습니다. 이때는 SPA의 로그인 페이지로 유저를 다시 이동시키는 등의 처리가 필요합니다.

> [!WARNING]
> 직접 `/login` 엔드포인트를 만들어도 상관 없으나, 반드시 Laravel이 제공하는 표준 [session based authentication services that Laravel provides](/docs/9.x/authentication#authenticating-users)로 사용자 인증이 이뤄져야 합니다. 보통 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party: -->
SPA에서 인증된 요청만 허용하려면 `routes/api.php` 내 API 라우트에 `sanctum` 인증 가드를 적용해야 합니다. 이 가드를 사용하면 SPA 프런트엔드에서 오는 상태를 가진(stateful) 인증 요청과 외부에서 오는 토큰 기반 인증 요청을 모두 처리할 수 있습니다:

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
<!-- ### Authorizing Private Broadcast Channels -->
### Authorizing Private Broadcast Channels

<!-- If your SPA needs to authenticate with [private / presence broadcast channels](/docs/9.x/broadcasting#authorizing-channels), you should place the `Broadcast::routes` method call within your `routes/api.php` file: -->
SPA 앱이 [private / presence broadcast channels](/docs/9.x/broadcasting#authorizing-channels)에 인증해야 한다면, `routes/api.php` 파일에 `Broadcast::routes` 호출을 추가해야 합니다:

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

<!-- Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/9.x/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies): -->
그리고, Pusher의 인가 요청이 제대로 동작하려면 [Laravel Echo](/docs/9.x/broadcasting#client-side-installation)를 초기화할 때 `axios`가 [properly configured for cross-domain requests](#cors-and-cookies) 세팅되었는지, 그리고 다음 예시처럼 커스텀 Pusher `authorizer`를 지정해야 합니다:

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
Sanctum 토큰을 이용해 모바일 애플리케이션에서도 API 요청 인증이 가능합니다. 모바일 앱의 인증 흐름은 외부 API 소비자 인증과 거의 동일하지만, 토큰 발급 방식에 일부 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 12". -->
우선, 사용자의 이메일/유저명, 비밀번호, 디바이스명을 받아 새로운 Sanctum 토큰을 발급해주는 라우트를 만듭니다. 이때 "디바이스명"은 토큰을 식별하기 위한 용도로 사용자에게 의미 있는 값을 넣으면 됩니다. (예: "Nuno의 iPhone 12"와 같이)

<!-- Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests: -->
일반적으로 모바일 앱의 "로그인" 화면에서 토큰 엔드포인트로 해당 정보를 보내 토큰을 받게 되며, 앱 내에 이 토큰을 저장하고 추가적인 API 요청에 활용합니다:

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
모바일 애플리케이션에서 이 토큰을 이용해 API 요청 할 때는 `Authorization` 헤더에 `Bearer` 토큰 형식으로 포함해 전송하면 됩니다.

> [!NOTE]
> 모바일 앱을 위한 토큰 발급 시에도 [token abilities](#token-abilities)을 자유롭게 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes: -->
앞서 소개한 대로, 모든 요청에 대해 인증을 강제하려면 해당 라우트에 `sanctum` 인증 가드를 적용하면 됩니다:

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
모바일 기기에 발급된 토큰 또한 사용자가 직접 회수하도록, 웹 애플리케이션 내 "계정 설정" 페이지에 토큰 목록 및 "회수" 버튼을 추가할 수 있습니다. 사용자가 버튼을 누르면 해당 토큰을 데이터베이스에서 삭제하게 처리하면 됩니다. 사용자의 API 토큰 목록은 역시 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 연관관계를 활용하면 됩니다:

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
테스트 시에는 `Sanctum::actingAs` 메서드를 사용해 특정 사용자로 인증하고, 해당 토큰에 부여할 권한(ability)도 지정할 수 있습니다:

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
토큰에 모든 권한을 부여할 경우, `actingAs` 메서드의 권한 리스트에 `*`를 추가하면 됩니다:

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
