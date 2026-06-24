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
대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 매번 직접 이 기능을 구현하지 않아도 되도록, 비밀번호 재설정 링크 전송과 안전한 비밀번호 재설정 서비스를 편리하게 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [application starter kit](/docs/11.x/starter-kits)를 설치해보세요. Laravel의 스타터 키트는 비밀번호 찾기 등 인증 시스템 전체의 기본 구조를 자동으로 만들어줍니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before using the password reset features of Laravel, your application's `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is already included on the default `App\Models\User` model that is created with new Laravel applications. -->
Laravel의 비밀번호 재설정 기능을 사용하려면, 애플리케이션의 `App\Models\User` 모델에서 반드시 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 일반적으로 Laravel에서 생성되는 기본 `App\Models\User` 모델에는 이 트레이트가 이미 포함되어 있습니다.

<!-- Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface. -->
또한, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약(interface)을 구현하고 있는지 확인해야 합니다. 프레임워크에 포함된 `App\Models\User` 모델에는 이미 이 인터페이스가 구현되어 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용하여 인터페이스 구현에 필요한 메서드도 포함합니다.

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- A table must be created to store your application's password reset tokens. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` database migration. -->
애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 일반적으로, 이 테이블은 Laravel의 기본 마이그레이션 파일 `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다.

<a name="configuring-trusted-hosts"></a>
<!-- ### Configuring Trusted Hosts -->
### Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 값과 관계없이 모든 요청에 응답합니다. 또한, 웹 요청을 처리할 때 애플리케이션의 절대 URL을 생성할 때도 이 `Host` 헤더의 값을 사용합니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by using the `trustHosts` middleware method in your application's `bootstrap/app.php` file. This is particularly important when your application offers password reset functionality. -->
일반적으로는 Nginx나 Apache 같은 웹 서버에서 지정한 호스트명과 일치하는 요청만 애플리케이션에 전달하도록 웹 서버를 설정하는 것이 좋습니다. 하지만 웹 서버를 직접 설정하기 어려운 상황이고, 특정 호스트에 대해서만 Laravel이 응답하도록 지정해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용해 설정할 수 있습니다. 이 설정은 비밀번호 재설정 기능을 제공하는 애플리케이션에서는 특히 중요합니다.

<!-- To learn more about this middleware method, please consult the [`TrustHosts` middleware documentation](/docs/11.x/requests#configuring-trusted-hosts). -->
이 미들웨어 메서드에 대한 자세한 내용은 [`TrustHosts` middleware documentation](/docs/11.x/requests#configuring-trusted-hosts)를 참고하시기 바랍니다.

<a name="routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them and completes the password reset form. -->
사용자가 비밀번호를 재설정하도록 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 관련된 두 개의 라우트를 정의합니다. 그리고 사용자가 이메일로 받은 비밀번호 재설정 링크를 통해 실제로 비밀번호를 변경할 수 있도록 또 다른 두 개의 라우트를 정의합니다.

<a name="requesting-the-password-reset-link"></a>
<!-- ### Requesting the Password Reset Link -->
### Requesting the Password Reset Link

<a name="the-password-reset-link-request-form"></a>
<!-- #### The Password Reset Link Request Form -->
#### The Password Reset Link Request Form

<!-- First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form: -->
우선, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의합니다. 시작하려면, 비밀번호 재설정 링크 요청 폼을 보여주는 뷰를 반환하는 라우트를 정의합니다:

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

<!-- The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address. -->
이 라우트가 반환하는 뷰에는 사용자가 특정 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 `email` 필드를 가진 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Next, we will define a route that handles the form submission request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user: -->
다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼을 제출할 때 해당 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소의 유효성을 검사하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다:

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::ResetLinkSent
        ? back()->with(['status' => __($status)])
        : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/11.x/notifications). -->
진행하기 전에 이 라우트가 어떤 동작을 하는지 좀 더 자세히 살펴보겠습니다. 먼저 요청의 `email` 속성에 대한 유효성 검사가 이루어집니다. 그리고 Laravel의 내장 "패스워드 브로커"(`Password` 파사드)를 사용하여 해당 사용자에게 비밀번호 재설정 링크를 보냅니다. 패스워드 브로커는 지정된 필드(여기서는 이메일 주소)로 사용자를 조회하며, Laravel 내장 [notification system](/docs/11.x/notifications)을 통해 비밀번호 재설정 링크를 전송합니다.

<!-- The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/11.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. -->
`sendResetLink` 메서드는 "status" 슬러그(짧은 상태 문자열)를 반환합니다. 이 값은 Laravel의 [localization](/docs/11.x/localization) 헬퍼를 사용해 의미 있는 메시지로 번역할 수 있으며, 해당 요청 처리 결과에 대해 사용자에게 친절하게 안내할 수 있습니다. 이 상태 메시지의 번역 값은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있으며, `passwords` 파일에 각 상태별 항목이 들어 있습니다.

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` 아티즌 명령어로 직접 파일을 생성할 수 있습니다.

<!-- You may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `sendResetLink` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/11.x/authentication#adding-custom-user-providers). -->
또한, `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 Laravel이 어떻게 애플리케이션의 데이터베이스에서 사용자 레코드를 찾는지 궁금할 수 있습니다. Laravel의 패스워드 브로커는 인증 시스템의 "user provider"를 이용해 데이터베이스 레코드를 조회합니다. 어떤 user provider가 사용될지는 `config/auth.php` 설정 파일 내 `passwords` 구성 배열에서 지정할 수 있습니다. 직접 user provider를 구현하고 싶다면 [authentication documentation](/docs/11.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정을 직접 구현하는 경우에는 뷰와 라우트의 내용을 스스로 정의해야 합니다. 모든 인증 및 검증 로직이 포함된 기본 구조를 빠르게 만들고 싶다면, [Laravel application starter kits](/docs/11.x/starter-kits)를 참고하세요.

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<a name="the-password-reset-form"></a>
<!-- #### The Password Reset Form -->
#### The Password Reset Form

<!-- Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request: -->
이제 사용자가 이메일로 받은 비밀번호 재설정 링크를 클릭해 실제로 비밀번호를 변경할 수 있도록 하는 라우트를 정의합니다. 먼저, 사용자가 비밀번호 재설정 링크를 클릭했을 때 표시되는 비밀번호 재설정 폼을 반환하는 라우트를 정의합니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용될 `token` 매개변수를 받습니다:

```
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

<!-- The view that is returned by this route should display a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret `$token` received by our route. -->
이 라우트가 반환하는 뷰에는 반드시 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드(라우트에서 전달받은 비밀 `$token` 값 포함)를 가진 폼이 있어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database: -->
물론, 실제로 비밀번호 재설정 폼이 제출되었을 때 이를 처리하는 라우트도 필요합니다. 이 라우트는 요청의 유효성을 검사하고, 데이터베이스에서 사용자의 비밀번호를 업데이트하는 역할을 합니다:

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

    return $status === Password::PasswordReset
        ? redirect()->route('login')->with('status', __($status))
        : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `token`, `email`, and `password` attributes are validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to validate the password reset request credentials. -->
이 라우트를 조금 더 살펴보겠습니다. 먼저, 요청 데이터에서 `token`, `email`, `password` 속성의 유효성 검사가 이루어집니다. 이후 Laravel의 내장 "패스워드 브로커"(`Password` 파사드)를 활용해 비밀번호 재설정 요청 정보를 확인하게 됩니다.

<!-- If the token, email address, and password given to the password broker are valid, the closure passed to the `reset` method will be invoked. Within this closure, which receives the user instance and the plain-text password provided to the password reset form, we may update the user's password in the database. -->
패스워드 브로커에 전달된 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달한 클로저(콜백)가 호출됩니다. 이 클로저는 사용자 인스턴스와 사용자가 입력한 평문 비밀번호를 전달받으며, 이 안에서 사용자의 데이터베이스 비밀번호를 직접 업데이트합니다.

<!-- The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/11.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. If your application does not contain a `lang` directory, you may create it using the `lang:publish` Artisan command. -->
`reset` 메서드 역시 "status" 슬러그를 반환합니다. 이 값은 Laravel의 [localization](/docs/11.x/localization) 헬퍼로 사용자에게 안내할 수 있는 메시지로 변환할 수 있습니다. 상태 메시지 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정되며, 가능한 각 상태 값에 해당하는 엔트리가 `passwords` 언어 파일 안에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉터리가 없다면, `lang:publish` 아티즌 명령어로 생성할 수 있습니다.

<!-- Before moving on, you may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `reset` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/11.x/authentication#adding-custom-user-providers). -->
그리고 Laravel이 `Password` 파사드의 `reset` 메서드 호출 시 어떻게 사용자 레코드를 찾아오는지 궁금할 수 있습니다. Laravel의 패스워드 브로커 역시 인증 시스템의 "user provider"를 사용하여 데이터베이스 레코드를 조회합니다. 실제로 어떤 user provider가 사용되는지는 `config/auth.php` 설정 파일의 `passwords` 설정 배열에서 지정할 수 있습니다. 커스텀 user provider 구현에 대한 자세한 내용은 [authentication documentation](/docs/11.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
<!-- ## Deleting Expired Tokens -->
## Deleting Expired Tokens

<!-- Password reset tokens that have expired will still be present within your database. However, you may easily delete these records using the `auth:clear-resets` Artisan command: -->
만료된 비밀번호 재설정 토큰도 데이터베이스에는 남아 있을 수 있습니다. 하지만 다음의 `auth:clear-resets` 아티즌 명령어를 사용해서 손쉽게 모든 만료된 레코드를 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

<!-- If you would like to automate this process, consider adding the command to your application's [scheduler](/docs/11.x/scheduling): -->
이 과정을 자동화하고 싶다면, 애플리케이션의 [scheduler](/docs/11.x/scheduling)에 명령어를 등록하면 됩니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
<!-- ## Customization -->
## Customization

<a name="reset-link-customization"></a>
<!-- #### Reset Link Customization -->
#### Reset Link Customization

<!-- You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from your `App\Providers\AppServiceProvider` service provider's `boot` method: -->
`ResetPassword` 알림(Notification) 클래스가 제공하는 `createUrlUsing` 메서드를 사용하면 비밀번호 재설정 링크의 URL을 원하는 대로 커스터마이즈할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 토큰을 인자로 받는 클로저를 등록합니다. 일반적으로, 이 메서드는 `App\Providers\AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Bootstrap any application services.
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

<!-- You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `App\Models\User` model. Within this method, you may send the notification using any [notification class](/docs/11.x/notifications) of your own creation. The password reset `$token` is the first argument received by the method. You may use this `$token` to build the password reset URL of your choice and send your notification to the user: -->
사용자에게 비밀번호 재설정 링크를 발송할 때 사용할 알림(Notification) 클래스를 쉽게 수정할 수 있습니다. 먼저, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드(재정의)합니다. 이 메서드 안에서 직접 만든 [notification class](/docs/11.x/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`이 이 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 활용해 원하는 비밀번호 재설정 URL을 만들고, 사용자에게 직접 알림을 발송할 수 있습니다:

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
