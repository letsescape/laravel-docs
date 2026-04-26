# Laravel Sanctum (Laravel Sanctum)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 능력](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증하기](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [Private 브로드캐스트 채널 인가](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(single page applications), 모바일 애플리케이션, 그리고 단순한 토큰 기반 API를 위한 매우 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 API 토큰을 생성할 수 있습니다. 이 토큰에는 해당 토큰이 수행할 수 있는 작업을 지정하는 능력(abilities) / 범위(scopes)를 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel Sanctum은 서로 다른 두 가지 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 살펴보기 전에 각각을 먼저 알아보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫 번째로, Sanctum은 OAuth의 복잡함 없이 사용자에게 API 토큰을 발급할 수 있게 해주는 단순한 패키지입니다. 이 기능은 "personal access tokens"를 발급하는 GitHub와 다른 애플리케이션에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "account settings"에 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있는 화면이 있다고 생각해 보겠습니다. Sanctum을 사용하면 이러한 토큰을 생성하고 관리할 수 있습니다. 이 토큰은 일반적으로 매우 긴 만료 시간(수년)을 가지지만, 사용자가 언제든지 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하고, 유효한 API 토큰이 포함되어야 하는 `Authorization` 헤더를 통해 들어오는 HTTP 요청을 인증함으로써 이 기능을 제공합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

두 번째로, Sanctum은 Laravel 기반 API와 통신해야 하는 single page applications(SPAs)을 인증하는 간단한 방법을 제공하기 위해 존재합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, Next.js나 Nuxt로 만든 SPA처럼 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능에서 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum은 Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum은 이를 위해 Laravel의 `web` 인증 가드를 활용합니다. 이 방식은 CSRF 보호와 세션 인증의 장점을 제공하며, XSS를 통해 인증 자격 증명이 유출되는 것도 방지합니다.

Sanctum은 들어오는 요청이 여러분의 SPA 프론트엔드에서 시작된 경우에만 쿠키를 사용한 인증을 시도합니다. Sanctum이 들어오는 HTTP 요청을 검사할 때 먼저 인증 쿠키를 확인하고, 쿠키가 없으면 `Authorization` 헤더에서 유효한 API 토큰을 확인합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용하는 것은 전혀 문제가 없습니다. Sanctum을 사용한다고 해서 Sanctum이 제공하는 두 기능을 모두 사용해야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` Artisan 명령어를 통해 Laravel Sanctum을 설치할 수 있습니다.

```shell
php artisan install:api
```

다음으로, SPA 인증에 Sanctum을 사용할 계획이라면 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하십시오.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의

일반적으로 필요하지는 않지만, Sanctum 내부에서 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다.

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그런 다음 Sanctum이 제공하는 `usePersonalAccessTokenModel` 메서드를 통해 Sanctum이 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일에 있는 `boot` 메서드에서 호출해야 합니다.

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
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 여러분이 직접 소유한 자사 SPA를 인증하기 위해 API 토큰을 사용해서는 안 됩니다. 대신 Sanctum에 내장된 [SPA 인증 기능](#spa-authentication)을 사용하십시오.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 애플리케이션에 대한 API 요청을 인증하는 데 사용할 수 있는 API 토큰 / personal access token을 발급할 수 있습니다. API 토큰을 사용하여 요청할 때는 토큰을 `Bearer` 토큰으로 `Authorization` 헤더에 포함해야 합니다.

사용자에게 토큰 발급을 시작하려면 User 모델에서 `Laravel\Sanctum\HasApiTokens` trait을 사용해야 합니다.

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용할 수 있습니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시로 해싱되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 사용하여 토큰의 평문 값을 확인할 수 있습니다. 토큰이 생성된 직후 이 값을 사용자에게 표시해야 합니다.

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` trait이 제공하는 `tokens` Eloquent 연관관계를 사용하여 사용자의 모든 토큰에 접근할 수 있습니다.

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 능력

Sanctum을 사용하면 토큰에 "능력(abilities)"을 할당할 수 있습니다. 능력은 OAuth의 "scopes"와 비슷한 목적을 가집니다. 문자열 능력 배열을 `createToken` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 들어오는 요청을 처리할 때는 `tokenCan` 또는 `tokenCant` 메서드를 사용하여 토큰이 특정 능력을 가지고 있는지 확인할 수 있습니다.

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 능력 Middleware

Sanctum에는 들어오는 요청이 특정 능력을 부여받은 토큰으로 인증되었는지 검증하는 데 사용할 수 있는 두 개의 Middleware도 포함되어 있습니다. 시작하려면 애플리케이션의 `bootstrap/app.php` 파일에 다음 Middleware 별칭을 정의하십시오.

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

`abilities` Middleware는 들어오는 요청의 토큰이 나열된 모든 능력을 가지고 있는지 검증하기 위해 라우트에 할당할 수 있습니다.

```php
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` Middleware는 들어오는 요청의 토큰이 나열된 능력 중 *최소 하나*를 가지고 있는지 검증하기 위해 라우트에 할당할 수 있습니다.

```php
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 자사 UI에서 시작된 요청

편의를 위해, 들어오는 인증된 요청이 자사 SPA에서 온 것이고 Sanctum에 내장된 [SPA 인증](#spa-authentication)을 사용하고 있다면 `tokenCan` 메서드는 항상 `true`를 반환합니다.

하지만 이것이 반드시 애플리케이션이 사용자에게 해당 작업 수행을 허용해야 한다는 뜻은 아닙니다. 일반적으로 애플리케이션의 [인가 정책](/docs/12.x/authorization#creating-policies)이 토큰에 해당 능력을 수행할 권한이 부여되었는지 판단하고, 사용자 인스턴스 자체가 그 작업을 수행할 수 있는지도 함께 확인합니다.

예를 들어 서버를 관리하는 애플리케이션을 생각해 보면, 이는 토큰이 서버 업데이트를 수행할 권한이 있는지 **그리고** 해당 서버가 사용자에게 속하는지 확인하는 것을 의미할 수 있습니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 자사 UI에서 시작된 요청에 대해 `tokenCan` 메서드를 호출할 수 있게 하고 항상 `true`를 반환하게 하는 것이 이상해 보일 수 있습니다. 하지만 API 토큰이 항상 존재하며 `tokenCan` 메서드를 통해 검사할 수 있다고 가정할 수 있다는 점은 편리합니다. 이 접근 방식을 사용하면 요청이 애플리케이션의 UI에서 트리거되었는지, 아니면 API의 타사 소비자 중 하나가 시작했는지 걱정하지 않고 애플리케이션의 인가 정책 안에서 항상 `tokenCan` 메서드를 호출할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 들어오는 요청이 인증되어야 하도록 라우트를 보호하려면 `routes/web.php`와 `routes/api.php` 라우트 파일 안에서 보호할 라우트에 `sanctum` 인증 가드를 연결해야 합니다. 이 가드는 들어오는 요청이 상태를 가지는 쿠키 인증 요청으로 인증되었거나, 요청이 타사에서 온 경우 유효한 API 토큰 헤더를 포함하는지 보장합니다.

애플리케이션의 `routes/web.php` 파일 안에 있는 라우트를 `sanctum` 가드로 인증하라고 제안하는 이유가 궁금할 수 있습니다. Sanctum은 먼저 Laravel의 일반적인 세션 인증 쿠키를 사용하여 들어오는 요청 인증을 시도한다는 점을 기억하십시오. 해당 쿠키가 없으면 Sanctum은 요청의 `Authorization` 헤더에 있는 토큰을 사용하여 요청 인증을 시도합니다. 또한 Sanctum으로 모든 요청을 인증하면 현재 인증된 사용자 인스턴스에서 항상 `tokenCan` 메서드를 호출할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` trait이 제공하는 `tokens` 연관관계를 사용하여 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기"할 수 있습니다.

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰을 폐기](#revoking-tokens)해야만 무효화할 수 있습니다. 하지만 애플리케이션의 API 토큰에 만료 시간을 설정하고 싶다면, 애플리케이션의 `sanctum` 설정 파일에 정의된 `expiration` 설정 옵션을 통해 설정할 수 있습니다. 이 설정 옵션은 발급된 토큰이 만료된 것으로 간주되기까지의 시간을 분 단위로 정의합니다.

```php
'expiration' => 525600,
```

각 토큰의 만료 시간을 개별적으로 지정하고 싶다면, 만료 시간을 `createToken` 메서드의 세 번째 인수로 제공하면 됩니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

애플리케이션에 토큰 만료 시간을 설정했다면, 애플리케이션의 만료된 토큰을 정리하기 위해 [작업을 스케줄링](/docs/12.x/scheduling)하고 싶을 수도 있습니다. 다행히 Sanctum에는 이를 수행하는 데 사용할 수 있는 `sanctum:prune-expired` Artisan 명령어가 포함되어 있습니다. 예를 들어 최소 24시간 전에 만료된 모든 만료 토큰 데이터베이스 레코드를 삭제하도록 스케줄링된 작업을 설정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel 기반 API와 통신해야 하는 single page applications(SPAs)을 인증하는 간단한 방법을 제공하기 위해서도 존재합니다. 이러한 SPA는 Laravel 애플리케이션과 같은 저장소에 있을 수도 있고, 완전히 별도의 저장소에 있을 수도 있습니다.

이 기능에서 Sanctum은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum은 Laravel에 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 이 인증 방식은 CSRF 보호와 세션 인증의 장점을 제공하며, XSS를 통해 인증 자격 증명이 유출되는 것도 방지합니다.

> [!WARNING]
> 인증을 수행하려면 SPA와 API가 동일한 최상위 도메인을 공유해야 합니다. 다만 서로 다른 서브도메인에 배치될 수는 있습니다. 또한 요청에 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더 중 하나를 보내도록 해야 합니다.

<a name="spa-configuration"></a>
### 설정

<a name="configuring-your-first-party-domains"></a>
#### 자사 도메인 설정

먼저 SPA가 어떤 도메인에서 요청을 보낼지 설정해야 합니다. 이 도메인들은 `sanctum` 설정 파일의 `stateful` 설정 옵션을 사용하여 설정할 수 있습니다. 이 설정은 API에 요청할 때 Laravel 세션 쿠키를 사용하여 "상태 저장 방식(stateful)" 인증을 유지할 도메인을 결정합니다.

자사 상태 저장 도메인을 설정하는 데 도움을 주기 위해 Sanctum은 설정에 포함할 수 있는 두 가지 헬퍼 함수를 제공합니다. 먼저 `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경 변수에서 현재 애플리케이션 URL을 반환합니다. 그리고 `Sanctum::currentRequestHost()`는 상태 저장 도메인 목록에 플레이스홀더를 삽입하며, 런타임에는 이 플레이스홀더가 현재 요청의 호스트로 대체되어 같은 도메인을 사용하는 모든 요청이 상태 저장 방식으로 간주됩니다.

> [!WARNING]
> 포트가 포함된 URL(`127.0.0.1:8000`)로 애플리케이션에 접근하는 경우, 도메인에 포트 번호도 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum Middleware

다음으로, SPA에서 들어오는 요청은 Laravel의 세션 쿠키를 사용하여 인증할 수 있도록 하면서도, 타사나 모바일 애플리케이션에서 오는 요청은 API 토큰을 사용하여 인증할 수 있도록 Laravel에 알려야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `statefulApi` Middleware 메서드를 호출하면 쉽게 처리할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키

별도의 서브도메인에서 실행되는 SPA에서 애플리케이션 인증에 문제가 있다면, CORS(Cross-Origin Resource Sharing) 또는 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

`config/cors.php` 설정 파일은 기본적으로 게시되지 않습니다. Laravel의 CORS 옵션을 사용자 정의해야 한다면 `config:publish` Artisan 명령어를 사용하여 전체 `cors` 설정 파일을 게시해야 합니다.

```shell
php artisan config:publish cors
```

다음으로, 애플리케이션의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `True` 값으로 반환하는지 확인해야 합니다. 이는 애플리케이션의 `config/cors.php` 설정 파일 안에서 `supports_credentials` 옵션을 `true`로 설정하여 처리할 수 있습니다.

또한 애플리케이션의 전역 `axios` 인스턴스에서 `withCredentials`와 `withXSRFToken` 옵션을 활성화해야 합니다. 일반적으로 이는 `resources/js/bootstrap.js` 파일에서 수행해야 합니다. 프론트엔드에서 HTTP 요청을 보내는 데 Axios를 사용하지 않는다면, 사용하는 HTTP 클라이언트에서 이에 해당하는 설정을 수행해야 합니다.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 애플리케이션의 세션 쿠키 도메인 설정이 루트 도메인의 모든 서브도메인을 지원하는지 확인해야 합니다. 애플리케이션의 `config/session.php` 설정 파일에서 도메인 앞에 `.`을 붙이면 이를 처리할 수 있습니다.

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증하기

<a name="csrf-protection"></a>
#### CSRF 보호

SPA를 인증하려면, SPA의 "login" 페이지가 먼저 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

이 요청 중에 Laravel은 현재 CSRF 토큰을 포함하는 `XSRF-TOKEN` 쿠키를 설정합니다. 이후 요청에서는 이 토큰을 URL 디코딩한 뒤 `X-XSRF-TOKEN` 헤더에 전달해야 합니다. Axios나 Angular HttpClient와 같은 일부 HTTP 클라이언트 라이브러리는 이 작업을 자동으로 처리합니다. 사용 중인 JavaScript HTTP 라이브러리가 값을 자동으로 설정하지 않는다면, 이 라우트가 설정한 `XSRF-TOKEN` 쿠키의 URL 디코딩된 값과 일치하도록 `X-XSRF-TOKEN` 헤더를 수동으로 설정해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화되면 Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내야 합니다. 이 `/login` 라우트는 [직접 구현](/docs/12.x/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/12.x/fortify) 같은 헤드리스 인증 패키지를 사용하여 구현할 수도 있습니다.

로그인 요청이 성공하면 인증된 상태가 되며, 이후 애플리케이션 라우트에 보내는 요청은 Laravel 애플리케이션이 클라이언트에 발급한 세션 쿠키를 통해 자동으로 인증됩니다. 또한 애플리케이션이 이미 `/sanctum/csrf-cookie` 라우트에 요청을 보냈으므로, JavaScript HTTP 클라이언트가 `XSRF-TOKEN` 쿠키 값을 `X-XSRF-TOKEN` 헤더로 보내는 한 이후 요청은 자동으로 CSRF 보호를 받게 됩니다.

물론 활동 부족으로 인해 사용자의 세션이 만료되면 Laravel 애플리케이션에 보내는 이후 요청은 401 또는 419 HTTP 오류 응답을 받을 수 있습니다. 이 경우 사용자를 SPA의 로그인 페이지로 리디렉션해야 합니다.

> [!WARNING]
> 여러분만의 `/login` 엔드포인트를 자유롭게 작성할 수 있습니다. 하지만 이 엔드포인트가 Laravel이 제공하는 표준 [세션 기반 인증 서비스](/docs/12.x/authentication#authenticating-users)를 사용하여 사용자를 인증하는지 확인해야 합니다. 일반적으로 이는 `web` 인증 가드를 사용하는 것을 의미합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 들어오는 요청이 인증되어야 하도록 라우트를 보호하려면 `routes/api.php` 파일 안의 API 라우트에 `sanctum` 인증 가드를 연결해야 합니다. 이 가드는 들어오는 요청이 SPA에서 온 상태 저장 인증 요청으로 인증되었거나, 요청이 타사에서 온 경우 유효한 API 토큰 헤더를 포함하는지 보장합니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### Private 브로드캐스트 채널 인가

SPA가 [private / presence 브로드캐스트 채널](/docs/12.x/broadcasting#authorizing-channels)로 인증해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일에 있는 `withRouting` 메서드에서 `channels` 항목을 제거해야 합니다. 대신 애플리케이션의 브로드캐스팅 라우트에 올바른 Middleware를 지정할 수 있도록 `withBroadcasting` 메서드를 호출해야 합니다.

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

다음으로, Pusher의 인가 요청이 성공하려면 [Laravel Echo](/docs/12.x/broadcasting#client-side-installation)를 초기화할 때 사용자 정의 Pusher `authorizer`를 제공해야 합니다. 이렇게 하면 애플리케이션에서 [크로스 도메인 요청에 맞게 올바르게 설정된](#cors-and-cookies) `axios` 인스턴스를 사용하도록 Pusher를 설정할 수 있습니다.

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
## 모바일 애플리케이션 인증 (Mobile Application Authentication)

Sanctum 토큰을 사용하여 모바일 애플리케이션이 API로 보내는 요청을 인증할 수도 있습니다. 모바일 애플리케이션 요청을 인증하는 과정은 서드파티 API 요청을 인증하는 과정과 비슷하지만, API 토큰을 발급하는 방식에는 약간의 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저 사용자의 이메일 / 사용자 이름, 비밀번호, 기기 이름을 받아 해당 자격 증명을 새 Sanctum 토큰으로 교환하는 라우트를 생성합니다. 이 엔드포인트에 전달되는 "기기 이름"은 정보 제공용이며 원하는 어떤 값이든 사용할 수 있습니다. 일반적으로 기기 이름 값은 사용자가 알아볼 수 있는 이름이어야 하며, 예를 들어 "Nuno's iPhone 17"과 같은 이름을 사용할 수 있습니다.

일반적으로 모바일 애플리케이션의 "로그인" 화면에서 토큰 엔드포인트로 요청을 보냅니다. 엔드포인트는 평문 API 토큰을 반환하며, 이 토큰은 모바일 기기에 저장한 뒤 추가 API 요청을 보낼 때 사용할 수 있습니다.

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

모바일 애플리케이션이 토큰을 사용하여 애플리케이션에 API 요청을 보낼 때는 `Authorization` 헤더에 `Bearer` 토큰으로 전달해야 합니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰을 발급할 때 [토큰 능력](#token-abilities)을 지정할 수도 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞서 설명한 것처럼, 라우트에 `sanctum` 인증 guard를 연결하여 들어오는 모든 요청이 반드시 인증되도록 라우트를 보호할 수 있습니다.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

사용자가 모바일 기기에 발급된 API 토큰을 폐기할 수 있도록 하려면, 웹 애플리케이션 UI의 "계정 설정" 영역에서 토큰 이름과 함께 "폐기" 버튼을 표시할 수 있습니다. 사용자가 "폐기" 버튼을 클릭하면 데이터베이스에서 해당 토큰을 삭제할 수 있습니다. 사용자의 API 토큰은 `Laravel\Sanctum\HasApiTokens` trait이 제공하는 `tokens` 연관관계를 통해 접근할 수 있다는 점을 기억하세요.

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 중에는 `Sanctum::actingAs` 메서드를 사용하여 사용자를 인증하고, 해당 사용자의 토큰에 어떤 능력을 부여할지 지정할 수 있습니다.

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

토큰에 모든 능력을 부여하려면 `actingAs` 메서드에 전달하는 능력 목록에 `*`를 포함해야 합니다.

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
