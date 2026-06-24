<!-- # Email Verification -->
# Email Verification

- [Introduction](#introduction)
    - [Model Preparation](#model-preparation)
    - [Database Preparation](#database-preparation)
- [Routing](#verification-routing)
    - [The Email Verification Notice](#the-email-verification-notice)
    - [The Email Verification Handler](#the-email-verification-handler)
    - [Resending The Verification Email](#resending-the-verification-email)
    - [Protecting Routes](#protecting-routes)
- [Customization](#customization)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications require users to verify their email addresses before using the application. Rather than forcing you to re-implement this feature by hand for each application you create, Laravel provides convenient built-in services for sending and verifying email verification requests. -->
많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 자신의 이메일 주소를 인증하도록 요구합니다. 이러한 기능을 매번 직접 구현하지 않도록, Laravel은 이메일 인증 요청을 보내고 처리하는 데 유용한 기본 제공 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로 설치된 Laravel 애플리케이션에서 [Laravel application starter kits](/docs/9.x/starter-kits) 중 하나를 설치해 보세요. 스타터 키트는 전체 인증 시스템, 그리고 이메일 인증 기능까지 모두 자동으로 구성해 줍니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before getting started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract: -->
시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약(인터페이스)을 구현하고 있는지 확인해야 합니다.

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

<!-- Once this interface has been added to your model, newly registered users will automatically be sent an email containing an email verification link. As you can see by examining your application's `App\Providers\EventServiceProvider`, Laravel already contains a `SendEmailVerificationNotification` [listener](/docs/9.x/events) that is attached to the `Illuminate\Auth\Events\Registered` event. This event listener will send the email verification link to the user. -->
이 인터페이스를 모델에 추가하면, 새로 회원가입한 사용자에게 이메일 인증 링크가 포함된 이메일이 자동으로 전송됩니다. 실제로 애플리케이션의 `App\Providers\EventServiceProvider`를 살펴보면, Laravel에는 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [listener](/docs/9.x/events)가 포함되어 있는 것을 확인할 수 있습니다. 이 이벤트 리스너가 사용자에게 이메일 인증 링크를 전송합니다.

<!-- If you are manually implementing registration within your application instead of using [a starter kit](/docs/9.x/starter-kits), you should ensure that you are dispatching the `Illuminate\Auth\Events\Registered` event after a user's registration is successful: -->
만약 [a starter kit](/docs/9.x/starter-kits)를 사용하지 않고 직접 회원가입 기능을 구현하는 경우, 사용자가 회원가입에 성공한 후 `Illuminate\Auth\Events\Registered` 이벤트가 반드시 디스패치(dispatch)되도록 해주어야 합니다.

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- Next, your `users` table must contain an `email_verified_at` column to store the date and time that the user's email address was verified. By default, the `users` table migration included with the Laravel framework already includes this column. So, all you need to do is run your database migrations: -->
다음으로, `users` 테이블에 사용자의 이메일 인증 시점(날짜와 시간)을 저장할 수 있도록 `email_verified_at` 컬럼이 있어야 합니다. 기본적으로 Laravel 프레임워크에 포함된 `users` 테이블 마이그레이션에는 이미 이 컬럼이 정의되어 있습니다. 따라서 데이터베이스 마이그레이션만 실행하면 됩니다.

```shell
php artisan migrate
```

<a name="verification-routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement email verification, three routes will need to be defined. First, a route will be needed to display a notice to the user that they should click the email verification link in the verification email that Laravel sent them after registration. -->
이메일 인증을 적절하게 구현하려면 세 가지 라우트를 정의해야 합니다. 첫 번째로, 회원가입 후 Laravel에서 전송한 인증 이메일 내의 링크를 클릭하라는 안내 화면을 사용자에게 보여주는 라우트가 필요합니다.

<!-- Second, a route will be needed to handle requests generated when the user clicks the email verification link in the email. -->
두 번째로, 사용자가 이메일에서 제공된 인증 링크를 클릭할 때 요청을 처리하는 라우트가 있어야 합니다.

<!-- Third, a route will be needed to resend a verification link if the user accidentally loses the first verification link. -->
세 번째로, 사용자가 실수로 인증 링크를 분실한 경우 인증 이메일을 다시 전송하는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
<!-- ### The Email Verification Notice -->
### The Email Verification Notice

<!-- As mentioned previously, a route should be defined that will return a view instructing the user to click the email verification link that was emailed to them by Laravel after registration. This view will be displayed to users when they try to access other parts of the application without verifying their email address first. Remember, the link is automatically emailed to the user as long as your `App\Models\User` model implements the `MustVerifyEmail` interface: -->
앞서 설명한 것처럼, 회원가입 후 Laravel에서 보낸 이메일 내 인증 링크를 클릭하라는 안내를 담은 뷰(view)를 반환하는 라우트를 정의해야 합니다. 사용자가 이메일 인증을 완료하지 않고 애플리케이션의 다른 부분에 접근하려고 할 때 이 뷰가 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면 이 링크는 자동으로 사용자에게 전송됩니다.

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

<!-- The route that returns the email verification notice should be named `verification.notice`. It is important that the route is assigned this exact name since the `verified` middleware [included with Laravel](#protecting-routes) will automatically redirect to this route name if a user has not verified their email address. -->
이메일 인증 안내 화면을 반환하는 라우트의 이름은 반드시 `verification.notice`여야 합니다. Laravel에 내장된 `verified` 미들웨어([included with Laravel](#protecting-routes))는 사용자가 이메일을 인증하지 않은 경우 자동으로 이 이름의 라우트로 리다이렉트하기 때문입니다.

> [!NOTE]
> 이메일 인증을 수동으로 직접 구현하는 경우, 인증 안내 화면의 뷰 내용을 직접 작성해야 합니다. 필요한 모든 인증 및 인증 관련 뷰가 포함된 기본 스캐폴딩이 필요하다면 [Laravel application starter kits](/docs/9.x/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
<!-- ### The Email Verification Handler -->
### The Email Verification Handler

<!-- Next, we need to define a route that will handle requests generated when the user clicks the email verification link that was emailed to them. This route should be named `verification.verify` and be assigned the `auth` and `signed` middlewares: -->
이제 사용자가 이메일로 받은 인증 링크를 클릭할 때 발생하는 요청을 처리하는 라우트를 정의해야 합니다. 이 라우트는 `verification.verify`라는 이름이어야 하며, `auth` 및 `signed` 미들웨어가 적용되어야 합니다.

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

<!-- Before moving on, let's take a closer look at this route. First, you'll notice we are using an `EmailVerificationRequest` request type instead of the typical `Illuminate\Http\Request` instance. The `EmailVerificationRequest` is a [form request](/docs/9.x/validation#form-request-validation) that is included with Laravel. This request will automatically take care of validating the request's `id` and `hash` parameters. -->
이 라우트를 자세히 살펴보면, 일반적으로 사용하는 `Illuminate\Http\Request` 대신에 `EmailVerificationRequest`를 파라미터로 사용합니다. `EmailVerificationRequest`는 Laravel에서 제공하는 [form request](/docs/9.x/validation#form-request-validation)으로, 해당 요청의 `id`와 `hash` 파라미터가 올바른지 자동으로 검증해 줍니다.

<!-- Next, we can proceed directly to calling the `fulfill` method on the request. This method will call the `markEmailAsVerified` method on the authenticated user and dispatch the `Illuminate\Auth\Events\Verified` event. The `markEmailAsVerified` method is available to the default `App\Models\User` model via the `Illuminate\Foundation\Auth\User` base class. Once the user's email address has been verified, you may redirect them wherever you wish. -->
그리고 나서, `fulfill` 메서드를 호출하여 인증 처리를 바로 할 수 있습니다. 이 메서드는 인증된 사용자에게 `markEmailAsVerified` 메서드를 실행하고, `Illuminate\Auth\Events\Verified` 이벤트를 디스패치합니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델이 상속하는 `Illuminate\Foundation\Auth\User` 클래스에서 제공됩니다. 이메일 인증이 완료되면 사용자를 원하는 위치로 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
<!-- ### Resending The Verification Email -->
### Resending The Verification Email

<!-- Sometimes a user may misplace or accidentally delete the email address verification email. To accommodate this, you may wish to define a route to allow the user to request that the verification email be resent. You may then make a request to this route by placing a simple form submission button within your [verification notice view](#the-email-verification-notice): -->
때때로 사용자가 인증 이메일을 실수로 분실하거나 삭제할 수 있습니다. 이를 위해, 사용자가 직접 인증 이메일을 다시 받을 수 있도록 하는 라우트를 정의할 수 있습니다. [verification notice view](#the-email-verification-notice) 뷰에 간단한 폼 전송 버튼을 추가하여 이 라우트로 요청을 보낼 수 있습니다.

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

<!-- [Route middleware](/docs/9.x/middleware) may be used to only allow verified users to access a given route. Laravel ships with a `verified` middleware, which references the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` class. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition. Typically, this middleware is paired with the `auth` middleware: -->
[Route middleware](/docs/9.x/middleware)를 사용하면 인증된 사용자 중 이메일 인증이 완료된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel에는 `verified`라는 미들웨어가 내장되어 있으며, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조합니다. 이 미들웨어는 이미 애플리케이션의 HTTP 커널에 등록되어 있으므로, 라우트 정의에서 미들웨어를 추가해주기만 하면 됩니다. 일반적으로 `auth` 미들웨어와 함께 사용됩니다.

```
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);
```

<!-- If an unverified user attempts to access a route that has been assigned this middleware, they will automatically be redirected to the `verification.notice` [named route](/docs/9.x/routing#named-routes). -->
이 미들웨어가 적용된 라우트에 이메일 인증을 완료하지 않은 사용자가 접근하면, 자동으로 `verification.notice` [named route](/docs/9.x/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
<!-- ## Customization -->
## Customization

<a name="verification-email-customization"></a>
<!-- #### Verification Email Customization -->
#### Verification Email Customization

<!-- Although the default email verification notification should satisfy the requirements of most applications, Laravel allows you to customize how the email verification mail message is constructed. -->
기본 제공되는 이메일 인증 알림만으로 대부분의 애플리케이션 요구사항을 충족할 수 있지만, Laravel에서는 이메일 인증 메일 메시지를 원하는 대로 커스터마이즈할 수도 있습니다.

<!-- To get started, pass a closure to the `toMailUsing` method provided by the `Illuminate\Auth\Notifications\VerifyEmail` notification. The closure will receive the notifiable model instance that is receiving the notification as well as the signed email verification URL that the user must visit to verify their email address. The closure should return an instance of `Illuminate\Notifications\Messages\MailMessage`. Typically, you should call the `toMailUsing` method from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
이를 위해, `Illuminate\Auth\Notifications\VerifyEmail` 노티피케이션에 있는 `toMailUsing` 메서드에 클로저를 전달하세요. 이 클로저는 알림을 받을 모델 인스턴스와 사용자가 방문해야 할 서명된(보안이 적용된) 이메일 인증 URL을 매개변수로 받습니다. 클로저에서는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드 내에서 `toMailUsing` 메서드를 호출해 설정합니다.

```
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    // ...

    VerifyEmail::toMailUsing(function ($notifiable, $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}
```

> [!NOTE]
> 메일 알림에 대해 더 자세히 알고 싶다면 [mail notification documentation](/docs/9.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- When using the [Laravel application starter kits](/docs/9.x/starter-kits), Laravel dispatches [events](/docs/9.x/events) during the email verification process. If you are manually handling email verification for your application, you may wish to manually dispatch these events after verification is completed. You may attach listeners to these events in your application's `EventServiceProvider`: -->
[Laravel application starter kits](/docs/9.x/starter-kits)를 사용할 때, Laravel은 이메일 인증 과정에서 [events](/docs/9.x/events)를 디스패치합니다. 만약 이메일 인증 과정을 직접 구현한다면, 인증 절차가 완료된 후 이러한 이벤트를 직접 디스패치할 수도 있습니다. `EventServiceProvider`에서 이러한 이벤트에 리스너를 등록하여 사용할 수 있습니다.

```
use App\Listeners\LogVerifiedUser;
use Illuminate\Auth\Events\Verified;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    Verified::class => [
        LogVerifiedUser::class,
    ],
];
```
