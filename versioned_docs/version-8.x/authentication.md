<!-- # Authentication -->
# Authentication

- [Introduction](#introduction)
    - [Starter Kits](#starter-kits)
    - [Database Considerations](#introduction-database-considerations)
    - [Ecosystem Overview](#ecosystem-overview)
- [Authentication Quickstart](#authentication-quickstart)
    - [Install A Starter Kit](#install-a-starter-kit)
    - [Retrieving The Authenticated User](#retrieving-the-authenticated-user)
    - [Protecting Routes](#protecting-routes)
    - [Login Throttling](#login-throttling)
- [Manually Authenticating Users](#authenticating-users)
    - [Remembering Users](#remembering-users)
    - [Other Authentication Methods](#other-authentication-methods)
- [HTTP Basic Authentication](#http-basic-authentication)
    - [Stateless HTTP Basic Authentication](#stateless-http-basic-authentication)
- [Logging Out](#logging-out)
    - [Invalidating Sessions On Other Devices](#invalidating-sessions-on-other-devices)
- [Password Confirmation](#password-confirmation)
    - [Configuration](#password-confirmation-configuration)
    - [Routing](#password-confirmation-routing)
    - [Protecting Routes](#password-confirmation-protecting-routes)
- [Adding Custom Guards](#adding-custom-guards)
    - [Closure Request Guards](#closure-request-guards)
- [Adding Custom User Providers](#adding-custom-user-providers)
    - [The User Provider Contract](#the-user-provider-contract)
    - [The Authenticatable Contract](#the-authenticatable-contract)
<!-- - [Social Authentication](/docs/8.x/socialite) -->
- [Social Authentication](/docs/8.x/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
많은 웹 애플리케이션에서는 사용자가 애플리케이션에 로그인할 수 있는 인증 기능을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 것은 복잡하고 때로는 보안상 위험이 따를 수도 있습니다. 그래서 Laravel은 인증을 빠르고, 안전하게, 그리고 쉽게 구현할 수 있는 다양한 도구를 제공합니다.

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel 인증 시스템의 핵심은 "가드(guard)"와 "프로바이더(provider)"로 이루어져 있습니다. 가드는 각각의 요청에서 사용자를 어떻게 인증할지 결정합니다. 예를 들어, Laravel에는 `session` 가드가 내장되어 있어 세션 저장소와 쿠키를 통해 인증 상태를 유지합니다.

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/8.x/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
프로바이더는 사용자를 영구 저장소에서 어떻게 가져올지 정의합니다. Laravel은 [Eloquent](/docs/8.x/eloquent)와 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 기본적으로 지원합니다. 필요하다면 애플리케이션에 맞는 추가 프로바이더도 자유롭게 정의할 수 있습니다.

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel의 인증 서비스 동작을 다양하게 조정할 수 있는 여러 옵션이 상세히 주석과 함께 포함되어 있습니다.

> [!TIP]
> 가드와 프로바이더는 "권한(roles)"과 "권한(permission)" 시스템과는 별개입니다. 권한 기반으로 사용자의 행동을 인가하는 방법은 [authorization](/docs/8.x/authorization) 문서를 참고해 주세요.

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/8.x/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에 [Laravel application starter kit](/docs/8.x/starter-kits)를 설치해 보세요. 데이터베이스 마이그레이션 후 `/register` 또는 애플리케이션에서 할당한 다른 URL로 접속하면, 스타터 키트가 전체 인증 시스템의 기본 구조를 자동으로 만들어줍니다.

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing the [Laravel Breeze](/docs/8.x/starter-kits#laravel-breeze) starter kit can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since Laravel Breeze creates authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**최종적으로 Laravel 애플리케이션에서 스타터 키트를 사용하지 않기로 정했다 하더라도, [Laravel Breeze](/docs/8.x/starter-kits#laravel-breeze) 스타터 키트를 설치해서 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구현되는지 학습해보는 것은 아주 좋은 기회가 될 수 있습니다.** Laravel Breeze는 인증 컨트롤러, 라우트, 뷰 파일들을 자동으로 생성해주기 때문에, 해당 파일의 코드를 직접 살펴보면서 Laravel 인증 기능의 내부 동작 방식을 쉽게 이해할 수 있습니다.

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/8.x/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. -->
Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent model](/docs/8.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버에서 사용할 수 있습니다. 애플리케이션이 Eloquent를 사용하지 않는 경우에는 Laravel 쿼리 빌더를 이용하는 `database` 인증 프로바이더를 사용할 수 있습니다.

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` 모델을 위한 데이터베이스 스키마를 작성할 때, 패스워드 컬럼의 길이가 최소 60자 이상이 되도록 해야 합니다. 물론, 새로 생성된 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션에서는 이미 이 길이보다 더 긴 컬럼이 생성됩니다.

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
또한, `users`(또는 이에 상응하는) 테이블에 `remember_token`이라는 100자 길이의 널(null) 허용 문자열 컬럼이 포함되어 있는지도 확인해야 합니다. 이 컬럼은 로그인 시 "로그인 상태 유지(remember me)" 옵션을 선택한 사용자의 토큰 저장에 사용됩니다. 역시 기본 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel은 인증과 관련하여 여러 패키지를 제공합니다. 본격적으로 살펴보기 전에, Laravel이 제공하는 인증 에코시스템 전반을 개괄적으로 정리하고 각 패키지의 용도를 설명합니다.

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/8.x/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
먼저, 인증의 일반적인 동작 방식을 살펴봅니다. 웹 브라우저를 사용할 때 사용자는 로그인 폼에 사용자명과 패스워드를 입력합니다. 이 정보가 올바르면, 애플리케이션은 인증된 사용자에 대한 정보를 사용자의 [session](/docs/8.x/session)에 저장합니다. 브라우저에는 세션 ID가 담긴 쿠키가 발급되어 이후의 모든 요청에서 이 세션 쿠키를 사용해 사용자를 식별합니다. 세션 쿠키가 올바르게 전달되면, 애플리케이션은 해당 세션 ID로 세션 데이터를 조회하여 인증 정보를 확인하고 해당 사용자를 "인증된 상태"라고 판단합니다.

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
반대로, API에 접근해야 하는 외부 서비스의 인증에는 일반적으로 쿠키를 사용하지 않습니다(브라우저가 없기 때문입니다). 대신, 외부 서비스는 각 요청마다 API 토큰을 함께 전송합니다. 애플리케이션은 전달받은 토큰이 데이터베이스 등에서 유효한지 검증하고, 해당 토큰에 연결된 사용자가 수행하는 요청으로 간주해 인증 처리를 합니다.

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel은 인증과 세션 서비스를 내장하고 있으며, 일반적으로 `Auth`와 `Session` 파사드를 통해 접근할 수 있습니다. 이 기능들은 웹 브라우저에서 이루어지는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명 검증 및 인증에 사용할 수 있는 다양한 메서드를 제공하며, 인증 데이터 처리와 세션 쿠키 발급도 자동으로 처리해줍니다. 이 서비스의 사용 방법은 본 문서에서 자세히 설명합니다.

<!-- **Application Starter Kits** -->
**애플리케이션 스타터 키트**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free packages](/docs/8.x/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. These packages are [Laravel Breeze](/docs/8.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/8.x/starter-kits#laravel-jetstream), and [Laravel Fortify](/docs/8.x/fortify). -->
여기서 설명한 대로, 애플리케이션의 인증 레이어를 직접 구축하기 위해 이 인증 서비스를 수동으로 사용할 수도 있습니다. 그러나 더 빠르게 시작할 수 있도록, 전체 인증 레이어를 견고하고 현대적으로 개발할 수 있는 [free packages](/docs/8.x/starter-kits)들이 준비되어 있습니다. 대표적으로 [Laravel Breeze](/docs/8.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/8.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/8.x/fortify)가 있습니다.

<!-- _Laravel Breeze_ is a simple, minimal implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is comprised of simple [Blade templates](/docs/8.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). To get started, check out the documentation on Laravel's [application starter kits](/docs/8.x/starter-kits). -->
_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 인증 기능을 아주 단순하고 미니멀하게 구현한 예제입니다. 템플릿은 [Blade templates](/docs/8.x/blade)와 [Tailwind CSS](https://tailwindcss.com)로 이루어져 있습니다. 처음 시작할 때 [application starter kits](/docs/8.x/starter-kits)를 참고해 주세요.

<!-- _Laravel Fortify_ is a headless authentication backend for Laravel that implements many of the features found in this documentation, including cookie-based authentication as well as other features such as two-factor authentication and email verification. Fortify provides the authentication backend for Laravel Jetstream or may be used independently in combination with [Laravel Sanctum](/docs/8.x/sanctum) to provide authentication for an SPA that needs to authenticate with Laravel. -->
_Laravel Fortify_는 Laravel의 다양한 인증 기능(쿠키 기반 인증, 2단계 인증, 이메일 인증 등)을 포함한 헤드리스 인증 백엔드입니다. Jetstream의 인증 백엔드로 작동하며, [Laravel Sanctum](/docs/8.x/sanctum)과 결합해 SPA 인증에도 사용할 수 있습니다.

<!-- _[Laravel Jetstream](https://jetstream.laravel.com)_ is a robust application starter kit that consumes and exposes Laravel Fortify's authentication services with a beautiful, modern UI powered by [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), and / or [Inertia.js](https://inertiajs.com). Laravel Jetstream includes optional support for two-factor authentication, team support, browser session management, profile management, and built-in integration with [Laravel Sanctum](/docs/8.x/sanctum) to offer API token authentication. Laravel's API authentication offerings are discussed below. -->
_[Laravel Jetstream](https://jetstream.laravel.com)_은 Fortify의 인증 서비스를 바탕으로, [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), [Inertia.js](https://inertiajs.com) 기반의 아름답고 현대적인 UI를 제공하는 강력한 애플리케이션 스타터 키트입니다. Jetstream은 2단계 인증, 팀 지원, 브라우저 세션 및 프로필 관리, [Laravel Sanctum](/docs/8.x/sanctum)과의 통합 등 다양한 기능을 선택적으로 제공합니다.

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/8.x/passport) and [Sanctum](/docs/8.x/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel은 API 토큰 관리 및 인증을 관리할 수 있도록 [Passport](/docs/8.x/passport)와 [Sanctum](/docs/8.x/sanctum) 두 가지 패키지를 제공합니다. 참고로 이 라이브러리들과 Laravel의 내장 쿠키 기반 인증 라이브러리는 상호 배타적이지 않습니다. API 토큰 인증에는 이 패키지들을, 브라우저 기반 인증에는 내장 인증 서비스를 사용할 수 있습니다. 대부분의 애플리케이션에서는 쿠키 기반 인증과 API 인증 패키지 중 하나를 함께 사용합니다.

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport는 다양한 OAuth2 "그랜트 타입"을 지원하는 OAuth2 인증 프로바이더입니다. 매우 다양하고 복잡한 API 인증 요구 사항에 적합한 강력한 패키지입니다. 다만, 대부분의 애플리케이션은 OAuth2 명세서의 모든 복잡한 기능이 필요하지 않을 수 있으며, 실제로 SPA나 모바일 앱 인증처럼 일부 시나리오에서는 Passport와 같은 OAuth2 방식의 사용이 혼란을 줄 수 있습니다.

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/8.x/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2의 복잡함과 개발자들의 혼동을 해소하기 위해, 더 간단하면서 실질적으로 웹(브라우저) 요청과 API 요청 모두를 처리할 수 있는 인증 패키지가 필요했습니다. 그래서 [Laravel Sanctum](/docs/8.x/sanctum)이 탄생했습니다. Sanctum은 웹 UI뿐만 아니라 별도의 백엔드(SPA, 모바일 클라이언트 등)에서 API를 호출할 때도 사용할 수 있으며, 대부분의 인증 요구에 권장되고 있습니다.

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/8.x/sanctum#how-it-works) documentation. -->
Sanctum은 웹과 API 인증의 하이브리드 패키지입니다. Sanctum을 기반으로 하는 애플리케이션이 요청을 받으면, 우선 세션 쿠키에 인증된 세션이 연관되어 있는지 확인합니다. 이때 위에서 설명한 내장 인증 서비스가 호출됩니다. 세션 쿠키로 인증되지 않은 요청의 경우, 요청에 API 토큰이 포함되어 있는지 검사하여 해당 토큰으로 인증을 진행합니다. 보다 자세한 동작 방식은 Sanctum의 ["how it works"](/docs/8.x/sanctum#how-it-works) 문서를 참고해 주세요.

<!-- Laravel Sanctum is the API package we have chosen to include with the [Laravel Jetstream](https://jetstream.laravel.com) application starter kit because we believe it is the best fit for the majority of web application's authentication needs. -->
Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트에 기본 포함되어 있으며, 대부분의 웹 애플리케이션 인증 요구에 가장 적합하다고 생각합니다.

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary & Choosing Your Stack -->
#### Summary & Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
요약하면, 애플리케이션이 브라우저로 접근하는 모놀리식 Laravel 프로젝트라면 Laravel의 내장 인증 서비스를 사용하게 됩니다.

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/8.x/passport) or [Sanctum](/docs/8.x/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
그 다음으로, 외부 API 소비자가 존재하는 API를 제공한다면 [Passport](/docs/8.x/passport) 또는 [Sanctum](/docs/8.x/sanctum) 중에서 선택해 토큰 기반 API 인증 기능을 추가할 수 있습니다. 일반적으로 복잡한 OAuth2 기능이 필요하지 않다면, 간단하고 강력한 솔루션인 Sanctum 사용을 권장합니다. Sanctum은 API, SPA, 모바일 인증, "scopes(역할 범위)" 및 "abilities(권한)"까지 지원합니다.

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/8.x/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/8.x/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
Laravel 백엔드를 기반으로 하는 SPA(single-page application)를 만들 경우에는 반드시 [Laravel Sanctum](/docs/8.x/sanctum)을 사용하는 것이 좋습니다. Sanctum을 쓸 때는 [manually implement your own backend authentication routes](#authenticating-users), [Laravel Fortify](/docs/8.x/fortify)를 헤드리스 인증 서비스로 사용해 회원가입, 비밀번호 재설정, 이메일 인증 등의 라우트와 컨트롤러를 구축할 수 있습니다.

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
만약 OAuth2 명세의 전체 기능이 반드시 필요한 경우에만 Passport를 선택하시길 바랍니다.

<!-- And, if you would like to get started quickly, we are pleased to recommend [Laravel Jetstream](https://jetstream.laravel.com) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services and Laravel Sanctum. -->
그리고, 빠르게 시작하려면 [Laravel Jetstream](https://jetstream.laravel.com)을 추천합니다. Jetstream은 Laravel 내장 인증 서비스와 Sanctum이 이미 적용되어 있어, 권장되는 인증 스택으로 새로운 Laravel 애플리케이션을 신속하게 시작할 수 있습니다.

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!NOTE]
> 이 문서는 UI 스캐폴딩을 포함한 [Laravel application starter kits](/docs/8.x/starter-kits)에 기반한 인증 사용자 생성 방법을 다룹니다. Laravel의 인증 시스템을 직접 다루고 싶다면, [manually authenticating users](#authenticating-users) 항목을 참고하세요.

<a name="install-a-starter-kit"></a>
<!-- ### Install A Starter Kit -->
### Install A Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/8.x/starter-kits). Our current starter kits, Laravel Breeze and Laravel Jetstream, offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
먼저, [install a Laravel application starter kit](/docs/8.x/starter-kits)를 설치합니다. 현재 제공되는 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 새 Laravel 애플리케이션에서 인증 기능을 아름답고 편리하게 시작할 수 있도록 돕습니다.

<!-- Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/8.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Breeze also offers an [Inertia](https://inertiajs.com) based scaffolding option using Vue or React. -->
Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 모든 인증 기능을 아주 간결하고 단순하게 제공합니다. 뷰 레이어는 [Blade templates](/docs/8.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. Breeze는 [Inertia](https://inertiajs.com)를 사용해 Vue나 React 기반의 스캐폴딩 옵션도 제공합니다.

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a more robust application starter kit that includes support for scaffolding your application with [Livewire](https://laravel-livewire.com) or [Inertia.js and Vue](https://inertiajs.com). In addition, Jetstream features optional support for two-factor authentication, teams, profile management, browser session management, API support via [Laravel Sanctum](/docs/8.x/sanctum), account deletion, and more. -->
[Laravel Jetstream](https://jetstream.laravel.com)은 더 강력한 스타터 키트로, [Livewire](https://laravel-livewire.com) 또는 [Inertia.js and Vue](https://inertiajs.com)를 기반으로 애플리케이션을 스캐폴딩하는 지원을 제공합니다. Jetstream은 2단계 인증, 팀, 프로필 관리, 브라우저 세션, [Laravel Sanctum](/docs/8.x/sanctum)을 통한 API 지원, 계정 삭제 등 다양한 부가 기능도 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving The Authenticated User -->
### Retrieving The Authenticated User

<!-- After installing an authentication starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
인증 스타터 키트를 설치하고 사용자가 회원가입 또는 인증에 성공한 후에는, 현재 인증된 사용자 정보와 자주 상호작용하게 됩니다. 들어오는 요청(Request)을 처리하는 중에, `Auth` 파사드의 `user` 메서드를 통해 현재 인증된 사용자를 쉽게 얻을 수 있습니다.

```
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
또는, 사용자가 인증된 이후에는 `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. 컨트롤러 메서드에서 타입힌트로 `Illuminate\Http\Request`를 사용하면 Laravel이 자동으로 객체를 주입하므로, 이 객체의 `user` 메서드로 언제든 인증 사용자를 참조할 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // $request->user()
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
<!-- #### Determining If The Current User Is Authenticated -->
#### Determining If The Current User Is Authenticated

<!-- To determine if the user making the incoming HTTP request is authenticated, you may use the `check` method on the `Auth` facade. This method will return `true` if the user is authenticated: -->
들어오는 HTTP 요청의 사용자가 인증된 상태인지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 로그인되어 있으면 `true`를 반환합니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!TIP]
> `check` 메서드로 사용자가 인증돼 있는지 확인할 수 있지만, 보통은 미들웨어를 사용해 인증된 사용자만 특정 라우트/컨트롤러에 접근하도록 제한하는 것이 일반적입니다. 자세한 내용은 [protecting routes](/docs/8.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/8.x/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which references the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/8.x/middleware)를 사용하면, 인증된 사용자만 특정 라우트에 접근할 수 있도록 할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어를 기본 제공하며, 이 미들웨어는 이미 애플리케이션의 HTTP 커널에 등록되어 있습니다. 사용 방법은 아래와 같이 라우트 정의에 미들웨어를 지정하면 됩니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/8.x/routing#named-routes). You may modify this behavior by updating the `redirectTo` function in your application's `app/Http/Middleware/Authenticate.php` file: -->
`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 해당 사용자를 `login` [named route](/docs/8.x/routing#named-routes)로 리다이렉트합니다. 이 동작은 `app/Http/Middleware/Authenticate.php` 파일의 `redirectTo` 함수를 수정하여 변경할 수 있습니다.

```
/**
 * Get the path the user should be redirected to.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return string
 */
protected function redirectTo($request)
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
<!-- #### Specifying A Guard -->
#### Specifying A Guard

<!-- When attaching the `auth` middleware to a route, you may also specify which "guard" should be used to authenticate the user. The guard specified should correspond to one of the keys in the `guards` array of your `auth.php` configuration file: -->
`auth` 미들웨어를 라우트에 적용할 때, 인증에 사용할 "가드"를 명시적으로 지정할 수도 있습니다. 지정한 가드는 `auth.php` 설정 파일의 `guards` 배열에 정의된 키 중 하나여야 합니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using the Laravel Breeze or Laravel Jetstream [starter kits](/docs/8.x/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
Laravel Breeze 또는 Laravel Jetstream [starter kits](/docs/8.x/starter-kits)를 사용하는 경우, 로그인 시도에 대해 자동으로 rate limit(속도 제한)이 적용됩니다. 기본적으로 몇 번의 실패 후에는 1분 동안 로그인할 수 없습니다. 이 제한은 사용자의 사용자명/이메일과 IP 주소를 조합해 개별적으로 동작합니다.

> [!TIP]
> 애플리케이션 내 다른 라우트에도 rate limit을 적용하고 싶다면 [rate limiting documentation](/docs/8.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/8.x/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
Laravel [application starter kits](/docs/8.x/starter-kits)가 제공하는 인증 스캐폴딩을 꼭 사용할 필요는 없습니다. 이 스캐폴딩을 사용하지 않기로 했다면, Laravel의 인증 클래스를 직접 활용해 사용자 인증을 관리해야 합니다. 걱정하지 마세요. 아주 간단하고 직관적으로 할 수 있습니다!

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/8.x/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/8.x/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
인증 서비스는 `Auth` [facade](/docs/8.x/facades)를 통해 사용할 수 있습니다. 먼저 클래스 상단에 `Auth` 파사드를 임포트해야 합니다. 다음으로, `attempt` 메서드를 살펴봅니다. `attempt` 메서드는 일반적으로 애플리케이션의 "로그인" 폼에서 인증 시도 시 사용합니다. 인증에 성공하면, [session](/docs/8.x/session) 공격을 방지하기 위해 사용자의 [session fixation](https://en.wikipedia.org/wiki/Session_fixation)을 반드시 재생성해야 합니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function authenticate(Request $request)
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
        ]);
    }
}
```

<!-- The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the `password` value passed to the method via the array. You should not hash the incoming request's `password` value, since the framework will automatically hash the value before comparing it to the hashed password in the database. An authenticated session will be started for the user if the two hashed passwords match. -->
`attempt` 메서드는 첫 번째 인자로 키-값 쌍의 배열을 받습니다. 이 배열의 값을 이용해 데이터베이스에서 사용자를 조회합니다. 위 예시의 경우에는 `email` 컬럼 값으로 사용자를 찾게 됩니다. 사용자를 찾으면 데이터베이스에 저장된 해시된 비밀번호와 배열로 전달된 `password` 값을 비교합니다. 들어온 요청의 `password` 값은 직접 해시할 필요가 없습니다. 프레임워크가 비교 전에 자동으로 해싱하기 때문입니다. 두 해시된 비밀번호가 일치하면 사용자의 인증 세션이 시작됩니다.

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
참고로, Laravel의 인증 서비스는 인증 가드의 "프로바이더" 설정에 따라 사용자를 데이터베이스에서 조회합니다. 기본 `config/auth.php` 파일에서는 Eloquent 사용자 프로바이더가 지정되어 있고, 사용자 모델로 `App\Models\User`을 사용하도록 되어 있습니다. 필요에 따라 이 값을 얼마든지 교체할 수 있습니다.

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
`attempt` 메서드는 인증 성공 시 `true`, 실패 시 `false`를 반환합니다.

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
또한 `intended` 메서드는 사용자가 인증 미들웨어에 의해 접근이 차단되기 전 시도했던 URL로 리다이렉트 시켜주며, 의도한 목적지가 없으면 대체 URL을 지정할 수도 있습니다.

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
필요하다면, 이메일과 비밀번호 외에 다른 쿼리 조건도 인증 쿼리에 추가할 수 있습니다. 이를 위해 인증 정보를 담은 배열에 필요한 조건을 더해 `attempt`에 전달하면 됩니다. 예를 들어 사용자가 "active" 상태인지 검사할 수도 있습니다.

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

> [!NOTE]
> 예시에서 사용된 `email`은 필수 컬럼이 아니라, 단순히 예시입니다. 실제로는 데이터베이스의 "username" 역할을 하는 컬럼 이름을 사용해야 합니다.

<a name="accessing-specific-guard-instances"></a>
<!-- #### Accessing Specific Guard Instances -->
#### Accessing Specific Guard Instances

<!-- Via the `Auth` facade's `guard` method, you may specify which guard instance you would like to utilize when authenticating the user. This allows you to manage authentication for separate parts of your application using entirely separate authenticatable models or user tables. -->
`Auth` 파사드의 `guard` 메서드를 이용하면, 인증에 사용할 가드 인스턴스를 명시적으로 지정할 수 있습니다. 이를 통해 서로 다른 인증 모델이나 사용자 테이블을 각기 다른 애플리케이션 영역에서 독립적으로 사용할 수 있습니다.

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard` 메서드에 전달하는 가드 이름은 반드시 `auth.php` 설정 파일에 정의되어야 합니다.

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
많은 웹 애플리케이션에서는 로그인 폼에 "로그인 상태 유지(remember me)" 체크박스를 제공합니다. 이 기능을 적용하려면, `attempt` 메서드의 두 번째 인자에 불린 값을 전달하면 됩니다.

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
이 값이 `true`이면 Laravel은 사용자를 수동 로그아웃할 때까지 계속 인증된 상태로 유지합니다. 이 기능을 사용하려면 `users` 테이블에 문자열 타입의 `remember_token` 컬럼이 존재해야 하며, Laravel의 기본 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<a name="other-authentication-methods"></a>
<!-- ### Other Authentication Methods -->
### Other Authentication Methods

<a name="authenticate-a-user-instance"></a>
<!-- #### Authenticate A User Instance -->
#### Authenticate A User Instance

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/8.x/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
이미 존재하는 사용자 인스턴스를 현재 인증 사용자로 직접 설정해야 할 경우, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달하면 됩니다. 이때의 사용자 인스턴스는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/8.x/contracts)을 구현해야 하며, Laravel의 기본 `App\Models\User` 모델은 이미 이를 구현하고 있습니다. 주로 사용자가 회원가입을 마치고 곧바로 로그인 상태로 만들어줘야 할 때 유용합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` 메서드의 두 번째 인자로 불린 값을 전달해 "로그인 상태 유지(remember me)" 기능을 사용할 수 있습니다. 이 값은 해당 인증 세션에 "remember me" 기능을 원하는지를 나타냅니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
먼저 사용할 가드를 지정한 뒤, `login`을 호출하는 것도 가능합니다.

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate A User By ID -->
#### Authenticate A User By ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
사용자 데이터베이스 레코드의 기본 키(primary key)를 이용해 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 첫 번째 인자로 인증하려는 사용자의 기본 키 값을 전달합니다.

```
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value as the second argument to the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId` 메서드의 두 번째 인자로 불린 값을 전달해 해당 인증 세션에 "remember me" 기능을 원하는지 지정할 수 있습니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate A User Once -->
#### Authenticate A User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method: -->
`once` 메서드를 이용하면, 한 번의 요청에 한해 사용자 인증을 할 수 있습니다. 이때는 세션이나 쿠키가 사용되지 않습니다.

```
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/8.x/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지를 만들지 않고 빠르게 사용자를 인증할 수 있는 방법입니다. 시작하려면, `auth.basic` [middleware](/docs/8.x/middleware)를 라우트에 적용하세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 기본 포함되어 있으므로 직접 정의할 필요가 없습니다.

```
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
이 미들웨어를 라우트에 적용하면, 브라우저에서 해당 경로 접속 시 인증 정보를 입력하라는 프롬프트가 자동으로 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자 이름으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note On FastCGI -->
#### A Note On FastCGI

<!-- If you are using PHP FastCGI and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
Laravel 애플리케이션을 PHP FastCGI와 Apache 조합으로 서비스하는 경우 HTTP Basic 인증이 올바로 동작하지 않을 수 있습니다. 이때에는 아래 코드를 `.htaccess` 파일에 추가해 주세요.

```
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/8.x/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
세션에 사용자 식별 쿠키를 남기지 않고 HTTP Basic 인증을 하고 싶을 때도 있습니다. 주로 API 요청 인증에 이 방법이 유용합니다. 이를 위해서는 [define a middleware](/docs/8.x/middleware)해, `onceBasic` 메서드를 호출하면 됩니다. `onceBasic`이 아무 응답도 반환하지 않으면, 요청은 애플리케이션의 다음 단계로 넘어갑니다.

```
<?php

namespace App\Http\Middleware;

use Illuminate\Support\Facades\Auth;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, $next)
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

<!-- Next, [register the route middleware](/docs/8.x/middleware#registering-middleware) and attach it to a route: -->
이제 [register the route middleware](/docs/8.x/middleware#registering-middleware)한 다음, 라우트에 적용하세요.

```
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
사용자를 수동으로 로그아웃시키려면, `Auth` 파사드의 `logout` 메서드를 사용하면 됩니다. 이 메서드는 사용자의 세션에서 인증 정보를 삭제하므로, 이후 요청부터는 인증이 해제됩니다.

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/8.x/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
`logout` 메서드를 호출하는 것과 더불어, 사용자의 세션을 무효화하고 [CSRF token](/docs/8.x/csrf)을 재생성하는 것이 좋습니다. 로그아웃 후 일반적으로 애플리케이션 루트로 리다이렉트합니다.

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 *
 * @param  \Illuminate\Http\Request  $request
 * @return \Illuminate\Http\Response
 */
public function logout(Request $request)
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
<!-- ### Invalidating Sessions On Other Devices -->
### Invalidating Sessions On Other Devices

<!-- Laravel also provides a mechanism for invalidating and "logging out" a user's sessions that are active on other devices without invalidating the session on their current device. This feature is typically utilized when a user is changing or updating their password and you would like to invalidate sessions on other devices while keeping the current device authenticated. -->
Laravel은 한 사용자가 비밀번호를 변경하거나 업데이트할 때, 현재 사용하는 기기는 그대로 인증된 상태로 두면서 다른 모든 기기에서의 세션을 무효화(로그아웃) 할 수 있는 기능을 제공합니다.

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is present and un-commented in your `App\Http\Kernel` class' `web` middleware group: -->
시작하기 전에, `App\Http\Kernel` 클래스의 `web` 미들웨어 그룹에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 활성화(주석 해제)되어 있는지 확인하세요.

```
'web' => [
    // ...
    \Illuminate\Session\Middleware\AuthenticateSession::class,
    // ...
],
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
이제 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 입력해야 하며, 애플리케이션에서 해당 값을 폼을 통해 받아야 합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices` 메서드가 호출되면, 해당 사용자의 다른 모든 세션이 완전히 무효화되며, 기존에 인증되어 있던 모든 가드에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
애플리케이션을 개발하다 보면, 사용자가 민감한 작업을 수행하거나 중요한 영역으로 이동하기 전에 비밀번호를 다시 한번 확인하도록 해야 할 때가 있습니다. Laravel은 이를 위한 미들웨어를 기본 제공하여, 이 과정을 아주 쉽게 구현할 수 있게 합니다. 비밀번호 확인 기능 구현을 위해서는 두 개의 라우트를 정의해야 합니다. 하나는 비밀번호를 입력받는 뷰를 보여주는 라우트, 다른 하나는 입력받은 비밀번호를 검증하고 사용자를 원래 목적지로 이동시키는 라우트입니다.

> [!TIP]
> 아래 문서는 Laravel 비밀번호 확인 기능을 직접 통합하는 방법을 안내합니다. 더 빠른 구현을 원하신다면, [Laravel application starter kits](/docs/8.x/starter-kits)도 이 기능을 지원합니다.

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
사용자가 비밀번호를 확인한 후에는 3시간(기본값) 동안 다시 비밀번호를 입력할 필요가 없습니다. 이 시간은 애플리케이션의 `config/auth.php` 설정 파일에서 `password_timeout` 값으로 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
먼저, 비밀번호 확인을 요청하는 뷰를 보여줄 라우트를 정의합니다.

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
이 라우트가 반환하는 뷰에는 반드시 `password` 필드를 가진 폼이 포함되어 있어야 하며, 민감한 영역에 접근하기 때문에 비밀번호 확인이 필요하다는 안내문을 자유롭게 추가할 수 있습니다.

<a name="confirming-the-password"></a>
<!-- #### Confirming The Password -->
#### Confirming The Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
그 다음, "비밀번호 확인" 뷰에서 폼 요청을 받아 처리할 라우트를 정의합니다. 이 라우트는 비밀번호 유효성 검사 및 목적지로의 리다이렉션을 담당합니다.

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
이 라우트의 내부 동작을 살펴보면, 먼저 폼 입력의 `password` 필드가 현재 인증된 사용자의 비밀번호와 일치하는지 검사합니다. 일치하면 사용자가 비밀번호를 확인했다는 정보를 세션에 저장하는데, 이때 `passwordConfirmed` 메서드를 사용합니다. 그 후 사용자를 원래 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/8.x/routing#named-routes): -->
비밀번호 확인이 필요한 라우트에는 반드시 `password.confirm` 미들웨어를 적용해야 합니다. 이 미들웨어는 Laravel에서 기본 설치시 포함되어 있으며, 사용자가 비밀번호를 확인한 직후 원하는 위치로 사용자를 되돌려 보내기 위해 목적지를 세션에 저장합니다. 그 후 사용자를 `password.confirm` [named route](/docs/8.x/routing#named-routes)로 리다이렉트합니다.

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

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/8.x/providers). Since Laravel already ships with an `AuthServiceProvider`, we can place the code in that provider: -->
`Auth` 파사드의 `extend` 메서드를 사용하면, 직접 인증 가드를 정의할 수도 있습니다. `extend` 호출은 보통 [service provider](/docs/8.x/providers) 내부에 위치합니다. Laravel에는 이미 `AuthServiceProvider`가 있으므로, 해당 파일에 코드를 추가하면 됩니다.

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * Register any application authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::extend('jwt', function ($app, $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

<!-- As you can see in the example above, the callback passed to the `extend` method should return an implementation of `Illuminate\Contracts\Auth\Guard`. This interface contains a few methods you will need to implement to define a custom guard. Once your custom guard has been defined, you may reference the guard in the `guards` configuration of your `auth.php` configuration file: -->
위 예시에서처럼, `extend`에 전달되는 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 하며, 이 인터페이스의 여러 메서드를 반드시 구현해야 합니다. 커스텀 가드 작성 후에는 `auth.php` 설정 파일 내 `guards` 섹션에서 사용할 수 있습니다.

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
HTTP 요청 기반의 간단한 커스텀 인증 시스템은 `Auth::viaRequest` 메서드로 곧바로 정의할 수 있습니다. 하나의 클로저만으로 인증 프로세스를 쉽고 빠르게 구현할 수 있습니다.

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your `AuthServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
시작하려면, `AuthServiceProvider`의 `boot` 메서드 내부에서 `Auth::viaRequest` 메서드를 호출하세요. `viaRequest` 메서드의 첫 번째 인자는 인증 드라이버 이름이며, 커스텀 가드를 설명하는 임의의 문자열이면 됩니다. 두 번째 인자는 들어오는 HTTP 요청을 받고, 인증에 성공하면 사용자 인스턴스를, 실패하면 `null`을 반환하는 클로저입니다.

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Register any application authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', $request->token)->first();
    });
}
```

<!-- Once your custom authentication driver has been defined, you may configure it as a driver within the `guards` configuration of your `auth.php` configuration file: -->
커스텀 인증 드라이버를 정의한 후에는 `auth.php` 설정 파일의 `guards` 설정에서 driver로 사용할 수 있습니다.

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
기존의 관계형 데이터베이스가 아닌 다른 저장소를 사용자 정보 저장에 사용할 경우, Laravel에 직접 사용자 프로바이더를 추가할 수 있습니다. 이를 위해 `Auth` 파사드의 `provider` 메서드로 사용자 프로바이더를 등록하면 됩니다. 이때 반환 타입은 반드시 `Illuminate\Contracts\Auth\UserProvider` 여야 합니다.

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * Register any application authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::provider('mongo', function ($app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

<!-- After you have registered the provider using the `provider` method, you may switch to the new user provider in your `auth.php` configuration file. First, define a `provider` that uses your new driver: -->
`provider` 메서드로 프로바이더를 등록한 뒤에는 `auth.php` 설정 파일에서 새 user provider를 사용하도록 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 `provider`를 정의합니다.

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

<!-- Finally, you may reference this provider in your `guards` configuration: -->
그리고 이제 `guards` 설정에서 이 프로바이더를 지정해 사용할 수 있습니다.

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
`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등 영구 저장소에서 꺼내오는 역할을 합니다. 이 두 인터페이스 덕분에 사용자 데이터 저장 방식이나 클래스타입과 관계없이 Laravel 인증 시스템이 일관성 있게 동작할 수 있습니다.

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
아래는 `Illuminate\Contracts\Auth\UserProvider` 계약 예시입니다.

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
}
```

<!-- The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method. -->
`retrieveById`는 보통 사용자 ID(예: MySQL의 auto-increment ID) 등 사용자를 특정할 수 있는 키 값을 받아 해당하는 `Authenticatable` 구현체를 반환해야 합니다.

<!-- The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method. -->
`retrieveByToken`은 고유 `$identifier`와 "remember me" `$token`(예: `remember_token` 컬럼 값)으로 사용자를 조회합니다. 앞선 메서드와 마찬가지로, 토큰 값이 일치하는 `Authenticatable` 구현체를 이 메서드에서 반환해야 합니다.

<!-- The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out. -->
`updateRememberToken`은 `$user` 인스턴스의 `remember_token` 값을 새 `$token`으로 갱신합니다. "remember me" 인증에 성공했을 때나 사용자가 로그아웃할 때 새 토큰이 사용자에게 할당됩니다.

<!-- The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.** -->
`retrieveByCredentials`는 애플리케이션 인증을 시도할 때 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받아, 해당 자격 증명과 일치하는 사용자를 기본 영구 저장소에서 "조회"해야 합니다. 일반적으로 이 메서드는 `$credentials['username']` 값과 일치하는 "username"을 가진 사용자 레코드를 찾기 위해 "where" 조건이 포함된 쿼리를 실행합니다. 이 메서드는 `Authenticatable` 구현체를 반환해야 합니다. **이 메서드에서 비밀번호 검증이나 인증을 시도해서는 안 됩니다.**

<!-- The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid. -->
`validateCredentials`는 주어진 `$user`와 `$credentials`를 비교해 비밀번호 등 자격 증명을 검증합니다. 예를 들어, 보통 `Hash::check`를 통해 `$user->getAuthPassword()`와 `$credentials['password']`를 비교하고, 결과에 따라 `true` 또는 `false`를 반환합니다.

<a name="the-authenticatable-contract"></a>
<!-- ### The Authenticatable Contract -->
### The Authenticatable Contract

<!-- Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods: -->
이제 `UserProvider`의 각 메서드를 살펴보았으니, `Authenticatable` 계약도 살펴봅시다. 사용자 프로바이더는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스를 구현한 인스턴스를 반환해야 한다는 점을 기억하세요.

```
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

<!-- This interface is simple. The `getAuthIdentifierName` method should return the name of the "primary key" field of the user and the `getAuthIdentifier` method should return the "primary key" of the user. When using a MySQL back-end, this would likely be the auto-incrementing primary key assigned to the user record. The `getAuthPassword` method should return the user's hashed password. -->
이 인터페이스는 매우 단순합니다. `getAuthIdentifierName`은 사용자 개체의 "기본 키" 필드 이름을, `getAuthIdentifier`는 "기본 키" 값을 반환해야 합니다(예: MySQL의 auto-increment 값). `getAuthPassword`는 사용자의 해시된 비밀번호를 반환해야 합니다.

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes a `App\Models\User` class in the `app/Models` directory which implements this interface. -->
이 덕분에 인증 시스템이 어떤 ORM, 저장소 구현체에서든 동작할 수 있습니다. Laravel은 `app/Models` 디렉터리에 `App\Models\User` 클래스를 제공하며, 이 클래스가 이미 이 인터페이스를 구현하고 있습니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/8.x/events) during the authentication process. You may attach listeners to these events in your `EventServiceProvider`: -->
Laravel은 인증 과정 중에 다양한 [events](/docs/8.x/events)를 발생시킵니다. `EventServiceProvider`에서 원하는 이벤트에 리스너를 등록할 수 있습니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Auth\Events\Registered' => [
        'App\Listeners\LogRegisteredUser',
    ],

    'Illuminate\Auth\Events\Attempting' => [
        'App\Listeners\LogAuthenticationAttempt',
    ],

    'Illuminate\Auth\Events\Authenticated' => [
        'App\Listeners\LogAuthenticated',
    ],

    'Illuminate\Auth\Events\Login' => [
        'App\Listeners\LogSuccessfulLogin',
    ],

    'Illuminate\Auth\Events\Failed' => [
        'App\Listeners\LogFailedLogin',
    ],

    'Illuminate\Auth\Events\Validated' => [
        'App\Listeners\LogValidated',
    ],

    'Illuminate\Auth\Events\Verified' => [
        'App\Listeners\LogVerified',
    ],

    'Illuminate\Auth\Events\Logout' => [
        'App\Listeners\LogSuccessfulLogout',
    ],

    'Illuminate\Auth\Events\CurrentDeviceLogout' => [
        'App\Listeners\LogCurrentDeviceLogout',
    ],

    'Illuminate\Auth\Events\OtherDeviceLogout' => [
        'App\Listeners\LogOtherDeviceLogout',
    ],

    'Illuminate\Auth\Events\Lockout' => [
        'App\Listeners\LogLockout',
    ],

    'Illuminate\Auth\Events\PasswordReset' => [
        'App\Listeners\LogPasswordReset',
    ],
];
```
