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
- [Two Factor Authentication](#two-factor-authentication)
    - [Enabling Two Factor Authentication](#enabling-two-factor-authentication)
    - [Authenticating With Two Factor Authentication](#authenticating-with-two-factor-authentication)
    - [Disabling Two Factor Authentication](#disabling-two-factor-authentication)
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
[Laravel Fortify](https://github.com/laravel/fortify)는 Laravel을 위한 프론트엔드에 독립적인 인증 백엔드 구현체입니다. Fortify는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 자동으로 등록합니다. Fortify를 설치한 후 `route:list` 아티즌 명령어를 실행하면, Fortify가 등록한 라우트를 확인할 수 있습니다.

<!-- Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation. -->
Fortify는 자체 사용자 인터페이스(UI)를 제공하지 않으므로, 여러분이 별도로 만든 UI에서 Fortify가 제공하는 라우트로 요청을 보내는 방식으로 사용합니다. 이 문서의 나머지 부분에서 이러한 라우트로 요청을 보내는 방법을 자세히 설명합니다.

> [!NOTE]
> Fortify는 Laravel 인증 기능 구현을 빠르게 시작할 수 있도록 도와주는 패키지입니다. **꼭 사용해야 하는 것은 아닙니다.** [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 공식 문서를 따라 Laravel의 인증 서비스를 직접 다루어도 괜찮습니다.

<a name="what-is-fortify"></a>
<!-- ### What is Fortify? -->
### What is Fortify?

<!-- As mentioned previously, Laravel Fortify is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. -->
앞서 언급한 것처럼, Laravel Fortify는 Laravel을 위한 프론트엔드 독립형 인증 백엔드 구현체입니다. 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 Laravel의 모든 인증 기능을 구현하는 데 필요한 라우트와 컨트롤러를 자동으로 등록합니다.

<!-- **You are not required to use Fortify in order to use Laravel's authentication features.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), and [email verification](/docs/11.x/verification) documentation. -->
**Fortify를 사용하지 않아도 Laravel의 인증 기능을 사용할 수 있습니다.** [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 공식 문서에서 안내하는 방법대로 직접 인증 로직을 구현해도 됩니다.

<!-- If you are new to Laravel, you may wish to explore the [Laravel Breeze](/docs/11.x/starter-kits) application starter kit before attempting to use Laravel Fortify. Laravel Breeze provides an authentication scaffolding for your application that includes a user interface built with [Tailwind CSS](https://tailwindcss.com). Unlike Fortify, Breeze publishes its routes and controllers directly into your application. This allows you to study and get comfortable with Laravel's authentication features before allowing Laravel Fortify to implement these features for you. -->
Laravel을 처음 접하는 분이라면, Fortify를 사용하기 전에 [Laravel Breeze](/docs/11.x/starter-kits) 시작 키트를 먼저 살펴보는 것도 좋습니다. Laravel Breeze는 [Tailwind CSS](https://tailwindcss.com)로 만들어진 기본 UI와 함께 전체 인증 뼈대 코드를 직접 프로젝트에 복사해줍니다. Breeze는 Fortify와 달리 라우트와 컨트롤러를 애플리케이션 내부로 직접 복사해주기 때문에, Laravel의 인증 기능을 소스코드를 통해 직접 공부하고 익힐 수 있습니다.

<!-- Laravel Fortify essentially takes the routes and controllers of Laravel Breeze and offers them as a package that does not include a user interface. This allows you to still quickly scaffold the backend implementation of your application's authentication layer without being tied to any particular frontend opinions. -->
Fortify는 Laravel Breeze의 라우트와 컨트롤러를 패키지 형태로 제공하며, UI 부분은 포함하지 않습니다. 덕분에 특정 프론트엔드 라이브러리에 종속되지 않고도 인증 백엔드 구현을 빠르게 설정할 수 있습니다.

<a name="when-should-i-use-fortify"></a>
<!-- ### When Should I Use Fortify? -->
### When Should I Use Fortify?

<!-- You may be wondering when it is appropriate to use Laravel Fortify. First, if you are using one of Laravel's [application starter kits](/docs/11.x/starter-kits), you do not need to install Laravel Fortify since all of Laravel's application starter kits already provide a full authentication implementation. -->
Laravel Fortify 사용 시점에 대해 고민할 수 있습니다. 먼저, [application starter kits](/docs/11.x/starter-kits)를 사용하는 경우, 별도의 Fortify 설치가 필요 없습니다. 시작 키트들은 이미 완전한 인증 구현을 제공합니다.

<!-- If you are not using an application starter kit and your application needs authentication features, you have two options: manually implement your application's authentication features or use Laravel Fortify to provide the backend implementation of these features. -->
별도의 시작 키트를 사용하지 않고 애플리케이션에 인증 기능이 필요하다면, 인증을 직접 구현하거나 Fortify를 설치하여 인증 백엔드를 구축할 수 있습니다.

<!-- If you choose to install Fortify, your user interface will make requests to Fortify's authentication routes that are detailed in this documentation in order to authenticate and register users. -->
Fortify를 설치했다면, 직접 만든 사용자 인터페이스에서 이 문서에서 안내하는 Fortify가 등록한 인증 라우트에 요청을 보내는 방식을 사용하게 됩니다.

<!-- If you choose to manually interact with Laravel's authentication services instead of using Fortify, you may do so by following the documentation available in the [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), and [email verification](/docs/11.x/verification) documentation. -->
Fortify 없이 인증 기능을 직접 구현하려면, [authentication](/docs/11.x/authentication), [password reset](/docs/11.x/passwords), [email verification](/docs/11.x/verification) 문서를 참고하면 됩니다.

<a name="laravel-fortify-and-laravel-sanctum"></a>
<!-- #### Laravel Fortify and Laravel Sanctum -->
#### Laravel Fortify and Laravel Sanctum

<!-- Some developers become confused regarding the difference between [Laravel Sanctum](/docs/11.x/sanctum) and Laravel Fortify. Because the two packages solve two different but related problems, Laravel Fortify and Laravel Sanctum are not mutually exclusive or competing packages. -->
[Laravel Sanctum](/docs/11.x/sanctum)과 Fortify의 차이점 때문에 혼란스러울 수 있습니다. 두 패키지는 서로 다른 문제를 해결하기 때문에, Fortify와 Sanctum은 경쟁하거나 상호 배타적인 패키지가 아닙니다.

<!-- Laravel Sanctum is only concerned with managing API tokens and authenticating existing users using session cookies or tokens. Sanctum does not provide any routes that handle user registration, password reset, etc. -->
Laravel Sanctum은 API 토큰 관리와 기존 사용자의 세션 쿠키 또는 토큰 인증만 담당합니다. 즉, Sanctum은 회원가입, 비밀번호 재설정 같은 라우트를 제공하지 않습니다.

<!-- If you are attempting to manually build the authentication layer for an application that offers an API or serves as the backend for a single-page application, it is entirely possible that you will utilize both Laravel Fortify (for user registration, password reset, etc.) and Laravel Sanctum (API token management, session authentication). -->
API 백엔드를 직접 구축하거나 싱글 페이지 애플리케이션(SPA) 백엔드를 만들 계획이라면, Fortify(회원가입, 비밀번호 재설정 등)와 Sanctum(API 토큰 관리, 세션 인증)을 함께 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Fortify using the Composer package manager: -->
먼저 Composer 패키지 매니저를 사용해 Fortify를 설치합니다.

```shell
composer require laravel/fortify
```

<!-- Next, publish Fortify's resources using the `fortify:install` Artisan command: -->
다음으로, Fortify의 리소스를 `fortify:install` 아티즌 명령어로 퍼블리시합니다.

```shell
php artisan fortify:install
```

<!-- This command will publish Fortify's actions to your `app/Actions` directory, which will be created if it does not exist. In addition, the `FortifyServiceProvider`, configuration file, and all necessary database migrations will be published. -->
이 명령어를 실행하면 `app/Actions` 디렉터리(없다면 생성됨)에 Fortify의 액션 파일들이 퍼블리시됩니다. 또한 `FortifyServiceProvider`, 설정 파일, 필요한 모든 데이터베이스 마이그레이션 파일도 함께 등록됩니다.

<!-- Next, you should migrate your database: -->
이후 데이터베이스 마이그레이션을 실행하세요.

```shell
php artisan migrate
```

<a name="fortify-features"></a>
<!-- ### Fortify Features -->
### Fortify Features

<!-- The `fortify` configuration file contains a `features` configuration array. This array defines which backend routes / features Fortify will expose by default. If you are not using Fortify in combination with [Laravel Jetstream](https://jetstream.laravel.com), we recommend that you only enable the following features, which are the basic authentication features provided by most Laravel applications: -->
`fortify` 설정 파일에는 `features` 설정 배열이 있습니다. 이 배열에서 Fortify가 기본적으로 제공할 백엔드 라우트 및 기능을 설정할 수 있습니다. [Laravel Jetstream](https://jetstream.laravel.com)과 함께 Fortify를 쓰지 않는다면, Laravel에서 흔히 사용하는 기본 인증 기능만 활성화하기를 권장합니다.

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
기본적으로 Fortify는 로그인/회원가입 화면 등 뷰를 반환하는 라우트도 정의합니다. 하지만 Javascript 기반의 싱글 페이지 애플리케이션을 만든다면 이런 뷰 라우트가 필요 없을 수 있습니다. 이럴 때는 애플리케이션의 `config/fortify.php` 설정 파일에서 `views` 옵션을 `false`로 설정하여 뷰 라우트 전체를 비활성화할 수 있습니다.

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
<!-- #### Disabling Views and Password Reset -->
#### Disabling Views and Password Reset

<!-- If you choose to disable Fortify's views and you will be implementing password reset features for your application, you should still define a route named `password.reset` that is responsible for displaying your application's "reset password" view. This is necessary because Laravel's `Illuminate\Auth\Notifications\ResetPassword` notification will generate the password reset URL via the `password.reset` named route. -->
Fortify의 뷰 기능을 비활성화하면서, 애플리케이션에서 비밀번호 재설정 기능은 구현할 계획이라면, 여전히 새로운 "비밀번호 재설정" 뷰를 보여주는 별도의 `password.reset` 이름의 라우트를 정의해야 합니다. 이유는 Laravel의 `Illuminate\Auth\Notifications\ResetPassword` 알림이 `password.reset` 네임드 라우트를 통해 비밀번호 재설정 URL을 생성하기 때문입니다.

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- To get started, we need to instruct Fortify how to return our "login" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/11.x/starter-kits). -->
인증 기능을 구현하려면 먼저 Fortify가 "로그인" 뷰를 어떻게 반환할지 알려주어야 합니다. Fortify는 UI가 없는(=헤드리스) 인증 라이브러리임을 다시 한번 떠올리세요. 이미 완성된 인증 UI가 필요하다면 [application starter kit](/docs/11.x/starter-kits)를 사용하는 것이 더 쉽습니다.

<!-- All of the authentication view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class. Fortify will take care of defining the `/login` route that returns this view: -->
인증 화면의 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 사용해 언제든 커스터마이징할 수 있습니다. 보통, 이 코드는 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다. Fortify는 `/login` 라우트를 자동으로 정의하여, 지정한 뷰를 반환하게 해 줍니다.

```
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
로그인 템플릿에는 `/login` 엔드포인트로 POST 요청하는 폼이 포함되어야 합니다. `/login` 엔드포인트는 문자열 타입의 `email` 또는 `username`과 `password` 필드를 기대합니다. 이때, email/username 필드의 이름은 설정 파일 `config/fortify.php`의 `username` 값과 일치해야 합니다. 추가로, "로그인 상태 유지" 기능을 원한다면 불린값 `remember` 필드를 함께 전송할 수 있습니다.

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. -->
로그인에 성공하면, Fortify는 애플리케이션의 `fortify` 설정 파일에서 `home` 옵션으로 지정한 URI로 리디렉트합니다. 만약 로그인 요청이 XHR 요청이었다면 200 HTTP 응답만 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the login screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with the 422 HTTP response. -->
로그인 실패 시에는 다시 로그인 화면으로 리디렉트되고, 유효성 검증 에러 메시지는 공유 변수인 `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors)로 조회할 수 있습니다. 또한 XHR 요청의 경우 422 HTTP 응답과 함께 검증 에러가 반환됩니다.

<a name="customizing-user-authentication"></a>
<!-- ### Customizing User Authentication -->
### Customizing User Authentication

<!-- Fortify will automatically retrieve and authenticate the user based on the provided credentials and the authentication guard that is configured for your application. However, you may sometimes wish to have full customization over how login credentials are authenticated and users are retrieved. Thankfully, Fortify allows you to easily accomplish this using the `Fortify::authenticateUsing` method. -->
Fortify는 제공된 자격 증명과 애플리케이션의 인증 가드를 바탕으로 사용자를 자동으로 인증합니다. 그러나, 로그인 자격 증명 검증과 사용자 조회 방식을 완전히 직접 제어하고 싶을 때가 있습니다. 이럴 때는 `Fortify::authenticateUsing` 메서드로 손쉽게 커스터마이즈할 수 있습니다.

<!-- This method accepts a closure which receives the incoming HTTP request. The closure is responsible for validating the login credentials attached to the request and returning the associated user instance. If the credentials are invalid or no user can be found, `null` or `false` should be returned by the closure. Typically, this method should be called from the `boot` method of your `FortifyServiceProvider`: -->
이 메서드는 HTTP 요청 객체를 받는 클로저를 인자로 받습니다. 이 클로저에서 로그인 자격 증명을 검증하고, 해당 사용자를 찾아 반환해야 합니다. 자격 증명이 올바르지 않거나 해당 사용자가 없다면 `null` 또는 `false`를 반환해야 합니다. 해당 코드는 보통 `FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

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
Fortify에서 사용할 인증 가드는 애플리케이션의 `fortify` 설정 파일에서 커스터마이징할 수 있습니다. 단, 반드시 `Illuminate\Contracts\Auth\StatefulGuard` 인터페이스의 구현체여야 합니다. SPA에서 Laravel Fortify 인증을 사용하려면, Laravel 기본 `web` 가드와 [Laravel Sanctum](https://laravel.com/docs/sanctum)을 함께 쓰는 방식을 추천합니다.

<a name="customizing-the-authentication-pipeline"></a>
<!-- ### Customizing the Authentication Pipeline -->
### Customizing the Authentication Pipeline

<!-- Laravel Fortify authenticates login requests through a pipeline of invokable classes. If you would like, you may define a custom pipeline of classes that login requests should be piped through. Each class should have an `__invoke` method which receives the incoming `Illuminate\Http\Request` instance and, like [middleware](/docs/11.x/middleware), a `$next` variable that is invoked in order to pass the request to the next class in the pipeline. -->
Laravel Fortify는 인증(로그인) 요청을 일련의 호출 가능한(Invokable) 클래스 파이프라인을 통해 처리합니다. 원한다면, 로그인 요청 시 거쳐야 할 커스텀 파이프라인 클래스를 직접 정의할 수 있습니다. 각 클래스에는 `__invoke` 메서드가 있어야 하며, [middleware](/docs/11.x/middleware)처럼 최초 인자로 `Illuminate\Http\Request` 인스턴스와, `$next` 변수(다음 클래스 실행시 호출)가 전달됩니다.

<!-- To define your custom pipeline, you may use the `Fortify::authenticateThrough` method. This method accepts a closure which should return the array of classes to pipe the login request through. Typically, this method should be called from the `boot` method of your `App\Providers\FortifyServiceProvider` class. -->
커스텀 파이프라인 정의는 `Fortify::authenticateThrough` 메서드를 통해 할 수 있습니다. 이 메서드는, 로그인 요청을 거칠 클래스 배열을 반환해야 하는 클로저를 인자로 받습니다. 이 역시 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 일반적입니다.

<!-- The example below contains the default pipeline definition that you may use as a starting point when making your own modifications: -->
아래는 각 항목을 커스터마이징하기 위한 기본 파이프라인 정의 예시입니다.

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
기본적으로 Fortify는 `EnsureLoginIsNotThrottled` 미들웨어를 통해 인증 시도를 제한합니다. 이 미들웨어는 사용자명과 IP 주소 조합별로 시도를 제한합니다.

<!-- Some applications may require a different approach to throttling authentication attempts, such as throttling by IP address alone. Therefore, Fortify allows you to specify your own [rate limiter](/docs/11.x/routing#rate-limiting) via the `fortify.limiters.login` configuration option. Of course, this configuration option is located in your application's `config/fortify.php` configuration file. -->
일부 애플리케이션에서는 IP 주소 단독으로 제한하는 등, 다른 접근법이 필요할 수 있습니다. Fortify는 이런 경우를 위해 `fortify.limiters.login` 설정 옵션을 통해 [rate limiter](/docs/11.x/routing#rate-limiting)를 지정할 수 있게 지원합니다. 이 옵션은 `config/fortify.php` 설정 파일에 있습니다.

> [!NOTE]
> 인증 시도 제한, [two factor authentication](/docs/11.x/fortify#two-factor-authentication), 외부 웹 애플리케이션 방화벽(WAF)을 함께 사용하면, 실제 사용자에게 훨씬 더 강력한 보안을 제공할 수 있습니다.

<a name="customizing-authentication-redirects"></a>
<!-- ### Customizing Redirects -->
### Customizing Redirects

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. After a user logs out of the application, the user will be redirected to the `/` URI. -->
로그인에 성공하면, Fortify는 애플리케이션의 `fortify` 설정 파일에서 `home` 옵션으로 지정된 URI로 리디렉션합니다. 로그인 요청이 XHR이었다면 200 HTTP 응답을 반환합니다. 사용자가 로그아웃하면 `/` URI로 리디렉션됩니다.

<!-- If you need advanced customization of this behavior, you may bind implementations of the `LoginResponse` and `LogoutResponse` contracts into the Laravel [service container](/docs/11.x/container). Typically, this should be done within the `register` method of your application's `App\Providers\FortifyServiceProvider` class: -->
이 리디렉션 동작을 더 세밀하게 제어하려면, `LoginResponse` 및 `LogoutResponse` 계약(Contract) 구현체를 Laravel [service container](/docs/11.x/container)에 바인딩해야 합니다. 일반적으로 이 코드는 `App\Providers\FortifyServiceProvider`의 `register` 메서드에서 등록합니다.

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
<!-- ## Two Factor Authentication -->
## Two Factor Authentication

<!-- When Fortify's two factor authentication feature is enabled, the user is required to input a six digit numeric token during the authentication process. This token is generated using a time-based one-time password (TOTP) that can be retrieved from any TOTP compatible mobile authentication application such as Google Authenticator. -->
Fortify의 이중 인증(2FA) 기능을 활성화하면, 인증 과정에서 6자리 숫자 토큰 입력을 추가로 요구하게 됩니다. 이 토큰은 TOTP(Time-based One-Time Password) 방식으로 생성되며, Google Authenticator 등 TOTP를 지원하는 모바일 인증 앱에서 받아올 수 있습니다.

<!-- Before getting started, you should first ensure that your application's `App\Models\User` model uses the `Laravel\Fortify\TwoFactorAuthenticatable` trait: -->
먼저, 여러분의 앱의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인하세요.

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
그 다음, 사용자들이 이중 인증 설정을 직접 관리할 수 있는 화면을 만드세요. 이곳에서는 이중 인증 활성화/비활성화, 리커버리 코드 재생성 등이 가능해야 합니다.

> 기본적으로 `fortify` 설정 파일의 `features` 배열에 따라, 이중 인증 설정을 변경할 때 비밀번호 확인이 요구됩니다. 따라서, 먼저 Fortify의 [password confirmation](#password-confirmation) 기능을 반드시 구현해두는 것이 좋습니다.

<a name="enabling-two-factor-authentication"></a>
<!-- ### Enabling Two Factor Authentication -->
### Enabling Two Factor Authentication

<!-- To begin enabling two factor authentication, your application should make a POST request to the `/user/two-factor-authentication` endpoint defined by Fortify. If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-enabled`. You may detect this `status` session variable within your templates to display the appropriate success message. If the request was an XHR request, `200` HTTP response will be returned. -->
이중 인증을 활성화하려면, 애플리케이션에서 Fortify가 정의한 `/user/two-factor-authentication` 엔드포인트로 POST 요청을 보내면 됩니다. 요청 성공 시, 사용자는 이전 URL로 리다이렉트되고 `status` 세션 변수가 `two-factor-authentication-enabled`로 설정됩니다. 템플릿에서 이 `status` 세션 변수를 감지해 적절한 성공 메시지를 표시할 수 있습니다. XHR 요청의 경우에는 `200` HTTP 응답이 반환됩니다.

<!-- After choosing to enable two factor authentication, the user must still "confirm" their two factor authentication configuration by providing a valid two factor authentication code. So, your "success" message should instruct the user that two factor authentication confirmation is still required: -->
이중 인증 활성화 직후에는, 사용자가 실제로 올바른 이중 인증 코드를 입력해 인증을 "확정"해야 기능이 활성화된 것으로 처리됩니다. 따라서 성공 메시지에는 이중 인증 확정 단계가 남았음을 안내해야 합니다.

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two factor authentication below.
    </div>
@endif
```

<!-- Next, you should display the two factor authentication QR code for the user to scan into their authenticator application. If you are using Blade to render your application's frontend, you may retrieve the QR code SVG using the `twoFactorQrCodeSvg` method available on the user instance: -->
다음 단계로, 사용자가 인증 앱으로 스캔할 수 있는 이중 인증 QR 코드를 보여주어야 합니다. Blade를 이용해 프론트엔드를 구현한다면, 사용자 모델의 `twoFactorQrCodeSvg` 메서드로 QR코드 SVG를 받아올 수 있습니다.

```php
$request->user()->twoFactorQrCodeSvg();
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-qr-code` endpoint to retrieve the user's two factor authentication QR code. This endpoint will return a JSON object containing an `svg` key. -->
Javascript 기반 프론트엔드라면, `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 보내면, JSON 형식으로 `svg` 값을 받을 수 있습니다.

<a name="confirming-two-factor-authentication"></a>
<!-- #### Confirming Two Factor Authentication -->
#### Confirming Two Factor Authentication

<!-- In addition to displaying the user's two factor authentication QR code, you should provide a text input where the user can supply a valid authentication code to "confirm" their two factor authentication configuration. This code should be provided to the Laravel application via a POST request to the `/user/confirmed-two-factor-authentication` endpoint defined by Fortify. -->
QR 코드 표시와 함께, 사용자가 직접 인증 코드를 입력하는 폼을 제공해 "이중 인증 확정"을 진행해야 합니다. 이 코드는 Fortify가 정의한 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청됩니다.

<!-- If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-confirmed`: -->
요청이 성공하면, 이전 화면으로 리디렉션되며, 세션의 `status` 값이 `two-factor-authentication-confirmed`로 설정됩니다.

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two factor authentication confirmed and enabled successfully.
    </div>
@endif
```

<!-- If the request to the two factor authentication confirmation endpoint was made via an XHR request, a `200` HTTP response will be returned. -->
이중 인증 확인 엔드포인트로의 요청이 XHR 요청으로 이루어진 경우, `200` HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
<!-- #### Displaying the Recovery Codes -->
#### Displaying the Recovery Codes

<!-- You should also display the user's two factor recovery codes. These recovery codes allow the user to authenticate if they lose access to their mobile device. If you are using Blade to render your application's frontend, you may access the recovery codes via the authenticated user instance: -->
이중 인증 사용자는, 만약 기기에 접근할 수 없게 된 경우 리커버리 코드를 이용해 인증할 수 있습니다. Blade 프론트엔드에서는 인증된 사용자 인스턴스를 통해 다음과 같이 리커버리 코드를 조회할 수 있습니다.

```php
(array) $request->user()->recoveryCodes()
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-recovery-codes` endpoint. This endpoint will return a JSON array containing the user's recovery codes. -->
Javascript 프론트엔드라면, `/user/two-factor-recovery-codes` 엔드포인트에 XHR GET 요청을 보내면 리커버리 코드 배열(JSON)이 반환됩니다.

<!-- To regenerate the user's recovery codes, your application should make a POST request to the `/user/two-factor-recovery-codes` endpoint. -->
리커버리 코드 재생성을 원한다면, `/user/two-factor-recovery-codes` 엔드포인트에 POST 요청을 보내면 됩니다.

<a name="authenticating-with-two-factor-authentication"></a>
<!-- ### Authenticating With Two Factor Authentication -->
### Authenticating With Two Factor Authentication

<!-- During the authentication process, Fortify will automatically redirect the user to your application's two factor authentication challenge screen. However, if your application is making an XHR login request, the JSON response returned after a successful authentication attempt will contain a JSON object that has a `two_factor` boolean property. You should inspect this value to know whether you should redirect to your application's two factor authentication challenge screen. -->
인증 과정에서 Fortify는 자동으로 사용자를 앱의 이중 인증 도전 화면(Challenge Screen)으로 리디렉션합니다. 만약 로그인 요청을 XHR 방식으로 보냈다면, 인증 성공 후 JSON 응답에 `two_factor`라는 불린값 프로퍼티가 포함되어 있습니다. 이 값을 활용해 두 번째 단계 인증화면으로 전환할지 결정할 수 있습니다.

<!-- To begin implementing two factor authentication functionality, we need to instruct Fortify how to return our two factor authentication challenge view. All of Fortify's authentication view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
이중 인증 기능 구현을 위해, Fortify가 이중 인증 도전 뷰를 반환하는 방법을 알려야 합니다. 모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스 메서드로 커스터마이징할 수 있습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 정의합니다.

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
Fortify는 이 뷰를 반환하는 `/two-factor-challenge` 라우트를 자동으로 정의합니다. `two-factor-challenge` 템플릿에는 `/two-factor-challenge` 엔드포인트로 POST 요청하는 폼이 필요합니다. `/two-factor-challenge` 액션은 유효한 TOTP 토큰을 담은 `code` 필드 또는 사용자의 복구 코드 중 하나를 담은 `recovery_code` 필드를 기대합니다.

<!-- If the login attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 204 HTTP response will be returned. -->
로그인에 성공하면, Fortify는 `fortify` 설정 파일의 `home` 옵션에 설정된 URI로 리디렉션합니다. XHR 요청의 경우 204 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the two factor challenge screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
인증 실패 시에는 다시 두 번째 인증 화면으로 돌아가며, 유효성 검증 에러는 `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors)로 노출됩니다. XHR 요청은 422 HTTP 응답과 함께 에러를 반환합니다.

<a name="disabling-two-factor-authentication"></a>
<!-- ### Disabling Two Factor Authentication -->
### Disabling Two Factor Authentication

<!-- To disable two factor authentication, your application should make a DELETE request to the `/user/two-factor-authentication` endpoint. Remember, Fortify's two factor authentication endpoints require [password confirmation](#password-confirmation) prior to being called. -->
이중 인증을 비활성화하려면 `/user/two-factor-authentication` 엔드포인트로 DELETE 요청을 보내면 됩니다. Fortify의 이중 인증 관련 엔드포인트 호출 전에는 [password confirmation](#password-confirmation)이 요구됩니다.

<a name="registration"></a>
<!-- ## Registration -->
## Registration

<!-- To begin implementing our application's registration functionality, we need to instruct Fortify how to return our "register" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/11.x/starter-kits). -->
회원가입 기능을 구현하려면, Fortify가 "회원가입" 뷰를 반환하는 방식을 알려주어야 합니다. Fortify는 UI가 없는 인증 라이브러리라는 점을 다시 한번 떠올리세요. 이미 완성된 인증 UI 구현이 필요하다면 [application starter kit](/docs/11.x/starter-kits)를 사용하는 것이 더 쉽습니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your `App\Providers\FortifyServiceProvider` class: -->
모든 인증 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스의 메서드를 사용해 커스터마이징할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출하게 됩니다.

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
Fortify는 `/register` 라우트를 자동으로 정의해 지정한 뷰를 반환합니다. `register` 템플릿에는 `/register` 엔드포인트로 POST 요청하는 폼이 필요합니다.

<!-- The `/register` endpoint expects a string `name`, string email address / username, `password`, and `password_confirmation` fields. The name of the email / username field should match the `username` configuration value defined within your application's `fortify` configuration file. -->
`/register` 엔드포인트는 문자열 타입의 `name`, email 또는 username, `password`, `password_confirmation` 필드를 기대합니다. email/username 필드의 이름은 애플리케이션의 `fortify` 설정 파일에 정의된 `username` 설정값과 일치해야 합니다.

<!-- If the registration attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the request was an XHR request, a 201 HTTP response will be returned. -->
회원가입에 성공하면, Fortify는 애플리케이션의 `fortify` 설정 파일에서 `home` 옵션으로 지정한 URI로 리디렉션하며, XHR 요청일 경우 201 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the registration screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
회원가입 실패 시, 다시 회원가입 화면으로 돌아가며, 유효성 검증 에러는 [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors)인 `$errors`로, XHR 요청일 경우 422 HTTP 응답에 포함되어 반환됩니다.

<a name="customizing-registration"></a>
<!-- ### Customizing Registration -->
### Customizing Registration

<!-- The user validation and creation process may be customized by modifying the `App\Actions\Fortify\CreateNewUser` action that was generated when you installed Laravel Fortify. -->
사용자 검증 및 생성 과정은 Fortify 설치 시 자동 생성되는 `App\Actions\Fortify\CreateNewUser` 액션 파일을 수정하여 커스터마이즈할 수 있습니다.

<a name="password-reset"></a>
<!-- ## Password Reset -->
## Password Reset

<a name="requesting-a-password-reset-link"></a>
<!-- ### Requesting a Password Reset Link -->
### Requesting a Password Reset Link

<!-- To begin implementing our application's password reset functionality, we need to instruct Fortify how to return our "forgot password" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/11.x/starter-kits). -->
비밀번호 재설정 기능 구현을 시작하려면, Fortify가 "비밀번호 찾기(비밀번호 재설정 링크 요청)" 뷰를 반환하도록 알려주어야 합니다. Fortify는 프론트엔드가 없는 헤드리스 인증 라이브러리임을 유념하세요. 완성된 인증 UI가 필요하다면 [application starter kit](/docs/11.x/starter-kits)가 더 적합합니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 방식은 `Laravel\Fortify\Fortify` 클래스의 메서드를 통해 원하는 대로 커스터마이징할 수 있습니다. 일반적으로 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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
Fortify는 `/forgot-password` 엔드포인트를 자동 정의해 위 뷰를 반환합니다. `forgot-password` 템플릿에는 `/forgot-password` 엔드포인트로 POST 요청하는 폼이 필요합니다.

<!-- The `/forgot-password` endpoint expects a string `email` field. The name of this field / database column should match the `email` configuration value within your application's `fortify` configuration file. -->
`/forgot-password` 엔드포인트는 문자열 타입의 `email` 필드를 요구하며, 필드/컬럼 이름은 애플리케이션의 `fortify` 설정 파일 내 `email` 값과 일치해야 합니다.

<a name="handling-the-password-reset-link-request-response"></a>
<!-- #### Handling the Password Reset Link Request Response -->
#### Handling the Password Reset Link Request Response

<!-- If the password reset link request was successful, Fortify will redirect the user back to the `/forgot-password` endpoint and send an email to the user with a secure link they can use to reset their password. If the request was an XHR request, a 200 HTTP response will be returned. -->
비밀번호 재설정 링크 요청에 성공하면, 사용자는 `/forgot-password` 페이지로 다시 리디렉션되며, 동시에 비밀번호 재설정 링크가 포함된 이메일을 받게 됩니다. XHR 요청의 경우 200 HTTP 응답을 반환합니다.

<!-- After being redirected back to the `/forgot-password` endpoint after a successful request, the `status` session variable may be used to display the status of the password reset link request attempt. -->
성공 후 `/forgot-password`로 돌아왔을 때, 세션의 `status` 변수를 통해 요청 상태를 화면에 표시할 수 있습니다.

<!-- The value of the `$status` session variable will match one of the translation strings defined within your application's `passwords` [language file](/docs/11.x/localization). If you would like to customize this value and have not published Laravel's language files, you may do so via the `lang:publish` Artisan command: -->
`$status` 세션 변수의 값은 애플리케이션의 `passwords` [language file](/docs/11.x/localization)에 정의된 번역 문자열 중 하나와 일치합니다. 이 값을 직접 커스터마이즈하려면, Laravel 언어 파일을 퍼블리시(`lang:publish`)하면 됩니다.

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was not successful, the user will be redirected back to the request password reset link screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
요청이 실패했다면, 비밀번호 재설정 링크 요청 화면으로 돌아가고 검증 에러는 [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors)인 `$errors`로 확인할 수 있습니다. XHR 요청은 422 HTTP 응답과 함께 에러를 반환합니다.

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<!-- To finish implementing our application's password reset functionality, we need to instruct Fortify how to return our "reset password" view. -->
비밀번호 재설정 기능을 완성하려면, Fortify가 "비밀번호 재설정" 뷰를 반환하도록 지정해야 합니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 반환 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 원하는 대로 커스터마이징할 수 있습니다. 보통 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 설정합니다.

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
Fortify는 해당 뷰를 보여주는 라우트를 자동으로 정의합니다. `reset-password` 템플릿에는 `/reset-password` 라우트로 POST 요청하는 폼이 필요합니다.

<!-- The `/reset-password` endpoint expects a string `email` field, a `password` field, a `password_confirmation` field, and a hidden field named `token` that contains the value of `request()->route('token')`. The name of the "email" field / database column should match the `email` configuration value defined within your application's `fortify` configuration file. -->
`/reset-password` 엔드포인트는 문자열 타입의 `email` 필드, `password` 필드, `password_confirmation` 필드, 그리고 `request()->route('token')` 값을 담는 숨겨진 `token` 필드를 요구합니다. "email" 필드/컬럼 이름은 애플리케이션의 `fortify` 설정 파일에 정의된 `email` 설정값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
<!-- #### Handling the Password Reset Response -->
#### Handling the Password Reset Response

<!-- If the password reset request was successful, Fortify will redirect back to the `/login` route so that the user can log in with their new password. In addition, a `status` session variable will be set so that you may display the successful status of the reset on your login screen: -->
비밀번호 재설정에 성공하면, Fortify는 `/login` 라우트로 리디렉션하여 사용자가 새 비밀번호로 로그인할 수 있게 해줍니다. 또한 세션에 `status` 값이 저장되어 있으므로, 로그인 화면에서 성공 메시지를 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was an XHR request, a 200 HTTP response will be returned. -->
XHR 요청일 경우 200 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the reset password screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
실패 시에는 비밀번호 재설정 화면으로 돌아가고, 검증 에러는 [Blade template variable](/docs/11.x/validation#quick-displaying-the-validation-errors)인 `$errors`나 XHR 요청의 경우 422 HTTP 응답으로 반환됩니다.

<a name="customizing-password-resets"></a>
<!-- ### Customizing Password Resets -->
### Customizing Password Resets

<!-- The password reset process may be customized by modifying the `App\Actions\ResetUserPassword` action that was generated when you installed Laravel Fortify. -->
비밀번호 재설정 과정은 Fortify 설치 시 생성된 `App\Actions\ResetUserPassword` 액션 파일을 수정하여 커스터마이즈할 수 있습니다.

<a name="email-verification"></a>
<!-- ## Email Verification -->
## Email Verification

<!-- After registration, you may wish for users to verify their email address before they continue accessing your application. To get started, ensure the `emailVerification` feature is enabled in your `fortify` configuration file's `features` array. Next, you should ensure that your `App\Models\User` class implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface. -->
회원가입 이후, 사용자가 본인 소유의 이메일 주소임을 인증하도록 하고 싶을 수 있습니다. 먼저, `fortify` 설정 파일의 `features` 배열에서 `emailVerification` 기능을 활성화하세요. 그리고 `App\Models\User` 클래스가 반드시 `Illuminate\Contracts\Auth\MustVerifyEmail` 인터페이스를 구현해야 합니다.

<!-- Once these two setup steps have been completed, newly registered users will receive an email prompting them to verify their email address ownership. However, we need to inform Fortify how to display the email verification screen which informs the user that they need to go click the verification link in the email. -->
이 세팅을 마치면, 새로 가입한 사용자에게 이메일 인증을 유도하는 이메일이 발송됩니다. 이제 Fortify가 이메일 인증 화면을 어떻게 보여줄지 지정해야 합니다. 이 화면은 사용자가 인증 메일의 링크를 클릭해야 함을 안내하는 역할을 합니다.

<!-- All of Fortify's view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 Fortify 뷰 반환 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 커스터마이즈할 수 있습니다. 대개 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 구현합니다.

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
Fortify는 `/email/verify` 엔드포인트에 연결되어, 사용자가 Laravel의 내장 `verified` 미들웨어 적용 라우트에 접근할 때 해당 뷰를 보여줍니다.

<!-- Your `verify-email` template should include an informational message instructing the user to click the email verification link that was sent to their email address. -->
`verify-email` 템플릿에서는 이메일 인증 메일의 링크를 클릭해야 한다는 안내 메시지를 포함해야 합니다.

<a name="resending-email-verification-links"></a>
<!-- #### Resending Email Verification Links -->
#### Resending Email Verification Links

<!-- If you wish, you may add a button to your application's `verify-email` template that triggers a POST request to the `/email/verification-notification` endpoint. When this endpoint receives a request, a new verification email link will be emailed to the user, allowing the user to get a new verification link if the previous one was accidentally deleted or lost. -->
원한다면, `verify-email` 템플릿에 `/email/verification-notification` 엔드포인트로 POST 요청하는 버튼을 추가할 수 있습니다. 이 엔드포인트는 새 인증 이메일을 전송하므로, 사용자가 인증 메일을 실수로 지웠거나 분실한 경우 적합합니다.

<!-- If the request to resend the verification link email was successful, Fortify will redirect the user back to the `/email/verify` endpoint with a `status` session variable, allowing you to display an informational message to the user informing them the operation was successful. If the request was an XHR request, a 202 HTTP response will be returned: -->
성공적으로 인증 메일이 재발송되면, Fortify는 `/email/verify`로 리디렉션하면서 세션의 `status` 변수를 통해 성공 메시지 표시가 가능하게 합니다. XHR 요청의 경우 202 HTTP 응답을 반환합니다.

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
특정 라우트(또는 라우트 그룹)는 반드시 사용자 이메일이 인증된 경우에만 접근 가능하도록 만들 수 있습니다. 이럴 때는 Laravel 내장 `verified` 미들웨어를 해당 라우트에 적용하면 됩니다. `verified` 미들웨어 별칭은 Laravel이 자동으로 등록해 주며, 실제로는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭입니다.

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed. Typically, these routes are protected by Laravel's built-in `password.confirm` middleware. -->
애플리케이션에서 사용자가 중요한 작업을 하기 전에 비밀번호 확인을 요구하고 싶을 때가 있습니다. 보통, 이런 라우트에는 Laravel 내장 `password.confirm` 미들웨어를 사용합니다.

<!-- To begin implementing password confirmation functionality, we need to instruct Fortify how to return our application's "password confirmation" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/11.x/starter-kits). -->
이 기능 구현을 위해서는 Fortify가 "비밀번호 확인" 화면 뷰를 반환하도록 지정해야 합니다. Fortify는 UI가 없는 인증 라이브러리라는 점을 다시 기억하세요. 완성된 인증 UI 구현을 원한다면 [application starter kit](/docs/11.x/starter-kits)를 사용해도 좋습니다.

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 직접 커스터마이즈할 수 있습니다. 일반적으로 `App\Providers\FortifyServiceProvider`의 `boot` 메서드에서 호출합니다.

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
Fortify는 이 뷰를 반환하는 `/user/confirm-password` 엔드포인트를 정의합니다. `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트로 POST 요청하는 폼이 필요합니다. `/user/confirm-password` 엔드포인트는 사용자의 현재 비밀번호를 담은 `password` 필드를 기대합니다.

<!-- If the password matches the user's current password, Fortify will redirect the user to the route they were attempting to access. If the request was an XHR request, a 201 HTTP response will be returned. -->
입력한 비밀번호가 현재 비밀번호와 일치하면, Fortify는 사용자가 원래 접근하려 했던 라우트로 리디렉션합니다. XHR 요청일 경우 201 HTTP 응답을 반환합니다.

<!-- If the request was not successful, the user will be redirected back to the confirm password screen and the validation errors will be available to you via the shared `$errors` Blade template variable. Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
비밀번호가 일치하지 않을 경우, 다시 비밀번호 확인 화면으로 돌아가고 검증 에러는 Blade의 `$errors` 변수 또는 XHR 요청의 경우 422 HTTP 응답으로 전달됩니다.
