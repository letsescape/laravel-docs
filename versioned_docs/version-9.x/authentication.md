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
<!-- - [Social Authentication](/docs/9.x/socialite) -->
- [Social Authentication](/docs/9.x/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 방식을 제공합니다. 이러한 기능을 구현하는 것은 복잡하고 잠재적으로 위험할 수 있기 때문에, Laravel은 인증을 빠르고, 안전하며, 쉽게 구현할 수 있도록 필요한 도구를 제공합니다.

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel의 인증의 핵심은 "가드(guard)"와 "프로바이더(provider)"로 구성됩니다. 가드는 각 요청마다 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel에는 session 저장소와 쿠키를 사용하여 상태를 유지하는 `session` 가드가 내장되어 있습니다.

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/9.x/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
프로바이더는 영구 저장소에서 사용자를 어떻게 조회할지 정의합니다. Laravel에서는 기본적으로 [Eloquent](/docs/9.x/eloquent)와 데이터베이스 쿼리 빌더를 통해 사용자를 조회하는 프로바이더가 제공됩니다. 필요하다면 자신만의 프로바이더를 추가할 수도 있습니다.

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel의 인증 서비스 동작을 조정할 수 있는 여러 옵션이 잘 설명되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "권한(roles)"과 "퍼미션(permissions)" 개념과는 다릅니다. 권한을 기반으로 사용자 액션을 인가하는 방법에 대해서는 [authorization](/docs/9.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/9.x/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
빠르게 시작하고 싶으신가요? 새 Laravel 애플리케이션에서 [Laravel application starter kit](/docs/9.x/starter-kits)를 설치해 보세요. 데이터베이스 마이그레이션 후, 웹 브라우저에서 `/register`나 애플리케이션 전용 라우트에 접속하면 됩니다. 스타터 키트는 인증 시스템 전체의 기본 구조를 자동으로 만들어 줍니다!

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing the [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze) starter kit can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since Laravel Breeze creates authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**최종적으로 스타터 키트를 사용하지 않을 계획이더라도, [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze) 스타터 키트를 설치해보면 실제 Laravel 프로젝트에 인증 기능을 직접 구현하는 방법을 배울 수 있습니다.** Breeze는 인증 컨트롤러, 라우트, 뷰 파일을 자동으로 생성해주기 때문에 그 코드들을 살펴보며 Laravel에서 인증 기능이 어떻게 동작하는지 쉽게 이해할 수 있습니다.

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/9.x/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. -->
Laravel은 기본적으로 `app/Models` 디렉터리에 `App\Models\User` [Eloquent model](/docs/9.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 만약 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 사용하는 `database` 인증 프로바이더를 이용하세요.

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` 모델에 맞는 데이터베이스 스키마를 설계할 때는 반드시 비밀번호 컬럼의 길이가 최소 60자 이상이어야 합니다. 다행히도, 새롭게 생성되는 Laravel 앱에 포함된 기본 `users` 테이블 마이그레이션은 이보다 더 넉넉한 길이의 컬럼을 생성합니다.

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
또한, `users` (또는 해당 역할의) 테이블에는 100자 크기의 nullable string 타입인 `remember_token` 컬럼이 있어야 합니다. 이 컬럼은 "로그인 상태 유지(remember me)"를 선택한 사용자를 위한 토큰을 저장하는 데 사용됩니다. 역시, Laravel의 기본 `users` 테이블 마이그레이션에 이미 포함되어 있습니다.

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel은 인증과 관련된 몇 가지 패키지를 제공합니다. 본격적으로 시작하기 전에, Laravel의 인증 에코시스템을 간단히 살펴보고 각 패키지의 목적을 안내하겠습니다.

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/9.x/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
먼저, 인증이 어떻게 동작하는지 생각해봅시다. 사용자가 웹 브라우저를 통해 아이디와 비밀번호를 로그인 폼에 입력하면, 인증에 성공하면 해당 사용자의 정보가 [session](/docs/9.x/session)에 저장됩니다. 이때 세션 ID가 담긴 쿠키가 브라우저에 발급되어 이후의 요청마다 애플리케이션이 해당 사용자를 정확히 식별할 수 있게 됩니다. 세션 쿠키를 받은 뒤, 애플리케이션은 ID로 세션 데이터를 조회해서 인증 정보를 확인하고 사용자를 "인증됨" 상태로 처리합니다.

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
원격 서비스에서 애플리케이션의 API에 접근하기 위해 인증이 필요한 경우, 일반적으로 웹 브라우저가 없으므로 쿠키를 직접 사용할 수 없습니다. 대신 원격 서비스는 각 요청마다 API 토큰을 전송하며, 애플리케이션은 들어온 토큰을 저장된 토큰과 비교, 해당 토큰에 연결된 사용자를 인증하게 됩니다.

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel은 기본적으로 인증과 세션 서비스를 제공하며, 보통 `Auth`와 `Session` 파사드를 통해 사용합니다. 이러한 기능은 웹 브라우저에서 발생하는 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 정보를 확인하고 인증할 수 있는 여러 메서드를 내장하고 있으며, 인증된 정보는 자동으로 세션에 저장되고, 세션 쿠키를 발급합니다. 이 문서에서는 이러한 서비스들의 사용법을 안내합니다.

<!-- **Application Starter Kits** -->
**애플리케이션 스타터 키트**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free packages](/docs/9.x/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. These packages are [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/9.x/starter-kits#laravel-jetstream), and [Laravel Fortify](/docs/9.x/fortify). -->
이 문서에서 설명하는 것처럼, 인증 서비스를 직접 사용하여 나만의 인증 레이어를 구현할 수도 있습니다. 하지만 빠르게 시작하려면 전체 인증 레이어의 견고하고 현대적인 스캐폴딩을 제공하는 [free packages](/docs/9.x/starter-kits)을 사용하는 것이 좋습니다. 대표적으로 [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/9.x/starter-kits#laravel-jetstream), 그리고 [Laravel Fortify](/docs/9.x/fortify) 패키지가 준비되어 있습니다.

<!-- _Laravel Breeze_ is a simple, minimal implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is comprised of simple [Blade templates](/docs/9.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). To get started, check out the documentation on Laravel's [application starter kits](/docs/9.x/starter-kits). -->
_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 재확인 등, Laravel 인증의 주요 기능을 간결하게 구현한 패키지입니다. Breeze의 뷰 레이어는 [Blade templates](/docs/9.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 구성되어 있습니다. 자세한 내용은 [application starter kits](/docs/9.x/starter-kits)를 참고하세요.

<!-- _Laravel Fortify_ is a headless authentication backend for Laravel that implements many of the features found in this documentation, including cookie-based authentication as well as other features such as two-factor authentication and email verification. Fortify provides the authentication backend for Laravel Jetstream or may be used independently in combination with [Laravel Sanctum](/docs/9.x/sanctum) to provide authentication for an SPA that needs to authenticate with Laravel. -->
_Laravel Fortify_는 인증 백엔드만 제공하는 헤드리스(headless) 패키지로, 이 문서에 설명된 기능(쿠키 기반 인증, 2단계 인증, 이메일 인증 등)을 구현합니다. Fortify는 Laravel Jetstream의 인증 백엔드이기도 하며, [Laravel Sanctum](/docs/9.x/sanctum)과 조합하면 SPA(싱글 페이지 애플리케이션) 인증 백엔드로도 사용할 수 있습니다.

<!-- _[Laravel Jetstream](https://jetstream.laravel.com)_ is a robust application starter kit that consumes and exposes Laravel Fortify's authentication services with a beautiful, modern UI powered by [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), and / or [Inertia](https://inertiajs.com). Laravel Jetstream includes optional support for two-factor authentication, team support, browser session management, profile management, and built-in integration with [Laravel Sanctum](/docs/9.x/sanctum) to offer API token authentication. Laravel's API authentication offerings are discussed below. -->
_[Laravel Jetstream](https://jetstream.laravel.com)_은 [Tailwind CSS](https://tailwindcss.com), [Livewire](https://laravel-livewire.com), 그리고 [Inertia](https://inertiajs.com)로 만들어진 아름답고 현대적인 UI와 Fortify 인증을 통합 제공합니다. Jetstream은 2단계 인증, 팀, 브라우저 세션 관리, 프로필 관리, [Laravel Sanctum](/docs/9.x/sanctum)으로 API 토큰 인증 등 다양한 기능을 선택적으로 제공합니다. Laravel의 API 인증은 아래에서 별도로 다룹니다.

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/9.x/passport) and [Sanctum](/docs/9.x/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel은 API 토큰 관리를 돕는 두 가지 패키지, [Passport](/docs/9.x/passport)와 [Sanctum](/docs/9.x/sanctum)을 제공합니다. 참고로 이 라이브러리들은 Laravel에 내장된 쿠키 기반 인증 시스템과 함께 사용할 수 있습니다. 이 패키지들은 주로 API 토큰 인증을, 내장 인증 서비스는 쿠키 기반 브라우저 인증을 담당합니다. 실무에는 종종 Laravel의 내장 인증 서비스와 API 인증 패키지 중 하나를 함께 사용하는 경우가 많습니다.

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport는 OAuth2 인증 공급자 역할을 하며, 여러 OAuth2 "그랜트 타입"을 제공합니다. 이는 API 인증에 robust하고 복잡한 솔루션이지만, 실제로 대부분의 애플리케이션에서는 OAuth2 사양의 복잡한 기능이 필요하지 않습니다. 또한, SPA나 모바일 앱에서 OAuth2와 Passport를 이용한 인증이 다소 어렵거나 혼란스러울 수 있습니다.

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/9.x/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2의 복잡함과 개발자들이 경험한 혼란을 해결하고자, 웹 브라우저 기반의 1st-party 요청과 API 토큰 기반 요청을 모두 간단하게 처리할 수 있는 인증 패키지인 [Laravel Sanctum](/docs/9.x/sanctum)을 만들게 되었습니다. API와 웹 UI를 모두 제공하거나, SPA(싱글 페이지 애플리케이션)가 백엔드 Laravel과 분리되어 있거나 모바일 클라이언트를 지원하는 경우에 가장 적합한 인증 패키지입니다.

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/9.x/sanctum#how-it-works) documentation. -->
Sanctum은 웹/API 인증을 모두 아우르는 하이브리드 패키지입니다. Sanctum을 사용하는 애플리케이션은 요청이 들어오면 우선 세션 쿠키가 존재하는지 확인하여 인증된 세션인가를 확인합니다(이 과정에서 앞서 설명한 Laravel 내장 인증 서비스가 사용됨). 세션 쿠키가 없으면 API 토큰이 첨부되어 있는지도 확인해, 있다면 그 토큰을 인증에 사용합니다. 자세한 내용은 Sanctum의 ["how it works"](/docs/9.x/sanctum#how-it-works) 문서를 참고하세요.

<!-- Laravel Sanctum is the API package we have chosen to include with the [Laravel Jetstream](https://jetstream.laravel.com) application starter kit because we believe it is the best fit for the majority of web application's authentication needs. -->
Sanctum은 [Laravel Jetstream](https://jetstream.laravel.com)에서도 기본적으로 포함되어 있으며, 많은 웹 애플리케이션의 다양한 인증 요구에 가장 잘 어울리는 솔루션입니다.

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary & Choosing Your Stack -->
#### Summary & Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
정리하자면, 브라우저를 사용해 접근하는 모놀리식 Laravel 애플리케이션을 만든다면 내장 인증 서비스를 사용하면 됩니다.

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/9.x/passport) or [Sanctum](/docs/9.x/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
외부에서 API로 접근하는 경우라면, [Passport](/docs/9.x/passport) 혹은 [Sanctum](/docs/9.x/sanctum) 중 하나를 선택해 API 토큰 인증 기능을 도입하세요. 특별한 OAuth2 스펙의 모든 기능이 꼭 필요한 경우가 아니면, 대부분은 추가 설정이 간편하고 완결성 있는 Sanctum이 더 적합합니다("scopes" 및 "abilities"도 지원함).

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/9.x/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/9.x/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
Laravel 백엔드를 사용하는 SPA를 개발한다면, [Laravel Sanctum](/docs/9.x/sanctum)을 선택해야 합니다. Sanctum 사용 시에는 [manually implement your own backend authentication routes](#authenticating-users)하거나, [Laravel Fortify](/docs/9.x/fortify)를 도입해 헤드리스 인증 백엔드(회원가입, 비밀번호 재설정, 이메일 인증 등)를 사용할 수 있습니다.

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
OAuth2의 모든 정교한 기능이 꼭 필요하다면 Passport를 선택하세요.

<!-- And, if you would like to get started quickly, we are pleased to recommend [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services and Laravel Sanctum. -->
빠르게 시작하고 싶다면, [Laravel Breeze](/docs/9.x/starter-kits#laravel-breeze)로 바로 시작해서 내장 인증 서비스와 Sanctum이 모두 적용된 스타킹 상태의 새로운 Laravel 앱을 만들 것을 추천합니다.

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!WARNING]
> 이 부분은 [Laravel application starter kits](/docs/9.x/starter-kits)를 통한 인증 시스템 구축 방법(UI 스캐폴딩 포함)을 안내합니다. 인증 시스템과 직접 연동하고 싶으신 경우, [manually authenticating users](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
<!-- ### Install A Starter Kit -->
### Install A Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/9.x/starter-kits). Our current starter kits, Laravel Breeze and Laravel Jetstream, offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
먼저, [install a Laravel application starter kit](/docs/9.x/starter-kits)를 설치해야 합니다. 최신 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 인증 기능을 손쉽게 포함할 수 있도록 아름답게 디자인된 출발점을 제공합니다.

<!-- Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/9.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Breeze also offers an [Inertia](https://inertiajs.com) based scaffolding option using Vue or React. -->
Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 재확인 등 Laravel 인증의 모든 항목을 미니멀하고 간단하게 구현한 패키지입니다. Breeze의 뷰 레이어는 [Blade templates](/docs/9.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 꾸며져 있으며, [Inertia](https://inertiajs.com) 기반(Vue 또는 React 활용)의 스캐폴딩도 지원합니다.

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a more robust application starter kit that includes support for scaffolding your application with [Livewire](https://laravel-livewire.com) or [Inertia and Vue](https://inertiajs.com). In addition, Jetstream features optional support for two-factor authentication, teams, profile management, browser session management, API support via [Laravel Sanctum](/docs/9.x/sanctum), account deletion, and more. -->
[Laravel Jetstream](https://jetstream.laravel.com)은 Breeze보다 더욱 강력한 스타터 키트로, [Livewire](https://laravel-livewire.com) 또는 [Inertia and Vue](https://inertiajs.com) 기반으로 스캐폴딩이 가능합니다. Jetstream은 2단계 인증, 팀 기능, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/9.x/sanctum) 기반 API 지원, 계정 삭제 등 다양한 부가 기능을 선택적으로 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving The Authenticated User -->
### Retrieving The Authenticated User

<!-- After installing an authentication starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
인증 스타터 키트 설치 후, 사용자가 회원가입과 인증을 할 수 있게 된 다음에는, 현재 인증된 사용자와 상호작용할 일이 많습니다. 요청을 처리하면서 현재 인증된 사용자는 `Auth` 파사드의 `user` 메서드로 쉽게 조회할 수 있습니다.

```
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
인증이 완료된 후라면, `Illuminate\Http\Request` 인스턴스를 통해서도 인증된 사용자에 접근할 수 있습니다. 컨트롤러의 메서드에서 의존성으로 `Illuminate\Http\Request` 오브젝트를 주입받으면 언제든 `user` 메서드를 통해 인증된 사용자를 조회할 수 있습니다.

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
들어오는 HTTP 요청을 보낸 사용자가 인증된 상태인지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용합니다. 인증된 경우 `true`를 반환합니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> 사용자가 인증되었는지 확인하려면 `check` 메서드를 쓸 수 있지만, 실제로는 보통 미들웨어를 이용해 특정 라우트나 컨트롤러 접근 전 인증 여부를 검사합니다. 관련해서는 [protecting routes](/docs/9.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/9.x/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which references the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/9.x/middleware)를 사용하면 특정 라우트에 대해 인증된 사용자만 접근하도록 제한할 수 있습니다. Laravel에는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어가 기본 등록되어 있으므로, 미들웨어를 라우트에 할당만 하면 됩니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/9.x/routing#named-routes). You may modify this behavior by updating the `redirectTo` function in your application's `app/Http/Middleware/Authenticate.php` file: -->
`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 기본적으로 `login` [named route](/docs/9.x/routing#named-routes)로 리다이렉트합니다. 이 동작을 바꾸고 싶을 때는 `app/Http/Middleware/Authenticate.php` 파일의 `redirectTo` 함수를 수정하면 됩니다.

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
`auth` 미들웨어를 라우트에 연결할 때, 사용자를 인증할 때 사용할 "가드"를 지정할 수도 있습니다. 지정하는 값은 `auth.php` 설정 파일의 `guards` 배열에 있는 키 중 하나와 일치해야 합니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using the Laravel Breeze or Laravel Jetstream [starter kits](/docs/9.x/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
Laravel Breeze나 Laravel Jetstream [starter kits](/docs/9.x/starter-kits)를 사용한다면 로그인 시도에 대해 자동으로 rate limiting(시도 제한)이 적용됩니다. 기본적으로 여러 번 비밀번호/이메일을 틀리면 1분간 로그인을 시도할 수 없게 됩니다. 시도 제한은 사용자의 사용자명/이메일과 IP 주소별로 개별 적용됩니다.

> [!NOTE]
> 애플리케이션의 다른 라우트에도 시도 제한을 두고 싶다면 [rate limiting documentation](/docs/9.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/9.x/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
Laravel의 [application starter kits](/docs/9.x/starter-kits)를 반드시 사용해야 하는 것은 아닙니다. 스타터 키트를 쓰지 않는 경우, Laravel의 인증 클래스를 직접 활용해 사용자 인증을 관리할 수 있습니다. 걱정하지 마세요, 어렵지 않습니다!

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/9.x/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/9.x/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
Laravel의 인증 서비스는 `Auth` [facade](/docs/9.x/facades)를 통해 접근합니다. 먼저 클래스 상단에 `Auth` 파사드를 import하세요. 그리고 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 보통 애플리케이션의 "로그인" 폼에서 인증 요청이 들어올 때 사용합니다. 인증에 성공하면 [session](/docs/9.x/session)을 재생성하여 [session fixation](https://en.wikipedia.org/wiki/Session_fixation)을 방지해야 합니다.

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
        ])->onlyInput('email');
    }
}
```

<!-- The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the `password` value passed to the method via the array. You should not hash the incoming request's `password` value, since the framework will automatically hash the value before comparing it to the hashed password in the database. An authenticated session will be started for the user if the two hashed passwords match. -->
`attempt` 메서드는 배열 형태의 키/값 쌍을 첫 번째 인수로 받습니다. 이 배열의 값이 데이터베이스에서 사용자를 조회하는 데 사용됩니다. 위 예시에서는 `email` 컬럼으로 사용자를 찾고, 사용자가 존재하면 데이터베이스에 저장된 해시된 비밀번호와 배열로 전달된 `password` 값을 비교합니다. 들어온 요청의 `password` 값은 직접 해시 처리할 필요가 없습니다. 프레임워크가 비교 전에 자동으로 해싱하기 때문입니다. 두 해시된 비밀번호가 일치하면 인증된 세션이 시작됩니다.

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
Laravel의 인증 서비스는 지정된 인증 가드의 "프로바이더" 설정에 따라 사용자를 조회합니다. 기본적으로는 `config/auth.php`에 Eloquent 사용자 프로바이더가 설정되어 있으며, 이 경우 `App\Models\User` 모델을 사용합니다. 애플리케이션 상황에 따라 이 값을 자유롭게 변경할 수 있습니다.

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
`attempt` 메서드의 반환값은 인증 성공 시 `true`, 실패 시 `false`입니다.

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
`intended` 메서드는 인증 미들웨어에 의해 가로채기 전 사용자가 진입하려 했던 URL로 리다이렉트해 줍니다. 만약 해당 URL이 없다면 두 번째 인자로 지정한 URI로 이동합니다.

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
필요하다면, 사용자의 이메일과 비밀번호 이외에 다른 조건도 인증 쿼리에 추가할 수 있습니다. 이를 위해서는 `attempt` 메서드에 전달하는 배열에 쿼리 조건을 추가하기만 하면 됩니다. 예를 들어, 사용자가 "active"로 표시되어 있는지 확인할 수 있습니다.

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

<!-- For complex query conditions, you may provide a closure in your array of credentials. This closure will be invoked with the query instance, allowing you to customize the query based on your application's needs: -->
더 복잡한 쿼리 조건이 필요하다면, 크레덴셜 배열 내에 클로저를 추가할 수 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아, 애플리케이션 상황에 맞게 쿼리를 수정할 수 있습니다.

```
if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn ($query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> 위 예시에서 `email` 컬럼을 사용하는 것은 단순한 예시일 뿐이며, 필수값이 아닙니다. 사용자의 "아이디" 역할을 하는 컬럼명으로 자유롭게 변경할 수 있습니다.

<!-- The `attemptWhen` method, which receives a closure as its second argument, may be used to perform more extensive inspection of the potential user before actually authenticating the user. The closure receives the potential user and should return `true` or `false` to indicate if the user may be authenticated: -->
더 심화된 사용자를 검사해야 한다면, 클로저를 두 번째 인자로 받는 `attemptWhen` 메서드를 사용할 수 있습니다. 이 클로저는 사용자를 인자로 받아, 인증 가능 여부를 `true` 또는 `false`로 반환하게 하면 됩니다.

```
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function ($user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a name="accessing-specific-guard-instances"></a>
<!-- #### Accessing Specific Guard Instances -->
#### Accessing Specific Guard Instances

<!-- Via the `Auth` facade's `guard` method, you may specify which guard instance you would like to utilize when authenticating the user. This allows you to manage authentication for separate parts of your application using entirely separate authenticatable models or user tables. -->
`Auth` 파사드의 `guard` 메서드를 사용하면, 인증 시 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 애플리케이션의 별도 영역마다 서로 다른 인증 모델/테이블을 사용할 수도 있습니다.

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard` 메서드에 전달하는 가드 이름은 `auth.php` 설정 파일에 구성된 가드 중 하나와 일치해야 합니다.

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
로그인 폼에 "로그인 상태 유지(remember me)" 체크박스가 구현된 경우, 두 번째 인수로 불린 값을 `attempt` 메서드에 전달하면 됩니다.

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
이 값이 `true`이면 사용자가 명시적으로 로그아웃할 때까지 Laravel이 사용자를 무기한 인증 상태로 유지합니다. "remember me" 토큰을 저장하는 데 사용되는 문자열 `remember_token` 컬럼이 `users` 테이블에 반드시 포함되어 있어야 합니다. 신규 Laravel 앱에 포함된 `users` 테이블 마이그레이션에는 이미 이 컬럼이 들어 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<!-- If your application offers "remember me" functionality, you may use the `viaRemember`  method to determine if the currently authenticated user was authenticated using the "remember me" cookie: -->
"로그인 상태 유지"로 인증된 사용자 여부를 확인하려면 `viaRemember` 메서드를 사용하세요.

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
<!-- #### Authenticate A User Instance -->
#### Authenticate A User Instance

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/9.x/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
이미 존재하는 사용자 인스턴스를 현재 인증된 사용자로 설정해야 한다면, `Auth` 파사드의 `login` 메서드에 그 인스턴스를 전달하세요. 이때 전달되는 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/9.x/contracts)을 구현해야 합니다. Laravel의 기본 `App\Models\User` 모델은 이미 이 계약을 구현하고 있습니다. 즉, 회원가입 직후 등 이미 신뢰할 수 있는 사용자 인스턴스가 있을 때 유용합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` 메서드의 두 번째 인수로 불린 값을 전달하면 "로그인 상태 유지" 기능을 적용할 수 있습니다. 이 값은 해당 인증 세션에 "remember me" 기능을 원하는지를 나타냅니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
필요하다면, 먼저 인증 가드를 지정한 뒤 `login`을 호출할 수도 있습니다.

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate A User By ID -->
#### Authenticate A User By ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
데이터베이스의 주 키(primary key)로 사용자를 인증하고 싶다면 `loginUsingId` 메서드를 사용할 수 있습니다. 인수로 인증하려는 사용자의 주 키를 전달하세요.

```
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value as the second argument to the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId` 메서드의 두 번째 인수로 불린 값을 전달해 해당 인증 세션에 "로그인 상태 유지" 기능을 원하는지 지정할 수 있습니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate A User Once -->
#### Authenticate A User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method: -->
`once` 메서드를 사용하면, 세션이나 쿠키를 남기지 않고 단일 요청만 인증 상태로 처리할 수 있습니다.

```
if (Auth::once($credentials)) {
    //
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/9.x/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 "로그인" 페이지 구성 없이 빠르게 사용자 인증을 구현할 수 있는 간단한 방법입니다. 사용법은 `auth.basic` [middleware](/docs/9.x/middleware)를 라우트에 연결하면 끝입니다. `auth.basic` 미들웨어는 Laravel에 내장되어 있으므로, 별도의 정의가 필요 없습니다.

```
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
이 미들웨어를 라우트에 사용할 경우 브라우저에서 해당 라우트에 접근하면 인증 정보를 입력하라는 창이 자동으로 나타납니다. 기본값으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자의 "username"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note On FastCGI -->
#### A Note On FastCGI

<!-- If you are using PHP FastCGI and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
PHP FastCGI 및 Apache로 Laravel 앱을 서비스하는 경우, HTTP Basic 인증이 정상 동작하지 않을 수 있습니다. 이럴 때는 `.htaccess` 파일에 다음 설정을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/9.x/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
세션에 사용자 식별자를 쿠키로 기록하지 않고도 HTTP Basic 인증을 사용할 수 있습니다. 보통 API 요청을 HTTP 인증으로 처리할 때 유용합니다. 이를 위해 [define a middleware](/docs/9.x/middleware)를 만들고, 내부에서 `onceBasic` 메서드를 활용하세요. `onceBasic`이 null을 반환할 경우, 요청을 계속 체인에 넘깁니다.

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

<!-- Next, [register the route middleware](/docs/9.x/middleware#registering-middleware) and attach it to a route: -->
이제 [register the route middleware](/docs/9.x/middleware#registering-middleware)한 후, 라우트에 연결할 수 있습니다.

```
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic.once');
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
직접 사용자에게 로그아웃 기능을 제공하려면, `Auth` 파사드의 `logout` 메서드를 사용합니다. 이 메서드는 세션의 인증 정보를 제거하므로 이후 요청부터는 더 이상 인증되지 않습니다.

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/9.x/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
`logout` 메서드를 호출하는 것과 더불어, 사용자의 세션을 무효화하고 [CSRF token](/docs/9.x/csrf)을 재생성하는 것이 좋습니다. 로그아웃 이후에는 주로 애플리케이션 루트로 리다이렉트합니다.

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
Laravel은 현재 기기 외의 모든 다른 기기에서 로그인된 사용자의 세션을 무효화(즉시 로그아웃)할 수 있는 기능도 제공합니다. 주로 사용자가 비밀번호를 변경하는 순간 다른 기기에서의 세션만 만료시키고, 현재 기기는 계속 인증되도록 처리할 때 쓰입니다.

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is included on the routes that should receive session authentication. Typically, you should place this middleware on a route group definition so that it can be applied to the majority of your application's routes. By default, the `AuthenticateSession` middleware may be attached to a route using the `auth.session` route middleware key as defined in your application's HTTP kernel: -->
우선, `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 적용할 라우트에 포함되어 있는지 확인하세요. 일반적으로 앱 대부분의 라우트에 일괄 적용할 수 있도록 라우트 그룹 정의에 이 미들웨어를 지정하는 것이 좋습니다. 기본적으로 `AuthenticateSession` 미들웨어는 애플리케이션의 HTTP 커널에 정의된 `auth.session` 라우트 미들웨어 키를 사용해 라우트에 적용할 수 있습니다.

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
이제 `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자의 현재 비밀번호를 입력받아야 하며, 입력 데이터는 별도 폼 등으로 전달받아야 합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices` 메서드를 호출하면, 그 사용자로 인증된 모든 다른 세션이 강제로 만료되어, 등록된 모든 가드에서 로그아웃 처리됩니다.

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
애플리케이션을 구축하다 보면 일부 액션이나 민감한 영역 접근 전 사용자의 비밀번호를 다시 한번 확인(재입력)해야 할 때가 있습니다. Laravel에는 이를 쉽게 구현할 수 있도록 미들웨어가 준비되어 있습니다. 이 기능을 적용하려면, 비밀번호 재확인 화면을 보여주는 라우트와 비밀번호를 실제로 체크해주는 라우트 두 개를 만들어야 합니다.

> [!NOTE]
> 아래 내용은 직접 비밀번호 재확인 기능을 연동하는 방법을 안내합니다. 빠르게 적용하고 싶으시다면 [Laravel application starter kits](/docs/9.x/starter-kits)들이 이 기능을 기본 지원합니다!

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
비밀번호를 재확인한 후 동일 사용자는 3시간 동안 다시 비밀번호를 확인하지 않아도 됩니다. 이 시간 간격은 애플리케이션의 `config/auth.php` 파일에서 `password_timeout` 값을 변경하면 설정할 수 있습니다.

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
먼저, 사용자에게 비밀번호 재입력을 요청하는 뷰를 보여줄 라우트를 만듭니다.

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
당연히, 위 라우트가 반환하는 뷰는 `password` 필드가 포함된 폼이어야 하며, 유저가 민감 영역에 진입하기 전에 비밀번호를 재입력해야 한다는 안내문도 함께 포함하면 좋습니다.

<a name="confirming-the-password"></a>
<!-- #### Confirming The Password -->
#### Confirming The Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
다음으로, 사용자로부터 전달받은 비밀번호를 실제로 검증하고, 인증이 완료되면 사용자를 원래 목적지로 리다이렉트하는 POST 라우트를 만듭니다.

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
이 라우트가 어떻게 동작하는지 살펴봅시다. 먼저 요청의 `password` 필드가 실제 인증된 사용자의 비밀번호와 일치하는지 확인합니다. 올바르면 Laravel 세션에 비밀번호 확인 완료를 알려야 합니다. `passwordConfirmed` 메서드는 Laravel이 사용자가 마지막으로 비밀번호를 확인한 시점을 판단하는 데 사용할 수 있는 타임스탬프를 세션에 기록합니다. 마지막으로 사용자를 원래 시도하던 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/9.x/routing#named-routes): -->
최근 비밀번호 재확인이 필요한 라우트는 반드시 `password.confirm` 미들웨어를 할당해야 합니다. 이 미들웨어는 Laravel에 기본 내장되어 있으며, 사용자의 원래 목적지를 세션에 저장했다가 인증 완료 후 리다이렉트될 수 있도록 처리합니다. 지정된 미들웨어에 의해, 인증되지 않은 사용자는 `password.confirm` [named route](/docs/9.x/routing#named-routes)로 리다이렉트됩니다.

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

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/9.x/providers). Since Laravel already ships with an `AuthServiceProvider`, we can place the code in that provider: -->
`Auth` 파사드의 `extend` 메서드를 사용하면 자신만의 인증 가드를 정의할 수 있습니다. `extend` 메서드는 [service provider](/docs/9.x/providers) 내부에서 호출해야 합니다. Laravel에는 이미 `AuthServiceProvider`가 포함되어 있으므로, 여기에 코드를 추가하는 것이 일반적입니다.

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
위 예시에서 보듯, `extend`에 전달하는 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 구현체를 반환해야 합니다. 이 인터페이스의 메서드를 적절히 구현하면 사용자 정의 가드가 완성됩니다. 커스텀 가드를 완성했다면, `auth.php` 설정 파일의 `guards` 항목에서 사용할 수 있습니다.

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
간단하게 HTTP 요청 기반의 커스텀 인증을 구현하려면 `Auth::viaRequest` 메서드를 사용할 수 있습니다. 이 메서드는 단일 클로저로 인증 프로세스를 신속하게 정의할 수 있도록 해줍니다.

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your `AuthServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
시작하려면, `AuthServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest` 메서드를 호출하세요. `viaRequest` 메서드의 첫 번째 인수는 인증 드라이버 이름이며, 커스텀 가드를 설명하는 임의의 문자열이면 됩니다. 두 번째 인수로는 들어오는 HTTP 요청을 받아서 사용자 인스턴스를 반환하거나, 인증에 실패하면 `null`을 반환하는 클로저를 전달합니다.

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
        return User::where('token', (string) $request->token)->first();
    });
}
```

<!-- Once your custom authentication driver has been defined, you may configure it as a driver within the `guards` configuration of your `auth.php` configuration file: -->
이제 이 커스텀 인증 드라이버를 `auth.php` 설정 파일의 `guards` 항목에서 사용할 수 있습니다.

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<!-- Finally, you may reference the guard when assigning the authentication middleware to a route: -->
마지막으로, 인증 미들웨어에 해당 가드를 적용해 라우트를 보호하면 됩니다.

```
Route::middleware('auth:api')->group(function () {
    // ...
}
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
기존의 관계형 데이터베이스가 아니라서 기본 UserProvider를 쓸 수 없다면, `Auth` 파사드의 `provider` 메서드로 커스텀 사용자 프로바이더를 정의할 수 있습니다. 사용자 프로바이더는 반드시 `Illuminate\Contracts\Auth\UserProvider` 계약을 구현해야 합니다.

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
마지막으로, `guards` 항목에서 이 프로바이더를 참조하도록 설정하세요.

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
`Illuminate\Contracts\Auth\UserProvider` 구현체는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등 영구 저장소 시스템에서 꺼내오는 역할을 합니다. 이 두 인터페이스를 통해 Laravel의 인증 메커니즘은 데이터 저장 방식이나 유저 클래스를 변경하더라도 동일하게 동작할 수 있습니다.

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
아래는 `Illuminate\Contracts\Auth\UserProvider` 계약의 핵심 메서드 예시입니다.

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
`retrieveById` 함수는 일반적으로 MySQL 데이터베이스의 자동 증가 ID처럼 사용자를 나타내는 키를 받습니다. 해당 ID와 일치하는 `Authenticatable` 구현체를 조회해 반환해야 합니다.

<!-- The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method. -->
`retrieveByToken` 함수는 사용자의 고유 `$identifier`와 "remember me" `$token`으로 사용자를 조회합니다. 이 토큰은 보통 `remember_token`과 같은 데이터베이스 컬럼에 저장됩니다. 앞선 메서드와 마찬가지로, 토큰 값이 일치하는 `Authenticatable` 구현체를 이 메서드에서 반환해야 합니다.

<!-- The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out. -->
`updateRememberToken` 메서드는 `$user` 인스턴스의 `remember_token`을 새 `$token`으로 갱신합니다. "remember me" 인증에 성공했을 때나 사용자가 로그아웃할 때 새 토큰이 사용자에게 할당됩니다.

<!-- The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.** -->
`retrieveByCredentials` 메서드는 애플리케이션 인증을 시도할 때 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받습니다. 그런 다음 이 메서드는 해당 자격 증명과 일치하는 사용자를 기본 영구 저장소에서 "조회"해야 합니다. 일반적으로 이 메서드는 `$credentials['username']` 값과 일치하는 "username"을 가진 사용자 레코드를 찾기 위해 "where" 조건이 포함된 쿼리를 실행합니다. 이 메서드는 `Authenticatable` 구현체를 반환해야 합니다. **이 메서드에서 비밀번호 검증이나 인증을 시도해서는 안 됩니다.**

<!-- The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid. -->
`validateCredentials` 메서드는 주어진 `$user`와 `$credentials`를 비교해 사용자를 인증해야 합니다. 예를 들어 이 메서드는 보통 `Hash::check` 메서드를 사용해 `$user->getAuthPassword()` 값과 `$credentials['password']` 값을 비교합니다. 이 메서드는 비밀번호가 유효한지 여부를 나타내는 `true` 또는 `false`를 반환해야 합니다.

<a name="the-authenticatable-contract"></a>
<!-- ### The Authenticatable Contract -->
### The Authenticatable Contract

<!-- Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods: -->
`UserProvider`의 각 메서드를 살펴봤으니, 이제 `Authenticatable` 계약도 살펴보겠습니다. 사용자 프로바이더는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스를 구현한 인스턴스를 반환해야 한다는 점을 기억하세요.

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
이 인터페이스는 단순합니다. `getAuthIdentifierName` 메서드는 사용자의 "primary key" 필드 이름을 반환하고, `getAuthIdentifier` 메서드는 사용자의 "primary key" 값을 반환해야 합니다. MySQL 백엔드를 사용하는 경우 이는 보통 사용자 레코드에 할당된 자동 증가 기본 키일 것입니다. `getAuthPassword` 메서드는 사용자의 해시된 비밀번호를 반환해야 합니다.

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes a `App\Models\User` class in the `app/Models` directory which implements this interface. -->
이 인터페이스만 구현되어 있으면 인증 시스템은 어떤 ORM이나 저장소 추상화 계층을 사용하든 모든 "user" 클래스와 연동할 수 있습니다. Laravel은 기본으로 이 인터페이스를 구현한 `App\Models\User` 클래스를 `app/Models` 디렉터리에 포함합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/9.x/events) during the authentication process. You may attach listeners to these events in your `EventServiceProvider`: -->
Laravel은 인증 과정에서 다양한 [events](/docs/9.x/events)를 발생시킵니다. `EventServiceProvider`에서 이 이벤트에 리스너를 등록해 활용할 수 있습니다.

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