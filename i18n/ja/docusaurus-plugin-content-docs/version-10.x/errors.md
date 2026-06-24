<!-- # Error Handling -->
# Error Handling

- [Introduction](#introduction)
- [Configuration](#configuration)
- [The Exception Handler](#the-exception-handler)
    - [Reporting Exceptions](#reporting-exceptions)
    - [Exception Log Levels](#exception-log-levels)
    - [Ignoring Exceptions by Type](#ignoring-exceptions-by-type)
    - [Rendering Exceptions](#rendering-exceptions)
    - [Reportable and Renderable Exceptions](#renderable-exceptions)
- [Throttling Reported Exceptions](#throttling-reported-exceptions)
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

<!-- All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/10.x/logging) configuration. However, you are free to log exceptions however you wish. -->
すべての例外は、`App\Exceptions\Handler` クラスによって処理されます。このクラスには、カスタム例外レポートおよびレンダリング コールバックを登録できる `register` メソッドが含まれています。これらの各概念を詳しく見ていきます。例外レポートは、例外をログに記録したり、例外を [Flare](https://flareapp.io)、[Bugsnag](https://bugsnag.com)、[Sentry](https://github.com/getsentry/sentry-laravel) などの外部サービスに送信したりするために使用されます。デフォルトでは、例外は [logging](/docs/10.x/logging) 構成に基づいて記録されます。ただし、例外を自由にログに記録することができます。

<!-- If you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will determine what type of exception the closure reports by examining the type-hint of the closure: -->
さまざまなタイプの例外をさまざまな方法で報告する必要がある場合は、`reportable` メソッドを使用して、特定のタイプの例外を報告する必要があるときに実行する必要があるクロージャを登録できます。 Laravel は、クロージャのタイプヒントを調べることで、クロージャが報告する例外のタイプを判断します。

```
use App\Exceptions\InvalidOrderException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->reportable(function (InvalidOrderException $e) {
        // ...
    });
}
```

<!-- When you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback: -->
`reportable` メソッドを使用してカスタム例外レポート コールバックを登録すると、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。デフォルトのログ スタックへの例外の伝播を停止したい場合は、レポート コールバックを定義するときに `stop` メソッドを使用するか、コールバックから `false` を返します。

```
$this->reportable(function (InvalidOrderException $e) {
    // ...
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!NOTE]
> 特定の例外の例外レポートをカスタマイズするには、[reportable exceptions](/docs/10.x/errors#renderable-exceptions) を利用することもできます。

<a name="global-log-context"></a>
<!-- #### Global Log Context -->
#### Global Log Context

<!-- If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by defining a `context` method on your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application: -->
利用可能な場合、Laravel は現在のユーザーの ID をコンテキスト データとしてすべての例外のログ メッセージに自動的に追加します。アプリケーションの `App\Exceptions\Handler` クラスで `context` メソッドを定義することで、独自のグローバル コンテキスト データを定義できます。この情報は、アプリケーションによって書き込まれるすべての例外のログ メッセージに含まれます。

```
/**
 * Get the default context variables for logging.
 *
 * @return array<string, mixed>
 */
protected function context(): array
{
    return array_merge(parent::context(), [
        'foo' => 'bar',
    ]);
}
```

<a name="exception-log-context"></a>
<!-- #### Exception Log Context -->
#### Exception Log Context

<!-- While adding context to every log message can be useful, sometimes a particular exception may have unique context that you would like to include in your logs. By defining a `context` method on one of your application's exceptions, you may specify any data relevant to that exception that should be added to the exception's log entry: -->
すべてのログ メッセージにコンテキストを追加すると便利ですが、場合によっては、特定の例外にログに含めたい固有のコンテキストが含まれる場合があります。アプリケーションの例外の 1 つで `context` メソッドを定義すると、例外のログ エントリに追加する必要がある、その例外に関連するデータを指定できます。

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
     * @return array<string, mixed>
     */
    public function context(): array
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
public function isValid(string $value): bool
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
<!-- #### Deduplicating Reported Exceptions -->
#### Deduplicating Reported Exceptions

<!-- If you are using the `report` function throughout your application, you may occasionally report the same exception multiple times, creating duplicate entries in your logs. -->
アプリケーション全体で `report` 関数を使用している場合、同じ例外が複数回報告され、ログに重複したエントリが作成されることがあります。

<!-- If you would like to ensure that a single instance of an exception is only ever reported once, you may set the `$withoutDuplicates` property to `true` within your application's `App\Exceptions\Handler` class: -->
例外の単一インスタンスが一度だけ報告されるようにしたい場合は、アプリケーションの `App\Exceptions\Handler` クラス内で `$withoutDuplicates` プロパティを `true` に設定します。

```php
namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;

class Handler extends ExceptionHandler
{
    /**
     * Indicates that an exception instance should only be reported once.
     *
     * @var bool
     */
    protected $withoutDuplicates = true;

    // ...
}
```

<!-- Now, when the `report` helper is called with the same instance of an exception, only the first call will be reported: -->
現在、`report` ヘルパが例外の同じインスタンスで呼び出される場合、最初の呼び出しのみが報告されます。

```php
$original = new RuntimeException('Whoops!');

report($original); // reported

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // ignored
}

report($original); // ignored
report($caught); // ignored
```

<a name="exception-log-levels"></a>
<!-- ### Exception Log Levels -->
### Exception Log Levels

<!-- When messages are written to your application's [logs](/docs/10.x/logging), the messages are written at a specified [log level](/docs/10.x/logging#log-levels), which indicates the severity or importance of the message being logged. -->
メッセージがアプリケーションの [logs](/docs/10.x/logging) に書き込まれる場合、メッセージは指定された [log level](/docs/10.x/logging#log-levels) に書き込まれます。これは、記録されるメッセージの重大度または重要性を示します。

<!-- As noted above, even when you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application; however, since the log level can sometimes influence the channels on which a message is logged, you may wish to configure the log level that certain exceptions are logged at. -->
上で述べたように、`reportable` メソッドを使用してカスタム例外レポート コールバックを登録した場合でも、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。ただし、ログ レベルはメッセージが記録されるチャネルに影響を与える場合があるため、特定の例外が記録されるログ レベルを構成することもできます。

<!-- To accomplish this, you may define a `$levels` property on your application's exception handler. This property should contain an array of exception types and their associated log levels: -->
これを実現するには、アプリケーションの例外ハンドラーで `$levels` プロパティを定義できます。このプロパティには、例外タイプとそれに関連するログ レベルの配列が含まれている必要があります。

```
use PDOException;
use Psr\Log\LogLevel;

/**
 * A list of exception types with their corresponding custom log levels.
 *
 * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
 */
protected $levels = [
    PDOException::class => LogLevel::CRITICAL,
];
```

<a name="ignoring-exceptions-by-type"></a>
<!-- ### Ignoring Exceptions by Type -->
### Ignoring Exceptions by Type

<!-- When building your application, there will be some types of exceptions you never want to report. To ignore these exceptions, define a `$dontReport` property on your application's exception handler. Any classes that you add to this property will never be reported; however, they may still have custom rendering logic: -->
アプリケーションを構築するとき、報告したくない種類の例外が発生することがあります。これらの例外を無視するには、アプリケーションの例外ハンドラーで `$dontReport` プロパティを定義します。このプロパティに追加したクラスは決して報告されません。ただし、カスタム レンダリング ロジックがまだ存在する場合があります。

```
use App\Exceptions\InvalidOrderException;

/**
 * A list of the exception types that are not reported.
 *
 * @var array<int, class-string<\Throwable>>
 */
protected $dontReport = [
    InvalidOrderException::class,
];
```

<!-- Internally, Laravel already ignores some types of errors for you, such as exceptions resulting from 404 HTTP errors or 419 HTTP responses generated by invalid CSRF tokens. If you would like to instruct Laravel to stop ignoring a given type of exception, you may invoke the `stopIgnoring` method within your exception handler's `register` method: -->
内部的には、Laravel はすでに、無効な CSRF トークンによって生成された 404 HTTP エラーや 419 HTTP 応答に起因する例外など、一部の種類のエラーを無視します。特定のタイプの例外の無視を停止するように Laravel に指示したい場合は、例外ハンドラーの `register` メソッド内で `stopIgnoring` メソッドを呼び出すことができます。

```
use Symfony\Component\HttpKernel\Exception\HttpException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->stopIgnoring(HttpException::class);

    // ...
}
```

<a name="rendering-exceptions"></a>
<!-- ### Rendering Exceptions -->
### Rendering Exceptions

<!-- By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this by invoking the `renderable` method within your exception handler. -->
デフォルトでは、Laravel 例外ハンドラーは例外を HTTP 応答に変換します。ただし、特定のタイプの例外に対してカスタム レンダリング クロージャを自由に登録できます。これを行うには、例外ハンドラー内で `renderable` メソッドを呼び出します。

<!-- The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will determine what type of exception the closure renders by examining the type-hint of the closure: -->
`renderable` メソッドに渡されるクロージャは、`response` ヘルパを介して生成できる `Illuminate\Http\Response` のインスタンスを返す必要があります。 Laravel は、クロージャのタイプヒントを調べることによって、クロージャがレンダリングする例外のタイプを決定します。

```
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->renderable(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', [], 500);
    });
}
```

<!-- You may also use the `renderable` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `renderable` method does not return a value, Laravel's default exception rendering will be utilized: -->
`renderable` メソッドを使用して、組み込み Laravel または Symfony 例外 (`NotFoundHttpException` など) のレンダリング動作をオーバーライドすることもできます。 `renderable` メソッドに指定されたクロージャが値を返さない場合、Laravel のデフォルトの例外レンダリングが利用されます。

```
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->renderable(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
}
```

<a name="renderable-exceptions"></a>
<!-- ### Reportable and Renderable Exceptions -->
### Reportable and Renderable Exceptions

<!-- Instead of defining custom reporting and rendering behavior in your exception handler's `register` method, you may define `report` and `render` methods directly on your application's exceptions. When these methods exist, they will automatically be called by the framework: -->
例外ハンドラーの `register` メソッドでカスタム レポートとレンダリング動作を定義する代わりに、アプリケーションの例外に `report` メソッドと `render` メソッドを直接定義できます。これらのメソッドが存在する場合、フレームワークによって自動的に呼び出されます。

```
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * Render the exception into an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

<!-- If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response: -->
組み込みの Laravel 例外や Symfony 例外など、すでにレンダリング可能な例外を例外が拡張する場合、例外の `render` メソッドから `false` を返して、例外のデフォルトの HTTP 応答をレンダリングできます。

```
/**
 * Render the exception into an HTTP response.
 */
public function render(Request $request): Response|bool
{
    if (/** Determine if the exception needs custom rendering */) {

        return response(/* ... */);
    }

    return false;
}
```

<!-- If your exception contains custom reporting logic that is only necessary when certain conditions are met, you may need to instruct Laravel to sometimes report the exception using the default exception handling configuration. To accomplish this, you may return `false` from the exception's `report` method: -->
例外に、特定の条件が満たされた場合にのみ必要なカスタムレポートロジックが含まれている場合は、デフォルトの例外処理設定を使用して例外をレポートするように Laravel に指示する必要がある場合があります。これを実現するには、例外の `report` メソッドから `false` を返すことができます。

```
/**
 * Report the exception.
 */
public function report(): bool
{
    if (/** Determine if the exception needs custom reporting */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` メソッドの必要な依存関係をタイプヒントで指定すると、それらは Laravel の [service container](/docs/10.x/container) によってメソッドに自動的に挿入されます。

<a name="throttling-reported-exceptions"></a>
<!-- ### Throttling Reported Exceptions -->
### Throttling Reported Exceptions

<!-- If your application reports a very large number of exceptions, you may want to throttle how many exceptions are actually logged or sent to your application's external error tracking service. -->
アプリケーションが非常に多くの例外を報告する場合、実際にログに記録される、またはアプリケーションの外部エラー追跡サービスに送信される例外の数を調整することができます。

<!-- To take a random sample rate of exceptions, you can return a `Lottery` instance from your exception handler's `throttle` method. If your `App\Exceptions\Handler` class does not contain this method, you may simply add it to the class: -->
例外のランダムなサンプルレートを取得するには、例外ハンドラーの `throttle` メソッドから `Lottery` インスタンスを返すことができます。 `App\Exceptions\Handler` クラスにこのメソッドが含まれていない場合は、単にクラスに追加するだけで済みます。

```php
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    return Lottery::odds(1, 1000);
}
```

<!-- It is also possible to conditionally sample based on the exception type. If you would like to only sample instances of a specific exception class, you may return a `Lottery` instance only for that class: -->
例外タイプに基づいて条件付きでサンプリングすることも可能です。特定の例外クラスのインスタンスのみをサンプルしたい場合は、そのクラスのみの `Lottery` インスタンスを返すことができます。

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof ApiMonitoringException) {
        return Lottery::odds(1, 1000);
    }
}
```

<!-- You may also rate limit exceptions logged or sent to an external error tracking service by returning a `Limit` instance instead of a `Lottery`. This is useful if you want to protect against sudden bursts of exceptions flooding your logs, for example, when a third-party service used by your application is down: -->
`Lottery` の代わりに `Limit` インスタンスを返すことで、ログに記録されるか、外部エラー追跡サービスに送信される例外をレート制限することもできます。これは、アプリケーションで使用されているサードパーティのサービスがダウンしている場合など、ログをあふれさせる突然の例外のバーストから保護したい場合に役立ちます。

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300);
    }
}
```

<!-- By default, limits will use the exception's class as the rate limit key. You can customize this by specifying your own key using the `by` method on the `Limit`: -->
デフォルトでは、制限は例外のクラスをレート制限キーとして使用します。これをカスタマイズするには、`Limit` で `by` メソッドを使用して独自のキーを指定します。

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    if ($e instanceof BroadcastException) {
        return Limit::perMinute(300)->by($e->getMessage());
    }
}
```

<!-- Of course, you may return a mixture of `Lottery` and `Limit` instances for different exceptions: -->
もちろん、さまざまな例外に対して、`Lottery` インスタンスと `Limit` インスタンスを組み合わせて返すこともできます。

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

/**
 * Throttle incoming exceptions.
 */
protected function throttle(Throwable $e): mixed
{
    return match (true) {
        $e instanceof BroadcastException => Limit::perMinute(300),
        $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
        default => Limit::none(),
    };
}
```

<a name="http-exceptions"></a>
<!-- ## HTTP Exceptions -->
## HTTP Exceptions

<!-- Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401), or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper: -->
一部の例外は、サーバーからの HTTP エラー コードを示します。たとえば、これは「ページが見つかりません」エラー (404)、「不正エラー」(401)、または開発者が生成した 500 エラーである可能性があります。アプリケーション内の任意の場所からこのような応答を生成するには、`abort` ヘルパを使用できます。

```
abort(404);
```

<a name="custom-http-error-pages"></a>
<!-- ### Custom HTTP Error Pages -->
### Custom HTTP Error Pages

<!-- Laravel makes it easy to display custom error pages for various HTTP status codes. For example, to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered for all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable: -->
Laravel を使用すると、さまざまな HTTP ステータス コードのカスタム エラー ページを簡単に表示できます。たとえば、404 HTTP ステータス コードのエラー ページをカスタマイズするには、`resources/views/errors/404.blade.php` ビュー テンプレートを作成します。このビューは、アプリケーションによって生成されたすべての 404 エラーに対してレンダリングされます。このディレクトリ内のビューには、対応する HTTP ステータス コードと一致する名前を付ける必要があります。 `abort` 関数によって生成された `Symfony\Component\HttpKernel\Exception\HttpException` インスタンスは、`$exception` 変数としてビューに渡されます。

```
<h2>{{ $exception->getMessage() }}</h2>
```

<!-- You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking: -->
`vendor:publish` Artisan コマンドを使用して、Laravel のデフォルトのエラー ページ テンプレートを公開できます。テンプレートが公開されたら、好みに合わせてカスタマイズできます。

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
<!-- #### Fallback HTTP Error Pages -->
#### Fallback HTTP Error Pages

<!-- You may also define a "fallback" error page for a given series of HTTP status codes. This page will be rendered if there is not a corresponding page for the specific HTTP status code that occurred. To accomplish this, define a `4xx.blade.php` template and a `5xx.blade.php` template in your application's `resources/views/errors` directory. -->
特定の一連の HTTP ステータス コードに対して「フォールバック」エラー ページを定義することもできます。このページは、発生した特定の HTTP ステータス コードに対応するページがない場合に表示されます。これを実現するには、アプリケーションの `resources/views/errors` ディレクトリに `4xx.blade.php` テンプレートと `5xx.blade.php` テンプレートを定義します。

