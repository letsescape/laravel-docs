# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [Origin(출처) 확인](#origin-verification)
    - [CSRF 보호에서 URI 제외](#csrf-excluding-uris)
- [X-CSRF-TOKEN](#csrf-x-csrf-token)
- [X-XSRF-TOKEN](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(CSRF, Cross-site request forgery)는 인증된 사용자를 가장해 무단으로 명령을 수행하도록 하는 악의적인 공격 방식 중 하나입니다. 다행히도 Laravel은 애플리케이션을 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 손쉽게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점에 대한 설명

크로스 사이트 요청 위조(CSRF)에 익숙하지 않은 분들을 위해, 이 취약점이 어떻게 악용될 수 있는지 예시를 들어 설명하겠습니다. 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `/user/email` 경로가 있다고 가정해봅니다. 이 경로는 사용자가 사용하고자 하는 이메일 주소가 담긴 `email` 입력 필드를 `POST` 요청으로 받아 처리할 것입니다.

만약 CSRF 보호가 없다면, 악의적인 웹사이트가 여러분의 애플리케이션의 `/user/email` 경로로 자신의 이메일 주소를 담아 HTML 폼을 작성할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

이 악의적인 웹사이트가 페이지가 로드될 때 위 폼을 자동으로 전송하도록 설정하면, 공격자는 여러분의 애플리케이션 사용자를 자신의 웹사이트로 유인하기만 하면 해당 사용자의 이메일 주소를 마음대로 변경할 수 있습니다.

이런 취약점을 막기 위해서는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 외부 애플리케이션이 알 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지 (Preventing CSRF Requests)

Laravel에서는 기본적으로 `web` 미들웨어 그룹에 포함된 `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [미들웨어](/docs/master/middleware)가 두 단계로 애플리케이션을 CSRF로부터 보호합니다.

첫 번째로, 미들웨어는 브라우저의 `Sec-Fetch-Site` 헤더를 확인합니다. 최신 브라우저는 모든 요청에 이 헤더를 자동으로 추가하여 동일 출처(same origin), 동일 사이트(same site), 또는 교차 사이트(cross-site) 요청인지를 표시합니다. 만약 이 헤더가 동일 출처에서 온 것임을 나타내면, 별도의 토큰 검증 없이 즉시 요청이 허용됩니다.

하지만 origin(출처) 확인에 실패하는 경우—예를 들어 구형 브라우저라서 `Sec-Fetch-Site` 헤더를 보내지 않거나, 연결이 안전하지 않은 경우—미들웨어는 전통적인 CSRF 토큰 검증 방식으로 전환합니다.

Laravel은 애플리케이션이 관리하는 활성 [사용자 세션](/docs/master/session)마다 고유한 CSRF "토큰"을 자동으로 생성합니다. 이 토큰을 통해 인증된 사용자가 실제로 요청을 보냈는지 확인할 수 있습니다. 이 토큰은 사용자의 세션에 저장되고, 세션이 재생성될 때마다 변경되기 때문에, 악의적인 애플리케이션은 이 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수를 통해 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE" HTML 폼을 정의할 때마다, 해당 폼에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 CSRF 보호 미들웨어가 요청을 검증할 수 있습니다. 편의상, `@csrf` Blade 디렉티브를 사용하면 숨겨진 토큰 입력 필드를 손쉽게 추가할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- 위와 동일한 기능 -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a name="csrf-tokens-and-spas"></a>
#### CSRF 토큰과 SPA

Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 개발 중이라면, API 인증 및 CSRF 취약점 방지 방법에 대해 [Laravel Sanctum 문서](/docs/master/sanctum)를 참고하시기 바랍니다.

<a name="origin-verification"></a>
### Origin(출처) 확인 (Origin Verification)

앞서 설명한 대로, Laravel의 요청 위조 방지 미들웨어는 먼저 `Sec-Fetch-Site` 헤더를 확인하여 요청의 출처(origin)를 판별합니다. 기본적으로 이 확인이 실패할 경우, 미들웨어는 CSRF 토큰 검증 방식으로 전환합니다.

그러나, 출처(origin) 확인에만 의존하고 싶고 CSRF 토큰 검증 방식은 완전히 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드를 사용하여 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

origin-only 모드를 사용할 때는, 출처 검증에 실패한 요청에 대해 보통 CSRF 토큰 불일치 상황에서 반환하는 `419` 응답 대신, `403` HTTP 응답이 반환됩니다.

> [!WARNING]
> `Sec-Fetch-Site` 헤더는 오직 HTTPS(보안) 연결을 통해 브라우저가 보낼 때만 전송됩니다. 만약 애플리케이션이 HTTPS로 제공되지 않는다면, 출처(origin) 확인을 사용할 수 없으므로 미들웨어는 CSRF 토큰 검증 방식으로 자동 전환합니다.

애플리케이션이 서브도메인(예: `dashboard.example.com`이 `example.com`에서 오는 요청을 수락해야 하는 경우) 요청을 허용할 필요가 있다면, 동일 출처(same-origin) 외에도 동일 사이트(same-site) 요청을 허용하도록 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외 (Excluding URIs From CSRF Protection)

특정 URI들을 CSRF 보호에서 제외하고 싶을 때가 있을 수 있습니다. 예를 들어, [Stripe](https://stripe.com)로 결제를 처리하고 웹훅(Webhook) 시스템을 사용하는 경우, Stripe가 여러분의 CSRF 토큰을 알지 못하므로 Stripe 웹훅 처리 경로를 CSRF 보호에서 제외해야 합니다.

이러한 경로들은 일반적으로 Laravel에서 모든 경로에 자동 적용되는 `routes/web.php`의 `web` 미들웨어 그룹 외부에 두는 것이 권장됩니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일 내 `preventRequestForgery` 메서드에 제외할 URI를 명시함으로써 특정 경로만 CSRF 보호에서 제외할 수도 있습니다:

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
> 편의를 위해, [테스트 실행](/docs/master/testing) 시에는 모든 경로에서 CSRF 미들웨어가 자동 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 파라미터로 검사하는 것 외에도, `PreventRequestForgery` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 검사합니다. 예를 들어, HTML `meta` 태그에 토큰을 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 다음, jQuery와 같은 라이브러리가 모든 요청 헤더에 토큰을 자동 추가하도록 설정할 수 있습니다. 이를 통해 레거시 자바스크립트 기술을 사용하는 AJAX 기반 애플리케이션에서도 간편하게 CSRF 보호를 적용할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 담아 프레임워크에서 생성하는 모든 응답에 포함시킵니다. 이 쿠키의 값을 이용해 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자 편의성을 위해 제공되며, Angular, Axios와 같이 일부 자바스크립트 프레임워크 및 라이브러리는 동일 출처 요청 시 이 값을 자동으로 `X-XSRF-TOKEN` 헤더에 넣어줍니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.
