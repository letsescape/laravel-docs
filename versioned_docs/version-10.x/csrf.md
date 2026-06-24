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
크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 가장하여 허가받지 않은 명령을 애플리케이션에 전달하는 악의적인 공격 방식 중 하나입니다. 다행히도 Laravel은 [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 애플리케이션을 쉽게 보호할 수 있도록 기능을 제공합니다.

<a name="csrf-explanation"></a>
<!-- #### An Explanation of the Vulnerability -->
#### An Explanation of the Vulnerability

<!-- In case you're not familiar with cross-site request forgeries, let's discuss an example of how this vulnerability can be exploited. Imagine your application has a `/user/email` route that accepts a `POST` request to change the authenticated user's email address. Most likely, this route expects an `email` input field to contain the email address the user would like to begin using. -->
CSRF가 무엇인지 익숙하지 않다면, 이 취약점이 실제로 어떻게 악용될 수 있는지 예시를 통해 설명드리겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `/user/email` 경로가 있다고 가정하겠습니다. 이 경로는 일반적으로 `POST` 요청을 받고, `email` 입력 필드에 변경할 이메일이 전달되는 방식을 사용합니다.

<!-- Without CSRF protection, a malicious website could create an HTML form that points to your application's `/user/email` route and submits the malicious user's own email address: -->
만약 CSRF 보호가 없다면, 악의적인 웹사이트는 여러분의 애플리케이션의 `/user/email` 경로로 요청을 보내도록 아래와 같이 HTML 폼을 만들 수 있습니다. 이 폼은 공격자의 이메일을 자동으로 제출하게 됩니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

<!--  If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
이처럼 악성 웹사이트가 페이지가 열리자마자 폼을 자동 제출하도록 하면, 여러분의 애플리케이션을 사용하는 사용자가 이 웹사이트에 접속하기만 하더라도 그 사용자의 이메일 주소가 공격자 의도대로 변경될 수 있습니다.

<!--  To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
이러한 취약점을 방지하려면, 들어오는 모든 `POST`, `PUT`, `PATCH`, 또는 `DELETE` 요청마다 공격자가 접근할 수 없는 비밀 세션 값을 반드시 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/10.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravel은 애플리케이션에서 관리되는 모든 [user session](/docs/10.x/session)에 대해 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 직접 요청을 보내고 있는지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며, 세션이 새로 생성될 때마다 토큰도 변경되기 때문에, 외부의 악성 애플리케이션에서는 이 값을 알 수 없습니다.

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
현재 세션의 CSRF 토큰은 요청의 세션을 통해서나, 또는 `csrf_token` 헬퍼 함수를 통해 가져올 수 있습니다:

```
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

<!-- Anytime you define a "POST", "PUT", "PATCH", or "DELETE" HTML form in your application, you should include a hidden CSRF `_token` field in the form so that the CSRF protection middleware can validate the request. For convenience, you may use the `@csrf` Blade directive to generate the hidden token input field: -->
애플리케이션에서 "POST", "PUT", "PATCH", 또는 "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼 안에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 합니다. 편리하게도, Blade의 `@csrf` 디렉티브를 사용하면 이 숨겨진 토큰 입력 필드를 쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<!-- The `App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/10.x/middleware), which is included in the `web` middleware group by default, will automatically verify that the token in the request input matches the token stored in the session. When these two tokens match, we know that the authenticated user is the one initiating the request. -->
`web` 미들웨어 그룹에 기본 포함되어 있는 `App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/10.x/middleware)는 요청 입력값의 토큰과 세션에 저장된 토큰이 일치하는지를 자동으로 확인합니다. 두 토큰이 일치하면, 해당 요청이 실제 인증된 사용자가 수행한 것임을 신뢰할 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
<!-- ### CSRF Tokens & SPAs -->
### CSRF Tokens & SPAs

<!-- If you are building a SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/10.x/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities. -->
Laravel을 API 백엔드로 사용하는 SPA(Single Page Application)를 개발하고 있다면, API 인증 및 CSRF 취약점 방지에 관한 자세한 내용은 [Laravel Sanctum documentation](/docs/10.x/sanctum)를 참고하시기 바랍니다.

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
경우에 따라 일부 URI를 CSRF 보호 대상에서 제외하고 싶을 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 통한 결제 처리를 위해 Stripe의 웹훅(Webhook) 시스템을 사용한다면, Stripe가 여러분의 경로로 CSRF 토큰을 보낼 수 없기 때문에 웹훅을 처리하는 라우트를 CSRF 보호에서 반드시 제외해야 합니다.

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that the `App\Providers\RouteServiceProvider` applies to all routes in the `routes/web.php` file. However, you may also exclude the routes by adding their URIs to the `$except` property of the `VerifyCsrfToken` middleware: -->
보통 이런 라우트는 `App\Providers\RouteServiceProvider`가 `routes/web.php`의 모든 라우트에 기본 적용하는 `web` 미들웨어 그룹 바깥에 배치하는 것이 좋습니다. 하지만, `VerifyCsrfToken` 미들웨어의 `$except` 속성에 해당 URI를 추가하는 방식으로도 제외할 수 있습니다:

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
> Laravel에서 [running tests](/docs/10.x/testing)을 할 때는 편의를 위해 모든 라우트에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `App\Http\Middleware\VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
POST 파라미터로 CSRF 토큰 값을 검사하는 것 외에도, `App\Http\Middleware\VerifyCsrfToken` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 함께 검사합니다. 예를 들어, HTML의 `meta` 태그에 토큰을 저장해 둘 수도 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

<!-- Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology: -->
이후 jQuery와 같은 라이브러리에서 모든 요청 헤더에 토큰값을 자동으로 추가하도록 설정할 수 있습니다. 이 방식은 레거시 JavaScript 기술로 구현된 AJAX 기반 애플리케이션에 간편한 CSRF 보호를 제공합니다:

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
Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하여 프레임워크가 생성하는 모든 응답에 포함시킵니다. 이 쿠키의 값을 읽어서 `X-XSRF-TOKEN` 요청 헤더에 넣어 사용할 수 있습니다.

<!-- This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests. -->
이 쿠키는 개발자 편의를 위해 제공되는 것이며, Angular, Axios와 같은 일부 JavaScript 프레임워크나 라이브러리가 동일 출처 요청(same-origin request)에 대해 쿠키 내 값을 자동으로 `X-XSRF-TOKEN` 헤더에 추가해 줍니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 `X-XSRF-TOKEN` 헤더를 자동으로 전송합니다.
