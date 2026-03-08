# 이메일 인증 (Email Verification)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 알림](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호하기](#protecting-routes)
- [커스터마이징](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 매번 이러한 기능을 손수 재구현하는 대신, Laravel은 이메일 인증 요청을 보내고 처리하는 편리한 내장 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits) 중 하나를 설치해 보세요. 이 스타터 키트는 이메일 인증 지원을 포함해 전체 인증 시스템 구성을 자동으로 처리해 줍니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

먼저, `App\Models\User` 모델에서 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현했는지 확인하세요:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}
```

이 인터페이스를 모델에 추가하면, 새로 가입하는 사용자에게 자동으로 이메일 인증 링크가 포함된 이메일이 발송됩니다. 이는 Laravel이 자동으로 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/master/events)를 등록하기 때문에 무리 없이 처리됩니다.

만약 [스타터 키트](/docs/master/starter-kits)를 사용하지 않고 직접 회원가입 기능을 구현하는 경우, 사용자가 성공적으로 등록된 후에 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 발생시키는지 확인해야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비 (Database Preparation)

다음으로, `users` 테이블에 사용자의 이메일 인증 시점(날짜와 시간)을 저장할 `email_verified_at` 컬럼이 있어야 합니다. 이 컬럼은 보통 Laravel 기본 마이그레이션 파일인 `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅 (Routing)

이메일 인증을 제대로 구현하려면 세 가지 라우트를 정의해야 합니다. 첫째, 사용자가 가입 후 Laravel에서 보낸 인증 이메일의 링크를 클릭해야 한다는 알림 화면을 보여줄 라우트가 필요합니다.

둘째, 사용자가 이메일에서 인증 링크를 클릭했을 때 요청을 처리할 라우트가 필요합니다.

셋째, 사용자가 인증 링크를 잃어버렸을 때 재전송 요청을 처리할 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림 (The Email Verification Notice)

앞서 언급한 것처럼, 사용자가 가입 후 Laravel에서 보낸 인증 이메일의 링크를 클릭하도록 안내하는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증을 완료하지 않고 애플리케이션의 다른 부분에 접근하려 시도할 때 보여줍니다. 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면 자동으로 사용자에게 이메일로 발송됩니다:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이 이메일 인증 알림을 반환하는 라우트의 이름은 반드시 `verification.notice`로 지정해야 합니다. `verified` 미들웨어가 이메일을 인증하지 않은 사용자를 자동으로 이 이름의 라우트로 리다이렉트하기 때문입니다.

> [!NOTE]
> 이메일 인증을 직접 구현하는 경우, 인증 알림 뷰 내용을 직접 정의해야 합니다. 인증과 관련된 모든 뷰가 포함된 기본 구성을 원한다면, [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기 (The Email Verification Handler)

다음으로, 사용자가 이메일 내 인증 링크를 클릭했을 때 요청을 처리할 라우트를 정의합니다. 이 라우트는 `verification.verify`라는 이름을 갖고 `auth`와 `signed` 미들웨어를 적용해야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 조금 더 자세히 살펴보면, 보통 `Illuminate\Http\Request` 대신에 `EmailVerificationRequest`라는 [폼 요청](/docs/master/validation#form-request-validation) 클래스를 사용하는 것을 알 수 있습니다. 이 요청 클래스는 `id`와 `hash` 파라미터를 자동으로 검증해 줍니다.

그리고 바로 `fulfill` 메서드를 호출합니다. 이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 호출하여 이메일 인증을 표시하고, `Illuminate\Auth\Events\Verified` 이벤트를 발생시킵니다. 기본 `App\Models\User` 모델은 `Illuminate\Foundation\Auth\User` 베이스 클래스를 통해 이 메서드를 제공합니다. 이메일 인증이 완료되면 원하는 경로로 리다이렉트하면 됩니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송 (Resending the Verification Email)

사용자가 인증 이메일을 잘못 삭제하거나 잃어버리는 경우가 있습니다. 이때 인증 이메일을 재전송해 줄 수 있는 라우트를 정의하면 좋습니다. 이 라우트는 간단한 폼 제출 버튼을 [이메일 인증 알림 뷰](#the-email-verification-notice)에 넣어 호출할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호하기 (Protecting Routes)

[라우트 미들웨어](/docs/master/middleware)를 사용하면 이메일 인증이 완료된 사용자만 특정 라우트에 접근하도록 제한할 수 있습니다. Laravel은 `verified`라는 미들웨어 별칭을 기본 제공하는데, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스에 대한 별칭입니다. 이 별칭은 Laravel에서 이미 자동 등록되므로, 라우트 정의 시 해당 미들웨어만 추가하면 됩니다. 보통 `auth` 미들웨어와 함께 사용합니다:

```php
Route::get('/profile', function () {
    // 이메일 인증 완료 사용자만 접근 가능...
})->middleware(['auth', 'verified']);
```

이메일 인증하지 않은 사용자가 이 미들웨어가 붙은 라우트에 접근하려 하면 자동으로 `verification.notice` [이름 있는 라우트](/docs/master/routing#named-routes)로 리다이렉트합니다.

<a name="customization"></a>
## 커스터마이징 (Customization)

<a name="verification-email-customization"></a>
#### 인증 이메일 커스터마이징 (Verification Email Customization)

기본 제공되는 이메일 인증 알림으로 대부분의 애플리케이션 요구 사항을 충족할 수 있지만, Laravel은 이메일 전송 메시지를 어떻게 구성할지 커스터마이징할 수 있도록 허용합니다.

먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스에서 제공하는 `toMailUsing` 메서드에 클로저를 전달합니다. 이 클로저는 알림을 받는 모델 인스턴스와 사용자가 방문해 이메일을 인증할 서명된 URL을 인수로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 보통 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 `toMailUsing`을 호출합니다:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]
> 메일 알림에 대해 더 자세히 알고 싶다면, [메일 알림 문서](/docs/master/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

[Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용할 경우, 이메일 인증 과정에서 `Illuminate\Auth\Events\Verified` [이벤트](/docs/master/events)가 자동으로 발생합니다. 직접 이메일 인증 기능을 구현하는 경우에는 인증 완료 후 이 이벤트들을 직접 발생시키는 것이 좋습니다.