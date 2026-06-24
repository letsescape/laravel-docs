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
多くの Web アプリケーションでは、ユーザーはアプリケーションを使用する前に電子メール アドレスを確認する必要があります。 Laravel では、作成するアプリケーションごとにこの機能を手動で再実装する必要がなく、電子メール検証リクエストを送信および検証するための便利な組み込みサービスが提供されます。

> [!NOTE]
> すぐに始めたいですか?新しい Laravel アプリケーションに [Laravel application starter kits](/docs/13.x/starter-kits) の 1 つをインストールします。スターター キットは、電子メール検証サポートを含む認証システム全体の足場を処理します。

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before getting started, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\MustVerifyEmail` contract: -->
開始する前に、`App\Models\User` モデルが `Illuminate\Contracts\Auth\MustVerifyEmail` コントラクトを実装していることを確認してください。

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

<!-- Once this interface has been added to your model, newly registered users will automatically be sent an email containing an email verification link. This happens seamlessly because Laravel automatically registers the `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [listener](/docs/13.x/events) for the `Illuminate\Auth\Events\Registered` event. -->
このインターフェースがモデルに追加されると、新規登録ユーザーには、電子メール検証リンクを含む電子メールが自動的に送信されます。 Laravel は `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [listener](/docs/13.x/events) を `Illuminate\Auth\Events\Registered` イベントに自動的に登録するため、これはシームレスに行われます。

<!-- If you are manually implementing registration within your application instead of using [a starter kit](/docs/13.x/starter-kits), you should ensure that you are dispatching the `Illuminate\Auth\Events\Registered` event after a user's registration is successful: -->
[a starter kit](/docs/13.x/starter-kits) を使用する代わりにアプリケーション内で登録を手動で実装している場合は、ユーザーの登録が成功した後に `Illuminate\Auth\Events\Registered` イベントをディスパッチしていることを確認する必要があります。

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));
```

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- Next, your `users` table must contain an `email_verified_at` column to store the date and time that the user's email address was verified. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` database migration. -->
次に、`users` テーブルには、ユーザーの電子メール アドレスが検証された日時を保存する `email_verified_at` 列が含まれている必要があります。通常、これはLaravelのデフォルトの`0001_01_01_000000_create_users_table.php`データベース移行に含まれています。

<a name="verification-routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement email verification, three routes will need to be defined. First, a route will be needed to display a notice to the user that they should click the email verification link in the verification email that Laravel sent them after registration. -->
電子メール検証を適切に実装するには、3 つのルートを定義する必要があります。まず、登録後に Laravel から送信された確認メール内のメール確認リンクをクリックする必要があるという通知をユーザーに表示するルートが必要です。

<!-- Second, a route will be needed to handle requests generated when the user clicks the email verification link in the email. -->
次に、ユーザーが電子メール内の電子メール検証リンクをクリックしたときに生成されるリクエストを処理するためのルートが必要になります。

<!-- Third, a route will be needed to resend a verification link if the user accidentally loses the first verification link. -->
3 番目に、ユーザーが最初の検証リンクを誤って失った場合に検証リンクを再送信するためのルートが必要になります。

<a name="the-email-verification-notice"></a>
<!-- ### The Email Verification Notice -->
### The Email Verification Notice

<!-- As mentioned previously, a route should be defined that will return a view instructing the user to click the email verification link that was emailed to them by Laravel after registration. This view will be displayed to users when they try to access other parts of the application without verifying their email address first. Remember, the link is automatically emailed to the user as long as your `App\Models\User` model implements the `MustVerifyEmail` interface: -->
前述したように、登録後に Laravel から電子メールで送信された電子メール検証リンクをクリックするようにユーザーに指示するビューを返すルートを定義する必要があります。このビューは、ユーザーが最初に電子メール アドレスを確認せずにアプリケーションの他の部分にアクセスしようとしたときに表示されます。 `App\Models\User` モデルが `MustVerifyEmail` インターフェイスを実装している限り、リンクはユーザーに自動的に電子メールで送信されることに注意してください。

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');
```

<!-- The route that returns the email verification notice should be named `verification.notice`. It is important that the route is assigned this exact name since the `verified` middleware [included with Laravel](#protecting-routes) will automatically redirect to this route name if a user has not verified their email address. -->
電子メール検証通知を返すルートには、`verification.notice` という名前を付ける必要があります。ユーザーが電子メール アドレスを確認していない場合、`verified` ミドルウェア [included with Laravel](#protecting-routes) が自動的にこのルート名にリダイレクトするため、ルートにこの正確な名前が割り当てられることが重要です。

> [!NOTE]
> 電子メール検証を手動で実装する場合は、検証通知ビューの内容を自分で定義する必要があります。必要なすべての認証ビューと検証ビューを含むスキャフォールディングが必要な場合は、[Laravel application starter kits](/docs/13.x/starter-kits) を確認してください。

<a name="the-email-verification-handler"></a>
<!-- ### The Email Verification Handler -->
### The Email Verification Handler

<!-- Next, we need to define a route that will handle requests generated when the user clicks the email verification link that was emailed to them. This route should be named `verification.verify` and be assigned the `auth` and `signed` middlewares: -->
次に、電子メールで送信された電子メール検証リンクをユーザーがクリックしたときに生成されるリクエストを処理するルートを定義する必要があります。このルートには `verification.verify` という名前を付け、`auth` および `signed` ミドルウェアを割り当てる必要があります。

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');
```

<!-- Before moving on, let's take a closer look at this route. First, you'll notice we are using an `EmailVerificationRequest` request type instead of the typical `Illuminate\Http\Request` instance. The `EmailVerificationRequest` is a [form request](/docs/13.x/validation#form-request-validation) that is included with Laravel. This request will automatically take care of validating the request's `id` and `hash` parameters. -->
次に進む前に、このルートを詳しく見てみましょう。まず、一般的な `Illuminate\Http\Request` インスタンスの代わりに、`EmailVerificationRequest` リクエスト タイプを使用していることがわかります。 `EmailVerificationRequest` は、Laravel に含まれる [form request](/docs/13.x/validation#form-request-validation) です。このリクエストは、リクエストの `id` および `hash` パラメータの検証を自動的に処理します。

<!-- Next, we can proceed directly to calling the `fulfill` method on the request. This method will call the `markEmailAsVerified` method on the authenticated user and dispatch the `Illuminate\Auth\Events\Verified` event. The `markEmailAsVerified` method is available to the default `App\Models\User` model via the `Illuminate\Foundation\Auth\User` base class. Once the user's email address has been verified, you may redirect them wherever you wish. -->
次に、リクエストに対する `fulfill` メソッドの呼び出しに直接進むことができます。このメソッドは、認証されたユーザーで `markEmailAsVerified` メソッドを呼び出し、`Illuminate\Auth\Events\Verified` イベントを送出します。 `markEmailAsVerified` メソッドは、`Illuminate\Foundation\Auth\User` 基本クラスを介してデフォルトの `App\Models\User` モデルで使用できます。ユーザーの電子メール アドレスが確認されたら、希望する場所にリダイレクトできます。

<a name="resending-the-verification-email"></a>
<!-- ### Resending the Verification Email -->
### Resending the Verification Email

<!-- Sometimes a user may misplace or accidentally delete the email address verification email. To accommodate this, you may wish to define a route to allow the user to request that the verification email be resent. You may then make a request to this route by placing a simple form submission button within your [verification notice view](#the-email-verification-notice): -->
ユーザーが電子メール アドレス確認電子メールを置き忘れたり、誤って削除したりする場合があります。これに対応するには、ユーザーが確認電子メールの再送信を要求できるようにルートを定義するとよいでしょう。次に、[verification notice view](#the-email-verification-notice) 内に簡単なフォーム送信ボタンを配置することで、このルートにリクエストを送信できます。

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');
```

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/13.x/middleware) may be used to only allow verified users to access a given route. Laravel includes a `verified` [middleware alias](/docs/13.x/middleware#middleware-aliases), which is an alias for the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` middleware class. Since this alias is already automatically registered by Laravel, all you need to do is attach the `verified` middleware to a route definition. Typically, this middleware is paired with the `auth` middleware: -->
[Route middleware](/docs/13.x/middleware) は、検証済みのユーザーにのみ特定のルートへのアクセスを許可するために使用できます。 Laravel には、`Illuminate\Auth\Middleware\EnsureEmailIsVerified` ミドルウェア クラスのエイリアスである `verified` [middleware alias](/docs/13.x/middleware#middleware-aliases) が含まれています。このエイリアスはすでに Laravel によって自動的に登録されているため、必要なのは `verified` ミドルウェアをルート定義にアタッチすることだけです。通常、このミドルウェアは `auth` ミドルウェアとペアになります。

```php
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);
```

<!-- If an unverified user attempts to access a route that has been assigned this middleware, they will automatically be redirected to the `verification.notice` [named route](/docs/13.x/routing#named-routes). -->
未検証のユーザーがこのミドルウェアが割り当てられたルートにアクセスしようとすると、自動的に `verification.notice` [named route](/docs/13.x/routing#named-routes) にリダイレクトされます。

<a name="customization"></a>
<!-- ## Customization -->
## Customization

<a name="verification-email-customization"></a>
<!-- #### Verification Email Customization -->
#### Verification Email Customization

<!-- Although the default email verification notification should satisfy the requirements of most applications, Laravel allows you to customize how the email verification mail message is constructed. -->
デフォルトの電子メール検証通知はほとんどのアプリケーションの要件を満たすはずですが、Laravel では電子メール検証メール メッセージの構築方法をカスタマイズできます。

<!-- To get started, pass a closure to the `toMailUsing` method provided by the `Illuminate\Auth\Notifications\VerifyEmail` notification. The closure will receive the notifiable model instance that is receiving the notification as well as the signed email verification URL that the user must visit to verify their email address. The closure should return an instance of `Illuminate\Notifications\Messages\MailMessage`. Typically, you should call the `toMailUsing` method from the `boot` method of your application's `AppServiceProvider` class: -->
まず、`Illuminate\Auth\Notifications\VerifyEmail` 通知によって提供される `toMailUsing` メソッドにクロージャーを渡します。クロージャは、通知を受信する通知可能なモデル インスタンスと、ユーザーが電子メール アドレスを確認するためにアクセスする必要がある署名付き電子メール検証 URL を受け取ります。クロージャは `Illuminate\Notifications\Messages\MailMessage` のインスタンスを返す必要があります。通常、アプリケーションの `AppServiceProvider` クラスの `boot` メソッドから `toMailUsing` メソッドを呼び出す必要があります。

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
> メール通知の詳細については、[mail notification documentation](/docs/13.x/notifications#mail-notifications) を参照してください。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- When using the [Laravel application starter kits](/docs/13.x/starter-kits), Laravel dispatches an `Illuminate\Auth\Events\Verified` [event](/docs/13.x/events) during the email verification process. If you are manually handling email verification for your application, you may wish to manually dispatch these events after verification is completed. -->
[Laravel application starter kits](/docs/13.x/starter-kits) を使用する場合、Laravel は電子メール検証プロセス中に `Illuminate\Auth\Events\Verified` [event](/docs/13.x/events) をディスパッチします。アプリケーションの電子メール検証を手動で処理している場合は、検証の完了後にこれらのイベントを手動でディスパッチすることができます。

