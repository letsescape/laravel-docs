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
<a id="logging" data-translation-alias="true"></a>
<!-- ## Introduction -->
## Introduction

<!-- When you start a new Laravel project, error and exception handling is already configured for you. The `App\Exceptions\Handler` class is where all exceptions thrown by your application are logged and then rendered to the user. We'll dive deeper into this class throughout this documentation. -->
새로운 Laravel 프로젝트를 시작하면, 에러 및 예외 처리가 이미 기본적으로 설정되어 있습니다. 모든 예외는 `App\Exceptions\Handler` 클래스에서 로그로 기록되고, 이후 사용자에게 표시되는 응답으로 렌더링됩니다. 이 문서에서는 해당 클래스를 좀 더 자세히 살펴봅니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 설정 파일의 `debug` 옵션은 실제로 사용자에게 에러에 대한 정보가 얼마나 표시될지 결정합니다. 이 옵션은 기본적으로 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따라가도록 설정되어 있습니다.

<!-- During local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the value is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 프로덕션 환경에서 이 값이 `true`로 되어 있으면, 사용자에게 민감한 설정 정보가 노출될 수 있으니 주의해야 합니다.**

<a name="the-exception-handler"></a>
<!-- ## The Exception Handler -->
## The Exception Handler

<a name="reporting-exceptions"></a>
<!-- ### Reporting Exceptions -->
### Reporting Exceptions

<!-- All exceptions are handled by the `App\Exceptions\Handler` class. This class contains a `register` method where you may register custom exception reporting and rendering callbacks. We'll examine each of these concepts in detail. Exception reporting is used to log exceptions or send them to an external service like [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com) or [Sentry](https://github.com/getsentry/sentry-laravel). By default, exceptions will be logged based on your [logging](/docs/8.x/logging) configuration. However, you are free to log exceptions however you wish. -->
모든 예외는 `App\Exceptions\Handler` 클래스에서 처리됩니다. 이 클래스에는 `register` 메서드가 있으며, 여기서 커스텀 예외 보고 및 렌더링 콜백을 등록할 수 있습니다. 이 개념들의 작동 방식을 하나씩 자세히 살펴보겠습니다. 예외 보고는 예외를 로그로 남기거나, [Flare](https://flareapp.io), [Bugsnag](https://bugsnag.com), [Sentry](https://github.com/getsentry/sentry-laravel)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로 모든 예외는 [logging](/docs/8.x/logging) 구성에 따라 기록됩니다. 하지만 예외를 기록하는 방식은 자유롭게 변경할 수 있습니다.

<!-- For example, if you need to report different types of exceptions in different ways, you may use the `reportable` method to register a closure that should be executed when an exception of a given type needs to be reported. Laravel will deduce what type of exception the closure reports by examining the type-hint of the closure: -->
예를 들어, 다양한 유형의 예외마다 각기 다른 방법으로 처리해야 한다면, `reportable` 메서드를 사용하여 특정 예외 타입에 대해 실행할 클로저를 등록할 수 있습니다. Laravel은 해당 클로저의 타입힌트를 분석하여 어떤 예외 타입을 보고하는지 자동으로 판단합니다.

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
`reportable` 메서드를 통해 커스텀 예외 보고 콜백을 등록하더라도, Laravel은 이 예외를 기본 로깅 구성에 따라 그대로 기록합니다. 만약 예외가 기본 로깅 스택으로 전파되는 것을 중지하려면, 콜백 정의 시 `stop` 메서드를 사용하거나, 콜백에서 `false`를 반환하면 됩니다.

```
$this->reportable(function (InvalidOrderException $e) {
    //
})->stop();

$this->reportable(function (InvalidOrderException $e) {
    return false;
});
```

> [!TIP]
> 특정 예외에 대한 예외 보고를 맞춤화하려면 [reportable exceptions](/docs/8.x/errors#renderable-exceptions) 기능을 활용할 수도 있습니다.

<a name="global-log-context"></a>
<!-- #### Global Log Context -->
#### Global Log Context

<!-- If available, Laravel automatically adds the current user's ID to every exception's log message as contextual data. You may define your own global contextual data by overriding the `context` method of your application's `App\Exceptions\Handler` class. This information will be included in every exception's log message written by your application: -->
Laravel은, 가능할 경우 현재 로그인한 사용자의 ID를 모든 예외 로그 메시지의 컨텍스트 정보로 자동 추가합니다. 만약 직접 전역 컨텍스트 정보를 추가하고 싶다면, 애플리케이션의 `App\Exceptions\Handler` 클래스에서 `context` 메서드를 오버라이드하면 됩니다. 이 메서드에서 반환한 정보는 애플리케이션이 기록하는 모든 예외 로그 메시지에 포함됩니다.

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
모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 어떤 예외는 해당 예외에만 적용되는 고유한 추가 정보가 필요할 수 있습니다. 이럴 때는, 커스텀 예외 클래스 내부에 `context` 메서드를 정의하면 해당 예외의 로그 엔트리에 추가 정보를 포함시킬 수 있습니다.

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
특정 예외를 로그로 기록하면서도, 별도의 에러 페이지를 렌더링하지 않고 현재 요청을 계속 처리하고 싶은 경우가 있습니다. 이럴 때는 `report` 헬퍼 함수를 사용하면 예외 핸들러를 통해 빠르게 예외를 보고할 수 있습니다.

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
애플리케이션을 개발하다 보면, 특정 예외 타입은 아예 보고하지 않고 무시하고 싶은 경우가 있을 수 있습니다. 예외 핸들러 클래스에는 `$dontReport` 프로퍼티가 있는데, 기본적으로는 빈 배열입니다. 여기에 추가한 클래스들은 예외가 발행되어도 로그로 기록되지 않습니다. 하지만, 커스텀 렌더링 로직은 여전히 적용할 수 있습니다.

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
> 실제로 Laravel은 이미 여러 유형의 에러(예: 404 HTTP "찾을 수 없음" 예외, 419 CSRF 토큰 오류 등)에 대해 자동으로 보고를 무시하고 있습니다.

<a name="rendering-exceptions"></a>
<!-- ### Rendering Exceptions -->
### Rendering Exceptions

<!-- By default, the Laravel exception handler will convert exceptions into an HTTP response for you. However, you are free to register a custom rendering closure for exceptions of a given type. You may accomplish this via the `renderable` method of your exception handler. -->
Laravel의 예외 핸들러는 기본적으로 예외를 HTTP 응답으로 변환해줍니다. 하지만, 특정 예외 타입에 대한 응답을 직접 정의하고 싶다면, 예외 핸들러에서 `renderable` 메서드를 사용해 커스텀 렌더링 클로저를 등록할 수 있습니다.

<!-- The closure passed to the `renderable` method should return an instance of `Illuminate\Http\Response`, which may be generated via the `response` helper. Laravel will deduce what type of exception the closure renders by examining the type-hint of the closure: -->
`renderable` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 분석해 어떤 예외를 처리하는지 자동으로 파악합니다.

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
또한, `renderable` 메서드를 사용하면 `NotFoundHttpException`과 같은 Laravel 혹은 Symfony의 기본 예외 렌더링을 오버라이드할 수도 있습니다. 만약 `renderable` 메서드에 전달된 클로저가 아무 값도 반환하지 않으면, Laravel의 기본 예외 렌더링 방식이 그대로 적용됩니다.

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
예외 핸들러의 `register` 메서드에서 예외 타입을 확인(type-checking)하는 대신, 커스텀 예외 안에 `report` 및 `render` 메서드를 직접 정의할 수도 있습니다. 이 메서드들이 존재하면, 프레임워크가 자동으로 호출합니다.

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
만약 여러분의 예외가 이미 렌더링 기능을 제공하는 Laravel 또는 Symfony의 기본 예외를 상속받고 있다면, 커스텀 `render` 메서드에서 `false`를 반환하여 예외의 기본 HTTP 응답 렌더링을 그대로 사용할 수도 있습니다.

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
예외가 특정 조건에서만 커스텀 보고 로직을 필요로 하고, 그렇지 않을 때는 기본 예외 처리 방식을 따르려면, `report` 메서드에서 `false`를 반환하면 됩니다.

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
> `report` 메서드에 필요한 의존성을 타입힌트하면, Laravel의 [service container](/docs/8.x/container)에서 자동으로 주입해줍니다.

<a name="mapping-exceptions-by-type"></a>
<!-- ### Mapping Exceptions By Type -->
### Mapping Exceptions By Type

<!-- Sometimes, third-party libraries used by your application may throw exceptions that you wish to make [renderable](#renderable-exceptions), but are unable to do so because you do not have control over the definitions of third-party exceptions. -->
애플리케이션에서 사용하는 서드파티 라이브러리가 던지는 예외에 자신만의 [renderable](#renderable-exceptions) 처리를 적용하고 싶지만, 해당 예외 클래스를 직접 수정할 수 없는 경우가 있을 수 있습니다.

<!-- Thankfully, Laravel allows you to conveniently map these exceptions to other exception types that you manage within your application. To accomplish this, call the `map` method from your exception handler's `register` method: -->
이때, Laravel의 예외 핸들러에서는 이런 외부 예외를 애플리케이션에서 직접 관리하는 다른 예외 타입으로 손쉽게 매핑할 수 있습니다. 이를 위해, 예외 핸들러의 `register` 메서드에서 `map` 메서드를 호출하면 됩니다.

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
만약 매핑된 예외를 생성하는 과정을 더 세밀하게 제어하고 싶다면, `map` 메서드에 클로저를 전달할 수도 있습니다.

```
use League\Flysystem\Exception;
use App\Exceptions\FilesystemException;

$this->map(fn (Exception $e) => new FilesystemException($e));
```

<a name="http-exceptions"></a>
<!-- ## HTTP Exceptions -->
## HTTP Exceptions

<!-- Some exceptions describe HTTP error codes from the server. For example, this may be a "page not found" error (404), an "unauthorized error" (401) or even a developer generated 500 error. In order to generate such a response from anywhere in your application, you may use the `abort` helper: -->
일부 예외는 서버에서 발생한 HTTP 에러 코드를 나타냅니다. 예를 들어, "페이지를 찾을 수 없음"(404), "인증되지 않음"(401), 개발자가 의도적으로 발생시키는 500 에러 등이 여기에 해당합니다. 이런 응답을 애플리케이션 어디에서든 쉽게 생성하려면 `abort` 헬퍼를 사용할 수 있습니다.

```
abort(404);
```

<a name="custom-http-error-pages"></a>
<!-- ### Custom HTTP Error Pages -->
### Custom HTTP Error Pages

<!-- Laravel makes it easy to display custom error pages for various HTTP status codes. For example, if you wish to customize the error page for 404 HTTP status codes, create a `resources/views/errors/404.blade.php` view template. This view will be rendered on all 404 errors generated by your application. The views within this directory should be named to match the HTTP status code they correspond to. The `Symfony\Component\HttpKernel\Exception\HttpException` instance raised by the `abort` function will be passed to the view as an `$exception` variable: -->
Laravel은 다양한 HTTP 상태 코드를 위한 커스텀 오류 페이지를 쉽게 만들 수 있도록 지원합니다. 예를 들어, 404 HTTP 상태 코드에 대한 오류 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 파일을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉터리 안의 각 뷰 파일명은 해당 HTTP 상태 코드와 일치해야 합니다. 또, `abort` 함수로 발생시킨 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스가 `$exception` 변수로 뷰에 전달됩니다.

```
<h2>{{ $exception->getMessage() }}</h2>
```

<!-- You may publish Laravel's default error page templates using the `vendor:publish` Artisan command. Once the templates have been published, you may customize them to your liking: -->
Laravel의 기본 오류 페이지 템플릿을 배포(publish)하려면, `vendor:publish` Artisan 명령어를 사용할 수 있습니다. 템플릿을 배포한 후에는 원하는 대로 직접 수정할 수 있습니다.

```
php artisan vendor:publish --tag=laravel-errors
```
