<!-- # Resetting Passwords -->
# Resetting Passwords

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Model Preparation](#model-preparation)
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
대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 각 애플리케이션마다 이러한 기능을 직접 구현할 필요 없이, 비밀번호 재설정 링크를 전송하고 안전하게 비밀번호를 재설정할 수 있도록 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [application starter kit](/docs/12.x/starter-kits)를 설치하세요. Laravel의 스타터 키트는 비밀번호 재설정 기능을 포함한 전체 인증 시스템의 스캐폴딩을 자동으로 구성해줍니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Your application's password reset configuration file is stored at `config/auth.php`. Be sure to review the options available to you in this file. By default, Laravel is configured to use the `database` password reset driver. -->
애플리케이션의 비밀번호 재설정 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에서 제공되는 옵션을 반드시 검토하세요. 기본적으로 Laravel은 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

<!-- The password reset `driver` configuration option defines where password reset data will be stored. Laravel includes two drivers: -->
비밀번호 재설정의 `driver` 설정 옵션은 비밀번호 재설정 데이터를 어디에 저장할지 정의합니다. Laravel은 두 가지 드라이버를 제공합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `database` - password reset data is stored in a relational database.
- `cache` - password reset data is stored in one of your cache-based stores.
-->
- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 저장소에 저장됩니다.

<!-- </div> -->
</div>

<a name="driver-prerequisites"></a>
<!-- ### Driver Prerequisites -->
### Driver Prerequisites

<a name="database"></a>
<!-- #### Database -->
#### Database

<!-- When using the default `database` driver, a table must be created to store your application's password reset tokens. Typically, this is included in Laravel's default `0001_01_01_000000_create_users_table.php` database migration. -->
기본 `database` 드라이버를 사용할 때는, 애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="cache"></a>
<!-- #### Cache -->
#### Cache

<!-- There is also a cache driver available for handling password resets, which does not require a dedicated database table. Entries are keyed by the user's email address, so ensure you are not using email addresses as a cache key elsewhere in your application: -->
비밀번호 재설정을 위한 별도 데이터베이스 테이블이 필요 없는 캐시 드라이버도 존재합니다. 항목들은 사용자의 이메일 주소를 키로 저장되므로, 애플리케이션에서 이메일 주소를 다른 캐시 키로 사용하지 않도록 주의해야 합니다.

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // Optional...
        'expire' => 60,
        'throttle' => 60,
    ],
],
```

<!-- To prevent a call to `artisan cache:clear` from flushing your password reset data, you can optionally specify a separate cache store with the `store` configuration key. The value should correspond to a store configured in your `config/cache.php` configuration value. -->
`artisan cache:clear` 명령어를 실행할 때 비밀번호 재설정 데이터까지 모두 삭제되는 것을 방지하려면, `store` 설정 키를 통해 별도의 캐시 저장소를 지정할 수 있습니다. 이 값은 `config/cache.php` 설정 파일에 정의된 저장소 이름과 일치해야 합니다.

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before using the password reset features of Laravel, your application's `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is already included on the default `App\Models\User` model that is created with new Laravel applications. -->
Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 반드시 사용해야 합니다. 일반적으로 이 트레이트는 새로운 Laravel 애플리케이션에서 생성되는 기본 `App\Models\User` 모델에 이미 포함되어 있습니다.

<!-- Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface. -->
다음으로, `App\Models\User` 모델이 반드시 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하는지 확인해야 합니다. 프레임워크와 함께 제공되는 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="configuring-trusted-hosts"></a>
<!-- ### Configuring Trusted Hosts -->
### Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
기본적으로, Laravel은 HTTP 요청의 `Host` 헤더에 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 과정에서 절대 URL을 생성할 때도 `Host` 헤더의 값을 활용합니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by using the `trustHosts` middleware method in your application's `bootstrap/app.php` file. This is particularly important when your application offers password reset functionality. -->
보통은 Nginx나 Apache와 같은 웹 서버에서 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 보낼 수 있도록 구성하는 것이 좋습니다. 하지만 웹 서버를 직접 사용자 지정 할 수 없는 환경이라면, Laravel에서 직접 특정 호스트에만 응답하도록 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용하는 방법도 있습니다. 특히 애플리케이션에서 비밀번호 재설정 기능을 제공하는 경우 중요한 설정입니다.

<!-- To learn more about this middleware method, please consult the [TrustHosts middleware documentation](/docs/12.x/requests#configuring-trusted-hosts). -->
이 미들웨어 메서드에 대한 자세한 내용은 [TrustHosts middleware documentation](/docs/12.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them and completes the password reset form. -->
사용자가 비밀번호를 재설정할 수 있도록 적절하게 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 자신의 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트 두 개가 필요합니다. 두 번째로, 이메일로 발송된 비밀번호 재설정 링크를 클릭하여 실제로 비밀번호를 재설정하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
<!-- ### Requesting the Password Reset Link -->
### Requesting the Password Reset Link

<a name="the-password-reset-link-request-form"></a>
<!-- #### The Password Reset Link Request Form -->
#### The Password Reset Link Request Form

<!-- First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form: -->
우선, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트부터 정의하겠습니다. 시작을 위해, 비밀번호 재설정 링크 요청 폼을 반환하는 뷰를 제공하는 라우트를 정의합니다.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

<!-- The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address. -->
이 라우트가 반환하는 뷰에는 `email` 필드를 포함한 폼이 있어야 하며, 사용자가 원하는 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Next, we will define a route that handles the form submission request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user: -->
다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼 제출 요청을 처리하는 라우트를 정의합니다. 이 라우트는 이메일 주소를 유효성 검증하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다.

```php
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

<!-- Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/12.x/notifications). -->
진행하기 전에 이 라우트가 어떤 역할을 하는지 자세히 살펴보겠습니다. 먼저, 요청에서 받은 `email` 속성을 유효성 검증합니다. 다음으로, Laravel의 내장 "password broker"(즉, `Password` 파사드)를 사용해 해당 사용자에게 비밀번호 재설정 링크를 전송합니다. password broker는 지정된 필드(여기에서는 이메일 주소)를 기준으로 사용자를 조회하고, Laravel의 내장 [notification system](/docs/12.x/notifications)을 통해 비밀번호 재설정 링크를 보냅니다.

<!-- The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/12.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. -->
`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [localization](/docs/12.x/localization) 도우미 함수를 활용하여, 요청 상태에 대한 사용자의 이해를 돕는 메시지로 표시할 수 있습니다. 비밀번호 재설정 status 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 해당 슬러그별로 `passwords` 언어 파일에 각각의 항목이 존재합니다.

> [!NOTE]
> Laravel 애플리케이션 스캐폴딩에는 기본적으로 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령어로 파일을 퍼블리시할 수 있습니다.

<!-- You may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `sendResetLink` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/12.x/authentication#adding-custom-user-providers). -->
Laravel에서 어떻게 데이터베이스에서 사용자를 조회하는지 궁금할 수 있습니다. 이는 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 적용됩니다. Laravel의 password broker는 인증 시스템의 "user providers"를 이용해 데이터베이스 레코드를 조회합니다. password broker가 사용하는 user provider는 `config/auth.php` 설정 파일의 `passwords` 설정 배열에서 지정합니다. 커스텀 user provider 작성 방법은 [authentication documentation](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정 기능을 수동으로 구현하는 경우, 뷰와 라우트의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 검증 로직이 포함된 스캐폴딩을 원한다면 [Laravel application starter kits](/docs/12.x/starter-kits)를 참고하세요.

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<a name="the-password-reset-form"></a>
<!-- #### The Password Reset Form -->
#### The Password Reset Form

<!-- Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request: -->
다음으로, 이메일로 비밀번호 재설정 링크를 받은 사용자가 실제로 비밀번호를 변경할 수 있도록 필요한 라우트를 정의하겠습니다. 먼저, 사용자가 이메일에 포함된 비밀번호 재설정 링크를 클릭하면 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 만듭니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증할 때 사용할 `token` 파라미터를 전달받습니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

<!-- The view that is returned by this route should display a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret `$token` received by our route. -->
이 라우트가 반환하는 뷰는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드를 포함해야 합니다. 이때 숨겨진 필드에는 라우트로부터 전달받은 `$token`의 값을 담아야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
<!-- #### Handling the Form Submission -->
#### Handling the Form Submission

<!-- Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database: -->
물론, 비밀번호 재설정 폼의 제출을 실제로 처리하는 라우트도 정의해야 합니다. 이 라우트는 들어온 요청을 유효성 검증하고, 데이터베이스의 사용자의 비밀번호를 업데이트하는 역할을 합니다.

```php
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
진행하기 전에, 이 라우트의 동작을 자세히 살펴보겠습니다. 먼저, 요청에서 받은 `token`, `email`, `password` 속성이 올바른지 유효성 검증을 합니다. 그런 다음, Laravel의 내장 "password broker"(즉, `Password` 파사드)를 통해 비밀번호 재설정 요청 자격 증명을 검증합니다.

<!-- If the token, email address, and password given to the password broker are valid, the closure passed to the `reset` method will be invoked. Within this closure, which receives the user instance and the plain-text password provided to the password reset form, we may update the user's password in the database. -->
password broker에 제공된 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 제공된 평문 비밀번호를 인수로 받으며, 여기서 데이터베이스의 사용자 비밀번호를 실제로 변경할 수 있습니다.

<!-- The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/12.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. If your application does not contain a `lang` directory, you may create it using the `lang:publish` Artisan command. -->
`reset` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [localization](/docs/12.x/localization) 도우미 함수를 활용해 사용자에게 요청 상태에 맞는 메시지로 보여줄 수 있습니다. 비밀번호 재설정 status의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. status 슬러그의 가능한 각 값에 해당하는 항목이 `passwords` 언어 파일 안에 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어로 디렉토리를 생성할 수 있습니다.

<!-- Before moving on, you may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `reset` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/12.x/authentication#adding-custom-user-providers). -->
또한, Laravel이 `Password` 파사드의 `reset` 메서드로 데이터베이스에서 사용자 레코드를 어떻게 가져오는지 궁금할 수 있습니다. password broker는 인증 시스템의 "user providers"를 활용해 사용자 레코드를 조회합니다. password broker에서 사용하는 user provider는 `config/auth.php` 설정 파일의 `passwords` 배열에서 지정합니다. 커스텀 user provider 작성에 관한 자세한 내용은 [authentication documentation](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
<!-- ## Deleting Expired Tokens -->
## Deleting Expired Tokens

<!-- If you are using the `database` driver, password reset tokens that have expired will still be present within your database. However, you may easily delete these records using the `auth:clear-resets` Artisan command: -->
`database` 드라이버를 사용할 경우, 만료된 비밀번호 재설정 토큰이 데이터베이스에 남아 있을 수 있습니다. 하지만, `auth:clear-resets` Artisan 명령어를 사용해 손쉽게 이 레코드들을 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

<!-- If you would like to automate this process, consider adding the command to your application's [scheduler](/docs/12.x/scheduling): -->
이 프로세스를 자동화하고 싶다면, 애플리케이션의 [scheduler](/docs/12.x/scheduling)에 명령어를 추가할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
<!-- ## Customization -->
## Customization

<a name="reset-link-customization"></a>
<!-- #### Reset Link Customization -->
#### Reset Link Customization

<!-- You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from the `boot` method of your application's `AppServiceProvider`: -->
비밀번호 재설정 링크 URL은 `ResetPassword` 알림 클래스의 `createUrlUsing` 메서드를 활용해 사용자 지정할 수 있습니다. 이 메서드는, 알림을 받고 있는 사용자 인스턴스와 비밀번호 재설정 토큰을 인수로 받는 클로저를 전달받습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드 내에서 호출합니다.

```php
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

<!-- You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `App\Models\User` model. Within this method, you may send the notification using any [notification class](/docs/12.x/notifications) of your own creation. The password reset `$token` is the first argument received by the method. You may use this `$token` to build the password reset URL of your choice and send your notification to the user: -->
사용자에게 비밀번호 재설정 링크를 전송할 때 사용하는 알림 클래스를 손쉽게 수정할 수 있습니다. 우선, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서는 원하는 [notification class](/docs/12.x/notifications)를 통해 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`은 해당 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 사용해 원하는 비밀번호 재설정 URL을 만들어 사용자의 알림에 활용할 수 있습니다.

```php
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
