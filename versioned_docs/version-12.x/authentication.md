# 인증(Authentication)

- [소개](#introduction)
    - [스타터 키트](#starter-kits)
    - [데이터베이스 고려사항](#introduction-database-considerations)
    - [에코시스템 개요](#ecosystem-overview)
- [인증 빠른 시작](#authentication-quickstart)
    - [스타터 키트 설치](#install-a-starter-kit)
    - [인증된 사용자 정보 조회](#retrieving-the-authenticated-user)
    - [라우트 보호하기](#protecting-routes)
    - [로그인 시도 제한](#login-throttling)
- [사용자 수동 인증하기](#authenticating-users)
    - [사용자 기억하기](#remembering-users)
    - [기타 인증 방식](#other-authentication-methods)
- [HTTP Basic 인증](#http-basic-authentication)
    - [Stateless HTTP Basic 인증](#stateless-http-basic-authentication)
- [로그아웃](#logging-out)
    - [다른 기기의 세션 무효화](#invalidating-sessions-on-other-devices)
- [비밀번호 재확인](#password-confirmation)
    - [설정](#password-confirmation-configuration)
    - [라우팅](#password-confirmation-routing)
    - [라우트 보호](#password-confirmation-protecting-routes)
- [커스텀 가드 추가](#adding-custom-guards)
    - [클로저 요청 가드](#closure-request-guards)
- [커스텀 사용자 제공자 추가](#adding-custom-user-providers)
    - [User Provider 계약](#the-user-provider-contract)
    - [Authenticatable 계약](#the-authenticatable-contract)
- [자동 비밀번호 재해싱](#automatic-password-rehashing)
- [소셜 인증](/docs/12.x/socialite)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션에서는 사용자가 애플리케이션에 인증(Authentication)하고 "로그인"할 수 있는 방법을 제공합니다. 웹 애플리케이션에서 이 기능을 구현하는 것은 복잡할 수 있으며, 잠재적으로 보안적인 위험도 존재합니다. 이러한 이유로, Laravel은 인증을 빠르고, 안전하며, 쉽게 구현할 수 있도록 필요한 도구들을 제공합니다.

Laravel의 인증 기능은 기본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자가 어떻게 인증되는지 정의합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 이용하여 상태를 유지하는 `session` 가드가 기본으로 포함되어 있습니다.

프로바이더는 영속 저장소(예: 데이터베이스)에서 사용자를 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/12.x/eloquent)와 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 지원합니다. 하지만, 애플리케이션의 필요에 따라 추가적인 프로바이더를 자유롭게 정의할 수 있습니다.

애플리케이션의 인증 구성 파일은 `config/auth.php`에 위치합니다. 이 파일은 Laravel의 인증 서비스 동작을 세밀하게 조정할 수 있는 다양한 옵션들과, 각 옵션에 대한 충분한 설명을 담고 있습니다.

> [!NOTE]
> 가드(guard)와 프로바이더(provider)는 "역할(roles)"과 "권한(permissions)"과는 다릅니다. 퍼미션 기반으로 사용자 행위를 인가(authorization)하는 방법은 [인가(authorization)](/docs/12.x/authorization) 문서를 참고하시기 바랍니다.

<a name="starter-kits"></a>
### 스타터 키트

빠르게 시작하고 싶으신가요? 새로 생성한 Laravel 애플리케이션에서 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 다른 URL에 접근하면, 스타터 키트가 인증 시스템 전체를 자동으로 구성해드립니다!

**실제 프로젝트에서 스타터 키트를 사용하지 않더라도, [스타터 키트](/docs/12.x/starter-kits)를 설치해 보는 것은 Laravel의 인증 기능 구현 방식을 익히기에 매우 좋은 학습 기회가 될 수 있습니다.** 스타터 키트에는 인증 컨트롤러, 라우트, 뷰 파일이 모두 포함되어 있으므로, 이 파일들의 코드를 참고하여 Laravel 인증 시스템을 어떻게 구현하면 되는지 직접 확인하실 수 있습니다.

<a name="introduction-database-considerations"></a>
### 데이터베이스 고려사항

기본적으로 Laravel은 `app/Models` 디렉터리에 `App\Models\User` [Eloquent 모델](/docs/12.x/eloquent)을 제공합니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. 만약 MongoDB를 사용한다면, MongoDB 공식 [Laravel 사용자 인증 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

`App\Models\User` 모델을 위한 데이터베이스 스키마를 만들 때, 비밀번호 컬럼의 길이가 최소 60자 이상인지 확인해야 합니다. 물론, 새 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션에는 이미 이보다 긴 컬럼이 생성됩니다.

또한, `users`(또는 이에 상응하는) 테이블에는 100자 길이의 nullable string 타입 `remember_token` 컬럼이 있어야 합니다. 이 컬럼은 사용자가 "로그인 상태 유지(remember me)" 옵션을 선택할 때 토큰을 저장하는 데 사용됩니다. 역시, 새 Laravel 애플리케이션의 기본 `users` 테이블 마이그레이션에 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
### 에코시스템 개요

Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기에 앞서, Laravel의 전체 인증 에코시스템을 살펴보고 각 패키지가 어떤 역할을 하는지 간략하게 알아보겠습니다.

먼저, 인증이 어떻게 동작하는지 생각해보겠습니다. 웹 브라우저를 사용할 때, 사용자는 로그인 폼에 아이디와 비밀번호를 입력합니다. 이 정보가 올바르면 애플리케이션은 인증된 사용자 정보를 [세션](/docs/12.x/session)에 저장합니다. 브라우저에는 세션 ID가 담긴 쿠키가 발급되고, 이후의 모든 요청에서는 이 세션 ID를 통해 사용자를 올바른 세션과 연관지을 수 있습니다. 세션 쿠키가 수신된 후, 애플리케이션은 세션 ID로 세션 데이터를 조회하고, 세션 내에 인증 정보가 저장되어 있음을 확인하여 해당 사용자를 "인증된 상태"로 간주합니다.

반면, 원격 서비스가 API에 접근해야 할 경우에는 브라우저가 없기 때문에 쿠키를 사용하지 않습니다. 원격 서비스는 매 요청마다 API 토큰을 함께 보내며, 애플리케이션은 이 토큰을 유효 토큰 목록과 비교하여 해당 요청이 정당한 사용자에 의한 것임을 판단하고 "인증" 처리를 합니다.

#### Laravel의 내장 브라우저 인증 서비스

Laravel은 주로 `Auth` 및 `Session` 파사드를 통해 접근할 수 있는 내장 인증 및 세션 서비스를 제공합니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 지원하며, 사용자의 자격 증명 확인 및 인증 처리용 메서드들을 제공합니다. 또한, 적절한 인증 정보를 사용자의 세션에 자동으로 저장하고 세션 쿠키를 발급합니다. 이러한 서비스의 사용법은 본 문서에서 자세히 다룹니다.

**애플리케이션 스타터 키트**

이 문서에서 다루는 것처럼, 인증 서비스를 수동으로 이용하여 직접 인증 레이어를 구축할 수도 있지만, 빠르고 쉽게 시작할 수 있도록 전체 인증 레이어에 대한 현대적이고 견고한 구조를 갖춘 [무료 스타터 키트](/docs/12.x/starter-kits)를 제공합니다.

#### Laravel의 API 인증 서비스

Laravel은 API 토큰 관리 및 토큰 기반 인증 요청 처리를 돕는 두 가지 선택적 패키지, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum)을 제공합니다. 이 라이브러리들과 Laravel 기본 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 집중하며, 기본 인증 서비스는 브라우저 쿠키 기반 인증에 집중합니다. 많은 애플리케이션에서는 두 방식을 모두 사용할 수 있습니다.

**Passport**

Passport는 OAuth2 인증 프로바이더로, 다양한 OAuth2 "grant type"을 지원해 여러 종류의 토큰을 발급할 수 있습니다. 일반적으로 API 인증을 위한 강력하고 복잡한 패키지입니다. 하지만, 대부분 애플리케이션은 OAuth2 명세에서 제공하는 복잡한 기능이 필요한 것은 아니며, 사용자는 물론 개발자에게도 혼란을 줄 수 있습니다. 특히 단일 페이지 애플리케이션(SPA)이나 모바일 애플리케이션 인증에 Passport 같은 OAuth2 기반 인증 프로바이더를 사용할 때 많은 개발자들이 혼란을 겪곤 합니다.

**Sanctum**

OAuth2의 복잡함과 개발자 혼란을 해결하기 위해, 더 단순하고 직관적인 인증 패키지를 만들고자 했습니다. 그 결과가 바로 [Laravel Sanctum](/docs/12.x/sanctum)이며, 웹 UI와 API를 동시에 제공하는 애플리케이션, 백엔드와 분리된 SPA, 모바일 앱까지 다양한 경우에 권장되는 인증 패키지입니다.

Laravel Sanctum은 웹/ API 하이브리드 인증 패키지로, 애플리케이션 전체의 인증 과정을 관리할 수 있습니다. 즉, Sanctum이 요청을 받으면 먼저 세션 쿠키가 포함되어 있는지 확인하여 인증된 세션이 존재하는지 체크합니다(이때 앞서 설명한 Laravel 기본 인증 서비스를 활용합니다). 만약 세션 쿠키로 인증되지 않았다면, 요청에 API 토큰이 있는지 검사하여 API 토큰으로 인증을 시도합니다. 이 과정의 자세한 동작 원리는 Sanctum의 ["동작 방식"](/docs/12.x/sanctum#how-it-works) 문서를 참고하시기 바랍니다.

#### 요약 및 인증 스택 선택

정리하자면, 웹 브라우저를 통해 접근하는 모놀리식 Laravel 애플리케이션이라면 Laravel의 내장 인증 서비스를 사용하면 됩니다.

외부 서비스가 이용하는 API를 제공해야 한다면, [Passport](/docs/12.x/passport)와 [Sanctum](/docs/12.x/sanctum) 중에서 API 토큰 인증 방식을 선택할 수 있습니다. 대부분의 경우, Sanctum은 API 인증, SPA 인증, 모바일 인증을 모두 지원하는 단순하고 완전한 솔루션이므로 기본적으로 Sanctum 사용을 권장합니다. 물론 "권한(Scope)"이나 "기능(Ability)" 지원도 포함됩니다.

SPA가 Laravel 백엔드에서 동작하는 경우, [Laravel Sanctum](/docs/12.x/sanctum)을 사용해야 합니다. Sanctum을 사용할 때에는 [인증 관련 라우트를 직접 구현](#authenticating-users)하거나, [Laravel Fortify](/docs/12.x/fortify)를 이용하여 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공하는 헤드리스 인증 백엔드 서비스를 사용할 수 있습니다.

어플리케이션에 OAuth2 명세의 모든 기능이 꼭 필요하다면 Passport를 선택할 수 있습니다.

빠르게 시작하고 싶다면, [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 이용하는 것이 Laravel 인증 스택을 가장 손쉽게 적용하는 방법입니다.

<a name="authentication-quickstart"></a>
## 인증 빠른 시작 (Authentication Quickstart)

> [!WARNING]
> 이 문서는 UI 스캐폴딩이 포함된 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 통한 사용자 인증 방법을 설명합니다. 인증 시스템과 직접 통합하고 싶다면, [사용자 수동 인증하기](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
### 스타터 키트 설치

먼저, [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. 스타터 키트는 인증 시스템을 손쉽게 도입할 수 있도록 아름답게 디자인된 출발점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
### 인증된 사용자 정보 조회

스타터 키트로 애플리케이션을 만들고, 사용자가 등록 및 인증할 수 있게 했다면, 현재 인증된 사용자의 정보를 활용하는 경우가 많습니다. 요청을 처리할 때는 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

또한, 사용자가 인증된 이후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. 컨트롤러 메서드에는 타입 힌트가 자동으로 주입되므로, `Illuminate\Http\Request` 오브젝트를 타입 힌트하면 `user` 메서드로 어느 컨트롤러에서나 인증된 사용자에 편리하게 접근할 수 있습니다:

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

#### 현재 사용자가 인증 상태인지 확인하기

들어오는 HTTP 요청을 수행한 사용자가 인증된 상태인지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증되어 있다면 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> 사용자가 인증 상태인지 `check` 메서드로 직접 확인할 수도 있지만, 보통은 미들웨어를 통해 사용자가 인증된 상태임을 보장합니다. 자세한 사용법은 [라우트 보호하기](/docs/12.x/authentication#protecting-routes) 문서를 확인하세요.

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/12.x/middleware)를 사용하면, 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 alias로 지정한 `auth` 미들웨어를 기본 제공하므로, 해당 미들웨어를 라우트에 바로 적용하면 됩니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 자동으로 사용자를 `login` [네임드 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

#### 인증된 사용자 리디렉션

`guest` 미들웨어가 인증된 사용자를 감지하면, 사용자를 `dashboard` 또는 `home` 네임드 라우트로 리디렉션합니다. 이 동작도 `redirectUsersTo` 메서드로 변경할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

#### 가드 지정하기

라우트에 `auth` 미들웨어를 적용할 때, 어떤 "가드"를 사용할 것인지 지정할 수 있습니다. 지정한 가드는 `auth.php` 설정 파일의 `guards` 배열 내 키와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
### 로그인 시도 제한

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 속도 제한이 적용됩니다. 여러 번 잘못된 자격 증명을 입력하면, 기본적으로 1분간 로그인 시도가 차단됩니다. 이 제한은 사용자 이름/이메일 및 IP 주소 별로 개별적으로 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에도 속도 제한을 적용하고 싶다면 [속도 제한 문서](/docs/12.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
## 사용자 수동 인증하기 (Manually Authenticating Users)

[애플리케이션 스타터 키트](/docs/12.x/starter-kits)에 포함된 인증 스캐폴딩을 반드시 사용해야 하는 것은 아닙니다. 만약 해당 스캐폴딩을 사용하지 않는다면, Laravel 인증 클래스를 직접 사용해 사용자 인증을 처리해야 합니다. 걱정하지 마세요, 매우 간단합니다!

`Auth` [파사드](/docs/12.x/facades)를 통해 Laravel의 인증 서비스에 접근할 수 있으니, 클래스 상단에 `Auth` 파사드를 import하세요. 이제 `attempt` 메서드를 살펴보겠습니다. 이 메서드는 일반적으로 애플리케이션의 "로그인" 폼 요청을 처리할 때 사용합니다. 인증에 성공하면, [세션](/docs/12.x/session)을 재생성하여 [세션 고정 공격(session fixation)](https://en.wikipedia.org/wiki/Session_fixation)을 방지하세요:

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

`attempt` 메서드는 키/값 쌍의 배열을 첫 번째 인수로 받습니다. 배열의 값들은 데이터베이스의 사용자 정보를 찾는 데 사용됩니다. 위 예시에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자가 존재하면 데이터베이스에 저장된 해시된 비밀번호와, 배열로 전달된 `password` 값을 비교합니다. 요청으로 입력받은 `password` 값은 별도로 해시할 필요 없습니다. 프레임워크가 자동으로 해시하여 데이터베이스의 값과 비교합니다. 두 해시가 일치하면 사용자의 인증 세션이 시작됩니다.

Laravel 인증 서비스는 가드(guard)의 "provider" 설정에 따라 데이터베이스에서 사용자를 조회합니다. 기본 `config/auth.php` 파일은 Eloquent 사용자 제공자를 지정하고, 사용자를 조회할 때 `App\Models\User` 모델을 사용하도록 설정되어 있습니다. 애플리케이션에 따라 해당 값들을 자유롭게 수정할 수 있습니다.

`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

`intended` 리디렉션 메서드는 인증 미들웨어에 차단되기 직전 사용자가 접근을 시도했던 URL로 리디렉션합니다. 만약 목적지가 없다면 대체 URI를 지정할 수도 있습니다.

#### 추가 조건 지정

사용자 이메일 및 비밀번호 외에도 인증 조건에 추가 쿼리 조건을 더할 수 있습니다. 단순하게 인증 조건 배열에 원하는 값을 더해 `attempt` 메서드에 전달하면 됩니다. 예를 들어, 사용자가 "활성(active)" 계정인지 확인할 수도 있습니다:

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

복잡한 쿼리 조건이 필요하다면, 자격 증명 배열에 클로저를 추가할 수 있습니다. 이 클로저는 쿼리 인스턴스를 받아, 애플리케이션에 맞는 쿼리 커스터마이징이 가능합니다:

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
> 위의 예시에서 `email`은 필수 옵션이 아니라 예시일 뿐입니다. 데이터베이스에서 "사용자 이름" 역할을 하는 컬럼명을 사용하세요.

두 번째 인수로 클로저를 전달하는 `attemptWhen` 메서드를 사용하면, 인증 전 후보 사용자를 보다 정교하게 검사할 수 있습니다. 클로저는 후보 사용자를 받아, 인증 가능 여부에 따라 `true` 또는 `false`를 반환해야 합니다:

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

#### 특정 가드 인스턴스 사용

`Auth` 파사드의 `guard` 메서드를 이용하면, 인증에 사용할 가드 인스턴스를 직접 지정할 수 있습니다. 이를 통해 애플리케이션의 각 영역에서 별도의 인증 모델 혹은 사용자 테이블을 기반으로 인증을 관리할 수 있습니다.

`guard` 메서드에 전달하는 이름은 `auth.php` 설정 파일의 guard 이름과 일치해야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션에서는 로그인 폼에 "로그인 상태 유지(remember me)" 체크박스를 제공합니다. 이 기능을 구현하려면, `attempt` 메서드의 두 번째 인수로 boolean 값을 전달하면 됩니다.

이 값이 `true`라면, Laravel은 사용자가 직접 로그아웃하기 전까지 인증 상태를 유지합니다. 이를 위해 `users` 테이블에는 문자열 타입의 `remember_token` 컬럼이 반드시 존재해야 하며, 기본 마이그레이션에는 이 컬럼이 이미 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

"로그인 상태 유지" 기능이 있다면, 현재 인증 사용자가 해당 쿠키로 인증되었는지 `viaRemember` 메서드로 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
### 기타 인증 방식

#### 사용자 인스턴스 인증

이미 존재하는 사용자 인스턴스를 현재 인증 사용자로 지정하려면, `Auth` 파사드의 `login` 메서드에 해당 인스턴스를 전달하면 됩니다. 이 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/12.x/contracts)을 구현하고 있어야 하며, 기본 `App\Models\User` 모델에는 이미 구현되어 있습니다. 이 방식은 예를 들어, 사용자가 회원가입 직후 바로 인증 처리해야 할 때 유용합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

또한, `login` 메서드의 두 번째 인수로 boolean 값을 전달하면 "로그인 상태 유지" 기능이 적용됩니다. 즉, 사용자가 명시적으로 로그아웃할 때까지 인증 세션이 유지됩니다:

```php
Auth::login($user, $remember = true);
```

필요에 따라 인증 전에 사용할 가드를 지정할 수도 있습니다:

```php
Auth::guard('admin')->login($user);
```

#### 사용자 ID로 인증

데이터베이스에서 사용자의 기본 키(primary key)로 사용자 인증을 하려면, `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증하려는 사용자의 기본 키를 인수로 받습니다:

```php
Auth::loginUsingId(1);
```

또한, `loginUsingId` 메서드의 `remember` 인수로 boolean 값을 전달하여 "로그인 상태 유지" 여부도 지정할 수 있습니다:

```php
Auth::loginUsingId(1, remember: true);
```

#### 1회성 인증

`once` 메서드를 사용하면, 한 번의 요청에서만 사용자 인증을 처리할 수 있습니다. 이 메서드는 세션이나 쿠키를 사용하지 않으며, `Login` 이벤트도 발생시키지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
## HTTP Basic 인증 (HTTP Basic Authentication)

[HTTP Basic 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 화면을 구성할 필요 없이, 사용자를 인증하는 빠른 방법입니다. 먼저, `auth.basic` [미들웨어](/docs/12.x/middleware)를 라우트에 적용하세요. 이 미들웨어는 Laravel 프레임워크에 기본 포함되어 있으므로 별도의 정의가 필요 없습니다:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

미들웨어가 라우트에 적용되면, 해당 라우트에 브라우저로 접근할 때 자동으로 자격 증명 입력창이 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼이 사용자 "아이디"로 사용된다고 가정합니다.

#### FastCGI 사용 시 주의사항

[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache를 함께 사용한다면, HTTP Basic 인증이 제대로 동작하지 않을 수 있습니다. 이런 경우, 애플리케이션의 `.htaccess` 파일에 다음 라인을 추가하세요:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

### Stateless HTTP Basic 인증

세션에 사용자 식별자 쿠키를 남기지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 주로 API 요청에 HTTP 인증을 적용할 때 유용합니다. [미들웨어](/docs/12.x/middleware)를 정의할 때 `onceBasic` 메서드를 호출하세요. 이 메서드가 응답을 반환하지 않는다면, 요청이 애플리케이션의 다음 단계로 전달됩니다:

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

다음으로, 방금 만든 미들웨어를 라우트에 적용하세요:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
## 로그아웃 (Logging Out)

사용자를 수동으로 로그아웃 처리하려면, `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 인증 정보를 사용자 세션에서 제거하므로, 이후의 요청은 인증되지 않은 상태가 됩니다.

`logout` 호출 외에도, 세션 무효화 및 [CSRF 토큰](/docs/12.x/csrf)을 재생성하는 것이 좋습니다. 로그아웃 후에는 보통 애플리케이션의 루트로 사용자를 리디렉션합니다:

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
### 다른 기기의 세션 무효화

Laravel은 또한 인증된 현재 기기는 유지한 채, 동일 사용자의 다른 기기 세션만 무효화(로그아웃)할 수 있는 기능을 제공합니다. 이 기능은 보통 사용자가 비밀번호를 변경할 때, 다른 모든 기기에서는 세션을 무효화하면서 현재 기기는 로그인 상태를 유지하고자 할 때 사용합니다.

우선, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 해당 라우트에 포함되어 있어야 합니다. 일반적으로 이 미들웨어를 라우트 그룹에 지정하여 애플리케이션의 대부분 라우트에 적용합니다. 기본적으로 이 미들웨어는 `auth.session` [미들웨어 alias](/docs/12.x/middleware#middleware-aliases)를 통해 라우트에 붙일 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

그런 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 이 메서드는 사용자의 현재 비밀번호 확인이 필요하니, 별도의 입력 폼을 제공해야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

`logoutOtherDevices` 메서드를 호출하면, 해당 사용자의 다른 모든 기기 세션이 완전히 무효화되어, 이전에 인증된 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
## 비밀번호 재확인 (Password Confirmation)

애플리케이션을 만들다 보면, 사용자가 보안 영역으로 이동하거나 중요한 작업을 하기 전에 비밀번호를 한 번 더 입력 받는 경우가 있습니다. Laravel은 이 과정을 쉽게 구현할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 이용하려면, 비밀번호 재확인 요청 뷰를 보여주는 라우트와, 비밀번호 검증 후 목적지로 리디렉션하는 라우트 두 개를 정의해야 합니다.

> [!NOTE]
> 아래 문서는 비밀번호 재확인 기능을 직접 연동하는 방법을 설명합니다. 더 빠르게 시작하고 싶다면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)도 해당 기능을 지원합니다!

<a name="password-confirmation-configuration"></a>
### 설정

비밀번호를 재확인한 후에는 기본적으로 3시간 동안 다시 확인하지 않아도 됩니다. 재확인 주기를 변경하고 싶다면, 애플리케이션의 `config/auth.php` 파일에서 `password_timeout` 값을 수정하세요.

<a name="password-confirmation-routing"></a>
### 라우팅

#### 비밀번호 재확인 폼

먼저, 사용자에게 비밀번호를 입력받는 뷰를 띄우는 라우트를 정의합니다:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

이 라우트에서 반환하는 뷰에는 `password` 필드가 포함된 폼이 있어야 합니다. 또한, 보호된 영역이므로 비밀번호를 재입력해야 한다는 안내문도 뷰에 포함하세요.

#### 비밀번호 검증 처리

다음으로, "비밀번호 확인" 폼으로부터의 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증한 뒤 사용자를 목적지로 리디렉션합니다:

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

이 라우트는 먼저, 요청에서 입력받은 `password`가 인증된 사용자의 비밀번호와 일치하는지 검증합니다. 비밀번호가 맞으면, Laravel 세션에 사용자가 재확인 과정을 마쳤음을 기록해야 합니다. `passwordConfirmed` 메서드는 사용자의 세션에 재확인된 시각을 기록합니다. 마지막으로, 사용자를 원래 목적지로 리디렉션합니다.

### 라우트 보호

비밀번호를 최근에 재확인해야만 접근할 수 있는 라우트에는 `password.confirm` 미들웨어를 적용해야 합니다. 이 미들웨어는 기본 Laravel 설치에 포함되어 있으며, 사용자의 접근 목적지를 세션에 저장한 뒤, 비밀번호 재확인이 필요하면 `password.confirm` [네임드 라우트](/docs/12.x/routing#named-routes)로 리디렉션합니다:

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

직접 인증 가드를 정의하려면, `Auth` 파사드의 `extend` 메서드를 사용하세요. 이 코드는 [서비스 프로바이더](/docs/12.x/providers)에 두는 것이 좋습니다. Laravel에 기본 포함된 `AppServiceProvider`에 코드를 추가해봅시다:

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

위 예시와 같이, `extend`에 전달한 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 해당 인터페이스의 몇 가지 메서드를 구현하면 커스텀 가드를 정의할 수 있습니다. 커스텀 가드를 정의한 후에는, `auth.php`의 `guards` 설정에서 해당 가드를 사용할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
### 클로저 요청 가드

HTTP 요청 기반의 커스텀 인증 시스템을 가장 간단하게 구현하려면, `Auth::viaRequest` 메서드를 사용할 수 있습니다. 이 메서드는 단일 클로저로 인증 프로세스를 정의할 수 있게 해줍니다.

`AppServiceProvider`의 `boot` 메서드 내에서 `Auth::viaRequest`를 호출하여 사용하세요. 첫 번째 인자는 인증 드라이버 이름(원하는 문자열 사용 가능), 두 번째 인자는 요청을 받아 인증에 성공하면 사용자 인스턴스를, 실패하면 `null`을 반환하는 클로저입니다:

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

커스텀 인증 드라이버도 다른 가드처럼 `auth.php` 설정 파일에서 지정할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

그리고 해당 가드를 라우트의 인증 미들웨어로 지정하면 됩니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
## 커스텀 사용자 제공자 추가 (Adding Custom User Providers)

전통적인 관계형 데이터베이스 외에 다른 방식으로 사용자를 저장한다면, Laravel에 커스텀 사용자 제공자(user provider)를 직접 추가해야 합니다. 이를 위해 `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 제공자를 등록할 수 있습니다. 해당 제공자는 반드시 `Illuminate\Contracts\Auth\UserProvider`를 구현해야 합니다:

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

`provider` 메서드로 등록 후, 이제 이 제공자를 `auth.php` 설정 파일에서 사용할 수 있습니다. 먼저, 새 드라이버를 사용하는 `provider`를 정의합니다:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

마지막으로, 필요한 가드에서 이 제공자를 사용하도록 설정합니다:

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

`Illuminate\Contracts\Auth\UserProvider` 구현체는 영속 저장소(예: MySQL, MongoDB 등)에서 `Illuminate\Contracts\Auth\Authenticatable` 객체를 불러오는 역할을 담당합니다. 이 두 인터페이스를 통해 사용자 데이터 저장 방식 또는 인증 사용자 클래스를 무엇을 사용하든, Laravel 인증 메커니즘은 동일하게 동작할 수 있습니다.

`Illuminate\Contracts\Auth\UserProvider` 계약은 다음과 같습니다:

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

- `retrieveById`는 주로 MySQL의 auto-increment ID 등 사용자 키를 받아 해당하는 `Authenticatable` 객체를 반환합니다.
- `retrieveByToken`은 고유 `$identifier` 및 "로그인 상태 유지(remember me)" `$token` 값으로 사용자를 반환하며, 보통 데이터베이스의 `remember_token` 컬럼을 사용합니다.
- `updateRememberToken`은 `$user` 인스턴스의 `remember_token` 값을 새 `$token`으로 업데이트합니다. 일반적으로 "로그인 상태 유지" 인증 성공이나 로그아웃 시 새 토큰이 할당됩니다.
- `retrieveByCredentials`는 `Auth::attempt` 메서드에 전달된 자격 증명 배열(예: `username` 등)로 데이터를 조회합니다. 이 메서드는 패스워드 검증을 하지 않고, 지정한 값으로 사용자를 조회해 반환합니다.
- `validateCredentials`는 `$user`와 `$credentials`를 비교해 인증 여부를 결정합니다. 보통 `Hash::check`로 `$user->getAuthPassword()`와 `$credentials['password']` 값을 비교합니다. 올바르면 `true`, 틀리면 `false`를 반환합니다.
- `rehashPasswordIfRequired`는 필요한 경우, `$user`의 비밀번호를 재해싱합니다. 예를 들어, `Hash::needsRehash`로 판별 후 필요하면 `Hash::make`로 재해싱 및 저장하면 됩니다.

<a name="the-authenticatable-contract"></a>
### Authenticatable 계약

`UserProvider`의 각 메서드를 살펴보았으니, 이번에는 `Authenticatable` 계약을 살펴봅시다. 사용자 제공자는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스의 구현체를 반환해야 합니다:

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

이 인터페이스는 단순합니다:
- `getAuthIdentifierName`은 사용자에 대한 "기본 키" 컬럼명을,
- `getAuthIdentifier`은 사용자의 "기본 키" 값을,
- `getAuthPasswordName`은 비밀번호 컬럼명을,
- `getAuthPassword`는 해시된 비밀번호 값을 반환합니다.

이 인터페이스를 통해 어떤 ORM 또는 저장소 추상화 계층이든 동일하게 인증 시스템이 동작할 수 있습니다. Laravel에서는 `app/Models` 디렉터리 내 `App\Models\User` 클래스가 이미 이 인터페이스를 구현하고 있습니다.

<a name="automatic-password-rehashing"></a>
## 자동 비밀번호 재해싱 (Automatic Password Rehashing)

Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt의 "work factor"는 애플리케이션의 `config/hashing.php` 또는 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

CPU/GPU 성능이 올라갈수록 bcrypt work factor도 점진적으로 올려주는 것이 좋습니다. work factor가 변경된 경우, 사용자가 Laravel 스타터 키트나 [수동 인증](#authenticating-users) 시도(즉, `attempt` 메서드 사용)로 인증하면, 비밀번호를 자동으로 재해싱할 수 있습니다.

자동 재해싱은 애플리케이션 운영에 별다른 영향을 주지 않으나, 이 기능을 비활성화하려면 `hashing` 설정 파일을 퍼블리시한 후,

```shell
php artisan config:publish hashing
```

설정 파일에서 `rehash_on_login` 옵션을 `false`로 두면 됩니다:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 인증 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 다음 이벤트에 대해 [리스너를 정의](/docs/12.x/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트명                                    |
| -------------------------------------------- |
| `Illuminate\Auth\Events\Registered`            |
| `Illuminate\Auth\Events\Attempting`            |
| `Illuminate\Auth\Events\Authenticated`         |
| `Illuminate\Auth\Events\Login`                 |
| `Illuminate\Auth\Events\Failed`                |
| `Illuminate\Auth\Events\Validated`             |
| `Illuminate\Auth\Events\Verified`              |
| `Illuminate\Auth\Events\Logout`                |
| `Illuminate\Auth\Events\CurrentDeviceLogout`   |
| `Illuminate\Auth\Events\OtherDeviceLogout`     |
| `Illuminate\Auth\Events\Lockout`               |
| `Illuminate\Auth\Events\PasswordReset`         |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>