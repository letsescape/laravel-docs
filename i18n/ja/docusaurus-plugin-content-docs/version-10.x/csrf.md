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

<!--  If the malicious website automatically submits the form when the page is loaded, the malicious user only needs to lure an unsuspecting user of your application to visit their website and their email address will be changed in your application. -->
悪意のある Web サイトがページのロード時にフォームを自動的に送信する場合、悪意のあるユーザーは、アプリケーションの疑いを持たないユーザーを誘導して Web サイトにアクセスさせるだけでよく、そのユーザーの電子メール アドレスはアプリケーション内で変更されます。

<!--  To prevent this vulnerability, we need to inspect every incoming `POST`, `PUT`, `PATCH`, or `DELETE` request for a secret session value that the malicious application is unable to access. -->
この脆弱性を防ぐには、悪意のあるアプリケーションがアクセスできないシークレット セッション値について、すべての受信 `POST`、`PUT`、`PATCH`、または `DELETE` リクエストを検査する必要があります。

<a name="preventing-csrf-requests"></a>
<!-- ## Preventing CSRF Requests -->
## Preventing CSRF Requests

<!-- Laravel automatically generates a CSRF "token" for each active [user session](/docs/10.x/session) managed by the application. This token is used to verify that the authenticated user is the person actually making the requests to the application. Since this token is stored in the user's session and changes each time the session is regenerated, a malicious application is unable to access it. -->
Laravelは、アプリケーションによって管理されるアクティブな[user session](/docs/10.x/session)ごとにCSRF「トークン」を自動的に生成します。このトークンは、認証されたユーザーが実際にアプリケーションにリクエストを行っている本人であることを確認するために使用されます。このトークンはユーザーのセッションに保存され、セッションが再生成されるたびに変更されるため、悪意のあるアプリケーションはアクセスできません。

<!-- The current session's CSRF token can be accessed via the request's session or via the `csrf_token` helper function: -->
現在のセッションの CSRF トークンには、リクエストのセッションまたは `csrf_token` ヘルパ関数を介してアクセスできます。

```
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

<!-- The `App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/10.x/middleware), which is included in the `web` middleware group by default, will automatically verify that the token in the request input matches the token stored in the session. When these two tokens match, we know that the authenticated user is the one initiating the request. -->
`App\Http\Middleware\VerifyCsrfToken` [middleware](/docs/10.x/middleware) は、デフォルトで `web` ミドルウェア グループに含まれており、リクエスト入力内のトークンがセッションに保存されているトークンと一致するかどうかを自動的に検証します。これら 2 つのトークンが一致すると、認証されたユーザーがリクエストを開始したユーザーであることがわかります。

<a name="csrf-tokens-and-spas"></a>
<!-- ### CSRF Tokens & SPAs -->
### CSRF Tokens & SPAs

<!-- If you are building a SPA that is utilizing Laravel as an API backend, you should consult the [Laravel Sanctum documentation](/docs/10.x/sanctum) for information on authenticating with your API and protecting against CSRF vulnerabilities. -->
Laravel を API バックエンドとして利用する SPA を構築している場合は、API での認証と CSRF 脆弱性からの保護に関する情報について [Laravel Sanctum documentation](/docs/10.x/sanctum) を参照してください。

<a name="csrf-excluding-uris"></a>
<!-- ### Excluding URIs From CSRF Protection -->
### Excluding URIs From CSRF Protection

<!-- Sometimes you may wish to exclude a set of URIs from CSRF protection. For example, if you are using [Stripe](https://stripe.com) to process payments and are utilizing their webhook system, you will need to exclude your Stripe webhook handler route from CSRF protection since Stripe will not know what CSRF token to send to your routes. -->
場合によっては、一連の URI を CSRF 保護から除外したい場合があります。たとえば、[Stripe](https://stripe.com) を使用して支払いを処理し、Webhook システムを利用している場合、Stripe はルートに送信する CSRF トークンがわからないため、Stripe Webhook ハンドラー ルートを CSRF 保護から除外する必要があります。

<!-- Typically, you should place these kinds of routes outside of the `web` middleware group that the `App\Providers\RouteServiceProvider` applies to all routes in the `routes/web.php` file. However, you may also exclude the routes by adding their URIs to the `$except` property of the `VerifyCsrfToken` middleware: -->
通常、これらの種類のルートは、`App\Providers\RouteServiceProvider` が `routes/web.php` ファイル内のすべてのルートに適用する `web` ミドルウェア グループの外側に配置する必要があります。ただし、`VerifyCsrfToken` ミドルウェアの `$except` プロパティに URI を追加することで、ルートを除外することもできます。

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
> 便宜上、[running tests](/docs/10.x/testing) の場合、CSRF ミドルウェアはすべてのルートに対して自動的に無効になります。

<a name="csrf-x-csrf-token"></a>
<!-- ## X-CSRF-TOKEN -->
## X-CSRF-TOKEN

<!-- In addition to checking for the CSRF token as a POST parameter, the `App\Http\Middleware\VerifyCsrfToken` middleware will also check for the `X-CSRF-TOKEN` request header. You could, for example, store the token in an HTML `meta` tag: -->
`App\Http\Middleware\VerifyCsrfToken` ミドルウェアは、POST パラメーターとして CSRF トークンをチェックするだけでなく、`X-CSRF-TOKEN` リクエスト ヘッダーもチェックします。たとえば、トークンを HTML `meta` タグに保存できます。

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

> [!NOTE]
> デフォルトでは、`resources/js/bootstrap.js` ファイルには、`X-XSRF-TOKEN` ヘッダーを自動的に送信する Axios HTTP ライブラリが含まれています。

