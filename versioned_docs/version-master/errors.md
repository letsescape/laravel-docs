# 오류 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 보고](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [예외 타입별 무시하기](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [보고 및 렌더링이 가능한 예외](#renderable-exceptions)
- [예외 보고 제한하기](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새로운 Laravel 프로젝트를 시작하면 오류 및 예외 처리가 이미 기본적으로 설정되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php` 파일에서 `withExceptions` 메서드를 사용하여 예외가 애플리케이션에서 어떻게 보고되고 렌더링될지 관리할 수 있습니다.

`withExceptions` 클로저에 주어지는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션의 예외 처리를 담당합니다. 이 문서 전체에서 이 객체에 대해 더 자세히 설명하겠습니다.

<a name="configuration"></a>
## 설정

`config/app.php` 설정 파일에 있는 `debug` 옵션은 오류에 대한 정보가 사용자에게 얼마나 자세히 보여질지를 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

로컬 개발 환경에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **프로덕션 환경에서는 반드시 이 값을 `false`로 설정해야 합니다. 만약 프로덕션에서 `true`로 설정된다면, 민감한 설정 값들이 최종 사용자에게 노출될 위험이 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel에서 예외 보고는 예외를 로그로 남기거나 [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io)와 같은 외부 서비스로 전송하는 데 사용됩니다. 기본적으로는 [로깅](/docs/master/logging) 설정에 따라 예외가 로그로 기록됩니다. 하지만 원하는 방식대로 예외를 로그로 남길 수 있습니다.

다양한 종류의 예외를 각각 다르게 보고해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `report` 예외 메서드를 사용해 특정 타입의 예외가 보고될 때 실행할 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입힌트를 통해 어떤 예외를 처리할지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드를 사용해 사용자 지정 예외 보고 콜백을 등록하더라도, Laravel은 기본 로그 설정에 따라 예외를 계속 기록합니다. 예외가 기본 로깅 스택에 전달되는 것을 중단하고 싶다면, 보고 콜백 정의시 `stop` 메서드를 호출하거나 콜백에서 `false`를 반환하면 됩니다.

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
> 특정 예외에 대한 보고 방식을 커스터마이즈하려면, [보고 및 렌더링이 가능한 예외](/docs/master/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전체 로그 컨텍스트(Global Log Context)

Laravel은 가능하다면 현재 사용자의 ID를 모든 예외의 로그 메시지에 컨텍스트 데이터로 자동 추가합니다. 또한, 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용해 자체 글로벌 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션에서 기록하는 모든 예외 로그 메시지에 포함됩니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외별 로그 컨텍스트

모든 로그 메시지에 동일한 컨텍스트를 추가하는 것이 유용할 수 있지만, 때때로 특정 예외만의 고유한 컨텍스트를 로그에 포함하고 싶을 수 있습니다. 애플리케이션 내 특정 예외 클래스에 `context` 메서드를 정의하면, 해당 예외에 관한 필요 데이터를 로그 항목에 추가할 수 있습니다.

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보를 반환합니다.
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
#### `report` 헬퍼

간혹 예외를 보고하되 현재 요청 처리는 계속 이어가야 할 때가 있습니다. `report` 헬퍼 함수는 사용자에게 오류 페이지를 보여주지 않고 빠르게 예외를 보고할 수 있게 해줍니다.

```php
public function isValid(string $value): bool
{
    try {
        // 값을 유효성 검증...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 예외 중복 보고 방지

애플리케이션에서 `report` 함수를 자주 사용하다 보면, 동일한 예외 인스턴스를 여러 번 보고하여 로그에 중복 항목이 생길 수 있습니다.

단일 예외 인스턴스가 한 번만 보고되도록 하려면, `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출할 수 있습니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

이제 동일한 예외 인스턴스로 `report` 헬퍼가 여러 번 호출되어도, 첫 번째 호출만 보고되고 나머지는 무시됩니다.

```php
$original = new RuntimeException('Whoops!');

report($original); // 보고됨

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // 무시됨
}

report($original); // 무시됨
report($caught); // 무시됨
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨

[로그](/docs/master/logging)에 메시지가 기록될 때, 해당 메시지는 특정 [로그 레벨](/docs/master/logging#log-levels)로 기록됩니다. 로그 레벨은 기록되는 메시지의 심각도나 중요도를 나타냅니다.

앞서 설명했듯, `report` 메서드를 사용해 사용자 지정 예외 보고 콜백을 등록하더라도 Laravel은 기본 로그 설정에 따라 예외를 기록합니다. 그러나 로그 레벨에 따라 메시지가 기록되는 채널이 달라질 수 있기 때문에, 특정 예외가 어떤 레벨로 기록될지 지정하고 싶을 때가 있습니다.

이럴 경우, `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 예외 타입을 첫 번째 인수로, 로그 레벨을 두 번째 인수로 받습니다.

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 예외 타입별 무시하기

애플리케이션을 개발할 때, 일부 예외는 결코 보고하지 않으려는 경우도 있습니다. 이러한 예외는 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용해 무시할 수 있습니다. 이 메서드에 지정한 클래스의 예외는 절대 보고되지 않지만, 사용자 지정 렌더링 로직은 적용될 수 있습니다.

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는, 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스만 구현해도 해당 예외는 Laravel의 예외 핸들러에 의해 결코 보고되지 않습니다.

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

특정 타입의 예외가 언제 무시될지 더 세밀하게 제어하려면, `dontReportWhen` 메서드에 클로저를 전달할 수 있습니다.

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

Laravel 내부적으로는 이미 404 HTTP 오류에서 발생한 예외, 출처(origin) 불일치로 인해 생성된 403 HTTP 응답, 잘못된 CSRF 토큰으로 인해 생성된 419 HTTP 응답 등 일부 오류는 자동으로 무시됩니다. 특정 예외 타입을 무시하지 않도록 지시하려면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다.

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 변환해줍니다. 그러나 원하는 경우, 특정 타입의 예외에 대해 자체 렌더링 클로저를 등록할 수 있습니다. 이를 위해 `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용하면 됩니다.

`render` 메서드에 전달되는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 통해 어떤 예외 타입을 처리할지 결정합니다.

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

내장 Laravel 혹은 Symfony 예외(`NotFoundHttpException` 등)의 렌더링 동작도 `render` 메서드를 이용해 오버라이드할 수 있습니다. 만약 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다.

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
#### 예외를 JSON으로 렌더링하기

예외를 렌더링할 때 Laravel은 요청의 `Accept` 헤더에 따라 예외를 HTML 또는 JSON 응답으로 자동 변환합니다. 만약 Laravel이 HTML 또는 JSON 예외 응답을 렌더링할지 결정하는 방식을 커스터마이즈하고 싶다면, `shouldRenderJsonWhen` 메서드를 활용하십시오.

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
#### 예외 응답 전체 커스터마이징

드물지만, Laravel의 예외 핸들러가 렌더링하는 전체 HTTP 응답을 커스터마이즈해야 할 때가 있습니다. 이럴 땐 `respond` 메서드를 사용해 응답 커스터마이징 클로저를 등록할 수 있습니다.

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
### 보고 및 렌더링이 가능한 예외

애플리케이션의 `bootstrap/app.php` 파일에서 사용자 지정 로직을 정의하는 대신, 예외 클래스 내에 직접 `report` 및 `render` 메서드를 정의할 수도 있습니다. 이 메서드들이 존재하면, 프레임워크가 자동으로 호출하게 됩니다.

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외를 보고합니다.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * 예외를 HTTP 응답으로 렌더링합니다.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 렌더링 기능이 있는 Laravel 내장 예외나 Symfony 예외를 상속한 예외의 경우, 예외 클래스의 `render` 메서드에서 `false`를 반환하면 기본 HTTP 응답을 렌더링합니다.

```php
/**
 * 예외를 HTTP 응답으로 렌더링합니다.
 */
public function render(Request $request): Response|bool
{
    if (/** 예외가 커스텀 렌더링이 필요한 경우 */) {

        return response(/* ... */);
    }

    return false;
}
```

특정 조건에서만 커스텀 로직이 필요하고, 나머지는 기본 예외 처리 방식을 따라야 한다면, `report` 메서드에서 `false`를 반환하면 됩니다.

```php
/**
 * 예외를 보고합니다.
 */
public function report(): bool
{
    if (/** 예외가 커스텀 보고가 필요한 경우 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 의존성이 있다면, Laravel의 [서비스 컨테이너](/docs/master/container)를 통해 자동으로 주입받을 수 있습니다.

<a name="throttling-reported-exceptions"></a>
### 예외 보고 제한하기

애플리케이션에서 매우 많은 예외가 보고되는 경우, 실제로 로그를 남기거나 외부 오류 추적 서비스에 전송되는 예외의 수를 제한(쓰로틀링)하고 싶을 수 있습니다.

무작위 샘플링 방식으로 예외를 제한하려면, `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. 이 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 인수로 받습니다.

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

예외 타입에 따라 조건부 샘플링도 가능합니다. 예를 들어, 특정 예외 클래스에 대해서만 샘플링을 적용하고 싶다면 그 클래스에 대해서만 `Lottery` 인스턴스를 반환하면 됩니다.

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

또는, `Lottery` 대신 `Limit` 인스턴스를 반환하여 외부 추적 서비스로 전송되거나 로그에 기록되는 예외를 단위 시간당 횟수로 제한할 수 있습니다. 예를 들어, 애플리케이션이 사용하는 외부 서비스가 다운되었을 때, 갑작스럽게 로그가 폭주하는 것을 막기에 유용합니다.

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

기본적으로 제한 키(rate limit key)는 예외 클래스가 사용됩니다. 별도의 키를 사용하려면, `Limit`의 `by` 메서드로 지정할 수 있습니다.

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

물론, 상황에 따라 예외마다 `Lottery`, `Limit`을 혼용해서 반환할 수도 있습니다.

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
## HTTP 예외

일부 예외는 서버에서 발생한 HTTP 오류 코드를 설명합니다. 예를 들어 "페이지를 찾을 수 없음" 오류(404), "인증되지 않은 오류"(401), 또는 개발자가 생성한 500 오류 등이 있습니다. 이러한 응답을 애플리케이션의 어떤 위치에서든 쉽게 생성하려면, `abort` 헬퍼를 사용하면 됩니다.

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 오류 페이지

Laravel은 다양한 HTTP 상태 코드에 맞는 커스텀 오류 페이지를 쉽게 표시할 수 있게 해줍니다. 예를 들어, 404 HTTP 상태 코드용 오류 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 파일을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 오류에서 렌더링됩니다. 이 디렉터리 내의 뷰 파일 이름은 HTTP 상태 코드와 동일해야 합니다. `abort` 함수에 의해 발생한 `Symfony\Component\HttpKernel\Exception.HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다.

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 오류 페이지 템플릿은 `vendor:publish` Artisan 명령어로 발행할 수 있습니다. 템플릿을 발행한 후에는 필요에 따라 자유롭게 커스터마이즈할 수 있습니다.

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 오류 페이지

특정 HTTP 상태 코드에 대한 페이지가 없을 경우를 대비해 "폴백" 오류 페이지를 정의할 수도 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php`, `5xx.blade.php` 템플릿을 만들어 놓으면 됩니다.

폴백 오류 페이지를 정의하더라도, 404, 500, 503 오류 응답에는 영향을 주지 않습니다. Laravel은 이 상태 코드에 대해 내부적으로 전용 페이지를 가지고 있기 때문입니다. 이러한 상태 코드에 대한 페이지를 커스터마이즈하려면, 각각에 맞는 오류 페이지를 개별적으로 작성해야 합니다.