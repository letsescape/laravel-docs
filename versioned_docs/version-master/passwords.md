# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 준비](#driver-prerequisites)
    - [모델 준비](#model-preparation)
    - [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이징](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 매번 직접 이 기능을 구현하지 않아도 되도록, 비밀번호 재설정 링크를 전송하고 안전하게 비밀번호를 재설정하는 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [애플리케이션 스타터 키트](/docs/master/starter-kits)를 설치해 보세요. Laravel의 스타터 키트는 잊어버린 비밀번호 재설정을 포함한 전체 인증 시스템의 스캐폴딩을 자동으로 처리합니다.

<a name="configuration"></a>
### 설정

애플리케이션의 비밀번호 재설정 설정 파일은 `config/auth.php`에 저장되어 있습니다. 이 파일에서 제공되는 옵션을 꼭 확인하시기 바랍니다. 기본적으로 Laravel은 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

비밀번호 재설정의 `driver` 설정 옵션은 비밀번호 재설정 데이터가 어디에 저장될지를 정의합니다. Laravel에는 두 가지 드라이버가 포함되어 있습니다:

<div class="content-list" markdown="1">

- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 저장소 중 하나에 저장됩니다.

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 준비

<a name="database"></a>
#### Database

기본 `database` 드라이버를 사용할 경우, 애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 마이그레이션 파일 `0001_01_01_000000_create_users_table.php`에 포함되어 있습니다.

<a name="cache"></a>
#### Cache

비밀번호 재설정 처리를 위한 캐시 드라이버도 제공되며, 별도의 데이터베이스 테이블이 필요하지 않습니다. 항목들은 사용자의 이메일 주소를 키로 하여 저장되므로, 애플리케이션의 다른 곳에서 이메일 주소를 캐시 키로 사용하고 있지 않은지 확인하세요:

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

`artisan cache:clear` 명령어 실행 시 비밀번호 재설정 데이터가 모두 삭제되는 것을 방지하려면, `store` 설정 키로 별도의 캐시 저장소를 지정할 수 있습니다. 이 값은 `config/cache.php`에 정의된 저장소 중 하나와 일치해야 합니다.

<a name="model-preparation"></a>
### 모델 준비

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 사용해야 합니다. 보통 새로운 Laravel 애플리케이션에서 기본으로 생성되는 `App\Models\User` 모델에 이미 이 트레이트가 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하는지 확인해야 합니다. Laravel 프레임워크에 기본 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용해 필요한 메서드를 제공합니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 설정

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용에 관계없이 모든 요청에 응답합니다. 또한 웹 요청 중 애플리케이션의 절대 URL을 생성할 때도 `Host` 헤더의 값이 사용됩니다.

일반적으로는 Nginx나 Apache 같은 웹 서버를 통해 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 전달하도록 설정하는 것이 좋습니다. 그러나 직접 웹 서버를 수정할 수 없는 환경이라면, Laravel에게 특정 호스트 이름에만 응답하도록 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용할 수 있습니다. 특히 비밀번호 재설정 기능이 제공되는 경우에는 이 설정이 중요합니다.

이 미들웨어 메서드에 대한 자세한 내용은 [TrustHosts 미들웨어 문서](/docs/master/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트가 필요합니다. 두 번째로, 사용자가 이메일로 전달된 비밀번호 재설정 링크를 클릭하고 재설정 폼을 완료하면 실제로 비밀번호를 재설정하는 라우트가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하기 위해 필요한 라우트를 정의하겠습니다. 시작을 위해 비밀번호 재설정 링크 요청 폼을 보여주는 뷰를 반환하는 라우트를 정의합니다:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 사용자가 특정 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 `email` 필드가 포함된 폼이 있어야 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, "비밀번호를 잊으셨나요" 뷰에서 폼이 제출되면 이를 처리할 라우트를 정의합니다. 이 라우트는 이메일 주소를 검증하고, 해당 사용자에게 비밀번호 재설정 요청을 전송하는 역할을 합니다:

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

이 라우트를 좀 더 자세히 살펴보면, 먼저 요청의 `email` 속성에 대해 유효성 검사를 진행합니다. 그 후, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 사용하여 해당 사용자에게 이메일로 비밀번호 재설정 링크를 전송합니다. 비밀번호 브로커는 주어진 필드(여기서는 이메일 주소)로 사용자를 조회하고, Laravel의 내장 [알림 시스템](/docs/master/notifications)을 통해 재설정 링크를 발송합니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [로컬라이제이션](/docs/master/localization) 헬퍼를 사용하여 사용자가 요청한 결과를 알기 쉬운 메시지로 변환할 수 있습니다. 비밀번호 재설정 status의 번역문은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 정의되어 있습니다. status 슬러그의 가능한 값마다 `passwords` 언어 파일에 해당 항목이 있습니다.

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 수정하고 싶다면, `lang:publish` Artisan 명령어로 파일을 퍼블리시 할 수 있습니다.

`Password` 파사드의 `sendResetLink` 메서드가 어떻게 애플리케이션 데이터베이스에서 사용자 레코드를 조회하는지 궁금할 수도 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "user providers(사용자 공급자)"를 활용하여 데이터베이스 레코드를 조회합니다. 비밀번호 브로커에서 어떤 user provider를 사용할지는 `config/auth.php`의 `passwords` 설정 배열에 지정되어 있습니다. 커스텀 user provider 작성 방법은 [인증 문서](/docs/master/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정을 수동으로 구현하는 경우, 뷰와 라우트의 내용을 직접 정의해야 합니다. 모든 인증 및 확인 로직이 포함된 스캐폴딩이 필요하다면 [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 확인하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로, 사용자가 이메일로 수신한 비밀번호 재설정 링크를 클릭하고, 새 비밀번호를 입력할 수 있도록 폼을 보여주는 라우트를 정의합니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증하는 데 사용할 `token` 파라미터를 받게 됩니다:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드를 포함해야 하며, 이 중 `token` 필드에는 라우트에서 전달받은 비밀 `$token` 값을 할당해야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 비밀번호 재설정 폼 제출을 실제로 처리할 라우트도 정의해야 합니다. 이 라우트는 들어온 요청을 검증하고, 사용자의 비밀번호를 데이터베이스에 반영하는 역할을 합니다:

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

조금 더 자세히 살펴보면, 요청의 `token`, `email`, `password` 속성에 우선 유효성 검사를 적용합니다. 그 뒤, Laravel의 내장 "비밀번호 브로커"(`Password` 파사드)를 사용해 비밀번호 재설정 요청의 자격 증명을 검증합니다.

비밀번호 브로커에 전달된 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 재설정 폼에 입력된 평문 비밀번호를 인수로 받아 데이터베이스에서 사용자의 비밀번호를 갱신합니다.

`reset` 메서드 역시 "status" 슬러그를 반환하며, 이 status는 Laravel의 [로컬라이제이션](/docs/master/localization) 헬퍼를 통해 사용자에게 친절한 메시지로 변환할 수 있습니다. 해당 status의 번역문은 애플리케이션의 `lang/{lang}/passwords.php` 파일에 위치합니다. 만약 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어로 쉽게 생성할 수 있습니다.

혹시 `Password` 파사드의 `reset` 메서드가 데이터베이스에서 사용자 레코드를 어떻게 조회하는지 궁금할 수 있습니다. Laravel의 비밀번호 브로커는 인증 시스템의 "user providers"를 통해 데이터베이스에서 사용자를 조회합니다. 어떤 user provider가 사용될지는 `config/auth.php`의 `passwords` 설정 배열에 지정되어 있습니다. 커스텀 user provider 작성법 등 자세한 내용은 [인증 문서](/docs/master/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

`database` 드라이버를 사용하는 경우, 만료된 비밀번호 재설정 토큰도 데이터베이스 내에 계속 남아 있을 수 있습니다. 이 레코드들은 `auth:clear-resets` Artisan 명령어로 손쉽게 삭제할 수 있습니다:

```shell
php artisan auth:clear-resets
```

이 과정을 자동화하고 싶다면, 명령어를 [스케줄러](/docs/master/scheduling)에 다음과 같이 추가할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이징 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이징

`ResetPassword` 알림(Notification) 클래스에서 제공하는 `createUrlUsing` 메서드를 활용해 비밀번호 재설정 링크 URL을 커스터마이징할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 링크 토큰을 전달받는 클로저를 인수로 받습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출하면 됩니다:

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
#### 재설정 이메일 커스터마이징

비밀번호 재설정 링크를 사용자에게 전송할 때 사용하는 알림(Notification) 클래스를 쉽게 변경할 수 있습니다. 먼저, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드해 주세요. 이 메서드 내에서 직접 만든 [알림 클래스](/docs/master/notifications)를 사용해 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`이 메서드의 첫 번째 인수로 전달되므로, 이를 사용하여 원하는 형태의 비밀번호 재설정 URL을 만들고 사용자에게 알림을 전송할 수 있습니다:

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
