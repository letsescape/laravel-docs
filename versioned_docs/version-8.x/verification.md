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
많은 웹 애플리케이션에서는 사용자가 서비스를 이용하기 전에 이메일 주소를 인증하도록 요구합니다. Laravel을 사용하면, 매번 직접 이 기능을 구현하지 않아도 되도록 이메일 인증 요청 전송과 검증을 쉽게 처리할 수 있는 내장 서비스를 제공합니다.

> [!TIP]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel application starter kits](/docs/8.x/starter-kits)를 설치해보세요. 이 스타터 키트는 이메일 인증을 포함한 전체 인증 시스템을 손쉽게 구축해줍니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before getting started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract: -->
시작하기 전에, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약(Contract)을 구현하는지 확인해야 합니다:

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

<!-- Once this interface has been added to your model, newly registered users will automatically be sent an email containing an email verification link. As you can see by examining your application's `App\Providers\EventServiceProvider`, Laravel already contains a `SendEmailVerificationNotification` [listener](/docs/8.x/events) that is attached to the `Illuminate\Auth\Events\Registered` event. This event listener will send the email verification link to the user. -->
이 인터페이스를 모델에 추가하면, 새로 가입한 사용자에게는 이메일 인증 링크가 담긴 이메일이 자동으로 전송됩니다. `App\Providers\EventServiceProvider` 파일을 살펴보면, Laravel에는 이미 `Illuminate\Auth\Events\Registered` 이벤트에 연결된 `SendEmailVerificationNotification` [listener](/docs/8.x/events)가 포함되어 있음을 알 수 있습니다. 이 이벤트 리스너가 사용자에게 이메일 인증 링크를 발송하는 역할을 합니다.

<!-- If you are manually implementing registration within your application instead of using [a starter kit](/docs/8.x/starter-kits), you should ensure that you are dispatching the `Illuminate\Auth\Events\Registered` event after a user's registration is successful: -->
만약 [a starter kit](/docs/8.x/starter-kits) 없이 직접 회원 가입 기능을 구현하고 있다면, 사용자가 회원가입을 마친 뒤 반드시 `Illuminate\Auth\Events\Registered` 이벤트를 발생시키는 코드를 추가해야 합니다:

```
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- Next, your `users` table must contain an `email_verified_at` column to store the date and time that the user's email address was verified. By default, the `users` table migration included with the Laravel framework already includes this column. So, all you need to do is run your database migrations: -->
다음으로, 사용자의 이메일 인증 시각을 저장할 수 있도록 `users` 테이블에 `email_verified_at` 컬럼이 있어야 합니다. 기본적으로 Laravel이 제공하는 `users` 테이블 마이그레이션에는 이 컬럼이 이미 포함되어 있습니다. 그러므로 데이터베이스 마이그레이션만 실행하면 됩니다:

```
php artisan migrate
```

<a name="verification-routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement email verification, three routes will need to be defined. First, a route will be needed to display a notice to the user that they should click the email verification link in the verification email that Laravel sent them after registration. -->
이메일 인증을 제대로 구현하려면, 세 가지 라우트를 정의해야 합니다.
첫 번째로, 사용자가 이메일로 받은 인증 링크를 클릭해야 한다는 안내 메시지를 보여주는 라우트가 필요합니다.

<!-- Second, a route will be needed to handle requests generated when the user clicks the email verification link in the email. -->
두 번째로, 사용자가 이메일에 포함된 인증 링크를 클릭했을 때 요청을 처리하는 라우트가 필요합니다.

<!-- Third, a route will be needed to resend a verification link if the user accidentally loses the first verification link. -->
세 번째로, 사용자가 인증 링크를 실수로 잃어버렸을 경우 인증 링크를 다시 보낼 수 있도록 도와주는 라우트가 필요합니다.

<a name="the-email-verification-notice"></a>
<!-- ### The Email Verification Notice -->
### The Email Verification Notice

<!-- As mentioned previously, a route should be defined that will return a view instructing the user to click the email verification link that was emailed to them by Laravel after registration. This view will be displayed to users when they try to access other parts of the application without verifying their email address first. Remember, the link is automatically emailed to the user as long as your `App\Models\User` model implements the `MustVerifyEmail` interface: -->
앞서 언급한 것처럼, 회원가입 후 Laravel이 이메일로 전송한 인증 링크를 클릭하라는 안내 메시지를 보여주는 라우트를 정의해야 합니다. 사용자가 이메일 인증을 하지 않고 애플리케이션 내 다른 페이지에 접근하려 할 때 이 뷰가 표시됩니다. 이메일 인증 링크는 `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하고 있다면 자동으로 발송됩니다:

```
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

<!-- The route that returns the email verification notice should be named `verification.notice`. It is important that the route is assigned this exact name since the `verified` middleware [included with Laravel](#protecting-routes) will automatically redirect to this route name if a user has not verified their email address. -->
이메일 인증 알림을 반환하는 라우트의 이름은 반드시 `verification.notice`로 지정해야 합니다. 이는 [included with Laravel](#protecting-routes)에서 다루는 Laravel의 `verified` 미들웨어가, 사용자가 이메일 인증을 하지 않았다면 자동으로 이 이름의 라우트로 리다이렉트하기 때문입니다.

> [!TIP]
> 이메일 인증을 직접 구현할 경우, 인증 알림 뷰의 내용을 개발자가 직접 정의해야 합니다. 인증 및 이메일 인증 관련 모든 페이지가 포함된 자동화된 구조가 필요하다면 [Laravel application starter kits](/docs/8.x/starter-kits)를 참고하세요.

<a name="the-email-verification-handler"></a>
<!-- ### The Email Verification Handler -->
### The Email Verification Handler

<!-- Next, we need to define a route that will handle requests generated when the user clicks the email verification link that was emailed to them. This route should be named `verification.verify` and be assigned the `auth` and `signed` middlewares: -->
다음으로, 사용자가 이메일로 받은 인증 링크를 클릭할 때 발생하는 요청을 처리할 라우트를 정의해야 합니다. 이 라우트의 이름은 `verification.verify`로 지정하고, `auth`와 `signed` 미들웨어를 적용해야 합니다:

```
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

<!-- Before moving on, let's take a closer look at this route. First, you'll notice we are using an `EmailVerificationRequest` request type instead of the typical `Illuminate\Http\Request` instance. The `EmailVerificationRequest` is a [form request](/docs/8.x/validation#form-request-validation) that is included with Laravel. This request will automatically take care of validating the request's `id` and `hash` parameters. -->
이 라우트를 좀 더 자세히 살펴보면, 평소와는 달리 `Illuminate\Http\Request` 대신 `EmailVerificationRequest` 타입을 사용하고 있는 것을 알 수 있습니다. `EmailVerificationRequest`는 Laravel에 내장된 [form request](/docs/8.x/validation#form-request-validation)입니다. 이 폼 리퀘스트가 요청에 포함된 `id`와 `hash` 파라미터의 유효성을 자동으로 검사해줍니다.

<!-- Next, we can proceed directly to calling the `fulfill` method on the request. This method will call the `markEmailAsVerified` method on the authenticated user and dispatch the `Illuminate\Auth\Events\Verified` event. The `markEmailAsVerified` method is available to the default `App\Models\User` model via the `Illuminate\Foundation\Auth\User` base class. Once the user's email address has been verified, you may redirect them wherever you wish. -->
그다음, 요청 인스턴스의 `fulfill` 메서드를 바로 호출할 수 있습니다. 이 메서드는 인증된 유저의 `markEmailAsVerified` 메서드를 호출하고, 동시에 `Illuminate\Auth\Events\Verified` 이벤트를 발행합니다. `markEmailAsVerified` 메서드는 기본 `App\Models\User` 모델이 상속하는 `Illuminate\Foundation\Auth\User` 클래스에 포함되어 있습니다. 사용자의 이메일이 인증되고 나면, 원하는 페이지로 자유롭게 리다이렉트할 수 있습니다.

<a name="resending-the-verification-email"></a>
<!-- ### Resending The Verification Email -->
### Resending The Verification Email

<!-- Sometimes a user may misplace or accidentally delete the email address verification email. To accommodate this, you may wish to define a route to allow the user to request that the verification email be resent. You may then make a request to this route by placing a simple form submission button within your [verification notice view](#the-email-verification-notice): -->
사용자가 이메일 인증 메일을 실수로 잃어버렸거나 삭제한 경우도 있을 수 있습니다. 이런 상황을 대비해 인증 이메일을 다시 요청할 수 있는 라우트를 추가할 수 있습니다. 이 라우트는 [verification notice view](#the-email-verification-notice)에서 간단한 폼 버튼을 이용해 동작하도록 구성할 수 있습니다:

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

<!-- [Route middleware](/docs/8.x/middleware) may be used to only allow verified users to access a given route. Laravel ships with a `verified` middleware, which references the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` class. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/8.x/middleware)를 이용해, 이메일 인증이 완료된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel에는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 클래스를 참조하는 `verified` 미들웨어가 기본 제공됩니다. 이 미들웨어는 이미 애플리케이션의 HTTP 커널에 등록되어 있으므로, 라우트 정의 시 미들웨어만 지정해주면 됩니다:

```
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware('verified');
```

<!-- If an unverified user attempts to access a route that has been assigned this middleware, they will automatically be redirected to the `verification.notice` [named route](/docs/8.x/routing#named-routes). -->
아직 인증이 완료되지 않은 사용자가 이 미들웨어가 적용된 라우트에 접근하면, 자동으로 `verification.notice` [named route](/docs/8.x/routing#named-routes)로 리다이렉트됩니다.

<a name="customization"></a>
<!-- ## Customization -->
## Customization

<a name="verification-email-customization"></a>
<!-- #### Verification Email Customization -->
#### Verification Email Customization

<!-- Although the default email verification notification should satisfy the requirements of most applications, Laravel allows you to customize how the email verification mail message is constructed. -->
기본 제공되는 이메일 인증 알림은 대부분의 애플리케이션에 충분하지만, 이메일 메시지의 내용을 커스터마이즈할 수도 있습니다.

<!-- To get started, pass a closure to the `toMailUsing` method provided by the `Illuminate\Auth\Notifications\VerifyEmail` notification. The closure will receive the notifiable model instance that is receiving the notification as well as the signed email verification URL that the user must visit to verify their email address. The closure should return an instance of `Illuminate\Notifications\Messages\MailMessage`. Typically, you should call the `toMailUsing` method from the `boot` method of your application's `App\Providers\AuthServiceProvider` class: -->
먼저, `Illuminate\Auth\Notifications\VerifyEmail` 알림 클래스에서 제공하는 `toMailUsing` 메서드에 클로저(익명 함수)를 전달하면 됩니다. 이 클로저는 알림을 받을 대상 모델 인스턴스와, 사용자가 인증해야 할 서명된 이메일 인증 URL을 인자로 받습니다. 그리고 이 함수는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로, 이 코드는 애플리케이션의 `App\Providers\AuthServiceProvider` 클래스의 `boot` 메서드에서 `toMailUsing` 메서드를 호출하는 방식으로 작성하는 것이 좋습니다:

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

> [!TIP]
> 메일 알림에 대해 더 자세히 알고 싶다면, [mail notification documentation](/docs/8.x/notifications#mail-notifications)를 참고하세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- When using the [Laravel application starter kits](/docs/8.x/starter-kits), Laravel dispatches [events](/docs/8.x/events) during the email verification process. If you are manually handling email verification for your application, you may wish to manually dispatch these events after verification is completed. You may attach listeners to these events in your application's `EventServiceProvider`: -->
[Laravel application starter kits](/docs/8.x/starter-kits)를 사용할 때, Laravel은 이메일 인증 과정 중에 [events](/docs/8.x/events)를 발생시킵니다. 직접 인증 처리를 구현하는 경우에도, 인증 완료 후에 이러한 이벤트를 수동으로 발생시킬 수 있습니다. 애플리케이션의 `EventServiceProvider`에 리스너를 등록해서 원하는 동작을 연결할 수 있습니다:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Auth\Events\Verified' => [
        'App\Listeners\LogVerifiedUser',
    ],
];
```
