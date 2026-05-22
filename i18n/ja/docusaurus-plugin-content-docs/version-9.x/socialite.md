# Laravel Socialite (Laravel Socialite)

- [Introduction](#introduction)
- [Installation](#installation)
- [Socialite のアップグレード](#upgrading-socialite)
- [Configuration](#configuration)
- [Authentication](#authentication)
    - [Routing](#routing)
    - [認証とストレージ](#authentication-and-storage)
    - [アクセス範囲](#access-scopes)
    - [オプションのパラメータ](#optional-parameters)
- [ユーザー詳細の取得](#retrieving-user-details)

<a name="introduction"></a>
## 導入 (Introduction)

一般的なフォームベースの認証に加えて、Laravel は、[Laravel Socialite](https://github.com/laravel/socialite) を使用して OAuth プロバイダで認証する簡単で便利な方法も提供します。 Socialite は現在、Facebook、Twitter、LinkedIn、Google、GitHub、GitLab、Bitbucket による認証をサポートしています。

> **注記**
> 他のプラットフォーム用のアダプターは、コミュニティ主導の [Socialite Providers](https://socialiteproviders.com/) Web サイトから入手できます。

<a name="installation"></a>
## インストール (Installation)

Socialite の使用を開始するには、Composer パッケージ マネージャーを使用して、プロジェクトの依存関係にパッケージを追加します。

```shell
composer require laravel/socialite
```

<a name="upgrading-socialite"></a>
## Socialite のアップグレード (Upgrading Socialite)

Socialite の新しいメジャー バージョンにアップグレードする場合は、[アップグレードガイド](https://github.com/laravel/socialite/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<a name="configuration"></a>
## 構成 (Configuration)

Socialite を使用する前に、アプリケーションが使用する OAuth プロバイダの資格情報を追加する必要があります。通常、これらの資格情報は、認証に使用するサービスのダッシュボード内に「開発者アプリケーション」を作成することによって取得できます。

これらの認証情報はアプリケーションの `config/services.php` 構成ファイルに配置する必要があり、キー `facebook`、`twitter` (OAuth 1.0)、`twitter-oauth-2` (OAuth 2.0)、`linkedin`、`google`、`github`、を使用する必要があります。アプリケーションが必要とするプロバイダに応じて、`gitlab` または `bitbucket`:

    'github' => [
        'client_id' => env('GITHUB_CLIENT_ID'),
        'client_secret' => env('GITHUB_CLIENT_SECRET'),
        'redirect' => 'http://example.com/callback-url',
    ],

> **注記**
> `redirect` オプションに相対パスが含まれている場合、完全修飾 URL に自動的に解決されます。

<a name="authentication"></a>
## 認証 (Authentication)

<a name="routing"></a>
### ルーティング

OAuth プロバイダを使用してユーザーを認証するには、2 つのルートが必要です。1 つはユーザーを OAuth プロバイダにリダイレクトするルート、もう 1 つは認証後にプロバイダからコールバックを受信するルートです。以下のルート例は、両方のルートの実装を示しています。

    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/redirect', function () {
        return Socialite::driver('github')->redirect();
    });

    Route::get('/auth/callback', function () {
        $user = Socialite::driver('github')->user();

        // $user->token
    });

`Socialite` ファサードによって提供される `redirect` メソッドは、ユーザーを OAuth プロバイダにリダイレクトします。一方、`user` メソッドは受信リクエストを検査し、認証リクエストが承認された後にプロバイダからユーザーの情報を取得します。

<a name="authentication-and-storage"></a>
### 認証とストレージ

OAuth プロバイダからユーザーを取得したら、そのユーザーがアプリケーションのデータベースと [ユーザーを認証する](/docs/{{version}}/authentication#authenticate-a-user-instance) に存在するかどうかを確認できます。ユーザーがアプリケーションのデータベースに存在しない場合は、通常、ユーザーを表す新しいレコードをデータベースに作成します。

    use App\Models\User;
    use Illuminate\Support\Facades\Auth;
    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/callback', function () {
        $githubUser = Socialite::driver('github')->user();

        $user = User::updateOrCreate([
            'github_id' => $githubUser->id,
        ], [
            'name' => $githubUser->name,
            'email' => $githubUser->email,
            'github_token' => $githubUser->token,
            'github_refresh_token' => $githubUser->refreshToken,
        ]);

        Auth::login($user);

        return redirect('/dashboard');
    });

> **注記**
> 特定の OAuth プロバイダからどのようなユーザー情報が入手できるかについて詳しくは、[ユーザー詳細の取得](#retrieving-user-details) のドキュメントを参照してください。

<a name="access-scopes"></a>
### アクセス範囲

ユーザーをリダイレクトする前に、`scopes` メソッドを使用して、認証リクエストに含める必要がある「スコープ」を指定できます。このメソッドは、以前に指定したすべてのスコープを指定したスコープとマージします。

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('github')
        ->scopes(['read:user', 'public_repo'])
        ->redirect();

`setScopes` メソッドを使用して、認証リクエストの既存のスコープをすべて上書きできます。

    return Socialite::driver('github')
        ->setScopes(['read:user', 'public_repo'])
        ->redirect();

<a name="optional-parameters"></a>
### オプションのパラメータ

多くの OAuth プロバイダは、リダイレクト要求の他のオプションのパラメーターをサポートしています。リクエストにオプションのパラメーターを含めるには、連想配列を使用して `with` メソッドを呼び出します。

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')
        ->with(['hd' => 'example.com'])
        ->redirect();

> **警告**
> `with` メソッドを使用する場合は、`state` や `response_type` などの予約キーワードを渡さないように注意してください。

<a name="retrieving-user-details"></a>
## ユーザー詳細の取得 (Retrieving User Details)

ユーザーがアプリケーションの認証コールバック ルートにリダイレクトされた後、Socialite の `user` メソッドを使用してユーザーの詳細を取得できます。 `user` メソッドによって返されるユーザー オブジェクトは、ユーザーに関する情報を独自のデータベースに保存するために使用できるさまざまなプロパティとメソッドを提供します。

認証に使用する OAuth プロバイダが OAuth 1.0 と OAuth 2.0 のどちらをサポートしているかに応じて、このオブジェクトでは異なるプロパティとメソッドを使用できる場合があります。

    use Laravel\Socialite\Facades\Socialite;

    Route::get('/auth/callback', function () {
        $user = Socialite::driver('github')->user();

        // OAuth 2.0 providers...
        $token = $user->token;
        $refreshToken = $user->refreshToken;
        $expiresIn = $user->expiresIn;

        // OAuth 1.0 providers...
        $token = $user->token;
        $tokenSecret = $user->tokenSecret;

        // All providers...
        $user->getId();
        $user->getNickname();
        $user->getName();
        $user->getEmail();
        $user->getAvatar();
    });

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### トークンからのユーザー詳細の取得 (OAuth2)

ユーザーの有効なアクセス トークンをすでに持っている場合は、Socialite の `userFromToken` メソッドを使用してユーザーの詳細を取得できます。

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('github')->userFromToken($token);

<a name="retrieving-user-details-from-a-token-and-secret-oauth1"></a>
#### トークンとシークレットからユーザーの詳細を取得する (OAuth1)

ユーザーの有効なトークンとシークレットをすでに持っている場合は、Socialite の `userFromTokenAndSecret` メソッドを使用してユーザーの詳細を取得できます。

    use Laravel\Socialite\Facades\Socialite;

    $user = Socialite::driver('twitter')->userFromTokenAndSecret($token, $secret);

<a name="stateless-authentication"></a>
#### ステートレス認証

`stateless` メソッドを使用して、セッション状態の検証を無効にすることができます。これは、Cookie ベースのセッションを使用しないステートレス API にソーシャル認証を追加する場合に便利です。

    use Laravel\Socialite\Facades\Socialite;

    return Socialite::driver('google')->stateless()->user();

> **警告**
> ステートレス認証は Twitter OAuth 1.0 ドライバでは使用できません。

