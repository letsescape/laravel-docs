# HTTP 応答 (HTTP Responses)

- [応答の作成](#creating-responses)
    - [応答にヘッダーを添付する](#attaching-headers-to-responses)
    - [応答に Cookie を添付する](#attaching-cookies-to-responses)
    - [Cookie と暗号化](#cookies-and-encryption)
- [Redirects](#redirects)
    - [名前付きルートへのリダイレクト](#redirecting-named-routes)
    - [コントローラアクションへのリダイレクト](#redirecting-controller-actions)
    - [外部ドメインへのリダイレクト](#redirecting-external-domains)
    - [フラッシュされたセッション データによるリダイレクト](#redirecting-with-flashed-session-data)
- [他の応答タイプ](#other-response-types)
    - [回答を見る](#view-responses)
    - [JSON 応答](#json-responses)
    - [ファイルのダウンロード](#file-downloads)
    - [ファイル応答](#file-responses)
- [応答マクロ](#response-macros)

<a name="creating-responses"></a>
## 応答の作成 (Creating Responses)

<a name="strings-arrays"></a>
#### 文字列と配列

すべてのルートとコントローラは、ユーザーのブラウザーに送り返される応答を返す必要があります。 Laravel は、応答を返すためのいくつかの異なる方法を提供します。最も基本的な応答は、ルートまたはコントローラから文字列を返すことです。フレームワークは、文字列を完全な HTTP 応答に自動的に変換します。

    Route::get('/', function () {
        return 'Hello World';
    });

ルートやコントローラから文字列を返すだけでなく、配列を返すこともできます。フレームワークは配列を JSON 応答に自動的に変換します。

    Route::get('/', function () {
        return [1, 2, 3];
    });

> [!NOTE]  
> ルートまたはコントローラから [Eloquent コレクション](/docs/{{version}}/eloquent-collections) を返すこともできることをご存知ですか?これらは自動的に JSON に変換されます。試してみてください!

<a name="response-objects"></a>
#### 応答オブジェクト

通常、ルート アクションから単純な文字列や配列を返すだけではありません。代わりに、完全な `Illuminate\Http\Response` インスタンスまたは [views](/docs/{{version}}/views) を返します。

完全な `Response` インスタンスを返すと、応答の HTTP ステータス コードとヘッダーをカスタマイズできます。 `Response` インスタンスは、HTTP 応答を構築するためのさまざまなメソッドを提供する `Symfony\Component\HttpFoundation\Response` クラスを継承します。

    Route::get('/home', function () {
        return response('Hello World', 200)
                      ->header('Content-Type', 'text/plain');
    });

<a name="eloquent-models-and-collections"></a>
#### Eloquent モデルとコレクション

[Eloquent ORM](/docs/{{version}}/eloquent) モデルとコレクションをルートとコントローラから直接返すこともできます。これを行うと、Laravel はモデルの [隠し属性](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) を尊重しながら、モデルとコレクションを JSON 応答に自動的に変換します。

    use App\Models\User;

    Route::get('/user/{user}', function (User $user) {
        return $user;
    });

<a name="attaching-headers-to-responses"></a>
### 応答にヘッダーを添付する

ほとんどの応答メソッドはチェーン可能であり、応答インスタンスをスムーズに構築できることに留意してください。たとえば、`header` メソッドを使用して、応答をユーザーに送り返す前に一連のヘッダーを応答に追加できます。

    return response($content)
                ->header('Content-Type', $type)
                ->header('X-Header-One', 'Header Value')
                ->header('X-Header-Two', 'Header Value');

または、`withHeaders` メソッドを使用して、応答に追加するヘッダーの配列を指定することもできます。

    return response($content)
                ->withHeaders([
                    'Content-Type' => $type,
                    'X-Header-One' => 'Header Value',
                    'X-Header-Two' => 'Header Value',
                ]);

<a name="cache-control-middleware"></a>
#### キャッシュ制御ミドルウェア

Laravel には `cache.headers` ミドルウェアが含まれており、ルートのグループに `Cache-Control` ヘッダーをすばやく設定するために使用できます。ディレクティブは、対応するキャッシュ制御ディレクティブと同等の「スネーク ケース」を使用して指定する必要があり、セミコロンで区切る必要があります。ディレクティブのリストで `etag` が指定されている場合、応答コンテンツの MD5 ハッシュが ETag 識別子として自動的に設定されます。

    Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
        Route::get('/privacy', function () {
            // ...
        });

        Route::get('/terms', function () {
            // ...
        });
    });

<a name="attaching-cookies-to-responses"></a>
### 応答に Cookie を添付する

`cookie` メソッドを使用して、発信 `Illuminate\Http\Response` インスタンスに Cookie を添付できます。名前、値、Cookie が有効であるとみなされる分数をこのメソッドに渡す必要があります。

    return response('Hello World')->cookie(
        'name', 'value', $minutes
    );

`cookie` メソッドは、使用頻度は低いですが、さらにいくつかの引数も受け入れます。一般に、これらの引数は、PHP のネイティブ [setcookie](https://secure.php.net/manual/en/function.setcookie.php) メソッドに与えられる引数と同じ目的と意味を持ちます。

    return response('Hello World')->cookie(
        'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
    );

発信応答とともに Cookie が送信されるようにしたいが、その応答のインスタンスがまだない場合は、`Cookie` ファサードを使用して、送信時に応答に添付する Cookie を「キュー」に入れることができます。 `queue` メソッドは、Cookie インスタンスの作成に必要な引数を受け取ります。これらの Cookie は、送信応答がブラウザーに送信される前に添付されます。

    use Illuminate\Support\Facades\Cookie;

    Cookie::queue('name', 'value', $minutes);

<a name="generating-cookie-instances"></a>
#### Cookie インスタンスの生成

後で応答インスタンスにアタッチできる `Symfony\Component\HttpFoundation\Cookie` インスタンスを生成したい場合は、グローバル `cookie` ヘルパを使用できます。この Cookie は、応答インスタンスに添付されない限り、クライアントに送り返されません。

    $cookie = cookie('name', 'value', $minutes);

    return response('Hello World')->cookie($cookie);

<a name="expiring-cookies-early"></a>
#### Cookie の期限切れを早める

発信応答の `withoutCookie` メソッドを使用して Cookie を期限切れにすることで、Cookie を削除できます。

    return response('Hello World')->withoutCookie('name');

発信応答のインスタンスをまだ持っていない場合は、`Cookie` ファサードの `expire` メソッドを使用して Cookie を期限切れにすることができます。

    Cookie::expire('name');

<a name="cookies-and-encryption"></a>
### Cookie と暗号化

デフォルトでは、Laravel によって生成されるすべての Cookie は暗号化および署名されるため、クライアントによる変更や読み取りはできません。アプリケーションによって生成された Cookie のサブセットの暗号化を無効にしたい場合は、`app/Http/Middleware` ディレクトリにある `App\Http\Middleware\EncryptCookies` ミドルウェアの `$except` プロパティを使用できます。

    /**
     * The names of the cookies that should not be encrypted.
     *
     * @var array
     */
    protected $except = [
        'cookie_name',
    ];

<a name="redirects"></a>
## リダイレクト (Redirects)

リダイレクト応答は `Illuminate\Http\RedirectResponse` クラスのインスタンスであり、ユーザーを別の URL にリダイレクトするために必要な適切なヘッダーが含まれています。 `RedirectResponse` インスタンスを生成するには、いくつかの方法があります。最も簡単な方法は、グローバル `redirect` ヘルパを使用することです。

    Route::get('/dashboard', function () {
        return redirect('home/dashboard');
    });

送信されたフォームが無効な場合など、ユーザーを以前の場所にリダイレクトしたい場合があります。これを行うには、グローバル `back` ヘルパ関数を使用します。この機能は [session](/docs/{{version}}/session) を利用するため、`back` 関数を呼び出すルートが `web` ミドルウェア グループを使用していることを確認してください。

    Route::post('/user/profile', function () {
        // Validate the request...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
### 名前付きルートへのリダイレクト

パラメーターを指定せずに `redirect` ヘルパを呼び出すと、`Illuminate\Routing\Redirector` のインスタンスが返され、`Redirector` インスタンスの任意のメソッドを呼び出すことができます。たとえば、名前付きルートに `RedirectResponse` を生成するには、`route` メソッドを使用できます。

    return redirect()->route('login');

ルートにパラメーターがある場合は、それらを `route` メソッドの 2 番目の引数として渡すことができます。

    // For a route with the following URI: /profile/{id}

    return redirect()->route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent モデルを介したパラメーターの入力

Eloquent モデルから設定されている「ID」パラメータを持つルートにリダイレクトしている場合は、モデル自体を渡すことができます。 ID は自動的に抽出されます。

    // For a route with the following URI: /profile/{id}

    return redirect()->route('profile', [$user]);

ルート パラメーターに配置される値をカスタマイズしたい場合は、ルート パラメーター定義 (`/profile/{id:slug}`) で列を指定するか、Eloquent モデルの `getRouteKey` メソッドをオーバーライドできます。

    /**
     * Get the value of the model's route key.
     */
    public function getRouteKey(): mixed
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
### コントローラアクションへのリダイレクト

[コントローラのアクション](/docs/{{version}}/controllers) へのリダイレクトを生成することもできます。これを行うには、コントローラとアクション名を `action` メソッドに渡します。

    use App\Http\Controllers\UserController;

    return redirect()->action([UserController::class, 'index']);

コントローラ ルートにパラメーターが必要な場合は、それらを `action` メソッドの 2 番目の引数として渡すことができます。

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-external-domains"></a>
### 外部ドメインへのリダイレクト

場合によっては、アプリケーションの外部のドメインにリダイレクトする必要があるかもしれません。これを行うには、`away` メソッドを呼び出して、追加の URL エンコード、検証、または検証を行わずに `RedirectResponse` を作成します。

    return redirect()->away('https://www.google.com');

<a name="redirecting-with-flashed-session-data"></a>
### フラッシュされたセッション データによるリダイレクト

通常、新しい URL へのリダイレクトと [セッションにデータをフラッシュする](/docs/{{version}}/session#flash-data) は同時に行われます。通常、これはアクションが正常に実行された後で、成功メッセージをセッションにフラッシュするときに行われます。便宜上、`RedirectResponse` インスタンスを作成し、単一の滑らかなメソッド チェーンでセッションにデータをフラッシュすることができます。

    Route::post('/user/profile', function () {
        // ...

        return redirect('dashboard')->with('status', 'Profile updated!');
    });

ユーザーがリダイレクトされた後、[session](/docs/{{version}}/session) からフラッシュされたメッセージを表示できます。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

<a name="redirecting-with-input"></a>
#### 入力によるリダイレクト

`RedirectResponse` インスタンスによって提供される `withInput` メソッドを使用して、ユーザーを新しい場所にリダイレクトする前に、現在のリクエストの入力データをセッションにフラッシュできます。これは通常、ユーザーが検証エラーに遭遇した場合に行われます。入力がセッションにフラッシュされると、次のリクエスト中に [それを取得します](/docs/{{version}}/requests#retrieving-old-input) を実行してフォームに再入力することが簡単にできます。

    return back()->withInput();

<a name="other-response-types"></a>
## 他の応答タイプ (Other Response Types)

`response` ヘルパは、他のタイプの応答インスタンスを生成するために使用できます。 `response` ヘルパが引数なしで呼び出されると、`Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/{{version}}/contracts) の実装が返されます。この規約は、応答を生成するためのいくつかの便利な方法を提供します。

<a name="view-responses"></a>
### 回答を見る

応答のステータスとヘッダーを制御する必要があるが、応答のコンテンツとして [view](/docs/{{version}}/views) を返す必要がある場合は、`view` メソッドを使用する必要があります。

    return response()
                ->view('hello', $data, 200)
                ->header('Content-Type', $type);

もちろん、カスタム HTTP ステータス コードやカスタム ヘッダーを渡す必要がない場合は、グローバル `view` ヘルパ関数を使用できます。

<a name="json-responses"></a>
### JSON 応答

`json` メソッドは、`Content-Type` ヘッダーを `application/json` に自動的に設定し、`json_encode` PHP 関数を使用して指定された配列を JSON に変換します。

    return response()->json([
        'name' => 'Abigail',
        'state' => 'CA',
    ]);

JSONP 応答を作成したい場合は、`json` メソッドを `withCallback` メソッドと組み合わせて使用​​できます。

    return response()
                ->json(['name' => 'Abigail', 'state' => 'CA'])
                ->withCallback($request->input('callback'));

<a name="file-downloads"></a>
### ファイルのダウンロード

`download` メソッドは、ユーザーのブラウザに指定されたパスにファイルをダウンロードさせる応答を生成するために使用できます。 `download` メソッドは、メソッドの 2 番目の引数としてファイル名を受け入れます。これにより、ファイルをダウンロードするユーザーに表示されるファイル名が決まります。最後に、HTTP ヘッダーの配列を 3 番目の引数としてメソッドに渡すことができます。

    return response()->download($pathToFile);

    return response()->download($pathToFile, $name, $headers);

> [!WARNING]  
> ファイルのダウンロードを管理する Symfony HttpFoundation では、ダウンロードされるファイルに ASCII ファイル名が付いている必要があります。

<a name="streamed-downloads"></a>
#### ストリーミングダウンロード

場合によっては、操作の内容をディスクに書き込むことなく、特定の操作の文字列応答をダウンロード可能な応答に変換したい場合があります。このシナリオでは、`streamDownload` メソッドを使用できます。このメソッドは、コールバック、ファイル名、およびオプションのヘッダー配列を引数として受け取ります。

    use App\Services\GitHub;

    return response()->streamDownload(function () {
        echo GitHub::api('repo')
                    ->contents()
                    ->readme('laravel', 'laravel')['contents'];
    }, 'laravel-readme.md');

<a name="file-responses"></a>
### ファイル応答

`file` メソッドは、ダウンロードを開始する代わりに、画像や PDF などのファイルをユーザーのブラウザーに直接表示するために使用できます。このメソッドは、ファイルへの絶対パスを最初の引数として受け入れ、ヘッダーの配列を 2 番目の引数として受け入れます。

    return response()->file($pathToFile);

    return response()->file($pathToFile, $headers);

<a name="response-macros"></a>
## 応答マクロ (Response Macros)

さまざまなルートやコントローラで再利用できるカスタム応答を定義したい場合は、`Response` ファサードで `macro` メソッドを使用できます。通常、このメソッドは、アプリケーションの [サービスプロバイダ](/docs/{{version}}/providers) の 1 つ (`App\Providers\AppServiceProvider` サービスプロバイダなど) の `boot` メソッドから呼び出す必要があります。

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Response;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         */
        public function boot(): void
        {
            Response::macro('caps', function (string $value) {
                return Response::make(strtoupper($value));
            });
        }
    }

`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャーは、`ResponseFactory` 実装または `response` ヘルパからマクロ名を呼び出すときに実行されます。

    return response()->caps('foo');

