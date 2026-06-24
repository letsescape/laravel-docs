<!-- # Laravel Fortify -->
# Laravel Fortify

- [Introduction](#introduction)
    - [What is Fortify?](#what-is-fortify)
    - [When Should I Use Fortify?](#when-should-i-use-fortify)
- [Installation](#installation)
    - [Fortify Features](#fortify-features)
    - [Disabling Views](#disabling-views)
- [Authentication](#authentication)
    - [Customizing User Authentication](#customizing-user-authentication)
    - [Customizing the Authentication Pipeline](#customizing-the-authentication-pipeline)
    - [Customizing Redirects](#customizing-authentication-redirects)
- [Two-Factor Authentication](#two-factor-authentication)
    - [Enabling Two-Factor Authentication](#enabling-two-factor-authentication)
    - [Authenticating With Two-Factor Authentication](#authenticating-with-two-factor-authentication)
    - [Disabling Two-Factor Authentication](#disabling-two-factor-authentication)
- [Registration](#registration)
    - [Customizing Registration](#customizing-registration)
- [Password Reset](#password-reset)
    - [Requesting a Password Reset Link](#requesting-a-password-reset-link)
    - [Resetting the Password](#resetting-the-password)
    - [Customizing Password Resets](#customizing-password-resets)
- [Email Verification](#email-verification)
    - [Protecting Routes](#protecting-routes)
- [Password Confirmation](#password-confirmation)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Fortify](https://github.com/laravel/fortify) is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. After installing Fortify, you may run the `route:list` Artisan command to see the routes that Fortify has registered. -->
[Laravel Fortify](https://github.com/laravel/fortify) は、Laravel のフロントエンドに依存しない認証バックエンド実装です。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などを含む、Laravel のすべての認証機能を実装するために必要なルートとコントローラを登録します。 Fortify をインストールした後、`route:list` Artisan コマンドを実行して、Fortify が登録したルートを確認できます。

<!-- Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation. -->
Fortify は独自のユーザー インターフェイスを提供していないため、登録されているルートにリクエストを行う独自のユーザー インターフェイスと組み合わせることが意図されています。これらのルートにリクエストを行う方法については、このドキュメントの残りの部分で詳しく説明します。

> [!NOTE]
> Fortify は、Laravel の認証機能の実装をいち早く開始できるようにすることを目的としたパッケージであることを忘れないでください。 **これを使用する必要はありません。** [authentication](/docs/12.x/authentication)、[password reset](/docs/12.x/passwords)、および [email verification](/docs/12.x/verification) ドキュメントにあるドキュメントに従って、いつでも自由に Laravel の認証サービスと手動で対話できます。

<a name="what-is-fortify"></a>
<!-- ### What is Fortify? -->
### What is Fortify?

<!-- As mentioned previously, Laravel Fortify is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. -->
前述したように、Laravel Fortify は、Laravel のフロントエンドに依存しない認証バックエンド実装です。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などを含む、Laravel のすべての認証機能を実装するために必要なルートとコントローラを登録します。

<!-- **You are not required to use Fortify in order to use Laravel's authentication features.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), and [email verification](/docs/12.x/verification) documentation. -->
**Laravel の認証機能を使用するために Fortify を使用する必要はありません。** [authentication](/docs/12.x/authentication)、[password reset](/docs/12.x/passwords)、および [email verification](/docs/12.x/verification) ドキュメントにあるドキュメントに従って、いつでも自由に Laravel の認証サービスを手動で操作できます。

<!-- If you are new to Laravel, you may wish to explore [our application starter kits](/docs/12.x/starter-kits). Laravel's application starter kits use Fortify internally to provide authentication scaffolding for your application that includes a user interface built with [Tailwind CSS](https://tailwindcss.com). This allows you to study and get comfortable with Laravel's authentication features. -->
Laravel を初めて使用する場合は、[our application starter kits](/docs/12.x/starter-kits) を検討してみてください。 Laravel のアプリケーション スターター キットは、内部で Fortify を使用して、[Tailwind CSS](https://tailwindcss.com) で構築されたユーザー インターフェイスを含むアプリケーションの認証スキャフォールディングを提供します。これにより、Laravel の認証機能を学習し、慣れることができます。

<!-- Laravel Fortify essentially takes the routes and controllers of our application starter kits and offers them as a package that does not include a user interface. This allows you to still quickly scaffold the backend implementation of your application's authentication layer without being tied to any particular frontend opinions. -->
Laravel Fortify は基本的に、アプリケーション スターター キットのルートとコントローラを取得し、ユーザー インターフェイスを含まないパッケージとして提供します。これにより、特定のフロントエンドの意見に縛られることなく、アプリケーションの認証層のバックエンド実装を迅速に構築することができます。

<a name="when-should-i-use-fortify"></a>
<!-- ### When Should I Use Fortify? -->
### When Should I Use Fortify?

<!-- You may be wondering when it is appropriate to use Laravel Fortify. First, if you are using one of Laravel's [application starter kits](/docs/12.x/starter-kits), you do not need to install Laravel Fortify since all of Laravel's application starter kits use Fortify and already provide a full authentication implementation. -->
Laravel Fortify をいつ使用するのが適切なのか疑問に思われるかもしれません。まず、Laravel の [application starter kits](/docs/12.x/starter-kits) のいずれかを使用している場合、Laravel のアプリケーション スターター キットはすべて Fortify を使用しており、完全な認証実装がすでに提供されているため、Laravel Fortify をインストールする必要はありません。

<!-- If you are not using an application starter kit and your application needs authentication features, you have two options: manually implement your application's authentication features or use Laravel Fortify to provide the backend implementation of these features. -->
アプリケーションスターターキットを使用しておらず、アプリケーションに認証機能が必要な場合、アプリケーションの認証機能を手動で実装するか、Laravel Fortify を使用してこれらの機能のバックエンド実装を提供するかの 2 つのオプションがあります。

<!-- If you choose to install Fortify, your user interface will make requests to Fortify's authentication routes that are detailed in this documentation in order to authenticate and register users. -->
Fortify のインストールを選択した場合、ユーザー インターフェイスは、ユーザーを認証して登録するために、このドキュメントで詳しく説明されている Fortify の認証ルートにリクエストを作成します。

<!-- If you choose to manually interact with Laravel's authentication services instead of using Fortify, you may do so by following the documentation available in the [authentication](/docs/12.x/authentication), [password reset](/docs/12.x/passwords), and [email verification](/docs/12.x/verification) documentation. -->
Fortify を使用する代わりに Laravel の認証サービスと手動で対話することを選択した場合は、[authentication](/docs/12.x/authentication)、[password reset](/docs/12.x/passwords)、および [email verification](/docs/12.x/verification) ドキュメントで入手可能なドキュメントに従って行うことができます。

<a name="laravel-fortify-and-laravel-sanctum"></a>
<!-- #### Laravel Fortify and Laravel Sanctum -->
#### Laravel Fortify and Laravel Sanctum

<!-- Some developers become confused regarding the difference between [Laravel Sanctum](/docs/12.x/sanctum) and Laravel Fortify. Because the two packages solve two different but related problems, Laravel Fortify and Laravel Sanctum are not mutually exclusive or competing packages. -->
開発者の中には、[Laravel Sanctum](/docs/12.x/sanctum) と Laravel Fortify の違いについて混乱する人もいます。 2 つのパッケージは 2 つの異なるが関連する問題を解決するため、Laravel Fortify と Laravel Sanctum は相互に排他的または競合するパッケージではありません。

<!-- Laravel Sanctum is only concerned with managing API tokens and authenticating existing users using session cookies or tokens. Sanctum does not provide any routes that handle user registration, password reset, etc. -->
Laravel Sanctum は、API トークンの管理と、セッション Cookie またはトークンを使用した既存のユーザーの認証のみに関係します。 Sanctum は、ユーザー登録、パスワードのリセットなどを処理するルートを提供しません。

<!-- If you are attempting to manually build the authentication layer for an application that offers an API or serves as the backend for a single-page application, it is entirely possible that you will utilize both Laravel Fortify (for user registration, password reset, etc.) and Laravel Sanctum (API token management, session authentication). -->
API を提供するアプリケーション、またはシングルページ アプリケーションのバックエンドとして機能するアプリケーションの認証レイヤーを手動で構築しようとしている場合、Laravel Fortify (ユーザー登録、パスワードリセットなど) と Laravel Sanctum (API トークン管理、セッション認証) の両方を利用する可能性があります。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Fortify using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Fortify をインストールします。

```shell
composer require laravel/fortify
```

<!-- Next, publish Fortify's resources using the `fortify:install` Artisan command: -->
次に、`fortify:install` Artisan コマンドを使用して Fortify のリソースを公開します。

```shell
php artisan fortify:install
```

<!-- This command will publish Fortify's actions to your `app/Actions` directory, which will be created if it does not exist. In addition, the `FortifyServiceProvider`, configuration file, and all necessary database migrations will be published. -->
このコマンドは、Fortify のアクションを `app/Actions` ディレクトリに公開します。ディレクトリが存在しない場合は作成されます。さらに、`FortifyServiceProvider`、構成ファイル、および必要なすべてのデータベース移行が公開されます。

<!-- Next, you should migrate your database: -->
次に、データベースを移行する必要があります。

```shell
php artisan migrate
```

<a name="fortify-features"></a>
<!-- ### Fortify Features -->
### Fortify Features

<!-- The `fortify` configuration file contains a `features` configuration array. This array defines which backend routes / features Fortify will expose by default. We recommend that you only enable the following features, which are the basic authentication features provided by most Laravel applications: -->
`fortify` 構成ファイルには、`features` 構成配列が含まれています。この配列は、Fortify がデフォルトで公開するバックエンド ルート/機能を定義します。次の機能のみを有効にすることをお勧めします。これらの機能は、ほとんどの Laravel アプリケーションで提供される基本認証機能です。

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```

<a name="disabling-views"></a>
<!-- ### Disabling Views -->
### Disabling Views

<!-- By default, Fortify defines routes that are intended to return views, such as a login screen or registration screen. However, if you are building a JavaScript driven single-page application, you may not need these routes. For that reason, you may disable these routes entirely by setting the `views` configuration value within your application's `config/fortify.php` configuration file to `false`: -->
デフォルトでは、Fortify はログイン画面や登録画面などのビューを返すことを目的としたルートを定義します。ただし、JavaScript 駆動の単一ページ アプリケーションを構築している場合は、これらのルートは必要ない場合があります。そのため、アプリケーションの `config/fortify.php` 構成ファイル内の `views` 構成値を `false` に設定することで、これらのルートを完全に無効にすることができます。

```php
'views' => false,
```

<a name="disabling-views-and-password-reset"></a>
<!-- #### Disabling Views and Password Reset -->
#### Disabling Views and Password Reset

<!-- If you choose to disable Fortify's views and you will be implementing password reset features for your application, you should still define a route named `password.reset` that is responsible for displaying your application's "reset password" view. This is necessary because Laravel's `Illuminate\Auth\Notifications\ResetPassword` notification will generate the password reset URL via the `password.reset` named route. -->
Fortify のビューを無効にすることを選択し、アプリケーションにパスワードリセット機能を実装する場合でも、アプリケーションの「パスワードリセット」ビューの表示を担当する `password.reset` という名前のルートを定義する必要があります。これが必要なのは、Laravel の `Illuminate\Auth\Notifications\ResetPassword` 通知が `password.reset` 名前付きルート経由でパスワードリセット URL を生成するためです。

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- To get started, we need to instruct Fortify how to return our "login" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
まず、「ログイン」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[application starter kit](/docs/12.x/starter-kits) を使用する必要があります。

<!-- All of the authentication view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class. Fortify will take care of defining the `/login` route that returns this view: -->
認証ビューのレンダリング ロジックはすべて、`Laravel\Fortify\Fortify` クラス経由で利用可能な適切なメソッドを使用してカスタマイズできます。通常、このメソッドはアプリケーションの `App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。 Fortify は、このビューを返す `/login` ルートの定義を処理します。

```php
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
```

<!-- Your login template should include a form that makes a POST request to `/login`. The `/login` endpoint expects a string `email` / `username` and a `password`. The name of the email / username field should match the `username` value within the `config/fortify.php` configuration file. In addition, a boolean `remember` field may be provided to indicate that the user would like to use the "remember me" functionality provided by Laravel. -->
ログイン テンプレートには、`/login` への POST リクエストを行うフォームが含まれている必要があります。 `/login` エンドポイントは、文字列 `email` / `username` および `password` を予期します。電子メール/ユーザー名フィールドの名前は、`config/fortify.php` 構成ファイル内の `username` 値と一致する必要があります。さらに、Laravel が提供する「記憶する」機能をユーザーが使用したいことを示すために、ブール値の `remember` フィールドを提供することもできます。

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. -->
ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にリダイレクトします。ログイン要求が XHR 要求の場合、200 HTTP 応答が返されます。

<!-- If the request was not successful, the user will be redirected back to the login screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with the 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーはログイン画面にリダイレクトされ、共有 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-user-authentication"></a>
<!-- ### Customizing User Authentication -->
### Customizing User Authentication

<!-- Fortify will automatically retrieve and authenticate the user based on the provided credentials and the authentication guard that is configured for your application. However, you may sometimes wish to have full customization over how login credentials are authenticated and users are retrieved. Thankfully, Fortify allows you to easily accomplish this using the `Fortify::authenticateUsing` method. -->
Fortify は、提供された資格情報とアプリケーション用に構成された認証ガードに基づいてユーザーを自動的に取得し、認証します。ただし、ログイン資格情報の認証方法やユーザーの取得方法を完全にカスタマイズしたい場合もあります。ありがたいことに、Fortify では、`Fortify::authenticateUsing` メソッドを使用してこれを簡単に実現できます。

<!-- This method accepts a closure which receives the incoming HTTP request. The closure is responsible for validating the login credentials attached to the request and returning the associated user instance. If the credentials are invalid or no user can be found, `null` or `false` should be returned by the closure. Typically, this method should be called from the `boot` method of your `FortifyServiceProvider`: -->
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
<!-- #### Authentication Guard -->
#### Authentication Guard

<!-- You may customize the authentication guard used by Fortify within your application's `fortify` configuration file. However, you should ensure that the configured guard is an implementation of `Illuminate\Contracts\Auth\StatefulGuard`. If you are attempting to use Laravel Fortify to authenticate an SPA, you should use Laravel's default `web` guard in combination with [Laravel Sanctum](https://laravel.com/docs/sanctum). -->
アプリケーションの `fortify` 構成ファイル内で Fortify によって使用される認証ガードをカスタマイズできます。ただし、構成されたガードが `Illuminate\Contracts\Auth\StatefulGuard` の実装であることを確認する必要があります。 Laravel Fortify を使用して SPA を認証しようとしている場合は、Laravel のデフォルトの `web` ガードを [Laravel Sanctum](https://laravel.com/docs/sanctum) と組み合わせて使用​​する必要があります。

<a name="customizing-the-authentication-pipeline"></a>
<!-- ### Customizing the Authentication Pipeline -->
### Customizing the Authentication Pipeline

<!-- Laravel Fortify authenticates login requests through a pipeline of invokable classes. If you would like, you may define a custom pipeline of classes that login requests should be piped through. Each class should have an `__invoke` method which receives the incoming `Illuminate\Http\Request` instance and, like [middleware](/docs/12.x/middleware), a `$next` variable that is invoked in order to pass the request to the next class in the pipeline. -->
Laravel Fortify は、呼び出し可能なクラスのパイプラインを通じてログインリクエストを認証します。必要に応じて、ログイン要求がパイプされるクラスのカスタム パイプラインを定義できます。各クラスには、受信 `Illuminate\Http\Request` インスタンスを受け取る `__invoke` メソッドと、[middleware](/docs/12.x/middleware) と同様に、パイプライン内の次のクラスにリクエストを渡すために呼び出される `$next` 変数が必要です。

<!-- To define your custom pipeline, you may use the `Fortify::authenticateThrough` method. This method accepts a closure which should return the array of classes to pipe the login request through. Typically, this method should be called from the `boot` method of your `App\Providers\FortifyServiceProvider` class. -->
カスタム パイプラインを定義するには、`Fortify::authenticateThrough` メソッドを使用できます。このメソッドは、ログイン要求をパイプ処理するクラスの配列を返すクロージャを受け入れます。通常、このメソッドは、`App\Providers\FortifyServiceProvider` クラスの `boot` メソッドから呼び出す必要があります。

<!-- The example below contains the default pipeline definition that you may use as a starting point when making your own modifications: -->
以下の例には、独自の変更を行う際の開始点として使用できるデフォルトのパイプライン定義が含まれています。

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```

<!-- #### Authentication Throttling -->
#### Authentication Throttling

<!-- By default, Fortify will throttle authentication attempts using the `EnsureLoginIsNotThrottled` middleware. This middleware throttles attempts that are unique to a username and IP address combination. -->
デフォルトでは、Fortify は `EnsureLoginIsNotThrottled` ミドルウェアを使用して認証試行を抑制します。このミドルウェアは、ユーザー名と IP アドレスの組み合わせに固有の試行を抑制します。

<!-- Some applications may require a different approach to throttling authentication attempts, such as throttling by IP address alone. Therefore, Fortify allows you to specify your own [rate limiter](/docs/12.x/routing#rate-limiting) via the `fortify.limiters.login` configuration option. Of course, this configuration option is located in your application's `config/fortify.php` configuration file. -->
一部のアプリケーションでは、IP アドレスのみによるスロットルなど、認証試行をスロットルするための別のアプローチが必要な場合があります。したがって、Fortify では、`fortify.limiters.login` 構成オプションを介して独自の [rate limiter](/docs/12.x/routing#rate-limiting) を指定できます。もちろん、この構成オプションはアプリケーションの `config/fortify.php` 構成ファイルにあります。

> [!NOTE]
> スロットリング、[two-factor authentication](/docs/12.x/fortify#two-factor-authentication)、および外部 Web アプリケーション ファイアウォール (WAF) を組み合わせて利用すると、正規のアプリケーション ユーザーに最も堅牢な防御が提供されます。

<a name="customizing-authentication-redirects"></a>
<!-- ### Customizing Redirects -->
### Customizing Redirects

<!-- If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. After a user logs out of the application, the user will be redirected to the `/` URI. -->
ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にリダイレクトします。ログイン要求が XHR 要求の場合、200 HTTP 応答が返されます。ユーザーがアプリケーションからログアウトすると、ユーザーは `/` URI にリダイレクトされます。

<!-- If you need advanced customization of this behavior, you may bind implementations of the `LoginResponse` and `LogoutResponse` contracts into the Laravel [service container](/docs/12.x/container). Typically, this should be done within the `register` method of your application's `App\Providers\FortifyServiceProvider` class: -->
この動作の高度なカスタマイズが必要な場合は、`LoginResponse` および `LogoutResponse` コントラクトの実装を Laravel [service container](/docs/12.x/container) にバインドできます。通常、これはアプリケーションの `App\Providers\FortifyServiceProvider` クラスの `register` メソッド内で行う必要があります。

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
<!-- ## Two-Factor Authentication -->
## Two-Factor Authentication

<!-- When Fortify's two-factor authentication feature is enabled, the user is required to input a six digit numeric token during the authentication process. This token is generated using a time-based one-time password (TOTP) that can be retrieved from any TOTP compatible mobile authentication application such as Google Authenticator. -->
Fortify の 2 要素認証機能が有効になっている場合、ユーザーは認証プロセス中に 6 桁の数字トークンを入力する必要があります。このトークンは、Google Authenticator などの TOTP 互換モバイル認証アプリケーションから取得できる時間ベースのワンタイム パスワード (TOTP) を使用して生成されます。

<!-- Before getting started, you should first ensure that your application's `App\Models\User` model uses the `Laravel\Fortify\TwoFactorAuthenticatable` trait: -->
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

<!-- Next, you should build a screen within your application where users can manage their two-factor authentication settings. This screen should allow the user to enable and disable two-factor authentication, as well as regenerate their two-factor authentication recovery codes. -->
次に、ユーザーが 2 要素認証設定を管理できる画面をアプリケーション内に構築する必要があります。この画面では、ユーザーが 2 要素認証を有効または無効にしたり、2 要素認証リカバリ コードを再生成したりできるようになります。

> デフォルトでは、`fortify` 構成ファイルの `features` 配列は、変更前にパスワードの確認を要求するように Fortify の 2 要素認証設定を指示します。したがって、続行する前に、アプリケーションは Fortify の [password confirmation](#password-confirmation) 機能を実装する必要があります。

<a name="enabling-two-factor-authentication"></a>
<!-- ### Enabling Two-Factor Authentication -->
### Enabling Two-Factor Authentication

<!-- To begin enabling two-factor authentication, your application should make a POST request to the `/user/two-factor-authentication` endpoint defined by Fortify. If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-enabled`. You may detect this `status` session variable within your templates to display the appropriate success message. If the request was an XHR request, `200` HTTP response will be returned. -->
2 要素認証の有効化を開始するには、アプリケーションは Fortify によって定義された `/user/two-factor-authentication` エンドポイントに対して POST リクエストを行う必要があります。リクエストが成功すると、ユーザーは前の URL にリダイレクトされ、`status` セッション変数が `two-factor-authentication-enabled` に設定されます。テンプレート内でこの `status` セッション変数を検出すると、適切な成功メッセージが表示されます。リクエストが XHR リクエストの場合、`200` HTTP レスポンスが返されます。

<!-- After choosing to enable two-factor authentication, the user must still "confirm" their two-factor authentication configuration by providing a valid two-factor authentication code. So, your "success" message should instruct the user that two-factor authentication confirmation is still required: -->
2 要素認証の有効化を選択した後も、ユーザーは有効な 2 要素認証コードを入力して 2 要素認証構成を「確認」する必要があります。したがって、「成功」メッセージは、2 要素認証の確認が引き続き必要であることをユーザーに通知する必要があります。

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```

<!-- Next, you should display the two-factor authentication QR code for the user to scan into their authenticator application. If you are using Blade to render your application's frontend, you may retrieve the QR code SVG using the `twoFactorQrCodeSvg` method available on the user instance: -->
次に、ユーザーが認証アプリケーションにスキャンするための 2 要素認証 QR コードを表示する必要があります。 Blade を使用してアプリケーションのフロントエンドをレンダリングしている場合は、ユーザー インスタンスで利用可能な `twoFactorQrCodeSvg` メソッドを使用して QR コード SVG を取得できます。

```php
$request->user()->twoFactorQrCodeSvg();
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-qr-code` endpoint to retrieve the user's two-factor authentication QR code. This endpoint will return a JSON object containing an `svg` key. -->
JavaScript を利用したフロントエンドを構築している場合は、`/user/two-factor-qr-code` エンドポイントに XHR GET リクエストを送信して、ユーザーの 2 要素認証 QR コードを取得できます。このエンドポイントは、`svg` キーを含む JSON オブジェクトを返します。

<a name="confirming-two-factor-authentication"></a>
<!-- #### Confirming Two-Factor Authentication -->
#### Confirming Two-Factor Authentication

<!-- In addition to displaying the user's two-factor authentication QR code, you should provide a text input where the user can supply a valid authentication code to "confirm" their two-factor authentication configuration. This code should be provided to the Laravel application via a POST request to the `/user/confirmed-two-factor-authentication` endpoint defined by Fortify. -->
ユーザーの 2 要素認証 QR コードを表示するだけでなく、ユーザーが 2 要素認証構成を「確認」するために有効な認証コードを入力できるテキスト入力を提供する必要があります。このコードは、Fortify によって定義された `/user/confirmed-two-factor-authentication` エンドポイントへの POST リクエストを介して Laravel アプリケーションに提供される必要があります。

<!-- If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-confirmed`: -->
リクエストが成功すると、ユーザーは前の URL にリダイレクトされ、`status` セッション変数が `two-factor-authentication-confirmed` に設定されます。

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```

<!-- If the request to the two-factor authentication confirmation endpoint was made via an XHR request, a `200` HTTP response will be returned. -->
2 要素認証確認エンドポイントへのリクエストが XHR リクエスト経由で行われた場合、`200` HTTP レスポンスが返されます。

<a name="displaying-the-recovery-codes"></a>
<!-- #### Displaying the Recovery Codes -->
#### Displaying the Recovery Codes

<!-- You should also display the user's two-factor recovery codes. These recovery codes allow the user to authenticate if they lose access to their mobile device. If you are using Blade to render your application's frontend, you may access the recovery codes via the authenticated user instance: -->
ユーザーの 2 要素リカバリー コードも表示する必要があります。これらのリカバリ コードを使用すると、モバイル デバイスにアクセスできなくなった場合にユーザーを認証できます。 Blade を使用してアプリケーションのフロントエンドをレンダリングしている場合は、認証されたユーザー インスタンスを介してリカバリ コードにアクセスできます。

```php
(array) $request->user()->recoveryCodes()
```

<!-- If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-recovery-codes` endpoint. This endpoint will return a JSON array containing the user's recovery codes. -->
JavaScript を利用したフロントエンドを構築している場合は、`/user/two-factor-recovery-codes` エンドポイントに対して XHR GET リクエストを行うことができます。このエンドポイントは、ユーザーのリカバリ コードを含む JSON 配列を返します。

<!-- To regenerate the user's recovery codes, your application should make a POST request to the `/user/two-factor-recovery-codes` endpoint. -->
ユーザーのリカバリ コードを再生成するには、アプリケーションは `/user/two-factor-recovery-codes` エンドポイントに対して POST リクエストを行う必要があります。

<a name="authenticating-with-two-factor-authentication"></a>
<!-- ### Authenticating With Two-Factor Authentication -->
### Authenticating With Two-Factor Authentication

<!-- During the authentication process, Fortify will automatically redirect the user to your application's two-factor authentication challenge screen. However, if your application is making an XHR login request, the JSON response returned after a successful authentication attempt will contain a JSON object that has a `two_factor` boolean property. You should inspect this value to know whether you should redirect to your application's two-factor authentication challenge screen. -->
認証プロセス中に、Fortify はユーザーをアプリケーションの 2 要素認証チャレンジ画面に自動的にリダイレクトします。ただし、アプリケーションが XHR ログイン要求を行っている場合、認証試行が成功した後に返される JSON 応答には、`two_factor` ブール型プロパティを持つ JSON オブジェクトが含まれます。この値を調べて、アプリケーションの 2 要素認証チャレンジ画面にリダイレクトする必要があるかどうかを確認する必要があります。

<!-- To begin implementing two-factor authentication functionality, we need to instruct Fortify how to return our two-factor authentication challenge view. All of Fortify's authentication view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the `/two-factor-challenge` route that returns this view. Your `two-factor-challenge` template should include a form that makes a POST request to the `/two-factor-challenge` endpoint. The `/two-factor-challenge` action expects a `code` field that contains a valid TOTP token or a `recovery_code` field that contains one of the user's recovery codes. -->
Fortify は、このビューを返す `/two-factor-challenge` ルートの定義を処理します。 `two-factor-challenge` テンプレートには、`/two-factor-challenge` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。 `/two-factor-challenge` アクションは、有効な TOTP トークンを含む `code` フィールド、またはユーザーのリカバリ コードの 1 つを含む `recovery_code` フィールドを予期します。

<!-- If the login attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 204 HTTP response will be returned. -->
ログイン試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にユーザーをリダイレクトします。ログイン要求が XHR 要求の場合、204 HTTP 応答が返されます。

<!-- If the request was not successful, the user will be redirected back to the two-factor challenge screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーは 2 要素チャレンジ画面にリダイレクトされ、共有 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="disabling-two-factor-authentication"></a>
<!-- ### Disabling Two-Factor Authentication -->
### Disabling Two-Factor Authentication

<!-- To disable two-factor authentication, your application should make a DELETE request to the `/user/two-factor-authentication` endpoint. Remember, Fortify's two-factor authentication endpoints require [password confirmation](#password-confirmation) prior to being called. -->
2 要素認証を無効にするには、アプリケーションは `/user/two-factor-authentication` エンドポイントに対して DELETE リクエストを行う必要があります。 Fortify の 2 要素認証エンドポイントでは、呼び出される前に [password confirmation](#password-confirmation) が必要であることに注意してください。

<a name="registration"></a>
<!-- ## Registration -->
## Registration

<!-- To begin implementing our application's registration functionality, we need to instruct Fortify how to return our "register" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
アプリケーションの登録機能の実装を開始するには、「登録」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[application starter kit](/docs/12.x/starter-kits) を使用する必要があります。

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the `/register` route that returns this view. Your `register` template should include a form that makes a POST request to the `/register` endpoint defined by Fortify. -->
Fortify は、このビューを返す `/register` ルートの定義を処理します。 `register` テンプレートには、Fortify によって定義された `/register` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。

<!-- The `/register` endpoint expects a string `name`, string email address / username, `password`, and `password_confirmation` fields. The name of the email / username field should match the `username` configuration value defined within your application's `fortify` configuration file. -->
`/register` エンドポイントは、文字列 `name`、文字列の電子メール アドレス/ユーザー名、`password`、および `password_confirmation` フィールドを予期します。電子メール/ユーザー名フィールドの名前は、アプリケーションの `fortify` 構成ファイル内で定義された `username` 構成値と一致する必要があります。

<!-- If the registration attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the request was an XHR request, a 201 HTTP response will be returned. -->
登録の試行が成功すると、Fortify はアプリケーションの `fortify` 構成ファイル内の `home` 構成オプションを介して構成された URI にユーザーをリダイレクトします。リクエストが XHR リクエストの場合、201 HTTP レスポンスが返されます。

<!-- If the request was not successful, the user will be redirected back to the registration screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーは登録画面にリダイレクトされ、共有 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-registration"></a>
<!-- ### Customizing Registration -->
### Customizing Registration

<!-- The user validation and creation process may be customized by modifying the `App\Actions\Fortify\CreateNewUser` action that was generated when you installed Laravel Fortify. -->
ユーザー検証および作成プロセスは、Laravel Fortify のインストール時に生成された `App\Actions\Fortify\CreateNewUser` アクションを変更することでカスタマイズできます。

<a name="password-reset"></a>
<!-- ## Password Reset -->
## Password Reset

<a name="requesting-a-password-reset-link"></a>
<!-- ### Requesting a Password Reset Link -->
### Requesting a Password Reset Link

<!-- To begin implementing our application's password reset functionality, we need to instruct Fortify how to return our "forgot password" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
アプリケーションのパスワードリセット機能の実装を開始するには、「パスワードを忘れた場合」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[application starter kit](/docs/12.x/starter-kits) を使用する必要があります。

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the `/forgot-password` endpoint that returns this view. Your `forgot-password` template should include a form that makes a POST request to the `/forgot-password` endpoint. -->
Fortify は、このビューを返す `/forgot-password` エンドポイントの定義を処理します。 `forgot-password` テンプレートには、`/forgot-password` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。

<!-- The `/forgot-password` endpoint expects a string `email` field. The name of this field / database column should match the `email` configuration value within your application's `fortify` configuration file. -->
`/forgot-password` エンドポイントは文字列 `email` フィールドを予期します。このフィールド/データベース列の名前は、アプリケーションの `fortify` 構成ファイル内の `email` 構成値と一致する必要があります。

<a name="handling-the-password-reset-link-request-response"></a>
<!-- #### Handling the Password Reset Link Request Response -->
#### Handling the Password Reset Link Request Response

<!-- If the password reset link request was successful, Fortify will redirect the user back to the `/forgot-password` endpoint and send an email to the user with a secure link they can use to reset their password. If the request was an XHR request, a 200 HTTP response will be returned. -->
パスワードリセット リンク リクエストが成功した場合、Fortify はユーザーを `/forgot-password` エンドポイントにリダイレクトし、パスワードのリセットに使用できる安全なリンクを含む電子メールをユーザーに送信します。リクエストが XHR リクエストの場合、200 HTTP レスポンスが返されます。

<!-- After being redirected back to the `/forgot-password` endpoint after a successful request, the `status` session variable may be used to display the status of the password reset link request attempt. -->
リクエストが成功した後に `/forgot-password` エンドポイントにリダイレクトされた後、`status` セッション変数を使用して、パスワードリセット リンク リクエスト試行のステータスを表示できます。

<!-- The value of the `$status` session variable will match one of the translation strings defined within your application's `passwords` [language file](/docs/12.x/localization). If you would like to customize this value and have not published Laravel's language files, you may do so via the `lang:publish` Artisan command: -->
`$status` セッション変数の値は、アプリケーションの `passwords` [language file](/docs/12.x/localization) 内で定義された変換文字列の 1 つと一致します。この値をカスタマイズしたいが、Laravel の言語ファイルを公開していない場合は、`lang:publish` Artisan コマンドを使用してカスタマイズできます。

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was not successful, the user will be redirected back to the request password reset link screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーはパスワードリセット リンクのリクエスト画面にリダイレクトされ、共有 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors) 経由で検証エラーを確認できるようになります。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="resetting-the-password"></a>
<!-- ### Resetting the Password -->
### Resetting the Password

<!-- To finish implementing our application's password reset functionality, we need to instruct Fortify how to return our "reset password" view. -->
アプリケーションのパスワードリセット機能の実装を完了するには、Fortify に「パスワードのリセット」ビューを返す方法を指示する必要があります。

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the route to display this view. Your `reset-password` template should include a form that makes a POST request to `/reset-password`. -->
Fortify は、このビューを表示するルートの定義を処理します。 `reset-password` テンプレートには、`/reset-password` への POST リクエストを行うフォームが含まれている必要があります。

<!-- The `/reset-password` endpoint expects a string `email` field, a `password` field, a `password_confirmation` field, and a hidden field named `token` that contains the value of `request()->route('token')`. The name of the "email" field / database column should match the `email` configuration value defined within your application's `fortify` configuration file. -->
`/reset-password` エンドポイントは、文字列 `email` フィールド、`password` フィールド、`password_confirmation` フィールド、および `request()->route('token')` の値を含む `token` という名前の隠しフィールドを期待します。 「電子メール」フィールド/データベース列の名前は、アプリケーションの `fortify` 構成ファイル内で定義された `email` 構成値と一致する必要があります。

<a name="handling-the-password-reset-response"></a>
<!-- #### Handling the Password Reset Response -->
#### Handling the Password Reset Response

<!-- If the password reset request was successful, Fortify will redirect back to the `/login` route so that the user can log in with their new password. In addition, a `status` session variable will be set so that you may display the successful status of the reset on your login screen: -->
パスワードのリセット要求が成功した場合、Fortify は `/login` ルートにリダイレクトして戻り、ユーザーが新しいパスワードでログインできるようにします。さらに、ログイン画面にリセットの成功ステータスを表示できるように、`status` セッション変数が設定されます。

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```

<!-- If the request was an XHR request, a 200 HTTP response will be returned. -->
リクエストが XHR リクエストの場合、200 HTTP レスポンスが返されます。

<!-- If the request was not successful, the user will be redirected back to the reset password screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーはパスワードのリセット画面にリダイレクトされ、共有 `$errors` [Blade template variable](/docs/12.x/validation#quick-displaying-the-validation-errors) を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

<a name="customizing-password-resets"></a>
<!-- ### Customizing Password Resets -->
### Customizing Password Resets

<!-- The password reset process may be customized by modifying the `App\Actions\ResetUserPassword` action that was generated when you installed Laravel Fortify. -->
パスワードのリセットプロセスは、Laravel Fortify のインストール時に生成された `App\Actions\ResetUserPassword` アクションを変更することでカスタマイズできます。

<a name="email-verification"></a>
<!-- ## Email Verification -->
## Email Verification

<!-- After registration, you may wish for users to verify their email address before they continue accessing your application. To get started, ensure the `emailVerification` feature is enabled in your `fortify` configuration file's `features` array. Next, you should ensure that your `App\Models\User` class implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface. -->
登録後、ユーザーがアプリケーションへのアクセスを続ける前に、自分の電子メール アドレスを確認するように求めることができます。開始するには、`emailVerification` 機能が `fortify` 構成ファイルの `features` 配列で有効になっていることを確認してください。次に、`App\Models\User` クラスが `Illuminate\Contracts\Auth\MustVerifyEmail` インターフェイスを実装していることを確認する必要があります。

<!-- Once these two setup steps have been completed, newly registered users will receive an email prompting them to verify their email address ownership. However, we need to inform Fortify how to display the email verification screen which informs the user that they need to go click the verification link in the email. -->
これら 2 つのセットアップ手順が完了すると、新規登録ユーザーは、電子メール アドレスの所有権を確認するよう求める電子メールを受け取ります。ただし、メール内の確認リンクをクリックする必要があることをユーザーに通知するメール確認画面を表示する方法を Fortify に通知する必要があります。

<!-- All of Fortify's view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the route that displays this view when a user is redirected to the `/email/verify` endpoint by Laravel's built-in `verified` middleware. -->
Fortify は、Laravel の組み込み `verified` ミドルウェアによってユーザーが `/email/verify` エンドポイントにリダイレクトされるときに、このビューを表示するルートの定義を処理します。

<!-- Your `verify-email` template should include an informational message instructing the user to click the email verification link that was sent to their email address. -->
`verify-email` テンプレートには、電子メール アドレスに送信された電子メール検証リンクをクリックするようにユーザーに指示する情報メッセージが含まれている必要があります。

<a name="resending-email-verification-links"></a>
<!-- #### Resending Email Verification Links -->
#### Resending Email Verification Links

<!-- If you wish, you may add a button to your application's `verify-email` template that triggers a POST request to the `/email/verification-notification` endpoint. When this endpoint receives a request, a new verification email link will be emailed to the user, allowing the user to get a new verification link if the previous one was accidentally deleted or lost. -->
必要に応じて、`/email/verification-notification` エンドポイントへの POST リクエストをトリガーするボタンをアプリケーションの `verify-email` テンプレートに追加できます。このエンドポイントがリクエストを受信すると、新しい検証電子メール リンクがユーザーに電子メールで送信されます。これにより、以前の検証リンクが誤って削除または紛失した場合でも、ユーザーは新しい検証リンクを取得できるようになります。

<!-- If the request to resend the verification link email was successful, Fortify will redirect the user back to the `/email/verify` endpoint with a `status` session variable, allowing you to display an informational message to the user informing them the operation was successful. If the request was an XHR request, a 202 HTTP response will be returned: -->
検証リンク電子メールの再送信リクエストが成功した場合、Fortify は `status` セッション変数を使用してユーザーを `/email/verify` エンドポイントにリダイレクトし、操作が成功したことを知らせる情報メッセージをユーザーに表示できるようにします。リクエストが XHR リクエストの場合、202 HTTP レスポンスが返されます。

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- To specify that a route or group of routes requires that the user has verified their email address, you should attach Laravel's built-in `verified` middleware to the route. The `verified` middleware alias is automatically registered by Laravel and serves as an alias for the `Illuminate\Auth\Middleware\EnsureEmailIsVerified` middleware: -->
ルートまたはルートのグループでユーザーが電子メール アドレスを検証していることを要求するように指定するには、Laravel の組み込み `verified` ミドルウェアをルートにアタッチする必要があります。 `verified` ミドルウェアのエイリアスは、Laravel によって自動的に登録され、`Illuminate\Auth\Middleware\EnsureEmailIsVerified` ミドルウェアのエイリアスとして機能します。

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed. Typically, these routes are protected by Laravel's built-in `password.confirm` middleware. -->
アプリケーションの構築中に、アクションを実行する前にユーザーにパスワードの確認を要求するアクションが発生する場合があります。通常、これらのルートは、Laravel の組み込み `password.confirm` ミドルウェアによって保護されます。

<!-- To begin implementing password confirmation functionality, we need to instruct Fortify how to return our application's "password confirmation" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/12.x/starter-kits). -->
パスワード確認機能の実装を開始するには、アプリケーションの「パスワード確認」ビューを返す方法を Fortify に指示する必要があります。 Fortify はヘッドレス認証ライブラリであることを思い出してください。すでに完成している Laravel の認証機能のフロントエンド実装が必要な場合は、[application starter kit](/docs/12.x/starter-kits) を使用する必要があります。

<!-- All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class: -->
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

<!-- Fortify will take care of defining the `/user/confirm-password` endpoint that returns this view. Your `confirm-password` template should include a form that makes a POST request to the `/user/confirm-password` endpoint. The `/user/confirm-password` endpoint expects a `password` field that contains the user's current password. -->
Fortify は、このビューを返す `/user/confirm-password` エンドポイントの定義を処理します。 `confirm-password` テンプレートには、`/user/confirm-password` エンドポイントに POST リクエストを行うフォームが含まれている必要があります。 `/user/confirm-password` エンドポイントは、ユーザーの現在のパスワードを含む `password` フィールドを予期します。

<!-- If the password matches the user's current password, Fortify will redirect the user to the route they were attempting to access. If the request was an XHR request, a 201 HTTP response will be returned. -->
パスワードがユーザーの現在のパスワードと一致する場合、Fortify はユーザーをアクセスしようとしていたルートにリダイレクトします。リクエストが XHR リクエストの場合、201 HTTP レスポンスが返されます。

<!-- If the request was not successful, the user will be redirected back to the confirm password screen and the validation errors will be available to you via the shared `$errors` Blade template variable. Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response. -->
リクエストが成功しなかった場合、ユーザーはパスワード確認画面にリダイレクトされ、共有の `$errors` Blade テンプレート変数を介して検証エラーが表示されます。または、XHR リクエストの場合、検証エラーは 422 HTTP レスポンスで返されます。

