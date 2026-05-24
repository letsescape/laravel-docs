# エラー処理 (Error Handling)

- [Introduction](#introduction)
- [Configuration](#configuration)
- [例外の処理](#handling-exceptions)
    - [例外の報告](#reporting-exceptions)
    - [例外ログレベル](#exception-log-levels)
    - [タイプごとの例外の無視](#ignoring-exceptions-by-type)
    - [レンダリングの例外](#rendering-exceptions)
    - [報告可能な例外とレンダリング可能な例外](#renderable-exceptions)
- [報告された例外の調整](#throttling-reported-exceptions)
- [HTTP例外](#http-exceptions)
    - [カスタム HTTP エラー ページ](#custom-http-error-pages)

<a name="introduction"></a>
## 導入 (Introduction)

新しい Laravel プロジェクトを開始すると、エラーと例外の処理がすでに構成されています。ただし、いつでも、アプリケーションの `bootstrap/app.php` で `withExceptions` メソッドを使用して、アプリケーションによる例外の報告方法とレンダリング方法を管理できます。

`withExceptions` クロージャーに提供される `$exceptions` オブジェクトは、`Illuminate\Foundation\Configuration\Exceptions` のインスタンスであり、アプリケーションでの例外処理を管理します。このドキュメントでは、このオブジェクトについてさらに詳しく説明します。

<a name="configuration"></a>
## 構成 (Configuration)

`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

ローカル開発中は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で値が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="handling-exceptions"></a>
## 例外の処理 (Handling Exceptions)

<a name="reporting-exceptions"></a>
### 例外の報告

Laravel では、例外レポートを使用して例外をログに記録したり、例外を [Sentry](https://github.com/getsentry/sentry-laravel) や [Flare](https://flareapp.io) などの外部サービスに送信したりします。デフォルトでは、例外は [logging](/docs/{{version}}/logging) 構成に基づいて記録されます。ただし、例外を自由にログに記録することができます。

さまざまなタイプの例外をさまざまな方法で報告する必要がある場合は、アプリケーションの `bootstrap/app.php` で `report` 例外メソッドを使用して、特定のタイプの例外を報告する必要があるときに実行する必要があるクロージャを登録できます。 Laravel は、クロージャのタイプヒントを調べることで、クロージャが報告する例外のタイプを判断します。

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->report(function (InvalidOrderException $e) {
            // ...
        });
    })

`report` メソッドを使用してカスタム例外レポート コールバックを登録すると、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。デフォルトのログ スタックへの例外の伝播を停止したい場合は、レポート コールバックを定義するときに `stop` メソッドを使用するか、コールバックから `false` を返します。

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->report(function (InvalidOrderException $e) {
            // ...
        })->stop();

        $exceptions->report(function (InvalidOrderException $e) {
            return false;
        });
    })

> [!NOTE]  
> 特定の例外の例外レポートをカスタマイズするには、[報告可能な例外](/docs/{{version}}/errors#renderable-exceptions) を利用することもできます。

<a name="global-log-context"></a>
#### グローバルログコンテキスト

利用可能な場合、Laravel は現在のユーザーの ID をコンテキスト データとしてすべての例外のログ メッセージに自動的に追加します。アプリケーションの `bootstrap/app.php` ファイルで `context` 例外メソッドを使用して、独自のグローバル コンテキスト データを定義できます。この情報は、アプリケーションによって書き込まれるすべての例外のログ メッセージに含まれます。

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->context(fn () => [
            'foo' => 'bar',
        ]);
    })

<a name="exception-log-context"></a>
#### 例外ログのコンテキスト

すべてのログ メッセージにコンテキストを追加すると便利ですが、場合によっては、特定の例外にログに含めたい固有のコンテキストが含まれる場合があります。アプリケーションの例外の 1 つで `context` メソッドを定義すると、例外のログ エントリに追加する必要がある、その例外に関連するデータを指定できます。

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

<a name="the-report-helper"></a>
#### `report` ヘルパ

場合によっては、例外を報告しても現在のリクエストの処理を続行する必要がある場合があります。 `report` ヘルパ関数を使用すると、ユーザーにエラー ページを表示せずに例外を迅速に報告できます。

    public function isValid(string $value): bool
    {
        try {
            // Validate the value...
        } catch (Throwable $e) {
            report($e);

            return false;
        }
    }

<a name="deduplicating-reported-exceptions"></a>
#### 報告された例外の重複排除

アプリケーション全体で `report` 関数を使用している場合、同じ例外が複数回報告され、ログに重複したエントリが作成されることがあります。

例外の 1 つのインスタンスが 1 回だけ報告されるようにしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `dontReportDuplicates` 例外メソッドを呼び出すことができます。

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->dontReportDuplicates();
    })

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
### 例外ログレベル

メッセージがアプリケーションの [logs](/docs/{{version}}/logging) に書き込まれる場合、メッセージは指定された [ログレベル](/docs/{{version}}/logging#log-levels) に書き込まれます。これは、記録されるメッセージの重大度または重要性を示します。

上で述べたように、`report` メソッドを使用してカスタム例外レポート コールバックを登録した場合でも、Laravel はアプリケーションのデフォルトのログ構成を使用して例外をログに記録します。ただし、ログ レベルはメッセージが記録されるチャネルに影響を与える場合があるため、特定の例外が記録されるログ レベルを構成することもできます。

これを実現するには、アプリケーションの `bootstrap/app.php` ファイルで `level` 例外メソッドを使用します。このメソッドは、最初の引数として例外タイプを受け取り、2 番目の引数としてログ レベルを受け取ります。

    use PDOException;
    use Psr\Log\LogLevel;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->level(PDOException::class, LogLevel::CRITICAL);
    })

<a name="ignoring-exceptions-by-type"></a>
### タイプごとの例外の無視

アプリケーションを構築するとき、報告したくない種類の例外が発生することがあります。これらの例外を無視するには、アプリケーションの `bootstrap/app.php` ファイルで `dontReport` 例外メソッドを使用します。このメソッドに提供されたクラスは決して報告されません。ただし、カスタム レンダリング ロジックがまだ存在する場合があります。

    use App\Exceptions\InvalidOrderException;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->dontReport([
            InvalidOrderException::class,
        ]);
    })

あるいは、`Illuminate\Contracts\Debug\ShouldntReport` インターフェイスを使用して例外クラスを単純に「マーク」することもできます。このインターフェースで例外がマークされると、Laravel の例外ハンドラーによって例外が報告されることはありません。

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Contracts\Debug\ShouldntReport;

class PodcastProcessingException extends Exception implements ShouldntReport
{
    //
}
```

内部的には、Laravel はすでに、無効な CSRF トークンによって生成された 404 HTTP エラーや 419 HTTP 応答に起因する例外など、一部の種類のエラーを無視します。特定のタイプの例外の無視を停止するように Laravel に指示したい場合は、アプリケーションの `bootstrap/app.php` ファイルで `stopIgnoring` 例外メソッドを使用できます。

    use Symfony\Component\HttpKernel\Exception\HttpException;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->stopIgnoring(HttpException::class);
    })

<a name="rendering-exceptions"></a>
### レンダリングの例外

デフォルトでは、Laravel 例外ハンドラーは例外を HTTP 応答に変換します。ただし、特定のタイプの例外に対してカスタム レンダリング クロージャを自由に登録できます。これを行うには、アプリケーションの `bootstrap/app.php` ファイルで `render` 例外メソッドを使用します。

`render` メソッドに渡されるクロージャは、`response` ヘルパを介して生成できる `Illuminate\Http\Response` のインスタンスを返す必要があります。 Laravel は、クロージャのタイプヒントを調べることによって、クロージャがレンダリングする例外のタイプを決定します。

    use App\Exceptions\InvalidOrderException;
    use Illuminate\Http\Request;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->render(function (InvalidOrderException $e, Request $request) {
            return response()->view('errors.invalid-order', status: 500);
        });
    })

`render` メソッドを使用して、組み込み Laravel または Symfony 例外 (`NotFoundHttpException` など) のレンダリング動作をオーバーライドすることもできます。 `render` メソッドに指定されたクロージャが値を返さない場合、Laravel のデフォルトの例外レンダリングが利用されます。

    use Illuminate\Http\Request;
    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->render(function (NotFoundHttpException $e, Request $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Record not found.'
                ], 404);
            }
        });
    })

<a name="rendering-exceptions-as-json"></a>
#### 例外を JSON としてレンダリングする

例外をレンダリングするとき、Laravel はリクエストの `Accept` ヘッダーに基づいて、例外を HTML 応答としてレンダリングするか JSON 応答としてレンダリングするかを自動的に決定します。 Laravel が HTML または JSON 例外応答をレンダリングするかどうかを決定する方法をカスタマイズしたい場合は、`shouldRenderJsonWhen` メソッドを利用できます。

    use Illuminate\Http\Request;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
            if ($request->is('admin/*')) {
                return true;
            }

            return $request->expectsJson();
        });
    })

<a name="customizing-the-exception-response"></a>
#### 例外応答のカスタマイズ

まれに、Laravel の例外ハンドラーによってレンダリングされる HTTP 応答全体をカスタマイズする必要がある場合があります。これを実現するには、`respond` メソッドを使用して応答カスタマイズ クロージャを登録できます。

    use Symfony\Component\HttpFoundation\Response;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->respond(function (Response $response) {
            if ($response->getStatusCode() === 419) {
                return back()->with([
                    'message' => 'The page expired, please try again.',
                ]);
            }

            return $response;
        });
    })

<a name="renderable-exceptions"></a>
### 報告可能な例外とレンダリング可能な例外

アプリケーションの `bootstrap/app.php` ファイルでカスタム レポートとレンダリング動作を定義する代わりに、アプリケーションの例外に対して `report` メソッドと `render` メソッドを直接定義できます。これらのメソッドが存在する場合、フレームワークによって自動的に呼び出されます。

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

組み込みの Laravel 例外や Symfony 例外など、すでにレンダリング可能な例外を例外が拡張する場合、例外の `render` メソッドから `false` を返して、例外のデフォルトの HTTP 応答をレンダリングできます。

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

例外に、特定の条件が満たされた場合にのみ必要なカスタムレポートロジックが含まれている場合は、デフォルトの例外処理設定を使用して例外をレポートするように Laravel に指示する必要がある場合があります。これを実現するには、例外の `report` メソッドから `false` を返すことができます。

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

> [!NOTE]  
> `report` メソッドの必要な依存関係をタイプヒントで指定すると、それらは Laravel の [サービスコンテナ](/docs/{{version}}/container) によってメソッドに自動的に挿入されます。

<a name="throttling-reported-exceptions"></a>
### 報告された例外の調整

アプリケーションが非常に多くの例外を報告する場合、実際にログに記録される、またはアプリケーションの外部エラー追跡サービスに送信される例外の数を調整することができます。

例外のランダムなサンプルレートを取得するには、アプリケーションの `bootstrap/app.php` ファイルで `throttle` 例外メソッドを使用できます。 `throttle` メソッドは、`Lottery` インスタンスを返すクロージャを受け取ります。

    use Illuminate\Support\Lottery;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            return Lottery::odds(1, 1000);
        });
    })

例外タイプに基づいて条件付きでサンプリングすることも可能です。特定の例外クラスのインスタンスのみをサンプルしたい場合は、そのクラスのみの `Lottery` インスタンスを返すことができます。

    use App\Exceptions\ApiMonitoringException;
    use Illuminate\Support\Lottery;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            if ($e instanceof ApiMonitoringException) {
                return Lottery::odds(1, 1000);
            }
        });
    })

`Lottery` の代わりに `Limit` インスタンスを返すことで、ログに記録されるか、外部エラー追跡サービスに送信される例外をレート制限することもできます。これは、アプリケーションで使用されているサードパーティのサービスがダウンしている場合など、ログをあふれさせる突然の例外のバーストから保護したい場合に役立ちます。

    use Illuminate\Broadcasting\BroadcastException;
    use Illuminate\Cache\RateLimiting\Limit;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            if ($e instanceof BroadcastException) {
                return Limit::perMinute(300);
            }
        });
    })

デフォルトでは、制限は例外のクラスをレート制限キーとして使用します。これをカスタマイズするには、`Limit` で `by` メソッドを使用して独自のキーを指定します。

    use Illuminate\Broadcasting\BroadcastException;
    use Illuminate\Cache\RateLimiting\Limit;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            if ($e instanceof BroadcastException) {
                return Limit::perMinute(300)->by($e->getMessage());
            }
        });
    })

もちろん、さまざまな例外に対して、`Lottery` インスタンスと `Limit` インスタンスを組み合わせて返すこともできます。

    use App\Exceptions\ApiMonitoringException;
    use Illuminate\Broadcasting\BroadcastException;
    use Illuminate\Cache\RateLimiting\Limit;
    use Illuminate\Support\Lottery;
    use Throwable;

    ->withExceptions(function (Exceptions $exceptions) {
        $exceptions->throttle(function (Throwable $e) {
            return match (true) {
                $e instanceof BroadcastException => Limit::perMinute(300),
                $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
                default => Limit::none(),
            };
        });
    })

<a name="http-exceptions"></a>
## HTTP例外 (HTTP Exceptions)

一部の例外は、サーバーからの HTTP エラー コードを示します。たとえば、これは「ページが見つかりません」エラー (404)、「不正エラー」(401)、または開発者が生成した 500 エラーである可能性があります。アプリケーション内の任意の場所からこのような応答を生成するには、`abort` ヘルパを使用できます。

    abort(404);

<a name="custom-http-error-pages"></a>
### カスタム HTTP エラー ページ

Laravel を使用すると、さまざまな HTTP ステータス コードのカスタム エラー ページを簡単に表示できます。たとえば、404 HTTP ステータス コードのエラー ページをカスタマイズするには、`resources/views/errors/404.blade.php` ビュー テンプレートを作成します。このビューは、アプリケーションによって生成されたすべての 404 エラーに対してレンダリングされます。このディレクトリ内のビューには、対応する HTTP ステータス コードと一致する名前を付ける必要があります。 `abort` 関数によって生成された `Symfony\Component\HttpKernel\Exception\HttpException` インスタンスは、`$exception` 変数としてビューに渡されます。

    <h2>{{ $exception->getMessage() }}</h2>

`vendor:publish` Artisan コマンドを使用して、Laravel のデフォルトのエラー ページ テンプレートを公開できます。テンプレートが公開されたら、好みに合わせてカスタマイズできます。

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### フォールバック HTTP エラー ページ

特定の一連の HTTP ステータス コードに対して「フォールバック」エラー ページを定義することもできます。このページは、発生した特定の HTTP ステータス コードに対応するページがない場合に表示されます。これを実現するには、アプリケーションの `resources/views/errors` ディレクトリに `4xx.blade.php` テンプレートと `5xx.blade.php` テンプレートを定義します。

Laravel にはこれらのステータス コード用の内部専用ページがあるため、フォールバック エラー ページを定義する場合、フォールバック ページは `404`、`500`、および `503` エラー応答には影響しません。これらのステータス コードに対して表示されるページをカスタマイズするには、それぞれのステータス コードに対してカスタム エラー ページを個別に定義する必要があります。

