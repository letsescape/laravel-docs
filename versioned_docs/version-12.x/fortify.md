# Laravel Fortify (Laravel Fortify)

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify를 언제 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이징](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이징](#customizing-the-authentication-pipeline)
    - [리디렉션 커스터마이징](#customizing-authentication-redirects)
- [2단계 인증](#two-factor-authentication)
    - [2단계 인증 활성화](#enabling-two-factor-authentication)
    - [2단계 인증으로 인증하기](#authenticating-with-two-factor-authentication)
    - [2단계 인증 비활성화](#disabling-two-factor-authentication)
- [회원가입](#registration)
    - [회원가입 커스터마이징](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이징](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 확인](#password-confirmation)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 라라벨의 모든 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후에는 `route:list` 아티즌 명령어를 실행하여 Fortify가 등록한 라우트들을 확인할 수 있습니다.

Fortify는 자체적으로 사용자 인터페이스를 제공하지 않으므로, 등록된 라우트에 요청을 보내는 여러분만의 사용자 인터페이스와 연동하는 것이 기본적인 사용 방식입니다. 이 문서에서는 이러한 라우트로 요청을 보내는 구체적인 방법에 대해 설명합니다.

> [!NOTE]
> Fortify는 라라벨의 인증 기능을 빠르게 구현하는 데 도움을 주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** 언제든지 [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 공식 문서를 따라 직접 인증 기능을 구현할 수 있습니다.

<a name="what-is-fortify"></a>
### Fortify란? (What is Fortify?)

앞서 언급했듯이, Laravel Fortify는 Laravel을 위한 프론트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 라라벨의 모든 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다.

**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 문서를 참고하여, Laravel의 인증 서비스와 직접 상호작용할 수 있습니다.

라라벨을 처음 접한다면 [스타터 키트](/docs/12.x/starter-kits)를 살펴볼 것을 권장합니다. 라라벨의 스타터 키트는 내부적으로 Fortify를 사용해 Tailwind CSS로 만든 사용자 인터페이스가 있는 인증 스캐폴딩을 제공합니다. 이를 통해 라라벨의 인증 기능을 쉽게 익힐 수 있습니다.

Laravel Fortify는 스타터 키트에서 제공하는 라우트와 컨트롤러를 별도의 UI 없이 패키지로 분리한 것입니다. 이를 통해 빠르게 인증 백엔드만 구축하고, 프론트엔드는 자유롭게 구현할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 하나요? (When Should I Use Fortify?)

Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, 라라벨의 [스타터 키트](/docs/12.x/starter-kits)를 사용한다면 별도로 Fortify를 설치할 필요가 없습니다. 모든 스타터 키트가 Fortify를 내부적으로 사용하며 완전한 인증 구현을 제공합니다.

스타터 키트를 사용하지 않고 애플리케이션에 인증 기능이 필요하다면
1. 인증 기능을 직접 수동으로 구현하거나
2. Fortify를 설치해 인증 백엔드 기능을 빠르게 설정할 수 있습니다.

Fortify를 설치하면, 사용자 인터페이스에서 Fortify가 등록하는 인증 라우트에 요청을 보내 인증 및 회원가입 처리를 하게 됩니다.

반대로 Fortify를 사용하지 않고 Laravel의 인증 기능을 직접 사용하려면, 위에서 언급한 [인증](/docs/12.x/authentication), [비밀번호 재설정](/docs/12.x/passwords), [이메일 인증](/docs/12.x/verification) 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자들은 [Laravel Sanctum](/docs/12.x/sanctum)과 Laravel Fortify의 차이점에 혼동을 느낄 수 있습니다. 이 두 패키지는 서로 다른 목적을 가지고 있기 때문에 상호 보완적이며 경쟁 관계가 아닙니다.

Laravel Sanctum은 API 토큰 관리 및 세션 쿠키/토큰을 통한 기존 사용자 인증만 담당합니다. 회원가입, 비밀번호 재설정 등과 같은 라우트는 제공하지 않습니다.

API를 제공하거나, SPA(싱글 페이지 애플리케이션)의 백엔드로 인증 계층을 직접 구축하려는 경우, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)를 모두 활용하는 것이 일반적입니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 사용해 Fortify를 설치합니다.

```shell
composer require laravel/fortify
```

다음으로, `fortify:install` 아티즌 명령어를 실행해 Fortify 리소스를 퍼블리시합니다.

```shell
php artisan fortify:install
```

이 명령어는 Fortify의 액션을 `app/Actions` 디렉터리에 생성합니다(해당 디렉터리가 없다면 새로 생성됨). 또한 `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션 파일들도 함께 퍼블리시됩니다.

이후 데이터베이스 마이그레이션을 실행해야 합니다.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능 (Fortify Features)

`fortify` 설정 파일에는 `features`라는 설정 배열이 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트/기능을 정의합니다. 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다.

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화 (Disabling Views)

기본적으로 Fortify는 로그인 화면이나 회원가입 화면처럼, 뷰를 반환하는 라우트를 정의합니다. 하지만 JavaScript 기반의 SPA(싱글 페이지 애플리케이션)을 만든다면 이러한 라우트가 필요 없을 수 있습니다. 이럴 때는 `config/fortify.php`의 `views` 값을 `false`로 설정해 이러한 라우트 전체를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

Fortify의 뷰를 비활성화하면서도 비밀번호 재설정 기능을 사용할 경우, 애플리케이션에서 "비밀번호 재설정" 화면을 표시하는 `password.reset`이라는 이름의 라우트는 직접 반드시 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 생성할 때 `password.reset` 라우트를 참조하기 때문입니다.

<a name="authentication"></a>
## 인증 (Authentication)

먼저 Fortify에 "로그인" 뷰를 어떻게 반환할지 알려줘야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)라는 것을 기억하세요. 이미 완성된 프론트엔드 인증 기능이 필요하다면 [스타터 키트](/docs/12.x/starter-kits)를 사용하는 것이 좋습니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 이용해 커스터마이즈할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다. Fortify가 `/login` 라우트를 정의해서 이 뷰를 반환하게 됩니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 있어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email`/`username`과 `password`를 기대합니다. `email`/`username` 필드명은 `config/fortify.php`의 `username` 값과 일치해야 합니다. 또한, Laravel의 "remember me" 기능을 사용하려면 불리언 타입의 `remember` 필드를 추가할 수 있습니다.

로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. 만약 로그인 요청이 XHR 요청이었다면 200 HTTP 응답이 반환됩니다.

요청이 실패하면, 사용자는 로그인 화면으로 돌아가며 유효성 검사 오류 정보는 공유된 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR 요청의 경우 422 HTTP 응답과 함께 유효성 검사 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이징 (Customizing User Authentication)

Fortify는 제공된 자격 증명과 애플리케이션에 설정된 인증 가드에 따라 사용자를 자동으로 조회하고 인증합니다. 하지만 로그인 자격 증명 검증 및 사용자 조회 방법을 완전히 커스터마이징하고 싶을 때도 있습니다. `Fortify::authenticateUsing` 메서드를 사용하면 쉽게 커스터마이징할 수 있습니다.

이 메서드는 들어오는 HTTP 요청을 받는 클로저를 인수로 받습니다. 클로저는 요청으로 전달된 로그인 정보를 검증하고, 해당 사용자가 존재한다면 사용자 인스턴스를 반환해야 합니다. 자격 증명이 올바르지 않거나 사용자를 찾지 못하면, `null`이나 `false`를 반환해야 합니다. 주로 `FortifyServiceProvider`의 `boot` 메서드에서 이 메서드를 호출하면 됩니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```

<a name="authentication-guard"></a>
#### 인증 가드 (Authentication Guard)

Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 설정한 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스의 구현체여야 합니다. SPA 인증에 Fortify를 사용할 경우, 라라벨의 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 사용하는 것을 권장합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이징 (Customizing the Authentication Pipeline)

Laravel Fortify는 로그인 요청을 여러 `__invoke` 메서드를 가진 클래스의 파이프라인을 거쳐 인증합니다. 원하는 경우 로그인 요청이 거치는 파이프라인 클래스를 커스텀할 수 있습니다. 각 클래스는 들어오는 `Illuminate\Http\Request` 인스턴스와, 그 요청을 다음 파이프라인 클래스에 넘기는 `$next` 변수를 인수로 받습니다(미들웨어와 비슷한 방식입니다).

커스텀 파이프라인 정의 방법은 `Fortify::authenticateThrough` 메서드를 사용합니다. 이 메서드는 로그인 요청을 거칠 클래스 배열을 반환하는 클로저를 인수로 받습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

아래 예시는 기본 파이프라인 정의를 보여주며, 커스터마이즈 시 참고하면 좋습니다.

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

#### 인증 제한 (Authentication Throttling)

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어로 로그인 시도 횟수를 제한합니다. 이 미들웨어는 사용자명과 IP 조합별로 로그인 시도를 제한합니다.

일부 애플리케이션에서는, 예를 들어 IP별로만 인증 시도를 제한하는 등 다른 방식의 인증 제한(스로틀링)이 필요할 수 있습니다. Fortify는 `fortify.limiters.login` 설정 옵션을 통해 직접 [속도 제한자](/docs/12.x/routing#rate-limiting)를 지정할 수 있습니다. 이 옵션은 `config/fortify.php` 파일에 있습니다.

> [!NOTE]
> 인증 제한, [2단계 인증](/docs/12.x/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 함께 적용할 때 애플리케이션의 보안이 가장 강력하게 보호됩니다.

<a name="customizing-authentication-redirects"></a>
### 리디렉션 커스터마이징 (Customizing Redirects)

로그인에 성공하면 Fortify는 `fortify` 설정 파일 내의 `home` 옵션에 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR일 경우 200 HTTP 응답을 반환합니다. 사용자가 로그아웃하면 `/`로 이동하게 됩니다.

이 동작을 더 세밀하게 커스터마이즈해야 한다면, Laravel [서비스 컨테이너](/docs/12.x/container)에 `LoginResponse`, `LogoutResponse` 계약의 인스턴스를 바인딩해서 구현할 수 있습니다. 주로 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 이 바인딩을 처리합니다.

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```

<a name="two-factor-authentication"></a>
## 2단계 인증 (Two-Factor Authentication)

Fortify의 2단계 인증 기능을 활성화하면, 인증 과정에서 사용자는 6자리 숫자 토큰을 추가로 입력해야 합니다. 이 토큰은 Google Authenticator 같은 TOTP 호환 모바일 인증앱에서 생성되는 시간 기반 일회용 비밀번호(TOTP)입니다.

먼저, 애플리케이션의 `App\Models\User` 모델에 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 추가해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
```

다음으로, 사용자들이 2단계 인증을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 2단계 인증 활성화/비활성화, 복구 코드 재생성 등을 지원해야 합니다.

> 기본적으로, `fortify` 설정 파일의 `features` 배열은 2단계 인증 설정 변경 전 비밀번호 확인이 필요하도록 구성되어 있습니다. 따라서 [비밀번호 확인](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2단계 인증 활성화 (Enabling Two-Factor Authentication)

2단계 인증을 활성화하려면, 애플리케이션에서 Fortify가 제공하는 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 요청에 성공하면 직전 URL로 리디렉션되고, 세션 변수 `status`에 `two-factor-authentication-enabled`가 저장됩니다. 뷰에서 이 값을 감지해 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

2단계 인증을 활성화한 후, 사용자는 "2단계 인증 구성 완료"를 위해 유효한 인증 코드를 입력해 설정을 "확인(Confirm)"해야 합니다. 따라서 성공 메시지에는 확인이 필요함을 반드시 안내해야 합니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

이후, 사용자가 인증 앱에 등록할 수 있도록 2단계 인증용 QR 코드를 표시해야 합니다. Blade를 사용한다면, 인증된 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 SVG QR 코드를 얻을 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript 프론트엔드에서 사용할 경우, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내면 QR 코드가 포함된 JSON(`svg` 키) 응답을 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 2단계 인증 확인 (Confirming Two-Factor Authentication)

QR 코드를 보여줄 뿐 아니라, 사용자가 인증 코드를 입력해서 2단계 인증 구성을 "확인"할 수 있는 입력란을 제공해야 합니다. 이 코드는 Fortify가 제공하는 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청을 보내야 하며,

성공 시 이전 URL로 리디렉션되고, 세션 변수 `status`에는 `two-factor-authentication-confirmed`가 저장됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시 (Displaying the Recovery Codes)

사용자에게 2단계 인증 복구 코드도 반드시 보여주어야 합니다. 복구 코드는 사용자가 기기를 분실했을 때 로그인에 사용할 수 있습니다. Blade에서는 인증된 사용자 인스턴스의 `recoveryCodes()`로 배열을 얻을 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

JavaScript 프론트엔드에서는 `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청을 보내 복구 코드 배열을 받을 수 있습니다.

복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트로 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 2단계 인증으로 인증하기 (Authenticating With Two-Factor Authentication)

인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 도전(Challenge) 화면으로 리디렉션합니다. 만약 XHR 로그인 요청이라면, 성공한 응답에 `two_factor`라는 불리언 값을 가진 JSON 오브젝트가 포함되어 있습니다. 이 값을 검사해 2단계 인증 도전 화면으로 이동해야 하는지 판단할 수 있습니다.

2단계 인증 기능을 구현하려면, Fortify에 2단계 인증 도전 뷰를 반환하는 방법을 알려주어야 합니다. 이 역시 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify가 `/two-factor-challenge` 라우트를 정의해 이 뷰를 반환합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge`로 POST 요청을 보내는 폼이 있어야 하며, 필드로 `code`(유효한 TOTP 토큰) 또는 `recovery_code`(복구 코드) 중 하나를 전달해야 합니다.

로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청이라면 204 HTTP 응답이 반환됩니다.

실패하면 다시 도전 화면으로 돌아가며, 유효성 오류는 Blade의 `$errors` 변수로 제공됩니다. XHR 요청인 경우 422 HTTP 오류와 함께 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2단계 인증 비활성화 (Disabling Two-Factor Authentication)

2단계 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내면 됩니다. 참고로 Fortify의 2단계 인증 관련 엔드포인트는 [비밀번호 확인](#password-confirmation)이 선행되어야 접근할 수 있습니다.

<a name="registration"></a>
## 회원가입 (Registration)

애플리케이션의 회원가입 기능을 구현하려면, 먼저 Fortify에 회원가입 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)라는 점을 다시 한 번 기억하세요. 이미 완성된 프론트엔드 기능이 필요하다면 [스타터 키트](/docs/12.x/starter-kits)를 사용하세요.

모든 뷰 렌더링 커스터마이징은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드로 할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify가 `/register` 라우트를 정의해 이 뷰를 반환합니다. `register` 템플릿에는 `/register`에 POST 요청을 보내는 폼이 있어야 하며, Fortify가 지정한 엔드포인트를 따라야 합니다.

`/register` 엔드포인트는 문자열 타입의 `name`, 이메일 또는 사용자명(`email`/`username`), `password`, `password_confirmation` 필드를 기대합니다. 이메일/사용자명 필드명은 설정 파일의 `username` 값과 일치해야 합니다.

회원가입이 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청이라면 201 HTTP 응답이 반환됩니다.

실패할 경우 사용자는 회원가입 화면으로 되돌아가며, 유효성 검사 오류 정보는 공유된 `$errors` [Blade 템플릿 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 제공됩니다. XHR 요청인 경우 422 HTTP 오류와 함께 반환됩니다.

<a name="customizing-registration"></a>
### 회원가입 커스터마이징 (Customizing Registration)

사용자 유효성 검사 및 생성 프로세스는 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션 파일을 수정하여 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정 (Password Reset)

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting a Password Reset Link)

비밀번호 재설정 기능을 구현하려면, 먼저 Fortify에 "비밀번호 재설정 링크 요청" 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리라는 점을 기억하세요. 프론트엔드까지 포함된 기능이 필요하다면 [스타터 키트](/docs/12.x/starter-kits)를 사용하세요.

모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 관련 메서드로 커스터마이즈할 수 있으며, 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify가 `/forgot-password` 엔드포인트를 정의해 뷰를 반환합니다. `forgot-password` 템플릿에는 `/forgot-password`로 POST 요청을 보내는 폼이 있어야 하며,

`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드만 요구합니다. 필드명/DB 컬럼명은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 결과 처리

비밀번호 재설정 링크 요청이 성공하면 Fortify는 사용자를 `/forgot-password` 라우트로 다시 리디렉션시키고, 보안이 적용된 링크가 포함된 이메일을 사용자에게 전송합니다. XHR 요청인 경우 200 HTTP 응답이 반환됩니다.

리디렉션된 후의 화면에서 `status` 세션 변수를 이용해 요청 성공 메시지를 표시할 수 있습니다.

`$status` 값은 애플리케이션의 `passwords` [언어 파일](/docs/12.x/localization) 내 번역 문자열 중 하나와 일치합니다. 값을 직접 커스터마이즈하고 싶다면 언어 파일을 퍼블리시(`lang:publish`)하여 수정하면 됩니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청 실패 시, 비밀번호 재설정 요청 화면으로 되돌아가며 오류 정보는 `$errors` [Blade 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인 가능합니다. XHR 요청인 경우 422 HTTP 오류가 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

기능 완성을 위해 Fortify에 실제 "비밀번호 재설정" 뷰를 반환하는 방법을 알려주어야 합니다.

역시 `Laravel\Fortify\Fortify` 클래스의 관련 메서드를 통해 뷰를 지정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify가 이 뷰를 보여주는 라우트를 등록합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼이 있어야 하며,

`/reset-password` 엔드포인트는 문자열 타입의 `email`, `password`, `password_confirmation` 필드와 함께, 숨겨진 필드 `token`(값은 `request()->route('token')`)을 요구합니다. 이메일 필드명/DB 컬럼명은 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 결과 처리

비밀번호 재설정 요청이 성공하면, Fortify는 `/login` 라우트로 리디렉션해 사용자가 새 비밀번호로 로그인할 수 있게 합니다. 이와 함께 성공 상태를 알리는 `status` 세션 변수가 설정되고, 로그인 화면에서 아래와 같이 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청인 경우 200 HTTP 응답을 반환합니다.

요청이 실패하면 재설정 화면으로 돌아가며, 유효성 오류 정보는 `$errors` [Blade 변수](/docs/12.x/validation#quick-displaying-the-validation-errors)로 제공됩니다. XHR 요청 시 422 HTTP 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이징 (Customizing Password Resets)

비밀번호 재설정 프로세스는 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증 (Email Verification)

회원가입 후, 사용자가 애플리케이션을 계속 이용하려면 이메일 인증을 거치도록 할 수 있습니다. 활성화하려면, `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 포함되어 있는지 확인하세요. 또한, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

이 두 가지 설정을 마치면, 새로 가입한 사용자에게 이메일 인증을 요청하는 메일이 발송됩니다. 다음으로, Fortify에 이메일 인증 안내 메시지를 보여주는 화면을 반환하는 방법을 알려주어야 합니다.

모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스에서 관련 메서드로 지정할 수 있으며, 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify가 이 뷰를 보여주는 라우트를 등록합니다. 사용자가 라라벨의 `verified` 미들웨어에 의해 `/email/verify`로 리디렉션되면 이 화면이 표시됩니다.

`verify-email` 템플릿에는 이메일 인증 링크를 클릭하라는 안내 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재전송

사용자가 이전 인증메일을 삭제했거나 잃어버린 경우를 위해, 인증 메일을 재전송하는 버튼을 `verify-email` 템플릿에 추가할 수 있습니다. 이 버튼은 `/email/verification-notification` 엔드포인트로 POST 요청을 보냅니다. 요청이 성공하면 새 인증 링크가 이메일로 전송되며, `/email/verify` 엔드포인트로 리디렉션되어 `status` 세션 변수로 성공 메시지를 보여줄 수 있습니다. XHR 요청의 경우 202 HTTP 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

특정 라우트나 라우트 그룹에 대해 사용자가 이메일 인증을 완료해야 접근할 수 있게 하려면, Laravel의 내장 `verified` 미들웨어를 해당 라우트에 추가하면 됩니다. `verified` 미들웨어 별칭은 자동 등록되며 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 확인 (Password Confirmation)

애플리케이션 개발 중에는 사용자가 특정 작업을 수행하기 전에 비밀번호를 다시 한 번 확인해야 하는 경우가 종종 있습니다. 이러한 라우트는 주로 Laravel의 내장 `password.confirm` 미들웨어로 보호됩니다.

비밀번호 확인 화면을 구현하려면, Fortify에 "비밀번호 확인" 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)임을 기억하세요. 이미 준비된 프론트엔드가 필요한 경우에는 [스타터 키트](/docs/12.x/starter-kits)를 사용하세요.

모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 적절한 메서드를 통해 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify가 `/user/confirm-password` 엔드포인트를 정의해 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password`로 POST 요청을 보내는 폼이 있어야 하며, `password` 필드에 사용자의 현재 비밀번호가 포함되어야 합니다.

비밀번호가 올바르면 사용자는 접근하려던 라우트로 리디렉션됩니다. XHR 요청인 경우 201 HTTP 응답이 반환됩니다.

실패하면 다시 비밀번호 확인 화면으로 돌아가며, 유효성 오류 정보는 Blade의 `$errors` 변수로 제공됩니다. XHR 요청이라면 422 HTTP 오류가 반환됩니다.
