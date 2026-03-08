# 로깅 (Logging)

- [소개](#introduction)
- [설정](#configuration)
    - [사용 가능한 채널 드라이버](#available-channel-drivers)
    - [채널 전제조건](#channel-prerequisites)
    - [사용 중단 경고 로깅](#logging-deprecation-warnings)
- [로그 스택 구성하기](#building-log-stacks)
- [로그 메시지 작성하기](#writing-log-messages)
    - [컨텍스트 정보](#contextual-information)
    - [특정 채널에 기록하기](#writing-to-specific-channels)
- [Monolog 채널 커스터마이징](#monolog-channel-customization)
    - [채널별 Monolog 커스터마이징](#customizing-monolog-for-channels)
    - [Monolog 핸들러 채널 생성하기](#creating-monolog-handler-channels)
    - [팩토리를 통한 커스텀 채널 생성](#creating-custom-channels-via-factories)
- [Pail을 사용한 로그 메시지 실시간 확인](#tailing-log-messages-using-pail)
    - [설치](#pail-installation)
    - [사용법](#pail-usage)
    - [로그 필터링](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내에서 어떤 일이 일어나고 있는지 더 잘 이해할 수 있도록, Laravel은 파일, 시스템 에러 로그, 그리고 팀 전체에 알림을 보낼 수 있는 Slack 등 다양한 장소에 로그 메시지를 기록할 수 있는 강력한 로깅 서비스를 제공합니다.

Laravel의 로깅은 "채널(channels)" 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 단일 로그 파일에 기록하는 반면, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

내부적으로 Laravel은 다양한 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. 이러한 핸들러의 설정을 매우 쉽게 할 수 있도록 도와주며, 여러 핸들러를 조합해 애플리케이션의 로그 처리를 맞춤 구성할 수 있습니다.

<a name="configuration"></a>
## 설정

애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 모여 있습니다. 이 파일에서 애플리케이션의 로그 채널을 구성할 수 있으니, 제공되는 여러 채널과 각 옵션을 꼼꼼히 확인하는 것이 좋습니다. 아래에서는 몇 가지 일반적인 옵션을 살펴보겠습니다.

기본적으로 Laravel은 로그 메시지 작성 시 `stack` 채널을 사용합니다. `stack` 채널은 여러 개의 로그 채널을 하나로 묶어 사용하기 위한 것입니다. 스택 구성에 관한 자세한 내용은 [아래 문서](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 "드라이버"로 동작합니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록될지를 결정합니다. 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버는 다음과 같습니다. 대부분의 드라이버에 대한 설정 항목이 이미 `config/logging.php`에 포함되어 있으므로 파일 내용을 꼭 확인해보세요:

<div class="overflow-auto">

| 이름          | 설명                                                                    |
| ------------ | ----------------------------------------------------------------------- |
| `custom`      | 지정된 팩토리를 호출해 채널을 생성하는 드라이버                            |
| `daily`       | 일별로 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버               |
| `errorlog`    | `ErrorLogHandler` 기반 Monolog 드라이버                                  |
| `monolog`     | Monolog 핸들러를 자유롭게 사용할 수 있는 Monolog 팩토리 드라이버           |
| `papertrail`  | `SyslogUdpHandler` 기반 Monolog 드라이버                                 |
| `single`      | 단일 파일 또는 경로 기반 로거 채널 (`StreamHandler`)                      |
| `slack`       | `SlackWebhookHandler` 기반 Monolog 드라이버                              |
| `stack`       | 여러 채널을 묶어 "멀티 채널"을 생성하기 위한 래퍼                          |
| `syslog`      | `SyslogHandler` 기반 Monolog 드라이버                                   |

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대해 더 알고 싶으면 [고급 채널 커스터마이징](#monolog-channel-customization) 문서를 확인하세요.

<a name="configuring-the-channel-name"></a>
#### 채널 이름 구성하기

기본적으로 Monolog 인스턴스는 현재 환경 이름(예: `production`, `local`)과 일치하는 "채널 이름"으로 생성됩니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 전제조건

<a name="configuring-the-single-and-daily-channels"></a>
#### single 및 daily 채널 설정하기

`single` 및 `daily` 채널은 `bubble`, `permission`, `locking` 세 가지 선택적 설정 항목을 지원합니다.

<div class="overflow-auto">

| 이름          | 설명                                                               | 기본값    |
| ------------ | ------------------------------------------------------------------ | -------- |
| `bubble`     | 메시지가 처리된 후 다른 채널로 전파(bubble)할지 여부를 나타냅니다.   | `true`   |
| `locking`    | 쓰기 전에 로그 파일 잠금 시도 여부                                   | `false`  |
| `permission` | 로그 파일의 퍼미션 (권한)                                           | `0644`   |

</div>

또한, `daily` 채널의 로그 보존 기간은 `LOG_DAILY_DAYS` 환경 변수나 `days` 설정 옵션으로 구성할 수 있습니다.

<div class="overflow-auto">

| 이름       | 설명                                            | 기본값 |
| ---------- | ----------------------------------------------- | ------ |
| `days`     | 일간 로그 파일을 몇 일간 보존할지 지정합니다.    | `14`   |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 구성

`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 일반적으로 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 지정할 수 있으며, 값을 얻으려면 [Papertrail 공식 문서](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)를 참고하세요.

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 구성

슬랙 채널에는 `url` 옵션이 필수입니다. 이는 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있으며, 해당 URL은 Slack 팀에 설정한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소와 일치해야 합니다.

기본적으로 Slack에는 `critical` 레벨 이상의 로그만 전달됩니다. 하지만 `LOG_LEVEL` 환경 변수나 Slack 로그 채널 설정 배열 내 `level` 옵션을 변경하여 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
### 사용 중단 경고 로깅

PHP, Laravel 및 다른 라이브러리들은 언제 제거될 예정인 기능 등에 대해 사용 중단(deprecation) 경고를 알리는 경우가 많습니다. 이러한 경고를 로그에 기록하고자 한다면, `LOG_DEPRECATIONS_CHANNEL` 환경 변수나 `config/logging.php` 설정 파일에 선호하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```

또는 `deprecations`라는 이름의 로그 채널을 직접 정의할 수도 있습니다. 만약 해당 이름의 채널이 존재하면, 항상 사용 중단 경고를 이 채널에 기록합니다:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```

<a name="building-log-stacks"></a>
## 로그 스택 구성하기

앞서 설명했듯, `stack` 드라이버는 여러 채널을 하나의 로그 채널로 묶어서 편리하게 쓸 수 있게 해줍니다. 실제 운영 환경에서 볼 수 있을 법한 예시 설정을 살펴보겠습니다:

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

위 설정을 하나씩 살펴봅니다. 먼저 `stack` 채널은 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 묶고 있습니다. 따라서 로그가 작성될 때 두 채널 모두 메시지를 로그할 기회를 갖게 됩니다. 하지만 아래 설명할 메시지 심각도 / "레벨"에 따라서 각 채널의 기록 여부가 결정됩니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예시에서 `syslog`와 `slack` 채널 설정에 동봉된 `level` 옵션을 눈여겨보세요. 이 옵션은 해당 채널이 로그를 기록하기 위한 최소 "레벨"을 정의합니다. Laravel의 로깅은 Monolog을 기반으로 하며, Monolog은 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 다음 8가지 로그 레벨을 지원합니다. 높은 심각도 순서대로: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

예를 들어, 다음과 같이 `debug` 레벨로 메시지를 로그했다고 가정합시다:

```php
Log::debug('An informational message.');
```

설정대로라면 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, `slack` 채널은 메시지가 `critical` 이상이 아니므로 Slack으로 전송하지 않습니다. 반면, 아래와 같이 `emergency` 메시지를 기록하면:

```php
Log::emergency('The system is down!');
```

`emergency`는 두 채널의 최소 레벨 기준보다 높으므로, 시스템 로그와 Slack 양쪽 모두에 메시지가 전송됩니다.

<a name="writing-log-messages"></a>
## 로그 메시지 작성하기

`Log` [파사드](/docs/12.x/facades)를 통해 로그에 내용을 기록할 수 있습니다. 앞에서 설명했듯, RFC 5424 기준 8가지 로그 레벨에 맞는 메서드가 제공됩니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**

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

이들 메서드를 사용해 각 레벨에 맞는 메시지를 기록할 수 있습니다. 기본적으로는 `logging` 설정 파일에 명시된 기본 로그 채널에 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 주어진 사용자의 프로필을 보여줍니다.
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
### 컨텍스트 정보

로그 메서드에는 로그 메시지와 함께 표시할 추가적인 컨텍스트 데이터를 배열로 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

특정 채널에 기록되는 모든 이후 로그에 포함될 공통 컨텍스트 정보를 지정할 수도 있습니다. 예를 들어, 애플리케이션에 들어오는 각 요청과 연관된 고유 요청 ID를 기록하고싶을 때, `Log` 파사드의 `withContext` 메서드를 사용할 수 있습니다.

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
     * 들어오는 요청을 처리합니다.
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

만약 모든 로그 채널에 걸쳐 공통 컨텍스트를 공유하고자 한다면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드는 현재 생성된 모든 채널과 이후 생성될 모든 채널에 컨텍스트 정보를 제공합니다.

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
     * 들어오는 요청을 처리합니다.
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
> 작업 큐(queued jobs)를 처리하는 중에도 로그 컨텍스트를 공유해야 한다면, [작업 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 기록하기

애플리케이션의 기본 로그 채널이 아닌 특정 채널에 메시지를 기록하고 싶을 때도 있습니다. 이 경우 `Log` 파사드의 `channel` 메서드를 사용해 구성 파일에 정의된 원하는 채널을 선택할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

또한, 여러 채널로 구성된 즉석 로그 스택을 만들어 쓸 수도 있습니다. 이때 `stack` 메서드를 사용하세요:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
#### 즉석 생성 채널 (On-Demand Channels)

구성 파일에 채널 설정이 없어도, 런타임 실행 시 설정 배열을 전달해 즉석 채널을 생성할 수도 있습니다. 이는 `Log` 파사드의 `build` 메서드를 통해 가능합니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

즉석 채널을 포함하는 스택을 만들고 싶다면, `stack` 메서드에 즉석 채널 인스턴스를 포함시키면 됩니다:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```

<a name="monolog-channel-customization"></a>
## Monolog 채널 커스터마이징

<a name="customizing-monolog-for-channels"></a>
### 채널별 Monolog 커스터마이징

기존 채널에서 Monolog 구성을 완전히 제어해야 하는 경우도 있습니다. 예를 들어, Laravel 기본 `single` 채널에서 사용하는 Monolog `FormatterInterface` 구현을 직접 설정하고 싶을 때가 그렇습니다.

먼저 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 직후 커스터마이징할 클래스들이 명시됩니다. 이러한 클래스들은 원하는 위치에 만들어도 무방합니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

이제 `tap` 옵션에서 지정한 클래스를 작성할 차례입니다. 클래스는 단 하나의 메서드 `__invoke`만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 받습니다. 이 인스턴스는 실제 내부 Monolog 인스턴스에 모든 메서드 호출을 프록시합니다:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * 주어진 로거 인스턴스를 커스터마이즈합니다.
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
> `tap`에 지정한 모든 클래스는 [서비스 컨테이너](/docs/12.x/container)가 자동으로 인스턴스 생성 및 의존성 주입을 처리합니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성하기

Monolog에는 다양한 [핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있지만, Laravel은 이 중 일부에 대한 기본 채널만 제공합니다. 경우에 따라 Laravel에서 제공하지 않는 특정 Monolog 핸들러를 단순히 사용하는 맞춤 채널을 만들고 싶을 수 있습니다. 이런 경우 `monolog` 드라이버를 사용하는 것이 편리합니다.

`monolog` 드라이버를 사용할 때에는 `handler` 설정으로 어떤 핸들러를 인스턴스화할지 지정합니다. 핸들러가 필요로 하는 생성자 인자는 `handler_with` 옵션을 통해 지정할 수 있습니다:

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
#### Monolog 포매터

`monolog` 드라이버를 사용할 경우 기본 포매터는 Monolog `LineFormatter`입니다. 그러나 `formatter` 및 `formatter_with` 설정을 활용해 핸들러에 전달할 포매터 타입을 커스터마이징할 수 있습니다:

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

만약 자체 포매터를 제공하는 핸들러라면, `formatter` 옵션에 `default` 값을 줄 수 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
#### Monolog 프로세서

Monolog은 로그 메시지가 기록되기 전 처리하는 프로세서도 지원합니다. 사용자가 직접 프로세서를 작성하거나, Monolog이 제공하는 [프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 활용할 수 있습니다.

`monolog` 드라이버에서 프로세서를 커스터마이징하려면 채널 설정에 `processors` 배열을 추가합니다:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // 간단한 문법...
        Monolog\Processor\MemoryUsageProcessor::class,

        // 옵션 포함...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog 인스턴스 생성과 구성을 완전 직접 제어하는 맞춤 채널을 만들고 싶다면, `config/logging.php`에 `custom` 드라이버 유형을 지정할 수 있습니다. 그리고 `via` 옵션에 Monolog 인스턴스를 생성할 팩토리 클래스명을 적어야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

`custom` 드라이버를 지정한 후에는 Monolog 인스턴스를 생성하는 클래스를 작성합니다. 이 클래스는 `__invoke` 메서드 하나만 필요하며, 이 메서드는 채널 설정 배열을 받아 Monolog `Logger` 인스턴스를 반환하면 됩니다:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * 커스텀 Monolog 인스턴스를 생성합니다.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```

<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용한 로그 메시지 실시간 확인

문제가 있을 때 디버깅하거나 특정 종류의 오류를 실시간 모니터링할 때 애플리케이션 로그를 실시간으로 확인(테일)해야 할 때가 많습니다.

Laravel Pail은 Laravel 애플리케이션의 로그 파일을 명령줄에서 간편하게 조회할 수 있는 패키지입니다. 일반적인 `tail` 명령과 달리 Pail은 Sentry나 Flare 같은 다양한 로그 드라이버와도 작동하며, 유용한 필터링 기능을 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png" alt="Pail 사용 예시 화면" />

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail 사용을 위해서는 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 필요합니다.

Composer를 이용해 개발 환경 전용 패키지로 Pail을 설치하세요:

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
### 사용법

로그 테일링을 시작하려면 `pail` 명령어를 실행하세요:

```shell
php artisan pail
```

출력 내용을 좀 더 자세히 보고 누락 없이 표시하려면 `-v` 옵션을 사용합니다:

```shell
php artisan pail -v
```

예외 스택 트레이스까지 최대 상세하게 표시하려면 `-vv` 옵션을 사용하세요:

```shell
php artisan pail -vv
```

로그 테일링을 종료하려면 언제든지 `Ctrl+C`로 중단할 수 있습니다.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그를 유형, 파일, 메시지, 스택 트레이스 내용 등으로 필터링할 때 사용합니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

메시지 내용만으로 로그를 필터링할 때 사용합니다:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

로그 [레벨](#log-levels)로 필터링할 때 사용합니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 상태에서 기록된 로그만 표시할 때는 사용자 ID를 `--user` 옵션에 넘깁니다:

```shell
php artisan pail --user=1
```