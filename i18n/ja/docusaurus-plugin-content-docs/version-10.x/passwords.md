# パスワードのリセット (Resetting Passwords)

- [Introduction](#introduction)
    - [モデルの準備](#model-preparation)
    - [データベースの準備](#database-preparation)
    - [信頼できるホストの構成](#configuring-trusted-hosts)
- [Routing](#routing)
    - [パスワードリセットリンクのリクエスト](#requesting-the-password-reset-link)
    - [パスワードをリセットする](#resetting-the-password)
- [期限切れのトークンの削除](#deleting-expired-tokens)
- [Customization](#password-customization)

<a name="introduction"></a>
## 導入 (Introduction)

ほとんどの Web アプリケーションには、ユーザーが忘れたパスワードをリセットする方法が用意されています。作成するアプリケーションごとにこれを手動で再実装することを強制するのではなく、Laravel は、パスワードリセット リンクを送信し、パスワードを安全にリセットするための便利なサービスを提供します。

> [!NOTE]  
> すぐに始めたいですか?新しい Laravel アプリケーションに Laravel [アプリケーションスターターキット](/docs/{{version}}/starter-kits) をインストールします。 Laravel のスターター キットは、忘れたパスワードのリセットを含む、認証システム全体の足場を処理します。

<a name="model-preparation"></a>
### モデルの準備

Laravel のパスワードリセット機能を使用する前に、アプリケーションの `App\Models\User` モデルは `Illuminate\Notifications\Notifiable` トレイトを使用する必要があります。通常、この特性は、新しい Laravel アプリケーションで作成されるデフォルトの `App\Models\User` モデルにすでに含まれています。

次に、`App\Models\User` モデルが `Illuminate\Contracts\Auth\CanResetPassword` コントラクトを実装していることを確認します。フレームワークに含まれる `App\Models\User` モデルはすでにこのインターフェイスを実装しており、`Illuminate\Auth\Passwords\CanResetPassword` 特性を使用してインターフェイスの実装に必要なメソッドを含めています。

<a name="database-preparation"></a>
### データベースの準備

アプリケーションのパスワードリセット トークンを保存するテーブルを作成する必要があります。このテーブルの移行はデフォルトの Laravel アプリケーションに含まれているため、データベースを移行してこのテーブルを作成するだけで済みます。

```shell
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
### 信頼できるホストの構成

デフォルトでは、Laravel は、HTTP リクエストの `Host` ヘッダーの内容に関係なく、受信したすべてのリクエストに応答します。さらに、`Host` ヘッダーの値は、Web リクエスト中にアプリケーションへの絶対 URL を生成するときに使用されます。

通常、指定されたホスト名に一致するリクエストのみをアプリケーションに送信するように、Nginx や Apache などの Web サーバーを構成する必要があります。ただし、Web サーバーを直接カスタマイズする機能がなく、特定のホスト名にのみ応答するように Laravel に指示する必要がある場合は、アプリケーションの `App\Http\Middleware\TrustHosts` ミドルウェアを有効にすることでこれを行うことができます。これは、アプリケーションがパスワードリセット機能を提供する場合に特に重要です。

このミドルウェアの詳細については、[`TrustHosts` ミドルウェアのドキュメント](/docs/{{version}}/requests#configuring-trusted-hosts) を参照してください。

<a name="routing"></a>
## ルーティング (Routing)

ユーザーがパスワードをリセットできるようにするサポートを適切に実装するには、いくつかのルートを定義する必要があります。まず、ユーザーが電子メール アドレス経由でパスワードリセット リンクをリクエストできるようにするためのルートのペアが必要です。次に、ユーザーが電子メールで送信されたパスワードリセット リンクにアクセスし、パスワードリセット フォームに記入した後で、実際にパスワードをリセットする処理を行うための 1 組のルートが必要です。

<a name="requesting-the-password-reset-link"></a>
### パスワードリセットリンクのリクエスト

<a name="the-password-reset-link-request-form"></a>
#### パスワードリセットリンクリクエストフォーム

まず、パスワードリセット リンクを要求するために必要なルートを定義します。まず、パスワードリセット リンク リクエスト フォームを含むビューを返すルートを定義します。

    Route::get('/forgot-password', function () {
        return view('auth.forgot-password');
    })->middleware('guest')->name('password.request');

このルートによって返されるビューには、`email` フィールドを含むフォームが必要です。これにより、ユーザーは特定の電子メール アドレスのパスワードリセット リンクを要求できます。

<a name="password-reset-link-handling-the-form-submission"></a>
#### フォーム送信の処理

次に、「パスワードを忘れた場合」ビューからのフォーム送信リクエストを処理するルートを定義します。このルートは、電子メール アドレスを検証し、対応するユーザーにパスワードリセット リクエストを送信する役割を果たします。

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Password;

    Route::post('/forgot-password', function (Request $request) {
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        return $status === Password::RESET_LINK_SENT
                    ? back()->with(['status' => __($status)])
                    : back()->withErrors(['email' => __($status)]);
    })->middleware('guest')->name('password.email');

次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `email` 属性が検証されます。次に、Laravel の組み込み「パスワード ブローカー」を (`Password` ファサード経由で) 使用して、パスワードリセット リンクをユーザーに送信します。パスワードブローカーは、指定されたフィールド (この場合は電子メールアドレス) によるユーザーの取得と、Laravel の組み込み [通知システム](/docs/{{version}}/notifications) を介したパスワードリセットリンクの送信を処理します。

`sendResetLink` メソッドは、「ステータス」スラッグを返します。このステータスは、リクエストのステータスに関するわかりやすいメッセージをユーザーに表示するために、Laravel の [localization](/docs/{{version}}/localization) ヘルパを使用して変換できます。パスワードリセット ステータスの翻訳は、アプリケーションの `lang/{lang}/passwords.php` 言語ファイルによって決まります。ステータス スラッグの考えられる各値のエントリは、`passwords` 言語ファイル内にあります。

> [!NOTE]  
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

`Password` ファサードの `sendResetLink` メソッドを呼び出すときに、Laravel がアプリケーションのデータベースからユーザー レコードを取得する方法をどのように認識するのか疑問に思われるかもしれません。 Laravel パスワードブローカーは、認証システムの「ユーザープロバイダ」を利用してデータベースレコードを取得します。パスワード ブローカーによって使用されるユーザー プロバイダは、`config/auth.php` 構成ファイルの `passwords` 構成配列内で構成されます。カスタム ユーザー プロバイダの作成の詳細については、[認証ドキュメント](/docs/{{version}}/authentication#adding-custom-user-providers) を参照してください。

> [!NOTE]  
> パスワードのリセットを手動で実装する場合は、ビューとルートの内容を自分で定義する必要があります。必要な認証および検証ロジックをすべて含むスキャフォールディングが必要な場合は、[Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) を確認してください。

<a name="resetting-the-password"></a>
### パスワードをリセットする

<a name="the-password-reset-form"></a>
#### パスワードリセットフォーム

次に、ユーザーが電子メールで送信されたパスワードリセット リンクをクリックして新しいパスワードを入力した後、実際にパスワードをリセットするために必要なルートを定義します。まず、ユーザーがパスワードのリセット リンクをクリックしたときに表示されるパスワードのリセット フォームを表示するルートを定義しましょう。このルートは、後でパスワードリセット要求を確認するために使用する `token` パラメーターを受け取ります。

    Route::get('/reset-password/{token}', function (string $token) {
        return view('auth.reset-password', ['token' => $token]);
    })->middleware('guest')->name('password.reset');

このルートによって返されるビューには、`email` フィールド、`password` フィールド、`password_confirmation` フィールド、および非表示の `token` フィールドを含むフォームが表示されます。これらのフィールドには、ルートによって受信されたシークレット `$token` の値が含まれている必要があります。

<a name="password-reset-handling-the-form-submission"></a>
#### フォーム送信の処理

もちろん、パスワードリセット フォームの送信を実際に処理するルートを定義する必要があります。このルートは、受信リクエストの検証とデータベース内のユーザーのパスワードの更新を担当します。

    use App\Models\User;
    use Illuminate\Auth\Events\PasswordReset;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Support\Facades\Password;
    use Illuminate\Support\Str;

    Route::post('/reset-password', function (Request $request) {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|min:8|confirmed',
        ]);

        $status = Password::reset(
            $request->only('email', 'password', 'password_confirmation', 'token'),
            function (User $user, string $password) {
                $user->forceFill([
                    'password' => Hash::make($password)
                ])->setRememberToken(Str::random(60));

                $user->save();

                event(new PasswordReset($user));
            }
        );

        return $status === Password::PASSWORD_RESET
                    ? redirect()->route('login')->with('status', __($status))
                    : back()->withErrors(['email' => [__($status)]]);
    })->middleware('guest')->name('password.update');

次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `token`、`email`、および `password` 属性が検証されます。次に、Laravel の組み込み「パスワード ブローカー」を (`Password` ファサード経由で) 使用して、パスワードリセット要求の資格情報を検証します。

パスワード ブローカーに指定されたトークン、電子メール アドレス、およびパスワードが有効な場合、`reset` メソッドに渡されたクロージャが呼び出されます。ユーザー インスタンスとパスワードリセット フォームに提供されたプレーンテキストのパスワードを受け取るこのクロージャー内で、データベース内のユーザーのパスワードを更新できます。

`reset` メソッドは、「ステータス」スラッグを返します。このステータスは、リクエストのステータスに関するわかりやすいメッセージをユーザーに表示するために、Laravel の [localization](/docs/{{version}}/localization) ヘルパを使用して変換できます。パスワードリセット ステータスの翻訳は、アプリケーションの `lang/{lang}/passwords.php` 言語ファイルによって決まります。ステータス スラッグの考えられる各値のエントリは、`passwords` 言語ファイル内にあります。アプリケーションに `lang` ディレクトリが含まれていない場合は、`lang:publish` Artisan コマンドを使用してディレクトリを作成できます。

次に進む前に、`Password` ファサードの `reset` メソッドを呼び出すときに、Laravel がアプリケーションのデータベースからユーザー レコードを取得する方法をどのように認識するのか疑問に思うかもしれません。 Laravel パスワードブローカーは、認証システムの「ユーザープロバイダ」を利用してデータベースレコードを取得します。パスワード ブローカーによって使用されるユーザー プロバイダは、`config/auth.php` 構成ファイルの `passwords` 構成配列内で構成されます。カスタム ユーザー プロバイダの作成の詳細については、[認証ドキュメント](/docs/{{version}}/authentication#adding-custom-user-providers) を参照してください。

<a name="deleting-expired-tokens"></a>
## 期限切れのトークンの削除 (Deleting Expired Tokens)

有効期限が切れたパスワードリセット トークンはデータベース内に残ります。ただし、`auth:clear-resets` Artisan コマンドを使用すると、これらのレコードを簡単に削除できます。

```shell
php artisan auth:clear-resets
```

このプロセスを自動化したい場合は、アプリケーションの [scheduler](/docs/{{version}}/scheduling) にコマンドを追加することを検討してください。

    $schedule->command('auth:clear-resets')->everyFifteenMinutes();

<a name="password-customization"></a>
## カスタマイズ (Customization)

<a name="reset-link-customization"></a>
#### リンクのカスタマイズをリセットする

`ResetPassword` 通知クラスによって提供される `createUrlUsing` メソッドを使用して、パスワードリセット リンク URL をカスタマイズできます。このメソッドは、通知を受け取るユーザー インスタンスとパスワードリセット リンク トークンを受け取るクロージャを受け入れます。通常、このメソッドは `App\Providers\AuthServiceProvider` サービスプロバイダの `boot` メソッドから呼び出す必要があります。

    use App\Models\User;
    use Illuminate\Auth\Notifications\ResetPassword;

    /**
     * Register any authentication / authorization services.
     */
    public function boot(): void
    {
        ResetPassword::createUrlUsing(function (User $user, string $token) {
            return 'https://example.com/reset-password?token='.$token;
        });
    }

<a name="reset-email-customization"></a>
#### 電子メールのカスタマイズをリセット

パスワードリセット リンクをユーザーに送信するために使用される通知クラスは簡単に変更できます。まず、`App\Models\User` モデルの `sendPasswordResetNotification` メソッドをオーバーライドします。このメソッド内で、独自に作成した [通知クラス](/docs/{{version}}/notifications) を使用して通知を送信できます。パスワードリセット `$token` は、メソッドによって受け取られる最初の引数です。この `$token` を使用して、選択したパスワードリセット URL を構築し、ユーザーに通知を送信できます。

    use App\Notifications\ResetPasswordNotification;

    /**
     * Send a password reset notification to the user.
     *
     * @param  string  $token
     */
    public function sendPasswordResetNotification($token): void
    {
        $url = 'https://example.com/reset-password?token='.$token;

        $this->notify(new ResetPasswordNotification($url));
    }

