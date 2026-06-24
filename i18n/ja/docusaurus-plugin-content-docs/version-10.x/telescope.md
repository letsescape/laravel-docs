<!-- # Laravel Telescope -->
# Laravel Telescope

- [Introduction](#introduction)
- [Installation](#installation)
    - [Local Only Installation](#local-only-installation)
    - [Configuration](#configuration)
    - [Data Pruning](#data-pruning)
    - [Dashboard Authorization](#dashboard-authorization)
- [Upgrading Telescope](#upgrading-telescope)
- [Filtering](#filtering)
    - [Entries](#filtering-entries)
    - [Batches](#filtering-batches)
- [Tagging](#tagging)
- [Available Watchers](#available-watchers)
    - [Batch Watcher](#batch-watcher)
    - [Cache Watcher](#cache-watcher)
    - [Command Watcher](#command-watcher)
    - [Dump Watcher](#dump-watcher)
    - [Event Watcher](#event-watcher)
    - [Exception Watcher](#exception-watcher)
    - [Gate Watcher](#gate-watcher)
    - [HTTP Client Watcher](#http-client-watcher)
    - [Job Watcher](#job-watcher)
    - [Log Watcher](#log-watcher)
    - [Mail Watcher](#mail-watcher)
    - [Model Watcher](#model-watcher)
    - [Notification Watcher](#notification-watcher)
    - [Query Watcher](#query-watcher)
    - [Redis Watcher](#redis-watcher)
    - [Request Watcher](#request-watcher)
    - [Schedule Watcher](#schedule-watcher)
    - [View Watcher](#view-watcher)
- [Displaying User Avatars](#displaying-user-avatars)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Telescope](https://github.com/laravel/telescope) makes a wonderful companion to your local Laravel development environment. Telescope provides insight into the requests coming into your application, exceptions, log entries, database queries, queued jobs, mail, notifications, cache operations, scheduled tasks, variable dumps, and more. -->
[Laravel Telescope](https://github.com/laravel/telescope) は、ローカルの Laravel 開発環境の素晴らしいパートナーになります。 Telescope は、アプリケーションに送られるリクエスト、例外、ログ エントリ、データベース クエリ、キューに入れられたジョブ、メール、通知、キャッシュ操作、スケジュールされたタスク、変数ダンプなどに関する洞察を提供します。

<!-- <img src="https://laravel.com/img/docs/telescope-example.png"/> -->
<img src="https://laravel.com/img/docs/telescope-example.png"/>

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may use the Composer package manager to install Telescope into your Laravel project: -->
Composer パッケージ マネージャーを使用して、Telescope を Laravel プロジェクトにインストールできます。

```shell
composer require laravel/telescope
```

<!-- After installing Telescope, publish its assets using the `telescope:install` Artisan command. After installing Telescope, you should also run the `migrate` command in order to create the tables needed to store Telescope's data: -->
Telescope をインストールした後、`telescope:install` Artisan コマンドを使用してそのアセットを公開します。 Telescope をインストールした後、Telescope のデータを保存するために必要なテーブルを作成するために、`migrate` コマンドも実行する必要があります。

```shell
php artisan telescope:install

php artisan migrate
```

<!-- Finally, you may access the Telescope dashboard via the `/telescope` route. -->
最後に、`/telescope` ルート経由で Telescope ダッシュボードにアクセスできます。

<a name="migration-customization"></a>
<!-- #### Migration Customization -->
#### Migration Customization

<!-- If you are not going to use Telescope's default migrations, you should call the `Telescope::ignoreMigrations` method in the `register` method of your application's `App\Providers\AppServiceProvider` class. You may export the default migrations using the following command: `php artisan vendor:publish --tag=telescope-migrations` -->
Telescope のデフォルトの移行を使用しない場合は、アプリケーションの `App\Providers\AppServiceProvider` クラスの `register` メソッドで `Telescope::ignoreMigrations` メソッドを呼び出す必要があります。次のコマンドを使用してデフォルトの移行をエクスポートできます: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
<!-- ### Local Only Installation -->
### Local Only Installation

<!-- If you plan to only use Telescope to assist your local development, you may install Telescope using the `--dev` flag: -->
ローカル開発を支援するためにのみ Telescope を使用する予定の場合は、`--dev` フラグを使用して Telescope をインストールできます。

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

<!-- After running `telescope:install`, you should remove the `TelescopeServiceProvider` service provider registration from your application's `config/app.php` configuration file. Instead, manually register Telescope's service providers in the `register` method of your `App\Providers\AppServiceProvider` class. We will ensure the current environment is `local` before registering the providers: -->
`telescope:install` を実行した後、アプリケーションの `config/app.php` 構成ファイルから `TelescopeServiceProvider` サービスプロバイダの登録を削除する必要があります。代わりに、`App\Providers\AppServiceProvider` クラスの `register` メソッドで Telescope のサービスプロバイダを手動で登録します。プロバイダを登録する前に、現在の環境が `local` であることを確認します。

```
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local')) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

<!-- Finally, you should also prevent the Telescope package from being [auto-discovered](/docs/10.x/packages#package-discovery) by adding the following to your `composer.json` file: -->
最後に、`composer.json` ファイルに以下を追加して、Telescope パッケージが [auto-discovered](/docs/10.x/packages#package-discovery) になるのを防ぐ必要もあります。

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Telescope's assets, its primary configuration file will be located at `config/telescope.php`. This configuration file allows you to configure your [watcher options](#available-watchers). Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
Telescope のアセットを公開すると、そのプライマリ構成ファイルは `config/telescope.php` に配置されます。この設定ファイルを使用すると、[watcher options](#available-watchers) を設定できます。各構成オプションにはその目的の説明が含まれているため、このファイルをよく調べてください。

<!-- If desired, you may disable Telescope's data collection entirely using the `enabled` configuration option: -->
必要に応じて、`enabled` 構成オプションを使用して Telescope のデータ収集を完全に無効にすることができます。

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
<!-- ### Data Pruning -->
### Data Pruning

<!-- Without pruning, the `telescope_entries` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/10.x/scheduling) the `telescope:prune` Artisan command to run daily: -->
プルーニングを行わない場合、`telescope_entries` テーブルは非常に迅速にレコードを蓄積できます。これを軽減するには、[schedule](/docs/10.x/scheduling) `telescope:prune` Artisan コマンドを毎日実行する必要があります。

```
$schedule->command('telescope:prune')->daily();
```

<!-- By default, all entries older than 24 hours will be pruned. You may use the `hours` option when calling the command to determine how long to retain Telescope data. For example, the following command will delete all records created over 48 hours ago: -->
デフォルトでは、24 時間より古いエントリはすべて削除されます。コマンドを呼び出すときに `hours` オプションを使用して、Telescope データを保持する期間を決定できます。たとえば、次のコマンドは 48 時間以上前に作成されたすべてのレコードを削除します。

```
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Telescope dashboard may be accessed via the `/telescope` route. By default, you will only be able to access this dashboard in the `local` environment. Within your `app/Providers/TelescopeServiceProvider.php` file, there is an [authorization gate](/docs/10.x/authorization#gates) definition. This authorization gate controls access to Telescope in **non-local** environments. You are free to modify this gate as needed to restrict access to your Telescope installation: -->
Telescope ダッシュボードには、`/telescope` ルート経由でアクセスできます。デフォルトでは、`local` 環境でのみこのダッシュボードにアクセスできます。 `app/Providers/TelescopeServiceProvider.php` ファイル内には、[authorization gate](/docs/10.x/authorization#gates) 定義があります。この認証ゲートは、**非ローカル**環境での Telescope へのアクセスを制御します。必要に応じてこのゲートを自由に変更して、Telescope インストールへのアクセスを制限できます。

```
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> 運用環境では、`APP_ENV` 環境変数を `production` に必ず変更する必要があります。そうしないと、Telescope のインストールが公開されてしまいます。

<a name="upgrading-telescope"></a>
<!-- ## Upgrading Telescope -->
## Upgrading Telescope

<!-- When upgrading to a new major version of Telescope, it's important that you carefully review [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md). -->
Telescope の新しいメジャー バージョンにアップグレードする場合は、[the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md) を注意深く確認することが重要です。

<!-- In addition, when upgrading to any new Telescope version, you should re-publish Telescope's assets: -->
さらに、新しい Telescope バージョンにアップグレードする場合は、Telescope のアセットを再公開する必要があります。

```shell
php artisan telescope:publish
```

<!-- To keep the assets up-to-date and avoid issues in future updates, you may add the `vendor:publish --tag=laravel-assets` command to the `post-update-cmd` scripts in your application's `composer.json` file: -->
アセットを最新の状態に保ち、今後の更新での問題を回避するには、アプリケーションの `composer.json` ファイル内の `post-update-cmd` スクリプトに `vendor:publish --tag=laravel-assets` コマンドを追加します。

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="filtering"></a>
<!-- ## Filtering -->
## Filtering

<a name="filtering-entries"></a>
<!-- ### Entries -->
### Entries

<!-- You may filter the data that is recorded by Telescope via the `filter` closure that is defined in your `App\Providers\TelescopeServiceProvider` class. By default, this closure records all data in the `local` environment and exceptions, failed jobs, scheduled tasks, and data with monitored tags in all other environments: -->
Telescope によって記録されたデータは、`App\Providers\TelescopeServiceProvider` クラスで定義されている `filter` クロージャを介してフィルタリングできます。デフォルトでは、このクロージャは、`local` 環境内のすべてのデータと、他のすべての環境内の例外、失敗したジョブ、スケジュールされたタスク、および監視対象のタグを持つデータを記録します。

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a name="filtering-batches"></a>
<!-- ### Batches -->
### Batches

<!-- While the `filter` closure filters data for individual entries, you may use the `filterBatch` method to register a closure that filters all data for a given request or console command. If the closure returns `true`, all of the entries are recorded by Telescope: -->
`filter` クロージャは個々のエントリのデータをフィルタリングしますが、`filterBatch` メソッドを使用して、特定のリクエストまたはコンソール コマンドのすべてのデータをフィルタリングするクロージャを登録できます。クロージャが `true` を返す場合、すべてのエントリが Telescope によって記録されます。

```
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a name="tagging"></a>
<!-- ## Tagging -->
## Tagging

<!-- Telescope allows you to search entries by "tag". Often, tags are Eloquent model class names or authenticated user IDs which Telescope automatically adds to entries. Occasionally, you may want to attach your own custom tags to entries. To accomplish this, you may use the `Telescope::tag` method. The `tag` method accepts a closure which should return an array of tags. The tags returned by the closure will be merged with any tags Telescope would automatically attach to the entry. Typically, you should call the `tag` method within the `register` method of your `App\Providers\TelescopeServiceProvider` class: -->
Telescope では、「タグ」によるエントリの検索が可能です。多くの場合、タグは Eloquent モデルのクラス名または認証されたユーザー ID であり、Telescope が自動的にエントリに追加します。場合によっては、エントリに独自のカスタム タグを添付したい場合があります。これを実現するには、`Telescope::tag` メソッドを使用できます。 `tag` メソッドは、タグの配列を返すクロージャを受け入れます。クロージャによって返されたタグは、Telescope が自動的にエントリに付加す​​るタグとマージされます。通常、`App\Providers\TelescopeServiceProvider` クラスの `register` メソッド内で `tag` メソッドを呼び出す必要があります。

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === 'request'
                    ? ['status:'.$entry->content['response_status']]
                    : [];
    });
 }
```

<a name="available-watchers"></a>
<!-- ## Available Watchers -->
## Available Watchers

<!-- Telescope "watchers" gather application data when a request or console command is executed. You may customize the list of watchers that you would like to enable within your `config/telescope.php` configuration file: -->
Telescopeの「ウォッチャー」は、リクエストまたはコンソール コマンドが実行されるときにアプリケーション データを収集します。 `config/telescope.php` 構成ファイル内で有効にするウォッチャーのリストをカスタマイズできます。

```
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

<!-- Some watchers also allow you to provide additional customization options: -->
一部のウォッチャーでは、追加のカスタマイズ オプションを提供することもできます。

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    ...
],
```

<a name="batch-watcher"></a>
<!-- ### Batch Watcher -->
### Batch Watcher

<!-- The batch watcher records information about queued [batches](/docs/10.x/queues#job-batching), including the job and connection information. -->
バッチ ウォッチャーは、ジョブや接続情報など、キューに入れられた [batches](/docs/10.x/queues#job-batching) に関する情報を記録します。

<a name="cache-watcher"></a>
<!-- ### Cache Watcher -->
### Cache Watcher

<!-- The cache watcher records data when a cache key is hit, missed, updated and forgotten. -->
キャッシュ ウォッチャーは、キャッシュ キーがヒットしたとき、ミスしたとき、更新されたとき、忘れられたときにデータを記録します。

<a name="command-watcher"></a>
<!-- ### Command Watcher -->
### Command Watcher

<!-- The command watcher records the arguments, options, exit code, and output whenever an Artisan command is executed. If you would like to exclude certain commands from being recorded by the watcher, you may specify the command in the `ignore` option within your `config/telescope.php` file: -->
コマンド ウォッチャーは、Artisan コマンドが実行されるたびに、引数、オプション、終了コード、および出力を記録します。ウォッチャーによる記録から特定のコマンドを除外したい場合は、`config/telescope.php` ファイル内の `ignore` オプションでコマンドを指定できます。

```
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    ...
],
```

<a name="dump-watcher"></a>
<!-- ### Dump Watcher -->
### Dump Watcher

<!-- The dump watcher records and displays your variable dumps in Telescope. When using Laravel, variables may be dumped using the global `dump` function. The dump watcher tab must be open in a browser for the dump to be recorded, otherwise, the dumps will be ignored by the watcher. -->
ダンプ ウォッチャーは、変数ダンプを記録し、Telescope に表示します。 Laravel を使用する場合、グローバル `dump` 関数を使用して変数をダンプすることができます。ダンプを記録するには、ブラウザでダンプ ウォッチャー タブが開かれている必要があります。そうしないと、ダンプはウォッチャーによって無視されます。

<a name="event-watcher"></a>
<!-- ### Event Watcher -->
### Event Watcher

<!-- The event watcher records the payload, listeners, and broadcast data for any [events](/docs/10.x/events) dispatched by your application. The Laravel framework's internal events are ignored by the Event watcher. -->
イベント ウォッチャーは、アプリケーションによってディスパッチされた [events](/docs/10.x/events) のペイロード、リスナ、およびブロードキャスト データを記録します。 Laravel フレームワークの内部イベントは、イベント ウォッチャーによって無視されます。

<a name="exception-watcher"></a>
<!-- ### Exception Watcher -->
### Exception Watcher

<!-- The exception watcher records the data and stack trace for any reportable exceptions that are thrown by your application. -->
例外ウォッチャーは、アプリケーションによってスローされた報告可能な例外のデータとスタック トレースを記録します。

<a name="gate-watcher"></a>
<!-- ### Gate Watcher -->
### Gate Watcher

<!-- The gate watcher records the data and result of [gate and policy](/docs/10.x/authorization) checks by your application. If you would like to exclude certain abilities from being recorded by the watcher, you may specify those in the `ignore_abilities` option in your `config/telescope.php` file: -->
ゲート ウォッチャーは、アプリケーションによる [gate and policy](/docs/10.x/authorization) チェックのデータと結果を記録します。ウォッチャーによる記録から特定の能力を除外したい場合は、`config/telescope.php` ファイルの `ignore_abilities` オプションでそれらを指定できます。

```
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    ...
],
```

<a name="http-client-watcher"></a>
<!-- ### HTTP Client Watcher -->
### HTTP Client Watcher

<!-- The HTTP client watcher records outgoing [HTTP client requests](/docs/10.x/http-client) made by your application. -->
HTTP クライアント ウォッチャーは、アプリケーションによって作成された送信 [HTTP client requests](/docs/10.x/http-client) を記録します。

<a name="job-watcher"></a>
<!-- ### Job Watcher -->
### Job Watcher

<!-- The job watcher records the data and status of any [jobs](/docs/10.x/queues) dispatched by your application. -->
ジョブ ウォッチャーは、アプリケーションによってディスパッチされた [jobs](/docs/10.x/queues) のデータとステータスを記録します。

<a name="log-watcher"></a>
<!-- ### Log Watcher -->
### Log Watcher

<!-- The log watcher records the [log data](/docs/10.x/logging) for any logs written by your application. -->
ログ ウォッチャーは、アプリケーションによって書き込まれたログの [log data](/docs/10.x/logging) を記録します。

<!-- By default, Telescope will only record logs at the `error` level and above. However, you can modify the `level` option in your application's `config/telescope.php` configuration file to modify this behavior: -->
デフォルトでは、Telescope は `error` レベル以上のログのみを記録します。ただし、アプリケーションの `config/telescope.php` 構成ファイルの `level` オプションを変更して、この動作を変更できます。

```
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a name="mail-watcher"></a>
<!-- ### Mail Watcher -->
### Mail Watcher

<!-- The mail watcher allows you to view an in-browser preview of [emails](/docs/10.x/mail) sent by your application along with their associated data. You may also download the email as an `.eml` file. -->
メール ウォッチャーを使用すると、アプリケーションによって送信された [emails](/docs/10.x/mail) とその関連データのブラウザー内プレビューを表示できます。電子メールを `.eml` ファイルとしてダウンロードすることもできます。

<a name="model-watcher"></a>
<!-- ### Model Watcher -->
### Model Watcher

<!-- The model watcher records model changes whenever an Eloquent [model event](/docs/10.x/eloquent#events) is dispatched. You may specify which model events should be recorded via the watcher's `events` option: -->
モデル ウォッチャーは、Eloquent [model event](/docs/10.x/eloquent#events) がディスパッチされるたびに、モデルの変更を記録します。ウォッチャーの `events` オプションを使用して、どのモデル イベントを記録するかを指定できます。

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

<!-- If you would like to record the number of models hydrated during a given request, enable the `hydrations` option: -->
特定のリクエスト中にハイドレートされたモデルの数を記録したい場合は、`hydrations` オプションを有効にします。

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    ...
],
```

<a name="notification-watcher"></a>
<!-- ### Notification Watcher -->
### Notification Watcher

<!-- The notification watcher records all [notifications](/docs/10.x/notifications) sent by your application. If the notification triggers an email and you have the mail watcher enabled, the email will also be available for preview on the mail watcher screen. -->
通知ウォッチャーは、アプリケーションによって送信されたすべての [notifications](/docs/10.x/notifications) を記録します。通知によって電子メールが送信され、メール ウォッチャーが有効になっている場合、その電子メールはメール ウォッチャー画面でプレビューすることもできます。

<a name="query-watcher"></a>
<!-- ### Query Watcher -->
### Query Watcher

<!-- The query watcher records the raw SQL, bindings, and execution time for all queries that are executed by your application. The watcher also tags any queries slower than 100 milliseconds as `slow`. You may customize the slow query threshold using the watcher's `slow` option: -->
クエリ ウォッチャーは、アプリケーションによって実行されるすべてのクエリの生の SQL、バインディング、および実行時間を記録します。また、ウォッチャーは、100 ミリ秒未満のクエリに `slow` としてタグ付けします。ウォッチャーの `slow` オプションを使用して、低速クエリのしきい値をカスタマイズできます。

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    ...
],
```

<a name="redis-watcher"></a>
<!-- ### Redis Watcher -->
### Redis Watcher

<!-- The Redis watcher records all [Redis](/docs/10.x/redis) commands executed by your application. If you are using Redis for caching, cache commands will also be recorded by the Redis watcher. -->
Redis ウォッチャーは、アプリケーションによって実行されたすべての [Redis](/docs/10.x/redis) コマンドを記録します。キャッシュに Redis を使用している場合、キャッシュ コマンドも Redis ウォッチャーによって記録されます。

<a name="request-watcher"></a>
<!-- ### Request Watcher -->
### Request Watcher

<!-- The request watcher records the request, headers, session, and response data associated with any requests handled by the application. You may limit your recorded response data via the `size_limit` (in kilobytes) option: -->
リクエスト ウォッチャーは、アプリケーションによって処理されるリクエストに関連付けられたリクエスト、ヘッダー、セッション、および応答データを記録します。 `size_limit` (キロバイト単位) オプションを使用して、記録された応答データを制限できます。

```
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    ...
],
```

<a name="schedule-watcher"></a>
<!-- ### Schedule Watcher -->
### Schedule Watcher

<!-- The schedule watcher records the command and output of any [scheduled tasks](/docs/10.x/scheduling) run by your application. -->
スケジュール ウォッチャーは、アプリケーションによって実行される [scheduled tasks](/docs/10.x/scheduling) のコマンドと出力を記録します。

<a name="view-watcher"></a>
<!-- ### View Watcher -->
### View Watcher

<!-- The view watcher records the [view](/docs/10.x/views) name, path, data, and "composers" used when rendering views. -->
ビュー ウォッチャーは、ビューのレンダリング時に使用される [view](/docs/10.x/views) 名、パス、データ、および「コンポーザー」を記録します。

<a name="displaying-user-avatars"></a>
<!-- ## Displaying User Avatars -->
## Displaying User Avatars

<!-- The Telescope dashboard displays the user avatar for the user that was authenticated when a given entry was saved. By default, Telescope will retrieve avatars using the Gravatar web service. However, you may customize the avatar URL by registering a callback in your `App\Providers\TelescopeServiceProvider` class. The callback will receive the user's ID and email address and should return the user's avatar image URL: -->
Telescope ダッシュボードには、特定のエントリが保存されたときに認証されたユーザーのユーザー アバターが表示されます。デフォルトでは、Telescope は Gravatar Web サービスを使用してアバターを取得します。ただし、`App\Providers\TelescopeServiceProvider` クラスにコールバックを登録することで、アバター URL をカスタマイズできます。コールバックはユーザーの ID と電子メール アドレスを受け取り、ユーザーのアバター画像 URL を返す必要があります。

```
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (string $id, string $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```

