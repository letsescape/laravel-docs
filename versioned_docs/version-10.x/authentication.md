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
<!-- - [Social Authentication](/docs/10.x/socialite) -->
- [Social Authentication](/docs/10.x/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
많은 웹 애플리케이션은 사용자가 인증 및 "로그인"할 수 있는 기능을 제공합니다. 이러한 기능을 웹 애플리케이션에 구현하는 일은 상당히 복잡하고 보안상 위험을 동반할 수 있습니다. Laravel은 여러분이 인증 기능을 빠르고 안전하게, 그리고 쉽게 구축할 수 있도록 필요한 도구들을 제공합니다.

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel 인증 시스템의 핵심은 "가드(guard)"와 "프로바이더(provider)"로 구성됩니다. 가드는 각 요청에 대해 사용자를 어떻게 인증할지 정의합니다. 예를 들어, Laravel에는 세션 저장소와 쿠키를 활용하여 상태를 유지하는 `session` 가드가 기본 제공됩니다.

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/10.x/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
프로바이더는 사용자를 영구 저장소(데이터베이스)에서 어떻게 불러오는지 정의합니다. Laravel은 [Eloquent](/docs/10.x/eloquent) 및 데이터베이스 쿼리 빌더를 이용한 사용자 조회를 지원합니다. 필요하다면 여러분의 애플리케이션에 맞는 추가 프로바이더 정의도 가능합니다.

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
애플리케이션의 인증 설정 파일은 `config/auth.php`에 위치합니다. 이 파일에는 Laravel 인증 서비스의 동작을 세밀하게 제어할 수 있는 다양한 옵션이 문서화되어 있습니다.

> [!NOTE]
> 가드와 프로바이더는 "역할(role)"이나 "권한(permission)"과 혼동해서는 안 됩니다. 권한을 이용한 사용자 액션 인가에 대해 더 알고 싶으시면 [authorization](/docs/10.x/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/10.x/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
빠르게 시작하고 싶으신가요? 새로운 Laravel 애플리케이션에서 [Laravel application starter kit](/docs/10.x/starter-kits)를 설치하세요. 데이터베이스 마이그레이션을 완료한 후, 브라우저에서 `/register` 또는 애플리케이션에 할당된 URL로 이동하면, 스타터 키트가 인증 시스템의 뼈대를 자동으로 만들어 줍니다!

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing the [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze) starter kit can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since Laravel Breeze creates authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**설령 실제 서비스에 스타터 키트를 직접 사용하지 않는다 하더라도, [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze) 스타터 키트를 설치하면 실제 Laravel 프로젝트에서 인증 기능 전반을 어떻게 구현하는지 학습할 수 있는 훌륭한 기회를 얻을 수 있습니다.** Laravel Breeze는 인증에 필요한 컨트롤러, 라우트, 뷰를 만들어 주므로, 해당 파일들의 코드를 직접 열어보고 Laravel 인증이 어떻게 작동하는지 배울 수 있습니다.

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/10.x/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. -->
Laravel은 기본적으로 `app/Models` 디렉토리에 `App\Models\User` [Eloquent model](/docs/10.x/eloquent)을 포함하고 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용할 수 있습니다. 애플리케이션에서 Eloquent를 사용하지 않는 경우, Laravel 쿼리 빌더를 활용하는 `database` 인증 프로바이더도 사용할 수 있습니다.

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` 모델에 맞는 데이터베이스 스키마를 정의할 때, 비밀번호 컬럼이 최소 60글자 이상이 되도록 하세요. 참고로, 새로운 Laravel 애플리케이션의 `users` 테이블 마이그레이션에는 이미 이보다 긴 컬럼이 생성되어 있습니다.

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
또한, `users`(또는 동등한) 테이블에 길이 100의 null 가능 문자열 타입 `remember_token` 컬럼이 포함되어 있는지 확인하세요. 이 컬럼은 사용자가 "로그인 상태 유지(remember me)" 옵션을 선택했을 때 토큰 값을 저장하는 데 사용됩니다. 역시, 기본 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel은 인증과 관련된 다양한 패키지를 제공합니다. 본격적으로 시작하기 전에, Laravel 전반에서 지원되는 인증 생태계를 살펴보고, 각 패키지의 목적에 대해 알아보겠습니다.

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/10.x/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
우선, 인증의 작동 방식을 생각해봅시다. 사용자가 웹 브라우저에서 로그인 폼에 아이디와 비밀번호를 입력하면, 서버는 이 정보를 확인한 뒤, 인증된 사용자 정보를 [session](/docs/10.x/session)에 저장합니다. 브라우저에는 세션 ID를 담은 쿠키가 발행되어, 앞으로의 요청에서 사용자가 올바른 세션에 연결될 수 있습니다. 세션 쿠키를 통해 애플리케이션은 세션 데이터를 읽어 인증 정보를 확인하고, 사용자를 "인증된 상태"로 처리합니다.

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
반면, 원격 서비스가 API 접근을 위해 인증하려는 경우에는 웹 브라우저가 없으므로 일반적으로 쿠키가 사용되지 않습니다. 대신, 원격 서비스는 매 요청마다 API 토큰을 API 서버에 전송합니다. 애플리케이션은 이 토큰을 허용된 토큰 목록과 비교해, 해당 토큰에 연결된 사용자로 요청을 "인증"하게 됩니다.

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel은 내장 인증 및 세션 서비스를 제공하며, 주로 `Auth`와 `Session` 파사드를 통해 사용할 수 있습니다. 이 기능들은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 사용자의 자격 증명 확인과 인증 처리를 위한 여러 메서드가 제공되며, 인증 데이터는 자동으로 세션에 저장되고, 세션 쿠키가 발급됩니다. 이 문서에서는 이러한 서비스의 사용 방법을 다룹니다.

<!-- **Application Starter Kits** -->
**애플리케이션 스타터 키트**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free packages](/docs/10.x/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. These packages are [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/10.x/starter-kits#laravel-jetstream), and [Laravel Fortify](/docs/10.x/fortify). -->
여기서 소개하는 인증 서비스들을 직접 조합해 애플리케이션만의 인증 레이어를 구현할 수도 있지만, 보다 빠른 시작을 원한다면 [free packages](/docs/10.x/starter-kits)를 활용하면 튼튼하고 현대적인 인증 시스템 뼈대를 신속하게 구축할 수 있습니다. 대표적인 스타터 키트로는 [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/10.x/starter-kits#laravel-jetstream), [Laravel Fortify](/docs/10.x/fortify)가 있습니다.

<!-- _Laravel Breeze_ is a simple, minimal implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is comprised of simple [Blade templates](/docs/10.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). To get started, check out the documentation on Laravel's [application starter kits](/docs/10.x/starter-kits). -->
_Laravel Breeze_는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel 인증의 모든 기능을 간소하고 최소한의 구성을 통해 제공합니다. 뷰는 간단한 [Blade templates](/docs/10.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 꾸며져 있습니다. 자세한 시작 방법은 Laravel의 [application starter kits](/docs/10.x/starter-kits) 문서를 참고하세요.

<!-- _Laravel Fortify_ is a headless authentication backend for Laravel that implements many of the features found in this documentation, including cookie-based authentication as well as other features such as two-factor authentication and email verification. Fortify provides the authentication backend for Laravel Jetstream or may be used independently in combination with [Laravel Sanctum](/docs/10.x/sanctum) to provide authentication for an SPA that needs to authenticate with Laravel. -->
_Laravel Fortify_는 Laravel용 헤드리스 인증 백엔드로, 쿠키 기반 인증 뿐만 아니라, 2차 인증, 이메일 인증 등 다양한 인증 기능을 제공합니다. 보통은 Laravel Jetstream의 인증 백엔드로 사용하거나, [Laravel Sanctum](/docs/10.x/sanctum)과 함께 SPA(싱글 페이지 애플리케이션) 인증 백엔드로 독립적으로 활용할 수 있습니다.

<!-- _[Laravel Jetstream](https://jetstream.laravel.com)_ is a robust application starter kit that consumes and exposes Laravel Fortify's authentication services with a beautiful, modern UI powered by [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), and / or [Inertia](https://inertiajs.com). Laravel Jetstream includes optional support for two-factor authentication, team support, browser session management, profile management, and built-in integration with [Laravel Sanctum](/docs/10.x/sanctum) to offer API token authentication. Laravel's API authentication offerings are discussed below. -->
_[Laravel Jetstream](https://jetstream.laravel.com)_은 Fortify의 인증 기능을 현대적인 UI와 함께 제공하는 강력한 스타터 키트로, [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), [Inertia](https://inertiajs.com) 기반의 아름답고 모던한 UI를 갖추고 있습니다. 2차 인증, 팀 시스템, 브라우저 세션/프로필 관리, [Laravel Sanctum](/docs/10.x/sanctum)과의 연동을 통한 API 토큰 인증 등까지 폭넓게 지원합니다. Laravel API 인증 관련 내용은 아래에서 자세히 다룹니다.

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/10.x/passport) and [Sanctum](/docs/10.x/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel은 API 토큰 관리 및 인증을 위해 선택적으로 사용할 수 있는 [Passport](/docs/10.x/passport)와 [Sanctum](/docs/10.x/sanctum) 두 가지 패키지를 제공합니다. 이들 패키지와 Laravel의 기본 쿠키 인증 라이브러리는 함께 쓸 수 있으며, 충돌하지 않습니다. 여기서 소개하는 패키지들은 주로 API 토큰 인증에, 기본 인증 서비스는 브라우저 쿠키 인증에 집중합니다. 많은 애플리케이션에서는 두 방식을 동시에 사용할 수 있습니다.

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport는 OAuth2 인증 제공자로, 다양한 OAuth2 "grant type" 지원을 통해 여러 종류의 토큰을 발급할 수 있습니다. 매우 강력하고 복잡한 API 인증 패키지이지만, 대부분의 애플리케이션에서는 OAuth2 규격의 복잡한 기능까지 필요하지 않아, 사용자와 개발자 모두에게 다소 부담이 될 수 있습니다. 또한, SPA나 모바일 앱에서의 OAuth2 사용에 혼란을 겪는 개발자들이 많았습니다.

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/10.x/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2의 복잡성과 혼란을 해결하기 위해, 더 간결하고 직관적인 인증 패키지인 [Laravel Sanctum](/docs/10.x/sanctum)이 만들어졌습니다. Sanctum은 웹 브라우저에서의 1차 요청과 API 토큰을 활용한 요청 모두를 처리할 수 있어, 웹 UI와 API를 동시에 제공하거나, 백엔드와 분리된 SPA, 모바일 클라이언트를 지원하는 애플리케이션에 가장 적합합니다.

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/10.x/sanctum#how-it-works) documentation. -->
Sanctum 기반 애플리케이션은 요청을 받을 때, 우선 세션 쿠키로 인증된 세션이 있는지 확인하며, 있다면 앞서 살펴본 Laravel의 내장 인증 서비스를 호출해 처리합니다. 만약 세션 쿠키가 인증되지 않은 경우라면, Sanctum은 해당 요청에 API 토큰이 있는지 검사하고, 있으면 해당 토큰으로 인증합니다. 자세한 내용은 Sanctum의 ["how it works"](/docs/10.x/sanctum#how-it-works)를 참고하세요.

<!-- Laravel Sanctum is the API package we have chosen to include with the [Laravel Jetstream](https://jetstream.laravel.com) application starter kit because we believe it is the best fit for the majority of web application's authentication needs. -->
Sanctum은 저희가 [Laravel Jetstream](https://jetstream.laravel.com) 스타터 키트와 함께 기본 포함시킨 인증 패키지로, 지금까지 소개한 인증 시나리오의 대부분에 가장 적합하다고 할 수 있습니다.

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary and Choosing Your Stack -->
#### Summary and Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
요약하자면, 브라우저를 이용하는 모놀리식(Monolithic) Laravel 애플리케이션이라면 내장 인증 서비스만으로 충분합니다.

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/10.x/passport) or [Sanctum](/docs/10.x/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
외부에서 API를 활용하는 경우라면, 애플리케이션 특성에 맞게 [Passport](/docs/10.x/passport) 또는 [Sanctum](/docs/10.x/sanctum) 중 하나를 선택해 API 토큰 인증을 적용하세요. 대부분의 경우, 간단하고 완성도 높은 API 인증/SPA 인증/모바일 인증 기능과 "scope(혹은 ability)"도 제공하는 Sanctum을 추천합니다.

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/10.x/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/10.x/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
Laravel을 백엔드로 사용하는 SPA를 개발하는 경우에도 [Laravel Sanctum](/docs/10.x/sanctum)이 가장 적합합니다. 이 때, [manually implement your own backend authentication routes](#authenticating-users), [Laravel Fortify](/docs/10.x/fortify)를 헤드리스 인증 백엔드로 이용할 수 있습니다. Fortify는 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 라우트와 컨트롤러도 제공합니다.

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
반드시 OAuth2의 모든 기능이 필요한 특별한 경우라면 Passport를 선택하세요.

<!-- And, if you would like to get started quickly, we are pleased to recommend [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services and Laravel Sanctum. -->
그리고, 빠르게 시작하고 싶으시다면, [Laravel Breeze](/docs/10.x/starter-kits#laravel-breeze)로 내장 인증 서비스와 Sanctum을 조합한 추천 인증 스택을 즉시 경험해 보실 수 있습니다.

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!WARNING]
> 이 섹션에서는 [Laravel application starter kits](/docs/10.x/starter-kits)를 이용해 인증 시스템을 구축하는 방법을 설명합니다. 스타터 키트에는 빠른 시작을 돕는 UI 뼈대가 포함되어 있습니다. Laravel 인증 시스템을 직접 구현하고 싶으시다면 [manually authenticating users](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
<!-- ### Install a Starter Kit -->
### Install a Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/10.x/starter-kits). Our current starter kits, Laravel Breeze and Laravel Jetstream, offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
먼저, [install a Laravel application starter kit](/docs/10.x/starter-kits)를 설치하세요. 최신의 스타터 키트인 Laravel Breeze와 Laravel Jetstream은 인증이 반영된 아름다운 초기 구조를 제공합니다.

<!-- Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/10.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Additionally, Breeze provides scaffolding options based on [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com), with the choice of using Vue or React for the Inertia-based scaffolding. -->
Laravel Breeze는 로그인, 회원가입, 비밀번호 재설정, 이메일 인증, 비밀번호 확인 등 Laravel의 모든 인증 기능을 최소 목적에 맞게, 간단하게 구현합니다. 뷰는 [Blade templates](/docs/10.x/blade)과 [Tailwind CSS](https://tailwindcss.com)로 만들었습니다. 더불어, [Livewire](https://livewire.laravel.com)나 [Inertia](https://inertiajs.com) 기반(Vue 또는 React 선택 가능) 뼈대도 옵션으로 제공합니다.

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a more robust application starter kit that includes support for scaffolding your application with [Livewire](https://livewire.laravel.com) or [Inertia and Vue](https://inertiajs.com). In addition, Jetstream features optional support for two-factor authentication, teams, profile management, browser session management, API support via [Laravel Sanctum](/docs/10.x/sanctum), account deletion, and more. -->
[Laravel Jetstream](https://jetstream.laravel.com)은 [Livewire](https://livewire.laravel.com) 또는 [Inertia and Vue](https://inertiajs.com)로 애플리케이션 뼈대를 구축할 수 있는 더욱 강력한 스타터 키트입니다. Jetstream에는 2차 인증, 팀, 프로필 관리, 브라우저 세션 관리, [Laravel Sanctum](/docs/10.x/sanctum)을 통한 API 지원, 계정 삭제 등 다양한 추가 기능도 선택적으로 제공됩니다.

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving the Authenticated User -->
### Retrieving the Authenticated User

<!-- After installing an authentication starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
인증 스타터 키트를 설치하고, 사용자가 회원가입 및 로그인할 수 있도록 구현한 후에는, 현재 인증된 사용자 정보를 자주 활용하게 됩니다. 요청을 처리할 때는 `Auth` 파사드의 `user` 메서드를 통해 현재 인증된 사용자 인스턴스에 접근할 수 있습니다.

```
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
또는, 인증된 사용자는 `Illuminate\Http\Request` 인스턴스에서도 접근할 수 있습니다. 타입힌트가 지정된 클래스는 컨트롤러 메서드에 자동으로 주입된다는 점을 기억하세요. `Illuminate\Http\Request` 객체에 타입힌트를 지정하면, 요청의 `user` 메서드를 통해 애플리케이션의 어떤 컨트롤러 메서드에서든 인증된 사용자에 편리하게 접근할 수 있습니다.

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
들어오는 HTTP 요청의 사용자가 인증된 상태인지 확인하려면, `Auth` 파사드의 `check` 메서드를 사용하면 됩니다. 사용자가 인증된 상태라면 `true`를 반환합니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드를 통해 인증 여부를 직접 확인할 수도 있지만, 실제로는 대부분의 경우 미들웨어를 활용해 사용자가 인증된 상태에서만 특정 라우트나 컨트롤러에 접근하도록 제한합니다. 자세한 내용은 [protecting routes](/docs/10.x/authentication#protecting-routes) 문서를 참고하세요.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/10.x/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which references the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already registered in your application's HTTP kernel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/10.x/middleware)를 사용하면, 인증된 사용자만 특정 라우트에 접근할 수 있도록 제한할 수 있습니다. Laravel에는 `Illuminate\Auth\Middleware\Authenticate` 클래스를 참조하는 `auth` 미들웨어가 내장되어 있습니다. 해당 미들웨어는 이미 애플리케이션의 HTTP 커널에 등록되어 있으므로, 라우트에 바로 붙여 사용할 수 있습니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/10.x/routing#named-routes). You may modify this behavior by updating the `redirectTo` function in your application's `app/Http/Middleware/Authenticate.php` file: -->
`auth` 미들웨어는 인증되지 않은 사용자를 감지하면 `login` [named route](/docs/10.x/routing#named-routes)로 자동 리다이렉트합니다. 이 동작을 변경하고 싶을 경우, 애플리케이션의 `app/Http/Middleware/Authenticate.php` 파일 내 `redirectTo` 함수를 수정하세요.

```
use Illuminate\Http\Request;

/**
 * Get the path the user should be redirected to.
 */
protected function redirectTo(Request $request): string
{
    return route('login');
}
```

<a name="specifying-a-guard"></a>
<!-- #### Specifying a Guard -->
#### Specifying a Guard

<!-- When attaching the `auth` middleware to a route, you may also specify which "guard" should be used to authenticate the user. The guard specified should correspond to one of the keys in the `guards` array of your `auth.php` configuration file: -->
`auth` 미들웨어를 라우트에 사용할 때 어떤 "가드"로 인증할지 명시적으로 지정할 수 있습니다. 해당 가드는 `auth.php` 설정 파일의 `guards` 배열 키 중 하나여야 합니다.

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using the Laravel Breeze or Laravel Jetstream [starter kits](/docs/10.x/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
Laravel Breeze나 Laravel Jetstream [starter kits](/docs/10.x/starter-kits)를 사용하는 경우, 로그인 시도에 자동으로 속도 제한(rate limit)이 적용됩니다. 기본적으로 사용자가 여러 번 틀린 정보를 입력하면 1분 동안 로그인을 시도할 수 없습니다. 이 제한은 사용자의 아이디/이메일, 그리고 IP를 기준으로 개별 적용됩니다.

> [!NOTE]
> 애플리케이션 내 다른 라우트에도 속도 제한을 적용하고 싶으시다면, [rate limiting documentation](/docs/10.x/routing#rate-limiting)를 참고하세요.

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/10.x/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
[application starter kits](/docs/10.x/starter-kits)가 제공하는 인증 뼈대를 꼭 사용해야 하는 것은 아닙니다. 만약 직접 인증 로직을 구현하고 싶다면, Laravel의 인증 클래스를 직접 활용하시면 됩니다. 걱정하지 마세요, 아주 간단합니다!

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/10.x/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/10.x/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
Laravel 인증 서비스는 `Auth` [facade](/docs/10.x/facades)를 통해 접근하므로, 클래스 상단에 `Auth` 파사드를 꼭 import 해주세요. 다음으로 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 일반적으로 애플리케이션의 "로그인" 폼에서 들어온 인증 시도를 처리하는 데 사용됩니다. 인증이 성공하면 [session](/docs/10.x/session)을 재생성하여 [session fixation](https://en.wikipedia.org/wiki/Session_fixation)을 예방해야 합니다.

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
`attempt` 메서드는 첫 번째 인자로 key/value 쌍의 배열을 받습니다. 이 배열의 값은 사용자를 데이터베이스에서 찾는 데 사용됩니다. 위 예시에서는 `email` 컬럼 값을 기준으로 사용자를 조회하고, 데이터베이스에 저장된 해시된 비밀번호와 배열로 전달된 `password` 값을 비교합니다. 들어온 요청의 `password` 값은 직접 해싱할 필요가 없습니다. 프레임워크가 비교 전에 자동으로 입력값을 해시하기 때문입니다. 두 해시된 비밀번호가 일치하면 사용자의 인증 세션이 시작됩니다.

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
Laravel 인증 서비스는 각 가드의 프로바이더 설정에 따라 사용자를 데이터베이스에서 조회합니다. 기본 `config/auth.php`에서는 Eloquent 사용자 프로바이더가 지정되어 있고, 사용자를 조회할 때 `App\Models\User` 모델을 사용합니다. 필요에 따라 설정 파일을 수정하면 됩니다.

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
인증 성공 시 `attempt`는 `true`를, 실패하면 `false`를 반환합니다.

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
Laravel redirector가 제공하는 `intended` 메서드는 인증 미들웨어에 의해 차단되기 전 사용자가 접근하려던 URL로 리다이렉트시켜 줍니다. 해당 목적지가 없을 경우 이 메서드에 대체 URI를 지정할 수 있습니다.

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
이메일과 비밀번호 외에 다른 조건도 인증 쿼리에 추가하고 싶을 때는, `attempt`에 전달하는 배열에 조건을 추가하면 됩니다. 예를 들어, 사용자 활성화 여부까지 확인하려면 아래와 같이 쓸 수 있습니다.

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

<!-- For complex query conditions, you may provide a closure in your array of credentials. This closure will be invoked with the query instance, allowing you to customize the query based on your application's needs: -->
더 복잡한 쿼리 조건이 필요할 경우, 배열의 값으로 클로저를 지정할 수 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받아, 쿼리를 자유롭게 커스터마이징할 수 있습니다.

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
> 위 예시에서 `email`은 필수 항목이 아니며, 예시를 위해 사용된 것입니다. 여러분의 데이터베이스에서 "사용자명"으로 쓰이는 컬럼 명을 자유롭게 사용하세요.

<!-- The `attemptWhen` method, which receives a closure as its second argument, may be used to perform more extensive inspection of the potential user before actually authenticating the user. The closure receives the potential user and should return `true` or `false` to indicate if the user may be authenticated: -->
`attemptWhen` 메서드는 두 번째 인자로 클로저를 받아, 실제 인증 전 후보 사용자를 좀 더 정밀하게 검사할 수 있습니다. 클로저는 해당 사용자 인스턴스를 받아, 인증 가능 여부에 따라 `true` 또는 `false`를 반환하면 됩니다.

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
`Auth` 파사드의 `guard` 메서드를 이용해, 인증에 사용할 특정 가드 인스턴스를 지정할 수 있습니다. 이를 통해 서로 다른 부분에서 독립적인 인증 모델이나 사용자 테이블을 쓸 수 있습니다.

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard`에 전달하는 이름은 반드시 `auth.php` 설정 파일의 guards 중 하나여야 합니다.

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
많은 웹 애플리케이션에서 로그인 폼에 "로그인 상태 유지(remember me)" 체크박스를 제공합니다. 이런 기능을 구현하려면 `attempt` 메서드의 두 번째 인자로 불리언 값을 넘기면 됩니다.

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
이 값이 `true`면, 사용자는 명시적으로 로그아웃하거나 삭제할 때까지 인증 상태로 유지됩니다. `users` 테이블에는 "remember me" 토큰을 저장하는 데 사용되는 문자열 `remember_token` 컬럼이 반드시 존재해야 합니다. Laravel 신규 프로젝트에 포함된 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다.

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<!-- If your application offers "remember me" functionality, you may use the `viaRemember`  method to determine if the currently authenticated user was authenticated using the "remember me" cookie: -->
만약 "로그인 상태 유지(remember me)" 기능이 있다면, 현재 인증된 사용자가 remember me 쿠키로 인증되었는지 `viaRemember` 메서드로 판단할 수 있습니다.

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

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/10.x/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
기존 사용자 인스턴스를 현재 인증된 사용자로 설정해야 할 때는, 해당 인스턴스를 `Auth` 파사드의 `login` 메서드에 넘기면 됩니다. 전달하는 사용자는 반드시 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/10.x/contracts)을 구현하고 있어야 하며, 기본 제공되는 `App\Models\User`도 이미 이 인터페이스를 구현하고 있습니다. 이 방식은 회원가입 직후와 같이 이미 사용자 인스턴스가 준비된 경우에 유용합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` 메서드의 두 번째 인자로 불리언 값을 넘기면 "로그인 상태 유지" 기능을 적용할 수 있습니다. 이 값은 해당 인증 세션에 "remember me" 기능을 원하는지를 나타냅니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
필요하다면, `login` 호출 전에 사용할 가드를 명시할 수도 있습니다.

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate a User by ID -->
#### Authenticate a User by ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
데이터베이스의 기본키를 활용해 사용자를 인증하고 싶다면, `loginUsingId` 메서드를 사용하세요. 이 메서드는 인증할 사용자의 기본키(primary key)를 전달받습니다.

```
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value as the second argument to the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId` 메서드의 두 번째 인자로 불리언 값을 넘겨 해당 인증 세션에 "로그인 상태 유지" 기능을 원하는지 지정할 수 있습니다. 즉, 사용자가 애플리케이션에서 직접 로그아웃할 때까지 세션이 무기한 인증 상태로 유지됩니다.

```
Auth::loginUsingId(1, $remember = true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate a User Once -->
#### Authenticate a User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method: -->
`once` 메서드를 사용하면 세션이나 쿠키 없이 단 한 번의 요청에 대해서만 인증할 수 있습니다.

```
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/10.x/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 별도의 로그인 페이지 구현 없이도 간단히 인증 기능을 제공합니다. 먼저, 라우트에 `auth.basic` [middleware](/docs/10.x/middleware)를 추가하면 됩니다. `auth.basic` 미들웨어는 Laravel 프레임워크에 기본 포함되어 있으므로 별도 등록 없이 바로 사용할 수 있습니다.

```
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
미들웨어를 라우트에 추가하면, 브라우저에서 해당 라우트에 접근할 때 즉시 인증을 요구하는 프롬프트가 나타납니다. 기본적으로 `auth.basic` 미들웨어는 `users` 테이블의 `email` 컬럼을 사용자명으로 사용합니다.

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note on FastCGI -->
#### A Note on FastCGI

<!-- If you are using PHP FastCGI and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
Laravel을 PHP FastCGI 및 Apache로 서비스하는 경우 HTTP 기본 인증이 올바로 동작하지 않을 수 있습니다. 이럴 때는 `.htaccess` 파일에 아래 내용을 추가하세요.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/10.x/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
세션에 사용자 식별 쿠키를 저장하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 주로 API 접근 인증에 유용합니다. 이를 위해서는 [define a middleware](/docs/10.x/middleware) 후, 내부에서 `onceBasic` 메서드를 호출하면 됩니다. `onceBasic` 메서드가 응답을 반환하지 않으면 요청이 어플리케이션에 계속 전달됩니다.

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
그 다음, 해당 미들웨어를 라우트에 적용하세요.

```
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
사용자를 수동으로 로그아웃시키려면 `Auth` 파사드의 `logout` 메서드를 사용하세요. 이 메서드는 현재 세션에서 인증 정보를 제거하여, 이후 요청엔 더 이상 인증이 유효하지 않게 만듭니다.

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/10.x/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
`logout` 메서드를 호출하는 것과 더불어, 사용자의 세션을 무효화하고 [CSRF token](/docs/10.x/csrf)을 재생성하는 것이 좋습니다. 사용자를 로그아웃한 뒤에는 보통 애플리케이션의 루트로 리다이렉트합니다.

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
Laravel은 다른 기기에서 유지 중인 사용자의 세션을 "로그아웃"시키는 기능도 제공합니다. 이 기능은 주로 사용자가 비밀번호를 변경할 때, 본인 기기를 제외한 모든 기기의 인증 세션을 무효화하고 싶을 때 사용합니다.

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is included on the routes that should receive session authentication. Typically, you should place this middleware on a route group definition so that it can be applied to the majority of your application's routes. By default, the `AuthenticateSession` middleware may be attached to a route using the `auth.session` route middleware alias as defined in your application's HTTP kernel: -->
시작하기 전에, 먼저 세션 인증을 적용할 라우트에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 포함되어 있는지 확인해야 합니다. 일반적으로 애플리케이션의 대부분 라우트에 적용할 수 있도록 라우트 그룹 정의에 이 미들웨어를 등록합니다. 기본적으로 `AuthenticateSession` 미들웨어는 애플리케이션의 HTTP 커널에 정의된 `auth.session` 라우트 미들웨어 alias를 사용해 라우트에 적용할 수 있습니다.

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
그 후, `Auth` 파사드의 `logoutOtherDevices` 메서드를 사용하세요. 사용자의 현재 비밀번호를 받아야 하므로, 별도의 입력 폼에서 비밀번호를 받고 전달해야 합니다.

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices`를 호출하면, 사용자의 나머지 세션이 전부 무효화되며, 로그인된 모든 가드에서 "로그아웃" 됩니다.

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
앱을 개발하다 보면, 사용자로 하여금 특정 액션 전이나 민감한 영역 진입 전 비밀번호를 한 번 더 확인하도록 해야 할 때가 있습니다. Laravel은 이를 쉽게 구현할 수 있는 미들웨어를 내장하고 있습니다. 이 기능을 적용하려면, 비밀번호 확인 폼을 보여주는 라우트와, 비밀번호 일치 여부를 확인해 사용자를 리다이렉트하는 라우트가 필요합니다.

> [!NOTE]
> 지금부터 소개하는 기능을 직접 구현하지 않고도, [Laravel application starter kits](/docs/10.x/starter-kits)에는 이미 이 기능이 내장되어 있습니다!

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
비밀번호를 한 번 확인한 뒤에는 3시간 동안 같은 요청이 발생해도 다시 묻지 않습니다. 이 재확인까지의 시간은 앱의 `config/auth.php` 설정 파일에서 `password_timeout` 값을 변경하여 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
먼저, 사용자의 비밀번호 확인을 요구하는 뷰를 반환하는 라우트를 만듭니다.

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
이 라우트의 뷰에는 `password` 필드가 포함된 폼이 있어야 하며, 사용자가 민감한 영역에 진입하기 전 비밀번호를 다시 확인해야 한다는 내용을 안내해주면 좋습니다.

<a name="confirming-the-password"></a>
<!-- #### Confirming the Password -->
#### Confirming the Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
그 다음, "비밀번호 확인" 폼에서 제출된 요청을 처리할 라우트를 정의합니다. 이 라우트가 비밀번호 검증 및 목적지 리다이렉트를 모두 담당합니다.

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
조금 더 자세히 살펴보면, 먼저 요청에서 전달된 `password` 값이 인증된 사용자 계정의 비밀번호와 일치하는지 확인합니다. 비밀번호가 올바르면, Laravel 세션에 비밀번호를 확인한 사실을 알려주는 표시(`passwordConfirmed`)를 남깁니다. 이 메서드는 사용자의 세션에 마지막 비밀번호 확인 시각을 기록하여, 다음 검증 시 활용하게 합니다. 이후, 사용자를 의도된 목적지로 리다이렉트합니다.

<a name="password-confirmation-protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/10.x/routing#named-routes): -->
최근에 비밀번호 확인이 수행된 사용자만 접근할 수 있도록 하고 싶은 라우트에는 반드시 `password.confirm` 미들웨어를 적용해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 인증이 필요한 라우트 접근 시 그 목적지를 세션에 저장하고, 비밀번호 재확인 뷰(`password.confirm` [named route](/docs/10.x/routing#named-routes))로 리다이렉트합니다.

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

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/10.x/providers). Since Laravel already ships with an `AuthServiceProvider`, we can place the code in that provider: -->
`Auth` 파사드의 `extend` 메서드를 사용해 자신만의 인증 가드(guard)를 만들 수도 있습니다. `extend` 메서드 호출은 [service provider](/docs/10.x/providers)에서 작성해야 합니다. Laravel에는 이미 `AuthServiceProvider`가 있으니 그곳에 코드를 추가하면 됩니다.

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * Register any application authentication / authorization services.
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
위 예시에서처럼, `extend`에 넘기는 콜백은 반드시 `Illuminate\Contracts\Auth\Guard` 인터페이스를 구현한 객체를 반환해야 합니다. 이 인터페이스의 메서드들을 구현해 커스텀 가드를 구성할 수 있습니다. 커스텀 가드가 준비되면, `auth.php` 설정 파일의 `guards` 항목에서 아래처럼 지정할 수 있습니다.

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
HTTP 요청 기반 커스텀 인증 시스템을 가장 빠르게 만드는 방법은 `Auth::viaRequest` 메서드를 활용하는 것입니다. 이 메서드를 사용하면 클로저 하나만으로 인증 프로세스를 정의할 수 있습니다.

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your `AuthServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
`AuthServiceProvider`의 `boot` 메서드에서 `Auth::viaRequest` 메서드를 호출하세요. `viaRequest` 메서드의 첫 번째 인자는 인증 드라이버 이름이며, 커스텀 가드를 설명하는 임의의 문자열이면 됩니다. 두 번째 인자는 들어오는 HTTP 요청을 받아 사용자 인스턴스를 반환하거나, 인증에 실패하면 `null`을 반환하는 클로저입니다.

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Register any application authentication / authorization services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

<!-- Once your custom authentication driver has been defined, you may configure it as a driver within the `guards` configuration of your `auth.php` configuration file: -->
커스텀 인증 드라이버를 정의했다면, 다음과 같이 `auth.php` 설정 파일의 `guards` 항목에 드라이버명을 지정하여 사용할 수 있습니다.

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<!-- Finally, you may reference the guard when assigning the authentication middleware to a route: -->
그리고 해당 가드를 라우트 미들웨어로도 지정 가능합니다.

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
관계형 데이터베이스가 아닌 다른 방식으로 사용자 정보를 보관한다면, 커스텀 사용자 프로바이더를 만들어 Laravel을 확장할 수 있습니다. `Auth` 파사드의 `provider` 메서드를 활용해 새로운 사용자 프로바이더를 등록하세요. 프로바이더 리졸버는 반드시 `Illuminate\Contracts\Auth\UserProvider` 를 구현한 객체를 반환해야 합니다.

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Auth;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * Register any application authentication / authorization services.
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
`provider` 메서드로 provider를 등록한 뒤에는 `auth.php` 설정 파일에서 새 user provider를 사용하도록 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 `provider`를 정의합니다.

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

<!-- Finally, you may reference this provider in your `guards` configuration: -->
마지막으로, 해당 프로바이더를 `guards` 설정에서 참조하세요.

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
`Illuminate\Contracts\Auth\UserProvider`는 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 MySQL, MongoDB 등 영구 저장소에서 불러오는 역할을 담당합니다. 이 두 인터페이스 덕분에, 사용자 데이터 저장 방식이나 구현 클래스가 달라도 Laravel 인증은 변함없이 동작할 수 있습니다.

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
`Illuminate\Contracts\Auth\UserProvider` 계약의 인터페이스는 다음과 같습니다.

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
이번에는 `UserProvider`에서 반환해야 하는 `Authenticatable` 인터페이스를 살펴보겠습니다. 사용자 프로바이더의 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드는 반드시 이 인터페이스를 구현한 인스턴스를 반환해야 합니다.

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
간단하게 설명하면,
- `getAuthIdentifierName`은 "기본키" 필드명을, `getAuthIdentifier`는 실제 PK 값을 반환합니다. MySQL에서는 사용자의 자동 증가 PK가 대표적입니다.
- `getAuthPassword`는 사용자 비밀번호(해시 값) 반환.

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes an `App\Models\User` class in the `app/Models` directory which implements this interface. -->
이 인터페이스 덕분에 인증 시스템은 어떤 ORM이나 저장소 추상화 계층을 사용하든 상관없이 모든 "user" 클래스와 연동할 수 있습니다. Laravel은 기본으로 이 인터페이스를 구현한 `App\Models\User` 클래스를 `app/Models` 디렉터리에 포함합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/10.x/events) during the authentication process. You may attach listeners to these events in your `EventServiceProvider`: -->
Laravel은 인증 프로세스 도중 여러 [events](/docs/10.x/events)를 발생시킵니다. `EventServiceProvider`에서 이러한 이벤트에 리스너를 연결할 수 있습니다.

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
