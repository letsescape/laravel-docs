<!-- # Logging -->
# Logging

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Available Channel Drivers](#available-channel-drivers)
    - [Channel Prerequisites](#channel-prerequisites)
    - [Logging Deprecation Warnings](#logging-deprecation-warnings)
- [Building Log Stacks](#building-log-stacks)
- [Writing Log Messages](#writing-log-messages)
    - [Contextual Information](#contextual-information)
    - [Writing to Specific Channels](#writing-to-specific-channels)
- [Monolog Channel Customization](#monolog-channel-customization)
    - [Customizing Monolog for Channels](#customizing-monolog-for-channels)
    - [Creating Monolog Handler Channels](#creating-monolog-handler-channels)
    - [Creating Custom Channels via Factories](#creating-custom-channels-via-factories)
- [Tailing Log Messages Using Pail](#tailing-log-messages-using-pail)
    - [Installation](#pail-installation)
    - [Usage](#pail-usage)
    - [Filtering Logs](#pail-filtering-logs)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To help you learn more about what's happening within your application, Laravel provides robust logging services that allow you to log messages to files, the system error log, and even to Slack to notify your entire team. -->
애플리케이션 내에서 어떤 일이 일어나고 있는지 더 잘 이해할 수 있도록, Laravel은 파일, 시스템 에러 로그, 그리고 팀 전체에 알림을 보낼 수 있는 Slack 등 다양한 장소에 로그 메시지를 기록할 수 있는 강력한 로깅 서비스를 제공합니다.

<!-- Laravel logging is based on "channels". Each channel represents a specific way of writing log information. For example, the `single` channel writes log files to a single log file, while the `slack` channel sends log messages to Slack. Log messages may be written to multiple channels based on their severity. -->
Laravel의 로깅은 "채널(channels)" 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 단일 로그 파일에 기록하는 반면, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수 있습니다.

<!-- Under the hood, Laravel utilizes the [Monolog](https://github.com/Seldaek/monolog) library, which provides support for a variety of powerful log handlers. Laravel makes it a cinch to configure these handlers, allowing you to mix and match them to customize your application's log handling. -->
내부적으로 Laravel은 다양한 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. 이러한 핸들러의 설정을 매우 쉽게 할 수 있도록 도와주며, 여러 핸들러를 조합해 애플리케이션의 로그 처리를 맞춤 구성할 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- All of the configuration options that control your application's logging behavior are housed in the `config/logging.php` configuration file. This file allows you to configure your application's log channels, so be sure to review each of the available channels and their options. We'll review a few common options below. -->
애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 모여 있습니다. 이 파일에서 애플리케이션의 로그 채널을 구성할 수 있으니, 제공되는 여러 채널과 각 옵션을 꼼꼼히 확인하는 것이 좋습니다. 아래에서는 몇 가지 일반적인 옵션을 살펴보겠습니다.

<!-- By default, Laravel will use the `stack` channel when logging messages. The `stack` channel is used to aggregate multiple log channels into a single channel. For more information on building stacks, check out the [documentation below](#building-log-stacks). -->
기본적으로 Laravel은 로그 메시지 작성 시 `stack` 채널을 사용합니다. `stack` 채널은 여러 개의 로그 채널을 하나로 묶어 사용하기 위한 것입니다. 스택 구성에 관한 자세한 내용은 [documentation below](#building-log-stacks)를 참고하세요.

<a name="available-channel-drivers"></a>
<!-- ### Available Channel Drivers -->
### Available Channel Drivers

<!-- Each log channel is powered by a "driver". The driver determines how and where the log message is actually recorded. The following log channel drivers are available in every Laravel application. An entry for most of these drivers is already present in your application's `config/logging.php` configuration file, so be sure to review this file to become familiar with its contents: -->
각 로그 채널은 "드라이버"로 동작합니다. 드라이버는 로그 메시지가 실제로 어떻게, 어디에 기록될지를 결정합니다. 모든 Laravel 애플리케이션에서 사용할 수 있는 로그 채널 드라이버는 다음과 같습니다. 대부분의 드라이버에 대한 설정 항목이 이미 `config/logging.php`에 포함되어 있으므로 파일 내용을 꼭 확인해보세요:

<div class="overflow-auto">

<!-- | Name | Description | | ------------ | -------------------------------------------------------------------- | | `custom` | A driver that calls a specified factory to create a channel. | | `daily` | A `RotatingFileHandler` based Monolog driver which rotates daily. | | `monthly` | A `RotatingFileHandler` based Monolog driver which rotates monthly. | | `errorlog` | An `ErrorLogHandler` based Monolog driver. | | `monolog` | A Monolog factory driver that may use any supported Monolog handler. | | `papertrail` | A `SyslogUdpHandler` based Monolog driver. | | `single` | A single file or path based logger channel (`StreamHandler`). | | `slack` | A `SlackWebhookHandler` based Monolog driver. | | `stack` | A wrapper to facilitate creating "multi-channel" channels. | | `syslog` | A `SyslogHandler` based Monolog driver. | -->
| 이름         | 설명                                                          |
| ------------ | ------------------------------------------------------------- |
| `custom`     | 지정한 팩토리를 호출해 채널을 생성하는 드라이버입니다.       |
| `daily`      | 매일 순환하는 `RotatingFileHandler` 기반 Monolog 드라이버입니다. |
| `monthly`    | 매월 순환하는 `RotatingFileHandler` 기반 Monolog 드라이버입니다. |
| `errorlog`   | `ErrorLogHandler` 기반 Monolog 드라이버입니다.                |
| `monolog`    | 지원되는 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버입니다. |
| `papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버입니다.              |
| `single`     | 단일 파일 또는 경로를 기반으로 하는 로거 채널(`StreamHandler`)입니다. |
| `slack`      | `SlackWebhookHandler` 기반 Monolog 드라이버입니다.            |
| `stack`      | "다중 채널" 채널을 쉽게 생성할 수 있도록 돕는 래퍼입니다.     |
| `syslog`     | `SyslogHandler` 기반 Monolog 드라이버입니다.                  |

</div>

> [!NOTE]
> 자세한 내용은 `monolog` 및 `custom` 드라이버에 대해 알아볼 수 있는 [advanced channel customization](#monolog-channel-customization) 문서를 참고하세요.

<a name="configuring-the-channel-name"></a>
<!-- #### Configuring the Channel Name -->
#### Configuring the Channel Name

<!-- By default, Monolog is instantiated with a "channel name" that matches the current environment, such as `production` or `local`. To change this value, you may add a `name` option to your channel's configuration: -->
기본적으로 Monolog 인스턴스는 현재 환경 이름(예: `production`, `local`)과 일치하는 "채널 이름"으로 생성됩니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다:

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
<!-- ### Channel Prerequisites -->
### Channel Prerequisites

<a name="configuring-the-single-daily-and-monthly-channels"></a>
<!-- #### Configuring the Single, Daily, and Monthly Channels -->
#### Configuring the Single, Daily, and Monthly Channels

<!-- The `single`, `daily`, and `monthly` channels have three optional configuration options: `bubble`, `permission`, and `locking`. -->
`single`, `daily`, `monthly` 채널에는 `bubble`, `permission`, `locking`이라는 세 가지 선택적 설정 옵션이 있습니다.

<div class="overflow-auto">

<!-- | Name | Description | Default | | ------------ | ----------------------------------------------------------------------------- | ------- | | `bubble` | Indicates if messages should bubble up to other channels after being handled. | `true` | | `locking` | Attempt to lock the log file before writing to it. | `false` | | `permission` | The log file's permissions. | `0644` | -->
| 이름        | 설명                                                                        | 기본값  |
| ----------- | --------------------------------------------------------------------------- | ------- |
| `bubble`    | 처리된 후 메시지를 다른 채널로 전파할지 나타냅니다.                        | `true`  |
| `locking`   | 로그 파일에 쓰기 전에 로그 파일을 잠그려고 시도합니다.                     | `false` |
| `permission` | 로그 파일의 권한입니다.                                                     | `0644`  |

</div>

<!-- Additionally, the retention policy for the `daily` and `monthly` channels can be configured via the `max_files` configuration option. The `LOG_DAILY_DAYS` environment variable may also be used to configure retention for the `daily` channel. -->
또한 `daily` 및 `monthly` 채널의 보존 정책은 `max_files` 설정 옵션으로 구성할 수 있습니다. `LOG_DAILY_DAYS` 환경 변수로 `daily` 채널의 보존 기간을 구성할 수도 있습니다.

<a name="configuring-the-papertrail-channel"></a>
<!-- #### Configuring the Papertrail Channel -->
#### Configuring the Papertrail Channel

<!-- The `papertrail` channel requires `host` and `port` configuration options. These may be defined via the `PAPERTRAIL_URL` and `PAPERTRAIL_PORT` environment variables. You can obtain these values from [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app). -->
`papertrail` 채널은 `host`와 `port` 설정이 필요합니다. 일반적으로 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수로 지정할 수 있으며, 값을 얻으려면 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)를 참고하세요.

<a name="configuring-the-slack-channel"></a>
<!-- #### Configuring the Slack Channel -->
#### Configuring the Slack Channel

<!-- The `slack` channel requires a `url` configuration option. This value may be defined via the `LOG_SLACK_WEBHOOK_URL` environment variable. This URL should match a URL for an [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) that you have configured for your Slack team. -->
`slack` 채널에는 `url` 옵션이 필수입니다. 이는 `LOG_SLACK_WEBHOOK_URL` 환경 변수로 지정할 수 있으며, 해당 URL은 Slack 팀에 설정한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소와 일치해야 합니다.

<!-- By default, Slack will only receive logs at the `critical` level and above; however, you can adjust this using the `LOG_LEVEL` environment variable or by modifying the `level` configuration option within your Slack log channel's configuration array. -->
기본적으로 Slack에는 `critical` 레벨 이상의 로그만 전달됩니다. 하지만 `LOG_LEVEL` 환경 변수나 Slack 로그 채널 설정 배열 내 `level` 옵션을 변경하여 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
<!-- ### Logging Deprecation Warnings -->
### Logging Deprecation Warnings

<!-- PHP, Laravel, and other libraries often notify their users that some of their features have been deprecated and will be removed in a future version. If you would like to log these deprecation warnings, you may specify your preferred `deprecations` log channel using the `LOG_DEPRECATIONS_CHANNEL` environment variable, or within your application's `config/logging.php` configuration file: -->
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

<!-- Or, you may define a log channel named `deprecations`. If a log channel with this name exists, it will always be used to log deprecations: -->
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
<!-- ## Building Log Stacks -->
## Building Log Stacks

<!-- As mentioned previously, the `stack` driver allows you to combine multiple channels into a single log channel for convenience. To illustrate how to use log stacks, let's take a look at an example configuration that you might see in a production application: -->
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

<!-- Let's dissect this configuration. First, notice our `stack` channel aggregates two other channels via its `channels` option: `syslog` and `slack`. So, when logging messages, both of these channels will have the opportunity to log the message. However, as we will see below, whether these channels actually log the message may be determined by the message's severity / "level". -->
위 설정을 하나씩 살펴봅니다. 먼저 `stack` 채널은 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 묶고 있습니다. 따라서 로그가 작성될 때 두 채널 모두 메시지를 로그할 기회를 갖게 됩니다. 하지만 아래 설명할 메시지 심각도 / "레벨"에 따라서 각 채널의 기록 여부가 결정됩니다.

<a name="log-levels"></a>
<!-- #### Log Levels -->
#### Log Levels

<!-- Take note of the `level` configuration option present on the `syslog` and `slack` channel configurations in the example above. This option determines the minimum "level" a message must be in order to be logged by the channel. Monolog, which powers Laravel's logging services, offers all of the log levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424). In descending order of severity, these log levels are: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, and **debug**. -->
위 예시에서 `syslog`와 `slack` 채널 설정에 동봉된 `level` 옵션을 눈여겨보세요. 이 옵션은 해당 채널이 로그를 기록하기 위한 최소 "레벨"을 정의합니다. Laravel의 로깅은 Monolog을 기반으로 하며, Monolog은 [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에 정의된 다음 8가지 로그 레벨을 지원합니다. 높은 심각도 순서대로: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 입니다.

<!-- So, imagine we log a message using the `debug` method: -->
예를 들어, 다음과 같이 `debug` 레벨로 메시지를 로그했다고 가정합시다:

```php
Log::debug('An informational message.');
```

<!-- Given our configuration, the `syslog` channel will write the message to the system log; however, since the error message is not `critical` or above, it will not be sent to Slack. However, if we log an `emergency` message, it will be sent to both the system log and Slack since the `emergency` level is above our minimum level threshold for both channels: -->
설정대로라면 `syslog` 채널은 이 메시지를 시스템 로그에 기록하지만, 에러 메시지가 `critical` 이상이 아니므로 Slack으로는 전송하지 않습니다. 반면 `emergency` 메시지를 기록하면, `emergency` 레벨이 두 채널의 최소 레벨 기준을 모두 넘으므로 시스템 로그와 Slack 양쪽 모두에 전송됩니다:

```php
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
<!-- ## Writing Log Messages -->
## Writing Log Messages

<!-- You may write information to the logs using the `Log` [facade](/docs/13.x/facades). As previously mentioned, the logger provides the eight logging levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**: -->
`Log` [facade](/docs/13.x/facades)를 사용해 로그에 정보를 기록할 수 있습니다. 앞서 설명했듯이 logger는 [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에 정의된 다음 8가지 로깅 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**:

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

<!-- You may call any of these methods to log a message for the corresponding level. By default, the message will be written to the default log channel as configured by your `logging` configuration file: -->
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
<!-- ### Contextual Information -->
### Contextual Information

<!-- An array of contextual data may be passed to the log methods. This contextual data will be formatted and displayed with the log message: -->
로그 메서드에는 로그 메시지와 함께 표시할 추가적인 컨텍스트 데이터를 배열로 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

<!-- Occasionally, you may wish to specify some contextual information that should be included with all subsequent log entries in a particular channel. For example, you may wish to log a request ID that is associated with each incoming request to your application. To accomplish this, you may call the `Log` facade's `withContext` method: -->
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

<!-- If you would like to share contextual information across _all_ logging channels, you may invoke the `Log::shareContext()` method. This method will provide the contextual information to all created channels and any channels that are created subsequently: -->
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
> 큐에 등록된 잡을 처리하는 동안 로그 컨텍스트를 공유해야 한다면 [job middleware](/docs/13.x/queues#job-middleware)를 사용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
<!-- ### Writing to Specific Channels -->
### Writing to Specific Channels

<!-- Sometimes you may wish to log a message to a channel other than your application's default channel. You may use the `channel` method on the `Log` facade to retrieve and log to any channel defined in your configuration file: -->
애플리케이션의 기본 로그 채널이 아닌 특정 채널에 메시지를 기록하고 싶을 때도 있습니다. 이 경우 `Log` 파사드의 `channel` 메서드를 사용해 구성 파일에 정의된 원하는 채널을 선택할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

<!-- If you would like to create an on-demand logging stack consisting of multiple channels, you may use the `stack` method: -->
또한, 여러 채널로 구성된 즉석 로그 스택을 만들어 쓸 수도 있습니다. 이때 `stack` 메서드를 사용하세요:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
<!-- #### On-Demand Channels -->
#### On-Demand Channels

<!-- It is also possible to create an on-demand channel by providing the configuration at runtime without that configuration being present in your application's `logging` configuration file. To accomplish this, you may pass a configuration array to the `Log` facade's `build` method: -->
애플리케이션의 `logging` 설정 파일에 채널 설정이 없어도, 런타임 실행 시 설정 배열을 전달해 즉석 채널을 생성할 수도 있습니다. 이는 `Log` 파사드의 `build` 메서드를 통해 가능합니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

<!-- You may also wish to include an on-demand channel in an on-demand logging stack. This can be achieved by including your on-demand channel instance in the array passed to the `stack` method: -->
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
<!-- ## Monolog Channel Customization -->
## Monolog Channel Customization

<a name="customizing-monolog-for-channels"></a>
<!-- ### Customizing Monolog for Channels -->
### Customizing Monolog for Channels

<!-- Sometimes you may need complete control over how Monolog is configured for an existing channel. For example, you may want to configure a custom Monolog `FormatterInterface` implementation for Laravel's built-in `single` channel. -->
기존 채널에서 Monolog 구성을 완전히 제어해야 하는 경우도 있습니다. 예를 들어, Laravel 기본 `single` 채널에서 사용하는 Monolog `FormatterInterface` 구현을 직접 설정하고 싶을 때가 그렇습니다.

<!-- To get started, define a `tap` array on the channel's configuration. The `tap` array should contain a list of classes that should have an opportunity to customize (or "tap" into) the Monolog instance after it is created. There is no conventional location where these classes should be placed, so you are free to create a directory within your application to contain these classes: -->
먼저 채널 설정에 `tap` 배열을 정의하세요. `tap` 배열에는 Monolog 인스턴스가 생성된 직후 사용자 지정할 클래스들이 명시됩니다. 이러한 클래스들은 원하는 위치에 만들어도 무방합니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```

<!-- Once you have configured the `tap` option on your channel, you're ready to define the class that will customize your Monolog instance. This class only needs a single method: `__invoke`, which receives an `Illuminate\Log\Logger` instance. The `Illuminate\Log\Logger` instance proxies all method calls to the underlying Monolog instance: -->
이제 `tap` 옵션에서 지정한 클래스를 작성할 차례입니다. 클래스는 단 하나의 메서드 `__invoke`만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 받습니다. `Illuminate\Log\Logger` 인스턴스는 실제 내부 Monolog 인스턴스에 모든 메서드 호출을 프록시합니다:

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
> 모든 "tap" 클래스는 [service container](/docs/13.x/container)를 통해 해결되므로, 해당 클래스에 필요한 모든 생성자 의존성이 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
<!-- ### Creating Monolog Handler Channels -->
### Creating Monolog Handler Channels

<!-- Monolog has a variety of [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) and Laravel does not include a built-in channel for each one. In some cases, you may wish to create a custom channel that is merely an instance of a specific Monolog handler that does not have a corresponding Laravel log driver. These channels can be easily created using the `monolog` driver. -->
Monolog에는 다양한 [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있지만, Laravel은 이 중 일부에 대한 기본 채널만 제공합니다. 경우에 따라 Laravel에서 제공하지 않는 특정 Monolog 핸들러를 단순히 사용하는 맞춤 채널을 만들고 싶을 수 있습니다. 이런 경우 `monolog` 드라이버를 사용하는 것이 편리합니다.

<!-- When using the `monolog` driver, the `handler` configuration option is used to specify which handler will be instantiated. Optionally, any constructor parameters the handler needs may be specified using the `handler_with` configuration option: -->
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
<!-- #### Monolog Formatters -->
#### Monolog Formatters

<!-- When using the `monolog` driver, the Monolog `LineFormatter` will be used as the default formatter. However, you may customize the type of formatter passed to the handler using the `formatter` and `formatter_with` configuration options: -->
`monolog` 드라이버를 사용할 경우 기본 포매터는 Monolog `LineFormatter`입니다. 그러나 `formatter` 및 `formatter_with` 설정을 활용해 핸들러에 전달할 포매터 타입을 사용자 지정할 수 있습니다:

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

<!-- If you are using a Monolog handler that is capable of providing its own formatter, you may set the value of the `formatter` configuration option to `default`: -->
만약 자체 포매터를 제공하는 핸들러라면, `formatter` 옵션에 `default` 값을 줄 수 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="monolog-processors"></a>
<!-- #### Monolog Processors -->
#### Monolog Processors

<!-- Monolog can also process messages before logging them. You can create your own processors or use the [existing processors offered by Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor). -->
Monolog은 로그 메시지가 기록되기 전 처리하는 프로세서도 지원합니다. 사용자가 직접 프로세서를 작성하거나, Monolog이 제공하는 [existing processors offered by Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 활용할 수 있습니다.

<!-- If you would like to customize the processors for a `monolog` driver, add a `processors` configuration value to your channel's configuration: -->
`monolog` 드라이버에서 프로세서를 사용자 지정하려면 채널 설정에 `processors` 배열을 추가합니다:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // Simple syntax...
        Monolog\Processor\MemoryUsageProcessor::class,

        // With options...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```

<a name="creating-custom-channels-via-factories"></a>
<!-- ### Creating Custom Channels via Factories -->
### Creating Custom Channels via Factories

<!-- If you would like to define an entirely custom channel in which you have full control over Monolog's instantiation and configuration, you may specify a `custom` driver type in your `config/logging.php` configuration file. Your configuration should include a `via` option that contains the name of the factory class which will be invoked to create the Monolog instance: -->
Monolog 인스턴스 생성과 구성을 완전 직접 제어하는 맞춤 채널을 만들고 싶다면, `config/logging.php`에 `custom` 드라이버 유형을 지정할 수 있습니다. 그리고 `via` 옵션에 Monolog 인스턴스를 생성할 팩토리 클래스명을 적어야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

<!-- Once you have configured the `custom` driver channel, you're ready to define the class that will create your Monolog instance. This class only needs a single `__invoke` method which should return the Monolog logger instance. The method will receive the channels configuration array as its only argument: -->
`custom` 드라이버 채널을 설정한 후에는 Monolog 인스턴스를 생성하는 클래스를 작성합니다. 이 클래스는 `__invoke` 메서드 하나만 필요하며, 이 메서드는 채널 설정 배열을 받아 Monolog 로거 인스턴스를 반환하면 됩니다:

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
<!-- ## Tailing Log Messages Using Pail -->
## Tailing Log Messages Using Pail

<!-- Often you may need to tail your application's logs in real time. For example, when debugging an issue or when monitoring your application's logs for specific types of errors. -->
문제가 있을 때 디버깅하거나 특정 종류의 오류를 실시간 모니터링할 때 애플리케이션 로그를 실시간으로 확인(테일)해야 할 때가 많습니다.

<!-- Laravel Pail is a package that allows you to easily dive into your Laravel application's log files directly from the command line. Unlike the standard `tail` command, Pail is designed to work with any log driver, including [Laravel Nightwatch](https://nightwatch.laravel.com), Sentry, or Flare. In addition, Pail provides a set of useful filters to help you quickly find what you're looking for. -->
Laravel Pail은 명령줄에서 Laravel 애플리케이션의 로그 파일을 쉽게 살펴볼 수 있는 패키지입니다. 표준 `tail` 명령어와 달리 Pail은 [Laravel Nightwatch](https://nightwatch.laravel.com), Sentry, Flare를 비롯한 모든 로그 드라이버와 함께 작동하도록 설계되었습니다. 또한 Pail은 원하는 내용을 빠르게 찾을 수 있도록 유용한 필터를 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png"/>

<a name="pail-installation"></a>
<!-- ### Installation -->
### Installation

> [!WARNING]
> Laravel Pail에는 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장이 필요합니다.

<!-- To get started, install Pail into your project using the Composer package manager: -->
Composer를 이용해 개발 환경 전용 패키지로 Pail을 설치하세요:

```shell
composer require --dev laravel/pail
```

<a name="pail-usage"></a>
<!-- ### Usage -->
### Usage

<!-- To start tailing logs, run the `pail` command: -->
로그 테일링을 시작하려면 `pail` 명령어를 실행하세요:

```shell
php artisan pail
```

<!-- To increase the verbosity of the output and avoid truncation (…), use the `-v` option: -->
출력 내용을 좀 더 자세히 보고 누락 없이 표시하려면 `-v` 옵션을 사용합니다:

```shell
php artisan pail -v
```

<!-- For maximum verbosity and to display exception stack traces, use the `-vv` option: -->
예외 스택 트레이스까지 최대 상세하게 표시하려면 `-vv` 옵션을 사용하세요:

```shell
php artisan pail -vv
```

<!-- To stop tailing logs, press `Ctrl+C` at any time. -->
로그 테일링을 종료하려면 언제든지 `Ctrl+C`로 중단할 수 있습니다.

<a name="pail-filtering-logs"></a>
<!-- ### Filtering Logs -->
### Filtering Logs

<a name="pail-filtering-logs-filter-option"></a>
<!-- #### `--filter` -->
#### `--filter`

<!-- You may use the `--filter` option to filter logs by their type, file, message, and stack trace content: -->
`--filter` 옵션을 사용하면 로그를 유형, 파일, 메시지, 스택 트레이스 내용 등으로 필터링할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
<!-- #### `--message` -->
#### `--message`

<!-- To filter logs by only their message, you may use the `--message` option: -->
메시지 내용만으로 로그를 필터링하려면 `--message` 옵션을 사용합니다:

```shell
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
<!-- #### `--level` -->
#### `--level`

<!-- The `--level` option may be used to filter logs by their [log level](#log-levels): -->
`--level` 옵션은 로그 [log level](#log-levels)로 필터링할 때 사용합니다:

```shell
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
<!-- #### `--user` -->
#### `--user`

<!-- To only display logs that were written while a given user was authenticated, you may provide the user's ID to the `--user` option: -->
특정 사용자가 인증된 상태에서 기록된 로그만 표시할 때는 사용자 ID를 `--user` 옵션에 넘깁니다:

```shell
php artisan pail --user=1
```
