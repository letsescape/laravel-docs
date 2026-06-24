<!-- # Authentication -->
# Authentication

- [Introduction](#introduction)
    - [Starter Kits](#starter-kits)
    - [Database Considerations](#introduction-database-considerations)
    - [Ecosystem Overview](#ecosystem-overview)
- [Authentication Quickstart](#authentication-quickstart)
    - [Install a Starter Kit](#install-a-starter-kit)
    - [Retrieving the Authenticated User](#retrieving-the-authenticated-user)
    - [Protecting Routes](#protecting-routes)
    - [Login Throttling](#login-throttling)
- [Manually Authenticating Users](#authenticating-users)
    - [Remembering Users](#remembering-users)
    - [Other Authentication Methods](#other-authentication-methods)
- [HTTP Basic Authentication](#http-basic-authentication)
    - [Stateless HTTP Basic Authentication](#stateless-http-basic-authentication)
- [Logging Out](#logging-out)
    - [Invalidating Sessions on Other Devices](#invalidating-sessions-on-other-devices)
- [Password Confirmation](#password-confirmation)
    - [Configuration](#password-confirmation-configuration)
    - [Routing](#password-confirmation-routing)
    - [Protecting Routes](#password-confirmation-protecting-routes)
- [Adding Custom Guards](#adding-custom-guards)
    - [Closure Request Guards](#closure-request-guards)
- [Adding Custom User Providers](#adding-custom-user-providers)
    - [The User Provider Contract](#the-user-provider-contract)
    - [The Authenticatable Contract](#the-authenticatable-contract)
- [Automatic Password Rehashing](#automatic-password-rehashing)
<!-- - [Social Authentication](/docs/11.x/socialite) -->
- [Social Authentication](/docs/11.x/socialite)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily. -->
多くの Web アプリケーションは、ユーザーがアプリケーションで認証して「ログイン」する方法を提供します。この機能を Web アプリケーションに実装することは、複雑で潜在的に危険な作業となる可能性があります。このため、Laravel は、認証を迅速、安全、簡単に実装するために必要なツールを提供するよう努めています。

<!-- At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies. -->
Laravel の認証機能の中核は、「ガード」と「プロバイダ」で構成されています。ガードは、各リクエストに対してユーザーが認証される方法を定義します。たとえば、Laravel には、セッションストレージと Cookie を使用して状態を維持する `session` ガードが付属しています。

<!-- Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/11.x/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application. -->
プロバイダは、永続ストレージからユーザーを取得する方法を定義します。 Laravel には、[Eloquent](/docs/11.x/eloquent) とデータベース クエリビルダを使用したユーザーの取得のサポートが付属しています。ただし、アプリケーションの必要に応じて追加のプロバイダを自由に定義できます。

<!-- Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services. -->
アプリケーションの認証構成ファイルは、`config/auth.php` にあります。このファイルには、Laravel の認証サービスの動作を調整するための、十分に文書化されたオプションがいくつか含まれています。

> [!NOTE]
> ガードとプロバイダを「ロール」と「権限」と混同しないでください。権限によるユーザーアクションの承認の詳細については、[authorization](/docs/11.x/authorization) ドキュメントを参照してください。

<a name="starter-kits"></a>
<!-- ### Starter Kits -->
### Starter Kits

<!-- Want to get started fast? Install a [Laravel application starter kit](/docs/11.x/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system! -->
すぐに始めたいですか?新しい Laravel アプリケーションに [Laravel application starter kit](/docs/11.x/starter-kits) をインストールします。データベースを移行した後、ブラウザーで `/register` またはアプリケーションに割り当てられているその他の URL に移動します。スターター キットは、認証システム全体の足場を整えます。

<!-- **Even if you choose not to use a starter kit in your final Laravel application, installing the [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) starter kit can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since Laravel Breeze creates authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented. -->
**最終的な Laravel アプリケーションでスターター キットを使用しないことを選択した場合でも、[Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) スターター キットのインストールは、Laravel のすべての認証機能を実際の Laravel プロジェクトに実装する方法を学ぶ素晴らしい機会になります。** Laravel Breeze は認証コントローラ、ルート、ビューを作成するため、これらのファイル内のコードを調べて、Laravel の認証機能がどのように実装されるかを学ぶことができます。

<a name="introduction-database-considerations"></a>
<!-- ### Database Considerations -->
### Database Considerations

<!-- By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/11.x/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver. -->
デフォルトでは、Laravel には `app/Models` ディレクトリに `App\Models\User` [Eloquent model](/docs/11.x/eloquent) が含まれています。このモデルは、デフォルトの Eloquent 認証ドライバとともに使用できます。

<!-- If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. If your application is using MongoDB, check out MongoDB's official [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/) . -->
アプリケーションが Eloquent を使用していない場合は、Laravel クエリビルダを使用する `database` 認証プロバイダを使用できます。アプリケーションが MongoDB を使用している場合は、MongoDB の公式 [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/) を確認してください。

<!-- When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length. -->
`App\Models\User` モデルのデータベース スキーマを構築するときは、パスワード列の長さが少なくとも 60 文字であることを確認してください。もちろん、新しい Laravel アプリケーションに含まれる `users` テーブルの移行では、この長さを超える列がすでに作成されています。

<!-- Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column. -->
また、`users` (または同等の) テーブルに、NULL 許容の 100 文字の文字列 `remember_token` 列が含まれていることを確認する必要があります。この列は、アプリケーションにログインするときに「記憶する」オプションを選択したユーザーのトークンを保存するために使用されます。繰り返しますが、新しい Laravel アプリケーションに含まれるデフォルトの `users` テーブル移行には、この列がすでに含まれています。

<a name="ecosystem-overview"></a>
<!-- ### Ecosystem Overview -->
### Ecosystem Overview

<!-- Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose. -->
Laravel は認証に関連するパッケージをいくつか提供しています。続行する前に、Laravel の一般的な認証エコシステムを確認し、各パッケージの意図された目的について説明します。

<!-- First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/11.x/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated". -->
まず、認証がどのように機能するかを考えてみましょう。 Web ブラウザを使用する場合、ユーザーはログイン フォームを介してユーザー名とパスワードを入力します。これらの資格情報が正しい場合、アプリケーションは認証されたユーザーに関する情報をユーザーの [session](/docs/11.x/session) に保存します。ブラウザに発行される Cookie にはセッション ID が含まれているため、アプリケーションへの後続のリクエストでユーザーを正しいセッションに関連付けることができます。セッション Cookie を受信すると、アプリケーションはセッション ID に基づいてセッション データを取得し、認証情報がセッションに保存されていることに注意して、ユーザーを「認証済み」と見なします。

<!-- When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token. -->
リモート サービスが API にアクセスするために認証が必要な場合、Web ブラウザがないため、通常は認証に Cookie は使用されません。代わりに、リモート サービスはリクエストごとに API トークンを API に送信します。アプリケーションは、受信したトークンを有効な API トークンのテーブルと照合して検証し、その API トークンに関連付けられたユーザーによって実行されたリクエストを「認証」します。

<a name="laravels-built-in-browser-authentication-services"></a>
<!-- #### Laravel's Built-in Browser Authentication Services -->
#### Laravel's Built-in Browser Authentication Services

<!-- Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation. -->
Laravel には、組み込みの認証サービスとセッション サービスが含まれており、通常は `Auth` および `Session` ファサードを介してアクセスされます。これらの機能は、Web ブラウザから開始されたリクエストに対して Cookie ベースの認証を提供します。これらは、ユーザーの資格情報を確認し、ユーザーを認証できるメソッドを提供します。さらに、これらのサービスは、ユーザーのセッションに適切な認証データを自動的に保存し、ユーザーのセッション Cookie を発行します。これらのサービスの使用方法については、このドキュメントに記載されています。

<!-- **Application Starter Kits** -->
**アプリケーション スターター キット**

<!-- As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free packages](/docs/11.x/starter-kits) that provide robust, modern scaffolding of the entire authentication layer. These packages are [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze), [Laravel Jetstream](/docs/11.x/starter-kits#laravel-jetstream), and [Laravel Fortify](/docs/11.x/fortify). -->
このドキュメントで説明したように、これらの認証サービスと手動で対話して、アプリケーション独自の認証層を構築できます。ただし、より迅速に開始できるように、認証レイヤー全体の堅牢で最新の足場を提供する [free packages](/docs/11.x/starter-kits) をリリースしました。これらのパッケージは、[Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze)、[Laravel Jetstream](/docs/11.x/starter-kits#laravel-jetstream)、および [Laravel Fortify](/docs/11.x/fortify) です。

<!-- _Laravel Breeze_ is a simple, minimal implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is comprised of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). To get started, check out the documentation on Laravel's [application starter kits](/docs/11.x/starter-kits). -->
_Laravel Breeze_ は、ログイン、登録、パスワードのリセット、電子メール検証、パスワード確認を含む、Laravel のすべての認証機能のシンプルかつ最小限の実装です。 Laravel Breeze のビューレイヤーは、[Blade templates](/docs/11.x/blade) でスタイル設定されたシンプルな [Tailwind CSS](https://tailwindcss.com) で構成されています。まず、Laravel の [application starter kits](/docs/11.x/starter-kits) のドキュメントを確認してください。

<!-- _Laravel Fortify_ is a headless authentication backend for Laravel that implements many of the features found in this documentation, including cookie-based authentication as well as other features such as two-factor authentication and email verification. Fortify provides the authentication backend for Laravel Jetstream or may be used independently in combination with [Laravel Sanctum](/docs/11.x/sanctum) to provide authentication for an SPA that needs to authenticate with Laravel. -->
_Laravel Fortify_ は、Cookie ベースの認証や 2 要素認証や電子メール検証などの他の機能を含む、このドキュメントで説明されている機能の多くを実装する Laravel のヘッドレス認証バックエンドです。 Fortify は、Laravel Jetstream の認証バックエンドを提供するか、Laravel で認証する必要がある SPA に認証を提供するために、[Laravel Sanctum](/docs/11.x/sanctum) と組み合わせて単独で使用することもできます。

<!-- _[Laravel Jetstream](https://jetstream.laravel.com)_ is a robust application starter kit that consumes and exposes Laravel Fortify's authentication services with a beautiful, modern UI powered by [Tailwind CSS](https://tailwindcss.com), [Livewire](https://livewire.laravel.com), and / or [Inertia](https://inertiajs.com). Laravel Jetstream includes optional support for two-factor authentication, team support, browser session management, profile management, and built-in integration with [Laravel Sanctum](/docs/11.x/sanctum) to offer API token authentication. Laravel's API authentication offerings are discussed below. -->
_[Laravel Jetstream](https://jetstream.laravel.com)_ は、[Tailwind CSS](https://tailwindcss.com)、[Livewire](https://livewire.laravel.com)、および/または [Inertia](https://inertiajs.com) を利用した美しくモダンな UI を備えた Laravel Fortify の認証サービスを利用および公開する堅牢なアプリケーション スターター キットです。 Laravel Jetstream には、2 要素認証、チーム サポート、ブラウザ セッション管理、プロファイル管理、および API トークン認証を提供する [Laravel Sanctum](/docs/11.x/sanctum) との組み込み統合のオプション サポートが含まれています。 Laravel の API 認証機能については以下で説明します。

<a name="laravels-api-authentication-services"></a>
<!-- #### Laravel's API Authentication Services -->
#### Laravel's API Authentication Services

<!-- Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/11.x/passport) and [Sanctum](/docs/11.x/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages. -->
Laravel は、API トークンの管理と API トークンを使用して行われたリクエストの認証を支援する 2 つのオプション パッケージ ([Passport](/docs/11.x/passport) と [Sanctum](/docs/11.x/sanctum)) を提供します。これらのライブラリとLaravelの組み込みCookieベースの認証ライブラリは相互に排他的ではないことに注意してください。これらのライブラリは主に API トークン認証に焦点を当てており、組み込みの認証サービスは Cookie ベースのブラウザ認証に焦点を当てています。多くのアプリケーションは、Laravel の組み込み Cookie ベースの認証サービスと、Laravel の API 認証パッケージの 1 つの両方を使用します。

<!-- **Passport** -->
**Passport**

<!-- Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport. -->
Passport は OAuth2 認証プロバイダであり、さまざまなタイプのトークンを発行できるさまざまな OAuth2 「許可タイプ」を提供します。一般に、これは API 認証用の堅牢かつ複雑なパッケージです。ただし、ほとんどのアプリケーションは OAuth2 仕様によって提供される複雑な機能を必要としないため、ユーザーと開発者の両方にとって混乱を招く可能性があります。さらに、開発者はこれまで、Passport などの OAuth2 認証プロバイダを使用して SPA アプリケーションやモバイル アプリケーションを認証する方法について混乱してきました。

<!-- **Sanctum** -->
**Sanctum**

<!-- In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/11.x/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client. -->
OAuth2 の複雑さと開発者の混乱に応えて、私たちは Web ブラウザーからのファーストパーティ Web リクエストとトークン経由の API リクエストの両方を処理できる、よりシンプルで合理化された認証パッケージの構築に着手しました。この目標は、[Laravel Sanctum](/docs/11.x/sanctum) のリリースによって実現されました。これは、API に加えてファーストパーティの Web UI を提供するアプリケーション、またはバックエンドの Laravel アプリケーションとは別に存在するシングルページ アプリケーション (SPA) によって動作するアプリケーション、またはモバイル クライアントを提供するアプリケーションにとって、優先および推奨される認証パッケージと見なされるべきです。

<!-- Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/11.x/sanctum#how-it-works) documentation. -->
Laravel Sanctum は、アプリケーションの認証プロセス全体を管理できるハイブリッド Web/API 認証パッケージです。これが可能なのは、Sanctum ベースのアプリケーションがリクエストを受信すると、Sanctum が最初にリクエストに認証されたセッションを参照するセッション Cookie が含まれているかどうかを判断するためです。 Sanctum は、前に説明した Laravel の組み込み認証サービスを呼び出すことでこれを実現します。リクエストがセッション Cookie によって認証されていない場合、Sanctum は API トークンのリクエストを検査します。 API トークンが存在する場合、Sanctum はそのトークンを使用してリクエストを認証します。このプロセスの詳細については、Sanctum の ["how it works"](/docs/11.x/sanctum#how-it-works) ドキュメントを参照してください。

<!-- Laravel Sanctum is the API package we have chosen to include with the [Laravel Jetstream](https://jetstream.laravel.com) application starter kit because we believe it is the best fit for the majority of web application's authentication needs. -->
Laravel Sanctum は、Web アプリケーションの認証ニーズの大部分に最適であると考えているため、[Laravel Jetstream](https://jetstream.laravel.com) アプリケーション スターター キットに含めることを選択した API パッケージです。

<a name="summary-choosing-your-stack"></a>
<!-- #### Summary and Choosing Your Stack -->
#### Summary and Choosing Your Stack

<!-- In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services. -->
要約すると、アプリケーションがブラウザを使用してアクセスされ、モノリシックな Laravel アプリケーションを構築している場合、アプリケーションは Laravel の組み込み認証サービスを使用します。

<!-- Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/11.x/passport) or [Sanctum](/docs/11.x/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities". -->
次に、アプリケーションがサードパーティによって使用される API を提供する場合は、アプリケーションに API トークン認証を提供するために [Passport](/docs/11.x/passport) または [Sanctum](/docs/11.x/sanctum) のいずれかを選択します。一般に、Sanctum は、「スコープ」または「能力」のサポートを含め、API 認証、SPA 認証、およびモバイル認証のシンプルで完全なソリューションであるため、可能な限り推奨されます。

<!-- If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/11.x/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/11.x/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more. -->
Laravel バックエンドを利用するシングルページ アプリケーション (SPA) を構築している場合は、[Laravel Sanctum](/docs/11.x/sanctum) を使用する必要があります。 Sanctum を使用する場合は、[manually implement your own backend authentication routes](#authenticating-users) を実行するか、登録、パスワードリセット、電子メール検証などの機能のルートとコントローラを提供するヘッドレス認証バックエンド サービスとして [Laravel Fortify](/docs/11.x/fortify) を利用する必要があります。

<!-- Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. -->
アプリケーションが OAuth2 仕様で提供されるすべての機能を絶対に必要とする場合は、Passportを選択できます。

<!-- And, if you would like to get started quickly, we are pleased to recommend [Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services and Laravel Sanctum. -->
また、すぐに始めたい場合は、Laravel の組み込み認証サービスと Laravel Sanctum の推奨認証スタックを既に使用している新しい Laravel アプリケーションを簡単に開始する方法として、[Laravel Breeze](/docs/11.x/starter-kits#laravel-breeze) をお勧めします。

<a name="authentication-quickstart"></a>
<!-- ## Authentication Quickstart -->
## Authentication Quickstart

> [!WARNING]
> ドキュメントのこの部分では、[Laravel application starter kits](/docs/11.x/starter-kits) を介したユーザーの認証について説明します。これには、すぐに開始できるようにする UI スキャフォールディングが含まれています。 Laravel の認証システムと直接統合したい場合は、[manually authenticating users](#authenticating-users) のドキュメントを確認してください。

<a name="install-a-starter-kit"></a>
<!-- ### Install a Starter Kit -->
### Install a Starter Kit

<!-- First, you should [install a Laravel application starter kit](/docs/11.x/starter-kits). Our current starter kits, Laravel Breeze and Laravel Jetstream, offer beautifully designed starting points for incorporating authentication into your fresh Laravel application. -->
まず、[install a Laravel application starter kit](/docs/11.x/starter-kits) を実行する必要があります。現在のスターター キットである Laravel Breeze と Laravel Jetstream は、新しい Laravel アプリケーションに認証を組み込むための美しく設計された出発点を提供します。

<!-- Laravel Breeze is a minimal, simple implementation of all of Laravel's authentication features, including login, registration, password reset, email verification, and password confirmation. Laravel Breeze's view layer is made up of simple [Blade templates](/docs/11.x/blade) styled with [Tailwind CSS](https://tailwindcss.com). Additionally, Breeze provides scaffolding options based on [Livewire](https://livewire.laravel.com) or [Inertia](https://inertiajs.com), with the choice of using Vue or React for the Inertia-based scaffolding. -->
Laravel Breeze は、ログイン、登録、パスワードのリセット、電子メール検証、パスワード確認を含む、Laravel のすべての認証機能を最小限にシンプルに実装したものです。 Laravel Breeze のビューレイヤーは、[Blade templates](/docs/11.x/blade) でスタイル設定されたシンプルな [Tailwind CSS](https://tailwindcss.com) で構成されています。さらに、Breeze は、[Livewire](https://livewire.laravel.com) または [Inertia](https://inertiajs.com) に基づくスキャフォールディング オプションを提供し、Inertiaベースのスキャフォールディングに Vue または React を使用することを選択できます。

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a more robust application starter kit that includes support for scaffolding your application with [Livewire](https://livewire.laravel.com) or [Inertia and Vue](https://inertiajs.com). In addition, Jetstream features optional support for two-factor authentication, teams, profile management, browser session management, API support via [Laravel Sanctum](/docs/11.x/sanctum), account deletion, and more. -->
[Laravel Jetstream](https://jetstream.laravel.com) は、[Livewire](https://livewire.laravel.com) または [Inertia and Vue](https://inertiajs.com) を使用したアプリケーションのスキャフォールディングのサポートを含む、より堅牢なアプリケーション スターター キットです。さらに、Jetstream は、2 要素認証、チーム、プロファイル管理、ブラウザー セッション管理、[Laravel Sanctum](/docs/11.x/sanctum) 経由の API サポート、アカウント削除などのオプション サポートを備えています。

<a name="retrieving-the-authenticated-user"></a>
<!-- ### Retrieving the Authenticated User -->
### Retrieving the Authenticated User

<!-- After installing an authentication starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method: -->
認証スターター キットをインストールし、ユーザーがアプリケーションに登録して認証できるようにした後、多くの場合、現在認証されているユーザーと対話する必要があります。受信リクエストの処理中に、`Auth` ファサードの `user` メソッドを介して認証されたユーザーにアクセスできます。

```
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```

<!-- Alternatively, once a user is authenticated, you may access the authenticated user via an `Illuminate\Http\Request` instance. Remember, type-hinted classes will automatically be injected into your controller methods. By type-hinting the `Illuminate\Http\Request` object, you may gain convenient access to the authenticated user from any controller method in your application via the request's `user` method: -->
あるいは、ユーザーが認証されると、`Illuminate\Http\Request` インスタンス経由で認証されたユーザーにアクセスできます。タイプヒント付きクラスはコントローラのメソッドに自動的に挿入されることに注意してください。 `Illuminate\Http\Request` オブジェクトをタイプヒントすることにより、リクエストの `user` メソッドを介して、アプリケーション内の任意のコントローラ メソッドから認証されたユーザーに簡単にアクセスできるようになります。

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```

<a name="determining-if-the-current-user-is-authenticated"></a>
<!-- #### Determining if the Current User is Authenticated -->
#### Determining if the Current User is Authenticated

<!-- To determine if the user making the incoming HTTP request is authenticated, you may use the `check` method on the `Auth` facade. This method will return `true` if the user is authenticated: -->
受信 HTTP リクエストを行っているユーザーが認証されているかどうかを確認するには、`Auth` ファサードで `check` メソッドを使用できます。ユーザーが認証されている場合、このメソッドは `true` を返します。

```
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```

> [!NOTE]
> `check` メソッドを使用してユーザーが認証されているかどうかを判断することは可能ですが、通常は、ユーザーに特定のルート/コントローラへのアクセスを許可する前に、ミドルウェアを使用してユーザーが認証されていることを確認します。これについて詳しくは、[protecting routes](/docs/11.x/authentication#protecting-routes) のドキュメントを参照してください。

<a name="protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- [Route middleware](/docs/11.x/middleware) can be used to only allow authenticated users to access a given route. Laravel ships with an `auth` middleware, which is a [middleware alias](/docs/11.x/middleware#middleware-aliases) for the `Illuminate\Auth\Middleware\Authenticate` class. Since this middleware is already aliased internally by Laravel, all you need to do is attach the middleware to a route definition: -->
[Route middleware](/docs/11.x/middleware) を使用すると、認証されたユーザーに特定のルートへのアクセスのみを許可できます。 Laravel には、`auth` ミドルウェアが同梱されています。これは、`Illuminate\Auth\Middleware\Authenticate` クラスの [middleware alias](/docs/11.x/middleware#middleware-aliases) です。このミドルウェアはすでに Laravel によって内部的にエイリアス化されているため、必要なのはミドルウェアをルート定義にアタッチすることだけです。

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```

<a name="redirecting-unauthenticated-users"></a>
<!-- #### Redirecting Unauthenticated Users -->
#### Redirecting Unauthenticated Users

<!-- When the `auth` middleware detects an unauthenticated user, it will redirect the user to the `login` [named route](/docs/11.x/routing#named-routes). You may modify this behavior using the method `redirectGuestsTo` of your application's `bootstrap/app.php` file: -->
`auth` ミドルウェアは、認証されていないユーザーを検出すると、ユーザーを `login` [named route](/docs/11.x/routing#named-routes) にリダイレクトします。アプリケーションの `bootstrap/app.php` ファイルのメソッド `redirectGuestsTo` を使用して、この動作を変更できます。

```
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware) {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```

<a name="specifying-a-guard"></a>
<!-- #### Specifying a Guard -->
#### Specifying a Guard

<!-- When attaching the `auth` middleware to a route, you may also specify which "guard" should be used to authenticate the user. The guard specified should correspond to one of the keys in the `guards` array of your `auth.php` configuration file: -->
`auth` ミドルウェアをルートにアタッチする場合、ユーザーの認証にどの「ガード」を使用するかを指定することもできます。指定したガードは、`auth.php` 構成ファイルの `guards` 配列内のキーの 1 つに対応する必要があります。

```
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```

<a name="login-throttling"></a>
<!-- ### Login Throttling -->
### Login Throttling

<!-- If you are using the Laravel Breeze or Laravel Jetstream [starter kits](/docs/11.x/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address. -->
Laravel Breeze または Laravel Jetstream [starter kits](/docs/11.x/starter-kits) を使用している場合、ログイン試行にレート制限が自動的に適用されます。デフォルトでは、ユーザーは数回試行しても正しい認証情報を入力できなかった場合、1 分間ログインできなくなります。スロットリングは、ユーザーのユーザー名/電子メール アドレスおよび IP アドレスに固有です。

> [!NOTE]
> アプリケーション内の他のルートをレート制限したい場合は、[rate limiting documentation](/docs/11.x/routing#rate-limiting) を確認してください。

<a name="authenticating-users"></a>
<!-- ## Manually Authenticating Users -->
## Manually Authenticating Users

<!-- You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/11.x/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch! -->
Laravel の [application starter kits](/docs/11.x/starter-kits) に含まれる認証スキャフォールディングを使用する必要はありません。このスキャフォールディングを使用しないことを選択した場合は、Laravel 認証クラスを直接使用してユーザー認証を管理する必要があります。心配しないでください、それは簡単です!

<!-- We will access Laravel's authentication services via the `Auth` [facade](/docs/11.x/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/11.x/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation): -->
`Auth` [facade](/docs/11.x/facades) 経由で Laravel の認証サービスにアクセスするため、クラスの先頭に `Auth` ファサードをインポートする必要があります。次に、`attempt` メソッドを確認してみましょう。 `attempt` メソッドは通常、アプリケーションの「ログイン」フォームからの認証試行を処理するために使用されます。認証が成功した場合は、ユーザーの [session](/docs/11.x/session) を再生成して [session fixation](https://en.wikipedia.org/wiki/Session_fixation) を防ぐ必要があります。

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```

<!-- The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the `password` value passed to the method via the array. You should not hash the incoming request's `password` value, since the framework will automatically hash the value before comparing it to the hashed password in the database. An authenticated session will be started for the user if the two hashed passwords match. -->
`attempt` メソッドは、キーと値のペアの配列を最初の引数として受け入れます。配列内の値は、データベース テーブル内でユーザーを検索するために使用されます。したがって、上記の例では、ユーザーは `email` 列の値によって取得されます。ユーザーが見つかった場合、データベースに保存されているハッシュ化されたパスワードが、配列を介してメソッドに渡された `password` 値と比較されます。受信リクエストの `password` 値をハッシュしないでください。フレームワークは、値をデータベース内のハッシュされたパスワードと比較する前に自動的にハッシュするからです。 2 つのハッシュ化されたパスワードが一致する場合、ユーザーの認証されたセッションが開始されます。

<!-- Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application. -->
Laravel の認証サービスは、認証ガードの「プロバイダ」設定に基づいてデータベースからユーザーを取得することに注意してください。デフォルトの `config/auth.php` 構成ファイルでは、Eloquent ユーザー プロバイダが指定されており、ユーザーを取得するときに `App\Models\User` モデルを使用するように指示されます。アプリケーションのニーズに基づいて、構成ファイル内でこれらの値を変更できます。

<!-- The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned. -->
認証が成功した場合、`attempt` メソッドは `true` を返します。それ以外の場合は、`false` が返されます。

<!-- The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available. -->
Laravel のリダイレクターによって提供される `intended` メソッドは、認証ミドルウェアによって傍受される前に、ユーザーがアクセスしようとしていた URL にユーザーをリダイレクトします。意図した宛先が利用できない場合に備えて、このメソッドにフォールバック URI を指定できます。

<a name="specifying-additional-conditions"></a>
<!-- #### Specifying Additional Conditions -->
#### Specifying Additional Conditions

<!-- If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active": -->
必要に応じて、ユーザーの電子メールとパスワードに加えて、追加のクエリ条件を認証クエリに追加することもできます。これを実現するには、`attempt` メソッドに渡される配列にクエリ条件を追加するだけです。たとえば、ユーザーが「アクティブ」としてマークされていることを確認できます。

```
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```

<!-- For complex query conditions, you may provide a closure in your array of credentials. This closure will be invoked with the query instance, allowing you to customize the query based on your application's needs: -->
複雑なクエリ条件の場合は、資格情報の配列にクロージャを指定できます。このクロージャはクエリ インスタンスで呼び出され、アプリケーションのニーズに基づいてクエリをカスタマイズできます。

```
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```

> [!WARNING]
> これらの例では、`email` は必須のオプションではなく、単に例として使用されています。データベーステーブルの「ユーザー名」に対応する列名を使用する必要があります。

<!-- The `attemptWhen` method, which receives a closure as its second argument, may be used to perform more extensive inspection of the potential user before actually authenticating the user. The closure receives the potential user and should return `true` or `false` to indicate if the user may be authenticated: -->
2 番目の引数としてクロージャを受け取る `attemptWhen` メソッドは、実際にユーザーを認証する前に、潜在的なユーザーのより広範な検査を実行するために使用できます。クロージャーは潜在的なユーザーを受け取り、ユーザーが認証されているかどうかを示す `true` または `false` を返す必要があります。

```
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```

<a name="accessing-specific-guard-instances"></a>
<!-- #### Accessing Specific Guard Instances -->
#### Accessing Specific Guard Instances

<!-- Via the `Auth` facade's `guard` method, you may specify which guard instance you would like to utilize when authenticating the user. This allows you to manage authentication for separate parts of your application using entirely separate authenticatable models or user tables. -->
`Auth` ファサードの `guard` メソッドを使用して、ユーザーの認証時にどのガード インスタンスを使用するかを指定できます。これにより、完全に別個の認証可能なモデルまたはユーザー テーブルを使用して、アプリケーションの別個の部分の認証を管理できます。

<!-- The guard name passed to the `guard` method should correspond to one of the guards configured in your `auth.php` configuration file: -->
`guard` メソッドに渡されるガード名は、`auth.php` 構成ファイルで構成されたガードの 1 つに対応する必要があります。

```
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```

<a name="remembering-users"></a>
<!-- ### Remembering Users -->
### Remembering Users

<!-- Many web applications provide a "remember me" checkbox on their login form. If you would like to provide "remember me" functionality in your application, you may pass a boolean value as the second argument to the `attempt` method. -->
多くの Web アプリケーションには、ログイン フォームに「記憶する」チェックボックスが用意されています。アプリケーションに「記憶する」機能を提供したい場合は、`attempt` メソッドの 2 番目の引数としてブール値を渡すことができます。

<!-- When this value is `true`, Laravel will keep the user authenticated indefinitely or until they manually logout. Your `users` table must include the string `remember_token` column, which will be used to store the "remember me" token. The `users` table migration included with new Laravel applications already includes this column: -->
この値が `true` の場合、Laravel はユーザーを無期限に、または手動でログアウトするまで認証し続けます。 `users` テーブルには、「remember me」トークンを保存するために使用される文字列 `remember_token` 列が含まれている必要があります。新しい Laravel アプリケーションに含まれる `users` テーブルの移行には、すでに次の列が含まれています。

```
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```

<!-- If your application offers "remember me" functionality, you may use the `viaRemember`  method to determine if the currently authenticated user was authenticated using the "remember me" cookie: -->
アプリケーションが「remember me」機能を提供する場合、`viaRemember` メソッドを使用して、現在認証されているユーザーが「remember me」Cookie を使用して認証されたかどうかを判断できます。

```
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```

<a name="other-authentication-methods"></a>
<!-- ### Other Authentication Methods -->
### Other Authentication Methods

<a name="authenticate-a-user-instance"></a>
<!-- #### Authenticate a User Instance -->
#### Authenticate a User Instance

<!-- If you need to set an existing user instance as the currently authenticated user, you may pass the user instance to the `Auth` facade's `login` method. The given user instance must be an implementation of the `Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/11.x/contracts). The `App\Models\User` model included with Laravel already implements this interface. This method of authentication is useful when you already have a valid user instance, such as directly after a user registers with your application: -->
既存のユーザー インスタンスを現在認証されているユーザーとして設定する必要がある場合は、そのユーザー インスタンスを `Auth` ファサードの `login` メソッドに渡すことができます。指定されたユーザー インスタンスは、`Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/11.x/contracts) の実装である必要があります。 Laravel に含まれる `App\Models\User` モデルはすでにこのインターフェイスを実装しています。この認証方法は、ユーザーがアプリケーションに登録した直後など、有効なユーザー インスタンスがすでにある場合に役立ちます。

```
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```

<!-- You may pass a boolean value as the second argument to the `login` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`login` メソッドの 2 番目の引数としてブール値を渡すことができます。この値は、認証されたセッションに「記憶する」機能が必要かどうかを示します。これは、セッションが無期限に、またはユーザーがアプリケーションから手動でログアウトするまで認証されることを意味することに注意してください。

```
Auth::login($user, $remember = true);
```

<!-- If needed, you may specify an authentication guard before calling the `login` method: -->
必要に応じて、`login` メソッドを呼び出す前に認証ガードを指定できます。

```
Auth::guard('admin')->login($user);
```

<a name="authenticate-a-user-by-id"></a>
<!-- #### Authenticate a User by ID -->
#### Authenticate a User by ID

<!-- To authenticate a user using their database record's primary key, you may use the `loginUsingId` method. This method accepts the primary key of the user you wish to authenticate: -->
データベース レコードの主キーを使用してユーザーを認証するには、`loginUsingId` メソッドを使用できます。このメソッドは、認証するユーザーの主キーを受け入れます。

```
Auth::loginUsingId(1);
```

<!-- You may pass a boolean value to the `remember` argument of the `loginUsingId` method. This value indicates if "remember me" functionality is desired for the authenticated session. Remember, this means that the session will be authenticated indefinitely or until the user manually logs out of the application: -->
`loginUsingId` メソッドの `remember` 引数にブール値を渡すことができます。この値は、認証されたセッションに「記憶する」機能が必要かどうかを示します。これは、セッションが無期限に、またはユーザーがアプリケーションから手動でログアウトするまで認証されることを意味することに注意してください。

```
Auth::loginUsingId(1, remember: true);
```

<a name="authenticate-a-user-once"></a>
<!-- #### Authenticate a User Once -->
#### Authenticate a User Once

<!-- You may use the `once` method to authenticate a user with the application for a single request. No sessions or cookies will be utilized when calling this method: -->
`once` メソッドを使用して、単一のリクエストに対してアプリケーションでユーザーを認証できます。このメソッドを呼び出す場合、セッションや Cookie は使用されません。

```
if (Auth::once($credentials)) {
    // ...
}
```

<a name="http-basic-authentication"></a>
<!-- ## HTTP Basic Authentication -->
## HTTP Basic Authentication

<!-- [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) provides a quick way to authenticate users of your application without setting up a dedicated "login" page. To get started, attach the `auth.basic` [middleware](/docs/11.x/middleware) to a route. The `auth.basic` middleware is included with the Laravel framework, so you do not need to define it: -->
[HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) は、専用の「ログイン」ページを設定せずに、アプリケーションのユーザーを認証する迅速な方法を提供します。まず、`auth.basic` [middleware](/docs/11.x/middleware) をルートにアタッチします。 `auth.basic` ミドルウェアは Laravel フレームワークに含まれているため、定義する必要はありません。

```
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```

<!-- Once the middleware has been attached to the route, you will automatically be prompted for credentials when accessing the route in your browser. By default, the `auth.basic` middleware will assume the `email` column on your `users` database table is the user's "username". -->
ミドルウェアがルートにアタッチされると、ブラウザでルートにアクセスするときに自動的に資格情報の入力を求められます。デフォルトでは、`auth.basic` ミドルウェアは、`users` データベース テーブルの `email` 列がユーザーの「ユーザー名」であると想定します。

<a name="a-note-on-fastcgi"></a>
<!-- #### A Note on FastCGI -->
#### A Note on FastCGI

<!-- If you are using PHP FastCGI and Apache to serve your Laravel application, HTTP Basic authentication may not work correctly. To correct these problems, the following lines may be added to your application's `.htaccess` file: -->
PHP FastCGI と Apache を使用して Laravel アプリケーションを提供している場合、HTTP 基本認証が正しく機能しない可能性があります。これらの問題を修正するには、アプリケーションの `.htaccess` ファイルに次の行を追加します。

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
<!-- ### Stateless HTTP Basic Authentication -->
### Stateless HTTP Basic Authentication

<!-- You may also use HTTP Basic Authentication without setting a user identifier cookie in the session. This is primarily helpful if you choose to use HTTP Authentication to authenticate requests to your application's API. To accomplish this, [define a middleware](/docs/11.x/middleware) that calls the `onceBasic` method. If no response is returned by the `onceBasic` method, the request may be passed further into the application: -->
セッションにユーザー識別子 Cookie を設定せずに、HTTP 基本認証を使用することもできます。これは主に、アプリケーションの API へのリクエストを認証するために HTTP 認証を使用することを選択した場合に役立ちます。これを実現するには、`onceBasic` メソッドを呼び出す [define a middleware](/docs/11.x/middleware) 。 `onceBasic` メソッドから応答が返されない場合、リクエストはさらにアプリケーションに渡される可能性があります。

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```

<!-- Next, attach the middleware to a route: -->
次に、ミドルウェアをルートにアタッチします。

```
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```

<a name="logging-out"></a>
<!-- ## Logging Out -->
## Logging Out

<!-- To manually log users out of your application, you may use the `logout` method provided by the `Auth` facade. This will remove the authentication information from the user's session so that subsequent requests are not authenticated. -->
ユーザーをアプリケーションから手動でログアウトするには、`Auth` ファサードによって提供される `logout` メソッドを使用できます。これにより、ユーザーのセッションから認証情報が削除され、後続のリクエストは認証されなくなります。

<!-- In addition to calling the `logout` method, it is recommended that you invalidate the user's session and regenerate their [CSRF token](/docs/11.x/csrf). After logging the user out, you would typically redirect the user to the root of your application: -->
`logout` メソッドの呼び出しに加えて、ユーザーのセッションを無効にして [CSRF token](/docs/11.x/csrf) を再生成することをお勧めします。ユーザーをログアウトした後、通常はユーザーをアプリケーションのルートにリダイレクトします。

```
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```

<a name="invalidating-sessions-on-other-devices"></a>
<!-- ### Invalidating Sessions on Other Devices -->
### Invalidating Sessions on Other Devices

<!-- Laravel also provides a mechanism for invalidating and "logging out" a user's sessions that are active on other devices without invalidating the session on their current device. This feature is typically utilized when a user is changing or updating their password and you would like to invalidate sessions on other devices while keeping the current device authenticated. -->
Laravel は、現在のデバイスのセッションを無効にすることなく、他のデバイスでアクティブなユーザーのセッションを無効にして「ログアウト」するメカニズムも提供します。この機能は通常、ユーザーがパスワードを変更または更新するときに、現在のデバイスの認証を維持しながら他のデバイスのセッションを無効にする場合に使用されます。

<!-- Before getting started, you should make sure that the `Illuminate\Session\Middleware\AuthenticateSession` middleware is included on the routes that should receive session authentication. Typically, you should place this middleware on a route group definition so that it can be applied to the majority of your application's routes. By default, the `AuthenticateSession` middleware may be attached to a route using the `auth.session` [middleware alias](/docs/11.x/middleware#middleware-aliases): -->
開始する前に、セッション認証を受け取る必要があるルートに `Illuminate\Session\Middleware\AuthenticateSession` ミドルウェアが含まれていることを確認する必要があります。通常、このミドルウェアをルート グループ定義に配置して、アプリケーションのルートの大部分に適用できるようにする必要があります。デフォルトでは、`AuthenticateSession` ミドルウェアは、`auth.session` [middleware alias](/docs/11.x/middleware#middleware-aliases) を使用してルートに接続できます。

```
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```

<!-- Then, you may use the `logoutOtherDevices` method provided by the `Auth` facade. This method requires the user to confirm their current password, which your application should accept through an input form: -->
その後、`Auth` ファサードによって提供される `logoutOtherDevices` メソッドを使用できます。この方法では、ユーザーは現在のパスワードを確認する必要があり、アプリケーションは入力フォームを通じてこのパスワードを受け入れる必要があります。

```
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```

<!-- When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by. -->
`logoutOtherDevices` メソッドが呼び出されると、ユーザーの他のセッションは完全に無効になります。つまり、以前に認証されたすべてのガードから「ログアウト」されます。

<a name="password-confirmation"></a>
<!-- ## Password Confirmation -->
## Password Confirmation

<!-- While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination. -->
アプリケーションの構築中に、アクションを実行する前、またはユーザーがアプリケーションの機密領域にリダイレクトされる前に、ユーザーにパスワードの確認を要求するアクションが発生する場合があります。 Laravel には、このプロセスを簡単にする組み込みのミドルウェアが含まれています。この機能を実装するには、2 つのルートを定義する必要があります。1 つはユーザーにパスワードの確認を求めるビューを表示するルート、もう 1 つはパスワードが有効であることを確認し、ユーザーを目的の宛先にリダイレクトするルートです。

> [!NOTE]
> 次のドキュメントでは、Laravel のパスワード確認機能と直接統合する方法について説明します。ただし、より迅速に開始したい場合は、[Laravel application starter kits](/docs/11.x/starter-kits) にこの機能のサポートが含まれています。

<a name="password-confirmation-configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file. -->
パスワードを確認した後、ユーザーは 3 時間はパスワードの再確認を求められません。ただし、アプリケーションの `config/auth.php` 構成ファイル内の `password_timeout` 構成値の値を変更することで、ユーザーにパスワードの再入力を求めるまでの時間を構成できます。

<a name="password-confirmation-routing"></a>
<!-- ### Routing -->
### Routing

<a name="the-password-confirmation-form"></a>
<!-- #### The Password Confirmation Form -->
#### The Password Confirmation Form

<!-- First, we will define a route to display a view that requests the user to confirm their password: -->
まず、ユーザーにパスワードの確認を要求するビューを表示するルートを定義します。

```
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```

<!-- As you might expect, the view that is returned by this route should have a form containing a `password` field. In addition, feel free to include text within the view that explains that the user is entering a protected area of the application and must confirm their password. -->
ご想像のとおり、このルートによって返されるビューには、`password` フィールドを含むフォームが含まれている必要があります。さらに、ユーザーがアプリケーションの保護された領域に入ろうとしているため、パスワードを確認する必要があることを説明するテキストをビュー内に自由に含めることができます。

<a name="confirming-the-password"></a>
<!-- #### Confirming the Password -->
#### Confirming the Password

<!-- Next, we will define a route that will handle the form request from the "confirm password" view. This route will be responsible for validating the password and redirecting the user to their intended destination: -->
次に、「パスワードの確認」ビューからのフォームリクエストを処理するルートを定義します。このルートは、パスワードを検証し、ユーザーを目的の宛先にリダイレクトする役割を果たします。

```
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```

<!-- Before moving on, let's examine this route in more detail. First, the request's `password` field is determined to actually match the authenticated user's password. If the password is valid, we need to inform Laravel's session that the user has confirmed their password. The `passwordConfirmed` method will set a timestamp in the user's session that Laravel can use to determine when the user last confirmed their password. Finally, we can redirect the user to their intended destination. -->
次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `password` フィールドが、認証されたユーザーのパスワードと実際に一致するかどうかが判断されます。パスワードが有効な場合は、ユーザーがパスワードを確認したことをLaravelのセッションに通知する必要があります。 `passwordConfirmed` メソッドは、Laravel がユーザーが最後にパスワードを確認した日時を判断するために使用できるタイムスタンプをユーザーのセッションに設定します。最後に、ユーザーを目的の宛先にリダイレクトできます。

<a name="password-confirmation-protecting-routes"></a>
<!-- ### Protecting Routes -->
### Protecting Routes

<!-- You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/11.x/routing#named-routes): -->
最近のパスワードの確認を必要とするアクションを実行するルートには、`password.confirm` ミドルウェアが割り当てられていることを確認する必要があります。このミドルウェアは Laravel のデフォルトのインストールに含まれており、ユーザーがパスワードを確認した後にその場所にリダイレクトされるように、ユーザーの意図した宛先をセッションに自動的に保存します。ユーザーの意図した宛先をセッションに保存した後、ミドルウェアはユーザーを `password.confirm` [named route](/docs/11.x/routing#named-routes) にリダイレクトします。

```
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```

<a name="adding-custom-guards"></a>
<!-- ## Adding Custom Guards -->
## Adding Custom Guards

<!-- You may define your own authentication guards using the `extend` method on the `Auth` facade. You should place your call to the `extend` method within a [service provider](/docs/11.x/providers). Since Laravel already ships with an `AppServiceProvider`, we can place the code in that provider: -->
`Auth` ファサードで `extend` メソッドを使用して、独自の認証ガードを定義できます。 `extend` メソッドの呼び出しは [service provider](/docs/11.x/providers) 内で行う必要があります。 Laravel にはすでに `AppServiceProvider` が同梱されているため、コードをそのプロバイダに配置できます。

```
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```

<!-- As you can see in the example above, the callback passed to the `extend` method should return an implementation of `Illuminate\Contracts\Auth\Guard`. This interface contains a few methods you will need to implement to define a custom guard. Once your custom guard has been defined, you may reference the guard in the `guards` configuration of your `auth.php` configuration file: -->
上の例でわかるように、`extend` メソッドに渡されるコールバックは、`Illuminate\Contracts\Auth\Guard` の実装を返す必要があります。このインターフェイスには、カスタム ガードを定義するために実装する必要があるメソッドがいくつか含まれています。カスタム ガードが定義されたら、`auth.php` 構成ファイルの `guards` 構成でガードを参照できます。

```
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```

<a name="closure-request-guards"></a>
<!-- ### Closure Request Guards -->
### Closure Request Guards

<!-- The simplest way to implement a custom, HTTP request based authentication system is by using the `Auth::viaRequest` method. This method allows you to quickly define your authentication process using a single closure. -->
カスタムの HTTP リクエスト ベースの認証システムを実装する最も簡単な方法は、`Auth::viaRequest` メソッドを使用することです。このメソッドを使用すると、単一のクロージャを使用して認証プロセスを迅速に定義できます。

<!-- To get started, call the `Auth::viaRequest` method within the `boot` method of your application's `AppServiceProvider`. The `viaRequest` method accepts an authentication driver name as its first argument. This name can be any string that describes your custom guard. The second argument passed to the method should be a closure that receives the incoming HTTP request and returns a user instance or, if authentication fails, `null`: -->
まず、アプリケーションの `AppServiceProvider` の `boot` メソッド内で `Auth::viaRequest` メソッドを呼び出します。 `viaRequest` メソッドは、最初の引数として認証ドライバ名を受け入れます。この名前には、カスタム ガードを説明する任意の文字列を指定できます。メソッドに渡される 2 番目の引数は、受信 HTTP リクエストを受け取り、ユーザー インスタンスを返すか、認証が失敗した場合は `null` を返すクロージャである必要があります。

```
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```

<!-- Once your custom authentication driver has been defined, you may configure it as a driver within the `guards` configuration of your `auth.php` configuration file: -->
カスタム認証ドライバを定義したら、それを `auth.php` 構成ファイルの `guards` 構成内のドライバとして構成できます。

```
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```

<!-- Finally, you may reference the guard when assigning the authentication middleware to a route: -->
最後に、認証ミドルウェアをルートに割り当てるときにガードを参照できます。

```
Route::middleware('auth:api')->group(function () {
    // ...
});
```

<a name="adding-custom-user-providers"></a>
<!-- ## Adding Custom User Providers -->
## Adding Custom User Providers

<!-- If you are not using a traditional relational database to store your users, you will need to extend Laravel with your own authentication user provider. We will use the `provider` method on the `Auth` facade to define a custom user provider. The user provider resolver should return an implementation of `Illuminate\Contracts\Auth\UserProvider`: -->
ユーザーの保存に従来のリレーショナル データベースを使用していない場合は、独自の認証ユーザー プロバイダを使用して Laravel を拡張する必要があります。 `Auth` ファサードで `provider` メソッドを使用して、カスタム ユーザー プロバイダを定義します。ユーザー プロバイダ リゾルバーは、`Illuminate\Contracts\Auth\UserProvider` の実装を返す必要があります。

```
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```

<!-- After you have registered the provider using the `provider` method, you may switch to the new user provider in your `auth.php` configuration file. First, define a `provider` that uses your new driver: -->
`provider` メソッドを使用してプロバイダを登録した後、`auth.php` 構成ファイルで新しいユーザー プロバイダに切り替えることができます。まず、新しいドライバを使用する `provider` を定義します。

```
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```

<!-- Finally, you may reference this provider in your `guards` configuration: -->
最後に、`guards` 構成でこのプロバイダを参照できます。

```
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```

<a name="the-user-provider-contract"></a>
<!-- ### The User Provider Contract -->
### The User Provider Contract

<!-- `Illuminate\Contracts\Auth\UserProvider` implementations are responsible for fetching an `Illuminate\Contracts\Auth\Authenticatable` implementation out of a persistent storage system, such as MySQL, MongoDB, etc. These two interfaces allow the Laravel authentication mechanisms to continue functioning regardless of how the user data is stored or what type of class is used to represent the authenticated user: -->
`Illuminate\Contracts\Auth\UserProvider` 実装は、MySQL、MongoDB などの永続ストレージ システムから `Illuminate\Contracts\Auth\Authenticatable` 実装をフェッチする役割を果たします。これら 2 つのインターフェイスにより、ユーザー データがどのように保存されているか、または認証されたユーザーを表すためにどのような種類のクラスが使用されているかに関係なく、Laravel 認証メカニズムが機能し続けることができます。

<!-- Let's take a look at the `Illuminate\Contracts\Auth\UserProvider` contract: -->
`Illuminate\Contracts\Auth\UserProvider` コントラクトを見てみましょう。

```
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```

<!-- The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method. -->
`retrieveById` 関数は通常、MySQL データベースからの自動インクリメント ID など、ユーザーを表すキーを受け取ります。 ID に一致する `Authenticatable` 実装がメソッドによって取得され、返される必要があります。

<!-- The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method. -->
`retrieveByToken` 関数は、一意の `$identifier` および「remember me」`$token` によってユーザーを取得します。通常、`remember_token` などのデータベース列に保存されます。前のメソッドと同様に、一致するトークン値を持つ `Authenticatable` 実装がこのメソッドによって返される必要があります。

<!-- The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out. -->
`updateRememberToken` メソッドは、`$user` インスタンスの `remember_token` を新しい `$token` で更新します。 「remember me」認証試行が成功したとき、またはユーザーがログアウトしたときに、新しいトークンがユーザーに割り当てられます。

<!-- The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.** -->
`retrieveByCredentials` メソッドは、アプリケーションで認証を試行するときに、`Auth::attempt` メソッドに渡される資格情報の配列を受け取ります。次に、メソッドは、それらの資格情報と一致するユーザーについて、基礎となる永続ストレージを「クエリ」する必要があります。通常、このメソッドは、`$credentials['username']` の値と一致する「ユーザー名」を持つユーザー レコードを検索する「where」条件を使用してクエリを実行します。このメソッドは、`Authenticatable` の実装を返す必要があります。 **このメソッドでは、パスワードの検証や認証を試行しないでください。**

<!-- The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid. -->
`validateCredentials` メソッドは、指定された `$user` と `$credentials` を比較してユーザーを認証する必要があります。たとえば、このメソッドは通常、`Hash::check` メソッドを使用して、`$user->getAuthPassword()` の値を `$credentials['password']` の値と比較します。このメソッドは、パスワードが有効かどうかを示す `true` または `false` を返す必要があります。

<!-- The `rehashPasswordIfRequired` method should rehash the given `$user`'s password if required and supported. For example, this method will typically use the `Hash::needsRehash` method to determine if the `$credentials['password']` value needs to be rehashed. If the password needs to be rehashed, the method should use the `Hash::make` method to rehash the password and update the user's record in the underlying persistent storage. -->
`rehashPasswordIfRequired` メソッドは、必要でサポートされている場合、指定された `$user` のパスワードを再ハッシュする必要があります。たとえば、このメソッドは通常、`Hash::needsRehash` メソッドを使用して、`$credentials['password']` 値を再ハッシュする必要があるかどうかを判断します。パスワードを再ハッシュする必要がある場合、メソッドは `Hash::make` メソッドを使用してパスワードを再ハッシュし、基礎となる永続ストレージ内のユーザーのレコードを更新する必要があります。

<a name="the-authenticatable-contract"></a>
<!-- ### The Authenticatable Contract -->
### The Authenticatable Contract

<!-- Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods: -->
`UserProvider` の各メソッドを調べたので、`Authenticatable` コントラクトを見てみましょう。ユーザープロバイダは、`retrieveById`、`retrieveByToken`、および `retrieveByCredentials` メソッドからこのインターフェイスの実装を返す必要があることに注意してください。

```
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```

<!-- This interface is simple. The `getAuthIdentifierName` method should return the name of the "primary key" column for the user and the `getAuthIdentifier` method should return the "primary key" of the user. When using a MySQL back-end, this would likely be the auto-incrementing primary key assigned to the user record. The `getAuthPasswordName` method should return the name of the user's password column. The `getAuthPassword` method should return the user's hashed password. -->
このインターフェースはシンプルです。 `getAuthIdentifierName` メソッドはユーザーの「主キー」列の名前を返し、`getAuthIdentifier` メソッドはユーザーの「主キー」を返す必要があります。 MySQL バックエンドを使用する場合、これはユーザー レコードに割り当てられる自動インクリメント主キーとなる可能性があります。 `getAuthPasswordName` メソッドは、ユーザーのパスワード列の名前を返す必要があります。 `getAuthPassword` メソッドは、ユーザーのハッシュされたパスワードを返す必要があります。

<!-- This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes an `App\Models\User` class in the `app/Models` directory which implements this interface. -->
このインターフェイスにより、使用している ORM またはストレージ抽象化レイヤーに関係なく、認証システムが任意の「ユーザー」クラスで動作できるようになります。デフォルトでは、Laravel には、このインターフェイスを実装する `App\Models\User` クラスが `app/Models` ディレクトリに含まれています。

<a name="automatic-password-rehashing"></a>
<!-- ## Automatic Password Rehashing -->
## Automatic Password Rehashing

<!-- Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via your application's `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable. -->
Laravel のデフォルトのパスワードハッシュアルゴリズムは bcrypt です。 bcrypt ハッシュの「作業係数」は、アプリケーションの `config/hashing.php` 構成ファイルまたは `BCRYPT_ROUNDS` 環境変数を介して調整できます。

<!-- Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will gracefully and automatically rehash user passwords as users authenticate with your application via Laravel's starter kits or when you [manually authenticate users](#authenticating-users) via the `attempt` method. -->
通常、CPU / GPU の処理能力が増加するにつれて、bcrypt 作業係数は時間の経過とともに増加する必要があります。アプリケーションの bcrypt 作業係数を増やすと、ユーザーが Laravel のスターター キット経由でアプリケーションで認証するとき、または `attempt` メソッド経由で [manually authenticate users](#authenticating-users) するときに、Laravel はユーザー パスワードを適切かつ自動的に再ハッシュします。

<!-- Typically, automatic password rehashing should not disrupt your application; however, you may disable this behavior by publishing the `hashing` configuration file: -->
通常、パスワードの自動再ハッシュによってアプリケーションが中断されることはありません。ただし、`hashing` 構成ファイルを公開することで、この動作を無効にすることができます。

```shell
php artisan config:publish hashing
```

<!-- Once the configuration file has been published, you may set the `rehash_on_login` configuration value to `false`: -->
構成ファイルが公開されたら、`rehash_on_login` 構成値を `false` に設定できます。

```php
'rehash_on_login' => false,
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/11.x/events) during the authentication process. You may [define listeners](/docs/11.x/events) for any of the following events: -->
Laravel は、認証プロセス中にさまざまな [events](/docs/11.x/events) をディスパッチします。次のイベントのいずれかに対して [define listeners](/docs/11.x/events) できます。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| イベント名 |
| --- |
| `Illuminate\Auth\Events\Registered` |
| `Illuminate\Auth\Events\Attempting` |
| `Illuminate\Auth\Events\Authenticated` |
| `Illuminate\Auth\Events\Login` |
| `Illuminate\Auth\Events\Failed` |
| `Illuminate\Auth\Events\Validated` |
| `Illuminate\Auth\Events\Verified` |
| `Illuminate\Auth\Events\Logout` |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout` |
| `Illuminate\Auth\Events\Lockout` |
| `Illuminate\Auth\Events\PasswordReset` |

<!-- </div> -->
</div>

