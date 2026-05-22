# Laravel の強化 (Laravel Fortify)

- [Introduction](#introduction)
    - [強化とは何ですか?](#what-is-fortify)
    - [Fortify をいつ使用する必要がありますか?](#when-should-i-use-fortify)
- [Installation](#installation)
    - [Fortify サービスプロバイダ](#the-fortify-service-provider)
    - [機能を強化する](#fortify-features)
    - [ビューの無効化](#disabling-views)
- [Authentication](#authentication)
    - [ユーザー認証のカスタマイズ](#customizing-user-authentication)
    - [認証パイプラインのカスタマイズ](#customizing-the-authentication-pipeline)
    - [リダイレクトのカスタマイズ](#customizing-authentication-redirects)
- [二要素認証](#two-factor-authentication)
    - [2 要素認証の有効化](#enabling-two-factor-authentication)
    - [2 要素認証による認証](#authenticating-with-two-factor-authentication)
    - [2 要素認証の無効化](#disabling-two-factor-authentication)
- [Registration](#registration)
    - [登録のカスタマイズ](#customizing-registration)
- [パスワードのリセット](#password-reset)
    - [パスワードリセットリンクのリクエスト](#requesting-a-password-reset-link)
    - [パスワードをリセットする](#resetting-the-password)
    - [パスワードのリセットのカスタマイズ](#customizing-password-resets)
- [メール認証](#email-verification)
    - [ルートを守る](#protecting-routes)
- [パスワードの確認](#password-confirmation)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel の強化](https://github.com/laravel/fortify) は、Laravel のフロントエンドに依存しない認証バックエンド実装です。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などを含む、Laravel のすべての認証機能を実装するために必要なルートとコントローラを登録します。 Fortify をインストールした後、`route:list` Artisan コマンドを実行して、Fortify が登録したルートを確認できます。

Fortify は独自のユーザー インターフェイスを提供していないため、登録されているルートにリクエストを行う独自のユーザー インターフェイスと組み合わせることが意図されています。これらのルートにリクエストを行う方法については、このドキュメントの残りの部分で詳しく説明します。

> [!NOTE]  
> Fortify は、Laravel の認証機能の実装をいち早く開始できるようにすることを目的としたパッケージであることを忘れないでください。 **これを使用する必要はありません。** [authentication](/docs/{{version}}/authentication)、[パスワードのリセット](/docs/{{version}}/passwords)、および [メール認証](/docs/{{version}}/verification) ドキュメントにあるドキュメントに従って、いつでも自由に Laravel の認証サービスと手動で対話できます。

<a name="what-is-fortify"></a>
### 強化とは何ですか?

前述したように、Laravel Fortify は、Laravel のフロントエンドに依存しない認証バックエンド実装です。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などを含む、Laravel のすべての認証機能を実装するために必要なルートとコントローラを登録します。

**Laravel の認証機能を使用するために Fortify を使用する必要はありません。** [authentication](/docs/{{version}}/authentication)、[パスワードのリセット](/docs/{{version}}/passwords)、および [メール認証](/docs/{{version}}/verification) ドキュメントにあるドキュメントに従って、いつでも自由に Laravel の認証サービスを手動で操作できます。

Laravel を初めて使用する場合は、Laravel Fortify を使用する前に、[Laravel Breeze](/docs/{{version}}/starter-kits) アプリケーション スターター キットを検討してください。 Laravel Breeze は、[Tailwind CSS](https://tailwindcss.com) で構築されたユーザー インターフェイスを含むアプリケーションの認証スキャフォールディングを提供します。 Fortify とは異なり、Breeze はルートとコントローラをアプリケーションに直接公開します。これにより、Laravel Fortify にこれらの機能を実装させる前に、Laravel の認証機能を勉強して慣れることができます。

Laravel Fortify は基本的に Laravel Breeze のルートとコントローラを取得し、ユーザーインターフェイスを含まないパッケージとして提供します。これにより、特定のフロントエンドの意見に縛られることなく、アプリケーションの認証層のバックエンド実装を迅速に構築することができます。

<a name="when-should-i-use-fortify"></a>
### Fortify をいつ使用する必要がありますか?

Laravel Fortify をいつ使用するのが適切なのか疑問に思われるかもしれません。まず、Laravel の [アプリケーションスターターキット](/docs/{{version}}/starter-kits) のいずれかを使用している場合は、Laravel のすべてのアプリケーション スターター キットがすでに完全な認証実装を提供しているため、Laravel Fortify をインストールする必要はありません。

アプリケーションスターターキットを使用しておらず、アプリケーションに認証機能が必要な場合、アプリケーションの認証機能を手動で実装するか、Laravel Fortify を使用してこれらの機能のバックエンド実装を提供するかの 2 つのオプションがあります。

Fortify のインストールを選択した場合、ユーザー インターフェイスは、ユーザーを認証して登録するために、このドキュメントで詳しく説明されている Fortify の認証ルートにリクエストを作成します。

Fortify を使用する代わりに Laravel の認証サービスと手動で対話することを選択した場合は、[authentication](/docs/{{version}}/authentication)、[パスワードのリセット](/docs/{{version}}/passwords)、および [メール認証](/docs/{{version}}/verification) ドキュメントで入手可能なドキュメントに従って行うことができます。

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify と Laravel Sanctum

開発者の中には、[Laravel Sanctum](/docs/{{version}}/sanctum) と Laravel Fortify の違いについて混乱する人もいます。 2 つのパッケージは 2 つの異なるが関連する問題を解決するため、Laravel Fortify と Laravel Sanctum は相互に排他的または競合するパッケージではありません。

Laravel Sanctum は、API トークンの管理と、セッション Cookie またはトークンを使用した既存のユーザーの認証のみに関係します。 Sanctum は、ユーザー登録、パスワードのリセットなどを処理するルートを提供しません。

API を提供するアプリケーション、またはシングルページ アプリケーションのバックエンドとして機能するアプリケーションの認証レイヤーを手動で構築しようとしている場合、Laravel Fortify (ユーザー登録、パスワードリセットなど) と Laravel Sanctum (API トークン管理、セッション認証) の両方を利用する可能性があります。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Fortify をインストールします。

```shell
composer require laravel/fortify
```

次に、`vendor:publish` コマンドを使用して Fortify のリソースを公開します。

```shell
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドは、Fortify のアクションを `app/Actions` ディレクトリに公開します。ディレクトリが存在しない場合は作成されます。さらに、`FortifyServiceProvider`、構成ファイル、および必要なすべてのデータベース移行が公開されます。

次に、データベースを移行する必要があります。

```shell
php artisan migrate
```

<a name="the-fortify-service-provider"></a>
### Fortify サービスプロバイダ

上で説明した `vendor:publish` コマンドは、`App\Providers\FortifyServiceProvider` クラスも公開します。このクラスがアプリケーションの `config/app.php` 構成ファイルの `providers` 配列内に登録されていることを確認する必要があります。

Fortify サービスプロバイダは、Fortify が公開したアクションを登録し、それぞれのタスクが Fortify によって実行されるときにそれらを使用するように Fortify に指示します。

<a name="fortify-features"></a>
### 機能を強化する

`fortify` 構成ファイルには、`features` 構成配列が含まれています。この配列は、Fortify がデフォルトで公開するバックエンド ルート/機能を定義します。 Fortify を [Laravel Jetstream](https://jetstream.laravel.com) と組み合わせて使用​​していない場合は、次の機能のみを有効にすることをお勧めします。これらの機能は、ほとんどの Laravel アプリケーションで提供される基本認証機能です。

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
### ビューの無効化

デフォルトでは、Fortify はログイン画面や登録画面などのビューを返すことを目的としたルートを定義します。ただし、JavaScript 駆動の単一ページ アプリケーションを構築している場合は、これらのルートは必要ない場合があります。そのため、アプリケーションの `config/fortify.php` 構成ファイル内の `views` 構成値を `false` に設定することで、これらのルートを完全に無効にすることができます。

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
#### ビューの無効化とパスワードのリセット

Fortify のビューを無効にすることを選択し、アプリケーションにパスワードリセット機能を実装する場合でも、アプリケーションの「パスワードリセット」ビューの表示を担当する `password.reset` という名前のルートを定義する必要があります。これが必要なのは、Laravel の `Illuminate\Auth\Notifications\ResetPassword` 通知が `password.reset` 名前付きルート経由でパスワードリセット URL を生成するためです。

<a name="authentication"></a>
## 認証 (Authentication)

まず、「ログイン」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[アプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用する必要があります。

認証ビューのレンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドはアプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。 Fortify は、このビューを返す `/login` ルートの定義を処理します。

    use Laravel\Fortify\Fortify;

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Fortify::loginView(function () {
            return view('auth.login');
        });

        // ...
    }

ログイン テンプレートには、`/login` への POST リクエストを行うフォームが含まれている必要があります。 `/login` エンドポイントは、文字列 `email` / `username` および `password` を予期します。電子メール/ユーザー名フィールドの名前は、`config/fortify.php` 構成ファイル内の `username` 値と一致する必要があります。さらに、Laravel が提供する「記憶する」機能をユーザーが使用したいことを示すために、ブール値の `remember` フィールドを提供することもできます。

ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にリダイレクトします。ログイン要求が XHR 要求の場合、200 HTTP 応答が返されます。

リクエストが成功しなかった場合、ユーザーはログイン画面にリダイレクトされ、共有 `$errors` [Blade テンプレート変数](/docs/{{version}}/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-user-authentication"></a>
### ユーザー認証のカスタマイズ

Fortify は、提供された資格情報とアプリケーション用に構成された認証ガードに基づいてユーザーを自動的に取得し、認証します。ただし、ログイン資格情報の認証方法やユーザーの取得方法を完全にカスタマイズしたい場合もあります。ありがたいことに、Fortify では、`Fortify::authenticateUsing` メソッドを使用してこれを簡単に実現できます。

このメソッドは、受信 HTTP リクエストを受け取るクロージャを受け入れます。クロージャは、リクエストに添付されたログイン認証情報を検証し、関連付けられたユーザー インスタンスを返す責任があります。資格情報が無効であるか、ユーザーが見つからない場合は、クロージャによって `null` または `false` が返される必要があります。通常、このメソッドは、`FortifyServiceProvider` の `boot` メソッドから呼び出す必要があります。

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```

<a name="authentication-guard"></a>
#### 認証ガード

アプリケーションの `fortify` 構成ファイル内で Fortify によって使用される認証ガードをカスタマイズできます。ただし、構成されたガードが `Illuminate\Contracts\Auth\StatefulGuard` の実装であることを確認する必要があります。 Laravel Fortify を使用して SPA を認証しようとしている場合は、Laravel のデフォルトの `web` ガードを [Laravel Sanctum](https://laravel.com/docs/sanctum) と組み合わせて使用​​する必要があります。

<a name="customizing-the-authentication-pipeline"></a>
### 認証パイプラインのカスタマイズ

Laravel Fortify は、呼び出し可能なクラスのパイプラインを通じてログインリクエストを認証します。必要に応じて、ログイン要求がパイプされるクラスのカスタム パイプラインを定義できます。各クラスには、受信 `Illuminate\Http\Request` インスタンスを受け取る `__invoke` メソッドと、[middleware](/docs/{{version}}/middleware) と同様に、パイプライン内の次のクラスにリクエストを渡すために呼び出される `$next` 変数が必要です。

カスタム パイプラインを定義するには、`Fortify::authenticateThrough` メソッドを使用できます。このメソッドは、ログイン要求をパイプ処理するクラスの配列を返すクロージャを受け入れます。通常、このメソッドは、`App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

以下の例には、独自の変更を行う際の開始点として使用できるデフォルトのパイプライン定義が含まれています。

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

<a name="customizing-authentication-redirects"></a>
### リダイレクトのカスタマイズ

ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にリダイレクトします。ログイン要求が XHR 要求の場合、200 HTTP 応答が返されます。ユーザーがアプリケーションからログアウトすると、ユーザーは `/` URI にリダイレクトされます。

この動作の高度なカスタマイズが必要な場合は、`LoginResponse` および `LogoutResponse` コントラクトの実装を Laravel [サービスコンテナ](/docs/{{version}}/container) にバインドできます。通常、これはアプリケーションの `App\Providers\FortifyServiceProvider` クラスの `register` メソッド内で行う必要があります。

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```

<a name="two-factor-authentication"></a>
## 二要素認証 (Two Factor Authentication)

Fortify の 2 要素認証機能が有効になっている場合、ユーザーは認証プロセス中に 6 桁の数字トークンを入力する必要があります。このトークンは、Google Authenticator などの TOTP 互換モバイル認証アプリケーションから取得できる時間ベースのワンタイム パスワード (TOTP) を使用して生成されます。

開始する前に、アプリケーションの `App\Models\User` モデルが `Laravel\Fortify\TwoFactorAuthenticatable` 特性を使用していることを確認する必要があります。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
 ```

次に、ユーザーが 2 要素認証設定を管理できる画面をアプリケーション内に構築する必要があります。この画面では、ユーザーが 2 要素認証を有効または無効にしたり、2 要素認証リカバリ コードを再生成したりできるようになります。

> デフォルトでは、`fortify` 構成ファイルの `features` 配列は、変更前にパスワードの確認を要求するように Fortify の 2 要素認証設定を指示します。したがって、続行する前に、アプリケーションは Fortify の [パスワードの確認](#password-confirmation) 機能を実装する必要があります。

<a name="enabling-two-factor-authentication"></a>
### 2 要素認証の有効化

2 要素認証の有効化を開始するには、アプリケーションは Fortify によって定義された `/user/two-factor-authentication` エンドポイントに対して POST リクエストを行う必要があります。リクエストが成功すると、ユーザーは前の URL にリダイレクトされ、`status` セッション変数が `two-factor-authentication-enabled` に設定されます。テンプレート内でこの `status` セッション変数を検出すると、適切な成功メッセージが表示されます。リクエストが XHR リクエストの場合、`200` HTTP レスポンスが返されます。

2 要素認証を有効にすることを選択した後も、ユーザーは有効な 2 要素認証コードを入力して 2 要素認証構成を「確認」する必要があります。したがって、「成功」メッセージは、2 要素認証の確認がまだ必要であることをユーザーに通知する必要があります。

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two factor authentication below.
    </div>
@endif
```

次に、ユーザーが認証アプリケーションにスキャンできるように、2 要素認証 QR コードを表示する必要があります。 Blade を使用してアプリケーションのフロントエンドをレンダリングしている場合は、ユーザー インスタンスで利用可能な `twoFactorQrCodeSvg` メソッドを使用して QR コード SVG を取得できます。

```php
$request->user()->twoFactorQrCodeSvg();
```

JavaScript を利用したフロントエンドを構築している場合は、`/user/two-factor-qr-code` エンドポイントに対して XHR GET リクエストを作成して、ユーザーの 2 要素認証 QR コードを取得できます。このエンドポイントは、`svg` キーを含む JSON オブジェクトを返します。

<a name="confirming-two-factor-authentication"></a>
#### 二要素認証の確認

ユーザーの 2 要素認証 QR コードを表示するだけでなく、ユーザーが 2 要素認証構成を「確認」するために有効な認証コードを入力できるテキスト入力を提供する必要があります。このコードは、Fortify によって定義された `/user/confirmed-two-factor-authentication` エンドポイントへの POST リクエストを介して Laravel アプリケーションに提供される必要があります。

リクエストが成功すると、ユーザーは前の URL にリダイレクトされ、`status` セッション変数が `two-factor-authentication-confirmed` に設定されます。

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two factor authentication confirmed and enabled successfully.
    </div>
@endif
```

2 要素認証確認エンドポイントへのリクエストが XHR リクエスト経由で行われた場合、`200` HTTP レスポンスが返されます。

<a name="displaying-the-recovery-codes"></a>
#### リカバリーコードの表示

ユーザーの 2 要素リカバリー コードも表示する必要があります。これらのリカバリ コードを使用すると、モバイル デバイスにアクセスできなくなった場合にユーザーを認証できます。 Blade を使用してアプリケーションのフロントエンドをレンダリングしている場合は、認証されたユーザー インスタンスを介してリカバリ コードにアクセスできます。

```php
(array) $request->user()->recoveryCodes()
```

JavaScript を利用したフロントエンドを構築している場合は、`/user/two-factor-recovery-codes` エンドポイントに対して XHR GET リクエストを行うことができます。このエンドポイントは、ユーザーのリカバリ コードを含む JSON 配列を返します。

ユーザーのリカバリ コードを再生成するには、アプリケーションは `/user/two-factor-recovery-codes` エンドポイントに対して POST リクエストを行う必要があります。

<a name="authenticating-with-two-factor-authentication"></a>
### 2 要素認証による認証

認証プロセス中に、Fortify はユーザーをアプリケーションの 2 要素認証チャレンジ画面に自動的にリダイレクトします。ただし、アプリケーションが XHR ログイン要求を行っている場合、認証試行が成功した後に返される JSON 応答には、`two_factor` ブール型プロパティを持つ JSON オブジェクトが含まれます。この値を調べて、アプリケーションの 2 要素認証チャレンジ画面にリダイレクトする必要があるかどうかを確認する必要があります。

2 要素認証機能の実装を開始するには、2 要素認証チャレンジ ビューを返す方法を Fortify に指示する必要があります。 Fortify の認証ビューのレンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```

Fortify は、このビューを返す `/two-factor-challenge` ルートの定義を処理します。 `two-factor-challenge` テンプレートには、`/two-factor-challenge` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。 `/two-factor-challenge` アクションは、有効な TOTP トークンを含む `code` フィールド、またはユーザーのリカバリ コードの 1 つを含む `recovery_code` フィールドを予期します。

ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にユーザーをリダイレクトします。ログイン要求が XHR 要求の場合、204 HTTP 応答が返されます。

リクエストが成功しなかった場合、ユーザーは 2 要素チャレンジ画面にリダイレクトされ、共有 `$errors` [Blade テンプレート変数](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 経由で検証エラーを確認できるようになります。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="disabling-two-factor-authentication"></a>
### 2 要素認証の無効化

2 要素認証を無効にするには、アプリケーションは `/user/two-factor-authentication` エンドポイントに対して DELETE リクエストを行う必要があります。 Fortify の 2 要素認証エンドポイントでは、呼び出される前に [パスワードの確認](#password-confirmation) が必要であることに注意してください。

<a name="registration"></a>
## 登録 (Registration)

アプリケーションの登録機能の実装を開始するには、「登録」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[アプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用する必要があります。

Fortify のビュー レンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、`App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```

Fortify は、このビューを返す `/register` ルートの定義を処理します。 `register` テンプレートには、Fortify によって定義された `/register` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。

`/register` エンドポイントは、文字列 `name`、文字列の電子メール アドレス/ユーザー名、`password`、および `password_confirmation` フィールドを予期します。電子メール/ユーザー名フィールドの名前は、アプリケーションの `fortify` 構成ファイル内で定義された `username` 構成値と一致する必要があります。

登録の試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にユーザーをリダイレクトします。リクエストが XHR リクエストの場合、201 HTTP レスポンスが返されます。

リクエストが成功しなかった場合、ユーザーは登録画面にリダイレクトされ、共有 `$errors` [Blade テンプレート変数](/docs/{{version}}/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-registration"></a>
### 登録のカスタマイズ

ユーザー検証および作成プロセスは、Laravel Fortify のインストール時に生成された `App\Actions\Fortify\CreateNewUser` アクションを変更することでカスタマイズできます。

<a name="password-reset"></a>
## パスワードのリセット (Password Reset)

<a name="requesting-a-password-reset-link"></a>
### パスワードリセットリンクのリクエスト

アプリケーションのパスワードリセット機能の実装を開始するには、「パスワードを忘れた場合」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[アプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用する必要があります。

Fortify のビュー レンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```

Fortify は、このビューを返す `/forgot-password` エンドポイントの定義を処理します。 `forgot-password` テンプレートには、`/forgot-password` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。

`/forgot-password` エンドポイントは文字列 `email` フィールドを予期します。このフィールド/データベース列の名前は、アプリケーションの `fortify` 構成ファイル内の `email` 構成値と一致する必要があります。

<a name="handling-the-password-reset-link-request-response"></a>
#### パスワードリセット リンク要求応答の処理

パスワードリセット リンク リクエストが成功した場合、Fortify はユーザーを `/forgot-password` エンドポイントにリダイレクトし、パスワードのリセットに使用できる安全なリンクを含む電子メールをユーザーに送信します。リクエストが XHR リクエストの場合、200 HTTP レスポンスが返されます。

リクエストが成功した後に `/forgot-password` エンドポイントにリダイレクトされた後、`status` セッション変数を使用して、パスワードリセット リンク リクエスト試行のステータスを表示できます。

`$status` セッション変数の値は、アプリケーションの `passwords` [言語ファイル](/docs/{{version}}/localization) 内で定義された変換文字列の 1 つと一致します。この値をカスタマイズしたいが、Laravel の言語ファイルを公開していない場合は、`lang:publish` Artisan コマンドを使用してカスタマイズできます。

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

リクエストが成功しなかった場合、ユーザーはパスワードリセット リンクのリクエスト画面にリダイレクトされ、共有 `$errors` [Blade テンプレート変数](/docs/{{version}}/validation#quick-displaying-the-validation-errors) 経由で検証エラーを確認できるようになります。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="resetting-the-password"></a>
### パスワードをリセットする

アプリケーションのパスワードリセット機能の実装を完了するには、Fortify に「パスワードのリセット」ビューを返す方法を指示する必要があります。

Fortify のビュー レンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```

Fortify は、このビューを表示するルートの定義を処理します。 `reset-password` テンプレートには、`/reset-password` への POST リクエストを行うフォームが含まれている必要があります。

`/reset-password` エンドポイントは、文字列 `email` フィールド、`password` フィールド、`password_confirmation` フィールド、および `request()->route('token')` の値を含む `token` という名前の隠しフィールドを期待します。 「電子メール」フィールド/データベース列の名前は、アプリケーションの `fortify` 構成ファイル内で定義された `email` 構成値と一致する必要があります。

<a name="handling-the-password-reset-response"></a>
#### パスワードリセット応答の処理

パスワードのリセット要求が成功した場合、Fortify は `/login` ルートにリダイレクトして戻り、ユーザーが新しいパスワードでログインできるようにします。さらに、ログイン画面にリセットの成功ステータスを表示できるように、`status` セッション変数が設定されます。

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

リクエストが XHR リクエストの場合、200 HTTP レスポンスが返されます。

リクエストが成功しなかった場合、ユーザーはパスワードのリセット画面にリダイレクトされ、共有 `$errors` [Blade テンプレート変数](/docs/{{version}}/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-password-resets"></a>
### パスワードのリセットのカスタマイズ

パスワードのリセットプロセスは、Laravel Fortify のインストール時に生成された `App\Actions\ResetUserPassword` アクションを変更することでカスタマイズできます。

<a name="email-verification"></a>
## メール認証 (Email Verification)

登録後、ユーザーがアプリケーションへのアクセスを続ける前に、自分の電子メール アドレスを確認するように求めることができます。開始するには、`emailVerification` 機能が `fortify` 構成ファイルの `features` 配列で有効になっていることを確認してください。次に、`App\Models\User` クラスが `Illuminate\Contracts\Auth\MustVerifyEmail` インターフェイスを実装していることを確認する必要があります。

これら 2 つのセットアップ手順が完了すると、新規登録ユーザーは、電子メール アドレスの所有権を確認するよう求める電子メールを受け取ります。ただし、メール内の確認リンクをクリックする必要があることをユーザーに通知するメール確認画面を表示する方法を Fortify に通知する必要があります。

Fortify のビューのレンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```

Fortify は、Laravel の組み込み `verified` ミドルウェアによってユーザーが `/email/verify` エンドポイントにリダイレクトされるときに、このビューを表示するルートの定義を処理します。

`verify-email` テンプレートには、電子メール アドレスに送信された電子メール検証リンクをクリックするようにユーザーに指示する情報メッセージが含まれている必要があります。

<a name="resending-email-verification-links"></a>
#### 電子メール検証リンクの再送信

必要に応じて、`/email/verification-notification` エンドポイントへの POST リクエストをトリガーするボタンをアプリケーションの `verify-email` テンプレートに追加できます。このエンドポイントがリクエストを受信すると、新しい検証電子メール リンクがユーザーに電子メールで送信されます。これにより、以前の検証リンクが誤って削除または紛失した場合でも、ユーザーは新しい検証リンクを取得できるようになります。

検証リンク電子メールの再送信リクエストが成功した場合、Fortify は `status` セッション変数を使用してユーザーを `/email/verify` エンドポイントにリダイレクトし、操作が成功したことを知らせる情報メッセージをユーザーに表示できるようにします。リクエストが XHR リクエストの場合、202 HTTP レスポンスが返されます。

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
### ルートを守る

ルートまたはルートのグループでユーザーが電子メール アドレスを検証していることを要求するように指定するには、Laravel の組み込み `verified` ミドルウェアをルートにアタッチする必要があります。このミドルウェアは、アプリケーションの `App\Http\Kernel` クラス内に登録されます。

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
## パスワードの確認 (Password Confirmation)

アプリケーションの構築中に、アクションを実行する前にユーザーにパスワードの確認を要求するアクションが発生する場合があります。通常、これらのルートは、Laravel の組み込み `password.confirm` ミドルウェアによって保護されます。

パスワード確認機能の実装を開始するには、アプリケーションの「パスワード確認」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[アプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用する必要があります。

Fortify のビュー レンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドは、アプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify は、このビューを返す `/user/confirm-password` エンドポイントの定義を処理します。 `confirm-password` テンプレートには、`/user/confirm-password` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。 `/user/confirm-password` エンドポイントは、ユーザーの現在のパスワードを含む `password` フィールドを予期します。

パスワードがユーザーの現在のパスワードと一致する場合、Fortify はユーザーをアクセスしようとしていたルートにリダイレクトします。リクエストが XHR リクエストの場合、201 HTTP レスポンスが返されます。

リクエストが成功しなかった場合、ユーザーはパスワード確認画面にリダイレクトされ、共有の `$errors` Blade テンプレート変数を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

