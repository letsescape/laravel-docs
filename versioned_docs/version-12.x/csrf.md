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
크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 가장해 무단 명령을 실행하는 악의적 공격 유형입니다. 다행히도, Laravel은 [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 애플리케이션을 간편하게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
<!-- #### An Explanation of the Vulnerability -->
#### An Explanation of the Vulnerability

<!-- In case you're not familiar with cross-site request forgeries, let's discuss an example of how this vulnerability can be exploited. Imagine your application has a `/user/email` route that accepts a `POST` request to change the authenticated user's email address. Most likely, this route expects an `email` input field to contain the email address the user would like to begin using. -->
크로스 사이트 요청 위조(CSRF)에 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 살펴보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보겠습니다. 이 라우트는 일반적으로 사용자가 변경하고 싶어하는 새 이메일 주소를 `email` 입력 필드로 받습니다.

<!-- Without CSRF protection, a malicious website could create an HTML form that points to your application's `/user/email` route and submits the malicious user's own email address: -->
만약 CSRF 보호 기능이 없다면, 악성 웹사이트가 여러분의 애플리케이션의 `/user/email` 라우트로 연결되는 HTML 폼을 만들고, 공격자의 이메일 주소를 입력값으로 제출할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

<!-- If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
만약 위와 같이 악성 웹사이트가 페이지가 로드될 때 폼을 자동으로 제출하도록 하면, 공격자는 아무것도 모르는 사용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 인증된 사용자의 이메일 주소가 공격자 소유의 이메일로 바뀔 수 있습니다.

<!-- To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
이런 취약점을 막기 위해서는, 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해, 외부 악성 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/12.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravel은 애플리케이션이 관리하는 활성 [user session](/docs/12.x/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내고 있는지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며 세션이 재생성될 때마다 변경되기 때문에, 악성 애플리케이션이 이 토큰에 접근할 수 없습니다.

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수로 얻을 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

<!-- Anytime you define a "POST", "PUT", "PATCH", or "DELETE" HTML form in your application, you should include a hidden CSRF `_token` field in the form so that the CSRF protection middleware can validate the request. For convenience, you may use the `@csrf` Blade directive to generate the hidden token input field: -->
애플리케이션에서 "POST", "PUT", "PATCH", "DELETE"와 같은 HTML 폼을 작성할 때마다, 폼 안에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 CSRF 보호 미들웨어가 요청을 검증할 수 있습니다. 편의를 위해 `@csrf` Blade 지시어를 사용하면, 숨겨진 토큰 입력 필드를 손쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<!-- The `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [middleware](/docs/12.x/middleware), which is included in the `web` middleware group by default, will automatically verify that the token in the request input matches the token stored in the session. When these two tokens match, we know that the authenticated user is the one initiating the request. -->
`Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` [middleware](/docs/12.x/middleware)는 기본적으로 `web` 미들웨어 그룹에 포함되어 있으며, 요청 입력에 포함된 토큰과 세션에 저장된 토큰이 일치하는지 자동으로 검사합니다. 두 토큰이 일치할 때, 인증된 사용자가 직접 요청을 보냈음을 알 수 있습니다.

<a name="csrf-tokens-and-spas"></a>
<!-- ### CSRF Tokens & SPAs -->
### CSRF Tokens & SPAs

<!-- If you are building an SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/12.x/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities. -->
만약 Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 개발 중이라면, API 인증 및 CSRF 공격 방지에 관한 자세한 내용은 [Laravel Sanctum documentation](/docs/12.x/sanctum)를 참고하시기 바랍니다.

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
특정 URI 경로를 CSRF 보호에서 제외하고 싶을 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 이용해 결제를 처리하고, 그들의 웹훅(Webhook) 시스템을 사용할 경우, Stripe가 CSRF 토큰 값을 모르는 상태에서 요청을 보내므로, Stripe 웹훅을 처리하는 라우트는 CSRF 보호 대상에서 반드시 제외해야 합니다.

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that Laravel applies to all routes in the `routes/web.php` file. However, you may also exclude specific routes by providing their URIs to the `validateCsrfTokens` method in your application's `bootstrap/app.php` file: -->
이런 종류의 라우트는 보통 Laravel이 `routes/web.php` 파일 내 모든 라우트에 적용하는 `web` 미들웨어 그룹 바깥에 배치하는 것이 일반적입니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `validateCsrfTokens` 메서드에 제외하고 싶은 URI를 지정해 특정 라우트만 선택적으로 제외할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->validateCsrfTokens(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> [!NOTE]
> 편의를 위해, [running tests](/docs/12.x/testing) 시에는 CSRF 미들웨어가 모든 라우트에서 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` middleware, which is included in the `web` middleware group by default, will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
CSRF 토큰을 POST 파라미터로 확인하는 것 외에도, `Illuminate\Foundation\Http\Middleware\ValidateCsrfToken` 미들웨어(기본적으로 `web` 미들웨어 그룹에 포함)는 `X-CSRF-TOKEN` 요청 헤더 값을 검사합니다. 아래와 같이 토큰을 HTML `meta` 태그에 저장할 수도 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

<!-- Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology: -->
그런 뒤, jQuery와 같은 라이브러리에 토큰을 모든 요청 헤더에 자동으로 포함하도록 설정할 수 있습니다. 이렇게 하면 기존 JavaScript 기술을 사용하는 AJAX 기반 애플리케이션에서도 간단하게 CSRF 보호를 적용할 수 있습니다:

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
Laravel은 현재 CSRF 토큰 값을 암호화된 `XSRF-TOKEN` 쿠키에 저장해서, 프레임워크가 생성하는 각 응답마다 함께 전송합니다. 이 쿠키 값을 읽어 `X-XSRF-TOKEN` 요청 헤더로 설정할 수 있습니다.

<!-- This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests. -->
이 쿠키는 주로 개발자 편의를 위해 제공되며, Angular나 Axios 같은 일부 JavaScript 프레임워크 및 라이브러리는 동일 출처(Same-origin) 요청 시 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 포함시킵니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.
