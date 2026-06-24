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
クロスサイトリクエストフォージェリは、認証されたユーザーに代わって未承認のコマンドが実行される、一種の悪意のあるエクスプロイトです。ありがたいことに、Laravel を使用すると、[cross-site request forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 攻撃からアプリケーションを簡単に保護できます。

<a name="csrf-explanation"></a>
<!-- #### An Explanation of the Vulnerability -->
#### An Explanation of the Vulnerability

<!-- In case you're not familiar with cross-site request forgeries, let's discuss an example of how this vulnerability can be exploited. Imagine your application has a `/user/email` route that accepts a `POST` request to change the authenticated user's email address. Most likely, this route expects an `email` input field to contain the email address the user would like to begin using. -->
クロスサイトリクエストフォージェリに詳しくない方のために、この脆弱性が悪用される例について説明します。アプリケーションに、認証されたユーザーの電子メール アドレスを変更する `POST` リクエストを受け入れる `/user/email` ルートがあると想像してください。おそらく、このルートでは、ユーザーが使用を開始したい電子メール アドレスが `email` 入力フィールドに含まれることが期待されます。

<!-- Without CSRF protection, a malicious website could create an HTML form that points to your application's `/user/email` route and submits the malicious user's own email address: -->
CSRF 保護がないと、悪意のある Web サイトは、アプリケーションの `/user/email` ルートを指す HTML フォームを作成し、悪意のあるユーザー自身の電子メール アドレスを送信する可能性があります。

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

<!-- If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
悪意のある Web サイトがページのロード時にフォームを自動的に送信する場合、悪意のあるユーザーは、アプリケーションの疑いを持たないユーザーを誘導して Web サイトにアクセスさせるだけでよく、そのユーザーの電子メール アドレスはアプリケーション内で変更されます。

<!-- To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
この脆弱性を防ぐには、悪意のあるアプリケーションがアクセスできないシークレット セッション値について、すべての受信 `POST`、`PUT`、`PATCH`、または `DELETE` リクエストを検査する必要があります。

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- The `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [middleware](/docs/13.x/middleware), which is included in the `web` middleware group by default, protects your application from cross-site request forgeries using a two-layer approach. -->
`Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [middleware](/docs/13.x/middleware) は、デフォルトで `web` ミドルウェア グループに含まれており、2 層アプローチを使用してクロスサイトリクエストフォージェリからアプリケーションを保護します。

<!-- First, the middleware checks the browser's `Sec-Fetch-Site` header. Modern browsers automatically set this header on every request, indicating whether it originated from the same origin, the same site, or a cross-site source. If the header indicates the request came from the same origin, the request is allowed immediately without any token verification. -->
まず、ミドルウェアはブラウザーの `Sec-Fetch-Site` ヘッダーをチェックします。最近のブラウザでは、すべてのリクエストにこのヘッダーが自動的に設定され、リクエストの発信元が同じオリジン、同じサイト、またはクロスサイト ソースのいずれであるかを示します。ヘッダーがリクエストが同じオリジンからのものであることを示している場合、リクエストはトークン検証なしで直ちに許可されます。

<!-- If origin verification does not pass — for example, because the request comes from an older browser that doesn't send the `Sec-Fetch-Site` header or because the connection is not secure — the middleware falls back to traditional CSRF token validation. -->
発信元の検証に合格しない場合、たとえば、`Sec-Fetch-Site` ヘッダーを送信しない古いブラウザーからのリクエスト、または接続が安全でないために、ミドルウェアは従来の CSRF トークン検証に戻ります。

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/13.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravelは、アプリケーションによって管理されるアクティブな[user session](/docs/13.x/session)ごとにCSRF「トークン」を自動的に生成します。このトークンは、認証されたユーザーが実際にアプリケーションにリクエストを行っている本人であることを確認するために使用されます。このトークンはユーザーのセッションに保存され、セッションが再生成されるたびに変更されるため、悪意のあるアプリケーションはアクセスできません。

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
現在のセッションの CSRF トークンには、リクエストのセッションまたは `csrf_token` ヘルパ関数を介してアクセスできます。

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

<!-- Anytime you define a "POST", "PUT", "PATCH", or "DELETE" HTML form in your application, you should include a hidden CSRF `_token` field in the form so that the CSRF protection middleware can validate the request. For convenience, you may use the `@csrf` Blade directive to generate the hidden token input field: -->
アプリケーションで「POST」、「PUT」、「PATCH」、または「DELETE」HTML フォームを定義するときは常に、CSRF 保護ミドルウェアがリクエストを検証できるように、フォームに非表示の CSRF `_token` フィールドを含める必要があります。便宜上、`@csrf` Blade ディレクティブを使用して、非表示のトークン入力フィールドを生成できます。

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
Laravel を API バックエンドとして利用する SPA を構築している場合は、API による認証と CSRF 脆弱性からの保護についての情報について [Laravel Sanctum documentation](/docs/13.x/sanctum) を参照してください。

<a name="origin-verification"></a>
<!-- ### Origin Verification -->
### Origin Verification

<!-- As discussed above, Laravel's request forgery middleware first checks the `Sec-Fetch-Site` header to determine if the request is from the same origin. By default, if this check does not pass, the middleware falls back to CSRF token validation. -->
上で説明したように、Laravel のリクエスト フォージェリ ミドルウェアは、最初に `Sec-Fetch-Site` ヘッダーをチェックして、リクエストが同じオリジンからのものであるかどうかを判断します。デフォルトでは、このチェックに合格しない場合、ミドルウェアは CSRF トークン検証に戻ります。

<!-- However, if you would like to rely solely on origin verification and disable the CSRF token fallback entirely, you may do so using the `preventRequestForgery` method in your application's `bootstrap/app.php` file: -->
ただし、発信元の検証のみに依存し、CSRF トークンのフォールバックを完全に無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `preventRequestForgery` メソッドを使用して無効にすることができます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

<!-- When using origin-only mode, requests that fail origin verification will receive a `403` HTTP response instead of the `419` response typically associated with CSRF token mismatches. -->
オリジンのみモードを使用する場合、オリジン検証に失敗したリクエストは、通常 CSRF トークンの不一致に関連付けられる `419` 応答ではなく、`403` HTTP 応答を受け取ります。

> [!WARNING]
> `Sec-Fetch-Site` ヘッダーは、安全な (HTTPS) 接続を介してブラウザーによってのみ送信されます。アプリケーションが HTTPS 経由で提供されない場合、オリジン検証は利用できず、ミドルウェアは CSRF トークン検証に戻ります。

<!-- If your application needs to accept requests from subdomains (for example, `dashboard.example.com` accepting requests from `example.com`), you may allow same-site requests in addition to same-origin requests: -->
アプリケーションがサブドメインからのリクエストを受け入れる必要がある場合 (たとえば、`dashboard.example.com` が `example.com` からのリクエストを受け入れる)、同一オリジンのリクエストに加えて同一サイトのリクエストを許可できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
場合によっては、一連の URI を CSRF 保護から除外したい場合があります。たとえば、[Stripe](https://stripe.com) を使用して支払いを処理し、Webhook システムを利用している場合、Stripe はルートに送信する CSRF トークンがわからないため、Stripe Webhook ハンドラー ルートを CSRF 保護から除外する必要があります。

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that Laravel applies to all routes in the `routes/web.php` file. However, you may also exclude specific routes by providing their URIs to the `preventRequestForgery` method in your application's `bootstrap/app.php` file: -->
通常、この種のルートは、Laravel が `routes/web.php` ファイル内のすべてのルートに適用する `web` ミドルウェア グループの外側に配置する必要があります。ただし、アプリケーションの `bootstrap/app.php` ファイル内の `preventRequestForgery` メソッドに URI を指定することで、特定のルートを除外することもできます。

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
> 便宜上、[running tests](/docs/13.x/testing) の場合、CSRF ミドルウェアはすべてのルートに対して自動的に無効になります。

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `PreventRequestForgery` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
`PreventRequestForgery` ミドルウェアは、POST パラメーターとして CSRF トークンをチェックするだけでなく、`X-CSRF-TOKEN` リクエスト ヘッダーもチェックします。たとえば、トークンを HTML `meta` タグに保存できます。

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

<!-- Then, you can instruct a library like jQuery to automatically add the token to all request headers. This provides simple, convenient CSRF protection for your AJAX based applications using legacy JavaScript technology: -->
次に、jQuery などのライブラリに、すべてのリクエスト ヘッダーにトークンを自動的に追加するように指示できます。これにより、レガシー JavaScript テクノロジを使用して、AJAX ベースのアプリケーションにシンプルで便利な CSRF 保護が提供されます。

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
Laravel は、フレームワークによって生成された各応答に含まれる暗号化された `XSRF-TOKEN` Cookie に現在の CSRF トークンを保存します。 Cookie 値を使用して、`X-XSRF-TOKEN` リクエスト ヘッダーを設定できます。

<!-- This cookie is primarily sent as a developer convenience since some JavaScript frameworks and libraries, like Angular and Axios, automatically place its value in the `X-XSRF-TOKEN` header on same-origin requests. -->
Angular や Axios などの一部の JavaScript フレームワークおよびライブラリでは、同一オリジン リクエストの `X-XSRF-TOKEN` ヘッダーにその値が自動的に配置されるため、この Cookie は主に開発者の利便性を目的として送信されます。

