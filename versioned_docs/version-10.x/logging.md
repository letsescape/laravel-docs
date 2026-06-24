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
애플리케이션 내에서 어떤 일이 일어나고 있는지 더 잘 파악할 수 있도록, Laravel은 강력한 로깅 기능을 제공합니다. 이를 통해 메시지를 파일, 시스템 에러 로그, 또는 Slack 등으로 남길 수 있으며, 팀 전체에 알림을 보낼 수도 있습니다.

<!-- Laravel logging is based on "channels". Each channel represents a specific way of writing log information. For example, the `single` channel writes log files to a single log file, while the `slack` channel sends log messages to Slack. Log messages may be written to multiple channels based on their severity. -->
Laravel의 로깅 시스템은 "채널(channel)"을 기반으로 동작합니다. 각 채널은 로그 정보를 기록하는 특정 방식을 나타냅니다. 예를 들어, `single` 채널은 하나의 로그 파일에 모든 로그를 기록하며, `slack` 채널은 Slack으로 로그를 전송합니다. 로그 메시지는 심각도에 따라 여러 채널에 동시에 기록될 수도 있습니다.

<!-- Under the hood, Laravel utilizes the [Monolog](https://github.com/Seldaek/monolog) library, which provides support for a variety of powerful log handlers. Laravel makes it a cinch to configure these handlers, allowing you to mix and match them to customize your application's log handling. -->
Laravel은 내부적으로 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 사용합니다. Monolog은 다양한 강력한 로그 핸들러를 지원하며, Laravel은 이러한 핸들러의 설정을 간단하게 할 수 있도록 도와줍니다. 여러 핸들러를 조합해 여러분의 애플리케이션에 맞는 로그 처리 방식을 쉽게 구축할 수 있습니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- All of the configuration options for your application's logging behavior are housed in the `config/logging.php` configuration file. This file allows you to configure your application's log channels, so be sure to review each of the available channels and their options. We'll review a few common options below. -->
애플리케이션의 로깅 동작과 관련된 모든 구성 옵션은 `config/logging.php` 설정 파일에 있습니다. 이 파일에서 로그 채널을 직접 구성할 수 있으니, 제공되는 각 채널과 그 옵션들을 꼭 살펴보시기 바랍니다. 아래에서 자주 사용되는 몇 가지 옵션을 소개합니다.

<!-- By default, Laravel will use the `stack` channel when logging messages. The `stack` channel is used to aggregate multiple log channels into a single channel. For more information on building stacks, check out the [documentation below](#building-log-stacks). -->
기본적으로 Laravel은 메시지를 로깅할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 모아 하나의 채널처럼 동작하게 해줍니다. 스택 구축에 대한 자세한 내용은 [documentation below](#building-log-stacks)를 참고하세요.

<a name="configuring-the-channel-name"></a>
<!-- #### Configuring the Channel Name -->
#### Configuring the Channel Name

<!-- By default, Monolog is instantiated with a "channel name" that matches the current environment, such as `production` or `local`. To change this value, add a `name` option to your channel's configuration: -->
기본적으로 Monolog 인스턴스는 현재 환경(`production` 또는 `local` 등)에 맞는 "채널 이름(channel name)"을 사용합니다. 이 값을 변경하려면 채널 설정에 `name` 옵션을 추가하면 됩니다.

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
각 로그 채널은 "드라이버(driver)"에 의해 동작합니다. 드라이버는 실제로 로그 메시지가 기록되는 방법과 위치를 결정합니다. 아래는 모든 Laravel 애플리케이션에서 사용 가능한 로그 채널 드라이버의 목록입니다. 대부분의 드라이버는 이미 `config/logging.php` 파일에 기본적으로 포함되어 있으니 꼭 내용을 확인해보시기 바랍니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Name | Description
------------- | -------------
`custom` | A driver that calls a specified factory to create a channel
`daily` | A `RotatingFileHandler` based Monolog driver which rotates daily
`errorlog` | An `ErrorLogHandler` based Monolog driver
`monolog` | A Monolog factory driver that may use any supported Monolog handler
`papertrail` | A `SyslogUdpHandler` based Monolog driver
`single` | A single file or path based logger channel (`StreamHandler`)
`slack` | A `SlackWebhookHandler` based Monolog driver
`stack` | A wrapper to facilitate creating "multi-channel" channels
`syslog` | A `SyslogHandler` based Monolog driver
-->
이름 | 설명
------------- | -------------
`custom` | 지정한 팩토리를 호출하여 채널을 생성하는 드라이버
`daily` | 매일 로그 파일을 분리하여 기록하는 `RotatingFileHandler` 기반 Monolog 드라이버
`errorlog` | 시스템의 ErrorLog에 기록하는 `ErrorLogHandler` 기반 Monolog 드라이버
`monolog` | 지원되는 모든 Monolog 핸들러를 사용할 수 있는 Monolog 팩토리 드라이버
`papertrail` | `SyslogUdpHandler` 기반 Monolog 드라이버
`single` | 하나의 파일이나 경로에 기록하는 로거 채널 (`StreamHandler`)
`slack` | Slack으로 로그를 보내는 `SlackWebhookHandler` 기반 Monolog 드라이버
`stack` | 여러 채널을 묶는 "멀티채널" 생성을 돕는 래퍼 채널
`syslog` | 시스템의 Syslog에 기록하는 `SyslogHandler` 기반 Monolog 드라이버

<!-- </div> -->
</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대한 더 자세한 내용은 [advanced channel customization](#monolog-channel-customization)를 참고하세요.

<a name="channel-prerequisites"></a>
<!-- ### Channel Prerequisites -->
### Channel Prerequisites

<a name="configuring-the-single-and-daily-channels"></a>
<!-- #### Configuring the Single and Daily Channels -->
#### Configuring the Single and Daily Channels

<!-- The `single` and `daily` channels have three optional configuration options: `bubble`, `permission`, and `locking`. -->
`single`과 `daily` 채널은 `bubble`, `permission`, `locking`의 세 가지 선택적 설정 옵션을 제공합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Name | Description | Default
------------- | ------------- | -------------
`bubble` | Indicates if messages should bubble up to other channels after being handled | `true`
`locking` | Attempt to lock the log file before writing to it | `false`
`permission` | The log file's permissions | `0644`
-->
이름 | 설명 | 기본값
------------- | ------------- | -------------
`bubble` | 메시지 처리 후 다른 채널로 전파할지 여부 | `true`
`locking` | 로그 파일에 기록하기 전 잠금 시도 여부 | `false`
`permission` | 로그 파일의 퍼미션(권한) | `0644`

<!-- </div> -->
</div>

<!-- Additionally, the retention policy for the `daily` channel can be configured via the `days` option: -->
또한, `daily` 채널에서는 `days` 옵션을 통해서 로그 파일의 보관 기간(일)을 설정할 수 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Name | Description                                                       | Default
------------- |-------------------------------------------------------------------| -------------
`days` | The number of days that daily log files should be retained | `7`
-->
이름 | 설명                                                       | 기본값
------------- |-------------------------------------------------------------------| -------------
`days` | 일별 로그 파일의 보관 일수 | `7`

<!-- </div> -->
</div>

<a name="configuring-the-papertrail-channel"></a>
<!-- #### Configuring the Papertrail Channel -->
#### Configuring the Papertrail Channel

<!-- The `papertrail` channel requires the `host` and `port` configuration options. You can obtain these values from [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app). -->
`papertrail` 채널을 사용하려면 반드시 `host`와 `port` 구성 옵션이 필요합니다. 이 값들은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app)에서 확인할 수 있습니다.

<a name="configuring-the-slack-channel"></a>
<!-- #### Configuring the Slack Channel -->
#### Configuring the Slack Channel

<!-- The `slack` channel requires a `url` configuration option. This URL should match a URL for an [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) that you have configured for your Slack team. -->
`slack` 채널 사용을 위해서는 `url` 설정값이 필요합니다. 이 URL은 Slack 팀을 위한 [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks)에서 발급받아 사용하셔야 합니다.

<!-- By default, Slack will only receive logs at the `critical` level and above; however, you can adjust this in your `config/logging.php` configuration file by modifying the `level` configuration option within your Slack log channel's configuration array. -->
기본적으로 Slack으로는 `critical` 이상 로그만 전송됩니다. 하지만, 이 조건은 `config/logging.php` 파일 내 Slack 채널의 `level` 옵션을 수정함으로써 원하는 레벨로 조정할 수 있습니다.

<a name="logging-deprecation-warnings"></a>
<!-- ### Logging Deprecation Warnings -->
### Logging Deprecation Warnings

<!-- PHP, Laravel, and other libraries often notify their users that some of their features have been deprecated and will be removed in a future version. If you would like to log these deprecation warnings, you may specify your preferred `deprecations` log channel in your application's `config/logging.php` configuration file: -->
PHP, Laravel 그리고 기타 라이브러리들은 경우에 따라 일부 기능이 사용 중단(deprecated)되었으며, 향후 버전에서 제거될 예정임을 사용자에게 알립니다. 이런 사용 중단 경고를 로그로 남기고 싶다면, `config/logging.php` 파일의 `deprecations` 로그 채널 옵션을 설정하세요.

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

<!-- Or, you may define a log channel named `deprecations`. If a log channel with this name exists, it will always be used to log deprecations: -->
또는, `deprecations`라는 이름의 로그 채널을 별도로 정의할 수도 있습니다. 이러한 채널이 설정되어 있다면, 사용 중단 메시지는 항상 이 채널에 기록됩니다.

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
앞서 언급한 것처럼, `stack` 드라이버를 이용하면 여러 채널을 하나의 로그 채널로 묶어 사용할 수 있습니다. 아래는 실제 운영 환경에서 볼 수 있는 예시 설정입니다.

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
이 구성을 하나씩 살펴보면, 먼저 `stack` 채널의 `channels` 옵션에 `syslog`와 `slack`이 포함되어 있습니다. 즉, 로그 메시지는 두 채널 모두에 기록될 수 있습니다. 하지만 실제로 로그가 어떤 채널에 기록될지는 메시지의 심각도(레벨)에 따라 달라질 수 있습니다.

<a name="log-levels"></a>
<!-- #### Log Levels -->
#### Log Levels

<!-- Take note of the `level` configuration option present on the `syslog` and `slack` channel configurations in the example above. This option determines the minimum "level" a message must be in order to be logged by the channel. Monolog, which powers Laravel's logging services, offers all of the log levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424). In descending order of severity, these log levels are: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, and **debug**. -->
위 예시에서 `syslog`와 `slack` 채널 설정에 `level` 옵션이 포함되어 있습니다. 이 옵션은 해당 채널이 메시지를 기록하기 위한 최소 "레벨"을 지정합니다. Laravel의 로깅 서비스는 Monolog을 기반으로 하며, [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 지원합니다. 심각도가 높은 순서대로, **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**가 있습니다.

<!-- So, imagine we log a message using the `debug` method: -->
예를 들어, 아래와 같이 `debug` 메서드로 로그를 남기는 경우를 생각해봅니다.

```
Log::debug('An informational message.');
```

<!-- Given our configuration, the `syslog` channel will write the message to the system log; however, since the error message is not `critical` or above, it will not be sent to Slack. However, if we log an `emergency` message, it will be sent to both the system log and Slack since the `emergency` level is above our minimum level threshold for both channels: -->
이 경우, `syslog` 채널은 메시지를 시스템 로그에 기록합니다. 하지만, 이 메시지가 `critical` 레벨 이상이 아니기 때문에 Slack에는 전송되지 않습니다. 반대로 `emergency` 레벨의 로그라면, 두 채널 모두에 메시지가 기록됩니다. 왜냐하면 `emergency`는 양쪽 채널의 최소 레벨 조건을 모두 충족하기 때문입니다.

```
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
<!-- ## Writing Log Messages -->
## Writing Log Messages

<!-- You may write information to the logs using the `Log` [facade](/docs/10.x/facades). As previously mentioned, the logger provides the eight logging levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**: -->
로그를 작성하려면 `Log` [facade](/docs/10.x/facades)를 사용할 수 있습니다. 위에서 언급한 [RFC 5424 specification](https://tools.ietf.org/html/rfc5424)에 명시된 여덟 가지 로깅 레벨, 즉 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 메서드를 제공합니다.

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
각 메서드를 호출해 해당 레벨의 메시지를 로그로 남길 수 있습니다. 기본적으로 이 메시지는 `logging` 설정 파일에서 지정한 기본 로그 채널에 기록됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
로그 메서드에 추가 정보를 담은 배열을 함께 전달할 수 있습니다. 이 컨텍스트 정보는 로그 메시지와 함께 포맷되어 표시됩니다.

```
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

<!-- Occasionally, you may wish to specify some contextual information that should be included with all subsequent log entries in a particular channel. For example, you may wish to log a request ID that is associated with each incoming request to your application. To accomplish this, you may call the `Log` facade's `withContext` method: -->
경우에 따라, 특정 채널에 포함될 모든 로그 메시지에 컨텍스트 정보를 추가하고 싶을 수 있습니다. 예를 들어, 모든 요청에 대한 ID를 로그에 남기고 싶다면, `Log` 파사드의 `withContext` 메서드를 사용하세요.

```
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
_모든_ 로깅 채널에서 동일한 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 사용할 수 있습니다. 이 메서드는 이미 생성된 채널은 물론, 이후 새로 생성되는 모든 채널에도 컨텍스트 정보를 전달합니다.

```
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
> 큐 작업 처리를 하는 도중에 로그 컨텍스트를 공유해야 한다면, [job middleware](/docs/10.x/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
<!-- ### Writing to Specific Channels -->
### Writing to Specific Channels

<!-- Sometimes you may wish to log a message to a channel other than your application's default channel. You may use the `channel` method on the `Log` facade to retrieve and log to any channel defined in your configuration file: -->
기본 채널이 아닌 다른 채널에 로그 메시지를 남기고 싶을 때는, `Log` 파사드의 `channel` 메서드를 사용하여 구성 파일에 정의된 채널을 지정할 수 있습니다.

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

<!-- If you would like to create an on-demand logging stack consisting of multiple channels, you may use the `stack` method: -->
여러 채널을 묶어 임시로 로그 스택을 만들고 싶다면, `stack` 메서드를 사용하세요.

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
<!-- #### On-Demand Channels -->
#### On-Demand Channels

<!-- It is also possible to create an on-demand channel by providing the configuration at runtime without that configuration being present in your application's `logging` configuration file. To accomplish this, you may pass a configuration array to the `Log` facade's `build` method: -->
`logging` 설정 파일에 따로 정의하지 않고, 런타임에 즉석으로 구성해서 채널을 만들 수도 있습니다. 이럴 땐 `Log` 파사드의 `build` 메서드에 설정 배열을 넘기면 됩니다.

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

<!-- You may also wish to include an on-demand channel in an on-demand logging stack. This can be achieved by including your on-demand channel instance in the array passed to the `stack` method: -->
또한, 온디맨드 채널을 온디맨드 로그 스택에 포함시킬 수도 있습니다. 즉석에서 만든 채널 인스턴스를 `stack` 메서드에 배열로 전달하세요.

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
<!-- ### Customizing Monolog for Channels -->
### Customizing Monolog for Channels

<!-- Sometimes you may need complete control over how Monolog is configured for an existing channel. For example, you may want to configure a custom Monolog `FormatterInterface` implementation for Laravel's built-in `single` channel. -->
가끔은 특정 Monolog 채널이 생성된 이후 Monolog 인스턴스를 완전히 제어하고 싶을 수 있습니다. 예를 들어, Laravel 내장 `single` 채널에 커스텀 Monolog `FormatterInterface` 구현을 적용하고 싶을 때가 대표적입니다.

<!-- To get started, define a `tap` array on the channel's configuration. The `tap` array should contain a list of classes that should have an opportunity to customize (or "tap" into) the Monolog instance after it is created. There is no conventional location where these classes should be placed, so you are free to create a directory within your application to contain these classes: -->
이를 위해 채널 설정에 `tap` 배열을 추가할 수 있습니다. `tap` 배열에는 Monolog 인스턴스가 생성된 후, 그 인스턴스를 커스터마이징(또는 "tap")할 수 있는 클래스들의 목록을 나열합니다. 이 클래스들을 저장할 디렉터리는 자유롭게 만들면 되며 별도의 규칙은 없습니다.

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

<!-- Once you have configured the `tap` option on your channel, you're ready to define the class that will customize your Monolog instance. This class only needs a single method: `__invoke`, which receives an `Illuminate\Log\Logger` instance. The `Illuminate\Log\Logger` instance proxies all method calls to the underlying Monolog instance: -->
`tap` 옵션에 클래스를 추가한 후, Monolog 인스턴스를 커스터마이징하는 클래스를 만들면 됩니다. 이 클래스는 `__invoke` 메서드만 있으면 됩니다. 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 받으며, `Illuminate\Log\Logger` 인스턴스는 내부적으로 모든 호출을 Monolog 인스턴스로 전달합니다.

```
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
> 모든 "tap" 클래스는 [service container](/docs/10.x/container)에서 자동으로 의존성이 주입되어 인스턴스화됩니다.

<a name="creating-monolog-handler-channels"></a>
<!-- ### Creating Monolog Handler Channels -->
### Creating Monolog Handler Channels

<!-- Monolog has a variety of [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) and Laravel does not include a built-in channel for each one. In some cases, you may wish to create a custom channel that is merely an instance of a specific Monolog handler that does not have a corresponding Laravel log driver.  These channels can be easily created using the `monolog` driver. -->
Monolog은 [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)를 제공하지만, Laravel은 모든 핸들러에 대해 기본 채널을 제공하지는 않습니다. 특정 Monolog 핸들러를 활용하고 싶지만 Laravel 기본 드라이버가 없다면, `monolog` 드라이버로 쉽게 커스텀 채널을 만들 수 있습니다.

<!-- When using the `monolog` driver, the `handler` configuration option is used to specify which handler will be instantiated. Optionally, any constructor parameters the handler needs may be specified using the `with` configuration option: -->
`monolog` 드라이버를 사용할 때는, `handler` 옵션에 사용할 핸들러를 지정합니다. 핸들러 생성자에 전달할 추가 인자가 있다면, `with` 옵션을 사용하세요.

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
`monolog` 드라이버를 사용하면, 기본으로 Monolog의 `LineFormatter`가 핸들러에 적용됩니다. 하지만, `formatter` 와 `formatter_with` 옵션을 통해 포매터 타입과 옵션을 커스터마이즈할 수 있습니다.

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
Monolog 핸들러 자체적으로 포매터를 제공하는 경우라면, `formatter` 옵션을 `default`로 지정할 수 있습니다.

```
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```

 <a name="monolog-processors"></a>
<!-- #### Monolog Processors -->
#### Monolog Processors

<!--  Monolog can also process messages before logging them. You can create your own processors or use the [existing processors offered by Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor). -->
Monolog은 로그 메시지를 기록하기 전에 가공 처리할 수 있도록 프로세서 기능을 제공합니다. 직접 커스텀 프로세서를 만들 수도 있고, [existing processors offered by Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)도 사용할 수 있습니다.

<!--  If you would like to customize the processors for a `monolog` driver, add a `processors` configuration value to your channel's configuration: -->
`monolog` 드라이버에서 프로세서를 지정하려면, 채널 설정에 `processors` 값을 추가하세요.

```
 'memory' => [
     'driver' => 'monolog',
     'handler' => Monolog\Handler\StreamHandler::class,
     'with' => [
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
Monolog 인스턴스의 생성 및 설정을 전적으로 직접 제어하고 싶은 경우, `config/logging.php`에 `custom` 드라이버를 지정해 채널을 만들 수 있습니다. 이때, Monolog 인스턴스를 생성할 팩토리 클래스명을 `via` 옵션에 입력합니다.

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

<!-- Once you have configured the `custom` driver channel, you're ready to define the class that will create your Monolog instance. This class only needs a single `__invoke` method which should return the Monolog logger instance. The method will receive the channels configuration array as its only argument: -->
이제, `custom` 드라이버용 클래스를 생성하면 됩니다. 이 클래스는 단 하나의 `__invoke` 메서드만 있으면 되며, 이 메서드는 채널 설정 배열을 인자로 받아 Monolog 로거 인스턴스를 반환해야 합니다.

```
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
애플리케이션 로그를 실시간으로 모니터링해야 할 때가 많습니다. 예를 들어, 문제를 디버깅하거나 특정 에러 유형을 실시간으로 감시하고 싶을 때가 있습니다.

<!-- Laravel Pail is a package that allows you to easily dive into your Laravel application's log files directly from the command line. Unlike the standard `tail` command, Pail is designed to work with any log driver, including Sentry or Flare. In addition, Pail provides a set of useful filters to help you quickly find what you're looking for. -->
Laravel Pail은 CLI에서 Laravel 애플리케이션 로그 파일을 손쉽게 탐색할 수 있도록 도와주는 패키지입니다. 표준 `tail` 커맨드와 달리, Pail은 Sentry나 Flare 등 어떤 로그 드라이버와도 연동됩니다. 또한, 원하는 정보를 빠르게 찾을 수 있도록 다양한 필터 기능도 제공합니다.

<!-- <img src="https://laravel.com/img/docs/pail-example.png"/> -->
<img src="https://laravel.com/img/docs/pail-example.png" />

<a name="pail-installation"></a>
<!-- ### Installation -->
### Installation

> [!WARNING]
> Laravel Pail은 [PHP 8.2+](https://php.net/releases/) 및 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 확장이 필요합니다.

<!-- To get started, install Pail into your project using the Composer package manager: -->
먼저, Composer 패키지 매니저를 이용해 Pail을 프로젝트에 설치하세요.

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
<!-- ### Usage -->
### Usage

<!-- To start tailing logs, run the `pail` command: -->
로그를 실시간으로 확인하려면 다음처럼 `pail` 명령어를 실행하세요.

```bash
php artisan pail
```

<!-- To increase the verbosity of the output and avoid truncation (…), use the `-v` option: -->
출력의 상세 정도를 높이고 줄임표(…) 없이 전체 로그를 보려면 `-v` 옵션을 사용합니다.

```bash
php artisan pail -v
```

<!-- For maximum verbosity and to display exception stack traces, use the `-vv` option: -->
최고 수준의 상세 출력과 예외 발생 시 스택 트레이스까지 보고 싶다면 `-vv` 옵션을 사용하세요.

```bash
php artisan pail -vv
```

<!-- To stop tailing logs, press `Ctrl+C` at any time. -->
로그 실시간 출력을 중지하려면 언제든 `Ctrl+C`를 누르면 됩니다.

<a name="pail-filtering-logs"></a>
<!-- ### Filtering Logs -->
### Filtering Logs

<a name="pail-filtering-logs-filter-option"></a>
<!-- #### `--filter` -->
#### `--filter`

<!-- You may use the `--filter` option to filter logs by their type, file, message, and stack trace content: -->
`--filter` 옵션을 사용하면 로그의 타입, 파일, 메시지, 스택 트레이스 내용을 기준으로 필터링할 수 있습니다.

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
<!-- #### `--message` -->
#### `--message`

<!-- To filter logs by only their message, you may use the `--message` option: -->
로그 메시지만을 기준으로 필터링하고 싶을 때는 `--message` 옵션을 사용하세요.

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
<!-- #### `--level` -->
#### `--level`

<!-- The `--level` option may be used to filter logs by their [log level](#log-levels): -->
`--level` 옵션을 사용하면 [log level](#log-levels)별로 로그를 필터링할 수 있습니다.

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
<!-- #### `--user` -->
#### `--user`

<!-- To only display logs that were written while a given user was authenticated, you may provide the user's ID to the `--user` option: -->
특정 사용자가 인증된 상태에서 기록된 로그만 보고 싶을 땐, 해당 사용자의 ID를 `--user` 옵션에 전달하세요.

```bash
php artisan pail --user=1
```
