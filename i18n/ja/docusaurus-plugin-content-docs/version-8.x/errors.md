# エラー処理 (Error Handling)

- [Introduction](#introduction)
- [Configuration](#configuration)
- [例外ハンドラー](#the-exception-handler)
    - [例外の報告](#reporting-exceptions)
    - [タイプ別の例外の無視](#ignoring-exceptions-by-type)
    - [レンダリングの例外](#rendering-exceptions)
    - [報告可能な例外とレンダリング可能な例外](#renderable-exceptions)
    - [タイプ別の例外のマッピング](#mapping-exceptions-by-type)
- [HTTP例外](#http-exceptions)
    - [カスタム HTTP エラー ページ](#custom-http-error-pages)

<a name="introduction"></a>
## 導入 (Introduction)

新しい Laravel プロジェクトを開始すると、エラーと例外の処理がすでに構成されています。 `App\Exceptions\Handler` クラスは、アプリケーションによってスローされたすべての例外がログに記録され、ユーザーに表示される場所です。このドキュメントでは、このクラスについてさらに詳しく説明します。

<a name="configuration"></a>
## 構成 (Configuration)

`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

ローカル開発中は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で値が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="the-exception-handler"></a>
## 例外ハンドラー (The Exception Handler)

<a name="reporting-exceptions"></a>
### 例外の報告

すべての例外は、`App\Exceptions\Handler` クラスによって処理されます。このクラスには、カスタム例外レポートおよびレンダリング コールバックを登録できる `register` メソッドが含まれています。これらの各概念を詳しく見ていきます。例外レポートは、例外をログに記録したり、例外を [Flare](https://flareapp.io)、[Bugsnag](https://bugsnag.com)、[Sentry](https://github.com/getsentry/sentry-laravel) などの外部サービスに送信したりするために使用されます。デフォルトでは、例外は [logging](/docs/{{version}}/logging) 構成に基づいて記録されます。ただし、例外を自由にログに記録することができます。

たとえば、さまざまなタイプの例外をさまざまな方法で報告する必要がある場合は、`reportable` メソッドを使用して、特定のタイプの例外を報告する必要があるときに実行する必要があるクロージャを登録できます。 Laravel は、クロージャのタイプヒントを調べることで、クロージャが報告する例外のタイプを推測します。

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->reportable(function (InvalidOrderException $e) {
            //
        });
    }

`reportable` メソッドを使用してカスタム例外レポート コールバックを登録すると、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。デフォルトのログ スタックへの例外の伝播を停止したい場合は、レポート コールバックを定義するときに `stop` メソッドを使用するか、コールバックから `false` を返します。

    $this->reportable(function (InvalidOrderException $e) {
        //
    })->stop();

    $this->reportable(function (InvalidOrderException $e) {
        return false;
    });

> {tip} 特定の例外の例外レポートをカスタマイズするには、[報告可能な例外](/docs/{{version}}/errors#renderable-exceptions) を利用することもできます。

<a name="global-log-context"></a>
#### グローバルログコンテキスト

利用可能な場合、Laravel は現在のユーザーの ID をコンテキスト データとしてすべての例外のログ メッセージに自動的に追加します。アプリケーションの `App\Exceptions\Handler` クラスの `context` メソッドをオーバーライドすることで、独自のグローバル コンテキスト データを定義できます。この情報は、アプリケーションによって書き込まれるすべての例外のログ メッセージに含まれます。

    /**
     * Get the default context variables for logging.
     *
     * @return array
     */
    protected function context()
    {
        return array_merge(parent::context(), [
            'foo' => 'bar',
        ]);
    }

<a name="exception-log-context"></a>
#### 例外ログのコンテキスト

すべてのログ メッセージにコンテキストを追加すると便利ですが、場合によっては、特定の例外にログに含めたい固有のコンテキストが含まれる場合があります。アプリケーションのカスタム例外の 1 つで `context` メソッドを定義すると、例外のログ エントリに追加する必要がある、その例外に関連するデータを指定できます。

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        // ...

        /**
         * Get the exception's context information.
         *
         * @return array
         */
        public function context()
        {
            return ['order_id' => $this->orderId];
        }
    }

<a name="the-report-helper"></a>
#### `report` ヘルパ

場合によっては、例外を報告しても現在のリクエストの処理を続行する必要がある場合があります。 `report` ヘルパ関数を使用すると、ユーザーにエラー ページを表示せずに、例外ハンドラーを介して例外を迅速に報告できます。

    public function isValid($value)
    {
        try {
            // Validate the value...
        } catch (Throwable $e) {
            report($e);

            return false;
        }
    }

<a name="ignoring-exceptions-by-type"></a>
### タイプ別の例外の無視

アプリケーションを構築するとき、無視して決して報告したくないいくつかの種類の例外が存在します。アプリケーションの例外ハンドラーには、空の配列に初期化される `$dontReport` プロパティが含まれています。このプロパティに追加したクラスは決して報告されません。ただし、カスタム レンダリング ロジックがまだ存在する場合があります。

    use App\Exceptions\InvalidOrderException;

    /**
     * A list of the exception types that should not be reported.
     *
     * @var array
     */
    protected $dontReport = [
        InvalidOrderException::class,
    ];

> {tip} Laravel は舞台裏で、404 HTTP "not found" エラーや無効な CSRF トークンによって生成された 419 HTTP 応答に起因する例外など、一部の種類のエラーをすでに無視しています。

<a name="rendering-exceptions"></a>
### レンダリングの例外

デフォルトでは、Laravel 例外ハンドラーは例外を HTTP 応答に変換します。ただし、特定のタイプの例外に対してカスタム レンダリング クロージャを自由に登録できます。これは、例外ハンドラーの `renderable` メソッドを介して実行できます。

`renderable` メソッドに渡されるクロージャは、`response` ヘルパを介して生成できる `Illuminate\Http\Response` のインスタンスを返す必要があります。 Laravel は、クロージャのタイプヒントを調べることで、クロージャがレンダリングする例外のタイプを推測します。

    use App\Exceptions\InvalidOrderException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (InvalidOrderException $e, $request) {
            return response()->view('errors.invalid-order', [], 500);
        });
    }

`renderable` メソッドを使用して、組み込み Laravel または Symfony 例外 (`NotFoundHttpException` など) のレンダリング動作をオーバーライドすることもできます。 `renderable` メソッドに指定されたクロージャが値を返さない場合、Laravel のデフォルトの例外レンダリングが利用されます。

    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Record not found.'
                ], 404);
            }
        });
    }

<a name="renderable-exceptions"></a>
### 報告可能な例外とレンダリング可能な例外

例外ハンドラーの `register` メソッドで例外の型をチェックする代わりに、カスタム例外に `report` メソッドと `render` メソッドを直接定義できます。これらのメソッドが存在する場合、フレームワークによって自動的に呼び出されます。

    <?php

    namespace App\Exceptions;

    use Exception;

    class InvalidOrderException extends Exception
    {
        /**
         * Report the exception.
         *
         * @return bool|null
         */
        public function report()
        {
            //
        }

        /**
         * Render the exception into an HTTP response.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function render($request)
        {
            return response(...);
        }
    }

組み込みの Laravel 例外や Symfony 例外など、すでにレンダリング可能な例外を例外が拡張する場合、例外の `render` メソッドから `false` を返して、例外のデフォルトの HTTP 応答をレンダリングできます。

    /**
     * Render the exception into an HTTP response.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function render($request)
    {
        // Determine if the exception needs custom rendering...

        return false;
    }

例外に、特定の条件が満たされた場合にのみ必要なカスタムレポートロジックが含まれている場合は、デフォルトの例外処理設定を使用して例外をレポートするように Laravel に指示する必要がある場合があります。これを実現するには、例外の `report` メソッドから `false` を返すことができます。

    /**
     * Report the exception.
     *
     * @return bool|null
     */
    public function report()
    {
        // Determine if the exception needs custom reporting...

        return false;
    }

> {tip} `report` メソッドの必要な依存関係をタイプヒントで指定すると、Laravel の [サービスコンテナ](/docs/{{version}}/container) によって自動的にメソッドに挿入されます。

<a name="mapping-exceptions-by-type"></a>
### タイプ別の例外のマッピング

場合によっては、アプリケーションで使用されるサードパーティ ライブラリが、[renderable](#renderable-exceptions) を実行したい例外をスローすることがありますが、サードパーティ例外の定義を制御できないため、実行できないことがあります。

ありがたいことに、Laravel では、これらの例外をアプリケーション内で管理する他の例外タイプに簡単にマップできます。これを実現するには、例外ハンドラーの `register` メソッドから `map` メソッドを呼び出します。

    use League\Flysystem\Exception;
    use App\Exceptions\FilesystemException;

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->map(Exception::class, FilesystemException::class);
    }

ターゲット例外の作成をより詳細に制御したい場合は、`map` メソッドにクロージャを渡すことができます。

    use League\Flysystem\Exception;
    use App\Exceptions\FilesystemException;

    $this->map(fn (Exception $e) => new FilesystemException($e));

<a name="http-exceptions"></a>
## HTTP例外 (HTTP Exceptions)

一部の例外は、サーバーからの HTTP エラー コードを示します。たとえば、これは「ページが見つかりません」エラー (404)、「不正エラー」(401)、または開発者が生成した 500 エラーである可能性があります。アプリケーション内の任意の場所からこのような応答を生成するには、`abort` ヘルパを使用できます。

    abort(404);

<a name="custom-http-error-pages"></a>
### カスタム HTTP エラー ページ

Laravel を使用すると、さまざまな HTTP ステータス コードのカスタム エラー ページを簡単に表示できます。たとえば、404 HTTP ステータス コードのエラー ページをカスタマイズする場合は、`resources/views/errors/404.blade.php` ビュー テンプレートを作成します。このビューは、アプリケーションによって生成されたすべての 404 エラーに対してレンダリングされます。このディレクトリ内のビューには、対応する HTTP ステータス コードと一致する名前を付ける必要があります。 `abort` 関数によって生成された `Symfony\Component\HttpKernel\Exception\HttpException` インスタンスは、`$exception` 変数としてビューに渡されます。

    <h2>{{ $exception->getMessage() }}</h2>

`vendor:publish` Artisan コマンドを使用して、Laravel のデフォルトのエラー ページ テンプレートを公開できます。テンプレートが公開されたら、好みに合わせてカスタマイズできます。

    php artisan vendor:publish --tag=laravel-errors

