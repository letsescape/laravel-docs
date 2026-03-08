# 에러 처리 (Error Handling)

- [소개](#introduction)
- [설정](#configuration)
- [예외 처리](#handling-exceptions)
    - [예외 리포팅](#reporting-exceptions)
    - [예외 로그 레벨](#exception-log-levels)
    - [타입별 예외 무시](#ignoring-exceptions-by-type)
    - [예외 렌더링](#rendering-exceptions)
    - [리포터블 & 렌더러블 예외](#renderable-exceptions)
- [예외 리포트 제한(Throttling)](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
    - [커스텀 HTTP 에러 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개 (Introduction)

새로운 Laravel 프로젝트를 시작하면, 에러 및 예외 처리가 이미 기본적으로 구성되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php` 내에서 `withExceptions` 메서드를 사용하여 예외가 리포팅(report)되고 렌더링(render)되는 방식을 직접 관리할 수 있습니다.

`withExceptions` 클로저에 전달되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions`의 인스턴스이며, 애플리케이션의 예외 처리 전체를 담당합니다. 이 문서에서는 이 객체의 구성과 활용법에 대해 자세히 설명합니다.

<a name="configuration"></a>
## 설정 (Configuration)

`config/app.php` 설정 파일의 `debug` 옵션은 사용자에게 에러에 대한 정보가 얼마나 표시되는지 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따릅니다.

개발 환경(local)에서는 `APP_DEBUG` 환경 변수를 `true`로 설정해야 합니다. **운영(프로덕션) 환경에서는 반드시 이 값을 `false`로 설정해야 하며, 만약 `true`로 되어 있으면 애플리케이션의 중요한 설정 정보가 사용자에게 노출될 수 있습니다.**

<a name="handling-exceptions"></a>
## 예외 처리 (Handling Exceptions)

<a name="reporting-exceptions"></a>
### 예외 리포팅 (Reporting Exceptions)

Laravel에서 예외 리포팅은 예외를 로그로 남기거나 [Sentry](https://github.com/getsentry/sentry-laravel), [Flare](https://flareapp.io)와 같은 외부 서비스로 전송할 때 사용합니다. 기본적으로는 [로깅](/docs/12.x/logging) 설정에 따라 예외가 기록되지만, 원한다면 다른 방법으로 리포팅할 수도 있습니다.

서로 다른 예외 타입에 대해 각기 다른 방식으로 리포트하려면, `bootstrap/app.php` 내에서 `report` 예외 메서드를 사용하여 해당 예외 타입에 대한 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입힌트를 검사하여 어느 타입의 예외를 리포트할지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

`report` 메서드를 통해 커스텀 예외 리포팅 콜백을 등록해도 Laravel은 여전히 기본 로깅 설정을 통해 예외를 기록합니다. 만약 예외가 기본 로깅 스택까지 전달되지 않도록 하려면, 리포팅 콜백 정의 시 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환하면 됩니다:

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
> 특정 예외의 리포팅 방식을 커스터마이즈하려면 [리포터블 예외](/docs/12.x/errors#renderable-exceptions) 기능도 활용할 수 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트 (Global Log Context)

가능한 경우, Laravel은 현재 사용자 ID를 모든 예외 로그 메시지의 부가 정보로 자동 추가합니다. `bootstrap/app.php` 파일 내에서 `context` 예외 메서드를 사용하여 직접 원하는 전역 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션에서 작성한 모든 예외 로그 메시지에 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```

<a name="exception-log-context"></a>
#### 예외 개별 로그 컨텍스트 (Exception Log Context)

모든 로그 메시지에 컨텍스트를 추가하는 것도 유용하지만, 경우에 따라 특정 예외와 관련된 추가 컨텍스트 정보를 로그에 포함하고 싶을 수 있습니다. 애플리케이션의 특정 예외 클래스에 `context` 메서드를 정의하면, 해당 예외가 로그에 기록될 때마다 이 메서드에서 반환하는 데이터가 포함됩니다:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * 예외의 컨텍스트 정보 반환
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
#### `report` 헬퍼 (The `report` Helper)

때로는 예외를 리포트해야 하지만 현재 요청 처리는 계속 이어가고 싶을 수 있습니다. 이런 경우 `report` 헬퍼 함수를 사용하면 에러 페이지를 렌더링하지 않고도 예외만 빠르게 리포트할 수 있습니다:

```php
public function isValid(string $value): bool
{
    try {
        // 값을 유효성 검사...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```

<a name="deduplicating-reported-exceptions"></a>
#### 중복 예외 리포트 방지 (Deduplicating Reported Exceptions)

애플리케이션 곳곳에서 `report` 함수를 사용하다 보면, 동일한 예외가 여러 번 리포트되어 로그에 중복 기록될 수 있습니다.

특정 예외 인스턴스를 한 번만 리포트하도록 하고 싶다면, `bootstrap/app.php` 파일 내에서 `dontReportDuplicates` 예외 메서드를 호출하세요:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```

이제 하나의 예외 인스턴스가 여러 번 리포트될 경우, 최초 한 번만 기록됩니다:

```php
$original = new RuntimeException('Whoops!');

report($original); // 기록됨

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // 무시됨
}

report($original); // 무시됨
report($caught); // 무시됨
```

<a name="exception-log-levels"></a>
### 예외 로그 레벨 (Exception Log Levels)

애플리케이션의 [로그](/docs/12.x/logging)에 메시지가 쓰일 때, 해당 메시지는 [로그 레벨](/docs/12.x/logging#log-levels)과 함께 기록되어 중요도 또는 심각도를 나타냅니다.

앞서 설명했듯, 커스텀 예외 리포팅 콜백을 등록해도 Laravel은 기본 로깅 설정을 통해 예외를 기록합니다. 하지만 로그 레벨에 따라 메시지가 기록되는 채널이 달라질 수 있으므로, 특정 예외가 어떤 로그 레벨로 기록될지 설정이 필요할 수 있습니다.

이때 `bootstrap/app.php` 파일 내에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 예외 타입과 로그 레벨을 각각 첫 번째, 두 번째 인자로 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```

<a name="ignoring-exceptions-by-type"></a>
### 타입별 예외 무시 (Ignoring Exceptions by Type)

애플리케이션을 만들다 보면, 절대 리포트하지 않고 싶은 예외 타입이 있을 수 있습니다. 이런 예외는 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드로 무시할 수 있습니다. 이 메서드에 지정된 클래스들은 리포트 대상에서 제외됩니다. 단, 렌더링 커스텀 로직은 계속 적용할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```

또는 예외 클래스에 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스를 구현하여 "마킹"할 수도 있습니다. 이 인터페이스를 구현한 예외는 Laravel 예외 핸들러에서 절대 리포트되지 않습니다:

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

특정 조건이 성립할 때만 예외를 무시하고 싶다면, `dontReportWhen` 메서드에 클로저를 전달하면 됩니다:

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

Laravel 내부적으로도 이미 일부 예외(예: 404 HTTP 에러, 잘못된 CSRF 토큰으로 인한 419 응답 등)는 자동 무시 대상입니다. 만약 Laravel이 무시하고 있는 특정 예외 타입을 무시하지 않도록(즉, 항상 리포트하도록) 변경하고 싶다면, `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```

<a name="rendering-exceptions"></a>
### 예외 렌더링 (Rendering Exceptions)

기본적으로 Laravel 예외 핸들러는 예외를 HTTP 응답으로 자동 변환합니다. 하지만 특정 예외 타입에 대해 직접 커스텀 렌더링 클로저를 등록할 수도 있습니다. `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용하면 가능합니다.

`render` 메서드에 전달하는 클로저는 `Illuminate\Http\Response` 인스턴스를 반환해야 하며, 이는 `response` 헬퍼로 쉽게 생성할 수 있습니다. Laravel은 클로저의 타입힌트를 보고 어떤 예외를 렌더링할지 결정합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```

이 방식은 `NotFoundHttpException` 등 Laravel 또는 Symfony의 내장 예외에 대해서도 적용할 수 있습니다. 만약 `render` 메서드에 전달된 클로저가 값을 반환하지 않으면, Laravel의 기본 예외 렌더링이 사용됩니다:

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
#### 예외의 JSON 렌더링 (Rendering Exceptions as JSON)

예외를 렌더링할 때 Laravel은 요청의 `Accept` 헤더를 기준으로 HTML 혹은 JSON 응답을 자동 결정합니다. 만약 이 판단 로직을 커스텀하고 싶다면, `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

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
#### 예외 응답 전체 커스터마이즈 (Customizing the Exception Response)

드물게, 예외 핸들러가 렌더링하는 전체 HTTP 응답을 커스터마이즈해야 할 때가 있습니다. 이때는 `respond` 메서드에 클로저를 등록할 수 있습니다:

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
### 리포터블 & 렌더러블 예외 (Reportable and Renderable Exceptions)

예외별 커스텀 리포팅, 렌더링 동작을 `bootstrap/app.php` 파일이 아니라, 개별 예외 클래스 안에서 직접 정의할 수도 있습니다. 예외 클래스에 `report` 및 `render` 메서드가 있으면 Laravel이 자동으로 호출합니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * 예외 리포트
     */
    public function report(): void
    {
        // ...
    }

    /**
     * 예외를 HTTP 응답으로 렌더링
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```

이미 렌더러블 예외(예: Laravel 또는 Symfony 내장 예외)를 상속 중이라면, `render` 메서드에서 `false`를 반환하여 해당 예외의 기본 HTTP 응답 렌더링을 사용하도록 할 수 있습니다:

```php
/**
 * 예외를 HTTP 응답으로 렌더링
 */
public function render(Request $request): Response|bool
{
    if (/** 예외의 커스텀 렌더링 필요 여부 판단 */) {

        return response(/* ... */);
    }

    return false;
}
```

조건 만족 시에만 커스텀 리포팅이 필요하다면, `report` 메서드에서 `false`를 반환하여 Laravel의 기본 예외 핸들링을 사용하도록 할 수 있습니다:

```php
/**
 * 예외 리포트
 */
public function report(): bool
{
    if (/** 예외의 커스텀 리포팅 필요 여부 판단 */) {

        // ...

        return true;
    }

    return false;
}
```

> [!NOTE]
> `report` 메서드에 필요한 의존성은 타입힌트만 하면 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 예외 리포트 제한(Throttling) (Throttling Reported Exceptions)

애플리케이션에서 정말 많은 양의 예외를 리포트해야 하는 경우, 실제로 로그로 기록하거나 외부 에러 트래킹 서비스로 보내는 예외의 양을 제한하고 싶을 수 있습니다.

무작위 샘플링 비율로 예외를 제한하려면 `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용하는 것이 좋습니다. 이 메서드는 `Lottery` 인스턴스를 반환하는 클로저를 받습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```

특정 예외 타입에 대해서만 조건부로 샘플링할 수도 있습니다. 예를 들어, 특정 예외 클래스에 대해서만 `Lottery` 인스턴스를 반환하면 됩니다:

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

또한, `Lottery` 대신 `Limit` 인스턴스를 반환하여 외부 서비스로 전송되는 예외의 속도를 제한(rate limit)할 수도 있습니다. 예를 들어, 외부 서비스 장애 시 예외 폭주로 인해 로그가 쏟아지는 것을 방지하려는 경우 유용합니다:

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

기본적으로 제한 키(rate limit key)는 예외의 클래스를 사용합니다. 직접 키를 커스터마이즈하려면 `Limit`의 `by` 메서드를 사용하면 됩니다:

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

물론 예외별로 `Lottery`와 `Limit`을 섞어 조합할 수도 있습니다:

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
## HTTP 예외 (HTTP Exceptions)

일부 예외는 서버의 HTTP 에러 코드를 나타냅니다. 예를 들어, "페이지를 찾을 수 없음"(404), "권한 없음"(401), 또는 개발자가 의도적으로 발생시킨 500 에러 등이 있습니다. 애플리케이션 어디에서든 다음과 같이 `abort` 헬퍼를 사용해 이런 응답을 생성할 수 있습니다:

```php
abort(404);
```

<a name="custom-http-error-pages"></a>
### 커스텀 HTTP 에러 페이지 (Custom HTTP Error Pages)

Laravel은 다양한 HTTP 상태 코드 별 커스텀 에러 페이지를 쉽게 만들 수 있도록 지원합니다. 예를 들어, 404 상태 코드용 에러 페이지를 커스터마이즈하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하세요. 이 뷰는 애플리케이션에서 발생하는 모든 404 에러에 대해 렌더링됩니다. 이 디렉터리 내의 뷰 파일명은 각 HTTP 상태 코드와 일치해야 합니다. `abort` 함수에서 발생한 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```

Laravel의 기본 에러 페이지 템플릿은 `vendor:publish` Artisan 명령어로 퍼블리시할 수 있습니다. 퍼블리시 후, 원하는 대로 템플릿을 수정하세요:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 폴백 HTTP 에러 페이지 (Fallback HTTP Error Pages)

특정 HTTP 상태 코드에 맞는 별도 페이지가 없을 경우를 대비해, 일련의 상태 코드(예: 4xx, 5xx)용 "폴백" 에러 페이지를 정의할 수도 있습니다. 이를 위해 `resources/views/errors` 디렉터리에 `4xx.blade.php`와 `5xx.blade.php` 템플릿을 각각 생성하면 됩니다.

폴백 에러 페이지는 `404`, `500`, `503` 상태 코드에 대해서는 영향이 없습니다. Laravel 내부적으로 각 코드에 대한 전용 페이지가 있기 때문입니다. 이 상태 코드들에 대해 커스텀 페이지를 만들고 싶다면, 개별적으로 에러 페이지를 정의하세요.
