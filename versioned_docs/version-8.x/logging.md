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
    - [Writing To Specific Channels](#writing-to-specific-channels)
- [Monolog Channel Customization](#monolog-channel-customization)
    - [Customizing Monolog For Channels](#customizing-monolog-for-channels)
    - [Creating Monolog Handler Channels](#creating-monolog-handler-channels)
    - [Creating Custom Channels Via Factories](#creating-custom-channels-via-factories)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- To help you learn more about what's happening within your application, Laravel provides robust logging services that allow you to log messages to files, the system error log, and even to Slack to notify your entire team. -->
애플리케이션 내부에서 일어나는 다양한 상황을 좀 더 쉽게 파악할 수 있도록, Laravel은 강력한 로깅 서비스를 제공합니다. 이를 통해 파일, 시스템 에러 로그, 심지어 Slack 등 다양한 곳에 로그 메시지를 남길 수 있어 팀원 전체에 알림을 줄 수도 있습니다.

<!-- Laravel logging is based on "channels". Each channel represents a specific way of writing log information. For example, the `single` channel writes log files to a single log file, while the `slack` channel sends log messages to Slack. Log messages may be written to multiple channels based on their severity. -->
Laravel의 로깅은 "채널(channel)"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 모든 로그를 하나의 로그 파일에 기록하고, `slack` 채널은 로그 메시지를 Slack으로 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수도 있습니다.

<!-- Under the hood, Laravel utilizes the [Monolog](https://github.com/Seldaek/monolog) library, which provides support for a variety of powerful log handlers. Laravel makes it a cinch to configure these handlers, allowing you to mix and match them to customize your application's log handling. -->
내부적으로 Laravel은 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 활용하여 다양한 강력한 로그 핸들러를 지원합니다. Laravel은 이러한 핸들러들을 손쉽게 설정할 수 있도록 도와주며, 필요에 따라 자유롭게 조합하여 애플리케이션의 로그 처리 방식을 원하는 대로 맞출 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- All of the configuration options for your application's logging behavior is housed in the `config/logging.php` configuration file. This file allows you to configure your application's log channels, so be sure to review each of the available channels and their options. We'll review a few common options below. -->
애플리케이션의 로깅 동작을 제어하는 모든 설정 옵션은 `config/logging.php` 설정 파일에 정의되어 있습니다. 이 파일을 통해 사용 중인 로그 채널을 구성할 수 있으니, 각 채널과 옵션을 꼭 확인해 보는 것이 좋습니다. 아래에서 자주 사용하는 몇 가지 주요 옵션을 살펴보겠습니다.

<!-- By default, Laravel will use the `stack` channel when logging messages. The `stack` channel is used to aggregate multiple log channels into a single channel. For more information on building stacks, check out the [documentation below](#building-log-stacks). -->
기본적으로 Laravel은 로그 메시지를 기록할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 하나로 묶어주는 역할을 합니다. 스택(stack) 구성에 대한 상세 내용은 [documentation below](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
<!-- #### Configuring The Channel Name -->
#### Configuring The Channel Name

<!-- By default, Monolog is instantiated with a "channel name" that matches the current environment, such as `production` or `local`. To change this value, add a `name` option to your channel's configuration: -->
기본적으로 Monolog은 현재 환경(`production`이나 `local` 등)에 맞는 "채널 이름"으로 인스턴스가 생성됩니다. 이 값을 바꾸고 싶다면, 해당 채널 설정에 `name` 옵션을 추가하면 됩니다:

```
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="available-channel-drivers"></a>
<!-- ### Available Channel Drivers -->
### Available Channel Drivers

<!-- Each log channel is powered by a "driver". The driver determines how and where the log message is actually recorded. The following log channel drivers are available in every Laravel application. An entry for most of these drivers is already present in your application's `config/logging.php` configuration file, so be sure to review this file to become familiar with its contents: -->
각 로그 채널은 "드라이버"에 의해 구동됩니다. 드라이버는 로그 메시지가 어떤 방식, 어디에 저장될지 결정합니다. 모든 Laravel 애플리케이션에서 사용 가능한 로그 채널 드라이버는 아래와 같습니다. 대부분의 드라이버에 대한 설정 예시는 이미 `config/logging.php` 파일에 포함되어 있으니, 이 파일을 꼭 확인해 보세요:

<!--
Name | Description
------------- | -------------
`custom` | A driver that calls a specified factory to create a channel
`daily` | A `RotatingFileHandler` based Monolog driver which rotates daily
`errorlog` | An `ErrorLogHandler` based Monolog driver
`monolog` | A Monolog factory driver that may use any supported Monolog handler
`null` | A driver that discards all log messages
`papertrail` | A `SyslogUdpHandler` based Monolog driver
`single` | A single file or path based logger channel (`StreamHandler`)
`slack` | A `SlackWebhookHandler` based Monolog driver
`stack` | A wrapper to facilitate creating "multi-channel" channels
`syslog` | A `SyslogHandler` based Monolog driver
-->
이름 | 설명
------------- | -------------
`custom` | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버
`daily` | 매일 로그 파일을 분리해 저장하는 Monolog의 `RotatingFileHandler` 기반 드라이버
`errorlog` | 시스템 에러 로그에 기록하는 Monolog의 `ErrorLogHandler` 기반 드라이버
`monolog` | 다양한 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`null` | 모든 로그 메시지를 폐기하는 드라이버
`papertrail` | Monolog의 `SyslogUdpHandler` 기반 드라이버 (Papertrail 서비스 연동)
`single` | 단일 파일 또는 경로에 로그를 저장하는 채널 (`StreamHandler`)
`slack` | Monolog의 `SlackWebhookHandler`를 사용하는 드라이버로 Slack에 로그를 전송
`stack` | 여러 채널을 하나로 묶어주는 래퍼 채널
`syslog` | 시스템 로그에 기록하는 Monolog의 `SyslogHandler` 기반 드라이버

> [!TIP]
> `monolog`과 `custom` 드라이버에 대한 고급 채널 커스터마이징은 [advanced channel customization](#monolog-channel-customization)에서 더 자세히 다루고 있으니 참고하시기 바랍니다.

<a name="channel-prerequisites"></a>
<!-- ### Channel Prerequisites -->
### Channel Prerequisites

<a name="configuring-the-single-and-daily-channels"></a>
<!-- #### Configuring The Single and Daily Channels -->
#### Configuring The Single and Daily Channels

<!-- The `single` and `daily` channels have three optional configuration options: `bubble`, `permission`, and `locking`. -->
`single`과 `daily` 채널은 세 가지 선택적 옵션(`bubble`, `permission`, `locking`)을 지원합니다.

<!--
Name | Description | Default
------------- | ------------- | -------------
`bubble` | Indicates if messages should bubble up to other channels after being handled | `true`
`locking` | Attempt to lock the log file before writing to it | `false`
`permission` | The log file's permissions | `0644`
-->
이름 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 처리 후 메시지가 다른 채널로 전달(bubble up)될지 여부 | `true`
`locking` | 로그 기록 전 파일 잠금을 시도할지 여부 | `false`
`permission` | 로그 파일의 권한 설정 | `0644`

<a name="configuring-the-papertrail-channel"></a>
<!-- #### Configuring The Papertrail Channel -->
#### Configuring The Papertrail Channel

<!-- The `papertrail` channel requires the `host` and `port` configuration options. You can obtain these values from [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app). -->
`papertrail` 채널을 사용하려면 `host`와 `port` 옵션을 필수로 설정해야 합니다. 각 값은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
<!-- #### Configuring The Slack Channel -->
#### Configuring The Slack Channel

<!-- The `slack` channel requires a `url` configuration option. This URL should match a URL for an [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) that you have configured for your Slack team. -->
`slack` 채널을 사용하려면 `url` 설정 값이 필요합니다. 이 URL은 여러분이 Slack 팀용으로 만들어 둔 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 주소와 일치해야 합니다.

<!-- By default, Slack will only receive logs at the `critical` level and above; however, you can adjust this in your `config/logging.php` configuration file by modifying the `level` configuration option within your Slack log channel's configuration array. -->
기본적으로 Slack은 `critical` 등급 이상의 로그만 수신합니다. 하지만, `config/logging.php` 설정 파일 내에 있는 Slack 로그 채널의 `level` 값을 조정함으로써 이 기준을 변경할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
<!-- ### Logging Deprecation Warnings -->
### Logging Deprecation Warnings

<!-- PHP, Laravel, and other libraries often notify their users that some of their features have been deprecated and will be removed in a future version. If you would like to log these deprecation warnings, you may specify your preferred `deprecations` log channel in your application's `config/logging.php` configuration file: -->
PHP, Laravel, 그리고 기타 라이브러리는 일부 기능이 더 이상 지원되지 않고, 앞으로 제거될 예정이라는 메시지(Deprecated Warnings)를 종종 제공합니다. 이러한 폐기 예정 경고를 로그로 남기고 싶을 땐, 애플리케이션의 `config/logging.php` 파일에서 원하는 `deprecations` 로그 채널을 지정할 수 있습니다:

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

<!-- Or, you may define a log channel named `deprecations`. If a log channel with this name exists, it will always be used to log deprecations: -->
또는, `deprecations`라는 이름의 로그 채널을 정의할 수도 있습니다. 해당 이름의 로그 채널이 존재하면, 폐기 경고는 항상 이 채널로 기록됩니다:

```
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
앞서 살펴봤듯이, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 편리하게 결합할 수 있습니다. 실제 운영 환경에서 볼 수 있는 구성 예시를 살펴보겠습니다:

```
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'],
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => 'debug',
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => 'Laravel Log',
        'emoji' => ':boom:',
        'level' => 'critical',
    ],
],
```

<!-- Let's dissect this configuration. First, notice our `stack` channel aggregates two other channels via its `channels` option: `syslog` and `slack`. So, when logging messages, both of these channels will have the opportunity to log the message. However, as we will see below, whether these channels actually log the message may be determined by the message's severity / "level". -->
이 예시를 하나씩 설명해 보겠습니다. 먼저, `stack` 채널이 `channels` 옵션을 통해 `syslog`와 `slack` 두 채널을 묶고 있다는 점을 확인할 수 있습니다. 즉, 로그 메시지가 기록될 때 이 두 채널에서 모두 메시지를 받아 처리할 수 있습니다. 단, 아래 설명하는 것처럼 실제로 어느 채널에 메시지가 쓰일지는 메시지의 심각도(level)에 따라 달라집니다.

<a name="log-levels"></a>
<!-- #### Log Levels -->
#### Log Levels

<!-- Take note of the `level` configuration option present on the `syslog` and `slack` channel configurations in the example above. This option determines the minimum "level" a message must be in order to be logged by the channel. Monolog, which powers Laravel's logging services, offers all of the log levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, and **debug**. -->
위 예시에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 포함되어 있는 점에 주목해주세요. 이 옵션은 해당 채널이 로깅할 메시지의 최소 "레벨"을 결정합니다. Monolog(Laravel 로깅 시스템의 기반)는 [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에서 정의된 모든 로그 레벨을 지원합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**.

<!-- So, imagine we log a message using the `debug` method: -->
예를 들어, `debug` 메서드로 메시지를 남겨본다고 가정해봅시다.

```
Log::debug('An informational message.');
```

<!-- Given our configuration, the `syslog` channel will write the message to the system log; however, since the error message is not `critical` or above, it will not be sent to Slack. However, if we log an `emergency` message, it will be sent to both the system log and Slack since the `emergency` level is above our minimum level threshold for both channels: -->
이 경우, 예시 구성에서는 `syslog` 채널이 시스템 로그에 메시지를 기록하게 됩니다. 하지만 이 메시지는 `critical` 이상 등급이 아니기 때문에 Slack에는 전송되지 않습니다. 반대로, 만약 `emergency` 등급의 메시지를 남긴다면, `emergency` 레벨이 두 채널의 최소 레벨 기준을 모두 넘으므로 시스템 로그와 Slack 양쪽 모두에 기록됩니다:

```
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
<!-- ## Writing Log Messages -->
## Writing Log Messages

<!-- You may write information to the logs using the `Log` [facade](/docs/8.x/facades). As previously mentioned, the logger provides the eight logging levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**: -->
`Log` [facade](/docs/8.x/facades)를 활용하여 로그에 다양한 정보를 기록할 수 있습니다. 앞서 언급했듯, 로거는 [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에서 정의한 여덟 가지 로그 레벨(**emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**)을 모두 지원합니다.

```
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
이 중 어디든 원하는 메서드를 호출해서 해당 레벨에 맞는 메시지를 로그로 남길 수 있습니다. 기본적으로는, 메시지가 `logging` 설정 파일에서 지정한 기본 로그 채널로 기록됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Support\Facades\Log;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        Log::info('Showing the user profile for user: '.$id);

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
로그 메서드에 컨텍스트 데이터(배열 형태)를 함께 전달할 수도 있습니다. 이 데이터는 로그 메시지와 같이 포맷되어 함께 기록됩니다.

```
use Illuminate\Support\Facades\Log;

Log::info('User failed to login.', ['id' => $user->id]);
```

<!-- Occasionally, you may wish to specify some contextual information that should be included with all subsequent log entries. For example, you may wish to log a request ID that is associated with each incoming request to your application. To accomplish this, you may call the `Log` facade's `withContext` method: -->
가끔은, 앞으로 남길 모든 로그 메시지에 공통적으로 포함해야 할 컨텍스트 정보를 지정하고 싶을 수도 있습니다. 예를 들어, 각 요청마다 고유하게 발급되는 request ID를 함께 기록하고 싶을 때가 있습니다. 이때는 `Log` 파사드의 `withContext` 메서드를 사용하면 됩니다.

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        return $next($request)->header('Request-Id', $requestId);
    }
}
```

<a name="writing-to-specific-channels"></a>
<!-- ### Writing To Specific Channels -->
### Writing To Specific Channels

<!-- Sometimes you may wish to log a message to a channel other than your application's default channel. You may use the `channel` method on the `Log` facade to retrieve and log to any channel defined in your configuration file: -->
애플리케이션의 기본 로그 채널이 아닌, 특정 채널로 메시지를 로깅하고 싶은 경우가 있습니다. 이럴 때는 `Log` 파사드의 `channel` 메서드를 사용해, 설정 파일에 정의된 채널 중 원하는 채널로 직접 메서드 체인을 연결해 로그를 남기면 됩니다.

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

<!-- If you would like to create an on-demand logging stack consisting of multiple channels, you may use the `stack` method: -->
만약 여러 채널을 묶은 스택(stack) 채널을 즉석에서 만들어 로그를 남기고 싶다면 `stack` 메서드를 사용하면 됩니다.

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
<!-- #### On-Demand Channels -->
#### On-Demand Channels

<!-- It is also possible to create an on-demand channel by providing the configuration at runtime without that configuration being present in your application's `logging` configuration file. To accomplish this, you may pass a configuration array to the `Log` facade's `build` method: -->
`logging` 설정 파일에 미리 정의되어 있지 않은 채널을, 런타임에 즉석으로 만들어 사용하고 싶을 때에는 `Log` 파사드의 `build` 메서드에 설정 배열을 전달하면 됩니다.

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

<!-- You may also wish to include an on-demand channel in an on-demand logging stack. This can be achieved by including your on-demand channel instance in the array passed to the `stack` method: -->
즉석으로 만든 채널 인스턴스를 즉석 스택에 포함시키고 싶은 경우에도, 해당 채널 인스턴스를 배열에 추가하여 `stack` 메서드에 전달하면 됩니다.

```
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
<!-- ### Customizing Monolog For Channels -->
### Customizing Monolog For Channels

<!-- Sometimes you may need complete control over how Monolog is configured for an existing channel. For example, you may want to configure a custom Monolog `FormatterInterface` implementation for Laravel's built-in `single` channel. -->
기존 채널에 대해 Monolog의 다양한 설정을 완전히 제어하고 싶을 때가 있습니다. 예를 들어, Laravel 기본 제공 `single` 채널에 Monolog의 커스텀 `FormatterInterface` 구현체를 적용하고 싶을 수 있습니다.

<!-- To get started, define a `tap` array on the channel's configuration. The `tap` array should contain a list of classes that should have an opportunity to customize (or "tap" into) the Monolog instance after it is created. There is no conventional location where these classes should be placed, so you are free to create a directory within your application to contain these classes: -->
이 경우, 채널 설정에 `tap` 배열을 정의하면 됩니다. `tap` 배열에는 Monolog 인스턴스가 생성된 후 커스터마이징을 할 수 있는 클래스의 목록을 지정합니다. 해당 클래스들은 애플리케이션 내 어디에 두어도 상관없으며, 필요한 폴더 내에 자유롭게 생성하면 됩니다.

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

<!-- Once you have configured the `tap` option on your channel, you're ready to define the class that will customize your Monolog instance. This class only needs a single method: `__invoke`, which receives an `Illuminate\Log\Logger` instance. The `Illuminate\Log\Logger` instance proxies all method calls to the underlying Monolog instance: -->
채널에 `tap` 옵션을 설정했다면, 이제 실제로 Monolog 인스턴스를 커스터마이즈하는 클래스를 정의하면 됩니다. 이 클래스에는 `__invoke`라는 단 하나의 메서드만 필요하며, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 인자로 받습니다. `Illuminate\Log\Logger`는 내부적으로 Monolog 인스턴스에 모든 메서드 호출을 위임합니다.

```
<?php

namespace App\Logging;

use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
     *
     * @param  \Illuminate\Log\Logger  $logger
     * @return void
     */
    public function __invoke($logger)
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```

> [!TIP]
> 모든 "tap" 클래스는 [service container](/docs/8.x/container)에 의해 자동 해석(resolve)되므로, 생성자에서 다른 의존성이 필요한 경우도 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
<!-- ### Creating Monolog Handler Channels -->
### Creating Monolog Handler Channels

<!-- Monolog has a variety of [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) and Laravel does not include a built-in channel for each one. In some cases, you may wish to create a custom channel that is merely an instance of a specific Monolog handler that does not have a corresponding Laravel log driver.  These channels can be easily created using the `monolog` driver. -->
Monolog에는 다양한 [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 존재하지만, Laravel에는 그 모든 핸들러에 대한 내장 채널이 준비되어 있는 것은 아닙니다. 특정 Monolog 핸들러만을 이용한 채널이 필요하다면, Laravel의 자체 로그 드라이버 대신 `monolog` 드라이버를 이용해 쉽게 직접 만들 수 있습니다.

<!-- When using the `monolog` driver, the `handler` configuration option is used to specify which handler will be instantiated. Optionally, any constructor parameters the handler needs may be specified using the `with` configuration option: -->
`monolog` 드라이버 사용 시, `handler` 옵션에 사용할 핸들러를 지정합니다. 핸들러 생성자에 필요로 하는 추가 파라미터가 있다면 `with` 옵션을 사용해 전달하면 됩니다.

```
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```

<a name="monolog-formatters"></a>
<!-- #### Monolog Formatters -->
#### Monolog Formatters

<!-- When using the `monolog` driver, the Monolog `LineFormatter` will be used as the default formatter. However, you may customize the type of formatter passed to the handler using the `formatter` and `formatter_with` configuration options: -->
`monolog` 드라이버를 사용하는 경우, Monolog의 `LineFormatter`가 기본 포매터로 쓰입니다. 하지만 핸들러에 전달되는 포매터 종류를 커스터마이즈하고 싶다면 `formatter`와 `formatter_with` 설정 옵션을 사용할 수 있습니다.

```
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
만약 사용하는 Monolog 핸들러가 자체적으로 포매터를 제공할 수 있다면, `formatter` 값을 `default`로 지정할 수 있습니다.

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

<a name="creating-custom-channels-via-factories"></a>
<!-- ### Creating Custom Channels Via Factories -->
### Creating Custom Channels Via Factories

<!-- If you would like to define an entirely custom channel in which you have full control over Monolog's instantiation and configuration, you may specify a `custom` driver type in your `config/logging.php` configuration file. Your configuration should include a `via` option that contains the name of the factory class which will be invoked to create the Monolog instance: -->
Monolog의 인스턴스 생성과 설정 과정을 완전히 직접 제어하고 싶을 경우, `config/logging.php` 파일에서 `custom` 드라이버 타입을 지정해 커스텀 채널을 만들 수 있습니다. 이때 설정에는 Monolog 인스턴스를 생성할 팩토리 클래스의 이름을 `via` 옵션에 명시해야 합니다.

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

<!-- Once you have configured the `custom` driver channel, you're ready to define the class that will create your Monolog instance. This class only needs a single `__invoke` method which should return the Monolog logger instance. The method will receive the channels configuration array as its only argument: -->
`custom` 드라이버 채널을 설정했다면, 이제 Monolog 인스턴스를 생성할 클래스를 정의할 차례입니다. 이 클래스는 단 하나의 `__invoke` 메서드만 필요하며, 해당 메서드는 채널 설정 배열을 인자로 받아 Monolog의 logger 인스턴스를 반환해야 합니다.

```
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     *
     * @param  array  $config
     * @return \Monolog\Logger
     */
    public function __invoke(array $config)
    {
        return new Logger(...);
    }
}
```