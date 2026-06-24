<!-- # CSRF Protection -->
# CSRF Protection

- [Introduction](#csrf-introduction)
- [Preventing CSRF Requests](#preventing-csrf-requests)
    - [Excluding URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of an authenticated user. Thankfully, Laravel makes it easy to protect your application from [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) attacks. -->
크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 대신하여 무단 명령을 수행하는 악의적인 공격 방식 중 하나입니다. 다행히도, Laravel은 애플리케이션을 [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 쉽게 보호할 수 있도록 해줍니다.

<a name="csrf-explanation"></a>
<!-- #### An Explanation Of The Vulnerability -->
#### An Explanation Of The Vulnerability

<!-- In case you're not familiar with cross-site request forgeries, let's discuss an example of how this vulnerability can be exploited. Imagine your application has a `/user/email` route that accepts a `POST` request to change the authenticated user's email address. Most likely, this route expects an `email` input field to contain the email address the user would like to begin using. -->
크로스 사이트 요청 위조에 익숙하지 않은 분들을 위해, 이 취약점이 실제로 어떻게 악용될 수 있는지 예시로 설명하겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청용 `/user/email` 라우트가 있다고 가정해보겠습니다. 이 라우트는 대부분 사용자가 사용하고자 하는 이메일 주소를 입력하는 `email` 필드 값을 기대할 것입니다.

<!-- Without CSRF protection, a malicious website could create an HTML form that points to your application's `/user/email` route and submits the malicious user's own email address: -->
CSRF 보호가 없다면, 악의적인 웹사이트는 여러분의 애플리케이션 `/user/email` 라우트로 향하는 HTML 폼을 만들고, 공격자의 이메일 주소로 해당 폼을 제출할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

<!--  If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
 만약 이 악의적인 웹사이트가 페이지가 로드될 때 자동으로 폼을 전송하도록 만들어졌다면, 공격자는 단지 여러분 애플리케이션의 아무런 의심 없는 사용자를 자신의 사이트로 방문하게끔 유도하기만 하면 됩니다. 그러면 그 사용자의 이메일 주소가 여러분의 애플리케이션에서 공격자의 이메일로 변경되어 버립니다.

<!--  To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
 이 취약점을 막기 위해서는, 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 악의적인 애플리케이션은 알 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/9.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravel은 애플리케이션에서 관리하는 각 [user session](/docs/9.x/session)마다 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 요청을 보내고 있는지 확인하는 목적으로 사용됩니다. 이 토큰은 사용자의 세션에 저장되며, 세션이 새로 생성될 때마다 값이 변경되기 때문에, 악의적인 애플리케이션은 접근할 수 없습니다.

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
현재 세션의 CSRF 토큰은 요청의 세션 객체나 `csrf_token` 헬퍼 함수를 통해 확인할 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

<!-- Anytime you define a "POST", "PUT", "PATCH", or "DELETE" HTML form in your application, you should include a hidden CSRF `_token` field in the form so that the CSRF protection middleware can validate the request. For convenience, you may use the `@csrf` Blade directive to generate the hidden token input field: -->
애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" 방식의 HTML 폼을 정의할 때마다, CSRF `_token` 숨김 필드를 반드시 포함시켜야 CSRF 보호 미들웨어가 해당 요청을 정상적으로 검증할 수 있습니다. 이를 더 편리하게 처리하기 위해, `@csrf` Blade 지시어를 사용해서 숨겨진 토큰 입력 필드를 자동으로 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<!-- The `App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/9.x/middleware), which is included in the `web` middleware group by default, will automatically verify that the token in the request input matches the token stored in the session. When these two tokens match, we know that the authenticated user is the one initiating the request. -->
기본적으로 `web` 미들웨어 그룹에 포함되어 있는 `App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/9.x/middleware)는 요청 입력값의 토큰이 세션에 저장된 토큰과 일치하는지 자동으로 검사합니다. 이 두 값이 일치한다면, 그 요청이 인증된 사용자가 실제로 보낸 것임을 신뢰할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
<!-- ### CSRF Tokens & SPAs -->
### CSRF Tokens & SPAs

<!-- If you are building a SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/9.x/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities. -->
만약 Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 개발 중이라면, API 인증 및 CSRF 취약점 방지에 대한 자세한 내용은 [Laravel Sanctum documentation](/docs/9.x/sanctum)를 참고하시기 바랍니다.

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
특정 URI 경로에 대해 CSRF 보호를 적용하지 않아야 할 상황도 있습니다. 예를 들어, [Stripe](https://stripe.com)를 이용하여 결제를 처리하고, Stripe의 웹훅 시스템을 사용하는 경우라면 Stripe 웹훅 처리 라우트는 CSRF 보호 대상에서 반드시 제외해야 합니다. Stripe는 Laravel 라우트에 어떤 CSRF 토큰을 보내야 할지 알지 못하기 때문입니다.

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that the `App\Providers\RouteServiceProvider` applies to all routes in the `routes/web.php` file. However, you may also exclude the routes by adding their URIs to the `$except` property of the `VerifyCsrfToken` middleware: -->
일반적으로 이런 라우트들은 `routes/web.php` 파일에서 `App\Providers\RouteServiceProvider`가 자동으로 적용하는 `web` 미들웨어 그룹 **밖**에 두는 것이 좋습니다. 그 대신, 해당 라우트를 `VerifyCsrfToken` 미들웨어의 `$except` 속성에 URI를 추가하여 보호 대상에서 제외할 수도 있습니다:

```
<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    /**
     * The URIs that should be excluded from CSRF verification.
     *
     * @var array
     */
    protected $except = [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ];
}
```

> [!NOTE]
> 편의상, [running tests](/docs/9.x/testing)에는 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `App\Http\Middleware\VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
POST 파라미터로 CSRF 토큰을 확인하는 것 이외에도, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 함께 검사합니다. 예를 들어, 다음과 같이 HTML의 `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

<!-- Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology: -->
그런 다음, jQuery와 같은 라이브러리에게 모든 요청의 헤더에 이 토큰을 자동으로 추가하도록 지시할 수 있습니다. 이렇게 하면 기존 자바스크립트를 사용하는 AJAX 기반 애플리케이션에서도 아주 쉽게 CSRF 보호를 적용할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
<!-- ## X-XSRF-TOKEN -->
## X-XSRF-TOKEN

<!-- Laravel stores the current CSRF token in an encrypted `XSRF-TOKEN` cookie that is included with each response generated by the framework. You can use the cookie value to set the `X-XSRF-TOKEN` request header. -->
Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여, 프레임워크가 생성하는 모든 응답에 함께 전송합니다. 여러분은 이 쿠키 값을 읽어와서 `X-XSRF-TOKEN` 요청 헤더에 셋팅할 수 있습니다.

<!-- This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests. -->
이 쿠키는 주로 개발 편의를 위해 제공됩니다. 왜냐하면 Angluar, Axios와 같은 일부 자바스크립트 프레임워크 및 라이브러리는 같은 출처(same-origin) 요청에서 이 쿠키의 값을 자동으로 `X-XSRF-TOKEN` 헤더에 설정해주기 때문입니다.

> [!NOTE]
> 기본적으로, `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리가 `X-XSRF-TOKEN` 헤더를 자동으로 전송해줍니다.