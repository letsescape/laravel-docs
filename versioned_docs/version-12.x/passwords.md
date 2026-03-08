# 비밀번호 재설정 (Resetting Passwords)

- [소개](#introduction)
    - [설정](#configuration)
    - [드라이버 사전 요구사항](#driver-prerequisites)
    - [모델 준비](#model-preparation)
    - [신뢰할 수 있는 호스트 구성](#configuring-trusted-hosts)
- [라우팅](#routing)
    - [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
    - [비밀번호 재설정](#resetting-the-password)
- [만료된 토큰 삭제](#deleting-expired-tokens)
- [커스터마이즈](#password-customization)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel은 각 애플리케이션마다 이러한 기능을 직접 구현할 필요 없이, 비밀번호 재설정 링크를 전송하고 안전하게 비밀번호를 재설정할 수 있도록 편리한 서비스를 제공합니다.

> [!NOTE]
> 빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 설치하세요. Laravel의 스타터 키트는 비밀번호 재설정 기능을 포함한 전체 인증 시스템의 스캐폴딩을 자동으로 구성해줍니다.

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 비밀번호 재설정 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에서 제공되는 옵션을 반드시 검토하세요. 기본적으로 Laravel은 `database` 비밀번호 재설정 드라이버를 사용하도록 설정되어 있습니다.

비밀번호 재설정의 `driver` 설정 옵션은 비밀번호 재설정 데이터를 어디에 저장할지 정의합니다. Laravel은 두 가지 드라이버를 제공합니다:

<div class="content-list" markdown="1">

- `database` - 비밀번호 재설정 데이터가 관계형 데이터베이스에 저장됩니다.
- `cache` - 비밀번호 재설정 데이터가 캐시 기반 저장소에 저장됩니다.

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항 (Driver Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

기본 `database` 드라이버를 사용할 때는, 애플리케이션의 비밀번호 재설정 토큰을 저장할 테이블이 필요합니다. 일반적으로 이 테이블은 Laravel의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다.

<a name="cache"></a>
#### 캐시 (Cache)

비밀번호 재설정을 위한 별도 데이터베이스 테이블이 필요 없는 캐시 드라이버도 존재합니다. 항목들은 사용자의 이메일 주소를 키로 저장되므로, 애플리케이션에서 이메일 주소를 다른 캐시 키로 사용하지 않도록 주의해야 합니다.

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // 선택 사항...
        'expire' => 60,
        'throttle' => 60,
    ],
],
```

`artisan cache:clear` 명령어를 실행할 때 비밀번호 재설정 데이터까지 모두 삭제되는 것을 방지하려면, `store` 설정 키를 통해 별도의 캐시 저장소를 지정할 수 있습니다. 이 값은 `config/cache.php` 설정 파일에 정의된 저장소 이름과 일치해야 합니다.

<a name="model-preparation"></a>
### 모델 준비 (Model Preparation)

Laravel의 비밀번호 재설정 기능을 사용하기 전에, 애플리케이션의 `App\Models\User` 모델이 `Illuminate\Notifications\Notifiable` 트레이트를 반드시 사용해야 합니다. 일반적으로 새로운 Laravel 애플리케이션에서 이 트레이트는 이미 기본적으로 포함되어 있습니다.

다음으로, `App\Models\User` 모델이 반드시 `Illuminate\Contracts\Auth\CanResetPassword` 인터페이스를 구현하는지 확인해야 합니다. 프레임워크와 함께 제공되는 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있으며, 필요한 메서드를 포함하기 위해 `Illuminate\Auth\Passwords\CanResetPassword` 트레이트를 사용합니다.

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성 (Configuring Trusted Hosts)

기본적으로, Laravel은 HTTP 요청의 `Host` 헤더에 상관없이 모든 요청에 응답합니다. 또한, 웹 요청 과정에서 절대 URL을 생성할 때도 `Host` 헤더의 값을 활용합니다.

보통은 Nginx나 Apache와 같은 웹 서버에서 특정 호스트 이름과 일치하는 요청만 애플리케이션으로 보낼 수 있도록 구성하는 것이 좋습니다. 하지만 웹 서버를 직접 커스터마이즈 할 수 없는 환경이라면, Laravel에서 직접 특정 호스트에만 응답하도록 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 사용하는 방법도 있습니다. 특히 애플리케이션에서 비밀번호 재설정 기능을 제공하는 경우 중요한 설정입니다.

이 미들웨어 메서드에 대한 자세한 내용은 [TrustHosts 미들웨어 문서](/docs/12.x/requests#configuring-trusted-hosts)를 참고하세요.

<a name="routing"></a>
## 라우팅 (Routing)

사용자가 비밀번호를 재설정할 수 있도록 적절하게 지원하려면 여러 개의 라우트를 정의해야 합니다. 먼저, 사용자가 자신의 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있도록 하는 라우트 두 개가 필요합니다. 두 번째로, 이메일로 발송된 비밀번호 재설정 링크를 클릭하여 실제로 비밀번호를 재설정하는 라우트 두 개가 필요합니다.

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청 (Requesting the Password Reset Link)

<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

우선, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트부터 정의하겠습니다. 시작을 위해, 비밀번호 재설정 링크 요청 폼을 반환하는 뷰를 제공하는 라우트를 정의합니다.

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

이 라우트가 반환하는 뷰에는 `email` 필드를 포함한 폼이 있어야 하며, 사용자가 원하는 이메일 주소로 비밀번호 재설정 링크를 요청할 수 있습니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

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

진행하기 전에 이 라우트가 어떤 역할을 하는지 자세히 살펴보겠습니다. 먼저, 요청에서 받은 `email` 속성을 유효성 검증합니다. 다음으로, Laravel의 내장 "password broker"(즉, `Password` 파사드)를 사용해 해당 사용자에게 비밀번호 재설정 링크를 전송합니다. password broker는 지정된 필드(여기에서는 이메일 주소)를 기준으로 사용자를 조회하고, Laravel의 내장 [알림 시스템](/docs/12.x/notifications)을 통해 비밀번호 재설정 링크를 보냅니다.

`sendResetLink` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [로컬라이제이션](/docs/12.x/localization) 도우미 함수를 활용하여, 요청 상태에 대한 사용자의 이해를 돕는 메시지로 표시할 수 있습니다. 비밀번호 재설정 status 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 해당 슬러그별로 `passwords` 언어 파일에 각각의 항목이 존재합니다.

> [!NOTE]
> Laravel 애플리케이션 스캐폴딩에는 기본적으로 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 파일을 퍼블리시할 수 있습니다.

Laravel에서 어떻게 데이터베이스에서 사용자를 조회하는지 궁금할 수 있습니다. 이는 `Password` 파사드의 `sendResetLink` 메서드를 호출할 때 적용됩니다. Laravel의 password broker는 인증 시스템의 "user providers"를 이용해 데이터베이스 레코드를 조회합니다. password broker가 사용하는 user provider는 `config/auth.php` 설정 파일의 `passwords` 설정 배열에서 지정합니다. 커스텀 user provider 작성 방법은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

> [!NOTE]
> 비밀번호 재설정 기능을 수동으로 구현하는 경우, 뷰와 라우트의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 검증 로직이 포함된 스캐폴딩을 원한다면 [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 참고하세요.

<a name="resetting-the-password"></a>
### 비밀번호 재설정 (Resetting the Password)

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 폼

다음으로, 이메일로 비밀번호 재설정 링크를 받은 사용자가 실제로 비밀번호를 변경할 수 있도록 필요한 라우트를 정의하겠습니다. 먼저, 사용자가 이메일에 포함된 비밀번호 재설정 링크를 클릭하면 표시되는 비밀번호 재설정 폼을 보여주는 라우트를 만듭니다. 이 라우트는 나중에 비밀번호 재설정 요청을 검증할 때 사용할 `token` 파라미터를 전달받습니다.

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

이 라우트가 반환하는 뷰는 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 숨겨진 `token` 필드를 포함해야 합니다. 이때 숨겨진 필드에는 라우트로부터 전달받은 `$token`의 값을 담아야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

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

진행하기 전에, 이 라우트의 동작을 자세히 살펴보겠습니다. 먼저, 요청에서 받은 `token`, `email`, `password` 속성이 올바른지 유효성 검증을 합니다. 그런 다음, Laravel의 내장 "password broker"(즉, `Password` 파사드)를 통해 비밀번호 재설정 요청 자격 증명을 검증합니다.

password broker에 제공된 토큰, 이메일, 비밀번호가 모두 유효하다면, `reset` 메서드에 전달된 클로저가 호출됩니다. 이 클로저는 사용자 인스턴스와 비밀번호 재설정 폼에서 제공된 평문 비밀번호를 인수로 받으며, 여기서 데이터베이스의 사용자 비밀번호를 실제로 변경할 수 있습니다.

`reset` 메서드는 "status" 슬러그를 반환합니다. 이 status는 Laravel의 [로컬라이제이션](/docs/12.x/localization) 도우미 함수를 활용해 사용자에게 요청 상태에 맞는 메시지로 보여줄 수 있습니다. 비밀번호 재설정 status의 번역은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에서 결정됩니다. 여러 status 슬러그별로 각각의 항목이 정의되어 있습니다. 만약 애플리케이션에 `lang` 디렉토리가 없다면, `lang:publish` Artisan 명령어로 디렉토리를 생성할 수 있습니다.

또한, Laravel이 `Password` 파사드의 `reset` 메서드로 데이터베이스에서 사용자 레코드를 어떻게 가져오는지 궁금할 수 있습니다. password broker는 인증 시스템의 "user providers"를 활용해 사용자 레코드를 조회합니다. password broker에서 사용하는 user provider는 `config/auth.php` 설정 파일의 `passwords` 배열에서 지정합니다. 커스텀 user provider 작성에 관한 자세한 내용은 [인증 문서](/docs/12.x/authentication#adding-custom-user-providers)를 참고하세요.

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제 (Deleting Expired Tokens)

`database` 드라이버를 사용할 경우, 만료된 비밀번호 재설정 토큰이 데이터베이스에 남아 있을 수 있습니다. 하지만, `auth:clear-resets` Artisan 명령어를 사용해 손쉽게 이 레코드들을 삭제할 수 있습니다.

```shell
php artisan auth:clear-resets
```

이 프로세스를 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/12.x/scheduling)에 명령어를 추가할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
## 커스터마이즈 (Customization)

<a name="reset-link-customization"></a>
#### 재설정 링크 커스터마이즈

비밀번호 재설정 링크 URL은 `ResetPassword` 알림 클래스의 `createUrlUsing` 메서드를 활용해 커스터마이즈할 수 있습니다. 이 메서드는, 알림을 받고 있는 사용자 인스턴스와 비밀번호 재설정 토큰을 인수로 받는 클로저를 전달받습니다. 보통 이 메서드는 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드 내에서 호출합니다.

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
#### 재설정 이메일 커스터마이즈

사용자에게 비밀번호 재설정 링크를 전송할 때 사용하는 알림 클래스를 손쉽게 수정할 수 있습니다. 우선, `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 오버라이드하세요. 이 메서드 내에서는 원하는 [알림 클래스](/docs/12.x/notifications)를 통해 알림을 전송할 수 있습니다. 비밀번호 재설정 `$token`은 해당 메서드의 첫 번째 인자로 전달됩니다. 이 `$token`을 사용해 원하는 비밀번호 재설정 URL을 만들어 사용자의 알림에 활용할 수 있습니다.

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
