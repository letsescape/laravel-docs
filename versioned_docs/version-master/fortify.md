# 라라벨 Fortify (Laravel Fortify)

- [소개](#introduction)
    - [Fortify란?](#what-is-fortify)
    - [Fortify를 언제 사용해야 하나요?](#when-should-i-use-fortify)
- [설치](#installation)
    - [Fortify 기능](#fortify-features)
    - [뷰 비활성화](#disabling-views)
- [인증](#authentication)
    - [사용자 인증 커스터마이즈](#customizing-user-authentication)
    - [인증 파이프라인 커스터마이즈](#customizing-the-authentication-pipeline)
    - [리다이렉트 커스터마이즈](#customizing-authentication-redirects)
- [2차 인증](#two-factor-authentication)
    - [2차 인증 활성화](#enabling-two-factor-authentication)
    - [2차 인증을 통한 인증](#authenticating-with-two-factor-authentication)
    - [2차 인증 비활성화](#disabling-two-factor-authentication)
- [사용자 등록](#registration)
    - [사용자 등록 커스터마이즈](#customizing-registration)
- [비밀번호 재설정](#password-reset)
    - [비밀번호 재설정 링크 요청](#requesting-a-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
    - [비밀번호 재설정 커스터마이즈](#customizing-password-resets)
- [이메일 인증](#email-verification)
    - [라우트 보호](#protecting-routes)
- [비밀번호 재확인](#password-confirmation)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Fortify](https://github.com/laravel/fortify)는 라라벨을 위한 프론트엔드에 종속되지 않는 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 라라벨의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록합니다. Fortify 설치 후, `route:list` 아티즌 명령어를 실행하면 Fortify가 등록한 라우트를 확인할 수 있습니다.

Fortify는 자체 사용자 인터페이스를 제공하지 않으므로, 여러분이 직접 사용자 인터페이스를 구현하여 Fortify가 등록한 라우트에 요청을 보내는 형태로 연동해야 합니다. 이러한 라우트에 어떻게 요청하는지에 대해서는 이 문서의 뒷부분에서 자세히 안내합니다.

> [!NOTE]
> Fortify는 라라벨 인증 기능 구현에 도움을 주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [인증](/docs/master/authentication), [비밀번호 재설정](/docs/master/passwords), [이메일 인증](/docs/master/verification) 공식 문서를 참고하여 수동으로 라라벨 인증 서비스를 사용할 수도 있습니다.

<a name="what-is-fortify"></a>
### Fortify란? (What is Fortify?)

앞서 설명했듯이, Laravel Fortify는 라라벨을 위한 프론트엔드에 종속되지 않는 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 라라벨 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다.

**라라벨의 인증 기능을 사용하기 위해 반드시 Fortify를 사용해야 하는 것은 아닙니다.** [인증](/docs/master/authentication), [비밀번호 재설정](/docs/master/passwords), [이메일 인증](/docs/master/verification) 공식 문서를 참고하여 직접 인증 기능을 구현할 수도 있습니다.

라라벨을 처음 사용한다면, [애플리케이션 스타터 킷](/docs/master/starter-kits)을 살펴보시기 바랍니다. 라라벨의 애플리케이션 스타터 킷은 내부적으로 Fortify를 사용하여 [Tailwind CSS](https://tailwindcss.com) 기반의 사용자 UI와 함께 인증 스캐폴딩을 제공합니다. 이를 통해 라라벨의 인증 기능을 쉽게 학습하며 익숙해질 수 있습니다.

Fortify는 애플리케이션 스타터 킷의 라우트와 컨트롤러를 패키지 형태로 제공합니다. 즉, UI는 제공하지 않으며, 백엔드 인증 레이어만 빠르게 스캐폴딩할 수 있게 해줍니다. 따라서 원하는 프론트엔드와 손쉽게 조합할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
### Fortify를 언제 사용해야 하나요? (When Should I Use Fortify?)

라라벨 Fortify를 언제 사용할지 고민될 수 있습니다. 우선, 라라벨의 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용한다면 Fortify를 별도로 설치할 필요가 없습니다. 모든 공식 애플리케이션 스타터 킷은 Fortify를 사용하고, 인증 기능을 완비한 상태로 제공합니다.

애플리케이션 스타터 킷을 사용하지 않고 인증 기능이 필요한 경우에는 두 가지 방법이 있습니다. 하나는 직접 인증 기능을 구현하는 것, 다른 하나는 Fortify를 설치하여 인증 백엔드 구현을 적용하는 것입니다.

Fortify를 설치하면, 여러분이 구현한 프론트엔드가 이 문서에서 안내하는 Fortify의 인증 라우트에 요청을 보내어 사용자 인증 및 등록을 처리하게 됩니다.

Fortify 대신 직접 라라벨의 인증 서비스를 사용하려면, [인증](/docs/master/authentication), [비밀번호 재설정](/docs/master/passwords), [이메일 인증](/docs/master/verification) 공식 문서를 참고하여 구현하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify와 Laravel Sanctum

일부 개발자는 [Laravel Sanctum](/docs/master/sanctum)과 Laravel Fortify의 차이점에 대해 혼란을 가질 수 있습니다. 이 두 패키지는 서로 연관되지만 다른 역할을 수행하므로, 상호 대체하거나 경쟁하는 패키지가 아닙니다.

Laravel Sanctum은 API 토큰 관리와, 세션 쿠키 또는 토큰을 사용한 기존 사용자 인증에만 집중합니다. 회원가입, 비밀번호 재설정 등과 관련된 라우트는 제공하지 않습니다.

만약 API를 제공하거나 싱글 페이지 애플리케이션(SPA)의 백엔드로 동작하는 애플리케이션에서 인증 레이어를 직접 구축하려고 한다면, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 함께 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

먼저, Composer 패키지 매니저를 이용해 Fortify를 설치합니다.

```shell
composer require laravel/fortify
```

그 다음, `fortify:install` 아티즌 명령어로 Fortify의 리소스를 퍼블리시합니다.

```shell
php artisan fortify:install
```

이 명령어는 Fortify의 액션을 `app/Actions` 디렉토리에 퍼블리시합니다. 해당 디렉토리가 없으면 새로 생성됩니다. 또한 `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션도 함께 퍼블리시됩니다.

그 다음, 데이터베이스 마이그레이션을 실행하세요.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
### Fortify 기능 (Fortify Features)

`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열은 Fortify가 어떤 백엔드 라우트/기능을 기본적으로 노출할 것인지 정의합니다. 대부분의 라라벨 애플리케이션에서 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다.

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### 뷰 비활성화 (Disabling Views)

기본적으로 Fortify는 로그인 화면, 회원가입 화면 등 뷰를 반환하는 라우트를 등록합니다. 하지만 자바스크립트 기반 싱글 페이지 애플리케이션(SPA)을 만든다면, 이러한 라우트는 필요하지 않을 수 있습니다. 이 경우, 애플리케이션의 `config/fortify.php` 설정 파일에서 `views` 값을 `false`로 설정하여 관련 라우트를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### 뷰 비활성화와 비밀번호 재설정

Fortify의 뷰를 비활성화하고 애플리케이션에 비밀번호 재설정 기능을 구현할 경우, 애플리케이션에서 "비밀번호 재설정" 뷰를 담당할 `password.reset` 명명 라우트를 직접 정의해야 합니다. 이는 라라벨의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset` 라우트를 이용해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
## 인증 (Authentication)

먼저, Fortify가 "로그인" 뷰를 반환하는 방법을 지정해야 합니다. Fortify는 별도의 UI를 제공하지 않는 헤드리스 인증 라이브러리입니다. 이미 완성된 인증 프론트엔드를 적용하고 싶다면, [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용하는 것이 좋습니다.

모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 이용해 커스터마이즈할 수 있습니다. 일반적으로, 해당 메서드는 애플리케이션 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다. 아래와 같이 `/login` 라우트가 정의되어 뷰를 반환합니다.

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

로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email`/`username`과 `password`를 기대합니다. 이메일/아이디 필드명은 `config/fortify.php`의 `username` 값과 일치해야 하며, "자동 로그인(remember me)" 기능을 사용하려면 불리언 타입의 `remember` 필드를 추가할 수 있습니다.

로그인에 성공하면, Fortify는 애플리케이션의 `fortify` 설정 파일 `home` 옵션에 지정된 URI로 리다이렉트합니다. 만약 로그인 요청이 XHR(ajax) 방식이었다면, 200 HTTP 응답이 반환됩니다.

요청이 실패하면 사용자는 다시 로그인 화면으로 리다이렉트되며, 검증 에러는 공유된 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)를 통해 접근할 수 있습니다. XHR 요청일 경우, 422 HTTP 응답과 함께 검증 에러가 반환됩니다.

<a name="customizing-user-authentication"></a>
### 사용자 인증 커스터마이즈 (Customizing User Authentication)

Fortify는 기본적으로 제공된 자격 증명과 애플리케이션에서 설정된 인증 가드를 기반으로 사용자를 자동 검색 및 인증합니다. 그러나 인증 과정을 완전히 커스터마이즈하고 싶을 때는 `Fortify::authenticateUsing` 메서드를 사용할 수 있습니다.

이 메서드는 인커밍 HTTP 요청을 인수로 받는 클로저를 전달받으며, 여기서 요청된 로그인 자격 증명을 검증하고 관련 사용자 인스턴스를 반환합니다. 자격 증명이 유효하지 않거나 사용자를 찾지 못하면 `null` 또는 `false`를 반환해야 합니다. 일반적으로 이 메서드는 `FortifyServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

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

Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이즈할 수 있습니다. 단, 설정된 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현해야 하며, 싱글 페이지 애플리케이션(SPA) 인증에 Fortify를 사용할 경우 [Laravel Sanctum](https://laravel.com/docs/sanctum) 및 기본 `web` 가드를 함께 사용해야 합니다.

<a name="customizing-the-authentication-pipeline"></a>
### 인증 파이프라인 커스터마이즈 (Customizing the Authentication Pipeline)

Laravel Fortify는 로그인 요청을 여러 개의 인보커블(호출 가능한) 클래스가 모여 있는 파이프라인 형태로 처리합니다. 필요하다면 로그인 요청이 통과할 클래스를 직접 정의할 수 있습니다. 각 클래스는 미들웨어처럼, 인커밍 `Illuminate\Http\Request` 인스턴스와 `$next` 변수를 받아 파이프라인 다음 클래스로 요청을 넘깁니다.

사용자 정의 파이프라인은 `Fortify::authenticateThrough` 메서드를 이용해 정의합니다. 이 메서드는 로그인 요청이 통과할 클래스 배열을 반환하는 클로저를 받습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

아래 예시는 기본 파이프라인 정의이며, 이 구조를 참고하여 필요한 로직을 추가하거나 수정할 수 있습니다.

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

#### 인증 시도 제한 (Authentication Throttling)

기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어를 사용하여 인증 시도 횟수를 제한합니다. 이 미들웨어는 사용자명과 IP 주소 조합별 시도를 제한합니다.

애플리케이션에 따라 IP별 제한 등 다른 제한 방식을 원할 수 있기 때문에, Fortify는 `fortify.limiters.login` 설정 옵션을 통해 [레이트 리미터](/docs/master/routing#rate-limiting)를 직접 지정할 수 있습니다. 이 옵션은 애플리케이션의 `config/fortify.php` 파일에 위치합니다.

> [!NOTE]
> 인증 시도 제한, [2차 인증](/docs/master/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 적절히 조합하면 사용자 계정의 보안성을 크게 높일 수 있습니다.

<a name="customizing-authentication-redirects"></a>
### 리다이렉트 커스터마이즈 (Customizing Redirects)

로그인에 성공하면 Fortify는 애플리케이션 `fortify` 설정 파일의 `home` 옵션에 설정된 URI로 리다이렉트합니다. XHR 요청의 경우 200 HTTP 응답을 반환합니다. 로그아웃 후에는 `/` URI로 리다이렉트됩니다.

더 세밀하게 동작을 제어하고 싶다면, `LoginResponse`와 `LogoutResponse` 계약(contract) 구현체를 라라벨 [서비스 컨테이너](/docs/master/container)에 바인딩하면 됩니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 다음과 같이 구현합니다.

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
## 2차 인증 (Two-Factor Authentication)

Fortify에서 2차 인증 기능을 활성화하면, 인증 과정에서 6자리 숫자 토큰 입력이 요구됩니다. 이 토큰은 Google Authenticator와 같은 TOTP 호환 모바일 인증 앱에서 생성되는 시간 기반 일회용 비밀번호(TOTP) 방식입니다.

먼저, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인해야 합니다.

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

그 다음, 사용자가 자신의 2차 인증 설정을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 2차 인증의 활성화/비활성화, 복구 코드 재생성 등이 가능해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열은 2차 인증 설정 시 비밀번호 재확인을 요구하도록 구성되어 있습니다. 계속 진행하기 전에 Fortify의 [비밀번호 재확인](#password-confirmation) 기능을 구현해 두어야 합니다.

<a name="enabling-two-factor-authentication"></a>
### 2차 인증 활성화 (Enabling Two-Factor Authentication)

2차 인증 활성화를 시작하려면, 애플리케이션이 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 성공 시 사용자는 이전 URL로 리다이렉트되고, `status` 세션 변수에 `two-factor-authentication-enabled`가 설정됩니다. 이를 템플릿에서 감지하여 성공 메시지를 띄울 수 있습니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

2차 인증을 활성화해도 실제로 "설정 확정(confirmation)"을 마치기 전까지는 완전히 적용되지 않습니다. 즉, 사용자는 유효한 2차 인증 코드를 직접 입력하여 인증 설정을 마무리해야 합니다. 성공 메시지에는 이 안내도 포함해야 합니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

그 다음, 사용자가 인증 앱에서 스캔할 수 있도록 2차 인증 QR 코드를 표시해야 합니다. Blade로 프론트엔드를 구현한다면, 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드를 이용해 QR 코드 SVG를 표시할 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

만약 자바스크립트 프론트엔드라면, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보낸 뒤, JSON 응답의 `svg` 키로 SVG 데이터를 가져다 쓸 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
#### 2차 인증 확정 (Confirming Two-Factor Authentication)

사용자에게 2차 인증 QR 코드를 보여주는 것 외에도, 올바른 인증 코드를 입력하여 2차 인증 설정을 "확정"할 수 있는 입력창을 제공해야 합니다. 이 코드는 Fortify가 정의한 `/user/confirmed-two-factor-authentication` 엔드포인트에 POST 방식으로 전달됩니다.

요청이 성공하면 사용자는 이전 URL로 리다이렉트되고, `status` 세션 변수에 `two-factor-authentication-confirmed`가 설정됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

XHR 요청인 경우엔 200 HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시 (Displaying the Recovery Codes)

사용자의 복구 코드도 화면에 함께 표시해야 합니다. 복구 코드는 사용자가 휴대폰을 분실했을 때 로그인할 수 있도록 도와줍니다. Blade로 프론트엔드를 구현 중이라면 아래와 같이 인증 사용자의 복구 코드를 확인할 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

자바스크립트 프론트엔드라면 `/user/two-factor-recovery-codes` 엔드포인트에 GET 요청을 보내 JSON 배열로 받아올 수 있습니다.

복구 코드를 재생성하려면, 애플리케이션이 `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청하면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
### 2차 인증을 통한 인증 (Authenticating With Two-Factor Authentication)

인증 과정에서 Fortify는 자동으로 사용자를 애플리케이션의 2차 인증 챌린지 화면으로 리다이렉트합니다. XHR로 로그인 시도한 경우, 응답 JSON에 `two_factor` 불리언 값이 포함되어 있으니, 이 값을 확인하여 2차 인증 챌린지 화면으로 리다이렉트할지 판단하면 됩니다.

이를 구현하려면 Fortify가 2차 인증 챌린지 뷰를 반환하도록 지정해 주어야 합니다. 이 역시 `Laravel\Fortify\Fortify` 클래스의 메서드로 커스터마이즈하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 작성합니다.

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

Fortify는 `/two-factor-challenge` 라우트를 정의하여 해당 뷰를 반환합니다. `two-factor-challenge` 템플릿은 `/two-factor-challenge`로 POST 요청하는 폼을 포함해야 하며, 유효한 TOTP 토큰이 담긴 `code` 필드나, 복구 코드가 담긴 `recovery_code` 필드를 전달해야 합니다.

로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉트하며, XHR 요청 시 204 HTTP 응답을 반환합니다.

인증 실패 시, 사용자는 2차 인증 챌린지 화면으로 리다이렉트되며, 검증 에러는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)에 담겨 있습니다. XHR 요청인 경우엔 422 HTTP 에러가 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
### 2차 인증 비활성화 (Disabling Two-Factor Authentication)

2차 인증을 비활성화하려면, 애플리케이션이 `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내야 합니다. 참고로 Fortify의 2차 인증 관련 엔드포인트는 [비밀번호 재확인](#password-confirmation)이 선행되어야 호출할 수 있습니다.

<a name="registration"></a>
## 사용자 등록 (Registration)

애플리케이션의 사용자 등록 기능을 구현하려면, Fortify가 "회원가입" 뷰를 반환하는 방법을 지정해야 합니다. Fortify는 UI가 없는 헤드리스 인증 라이브러리입니다. 이미 완성된 인증 UI를 적용하려면 [애플리케이션 스타터 킷](/docs/master/starter-kits)이 적합합니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 활용해 커스터마이즈할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 사용합니다.

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

Fortify는 `/register` 라우트를 정의하여 이 뷰를 반환합니다. `register` 템플릿에는 Fortify가 정의한 `/register` 엔드포인트에 POST 요청하는 폼이 포함되어야 합니다.

`/register` 엔드포인트에는 문자열 타입의 `name`, 이메일 또는 아이디, `password`, `password_confirmation` 필드가 필요합니다. 이메일/아이디 필드명은 애플리케이션 `fortify` 설정 파일의 `username` 값과 일치해야 합니다.

등록이 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리다이렉트하며, XHR 요청은 201 HTTP 응답을 반환합니다.

등록이 실패하면 사용자는 다시 회원가입 화면으로 리다이렉트되며, 검증 에러는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)로 접근하고, XHR 요청 시 422 HTTP 에러가 반환됩니다.

<a name="customizing-registration"></a>
### 사용자 등록 커스터마이즈 (Customizing Registration)

사용자 검증 및 생성 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
## 비밀번호 재설정 (Password Reset)

<a name="requesting-a-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting a Password Reset Link)

비밀번호 재설정 기능을 구현하기 위해서, 먼저 Fortify가 "비밀번호 찾기" 뷰를 반환하도록 지정해야 합니다. Fortify는 UI를 제공하지 않는 헤드리스 인증 라이브러리이기 때문에, UI가 완비된 인증이 필요하다면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용하면 됩니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드로 커스터마이즈하며, `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 구현할 수 있습니다.

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

Fortify는 `/forgot-password` 엔드포인트를 정의하여 이 뷰를 반환합니다. `forgot-password` 템플릿에는 Fortify가 정의한 `/forgot-password` 엔드포인트로 POST 요청을 보내는 폼이 있어야 합니다.

`/forgot-password` 엔드포인트에는 문자열 타입의 `email` 필드가 필요합니다. 이 필드나 DB 컬럼의 이름은 애플리케이션 `fortify` 설정 파일의 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
#### 비밀번호 재설정 링크 요청 응답 처리

비밀번호 재설정 링크 요청이 성공하면, Fortify는 사용자를 `/forgot-password` 엔드포인트로 리다이렉트하고, 사용자에게 비밀번호 재설정 링크가 포함된 이메일을 보냅니다. XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

성공적으로 요청을 마친 후 `/forgot-password` 페이지로 돌아오면, `status` 세션 변수를 활용해 결과 메시지를 화면에 표시할 수 있습니다.

`$status` 세션 변수의 값은 애플리케이션 `passwords` [언어 파일](/docs/master/localization)에 정의된 번역 문자열 중 하나와 일치합니다. 값을 커스터마이즈하고 싶은데 라라벨 언어 파일이 퍼블리시되어 있지 않다면, `lang:publish` 아티즌 명령어를 사용할 수 있습니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

요청이 실패하면, 사용자는 다시 비밀번호 재설정 링크 요청 화면으로 리다이렉트되며, 검증 에러는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)를 통해 접근할 수 있습니다. XHR 요청의 경우 422 HTTP 응답이 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

비밀번호 재설정 기능을 마무리하기 위해, Fortify가 "비밀번호 재설정" 뷰를 반환하도록 지정해야 합니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드로 커스터마이즈하며, 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 구현합니다.

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

Fortify는 이 뷰를 렌더링하는 라우트를 자동으로 정의합니다. `reset-password` 템플릿에는 `/reset-password` 엔드포인트로 POST 요청을 보내는 폼이 필요합니다.

`/reset-password` 엔드포인트에는 문자열 타입의 `email`, `password`, `password_confirmation` 필드와, 숨김 필드로 `token`(값은 `request()->route('token')`)이 필요합니다. "이메일" 필드명이나 DB 컬럼명은 애플리케이션 `fortify` 설정 파일에 정의된 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 `/login` 라우트로 리다이렉트해, 사용자가 새 비밀번호로 로그인할 수 있도록 합니다. 또한 `status` 세션 변수를 통해 재설정 성공 메시지를 로그인 화면에 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

XHR 요청의 경우 200 HTTP 응답이 반환됩니다.

요청이 실패하면 사용자는 다시 비밀번호 재설정 화면으로 리다이렉트되고, 검증 에러는 `$errors` [Blade 템플릿 변수](/docs/master/validation#quick-displaying-the-validation-errors)를 통해 접근할 수 있습니다. XHR 요청 시 422 HTTP 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
### 비밀번호 재설정 커스터마이즈 (Customizing Password Resets)

비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
## 이메일 인증 (Email Verification)

회원가입 후, 사용자가 애플리케이션을 계속 사용하려면 이메일 인증을 요구할 수 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에 `emailVerification`이 활성화되어 있는지 확인하세요. 그 다음, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하고 있는지 확인해야 합니다.

이 두 단계를 완료하면, 새롭게 회원가입한 사용자에게 이메일 인증 링크가 포함된 메일이 자동 발송됩니다. 하지만, 사용자가 이메일 인증 링크를 클릭해야 한다고 안내하는 화면이 필요하므로, Fortify가 해당 뷰를 렌더링하도록 지정해 주어야 합니다.

모든 Fortify 인증 뷰 렌더링은 `Laravel\Fortify\Fortify`의 메서드를 이용해 커스터마이즈할 수 있으며, 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 다음과 같이 지정합니다.

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

Fortify는 사용자가 Laravel의 기본 제공 `verified` 미들웨어에 의해 `/email/verify` 엔드포인트로 리다이렉트될 때, 이 뷰를 렌더링하는 라우트를 정의합니다.

`verify-email` 템플릿에는 이메일로 전송된 인증 링크를 클릭하라는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
#### 이메일 인증 링크 재발송 (Resending Email Verification Links)

필요하다면, `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트로 POST 요청하는 버튼을 추가할 수 있습니다. 이 요청이 들어오면 Fortify가 새로운 인증 메일을 다시 전송하며, 사용자가 이전 링크를 실수로 삭제했거나 분실한 경우 다시 인증할 기회를 제공합니다.

이메일 인증 링크 재발송 요청이 성공하면 Fortify는 사용자를 `/email/verify` 엔드포인트로 리다이렉트하고, `status` 세션 변수를 통해 결과 메시지를 표시할 수 있습니다. XHR 요청의 경우 202 HTTP 응답을 반환합니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### 라우트 보호 (Protecting Routes)

특정 라우트 또는 라우트 그룹에 대해 사용자의 이메일 인증이 필수인 경우, 라라벨 내장 `verified` 미들웨어를 해당 라우트에 적용해야 합니다. 이 미들웨어는 자동으로 등록되며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## 비밀번호 재확인 (Password Confirmation)

애플리케이션을 개발하다 보면, 사용자가 특정 행동을 취하기 전 비밀번호를 다시 한 번 확인해야 할 때가 있습니다. 보통 이러한 경로는 라라벨 내장 `password.confirm` 미들웨어로 보호합니다.

비밀번호 재확인 기능을 구현하려면, Fortify가 애플리케이션의 "비밀번호 재확인" 뷰를 반환하도록 지정해야 합니다. Fortify는 UI가 없는 헤드리스 인증 라이브러리이며, 완성된 인증 UI가 필요하다면 [애플리케이션 스타터 킷](/docs/master/starter-kits)을 사용할 수 있습니다.

Fortify의 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드에서 커스터마이즈할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 다음과 같이 지정합니다.

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

Fortify는 `/user/confirm-password` 엔드포인트를 정의하여 이 뷰를 반환합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트로 POST 요청하는 폼이 포함되어야 하며, 현재 비밀번호가 담긴 `password` 필드를 기대합니다.

비밀번호가 현재 비밀번호와 일치하면, Fortify는 사용자가 접근하려 했던 경로로 리다이렉트합니다. XHR 요청의 경우 201 HTTP 응답을 반환합니다.

요청이 실패하면 사용자는 다시 비밀번호 재확인 화면으로 리다이렉트되며, 검증 에러는 공유된 `$errors` Blade 템플릿 변수로 접근하거나, XHR 요청의 경우 422 HTTP 에러를 반환합니다.
