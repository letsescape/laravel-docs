<!-- # Resetting Passwords -->
# Resetting Passwords

- [Introduction](#introduction)
    - [Model Preparation](#model-preparation)
    - [Database Preparation](#database-preparation)
    - [Configuring Trusted Hosts](#configuring-trusted-hosts)
- [Routing](#routing)
    - [Requesting The Password Reset Link](#requesting-the-password-reset-link)
    - [Resetting The Password](#resetting-the-password)
- [Deleting Expired Tokens](#deleting-expired-tokens)
- [Customization](#password-customization)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Most web applications provide a way for users to reset their forgotten passwords. Rather than forcing you to re-implement this by hand for every application you create, Laravel provides convenient services for sending password reset links and secure resetting passwords. -->
ほとんどの Web アプリケーションには、ユーザーが忘れたパスワードをリセットする方法が用意されています。作成するアプリケーションごとにこれを手動で再実装することを強制するのではなく、Laravel は、パスワードリセット リンクを送信し、パスワードを安全にリセットするための便利なサービスを提供します。

> [!TIP]
> すぐに始めたいですか?新しい Laravel アプリケーションに Laravel [application starter kit](/docs/8.x/starter-kits) をインストールします。 Laravel のスターター キットは、忘れたパスワードのリセットを含む、認証システム全体の足場を処理します。

<a name="model-preparation"></a>
<!-- ### Model Preparation -->
### Model Preparation

<!-- Before using the password reset features of Laravel, your application's `App\Models\User` model must use the `Illuminate\Notifications\Notifiable` trait. Typically, this trait is already included on the default `App\Models\User` model that is created with new Laravel applications. -->
Laravel のパスワードリセット機能を使用する前に、アプリケーションの `App\Models\User` モデルは `Illuminate\Notifications\Notifiable` トレイトを使用する必要があります。通常、この特性は、新しい Laravel アプリケーションで作成されるデフォルトの `App\Models\User` モデルにすでに含まれています。

<!-- Next, verify that your `App\Models\User` model implements the `Illuminate\Contracts\Auth\CanResetPassword` contract. The `App\Models\User` model included with the framework already implements this interface, and uses the `Illuminate\Auth\Passwords\CanResetPassword` trait to include the methods needed to implement the interface. -->
次に、`App\Models\User` モデルが `Illuminate\Contracts\Auth\CanResetPassword` コントラクトを実装していることを確認します。フレームワークに含まれる `App\Models\User` モデルはすでにこのインターフェイスを実装しており、`Illuminate\Auth\Passwords\CanResetPassword` 特性を使用してインターフェイスの実装に必要なメソッドを含めています。

<a name="database-preparation"></a>
<!-- ### Database Preparation -->
### Database Preparation

<!-- A table must be created to store your application's password reset tokens. The migration for this table is included in the default Laravel application, so you only need to migrate your database to create this table: -->
アプリケーションのパスワードリセット トークンを保存するテーブルを作成する必要があります。このテーブルの移行はデフォルトの Laravel アプリケーションに含まれているため、データベースを移行してこのテーブルを作成するだけで済みます。

```
php artisan migrate
```

<a name="configuring-trusted-hosts"></a>
<!-- ### Configuring Trusted Hosts -->
### Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
デフォルトでは、Laravel は、HTTP リクエストの `Host` ヘッダーの内容に関係なく、受信したすべてのリクエストに応答します。さらに、`Host` ヘッダーの値は、Web リクエスト中にアプリケーションへの絶対 URL を生成するときに使用されます。

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given host name. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain host names, you may do so by enabling the `App\Http\Middleware\TrustHosts` middleware for your application. This is particularly important when your application offers password reset functionality. -->
通常、指定されたホスト名に一致するリクエストのみをアプリケーションに送信するように、Nginx や Apache などの Web サーバーを構成する必要があります。ただし、Web サーバーを直接カスタマイズする機能がなく、特定のホスト名にのみ応答するように Laravel に指示する必要がある場合は、アプリケーションの `App\Http\Middleware\TrustHosts` ミドルウェアを有効にすることでこれを行うことができます。これは、アプリケーションがパスワードリセット機能を提供する場合に特に重要です。

<!-- To learn more about this middleware, please consult the [`TrustHosts` middleware documentation](/docs/8.x/requests#configuring-trusted-hosts). -->
このミドルウェアの詳細については、[`TrustHosts` middleware documentation](/docs/8.x/requests#configuring-trusted-hosts) を参照してください。

<a name="routing"></a>
<!-- ## Routing -->
## Routing

<!-- To properly implement support for allowing users to reset their passwords, we will need to define several routes. First, we will need a pair of routes to handle allowing the user to request a password reset link via their email address. Second, we will need a pair of routes to handle actually resetting the password once the user visits the password reset link that is emailed to them and completes the password reset form. -->
ユーザーがパスワードをリセットできるようにするサポートを適切に実装するには、いくつかのルートを定義する必要があります。まず、ユーザーが電子メール アドレス経由でパスワードリセット リンクをリクエストできるようにするためのルートのペアが必要です。次に、ユーザーが電子メールで送信されたパスワードリセット リンクにアクセスし、パスワードリセット フォームに記入した後で、実際にパスワードをリセットする処理を行うための 1 組のルートが必要です。

<a name="requesting-the-password-reset-link"></a>
<!-- ### Requesting The Password Reset Link -->
### Requesting The Password Reset Link

<a name="the-password-reset-link-request-form"></a>
<!-- #### The Password Reset Link Request Form -->
#### The Password Reset Link Request Form

<!-- First, we will define the routes that are needed to request password reset links. To get started, we will define a route that returns a view with the password reset link request form: -->
まず、パスワードリセット リンクを要求するために必要なルートを定義します。まず、パスワードリセット リンク リクエスト フォームを含むビューを返すルートを定義します。

```
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');
```

<!-- The view that is returned by this route should have a form containing an `email` field, which will allow the user to request a password reset link for a given email address. -->
このルートによって返されるビューには、`email` フィールドを含むフォームが必要です。これにより、ユーザーは特定の電子メール アドレスのパスワードリセット リンクを要求できます。

<a name="password-reset-link-handling-the-form-submission"></a>
<!-- #### Handling The Form Submission -->
#### Handling The Form Submission

<!-- Next, we will define a route that handles the form submission request from the "forgot password" view. This route will be responsible for validating the email address and sending the password reset request to the corresponding user: -->
次に、「パスワードを忘れた場合」ビューからのフォーム送信リクエストを処理するルートを定義します。このルートは、電子メール アドレスを検証し、対応するユーザーにパスワードリセット リクエストを送信する役割を果たします。

```
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
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `email` attribute is validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to send a password reset link to the user. The password broker will take care of retrieving the user by the given field (in this case, the email address) and sending the user a password reset link via Laravel's built-in [notification system](/docs/8.x/notifications). -->
次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `email` 属性が検証されます。次に、Laravel の組み込み「パスワード ブローカー」を (`Password` ファサード経由で) 使用して、パスワードリセット リンクをユーザーに送信します。パスワードブローカーは、指定されたフィールド (この場合は電子メールアドレス) によるユーザーの取得と、Laravel の組み込み [notification system](/docs/8.x/notifications) を介したパスワードリセットリンクの送信を処理します。

<!-- The `sendResetLink` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/8.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `resources/lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. -->
`sendResetLink` メソッドは、「ステータス」スラッグを返します。このステータスは、リクエストのステータスに関するわかりやすいメッセージをユーザーに表示するために、Laravel の [localization](/docs/8.x/localization) ヘルパを使用して変換できます。パスワードリセット ステータスの翻訳は、アプリケーションの `resources/lang/{lang}/passwords.php` 言語ファイルによって決まります。ステータス スラッグの考えられる各値のエントリは、`passwords` 言語ファイル内にあります。

<!-- You may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `sendResetLink` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/8.x/authentication#adding-custom-user-providers). -->
`Password` ファサードの `sendResetLink` メソッドを呼び出すときに、Laravel がアプリケーションのデータベースからユーザー レコードを取得する方法をどのように認識するのか疑問に思われるかもしれません。 Laravel パスワードブローカーは、認証システムの「ユーザープロバイダ」を利用してデータベースレコードを取得します。パスワード ブローカーによって使用されるユーザー プロバイダは、`config/auth.php` 構成ファイルの `passwords` 構成配列内で構成されます。カスタム ユーザー プロバイダの作成の詳細については、[authentication documentation](/docs/8.x/authentication#adding-custom-user-providers) を参照してください。

> [!TIP]
> パスワードのリセットを手動で実装する場合は、ビューとルートの内容を自分で定義する必要があります。必要な認証および検証ロジックをすべて含むスキャフォールディングが必要な場合は、[Laravel application starter kits](/docs/8.x/starter-kits) を確認してください。

<a name="resetting-the-password"></a>
<!-- ### Resetting The Password -->
### Resetting The Password

<a name="the-password-reset-form"></a>
<!-- #### The Password Reset Form -->
#### The Password Reset Form

<!-- Next, we will define the routes necessary to actually reset the password once the user clicks on the password reset link that has been emailed to them and provides a new password. First, let's define the route that will display the reset password form that is displayed when the user clicks the reset password link. This route will receive a `token` parameter that we will use later to verify the password reset request: -->
次に、ユーザーが電子メールで送信されたパスワードリセット リンクをクリックして新しいパスワードを入力した後、実際にパスワードをリセットするために必要なルートを定義します。まず、ユーザーがパスワードのリセット リンクをクリックしたときに表示されるパスワードのリセット フォームを表示するルートを定義しましょう。このルートは、後でパスワードリセット要求を確認するために使用する `token` パラメーターを受け取ります。

```
Route::get('/reset-password/{token}', function ($token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');
```

<!-- The view that is returned by this route should display a form containing an `email` field, a `password` field, a `password_confirmation` field, and a hidden `token` field, which should contain the value of the secret `$token` received by our route. -->
このルートによって返されるビューには、`email` フィールド、`password` フィールド、`password_confirmation` フィールド、および非表示の `token` フィールドを含むフォームが表示されます。これらのフィールドには、ルートによって受信されたシークレット `$token` の値が含まれている必要があります。

<a name="password-reset-handling-the-form-submission"></a>
<!-- #### Handling The Form Submission -->
#### Handling The Form Submission

<!-- Of course, we need to define a route to actually handle the password reset form submission. This route will be responsible for validating the incoming request and updating the user's password in the database: -->
もちろん、パスワードリセット フォームの送信を実際に処理するルートを定義する必要があります。このルートは、受信リクエストの検証とデータベース内のユーザーのパスワードの更新を担当します。

```
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
        function ($user, $password) {
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
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `token`, `email`, and `password` attributes are validated. Next, we will use Laravel's built-in "password broker" (via the `Password` facade) to validate the password reset request credentials. -->
次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `token`、`email`、および `password` 属性が検証されます。次に、Laravel の組み込み「パスワード ブローカー」を (`Password` ファサード経由で) 使用して、パスワードリセット要求の資格情報を検証します。

<!-- If the token, email address, and password given to the password broker are valid, the closure passed to the `reset` method will be invoked. Within this closure, which receives the user instance and the plain-text password provided to the password reset form, we may update the user's password in the database. -->
パスワード ブローカーに指定されたトークン、電子メール アドレス、およびパスワードが有効な場合、`reset` メソッドに渡されたクロージャが呼び出されます。ユーザー インスタンスとパスワードリセット フォームに提供されたプレーンテキストのパスワードを受け取るこのクロージャー内で、データベース内のユーザーのパスワードを更新できます。

<!-- The `reset` method returns a "status" slug. This status may be translated using Laravel's [localization](/docs/8.x/localization) helpers in order to display a user-friendly message to the user regarding the status of their request. The translation of the password reset status is determined by your application's `resources/lang/{lang}/passwords.php` language file. An entry for each possible value of the status slug is located within the `passwords` language file. -->
`reset` メソッドは、「ステータス」スラッグを返します。このステータスは、リクエストのステータスに関するわかりやすいメッセージをユーザーに表示するために、Laravel の [localization](/docs/8.x/localization) ヘルパを使用して変換できます。パスワードリセット ステータスの翻訳は、アプリケーションの `resources/lang/{lang}/passwords.php` 言語ファイルによって決まります。ステータス スラッグの考えられる各値のエントリは、`passwords` 言語ファイル内にあります。

<!-- Before moving on, you may be wondering how Laravel knows how to retrieve the user record from your application's database when calling the `Password` facade's `reset` method. The Laravel password broker utilizes your authentication system's "user providers" to retrieve database records. The user provider used by the password broker is configured within the `passwords` configuration array of your `config/auth.php` configuration file. To learn more about writing custom user providers, consult the [authentication documentation](/docs/8.x/authentication#adding-custom-user-providers). -->
次に進む前に、`Password` ファサードの `reset` メソッドを呼び出すときに、Laravel がアプリケーションのデータベースからユーザー レコードを取得する方法をどのように認識するのか疑問に思うかもしれません。 Laravel パスワードブローカーは、認証システムの「ユーザープロバイダ」を利用してデータベースレコードを取得します。パスワード ブローカーによって使用されるユーザー プロバイダは、`config/auth.php` 構成ファイルの `passwords` 構成配列内で構成されます。カスタム ユーザー プロバイダの作成の詳細については、[authentication documentation](/docs/8.x/authentication#adding-custom-user-providers) を参照してください。

<a name="deleting-expired-tokens"></a>
<!-- ## Deleting Expired Tokens -->
## Deleting Expired Tokens

<!-- Password reset tokens that have expired will still be present within your database. However, you may easily delete these records using the `auth:clear-resets` Artisan command: -->
有効期限が切れたパスワードリセット トークンはデータベース内に残ります。ただし、`auth:clear-resets` Artisan コマンドを使用すると、これらのレコードを簡単に削除できます。

```
php artisan auth:clear-resets
```

<!-- If you would like to automate this process, consider adding the command to your application's [scheduler](/docs/8.x/scheduling): -->
このプロセスを自動化したい場合は、アプリケーションの [scheduler](/docs/8.x/scheduling) にコマンドを追加することを検討してください。

```
$schedule->command('auth:clear-resets')->everyFifteenMinutes();
```

<a name="password-customization"></a>
<!-- ## Customization -->
## Customization

<a name="reset-link-customization"></a>
<!-- #### Reset Link Customization -->
#### Reset Link Customization

<!-- You may customize the password reset link URL using the `createUrlUsing` method provided by the `ResetPassword` notification class. This method accepts a closure which receives the user instance that is receiving the notification as well as the password reset link token. Typically, you should call this method from your `App\Providers\AuthServiceProvider` service provider's `boot` method: -->
`ResetPassword` 通知クラスによって提供される `createUrlUsing` メソッドを使用して、パスワードリセット リンク URL をカスタマイズできます。このメソッドは、通知を受け取るユーザー インスタンスとパスワードリセット リンク トークンを受け取るクロージャを受け入れます。通常、このメソッドは `App\Providers\AuthServiceProvider` サービスプロバイダの `boot` メソッドから呼び出す必要があります。

```
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Register any authentication / authorization services.
 *
 * @return void
 */
public function boot()
{
    $this->registerPolicies();

    ResetPassword::createUrlUsing(function ($user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}
```

<a name="reset-email-customization"></a>
<!-- #### Reset Email Customization -->
#### Reset Email Customization

<!-- You may easily modify the notification class used to send the password reset link to the user. To get started, override the `sendPasswordResetNotification` method on your `App\Models\User` model. Within this method, you may send the notification using any [notification class](/docs/8.x/notifications) of your own creation. The password reset `$token` is the first argument received by the method. You may use this `$token` to build the password reset URL of your choice and send your notification to the user: -->
パスワードリセット リンクをユーザーに送信するために使用される通知クラスは簡単に変更できます。まず、`App\Models\User` モデルの `sendPasswordResetNotification` メソッドをオーバーライドします。このメソッド内で、独自に作成した [notification class](/docs/8.x/notifications) を使用して通知を送信できます。パスワードリセット `$token` は、メソッドによって受け取られる最初の引数です。この `$token` を使用して、選択したパスワードリセット URL を構築し、ユーザーに通知を送信できます。

```
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 * @return void
 */
public function sendPasswordResetNotification($token)
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}
```

