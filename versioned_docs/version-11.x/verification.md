<!-- # Email Verification -->
# Email Verification

- [Introduction](#introduction)
    - [Model Preparation](#model-preparation)
    - [Database Preparation](#database-preparation)
- [Routing](#verification-routing)
    - [The Email Verification Notice](#the-email-verification-notice)
    - [The Email Verification Handler](#the-email-verification-handler)
    - [Resending the Verification Email](#resending-the-verification-email)
    - [Protecting Routes](#protecting-routes)
- [Customization](#customization)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this feature by hand for each application you create, Laravel provides convenient built-in services for sending and verifying email verification requests. -->
많은 웹 애플리케이션에서는 사용자에게 애플리케이션을 사용하기 전에 이메일 주소를 인증하도록 요구합니다. Laravel은 이 기능을 애플리케이션마다 직접 구현할 필요 없이, 이메일 인증 요청의 전송과 검증을 간편하게 처리할 수 있는 내장 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel application starter kits](/docs/11.x/starter-kits)를 설치해 보세요. 스타터 키트는 이메일 인증 지원을 포함하여 전체 인증 시스템을 자동으로 구성해줍니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before getting started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract: -->
시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약을 구현하고 있는지 확인해야 합니다:

```
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

<!-- Once this interface has been added to your model, newly registered users will automatically be sent an email containing an email verification link. This happens seamlessly because Laravel automatically registers the `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [listener](/docs/11.x/events) for the `Illuminate\Auth\Events\Registered` event. -->
이 인터페이스를 모델에 추가하면, 새로 등록된 사용자에게 자동으로 이메일 인증 링크가 포함된 이메일이 전송됩니다. 이는 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [listener](/docs/11.x/events)를 자동으로 등록하기 때문에 별도의 작업 없이 처리됩니다.

<!-- If you are manually implementing registration within your application instead of using [a starter kit](/docs/11.x/starter-kits), you should ensure that you are dispatching the `Illuminate\Auth\Events\Registered` event after a user's registration is successful: -->
만약 [a starter kit](/docs/11.x/starter-kits)가 아닌 직접 회원가입 로직을 구현하고 있다면, 사용자의 회원가입이 성공적으로 이루어진 후 `Illuminate\Auth\Events\Registered` 이벤트를 반드시 디스패치해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- Next, your `users` table must contain an `email_verified_at` column to store the date and time that the user's email address was verified. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` database migration. -->
다음으로, 사용자가 이메일 주소를 인증한 날짜와 시간을 저장하기 위해 `users` 테이블에 `email_verified_at` 컬럼이 존재해야 합니다. 보통 이는 Laravel의 기본 마이그레이션 파일인 `0001_01_01_000000_create_users_table.php`에 이미 포함되어 있습니다.

<a name="verification-routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement email verification, three routes will need to be defined. First, a route will be needed to display a notice to the user that they should click the email verification link in the verification email that Laravel sent them after registration. -->
이메일 인증을 제대로 구현하려면 총 세 개의 라우트를 정의해야 합니다.
첫 번째로, 사용자가 회원가입 후 Laravel이 보낸 이메일 인증 링크를 클릭하도록 안내하는 알림을 보여주는 라우트가 필요합니다.

<!-- Second, a route will be needed to handle requests generated when the user clicks the email verification link in the email. -->
두 번째로, 사용자가 이메일 내의 인증 링크를 클릭했을 때 처리를 담당하는 라우트가 필요합니다.

<!-- Third, a route will be needed to resend a verification link if the user accidentally loses the first verification link. -->
세 번째로, 사용자가 처음 받은 인증 링크를 잃어버렸을 때 재전송을 요청할 수 있는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
<!-- ### The Email Verification Notice -->
### The Email Verification Notice

<!-- As mentioned previously, a route should be defined that will return a view instructing the user to click the email verification link that was emailed to them by Laravel after registration. This view will be displayed to users when they try to access other parts of the application without verifying their email address first. Remember, the link is automatically emailed to the user as long as your `App\Models\User` model implements the `MustVerifyEmail` interface: -->
앞서 언급한 것처럼, 사용자가 회원가입 후 이메일로 전달받은 인증 링크를 클릭하라는 안내 메시지를 보여주는 뷰를 반환하는 라우트를 정의해야 합니다. 이 뷰는 사용자가 이메일 인증을 완료하지 않은 상태에서 애플리케이션의 다른 영역에 접근하려 할 때 표시됩니다. 참고로, `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면 인증 링크는 사용자에게 자동으로 발송됩니다.

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

<!-- The route that returns the email verification notice should be named `verification.notice`. It is important that the route is assigned this exact name since the `verified` middleware [included with Laravel](#protecting-routes) will automatically redirect to this route name if a user has not verified their email address. -->
이메일 인증 알림을 반환하는 라우트의 이름은 반드시 `verification.notice`여야 합니다. 이 이름이 중요한 이유는, Laravel에 포함된 `verified` 미들웨어([included with Laravel](#protecting-routes))가 사용자가 이메일을 인증하지 않았을 경우 자동으로 이 라우트로 리다이렉트하기 때문입니다.

> [!NOTE]
> 이메일 인증을 직접 구현하는 경우 인증 알림 뷰의 내용을 직접 정의해야 합니다. 인증과 이메일 인증에 필요한 모든 뷰가 자동으로 제공되기를 원한다면 [Laravel application starter kits](/docs/11.x/starter-kits)를 참고해 주세요.

<a name="the-email-verification-handler"></a>
<!-- ### The Email Verification Handler -->
### The Email Verification Handler

<!-- Next, we need to define a route that will handle requests generated when the user clicks the email verification link that was emailed to them. This route should be named `verification.verify` and be assigned the `auth` and `signed` middlewares: -->
다음으로, 사용자에게 이메일로 전송된 인증 링크를 클릭할 때 처리를 담당하는 라우트를 정의해야 합니다. 이 라우트의 이름은 `verification.verify`여야 하며, `auth`와 `signed` 미들웨어가 적용되어야 합니다.

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

<!-- Before moving on, let's take a closer look at this route. First, you'll notice we are using an `EmailVerificationRequest` request type instead of the typical `Illuminate\Http\Request` instance. The `EmailVerificationRequest` is a [form request](/docs/11.x/validation#form-request-validation) that is included with Laravel. This request will automatically take care of validating the request's `id` and `hash` parameters. -->
여기서, 이 라우트를 자세히 살펴보면 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest`를 사용하고 있다는 점을 알 수 있습니다.
`EmailVerificationRequest`는 Laravel에 기본 제공되는 [form request](/docs/11.x/validation#form-request-validation)로, 전달받은 `id`와 `hash` 파라미터의 유효성을 자동으로 검증해줍니다.

<!-- Next, we can proceed directly to calling the `fulfill` method on the request. This method will call the `markEmailAsVerified` method on the authenticated user and dispatch the `Illuminate\Auth\Events\Verified` event. The `markEmailAsVerified` method is available to the default `App\Models\User` model via the `Illuminate\Foundation\Auth\User` base class. Once the user's email address has been verified, you may redirect them wherever you wish. -->
그 다음, 요청 객체의 `fulfill` 메서드를 호출하는 것으로 인증 처리를 바로 진행할 수 있습니다.
이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 호출하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다.
`markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델의 부모 클래스인 `Illuminate\Foundation\Auth\User`를 통해 제공됩니다.
사용자의 이메일 인증이 완료되면 원하는 경로로 자유롭게 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
<!-- ### Resending the Verification Email -->
### Resending the Verification Email

<!-- Sometimes a user may misplace or accidentally delete the email address verification email. To accommodate this, you may wish to define a route to allow the user to request that the verification email be resent. You may then make a request to this route by placing a simple form submission button within your [verification notice view](#the-email-verification-notice): -->
사용자가 이메일 인증 메일을 분실하거나 실수로 삭제하는 경우가 있을 수 있습니다.
이럴 때 사용자가 인증 이메일을 다시 받을 수 있도록 별도의 라우트를 정의할 수 있습니다.
[verification notice view](#the-email-verification-notice)에 간단한 폼 버튼을 만들어 이 라우트로 요청을 보낼 수 있습니다.

```
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/11.x/middleware) may be used to only allow verified users to access a given route. Laravel includes a `verified` [middleware alias](/docs/11.x/middleware#middleware-aliases), which is an alias for the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` middleware class. Since this alias is already automatically registered by Laravel, all you need to do is attach the `verified` middleware to a route definition. Typically, this middleware is paired with the `auth` middleware: -->
[Route middleware](/docs/11.x/middleware)를 사용하면 인증을 마친 사용자만 특정 라우트에 접근할 수 있도록 할 수 있습니다.
Laravel에는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스의 별칭인 `verified` [middleware alias](/docs/11.x/middleware#middleware-aliases)이 기본으로 등록되어 있습니다.
따라서 `verified` 미들웨어를 라우트에 추가하기만 하면 됩니다. 보통 `auth` 미들웨어와 함께 사용합니다.

```
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);
```

<!-- If an unverified user attempts to access a route that has been assigned this middleware, they will automatically be redirected to the `verification.notice` [named route](/docs/11.x/routing#named-routes). -->
아직 이메일 인증을 하지 않은 사용자가 이 미들웨어가 적용된 라우트에 접근할 경우, 자동으로 `verification.notice` [named route](/docs/11.x/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
<!-- ## Customization -->
## Customization

<a name="verification-email-customization"></a>
<!-- #### Verification Email Customization -->
#### Verification Email Customization

<!-- Although the default email verification notification should satisfy the requirements of most applications, Laravel allows you to customize how the email verification mail message is constructed. -->
기본 이메일 인증 알림은 대부분의 애플리케이션 요구 사항을 충족하지만, Laravel은 이메일 인증 메일의 내용을 커스터마이즈할 수 있는 기능도 제공합니다.

<!-- To get started, pass a closure to the `toMailUsing` method provided by the `Illuminate\Auth\Notifications\VerifyEmail` notification. The closure will receive the notifiable model instance that is receiving the notification as well as the signed email verification URL that the user must visit to verify their email address. The closure should return an instance of `Illuminate\Notifications\Messages\MailMessage`. Typically, you should call the `toMailUsing` method from the `boot` method of your application's `AppServiceProvider` class: -->
먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저를 전달해 주세요.
이 클로저는 알림을 받는 모델 인스턴스와, 사용자가 이메일 인증을 위해 방문해야 하는 서명된 이메일 인증 URL을 매개변수로 받습니다.
클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.
보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 `toMailUsing` 메서드를 호출합니다.

```
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
> 메일 알림에 대해 더 자세한 내용이 궁금하다면 [mail notification documentation](/docs/11.x/notifications#mail-notifications)를 참고해 주세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- When using the [Laravel application starter kits](/docs/11.x/starter-kits), Laravel dispatches an `Illuminate\Auth\Events\Verified` [event](/docs/11.x/events) during the email verification process. If you are manually handling email verification for your application, you may wish to manually dispatch these events after verification is completed. -->
[Laravel application starter kits](/docs/11.x/starter-kits)를 사용하는 경우, Laravel은 이메일 인증 과정에서 `Illuminate\Auth\Events\Verified` [event](/docs/11.x/events)를 자동으로 디스패치합니다. 애플리케이션에서 이메일 인증 과정을 직접 구현할 때도, 인증 완료 후 해당 이벤트를 수동으로 디스패치하는 것이 필요할 수 있습니다.
