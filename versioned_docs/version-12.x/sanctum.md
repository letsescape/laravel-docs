# Laravel Sanctum (Laravel Sanctum)

- [소개](#introduction)
    - [작동 방식](#how-it-works)
- [설치](#installation)
- [설정](#configuration)
    - [기본 모델 오버라이딩](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기(Revoking)](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [설정](#spa-configuration)
    - [인증 절차](#spa-authenticating)
    - [라우트 보호](#protecting-spa-routes)
    - [프라이빗 브로드캐스트 채널 인가](#authorizing-private-broadcast-channels)
- [모바일 애플리케이션 인증](#mobile-application-authentication)
    - [API 토큰 발급](#issuing-mobile-api-tokens)
    - [라우트 보호](#protecting-mobile-api-routes)
    - [토큰 폐기](#revoking-mobile-api-tokens)
- [테스트](#testing)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(Single Page Application), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 가벼운 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 계정당 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰에는 각 토큰이 수행할 수 있는 동작을 명시하는 권한(abilities/범위(scope))을 부여할 수 있습니다.

<a name="how-it-works"></a>
### 작동 방식

Laravel Sanctum은 두 가지 별개의 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 이해하기 전에 각각에 대해 알아보겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

먼저, Sanctum은 복잡한 OAuth 없이도 사용자에게 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub 등에서 개인 인증 토큰(personal access tokens)을 발급하는 방식에서 영감을 받아 구현되었습니다. 예를 들어, 여러분의 애플리케이션의 "계정 설정" 화면에서 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있다고 가정할 수 있습니다. Sanctum을 사용하면 이러한 토큰을 쉽게 생성 및 관리할 수 있습니다. 이 토큰은 일반적으로 만료 기간이 매우 깁니다(수년)만, 사용자가 언제든지 직접 폐기(revoke)할 수 있습니다.

Laravel Sanctum은 데이터베이스의 한 테이블에 사용자 API 토큰을 저장하고, 들어오는 HTTP 요청의 `Authorization` 헤더에 포함된 유효한 API 토큰을 통해 인증을 수행합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

두 번째로, Sanctum은 Laravel로 구동되는 API와 통신해야 하는 SPA(single page application)를 간편하게 인증할 수 있도록 설계되었습니다. 이러한 SPA는 Laravel 애플리케이션과 동일한 저장소(repository)에 존재할 수도 있고, Next.js나 Nuxt로 작성된 완전히 분리된 저장소에 존재할 수도 있습니다.

이 기능을 위해 Sanctum은 토큰을 전혀 사용하지 않습니다. 대신, Laravel에서 기본적으로 제공하는 쿠키 기반 세션 인증 서비스를 활용합니다. 일반적으로 Sanctum은 Laravel의 `web` 인증 가드(guard)를 사용하여 이 작업을 처리합니다. 이 방식은 CSRF 보호, 세션 인증, 인증 정보가 XSS를 통해 노출되는 위험 방지 등 다양한 이점을 제공합니다.

Sanctum은 들어오는 요청이 여러분의 SPA 프론트엔드에서 유래한 경우에만 쿠키를 이용한 인증을 시도합니다. 따라서, Sanctum은 요청을 검사할 때 인증 쿠키가 있는지 먼저 확인하고, 쿠키가 없으면 `Authorization` 헤더의 유효한 API 토큰을 검증합니다.

> [!NOTE]
> Sanctum을 반드시 API 토큰 인증과 SPA 인증 모두에 사용해야 하는 것은 아닙니다. 둘 중 하나의 기능만 사용해도 전혀 문제가 없습니다.

<a name="installation"></a>
## 설치 (Installation)

Sanctum은 `install:api` Artisan 명령어를 통해 설치할 수 있습니다:

```shell
php artisan install:api
```

이후 SPA 인증 기능을 활용하고자 한다면, 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하시기 바랍니다.

<a name="configuration"></a>
## 설정 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 오버라이딩 (Overriding Default Models)

일반적으로 필요하지 않지만, 내부적으로 Sanctum에서 사용하는 `PersonalAccessToken` 모델을 확장할 수도 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

이후, `Sanctum`에서 제공하는 `usePersonalAccessTokenModel` 메서드를 사용하여 커스텀 모델을 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출합니다:

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
> 여러분의 1st-party SPA를 인증하는 방법으로는 API 토큰을 사용하지 마십시오. 대신 Sanctum의 [SPA 인증 기능](#spa-authentication)을 이용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

Sanctum을 이용해 API 토큰(개인 접근 토큰)을 발급하여 API 요청을 인증할 수 있습니다. API 토큰을 사용하여 요청할 때에는 `Authorization` 헤더에 `Bearer` 토큰 형식으로 해당 토큰을 포함해야 합니다.

토큰을 발급하기 전에, User 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 추가해야 합니다:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용합니다. `createToken` 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시로 변환되지만, 토큰 생성 직후 `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 평문 값을 확인할 수 있습니다. 생성 즉시 사용자에게 이 값을 제공해야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레이트에서 제공하는 `tokens` Eloquent 연관관계를 사용하여 사용자가 소유한 모든 토큰에 접근할 수 있습니다:

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한(Abilities) (Token Abilities)

Sanctum을 사용하면 발급된 토큰에 "권한(abilities)"을 부여할 수 있습니다. 권한(abilities)은 OAuth의 "스코프(scopes)"와 유사한 역할을 합니다. `createToken` 메서드의 두 번째 인수로 문자열 배열로 권한을 지정할 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

토큰으로 인증된 요청을 처리할 때, `tokenCan` 또는 `tokenCant` 메서드를 이용해 해당 토큰이 특정 권한을 지녔는지 확인할 수 있습니다:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어 (Token Ability Middleware)

Sanctum에는 토큰에 특정 권한이 부여되어 있는지 검증할 수 있는 두 가지 미들웨어도 포함되어 있습니다. 우선, 아래와 같이 애플리케이션의 `bootstrap/app.php` 파일에 미들웨어 별칭을 정의하세요:

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

`abilities` 미들웨어를 라우트에 할당하면 들어오는 요청의 토큰이 지정된 모든 권한을 가지고 있는지 검증할 수 있습니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한을 모두 가지고 있음...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어를 라우트에 할당하면 토큰이 지정된 권한 중 *하나라도* 가지고 있는지 확인합니다:

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 또는 "place-orders" 권한 중 하나만 가지고 있어도 허용...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1st-party UI에서 시작된 요청

편의상, Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용할 경우 1st-party SPA에서 인증된 요청이 들어올 때는 `tokenCan` 메서드가 항상 `true`를 반환합니다.

하지만, 이것이 반드시 사용자가 해당 동작을 수행할 수 있음을 의미하지는 않습니다. 일반적으로 애플리케이션의 [인가 정책](/docs/12.x/authorization#creating-policies)이 토큰에 권한이 있는지와 사용자가 실제로 해당 동작을 수행할 수 있는지를 함께 판단하게 됩니다.

예를 들어, 서버 관리 애플리케이션을 가정할 때, 토큰이 서버 업데이트 권한을 가지고 있고, 해당 서버가 사용자 소유인지도 함께 체크할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 1st-party UI에서 시작된 요청에 대해 `tokenCan`이 항상 `true`를 반환한다는 점이 다소 이상하게 느껴질 수 있습니다. 그러나 이렇게 하면 항상 API 토큰이 존재한다고 가정하고 언제든지 `tokenCan`을 통해 검사할 수 있기 때문에, UI에서 요청했든, 외부에서 API 요청이 들어왔든 관계없이 인가 정책 내에서 보다 일관적으로 사용할 수 있습니다.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

모든 들어오는 요청이 인증되어야 하는 라우트를 보호하려면, 해당 라우트에 `sanctum` 인증 가드를 적용하세요(`routes/web.php`, `routes/api.php` 등). 이 가드는 쿠키 인증(상태 세션) 요청이나, 외부 애플리케이션의 유효한 API 토큰 요청 모두를 인증합니다.

애플리케이션의 `routes/web.php`에서 `sanctum` 가드를 이용한 인증을 권장하는 이유는, Sanctum이 먼저 일반적인 세션 인증 쿠키를 확인하고, 없으면 `Authorization` 헤더의 토큰을 검사하기 때문입니다. 또한 모든 요청을 Sanctum으로 인증하면, 현재 인증된 사용자 인스턴스에 대해 항상 `tokenCan` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기(Revoking Tokens)

토큰을 폐기(revoke)하려면, `Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 연관관계를 통해 데이터베이스에서 해당 토큰을 삭제하면 됩니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 현재 요청에 사용된 토큰 폐기
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료 (Token Expiration)

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 그러나 애플리케이션의 API 토큰에 만료 시간을 설정하고 싶다면, 설정 파일의 `sanctum`에서 `expiration` 옵션을 통해 설정할 수 있습니다. 이 값(분 단위) 동안 토큰이 유효합니다:

```php
'expiration' => 525600,
```

각 토큰의 만료 시간을 개별적으로 지정하고 싶다면, `createToken`의 세 번째 인수로 만료 시각을 전달하면 됩니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

토큰 만료 시간을 설정했다면, 만료된 토큰을 데이터베이스에서 정리(prune)하는 스케줄러 작업도 함께 구성하는 것이 좋습니다. Sanctum은 만료된 토큰을 삭제할 수 있는 `sanctum:prune-expired` Artisan 명령어를 제공합니다. 예를 들어, 아래와 같이 24시간 이상 지난 만료 토큰을 매일 정기적으로 삭제하도록 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 Laravel로 구동되는 API와 통신해야 하는 SPA(single page application)를 간단하게 인증하는 방법도 제공합니다. 이러한 SPA는 Laravel 애플리케이션과 동일한 저장소 혹은 별도의 저장소에 존재할 수 있습니다.

이 기능을 사용하는 경우, Sanctum은 어떠한 토큰도 사용하지 않고 Laravel의 기본 쿠키 기반 세션 인증 서비스를 활용합니다. 이 방식은 CSRF 보호, 세션 인증, 인증 정보의 XSS 유출 방지 등 다양한 장점을 가집니다.

> [!WARNING]
> SPA와 API는 반드시 같은 최상위 도메인을 공유해야 합니다. 다른 서브도메인이라도 괜찮습니다. 또한, 요청시 반드시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 함께 전송해야 합니다.

<a name="spa-configuration"></a>
### 설정 (Configuration)

<a name="configuring-your-first-party-domains"></a>
#### 1st-party 도메인 구성

먼저, SPA가 요청을 보낼 도메인을 지정해야 합니다. `sanctum` 설정 파일의 `stateful` 옵션을 통해 해당 도메인을 설정할 수 있습니다. 이 설정을 통해 Laravel 세션 쿠키를 사용하여 “상태 유지” 인증이 적용되는 도메인을 지정할 수 있습니다.

stateful 도메인 세팅을 보조하기 위해 Sanctum은 두 가지 헬퍼 함수를 제공합니다. `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경변수의 현재 애플리케이션 URL을 반환하며, `Sanctum::currentRequestHost()`는 실행 시점의 요청 호스트로 대체될 플레이스홀더를 stateful 도메인 리스트에 추가합니다.

> [!WARNING]
> 포트 번호(`127.0.0.1:8000` 등)를 포함한 URL로 접근하는 경우, domain 설정에도 포트 번호가 반드시 포함되어야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, SPA에서의 요청이 Laravel 세션 쿠키로 인증되도록 하면서, 외부 애플리케이션이나 모바일에서도 API 토큰을 사용할 수 있도록 해야 합니다. 애플리케이션의 `bootstrap/app.php` 파일에 `statefulApi` 미들웨어 메서드를 호출하여 간단히 구성할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS 및 쿠키 설정

서로 다른 서브도메인에 위치한 SPA에서 인증이 잘 동작하지 않는다면, CORS(교차출처 리소스 공유) 또는 세션 쿠키 설정이 잘못되었을 가능성이 높습니다.

`config/cors.php` 설정 파일은 기본적으로 퍼블리시되지 않습니다. CORS 옵션을 직접 수정하려면, 아래 Artisan 명령어로 설정 파일을 퍼블리시하십시오:

```shell
php artisan config:publish cors
```

이후, CORS 설정에서 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되는지 확인해야 합니다. 이를 위해서는 `config/cors.php` 파일의 `supports_credentials` 옵션을 `true`로 설정하십시오.

그리고 글로벌 `axios` 인스턴스에 `withCredentials`와 `withXSRFToken` 옵션을 켜 주어야 합니다. 보통 `resources/js/bootstrap.js` 파일에서 설정합니다. 만약 Axios를 사용하지 않는다면 사용 중인 HTTP 클라이언트에 맞게 동일하게 설정해야 합니다:

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 세션 쿠키 도메인 설정이 루트 도메인 하위의 모든 서브도메인을 지원하도록 `.domain.com`과 같이 도메인 앞에 점을 붙여 지정해야 합니다(`config/session.php`):

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 절차 (Authenticating)

<a name="csrf-protection"></a>
#### CSRF 보호

SPA에서 인증을 시작할 때, 우선 “로그인” 페이지에서 `/sanctum/csrf-cookie` 엔드포인트로 요청을 보내 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

이 요청 중에 Laravel은 현재의 CSRF 토큰이 담긴 `XSRF-TOKEN` 쿠키를 설정합니다. 이후, 이 토큰을 URL 디코딩하여 모든 후속 요청의 `X-XSRF-TOKEN` 헤더에 전달해야 하며, Axios나 Angular HttpClient 같은 일부 라이브러리는 이를 자동으로 처리합니다. 직접 구현 중이라면, `XSRF-TOKEN` 쿠키의 URL 디코드 값을 `X-XSRF-TOKEN` 헤더에 직접 추가해야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화된 후에는 Laravel 애플리케이션의 `/login` 라우트에 `POST` 요청을 보내 로그인할 수 있습니다. 이 `/login` 라우트는 [직접 구현](/docs/12.x/authentication#authenticating-users)하거나 [Laravel Fortify](/docs/12.x/fortify)와 같은 무상태 인증 패키지로 처리해도 됩니다.

로그인 요청이 성공하면, 이후의 모든 요청은 세션 쿠키를 통해 자동으로 인증됩니다. 또한, `/sanctum/csrf-cookie` 요청 덕분에 잘 구성된 HTTP 클라이언트가 `XSRF-TOKEN` 쿠키를 읽어 `X-XSRF-TOKEN` 헤더로 전송하기 때문에 CSRF 보호도 자동으로 이루어집니다.

물론, 사용자의 세션이 만료(비활성 상태 등)된 경우 이후 요청은 401 또는 419 HTTP 오류를 반환할 수 있습니다. 이 때는 SPA의 로그인 페이지로 사용자를 리디렉션해야 합니다.

> [!WARNING]
> `/login` 엔드포인트를 직접 구현할 수도 있지만, 반드시 Laravel의 표준 [세션 기반 인증 서비스](/docs/12.x/authentication#authenticating-users)를 사용해야 합니다. 이는 보통 `web` 인증 가드를 뜻합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호 (Protecting Routes)

SPA에서 들어오는 모든 요청이 인증되도록 하려면 `routes/api.php`의 API 라우트에 `sanctum` 인증 가드를 적용해야 합니다. 이 가드는 SPA로부터 들어오는 상태 유지(session) 요청, 그리고 다른 외부 요청(토큰 활용) 모두를 인증합니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 인가

SPA에서 [프라이빗/프레즌스 브로드캐스트 채널](/docs/12.x/broadcasting#authorizing-channels)을 인증하고자 한다면, 애플리케이션의 `bootstrap/app.php`의 `withRouting` 메서드에서 `channels` 엔트리를 제거해야 합니다. 대신, `withBroadcasting` 메서드를 호출하여 브로드캐스트 라우트에 적절한 미들웨어를 직접 지정하세요:

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

그 다음, Pusher의 인증 요청을 성공시키기 위해 [Laravel Echo](/docs/12.x/broadcasting#client-side-installation) 초기화 시 커스텀 Pusher `authorizer`를 지정해야 합니다. 즉, [교차 도메인 요청에 맞게 설정된 axios 인스턴스](#cors-and-cookies)를 활용하도록 안내할 수 있습니다:

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

Sanctum 토큰은 모바일 애플리케이션의 API 요청 인증에도 사용할 수 있습니다. 모바일 애플리케이션에서의 인증 방식은 외부(서드파티) API 인증과 거의 동일하지만, API 토큰 발급 과정에 작은 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급 (Issuing API Tokens)

우선, 사용자의 이메일/사용자명, 비밀번호, 그리고 디바이스명(device name)을 받아 새로운 Sanctum 토큰과 교환해 주는 라우트를 만들어야 합니다. 여기서 device name은 단순한 정보 제공용이며, 사용자가 인식하기 쉬운 이름(예: 'Nuno의 iPhone 12')을 넣을 수 있습니다.

대개는 모바일 앱의 "로그인" 화면에서 해당 엔드포인트로 요청하게 됩니다. 엔드포인트는 평문 API 토큰을 반환하며, 이 토큰을 모바일 기기에 저장해두었다가 추가적인 API 요청에 사용하게 됩니다:

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

모바일 애플리케이션이 API에 접근할 때는 `Authorization` 헤더에 `Bearer` 토큰 형식으로 인증 토큰을 첨부해야 합니다.

> [!NOTE]
> 모바일 애플리케이션을 위한 토큰을 발급할 때도 [토큰 권한(abilities)](#token-abilities)을 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호 (Protecting Routes)

앞서 설명한 것처럼, 모든 들어오는 요청을 인증하려면 대상 라우트에 `sanctum` 인증 가드를 적용하십시오:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기 (Revoking Tokens)

모바일 기기에 발급한 API 토큰을 사용자가 직접 폐기할 수 있도록 하려면, 웹 애플리케이션의 "계정 설정" 화면 등에서 토큰을 이름과 함께 나열하고, "폐기" 버튼을 제공하면 됩니다. 사용자가 버튼을 클릭하면 해당 토큰을 데이터베이스에서 삭제할 수 있습니다. `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 연관관계를 통해 사용자 토큰에 접근할 수 있습니다:

```php
// 모든 토큰 폐기
$user->tokens()->delete();

// 특정 토큰 폐기
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 환경에서는 `Sanctum::actingAs` 메서드를 통해 사용자를 인증할 수 있으며, 토큰에 부여할 권한(ability)도 함께 지정할 수 있습니다:

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

토큰에 모든 권한을 부여하고자 할 경우, `actingAs` 메서드에 `*`를 ability 목록에 추가하세요:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
