<!-- # Error Handling -->
# Error Handling

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Handling Exceptions](#handling-exceptions)
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

<!-- When you start a new Laravel project, error and exception handling is already configured for you; however, at any point, you may use the `withExceptions` method in your application's `bootstrap/app.php` to manage how exceptions are reported and rendered by your application. -->
새 Laravel 프로젝트를 시작하면 오류 및 예외 처리는 이미 설정되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php`에서 `withExceptions` 메서드를 사용하여 애플리케이션이 예외를 보고하고 렌더링하는 방식을 관리할 수 있습니다.

<!-- The `$exceptions` object provided to the `withExceptions` closure is an instance of `Illuminate\Foundation\Configuration\Exceptions` and is responsible for managing exception handling in your application. We'll dive deeper into this object throughout this documentation. -->
`withExceptions` 클로저에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션의 예외 처리를 관리합니다. 이 문서 전반에서 이 객체를 더 자세히 살펴보겠습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 오류에 대한 정보가 실제로 사용자에게 얼마나 표시될지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따르도록 설정되어 있습니다.

<!-- During local development, you should set the `APP_DEBUG` environment variable to `true`. -->
로컬 개발 중에는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다.

> [!WARNING]
> 프로덕션 환경에서는 `APP_DEBUG` 값이 항상 `false`여야 합니다. 프로덕션에서 이 값이 `true`로 설정되면 민감한 설정 값이 애플리케이션의 최종 사용자에게 노출될 위험이 있습니다.

<a name="handling-exceptions"></a>
<!-- ## Handling Exceptions -->
## Handling Exceptions

<a name="reporting-exceptions"></a>
<!-- ### Reporting Exceptions -->
### Reporting Exceptions

<!-- In Laravel, exception reporting is used to log exceptions or send them to an external service like [Sentry](https://github.com/getsentry/sentry-laravel) or [Flare](https://flareapp.io). By default, exceptions will be logged based on your [logging](/docs/13.x/logging) configuration. However, you are free to log exceptions however you wish. -->
Laravel에서 예외 보고는 예외를 로그에 기록하거나 [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io) 같은 외부 서비스로 보내는 데 사용됩니다. 기본적으로 예외는 [logging](/docs/13.x/logging) 설정에 따라 로그에 기록됩니다. 하지만 원하는 방식으로 자유롭게 예외를 기록할 수 있습니다.

<!-- If you need to report different types of exceptions in different ways, you may use the `report` exception method in your application's `bootstrap/app.php` to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will determine what type of exception the closure reports by examining the type-hint of the closure: -->
서로 다른 타입의 예외를 서로 다른 방식으로 보고해야 한다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드를 사용하여 특정 타입의 예외를 보고해야 할 때 실행될 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 검사하여 해당 클로저가 어떤 타입의 예외를 보고하는지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<!-- When you register a custom exception reporting callback using the `report` method, Laravel will still log the exception using the default logging configuration for the application. If you wish to stop the propagation of the exception to the default logging stack, you may use the `stop` method when defining your reporting callback or return `false` from the callback: -->
`report` 메서드를 사용하여 사용자 정의 예외 보고 콜백을 등록하더라도, Laravel은 애플리케이션의 기본 로깅 설정을 사용하여 예외를 계속 로그에 기록합니다. 예외가 기본 로깅 스택으로 전달되는 것을 중지하려면 보고 콜백을 정의할 때 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```

> [!NOTE]
> 특정 예외의 예외 보고를 사용자 정의하려면 [reportable exceptions](/docs/13.x/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
<!-- #### Global Log Context -->
#### Global Log Context

<!-- If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data using the `context` exception method in your application's `bootstrap/app.php` file. This information will be included in every exception's log message written by your application: -->
가능한 경우 Laravel은 현재 사용자의 ID를 모든 예외 로그 메시지에 컨텍스트 데이터로 자동 추가합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용하여 직접 전역 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션이 작성하는 모든 예외 로그 메시지에 포함됩니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
<!-- #### Exception Log Context -->
#### Exception Log Context

<!-- While adding context to every log message can be useful, sometimes a particular exception may have unique context that you would like to include in your logs. By defining a `context` method on one of your application's exceptions, you may specify any data relevant to that exception that should be added to the exception's log entry: -->
모든 로그 메시지에 컨텍스트를 추가하는 것은 유용할 수 있지만, 때로는 특정 예외에 로그에 포함하고 싶은 고유한 컨텍스트가 있을 수 있습니다. 애플리케이션의 예외 클래스 중 하나에 `context` 메서드를 정의하면, 해당 예외의 로그 항목에 추가되어야 하는 관련 데이터를 지정할 수 있습니다.

```php
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

<!-- Sometimes you may need to report an exception but continue handling the current request. The `report` helper function allows you to quickly report an exception without rendering an error page to the user: -->
때로는 예외를 보고해야 하지만 현재 요청 처리는 계속해야 할 수 있습니다. `report` 헬퍼 함수는 사용자에게 오류 페이지를 렌더링하지 않고 예외를 빠르게 보고할 수 있게 해줍니다.

```php
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
애플리케이션 전반에서 `report` 함수를 사용하고 있다면, 가끔 같은 예외를 여러 번 보고하여 로그에 중복 항목이 생길 수 있습니다.

<!-- If you would like to ensure that a single instance of an exception is only ever reported once, you may invoke the `dontReportDuplicates` exception method in your application's `bootstrap/app.php` file: -->
하나의 예외 인스턴스가 반드시 한 번만 보고되도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출할 수 있습니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

<!-- Now, when the `report` helper is called with the same instance of an exception, only the first call will be reported: -->
이제 동일한 예외 인스턴스로 `report` 헬퍼를 호출하면 첫 번째 호출만 보고됩니다.

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

<!-- When messages are written to your application's [logs](/docs/13.x/logging), the messages are written at a specified [log level](/docs/13.x/logging#log-levels), which indicates the severity or importance of the message being logged. -->
애플리케이션의 [logs](/docs/13.x/logging)에 메시지가 작성될 때, 메시지는 지정된 [log level](/docs/13.x/logging#log-levels)로 기록됩니다. 로그 레벨은 기록되는 메시지의 심각도나 중요도를 나타냅니다.

<!-- As noted above, even when you register a custom exception reporting callback using the `report` method, Laravel will still log the exception using the default logging configuration for the application; however, since the log level can sometimes influence the channels on which a message is logged, you may wish to configure the log level that certain exceptions are logged at. -->
앞서 언급했듯이 `report` 메서드를 사용하여 사용자 정의 예외 보고 콜백을 등록하더라도, Laravel은 애플리케이션의 기본 로깅 설정을 사용하여 예외를 계속 로그에 기록합니다. 하지만 로그 레벨은 메시지가 기록되는 채널에 영향을 줄 수 있으므로, 특정 예외가 어떤 로그 레벨로 기록될지 설정하고 싶을 수 있습니다.

<!-- To accomplish this, you may use the `level` exception method in your application's `bootstrap/app.php` file. This method receives the exception type as its first argument and the log level as its second argument: -->
이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 예외 타입을, 두 번째 인수로 로그 레벨을 받습니다.

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
<!-- ### Ignoring Exceptions by Type -->
### Ignoring Exceptions by Type

<!-- When building your application, there will be some types of exceptions you never want to report. To ignore these exceptions, you may use the `dontReport` exception method in your application's `bootstrap/app.php` file. Any class provided to this method will never be reported; however, they may still have custom rendering logic: -->
애플리케이션을 만들다 보면 보고하고 싶지 않은 예외 타입이 있을 수 있습니다. 이러한 예외를 무시하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용할 수 있습니다. 이 메서드에 제공된 클래스는 절대 보고되지 않습니다. 다만 사용자 정의 렌더링 로직은 여전히 가질 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

<!-- Alternatively, you may simply "mark" an exception class with the `Illuminate\Contracts\Debug\ShouldntReport` interface. When an exception is marked with this interface, it will never be reported by Laravel's exception handler: -->
또는 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 간단히 "표시"할 수도 있습니다. 예외가 이 인터페이스로 표시되면 Laravel의 예외 핸들러가 절대 보고하지 않습니다.

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

<!-- If you need even more control over when a particular type of exception is ignored, you may provide a closure to the `dontReportWhen` method: -->
특정 타입의 예외를 언제 무시할지 더 세밀하게 제어해야 한다면, `dontReportWhen` 메서드에 클로저를 제공할 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```

<!-- Internally, Laravel already ignores some types of errors for you, such as exceptions resulting from 404 HTTP errors, 403 HTTP responses generated by origin mismatches, or 419 HTTP responses generated by invalid CSRF tokens. If you would like to instruct Laravel to stop ignoring a given type of exception, you may use the `stopIgnoring` exception method in your application's `bootstrap/app.php` file: -->
내부적으로 Laravel은 이미 일부 오류 타입을 무시합니다. 예를 들어 404 HTTP 오류로 인한 예외, origin 불일치로 생성된 403 HTTP 응답, 유효하지 않은 CSRF 토큰으로 생성된 419 HTTP 응답 등이 있습니다. Laravel이 특정 타입의 예외를 더 이상 무시하지 않도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다.

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
<!-- ### Rendering Exceptions -->
### Rendering Exceptions

<!-- By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this by using the `render` exception method in your application's `bootstrap/app.php` file. -->
기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해 줍니다. 하지만 특정 타입의 예외에 대해 사용자 정의 렌더링 클로저를 자유롭게 등록할 수 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용하면 됩니다.

<!-- The closure passed to the `render` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will determine what type of exception the closure renders by examining the type-hint of the closure: -->
`render` 메서드에 전달되는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이 인스턴스는 `response` 헬퍼를 통해 생성할 수 있습니다. Laravel은 클로저의 타입 힌트를 검사하여 해당 클로저가 어떤 타입의 예외를 렌더링하는지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

<!-- You may also use the `render` method to override the rendering behavior for built-in Laravel or Symfony exceptions such as `NotFoundHttpException`. If the closure given to the `render` method does not return a value, Laravel's default exception rendering will be utilized: -->
`render` 메서드를 사용하여 `NotFoundHttpException` 같은 Laravel 또는 Symfony 내장 예외의 렌더링 동작을 재정의할 수도 있습니다. `render` 메서드에 전달된 클로저가 값을 반환하지 않으면 Laravel의 기본 예외 렌더링이 사용됩니다.

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
})
```

<a name="rendering-exceptions-as-json"></a>
<!-- #### Rendering Exceptions as JSON -->
#### Rendering Exceptions as JSON

<!-- When rendering an exception, Laravel will automatically determine if the exception should be rendered as an HTML or JSON response based on the `Accept` header of the request. If you would like to customize how Laravel determines whether to render HTML or JSON exception responses, you may utilize the `shouldRenderJsonWhen` method: -->
예외를 렌더링할 때 Laravel은 요청의 `Accept` 헤더를 기준으로 예외를 HTML 응답으로 렌더링할지 JSON 응답으로 렌더링할지 자동으로 결정합니다. Laravel이 HTML 또는 JSON 예외 응답 중 무엇을 렌더링할지 결정하는 방식을 사용자 정의하고 싶다면 `shouldRenderJsonWhen` 메서드를 활용할 수 있습니다.

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```

<a name="customizing-the-exception-response"></a>
<!-- #### Customizing the Exception Response -->
#### Customizing the Exception Response

<!-- Rarely, you may need to customize the entire HTTP response rendered by Laravel's exception handler. To accomplish this, you may register a response customization closure using the `respond` method: -->
드물게 Laravel 예외 핸들러가 렌더링하는 전체 HTTP 응답을 사용자 정의해야 할 수 있습니다. 이를 위해 `respond` 메서드를 사용하여 응답 사용자 정의 클로저를 등록할 수 있습니다.

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
})
```

<a name="renderable-exceptions"></a>
<!-- ### Reportable and Renderable Exceptions -->
### Reportable and Renderable Exceptions

<!-- Instead of defining custom reporting and rendering behavior in your application's `bootstrap/app.php` file, you may define `report` and `render` methods directly on your application's exceptions. When these methods exist, they will automatically be called by the framework: -->
애플리케이션의 `bootstrap/app.php` 파일에서 사용자 정의 보고 및 렌더링 동작을 정의하는 대신, 애플리케이션의 예외 클래스에 직접 `report`와 `render` 메서드를 정의할 수 있습니다. 이러한 메서드가 존재하면 프레임워크가 자동으로 호출합니다.

```php
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
     * Render the exception as an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

<!-- If your exception extends an exception that is already renderable, such as a built-in Laravel or Symfony exception, you may return `false` from the exception's `render` method to render the exception's default HTTP response: -->
예외가 Laravel 또는 Symfony 내장 예외처럼 이미 렌더링 가능한 예외를 확장하는 경우, 예외의 기본 HTTP 응답을 렌더링하려면 예외의 `render` 메서드에서 `false`를 반환할 수 있습니다.

```php
/**
 * Render the exception as an HTTP response.
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
예외에 특정 조건이 충족될 때만 필요한 사용자 정의 보고 로직이 포함되어 있다면, Laravel이 때로는 기본 예외 처리 설정을 사용하여 예외를 보고하도록 지시해야 할 수 있습니다. 이를 위해 예외의 `report` 메서드에서 `false`를 반환할 수 있습니다.

```php
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
> `report` 메서드에 필요한 의존성을 타입 힌트로 지정할 수 있으며, Laravel의 [service container](/docs/13.x/container)가 해당 의존성을 메서드에 자동으로 주입합니다.

<a name="throttling-reported-exceptions"></a>
<!-- ### Throttling Reported Exceptions -->
### Throttling Reported Exceptions

<!-- If your application reports a very large number of exceptions, you may want to throttle how many exceptions are actually logged or sent to your application's external error tracking service. -->
애플리케이션이 매우 많은 수의 예외를 보고한다면, 실제로 로그에 기록되거나 애플리케이션의 외부 오류 추적 서비스로 전송되는 예외 수를 제한하고 싶을 수 있습니다.

<!-- To take a random sample rate of exceptions, you may use the `throttle` exception method in your application's `bootstrap/app.php` file. The `throttle` method receives a closure that should return a `Lottery` instance: -->
예외를 무작위 샘플 비율로 처리하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. `throttle` 메서드는 `Lottery` 인스턴스를 반환해야 하는 클로저를 받습니다.

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

<!-- It is also possible to conditionally sample based on the exception type. If you would like to only sample instances of a specific exception class, you may return a `Lottery` instance only for that class: -->
예외 타입에 따라 조건부로 샘플링하는 것도 가능합니다. 특정 예외 클래스의 인스턴스만 샘플링하고 싶다면, 해당 클래스에 대해서만 `Lottery` 인스턴스를 반환하면 됩니다.
```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```

<!-- You may also rate limit exceptions logged or sent to an external error tracking service by returning a `Limit` instance instead of a `Lottery`. This is useful if you want to protect against sudden bursts of exceptions flooding your logs, for example, when a third-party service used by your application is down: -->
`Lottery` 대신 `Limit` 인스턴스를 반환하여 로그에 기록되거나 외부 오류 추적 서비스로 전송되는 예외에 속도 제한을 적용할 수도 있습니다. 예를 들어, 애플리케이션에서 사용하는 서드파티 서비스가 중단되어 예외가 갑자기 많이 발생하는 상황에서 로그가 폭주하지 않도록 보호하고 싶을 때 유용합니다.

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```

<!-- By default, limits will use the exception's class as the rate limit key. You can customize this by specifying your own key using the `by` method on the `Limit`: -->
기본적으로 제한은 예외의 클래스를 속도 제한 키로 사용합니다. `Limit`의 `by` 메서드를 사용해 직접 키를 지정하여 이를 사용자 정의할 수 있습니다.

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```

<!-- Of course, you may return a mixture of `Lottery` and `Limit` instances for different exceptions: -->
물론 서로 다른 예외에 대해 `Lottery`와 `Limit` 인스턴스를 함께 반환할 수도 있습니다.

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return match (true) {
            $e instanceof BroadcastException => Limit::perMinute(300),
            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
            default => Limit::none(),
        };
    });
})
```

<a name="http-exceptions"></a>
<!-- ## HTTP Exceptions -->
## HTTP Exceptions

<!-- Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401), or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper: -->
일부 예외는 서버의 HTTP 오류 코드를 설명합니다. 예를 들어 "페이지를 찾을 수 없음" 오류(404), "인가되지 않음" 오류(401), 또는 개발자가 발생시킨 500 오류일 수 있습니다. 애플리케이션 어디에서든 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다.

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
<!-- ### Custom HTTP Error Pages -->
### Custom HTTP Error Pages

<!-- Laravel makes it easy to display custom error pages for various HTTP status codes. For example, to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered for all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable: -->
Laravel은 다양한 HTTP 상태 코드에 대한 사용자 정의 오류 페이지를 쉽게 표시할 수 있게 해줍니다. 예를 들어 404 HTTP 상태 코드의 오류 페이지를 사용자 정의하려면 `resources/views/errors/404.blade.php` view 템플릿을 생성합니다. 이 view는 애플리케이션에서 생성된 모든 404 오류에 대해 렌더링됩니다. 이 디렉터리 안의 view는 해당하는 HTTP 상태 코드와 일치하도록 이름을 지정해야 합니다. `abort` 함수에서 발생한 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 view에 전달됩니다.

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

<!-- You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking: -->
`vendor:publish` Artisan 명령어를 사용하여 Laravel의 기본 오류 페이지 템플릿을 게시할 수 있습니다. 템플릿을 게시한 뒤에는 원하는 대로 사용자 정의할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
<!-- #### Fallback HTTP Error Pages -->
#### Fallback HTTP Error Pages

<!-- You may also define a "fallback" error page for a given series of HTTP status codes. This page will be rendered if there is not a corresponding page for the specific HTTP status code that occurred. To accomplish this, define a `4xx.blade.php` template and a `5xx.blade.php` template in your application's `resources/views/errors` directory. -->
특정 HTTP 상태 코드 계열에 대한 "대체" 오류 페이지를 정의할 수도 있습니다. 발생한 특정 HTTP 상태 코드에 해당하는 페이지가 없으면 이 페이지가 렌더링됩니다. 이를 위해 애플리케이션의 `resources/views/errors` 디렉터리에 `4xx.blade.php` 템플릿과 `5xx.blade.php` 템플릿을 정의합니다.

<!-- When defining fallback error pages, the fallback pages will not affect `404`, `500`, and `503` error responses since Laravel has internal, dedicated pages for these status codes. To customize the pages rendered for these status codes, you should define a custom error page for each of them individually. -->
대체 오류 페이지를 정의할 때, Laravel은 `404`, `500`, `503` 상태 코드에 대해 내부 전용 페이지를 가지고 있으므로 대체 페이지는 이러한 오류 응답에 영향을 주지 않습니다. 이러한 상태 코드에 대해 렌더링되는 페이지를 사용자 정의하려면 각각에 대해 별도의 사용자 정의 오류 페이지를 정의해야 합니다.
