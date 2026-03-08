# 이메일 인증 (Email Verification)

- [소개](#introduction)
    - [모델 준비](#model-preparation)
    - [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
    - [이메일 인증 알림](#the-email-verification-notice)
    - [이메일 인증 처리기](#the-email-verification-handler)
    - [인증 이메일 재전송](#resending-the-verification-email)
    - [라우트 보호](#protecting-routes)
- [사용자 정의](#customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션은 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. 각 애플리케이션마다 이 기능을 직접 구현하도록 강요하지 않고, Laravel은 이메일 인증 요청을 보내고 검증할 수 있는 편리한 내장 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶다면, 새로운 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits) 중 하나를 설치하세요. 스타터 키트는 이메일 인증 지원을 포함한 전체 인증 시스템의 뼈대를 자동으로 구성해 줍니다.

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현하고 있는지 확인하세요:

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

이 인터페이스를 모델에 추가하면, 새로 등록되는 사용자에게 이메일 인증 링크가 포함된 이메일이 자동으로 발송됩니다. 이 과정은 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/12.x/events)를 자동으로 등록해 주기 때문에 자연스럽게 이루어집니다.

만약 [스타터 키트](/docs/12.x/starter-kits)를 사용하지 않고 애플리케이션 내에서 직접 회원가입을 구현하고 있다면, 회원가입이 성공한 후 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 직접 발생시켜야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로, `users` 테이블에 사용자의 이메일이 인증된 날짜와 시간을 저장할 `email_verified_at` 컬럼이 있어야 합니다. 보통 Laravel이 기본 제공하는 `0001_01_01_000000_create_users_table.php` 마이그레이션 파일에 포함되어 있습니다.

<a name="verification-routing"></a>
## 라우팅

이메일 인증을 적절히 구현하려면 세 가지 라우트를 정의해야 합니다. 첫 번째는 사용자가 회원가입 후 Laravel이 발송한 인증 이메일에서 인증 링크를 클릭하라는 알림을 표시하기 위한 라우트입니다.

두 번째는 사용자가 이메일 인증 링크를 클릭했을 때 요청을 처리하는 라우트입니다.

세 번째는 사용자가 처음 인증 링크를 분실했을 경우 인증 링크를 재전송해 주는 라우트입니다.

<a name="the-email-verification-notice"></a>
### 이메일 인증 알림

앞서 언급했듯, 회원가입 후 Laravel이 사용자에게 보낸 이메일 인증 링크를 클릭하라는 안내 페이지를 반환하는 라우트를 정의해야 합니다. 사용자가 이메일 인증을 하지 않고 애플리케이션의 다른 부분에 접근하려 할 때 이 뷰가 표시됩니다. 중요한 점은 이메일 인증 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있으면 사용자에게 자동 발송된다는 것입니다:

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

이 이메일 인증 알림을 반환하는 라우트는 `verification.notice`라는 이름을 가져야 합니다. 이 정확한 이름은 Laravel에 내장된 `verified` 미들웨어([라우트 보호](#protecting-routes) 참고)가 이메일 인증되지 않은 사용자를 자동으로 이 라우트로 리디렉션하기 때문에 매우 중요합니다.

> [!NOTE]
> 이메일 인증을 직접 구현하는 경우, 인증 알림 뷰의 내용을 직접 작성해야 합니다. 만약 모든 인증 및 인증 뷰가 포함된 뼈대 코드를 원한다면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
### 이메일 인증 처리기

다음은 사용자가 이메일 내 인증 링크를 클릭할 때 발생하는 요청을 처리할 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름을 가져야 하며 `auth`와 `signed` 미들웨어가 할당되어야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

이 라우트를 자세히 살펴보면, 일반적인 `Illuminate\Http\Request` 대신 `EmailVerificationRequest` 요청 타입을 사용하는 것을 볼 수 있습니다. `EmailVerificationRequest`는 Laravel에 포함된 [폼 요청](/docs/12.x/validation#form-request-validation)으로, 요청의 `id` 와 `hash` 파라미터를 자동으로 검증해 줍니다.

그다음, `fulfill` 메서드를 호출하여 인증을 완료합니다. 이 메서드는 인증된 사용자 객체의 `markEmailAsVerified` 메서드를 호출하고 `Illuminate\Auth\Events\Verified` 이벤트를 발생시킵니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델이 상속받는 `Illuminate\Foundation\Auth\User` 기본 클래스에서 제공합니다. 이메일 인증이 완료되면 원하는 경로로 리디렉션할 수 있습니다.

<a name="resending-the-verification-email"></a>
### 인증 이메일 재전송

때때로 사용자가 이메일 인증 메일을 분실하거나 실수로 삭제할 수 있습니다. 이를 대비해 인증 이메일을 재전송 요청할 수 있는 라우트를 정의할 수 있습니다. 사용자는 이 라우트로 폼 제출 버튼을 눌러 인증 이메일을 재요청할 수 있습니다([이메일 인증 알림](#the-email-verification-notice) 뷰에 폼 배치 가능):

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
### 라우트 보호

특정 라우트를 이메일 인증된 사용자만 접근할 수 있도록 [라우트 미들웨어](/docs/12.x/middleware)를 사용할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스에 대한 별칭인 `verified` 미들웨어를 기본 제공합니다. 이 별칭은 Laravel에서 자동 등록되므로, 라우트 정의에 단순히 `verified` 미들웨어를 추가하면 됩니다. 보통 `auth` 미들웨어와 함께 사용합니다:

```php
Route::get('/profile', function () {
    // 인증 완료된 사용자만 접근 가능...
})->middleware(['auth', 'verified']);
```

인증되지 않은 사용자가 이 미들웨어가 할당된 라우트에 접근하려 하면 자동으로 `verification.notice` [이름 있는 라우트](/docs/12.x/routing#named-routes)로 리디렉션됩니다.

<a name="customization"></a>
## 사용자 정의

<a name="verification-email-customization"></a>
#### 인증 이메일 사용자 정의

기본 이메일 인증 알림은 대부분 애플리케이션에 충분하지만, Laravel은 이메일 인증 메일 메시지 생성 방식을 사용자 정의할 수 있도록 지원합니다.

시작하려면 `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스가 제공하는 `toMailUsing` 메서드에 클로저를 전달하세요. 이 클로저는 알림을 받는 모델 인스턴스와 사용자가 이메일 주소를 인증하기 위해 방문해야 하는 서명된 이메일 인증 URL을 인수로 받습니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 보통 이 작업은 애플리케이션의 `AppServiceProvider` 클래스 내 `boot` 메서드에서 수행합니다:

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * 부트스트랩 애플리케이션 서비스.
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
> 메일 알림에 대해 더 알아보려면 [메일 알림 문서](/docs/12.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
## 이벤트

[Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, 이메일 인증 과정 중에 Laravel은 `Illuminate\Auth\Events\Verified` [이벤트](/docs/12.x/events)를 발송합니다. 만약 애플리케이션에서 이메일 인증을 수동으로 처리한다면, 인증 완료 후 이 이벤트를 수동으로 발생시키는 것도 고려해 보세요.