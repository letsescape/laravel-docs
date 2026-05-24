# URLの生成 (URL Generation)

- [Introduction](#introduction)
- [基本](#the-basics)
    - [URLの生成](#generating-urls)
    - [現在の URL にアクセスする](#accessing-the-current-url)
- [名前付きルートの URL](#urls-for-named-routes)
    - [署名付き URL](#signed-urls)
- [コントローラアクションの URL](#urls-for-controller-actions)
- [デフォルト値](#default-values)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、アプリケーションの URL の生成を支援するいくつかのヘルパが用意されています。これらのヘルパは主に、テンプレートや API 応答にリンクを構築するとき、またはアプリケーションの別の部分へのリダイレクト応答を生成するときに役立ちます。

<a name="the-basics"></a>
## 基本 (The Basics)

<a name="generating-urls"></a>
### URLの生成

`url` ヘルパは、アプリケーションの任意の URL を生成するために使用できます。生成された URL は、アプリケーションによって処理されている現在のリクエストのスキーム (HTTP または HTTPS) とホストを自動的に使用します。

    $post = App\Models\Post::find(1);

    echo url("/posts/{$post->id}");

    // http://example.com/posts/1

<a name="accessing-the-current-url"></a>
### 現在の URL にアクセスする

`url` ヘルパにパスが指定されていない場合は、`Illuminate\Routing\UrlGenerator` インスタンスが返され、現在の URL に関する情報にアクセスできるようになります。

    // Get the current URL without the query string...
    echo url()->current();

    // Get the current URL including the query string...
    echo url()->full();

    // Get the full URL for the previous request...
    echo url()->previous();

これらの各メソッドには、`URL` [facade](/docs/{{version}}/facades) 経由でもアクセスできます。

    use Illuminate\Support\Facades\URL;

    echo URL::current();

<a name="urls-for-named-routes"></a>
## 名前付きルートの URL (URLs For Named Routes)

`route` ヘルパを使用して、[名前付きルート](/docs/{{version}}/routing#named-routes) への URL を生成できます。名前付きルートを使用すると、ルート上で定義された実際の URL に結合せずに URL を生成できます。したがって、ルートの URL が変更された場合、`route` 関数の呼び出しを変更する必要はありません。たとえば、アプリケーションに次のように定義されたルートが含まれていると想像してください。

    Route::get('/post/{post}', function (Post $post) {
        //
    })->name('post.show');

このルートへの URL を生成するには、次のように `route` ヘルパを使用します。

    echo route('post.show', ['post' => 1]);

    // http://example.com/post/1

もちろん、`route` ヘルパを使用して、複数のパラメータを持つルートの URL を生成することもできます。

    Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
        //
    })->name('comment.show');

    echo route('comment.show', ['post' => 1, 'comment' => 3]);

    // http://example.com/post/1/comment/3

ルートの定義パラメーターに対応しない追加の配列要素は、URL のクエリ文字列に追加されます。

    echo route('post.show', ['post' => 1, 'search' => 'rocket']);

    // http://example.com/post/1?search=rocket

<a name="eloquent-models"></a>
#### Eloquent モデル

多くの場合、[Eloquent モデル](/docs/{{version}}/eloquent) のルート キー (通常は主キー) を使用して URL を生成します。このため、Eloquent モデルをパラメーター値として渡すことができます。 `route` ヘルパは、モデルのルート キーを自動的に抽出します。

    echo route('post.show', ['post' => $post]);

<a name="signed-urls"></a>
### 署名付き URL

Laravel を使用すると、名前付きルートへの「署名付き」URL を簡単に作成できます。これらの URL にはクエリ文字列に「署名」ハッシュが追加されており、これにより Laravel は URL が作成されてから変更されていないことを確認できます。署名付き URL は、公的にアクセス可能でありながら、URL 操作に対する保護層が必要なルートに特に役立ちます。

たとえば、署名付き URL を使用して、顧客に電子メールで送信される公開「購読解除」リンクを実装できます。名前付きルートへの署名付き URL を作成するには、`URL` ファサードの `signedRoute` メソッドを使用します。

    use Illuminate\Support\Facades\URL;

    return URL::signedRoute('unsubscribe', ['user' => 1]);

指定した時間が経過すると期限切れになる一時的な署名付きルート URL を生成したい場合は、`temporarySignedRoute` メソッドを使用できます。 Laravel は、一時的な署名付きルート URL を検証するときに、署名付き URL にエンコードされている有効期限タイムスタンプが経過していないことを確認します。

    use Illuminate\Support\Facades\URL;

    return URL::temporarySignedRoute(
        'unsubscribe', now()->addMinutes(30), ['user' => 1]
    );

<a name="validating-signed-route-requests"></a>
#### 署名されたルートリクエストの検証

受信リクエストに有効な署名があることを確認するには、受信 `Request` で `hasValidSignature` メソッドを呼び出す必要があります。

    use Illuminate\Http\Request;

    Route::get('/unsubscribe/{user}', function (Request $request) {
        if (! $request->hasValidSignature()) {
            abort(401);
        }

        // ...
    })->name('unsubscribe');

あるいは、`Illuminate\Routing\Middleware\ValidateSignature` [middleware](/docs/{{version}}/middleware) をルートに割り当てることもできます。まだ存在していない場合は、このミドルウェアに HTTP カーネルの `routeMiddleware` 配列内のキーを割り当てる必要があります。

    /**
     * The application's route middleware.
     *
     * These middleware may be assigned to groups or used individually.
     *
     * @var array
     */
    protected $routeMiddleware = [
        'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
    ];

カーネルにミドルウェアを登録したら、それをルートに接続できます。受信リクエストに有効な署名がない場合、ミドルウェアは自動的に `403` HTTP レスポンスを返します。

    Route::post('/unsubscribe/{user}', function (Request $request) {
        // ...
    })->name('unsubscribe')->middleware('signed');

<a name="responding-to-invalid-signed-routes"></a>
#### 無効な署名付きルートへの対応

有効期限が切れた署名付き URL にアクセスすると、`403` HTTP ステータス コードの一般的なエラー ページが表示されます。ただし、例外ハンドラーで `InvalidSignatureException` 例外のカスタム「レンダリング可能な」クロージャーを定義することで、この動作をカスタマイズできます。このクロージャは HTTP 応答を返す必要があります。

    use Illuminate\Routing\Exceptions\InvalidSignatureException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (InvalidSignatureException $e) {
            return response()->view('error.link-expired', [], 403);
        });
    }

<a name="urls-for-controller-actions"></a>
## コントローラアクションの URL (URLs For Controller Actions)

`action` 関数は、指定されたコントローラ アクションの URL を生成します。

    use App\Http\Controllers\HomeController;

    $url = action([HomeController::class, 'index']);

コントローラ メソッドがルート パラメーターを受け入れる場合、ルート パラメーターの連想配列を 2 番目の引数として関数に渡すことができます。

    $url = action([UserController::class, 'profile'], ['id' => 1]);

<a name="default-values"></a>
## デフォルト値 (Default Values)

一部のアプリケーションでは、特定の URL パラメータに対してリクエスト全体のデフォルト値を指定することが必要な場合があります。たとえば、多くのルートで `{locale}` パラメータが定義されていると想像してください。

    Route::get('/{locale}/posts', function () {
        //
    })->name('post.index');

`route` ヘルパを呼び出すたびに、常に `locale` を渡すのは面倒です。したがって、`URL::defaults` メソッドを使用して、現在のリクエスト中に常に適用されるこのパラメータのデフォルト値を定義できます。現在のリクエストにアクセスできるように、[ルートミドルウェア](/docs/{{version}}/middleware#assigning-middleware-to-routes) からこのメソッドを呼び出すこともできます。

    <?php

    namespace App\Http\Middleware;

    use Closure;
    use Illuminate\Support\Facades\URL;

    class SetDefaultLocaleForUrls
    {
        /**
         * Handle the incoming request.
         *
         * @param  \Illuminate\Http\Request  $request
         * @param  \Closure  $next
         * @return \Illuminate\Http\Response
         */
        public function handle($request, Closure $next)
        {
            URL::defaults(['locale' => $request->user()->locale]);

            return $next($request);
        }
    }

`locale` パラメータのデフォルト値を設定すると、`route` ヘルパを介して URL を生成するときにその値を渡す必要はなくなります。

<a name="url-defaults-middleware-priority"></a>
#### URLのデフォルトとミドルウェアの優先順位

URL のデフォルト値を設定すると、Laravel による暗黙的なモデルバインディングの処理が妨げられる可能性があります。したがって、URL のデフォルトを設定する [ミドルウェアに優先順位を付ける](/docs/{{version}}/middleware#sorting-middleware) は、Laravel 独自の `SubstituteBindings` ミドルウェアよりも前に実行する必要があります。これを実現するには、アプリケーションの HTTP カーネルの `$middlewarePriority` プロパティ内で、ミドルウェアが `SubstituteBindings` ミドルウェアよりも前に存在するようにします。

`$middlewarePriority` プロパティは、基本 `Illuminate\Foundation\Http\Kernel` クラスで定義されます。変更するには、そのクラスからその定義をコピーし、アプリケーションの HTTP カーネルで上書きします。

    /**
     * The priority-sorted list of middleware.
     *
     * This forces non-global middleware to always be in the given order.
     *
     * @var array
     */
    protected $middlewarePriority = [
        // ...
         \App\Http\Middleware\SetDefaultLocaleForUrls::class,
         \Illuminate\Routing\Middleware\SubstituteBindings::class,
         // ...
    ];

