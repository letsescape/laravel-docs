# Laravel Sanctum (Laravel Sanctum)

- [Introduction](#introduction)
    - [仕組み](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
    - [デフォルトモデルの上書き](#overriding-default-models)
- [APIトークン認証](#api-token-authentication)
    - [APIトークンの発行](#issuing-api-tokens)
    - [トークンの能力](#token-abilities)
    - [ルートを守る](#protecting-routes)
    - [トークンの取り消し](#revoking-tokens)
    - [トークンの有効期限](#token-expiration)
- [SPA認証](#spa-authentication)
    - [Configuration](#spa-configuration)
    - [Authenticating](#spa-authenticating)
    - [ルートを守る](#protecting-spa-routes)
    - [プライベートブロードキャストチャンネルの認可](#authorizing-private-broadcast-channels)
- [モバイルアプリケーション認証](#mobile-application-authentication)
    - [APIトークンの発行](#issuing-mobile-api-tokens)
    - [ルートを守る](#protecting-mobile-api-routes)
    - [トークンの取り消し](#revoking-mobile-api-tokens)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Sanctum](https://github.com/laravel/sanctum) は、SPA (シングル ページ アプリケーション)、モバイル アプリケーション、およびシンプルなトークン ベースの API に非常に軽量な認証システムを提供します。 Sanctum を使用すると、アプリケーションの各ユーザーが自分のアカウント用に複数の API トークンを生成できます。これらのトークンには、トークンが実行できるアクションを指定する能力/スコープが付与される場合があります。

<a name="how-it-works"></a>
### 仕組み

Laravel Sanctum は 2 つの別々の問題を解決するために存在します。ライブラリについて詳しく説明する前に、それぞれについて説明しましょう。

<a name="how-it-works-api-tokens"></a>
#### APIトークン

まず、Sanctum は、複雑な OAuth を使用せずに、ユーザーに API トークンを発行するために使用できるシンプルなパッケージです。この機能は、GitHub や「個人アクセス トークン」を発行するその他のアプリケーションからインスピレーションを得ています。たとえば、アプリケーションの「アカウント設定」に、ユーザーが自分のアカウントの API トークンを生成できる画面があると想像してください。 Sanctum を使用してこれらのトークンを生成および管理できます。これらのトークンの有効期限は通常 (数年) 非常に長いですが、ユーザーがいつでも手動で取り消すことができます。

Laravel Sanctum は、ユーザー API トークンを単一のデータベース テーブルに保存し、有効な API トークンが含まれている必要がある `Authorization` ヘッダーを介して受信 HTTP リクエストを認証することにより、この機能を提供します。

<a name="how-it-works-spa-authentication"></a>
#### SPA認証

次に、Sanctum は、Laravel を利用した API と通信する必要があるシングル ページ アプリケーション (SPA) を認証する簡単な方法を提供するために存在します。これらの SPA は、Laravel アプリケーションと同じリポジトリに存在することも、Next.js や Nuxt を使用して作成された SPA など、完全に別のリポジトリであることもあります。

この機能に関して、Sanctum はいかなる種類のトークンも使用しません。代わりに、Sanctum は Laravel の組み込み Cookie ベースのセッション認証サービスを使用します。通常、Sanctum はこれを実現するために Laravel の `web` 認証ガードを利用します。これにより、CSRF 保護、セッション認証の利点が得られるだけでなく、XSS を介した認証資格情報の漏洩からも保護されます。

Sanctum は、受信リクエストが独自の SPA フロントエンドから発信された場合にのみ、Cookie を使用して認証を試みます。 Sanctum が受信 HTTP リクエストを検査するときは、まず認証 Cookie を確認し、存在しない場合は、有効な API トークンの `Authorization` ヘッダーを検査します。

> [!NOTE]
> API トークン認証のみまたは SPA 認証のみに Sanctum を使用することはまったく問題ありません。 Sanctum を使用しているからといって、Sanctum が提供する両方の機能を使用する必要があるというわけではありません。

<a name="installation"></a>
## インストール (Installation)

Laravel Sanctum は、`install:api` Artisan コマンドを使用してインストールできます。

```shell
php artisan install:api
```

次に、Sanctum を使用して SPA を認証する予定がある場合は、このドキュメントの [SPA認証](#spa-authentication) セクションを参照してください。

<a name="configuration"></a>
## 構成 (Configuration)

<a name="overriding-default-models"></a>
### デフォルトモデルの上書き

通常は必須ではありませんが、Sanctum によって内部的に使用される `PersonalAccessToken` モデルを自由に拡張できます。

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

次に、Sanctum が提供する `usePersonalAccessTokenModel` メソッドを介してカスタム モデルを使用するように Sanctum に指示できます。通常、このメソッドはアプリケーションの `AppServiceProvider` ファイルの `boot` メソッドで呼び出す必要があります。

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
## APIトークン認証 (API Token Authentication)

> [!NOTE]
> 独自のファーストパーティ SPA の認証に API トークンを使用しないでください。代わりに、Sanctum の組み込み [SPA認証機能](#spa-authentication) を使用してください。

<a name="issuing-api-tokens"></a>
### APIトークンの発行

Sanctum を使用すると、アプリケーションへの API リクエストの認証に使用できる API トークン/個人アクセス トークンを発行できます。 API トークンを使用してリクエストを行う場合、トークンは `Bearer` トークンとして `Authorization` ヘッダーに含める必要があります。

ユーザーへのトークンの発行を開始するには、ユーザー モデルで `Laravel\Sanctum\HasApiTokens` トレイトを使用する必要があります。

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

トークンを発行するには、`createToken` メソッドを使用できます。 `createToken` メソッドは、`Laravel\Sanctum\NewAccessToken` インスタンスを返します。 API トークンはデータベースに保存される前に SHA-256 ハッシュを使用してハッシュされますが、`NewAccessToken` インスタンスの `plainTextToken` プロパティを使用してトークンのプレーンテキスト値にアクセスできます。トークンが作成された直後に、この値をユーザーに表示する必要があります。

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

`HasApiTokens` トレイトによって提供される `tokens` Eloquent 関係を使用して、ユーザーのすべてのトークンにアクセスできます。

```php
foreach ($user->tokens as $token) {
    // ...
}
```

<a name="token-abilities"></a>
### トークンの能力

Sanctumでは、トークンに「能力」を割り当てることができます。アビリティは、OAuth の「スコープ」と同様の目的を果たします。文字列能力の配列を 2 番目の引数として `createToken` メソッドに渡すことができます。

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

Sanctum によって認証された受信リクエストを処理するとき、`tokenCan` メソッドまたは `tokenCant` メソッドを使用して、トークンに特定の機能があるかどうかを判断できます。

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```

<a name="token-ability-middleware"></a>
#### トークンアビリティミドルウェア

Sanctum には、受信リクエストが特定の機能が付与されたトークンで認証されていることを検証するために使用できる 2 つのミドルウェアも含まれています。まず、アプリケーションの `bootstrap/app.php` ファイルで次のミドルウェア エイリアスを定義します。

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```

`abilities` ミドルウェアをルートに割り当てて、受信リクエストのトークンにリストされているすべての機能があることを確認できます。

```php
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

`ability` ミドルウェアをルートに割り当てて、受信リクエストのトークンに、リストされている機能の * 少なくとも 1 つ* があることを確認できます。

```php
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
#### ファーストパーティ UI が開始したリクエスト

便宜上、受信した認証済みリクエストがファーストパーティ SPA からのものであり、Sanctum の組み込み [SPA認証](#spa-authentication) を使用している場合、`tokenCan` メソッドは常に `true` を返します。

ただし、これは必ずしもアプリケーションがユーザーにアクションの実行を許可する必要があることを意味するわけではありません。通常、アプリケーションの [認可ポリシー](/docs/{{version}}/authorization#creating-policies) は、トークンに機能を実行する権限が付与されているかどうかを判断し、ユーザー インスタンス自体にアクションの実行を許可する必要があるかどうかを確認します。

たとえば、サーバーを管理するアプリケーションを想像すると、トークンがサーバーを更新する権限を持っているかどうか、**および** サーバーがユーザーに属していることを確認することを意味します。

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

最初は、`tokenCan` メソッドの呼び出しを許可し、ファーストパーティ UI で開始されたリクエストに対して常に `true` を返すのは奇妙に思えるかもしれません。ただし、API トークンが利用可能であり、`tokenCan` メソッド経由で検査できると常に想定できると便利です。このアプローチを採用すると、リクエストがアプリケーションの UI からトリガーされたのか、API のサードパーティ コンシューマーのいずれかによって開始されたのかを気にすることなく、アプリケーションの承認ポリシー内で `tokenCan` メソッドをいつでも呼び出すことができます。

<a name="protecting-routes"></a>
### ルートを守る

すべての受信リクエストを認証する必要があるようにルートを保護するには、`routes/web.php` および `routes/api.php` ルート ファイル内の保護されたルートに `sanctum` 認証ガードをアタッチする必要があります。このガードは、受信リクエストがステートフルな Cookie 認証リクエストとして認証されるか、リクエストがサードパーティからのものである場合は有効な API トークン ヘッダーを含むことを保証します。

`sanctum` ガードを使用してアプリケーションの `routes/web.php` ファイル内のルートを認証することをなぜ推奨するのか疑問に思われるかもしれません。 Sanctum は最初に、Laravel の一般的なセッション認証 Cookie を使用して受信リクエストの認証を試みることに注意してください。その Cookie が存在しない場合、Sanctum はリクエストの `Authorization` ヘッダー内のトークンを使用してリクエストの認証を試みます。さらに、Sanctum を使用してすべてのリクエストを認証すると、現在認証されているユーザー インスタンスで常に `tokenCan` メソッドを呼び出すことができるようになります。

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-tokens"></a>
### トークンの取り消し

`Laravel\Sanctum\HasApiTokens` トレイトによって提供される `tokens` 関係を使用してデータベースからトークンを削除することで、トークンを「取り消す」ことができます。

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="token-expiration"></a>
### トークンの有効期限

デフォルトでは、Sanctum トークンは期限切れになることはなく、[トークンを取り消す](#revoking-tokens) によってのみ無効化されます。ただし、アプリケーションの API トークンの有効期限を構成したい場合は、アプリケーションの `sanctum` 構成ファイルで定義されている `expiration` 構成オプションを使用して構成できます。この構成オプションは、発行されたトークンが期限切れとみなされるまでの分数を定義します。

```php
'expiration' => 525600,
```

各トークンの有効期限を個別に指定したい場合は、`createToken` メソッドの 3 番目の引数として有効期限を指定します。

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```

アプリケーションのトークンの有効期限を設定している場合は、[タスクをスケジュールする](/docs/{{version}}/scheduling) を実行してアプリケーションの期限切れのトークンを削除することもできます。ありがたいことに、Sanctum には、これを実現するために使用できる `sanctum:prune-expired` Artisan コマンドが含まれています。たとえば、少なくとも 24 時間経過している期限切れのトークン データベース レコードをすべて削除するようにスケジュールされたタスクを構成できます。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA認証 (SPA Authentication)

Sanctum は、Laravel を利用した API と通信する必要があるシングル ページ アプリケーション (SPA) を認証する簡単な方法を提供するためにも存在します。これらの SPA は、Laravel アプリケーションと同じリポジトリに存在する場合もあれば、完全に別のリポジトリである場合もあります。

この機能に関して、Sanctum はいかなる種類のトークンも使用しません。代わりに、Sanctum は Laravel の組み込み Cookie ベースのセッション認証サービスを使用します。この認証アプローチでは、CSRF 保護、セッション認証の利点が得られるだけでなく、XSS を介した認証資格情報の漏洩からも保護されます。

> [!WARNING]
> 認証するには、SPA と API が同じトップレベル ドメインを共有する必要があります。ただし、異なるサブドメインに配置される場合もあります。さらに、リクエストとともに `Accept: application/json` ヘッダーと、`Referer` ヘッダーまたは `Origin` ヘッダーのいずれかを送信するようにしてください。

<a name="spa-configuration"></a>
### 構成

<a name="configuring-your-first-party-domains"></a>
#### ファーストパーティドメインの構成

まず、SPA がどのドメインからリクエストを行うかを設定する必要があります。これらのドメインは、`sanctum` 構成ファイルの `stateful` 構成オプションを使用して構成できます。この構成設定は、API にリクエストを行うときに、Laravel セッション Cookie を使用して「ステートフル」認証を維持するドメインを決定します。

ファーストパーティのステートフル ドメインのセットアップを支援するために、Sanctum は構成に含めることができる 2 つのヘルパ関数を提供します。まず、`Sanctum::currentApplicationUrlWithPort()` は `APP_URL` 環境変数から現在のアプリケーション URL を返し、`Sanctum::currentRequestHost()` はステートフル ドメイン リストにプレースホルダーを挿入します。これは実行時に現在のリクエストのホストによって置き換えられ、同じドメインを持つすべてのリクエストがステートフルであると見なされます。

> [!WARNING]
> ポート (`127.0.0.1:8000`) を含む URL 経由でアプリケーションにアクセスしている場合は、ドメインにポート番号を必ず含める必要があります。

<a name="sanctum-middleware"></a>
#### Sanctumミドルウェア

次に、サードパーティまたはモバイルアプリケーションからのリクエストが API トークンを使用して認証できるようにしながら、SPA から受信したリクエストを Laravel のセッション Cookie を使用して認証できるように Laravel に指示する必要があります。これは、アプリケーションの `bootstrap/app.php` ファイルで `statefulApi` ミドルウェア メソッドを呼び出すことで簡単に実現できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```

<a name="cors-and-cookies"></a>
#### CORS と Cookie

別のサブドメインで実行される SPA からのアプリケーションの認証で問題が発生する場合は、CORS (Cross-Origin Resource Sharing) またはセッション Cookie の設定が間違っている可能性があります。

`config/cors.php` 構成ファイルは、デフォルトでは公開されません。 Laravel の CORS オプションをカスタマイズする必要がある場合は、`config:publish` Artisan コマンドを使用して、完全な `cors` 構成ファイルを公開する必要があります。

```shell
php artisan config:publish cors
```

次に、アプリケーションの CORS 構成が `True` の値を持つ `Access-Control-Allow-Credentials` ヘッダーを返していることを確認する必要があります。これは、アプリケーションの `config/cors.php` 構成ファイル内の `supports_credentials` オプションを `true` に設定することで実現できます。

さらに、アプリケーションのグローバル `axios` インスタンスで `withCredentials` および `withXSRFToken` オプションを有効にする必要があります。通常、これは `resources/js/bootstrap.js` ファイルで実行する必要があります。 Axios を使用してフロントエンドから HTTP リクエストを作成していない場合は、独自の HTTP クライアントで同等の構成を実行する必要があります。

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```

最後に、アプリケーションのセッション Cookie ドメイン構成がルート ドメインのサブドメインをサポートしていることを確認する必要があります。これを行うには、アプリケーションの `config/session.php` 構成ファイル内でドメインの先頭に `.` を付加します。

```php
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
### 認証中

<a name="csrf-protection"></a>
#### CSRF保護

SPA を認証するには、SPA の「ログイン」ページでまず `/sanctum/csrf-cookie` エンドポイントにリクエストを作成し、アプリケーションの CSRF 保護を初期化する必要があります。

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

このリクエスト中に、Laravel は現在の CSRF トークンを含む `XSRF-TOKEN` Cookie を設定します。このトークンは URL デコードされ、後続のリクエストで `X-XSRF-TOKEN` ヘッダーに渡される必要があります。これは、Axios や Angular HttpClient などの一部の HTTP クライアント ライブラリが自動的に実行します。 JavaScript HTTP ライブラリが値を設定しない場合は、このルートによって設定される `XSRF-TOKEN` Cookie の URL デコードされた値と一致するように、`X-XSRF-TOKEN` ヘッダーを手動で設定する必要があります。

<a name="logging-in"></a>
#### ログインする

CSRF保護が初期化されたら、Laravelアプリケーションの`/login`ルートに対して`POST`リクエストを行う必要があります。この `/login` ルートは、[手動で実装](/docs/{{version}}/authentication#authenticating-users) であるか、[Laravel の強化](/docs/{{version}}/fortify) のようなヘッドレス認証パッケージを使用している可能性があります。

ログインリクエストが成功すると認証され、アプリケーションのルートへの後続のリクエストは、Laravel アプリケーションがクライアントに発行したセッション Cookie を介して自動的に認証されます。さらに、アプリケーションはすでに `/sanctum/csrf-cookie` ルートにリクエストを行っているため、JavaScript HTTP クライアントが `X-XSRF-TOKEN` ヘッダーの `XSRF-TOKEN` Cookie の値を送信している限り、後続のリクエストは自動的に CSRF 保護を受ける必要があります。

もちろん、アクティビティがないためにユーザーのセッションが期限切れになった場合、Laravel アプリケーションへの後続のリクエストは 401 または 419 HTTP エラー応答を受け取る可能性があります。この場合、ユーザーを SPA のログイン ページにリダイレクトする必要があります。

> [!WARNING]
> 独自の `/login` エンドポイントを自由に作成できます。ただし、標準の [Laravelが提供するセッションベースの認証サービス](/docs/{{version}}/authentication#authenticating-users) を使用してユーザーを認証することを確認する必要があります。通常、これは、`web` 認証ガードを使用することを意味します。

<a name="protecting-spa-routes"></a>
### ルートを守る

すべての受信リクエストを認証する必要があるようにルートを保護するには、`routes/api.php` ファイル内の API ルートに `sanctum` 認証ガードをアタッチする必要があります。このガードは、受信リクエストが SPA からのステートフル認証リクエストとして認証されるか、リクエストがサードパーティからのものである場合は有効な API トークン ヘッダーを含むことを保証します。

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="authorizing-private-broadcast-channels"></a>
### プライベートブロードキャストチャンネルの認可

SPA が [プライベート/プレゼンスブロードキャストチャンネル](/docs/{{version}}/broadcasting#authorizing-channels) で認証する必要がある場合は、アプリケーションの `bootstrap/app.php` ファイルに含まれる `withRouting` メソッドから `channels` エントリを削除する必要があります。代わりに、`withBroadcasting` メソッドを呼び出して、アプリケーションのブロードキャスト ルートに適切なミドルウェアを指定できるようにする必要があります。

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
```

次に、プッシャーの認証リクエストを成功させるには、[Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation) を初期化するときにカスタム プッシャー `authorizer` を指定する必要があります。これにより、アプリケーションで `axios` インスタンス ([クロスドメインリクエスト用に適切に構成されている](#cors-and-cookies)) を使用するようにプッシャーを構成できるようになります。

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```

<a name="mobile-application-authentication"></a>
## モバイルアプリケーション認証 (Mobile Application Authentication)

Sanctum トークンを使用して、モバイル アプリケーションの API へのリクエストを認証することもできます。モバイル アプリケーション リクエストを認証するプロセスは、サードパーティ API リクエストを認証するプロセスと似ています。ただし、API トークンの発行方法には若干の違いがあります。

<a name="issuing-mobile-api-tokens"></a>
### APIトークンの発行

まず、ユーザーの電子メール/ユーザー名、パスワード、デバイス名を受け入れるルートを作成し、それらの資格情報を新しい Sanctum トークンと交換します。このエンドポイントに与えられる「デバイス名」は情報提供を目的としており、任意の値を指定できます。一般に、デバイス名の値は、「Nuno's iPhone 17」など、ユーザーが認識できる名前にする必要があります。

通常、モバイル アプリケーションの「ログイン」画面からトークン エンドポイントにリクエストを送信します。エンドポイントはプレーンテキストの API トークンを返します。このトークンはモバイル デバイスに保存され、追加の API リクエストを行うために使用されます。

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```

モバイル アプリケーションがトークンを使用してアプリケーションに API リクエストを行う場合、`Authorization` ヘッダー内のトークンを `Bearer` トークンとして渡す必要があります。

> [!NOTE]
> モバイル アプリケーションのトークンを発行する場合は、[トークンの能力](#token-abilities) を自由に指定することもできます。

<a name="protecting-mobile-api-routes"></a>
### ルートを守る

前に説明したように、`sanctum` 認証ガードをルートにアタッチすることで、すべての受信リクエストが認証される必要があるようにルートを保護できます。

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

<a name="revoking-mobile-api-tokens"></a>
### トークンの取り消し

ユーザーがモバイル デバイスに発行された API トークンを取り消すことができるようにするには、Web アプリケーションの UI の「アカウント設定」部分内で、「取り消し」ボタンとともに名前でリストすることができます。ユーザーが「取り消し」ボタンをクリックすると、データベースからトークンを削除できます。 `Laravel\Sanctum\HasApiTokens` トレイトによって提供される `tokens` 関係を介してユーザーの API トークンにアクセスできることを覚えておいてください。

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
## テスト (Testing)

テスト中に、`Sanctum::actingAs` メソッドを使用してユーザーを認証し、トークンにどの能力を付与するかを指定できます。

```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

トークンにすべての能力を付与したい場合は、`actingAs` メソッドに提供される能力リストに `*` を含める必要があります。

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```

