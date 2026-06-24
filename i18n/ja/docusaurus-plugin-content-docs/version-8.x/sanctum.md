<!-- # Laravel Sanctum -->
# Laravel Sanctum

- [Introduction](#introduction)
    - [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Overriding Default Models](#overriding-default-models)
- [API Token Authentication](#api-token-authentication)
    - [Issuing API Tokens](#issuing-api-tokens)
    - [Token Abilities](#token-abilities)
    - [Protecting Routes](#protecting-routes)
    - [Revoking Tokens](#revoking-tokens)
- [SPA Authentication](#spa-authentication)
    - [Configuration](#spa-configuration)
    - [Authenticating](#spa-authenticating)
    - [Protecting Routes](#protecting-spa-routes)
    - [Authorizing Private Broadcast Channels](#authorizing-private-broadcast-channels)
- [Mobile Application Authentication](#mobile-application-authentication)
    - [Issuing API Tokens](#issuing-mobile-api-tokens)
    - [Protecting Routes](#protecting-mobile-api-routes)
    - [Revoking Tokens](#revoking-mobile-api-tokens)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Sanctum](https://github.com/laravel/sanctum) provides a featherweight authentication system for SPAs (single page applications), mobile applications, and simple, token based APIs. Sanctum allows each user of your application to generate multiple API tokens for their account. These tokens may be granted abilities / scopes which specify which actions the tokens are allowed to perform. -->
[Laravel Sanctum](https://github.com/laravel/sanctum) は、SPA (シングル ページ アプリケーション)、モバイル アプリケーション、およびシンプルなトークン ベースの API に非常に軽量な認証システムを提供します。 Sanctum を使用すると、アプリケーションの各ユーザーが自分のアカウント用に複数の API トークンを生成できます。これらのトークンには、トークンが実行できるアクションを指定する能力/スコープが付与される場合があります。

<a name="how-it-works"></a>
<!-- ### How It Works -->
### How It Works

<!-- Laravel Sanctum exists to solve two separate problems. Let's discuss each before digging deeper into the library. -->
Laravel Sanctum は 2 つの別々の問題を解決するために存在します。ライブラリについて詳しく説明する前に、それぞれについて説明しましょう。

<a name="how-it-works-api-tokens"></a>
<!-- #### API Tokens -->
#### API Tokens

<!-- First, Sanctum is a simple package you may use to issue API tokens to your users without the complication of OAuth. This feature is inspired by GitHub and other applications which issue "personal access tokens". For example, imagine the "account settings" of your application has a screen where a user may generate an API token for their account. You may use Sanctum to generate and manage those tokens. These tokens typically have a very long expiration time (years), but may be manually revoked by the user at anytime. -->
まず、Sanctum は、複雑な OAuth を使用せずに、ユーザーに API トークンを発行するために使用できるシンプルなパッケージです。この機能は、GitHub や「個人アクセス トークン」を発行するその他のアプリケーションからインスピレーションを得ています。たとえば、アプリケーションの「アカウント設定」に、ユーザーが自分のアカウントの API トークンを生成できる画面があると想像してください。 Sanctum を使用してこれらのトークンを生成および管理できます。これらのトークンの有効期限は通常非常に長い (年単位) ですが、ユーザーがいつでも手動で取り消すことができます。

<!-- Laravel Sanctum offers this feature by storing user API tokens in a single database table and authenticating incoming HTTP requests via the `Authorization` header which should contain a valid API token. -->
Laravel Sanctum は、ユーザー API トークンを単一のデータベース テーブルに保存し、有効な API トークンが含まれている必要がある `Authorization` ヘッダーを介して受信 HTTP リクエストを認証することにより、この機能を提供します。

<a name="how-it-works-spa-authentication"></a>
<!-- #### SPA Authentication -->
#### SPA Authentication

<!-- Second, Sanctum exists to offer a simple way to authenticate single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository, such as a SPA created using Vue CLI or a Next.js application. -->
次に、Sanctum は、Laravel を利用した API と通信する必要があるシングル ページ アプリケーション (SPA) を認証する簡単な方法を提供するために存在します。これらの SPA は、Laravel アプリケーションと同じリポジトリに存在することも、Vue CLI や Next.js アプリケーションを使用して作成された SPA など、完全に別のリポジトリであることもあります。

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. Typically, Sanctum utilizes Laravel's `web` authentication guard to accomplish this. This provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
この機能に関して、Sanctum はいかなる種類のトークンも使用しません。代わりに、Sanctum は Laravel の組み込み Cookie ベースのセッション認証サービスを使用します。通常、Sanctum はこれを実現するために Laravel の `web` 認証ガードを利用します。これにより、CSRF 保護、セッション認証の利点が得られるだけでなく、XSS を介した認証資格情報の漏洩からも保護されます。

<!-- Sanctum will only attempt to authenticate using cookies when the incoming request originates from your own SPA frontend. When Sanctum examines an incoming HTTP request, it will first check for an authentication cookie and, if none is present, Sanctum will then examine the `Authorization` header for a valid API token. -->
Sanctum は、受信リクエストが独自の SPA フロントエンドから発信された場合にのみ、Cookie を使用して認証を試みます。 Sanctum が受信 HTTP リクエストを検査するときは、まず認証 Cookie を確認し、存在しない場合は、有効な API トークンの `Authorization` ヘッダーを検査します。

> [!TIP]
> Sanctum を API トークン認証のみまたは SPA 認証のみに使用するのはまったく問題ありません。 Sanctum を使用しているからといって、Sanctum が提供する両方の機能を使用する必要があるというわけではありません。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!TIP]
> Laravel の最新バージョンには、すでに Laravel Sanctum が含まれています。ただし、アプリケーションの `composer.json` ファイルに `laravel/sanctum` が含まれていない場合は、以下のインストール手順に従ってください。

<!-- You may install Laravel Sanctum via the Composer package manager: -->
Composer パッケージマネージャーを介して Laravel Sanctum をインストールできます。

```
composer require laravel/sanctum
```

<!-- Next, you should publish the Sanctum configuration and migration files using the `vendor:publish` Artisan command. The `sanctum` configuration file will be placed in your application's `config` directory: -->
次に、`vendor:publish` Artisan コマンドを使用して、Sanctum 構成ファイルと移行ファイルを公開する必要があります。 `sanctum` 構成ファイルは、アプリケーションの `config` ディレクトリに配置されます。

```
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

<!-- Finally, you should run your database migrations. Sanctum will create one database table in which to store API tokens: -->
最後に、データベースの移行を実行する必要があります。 Sanctum は、API トークンを保存するデータベース テーブルを 1 つ作成します。

```
php artisan migrate
```

<!-- Next, if you plan to utilize Sanctum to authenticate an SPA, you should add Sanctum's middleware to your `api` middleware group within your application's `app/Http/Kernel.php` file: -->
次に、Sanctum を使用して SPA を認証する予定の場合は、アプリケーションの `app/Http/Kernel.php` ファイル内の `api` ミドルウェア グループに Sanctum のミドルウェアを追加する必要があります。

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="migration-customization"></a>
<!-- #### Migration Customization -->
#### Migration Customization

<!-- If you are not going to use Sanctum's default migrations, you should call the `Sanctum::ignoreMigrations` method in the `register` method of your `App\Providers\AppServiceProvider` class. You may export the default migrations by executing the following command: `php artisan vendor:publish --tag=sanctum-migrations` -->
Sanctum のデフォルトの移行を使用しない場合は、`App\Providers\AppServiceProvider` クラスの `register` メソッドで `Sanctum::ignoreMigrations` メソッドを呼び出す必要があります。次のコマンドを実行して、デフォルトの移行をエクスポートできます: `php artisan vendor:publish --tag=sanctum-migrations`

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- Although not typically required, you are free to extend the `PersonalAccessToken` model used internally by Sanctum: -->
通常は必須ではありませんが、Sanctum によって内部的に使用される `PersonalAccessToken` モデルを自由に拡張できます。

```
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```

<!-- Then, you may instruct Sanctum to use your custom model via the `usePersonalAccessTokenModel` method provided by Sanctum. Typically, you should call this method in the `boot` method of one of your application's service providers: -->
次に、Sanctum が提供する `usePersonalAccessTokenModel` メソッドを介してカスタム モデルを使用するように Sanctum に指示できます。通常、このメソッドは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッドで呼び出す必要があります。

```
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```

<a name="api-token-authentication"></a>
<!-- ## API Token Authentication -->
## API Token Authentication

> [!TIP]
> 独自のファーストパーティ SPA の認証に API トークンを使用しないでください。代わりに、Sanctum の組み込み [SPA authentication features](#spa-authentication) を使用してください。

<a name="issuing-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- Sanctum allows you to issue API tokens / personal access tokens that may be used to authenticate API requests to your application. When making requests using API tokens, the token should be included in the `Authorization` header as a `Bearer` token. -->
Sanctum を使用すると、アプリケーションへの API リクエストの認証に使用できる API トークン/個人アクセス トークンを発行できます。 API トークンを使用してリクエストを行う場合、トークンは `Bearer` トークンとして `Authorization` ヘッダーに含める必要があります。

<!-- To begin issuing tokens for users, your User model should use the `Laravel\Sanctum\HasApiTokens` trait: -->
ユーザーへのトークンの発行を開始するには、ユーザー モデルで `Laravel\Sanctum\HasApiTokens` トレイトを使用する必要があります。

```
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- To issue a token, you may use the `createToken` method. The `createToken` method returns a `Laravel\Sanctum\NewAccessToken` instance. API tokens are hashed using SHA-256 hashing before being stored in your database, but you may access the plain-text value of the token using the `plainTextToken` property of the `NewAccessToken` instance. You should display this value to the user immediately after the token has been created: -->
トークンを発行するには、`createToken` メソッドを使用できます。 `createToken` メソッドは、`Laravel\Sanctum\NewAccessToken` インスタンスを返します。 API トークンはデータベースに保存される前に SHA-256 ハッシュを使用してハッシュされますが、`NewAccessToken` インスタンスの `plainTextToken` プロパティを使用してトークンのプレーンテキスト値にアクセスできます。トークンが作成された直後に、この値をユーザーに表示する必要があります。

```
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```

<!-- You may access all of the user's tokens using the `tokens` Eloquent relationship provided by the `HasApiTokens` trait: -->
`HasApiTokens` トレイトによって提供される `tokens` Eloquent 関係を使用して、ユーザーのすべてのトークンにアクセスできます。

```
foreach ($user->tokens as $token) {
    //
}
```

<a name="token-abilities"></a>
<!-- ### Token Abilities -->
### Token Abilities

<!-- Sanctum allows you to assign "abilities" to tokens. Abilities serve a similar purpose as OAuth's "scopes". You may pass an array of string abilities as the second argument to the `createToken` method: -->
Sanctumでは、トークンに「能力」を割り当てることができます。アビリティは、OAuth の「スコープ」と同様の目的を果たします。文字列能力の配列を 2 番目の引数として `createToken` メソッドに渡すことができます。

```
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```

<!-- When handling an incoming request authenticated by Sanctum, you may determine if the token has a given ability using the `tokenCan` method: -->
Sanctum によって認証された受信リクエストを処理するとき、`tokenCan` メソッドを使用して、トークンに特定の機能があるかどうかを判断できます。

```
if ($user->tokenCan('server:update')) {
    //
}
```

<a name="token-ability-middleware"></a>
<!-- #### Token Ability Middleware -->
#### Token Ability Middleware

<!-- Sanctum also includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given ability. To get started, add the following middleware to the `$routeMiddleware` property of your application's `app/Http/Kernel.php` file: -->
Sanctum には、受信リクエストが特定の機能が付与されたトークンで認証されていることを検証するために使用できる 2 つのミドルウェアも含まれています。まず、次のミドルウェアをアプリケーションの `app/Http/Kernel.php` ファイルの `$routeMiddleware` プロパティに追加します。

```
'abilities' => \Laravel\Sanctum\Http\Middleware\CheckAbilities::class,
'ability' => \Laravel\Sanctum\Http\Middleware\CheckForAnyAbility::class,
```

<!-- The `abilities` middleware may be assigned to a route to verify that the incoming request's token has all of the listed abilities: -->
`abilities` ミドルウェアをルートに割り当てて、受信リクエストのトークンにリストされているすべての機能があることを確認できます。

```
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```

<!-- The `ability` middleware may be assigned to a route to verify that the incoming request's token has *at least one* of the listed abilities: -->
`ability` ミドルウェアをルートに割り当てて、受信リクエストのトークンに、リストされている機能の * 少なくとも 1 つ* があることを確認できます。

```
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```

<a name="first-party-ui-initiated-requests"></a>
<!-- #### First-Party UI Initiated Requests -->
#### First-Party UI Initiated Requests

<!-- For convenience, the `tokenCan` method will always return `true` if the incoming authenticated request was from your first-party SPA and you are using Sanctum's built-in [SPA authentication](#spa-authentication). -->
便宜上、受信した認証済みリクエストがファーストパーティ SPA からのものであり、Sanctum の組み込み [SPA authentication](#spa-authentication) を使用している場合、`tokenCan` メソッドは常に `true` を返します。

<!-- However, this does not necessarily mean that your application has to allow the user to perform the action. Typically, your application's [authorization policies](/docs/8.x/authorization#creating-policies) will determine if the token has been granted the permission to perform the abilities as well as check that the user instance itself should be allowed to perform the action. -->
ただし、これは必ずしもアプリケーションがユーザーにアクションの実行を許可する必要があることを意味するわけではありません。通常、アプリケーションの [authorization policies](/docs/8.x/authorization#creating-policies) は、トークンに機能を実行する権限が付与されているかどうかを判断し、ユーザー インスタンス自体にアクションの実行を許可する必要があるかどうかを確認します。

<!-- For example, if we imagine an application that manages servers, this might mean checking that token is authorized to update servers **and** that the server belongs to the user: -->
たとえば、サーバーを管理するアプリケーションを想像すると、トークンがサーバーを更新する権限を持っているかどうか、**および** サーバーがユーザーに属していることを確認することを意味します。

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update')
```

<!-- At first, allowing the `tokenCan` method to be called and always return `true` for first-party UI initiated requests may seem strange; however, it is convenient to be able to always assume an API token is available and can be inspected via the `tokenCan` method. By taking this approach, you may always call the `tokenCan` method within your application's authorizations policies without worrying about whether the request was triggered from your application's UI or was initiated by one of your API's third-party consumers. -->
最初は、`tokenCan` メソッドの呼び出しを許可し、ファーストパーティ UI で開始されたリクエストに対して常に `true` を返すのは奇妙に思えるかもしれません。ただし、API トークンが利用可能であり、`tokenCan` メソッド経由で検査できると常に想定できると便利です。このアプローチを採用すると、リクエストがアプリケーションの UI からトリガーされたのか、API のサードパーティ コンシューマーのいずれかによって開始されたのかを気にすることなく、アプリケーションの承認ポリシー内でいつでも `tokenCan` メソッドを呼び出すことができます。

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your protected routes within your `routes/web.php` and `routes/api.php` route files. This guard will ensure that incoming requests are authenticated as either stateful, cookie authenticated requests or contain a valid API token header if the request is from a third party. -->
すべての受信リクエストを認証する必要があるようにルートを保護するには、`routes/web.php` および `routes/api.php` ルート ファイル内の保護されたルートに `sanctum` 認証ガードをアタッチする必要があります。このガードは、受信リクエストがステートフルな Cookie 認証リクエストとして認証されるか、リクエストがサードパーティからのものである場合は有効な API トークン ヘッダーを含むことを保証します。

<!-- You may be wondering why we suggest that you authenticate the routes within your application's `routes/web.php` file using the `sanctum` guard. Remember, Sanctum will first attempt to authenticate incoming requests using Laravel's typical session authentication cookie. If that cookie is not present then Sanctum will attempt to authenticate the request using a token in the request's `Authorization` header. In addition, authenticating all requests using Sanctum ensures that we may always call the `tokenCan` method on the currently authenticated user instance: -->
`sanctum` ガードを使用してアプリケーションの `routes/web.php` ファイル内のルートを認証することをなぜ推奨するのか疑問に思われるかもしれません。 Sanctum は最初に、Laravel の一般的なセッション認証 Cookie を使用して受信リクエストの認証を試みることに注意してください。その Cookie が存在しない場合、Sanctum はリクエストの `Authorization` ヘッダー内のトークンを使用してリクエストの認証を試みます。さらに、Sanctum を使用してすべてのリクエストを認証すると、現在認証されているユーザー インスタンスで常に `tokenCan` メソッドを呼び出すことができるようになります。

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may "revoke" tokens by deleting them from your database using the `tokens` relationship that is provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
`Laravel\Sanctum\HasApiTokens` トレイトによって提供される `tokens` 関係を使用してデータベースからトークンを削除することで、トークンを「取り消す」ことができます。

```
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- Sanctum also exists to provide a simple method of authenticating single page applications (SPAs) that need to communicate with a Laravel powered API. These SPAs might exist in the same repository as your Laravel application or might be an entirely separate repository. -->
Sanctum は、Laravel を利用した API と通信する必要があるシングル ページ アプリケーション (SPA) を認証する簡単な方法を提供するためにも存在します。これらの SPA は、Laravel アプリケーションと同じリポジトリに存在する場合もあれば、完全に別のリポジトリである場合もあります。

<!-- For this feature, Sanctum does not use tokens of any kind. Instead, Sanctum uses Laravel's built-in cookie based session authentication services. This approach to authentication provides the benefits of CSRF protection, session authentication, as well as protects against leakage of the authentication credentials via XSS. -->
この機能に関して、Sanctum はいかなる種類のトークンも使用しません。代わりに、Sanctum は Laravel の組み込み Cookie ベースのセッション認証サービスを使用します。この認証アプローチでは、CSRF 保護、セッション認証の利点が得られるだけでなく、XSS を介した認証資格情報の漏洩からも保護されます。

> [!NOTE]
> 認証するには、SPA と API が同じトップレベル ドメインを共有する必要があります。ただし、異なるサブドメインに配置される場合もあります。さらに、リクエストとともに `Accept: application/json` ヘッダーを送信するようにしてください。


<a name="spa-configuration"></a>
<!-- ### Configuration -->
### Configuration

<a name="configuring-your-first-party-domains"></a>
<!-- #### Configuring Your First-Party Domains -->
#### Configuring Your First-Party Domains

<!-- First, you should configure which domains your SPA will be making requests from. You may configure these domains using the `stateful` configuration option in your `sanctum` configuration file. This configuration setting determines which domains will maintain "stateful" authentication using Laravel session cookies when making requests to your API. -->
まず、SPA がどのドメインからリクエストを行うかを設定する必要があります。これらのドメインは、`sanctum` 構成ファイルの `stateful` 構成オプションを使用して構成できます。この構成設定は、API にリクエストを行うときに、Laravel セッション Cookie を使用して「ステートフル」認証を維持するドメインを決定します。

> [!NOTE]
> ポート (`127.0.0.1:8000`) を含む URL 経由でアプリケーションにアクセスしている場合は、ドメインにポート番号を必ず含める必要があります。

<a name="sanctum-middleware"></a>
<!-- #### Sanctum Middleware -->
#### Sanctum Middleware

<!-- Next, you should add Sanctum's middleware to your `api` middleware group within your `app/Http/Kernel.php` file. This middleware is responsible for ensuring that incoming requests from your SPA can authenticate using Laravel's session cookies, while still allowing requests from third parties or mobile applications to authenticate using API tokens: -->
次に、Sanctum のミドルウェアを、`app/Http/Kernel.php` ファイル内の `api` ミドルウェア グループに追加する必要があります。このミドルウェアは、SPA からの受信リクエストが Laravel のセッション Cookie を使用して認証できるようにすると同時に、サードパーティまたはモバイル アプリケーションからのリクエストが API トークンを使用して認証できるようにする役割を果たします。

```
'api' => [
    \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    'throttle:api',
    \Illuminate\Routing\Middleware\SubstituteBindings::class,
],
```

<a name="cors-and-cookies"></a>
<!-- #### CORS & Cookies -->
#### CORS & Cookies

<!-- If you are having trouble authenticating with your application from a SPA that executes on a separate subdomain, you have likely misconfigured your CORS (Cross-Origin Resource Sharing) or session cookie settings. -->
別のサブドメインで実行される SPA からのアプリケーションの認証で問題が発生する場合は、CORS (Cross-Origin Resource Sharing) またはセッション Cookie の設定が間違っている可能性があります。

<!-- You should ensure that your application's CORS configuration is returning the `Access-Control-Allow-Credentials` header with a value of `True`. This may be accomplished by setting the `supports_credentials` option within your application's `config/cors.php` configuration file to `true`. -->
アプリケーションの CORS 構成が、値 `True` を持つ `Access-Control-Allow-Credentials` ヘッダーを返していることを確認する必要があります。これは、アプリケーションの `config/cors.php` 構成ファイル内の `supports_credentials` オプションを `true` に設定することで実現できます。

<!-- In addition, you should enable the `withCredentials` option on your application's global `axios` instance. Typically, this should be performed in your `resources/js/bootstrap.js` file. If you are not using Axios to make HTTP requests from your frontend, you should perform the equivalent configuration on your own HTTP client: -->
さらに、アプリケーションのグローバル `axios` インスタンスで `withCredentials` オプションを有効にする必要があります。通常、これは `resources/js/bootstrap.js` ファイルで実行する必要があります。 Axios を使用してフロントエンドから HTTP リクエストを作成していない場合は、独自の HTTP クライアントで同等の構成を実行する必要があります。

```
axios.defaults.withCredentials = true;
```

<!-- Finally, you should ensure your application's session cookie domain configuration supports any subdomain of your root domain. You may accomplish this by prefixing the domain with a leading `.` within your application's `config/session.php` configuration file: -->
最後に、アプリケーションのセッション Cookie ドメイン構成がルート ドメインのサブドメインをサポートしていることを確認する必要があります。これを行うには、アプリケーションの `config/session.php` 構成ファイル内でドメインの先頭に `.` を付加します。

```
'domain' => '.domain.com',
```

<a name="spa-authenticating"></a>
<!-- ### Authenticating -->
### Authenticating

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- To authenticate your SPA, your SPA's "login" page should first make a request to the `/sanctum/csrf-cookie` endpoint to initialize CSRF protection for the application: -->
SPA を認証するには、SPA の「ログイン」ページでまず `/sanctum/csrf-cookie` エンドポイントにリクエストを作成し、アプリケーションの CSRF 保護を初期化する必要があります。

```
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

<!-- During this request, Laravel will set an `XSRF-TOKEN` cookie containing the current CSRF token. This token should then be passed in an `X-XSRF-TOKEN` header on subsequent requests, which some HTTP client libraries like Axios and the Angular HttpClient will do automatically for you. If your JavaScript HTTP library does not set the value for you, you will need to manually set the `X-XSRF-TOKEN` header to match the value of the `XSRF-TOKEN` cookie that is set by this route. -->
このリクエスト中に、Laravel は現在の CSRF トークンを含む `XSRF-TOKEN` Cookie を設定します。このトークンは、後続のリクエストの `X-XSRF-TOKEN` ヘッダーで渡す必要があります。これは、Axios や Angular HttpClient などの一部の HTTP クライアント ライブラリが自動的に行います。 JavaScript HTTP ライブラリが値を設定しない場合は、このルートによって設定される `XSRF-TOKEN` Cookie の値と一致するように `X-XSRF-TOKEN` ヘッダーを手動で設定する必要があります。

<a name="logging-in"></a>
<!-- #### Logging In -->
#### Logging In

<!-- Once CSRF protection has been initialized, you should make a `POST` request to your Laravel application's `/login` route. This `/login` route may be [implemented manually](/docs/8.x/authentication#authenticating-users) or using a headless authentication package like [Laravel Fortify](/docs/8.x/fortify). -->
CSRF保護が初期化されたら、Laravelアプリケーションの`/login`ルートに対して`POST`リクエストを行う必要があります。この `/login` ルートは、[implemented manually](/docs/8.x/authentication#authenticating-users) であるか、[Laravel Fortify](/docs/8.x/fortify) のようなヘッドレス認証パッケージを使用している可能性があります。

<!-- If the login request is successful, you will be authenticated and subsequent requests to your application's routes will automatically be authenticated via the session cookie that the Laravel application issued to your client. In addition, since your application already made a request to the `/sanctum/csrf-cookie` route, subsequent requests should automatically receive CSRF protection as long as your JavaScript HTTP client sends the value of the `XSRF-TOKEN` cookie in the `X-XSRF-TOKEN` header. -->
ログインリクエストが成功すると認証され、アプリケーションのルートへの後続のリクエストは、Laravel アプリケーションがクライアントに発行したセッション Cookie を介して自動的に認証されます。さらに、アプリケーションはすでに `/sanctum/csrf-cookie` ルートにリクエストを行っているため、JavaScript HTTP クライアントが `X-XSRF-TOKEN` ヘッダーの `XSRF-TOKEN` Cookie の値を送信している限り、後続のリクエストは自動的に CSRF 保護を受ける必要があります。

<!-- Of course, if your user's session expires due to lack of activity, subsequent requests to the Laravel application may receive 401 or 419 HTTP error response. In this case, you should redirect the user to your SPA's login page. -->
もちろん、アクティビティがないためにユーザーのセッションが期限切れになった場合、Laravel アプリケーションへの後続のリクエストは 401 または 419 HTTP エラー応答を受け取る可能性があります。この場合、ユーザーを SPA のログイン ページにリダイレクトする必要があります。

> [!NOTE]
> 独自の `/login` エンドポイントを自由に作成できます。ただし、標準の [session based authentication services that Laravel provides](/docs/8.x/authentication#authenticating-users) を使用してユーザーを認証することを確認する必要があります。通常、これは、`web` 認証ガードを使用することを意味します。

<a name="protecting-spa-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To protect routes so that all incoming requests must be authenticated, you should attach the `sanctum` authentication guard to your API routes within your `routes/api.php` file. This guard will ensure that incoming requests are authenticated as either a stateful authenticated requests from your SPA or contain a valid API token header if the request is from a third party: -->
すべての受信リクエストを認証する必要があるようにルートを保護するには、`routes/api.php` ファイル内の API ルートに `sanctum` 認証ガードをアタッチする必要があります。このガードにより、受信リクエストが SPA からのステートフルな認証済みリクエストとして認証されるか、リクエストがサードパーティからのものである場合は有効な API トークン ヘッダーが含まれることが保証されます。

```
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="authorizing-private-broadcast-channels"></a>
<!-- ### Authorizing Private Broadcast Channels -->
### Authorizing Private Broadcast Channels

<!-- If your SPA needs to authenticate with [private / presence broadcast channels](/docs/8.x/broadcasting#authorizing-channels), you should place the `Broadcast::routes` method call within your `routes/api.php` file: -->
SPA が [private / presence broadcast channels](/docs/8.x/broadcasting#authorizing-channels) で認証する必要がある場合は、`routes/api.php` ファイル内に `Broadcast::routes` メソッド呼び出しを配置する必要があります。

```
Broadcast::routes(['middleware' => ['auth:sanctum']]);
```

<!-- Next, in order for Pusher's authorization requests to succeed, you will need to provide a custom Pusher `authorizer` when initializing [Laravel Echo](/docs/8.x/broadcasting#client-side-installation). This allows your application to configure Pusher to use the `axios` instance that is [properly configured for cross-domain requests](#cors-and-cookies): -->
次に、プッシャーの認証リクエストを成功させるには、[Laravel Echo](/docs/8.x/broadcasting#client-side-installation) を初期化するときにカスタム プッシャー `authorizer` を指定する必要があります。これにより、アプリケーションで `axios` インスタンス ([properly configured for cross-domain requests](#cors-and-cookies)) を使用するようにプッシャーを構成できるようになります。

```
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: process.env.MIX_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: process.env.MIX_PUSHER_APP_KEY,
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
<!-- ## Mobile Application Authentication -->
## Mobile Application Authentication

<!-- You may also use Sanctum tokens to authenticate your mobile application's requests to your API. The process for authenticating mobile application requests is similar to authenticating third-party API requests; however, there are small differences in how you will issue the API tokens. -->
Sanctum トークンを使用して、モバイル アプリケーションの API へのリクエストを認証することもできます。モバイル アプリケーション リクエストを認証するプロセスは、サードパーティ API リクエストを認証するプロセスと似ています。ただし、API トークンの発行方法には若干の違いがあります。

<a name="issuing-mobile-api-tokens"></a>
<!-- ### Issuing API Tokens -->
### Issuing API Tokens

<!-- To get started, create a route that accepts the user's email / username, password, and device name, then exchanges those credentials for a new Sanctum token. The "device name" given to this endpoint is for informational purposes and may be any value you wish. In general, the device name value should be a name the user would recognize, such as "Nuno's iPhone 12". -->
まず、ユーザーの電子メール/ユーザー名、パスワード、デバイス名を受け入れるルートを作成し、それらの資格情報を新しい Sanctum トークンと交換します。このエンドポイントに与えられる「デバイス名」は情報提供を目的としており、任意の値を指定できます。一般に、デバイス名の値は、「Nuno's iPhone 12」など、ユーザーが認識できる名前にする必要があります。

<!-- Typically, you will make a request to the token endpoint from your mobile application's "login" screen. The endpoint will return the plain-text API token which may then be stored on the mobile device and used to make additional API requests: -->
通常、モバイル アプリケーションの「ログイン」画面からトークン エンドポイントにリクエストを送信します。エンドポイントはプレーンテキストの API トークンを返します。このトークンはモバイル デバイスに保存され、追加の API リクエストを行うために使用されます。

```
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

<!-- When the mobile application uses the token to make an API request to your application, it should pass the token in the `Authorization` header as a `Bearer` token. -->
モバイル アプリケーションがトークンを使用してアプリケーションに API リクエストを行う場合、`Authorization` ヘッダー内のトークンを `Bearer` トークンとして渡す必要があります。

> [!TIP]
> モバイル アプリケーションのトークンを発行する場合、[token abilities](#token-abilities) を自由に指定することもできます。

<a name="protecting-mobile-api-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- As previously documented, you may protect routes so that all incoming requests must be authenticated by attaching the `sanctum` authentication guard to the routes: -->
前に説明したように、`sanctum` 認証ガードをルートにアタッチすることで、すべての受信リクエストが認証される必要があるようにルートを保護できます。

```
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
```

<a name="revoking-mobile-api-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- To allow users to revoke API tokens issued to mobile devices, you may list them by name, along with a "Revoke" button, within an "account settings" portion of your web application's UI. When the user clicks the "Revoke" button, you can delete the token from the database. Remember, you can access a user's API tokens via the `tokens` relationship provided by the `Laravel\Sanctum\HasApiTokens` trait: -->
ユーザーがモバイル デバイスに発行された API トークンを取り消すことができるようにするには、Web アプリケーションの UI の「アカウント設定」部分内で、「取り消し」ボタンとともに名前でリストすることができます。ユーザーが「取り消し」ボタンをクリックすると、データベースからトークンを削除できます。 `Laravel\Sanctum\HasApiTokens` トレイトによって提供される `tokens` 関係を介してユーザーの API トークンにアクセスできることを覚えておいてください。

```
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- While testing, the `Sanctum::actingAs` method may be used to authenticate a user and specify which abilities should be granted to their token: -->
テスト中に、`Sanctum::actingAs` メソッドを使用してユーザーを認証し、トークンにどの能力を付与するかを指定できます。

```
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved()
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```

<!-- If you would like to grant all abilities to the token, you should include `*` in the ability list provided to the `actingAs` method: -->
トークンにすべての能力を付与したい場合は、`actingAs` メソッドに提供される能力リストに `*` を含める必要があります。

```
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```

