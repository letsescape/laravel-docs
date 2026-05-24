# 認証 (Authentication)

- [Introduction](#introduction)
    - [スターターキット](#starter-kits)
    - [データベースに関する考慮事項](#introduction-database-considerations)
    - [生態系の概要](#ecosystem-overview)
- [認証クイックスタート](#authentication-quickstart)
    - [スターター キットをインストールする](#install-a-starter-kit)
    - [認証されたユーザーの取得](#retrieving-the-authenticated-user)
    - [ルートを守る](#protecting-routes)
    - [ログインスロットル](#login-throttling)
- [ユーザーを手動で認証する](#authenticating-users)
    - [ユーザーを記憶する](#remembering-users)
    - [その他の認証方法](#other-authentication-methods)
- [HTTP基本認証](#http-basic-authentication)
    - [ステートレスHTTP基本認証](#stateless-http-basic-authentication)
- [ログアウトする](#logging-out)
    - [他のデバイスのセッションを無効にする](#invalidating-sessions-on-other-devices)
- [パスワードの確認](#password-confirmation)
    - [Configuration](#password-confirmation-configuration)
    - [Routing](#password-confirmation-routing)
    - [ルートを守る](#password-confirmation-protecting-routes)
- [カスタムガードの追加](#adding-custom-guards)
    - [閉鎖リクエストガード](#closure-request-guards)
- [カスタム ユーザー プロバイダの追加](#adding-custom-user-providers)
    - [ユーザープロバイダ契約](#the-user-provider-contract)
    - [認証可能な契約](#the-authenticatable-contract)
- [ソーシャル認証](/docs/{{version}}/socialite)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

多くの Web アプリケーションは、ユーザーがアプリケーションで認証して「ログイン」する方法を提供します。この機能を Web アプリケーションに実装することは、複雑で潜在的に危険な作業となる可能性があります。このため、Laravel は、認証を迅速、安全、簡単に実装するために必要なツールを提供するよう努めています。

Laravel の認証機能の中核は、「ガード」と「プロバイダ」で構成されています。ガードは、各リクエストに対してユーザーが認証される方法を定義します。たとえば、Laravel には、セッションストレージと Cookie を使用して状態を維持する `session` ガードが付属しています。

プロバイダは、永続ストレージからユーザーを取得する方法を定義します。 Laravel には、[Eloquent](/docs/{{version}}/eloquent) とデータベース クエリビルダを使用したユーザーの取得のサポートが付属しています。ただし、アプリケーションの必要に応じて追加のプロバイダを自由に定義できます。

アプリケーションの認証構成ファイルは、`config/auth.php` にあります。このファイルには、Laravel の認証サービスの動作を調整するための、十分に文書化されたオプションがいくつか含まれています。

> **注記**
> ガードとプロバイダを「ロール」と「権限」と混同しないでください。権限によるユーザーアクションの承認の詳細については、[authorization](/docs/{{version}}/authorization) ドキュメントを参照してください。

<a name="starter-kits"></a>
### スターターキット

すぐに始めたいですか?新しい Laravel アプリケーションに [Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) をインストールします。データベースを移行した後、ブラウザーで `/register` またはアプリケーションに割り当てられているその他の URL に移動します。スターター キットは、認証システム全体の足場を整えます。

**最終的な Laravel アプリケーションでスターター キットを使用しないことを選択した場合でも、[Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) スターター キットのインストールは、Laravel のすべての認証機能を実際の Laravel プロジェクトに実装する方法を学ぶ素晴らしい機会になります。** Laravel Breeze は認証コントローラ、ルート、ビューを作成するため、これらのファイル内のコードを調べて、Laravel の認証機能がどのように実装されるかを学ぶことができます。

<a name="introduction-database-considerations"></a>
### データベースに関する考慮事項

デフォルトでは、Laravel には `app/Models` ディレクトリに `App\Models\User` [Eloquent モデル](/docs/{{version}}/eloquent) が含まれています。このモデルは、デフォルトの Eloquent 認証ドライバとともに使用できます。アプリケーションが Eloquent を使用していない場合は、Laravel クエリビルダを使用する `database` 認証プロバイダを使用できます。

`App\Models\User` モデルのデータベース スキーマを構築するときは、パスワード列の長さが少なくとも 60 文字であることを確認してください。もちろん、新しい Laravel アプリケーションに含まれる `users` テーブルの移行では、この長さを超える列がすでに作成されています。

また、`users` (または同等の) テーブルに、NULL 許容の 100 文字の文字列 `remember_token` 列が含まれていることを確認する必要があります。この列は、アプリケーションにログインするときに「記憶する」オプションを選択したユーザーのトークンを保存するために使用されます。繰り返しますが、新しい Laravel アプリケーションに含まれるデフォルトの `users` テーブル移行には、この列がすでに含まれています。

<a name="ecosystem-overview"></a>
### 生態系の概要

Laravel は認証に関連するパッケージをいくつか提供しています。続行する前に、Laravel の一般的な認証エコシステムを確認し、各パッケージの意図された目的について説明します。

まず、認証がどのように機能するかを考えてみましょう。 Web ブラウザを使用する場合、ユーザーはログイン フォームを介してユーザー名とパスワードを入力します。これらの資格情報が正しい場合、アプリケーションは認証されたユーザーに関する情報をユーザーの [session](/docs/{{version}}/session) に保存します。ブラウザに発行される Cookie にはセッション ID が含まれているため、アプリケーションへの後続のリクエストでユーザーを正しいセッションに関連付けることができます。セッション Cookie を受信すると、アプリケーションはセッション ID に基づいてセッション データを取得し、認証情報がセッションに保存されていることに注意して、ユーザーを「認証済み」と見なします。

リモート サービスが API にアクセスするために認証が必要な場合、Web ブラウザがないため、通常は認証に Cookie は使用されません。代わりに、リモート サービスはリクエストごとに API トークンを API に送信します。アプリケーションは、受信したトークンを有効な API トークンのテーブルと照合して検証し、その API トークンに関連付けられたユーザーによって実行されたリクエストを「認証」します。

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravelの組み込みブラウザ認証サービス

Laravel には、組み込みの認証サービスとセッション サービスが含まれており、通常は `Auth` および `Session` ファサードを介してアクセスされます。これらの機能は、Web ブラウザから開始されたリクエストに対して Cookie ベースの認証を提供します。これらは、ユーザーの資格情報を確認し、ユーザーを認証できるメソッドを提供します。さらに、これらのサービスは、ユーザーのセッションに適切な認証データを自動的に保存し、ユーザーのセッション Cookie を発行します。これらのサービスの使用方法については、このドキュメントに記載されています。

**アプリケーション スターター キット**

このドキュメントで説明したように、これらの認証サービスと手動で対話して、アプリケーション独自の認証層を構築できます。ただし、より迅速に開始できるように、認証レイヤー全体の堅牢で最新の足場を提供する [無料パッケージ](/docs/{{version}}/starter-kits) をリリースしました。これらのパッケージは、[Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze)、[Laravel Jetstream](/docs/{{version}}/starter-kits#laravel-jetstream)、および [Laravel の強化](/docs/{{version}}/fortify) です。

_Laravel Breeze_ は、ログイン、登録、パスワードのリセット、電子メール検証、パスワード確認を含む、Laravel のすべての認証機能のシンプルかつ最小限の実装です。 Laravel Breeze のビューレイヤーは、[Tailwind CSS](/docs/{{version}}/blade) でスタイル設定されたシンプルな [Blade テンプレート](https://tailwindcss.com) で構成されています。まず、Laravel の [アプリケーションスターターキット](/docs/{{version}}/starter-kits) のドキュメントを確認してください。

_Laravel Fortify_ は、Cookie ベースの認証や 2 要素認証や電子メール検証などの他の機能を含む、このドキュメントで説明されている機能の多くを実装する Laravel のヘッドレス認証バックエンドです。 Fortify は、Laravel Jetstream の認証バックエンドを提供するか、Laravel で認証する必要がある SPA に認証を提供するために、[Laravel Sanctum](/docs/{{version}}/sanctum) と組み合わせて単独で使用することもできます。

_[Laravel Jetstream](https://jetstream.laravel.com)_ は、[Tailwind CSS](https://tailwindcss.com)、[Livewire](https://laravel-livewire.com)、および/または [Inertia](https://inertiajs.com) を利用した美しくモダンな UI を備えた Laravel Fortify の認証サービスを利用および公開する堅牢なアプリケーション スターター キットです。 Laravel Jetstream には、2 要素認証、チーム サポート、ブラウザ セッション管理、プロファイル管理、および API トークン認証を提供する [Laravel Sanctum](/docs/{{version}}/sanctum) との組み込み統合のオプション サポートが含まれています。 Laravel の API 認証機能については以下で説明します。

<a name="laravels-api-authentication-services"></a>
#### LaravelのAPI認証サービス

Laravel は、API トークンの管理と API トークンを使用して行われたリクエストの認証を支援する 2 つのオプション パッケージ ([Passport](/docs/{{version}}/passport) と [Sanctum](/docs/{{version}}/sanctum)) を提供します。これらのライブラリとLaravelの組み込みCookieベースの認証ライブラリは相互に排他的ではないことに注意してください。これらのライブラリは主に API トークン認証に焦点を当てており、組み込みの認証サービスは Cookie ベースのブラウザ認証に焦点を当てています。多くのアプリケーションは、Laravel の組み込み Cookie ベースの認証サービスと、Laravel の API 認証パッケージの 1 つの両方を使用します。

**Passport**

Passport は OAuth2 認証プロバイダであり、さまざまなタイプのトークンを発行できるさまざまな OAuth2 「許可タイプ」を提供します。一般に、これは API 認証用の堅牢かつ複雑なパッケージです。ただし、ほとんどのアプリケーションは OAuth2 仕様によって提供される複雑な機能を必要としないため、ユーザーと開発者の両方にとって混乱を招く可能性があります。さらに、開発者はこれまで、Passport などの OAuth2 認証プロバイダを使用して SPA アプリケーションやモバイル アプリケーションを認証する方法について混乱してきました。

**Sanctum**

OAuth2 の複雑さと開発者の混乱に応えて、私たちは Web ブラウザーからのファーストパーティ Web リクエストとトークン経由の API リクエストの両方を処理できる、よりシンプルで合理化された認証パッケージの構築に着手しました。この目標は、[Laravel Sanctum](/docs/{{version}}/sanctum) のリリースによって実現されました。これは、API に加えてファーストパーティの Web UI を提供するアプリケーション、またはバックエンドの Laravel アプリケーションとは別に存在するシングルページ アプリケーション (SPA) によって動作するアプリケーション、またはモバイル クライアントを提供するアプリケーションにとって、優先および推奨される認証パッケージと見なされるべきです。

Laravel Sanctum は、アプリケーションの認証プロセス全体を管理できるハイブリッド Web/API 認証パッケージです。これが可能なのは、Sanctum ベースのアプリケーションがリクエストを受信すると、Sanctum が最初にリクエストに認証されたセッションを参照するセッション Cookie が含まれているかどうかを判断するためです。 Sanctum は、前に説明した Laravel の組み込み認証サービスを呼び出すことでこれを実現します。リクエストがセッション Cookie によって認証されていない場合、Sanctum は API トークンのリクエストを検査します。 API トークンが存在する場合、Sanctum はそのトークンを使用してリクエストを認証します。このプロセスの詳細については、Sanctum の [「仕組み」](/docs/{{version}}/sanctum#how-it-works) ドキュメントを参照してください。

Laravel Sanctum は、Web アプリケーションの認証ニーズの大部分に最適であると考えているため、[Laravel Jetstream](https://jetstream.laravel.com) アプリケーション スターター キットに含めることを選択した API パッケージです。

<a name="summary-choosing-your-stack"></a>
#### まとめとスタックの選択

要約すると、アプリケーションがブラウザを使用してアクセスされ、モノリシックな Laravel アプリケーションを構築している場合、アプリケーションは Laravel の組み込み認証サービスを使用します。

次に、アプリケーションがサードパーティによって使用される API を提供する場合は、アプリケーションに API トークン認証を提供するために [Passport](/docs/{{version}}/passport) または [Sanctum](/docs/{{version}}/sanctum) のいずれかを選択します。一般に、Sanctum は、「スコープ」または「能力」のサポートを含め、API 認証、SPA 認証、およびモバイル認証のシンプルで完全なソリューションであるため、可能な限り推奨されます。

Laravel バックエンドを利用するシングルページ アプリケーション (SPA) を構築している場合は、[Laravel Sanctum](/docs/{{version}}/sanctum) を使用する必要があります。 Sanctum を使用する場合は、[独自のバックエンド認証ルートを手動で実装する](#authenticating-users) を実行するか、登録、パスワードリセット、電子メール検証などの機能のルートとコントローラを提供するヘッドレス認証バックエンド サービスとして [Laravel の強化](/docs/{{version}}/fortify) を利用する必要があります。

アプリケーションが OAuth2 仕様で提供されるすべての機能を絶対に必要とする場合は、Passportを選択できます。

また、すぐに始めたい場合は、Laravel の組み込み認証サービスと Laravel Sanctum の推奨認証スタックを既に使用している新しい Laravel アプリケーションを簡単に開始する方法として、[Laravel Breeze](/docs/{{version}}/starter-kits#laravel-breeze) をお勧めします。

<a name="authentication-quickstart"></a>
## 認証クイックスタート (Authentication Quickstart)

> **警告**
> ドキュメントのこの部分では、[Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) を介したユーザーの認証について説明します。これには、すぐに開始できるようにする UI スキャフォールディングが含まれています。 Laravel の認証システムと直接統合したい場合は、[ユーザーを手動で認証する](#authenticating-users) のドキュメントを確認してください。

<a name="install-a-starter-kit"></a>
### スターター キットをインストールする

まず、[Laravelアプリケーションスターターキットをインストールする](/docs/{{version}}/starter-kits) を実行する必要があります。現在のスターター キットである Laravel Breeze と Laravel Jetstream は、新しい Laravel アプリケーションに認証を組み込むための美しく設計された出発点を提供します。

Laravel Breeze は、ログイン、登録、パスワードのリセット、電子メール検証、パスワード確認を含む、Laravel のすべての認証機能を最小限にシンプルに実装したものです。 Laravel Breeze のビューレイヤーは、[Tailwind CSS](/docs/{{version}}/blade) でスタイル設定されたシンプルな [Blade テンプレート](https://tailwindcss.com) で構成されています。 Breeze は、Vue または React を使用した [Inertia](https://inertiajs.com) ベースのスキャフォールディング オプションも提供します。

[Laravel Jetstream](https://jetstream.laravel.com) は、[Livewire](https://laravel-livewire.com) または [Inertiaと Vue](https://inertiajs.com) を使用したアプリケーションのスキャフォールディングのサポートを含む、より堅牢なアプリケーション スターター キットです。さらに、Jetstream は、2 要素認証、チーム、プロファイル管理、ブラウザー セッション管理、[Laravel Sanctum](/docs/{{version}}/sanctum) 経由の API サポート、アカウント削除などのオプション サポートを備えています。

<a name="retrieving-the-authenticated-user"></a>
### 認証されたユーザーの取得

認証スターター キットをインストールし、ユーザーがアプリケーションに登録して認証できるようにした後、多くの場合、現在認証されているユーザーと対話する必要があります。受信リクエストの処理中に、`Auth` ファサードの `user` メソッドを介して認証されたユーザーにアクセスできます。

    use Illuminate\Support\Facades\Auth;

    // Retrieve the currently authenticated user...
    $user = Auth::user();

    // Retrieve the currently authenticated user's ID...
    $id = Auth::id();

あるいは、ユーザーが認証されると、`Illuminate\Http\Request` インスタンス経由で認証されたユーザーにアクセスできます。タイプヒント付きクラスはコントローラのメソッドに自動的に挿入されることに注意してください。 `Illuminate\Http\Request` オブジェクトをタイプヒントすることにより、リクエストの `user` メソッドを介して、アプリケーション内の任意のコントローラ メソッドから認証されたユーザーに簡単にアクセスできるようになります。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;

    class FlightController extends Controller
    {
        /**
         * Update the flight information for an existing flight.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function update(Request $request)
        {
            // $request->user()
        }
    }

<a name="determining-if-the-current-user-is-authenticated"></a>
#### 現在のユーザーが認証されているかどうかを確認する

受信 HTTP リクエストを行っているユーザーが認証されているかどうかを確認するには、`Auth` ファサードで `check` メソッドを使用できます。ユーザーが認証されている場合、このメソッドは `true` を返します。

    use Illuminate\Support\Facades\Auth;

    if (Auth::check()) {
        // The user is logged in...
    }

> **注記**
> `check` メソッドを使用してユーザーが認証されているかどうかを判断することは可能ですが、通常は、ユーザーに特定のルート/コントローラへのアクセスを許可する前に、ミドルウェアを使用してユーザーが認証されていることを確認します。これについて詳しくは、[ルートを保護する](/docs/{{version}}/authentication#protecting-routes) のドキュメントを参照してください。

<a name="protecting-routes"></a>
### ルートを守る

[ルートミドルウェア](/docs/{{version}}/middleware) を使用すると、認証されたユーザーに特定のルートへのアクセスのみを許可できます。 Laravel には、`Illuminate\Auth\Middleware\Authenticate` クラスを参照する `auth` ミドルウェアが付属しています。このミドルウェアはアプリケーションの HTTP カーネルにすでに登録されているため、必要なのはミドルウェアをルート定義にアタッチすることだけです。

    Route::get('/flights', function () {
        // Only authenticated users may access this route...
    })->middleware('auth');

<a name="redirecting-unauthenticated-users"></a>
#### 認証されていないユーザーのリダイレクト

`auth` ミドルウェアは、認証されていないユーザーを検出すると、ユーザーを `login` [名前付きルート](/docs/{{version}}/routing#named-routes) にリダイレクトします。アプリケーションの `app/Http/Middleware/Authenticate.php` ファイル内の `redirectTo` 関数を更新することで、この動作を変更できます。

    /**
     * Get the path the user should be redirected to.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return string
     */
    protected function redirectTo($request)
    {
        return route('login');
    }

<a name="specifying-a-guard"></a>
#### ガードの指定

`auth` ミドルウェアをルートにアタッチする場合、ユーザーの認証にどの「ガード」を使用するかを指定することもできます。指定したガードは、`auth.php` 構成ファイルの `guards` 配列内のキーの 1 つに対応する必要があります。

    Route::get('/flights', function () {
        // Only authenticated users may access this route...
    })->middleware('auth:admin');

<a name="login-throttling"></a>
### ログインスロットル

Laravel Breeze または Laravel Jetstream [スターターキット](/docs/{{version}}/starter-kits) を使用している場合、ログイン試行にレート制限が自動的に適用されます。デフォルトでは、ユーザーは数回試行しても正しい認証情報を入力できなかった場合、1 分間ログインできなくなります。スロットリングは、ユーザーのユーザー名/電子メール アドレスおよび IP アドレスに固有です。

> **注記**
> アプリケーション内の他のルートをレート制限したい場合は、[レート制限に関するドキュメント](/docs/{{version}}/routing#rate-limiting) を確認してください。

<a name="authenticating-users"></a>
## ユーザーを手動で認証する (Manually Authenticating Users)

Laravel の [アプリケーションスターターキット](/docs/{{version}}/starter-kits) に含まれる認証スキャフォールディングを使用する必要はありません。このスキャフォールディングを使用しないことを選択した場合は、Laravel 認証クラスを直接使用してユーザー認証を管理する必要があります。心配しないでください、それは簡単です!

`Auth` [facade](/docs/{{version}}/facades) 経由で Laravel の認証サービスにアクセスするため、クラスの先頭に `Auth` ファサードをインポートする必要があります。次に、`attempt` メソッドを確認してみましょう。 `attempt` メソッドは通常、アプリケーションの「ログイン」フォームからの認証試行を処理するために使用されます。認証が成功した場合は、[セッション固定](/docs/{{version}}/session) を防ぐためにユーザーの [session](https://en.wikipedia.org/wiki/Session_fixation) を再生成する必要があります。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Auth;

    class LoginController extends Controller
    {
        /**
         * Handle an authentication attempt.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function authenticate(Request $request)
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

`attempt` メソッドは、キーと値のペアの配列を最初の引数として受け入れます。配列内の値は、データベース テーブル内でユーザーを検索するために使用されます。したがって、上記の例では、ユーザーは `email` 列の値によって取得されます。ユーザーが見つかった場合、データベースに保存されているハッシュ化されたパスワードが、配列を介してメソッドに渡された `password` 値と比較されます。受信リクエストの `password` 値をハッシュしないでください。フレームワークは、値をデータベース内のハッシュされたパスワードと比較する前に自動的にハッシュするからです。 2 つのハッシュ化されたパスワードが一致する場合、ユーザーの認証されたセッションが開始されます。

Laravel の認証サービスは、認証ガードの「プロバイダ」設定に基づいてデータベースからユーザーを取得することに注意してください。デフォルトの `config/auth.php` 構成ファイルでは、Eloquent ユーザー プロバイダが指定されており、ユーザーを取得するときに `App\Models\User` モデルを使用するように指示されます。アプリケーションのニーズに基づいて、構成ファイル内でこれらの値を変更できます。

認証が成功した場合、`attempt` メソッドは `true` を返します。それ以外の場合は、`false` が返されます。

Laravel のリダイレクターによって提供される `intended` メソッドは、認証ミドルウェアによって傍受される前に、ユーザーがアクセスしようとしていた URL にユーザーをリダイレクトします。意図した宛先が利用できない場合に備えて、このメソッドにフォールバック URI を指定できます。

<a name="specifying-additional-conditions"></a>
#### 追加条件の指定

必要に応じて、ユーザーの電子メールとパスワードに加えて、追加のクエリ条件を認証クエリに追加することもできます。これを実現するには、`attempt` メソッドに渡される配列にクエリ条件を追加するだけです。たとえば、ユーザーが「アクティブ」としてマークされていることを確認できます。

    if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
        // Authentication was successful...
    }

複雑なクエリ条件の場合は、資格情報の配列にクロージャを指定できます。このクロージャはクエリ インスタンスで呼び出され、アプリケーションのニーズに基づいてクエリをカスタマイズできます。

    if (Auth::attempt([
        'email' => $email, 
        'password' => $password, 
        fn ($query) => $query->has('activeSubscription'),
    ])) {
        // Authentication was successful...
    }

> **警告**
> これらの例では、`email` は必須のオプションではなく、単に例として使用されています。データベーステーブルの「ユーザー名」に対応する列名を使用する必要があります。

2 番目の引数としてクロージャを受け取る `attemptWhen` メソッドは、実際にユーザーを認証する前に、潜在的なユーザーのより広範な検査を実行するために使用できます。クロージャーは潜在的なユーザーを受け取り、ユーザーが認証されているかどうかを示す `true` または `false` を返す必要があります。

    if (Auth::attemptWhen([
        'email' => $email,
        'password' => $password,
    ], function ($user) {
        return $user->isNotBanned();
    })) {
        // Authentication was successful...
    }

<a name="accessing-specific-guard-instances"></a>
#### 特定の Guard インスタンスへのアクセス

`Auth` ファサードの `guard` メソッドを使用して、ユーザーの認証時にどのガード インスタンスを使用するかを指定できます。これにより、完全に別個の認証可能なモデルまたはユーザー テーブルを使用して、アプリケーションの別個の部分の認証を管理できます。

`guard` メソッドに渡されるガード名は、`auth.php` 構成ファイルで構成されたガードの 1 つに対応する必要があります。

    if (Auth::guard('admin')->attempt($credentials)) {
        // ...
    }

<a name="remembering-users"></a>
### ユーザーを記憶する

多くの Web アプリケーションには、ログイン フォームに「記憶する」チェックボックスが用意されています。アプリケーションに「記憶する」機能を提供したい場合は、`attempt` メソッドの 2 番目の引数としてブール値を渡すことができます。

この値が `true` の場合、Laravel はユーザーを無期限に、または手動でログアウトするまで認証し続けます。 `users` テーブルには、「remember me」トークンを保存するために使用される文字列 `remember_token` 列が含まれている必要があります。新しい Laravel アプリケーションに含まれる `users` テーブルの移行には、すでに次の列が含まれています。

    use Illuminate\Support\Facades\Auth;

    if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
        // The user is being remembered...
    }

アプリケーションが「remember me」機能を提供する場合、`viaRemember` メソッドを使用して、現在認証されているユーザーが「remember me」Cookie を使用して認証されたかどうかを判断できます。

    use Illuminate\Support\Facades\Auth;

    if (Auth::viaRemember()) {
        // ...
    }

<a name="other-authentication-methods"></a>
### その他の認証方法

<a name="authenticate-a-user-instance"></a>
#### ユーザーインスタンスの認証

既存のユーザー インスタンスを現在認証されているユーザーとして設定する必要がある場合は、そのユーザー インスタンスを `Auth` ファサードの `login` メソッドに渡すことができます。指定されたユーザー インスタンスは、`Illuminate\Contracts\Auth\Authenticatable` [contract](/docs/{{version}}/contracts) の実装である必要があります。 Laravel に含まれる `App\Models\User` モデルはすでにこのインターフェイスを実装しています。この認証方法は、ユーザーがアプリケーションに登録した直後など、有効なユーザー インスタンスがすでにある場合に役立ちます。

    use Illuminate\Support\Facades\Auth;

    Auth::login($user);

`login` メソッドの 2 番目の引数としてブール値を渡すことができます。この値は、認証されたセッションに「記憶する」機能が必要かどうかを示します。これは、セッションが無期限に、またはユーザーがアプリケーションから手動でログアウトするまで認証されることを意味することに注意してください。

    Auth::login($user, $remember = true);

必要に応じて、`login` メソッドを呼び出す前に認証ガードを指定できます。

    Auth::guard('admin')->login($user);

<a name="authenticate-a-user-by-id"></a>
#### IDによるユーザー認証

データベース レコードの主キーを使用してユーザーを認証するには、`loginUsingId` メソッドを使用できます。このメソッドは、認証するユーザーの主キーを受け入れます。

    Auth::loginUsingId(1);

`loginUsingId` メソッドの 2 番目の引数としてブール値を渡すことができます。この値は、認証されたセッションに「記憶する」機能が必要かどうかを示します。これは、セッションが無期限に、またはユーザーがアプリケーションから手動でログアウトするまで認証されることを意味することに注意してください。

    Auth::loginUsingId(1, $remember = true);

<a name="authenticate-a-user-once"></a>
#### ユーザーを一度認証する

`once` メソッドを使用して、単一のリクエストに対してアプリケーションでユーザーを認証できます。このメソッドを呼び出す場合、セッションや Cookie は使用されません。

    if (Auth::once($credentials)) {
        //
    }

<a name="http-basic-authentication"></a>
## HTTP基本認証 (HTTP Basic Authentication)

[HTTP基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication) は、専用の「ログイン」ページを設定せずに、アプリケーションのユーザーを認証する迅速な方法を提供します。まず、`auth.basic` [middleware](/docs/{{version}}/middleware) をルートにアタッチします。 `auth.basic` ミドルウェアは Laravel フレームワークに含まれているため、定義する必要はありません。

    Route::get('/profile', function () {
        // Only authenticated users may access this route...
    })->middleware('auth.basic');

ミドルウェアがルートにアタッチされると、ブラウザでルートにアクセスするときに自動的に資格情報の入力を求められます。デフォルトでは、`auth.basic` ミドルウェアは、`users` データベース テーブルの `email` 列がユーザーの「ユーザー名」であると想定します。

<a name="a-note-on-fastcgi"></a>
#### FastCGI に関する注意事項

PHP FastCGI と Apache を使用して Laravel アプリケーションを提供している場合、HTTP 基本認証が正しく機能しない可能性があります。これらの問題を修正するには、アプリケーションの `.htaccess` ファイルに次の行を追加します。

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```

<a name="stateless-http-basic-authentication"></a>
### ステートレスHTTP基本認証

セッションにユーザー識別子 Cookie を設定せずに、HTTP 基本認証を使用することもできます。これは主に、アプリケーションの API へのリクエストを認証するために HTTP 認証を使用することを選択した場合に役立ちます。これを実現するには、`onceBasic` メソッドを呼び出す [ミドルウェアを定義する](/docs/{{version}}/middleware) 。 `onceBasic` メソッドから応答が返されない場合、リクエストはさらにアプリケーションに渡される可能性があります。

    <?php

    namespace App\Http\Middleware;

    use Illuminate\Support\Facades\Auth;

    class AuthenticateOnceWithBasicAuth
    {
        /**
         * Handle an incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return mixed
         */
        public function handle($request, $next)
        {
            return Auth::onceBasic() ?: $next($request);
        }

    }

次に、[ルートミドルウェアを登録する](/docs/{{version}}/middleware#registering-middleware) をルートにアタッチします。

    Route::get('/api/user', function () {
        // Only authenticated users may access this route...
    })->middleware('auth.basic.once');

<a name="logging-out"></a>
## ログアウトする (Logging Out)

ユーザーをアプリケーションから手動でログアウトするには、`Auth` ファサードによって提供される `logout` メソッドを使用できます。これにより、ユーザーのセッションから認証情報が削除され、後続のリクエストは認証されなくなります。

`logout` メソッドの呼び出しに加えて、ユーザーのセッションを無効にして [CSRFトークン](/docs/{{version}}/csrf) を再生成することをお勧めします。ユーザーをログアウトした後、通常はユーザーをアプリケーションのルートにリダイレクトします。

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Auth;

    /**
     * Log the user out of the application.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function logout(Request $request)
    {
        Auth::logout();

        $request->session()->invalidate();

        $request->session()->regenerateToken();

        return redirect('/');
    }

<a name="invalidating-sessions-on-other-devices"></a>
### 他のデバイスのセッションを無効にする

Laravel は、現在のデバイスのセッションを無効にすることなく、他のデバイスでアクティブなユーザーのセッションを無効にして「ログアウト」するメカニズムも提供します。この機能は通常、ユーザーがパスワードを変更または更新するときに、現在のデバイスの認証を維持しながら他のデバイスのセッションを無効にする場合に使用されます。

開始する前に、セッション認証を受け取る必要があるルートに `Illuminate\Session\Middleware\AuthenticateSession` ミドルウェアが含まれていることを確認する必要があります。通常、このミドルウェアをルート グループ定義に配置して、アプリケーションのルートの大部分に適用できるようにする必要があります。デフォルトでは、`AuthenticateSession` ミドルウェアは、アプリケーションの HTTP カーネルで定義されている `auth.session` ルート ミドルウェア キーを使用してルートに接続できます。

    Route::middleware(['auth', 'auth.session'])->group(function () {
        Route::get('/', function () {
            // ...
        });
    });

その後、`Auth` ファサードによって提供される `logoutOtherDevices` メソッドを使用できます。この方法では、ユーザーは現在のパスワードを確認する必要があり、アプリケーションは入力フォームを通じてこのパスワードを受け入れる必要があります。

    use Illuminate\Support\Facades\Auth;

    Auth::logoutOtherDevices($currentPassword);

`logoutOtherDevices` メソッドが呼び出されると、ユーザーの他のセッションは完全に無効になります。つまり、以前に認証されたすべてのガードから「ログアウト」されます。

<a name="password-confirmation"></a>
## パスワードの確認 (Password Confirmation)

アプリケーションの構築中に、アクションを実行する前、またはユーザーがアプリケーションの機密領域にリダイレクトされる前に、ユーザーにパスワードの確認を要求するアクションが発生する場合があります。 Laravel には、このプロセスを簡単にする組み込みのミドルウェアが含まれています。この機能を実装するには、2 つのルートを定義する必要があります。1 つはユーザーにパスワードの確認を求めるビューを表示するルート、もう 1 つはパスワードが有効であることを確認し、ユーザーを目的の宛先にリダイレクトするルートです。

> **注記**
> 次のドキュメントでは、Laravel のパスワード確認機能と直接統合する方法について説明します。ただし、より迅速に開始したい場合は、[Laravelアプリケーションスターターキット](/docs/{{version}}/starter-kits) にこの機能のサポートが含まれています。

<a name="password-confirmation-configuration"></a>
### 構成

パスワードを確認した後、ユーザーは 3 時間はパスワードの再確認を求められません。ただし、アプリケーションの `config/auth.php` 構成ファイル内の `password_timeout` 構成値の値を変更することで、ユーザーにパスワードの再入力を求めるまでの時間を構成できます。

<a name="password-confirmation-routing"></a>
### ルーティング

<a name="the-password-confirmation-form"></a>
#### パスワード確認フォーム

まず、ユーザーにパスワードの確認を要求するビューを表示するルートを定義します。

    Route::get('/confirm-password', function () {
        return view('auth.confirm-password');
    })->middleware('auth')->name('password.confirm');

ご想像のとおり、このルートによって返されるビューには、`password` フィールドを含むフォームが含まれている必要があります。さらに、ユーザーがアプリケーションの保護された領域に入ろうとしているため、パスワードを確認する必要があることを説明するテキストをビュー内に自由に含めることができます。

<a name="confirming-the-password"></a>
#### パスワードを確認する

次に、「パスワードの確認」ビューからのフォームリクエストを処理するルートを定義します。このルートは、パスワードを検証し、ユーザーを目的の宛先にリダイレクトする役割を果たします。

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

次に進む前に、このルートを詳しく調べてみましょう。まず、リクエストの `password` フィールドが、認証されたユーザーのパスワードと実際に一致するかどうかが判断されます。パスワードが有効な場合は、ユーザーがパスワードを確認したことをLaravelのセッションに通知する必要があります。 `passwordConfirmed` メソッドは、Laravel がユーザーが最後にパスワードを確認した日時を判断するために使用できるタイムスタンプをユーザーのセッションに設定します。最後に、ユーザーを目的の宛先にリダイレクトできます。

<a name="password-confirmation-protecting-routes"></a>
### ルートを守る

最近のパスワードの確認を必要とするアクションを実行するルートには、`password.confirm` ミドルウェアが割り当てられていることを確認する必要があります。このミドルウェアは Laravel のデフォルトのインストールに含まれており、ユーザーがパスワードを確認した後にその場所にリダイレクトされるように、ユーザーの意図した宛先をセッションに自動的に保存します。ユーザーの意図した宛先をセッションに保存した後、ミドルウェアはユーザーを `password.confirm` [名前付きルート](/docs/{{version}}/routing#named-routes) にリダイレクトします。

    Route::get('/settings', function () {
        // ...
    })->middleware(['password.confirm']);

    Route::post('/settings', function () {
        // ...
    })->middleware(['password.confirm']);

<a name="adding-custom-guards"></a>
## カスタムガードの追加 (Adding Custom Guards)

`Auth` ファサードで `extend` メソッドを使用して、独自の認証ガードを定義できます。 `extend` メソッドの呼び出しは [サービスプロバイダ](/docs/{{version}}/providers) 内で行う必要があります。 Laravel にはすでに `AuthServiceProvider` が同梱されているため、コードをそのプロバイダに配置できます。

    <?php

    namespace App\Providers;

    use App\Services\Auth\JwtGuard;
    use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
    use Illuminate\Support\Facades\Auth;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Register any application authentication / authorization services.
         *
         * @return void
         */
        public function boot()
        {
            $this->registerPolicies();

            Auth::extend('jwt', function ($app, $name, array $config) {
                // Return an instance of Illuminate\Contracts\Auth\Guard...

                return new JwtGuard(Auth::createUserProvider($config['provider']));
            });
        }
    }

上の例でわかるように、`extend` メソッドに渡されるコールバックは、`Illuminate\Contracts\Auth\Guard` の実装を返す必要があります。このインターフェイスには、カスタム ガードを定義するために実装する必要があるメソッドがいくつか含まれています。カスタム ガードが定義されたら、`auth.php` 構成ファイルの `guards` 構成でガードを参照できます。

    'guards' => [
        'api' => [
            'driver' => 'jwt',
            'provider' => 'users',
        ],
    ],

<a name="closure-request-guards"></a>
### 閉鎖リクエストガード

カスタムの HTTP リクエスト ベースの認証システムを実装する最も簡単な方法は、`Auth::viaRequest` メソッドを使用することです。このメソッドを使用すると、単一のクロージャを使用して認証プロセスを迅速に定義できます。

まず、`AuthServiceProvider` の `boot` メソッド内で `Auth::viaRequest` メソッドを呼び出します。 `viaRequest` メソッドは、最初の引数として認証ドライバ名を受け入れます。この名前には、カスタム ガードを説明する任意の文字列を指定できます。メソッドに渡される 2 番目の引数は、受信 HTTP リクエストを受け取り、ユーザー インスタンスを返すか、認証が失敗した場合は `null` を返すクロージャである必要があります。

    use App\Models\User;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Auth;

    /**
     * Register any application authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();

        Auth::viaRequest('custom-token', function (Request $request) {
            return User::where('token', (string) $request->token)->first();
        });
    }

カスタム認証ドライバを定義したら、それを `auth.php` 構成ファイルの `guards` 構成内のドライバとして構成できます。

    'guards' => [
        'api' => [
            'driver' => 'custom-token',
        ],
    ],

最後に、認証ミドルウェアをルートに割り当てるときにガードを参照できます。

    Route::middleware('auth:api')->group(function () {
        // ...
    }

<a name="adding-custom-user-providers"></a>
## カスタム ユーザー プロバイダの追加 (Adding Custom User Providers)

ユーザーの保存に従来のリレーショナル データベースを使用していない場合は、独自の認証ユーザー プロバイダを使用して Laravel を拡張する必要があります。 `Auth` ファサードで `provider` メソッドを使用して、カスタム ユーザー プロバイダを定義します。ユーザー プロバイダ リゾルバーは、`Illuminate\Contracts\Auth\UserProvider` の実装を返す必要があります。

    <?php

    namespace App\Providers;

    use App\Extensions\MongoUserProvider;
    use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
    use Illuminate\Support\Facades\Auth;

    class AuthServiceProvider extends ServiceProvider
    {
        /**
         * Register any application authentication / authorization services.
         *
         * @return void
         */
        public function boot()
        {
            $this->registerPolicies();

            Auth::provider('mongo', function ($app, array $config) {
                // Return an instance of Illuminate\Contracts\Auth\UserProvider...

                return new MongoUserProvider($app->make('mongo.connection'));
            });
        }
    }

`provider` メソッドを使用してプロバイダを登録した後、`auth.php` 構成ファイルで新しいユーザー プロバイダに切り替えることができます。まず、新しいドライバを使用する `provider` を定義します。

    'providers' => [
        'users' => [
            'driver' => 'mongo',
        ],
    ],

最後に、`guards` 構成でこのプロバイダを参照できます。

    'guards' => [
        'web' => [
            'driver' => 'session',
            'provider' => 'users',
        ],
    ],

<a name="the-user-provider-contract"></a>
### ユーザープロバイダ契約

`Illuminate\Contracts\Auth\UserProvider` 実装は、MySQL、MongoDB などの永続ストレージ システムから `Illuminate\Contracts\Auth\Authenticatable` 実装をフェッチする役割を果たします。これら 2 つのインターフェイスにより、ユーザー データがどのように保存されているか、または認証されたユーザーを表すためにどのような種類のクラスが使用されているかに関係なく、Laravel 認証メカニズムが機能し続けることができます。

`Illuminate\Contracts\Auth\UserProvider` コントラクトを見てみましょう。

    <?php

    namespace Illuminate\Contracts\Auth;

    interface UserProvider
    {
        public function retrieveById($identifier);
        public function retrieveByToken($identifier, $token);
        public function updateRememberToken(Authenticatable $user, $token);
        public function retrieveByCredentials(array $credentials);
        public function validateCredentials(Authenticatable $user, array $credentials);
    }

`retrieveById` 関数は通常、MySQL データベースからの自動インクリメント ID など、ユーザーを表すキーを受け取ります。 ID に一致する `Authenticatable` 実装がメソッドによって取得され、返される必要があります。

`retrieveByToken` 関数は、一意の `$identifier` および「remember me」`$token` によってユーザーを取得します。通常、`remember_token` などのデータベース列に保存されます。前のメソッドと同様に、一致するトークン値を持つ `Authenticatable` 実装がこのメソッドによって返される必要があります。

`updateRememberToken` メソッドは、`$user` インスタンスの `remember_token` を新しい `$token` で更新します。 「remember me」認証試行が成功したとき、またはユーザーがログアウトしたときに、新しいトークンがユーザーに割り当てられます。

`retrieveByCredentials` メソッドは、アプリケーションで認証を試行するときに、`Auth::attempt` メソッドに渡される資格情報の配列を受け取ります。次に、メソッドは、それらの資格情報と一致するユーザーについて、基礎となる永続ストレージを「クエリ」する必要があります。通常、このメソッドは、`$credentials['username']` の値と一致する「ユーザー名」を持つユーザー レコードを検索する「where」条件を使用してクエリを実行します。このメソッドは、`Authenticatable` の実装を返す必要があります。 **このメソッドでは、パスワードの検証や認証を試行しないでください。**

`validateCredentials` メソッドは、指定された `$user` と `$credentials` を比較してユーザーを認証する必要があります。たとえば、このメソッドは通常、`Hash::check` メソッドを使用して、`$user->getAuthPassword()` の値を `$credentials['password']` の値と比較します。このメソッドは、パスワードが有効かどうかを示す `true` または `false` を返す必要があります。

<a name="the-authenticatable-contract"></a>
### 認証可能な契約

`UserProvider` の各メソッドを調べたので、`Authenticatable` コントラクトを見てみましょう。ユーザープロバイダは、`retrieveById`、`retrieveByToken`、および `retrieveByCredentials` メソッドからこのインターフェイスの実装を返す必要があることに注意してください。

    <?php

    namespace Illuminate\Contracts\Auth;

    interface Authenticatable
    {
        public function getAuthIdentifierName();
        public function getAuthIdentifier();
        public function getAuthPassword();
        public function getRememberToken();
        public function setRememberToken($value);
        public function getRememberTokenName();
    }

このインターフェースはシンプルです。 `getAuthIdentifierName` メソッドはユーザーの「主キー」フィールドの名前を返し、`getAuthIdentifier` メソッドはユーザーの「主キー」を返す必要があります。 MySQL バックエンドを使用する場合、これはユーザー レコードに割り当てられる自動インクリメント主キーとなる可能性があります。 `getAuthPassword` メソッドは、ユーザーのハッシュされたパスワードを返す必要があります。

このインターフェイスにより、使用している ORM またはストレージ抽象化レイヤーに関係なく、認証システムが任意の「ユーザー」クラスで動作できるようになります。デフォルトでは、Laravel には、このインターフェイスを実装する `App\Models\User` クラスが `app/Models` ディレクトリに含まれています。

<a name="events"></a>
## イベント (Events)

Laravel は、認証プロセス中にさまざまな [events](/docs/{{version}}/events) をディスパッチします。 `EventServiceProvider` でこれらのイベントにリスナをアタッチできます。

    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        'Illuminate\Auth\Events\Registered' => [
            'App\Listeners\LogRegisteredUser',
        ],

        'Illuminate\Auth\Events\Attempting' => [
            'App\Listeners\LogAuthenticationAttempt',
        ],

        'Illuminate\Auth\Events\Authenticated' => [
            'App\Listeners\LogAuthenticated',
        ],

        'Illuminate\Auth\Events\Login' => [
            'App\Listeners\LogSuccessfulLogin',
        ],

        'Illuminate\Auth\Events\Failed' => [
            'App\Listeners\LogFailedLogin',
        ],

        'Illuminate\Auth\Events\Validated' => [
            'App\Listeners\LogValidated',
        ],

        'Illuminate\Auth\Events\Verified' => [
            'App\Listeners\LogVerified',
        ],

        'Illuminate\Auth\Events\Logout' => [
            'App\Listeners\LogSuccessfulLogout',
        ],

        'Illuminate\Auth\Events\CurrentDeviceLogout' => [
            'App\Listeners\LogCurrentDeviceLogout',
        ],

        'Illuminate\Auth\Events\OtherDeviceLogout' => [
            'App\Listeners\LogOtherDeviceLogout',
        ],

        'Illuminate\Auth\Events\Lockout' => [
            'App\Listeners\LogLockout',
        ],

        'Illuminate\Auth\Events\PasswordReset' => [
            'App\Listeners\LogPasswordReset',
        ],
    ];

