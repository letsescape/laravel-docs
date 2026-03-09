# 인증 (Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려 사항](#introduction-database-considerations)
    - [생태계 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 검색](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 속도 제한](#login-throttling)
- [수동으로 사용자 인증하기](#authenticating-users)
    - [기억하는 사용자](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP 기본 인증](#http-basic-authentication)
    - [세션 없는 HTTP 기본 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 장치의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [구성](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [사용자 지정 Guard 추가](#adding-custom-guards)
    - [클로저 Request Guard](#closure-request-guards)
- [사용자 지정 User Provider 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [인증 가능한 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 하지만 이 기능을 직접 구현하는 일은 복잡할 뿐 아니라 보안상 위험도 따를 수 있습니다. Laravel은 인증 기능을 빠르고, 안전하고, 간단하게 구현할 수 있도록 필요한 도구를 제공합니다.

Laravel의 인증 기능은 크게 `guard`와 `provider`로 구성됩니다. `guard`는 각 요청에서 사용자를 어떻게 인증할지 정의합니다. 예를 들어 Laravel에는 세션 저장소와 쿠키로 상태를 유지하는 `session` guard가 기본 제공됩니다.

`provider`는 영구 저장소에서 사용자를 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 사용한 사용자 조회를 지원하며, 필요하다면 애플리케이션에 맞는 provider를 추가로 정의할 수도 있습니다.

애플리케이션의 인증 구성 파일은 `config/auth.php`에 있습니다. 이 파일에는 Laravel 인증 서비스의 동작을 조정하기 위한 잘 문서화된 몇 가지 옵션이 포함되어 있습니다.

> [!NOTE]
> `guard`와 `provider`를 "역할(role)"이나 "권한(permission)"과 혼동하면 안 됩니다. 권한을 기준으로 사용자 동작을 제어하는 방법은 [인가](/docs/12.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶다면 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션을 실행한 뒤 브라우저에서 `/register` 또는 애플리케이션에 연결된 다른 URL로 이동하면 됩니다. 스타터 키트가 전체 인증 시스템의 기본 구조를 자동으로 준비해 줍니다.

**최종 Laravel 애플리케이션에서 스타터 키트를 사용하지 않더라도 [스타터 키트](/docs/12.x/starter-kits)를 한 번 설치해 보면 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구성되는지 배우는 데 큰 도움이 됩니다.** Laravel 스타터 키트에는 인증용 컨트롤러, 라우트, 뷰가 포함되어 있으므로 관련 파일의 코드를 살펴보면 Laravel의 인증 기능이 어떻게 구현되는지 이해할 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려 사항

기본적으로 Laravel에는 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)가 포함되어 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용될 수 있습니다.

애플리케이션이 Eloquent를 사용하지 않는 경우 Laravel 쿼리 빌더를 사용하는 `database` 인증 provider를 사용할 수 있습니다. 애플리케이션이 MongoDB를 사용하는 경우 MongoDB의 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 확인하세요.

`App\Models\User` 모델에 대한 데이터베이스 스키마를 빌드할 때 비밀번호 열 길이가 60자 이상인지 확인하세요. 물론 새로운 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이 길이를 초과하는 열을 생성합니다.

또한 `users`(또는 이에 상응하는) 테이블에 100자의 null 허용 문자열 `remember_token` 열이 포함되어 있는지 확인해야 합니다. 이 열은 애플리케이션에 로그인할 때 "기억하기" 옵션을 선택한 사용자를 위한 토큰을 저장하는 데 사용됩니다. 다시 말하지만, 새 Laravel 애플리케이션에 포함된 기본 `users` 테이블 마이그레이션에는 이미 이 열이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 생태계 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel의 전반적인 인증 생태계를 살펴보고 각 패키지가 어떤 목적에 맞는지 정리해 보겠습니다.

먼저 인증 작동 방식을 고려하세요. 웹 브라우저를 사용할 때 사용자는 로그인 양식을 통해 사용자 이름과 비밀번호를 제공합니다. 이러한 자격 증명이 올바른 경우 애플리케이션은 인증된 사용자에 대한 정보를 사용자의 [세션](/docs/12.x/session)에 저장합니다. 브라우저에 발행된 쿠키에는 세션 ID가 포함되어 있어 애플리케이션에 대한 후속 요청이 사용자를 올바른 세션과 연결할 수 있습니다. 세션 쿠키가 수신된 후 애플리케이션은 세션 ID를 기반으로 세션 데이터를 검색하고 인증 정보가 세션에 저장되었음을 확인하며 사용자를 "인증된" 것으로 간주합니다.

원격 서비스가 API에 액세스하기 위해 인증해야 하는 경우 웹 브라우저가 없기 때문에 일반적으로 쿠키가 인증에 사용되지 않습니다. 대신 원격 서비스는 각 요청마다 API 토큰을 API로 보냅니다. 애플리케이션은 유효한 API 토큰 테이블에 대해 들어오는 토큰의 유효성을 검사하고 해당 API 토큰과 연결된 사용자가 수행하는 요청을 "인증"할 수 있습니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel에는 보통 `Auth`와 `Session` 파사드로 접근하는 내장 인증 및 세션 서비스가 포함되어 있습니다. 이 기능은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 이를 통해 사용자의 자격 증명을 검증하고 사용자를 인증할 수 있습니다. 또한 필요한 인증 데이터를 자동으로 사용자 세션에 저장하고 세션 쿠키도 발급합니다. 이러한 서비스를 사용하는 방법은 이 문서 전체에서 설명합니다.

**애플리케이션 스타터 키트**

이 문서에서 설명하는 것처럼 이러한 인증 서비스와 직접 상호작용해 애플리케이션만의 인증 계층을 구축할 수도 있습니다. 다만 더 빠르게 시작할 수 있도록 전체 인증 계층을 현대적인 형태로 미리 구성해 주는 [무료 스타터 키트](/docs/12.x/starter-kits)도 제공됩니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰을 관리하고 API 토큰으로 들어오는 요청을 인증하는 데 도움이 되는 두 가지 선택적 패키지, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들과 Laravel의 내장 쿠키 기반 인증 라이브러리는 서로 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 초점을 맞추고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 초점을 맞춥니다. 많은 애플리케이션이 Laravel의 내장 쿠키 기반 인증 서비스와 Laravel의 API 인증 패키지 중 하나를 함께 사용합니다.

**Passport**

Passport는 여러 종류의 토큰을 발급할 수 있는 다양한 OAuth2 `grant type`을 제공하는 OAuth2 인증 패키지입니다. 전반적으로 API 인증에 적합한 강력하고 복잡한 패키지지만, 대부분의 애플리케이션은 OAuth2 사양이 제공하는 복잡한 기능 전체를 필요로 하지 않습니다. 그래서 사용자와 개발자 모두에게 다소 혼란을 줄 수 있습니다. 또한 역사적으로 개발자들은 Passport 같은 OAuth2 솔루션으로 SPA나 모바일 애플리케이션을 어떻게 인증해야 하는지 자주 헷갈려 했습니다.

**Sanctum**

OAuth2의 복잡성과 그로 인한 개발자 혼란에 대응하기 위해, 우리는 웹 브라우저에서 오는 자사 웹 요청과 토큰 기반 API 요청을 모두 처리할 수 있는 더 단순하고 효율적인 인증 패키지를 만들었습니다. 그 결과가 [Laravel Sanctum](/docs/12.x/sanctum)입니다. Sanctum은 API와 함께 자사 웹 UI를 제공하는 애플리케이션, 백엔드 Laravel 애플리케이션과 별도로 존재하는 SPA, 그리고 모바일 클라이언트를 제공하는 애플리케이션에서 우선적으로 고려할 만한 인증 패키지입니다.

Laravel Sanctum은 애플리케이션의 전체 인증 과정을 관리할 수 있는 하이브리드 웹/API 인증 패키지입니다. Sanctum 기반 애플리케이션이 요청을 받으면, 먼저 해당 요청에 인증된 세션을 가리키는 세션 쿠키가 포함되어 있는지 확인합니다. 이를 위해 Sanctum은 앞서 설명한 Laravel의 내장 인증 서비스를 호출합니다. 요청이 세션 쿠키로 인증되지 않았다면, Sanctum은 API 토큰이 포함되어 있는지 검사합니다. API 토큰이 있으면 그 토큰으로 요청을 인증합니다. 이 과정에 대한 자세한 내용은 Sanctum의 ["작동 방식"](/docs/12.x/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택

요약하면, 브라우저를 사용하여 애플리케이션에 액세스하고 모놀리식 Laravel 애플리케이션을 구축하는 경우 애플리케이션은 Laravel의 내장 인증 서비스를 사용하게 됩니다.

다음으로, 애플리케이션이 제3자가 사용할 API를 제공하는 경우 [Passport](/docs/12.x/passport) 또는 [Sanctum](/docs/12.x/sanctum) 중에서 선택하여 애플리케이션에 API 토큰 인증을 제공합니다. 일반적으로 Sanctum는 "범위" 또는 "능력" 지원을 포함하여 API 인증, SPA 인증 및 모바일 인증을 위한 간단하고 완전한 솔루션이므로 가능한 경우 선호되어야 합니다.

Laravel 백엔드로 구동되는 단일 페이지 애플리케이션(SPA)을 구축하는 경우에는 [Laravel Sanctum](/docs/12.x/sanctum)을 사용하는 것이 좋습니다. Sanctum을 사용할 때는 [백엔드 인증 라우트를 직접 구현](#authenticating-users)하거나, 회원가입, 비밀번호 재설정, 이메일 인증 같은 기능을 위한 라우트와 컨트롤러를 제공하는 헤드리스 인증 백엔드 서비스인 [Laravel Fortify](/docs/12.x/fortify)를 활용할 수 있습니다.

애플리케이션에 OAuth2 사양에서 제공하는 모든 기능이 절대적으로 필요한 경우 Passport를 선택할 수 있습니다.

빠르게 시작하고 싶다면, Laravel이 권장하는 내장 인증 스택을 이미 적용한 새 애플리케이션을 시작하는 방법으로 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 추천합니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 문서의 이 부분에서는 빠르게 시작할 수 있도록 UI scaffolding이 포함된 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)로 사용자를 인증하는 방법을 설명합니다. Laravel의 인증 시스템과 직접 통합하려면 [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저 [Laravel 애플리케이션 스타터 키트를 설치](/docs/12.x/starter-kits)해야 합니다. 당사의 스타터 키트는 새로운 Laravel 애플리케이션에 인증을 통합하기 위한 아름답게 디자인된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 검색

스타터 킷에서 애플리케이션을 작성하고 사용자가 애플리케이션에 등록하고 인증할 수 있도록 허용한 후에는 현재 인증된 사용자와 상호작용해야 하는 경우가 많습니다. 들어오는 요청을 처리하는 동안 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

또는 사용자가 인증되면 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 액세스할 수 있습니다. 타입힌트 클래스가 컨트롤러 메서드에 자동으로 삽입된다는 점을 기억하세요. `Illuminate\Http\Request` 객체를 타입힌트하면 요청의 `user` 메서드를 통해 애플리케이션의 모든 컨트롤러 메서드에서 인증된 사용자에 편리하게 액세스할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자가 인증되었는지 확인

들어오는 HTTP 요청을 하는 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증되면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드를 사용하여 사용자가 인증되었는지 확인할 수 있더라도 일반적으로 특정 라우트 / 컨트롤러에 대한 사용자 액세스를 허용하기 전에 미들웨어를 사용하여 사용자가 인증되었는지 확인합니다. 이에 대해 자세히 알아보려면 [라우트 보호](/docs/12.x/authentication#protecting-routes) 문서를 확인하세요.

<a name="protecting-routes"></a>
### 라우트 보호

[라우트 미들웨어](/docs/12.x/middleware)는 인증된 사용자만 특정 라우트에 액세스하도록 허용하는 데 사용할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)인 `auth` 미들웨어를 기본 제공합니다. 이 미들웨어는 이미 Laravel에 의해 내부적으로 별칭이 지정되어 있으므로 미들웨어를 라우트 정의에 연결하기만 하면 됩니다.

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면 사용자를 `login` [라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다. 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드를 사용하여 이 동작을 수정할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리디렉션

`guest` 미들웨어가 인증된 사용자를 감지하면 사용자를 `dashboard` 또는 `home` 이름의 라우트로 리디렉션합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectUsersTo` 메서드를 사용하면 이 동작을 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정

`auth` 미들웨어를 라우트에 연결할 때 사용자를 인증하는 데 사용해야 하는 "가드"를 지정할 수도 있습니다. 지정된 가드는 `auth.php` 구성 파일의 `guards` 배열에 있는 키 중 하나와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한

[애플리케이션 스타터 키트](/docs/12.x/starter-kits) 중 하나를 사용하는 경우 로그인 시도에 속도 제한이 자동으로 적용됩니다. 기본적으로 사용자는 여러 번 시도한 후에도 올바른 자격 증명을 제공하지 못하면 1분 동안 로그인할 수 없습니다. 제한은 사용자의 사용자 이름/이메일 주소 및 IP 주소에 따라 고유합니다.

> [!NOTE]
> 애플리케이션에서 다른 라우트의 속도를 제한하려면 [속도 제한 문서](/docs/12.x/routing#rate-limiting)를 확인하세요.

<a name="authenticating-users"></a>
## 수동으로 사용자 인증 (Manually Authenticating Users)

Laravel의 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)에 포함된 인증 scaffolding을 반드시 사용할 필요는 없습니다. 이를 사용하지 않기로 했다면 Laravel의 인증 클래스를 직접 사용해 사용자 인증을 관리하면 됩니다. 생각보다 어렵지 않습니다.

Laravel의 인증 서비스는 `Auth` [파사드](/docs/12.x/facades)를 통해 사용하므로, 먼저 클래스 상단에서 `Auth` 파사드를 가져와야 합니다. 다음으로 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 보통 애플리케이션의 로그인 폼에서 들어온 인증 시도를 처리할 때 사용합니다. 인증에 성공했다면 [세션 고정](https://en.wikipedia.org/wiki/Session_fixation)을 방지하기 위해 사용자의 [세션](/docs/12.x/session)을 다시 생성해야 합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

`attempt` 메서드는 키/값 쌍의 배열을 첫 번째 인수로 허용합니다. 배열의 값은 데이터베이스 테이블에서 사용자를 찾는 데 사용됩니다. 따라서 위의 예에서는 `email` 열의 값으로 사용자를 검색합니다. 사용자가 발견되면 데이터베이스에 저장된 해시된 비밀번호는 배열을 통해 메서드에 전달된 `password` 값과 비교됩니다. 들어오는 요청의 `password` 값을 해시하면 안 됩니다. 프레임워크가 값을 데이터베이스의 해시된 비밀번호와 비교하기 전에 자동으로 해시하기 때문입니다. 두 개의 해시된 비밀번호가 일치하면 사용자에 대해 인증된 세션이 시작됩니다.

Laravel의 인증 서비스는 인증 guard의 `provider` 설정을 기준으로 데이터베이스에서 사용자를 조회한다는 점을 기억하세요. 기본 `config/auth.php` 설정 파일에는 Eloquent user provider가 지정되어 있으며, 사용자를 조회할 때 `App\Models\User` 모델을 사용합니다. 애플리케이션 요구 사항에 따라 이 값은 변경할 수 있습니다.

인증이 성공하면 `attempt` 메서드는 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

Laravel의 리디렉터가 제공하는 `intended` 메서드는 인증 미들웨어에 의해 차단되기 전에 액세스를 시도했던 URL로 사용자를 리디렉션합니다. 의도한 대상을 사용할 수 없는 경우 대체 URI가 이 메서드에 제공될 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정

원하는 경우 사용자의 이메일 및 비밀번호 외에 추가 쿼리 조건을 인증 쿼리에 추가할 수도 있습니다. 이를 달성하려면 `attempt` 메서드에 전달된 배열에 쿼리 조건을 추가하기만 하면 됩니다. 예를 들어, 사용자가 "활성"으로 표시되어 있는지 확인할 수 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

복잡한 쿼리 조건의 경우 자격 증명 배열에 클로저를 제공할 수 있습니다. 이 클로저는 쿼리 인스턴스와 함께 호출되므로 애플리케이션의 요구 사항에 따라 쿼리를 사용자 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> 이 예에서 `email`는 필수 옵션이 아니며 단지 예로서 사용됩니다. 데이터베이스 테이블의 "사용자 이름"에 해당하는 열 이름을 사용해야 합니다.

두 번째 인수로 클로저를 수신하는 `attemptWhen` 메서드는 실제로 사용자를 인증하기 전에 잠재적인 사용자에 대한 보다 광범위한 검사를 수행하는 데 사용될 수 있습니다. 클로저는 잠재적인 사용자를 수신하고 사용자가 인증될 수 있는지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스에 액세스

`Auth` 파사드의 `guard` 메서드를 통해, 사용자를 인증할 때 어떤 가드 인스턴스를 활용하고 싶은지 지정할 수 있습니다. 이를 통해 완전히 별도의 인증 가능한 모델 또는 사용자 테이블을 사용하여 애플리케이션의 개별 부분에 대한 인증을 관리할 수 있습니다.

`guard` 메서드에 전달된 가드 이름은 `auth.php` 구성 파일에 구성된 가드 중 하나와 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션은 로그인 양식에 "기억하기" 확인란을 제공합니다. 애플리케이션에 "기억하기" 기능을 제공하려면 부울 값을 `attempt` 메서드의 두 번째 인수로 전달할 수 있습니다.

이 값이 `true`이면 Laravel은 사용자의 인증 상태를 무기한 유지하거나 수동으로 로그아웃할 때까지 유지합니다. `users` 테이블에는 "기억하기" 토큰을 저장하는 데 사용되는 문자열 `remember_token` 열이 포함되어야 합니다. 새로운 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션에는 이미 다음 열이 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

애플리케이션이 "기억하기" 기능을 제공하는 경우 `viaRemember` 메서드를 사용하여 현재 인증된 사용자가 "기억하기" 쿠키를 사용하여 인증되었는지 확인할 수 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증

기존 사용자 인스턴스를 현재 인증된 사용자로 설정해야 하는 경우 사용자 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달할 수 있습니다. 지정된 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)의 구현이어야 합니다. Laravel에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 이 인증 방법은 사용자가 애플리케이션에 등록한 직후와 같이 유효한 사용자 인스턴스가 이미 있는 경우에 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

`login` 메서드의 두 번째 인수로 부울 값을 전달할 수 있습니다. 이 값은 인증된 세션에 "기억하기" 기능이 필요한지 여부를 나타냅니다. 이는 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 인증된다는 것을 기억하세요.

```php
Auth::login($user, $remember = true);
```

필요한 경우 `login` 메서드를 호출하기 전에 인증 가드를 지정할 수 있습니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증

데이터베이스 레코드의 기본 키를 사용하여 사용자를 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증하려는 사용자의 기본 키를 허용합니다.

```php
Auth::loginUsingId(1);
```

`loginUsingId` 메서드의 `remember` 인수에 부울 값을 전달할 수 있습니다. 이 값은 인증된 세션에 "기억하기" 기능이 필요한지 여부를 나타냅니다. 이는 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 인증된다는 것을 기억하세요.

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 한 번만 사용자 인증하기

`once` 메서드를 사용하면 단일 요청에 한해 사용자를 인증할 수 있습니다. 이 메서드를 호출할 때는 세션이나 쿠키를 사용하지 않으며, `Login` 이벤트도 디스패치되지 않습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP 기본 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 전용 "로그인" 페이지를 설정하지 않고도 애플리케이션 사용자를 인증하는 빠른 방법을 제공합니다. 시작하려면 `auth.basic` [미들웨어](/docs/12.x/middleware)를 라우트에 연결하세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 포함되어 있으므로 정의할 필요가 없습니다.

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

미들웨어를 라우트에 연결하면, 브라우저로 해당 라우트에 접근할 때 자격 증명 입력 창이 자동으로 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자의 "사용자 이름"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI에 대한 참고 사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php) 및 Apache를 사용하여 Laravel 애플리케이션을 제공하는 경우 HTTP 기본 인증이 올바르게 작동하지 않을 수 있습니다. 이러한 문제를 해결하기 위해 애플리케이션의 `.htaccess` 파일에 다음 줄을 추가할 수 있습니다.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 세션 없는 HTTP 기본 인증

세션에 사용자 식별 쿠키를 저장하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 이 방식은 애플리케이션 API 요청을 HTTP 인증으로 처리하려는 경우에 특히 유용합니다. 이를 위해 `onceBasic` 메서드를 호출하는 [미들웨어를 정의](/docs/12.x/middleware)하세요. `onceBasic` 메서드가 응답을 반환하지 않으면 요청은 애플리케이션의 다음 처리 단계로 계속 전달됩니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

다음으로 미들웨어를 라우트에 연결합니다.

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

애플리케이션에서 사용자를 수동으로 로그아웃하려면 `Auth` 파사드가 제공하는 `logout` 메서드를 사용하면 됩니다. 그러면 이후 요청에서는 더 이상 인증된 사용자로 처리되지 않도록 세션에서 인증 정보가 제거됩니다.

`logout` 메서드를 호출하는 것 외에도 사용자 세션을 무효화하고 [CSRF 토큰](/docs/12.x/csrf)을 다시 생성하는 것이 좋습니다. 사용자를 로그아웃한 후 일반적으로 사용자를 애플리케이션의 루트로 리디렉션합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
### 다른 장치의 세션 무효화

Laravel은 현재 사용 중인 기기의 세션은 유지한 채, 다른 기기에서 활성 상태인 사용자 세션만 무효화하고 로그아웃시키는 기능도 제공합니다. 이 기능은 사용자가 비밀번호를 변경하거나 갱신할 때, 현재 기기에서는 계속 로그인 상태를 유지하면서 다른 기기의 세션만 끊고 싶을 때 주로 사용합니다.

시작하기 전에 세션 인증이 필요한 라우트에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 포함되어 있는지 확인해야 합니다. 일반적으로는 이 미들웨어를 라우트 그룹에 배치해 애플리케이션의 여러 라우트에 한꺼번에 적용합니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [미들웨어 별칭](/docs/12.x/middleware#middleware-aliases)으로 라우트에 연결할 수 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그다음 `Auth` 파사드가 제공하는 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드를 사용하려면 사용자가 현재 비밀번호를 다시 입력해 확인해야 하므로, 애플리케이션에서도 이를 받을 수 있는 입력 폼을 제공해야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 메서드가 호출되면 사용자의 다른 세션은 완전히 무효화됩니다. 즉, 이전에 인증된 모든 가드에서 "로그아웃"됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 만들다 보면, 특정 작업을 수행하기 전에 또는 민감한 영역으로 이동시키기 전에 사용자에게 비밀번호를 다시 확인하도록 요구해야 할 때가 있습니다. Laravel은 이 과정을 쉽게 구현할 수 있도록 관련 미들웨어를 기본으로 제공합니다. 이 기능을 구현하려면 두 개의 라우트를 정의해야 합니다. 하나는 비밀번호 확인을 요청하는 뷰를 보여주는 라우트이고, 다른 하나는 입력한 비밀번호를 검증한 뒤 사용자를 원래 의도한 위치로 리디렉션하는 라우트입니다.

> [!NOTE]
> 다음 문서에서는 Laravel의 비밀번호 확인 기능과 직접 통합하는 방법을 설명합니다. 그러나 더 빨리 시작하고 싶다면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)에 이 기능에 대한 지원이 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
### 구성

비밀번호를 한 번 확인하면 이후 3시간 동안은 다시 비밀번호를 묻지 않습니다. 이 시간은 애플리케이션의 `config/auth.php` 설정 파일에서 `password_timeout` 값을 변경해 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 양식

먼저, 사용자에게 비밀번호 확인을 요청하는 뷰를 표시하도록 라우트를 정의합니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

예상할 수 있듯이, 이 라우트가 반환하는 뷰에는 `password` 필드를 포함한 폼이 있어야 합니다. 또한 사용자가 보호된 영역으로 들어가려는 중이므로 비밀번호 확인이 필요하다는 안내 문구를 뷰에 함께 표시하면 됩니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인

다음으로 "비밀번호 확인" 뷰의 폼 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증하고 사용자를 원래 의도한 위치로 리디렉션하는 역할을 합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

계속하기 전에 이 라우트가 하는 일을 조금 더 자세히 살펴보겠습니다. 먼저 요청의 `password` 필드 값이 현재 인증된 사용자의 비밀번호와 실제로 일치하는지 확인합니다. 비밀번호가 유효하면, 사용자가 비밀번호 확인을 마쳤다는 사실을 Laravel 세션에 기록해야 합니다. `passwordConfirmed` 메서드는 사용자가 마지막으로 비밀번호를 확인한 시점을 나타내는 타임스탬프를 세션에 저장합니다. 마지막으로 사용자를 원래 가려던 목적지로 리디렉션합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

최근에 비밀번호를 확인한 사용자만 접근할 수 있어야 하는 라우트에는 `password.confirm` 미들웨어를 할당해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자가 비밀번호를 확인한 뒤 원래 가려던 위치로 돌아갈 수 있도록 세션에 의도한 목적지를 자동으로 저장합니다. 목적지를 저장한 뒤에는 사용자를 `password.confirm` [이름 있는 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다.

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 사용자 지정 Guard 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 사용하면 직접 인증 guard를 정의할 수 있습니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers) 안에서 호출해야 합니다. Laravel은 기본으로 `AppServiceProvider`를 제공하므로 여기에 코드를 추가하면 됩니다.

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

위 예제에서 보듯, `extend` 메서드에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현을 반환해야 합니다. 이 인터페이스에는 사용자 지정 guard를 만들 때 구현해야 할 메서드가 정의되어 있습니다. guard를 정의한 뒤에는 `auth.php` 설정 파일의 `guards` 설정에서 이를 참조할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 Request Guard

사용자 지정 HTTP 요청 기반 인증 시스템을 구현하는 가장 간단한 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 사용하면 하나의 클로저로 인증 과정을 빠르게 정의할 수 있습니다.

시작하려면 애플리케이션의 `AppServiceProvider` `boot` 메서드 안에서 `Auth::viaRequest` 메서드를 호출하세요. 첫 번째 인수는 인증 드라이버 이름이며, 사용자 지정 guard를 설명하는 임의의 문자열이면 됩니다. 두 번째 인수는 들어오는 HTTP 요청을 받아 사용자 인스턴스를 반환하는 클로저이며, 인증에 실패하면 `null`을 반환해야 합니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

사용자 지정 인증 드라이버를 정의한 뒤에는 `auth.php` 설정 파일의 `guards` 항목에서 해당 드라이버를 사용할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

마지막으로 인증 미들웨어를 라우트에 적용할 때 이 guard를 참조하면 됩니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 사용자 지정 User Provider 추가 (Adding Custom User Providers)

사용자 정보를 저장할 때 전통적인 관계형 데이터베이스를 사용하지 않는다면, 자체 인증 user provider를 사용하도록 Laravel을 확장해야 합니다. 사용자 지정 user provider를 정의하려면 `Auth` 파사드의 `provider` 메서드를 사용합니다. 이때 등록하는 콜백은 `Illuminate\Contracts\Auth\UserProvider` 구현을 반환해야 합니다.

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

`provider` 메서드로 provider를 등록한 뒤에는 `auth.php` 설정 파일에서 새 user provider를 사용하도록 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 `provider`를 정의합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로 `guards` 설정에서 이 provider를 참조하면 됩니다.

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### User Provider 계약

`Illuminate\Contracts\Auth\UserProvider` 구현은 MySQL, MongoDB 같은 영구 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현을 가져오는 역할을 합니다. 이 두 인터페이스 덕분에 Laravel의 인증 메커니즘은 사용자 데이터가 어떻게 저장되는지, 인증된 사용자를 어떤 클래스가 표현하는지와 관계없이 일관되게 동작할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약을 살펴보겠습니다.

```php
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

`retrieveById` 메서드는 일반적으로 MySQL 데이터베이스의 자동 증가 ID처럼 사용자를 나타내는 키를 받습니다. 이 메서드는 해당 ID와 일치하는 `Authenticatable` 구현을 조회해 반환해야 합니다.

`retrieveByToken` 메서드는 일반적으로 `remember_token` 같은 데이터베이스 컬럼에 저장된 고유한 `$identifier`와 "기억하기" `$token`을 사용해 사용자를 조회합니다. 앞선 메서드와 마찬가지로, 이 메서드도 일치하는 토큰 값을 가진 `Authenticatable` 구현을 반환해야 합니다.

`updateRememberToken` 메서드는 `$user` 인스턴스의 `remember_token` 값을 새로운 `$token`으로 갱신합니다. "기억하기" 인증이 성공했거나 사용자가 로그아웃할 때는 새로운 토큰이 사용자에게 할당됩니다.

`retrieveByCredentials` 메서드는 애플리케이션 인증 시 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받습니다. 이 메서드는 해당 자격 증명과 일치하는 사용자를 기본 영구 저장소에서 조회해야 합니다. 일반적으로는 `$credentials['username']` 값과 일치하는 "사용자 이름"을 기준으로 `where` 조건을 추가해 사용자 레코드를 찾습니다. 이 메서드는 `Authenticatable` 구현을 반환해야 합니다. **이 메서드에서 비밀번호 검증이나 인증 자체를 시도해서는 안 됩니다.**

`validateCredentials` 메서드는 사용자를 인증하기 위해 주어진 `$user`와 `$credentials`를 비교해야 합니다. 예를 들어 이 메서드는 일반적으로 `Hash::check` 메서드를 사용해 `$user->getAuthPassword()` 값과 `$credentials['password']` 값을 비교합니다. 반환값은 비밀번호가 유효한지를 나타내는 `true` 또는 `false`여야 합니다.

`rehashPasswordIfRequired` 메서드는 필요하고 지원되는 경우 지정된 `$user`의 비밀번호를 다시 해시해야 합니다. 예를 들어 이 메서드는 일반적으로 `Hash::needsRehash` 메서드를 사용해 `$credentials['password']` 값을 다시 해시해야 하는지 판단합니다. 다시 해시가 필요하면 `Hash::make` 메서드로 비밀번호를 새로 해시하고, 기본 영구 저장소에 있는 사용자 레코드도 함께 갱신해야 합니다.

<a name="the-authenticatable-contract"></a>
### 인증 가능한 계약

이제 `UserProvider`의 각 메서드를 살펴봤으니 `Authenticatable` 계약을 보겠습니다. user provider는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스를 구현한 객체를 반환해야 합니다.

```php
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

이 인터페이스는 비교적 단순합니다. `getAuthIdentifierName` 메서드는 사용자의 "기본 키" 컬럼 이름을 반환해야 하고, `getAuthIdentifier` 메서드는 사용자의 "기본 키" 값을 반환해야 합니다. MySQL 백엔드를 사용한다면 대개 사용자 레코드에 할당된 자동 증가 기본 키가 여기에 해당합니다. `getAuthPasswordName` 메서드는 사용자 비밀번호 컬럼의 이름을 반환해야 하며, `getAuthPassword` 메서드는 해시된 비밀번호 값을 반환해야 합니다.

이 인터페이스를 사용하면 어떤 ORM이나 저장소 추상화 계층을 사용하든 인증 시스템이 모든 "사용자" 클래스에서 동작할 수 있습니다. 기본적으로 Laravel에는 `app/Models` 디렉터리에 이 인터페이스를 구현한 `App\Models\User` 클래스가 포함되어 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt 해시의 "작업 요소"는 애플리케이션의 `config/hashing.php` 구성 파일 또는 `BCRYPT_ROUNDS` 환경 변수를 통해 조정할 수 있습니다.

일반적으로 bcrypt 작업 계수는 CPU나 GPU의 처리 성능이 향상됨에 따라 시간이 지나면서 높여야 합니다. 애플리케이션의 bcrypt 작업 계수를 늘리면, 사용자가 Laravel 스타터 키트를 통해 로그인할 때나 `attempt` 메서드로 [사용자를 수동 인증](#authenticating-users)할 때 Laravel이 사용자 비밀번호를 자동으로 다시 해시합니다.

대부분의 경우 자동 비밀번호 재해싱이 애플리케이션 동작에 문제를 일으키지는 않습니다. 하지만 필요하다면 `hashing` 설정 파일을 게시한 뒤 이 동작을 비활성화할 수 있습니다.

```shell
php artisan config:publish hashing
```

구성 파일이 게시되면 `rehash_on_login` 구성 값을 `false`로 설정할 수 있습니다.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 디스패치합니다. 다음 이벤트에 대해 [리스너를 정의](/docs/12.x/events)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름 |
| --------------------------------- |
| `Illuminate\Auth\Events\Registered` |
| `Illuminate\Auth\Events\Attempting` |
| `Illuminate\Auth\Events\Authenticated` |
| `Illuminate\Auth\Events\Login` |
| `Illuminate\Auth\Events\Failed` |
| `Illuminate\Auth\Events\Validated` |
| `Illuminate\Auth\Events\Verified` |
| `Illuminate\Auth\Events\Logout` |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout` |
| `Illuminate\Auth\Events\Lockout` |
| `Illuminate\Auth\Events\PasswordReset` |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>
