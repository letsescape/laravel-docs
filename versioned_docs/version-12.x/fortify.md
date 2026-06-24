<!-- # Laravel Fortify -->
# Laravel Fortify

- [Introduction](#introduction)
    - [What is Fortify?](#what-is-fortify)
    - [When Should I Use Fortify?](#when-should-i-use-fortify)
- [Installation](#installation)
    - [Fortify Features](#fortify-features)
    - [Disabling Views](#disabling-views)
- [Authentication](#authentication)
    - [Customizing User Authentication](#customizing-user-authentication)
    - [Customizing the Authentication Pipeline](#customizing-the-authentication-pipeline)
    - [Customizing Redirects](#customizing-authentication-redirects)
- [Two-Factor Authentication](#two-factor-authentication)
    - [Enabling Two-Factor Authentication](#enabling-two-factor-authentication)
    - [Authenticating With Two-Factor Authentication](#authenticating-with-two-factor-authentication)
    - [Disabling Two-Factor Authentication](#disabling-two-factor-authentication)
- [Registration](#registration)
    - [Customizing Registration](#customizing-registration)
- [Password Reset](#password-reset)
    - [Requesting a Password Reset Link](#requesting-a-password-reset-link)
    - [Resetting the Password](#resetting-the-password)
    - [Customizing Password Resets](#customizing-password-resets)
- [Email Verification](#email-verification)
    - [Protecting Routes](#protecting-routes)
- [Password Confirmation](#password-confirmation)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Fortify](https://github.com/laravel/fortify) is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. After installing Fortify, you may run the `route:list` Artisan command to see the routes that Fortify has registered. -->
[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다. Fortify를 설치한 후에는 `route:list` 아티즌 명령어를 실행하여 Fortify가 등록한 라우트들을 확인할 수 있습니다.

<!-- Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation. -->
Fortify는 자체적으로 사용자 인터페이스를 제공하지 않으므로, 등록된 라우트에 요청을 보내는 여러분만의 사용자 인터페이스와 연동하는 것이 기본적인 사용 방식입니다. 이 문서에서는 이러한 라우트로 요청을 보내는 구체적인 방법에 대해 설명합니다.

> [!NOTE]
> Fortify는 Laravel의 인증 기능을 빠르게 구현하는 데 도움을 주는 패키지입니다. **반드시 사용해야 하는 것은 아닙니다.** 언제든지 [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification) 공식 문서를 따라 직접 인증 기능을 구현할 수 있습니다.

<a name="what-is-fortify"></a>
<!-- ### What is Fortify? -->
### What is Fortify?

<!-- As mentioned previously, Laravel Fortify is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. -->
앞서 언급했듯이, Laravel Fortify는 Laravel을 위한 프론트엔드 독립형 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능 구현에 필요한 라우트와 컨트롤러를 등록합니다.

<!-- **You are not required to use Fortify in order to use Laravel's authentication features.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), and [email verification](/docs/12.x/verification) documentation. -->
**Laravel의 인증 기능을 사용하기 위해 반드시 Fortify를 사용할 필요는 없습니다.** [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification) 문서를 참고하여, Laravel의 인증 서비스와 직접 상호작용할 수 있습니다.

<!-- If you are new to Laravel, you may wish to explore [our application starter kits](/docs/12.x/starter-kits). Laravel's application starter kits use Fortify internally to provide authentication scaffolding for your application that includes a user interface built with [Tailwind CSS](https://tailwindcss.com). This allows you to study and get comfortable with Laravel's authentication features. -->
Laravel을 처음 접한다면 [our application starter kits](/docs/12.x/starter-kits)를 살펴볼 것을 권장합니다. Laravel의 스타터 키트는 내부적으로 Fortify를 사용해 [Tailwind CSS](https://tailwindcss.com)로 만든 사용자 인터페이스가 있는 인증 스캐폴딩을 제공합니다. 이를 통해 Laravel의 인증 기능을 쉽게 익힐 수 있습니다.

<!-- Laravel Fortify essentially takes the routes and controllers of our application starter kits and offers them as a package that does not include a user interface. This allows you to still quickly scaffold the backend implementation of your application's authentication layer without being tied to any particular frontend opinions. -->
Laravel Fortify는 스타터 키트에서 제공하는 라우트와 컨트롤러를 별도의 UI 없이 패키지로 분리한 것입니다. 이를 통해 빠르게 인증 백엔드만 구축하고, 프론트엔드는 자유롭게 구현할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
<!-- ### When Should I Use Fortify? -->
### When Should I Use Fortify?

<!-- You may be wondering when it is appropriate to use Laravel Fortify. First, if you are using one of Laravel's [application starter kits](/docs/12.x/starter-kits), you do not need to install Laravel Fortify since all of Laravel's application starter kits use Fortify and already provide a full authentication implementation. -->
Laravel Fortify를 언제 사용하는 것이 적절한지 궁금할 수 있습니다. 먼저, Laravel의 [application starter kits](/docs/12.x/starter-kits)를 사용한다면 별도로 Fortify를 설치할 필요가 없습니다. 모든 스타터 키트가 Fortify를 내부적으로 사용하며 완전한 인증 구현을 제공합니다.

<!-- If you are not using an application starter kit and your application needs authentication features, you have two options: manually implement your application's authentication features or use Laravel Fortify to provide the backend implementation of these features. -->
스타터 키트를 사용하지 않고 애플리케이션에 인증 기능이 필요하다면, 두 가지 선택지가 있습니다. 인증 기능을 직접 수동으로 구현하거나, Laravel Fortify를 사용해 이러한 기능의 백엔드 구현을 도입하는 것입니다.

<!-- If you choose to install Fortify, your user interface will make requests to Fortify's authentication routes that are detailed in this documentation in order to authenticate and register users. -->
Fortify를 설치하면, 사용자 인터페이스에서 Fortify가 등록하는 인증 라우트에 요청을 보내 인증 및 회원가입 처리를 하게 됩니다.

<!-- If you choose to manually interact with Laravel's authentication services instead of using Fortify, you may do so by following the documentation available in the [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), and [email verification](/docs/12.x/verification) documentation. -->
반대로 Fortify를 사용하지 않고 Laravel의 인증 기능을 직접 사용하려면, 위에서 언급한 [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), [email verification](/docs/12.x/verification) 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
<!-- #### Laravel Fortify and Laravel Sanctum -->
#### Laravel Fortify and Laravel Sanctum

<!-- Some developers become confused regarding the difference between [Laravel Sanctum](/docs/12.x/sanctum) and Laravel Fortify. Because the two packages solve two different but related problems, Laravel Fortify and Laravel Sanctum are not mutually exclusive or competing packages. -->
일부 개발자들은 [Laravel Sanctum](/docs/12.x/sanctum)과 Laravel Fortify의 차이점에 혼동을 느낄 수 있습니다. 이 두 패키지는 서로 다른 목적을 가지고 있기 때문에 상호 보완적이며 경쟁 관계가 아닙니다.

<!-- Laravel Sanctum is only concerned with managing API tokens and authenticating existing users using session cookies or tokens. Sanctum does not provide any routes that handle user registration, password reset, etc. -->
Laravel Sanctum은 API 토큰 관리 및 세션 쿠키/토큰을 통한 기존 사용자 인증만 담당합니다. 회원가입, 비밀번호 재설정 등과 같은 라우트는 제공하지 않습니다.

<!-- If you are attempting to manually build the authentication layer for an application that offers an API or serves as the backend for a single-page application, it is entirely possible that you will utilize both Laravel Fortify (for user registration, password reset, etc.) and Laravel Sanctum (API token management, session authentication). -->
API를 제공하거나, SPA(싱글 페이지 애플리케이션)의 백엔드로 인증 계층을 직접 구축하려는 경우, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)를 모두 활용하는 것이 일반적입니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Fortify using the Composer package manager: -->
먼저, Composer 패키지 매니저를 사용해 Fortify를 설치합니다.

```shell
composer require laravel/fortify
```

<!-- Next, publish Fortify's resources using the `fortify:install` Artisan command: -->
다음으로, `fortify:install` 아티즌 명령어를 실행해 Fortify 리소스를 퍼블리시합니다.

```shell
php artisan fortify:install
```

<!-- This command will publish Fortify's actions to your `app/Actions` directory, which will be created if it does not exist. In addition, the `FortifyServiceProvider`, configuration file, and all necessary database migrations will be published. -->
이 명령어는 Fortify의 액션을 `app/Actions` 디렉터리에 생성합니다(해당 디렉터리가 없다면 새로 생성됨). 또한 `FortifyServiceProvider`, 설정 파일, 필요한 데이터베이스 마이그레이션 파일들도 함께 퍼블리시됩니다.

<!-- Next, you should migrate your database: -->
이후 데이터베이스 마이그레이션을 실행해야 합니다.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
<!-- ### Fortify Features -->
### Fortify Features

<!-- The `fortify` configuration file contains a `features` configuration array. This array defines which backend routes / features Fortify will expose by default. We recommend that you only enable the following features, which are the basic authentication features provided by most Laravel applications: -->
`fortify` 설정 파일에는 `features`라는 설정 배열이 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 라우트/기능을 정의합니다. 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능만 활성화하는 것을 권장합니다.

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
기본적으로 Fortify는 로그인 화면이나 회원가입 화면처럼, 뷰를 반환하는 라우트를 정의합니다. 하지만 JavaScript 기반의 SPA(싱글 페이지 애플리케이션)을 만든다면 이러한 라우트가 필요 없을 수 있습니다. 이럴 때는 `config/fortify.php`의 `views` 값을 `false`로 설정해 이러한 라우트 전체를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
<!-- #### Disabling Views and Password Reset -->
#### Disabling Views and Password Reset

<!-- If you choose to disable Fortify's views and you will be implementing password reset features for your application, you should still define a route named `password.reset` that is responsible for displaying your application's "reset password" view. This is necessary because Laravel's `Illuminate\Auth\Notifications\ResetPassword` notification will generate the password reset URL via the `password.reset` named route. -->
Fortify의 뷰를 비활성화하면서도 비밀번호 재설정 기능을 사용할 경우, 애플리케이션에서 "비밀번호 재설정" 화면을 표시하는 `password.reset`이라는 이름의 라우트는 직접 반드시 정의해야 합니다. 이는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 비밀번호 재설정 URL을 생성할 때 `password.reset` 라우트를 참조하기 때문입니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- To get started, we need to instruct Fortify how to return our "login" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
먼저 Fortify에 "로그인" 뷰를 어떻게 반환할지 알려줘야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)라는 것을 기억하세요. 이미 완성된 프론트엔드 인증 기능이 필요하다면 [application starter kit](/docs/12.x/starter-kits)를 사용하는 것이 좋습니다.

<!-- All of the authentication view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class. Fortify will take care of defining the `/login` route that returns this view: -->
모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드를 이용해 사용자 지정할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다. Fortify가 `/login` 라우트를 정의해서 이 뷰를 반환하게 됩니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```

<!-- Your login template should include a form that makes a POST request to `/login`. The `/login` endpoint expects a string `email` / `username` and a `password`. The name of the email / username field should match the `username` value within the `config/fortify.php` configuration file. In addition, a boolean `remember` field may be provided to indicate that the user would like to use the "remember me" functionality provided by Laravel. -->
로그인 템플릿에는 `/login`으로 POST 요청을 보내는 폼이 있어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email`/`username`과 `password`를 기대합니다. email/username 필드명은 `config/fortify.php`의 `username` 값과 일치해야 합니다. 또한, Laravel의 "remember me" 기능을 사용하려면 불리언 타입의 `remember` 필드를 추가할 수 있습니다.

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. -->
로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. 만약 로그인 요청이 XHR 요청이었다면 200 HTTP 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the login screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with the 422 HTTP response. -->
요청이 실패하면, 사용자는 로그인 화면으로 돌아가며 유효성 검사 오류 정보는 공유된 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인할 수 있습니다. XHR 요청의 경우 422 HTTP 응답과 함께 유효성 검사 오류가 반환됩니다.

<a name="customizing-user-authentication"></a>
<!-- ### Customizing User Authentication -->
### Customizing User Authentication

<!-- Fortify will automatically retrieve and authenticate the user based on the provided credentials and the authentication guard that is configured for your application. However, you may sometimes wish to have full customization over how login credentials are authenticated and users are retrieved. Thankfully, Fortify allows you to easily accomplish this using the `Fortify::authenticateUsing` method. -->
Fortify는 제공된 자격 증명과 애플리케이션에 설정된 인증 가드에 따라 사용자를 자동으로 조회하고 인증합니다. 하지만 로그인 자격 증명 검증 및 사용자 조회 방법을 완전히 사용자 지정하고 싶을 때도 있습니다. `Fortify::authenticateUsing` 메서드를 사용하면 쉽게 사용자 지정할 수 있습니다.

<!-- This method accepts a closure which receives the incoming HTTP request. The closure is responsible for validating the login credentials attached to the request and returning the associated user instance. If the credentials are invalid or no user can be found, `null` or `false` should be returned by the closure. Typically, this method should be called from the `boot` method of your `FortifyServiceProvider`: -->
이 메서드는 들어오는 HTTP 요청을 받는 클로저를 인수로 받습니다. 클로저는 요청으로 전달된 로그인 정보를 검증하고, 해당 사용자가 존재한다면 사용자 인스턴스를 반환해야 합니다. 자격 증명이 올바르지 않거나 사용자를 찾지 못하면, `null`이나 `false`를 반환해야 합니다. 주로 `FortifyServiceProvider`의 `boot` 메서드에서 이 메서드를 호출하면 됩니다.

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
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
Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 사용자 지정할 수 있습니다. 단, 설정한 가드는 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스의 구현체여야 합니다. SPA 인증에 Fortify를 사용할 경우, Laravel의 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 사용하는 것을 권장합니다.

<a name="customizing-the-authentication-pipeline"></a>
<!-- ### Customizing the Authentication Pipeline -->
### Customizing the Authentication Pipeline

<!-- Laravel Fortify authenticates login requests through a pipeline of invokable classes. If you would like, you may define a custom pipeline of classes that login requests should be piped through. Each class should have an `__invoke` method which receives the incoming `Illuminate\Http\Request` instance and, like [middleware](/docs/12.x/middleware), a `$next` variable that is invoked in order to pass the request to the next class in the pipeline. -->
Laravel Fortify는 로그인 요청을 여러 `__invoke` 메서드를 가진 클래스의 파이프라인을 거쳐 인증합니다. 원하는 경우 로그인 요청이 거치는 파이프라인 클래스를 커스텀할 수 있습니다. 각 클래스는 들어오는 `Illuminate\Http\Request` 인스턴스와, 그 요청을 다음 파이프라인 클래스에 넘기는 `$next` 변수를 인수로 받습니다([middleware](/docs/12.x/middleware)와 비슷한 방식입니다).

<!-- To define your custom pipeline, you may use the `Fortify::authenticateThrough` method. This method accepts a closure which should return the array of classes to pipe the login request through. Typically, this method should be called from the `boot` method of your `App\Providers\FortifyServiceProvider` class. -->
커스텀 파이프라인 정의 방법은 `Fortify::authenticateThrough` 메서드를 사용합니다. 이 메서드는 로그인 요청을 거칠 클래스 배열을 반환하는 클로저를 인수로 받습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

<!-- The example below contains the default pipeline definition that you may use as a starting point when making your own modifications: -->
아래 예시는 기본 파이프라인 정의를 보여주며, 사용자 지정 시 참고하면 좋습니다.

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

<!-- #### Authentication Throttling -->
#### Authentication Throttling

<!-- By default, Fortify will throttle authentication attempts using the `EnsureLoginIsNotThrottled` middleware. This middleware throttles attempts that are unique to a username and IP address combination. -->
기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어로 로그인 시도 횟수를 제한합니다. 이 미들웨어는 사용자명과 IP 조합별로 로그인 시도를 제한합니다.

<!-- Some applications may require a different approach to throttling authentication attempts, such as throttling by IP address alone. Therefore, Fortify allows you to specify your own [rate limiter](/docs/12.x/routing#rate-limiting) via the `fortify.limiters.login` configuration option. Of course, this configuration option is located in your application's `config/fortify.php` configuration file. -->
일부 애플리케이션에서는, 예를 들어 IP별로만 인증 시도를 제한하는 등 다른 방식의 인증 제한(스로틀링)이 필요할 수 있습니다. Fortify는 `fortify.limiters.login` 설정 옵션을 통해 직접 [rate limiter](/docs/12.x/routing#rate-limiting)를 지정할 수 있습니다. 이 옵션은 `config/fortify.php` 파일에 있습니다.

> [!NOTE]
> 인증 제한, [two-factor authentication](/docs/12.x/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 함께 적용할 때 애플리케이션의 보안이 가장 강력하게 보호됩니다.

<a name="customizing-authentication-redirects"></a>
<!-- ### Customizing Redirects -->
### Customizing Redirects

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. After a user logs out of the application, the user will be redirected to the `/` URI. -->
로그인에 성공하면 Fortify는 `fortify` 설정 파일 내의 `home` 옵션에 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR일 경우 200 HTTP 응답을 반환합니다. 사용자가 로그아웃하면 `/`로 이동하게 됩니다.

<!-- If you need advanced customization of this behavior, you may bind implementations of the `LoginResponse` and `LogoutResponse` contracts into the Laravel [service container](/docs/12.x/container). Typically, this should be done within the `register` method of your application's `App\Providers\FortifyServiceProvider` class: -->
이 동작을 더 세밀하게 사용자 지정해야 한다면, Laravel [service container](/docs/12.x/container)에 `LoginResponse`, `LogoutResponse` 계약의 인스턴스를 바인딩해서 구현할 수 있습니다. 주로 `App\Providers\FortifyServiceProvider` 클래스의 `register` 메서드에서 이 바인딩을 처리합니다.

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
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
<!-- ## Two-Factor Authentication -->
## Two-Factor Authentication

<!-- When Fortify's two-factor authentication feature is enabled, the user is required to input a six digit numeric token during the authentication process. This token is generated using a time-based one-time password (TOTP) that can be retrieved from any TOTP compatible mobile authentication application such as Google Authenticator. -->
Fortify의 2단계 인증 기능을 활성화하면, 인증 과정에서 사용자는 6자리 숫자 토큰을 추가로 입력해야 합니다. 이 토큰은 Google Authenticator 같은 TOTP 호환 모바일 인증앱에서 생성되는 시간 기반 일회용 비밀번호(TOTP)입니다.

<!-- Before getting started, you should first ensure that your application's `App\Models\User` model uses the `Laravel\Fortify\TwoFactorAuthenticatable` trait: -->
먼저, 애플리케이션의 `App\Models\User` 모델에 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 추가해야 합니다.

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

<!-- Next, you should build a screen within your application where users can manage their two-factor authentication settings. This screen should allow the user to enable and disable two-factor authentication, as well as regenerate their two-factor authentication recovery codes. -->
다음으로, 사용자들이 2단계 인증을 관리할 수 있는 화면을 구현해야 합니다. 이 화면에서는 2단계 인증 활성화/비활성화, 복구 코드 재생성 등을 지원해야 합니다.

> 기본적으로, `fortify` 설정 파일의 `features` 배열은 2단계 인증 설정 변경 전 비밀번호 확인이 필요하도록 구성되어 있습니다. 따라서 [password confirmation](#password-confirmation) 기능을 먼저 구현해야 합니다.

<a name="enabling-two-factor-authentication"></a>
<!-- ### Enabling Two-Factor Authentication -->
### Enabling Two-Factor Authentication

<!-- To begin enabling two-factor authentication, your application should make a POST request to the `/user/two-factor-authentication` endpoint defined by Fortify. If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-enabled`. You may detect this `status` session variable within your templates to display the appropriate success message. If the request was an XHR request, `200` HTTP response will be returned. -->
2단계 인증을 활성화하려면, 애플리케이션에서 Fortify가 제공하는 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내야 합니다. 요청에 성공하면 직전 URL로 리디렉션되고, `status` 세션 변수가 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 `status` 세션 변수를 감지해 적절한 성공 메시지를 표시할 수 있습니다. XHR 요청인 경우 `200` HTTP 응답이 반환됩니다.

<!-- After choosing to enable two-factor authentication, the user must still "confirm" their two-factor authentication configuration by providing a valid two-factor authentication code. So, your "success" message should instruct the user that two-factor authentication confirmation is still required: -->
2단계 인증을 활성화한 후, 사용자는 "2단계 인증 구성 완료"를 위해 유효한 인증 코드를 입력해 설정을 "확인(Confirm)"해야 합니다. 따라서 성공 메시지에는 확인이 필요함을 반드시 안내해야 합니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

<!-- Next, you should display the two-factor authentication QR code for the user to scan into their authenticator application. If you are using Blade to render your application's frontend, you may retrieve the QR code SVG using the `twoFactorQrCodeSvg` method available on the user instance: -->
이후, 사용자가 인증 앱에 등록할 수 있도록 2단계 인증용 QR 코드를 표시해야 합니다. Blade를 사용한다면, 인증된 사용자 인스턴스의 `twoFactorQrCodeSvg` 메서드로 SVG QR 코드를 얻을 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-qr-code` endpoint to retrieve the user's two-factor authentication QR code. This endpoint will return a JSON object containing an `svg` key. -->
JavaScript 프론트엔드에서 사용할 경우, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내면 QR 코드가 포함된 JSON(`svg` 키) 응답을 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
<!-- #### Confirming Two-Factor Authentication -->
#### Confirming Two-Factor Authentication

<!-- In addition to displaying the user's two-factor authentication QR code, you should provide a text input where the user can supply a valid authentication code to "confirm" their two-factor authentication configuration. This code should be provided to the Laravel application via a POST request to the `/user/confirmed-two-factor-authentication` endpoint defined by Fortify. -->
QR 코드를 보여줄 뿐 아니라, 사용자가 인증 코드를 입력해서 2단계 인증 구성을 "확인"할 수 있는 입력란을 제공해야 합니다. 이 코드는 Fortify가 제공하는 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청을 보내야 하며,

<!-- If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-confirmed`: -->
성공 시 이전 URL로 리디렉션되고, 세션 변수 `status`에는 `two-factor-authentication-confirmed`가 저장됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

<!-- If the request to the two-factor authentication confirmation endpoint was made via an XHR request, a `200` HTTP response will be returned. -->
이중 인증 확인 엔드포인트로의 요청이 XHR 요청으로 이루어진 경우, `200` HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
<!-- #### Displaying the Recovery Codes -->
#### Displaying the Recovery Codes

<!-- You should also display the user's two-factor recovery codes. These recovery codes allow the user to authenticate if they lose access to their mobile device. If you are using Blade to render your application's frontend, you may access the recovery codes via the authenticated user instance: -->
사용자에게 2단계 인증 복구 코드도 반드시 보여주어야 합니다. 복구 코드는 사용자가 기기에 접근할 수 없게 되었을 때 인증에 사용할 수 있습니다. 애플리케이션 프런트엔드를 Blade로 렌더링하는 경우, 인증된 사용자 인스턴스를 통해 복구 코드에 접근할 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-recovery-codes` endpoint. This endpoint will return a JSON array containing the user's recovery codes. -->
JavaScript 프론트엔드에서는 `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청을 보내 복구 코드 배열을 받을 수 있습니다.

<!-- To regenerate the user's recovery codes, your application should make a POST request to the `/user/two-factor-recovery-codes` endpoint. -->
복구 코드를 재생성하려면 `/user/two-factor-recovery-codes` 엔드포인트로 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
<!-- ### Authenticating With Two-Factor Authentication -->
### Authenticating With Two-Factor Authentication

<!-- During the authentication process, Fortify will automatically redirect the user to your application's two-factor authentication challenge screen. However, if your application is making an XHR login request, the JSON response returned after a successful authentication attempt will contain a JSON object that has a `two_factor` boolean property. You should inspect this value to know whether you should redirect to your application's two-factor authentication challenge screen. -->
인증 과정에서 Fortify는 자동으로 사용자를 2단계 인증 도전(Challenge) 화면으로 리디렉션합니다. 만약 XHR 로그인 요청이라면, 성공한 응답에 `two_factor`라는 불리언 값을 가진 JSON 오브젝트가 포함되어 있습니다. 이 값을 검사해 2단계 인증 도전 화면으로 이동해야 하는지 판단할 수 있습니다.

<!-- To begin implementing two-factor authentication functionality, we need to instruct Fortify how to return our two-factor authentication challenge view. All of Fortify's authentication view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
2단계 인증 기능을 구현하려면, Fortify에 2단계 인증 도전 뷰를 반환하는 방법을 알려주어야 합니다. 이 역시 `Laravel\Fortify\Fortify` 클래스의 적절한 메서드로 사용자 지정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/two-factor-challenge` route that returns this view. Your `two-factor-challenge` template should include a form that makes a POST request to the `/two-factor-challenge` endpoint. The `/two-factor-challenge` action expects a `code` field that contains a valid TOTP token or a `recovery_code` field that contains one of the user's recovery codes. -->
Fortify는 이 뷰를 반환하는 `/two-factor-challenge` 라우트를 자동으로 정의합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge` 엔드포인트로 POST 요청을 보내는 폼이 있어야 합니다. `/two-factor-challenge` 액션은 유효한 TOTP 토큰을 담은 `code` 필드 또는 사용자의 복구 코드 중 하나를 담은 `recovery_code` 필드를 기대합니다.

<!-- If the login attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 204 HTTP response will be returned. -->
로그인에 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청이라면 204 HTTP 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the two-factor challenge screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패하면 다시 도전 화면으로 돌아가며, 유효성 오류는 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors)로 제공됩니다. XHR 요청인 경우 422 HTTP 오류와 함께 반환됩니다.

<a name="disabling-two-factor-authentication"></a>
<!-- ### Disabling Two-Factor Authentication -->
### Disabling Two-Factor Authentication

<!-- To disable two-factor authentication, your application should make a DELETE request to the `/user/two-factor-authentication` endpoint. Remember, Fortify's two-factor authentication endpoints require [password confirmation](#password-confirmation) prior to being called. -->
2단계 인증을 비활성화하려면, `/user/two-factor-authentication` 엔드포인트에 DELETE 요청을 보내면 됩니다. 참고로 Fortify의 2단계 인증 관련 엔드포인트는 [password confirmation](#password-confirmation)이 선행되어야 접근할 수 있습니다.

<a name="registration"></a>
<!-- ## Registration -->
## Registration

<!-- To begin implementing our application's registration functionality, we need to instruct Fortify how to return our "register" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
애플리케이션의 회원가입 기능을 구현하려면, 먼저 Fortify에 회원가입 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)라는 점을 다시 한 번 기억하세요. 이미 완성된 프론트엔드 기능이 필요하다면 [application starter kit](/docs/12.x/starter-kits)를 사용하세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 사용자 지정은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 메서드로 할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/register` route that returns this view. Your `register` template should include a form that makes a POST request to the `/register` endpoint defined by Fortify. -->
Fortify가 `/register` 라우트를 정의해 이 뷰를 반환합니다. `register` 템플릿에는 `/register`에 POST 요청을 보내는 폼이 있어야 하며, Fortify가 지정한 엔드포인트를 따라야 합니다.

<!-- The `/register` endpoint expects a string `name`, string email address / username, `password`, and `password_confirmation` fields. The name of the email / username field should match the `username` configuration value defined within your application's `fortify` configuration file. -->
`/register` 엔드포인트는 문자열 타입의 `name`, 문자열 이메일 주소 또는 사용자명, `password`, `password_confirmation` 필드를 기대합니다. 이메일/사용자명 필드명은 애플리케이션의 `fortify` 설정 파일에 정의된 `username` 설정값과 일치해야 합니다.

<!-- If the registration attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the request was an XHR request, a 201 HTTP response will be returned. -->
회원가입이 성공하면 Fortify는 `fortify` 설정 파일의 `home` 옵션에 지정된 URI로 리디렉션합니다. XHR 요청이라면 201 HTTP 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the registration screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패할 경우 사용자는 회원가입 화면으로 되돌아가며, 유효성 검사 오류 정보는 공유된 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors)로 제공됩니다. XHR 요청인 경우 422 HTTP 오류와 함께 반환됩니다.

<a name="customizing-registration"></a>
<!-- ### Customizing Registration -->
### Customizing Registration

<!-- The user validation and creation process may be customized by modifying the `App\Actions\Fortify\CreateNewUser` action that was generated when you installed Laravel Fortify. -->
사용자 유효성 검사 및 생성 프로세스는 Fortify 설치 시 생성된 `App\Actions\Fortify\CreateNewUser` 액션 파일을 수정하여 사용자 지정할 수 있습니다.

<a name="password-reset"></a>
<!-- ## Password Reset -->
## Password Reset

<a name="requesting-a-password-reset-link"></a>
<!-- ### Requesting a Password Reset Link -->
### Requesting a Password Reset Link

<!-- To begin implementing our application's password reset functionality, we need to instruct Fortify how to return our "forgot password" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
비밀번호 재설정 기능을 구현하려면, 먼저 Fortify에 "비밀번호 재설정 링크 요청" 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리라는 점을 기억하세요. 프론트엔드까지 포함된 기능이 필요하다면 [application starter kit](/docs/12.x/starter-kits)를 사용하세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스의 관련 메서드로 사용자 지정할 수 있으며, 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/forgot-password` endpoint that returns this view. Your `forgot-password` template should include a form that makes a POST request to the `/forgot-password` endpoint. -->
Fortify가 `/forgot-password` 엔드포인트를 정의해 뷰를 반환합니다. `forgot-password` 템플릿에는 `/forgot-password`로 POST 요청을 보내는 폼이 있어야 하며,

<!-- The `/forgot-password` endpoint expects a string `email` field. The name of this field / database column should match the `email` configuration value within your application's `fortify` configuration file. -->
`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드를 요구합니다. 이 필드명/DB 컬럼명은 애플리케이션의 `fortify` 설정 파일의 `email` 설정값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
<!-- #### Handling the Password Reset Link Request Response -->
#### Handling the Password Reset Link Request Response

<!-- If the password reset link request was successful, Fortify will redirect the user back to the `/forgot-password` endpoint and send an email to the user with a secure link they can use to reset their password. If the request was an XHR request, a 200 HTTP response will be returned. -->
비밀번호 재설정 링크 요청이 성공하면 Fortify는 사용자를 `/forgot-password` 엔드포인트로 다시 리디렉션시키고, 비밀번호 재설정에 사용할 수 있는 보안 링크가 담긴 이메일을 사용자에게 전송합니다. XHR 요청이었다면 200 HTTP 응답이 반환됩니다.

<!-- After being redirected back to the `/forgot-password` endpoint after a successful request, the `status` session variable may be used to display the status of the password reset link request attempt. -->
요청 성공 후 `/forgot-password` 엔드포인트로 다시 리디렉션되면, `status` 세션 변수를 이용해 비밀번호 재설정 링크 요청 시도의 상태를 표시할 수 있습니다.

<!-- The value of the `$status` session variable will match one of the translation strings defined within your application's `passwords` [language file](/docs/12.x/localization). If you would like to customize this value and have not published Laravel's language files, you may do so via the `lang:publish` Artisan command: -->
`$status` 값은 애플리케이션의 `passwords` [language file](/docs/12.x/localization) 내 번역 문자열 중 하나와 일치합니다. 값을 직접 사용자 지정하고 싶다면 언어 파일을 퍼블리시(`lang:publish`)하여 수정하면 됩니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was not successful, the user will be redirected back to the request password reset link screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
요청 실패 시, 비밀번호 재설정 요청 화면으로 되돌아가며 오류 정보는 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors)로 확인 가능합니다. XHR 요청인 경우 422 HTTP 오류가 반환됩니다.

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<!-- To finish implementing our application's password reset functionality, we need to instruct Fortify how to return our "reset password" view. -->
기능 완성을 위해 Fortify에 실제 "비밀번호 재설정" 뷰를 반환하는 방법을 알려주어야 합니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
역시 `Laravel\Fortify\Fortify` 클래스의 관련 메서드를 통해 뷰를 지정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

<!-- Fortify will take care of defining the route to display this view. Your `reset-password` template should include a form that makes a POST request to `/reset-password`. -->
Fortify가 이 뷰를 보여주는 라우트를 등록합니다. `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼이 있어야 하며,

<!-- The `/reset-password` endpoint expects a string `email` field, a `password` field, a `password_confirmation` field, and a hidden field named `token` that contains the value of `request()->route('token')`. The name of the "email" field / database column should match the `email` configuration value defined within your application's `fortify` configuration file. -->
`/reset-password` 엔드포인트는 문자열 타입의 `email`, `password`, `password_confirmation` 필드와 함께, 숨겨진 필드 `token`(값은 `request()->route('token')`)을 요구합니다. "email" 필드명/DB 컬럼명은 애플리케이션의 `fortify` 설정 파일에 정의된 `email` 설정값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
<!-- #### Handling the Password Reset Response -->
#### Handling the Password Reset Response

<!-- If the password reset request was successful, Fortify will redirect back to the `/login` route so that the user can log in with their new password. In addition, a `status` session variable will be set so that you may display the successful status of the reset on your login screen: -->
비밀번호 재설정 요청이 성공하면, Fortify는 `/login` 라우트로 리디렉션해 사용자가 새 비밀번호로 로그인할 수 있게 합니다. 이와 함께 성공 상태를 알리는 `status` 세션 변수가 설정되고, 로그인 화면에서 아래와 같이 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was an XHR request, a 200 HTTP response will be returned. -->
XHR 요청인 경우 200 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the reset password screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
요청이 실패하면 재설정 화면으로 돌아가며, 유효성 오류 정보는 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors)로 제공됩니다. XHR 요청 시 422 HTTP 오류가 반환됩니다.

<a name="customizing-password-resets"></a>
<!-- ### Customizing Password Resets -->
### Customizing Password Resets

<!-- The password reset process may be customized by modifying the `App\Actions\ResetUserPassword` action that was generated when you installed Laravel Fortify. -->
비밀번호 재설정 프로세스는 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션을 수정하여 사용자 지정할 수 있습니다.

<a name="email-verification"></a>
<!-- ## Email Verification -->
## Email Verification

<!-- After registration, you may wish for users to verify their email address before they continue accessing your application. To get started, ensure the `emailVerification` feature is enabled in your `fortify` configuration file's `features` array. Next, you should ensure that your `App\Models\User` class implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface. -->
회원가입 후, 사용자가 애플리케이션을 계속 이용하려면 이메일 인증을 거치도록 할 수 있습니다. 활성화하려면, `fortify` 설정 파일의 `features` 배열에 `emailVerification` 기능이 포함되어 있는지 확인하세요. 또한, `App\Models\User` 클래스가 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

<!-- Once these two setup steps have been completed, newly registered users will receive an email prompting them to verify their email address ownership. However, we need to inform Fortify how to display the email verification screen which informs the user that they need to go click the verification link in the email. -->
이 두 가지 설정을 마치면, 새로 가입한 사용자에게 이메일 인증을 요청하는 메일이 발송됩니다. 다음으로, Fortify에 이메일 인증 안내 메시지를 보여주는 화면을 반환하는 방법을 알려주어야 합니다.

<!-- All of Fortify's view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링은 `Laravel\Fortify\Fortify` 클래스에서 관련 메서드로 지정할 수 있으며, 주로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

<!-- Fortify will take care of defining the route that displays this view when a user is redirected to the `/email/verify` endpoint by Laravel's built-in `verified` middleware. -->
Fortify가 이 뷰를 보여주는 라우트를 등록합니다. 사용자가 Laravel의 `verified` 미들웨어에 의해 `/email/verify`로 리디렉션되면 이 화면이 표시됩니다.

<!-- Your `verify-email` template should include an informational message instructing the user to click the email verification link that was sent to their email address. -->
`verify-email` 템플릿에는 이메일 인증 링크를 클릭하라는 안내 메시지가 포함되어야 합니다.

<a name="resending-email-verification-links"></a>
<!-- #### Resending Email Verification Links -->
#### Resending Email Verification Links

<!-- If you wish, you may add a button to your application's `verify-email` template that triggers a POST request to the `/email/verification-notification` endpoint. When this endpoint receives a request, a new verification email link will be emailed to the user, allowing the user to get a new verification link if the previous one was accidentally deleted or lost. -->
원한다면 애플리케이션의 `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트로 POST 요청을 보내는 버튼을 추가할 수 있습니다. 이 엔드포인트가 요청을 받으면 사용자에게 새 인증 이메일 링크가 발송되므로, 이전 링크를 실수로 삭제했거나 잃어버린 경우 사용자가 새 인증 링크를 받을 수 있습니다.

<!-- If the request to resend the verification link email was successful, Fortify will redirect the user back to the `/email/verify` endpoint with a `status` session variable, allowing you to display an informational message to the user informing them the operation was successful. If the request was an XHR request, a 202 HTTP response will be returned: -->
인증 링크 이메일 재발송 요청이 성공하면, Fortify는 사용자를 `/email/verify` 엔드포인트로 다시 리디렉션하면서 `status` 세션 변수를 설정하여, 작업이 성공했다는 안내 메시지를 사용자에게 표시할 수 있게 합니다. XHR 요청인 경우 202 HTTP 응답이 반환됩니다.

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To specify that a route or group of routes requires that the user has verified their email address, you should attach Laravel's built-in `verified` middleware to the route. The `verified` middleware alias is automatically registered by Laravel and serves as an alias for the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` middleware: -->
특정 라우트나 라우트 그룹에 대해 사용자가 이메일 인증을 완료해야 접근할 수 있게 하려면, Laravel의 내장 `verified` 미들웨어를 해당 라우트에 추가하면 됩니다. `verified` 미들웨어 별칭은 자동 등록되며 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed. Typically, these routes are protected by Laravel's built-in `password.confirm` middleware. -->
애플리케이션 개발 중에는 사용자가 특정 작업을 수행하기 전에 비밀번호를 다시 한 번 확인해야 하는 경우가 종종 있습니다. 이러한 라우트는 주로 Laravel의 내장 `password.confirm` 미들웨어로 보호됩니다.

<!-- To begin implementing password confirmation functionality, we need to instruct Fortify how to return our application's "password confirmation" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
비밀번호 확인 화면을 구현하려면, Fortify에 "비밀번호 확인" 뷰를 반환하는 방법을 알려주어야 합니다. Fortify는 백엔드 인증 라이브러리(헤드리스)임을 기억하세요. 이미 준비된 프론트엔드가 필요한 경우에는 [application starter kit](/docs/12.x/starter-kits)를 사용하세요.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 적절한 메서드를 통해 사용자 지정할 수 있으며, 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

<!-- Fortify will take care of defining the `/user/confirm-password` endpoint that returns this view. Your `confirm-password` template should include a form that makes a POST request to the `/user/confirm-password` endpoint. The `/user/confirm-password` endpoint expects a `password` field that contains the user's current password. -->
Fortify는 이 뷰를 반환하는 `/user/confirm-password` 엔드포인트를 정의합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트로 POST 요청을 보내는 폼이 있어야 합니다. `/user/confirm-password` 엔드포인트는 사용자의 현재 비밀번호를 담은 `password` 필드를 기대합니다.

<!-- If the password matches the user's current password, Fortify will redirect the user to the route they were attempting to access. If the request was an XHR request, a 201 HTTP response will be returned. -->
비밀번호가 올바르면 사용자는 접근하려던 라우트로 리디렉션됩니다. XHR 요청인 경우 201 HTTP 응답이 반환됩니다.

<!-- If the request was not successful, the user will be redirected back to the confirm password screen and the validation errors will be available to you via the shared `$errors` Blade template variable. Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패하면 다시 비밀번호 확인 화면으로 돌아가며, 유효성 오류 정보는 Blade의 `$errors` 변수로 제공됩니다. XHR 요청이라면 422 HTTP 오류가 반환됩니다.
