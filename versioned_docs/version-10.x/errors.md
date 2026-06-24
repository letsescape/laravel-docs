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
<a id="logging" data-translation-alias="true"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you start a new Laravel project, error and exception handling is already configured for you. The `App\Exceptions\Handler` class is where all exceptions thrown by your application are logged and then rendered to the user. We'll dive deeper into this class throughout this documentation. -->
새로운 Laravel 프로젝트를 시작하면 에러 및 예외 처리가 이미 기본적으로 설정되어 있습니다. 애플리케이션에서 발생하는 모든 예외는 `App\Exceptions\Handler` 클래스에서 기록(로그)되며, 이후 사용자에게 렌더링됩니다. 이 문서에서는 해당 클래스의 주요 동작에 대해 자세히 다룹니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 에러 발생 시 사용자에게 표시되는 정보의 상세 정도를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수 값을 따르게 설정되어 있습니다.

<!-- During local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the value is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **반면, 운영(프로덕션) 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 운영 환경에서 `true`로 설정하면, 애플리케이션의 중요 설정 정보가 사용자에게 노출될 위험이 있습니다.**

<a name="the-exception-handler"></a>
<!-- ## The Exception Handler -->
## The Exception Handler

<a name="reporting-exceptions"></a>
<!-- ### Reporting Exceptions -->
### Reporting Exceptions

<!-- All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/10.x/logging) configuration. However, you are free to log exceptions however you wish. -->
모든 예외 처리는 `App\Exceptions\Handler` 클래스에서 담당합니다. 이 클래스에는 예외를 보고하거나 렌더링하는 커스텀 콜백을 등록할 수 있는 `register` 메서드가 있습니다. 아래에서 각 개념을 자세히 살펴봅니다. 예외 보고란 예외를 로그로 남기거나, [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel)와 같은 외부 서비스로 전송하는 것을 의미합니다. 기본적으로는 여러분의 [logging](/docs/10.x/logging)에 따라 예외가 기록됩니다. 하지만 원한다면 예외를 원하는 방식으로 직접 기록할 수도 있습니다.

<!-- If you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will determine what type of exception the closure reports by examining the type-hint of the closure: -->
각기 다른 타입의 예외를 다양하게 처리하고 싶다면, `reportable` 메서드를 사용하여 특정 타입의 예외가 보고될 때 실행되는 클로저를 등록할 수 있습니다. Laravel은 이 클로저의 타입-힌트를 참고하여 어떤 타입의 예외를 처리할지 결정합니다:

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
`reportable` 메서드로 커스텀 예외 보고 콜백을 등록해도 Laravel은 여전히 기본 로그 설정에 따라 예외를 기록합니다. 만약 이 예외가 더 이상 기본 로그 스택에 전파되지 않도록 하려면, 리포팅 콜백 정의 시 `stop` 메서드를 체이닝하거나, 콜백에서 `false`를 반환하면 됩니다:

```
$this->reportable(function (InvalidOrderException $e) {
    // ...
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!NOTE]
> 특정 예외의 리포팅 동작을 커스터마이징하고 싶을 경우, [reportable exceptions](/docs/10.x/errors#renderable-exceptions) 기능을 활용할 수도 있습니다.

<a name="global-log-context"></a>
<!-- #### Global Log Context -->
#### Global Log Context

<!-- If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by defining a `context` method on your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application: -->
가능하다면, Laravel은 현재 사용자 ID를 예외 로그 메시지의 컨텍스트 데이터로 자동 추가합니다. 여러분이 애플리케이션의 `App\Exceptions\Handler` 클래스에 `context` 메서드를 정의하면 원하는 전역 컨텍스트 정보를 추가할 수 있습니다. 이 정보는 애플리케이션이 작성하는 모든 예외 로그 메시지에 포함됩니다:

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
모든 로그에 컨텍스트를 추가하는 것도 유용하지만, 어떤 예외는 해당 예외만의 고유한 정보를 로그에 남기고 싶을 수 있습니다. 애플리케이션의 예외 클래스 중 하나에 `context` 메서드를 정의하면, 해당 예외에만 관련된 데이터를 로그 기록에 추가할 수 있습니다:

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
때로는 예외를 보고는 하되, 현재 요청 처리를 계속 이어가고 싶을 때가 있습니다. 이럴 때 `report` 헬퍼 함수를 사용하면 에러 페이지를 사용자에게 보여주지 않고도 에러 핸들러를 통해 빠르게 예외를 기록할 수 있습니다:

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
애플리케이션 곳곳에서 `report` 함수를 사용하다 보면 동일한 예외가 여러 번 보고되어 로그에 중복 기록되는 일이 생길 수 있습니다.

<!-- If you would like to ensure that a single instance of an exception is only ever reported once, you may set the `$withoutDuplicates` property to `true` within your application's `App\Exceptions\Handler` class: -->
특정 예외 인스턴스가 단 한 번만 보고되게 하고 싶다면, 애플리케이션의 `App\Exceptions\Handler` 클래스에 `$withoutDuplicates` 속성을 `true`로 설정하면 됩니다:

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
이제 `report` 헬퍼로 동일한 예외 인스턴스를 여러 번 호출하더라도, 최초 한 번만 기록됩니다:

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
애플리케이션의 [logs](/docs/10.x/logging)에 메시지를 기록할 때, 해당 메시지는 특정 [log level](/docs/10.x/logging#log-levels)로 분류되어 저장됩니다. 로그 레벨은 해당 메시지의 중요도나 심각도를 나타냅니다.

<!-- As noted above, even when you register a custom exception reporting callback using the `reportable` method, Laravel will still log the exception using the default logging configuration for the application; however, since the log level can sometimes influence the channels on which a message is logged, you may wish to configure the log level that certain exceptions are logged at. -->
앞서 설명한 것처럼, `reportable` 메서드로 커스텀 예외 보고 콜백을 등록하더라도 Laravel은 여전히 기본 로그 설정에 따라 예외를 기록합니다. 하지만 로그 레벨에 따라 메시지가 기록되는 채널이 달라질 수 있으므로, 예외별로 로그 레벨을 지정해야 할 때가 있습니다.

<!-- To accomplish this, you may define a `$levels` property on your application's exception handler. This property should contain an array of exception types and their associated log levels: -->
이럴 때는 예외 핸들러에서 `$levels` 속성을 정의하면 됩니다. 이 속성에는 예외 타입별로 대응되는 로그 레벨을 배열 형태로 지정합니다:

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
애플리케이션 제작 시 어떤 예외는 아예 보고하지 않게 하고 싶을 수 있습니다. 이런 예외들은 예외 핸들러의 `$dontReport` 속성에 추가하면 됩니다. 여기에 지정된 클래스의 예외는 로그로 기록되지 않으며, 필요에 따라 렌더링은 별도로 처리할 수 있습니다:

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
Laravel 내부적으로도 404 HTTP 에러나 잘못된 CSRF 토큰으로 인한 419 응답과 같이, 일부 예외는 이미 자동으로 무시하고 있습니다. 만약 특정 예외의 "무시" 동작을 취소하고 싶다면, 예외 핸들러의 `register` 메서드 안에서 `stopIgnoring` 메서드를 사용하면 됩니다:

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
기본적으로 Laravel의 예외 핸들러는 예외를 HTTP 응답으로 자동 변환합니다. 하지만 원하는 경우 특정 타입의 예외에 대해 직접 커스텀 렌더링 클로저를 등록할 수도 있습니다. 이때는 예외 핸들러에서 `renderable` 메서드를 사용하면 됩니다.

<!-- The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will determine what type of exception the closure renders by examining the type-hint of the closure: -->
`renderable` 메서드에 전달된 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 보통 `response` 헬퍼로 생성합니다. Laravel은 클로저의 타입-힌트를 참고하여 어떤 예외를 렌더링할지 판단합니다:

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
또한, `NotFoundHttpException`과 같은 Laravel 또는 Symfony의 내장 예외에 대해서도 `renderable` 메서드를 사용하여 렌더링 동작을 오버라이드할 수 있습니다. 만약 `renderable`로 전달된 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

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
예외 핸들러의 `register` 메서드 외에도, 각 예외 클래스 자체에 `report` 및 `render` 메서드를 직접 정의할 수 있습니다. 이러한 메서드가 존재하면 프레임워크에서 자동으로 호출해줍니다:

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
예외가 이미 렌더링 가능한(예: Laravel 또는 Symfony의 내장 예외 등) 예외를 확장하는 경우, 예외 클래스의 `render` 메서드에서 `false`를 반환하면 기본 HTTP 응답이 렌더링됩니다:

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
예외에 커스텀 보고 로직이 있으며 특정 조건에서만 적용해야 할 경우, 예외의 `report` 메서드에서 `false`를 반환하면 Laravel의 기본 예외 처리 설정대로 동작시킬 수 있습니다:

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
> `report` 메서드에서 필요한 의존성을 타입-힌트하면, Laravel의 [service container](/docs/10.x/container)에서 자동으로 주입해줍니다.

<a name="throttling-reported-exceptions"></a>
<!-- ### Throttling Reported Exceptions -->
### Throttling Reported Exceptions

<!-- If your application reports a very large number of exceptions, you may want to throttle how many exceptions are actually logged or sent to your application's external error tracking service. -->
애플리케이션에서 대량의 예외가 발생해 로그나 외부 에러 추적 서비스로 너무 많이 전송되는 상황을 막고 싶을 수 있습니다.

<!-- To take a random sample rate of exceptions, you can return a `Lottery` instance from your exception handler's `throttle` method. If your `App\Exceptions\Handler` class does not contain this method, you may simply add it to the class: -->
예외의 일부만 무작위로 기록하려면, 예외 핸들러의 `throttle` 메서드에서 `Lottery` 인스턴스를 반환하면 됩니다. 만약 `App\Exceptions\Handler` 클래스에 이 메서드가 없다면, 새로 추가하면 됩니다:

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
예외 타입에 따라 조건부로 샘플링할 수도 있습니다. 예를 들어, 특정 예외 클래스만 샘플링하려면 해당 클래스에만 `Lottery` 인스턴스를 반환하면 됩니다:

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
외부 에러 추적 서비스로 전송하거나 로그에 기록하는 비율을 조정하고 싶다면, `Lottery` 대신 `Limit` 인스턴스를 반환할 수도 있습니다. 이 방법은, 예를 들어 서드파티 서비스가 다운되어 대량의 예외가 발생할 때 로그가 넘쳐나는 것을 방지하는 데 유용합니다:

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
기본적으로 Laravel은 예외 클래스명을 기준으로 rate limit 키를 사용합니다. 직접 원하는 키로 설정할 수도 있는데, 이때는 `Limit`의 `by` 메서드를 사용하면 됩니다:

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
물론, 예외 종류마다 `Lottery`와 `Limit`을 조합해서 사용할 수 있습니다:

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
어떤 예외는 서버의 HTTP 에러 코드를 나타냅니다. 예를 들어 "페이지를 찾을 수 없음" (404), "권한 없음" (401), 또는 개발자가 직접 발생시킨 500 에러 등이 이에 해당합니다. 애플리케이션 어디에서든 이러한 응답을 발생시키려면 `abort` 헬퍼를 사용할 수 있습니다:

```
abort(404);
```

<a name="custom-http-error-pages"></a>
<!-- ### Custom HTTP Error Pages -->
### Custom HTTP Error Pages

<!-- Laravel makes it easy to display custom error pages for various HTTP status codes. For example, to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered for all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable: -->
Laravel은 다양한 HTTP 상태 코드에 맞춰 사용자 정의 에러 페이지를 쉽게 만들 수 있게 해줍니다. 예를 들어, 404 상태 코드에 대한 에러 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 파일을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉터리 내의 뷰 파일 이름은 해당 HTTP 상태 코드와 일치해야 합니다. 또한, `abort` 함수로 발생시킨 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다:

```
<h2>{{ $exception->getMessage() }}</h2>
```

<!-- You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking: -->
Laravel의 기본 에러 페이지 템플릿을 `vendor:publish` 아티즌 명령어로 퍼블리시할 수 있습니다. 템플릿을 퍼블리시한 뒤 원하는 대로 수정하세요:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
<!-- #### Fallback HTTP Error Pages -->
#### Fallback HTTP Error Pages

<!-- You may also define a "fallback" error page for a given series of HTTP status codes. This page will be rendered if there is not a corresponding page for the specific HTTP status code that occurred. To accomplish this, define a `4xx.blade.php` template and a `5xx.blade.php` template in your application's `resources/views/errors` directory. -->
특정 HTTP 상태 코드에 해당하는 에러 페이지가 없을 경우를 대비하여, 각 HTTP 오류 범위에 대한 "폴백" 에러 페이지도 정의할 수 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php` 와 `5xx.blade.php` 템플릿을 만들어 두세요.
