<!-- # Resetting Passwords -->
# Resetting Passwords

- [Introduction](#introduction)
    - [Model Preparation](#model-preparation)
    - [Database Preparation](#database-preparation)
    - [Configuring Trusted Hosts](#configuring-trusted-hosts)
- [Routing](#routing)
    - [Requesting the Password Reset Link](#requesting-the-password-reset-link)
    - [Resetting the Password](#resetting-the-password)
- [Deleting Expired Tokens](#deleting-expired-tokens)
- [Customization](#password-customization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this by hand for every application you create, Laravel provides convenient services for sending password reset links and secure resetting passwords. -->
대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 매번 새로운 애플리케이션을 만들 때마다 직접 비밀번호 재설정 기능을 구현할 필요 없이, 비밀번호 재설정 링크를 전송하고 안전하게 비밀번호를 재설정할 수 있도록 지원하는 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에서 [application starter kit](/docs/10.x/starter-kits)를 설치해 보세요. Laravel의 스타터 키트는 인증 시스템 구축을 알아서 처리해주며, 비밀번호 분실 시 재설정 기능도 포함되어 있습니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before using the password reset features of Laravel, your application's `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is already included on the default `App\Models\User` model that is created with new Laravel applications. -->
Laravel의 비밀번호 재설정 기능을 사용하려면, 애플리케이션의 `App\Models\User` 모델에 `Illuminate\Notifications\Notifiable` 트레이트가 사용되어 있어야 합니다. 일반적으로, 이 트레이트는 새로 생성된 Laravel 애플리케이션의 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

<!-- Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface. -->
다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하고 있는지 확인해야 합니다. 프레임워크에 기본 제공되는 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 관련 메서드를 제공하는 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용하고 있습니다.

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- A table must be created to store your application's password reset tokens. The migration for this table is included in the default Laravel application, so you only need to migrate your database to create this table: -->
비밀번호 재설정 토큰을 저장하려면 테이블이 필요합니다. 이 테이블을 위한 마이그레이션은 Laravel의 기본 애플리케이션에 포함되어 있으므로, 데이터베이스 마이그레이션만 수행하면 됩니다.

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
<!-- ### Configuring Trusted Hosts -->
### Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
기본적으로 Laravel은 HTTP 요청의 `Host` 헤더의 내용과 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 시 애플리케이션의 절대 URL을 생성할 때 `Host` 헤더 값을 사용합니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given host name. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain host names, you may do so by enabling the `App\Http\Middleware\TrustHosts` middleware for your application. This is particularly important when your application offers password reset functionality. -->
일반적으로는 Nginx나 Apache와 같은 웹 서버에서 정의한 호스트명과 일치하는 요청만 애플리케이션에 전달하도록 설정하는 것이 좋습니다. 하지만 웹 서버 설정을 직접 바꿀 수 없는 환경이라면 Laravel의 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화해서 Laravel이 응답할 호스트를 제한할 수 있습니다. 특히 비밀번호 재설정 기능을 제공하는 경우 보안을 위해 중요한 설정입니다.

<!-- To learn more about this middleware, please consult the [`TrustHosts` middleware documentation](/docs/10.x/requests#configuring-trusted-hosts). -->
이 미들웨어에 대해 더 자세히 알고 싶다면 [`TrustHosts` middleware documentation](/docs/10.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them and completes the password reset form. -->
사용자가 비밀번호를 재설정할 수 있도록 하려면 여러 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있게 하는 라우트가 두 개 필요합니다. 그리고 다시, 이메일로 전달된 비밀번호 재설정 링크를 클릭해서 재설정 양식을 작성하면, 실제로 비밀번호를 재설정하는 과정에도 두 개의 라우트가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
<!-- ### Requesting the Password Reset Link -->
### Requesting the Password Reset Link

<a name="the-password-reset-link-request-form"></a>
<!-- #### The Password Reset Link Request Form -->
#### The Password Reset Link Request Form

<!-- First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form: -->
먼저, 비밀번호 재설정 링크를 요청할 수 있도록 필요한 라우트를 정의하겠습니다. 먼저, 비밀번호 재설정 링크를 요청할 수 있는 폼을 보여주는 뷰를 반환하는 라우트부터 만듭니다.

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

<!-- The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address. -->
이 라우트에서 반환하는 뷰에는 `email` 필드를 포함하는 폼이 있어야 하며, 사용자는 이 폼을 통해 입력한 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Next, we will define a route that handles the form submission request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user: -->
다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼이 제출될 때 실제로 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검사하고 해당 사용자를 위한 비밀번호 재설정 요청을 전송하는 역할을 합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::RESET_LINK_SENT
                ? back()->with(['status' => __($status)])
                : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/10.x/notifications). -->
위 라우트 내용을 좀 더 자세히 살펴보면, 먼저 요청된 `email` 필드를 유효성 검증합니다. 그리고 나서, Laravel이 제공하는 "비밀번호 브로커"(`Password` 파사드 사용)를 통해 해당 이메일의 사용자에게 비밀번호 재설정 링크를 전송합니다. 비밀번호 브로커는 주어진 필드(여기서는 이메일 주소)로 사용자를 조회한 후 Laravel의 [notification system](/docs/10.x/notifications)을 이용해 비밀번호 재설정 링크를 발송합니다.

<!-- The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/10.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. -->
`sendResetLink` 메서드는 "상태"를 나타내는 슬러그를 반환합니다. 이 상태 값은 Laravel의 [localization](/docs/10.x/localization) 헬퍼를 이용해 사용자에게 보기 쉬운 메시지로 번역할 수 있습니다. 비밀번호 재설정 상태의 실제 번역문은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 의해 결정됩니다. 상태 슬러그의 가능한 각 값에 해당하는 엔트리가 `passwords` 언어 파일 안에 위치해 있습니다.

> [!NOTE]
> 기본적으로 Laravel 애플리케이션의 뼈대에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 수정하려면 `lang:publish` 아티즌 명령어를 통해 파일을 게시할 수 있습니다.

<!-- You may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `sendResetLink` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/10.x/authentication#adding-custom-user-providers). -->
아마도 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 Laravel이 어떻게 데이터베이스에 저장된 사용자 정보를 찾는지 궁금할 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "사용자 공급자(user provider)"를 활용해서 데이터베이스 레코드를 가져옵니다. 비밀번호 브로커가 사용하는 사용자 공급자는 `config/auth.php` 설정 파일의 `passwords` 설정 배열 내에서 지정할 수 있습니다. 사용자 공급자를 직접 만들어 쓰고 싶다면 [authentication documentation](/docs/10.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정 로직을 직접 구현하는 경우, 각 뷰와 라우트를 스스로 정의해야 합니다. 필요한 인증·인증 검증 로직이 모두 포함된 사전 구축된 스캐폴딩이 필요하다면 [Laravel application starter kits](/docs/10.x/starter-kits)를 살펴보세요.

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<a name="the-password-reset-form"></a>
<!-- #### The Password Reset Form -->
#### The Password Reset Form

<!-- Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request: -->
이제, 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해서 새 비밀번호를 입력할 수 있도록 필요한 라우트를 정의하겠습니다. 먼저, 사용자가 재설정 링크를 클릭하면 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 만듭니다. 이 라우트는 추후에 비밀번호 재설정 요청 검증에 사용할 `token` 파라미터를 전달받아야 합니다.

```
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

<!-- The view that is returned by this route should display a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret `$token` received by our route. -->
이 라우트에서 반환하는 뷰에는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드를 포함한 폼이 있어야 하며, 이 token 필드에는 라우트가 전달받은 비밀 `$token` 값이 들어 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database: -->
물론, 비밀번호 재설정 폼이 실제로 제출될 때 처리하는 라우트도 정의해야 합니다. 이 라우트는 요청 데이터의 유효성을 검사하고, 사용자의 비밀번호를 데이터베이스에서 업데이트하는 역할을 합니다.

```
use App\Models\User;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

Route::post('/reset-password', function (Request $request) {
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8|confirmed',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'password_confirmation', 'token'),
        function (User $user, string $password) {
            $user->forceFill([
                'password' => Hash::make($password)
            ])->setRememberToken(Str::random(60));

            $user->save();

            event(new PasswordReset($user));
        }
    );

    return $status === Password::PASSWORD_RESET
                ? redirect()->route('login')->with('status', __($status))
                : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `token`, `email`, and `password` attributes are validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to validate the password reset request credentials. -->
다시 한 번, 이 라우트의 내용을 살펴보면 먼저 `token`, `email`, `password` 필드가 유효성 검증됩니다. 그다음, Laravel의 "비밀번호 브로커"(`Password` 파사드)를 사용해 비밀번호 재설정 요청이 유효한지 확인합니다.

<!-- If the token, email address, and password given to the password broker are valid, the closure passed to the `reset` method will be invoked. Within this closure, which receives the user instance and the plain-text password provided to the password reset form, we may update the user's password in the database. -->
입력된 토큰, 이메일, 비밀번호가 모두 유효하면 `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저에서는 사용자 인스턴스와 사용자가 비밀번호 재설정 폼에 입력한 평문 비밀번호를 받아 데이터베이스에 새로운 비밀번호를 저장할 수 있습니다.

<!-- The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/10.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. If your application does not contain a `lang` directory, you may create it using the `lang:publish` Artisan command. -->
`reset` 메서드는 "상태" 슬러그를 반환하며, 이 값은 Laravel의 [localization](/docs/10.x/localization) 헬퍼를 통해 사용자에게 보기 쉬운 메시지로 변환할 수 있습니다. 상태 값에 대한 번역문은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있으며, 각 상태 값에 해당하는 엔트리가 `passwords` 언어 파일 안에 위치합니다. 만약 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

<!-- Before moving on, you may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `reset` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/10.x/authentication#adding-custom-user-providers). -->
여기까지 살펴봤다면, `Password` 파사드의 `reset` 메서드를 호출할 때 Laravel이 어떻게 데이터베이스에서 사용자를 가져오는지 궁금할 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "사용자 공급자(user provider)"를 활용하여 사용자 레코드를 찾습니다. 사용되는 사용자 공급자는 `config/auth.php` 파일의 `passwords` 설정 배열에서 지정합니다. 사용자 공급자에 대해 더 알고 싶다면 [authentication documentation](/docs/10.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
<!-- ## Deleting Expired Tokens -->
## Deleting Expired Tokens

<!-- Password reset tokens that have expired will still be present within your database. However, you may easily delete these records using the `auth:clear-resets` Artisan command: -->
만료된 비밀번호 재설정 토큰도 데이터베이스에 남아 있을 수 있습니다. 이 기록은 `auth:clear-resets` 아티즌 명령어로 쉽게 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

<!-- If you would like to automate this process, consider adding the command to your application's [scheduler](/docs/10.x/scheduling): -->
이 과정을 자동화하고 싶다면, 애플리케이션의 [scheduler](/docs/10.x/scheduling)에 명령어를 추가하는 방법도 있습니다.

```
$schedule->command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
<!-- ## Customization -->
## Customization

<a name="reset-link-customization"></a>
<!-- #### Reset Link Customization -->
#### Reset Link Customization

<!-- You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from your `App\Providers\AuthServiceProvider` service provider's `boot` method: -->
`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 이용해 비밀번호 재설정 링크 URL을 직접 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 전달받는 클로저를 인자로 받습니다. 일반적으로 `App\Providers\AuthServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 이 메서드를 호출하면 됩니다.

```
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Register any authentication / authorization services.
 */
public function boot(): void
{
    ResetPassword::createUrlUsing(function (User $user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a name="reset-email-customization"></a>
<!-- #### Reset Email Customization -->
#### Reset Email Customization

<!-- You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `App\Models\User` model. Within this method, you may send the notification using any [notification class](/docs/10.x/notifications) of your own creation. The password reset `$token` is the first argument received by the method. You may use this `$token` to build the password reset URL of your choice and send your notification to the user: -->
사용자에게 비밀번호 재설정 링크를 전송할 때 사용하는 알림 클래스를 쉽게 커스터마이즈할 수 있습니다. 이를 위해 `App\Models\User` 모델의 `sendPasswordResetNotification` 메서드를 오버라이드하면 됩니다. 이 메서드에서 직접 만든 [notification class](/docs/10.x/notifications)를 사용해 알림을 전송할 수 있습니다. 메서드의 첫 번째 인수로 비밀번호 재설정 `$token`이 전달됩니다. 이 `$token`을 활용해 원하는 비밀번호 재설정 URL을 만들어 사용자에게 알림을 보낼 수 있습니다.

```
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```
