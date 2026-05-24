# Laravel Passport (Laravel Passport)

- [Introduction](#introduction)
    - [PassportかSanctumか？](#passport-or-sanctum)
- [Installation](#installation)
    - [Passportの展開](#deploying-passport)
    - [移行のカスタマイズ](#migration-customization)
    - [Passportのアップグレード](#upgrading-passport)
- [Configuration](#configuration)
    - [クライアントシークレットのハッシュ化](#client-secret-hashing)
    - [トークンの有効期間](#token-lifetimes)
    - [デフォルトモデルの上書き](#overriding-default-models)
    - [ルートの上書き](#overriding-routes)
- [アクセストークンの発行](#issuing-access-tokens)
    - [クライアントの管理](#managing-clients)
    - [トークンのリクエスト](#requesting-tokens)
    - [トークンのリフレッシュ](#refreshing-tokens)
    - [トークンの取り消し](#revoking-tokens)
    - [トークンのパージ](#purging-tokens)
- [PKCE による認証コードの付与](#code-grant-pkce)
    - [クライアントの作成](#creating-a-auth-pkce-grant-client)
    - [トークンのリクエスト](#requesting-auth-pkce-grant-tokens)
- [パスワード付与トークン](#password-grant-tokens)
    - [パスワード付与クライアントの作成](#creating-a-password-grant-client)
    - [トークンのリクエスト](#requesting-password-grant-tokens)
    - [すべてのスコープのリクエスト](#requesting-all-scopes)
    - [ユーザープロバイダのカスタマイズ](#customizing-the-user-provider)
    - [ユーザー名フィールドのカスタマイズ](#customizing-the-username-field)
    - [パスワード検証のカスタマイズ](#customizing-the-password-validation)
- [暗黙的な付与トークン](#implicit-grant-tokens)
- [クライアント認証情報付与トークン](#client-credentials-grant-tokens)
- [パーソナルアクセストークン](#personal-access-tokens)
    - [パーソナルアクセスクライアントの作成](#creating-a-personal-access-client)
    - [パーソナルアクセストークンの管理](#managing-personal-access-tokens)
- [ルートを守る](#protecting-routes)
    - [ミドルウェア経由](#via-middleware)
    - [アクセストークンを渡す](#passing-the-access-token)
- [トークンのスコープ](#token-scopes)
    - [スコープの定義](#defining-scopes)
    - [デフォルトのスコープ](#default-scope)
    - [トークンへのスコープの割り当て](#assigning-scopes-to-tokens)
    - [スコープの確認](#checking-scopes)
- [JavaScript を使用した API の使用](#consuming-your-api-with-javascript)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel Passport](https://github.com/laravel/passport) は、Laravel アプリケーションに完全な OAuth2 サーバー実装を数分で提供します。Passportは、Andy Millington と Simon Hamp によって保守されている [リーグOAuth2サーバー](https://github.com/thephpleague/oauth2-server) の上に構築されています。

> [!WARNING]  
> このドキュメントは、OAuth2 についてすでに理解していることを前提としています。 OAuth2 について何も知らない場合は、続行する前に、一般的な [terminology](https://oauth2.thephpleague.com/terminology/) と OAuth2 の機能についてよく理解しておくことを検討してください。

<a name="passport-or-sanctum"></a>
### PassportかSanctumか？

始める前に、アプリケーションが Laravel Passport と [Laravel Sanctum](/docs/{{version}}/sanctum) のどちらの方が適切に提供されるかを判断したい場合があります。アプリケーションが OAuth2 をサポートする必要がある場合は、Laravel Passport を使用する必要があります。

ただし、シングルページ アプリケーション、モバイル アプリケーションを認証しようとする場合、または API トークンを発行しようとする場合は、[Laravel Sanctum](/docs/{{version}}/sanctum) を使用する必要があります。 Laravel Sanctum は OAuth2 をサポートしていません。ただし、よりシンプルな API 認証開発エクスペリエンスが提供されます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを介して Passport をインストールします。

```shell
composer require laravel/passport
```

Passport の [サービスプロバイダ](/docs/{{version}}/providers) は独自のデータベース移行ディレクトリを登録するため、パッケージのインストール後にデータベースを移行する必要があります。Passportの移行により、アプリケーションが OAuth2 クライアントとアクセス トークンを保存するために必要なテーブルが作成されます。

```shell
php artisan migrate
```

次に、`passport:install` Artisan コマンドを実行する必要があります。このコマンドは、安全なアクセス トークンを生成するために必要な暗号化キーを作成します。さらに、このコマンドは、アクセス トークンの生成に使用される「個人アクセス」クライアントと「パスワード許可」クライアントを作成します。

```shell
php artisan passport:install
```

> [!NOTE]  
> 自動インクリメント整数の代わりに、Passport `Client` モデルの主キー値として UUID を使用したい場合は、[`uuids` オプション](#client-uuids) を使用して Passport をインストールしてください。

`passport:install` コマンドを実行した後、`Laravel\Passport\HasApiTokens` 特性を `App\Models\User` モデルに追加します。この特性は、認証されたユーザーのトークンとスコープを検査できるようにするいくつかのヘルパ メソッドをモデルに提供します。モデルがすでに `Laravel\Sanctum\HasApiTokens` 特性を使用している場合は、その特性を削除できます。

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;
    use Laravel\Passport\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, HasFactory, Notifiable;
    }

最後に、アプリケーションの `config/auth.php` 構成ファイルで、`api` 認証ガードを定義し、`driver` オプションを `passport` に設定する必要があります。これにより、受信 API リクエストを認証するときに Passport の `TokenGuard` を使用するようにアプリケーションに指示されます。

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

<a name="client-uuids"></a>
#### クライアントUUID

`--uuids` オプションを指定して `passport:install` コマンドを実行することもできます。このオプションは、Passport `Client` モデルの主キー値として自動インクリメント整数の代わりに UUID を使用するように Passport に指示します。 `--uuids` オプションを指定して `passport:install` コマンドを実行すると、Passportのデフォルト移行の無効化に関する追加の指示が表示されます。

```shell
php artisan passport:install --uuids
```

<a name="deploying-passport"></a>
### Passportの展開

Passport をアプリケーションのサーバーに初めてデプロイするときは、おそらく `passport:keys` コマンドを実行する必要があります。このコマンドは、Passportがアクセス トークンを生成するために必要な暗号化キーを生成します。生成されたキーは通常、ソース管理に保持されません。

```shell
php artisan passport:keys
```

必要に応じて、Passport のキーのロード元となるパスを定義できます。これを実現するには、`Passport::loadKeysFrom` メソッドを使用できます。通常、このメソッドは、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
    }

<a name="loading-keys-from-the-environment"></a>
#### 環境からのキーのロード

あるいは、`vendor:publish` Artisan コマンドを使用して、Passport の構成ファイルを公開することもできます。

```shell
php artisan vendor:publish --tag=passport-config
```

構成ファイルが公開された後、アプリケーションの暗号化キーを環境変数として定義してロードできます。

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```

<a name="migration-customization"></a>
### 移行のカスタマイズ

Passport のデフォルトの移行を使用しない場合は、`App\Providers\AppServiceProvider` クラスの `register` メソッドで `Passport::ignoreMigrations` メソッドを呼び出す必要があります。 `vendor:publish` Artisan コマンドを使用して、デフォルトの移行をエクスポートできます。

```shell
php artisan vendor:publish --tag=passport-migrations
```

<a name="upgrading-passport"></a>
### Passportのアップグレード

Passport の新しいメジャー バージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/passport/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="configuration"></a>
## 構成 (Configuration)

<a name="client-secret-hashing"></a>
### クライアントシークレットのハッシュ化

データベースに保存するときにクライアントのシークレットをハッシュしたい場合は、`App\Providers\AuthServiceProvider` クラスの `boot` メソッドで `Passport::hashClientSecrets` メソッドを呼び出す必要があります。

    use Laravel\Passport\Passport;

    Passport::hashClientSecrets();

有効にすると、すべてのクライアント シークレットは作成直後にのみユーザーに表示されます。プレーンテキストのクライアント シークレット値はデータベースに保存されないため、シークレットの値が失われた場合に回復することはできません。

<a name="token-lifetimes"></a>
### トークンの有効期間

デフォルトでは、Passport は 1 年後に期限切れになる長期間のアクセス トークンを発行します。トークンの有効期間を長く/短く設定したい場合は、`tokensExpireIn`、`refreshTokensExpireIn`、および `personalAccessTokensExpireIn` メソッドを使用できます。これらのメソッドは、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::tokensExpireIn(now()->addDays(15));
        Passport::refreshTokensExpireIn(now()->addDays(30));
        Passport::personalAccessTokensExpireIn(now()->addMonths(6));
    }

> [!WARNING]  
> Passport のデータベース テーブルの `expires_at` 列は読み取り専用で、表示のみを目的としています。トークンを発行するとき、Passport は署名され暗号化されたトークン内に有効期限情報を保存します。トークンを無効にする必要がある場合は、[それを取り消す](#revoking-tokens) を実行する必要があります。

<a name="overriding-default-models"></a>
### デフォルトモデルの上書き

独自のモデルを定義し、対応する Passport モデルを拡張することで、Passport が内部で使用するモデルを自由に拡張できます。

    use Laravel\Passport\Client as PassportClient;

    class Client extends PassportClient
    {
        // ...
    }

モデルを定義した後、`Laravel\Passport\Passport` クラスを介してカスタム モデルを使用するように Passport に指示できます。通常、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドでカスタム モデルについて Passport に通知する必要があります。

    use App\Models\Passport\AuthCode;
    use App\Models\Passport\Client;
    use App\Models\Passport\PersonalAccessClient;
    use App\Models\Passport\RefreshToken;
    use App\Models\Passport\Token;

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::useTokenModel(Token::class);
        Passport::useRefreshTokenModel(RefreshToken::class);
        Passport::useAuthCodeModel(AuthCode::class);
        Passport::useClientModel(Client::class);
        Passport::usePersonalAccessClientModel(PersonalAccessClient::class);
    }

<a name="overriding-routes"></a>
### ルートの上書き

場合によっては、Passport で定義されたルートをカスタマイズしたい場合があります。これを実現するには、まずアプリケーションの `AppServiceProvider` の `register` メソッドに `Passport::ignoreRoutes` を追加して、Passport によって登録されたルートを無視する必要があります。

    use Laravel\Passport\Passport;

    /**
     * Register any application services.
     */
    public function register(): void
    {
        Passport::ignoreRoutes();
    }

次に、[そのルートファイル](https://github.com/laravel/passport/blob/11.x/routes/web.php) の Passport で定義されたルートをアプリケーションの `routes/web.php` ファイルにコピーし、好みに合わせて変更します。

    Route::group([
        'as' => 'passport.',
        'prefix' => config('passport.path', 'oauth'),
        'namespace' => '\Laravel\Passport\Http\Controllers',
    ], function () {
        // Passport routes...
    });

<a name="issuing-access-tokens"></a>
## アクセストークンの発行 (Issuing Access Tokens)

認証コードを介して OAuth2 を使用することは、ほとんどの開発者が OAuth2 に慣れている方法です。認証コードを使用する場合、クライアント アプリケーションはユーザーをサーバーにリダイレクトし、そこでユーザーはクライアントにアクセス トークンを発行するリクエストを承認または拒否します。

<a name="managing-clients"></a>
### クライアントの管理

まず、アプリケーションの API と対話する必要があるアプリケーションを構築する開発者は、「クライアント」を作成して、自分のアプリケーションをあなたのアプリケーションに登録する必要があります。通常、これは、アプリケーションの名前と、ユーザーが承認リクエストを承認した後にアプリケーションがリダイレクトできる URL を提供することで構成されます。

<a name="the-passportclient-command"></a>
#### `passport:client` コマンド

クライアントを作成する最も簡単な方法は、`passport:client` Artisan コマンドを使用することです。このコマンドは、OAuth2 機能をテストするための独自のクライアントを作成するために使用できます。 `client` コマンドを実行すると、Passport はクライアントに関する詳細情報の入力を求め、クライアント ID とシークレットを提供します。

```shell
php artisan passport:client
```

**リダイレクト URL**

クライアントに複数のリダイレクト URL を許可する場合は、`passport:client` コマンドで URL の入力を求められたときに、カンマ区切りのリストを使用して指定できます。カンマを含む URL は URL エンコードする必要があります。

```shell
http://example.com/callback,http://examplefoo.com/callback
```

<a name="clients-json-api"></a>
#### JSON API

アプリケーションのユーザーは `client` コマンドを利用できないため、Passport はクライアントの作成に使用できる JSON API を提供します。これにより、クライアントを作成、更新、削除するためにコントローラを手動でコーディングする手間が省けます。

ただし、ユーザーがクライアントを管理するためのダッシュボードを提供するには、Passport の JSON API を独自のフロントエンドと組み合わせる必要があります。以下では、クライアントを管理するためのすべての API エンドポイントを確認します。便宜上、[Axios](https://github.com/axios/axios) を使用して、エンドポイントへの HTTP リクエストの実行を示します。

JSON API は、`web` および `auth` ミドルウェアによって保護されています。したがって、独自のアプリケーションからのみ呼び出すことができます。外部ソースから呼び出すことはできません。

<a name="get-oauthclients"></a>
#### `GET /oauth/clients`

このルートは、認証されたユーザーのすべてのクライアントを返します。これは主に、ユーザーのクライアントをすべてリストして編集または削除できるようにする場合に役立ちます。

```js
axios.get('/oauth/clients')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthclients"></a>
#### `POST /oauth/clients`

このルートは、新しいクライアントを作成するために使用されます。これには、クライアントの `name` と `redirect` URL の 2 つのデータが必要です。 `redirect` URL は、承認リクエストを承認または拒否した後にユーザーがリダイレクトされる場所です。

クライアントが作成されると、クライアント ID とクライアント シークレットが発行されます。これらの値は、アプリケーションからアクセス トークンを要求するときに使用されます。クライアント作成ルートは、新しいクライアント インスタンスを返します。

```js
const data = {
    name: 'Client Name',
    redirect: 'http://example.com/callback'
};

axios.post('/oauth/clients', data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="put-oauthclientsclient-id"></a>
#### `PUT /oauth/clients/{client-id}`

このルートはクライアントを更新するために使用されます。これには、クライアントの `name` と `redirect` URL の 2 つのデータが必要です。 `redirect` URL は、承認リクエストを承認または拒否した後にユーザーがリダイレクトされる場所です。ルートは更新されたクライアント インスタンスを返します。

```js
const data = {
    name: 'New Client Name',
    redirect: 'http://example.com/callback'
};

axios.put('/oauth/clients/' + clientId, data)
    .then(response => {
        console.log(response.data);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="delete-oauthclientsclient-id"></a>
#### `DELETE /oauth/clients/{client-id}`

このルートはクライアントを削除するために使用されます。

```js
axios.delete('/oauth/clients/' + clientId)
    .then(response => {
        // ...
    });
```

<a name="requesting-tokens"></a>
### トークンのリクエスト

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 認可のためのリダイレクト

クライアントが作成されると、開発者はクライアント ID とシークレットを使用して、アプリケーションから認証コードとアクセス トークンをリクエストできます。まず、使用側アプリケーションは、次のようにアプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

    use Illuminate\Http\Request;
    use Illuminate\Support\Str;

    Route::get('/redirect', function (Request $request) {
        $request->session()->put('state', $state = Str::random(40));

        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://third-party-app.com/callback',
            'response_type' => 'code',
            'scope' => '',
            'state' => $state,
            // 'prompt' => '', // "none", "consent", or "login"
        ]);

        return redirect('http://passport-app.test/oauth/authorize?'.$query);
    });

`prompt` パラメータは、Passport アプリケーションの認証動作を指定するために使用できます。

`prompt` 値が `none` の場合、ユーザーが Passport アプリケーションでまだ認証されていない場合、Passport は常に認証エラーをスローします。値が `consent` の場合、すべてのスコープが使用側アプリケーションに以前に付与されていたとしても、Passport は常に認証承認画面を表示します。値が `login` の場合、Passport アプリケーションは、ユーザーがすでに既存のセッションを持っている場合でも、常にユーザーにアプリケーションへの再ログインを要求します。

`prompt` 値が指定されていない場合、ユーザーは、要求されたスコープの使用アプリケーションへのアクセスを以前に承認していない場合にのみ、承認を求められます。

> [!NOTE]  
> `/oauth/authorize` ルートは Passport によってすでに定義されていることに注意してください。このルートを手動で定義する必要はありません。

<a name="approving-the-request"></a>
#### リクエストの承認

認証リクエストを受信すると、Passport は `prompt` パラメータ (存在する場合) の値に基づいて自動的に応答し、ユーザーに認証リクエストを承認または拒否できるテンプレートを表示する場合があります。リクエストを承認すると、使用側アプリケーションによって指定された `redirect_uri` にリダイレクトされます。 `redirect_uri` は、クライアントの作成時に指定された `redirect` URL と一致する必要があります。

認可承認画面をカスタマイズしたい場合は、`vendor:publish` Artisan コマンドを使用して Passport のビューを公開できます。パブリッシュされたビューは、`resources/views/vendor/passport` ディレクトリに配置されます。

```shell
php artisan vendor:publish --tag=passport-views
```

ファーストパーティクライアントを認証する場合など、認証プロンプトをスキップしたい場合があります。これは、[`Client` モデルの拡張](#overriding-default-models) と `skipsAuthorization` メソッドを定義することで実現できます。 `skipsAuthorization` が `true` を返した場合、クライアントは承認され、ユーザーはすぐに `redirect_uri` にリダイレクトされます。 ただし、使用側アプリケーションが承認のためにリダイレクトするときに `prompt` パラメーターを明示的に設定していない限り、次のようになります。

    <?php

    namespace App\Models\Passport;

    use Laravel\Passport\Client as BaseClient;

    class Client extends BaseClient
    {
        /**
         * Determine if the client should skip the authorization prompt.
         */
        public function skipsAuthorization(): bool
        {
            return $this->firstParty();
        }
    }

<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 認可コードからアクセストークンへの変換

ユーザーが認可リクエストを承認すると、ユーザーは使用側アプリケーションにリダイレクトされます。コンシューマは、まず `state` パラメータを、リダイレクト前に保存された値と比較して検証する必要があります。状態パラメータが一致する場合、コンシューマはアプリケーションに `POST` リクエストを発行して、アクセス トークンをリクエストする必要があります。リクエストには、ユーザーが認可リクエストを承認したときにアプリケーションによって発行された認可コードが含まれている必要があります。

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Http;

    Route::get('/callback', function (Request $request) {
        $state = $request->session()->pull('state');

        throw_unless(
            strlen($state) > 0 && $state === $request->state,
            InvalidArgumentException::class,
            'Invalid state value.'
        );

        $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
            'grant_type' => 'authorization_code',
            'client_id' => 'client-id',
            'client_secret' => 'client-secret',
            'redirect_uri' => 'http://third-party-app.com/callback',
            'code' => $request->code,
        ]);

        return $response->json();
    });

この `/oauth/token` ルートは、`access_token`、`refresh_token`、および `expires_in` 属性を含む JSON 応答を返します。 `expires_in` 属性には、アクセス トークンの有効期限が切れるまでの秒数が含まれます。

> [!NOTE]  
> `/oauth/authorize` ルートと同様に、`/oauth/token` ルートは Passport によって定義されます。このルートを手動で定義する必要はありません。

<a name="tokens-json-api"></a>
#### JSON API

Passport には、承認されたアクセス トークンを管理するための JSON API も含まれています。これを独自のフロントエンドと組み合わせて、アクセス トークンを管理するためのダッシュボードをユーザーに提供できます。便宜上、[Axios](https://github.com/mzabriskie/axios) を使用して、エンドポイントへの HTTP リクエストの実行を示します。 JSON API は、`web` および `auth` ミドルウェアによって保護されています。したがって、独自のアプリケーションからのみ呼び出すことができます。

<a name="get-oauthtokens"></a>
#### `GET /oauth/tokens`

このルートは、認証されたユーザーが作成したすべての許可されたアクセス トークンを返します。これは主に、ユーザーがトークンを取り消すことができるように、すべてのユーザーのトークンをリストするのに役立ちます。

```js
axios.get('/oauth/tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="delete-oauthtokenstoken-id"></a>
#### `DELETE /oauth/tokens/{token-id}`

このルートは、承認されたアクセス トークンとそれに関連するリフレッシュ トークンを取り消すために使用できます。

```js
axios.delete('/oauth/tokens/' + tokenId);
```

<a name="refreshing-tokens"></a>
### トークンのリフレッシュ

アプリケーションが有効期間の短いアクセス トークンを発行する場合、ユーザーは、アクセス トークンの発行時に提供された更新トークンを使用してアクセス トークンを更新する必要があります。

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'refresh_token',
        'refresh_token' => 'the-refresh-token',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'scope' => '',
    ]);

    return $response->json();

この `/oauth/token` ルートは、`access_token`、`refresh_token`、および `expires_in` 属性を含む JSON 応答を返します。 `expires_in` 属性には、アクセス トークンの有効期限が切れるまでの秒数が含まれます。

<a name="revoking-tokens"></a>
### トークンの取り消し

`Laravel\Passport\TokenRepository` で `revokeAccessToken` メソッドを使用して、トークンを取り消すことができます。 `Laravel\Passport\RefreshTokenRepository` の `revokeRefreshTokensByAccessTokenId` メソッドを使用して、トークンのリフレッシュ トークンを取り消すことができます。これらのクラスは、Laravel の [サービスコンテナ](/docs/{{version}}/container) を使用して解決できます。

    use Laravel\Passport\TokenRepository;
    use Laravel\Passport\RefreshTokenRepository;

    $tokenRepository = app(TokenRepository::class);
    $refreshTokenRepository = app(RefreshTokenRepository::class);

    // Revoke an access token...
    $tokenRepository->revokeAccessToken($tokenId);

    // Revoke all of the token's refresh tokens...
    $refreshTokenRepository->revokeRefreshTokensByAccessTokenId($tokenId);

<a name="purging-tokens"></a>
### トークンのパージ

トークンが取り消されたり期限切れになったりした場合、データベースからトークンを削除することができます。Passportに含まれている `passport:purge` Artisan コマンドを使用すると、次のことができます。

```shell
# Purge revoked and expired tokens and auth codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens and auth codes...
php artisan passport:purge --revoked

# Only purge expired tokens and auth codes...
php artisan passport:purge --expired
```

アプリケーションの `App\Console\Kernel` クラスで [スケジュールされたジョブ](/docs/{{version}}/scheduling) を構成して、スケジュールに従ってトークンを自動的にプルーニングすることもできます。

    /**
     * Define the application's command schedule.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->command('passport:purge')->hourly();
    }

<a name="code-grant-pkce"></a>
## PKCE による認証コードの付与 (Authorization Code Grant With PKCE)

「Proof Key for Code Exchange」(PKCE) を使用した認証コード付与は、シングル ページ アプリケーションまたはネイティブ アプリケーションが API にアクセスすることを認証するための安全な方法です。この許可は、クライアント シークレットが機密で保存されることが保証できない場合、または攻撃者によって認証コードが傍受される脅威を軽減するために使用する必要があります。 「コードベリファイア」と「コードチャレンジ」の組み合わせは、アクセストークンの認可コードを交換するときにクライアントシークレットを置き換えます。

<a name="creating-a-auth-pkce-grant-client"></a>
### クライアントの作成

アプリケーションが PKCE を使用して認証コードグラント経由でトークンを発行できるようにするには、PKCE 対応クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--public` オプションを指定します。

```shell
php artisan passport:client --public
```

<a name="requesting-auth-pkce-grant-tokens"></a>
### トークンのリクエスト

<a name="code-verifier-code-challenge"></a>
#### コードベリファイアとコードチャレンジ

この認可付与ではクライアント シークレットが提供されないため、開発者はトークンを要求するためにコード検証ツールとコード チャレンジの組み合わせを生成する必要があります。

コード検証子は、[RFC 7636仕様](https://tools.ietf.org/html/rfc7636) で定義されているように、文字、数字、および `"-"`、`"."`、`"_"`、`"~"` 文字を含む 43 ～ 128 文字のランダムな文字列である必要があります。

コード チャレンジは、URL とファイル名に安全な文字を含む Base64 でエンコードされた文字列である必要があります。末尾の `'='` 文字は削除する必要があり、改行、空白、その他の追加文字が存在しないようにする必要があります。

    $encoded = base64_encode(hash('sha256', $code_verifier, true));

    $codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');

<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 認可のためのリダイレクト

クライアントが作成されたら、クライアント ID と生成されたコード検証ツールおよびコード チャレンジを使用して、アプリケーションから認証コードとアクセス トークンをリクエストできます。まず、使用側アプリケーションは、アプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

    use Illuminate\Http\Request;
    use Illuminate\Support\Str;

    Route::get('/redirect', function (Request $request) {
        $request->session()->put('state', $state = Str::random(40));

        $request->session()->put(
            'code_verifier', $code_verifier = Str::random(128)
        );

        $codeChallenge = strtr(rtrim(
            base64_encode(hash('sha256', $code_verifier, true))
        , '='), '+/', '-_');

        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://third-party-app.com/callback',
            'response_type' => 'code',
            'scope' => '',
            'state' => $state,
            'code_challenge' => $codeChallenge,
            'code_challenge_method' => 'S256',
            // 'prompt' => '', // "none", "consent", or "login"
        ]);

        return redirect('http://passport-app.test/oauth/authorize?'.$query);
    });

<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 認可コードからアクセストークンへの変換

ユーザーが認可リクエストを承認すると、ユーザーは使用側アプリケーションにリダイレクトされます。コンシューマは、標準の認可コード付与と同様に、リダイレクト前に保存された値に対して `state` パラメータを検証する必要があります。

状態パラメータが一致する場合、コンシューマはアプリケーションに `POST` リクエストを発行して、アクセス トークンをリクエストする必要があります。リクエストには、ユーザーが認可リクエストを承認したときにアプリケーションによって発行された認可コードと、最初に生成されたコードベリファイアが含まれている必要があります。

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Http;

    Route::get('/callback', function (Request $request) {
        $state = $request->session()->pull('state');

        $codeVerifier = $request->session()->pull('code_verifier');

        throw_unless(
            strlen($state) > 0 && $state === $request->state,
            InvalidArgumentException::class
        );

        $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
            'grant_type' => 'authorization_code',
            'client_id' => 'client-id',
            'redirect_uri' => 'http://third-party-app.com/callback',
            'code_verifier' => $codeVerifier,
            'code' => $request->code,
        ]);

        return $response->json();
    });

<a name="password-grant-tokens"></a>
## パスワード付与トークン (Password Grant Tokens)

> [!WARNING]  
> パスワード付与トークンの使用は推奨されなくなりました。代わりに、[OAuth2 サーバーによって現在推奨されている許可タイプ](https://oauth2.thephpleague.com/authorization-server/which-grant/) を選択する必要があります。

OAuth2 パスワード付与により、モバイル アプリケーションなどの他のファーストパーティ クライアントが、電子メール アドレス/ユーザー名とパスワードを使用してアクセス トークンを取得できるようになります。これにより、ユーザーが OAuth2 認証コード リダイレクト フロー全体を実行する必要がなく、ファーストパーティ クライアントにアクセス トークンを安全に発行できます。

<a name="creating-a-password-grant-client"></a>
### パスワード付与クライアントの作成

アプリケーションがパスワード付与を通じてトークンを発行できるようにするには、パスワード付与クライアントを作成する必要があります。これを行うには、`passport:client` Artisan コマンドに `--password` オプションを指定します。 **すでに `passport:install` コマンドを実行している場合は、このコマンドを実行する必要はありません。**

```shell
php artisan passport:client --password
```

<a name="requesting-password-grant-tokens"></a>
### トークンのリクエスト

パスワード付与クライアントを作成したら、ユーザーの電子メール アドレスとパスワードを使用して `POST` リクエストを `/oauth/token` ルートに発行することで、アクセス トークンをリクエストできます。このルートは Passport によってすでに登録されているため、手動で定義する必要がないことに注意してください。リクエストが成功すると、サーバーからの JSON レスポンスで `access_token` および `refresh_token` を受け取ります。

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'password',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'username' => 'taylor@laravel.com',
        'password' => 'my-password',
        'scope' => '',
    ]);

    return $response->json();

> [!NOTE]  
> アクセス トークンはデフォルトで長期間有効であることに注意してください。ただし、必要に応じて自由に [アクセス トークンの最大有効期間を設定する](#configuration) を実行できます。

<a name="requesting-all-scopes"></a>
### すべてのスコープのリクエスト

パスワード付与またはクライアント資格情報付与を使用する場合、アプリケーションでサポートされているすべてのスコープに対してトークンを承認したい場合があります。これを行うには、`*` スコープをリクエストします。 `*` スコープをリクエストした場合、トークン インスタンスの `can` メソッドは常に `true` を返します。このスコープは、`password` または `client_credentials` 付与を使用して発行されたトークンにのみ割り当てることができます。

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'password',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'username' => 'taylor@laravel.com',
        'password' => 'my-password',
        'scope' => '*',
    ]);

<a name="customizing-the-user-provider"></a>
### ユーザープロバイダのカスタマイズ

アプリケーションが複数の [認証ユーザープロバイダ](/docs/{{version}}/authentication#introduction) を使用する場合、`artisan passport:client --password` コマンドでクライアントを作成するときに `--provider` オプションを指定することで、パスワード付与クライアントが使用するユーザー プロバイダを指定できます。指定されたプロバイダ名は、アプリケーションの `config/auth.php` 構成ファイルで定義されている有効なプロバイダと一致する必要があります。その後、[ミドルウェアを使用してルートを保護する](#via-middleware) を実行して、ガードの指定されたプロバイダのユーザーのみが承認されるようにすることができます。

<a name="customizing-the-username-field"></a>
### ユーザー名フィールドのカスタマイズ

パスワード付与を使用して認証する場合、Passport は認証可能なモデルの `email` 属性を「ユーザー名」として使用します。ただし、モデルで `findForPassport` メソッドを定義することで、この動作をカスタマイズできます。

    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;
    use Laravel\Passport\HasApiTokens;

    class User extends Authenticatable
    {
        use HasApiTokens, Notifiable;

        /**
         * Find the user instance for the given username.
         */
        public function findForPassport(string $username): User
        {
            return $this->where('username', $username)->first();
        }
    }

<a name="customizing-the-password-validation"></a>
### パスワード検証のカスタマイズ

パスワード付与を使用して認証する場合、Passport はモデルの `password` 属性を使用して、指定されたパスワードを検証します。モデルに `password` 属性がない場合、またはパスワード検証ロジックをカスタマイズしたい場合は、モデルに `validateForPassportPasswordGrant` メソッドを定義できます。

    <?php

    namespace App\Models;

    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;
    use Illuminate\Support\Facades\Hash;
    use Laravel\Passport\HasApiTokens;

    class User extends Authenticatable
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

<a name="implicit-grant-tokens"></a>
## 暗黙的な付与トークン (Implicit Grant Tokens)

> [!WARNING]  
> 暗黙的な付与トークンの使用は推奨されなくなりました。代わりに、[OAuth2 サーバーによって現在推奨されている許可タイプ](https://oauth2.thephpleague.com/authorization-server/which-grant/) を選択する必要があります。

暗黙的グラントは認可コードグラントに似ています。ただし、トークンは認証コードを交換せずにクライアントに返されます。この許可は、クライアントの資格情報を安全に保存できない JavaScript またはモバイル アプリケーションに最も一般的に使用されます。付与を有効にするには、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドで `enableImplicitGrant` メソッドを呼び出します。

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::enableImplicitGrant();
    }

付与が有効になると、開発者はクライアント ID を使用してアプリケーションからのアクセス トークンをリクエストできるようになります。使用側アプリケーションは、次のようにアプリケーションの `/oauth/authorize` ルートへのリダイレクト リクエストを作成する必要があります。

    use Illuminate\Http\Request;

    Route::get('/redirect', function (Request $request) {
        $request->session()->put('state', $state = Str::random(40));

        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://third-party-app.com/callback',
            'response_type' => 'token',
            'scope' => '',
            'state' => $state,
            // 'prompt' => '', // "none", "consent", or "login"
        ]);

        return redirect('http://passport-app.test/oauth/authorize?'.$query);
    });

> [!NOTE]  
> `/oauth/authorize` ルートは Passport によってすでに定義されていることに注意してください。このルートを手動で定義する必要はありません。

<a name="client-credentials-grant-tokens"></a>
## クライアント認証情報付与トークン (Client Credentials Grant Tokens)

クライアント資格情報の付与は、マシン間の認証に適しています。たとえば、API を介してメンテナンス タスクを実行するスケジュールされたジョブでこの許可を使用できます。

アプリケーションがクライアント資格情報付与を通じてトークンを発行できるようにするには、クライアント資格情報付与クライアントを作成する必要があります。これは、`passport:client` Artisan コマンドの `--client` オプションを使用して実行できます。

```shell
php artisan passport:client --client
```

次に、この許可タイプを使用するには、アプリケーションの `app/Http/Kernel.php` ファイルの `$middlewareAliases` プロパティに `CheckClientCredentials` ミドルウェアを追加します。

    use Laravel\Passport\Http\Middleware\CheckClientCredentials;

    protected $middlewareAliases = [
        'client' => CheckClientCredentials::class,
    ];

次に、ミドルウェアをルートにアタッチします。

    Route::get('/orders', function (Request $request) {
        ...
    })->middleware('client');

ルートへのアクセスを特定のスコープに制限するには、`client` ミドルウェアをルートにアタッチするときに、必要なスコープのカンマ区切りのリストを指定できます。

    Route::get('/orders', function (Request $request) {
        ...
    })->middleware('client:check-status,your-scope');

<a name="retrieving-tokens"></a>
### トークンの取得

この付与タイプを使用してトークンを取得するには、`oauth/token` エンドポイントにリクエストを作成します。

    use Illuminate\Support\Facades\Http;

    $response = Http::asForm()->post('http://passport-app.test/oauth/token', [
        'grant_type' => 'client_credentials',
        'client_id' => 'client-id',
        'client_secret' => 'client-secret',
        'scope' => 'your-scope',
    ]);

    return $response->json()['access_token'];

<a name="personal-access-tokens"></a>
## パーソナルアクセストークン (Personal Access Tokens)

場合によっては、ユーザーが通常の認可コード リダイレクト フローを経由せずに自分自身にアクセス トークンを発行したい場合があります。ユーザーがアプリケーションの UI を介して自分自身にトークンを発行できるようにすると、ユーザーが API を実験できるようにする場合や、一般にアクセス トークンを発行するためのより簡単なアプローチとして機能する場合があります。

> [!NOTE]  
> アプリケーションが主に Passport を使用して個人アクセス トークンを発行している場合は、API アクセス トークンを発行するための Laravel の軽量ファーストパーティ ライブラリである [Laravel Sanctum](/docs/{{version}}/sanctum) の使用を検討してください。

<a name="creating-a-personal-access-client"></a>
### パーソナルアクセスクライアントの作成

アプリケーションが個人アクセス トークンを発行できるようにするには、個人アクセス クライアントを作成する必要があります。これを行うには、`--personal` オプションを指定して `passport:client` Artisan コマンドを実行します。すでに `passport:install` コマンドを実行している場合は、このコマンドを実行する必要はありません。

```shell
php artisan passport:client --personal
```

パーソナル アクセス クライアントを作成した後、クライアントの ID とプレーンテキストのシークレット値をアプリケーションの `.env` ファイルに配置します。

```ini
PASSPORT_PERSONAL_ACCESS_CLIENT_ID="client-id-value"
PASSPORT_PERSONAL_ACCESS_CLIENT_SECRET="unhashed-client-secret-value"
```

<a name="managing-personal-access-tokens"></a>
### パーソナルアクセストークンの管理

パーソナル アクセス クライアントを作成したら、`App\Models\User` モデル インスタンスの `createToken` メソッドを使用して、特定のユーザーにトークンを発行できます。 `createToken` メソッドは、トークンの名前を最初の引数として受け入れ、オプションの [scopes](#token-scopes) 配列を 2 番目の引数として受け入れます。

    use App\Models\User;

    $user = User::find(1);

    // Creating a token without scopes...
    $token = $user->createToken('Token Name')->accessToken;

    // Creating a token with scopes...
    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

<a name="personal-access-tokens-json-api"></a>
#### JSON API

Passport には、個人アクセス トークンを管理するための JSON API も含まれています。これを独自のフロントエンドと組み合わせて、個人アクセス トークンを管理するためのダッシュボードをユーザーに提供できます。以下では、個人アクセス トークンを管理するためのすべての API エンドポイントを確認します。便宜上、[Axios](https://github.com/mzabriskie/axios) を使用して、エンドポイントへの HTTP リクエストの実行を示します。

JSON API は、`web` および `auth` ミドルウェアによって保護されています。したがって、独自のアプリケーションからのみ呼び出すことができます。外部ソースから呼び出すことはできません。

<a name="get-oauthscopes"></a>
#### `GET /oauth/scopes`

このルートは、アプリケーションに定義されたすべての [scopes](#token-scopes) を返します。このルートを使用して、ユーザーが個人アクセス トークンに割り当てることができるスコープを一覧表示できます。

```js
axios.get('/oauth/scopes')
    .then(response => {
        console.log(response.data);
    });
```

<a name="get-oauthpersonal-access-tokens"></a>
#### `GET /oauth/personal-access-tokens`

このルートは、認証されたユーザーが作成したすべての個人アクセス トークンを返します。これは主に、ユーザーが編集または取り消しできるように、すべてのユーザーのトークンをリストするのに役立ちます。

```js
axios.get('/oauth/personal-access-tokens')
    .then(response => {
        console.log(response.data);
    });
```

<a name="post-oauthpersonal-access-tokens"></a>
#### `POST /oauth/personal-access-tokens`

このルートは、新しい個人アクセス トークンを作成します。これには、トークンの `name` と、トークンに割り当てる必要がある `scopes` という 2 つのデータが必要です。

```js
const data = {
    name: 'Token Name',
    scopes: []
};

axios.post('/oauth/personal-access-tokens', data)
    .then(response => {
        console.log(response.data.accessToken);
    })
    .catch (response => {
        // List errors on response...
    });
```

<a name="delete-oauthpersonal-access-tokenstoken-id"></a>
#### `DELETE /oauth/personal-access-tokens/{token-id}`

このルートは、個人アクセス トークンを取り消すために使用される場合があります。

```js
axios.delete('/oauth/personal-access-tokens/' + tokenId);
```

<a name="protecting-routes"></a>
## ルートを守る (Protecting Routes)

<a name="via-middleware"></a>
### ミドルウェア経由

Passportには、受信リクエストのアクセス トークンを検証する [認証ガード](/docs/{{version}}/authentication#adding-custom-guards) が含まれています。 `passport` ドライバを使用するように `api` ガードを構成したら、有効なアクセス トークンを必要とするルートで `auth:api` ミドルウェアを指定するだけで済みます。

    Route::get('/user', function () {
        // ...
    })->middleware('auth:api');

> [!WARNING]  
> [クライアント資格情報の付与](#client-credentials-grant-tokens) を使用している場合は、`auth:api` ミドルウェアの代わりに [`client` ミドルウェア](#client-credentials-grant-tokens) を使用してルートを保護する必要があります。

<a name="multiple-authentication-guards"></a>
#### 複数の認証ガード

アプリケーションが、おそらくまったく異なる Eloquent モデルを使用するさまざまなタイプのユーザーを認証する場合、アプリケーション内のユーザー プロバイダ タイプごとにガード構成を定義する必要がある可能性があります。これにより、特定のユーザー プロバイダを対象としたリクエストを保護できます。たとえば、`config/auth.php` 構成ファイルに次のガード構成があるとします。

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],

次のルートは、`customers` ユーザー プロバイダを使用する `api-customers` ガードを利用して、受信リクエストを認証します。

    Route::get('/customer', function () {
        // ...
    })->middleware('auth:api-customers');

> [!NOTE]  
> Passport で複数のユーザー プロバイダを使用する方法の詳細については、[パスワード付与に関するドキュメント](#customizing-the-user-provider) を参照してください。

<a name="passing-the-access-token"></a>
### アクセストークンを渡す

Passport によって保護されているルートを呼び出す場合、アプリケーションの API コンシューマーは、リクエストの `Authorization` ヘッダーでアクセス トークンを `Bearer` トークンとして指定する必要があります。たとえば、Guzzle HTTP ライブラリを使用する場合は次のようになります。

    use Illuminate\Support\Facades\Http;

    $response = Http::withHeaders([
        'Accept' => 'application/json',
        'Authorization' => 'Bearer '.$accessToken,
    ])->get('https://passport-app.test/api/user');

    return $response->json();

<a name="token-scopes"></a>
## トークンのスコープ (Token Scopes)

スコープを使用すると、API クライアントがアカウントにアクセスするための承認をリクエストするときに、特定の権限のセットをリクエストできるようになります。たとえば、電子商取引アプリケーションを構築している場合、すべての API コンシューマーが注文する機能を必要とするわけではありません。代わりに、消費者が注文の出荷ステータスにアクセスするための承認のみを要求できるようにすることもできます。つまり、スコープを使用すると、アプリケーションのユーザーは、サードパーティのアプリケーションがユーザーに代わって実行できるアクションを制限できます。

<a name="defining-scopes"></a>
### スコープの定義

アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドの `Passport::tokensCan` メソッドを使用して、API のスコープを定義できます。 `tokensCan` メソッドは、スコープ名とスコープの説明の配列を受け入れます。スコープの説明は任意のものにすることができ、認可承認画面でユーザーに表示されます。

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::tokensCan([
            'place-orders' => 'Place orders',
            'check-status' => 'Check order status',
        ]);
    }

<a name="default-scope"></a>
### デフォルトのスコープ

クライアントが特定のスコープを要求しない場合は、`setDefaultScope` メソッドを使用してデフォルトのスコープをトークンに付加するように Passport サーバーを構成できます。通常、このメソッドは、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

    use Laravel\Passport\Passport;

    Passport::tokensCan([
        'place-orders' => 'Place orders',
        'check-status' => 'Check order status',
    ]);

    Passport::setDefaultScope([
        'check-status',
        'place-orders',
    ]);

> [!NOTE]  
> Passportのデフォルトのスコープは、ユーザーが生成した個人用アクセス トークンには適用されません。

<a name="assigning-scopes-to-tokens"></a>
### トークンへのスコープの割り当て

<a name="when-requesting-authorization-codes"></a>
#### 認証コードを要求する場合

認可コードグラントを使用してアクセストークンをリクエストする場合、コンシューマは希望するスコープを `scope` クエリ文字列パラメータとして指定する必要があります。 `scope` パラメータは、スペースで区切られたスコープのリストである必要があります。

    Route::get('/redirect', function () {
        $query = http_build_query([
            'client_id' => 'client-id',
            'redirect_uri' => 'http://example.com/callback',
            'response_type' => 'code',
            'scope' => 'place-orders check-status',
        ]);

        return redirect('http://passport-app.test/oauth/authorize?'.$query);
    });

<a name="when-issuing-personal-access-tokens"></a>
#### パーソナルアクセストークンを発行する場合

`App\Models\User` モデルの `createToken` メソッドを使用してパーソナル アクセス トークンを発行している場合は、目的のスコープの配列を 2 番目の引数としてメソッドに渡すことができます。

    $token = $user->createToken('My Token', ['place-orders'])->accessToken;

<a name="checking-scopes"></a>
### スコープの確認

Passport には、受信リクエストが特定のスコープが付与されたトークンで認証されていることを検証するために使用できる 2 つのミドルウェアが含まれています。まず、次のミドルウェアを `app/Http/Kernel.php` ファイルの `$middlewareAliases` プロパティに追加します。

    'scopes' => \Laravel\Passport\Http\Middleware\CheckScopes::class,
    'scope' => \Laravel\Passport\Http\Middleware\CheckForAnyScope::class,

<a name="check-for-all-scopes"></a>
#### すべてのスコープをチェックする

`scopes` ミドルウェアをルートに割り当てて、受信リクエストのアクセス トークンにリストされているスコープがすべて含まれていることを確認できます。

    Route::get('/orders', function () {
        // Access token has both "check-status" and "place-orders" scopes...
    })->middleware(['auth:api', 'scopes:check-status,place-orders']);

<a name="check-for-any-scopes"></a>
#### スコープを確認する

`scope` ミドルウェアをルートに割り当てて、受信リクエストのアクセス トークンにリストされているスコープの * 少なくとも 1 つ* があることを確認できます。

    Route::get('/orders', function () {
        // Access token has either "check-status" or "place-orders" scope...
    })->middleware(['auth:api', 'scope:check-status,place-orders']);

<a name="checking-scopes-on-a-token-instance"></a>
#### トークンインスタンスのスコープの確認

アクセス トークン認証されたリクエストがアプリケーションに入ると、認証された `App\Models\User` インスタンスの `tokenCan` メソッドを使用して、トークンに特定のスコープがあるかどうかを確認できます。

    use Illuminate\Http\Request;

    Route::get('/orders', function (Request $request) {
        if ($request->user()->tokenCan('place-orders')) {
            // ...
        }
    });

<a name="additional-scope-methods"></a>
#### 追加のスコープメソッド

`scopeIds` メソッドは、定義されたすべての ID/名前の配列を返します。

    use Laravel\Passport\Passport;

    Passport::scopeIds();

`scopes` メソッドは、定義されたすべてのスコープの配列を `Laravel\Passport\Scope` のインスタンスとして返します。

    Passport::scopes();

`scopesFor` メソッドは、指定された ID / 名前に一致する `Laravel\Passport\Scope` インスタンスの配列を返します。

    Passport::scopesFor(['place-orders', 'check-status']);

`hasScope` メソッドを使用して、特定のスコープが定義されているかどうかを確認できます。

    Passport::hasScope('place-orders');

<a name="consuming-your-api-with-javascript"></a>
## JavaScript を使用した API の使用 (Consuming Your API With JavaScript)

API を構築するとき、JavaScript アプリケーションから独自の API を利用できると非常に便利です。この API 開発アプローチにより、独自のアプリケーションで世界と共有しているのと同じ API を使用できるようになります。同じ API は、Web アプリケーション、モバイル アプリケーション、サードパーティ アプリケーション、およびさまざまなパッケージ マネージャーで公開される SDK によって使用される場合があります。

通常、JavaScript アプリケーションから API を使用したい場合は、アクセス トークンをアプリケーションに手動で送信し、各リクエストとともにそれをアプリケーションに渡す必要があります。ただし、Passport にはこれを処理できるミドルウェアが含まれています。必要なのは、`app/Http/Kernel.php` ファイル内の `web` ミドルウェア グループに `CreateFreshApiToken` ミドルウェアを追加することだけです。

    'web' => [
        // Other middleware...
        \Laravel\Passport\Http\Middleware\CreateFreshApiToken::class,
    ],

> [!WARNING]  
> `CreateFreshApiToken` ミドルウェアがミドルウェア スタックにリストされている最後のミドルウェアであることを確認する必要があります。

このミドルウェアは、発信応答に `laravel_token` Cookie を添付します。この Cookie には、JavaScript アプリケーションからの API リクエストを認証するために Passport が使用する暗号化された JWT が含まれています。 JWT の有効期間は、`session.lifetime` 構成値と同じです。これで、ブラウザは後続のすべてのリクエストとともに Cookie を自動的に送信するため、明示的にアクセス トークンを渡さなくてもアプリケーションの API にリクエストを行うことができます。

    axios.get('/api/user')
        .then(response => {
            console.log(response.data);
        });

<a name="customizing-the-cookie-name"></a>
#### Cookie名のカスタマイズ

必要に応じて、`Passport::cookie` メソッドを使用して、`laravel_token` Cookie の名前をカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        Passport::cookie('custom_name');
    }

<a name="csrf-protection"></a>
#### CSRF保護

この認証方法を使用する場合は、有効な CSRF トークン ヘッダーがリクエストに含まれていることを確認する必要があります。デフォルトの Laravel JavaScript スキャフォールディングには、暗号化された `XSRF-TOKEN` Cookie 値を自動的に使用して、同一オリジンリクエストで `X-XSRF-TOKEN` ヘッダーを送信する Axios インスタンスが含まれています。

> [!NOTE]  
> `X-XSRF-TOKEN` の代わりに `X-CSRF-TOKEN` ヘッダーを送信することを選択した場合は、`csrf_token()` によって提供される暗号化されていないトークンを使用する必要があります。

<a name="events"></a>
## イベント (Events)

Passportは、アクセス トークンとリフレッシュ トークンを発行するときにイベントを発生させます。これらのイベントを使用して、データベース内の他のアクセス トークンをプルーニングまたは取り消すことができます。必要に応じて、アプリケーションの `App\Providers\EventServiceProvider` クラスでこれらのイベントにリスナをアタッチできます。

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Laravel\Passport\Events\AccessTokenCreated' => [
            'App\Listeners\RevokeOldTokens',
        ],

        'Laravel\Passport\Events\RefreshTokenCreated' => [
            'App\Listeners\PruneOldTokens',
        ],
    ];

<a name="testing"></a>
## テスト (Testing)

Passport の `actingAs` メソッドを使用して、現在認証されているユーザーとそのスコープを指定できます。 `actingAs` メソッドに指定される最初の引数はユーザー インスタンスで、2 番目の引数はユーザーのトークンに付与されるスコープの配列です。

    use App\Models\User;
    use Laravel\Passport\Passport;

    public function test_servers_can_be_created(): void
    {
        Passport::actingAs(
            User::factory()->create(),
            ['create-servers']
        );

        $response = $this->post('/api/create-server');

        $response->assertStatus(201);
    }

Passport の `actingAsClient` メソッドを使用して、現在認証されているクライアントとそのスコープを指定できます。 `actingAsClient` メソッドに指定される最初の引数はクライアント インスタンスで、2 番目の引数はクライアントのトークンに付与されるスコープの配列です。

    use Laravel\Passport\Client;
    use Laravel\Passport\Passport;

    public function test_orders_can_be_retrieved(): void
    {
        Passport::actingAsClient(
            Client::factory()->create(),
            ['check-status']
        );

        $response = $this->get('/api/orders');

        $response->assertStatus(200);
    }

