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
アプリケーション内で何が起こっているかを詳しく知るために、Laravel はメッセージをファイル、システム エラー ログ、さらには Slack に記録してチーム全体に通知できる堅牢なログ サービスを提供します。

<!-- Laravel logging is based on "channels". Each channel represents a specific way of writing log information. For example, the `single` channel writes log files to a single log file, while the `slack` channel sends log messages to Slack. Log messages may be written to multiple channels based on their severity. -->
Laravelのロギングは「チャネル」に基づいています。各チャネルは、ログ情報を書き込む特定の方法を表します。たとえば、`single` チャネルはログ ファイルを 1 つのログ ファイルに書き込みますが、`slack` チャネルはログ メッセージを Slack に送信します。ログ メッセージは、重大度に基づいて複数のチャネルに書き込まれる場合があります。

<!-- Under the hood, Laravel utilizes the [Monolog](https://github.com/Seldaek/monolog) library, which provides support for a variety of powerful log handlers. Laravel makes it a cinch to configure these handlers, allowing you to mix and match them to customize your application's log handling. -->
Laravel は内部で、さまざまな強力なログ ハンドラーのサポートを提供する [Monolog](https://github.com/Seldaek/monolog) ライブラリを利用します。 Laravel を使用すると、これらのハンドラーの設定が簡単になり、それらを組み合わせてアプリケーションのログ処理をカスタマイズできるようになります。

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- All of the configuration options for your application's logging behavior are housed in the `config/logging.php` configuration file. This file allows you to configure your application's log channels, so be sure to review each of the available channels and their options. We'll review a few common options below. -->
アプリケーションのロギング動作の構成オプションはすべて、`config/logging.php` 構成ファイルに格納されています。このファイルを使用すると、アプリケーションのログ チャネルを構成できるため、使用可能な各チャネルとそのオプションを必ず確認してください。以下でいくつかの一般的なオプションを確認します。

<!-- By default, Laravel will use the `stack` channel when logging messages. The `stack` channel is used to aggregate multiple log channels into a single channel. For more information on building stacks, check out the [documentation below](#building-log-stacks). -->
デフォルトでは、Laravel はメッセージをログに記録するときに `stack` チャネルを使用します。 `stack` チャネルは、複数のログ チャネルを 1 つのチャネルに集約するために使用されます。スタックの構築の詳細については、[documentation below](#building-log-stacks) を確認してください。

<a name="configuring-the-channel-name"></a>
<!-- #### Configuring the Channel Name -->
#### Configuring the Channel Name

<!-- By default, Monolog is instantiated with a "channel name" that matches the current environment, such as `production` or `local`. To change this value, add a `name` option to your channel's configuration: -->
デフォルトでは、Monolog は、`production` や `local` など、現在の環境に一致する「チャネル名」でインスタンス化されます。この値を変更するには、チャネルの構成に `name` オプションを追加します。

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
各ログ チャネルは「ドライバ」によって駆動されます。ドライバは、ログ メッセージが実際にどのように、どこに記録されるかを決定します。次のログ チャネル ドライバは、すべての Laravel アプリケーションで利用できます。これらのドライバのほとんどのエントリはアプリケーションの `config/logging.php` 構成ファイルにすでに存在しているため、必ずこのファイルを確認してその内容を理解してください。

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
名前 |説明
------------- | -------------
`custom` |指定されたファクトリを呼び出してチャネルを作成するドライバ
`daily` |毎日ローテーションする `RotatingFileHandler` ベースの Monolog ドライバ
`errorlog` | `ErrorLogHandler` ベースの Monolog ドライバ
`monolog` |サポートされている Monolog ハンドラーを使用できる Monolog ファクトリ ドライバ
`papertrail` | `SyslogUdpHandler` ベースの Monolog ドライバ
`single` |単一のファイルまたはパスベースのロガーチャネル (`StreamHandler`)
`slack` | `SlackWebhookHandler` ベースの Monolog ドライバ
`stack` | 「マルチチャネル」チャネルの作成を容易にするラッパー
`syslog` | `SyslogHandler` ベースの Monolog ドライバ

<!-- </div> -->
</div>

> [!NOTE]
> `monolog` および `custom` ドライバの詳細については、[advanced channel customization](#monolog-channel-customization) のドキュメントを参照してください。

<a name="channel-prerequisites"></a>
<!-- ### Channel Prerequisites -->
### Channel Prerequisites

<a name="configuring-the-single-and-daily-channels"></a>
<!-- #### Configuring the Single and Daily Channels -->
#### Configuring the Single and Daily Channels

<!-- The `single` and `daily` channels have three optional configuration options: `bubble`, `permission`, and `locking`. -->
`single` および `daily` チャネルには、`bubble`、`permission`、および `locking` の 3 つのオプション構成オプションがあります。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Name | Description | Default
------------- | ------------- | -------------
`bubble` | Indicates if messages should bubble up to other channels after being handled | `true`
`locking` | Attempt to lock the log file before writing to it | `false`
`permission` | The log file's permissions | `0644`
-->
名前 | 説明 | デフォルト
------------- | ------------- | -------------
`bubble` | メッセージが処理された後に他のチャネルにバブルアップする必要があるかどうかを示します | `true`
`locking` | ログ ファイルに書き込む前にログ ファイルをロックしようとします | `false`
`permission` | ログファイルの権限 | `0644`

<!-- </div> -->
</div>

<!-- Additionally, the retention policy for the `daily` channel can be configured via the `days` option: -->
さらに、`daily` チャネルの保持ポリシーは、`days` オプションを使用して構成できます。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Name | Description                                                       | Default
------------- |-------------------------------------------------------------------| -------------
`days` | The number of days that daily log files should be retained | `7`
-->
名前 | 説明                                                       | デフォルト
------------- |-------------------------------------------------------------------| -------------
`days` | 毎日のログ ファイルを保持する日数 | `7`

<!-- </div> -->
</div>

<a name="configuring-the-papertrail-channel"></a>
<!-- #### Configuring the Papertrail Channel -->
#### Configuring the Papertrail Channel

<!-- The `papertrail` channel requires the `host` and `port` configuration options. You can obtain these values from [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app). -->
`papertrail` チャネルには、`host` および `port` 構成オプションが必要です。これらの値は、[Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app) から取得できます。

<a name="configuring-the-slack-channel"></a>
<!-- #### Configuring the Slack Channel -->
#### Configuring the Slack Channel

<!-- The `slack` channel requires a `url` configuration option. This URL should match a URL for an [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) that you have configured for your Slack team. -->
`slack` チャネルには、`url` 構成オプションが必要です。この URL は、Slack チーム用に構成した [incoming webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) の URL と一致する必要があります。

<!-- By default, Slack will only receive logs at the `critical` level and above; however, you can adjust this in your `config/logging.php` configuration file by modifying the `level` configuration option within your Slack log channel's configuration array. -->
デフォルトでは、Slack は `critical` レベル以上のログのみを受信します。ただし、Slack ログ チャネルの構成配列内の `level` 構成オプションを変更することで、`config/logging.php` 構成ファイルでこれを調整できます。

<a name="logging-deprecation-warnings"></a>
<!-- ### Logging Deprecation Warnings -->
### Logging Deprecation Warnings

<!-- PHP, Laravel, and other libraries often notify their users that some of their features have been deprecated and will be removed in a future version. If you would like to log these deprecation warnings, you may specify your preferred `deprecations` log channel in your application's `config/logging.php` configuration file: -->
PHP、Laravel、およびその他のライブラリは、機能の一部が非推奨になり、将来のバージョンで削除されることをユーザーに通知することがよくあります。これらの非推奨の警告をログに記録したい場合は、アプリケーションの `config/logging.php` 構成ファイルで優先する `deprecations` ログ チャネルを指定できます。

```
'deprecations' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),

'channels' => [
    ...
]
```

<!-- Or, you may define a log channel named `deprecations`. If a log channel with this name exists, it will always be used to log deprecations: -->
または、`deprecations` という名前のログ チャネルを定義することもできます。この名前のログ チャネルが存在する場合は、非推奨のログを記録するために常に使用されます。

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
前述したように、`stack` ドライバを使用すると、便宜上、複数のチャネルを 1 つのログ チャネルに結合できます。ログ スタックの使用方法を説明するために、運用アプリケーションで見られる構成例を見てみましょう。

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
この構成を詳しく見てみましょう。まず、`stack` チャネルが、`channels` オプションを介して他の 2 つのチャネル (`syslog` および `slack`) を集約していることに注目してください。したがって、メッセージをログに記録する場合、これらのチャネルの両方にメッセージをログに記録する機会があります。ただし、以下で説明するように、これらのチャネルが実際にメッセージをログに記録するかどうかは、メッセージの重大度/「レベル」によって決定される場合があります。

<a name="log-levels"></a>
<!-- #### Log Levels -->
#### Log Levels

<!-- Take note of the `level` configuration option present on the `syslog` and `slack` channel configurations in the example above. This option determines the minimum "level" a message must be in order to be logged by the channel. Monolog, which powers Laravel's logging services, offers all of the log levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424). In descending order of severity, these log levels are: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, and **debug**. -->
上記の例の `syslog` および `slack` チャネル構成に存在する `level` 構成オプションに注目してください。このオプションは、チャネルによってログに記録されるメッセージの最小「レベル」を決定します。 Laravel のロギング サービスを強化する Monolog は、[RFC 5424 specification](https://tools.ietf.org/html/rfc5424) で定義されたすべてのログ レベルを提供します。これらのログ レベルは、重大度の降順で、**緊急**、**アラート**、**重大**、**エラー**、**警告**、**通知**、**情報**、**デバッグ**です。

<!-- So, imagine we log a message using the `debug` method: -->
そこで、`debug` メソッドを使用してメッセージをログに記録するとします。

```
Log::debug('An informational message.');
```

<!-- Given our configuration, the `syslog` channel will write the message to the system log; however, since the error message is not `critical` or above, it will not be sent to Slack. However, if we log an `emergency` message, it will be sent to both the system log and Slack since the `emergency` level is above our minimum level threshold for both channels: -->
この構成では、`syslog` チャネルはメッセージをシステム ログに書き込みます。ただし、エラーメッセージは`critical`以上ではないため、Slackには送信されません。ただし、`emergency` メッセージをログに記録すると、`emergency` レベルが両方のチャネルの最小レベルしきい値を超えているため、メッセージはシステム ログと Slack の両方に送信されます。

```
Log::emergency('The system is down!');
```

<a name="writing-log-messages"></a>
<!-- ## Writing Log Messages -->
## Writing Log Messages

<!-- You may write information to the logs using the `Log` [facade](/docs/10.x/facades). As previously mentioned, the logger provides the eight logging levels defined in the [RFC 5424 specification](https://tools.ietf.org/html/rfc5424): **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info** and **debug**: -->
`Log` [facade](/docs/10.x/facades) を使用して、ログに情報を書き込むことができます。前述したように、ロガーは、[RFC 5424 specification](https://tools.ietf.org/html/rfc5424) で定義された 8 つのログ レベル (**緊急**、**アラート**、**クリティカル**、**エラー**、**警告**、**通知**、**情報**、**デバッグ**) を提供します。

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
これらのメソッドのいずれかを呼び出して、対応するレベルのメッセージをログに記録できます。デフォルトでは、メッセージは、`logging` 構成ファイルで構成されているデフォルトのログ チャネルに書き込まれます。

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
コンテキスト データの配列をログ メソッドに渡すことができます。このコンテキスト データはフォーマットされて、ログ メッセージとともに表示されます。

```
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```

<!-- Occasionally, you may wish to specify some contextual information that should be included with all subsequent log entries in a particular channel. For example, you may wish to log a request ID that is associated with each incoming request to your application. To accomplish this, you may call the `Log` facade's `withContext` method: -->
場合によっては、特定のチャネルの後続のすべてのログ エントリに含める必要があるコンテキスト情報を指定したい場合があります。たとえば、アプリケーションへの各受信リクエストに関連付けられたリクエスト ID をログに記録したい場合があります。これを実現するには、`Log` ファサードの `withContext` メソッドを呼び出します。

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
すべてのロギング チャネル間でコンテキスト情報を共有したい場合は、`Log::shareContext()` メソッドを呼び出すことができます。このメソッドは、作成されたすべてのチャネルとその後に作成されるチャネルにコンテキスト情報を提供します。

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
> キューに入れられたジョブの処理中にログ コンテキストを共有する必要がある場合は、[job middleware](/docs/10.x/queues#job-middleware) を利用できます。

<a name="writing-to-specific-channels"></a>
<!-- ### Writing to Specific Channels -->
### Writing to Specific Channels

<!-- Sometimes you may wish to log a message to a channel other than your application's default channel. You may use the `channel` method on the `Log` facade to retrieve and log to any channel defined in your configuration file: -->
場合によっては、アプリケーションのデフォルト チャネル以外のチャネルにメッセージを記録したい場合があります。 `Log` ファサードで `channel` メソッドを使用して、構成ファイルで定義されている任意のチャネルを取得してログに記録できます。

```
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```

<!-- If you would like to create an on-demand logging stack consisting of multiple channels, you may use the `stack` method: -->
複数のチャネルで構成されるオンデマンド ロギング スタックを作成したい場合は、`stack` メソッドを使用できます。

```
Log::stack(['single', 'slack'])->info('Something happened!');
```

<a name="on-demand-channels"></a>
<!-- #### On-Demand Channels -->
#### On-Demand Channels

<!-- It is also possible to create an on-demand channel by providing the configuration at runtime without that configuration being present in your application's `logging` configuration file. To accomplish this, you may pass a configuration array to the `Log` facade's `build` method: -->
アプリケーションの `logging` 構成ファイルにその構成が存在しなくても、実行時に構成を提供することでオンデマンド チャネルを作成することもできます。これを実現するには、構成配列を `Log` ファサードの `build` メソッドに渡すことができます。

```
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```

<!-- You may also wish to include an on-demand channel in an on-demand logging stack. This can be achieved by including your on-demand channel instance in the array passed to the `stack` method: -->
オンデマンド ログ スタックにオンデマンド チャネルを含めることもできます。これは、`stack` メソッドに渡される配列にオンデマンド チャネル インスタンスを含めることによって実現できます。

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
場合によっては、既存のチャネルに対して Monolog を構成する方法を完全に制御する必要がある場合があります。たとえば、Laravel の組み込み `single` チャネルに対してカスタム Monolog `FormatterInterface` 実装を構成することができます。

<!-- To get started, define a `tap` array on the channel's configuration. The `tap` array should contain a list of classes that should have an opportunity to customize (or "tap" into) the Monolog instance after it is created. There is no conventional location where these classes should be placed, so you are free to create a directory within your application to contain these classes: -->
まず、チャネルの構成で `tap` 配列を定義します。 `tap` 配列には、Monolog インスタンスの作成後にカスタマイズ (または「利用」) する機会を持つクラスのリストが含まれている必要があります。これらのクラスを配置する従来の場所はないため、アプリケーション内にこれらのクラスを含むディレクトリを自由に作成できます。

```
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
],
```

<!-- Once you have configured the `tap` option on your channel, you're ready to define the class that will customize your Monolog instance. This class only needs a single method: `__invoke`, which receives an `Illuminate\Log\Logger` instance. The `Illuminate\Log\Logger` instance proxies all method calls to the underlying Monolog instance: -->
チャネルで `tap` オプションを構成したら、Monolog インスタンスをカスタマイズするクラスを定義する準備が整います。このクラスには、`Illuminate\Log\Logger` インスタンスを受け取る 1 つのメソッド `__invoke` のみが必要です。 `Illuminate\Log\Logger` インスタンスは、すべてのメソッド呼び出しを基になる Monolog インスタンスにプロキシします。

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
> すべての「タップ」クラスは [service container](/docs/10.x/container) によって解決されるため、必要なコンストラクターの依存関係は自動的に挿入されます。

<a name="creating-monolog-handler-channels"></a>
<!-- ### Creating Monolog Handler Channels -->
### Creating Monolog Handler Channels

<!-- Monolog has a variety of [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) and Laravel does not include a built-in channel for each one. In some cases, you may wish to create a custom channel that is merely an instance of a specific Monolog handler that does not have a corresponding Laravel log driver.  These channels can be easily created using the `monolog` driver. -->
Monolog にはさまざまな [available handlers](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) があり、Laravel にはそれぞれの組み込みチャネルが含まれていません。場合によっては、対応する Laravel ログ ドライバを持たない特定の Monolog ハンドラーのインスタンスにすぎないカスタム チャネルを作成したい場合があります。  これらのチャネルは、`monolog` ドライバを使用して簡単に作成できます。

<!-- When using the `monolog` driver, the `handler` configuration option is used to specify which handler will be instantiated. Optionally, any constructor parameters the handler needs may be specified using the `with` configuration option: -->
`monolog` ドライバを使用する場合、`handler` 構成オプションを使用して、インスタンス化されるハンドラーを指定します。オプションで、ハンドラーに必要なコンストラクター パラメーターは、`with` 構成オプションを使用して指定できます。

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
`monolog` ドライバを使用する場合、Monolog `LineFormatter` がデフォルトのフォーマッタとして使用されます。ただし、`formatter` および `formatter_with` 構成オプションを使用して、ハンドラーに渡されるフォーマッタのタイプをカスタマイズできます。

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
独自のフォーマッタを提供できる Monolog ハンドラーを使用している場合は、`formatter` 構成オプションの値を `default` に設定できます。

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
Monolog は、メッセージをログに記録する前にメッセージを処理することもできます。独自のプロセッサを作成することも、[existing processors offered by Monolog](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor) を使用することもできます。

<!--  If you would like to customize the processors for a `monolog` driver, add a `processors` configuration value to your channel's configuration: -->
`monolog` ドライバのプロセッサーをカスタマイズする場合は、チャネルの構成に `processors` 構成値を追加します。

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
Monolog のインスタンス化と構成を完全に制御できる完全なカスタム チャネルを定義したい場合は、`config/logging.php` 構成ファイルで `custom` ドライバ タイプを指定できます。構成には、Monolog インスタンスを作成するために呼び出されるファクトリ クラスの名前を含む `via` オプションが含まれている必要があります。

```
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```

<!-- Once you have configured the `custom` driver channel, you're ready to define the class that will create your Monolog instance. This class only needs a single `__invoke` method which should return the Monolog logger instance. The method will receive the channels configuration array as its only argument: -->
`custom` ドライバ チャネルを構成したら、Monolog インスタンスを作成するクラスを定義する準備が整います。このクラスには、Monolog ロガー インスタンスを返す `__invoke` メソッドが 1 つだけ必要です。このメソッドは、チャネル構成配列を唯一の引数として受け取ります。

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
多くの場合、アプリケーションのログをリアルタイムで追跡する必要があるかもしれません。たとえば、問題をデバッグする場合や、アプリケーションのログで特定の種類のエラーを監視する場合などです。

<!-- Laravel Pail is a package that allows you to easily dive into your Laravel application's log files directly from the command line. Unlike the standard `tail` command, Pail is designed to work with any log driver, including Sentry or Flare. In addition, Pail provides a set of useful filters to help you quickly find what you're looking for. -->
Laravel Pail は、コマンドラインから直接 Laravel アプリケーションのログファイルに簡単にアクセスできるパッケージです。標準の `tail` コマンドとは異なり、Pail は Sentry や Flare を含むあらゆるログ ドライバで動作するように設計されています。さらに、Pail は、探しているものをすばやく見つけるのに役立つ一連の便利なフィルターを提供します。

<!-- <img src="https://laravel.com/img/docs/pail-example.png"/> -->
<img src="https://laravel.com/img/docs/pail-example.png"/>

<a name="pail-installation"></a>
<!-- ### Installation -->
### Installation

> [!WARNING]
> Laravel Pail には、[PHP 8.2+](https://php.net/releases/) および [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 拡張機能が必要です。

<!-- To get started, install Pail into your project using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Pail をプロジェクトにインストールします。

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
<!-- ### Usage -->
### Usage

<!-- To start tailing logs, run the `pail` command: -->
ログの追跡を開始するには、`pail` コマンドを実行します。

```bash
php artisan pail
```

<!-- To increase the verbosity of the output and avoid truncation (…), use the `-v` option: -->
出力の冗長性を高め、切り捨て (…) を回避するには、`-v` オプションを使用します。

```bash
php artisan pail -v
```

<!-- For maximum verbosity and to display exception stack traces, use the `-vv` option: -->
冗長性を最大限に高め、例外スタック トレースを表示するには、`-vv` オプションを使用します。

```bash
php artisan pail -vv
```

<!-- To stop tailing logs, press `Ctrl+C` at any time. -->
ログの追跡を停止するには、いつでも `Ctrl+C` を押してください。

<a name="pail-filtering-logs"></a>
<!-- ### Filtering Logs -->
### Filtering Logs

<a name="pail-filtering-logs-filter-option"></a>
<!-- #### `--filter` -->
#### `--filter`

<!-- You may use the `--filter` option to filter logs by their type, file, message, and stack trace content: -->
`--filter` オプションを使用すると、タイプ、ファイル、メッセージ、スタック トレースの内容によってログをフィルタリングできます。

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
<!-- #### `--message` -->
#### `--message`

<!-- To filter logs by only their message, you may use the `--message` option: -->
メッセージのみでログをフィルターするには、`--message` オプションを使用できます。

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
<!-- #### `--level` -->
#### `--level`

<!-- The `--level` option may be used to filter logs by their [log level](#log-levels): -->
`--level` オプションは、[log level](#log-levels) でログをフィルタリングするために使用できます。

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
<!-- #### `--user` -->
#### `--user`

<!-- To only display logs that were written while a given user was authenticated, you may provide the user's ID to the `--user` option: -->
特定のユーザーが認証されている間に書き込まれたログのみを表示するには、ユーザーの ID を `--user` オプションに指定します。

```bash
php artisan pail --user=1
```

