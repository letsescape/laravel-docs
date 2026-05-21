# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [출처 검증](#origin-verification)
    - [URI 제외](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(Cross-site request forgery)는 인증된 사용자를 대신해 인가되지 않은 명령을 실행하는 악의적인 공격 방식입니다. 다행히 Laravel을 사용하면 애플리케이션을 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery)(CSRF) 공격으로부터 쉽게 보호할 수 있습니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조가 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예시로 살펴보겠습니다. 애플리케이션에 인증된 사용자의 이메일 주소를 변경하기 위해 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보겠습니다. 이 라우트는 사용자가 새로 사용하려는 이메일 주소가 `email` 입력 필드에 담겨 있을 것으로 예상할 가능성이 높습니다.

CSRF 보호가 없다면, 악의적인 웹사이트는 애플리케이션의 `/user/email` 라우트를 가리키고 공격자 자신의 이메일 주소를 제출하는 HTML 폼을 만들 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

악의적인 웹사이트가 페이지가 로드될 때 폼을 자동으로 제출한다면, 공격자는 아무것도 모르는 애플리케이션 사용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 됩니다. 그러면 해당 사용자의 이메일 주소가 애플리케이션에서 변경됩니다.

이 취약점을 막으려면 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에서 악의적인 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지 (Preventing CSRF Requests)

기본적으로 `web` Middleware 그룹에 포함되어 있는 `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [Middleware](/docs/13.x/middleware)는 두 계층 방식으로 애플리케이션을 크로스 사이트 요청 위조로부터 보호합니다.

먼저 Middleware는 브라우저의 `Sec-Fetch-Site` 헤더를 확인합니다. 최신 브라우저는 모든 요청에 이 헤더를 자동으로 설정하며, 요청이 같은 origin, 같은 site, 또는 cross-site 소스에서 시작되었는지를 나타냅니다. 헤더가 요청이 같은 origin에서 왔음을 나타내면, 토큰 검증 없이 요청이 즉시 허용됩니다.

출처 검증을 통과하지 못하면, 예를 들어 요청이 `Sec-Fetch-Site` 헤더를 보내지 않는 오래된 브라우저에서 왔거나 연결이 안전하지 않은 경우, Middleware는 기존 방식의 CSRF 토큰 유효성 검증으로 대체합니다.

Laravel은 애플리케이션이 관리하는 활성 [사용자 세션](/docs/13.x/session)마다 CSRF "토큰"을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내는 사람인지 확인하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되고 세션이 재생성될 때마다 변경되므로, 악의적인 애플리케이션은 이 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션 또는 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다 CSRF 보호 Middleware가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의를 위해 `@csrf` Blade 디렉티브를 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a name="csrf-tokens-and-spas"></a>
#### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA를 만들고 있다면, API 인증과 CSRF 취약점 방지에 대한 정보는 [Laravel Sanctum 문서](/docs/13.x/sanctum)를 참고해야 합니다.

<a name="origin-verification"></a>
### 출처 검증

앞에서 설명한 것처럼, Laravel의 request forgery Middleware는 먼저 `Sec-Fetch-Site` 헤더를 확인하여 요청이 같은 origin에서 온 것인지 판단합니다. 기본적으로 이 검사를 통과하지 못하면 Middleware는 CSRF 토큰 유효성 검증으로 대체합니다.

하지만 출처 검증에만 의존하고 CSRF 토큰 대체 검증을 완전히 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

origin 전용 모드를 사용하면 출처 검증에 실패한 요청은 일반적으로 CSRF 토큰 불일치와 관련된 `419` 응답 대신 `403` HTTP 응답을 받습니다.

> [!WARNING]
> `Sec-Fetch-Site` 헤더는 브라우저가 안전한(HTTPS) 연결을 사용할 때만 전송합니다. 애플리케이션이 HTTPS로 제공되지 않는다면 출처 검증을 사용할 수 없으며, Middleware는 CSRF 토큰 유효성 검증으로 대체합니다.

애플리케이션이 서브도메인에서 오는 요청을 허용해야 하는 경우(예: `dashboard.example.com`이 `example.com`에서 오는 요청을 허용하는 경우), same-origin 요청뿐만 아니라 same-site 요청도 허용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외

때로는 특정 URI 집합을 CSRF 보호에서 제외하고 싶을 수 있습니다. 예를 들어 결제 처리를 위해 [Stripe](https://stripe.com)를 사용하고 Webhook 시스템을 활용하는 경우, Stripe는 라우트에 어떤 CSRF 토큰을 보내야 하는지 알 수 없으므로 Stripe Webhook 처리 라우트를 CSRF 보호에서 제외해야 합니다.

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
> 편의를 위해 [테스트 실행](/docs/13.x/testing) 중에는 모든 라우트에 대해 CSRF Middleware가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 파라미터로 확인하는 것 외에도, `PreventRequestForgery` Middleware는 `X-CSRF-TOKEN` 요청 헤더도 확인합니다. 예를 들어 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음 jQuery 같은 라이브러리가 모든 요청 헤더에 토큰을 자동으로 추가하도록 설정할 수 있습니다. 이렇게 하면 레거시 JavaScript 기술을 사용하는 AJAX 기반 애플리케이션에 간단하고 편리한 CSRF 보호를 제공할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하며, 이 쿠키는 프레임워크가 생성하는 각 응답에 포함됩니다. 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발 편의를 위해 전송됩니다. Angular와 Axios 같은 일부 JavaScript 프레임워크와 라이브러리는 same-origin 요청에서 이 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어 주기 때문입니다.
