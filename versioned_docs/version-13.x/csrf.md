<!-- # CSRF Protection -->
# CSRF Protection

- [Introduction](#csrf-introduction)
- [Preventing CSRF Requests](#preventing-csrf-requests)
    - [Origin Verification](#origin-verification)
    - [Excluding URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Cross-site request forgeries are a type of malicious exploit whereby unauthorized commands are performed on behalf of an authenticated user. Thankfully, Laravel makes it easy to protect your application from [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) attacks. -->
크로스 사이트 요청 위조(Cross-site request forgery)는 인증된 사용자를 대신해 인가되지 않은 명령을 실행하는 악의적인 공격 방식입니다. 다행히 Laravel을 사용하면 애플리케이션을 [cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery)(CSRF) 공격으로부터 쉽게 보호할 수 있습니다.

<a name="csrf-explanation"></a>
<!-- #### An Explanation of the Vulnerability -->
#### An Explanation of the Vulnerability

<!-- In case you're not familiar with cross-site request forgeries, let's discuss an example of how this vulnerability can be exploited. Imagine your application has a `/user/email` route that accepts a `POST` request to change the authenticated user's email address. Most likely, this route expects an `email` input field to contain the email address the user would like to begin using. -->
크로스 사이트 요청 위조가 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예시로 살펴보겠습니다. 애플리케이션에 인증된 사용자의 이메일 주소를 변경하기 위해 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보겠습니다. 이 라우트는 사용자가 새로 사용하려는 이메일 주소가 `email` 입력 필드에 담겨 있을 것으로 예상할 가능성이 높습니다.

<!-- Without CSRF protection, a malicious website could create an HTML form that points to your application's `/user/email` route and submits the malicious user's own email address: -->
CSRF 보호가 없다면, 악의적인 웹사이트는 애플리케이션의 `/user/email` 라우트를 가리키고 공격자 자신의 이메일 주소를 제출하는 HTML 폼을 만들 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

<!-- If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
악의적인 웹사이트가 페이지가 로드될 때 폼을 자동으로 제출한다면, 공격자는 아무것도 모르는 애플리케이션 사용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 됩니다. 그러면 해당 사용자의 이메일 주소가 애플리케이션에서 변경됩니다.

<!-- To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
이 취약점을 막으려면 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에서 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- The `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [middleware](/docs/13.x/middleware), which is included in the `web` middleware group by default, protects your application from cross-site request forgeries using a two-layer approach. -->
기본적으로 `web` Middleware 그룹에 포함되어 있는 `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [middleware](/docs/13.x/middleware)는 두 계층 방식으로 애플리케이션을 크로스 사이트 요청 위조로부터 보호합니다.

<!-- First, the middleware checks the browser's `Sec-Fetch-Site` header. Modern browsers automatically set this header on every request, indicating whether it originated from the same origin, the same site, or a cross-site source. If the header indicates the request came from the same origin, the request is allowed immediately without any token verification. -->
먼저 Middleware는 브라우저의 `Sec-Fetch-Site` 헤더를 확인합니다. 최신 브라우저는 모든 요청에 이 헤더를 자동으로 설정하며, 요청이 같은 origin, 같은 site, 또는 cross-site 소스에서 시작되었는지를 나타냅니다. 헤더가 요청이 같은 origin에서 왔음을 나타내면, 토큰 검증 없이 요청이 즉시 허용됩니다.

<!-- If origin verification does not pass — for example, because the request comes from an older browser that doesn't send the `Sec-Fetch-Site` header or because the connection is not secure — the middleware falls back to traditional CSRF token validation. -->
출처 검증을 통과하지 못하면, 예를 들어 요청이 `Sec-Fetch-Site` 헤더를 보내지 않는 오래된 브라우저에서 왔거나 연결이 안전하지 않은 경우, Middleware는 기존 방식의 CSRF 토큰 유효성 검증으로 대체합니다.

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/13.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravel은 애플리케이션이 관리하는 활성 [user session](/docs/13.x/session)마다 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내는 사람인지 확인하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 이 토큰에 접근할 수 없습니다.

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
현재 세션의 CSRF 토큰은 요청의 세션 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

<!-- Anytime you define a "POST", "PUT", "PATCH", or "DELETE" HTML form in your application, you should include a hidden CSRF `_token` field in the form so that the CSRF protection middleware can validate the request. For convenience, you may use the `@csrf` Blade directive to generate the hidden token input field: -->
애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다 CSRF 보호 Middleware가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의를 위해 `@csrf` Blade 디렉티브를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a name="csrf-tokens-and-spas"></a>
<!-- #### CSRF Tokens & SPAs -->
#### CSRF Tokens & SPAs

<!-- If you are building an SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/13.x/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities. -->
Laravel을 API 백엔드로 사용하는 SPA를 만들고 있다면, API 인증과 CSRF 취약점 방지에 대한 정보는 [Laravel Sanctum documentation](/docs/13.x/sanctum)를 참고해야 합니다.

<a name="origin-verification"></a>
<!-- ### Origin Verification -->
### Origin Verification

<!-- As discussed above, Laravel's request forgery middleware first checks the `Sec-Fetch-Site` header to determine if the request is from the same origin. By default, if this check does not pass, the middleware falls back to CSRF token validation. -->
앞에서 설명한 것처럼, Laravel의 request forgery Middleware는 먼저 `Sec-Fetch-Site` 헤더를 확인하여 요청이 같은 origin에서 온 것인지 판단합니다. 기본적으로 이 검사를 통과하지 못하면 Middleware는 CSRF 토큰 유효성 검증으로 대체합니다.

<!-- However, if you would like to rely solely on origin verification and disable the CSRF token fallback entirely, you may do so using the `preventRequestForgery` method in your application's `bootstrap/app.php` file: -->
하지만 출처 검증에만 의존하고 CSRF 토큰 대체 검증을 완전히 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

<!-- When using origin-only mode, requests that fail origin verification will receive a `403` HTTP response instead of the `419` response typically associated with CSRF token mismatches. -->
origin 전용 모드를 사용하면 출처 검증에 실패한 요청은 일반적으로 CSRF 토큰 불일치와 관련된 `419` 응답 대신 `403` HTTP 응답을 받습니다.

> [!WARNING]
> `Sec-Fetch-Site` 헤더는 브라우저가 안전한(HTTPS) 연결을 사용할 때만 전송합니다. 애플리케이션이 HTTPS로 제공되지 않는다면 출처 검증을 사용할 수 없으며, Middleware는 CSRF 토큰 유효성 검증으로 대체합니다.

<!-- If your application needs to accept requests from subdomains (for example, `dashboard.example.com` accepting requests from `example.com`), you may allow same-site requests in addition to same-origin requests: -->
애플리케이션이 서브도메인에서 오는 요청을 허용해야 하는 경우(예: `dashboard.example.com`이 `example.com`에서 오는 요청을 허용하는 경우), same-origin 요청뿐만 아니라 same-site 요청도 허용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
때로는 특정 URI 집합을 CSRF 보호에서 제외하고 싶을 수 있습니다. 예를 들어 결제 처리를 위해 [Stripe](https://stripe.com)를 사용하고 Webhook 시스템을 활용하는 경우, Stripe는 라우트에 어떤 CSRF 토큰을 보내야 하는지 알 수 없으므로 Stripe Webhook 처리 라우트를 CSRF 보호에서 제외해야 합니다.

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that Laravel applies to all routes in the `routes/web.php` file. However, you may also exclude specific routes by providing their URIs to the `preventRequestForgery` method in your application's `bootstrap/app.php` file: -->
일반적으로 이런 종류의 라우트는 Laravel이 `routes/web.php` 파일의 모든 라우트에 적용하는 `web` Middleware 그룹 밖에 두어야 합니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드에 URI를 제공하여 특정 라우트를 제외할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})
```

> [!NOTE]
> 편의를 위해 [running tests](/docs/13.x/testing) 중에는 모든 라우트에 대해 CSRF Middleware가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `PreventRequestForgery` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
CSRF 토큰을 POST 파라미터로 확인하는 것 외에도, `PreventRequestForgery` Middleware는 `X-CSRF-TOKEN` 요청 헤더도 확인합니다. 예를 들어 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

<!-- Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology: -->
그런 다음 jQuery 같은 라이브러리가 모든 요청 헤더에 토큰을 자동으로 추가하도록 설정할 수 있습니다. 이렇게 하면 레거시 JavaScript 기술을 사용하는 AJAX 기반 애플리케이션에 간단하고 편리한 CSRF 보호를 제공할 수 있습니다:

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
Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하며, 이 쿠키는 프레임워크가 생성하는 각 응답에 포함됩니다. 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

<!-- This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests. -->
이 쿠키는 주로 개발 편의를 위해 전송됩니다. Angular와 Axios 같은 일부 JavaScript 프레임워크와 라이브러리는 same-origin 요청에서 이 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어 주기 때문입니다.
