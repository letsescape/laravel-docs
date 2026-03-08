# 라라벨 Sanctum (Laravel Sanctum)

- [소개](#introduction)
    - [동작 방식](#how-it-works)
- [설치](#installation)
- [구성](#configuration)
    - [기본 모델 재정의](#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
    - [API 토큰 발급](#issuing-api-tokens)
    - [토큰 권한(Abilities)](#token-abilities)
    - [라우트 보호](#protecting-routes)
    - [토큰 폐기](#revoking-tokens)
    - [토큰 만료](#token-expiration)
- [SPA 인증](#spa-authentication)
    - [구성](#spa-configuration)
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

[Laravel Sanctum](https://github.com/laravel/sanctum)은 SPA(싱글 페이지 애플리케이션), 모바일 애플리케이션, 그리고 간단한 토큰 기반 API를 위한 경량 인증 시스템을 제공합니다. Sanctum을 사용하면 애플리케이션의 각 사용자가 계정별로 여러 개의 API 토큰을 생성할 수 있습니다. 이 토큰들은 토큰이 수행할 수 있는 동작을 정의하는 권한(abilities) 또는 범위(scopes)를 가질 수 있습니다.

<a name="how-it-works"></a>
### 동작 방식

Laravel Sanctum은 서로 다른 두 가지 문제를 해결하기 위해 존재합니다. 라이브러리를 더 깊이 살펴보기 전에 각각을 설명하겠습니다.

<a name="how-it-works-api-tokens"></a>
#### API 토큰

먼저, Sanctum은 OAuth의 복잡함 없이 사용자의 API 토큰을 발급할 수 있는 간단한 패키지입니다. 이 기능은 GitHub와 기타 애플리케이션의 "개인 액세스 토큰" 발급 방식에서 영감을 받았습니다. 예를 들어, 애플리케이션의 "계정 설정" 화면에서 사용자가 직접 계정용 API 토큰을 생성할 수 있게 할 수 있습니다. Sanctum으로 이러한 토큰을 생성·관리할 수 있습니다. 이 토큰들은 일반적으로 굉장히 긴 만료 기간(여러 해)을 가지고 있지만, 사용자가 언제든 수동으로 폐기할 수 있습니다.

Laravel Sanctum은 이 기능을 위해 사용자 API 토큰을 하나의 데이터베이스 테이블에 저장하며, 들어오는 HTTP 요청의 `Authorization` 헤더에 유효한 API 토큰이 포함되어 있는지 확인해 인증을 처리합니다.

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증

두 번째로, Sanctum은 라라벨 기반 API와 통신해야 하는 싱글 페이지 애플리케이션(SPA)를 간단하게 인증할 수 있는 방법을 제공합니다. 이러한 SPA는 라라벨 애플리케이션과 동일한 저장소에 존재할 수도 있고, Next.js나 Nuxt로 만든 별도의 저장소에 존재할 수도 있습니다.

이 기능에서는 어떠한 종류의 토큰도 사용하지 않습니다. 대신, Sanctum은 Laravel이 기본으로 제공하는 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum은 이를 위해 Laravel의 `web` 인증 가드를 이용합니다. 이 방식은 CSRF 보호, 세션 인증의 이점, 그리고 XSS를 통한 인증 정보 노출 방지 효과를 줍니다.

Sanctum은 오로지 들어오는 요청이 자신의 SPA 프론트엔드에서 왔을 때만 쿠키를 통한 인증을 시도합니다. HTTP 요청을 검사할 때 먼저 인증 쿠키가 있는지 확인하고, 없으면 그때 `Authorization` 헤더에서 유효한 API 토큰이 있는지 검사합니다.

> [!NOTE]
> Sanctum을 API 토큰 인증에만 사용하거나, SPA 인증에만 사용해도 괜찮습니다. Sanctum을 사용한다고 해서 반드시 두 가지 기능을 모두 써야 하는 것은 아닙니다.

<a name="installation"></a>
## 설치 (Installation)

`install:api` 아티즌 명령어로 Laravel Sanctum을 설치할 수 있습니다.

```shell
php artisan install:api
```

다음으로, Sanctum을 SPA 인증에 활용할 예정이라면 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참고하시기 바랍니다.

<a name="configuration"></a>
## 구성 (Configuration)

<a name="overriding-default-models"></a>
### 기본 모델 재정의

반드시 필요한 것은 아니지만, Sanctum이 내부적으로 사용하는 `PersonalAccessToken` 모델을 확장할 수 있습니다.

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

그 다음 Sanctum에서 제공하는 `usePersonalAccessTokenModel` 메서드를 사용해 커스텀 모델을 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출해야 합니다.

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * 어플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## API 토큰 인증 (API Token Authentication)

> [!NOTE]
> 자신의 1st-party SPA를 인증하는 용도로 API 토큰을 사용해서는 안 됩니다. 대신 Sanctum의 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum을 사용하면 API 요청을 인증하기 위한 API 토큰 또는 개인 액세스 토큰을 발급할 수 있습니다. 이 토큰을 사용하는 요청에서는 `Authorization` 헤더에 `Bearer` 토큰으로 포함해야 합니다.

사용자별로 토큰을 발급하려면 `User` 모델에 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다.

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

토큰을 발급하려면 `createToken` 메서드를 사용합니다. 이 메서드는 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해시 처리되지만, 생성 직후에는 `NewAccessToken` 인스턴스의 `plainTextToken` 속성에서 평문 값을 확인할 수 있습니다. 토큰 생성 직후 사용자에게 이 값을 반드시 표시해 주세요.

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` 트레이트에서 제공하는 `tokens` Eloquent 연관관계를 이용해 사용자의 모든 토큰에 접근할 수 있습니다.

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### 토큰 권한(Abilities)

Sanctum에서는 토큰에 "권한(abilities)"을 부여할 수 있습니다. 권한은 OAuth의 "스코프(scopes)"와 비슷한 개념입니다. `createToken` 메서드의 두 번째 인수로 문자열 배열을 전달해 토큰 권한을 지정할 수 있습니다.

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum으로 인증된 들어오는 요청을 처리할 때, 해당 토큰에 특정 권한이 있는지 `tokenCan` 또는 `tokenCant` 메서드로 확인할 수 있습니다.

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum에는 요청을 인증할 때 토큰이 특정 권한을 가지고 있는지 검사할 수 있는 두 가지 미들웨어가 있습니다. 먼저, `bootstrap/app.php` 파일에서 다음과 같이 미들웨어 별칭을 등록합니다.

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

`abilities` 미들웨어는 들어오는 요청의 토큰이 지정된 모든 권한을 가지고 있는지 검사합니다.

```php
Route::get('/orders', function () {
    // 토큰이 "check-status"와 "place-orders" 권한 모두를 갖고 있어야 함...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` 미들웨어는 들어오는 토큰이 나열된 권한 중 최소 하나라도 가지고 있는지 확인합니다.

```php
Route::get('/orders', function () {
    // 토큰이 "check-status" 혹은 "place-orders" 권한 중 하나라도 있으면 통과...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### 1st-party UI 요청에 대한 특이사항

편의상, 만약 들어온 인증 요청이 1st-party SPA에서 발생한 것이고, Sanctum의 [SPA 인증](#spa-authentication)을 사용하는 경우, `tokenCan` 메서드는 항상 `true`를 반환합니다.

하지만 이것이 무조건 해당 동작이 허용되어야 한다는 뜻은 아닙니다. 일반적으로 애플리케이션의 [인가 정책](/docs/master/authorization#creating-policies)에서 해당 권한(ability)에 대한 권한 부여 여부와 사용자 인스턴스 자체가 해당 동작을 할 수 있는지를 결정하게 됩니다.

예를 들어, 서버를 관리하는 애플리케이션이라면, 토큰이 서버 업데이트 권한이 있는지는 물론 해당 서버가 해당 유저의 소유인지까지 체크해야 합니다.

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

처음에는 1st-party UI 요청에서 `tokenCan`이 항상 `true` 를 반환하는 것이 다소 이상해 보일 수 있습니다. 하지만 이 방식은 항상 API 토큰이 있는 것처럼 가정하고 `tokenCan`을 이용해 권한 검사를 일관적으로 할 수 있으므로, 애플리케이션의 인가 정책 안에서 요청이 UI에서 발생했는지, 외부 API 컨슈머에서 발생했는지 구분하지 않아도 됩니다.

<a name="protecting-routes"></a>
### 라우트 보호

모든 들어오는 요청이 인증되어야만 접근할 수 있도록 하려면, `routes/web.php`, `routes/api.php` 라우트 파일에서 보호할 라우트에 `sanctum` 인증 가드를 붙여야 합니다. 이 가드는 쿠키 인증이 있는 상태 유지성(stateful) 요청이나, 3rd-party 요청의 경우 유효한 API 토큰 헤더가 포함되어 있어야 인증이 통과됩니다.

왜 `routes/web.php` 파일의 라우트도 `sanctum` 가드를 사용할 것을 권장할까요? 그 이유는 Sanctum이 들어오는 요청을 먼저 세션 인증 쿠키로 인증하려 시도하고, 해당 쿠키가 없으면 `Authorization` 헤더의 토큰을 사용해 인증을 시도하기 때문입니다. 모든 요청을 Sanctum으로 인증하면, 현재 인증된 사용자 인스턴스에서 언제든 `tokenCan` 을 호출할 수 있게 됩니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### 토큰 폐기

`Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 관계를 사용해 데이터베이스에서 토큰을 삭제함으로써 토큰을 "폐기"할 수 있습니다.

```php
// 모든 토큰 폐기...
$user->tokens()->delete();

// 현재 요청을 인증한 토큰 폐기...
$request->user()->currentAccessToken()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며, [토큰 폐기](#revoking-tokens)를 통해서만 무효화할 수 있습니다. 하지만, 애플리케이션의 API 토큰에 만료 시간을 설정하고 싶다면 `sanctum` 설정 파일의 `expiration` 옵션을 사용해 분 단위로 지정할 수 있습니다.

```php
'expiration' => 525600,
```

각 토큰별로 만료 시간을 개별 지정하려면, `createToken` 메서드의 세 번째 인수로 만료 시간을 전달하면 됩니다.

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

애플리케이션에 토큰 만료 시간을 설정했다면, [스케줄러 작업](/docs/master/scheduling)을 등록해 만료된 토큰을 정기적으로 삭제하는 것이 좋습니다. 이를 위해 Sanctum에서 제공하는 `sanctum:prune-expired` 아티즌 명령어를 사용할 수 있습니다. 예를 들어, 만료 후 24시간 지난 모든 토큰을 매일 삭제하도록 예약할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증 (SPA Authentication)

Sanctum은 라라벨 기반 API와 통신해야 하는 SPA(싱글 페이지 애플리케이션)를 인증하는 간단한 방법도 제공합니다. 이 SPA는 라라벨 애플리케이션과 같은 저장소에 존재하거나, 완전히 별도로 분리된 저장소일 수도 있습니다.

이 경우 토큰이 아니라, Laravel의 기본 쿠키 기반 세션 인증 서비스를 사용합니다. 이 방식은 CSRF 보호, 세션 인증, XSS로 인한 인증 정보 노출 방지 등의 이점을 제공합니다.

> [!WARNING]
> 인증을 위해 SPA와 API는 반드시 동일한 최상위 도메인을 공유해야 합니다. 서로 다른 서브도메인은 괜찮지만, 최상위 도메인은 같아야 합니다. 또한, 요청 시 반드시 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 추가해야 합니다.

<a name="spa-configuration"></a>
### 구성

<a name="configuring-your-first-party-domains"></a>
#### 1st-party 도메인 설정

먼저, SPA가 요청을 보내는 도메인을 구성해야 합니다. 이 도메인들은 Sanctum의 설정 파일 `sanctum`의 `stateful` 옵션에서 지정할 수 있습니다. 이 설정은 요청 시 Laravel 세션 쿠키를 사용해 상태가 유지되는(stateful) 인증이 활성화될 도메인을 결정합니다.

1st-party 도메인 설정을 돕기 위해 Sanctum은 두 개의 헬퍼 함수를 제공합니다. `Sanctum::currentApplicationUrlWithPort()`는 `APP_URL` 환경 변수에 지정된 현재 애플리케이션 URL을 반환합니다. `Sanctum::currentRequestHost()`는 stateful 도메인 목록에 플레이스홀더로 삽입되어 런타임 시 현재 요청의 호스트로 대체되므로, 같은 도메인의 모든 요청이 상태 유지성으로 간주됩니다.

> [!WARNING]
> 만약 포트가 포함된 URL(`127.0.0.1:8000`)로 애플리케이션에 접근한다면, 반드시 포트 번호까지 도메인에 포함해야 합니다.

<a name="sanctum-middleware"></a>
#### Sanctum 미들웨어

다음으로, SPA에서 온 요청은 Laravel의 세션 쿠키로 인증되도록, 그리고 동시에 외부 3rd-party나 모바일 앱의 요청도 API 토큰을 통해 인증될 수 있도록 해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출하면 쉽게 설정됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS와 쿠키 설정

별도의 서브도메인에서 동작하는 SPA에서 인증 문제가 발생한다면, CORS(교차 출처 리소스 공유)나 세션 쿠키 설정이 잘못된 경우일 수 있습니다.

`config/cors.php` 설정 파일은 기본적으로 공개되지 않습니다. Laravel의 CORS 옵션을 커스터마이징하려면, 다음 아티즌 명령어로 전체 `cors` 설정 파일을 퍼블리시하세요.

```shell
php artisan config:publish cors
```

애플리케이션의 CORS 설정에서 반드시 `Access-Control-Allow-Credentials` 헤더가 `True`로 반환되도록 해야 합니다. 이는 `config/cors.php` 설정 파일의 `supports_credentials` 옵션을 `true`로 지정해 달성할 수 있습니다.

또한, 전체적으로 사용하는 axios 인스턴스의 `withCredentials`와 `withXSRFToken` 옵션을 활성화해 주어야 합니다. 일반적으로 이 설정은 `resources/js/bootstrap.js` 파일에서 처리합니다. 프론트엔드에서 axios를 사용하지 않는다면, 자체 HTTP 클라이언트에서도 동등하게 설정해야 합니다.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

마지막으로, 애플리케이션의 세션 쿠키 도메인이 루트 도메인의 모든 서브도메인을 지원하도록 앞에 점(`.`)을 붙여 구성파일 `config/session.php`에 설정해야 합니다.

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 인증 절차

<a name="csrf-protection"></a>
#### CSRF 보호

SPA에서 인증을 시작하려면, SPA의 "로그인" 페이지에서 `/sanctum/csrf-cookie` 엔드포인트에 먼저 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다.

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

이 요청을 통해 Laravel은 현재 CSRF 토큰이 포함된 `XSRF-TOKEN` 쿠키를 설정합니다. 이 토큰은 URL 디코딩되어 이후 요청의 `X-XSRF-TOKEN` 헤더로 전달되어야 하며, axios나 Angular HttpClient 같은 HTTP 클라이언트가 자동으로 처리해줍니다. 만약 사용하는 자바스크립트 HTTP 라이브러리가 이 값을 자동으로 설정하지 않는다면, 해당 쿠키의 값(URL 디코드된 값)을 수동으로 `X-XSRF-TOKEN` 헤더에 지정해 주어야 합니다.

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화되면, Laravel 애플리케이션의 `/login` 라우트로 `POST` 요청을 보내야 합니다. 이 `/login` 라우트는 [직접 구현](/docs/master/authentication#authenticating-users)할 수도 있고, [Laravel Fortify](/docs/master/fortify) 같은 헤드리스 인증 패키지를 사용할 수도 있습니다.

로그인 요청이 성공하면 세션 쿠키가 발급되어, 이후 모든 요청은 자동으로 인증 상태가 됩니다. 또한, 이미 `/sanctum/csrf-cookie` 라우트에 요청을 했기 때문에, 자바스크립트 HTTP 클라이언트가 쿠키의 값을 헤더에 잘 담아 보낸다면 이후 요청 역시 CSRF 보호가 자동 적용됩니다.

사용자의 세션이 만료(오랜 미활동 등)된 경우 Laravel에서 401 또는 419 HTTP 에러가 반환될 수 있으니, 이 경우 SPA의 로그인 페이지로 리다이렉션해야 합니다.

> [!WARNING]
> 직접 `/login` 엔드포인트를 구현해도 되지만, 반드시 Laravel이 기본 제공하는 [세션 기반 인증 서비스](/docs/master/authentication#authenticating-users)를 사용해 사용자 인증을 처리해야 합니다. 일반적으로는 `web` 인증 가드를 사용합니다.

<a name="protecting-spa-routes"></a>
### 라우트 보호

모든 들어오는 요청에 인증이 필요하도록 만들려면 `routes/api.php` 내 라우트에 `sanctum` 인증 가드를 연결하세요. 이 가드는 SPA에서 오는 상태 유지성(stateful) 인증 요청과 외부에서 올 수 있는 유효한 API 토큰을 모두 지원합니다.

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### 프라이빗 브로드캐스트 채널 인가

SPA에서 [프라이빗 / 프레즌스 브로드캐스트 채널](/docs/master/broadcasting#authorizing-channels)로 인증이 필요한 경우, `bootstrap/app.php`의 `withRouting` 메서드에서 `channels` 항목을 제거해야 합니다. 대신, `withBroadcasting` 메서드를 호출하여 브로드캐스팅 라우트에 올바른 미들웨어를 명시할 수 있습니다.

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

그리고 Pusher 인증 요청이 성공하려면, [Laravel Echo](/docs/master/broadcasting#client-side-installation) 설정 시 커스텀 Pusher `authorizer`를 제공해야 합니다. 이를 통해 SPA가 [교차 도메인 요청에 적합하게 설정된 axios 인스턴스](#cors-and-cookies)를 제대로 사용하게 할 수 있습니다.

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

모바일 애플리케이션이 API 요청을 인증할 때도 Sanctum 토큰을 사용할 수 있습니다. 기본 흐름은 외부 API 요청을 인증하는 것과 거의 같지만, 토큰 발급 과정에 약간 차이가 있습니다.

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발급

먼저, 사용자의 이메일(또는 사용자명), 비밀번호, 그리고 디바이스 이름을 받아 새로운 Sanctum 토큰을 반환하는 라우트를 구현합니다. 이때 "디바이스 이름"은 사용자가 알아보기 쉬운 임의의 값(예시: "Nuno의 iPhone 12")을 전달하면 됩니다.

일반적으로 모바일 앱의 "로그인" 화면에서 이 엔드포인트로 요청을 보내면, 반환된 평문 API 토큰을 모바일 기기에 저장하여 이후 요청에 활용할 수 있습니다.

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

모바일 애플리케이션에서 API 요청 시에는 반드시 이 토큰을 `Authorization` 헤더의 `Bearer` 토큰으로 포함해서 보내야 합니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰에도 [토큰 권한(abilities)](#token-abilities)을 자유롭게 지정할 수 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 라우트 보호

앞서 설명한 것처럼 모든 요청을 인증이 필요하도록 하려면 라우트에 `sanctum` 인증 가드를 적용하세요.

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### 토큰 폐기

모바일 기기에서 발급된 API 토큰을 폐기할 수 있도록, 웹 애플리케이션 UI의 "계정 설정" 등에서 토큰 이름과 함께 "폐기" 버튼을 노출할 수 있습니다. 사용자가 "폐기"를 누른 경우, 해당 토큰을 데이터베이스에서 삭제하면 됩니다. 사용자 API 토큰은 `Laravel\Sanctum\HasApiTokens` 트레이트의 `tokens` 관계로 접근할 수 있습니다.

```php
// 모든 토큰 폐기...
$user->tokens()->delete();

// 특정 토큰 폐기...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## 테스트 (Testing)

테스트 시에는 `Sanctum::actingAs` 메서드를 사용해 사용자를 인증하고 토큰에 부여할 권한을 지정할 수 있습니다.

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

토큰에 모든 권한을 부여하려면, `actingAs` 메서드의 권한 배열에 `*`를 포함시키면 됩니다.

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
