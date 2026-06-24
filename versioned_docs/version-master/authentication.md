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
<!-- - [Social Authentication](/docs/master/socialite) -->
- [Social Authentication](/docs/master/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
많은 웹 애플리케이션은 사용자가 애플리케이션에 인증하고 "로그인"할 수 있는 기능을 제공합니다. 하지만 이 기능을 직접 구현하는 일은 복잡할 뿐 아니라 보안상 위험도 따를 수 있습니다. Laravel은 인증 기능을 빠르고, 안전하고, 간단하게 구현할 수 있도록 필요한 도구를 제공합니다.

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel의 인증 기능은 크게 "guard"와 "provider"로 구성됩니다. guard는 각 요청에서 사용자를 어떻게 인증할지 정의합니다. 예를 들어 Laravel에는 세션 저장소와 쿠키로 상태를 유지하는 `session` guard가 기본 제공됩니다.

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/master/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
provider는 영구 저장소에서 사용자를 어떻게 조회할지 정의합니다. Laravel은 [Eloquent](/docs/master/eloquent)와 데이터베이스 쿼리 빌더를 사용한 사용자 조회를 지원하며, 필요하다면 애플리케이션에 맞는 provider를 추가로 정의할 수도 있습니다.

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
애플리케이션의 인증 구성 파일은 `config/auth.php`에 있습니다. 이 파일에는 Laravel 인증 서비스의 동작을 조정하기 위한 잘 문서화된 몇 가지 옵션이 포함되어 있습니다.

> [!NOTE]
> guard와 provider를 "역할(role)"이나 "권한(permission)"과 혼동하면 안 됩니다. 권한을 기준으로 사용자 동작을 제어하는 방법은 [authorization](/docs/master/authorization) 문서를 참고하세요.

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/master/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
빠르게 시작하고 싶다면 새 Laravel 애플리케이션에 [Laravel application starter kit](/docs/master/starter-kits)를 설치하세요. 데이터베이스 마이그레이션을 실행한 뒤 브라우저에서 `/register` 또는 애플리케이션에 연결된 다른 URL로 이동하면 됩니다. 스타터 키트가 전체 인증 시스템의 기본 구조를 자동으로 준비해 줍니다.

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing a [starter kit](/docs/master/starter-kits) can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since the Laravel starter kits contain authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**최종 Laravel 애플리케이션에서 스타터 키트를 사용하지 않더라도 [starter kit](/docs/master/starter-kits)를 한 번 설치해 보면 실제 Laravel 프로젝트에서 인증 기능이 어떻게 구성되는지 배우는 데 큰 도움이 됩니다.** Laravel 스타터 키트에는 인증용 컨트롤러, 라우트, 뷰가 포함되어 있으므로 관련 파일의 코드를 살펴보면 Laravel의 인증 기능이 어떻게 구현되는지 이해할 수 있습니다.

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/master/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. -->
기본적으로 Laravel에는 `app/Models` 디렉터리에 `App\Models\User` [Eloquent model](/docs/master/eloquent)가 포함되어 있습니다. 이 모델은 기본 Eloquent 인증 드라이버와 함께 사용될 수 있습니다.

<!-- If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. If your application is using MongoDB, check out MongoDB's official [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/). -->
애플리케이션이 Eloquent를 사용하지 않는 경우 Laravel 쿼리 빌더를 사용하는 `database` 인증 provider를 사용할 수 있습니다. 애플리케이션이 MongoDB를 사용하는 경우 MongoDB의 공식 [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/)를 확인하세요.

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` 모델에 대한 데이터베이스 스키마를 빌드할 때 비밀번호 열 길이가 60자 이상인지 확인하세요. 물론 새로운 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션은 이미 이 길이를 초과하는 열을 생성합니다.

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
또한 `users`(또는 이에 상응하는) 테이블에 100자의 null 허용 문자열 `remember_token` 열이 포함되어 있는지 확인해야 합니다. 이 열은 애플리케이션에 로그인할 때 "기억하기" 옵션을 선택한 사용자를 위한 토큰을 저장하는 데 사용됩니다. 다시 말하지만, 새 Laravel 애플리케이션에 포함된 기본 `users` 테이블 마이그레이션에는 이미 이 열이 포함되어 있습니다.

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel은 인증과 관련된 여러 패키지를 제공합니다. 계속하기 전에 Laravel의 전반적인 인증 생태계를 살펴보고 각 패키지가 어떤 목적에 맞는지 정리해 보겠습니다.

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/master/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
먼저 인증 작동 방식을 고려하세요. 웹 브라우저를 사용할 때 사용자는 로그인 양식을 통해 사용자 이름과 비밀번호를 제공합니다. 이러한 자격 증명이 올바른 경우 애플리케이션은 인증된 사용자에 대한 정보를 사용자의 [session](/docs/master/session)에 저장합니다. 브라우저에 발행된 쿠키에는 세션 ID가 포함되어 있어 애플리케이션에 대한 후속 요청이 사용자를 올바른 세션과 연결할 수 있습니다. 세션 쿠키가 수신된 후 애플리케이션은 세션 ID를 기반으로 세션 데이터를 검색하고 인증 정보가 세션에 저장되었음을 확인하며 사용자를 "인증된" 것으로 간주합니다.

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
원격 서비스가 API에 액세스하기 위해 인증해야 하는 경우 웹 브라우저가 없기 때문에 일반적으로 쿠키가 인증에 사용되지 않습니다. 대신 원격 서비스는 각 요청마다 API 토큰을 API로 보냅니다. 애플리케이션은 유효한 API 토큰 테이블에 대해 들어오는 토큰의 유효성을 검사하고 해당 API 토큰과 연결된 사용자가 수행하는 요청을 "인증"할 수 있습니다.

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel에는 보통 `Auth`와 `Session` 파사드로 접근하는 내장 인증 및 세션 서비스가 포함되어 있습니다. 이 기능은 웹 브라우저에서 시작된 요청에 대해 쿠키 기반 인증을 제공합니다. 이를 통해 사용자의 자격 증명을 검증하고 사용자를 인증할 수 있습니다. 또한 필요한 인증 데이터를 자동으로 사용자 세션에 저장하고 세션 쿠키도 발급합니다. 이러한 서비스를 사용하는 방법은 이 문서 전체에서 설명합니다.

<!-- **Application Starter Kits** -->
**애플리케이션 스타터 키트**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free starter kits](/docs/master/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. -->
이 문서에서 설명하는 것처럼 이러한 인증 서비스와 직접 상호작용해 애플리케이션만의 인증 계층을 구축할 수도 있습니다. 다만 더 빠르게 시작할 수 있도록 전체 인증 계층을 현대적인 형태로 미리 구성해 주는 [free starter kits](/docs/master/starter-kits)도 제공됩니다.

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/master/passport) and [Sanctum](/docs/master/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel은 API 토큰을 관리하고 API 토큰으로 들어오는 요청을 인증하는 데 도움이 되는 두 가지 선택적 패키지, [Passport](/docs/master/passport)와 [Sanctum](/docs/master/sanctum)을 제공합니다. 이 라이브러리들과 Laravel의 내장 쿠키 기반 인증 라이브러리는 서로 배타적이지 않습니다. 이 라이브러리들은 주로 API 토큰 인증에 초점을 맞추고, 내장 인증 서비스는 쿠키 기반 브라우저 인증에 초점을 맞춥니다. 많은 애플리케이션이 Laravel의 내장 쿠키 기반 인증 서비스와 Laravel의 API 인증 패키지 중 하나를 함께 사용합니다.

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport는 여러 종류의 토큰을 발급할 수 있는 다양한 OAuth2 "grant type"을 제공하는 OAuth2 인증 패키지입니다. 전반적으로 API 인증에 적합한 강력하고 복잡한 패키지지만, 대부분의 애플리케이션은 OAuth2 사양이 제공하는 복잡한 기능 전체를 필요로 하지 않습니다. 그래서 사용자와 개발자 모두에게 다소 혼란을 줄 수 있습니다. 또한 역사적으로 개발자들은 Passport 같은 OAuth2 솔루션으로 SPA나 모바일 애플리케이션을 어떻게 인증해야 하는지 자주 헷갈려 했습니다.

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/master/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2의 복잡성과 그로 인한 개발자 혼란에 대응하기 위해, 우리는 웹 브라우저에서 오는 자사 웹 요청과 토큰 기반 API 요청을 모두 처리할 수 있는 더 단순하고 효율적인 인증 패키지를 만들었습니다. 그 결과가 [Laravel Sanctum](/docs/master/sanctum)입니다. Sanctum은 API와 함께 자사 웹 UI를 제공하는 애플리케이션, 백엔드 Laravel 애플리케이션과 별도로 존재하는 SPA, 그리고 모바일 클라이언트를 제공하는 애플리케이션에서 우선적으로 고려할 만한 인증 패키지입니다.

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/master/sanctum#how-it-works) documentation. -->
Laravel Sanctum은 애플리케이션의 전체 인증 과정을 관리할 수 있는 하이브리드 웹/API 인증 패키지입니다. Sanctum 기반 애플리케이션이 요청을 받으면, 먼저 해당 요청에 인증된 세션을 가리키는 세션 쿠키가 포함되어 있는지 확인합니다. 이를 위해 Sanctum은 앞서 설명한 Laravel의 내장 인증 서비스를 호출합니다. 요청이 세션 쿠키로 인증되지 않았다면, Sanctum은 API 토큰이 포함되어 있는지 검사합니다. API 토큰이 있으면 그 토큰으로 요청을 인증합니다. 이 과정에 대한 자세한 내용은 Sanctum의 ["how it works"](/docs/master/sanctum#how-it-works) 문서를 참고하세요.

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary and Choosing Your Stack -->
#### Summary and Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
요약하면, 브라우저를 사용하여 애플리케이션에 액세스하고 모놀리식 Laravel 애플리케이션을 구축하는 경우 애플리케이션은 Laravel의 내장 인증 서비스를 사용하게 됩니다.

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/master/passport) or [Sanctum](/docs/master/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
다음으로, 애플리케이션이 제3자가 사용할 API를 제공하는 경우 [Passport](/docs/master/passport) 또는 [Sanctum](/docs/master/sanctum) 중에서 선택하여 애플리케이션에 API 토큰 인증을 제공합니다. 일반적으로 Sanctum는 "범위" 또는 "능력" 지원을 포함하여 API 인증, SPA 인증 및 모바일 인증을 위한 간단하고 완전한 솔루션이므로 가능한 경우 선호되어야 합니다.

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/master/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/master/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
Laravel 백엔드로 구동되는 단일 페이지 애플리케이션(SPA)을 구축하는 경우에는 [Laravel Sanctum](/docs/master/sanctum)을 사용하는 것이 좋습니다. Sanctum을 사용할 때는 [manually implement your own backend authentication routes](#authenticating-users)하거나, 회원가입, 비밀번호 재설정, 이메일 인증 같은 기능을 위한 라우트와 컨트롤러를 제공하는 헤드리스 인증 백엔드 서비스인 [Laravel Fortify](/docs/master/fortify)를 활용할 수 있습니다.

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
애플리케이션에 OAuth2 사양에서 제공하는 모든 기능이 절대적으로 필요한 경우 Passport를 선택할 수 있습니다.

<!-- And, if you would like to get started quickly, we are pleased to recommend [our application starter kits](/docs/master/starter-kits) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services. -->
빠르게 시작하고 싶다면, Laravel이 권장하는 내장 인증 스택을 이미 적용한 새 애플리케이션을 시작하는 방법으로 [our application starter kits](/docs/master/starter-kits)를 추천합니다.

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!WARNING]
> 문서의 이 부분에서는 빠르게 시작할 수 있도록 UI scaffolding이 포함된 [Laravel application starter kits](/docs/master/starter-kits)로 사용자를 인증하는 방법을 설명합니다. Laravel의 인증 시스템과 직접 통합하려면 [manually authenticating users](#authenticating-users) 문서를 참고하세요.

<a name="install-a-starter-kit"></a>
<!-- ### Install a Starter Kit -->
### Install a Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/master/starter-kits). Our starter kits offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
먼저 [install a Laravel application starter kit](/docs/master/starter-kits)해야 합니다. 당사의 스타터 키트는 새로운 Laravel 애플리케이션에 인증을 통합하기 위한 아름답게 디자인된 시작점을 제공합니다.

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving the Authenticated User -->
### Retrieving the Authenticated User

<!-- After creating an application from a starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
스타터 킷에서 애플리케이션을 작성하고 사용자가 애플리케이션에 등록하고 인증할 수 있도록 허용한 후에는 현재 인증된 사용자와 상호작용해야 하는 경우가 많습니다. 들어오는 요청을 처리하는 동안 `Auth` 파사드의 `user` 메서드를 통해 인증된 사용자에 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
또는 사용자가 인증되면 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 액세스할 수 있습니다. 타입힌트 클래스가 컨트롤러 메서드에 자동으로 삽입된다는 점을 기억하세요. `Illuminate\Http\Request` 객체를 타입힌트하면 요청의 `user` 메서드를 통해 애플리케이션의 모든 컨트롤러 메서드에서 인증된 사용자에 편리하게 액세스할 수 있습니다.

```php
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
들어오는 HTTP 요청을 하는 사용자가 인증되었는지 확인하려면 `Auth` 파사드의 `check` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 인증되면 `true`를 반환합니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` 메서드를 사용하여 사용자가 인증되었는지 확인할 수 있더라도 일반적으로 특정 라우트 / 컨트롤러에 대한 사용자 액세스를 허용하기 전에 미들웨어를 사용하여 사용자가 인증되었는지 확인합니다. 이에 대해 자세히 알아보려면 [protecting routes](/docs/master/authentication#protecting-routes) 문서를 확인하세요.

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/master/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which is a [middleware alias](/docs/master/middleware#middleware-aliases) for the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already aliased internally by Laravel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/master/middleware)는 인증된 사용자만 특정 라우트에 액세스하도록 허용하는 데 사용할 수 있습니다. Laravel은 `Illuminate\Auth\Middleware\Authenticate` 클래스의 [middleware alias](/docs/master/middleware#middleware-aliases)인 `auth` 미들웨어를 기본 제공합니다. 이 미들웨어는 이미 Laravel에 의해 내부적으로 별칭이 지정되어 있으므로 미들웨어를 라우트 정의에 연결하기만 하면 됩니다.

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/master/routing#named-routes). You may modify this behavior using the `redirectGuestsTo` method within your application's `bootstrap/app.php` file: -->
`auth` 미들웨어가 인증되지 않은 사용자를 감지하면 사용자를 `login` [named route](/docs/master/routing#named-routes)로 리디렉션합니다. 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드를 사용하여 이 동작을 수정할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="redirecting-authenticated-users"></a>
<!-- #### Redirecting Authenticated Users -->
#### Redirecting Authenticated Users

<!-- When the `guest` middleware detects an authenticated user, it will redirect the user to the `dashboard` or `home` named route. You may modify this behavior using the `redirectUsersTo` method within your application's `bootstrap/app.php` file: -->
`guest` 미들웨어가 인증된 사용자를 감지하면 사용자를 `dashboard` 또는 `home` 이름의 라우트로 리디렉션합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `redirectUsersTo` 메서드를 사용하면 이 동작을 변경할 수 있습니다.

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```

<a name="specifying-a-guard"></a>
<!-- #### Specifying a Guard -->
#### Specifying a Guard

<!-- When attaching the `auth` middleware to a route, you may also specify which "guard" should be used to authenticate the user. The guard specified should correspond to one of the keys in the `guards` array of your `auth.php` configuration file: -->
`auth` 미들웨어를 라우트에 연결할 때 사용자를 인증하는 데 사용해야 하는 "가드"를 지정할 수도 있습니다. 지정된 가드는 `auth.php` 구성 파일의 `guards` 배열에 있는 키 중 하나와 일치해야 합니다.

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using one of our [application starter kits](/docs/master/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
[application starter kits](/docs/master/starter-kits) 중 하나를 사용하는 경우 로그인 시도에 속도 제한이 자동으로 적용됩니다. 기본적으로 사용자는 여러 번 시도한 후에도 올바른 자격 증명을 제공하지 못하면 1분 동안 로그인할 수 없습니다. 제한은 사용자의 사용자 이름/이메일 주소 및 IP 주소에 따라 고유합니다.

> [!NOTE]
> 애플리케이션에서 다른 라우트의 속도를 제한하려면 [rate limiting documentation](/docs/master/routing#rate-limiting)를 확인하세요.

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/master/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
Laravel의 [application starter kits](/docs/master/starter-kits)에 포함된 인증 scaffolding을 반드시 사용할 필요는 없습니다. 이를 사용하지 않기로 했다면 Laravel의 인증 클래스를 직접 사용해 사용자 인증을 관리하면 됩니다. 생각보다 어렵지 않습니다.

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/master/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/master/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
Laravel의 인증 서비스는 `Auth` [facade](/docs/master/facades)를 통해 사용하므로, 먼저 클래스 상단에서 `Auth` 파사드를 가져와야 합니다. 다음으로 `attempt` 메서드를 살펴보겠습니다. `attempt` 메서드는 보통 애플리케이션의 로그인 폼에서 들어온 인증 시도를 처리할 때 사용합니다. 인증에 성공했다면 [session](https://en.wikipedia.org/wiki/Session_fixation)을 방지하기 위해 사용자의 [session fixation](/docs/master/session)을 다시 생성해야 합니다.

```php
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
`attempt` 메서드는 키/값 쌍의 배열을 첫 번째 인수로 허용합니다. 배열의 값은 데이터베이스 테이블에서 사용자를 찾는 데 사용됩니다. 따라서 위의 예에서는 `email` 열의 값으로 사용자를 검색합니다. 사용자가 발견되면 데이터베이스에 저장된 해시된 비밀번호는 배열을 통해 메서드에 전달된 `password` 값과 비교됩니다. 들어오는 요청의 `password` 값을 해시하면 안 됩니다. 프레임워크가 값을 데이터베이스의 해시된 비밀번호와 비교하기 전에 자동으로 해시하기 때문입니다. 두 개의 해시된 비밀번호가 일치하면 사용자에 대해 인증된 세션이 시작됩니다.

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
Laravel의 인증 서비스는 인증 guard의 "provider" 설정을 기준으로 데이터베이스에서 사용자를 조회한다는 점을 기억하세요. 기본 `config/auth.php` 설정 파일에는 Eloquent user provider가 지정되어 있으며, 사용자를 조회할 때 `App\Models\User` 모델을 사용합니다. 애플리케이션 요구 사항에 따라 이 값은 변경할 수 있습니다.

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
인증이 성공하면 `attempt` 메서드는 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
Laravel의 리디렉터가 제공하는 `intended` 메서드는 인증 미들웨어에 의해 차단되기 전에 액세스를 시도했던 URL로 사용자를 리디렉션합니다. 의도한 대상을 사용할 수 없는 경우 대체 URI가 이 메서드에 제공될 수 있습니다.

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
원하는 경우 사용자의 이메일 및 비밀번호 외에 추가 쿼리 조건을 인증 쿼리에 추가할 수도 있습니다. 이를 달성하려면 `attempt` 메서드에 전달된 배열에 쿼리 조건을 추가하기만 하면 됩니다. 예를 들어, 사용자가 "활성"으로 표시되어 있는지 확인할 수 있습니다.

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

<!-- For complex query conditions, you may provide a closure in your array of credentials. This closure will be invoked with the query instance, allowing you to customize the query based on your application's needs: -->
복잡한 쿼리 조건의 경우 자격 증명 배열에 클로저를 제공할 수 있습니다. 이 클로저는 쿼리 인스턴스와 함께 호출되므로 애플리케이션의 요구 사항에 따라 쿼리를 사용자 지정할 수 있습니다.

```php
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
> 이 예에서 `email`는 필수 옵션이 아니며 단지 예로서 사용됩니다. 데이터베이스 테이블의 "사용자 이름"에 해당하는 열 이름을 사용해야 합니다.

<!-- The `attemptWhen` method, which receives a closure as its second argument, may be used to perform more extensive inspection of the potential user before actually authenticating the user. The closure receives the potential user and should return `true` or `false` to indicate if the user may be authenticated: -->
두 번째 인수로 클로저를 수신하는 `attemptWhen` 메서드는 실제로 사용자를 인증하기 전에 잠재적인 사용자에 대한 보다 광범위한 검사를 수행하는 데 사용될 수 있습니다. 클로저는 잠재적인 사용자를 수신하고 사용자가 인증될 수 있는지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다.

```php
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
`Auth` 파사드의 `guard` 메서드를 통해, 사용자를 인증할 때 어떤 가드 인스턴스를 활용하고 싶은지 지정할 수 있습니다. 이를 통해 완전히 별도의 인증 가능한 모델 또는 사용자 테이블을 사용하여 애플리케이션의 개별 부분에 대한 인증을 관리할 수 있습니다.

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard` 메서드에 전달된 가드 이름은 `auth.php` 구성 파일에 구성된 가드 중 하나와 일치해야 합니다.

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
많은 웹 애플리케이션은 로그인 양식에 "기억하기" 확인란을 제공합니다. 애플리케이션에 "기억하기" 기능을 제공하려면 부울 값을 `attempt` 메서드의 두 번째 인수로 전달할 수 있습니다.

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
이 값이 `true`이면 Laravel은 사용자의 인증 상태를 무기한 유지하거나 수동으로 로그아웃할 때까지 유지합니다. `users` 테이블에는 "기억하기" 토큰을 저장하는 데 사용되는 문자열 `remember_token` 열이 포함되어야 합니다. 새로운 Laravel 애플리케이션에 포함된 `users` 테이블 마이그레이션에는 이미 다음 열이 포함되어 있습니다.

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<!-- If your application offers "remember me" functionality, you may use the `viaRemember`  method to determine if the currently authenticated user was authenticated using the "remember me" cookie: -->
애플리케이션이 "기억하기" 기능을 제공하는 경우 `viaRemember` 메서드를 사용하여 현재 인증된 사용자가 "기억하기" 쿠키를 사용하여 인증되었는지 확인할 수 있습니다.

```php
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

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/master/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
기존 사용자 인스턴스를 현재 인증된 사용자로 설정해야 하는 경우 사용자 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달할 수 있습니다. 지정된 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/master/contracts)의 구현이어야 합니다. Laravel에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현합니다. 이 인증 방법은 사용자가 애플리케이션에 등록한 직후와 같이 유효한 사용자 인스턴스가 이미 있는 경우에 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` 메서드의 두 번째 인수로 부울 값을 전달할 수 있습니다. 이 값은 인증된 세션에 "기억하기" 기능이 필요한지 여부를 나타냅니다. 이는 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 인증된다는 것을 기억하세요.

```php
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
필요한 경우 `login` 메서드를 호출하기 전에 인증 가드를 지정할 수 있습니다.

```php
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate a User by ID -->
#### Authenticate a User by ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
데이터베이스 레코드의 기본 키를 사용하여 사용자를 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증하려는 사용자의 기본 키를 허용합니다.

```php
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value to the `remember` argument of the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId` 메서드의 `remember` 인수에 부울 값을 전달할 수 있습니다. 이 값은 인증된 세션에 "기억하기" 기능이 필요한지 여부를 나타냅니다. 이는 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 인증된다는 것을 기억하세요.

```php
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate a User Once -->
#### Authenticate a User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method, and the `Login` event will not be dispatched: -->
`once` 메서드를 사용하면 단일 요청에 한해 사용자를 인증할 수 있습니다. 이 메서드를 호출할 때는 세션이나 쿠키를 사용하지 않으며, `Login` 이벤트도 디스패치되지 않습니다.

```php
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/master/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication)은 전용 "로그인" 페이지를 설정하지 않고도 애플리케이션 사용자를 인증하는 빠른 방법을 제공합니다. 시작하려면 `auth.basic` [middleware](/docs/master/middleware)를 라우트에 연결하세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 포함되어 있으므로 정의할 필요가 없습니다.

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
미들웨어를 라우트에 연결하면, 브라우저로 해당 라우트에 접근할 때 자격 증명 입력 창이 자동으로 표시됩니다. 기본적으로 `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 컬럼을 사용자의 "사용자 이름"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note on FastCGI -->
#### A Note on FastCGI

<!-- If you are using [PHP FastCGI](https://www.php.net/manual/en/install.fpm.php) and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
[PHP FastCGI](https://www.php.net/manual/en/install.fpm.php) 및 Apache를 사용하여 Laravel 애플리케이션을 제공하는 경우 HTTP 기본 인증이 올바르게 작동하지 않을 수 있습니다. 이러한 문제를 해결하기 위해 애플리케이션의 `.htaccess` 파일에 다음 줄을 추가할 수 있습니다.

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/master/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
세션에 사용자 식별 쿠키를 저장하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 이 방식은 애플리케이션 API 요청을 HTTP 인증으로 처리하려는 경우에 특히 유용합니다. 이를 위해 `onceBasic` 메서드를 호출하는 [define a middleware](/docs/master/middleware)하세요. `onceBasic` 메서드가 응답을 반환하지 않으면 요청은 애플리케이션의 다음 처리 단계로 계속 전달됩니다.

```php
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
다음으로 미들웨어를 라우트에 연결합니다.

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
애플리케이션에서 사용자를 수동으로 로그아웃하려면 `Auth` 파사드가 제공하는 `logout` 메서드를 사용하면 됩니다. 그러면 이후 요청에서는 더 이상 인증된 사용자로 처리되지 않도록 세션에서 인증 정보가 제거됩니다.

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/master/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
`logout` 메서드를 호출하는 것 외에도 사용자 세션을 무효화하고 [CSRF token](/docs/master/csrf)을 다시 생성하는 것이 좋습니다. 사용자를 로그아웃한 후 일반적으로 사용자를 애플리케이션의 루트로 리디렉션합니다.

```php
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
Laravel은 현재 사용 중인 기기의 세션은 유지한 채, 다른 기기에서 활성 상태인 사용자 세션만 무효화하고 로그아웃시키는 기능도 제공합니다. 이 기능은 사용자가 비밀번호를 변경하거나 갱신할 때, 현재 기기에서는 계속 로그인 상태를 유지하면서 다른 기기의 세션만 끊고 싶을 때 주로 사용합니다.

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is included on the routes that should receive session authentication. Typically, you should place this middleware on a route group definition so that it can be applied to the majority of your application's routes. By default, the `AuthenticateSession` middleware may be attached to a route using the `auth.session` [middleware alias](/docs/master/middleware#middleware-aliases): -->
시작하기 전에 세션 인증이 필요한 라우트에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 포함되어 있는지 확인해야 합니다. 일반적으로는 이 미들웨어를 라우트 그룹에 배치해 애플리케이션의 여러 라우트에 한꺼번에 적용합니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [middleware alias](/docs/master/middleware#middleware-aliases)으로 라우트에 연결할 수 있습니다.

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
그다음 `Auth` 파사드가 제공하는 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드를 사용하려면 사용자가 현재 비밀번호를 다시 입력해 확인해야 하므로, 애플리케이션에서도 이를 받을 수 있는 입력 폼을 제공해야 합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices` 메서드가 호출되면 사용자의 다른 세션은 완전히 무효화됩니다. 즉, 이전에 인증된 모든 가드에서 "로그아웃"됩니다.

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
애플리케이션을 만들다 보면, 특정 작업을 수행하기 전에 또는 민감한 영역으로 이동시키기 전에 사용자에게 비밀번호를 다시 확인하도록 요구해야 할 때가 있습니다. Laravel은 이 과정을 쉽게 구현할 수 있도록 관련 미들웨어를 기본으로 제공합니다. 이 기능을 구현하려면 두 개의 라우트를 정의해야 합니다. 하나는 비밀번호 확인을 요청하는 뷰를 보여주는 라우트이고, 다른 하나는 입력한 비밀번호를 검증한 뒤 사용자를 원래 의도한 위치로 리디렉션하는 라우트입니다.

> [!NOTE]
> 다음 문서에서는 Laravel의 비밀번호 확인 기능과 직접 통합하는 방법을 설명합니다. 그러나 더 빨리 시작하고 싶다면 [Laravel application starter kits](/docs/master/starter-kits)에 이 기능에 대한 지원이 포함되어 있습니다!

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
비밀번호를 한 번 확인하면 이후 3시간 동안은 다시 비밀번호를 묻지 않습니다. 이 시간은 애플리케이션의 `config/auth.php` 설정 파일에서 `password_timeout` 값을 변경해 조정할 수 있습니다.

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
먼저, 사용자에게 비밀번호 확인을 요청하는 뷰를 표시하도록 라우트를 정의합니다.

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
예상할 수 있듯이, 이 라우트가 반환하는 뷰에는 `password` 필드를 포함한 폼이 있어야 합니다. 또한 사용자가 보호된 영역으로 들어가려는 중이므로 비밀번호 확인이 필요하다는 안내 문구를 뷰에 함께 표시하면 됩니다.

<a name="confirming-the-password"></a>
<!-- #### Confirming the Password -->
#### Confirming the Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
다음으로 "비밀번호 확인" 뷰의 폼 요청을 처리할 라우트를 정의합니다. 이 라우트는 비밀번호를 검증하고 사용자를 원래 의도한 위치로 리디렉션하는 역할을 합니다.

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

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
계속하기 전에 이 라우트가 하는 일을 조금 더 자세히 살펴보겠습니다. 먼저 요청의 `password` 필드 값이 현재 인증된 사용자의 비밀번호와 실제로 일치하는지 확인합니다. 비밀번호가 유효하면, 사용자가 비밀번호 확인을 마쳤다는 사실을 Laravel 세션에 기록해야 합니다. `passwordConfirmed` 메서드는 사용자가 마지막으로 비밀번호를 확인한 시점을 나타내는 타임스탬프를 세션에 저장합니다. 마지막으로 사용자를 원래 가려던 목적지로 리디렉션합니다.

<a name="password-confirmation-protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/master/routing#named-routes): -->
최근에 비밀번호를 확인한 사용자만 접근할 수 있어야 하는 라우트에는 `password.confirm` 미들웨어를 할당해야 합니다. 이 미들웨어는 Laravel 기본 설치에 포함되어 있으며, 사용자가 비밀번호를 확인한 뒤 원래 가려던 위치로 돌아갈 수 있도록 세션에 의도한 목적지를 자동으로 저장합니다. 목적지를 저장한 뒤에는 사용자를 `password.confirm` [named route](/docs/master/routing#named-routes)로 리디렉션합니다.

```php
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

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/master/providers). Since Laravel already ships with an `AppServiceProvider`, we can place the code in that provider: -->
`Auth` 파사드의 `extend` 메서드를 사용하면 직접 인증 guard를 정의할 수 있습니다. `extend` 메서드 호출은 [service provider](/docs/master/providers) 안에서 작성해야 합니다. Laravel은 기본으로 `AppServiceProvider`를 제공하므로 여기에 코드를 추가하면 됩니다.

```php
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
위 예제에서 보듯, `extend` 메서드에 전달하는 콜백은 `Illuminate\Contracts\Auth\Guard` 구현을 반환해야 합니다. 이 인터페이스에는 사용자 지정 guard를 만들 때 구현해야 할 메서드가 정의되어 있습니다. guard를 정의한 뒤에는 `auth.php` 설정 파일의 `guards` 설정에서 이를 참조할 수 있습니다.

```php
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
사용자 지정 HTTP 요청 기반 인증 시스템을 구현하는 가장 간단한 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 사용하면 하나의 클로저로 인증 과정을 빠르게 정의할 수 있습니다.

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your application's `AppServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
시작하려면 애플리케이션의 `AppServiceProvider` `boot` 메서드 안에서 `Auth::viaRequest` 메서드를 호출하세요. `viaRequest` 메서드의 첫 번째 인수는 인증 드라이버 이름이며, 사용자 지정 guard를 설명하는 임의의 문자열이면 됩니다. 두 번째 인수는 들어오는 HTTP 요청을 받아 사용자 인스턴스를 반환하는 클로저이며, 인증에 실패하면 `null`을 반환해야 합니다.

```php
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
사용자 지정 인증 드라이버를 정의한 뒤에는 `auth.php` 설정 파일의 `guards` 항목에서 해당 드라이버를 사용할 수 있습니다.

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<!-- Finally, you may reference the guard when assigning the authentication middleware to a route: -->
마지막으로 인증 미들웨어를 라우트에 적용할 때 이 guard를 참조하면 됩니다.

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
사용자 정보를 저장할 때 전통적인 관계형 데이터베이스를 사용하지 않는다면, 자체 인증 user provider를 사용하도록 Laravel을 확장해야 합니다. 사용자 지정 user provider를 정의하려면 `Auth` 파사드의 `provider` 메서드를 사용합니다. 이때 등록하는 콜백은 `Illuminate\Contracts\Auth\UserProvider` 구현을 반환해야 합니다.

```php
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
`provider` 메서드로 provider를 등록한 뒤에는 `auth.php` 설정 파일에서 새 user provider를 사용하도록 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 `provider`를 정의합니다.

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

<!-- Finally, you may reference this provider in your `guards` configuration: -->
마지막으로 `guards` 설정에서 이 provider를 참조하면 됩니다.

```php
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
`Illuminate\Contracts\Auth\UserProvider` 구현은 MySQL, MongoDB 같은 영구 저장소에서 `Illuminate\Contracts\Auth\Authenticatable` 구현을 가져오는 역할을 합니다. 이 두 인터페이스 덕분에 Laravel의 인증 메커니즘은 사용자 데이터가 어떻게 저장되는지, 인증된 사용자를 어떤 클래스가 표현하는지와 관계없이 일관되게 동작할 수 있습니다.

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
`Illuminate\Contracts\Auth\UserProvider` 계약을 살펴보겠습니다.

```php
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
`retrieveById` 메서드는 일반적으로 MySQL 데이터베이스의 자동 증가 ID처럼 사용자를 나타내는 키를 받습니다. 이 메서드는 해당 ID와 일치하는 `Authenticatable` 구현을 조회해 반환해야 합니다.

<!-- The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method. -->
`retrieveByToken` 메서드는 일반적으로 `remember_token` 같은 데이터베이스 컬럼에 저장된 고유한 `$identifier`와 "기억하기" `$token`을 사용해 사용자를 조회합니다. 앞선 메서드와 마찬가지로, 이 메서드도 일치하는 토큰 값을 가진 `Authenticatable` 구현을 반환해야 합니다.

<!-- The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out. -->
`updateRememberToken` 메서드는 `$user` 인스턴스의 `remember_token` 값을 새로운 `$token`으로 갱신합니다. "기억하기" 인증이 성공했거나 사용자가 로그아웃할 때는 새로운 토큰이 사용자에게 할당됩니다.

<!-- The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.** -->
`retrieveByCredentials` 메서드는 애플리케이션 인증 시 `Auth::attempt` 메서드에 전달된 자격 증명 배열을 받습니다. 이 메서드는 해당 자격 증명과 일치하는 사용자를 기본 영구 저장소에서 조회해야 합니다. 일반적으로는 `$credentials['username']` 값과 일치하는 "사용자 이름"을 기준으로 "where" 조건을 추가해 사용자 레코드를 찾습니다. 이 메서드는 `Authenticatable` 구현을 반환해야 합니다. **이 메서드에서 비밀번호 검증이나 인증 자체를 시도해서는 안 됩니다.**

<!-- The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid. -->
`validateCredentials` 메서드는 사용자를 인증하기 위해 주어진 `$user`와 `$credentials`를 비교해야 합니다. 예를 들어 이 메서드는 일반적으로 `Hash::check` 메서드를 사용해 `$user->getAuthPassword()` 값과 `$credentials['password']` 값을 비교합니다. 반환값은 비밀번호가 유효한지를 나타내는 `true` 또는 `false`여야 합니다.

<!-- The `rehashPasswordIfRequired` method should rehash the given `$user`'s password if required and supported. For example, this method will typically use the `Hash::needsRehash` method to determine if the `$credentials['password']` value needs to be rehashed. If the password needs to be rehashed, the method should use the `Hash::make` method to rehash the password and update the user's record in the underlying persistent storage. -->
`rehashPasswordIfRequired` 메서드는 필요하고 지원되는 경우 지정된 `$user`의 비밀번호를 다시 해시해야 합니다. 예를 들어 이 메서드는 일반적으로 `Hash::needsRehash` 메서드를 사용해 `$credentials['password']` 값을 다시 해시해야 하는지 판단합니다. 다시 해시가 필요하면 `Hash::make` 메서드로 비밀번호를 새로 해시하고, 기본 영구 저장소에 있는 사용자 레코드도 함께 갱신해야 합니다.

<a name="the-authenticatable-contract"></a>
<!-- ### The Authenticatable Contract -->
### The Authenticatable Contract

<!-- Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods: -->
이제 `UserProvider`의 각 메서드를 살펴봤으니 `Authenticatable` 계약을 보겠습니다. user provider는 `retrieveById`, `retrieveByToken`, `retrieveByCredentials` 메서드에서 이 인터페이스를 구현한 객체를 반환해야 합니다.

```php
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
이 인터페이스는 비교적 단순합니다. `getAuthIdentifierName` 메서드는 사용자의 "기본 키" 컬럼 이름을 반환해야 하고, `getAuthIdentifier` 메서드는 사용자의 "기본 키" 값을 반환해야 합니다. MySQL 백엔드를 사용한다면 대개 사용자 레코드에 할당된 자동 증가 기본 키가 여기에 해당합니다. `getAuthPasswordName` 메서드는 사용자 비밀번호 컬럼의 이름을 반환해야 하며, `getAuthPassword` 메서드는 해시된 비밀번호 값을 반환해야 합니다.

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes an `App\Models\User` class in the `app/Models` directory which implements this interface. -->
이 인터페이스를 사용하면 어떤 ORM이나 저장소 추상화 계층을 사용하든 인증 시스템이 모든 "사용자" 클래스에서 동작할 수 있습니다. 기본적으로 Laravel에는 `app/Models` 디렉터리에 이 인터페이스를 구현한 `App\Models\User` 클래스가 포함되어 있습니다.

<a name="automatic-password-rehashing"></a>
<!-- ## Automatic Password Rehashing -->
## Automatic Password Rehashing

<!-- Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via your application's `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable. -->
Laravel의 기본 비밀번호 해싱 알고리즘은 bcrypt입니다. bcrypt 해시의 "작업 요소"는 애플리케이션의 `config/hashing.php` 구성 파일 또는 `BCRYPT_ROUNDS` 환경 변수를 통해 조정할 수 있습니다.

<!-- Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will gracefully and automatically rehash user passwords as users authenticate with your application via Laravel's starter kits or when you [manually authenticate users](#authenticating-users) via the `attempt` method. -->
일반적으로 bcrypt 작업 계수는 CPU나 GPU의 처리 성능이 향상됨에 따라 시간이 지나면서 높여야 합니다. 애플리케이션의 bcrypt 작업 계수를 늘리면, 사용자가 Laravel 스타터 키트를 통해 로그인할 때나 `attempt` 메서드로 [manually authenticate users](#authenticating-users)할 때 Laravel이 사용자 비밀번호를 자동으로 다시 해시합니다.

<!-- Typically, automatic password rehashing should not disrupt your application; however, you may disable this behavior by publishing the `hashing` configuration file: -->
대부분의 경우 자동 비밀번호 재해싱이 애플리케이션 동작에 문제를 일으키지는 않습니다. 하지만 필요하다면 `hashing` 설정 파일을 게시한 뒤 이 동작을 비활성화할 수 있습니다.

```shell
php artisan config:publish hashing
```

<!-- Once the configuration file has been published, you may set the `rehash_on_login` configuration value to `false`: -->
구성 파일이 게시되면 `rehash_on_login` 구성 값을 `false`로 설정할 수 있습니다.

```php
'rehash_on_login' => false,
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/master/events) during the authentication process. You may [define listeners](/docs/master/events) for any of the following events: -->
Laravel은 인증 과정에서 다양한 [events](/docs/master/events)를 디스패치합니다. 다음 이벤트에 대해 [define listeners](/docs/master/events)할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트 이름 |
| --------------------------------- |
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
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

<!-- </div> -->
</div>
