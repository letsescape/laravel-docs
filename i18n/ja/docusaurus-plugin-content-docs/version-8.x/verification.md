# メール認証 (Email Verification)

- [Introduction](#introduction)
    - [モデルの準備](#model-preparation)
    - [データベースの準備](#database-preparation)
- [Routing](#verification-routing)
    - [電子メール認証通知](#the-email-verification-notice)
    - [電子メール検証ハンドラー](#the-email-verification-handler)
    - [確認メールの再送信](#resending-the-verification-email)
    - [ルートを守る](#protecting-routes)
- [Customization](#customization)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

多くの Web アプリケーションでは、ユーザーはアプリケーションを使用する前に電子メール アドレスを確認する必要があります。 Laravel では、作成するアプリケーションごとにこの機能を手動で再実装する必要がなく、電子メール検証リクエストを送信および検証するための便利な組み込みサービスが提供されます。

> {tip} すぐに始めたいですか?新しい Laravel アプリケーションに [Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) の 1 つをインストールします。スターター キットは、電子メール検証サポートを含む認証システム全体の足場を処理します。

<a name="model-preparation"></a>
### モデルの準備

開始する前に、`App\Models\User` モデルが `Illuminate\Contracts\Auth\MustVerifyEmail` コントラクトを実装していることを確認してください。

    <?php

    namespace App\Models;

    use Illuminate\Contracts\Auth\MustVerifyEmail;
    use Illuminate\Foundation\Auth\User as Authenticatable;
    use Illuminate\Notifications\Notifiable;

    class User extends Authenticatable implements MustVerifyEmail
    {
        use Notifiable;

        // ...
    }

このインターフェースがモデルに追加されると、新規登録ユーザーには、電子メール検証リンクを含む電子メールが自動的に送信されます。アプリケーションの `App\Providers\EventServiceProvider` を調べるとわかるように、Laravel には、`Illuminate\Auth\Events\Registered` イベントに関連付けられた `SendEmailVerificationNotification` [listener](/docs/{{version}}/events) がすでに含まれています。このイベント リスナは、電子メール検証リンクをユーザーに送信します。

[スターターキット](/docs/{{version}}/starter-kits) を使用する代わりにアプリケーション内で登録を手動で実装している場合は、ユーザーの登録が成功した後に `Illuminate\Auth\Events\Registered` イベントをディスパッチしていることを確認する必要があります。

    use Illuminate\Auth\Events\Registered;

    event(new Registered($user));

<a name="database-preparation"></a>
### データベースの準備

次に、`users` テーブルには、ユーザーの電子メール アドレスが検証された日時を保存する `email_verified_at` 列が含まれている必要があります。デフォルトでは、Laravel フレームワークに含まれる `users` テーブルの移行には、この列がすでに含まれています。したがって、必要なのはデータベースの移行を実行することだけです。

    php artisan migrate

<a name="verification-routing"></a>
## ルーティング (Routing)

電子メール検証を適切に実装するには、3 つのルートを定義する必要があります。まず、登録後に Laravel から送信された確認メール内のメール確認リンクをクリックする必要があるという通知をユーザーに表示するルートが必要です。

次に、ユーザーが電子メール内の電子メール検証リンクをクリックしたときに生成されるリクエストを処理するためのルートが必要になります。

3 番目に、ユーザーが最初の検証リンクを誤って失った場合に検証リンクを再送信するためのルートが必要になります。

<a name="the-email-verification-notice"></a>
### 電子メール認証通知

前述したように、登録後に Laravel から電子メールで送信された電子メール検証リンクをクリックするようにユーザーに指示するビューを返すルートを定義する必要があります。このビューは、ユーザーが最初に電子メール アドレスを確認せずにアプリケーションの他の部分にアクセスしようとしたときに表示されます。 `App\Models\User` モデルが `MustVerifyEmail` インターフェイスを実装している限り、リンクはユーザーに自動的に電子メールで送信されることに注意してください。

    Route::get('/email/verify', function () {
        return view('auth.verify-email');
    })->middleware('auth')->name('verification.notice');

電子メール検証通知を返すルートには、`verification.notice` という名前を付ける必要があります。ユーザーが電子メール アドレスを確認していない場合、`verified` ミドルウェア [Laravelに付属](#protecting-routes) が自動的にこのルート名にリダイレクトするため、ルートにこの正確な名前が割り当てられることが重要です。

> {tip} メール検証を手動で実装する場合は、検証通知ビューの内容を自分で定義する必要があります。必要なすべての認証ビューと検証ビューを含むスキャフォールディングが必要な場合は、[Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) を確認してください。

<a name="the-email-verification-handler"></a>
### 電子メール検証ハンドラー

次に、電子メールで送信された電子メール検証リンクをユーザーがクリックしたときに生成されるリクエストを処理するルートを定義する必要があります。このルートには `verification.verify` という名前を付け、`auth` および `signed` ミドルウェアを割り当てる必要があります。

    use Illuminate\Foundation\Auth\EmailVerificationRequest;

    Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
        $request->fulfill();

        return redirect('/home');
    })->middleware(['auth', 'signed'])->name('verification.verify');

次に進む前に、このルートを詳しく見てみましょう。まず、一般的な `Illuminate\Http\Request` インスタンスの代わりに、`EmailVerificationRequest` リクエスト タイプを使用していることがわかります。 `EmailVerificationRequest` は、Laravel に含まれる [フォームリクエスト](/docs/{{version}}/validation#form-request-validation) です。このリクエストは、リクエストの `id` および `hash` パラメータの検証を自動的に処理します。

次に、リクエストに対する `fulfill` メソッドの呼び出しに直接進むことができます。このメソッドは、認証されたユーザーで `markEmailAsVerified` メソッドを呼び出し、`Illuminate\Auth\Events\Verified` イベントを送出します。 `markEmailAsVerified` メソッドは、`Illuminate\Foundation\Auth\User` 基本クラスを介してデフォルトの `App\Models\User` モデルで使用できます。ユーザーの電子メール アドレスが確認されたら、希望する場所にリダイレクトできます。

<a name="resending-the-verification-email"></a>
### 確認メールの再送信

ユーザーが電子メール アドレス確認電子メールを置き忘れたり、誤って削除したりする場合があります。これに対応するには、ユーザーが確認電子メールの再送信を要求できるようにルートを定義するとよいでしょう。次に、[検証通知ビュー](#the-email-verification-notice) 内に簡単なフォーム送信ボタンを配置することで、このルートにリクエストを送信できます。

    use Illuminate\Http\Request;

    Route::post('/email/verification-notification', function (Request $request) {
        $request->user()->sendEmailVerificationNotification();

        return back()->with('message', 'Verification link sent!');
    })->middleware(['auth', 'throttle:6,1'])->name('verification.send');

<a name="protecting-routes"></a>
### ルートを守る

[ルートミドルウェア](/docs/{{version}}/middleware) は、検証済みのユーザーにのみ特定のルートへのアクセスを許可するために使用できます。 Laravel には、`Illuminate\Auth\Middleware\EnsureEmailIsVerified` クラスを参照する `verified` ミドルウェアが付属しています。このミドルウェアはアプリケーションの HTTP カーネルにすでに登録されているため、必要なのはミドルウェアをルート定義にアタッチすることだけです。

    Route::get('/profile', function () {
        // Only verified users may access this route...
    })->middleware('verified');

未検証のユーザーがこのミドルウェアが割り当てられたルートにアクセスしようとすると、自動的に `verification.notice` [名前付きルート](/docs/{{version}}/routing#named-routes) にリダイレクトされます。

<a name="customization"></a>
## カスタマイズ (Customization)

<a name="verification-email-customization"></a>
#### 確認メールのカスタマイズ

デフォルトの電子メール検証通知はほとんどのアプリケーションの要件を満たすはずですが、Laravel では電子メール検証メール メッセージの構築方法をカスタマイズできます。

まず、`Illuminate\Auth\Notifications\VerifyEmail` 通知によって提供される `toMailUsing` メソッドにクロージャーを渡します。クロージャは、通知を受信する通知可能なモデル インスタンスと、ユーザーが電子メール アドレスを確認するためにアクセスする必要がある署名付き電子メール検証 URL を受け取ります。クロージャは `Illuminate\Notifications\Messages\MailMessage` のインスタンスを返す必要があります。通常、アプリケーションの `App\Providers\AuthServiceProvider` クラスの `boot` メソッドから `toMailUsing` メソッドを呼び出す必要があります。

    use Illuminate\Auth\Notifications\VerifyEmail;
    use Illuminate\Notifications\Messages\MailMessage;

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        // ...

        VerifyEmail::toMailUsing(function ($notifiable, $url) {
            return (new MailMessage)
                ->subject('Verify Email Address')
                ->line('Click the button below to verify your email address.')
                ->action('Verify Email Address', $url);
        });
    }

> {tip} メール通知の詳細については、[メール通知のドキュメント](/docs/{{version}}/notifications#mail-notifications) を参照してください。

<a name="events"></a>
## イベント (Events)

[Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) を使用する場合、Laravel は電子メール検証プロセス中に [events](/docs/{{version}}/events) をディスパッチします。アプリケーションの電子メール検証を手動で処理している場合は、検証の完了後にこれらのイベントを手動でディスパッチすることができます。アプリケーションの `EventServiceProvider` でこれらのイベントにリスナをアタッチできます。

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerifiedUser',
        ],
    ];

