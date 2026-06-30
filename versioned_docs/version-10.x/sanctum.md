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
[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 각각 수행할 수 있는 작업을 정의하는 권한(Ability) 또는 스코프(Scope)를 부여받을 수 있습니다.

<a name="how-it-works"></a>
<!-- ### How it Works -->
### How it Works

<!-- Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library. -->
Laravel Sanctum은 두 가지 별도의 문제를 해결하기 위해 만들어졌습니다. 본격적으로 라이브러리에 대해 살펴보기 전에 이 두 가지 문제를 각각 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
<!-- #### API Tokens -->
#### API Tokens

<!-- First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime. -->
우선, Sanctum은 OAuth처럼 복잡하지 않으면서 사용자에게 API 토큰을 발급할 수 있는 단순한 패키지입니다. 이 기능은 GitHub나 그 외 애플리케이션에서 제공하는 "개인 접근 토큰"에서 영감을 얻었습니다. 예를 들어, 여러분의 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대해 API 토큰을 직접 생성할 수 있는 화면을 만들 수 있습니다. Sanctum을 이용하면 이러한 토큰을 손쉽게 생성하고 관리할 수 있습니다. 이러한 토큰은 대개 유효기간이 매우 길게(수년 이상) 설정되지만, 사용자가 언제든 직접 토큰을 폐기(취소)할 수도 있습니다.

<!-- Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token. -->
Laravel Sanctum에서는 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, HTTP 요청의 `Authorization` 헤더에 존재하는 유효한 API 토큰을 이용해 인증을 처리합니다.

<a name="how-it-works-spa-authentication"></a>
<!-- #### SPA Authentication -->
#### SPA Authentication

<!-- Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI or a Next.js application. -->
두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 인증하는 간단한 방법을 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 동일한 저장소에 위치할 수도 있고, Vue CLI나 Next.js 등으로 별도의 저장소에 만들어졌을 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능을 위해 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신, Laravel의 내장 쿠키 기반 세션 인증 서비스를 이용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드를 사용해 이 작업을 수행합니다. 이 방식은 CSRF 보호, 세션 기반 인증, 및 XSS를 통한 인증 정보 노출 방지 등 다양한 장점을 제공합니다.

<!-- Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token. -->
Sanctum은 요청이 여러분의 SPA 프론트엔드에서 시작된 경우에만 쿠키 기반 인증을 시도합니다. Sanctum은 들어오는 HTTP 요청을 처리할 때 우선 인증 쿠키가 있는지 확인하며, 만약 쿠키가 없다면 그 다음으로 `Authorization` 헤더에 유효한 API 토큰이 있는지 확인합니다.

> [!NOTE]
> Sanctum을 오직 API 토큰 인증 용도로만 사용하거나, 오직 SPA 인증 용도로만 사용하는 것 모두 문제없습니다. Sanctum을 도입했다고 해서 반드시 두 가지 방식을 모두 써야 하는 것은 아닙니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!NOTE]
> 최신 버전의 Laravel은 이미 Laravel Sanctum이 포함되어 있습니다. 하지만, 애플리케이션의 `composer.json` 파일에 `laravel/sanctum`이 없다면 아래 설치 방법을 따라 추가할 수 있습니다.

<!-- You may install Laravel Sanctum via the Composer package manager: -->
Composer 패키지 매니저를 통해 Laravel Sanctum을 설치할 수 있습니다.

```shell
composer require laravel/sanctum
```

<!-- Next, you should publish the Sanctum configuration and migration files using the `vendor:publish` Artisan command. The `sanctum` configuration file will be placed in your application's `config` directory: -->
다음으로, `vendor:publish` Artisan 명령어를 실행하여 Sanctum의 설정 파일과 마이그레이션 파일을 배포해야 합니다. 이렇게 하면 `sanctum` 설정 파일이 애플리케이션의 `config` 디렉터리에 생성됩니다.

```shell
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

<!-- Finally, you should run your database migrations. Sanctum will create one database table in which to store API tokens: -->
마지막으로, 데이터베이스 마이그레이션을 실행하세요. Sanctum은 API 토큰을 저장하기 위한 하나의 테이블을 생성합니다.

```shell
php artisan migrate
```

<!-- Next, if you plan to utilize Sanctum to authenticate a SPA, you should add Sanctum's middleware to your `api` middleware group within your application's `app/Http/Kernel.php` file: -->
그리고, SPA 인증에 Sanctum을 활용할 계획이라면, 애플리케이션의 `app/Http/Kernel.php` 파일 내 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가해야 합니다.

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
<!-- #### Migration Customization -->
#### Migration Customization

<!-- If you are not going to use Sanctum's default migrations, you should call the `Sanctum::ignoreMigrations` method in the `register` method of your `App\Providers\AppServiceProvider` class. You may export the default migrations by executing the following command: `php artisan vendor:publish --tag=sanctum-migrations` -->
Sanctum의 기본 마이그레이션을 사용하지 않을 경우, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Sanctum::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션을 내보내려면, 다음 명령어를 실행하면 됩니다: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum: -->
일반적으로 필요 없지만, 원한다면 Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수도 있습니다.

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

<!-- Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of one of your application's service providers: -->
그런 다음, Sanctum이 제공하는 `usePersonalAccessTokenModel` 메서드로 커스텀 모델을 사용하도록 Sanctum에 지시할 수 있습니다. 보통 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출합니다.

```
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
> 여러분의 1차 서비스(1st-party) SPA를 API 토큰으로 인증하면 안 됩니다. 대신 Sanctum의 내장 [SPA authentication features](#spa-authentication)을 사용하십시오.

<a name="issuing-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token. -->
Sanctum을 사용하면 API 요청 인증에 사용할 수 있는 API 토큰/개인 액세스 토큰을 발급할 수 있습니다. API 토큰을 사용할 때, 토큰은 `Authorization` 헤더의 `Bearer` 토큰 형식으로 포함되어야 합니다.

<!-- To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait: -->
토큰 발급을 시작하려면, 사용자(User) 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다.

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created: -->
토큰을 발급하려면, `createToken` 메서드를 사용할 수 있습니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시로 암호화되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 평문 토큰 값을 얻을 수 있습니다. 이 값은 토큰 생성 직후 사용자에게 반드시 보여주어야 합니다.

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

<!-- You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait: -->
사용자의 모든 토큰은 `HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 연관관계를 통해 확인할 수 있습니다.

```
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
<!-- ### Token Abilities -->
### Token Abilities

<!-- Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method: -->
Sanctum을 사용하면 토큰에 "권한(Ability)"을 부여할 수 있습니다. 이 권한은 OAuth의 "스코프"와 비슷한 개념입니다. `createToken` 메서드의 두 번째 인수로 문자열 배열 형태의 권한을 전달할 수 있습니다.

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

<!-- When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` method: -->
Sanctum을 통해 인증된 요청을 처리할 때, 토큰이 특정 권한을 가지고 있는지 `tokenCan` 메서드를 통해 확인할 수 있습니다.

```
if ($user->tokenCan('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
<!-- #### Token Ability Middleware -->
#### Token Ability Middleware

<!-- Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, add the following middleware to the `$middlewareAliases` property of your application's `app/Http/Kernel.php` file: -->
Sanctum에는 요청의 토큰이 특정 권한을 보유하고 있는지 확인해 주는 두 가지 미들웨어가 포함되어 있습니다. 우선, 다음 미들웨어를 애플리케이션의 `app/Http/Kernel.php` 파일의 `$middlewareAliases` 프로퍼티에 추가하세요.

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

<!-- The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities: -->
`abilities` 미들웨어는 요청의 토큰이 지정한 모든 권한을 가지고 있는지 검증합니다.

```
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

<!-- The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities: -->
`ability` 미들웨어는 요청의 토큰이 지정한 권한(들) 중 *하나 이상*을 가지고 있으면 통과시킵니다.

```
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
<!-- #### First-Party UI Initiated Requests -->
#### First-Party UI Initiated Requests

<!-- For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication). -->
편의를 위해, 요청이 여러분의 1차 서비스 SPA로부터 오고, 내장 [SPA authentication](#spa-authentication)을 사용 중이라면, `tokenCan` 메서드는 항상 `true`를 반환합니다.

<!-- However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/10.x/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action. -->
하지만, 이것이 해당 사용자가 실제로 해당 작업을 수행할 수 있다는 의미는 아닙니다. 실제 권한 부여 여부는 일반적으로 [authorization policies](/docs/10.x/authorization#creating-policies)에서 판단하게 됩니다. 즉, 토큰이 필요한 권한을 가지고 있는지와 동시에, 사용자가 해당 리소스에 대해 실제로 작업할 수 있는지도 확인해야 합니다.

<!-- For example, if we imagine an application that manages servers, this might mean checking that token is authorized to update servers **and** that the server belongs to the user: -->
예를 들어 서버 관리 애플리케이션이라면, 토큰이 "서버 업데이트" 권한을 가지고 있고, 서버가 실제로 해당 사용자 소유인지 확인해야 합니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

<!-- At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorizations policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers. -->
처음에는 1차 서비스 UI에서 온 요청에 대해 항상 `tokenCan`가 `true`를 반환하는 것이 어색해 보일 수 있습니다. 하지만, 이 방식 덕분에 "항상 API 토큰이 있다고 가정하고 `tokenCan` 메서드를 호출할 수 있다"고 믿을 수 있습니다. 이로 인해, 요청이 여러분의 UI에서 오든, 외부 타사 API 클라이언트에서 오든 관계없이, 인가 정책 내부에서 `tokenCan`과 같은 메서드를 항상 동일하게 호출할 수 있다는 장점이 있습니다.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party. -->
모든 들어오는 요청이 인증되도록 라우트를 보호하려면, 보호가 필요한 라우트를 `routes/web.php` 혹은 `routes/api.php` 파일에서 `sanctum` 인증 가드를 사용하도록 설정하면 됩니다. 이 가드는 요청이 세션 기반 쿠키 인증이든, 혹은 외부에서 오는 유효한 API 토큰이든 모두 처리합니다.

<!-- You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance: -->
왜 `routes/web.php`에서도 `sanctum` 가드로 인증하라고 권장하는지 궁금할 수 있습니다. 그 이유는, Sanctum이 먼저 Laravel 기본 세션 인증 쿠키로 인증을 시도하고, 쿠키가 없으면 요청의 `Authorization` 헤더에 토큰이 있는지 확인하기 때문입니다. 이 방식 덕분에 언제든 현재 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 호출할 수 있습니다.

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
발급된 토큰을 폐기(차단)하려면, `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 연관관계를 사용해 데이터베이스에서 토큰을 직접 삭제하면 됩니다.

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
기본적으로 Sanctum 토큰은 만료되지 않으며, [revoking the token](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 하지만, 애플리케이션의 API 토큰에 만료시간을 설정하고 싶다면, `sanctum` 설정 파일의 `expiration` 옵션을 이용할 수 있습니다. 이 값에는 토큰이 발급된 후 만료될 때까지의 "분" 단위 시간을 설정합니다.

```php
'expiration' => 525600,
```

<!-- If you would like to specify the expiration time of each token independently, you may do so by providing the expiration time as the third argument to the `createToken` method: -->
각 토큰마다 만료시간을 따로 지정하려면, `createToken` 메서드의 세 번째 인자로 만료시간을 개별적으로 지정할 수 있습니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->addWeek()
)->plainTextToken;
```

<!-- If you have configured a token expiration time for your application, you may also wish to [schedule a task](/docs/10.x/scheduling) to prune your application's expired tokens. Thankfully, Sanctum includes a `sanctum:prune-expired` Artisan command that you may use to accomplish this. For example, you may configure a scheduled tasks to delete all expired token database records that have been expired for at least 24 hours: -->
토큰에 만료시간을 설정한 경우, 애플리케이션의 만료된 토큰들을 정기적으로 삭제하는 [schedule a task](/docs/10.x/scheduling)을 추가하는 것이 좋습니다. Sanctum에는 이를 위한 `sanctum:prune-expired` Artisan 명령어가 제공됩니다. 예를 들어, 24시간 동안 만료된 토큰을 매일 한 번 삭제하려면 아래와 같이 스케줄을 구성할 수 있습니다.

```php
$schedule->command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository. -->
Sanctum은 Laravel 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)을 손쉽게 인증할 수 있도록 기능을 제공합니다. 이 SPA는 Laravel 애플리케이션과 같은 저장소에서 관리될 수도 있고, 완전히 별개 저장소일 수도 있습니다.

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
이 기능의 경우, Sanctum은 토큰을 전혀 사용하지 않습니다. 대신 Laravel의 내장 쿠키 기반 세션 인증 서비스를 사용합니다. 이렇게 하면 CSRF 보호, 세션 인증, 그리고 XSS에 의한 인증 정보 유출 방지 등의 장점이 있습니다.

> [!WARNING]
> 인증이 제대로 동작하려면 SPA와 API가 같은 최상위 도메인(Top-level Domain)을 공유해야 합니다. 단, 서로 다른 서브도메인에 위치하는 것은 괜찮습니다. 그리고 요청 시 `Accept: application/json` 헤더와, `Referer` 또는 `Origin` 헤더를 반드시 함께 전송해야 합니다.


<a name="spa-configuration"></a>
<!-- ### Configuration -->
### Configuration

<a name="configuring-your-first-party-domains"></a>
<!-- #### Configuring Your First-Party Domains -->
#### Configuring Your First-Party Domains

<!-- First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API. -->
먼저, SPA가 어떤 도메인에서 API 요청을 할지 지정해야 합니다. `sanctum` 설정 파일의 `stateful` 구성 옵션을 이용해 도메인(들)을 등록할 수 있습니다. 이 설정에 포함된 도메인들은 Laravel 세션 쿠키를 사용해서 API와 "stateful" 인증을 유지할 수 있게 됩니다.

> [!WARNING]
> 만약 포트가 포함된 주소(`127.0.0.1:8000` 등)로 애플리케이션에 접근한다면, 반드시 도메인 값에 포트번호도 함께 포함해야 합니다.

<a name="sanctum-middleware"></a>
<!-- #### Sanctum Middleware -->
#### Sanctum Middleware

<!-- Next, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file. This middleware is responsible for ensuring that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens: -->
다음으로, `app/Http/Kernel.php` 파일의 `api` 미들웨어 그룹에 Sanctum의 미들웨어를 추가하세요. 이 미들웨어는 SPA에서 온 요청이 Laravel의 세션 쿠키를 통해 인증될 수 있도록 하며, 동시에 외부 혹은 모바일 앱에서 온 요청은 여전히 API 토큰으로 인증될 수 있게 해줍니다.

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
<!-- #### CORS and Cookies -->
#### CORS and Cookies

<!-- If you are having trouble authenticating with your application from a SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings. -->
별도의 서브도메인에서 실행되는 SPA에서 인증이 잘 되지 않는다면, CORS(교차 출처 리소스 공유) 또는 세션 쿠키 설정에 문제가 있을 가능성이 높습니다.

<!-- You should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`. -->
CORS 설정에서 반드시 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되는지 확인하세요. 이는 애플리케이션의 `config/cors.php` 설정 파일에서 `supports_credentials` 옵션을 `true`로 설정하면 됩니다.

<!-- In addition, you should enable the `withCredentials` and `withXSRFToken` options on your application's global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client: -->
또한, 애플리케이션의 전역 `axios` 인스턴스에 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 일반적으로 이 설정은 `resources/js/bootstrap.js` 파일에서 수행합니다. 프론트엔드에서 HTTP 요청에 Axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트에 맞게 동일한 설정을 해야 합니다.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

<!-- Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file: -->
마지막으로, 세션 쿠키의 도메인 설정도 반드시 루트 도메인의 하위 모든 서브도메인을 지원하도록 작성해야 합니다. 이를 위해 `config/session.php` 파일에서 도메인 값을 앞에 점(`.`)을 붙여 지정하세요.

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
SPA 인증을 위해서는, SPA의 "로그인" 페이지에서 먼저 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

<!-- During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the value of the `XSRF-TOKEN` cookie that is set by this route. -->
이 요청이 정상적으로 처리되면, Laravel은 현재 CSRF 토큰을 담은 `XSRF-TOKEN` 쿠키를 설정합니다. 이 토큰은 이후의 요청에서 `X-XSRF-TOKEN` 헤더로 같이 전송되어야 하며, Axios나 Angular HttpClient와 같은 일부 HTTP 클라이언트들은 이를 자동으로 처리해줍니다. 만약 사용 중인 자바스크립트 HTTP 라이브러리가 이를 자동으로 처리하지 않는다면, 반드시 직접 `X-XSRF-TOKEN` 헤더에 `XSRF-TOKEN` 쿠키 값을 넣어주어야 합니다.

<a name="logging-in"></a>
<!-- #### Logging In -->
#### Logging In

<!-- Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/10.x/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/10.x/fortify). -->
CSRF 보호가 초기화된 후, 이제 Laravel 애플리케이션의 `/login` 라우트로 `POST` 요청을 보내 인증을 진행하면 됩니다. 이 `/login` 라우트는 [implemented manually](/docs/10.x/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/10.x/fortify) 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

<!-- If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header. -->
로그인 요청이 성공하면 인증된 상태가 되며, 이후의 모든 요청은 Laravel이 발급한 세션 쿠키를 통해 자동으로 인증이 처리됩니다. 그리고 이미 `/sanctum/csrf-cookie` 라우트로 요청을 보냈으므로, 이 후의 요청은 Javascript HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더에 포함해서 CSRF 보호도 계속 유지됩니다.

<!-- Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page. -->
사용자의 세션이 만료(예: 장시간 미활동 등)되면 이후 요청에 대해 401 또는 419 HTTP 오류가 반환될 수 있습니다. 이 경우 사용자를 다시 SPA 로그인 페이지로 리다이렉트해야 합니다.

> [!WARNING]
> 직접 `/login` 엔드포인트를 구현할 수도 있지만, 반드시 [session based authentication services that Laravel provides](/docs/10.x/authentication#authenticating-users)로 사용자를 인증해야 합니다. 보통은 `web` 인증 가드를 사용한다는 뜻입니다.

<a name="protecting-spa-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party: -->
SPA의 모든 요청이 인증 상태를 요구하도록 보호하려면, 애플리케이션의 `routes/api.php` 파일에서 해당 API 라우트에 `sanctum` 인증 가드를 적용해야 합니다. 이 가드는, SPA의 세션 기반 요청이든, 외부의 토큰 기반 요청이든 모두 인증을 처리해줍니다.

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
<!-- ### Authorizing Private Broadcast Channels -->
### Authorizing Private Broadcast Channels

<!-- If your SPA needs to authenticate with [private / presence broadcast channels](/docs/10.x/broadcasting#authorizing-channels), you should place the `Broadcast::routes` method call within your `routes/api.php` file: -->
SPA에서 [private / presence broadcast channels](/docs/10.x/broadcasting#authorizing-channels)에 인증이 필요한 경우, `Broadcast::routes` 메서드를 `routes/api.php` 파일 내에서 아래와 같이 사용하세요.

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

<!-- Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/10.x/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies): -->
이후, Pusher의 인가 요청이 정상 동작하려면 [Laravel Echo](/docs/10.x/broadcasting#client-side-installation) 초기화 시 커스텀 Pusher `authorizer`를 구현해야 합니다. 이렇게 하면 [properly configured for cross-domain requests](#cors-and-cookies) `axios` 인스턴스를 사용하도록 Pusher를 구성할 수 있습니다.

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
Sanctum 토큰을 사용해 모바일 애플리케이션의 API 요청도 인증할 수 있습니다. 모바일 앱 인증 방식은 타사 API 인증과 거의 유사하지만, API 토큰 발급 과정에 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 12". -->
먼저, 사용자의 이메일 또는 사용자명, 비밀번호, 그리고 디바이스 이름을 받아 Sanctum 토큰을 발급해주는 엔드포인트를 만들어야 합니다. 여기서 "디바이스 이름"은 주로 나중에 관리 편의와 정보 제공을 위해 사용되며 아무 값이나 지정해도 됩니다. 보통 "Nuno의 iPhone 12"와 같이 사용자가 인식하기 편한 이름으로 지정합니다.

<!-- Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests: -->
일반적으로 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내어, 사용자 인증에 성공하면 평문 API 토큰을 반환받아 모바일 기기에 저장하고, 이후 추가적인 API 요청 시 이 토큰을 사용하면 됩니다.

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
모바일 애플리케이션이 API 요청을 보낼 때는, 토큰을 반드시 `Authorization` 헤더의 `Bearer` 토큰 형태로 전달해야 합니다.

> [!NOTE]
> 모바일 애플리케이션 토큰 발급 시, [token abilities](#token-abilities)도 자유롭게 추가할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes: -->
앞서 설명한 대로, 모든 들어오는 요청이 인증되도록 라우트를 보호하려면 `sanctum` 인증 가드를 라우트에 적용하면 됩니다.

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
모바일 기기에 발급된 API 토큰을 사용자가 직접 폐기할 수 있도록, 웹 애플리케이션의 "계정 설정" 화면 등에서 발급한 각 토큰을 이름과 함께 나열하고, "폐기" 버튼을 제공할 수 있습니다. 사용자가 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제하면 됩니다. 토큰 목록은 `Laravel\Sanctum\HasApiTokens` 트레이트가 제공하는 `tokens` 연관관계를 통해 얻을 수 있습니다.

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
테스트 코드에서 `Sanctum::actingAs` 메서드를 사용해 인증된 유저를 지정하고, 해당 유저의 토큰에 어떤 권한(Ability)을 부여할지 같이 지정할 수 있습니다.

```
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
토큰에 모든 권한을 부여하고 싶다면, `actingAs` 메서드의 권한 목록에 `*` 을 포함하면 됩니다.

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
