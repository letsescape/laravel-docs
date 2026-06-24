<!-- # Error Handling -->
# Error Handling

- [Introduction](#introduction)
- [Configuration](#configuration)
- [The Exception Handler](#the-exception-handler)
    - [Reporting Exceptions](#reporting-exceptions)
    - [Ignoring Exceptions By Type](#ignoring-exceptions-by-type)
    - [Rendering Exceptions](#rendering-exceptions)
    - [Reportable & Renderable Exceptions](#renderable-exceptions)
    - [Mapping Exceptions By Type](#mapping-exceptions-by-type)
- [HTTP Exceptions](#http-exceptions)
    - [Custom HTTP Error Pages](#custom-http-error-pages)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you start a new Laravel project, error and exception handling is already configured for you. The `App\Exceptions\Handler` class is where all exceptions thrown by your application are logged and then rendered to the user. We'll dive deeper into this class throughout this documentation. -->
新しい Laravel プロジェクトを開始すると、エラーと例外の処理がすでに構成されています。 `App\Exceptions\Handler` クラスは、アプリケーションによってスローされたすべての例外がログに記録され、ユーザーに表示される場所です。このドキュメントでは、このクラスについてさらに詳しく説明します。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

<!-- During local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the value is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
ローカル開発中は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で値が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="the-exception-handler"></a>
<!-- ## The Exception Handler -->
## The Exception Handler

<a name="reporting-exceptions"></a>
<!-- ### Reporting Exceptions -->
### Reporting Exceptions

<!-- All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com) or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/8.x/logging) configuration. However, you are free to log exceptions however you wish. -->
すべての例外は、`App\Exceptions\Handler` クラスによって処理されます。このクラスには、カスタム例外レポートおよびレンダリング コールバックを登録できる `register` メソッドが含まれています。これらの各概念を詳しく見ていきます。例外レポートは、例外をログに記録したり、例外を [Flare](https://flareapp.io)、[Bugsnag](https://bugsnag.com)、[Sentry](https://github.com/getsentry/sentry-laravel) などの外部サービスに送信したりするために使用されます。デフォルトでは、例外は [logging](/docs/8.x/logging) 構成に基づいて記録されます。ただし、例外を自由にログに記録することができます。

<!-- For example, if you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will deduce what type of exception the closure reports by examining the type-hint of the closure: -->
たとえば、さまざまなタイプの例外をさまざまな方法で報告する必要がある場合は、`reportable` メソッドを使用して、特定のタイプの例外を報告する必要があるときに実行する必要があるクロージャを登録できます。 Laravel は、クロージャのタイプヒントを調べることで、クロージャが報告する例外のタイプを推測します。

```
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
```

<!-- When you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback: -->
`reportable` メソッドを使用してカスタム例外レポート コールバックを登録すると、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。デフォルトのログ スタックへの例外の伝播を停止したい場合は、レポート コールバックを定義するときに `stop` メソッドを使用するか、コールバックから `false` を返します。

```
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!TIP]
> 特定の例外の例外レポートをカスタマイズするには、[reportable exceptions](/docs/8.x/errors#renderable-exceptions) を利用することもできます。

<a name="global-log-context"></a>
<!-- #### Global Log Context -->
#### Global Log Context

<!-- If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by overriding the `context` method of your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application: -->
利用可能な場合、Laravel は現在のユーザーの ID をコンテキスト データとしてすべての例外のログ メッセージに自動的に追加します。アプリケーションの `App\Exceptions\Handler` クラスの `context` メソッドをオーバーライドすることで、独自のグローバル コンテキスト データを定義できます。この情報は、アプリケーションによって書き込まれるすべての例外のログ メッセージに含まれます。

```
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
```

<a name="exception-log-context"></a>
<!-- #### Exception Log Context -->
#### Exception Log Context

<!-- While adding context to every log message can be useful, sometimes a particular exception may have unique context that you would like to include in your logs. By defining a `context` method on one of your application's custom exceptions, you may specify any data relevant to that exception that should be added to the exception's log entry: -->
すべてのログ メッセージにコンテキストを追加すると便利ですが、場合によっては、特定の例外にログに含めたい固有のコンテキストが含まれる場合があります。アプリケーションのカスタム例外の 1 つで `context` メソッドを定義すると、例外のログ エントリに追加する必要がある、その例外に関連するデータを指定できます。

```
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
```

<a name="the-report-helper"></a>
<!-- #### The `report` Helper -->
#### The `report` Helper

<!-- Sometimes you may need to report an exception but continue handling the current request. The `report` helper function allows you to quickly report an exception via the exception handler without rendering an error page to the user: -->
場合によっては、例外を報告しても現在のリクエストの処理を続行する必要がある場合があります。 `report` ヘルパ関数を使用すると、ユーザーにエラー ページを表示せずに、例外ハンドラーを介して例外を迅速に報告できます。

```
public function isValid($value)
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="ignoring-exceptions-by-type"></a>
<!-- ### Ignoring Exceptions By Type -->
### Ignoring Exceptions By Type

<!-- When building your application, there will be some types of exceptions you simply want to ignore and never report. Your application's exception handler contains a `$dontReport` property which is initialized to an empty array. Any classes that you add to this property will never be reported; however, they may still have custom rendering logic: -->
アプリケーションを構築するとき、無視して決して報告したくないいくつかの種類の例外が存在します。アプリケーションの例外ハンドラーには、空の配列に初期化される `$dontReport` プロパティが含まれています。このプロパティに追加したクラスは決して報告されません。ただし、カスタム レンダリング ロジックがまだ存在する場合があります。

```
use App\Exceptions\InvalidOrderException;

/**
 * A list of the exception types that should not be reported.
 *
 * @var array
 */
protected $dontReport = [
    InvalidOrderException::class,
];
```

> [!TIP]
> Laravel は舞台裏で、404 HTTP "not found" エラーや無効な CSRF トークンによって生成された 419 HTTP 応答に起因する例外など、一部の種類のエラーをすでに無視しています。

<a name="rendering-exceptions"></a>
<!-- ### Rendering Exceptions -->
### Rendering Exceptions

<!-- By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this via the `renderable` method of your exception handler. -->
デフォルトでは、Laravel 例外ハンドラーは例外を HTTP 応答に変換します。ただし、特定のタイプの例外に対してカスタム レンダリング クロージャを自由に登録できます。これは、例外ハンドラーの `renderable` メソッドを介して実行できます。

<!-- The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will deduce what type of exception the closure renders by examining the type-hint of the closure: -->
`renderable` メソッドに渡されるクロージャは、`response` ヘルパを介して生成できる `Illuminate\Http\Response` のインスタンスを返す必要があります。 Laravel は、クロージャのタイプヒントを調べることで、クロージャがレンダリングする例外のタイプを推測します。

```
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
```

<!-- You may also use the `renderable` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `renderable` method does not return a value, Laravel's default exception rendering will be utilized: -->
`renderable` メソッドを使用して、組み込み Laravel または Symfony 例外 (`NotFoundHttpException` など) のレンダリング動作をオーバーライドすることもできます。 `renderable` メソッドに指定されたクロージャが値を返さない場合、Laravel のデフォルトの例外レンダリングが利用されます。

```
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
```

<a name="renderable-exceptions"></a>
<!-- ### Reportable & Renderable Exceptions -->
### Reportable & Renderable Exceptions

<!-- Instead of type-checking exceptions in the exception handler's `register` method, you may define `report` and `render` methods directly on your custom exceptions. When these methods exist, they will be automatically called by the framework: -->
例外ハンドラーの `register` メソッドで例外の型をチェックする代わりに、カスタム例外に `report` メソッドと `render` メソッドを直接定義できます。これらのメソッドが存在する場合、フレームワークによって自動的に呼び出されます。

```
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
```

<!-- If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response: -->
組み込みの Laravel 例外や Symfony 例外など、すでにレンダリング可能な例外を例外が拡張する場合、例外の `render` メソッドから `false` を返して、例外のデフォルトの HTTP 応答をレンダリングできます。

```
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
```

<!-- If your exception contains custom reporting logic that is only necessary when certain conditions are met, you may need to instruct Laravel to sometimes report the exception using the default exception handling configuration. To accomplish this, you may return `false` from the exception's `report` method: -->
例外に、特定の条件が満たされた場合にのみ必要なカスタムレポートロジックが含まれている場合は、デフォルトの例外処理設定を使用して例外をレポートするように Laravel に指示する必要がある場合があります。これを実現するには、例外の `report` メソッドから `false` を返すことができます。

```
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
```

> [!TIP]
> `report` メソッドの必要な依存関係をタイプヒントで指定すると、Laravel の [service container](/docs/8.x/container) によって自動的にメソッドに挿入されます。

<a name="mapping-exceptions-by-type"></a>
<!-- ### Mapping Exceptions By Type -->
### Mapping Exceptions By Type

<!-- Sometimes, third-party libraries used by your application may throw exceptions that you wish to make [renderable](#renderable-exceptions), but are unable to do so because you do not have control over the definitions of third-party exceptions. -->
場合によっては、アプリケーションで使用されるサードパーティ ライブラリが、[renderable](#renderable-exceptions) を実行したい例外をスローすることがありますが、サードパーティ例外の定義を制御できないため、実行できないことがあります。

<!-- Thankfully, Laravel allows you to conveniently map these exceptions to other exception types that you manage within your application. To accomplish this, call the `map` method from your exception handler's `register` method: -->
ありがたいことに、Laravel では、これらの例外をアプリケーション内で管理する他の例外タイプに簡単にマップできます。これを実現するには、例外ハンドラーの `register` メソッドから `map` メソッドを呼び出します。

```
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
```

<!-- If you would like more control over the creation of the target exception, you may pass a closure to the `map` method: -->
ターゲット例外の作成をより詳細に制御したい場合は、`map` メソッドにクロージャを渡すことができます。

```
use League\Flysystem\Exception;
use App\Exceptions\FilesystemException;

$this->map(fn (Exception $e) => new FilesystemException($e));
```

<a name="http-exceptions"></a>
<!-- ## HTTP Exceptions -->
## HTTP Exceptions

<!-- Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401) or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper: -->
一部の例外は、サーバーからの HTTP エラー コードを示します。たとえば、これは「ページが見つかりません」エラー (404)、「不正エラー」(401)、または開発者が生成した 500 エラーである可能性があります。アプリケーション内の任意の場所からこのような応答を生成するには、`abort` ヘルパを使用できます。

```
abort(404);
```

<a name="custom-http-error-pages"></a>
<!-- ### Custom HTTP Error Pages -->
### Custom HTTP Error Pages

<!-- Laravel makes it easy to display custom error pages for various HTTP status codes. For example, if you wish to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered on all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable: -->
Laravel を使用すると、さまざまな HTTP ステータス コードのカスタム エラー ページを簡単に表示できます。たとえば、404 HTTP ステータス コードのエラー ページをカスタマイズする場合は、`resources/views/errors/404.blade.php` ビュー テンプレートを作成します。このビューは、アプリケーションによって生成されたすべての 404 エラーに対してレンダリングされます。このディレクトリ内のビューには、対応する HTTP ステータス コードと一致する名前を付ける必要があります。 `abort` 関数によって生成された `Symfony\Component\HttpKernel\Exception\HttpException` インスタンスは、`$exception` 変数としてビューに渡されます。

```
<h2>{{ $exception->getMessage() }}</h2>
```

<!-- You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking: -->
`vendor:publish` Artisan コマンドを使用して、Laravel のデフォルトのエラー ページ テンプレートを公開できます。テンプレートが公開されたら、好みに合わせてカスタマイズできます。

```
php artisan vendor:publish --tag=laravel-errors
```

