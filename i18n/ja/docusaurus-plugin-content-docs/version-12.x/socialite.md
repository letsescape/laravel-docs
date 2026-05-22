# Laravel Socialite (Laravel Socialite)

- [Introduction](#introduction)
- [Installation](#installation)
- [Socialite のアップグレード](#upgrading-socialite)
- [Configuration](#configuration)
- [Authentication](#authentication)
    - [Routing](#routing)
    - [認証とストレージ](#authentication-and-storage)
    - [アクセス範囲](#access-scopes)
    - [Slack ボットのスコープ](#slack-bot-scopes)
    - [オプションのパラメータ](#optional-parameters)
- [ユーザー詳細の取得](#retrieving-user-details)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

一般的なフォームベースの認証に加えて、Laravel は、[Laravel Socialite](https://github.com/laravel/socialite) を使用して OAuth プロバイダで認証する簡単で便利な方法も提供します。 Socialite は現在、Facebook、X、LinkedIn、Google、GitHub、GitLab、Bitbucket、Slack による認証をサポートしています。

> [!NOTE]
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

これらの資格情報はアプリケーションの `config/services.php` 構成ファイルに配置する必要があり、キー `facebook`、`x`、`linkedin-openid`、`google`、`github`、`gitlab`、`bitbucket`、を使用する必要があります。アプリケーションが必要とするプロバイダに応じて、`slack` または `slack-openid`:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],
```

> [!NOTE]
> `redirect` オプションに相対パスが含まれている場合、完全修飾 URL に自動的に解決されます。

<a name="authentication"></a>
## 認証 (Authentication)

<a name="routing"></a>
### ルーティング

OAuth プロバイダを使用してユーザーを認証するには、2 つのルートが必要です。1 つはユーザーを OAuth プロバイダにリダイレクトするルート、もう 1 つは認証後にプロバイダからコールバックを受信するルートです。以下のルート例は、両方のルートの実装を示しています。

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});
```

`Socialite` ファサードによって提供される `redirect` メソッドは、ユーザーを OAuth プロバイダにリダイレクトします。一方、`user` メソッドは受信リクエストを検査し、認証リクエストが承認された後にプロバイダからユーザーの情報を取得します。

<a name="authentication-and-storage"></a>
### 認証とストレージ

OAuth プロバイダからユーザーを取得したら、そのユーザーがアプリケーションのデータベースと [ユーザーを認証する](/docs/{{version}}/authentication#authenticate-a-user-instance) に存在するかどうかを確認できます。ユーザーがアプリケーションのデータベースに存在しない場合は、通常、ユーザーを表す新しいレコードをデータベースに作成します。

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

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
```

> [!NOTE]
> 特定の OAuth プロバイダからどのようなユーザー情報が入手できるかについて詳しくは、[ユーザー詳細の取得](#retrieving-user-details) のドキュメントを参照してください。

<a name="access-scopes"></a>
### アクセス範囲

ユーザーをリダイレクトする前に、`scopes` メソッドを使用して、認証リクエストに含める必要がある「スコープ」を指定できます。このメソッドは、以前に指定したすべてのスコープを指定したスコープとマージします。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();
```

`setScopes` メソッドを使用して、認証リクエストの既存のスコープをすべて上書きできます。

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();
```

<a name="slack-bot-scopes"></a>
### Slack ボットのスコープ

Slack の API は [さまざまな種類のアクセストークン](https://api.slack.com/authentication/token-types) を提供し、それぞれに独自の [権限の範囲](https://api.slack.com/scopes) セットが含まれます。 Socialite は、次の両方の Slack アクセス トークン タイプと互換性があります。

<div class="content-list" markdown="1">

- ボット (接頭辞 `xoxb-`)
- ユーザー (接頭辞 `xoxp-`)

</div>

デフォルトでは、`slack` ドライバは `user` トークンを生成し、ドライバの `user` メソッドを呼び出すとユーザーの詳細が返されます。

ボット トークンは、アプリケーションのユーザーが所有する外部 Slack ワークスペースにアプリケーションが通知を送信する場合に主に役立ちます。ボット トークンを生成するには、認証のためにユーザーを Slack にリダイレクトする前に、`asBotUser` メソッドを呼び出します。

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();
```

さらに、認証後に Slack がユーザーをアプリケーションにリダイレクトした後、`user` メソッドを呼び出す前に、`asBotUser` メソッドを呼び出す必要があります。

```php
$user = Socialite::driver('slack')->asBotUser()->user();
```

ボット トークンを生成する場合、`user` メソッドは引き続き `Laravel\Socialite\Two\User` インスタンスを返します。ただし、`token` プロパティのみがハイドレートされます。このトークンは、[認証されたユーザーの Slack ワークスペースに通知を送信する](/docs/{{version}}/notifications#notifying-external-slack-workspaces) に保存される場合があります。

<a name="optional-parameters"></a>
### オプションのパラメータ

多くの OAuth プロバイダは、リダイレクト要求の他のオプションのパラメーターをサポートしています。リクエストにオプションのパラメーターを含めるには、連想配列を使用して `with` メソッドを呼び出します。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();
```

> [!WARNING]
> `with` メソッドを使用する場合は、`state` や `response_type` などの予約キーワードを渡さないように注意してください。

<a name="retrieving-user-details"></a>
## ユーザー詳細の取得 (Retrieving User Details)

ユーザーがアプリケーションの認証コールバック ルートにリダイレクトされた後、Socialite の `user` メソッドを使用してユーザーの詳細を取得できます。 `user` メソッドによって返されるユーザー オブジェクトは、ユーザーに関する情報を独自のデータベースに保存するために使用できるさまざまなプロパティとメソッドを提供します。

認証に使用する OAuth プロバイダが OAuth 1.0 と OAuth 2.0 のどちらをサポートしているかに応じて、このオブジェクトでは異なるプロパティとメソッドを使用できる場合があります。

```php
use Laravel\Socialite\Socialite;

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
```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### トークンからのユーザー詳細の取得

ユーザーの有効なアクセス トークンをすでに持っている場合は、Socialite の `userFromToken` メソッドを使用してユーザーの詳細を取得できます。

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);
```

iOS アプリケーション経由で Facebook 限定ログインを使用している場合、Facebook はアクセス トークンの代わりに OIDC トークンを返します。アクセス トークンと同様に、ユーザーの詳細を取得するために、OIDC トークンを `userFromToken` メソッドに提供できます。

<a name="stateless-authentication"></a>
#### ステートレス認証

`stateless` メソッドを使用して、セッション状態の検証を無効にすることができます。これは、Cookie ベースのセッションを使用しないステートレス API にソーシャル認証を追加する場合に便利です。

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();
```

<a name="testing"></a>
## テスト (Testing)

Laravel Socialite は、OAuth プロバイダに実際のリクエストを行わずに OAuth 認証フローをテストする便利な方法を提供します。 `fake` メソッドを使用すると、OAuth プロバイダの動作を模擬し、返されるユーザー データを定義できます。

<a name="faking-the-redirect"></a>
#### リダイレクトを偽装する

アプリケーションがユーザーを OAuth プロバイダに正しくリダイレ​​クトすることをテストするには、リダイレクト ルートにリクエストを行う前に `fake` メソッドを呼び出します。これにより、Socialite は実際の OAuth プロバイダにリダイレクトするのではなく、偽の認証 URL へのリダイレクトを返します。

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});
```

<a name="faking-the-callback"></a>
#### コールバックを偽装する

アプリケーションのコールバック ルートをテストするには、`fake` メソッドを呼び出し、アプリケーションがプロバイダにユーザーの詳細を要求したときに返される `User` インスタンスを指定します。 `User` インスタンスは、`map` メソッドを使用して作成できます。

```php
use Laravel\Socialite\Socialite;
use Laravel\Socialite\Two\User;

test('user can login with github', function () {
    Socialite::fake('github', (new User)->map([
        'id' => 'github-123',
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
    ]));

    $response = $this->get('/auth/github/callback');

    $response->assertRedirect('/dashboard');

    $this->assertDatabaseHas('users', [
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
        'github_id' => 'github-123',
    ]);
});
```

デフォルトでは、`User` インスタンスには `token` プロパティも含まれます。必要に応じて、`User` インスタンスに追加のプロパティを手動で指定できます。

```php
$fakeUser = (new User)->map([
    'id' => 'github-123',
    'name' => 'Jason Beggs',
    'email' => 'jason@example.com',
])->setToken('fake-token')
  ->setRefreshToken('fake-refresh-token')
  ->setExpiresIn(3600)
  ->setApprovedScopes(['read', 'write'])
```

