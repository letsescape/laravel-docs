<!-- # Laravel Passport -->
# Laravel Passport

- [Introduction](#introduction)
    - [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
    - [Overriding Routes](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Managing Tokens](#managing-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [Creating the Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Creating a Device Code Grant Client](#creating-a-device-authorization-grant-client)
    - [Requesting Tokens](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Creating a Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing the User Provider](#customizing-the-user-provider)
    - [Customizing the Username Field](#customizing-the-username-field)
    - [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating a Personal Access Client](#creating-a-personal-access-client)
    - [Customizing the User Provider](#customizing-the-user-provider-for-pat)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [SPA Authentication](#spa-authentication)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp. -->
[Laravel Passport](https://github.com/laravel/passport) は、Laravel アプリケーションに完全な OAuth2 サーバー実装を数分で提供します。Passportは、Andy Millington と Simon Hamp によって保守されている [League OAuth2 server](https://github.com/thephpleague/oauth2-server) の上に構築されています。

> [!NOTE]
> このドキュメントは、OAuth2 についてすでに理解していることを前提としています。 OAuth2 について何も知らない場合は、続行する前に、一般的な [terminology](https://oauth2.thephpleague.com/terminology/) と OAuth2 の機能についてよく理解しておくことを検討してください。

<a name="passport-or-sanctum"></a>
<!-- ### Passport or Sanctum? -->
### Passport or Sanctum?

<!-- Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/12.x/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport. -->
始める前に、アプリケーションが Laravel Passport と [Laravel Sanctum](/docs/12.x/sanctum) のどちらの方が適切に提供されるかを判断したい場合があります。アプリケーションが OAuth2 をサポートする必要がある場合は、Laravel Passport を使用する必要があります。

<!-- However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/12.x/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience. -->
ただし、シングルページ アプリケーション、モバイル アプリケーションを認証しようとする場合、または API トークンを発行しようとする場合は、[Laravel Sanctum](/docs/12.x/sanctum) を使用する必要があります。 Laravel Sanctum は OAuth2 をサポートしていません。ただし、よりシンプルな API 認証開発エクスペリエンスが提供されます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may install Laravel Passport via the `install:api` Artisan command: -->
Laravel Passport は、`install:api` Artisan コマンドを使用してインストールできます。

```shell
php artisan install:api --passport
```

<!-- This command will publish and run the database migrations necessary for creating the tables your application needs to store OAuth2 clients and access tokens. The command will also create the encryption keys required to generate secure access tokens. -->
このコマンドは、アプリケーションが OAuth2 クライアントとアクセス トークンを保存するために必要なテーブルを作成するために必要なデータベース移行を公開し、実行します。このコマンドは、安全なアクセス トークンを生成するために必要な暗号化キーも作成します。

<!-- After running the `install:api` command, add the `Laravel\Passport\HasApiTokens` trait and `Laravel\Passport\Contracts\OAuthenticatable` interface to your `App\Models\User` model. This trait will provide a few helper methods to your model which allow you to inspect the authenticated user's token and scopes: -->
`install:api` コマンドを実行した後、`Laravel\Passport\HasApiTokens` 特性と `Laravel\Passport\Contracts\OAuthenticatable` インターフェイスを `App\Models\User` モデルに追加します。この特性は、認証されたユーザーのトークンとスコープを検査できるようにするいくつかのヘルパ メソッドをモデルに提供します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```

<!-- Finally, in your application's `config/auth.php` configuration file, you should define an `api` authentication guard and set the `driver` option to `passport`. This will instruct your application to use Passport's `TokenGuard` when authenticating incoming API requests: -->
最後に、アプリケーションの `config/auth.php` 構成ファイルで、`api` 認証ガードを定義し、`driver` オプションを `passport` に設定する必要があります。これにより、受信 API リクエストを認証するときに Passport の `TokenGuard` を使用するようにアプリケーションに指示されます。

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```

<a name="deploying-passport"></a>
<!-- ### Deploying Passport -->
### Deploying Passport

<!-- When deploying Passport to your application's servers for the first time, you will likely need to run the `passport:keys` command. This command generates the encryption keys Passport needs in order to generate access tokens. The generated keys are not typically kept in source control: -->
Passport をアプリケーションのサーバーに初めてデプロイするときは、おそらく `passport:keys` コマンドを実行する必要があります。このコマンドは、Passportがアクセス トークンを生成するために必要な暗号化キーを生成します。生成されたキーは通常、ソース管理に保持されません。

```shell
php artisan passport:keys
```

<!-- If necessary, you may define the path where Passport's keys should be loaded from. You may use the `Passport::loadKeysFrom` method to accomplish this. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
必要に応じて、Passport のキーのロード元となるパスを定義できます。これを実現するには、`Passport::loadKeysFrom` メソッドを使用できます。通常、このメソッドは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```

<a name="loading-keys-from-the-environment"></a>
<!-- #### Loading Keys From the Environment -->
#### Loading Keys From the Environment

<!-- Alternatively, you may publish Passport's configuration file using the `vendor:publish` Artisan command: -->
あるいは、`vendor:publish` Artisan コマンドを使用して、Passport の構成ファイルを公開することもできます。

```shell
php artisan vendor:publish --tag=passport-config
```

<!-- After the configuration file has been published, you may load your application's encryption keys by defining them as environment variables: -->
構成ファイルが公開された後、アプリケーションの暗号化キーを環境変数として定義してロードできます。

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="upgrading-passport"></a>
<!-- ### Upgrading Passport -->
### Upgrading Passport

<!-- When upgrading to a new major version of Passport, it's important that you carefully review [the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md). -->
Passport の新しいメジャー バージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/passport/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<a name="token-lifetimes"></a>
<!-- ### Token Lifetimes -->
### Token Lifetimes

<!-- By default, Passport issues long-lived access tokens that expire after one year. If you would like to configure a longer / shorter token lifetime, you may use the `tokensExpireIn`, `refreshTokensExpireIn`, and `personalAccessTokensExpireIn` methods. These methods should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
デフォルトでは、Passport は 1 年後に期限切れになる長期間のアクセス トークンを発行します。トークンの有効期間を長く/短く設定したい場合は、`tokensExpireIn`、`refreshTokensExpireIn`、および `personalAccessTokensExpireIn` メソッドを使用できます。これらのメソッドは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```

> [!WARNING]
> Passport のデータベース テーブルの `expires_at` 列は読み取り専用で、表示のみを目的としています。トークンを発行するとき、Passport は署名され暗号化されたトークン内に有効期限情報を保存します。トークンを無効にする必要がある場合は、[revoke it](#revoking-tokens) を実行する必要があります。

<a name="overriding-default-models"></a>
<!-- ### Overriding Default Models -->
### Overriding Default Models

<!-- You are free to extend the models used internally by Passport by defining your own model and extending the corresponding Passport model: -->
独自のモデルを定義し、対応する Passport モデルを拡張することで、Passport が内部で使用するモデルを自由に拡張できます。

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```

<!-- After defining your model, you may instruct Passport to use your custom model via the `Laravel\Passport\Passport` class. Typically, you should inform Passport about your custom models in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
モデルを定義した後、`Laravel\Passport\Passport` クラスを介してカスタム モデルを使用するように Passport に指示できます。通常、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Passport に通知する必要があります。

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```

<a name="overriding-routes"></a>
<!-- ### Overriding Routes -->
### Overriding Routes

<!-- Sometimes you may wish to customize the routes defined by Passport. To achieve this, you first need to ignore the routes registered by Passport by adding `Passport::ignoreRoutes` to the `register` method of your application's `AppServiceProvider`: -->
場合によっては、Passport で定義されたルートをカスタマイズしたい場合があります。これを実現するには、まずアプリケーションの `AppServiceProvider` の `register` メソッドに `Passport::ignoreRoutes` を追加して、Passport によって登録されたルートを無視する必要があります。

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```

<!-- Then, you may copy the routes defined by Passport in [its routes file](https://github.com/laravel/passport/blob/master/routes/web.php) to your application's `routes/web.php` file and modify them to your liking: -->
次に、[its routes file](https://github.com/laravel/passport/blob/master/routes/web.php) の Passport で定義されたルートをアプリケーションの `routes/web.php` ファイルにコピーし、好みに合わせて変更します。

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```

<a name="authorization-code-grant"></a>
<!-- ## Authorization Code Grant -->
## Authorization Code Grant

<!-- Using OAuth2 via authorization codes is how most developers are familiar with OAuth2. When using authorization codes, a client application will redirect a user to your server where they will either approve or deny the request to issue an access token to the client. -->
認証コードを介して OAuth2 を使用することは、ほとんどの開発者が OAuth2 に慣れている方法です。認証コードを使用する場合、クライアント アプリケーションはユーザーをサーバーにリダイレクトし、そこでユーザーはクライアントにアクセス トークンを発行するリクエストを承認または拒否します。

<!-- To get started, we need to instruct Passport how to return our "authorization" view. -->
まず、「認証」ビューを返す方法を Passport に指示する必要があります。

<!-- All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
すべての認可ビューのレンダリング ロジックは、`Laravel\Passport\Passport` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::authorizationView('auth.oauth.authorize');

    // By providing a closure...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```

<!-- Passport will automatically define the `/oauth/authorize` route that returns this view. Your `auth.oauth.authorize` template should include a form that makes a POST request to the `passport.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.authorizations.deny` route to deny the authorization. The `passport.authorizations.approve` and `passport.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields. -->
Passportは、このビューを返す `/oauth/authorize` ルートを自動的に定義します。 `auth.oauth.authorize` テンプレートには、認可を承認するために `passport.authorizations.approve` ルートに POST リクエストを行うフォームと、認可を拒否するために `passport.authorizations.deny` ルートに DELETE リクエストを行うフォームが含まれている必要があります。 `passport.authorizations.approve` および `passport.authorizations.deny` ルートは、`state`、`client_id`、および `auth_token` フィールドを予期します。

<a name="managing-clients"></a>
<!-- ### Managing Clients -->
### Managing Clients

<!-- Developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URI that your application can redirect to after users approve their request for authorization. -->
アプリケーションの API と対話する必要があるアプリケーションを構築する開発者は、「クライアント」を作成して、アプリケーションをあなたのアプリケーションに登録する必要があります。通常、これは、アプリケーションの名前と、ユーザーが承認リクエストを承認した後にアプリケーションがリダイレクトできる URI を提供することで構成されます。

<a name="managing-first-party-clients"></a>
<!-- #### First-Party Clients -->
#### First-Party Clients

<!-- The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create first-party clients or testing your OAuth2 functionality. When you run the `passport:client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret: -->
クライアントを作成する最も簡単な方法は、`passport:client` Artisan コマンドを使用することです。このコマンドは、ファーストパーティ クライアントの作成や OAuth2 機能のテストに使用できます。 `passport:client` コマンドを実行すると、Passport はクライアントに関する詳細情報の入力を求め、クライアント ID とシークレットを提供します。

```shell
php artisan passport:client
```

<!-- If you would like to allow multiple redirect URIs for your client, you may specify them using a comma-delimited list when prompted for the URI by the `passport:client` command. Any URIs which contain commas should be URI encoded: -->
クライアントに複数のリダイレクト URI を許可する場合は、`passport:client` コマンドによって URI の入力を求められたときに、カンマ区切りのリストを使用してそれらを指定できます。カンマを含む URI はすべて URI エンコードする必要があります。

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```

<a name="managing-third-party-clients"></a>
<!-- #### Third-Party Clients -->
#### Third-Party Clients

<!-- Since your application's users will not be able to utilize the `passport:client` command, you may use `createAuthorizationCodeGrantClient` method of the `Laravel\Passport\ClientRepository` class to register a client for a given user: -->
アプリケーションのユーザーは `passport:client` コマンドを利用できないため、`Laravel\Passport\ClientRepository` クラスの `createAuthorizationCodeGrantClient` メソッドを使用して、特定のユーザーのクライアントを登録できます。

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// Creating an OAuth app client that belongs to the given user...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// Retrieving all the OAuth app clients that belong to the user...
$clients = $user->oauthApps()->get();
```

<!-- The `createAuthorizationCodeGrantClient` method returns an instance of `Laravel\Passport\Client`. You may display the `$client->id` as the client ID and `$client->plainSecret` as the client secret to the user. -->
`createAuthorizationCodeGrantClient` メソッドは、`Laravel\Passport\Client` のインスタンスを返します。ユーザーに対して、クライアント ID として `$client->id` を表示し、クライアント シークレットとして `$client->plainSecret` を表示できます。

<a name="requesting-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="requesting-tokens-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, developers may use their client ID and secret to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
クライアントが作成されると、開発者はクライアント ID とシークレットを使用して、アプリケーションから認証コードとアクセス トークンをリクエストできます。まず、使用側アプリケーションは、次のようにアプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<!-- The `prompt` parameter may be used to specify the authentication behavior of the Passport application. -->
`prompt` パラメータは、Passport アプリケーションの認証動作を指定するために使用できます。

<!-- If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session. -->
`prompt` 値が `none` の場合、ユーザーが Passport アプリケーションでまだ認証されていない場合、Passport は常に認証エラーをスローします。値が `consent` の場合、すべてのスコープが使用側アプリケーションに以前に付与されていたとしても、Passport は常に認証承認画面を表示します。値が `login` の場合、Passport アプリケーションは、ユーザーがすでに既存のセッションを持っている場合でも、常にユーザーにアプリケーションへの再ログインを要求します。

<!-- If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes. -->
`prompt` 値が指定されていない場合、ユーザーは、要求されたスコープの使用アプリケーションへのアクセスを以前に承認していない場合にのみ、承認を求められます。

> [!NOTE]
> `/oauth/authorize` ルートは Passport によってすでに定義されていることに注意してください。このルートを手動で定義する必要はありません。

<a name="approving-the-request"></a>
<!-- #### Approving the Request -->
#### Approving the Request

<!-- When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created. -->
認証リクエストを受信すると、Passport は `prompt` パラメータ (存在する場合) の値に基づいて自動的に応答し、ユーザーに認証リクエストを承認または拒否できるテンプレートを表示する場合があります。リクエストを承認すると、使用側アプリケーションによって指定された `redirect_uri` にリダイレクトされます。 `redirect_uri` は、クライアントの作成時に指定された `redirect` URL と一致する必要があります。

<!-- Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization: -->
ファーストパーティクライアントを認証する場合など、認証プロンプトをスキップしたい場合があります。これは、[extending the `Client` model](#overriding-default-models) と `skipsAuthorization` メソッドを定義することで実現できます。 `skipsAuthorization` が `true` を返した場合、クライアントは承認され、ユーザーはすぐに `redirect_uri` にリダイレクトされます。 ただし、使用側アプリケーションが承認のためにリダイレクトするときに `prompt` パラメーターを明示的に設定していない限り、次のようになります。

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should first verify the `state` parameter against the value that was stored prior to the redirect. If the state parameter matches then the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request: -->
ユーザーが認可リクエストを承認すると、ユーザーは使用側アプリケーションにリダイレクトされます。コンシューマは、まず `state` パラメータを、リダイレクト前に保存された値と比較して検証する必要があります。状態パラメータが一致する場合、コンシューマはアプリケーションに `POST` リクエストを発行して、アクセス トークンをリクエストする必要があります。リクエストには、ユーザーが認可リクエストを承認したときにアプリケーションによって発行された認可コードが含まれている必要があります。

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
この `/oauth/token` ルートは、`access_token`、`refresh_token`、および `expires_in` 属性を含む JSON 応答を返します。 `expires_in` 属性には、アクセス トークンの有効期限が切れるまでの秒数が含まれます。

> [!NOTE]
> `/oauth/authorize` ルートと同様に、`/oauth/token` ルートは Passport によって定義されます。このルートを手動で定義する必要はありません。

<a name="managing-tokens"></a>
<!-- ### Managing Tokens -->
### Managing Tokens

<!-- You may retrieve user's authorized tokens using the `tokens` method of the `Laravel\Passport\HasApiTokens` trait. For example, this may be used to offer your users a dashboard to keep track of their connections with third-party applications: -->
`Laravel\Passport\HasApiTokens` トレイトの `tokens` メソッドを使用して、ユーザーの許可されたトークンを取得できます。たとえば、これは、サードパーティ アプリケーションとの接続を追跡するためのダッシュボードをユーザーに提供するために使用できます。

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Retrieving all of the valid tokens for the user...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// Retrieving all the user's connections to third-party OAuth app clients...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```

<a name="refreshing-tokens"></a>
<!-- ### Refreshing Tokens -->
### Refreshing Tokens

<!-- If your application issues short-lived access tokens, users will need to refresh their access tokens via the refresh token that was provided to them when the access token was issued: -->
アプリケーションが有効期間の短いアクセス トークンを発行する場合、ユーザーは、アクセス トークンの発行時に提供された更新トークンを使用してアクセス トークンを更新する必要があります。

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

<!-- This `/oauth/token` route will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
この `/oauth/token` ルートは、`access_token`、`refresh_token`、および `expires_in` 属性を含む JSON 応答を返します。 `expires_in` 属性には、アクセス トークンの有効期限が切れるまでの秒数が含まれます。

<a name="revoking-tokens"></a>
<!-- ### Revoking Tokens -->
### Revoking Tokens

<!-- You may revoke a token by using the `revoke` method on the `Laravel\Passport\Token` model. You may revoke a token's refresh token using the `revoke` method on the `Laravel\Passport\RefreshToken` model: -->
`Laravel\Passport\Token` モデルで `revoke` メソッドを使用して、トークンを取り消すことができます。 `Laravel\Passport\RefreshToken` モデルで `revoke` メソッドを使用して、トークンのリフレッシュ トークンを取り消すことができます。

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Revoke an access token...
$token->revoke();

// Revoke the token's refresh token...
$token->refreshToken?->revoke();

// Revoke all of the user's tokens...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```

<a name="purging-tokens"></a>
<!-- ### Purging Tokens -->
### Purging Tokens

<!-- When tokens have been revoked or expired, you might want to purge them from the database. Passport's included `passport:purge` Artisan command can do this for you: -->
トークンが取り消されたり期限切れになったりした場合、データベースからトークンを削除することができます。Passportに含まれている `passport:purge` Artisan コマンドを使用すると、次のことができます。

```shell
# Purge revoked and expired tokens, auth codes, and device codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens, auth codes, and device codes...
php artisan passport:purge --revoked

# Only purge expired tokens, auth codes, and device codes...
php artisan passport:purge --expired
```

<!-- You may also configure a [scheduled job](/docs/12.x/scheduling) in your application's `routes/console.php` file to automatically prune your tokens on a schedule: -->
アプリケーションの `routes/console.php` ファイルで [scheduled job](/docs/12.x/scheduling) を構成して、スケジュールに従ってトークンを自動的にプルーニングすることもできます。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```

<a name="code-grant-pkce"></a>
<!-- ## Authorization Code Grant With PKCE -->
## Authorization Code Grant With PKCE

<!-- The Authorization Code grant with "Proof Key for Code Exchange" (PKCE) is a secure way to authenticate single page applications or mobile applications to access your API. This grant should be used when you can't guarantee that the client secret will be stored confidentially or in order to mitigate the threat of having the authorization code intercepted by an attacker. A combination of a "code verifier" and a "code challenge" replaces the client secret when exchanging the authorization code for an access token. -->
「Proof Key for Code Exchange」(PKCE) を使用した認証コード付与は、シングル ページ アプリケーションまたはモバイル アプリケーションが API にアクセスすることを認証するための安全な方法です。この許可は、クライアント シークレットが機密で保存されることが保証できない場合、または攻撃者によって認証コードが傍受される脅威を軽減するために使用する必要があります。 「コードベリファイア」と「コードチャレンジ」の組み合わせは、アクセストークンの認可コードを交換するときにクライアントシークレットを置き換えます。

<a name="creating-a-auth-pkce-grant-client"></a>
<!-- ### Creating the Client -->
### Creating the Client

<!-- Before your application can issue tokens via the authorization code grant with PKCE, you will need to create a PKCE-enabled client. You may do this using the `passport:client` Artisan command with the `--public` option: -->
アプリケーションが PKCE を使用して認証コードグラント経由でトークンを発行できるようにするには、PKCE 対応クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--public` オプションを指定します。

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="code-verifier-code-challenge"></a>
<!-- #### Code Verifier and Code Challenge -->
#### Code Verifier and Code Challenge

<!-- As this authorization grant does not provide a client secret, developers will need to generate a combination of a code verifier and a code challenge in order to request a token. -->
この認可付与ではクライアント シークレットが提供されないため、開発者はトークンを要求するためにコード検証ツールとコード チャレンジの組み合わせを生成する必要があります。

<!-- The code verifier should be a random string of between 43 and 128 characters containing letters, numbers, and  `"-"`, `"."`, `"_"`, `"~"` characters, as defined in the [RFC 7636 specification](https://tools.ietf.org/html/rfc7636). -->
コード検証子は、[RFC 7636 specification](https://tools.ietf.org/html/rfc7636) で定義されているように、文字、数字、および `"-"`、`"."`、`"_"`、`"~"` 文字を含む 43 ～ 128 文字のランダムな文字列である必要があります。

<!-- The code challenge should be a Base64 encoded string with URL and filename-safe characters. The trailing `'='` characters should be removed and no line breaks, whitespace, or other additional characters should be present. -->
コード チャレンジは、URL とファイル名に安全な文字を含む Base64 でエンコードされた文字列である必要があります。末尾の `'='` 文字は削除する必要があり、改行、空白、その他の追加文字が存在しないようにする必要があります。

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```

<a name="code-grant-pkce-redirecting-for-authorization"></a>
<!-- #### Redirecting for Authorization -->
#### Redirecting for Authorization

<!-- Once a client has been created, you may use the client ID and the generated code verifier and code challenge to request an authorization code and access token from your application. First, the consuming application should make a redirect request to your application's `/oauth/authorize` route: -->
クライアントが作成されたら、クライアント ID と生成されたコード検証ツールおよびコード チャレンジを使用して、アプリケーションから認証コードとアクセス トークンをリクエストできます。まず、使用側アプリケーションは、アプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
<!-- #### Converting Authorization Codes to Access Tokens -->
#### Converting Authorization Codes to Access Tokens

<!-- If the user approves the authorization request, they will be redirected back to the consuming application. The consumer should verify the `state` parameter against the value that was stored prior to the redirect, as in the standard Authorization Code Grant. -->
ユーザーが認可リクエストを承認すると、ユーザーは使用側アプリケーションにリダイレクトされます。コンシューマは、標準の認可コード付与と同様に、リダイレクト前に保存された値に対して `state` パラメータを検証する必要があります。

<!-- If the state parameter matches, the consumer should issue a `POST` request to your application to request an access token. The request should include the authorization code that was issued by your application when the user approved the authorization request along with the originally generated code verifier: -->
状態パラメータが一致する場合、コンシューマはアプリケーションに `POST` リクエストを発行して、アクセス トークンをリクエストする必要があります。リクエストには、ユーザーが認可リクエストを承認したときにアプリケーションによって発行された認可コードと、最初に生成されたコードベリファイアが含まれている必要があります。

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```

<a name="device-authorization-grant"></a>
<!-- ## Device Authorization Grant -->
## Device Authorization Grant

<!-- The OAuth2 device authorization grant allows browserless or limited input devices, such as TVs and game consoles, to obtain an access token by exchanging a "device code". When using device flow, the device client will instruct the user to use a secondary device, such as a computer or a smartphone and connect to your server where they will enter the provided "user code" and either approve or deny the access request. -->
OAuth2 デバイス認証許可により、テレビやゲーム機などのブラウザレスまたは制限された入力デバイスが「デバイス コード」を交換することでアクセス トークンを取得できるようになります。デバイス フローを使用する場合、デバイス クライアントはユーザーに、コンピューターやスマートフォンなどのセカンダリ デバイスを使用してサーバーに接続し、提供された「ユーザー コード」を入力してアクセス要求を承認または拒否するように指示します。

<!-- To get started, we need to instruct Passport how to return our "user code" and "authorization" views. -->
まず、「ユーザー コード」ビューと「認証」ビューを返す方法を Passport に指示する必要があります。

<!-- All the authorization view's rendering logic may be customized using the appropriate methods available via the `Laravel\Passport\Passport` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class. -->
すべての認可ビューのレンダリング ロジックは、`Laravel\Passport\Passport` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドはアプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // By providing a closure...
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```

<!-- Passport will automatically define routes that return these views. Your `auth.oauth.device.user-code` template should include a form that makes a GET request to the `passport.device.authorizations.authorize` route. The `passport.device.authorizations.authorize` route expects a `user_code` query parameter. -->
Passportは、これらのビューを返すルートを自動的に定義します。 `auth.oauth.device.user-code` テンプレートには、`passport.device.authorizations.authorize` ルートへの GET リクエストを行うフォームが含まれている必要があります。 `passport.device.authorizations.authorize` ルートには、`user_code` クエリ パラメーターが必要です。

<!-- Your `auth.oauth.device.authorize` template should include a form that makes a POST request to the `passport.device.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.device.authorizations.deny` route to deny the authorization. The `passport.device.authorizations.approve` and `passport.device.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields. -->
`auth.oauth.device.authorize` テンプレートには、認可を承認するために `passport.device.authorizations.approve` ルートに POST リクエストを行うフォームと、認可を拒否するために `passport.device.authorizations.deny` ルートに DELETE リクエストを行うフォームが含まれている必要があります。 `passport.device.authorizations.approve` および `passport.device.authorizations.deny` ルートは、`state`、`client_id`、および `auth_token` フィールドを予期します。

<a name="creating-a-device-authorization-grant-client"></a>
<!-- ### Creating a Device Authorization Grant Client -->
### Creating a Device Authorization Grant Client

<!-- Before your application can issue tokens via the device authorization grant, you will need to create a device flow enabled client. You may do this using the `passport:client` Artisan command with the `--device` option. This command will create a first-party device flow enabled client and provide you with a client ID and secret: -->
アプリケーションがデバイス認証許可を通じてトークンを発行できるようにするには、デバイス フロー対応クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--device` オプションを指定します。このコマンドは、ファーストパーティのデバイス フロー対応クライアントを作成し、クライアント ID とシークレットを提供します。

```shell
php artisan passport:client --device
```

<!-- Additionally, you may use `createDeviceAuthorizationGrantClient` method on the `ClientRepository` class to register a third-party client that belongs to the given user: -->
さらに、`ClientRepository` クラスの `createDeviceAuthorizationGrantClient` メソッドを使用して、指定されたユーザーに属するサードパーティ クライアントを登録することもできます。

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```

<a name="requesting-device-authorization-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<a name="device-code"></a>
<!-- #### Requesting a Device Code -->
#### Requesting a Device Code

<!-- Once a client has been created, developers may use their client ID to request a device code from your application. First, the consuming device should make a `POST` request to your application's `/oauth/device/code` route to request a device code: -->
クライアントが作成されると、開発者はクライアント ID を使用してアプリケーションからデバイス コードをリクエストできます。まず、使用側デバイスは、アプリケーションの `/oauth/device/code` ルートに対して `POST` リクエストを作成して、デバイス コードをリクエストする必要があります。

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

<!-- This will return a JSON response containing `device_code`, `user_code`, `verification_uri`, `interval`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the device code expires. The `interval` attribute contains the number of seconds the consuming device should wait between requests when polling `/oauth/token` route to avoid rate limit errors. -->
これにより、`device_code`、`user_code`、`verification_uri`、`interval`、および `expires_in` 属性を含む JSON 応答が返されます。 `expires_in` 属性には、デバイス コードの有効期限が切れるまでの秒数が含まれます。 `interval` 属性には、レート制限エラーを回避するために `/oauth/token` ルートをポーリングするときに、消費デバイスがリクエスト間で待機する秒数が含まれています。

> [!NOTE]
> `/oauth/device/code` ルートは Passport によってすでに定義されていることに注意してください。このルートを手動で定義する必要はありません。

<a name="user-code"></a>
<!-- #### Displaying the Verification URI and User Code -->
#### Displaying the Verification URI and User Code

<!-- Once a device code request has been obtained, the consuming device should instruct the user to use another device and visit the provided `verification_uri` and enter the `user_code` in order to approve the authorization request. -->
デバイス コード リクエストを取得したら、消費デバイスは、別のデバイスを使用し、提供された `verification_uri` にアクセスして `user_code` を入力して認証リクエストを承認するようにユーザーに指示する必要があります。

<a name="polling-token-request"></a>
<!-- #### Polling Token Request -->
#### Polling Token Request

<!-- Since the user will be using a separate device to grant (or deny) access, the consuming device should poll your application's `/oauth/token` route to determine when the user has responded to the request. The consuming device should use the minimum polling `interval` provided in the JSON response when requesting device code to avoid rate limit errors: -->
ユーザーはアクセスを許可 (または拒否) するために別のデバイスを使用するため、使用側デバイスはアプリケーションの `/oauth/token` ルートをポーリングして、ユーザーがリクエストにいつ応答したかを判断する必要があります。使用側デバイスは、レート制限エラーを回避するために、デバイス コードを要求するときに、JSON 応答で提供される最小ポーリング `interval` を使用する必要があります。

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```

<!-- If the user has approved the authorization request, this will return a JSON response containing `access_token`, `refresh_token`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the access token expires. -->
ユーザーが承認リクエストを承認した場合、`access_token`、`refresh_token`、および `expires_in` 属性を含む JSON 応答が返されます。 `expires_in` 属性には、アクセス トークンの有効期限が切れるまでの秒数が含まれます。

<a name="password-grant"></a>
<!-- ## Password Grant -->
## Password Grant

> [!WARNING]
> パスワード付与トークンの使用は推奨されなくなりました。代わりに、[a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/) を選択する必要があります。

<!-- The OAuth2 password grant allows your other first-party clients, such as a mobile application, to obtain an access token using an email address / username and password. This allows you to issue access tokens securely to your first-party clients without requiring your users to go through the entire OAuth2 authorization code redirect flow. -->
OAuth2 パスワード付与により、モバイル アプリケーションなどの他のファーストパーティ クライアントが、電子メール アドレス/ユーザー名とパスワードを使用してアクセス トークンを取得できるようになります。これにより、ユーザーが OAuth2 認証コード リダイレクト フロー全体を実行する必要がなく、ファーストパーティ クライアントにアクセス トークンを安全に発行できます。

<!-- To enable the password grant, call the `enablePasswordGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
パスワード付与を有効にするには、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドで `enablePasswordGrant` メソッドを呼び出します。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="creating-a-password-grant-client"></a>
<!-- ### Creating a Password Grant Client -->
### Creating a Password Grant Client

<!-- Before your application can issue tokens via the password grant, you will need to create a password grant client. You may do this using the `passport:client` Artisan command with the `--password` option. -->
アプリケーションがパスワード付与を通じてトークンを発行できるようにするには、パスワード付与クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--password` オプションを指定します。

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
<!-- ### Requesting Tokens -->
### Requesting Tokens

<!-- Once you have enabled the grant and have created a password grant client, you may request an access token by issuing a `POST` request to the `/oauth/token` route with the user's email address and password. Remember, this route is already registered by Passport so there is no need to define it manually. If the request is successful, you will receive an `access_token` and `refresh_token` in the JSON response from the server: -->
付与を有効にしてパスワード付与クライアントを作成したら、ユーザーの電子メール アドレスとパスワードを使用して `POST` リクエストを `/oauth/token` ルートに発行して、アクセス トークンをリクエストできます。このルートは Passport によってすでに登録されているため、手動で定義する必要がないことに注意してください。リクエストが成功すると、サーバーからの JSON レスポンスで `access_token` および `refresh_token` を受け取ります。

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```

> [!NOTE]
> アクセス トークンはデフォルトで長期間有効であることに注意してください。ただし、必要に応じて自由に [configure your maximum access token lifetime](#configuration) を実行できます。

<a name="requesting-all-scopes"></a>
<!-- ### Requesting All Scopes -->
### Requesting All Scopes

<!-- When using the password grant or client credentials grant, you may wish to authorize the token for all of the scopes supported by your application. You can do this by requesting the `*` scope. If you request the `*` scope, the `can` method on the token instance will always return `true`. This scope may only be assigned to a token that is issued using the `password` or `client_credentials` grant: -->
パスワード付与またはクライアント資格情報付与を使用する場合、アプリケーションでサポートされているすべてのスコープに対してトークンを承認したい場合があります。これを行うには、`*` スコープをリクエストします。 `*` スコープをリクエストした場合、トークン インスタンスの `can` メソッドは常に `true` を返します。このスコープは、`password` または `client_credentials` 付与を使用して発行されたトークンにのみ割り当てることができます。

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```

<a name="customizing-the-user-provider"></a>
<!-- ### Customizing the User Provider -->
### Customizing the User Provider

<!-- If your application uses more than one [authentication user provider](/docs/12.x/authentication#introduction), you may specify which user provider the password grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --password` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized. -->
アプリケーションが複数の [authentication user provider](/docs/12.x/authentication#introduction) を使用する場合、`artisan passport:client --password` コマンドでクライアントを作成するときに `--provider` オプションを指定することで、パスワード付与クライアントが使用するユーザー プロバイダを指定できます。指定されたプロバイダ名は、アプリケーションの `config/auth.php` 構成ファイルで定義されている有効なプロバイダと一致する必要があります。その後、[protect your route using middleware](#multiple-authentication-guards) を実行して、ガードの指定されたプロバイダのユーザーのみが承認されるようにすることができます。

<a name="customizing-the-username-field"></a>
<!-- ### Customizing the Username Field -->
### Customizing the Username Field

<!-- When authenticating using the password grant, Passport will use the `email` attribute of your authenticatable model as the "username". However, you may customize this behavior by defining a `findForPassport` method on your model: -->
パスワード付与を使用して認証する場合、Passport は認証可能なモデルの `email` 属性を「ユーザー名」として使用します。ただし、モデルで `findForPassport` メソッドを定義することで、この動作をカスタマイズできます。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Bridge\Client;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```

<a name="customizing-the-password-validation"></a>
<!-- ### Customizing the Password Validation -->
### Customizing the Password Validation

<!-- When authenticating using the password grant, Passport will use the `password` attribute of your model to validate the given password. If your model does not have a `password` attribute or you wish to customize the password validation logic, you can define a `validateForPassportPasswordGrant` method on your model: -->
パスワード付与を使用して認証する場合、Passport はモデルの `password` 属性を使用して、指定されたパスワードを検証します。モデルに `password` 属性がない場合、またはパスワード検証ロジックをカスタマイズしたい場合は、モデルに `validateForPassportPasswordGrant` メソッドを定義できます。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```

<a name="implicit-grant"></a>
<!-- ## Implicit Grant -->
## Implicit Grant

> [!WARNING]
> 暗黙的な付与トークンの使用は推奨されなくなりました。代わりに、[a grant type that is currently recommended by OAuth2 Server](https://oauth2.thephpleague.com/authorization-server/which-grant/) を選択する必要があります。

<!-- The implicit grant is similar to the authorization code grant; however, the token is returned to the client without exchanging an authorization code. This grant is most commonly used for JavaScript or mobile applications where the client credentials can't be securely stored. To enable the grant, call the `enableImplicitGrant` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
暗黙的グラントは認可コードグラントに似ています。ただし、トークンは認証コードを交換せずにクライアントに返されます。この許可は、クライアントの資格情報を安全に保存できない JavaScript またはモバイル アプリケーションに最も一般的に使用されます。付与を有効にするには、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドで `enableImplicitGrant` メソッドを呼び出します。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```

<!-- Before your application can issue tokens via the implicit grant, you will need to create an implicit grant client. You may do this using the `passport:client` Artisan command with the `--implicit` option. -->
アプリケーションが暗黙的許可を介してトークンを発行できるようにするには、暗黙的許可クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--implicit` オプションを指定します。

```shell
php artisan passport:client --implicit
```

<!-- Once the grant has been enabled and an implicit client has been created, developers may use their client ID to request an access token from your application. The consuming application should make a redirect request to your application's `/oauth/authorize` route like so: -->
許可が有効になり、暗黙的なクライアントが作成されると、開発者はクライアント ID を使用してアプリケーションからのアクセス トークンをリクエストできます。使用側アプリケーションは、次のようにアプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

> [!NOTE]
> `/oauth/authorize` ルートは Passport によってすでに定義されていることに注意してください。このルートを手動で定義する必要はありません。

<a name="client-credentials-grant"></a>
<!-- ## Client Credentials Grant -->
## Client Credentials Grant

<!-- The client credentials grant is suitable for machine-to-machine authentication. For example, you might use this grant in a scheduled job which is performing maintenance tasks over an API. -->
クライアント資格情報の付与は、マシン間の認証に適しています。たとえば、API を介してメンテナンス タスクを実行するスケジュールされたジョブでこの許可を使用できます。

<!-- Before your application can issue tokens via the client credentials grant, you will need to create a client credentials grant client. You may do this using the `--client` option of the `passport:client` Artisan command: -->
アプリケーションがクライアント資格情報付与を通じてトークンを発行できるようにするには、クライアント資格情報付与クライアントを作成する必要があります。これは、`passport:client` Artisan コマンドの `--client` オプションを使用して実行できます。

```shell
php artisan passport:client --client
```

<!-- Next, assign the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware to a route: -->
次に、`Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` ミドルウェアをルートに割り当てます。

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```

<!-- To restrict access to the route to specific scopes, you may provide a list of the required scopes to the `using` method`: -->
ルートへのアクセスを特定のスコープに制限するには、必要なスコープのリストを `using` メソッドに提供します。

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```

> [!WARNING]
> [underlying OAuth2 server](https://oauth2.thephpleague.com/database-setup/#:~:text=Please%20note%20that,the%20bearer%20token.) は、トークンの `sub` クレームをクライアント資格情報トークンのクライアントの識別子に設定します。デフォルトでは、Passport はクライアントに UUID を使用するため、これがユーザーの整数主キーと衝突することはありません。ただし、`Passport::$clientUuids` を `false` に設定した場合、クライアントの資格情報トークンによって、ID がクライアントの ID と一致するユーザーが誤って解決される可能性があります。このような場合、このミドルウェアを使用しても、受信トークンがクライアント資格情報トークンであることは保証できません。

<a name="retrieving-tokens"></a>
<!-- ### Retrieving Tokens -->
### Retrieving Tokens

<!-- To retrieve a token using this grant type, make a request to the `oauth/token` endpoint: -->
この付与タイプを使用してトークンを取得するには、`oauth/token` エンドポイントにリクエストを作成します。

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```

<a name="personal-access-tokens"></a>
<!-- ## Personal Access Tokens -->
## Personal Access Tokens

<!-- Sometimes, your users may want to issue access tokens to themselves without going through the typical authorization code redirect flow. Allowing users to issue tokens to themselves via your application's UI can be useful for allowing users to experiment with your API or may serve as a simpler approach to issuing access tokens in general. -->
場合によっては、ユーザーが通常の認可コード リダイレクト フローを経由せずに自分自身にアクセス トークンを発行したい場合があります。ユーザーがアプリケーションの UI を介して自分自身にトークンを発行できるようにすると、ユーザーが API を実験できるようにする場合や、一般にアクセス トークンを発行するためのより簡単なアプローチとして機能する場合があります。

> [!NOTE]
> アプリケーションが主に個人アクセス トークンを発行するために Passport を使用している場合は、API アクセス トークンを発行するための Laravel の軽量ファーストパーティ ライブラリである [Laravel Sanctum](/docs/12.x/sanctum) の使用を検討してください。

<a name="creating-a-personal-access-client"></a>
<!-- ### Creating a Personal Access Client -->
### Creating a Personal Access Client

<!-- Before your application can issue personal access tokens, you will need to create a personal access client. You may do this by executing the `passport:client` Artisan command with the `--personal` option. If you have already run the `passport:install` command, you do not need to run this command: -->
アプリケーションが個人アクセス トークンを発行できるようにするには、個人アクセス クライアントを作成する必要があります。これを行うには、`--personal` オプションを指定して `passport:client` Artisan コマンドを実行します。すでに `passport:install` コマンドを実行している場合は、このコマンドを実行する必要はありません。

```shell
php artisan passport:client --personal
```

<a name="customizing-the-user-provider-for-pat"></a>
<!-- ### Customizing the User Provider -->
### Customizing the User Provider

<!-- If your application uses more than one [authentication user provider](/docs/12.x/authentication#introduction), you may specify which user provider the personal access grant client uses by providing a `--provider` option when creating the client via the `artisan passport:client --personal` command. The given provider name should match a valid provider defined in your application's `config/auth.php` configuration file. You can then [protect your route using middleware](#multiple-authentication-guards) to ensure that only users from the guard's specified provider are authorized. -->
アプリケーションが複数の [authentication user provider](/docs/12.x/authentication#introduction) を使用する場合、`artisan passport:client --personal` コマンドでクライアントを作成するときに `--provider` オプションを指定することで、個人用アクセス許可クライアントが使用するユーザー プロバイダを指定できます。指定されたプロバイダ名は、アプリケーションの `config/auth.php` 構成ファイルで定義されている有効なプロバイダと一致する必要があります。その後、[protect your route using middleware](#multiple-authentication-guards) を実行して、ガードの指定されたプロバイダのユーザーのみが承認されるようにすることができます。

<a name="managing-personal-access-tokens"></a>
<!-- ### Managing Personal Access Tokens -->
### Managing Personal Access Tokens

<!-- Once you have created a personal access client, you may issue tokens for a given user using the `createToken` method on the `App\Models\User` model instance. The `createToken` method accepts the name of the token as its first argument and an optional array of [scopes](#token-scopes) as its second argument: -->
パーソナル アクセス クライアントを作成したら、`App\Models\User` モデル インスタンスの `createToken` メソッドを使用して、特定のユーザーにトークンを発行できます。 `createToken` メソッドは、トークンの名前を最初の引数として受け入れ、オプションの [scopes](#token-scopes) 配列を 2 番目の引数として受け入れます。

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Creating a token without scopes...
$token = $user->createToken('My Token')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// Creating a token with all scopes...
$token = $user->createToken('My Token', ['*'])->accessToken;

// Retrieving all the valid personal access tokens that belong to the user...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```

<a name="protecting-routes"></a>
<!-- ## Protecting Routes -->
## Protecting Routes

<a name="via-middleware"></a>
<!-- ### Via Middleware -->
### Via Middleware

<!-- Passport includes an [authentication guard](/docs/12.x/authentication#adding-custom-guards) that will validate access tokens on incoming requests. Once you have configured the `api` guard to use the `passport` driver, you only need to specify the `auth:api` middleware on any routes that should require a valid access token: -->
Passportには、受信リクエストのアクセス トークンを検証する [authentication guard](/docs/12.x/authentication#adding-custom-guards) が含まれています。 `passport` ドライバを使用するように `api` ガードを構成したら、有効なアクセス トークンを必要とするルートで `auth:api` ミドルウェアを指定するだけで済みます。

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```

> [!WARNING]
> [client credentials grant](#client-credentials-grant) を使用している場合は、`auth:api` ミドルウェアの代わりに [the `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` middleware](#client-credentials-grant) を使用してルートを保護してください。

<a name="multiple-authentication-guards"></a>
<!-- #### Multiple Authentication Guards -->
#### Multiple Authentication Guards

<!-- If your application authenticates different types of users that perhaps use entirely different Eloquent models, you will likely need to define a guard configuration for each user provider type in your application. This allows you to protect requests intended for specific user providers. For example, given the following guard configuration the `config/auth.php` configuration file: -->
アプリケーションが、おそらくまったく異なる Eloquent モデルを使用するさまざまなタイプのユーザーを認証する場合、アプリケーション内のユーザー プロバイダ タイプごとにガード構成を定義する必要がある可能性があります。これにより、特定のユーザー プロバイダを対象としたリクエストを保護できます。たとえば、`config/auth.php` 構成ファイルに次のガード構成があるとします。

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```

<!-- The following route will utilize the `api-customers` guard, which uses the `customers` user provider, to authenticate incoming requests: -->
次のルートは、`customers` ユーザー プロバイダを使用する `api-customers` ガードを利用して、受信リクエストを認証します。

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```

> [!NOTE]
> Passport で複数のユーザー プロバイダを使用する方法の詳細については、[personal access tokens documentation](#customizing-the-user-provider-for-pat) および [password grant documentation](#customizing-the-user-provider) を参照してください。

<a name="passing-the-access-token"></a>
<!-- ### Passing the Access Token -->
### Passing the Access Token

<!-- When calling routes that are protected by Passport, your application's API consumers should specify their access token as a `Bearer` token in the `Authorization` header of their request. For example, when using the `Http` Facade: -->
Passport によって保護されているルートを呼び出す場合、アプリケーションの API コンシューマーは、リクエストの `Authorization` ヘッダーでアクセス トークンを `Bearer` トークンとして指定する必要があります。たとえば、`Http` ファサードを使用する場合:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```

<a name="token-scopes"></a>
<!-- ## Token Scopes -->
## Token Scopes

<!-- Scopes allow your API clients to request a specific set of permissions when requesting authorization to access an account. For example, if you are building an e-commerce application, not all API consumers will need the ability to place orders. Instead, you may allow the consumers to only request authorization to access order shipment statuses. In other words, scopes allow your application's users to limit the actions a third-party application can perform on their behalf. -->
スコープを使用すると、API クライアントがアカウントにアクセスするための承認をリクエストするときに、特定の権限のセットをリクエストできるようになります。たとえば、電子商取引アプリケーションを構築している場合、すべての API コンシューマーが注文する機能を必要とするわけではありません。代わりに、消費者が注文の出荷ステータスにアクセスするための承認のみを要求できるようにすることもできます。つまり、スコープを使用すると、アプリケーションのユーザーは、サードパーティのアプリケーションがユーザーに代わって実行できるアクションを制限できます。

<a name="defining-scopes"></a>
<!-- ### Defining Scopes -->
### Defining Scopes

<!-- You may define your API's scopes using the `Passport::tokensCan` method in the `boot` method of your application's `App\Providers\AppServiceProvider` class. The `tokensCan` method accepts an array of scope names and scope descriptions. The scope description may be anything you wish and will be displayed to users on the authorization approval screen: -->
アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドの `Passport::tokensCan` メソッドを使用して、API のスコープを定義できます。 `tokensCan` メソッドは、スコープ名とスコープの説明の配列を受け入れます。スコープの説明は任意のものにすることができ、認可承認画面でユーザーに表示されます。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```

<a name="default-scope"></a>
<!-- ### Default Scope -->
### Default Scope

<!-- If a client does not request any specific scopes, you may configure your Passport server to attach default scopes to the token using the `defaultScopes` method. Typically, you should call this method from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
クライアントが特定のスコープを要求しない場合は、`defaultScopes` メソッドを使用してデフォルトのスコープをトークンに付加するように Passport サーバーを構成できます。通常、このメソッドは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```

<a name="assigning-scopes-to-tokens"></a>
<!-- ### Assigning Scopes to Tokens -->
### Assigning Scopes to Tokens

<a name="when-requesting-authorization-codes"></a>
<!-- #### When Requesting Authorization Codes -->
#### When Requesting Authorization Codes

<!-- When requesting an access token using the authorization code grant, consumers should specify their desired scopes as the `scope` query string parameter. The `scope` parameter should be a space-delimited list of scopes: -->
認可コードグラントを使用してアクセストークンをリクエストする場合、コンシューマは希望するスコープを `scope` クエリ文字列パラメータとして指定する必要があります。 `scope` パラメータは、スペースで区切られたスコープのリストである必要があります。

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```

<a name="when-issuing-personal-access-tokens"></a>
<!-- #### When Issuing Personal Access Tokens -->
#### When Issuing Personal Access Tokens

<!-- If you are issuing personal access tokens using the `App\Models\User` model's `createToken` method, you may pass the array of desired scopes as the second argument to the method: -->
`App\Models\User` モデルの `createToken` メソッドを使用してパーソナル アクセス トークンを発行している場合は、目的のスコープの配列を 2 番目の引数としてメソッドに渡すことができます。

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```

<a name="checking-scopes"></a>
<!-- ### Checking Scopes -->
### Checking Scopes

<!-- Passport includes two middleware that may be used to verify that an incoming request is authenticated with a token that has been granted a given scope. -->
Passport には、受信リクエストが特定のスコープが付与されたトークンで認証されていることを検証するために使用できる 2 つのミドルウェアが含まれています。

<a name="check-for-all-scopes"></a>
<!-- #### Check For All Scopes -->
#### Check For All Scopes

<!-- The `Laravel\Passport\Http\Middleware\CheckToken` middleware may be assigned to a route to verify that the incoming request's access token has all the listed scopes: -->
`Laravel\Passport\Http\Middleware\CheckToken` ミドルウェアをルートに割り当てて、受信リクエストのアクセス トークンにリストされているすべてのスコープがあることを確認できます。

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```

<a name="check-for-any-scopes"></a>
<!-- #### Check for Any Scopes -->
#### Check for Any Scopes

<!-- The `Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` middleware may be assigned to a route to verify that the incoming request's access token has *at least one* of the listed scopes: -->
`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` ミドルウェアをルートに割り当てて、受信リクエストのアクセス トークンにリストされているスコープの * 少なくとも 1 つ* があることを確認できます。

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```

<a name="checking-scopes-on-a-token-instance"></a>
<!-- #### Checking Scopes on a Token Instance -->
#### Checking Scopes on a Token Instance

<!-- Once an access token authenticated request has entered your application, you may still check if the token has a given scope using the `tokenCan` method on the authenticated `App\Models\User` instance: -->
アクセス トークン認証されたリクエストがアプリケーションに入ると、認証された `App\Models\User` インスタンスの `tokenCan` メソッドを使用して、トークンに特定のスコープがあるかどうかを確認できます。

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```

<a name="additional-scope-methods"></a>
<!-- #### Additional Scope Methods -->
#### Additional Scope Methods

<!-- The `scopeIds` method will return an array of all defined IDs / names: -->
`scopeIds` メソッドは、定義されたすべての ID/名前の配列を返します。

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```

<!-- The `scopes` method will return an array of all defined scopes as instances of `Laravel\Passport\Scope`: -->
`scopes` メソッドは、定義されたすべてのスコープの配列を `Laravel\Passport\Scope` のインスタンスとして返します。

```php
Passport::scopes();
```

<!-- The `scopesFor` method will return an array of `Laravel\Passport\Scope` instances matching the given IDs / names: -->
`scopesFor` メソッドは、指定された ID / 名前に一致する `Laravel\Passport\Scope` インスタンスの配列を返します。

```php
Passport::scopesFor(['user:read', 'orders:create']);
```

<!-- You may determine if a given scope has been defined using the `hasScope` method: -->
`hasScope` メソッドを使用して、特定のスコープが定義されているかどうかを確認できます。

```php
Passport::hasScope('orders:create');
```

<a name="spa-authentication"></a>
<!-- ## SPA Authentication -->
## SPA Authentication

<!-- When building an API, it can be extremely useful to be able to consume your own API from your JavaScript application. This approach to API development allows your own application to consume the same API that you are sharing with the world. The same API may be consumed by your web application, mobile applications, third-party applications, and any SDKs that you may publish on various package managers. -->
API を構築するとき、JavaScript アプリケーションから独自の API を利用できると非常に便利です。この API 開発アプローチにより、独自のアプリケーションで世界と共有しているのと同じ API を使用できるようになります。同じ API は、Web アプリケーション、モバイル アプリケーション、サードパーティ アプリケーション、およびさまざまなパッケージ マネージャーで公開される SDK によって使用される場合があります。

<!-- Typically, if you want to consume your API from your JavaScript application, you would need to manually send an access token to the application and pass it with each request to your application. However, Passport includes a middleware that can handle this for you. All you need to do is append the `CreateFreshApiToken` middleware to the `web` middleware group in your application's `bootstrap/app.php` file: -->
通常、JavaScript アプリケーションから API を使用したい場合は、アクセス トークンをアプリケーションに手動で送信し、各リクエストとともにそれをアプリケーションに渡す必要があります。ただし、Passport にはこれを処理できるミドルウェアが含まれています。必要なのは、アプリケーションの `bootstrap/app.php` ファイル内の `web` ミドルウェア グループに `CreateFreshApiToken` ミドルウェアを追加することだけです。

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```

> [!WARNING]
> `CreateFreshApiToken` ミドルウェアがミドルウェア スタックにリストされている最後のミドルウェアであることを確認する必要があります。

<!-- This middleware will attach a `laravel_token` cookie to your outgoing responses. This cookie contains an encrypted JWT that Passport will use to authenticate API requests from your JavaScript application. The JWT has a lifetime equal to your `session.lifetime` configuration value. Now, since the browser will automatically send the cookie with all subsequent requests, you may make requests to your application's API without explicitly passing an access token: -->
このミドルウェアは、発信応答に `laravel_token` Cookie を添付します。この Cookie には、JavaScript アプリケーションからの API リクエストを認証するために Passport が使用する暗号化された JWT が含まれています。 JWT の有効期間は、`session.lifetime` 構成値と同じです。これで、ブラウザは後続のすべてのリクエストとともに Cookie を自動的に送信するため、明示的にアクセス トークンを渡さなくてもアプリケーションの API にリクエストを行うことができます。

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```

<a name="customizing-the-cookie-name"></a>
<!-- #### Customizing the Cookie Name -->
#### Customizing the Cookie Name

<!-- If needed, you can customize the `laravel_token` cookie's name using the `Passport::cookie` method. Typically, this method should be called from the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
必要に応じて、`Passport::cookie` メソッドを使用して、`laravel_token` Cookie の名前をカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding included with the skeleton application and all starter kits includes an [Axios](https://github.com/axios/axios) instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests. -->
この認証方法を使用する場合は、有効な CSRF トークン ヘッダーがリクエストに含まれていることを確認する必要があります。スケルトン アプリケーションとすべてのスターター キットに含まれるデフォルトの Laravel JavaScript スキャフォールディングには、暗号化された `XSRF-TOKEN` Cookie 値を自動的に使用して、同一オリジン リクエストで `X-XSRF-TOKEN` ヘッダーを送信する [Axios](https://github.com/axios/axios) インスタンスが含まれています。

> [!NOTE]
> `X-XSRF-TOKEN` の代わりに `X-CSRF-TOKEN` ヘッダーを送信することを選択した場合は、`csrf_token()` によって提供される暗号化されていないトークンを使用する必要があります。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Passport raises events when issuing access tokens and refresh tokens. You may [listen for these events](/docs/12.x/events) to prune or revoke other access tokens in your database: -->
Passportは、アクセス トークンとリフレッシュ トークンを発行するときにイベントを発生させます。 [listen for these events](/docs/12.x/events) を使用して、データベース内の他のアクセス トークンを削除または取り消すことができます。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| イベント名                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

<!-- </div> -->
</div>

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token: -->
Passport の `actingAs` メソッドを使用して、現在認証されているユーザーとそのスコープを指定できます。 `actingAs` メソッドに指定される最初の引数はユーザー インスタンスで、2 番目の引数はユーザーのトークンに付与されるスコープの配列です。

```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```

<!-- Passport's `actingAsClient` method may be used to specify the currently authenticated client as well as its scopes. The first argument given to the `actingAsClient` method is the client instance and the second is an array of scopes that should be granted to the client's token: -->
Passport の `actingAsClient` メソッドを使用して、現在認証されているクライアントとそのスコープを指定できます。 `actingAsClient` メソッドに指定される最初の引数はクライアント インスタンスで、2 番目の引数はクライアントのトークンに付与されるスコープの配列です。

```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```

