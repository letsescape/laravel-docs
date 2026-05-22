# CSRF保護 (CSRF Protection)

- [Introduction](#csrf-introduction)
- [CSRFリクエストの防止](#preventing-csrf-requests)
    - [原産地検証](#origin-verification)
    - [URIを除く](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 導入 (Introduction)

クロスサイトリクエストフォージェリは、認証されたユーザーに代わって未承認のコマンドが実行される、一種の悪意のあるエクスプロイトです。ありがたいことに、Laravel を使用すると、[クロスサイトリクエストフォージェリ](https://en.wikipedia.org/wiki/Cross-site_request_forgery) (CSRF) 攻撃からアプリケーションを簡単に保護できます。

<a name="csrf-explanation"></a>
#### 脆弱性の説明

クロスサイトリクエストフォージェリに詳しくない方のために、この脆弱性が悪用される例について説明します。アプリケーションに、認証されたユーザーの電子メール アドレスを変更する `POST` リクエストを受け入れる `/user/email` ルートがあると想像してください。おそらく、このルートでは、ユーザーが使用を開始したい電子メール アドレスが `email` 入力フィールドに含まれることが期待されます。

CSRF 保護がないと、悪意のある Web サイトは、アプリケーションの `/user/email` ルートを指す HTML フォームを作成し、悪意のあるユーザー自身の電子メール アドレスを送信する可能性があります。

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>
```

悪意のある Web サイトがページのロード時にフォームを自動的に送信する場合、悪意のあるユーザーは、アプリケーションの疑いを持たないユーザーを誘導して Web サイトにアクセスさせるだけでよく、そのユーザーの電子メール アドレスはアプリケーション内で変更されます。

この脆弱性を防ぐには、悪意のあるアプリケーションがアクセスできないシークレット セッション値について、すべての受信 `POST`、`PUT`、`PATCH`、または `DELETE` リクエストを検査する必要があります。

<a name="preventing-csrf-requests"></a>
## CSRFリクエストの防止 (Preventing CSRF Requests)

`Illuminate\Foundation\Http\Middleware\PreventRequestForgery` [middleware](/docs/{{version}}/middleware) は、デフォルトで `web` ミドルウェア グループに含まれており、2 層アプローチを使用してクロスサイトリクエストフォージェリからアプリケーションを保護します。

まず、ミドルウェアはブラウザーの `Sec-Fetch-Site` ヘッダーをチェックします。最近のブラウザでは、すべてのリクエストにこのヘッダーが自動的に設定され、リクエストの発信元が同じオリジン、同じサイト、またはクロスサイト ソースのいずれであるかを示します。ヘッダーがリクエストが同じオリジンからのものであることを示している場合、リクエストはトークン検証なしで直ちに許可されます。

発信元の検証に合格しない場合、たとえば、`Sec-Fetch-Site` ヘッダーを送信しない古いブラウザーからのリクエスト、または接続が安全でないために、ミドルウェアは従来の CSRF トークン検証に戻ります。

Laravelは、アプリケーションによって管理されるアクティブな[ユーザーセッション](/docs/{{version}}/session)ごとにCSRF「トークン」を自動的に生成します。このトークンは、認証されたユーザーが実際にアプリケーションにリクエストを行っている本人であることを確認するために使用されます。このトークンはユーザーのセッションに保存され、セッションが再生成されるたびに変更されるため、悪意のあるアプリケーションはアクセスできません。

現在のセッションの CSRF トークンには、リクエストのセッションまたは `csrf_token` ヘルパ関数を介してアクセスできます。

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});
```

アプリケーションで「POST」、「PUT」、「PATCH」、または「DELETE」HTML フォームを定義するときは常に、CSRF 保護ミドルウェアがリクエストを検証できるように、フォームに非表示の CSRF `_token` フィールドを含める必要があります。便宜上、`@csrf` Blade ディレクティブを使用して、非表示のトークン入力フィールドを生成できます。

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>
```

<a name="csrf-tokens-and-spas"></a>
#### CSRFトークンとSPA

Laravel を API バックエンドとして利用する SPA を構築している場合は、API による認証と CSRF 脆弱性からの保護についての情報について [Laravel Sanctum ドキュメント](/docs/{{version}}/sanctum) を参照してください。

<a name="origin-verification"></a>
### 原産地検証

上で説明したように、Laravel のリクエスト フォージェリ ミドルウェアは、最初に `Sec-Fetch-Site` ヘッダーをチェックして、リクエストが同じオリジンからのものであるかどうかを判断します。デフォルトでは、このチェックに合格しない場合、ミドルウェアは CSRF トークン検証に戻ります。

ただし、発信元の検証のみに依存し、CSRF トークンのフォールバックを完全に無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `preventRequestForgery` メソッドを使用して無効にすることができます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})
```

オリジンのみモードを使用する場合、オリジン検証に失敗したリクエストは、通常 CSRF トークンの不一致に関連付けられる `419` 応答ではなく、`403` HTTP 応答を受け取ります。

> [!WARNING]
> `Sec-Fetch-Site` ヘッダーは、安全な (HTTPS) 接続を介してブラウザーによってのみ送信されます。アプリケーションが HTTPS 経由で提供されない場合、オリジン検証は利用できず、ミドルウェアは CSRF トークン検証に戻ります。

アプリケーションがサブドメインからのリクエストを受け入れる必要がある場合 (たとえば、`dashboard.example.com` が `example.com` からのリクエストを受け入れる)、同一オリジンのリクエストに加えて同一サイトのリクエストを許可できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})
```

<a name="csrf-excluding-uris"></a>
### CSRF 保護からの URI の除外

場合によっては、一連の URI を CSRF 保護から除外したい場合があります。たとえば、[Stripe](https://stripe.com) を使用して支払いを処理し、Webhook システムを利用している場合、Stripe はルートに送信する CSRF トークンがわからないため、Stripe Webhook ハンドラー ルートを CSRF 保護から除外する必要があります。

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
> 便宜上、[テストの実行](/docs/{{version}}/testing) の場合、CSRF ミドルウェアはすべてのルートに対して自動的に無効になります。

<a name="csrf-x-csrf-token"></a>
## X-CSRF-トークン (X-CSRF-TOKEN)

`PreventRequestForgery` ミドルウェアは、POST パラメーターとして CSRF トークンをチェックするだけでなく、`X-CSRF-TOKEN` リクエスト ヘッダーもチェックします。たとえば、トークンを HTML `meta` タグに保存できます。

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

次に、jQuery などのライブラリに、すべてのリクエスト ヘッダーにトークンを自動的に追加するように指示できます。これにより、レガシー JavaScript テクノロジを使用して、AJAX ベースのアプリケーションにシンプルで便利な CSRF 保護が提供されます。

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-トークン (X-XSRF-TOKEN)

Laravel は、フレームワークによって生成された各応答に含まれる暗号化された `XSRF-TOKEN` Cookie に現在の CSRF トークンを保存します。 Cookie 値を使用して、`X-XSRF-TOKEN` リクエスト ヘッダーを設定できます。

Angular や Axios などの一部の JavaScript フレームワークおよびライブラリでは、同一オリジン リクエストの `X-XSRF-TOKEN` ヘッダーにその値が自動的に配置されるため、この Cookie は主に開発者の利便性を目的として送信されます。

