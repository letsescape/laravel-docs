# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 조회](#retrieving-the-authenticated-user)
    - [라우트 보호](#protecting-routes)
    - [로그인 제한(Throttling)](#login-throttling)
- [사용자 수동 인증](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방법](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [무상태(Stateless) HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기에서의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 기반 요청 가드](#closure-request-guards)
- [커스텀 사용자 공급자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/master/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션에서는 사용자가 애플리케이션에 인증(authenticate)하여 "로그인"할 수 있는 방법을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 것은 복잡할 수 있으며, 때로는 보안상 위험을 초래할 수도 있습니다. 이러한 이유로 Laravel은 빠르고, 안전하며, 쉽게 인증 기능을 구현할 수 있도록 필요한 도구들을 제공합니다.

Laravel의 인증 기능은 기본적으로 "가드(guards)"와 "공급자(providers)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 사용하여 상태를 관리하는 `session` 가드가 기본으로 제공됩니다.

공급자(provider)는 사용자를 영속 저장소(데이터베이스 등)에서 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/master/eloquent)와 데이터베이스 쿼리 빌더를 이용해 사용자를 조회하는 방법을 지원하지만, 필요한 경우 애플리케이션에 맞춰 추가 공급자를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 설정 파일(`config/auth.php`)은 여러 가지 인증 서비스 동작을 세밀하게 조정할 수 있도록 잘 문서화된 여러 옵션을 포함하고 있습니다.

> [!NOTE]
> 가드와 공급자는 "역할(roles)"이나 "권한(permissions)"과 혼동해서는 안 됩니다. 권한을 통해 사용자 행위 인가(authorize)에 대해 자세히 알고 싶다면 [인가(authorization)](/docs/master/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
### 스타터 키트 (Starter Kits)

빠르게 시작하고 싶으신가요? [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 신규 Laravel 애플리케이션에 설치하세요. 데이터베이스 마이그레이션 이후, 브라우저로 `/register`나 애플리케이션에 할당된 다른 URL에 접속하면 됩니다. 스타터 키트가 전체 인증 시스템의 스캐폴딩(기본 구조 설정)을 자동으로 처리해줍니다!

**최종적으로 스타터 키트를 사용하지 않더라도, [스타터 키트](/docs/master/starter-kits)를 설치하는 과정은 실제 Laravel 프로젝트에서 인증 기능 전체 구현 방식을 배우는 아주 좋은 기회가 될 수 있습니다.** Laravel 스타터 키트에는 인증 컨트롤러, 라우트, 뷰 파일이 모두 포함되어 있으므로, 이들의 코드를 살펴보면 Laravel 인증 기능 구현 방식을 자세히 익힐 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항 (Database Considerations)

Laravel에는 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/master/eloquent)이 포함되어 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 공급자를 사용할 수 있습니다. 만약 MongoDB를 사용하는 경우라면, MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델의 데이터베이스 스키마를 작성할 때는 비밀번호 컬럼이 최소 60자 이상이 되도록 해야 합니다. 참고로, 신규 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이보다 큰 길이의 컬럼을 생성합니다.

또한, `users`(또는 동일한 역할을 하는) 테이블에 100자 길이의 nullable(널 허용), string 타입의 `remember_token` 컬럼이 포함되어 있는지 반드시 확인해야 합니다. 이 컬럼은 사용자가 로그인 시 "자동 로그인(remember me)" 옵션을 선택했을 때 토큰을 저장하는 용도로 활용됩니다. 역시 Laravel 신규 애플리케이션의 기본 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요 (Ecosystem Overview)

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 앞으로 진행하기 전에, Laravel의 전반적인 인증 에코시스템을 요약해보고 각각의 패키지가 어떤 목적으로 사용되는지 알아봅니다.

먼저 인증이 어떻게 동작하는지 생각해봅시다. 웹 브라우저를 사용할 때 사용자는 로그인 폼을 통해 아이디와 패스워드를 입력합니다. 이 정보가 맞으면, 애플리케이션은 해당 사용자의 정보를 [세션](/docs/master/session)에 저장합니다. 브라우저에는 세션 ID가 담긴 쿠키가 발급되어, 추후의 요청에서도 이 세션 ID를 통해 애플리케이션이 해당 사용자를 식별할 수 있게 됩니다. 세션 쿠키를 통해 요청이 들어오면, 애플리케이션은 세션 ID로 세션 데이터를 조회하여 사용자가 인증되었음을 확인하고 "인증됨" 상태로 간주합니다.

원격 서비스가 API에 접근할 때 인증해야 하는 경우에는 웹 브라우저가 없으므로 쿠키를 주로 사용하지 않습니다. 대신, 원격 서비스가 매 요청마다 API 토큰을 전달하고, 애플리케이션은 이 토큰이 유효한지(즉, 올바른 사용자의 토큰과 일치하는지) 확인하여 요청을 인증 처리할 수 있습니다.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel의 내장 브라우저 인증 서비스

Laravel은 인증 및 세션 서비스를 내장하고 있으며, 주로 `Auth` 및 `Session` 파사드를 통해 접근합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명(credential) 검증 및 로그인 처리를 위한 메서드를 제공하며, 인증 정보를 세션에 자동 저장하고, 세션 쿠키를 발급합니다. 이러한 서비스 사용 방법은 이 문서에서 다룹니다.

**애플리케이션 스타터 키트**

이 문서에서 설명하는 대로 인증 서비스를 직접 다뤄 애플리케이션만의 인증 레이어를 구축할 수도 있지만, 보다 빠른 시작을 돕기 위해 전체 인증 레이어를 현대적 구조로 견고하게 스캐폴딩하는 [무료 스타터 키트](/docs/master/starter-kits)를 제공합니다.

<a name="laravels-api-authentication-services"></a>
#### Laravel의 API 인증 서비스

Laravel은 API 토큰을 관리하고, 토큰을 통해 들어오는 API 요청을 인증하는 데 도움이 되는 두 가지 추가 패키지 [Passport](/docs/master/passport)와 [Sanctum](/docs/master/sanctum)을 제공합니다. 참고로, 이 라이브러리들과 Laravel의 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 초점을 맞추고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 초점을 둡니다. 많은 애플리케이션이, 내부용(예: 브라우저)에는 내장 인증을, 외부 API에는 별도의 API 인증 패키지를 병행하여 사용합니다.

**Passport**

Passport는 OAuth2 인증 공급자로, 다양한 OAuth2 "grant type(인증 유형)"을 제공해 여러 종류의 토큰을 발급할 수 있습니다. 전반적으로 Passport는 강력하고 복잡한 API 인증 패키지입니다. 하지만 대부분의 애플리케이션은 OAuth2 규격이 제공하는 복잡한 기능까지는 필요하지 않으며, 이러한 복잡함이 개발자와 사용자 모두에게 혼란을 주기도 합니다. 특히 SPA나 모바일 애플리케이션을 Passport 같은 OAuth2 인증 공급자와 연결할 때 헷갈릴 수 있습니다.

**Sanctum**

OAuth2의 복잡함과 개발자 혼란을 줄이기 위해, 우리는 더욱 단순하고 직관적인 인증 패키지를 만들기로 했고, 그 결과물이 [Laravel Sanctum](/docs/master/sanctum)입니다. Sanctum은 브라우저에서 발생하는 1차 요청과 토큰을 통한 API 요청 모두를 처리할 수 있어, API와 1차 웹 UI, 혹은 백엔드와 분리된 SPA 또는 모바일 클라이언트까지 함께 지원하는 것이 목적입니다.

Laravel Sanctum은 웹/ API 인증을 동시에 처리할 수 있는 하이브리드 인증 패키지입니다. Sanctum 기반 애플리케이션은 요청을 받으면, 세션 쿠키가 인증된 세션을 참조하는지 먼저 확인합니다(내장 인증 서비스 호출). 세션 쿠키로 인증되지 않았다면, API 토큰이 있는지 검사하고, API 토큰이 있으면 해당 토큰으로 인증합니다. 이 과정에 대해서는 Sanctum의 ["how it works"](docs/master/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
#### 요약 및 스택 선택(Summary and Choosing Your Stack)

요약하자면, 애플리케이션이 브라우저에서 접근되고, 모놀리식 Laravel 애플리케이션으로 개발하는 경우, Laravel의 내장 인증 서비스를 사용하면 됩니다.

또한, 써드파티에서 사용할 API를 제공하는 경우에는 API 토큰 인증을 위해 [Passport](/docs/master/passport) 또는 [Sanctum](/docs/master/sanctum) 중 선택하게 됩니다. 일반적으로는 Sanctum이 가장 간단하고 완벽한 솔루션이므로 선호됩니다. Sanctum은 "scope(스코프)"나 "ability(권한)" 지원 등, API 인증/SPA 인증/모바일 인증을 하나로 처리합니다.

만약 Laravel 백엔드를 사용하는 싱글 페이지 애플리케이션(SPA)을 만든다면 [Laravel Sanctum](/docs/master/sanctum)을 사용해야 합니다. 이 경우, [인증 라우트를 직접 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/master/fortify)를 헤드리스 인증(뷰 없이 백엔드 인증 기능만 제공) 백엔드 서비스로 활용할 수 있습니다.

Passpport는 OAuth2 사양의 모든 기능이 반드시 필요한 경우에만 선택해야 합니다.

마지막으로 빠르게 시작하고 싶다면, [애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용해 Laravel 내장 인증 서비스 기반의 새로운 프로젝트를 만들어보는 것이 좋습니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 절에서는 Laravel [애플리케이션 스타터 키트](/docs/master/starter-kits)로 사용자 인증을 구현하는 방법을 다룹니다. (UI 스캐폴딩 포함) 만약 인증 시스템과 직접 통합하고 싶다면, [사용자 수동 인증](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치 (Install a Starter Kit)

먼저, [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 설치해야 합니다. 스타터 키트는 인증이 포함된 아름답게 디자인된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 조회 (Retrieving the Authenticated User)

스타터 키트로 애플리케이션을 생성하고 사용자가 회원가입 및 인증이 가능해진 이후에는, 현재 인증된 사용자에 접근해야 할 일이 많습니다. 요청을 처리하는 동안에는 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

또는, 사용자가 인증된 이후에는 컨트롤러에서 `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자를 곧바로 얻을 수 있습니다. 타입힌트된 클래스를 컨트롤러 메서드에 넣으면, Laravel이 자동으로 주입합니다. `Illuminate\Http\Request`를 타입힌트 하여, 요청의 `user` 메서드를 통해 인증 사용자에 접근할 수 있습니다:

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
#### 현재 사용자가 인증되었는지 확인하기

들어온 HTTP 요청의 사용자가 인증되었는지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증된 경우 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드로 인증 여부를 직접 확인할 수도 있지만, 일반적으로 미들웨어를 사용하여 특정 라우트/컨트롤러 접근 전 인증 여부를 검증하는 것이 표준적입니다. 자세한 내용은 [라우트 보호](/docs/master/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

[라우트 미들웨어](/docs/master/middleware)를 사용하여 인증된 사용자만 특정 라우트에 접근할 수 있도록 할 수 있습니다. Laravel은 `auth` 미들웨어를 기본 제공하며, 이는 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [미들웨어 별칭](/docs/master/middleware#middleware-aliases)입니다. Laravel 내부에 이미 기본 등록되어 있으므로, 라우트에 그냥 붙여주면 됩니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리다이렉트

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [이름이 지정된 라우트](/docs/master/routing#named-routes)로 리다이렉트합니다. 이 동작을 변경하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리다이렉트

`guest` 미들웨어가 인증된 사용자를 감지하면, 해당 사용자를 `dashboard` 또는 `home` 이름이 지정된 라우트로 리다이렉트합니다. 이 동작을 변경하려면, `bootstrap/app.php` 파일에서 `redirectUsersTo` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
#### 가드 지정하기

`auth` 미들웨어를 라우트에 적용할 때, 어떤 "가드"를 사용할 것인지 지정할 수도 있습니다. 지정한 가드명은 `auth.php` 설정 파일의 `guards` 배열의 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 제한(Throttling) (Login Throttling)

[애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 Rate Limiting이 적용됩니다. 기본적으로, 사용자가 일정 횟수 이상 잘못된 인증 정보를 입력하면 로그인은 1분 동안 차단됩니다. 이 제한은 사용자별 이메일/아이디와 IP 주소에 대해 고유하게 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에서도 Rate Limiting을 적용하고 싶다면 [Rate Limiting 문서](/docs/master/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증 (Manually Authenticating Users)

[애플리케이션 스타터 키트](/docs/master/starter-kits)가 제공하는 인증 스캐폴딩을 반드시 사용해야 하는 것은 아닙니다. 스캐폴딩을 사용하지 않기로 했다면, Laravel의 인증 클래스를 직접 사용하여 사용자 인증을 처리하면 됩니다. 걱정 마세요, 아주 간단합니다!

Laravel의 인증 서비스를 사용하려면 `Auth` [파사드](/docs/master/facades)를 임포트해야 합니다. 이제 `attempt` 메서드를 살펴봅시다. 이 메서드는 보통 "로그인" 폼에서 인증 시도를 처리할 때 사용됩니다. 인증에 성공하면, [세션](/docs/master/session) 고정 공격(session fixation)을 방지하기 위해 반드시 사용자의 세션을 재생성해야 합니다:

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

`attempt` 메서드는 첫 번째 인수로 키-값 쌍의 배열을 받습니다. 이 배열의 값이 데이터베이스에서 사용자를 조회하는 데 쓰입니다. 위 예시에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자가 조회되면, 데이터베이스에 저장된 해시된 비밀번호와 입력된 비밀번호가 비교됩니다. 입력값의 비밀번호는 해싱하지 않아도 됩니다. 프레임워크가 내부적으로 자동 해싱 후 비교합니다. 두 해시가 일치하면 인증 세션이 시작됩니다.

Laravel 인증 서비스는, 인증 가드의 "provider" 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본 `config/auth.php`에서는 Eloquent 사용자 공급자를 지정하고, 사용자 조회 모델로 `App\Models\User`를 사용합니다. 필요에 따라 이 값을 설정 파일에서 변경할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`intended` 메서드는 인증 미들웨어에서 막혔다가 다시 인증 성공 후, 사용자가 원래 접근하려고 했던 URL로 즉시 리다이렉트할 수 있도록 해줍니다. 타겟 경로가 없는 경우, 대체 경로도 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
#### 추가 조건 지정하기

원한다면, 이메일과 비밀번호 외에 추가 조건을 `attempt` 메서드의 배열에 넣어 더욱 정교하게 인증 쿼리를 만들 수 있습니다. 예를 들어, 사용자가 "active" 상태인지 검사할 수 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

더 복잡한 쿼리 조건이 필요할 경우, 배열에 클로저를 넣어 직접 쿼리를 조작할 수도 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아 원하는 조건을 추가할 수 있게 해줍니다:

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
> 예시에서는 컬럼명을 `email`로 썼지만, 반드시 이 컬럼명을 써야 하는 것은 아닙니다. 데이터베이스에서 "사용자명" 역할로 사용하는 컬럼명을 적용하면 됩니다.

보다 광범위한 사용자 검증이 필요하다면, 두 번째 인수로 클로저를 받는 `attemptWhen` 메서드를 사용할 수 있습니다. 이 클로저는 잠재적 사용자 객체를 전달받고, 인증 허용 여부에 따라 `true` 또는 `false`를 반환해야 합니다:

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
#### 특정 가드 인스턴스 사용하기

`Auth` 파사드의 `guard` 메서드를 통해 사용자 인증 시 사용하고자 하는 가드 인스턴스를 지정할 수 있습니다. 이를 활용하면 애플리케이션의 각 영역을 완전히 별도의 authenticatable 모델 또는 별도의 사용자 테이블로 관리할 수 있습니다.

전달하는 가드명은 `auth.php` 설정 파일에 설정된 것 중 하나여야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기 (Remembering Users)

많은 웹 애플리케이션에서는 로그인 폼에 "자동 로그인(remember me)" 체크박스를 제공합니다. 이 기능을 구현하려면 `attempt` 메서드의 두 번째 인수로 boolean 값을 전달하면 됩니다.

이 값이 `true`이면, 사용자는 로그아웃할 때까지 또는 수동으로 세션을 만료시킬 때까지 인증 상태가 유지됩니다. `users` 테이블에는 string 타입의 `remember_token` 컬럼이 반드시 존재해야 합니다(스타터 키트 기본 마이그레이션에 이미 포함됨):

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

"자동 로그인" 기능이 활성화되어 있다면, 현재 인증된 사용자가 "자동 로그인" 쿠키로 인증되었는지 여부를 `viaRemember` 메서드로 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방법 (Other Authentication Methods)

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스를 직접 인증하기

이미 사용자 인스턴스를 가지고 있고 이를 인증된 사용자로 세팅하고자 한다면, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하세요. 이때 전달하는 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/master/contracts)의 구현체여야 합니다. Laravel의 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 이 방식은 회원가입 직후 등 이미 사용자 인스턴스가 유효할 때 특히 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

두 번째 인수로 boolean 값을 전달해 "자동 로그인(remember me)" 여부도 지정할 수 있습니다. 이 값이 `true`이면 사용자는 수동 로그아웃 전까지 인증 상태가 유지됩니다:

```php
Auth::login($user, $remember = true);
```

필요하다면, `login` 호출 전에 사용할 인증 가드를 미리 지정할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
#### 사용자의 ID로 인증하기

사용자 레코드의 기본 키(Primary Key)를 이용해 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증하고자 하는 사용자의 기본 키를 인수로 받습니다:

```php
Auth::loginUsingId(1);
```

`loginUsingId` 메서드의 `remember` 인수에 boolean 값을 전달하면 "자동 로그인" 여부도 같이 지정할 수 있습니다:

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
#### 1회성(once) 인증하기

`once` 메서드를 이용하면 지속적인 세션이나 쿠키 없이 한 번의 요청에 대해 사용자 인증을 처리할 수 있습니다. 이때는 `Login` 이벤트가 발생하지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 전용 "로그인" 페이지를 따로 만들지 않고 간단하게 사용자 인증을 처리할 수 있습니다. 시작하려면, `auth.basic` [미들웨어](/docs/master/middleware)를 라우트에 붙이기만 하면 됩니다. 이 미들웨어는 Laravel에 기본으로 포함되어 있어 별도로 등록할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

미들웨어가 라우트에 적용되면, 해당 라우트에 브라우저로 접근할 때 인증을 위한 대화창이 자동으로 나타납니다. 기본적으로, `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼이 사용자명(username)이라고 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI 사용 시 참고 사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache를 조합해 Laravel을 서비스하는 경우, HTTP Basic 인증이 정상 동작하지 않을 수 있습니다. 이럴 때는 `.htaccess` 파일에 아래 설정을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### 무상태(Stateless) HTTP Basic 인증

세션에 사용자 식별자 쿠키를 저장하지 않고 HTTP Basic 인증만 사용하고 싶을 때도 있습니다. 주로 API에서 HTTP 인증으로 요청을 인증하고자 할 때 유용합니다. 이를 위해서는 [미들웨어 정의](/docs/master/middleware) 후 그 안에서 `onceBasic` 메서드를 호출하면 됩니다. `onceBasic`에서 응답이 반환되지 않았을 경우, 다음 미들웨어로 요청이 전달됩니다:

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

다음으로, 해당 미들웨어를 라우트에 적용하세요:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃시키려면, `Auth` 파사드가 제공하는 `logout` 메서드를 사용하면 됩니다. 이 메서드는 사용자의 세션에서 인증 정보를 제거해 이후 요청에서 인증이 되지 않게 만듭니다.

추가로, `logout` 호출 이후에는 사용자의 세션을 무효화 하고, [CSRF 토큰](/docs/master/csrf)을 반드시 재생성해주어야 합니다. 로그아웃 후에는 보통 애플리케이션 루트로 리다이렉트합니다:

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
### 다른 기기에서의 세션 무효화 (Invalidating Sessions on Other Devices)

Laravel은 한 사용자가 여러 기기에서 로그인한 경우, 현재 사용 중인 기기를 제외하고 다른 기기에서의 세션(로그인 대부분)을 무효화하는 기능도 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경하거나 업데이트할 때 다른 기기에서의 세션을 만료시키는 용도로 사용됩니다.

이 기능을 사용하기 전에는 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 해당 라우트에 등록되어 있는지 확인해야 합니다. 일반적으로 이 미들웨어는 라우트 그룹에 붙여서 애플리케이션의 대부분 라우트에 적용합니다. 이 미들웨어는 `auth.session` [미들웨어 별칭](/docs/master/middleware#middleware-aliases)으로 라우트에 연결할 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

이제, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자의 현재 비밀번호 확인이 필요하며, 사용자는 입력 폼을 통해 비밀번호를 직접 입력해야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 호출 시 사용자의 다른 세션들은 모두 완전히 무효화되며, 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션을 만들다 보면, 사용자가 중요한 동작을 수행하기 전에 또는 민감한 영역으로 이동하기 전에 반드시 비밀번호를 다시 입력하도록 요구해야 할 때가 있습니다. 이러한 요구를 간편하게 처리할 수 있도록 Laravel은 내장 미들웨어를 제공합니다. 이를 구현하려면, 사용자의 비밀번호 확인을 요청하는 뷰를 보여주는 라우트와, 실제로 비밀번호가 유효한지 검증한 뒤 사용자를 원래 위치로 보내주는 라우트 두 개를 정의해야 합니다.

> [!NOTE]
> 아래 설명은 Laravel의 비밀번호 확인 기능을 직접 통합하는 방법을 다룹니다. 좀 더 빠르게 시작하고 싶다면 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하세요!

<a name="password-confirmation-configuration"></a>
### 설정 (Configuration)

사용자가 비밀번호를 확인한 뒤에는 3시간 동안은 다시 확인을 요구하지 않습니다. 이 재확인까지의 시간은 애플리케이션의 `config/auth.php` 설정 파일의 `password_timeout` 값으로 변경할 수 있습니다.

<a name="password-confirmation-routing"></a>
### 라우팅 (Routing)

<a name="the-password-confirmation-form"></a>
#### 비밀번호 확인 폼

먼저, 사용자에게 비밀번호를 확인하도록 요청하는 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트에서 반환되는 뷰에는 반드시 `password` 필드를 포함하는 폼이 있어야 합니다. 사용자가 애플리케이션의 보호 구역에 진입하기 위해 비밀번호 확인이 필요함을 알리는 설명도 부가할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인 처리

다음으로, 위 폼에서 submit된 요청을 처리할 라우트를 정의합니다. 이 라우트가 비밀번호의 유효성을 검사하고, 사용자를 원래 목적지로 리다이렉트하는 역할을 담당합니다:

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

위 코드를 보면 먼저 사용자가 입력한 비밀번호가 실제 현재 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 입력값이 유효하면, Laravel 세션에 사용자가 비밀번호를 확인했다는 정보를 저장해야 합니다. `passwordConfirmed` 메서드는 비밀번호 확인 시각을 세션에 기록하며, 이 정보를 통해 Laravel은 사용자가 최근에 비밀번호를 확인했는지 판단합니다. 마지막으로 사용자를 원래 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
### 라우트 보호

비밀번호 재확인이 필요한 중요 동작을 수행하는 라우트에는 반드시 `password.confirm` 미들웨어를 할당하세요. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자의 '이동 예정지'를 세션에 저장해, 비밀번호 재입력 후 그 위치로 자동 리다이렉트하게 해줍니다. 세션에 이동 예정지를 저장한 뒤, 미들웨어는 사용자를 `password.confirm` [이름이 지정된 라우트](/docs/master/routing#named-routes)로 리다이렉트합니다:

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
## 커스텀 가드 추가 (Adding Custom Guards)

`Auth` 파사드의 `extend` 메서드를 이용해 직접 인증 가드를 정의할 수 있습니다. 이 코드는 [서비스 프로바이더](/docs/master/providers) 내부에 위치해야 합니다. Laravel은 기본적으로 `AppServiceProvider`를 제공하므로, 그곳에 코드를 추가하면 됩니다:

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

위 예시처럼, `extend` 메서드에 전달된 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스에 따라 여러 메서드를 구현해야 하며, 커스텀 가드 작성이 마무리되면, `auth.php` 설정 파일의 `guards` 설정에서 사용할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 기반 요청 가드 (Closure Request Guards)

HTTP 요청 기반의 커스텀 인증 시스템을 가장 빠르게 구현하는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드로 하나의 클로저만으로 인증 로직을 정의할 수 있습니다.

먼저, 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드 내에 `Auth::viaRequest`를 호출하세요. 이 메서드는 첫 번째 인수로 인증 드라이버 이름(아무 문자열 가능), 두 번째 인수로 HTTP 요청을 받아 사용자 인스턴스(또는 인증 실패 시 `null`)를 반환하는 클로저를 받습니다:

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

커스텀 인증 드라이버를 등록한 후에는, 해당 이름을 `auth.php`의 `guards` 구성에서 사용할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

이제 해당 가드를 라우트에 인증 미들웨어로 적용할 수 있습니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 공급자 추가 (Adding Custom User Providers)

전통적인 관계형 데이터베이스가 아닌 저장소에 사용자를 저장한다면, Laravel의 인증 시스템을 확장하여 직접 사용자 공급자를 만들어야 합니다. `Auth` 파사드의 `provider` 메서드로 커스텀 사용자 공급자 등록이 가능합니다. 이때 반환값은 반드시 `Illuminate\Contracts\Auth\UserProvider` 구현체여야 합니다:

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

`provider` 메서드로 등록한 후에는, 새 공급자를 `auth.php`에 다음과 같이 적용할 수 있습니다. 먼저, 새로운 드라이버를 사용하는 `provider`를 정의합니다:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

그 다음, 이 공급자를 `guards` 설정에서 참조할 수 있습니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
### User Provider 계약 (The User Provider Contract)

`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등과 같은 영속 저장소에서 조회하는 역할을 합니다. 이 두 인터페이스 덕분에, 사용자 데이터 저장소/클래스 구조에 상관없이 Laravel 인증이 동일하게 작동할 수 있습니다.

아래는 `Illuminate\Contracts\Auth\UserProvider` 계약의 메서드 목록입니다:

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

- `retrieveById`: 보통 MySQL auto-increment ID 등 사용자의 주요 식별 key를 받아, 해당 ID에 맞는 Authenticatable 인스턴스를 반환합니다.
- `retrieveByToken`: 고유 `$identifier`와 "remember me" `$token`(주로 `remember_token` 컬럼 사용)으로 사용자를 조회하고, 해당 Authenticatable 인스턴스를 반환합니다.
- `updateRememberToken`: 사용자의 `remember_token`을 새 토큰으로 갱신합니다. "자동 로그인" 성공 시점이나 로그아웃 시 새로운 토큰이 할당됩니다.
- `retrieveByCredentials`: `Auth::attempt` 호출 시 받은 credential 배열로 사용자를 조회합니다. 일반적으로 username 등 조건으로 조회된 사용자 Authenticatable 인스턴스를 반환하며 **여기서는 비밀번호 검증을 하지 않습니다.**
- `validateCredentials`: 주어진 `$user`와 `$credentials`를 비교해 인증 여부를 판단합니다. 보통 `Hash::check`로 `user->getAuthPassword()`와 `$credentials['password']`를 비교하고, 결과를 `true`/`false`로 반환합니다.
- `rehashPasswordIfRequired`: 사용자의 비밀번호 재해싱이 필요한 경우(`Hash::needsRehash` 체크) 비밀번호를 새롭게 해시 후 저장합니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약 (The Authenticatable Contract)

`UserProvider`의 각 메서드를 살펴봤으니, 이제 `Authenticatable` 계약도 봅시다. 공급자는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials`에서 해당 인터페이스 구현체를 반환해야 합니다:

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

이 인터페이스는 심플합니다.  
- `getAuthIdentifierName`: 사용자의 "기본 키" 컬럼명을 반환합니다.
- `getAuthIdentifier`: 사용자의 실제 "기본 키" 값을 반환합니다.
- `getAuthPasswordName`: 비밀번호 컬럼명을,  
- `getAuthPassword`: 해시된 비밀번호를 반환합니다.

이 인터페이스 덕분에 인증 시스템은 ORM이나 스토리지 방식에 상관없이 모든 "user" 클래스를 사용할 수 있습니다. Laravel은 기본적으로 `app/Models` 디렉터리에 해당 인터페이스를 구현한 `App\Models\User` 클래스를 제공합니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해시 알고리즘은 bcrypt입니다. bcrypt의 "작업 인자(work factor)"는 `config/hashing.php` 설정 파일이나 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

컴퓨터 연산 능력이 좋아질수록 bcrypt 작업 인자도 시간에 따라 높여주는 것이 권장됩니다. bcrypt 인자를 높이면, 기존 사용자 비밀번호 해시가 새 인자로 자동 재해싱됩니다. 자동 재해싱은 starter kit이나 [수동 인증](#authenticating-users)의 `attempt` 메서드로 인증할 때 자동 수행됩니다.

이 동작은 기본적으로 애플리케이션에 영향을 주지 않지만, 원한다면 `hashing` 설정 파일을 발행해서(`php artisan config:publish hashing`)  
`rehash_on_login` 값을 `false`로 바꿔 비활성화할 수도 있습니다:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 프로세스 중 다양한 [이벤트](/docs/master/events)를 디스패치합니다. 아래 이벤트에 대해 [리스너를 정의](/docs/master/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                      |
| ------------------------------------------------ |
| `Illuminate\Auth\Events\Registered`              |
| `Illuminate\Auth\Events\Attempting`              |
| `Illuminate\Auth\Events\Authenticated`           |
| `Illuminate\Auth\Events\Login`                   |
| `Illuminate\Auth\Events\Failed`                  |
| `Illuminate\Auth\Events\Validated`               |
| `Illuminate\Auth\Events\Verified`                |
| `Illuminate\Auth\Events\Logout`                  |
| `Illuminate\Auth\Events\CurrentDeviceLogout`     |
| `Illuminate\Auth\Events\OtherDeviceLogout`       |
| `Illuminate\Auth\Events\Lockout`                 |
| `Illuminate\Auth\Events\PasswordReset`           |
| `Illuminate\Auth\Events\PasswordResetLinkSent`   |

</div>
