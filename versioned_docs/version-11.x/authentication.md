<!-- # Authentication -->
# Authentication

- [Introduction](#introduction)
    - [Starter Kits](#starter-kits)
    - [Database Considerations](#introduction-database-considerations)
    - [Ecosystem Overview](#ecosystem-overview)
- [Authentication Quickstart](#authentication-quickstart)
    - [Install a Starter Kit](#install-a-starter-kit)
    - [Retrieving the Authenticated User](#retrieving-the-authenticated-user)
    - [Protecting Routes](#protecting-routes)
    - [Login Throttling](#login-throttling)
- [Manually Authenticating Users](#authenticating-users)
    - [Remembering Users](#remembering-users)
    - [Other Authentication Methods](#other-authentication-methods)
- [HTTP Basic Authentication](#http-basic-authentication)
    - [Stateless HTTP Basic Authentication](#stateless-http-basic-authentication)
- [Logging Out](#logging-out)
    - [Invalidating Sessions on Other Devices](#invalidating-sessions-on-other-devices)
- [Password Confirmation](#password-confirmation)
    - [Configuration](#password-confirmation-configuration)
    - [Routing](#password-confirmation-routing)
    - [Protecting Routes](#password-confirmation-protecting-routes)
- [Adding Custom Guards](#adding-custom-guards)
    - [Closure Request Guards](#closure-request-guards)
- [Adding Custom User Providers](#adding-custom-user-providers)
    - [The User Provider Contract](#the-user-provider-contract)
    - [The Authenticatable Contract](#the-authenticatable-contract)
- [Automatic Password Rehashing](#automatic-password-rehashing)
<!-- - [Social Authentication](/docs/11.x/socialite) -->
- [Social Authentication](/docs/11.x/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
대부분의 웹 애플리케이션은 사용자들이 애플리케이션에 인증하여 "로그인"할 수 있는 방법을 제공합니다. 이 기능을 웹 애플리케이션에 직접 구현하려고 하면 복잡하거나 보안상 위험을 초래할 수 있습니다. Laravel은 이러한 이유로 인증 기능을 빠르고, 안전하며, 쉽게 구현할 수 있는 다양한 도구를 제공합니다.

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel의 인증 시스템은 기본적으로 "가드(guard)"와 "프로바이더(provider)"로 구성되어 있습니다. 가드는 각 요청에 대해 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel에는 세션 스토리지와 쿠키를 사용해 상태를 유지하는 `session` 가드가 기본으로 제공됩니다.

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/11.x/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
프로바이더는 사용자 정보를 영구 저장소(데이터베이스 등)에서 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/11.x/eloquent)와 데이터베이스 쿼리 빌더를 이용해 사용자를 조회하는 기본 기능을 제공합니다. 물론 필요하다면 애플리케이션에 맞게 추가 프로바이더를 정의할 수도 있습니다.

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel 인증 서비스 동작을 세부 조정할 수 있는 다양한 옵션과 그에 대한 자세한 설명이 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(role)"이나 "권한(permission)"과는 다릅니다. 권한을 통한 사용자 행위 인가에 대해 더 알고 싶다면 [authorization](/docs/11.x/authorization) 문서를 참고해 주세요.

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/11.x/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel application starter kit](/docs/11.x/starter-kits)를 설치해보세요. 데이터베이스 마이그레이션을 마친 후, `/register` 또는 애플리케이션에 할당된 URL로 브라우저에서 접속해 보시면 됩니다. 스타터 키트는 인증 시스템 전체의 구조를 자동으로 구성해 줍니다.

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing the [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) starter kit can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since Laravel Breeze creates authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**최종적으로 스타터 키트를 사용하지 않을 계획이더라도, [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) 스타터 키트를 설치해보면 실제 Laravel 프로젝트에서 인증 기능을 어떻게 구현하는지 배울 수 있는 훌륭한 기회가 됩니다.** Laravel Breeze는 인증 컨트롤러, 라우트, 뷰까지 모두 생성해 주므로, 파일 내 코드를 직접 확인하면서 Laravel의 인증 기능이 실제로 어떻게 동작하는지 학습할 수 있습니다.

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/11.x/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. -->
Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent model](/docs/11.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다.

<!-- If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. If your application is using MongoDB, check out MongoDB's official [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/) . -->
애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 사용할 수 있습니다. MongoDB를 사용하는 경우에는 MongoDB의 공식 [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 참고하세요.

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` 모델의 데이터베이스 스키마를 작성할 때, 비밀번호 컬럼(password)은 최소 60자 이상으로 설정해야 합니다. 사실, 새로운 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 충분히 긴 컬럼을 생성합니다.

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
또한, `users`(혹은 그에 준하는) 테이블에는 100자 길이의 null 허용 문자열 컬럼인 `remember_token` 컬럼이 있는지 확인해야 합니다. 이 컬럼은 사용자가 "로그인 상태 유지" 옵션을 선택할 경우 토큰을 저장하는 데 사용됩니다. 마찬가지로, Laravel 기본 `users` 테이블 마이그레이션에는 이미 해당 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel은 인증과 관련된 여러 패키지를 제공합니다. 본격적으로 시작하기 전에, Laravel의 전반적인 인증 생태계와 각 패키지의 목적에 대해 간략히 살펴보겠습니다.

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/11.x/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
우선 인증 방식의 개념부터 생각해 봅시다. 웹 브라우저에서 사용자는 로그인 폼을 통해 사용자명과 비밀번호를 입력합니다. 이 자격 증명이 정확하다면, 애플리케이션은 인증된 사용자 정보를 [session](/docs/11.x/session)에 저장합니다. 브라우저에 발급된 쿠키에는 세션 ID가 담기며, 이후 애플리케이션의 요청마다 이 세션 ID로 사용자를 식별할 수 있습니다. 세션 쿠키가 브라우저에 전달되면, 애플리케이션은 해당 세션 ID로 세션 데이터를 조회하고 인증 정보를 확인해서 사용자를 "인증됨" 상태로 간주합니다.

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
반면, 외부 서비스가 API에 접근하기 위해 인증해야 할 때에는 보통 쿠키를 사용하지 않습니다(브라우저가 없기 때문입니다). 대신, 외부 서비스는 매 요청마다 API 토큰을 전달합니다. 애플리케이션은 들어온 토큰을 유효한 토큰 테이블과 대조해 사용자를 인증하며, 해당 API 토큰을 가진 사용자가 요청을 보낸 것으로 판단합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel에는 `Auth` 및 `Session` 파사드를 통해 주로 접근하는 내장 인증, 세션 서비스가 포함되어 있습니다. 이 기능은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 다양한 메서드로 사용자의 자격 증명을 확인하고 인증 상태로 만들 수 있으며, 적절한 인증 데이터를 세션에 저장하고 세션 쿠키를 발급하는 작업도 자동으로 처리됩니다. 이러한 서비스의 활용법은 이 문서에서 자세히 다룹니다.

<!-- **Application Starter Kits** -->
**애플리케이션 스타터 키트**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free packages](/docs/11.x/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. These packages are [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/11.x/starter-kits#laravel-jetstream), and [Laravel Fortify](/docs/11.x/fortify). -->
문서에서 살펴보듯, 직접 인증 서비스를 활용해 나만의 인증 계층을 만들 수 있습니다. 하지만 더 빠르게 시작하고 싶다면, 인증 계층 전체를 견고하고 현대적으로 자동 구성해 주는 [free packages](/docs/11.x/starter-kits)를 활용할 수 있습니다. 현재 공식적으로 제공되는 패키지는 [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/11.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/11.x/fortify)입니다.

<!-- _Laravel Breeze_ is a simple, minimal implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is comprised of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). To get started, check out the documentation on Laravel's [application starter kits](/docs/11.x/starter-kits). -->
_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 Laravel 인증 기능을 매우 심플하고 최소한의 구현으로 제공합니다. 뷰는 [Blade templates](/docs/11.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 스타일링되어 있습니다. 자세한 시작 방법은 [application starter kits](/docs/11.x/starter-kits) 문서를 참고하세요.

<!-- _Laravel Fortify_ is a headless authentication backend for Laravel that implements many of the features found in this documentation, including cookie-based authentication as well as other features such as two-factor authentication and email verification. Fortify provides the authentication backend for Laravel Jetstream or may be used independently in combination with [Laravel Sanctum](/docs/11.x/sanctum) to provide authentication for an SPA that needs to authenticate with Laravel. -->
_Laravel Fortify_는 Laravel용 헤드리스(화면 없는) 인증 백엔드로, 여기에 설명된 기능(쿠키 인증, 2단계 인증, 이메일 인증 등)을 다수 구현합니다. Fortify는 Laravel Jetstream의 백엔드로 포함되거나, [Laravel Sanctum](/docs/11.x/sanctum)과 결합하여 단일 페이지 애플리케이션(SPA) 인증 백엔드로도 활용할 수 있습니다.

<!-- _[Laravel Jetstream](https://jetstream.laravel.com)_ is a robust application starter kit that consumes and exposes Laravel Fortify's authentication services with a beautiful, modern UI powered by [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), and / or [Inertia](https://inertiajs.com). Laravel Jetstream includes optional support for two-factor authentication, team support, browser session management, profile management, and built-in integration with [Laravel Sanctum](/docs/11.x/sanctum) to offer API token authentication. Laravel's API authentication offerings are discussed below. -->
_[Laravel Jetstream](https://jetstream.laravel.com)_은 Fortify의 인증 기능을 기본 내장으로 사용하면서, [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com)로 구성된 아름답고 현대적인 UI도 제공합니다. 옵션에 따라 2단계 인증, 팀 기능, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/11.x/sanctum)과의 연동으로 API 토큰 인증 등 다양한 편의 기능도 지원합니다. Laravel의 API 인증 기능은 아래에서 다시 다룹니다.

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/11.x/passport) and [Sanctum](/docs/11.x/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel은 API 토큰을 관리하고 토큰 기반 인증을 처리하는 데 도움이 되는 두 가지 선택적 패키지([Passport](/docs/11.x/passport), [Sanctum](/docs/11.x/sanctum))를 제공합니다. 이 라이브러리들과 Laravel의 내장 쿠키 기반 인증 서비스는 서로 배타적이지 않습니다. 즉, 주로 API 토큰 인증이 필요하다면 별도의 패키지를 활용하고, 웹 브라우저 인증에는 내장 기능을 사용할 수 있습니다. 실제로 많은 애플리케이션에서는 쿠키 기반 인증 서비스와 한 가지 API 인증 패키지를 함께 사용하게 됩니다.

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport는 OAuth2 인증 제공자로, 다양한 OAuth2 "grant type"을 지원하여 여러 유형의 토큰을 발급할 수 있습니다. 이는 robust하면서도 복잡한 API 인증 패키지입니다. 하지만 일반적으로 OAuth2 명세의 복잡한 기능까지 필요한 애플리케이션은 많지 않으며, 오히려 개발자나 사용자 모두 혼란을 겪을 수 있습니다. SPA나 모바일 애플리케이션이 Passport와 같은 OAuth2 인증 제공자를 어떻게 사용해야 할지 난해했던 이슈도 있었습니다.

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/11.x/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2의 복잡함과 개발자 혼란을 해소하기 위해, 웹 브라우저로 직접 오는 요청과 API 토큰 요청 모두를 지원하는 더 간단하고 직관적인 인증 패키지 개발을 목표로 했고, 그 결과물이 [Laravel Sanctum](/docs/11.x/sanctum)입니다. Sanctum은 웹 UI와 API를 함께 제공하는 애플리케이션, 백엔드와 따로 동작하는 SPA, 모바일 앱 등 대다수 상황에 가장 적합한 인증 패키지로 권장합니다.

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/11.x/sanctum#how-it-works) documentation. -->
Sanctum은 웹/ API 하이브리드 인증 패키지로, 애플리케이션의 전체 인증 과정을 관리할 수 있습니다. 요청을 받을 때 Sanctum은 먼저 세션 쿠키로 인증된 상태인지 확인하고(내장 인증 서비스 활용), 세션이 아니라면 API 토큰이 있는지 검사하여 토큰 인증을 시도합니다. ["how it works"](/docs/11.x/sanctum#how-it-works) 문서에서 자세히 확인할 수 있습니다.

<!-- Laravel Sanctum is the API package we have chosen to include with the [Laravel Jetstream](https://jetstream.laravel.com) application starter kit because we believe it is the best fit for the majority of web application's authentication needs. -->
Sanctum이 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트에 기본 포함된 이유도, 대다수 웹 애플리케이션의 인증 요구사항에 가장 잘 부합한다고 판단했기 때문입니다.

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary and Choosing Your Stack -->
#### Summary and Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
요약하자면, 브라우저로 접근하는 모놀리식 Laravel 애플리케이션을 만든다면 기본 내장 인증 서비스를 쓰게 됩니다.

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/11.x/passport) or [Sanctum](/docs/11.x/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
추가로 외부에서 API를 제공해야 한다면, [Passport](/docs/11.x/passport)와 [Sanctum](/docs/11.x/sanctum) 중 하나를 선택해 API 토큰 인증을 구현할 수 있습니다. 대부분의 경우, Sanctum이 더 단순하고 완성도 높은 API, SPA, 모바일 인증 솔루션이므로 우선적으로 사용하는 것이 좋습니다. Sanctum 역시 "scope" 또는 "ability" 지원이 포함되어 있습니다.

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/11.x/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/11.x/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
만약 Laravel 백엔드와 함께 동작하는 SPA(single-page application)를 만든다면, [Laravel Sanctum](/docs/11.x/sanctum)을 사용하는 것이 권장됩니다. 이때는 [manually implement your own backend authentication routes](#authenticating-users)하거나, [Laravel Fortify](/docs/11.x/fortify)를 헤드리스 인증 서비스로 사용해 회원가입, 비밀번호 재설정, 이메일 인증 등을 처리할 수도 있습니다.

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
OAuth2 명세의 모든 기능이 반드시 필요한 경우에만 Passport를 사용하는 것이 적합합니다.

<!-- And, if you would like to get started quickly, we are pleased to recommend [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services and Laravel Sanctum. -->
그리고 빠르게 시작하려면, [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)를 설치하면 내장 인증 서비스와 Sanctum을 기본으로 사용하는 새 Laravel 프로젝트를 손쉽게 시작할 수 있습니다.

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!WARNING]
> 이 문서는 [Laravel application starter kits](/docs/11.x/starter-kits)를 통한 사용자 인증 방법을 다룹니다. 스타터 키트는 빠른 시작을 위해 UI까지 포함된 구조를 제공합니다. 내장 인증 시스템과 직접 연동하고 싶다면 [manually authenticating users](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
<!-- ### Install a Starter Kit -->
### Install a Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/11.x/starter-kits). Our current starter kits, Laravel Breeze and Laravel Jetstream, offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
먼저, [install a Laravel application starter kit](/docs/11.x/starter-kits)를 설치해야 합니다. 현재 제공되는 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 새 프로젝트에 인증 기능을 멋지게 통합할 수 있는 다양한 시작점을 제공합니다.

<!-- Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Additionally, Breeze provides scaffolding options based on [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com), with the choice of using Vue or React for the Inertia-based scaffolding. -->
Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 인증 기능을 아주 간단하고 최소한의 코드로 구현해 줍니다. Breeze의 뷰 레이어는 [Blade templates](/docs/11.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 추가로, [Livewire](https://livewire.laravel.com) 또는 [Inertia](https://inertiajs.com)(Vue 또는 React 기반)로 스캐폴딩을 생성하는 옵션도 지원합니다.

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a more robust application starter kit that includes support for scaffolding your application with [Livewire](https://livewire.laravel.com) or [Inertia and Vue](https://inertiajs.com). In addition, Jetstream features optional support for two-factor authentication, teams, profile management, browser session management, API support via [Laravel Sanctum](/docs/11.x/sanctum), account deletion, and more. -->
[Laravel Jetstream](https://jetstream.laravel.com)은 더 강력한 스타터 키트로, [Livewire](https://livewire.laravel.com)나 [Inertia and Vue](https://inertiajs.com) 기반 스캐폴딩을 지원합니다. 또한 Jetstream은 2단계 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/11.x/sanctum)을 통한 API 지원, 계정 삭제 등 다양한 고급 기능까지 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving the Authenticated User -->
### Retrieving the Authenticated User

<!-- After installing an authentication starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
인증용 스타터 키트 설치 후, 사용자가 애플리케이션에 가입하고 인증을 완료했다면 종종 현재 인증된 사용자와 상호작용해야 할 때가 있습니다. 요청을 처리하는 도중 `Auth` 파사드의 `user` 메서드로 인증 사용자 정보를 쉽게 가져올 수 있습니다.

```
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
또 다른 방법으로, 인증된 사용자는 `Illuminate\Http\Request` 인스턴스를 통해서도 접근할 수 있습니다. 타입힌트가 지정된 클래스는 컨트롤러 메서드에 자동으로 주입된다는 점을 기억하세요. `Illuminate\Http\Request` 객체에 타입힌트를 지정하면, 해당 메서드에서 언제든 요청의 `user` 메서드로 애플리케이션의 어떤 컨트롤러 메서드에서든 인증된 사용자에 편리하게 접근할 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
<!-- #### Determining if the Current User is Authenticated -->
#### Determining if the Current User is Authenticated

<!-- To determine if the user making the incoming HTTP request is authenticated, you may use the `check` method on the `Auth` facade. This method will return `true` if the user is authenticated: -->
들어온 HTTP 요청의 사용자가 인증 상태인지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용하세요. 이 메서드는 사용자가 인증되어 있으면 `true`를 반환합니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드로 사용자의 인증 여부를 확인할 수 있지만, 실제로는 미들웨어를 활용해 특정 라우트나 컨트롤러에 접근하기 전에 인증 여부를 검증하는 것이 일반적입니다. 자세한 내용은 [protecting routes](/docs/11.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/11.x/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which is a [middleware alias](/docs/11.x/middleware#middleware-aliases) for the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already aliased internally by Laravel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/11.x/middleware)를 사용하면 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel은 기본적으로 `auth` 미들웨어를 제공하며, 이는 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [middleware alias](/docs/11.x/middleware#middleware-aliases)입니다. 이미 Laravel 내부적으로 별칭이 세팅되어 있기 때문에, 라우트 정의에 미들웨어를 붙이기만 하면 됩니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/11.x/routing#named-routes). You may modify this behavior using the method `redirectGuestsTo` of your application's `bootstrap/app.php` file: -->
`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 사용자를 `login` [named route](/docs/11.x/routing#named-routes)로 자동 리다이렉트합니다. 만약 이 동작을 수정하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectGuestsTo` 메서드를 사용하여 리다이렉트 경로를 변경할 수 있습니다.

```
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="specifying-a-guard"></a>
<!-- #### Specifying a Guard -->
#### Specifying a Guard

<!-- When attaching the `auth` middleware to a route, you may also specify which "guard" should be used to authenticate the user. The guard specified should correspond to one of the keys in the `guards` array of your `auth.php` configuration file: -->
라우트에 `auth` 미들웨어를 붙일 때, 어느 "가드"로 인증할지도 명시할 수 있습니다. 지정하는 가드명은 `auth.php` 설정 파일의 `guards` 배열에 있는 키와 일치해야 합니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using the Laravel Breeze or Laravel Jetstream [starter kits](/docs/11.x/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
Laravel Breeze나 Laravel Jetstream [starter kits](/docs/11.x/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 rate limit(속도 제한)이 적용됩니다. 기본적으로 여러 번 잘못된 인증 정보를 입력하면 1분 동안 로그인 시도가 차단되며, 이 제한은 사용자명/이메일 주소와 IP 주소별로 개별 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에도 rate limiting을 적용하고 싶다면, [rate limiting documentation](/docs/11.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/11.x/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
Laravel [application starter kits](/docs/11.x/starter-kits)가 제공하는 인증 스캐폴딩을 반드시 사용해야 하는 것은 아닙니다. 만약 직접 인증 로직을 구현하고 싶다면, Laravel 인증 클래스를 직접 활용해 사용자 인증을 처리할 수 있습니다. 걱정 마세요, 생각보다 어렵지 않습니다!

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/11.x/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/11.x/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
`Auth` [facade](/docs/11.x/facades)를 통해 인증 서비스를 사용할 것이므로, 클래스 상단에 `Auth` 파사드를 import해야 합니다. 이제 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 일반적으로 애플리케이션 "로그인" 폼의 인증 시도를 처리하는 데 사용됩니다. 인증에 성공했다면 [session](/docs/11.x/session)을 재생성하여 [session fixation](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

<!-- The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the `password` value passed to the method via the array. You should not hash the incoming request's `password` value, since the framework will automatically hash the value before comparing it to the hashed password in the database. An authenticated session will be started for the user if the two hashed passwords match. -->
`attempt` 메서드는 첫 번째 인수로 key/value 쌍의 배열을 받습니다. 이 배열의 값으로 데이터베이스에서 사용자를 검색합니다. 위 예시에서는 `email` 컬럼 값으로 사용자를 조회합니다. 사용자가 존재하면 데이터베이스의 해시된 비밀번호와 배열로 전달된 `password` 값을 비교합니다. 이때 들어온 요청의 `password` 값을 별도로 해시할 필요는 없습니다 — 프레임워크가 자동으로 해시해서 비교해 줍니다. 두 비밀번호가 일치하면 인증 세션이 시작됩니다.

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
Laravel의 인증 서비스는 "가드"의 "프로바이더" 설정에 따라 데이터베이스에서 사용자를 가져옵니다. 기본 설정(`config/auth.php`)에서는 Eloquent user provider를 사용하며, `App\Models\User` 모델을 지정하도록 되어 있습니다. 필요하다면 이 값을 변경할 수 있습니다.

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
`attempt` 메서드는 인증에 성공하면 `true`, 실패하면 `false`를 반환합니다.

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
`intended` 메서드는 사용자가 인증 미들웨어에 의해 가로채이기 전 시도했던 URL로 리다이렉트해 줍니다. 만약 그 URL이 없다면, 대체(fallback) URI를 인수로 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
필요하다면, 사용자의 이메일과 비밀번호 외에도 추가 쿼리 조건을 인증 시에 적용할 수 있습니다. 단순히 `attempt` 메서드에 전달하는 배열에 조건을 추가해 주면 됩니다. 예를 들어 사용자가 "active" 플래그가 있는지 검사하려면 다음처럼 작성할 수 있습니다.

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

<!-- For complex query conditions, you may provide a closure in your array of credentials. This closure will be invoked with the query instance, allowing you to customize the query based on your application's needs: -->
더 복잡한 쿼리가 필요하다면, 배열에 클로저를 추가할 수도 있습니다. 클로저는 쿼리 인스턴스를 받아 애플리케이션의 필요에 맞게 쿼리를 커스터마이징할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> 위 예시에서 `email` 필드는 필수 옵션이 아니며, 단순한 예시일 뿐입니다. 데이터베이스에서 "사용자명"에 해당하는 컬럼명을 사용해야 합니다.

<!-- The `attemptWhen` method, which receives a closure as its second argument, may be used to perform more extensive inspection of the potential user before actually authenticating the user. The closure receives the potential user and should return `true` or `false` to indicate if the user may be authenticated: -->
`attemptWhen` 메서드는 두 번째 인수로 클로저를 받아, 인증 전에 사용자를 추가적으로 검증할 수 있도록 해줍니다. 이 클로저는 해당 사용자 인스턴스를 받아, 인증 가능 여부를 `true` 또는 `false`로 반환해야 합니다.

```
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a name="accessing-specific-guard-instances"></a>
<!-- #### Accessing Specific Guard Instances -->
#### Accessing Specific Guard Instances

<!-- Via the `Auth` facade's `guard` method, you may specify which guard instance you would like to utilize when authenticating the user. This allows you to manage authentication for separate parts of your application using entirely separate authenticatable models or user tables. -->
`Auth` 파사드의 `guard` 메서드를 사용해 인증 시 특정 가드 인스턴스를 지정할 수도 있습니다. 이를 통해 애플리케이션의 서로 다른 영역마다 완전히 별도의 인증 모델 또는 사용자 테이블을 관리할 수 있습니다.

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard` 메서드에 전달하는 가드명은 `auth.php` 설정 파일의 guards 설정과 일치해야 합니다.

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
많은 웹 애플리케이션은 로그인 폼에 "로그인 상태 유지" 옵션을 제공합니다. 이 기능을 구현하려면 `attempt` 메서드의 두 번째 인수로 불리언 값을 전달하면 됩니다.

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
이 값이 `true`이면, Laravel은 사용자가 직접 로그아웃할 때까지 인증 상태를 무기한 유지합니다. "remember me" 토큰을 저장하는 데 사용되는 문자열 `remember_token` 컬럼이 `users` 테이블에 반드시 포함되어 있어야 합니다. 새 Laravel 프로젝트에서 제공되는 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<!-- If your application offers "remember me" functionality, you may use the `viaRemember`  method to determine if the currently authenticated user was authenticated using the "remember me" cookie: -->
"로그인 상태 유지" 기능이 제공되는 경우, 현재 인증된 사용자가 해당 쿠키로 인증되었는지 `viaRemember` 메서드로 확인할 수 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
<!-- ### Other Authentication Methods -->
### Other Authentication Methods

<a name="authenticate-a-user-instance"></a>
<!-- #### Authenticate a User Instance -->
#### Authenticate a User Instance

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/11.x/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
이미 인증이 필요한 사용자 인스턴스가 있다면, `Auth` 파사드의 `login` 메서드에 사용자 인스턴스를 전달하여 현재 인증된 사용자로 설정할 수 있습니다. 전달하는 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/11.x/contracts)을 구현해야 하며, Laravel의 `App\Models\User` 모델은 이를 기본적으로 구현합니다. 이 방식은 예를 들어 회원가입 직후와 같이 이미 유효한 사용자 인스턴스가 손에 있을 때 유용합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` 메서드의 두 번째 인수로 불리언 값을 전달하면, "로그인 상태 유지" 기능을 함께 적용할지 여부를 지정할 수 있습니다.

```
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
필요하다면, `login` 호출 전에 인증할 가드를 지정할 수도 있습니다.

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate a User by ID -->
#### Authenticate a User by ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
데이터베이스의 기본키(주로 ID)로 사용자를 인증하고 싶을 때는 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증할 사용자의 기본키를 인수로 받습니다.

```
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value to the `remember` argument of the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId`의 `remember` 인수로 불리언 값을 전달하면 "로그인 상태 유지"도 함께 지정할 수 있습니다.

```
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate a User Once -->
#### Authenticate a User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method: -->
`once` 메서드를 이용하면 세션이나 쿠키를 남기지 않고 애플리케이션에 단 한 번만 인증할 수 있습니다. 이 방식은 오직 해당 요청에만 잠깐 인증이 필요할 때 유용합니다.

```
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/11.x/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지를 만들 필요 없이 사용자를 빠르게 인증할 수 있는 방법입니다. 우선, 라우트에 `auth.basic` [middleware](/docs/11.x/middleware)를 추가하세요. `auth.basic` 미들웨어는 프레임워크에 내장되어 있어서 별도로 정의할 필요가 없습니다.

```
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
해당 미들웨어가 라우트에 붙어 있으면, 브라우저에서 접속할 때 자동으로 인증 창이 뜹니다. 기본적으로, `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자명으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note on FastCGI -->
#### A Note on FastCGI

<!-- If you are using PHP FastCGI and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
Laravel을 PHP FastCGI와 Apache 환경에서 운영하는 경우, HTTP Basic 인증이 정상 동작하지 않을 수 있습니다. 이 문제를 해결하려면 다음과 같이 애플리케이션의 `.htaccess` 파일에 라인을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/11.x/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
세션에 사용자 식별자 쿠키를 저장하지 않고 HTTP Basic 인증을 사용할 수도 있습니다. 이는 API 요청과 같은 상황에 유용합니다. 이를 위해 [define a middleware](/docs/11.x/middleware)하고, `onceBasic` 메서드를 호출하면 됩니다. 만약 `onceBasic`이 응답을 반환하지 않는다면, 요청은 계속 애플리케이션 내부로 전달됩니다.

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

<!-- Next, attach the middleware to a route: -->
이제 이 미들웨어를 원하는 라우트에 붙이면 됩니다.

```
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
사용자를 수동으로 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 호출하면 됩니다. 이 호출은 세션에서 인증 정보를 제거해, 이후 요청에서는 인증되지 않게 만듭니다.

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/11.x/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
또한, `logout` 호출 후에는 세션을 무효화하고 [CSRF token](/docs/11.x/csrf)을 재생성하는 것이 권장됩니다. 로그아웃 후에는 보통 애플리케이션의 루트로 리다이렉트하게 됩니다.

```
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
<!-- ### Invalidating Sessions on Other Devices -->
### Invalidating Sessions on Other Devices

<!-- Laravel also provides a mechanism for invalidating and "logging out" a user's sessions that are active on other devices without invalidating the session on their current device. This feature is typically utilized when a user is changing or updating their password and you would like to invalidate sessions on other devices while keeping the current device authenticated. -->
Laravel은 현재 기기를 제외한 다른 기기에서의 세션만 무효화(강제 로그아웃)할 수 있는 기능도 제공합니다. 이 기능은 주로 사용자가 비밀번호를 변경할 때, 다른 기기에서는 로그인을 해제하고 현재 기기만 유지하고 싶을 때 활용됩니다.

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is included on the routes that should receive session authentication. Typically, you should place this middleware on a route group definition so that it can be applied to the majority of your application's routes. By default, the `AuthenticateSession` middleware may be attached to a route using the `auth.session` [middleware alias](/docs/11.x/middleware#middleware-aliases): -->
시작에 앞서, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 받아야 할 경로에 포함되어야 합니다. 일반적으로는 라우트 그룹에 이 미들웨어를 추가해 대다수 라우트에 적용합니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [middleware alias](/docs/11.x/middleware#middleware-aliases)으로 붙일 수 있습니다.

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
그 다음, `Auth` 파사드의 `logoutOtherDevices` 메서드를 호출하면 됩니다. 이 메서드는 사용자의 현재 비밀번호 확인이 필요하므로 입력 폼에서 비밀번호를 받아야 합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices`가 호출되면, 나머지 기기에서의 세션은 완전히 무효화되며, 기존에 인증되어 있던 모든 가드에서 로그아웃됩니다.

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
애플리케이션을 개발하다 보면, 특정 작업을 수행하거나 중요한 영역에 진입하기 전에 사용자의 비밀번호를 한 번 더 확인해야 할 때가 있습니다. Laravel은 이런 과정을 간단히 처리할 수 있는 내장 미들웨어를 제공합니다. 이 기능을 구현하려면 다음 두 개의 라우트를 정의해야 합니다: 사용자의 비밀번호 확인을 요청하는 뷰를 보여주는 라우트, 그리고 사용자가 비밀번호를 제출하면 올바른지 확인하고 최종 목적지로 리다이렉트하는 라우트입니다.

> [!NOTE]
> 아래 문서는 Laravel의 비밀번호 재확인 기능을 직접 사용하는 방법을 설명합니다. 더 빠르게 시작하고 싶다면 [Laravel application starter kits](/docs/11.x/starter-kits)에도 이 기능이 기본 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
사용자가 비밀번호를 재확인하면, 3시간 동안 다시 비밀번호를 물어보지 않습니다. 이 시간 간격을 변경하려면 `config/auth.php` 설정 파일의 `password_timeout` 값을 조절할 수 있습니다.

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
먼저, 사용자의 비밀번호를 확인받는 뷰를 보여주는 라우트를 정의합니다.

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
예상할 수 있듯, 이 라우트에서 반환되는 뷰에는 `password` 필드가 포함된 폼이 있어야 합니다. 뷰 내부에는 사용자가 보호된 영역에 진입하려면 비밀번호를 한번 더 입력해야 한다는 안내 문구도 포함하면 좋습니다.

<a name="confirming-the-password"></a>
<!-- #### Confirming the Password -->
#### Confirming the Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
다음으로, "비밀번호 재확인" 뷰에서 전송된 폼을 처리하는 라우트를 만듭니다. 이 라우트는 실제로 비밀번호가 맞는지 확인하고, 사용자를 의도한 목적지로 리다이렉트하는 역할을 합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `password` field is determined to actually match the authenticated user's password. If the password is valid, we need to inform Laravel's session that the user has confirmed their password. The `passwordConfirmed` method will set a timestamp in the user's session that Laravel can use to determine when the user last confirmed their password. Finally, we can redirect the user to their intended destination. -->
진행하기 전, 이 라우트의 처리를 조금 더 살펴봅시다. 먼저, 요청의 `password` 필드가 실제로 인증된 사용자 비밀번호와 일치하는지 확인합니다. 비밀번호가 올바르면 Laravel 세션에 사용자가 재확인했다는 사실을 기록해야 합니다. `passwordConfirmed` 메서드는 재확인 시각을 세션에 저장하며, 이를 활용해 나중에 비밀번호 재확인 시점을 판별합니다. 마지막 단계에서는 사용자를 원래 의도했던 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>

<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/11.x/routing#named-routes): -->
최근 비밀번호 확인이 필요한 작업을 수행하는 모든 라우트에는 반드시 `password.confirm` 미들웨어를 지정해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자가 비밀번호를 확인한 후 원래 가려던 위치로 리디렉션될 수 있도록 해당 위치 정보를 세션에 자동으로 저장합니다. 사용자의 의도한 목적지가 세션에 저장된 후, 미들웨어는 사용자를 `password.confirm` [named route](/docs/11.x/routing#named-routes)로 리디렉션합니다.

```
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
<!-- ## Adding Custom Guards -->
## Adding Custom Guards

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/11.x/providers). Since Laravel already ships with an `AppServiceProvider`, we can place the code in that provider: -->
`Auth` 파사드의 `extend` 메서드를 사용하면 자신만의 인증 가드(guard)를 정의할 수 있습니다. `extend` 메서드는 [service provider](/docs/11.x/providers) 내에서 호출해야 합니다. Laravel에는 이미 `AppServiceProvider`가 포함되어 있으므로, 해당 프로바이더 안에 코드를 작성하면 됩니다.

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

<!-- As you can see in the example above, the callback passed to the `extend` method should return an implementation of `Illuminate\Contracts\Auth\Guard`. This interface contains a few methods you will need to implement to define a custom guard. Once your custom guard has been defined, you may reference the guard in the `guards` configuration of your `auth.php` configuration file: -->
위 예제에서 볼 수 있듯이, `extend` 메서드에 전달하는 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 인터페이스의 구현 인스턴스를 반환해야 합니다. 이 인터페이스에 정의된 여러 메서드를 구현하여 커스텀 가드를 만들 수 있습니다. 커스텀 가드를 정의한 후에는 `auth.php` 설정 파일의 `guards` 설정에서 해당 가드를 사용할 수 있습니다.

```
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
<!-- ### Closure Request Guards -->
### Closure Request Guards

<!-- The simplest way to implement a custom, HTTP request based authentication system is by using the `Auth::viaRequest` method. This method allows you to quickly define your authentication process using a single closure. -->
HTTP 요청을 기반으로 한 커스텀 인증 시스템을 가장 쉽게 구현하는 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 이용하면 단일 클로저로 인증 과정을 간편하게 정의할 수 있습니다.

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your application's `AppServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
먼저, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 `Auth::viaRequest`를 호출하세요. `viaRequest`의 첫 번째 인수는 인증 드라이버의 이름이며, 이는 여러분의 커스텀 가드를 설명하는 아무 문자열이나 사용할 수 있습니다. 두 번째 인수로는 HTTP 요청을 받아 사용자 인스턴스를 반환하거나, 인증에 실패할 경우 `null`을 반환하는 클로저를 전달합니다.

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

<!-- Once your custom authentication driver has been defined, you may configure it as a driver within the `guards` configuration of your `auth.php` configuration file: -->
커스텀 인증 드라이버를 정의했다면, 이제 `auth.php` 설정 파일의 `guards` 설정에서 해당 드라이버를 지정할 수 있습니다.

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<!-- Finally, you may reference the guard when assigning the authentication middleware to a route: -->
마지막으로, 라우트에 인증 미들웨어를 할당할 때 해당 가드를 참조하면 됩니다.

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
기존의 관계형 데이터베이스가 아닌 곳에 사용자 정보를 저장하는 경우, Laravel의 인증 시스템을 확장해서 커스텀 사용자 프로바이더(user provider)를 구현해야 합니다. 이때는 `Auth` 파사드의 `provider` 메서드를 사용해 커스텀 프로바이더를 정의합니다. 사용자 프로바이더 리졸버는 반드시 `Illuminate\Contracts\Auth\UserProvider` 인터페이스의 구현 인스턴스를 반환해야 합니다.

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

<!-- After you have registered the provider using the `provider` method, you may switch to the new user provider in your `auth.php` configuration file. First, define a `provider` that uses your new driver: -->
`provider` 메서드로 프로바이더를 등록했다면, 이제 `auth.php` 설정 파일에서 새로운 사용자 프로바이더를 사용할 수 있습니다. 먼저, 여러분이 만든 드라이버를 사용하는 `provider`를 정의하세요.

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

<!-- Finally, you may reference this provider in your `guards` configuration: -->
이제 `guards` 설정에서 이 프로바이더를 참조할 수 있습니다.

```
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
<!-- ### The User Provider Contract -->
### The User Provider Contract

<!-- `Illuminate\Contracts\Auth\UserProvider` implementations are responsible for fetching an `Illuminate\Contracts\Auth\Authenticatable` implementation out of a persistent storage system, such as MySQL, MongoDB, etc. These two interfaces allow the Laravel authentication mechanisms to continue functioning regardless of how the user data is stored or what type of class is used to represent the authenticated user: -->
`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등 다양한 영속 스토리지 시스템에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 역할을 합니다. 이 두 인터페이스를 통해 사용자 데이터 저장 방식이나 인증된 사용자를 나타내는 객체 타입에 상관없이 Laravel의 인증 시스템이 일관적으로 동작할 수 있습니다.

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
아래는 `Illuminate\Contracts\Auth\UserProvider`에 정의된 메서드들입니다.

```
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

<!-- The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method. -->
`retrieveById` 함수는 일반적으로 MySQL 데이터베이스의 자동 증가 ID처럼 사용자를 나타내는 키를 받습니다. 해당 ID와 일치하는 `Authenticatable` 구현체를 조회해 반환해야 합니다.

<!-- The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method. -->
`retrieveByToken` 함수는 사용자의 고유 `$identifier`와 "remember me" `$token`으로 사용자를 조회합니다. 이 토큰은 보통 `remember_token`과 같은 데이터베이스 컬럼에 저장됩니다. 앞선 메서드와 마찬가지로, 토큰 값이 일치하는 `Authenticatable` 구현체를 이 메서드에서 반환해야 합니다.

<!-- The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out. -->
`updateRememberToken` 메서드는 `$user` 인스턴스의 `remember_token`을 새 `$token`으로 갱신합니다. "remember me" 인증에 성공했을 때나 사용자가 로그아웃할 때 새 토큰이 사용자에게 할당됩니다.

<!-- The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.** -->
`retrieveByCredentials` 메서드는 애플리케이션 인증을 시도할 때 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받습니다. 그런 다음 이 메서드는 해당 자격 증명과 일치하는 사용자를 기본 영구 저장소에서 "조회"해야 합니다. 일반적으로 이 메서드는 `$credentials['username']` 값과 일치하는 "username"을 가진 사용자 레코드를 찾기 위해 "where" 조건이 포함된 쿼리를 실행합니다. 이 메서드는 `Authenticatable` 구현체를 반환해야 합니다. **이 메서드에서 비밀번호 검증이나 인증을 시도해서는 안 됩니다.**

<!-- The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid. -->
`validateCredentials` 메서드는 주어진 `$user`와 `$credentials`를 비교해 사용자를 인증해야 합니다. 예를 들어 이 메서드는 보통 `Hash::check` 메서드를 사용해 `$user->getAuthPassword()` 값과 `$credentials['password']` 값을 비교합니다. 이 메서드는 비밀번호가 유효한지 여부를 나타내는 `true` 또는 `false`를 반환해야 합니다.

<!-- The `rehashPasswordIfRequired` method should rehash the given `$user`'s password if required and supported. For example, this method will typically use the `Hash::needsRehash` method to determine if the `$credentials['password']` value needs to be rehashed. If the password needs to be rehashed, the method should use the `Hash::make` method to rehash the password and update the user's record in the underlying persistent storage. -->
`rehashPasswordIfRequired` 메서드는 필요하고 지원되는 경우 주어진 `$user`의 비밀번호를 다시 해시해야 합니다. 예를 들어 이 메서드는 보통 `Hash::needsRehash` 메서드를 사용해 `$credentials['password']` 값을 다시 해시해야 하는지 판단합니다. 비밀번호를 다시 해시해야 한다면, 이 메서드는 `Hash::make` 메서드로 비밀번호를 다시 해시하고 기본 영구 저장소의 사용자 레코드를 갱신해야 합니다.

<a name="the-authenticatable-contract"></a>
<!-- ### The Authenticatable Contract -->
### The Authenticatable Contract

<!-- Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods: -->
이제 `UserProvider` 인터페이스의 각 메서드를 살펴봤으니, 이번에는 `Authenticatable` 컨트랙트를 살펴보겠습니다. 사용자 프로바이더는 반드시 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스의 구현체를 반환해야 합니다.

```
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

<!-- This interface is simple. The `getAuthIdentifierName` method should return the name of the "primary key" column for the user and the `getAuthIdentifier` method should return the "primary key" of the user. When using a MySQL back-end, this would likely be the auto-incrementing primary key assigned to the user record. The `getAuthPasswordName` method should return the name of the user's password column. The `getAuthPassword` method should return the user's hashed password. -->
이 인터페이스는 매우 간단합니다.
- `getAuthIdentifierName`은 사용자의 "기본 키" 컬럼명을 반환하고,
- `getAuthIdentifier`는 사용자의 "기본 키" 값을 반환합니다.
MySQL을 사용하는 경우에는 보통 해당 레코드의 자동 증가 기본 키가 여기에 해당합니다.
- `getAuthPasswordName`은 비밀번호 컬럼의 이름을,
- `getAuthPassword`는 해싱되어 저장된 실제 비밀번호를 반환합니다.

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes an `App\Models\User` class in the `app/Models` directory which implements this interface. -->
이 인터페이스 덕분에 어떤 ORM이나 저장소 추상화 레이어를 사용하더라도 인증 시스템이 다양한 "user" 클래스를 호환하여 사용할 수 있습니다. Laravel은 기본적으로 `app/Models` 디렉터리에 이 인터페이스를 구현한 `App\Models\User` 클래스를 제공합니다.

<a name="automatic-password-rehashing"></a>
<!-- ## Automatic Password Rehashing -->
## Automatic Password Rehashing

<!-- Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via your application's `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable. -->
Laravel에서는 기본적으로 bcrypt 해싱 알고리즘으로 비밀번호를 암호화합니다. bcrypt의 "연산 강도(work factor)"는 애플리케이션의 `config/hashing.php` 설정 파일 혹은 `BCRYPT_ROUNDS` 환경 변수로 조정할 수 있습니다.

<!-- Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will gracefully and automatically rehash user passwords as users authenticate with your application via Laravel's starter kits or when you [manually authenticate users](#authenticating-users) via the `attempt` method. -->
일반적으로 CPU/GPU 성능이 향상됨에 따라 bcrypt 연산 강도도 점진적으로 높이는 것이 바람직합니다. 어플리케이션의 bcrypt 연산 강도를 높이면, Laravel은 [스타터 킷을 통한 로그인]이나 [manually authenticate users](#authenticating-users)에서 `attempt` 메서드를 통해 사용자가 인증할 때 비밀번호를 자동으로 안전하게 재암호화합니다.

<!-- Typically, automatic password rehashing should not disrupt your application; however, you may disable this behavior by publishing the `hashing` configuration file: -->
자동 비밀번호 리해시 기능이 애플리케이션에 불편을 주는 경우는 드물지만, 원하지 않는다면 `hashing` 설정 파일을 퍼블리시하여 비활성화할 수 있습니다.

```shell
php artisan config:publish hashing
```

<!-- Once the configuration file has been published, you may set the `rehash_on_login` configuration value to `false`: -->
설정 파일을 퍼블리시한 후, 다음과 같이 `rehash_on_login` 설정 값을 `false`로 지정하세요.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/11.x/events) during the authentication process. You may [define listeners](/docs/11.x/events) for any of the following events: -->
Laravel은 인증 과정 중 다양한 [events](/docs/11.x/events)를 디스패치(dispatch)합니다. 아래에 열거된 이벤트들에 대해 [define listeners](/docs/11.x/events)할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트명 |
| --- |
| `Illuminate\Auth\Events\Registered` |
| `Illuminate\Auth\Events\Attempting` |
| `Illuminate\Auth\Events\Authenticated` |
| `Illuminate\Auth\Events\Login` |
| `Illuminate\Auth\Events\Failed` |
| `Illuminate\Auth\Events\Validated` |
| `Illuminate\Auth\Events\Verified` |
| `Illuminate\Auth\Events\Logout` |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout` |
| `Illuminate\Auth\Events\Lockout` |
| `Illuminate\Auth\Events\PasswordReset` |

<!-- </div> -->
</div>