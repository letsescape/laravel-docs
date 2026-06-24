<!-- # Laravel Fortify -->
# Laravel Fortify

- [Introduction](#introduction)
    - [What Is Fortify?](#what-is-fortify)
    - [When Should I Use Fortify?](#when-should-i-use-fortify)
- [Installation](#installation)
    - [The Fortify Service Provider](#the-fortify-service-provider)
    - [Fortify Features](#fortify-features)
    - [Disabling Views](#disabling-views)
- [Authentication](#authentication)
    - [Customizing User Authentication](#customizing-user-authentication)
    - [Customizing The Authentication Pipeline](#customizing-the-authentication-pipeline)
    - [Customizing Redirects](#customizing-authentication-redirects)
- [Two Factor Authentication](#two-factor-authentication)
    - [Enabling Two Factor Authentication](#enabling-two-factor-authentication)
    - [Authenticating With Two Factor Authentication](#authenticating-with-two-factor-authentication)
    - [Disabling Two Factor Authentication](#disabling-two-factor-authentication)
- [Registration](#registration)
    - [Customizing Registration](#customizing-registration)
- [Password Reset](#password-reset)
    - [Requesting A Password Reset Link](#requesting-a-password-reset-link)
    - [Resetting The Password](#resetting-the-password)
    - [Customizing Password Resets](#customizing-password-resets)
- [Email Verification](#email-verification)
    - [Protecting Routes](#protecting-routes)
- [Password Confirmation](#password-confirmation)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Fortify](https://github.com/laravel/fortify) is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. After installing Fortify, you may run the `route:list` Artisan command to see the routes that Fortify has registered. -->
[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드에 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 등록해줍니다. Fortify를 설치한 후에는 `route:list` 아티즌 명령어를 실행하여 Fortify가 등록한 라우트를 확인할 수 있습니다.

<!-- Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation. -->
Fortify는 별도의 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분은 직접 만든 UI에서 Fortify가 등록한 라우트로 요청을 보내는 방식으로 사용하게 됩니다. 이 문서의 나머지 부분에서는 이러한 라우트로 어떻게 요청을 보내야 하는지 자세히 안내합니다.

> [!TIP]
> Fortify는 Laravel의 인증 기능을 빠르게 구현할 수 있도록 도와주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** [authentication](/docs/8.x/authentication), [password reset](/docs/8.x/passwords), [email verification](/docs/8.x/verification) 공식 문서를 참고해 직접 Laravel 인증 서비스를 다루실 수도 있습니다.

<a name="what-is-fortify"></a>
<!-- ### What Is Fortify? -->
### What Is Fortify?

<!-- As mentioned previously, Laravel Fortify is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. -->
앞서 언급했듯, Laravel Fortify는 프론트엔드에 구애받지 않고 인증 기능을 백엔드에서 구현해주는 패키지입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다.

<!-- **You are not required to use Fortify in order to use Laravel's authentication features.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/8.x/authentication), [password reset](/docs/8.x/passwords), and [email verification](/docs/8.x/verification) documentation. -->
**Laravel의 인증 기능을 사용하려면 반드시 Fortify를 설치할 필요는 없습니다.** [authentication](/docs/8.x/authentication), [password reset](/docs/8.x/passwords), [email verification](/docs/8.x/verification) 공식 문서를 참고해 직접 인증 서비스를 구현할 수도 있습니다.

<!-- If you are new to Laravel, you may wish to explore the [Laravel Breeze](/docs/8.x/starter-kits) application starter kit before attempting to use Laravel Fortify. Laravel Breeze provides an authentication scaffolding for your application that includes a user interface built with [Tailwind CSS](https://tailwindcss.com). Unlike Fortify, Breeze publishes its routes and controllers directly into your application. This allows you to study and get comfortable with Laravel's authentication features before allowing Laravel Fortify to implement these features for you. -->
Laravel을 처음 접하신다면, Fortify를 사용하기 전에 [Laravel Breeze](/docs/8.x/starter-kits) 스타터 키트를 먼저 살펴보시기를 권장합니다. Breeze는 [Tailwind CSS](https://tailwindcss.com)로 만들어진 UI와 함께 인증 스캐폴딩(기본 틀)을 제공합니다. Breeze는 Fortify와 달리, 라우트와 컨트롤러가 프로젝트 코드에 직접 추가되어 소스 코드를 분석하며 인증 구조를 익히기에 적합합니다.

<!-- Laravel Fortify essentially takes the routes and controllers of Laravel Breeze and offers them as a package that does not include a user interface. This allows you to still quickly scaffold the backend implementation of your application's authentication layer without being tied to any particular frontend opinions. -->
Fortify는 기본적으로 Breeze의 라우트와 컨트롤러를 별도의 UI 없이 패키지 형태로 제공합니다. 즉, 프론트엔드 구현 방식에 구애받지 않고, 인증 백엔드만 빠르게 도입할 수 있도록 도와줍니다.

<a name="when-should-i-use-fortify"></a>
<!-- ### When Should I Use Fortify? -->
### When Should I Use Fortify?

<!-- You may be wondering when it is appropriate to use Laravel Fortify. First, if you are using one of Laravel's [application starter kits](/docs/8.x/starter-kits), you do not need to install Laravel Fortify since all of Laravel's application starter kits already provide a full authentication implementation. -->
Fortify가 언제 적합한 선택인지 궁금할 수 있습니다. 먼저, Laravel의 [application starter kits](/docs/8.x/starter-kits)를 사용 중이라면 Fortify를 별도로 설치할 필요가 없습니다. 모든 스타터 키트에는 이미 인증 기능이 완비되어 있습니다.

<!-- If you are not using an application starter kit and your application needs authentication features, you have two options: manually implement your application's authentication features or use Laravel Fortify to provide the backend implementation of these features. -->
스타터 키트를 사용하지 않고 자체적으로 인증이 필요한 애플리케이션을 만든다면, 두 가지 방법이 있습니다: 직접 인증 기능을 구현하거나, Fortify로 백엔드 인증 부분을 빠르게 도입하는 방법입니다.

<!-- If you choose to install Fortify, your user interface will make requests to Fortify's authentication routes that are detailed in this documentation in order to authenticate and register users. -->
Fortify를 설치한다면, 여러분은 이 문서에 설명된 Fortify의 인증 관련 라우트로 직접 요청을 보내는 UI를 만들어야 합니다.

<!-- If you choose to manually interact with Laravel's authentication services instead of using Fortify, you may do so by following the documentation available in the [authentication](/docs/8.x/authentication), [password reset](/docs/8.x/passwords), and [email verification](/docs/8.x/verification) documentation. -->
반대로 Fortify 없이 인증 서비스를 직접 다루려면, [authentication](/docs/8.x/authentication), [password reset](/docs/8.x/passwords), [email verification](/docs/8.x/verification) 문서를 참고하세요.

<a name="laravel-fortify-and-laravel-sanctum"></a>
<!-- #### Laravel Fortify & Laravel Sanctum -->
#### Laravel Fortify & Laravel Sanctum

<!-- Some developers become confused regarding the difference between [Laravel Sanctum](/docs/8.x/sanctum) and Laravel Fortify. Because the two packages solve two different but related problems, Laravel Fortify and Laravel Sanctum are not mutually exclusive or competing packages. -->
[Laravel Sanctum](/docs/8.x/sanctum)과 Laravel Fortify의 차이점에 헷갈릴 수 있습니다. 이 두 패키지는 서로 다른 목적을 해결하므로, 경쟁하거나 대체 관계가 아닙니다.

<!-- Laravel Sanctum is only concerned with managing API tokens and authenticating existing users using session cookies or tokens. Sanctum does not provide any routes that handle user registration, password reset, etc. -->
Laravel Sanctum은 API 토큰 관리와, 기존 사용자의 세션 쿠키 또는 토큰 인증에만 집중합니다. 회원가입, 비밀번호 재설정 등 사용자 관리를 위한 라우트는 제공하지 않습니다.

<!-- If you are attempting to manually build the authentication layer for an application that offers an API or serves as the backend for a single-page application, it is entirely possible that you will utilize both Laravel Fortify (for user registration, password reset, etc.) and Laravel Sanctum (API token management, session authentication). -->
따라서, API나 싱글 페이지 애플리케이션(SPA) 백엔드를 구축하면서 인증 기능(회원가입, 비밀번호 재설정 등)은 Fortify로, API 토큰 관리나 세션 인증은 Sanctum으로 동시에 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Fortify using the Composer package manager: -->
먼저, Composer 패키지 매니저를 사용해 Fortify를 설치합니다.

```nothing
composer require laravel/fortify
```

<!-- Next, publish Fortify's resources using the `vendor:publish` command: -->
그 다음, `vendor:publish` 명령어로 Fortify의 리소스를 퍼블리시합니다:

```bash
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

<!-- This command will publish Fortify's actions to your `app/Actions` directory, which will be created if it does not exist. In addition, Fortify's configuration file and migrations will be published. -->
이 명령어를 실행하면, Fortify의 액션 클래스가 여러분의 `app/Actions` 디렉토리에 생성됩니다(존재하지 않으면 새로 생성). 또한 Fortify 관련 설정 파일과 마이그레이션도 퍼블리시됩니다.

<!-- Next, you should migrate your database: -->
이제 데이터베이스 마이그레이션을 실행하세요.

```bash
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
<!-- ### The Fortify Service Provider -->
### The Fortify Service Provider

<!-- The `vendor:publish` command discussed above will also publish the `App\Providers\FortifyServiceProvider` class. You should ensure this class is registered within the `providers` array of your application's `config/app.php` configuration file. -->
위에서 사용한 `vendor:publish` 명령어는 `App\Providers\FortifyServiceProvider` 클래스도 생성합니다. 반드시 Laravel의 `config/app.php` 파일 `providers` 배열에 이 서비스 프로바이더가 등록되어 있는지 확인하세요.

<!-- The Fortify service provider registers the actions that Fortify published and instructs Fortify to use them when their respective tasks are executed by Fortify. -->
Fortify 서비스 프로바이더는 퍼블리시된 액션들을 등록하고, Fortify가 관련 작업을 수행할 때 이 액션들을 사용하도록 설정합니다.

<a name="fortify-features"></a>
<!-- ### Fortify Features -->
### Fortify Features

<!-- The `fortify` configuration file contains a `features` configuration array. This array defines which backend routes / features Fortify will expose by default. If you are not using Fortify in combination with [Laravel Jetstream](https://jetstream.laravel.com), we recommend that you only enable the following features, which are the basic authentication features provided by most Laravel applications: -->
`fortify` 설정 파일에는 `features` 배열이 있습니다. 이 배열에서 Fortify가 기본적으로 노출할 백엔드 라우트와 기능을 결정합니다. [Laravel Jetstream](https://jetstream.laravel.com)과 Fortify를 함께 사용하지 않는다면, 대부분의 Laravel 애플리케이션에서 필요한 로그인, 회원가입, 비밀번호 재설정 등 인증 기본 기능만 활성화하는 것을 추천합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
<!-- ### Disabling Views -->
### Disabling Views

<!-- By default, Fortify defines routes that are intended to return views, such as a login screen or registration screen. However, if you are building a JavaScript driven single-page application, you may not need these routes. For that reason, you may disable these routes entirely by setting the `views` configuration value within your application's `config/fortify.php` configuration file to `false`: -->
Fortify는 기본적으로 로그인, 회원가입 화면 등 뷰를 반환하는 라우트를 정의합니다. 하지만 자바스크립트 기반 싱글페이지 애플리케이션(SPA)이라면, 이러한 라우트가 불필요할 수 있습니다. 이 경우, 애플리케이션의 `config/fortify.php` 파일에서 `views` 값을 `false`로 설정해 이러한 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
<!-- #### Disabling Views & Password Reset -->
#### Disabling Views & Password Reset

<!-- If you choose to disable Fortify's views and you will be implementing password reset features for your application, you should still define a route named `password.reset` that is responsible for displaying your application's "reset password" view. This is necessary because Laravel's `Illuminate\Auth\Notifications\ResetPassword` notification will generate the password reset URL via the `password.reset` named route. -->
만약 Fortify의 뷰를 비활성화하면서 애플리케이션의 비밀번호 재설정 기능을 구현하려면, `password.reset`이라는 이름의 라우트를 정의해 비밀번호 재설정 화면을 보여주도록 해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset` 명명 라우트를 통해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- To get started, we need to instruct Fortify how to return our "login" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/8.x/starter-kits). -->
먼저, Fortify가 "로그인" 화면을 반환하도록 설정해야 합니다. Fortify는 프론트엔드가 없는(headless) 인증 라이브러리임을 기억하세요. 프론트엔드까지 포함된 완성된 인증 기능이 필요하다면 [application starter kit](/docs/8.x/starter-kits) 사용을 고려해 주세요.

<!-- All of the authentication view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class. Fortify will take care of defining the `/login` route that returns this view: -->
모든 인증 관련 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 통해 커스터마이즈할 수 있습니다. 일반적으로, 여러분의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출하면 됩니다. `/login` 라우트 정의는 Fortify가 알아서 처리합니다:

```
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

<!-- Your login template should include a form that makes a POST request to `/login`. The `/login` endpoint expects a string `email` / `username` and a `password`. The name of the email / username field should match the `username` value within the `config/fortify.php` configuration file. In addition, a boolean `remember` field may be provided to indicate that the user would like to use the "remember me" functionality provided by Laravel. -->
로그인 폼에서는 `/login`에 POST 요청을 보내야 합니다. `/login` 엔드포인트는 `email`/`username`(문자열)과 `password`를 기대합니다. 이메일/사용자명 필드의 이름은 `config/fortify.php` 설정 파일의 `username` 값과 동일해야 합니다. 또한, "remember me" 기능을 사용하고 싶다면 `remember`(불린 값) 필드를 함께 전송할 수 있습니다.

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. -->
로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청일 경우에는 200 HTTP 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the login screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with the 422 HTTP response. -->
로그인에 실패하면, 사용자는 로그인 화면으로 되돌아가고, 검증 에러는 공유 `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors)에서 확인할 수 있습니다. XHR 요청이라면, 422 HTTP 응답과 검증 에러가 반환됩니다.

<a name="customizing-user-authentication"></a>
<!-- ### Customizing User Authentication -->
### Customizing User Authentication

<!-- Fortify will automatically retrieve and authenticate the user based on the provided credentials and the authentication guard that is configured for your application. However, you may sometimes wish to have full customization over how login credentials are authenticated and users are retrieved. Thankfully, Fortify allows you to easily accomplish this using the `Fortify::authenticateUsing` method. -->
Fortify는 기본적으로 전달 받은 자격 정보를 기반으로 사용자와 인증 가드를 이용해 인증을 자동으로 처리합니다. 하지만, 직접 로그인 자격 증명 검증 및 사용자 조회 과정을 커스터마이즈하고 싶다면, `Fortify::authenticateUsing` 메서드를 사용할 수 있습니다.

<!-- This method accepts a closure which receives the incoming HTTP request. The closure is responsible for validating the login credentials attached to the request and returning the associated user instance. If the credentials are invalid or no user can be found, `null` or `false` should be returned by the closure. Typically, this method should be called from the `boot` method of your `FortifyServiceProvider`: -->
이 메서드는 클로저를 인자로 받으며, 요청이 전달됩니다. 이 클로저에서 자격 증명을 검증하고, 해당 사용자를 반환하면 됩니다. 유효하지 않은 경우에는 `null` 또는 `false`를 반환해야 합니다. 보통 `FortifyServiceProvider` 클래스의 `boot` 메서드 안에서 호출하면 됩니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```

<a name="authentication-guard"></a>
<!-- #### Authentication Guard -->
#### Authentication Guard

<!-- You may customize the authentication guard used by Fortify within your application's `fortify` configuration file. However, you should ensure that the configured guard is an implementation of `Illuminate\Contracts\Auth\StatefulGuard`. If you are attempting to use Laravel Fortify to authenticate an SPA, you should use Laravel's default `web` guard in combination with [Laravel Sanctum](https://laravel.com/docs/sanctum). -->
Fortify에서 사용할 인증 가드는 `fortify` 설정 파일에서 수정할 수 있습니다. 단, 반드시 `Illuminate\Contracts\Auth\StatefulGuard`를 구현한 가드여야 합니다. SPA(싱글 페이지 애플리케이션) 인증에 Fortify를 사용하려면 Laravel 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 조합해 사용하세요.

<a name="customizing-the-authentication-pipeline"></a>
<!-- ### Customizing The Authentication Pipeline -->
### Customizing The Authentication Pipeline

<!-- Laravel Fortify authenticates login requests through a pipeline of invokable classes. If you would like, you may define a custom pipeline of classes that login requests should be piped through. Each class should have an `__invoke` method which receives the incoming `Illuminate\Http\Request` instance and, like [middleware](/docs/8.x/middleware), a `$next` variable that is invoked in order to pass the request to the next class in the pipeline. -->
Laravel Fortify는 로그인 요청을 일련의 호출 가능한 파이프라인 클래스들을 거쳐 인증합니다. 필요에 따라, 로그인 요청이 거치는 파이프라인 클래스를 직접 지정할 수도 있습니다. 각 클래스에는 들어오는 `Illuminate\Http\Request` 인스턴스를 받는 `__invoke` 메서드가 있어야 하며, [middleware](/docs/8.x/middleware)와 마찬가지로 다음 클래스로 요청을 전달하기 위해 호출되는 `$next` 변수도 받습니다.

<!-- To define your custom pipeline, you may use the `Fortify::authenticateThrough` method. This method accepts a closure which should return the array of classes to pipe the login request through. Typically, this method should be called from the `boot` method of your `App\Providers\FortifyServiceProvider` class. -->
커스텀 파이프라인을 정의하려면 `Fortify::authenticateThrough` 메서드를 사용하세요. 이 메서드는 클래스를 배열로 반환하는 클로저를 인자로 받습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

<!-- The example below contains the default pipeline definition that you may use as a starting point when making your own modifications: -->
아래는 기본 파이프라인 정의 예시입니다. 이를 참고해 필요한 부분만 수정해서 사용할 수 있습니다:

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

<a name="customizing-authentication-redirects"></a>
<!-- ### Customizing Redirects -->
### Customizing Redirects

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. After a user logs out of the application, the user will be redirected to the `/` URI. -->
로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정한 URI로 리디렉션합니다. XHR 요청이라면 200 HTTP 응답이 반환됩니다. 사용자가 로그아웃하면, 기본적으로 `/` URI로 리디렉션됩니다.

<!-- If you need advanced customization of this behavior, you may bind implementations of the `LoginResponse` and `LogoutResponse` contracts into the Laravel [service container](/docs/8.x/container). Typically, this should be done within the `register` method of your application's `App\Providers\FortifyServiceProvider` class: -->
만약 이 동작을 더 세밀하게 제어하고 싶다면, `LoginResponse` 및 `LogoutResponse` 계약을 Laravel의 [service container](/docs/8.x/container)에 바인딩하세요. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 처리합니다:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```

<a name="two-factor-authentication"></a>
<!-- ## Two Factor Authentication -->
## Two Factor Authentication

<!-- When Fortify's two factor authentication feature is enabled, the user is required to input a six digit numeric token during the authentication process. This token is generated using a time-based one-time password (TOTP) that can be retrieved from any TOTP compatible mobile authentication application such as Google Authenticator. -->
Fortify의 이중 인증(2FA) 기능을 활성화하면, 인증 과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 Google Authenticator 등 TOTP(시간 기반 일회용 비밀번호) 호환 모바일 인증 앱으로 생성할 수 있습니다.

<!-- Before getting started, you should first ensure that your application's `App\Models\User` model uses the `Laravel\Fortify\TwoFactorAuthenticatable` trait: -->
먼저, 여러분의 `App\Models\User` 모델에서 `Laravel\Fortify\TwoFactorAuthenticatable` 트레잇을 사용하고 있는지 확인하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
 ```

<!-- Next, you should build a screen within your application where users can manage their two factor authentication settings. This screen should allow the user to enable and disable two factor authentication, as well as regenerate their two factor authentication recovery codes. -->
그리고 사용자가 이중 인증을 관리할 수 있는 화면을 구현해야 합니다. 즉, 사용자가 이중 인증을 켜거나 끄고, 복구 코드를 재생성할 수 있는 UI가 필요합니다.

> 기본적으로, `fortify` 설정 파일의 `features` 배열은 이중 인증 설정 변경 전에 비밀번호 확인이 필요하도록 설정합니다. 따라서, 계속 진행하기 전에 [password confirmation](#password-confirmation) 기능이 함께 구현되어야 합니다.

<a name="enabling-two-factor-authentication"></a>
<!-- ### Enabling Two Factor Authentication -->
### Enabling Two Factor Authentication

<!-- To enable two factor authentication, your application should make a POST request to the `/user/two-factor-authentication` endpoint defined by Fortify. If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-enabled`. You may detect this `status` session variable within your templates to display the appropriate success message. If the request was an XHR request, `200` HTTP response will be returned: -->
이중 인증을 활성화하려면, 애플리케이션에서 Fortify의 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내면 됩니다. 성공 시, 이전 URL로 리디렉션되며 `status` 세션 변수가 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 `status` 세션 변수를 감지해 적절한 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우, `200` HTTP 응답이 반환됩니다:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm text-green-600">
        Two factor authentication has been enabled.
    </div>
@endif
```

<!-- Next, you should display the two factor authentication QR code for the user to scan into their authenticator application. If you are using Blade to render your application's frontend, you may retrieve the QR code SVG using the `twoFactorQrCodeSvg` method available on the user instance: -->
이제 사용자에게 2FA(이중 인증) QR 코드를 표시해야 하며, 사용자는 이를 인증 앱에 스캔해야 합니다. Blade를 사용한다면, user 인스턴스에서 `twoFactorQrCodeSvg` 메서드로 QR 코드 SVG를 받아올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-qr-code` endpoint to retrieve the user's two factor authentication QR code. This endpoint will return a JSON object containing an `svg` key. -->
자바스크립트 기반 프론트엔드라면, `/user/two-factor-qr-code`로 GET 요청을 해 QR 코드(리턴되는 JSON 객체의 `svg` 키 포함)를 받아올 수 있습니다.

<a name="displaying-the-recovery-codes"></a>
<!-- #### Displaying The Recovery Codes -->
#### Displaying The Recovery Codes

<!-- You should also display the user's two factor recovery codes. These recovery codes allow the user to authenticate if they lose access to their mobile device. If you are using Blade to render your application's frontend, you may access the recovery codes via the authenticated user instance: -->
2FA 복구 코드도 사용자에게 안내해야 합니다. 사용자가 모바일 기기 접근 권한을 잃더라도 이 코드로 인증할 수 있습니다. Blade라면 아래처럼 복구 코드를 가져올 수 있습니다:

```php
(array) $request->user()->recoveryCodes()
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-recovery-codes` endpoint. This endpoint will return a JSON array containing the user's recovery codes. -->
자바스크립트 기반 프론트엔드를 구축한다면, `/user/two-factor-recovery-codes` 엔드포인트로 XHR GET 요청을 보낼 수 있습니다. 이 엔드포인트는 사용자의 복구 코드가 담긴 JSON 배열을 반환합니다.

<!-- To regenerate the user's recovery codes, your application should make a POST request to the `/user/two-factor-recovery-codes` endpoint. -->
사용자의 복구 코드를 재생성하려면, 애플리케이션에서 `/user/two-factor-recovery-codes` 엔드포인트로 POST 요청을 보내야 합니다.

<a name="authenticating-with-two-factor-authentication"></a>
<!-- ### Authenticating With Two Factor Authentication -->
### Authenticating With Two Factor Authentication

<!-- During the authentication process, Fortify will automatically redirect the user to your application's two factor authentication challenge screen. However, if your application is making an XHR login request, the JSON response returned after a successful authentication attempt will contain a JSON object that has a `two_factor` boolean property. You should inspect this value to know whether you should redirect to your application's two factor authentication challenge screen. -->
인증 과정에서 Fortify는 자동으로 2FA 챌린지 화면으로 리디렉션합니다. 그러나 XHR(비동기) 로그인 요청인 경우, 인증 성공 후 반환되는 JSON 응답 객체의 `two_factor` 속성을 확인해 2FA 인증이 필요한지 판단해야 합니다.

<!-- To begin implementing two factor authentication functionality, we need to instruct Fortify how to return our two factor authentication challenge view. All of Fortify's authentication view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
이중 인증 기능 사용을 시작하려면 Fortify가 2FA 챌린지(2단계 인증) 화면을 반환하는 방법을 지정해주어야 합니다. 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 메서드로 커스터마이즈할 수 있으며, `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/two-factor-challenge` route that returns this view. Your `two-factor-challenge` template should include a form that makes a POST request to the `/two-factor-challenge` endpoint. The `/two-factor-challenge` action expects a `code` field that contains a valid TOTP token or a `recovery_code` field that contains one of the user's recovery codes. -->
Fortify는 이 뷰를 반환하는 `/two-factor-challenge` 라우트를 자동으로 정의합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge` 엔드포인트로 POST 요청하는 폼이 필요합니다. `/two-factor-challenge` 액션은 유효한 TOTP 토큰을 담은 `code` 필드 또는 사용자의 복구 코드 중 하나를 담은 `recovery_code` 필드를 기대합니다.

<!-- If the login attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 204 HTTP response will be returned. -->
로그인 성공 시, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청인 경우에는 204 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the two factor challenge screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패 시, 다시 2FA 챌린지 화면으로 되돌아가며, 검증 에러는 `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors) 또는 XHR 요청의 경우 422 응답에 포함됩니다.

<a name="disabling-two-factor-authentication"></a>
<!-- ### Disabling Two Factor Authentication -->
### Disabling Two Factor Authentication

<!-- To disable two factor authentication, your application should make a DELETE request to the `/user/two-factor-authentication` endpoint. Remember, Fortify's two factor authentication endpoints require [password confirmation](#password-confirmation) prior to being called. -->
이중 인증을 끄려면, 애플리케이션에서 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내면 됩니다. Fortify의 2FA 관련 엔드포인트는 호출 전에 반드시 [password confirmation](#password-confirmation)이 필요합니다.

<a name="registration"></a>
<!-- ## Registration -->
## Registration

<!-- To begin implementing our application's registration functionality, we need to instruct Fortify how to return our "register" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/8.x/starter-kits). -->
회원가입 기능을 구현하려면 Fortify가 "회원가입" 화면을 반환하는 방식을 지정해줘야 합니다. Fortify는 앞서 언급한 것처럼 프론트엔드가 없는 인증 라이브러리입니다. 인증 UI까지 포함해 완성된 방식이 필요하면 [application starter kit](/docs/8.x/starter-kits)를 사용해 주세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your `App\Providers\FortifyServiceProvider` class: -->
Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 메서드를 통해 설정할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 아래와 같이 지정합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/register` route that returns this view. Your `register` template should include a form that makes a POST request to the `/register` endpoint defined by Fortify. -->
Fortify는 이 뷰를 반환하는 `/register` 라우트를 자동으로 정의합니다. `register` 템플릿에는 Fortify가 정의한 `/register` 엔드포인트로 POST 요청하는 폼이 필요합니다.

<!-- The `/register` endpoint expects a string `name`, string email address / username, `password`, and `password_confirmation` fields. The name of the email / username field should match the `username` configuration value defined within your application's `fortify` configuration file. -->
`/register` 엔드포인트는 `name`(문자열), 이메일/사용자명(문자열), `password`, `password_confirmation` 필드를 기대합니다. 이메일/사용자명 필드의 이름은 `fortify` 설정 파일의 `username` 값과 맞추어야 합니다.

<!-- If the registration attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. -->
회원가입에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 정의된 URI로 리디렉션합니다. XHR 요청일 때는 200 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the registration screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패 시에는 회원가입 화면으로 다시 되돌아가고, 검증 에러는 `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors) 또는 XHR 422 응답에 포함됩니다.

<a name="customizing-registration"></a>
<!-- ### Customizing Registration -->
### Customizing Registration

<!-- The user validation and creation process may be customized by modifying the `App\Actions\Fortify\CreateNewUser` action that was generated when you installed Laravel Fortify. -->
회원 검증 및 생성 과정은 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션을 수정해 원하는 대로 변경할 수 있습니다.

<a name="password-reset"></a>
<!-- ## Password Reset -->
## Password Reset

<a name="requesting-a-password-reset-link"></a>
<!-- ### Requesting A Password Reset Link -->
### Requesting A Password Reset Link

<!-- To begin implementing our application's password reset functionality, we need to instruct Fortify how to return our "forgot password" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/8.x/starter-kits). -->
비밀번호 재설정 기능 구현을 시작하려면, Fortify가 "비밀번호 찾기" 뷰를 반환하는 방식을 지정해주어야 합니다. Fortify는 프론트엔드 없는 라이브러리이므로, 완성된 인증 UI가 필요하다면 [application starter kit](/docs/8.x/starter-kits)를 사용해 주세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 커스터마이징은 `Laravel\Fortify\Fortify` 클래스에서 지정할 수 있습니다. `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 아래와 같이 작성합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/forgot-password` endpoint that returns this view. Your `forgot-password` template should include a form that makes a POST request to the `/forgot-password` endpoint. -->
Fortify는 이 뷰를 반환하는 `/forgot-password` 엔드포인트를 자동으로 정의합니다. `forgot-password` 템플릿에는 `/forgot-password` 엔드포인트로 POST 요청하는 폼이 필요합니다.

<!-- The `/forgot-password` endpoint expects a string `email` field. The name of this field / database column should match the `email` configuration value within your application's `fortify` configuration file. -->
`/forgot-password` 엔드포인트에는 `email` 필드(문자열)가 필요합니다. 이 필드와 DB 컬럼 이름은 애플리케이션의 `fortify` 설정 파일의 `email` 설정값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
<!-- #### Handling The Password Reset Link Request Response -->
#### Handling The Password Reset Link Request Response

<!-- If the password reset link request was successful, Fortify will redirect the user back to the `/forgot-password` endpoint and send an email to the user with a secure link they can use to reset their password. If the request was an XHR request, a 200 HTTP response will be returned. -->
비밀번호 재설정 링크 요청이 성공하면, Fortify는 사용자를 다시 `/forgot-password` 엔드포인트로 리디렉션하고, 사용자의 이메일로 비밀번호 재설정 링크가 발송됩니다. XHR 요청 시에는 200 응답이 반환됩니다.

<!-- After being redirected back to the `/forgot-password` endpoint after a successful request, the `status` session variable may be used to display the status of the password reset link request attempt. The value of this session variable will match one of the translation strings defined within your application's `passwords` [language file](/docs/8.x/localization): -->
성공 후 `/forgot-password`에 리디렉션되었을 때, 세션 변수 `status`로 요청 결과 메시지를 표시할 수 있습니다. 이 값은 애플리케이션의 `passwords` [language file](/docs/8.x/localization)에 정의된 번역 문자열 중 하나와 일치합니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was not successful, the user will be redirected back to the request password reset link screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패하면, 다시 비밀번호 재설정 화면으로 돌아가며 검증 에러는 `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors) 또는 XHR 422 응답으로 반환됩니다.

<a name="resetting-the-password"></a>
<!-- ### Resetting The Password -->
### Resetting The Password

<!-- To finish implementing our application's password reset functionality, we need to instruct Fortify how to return our "reset password" view. -->
비밀번호 재설정 절차를 완성하려면, Fortify가 "비밀번호 재설정" 화면을 반환하도록 지정해야 합니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 커스터마이징은 `Laravel\Fortify\Fortify` 클래스에서 처리할 수 있습니다. 아래 방식으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 지정합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::resetPasswordView(function ($request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

<!-- Fortify will take care of defining the route to display this view. Your `reset-password` template should include a form that makes a POST request to `/reset-password`. -->
Fortify가 이 뷰를 표시하는 라우트를 자동으로 정의합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청하는 폼이 필요합니다.

<!-- The `/reset-password` endpoint expects a string `email` field, a `password` field, a `password_confirmation` field, and a hidden field named `token` that contains the value of `request()->route('token')`. The name of the "email" field / database column should match the `email` configuration value defined within your application's `fortify` configuration file. -->
`/reset-password` 엔드포인트는 `email`(문자열), `password`, `password_confirmation`, 그리고 `request()->route('token')` 값을 담은 숨겨진 `token` 필드를 필요로 합니다. "email" 필드/DB 컬럼명은 `fortify` 설정 파일의 `email` 값과 맞추어야 합니다.

<a name="handling-the-password-reset-response"></a>
<!-- #### Handling The Password Reset Response -->
#### Handling The Password Reset Response

<!-- If the password reset request was successful, Fortify will redirect back to the `/login` route so that the user can log in with their new password. In addition, a `status` session variable will be set so that you may display the successful status of the reset on your login screen: -->
비밀번호 재설정이 성공적으로 완료되면, Fortify는 `/login` 라우트로 리디렉션하여 새로운 비밀번호로 로그인할 수 있게 합니다. 또한 세션 변수 `status`가 설정되어 성공 메시지를 표시할 수 있습니다:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was an XHR request, a 200 HTTP response will be returned. -->
XHR 요청인 경우 200 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the reset password screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패하면 비밀번호 재설정 화면으로 되돌아가며, 검증 에러는 `$errors` [Blade template variable](/docs/8.x/validation#quick-displaying-the-validation-errors) 또는 XHR 422 응답으로 확인할 수 있습니다.

<a name="customizing-password-resets"></a>
<!-- ### Customizing Password Resets -->
### Customizing Password Resets

<!-- The password reset process may be customized by modifying the `App\Actions\ResetUserPassword` action that was generated when you installed Laravel Fortify. -->
비밀번호 재설정 관련 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정해 원하는 대로 바꿀 수 있습니다.

<a name="email-verification"></a>
<!-- ## Email Verification -->
## Email Verification

<!-- After registration, you may wish for users to verify their email address before they continue accessing your application. To get started, ensure the `emailVerification` feature is enabled in your `fortify` configuration file's `features` array. Next, you should ensure that your `App\Models\User` class implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface. -->
회원가입 후, 사용자가 애플리케이션을 계속 사용하기 전에 이메일 인증을 요구할 수도 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에서 `emailVerification` 기능이 활성화되어 있는지 확인하세요. 그리고 `App\Models\User` 클래스가 반드시 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

<!-- Once these two setup steps have been completed, newly registered users will receive an email prompting them to verify their email address ownership. However, we need to inform Fortify how to display the email verification screen which informs the user that they need to go click the verification link in the email. -->
이 두 가지가 준비되면, 새로 가입한 사용자에게 이메일 소유권 인증을 위한 메일이 전송됩니다. 이제 Fortify가 이메일 인증 안내 화면을 반환하는 방법을 지정해줘야 합니다.

<!-- All of Fortify's view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 커스터마이징은 `Laravel\Fortify\Fortify` 클래스에서 처리할 수 있고, 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

<!-- Fortify will take care of defining the route that displays this view when a user is redirected to the `/email/verify` endpoint by Laravel's built-in `verified` middleware. -->
Fortify가 `/email/verify` 엔드포인트에서 해당 뷰를 반환하도록 라우트를 정의하며, 이는 Laravel 내장 `verified` 미들웨어에 의해 리디렉션될 때 사용됩니다.

<!-- Your `verify-email` template should include an informational message instructing the user to click the email verification link that was sent to their email address. -->
`verify-email` 템플릿에서는 사용자에게 이메일로 전송된 인증 링크를 클릭하라는 메시지(안내문)를 표시하세요.

<a name="resending-email-verification-links"></a>
<!-- #### Resending Email Verification Links -->
#### Resending Email Verification Links

<!-- If you wish, you may add a button to your application's `verify-email` template that triggers a POST request to the `/email/verification-notification` endpoint. When this endpoint receives a request, a new verification email link will be emailed to the user, allowing the user to get a new verification link if the previous one was accidentally deleted or lost. -->
필요하다면, `verify-email` 템플릿에 인증 이메일을 다시 요청하는 버튼을 두고, `/email/verification-notification` 엔드포인트로 POST 요청을 전송하면 됩니다. 이 요청이 접수되면, 새로운 인증 링크가 사용자에게 이메일로 전송됩니다. 이전 인증 메일을 삭제했거나 잃어버린 경우 새로운 링크를 받을 수 있습니다.

<!-- If the request to resend the verification link email was successful, Fortify will redirect the user back to the `/email/verify` endpoint with a `status` session variable, allowing you to display an informational message to the user informing them the operation was successful. If the request was an XHR request, a 202 HTTP response will be returned: -->
인증 메일 재전송에 성공하면, Fortify는 `/email/verify` 엔드포인트로 다시 리디렉션하면서 세션 변수 `status`를 설정합니다. 이를 통해 성공 메시지를 표시할 수 있습니다. XHR 요청일 경우에는 202 응답이 반환됩니다:

```html
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To specify that a route or group of routes requires that the user has verified their email address, you should attach Laravel's built-in `verified` middleware to the route. This middleware is registered within your application's `App\Http\Kernel` class: -->
특정 라우트(또는 라우트 그룹)에 이메일 인증이 완료된 사용자만 접근할 수 있도록 제한하려면, 해당 라우트에 Laravel 내장 `verified` 미들웨어를 추가하세요. 이 미들웨어는 `App\Http\Kernel` 클래스에 이미 등록되어 있습니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed. Typically, these routes are protected by Laravel's built-in `password.confirm` middleware. -->
애플리케이션을 개발하다 보면, 중요한 작업 전에 사용자에게 비밀번호 재확인을 요구해야 할 때가 있습니다. 보통 이런 라우트에는 Laravel 내장 `password.confirm` 미들웨어가 적용됩니다.

<!-- To begin implementing password confirmation functionality, we need to instruct Fortify how to return our application's "password confirmation" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/8.x/starter-kits). -->
비밀번호 확인 기능 구현을 시작하려면, Fortify가 "비밀번호 확인" 화면을 반환하도록 지정해야 합니다. Fortify는 프론트엔드가 없는 인증 라이브러리이므로, 완성된 UI가 포함된 인증 시스템이 필요하다면 [application starter kit](/docs/8.x/starter-kits)를 사용해 주세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 커스터마이징은 `Laravel\Fortify\Fortify` 클래스에서 처리할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 지정합니다:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/user/confirm-password` endpoint that returns this view. Your `confirm-password` template should include a form that makes a POST request to the `/user/confirm-password` endpoint. The `/user/confirm-password` endpoint expects a `password` field that contains the user's current password. -->
Fortify는 이 뷰를 반환하는 `/user/confirm-password` 엔드포인트를 정의합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트로 POST 요청하는 폼이 들어가야 합니다. `/user/confirm-password` 엔드포인트는 사용자의 현재 비밀번호를 담은 `password` 필드를 기대합니다.

<!-- If the password matches the user's current password, Fortify will redirect the user to the route they were attempting to access. If the request was an XHR request, a 201 HTTP response will be returned. -->
비밀번호가 현재 비밀번호와 일치하면, Fortify는 사용자가 접근하려 했던 라우트로 리디렉션합니다. XHR 요청이라면 201 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the confirm password screen and the validation errors will be available to you via the shared `$errors` Blade template variable. Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패하면 비밀번호 확인 화면으로 다시 돌아가며, 검증 에러는 공유 `$errors` Blade 변수 또는 XHR 422 응답으로 받을 수 있습니다.