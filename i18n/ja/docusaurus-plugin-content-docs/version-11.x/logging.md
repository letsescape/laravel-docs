# ロギング (Logging)

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [利用可能なチャネルドライバ](#available-channel-drivers)
    - [チャネルの前提条件](#channel-prerequisites)
    - [非推奨の警告のログ記録](#logging-deprecation-warnings)
- [ログスタックの構築](#building-log-stacks)
- [ログメッセージの書き込み](#writing-log-messages)
    - [コンテキスト情報](#contextual-information)
    - [特定のチャネルへの書き込み](#writing-to-specific-channels)
- [モノログチャンネルのカスタマイズ](#monolog-channel-customization)
    - [チャンネルのモノログのカスタマイズ](#customizing-monolog-for-channels)
    - [モノログ ハンドラー チャネルの作成](#creating-monolog-handler-channels)
    - [ファクトリ経由でカスタム チャネルを作成する](#creating-custom-channels-via-factories)
- [Pail を使用したログ メッセージの追跡](#tailing-log-messages-using-pail)
    - [Installation](#pail-installation)
    - [Usage](#pail-usage)
    - [ログのフィルタリング](#pail-filtering-logs)

<a name="introduction"></a>
## 導入 (Introduction)

アプリケーション内で何が起こっているかを詳しく知るために、Laravel はメッセージをファイル、システム エラー ログ、さらには Slack に記録してチーム全体に通知できる堅牢なログ サービスを提供します。

Laravelのロギングは「チャネル」に基づいています。各チャネルは、ログ情報を書き込む特定の方法を表します。たとえば、`single` チャネルはログ ファイルを 1 つのログ ファイルに書き込みますが、`slack` チャネルはログ メッセージを Slack に送信します。ログ メッセージは、重大度に基づいて複数のチャネルに書き込まれる場合があります。

Laravel は内部で、さまざまな強力なログ ハンドラーのサポートを提供する [Monolog](https://github.com/Seldaek/monolog) ライブラリを利用します。 Laravel を使用すると、これらのハンドラーの設定が簡単になり、それらを組み合わせてアプリケーションのログ処理をカスタマイズできるようになります。

<a name="configuration"></a>
## 構成 (Configuration)

アプリケーションのロギング動作を制御するすべての構成オプションは、`config/logging.php` 構成ファイルに格納されています。このファイルを使用すると、アプリケーションのログ チャネルを構成できるため、使用可能な各チャネルとそのオプションを必ず確認してください。以下でいくつかの一般的なオプションを確認します。

デフォルトでは、Laravel はメッセージをログに記録するときに `stack` チャネルを使用します。 `stack` チャネルは、複数のログ チャネルを 1 つのチャネルに集約するために使用されます。スタックの構築の詳細については、[以下のドキュメント](#building-log-stacks) を確認してください。

<a name="available-channel-drivers"></a>
### 利用可能なチャネルドライバ

各ログ チャネルは「ドライバ」によって駆動されます。ドライバは、ログ メッセージが実際にどのように、どこに記録されるかを決定します。次のログ チャネル ドライバは、すべての Laravel アプリケーションで利用できます。これらのドライバのほとんどのエントリはアプリケーションの `config/logging.php` 構成ファイルにすでに存在しているため、必ずこのファイルを確認してその内容を理解してください。

<div class="overflow-auto">

| 名前         | 説明                                                          |
| ------------ | -------------------------------------------------------------------- |
| `custom`     | 指定されたファクトリを呼び出してチャネルを作成するドライバ。         |
| `daily`      | 毎日ローテーションする `RotatingFileHandler` ベースの Monolog ドライバ。    |
| `errorlog`   | `ErrorLogHandler` ベースの Monolog ドライバ。                           |
| `monolog`    | サポートされている Monolog ハンドラーを使用できる Monolog ファクトリ ドライバ。 |
| `papertrail` | `SyslogUdpHandler` ベースの Monolog ドライバ。                           |
| `single`     | 単一のファイルまたはパス ベースのロガー チャネル (`StreamHandler`)。        |
| `slack`      | `SlackWebhookHandler` ベースの Monolog ドライバ。                        |
| `stack`      | 「マルチチャネル」チャネルの作成を容易にするラッパー。           |
| `syslog`     | `SyslogHandler` ベースの Monolog ドライバ。                              |

</div>

> [!NOTE]  
> `monolog` および `custom` ドライバの詳細については、[高度なチャネルのカスタマイズ](#monolog-channel-customization) のドキュメントを参照してください。

<a name="configuring-the-channel-name"></a>
#### チャンネル名の設定

デフォルトでは、Monolog は、`production` や `local` など、現在の環境に一致する「チャネル名」でインスタンス化されます。この値を変更するには、チャネルの構成に `name` オプションを追加します。

    'stack' => [
        'driver' => 'stack',
        'name' => 'channel-name',
        'channels' => ['single', 'slack'],
    ],

<a name="channel-prerequisites"></a>
### チャネルの前提条件

<a name="configuring-the-single-and-daily-channels"></a>
#### 単一チャネルと日次チャネルの構成

`single` および `daily` チャネルには、`bubble`、`permission`、および `locking` の 3 つのオプション構成オプションがあります。

<div class="overflow-auto">

| 名前         | 説明                                                                   | デフォルト |
| ------------ | ----------------------------------------------------------------------------- | ------- |
| `bubble`     | メッセージが処理された後に他のチャネルにバブルアップする必要があるかどうかを示します。 | `true`  |
| `locking`    | ログ ファイルに書き込む前に、ログ ファイルをロックしてみてください。                            | `false` |
| `permission` | ログ ファイルの権限。                                                   | `0644`  |

</div>

さらに、`daily` チャネルの保持ポリシーは、`LOG_DAILY_DAYS` 環境変数を介して、または `days` 構成オプションを設定することによって構成できます。

<div class="overflow-auto">

| 名前   | 説明                                                 | デフォルト |
| ------ | ----------------------------------------------------------- | ------- |
| `days` | 毎日のログ ファイルを保持する日数。 | `14`    |

</div>

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail チャネルの構成

`papertrail` チャネルには、`host` および `port` 構成オプションが必要です。これらは、`PAPERTRAIL_URL` および `PAPERTRAIL_PORT` 環境変数を介して定義できます。これらの値は、[Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app) から取得できます。

<a name="configuring-the-slack-channel"></a>
#### Slack チャネルの構成

`slack` チャネルには、`url` 構成オプションが必要です。この値は、`LOG_SLACK_WEBHOOK_URL` 環境変数を介して定義できます。この URL は、Slack チーム用に構成した [受信 Webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) の URL と一致する必要があります。

デフォルトでは、Slack は `critical` レベル以上のログのみを受信します。ただし、`LOG_LEVEL` 環境変数を使用するか、Slack ログ チャネルの構成配列内の `level` 構成オプションを変更することで、これを調整できます。

<a name="logging-deprecation-warnings"></a>
### 非推奨の警告のログ記録

PHP、Laravel、およびその他のライブラリは、機能の一部が非推奨になり、将来のバージョンで削除されることをユーザーに通知することがよくあります。これらの非推奨の警告をログに記録したい場合は、`LOG_DEPRECATIONS_CHANNEL` 環境変数を使用するか、アプリケーションの `config/logging.php` 構成ファイル内で、優先する `deprecations` ログ チャネルを指定できます。

    'deprecations' => [
        'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
        'trace' => env('LOG_DEPRECATIONS_TRACE', false),
    ],

    'channels' => [
        // ...
    ]

または、`deprecations` という名前のログ チャネルを定義することもできます。この名前のログ チャネルが存在する場合は、非推奨のログを記録するために常に使用されます。

    'channels' => [
        'deprecations' => [
            'driver' => 'single',
            'path' => storage_path('logs/php-deprecation-warnings.log'),
        ],
    ],

<a name="building-log-stacks"></a>
## ログスタックの構築 (Building Log Stacks)

前述したように、`stack` ドライバを使用すると、便宜上、複数のチャネルを 1 つのログ チャネルに結合できます。ログ スタックの使用方法を説明するために、運用アプリケーションで見られる構成例を見てみましょう。

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

この構成を詳しく見てみましょう。まず、`stack` チャネルが、`channels` オプションを介して他の 2 つのチャネル (`syslog` および `slack`) を集約していることに注目してください。したがって、メッセージをログに記録する場合、これらのチャネルの両方にメッセージをログに記録する機会があります。ただし、以下で説明するように、これらのチャネルが実際にメッセージをログに記録するかどうかは、メッセージの重大度/「レベル」によって決定される場合があります。

<a name="log-levels"></a>
#### ログレベル

上記の例の `syslog` および `slack` チャネル構成に存在する `level` 構成オプションに注目してください。このオプションは、チャネルによってログに記録されるメッセージの最小「レベル」を決定します。 Laravel のロギング サービスを強化する Monolog は、[RFC 5424仕様](https://tools.ietf.org/html/rfc5424) で定義されたすべてのログ レベルを提供します。これらのログ レベルは、重大度の降順で、**緊急**、**アラート**、**重大**、**エラー**、*警告**、**通知**、**情報**、**デバッグ**です。

そこで、`debug` メソッドを使用してメッセージをログに記録するとします。

    Log::debug('An informational message.');

この構成では、`syslog` チャネルはメッセージをシステム ログに書き込みます。ただし、エラーメッセージは`critical`以上ではないため、Slackには送信されません。ただし、`emergency` メッセージをログに記録すると、`emergency` レベルが両方のチャネルの最小レベルしきい値を超えているため、メッセージはシステム ログと Slack の両方に送信されます。

    Log::emergency('The system is down!');

<a name="writing-log-messages"></a>
## ログメッセージの書き込み (Writing Log Messages)

`Log` [facade](/docs/{{version}}/facades) を使用して、ログに情報を書き込むことができます。前述したように、ロガーは、[RFC 5424仕様](https://tools.ietf.org/html/rfc5424) で定義された 8 つのログ レベル (**緊急**、**アラート**、**クリティカル**、*エラー**、**警告**、**通知**、**情報**、**デバッグ**) を提供します。

    use Illuminate\Support\Facades\Log;

    Log::emergency($message);
    Log::alert($message);
    Log::critical($message);
    Log::error($message);
    Log::warning($message);
    Log::notice($message);
    Log::info($message);
    Log::debug($message);

これらのメソッドのいずれかを呼び出して、対応するレベルのメッセージをログに記録できます。デフォルトでは、メッセージは、`logging` 構成ファイルで構成されているデフォルトのログ チャネルに書き込まれます。

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

<a name="contextual-information"></a>
### コンテキスト情報

コンテキスト データの配列をログ メソッドに渡すことができます。このコンテキスト データはフォーマットされて、ログ メッセージとともに表示されます。

    use Illuminate\Support\Facades\Log;

    Log::info('User {id} failed to login.', ['id' => $user->id]);

場合によっては、特定のチャネルの後続のすべてのログ エントリに含める必要があるコンテキスト情報を指定したい場合があります。たとえば、アプリケーションへの各受信リクエストに関連付けられたリクエスト ID をログに記録したい場合があります。これを実現するには、`Log` ファサードの `withContext` メソッドを呼び出します。

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

すべてのロギング チャネル間でコンテキスト情報を共有したい場合は、`Log::shareContext()` メソッドを呼び出すことができます。このメソッドは、作成されたすべてのチャネルとその後に作成されるチャネルにコンテキスト情報を提供します。

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

> [!NOTE]  
> キューに入れられたジョブの処理中にログ コンテキストを共有する必要がある場合は、[ジョブミドルウェア](/docs/{{version}}/queues#job-middleware) を利用できます。

<a name="writing-to-specific-channels"></a>
### 特定のチャネルへの書き込み

場合によっては、アプリケーションのデフォルト チャネル以外のチャネルにメッセージを記録したい場合があります。 `Log` ファサードで `channel` メソッドを使用して、構成ファイルで定義されている任意のチャネルを取得してログに記録できます。

    use Illuminate\Support\Facades\Log;

    Log::channel('slack')->info('Something happened!');

複数のチャネルで構成されるオンデマンド ロギング スタックを作成したい場合は、`stack` メソッドを使用できます。

    Log::stack(['single', 'slack'])->info('Something happened!');

<a name="on-demand-channels"></a>
#### オンデマンドチャネル

アプリケーションの `logging` 構成ファイルにその構成が存在しなくても、実行時に構成を提供することでオンデマンド チャネルを作成することもできます。これを実現するには、構成配列を `Log` ファサードの `build` メソッドに渡すことができます。

    use Illuminate\Support\Facades\Log;

    Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ])->info('Something happened!');

オンデマンド ログ スタックにオンデマンド チャネルを含めることもできます。これは、`stack` メソッドに渡される配列にオンデマンド チャネル インスタンスを含めることによって実現できます。

    use Illuminate\Support\Facades\Log;

    $channel = Log::build([
      'driver' => 'single',
      'path' => storage_path('logs/custom.log'),
    ]);

    Log::stack(['slack', $channel])->info('Something happened!');

<a name="monolog-channel-customization"></a>
## モノログチャンネルのカスタマイズ (Monolog Channel Customization)

<a name="customizing-monolog-for-channels"></a>
### チャンネルのモノログのカスタマイズ

場合によっては、既存のチャネルに対して Monolog を構成する方法を完全に制御する必要がある場合があります。たとえば、Laravel の組み込み `single` チャネルに対してカスタム Monolog `FormatterInterface` 実装を構成することができます。

まず、チャネルの構成で `tap` 配列を定義します。 `tap` 配列には、Monolog インスタンスの作成後にカスタマイズ (または「利用」) する機会を持つクラスのリストが含まれている必要があります。これらのクラスを配置する従来の場所はないため、アプリケーション内にこれらのクラスを含むディレクトリを自由に作成できます。

    'single' => [
        'driver' => 'single',
        'tap' => [App\Logging\CustomizeFormatter::class],
        'path' => storage_path('logs/laravel.log'),
        'level' => env('LOG_LEVEL', 'debug'),
        'replace_placeholders' => true,
    ],

チャネルで `tap` オプションを構成したら、Monolog インスタンスをカスタマイズするクラスを定義する準備が整います。このクラスには、`Illuminate\Log\Logger` インスタンスを受け取る 1 つのメソッド `__invoke` のみが必要です。 `Illuminate\Log\Logger` インスタンスは、すべてのメソッド呼び出しを基になる Monolog インスタンスにプロキシします。

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

> [!NOTE]  
> すべての「タップ」クラスは [サービスコンテナ](/docs/{{version}}/container) によって解決されるため、必要なコンストラクターの依存関係は自動的に挿入されます。

<a name="creating-monolog-handler-channels"></a>
### モノログ ハンドラー チャネルの作成

Monolog にはさまざまな [利用可能なハンドラー](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler) があり、Laravel にはそれぞれの組み込みチャネルが含まれていません。場合によっては、対応する Laravel ログ ドライバを持たない特定の Monolog ハンドラーのインスタンスにすぎないカスタム チャネルを作成したい場合があります。  これらのチャネルは、`monolog` ドライバを使用して簡単に作成できます。

`monolog` ドライバを使用する場合、`handler` 構成オプションを使用して、インスタンス化されるハンドラーを指定します。オプションで、ハンドラーに必要なコンストラクター パラメーターは、`with` 構成オプションを使用して指定できます。

    'logentries' => [
        'driver'  => 'monolog',
        'handler' => Monolog\Handler\SyslogUdpHandler::class,
        'with' => [
            'host' => 'my.logentries.internal.datahubhost.company.com',
            'port' => '10000',
        ],
    ],

<a name="monolog-formatters"></a>
#### モノログ フォーマッタ

`monolog` ドライバを使用する場合、Monolog `LineFormatter` がデフォルトのフォーマッタとして使用されます。ただし、`formatter` および `formatter_with` 構成オプションを使用して、ハンドラーに渡されるフォーマッタのタイプをカスタマイズできます。

    'browser' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\BrowserConsoleHandler::class,
        'formatter' => Monolog\Formatter\HtmlFormatter::class,
        'formatter_with' => [
            'dateFormat' => 'Y-m-d',
        ],
    ],

独自のフォーマッタを提供できる Monolog ハンドラーを使用している場合は、`formatter` 構成オプションの値を `default` に設定できます。

    'newrelic' => [
        'driver' => 'monolog',
        'handler' => Monolog\Handler\NewRelicHandler::class,
        'formatter' => 'default',
    ],

<a name="monolog-processors"></a>
#### モノログプロセッサ

Monolog は、メッセージをログに記録する前にメッセージを処理することもできます。独自のプロセッサを作成することも、[Monolog が提供する既存のプロセッサ](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor) を使用することもできます。

`monolog` ドライバのプロセッサーをカスタマイズする場合は、チャネルの構成に `processors` 構成値を追加します。

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

<a name="creating-custom-channels-via-factories"></a>
### ファクトリ経由でカスタム チャネルを作成する

Monolog のインスタンス化と構成を完全に制御できる完全なカスタム チャネルを定義したい場合は、`config/logging.php` 構成ファイルで `custom` ドライバ タイプを指定できます。構成には、Monolog インスタンスを作成するために呼び出されるファクトリ クラスの名前を含む `via` オプションが含まれている必要があります。

    'channels' => [
        'example-custom-channel' => [
            'driver' => 'custom',
            'via' => App\Logging\CreateCustomLogger::class,
        ],
    ],

`custom` ドライバ チャネルを構成したら、Monolog インスタンスを作成するクラスを定義する準備が整います。このクラスには、Monolog ロガー インスタンスを返す `__invoke` メソッドが 1 つだけ必要です。このメソッドは、チャネル構成配列を唯一の引数として受け取ります。

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

<a name="tailing-log-messages-using-pail"></a>
## Pail を使用したログ メッセージの追跡 (Tailing Log Messages Using Pail)

多くの場合、アプリケーションのログをリアルタイムで追跡する必要があるかもしれません。たとえば、問題をデバッグする場合や、アプリケーションのログで特定の種類のエラーを監視する場合などです。

Laravel Pail は、コマンドラインから直接 Laravel アプリケーションのログファイルに簡単にアクセスできるパッケージです。標準の `tail` コマンドとは異なり、Pail は Sentry や Flare を含むあらゆるログ ドライバで動作するように設計されています。さらに、Pail は、探しているものをすばやく見つけるのに役立つ一連の便利なフィルターを提供します。

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### インストール

> [!WARNING]  
> Laravel Pail には、[PHP 8.2+](https://php.net/releases/) および [PCNTL](https://www.php.net/manual/en/book.pcntl.php) 拡張機能が必要です。

まず、Composer パッケージ マネージャーを使用して Pail をプロジェクトにインストールします。

```bash
composer require laravel/pail
```

<a name="pail-usage"></a>
### 使用法

ログの追跡を開始するには、`pail` コマンドを実行します。

```bash
php artisan pail
```

出力の冗長性を高め、切り捨て (…) を回避するには、`-v` オプションを使用します。

```bash
php artisan pail -v
```

冗長性を最大限に高め、例外スタック トレースを表示するには、`-vv` オプションを使用します。

```bash
php artisan pail -vv
```

ログの追跡を停止するには、いつでも `Ctrl+C` を押してください。

<a name="pail-filtering-logs"></a>
### ログのフィルタリング

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

`--filter` オプションを使用すると、タイプ、ファイル、メッセージ、スタック トレースの内容によってログをフィルタリングできます。

```bash
php artisan pail --filter="QueryException"
```

<a name="pail-filtering-logs-message-option"></a>
#### `--message`

メッセージのみでログをフィルターするには、`--message` オプションを使用できます。

```bash
php artisan pail --message="User created"
```

<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` オプションは、[ログレベル](#log-levels) でログをフィルタリングするために使用できます。

```bash
php artisan pail --level=error
```

<a name="pail-filtering-logs-user-option"></a>
#### `--user`

特定のユーザーが認証されている間に書き込まれたログのみを表示するには、ユーザーの ID を `--user` オプションに指定します。

```bash
php artisan pail --user=1
```

