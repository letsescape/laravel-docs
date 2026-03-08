# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널별 사전 준비 사항](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구축](#building-log-stacks)
- [로그 메시지 작성](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성](#creating-monolog-handler-channels)
    - [팩토리를 이용한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 확인](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션에서 무슨 일이 일어나고 있는지 더 잘 파악할 수 있도록, Laravel은 강력한 로깅 서비스를 제공합니다. 이를 통해 메시지를 파일, 시스템 에러 로그, 또는 Slack 등으로 기록하여 팀 전체에 알릴 수 있습니다.

Laravel의 로깅 시스템은 "채널(channel)"을 기반으로 작동합니다. 각 채널은 로그 정보를 기록하는 특정한 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 모든 로그를 저장하며, `slack` 채널은 Slack으로 로그 메시지를 전송합니다. 로그 메시지는 심각도(severity)에 따라 여러 채널로 동시에 기록될 수 있습니다.

Laravel 내부적으로는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 활용하며, 다양한 강력한 로그 핸들러를 지원합니다. Laravel에서는 이러한 핸들러 설정을 매우 쉽게 할 수 있으며, 이를 조합하여 애플리케이션의 로그 처리 방식을 자유롭게 맞춤화할 수 있습니다.

<a name="configuration"></a>
## 설정 (Configuration)

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 구성 파일에 정의되어 있습니다. 이 파일에서 애플리케이션의 로그 채널을 설정할 수 있으므로, 제공되는 각 채널과 옵션을 꼭 확인해 보시기 바랍니다. 아래에서 몇 가지 일반적인 옵션을 살펴보겠습니다.

기본적으로 Laravel은 메시지 기록 시 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어서 사용할 수 있는 기능을 제공합니다. 스택 구성에 대한 자세한 설명은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버 (Available Channel Drivers)

각 로그 채널은 "드라이버(driver)"로 구동됩니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록될지를 결정합니다. 모든 Laravel 애플리케이션에서는 다음과 같은 로그 채널 드라이버를 사용할 수 있습니다. 대부분의 드라이버는 `config/logging.php` 구성 파일에 기본적으로 포함되어 있으니, 이 파일을 확인해 드라이버별 옵션을 익혀 두세요.

<div class="overflow-auto">

| 이름           | 설명                                                                               |
| -------------- | ---------------------------------------------------------------------------------- |
| `custom`       | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버                                  |
| `daily`        | 일별로 로그 파일이 교체되는 `RotatingFileHandler` 기반 Monolog 드라이버            |
| `errorlog`     | 시스템 에러 로그에 기록하는 `ErrorLogHandler` 기반 Monolog 드라이버                |
| `monolog`      | Monolog에서 지원하는 어떤 핸들러도 사용 가능한 Monolog 팩토리 드라이버             |
| `papertrail`   | `SyslogUdpHandler` 기반 Monolog 드라이버                                            |
| `single`       | 하나의 파일 또는 경로에 로그를 기록하는 채널 (`StreamHandler`)                      |
| `slack`        | Slack으로 로그를 보내는 `SlackWebhookHandler` 기반 Monolog 드라이버                 |
| `stack`        | 여러 채널을 묶어주는 래퍼 역할의 드라이버                                          |
| `syslog`       | 시스템 로그에 기록하는 `SyslogHandler` 기반 Monolog 드라이버                        |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 자세한 내용은 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 설정

기본적으로 Monolog는 현재 환경(예: `production`, `local`)과 동일한 "채널 이름"으로 인스턴스화됩니다. 이 값을 변경하고 싶다면 해당 채널 설정에 `name` 옵션을 추가할 수 있습니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널별 사전 준비 사항 (Channel Prerequisites)

<a name="configuring-the-single-and-daily-channels"></a>
#### Single 및 Daily 채널 설정

`single` 및 `daily` 채널에는 선택적으로 `bubble`, `permission`, `locking` 세 가지 설정 옵션이 있습니다.

<div class="overflow-auto">

| 이름         | 설명                                                                        | 기본값    |
| ------------ | --------------------------------------------------------------------------- | --------- |
| `bubble`     | 메시지를 처리한 뒤 다른 채널로도 전파(bubble)할지 여부                      | `true`    |
| `locking`    | 로그 파일에 기록하기 전 파일을 잠글지 여부                                   | `false`   |
| `permission` | 로그 파일의 권한 설정                                                       | `0644`    |

</div>

또한, `daily` 채널의 로그 보관 기간은 `LOG_DAILY_DAYS` 환경 변수 또는 `days` 옵션으로 설정할 수 있습니다.

<div class="overflow-auto">

| 이름     | 설명                                                    | 기본값   |
| -------- | ------------------------------------------------------- | -------- |
| `days`   | 일별 로그 파일을 보관할 일 수                           | `14`     |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 설정

`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 이 값은 `PAPERTRAIL_URL`과 `PAPERTRAIL_PORT` 환경 변수로 정의할 수 있습니다. 해당 값은 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 설정

`slack` 채널을 사용하려면 `url` 설정이 필수입니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있으며, [Slack 인커밍 웹후크](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)에서 생성한 URL이어야 합니다.

기본적으로 Slack은 `critical` 수준 이상의 로그만 수신합니다. 물론 `LOG_LEVEL` 환경 변수나 Slack 채널 설정의 `level` 옵션을 변경해 수신 로그 레벨을 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅 (Logging Deprecation Warnings)

PHP, Laravel, 그 외 라이브러리들은 일부 기능이 더 이상 지원되지 않거나 이후 버전에서 제거될 예정임을 사용자에게 알리기 위해 "사용 중단(deprecation)" 경고를 남깁니다. 이러한 경고를 로깅하고 싶다면, 원하는 `deprecations` 로그 채널을 `LOG_DEPRECATIONS_CHANNEL` 환경 변수 또는 애플리케이션의 `config/logging.php` 파일에 지정하면 됩니다.

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는, `deprecations`라는 이름의 로그 채널을 별도로 정의해도 됩니다. 이렇게 채널을 생성하면, 해당 채널이 항상 사용 중단 경고 기록에 사용됩니다.

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구축 (Building Log Stacks)

앞서 언급한 대로, `stack` 드라이버를 사용하면 여러 채널을 하나의 로그 채널로 결합해서 사용할 수 있습니다. 프로덕션 환경에서 주로 볼 수 있는 예시 설정은 다음과 같습니다.

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'], // [tl! add]
        'ignore_exceptions' => false,
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => env('LOG_LEVEL', 'debug'),
        'facility' => env('LOG_SYSLOG_FACILITY', LOG_USER),
        'replace_placeholders' => true,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => env('LOG_SLACK_USERNAME', 'Laravel Log'),
        'emoji' => env('LOG_SLACK_EMOJI', ':boom:'),
        'level' => env('LOG_LEVEL', 'critical'),
        'replace_placeholders' => true,
    ],
],
```

이 설정을 하나씩 살펴보면, `stack` 채널이 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 묶는 것을 볼 수 있습니다. 따라서 로그 메시지가 발생하면 두 채널 모두에서 메시지를 기록할 기회를 갖게 됩니다. 다만, 실제로 메시지가 기록될지는 해당 채널의 심각도("레벨") 설정에 따라 달라집니다.

<a name="log-levels"></a>
#### 로그 레벨 (Log Levels)

위 예제에서 볼 수 있듯, `syslog` 및 `slack` 채널 설정에 `level` 옵션이 있습니다. 이 옵션은 해당 채널이 기록할 최소 "레벨"을 지정합니다. Laravel의 로깅 서비스의 기반이 되는 Monolog는 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 제공합니다. 심각도가 높은 순부터 나열하면: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

예를 들어, 다음처럼 `debug` 메서드를 사용해 로그를 남기면:

```php
Log::debug('An informational message.');
```

이 설정에서는 `syslog` 채널이 시스템 로그에 메시지를 기록하게 되지만, 해당 메시지가 `critical` 이상이 아니기 때문에 Slack에는 보내지지 않습니다. 하지만, `emergency` 레벨의 메시지를 기록하면, 두 채널 모두로 전송됩니다.

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
## 로그 메시지 작성 (Writing Log Messages)

로그를 작성하려면 `Log` [파사드](/docs/master/facades)를 사용합니다. 앞서 설명한 것처럼, 로거는 [RFC 5424 규격](https://tools.ietf.org/html/rfc5424)에 정의된 여덟 가지 로깅 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

```php
use Illuminate\Support\Facades\Log;

Log::emergency($message);
Log::alert($message);
Log::critical($message);
Log::error($message);
Log::warning($message);
Log::notice($message);
Log::info($message);
Log::debug($message);
```

해당 레벨의 메서드를 호출하면, 메시지가 그 레벨로 기록됩니다. 기본적으로는, 메시지가 `logging` 구성 파일에 설정된 기본 로그 채널에 남겨집니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        Log::info('Showing the user profile for user: {id}', ['id' => $id]);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

<a name="contextual-information"></a>
### 컨텍스트 정보 (Contextual Information)

로그 메서드에 컨텍스트 데이터를 배열로 전달할 수 있습니다. 이 데이터는 로그 메시지와 함께 포맷되어 기록됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널에서 이후의 모든 로그에 공통적으로 포함할 컨텍스트 정보를 지정하고 싶을 때가 있을 수 있습니다. 예를 들어, 들어오는 각 요청에 대해 고유한 요청 ID를 로그에 남기고 싶다면, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        $response = $next($request);

        $response->headers->set('Request-Id', $requestId);

        return $response;
    }
}
```

_모든_ 로깅 채널에 걸쳐 컨텍스트 정보를 공유하고 싶다면 `Log::shareContext()` 메서드를 호출하세요. 이 메서드는 이미 생성된 모든 채널은 물론, 이후 생성되는 채널에도 해당 컨텍스트 정보를 제공합니다.

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::shareContext([
            'request-id' => $requestId
        ]);

        // ...
    }
}
```

> [!NOTE]
> 큐 작업을 처리하는 동안 로그 컨텍스트를 공유해야 한다면, [잡 미들웨어](/docs/master/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기 (Writing to Specific Channels)

애플리케이션의 기본 채널이 아닌 다른 채널로 로그를 남기고 싶을 때, `Log` 파사드의 `channel` 메서드를 사용하면 됩니다. 이 메서드는 환경설정 파일에 정의된 채널을 반환합니다.

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

여러 채널로 구성된 로그 스택을 그때그때 만들고 싶다면 `stack` 메서드를 사용할 수도 있습니다.

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 온디맨드(즉시 생성) 채널

애플리케이션의 `logging` 설정 파일에 미리 정의되어 있지 않더라도, 실행 시점에 직접 설정을 전달해 온디맨드(즉시 생성) 채널을 만들 수 있습니다. 이를 위해 `Log` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다.

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

또한, 온디맨드로 생성한 채널을 다른 채널들과 함께 즉시 생성 스택에 포함시킬 수도 있습니다. 배열에 온디맨드 채널 인스턴스를 함께 전달하면 됩니다.

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이징 (Monolog Channel Customization)

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 커스터마이징 (Customizing Monolog for Channels)

기존 채널의 Monolog 설정을 완벽하게 제어해야 할 경우가 있습니다. 예를 들어, Laravel의 내장 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

시작하려면, 해당 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 후 커스터마이징할 기회를 갖는 클래스 목록을 넣습니다. 이 클래스들은 애플리케이션 내 원하는 위치(예: 별도 디렉터리)에 자유롭게 생성하면 됩니다.

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

이제 `tap` 옵션에 지정한 클래스를 만들어야 합니다. 이 클래스에는 오직 하나의 메서드만 있으면 됩니다: `__invoke`, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. 이 인스턴스는 내부적으로 Monolog 인스턴스로 모든 메서드 호출을 전달합니다.

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
     */
    public function __invoke(Logger $logger): void
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```

> [!NOTE]
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/master/container)에서 resolve되므로, 생성자에서 의존성을 주입받을 수 있습니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성 (Creating Monolog Handler Channels)

Monolog에는 매우 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 존재하지만, Laravel이 내장 채널로 전부를 지원하지는 않습니다. 따라서, Laravel에서 제공하지 않는 특정 Monolog 핸들러 인스턴스로 채널을 직접 생성하고 싶을 때가 있습니다. 이럴 때는 `monolog` 드라이버를 이용하면 됩니다.

`monolog` 드라이버에서는 `handler` 설정 옵션을 통해 사용할 핸들러 클래스를 지정합니다. 핸들러에 필요한 생성자 인자들은 `handler_with` 옵션에서 설정할 수 있습니다.

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'handler_with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a name="monolog-formatters"></a>
#### Monolog 포매터 (Monolog Formatters)

`monolog` 드라이버 사용 시 기본적으로 Monolog의 `LineFormatter`가 포매터로 지정됩니다. 하지만, `formatter` 및 `formatter_with` 옵션을 사용해 핸들러에 전달되는 포매터를 커스텀할 수 있습니다.

```php
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```

만약 사용 중인 Monolog 핸들러가 자체적으로 포매터 제공 능력을 갖췄다면, `formatter` 값을 `default`로 지정하면 됩니다.

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서 (Monolog Processors)

Monolog는 로그를 남기기 전에 메시지를 가공할 수 있도록 프로세서(processor) 기능을 지원합니다. 직접 프로세서를 만들거나, [Monolog에서 제공하는 내장 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수도 있습니다.

`monolog` 드라이버의 프로세서를 커스텀하고 싶다면, `processors` 설정 항목을 추가하세요.

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 형태...
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션과 함께...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 이용한 커스텀 채널 생성 (Creating Custom Channels via Factories)

Monolog의 인스턴스화와 설정 과정을 완전히 직접 제어하고 싶은 경우, `config/logging.php` 구성 파일에서 `custom` 드라이버 타입을 지정할 수 있습니다. 이 설정에는 Monolog 인스턴스를 생성할 팩토리 클래스 이름을 `via` 옵션으로 포함해야 합니다.

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버 채널을 설정했다면, Monolog 인스턴스를 생성할 클래스를 만들어야 합니다. 이 클래스에는 한 개의 `__invoke` 메서드만 있으면 되고, 이 메서드는 Monolog logger 인스턴스를 반환해야 합니다. 메서드는 채널 설정 배열을 인수로 받습니다.

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용한 로그 메시지 실시간 확인 (Tailing Log Messages Using Pail)

실제로 로그를 실시간으로 모니터링해야 할 일이 자주 있습니다. 예를 들어, 문제를 디버깅하거나, 특정 유형의 에러가 발생하는지 살펴볼 때 등입니다.

Laravel Pail은 커맨드라인에서 Laravel 애플리케이션의 로그 파일을 쉽게 확인할 수 있도록 해주는 패키지입니다. 표준 `tail` 명령어와 달리, Pail은 Sentry, Flare 등 어떤 로그 드라이버와도 함께 사용할 수 있도록 설계되었습니다. 또한, Pail은 원하는 정보를 빠르게 찾을 수 있도록 여러 유용한 필터 기능을 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
### 설치 (Installation)

> [!WARNING]
> Laravel Pail을 사용하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다.

시작하려면 Composer 패키지 매니저를 사용해 Pail을 프로젝트에 추가하세요.

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법 (Usage)

로그 실시간 확인을 시작하려면 `pail` 명령어를 실행하세요:

```shell
php artisan pail
```

출력의 상세 수준을 높이고 로그가 생략(…)되지 않도록 하려면 `-v` 옵션을 사용하세요.

```shell
php artisan pail -v
```

최고 수준의 상세 출력 및 예외 스택 트레이스 표시까지 원한다면 `-vv` 옵션을 사용하세요.

```shell
php artisan pail -vv
```

로그 확인을 중지하려면 언제든 `Ctrl+C`를 누르면 됩니다.

<a name="pail-filtering-logs"></a>
### 로그 필터링 (Filtering Logs)

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` 옵션을 사용해 로그의 유형, 파일, 메시지, 스택 트레이스 내용으로 로그를 필터링할 수 있습니다.

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

로그 메시지 내용만으로 필터링하려면 `--message` 옵션을 사용하세요.

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션을 사용해 [로그 레벨](#log-levels) 기준으로 로그를 필터링할 수 있습니다.

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 작성된 로그만 표시하고 싶을 때는, 해당 사용자의 ID를 `--user` 옵션에 전달하면 됩니다.

```shell
php artisan pail --user=1
```
