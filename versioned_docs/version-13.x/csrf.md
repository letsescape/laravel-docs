# CSRF 보호 (CSRF Protection)

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
    - [Origin 검증](#origin-verification)
    - [URI 제외하기](#csrf-excluding-uris)
- [X-CSRF-TOKEN](#csrf-x-csrf-token)
- [X-XSRF-TOKEN](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개 (Introduction)

크로스 사이트 요청 위조(Cross-site request forgery, CSRF)는 인증된 사용자를 가장해 무단 명령을 실행하는 악의적 공격 유형입니다. 다행히도, Laravel은 [크로스 사이트 요청 위조](https://en.wikipedia.org/wiki/Cross-site_request_forgery) 공격으로부터 애플리케이션을 간편하게 보호할 수 있도록 지원합니다.

<a name="csrf-explanation"></a>
#### 취약점 설명

크로스 사이트 요청 위조(CSRF)에 익숙하지 않다면, 이 취약점이 어떻게 악용될 수 있는지 예를 들어 살펴보겠습니다. 예를 들어, 여러분의 애플리케이션에 인증된 사용자의 이메일 주소를 변경하는 `POST` 요청을 받는 `/user/email` 라우트가 있다고 가정해 보겠습니다. 이 라우트는 일반적으로 사용자가 변경하고 싶어하는 새 이메일 주소를 `email` 입력 필드로 받습니다.

만약 CSRF 보호 기능이 없다면, 악성 웹사이트가 여러분의 애플리케이션의 `/user/email` 라우트로 연결되는 HTML 폼을 만들고, 공격자의 이메일 주소를 입력값으로 제출할 수 있습니다:

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

만약 위와 같이 악성 웹사이트가 페이지가 로드될 때 폼을 자동으로 제출하도록 하면, 공격자는 아무것도 모르는 사용자가 자신의 웹사이트를 방문하도록 유도하기만 하면 인증된 사용자의 이메일 주소가 공격자 소유의 이메일로 바뀔 수 있습니다.

이런 취약점을 막기 위해서는, 들어오는 모든 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해, 외부 악성 애플리케이션이 접근할 수 없는 비밀 세션 값을 검사해야 합니다.

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지 (Preventing CSRF Requests)

기본적으로 `web` 미들웨어 그룹에 포함되는 `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [미들웨어](/docs/13.x/middleware)는 두 단계 방식으로 애플리케이션을 크로스 사이트 요청 위조로부터 보호합니다.

먼저, 이 미들웨어는 브라우저의 `Sec-Fetch-Site` 헤더를 확인합니다. 최신 브라우저는 모든 요청에 이 헤더를 자동으로 포함하며, 요청이 동일 출처, 동일 사이트, 또는 교차 사이트에서 시작되었는지를 나타냅니다. 이 헤더가 동일 출처에서 온 요청임을 나타내면 토큰 검증 없이 즉시 요청을 허용합니다.

Origin 검증을 통과하지 못하면, 예를 들어 오래된 브라우저가 `Sec-Fetch-Site` 헤더를 보내지 않거나 연결이 보안되지 않은 경우에는, 미들웨어가 기존의 CSRF 토큰 검증 방식으로 되돌아갑니다.

Laravel은 애플리케이션이 관리하는 활성 [사용자 세션](/docs/13.x/session)마다 자동으로 CSRF "토큰"을 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 보내고 있는지 검증하는 데 사용됩니다. 이 토큰은 사용자의 세션에 저장되며 세션이 재생성될 때마다 변경되기 때문에, 악성 애플리케이션이 이 토큰에 접근할 수 없습니다.

현재 세션의 CSRF 토큰은 요청의 세션이나 `csrf_token` 헬퍼 함수로 얻을 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

애플리케이션에서 "POST", "PUT", "PATCH", "DELETE"와 같은 HTML 폼을 작성할 때마다, 폼 안에 숨겨진 CSRF `_token` 필드를 반드시 포함해야 CSRF 보호 미들웨어가 요청을 검증할 수 있습니다. 편의를 위해 `@csrf` Blade 지시어를 사용하면, 숨겨진 토큰 입력 필드를 손쉽게 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a name="csrf-tokens-and-spas"></a>
#### CSRF 토큰과 SPA

만약 Laravel을 API 백엔드로 사용하는 SPA(싱글 페이지 애플리케이션)를 개발 중이라면, API 인증 및 CSRF 공격 방지에 관한 자세한 내용은 [Laravel Sanctum 문서](/docs/13.x/sanctum)를 참고하시기 바랍니다.

<a name="origin-verification"></a>
### Origin 검증

앞서 설명한 것처럼 Laravel의 요청 위조 방지 미들웨어는 먼저 `Sec-Fetch-Site` 헤더를 검사해 요청이 동일 출처에서 온 것인지 판단합니다. 기본적으로 이 검사를 통과하지 못하면 미들웨어는 CSRF 토큰 검증으로 되돌아갑니다.

하지만 Origin 검증만 사용하고 CSRF 토큰 폴백을 완전히 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

origin-only 모드를 사용할 때 Origin 검증에 실패한 요청은 일반적인 CSRF 토큰 불일치 시 반환되는 `419` 응답 대신 `403` HTTP 응답을 받습니다.

> [!WARNING]
> `Sec-Fetch-Site` 헤더는 브라우저가 보안 연결(HTTPS)에서만 전송합니다. 애플리케이션이 HTTPS로 제공되지 않는다면 Origin 검증은 사용할 수 없으며, 미들웨어는 CSRF 토큰 검증으로 되돌아갑니다.

애플리케이션이 서브도메인에서 오는 요청도 허용해야 한다면, 예를 들어 `dashboard.example.com`이 `example.com`에서 오는 요청을 받아야 한다면, 동일 출처뿐 아니라 동일 사이트 요청도 허용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

특정 URI 경로를 CSRF 보호에서 제외하고 싶을 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 이용해 결제를 처리하고, 그들의 웹훅(Webhook) 시스템을 사용할 경우, Stripe가 CSRF 토큰 값을 모르는 상태에서 요청을 보내므로, Stripe 웹훅을 처리하는 라우트는 CSRF 보호 대상에서 반드시 제외해야 합니다.

이런 종류의 라우트는 보통 Laravel이 `routes/web.php` 파일 내 모든 라우트에 적용하는 `web` 미들웨어 그룹 바깥에 배치하는 것이 일반적입니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드에 제외하고 싶은 URI를 지정해 특정 라우트만 선택적으로 제외할 수도 있습니다:

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
> 편의를 위해, [테스트 실행](/docs/13.x/testing) 시에는 CSRF 미들웨어가 모든 라우트에서 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 `POST` 파라미터로 확인하는 것 외에도 `PreventRequestForgery` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더 값도 검사합니다. 예를 들어 아래와 같이 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

그런 뒤, jQuery와 같은 라이브러리에 토큰을 모든 요청 헤더에 자동으로 포함하도록 설정할 수 있습니다. 이렇게 하면 기존 JavaScript 기술을 사용하는 AJAX 기반 애플리케이션에서도 간단하게 CSRF 보호를 적용할 수 있습니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel은 현재 CSRF 토큰 값을 암호화된 `XSRF-TOKEN` 쿠키에 저장해서, 프레임워크가 생성하는 각 응답마다 함께 전송합니다. 이 쿠키 값을 읽어 `X-XSRF-TOKEN` 요청 헤더로 설정할 수 있습니다.

이 쿠키는 주로 개발자 편의를 위해 제공되며, Angular나 Axios 같은 일부 JavaScript 프레임워크 및 라이브러리는 동일 출처(Same-origin) 요청 시 쿠키 값을 자동으로 `X-XSRF-TOKEN` 헤더에 포함시킵니다.

> [!NOTE]
> 기본적으로 `resources/js/bootstrap.js` 파일에는 Axios HTTP 라이브러리가 포함되어 있으며, 이 라이브러리는 자동으로 `X-XSRF-TOKEN` 헤더를 전송합니다.
